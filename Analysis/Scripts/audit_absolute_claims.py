#!/usr/bin/env python3
"""An absolute clinical claim must cite a PMID whose abstract says the same
absolute thing.

WHY THIS EXISTS
---------------
The credibility sweep in this repo greps for overstatement and then asks a human
(or an unattended run) to judge each hit in free text. The judgement is where it
fails. Both overstatements repaired on 2026-08-25 had been read by earlier
sweeps and written up as "factual/contextual":

    monitor_report_2026-04-11    inspected, cleared
    iterate_run_report_2026-05-22 inspected, cleared

"Eliminates hypoglycemia risk" sat live on the site for four months after being
looked at twice. The grep worked. The adjudication did not, because
"is this overstated?" has no answer that can be checked, so the answer drifts
toward whatever lets the run finish.

THE RULE THAT REPLACES IT
-------------------------
An absolute verb (eliminates, abolishes, prevents, guarantees, achieves, cures,
normalises, reverses, ensures, or a zero/100%/completely/always quantifier)
attached to a CLINICAL ENDPOINT is a claim of the strongest possible kind. It
must satisfy both of:

  1. It cites a PMID within CITE_WINDOW characters.
  2. That PMID's PubMed abstract itself contains an absolute of the same
     family.

If the abstract says "reduced hypoglycaemia by 40%", the page may not say
"eliminates hypoglycaemia". That comparison is mechanical: fetch the abstract,
look for the absolute, decide. There is no judgement left to drift.

VERDICTS
--------
  UNSOURCED_ABSOLUTE  no PMID anywhere near the claim -- fails
  OVERSTATED          PMID cited, abstract contains no absolute -- fails
  SUPPORTED           abstract carries a matching absolute -- passes
  NO_ABSTRACT         PubMed has no abstract text (editorial, chapter, some
                      older records). Reported and counted, NOT failed: absence
                      of an abstract is a fact about the record, not evidence
                      the claim is wrong. These need a human to read the paper.

Negated absolutes are skipped by design. "Nicotinamide did NOT prevent T1D" and
"insulin does not eliminate hypoglycaemia risk" are the honest form of the
sentence; failing them would push the text toward vagueness rather than
accuracy, which is the opposite of the point.

Exit 1 on any UNSOURCED_ABSOLUTE or OVERSTATED.
Output: Analysis/Results/absolute_claims.json

LIMIT, STATED
-------------
This checks that an absolute is ECHOED by the source abstract. It does not check
that the abstract's absolute is about the same endpoint in the same population.
A paper reporting "complete remission" in mice cited for "eliminates
hypoglycaemia" in humans passes this gate and is caught by the preclinical-
overstatement rules elsewhere. Reported so the coverage is not overread.
"""

import html
import json
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_citation_identifiers import _get, TOOL  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
SCRIPTS = os.path.join(BASE, 'Scripts')
REPORT = os.path.join(RESULTS, 'absolute_claims.json')
ABS_CACHE = os.path.join(RESULTS, '.abstract_cache.json')

EFETCH = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
CITE_WINDOW = 400

RE_TAG = re.compile(r'<[^>]{0,400}?>')
RE_WS = re.compile(r'\s+')
RE_PMID = re.compile(r'(?:PMID\s*[:=]?\s*(\d{7,8})'
                     r'|pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,8}))', re.I)

# The absolute families. Each maps the surface form used in the repo's prose to
# the stems that would have to appear in an abstract for the claim to be echoed.
ABSOLUTE_FAMILIES = {
    'eliminate': r'eliminat|abolish|obviat|remov\w+ (?:the )?(?:risk|need)',
    'abolish': r'abolish|eliminat',
    'prevent': r'prevent|prophylax|avert',
    'guarantee': r'guarantee|assur|ensur',
    'achieve': r'achiev|attain|reach\w*',
    'cure': r'cure|curativ|eradicat',
    'normalize': r'normalis|normaliz|restor\w+ to normal',
    'reverse': r'revers',
    'ensure': r'ensur|guarantee',
    'zero': r'\bzero\b|\bno (?:cases|events|episodes|rejection|deaths)\b|'
            r'\bnone\b|100\s?%|\bcomplete(?:ly)?\b|\ball (?:patients|subjects)\b',
}

# FINITE ASSERTING FORMS ONLY. The first version of this gate matched
# `prevent\w*` and fired on "prevention", "preventive", "preventable",
# "reversal", "reversible" -- 57 hits, almost none of them claims. A
# nominalisation names a topic ("diabetes prevention research"); a finite verb
# makes an assertion ("prevents blindness"). Only the second is falsifiable, and
# only the second is what put "eliminates hypoglycemia risk" on the site.
# Past-tense reporting of a trial result ("70% achieved insulin independence")
# is excluded for the same reason -- it is a measurement, usually with a number
# attached, not an absolute.
RE_ABSOLUTE = re.compile(
    r'\b(eliminates?|eliminating|abolish(?:es)?|abolishing|prevents?|preventing'
    r'|cures?|curing|eradicates?|eradicating|guarantees?|ensures?|ensuring'
    r'|normali[sz]es?|normali[sz]ing|reverses?|reversing|achieves?'
    r'|zero|100\s?%|completely|always|never fails?)\b', re.I)

# A hedged sentence is not an absolute claim. "Could prevent blindness in LMICs"
# and "making it ideal for preventive cell therapy" are proposals; the gate is
# for assertions. Failing hedges would push the prose toward vagueness, which is
# the opposite of what this repo wants.
RE_HEDGE = re.compile(
    r'\b(may|might|could|would|should|potential\w*|possibl\w*|likely|unlikely'
    r'|expected|anticipat\w*|projected|estimat\w*|hypothes\w*|propos\w*'
    r'|suggest\w*|appears?|seems?|if|whether|aims?|goal|target(?:ing)?'
    r'|scenario|model(?:led|ed|ling|ing)?|theoretical|in principle'
    r'|question|unclear|unknown)\b', re.I)

# "zero publications", "zero trial access", "myelin protein zero" are facts
# about the literature or a protein name, not claims about patients.
RE_ZERO_BIBLIOMETRIC = re.compile(
    r'\bzero\b[^.]{0,30}\b(publications?|trials?|studies|results?|literature|'
    r'papers?|access|data|citations?|records?)\b'
    r'|\bprotein zero\b', re.I)

# How close the endpoint has to sit to the verb to count as its object.
ENDPOINT_SPAN = 70

# Purpose and definition, not efficacy. "Drugs that weaken the immune system TO
# PREVENT organ rejection" says what a drug class is FOR; it does not claim the
# rejection never happens. Same for "the mechanism THAT PREVENTS rejection".
# These are the correct way to define a drug and the gate must not push them
# into hedged mush.
RE_PURPOSE = re.compile(
    r'\b(to|that|which|used to|in order to|designed to|intended to|aimed at|'
    r'for|helps?|works? to|acts? to)\s+$', re.I)

# Machine-readable blobs. A dict/JSON literal split on sentence punctuation
# produces "sentences" that span unrelated keys, so a verb in one field lands
# within ENDPOINT_SPAN of an endpoint in the next. Prose is checked; serialised
# data structures are left to the citation gates.
RE_BLOB = re.compile(r'["\']\s*:\s*[\[{"\']|["\']\s*,\s*["\']\w+["\']\s*:')

FAMILY_OF = [
    (re.compile(r'eliminat', re.I), 'eliminate'),
    (re.compile(r'abolish', re.I), 'abolish'),
    (re.compile(r'prevent', re.I), 'prevent'),
    (re.compile(r'guarantee', re.I), 'guarantee'),
    (re.compile(r'achiev', re.I), 'achieve'),
    (re.compile(r'cur(e|es|ed|ing)|eradicat', re.I), 'cure'),
    (re.compile(r'normali[sz]', re.I), 'normalize'),
    (re.compile(r'revers', re.I), 'reverse'),
    (re.compile(r'ensur', re.I), 'ensure'),
    (re.compile(r'zero|100\s?%|completely|always|never fails?', re.I), 'zero'),
]

# The claim only matters if it is attached to something that happens to a
# patient. "Eliminates the need for a second regex pass" is not a clinical
# claim.
RE_ENDPOINT = re.compile(
    r'hypoglyc[ae]mi|hyperglyc[ae]mi|mortalit|\bdeath|retinopath|nephropath|'
    r'neuropath|amputation|blindness|dialysis|rejection|graft loss|\bDKA\b|'
    r'ketoacidosis|beta.?cell (?:loss|death|destruction)|β.?cell (?:loss|death)|'
    r'insulin (?:dependence|independence|requirement)|exogenous insulin|'
    r'hba1c|glycaemic control|glycemic control|remission|complications|'
    r'cardiovascular (?:events?|death|outcomes?)|\bstroke\b|myocardial|'
    r'kidney failure|renal failure|end.stage|adverse events?|\bSAEs?\b|'
    r'type 1 diabetes|type 2 diabetes|\bT1D\b|\bT2D\b|\bLADA\b|autoimmunit',
    re.I)

# The honest negative. "did not prevent", "failed to eliminate", "does not cure"
# are accurate reporting of a null result and must not be pushed toward vaguer
# language by this gate.
RE_NEGATED = re.compile(
    r'\b(not|never|no|failed to|without|neither|nor|cannot|can\'t|does not|'
    r'did not|does nt|non-?)\s+(?:\w+\s+){0,2}$', re.I)

SENT_SPLIT = re.compile(r'(?<=[.!?])\s+|<br\s*/?>|\n')


def strip_html(text):
    return RE_WS.sub(' ', html.unescape(RE_TAG.sub(' ', text))).strip()


def load_abstract_cache():
    if os.path.exists(ABS_CACHE):
        try:
            with open(ABS_CACHE, encoding='utf-8') as fh:
                return json.load(fh)
        except ValueError:
            pass
    return {}


def fetch_abstracts(pmids, cache):
    missing = sorted({p for p in pmids if p not in cache})
    for i in range(0, len(missing), 100):
        batch = missing[i:i + 100]
        q = dict(TOOL, db='pubmed', rettype='abstract', retmode='text',
                 id=','.join(batch))
        try:
            text = _get(EFETCH + urllib.parse.urlencode(q))
        except Exception as exc:
            print('  [WARN] efetch failed: %s' % exc)
            continue
        # efetch text mode returns records separated by blank lines; the PMID
        # line anchors each one.
        blocks = re.split(r'\n\n(?=\d+\. )', text)
        by_pmid = {}
        for b in blocks:
            m = re.search(r'PMID:\s*(\d{7,8})', b)
            if m:
                by_pmid[m.group(1)] = b
        for p in batch:
            cache[p] = by_pmid.get(p, '')
        time.sleep(0.4)
    return {p: cache.get(p, '') for p in pmids}


def family_of(term):
    for rx, fam in FAMILY_OF:
        if rx.search(term):
            return fam
    return None


def find_claims(source, filename):
    claims, seen = [], set()
    flat = strip_html(source)
    for sent in SENT_SPLIT.split(flat):
        sent = sent.strip()
        if len(sent) < 25 or len(sent) > 600:
            continue
        if not RE_ENDPOINT.search(sent):
            continue
        if RE_HEDGE.search(sent):
            continue
        if len(RE_BLOB.findall(sent)) >= 2:
            continue
        for m in RE_ABSOLUTE.finditer(sent):
            before = sent[:m.start()]
            if RE_NEGATED.search(before):
                continue
            if RE_PURPOSE.search(before[-24:]):
                continue
            # Bare-verb list heading: "<strong>Prevent autoimmunity:</strong>
            # Suppress autoreactive T cells". A function label naming what a
            # cell type does is a definition, not an efficacy claim, and the
            # colon is what marks it as a label rather than a sentence.
            if ':' in sent[m.end():m.end() + 30]:
                continue
            # The endpoint must be the verb's object, not merely somewhere in
            # the same sentence. "Blocks T cell activation preventing rejection"
            # qualifies; "Driven by VEGF ... Affects 30% of T1D" does not.
            after = sent[m.end():m.end() + ENDPOINT_SPAN]
            if not RE_ENDPOINT.search(after):
                continue
            if RE_ZERO_BIBLIOMETRIC.search(sent):
                continue
            fam = family_of(m.group(1))
            if not fam:
                continue
            key = (filename, sent[:120], fam)
            if key in seen:
                continue
            seen.add(key)
            # Cited PMIDs: in the sentence, or just after it in the source.
            idx = source.find(sent[:60].split('<')[0][:40])
            window = sent
            if idx >= 0:
                window = strip_html(source[idx:idx + CITE_WINDOW])
            pmids = [a or b for a, b in RE_PMID.findall(window)]
            claims.append({'file': filename, 'sentence': sent[:400],
                           'term': m.group(1), 'family': fam,
                           'pmids': sorted(set(pmids))})
    return claims


def main():
    claims = []
    for name in sorted(os.listdir(SCRIPTS)):
        if not name.endswith('.py'):
            continue
        if not (name.startswith('build_') or name.startswith('rebuild_')):
            continue
        with open(os.path.join(SCRIPTS, name), encoding='utf-8',
                  errors='replace') as fh:
            claims.extend(find_claims(fh.read(), name))

    print('Absolute claims attached to a clinical endpoint: %d' % len(claims))
    if not claims:
        print('[OK] none found')
        return 0

    cache = load_abstract_cache()
    wanted = sorted({p for c in claims for p in c['pmids']})
    print('Fetching %d abstracts...' % len(wanted))
    abstracts = fetch_abstracts(wanted, cache)
    with open(ABS_CACHE, 'w', encoding='utf-8') as fh:
        json.dump(cache, fh, ensure_ascii=False)

    unsourced, overstated, supported, no_abstract = [], [], [], []
    for c in claims:
        if not c['pmids']:
            c['verdict'] = 'UNSOURCED_ABSOLUTE'
            unsourced.append(c)
            continue
        echo = re.compile(ABSOLUTE_FAMILIES[c['family']], re.I)
        hits, empty = [], []
        for p in c['pmids']:
            body = abstracts.get(p) or ''
            if not body.strip():
                empty.append(p)
                continue
            m = echo.search(body)
            if m:
                hits.append({'pmid': p, 'matched': m.group(0)})
        if hits:
            c['verdict'] = 'SUPPORTED'
            c['echoed_by'] = hits
            supported.append(c)
        elif empty and len(empty) == len(c['pmids']):
            c['verdict'] = 'NO_ABSTRACT'
            c['pmids_without_abstract'] = empty
            no_abstract.append(c)
        else:
            c['verdict'] = 'OVERSTATED'
            overstated.append(c)

    print()
    print('=' * 74)
    print('UNSOURCED_ABSOLUTE %d   OVERSTATED %d   NO_ABSTRACT %d   SUPPORTED %d'
          % (len(unsourced), len(overstated), len(no_abstract), len(supported)))
    print()
    if overstated:
        print('--- OVERSTATED: cited abstract contains no matching absolute ---')
        for c in overstated:
            print('  %s  [%s -> %s]  PMIDs %s'
                  % (c['file'], c['term'], c['family'], ','.join(c['pmids'])))
            print('     %s' % c['sentence'][:180])
    if unsourced:
        print('\n--- UNSOURCED_ABSOLUTE: absolute claim, no PMID within %d '
              'chars ---' % CITE_WINDOW)
        for c in unsourced:
            print('  %s  [%s]' % (c['file'], c['term']))
            print('     %s' % c['sentence'][:180])
    if no_abstract:
        print('\n--- NO_ABSTRACT (reported, not failed; needs a human read) ---')
        for c in no_abstract:
            print('  %s  [%s]  PMIDs %s' % (c['file'], c['term'],
                                            ','.join(c['pmids'])))

    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump({'generated': time.strftime('%Y-%m-%d'),
                   'rule': 'absolute verb + clinical endpoint => must cite a '
                           'PMID whose abstract contains a same-family absolute',
                   'cite_window_chars': CITE_WINDOW,
                   # Recall is deliberately traded for precision, and the trade
                   # is recorded so the next reader can judge it rather than
                   # inherit it. Each filter was added only after inspecting
                   # what it removed.
                   'calibration_2026_08_26': {
                       'raw_vocabulary_grep': 65,
                       'after_finite_verb_forms_only': 9,
                       'after_hedge_and_blob_and_purpose_filters': 4,
                       'after_label_form_filter': 1,
                       'note': 'The 64 removed were nominalisations '
                               '("prevention", "reversible"), hedged proposals '
                               '("could prevent"), bibliometric zeros ("zero '
                               'publications"), serialised dict blobs, '
                               'infinitives of purpose ("drugs used to prevent '
                               'rejection") and list-item labels ("Prevent '
                               'autoimmunity:"). NONE was an absolute clinical '
                               'claim. But a filter tuned on 65 examples can '
                               'over-fit: this gate now finds ONE claim '
                               'repo-wide, which is a suspiciously clean '
                               'result and should be widened deliberately, '
                               'measuring what each relaxation admits.'},
                   'claims_found': len(claims),
                   'unsourced_absolute': unsourced,
                   'overstated': overstated,
                   'no_abstract': no_abstract,
                   'supported': supported},
                  fh, indent=1, ensure_ascii=False)
    fails = len(unsourced) + len(overstated)
    print('\nReport: %s' % REPORT)
    print('[OK]' if not fails else '[FAIL] %d absolute claim(s) unsupported'
          % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
