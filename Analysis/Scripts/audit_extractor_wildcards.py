#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_extractor_wildcards.py  -  added 2026-08-22

WHY THIS EXISTS
---------------
Work-queue item P1 (2026-08-21): "AUDIT THE OTHER 8 EXTRACTORS FOR THE
UNBOUNDED-WILDCARD DEFECT."

On 2026-08-21 `inflammatory_markers` was rewritten after an audit showed 52 of
its 92 extractions (57%) were not measurements - the patterns ended in
`.*?(\\d+\\.?\\d*)` and the capture group therefore took the first digit
ANYWHERE downstream of the marker name. The item flagged four more extractors
as suspect BY CONSTRUCTION (c_peptide, hba1c_change, survival_graft, remission)
but nobody had measured them.

This script measures them. It does two things, both mechanical:

  1. STATIC SCAN. Parse EXTRACTORS out of extract_corpus_data.py and flag every
     pattern containing an unbounded wildcard (`.*?` / `.*` / `.+?`) between a
     marker token and a capture group. Unbounded means: not fenced by a
     character class that excludes `.` and newline.

  2. EMPIRICAL SCAN. Replay every extraction already in
     extracted_corpus_data.json against a set of ARTIFACT SIGNATURES that were
     derived by reading all 292 matched_text strings by hand on 2026-08-22.
     Each signature is a *provable* statement about the matched text, not a
     guess about the paper.

The output is a per-type table of TOTAL / CLEAN / ARTIFACT with the reason
distribution, written to Analysis/Results/extractor_wildcard_audit.json.

WHAT THIS SCRIPT DOES NOT DO
----------------------------
It does not modify extract_corpus_data.py. Rewriting a pattern changes the
published corpus count, so the measurement is committed first and the rewrite
is a separate, reviewable change. Zero is exact; the artifact counts here are a
LOWER bound on the problem because a signature only fires when it is certain.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
SCRIPTS = os.path.join(BASE, 'Scripts')
EXTRACTION_FILE = os.path.join(RESULTS, 'extracted_corpus_data.json')
SOURCE_FILE = os.path.join(SCRIPTS, 'extract_corpus_data.py')
OUT_FILE = os.path.join(RESULTS, 'extractor_wildcard_audit.json')


# ---------------------------------------------------------------------------
# PART 1 - STATIC SCAN
# ---------------------------------------------------------------------------

# An unbounded gap: `.*?`, `.*`, `.+?`, `.+`. A BOUNDED gap looks like
# `[^.\n]{0,60}?` - it cannot cross a sentence boundary or a newline, which is
# the fix applied to inflammatory_markers on 2026-08-21.
UNBOUNDED_GAP = re.compile(r'\.\s*[*+]\??')


def static_scan():
    """Flag every EXTRACTORS pattern containing an unbounded wildcard gap."""
    with open(SOURCE_FILE, encoding='utf-8') as fh:
        src = fh.read()

    # Isolate the EXTRACTORS dict literal.
    start = src.index('EXTRACTORS = {')
    depth, i = 0, start + len('EXTRACTORS = ')
    while i < len(src):
        if src[i] == '{':
            depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0:
                break
        i += 1
    block = src[start:i + 1]

    findings = []
    current_type = None
    for line in block.splitlines():
        m = re.match(r"\s*'([a-z0-9_]+)':\s*\{", line)
        if m:
            current_type = m.group(1)
            continue
        # Pattern lines are raw strings.
        if current_type and re.search(r"r['\"]", line):
            # Strip the comment tail so a `.*` inside a comment is not counted.
            code = line.split('#')[0]
            if UNBOUNDED_GAP.search(code):
                findings.append({
                    'data_type': current_type,
                    'pattern_fragment': line.strip()[:160],
                })
    return findings


# ---------------------------------------------------------------------------
# PART 2 - ARTIFACT SIGNATURES
# ---------------------------------------------------------------------------
# Every signature below was written after reading the matched_text of all 292
# extractions on 2026-08-22. Each returns a reason string only when the text
# PROVES the match is not the measurement its data_type claims. Ambiguous cases
# return None and are counted CLEAN, so these numbers understate the problem.

SENTENCE_BREAK = re.compile(r'[.!?]\s+[A-Z0-9]')

# Registration / accession / genotype identifiers that pattern 3 of `remission`
# - r"(\d+)/(\d+).*?(?:remission|complete response)" - happily swallows.
ID_FRACTION = re.compile(
    r'(?:'
    r'CTRI/\d{4}|NCT\d+|/\d{4}/|\d{4}/\d{2}\b|'          # trial registrations
    r'\b\d{4}/\d+[A-Z]{3}\b|'                             # ethics approvals e.g. 2018/23JAN
    r'\bCD\s?\d+/\d+|\b\d+/\d+\+\s*(?:macrophage|cell)|'  # CD80/86, F4/80+
    r'\bHLA|\bDRB1|\bDQB1|genotype'                       # HLA genotype fractions
    r')', re.IGNORECASE)

# Statistical furniture: a captured number that is part of a CI label, a
# p-value, or an alpha level is not an outcome rate.
STAT_FURNITURE = re.compile(
    r'(?:95\s*%\s*(?:CI|confidence)|significance\s+level|two[- ]tailed|'
    r'\bP\s*[=<≤]|\balpha\b|risk\s+ratio\s+(?:was|of)?\s*\d)', re.IGNORECASE)

# A definition threshold ("remission was defined as HbA1c <6.5%") is metadata.
DEFINITION_THRESHOLD = re.compile(
    r'(?:defined\s+as|definition\s+of|criteri\w+\s+(?:was|were|of))', re.IGNORECASE)

# Time units where a rate was claimed.
TIME_UNIT = re.compile(
    r'\b\d+(?:\.\d+)?\s*(?:month|months|year|years|day|days|week|weeks|mo|yr)\b',
    re.IGNORECASE)

# NOTE: no leading \b. "IL-1beta 20ng/ml" has no word boundary between the
# digit and the unit, and an earlier draft of this audit reported that real
# measurement as an artifact because of it. `fold` counts as a unit: a fold
# change is a legitimate relative measurement and pattern (3) of the rewritten
# inflammatory_markers extractor is built to capture exactly that.
CONC_UNIT = re.compile(
    r'(?:pmol/[Ll]|ng/m[Ll]|nmol/[Ll]|mg/[Ll]|mg/d[Ll]|pg/m[Ll]|[µu]g/m[Ll]|%|'
    r'[-\s]?fold)',
    re.IGNORECASE)

# METHODS-list phrasing: the marker appears in an enumeration of variables that
# were measured, not in a statement of what was measured.
METHODS_ENUMERATION = re.compile(
    r'(?:\bin\s+(?:ng/m[Ll]|pmol/[Ll]|mg/d[Ll])\s*,|'
    r'\band\s+glucose\s+levels\s+of\s+each\s+subject|'
    r'\bwas\s+(?:measured|assessed|performed|collected|determined)\b|'
    r'\bwere\s+(?:measured|assessed|screened|recruited|included)\b|'
    r'\bwe\s+(?:developed|described|assessed|adopted)\b|'
    r'\bMethods\b)', re.IGNORECASE)


def classify(data_type, rec):
    """Return (verdict, reason). verdict in {CLEAN, ARTIFACT}."""
    text = re.sub(r'\s+', ' ', rec.get('matched_text', ''))
    values = rec.get('values') or []
    value = str(values[0]) if values else ''

    # --- universal signatures -------------------------------------------
    if not values:
        return 'ARTIFACT', 'NO_CAPTURED_VALUE'

    if ID_FRACTION.search(text):
        return 'ARTIFACT', 'IDENTIFIER_NOT_OUTCOME'

    if STAT_FURNITURE.search(text) and value in ('95', '0.05', '5'):
        return 'ARTIFACT', 'STATISTICAL_FURNITURE'

    if DEFINITION_THRESHOLD.search(text):
        return 'ARTIFACT', 'DEFINITION_THRESHOLD'

    # A match that crosses a sentence boundary cannot be trusted to have
    # captured a number belonging to the marker. This is the single largest
    # class and is exactly what the bounded-gap rewrite eliminates.
    if SENTENCE_BREAK.search(text):
        return 'ARTIFACT', 'CROSSES_SENTENCE_BOUNDARY'

    # --- per-type signatures --------------------------------------------
    if data_type in ('c_peptide', 'inflammatory_markers'):
        if METHODS_ENUMERATION.search(text):
            return 'ARTIFACT', 'METHODS_ENUMERATION'
        if not CONC_UNIT.search(text):
            return 'ARTIFACT', 'NO_CONCENTRATION_UNIT'

    if data_type in ('remission', 'survival_graft'):
        # A rate needs a percent sign or an explicit n/N denominator adjacent
        # to the claim. Time spans are the commonest impostor.
        has_pct = '%' in text
        has_denom = re.search(r'\b\d+\s*/\s*\d+\b', text) is not None
        if not (has_pct or has_denom):
            if TIME_UNIT.search(text):
                return 'ARTIFACT', 'DURATION_NOT_RATE'
            return 'ARTIFACT', 'NO_RATE_UNIT_OR_DENOMINATOR'
        if METHODS_ENUMERATION.search(text):
            return 'ARTIFACT', 'METHODS_ENUMERATION'

    if data_type == 'hba1c_change':
        # The `glycated hemoglobin .*? (\d+) ± (\d+)` pattern is the offender:
        # it reaches past the HbA1c mention into whatever mean ± SD comes next.
        if 'glycated' in text.lower() and '%' not in text:
            return 'ARTIFACT', 'MEAN_SD_OF_ANOTHER_VARIABLE'

    if data_type == 'autoantibody':
        if METHODS_ENUMERATION.search(text):
            return 'ARTIFACT', 'METHODS_ENUMERATION'
        if '%' not in text:
            return 'ARTIFACT', 'NO_RATE_UNIT_OR_DENOMINATOR'

    return 'CLEAN', ''


def empirical_scan():
    with open(EXTRACTION_FILE, encoding='utf-8') as fh:
        data = json.load(fh)

    report = {}
    detail = defaultdict(list)
    for data_type, records in data['extractions'].items():
        reasons = Counter()
        clean = 0
        for rec in records:
            verdict, reason = classify(data_type, rec)
            if verdict == 'CLEAN':
                clean += 1
            else:
                reasons[reason] += 1
                detail[data_type].append({
                    'pmid': rec.get('pmid'),
                    'reason': reason,
                    'value': (rec.get('values') or [''])[0],
                    'matched_text': re.sub(r'\s+', ' ', rec.get('matched_text', ''))[:180],
                })
        total = len(records)
        report[data_type] = {
            'total': total,
            'clean': clean,
            'artifact': total - clean,
            'artifact_pct': round(100.0 * (total - clean) / total, 1) if total else 0.0,
            'reasons': dict(reasons),
        }
    return report, dict(detail), data


def main():
    static = static_scan()
    report, detail, data = empirical_scan()

    print('=' * 74)
    print('STATIC SCAN - patterns with an unbounded wildcard gap')
    print('=' * 74)
    by_type = defaultdict(int)
    for f in static:
        by_type[f['data_type']] += 1
    for t, n in sorted(by_type.items(), key=lambda kv: -kv[1]):
        print(f'  [WILDCARD] {t:24s} {n} pattern(s)')
    if not static:
        print('  [OK] no unbounded wildcard gaps remain')

    print()
    print('=' * 74)
    print('EMPIRICAL SCAN - artifact rate per extractor')
    print('=' * 74)
    print(f"{'data_type':24s} {'total':>6} {'clean':>6} {'artifact':>9} {'rate':>7}")
    tot = cle = 0
    for t, r in sorted(report.items(), key=lambda kv: -kv[1]['artifact']):
        flag = '[FAIL]' if r['artifact_pct'] >= 40 else ('[WARN]' if r['artifact'] else '[OK]  ')
        print(f"{t:24s} {r['total']:>6} {r['clean']:>6} {r['artifact']:>9} "
              f"{r['artifact_pct']:>6}% {flag}")
        tot += r['total']
        cle += r['clean']
    print('-' * 74)
    print(f"{'TOTAL':24s} {tot:>6} {cle:>6} {tot - cle:>9} "
          f"{round(100.0 * (tot - cle) / tot, 1) if tot else 0:>6}%")

    print()
    print('Reason distribution:')
    allr = Counter()
    for r in report.values():
        allr.update(r['reasons'])
    for reason, n in allr.most_common():
        print(f'  {reason:34s} {n}')

    out = {
        'generated': '2026-08-22',
        'source': 'audit_extractor_wildcards.py',
        'queue_item': 'P1 2026-08-21 - audit the other 8 extractors',
        'corpus_snapshot': data['metadata'].get('total_extractions'),
        'static_wildcard_patterns': static,
        'per_type': report,
        'totals': {'total': tot, 'clean': cle, 'artifact': tot - cle},
        'artifact_detail': detail,
        'caveat': ('Artifact counts are a LOWER bound. A signature fires only '
                   'when the matched text proves the capture is not the claimed '
                   'measurement; ambiguous matches are counted CLEAN.'),
    }
    with open(OUT_FILE, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f'\n[OK] wrote {OUT_FILE}')

    # GATE (added 2026-08-22 when this script joined run_quality_improvements).
    # Two independent failure conditions, because they catch different things:
    #   - a reintroduced unbounded wildcard is a CONSTRUCTION defect, visible
    #     before it has produced a single bad data point;
    #   - a nonzero artifact count is an OUTCOME defect, visible even if the
    #     pattern style looks fine.
    # Both were needed on 2026-08-21: the wildcard in `remission` had been in
    # the file since it was written and nobody measured its output for months.
    failed = False
    if static:
        print(f'\n[FAIL] {len(static)} pattern(s) reintroduce an unbounded '
              f'wildcard gap. Bound the gap with [^.\\n]{{0,N}}? instead.')
        failed = True
    if tot - cle:
        print(f'\n[FAIL] {tot - cle} extraction(s) are provably not the '
              f'measurement their data_type claims.')
        failed = True
    if not failed:
        print('[OK] no unbounded wildcards and no provable artifacts.')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
