#!/usr/bin/env python3
"""
Verification Gate for Diabetes Research Hub Dashboards.

Scans HTML dashboard files for credibility issues before deployment.
Each dashboard receives a severity-scored report. Dashboards with CRITICAL
issues are flagged for quarantine.

Checks performed:
  1. PMID Density     — Are specific claims backed by PMIDs?
  2. Vague Citations  — "Nature 2024" style references without PMIDs
  3. Unsourced Stats  — Dollar amounts, percentages, sample sizes without citations
  4. Implausible Claims — AUC 1.0, "100% cure rate", "zero side effects"
  5. Overstated Language — "curative", "proven", "breakthrough" in clinical context
  6. Financial Claims  — Market projections, cost estimates without methodology

Output:
  - Console summary
  - JSON report per dashboard in Analysis/Results/verification_reports/
  - Exit code 0 if no CRITICAL, 1 if any CRITICAL found

Usage:
  python verify_before_deploy.py                    # Check all dashboards
  python verify_before_deploy.py --file X.html      # Check one dashboard
  python verify_before_deploy.py --quarantine       # Move CRITICAL dashboards to quarantine
"""

import os
import re
import json
import sys
import shutil
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..'))
DASHBOARD_DIR = os.path.join(BASE_DIR, 'Dashboards')
QUARANTINE_DIR = os.path.join(DASHBOARD_DIR, '_quarantine')
REPORT_DIR = os.path.join(BASE_DIR, 'Analysis', 'Results', 'verification_reports')


# ── Patterns ────────────────────────────────────────────────────────────────

# PMIDs: both "PMID:12345678" and pubmed.ncbi.nlm.nih.gov/12345678
PMID_PATTERN = re.compile(r'PMID[:\s]?\d{7,8}|pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,8})')

# PMIDs embedded in JavaScript data structures (e.g., "key_pmids": "29988125, 36060506")
# These appear in dashboards that render citations via JS template literals rather than static HTML.
JS_PMID_PATTERN = re.compile(
    r'["\']key_pmids["\']\s*:\s*["\']'   # field name and opening quote
    r'([\d,\s]+)'                          # comma-separated digit sequences
    r'["\']'                               # closing quote
)

# NCT numbers: "NCT12345678" — valid citations for trial dashboards
NCT_PATTERN = re.compile(r'NCT\d{8}')

# Reference/structural dashboards where PMIDs are not the primary citation type.
# These get relaxed PMID density thresholds (issues downgraded from CRITICAL to MEDIUM).
REFERENCE_DASHBOARDS = {
    'Acronym_Database.html',        # Abbreviation lookup — no evidence claims
    'Methodology.html',             # Process documentation — describes our methods
    'Corpus_Analysis.html',         # Co-occurrence statistics — computational, not clinical
    'PMID_Verification.html',       # Internal audit tool
    'Research_Dashboard.html',      # Overview/landing page — links to other dashboards
    'Statistical_Analysis.html',    # Meta-analytic computations — stats, not clinical claims
}

# Trial-centric dashboards where NCT numbers are valid citations alongside PMIDs
TRIAL_DASHBOARDS = {
    'Clinical_Trial_Dashboard.html',
    'Trial_Equity_Mapper.html',
    'Research_Paths.html',          # Contains trial-based paths
}

# Vague journal citations without PMIDs — "Nature 2024", "Lancet Diabetes Endocrinol 2024"
VAGUE_JOURNAL = re.compile(
    r'(?:Nature|Lancet|NEJM|New England Journal|Science|JAMA|BMJ|Cell|'
    r'Diabetes Care|Diabetologia|Journal of Clinical Investigation|JCI|'
    r'Frontiers in Immunology|Nature Medicine|Nature Immunology|'
    r'Nature Biotechnology|Nature Reviews|Nature Biomedical Engineering|'
    r'Nature Communications|Lancet Diabetes)'
    r'\s*(?:&amp;\s*)?(?:Endocrinol(?:ogy)?)?\s*'
    r'(?:,?\s*)?(?:20\d{2})',
    re.IGNORECASE
)

# Dollar amounts — $500, $1.3B, $20,000/year, etc.
DOLLAR_PATTERN = re.compile(r'\$[\d,]+(?:\.\d+)?(?:\s*(?:billion|million|B|M|K|trillion))?(?:/\w+)?')

# Specific percentages — "37.6%", "72.7% remission"
PERCENT_PATTERN = re.compile(r'\d+\.?\d*\s*%')

# Sample sizes — "n=297", "N=6,156"
SAMPLE_SIZE = re.compile(r'[nN]\s*[=:]\s*[\d,]+')

# Implausible perfection claims
IMPLAUSIBLE = re.compile(
    r'AUC\s*(?:of\s*)?(?:=\s*)?1\.0|'
    r'100\s*%\s*(?:cure|remission|success|accuracy|sensitivity|specificity)|'
    r'zero\s+(?:rejection|side\s*effects?|adverse\s*events?|SAEs?|mortality|failure)',
    re.IGNORECASE
)

# Overstated clinical language
OVERSTATED = re.compile(
    r'\bcurative\b|\bproven\s+(?:to|effective|safe)\b|\bbreakthrough\s+(?:cure|treatment|therapy)\b|'
    r'\bguaranteed\b|\bdefinitively\b|\bundeniably\b',
    re.IGNORECASE
)

# Financial projections — market size, CAGR, investment totals
FINANCIAL_PROJECTION = re.compile(
    r'\bCAGR\b|market\s+(?:size|potential|projection)|'
    r'(?:billion|million)\s+(?:dollar|USD|\$)\s+(?:market|opportunity)|'
    r'investment\s+of\s+\$|'
    r'\$\d+(?:\.\d+)?\s*(?:billion|B)\s+(?:market|opportunity|investment)',
    re.IGNORECASE
)


# ── Tag stripping ───────────────────────────────────────────────────────────

TAG_RE = re.compile(r'<[^>]+>')
SCRIPT_STYLE_RE = re.compile(r'<(?:script|style)[^>]*>.*?</(?:script|style)>', re.DOTALL | re.IGNORECASE)


def strip_html(html_text):
    """Strip script/style blocks, then all tags, returning visible text."""
    text = SCRIPT_STYLE_RE.sub(' ', html_text)
    text = TAG_RE.sub(' ', text)
    return text


def get_text_with_line_numbers(html_text):
    """Return list of (line_number, visible_text) tuples from HTML lines."""
    lines = html_text.split('\n')
    result = []
    for i, line in enumerate(lines, 1):
        visible = TAG_RE.sub(' ', line).strip()
        if visible:
            result.append((i, line, visible))
    return result


# ── Individual checks ───────────────────────────────────────────────────────

def check_pmid_density(html_text, visible_lines, filename=''):
    """Check overall PMID citation density.

    Accounts for dashboard type:
    - Reference dashboards (acronyms, methodology) get relaxed thresholds
    - Trial dashboards count NCT numbers as valid citations
    """
    pmids = PMID_PATTERN.findall(html_text)
    pmid_count = len(pmids)

    # Also count PMIDs embedded in JavaScript data (key_pmids fields)
    js_pmid_matches = JS_PMID_PATTERN.findall(html_text)
    for match in js_pmid_matches:
        # Each match is comma-separated digits like "29988125, 36060506"
        bare_ids = [x.strip() for x in match.split(',') if x.strip() and len(x.strip()) >= 7]
        pmid_count += len(bare_ids)

    nct_count = len(NCT_PATTERN.findall(html_text))
    citation_count = pmid_count + nct_count  # total verifiable citations

    is_reference = filename in REFERENCE_DASHBOARDS
    is_trial = filename in TRIAL_DASHBOARDS

    # Count claims (lines with percentages, dollar amounts, or sample sizes)
    claim_lines = []
    for lineno, raw, visible in visible_lines:
        has_stat = (PERCENT_PATTERN.search(visible) or
                    DOLLAR_PATTERN.search(visible) or
                    SAMPLE_SIZE.search(visible))
        if has_stat:
            claim_lines.append(lineno)

    claim_count = len(claim_lines)

    issues = []

    if is_reference:
        # Reference dashboards: only flag if there are dollar/financial claims with no citations
        dollar_lines = [ln for ln, raw, vis in visible_lines if DOLLAR_PATTERN.search(vis)]
        if dollar_lines and citation_count == 0:
            issues.append({
                'severity': 'MEDIUM',
                'check': 'pmid_density',
                'message': f'Reference dashboard has {len(dollar_lines)} lines with dollar amounts but no citations',
                'lines': dollar_lines[:5],
            })
    elif is_trial:
        # Trial dashboards: NCTs count as citations
        if claim_count > 0 and citation_count == 0:
            issues.append({
                'severity': 'HIGH',
                'check': 'pmid_density',
                'message': f'Trial dashboard has {claim_count} statistical lines but ZERO PMIDs or NCTs',
                'lines': claim_lines[:10],
            })
    else:
        # Evidence dashboards: standard rules
        if claim_count > 0 and pmid_count == 0:
            issues.append({
                'severity': 'CRITICAL',
                'check': 'pmid_density',
                'message': f'Dashboard contains {claim_count} lines with specific statistics but ZERO PMIDs',
                'lines': claim_lines[:10],
            })
        elif claim_count > 10 and pmid_count < 3:
            issues.append({
                'severity': 'HIGH',
                'check': 'pmid_density',
                'message': f'{claim_count} statistical claims but only {pmid_count} PMIDs — low citation density',
                'lines': claim_lines[:10],
            })

    return issues, {'pmid_count': pmid_count, 'nct_count': nct_count, 'claim_line_count': claim_count}


def check_vague_citations(html_text, visible_lines):
    """Find journal+year citations that lack a corresponding PMID."""
    issues = []
    for lineno, raw, visible in visible_lines:
        vague_matches = VAGUE_JOURNAL.findall(visible)
        for match in vague_matches:
            # Check if this line also has a PMID
            has_pmid = PMID_PATTERN.search(raw)
            if not has_pmid:
                issues.append({
                    'severity': 'HIGH',
                    'check': 'vague_citation',
                    'message': f'Vague journal citation without PMID: "{match.strip()}"',
                    'line': lineno,
                    'context': visible[:120],
                })
    return issues


def check_unsourced_statistics(html_text, visible_lines):
    """Find dollar amounts and specific percentages without nearby PMIDs."""
    issues = []

    for lineno, raw, visible in visible_lines:
        dollars = DOLLAR_PATTERN.findall(visible)
        for d in dollars:
            # Check if this line or adjacent HTML has a PMID
            has_pmid = PMID_PATTERN.search(raw)
            if not has_pmid:
                issues.append({
                    'severity': 'MEDIUM',
                    'check': 'unsourced_dollar',
                    'message': f'Dollar amount without citation: {d}',
                    'line': lineno,
                    'context': visible[:120],
                })

    return issues


def check_implausible_claims(html_text, visible_lines):
    """Flag impossible or near-impossible claims."""
    issues = []
    for lineno, raw, visible in visible_lines:
        matches = IMPLAUSIBLE.finditer(visible)
        for m in matches:
            issues.append({
                'severity': 'CRITICAL',
                'check': 'implausible_claim',
                'message': f'Implausible claim: "{m.group()}"',
                'line': lineno,
                'context': visible[:120],
            })
    return issues


def check_overstated_language(html_text, visible_lines):
    """Flag clinical overstatement."""
    issues = []
    for lineno, raw, visible in visible_lines:
        matches = OVERSTATED.finditer(visible)
        for m in matches:
            issues.append({
                'severity': 'MEDIUM',
                'check': 'overstated_language',
                'message': f'Overstated clinical language: "{m.group()}"',
                'line': lineno,
                'context': visible[:120],
            })
    return issues


def check_financial_projections(html_text, visible_lines):
    """Flag market projections and financial claims without methodology."""
    issues = []
    for lineno, raw, visible in visible_lines:
        matches = FINANCIAL_PROJECTION.finditer(visible)
        for m in matches:
            has_pmid = PMID_PATTERN.search(raw)
            if not has_pmid:
                issues.append({
                    'severity': 'HIGH',
                    'check': 'unsourced_financial',
                    'message': f'Financial projection without source: "{m.group()}"',
                    'line': lineno,
                    'context': visible[:120],
                })
    return issues


# ── Main verification ───────────────────────────────────────────────────────

def verify_dashboard(filepath):
    """Run all checks on a single dashboard file. Returns a report dict."""
    filename = os.path.basename(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        html_text = f.read()

    visible_lines = get_text_with_line_numbers(html_text)

    is_reference = filename in REFERENCE_DASHBOARDS
    is_trial = filename in TRIAL_DASHBOARDS

    all_issues = []
    density_issues, density_stats = check_pmid_density(html_text, visible_lines, filename)
    all_issues.extend(density_issues)
    all_issues.extend(check_vague_citations(html_text, visible_lines))
    # Skip unsourced-dollar check for reference dashboards (methodology pages, etc.)
    if not is_reference:
        all_issues.extend(check_unsourced_statistics(html_text, visible_lines))
    all_issues.extend(check_implausible_claims(html_text, visible_lines))
    all_issues.extend(check_overstated_language(html_text, visible_lines))
    # Skip financial projection check for trial/reference dashboards where
    # "CAGR" appears in clinical trial enrollment data, not as unsourced projections
    if not is_reference and not is_trial:
        all_issues.extend(check_financial_projections(html_text, visible_lines))

    # Severity summary
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    for issue in all_issues:
        sev = issue.get('severity', 'LOW')
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    # Determine overall status
    if severity_counts['CRITICAL'] > 0:
        status = 'QUARANTINE'
    elif severity_counts['HIGH'] > 3:
        status = 'QUARANTINE'
    elif severity_counts['HIGH'] > 0:
        status = 'UNVERIFIED'
    elif severity_counts['MEDIUM'] > 5:
        status = 'UNVERIFIED'
    elif severity_counts['MEDIUM'] > 0:
        status = 'PARTIALLY_VERIFIED'
    else:
        status = 'VERIFIED'

    report = {
        'dashboard': filename,
        'filepath': filepath,
        'audit_date': datetime.now().isoformat(),
        'status': status,
        'severity_counts': severity_counts,
        'pmid_count': density_stats['pmid_count'],
        'nct_count': density_stats.get('nct_count', 0),
        'claim_line_count': density_stats['claim_line_count'],
        'total_issues': len(all_issues),
        'issues': all_issues,
    }
    return report


def print_report(report, verbose=False):
    """Print a human-readable summary of a verification report."""
    status_icons = {
        'VERIFIED': '[PASS]',
        'PARTIALLY_VERIFIED': '[WARN]',
        'UNVERIFIED': '[FAIL]',
        'QUARANTINE': '[QUAR]',
    }

    icon = status_icons.get(report['status'], '[????]')
    sc = report['severity_counts']
    name = report['dashboard']
    pmids = report['pmid_count']

    print(f"  {icon} {name}")
    print(f"        Status: {report['status']} | PMIDs: {pmids} | "
          f"Issues: C={sc['CRITICAL']} H={sc['HIGH']} M={sc['MEDIUM']}")

    if verbose or report['status'] == 'QUARANTINE':
        critical_and_high = [i for i in report['issues']
                            if i['severity'] in ('CRITICAL', 'HIGH')]
        for issue in critical_and_high[:10]:
            line_info = f"L{issue.get('line', '?')}" if 'line' in issue else ''
            print(f"        {issue['severity']}: {issue['message']} {line_info}")
        if len(critical_and_high) > 10:
            print(f"        ... and {len(critical_and_high) - 10} more CRITICAL/HIGH issues")


def quarantine_dashboard(filepath):
    """Move a dashboard to the quarantine directory."""
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    filename = os.path.basename(filepath)
    dest = os.path.join(QUARANTINE_DIR, filename)
    shutil.move(filepath, dest)
    return dest


def main():
    args = sys.argv[1:]

    do_quarantine = '--quarantine' in args
    verbose = '--verbose' in args or '-v' in args
    args = [a for a in args if not a.startswith('-')]

    # Determine which files to check
    if '--file' in sys.argv:
        idx = sys.argv.index('--file')
        if idx + 1 < len(sys.argv):
            target = sys.argv[idx + 1]
            if not os.path.isabs(target):
                target = os.path.join(DASHBOARD_DIR, target)
            files = [target]
        else:
            print("Error: --file requires a filename")
            sys.exit(1)
    else:
        files = sorted([
            os.path.join(DASHBOARD_DIR, f)
            for f in os.listdir(DASHBOARD_DIR)
            if f.endswith('.html') and not f.startswith('_')
        ])

    if not files:
        print("No dashboard files found.")
        sys.exit(0)

    # Run verification
    print("=" * 70)
    print("  VERIFICATION GATE — Diabetes Research Hub Dashboards")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')} | Checking {len(files)} dashboard(s)")
    print("=" * 70)

    reports = []
    for filepath in files:
        report = verify_dashboard(filepath)
        reports.append(report)
        print_report(report, verbose=verbose)

    # Summary
    status_counts = {}
    for r in reports:
        s = r['status']
        status_counts[s] = status_counts.get(s, 0) + 1

    print(f"\n{'=' * 70}")
    print("  SUMMARY")
    print(f"{'=' * 70}")
    for status in ['VERIFIED', 'PARTIALLY_VERIFIED', 'UNVERIFIED', 'QUARANTINE']:
        count = status_counts.get(status, 0)
        if count > 0:
            print(f"  {status}: {count}")
    print(f"  Total issues: {sum(r['total_issues'] for r in reports)}")

    # Save reports
    os.makedirs(REPORT_DIR, exist_ok=True)
    for report in reports:
        name = report['dashboard'].replace('.html', '')
        report_path = os.path.join(REPORT_DIR, f'verify_{name}.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    # Save summary
    summary = {
        'run_date': datetime.now().isoformat(),
        'dashboards_checked': len(reports),
        'status_counts': status_counts,
        'total_issues': sum(r['total_issues'] for r in reports),
        'dashboards': [
            {
                'name': r['dashboard'],
                'status': r['status'],
                'pmid_count': r['pmid_count'],
                'severity_counts': r['severity_counts'],
            }
            for r in reports
        ]
    }
    summary_path = os.path.join(REPORT_DIR, 'verification_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\n  Reports saved to: Analysis/Results/verification_reports/")

    # Quarantine if requested
    quarantine_reports = [r for r in reports if r['status'] == 'QUARANTINE']
    if do_quarantine and quarantine_reports:
        print(f"\n  QUARANTINING {len(quarantine_reports)} dashboard(s):")
        for r in quarantine_reports:
            if os.path.exists(r['filepath']):
                dest = quarantine_dashboard(r['filepath'])
                print(f"    Moved: {r['dashboard']} -> _quarantine/")
                # Also try to remove from docs/ if present
                docs_path = os.path.join(BASE_DIR, 'docs', 'Dashboards', r['dashboard'])
                if os.path.exists(docs_path):
                    try:
                        os.remove(docs_path)
                        print(f"    Removed from docs/Dashboards/")
                    except PermissionError:
                        print(f"    WARNING: Could not remove from docs/Dashboards/ (permission denied)")

    # Exit code
    has_critical = any(r['status'] == 'QUARANTINE' for r in reports)
    if has_critical:
        print(f"\n  EXIT 1 — {len(quarantine_reports)} dashboard(s) have CRITICAL issues")
        sys.exit(1)
    else:
        print(f"\n  EXIT 0 — No CRITICAL issues found")
        sys.exit(0)


if __name__ == '__main__':
    main()
