#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gate: a research path may not rest its OUTCOME claim on a DESIGN paper.

WHY THIS EXISTS
---------------
Work-queue item P2 (2026-08-21):

    "SWEEP FOR BASELINE/DESIGN PAPERS CITED AS OUTCOME EVIDENCE. Found this
     run: dapagliflozin -> nephropathy cited PMID 32862232, the DAPA-CKD
     BASELINE CHARACTERISTICS paper, as proof of renoprotection. That PMID
     resolves and is on topic, so every existing gate passes it - the defect is
     that a baseline-characteristics paper reports who enrolled, not what
     happened."

This is the third distinct citation-defect class found in four days, and each
one slipped a gate that was built for the previous one:

    2026-08-16  PMID >= 42,000,000            -> catches fabrication only
    2026-08-20  audit_path_citations.py       -> catches wrong SUBJECT only
    2026-08-21  this file                     -> catches wrong PAPER TYPE

A trial publishes several papers. "Rationale and design of DAPA-CKD" and
"Baseline characteristics of DAPA-CKD" and "Dapagliflozin in patients with
chronic kidney disease" are all real, all resolvable, all about dapagliflozin
and all about kidney disease. Only the third reports an outcome. Every gate
before this one passes all three, because the difference is not in the subject
matter - it is in what section of the trial lifecycle the paper belongs to.

The same class produced the 2026-08-19 insulin_glargine finding, where corpus
"evidence" came from the characteristics-of-included-studies TABLE of a
meta-analysis.

WHAT IT DOES
------------
1. Resolve every external_pmid on every path (shared title cache with
   audit_path_citations.py, so no extra PubMed traffic for known PMIDs).
2. Classify each title as DESIGN or OUTCOME using title-level phrasing.
3. FAIL any path whose cited evidence is 100% DESIGN papers - that path claims
   an effect while citing only documents that describe an intention.
4. WARN on paths that mix the two: the design paper is not wrong to cite, but
   it is not the thing carrying the result, so it should not stand alone.

Exit 0 = no path rests solely on design papers. Exit 1 = at least one does.
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
STATE = os.path.join(RESULTS, 'agent_state.json')
CACHE = os.path.join(RESULTS, '.pmid_title_cache.json')
OUT = os.path.join(RESULTS, 'baseline_citation_audit.json')
EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?'

# Title phrasing that identifies a paper as describing a study rather than
# reporting its result. Anchored to phrases that appear in TITLES; body text
# would produce far too many hits.
DESIGN_TITLE = re.compile(
    r'baseline\s+characteristic|'
    r'rationale\s+and\s+design|'
    r'design\s+and\s+(?:method|rationale|baseline)|'
    r'study\s+(?:protocol|design)\b|'
    r'trial\s+(?:protocol|design)\b|'
    r'statistical\s+analysis\s+plan|'
    r'\bprotocol\s+for\s+a\b|'
    r'methodology\s+of\s+the|'
    r'design\s+of\s+(?:the|a)\s+\w+\s+(?:trial|study)|'
    r'characteristics\s+of\s+(?:the\s+)?(?:patients|participants)\s+(?:enrolled|randomi)',
    re.IGNORECASE)

# Title phrasing that positively identifies an outcome report. Used only to
# explain a verdict, never to override DESIGN_TITLE.
OUTCOME_TITLE = re.compile(
    r'\beffect(?:s)?\s+of\b|\befficacy\b|\boutcome|\bresults?\b|randomi[sz]ed\s+'
    r'(?:controlled\s+)?trial|meta[- ]analys|systematic\s+review|'
    r'\bimprove|\breduc|\bassociation\s+(?:of|between)|\bin\s+patients\s+with\b',
    re.IGNORECASE)

# Reviewed exceptions. An unexplained exception is how a gate rots.
ACCEPTED = {}


def collect(state):
    """{path_key: {'stores': [...], 'pmids': [...]}}"""
    out = defaultdict(lambda: {'stores': set(), 'pmids': set()})
    for store in ('paths', 'validated_paths'):
        for key, rec in (state.get(store) or {}).items():
            if not isinstance(rec, dict):
                continue
            ep = rec.get('external_pmids')
            ids = list(ep) if isinstance(ep, (list, dict)) else []
            for pmid in ids:
                pmid = str(pmid)
                if re.fullmatch(r'\d{7,8}', pmid):
                    out[key]['stores'].add(store)
                    out[key]['pmids'].add(pmid)
    return {k: {'stores': sorted(v['stores']), 'pmids': sorted(v['pmids'])}
            for k, v in out.items() if v['pmids']}


def fetch_titles(pmids):
    cache = {}
    if os.path.exists(CACHE):
        try:
            with open(CACHE, encoding='utf-8') as f:
                cache = json.load(f)
        except ValueError:
            cache = {}
    missing = [p for p in pmids if p not in cache]
    for i in range(0, len(missing), 150):
        batch = missing[i:i + 150]
        q = urllib.parse.urlencode({'db': 'pubmed', 'retmode': 'json',
                                    'id': ','.join(batch)})
        try:
            data = json.load(urllib.request.urlopen(EUTILS + q, timeout=60))
        except Exception as exc:
            print(f'  [WARN] PubMed lookup failed for a batch: {exc}')
            continue
        for p in batch:
            cache[p] = (data.get('result', {}).get(p, {}) or {}).get('title', '')
        time.sleep(0.4)
    with open(CACHE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=1, ensure_ascii=False)
    return cache


def main():
    with open(STATE, encoding='utf-8') as f:
        state = json.load(f)

    by_path = collect(state)
    all_pmids = sorted({p for v in by_path.values() for p in v['pmids']})
    titles = fetch_titles(all_pmids)

    design_pmids = {}
    for pmid in all_pmids:
        title = titles.get(pmid, '')
        if title and pmid not in ACCEPTED and DESIGN_TITLE.search(title):
            design_pmids[pmid] = title

    sole, mixed = [], []
    for key, rec in sorted(by_path.items()):
        resolved = [p for p in rec['pmids'] if titles.get(p)]
        if not resolved:
            continue
        d = [p for p in resolved if p in design_pmids]
        if not d:
            continue
        o = [p for p in resolved if p not in design_pmids]
        entry = {
            'path': key,
            'stores': rec['stores'],
            'design_pmids': [{'pmid': p, 'title': design_pmids[p][:130]} for p in d],
            'outcome_pmids': [{'pmid': p, 'title': (titles.get(p) or '')[:130],
                               'looks_like_outcome': bool(OUTCOME_TITLE.search(titles.get(p) or ''))}
                              for p in o],
        }
        (sole if not o else mixed).append(entry)

    print('Design-paper-as-outcome-evidence audit')
    print(f'  paths with citations : {len(by_path)}')
    print(f'  distinct PMIDs cited : {len(all_pmids)}')
    print(f'  design papers found  : {len(design_pmids)}')
    for pmid, title in sorted(design_pmids.items()):
        print(f'    {pmid}  {title[:96]}')

    if mixed:
        print(f'\n[WARN] {len(mixed)} path(s) cite a design paper alongside other evidence.')
        print('       Not an error - but the design paper is not what carries the result.')
        for e in mixed:
            print(f"  - {e['path']}")
            for d in e['design_pmids']:
                print(f"      DESIGN  {d['pmid']} {d['title'][:80]}")
            for o in e['outcome_pmids']:
                mark = 'OUTCOME' if o['looks_like_outcome'] else 'OTHER  '
                print(f"      {mark} {o['pmid']} {o['title'][:80]}")

    if sole:
        print(f'\n[FAIL] {len(sole)} path(s) cite ONLY design/baseline papers as evidence.')
        print('       These claim an effect while citing only a description of intent.')
        for e in sole:
            print(f"  - {e['path']}  (stores: {', '.join(e['stores'])})")
            for d in e['design_pmids']:
                print(f"      DESIGN  {d['pmid']} {d['title'][:88]}")

    if not sole and not mixed:
        print('\n[OK] No path cites a baseline/design paper.')

    # ------------------------------------------------------------------
    # CORPUS ARM (added 2026-08-22, same run)
    #
    # The external_pmids screen above found only 2 design papers, and both
    # paths also cited real outcome papers - so the citation side is close to
    # clean. But running the same title test over the CORPUS revealed the
    # larger version of the defect: a design paper can be a SOURCE, not just a
    # citation, and then its content is extracted as evidence.
    #
    # PMID 39613428, Ver-A-T1D, is titled "...protocol for a randomised,
    # double-blind, placebo-controlled ... trial". It contributes 15 corpus
    # data points to `verapamil -> T1D` and `verapamil -> beta_cell`, which
    # published at ranks #7 and #8. A protocol paper reports no outcomes at
    # all - every one of those 15 is a planned dose.
    #
    # This is queue item P2 (2026-08-20) "extend the topic screen beyond
    # external_pmids" answered for this defect class.
    # ------------------------------------------------------------------
    corpus_design = []
    extraction_file = os.path.join(RESULTS, 'extracted_corpus_data.json')
    if os.path.exists(extraction_file):
        with open(extraction_file, encoding='utf-8') as f:
            corpus = json.load(f)
        for pmid, rec in (corpus.get('paper_stats') or {}).items():
            title = rec.get('title') or ''
            if title and DESIGN_TITLE.search(title):
                corpus_design.append({
                    'pmid': pmid,
                    'title': title[:160],
                    'journal': rec.get('journal'),
                    'data_points': rec.get('total_extractions', 0),
                    'extraction_types': rec.get('extraction_types', []),
                })
        corpus_design.sort(key=lambda r: -r['data_points'])

    if corpus_design:
        n = sum(r['data_points'] for r in corpus_design)
        total = (corpus.get('metadata') or {}).get('total_extractions', 0)
        pct = round(100.0 * n / total, 1) if total else 0.0
        print(f'\n[WARN] {len(corpus_design)} CORPUS paper(s) are design/protocol '
              f'papers, contributing {n} of {total} data points ({pct}%).')
        print('       A protocol paper reports planned doses, not results. Its '
              'extractions are\n       legitimate metadata but must not be '
              'counted as outcome evidence.')
        for r in corpus_design:
            print(f"  - {r['pmid']} [{r['data_points']} pts, "
                  f"{','.join(r['extraction_types'])}] {r['title'][:80]}")
    else:
        print('\n[OK] No corpus paper is a design/protocol publication.')

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({
            'generated': '2026-08-22',
            'queue_item': 'P2 2026-08-21 - baseline/design papers cited as outcome evidence',
            'design_pmids': design_pmids,
            'paths_sole_design_evidence': sole,
            'paths_mixed_evidence': mixed,
            'corpus_design_papers': corpus_design,
        }, f, indent=2, ensure_ascii=False)
    print(f'\n[OK] wrote {OUT}')

    return 1 if sole else 0


if __name__ == '__main__':
    sys.exit(main())
