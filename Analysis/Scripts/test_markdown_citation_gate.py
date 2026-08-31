#!/usr/bin/env python3
"""Regression fixture for audit_markdown_citations.py.

WHY THIS EXISTS
---------------
On 2026-08-31 the markdown gate reported 0 findings. That number is worthless on
its own, because the same run had just repaired every defect the gate was built
to catch. A silent gate and a working gate look identical from the outside.

This file pins the gate against the ACTUAL text that was in the repo that
morning, before repair. Every fixture below is a verbatim defect, with the true
PubMed record it should have been checked against. If a future edit to the
classifier makes the gate lenient, these fail.

The second block is as important as the first: correct citations that an
over-eager gate flagged on its first draft. A gate that catches every defect by
flagging everything is not a gate. The first draft flagged 71 of 73 sites.

Run: python test_markdown_citation_gate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_markdown_citations import (  # noqa: E402
    citation_record, classify, journal_contradiction, journal_lexicon, LOOKAHEAD,
)
from audit_citation_identifiers import load_cache  # noqa: E402
from audit_builder_title_agreement import overlap, MATCH_THRESHOLD, WEAK_THRESHOLD  # noqa: E402

_cache = load_cache()
LEXICON = journal_lexicon(_cache.get('title', _cache))

# (label, window_text_ending_at_the_pmid, real_meta, expectation)
# `expectation` is 'FLAG' if the gate must report it, 'PASS' if it must not.

MUST_FLAG = [
    (
        'Research_Findings_Summary beta-cell dedifferentiation: Cell 2012 cited '
        'as Diabetologia 2023',
        'Beta cell recovery through reversal of dedifferentiation is now recognized '
        'as a plausible remission mechanism. [PMID:22980982, Diabetologia, 2023]',
        {'title': 'Pancreatic beta cell dedifferentiation as a mechanism of '
                  'diabetic beta cell failure.',
         'journal': 'Cell', 'year': '2012'},
    ),
    (
        'Research_Findings_Summary retatrutide: NEJM 2023 cited as JAMA 2024',
        '**Retatrutide ("Triple G"):** GLP-1/GIP/glucagon triple receptor agonist. '
        'In the TRIUMPH-4 Phase 2 trial, achieved 28.7% mean body weight reduction '
        'at 68 weeks. [PMID:37366315, JAMA, 2024]',
        {'title': 'Triple-Hormone-Receptor Agonist Retatrutide for Obesity - '
                  'A Phase 2 Trial.',
         'journal': 'The New England journal of medicine', 'year': '2023'},
    ),
    (
        'Research_Findings_Summary dorzagliatin: Pharmaceuticals 2025 cited as '
        'Nature Medicine 2022',
        '**Dorzagliatin:** First-in-class glucokinase activator that targets the '
        'glucose-sensing mechanism. Approved in China (2022); US Phase 1b trials '
        'underway. [PMID:40573322, Nature Medicine, 2022]',
        {'title': 'In Vivo PK-PD and Drug-Drug Interaction Study of Dorzagliatin '
                  'for the Management of PI3K-alpha Inhibitor-Induced Hyperglycemia.',
         'journal': 'Pharmaceuticals (Basel, Switzerland)', 'year': '2025'},
    ),
    (
        'RESEARCH_DOCTRINE citation-format exemplar pointing at a RETRACTED '
        'ginsenoside paper',
        'Mehta A, Beatus T, Smith R, et al. "Islet transplantation outcomes in '
        'Type 1 diabetes." Diabetes Care. 2024;47(3):456-468. PMID: 38234567.',
        {'title': 'Retracted: Ginsenoside Rg1 Ameliorates Acute Renal '
                  'Ischemia/Reperfusion Injury via Upregulating AMPK-alpha1 Expression.',
         'journal': 'Oxidative medicine and cellular longevity', 'year': '2024'},
    ),
]

MUST_PASS = [
    (
        'descriptive prose naming no title and no year (first draft flagged this)',
        '- General diabetes drug cost-effectiveness (PMID 38639547) covers SGLT2i '
        'and GLP-1 agonists',
        {'title': 'Cost-Effectiveness of Newer Pharmacologic Treatments in Adults '
                  'With Type 2 Diabetes: A Systematic Review.',
         'journal': 'Annals of internal medicine', 'year': '2024'},
    ),
    (
        'descriptive prose with an incidental short quote (first draft flagged this)',
        '- Note: PMID 37385967 found as reference to "diabetes remission" study '
        'but not fully verified',
        {'title': 'Diabetes remission in drug-naive patients with type 2 diabetes '
                  'after dorzagliatin treatment: A prospective cohort study.',
         'journal': 'Diabetes, obesity & metabolism', 'year': '2023'},
    ),
    (
        'correctly asserted title beside its identifier',
        'Markmann JF, Rickels MR, et al. "Phase 3 trial of human islet-after-kidney '
        'transplantation in type 1 diabetes." Am J Transplant. 2021;21(4):1477-1492. '
        'PMID: 32627352.',
        {'title': 'Phase 3 trial of human islet-after-kidney transplantation in '
                  'type 1 diabetes.',
         'journal': 'American journal of transplantation', 'year': '2021'},
    ),
    (
        'bold used for emphasis, not as a title (first draft read it as a title)',
        'GLP-1 receptor agonists have reported anti-inflammatory effects. '
        '**Both are narrative reviews, not studies** [PMID:38578067, '
        'J R Coll Physicians Edinb, 2024]',
        {'title': 'Existing and emerging GLP-1 receptor agonist therapy: '
                  'Ramifications for diabetic retinopathy screening.',
         'journal': 'The journal of the Royal College of Physicians of Edinburgh',
         'year': '2024'},
    ),
]


def verdict_for(window, meta):
    """Mirror the decision main() makes, without the network."""
    import re
    padded = window + ' ' * LOOKAHEAD
    kind, residual = classify(padded, meta)
    if kind == 'TITLE_ASSERTED':
        score = max(overlap(span, meta['title']) for span in residual)
        if score < WEAK_THRESHOLD:
            return 'FLAG', f'MISMATCH kind={kind} score={score:.2f}'
        if score < MATCH_THRESHOLD:
            return 'FLAG', f'WEAK kind={kind} score={score:.2f}'
        return 'PASS', f'OK kind={kind} score={score:.2f}'
    if kind == 'COORDINATE_ONLY':
        pmid = re.search(r'PMID[:\s#]*(\d{7,9})', window, re.IGNORECASE).group(1)
        record = citation_record(window, pmid)
        scope = record if record else window[-160:]
        years = [int(y) for y in re.findall(r'\b((?:19|20)\d{2})\b', scope)]
        real = meta.get('year')
        if years and real and not any(abs(y - int(real)) <= 1 for y in years):
            return 'FLAG', f'COORDINATE_MISMATCH years={years} real={real}'
        named = journal_contradiction(record, meta.get('journal'), LEXICON)
        if named:
            return 'FLAG', f'COORDINATE_MISMATCH names={named} real={meta.get("journal")!r}'
        return 'PASS', f'OK kind={kind} years={years}'
    return 'PASS', f'OK kind={kind}'


def main():
    failures = 0
    print('=' * 74)
    print('REGRESSION FIXTURE - audit_markdown_citations.py')
    print('=' * 74)

    print('\nMUST FLAG (verbatim defects present in the repo on 2026-08-31):')
    for label, window, meta in MUST_FLAG:
        got, detail = verdict_for(window, meta)
        ok = got == 'FLAG'
        failures += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
        print(f"         -> {detail}")

    print('\nMUST NOT FLAG (correct citations the first draft flagged anyway):')
    for label, window, meta in MUST_PASS:
        got, detail = verdict_for(window, meta)
        ok = got == 'PASS'
        failures += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
        print(f"         -> {detail}")

    total = len(MUST_FLAG) + len(MUST_PASS)
    print(f'\n{total - failures}/{total} fixtures behave as specified.')
    if failures:
        print('[FAIL] the gate no longer behaves as calibrated')
        return 1
    print('[OK] gate sensitivity and specificity both pinned')
    return 0


if __name__ == '__main__':
    sys.exit(main())
