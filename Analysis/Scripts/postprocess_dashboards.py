#!/usr/bin/env python3
"""
Post-process all dashboard HTML files to ensure consistent:
  1. Navigation bar with hub back-link and cross-dashboard links
  2. ARIA labels on interactive elements (tabs, buttons, tables)
  3. PMID text → PubMed hyperlinks

Runs after all build scripts. Idempotent — safe to run multiple times.
"""

import os
import re
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
DASHBOARDS_DIR = os.path.join(BASE_DIR, 'Dashboards')

# ─── Dashboard registry for cross-navigation ───────────────────────────
# Grouped by category for the nav bar dropdown
DASHBOARD_GROUPS = {
    "Core Tools": [
        ("Research Dashboard", "Research_Dashboard.html"),
        ("Clinical Trials", "Clinical_Trial_Dashboard.html"),
        ("Data Dictionary", "Medical_Data_Dictionary.html"),
        ("Paper Library", "Paper_Library.html"),
        ("Methodology", "Methodology.html"),
        ("Acronym Database", "Acronym_Database.html"),
    ],
    "Analysis": [
        ("Gap Synthesis", "Gap_Synthesis.html"),
        ("Gap Deep Dives", "Gap_Deep_Dives.html"),
        ("Gap Evidence", "Gap_Evidence.html"),
        ("Extracted Evidence", "Extracted_Evidence.html"),
        ("Corpus Analysis", "Corpus_Analysis.html"),
        ("Research Paths", "Research_Paths.html"),
        ("Statistical Analysis", "Statistical_Analysis.html"),
    ],
    "Drug & Treatment": [
        ("Drug Repurposing Screen", "Drug_Repurposing_Screen.html"),
        ("Drug Repurposing Islet", "Drug_Repurposing_Islet.html"),
        ("Islet Drug Repurposing", "Islet_Drug_Repurposing.html"),
        ("Generic Drug Catalog", "Generic_Drug_Catalog.html"),
        ("GKA Landscape", "GKA_Landscape.html"),
        ("GKA LADA", "GKA_LADA.html"),
        ("GKA Pricing", "GKA_Pricing.html"),
        ("Immunomod LADA", "Immunomod_LADA.html"),
    ],
    "Equity & Access": [
        ("Health Equity", "Health_Equity.html"),
        ("Equity Map", "Equity_Map.html"),
        ("Trial Equity Mapper", "Trial_Equity_Mapper.html"),
        ("CART Access Barriers", "CART_Access_Barriers.html"),
        ("Islet Transplant Equity", "Islet_Transplant_Equity.html"),
    ],
    "LADA & Nutrition": [
        ("LADA Natural History", "LADA_Natural_History.html"),
        ("LADA Prevalence", "LADA_Prevalence.html"),
        ("LADA Diagnostic Model", "LADA_Diagnostic_Model.html"),
        ("Nutrition Beta Cells", "Nutrition_Beta_Cells.html"),
        ("Nutrition LADA", "Nutrition_LADA.html"),
        ("Treg Neuropathy", "Treg_Neuropathy.html"),
        ("Islet Transplant Analysis", "Islet_Transplant_Analysis.html"),
    ],
    "Verification": [
        ("PMID Verification", "PMID_Verification.html"),
    ],
}

# ─── Navigation bar HTML/CSS ───────────────────────────────────────────
NAV_MARKER = '<!-- DRH-NAV-BAR -->'

def build_nav_css():
    return """
/* ── DRH Navigation Bar ── */
.drh-nav { background:#fff; border-bottom:1px solid #e0ddd5; padding:0 2rem; display:flex; align-items:center; gap:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; font-size:13px; position:relative; z-index:1000; flex-wrap:wrap; }
.drh-nav a.drh-home { color:#2c5f8a; text-decoration:none; font-weight:600; padding:10px 16px 10px 0; border-right:1px solid #e0ddd5; margin-right:8px; white-space:nowrap; }
.drh-nav a.drh-home:hover { color:#1a4a6e; }
.drh-nav .drh-group { position:relative; }
.drh-nav .drh-group-label { color:#636363; cursor:pointer; padding:10px 12px; border:none; background:none; font-size:13px; font-family:inherit; }
.drh-nav .drh-group-label:hover { color:#1a1a1a; background:#f5f5f0; }
.drh-nav .drh-dropdown { display:none; position:absolute; top:100%; left:0; background:#fff; border:1px solid #e0ddd5; box-shadow:0 4px 12px rgba(0,0,0,0.08); min-width:220px; z-index:1001; }
.drh-nav .drh-group:hover .drh-dropdown { display:block; }
.drh-nav .drh-dropdown a { display:block; padding:8px 16px; color:#1a1a1a; text-decoration:none; font-size:13px; white-space:nowrap; }
.drh-nav .drh-dropdown a:hover { background:#f5f5f0; color:#2c5f8a; }
.drh-nav .drh-dropdown a.drh-current { background:#f0f4f8; color:#2c5f8a; font-weight:600; }
"""

def build_nav_html(current_file):
    groups_html = []
    for group_name, dashboards in DASHBOARD_GROUPS.items():
        links = []
        for label, filename in dashboards:
            css_class = ' class="drh-current"' if filename == current_file else ''
            links.append(f'      <a href="{filename}"{css_class}>{label}</a>')
        links_html = '\n'.join(links)
        groups_html.append(f'''  <div class="drh-group">
    <button class="drh-group-label" aria-haspopup="true" aria-expanded="false">{group_name} &#9662;</button>
    <div class="drh-dropdown" role="menu">
{links_html}
    </div>
  </div>''')

    return f'''{NAV_MARKER}
<nav class="drh-nav" role="navigation" aria-label="Dashboard navigation">
  <a class="drh-home" href="../docs/index.html" aria-label="Return to Diabetes Research Hub">&larr; Hub</a>
{''.join(groups_html)}
</nav>
'''


# ─── PMID text → hyperlink conversion ──────────────────────────────────
PMID_LINK_PATTERN = re.compile(
    r'(?<!href="https://pubmed\.ncbi\.nlm\.nih\.gov/)'  # not already in a link href
    r'(?<!">)'  # not already inside link text
    r'(?<![/\d])'  # not preceded by slash+digits (part of URL)
    r'(PMID[:\s]*(\d{6,9}))'  # match PMID: 12345678 or PMID 12345678
    r'(?!</a>)'  # not already a closing link
)

def convert_pmid_to_links(html):
    """Convert plain-text PMID references to PubMed hyperlinks.

    Skips PMIDs that are already inside <a> tags.
    """
    # First, find all PMIDs that are already linked (inside <a> tags)
    linked_pattern = re.compile(r'<a[^>]*href="https://pubmed\.ncbi\.nlm\.nih\.gov/\d+[^"]*"[^>]*>.*?</a>', re.DOTALL)

    # Track positions of existing links to avoid double-linking
    linked_positions = set()
    for m in linked_pattern.finditer(html):
        linked_positions.add((m.start(), m.end()))

    def is_inside_link(pos, html_text):
        """Check if position is inside an existing <a> tag."""
        # Find the nearest preceding <a or </a
        before = html_text[:pos]
        last_a_open = before.rfind('<a ')
        if last_a_open == -1:
            last_a_open = before.rfind('<a\n')
        last_a_close = before.rfind('</a>')

        if last_a_open > last_a_close:
            return True  # We're inside an <a> tag
        return False

    def is_inside_href(pos, html_text):
        """Check if position is inside an href attribute."""
        before = html_text[max(0, pos-200):pos]
        last_href = before.rfind('href="')
        if last_href == -1:
            return False
        last_quote = before.rfind('"', last_href + 6)
        if last_quote == -1:
            return True  # href not closed yet
        return False

    # Find all PMID patterns
    pmid_pattern = re.compile(r'PMID[:\s]*(\d{6,9})')

    result = []
    last_end = 0

    for m in pmid_pattern.finditer(html):
        pos = m.start()

        # Skip if inside a link or href
        if is_inside_link(pos, html) or is_inside_href(pos, html):
            continue

        pmid_num = m.group(1)
        original = m.group(0)
        replacement = f'<a href="https://pubmed.ncbi.nlm.nih.gov/{pmid_num}/" target="_blank" rel="noopener" title="View on PubMed">{original}</a>'

        result.append(html[last_end:pos])
        result.append(replacement)
        last_end = m.end()

    result.append(html[last_end:])
    return ''.join(result)


# ─── ARIA label injection ──────────────────────────────────────────────
def add_aria_labels(html):
    """Add ARIA attributes to interactive elements."""

    # Add role="tablist" to tab containers
    html = re.sub(
        r'<div class="tabs-nav"(?![^>]*role=)',
        '<div class="tabs-nav" role="tablist"',
        html
    )
    html = re.sub(
        r'<div class="tabs"(?![^>]*role=)',
        '<div class="tabs" role="tablist"',
        html
    )

    # Add role="tab" and aria-label to tab buttons
    def add_tab_role(match):
        tag = match.group(0)
        if 'role=' not in tag:
            tag = tag.replace('class="tab-button', 'role="tab" class="tab-button')
        return tag

    html = re.sub(r'<button[^>]*class="tab-button[^"]*"[^>]*>', add_tab_role, html)

    # Add role="tabpanel" to tab content divs
    html = re.sub(
        r'<div class="tab-content"(?![^>]*role=)',
        '<div class="tab-content" role="tabpanel"',
        html
    )
    html = re.sub(
        r'<div class="tab-pane"(?![^>]*role=)',
        '<div class="tab-pane" role="tabpanel"',
        html
    )

    # Add aria-label to search inputs
    html = re.sub(
        r'<input([^>]*?)type="text"([^>]*?)placeholder="([^"]*?)"',
        lambda m: f'<input{m.group(1)}type="text"{m.group(2)}placeholder="{m.group(3)}" aria-label="{m.group(3)}"'
            if 'aria-label' not in m.group(0) else m.group(0),
        html
    )
    html = re.sub(
        r'<input([^>]*?)type="search"([^>]*?)placeholder="([^"]*?)"',
        lambda m: f'<input{m.group(1)}type="search"{m.group(2)}placeholder="{m.group(3)}" aria-label="{m.group(3)}"'
            if 'aria-label' not in m.group(0) else m.group(0),
        html
    )

    # Add role="table" with aria-label to tables that lack it
    html = re.sub(
        r'<table(?![^>]*role=)(?![^>]*aria-)',
        '<table role="table"',
        html
    )

    return html


# ─── Main processing ───────────────────────────────────────────────────
def process_dashboard(filepath):
    """Process a single dashboard HTML file."""
    filename = os.path.basename(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html
    changes = []

    # 1. Remove any existing nav bar (for idempotent re-runs)
    if NAV_MARKER in html:
        # Remove old nav bar
        nav_start = html.index(NAV_MARKER)
        nav_end = html.index('</nav>', nav_start) + len('</nav>') + 1
        html = html[:nav_start] + html[nav_end:]

    # Also remove old standalone back-links that we'll replace with the nav bar
    old_backlink_patterns = [
        r'<div[^>]*>\s*<a[^>]*href="[^"]*index\.html"[^>]*>[^<]*Diabetes Research Hub[^<]*</a>\s*</div>\s*',
        r'<a[^>]*href="[^"]*index\.html"[^>]*style="[^"]*"[^>]*>[^<]*Diabetes Research Hub[^<]*</a>\s*',
    ]
    for pattern in old_backlink_patterns:
        html = re.sub(pattern, '', html, count=1)

    # 2. Inject nav bar after <body> tag
    nav_css = build_nav_css()
    nav_html = build_nav_html(filename)

    # Add CSS before </style> or </head>
    if '</style>' in html:
        # Insert before the last </style>
        last_style_end = html.rfind('</style>')
        html = html[:last_style_end] + nav_css + html[last_style_end:]
        changes.append('nav CSS')

    # Add nav HTML after <body> tag
    body_match = re.search(r'<body[^>]*>', html)
    if body_match:
        insert_pos = body_match.end()
        html = html[:insert_pos] + '\n' + nav_html + html[insert_pos:]
        changes.append('nav bar')

    # 3. Convert PMID text to hyperlinks
    before_pmid = html
    html = convert_pmid_to_links(html)
    if html != before_pmid:
        changes.append('PMID links')

    # 4. Add ARIA labels
    before_aria = html
    html = add_aria_labels(html)
    if html != before_aria:
        changes.append('ARIA labels')

    # Write if changed
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return changes
    return []


def main():
    print("Post-processing dashboards (nav, PMID links, ARIA)...")

    html_files = sorted(glob.glob(os.path.join(DASHBOARDS_DIR, '*.html')))

    if not html_files:
        print("  No dashboard HTML files found!")
        return

    total_changes = 0
    for filepath in html_files:
        filename = os.path.basename(filepath)
        changes = process_dashboard(filepath)
        if changes:
            print(f"  {filename}: {', '.join(changes)}")
            total_changes += 1
        else:
            print(f"  {filename}: no changes needed")

    print(f"\n  Processed {len(html_files)} dashboards, {total_changes} modified.")
    print("Done.")


if __name__ == '__main__':
    main()
