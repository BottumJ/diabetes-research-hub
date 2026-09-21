#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_endpoint_value_agreement.py
=================================

NEW 2026-09-21, from three live defects found the same day in
build_gap_deep_dives.py, all concerning ONE paper -- Wisel et al.,
Transpl Int 2023, PMID 37359825.

WHAT THE PAPER SAYS (verbatim, abstract, fetched live this run):

    "Ten consecutive non-uremic patients with Type 1 diabetes underwent islet
     transplant with immunosuppression based on belatacept (BELA; n = 5) or
     efalizumab (EFA; n = 5). ... 70% of patients (four EFA, three BELA)
     maintained insulin independence at 10 years post-islet transplant ...
     60% remain insulin independent at mean follow-up of 13.3 +/- 1.1 years"

ONE series, TEN patients, TWO timepoints.

WHAT THIS REPOSITORY PUBLISHED:

  (1) "Calcineurin-sparing alternatives: Belatacept 70% at 10yr, Efalizumab
      60% at 13.3yr" -- a difference of TIMEPOINT re-read as a difference of
      DRUG, inventing two per-drug rates the paper never reports, and handing
      belatacept the better number when efalizumab contributed MORE of the
      seven responders (four vs three).
  (2) The same invention repeated in the clinical_pipeline field.
  (3) "Validated graft survival: 6/10 insulin-independent at 10 years
      (PMID:37359825)" -- the 13.3-year NUMERATOR pinned to the 10-year
      ENDPOINT, so the file stated 70%-at-10y and 6/10-at-10y for one paper.

--------------------------------------------------------------------------
THIS GATE'S FIRST DESIGN WAS WRONG, AND SAYING SO IS THE POINT OF THIS NOTE
--------------------------------------------------------------------------
The first version associated a value with "the sole PMID within 900
characters". Its first run on the pre-fix file reported one conflict:
PMID 40544428 at 1 year holding 61%, 61%, 67%, 61%. That is not a defect.
61% is Edmonton and 67% is LANTIDRA -- two different cohorts that correctly
have different 1-year rates, both discussed near one citation. The gate had
manufactured a contradiction out of proximity, which is precisely the failure
its own docstring claimed to have made impossible, and precisely the failure
the 2026-09-15 surname gate (103 reported, nearly all invented) and the
2026-09-18 coordinate gate already taught this repository. Proximity is not
attribution. A gate that infers the link will eventually demand that a
correct statement be made wrong to turn it green.

So attribution here is EXPLICIT ONLY: a value belongs to an identifier when
the author wrote them in the SAME STATEMENT (same source line). Nothing is
inferred from distance, ever.

That honesty costs the gate its grip on defect (3): measured under the strict
rule, 37359825-at-10-years appears in only one identifier-bearing statement,
so there is no pair to compare and the conflict check is silent on it. A gate
that cannot catch the defect that motivated it is worth little, so measuring
why exposed the condition that actually ENABLED all three defects:

    46 endpoint-values exist in builder source. FOUR carry an identifier in
    the same statement. FORTY-TWO carry none at all.

"Belatacept 70% at 10yr" was not mis-cited. It was never cited. A reader
meets a clinical percentage with no source, no denominator and no cohort, and
the only reason it looks authoritative is the company it keeps. Twenty-one of
the forty-two sit in build_gap_deep_dives.py alone.

--------------------------------------------------------------------------
WHAT THIS GATE DOES
--------------------------------------------------------------------------
A. UNSOURCED (the ratchet -- THE ONLY PART THAT FAILS THE BUILD). Counts
   endpoint-values in builder source with no PMID/NCT in the same statement.
   Purely mechanical: an identifier is on the line or it is not, and no
   judgment enters. The backlog is too large to fail on outright -- failing
   the build on numbers that have been uncited for months would block every
   other repair -- so it is ratcheted against a recorded baseline. It may
   fall; it may never rise. A NEW uncited clinical percentage fails the build
   the day it is added.

B. CONFLICT (REPORT ONLY -- deliberately does NOT fail the build). Two
   identifier-bearing statements in one file giving different values for the
   same (identifier, timepoint) pair, with "70%" and "7/10" normalised alike.

   WHY B ONLY REPORTS, which is the second thing this gate learned the hard
   way. An adversarial re-check of this file on the day it was written
   produced two false positives that are not fixable by regex:

       "61% at 5 years in adults ... 32% at 5 years in children"   (subgroups)
       "insulin independence 44% at 1 year ... C-peptide 90% at 1 year"
                                                        (distinct outcomes)

   Both are correct writing. The gate keys on (identifier, TIMEPOINT); it does
   not and cannot parse WHAT IS BEING MEASURED. Any paper reporting two
   outcomes, or two subgroups, at one timepoint will trip it. A heuristic
   filter below suppresses the clearest cases by comparing the outcome words
   around each value, but a filter that works most of the time is not a
   licence to fail a build -- that is the surname gate's 2026-09-15 mistake
   and the coordinate gate's 2026-09-18 mistake, and this repository has now
   made it twice. So B prints, a human adjudicates, and the build stays green.
   Calling a heuristic a gate is how correct text gets edited into wrong text
   to turn a stage green.

Timepoints must match EXACTLY after normalisation: 10y and 13.3y are never
compared. Treating them as comparable is what created defect (1).

DELIBERATE LIMITS, so no future run overreads a green line:
  * Conflict buckets are per-file. The cross-file case is structurally
    invisible here -- and it is real: the same invented belatacept figure was
    live in THREE builders with THREE different comparators on 2026-09-21,
    and only reading them side by side showed it.
  * This gate proves two statements disagree, or that one has no source. It
    never says which is right, and it CANNOT see a claim that is wrong but
    consistently repeated. Defects (1) and (2) are exactly that case and were
    found by reading the paper, not by any gate.
  * Correction prose quotes old wrong values deliberately, so comment lines
    and lines near a CORRECTED/FLAGGED marker are excluded (the 2026-09-14
    count-inflation finding). THIS EXCLUSION IS EVADABLE -- a live line
    containing the word "CORRECTED" is skipped. It is a convenience for
    honest authors, not a security boundary, and it is one more reason B does
    not fail.
  * Green means "no NEW uncited clinical percentage". That is a floor, not a
    warrant.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(os.path.dirname(HERE), "Results")
OUT = os.path.join(RESULTS, "endpoint_value_agreement_audit.json")
BASELINE = os.path.join(RESULTS, "endpoint_value_unsourced_baseline.json")

TOLERANCE = 0.015

ID_RE = re.compile(r"(?:PMID[:\s]*(\d{6,9})|\b(NCT\d{8})\b)", re.I)

VALUE_RE = re.compile(
    r"(?P<val>\d{1,3}(?:\.\d+)?\s*%|\b\d{1,3}\s*/\s*\d{1,3}\b)"
    r"(?P<mid>[^.;|\n\"']{0,60}?)"
    r"\bat\s+(?P<num>\d{1,3}(?:\.\d+)?)\s*(?:-|\s)?\s*(?P<unit>years?|yrs?|yr|months?|mo)\b",
    re.I,
)

CORRECTION_MARKERS = re.compile(
    r"CORRECTED|FLAGGED|previously (?:read|attributed|said)|this field previously|"
    r"used to read|WITHDRAWN|NOT CHANGED|invented|defect",
    re.I,
)


def normalise_value(raw):
    raw = raw.strip()
    if raw.endswith("%"):
        try:
            return float(raw[:-1].strip()) / 100.0
        except ValueError:
            return None
    if "/" in raw:
        a, b = raw.split("/", 1)
        try:
            a, b = float(a.strip()), float(b.strip())
        except ValueError:
            return None
        return None if b == 0 else a / b
    return None


def normalise_endpoint(num, unit):
    years = float(num) / 12.0 if unit.lower().startswith("mo") else float(num)
    return "%.1fy" % years


STOPWORDS = {
    "the", "a", "an", "of", "in", "with", "and", "or", "at", "to", "for", "on",
    "was", "were", "is", "are", "by", "vs", "versus", "from", "this", "that",
    "patients", "patient", "group", "groups", "rate", "rates", "data",
    # timepoint words carry no information about WHAT is measured, and leaving
    # them in inflates overlap between two genuinely different statements
    "year", "years", "month", "months", "yrs",
}

# Words that partition a cohort. If two statements differ on one of these, they
# describe DIFFERENT PEOPLE and their values are not expected to agree. Closed,
# explicit list: guessing at subgroups is how a gate invents a defect.
SUBGROUP_MARKERS = {
    "adults", "adult", "children", "child", "paediatric", "pediatric",
    "men", "women", "male", "female", "males", "females",
    "responders", "nonresponders", "placebo", "control", "controls",
    "treated", "untreated", "intervention", "baseline", "failure", "success",
    "black", "white", "hispanic", "asian",
}


def outcome_key(line, match):
    """Words that say WHAT is measured and IN WHOM, around one value.

    Takes the text immediately before the value and immediately after the
    timepoint. Two values are comparable only if these agree. This suppresses
    the two false-positive classes found by adversarial review on the day this
    gate was written -- subgroup splits ("in adults" / "in children") and two
    different outcomes at one timepoint ("insulin independence" / "C-peptide
    positivity"). It is a NOISE FILTER, not a proof of comparability, which is
    why the conflict check it feeds only reports and never fails a build.
    """
    before = line[max(0, match.start() - 70):match.start()]
    after = line[match.end():match.end() + 70]
    blob = (before + " " + match.group("mid") + " " + after).lower()
    blob = re.sub(r"pmid[:\s]*\d+|nct\d+", " ", blob)
    blob = re.sub(r"[^a-z\s]", " ", blob)
    toks = {t for t in blob.split() if len(t) > 2 and t not in STOPWORDS}
    return frozenset(toks)


def comparable(key_a, key_b):
    """True when two outcome keys plausibly describe the same measurement."""
    # Differ on a cohort-partition word -> different people, not a conflict.
    if (key_a ^ key_b) & SUBGROUP_MARKERS:
        return False
    if not key_a or not key_b:
        return True                    # no descriptive words either side: allow
    overlap = key_a & key_b
    smaller = min(len(key_a), len(key_b))
    return smaller > 0 and len(overlap) / float(smaller) >= 0.34


def harvest(path):
    """Return (attributed_rows, unsourced_rows) for one builder file."""
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")

    attributed, unsourced = [], []
    for n, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue                       # comment: correction prose, not a claim
        if CORRECTION_MARKERS.search(line):
            continue
        # a correction comment immediately above suppresses the line it repairs
        window = "\n".join(lines[max(0, n - 6):n - 1])
        if CORRECTION_MARKERS.search(window) and "#" in window:
            continue

        for m in VALUE_RE.finditer(line):
            value = normalise_value(m.group("val"))
            if value is None or not 0.0 <= value <= 1.0:
                continue
            endpoint = normalise_endpoint(m.group("num"), m.group("unit"))
            ids = sorted({(a or b) for a, b in ID_RE.findall(line)})
            row = {
                "line": n,
                "display": m.group("val").strip(),
                "value": value,
                "endpoint": endpoint,
                "context": " ".join(line.strip().split())[:160],
                "outcome_key": outcome_key(line, m),
            }
            if len(ids) == 1:
                row["identifier"] = ids[0]
                attributed.append(row)
            elif len(ids) == 0:
                unsourced.append(row)
            # 2+ identifiers on one line: ambiguous, deliberately neither bucket
    return attributed, unsourced


def main():
    targets = sorted(
        os.path.join(HERE, f)
        for f in os.listdir(HERE)
        if f.endswith(".py") and not f.startswith(("_", "audit_"))
    )

    conflicts, unsourced_by_file = [], {}
    attributed_total = unsourced_total = 0

    for path in targets:
        name = os.path.basename(path)
        attributed, unsourced = harvest(path)
        attributed_total += len(attributed)
        if unsourced:
            unsourced_total += len(unsourced)
            unsourced_by_file[name] = [
                {"line": r["line"], "value": r["display"],
                 "endpoint": r["endpoint"], "context": r["context"]}
                for r in unsourced
            ]

        buckets = defaultdict(list)
        for r in attributed:
            buckets[(r["identifier"], r["endpoint"])].append(r)
        for (ident, endpoint), rows in sorted(buckets.items()):
            rows = sorted(rows, key=lambda x: x["line"])
            for i in range(len(rows)):
                for j in range(i + 1, len(rows)):
                    a, b = rows[i], rows[j]
                    if abs(a["value"] - b["value"]) <= TOLERANCE:
                        continue
                    # Different outcome or different subgroup -> not comparable.
                    if not comparable(a["outcome_key"], b["outcome_key"]):
                        continue
                    conflicts.append({
                        "file": name, "identifier": ident, "endpoint": endpoint,
                        "shared_outcome_words": sorted(
                            a["outcome_key"] & b["outcome_key"])[:8],
                        "statements": [
                            {"line": r["line"], "value": r["display"],
                             "normalised": round(r["value"], 4),
                             "context": r["context"]}
                            for r in (a, b)
                        ],
                    })

    # ---- ratchet ---------------------------------------------------------
    baseline = None
    if os.path.exists(BASELINE):
        try:
            with open(BASELINE, "r", encoding="utf-8") as fh:
                baseline = json.load(fh)
        except Exception:
            baseline = None

    if baseline is None:
        baseline = {
            "established": datetime.date.today().isoformat(),
            "unsourced_total": unsourced_total,
            "note": ("Baseline set the day this gate was built. It is a debt "
                     "ledger, not a target. It may fall and must never rise."),
        }
        with open(BASELINE, "w", encoding="utf-8") as fh:
            json.dump(baseline, fh, indent=2)
        ratchet = "BASELINE_ESTABLISHED"
    elif unsourced_total > baseline["unsourced_total"]:
        ratchet = "REGRESSED"
    elif unsourced_total < baseline["unsourced_total"]:
        baseline["unsourced_total"] = unsourced_total
        baseline["last_lowered"] = datetime.date.today().isoformat()
        with open(BASELINE, "w", encoding="utf-8") as fh:
            json.dump(baseline, fh, indent=2)
        ratchet = "IMPROVED"
    else:
        ratchet = "HELD"

    # ONLY the ratchet fails. Conflicts report. See section B of the docstring:
    # the conflict check cannot parse what is being measured, so it cannot be
    # allowed to force an edit.
    status = "FAIL" if ratchet == "REGRESSED" else "OK"

    verdict = {
        "audit": "endpoint_value_agreement",
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "files_scanned": len(targets),
        "values_attributed_same_statement": attributed_total,
        "values_unsourced": unsourced_total,
        "unsourced_baseline": baseline["unsourced_total"],
        "ratchet": ratchet,
        "conflicts": conflicts,
        "unsourced_by_file": unsourced_by_file,
        "status": status,
    }
    os.makedirs(RESULTS, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(verdict, fh, indent=2)

    print("[%s] endpoint_value_agreement: %d files | %d values cited in-statement | "
          "%d unsourced (baseline %d, %s) | %d conflicts"
          % (status, len(targets), attributed_total, unsourced_total,
             baseline["unsourced_total"], ratchet, len(conflicts)))
    for c in conflicts:
        print("  CONFLICT (report only, adjudicate by hand) %s %s at %s"
              % (c["file"], c["identifier"], c["endpoint"]))
        for s in c["statements"]:
            print("    line %-5d %-8s %s" % (s["line"], s["value"], s["context"][:110]))
    if ratchet == "REGRESSED":
        print("  RATCHET REGRESSED: %d unsourced endpoint-values, baseline %d. "
              "A clinical percentage was added without a citation on its line."
              % (unsourced_total, baseline["unsourced_total"]))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
