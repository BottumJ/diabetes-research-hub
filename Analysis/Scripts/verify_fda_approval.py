#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_fda_approval.py
======================

NEW 2026-09-30. Closes open finding E-01 / N-06: FDA actions were being
reported from press coverage and search summaries, never from FDA.

THE PROCESS, in the order it has to be done
    1. Look the product up in Drugs@FDA through openFDA
       (api.fda.gov/drug/drugsfda.json) by BRAND name under
       products.brand_name. The openfda.* fields are empty for recent
       approvals, so searching them returns 404 for a product that exists.
    2. Read the application's submissions. An approval is a submission with
       status AP. ORIG-1 is the original approval; SUPPL-n with class
       "Efficacy" is a new indication or population. The date is
       submission_status_date, which is the action date on the letter and can
       be a day EARLIER than the date in press coverage.
    3. An approved supplement proves that SOMETHING was approved that day. It
       does not say what. Open the approval letter attached to that
       submission and read the sentence that states the indication. That
       sentence, the application number and the action date are the citation.

    Step 3 is the one press coverage cannot substitute for. On 2026-09-30 it
    showed that Onswik (insulin efsitora alfa) is approved for TYPE 2 diabetes
    only, and that Kerendia's type 1 indication is worded around a surrogate:
    "to reduce urinary albumin-to-creatinine ratio, which is expected to
    reduce the risk of" kidney outcomes.

USAGE
    python verify_fda_approval.py KERENDIA
    python verify_fda_approval.py ONSWIK --since 2026-01-01

    Prints each approved submission on or after --since with the indication
    sentence found in its letter, and writes fda_approval_verification.json.
    Exit 1 if the brand is not found or no letter text could be read.

Requires pypdf for step 3. Letters are read in memory; nothing is saved.
"""

from __future__ import annotations

import datetime
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "Results", "fda_approval_verification.json")
API = "https://api.fda.gov/drug/drugsfda.json?search=%s&limit=1"
# accessdata.fda.gov answers 404 to a non-browser User-Agent.
UA = {"User-Agent": "Mozilla/5.0 DiabetesResearchHub/1.0"}

# The sentences an approval letter uses to say what it approved.
INDICATION_RE = re.compile(
    r"(provides for the following new indication[s]?:.*?(?=APPROVAL|We have completed)"
    r"|provides for .*?(?=APPROVAL|We have completed)"
    r"|is indicated .*?\.)", re.S)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()


def letter_text(url):
    import pypdf
    reader = pypdf.PdfReader(io.BytesIO(get(url)))
    return " ".join(" ".join((p.extract_text() or "") for p in reader.pages[:2]).split())


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    brand = argv[1].upper()
    since = argv[argv.index("--since") + 1] if "--since" in argv else "1900-01-01"
    since = since.replace("-", "")

    query = urllib.parse.quote('products.brand_name:"%s"' % brand)
    try:
        app = json.loads(get(API % query))["results"][0]
    except Exception as exc:
        print("[FAIL] %s not found in Drugs@FDA via openFDA: %s" % (brand, exc))
        return 1

    print("%s  %s  %s" % (brand, app["application_number"], app.get("sponsor_name")))
    rows, read_any = [], False
    for sub in sorted(app.get("submissions", []),
                      key=lambda s: s.get("submission_status_date", ""), reverse=True):
        date = sub.get("submission_status_date", "")
        if sub.get("submission_status") != "AP" or date < since:
            continue
        letters = [d["url"] for d in sub.get("application_docs", []) if d.get("type") == "Letter"]
        indication, problem = None, None
        if not letters:
            problem = "no approval letter attached to this submission"
        else:
            try:
                m = INDICATION_RE.search(letter_text(letters[0]))
                indication = m.group(1).strip() if m else None
                problem = None if m else "letter read, no indication sentence recognised - read it by hand"
                read_any = read_any or bool(m)
            except Exception as exc:
                problem = "letter could not be read: %s" % exc
        row = {
            "brand": brand, "application": app["application_number"],
            "submission": "%s-%s" % (sub.get("submission_type"), sub.get("submission_number")),
            "class": sub.get("submission_class_code_description"),
            "action_date": "%s-%s-%s" % (date[:4], date[4:6], date[6:8]),
            "letter_url": letters[0] if letters else None,
            "indication_as_stated_in_letter": indication,
            "problem": problem,
        }
        rows.append(row)
        print("  %s  %-9s %-32s %s" % (row["action_date"], row["submission"],
                                       row["class"] or "", problem or ""))
        if indication:
            print("      %s" % indication[:400].encode("ascii", "replace").decode())

    stored = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            stored = json.load(fh)
    stored[brand] = {"checked": datetime.date.today().isoformat(),
                     "source": "openFDA drugsfda + the approval letter on accessdata.fda.gov",
                     "approved_submissions": rows}
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(stored, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    if not rows:
        print("[FAIL] no approved submission on or after %s" % since)
        return 1
    if not read_any:
        print("[FAIL] approvals found, but no letter yielded an indication sentence")
        return 1
    print("[OK] %d approved submission(s); indication read from the letter" % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
