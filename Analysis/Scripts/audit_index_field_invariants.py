#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_index_field_invariants.py
===============================

NEW 2026-09-19. The paper library index carried, for at least 33 days:

    metadata.pmc_available    174
    metadata.fulltext_fetched 150
    records with a pmcid        1  of 347
    records with has_fulltext   0  of 347

Cause: convert_pmids_to_pmcids() keyed its map by int, build_index() looked it
up by str. The download loop iterates the map directly, so 150 full texts were
fetched and saved while the index recorded none of them.

NOT ONE gate in this repository looked at that, because every gate here checks
the CONTENT of assertions (PMIDs, titles, authors, numbers). This one checks an
INTERNAL CONSISTENCY INVARIANT of a data file: a summary count and the records
it summarises must agree. The class of bug it catches is the silent lookup miss,
which produces confident, well-formed, empty fields - and the published Paper
Library dashboard rendered exactly that: "PMC Available: 174" above 347 rows
that every one of them read "Abstract" or "Metadata only".

Invariants checked:
  I1  metadata.fulltext_fetched > 0  =>  records with has_fulltext > 0
  I2  metadata.pmc_available    > 0  =>  records with pmcid        > 0
  I3  count of fulltext/*.json on disk vs records with has_fulltext, within a
      declared tolerance for full texts whose PMID is not indexed (reported,
      not failed -- that is an ingestion gap, a different question)
  I4  metadata.total_indexed (when present) == len(papers)

Usage:
    python audit_index_field_invariants.py          # measure, exit 0
    python audit_index_field_invariants.py --gate   # exit 1 on I1/I2/I4 break

Output: Analysis/Results/index_field_invariants.json
"""

import glob
import json
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RESULTS = os.path.join(REPO, "Analysis", "Results")
LIB = os.path.join(RESULTS, "paper_library")
INDEX = os.path.join(LIB, "index.json")
OUT = os.path.join(RESULTS, "index_field_invariants.json")


def main():
    gate = "--gate" in sys.argv
    print("=" * 62)
    print("  PAPER INDEX FIELD INVARIANTS")
    print("=" * 62)
    if not os.path.exists(INDEX):
        print("  [SKIP] no index.json")
        return 0
    with open(INDEX, encoding="utf-8") as fh:
        index = json.load(fh)
    meta = index.get("metadata", {}) or {}
    papers = index.get("papers", {}) or {}

    rec_pmcid = sum(1 for e in papers.values() if (e or {}).get("pmcid"))
    rec_ft = sum(1 for e in papers.values() if (e or {}).get("has_fulltext"))
    rec_abs = sum(1 for e in papers.values() if (e or {}).get("has_abstract"))
    on_disk = len(glob.glob(os.path.join(LIB, "fulltext", "*.json")))

    print(f"  papers indexed            : {len(papers)}")
    print(f"  metadata.pmc_available    : {meta.get('pmc_available')}")
    print(f"  metadata.fulltext_fetched : {meta.get('fulltext_fetched')}")
    print(f"  records with pmcid        : {rec_pmcid}")
    print(f"  records with has_fulltext : {rec_ft}")
    print(f"  records with has_abstract : {rec_abs}")
    print(f"  fulltext files on disk    : {on_disk}")
    print()

    breaks, notes = [], []

    def claimed(key):
        v = meta.get(key)
        return v if isinstance(v, int) else 0

    if claimed("fulltext_fetched") > 0 and rec_ft == 0:
        breaks.append({
            "invariant": "I1",
            "detail": f"metadata.fulltext_fetched={meta.get('fulltext_fetched')} "
                      f"but 0 of {len(papers)} records carry has_fulltext"})
    if claimed("pmc_available") > 0 and rec_pmcid == 0:
        breaks.append({
            "invariant": "I2",
            "detail": f"metadata.pmc_available={meta.get('pmc_available')} "
                      f"but 0 of {len(papers)} records carry a pmcid"})
    if on_disk and rec_ft < on_disk:
        notes.append({
            "invariant": "I3",
            "detail": f"{on_disk} full texts on disk, {rec_ft} records flagged; "
                      f"difference of {on_disk - rec_ft} is full text held for "
                      f"papers the index does not list (ingestion gap)"})
    ti = meta.get("total_indexed")
    if isinstance(ti, int) and ti != len(papers):
        breaks.append({
            "invariant": "I4",
            "detail": f"metadata.total_indexed={ti} != len(papers)={len(papers)}"})

    for b in breaks:
        print(f"  [BREAK] {b['invariant']}: {b['detail']}")
    for n in notes:
        print(f"  [NOTE]  {n['invariant']}: {n['detail']}")
    if not breaks and not notes:
        print("  all invariants hold")
    print()

    payload = {
        "audit": "index_field_invariants",
        "run_date": str(date.today()),
        "measured": {
            "papers": len(papers),
            "meta_pmc_available": meta.get("pmc_available"),
            "meta_fulltext_fetched": meta.get("fulltext_fetched"),
            "records_with_pmcid": rec_pmcid,
            "records_with_fulltext": rec_ft,
            "records_with_abstract": rec_abs,
            "fulltext_files_on_disk": on_disk,
        },
        "breaks": breaks,
        "notes": notes,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"  Output: {OUT}")

    if gate and breaks:
        print("  [FAIL] index summary counts disagree with its own records")
        return 1
    print("  [OK] index summary counts agree with its records" if gate
          else "  [MEASURE] reporting only; not gating")
    return 0


if __name__ == "__main__":
    sys.exit(main())
