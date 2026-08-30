#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The design grader reads a PubMed field that PubMed fills in LATE.

THE FINDING THIS ANSWERS (work queue, 2026-08-29)
-------------------------------------------------
134 of 359 corpus papers carry no design-bearing pubtype, and the blindness is
worst where the corpus is newest: ~31% of pre-2018 papers, 46% of 2025, 66% of
2026. That gradient is the tell. It is not that recent diabetes research stopped
being randomised - it is that MeSH indexing runs on a lag, so a paper enters
this repo through a daily sweep BEFORE NCBI has assigned its publication types,
and the grader records "no design tag" as a permanent fact about the paper.

`.pubtype_cache.json` made that permanent in a second way: it had no expiry and
no fetch date, so once a paper was read on the day it was indexed as
['Journal Article'], every later run reused that answer forever. The cache was
built to save API calls and ended up freezing the exact field most likely to
change.

WHAT THIS DOES, AND WHAT IT DELIBERATELY DOES NOT DO
----------------------------------------------------
Re-fetches publication types from PubMed for cache entries older than
--max-age-days (default 30) and reports every CHANGE. Re-reading a PubMed field
is not a modelling decision - it replaces a stale copy of someone else's fact
with a current copy of the same fact - so an unattended run may do it.

It does NOT re-tier any path or gap, does NOT edit a dashboard, and does NOT
infer design from titles. Title-based inference is audit_pubtype_title_
disagreement.py's job and is reported, never applied. The open P1 questions
about whether the Bayesian prior should encode design, and whether
PRIMARY_OTHER should render as UNKNOWN DESIGN, stay open - this only makes the
input to those decisions current.

Every entry gains a `fetched` date. Absence of that key is treated as
infinitely stale, which is correct for the pre-existing entries: they were
written without one and nothing recorded when.

Writes .pubtype_cache.json (in place, atomically) and pubtype_refresh.json.
Never fails the build: an unreachable PubMed leaves the cache untouched and
reports the staleness rather than pretending it refreshed.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta

RESULTS = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'Results'))
CACHE = os.path.join(RESULTS, '.pubtype_cache.json')
OUT = os.path.join(RESULTS, 'pubtype_refresh.json')

ESUMMARY = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
            '?db=pubmed&retmode=json&id=%s')

# Kept identical to audit_path_evidence_design.py on purpose. If these two
# lists ever drift, the refresh will report "design tag gained" for a type the
# grader does not read, which is worse than not reporting at all.
DESIGN_BEARING = {
    'Clinical Trial Protocol', 'Editorial', 'Comment', 'Letter',
    'Published Erratum', 'Retraction of Publication', 'News',
    'Bibliometric', 'Video-Audio Media',
    'Systematic Review', 'Meta-Analysis', 'Network Meta-Analysis',
    'Consensus Development Conference', 'Guideline', 'Practice Guideline',
    'Review',
    'Randomized Controlled Trial', 'Clinical Trial', 'Controlled Clinical Trial',
    'Clinical Trial, Phase I', 'Clinical Trial, Phase II',
    'Clinical Trial, Phase III', 'Clinical Trial, Phase IV',
    'Observational Study', 'Multicenter Study', 'Case Reports',
    'Retracted Publication',
}


def has_design(pubtypes):
    return bool(set(pubtypes or []) & DESIGN_BEARING)


def fetch(pmids):
    """Returns {pmid: record}. Missing PMIDs simply do not appear."""
    out = {}
    pmids = [str(p) for p in pmids]
    for i in range(0, len(pmids), 40):
        chunk = pmids[i:i + 40]
        try:
            with urllib.request.urlopen(ESUMMARY % ','.join(chunk),
                                        timeout=45) as fh:
                data = json.loads(fh.read().decode('utf-8'))['result']
        except Exception as exc:
            print('  [WARN] esummary failed for %d PMID(s): %s'
                  % (len(chunk), exc))
            continue
        for p in data.get('uids', []):
            rec = data[p]
            out[p] = {
                'pubtype': rec.get('pubtype', []),
                'title': rec.get('title', ''),
                'journal': rec.get('fulljournalname') or rec.get('source', ''),
                'year': (rec.get('pubdate', '') or '')[:4],
            }
        time.sleep(0.4)
    return out


def stale(entry, cutoff):
    got = entry.get('fetched')
    if not got:
        return True
    try:
        return datetime.strptime(got, '%Y-%m-%d').date() < cutoff
    except ValueError:
        return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-age-days', type=int, default=30)
    ap.add_argument('--limit', type=int, default=0,
                    help='refresh at most N stale entries (0 = all)')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    try:
        with open(CACHE, 'r', encoding='utf-8') as fh:
            cache = json.load(fh)
    except (OSError, ValueError) as exc:
        print('  [skip] cannot read .pubtype_cache.json: %s' % exc)
        return 0

    today = date.today()
    cutoff = today - timedelta(days=args.max_age_days)
    due = [p for p, e in cache.items() if stale(e, cutoff)]
    due.sort()
    if args.limit:
        due = due[:args.limit]

    blind_before = [p for p, e in cache.items() if not has_design(e.get('pubtype'))]
    print('  Cache: %d entries   design-bearing tag missing on %d (%.0f%%)'
          % (len(cache), len(blind_before), 100.0 * len(blind_before) / max(1, len(cache))))
    print('  Stale (>%dd or undated): %d' % (args.max_age_days, len(due)))

    if args.dry_run or not due:
        print('  [OK] nothing refreshed (%s)'
              % ('dry run' if args.dry_run else 'cache current'))
        return 0

    fresh = fetch(due)
    if not fresh:
        print('  [WARN] PubMed returned nothing; cache left untouched.')
        return 0

    gained, lost, changed, unresolved = [], [], [], []
    for pmid in due:
        if pmid not in fresh:
            unresolved.append(pmid)
            continue
        old = cache[pmid]
        new = fresh[pmid]
        was, now = list(old.get('pubtype') or []), list(new['pubtype'])
        if set(was) != set(now):
            rec = {'pmid': pmid, 'title': new['title'][:140],
                   'journal': new['journal'], 'year': new['year'],
                   'was': sorted(was), 'now': sorted(now),
                   'added': sorted(set(now) - set(was)),
                   'removed': sorted(set(was) - set(now))}
            changed.append(rec)
            if not has_design(was) and has_design(now):
                gained.append(rec)
            elif has_design(was) and not has_design(now):
                lost.append(rec)
        cache[pmid] = {
            'pubtype': now,
            # Keep the repo's verified title/journal if PubMed returns an empty
            # one; a blank overwrite would silently break the title audits.
            'title': new['title'] or old.get('title', ''),
            'journal': new['journal'] or old.get('journal', ''),
            'year': new['year'] or old.get('year', ''),
            'fetched': today.isoformat(),
        }

    blind_after = [p for p, e in cache.items() if not has_design(e.get('pubtype'))]

    tmp = CACHE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(cache, fh, indent=2, ensure_ascii=False, sort_keys=True)
    os.replace(tmp, CACHE)

    report = {
        'generated': today.isoformat(),
        'max_age_days': args.max_age_days,
        'entries': len(cache),
        'refreshed': len(due) - len(unresolved),
        'unresolved': unresolved,
        'design_blind_before': len(blind_before),
        'design_blind_after': len(blind_after),
        'gained_design_tag': gained,
        'lost_design_tag': lost,
        'all_changes': changed,
    }
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)

    print('  Refreshed %d   changed %d   gained a design tag %d   lost %d   unresolved %d'
          % (len(due) - len(unresolved), len(changed), len(gained), len(lost),
             len(unresolved)))
    print('  Design-blind: %d -> %d (%.0f%% -> %.0f%%)'
          % (len(blind_before), len(blind_after),
             100.0 * len(blind_before) / max(1, len(cache)),
             100.0 * len(blind_after) / max(1, len(cache))))
    for rec in gained:
        print('    + %-9s %-4s %s' % (rec['pmid'], rec['year'],
                                      '/'.join(rec['added'])[:60]))
        print('      %s' % rec['title'][:96])
    for rec in lost:
        print('    - %-9s LOST %s' % (rec['pmid'], '/'.join(rec['removed'])[:60]))
    if gained or lost:
        print()
        print('  NOTE: a gained or lost design tag can change a path or gap tier.')
        print('  Re-run audit_path_evidence_design.py and audit_gap_evidence_design.py.')
    print('  [OK] wrote %s' % os.path.basename(OUT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
