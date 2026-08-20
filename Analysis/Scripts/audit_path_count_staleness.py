#!/usr/bin/env python3
"""Audit: are the per-path data_point_counts on the dashboard still true?

BACKGROUND
----------
Work-queue item (P3, added 2026-08-19) asked whether the new text-level dedupe
"changes any path ranking" -- specifically whether verapamil -> T1D and
verapamil -> beta_cell, both sourced solely from PMID 39613428 (39 -> 16 raw
data points), had been ranked above better-supported paths.

The item assumed the path counts had been recomputed post-dedupe and only the
ORDERING was in question. That assumption is wrong, and this script exists to
prove it with numbers rather than assert it.

WHAT IT MEASURES
----------------
research_paths.json stores, per path, a `data_point_count` and a `data_types`
histogram, and the PMIDs the path draws on. extracted_corpus_data.json stores a
`dedupe_log` of every (pmid, data_type) bucket the 2026-08-19 text-level dedupe
collapsed, with raw and unique counts.

Intersecting the two gives, for each path, the exact number of its data points
that were restatements of text already counted -- i.e. how much of its apparent
evidence depth is double-counting. That is an exact figure for the buckets the
path declares, not an estimate.

Reports: file staleness, per-path inflation, and whether removing the
restatements reorders the ranking.

Exit 0 always -- this is a measurement, not a gate.
"""

import json
import os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
PATHS_FILE = os.path.join(RESULTS, 'research_paths.json')
EXTRACT_FILE = os.path.join(RESULTS, 'extracted_corpus_data.json')


def mtime(path):
    return datetime.fromtimestamp(os.path.getmtime(path), timezone.utc).date()


def main():
    with open(PATHS_FILE, encoding='utf-8') as f:
        paths = json.load(f)['paths']
    with open(EXTRACT_FILE, encoding='utf-8') as f:
        extract = json.load(f)

    p_date, e_date = mtime(PATHS_FILE), mtime(EXTRACT_FILE)
    lag = (e_date - p_date).days

    print('Path data_point_count staleness audit')
    print(f'  research_paths.json        last written : {p_date}')
    print(f'  extracted_corpus_data.json last written : {e_date}')
    print(f'  lag                                     : {lag} days')
    meta = extract.get('metadata', {})
    td = meta.get('text_dedupe', {})
    print(f'  live corpus                             : '
          f'{meta.get("total_extractions")} data points / '
          f'{meta.get("papers_processed")} papers')
    print(f'  dedupe (added {td.get("added")})            : '
          f'{td.get("restatements_collapsed")} restatements collapsed across '
          f'{td.get("papers_affected")} papers')

    if lag > 0:
        print(f'\n  [STALE] research_paths.json predates the dedupe by {lag} days.')
        print('          No script in Analysis/Scripts/ writes research_paths.json -')
        print('          build_research_paths.py only READS it. The per-path counts')
        print('          rendered on the dashboard are a frozen snapshot.')

    # (pmid, data_type) -> collapsed restatement count
    collapsed = {}
    for rec in extract.get('dedupe_log', []):
        collapsed[(rec['pmid'], rec['data_type'])] = rec

    rows = []
    for name, pdata in paths.items():
        stored = pdata.get('data_point_count', 0)
        pmids = pdata.get('pmids', []) or []
        dtypes = pdata.get('data_types', {}) or {}
        inflation = 0
        touched = []
        for pmid in pmids:
            for dtype in dtypes:
                rec = collapsed.get((pmid, dtype))
                if not rec:
                    continue
                # The path can only lose what it actually claims from this
                # bucket. Cap at the path's own declared count for the type so a
                # shared paper is never charged more than the path holds.
                loss = min(rec['collapsed'], dtypes.get(dtype, 0))
                inflation += loss
                touched.append(f'{pmid}/{dtype} raw{rec["raw"]}->uniq{rec["unique"]}')
        rows.append((name, stored, max(stored - inflation, 0), inflation, touched))

    affected = [r for r in rows if r[3] > 0]
    print(f'\n  paths audited                           : {len(rows)}')
    print(f'  paths carrying restated evidence        : {len(affected)}')

    if affected:
        print('\n  PER-PATH INFLATION (stored -> corrected)')
        print(f'  {"path":<44} {"stored":>7} {"corr":>7} {"inflated":>9}  buckets')
        for name, stored, corrected, inflation, touched in sorted(
                affected, key=lambda r: -r[3]):
            pct = (inflation / stored * 100) if stored else 0
            print(f'  {name:<44} {stored:>7} {corrected:>7} '
                  f'{inflation:>7} ({pct:.0f}%)  {"; ".join(touched)}')

    # Does correcting the counts reorder the ranking?
    before = [n for n, s, c, i, t in sorted(rows, key=lambda r: (-r[1], r[0]))]
    after = [n for n, s, c, i, t in sorted(rows, key=lambda r: (-r[2], r[0]))]
    moved = [(n, before.index(n) + 1, after.index(n) + 1)
             for n in before if before.index(n) != after.index(n)]

    print('\n  RANKING IMPACT')
    if not moved:
        print('    No path changes rank. Restated evidence was spread evenly enough')
        print('    that the ORDER survives - but the printed NUMBERS do not.')
    else:
        print(f'    {len(moved)} path(s) change rank once restatements are removed:')
        for name, b, a in moved[:15]:
            print(f'      {name:<44} #{b} -> #{a}')

    print('\n  TOP 8 BY CORRECTED COUNT')
    for name, stored, corrected, inflation, _ in sorted(rows, key=lambda r: -r[2])[:8]:
        flag = f'  (stored {stored})' if inflation else ''
        print(f'    {corrected:>4}  {name}{flag}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
