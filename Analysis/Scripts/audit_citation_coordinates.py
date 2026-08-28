#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_citation_coordinates.py - the SIXTH citation-defect class.

WHY THIS GATE EXISTS
--------------------
Every citation control this repo owns asks a question about IDENTITY:

    verify_pmids.py                does this PMID resolve at all?
    audit_index_provenance.py      did this PMID enter through a real door?
    topic screening                is the paper on-topic?
    audit_builder_title_agreement  does the title a builder ASSERTS for a PMID
                                   match the title PubMed returns?
    audit_prose_citation_titles    does the surrounding prose name the same
                                   paper the PMID resolves to?
    audit_retractions.py           has the paper been withdrawn?

All six are silent on a defect found on 2026-08-27 in build_gka_lada.py:

    <div class="evidence-detail">
        Matschinsky FM et al. (2009). Comprehensive review of glucokinase as
        beta cell glucose sensor. ...
    </div>
    <div class="data-source">
        Diabetes. 2009 Jul;58(7):1416-28. PMID:19373249.
    </div>

PMID 19373249 resolves. It is on-topic. It is not retracted. The prose
describes it CORRECTLY - it really is Matschinsky's 2009 glucokinase review.
audit_prose_citation_titles.py scores the title overlap and passes it.

But the paper is Nat Rev Drug Discov 2009;8(5):399-416. The string
"Diabetes. 2009 Jul;58(7):1416-28" resolves to NOTHING. Diabetes volume 58
issue 7 exists and contains 34 articles; page 1416 is not among them. The
citation is a well-formed, authoritative-looking bibliographic coordinate for
a paper that does not exist, sitting directly beneath prose that is accurate.

That is the defect class: THE NARRATIVE IS RIGHT AND THE COORDINATES ARE
INVENTED. A title gate cannot catch it, because a title gate reads the
narrative - and the narrative is the part that is true.

WHAT THIS GATE CHECKS
---------------------
Only explicit numeric coordinates: YEAR;VOLUME(ISSUE):PAGES, in a window
around a PMID. Those are falsifiable against PubMed and cheap to check. Prose
without coordinates is NOT this gate's business - audit_prose_citation_titles
already owns that surface, and duplicating it here would double the false
alarms without adding a fact.

Verdicts, in descending severity:

  NONRESOLVING     the asserted coordinate matches no PubMed record at all.
                   The most serious: the string was not copied from anywhere.
  POINTS_ELSEWHERE the coordinate resolves, but to a DIFFERENT PMID than the
                   one attached. A mis-paste, not an invention.
  COORD_MISMATCH   coordinate disagrees with the attached PMID and could not
                   be probed independently (no journal token recognised).
  OK               volume and first page agree with the attached PMID.

NONRESOLVING is separated from POINTS_ELSEWHERE on purpose. "You cited the
wrong real paper" and "you cited a paper that was never published" are
different failures with different causes, and collapsing them would hide the
second inside the first - the same mistake not_corpus_pmids.json was extended
on 2026-08-26 to avoid when RETRACTION was filed under PROVENANCE.

Read-only. Writes one report. Exit 1 on any non-OK verdict.
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
SCRIPTS = os.path.join(BASE, 'Scripts')
REPORT = os.path.join(RESULTS, 'citation_coordinates.json')
CACHE = os.path.join(RESULTS, '.citation_coord_cache.json')

EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
WINDOW = 200          # chars scanned on each side of a PMID marker
# A trailing coordinate belongs to this PMID until a LIST SEPARATOR appears.
# Distance was the first attempt and it was wrong in both directions: 12 chars
# suppressed the real defect at build_gka_landscape.py:1144, where the
# coordinate legitimately trails its PMID by ~120 characters:
#     <strong>PMID:30949058</strong> | Matschinsky FM. "..." Diabetes Care.
#     2002;25(10):1897-1902.
# while any radius large enough to catch it also swallowed the NEXT entry in
# a citation list:
#     (PMID:32307525) - biphasic decline in LADA; Latres E et al. Diabetes
#     2024;73(6):823-833 (PMID:38349844)
# "; " separates list entries in this repo's citation strings and cannot occur
# inside a coordinate, where the semicolon is always followed by a digit.
# Structure discriminates where distance could not.
RE_LIST_SEP = re.compile(r';\s')

# Block-level boundaries: a new cell, row, list item or paragraph starts a
# new citation. Matched against RAW source, before strip_html flattens it.
RE_BLOCK_END = re.compile(r'</(?:td|tr|li|p|div|h[1-6])>', re.I)
YEAR_SLACK = 1        # e-pub ahead of print legitimately shifts the year by 1

RE_REF = re.compile(
    r'(?:PMID\s*[:=]?\s*(\d{7,8})'
    r'|pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,8}))', re.I)

# "2009 Jul;58(7):1416-28"  /  "2004 Jan;21(1):31-7"  /  "2021;44(4):960-968"
# The month is optional and the issue is optional, because both are routinely
# dropped in hand-written citations. Volume and first page are NOT optional:
# they are the two fields that make the coordinate falsifiable.
RE_COORD = re.compile(
    r'\b(19[5-9]\d|20[0-4]\d)\s*'
    r'(?:[A-Z][a-z]{2}\s*\d{0,2}\s*)?'
    r';\s*(\d{1,4})\s*'
    r'(?:\(\s*([0-9A-Za-z\-]{1,10})\s*\)\s*)?'
    r':\s*(\d{1,7})')

RE_TAG = re.compile(r'<[^>]{0,400}?>')
RE_WS = re.compile(r'\s+')

# Journal token sitting immediately before the year. Used only to PROBE an
# asserted coordinate independently; an unrecognised journal downgrades the
# verdict to COORD_MISMATCH rather than asserting NONRESOLVING on no evidence.
RE_JOURNAL_HEAD = re.compile(
    r'([A-Z][A-Za-z&\.\- ]{2,44}?)\.?\s*'
    r'(?:19[5-9]\d|20[0-4]\d)\s*'
    r'(?:[A-Z][a-z]{2}\s*\d{0,2}\s*)?;')

SKIP_FILES = {os.path.basename(__file__)}

# Documentation of a defect is not the defect. The comment in
# run_quality_improvements.py that explains WHY this gate exists necessarily
# quotes the fabricated coordinate it was built to catch, and on the gate's
# first wired run it dutifully reported that comment as a live defect.
#
# Blanket-skipping audit_*.py and the pipeline runner would fix it and open a
# blind spot: those files also carry real citations. So the opt-out is an
# EXPLICIT marker that must be written next to the example, which means every
# suppression is visible in the diff and greppable later. Silence has to be
# requested by name, never inherited from a filename.
EXEMPT_MARKER = 'CITATION-EXAMPLE'
EXEMPT_RADIUS = 1200   # generous on purpose: the marker is opt-IN, never inherited

# AUDIT TRAIL vs LIVE EVIDENCE (added 2026-08-28).
#
# The gate went red on 5 coordinates, all 5 inside _run_2026_08_27.py - the
# dated close-out script that RECORDS the miscitations it repaired the day
# before. Every one of them is a quotation of a defect, written down so the
# repair is explicable. Four are proximity artifacts on top of that: the
# harvester pairs a PMID from one repair tuple with a coordinate from the
# next, because these files are prose about citations rather than citations.
#
# The two coordinates that also appear in LIVE builders were checked by hand
# before this exemption was written, and both are correct:
#   Latres E, Diabetes 2024;73(6):823-833 -> PMID 38349844 (build_gka_lada.py)
#   Speake C, Nat Rev Endocrinol 2023;19(7):377-378 -> 37202589 (build_data_dictionary.py)
# The gate's own probe resolved both coordinates to exactly those PMIDs. So
# nothing is being suppressed here that is wrong on the site.
#
# Repairing the run files instead would be worse than the finding: it would
# edit the historical record of a repair to make a gate green. This is the
# THIRD time this repo has hit the shape - audit_retractions.py counted its
# own exclusion registry, audit_citation_identifiers.py needed
# AUDIT_TRAIL_FIELDS - so it is applied here as the established rule rather
# than rediscovered. Reported, never failed; the count is printed so the
# category can never go silent.
# NEGATIVE CONTROL, run 2026-08-28 before this exemption was accepted: a
# fabricated coordinate ("Diabetes Care 1999;22(3):999-1000. PMID:32847960")
# was appended to build_lada_prevalence.py, a LIVE builder. The gate failed
# with exactly 1 live suspect while the 5 audit-trail records stayed reported
# and non-failing; the injection was then reverted. An exemption is only
# worth having if the gate still fires without it, and that was measured
# rather than assumed.
RE_ONESHOT = re.compile(r'^(_run_|_close_run_|_tmp_)|_\d{8}\.py$')


def is_audit_trail(filename):
    return bool(RE_ONESHOT.match(filename) or RE_ONESHOT.search(filename))


def strip_html(text):
    return RE_WS.sub(' ', RE_TAG.sub(' ', text)).strip()


def load_cache():
    try:
        with open(CACHE, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return {}


def save_cache(cache):
    with open(CACHE, 'w', encoding='utf-8') as fh:
        json.dump(cache, fh, indent=1, sort_keys=True)


def fetch(url):
    with urllib.request.urlopen(url, timeout=45) as fh:
        return json.load(fh)


def resolve(pmids, cache):
    """esummary in bulk; cache by PMID so repeat runs cost no requests."""
    todo = sorted(p for p in pmids if p not in cache)
    for i in range(0, len(todo), 150):
        batch = todo[i:i + 150]
        url = '%s/esummary.fcgi?db=pubmed&retmode=json&id=%s' % (
            EUTILS, ','.join(batch))
        try:
            result = fetch(url).get('result', {})
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
    return cache


def clean_journal(raw):
    """Trim a captured journal head down to the journal name itself.

    RE_JOURNAL_HEAD walks backwards from the year and happily swallows the end
    of the preceding sentence: "...for GKA intervention. UKPDS Group. Diabet
    Med 2004;21(1):31". Probing PubMed for a journal called "GKA intervention.
    UKPDS Group. Diabet Med" returns nothing, which the gate would then report
    as NONRESOLVING - a true verdict reached by a false route, and one that
    would go on being true even after the citation was repaired.

    Keep only the final sentence-segment, then drop leading words that are
    lowercase or that end a sentence, since journal abbreviations do not.
    """
    seg = (raw or '').strip().rstrip('.').split('. ')[-1].strip()
    words = [w for w in seg.split() if w]
    while words and not re.match(r'^[A-Z]', words[0]):
        words.pop(0)
    # "UKPDS Group Diabet Med" -> a group name is not a journal. Cap the
    # abbreviation at its last 5 tokens and let the probe's phrasesnotfound
    # branch downgrade anything still wrong to COORD_MISMATCH.
    return ' '.join(words[-5:])


def first_page(pages):
    m = re.match(r'\s*([A-Za-z]?\d+)', pages or '')
    return m.group(1) if m else ''


def _esearch(term):
    url = '%s/esearch.fcgi?db=pubmed&retmode=json&retmax=5&term=%s' % (
        EUTILS, urllib.parse.quote(term))
    try:
        res = fetch(url).get('esearchresult', {})
    except Exception:
        return None
    time.sleep(0.35)
    return res


def probe(journal, volume, page, control_cache):
    """Does the ASSERTED coordinate resolve to any record at all?

    A NEGATIVE result here is the whole point of the gate - it is what
    licenses the word NONRESOLVING, which is the strongest accusation this
    repo makes about a citation. So the negative has to be earned.

    PubMed's [ta] field indexes NLM abbreviations and SOME full titles, with
    no rule that predicts which. Measured 2026-08-27:

        "Nature Reviews Endocrinology"[ta]    -> 3059 records
        "Journal of Clinical Investigation"[ta] ->   0 records
        "Trends in Endocrinology & Metabolism"[ta] -> 0 records

    All three are real, current, indexed journals. The middle two simply have
    to be spelled "J Clin Invest" and "Trends Endocrinol Metab". Critically,
    NCBI returns those as an empty idlist with NO phrasesnotfound error, so
    the obvious guard does not fire and a zero-result query looks exactly like
    a coordinate that was invented.

    The first draft of this gate reported three build_data_dictionary.py
    citations as NONRESOLVING on precisely that basis. The verdict was reached
    by a broken instrument, and it would have stayed "true" no matter how the
    citation was repaired. So: run a positive control on the journal alone
    first. If the journal token returns nothing, this gate cannot see the
    journal at all and must say COORD_MISMATCH - a claim about disagreement,
    which is still supported - instead of NONRESOLVING, a claim about
    non-existence, which is not.
    """
    if journal not in control_cache:
        res = _esearch('"%s"[ta]' % journal)
        control_cache[journal] = None if res is None else int(res.get('count', 0) or 0)
    control = control_cache[journal]
    if not control:
        return None          # journal token unusable -> cannot conclude

    res = _esearch('"%s"[ta] AND %s[vi] AND %s[pg]' % (journal, volume, page))
    if res is None:
        return None
    if (res.get('errorlist') or {}).get('phrasesnotfound'):
        return None
    return res.get('idlist', [])


def harvest(source, filename):
    """Every PMID that has a numeric coordinate within WINDOW chars."""
    out, seen = [], set()
    for m in RE_REF.finditer(source):
        pmid = m.group(1) or m.group(2)
        neighbourhood = source[max(0, m.start() - EXEMPT_RADIUS):
                               m.end() + EXEMPT_RADIUS]
        if EXEMPT_MARKER in neighbourhood:
            continue
        left = strip_html(source[max(0, m.start() - WINDOW):m.start()])
        # Cut the RIGHT window at the first block-level boundary, BEFORE the
        # tags are stripped. A coordinate in the next table cell, list item or
        # paragraph is a different citation, and strip_html destroys the only
        # evidence of that:
        #   <td>...(PMID:36449148)</td><td>Khan MAB et al. J Epidemiol Glob
        #   Health 2020;10(1):107-111 (PMID:32175717)</td>
        # flattens to one run of prose in which Khan's coordinate appears to
        # trail the dorzagliatin PMID. Structure that exists in the source has
        # to be consumed before it is thrown away.
        right_raw = source[m.end():m.end() + WINDOW]
        bound = RE_BLOCK_END.search(right_raw)
        if bound:
            right_raw = right_raw[:bound.start()]
        right = strip_html(right_raw)
        # A coordinate BEFORE the PMID belongs to it ("Diabetes. 2009
        # Jul;58(7):1416-28. PMID:19373249"). A coordinate AFTER the PMID only
        # belongs to it if no other PMID intervenes, otherwise it is the next
        # entry's. Cut BOTH windows at the neighbouring marker.
        #
        # Cutting the left window matters as much as the right. A data-source
        # div that lists five citations - "Diabetes 2013;62(12):4297. PMID:a;
        # Buzzetti PMID:b; Mishra PMID:c" - otherwise hands the SAME leading
        # coordinate to b and c, and the gate then reports three defects where
        # the author wrote one. A gate that multiplies a single mistake into
        # three teaches the reader to discount its count.
        prev = None
        for mm in RE_REF.finditer(left):
            prev = mm
        if prev:
            left = left[prev.end():]
        nxt = RE_REF.search(right)
        if nxt:
            right = right[:nxt.start()]
        for side, text in (('left', left), ('right', right)):
            hits = list(RE_COORD.finditer(text))
            if not hits:
                continue
            # nearest coordinate to the marker wins
            hit = hits[-1] if side == 'left' else hits[0]
            # A coordinate to the RIGHT of a PMID belongs to it only when it
            # trails immediately: "PMID: 33622669. Diabetes Care. 2021
            # Apr;44(4):960-968". In a citation LIST the next entry's
            # coordinate also sits to the right and before the next marker:
            #   "(PMID:32307525) - biphasic decline in LADA; Latres E et al.
            #    Diabetes 2024;73(6):823-833 (PMID:38349844)"
            # Attributing Latres' coordinate to Li's PMID invents a defect.
            # Cutting at the next MARKER is not enough because the coordinate
            # precedes that marker; distance is the discriminator that works.
            if side == 'right':
                sep = RE_LIST_SEP.search(text)
                if sep and hit.start() > sep.start():
                    continue
            year, volume, issue, page = hit.groups()
            head = RE_JOURNAL_HEAD.search(text[:hit.end()])
            journal = clean_journal(head.group(1) if head else '')
            key = (filename, pmid, year, volume, page)
            if key in seen:
                continue
            seen.add(key)
            out.append({
                'file': filename,
                'line': source.count('\n', 0, m.start()) + 1,
                'pmid': pmid,
                'asserted': {
                    'journal': journal, 'year': year,
                    'volume': volume, 'issue': issue or '', 'page': page,
                },
                'record': text[-160:] if side == 'left' else text[:160],
            })
            break
    return out


def main():
    refs = []
    for name in sorted(os.listdir(SCRIPTS)):
        if not name.endswith('.py') or name in SKIP_FILES:
            continue
        path = os.path.join(SCRIPTS, name)
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                src = fh.read()
        except Exception:
            continue
        refs.extend(harvest(src, name))

    print('Citation coordinates found: %d' % len(refs))
    if not refs:
        print('[OK] no explicit bibliographic coordinates to check')
        return 0

    cache = load_cache()
    cache = resolve({r['pmid'] for r in refs}, cache)
    save_cache(cache)

    control_cache = {}
    buckets = {'OK': [], 'COORD_MISMATCH': [],
               'POINTS_ELSEWHERE': [], 'NONRESOLVING': [], 'UNRESOLVED': []}

    for ref in refs:
        meta = cache.get(ref['pmid']) or {}
        if not meta.get('journal') and not meta.get('volume'):
            ref['verdict'] = 'UNRESOLVED'
            buckets['UNRESOLVED'].append(ref)
            continue
        ref['actual'] = meta
        a = ref['asserted']
        vol_ok = (a['volume'] == meta.get('volume', ''))
        page_ok = (a['page'] == first_page(meta.get('pages', '')))
        try:
            year_ok = abs(int(a['year']) - int(meta.get('year') or 0)) <= YEAR_SLACK
        except ValueError:
            year_ok = False
        ref['checks'] = {'volume': vol_ok, 'page': page_ok, 'year': year_ok}

        if vol_ok and page_ok:
            ref['verdict'] = 'OK'
            buckets['OK'].append(ref)
            continue

        # Disagrees with the attached PMID. Is the asserted coordinate real?
        found = (probe(a['journal'], a['volume'], a['page'], control_cache)
                 if a['journal'] else None)
        if found is None:
            ref['verdict'] = 'COORD_MISMATCH'
            ref['probe'] = 'journal token not indexed - could not conclude'
        elif not found:
            ref['verdict'] = 'NONRESOLVING'
            ref['probe'] = 'no PubMed record at %s %s:%s' % (
                a['journal'], a['volume'], a['page'])
        else:
            ref['verdict'] = 'POINTS_ELSEWHERE'
            ref['probe'] = 'coordinate resolves to PMID %s' % ','.join(found)
        buckets[ref['verdict']].append(ref)

    report = {
        'generated': time.strftime('%Y-%m-%d'),
        'window_chars': WINDOW,
        'coordinates_checked': len(refs),
        'counts': {k: len(v) for k, v in buckets.items()},
        'nonresolving': buckets['NONRESOLVING'],
        'points_elsewhere': buckets['POINTS_ELSEWHERE'],
        'coord_mismatch': buckets['COORD_MISMATCH'],
        'unresolved': buckets['UNRESOLVED'],
        'ok': buckets['OK'],
    }
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)

    for label in ('NONRESOLVING', 'POINTS_ELSEWHERE', 'COORD_MISMATCH', 'UNRESOLVED'):
        rows = buckets[label]
        if not rows:
            continue
        print('\n--- %s (%d) ---' % (label, len(rows)))
        for r in rows:
            a = r['asserted']
            act = r.get('actual', {})
            print('  %s:%s  PMID %s' % (r['file'], r['line'], r['pmid']))
            print('     ASSERTED %s %s;%s(%s):%s' % (
                a['journal'] or '?', a['year'], a['volume'], a['issue'], a['page']))
            if act:
                print('     ACTUAL   %s %s;%s(%s):%s' % (
                    act.get('journal', '?'), act.get('year', '?'),
                    act.get('volume', '?'), act.get('issue', ''), act.get('pages', '?')))
            if r.get('probe'):
                print('     PROBE    %s' % r['probe'])

    suspect = [r for k in ('NONRESOLVING', 'POINTS_ELSEWHERE',
                           'COORD_MISMATCH', 'UNRESOLVED')
               for r in buckets[k]]
    live = [r for r in suspect if not is_audit_trail(r['file'])]
    trail = [r for r in suspect if is_audit_trail(r['file'])]
    bad = len(live)

    print('\nReport: %s' % REPORT)
    print('Checked %d coordinates: %d OK, %d suspect (%d live, %d audit-trail)'
          % (len(refs), len(buckets['OK']), len(suspect), bad, len(trail)))
    if trail:
        # Printed, not hidden. A category that stops being counted is a
        # category that can start hiding real defects.
        print('  Audit-trail records quoting a repaired defect (do not fail):')
        for r in trail:
            print('    %s:%s  PMID %s' % (r['file'], r['line'], r['pmid']))
    if bad:
        print('[FAIL] %d citation coordinate(s) do not match their PMID' % bad)
        return 1
    print('[OK] every bibliographic coordinate matches its PMID')
    return 0


if __name__ == '__main__':
    sys.exit(main())
