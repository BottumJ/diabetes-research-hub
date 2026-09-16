#!/usr/bin/env python3
"""
weekly_platform_audit.py — reproducible weekly audit of the Diabetes Research Hub.

WHY THIS EXISTS AS A SCRIPT RATHER THAN A ONE-OFF DOCUMENT
----------------------------------------------------------
The weekly audit was previously produced by an assistant reading the tree and
writing prose. That has two defects this file closes:

  1. The numbers were not reproducible. "28 dashboards, 1147 PMIDs" could not be
     re-derived by anyone, including the next audit, so week-over-week deltas
     were assertions rather than measurements.
  2. It depended on a working remote sandbox. On 2026-09-13 the sandbox could
     not mount the repo at all (Windows update 2026-09-08 broke the Plan9
     share), and the audit could not run. A local script has no such dependency.

Run it:
    cd C:\\Users\\justi\\OneDrive\\Diabetes_Research
    python Analysis/Scripts/weekly_platform_audit.py

Outputs:
    Platform_Audit_Report.docx                       (current; previous copy archived)
    Analysis/Results/platform_audit_history.json     (machine-readable, for deltas)

Requires: python-docx  ->  pip install python-docx
"""

from __future__ import annotations

import html as html_mod
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from datetime import date, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC_DASH = os.path.join(ROOT, 'Dashboards')
PUB_DASH = os.path.join(ROOT, 'docs', 'Dashboards')
PUB_INDEX = os.path.join(ROOT, 'docs', 'index.html')
PUB_REPORTS = os.path.join(ROOT, 'docs', 'Reports')
RESULTS = os.path.join(ROOT, 'Analysis', 'Results')
HISTORY = os.path.join(RESULTS, 'platform_audit_history.json')
REPORT = os.path.join(ROOT, 'Platform_Audit_Report.docx')

TODAY = date.today()

# --- thresholds, stated once so the report can quote them -------------------
PMID_HIGH = 0      # zero PMIDs on a published dashboard -> HIGH
PMID_MEDIUM = 3    # fewer than this -> MEDIUM
CONTRAST_AA = 4.5  # WCAG 2.1 AA, normal text

# Dashboards that legitimately carry no citations of their own. Every exemption
# must be written by name and justified, per repo doctrine: an exemption list
# that grows silently is how a gate stops meaning anything.
PMID_EXEMPT = {
    'Acronym_Database.html': 'Terminology reference; expands abbreviations, asserts no findings.',
    'Prediction_Ledger.html': 'Registry of this project\'s own forward predictions; '
                              'resolution evidence is cited on resolution, not at entry.',
}

NAV_MARKER = '<!-- DRH-NAV-BAR -->'

RE_PMID_TEXT = re.compile(r'PMID[\s:]*([1-9]\d{5,8})')
RE_PMID_LINK = re.compile(r'href="https://pubmed\.ncbi\.nlm\.nih\.gov/([1-9]\d{5,8})/?"')
RE_PUBMED_ANY = re.compile(r'pubmed\.ncbi\.nlm\.nih\.gov/(\d+)')
RE_HOME = re.compile(r'class="drh-home"\s+href="([^"]+)"')
RE_NAVLINK = re.compile(r'<a href="([A-Za-z0-9_\-]+\.html)"')
RE_TABLE = re.compile(r'<table\b', re.I)
RE_TH = re.compile(r'<th\b', re.I)
RE_TABLE_LABELLED = re.compile(r'<table[^>]*(role="table"|aria-label=)', re.I)
RE_TABBTN = re.compile(r'role="tab"', re.I)
RE_INDEX_DASH = re.compile(r'href="Dashboards/([A-Za-z0-9_\-]+\.html)"')
RE_INDEX_REPORT = re.compile(r'href="(Reports/[A-Za-z0-9_\-.]+)"')
RE_LASTUPD = re.compile(r'Last updated:\s*(\d{4}-\d{2}-\d{2})')
RE_GENERATED = re.compile(r'\*\*Generated:\*\*\s*(\d{4}-\d{2}-\d{2})')
RE_LOOKBACK = re.compile(r'(?:Lookback period|rolling)\D{0,20}(\d{1,3})\s*[- ]?day', re.I)
RE_SNAPSHOT = re.compile(r'Snapshot:\s*(\d{4}-\d{2}-\d{2})')


# ---------------------------------------------------------------------------
# measurement
# ---------------------------------------------------------------------------

def read(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        return fh.read()


def block_context(text: str, pos: int) -> str:
    """Nearest enclosing list item / cell / paragraph text before `pos`.

    Used ONLY to surface duplicate-PMID review candidates. It is a heuristic on
    rendered HTML, not a parse of the citation store, so its output is labelled
    'candidate' everywhere and never gates.
    """
    start = max(text.rfind(tag, 0, pos) for tag in ('<li', '<td', '<p', '<div'))
    if start < 0:
        start = max(0, pos - 300)
    chunk = re.sub(r'<[^>]+>', ' ', text[start:pos])
    chunk = html_mod.unescape(chunk)
    return re.sub(r'\s+', ' ', chunk).strip()[-140:]


def audit_dashboard(path: str, published: bool) -> dict:
    name = os.path.basename(path)
    text = read(path)

    text_pmids = RE_PMID_TEXT.findall(text)
    link_pmids = RE_PMID_LINK.findall(text)
    any_pubmed = RE_PUBMED_ANY.findall(text)
    distinct = sorted(set(text_pmids) | set(link_pmids))

    # PMIDs mentioned in prose but never hyperlinked anywhere on the page.
    unlinked = sorted(set(text_pmids) - set(link_pmids))

    # Malformed pubmed hrefs: postprocess_dashboards.py emits /NNN/ ; anything
    # else (query strings, missing trailing slash, non-numeric) is drift.
    malformed = [m for m in re.findall(r'href="(https://pubmed\.ncbi\.nlm\.nih\.gov/[^"]*)"', text)
                 if not re.fullmatch(r'https://pubmed\.ncbi\.nlm\.nih\.gov/[1-9]\d{5,8}/', m)]

    # duplicate-PMID review candidates
    contexts = defaultdict(set)
    for m in RE_PMID_TEXT.finditer(text):
        contexts[m.group(1)].add(block_context(text, m.start()))
    dup_candidates = {p: sorted(c) for p, c in contexts.items() if len(c) > 1}

    home = RE_HOME.search(text)
    nav_targets = set()
    if NAV_MARKER in text:
        nav_end = text.find('</nav>', text.find(NAV_MARKER))
        nav_targets = set(RE_NAVLINK.findall(text[text.find(NAV_MARKER):nav_end if nav_end > 0 else None]))

    tables = len(RE_TABLE.findall(text))
    return {
        'name': name,
        'published': published,
        'bytes': os.path.getsize(path),
        'pmid_distinct': len(distinct),
        'pmid_linked': len(set(link_pmids)),
        'pmid_unlinked': unlinked,
        'pmid_malformed': malformed,
        'dup_candidates': dup_candidates,
        'has_nav': NAV_MARKER in text,
        'home_href': home.group(1) if home else None,
        'nav_crosslinks': len(nav_targets),
        'nav_targets': sorted(nav_targets),
        'tables': tables,
        'tables_with_th': len(RE_TH.findall(text)) > 0,
        'tables_labelled': len(RE_TABLE_LABELLED.findall(text)),
        'tab_roles': len(RE_TABBTN.findall(text)),
    }


def relative_luminance(hex_color: str) -> float:
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    srgb = [int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast_ratio(fg: str, bg: str) -> float:
    l1, l2 = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def days_since(iso: str) -> int | None:
    try:
        return (TODAY - datetime.strptime(iso, '%Y-%m-%d').date()).days
    except Exception:
        return None


def audit_site() -> dict:
    idx = read(PUB_INDEX)
    linked = RE_INDEX_DASH.findall(idx)
    linked_reports = RE_INDEX_REPORT.findall(idx)

    on_disk = {f for f in os.listdir(PUB_DASH) if f.endswith('.html')}
    dead = sorted(f for f in linked if f not in on_disk)
    orphan = sorted(on_disk - set(linked))
    dead_reports = sorted(r for r in linked_reports
                          if not os.path.exists(os.path.join(ROOT, 'docs', r)))

    last_upd = RE_LASTUPD.search(idx)
    reports = []
    if os.path.isdir(PUB_REPORTS):
        for fn in sorted(os.listdir(PUB_REPORTS)):
            body = read(os.path.join(PUB_REPORTS, fn))
            gen = RE_GENERATED.search(body)
            look = RE_LOOKBACK.search(body)
            age = days_since(gen.group(1)) if gen else None
            window = int(look.group(1)) if look else None
            reports.append({
                'file': fn, 'generated': gen.group(1) if gen else None,
                'age_days': age, 'declared_window_days': window,
                'exceeds_window': (age is not None and window is not None and age > window),
            })

    ct = os.path.join(PUB_DASH, 'Clinical_Trial_Dashboard.html')
    snap = RE_SNAPSHOT.search(read(ct)) if os.path.exists(ct) else None

    return {
        'dashboards_linked': len(linked),
        'dashboards_on_disk': len(on_disk),
        'dead_dashboard_links': dead,
        'orphan_dashboards': orphan,
        'dead_report_links': dead_reports,
        'index_last_updated': last_upd.group(1) if last_upd else None,
        'index_age_days': days_since(last_upd.group(1)) if last_upd else None,
        'reports': reports,
        'trial_snapshot': snap.group(1) if snap else None,
        'trial_snapshot_age_days': days_since(snap.group(1)) if snap else None,
    }


def audit_collab() -> dict:
    gh = os.path.join(ROOT, '.github', 'ISSUE_TEMPLATE')
    templates = sorted(os.listdir(gh)) if os.path.isdir(gh) else []
    citation_cff = os.path.exists(os.path.join(ROOT, 'CITATION.cff'))
    contributing = os.path.join(ROOT, 'CONTRIBUTING.md')
    cite_block = False
    if os.path.exists(contributing):
        body = read(contributing).lower()
        cite_block = ('cite this' in body or 'citation' in body)
    readme = os.path.join(ROOT, 'README.md')
    readme_cite = False
    if os.path.exists(readme):
        readme_cite = 'cite' in read(readme).lower()
    return {
        'contributing': os.path.exists(contributing),
        'citation_cff': citation_cff,
        'citation_in_contributing': cite_block,
        'citation_in_readme': readme_cite,
        'issue_templates': templates,
        'pr_template': os.path.exists(os.path.join(ROOT, '.github', 'pull_request_template.md')),
        'code_of_conduct': os.path.exists(os.path.join(ROOT, 'CODE_OF_CONDUCT.md')),
    }


def collect() -> dict:
    src = [audit_dashboard(os.path.join(SRC_DASH, f), False)
           for f in sorted(os.listdir(SRC_DASH)) if f.endswith('.html')]
    pub = [audit_dashboard(os.path.join(PUB_DASH, f), True)
           for f in sorted(os.listdir(PUB_DASH)) if f.endswith('.html')]

    src_by = {d['name']: d for d in src}
    for d in pub:
        s = src_by.get(d['name'])
        d['source_has_nav'] = s['has_nav'] if s else None
        d['source_missing'] = s is None
        d['nav_regression_pending'] = bool(s and d['has_nav'] and not s['has_nav'])

    return {
        'generated': TODAY.isoformat(),
        'source': src,
        'published': pub,
        'site': audit_site(),
        'collab': audit_collab(),
        'contrast_muted_on_bg': round(contrast_ratio('#636363', '#fafaf7'), 2),
    }


# ---------------------------------------------------------------------------
# findings
# ---------------------------------------------------------------------------

def classify(data: dict) -> list[dict]:
    """Every finding carries a severity, a measurement, and what would clear it."""
    out = []
    pub, site, collab = data['published'], data['site'], data['collab']

    pending = [d['name'] for d in pub if d['nav_regression_pending']]
    if pending:
        out.append(dict(
            sev='HIGH', area='Navigation',
            title='Nav bar is live on the site but absent from the source file',
            detail=(f'{len(pending)} of {len(pub)} published dashboards carry the nav bar while '
                    f'their Dashboards/ source does not. postprocess_dashboards.py injects nav '
                    f'into Dashboards/*.html and sync_docs_dashboards.py publishes afterwards, so '
                    f'this state means builders have rewritten the source since the last '
                    f'postprocess pass. The next syncdocs publishes {len(pending)} dashboards '
                    f'with no nav and no back-link.'),
            evidence=', '.join(pending),
            fix=('Run the full pipeline (postprocess then syncdocs), and add a pre-sync assertion '
                 'that every Dashboards/*.html contains the DRH-NAV-BAR marker. linkgate checks '
                 'docs/ only, which is why this class is invisible today.')))

    nonav_pub = [d['name'] for d in pub if not d['has_nav']]
    if nonav_pub:
        out.append(dict(sev='HIGH', area='Navigation',
                        title='Published dashboard with no navigation bar',
                        detail=f'{len(nonav_pub)} published dashboards have no nav bar.',
                        evidence=', '.join(nonav_pub),
                        fix='Re-run postprocess_dashboards.py then sync_docs_dashboards.py.'))

    bad_home = [f"{d['name']} -> {d['home_href']}" for d in pub
                if d['has_nav'] and d['home_href'] != '../index.html']
    if bad_home:
        out.append(dict(sev='HIGH', area='Navigation',
                        title='Back-link does not resolve from the published depth',
                        detail='Published dashboards sit at docs/Dashboards/, so the hub '
                               'back-link must be ../index.html.',
                        evidence='; '.join(bad_home), fix='Fix depth rewrite in sync_docs_dashboards.py.'))

    zero = [d['name'] for d in pub
            if d['pmid_distinct'] == PMID_HIGH and d['name'] not in PMID_EXEMPT]
    if zero:
        out.append(dict(sev='HIGH', area='Citations',
                        title='Published dashboard asserts findings with zero PMIDs',
                        detail=f'{len(zero)} dashboards carry no citation at all and are not on '
                               f'the named exemption list.',
                        evidence=', '.join(zero),
                        fix='Cite the evidence, or add the file to PMID_EXEMPT with a written reason.'))

    thin = [f"{d['name']} ({d['pmid_distinct']})" for d in pub
            if PMID_HIGH < d['pmid_distinct'] < PMID_MEDIUM and d['name'] not in PMID_EXEMPT]
    if thin:
        out.append(dict(sev='MEDIUM', area='Citations',
                        title=f'Published dashboard with fewer than {PMID_MEDIUM} distinct PMIDs',
                        detail='Thin citation base relative to the claims made.',
                        evidence=', '.join(thin), fix='Broaden the evidence base or soften the claims.'))

    unlinked = [(d['name'], len(d['pmid_unlinked'])) for d in pub if d['pmid_unlinked']]
    if unlinked:
        total = sum(n for _, n in unlinked)
        out.append(dict(sev='MEDIUM', area='Citations',
                        title='PMID cited in prose but never hyperlinked',
                        detail=f'{total} distinct PMIDs across {len(unlinked)} published dashboards '
                               f'appear as bare text. A reader cannot check them in one click, '
                               f'which is the entire point of publishing the identifier.',
                        evidence=', '.join(f'{n} ({c})' for n, c in sorted(unlinked, key=lambda x: -x[1])[:12]),
                        fix='convert_pmid_to_links() in postprocess_dashboards.py already does this; '
                            'it has not been run over the current build.'))

    malformed = [(d['name'], d['pmid_malformed']) for d in pub if d['pmid_malformed']]
    if malformed:
        out.append(dict(sev='MEDIUM', area='Citations',
                        title='PubMed href does not match the canonical form',
                        detail='Expected https://pubmed.ncbi.nlm.nih.gov/{pmid}/ exactly.',
                        evidence='; '.join(f'{n}: {v[0]}' for n, v in malformed[:8]),
                        fix='Normalise in postprocess_dashboards.py.'))

    dups = [(d['name'], p, ctx) for d in pub for p, ctx in d['dup_candidates'].items()]
    if dups:
        out.append(dict(sev='MEDIUM', area='Citations',
                        title='Duplicate-PMID review candidates (heuristic, not a gate)',
                        detail=f'{len(dups)} cases where one PMID appears in two or more '
                               f'materially different surrounding blocks on the same page. Most '
                               f'will be the same paper cited twice, which is fine. The ones that '
                               f'matter are where the two blocks describe different studies.',
                        evidence='; '.join(f'{n} PMID {p}' for n, p, _ in dups[:10]),
                        fix='Human review. audit_citation_identifiers.py is the authoritative check.'))

    if site['dead_dashboard_links']:
        out.append(dict(sev='HIGH', area='Navigation',
                        title='Landing page links to a dashboard that does not exist',
                        detail='404 for every reader who clicks it.',
                        evidence=', '.join(site['dead_dashboard_links']),
                        fix='Build the dashboard or remove the card.'))
    if site['dead_report_links']:
        out.append(dict(sev='HIGH', area='Navigation', title='Landing page links to a missing report',
                        detail='', evidence=', '.join(site['dead_report_links']),
                        fix='sync_docs_reports.py should publish it.'))
    if site['orphan_dashboards']:
        out.append(dict(sev='MEDIUM', area='Navigation',
                        title='Published dashboard not listed on the landing page',
                        detail='Reachable only by guessing the URL, so effectively unpublished.',
                        evidence=', '.join(site['orphan_dashboards']),
                        fix='Add a card in rebuild_website.py, or delete the file.'))

    for r in site['reports']:
        if r['exceeds_window']:
            out.append(dict(sev='HIGH', area='Freshness',
                            title=f"{r['file']} is older than the window it advertises",
                            detail=f"Generated {r['generated']} ({r['age_days']}d ago); declares a "
                                   f"{r['declared_window_days']}-day window.",
                            evidence=r['file'], fix='Re-run the pipeline; audit_report_freshness.py gates this.'))

    if site['index_age_days'] is not None and site['index_age_days'] > 7:
        out.append(dict(sev='MEDIUM', area='Freshness',
                        title='Daily pipeline has not run in over a week',
                        detail=f"docs/index.html declares Last updated: {site['index_last_updated']} "
                               f"({site['index_age_days']} days ago). The pipeline is scheduled daily.",
                        evidence='docs/index.html',
                        fix='Check register_daily_task.ps1 / run_daily_pipeline.ps1 on the host.'))

    if site['trial_snapshot_age_days'] is not None and site['trial_snapshot_age_days'] > 30:
        out.append(dict(sev='MEDIUM', area='Freshness',
                        title='Clinical trial snapshot is over 30 days old',
                        detail=f"Snapshot {site['trial_snapshot']} "
                               f"({site['trial_snapshot_age_days']} days). Trial counts quoted in "
                               f"outreach material inherit this age.",
                        evidence='Clinical_Trial_Dashboard.html',
                        fix='Re-run baseline_clinical_trials.py and rebuild_clinical_trial_dashboard.py.'))

    unlabelled = [d['name'] for d in pub if d['tables'] and d['tables_labelled'] < d['tables']]
    if unlabelled:
        out.append(dict(sev='LOW', area='Accessibility',
                        title='Table without role/aria-label',
                        detail=f'{len(unlabelled)} published dashboards contain at least one table '
                               f'lacking role="table" or aria-label.',
                        evidence=', '.join(unlabelled[:12]),
                        fix='add_aria_labels() in postprocess_dashboards.py covers this.'))
    noth = [d['name'] for d in pub if d['tables'] and not d['tables_with_th']]
    if noth:
        out.append(dict(sev='MEDIUM', area='Accessibility',
                        title='Table rendered without header cells',
                        detail='Screen readers announce no column context.',
                        evidence=', '.join(noth), fix='Emit <thead><th> in the builder.'))

    cr = data['contrast_muted_on_bg']
    if cr < CONTRAST_AA:
        out.append(dict(sev='MEDIUM', area='Accessibility',
                        title='Muted text fails WCAG AA',
                        detail=f'#636363 on #fafaf7 measures {cr}:1 against a {CONTRAST_AA}:1 floor.',
                        evidence='nav group labels, figure notes', fix='Darken muted to #595959 or below.'))

    if not collab['contributing']:
        out.append(dict(sev='HIGH', area='Collaboration', title='CONTRIBUTING.md missing',
                        detail='', evidence='repo root', fix='Add one.'))
    if not (collab['citation_cff'] or collab['citation_in_readme'] or collab['citation_in_contributing']):
        out.append(dict(sev='MEDIUM', area='Collaboration',
                        title='No machine-readable citation format',
                        detail='Nothing tells an academic how to cite this platform. CITATION.cff '
                               'is what GitHub reads to render a "Cite this repository" button.',
                        evidence='no CITATION.cff', fix='Add CITATION.cff with the OSF DOI.'))
    elif not collab['citation_cff']:
        out.append(dict(sev='LOW', area='Collaboration',
                        title='Citation guidance exists only as prose',
                        detail='A CITATION.cff would make it machine-readable and surface GitHub\'s '
                               '"Cite this repository" button.',
                        evidence='CONTRIBUTING.md / README.md', fix='Add CITATION.cff.'))
    if not collab['issue_templates']:
        out.append(dict(sev='MEDIUM', area='Collaboration', title='No GitHub issue templates',
                        detail='', evidence='.github/ISSUE_TEMPLATE', fix='Add templates.'))
    if not collab['pr_template']:
        out.append(dict(sev='LOW', area='Collaboration', title='No pull request template',
                        detail='Issue templates exist; the PR path has no equivalent checklist.',
                        evidence='.github/pull_request_template.md', fix='Add one.'))
    if not collab['code_of_conduct']:
        out.append(dict(sev='LOW', area='Collaboration', title='No CODE_OF_CONDUCT.md',
                        detail='Commonly expected for an open collaboration invitation.',
                        evidence='repo root', fix='Adopt Contributor Covenant.'))

    order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    return sorted(out, key=lambda f: (order[f['sev']], f['area']))


def load_previous() -> dict | None:
    if not os.path.exists(HISTORY):
        return None
    try:
        hist = json.load(open(HISTORY, encoding='utf-8'))
        return hist[-1] if hist else None
    except Exception:
        return None


def save_history(data: dict, findings: list[dict]) -> None:
    os.makedirs(RESULTS, exist_ok=True)
    hist = []
    if os.path.exists(HISTORY):
        try:
            hist = json.load(open(HISTORY, encoding='utf-8'))
        except Exception:
            hist = []
    hist.append({
        'date': data['generated'],
        'published_count': len(data['published']),
        'source_count': len(data['source']),
        'total_bytes': sum(d['bytes'] for d in data['published']),
        'pmid_total': sum(d['pmid_distinct'] for d in data['published']),
        'nav_coverage_published': sum(1 for d in data['published'] if d['has_nav']),
        'nav_coverage_source': sum(1 for d in data['source'] if d['has_nav']),
        'high': sum(1 for f in findings if f['sev'] == 'HIGH'),
        'medium': sum(1 for f in findings if f['sev'] == 'MEDIUM'),
        'low': sum(1 for f in findings if f['sev'] == 'LOW'),
        'titles': [f"{f['sev']}: {f['title']}" for f in findings],
    })
    json.dump(hist[-52:], open(HISTORY, 'w', encoding='utf-8'), indent=2)


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

def build_docx(data: dict, findings: list[dict], prev: dict | None) -> None:
    try:
        from docx import Document
        from docx.enum.table import WD_TABLE_ALIGNMENT
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt, RGBColor
    except ImportError:
        sys.exit('python-docx is required:  pip install python-docx')

    INK = RGBColor(0x1A, 0x1A, 0x1A)
    MUTED = RGBColor(0x59, 0x59, 0x59)
    RULE = 'D8D4CC'

    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.25)
        s.right_margin = Inches(1.25)

    normal = doc.styles['Normal']
    normal.font.name = 'Georgia'
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = INK
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = 1.25

    def hrule(p):
        pPr = p._p.get_or_add_pPr()
        bd = OxmlElement('w:pBdr')
        bot = OxmlElement('w:bottom')
        bot.set(qn('w:val'), 'single')
        bot.set(qn('w:sz'), '4')
        bot.set(qn('w:space'), '4')
        bot.set(qn('w:color'), RULE)
        bd.append(bot)
        pPr.append(bd)

    def heading(text, size=14, space_before=18, rule=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.font.bold = False
        r.font.name = 'Georgia'
        r.font.color.rgb = INK
        if rule:
            hrule(p)
        return p

    def small(text, italic=True):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        r = p.add_run(text)
        r.font.size = Pt(8.5)
        r.font.italic = italic
        r.font.color.rgb = MUTED
        return p

    def plain_table(headers, rows, widths=None):
        """Tufte: horizontal rules only, no vertical lines, no fill."""
        t = doc.add_table(rows=1, cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        t.style = 'Table Grid'
        # strip all borders, then add a rule under the header row only
        tblPr = t._tbl.tblPr
        borders = OxmlElement('w:tblBorders')
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            e = OxmlElement(f'w:{edge}')
            e.set(qn('w:val'), 'single' if edge in ('top', 'bottom', 'insideH') else 'none')
            e.set(qn('w:sz'), '4')
            e.set(qn('w:color'), RULE)
            borders.append(e)
        tblPr.append(borders)

        for i, h in enumerate(headers):
            cell = t.rows[0].cells[i]
            cell.text = ''
            r = cell.paragraphs[0].add_run(h)
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.name = 'Georgia'
        for row in rows:
            cells = t.add_row().cells
            for i, v in enumerate(row):
                cells[i].text = ''
                r = cells[i].paragraphs[0].add_run(str(v))
                r.font.size = Pt(8.5)
                r.font.name = 'Consolas' if i and str(v).replace('.', '').isdigit() else 'Georgia'
        if widths:
            for row in t.rows:
                for i, w in enumerate(widths):
                    row.cells[i].width = Inches(w)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        return t

    pub, site, collab = data['published'], data['site'], data['collab']
    highs = [f for f in findings if f['sev'] == 'HIGH']
    meds = [f for f in findings if f['sev'] == 'MEDIUM']
    lows = [f for f in findings if f['sev'] == 'LOW']

    # --- title -------------------------------------------------------------
    p = doc.add_paragraph()
    r = p.add_run('Diabetes Research Hub — Platform Audit')
    r.font.size = Pt(19)
    r.font.name = 'Georgia'
    r.font.color.rgb = INK
    p.paragraph_format.space_after = Pt(2)
    hrule(p)
    small(f"Week of {data['generated']}  ·  bottumj.github.io/diabetes-research-hub  ·  "
          f"generated by Analysis/Scripts/weekly_platform_audit.py")

    # --- executive summary -------------------------------------------------
    heading('Executive summary', 14, 12)
    nav_pub = sum(1 for d in pub if d['has_nav'])
    nav_src = sum(1 for d in data['source'] if d['has_nav'])
    total_mb = sum(d['bytes'] for d in pub) / 1_048_576

    delta = ''
    if prev:
        dh = len(highs) - prev.get('high', 0)
        delta = (f"  Previous audit {prev['date']}: {prev.get('high', 0)} high, "
                 f"{prev.get('medium', 0)} medium, {prev.get('low', 0)} low "
                 f"({dh:+d} high this week).")

    doc.add_paragraph(
        f"{len(pub)} dashboards are published under docs/ totalling {total_mb:.1f} MB, carrying "
        f"{sum(d['pmid_distinct'] for d in pub)} distinct PMID citations. "
        f"{len(highs)} high-priority, {len(meds)} medium and {len(lows)} low-priority findings "
        f"are open.{delta}")

    plain_table(
        ['Check', 'Result', 'Status'],
        [
            ['Published dashboards', len(pub), 'pass'],
            ['Nav bar, published copies', f"{nav_pub}/{len(pub)}", 'pass' if nav_pub == len(pub) else 'FAIL'],
            ['Nav bar, source copies', f"{nav_src}/{len(data['source'])}",
             'pass' if nav_src == len(data['source']) else 'FAIL'],
            ['Landing-page links resolve',
             f"{site['dashboards_linked'] - len(site['dead_dashboard_links'])}/{site['dashboards_linked']}",
             'pass' if not site['dead_dashboard_links'] else 'FAIL'],
            ['Dashboards listed on landing page',
             f"{site['dashboards_on_disk'] - len(site['orphan_dashboards'])}/{site['dashboards_on_disk']}",
             'pass' if not site['orphan_dashboards'] else 'FAIL'],
            ['Dashboards with zero PMIDs',
             sum(1 for d in pub if d['pmid_distinct'] == 0 and d['name'] not in PMID_EXEMPT),
             'pass' if not any(d['pmid_distinct'] == 0 and d['name'] not in PMID_EXEMPT for d in pub) else 'FAIL'],
            ['Muted text contrast (AA ≥ 4.5:1)', f"{data['contrast_muted_on_bg']}:1",
             'pass' if data['contrast_muted_on_bg'] >= CONTRAST_AA else 'FAIL'],
            ['CONTRIBUTING.md', 'present' if collab['contributing'] else 'absent',
             'pass' if collab['contributing'] else 'FAIL'],
            ['Issue templates', len(collab['issue_templates']),
             'pass' if collab['issue_templates'] else 'FAIL'],
            ['CITATION.cff', 'present' if collab['citation_cff'] else 'absent',
             'pass' if collab['citation_cff'] else 'FAIL'],
        ], widths=[3.2, 1.5, 1.1])

    # --- priority actions --------------------------------------------------
    heading('Priority actions', 14, 18, rule=True)
    for sev, group in (('HIGH', highs), ('MEDIUM', meds), ('LOW', lows)):
        if not group:
            continue
        heading(sev, 11, 10)
        for i, f in enumerate(group, 1):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.left_indent = Inches(0.2)
            r = p.add_run(f"{i}. {f['title']}  ")
            r.font.bold = True
            r.font.size = Pt(10)
            r2 = p.add_run(f"[{f['area']}]")
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = MUTED
            if f['detail']:
                q = doc.add_paragraph()
                q.paragraph_format.left_indent = Inches(0.45)
                q.paragraph_format.space_after = Pt(2)
                rr = q.add_run(f['detail'])
                rr.font.size = Pt(9.5)
            if f['evidence']:
                q = doc.add_paragraph()
                q.paragraph_format.left_indent = Inches(0.45)
                q.paragraph_format.space_after = Pt(2)
                rr = q.add_run(f"Evidence: {f['evidence']}")
                rr.font.size = Pt(8.5)
                rr.font.color.rgb = MUTED
            q = doc.add_paragraph()
            q.paragraph_format.left_indent = Inches(0.45)
            q.paragraph_format.space_after = Pt(9)
            rr = q.add_run(f"Clears when: {f['fix']}")
            rr.font.size = Pt(8.5)
            rr.font.italic = True
            rr.font.color.rgb = MUTED

    # --- dashboard table ---------------------------------------------------
    doc.add_page_break()
    heading('Dashboard status', 14, 0, rule=True)
    small('One row per published dashboard. "Src nav" is the Dashboards/ source copy; '
          'where it reads no while "Nav" reads yes, the next publish removes the nav bar.')
    rows = []
    for d in sorted(pub, key=lambda x: -x['pmid_distinct']):
        issues = []
        if not d['has_nav']:
            issues.append('no nav')
        if d['nav_regression_pending']:
            issues.append('src nav lost')
        if d['pmid_distinct'] == 0 and d['name'] not in PMID_EXEMPT:
            issues.append('no PMIDs')
        if d['pmid_unlinked']:
            issues.append(f"{len(d['pmid_unlinked'])} unlinked")
        if d['tables'] and not d['tables_with_th']:
            issues.append('no <th>')
        pri = 'HIGH' if ('no nav' in issues or 'no PMIDs' in issues or 'src nav lost' in issues) \
            else ('MED' if issues else '—')
        rows.append([
            d['name'].replace('.html', ''),
            f"{d['bytes'] / 1024:.0f}K",
            d['pmid_distinct'],
            'yes' if d['has_nav'] else 'NO',
            'yes' if d['source_has_nav'] else 'NO',
            ', '.join(issues) if issues else 'clean',
            pri,
        ])
    plain_table(['Dashboard', 'Size', 'PMIDs', 'Nav', 'Src nav', 'Issues', 'Pri'], rows,
                widths=[1.75, 0.5, 0.5, 0.4, 0.5, 1.75, 0.5])

    # --- detail by area ----------------------------------------------------
    doc.add_page_break()
    heading('Findings by area', 14, 0, rule=True)
    for area in ('Navigation', 'Citations', 'Build integrity', 'Freshness', 'Accessibility', 'Collaboration'):
        heading(area, 12, 14)
        group = [f for f in findings if f['area'] == area]
        if area == 'Build integrity':
            doc.add_paragraph(
                'run_quality_improvements.py defines 71 pipeline stages. This audit does not '
                'execute them — running the full pipeline makes several hundred live PubMed and '
                'ClinicalTrials.gov calls and rewrites the repo, which an audit must not do. '
                'Build integrity is instead inferred from the artefacts on disk, and the '
                'inference is stated rather than assumed: the nav and PMID-link gaps below are '
                'what a pipeline that has not completed a postprocess pass looks like from the '
                'outside. Run the pipeline separately and read its own SUMMARY block for '
                'stage-level pass/fail.')
            doc.add_paragraph(
                f"docs/index.html declares Last updated: {site['index_last_updated']} "
                f"({site['index_age_days']} days ago). Clinical trial snapshot: "
                f"{site['trial_snapshot']} ({site['trial_snapshot_age_days']} days).")
        if not group:
            if area != 'Build integrity':
                small('No findings.', italic=True)
            continue
        for f in group:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(f"{f['sev']} — {f['title']}")
            r.font.bold = True
            r.font.size = Pt(10)
            if f['detail']:
                doc.add_paragraph(f['detail']).runs[0].font.size = Pt(9.5)
            if f['evidence']:
                q = doc.add_paragraph()
                rr = q.add_run(f"Evidence: {f['evidence']}")
                rr.font.size = Pt(8.5)
                rr.font.color.rgb = MUTED

    # --- freshness table ---------------------------------------------------
    heading('Published report freshness', 12, 16)
    plain_table(['Report', 'Generated', 'Age (d)', 'Declared window', 'Within window'],
                [[r['file'], r['generated'] or '—', r['age_days'] if r['age_days'] is not None else '—',
                  f"{r['declared_window_days']}d" if r['declared_window_days'] else '—',
                  'no' if r['exceeds_window'] else 'yes'] for r in site['reports']],
                widths=[2.0, 1.1, 0.7, 1.2, 1.0])

    # --- method ------------------------------------------------------------
    heading('Method and limits', 12, 18, rule=True)
    doc.add_paragraph(
        'Every number in this report is produced by weekly_platform_audit.py reading the working '
        'tree, and can be re-derived by re-running it. Three things it deliberately does not do, '
        'stated so no one reads more into a clean result than is there:')
    for lim in (
        'It does not execute the build pipeline (see Build integrity above).',
        'It does not verify that a PMID resolves, is on topic, or has been retracted. The repo '
        'has fourteen gates for that; this audit checks only that citations are present, '
        'well-formed and clickable.',
        'It reads the working tree, not origin. A reader loads origin/main:docs/. '
        'audit_publish_reachability.py is the stage that compares the two, and its verdict is the '
        'one that decides whether anything here reached an actual reader.',
    ):
        q = doc.add_paragraph(lim, style='List Bullet')
        q.runs[0].font.size = Pt(9.5)

    if prev:
        heading('Change since last audit', 12, 16)
        plain_table(['Metric', prev['date'], data['generated']],
                    [['Published dashboards', prev.get('published_count', '—'), len(pub)],
                     ['Total size (MB)', f"{prev.get('total_bytes', 0) / 1048576:.1f}", f"{total_mb:.1f}"],
                     ['PMID citations', prev.get('pmid_total', '—'), sum(d['pmid_distinct'] for d in pub)],
                     ['Nav coverage (published)', prev.get('nav_coverage_published', '—'), nav_pub],
                     ['Nav coverage (source)', prev.get('nav_coverage_source', '—'), nav_src],
                     ['HIGH findings', prev.get('high', '—'), len(highs)],
                     ['MEDIUM findings', prev.get('medium', '—'), len(meds)]],
                    widths=[2.4, 1.4, 1.4])
    else:
        small('No prior machine-readable audit found. This run establishes the baseline in '
              'Analysis/Results/platform_audit_history.json; next week\'s report will show deltas.')

    if os.path.exists(REPORT):
        archive = os.path.join(ROOT, f'Platform_Audit_Report_{TODAY.isoformat()}.docx')
        if not os.path.exists(archive):
            shutil.copy2(REPORT, archive)
    doc.save(REPORT)


def main() -> None:
    for d in (SRC_DASH, PUB_DASH):
        if not os.path.isdir(d):
            sys.exit(f'Not found: {d}. Run from the repository root.')
    data = collect()
    findings = classify(data)
    prev = load_previous()
    build_docx(data, findings, prev)
    save_history(data, findings)

    h = sum(1 for f in findings if f['sev'] == 'HIGH')
    m = sum(1 for f in findings if f['sev'] == 'MEDIUM')
    l = sum(1 for f in findings if f['sev'] == 'LOW')
    print(f'Platform_Audit_Report.docx written — {h} HIGH, {m} MEDIUM, {l} LOW')
    for f in findings:
        if f['sev'] == 'HIGH':
            print(f"  HIGH  {f['title']}")
    sys.exit(1 if h else 0)


if __name__ == '__main__':
    main()
