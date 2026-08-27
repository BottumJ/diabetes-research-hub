#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_citation_load_bearing.py - the SEVENTH citation-defect class.

WHY THIS GATE EXISTS
--------------------
Found 2026-08-27. PMID 34763823 is Herman WH & Kuo S, "100 years of Insulin:
Why is Insulin So Expensive and What Can be Done to Control Its Cost?",
Endocrinol Metab Clin North Am 2021;50(3S):e21-e34.

It is real, current, on-topic, not retracted, correctly titled wherever a
title is asserted, and it carries valid coordinates. It passes all six
existing citation gates. It is cited 70 times across this repo, attached to:

    GLP-1 agonist pricing            $10-15K/yr, ~$1,000/month
    SGLT2i launch pricing            $5,000-$8,000/year
    GKA generic price projections    $200-$500/year by 2042-2045
    Drug development cost            $2.6B, 10-15 years; $300M average
    CGM device cost                  ~$300/device
    Verapamil/TXNIP therapy cost     $50/year
    Semaglutide generic launch       Dec 2024, $3-5/day (Hikma)
    Generic approval forecasts       5-7 approvals by 2027

A review of INSULIN pricing contains none of those figures, and a paper
published in 2021 cannot report a December 2024 launch or forecast 2027
approvals no matter what it contains.

That is the defect: ONE REAL SOURCE LENDING ITS AUTHORITY TO MANY CLAIMS IT
DOES NOT MAKE. Every individual instance passes every existing gate, because
every existing gate asks about the PAPER. This gate asks about the CLAIM.

WHAT THIS GATE CHECKS
---------------------
1. TEMPORAL_IMPOSSIBILITY - the cited text names a year LATER than the year
   the cited paper was published. Fully objective: no 2021 paper reports a
   2024 event. This needs no judgement and admits no argument, which is what
   makes it worth automating first.

2. LOAD_BEARING - one PMID attached to many DISTINCT claim contexts. This is
   a smell, not a defect: a genuine landmark trial is legitimately cited
   often, and the count alone cannot separate the two. So it is REPORTED with
   its contexts for a human to read, and only TEMPORAL_IMPOSSIBILITY fails the
   build. A gate that cried wolf on every well-cited paper would be switched
   off within a week, which is how the prose-citation gate nearly died.

Read-only. Writes one report. Exit 1 only on temporal impossibilities.
"""

import json
import os
import re
import sys
import time
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
SCRIPTS = os.path.join(BASE, 'Scripts')
REPORT = os.path.join(RESULTS, 'citation_load_bearing.json')
CACHE = os.path.join(RESULTS, '.citation_coord_cache.json')   # shared with the coordinate gate

EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
CONTEXT = 130          # chars of claim text carried with each citation
LOAD_BEARING_MIN = 8   # distinct contexts before a PMID is reported as load-bearing

RE_REF = re.compile(
    r'(?:PMID\s*[:=]?\s*(\d{7,8})'
    r'|pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,8}))', re.I)
RE_TAG = re.compile(r'<[^>]{0,400}?>')
RE_WS = re.compile(r'\s+')
RE_YEAR = re.compile(r'\b(19[5-9]\d|20[0-5]\d)\b')

# Years inside a bibliographic coordinate belong to the CITATION, not to the
# claim, and must never be read as evidence of a temporal impossibility:
#   "Diabetes Care. 2021 Apr;44(4):960-968. PMID: 33622669"
# Strip any "YYYY;VOL:PAGE" run and any "PMID: nnnnnnnn" before scanning.
RE_COORD_RUN = re.compile(
    r'\b(?:19[5-9]\d|20[0-5]\d)\s*(?:[A-Z][a-z]{2}\s*\d{0,2}\s*)?;\s*\d{1,4}'
    r'\s*(?:\([0-9A-Za-z\-]{1,10}\)\s*)?:\s*[\dA-Za-z\-]+')
RE_PMID_RUN = re.compile(r'PMID\s*[:=]?\s*\d{7,8}', re.I)

# A paper may legitimately look FORWARD. "projected 46% increase by 2050"
# cited to a 2023 GBD paper is exactly what a GBD paper is for, and the first
# draft of this gate reported it as an impossibility. The impossibility only
# holds for RETROSPECTIVE claims - an event asserted to have already happened.
# Two filters, both required, keep the accusation honest:
#   * the claim year must not be in the future (a future year is a forecast)
#   * the claim must not be phrased as a forecast
RE_PROJECTION = re.compile(
    r'\b(project|projected|projection|expect|expected|anticipat|forecast|'
    r'estimat\w*\s+(?:to|by)|will\s+\w+|by\s+20[2-5]\d|through\s+20[2-5]\d|'
    r'patent\s+expir|target|goal|scenario|model\w*\s+estimate|if\s+approved|'
    r'timeline|horizon|due\s+in|decision\s+expected)\b', re.I)

# Scripts whose PROSE is about dates by design: the audit gates document their
# own findings by date, and the _run_/_close_run_ scripts are dated run logs.
# Scanning them reports the repo's own changelog as a citation defect.
RE_SKIP_NAME = re.compile(r'^(audit_|_run_|_close_run_|_tmp_)')

# Two contexts where a year near a PMID is NOT that PMID being blamed:
#
#   LIST     "Poudyal et al. (J Nutr Metab, 2011); Hartweg et al. Curr Opin
#            Lipidol, 2009 (PMID:19133409)" - the 2011 belongs to the FIRST
#            citation in the list. The PMID is innocent and correctly placed.
#   COMMENT  "# 2026-05-14: added to the work queue ... (PMID:35466661)" - the
#            repo annotating its own history, not sourcing a claim.
#
# Instances matching either are downgraded to REVIEW rather than dropped: the
# heuristics are good enough to deprioritise a finding, not good enough to
# erase one. Only HIGH_CONFIDENCE fails the build.
RE_LIST_CITATION = re.compile(
    r'\b[A-Z][a-z]{2,}\s+(?:et\s+al\.?|and\s+[A-Z][a-z]{2,})[^;]{0,40}'
    r'(?:19[5-9]\d|20[0-5]\d)\s*[;)]')
RE_COMMENT_CTX = re.compile(r'(^|\s)#\s|\bwork queue\b|\bcanonical example\b', re.M)

SKIP_FILES = {os.path.basename(__file__)}


def strip_html(text):
    return RE_WS.sub(' ', RE_TAG.sub(' ', text)).strip()


def load_cache():
    try:
        with open(CACHE, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return {}


def resolve(pmids, cache):
    todo = sorted(p for p in pmids if p not in cache)
    for i in range(0, len(todo), 150):
        batch = todo[i:i + 150]
        url = '%s/esummary.fcgi?db=pubmed&retmode=json&id=%s' % (EUTILS, ','.join(batch))
        try:
            with urllib.request.urlopen(url, timeout=45) as fh:
                result = json.load(fh).get('result', {})
        except Exception as exc:
            sys.stderr.write('  esummary failed: %s\n' % exc)
            continue
        for pmid in batch:
            rec = result.get(pmid) or {}
            cache[pmid] = {
                'title': rec.get('title', ''),
                'journal': rec.get('source', ''),
                'year': (rec.get('pubdate', '') or '')[:4],
                'volume': (rec.get('volume', '') or '').strip(),
                'issue': (rec.get('issue', '') or '').strip(),
                'pages': (rec.get('pages', '') or '').strip(),
            }
        time.sleep(0.35)
    with open(CACHE, 'w', encoding='utf-8') as fh:
        json.dump(cache, fh, indent=1, sort_keys=True)
    return cache


def harvest(source, filename):
    out = []
    for m in RE_REF.finditer(source):
        pmid = m.group(1) or m.group(2)
        left = strip_html(source[max(0, m.start() - CONTEXT):m.start()])
        prev = None
        for mm in RE_REF.finditer(left):
            prev = mm
        if prev:
            left = left[prev.end():]
        out.append({
            'file': filename,
            'line': source.count('\n', 0, m.start()) + 1,
            'pmid': pmid,
            'claim': left.strip(),
        })
    return out


def claim_years(claim):
    """Years asserted by the CLAIM, with citation apparatus removed."""
    scrubbed = RE_PMID_RUN.sub(' ', RE_COORD_RUN.sub(' ', claim))
    return sorted({int(y) for y in RE_YEAR.findall(scrubbed)})


def main():
    refs = []
    for name in sorted(os.listdir(SCRIPTS)):
        if not name.endswith('.py') or name in SKIP_FILES:
            continue
        if RE_SKIP_NAME.match(name):
            continue
        try:
            with open(os.path.join(SCRIPTS, name), 'r', encoding='utf-8') as fh:
                src = fh.read()
        except Exception:
            continue
        refs.extend(harvest(src, name))

    print('Citation instances scanned: %d' % len(refs))
    cache = resolve({r['pmid'] for r in refs}, load_cache())

    impossible, by_pmid = [], {}
    for ref in refs:
        meta = cache.get(ref['pmid']) or {}
        try:
            pub = int(meta.get('year') or 0)
        except ValueError:
            pub = 0
        if not ref['claim']:
            continue
        by_pmid.setdefault(ref['pmid'], set()).add(ref['claim'][-CONTEXT:])
        if not pub:
            continue
        # +1 year of slack: a paper carrying a 2021 print date is routinely
        # published online in 2020 and may legitimately discuss 2022 events
        # in press. Two or more years ahead is not slack, it is impossible.
        this_year = int(time.strftime('%Y'))
        ahead = [y for y in claim_years(ref['claim'])
                 if pub + 1 < y <= this_year]
        if ahead and RE_PROJECTION.search(ref['claim']):
            ahead = []
        if ahead:
            listy = bool(RE_LIST_CITATION.search(ref['claim']))
            commenty = bool(RE_COMMENT_CTX.search(ref['claim']))
            impossible.append({
                'file': ref['file'], 'line': ref['line'], 'pmid': ref['pmid'],
                'published': pub, 'claim_years': ahead,
                'paper': meta.get('title', '')[:90],
                'claim': ref['claim'][-CONTEXT:],
                'confidence': 'REVIEW' if (listy or commenty) else 'HIGH',
                'downgraded_because': ('sibling citation in list' if listy
                                       else 'code comment / repo annotation'
                                       if commenty else ''),
            })

    load_bearing = []
    for pmid, claims in by_pmid.items():
        if len(claims) < LOAD_BEARING_MIN:
            continue
        meta = cache.get(pmid) or {}
        load_bearing.append({
            'pmid': pmid,
            'distinct_claims': len(claims),
            'paper': meta.get('title', '')[:110],
            'journal': meta.get('journal', ''),
            'year': meta.get('year', ''),
            'sample': sorted(claims)[:12],
        })
    load_bearing.sort(key=lambda r: -r['distinct_claims'])

    report = {
        'generated': time.strftime('%Y-%m-%d'),
        'citation_instances': len(refs),
        'distinct_pmids': len(by_pmid),
        'temporal_impossibilities': impossible,
        'load_bearing_threshold': LOAD_BEARING_MIN,
        'load_bearing': load_bearing,
    }
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)

    if load_bearing:
        print('\n--- LOAD-BEARING (reported, does not fail the build) ---')
        for r in load_bearing[:12]:
            print('  PMID %s  %d distinct claims  [%s %s]' % (
                r['pmid'], r['distinct_claims'], r['journal'], r['year']))
            print('     %s' % r['paper'])

    high = [r for r in impossible if r['confidence'] == 'HIGH']
    review = [r for r in impossible if r['confidence'] == 'REVIEW']
    if review:
        print('\n--- TEMPORAL, REVIEW (%d, does not fail) ---' % len(review))
        for r in review:
            print('  %s:%s PMID %s (%s) cites %s - %s' % (
                r['file'], r['line'], r['pmid'], r['published'],
                ','.join(str(y) for y in r['claim_years']),
                r['downgraded_because']))
    if high:
        print('\n--- TEMPORAL IMPOSSIBILITY, HIGH CONFIDENCE (%d) ---' % len(high))
        for r in high[:40]:
            print('  %s:%s  PMID %s published %s, claim cites %s' % (
                r['file'], r['line'], r['pmid'], r['published'],
                ','.join(str(y) for y in r['claim_years'])))
            print('     paper: %s' % r['paper'])
            print('     claim: ...%s' % r['claim'][-105:])

    report['high_confidence'] = len(high)
    report['review'] = len(review)
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
    print('\nReport: %s' % REPORT)
    if high:
        print('[FAIL] %d citation(s) attribute a past event to a paper '
              'published before it happened' % len(high))
        return 1
    print('[OK] no temporal impossibilities')
    return 0


if __name__ == '__main__':
    sys.exit(main())
