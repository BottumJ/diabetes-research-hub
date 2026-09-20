#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
repair_index_pmcid_map.py
=========================

Rebuilds the `pmcid` and `has_fulltext` fields of paper_library/index.json from
the ONE authoritative local source: the full-text files themselves. Each
fulltext/PMC*.json carries both its own pmcid and its pmid, so the mapping
needs no network call and cannot drift from what is actually on disk.

WHY THIS EXISTS (2026-09-19). ingest_papers.convert_pmids_to_pmcids() returned
a map keyed by INT (the NCBI ID converter sends pmid as a JSON number) while
build_index() looked it up with a STR pmid. Every lookup missed, so:

    metadata.pmc_available   174    (len(pmcid_map) -- correct)
    metadata.fulltext_fetched 150   (correct; downloads iterate the map directly)
    records with a pmcid       1  of 347
    records with has_fulltext  0  of 347

The 2026-08-17 index has the identical shape, so the index has misreported its
own full-text holdings for at least 33 days. The type bug is fixed at source in
ingest_papers.py; this script repairs the index that is already on disk without
waiting for a full re-ingest, and is safe to re-run.

Also emits a pmcid -> pmid map to Analysis/Results/pmcid_to_pmid.json, which
closes the 2026-09-07 queue item asking for PMCID normalisation at intake: a
PMCID-shaped find can now be resolved against the corpus locally before being
logged as novel. (PMC12211534 was carried for four days as a novel find while
already in corpus as PMID 40598585 -- whose full text was sitting on disk as
PMC12211534.json the entire time.)

Usage:
    python repair_index_pmcid_map.py            # report only
    python repair_index_pmcid_map.py --apply    # write index.json + map
"""

import glob
import json
import os
import shutil
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RESULTS = os.path.join(REPO, "Analysis", "Results")
LIB = os.path.join(RESULTS, "paper_library")
INDEX = os.path.join(LIB, "index.json")
MAP_OUT = os.path.join(RESULTS, "pmcid_to_pmid.json")


def build_map():
    """pmcid -> pmid, read from the full-text files on disk."""
    fwd, conflicts = {}, []
    for path in sorted(glob.glob(os.path.join(LIB, "fulltext", "*.json"))):
        stem = os.path.basename(path)[:-5]
        try:
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
        except (OSError, ValueError):
            continue
        pmid = str((doc or {}).get("pmid") or "").strip()
        pmcid = str((doc or {}).get("pmcid") or stem).strip()
        if not pmid or not pmcid:
            continue
        if pmcid != stem:
            conflicts.append({"file": stem, "internal_pmcid": pmcid})
        fwd[pmcid] = pmid
    return fwd, conflicts


def main():
    apply = "--apply" in sys.argv
    pmcid_to_pmid, conflicts = build_map()
    print("=" * 62)
    print("  PAPER INDEX pmcid / has_fulltext REPAIR")
    print("=" * 62)
    print(f"  full-text files on disk: {len(pmcid_to_pmid)}")
    if conflicts:
        print(f"  [WARN] {len(conflicts)} file(s) whose internal pmcid differs "
              f"from their filename: {conflicts[:3]}")

    with open(INDEX, encoding="utf-8") as fh:
        index = json.load(fh)
    papers = index.get("papers", {})
    pmid_to_pmcid = {v: k for k, v in pmcid_to_pmid.items()}

    before_pmcid = sum(1 for e in papers.values() if e.get("pmcid"))
    before_ft = sum(1 for e in papers.values() if e.get("has_fulltext"))

    fixed_pmcid, fixed_ft, unmatched = [], [], []
    for pmid, rec in papers.items():
        pmcid = pmid_to_pmcid.get(str(pmid))
        if not pmcid:
            continue
        if not rec.get("pmcid"):
            rec["pmcid"] = pmcid
            fixed_pmcid.append(pmid)
        if not rec.get("has_fulltext"):
            rec["has_fulltext"] = True
            fixed_ft.append(pmid)
    for pmcid, pmid in pmcid_to_pmid.items():
        if str(pmid) not in papers:
            unmatched.append({"pmcid": pmcid, "pmid": pmid})

    after_pmcid = sum(1 for e in papers.values() if e.get("pmcid"))
    after_ft = sum(1 for e in papers.values() if e.get("has_fulltext"))

    print(f"  records with pmcid      : {before_pmcid} -> {after_pmcid}")
    print(f"  records with has_fulltext: {before_ft} -> {after_ft}")
    print(f"  metadata claims pmc_available={index.get('metadata', {}).get('pmc_available')}, "
          f"fulltext_fetched={index.get('metadata', {}).get('fulltext_fetched')}")
    if unmatched:
        # SPLIT BY MEMBERSHIP, added 2026-09-20.
        #
        # This used to print one undifferentiated count and call it "an
        # ingestion question". It is two questions, and only one of them is
        # work. A full text held for an OFF_TOPIC or RETRACTED paper is
        # ABSENT ON PURPOSE - the index is right and the file on disk is the
        # leftover. A full text held for a paper with no disqualifier is a
        # paper this repository can read and does not list, which is the
        # defect the 2026-09-19 run named.
        #
        # This is also why the script imports corpus_membership rather than
        # taking an exemption from audit_unguarded_pmid_readers.py. It does
        # not FILTER anything - it only annotates records that already exist -
        # but it does REPORT on PMIDs, and a report that cannot tell a
        # deliberate exclusion from an accidental one sends someone to
        # re-ingest papers that were thrown out for cause.
        import corpus_membership
        corpus_membership.reload()
        deliberate, accidental = [], []
        for u in unmatched:
            r = corpus_membership.reason(str(u["pmid"]))
            (deliberate if r else accidental).append(
                dict(u, code=(r or {}).get("code")))
        print(f"  [NOTE] {len(unmatched)} full text(s) whose PMID is not in "
              f"the index at all. Split by corpus_membership:")
        if deliberate:
            by = {}
            for u in deliberate:
                by.setdefault(u["code"], []).append(str(u["pmid"]))
            print(f"         {len(deliberate)} excluded ON PURPOSE - the index "
                  f"is correct, the file on disk is residue:")
            for code, pmids in sorted(by.items()):
                print(f"           {code:<12} {', '.join(sorted(pmids))}")
        if accidental:
            print(f"         {len(accidental)} carry NO disqualifier - this "
                  f"repository holds their full text and does not list them:")
            print(f"           {', '.join(sorted(str(u['pmid']) for u in accidental))}")
            print("         That second list is the ingestion backlog. The "
                  "first list is not work.")
        unmatched = [dict(u, membership=(u.get("code") or "NONE"))
                     for u in deliberate + accidental]

    if apply:
        shutil.copy2(INDEX, INDEX + f".bak_{date.today()}")
        index.setdefault("metadata", {})["pmcid_repair"] = {
            "date": str(date.today()),
            "by": "repair_index_pmcid_map.py",
            "cause": ("convert_pmids_to_pmcids() keyed its map by int while "
                      "build_index() looked up by str; fixed at source the "
                      "same day"),
            "records_pmcid_filled": len(fixed_pmcid),
            "records_fulltext_flagged": len(fixed_ft),
            "source_of_truth": "paper_library/fulltext/*.json (pmid + pmcid "
                               "inside each file)",
        }
        with open(INDEX, "w", encoding="utf-8") as fh:
            json.dump(index, fh, indent=2, ensure_ascii=False)
        payload = {
            "generated": str(date.today()),
            "generated_by": "repair_index_pmcid_map.py",
            "source": "paper_library/fulltext/*.json",
            "count": len(pmcid_to_pmid),
            "pmcid_to_pmid": pmcid_to_pmid,
            "unmatched_fulltext": unmatched,
            "use": ("Normalise a PMCID-shaped identifier to its PMID BEFORE the "
                    "novelty/dedup check at intake (2026-09-07 queue item)."),
        }
        with open(MAP_OUT, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        print(f"  [APPLIED] index.json updated; map written to {MAP_OUT}")
    else:
        print("  [REPORT ONLY] re-run with --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
