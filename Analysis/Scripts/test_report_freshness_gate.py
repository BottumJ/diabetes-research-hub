#!/usr/bin/env python3
"""Regression fixture: report-freshness gate sensitivity AND specificity.

WHY THIS EXISTS
---------------
audit_report_freshness.py passed 2/2 on its first run. That proves nothing on
its own, for the same reason test_markdown_citation_gate.py exists: the run
that first executed the gate had already repaired both defects it was built to
catch, so a green result is equally consistent with "the repo is clean" and
"the gate is a no-op". This replays the PRE-REPAIR text and asserts the gate
fails on it, then replays clean text and asserts it does not.

The four cases below are the two real 2026-09 defects plus their controls:

  A  SELF-CONTRADICTING (real, pubmed_recent_summary.md as of 2026-09-04):
     declares a 30-day rolling window, generated 49 days ago. MUST FAIL.

  B  LAUNDERED PROVENANCE (real, literature_gap_report.md as of 2026-09-04):
     rendered today, from a data file written 50 days ago. This is the case
     the 2026-09-04 run inspected and cleared as "regenerates, therefore
     fine". MUST FAIL, and it is the reason the gate reads the DATA date
     rather than the render date.

  C  FRESH (control): rendered today from data written today. MUST PASS -
     a gate that fails everything is as useless as one that fails nothing.

  D  UNDATED (control): a report declaring no window at all. Must still be
     held to the default ceiling, so that adding an undated report to the hub
     cannot silently opt out of the gate. MUST FAIL when old.

Runs entirely on temporary fixtures. Touches no repo file.

EXIT CODES
    0 = gate is both sensitive and specific
    1 = gate missed a defect it exists to catch, or flagged a clean report
"""
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from datetime import date, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(SCRIPT_DIR, 'audit_report_freshness.py')


def load_gate():
    spec = importlib.util.spec_from_file_location('_freshness_gate', GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_case(root, report_name, report_text, data_name=None, data_date=None):
    """Write one fixture: a hub that links the report, plus its data file."""
    results = os.path.join(root, 'Analysis', 'Results')
    docs = os.path.join(root, 'docs')
    reports = os.path.join(docs, 'Reports')
    for d in (results, reports):
        os.makedirs(d, exist_ok=True)

    for path in (os.path.join(results, report_name),
                 os.path.join(reports, report_name)):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(report_text)

    with open(os.path.join(docs, 'index.html'), 'w', encoding='utf-8') as f:
        f.write('<a href="Reports/%s">View report &rarr;</a>' % report_name)

    if data_name:
        with open(os.path.join(results, data_name), 'w', encoding='utf-8') as f:
            json.dump({'metadata': {'generated': data_date.isoformat()}}, f)


def run_case(mod, root, report_name):
    """Point the gate's paths at the fixture and audit the one report."""
    mod.BASE_DIR = root
    mod.RESULTS_DIR = os.path.join(root, 'Analysis', 'Results')
    mod.DOCS_DIR = os.path.join(root, 'docs')
    mod.REPORTS_DIR = os.path.join(mod.DOCS_DIR, 'Reports')
    mod.INDEX = os.path.join(mod.DOCS_DIR, 'index.html')
    assert mod.hub_reports() == [report_name], 'fixture hub did not advertise the report'
    return mod.audit_one(report_name, date.today())


def main():
    mod = load_gate()
    today = date.today()
    saved = {k: getattr(mod, k) for k in
             ('BASE_DIR', 'RESULTS_DIR', 'DOCS_DIR', 'REPORTS_DIR', 'INDEX',
              'PROVENANCE')}

    cases = []

    # A - self-contradicting rolling window (the real 2026-09-04 text)
    gen_a = today - timedelta(days=49)
    cases.append(dict(
        label='A self-contradicting 30-day window generated 49d ago',
        report='pubmed_recent_summary.md',
        text=('# PubMed Recent Publications Report\n'
              '**Generated:** %s\n'
              '**Lookback period:** 30 days\n'
              '**Unique papers found:** 158\n' % gen_a.isoformat()),
        data=('pubmed_recent_latest.json', gen_a),
        must_fail=True,
        expect_substring='SELF-CONTRADICTING'))

    # B - laundered provenance: fresh render over 50-day-old data
    cases.append(dict(
        label='B fresh render over 50-day-old data (cleared as "fine" 2026-09-04)',
        report='literature_gap_report.md',
        text=('# Literature Gap Analysis - Interpreted Report\n'
              '**Generated:** %s\n'
              '**Source:** PubMed E-utilities API (esearch.fcgi)\n'
              '**Date range:** 2020/01/01 to %s\n'
              % (today.isoformat(),
                 (today - timedelta(days=50)).strftime('%Y/%m/%d'))),
        data=('literature_gap_data.json', today - timedelta(days=50)),
        must_fail=True,
        expect_substring='STALE DATA BEHIND A FRESH STAMP'))

    # C - control: genuinely fresh
    cases.append(dict(
        label='C genuinely fresh report (control - must pass)',
        report='literature_gap_report.md',
        text=('# Literature Gap Analysis Report\n'
              '**Generated:** %s\n'
              '**Source:** PubMed (date range: 2020/01/01 to %s)\n'
              % (today.isoformat(), today.strftime('%Y/%m/%d'))),
        data=('literature_gap_data.json', today),
        must_fail=False,
        expect_substring=None))

    # D - control: no declared window at all, and old
    cases.append(dict(
        label='D undated report, %dd old (must not escape the ceiling)'
              % (mod.DEFAULT_MAX_AGE_DAYS + 10),
        report='literature_gap_report.md',
        text=('# Some Report\n**Generated:** %s\n'
              % (today - timedelta(days=mod.DEFAULT_MAX_AGE_DAYS + 10)).isoformat()),
        data=None,
        must_fail=True,
        expect_substring='SELF-CONTRADICTING'))

    print('=' * 68)
    print('  REGRESSION FIXTURE: report-freshness gate')
    print('=' * 68)
    print('  A gate that has only ever seen clean input is untested.')
    print()

    problems = []
    try:
        for c in cases:
            root = tempfile.mkdtemp(prefix='freshfix_')
            try:
                data_name, data_date = c['data'] if c['data'] else (None, None)
                build_case(root, c['report'], c['text'], data_name, data_date)
                mod.PROVENANCE = ({c['report']: data_name} if data_name else {})
                rec = run_case(mod, root, c['report'])
                failed = bool(rec['failures'])

                if failed != c['must_fail']:
                    verdict = 'WRONG'
                    problems.append(
                        '%s: expected %s, got %s'
                        % (c['label'],
                           'FAIL' if c['must_fail'] else 'PASS',
                           'FAIL' if failed else 'PASS'))
                elif c['expect_substring'] and not any(
                        c['expect_substring'] in f for f in rec['failures']):
                    verdict = 'WRONG'
                    problems.append(
                        '%s: failed, but for the wrong reason - no "%s" in %r'
                        % (c['label'], c['expect_substring'], rec['failures']))
                else:
                    verdict = 'OK'

                print('  [%s] %s' % (verdict, c['label']))
                print('        gate says: %s'
                      % ('FAIL' if failed else 'PASS'))
                for f in rec['failures']:
                    print('          -> %s' % f)
            finally:
                shutil.rmtree(root, ignore_errors=True)
    finally:
        for k, v in saved.items():
            setattr(mod, k, v)

    print()
    if problems:
        print('  FAIL - the gate is not doing what it claims:')
        for p in problems:
            print('    * %s' % p)
        return 1
    print('  PASS - gate is sensitive to both real 2026-09 defects and')
    print('  specific enough to clear a genuinely fresh report.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
