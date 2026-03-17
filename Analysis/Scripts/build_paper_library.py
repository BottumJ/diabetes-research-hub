#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper Library Dashboard
========================
Generates an interactive HTML dashboard that visualizes the ingested paper library:
  - Searchable/sortable table of all 187 papers with abstracts
  - Validation scores (CONFIRMED/PLAUSIBLE/WEAK)
  - Evidence network: cross-citations and shared MeSH clusters
  - Coverage statistics (abstracts, full text, PMC availability)
  - Links to PubMed for each paper

Reads from:
  - Analysis/Results/paper_library/index.json
  - Analysis/Results/citation_validation.json
  - Analysis/Results/evidence_network.json

Outputs:
  - Dashboards/Paper_Library.html

Tufte style: cream background, serif headers, no gradients/rounded corners/emojis.
"""

import os
import json
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
results_dir = os.path.join(base_dir, 'Analysis', 'Results')
library_dir = os.path.join(results_dir, 'paper_library')
output_dir = os.path.join(base_dir, 'Dashboards')
os.makedirs(output_dir, exist_ok=True)

# Tufte colors
COLORS = {
    'bg': '#fafaf7',
    'text': '#333333',
    'muted': '#636363',
    'border': '#e0ddd5',
    'accent': '#2c5f8a',
    'header_bg': '#ffffff',
    'confirmed': '#2d6a2e',
    'plausible': '#4a7c59',
    'weak': '#8b7355',
    'mismatch': '#a33b2c',
    'no_data': '#999999',
}


def load_data():
    """Load all required JSON data files."""
    data = {}

    index_path = os.path.join(library_dir, 'index.json')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            data['index'] = json.load(f)
    else:
        print('  ERROR: paper library index.json not found. Run ingest_papers.py first.')
        return None

    validation_path = os.path.join(results_dir, 'citation_validation.json')
    if os.path.exists(validation_path):
        with open(validation_path, 'r', encoding='utf-8') as f:
            data['validation'] = json.load(f)

    network_path = os.path.join(results_dir, 'evidence_network.json')
    if os.path.exists(network_path):
        with open(network_path, 'r', encoding='utf-8') as f:
            data['network'] = json.load(f)

    return data


def escape_html(text):
    """Escape HTML special characters."""
    return (text.replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def build_html(data):
    """Generate the Paper Library dashboard HTML."""
    index = data['index']
    validation = data.get('validation', {})
    network = data.get('network', {})

    papers = index.get('papers', {})
    meta = index.get('metadata', {})
    val_results = validation.get('results', {})
    val_summary = validation.get('summary', {})
    net_data = network.get('network', {})
    net_meta = network.get('metadata', {})

    # Sort papers by year (newest first), then by PMID
    sorted_pmids = sorted(papers.keys(),
                          key=lambda p: (papers[p].get('year', '0000'), p),
                          reverse=True)

    # Build paper rows
    paper_rows = []
    for pmid in sorted_pmids:
        p = papers[pmid]
        v = val_results.get(pmid, {})
        score = v.get('score', 'N/A')
        confidence = v.get('confidence', 0)
        title = escape_html(p.get('title', 'Unknown'))
        journal = escape_html(p.get('journal', ''))
        year = p.get('year', '')
        doi = p.get('doi', '')
        pmcid = p.get('pmcid', '')
        has_abstract = p.get('has_abstract', False)
        has_fulltext = p.get('has_fulltext', False)
        mesh_terms = p.get('mesh_terms', [])
        keywords = p.get('keywords', [])
        cited_in_hub = p.get('cited_pmids_in_hub', [])
        locations = p.get('dashboard_locations', [])

        # Score color
        score_color = COLORS.get(score.lower(), COLORS['muted'])

        # Build location tags
        loc_files = list(set(l.get('file', '').replace('.py', '') for l in locations))
        loc_tags = ', '.join(loc_files[:3])
        if len(loc_files) > 3:
            loc_tags += f' +{len(loc_files)-3}'

        # Coverage indicators
        coverage = []
        if has_abstract:
            coverage.append('Abstract')
        if has_fulltext:
            coverage.append('Full Text')
        if pmcid:
            coverage.append(f'PMC')
        coverage_str = ' | '.join(coverage) if coverage else 'Metadata only'

        paper_rows.append(f'''
        <tr class="paper-row" data-score="{score}" data-year="{year}" data-pmid="{pmid}">
            <td class="pmid-col"><a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank" rel="noopener">{pmid}</a></td>
            <td class="title-col">{title}</td>
            <td class="journal-col">{journal}</td>
            <td class="year-col">{year}</td>
            <td class="score-col" style="color:{score_color};font-weight:600;">{score}</td>
            <td class="coverage-col">{coverage_str}</td>
            <td class="loc-col">{loc_tags}</td>
        </tr>''')

    paper_rows_html = '\n'.join(paper_rows)

    # Build MeSH cluster section (top clinical clusters)
    clusters = net_data.get('clusters', [])
    cluster_rows = []
    for c in clusters[:20]:
        topic = escape_html(c.get('topic', ''))
        count = c.get('paper_count', 0)
        cluster_rows.append(f'<tr><td>{topic}</td><td>{count}</td></tr>')
    cluster_rows_html = '\n'.join(cluster_rows)

    # Build cross-citation list
    citing = index.get('cross_references', {}).get('papers_citing_each_other', {})
    citation_rows = []
    for pmid, cited_list in sorted(citing.items(), key=lambda x: -len(x[1]))[:15]:
        p = papers.get(pmid, {})
        title_short = escape_html(p.get('title', '')[:70])
        cited_str = ', '.join(f'<a href="https://pubmed.ncbi.nlm.nih.gov/{c}/" target="_blank">{c}</a>' for c in cited_list[:5])
        if len(cited_list) > 5:
            cited_str += f' +{len(cited_list)-5} more'
        citation_rows.append(f'<tr><td><a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank">{pmid}</a></td><td>{title_short}</td><td>{cited_str}</td></tr>')
    citation_rows_html = '\n'.join(citation_rows)

    # Validation summary counts
    confirmed = val_summary.get('CONFIRMED', 0)
    plausible = val_summary.get('PLAUSIBLE', 0)
    weak = val_summary.get('WEAK', 0)
    mismatch = val_summary.get('MISMATCH', 0)
    no_data = val_summary.get('NO_DATA', 0)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paper Library - Diabetes Research Hub</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: {COLORS['text']};
            line-height: 1.6;
            background-color: {COLORS['bg']};
        }}
        h1, h2, h3 {{ font-family: Georgia, "Times New Roman", serif; font-weight: normal; }}
        h1 {{ font-size: 1.8rem; margin-bottom: 0.3rem; }}
        h2 {{ font-size: 1.3rem; margin: 2rem 0 0.8rem 0; color: {COLORS['text']}; border-bottom: 1px solid {COLORS['border']}; padding-bottom: 0.3rem; }}
        h3 {{ font-size: 1.1rem; margin: 1.2rem 0 0.5rem 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px 30px 40px 30px; }}
        .description {{ color: {COLORS['muted']}; font-size: 0.9rem; margin-bottom: 1.5rem; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px;
            margin-bottom: 1.5rem;
        }}
        .stat-card {{
            background: {COLORS['header_bg']};
            border: 1px solid {COLORS['border']};
            padding: 12px 16px;
        }}
        .stat-value {{ font-family: "SF Mono", Consolas, "Liberation Mono", Menlo, monospace; font-size: 1.6rem; font-weight: 600; }}
        .stat-label {{ font-size: 0.8rem; color: {COLORS['muted']}; text-transform: uppercase; letter-spacing: 0.05em; }}
        .filters {{
            display: flex;
            gap: 12px;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }}
        .filters input {{
            padding: 6px 10px;
            border: 1px solid {COLORS['border']};
            background: {COLORS['header_bg']};
            font-size: 0.9rem;
            width: 300px;
            font-family: inherit;
        }}
        .filters select {{
            padding: 6px 10px;
            border: 1px solid {COLORS['border']};
            background: {COLORS['header_bg']};
            font-size: 0.9rem;
            font-family: inherit;
        }}
        .filter-label {{ font-size: 0.8rem; color: {COLORS['muted']}; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }}
        th {{
            text-align: left;
            padding: 8px 10px;
            border-bottom: 2px solid {COLORS['text']};
            font-weight: 600;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
        }}
        th:hover {{ color: {COLORS['accent']}; }}
        td {{
            padding: 6px 10px;
            border-bottom: 1px solid {COLORS['border']};
            vertical-align: top;
        }}
        tr:hover {{ background-color: #f5f4f0; }}
        a {{ color: {COLORS['accent']}; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .pmid-col {{ width: 80px; font-family: "SF Mono", Consolas, monospace; font-size: 0.82rem; }}
        .title-col {{ min-width: 250px; }}
        .journal-col {{ width: 120px; font-size: 0.82rem; color: {COLORS['muted']}; }}
        .year-col {{ width: 50px; text-align: center; }}
        .score-col {{ width: 90px; font-family: "SF Mono", Consolas, monospace; font-size: 0.82rem; text-align: center; }}
        .coverage-col {{ width: 120px; font-size: 0.8rem; color: {COLORS['muted']}; }}
        .loc-col {{ width: 130px; font-size: 0.78rem; color: {COLORS['muted']}; }}
        .tabs {{ display: flex; gap: 0; margin-bottom: 0; }}
        .tab-btn {{
            padding: 8px 20px;
            background: none;
            border: 1px solid {COLORS['border']};
            border-bottom: none;
            cursor: pointer;
            font-family: inherit;
            font-size: 0.9rem;
            color: {COLORS['muted']};
        }}
        .tab-btn.active {{
            background: {COLORS['header_bg']};
            color: {COLORS['text']};
            font-weight: 600;
            border-bottom: 1px solid {COLORS['header_bg']};
            position: relative;
            top: 1px;
        }}
        .tab-content {{
            display: none;
            border: 1px solid {COLORS['border']};
            background: {COLORS['header_bg']};
            padding: 16px;
        }}
        .tab-content.active {{ display: block; }}
        .validation-bar {{
            display: flex;
            height: 24px;
            margin: 8px 0 16px 0;
            border: 1px solid {COLORS['border']};
        }}
        .validation-bar div {{ height: 100%; }}
        .bar-confirmed {{ background: {COLORS['confirmed']}; }}
        .bar-plausible {{ background: {COLORS['plausible']}; }}
        .bar-weak {{ background: {COLORS['weak']}; }}
        .bar-mismatch {{ background: {COLORS['mismatch']}; }}
        .bar-nodata {{ background: {COLORS['no_data']}; }}
        .legend {{ display: flex; gap: 16px; font-size: 0.8rem; color: {COLORS['muted']}; margin-bottom: 16px; flex-wrap: wrap; }}
        .legend-item {{ display: flex; align-items: center; gap: 4px; }}
        .legend-swatch {{ width: 12px; height: 12px; display: inline-block; }}
        .count-badge {{
            font-family: "SF Mono", Consolas, monospace;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .small-table {{ max-width: 600px; }}
        .network-stat {{ display: inline-block; margin-right: 24px; margin-bottom: 8px; }}
        .timestamp {{ font-size: 0.75rem; color: {COLORS['muted']}; margin-top: 2rem; }}
    </style>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-JGMD5VRYPH');</script>
</head>
<body>
<div style="background:#ffffff;border-bottom:1px solid #e0ddd5;padding:8px 20px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:13px;display:flex;gap:16px;align-items:center;flex-wrap:wrap;">
  <a href="../index.html" style="color:#2c5f8a;text-decoration:none;font-weight:600;">&larr; Diabetes Research Hub</a>
  <span style="color:#e0ddd5;">|</span>
  <a href="Research_Dashboard.html" style="color:#636363;text-decoration:none;">Research</a>
  <a href="Clinical_Trial_Dashboard.html" style="color:#636363;text-decoration:none;">Trials</a>
  <a href="Gap_Deep_Dives.html" style="color:#636363;text-decoration:none;">Gaps</a>
  <a href="Gap_Synthesis.html" style="color:#636363;text-decoration:none;">Synthesis</a>
  <a href="Equity_Map.html" style="color:#636363;text-decoration:none;">Equity</a>
  <a href="Medical_Data_Dictionary.html" style="color:#636363;text-decoration:none;">Dictionary</a>
  <a href="Acronym_Database.html" style="color:#636363;text-decoration:none;">Acronyms</a>
  <a href="Paper_Library.html" style="color:#2c5f8a;text-decoration:none;font-weight:600;">Paper Library</a>
</div>
<div class="container">
    <h1>Paper Library</h1>
    <p class="description">Ingested research papers with abstracts, full text (where available), citation validation scores, and cross-paper linkage. Every citation in the Diabetes Research Hub is verified against PubMed and scored for relevance.</p>

    <!-- Summary Statistics -->
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{meta.get('total_pmids', 0)}</div>
            <div class="stat-label">Total Papers</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{meta.get('abstracts_fetched', 0)}</div>
            <div class="stat-label">Abstracts</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{meta.get('pmc_available', 0)}</div>
            <div class="stat-label">PMC Available</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{meta.get('fulltext_fetched', 0)}</div>
            <div class="stat-label">Full Text</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{net_meta.get('citation_edges', 0)}</div>
            <div class="stat-label">Cross-Citations</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{net_meta.get('topic_clusters', 0)}</div>
            <div class="stat-label">Topic Clusters</div>
        </div>
    </div>

    <!-- Validation Bar -->
    <h2>Citation Validation</h2>
    <div class="validation-bar">
        <div class="bar-confirmed" style="width:{confirmed/max(meta.get('total_pmids',1),1)*100:.1f}%;" title="CONFIRMED: {confirmed}"></div>
        <div class="bar-plausible" style="width:{plausible/max(meta.get('total_pmids',1),1)*100:.1f}%;" title="PLAUSIBLE: {plausible}"></div>
        <div class="bar-weak" style="width:{weak/max(meta.get('total_pmids',1),1)*100:.1f}%;" title="WEAK: {weak}"></div>
        <div class="bar-mismatch" style="width:{mismatch/max(meta.get('total_pmids',1),1)*100:.1f}%;" title="MISMATCH: {mismatch}"></div>
        <div class="bar-nodata" style="width:{no_data/max(meta.get('total_pmids',1),1)*100:.1f}%;" title="NO DATA: {no_data}"></div>
    </div>
    <div class="legend">
        <div class="legend-item"><span class="legend-swatch" style="background:{COLORS['confirmed']};"></span> Confirmed <span class="count-badge">{confirmed}</span></div>
        <div class="legend-item"><span class="legend-swatch" style="background:{COLORS['plausible']};"></span> Plausible <span class="count-badge">{plausible}</span></div>
        <div class="legend-item"><span class="legend-swatch" style="background:{COLORS['weak']};"></span> Weak <span class="count-badge">{weak}</span></div>
        <div class="legend-item"><span class="legend-swatch" style="background:{COLORS['mismatch']};"></span> Mismatch <span class="count-badge">{mismatch}</span></div>
        <div class="legend-item"><span class="legend-swatch" style="background:{COLORS['no_data']};"></span> No Data <span class="count-badge">{no_data}</span></div>
    </div>
    <p style="font-size:0.85rem;color:{COLORS['muted']};margin-bottom:1rem;">Scores reflect automated term-matching between dashboard claims and paper abstracts. "Weak" often means the claim context in our scripts is HTML-heavy rather than a true content mismatch.</p>

    <!-- Tabs -->
    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('papers')">All Papers</button>
        <button class="tab-btn" onclick="switchTab('network')">Evidence Network</button>
        <button class="tab-btn" onclick="switchTab('clusters')">Topic Clusters</button>
    </div>

    <!-- Tab: All Papers -->
    <div id="tab-papers" class="tab-content active">
        <div class="filters">
            <div>
                <div class="filter-label">Search</div>
                <input type="text" id="searchInput" placeholder="Search by title, PMID, journal..." oninput="filterTable()">
            </div>
            <div>
                <div class="filter-label">Score</div>
                <select id="scoreFilter" onchange="filterTable()">
                    <option value="">All</option>
                    <option value="CONFIRMED">Confirmed</option>
                    <option value="PLAUSIBLE">Plausible</option>
                    <option value="WEAK">Weak</option>
                    <option value="MISMATCH">Mismatch</option>
                    <option value="NO_DATA">No Data</option>
                </select>
            </div>
            <div>
                <div class="filter-label">Coverage</div>
                <select id="coverageFilter" onchange="filterTable()">
                    <option value="">All</option>
                    <option value="Full Text">Full Text</option>
                    <option value="Abstract">Has Abstract</option>
                    <option value="PMC">PMC Available</option>
                </select>
            </div>
            <div style="margin-left:auto;font-size:0.85rem;color:{COLORS['muted']};">
                Showing <span id="visibleCount">{len(sorted_pmids)}</span> of {len(sorted_pmids)} papers
            </div>
        </div>
        <div style="overflow-x:auto;">
        <table id="paperTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">PMID</th>
                    <th onclick="sortTable(1)">Title</th>
                    <th onclick="sortTable(2)">Journal</th>
                    <th onclick="sortTable(3)">Year</th>
                    <th onclick="sortTable(4)">Score</th>
                    <th onclick="sortTable(5)">Coverage</th>
                    <th onclick="sortTable(6)">Used In</th>
                </tr>
            </thead>
            <tbody>
{paper_rows_html}
            </tbody>
        </table>
        </div>
    </div>

    <!-- Tab: Evidence Network -->
    <div id="tab-network" class="tab-content">
        <h3>Intra-Hub Cross-Citations</h3>
        <p style="font-size:0.85rem;color:{COLORS['muted']};margin-bottom:12px;">Papers in our library that cite other papers also in our library. This shows how our evidence base is interconnected.</p>
        <div style="overflow-x:auto;">
        <table class="small-table">
            <thead><tr><th>PMID</th><th>Title</th><th>Cites (in hub)</th></tr></thead>
            <tbody>
{citation_rows_html}
            </tbody>
        </table>
        </div>
    </div>

    <!-- Tab: Topic Clusters -->
    <div id="tab-clusters" class="tab-content">
        <h3>Shared MeSH Term Clusters</h3>
        <p style="font-size:0.85rem;color:{COLORS['muted']};margin-bottom:12px;">Clinical MeSH terms shared by 3 or more papers in the library. These reveal the topical structure of our evidence base.</p>
        <div style="overflow-x:auto;">
        <table class="small-table">
            <thead><tr><th>MeSH Term</th><th>Papers</th></tr></thead>
            <tbody>
{cluster_rows_html}
            </tbody>
        </table>
        </div>
    </div>

    <p class="timestamp">Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} | Data from PubMed/PMC via NCBI E-utilities</p>
</div>

<script>
function switchTab(tabName) {{
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-' + tabName).classList.add('active');
    event.target.classList.add('active');
}}

function filterTable() {{
    const search = document.getElementById('searchInput').value.toLowerCase();
    const score = document.getElementById('scoreFilter').value;
    const coverage = document.getElementById('coverageFilter').value;
    const rows = document.querySelectorAll('#paperTable tbody tr');
    let visible = 0;
    rows.forEach(row => {{
        const text = row.textContent.toLowerCase();
        const rowScore = row.getAttribute('data-score');
        const coverageText = row.cells[5].textContent;
        const matchSearch = !search || text.includes(search);
        const matchScore = !score || rowScore === score;
        const matchCoverage = !coverage || coverageText.includes(coverage);
        if (matchSearch && matchScore && matchCoverage) {{
            row.style.display = '';
            visible++;
        }} else {{
            row.style.display = 'none';
        }}
    }});
    document.getElementById('visibleCount').textContent = visible;
}}

let sortDirection = {{}};
function sortTable(colIndex) {{
    const table = document.getElementById('paperTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const dir = sortDirection[colIndex] = !(sortDirection[colIndex] || false);
    rows.sort((a, b) => {{
        let aVal = a.cells[colIndex].textContent.trim();
        let bVal = b.cells[colIndex].textContent.trim();
        if (colIndex === 0 || colIndex === 3) {{
            aVal = parseInt(aVal) || 0;
            bVal = parseInt(bVal) || 0;
            return dir ? aVal - bVal : bVal - aVal;
        }}
        return dir ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    }});
    rows.forEach(r => tbody.appendChild(r));
}}
</script>
</body>
</html>'''

    return html


def main():
    print('Paper Library Dashboard')
    print('=' * 60)

    data = load_data()
    if not data:
        return 1

    html = build_html(data)
    output_path = os.path.join(output_dir, 'Paper_Library.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_kb = os.path.getsize(output_path) / 1024
    papers_count = len(data['index'].get('papers', {}))
    print(f'  Paper Library: {size_kb:.1f} KB ({papers_count} papers)')
    print(f'  Output: {output_path}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
