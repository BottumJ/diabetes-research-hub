"""Probe: are the two low-count PubMed alert queries over-narrowed?

Written by the 2026-09-18 monitor run. The sandbox cannot reach E-utilities,
so this runs locally. Read-only: issues esearch counts, writes nothing.

Context (monitor_report_2026-09-18.md §3a):
  Two of the 16 alert domains returned a 30-day count of 1.
  Both are triple conjunctions with a narrow third clause.
  Expected counts derived from the gap analysis's own 2020+ totals:
      Drug Repurposing   622 pubs  ->  ~7.6 / 30d   observed 1   (0.13x)
      Epigenetics      7,811 pubs  -> ~95.5 / 30d   observed 1   (0.01x)

Decision rule, fixed in advance:
  If dropping the third clause raises the 30-day count by MORE THAN 5x,
  the query is over-narrowed -> widen it in baseline_pubmed_alerts.py.
  If it does not, the low counts are real and gap #3's Tier 1 opening
  (Islet Transplant x Drug Repurposing) is STRENGTHENED, not undermined.

Usage:
    python Analysis/Scripts/_probe_query_narrowing.py
"""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# Optional but polite; NCBI raises your rate limit if you set these.
TOOL = "diabetes_research_hub"
EMAIL = ""  # put your email here to lift the rate limit to 3 req/s cleanly

# label -> (query, paired_with)  paired_with links a narrowed query to its wide form
PROBES = [
    ("Drug Repurpose  [current, triple]",
     'diabetes AND ("drug repurposing" OR "drug repositioning") '
     'AND (computational OR network OR screening)', None),
    ("Drug Repurpose  [3rd clause dropped]",
     'diabetes AND ("drug repurposing" OR "drug repositioning")',
     "Drug Repurpose  [current, triple]"),

    ("Epigenetics     [current, triple]",
     'diabetes AND (epigenetic OR methylation) AND (GWAS OR "genome-wide")', None),
    ("Epigenetics     [3rd clause dropped]",
     'diabetes AND (epigenetic OR methylation)',
     "Epigenetics     [current, triple]"),

    # Gap-script strings. The monitor report could not make a like-for-like
    # comparison because the gap script and the alert script use different
    # domain strings. These two supply it.
    ("GAP: Drug Repurposing", '"drug repurposing" AND diabetes', None),
    ("GAP: Islet Transplant", '"islet transplantation"', None),
]


def count(term, reldate=None):
    """Return the PubMed hit count for `term`, optionally windowed to reldate days."""
    params = {"db": "pubmed", "term": term, "retmax": 0, "retmode": "json",
              "tool": TOOL}
    if EMAIL:
        params["email"] = EMAIL
    if reldate:
        params["reldate"] = reldate
        params["datetype"] = "pdat"
    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return int(json.load(r)["esearchresult"]["count"])
    except (urllib.error.URLError, KeyError, ValueError) as e:
        print(f"    ! query failed: {e}", file=sys.stderr)
        return None


def main():
    results = {}
    print(f"{'probe':38} {'30d':>8} {'all-time':>10}")
    print("-" * 58)
    for label, term, _ in PROBES:
        c30 = count(term, reldate=30)
        time.sleep(0.4)                      # NCBI: <=3 req/s unauthenticated
        call = count(term)
        time.sleep(0.4)
        results[label] = c30
        s30 = "ERR" if c30 is None else f"{c30:,}"
        sall = "ERR" if call is None else f"{call:,}"
        print(f"{label:38} {s30:>8} {sall:>10}")

    print("\n" + "=" * 58)
    print("VERDICT (rule: >5x on the 30-day count => over-narrowed)")
    print("=" * 58)
    for label, _, paired_with in PROBES:
        if not paired_with:
            continue
        wide, narrow = results.get(label), results.get(paired_with)
        if wide is None or narrow is None:
            print(f"  {paired_with.split('[')[0].strip():18} inconclusive (query error)")
            continue
        if narrow == 0:
            ratio = float("inf")
        else:
            ratio = wide / narrow
        verdict = "OVER-NARROWED -> widen" if ratio > 5 else "low count is REAL"
        print(f"  {paired_with.split('[')[0].strip():18} "
              f"{narrow} -> {wide}  ({ratio:.1f}x)  {verdict}")

    print("\nIf 'Drug Repurpose' reads OVER-NARROWED, re-check gap #3's domain count")
    print("against 'GAP: Drug Repurposing' above before relying on its 100.0 score.")


if __name__ == "__main__":
    main()
