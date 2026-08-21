#!/usr/bin/env python3
"""Recount every research path against the LIVE corpus extraction.

WHY THIS EXISTS
---------------
Work-queue item (P1, added 2026-08-20): research_paths.json is an orphan. It was
last written 2026-05-04 and NO script in Analysis/Scripts/ writes it -
build_research_paths.py, statistical_analysis.py and path_store.py only read it.
Every per-path `data_point_count` rendered on the published Research Paths page
is therefore a frozen May snapshot, and the dashboard's `key_claims` are frozen
with it.

That item offered two fixes: (a) regenerate the file from
extracted_corpus_data.json, or (b) retire it. Option (a) as written requires the
original path-CLUSTERING rule, which is not in the repo. Reconstructing that
rule from histograms would be a guess, and guessing is how bad data got into
this corpus in the first place.

WHAT THIS SCRIPT DOES INSTEAD
-----------------------------
It does not invent a clustering rule. It takes each path's OWN declarations -
the `pmids` list and the `data_types` histogram already stored in
research_paths.json - and recounts that path against the live extraction:

    live_count(path) = |{ e in extractions :
                          e.pmid in path.pmids AND e.data_type in path.data_types }|

Cluster MEMBERSHIP (which pmids belong to which path) stays exactly as it was and
remains a human decision; only the COUNT and the displayed CLAIMS are refreshed.

IMPORTANT - THIS COUNT IS AN UPPER BOUND, NOT AN EXACT FIGURE
-------------------------------------------------------------
The rule takes the full cross product of the path's pmids and its data_types.
Running it against the PRE-fix extraction reproduces numbers LARGER than the
stored ones for many paths (e.g. `NF_kB -> inflammation` stores 5, this rule
yields 62), which proves the original clustering applied further constraints
that are not recorded in the file. So:

    live_count == 0   is EXACT.  A superset that is empty means the true
                      count is also empty - the path has no surviving
                      evidence at all. This is the finding that matters.
    live_count  > 0   is an UPPER BOUND. Treat it as "at most this much",
                      not as a published figure.

Fields are named accordingly (`data_point_count_upper_bound`) so no downstream
script can mistake the bound for a measurement. Restoring exact counts requires
the original clustering rule and is a separate, human-owned task.

It also rewrites `key_claims` to contain only claims that still exist in the live
extraction. This matters: on 2026-08-21 the top-ranked path on the entire hub,
`NLRP3_inflammasome -> inflammation` (61 data points), was found to consist
entirely of regex artifacts from the pre-fix inflammatory_markers patterns - its
displayed key_claims were prose fragments like
    "NLRP3 activation could be a trigger for DKD. Additionally,
     pharmacological inhibition of the IL-1"     -> "value" = the 1 in IL-1
Those claims were being served to readers as extracted quantitative evidence.

OUTPUT
------
Rewrites research_paths.json in place (previous version saved alongside as
.bak_<date>) with, per path:
    data_point_count        - recounted, live
    data_point_count_stored - the frozen figure, preserved for audit
    recount_delta
    key_claims              - only claims present in the live extraction
    status                  - LIVE | HOLLOW  (HOLLOW = zero live data points)
and a top-level `recount` metadata block.

Exit code is 0 always; this reports, it does not gate.
"""

import json
import os
import re
import shutil
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
PATHS_FILE = os.path.join(RESULTS, 'research_paths.json')
EXTRACT_FILE = os.path.join(RESULTS, 'extracted_corpus_data.json')


def norm(text):
    return re.sub(r'\s+', ' ', text or '').strip().lower()


def main():
    with open(PATHS_FILE, encoding='utf-8') as f:
        doc = json.load(f)
    with open(EXTRACT_FILE, encoding='utf-8') as f:
        extract = json.load(f)

    extractions = extract['extractions']

    # Index the live corpus by (pmid, data_type) and by normalised matched_text.
    live_buckets = {}
    live_texts = set()
    for data_type, items in extractions.items():
        for e in items:
            live_buckets.setdefault((str(e['pmid']), data_type), []).append(e)
            live_texts.add((data_type, str(e['pmid']), norm(e['matched_text'])))

    paths = doc['paths']
    is_list = isinstance(paths, list)
    iterator = enumerate(paths) if is_list else paths.items()

    rows = []
    hollow = []
    claims_dropped_total = 0

    for key, path in list(iterator):
        name = path.get('name') or (key if not is_list else f'path_{key}')
        pmids = [str(p) for p in path.get('pmids', [])]
        data_types = list(path.get('data_types', {}).keys())

        live = []
        live_types = {}
        for pmid in pmids:
            for dt in data_types:
                bucket = live_buckets.get((pmid, dt), [])
                if bucket:
                    live.extend(bucket)
                    live_types[dt] = live_types.get(dt, 0) + len(bucket)

        stored = path.get('data_point_count', 0)
        live_count = len(live)

        # Keep only key_claims that still exist in the live extraction.
        kept_claims = []
        for c in path.get('key_claims', []):
            sig = (c.get('data_type'), str(c.get('pmid')), norm(c.get('matched_text')))
            if sig in live_texts:
                kept_claims.append(c)
        dropped = len(path.get('key_claims', [])) - len(kept_claims)
        claims_dropped_total += dropped

        path['data_point_count_stored'] = stored
        # Upper bound, not a measurement - see module docstring. Deliberately
        # NOT written to `data_point_count`, so that any dashboard reading the
        # old field name fails loudly rather than publishing a bound as a fact.
        path.pop('data_point_count', None)
        path['data_point_count_upper_bound'] = live_count
        path['count_semantics'] = (
            'EXACT_ZERO' if live_count == 0 else 'UPPER_BOUND_ONLY'
        )
        path['data_types_live_upper_bound'] = live_types
        path['key_claims'] = kept_claims
        path['key_claims_dropped'] = dropped
        path['status'] = 'LIVE' if live_count > 0 else 'HOLLOW'
        path['evidence_note'] = (
            'No surviving corpus evidence. All previously displayed data points were '
            'removed by the 2026-08-21 extraction-gate fix (regex artifacts: digits '
            'belonging to molecule names, years, table fragments). Must not rank on '
            'the dashboard until re-sourced.'
            if live_count == 0 else
            'Upper bound only; exact count needs the original clustering rule.'
        )
        path['recounted_at'] = date.today().isoformat()

        rows.append((name, stored, live_count, dropped))
        if live_count == 0:
            hollow.append((name, stored))

    rows.sort(key=lambda r: r[1] - r[2], reverse=True)

    print('=' * 74)
    print('  RESEARCH PATH RECOUNT AGAINST LIVE CORPUS')
    print('=' * 74)
    meta = extract.get('metadata', {})
    print(f"  live corpus : {meta.get('total_extractions')} data points "
          f"/ {meta.get('papers_processed')} papers")
    print(f"  paths       : {len(rows)}")
    print()
    print(f"  {'path':<44}{'stored':>8}{'live':>7}{'delta':>8}{'claims-':>9}")
    print(f"  {'':<44}{'':>8}{'':>7}{'':>8}{'dropped':>9}")
    print('  ' + '-' * 70)
    for name, stored, live_count, dropped in rows[:25]:
        delta = live_count - stored
        print(f"  {str(name)[:43]:<44}{stored:>8}{live_count:>7}{delta:>+8}{dropped:>9}")

    total_stored = sum(r[1] for r in rows)
    total_live = sum(r[2] for r in rows)
    print('  ' + '-' * 70)
    print(f"  {'TOTAL':<44}{total_stored:>8}{total_live:>7}{total_live - total_stored:>+8}"
          f"{claims_dropped_total:>9}")

    if hollow:
        print(f"\n  HOLLOW PATHS ({len(hollow)}) - zero live data points, "
              f"should not rank on the dashboard:")
        for name, stored in sorted(hollow, key=lambda x: -x[1]):
            print(f"    {str(name)[:50]:<52} (displayed {stored})")

    doc['recount'] = {
        'recounted_at': date.today().isoformat(),
        'rule': 'live_count(path) = extractions whose (pmid, data_type) is declared '
                'by the path itself. Cluster membership unchanged; only counts and '
                'displayed claims refreshed.',
        'count_semantics': 'Cross product of the path\'s own pmids x data_types, which '
                           'is a SUPERSET of the original clustering (verified: it '
                           'reproduces larger-than-stored figures on the pre-fix '
                           'extraction). A live count of 0 is therefore EXACT; any '
                           'nonzero live count is an UPPER BOUND and must not be '
                           'published as a measurement.',
        'corpus_total_extractions': meta.get('total_extractions'),
        'paths_total': len(rows),
        'stored_sum': total_stored,
        'live_sum': total_live,
        'hollow_paths': [h[0] for h in hollow],
        'key_claims_dropped': claims_dropped_total,
    }

    backup = f'{PATHS_FILE}.bak_{date.today().isoformat()}'
    if not os.path.exists(backup):
        shutil.copyfile(PATHS_FILE, backup)
    with open(PATHS_FILE, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)

    print(f"\n  [OK] research_paths.json recounted "
          f"(previous version: {os.path.basename(backup)})")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
