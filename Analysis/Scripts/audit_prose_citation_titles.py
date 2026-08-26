#!/usr/bin/env python3
"""Does the PROSE a builder writes beside a PMID describe the paper PubMed returns?

WHY THIS EXISTS
---------------
audit_builder_title_agreement.py (2026-08-24) asks the strong question -- does
the asserted title match the real one -- but it can only see dict literals that
carry both a `pmid` key and a `title` key. Repo-wide that is 11 records, and 9
of them were wrong.

The 10th miscitation found on 2026-08-24 was invisible to it:

  22723585  asserted "Bi et al. Omega-3 fatty acids and diabetes"
            actual   "Effect of fructose on glycemic control in diabetes:
                      a systematic review and meta-analysis of controlled
                      feeding trials."  [Diabetes Care 2012]

It was invisible because it lived in an HTML template string, not a dict. Most
citations in this repo are written that way.

WHAT THIS GATE LEARNED ON ITS FIRST RUN (2026-08-26)
-----------------------------------------------------
A naive title-overlap test over prose reported 249 mismatches, and almost all of
them were the gate's fault, not the repo's. The dominant citation shape here is

    Source: Hernandez et al. JAMA Oncol 2018 (PMID:29710129)

which asserts an AUTHOR, a JOURNAL and a YEAR and no title at all. Scoring that
against the real title ("Total Costs of Chimeric Antigen Receptor T-Cell
Immunotherapy") returns 0.00 for a citation that is completely correct. A gate
that cries wolf 249 times is worse than no gate, because the next reader learns
to skip its output -- which is exactly the failure mode recorded in the
2026-08-25 queue item about the credibility sweep clearing its own findings.

So the reference is CLASSIFIED before it is scored, and each class gets the test
that can actually falsify it:

  TITLE_ASSERTED   After removing the tokens that PubMed itself accounts for
                   (first-author surname, journal words, the year, bare
                   initials, digits), >= MIN_TITLE_WORDS content words remain.
                   Those residual words are a title claim. Scored by directional
                   content-word overlap against the real title, using the same
                   thresholds as audit_builder_title_agreement.py so a number
                   from one gate means the same thing in the other.

  METADATA_ONLY    Nothing is left after that subtraction: the prose claims
                   author/journal/year and stops. Title overlap is undefined
                   here. Checked instead on the three things it does assert --
                   first-author surname present, journal recognisable, year
                   within YEAR_SLACK.

  DESCRIPTIVE      No citation marker at all -- a sentence about the science
                   with a PMID hung off it ("Zinc is a cofactor for insulin
                   crystallisation [PMID:25287711]"). That is a support claim,
                   not an identity claim, and neither test applies. COUNTED and
                   REPORTED, never failed. The topic screens
                   (audit_path_citations.py, audit_published_citation_stores.py)
                   are the control for this class.

Exit 1 on any MISMATCH.
Output: Analysis/Results/prose_citation_titles.json

LIMITS, STATED
--------------
- DESCRIPTIVE references are UNCHECKED by this gate, not verified by it.
  Coverage is printed as a fraction so it cannot be read as completeness.
- METADATA_ONLY is a weaker test than TITLE_ASSERTED. A wrong PMID that happens
  to land on a paper by the same author in the same journal and year passes it.
  Counts for the two classes are reported separately for that reason.
- The lookback is 300 characters and records are cut at citation separators, so
  a citation whose title sits further back than that is missed.
"""

import html
import json
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_citation_identifiers import (  # noqa: E402
    load_cache, save_cache, resolve_titles, _get, ESUMMARY, TOOL,
)
from audit_builder_title_agreement import (  # noqa: E402
    content_words, overlap, MATCH_THRESHOLD, WEAK_THRESHOLD, STOPWORDS,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
SCRIPTS = os.path.join(BASE, 'Scripts')
REPORT = os.path.join(RESULTS, 'prose_citation_titles.json')
AUTHOR_CACHE = os.path.join(RESULTS, '.prose_author_cache.json')

LOOKBACK = 300
MIN_TITLE_WORDS = 4
YEAR_SLACK = 1
# A journal-year tail sits at the very end of the record, immediately before
# the PMID: "... Diabetes 2005;54(6):1726-1731 (PMID:x)". 70 characters was too
# generous -- it let a year anywhere in a sentence of market prose ("Approved:
# China, September 2022 ... $2,000-$3,000/year") certify that sentence as a
# bibliographic record, which produced 20 false mismatches in build_gka_pricing.
TAIL = 28

RE_REF = re.compile(
    r'(?:PMID\s*[:=]?\s*(\d{7,8})'
    r'|pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,8}))', re.I)

RE_TAG = re.compile(r'<[^>]{0,400}?>')
RE_WS = re.compile(r'\s+')
RE_ET_AL = re.compile(r'\bet\s+al\b', re.I)
RE_AUTHOR_INITIALS = re.compile(r'\b[A-Z][a-z]{2,}\s+[A-Z]{1,3}\b')
RE_YEAR = re.compile(r'\b(19[5-9]\d|20[0-4]\d)\b')
RE_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9'\-]*")

RE_JOURNAL = re.compile(
    r'\b(NEJM|N Engl J Med|Lancet|JAMA|BMJ|Diabetes Care|Diabetologia|'
    r'Diabetes Obes Metab|J Clin Invest|JCI|Nature|Science|Cell Metab|Cell|'
    r'Front Endocrinol|Front Immunol|World J Diabetes|Endocr Rev|Immunity|'
    r'Am J Transplant|Transplantation|Kidney Int|Circulation|Endocrine Reviews|'
    r'Ann Intern Med|PLoS|Sci Rep|Metabolism|PNAS|Diabetes\b)', re.I)

# Where one citation record ends and the next begins. `;\s+(?=[A-Z])` on
# purpose: a bare `;` also appears inside volume/issue strings such as
# "Diabetes 2005;54(6):1726-1731", and splitting there would throw the title
# away and silently reclassify a real assertion as METADATA_ONLY.
RE_SEPARATOR = re.compile(
    r';\s+(?=[A-Z])|\bSources?\s*:\s*|\bRefs?\s*:\s*|\bReferences?\s*:\s*|\|'
    # JSON / dict key boundaries. Builders store citations as
    # {"evidence": "<long prose>", "cost_source": "Hernandez 2018 (PMID:x)"};
    # without this cut the *previous* value's prose is scored as if it were the
    # asserted title, which is what produced 20 identical false mismatches on
    # build_drug_repurposing_screen.py in the first run of this gate.
    r'|[,{]\s*["\'][A-Za-z_]+["\']\s*:\s*["\']'
    # JSON list-item boundary: ["Diabetes Care 2023", "PMID:40544428 ..."].
    # Each element is its own reference; without this cut the PMID in one
    # element is scored against the text of the element before it.
    r'|["\']\s*,\s*["\']'
    r'|\[\s*["\']')

# The author block: "et al", or "Surname AB" initials, optionally a comma-run of
# them ("Sandoval DA, D'Alessio DA."). Everything BEFORE the last author block
# is prose leading up to the citation -- a section heading, a sentence, a dict
# key -- and is not part of the record. Cutting there is what separates a real
# title claim from the surrounding page furniture; without it, headings like
# "CAR-T Cost & Health Economics:" get scored as if they were titles and every
# correct author/journal/year citation is reported as a mismatch.
RE_AUTHOR_BLOCK = re.compile(
    # Full surname+initials run, absorbing a trailing "et al" so that
    # "Brissova M et al." is ONE block and the title starts after it.
    r"(?:\b[A-Z][A-Za-z'’\-]{2,}\s+[A-Z]{1,3}\b\.?"
    r"(?:\s*,\s*[A-Z][A-Za-z'’\-]{2,}\s+[A-Z]{1,3}\b\.?)*"
    r"(?:\s+et\s+al\b\.?)?"
    # Bare "et al" where the surname carries no initials ("Feutren et al,").
    r"|\bet\s+al\b\.?"
    # Author-year shorthand: "Pricing data from Hernandez 2018 (PMID:29710129)".
    r"|\b[A-Z][A-Za-z'’\-]{2,}\s+(?:19|20)\d\d\b)")

# A citation that BEGINS with its authors is a bibliographic record and its
# title follows the first author block. A citation embedded at the end of a
# sentence ("Combination costs from Hernandez 2018") has its author block last.
# Taking the last match unconditionally broke the first case, because the
# author-year alternative also matches the journal-year tail
# ("... & Metabolism 2023;34(12)") and swallowed the title.
AUTHOR_HEAD_WINDOW = 40

# Journal abbreviations whose letters share nothing with the indexed full name,
# so prefix matching alone would report a correct journal as unrecognised.
JOURNAL_ALIASES = {
    'nejm': 'new england journal of medicine',
    'jci': 'journal of clinical investigation',
    'pnas': 'proceedings of the national academy of sciences',
    'bmj': 'bmj',
    'jama': 'jama',
    'jcem': 'journal of clinical endocrinology',
    'dcct': 'new england journal of medicine',
    'ukpds': 'lancet',
}

BOILERPLATE = re.compile(
    r'^(source|sources|ref|refs|reference|references|evidence|citation|'
    r'see|note|notes|tier|gold|silver|bronze|pmid|and|et al)s?$', re.I)


def strip_html(text):
    return RE_WS.sub(' ', html.unescape(RE_TAG.sub(' ', text))).strip()


def load_author_cache():
    if os.path.exists(AUTHOR_CACHE):
        try:
            with open(AUTHOR_CACHE, encoding='utf-8') as fh:
                return json.load(fh)
        except ValueError:
            pass
    return {}


def resolve_first_authors(pmids, cache):
    """First-author surname per PMID. Separate cache so the shared citation
    cache written by audit_citation_identifiers.py keeps its existing shape."""
    missing = sorted({p for p in pmids if p not in cache})
    for i in range(0, len(missing), 150):
        batch = missing[i:i + 150]
        q = dict(TOOL, db='pubmed', retmode='json', id=','.join(batch))
        try:
            data = json.loads(_get(ESUMMARY + urllib.parse.urlencode(q)))
        except Exception as exc:
            print('  [WARN] esummary (authors) failed: %s' % exc)
            continue
        res = data.get('result', {})
        for p in batch:
            rec = res.get(p)
            surname = ''
            if isinstance(rec, dict):
                sfa = rec.get('sortfirstauthor') or ''
                if not sfa:
                    auths = rec.get('authors') or []
                    if auths and isinstance(auths[0], dict):
                        sfa = auths[0].get('name', '')
                surname = (sfa.split() or [''])[0].lower().strip(',')
            cache[p] = surname
        time.sleep(0.4)
    return {p: cache.get(p, '') for p in pmids}


def journal_terms(journal):
    """Discriminating words of an indexed journal name."""
    return [w for w in re.findall(r'[a-z]+', (journal or '').lower())
            if len(w) >= 4 and w not in
            ('journal', 'official', 'american', 'society', 'england', 'london',
             'research', 'international', 'clinical', 'reports')]


def journal_recognised(tokens_lower, journal):
    """Any discriminating journal word present, prefix-matched for
    abbreviation ('Oncol' -> 'oncology', 'Transplant' -> 'transplantation')."""
    terms = journal_terms(journal)
    jl = (journal or '').lower()
    for t in tokens_lower:
        if len(t) < 3:
            continue
        if JOURNAL_ALIASES.get(t) and JOURNAL_ALIASES[t] in jl:
            return True
        if any(term.startswith(t) or t.startswith(term) for term in terms):
            return True
    return not terms  # nothing discriminating to match against


def isolate_record(window):
    """The last citation record in the window -- the one the PMID belongs to."""
    parts = RE_SEPARATOR.split(window)
    chunk = parts[-1] if parts else window
    return chunk.strip(' .,:;|-–—([')


def after_author_block(chunk):
    """The citation body: everything after the LAST author block.

    Returns (body, found). When no author block is present the whole chunk is
    returned with found=False, so a journal/year-only record is still checked
    rather than silently dropped.
    """
    matches = list(RE_AUTHOR_BLOCK.finditer(chunk))
    if not matches:
        return chunk, False
    pick = matches[0] if matches[0].start() <= AUTHOR_HEAD_WINDOW else matches[-1]
    return chunk[pick.end():].strip(' .,:;|-–—'), True


def residual_title_words(chunk, meta, surname):
    """What the prose claims that PubMed's author/journal/year do not explain."""
    jterms = journal_terms(meta.get('journal'))
    jl = (meta.get('journal') or '').lower()
    keep = []
    for tok in RE_TOKEN.findall(chunk):
        t = tok.lower()
        if len(t) < 3 or t in STOPWORDS or t in ('et', 'al'):
            continue
        if BOILERPLATE.match(t):
            continue
        if surname and t == surname:
            continue
        if JOURNAL_ALIASES.get(t) and JOURNAL_ALIASES[t] in jl:
            continue
        if any(term.startswith(t) or t.startswith(term) for term in jterms):
            continue
        keep.append(tok)
    return keep


def harvest(source, filename):
    refs, seen = [], set()
    for m in RE_REF.finditer(source):
        pmid = m.group(1) or m.group(2)
        window = strip_html(source[max(0, m.start() - LOOKBACK):m.start()])
        chunk = isolate_record(window)
        # A bibliographic record ENDS in journal + year, immediately before the
        # PMID. Requiring a year in the last TAIL characters is the tightest
        # available definition of "this prose is asserting a record" and it is
        # what separates
        #     "... composition. Diabetes 2005;54(6):1726-1731 (PMID:x)"   record
        # from
        #     "... Widely studied in gestational diabetes [PMID:x]"       prose
        # Both contain a citation marker somewhere; only the first is a claim
        # about what the paper IS. Citations that omit the year fall to
        # DESCRIPTIVE and go unchecked -- that cost is paid in the coverage
        # figure rather than in false alarms.
        tail = chunk[-TAIL:]
        if RE_REF.search(chunk):
            # Another PMID is already inside this record. That happens in lists
            # written as "PMID:32847960 (Buzzetti 2020): consensus criteria -
            # PMID:24598244 (Krause 2014): GAD affinity", where the descriptor
            # FOLLOWS its PMID instead of preceding it. The prose in the
            # lookback then belongs to the previous entry, so attributing it to
            # this PMID would be guessing. Declared unattributable rather than
            # scored -- a gate must not invent the claim it then fails.
            marker = ''
        elif not RE_YEAR.search(tail):
            marker = ''
        elif RE_ET_AL.search(chunk):
            marker = 'et_al'
        elif RE_JOURNAL.search(chunk):
            marker = 'journal_year'
        elif RE_AUTHOR_INITIALS.search(chunk):
            marker = 'author_initials_year'
        else:
            marker = 'year_tail'
        key = (filename, pmid, chunk[-140:])
        if key in seen:
            continue
        seen.add(key)
        refs.append({
            'file': filename,
            'line': source.count('\n', 0, m.start()) + 1,
            'pmid': pmid,
            'record': chunk[-240:],
            'marker': marker,
            'kind': 'CITATION' if marker else 'DESCRIPTIVE',
        })
    return refs


def main():
    refs = []
    for name in sorted(os.listdir(SCRIPTS)):
        if not name.endswith('.py'):
            continue
        if not (name.startswith('build_') or name.startswith('rebuild_')):
            continue
        with open(os.path.join(SCRIPTS, name), encoding='utf-8',
                  errors='replace') as fh:
            refs.extend(harvest(fh.read(), name))

    cited = [r for r in refs if r['kind'] == 'CITATION']
    descriptive = [r for r in refs if r['kind'] == 'DESCRIPTIVE']
    print('PMID references in builder prose: %d' % len(refs))
    print('  identity asserted (checked):     %d' % len(cited))
    print('  descriptive support (unchecked): %d' % len(descriptive))
    if not cited:
        print('[OK] no identity assertions to check')
        return 0

    cache = load_cache()
    pmids = sorted({r['pmid'] for r in cited})
    titles = resolve_titles(pmids, cache)
    save_cache(cache)
    acache = load_author_cache()
    authors = resolve_first_authors(pmids, acache)
    with open(AUTHOR_CACHE, 'w', encoding='utf-8') as fh:
        json.dump(acache, fh, indent=1, ensure_ascii=False)

    mismatch, weak, unresolved, journal_off = [], [], [], []
    n_title, n_meta = 0, 0
    for r in cited:
        meta = titles.get(r['pmid'])
        if not meta:
            r['verdict'] = 'UNRESOLVED'
            unresolved.append(r)
            continue
        surname = authors.get(r['pmid'], '')
        r['actual_title'] = meta['title']
        r['actual_journal'] = meta['journal']
        r['actual_year'] = meta['year']
        r['actual_first_author'] = surname

        body, had_author = after_author_block(r['record'])
        r['citation_body'] = body
        residual = residual_title_words(body, meta, surname)
        tokens_lower = [t.lower() for t in RE_TOKEN.findall(r['record'])]

        # Journal and year are asserted by every class and are checked for
        # every class. They do not fail the build on their own -- a right paper
        # under a wrong journal name is a labelling error, not a miscitation --
        # but they are reported, because that is how PMID 30949058 was found
        # sitting under "Frontiers in Diabetes" when it is in Front Physiol.
        r['journal_ok'] = journal_recognised(tokens_lower, meta['journal'])
        years = [int(y) for y in RE_YEAR.findall(r['record'])]
        try:
            r['year_ok'] = any(
                abs(y - int(meta['year'])) <= YEAR_SLACK for y in years)
        except (TypeError, ValueError):
            r['year_ok'] = False
        r['author_ok'] = bool(surname) and surname in tokens_lower

        if len(content_words(' '.join(residual))) >= MIN_TITLE_WORDS:
            r['claim_class'] = 'TITLE_ASSERTED'
            n_title += 1
            r['asserted_title_residual'] = ' '.join(residual)
            r['overlap'] = round(overlap(' '.join(residual), meta['title']), 3)
            if r['overlap'] >= MATCH_THRESHOLD:
                r['verdict'] = 'MATCH'
            elif r['overlap'] >= WEAK_THRESHOLD:
                r['verdict'] = 'WEAK'
                weak.append(r)
            elif r['author_ok'] and r['journal_ok'] and r['year_ok']:
                # Three independent identifiers agree. A wrong PMID that lands
                # on the same author in the same journal in the same year is
                # not a plausible accident; a shortened title is. Hardie's AMPK
                # review is the type case: the builder writes "AMPK: a nutrient
                # and energy sensor", PubMed says "AMP-activated protein
                # kinase: maintaining energy homeostasis at the cellular and
                # whole-body levels", Annu Rev Nutr 2014, Hardie. Same paper.
                r['verdict'] = 'WEAK'
                r['downgraded'] = 'title paraphrase; author+journal+year agree'
                weak.append(r)
            else:
                r['verdict'] = 'MISMATCH'
                mismatch.append(r)
        else:
            r['claim_class'] = 'METADATA_ONLY'
            n_meta += 1
            if r['author_ok'] and (r['journal_ok'] or r['year_ok']):
                r['verdict'] = 'MATCH'
            elif not r['author_ok'] and not r['journal_ok']:
                r['verdict'] = 'MISMATCH'
                mismatch.append(r)
            else:
                r['verdict'] = 'WEAK'
                weak.append(r)

        if r['verdict'] in ('MATCH', 'WEAK') and not r['journal_ok']:
            journal_off.append(r)

    matched = len(cited) - len(mismatch) - len(weak) - len(unresolved)
    print()
    print('=' * 74)
    print('claim classes:  TITLE_ASSERTED %d   METADATA_ONLY %d' %
          (n_title, n_meta))
    print('MISMATCH %d   WEAK %d   UNRESOLVED %d   MATCH %d'
          % (len(mismatch), len(weak), len(unresolved), matched))
    print()
    if mismatch:
        print('--- MISMATCH: the prose names a different paper ---')
        for r in mismatch:
            print('  %s:%d  PMID %s  [%s]' % (r['file'], r['line'], r['pmid'],
                                              r['claim_class']))
            print('     PROSE  %s' % r['record'][-160:])
            print('     ACTUAL %s | %s %s | first author %s'
                  % (r['actual_title'][:90], r['actual_journal'][:40],
                     r['actual_year'], r['actual_first_author'] or '?'))
    if weak:
        print('\n--- WEAK: paraphrase, truncation or wrong paper ---')
        for r in weak:
            print('  %s:%d  PMID %s  [%s] %s'
                  % (r['file'], r['line'], r['pmid'], r['claim_class'],
                     ('overlap %.2f' % r['overlap']) if 'overlap' in r
                     else 'author=%s journal=%s year=%s'
                     % (r.get('author_ok'), r.get('journal_ok'),
                        r.get('year_ok'))))
            print('     PROSE  %s' % r['record'][-140:])
            print('     ACTUAL %s' % r['actual_title'][:120])
    if journal_off:
        print('\n--- JOURNAL NOT RECOGNISED (title agrees; reported, not '
              'failed) ---')
        for r in journal_off:
            print('  %s:%d  PMID %s  asserted-in: %s'
                  % (r['file'], r['line'], r['pmid'], r['record'][-70:]))
            print('     ACTUAL journal %s' % r['actual_journal'])
    if unresolved:
        print('\n--- UNRESOLVED (not in PubMed) ---')
        for r in unresolved:
            print('  %s:%d  PMID %s' % (r['file'], r['line'], r['pmid']))

    coverage = round(len(cited) / len(refs), 3) if refs else 0.0
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump({'generated': time.strftime('%Y-%m-%d'),
                   'lookback_chars': LOOKBACK,
                   'thresholds': {'match': MATCH_THRESHOLD,
                                  'weak': WEAK_THRESHOLD,
                                  'min_title_words': MIN_TITLE_WORDS,
                                  'year_slack': YEAR_SLACK},
                   'refs_total': len(refs),
                   'identity_assertions_checked': len(cited),
                   'title_asserted': n_title,
                   'metadata_only': n_meta,
                   'descriptive_unchecked': len(descriptive),
                   'coverage_fraction_of_refs_checked': coverage,
                   'mismatch': mismatch,
                   'weak': weak,
                   'journal_not_recognised': journal_off,
                   'unresolved': unresolved,
                   'descriptive_sample': descriptive[:40],
                   'all_checked': cited},
                  fh, indent=1, ensure_ascii=False)
    print('\nReport: %s' % REPORT)
    print('Coverage: %.1f%% of builder PMID references assert an identity and '
          'were checked; the rest are descriptive and are NOT verified here.'
          % (coverage * 100))
    print('[OK]' if not mismatch else '[FAIL] %d mismatched prose citation(s)'
          % len(mismatch))
    return 1 if mismatch else 0


if __name__ == '__main__':
    sys.exit(main())
