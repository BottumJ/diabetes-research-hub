#!/usr/bin/env python3
"""
Citation MISMATCH gate.

WHY THIS EXISTS
---------------
validate_citations.py has been correctly scoring miscited PMIDs as "MISMATCH"
for months, writing them to Analysis/Results/citation_validation.json. Nothing
ever read that field. On 2026-08-16 a routine audit found SEVEN real
miscitations sitting unactioned in the build scripts, including two PMIDs that
resolved to plant-biology papers being cited as the DIAGNODE-2 trial and a
GAD-alum meta-analysis:

    19237585  nicotinic receptors / epilepsy  <- cited as Lamkanfi glyburide NLRP3
    23223116  anesthesiology resident survey  <- cited as TINSAL-T2D salsalate RCT
    33515517  paediatric pneumococcal disease <- cited as DIAGNODE-2
    18794064  metastatic colon cancer         <- cited as Ludvigsson NEJM 2008
    32243867  multiple sclerosis / MMP        <- cited as ACTION LADA
    34299352  Medicago sativa GRAS genes      <- cited as DIAGNODE-2
    35491968  Capsicum bacterial wilt         <- cited as GAD-alum IPD meta-analysis

Those miscitations were also the reason several off-topic oncology/infectious
-disease papers were sitting in the corpus flagged as "unclear relevance": they
were ingested BECAUSE they were miscited.

The detector worked. The loop was open. This script closes it.

BEHAVIOUR
---------
Exit 0  -> no unresolved mismatches, pipeline may proceed.
Exit 1  -> at least one unresolved MISMATCH; prints each with its citation site.

A mismatch may be suppressed only by adding its PMID to WHITELIST below, with a
written reason. The only legitimate suppression is a false positive where the
"PMID" is not a citation at all (e.g. a regex example inside source code).

Usage:
    python check_citation_mismatches.py            # gate
    python check_citation_mismatches.py --report   # list, always exit 0
"""

import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'Results')
VALIDATION_PATH = os.path.join(RESULTS_DIR, 'citation_validation.json')

# PMID -> reason. Suppression requires a written justification.
WHITELIST = {
    '12345678': (
        'FALSE POSITIVE, not a citation. Appears in postprocess_dashboards.py '
        'inside a regex comment illustrating the PMID-linkifier pattern '
        '("match PMID: 12345678"). No claim is attached to it.'
    ),
}


def load_validation():
    if not os.path.exists(VALIDATION_PATH):
        print('[WARN] %s not found - run validate_citations.py first.' % VALIDATION_PATH)
        return None
    with open(VALIDATION_PATH, encoding='utf-8') as fh:
        return json.load(fh)


# Scripts whose PURPOSE is to name a bad citation. A repair script's docstring
# has to quote the PMID it is repairing in order to document the repair; scoring
# that quotation as a citation makes every fix generate a new failure, and the
# only ways out are deleting the explanation or whitelisting a PMID that is
# genuinely wrong -- both of which destroy the audit trail.
#
# This mirrors AUDIT_TRAIL_FIELDS in audit_citation_identifiers.py, which
# already applies the same rule at field level to state records. Added
# 2026-08-24, when repair_builder_citations_20260824.py explaining that PMID
# 19148081 is "Your inbox, Mr President." failed the gate for saying so.
#
# Structural, not per-PMID: suppression by PMID would also hide the citation if
# it reappeared at a real claim site, which is exactly what must not happen.
ERROR_REPORT_SCRIPT = re.compile(
    r'^(repair_|fix_|audit_|check_|reconcile_|_close_run_|_run_)', re.I)


def only_cited_by_error_reports(rec):
    """True if every citing site is a script that exists to report the error."""
    claims = rec.get('claims') or []
    if not claims:
        return False
    files = [os.path.basename(c.get('file') or '') for c in claims]
    return all(ERROR_REPORT_SCRIPT.match(f) for f in files if f)


def collect_mismatches(data):
    out, audit_only = [], []
    for pmid, rec in (data.get('results') or {}).items():
        if rec.get('score') != 'MISMATCH':
            continue
        if pmid in WHITELIST:
            continue
        if only_cited_by_error_reports(rec):
            audit_only.append(pmid)
            continue
        out.append((pmid, rec))
    out.sort(key=lambda kv: kv[1].get('confidence', 0))
    return out, audit_only


def main():
    report_only = '--report' in sys.argv
    data = load_validation()
    if data is None:
        return 0 if report_only else 1

    mismatches, audit_only = collect_mismatches(data)
    total = len(data.get('results') or {})

    print('Citation mismatch gate')
    print('  source      : %s' % VALIDATION_PATH)
    print('  generated   : %s' % data.get('timestamp', 'unknown'))
    print('  PMIDs scored: %d' % total)
    print('  suppressed  : %d (whitelisted false positives)' % len(WHITELIST))
    print('  audit-trail : %d (cited only by scripts that report the error: %s)'
          % (len(audit_only), ', '.join(sorted(audit_only)) or '-'))
    print('  unresolved  : %d' % len(mismatches))
    print()

    if not mismatches:
        print('[OK] No unresolved citation mismatches.')
        return 0

    print('[FAIL] Unresolved MISMATCH citations - a cited PMID does not support its claim.')
    print('       Resolve each by verifying the intended paper via NCBI esummary and')
    print('       correcting the PMID at the citation site (do NOT delete the claim).')
    print()
    for pmid, rec in mismatches:
        print('  PMID %s  confidence=%.3f' % (pmid, rec.get('confidence', 0)))
        print('    resolves to : %s' % (rec.get('title') or '?')[:100])
        print('    detail      : %s' % rec.get('details', ''))
        for claim in (rec.get('claims') or [])[:3]:
            print('    cited in    : %s line %s' % (claim.get('file'), claim.get('line')))
        print()

    return 0 if report_only else 1


if __name__ == '__main__':
    sys.exit(main())
