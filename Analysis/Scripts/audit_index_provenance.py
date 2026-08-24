#!/usr/bin/env python3
"""Why is each paper in the library index, and has anything ever vetted it?

WHY THIS EXISTS
---------------
The 2026-08-23 queue item observed that PMID 37889505 -- the probiotic-breads
paper that was wrongly cited on the teplizumab path -- is still indexed as a
corpus paper. Its only citing sites are the three scripts that name it as a BAD
citation. It is in the corpus solely because this repo wrote about it being
wrong, and it will never be vetted because the vetting batch iterates
state["papers"], which it is absent from.

The item asked how many other index entries have that shape. Answering it
required a sharper definition than "cited only by audit scripts": a daily run
script that discovered a paper during a PubMed sweep is a legitimate provenance,
and 15 of the 16 entries matching that loose rule turned out to be exactly that.
The distinguishing feature is whether the CONTEXT of the citation is an error
report.

WHAT IT MEASURES, per index entry
---------------------------------
  provenance        SELF_REFERENTIAL  every citing context calls it a bad
                                      citation -> should not count as corpus
                    RUN_LOG_ONLY      only daily-run scripts cite it; real
                                      sweep finding, but no dashboard uses it
                    DASHBOARD         cited by a build_*/rebuild_* builder
                    UNCITED           no dashboard_locations at all
  vetting_state     VETTED / FLAGGED / ABSENT_FROM_STATE

The pairing that matters is ABSENT_FROM_STATE, because those papers are
invisible to the vetting batch by construction. Every run's vetting batch
iterates state["papers"]; a paper that is indexed but not in state is a paper
that can never be reached.

Output: Analysis/Results/index_provenance_audit.json
Exit 1 if any SELF_REFERENTIAL entry is still indexed.
"""

import json
import os
import re
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
INDEX = os.path.join(RESULTS, 'paper_library', 'index.json')
STATE = os.path.join(RESULTS, 'agent_state.json')
OUT = os.path.join(RESULTS, 'index_provenance_audit.json')

# A citing context that says the citation was WRONG.
ERROR_CONTEXT = re.compile(
    r'bad citation|off.?topic|wrong pmid|does not belong|not the paper|'
    r'purge|withdraw|bakery|breads|mis.?cited|fabricat|nothing to do with',
    re.I)

# A citing "context" that is source code, not a citation: a regex literal, a
# comment showing an example identifier, a docstring illustrating a pattern.
# 2026-08-24: PMID 12345678 ("Denpasar Declaration on Population and
# Development", Integration 1994) is indexed as a corpus paper and rendered on
# Paper_Library.html and PMID_Verification.html. Its entire provenance is the
# comment `# match PMID: 12345678 or PMID 12345678` next to a regex in
# postprocess_dashboards.py. The harvester read an example as a citation.
#
# The first version of this pattern included a bare `pattern` alternative and
# matched "different patterns of lymphokine secretion" in the Mosmann TH1/TH2
# citation in build_data_dictionary.py -- i.e. it would have withdrawn a real,
# correctly-cited paper. A screen that produces false positives on legitimate
# citations is worse than no screen, because acting on it destroys good data.
# The alternatives below are all regex/code syntax that cannot occur in a
# bibliographic string.
CODE_ARTIFACT = re.compile(
    r"\\d\{|\\s\*|\\s\+|re\.compile|\(\?:|\[\^|"          # regex syntax
    r"#\s*match\b|#\s*e\.?g\.?\b|#\s*example\b|"           # example comments
    r'"match PMID|\bmatch PMID:\s*\d+"',                    # quoted examples
    re.I)

RUN_LOG = re.compile(r'^(_run_|_close_run_|_tmp_)', re.I)
# postprocess_dashboards.py is deliberately NOT a builder here: it rewrites
# already-built HTML and originates no citations, so a PMID whose only
# "dashboard" site is that file has no editorial provenance at all.
BUILDER = re.compile(r'^(build_|rebuild_|refresh_)', re.I)
AUDIT = re.compile(
    r'^(audit_|fix_|repair_|reconcile_|check_|falsify_|validate_|mark_|'
    r'recount_|resolve_|regression_)', re.I)


def classify(record, adjudicated):
    pmid = record.get('pmid', '')
    locs = record.get('dashboard_locations') or []
    if not locs:
        return 'UNCITED', []
    files = []
    error_hits, non_error, code_hits = 0, 0, 0
    for loc in locs:
        fname = loc.get('file', '')
        ctx = loc.get('context', '') or ''
        files.append(fname)
        if CODE_ARTIFACT.search(ctx):
            code_hits += 1
        elif ERROR_CONTEXT.search(ctx):
            error_hits += 1
        else:
            non_error += 1
    files_set = sorted(set(files))
    if code_hits and not non_error and not error_hits:
        return 'CODE_ARTIFACT', files_set
    # The stored `context` snippet is truncated, so error language is often cut
    # off (37889505's snippet stops at "The most consequential is PMID 37889").
    # The adjudication registry is the authoritative record of "this repo
    # concluded the citation was wrong", so it is consulted directly rather than
    # inferred from a truncated string.
    if pmid in adjudicated and not any(BUILDER.match(f) for f in files_set):
        return 'SELF_REFERENTIAL', files_set
    if error_hits and not non_error:
        return 'SELF_REFERENTIAL', files_set
    if any(BUILDER.match(f) for f in files_set):
        return 'DASHBOARD', files_set
    if all(RUN_LOG.match(f) or AUDIT.match(f) for f in files_set):
        return ('RUN_LOG_ONLY' if any(RUN_LOG.match(f) for f in files_set)
                else 'AUDIT_ONLY'), files_set
    return 'OTHER', files_set


def main():
    with open(INDEX, encoding='utf-8') as fh:
        papers = json.load(fh)['papers']
    with open(STATE, encoding='utf-8') as fh:
        state = json.load(fh)
    known = state.get('papers') or {}
    adj_path = os.path.join(RESULTS, 'adjudicated_offtopic_pmids.json')
    adjudicated = {}
    if os.path.exists(adj_path):
        with open(adj_path, encoding='utf-8') as fh:
            adjudicated = json.load(fh).get('pmids') or {}

    rows = {}
    for pmid, rec in papers.items():
        prov, files = classify(rec, adjudicated)
        entry = known.get(pmid)
        vet = (entry.get('status', 'UNKNOWN') if isinstance(entry, dict)
               else 'ABSENT_FROM_STATE' if entry is None else str(entry))
        rows[pmid] = {
            'title': rec.get('title', '')[:120],
            'journal': rec.get('journal', ''),
            'year': rec.get('year', ''),
            'has_fulltext': rec.get('has_fulltext', False),
            'provenance': prov,
            'citing_files': files,
            'vetting_state': vet,
        }

    by_prov = {}
    for r in rows.values():
        slot = by_prov.setdefault(r['provenance'], {'n': 0, 'unreachable': 0})
        slot['n'] += 1
        if r['vetting_state'] == 'ABSENT_FROM_STATE':
            slot['unreachable'] += 1

    unreachable = sorted(p for p, r in rows.items()
                         if r['vetting_state'] == 'ABSENT_FROM_STATE')
    selfref = sorted(p for p, r in rows.items()
                     if r['provenance'] == 'SELF_REFERENTIAL')
    artifacts = sorted(p for p, r in rows.items()
                       if r['provenance'] == 'CODE_ARTIFACT')

    print('Index entries: %d' % len(rows))
    print()
    print('%-18s %6s %s' % ('PROVENANCE', 'N', 'of which never reachable by '
                            'the vetting batch'))
    for prov in sorted(by_prov, key=lambda p: -by_prov[p]['n']):
        s = by_prov[prov]
        print('%-18s %6d %d' % (prov, s['n'], s['unreachable']))
    print()
    print('SELF_REFERENTIAL (indexed only because this repo reported it as a '
          'bad citation): %d' % len(selfref))
    for p in selfref:
        print('  %s  %s' % (p, rows[p]['title'][:70]))
        print('        cited by: %s' % ', '.join(rows[p]['citing_files']))
    print()
    print('CODE_ARTIFACT (indexed from a regex example or code comment, not a '
          'citation): %d' % len(artifacts))
    for p in artifacts:
        print('  %s  %s' % (p, rows[p]['title'][:70]))
        print('        cited by: %s' % ', '.join(rows[p]['citing_files']))
    print()
    print('INDEXED BUT ABSENT FROM state["papers"] - the vetting batch '
          'iterates state, so these can never be vetted: %d' % len(unreachable))
    for p in unreachable[:40]:
        print('  %s  [%-16s] %s' % (p, rows[p]['provenance'],
                                    rows[p]['title'][:60]))
    if len(unreachable) > 40:
        print('  ... and %d more' % (len(unreachable) - 40))

    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump({'generated': time.strftime('%Y-%m-%d'),
                   'index_entries': len(rows),
                   'by_provenance': by_prov,
                   'self_referential': selfref,
                   'code_artifacts': artifacts,
                   'absent_from_state': unreachable,
                   'rows': rows}, fh, indent=1, ensure_ascii=False)
    print('\nReport: %s' % OUT)
    bad = len(selfref) + len(artifacts)
    print('[OK]' if not bad
          else '[FAIL] %d entr(ies) that are not corpus papers: '
               '%d self-referential, %d code artifact'
               % (bad, len(selfref), len(artifacts)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
