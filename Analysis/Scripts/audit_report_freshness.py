#!/usr/bin/env python3
"""Assert that every report the hub publishes is as current as it claims to be.

WHY THIS EXISTS
---------------
This repo owns fourteen citation gates. Every one of them asks a question about
a SOURCE: does the PMID resolve, is it on topic, is the title right, was it
retracted, is the journal coordinate real, does the abstract echo the claim.
Not one of them asks whether the PAGE is current, and a page can be false for
that reason alone while every citation on it is true.

Two instances, found a day apart, and the second is the reason this file is a
gate rather than a fix:

  2026-09-04  pubmed_recent_summary.md declared "Lookback period: 30 days" and
              "Generated: 2026-07-17" - 49 days into a 30-day window - under a
              hub card reading "Rolling 30-day PubMed snapshot", status
              "Available". 47 green pipeline stages said nothing. The run
              added a provenance banner so a reader could see the age. That is
              disclosure, not repair.

  2026-09-05  The same run cleared the other published report in one line:
              "literature_gap_report.md, which regenerates (2026-09-03) and is
              therefore fine." It was not fine. Measured:

                  literature_gap_report.md   rendered 2026-09-04   <- fresh
                  literature_gap_data.json   written  2026-07-17   <- 50 days

              improve_gap_analysis.py re-rendered the report from frozen JSON
              every day and stamped each copy "**Generated:** <today>". The
              stale one at least admitted its age; this one laundered 50-day-old
              data behind a fresh timestamp, and the check that cleared it -
              "does the file regenerate" - is a check that cannot ever catch it.

THE RULE
--------
A report's freshness is the age of its OLDEST INPUT, never the age of its own
rendering. Two independent assertions, and a report must pass both:

  1. DECLARED-WINDOW RULE. If a report declares a lookback window ("Lookback
     period: N days", "Date range: A to B"), the data behind it must not be
     older than that window. A 30-day rolling snapshot generated 49 days ago is
     self-contradicting on its own face.

  2. PROVENANCE RULE. Where a report is rendered from a named data file, that
     data file's age is what counts, and it is compared against the report's
     own declared generation date. A gap wider than PROVENANCE_TOLERANCE_DAYS
     means the report is advertising a currency its inputs do not have.

SCOPE IS DERIVED, NOT LISTED
----------------------------
Which reports are in scope comes from docs/index.html at run time - the same
rule sync_docs_reports.py uses - so a report added to the hub is gated the day
it is added and one removed stops being gated without anyone editing this file.
A hardcoded list is how the two files above went years unchecked.

EXIT CODES
    0 = every published report is within the currency it advertises
    1 = at least one report is older than it claims (FAIL)
"""
import json
import os
import re
import sys
from datetime import date, datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
RESULTS_DIR = os.path.join(BASE_DIR, 'Analysis', 'Results')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
REPORTS_DIR = os.path.join(DOCS_DIR, 'Reports')
INDEX = os.path.join(DOCS_DIR, 'index.html')
OUT_JSON = os.path.join(RESULTS_DIR, 'report_freshness_audit.json')

HUB_LINK_RE = re.compile(r'href="Reports/([A-Za-z0-9_\-.]+\.md)"')

# Slack on the provenance rule. A report rendered today from data written
# yesterday is fine; the failure being gated is a report rendered today from
# data written seven weeks ago. Set generously on purpose - this gate should
# fire on laundering, not on ordinary pipeline ordering.
PROVENANCE_TOLERANCE_DAYS = 7

# A report that declares NO window at all gets this ceiling, so that adding an
# undated report to the hub cannot silently opt out of the gate.
DEFAULT_MAX_AGE_DAYS = 45

# Report -> the data file it is rendered from. Only entries whose data file the
# report cannot name itself; this is deliberately small and each line is a
# claim that can be checked by reading the renderer.
#   improve_gap_analysis.py:load_gap_data() reads literature_gap_data.json
#   baseline_pubmed_alerts.py writes its own md and json in the same call
PROVENANCE = {
    'literature_gap_report.md': 'literature_gap_data.json',
    'pubmed_recent_summary.md': 'pubmed_recent_latest.json',
}

GEN_RE = re.compile(r'\*\*Generated:\*\*\s*(\d{4}-\d{2}-\d{2})')
LOOKBACK_RE = re.compile(r'\*\*Lookback period:\*\*\s*(\d+)\s*days', re.I)
# Two renderers write this report and they word the coverage line differently:
#   improve_gap_analysis.py   "**Date range:** 2020/01/01 to 2026/09/05"
#   gap_analysis_daily.py     "**Source:** PubMed (date range: 2020/01/01 to 2026/09/05)"
# Matching only the first is how a gate acquires a blind spot that looks like a
# pass, so this matches the coverage statement wherever it sits on the line.
DATERANGE_RE = re.compile(
    r'date\s*range:?\*{0,2}\s*\(?\s*(\d{4}/\d{2}/\d{2})\s*to\s*(\d{4}/\d{2}/\d{2})',
    re.I)


def _d(s, fmt='%Y-%m-%d'):
    try:
        return datetime.strptime(s, fmt).date()
    except (ValueError, TypeError):
        return None


def hub_reports():
    """The reports the hub advertises. Authority is docs/index.html."""
    if not os.path.exists(INDEX):
        return []
    with open(INDEX, encoding='utf-8') as f:
        return sorted(set(HUB_LINK_RE.findall(f.read())))


def data_file_date(basename):
    """Generation date a data file declares, falling back to its mtime."""
    path = os.path.join(RESULTS_DIR, basename)
    if not os.path.exists(path):
        return None, 'missing'
    try:
        with open(path, encoding='utf-8') as f:
            meta = (json.load(f) or {}).get('metadata', {})
        stamp = meta.get('generated') or meta.get('date')
        if stamp:
            d = _d(str(stamp)[:10])
            if d:
                return d, 'declared'
    except (ValueError, OSError):
        pass
    return date.fromtimestamp(os.path.getmtime(path)), 'mtime'


def audit_one(basename, today):
    """Return a finding dict for one published report."""
    src = os.path.join(RESULTS_DIR, basename)
    pub = os.path.join(REPORTS_DIR, basename)
    rec = {
        'report': basename,
        'published': os.path.exists(pub),
        'failures': [],
    }
    if not os.path.exists(src):
        rec['failures'].append('SOURCE MISSING: %s' % src)
        return rec

    with open(src, encoding='utf-8') as f:
        text = f.read()

    gen = GEN_RE.search(text)
    gen_date = _d(gen.group(1)) if gen else None
    rec['declared_generated'] = gen_date.isoformat() if gen_date else None
    rec['render_age_days'] = (today - gen_date).days if gen_date else None

    # ---- Rule 1: declared window ----------------------------------------
    window = None
    window_src = None
    m = LOOKBACK_RE.search(text)
    if m:
        window, window_src = int(m.group(1)), 'lookback period'
    else:
        m = DATERANGE_RE.search(text)
        if m:
            end = _d(m.group(2), '%Y/%m/%d')
            if end:
                # A date range is not a rolling window; what it asserts is that
                # the data runs up to `end`. Age of the data is today - end.
                window, window_src = DEFAULT_MAX_AGE_DAYS, 'date range'
                rec['data_covered_through'] = end.isoformat()
                rec['coverage_age_days'] = (today - end).days
                if (today - end).days > DEFAULT_MAX_AGE_DAYS:
                    rec['failures'].append(
                        'COVERAGE STALE: declares data through %s, %d days ago '
                        '(ceiling %d).'
                        % (end.isoformat(), (today - end).days,
                           DEFAULT_MAX_AGE_DAYS))
    if window is None:
        window, window_src = DEFAULT_MAX_AGE_DAYS, 'default ceiling'
    rec['window_days'] = window
    rec['window_source'] = window_src

    if gen_date and (today - gen_date).days > window:
        rec['failures'].append(
            'SELF-CONTRADICTING: declares a %d-day %s but was generated %s, '
            '%d days ago.'
            % (window, window_src, gen_date.isoformat(),
               (today - gen_date).days))

    # ---- Rule 2: provenance ---------------------------------------------
    dep = PROVENANCE.get(basename)
    if dep:
        dep_date, how = data_file_date(dep)
        rec['data_file'] = dep
        rec['data_date'] = dep_date.isoformat() if dep_date else None
        rec['data_date_source'] = how
        if dep_date is None:
            rec['failures'].append('DATA FILE MISSING: %s' % dep)
        else:
            rec['data_age_days'] = (today - dep_date).days
            if gen_date:
                lag = (gen_date - dep_date).days
                rec['render_minus_data_days'] = lag
                if lag > PROVENANCE_TOLERANCE_DAYS:
                    rec['failures'].append(
                        'STALE DATA BEHIND A FRESH STAMP: rendered %s from %s '
                        'written %s - a %d-day lag (tolerance %d). The report '
                        'advertises a currency its input does not have.'
                        % (gen_date.isoformat(), dep, dep_date.isoformat(),
                           lag, PROVENANCE_TOLERANCE_DAYS))
            if (today - dep_date).days > window:
                rec['failures'].append(
                    'DATA OLDER THAN DECLARED WINDOW: %s written %s, %d days '
                    'ago, against a %d-day %s.'
                    % (dep, dep_date.isoformat(), (today - dep_date).days,
                       window, window_src))
    return rec


def main():
    today = date.today()
    reports = hub_reports()

    print('=' * 68)
    print('  PUBLISHED REPORT FRESHNESS AUDIT')
    print('=' * 68)
    if not os.path.exists(INDEX):
        print('  docs/index.html not found - nothing advertised, nothing to check.')
        return 0
    print('  Hub advertises %d markdown report(s); today is %s.'
          % (len(reports), today.isoformat()))
    print('  Freshness is the age of a report\'s OLDEST INPUT, not of its render.')
    print()

    findings = [audit_one(r, today) for r in reports]

    for rec in findings:
        ok = not rec['failures']
        print('  [%s] %s' % ('OK' if ok else 'FAIL', rec['report']))
        bits = []
        if rec.get('declared_generated'):
            bits.append('rendered %s (%dd ago)'
                        % (rec['declared_generated'], rec['render_age_days']))
        if rec.get('data_file'):
            bits.append('data %s %s (%dd ago)'
                        % (rec['data_file'], rec.get('data_date'),
                           rec.get('data_age_days', -1)))
        if rec.get('window_days'):
            bits.append('window %dd (%s)'
                        % (rec['window_days'], rec['window_source']))
        if bits:
            print('         %s' % ' | '.join(bits))
        for f in rec['failures']:
            print('         -> %s' % f)

    failing = [r for r in findings if r['failures']]
    payload = {
        'generated': datetime.now().isoformat(),
        'today': today.isoformat(),
        'provenance_tolerance_days': PROVENANCE_TOLERANCE_DAYS,
        'default_max_age_days': DEFAULT_MAX_AGE_DAYS,
        'reports_checked': len(findings),
        'reports_failing': len(failing),
        'findings': findings,
    }
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)

    print()
    print('  %d report(s) checked, %d failing.' % (len(findings), len(failing)))
    print('  Written: %s' % OUT_JSON)

    if failing:
        print()
        print('  FAIL. A report that is older than the window it advertises is')
        print('  a false claim on the published site, whatever its citations say.')
        return 1
    print('  PASS.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
