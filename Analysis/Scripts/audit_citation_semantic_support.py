#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""THE EIGHTH DEFECT CLASS: every identifier correct, the claim unsupported.

THE FINDING THAT PROMPTED THIS (2026-08-29)
-------------------------------------------
PMID 29710129 was the source for 47 cost claims across the drug repurposing
screen. It is a JAMA Oncology research LETTER titled "Total Costs of Chimeric
Antigen Receptor T-Cell Immunotherapy", whose entire abstract is one sentence
about CAR-T administration costs. It says nothing about metformin, verapamil,
generic pricing, or diabetes.

Every gate in this repo passed it, and each was right to. The PMID resolves.
The title is correct. The journal is correct. The year is correct. The first
author is correct. Seven defect classes had been built by then and not one of
them asks the only question that would have caught it: DOES THE CITED PAPER
HAVE ANYTHING TO DO WITH THE SENTENCE CITING IT?

That is a semantic distance, not an identifier match, and nothing here measured
it. This script measures it.

WHY IT REPORTS AND NEVER GATES
------------------------------
Topical overlap is a weak signal by construction. A correct citation can score
low (a mechanism paper cited for a number in its Table 2, where the citing
prose uses clinical vocabulary and the abstract uses molecular vocabulary), and
a wrong citation can score high (two papers about the same disease). A gate
built on it would fail honest citations and teach the repo to write prose that
pleases a scorer. So this ranks and reports the worst N. Deciding whether a
low scorer is wrong is a reading task, and the script's job is to say which
sentences are worth a human's ten minutes.

HOW THE SCORE IS BUILT
----------------------
Both sides are reduced to content-word sets: the citing sentence on one side,
and the cited paper's title + abstract + MeSH terms + keywords on the other.
Overlap is weighted by INVERSE DOCUMENT FREQUENCY computed across this corpus's
own abstracts, which matters more here than in a general corpus: every paper in
this library is about diabetes, so "diabetes", "patients", "glucose" and
"insulin" carry almost no discriminating power and a raw word-overlap score is
dominated by them. IDF makes "chimeric", "verapamil" and "belatacept" count and
"patients" nearly free.

    support = sum(idf of shared terms) / sum(idf of claim terms)

so the denominator is the claim's own specificity. A vague sentence cannot
score well against anything, and is reported as UNSCOREABLE rather than as a
defect - an unspecific claim is a different problem from a misattributed one.

VALIDATED AGAINST A KNOWN ANSWER, AND THE VALIDATION FOUND A LIMIT
------------------------------------------------------------------
A scorer nobody has checked is worse than no scorer, because it launders a
guess as a measurement. `--self-test` scores 29710129's ON-TOPIC uses (the
CAR-T access dashboard, where it is the right paper) against its OFF-TOPIC
uses, rather than merely checking that the PMID scores low everywhere - which
a metric could pass while having learned nothing.

Measured 2026-08-30, over 786 instances:

    support vs log(abstract words)          Pearson r = 0.226
    abstract 1-30 words    n=94    mean 0.010   median 0.000
    abstract 31-120 words  n=122   mean 0.162   median 0.133
    abstract 121-250 words n=319   mean 0.224   median 0.153
    abstract 251+ words    n=228   mean 0.216   median 0.167

The confound is a CLIFF, not a gradient: above ~30 words the score is flat and
is measuring topical fit; at or below 30 words there is not enough text on the
paper side for any claim to match, and the score is measuring abstract length.
27 corpus papers have an abstract of 30 words or fewer and they supply 94
citation instances.

This has a blunt consequence that is worth stating plainly rather than
burying: THE FOUNDING CASE IS IN THAT BAND. PMID 29710129's entire abstract is
14 words, so semantic scoring cannot convict it, and a version of this script
that ranked it first would have been right by accident. Short-abstract papers
are therefore EXCLUDED from the semantic ranking (INSUFFICIENT_PAPER_TEXT) and
routed to a second, independent signal that needs no text at all:

CLAIM DENSITY - the signal that does catch the founding case
------------------------------------------------------------
A 14-word research letter that is the cited source for 82 distinct claims is a
defect whatever any language model thinks, because there is not enough paper
there to support that many assertions. Density needs no semantics, has no
length confound, and is not defeated by vocabulary mismatch:

    claims_per_100_source_words = distinct claims / (title + abstract words)

Reported alongside the semantic ranking, not merged into it - two weak
independent signals kept separate are more legible than one blended number,
and blending them would hide which one fired.

SELF-TEST RESULT, 2026-08-30
----------------------------
    real (claim, cited paper) pairs      mean 0.213   median 0.156   n=646
    random (claim, uncited paper) pairs  mean 0.043   median 0.000
    lift 0.170 (4.92x); real beats random on 72.9% of claims, 17.0% tied
    VERDICT: DISCRIMINATES
    density signal top: 29710129 at 454.5 claims/100 source words
                        -> CATCHES_FOUNDING_CASE

KNOWN LIMITATION, MEASURED NOT ASSUMED
--------------------------------------
There is no stemming, so morphological variants do not match. The clearest
example in the 2026-08-30 output: PMID 40249888, "Decentralized Point-of-Care
Manufacturing of CD19 Chimeric Antigen Receptor T Cells in Mexico", cited for
"...represents a path to decentralization", scores 0.00 - "decentralization"
and "Decentralized" are different strings. The citation is correct and the
score is wrong. Light suffix normalisation would fix this class, and it is
filed for a MEASURED widening rather than applied here, on the same discipline
the repo applied to dose_fragment_patterns on 2026-08-20: relax one rule, count
the delta, read every newly-admitted hit before keeping it. Until then, treat
a low score as a reason to read the sentence, never as a verdict.

Never fails the build. Writes semantic_support.json.
"""

import argparse
import json
import math
import os
import re
import sys
import time
from collections import Counter

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
RESULTS = os.path.join(BASE, 'Results')
SCRIPTS = os.path.join(BASE, 'Scripts')
ABSTRACTS = os.path.join(RESULTS, 'paper_library', 'abstracts')
CACHE = os.path.join(RESULTS, '.pubtype_cache.json')
OUT = os.path.join(RESULTS, 'semantic_support.json')

# Identical harvesting rules to audit_citation_load_bearing.py. Two audits
# disagreeing about what counts as a citation would make their findings
# incomparable, which is how the 2026-08-27 coordinate gate and the published
# page ended up reporting different defects.
RE_REF = re.compile(r'(?:PMID\s*[:=]?\s*(\d{7,8})'
                    r'|pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,8}))', re.I)
RE_TAG = re.compile(r'<[^>]{0,400}?>')
RE_WS = re.compile(r'\s+')
RE_SKIP_NAME = re.compile(r'^(audit_|_run_|_close_run_|_tmp_)')
RE_WORD = re.compile(r"[A-Za-z][A-Za-z\-']{2,}")
CONTEXT = 220          # wider than load_bearing's 130: a claim needs enough
                       # words to have a measurable vocabulary at all

# Structural and presentational vocabulary. These are not stopwords in the
# linguistic sense - they are the words this repo's own HTML builders emit, and
# leaving them in would let a citation score well for sharing the word "table"
# with nothing at all.
NOISE = set('''
the and for with that this from are was were has have had not but its it's
which who whom whose their there then than they them these those such been
being can could may might will would shall should must into onto upon out off
over under about above below between among within without across per via
also more most less least much many few some any all both each other another
same very just only even still yet however therefore thus hence because since
while when where what how why does did done doing use used using uses
show shows shown showed report reports reported reporting find finds found
suggest suggests suggested indicate indicates indicated
class div span href https http www style width href container section header
footer nav html body table thead tbody tr td th ul li ol strong em br hr img
color background font size margin padding border align center left right
data value label title text link page dashboard chart card grid row col
pmid doi vol pp issue suppl et al
new note notes see also ref refs source sources cite cited citation
year years month months day days time times
'''.split())


# --- Three artifact classes found by reading the first run's own output ------
#
# The first version of this script ranked 990 instances and its bottom twelve
# were ELEVEN false positives. Every one failed for a reason that has nothing
# to do with whether the citation is sound, and shipping that list would have
# spent exactly the human attention the script exists to save. They are:
#
#  1 COORDINATE, NOT CLAIM.  "; Frey et al. Biol Blood Marrow Transplant 2019 ("
#    scored 0.00 against a paper it cites CORRECTLY. Of course it did - a
#    bibliographic coordinate is made of surnames, journal abbreviations and a
#    year, and none of those appear in an abstract. Scoring a reference string
#    for topical overlap is a category error, so these are now excluded rather
#    than scored, the same way audit_citation_load_bearing.py already
#    downgrades list citations.
#
#  2 HTML ATTRIBUTE RESIDUE.  'div class="bar-label">Carvykti ... $465K' left
#    "bar-label" in the claim, because strip_html only removes COMPLETE tags
#    and a 220-char window routinely starts inside one. The layout vocabulary
#    then counts as unsupported claim content.
#
#  3 BRAND AND PROPER NAMES.  "Carvykti (ciltacabtagene autoleucel)" cited to
#    "Cost Effectiveness of Chimeric Antigen Receptor T-Cell Therapy" is a
#    CORRECT citation that cannot score, because abstracts use generic and
#    mechanistic names while dashboards use trade names. This one is not
#    fully fixable by filtering and is handled by reporting it: an instance
#    whose unsupported terms are ALL absent from the entire corpus vocabulary
#    is marked OUT_OF_CORPUS_VOCAB, because a term no abstract anywhere uses
#    says more about the vocabulary than about the citation.
RE_ATTR = re.compile(r'\b(?:class|style|id|href|src|width|height|colspan|'
                     r'rowspan|align|target|rel|alt|title)\s*=\s*'
                     r'(?:"[^"]{0,300}"|\'[^\']{0,300}\'|[^\s>]{0,120})', re.I)
RE_OPEN_TAG_TAIL = re.compile(r'^[^<>]{0,200}?>')     # window began inside a tag
RE_ETAL_NAME = re.compile(r"\b[A-Z][A-Za-z'\-]{2,}\s+(?:et\s+al\.?|and\s+"
                          r"[A-Z][A-Za-z'\-]{2,})", re.I)
# A claim that is MOSTLY a reference string. Requires a surname-shaped token
# plus a year, or a journal-style abbreviation run plus a year, in a short
# window - the shape of "Frey et al. Biol Blood Marrow Transplant 2019".
# A coordinate can also sit at the END of an otherwise real sentence
# ("... GMP manufacturing requirements; Biol Blood Marrow Transplant 2019 (").
# The journal abbreviation and year are bibliography, not assertion, and
# counting them as unsupported claim content manufactured six of the first
# run's bottom eight. Trimmed rather than excluded: the sentence before the
# coordinate is a real claim and should still be scored.
RE_COORDINATE_TAIL = re.compile(
    r'(?:Source|Sources|See|Ref|Refs|From)?\s*[:;,]?\s*'
    r'(?:[A-Z][A-Za-z\'\-]{2,},?\s+)?'
    r'(?:(?:[A-Z][A-Za-z]{1,11}\.?|of|and|the|for)\s+){1,7}'
    r'(?:19[5-9]\d|20[0-5]\d)\s*[\s;,.)(\[\]-]*$')
RE_COORDINATE_ONLY = re.compile(
    r'^[\s;,.)(\[\]-]*(?:[A-Z][A-Za-z\'\-]{2,}\s+et\s+al\.?,?\s+)?'
    r'(?:[A-Z][A-Za-z]*\.?\s+){0,6}(?:19[5-9]\d|20[0-5]\d)[\s;,.)(\[\]-]*$')


def strip_html(text):
    text = RE_OPEN_TAG_TAIL.sub(' ', text)
    text = RE_ATTR.sub(' ', text)
    return RE_WS.sub(' ', RE_TAG.sub(' ', text)).strip()


def terms(text):
    out = set()
    for w in RE_WORD.findall((text or '').lower()):
        w = w.strip("-'")
        if len(w) < 4 or w in NOISE or w.isdigit():
            continue
        out.add(w)
    return out


def load_papers():
    """{pmid: (term_set, title, journal, year)} from the local abstract cache."""
    papers = {}
    if not os.path.isdir(ABSTRACTS):
        return papers
    for name in os.listdir(ABSTRACTS):
        if not name.endswith('.json'):
            continue
        try:
            with open(os.path.join(ABSTRACTS, name), 'r', encoding='utf-8') as fh:
                rec = json.load(fh)
        except (OSError, ValueError):
            continue
        blob = ' '.join([
            rec.get('title') or '',
            rec.get('abstract') or '',
            ' '.join(rec.get('keywords') or []),
            ' '.join(rec.get('mesh_terms') or []),
        ])
        title = rec.get('title') or ''
        abstract = rec.get('abstract') or ''
        papers[str(rec.get('pmid') or name[:-5])] = {
            'terms': terms(blob),
            'title': title,
            'journal': rec.get('journal') or '',
            'year': str(rec.get('year') or ''),
            # Source text a claim could actually be supported BY. MeSH and
            # keywords are indexing metadata, not assertions, so they are
            # deliberately excluded from the density denominator even though
            # they contribute to the term set.
            'source_words': len(title.split()) + len(abstract.split()),
            'abstract_words': len(abstract.split()),
        }
    return papers


def build_idf(papers):
    """IDF over this corpus's abstracts, so corpus-wide vocabulary costs nothing."""
    df = Counter()
    for rec in papers.values():
        df.update(rec['terms'])
    n = max(1, len(papers))
    # Smoothed. A term unseen in the corpus gets the maximum weight, which is
    # correct: a claim word that appears in no abstract anywhere is either
    # highly specific or not scientific vocabulary at all, and both cases
    # deserve to be visible rather than silently free.
    return {t: math.log((n + 1.0) / (c + 1.0)) + 1.0 for t, c in df.items()}, \
           math.log(n + 1.0) + 1.0


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
        out.append({'file': filename,
                    'line': source.count('\n', 0, m.start()) + 1,
                    'pmid': pmid,
                    'claim': left.strip()})
    return out


def score(claim_terms, paper_terms, idf, default_idf):
    if not claim_terms:
        return None, [], []
    weight = lambda t: idf.get(t, default_idf)
    total = sum(weight(t) for t in claim_terms)
    if total <= 0:
        return None, [], []
    shared = claim_terms & paper_terms
    missing = claim_terms - paper_terms
    got = sum(weight(t) for t in shared)
    top_missing = sorted(missing, key=lambda t: -weight(t))[:6]
    top_shared = sorted(shared, key=lambda t: -weight(t))[:6]
    return got / total, top_shared, top_missing


# Below this, the claim has too little specific vocabulary for any score to
# mean anything. Reported separately so a vague sentence is never mistaken
# for a misattributed one.
MIN_CLAIM_TERMS = 4

# At or below this many abstract words there is not enough paper-side text for
# any claim to match, and the score degenerates to a measure of abstract
# length. Measured, not assumed - see the docstring table. Instances against
# these papers are excluded from the ranking and reported under claim density
# instead.
MIN_ABSTRACT_WORDS = 30


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--worst', type=int, default=25)
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()

    papers = load_papers()
    if not papers:
        print('  [skip] no local abstracts to score against')
        return 0
    idf, default_idf = build_idf(papers)
    print('  Abstracts loaded: %d   distinct corpus terms: %d'
          % (len(papers), len(idf)))

    refs = []
    me = os.path.basename(__file__)
    for name in sorted(os.listdir(SCRIPTS)):
        if not name.endswith('.py') or name == me or RE_SKIP_NAME.match(name):
            continue
        try:
            with open(os.path.join(SCRIPTS, name), 'r', encoding='utf-8') as fh:
                refs.extend(harvest(fh.read(), name))
        except (OSError, UnicodeDecodeError):
            continue

    scored, unscoreable, coordinate_only, no_abstract = [], 0, 0, set()
    thin_text = {}
    for ref in refs:
        if ref['pmid'] not in papers:
            no_abstract.add(ref['pmid'])
            continue
        claim = ref['claim']
        if RE_COORDINATE_ONLY.match(claim):
            coordinate_only += 1
            continue
        # Author names are never abstract vocabulary; leaving them in
        # manufactures unsupported terms for correctly-cited papers.
        claim = RE_ETAL_NAME.sub(' ', claim)
        claim = RE_COORDINATE_TAIL.sub(' ', claim).strip()
        ct = terms(claim)
        if len(ct) < MIN_CLAIM_TERMS:
            unscoreable += 1
            continue
        pap = papers[ref['pmid']]
        if pap['abstract_words'] <= MIN_ABSTRACT_WORDS:
            thin_text.setdefault(ref['pmid'], []).append(ref)
            continue
        title, journal, year = pap['title'], pap['journal'], pap['year']
        s, shared, missing = score(ct, pap['terms'], idf, default_idf)
        if s is None:
            unscoreable += 1
            continue
        # A term absent from EVERY abstract in the corpus is out-of-vocabulary
        # (trade names, proper nouns, repo jargon), not evidence that this
        # paper fails to support the claim.
        oov = [t for t in missing if t not in idf]
        scored.append({
            'pmid': ref['pmid'], 'file': ref['file'], 'line': ref['line'],
            'support': round(s, 3),
            'flag': 'OUT_OF_CORPUS_VOCAB' if missing and len(oov) == len(missing) else '',
            'claim': claim[-180:],
            'paper_title': title[:150], 'journal': journal, 'year': year,
            'shared_terms': shared, 'unsupported_terms': missing,
        })

    # --- independent signal: claim density against source text -------------
    # Counts DISTINCT claim strings, not instances: the same sentence emitted
    # into two dashboards is one assertion resting on the paper, not two.
    density = []
    per_pmid = {}
    for ref in refs:
        if ref['pmid'] in papers and ref['claim']:
            per_pmid.setdefault(ref['pmid'], set()).add(ref['claim'][-130:])
    for pmid, claims in per_pmid.items():
        pap = papers[pmid]
        words = max(1, pap['source_words'])
        density.append({
            'pmid': pmid,
            'distinct_claims': len(claims),
            'source_words': pap['source_words'],
            'claims_per_100_source_words': round(100.0 * len(claims) / words, 1),
            'abstract_words': pap['abstract_words'],
            'title': pap['title'][:140],
            'journal': pap['journal'],
            'year': pap['year'],
            'semantically_scoreable': pap['abstract_words'] > MIN_ABSTRACT_WORDS,
        })
    density.sort(key=lambda r: -r['claims_per_100_source_words'])

    scored.sort(key=lambda r: r['support'])
    print('  Citation instances: %d   scored: %d' % (len(refs), len(scored)))
    print('  Excluded: %d bibliographic-coordinate-only, %d claim too vague'
          % (coordinate_only, unscoreable))
    print('  PMIDs with no local abstract (not scored): %d' % len(no_abstract))

    self_test = None
    if args.self_test and scored:
        self_test = run_self_test(scored, papers, idf, default_idf, density)

    report = {
        'generated': time.strftime('%Y-%m-%d'),
        'method': ('IDF-weighted content-word overlap between the citing '
                   'sentence and the cited title+abstract+MeSH+keywords; IDF '
                   'computed over this corpus so corpus-wide vocabulary is '
                   'nearly free'),
        'gates': False,
        'instances_scanned': len(refs),
        'instances_scored': len(scored),
        'unscoreable_vague_claim': unscoreable,
        'excluded_coordinate_only': coordinate_only,
        'excluded_insufficient_paper_text': sum(len(v) for v in thin_text.values()),
        'excluded_insufficient_paper_text_pmids': sorted(thin_text),
        'min_abstract_words': MIN_ABSTRACT_WORDS,
        'length_confound_measured_2026_08_30': {
            'pearson_r_support_vs_log_abstract_words': 0.226,
            'bands': {'1-30w': {'n': 94, 'median': 0.0},
                      '31-120w': {'n': 122, 'median': 0.133},
                      '121-250w': {'n': 319, 'median': 0.153},
                      '251+w': {'n': 228, 'median': 0.167}},
            'note': ('confound is a cliff at ~30 abstract words, not a '
                     'gradient; papers at or below it are excluded from the '
                     'semantic ranking'),
        },
        'claim_density': density[:40],
        'pmids_without_local_abstract': sorted(no_abstract),
        'min_claim_terms': MIN_CLAIM_TERMS,
        'self_test': self_test,
        'worst': scored[:args.worst],
        'all_scores': [{'pmid': r['pmid'], 'file': r['file'], 'line': r['line'],
                        'support': r['support']} for r in scored],
    }
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)

    print()
    print('  WORST %d BY SEMANTIC SUPPORT (low = citing sentence shares little'
          % args.worst)
    print('  specific vocabulary with the paper it cites)')
    print()
    for r in scored[:args.worst]:
        print('  %.2f  %-9s %-34s:%-5s %s %s'
              % (r['support'], r['pmid'], r['file'][:34], r['line'],
                 r['journal'][:22], r['flag']))
        print('        CLAIM: %s' % r['claim'][-96:].strip())
        print('        PAPER: %s' % r['paper_title'][:96])
        if r['unsupported_terms']:
            print('        UNSUPPORTED: %s' % ', '.join(r['unsupported_terms']))
    print()
    print('  HIGHEST CLAIM DENSITY (distinct claims per 100 words of title+abstract).')
    print('  Independent of the score above and immune to its length confound:')
    print('  a paper cannot support more assertions than it contains text for.')
    print()
    print('  %-6s %-9s %-7s %-7s %-5s %s'
          % ('/100w', 'PMID', 'CLAIMS', 'WORDS', 'SEM?', 'PAPER'))
    for d in density[:12]:
        print('  %-6.1f %-9s %-7d %-7d %-5s %s'
              % (d['claims_per_100_source_words'], d['pmid'],
                 d['distinct_claims'], d['source_words'],
                 'y' if d['semantically_scoreable'] else 'NO',
                 d['title'][:52]))
    print()
    print('  [OK] wrote %s  (reports only, never gates)' % os.path.basename(OUT))
    return 0


def run_self_test(scored, papers, idf, default_idf, density):
    """Does the score detect topical fit at all? Tested against random pairings.

    The first version of this test used one probe PMID, and the filter added
    later - excluding papers with almost no abstract - removed that probe from
    the scored set entirely, leaving the test INCONCLUSIVE by construction.
    A validation that a later fix can silently disable was the wrong design.

    This replaces it with a discrimination test that needs no probe. Every
    scored claim is ALSO scored against a randomly drawn corpus paper it does
    not cite. If the metric measures topical fit, real (claim, cited paper)
    pairs must score materially above random (claim, unrelated paper) pairs.
    If they do not, the number is noise and the ranking above means nothing.

    Deterministic seed so the reported figure is reproducible.
    """
    import random
    rng = random.Random(20260830)
    pool = [p for p, rec in papers.items()
            if rec['abstract_words'] > MIN_ABSTRACT_WORDS]
    real, rand = [], []
    for r in scored:
        ct = terms(r['claim'])
        if not ct:
            continue
        other = rng.choice(pool)
        if other == r['pmid']:
            continue
        s_rand, _, _ = score(ct, papers[other]['terms'], idf, default_idf)
        if s_rand is None:
            continue
        real.append(r['support'])
        rand.append(s_rand)
    mean = lambda v: round(sum(v) / len(v), 4) if v else None
    med = lambda v: round(sorted(v)[len(v) // 2], 4) if v else None
    out = {
        'design': ('real (claim, cited paper) pairs vs random (claim, '
                   'uncited corpus paper) pairs; seed 20260830'),
        'pairs': len(real),
        'real_mean': mean(real), 'real_median': med(real),
        'random_mean': mean(rand), 'random_median': med(rand),
    }
    if real:
        lift = out['real_mean'] - out['random_mean']
        out['lift'] = round(lift, 4)
        out['lift_ratio'] = (round(out['real_mean'] / out['random_mean'], 2)
                             if out['random_mean'] else None)
        wins = sum(1 for a, b in zip(real, rand) if a > b)
        ties = sum(1 for a, b in zip(real, rand) if a == b)
        out['real_beats_random_pct'] = round(100.0 * wins / len(real), 1)
        out['tied_pct'] = round(100.0 * ties / len(real), 1)
        out['verdict'] = ('DISCRIMINATES' if lift >= 0.05 and wins / len(real) > 0.55
                          else 'WEAK' if lift > 0.01 else 'FAILS')
    else:
        out['verdict'] = 'NO_PAIRS'

    # The density signal gets its own check: it must rank the founding case
    # first, and that case must be one semantics could NOT reach.
    if density:
        top = density[0]
        out['density_check'] = {
            'top_pmid': top['pmid'],
            'claims_per_100_source_words': top['claims_per_100_source_words'],
            'semantically_scoreable': top['semantically_scoreable'],
            'verdict': ('CATCHES_FOUNDING_CASE' if top['pmid'] == '29710129'
                        else 'TOP_IS_' + top['pmid']),
        }

    print()
    print('  SELF-TEST - does the score detect topical fit?')
    print('    real pairs   mean %-7s median %s  (n=%d)'
          % (out['real_mean'], out['real_median'], out['pairs']))
    print('    random pairs mean %-7s median %s'
          % (out['random_mean'], out['random_median']))
    print('    lift %s (%sx)   real beats random on %s%% of claims, tied %s%%'
          % (out.get('lift'), out.get('lift_ratio'),
             out.get('real_beats_random_pct'), out.get('tied_pct')))
    print('    VERDICT: %s' % out['verdict'])
    if 'density_check' in out:
        d = out['density_check']
        print('    density signal top: %s at %s claims/100w -> %s'
              % (d['top_pmid'], d['claims_per_100_source_words'], d['verdict']))
    return out


if __name__ == '__main__':
    sys.exit(main())
