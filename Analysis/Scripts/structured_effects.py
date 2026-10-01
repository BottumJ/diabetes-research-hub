#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
structured_effects.py
=====================

NEW 2026-09-30. Phase 1 of SCIENCE_ARM_BUILD_CHARTER.md: the evidence
substrate.

WHY THIS EXISTS
    extract_corpus_data.py captures numbers by regex. The charter's own
    example: under `hba1c_change`, PMID 31618560 contributed [61, 17] -- a
    demographic table row. Nothing in that pipeline can tell an effect size
    from a percentage that happens to sit near the word "HbA1c", so nothing
    downstream of it is poolable.

    This file does not try to extract better. It refuses to extract at all.
    A record is WRITTEN by an analyst reading the abstract, and this script's
    only job is to make that record impossible to get wrong quietly:

      validate   every record has an effect AND a variance (CI or SE), or it
                 is rejected. A record without variance cannot be pooled and
                 must not look as though it can.
      verify     the record's `source_span` must occur VERBATIM in the PubMed
                 abstract for its PMID, fetched live, and the effect and its
                 interval must occur as numerals INSIDE that span. A number
                 that is not in the quoted sentence is not from the paper.
      compare    a second, independent extraction (a file of records made
                 without sight of the first) must agree on every numeric
                 field. Agreement is what moves a record BRONZE -> SILVER.

WHAT A GREEN RUN MEANS, AND DOES NOT
    Green means: each number is where the record says it is, and two
    extractions agree. It does NOT mean the record is the right number to
    pool -- estimand, analysis population and multi-arm correlation are
    recorded as fields precisely because this script cannot judge them.
    It reads abstracts only. A figure that exists only in the full text
    cannot be verified here and is therefore not admitted.

USAGE
    python structured_effects.py validate
    python structured_effects.py verify
    python structured_effects.py compare <second_pass.json>
    python structured_effects.py report
"""

from __future__ import annotations

import datetime
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(os.path.dirname(HERE), "Results")
LEDGER = os.path.join(RESULTS, "structured_effects.json")
CACHE = os.path.join(RESULTS, ".structured_effects_abstract_cache.json")
REPORT = os.path.join(RESULTS, "structured_effects_report.md")

EFETCH = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
          "?db=pubmed&retmode=xml&id=%s")

REQUIRED = ("record_id", "pmid", "nct_id", "trial", "intervention",
            "comparator", "population", "outcome", "effect", "effect_type",
            "unit", "timepoint", "estimand", "source_span")
EFFECT_TYPES = {"mean_difference", "change_from_baseline"}
NUMERIC = ("effect", "ci_low", "ci_high", "se", "n_arm", "n_comparator")


# --------------------------------------------------------------- normalising
def norm_text(s):
    """Collapse whitespace and unify the glyphs journals disagree on.

    The Lancet prints a raised decimal point and a true minus sign. Those are
    typography, not content, so they are folded before any comparison. Nothing
    else is folded: a verifier that is generous about text is a verifier that
    passes a paraphrase.
    """
    s = s.replace("·", ".").replace("−", "-").replace("–", "-")
    s = s.replace(" ", " ").replace(" ", " ")
    return " ".join(s.split())


def numeral_forms(x):
    """Every way a float is plausibly printed: -1.07, -1.070 is NOT added."""
    if x is None:
        return []
    forms = set()
    for fmt in ("%g", "%.1f", "%.2f", "%.3f"):
        s = fmt % abs(x)
        if abs(float(s) - abs(x)) < 1e-9:
            forms.add(s)
    return sorted(forms, key=len, reverse=True)


def numeral_in(span, x):
    """True when |x| appears in span as a whole numeral (not inside another)."""
    for f in numeral_forms(x):
        if re.search(r"(?<![\d.])%s(?![\d]|\.\d)" % re.escape(f), span):
            return True
    return False


# ------------------------------------------------------------------ schema
def validate_record(r):
    """Return a list of reasons this record is NOT admissible. Empty = valid."""
    why = []
    for k in REQUIRED:
        if r.get(k) in (None, "", []):
            why.append("missing %s" % k)
    if r.get("effect_type") not in EFFECT_TYPES:
        why.append("effect_type must be one of %s" % sorted(EFFECT_TYPES))
    if not isinstance(r.get("effect"), (int, float)):
        why.append("effect is not a number")
    has_ci = all(isinstance(r.get(k), (int, float)) for k in ("ci_low", "ci_high"))
    has_se = isinstance(r.get("se"), (int, float))
    if not (has_ci or has_se):
        why.append("no variance: needs ci_low+ci_high or se")
    if has_ci and isinstance(r.get("effect"), (int, float)):
        if not r["ci_low"] <= r["effect"] <= r["ci_high"]:
            why.append("effect %s outside its own interval [%s, %s]"
                       % (r["effect"], r["ci_low"], r["ci_high"]))
    if not re.fullmatch(r"\d{6,9}", str(r.get("pmid", ""))):
        why.append("pmid malformed")
    if not re.fullmatch(r"NCT\d{8}", str(r.get("nct_id", ""))):
        why.append("nct_id malformed")
    return why


def load():
    with open(LEDGER, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save(doc):
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ------------------------------------------------------------------- fetch
def fetch_abstract(pmid, cache):
    """Live PubMed abstract text. Cache is a fallback for an offline run only,
    and a record verified from cache says so."""
    for attempt in range(3):                      # NCBI answers 429 under load
        try:
            with urllib.request.urlopen(EFETCH % pmid, timeout=30) as resp:
                root = ET.fromstring(resp.read())
            parts = ["".join(a.itertext()) for a in root.iter("AbstractText")]
            text = norm_text(" ".join(parts))
            if text:
                cache[str(pmid)] = {"fetched": datetime.date.today().isoformat(),
                                    "abstract": text}
                return text, "live"
            break
        except Exception as exc:                  # network, parse, rate limit
            print("    (live fetch failed for %s, attempt %d: %s)"
                  % (pmid, attempt + 1, exc))
            time.sleep(3 * (attempt + 1))
    hit = cache.get(str(pmid))
    return (hit["abstract"], "cache:%s" % hit["fetched"]) if hit else (None, None)


# ---------------------------------------------------------------- commands
def cmd_validate(doc):
    bad = 0
    ids = [r.get("record_id") for r in doc["records"]]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        print("  INVALID duplicate record_id %s" % dup)
        bad += 1
    for r in doc["records"]:
        why = validate_record(r)
        if why:
            bad += 1
            print("  INVALID %s: %s" % (r.get("record_id"), "; ".join(why)))
    print("[%s] structured_effects validate: %d records, %d invalid"
          % ("FAIL" if bad else "OK", len(doc["records"]), bad))
    return 1 if bad else 0


def cmd_verify(doc):
    cache = {}
    if os.path.exists(CACHE):
        with open(CACHE, "r", encoding="utf-8") as fh:
            cache = json.load(fh)
    abstracts, failed = {}, 0
    for r in doc["records"]:
        if validate_record(r):
            continue                               # validate reports these
        pmid = str(r["pmid"])
        if pmid not in abstracts:
            abstracts[pmid] = fetch_abstract(pmid, cache)
            time.sleep(0.5)
        text, origin = abstracts[pmid]
        span = norm_text(r["source_span"])
        problems = []
        if text is None:
            problems.append("abstract unavailable")
        elif span not in text:
            problems.append("source_span is not verbatim in the abstract")
        for k in ("effect", "ci_low", "ci_high", "se"):
            if r.get(k) is not None and not numeral_in(span, r[k]):
                problems.append("%s=%s is not a numeral in source_span" % (k, r[k]))
        r.setdefault("verification", {})["span_check"] = {
            "status": "FAIL" if problems else "PASS",
            "checked": datetime.date.today().isoformat(),
            "abstract_origin": origin,
            "problems": problems,
        }
        if problems:
            failed += 1
            print("  FAIL %s: %s" % (r["record_id"], "; ".join(problems)))
    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, indent=2, ensure_ascii=False)
    grade(doc)
    save(doc)
    print("[%s] structured_effects verify: %d records, %d failed span check"
          % ("FAIL" if failed else "OK", len(doc["records"]), failed))
    return 1 if failed else 0


def cmd_compare(doc, second_path):
    with open(second_path, "r", encoding="utf-8") as fh:
        second_doc = json.load(fh)
    second = second_doc.get("records", second_doc) if isinstance(second_doc, dict) else second_doc
    # Matched on what the record IS, never on record_id: a second extractor
    # who is handed the first pass's ids has been handed the first pass.
    def key(r):
        return (str(r.get("pmid")), norm_text(str(r.get("intervention", ""))).lower(),
                norm_text(str(r.get("comparator", ""))).lower())
    by_key = {}
    for s in second:
        by_key.setdefault(key(s), []).append(s)
    disagreed = 0
    # A second-pass file covers the papers it was given, not the whole ledger.
    # Records from other papers keep the second_pass result they already have.
    covered = {str(s.get("pmid")) for s in second}
    covered |= {str(e.get("pmid")) for e in (second_doc.get("excluded", [])
                                            if isinstance(second_doc, dict) else [])}
    for r in doc["records"]:
        if str(r["pmid"]) not in covered:
            continue
        hits = by_key.get(key(r), [])
        diffs = []
        if len(hits) != 1:
            diffs.append("%d second-pass records match this pmid/intervention/"
                         "comparator (need exactly 1)" % len(hits))
        else:
            for k in NUMERIC:
                a, b = r.get(k), hits[0].get(k)
                if a is None and b is None:
                    continue
                if a is None or b is None or abs(float(a) - float(b)) > 1e-9:
                    diffs.append("%s: first=%s second=%s" % (k, a, b))
            if norm_text(str(r.get("timepoint"))).lower() != \
               norm_text(str(hits[0].get("timepoint"))).lower():
                diffs.append("timepoint: first=%s second=%s"
                             % (r.get("timepoint"), hits[0].get("timepoint")))
        r.setdefault("verification", {})["second_pass"] = {
            "status": "DISAGREE" if diffs else "AGREE",
            "checked": datetime.date.today().isoformat(),
            "method": doc.get("second_pass_method", "independent re-extraction"),
            "differences": diffs,
        }
        if diffs:
            disagreed += 1
            print("  DISAGREE %s: %s" % (r["record_id"], "; ".join(diffs)))
    first_keys = {key(r) for r in doc["records"] if str(r["pmid"]) in covered}
    extra = [s for s in second if key(s) not in first_keys]
    for s in extra:
        print("  SECOND PASS ONLY (first pass has no such record): pmid %s | %s vs %s"
              % (s.get("pmid"), s.get("intervention"), s.get("comparator")))
    grade(doc)
    save(doc)
    print("[%s] structured_effects compare: %d records, %d disagree, "
          "%d found only by the second pass"
          % ("FAIL" if disagreed or extra else "OK", len(doc["records"]),
             disagreed, len(extra)))
    return 1 if disagreed or extra else 0


def grade(doc):
    """BRONZE until the span check passes AND a second pass agrees -> SILVER.
    Never GOLD from here: GOLD needs replication, which is a fact about the
    world and not about this file."""
    for r in doc["records"]:
        v = r.get("verification", {})
        ok = (not validate_record(r)
              and v.get("span_check", {}).get("status") == "PASS"
              and v.get("second_pass", {}).get("status") == "AGREE")
        r["evidence_level"] = "SILVER" if ok else "BRONZE"
        r["poolable"] = bool(ok)


def cmd_report(doc):
    grade(doc)
    lines = ["# Structured Effects - Standings", "",
             "_Generated %s by structured_effects.py_" % datetime.date.today().isoformat(),
             ""]
    clusters = {}
    for r in doc["records"]:
        clusters.setdefault(r.get("cluster", "(none)"), []).append(r)
    for name, rows in sorted(clusters.items()):
        n_ok = sum(1 for r in rows if r.get("poolable"))
        lines += ["## %s" % name, "",
                  "%d records, %d poolable (schema-valid, span-verified, "
                  "second-pass agreed)." % (len(rows), n_ok), "",
                  "| Trial | PMID | Intervention | Comparator | Effect (95% CI) | Week | Level |",
                  "|---|---|---|---|---|---|---|"]
        for r in rows:
            ci = ("%s to %s" % (r.get("ci_low"), r.get("ci_high"))
                  if r.get("ci_low") is not None else "SE %s" % r.get("se"))
            lines.append("| %s | %s | %s | %s | %s (%s) | %s | %s |" % (
                r.get("trial"), r.get("pmid"), r.get("intervention"),
                r.get("comparator"), r.get("effect"), ci,
                r.get("timepoint"), r.get("evidence_level")))
        lines.append("")
    if doc.get("excluded"):
        lines += ["## Considered and not admitted", ""]
        for e in doc["excluded"]:
            lines.append("- **%s** (PMID %s): %s" % (e["trial"], e["pmid"], e["reason"]))
        lines.append("")
    lines += ["---",
              "_No pooled estimate is produced here. Records from one trial "
              "share a comparator arm and are correlated; pooling them as "
              "independent would understate the variance._"]
    with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print("[OK] wrote %s" % os.path.relpath(REPORT, os.path.dirname(HERE)))
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] not in ("validate", "verify", "compare", "report"):
        print(__doc__)
        return 2
    doc = load()
    if argv[1] == "validate":
        return cmd_validate(doc)
    if argv[1] == "verify":
        return cmd_validate(doc) or cmd_verify(doc)
    if argv[1] == "compare":
        if len(argv) < 3:
            print("compare needs the second-pass file")
            return 2
        return cmd_compare(doc, argv[2])
    return cmd_report(doc)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
