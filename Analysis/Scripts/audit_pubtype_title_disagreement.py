#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The evidence-design grader's ONLY input is silently incomplete.

THE FINDING (2026-08-29)
------------------------
audit_path_evidence_design.py grades every research path by PubMed publication
type, and its own docstring gives the reason: pubtype "comes from PubMed rather
than from this repo's own regexes, and it is the one field a builder cannot
accidentally invent."

That is true and it is not enough. A builder cannot invent the field, but
PubMed can leave it OFF, and the grader reads absence as "design unknown"
(PRIMARY_OTHER). Vetting the 16 PRIMARY_OTHER papers on 2026-08-29 found the
omission running in BOTH directions inside one 16-paper batch:

  PMID 36643381  Biomed Hub 2022. Title ends "... Protocol for a Randomized,
                 Double-Blind, Placebo-Controlled, Phase 2, Dose-Finding
                 Study". PubMed pubtype: ['Journal Article'] only. No
                 'Clinical Trial Protocol' tag. It reports NO results, and it
                 supplies 7 live extractions to the corpus. The repo raised a
                 P1 item about protocol papers ranking as evidence and then
                 could not see the second protocol it already had.

  PMID 36826844  JAMA 2023. Title ends "... A Randomized Clinical Trial".
                 PubMed pubtype: ['Journal Article', 'Research Support,
                 Non-U.S. Gov't']. No 'Randomized Controlled Trial' tag. This
                 is CLVer, n=88 (47 verapamil / 41 placebo), and it MEASURED
                 the outcome the repo's two NO_RESULTS verapamil paths are
                 about. It supplies 0 extractions.

So the same missing field demotes a randomised trial and promotes a protocol.
The net effect on this corpus, measured the same day:

    39613428  Ver-A-T1D PROTOCOL, no results     15 extractions  (rank 1 of all papers)
    36643381  colchicine PROTOCOL, no results     7 extractions
    36826844  CLVer RCT, n=88, measured result     0 extractions

Two protocols supply 22 of 232 live extractions (9.5%); the trial that
actually measured the outcome supplies none.

WHAT THIS SCRIPT DOES
---------------------
Uses the VERIFIED TITLE as an independent check on the pubtype field. The
title is not a free-text guess: this repo already verifies every title against
PubMed (verify_pmids.py, audit_prose_citation_titles.py), so a design phrase
inside a confirmed title is a PubMed-sourced fact, from a different field than
the one being audited. Where the two PubMed fields disagree, that is worth a
human's attention in either direction.

Deliberately NOT done: this does not rewrite pubtypes or re-grade any path.
Inferring design from words is exactly the habit that produced this repo's
hollow paths. The title phrases matched here are terminal, formulaic
sub-titles ("...: A Randomized Clinical Trial", "Protocol for a ...") that
journals append structurally, not adjectives lifted from a sentence, and every
hit is reported for a human to confirm rather than applied.

Never fails the build. Writes pubtype_title_disagreement.json.
"""

import json
import os
import re
import sys

RESULTS = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'Results'))
PUBTYPE_CACHE = os.path.join(RESULTS, '.pubtype_cache.json')
EXTRACTED = os.path.join(RESULTS, 'extracted_corpus_data.json')
OUT = os.path.join(RESULTS, 'pubtype_title_disagreement.json')

# Each rule: (label, title pattern, pubtypes that would make the title
# redundant, why it matters). Patterns are anchored on the formulaic
# sub-title constructions journals append, not on loose adjectives.
RULES = [
    (
        'PROTOCOL_NOT_TAGGED',
        re.compile(r'\bprotocol\s+for\s+a\b|\bprotocol\s+for\s+an\b|'
                   r':\s*(?:study\s+)?protocol\b|\bstudy\s+protocol\b',
                   re.I),
        {'Clinical Trial Protocol'},
        'title announces a protocol; PubMed did not tag it as one, so the '
        'evidence-design grader cannot see that this paper reports NO results',
    ),
    (
        'RCT_NOT_TAGGED',
        re.compile(r':\s*a\s+randomi[sz]ed\s+(?:clinical\s+|controlled\s+)?trial\b|'
                   r'\ba\s+randomi[sz]ed\s+clinical\s+trial\s*$|'
                   r':\s*a\s+phase\s+[123ivx]+\s+randomi[sz]ed\b',
                   re.I),
        {'Randomized Controlled Trial', 'Clinical Trial',
         'Clinical Trial, Phase I', 'Clinical Trial, Phase II',
         'Clinical Trial, Phase III', 'Controlled Clinical Trial'},
        'title announces a randomised trial; PubMed did not tag it as one, so '
        'the grader demotes measured primary evidence to unknown design',
    ),
    (
        'SYNTHESIS_NOT_TAGGED',
        re.compile(r':\s*a\s+(?:systematic\s+review|meta-?analysis)|'
                   r'\ba\s+systematic\s+review\s+and\s+meta-?analysis',
                   re.I),
        {'Systematic Review', 'Meta-Analysis', 'Network Meta-Analysis'},
        'title announces a synthesis; PubMed did not tag it as one, so the '
        'attribution caveat that applies to scraped synthesis numbers is not raised',
    ),
]

# A protocol that is also tagged as one is fine. These are the pubtypes that,
# if present, mean the grader already knows the design and no gap exists.


def load(path, label):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        print(f'  [skip] cannot read {label}: {exc}')
        return None


def extraction_counts():
    """How many live extractions each PMID supplies. Zero when unavailable."""
    data = load(EXTRACTED, 'extracted_corpus_data.json')
    counts = {}
    if not data:
        return counts
    for bucket in (data.get('extractions') or {}).values():
        if not isinstance(bucket, list):
            continue
        for item in bucket:
            if isinstance(item, dict):
                pmid = str(item.get('pmid') or '')
                if pmid:
                    counts[pmid] = counts.get(pmid, 0) + 1
    return counts


def main():
    print('=' * 74)
    print('PUBTYPE vs VERIFIED-TITLE DISAGREEMENT')
    print('=' * 74)

    cache = load(PUBTYPE_CACHE, '.pubtype_cache.json')
    if not cache:
        print('  No pubtype cache. Exiting clean.')
        return 0

    counts = extraction_counts()
    findings = []

    for pmid, rec in cache.items():
        if not isinstance(rec, dict):
            continue
        title = rec.get('title') or ''
        pubtypes = set(rec.get('pubtype') or [])
        if not title:
            continue
        for label, pattern, satisfying, why in RULES:
            if not pattern.search(title):
                continue
            if pubtypes & satisfying:
                continue  # PubMed already knows; no gap
            findings.append({
                'pmid': pmid,
                'class': label,
                'title': title,
                'journal': rec.get('journal'),
                'year': rec.get('year'),
                'pubtypes': sorted(pubtypes),
                'live_extractions': counts.get(pmid, 0),
                'why_it_matters': why,
            })

    by_class = {}
    for f in findings:
        by_class.setdefault(f['class'], []).append(f)

    print(f'\n  PMIDs with cached pubtypes : {len(cache)}')
    print(f'  Disagreements found        : {len(findings)}')

    for label in ('PROTOCOL_NOT_TAGGED', 'RCT_NOT_TAGGED', 'SYNTHESIS_NOT_TAGGED'):
        rows = sorted(by_class.get(label, []),
                      key=lambda r: -r['live_extractions'])
        if not rows:
            continue
        print(f'\n  {label}  ({len(rows)})')
        for r in rows:
            print(f"    PMID {r['pmid']}  {r['live_extractions']:>3} live extraction(s)"
                  f"  {r['journal']} {r['year']}")
            print(f"        {r['title'][:112]}")
            print(f"        PubMed pubtype: {r['pubtypes'] or '(none)'}")

    # The two directions have opposite consequences and are worth separating.
    untagged_protocol_extractions = sum(
        r['live_extractions'] for r in by_class.get('PROTOCOL_NOT_TAGGED', []))
    silent_trials = [r for r in by_class.get('RCT_NOT_TAGGED', [])
                     if r['live_extractions'] == 0]

    if untagged_protocol_extractions:
        print(f'\n  Untagged protocols are supplying {untagged_protocol_extractions} '
              f'live extraction(s) that the design grader believes came from '
              f'papers of unknown, possibly primary, design.')
    if silent_trials:
        print(f'\n  {len(silent_trials)} untagged randomised trial(s) supply ZERO '
              f'extractions. Measured evidence the corpus already holds is not '
              f'reaching any path:')
        for r in silent_trials:
            print(f"    PMID {r['pmid']}  {r['journal']} {r['year']}  {r['title'][:80]}")

    # ------------------------------------------------------------------
    # How blind is the grader overall, and is it getting blinder?
    # ------------------------------------------------------------------
    # The five disagreements above are the cases a title happens to expose.
    # They are the visible part of a larger hole: any paper whose pubtypes are
    # all generic carries NO design signal at all, and the grader files it as
    # PRIMARY_OTHER. Measuring that by publication year answers whether the
    # gap is a fixed historical residue or something the daily PubMed sweeps
    # actively enlarge.
    GENERIC = {
        'Journal Article', "Research Support, Non-U.S. Gov't",
        'Research Support, N.I.H., Extramural', 'English Abstract',
        "Research Support, U.S. Gov't, P.H.S.",
        "Research Support, U.S. Gov't, Non-P.H.S.",
        'Research Support, N.I.H., Intramural',
    }
    by_year = {}
    generic_total = 0
    for pmid, rec in cache.items():
        if not isinstance(rec, dict):
            continue
        year = str(rec.get('year') or '')
        if not year.isdigit():
            continue
        bucket = year if int(year) >= 2023 else (
            '2018-2022' if int(year) >= 2018 else 'pre-2018')
        slot = by_year.setdefault(bucket, {'papers': 0, 'design_blind': 0})
        slot['papers'] += 1
        if not (set(rec.get('pubtype') or []) - GENERIC):
            slot['design_blind'] += 1
            generic_total += 1
    for slot in by_year.values():
        slot['blind_pct'] = round(100 * slot['design_blind'] / slot['papers'], 1)

    print('\n  DESIGN-BLIND COVERAGE (no design-bearing pubtype at all)')
    print(f'    {"bucket":<12}{"papers":>8}{"blind":>8}{"pct":>8}')
    for bucket in ('pre-2018', '2018-2022', '2023', '2024', '2025', '2026'):
        slot = by_year.get(bucket)
        if slot:
            print(f"    {bucket:<12}{slot['papers']:>8}{slot['design_blind']:>8}"
                  f"{slot['blind_pct']:>7.1f}%")
    print(f'\n    {generic_total} of {len(cache)} cached papers carry no design signal.')
    print('    PubMed assigns design pubtypes on a lag, so the newest papers -'
          '\n    the ones the daily sweeps keep adding - are the least graded.'
          '\n    Evidence-design tiers are most trustworthy on the OLDEST corpus.')

    out = {
        'generated': __import__('datetime').date.today().isoformat(),
        'method': ('verified PubMed title compared against PubMed publication '
                   'type; reported, never applied'),
        'pmids_checked': len(cache),
        'design_blind_total': generic_total,
        'design_blind_by_year': by_year,
        'disagreements': len(findings),
        'by_class': {k: len(v) for k, v in by_class.items()},
        'untagged_protocol_live_extractions': untagged_protocol_extractions,
        'untagged_trials_with_zero_extractions': [r['pmid'] for r in silent_trials],
        'findings': sorted(findings, key=lambda r: -r['live_extractions']),
    }
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f'\n  Written: {OUT}')
    print('\n[OK] audit_pubtype_title_disagreement')
    return 0


if __name__ == '__main__':
    sys.exit(main())
