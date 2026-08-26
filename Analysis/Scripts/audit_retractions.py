#!/usr/bin/env python3
"""Is any paper this repo cites RETRACTED?

WHY THIS EXISTS
---------------
Found on 2026-08-26 while vetting the 37 papers folded in on 2026-08-25:

  38918878  "Emerging insights into the role of IL-1 inhibitors and colchicine
             for inflammation management in type 2 diabetes and cardiovascular
             disease"   Diabetol Metab Syndr 2024
             PubMed publication type: **Retracted Publication**

It was cited in 17 places and published in 3 files under docs/. Every gate this
repo owns had passed it, because every one of them asks a different question:

  validate_citations.py            does the PMID resolve?           yes
  audit_path_citations.py          is the subject on-topic?         yes
  audit_builder_title_agreement.py does the title match?            yes
  audit_prose_citation_titles.py   does the prose match?            yes

A retracted paper resolves, is on-topic, and has a correct title. It is the one
defect class where every existing control is silent by construction, and it is
strictly worse than a miscitation: a miscitation points at the wrong paper, a
retraction points at a paper the literature has withdrawn.

WHAT IT DOES
------------
Resolves every PMID in state['papers'] plus every PMID cited by a builder
against NCBI esummary and reads the `pubtype` list.

  RETRACTED            pubtype contains "Retracted Publication" -- fails
  RETRACTION_NOTICE    the record IS the retraction notice -- fails if cited as
                       evidence, since it contains no findings
  EXPRESSION_OF_CONCERN / ERRATUM
                       reported, not failed: an erratum usually corrects a
                       detail and the paper stands. It still needs a human to
                       confirm the corrected detail is not the number this repo
                       is quoting.

Exit 1 on any RETRACTED or RETRACTION_NOTICE.
Output: Analysis/Results/retraction_audit.json

LIMIT, STATED
-------------
This reads PubMed's publication type, which is how PubMed records a retraction
once the notice is indexed. A retraction announced by a journal but not yet
indexed will not be caught here, and neither will an unretracted paper whose
findings have failed to replicate. This gate answers "has it been formally
withdrawn", nothing softer.
"""

import json
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_citation_identifiers import _get, ESUMMARY, TOOL  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
SCRIPTS = os.path.join(BASE, 'Scripts')
STATE = os.path.join(RESULTS, 'agent_state.json')
REPORT = os.path.join(RESULTS, 'retraction_audit.json')
CACHE = os.path.join(RESULTS, '.pubtype_cache.json')

RE_PMID = re.compile(r'(?:PMID\s*[:=]?\s*(\d{7,8})'
                     r'|pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,8}))', re.I)

FAIL_TYPES = {'Retracted Publication', 'Retraction of Publication'}
WARN_TYPES = {'Expression of Concern', 'Published Erratum',
              'Corrected and Republished Article'}

# Files whose PURPOSE is to name a retracted paper: the exclusion registry, the
# audit reports, this gate's own docstring, the pipeline comment explaining why
# the gate exists, and the raw abstract/fulltext caches that predate the
# finding. Counting them as citations makes the gate fail forever on the record
# of its own fix, which is how a gate stops being read. Same reasoning as
# AUDIT_TRAIL_FIELDS in audit_citation_identifiers.py.
AUDIT_TRAIL = (
    'not_corpus_pmids.json', 'retraction_audit.json', 'audit_retractions.py',
    'run_quality_improvements.py', 'citation_identifier_audit.json',
    'index_provenance_audit.json', 'pmid_verification.json',
    'citation_validation.json', 'prose_citation_titles.json',
    'builder_title_agreement.json', 'adjudicated_offtopic_pmids.json',
    'agent_state.json',
)
AUDIT_TRAIL_DIRS = ('paper_library/abstracts', 'paper_library/fulltext')

# Where a citation still MEANS something: an evidence store the dashboards read,
# or a builder that writes a page. Presence here is what fails the build.
LIVE_EVIDENCE = (
    'extracted_corpus_data.json', 'evidence_network.json',
    'research_paths.json', 'validated_research_paths.json',
    'gap_evidence.json', 'extracted_evidence.json',
)


def is_audit_trail(path):
    p = path.replace('\\', '/')
    if any(p.endswith(n) for n in AUDIT_TRAIL):
        return True
    if any(d in p for d in AUDIT_TRAIL_DIRS):
        return True
    # A one-off dated run script is a log of what a past run did.
    return '/_run_' in p or '/_close_run_' in p or 'reconcile_' in p


def is_live_evidence(path):
    p = path.replace('\\', '/')
    if any(p.endswith(n) for n in LIVE_EVIDENCE):
        return True
    base = p.rsplit('/', 1)[-1]
    return base.startswith(('build_', 'rebuild_')) and base.endswith('.py')


def load_cache():
    if os.path.exists(CACHE):
        try:
            with open(CACHE, encoding='utf-8') as fh:
                return json.load(fh)
        except ValueError:
            pass
    return {}


def resolve_pubtypes(pmids, cache):
    missing = sorted({p for p in pmids if p not in cache})
    for i in range(0, len(missing), 150):
        batch = missing[i:i + 150]
        q = dict(TOOL, db='pubmed', retmode='json', id=','.join(batch))
        try:
            data = json.loads(_get(ESUMMARY + urllib.parse.urlencode(q)))
        except Exception as exc:
            print('  [WARN] esummary failed: %s' % exc)
            continue
        res = data.get('result', {})
        for p in batch:
            rec = res.get(p)
            if isinstance(rec, dict):
                cache[p] = {'pubtype': rec.get('pubtype', []),
                            'title': rec.get('title', ''),
                            'journal': rec.get('fulljournalname', ''),
                            'year': (rec.get('pubdate') or '')[:4]}
            else:
                cache[p] = None
        time.sleep(0.4)
    return {p: cache.get(p) for p in pmids}


def cited_where(pmid):
    """Every repo file that names this PMID, so the blast radius is visible."""
    hits = []
    for root in ('Analysis/Scripts', 'Analysis/Results', 'docs', 'Dashboards'):
        full = os.path.join(BASE, '..', root)
        if not os.path.isdir(full):
            continue
        for dirpath, _, names in os.walk(full):
            for n in names:
                if not n.endswith(('.py', '.json', '.html', '.md')):
                    continue
                if n.startswith('.') or n.startswith('agent_state'):
                    continue
                path = os.path.join(dirpath, n)
                try:
                    with open(path, encoding='utf-8', errors='replace') as fh:
                        if re.search(r'\b%s\b' % pmid, fh.read()):
                            hits.append(os.path.relpath(path,
                                                        os.path.join(BASE, '..')))
                except OSError:
                    pass
    return sorted(hits)


def main():
    pmids = set()
    with open(STATE, encoding='utf-8') as fh:
        state = json.load(fh)
    pmids |= {p for p in state.get('papers', {}) if re.fullmatch(r'\d{7,8}', p)}
    for name in sorted(os.listdir(SCRIPTS)):
        if name.endswith('.py') and (name.startswith('build_')
                                     or name.startswith('rebuild_')):
            with open(os.path.join(SCRIPTS, name), encoding='utf-8',
                      errors='replace') as fh:
                for a, b in RE_PMID.findall(fh.read()):
                    pmids.add(a or b)

    pmids = sorted(pmids)
    print('PMIDs to check for retraction: %d' % len(pmids))
    cache = load_cache()
    meta = resolve_pubtypes(pmids, cache)
    with open(CACHE, 'w', encoding='utf-8') as fh:
        json.dump(cache, fh, indent=1, ensure_ascii=False)

    # A retraction that has been adjudicated and written into the exclusion
    # registry is HANDLED. The gate must still report it every run -- silence
    # would let it drift back in -- but it fails only if the paper is still
    # feeding evidence, or if nobody has recorded the decision at all.
    acknowledged = set()
    reg = os.path.join(RESULTS, 'not_corpus_pmids.json')
    if os.path.exists(reg):
        try:
            with open(reg, encoding='utf-8') as fh:
                for k, v in (json.load(fh).get('pmids') or {}).items():
                    if (v or {}).get('provenance') == 'RETRACTED':
                        acknowledged.add(k)
        except ValueError:
            pass

    retracted, warned, unresolved = [], [], []
    for p in pmids:
        m = meta.get(p)
        if not m:
            unresolved.append(p)
            continue
        types = set(m.get('pubtype') or [])
        if types & FAIL_TYPES:
            where = cited_where(p)
            live = [f for f in where if is_live_evidence(f)]
            trail = [f for f in where if is_audit_trail(f)]
            other = [f for f in where
                     if f not in live and f not in trail]
            retracted.append({'pmid': p, 'title': m['title'],
                              'journal': m['journal'], 'year': m['year'],
                              'pubtype': sorted(types),
                              'cited_in': where,
                              'live_evidence': live,
                              'audit_trail': trail,
                              'other': other,
                              'acknowledged': p in acknowledged,
                              'fails': bool(live) or not (p in acknowledged)})
        elif types & WARN_TYPES:
            warned.append({'pmid': p, 'title': m['title'],
                           'journal': m['journal'], 'year': m['year'],
                           'pubtype': sorted(types)})

    print()
    print('=' * 74)
    print('RETRACTED %d   ERRATUM/CONCERN %d   UNRESOLVED %d   CLEAN %d'
          % (len(retracted), len(warned), len(unresolved),
             len(pmids) - len(retracted) - len(warned) - len(unresolved)))
    print()
    if retracted:
        print('--- RETRACTED papers found in this repo ---')
        for r in retracted:
            print('  PMID %s  %s' % (r['pmid'], r['title'][:80]))
            print('     %s %s   pubtype=%s'
                  % (r['journal'][:44], r['year'], ','.join(r['pubtype'])))
            print('     acknowledged in exclusion registry: %s'
                  % ('YES' if r['acknowledged'] else 'NO'))
            print('     LIVE EVIDENCE references: %d %s'
                  % (len(r['live_evidence']),
                     '  <-- THIS is what fails the build'
                     if r['live_evidence'] else '(none)'))
            for f in r['live_evidence']:
                print('       %s' % f)
            print('     audit-trail references (expected, not a defect): %d'
                  % len(r['audit_trail']))
            if r['other']:
                print('     other references, needing a human read: %d'
                      % len(r['other']))
                for f in r['other'][:10]:
                    print('       %s' % f)
    if warned:
        print('\n--- ERRATUM / EXPRESSION OF CONCERN (reported, not failed) ---')
        for w in warned:
            print('  PMID %s  %s  [%s]'
                  % (w['pmid'], w['title'][:70], ','.join(w['pubtype'])))

    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump({'generated': time.strftime('%Y-%m-%d'),
                   'pmids_checked': len(pmids),
                   'retracted': retracted,
                   'retracted_and_handled': [r['pmid'] for r in retracted
                                             if not r['fails']],
                   'retracted_and_live': [r['pmid'] for r in retracted
                                          if r['fails']],
                   'erratum_or_concern': warned,
                   'unresolved': unresolved},
                  fh, indent=1, ensure_ascii=False)
    failing = [r for r in retracted if r['fails']]
    print('\nReport: %s' % REPORT)
    if retracted and not failing:
        print('%d retracted paper(s) present and correctly excluded; the '
              'remaining references are the record of that exclusion.'
              % len(retracted))
    print('[OK]' if not failing
          else '[FAIL] %d retracted paper(s) still feeding evidence' % len(failing))
    return 1 if failing else 0


if __name__ == '__main__':
    sys.exit(main())
