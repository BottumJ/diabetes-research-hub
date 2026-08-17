#!/usr/bin/env python3
"""
falsify_equity_gaps.py — Falsification test for the Health Equity gap cluster.

WHY THIS EXISTS
---------------
literature_gap_report.md ranks 7 domain pairs at Gap Score ~100 with 0-1 joint
publications. Four of the top six involve "Health Equity". A cluster of perfect
zeros is as consistent with a TERMINOLOGY ARTIFACT as with a genuine open field:
"health equity" is a young literal string, while the same research publishes
under disparities / access / socioeconomic / social determinants / underserved.

This script runs each pair TWICE -- once with the narrow doctrine terms, once
with synonym-expanded terms -- and prints them side by side.

DECISION RULE (pre-committed; do not rationalize after seeing results)
---------------------------------------------------------------------
  Gaps SURVIVE expansion  (expanded joint count still ~0)
      -> genuine open field. Promote Drug Repurposing x Health Equity to an
         active Tier 1 project. Upgrade classification BRONZE -> SILVER.

  Gaps COLLAPSE           (expansion finds substantial literature)
      -> the gap-scoring keyword set is broken. This is the MORE valuable
         finding: it invalidates 4 of the top 6 gaps AND the fix improves all
         435 pairs. Rebuild the domain term sets before the next gap run.

  MIXED                   -> classify pair by pair.

Rule of thumb for "collapse": expanded_joint >= 10x narrow_joint AND
expanded_joint >= 20. Reported automatically per pair.

WHY IT ISN'T ALREADY DONE
-------------------------
The NCBI E-utilities endpoint is not reachable from the Cowork sandbox. The
monitor structurally cannot validate its own gap scores. This must run locally.

USAGE
-----
    set NCBI_API_KEY=<your key>          (Windows cmd)
    $env:NCBI_API_KEY="<your key>"       (PowerShell)
    python falsify_equity_gaps.py

    python falsify_equity_gaps.py --json out.json    # also write machine-readable

An API key is optional but raises the rate limit from 3/sec to 10/sec.
Runtime: ~30 seconds for 14 queries. No writes to any existing hub file.
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import date

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
MINDATE = "2020/01/01"
MAXDATE = date.today().strftime("%Y/%m/%d")
API_KEY = os.environ.get("NCBI_API_KEY", "")
DELAY = 0.11 if API_KEY else 0.34
TOOL = "diabetes-hub-gap-falsification"
EMAIL = "justin.bottum@gmail.com"

# ---------------------------------------------------------------------------
# Term sets. NARROW mirrors what the gap analysis appears to use.
# EXPANDED adds the synonyms the narrow term would miss.
# ---------------------------------------------------------------------------
NARROW = {
    "Health Equity":       '"health equity"',
    "Treg / CAR-T":        '("regulatory T cell" OR "CAR-T" OR Treg)',
    "Neuropathy":          '"diabetic neuropathy"',
    "Beta Cell Regen":     '("beta cell regeneration" OR "islet regeneration")',
    "Glucokinase":         '(glucokinase OR "glucokinase activator")',
    "Gene Therapy":        '"gene therapy"',
    "LADA":                '("latent autoimmune diabetes" OR LADA)',
    "Drug Repurposing":    '("drug repurposing" OR "drug repositioning")',
    "Insulin Resistance":  '"insulin resistance"',
    "Islet Transplant":    '"islet transplantation"',
}

EXPANDED = dict(NARROW)
EXPANDED["Health Equity"] = (
    '("health equity" OR "health disparities" OR "healthcare disparities" '
    'OR "social determinants" OR socioeconomic OR "access to care" '
    'OR underserved OR "health inequities" OR "racial disparities" '
    'OR "treatment access" OR affordability)'
)
EXPANDED["Treg / CAR-T"] = (
    '("regulatory T cell" OR "regulatory T cells" OR Treg OR Tregs '
    'OR "CAR-T" OR "CAR T" OR "chimeric antigen receptor" OR "TCR-Treg" '
    'OR "adoptive cell therapy" OR "immune tolerance")'
)
EXPANDED["Beta Cell Regen"] = (
    '("beta cell regeneration" OR "islet regeneration" OR "beta-cell '
    'proliferation" OR "beta cell replacement" OR "stem cell derived islet" '
    'OR "islet neogenesis" OR "beta cell mass")'
)
EXPANDED["Drug Repurposing"] = (
    '("drug repurposing" OR "drug repositioning" OR "drug reprofiling" '
    'OR "therapeutic switching" OR "off-label" OR "existing drugs")'
)
EXPANDED["Neuropathy"] = (
    '("diabetic neuropathy" OR "peripheral neuropathy" OR "diabetic '
    'polyneuropathy" OR "nerve damage" OR "diabetic foot")'
)
EXPANDED["Gene Therapy"] = (
    '("gene therapy" OR "gene editing" OR CRISPR OR "AAV vector" '
    'OR "gene transfer" OR "genetic engineering")'
)
EXPANDED["LADA"] = (
    '("latent autoimmune diabetes" OR LADA OR "slowly progressive '
    'autoimmune diabetes" OR "type 1.5 diabetes")'
)
EXPANDED["Glucokinase"] = (
    '(glucokinase OR "glucokinase activator" OR dorzagliatin OR GKA '
    'OR "hexokinase 4" OR GCK)'
)
EXPANDED["Islet Transplant"] = (
    '("islet transplantation" OR "islet cell transplant" OR "pancreatic '
    'islet transplantation" OR "islet allotransplantation" OR "islet graft")'
)

# The 7 pairs from literature_gap_report.md, in rank order.
PAIRS = [
    (1, "Treg / CAR-T",       "Neuropathy",       100.0, 0),
    (2, "Beta Cell Regen",    "Health Equity",    100.0, 0),
    (3, "Treg / CAR-T",       "Health Equity",    100.0, 0),
    (4, "Glucokinase",        "Health Equity",    100.0, 0),
    (5, "Gene Therapy",       "LADA",             100.0, 0),
    (6, "Drug Repurposing",   "Health Equity",    100.0, 0),
    (7, "Insulin Resistance", "Islet Transplant",  91.9, 1),
]

DIABETES = '(diabetes OR diabetic)'


def esearch_count(term):
    """Return PubMed hit count for a query string. Retries once on failure."""
    params = {
        "db": "pubmed", "term": term, "rettype": "count", "retmode": "json",
        "mindate": MINDATE, "maxdate": MAXDATE, "datetype": "pdat",
        "tool": TOOL, "email": EMAIL,
    }
    if API_KEY:
        params["api_key"] = API_KEY
    url = ESEARCH + "?" + urllib.parse.urlencode(params)
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = json.loads(r.read().decode())
            return int(data["esearchresult"]["count"])
        except Exception as e:
            if attempt == 2:
                print(f"    ! query failed: {e}", file=sys.stderr)
                return None
            time.sleep(2)


def joint_query(termset, d1, d2):
    return f"{DIABETES} AND {termset[d1]} AND {termset[d2]}"


def verdict(narrow, expanded):
    if narrow is None or expanded is None:
        return "ERROR"
    if expanded >= 20 and expanded >= max(10 * narrow, 10):
        return "COLLAPSED"
    if expanded <= 2:
        return "SURVIVED"
    return "PARTIAL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="also write results to this JSON file")
    args = ap.parse_args()

    print("=" * 78)
    print("HEALTH EQUITY GAP CLUSTER — FALSIFICATION TEST")
    print(f"Date range: {MINDATE} to {MAXDATE}   |   API key: "
          f"{'yes' if API_KEY else 'NO (slower, 3 req/sec)'}")
    print("=" * 78)

    results = []
    for rank, d1, d2, score, reported in PAIRS:
        print(f"\n[{rank}] {d1}  x  {d2}"
              f"   (report: gap={score}, joint={reported})")

        n = esearch_count(joint_query(NARROW, d1, d2))
        time.sleep(DELAY)
        e = esearch_count(joint_query(EXPANDED, d1, d2))
        time.sleep(DELAY)

        v = verdict(n, e)
        print(f"    narrow terms   : {n}")
        print(f"    expanded terms : {e}")
        print(f"    -> {v}")

        results.append({
            "rank": rank, "domain_1": d1, "domain_2": d2,
            "reported_gap_score": score, "reported_joint_pubs": reported,
            "narrow_joint": n, "expanded_joint": e, "verdict": v,
        })

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"{'#':<3}{'Pair':<44}{'narrow':>8}{'expand':>8}  verdict")
    print("-" * 78)
    for r in results:
        pair = f"{r['domain_1']} x {r['domain_2']}"
        print(f"{r['rank']:<3}{pair:<44}{str(r['narrow_joint']):>8}"
              f"{str(r['expanded_joint']):>8}  {r['verdict']}")

    tally = {}
    for r in results:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    print("-" * 78)
    print("Tally:", ", ".join(f"{k}={v}" for k, v in sorted(tally.items())))

    print("\nINTERPRETATION (pre-committed decision rule)")
    coll = tally.get("COLLAPSED", 0)
    surv = tally.get("SURVIVED", 0)
    if coll >= 4:
        print("  >> The gap-scoring keyword set is BROKEN. Most gaps are")
        print("     terminology artifacts, not open fields. Rebuild the domain")
        print("     term sets before the next gap run. This finding is worth")
        print("     more than the gaps were -- it affects all 435 pairs.")
    elif surv >= 4:
        print("  >> Gaps are GENUINE. Promote Drug Repurposing x Health Equity")
        print("     to an active Tier 1 project (hits Tier 1 #4 and #6).")
        print("     Upgrade gap classification BRONZE -> SILVER.")
    else:
        print("  >> MIXED. Classify pair by pair; do not treat the cluster as")
        print("     a single finding. Per-pair verdicts above are the unit.")

    print("\nNOTE: PubMed keyword search is approximate. A SURVIVED verdict is")
    print("necessary but not sufficient for a real gap -- also check Cochrane")
    print("and PROSPERO for unindexed systematic reviews before committing.")
    print("Evidence level after this run: SILVER at best (two independent")
    print("query formulations, one database). GOLD needs a second database.")

    if args.json:
        payload = {
            "generated": date.today().isoformat(),
            "date_range": {"min": MINDATE, "max": MAXDATE},
            "source": "PubMed E-utilities esearch.fcgi",
            "tally": tally,
            "results": results,
        }
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"\nWrote {args.json}")


if __name__ == "__main__":
    main()
