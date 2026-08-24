#!/usr/bin/env python3
"""Screen the citation stores audit_citation_identifiers.py does NOT cover.

WHY THIS EXISTS
---------------
audit_citation_identifiers.py (2026-08-23) harvests every field, in three
identifier namespaces, from state["paths"] and state["validated_paths"]. That is
two stores out of five. The 2026-08-23 queue item recorded the other three as
unmeasured and assumed defective:

  (a) Analysis/Results/gap_evidence.json   written by extract_evidence.py
  (b) PMIDs hardcoded as literals in the ~50 build_*.py dashboard builders
      (validate_citations.py checks these for EXISTENCE, never for RELEVANCE)
  (c) Analysis/Results/research_paths.json + validated_research_paths.json

THE 2026-08-24 FINDING THAT REORDERS THIS
-----------------------------------------
audit_narrative_field_exposure.py measured, for the first time, which stores
actually reach docs/. Result: build_research_paths.py -- the only builder that
renders path narrative -- reads research_paths.json and
validated_research_paths.json. It does NOT read agent_state.json for content.

So store (c) is the PUBLISHED store and stores (a)+(b) feed published HTML
directly, while the two stores every existing gate gets pointed at are
internal bookkeeping. The gates were aimed at the private copy.

WHAT IT DOES
------------
Reuses harvest(), the DOMAIN topic screen, path_tokens(), and the PMC/DOI/title
resolvers from audit_citation_identifiers.py unchanged -- they are
namespace-agnostic, which was the whole point of writing them that way -- and
applies them to the three uncovered stores.

Verdicts per identifier: ON_TOPIC / OFF_TOPIC / UNINDEXED.
Exit 1 if any OFF_TOPIC citation is found in a store that reaches docs/.

Output: Analysis/Results/published_citation_store_audit.json
"""

import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_citation_identifiers import (  # noqa: E402
    DOMAIN, harvest, path_tokens, load_cache, save_cache,
    resolve_pmc, resolve_doi, resolve_titles,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
SCRIPTS = os.path.join(BASE, 'Scripts')
REPORT = os.path.join(RESULTS, 'published_citation_store_audit.json')

# A builder literal has no path key to screen against, so path_tokens() gives
# nothing; the DOMAIN vocabulary carries the whole test there. That is the same
# standard audit_path_citations.py applies, so it is not a weaker screen -- it
# just has one of its two arms unavailable.
RE_PMID_LITERAL = re.compile(r"['\"](\d{8})['\"]")

# Builder lines that EXIST to name a bad citation would be re-flagged forever.
REPAIR_MARKERS = re.compile(
    r'off.?topic|bad citation|wrong pmid|purge|repair|BAD_|WRONG_|# was ',
    re.I)


def collect_records():
    """(store, key, dict) triples for every record in the three stores."""
    out = []

    # --- (c) the PUBLISHED path stores ---------------------------------
    for fname, sub in (('research_paths.json', 'paths'),
                       ('validated_research_paths.json', 'paths')):
        path = os.path.join(RESULTS, fname)
        if not os.path.exists(path):
            print('  [WARN] missing %s' % fname)
            continue
        with open(path, encoding='utf-8') as fh:
            data = json.load(fh)
        recs = data.get(sub) or {}
        items = recs.items() if isinstance(recs, dict) else enumerate(recs)
        for key, rec in items:
            if isinstance(rec, dict):
                out.append((fname, str(key), rec))

    # --- (a) gap evidence ----------------------------------------------
    gap_path = os.path.join(RESULTS, 'gap_evidence.json')
    if os.path.exists(gap_path):
        with open(gap_path, encoding='utf-8') as fh:
            gaps = (json.load(fh).get('gaps') or {})
        for gid, gdata in gaps.items():
            if isinstance(gdata, dict):
                out.append(('gap_evidence.json', 'gap_%s' % gid, gdata))
    else:
        print('  [WARN] gap_evidence.json absent - run extract_evidence.py')

    return out


def collect_builder_literals():
    """8-digit PMID string literals hardcoded in build_*.py / rebuild_*.py."""
    hits = {}   # pmid -> [ "file:line" ]
    for name in sorted(os.listdir(SCRIPTS)):
        if not (name.startswith('build_') or name.startswith('rebuild_')):
            continue
        if not name.endswith('.py'):
            continue
        with open(os.path.join(SCRIPTS, name), encoding='utf-8',
                  errors='replace') as fh:
            for lineno, line in enumerate(fh, 1):
                if REPAIR_MARKERS.search(line):
                    continue
                for m in RE_PMID_LITERAL.finditer(line):
                    hits.setdefault(m.group(1), []).append(
                        '%s:%d' % (name, lineno))
    return hits


def load_screen_exceptions():
    """Citations that fail the DOMAIN screen but were reviewed and are correct.

    Added 2026-08-24. The alternative was widening DOMAIN to admit 'macrophage'
    and 'coronary', which would also widen it for every future miscitation that
    happens to contain those words. A named, reasoned exception cannot do that.
    """
    path = os.path.join(RESULTS, 'topic_screen_exceptions.json')
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh).get('pmids') or {}
    except (OSError, ValueError):
        return {}


def main():
    cache = load_cache()
    exceptions = load_screen_exceptions()
    records = collect_records()
    print('Records: %d across the three uncovered stores' % len(records))

    harvested = []
    for store, key, rec in records:
        for ident in harvest(key, rec):
            ident['store'] = store
            ident['key'] = key
            harvested.append(ident)

    literals = collect_builder_literals()
    for pmid, sites in literals.items():
        harvested.append({'ns': 'pmid', 'value': pmid, 'field': 'source_literal',
                          'store': 'build_*.py', 'key': sites[0],
                          'sites': len(sites)})

    print('Identifiers harvested: %d (%d builder literals across %d PMIDs)'
          % (len(harvested), sum(len(v) for v in literals.values()),
             len(literals)))

    pmcs = sorted({i['value'] for i in harvested if i['ns'] == 'pmc'})
    dois = sorted({i['value'] for i in harvested if i['ns'] == 'doi'})
    pmc_map = resolve_pmc(pmcs, cache)
    doi_map = resolve_doi(dois, cache)

    wanted = set()
    for i in harvested:
        i['pmid'] = (i['value'] if i['ns'] == 'pmid'
                     else pmc_map.get(i['value']) if i['ns'] == 'pmc'
                     else doi_map.get(i['value']))
        if i['pmid']:
            wanted.add(i['pmid'])
    titles = resolve_titles(sorted(wanted), cache)
    save_cache(cache)

    offtopic, unindexed, ontopic = [], [], 0
    for i in harvested:
        meta = titles.get(i['pmid']) if i['pmid'] else None
        if not meta:
            i['verdict'] = 'UNINDEXED'
            unindexed.append(i)
            continue
        i['title'] = meta['title']
        i['journal'] = meta['journal']
        i['year'] = meta['year']
        tl = meta['title'].lower()
        toks = path_tokens(i['key']) if i['store'] != 'build_*.py' else set()
        on = bool(DOMAIN.search(tl)) or any(t in tl for t in toks)
        if not on and i['pmid'] in exceptions:
            on = True
            i['screen_exception'] = exceptions[i['pmid']].get('reasoning', '')
            i['verdict'] = 'ON_TOPIC_BY_REVIEW'
            ontopic += 1
            continue
        i['verdict'] = 'ON_TOPIC' if on else 'OFF_TOPIC'
        if on:
            ontopic += 1
        else:
            offtopic.append(i)

    by_store = {}
    for i in harvested:
        slot = by_store.setdefault(i['store'], {'ON_TOPIC': 0, 'OFF_TOPIC': 0,
                                                'UNINDEXED': 0,
                                                'ON_TOPIC_BY_REVIEW': 0})
        slot[i['verdict']] += 1

    print()
    print('=' * 74)
    print('%-30s %8s %8s %8s %8s'
          % ('STORE', 'ON_TOPIC', 'BY_REVIEW', 'OFF', 'UNINDEXED'))
    for store in sorted(by_store):
        s = by_store[store]
        print('%-30s %8d %8d %8d %8d'
              % (store, s['ON_TOPIC'], s['ON_TOPIC_BY_REVIEW'],
                 s['OFF_TOPIC'], s['UNINDEXED']))
    print()
    print('OFF-TOPIC CITATIONS IN PUBLISHED STORES: %d' % len(offtopic))
    for i in offtopic:
        print('  [%s] %-34s %s:%s' % (i['store'][:18], i['key'][:34],
                                      i['ns'], i['value']))
        print('        field=%-16s %s' % (i['field'], i.get('title', '')[:78]))
        if i['store'] == 'build_*.py':
            print('        sites: %s' % ', '.join(literals[i['value']][:6]))
    print()
    print('UNINDEXED (reported, not failed): %d' % len(unindexed))
    for i in unindexed[:25]:
        print('  [%s] %-30s %s:%s  [%s]'
              % (i['store'][:18], i['key'][:30], i['ns'], i['value'],
                 i['field']))
    if len(unindexed) > 25:
        print('  ... and %d more' % (len(unindexed) - 25))

    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump({'generated': time.strftime('%Y-%m-%d'),
                   'stores_covered': sorted(by_store),
                   'totals_by_store': by_store,
                   'offtopic': offtopic,
                   'unindexed': unindexed,
                   'builder_literal_sites': literals},
                  fh, indent=1, ensure_ascii=False)
    print('\nReport: %s' % REPORT)
    print('[OK]' if not offtopic else '[FAIL] %d off-topic' % len(offtopic))
    return 1 if offtopic else 0


if __name__ == '__main__':
    sys.exit(main())
