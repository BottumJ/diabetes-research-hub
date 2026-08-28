#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper-index orphan reconciliation.

WHY THIS EXISTS
---------------
The corpus intake chain is:

    verify_pmids.py  (scans *.py source literals only)
        -> pmid_verification.json
            -> ingest_papers.py  (fetches abstracts + full text)
                -> paper_library/index.json
                    -> validate_citations.py / check_citation_mismatches.py  (the audit gate)

Because the FIRST stage only reads PMIDs written literally into .py files, any
paper that entered the corpus some other way -- via extraction output
(extracted_corpus_data.json), via research_paths.json, via a weekly PubMed
sweep recorded in agent_state.json -- never reaches the index, even when its
abstract and full text have already been downloaded to disk.

Consequence: THE AUDIT GATE CANNOT SEE THOSE PAPERS. On 2026-08-18 there were
39 such orphans (13% of the 298 fetched abstracts), including PMID 39412512,
which is the SOLE source for the `NLRP3_inflammasome -> nephropathy` path and
supplies 61 data points to `NLRP3_inflammasome -> inflammation`.

This script folds every orphan into index.json, marked with provenance so the
distinction between "cited in a dashboard script" and "present in the corpus
only" is never lost. Run it after ingest_papers.py and before
build_paper_library.py.
"""
import json
import os
import glob
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RESULTS = os.path.join(BASE_DIR, 'Analysis', 'Results')
LIBRARY = os.path.join(RESULTS, 'paper_library')
INDEX = os.path.join(LIBRARY, 'index.json')


def _maybe_list(value):
    """Abstract records store lists as their repr string. Recover the list."""
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
        try:
            import ast
            parsed = ast.literal_eval(value)
            return parsed if isinstance(parsed, list) else []
        except (ValueError, SyntaxError):
            return []
    return []


def find_orphans():
    """PMIDs with a fetched abstract that are absent from index.json."""
    if not os.path.exists(INDEX):
        return [], {}
    with open(INDEX, encoding='utf-8') as f:
        index = json.load(f)
    indexed = set(index.get('papers', {}))
    on_disk = {os.path.basename(p)[:-5]
               for p in glob.glob(os.path.join(LIBRARY, 'abstracts', '*.json'))}
    return sorted(on_disk - indexed), index


# A paper is presumed ON-TOPIC only if diabetes/islet/beta-cell vocabulary
# appears in its title, MeSH headings or keywords. Deliberately broad: this is
# a screen to force review, not a verdict.
TOPIC_TERMS = [
    'diabet', 'insulin', 'islet', 'beta cell', 'beta-cell', 'glycem', 'glycaem',
    'hba1c', 'glucose', 'glucagon', 'lada', 'autoimmun', 'pancrea',
    'sglt2', 'glp-1', 'glp1', 'metformin', 'nephropath', 'retinopath',
    'neuropath', 'nlrp3', 'inflammasome', 'hyperglyc',
]


def screen_topic(record, abstract_record):
    """Presumptive on/off-topic screen from title + MeSH + keywords."""
    hay = ' '.join([
        str(record.get('title', '')),
        ' '.join(record.get('mesh_terms', []) or []),
        ' '.join(record.get('keywords', []) or []),
        str(abstract_record.get('abstract', ''))[:400],
    ]).lower()
    hits = sorted({t for t in TOPIC_TERMS if t in hay})
    return hits


def load_flagged_pmids():
    """PMIDs an earlier run already judged off-topic, so the screen agrees with
    decisions already on the record instead of re-litigating them."""
    path = os.path.join(RESULTS, 'agent_state.json')
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding='utf-8') as f:
            state = json.load(f)
    except (OSError, ValueError):
        return {}
    return {p: v.get('issues_found', [])
            for p, v in state.get('papers', {}).items()
            if v.get('status') == 'FLAGGED'}


def provenance_for(pmid):
    """Where did this PMID enter the corpus from, if not a .py literal?"""
    sources = []
    probes = [
        ('extracted_corpus_data.json', 'corpus extraction'),
        ('research_paths.json', 'research path evidence'),
        ('statistical_analysis.json', 'statistical analysis input'),
        ('agent_state.json', 'agent state / PubMed sweep'),
    ]
    for fname, label in probes:
        path = os.path.join(RESULTS, fname)
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding='utf-8') as f:
                if pmid in f.read():
                    sources.append(label)
        except OSError:
            continue
    return sources or ['unknown - abstract on disk with no traceable referrer']


def load_not_corpus():
    """PMIDs adjudicated as not corpus papers; see not_corpus_pmids.json.

    Added 2026-08-24. ingest_papers.py was given this guard first, and the
    index still came back with both entries: this function re-adds any PMID
    whose abstract is on disk, which is the second door into the index. A
    guard on one intake path is not a guard.

    Rewired 2026-08-28 to corpus_membership. This function and
    load_flagged_pmids() above were reading the two registries separately and
    treating them differently - FLAGGED produced a REPORTED note, the
    registry produced an EXCLUSION - so an off-topic paper adjudicated in
    state was described here and admitted anyway.
    """
    import corpus_membership
    return {p: corpus_membership.reason(p) for p in corpus_membership.excluded_pmids()}


def reconcile(dry_run=False):
    orphans, index = find_orphans()
    not_corpus = load_not_corpus()
    if not_corpus:
        blocked = [p for p in orphans if p in not_corpus]
        if blocked:
            print('  [not_corpus] refusing to reconcile %d adjudicated '
                  'non-corpus PMID(s): %s'
                  % (len(blocked), ', '.join(sorted(blocked))))
        orphans = [p for p in orphans if p not in not_corpus]
        # Also evict any that a previous run already admitted.
        stale = [p for p in list(index.get('papers', {})) if p in not_corpus]
        for p in stale:
            del index['papers'][p]
        if stale and not dry_run:
            print('  [not_corpus] evicted %d stale index entr(ies): %s'
                  % (len(stale), ', '.join(sorted(stale))))
            # Persist immediately. The `if not orphans` early return below does
            # not write the index, so an eviction with nothing else to do would
            # otherwise be silently discarded and the entries would survive.
            index.setdefault('metadata', {})['not_corpus_evicted_on'] = \
                datetime.now().strftime('%Y-%m-%d')
            with open(INDEX, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
    if not orphans:
        return {'added': [], 'total_before': len(index.get('papers', {})),
                'total_after': len(index.get('papers', {}))}

    fulltext_pmcids = {os.path.basename(p)[:-5]
                       for p in glob.glob(os.path.join(LIBRARY, 'fulltext', '*.json'))}
    already_flagged = load_flagged_pmids()

    before = len(index['papers'])
    added = []
    for pmid in orphans:
        apath = os.path.join(LIBRARY, 'abstracts', f'{pmid}.json')
        try:
            with open(apath, encoding='utf-8') as f:
                a = json.load(f)
        except (OSError, ValueError):
            continue

        # Does a full-text file exist for this paper's PMCID?
        pmcid = a.get('pmcid', '') or ''
        has_ft = bool(pmcid) and pmcid in fulltext_pmcids

        record = {
            'pmid': pmid,
            'title': a.get('title', ''),
            'journal': a.get('journal', ''),
            # 'Unknown' not '' -- downstream builders int() this field.
            'year': str(a.get('year', '') or '').strip() or 'Unknown',
            'doi': a.get('doi', ''),
            'has_abstract': bool(a.get('abstract')),
            'has_fulltext': has_ft,
            'pmcid': pmcid,
            # Empty by definition: an orphan is a paper NO dashboard script cites.
            'dashboard_locations': [],
            'mesh_terms': _maybe_list(a.get('mesh_terms')),
            'keywords': _maybe_list(a.get('keywords')),
            'pub_types': _maybe_list(a.get('pub_types')),
            'index_provenance': 'reconcile_paper_index.py',
            'index_provenance_note': (
                'Not cited in any .py dashboard script, so verify_pmids.py never '
                'saw it and ingest_papers.py never indexed it. Abstract was '
                'already on disk. Entered corpus via: '
                + '; '.join(provenance_for(pmid))
            ),
            'index_reconciled_on': datetime.now().strftime('%Y-%m-%d'),
        }

        # Topic screen. An orphan must NOT silently join the headline corpus
        # count: 6 of the 39 orphans found on 2026-08-18 were already FLAGGED
        # off-topic (colon cancer, nicotinic receptors, pepper-plant genetics).
        # Indexing them as corpus members would have inflated the corpus by 15%
        # with papers a previous run had explicitly rejected.
        hits = screen_topic(record, a)
        if pmid in already_flagged:
            record['corpus_status'] = 'OFF_TOPIC'
            record['corpus_status_reason'] = (
                'Already FLAGGED off-topic in agent_state: '
                + '; '.join(already_flagged[pmid][:1] or ['no reason recorded'])
            )
        elif hits:
            record['corpus_status'] = 'UNSCREENED_ORPHAN'
            record['corpus_status_reason'] = (
                'Topic vocabulary present (' + ', '.join(hits[:6])
                + '); needs human relevance review before counting as corpus.'
            )
        else:
            record['corpus_status'] = 'OFF_TOPIC_PRESUMED'
            record['corpus_status_reason'] = (
                'No diabetes/islet/beta-cell vocabulary in title, MeSH, keywords '
                'or abstract opening. Presumed miscitation intake.'
            )
        record['topic_hits'] = hits

        added.append({'pmid': pmid, 'title': record['title'][:70],
                      'journal': record['journal'], 'year': record['year'],
                      'pub_types': record['pub_types'],
                      'corpus_status': record['corpus_status'],
                      'topic_hits': hits})
        if not dry_run:
            index['papers'][pmid] = record

    if not dry_run:
        index.setdefault('metadata', {})
        # `total_pmids` is the HEADLINE CORPUS COUNT consumed by the dashboards.
        # Reconciled orphans are indexed (so the audit gate can see them) but
        # deliberately excluded from it until screened.
        index['metadata']['total_pmids'] = before
        index['metadata']['total_indexed'] = len(index['papers'])
        index['metadata']['orphans_reconciled'] = len(added)
        index['metadata']['orphans_reconciled_on'] = datetime.now().strftime('%Y-%m-%d')
        index['metadata']['orphan_status_counts'] = {
            s: sum(1 for a in added if a['corpus_status'] == s)
            for s in sorted({a['corpus_status'] for a in added})
        }
        index['metadata']['reconciliation_note'] = (
            'Papers carrying index_provenance=reconcile_paper_index.py are '
            'present in the corpus directory but cited by no dashboard script, '
            'so verify_pmids.py never saw them and the citation audit gate was '
            'blind to them. They are now indexed and auditable, but are NOT '
            'counted in total_pmids until their corpus_status is resolved to '
            'IN_CORPUS by review. total_pmids = cited corpus; total_indexed = '
            'everything the audit gate can see.'
        )
        with open(INDEX, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    return {'added': added, 'total_before': before,
            'total_after': before + (0 if dry_run else len(added))}


def main():
    import sys
    dry = '--dry-run' in sys.argv
    result = reconcile(dry_run=dry)
    print('=' * 64)
    print('  PAPER INDEX ORPHAN RECONCILIATION' + ('  (DRY RUN)' if dry else ''))
    print('=' * 64)
    print(f"  Indexed before : {result['total_before']}")
    print(f"  Orphans found  : {len(result['added'])}")
    print(f"  Indexed after  : {result['total_after']}")
    if result['added']:
        counts = {}
        for a in result['added']:
            counts[a['corpus_status']] = counts.get(a['corpus_status'], 0) + 1
        print('\n  Screen result:')
        for k, v in sorted(counts.items(), key=lambda x: -x[1]):
            print(f'    {v:>3}  {k}')
        print('\n  Papers folded into the audit gate:')
        order = {'UNSCREENED_ORPHAN': 0, 'OFF_TOPIC': 1, 'OFF_TOPIC_PRESUMED': 2}
        for a in sorted(result['added'], key=lambda x: (order.get(x['corpus_status'], 9), x['pmid'])):
            rev = ' [REVIEW ARTICLE]' if 'Review' in a['pub_types'] else ''
            print(f"    [{a['corpus_status']:<19}] {a['pmid']}  {a['year']:<5} "
                  f"{a['journal'][:20]:<20} {a['title'][:52]}{rev}")
        print('\n  NOTE: orphans are indexed but excluded from the headline '
              'corpus count (total_pmids) until reviewed.')
    print('\n  [OK] reconcile_paper_index')


if __name__ == '__main__':
    main()
