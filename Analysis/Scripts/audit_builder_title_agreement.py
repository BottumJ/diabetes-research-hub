#!/usr/bin/env python3
"""Does the title a builder ASSERTS for a PMID match the title PubMed returns?

WHY THIS EXISTS
---------------
Every citation gate in this repo so far asks a weak question: is this PMID real
(validate_citations.py), or is its subject matter roughly on-topic
(audit_path_citations.py, audit_citation_identifiers.py,
audit_published_citation_stores.py). None of them asks the strong question,
even where the data to ask it is sitting right there.

The ~50 build_*.py dashboard builders hardcode citation records that carry BOTH
a pmid AND the title/authors/year/journal the builder claims for it. That is a
checkable assertion. On 2026-08-24 the topic screen caught 5 builder literals
whose real titles are off-topic; among them:

  19148081  asserted "Edmonton Protocol: allogeneic islet transplantation..."
            [NEJM 2006, Shapiro, evidence_tier GOLD]
            actual   "Your inbox, Mr President."  [a Nature editorial]

The topic screen only caught it because the true title happened to contain no
diabetes vocabulary. A wrong PMID that lands on ANY diabetes paper passes every
gate in the repo while the dashboard shows a fabricated author, year, journal
and evidence tier. The topic screen is not the control here -- title agreement
is.

WHAT IT DOES
------------
Parses build_*.py / rebuild_*.py for dict literals containing a PMID key and a
title key. For each, resolves the PMID against PubMed and scores title
agreement by content-word overlap.

  MATCH      >= MATCH_THRESHOLD overlap of asserted content words
  WEAK       >= WEAK_THRESHOLD  -- likely a paraphrase or truncation, review
  MISMATCH   below that -- the builder is asserting a different paper

Year is checked independently: an asserted year more than YEAR_SLACK from the
PubMed year is reported even when titles agree, because a right-title/wrong-year
record usually means the wrong edition or a duplicate record was cited.

Exit 1 on any MISMATCH.
Output: Analysis/Results/builder_title_agreement.json
"""

import ast
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_citation_identifiers import (  # noqa: E402
    load_cache, save_cache, resolve_titles,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
SCRIPTS = os.path.join(BASE, 'Scripts')
REPORT = os.path.join(RESULTS, 'builder_title_agreement.json')

MATCH_THRESHOLD = 0.55
WEAK_THRESHOLD = 0.30
YEAR_SLACK = 1

PMID_KEYS = ('pmid', 'PMID', 'pmid_ref')
TITLE_KEYS = ('title', 'paper_title', 'citation_title')
YEAR_KEYS = ('year', 'pub_year')

# Words that carry no discriminating power in a biomedical title.
STOPWORDS = {
    'a', 'an', 'and', 'the', 'of', 'in', 'on', 'for', 'to', 'with', 'by',
    'from', 'via', 'is', 'are', 'as', 'at', 'or', 'its', 'their', 'study',
    'trial', 'analysis', 'effects', 'effect', 'role', 'new', 'novel',
    'using', 'after', 'during', 'among', 'between', 'versus', 'vs',
}

WORD = re.compile(r"[a-z0-9]+")


def content_words(text):
    return {w for w in WORD.findall((text or '').lower())
            if len(w) > 2 and w not in STOPWORDS}


def overlap(asserted, actual):
    """Fraction of the ASSERTED title's content words present in the actual.

    Directional on purpose. PubMed titles are often longer than the shorthand a
    builder stores, so symmetric similarity would penalise honest abbreviation.
    What matters is whether everything the builder claims is actually there.
    """
    a = content_words(asserted)
    b = content_words(actual)
    if not a:
        return 0.0
    return len(a & b) / len(a)


def extract_citation_dicts(source, filename):
    """Every dict literal in the file that has a PMID key and a title key."""
    out = []
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as exc:
        print('  [WARN] could not parse %s: %s' % (filename, exc))
        return out
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        rec = {}
        for k, v in zip(node.keys, node.values):
            if isinstance(k, ast.Constant) and isinstance(k.value, str) \
                    and isinstance(v, ast.Constant):
                rec[k.value] = v.value
        pmid = next((str(rec[k]) for k in PMID_KEYS if rec.get(k)), None)
        title = next((rec[k] for k in TITLE_KEYS if rec.get(k)), None)
        if not pmid or not title:
            continue
        pmid = re.sub(r'\D', '', pmid)
        if not re.fullmatch(r'\d{7,8}', pmid):
            continue
        out.append({
            'file': filename,
            'line': node.lineno,
            'pmid': pmid,
            'asserted_title': title,
            'asserted_year': next((rec[k] for k in YEAR_KEYS if rec.get(k)), None),
            'asserted_journal': rec.get('journal'),
            'asserted_authors': rec.get('authors'),
            'evidence_tier': rec.get('evidence_tier') or rec.get('evidence_level'),
        })
    return out


def main():
    claims = []
    for name in sorted(os.listdir(SCRIPTS)):
        if not name.endswith('.py'):
            continue
        if not (name.startswith('build_') or name.startswith('rebuild_')):
            continue
        with open(os.path.join(SCRIPTS, name), encoding='utf-8',
                  errors='replace') as fh:
            claims.extend(extract_citation_dicts(fh.read(), name))

    print('Builder citation records carrying BOTH a pmid and a title: %d'
          % len(claims))
    if not claims:
        print('[OK] nothing to check')
        return 0

    cache = load_cache()
    titles = resolve_titles(sorted({c['pmid'] for c in claims}), cache)
    save_cache(cache)

    mismatch, weak, year_off, unresolved = [], [], [], []
    for c in claims:
        meta = titles.get(c['pmid'])
        if not meta:
            c['verdict'] = 'UNRESOLVED'
            unresolved.append(c)
            continue
        c['actual_title'] = meta['title']
        c['actual_journal'] = meta['journal']
        c['actual_year'] = meta['year']
        c['overlap'] = round(overlap(c['asserted_title'], meta['title']), 3)
        if c['overlap'] >= MATCH_THRESHOLD:
            c['verdict'] = 'MATCH'
        elif c['overlap'] >= WEAK_THRESHOLD:
            c['verdict'] = 'WEAK'
            weak.append(c)
        else:
            c['verdict'] = 'MISMATCH'
            mismatch.append(c)
        try:
            if c['asserted_year'] and meta['year'] and \
                    abs(int(c['asserted_year']) - int(meta['year'])) > YEAR_SLACK:
                year_off.append(c)
        except (TypeError, ValueError):
            pass

    print()
    print('=' * 74)
    print('MISMATCH  %d   WEAK %d   YEAR_DISAGREE %d   UNRESOLVED %d   MATCH %d'
          % (len(mismatch), len(weak), len(year_off), len(unresolved),
             len(claims) - len(mismatch) - len(weak) - len(unresolved)))
    print()
    if mismatch:
        print('--- MISMATCH: the builder is describing a different paper ---')
        for c in mismatch:
            print('  %s:%d  PMID %s   overlap %.2f  tier=%s'
                  % (c['file'], c['line'], c['pmid'], c['overlap'],
                     c['evidence_tier']))
            print('     ASSERTED %s (%s, %s)'
                  % (c['asserted_title'][:72], c['asserted_authors'],
                     c['asserted_year']))
            print('     ACTUAL   %s (%s, %s)'
                  % (c['actual_title'][:72], c['actual_journal'],
                     c['actual_year']))
    if weak:
        print('\n--- WEAK: paraphrase or wrong paper, needs a human read ---')
        for c in weak:
            print('  %s:%d  PMID %s  overlap %.2f' % (c['file'], c['line'],
                                                      c['pmid'], c['overlap']))
            print('     ASSERTED %s' % c['asserted_title'][:72])
            print('     ACTUAL   %s' % c['actual_title'][:72])
    if year_off:
        print('\n--- YEAR DISAGREES BY > %d ---' % YEAR_SLACK)
        for c in year_off:
            print('  %s:%d  PMID %s  asserted %s vs actual %s  [%s]'
                  % (c['file'], c['line'], c['pmid'], c['asserted_year'],
                     c['actual_year'], c['verdict']))
    if unresolved:
        print('\n--- UNRESOLVED (not in PubMed) ---')
        for c in unresolved:
            print('  %s:%d  PMID %s  %s'
                  % (c['file'], c['line'], c['pmid'],
                     c['asserted_title'][:60]))

    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump({'generated': time.strftime('%Y-%m-%d'),
                   'thresholds': {'match': MATCH_THRESHOLD,
                                  'weak': WEAK_THRESHOLD,
                                  'year_slack': YEAR_SLACK},
                   'claims_checked': len(claims),
                   'mismatch': mismatch,
                   'weak': weak,
                   'year_disagree': [c['pmid'] for c in year_off],
                   'unresolved': unresolved,
                   'all': claims},
                  fh, indent=1, ensure_ascii=False)
    print('\nReport: %s' % REPORT)
    print('[OK]' if not mismatch else '[FAIL] %d mismatched citation(s)'
          % len(mismatch))
    return 1 if mismatch else 0


if __name__ == '__main__':
    sys.exit(main())
