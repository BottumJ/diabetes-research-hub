#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extracted Evidence Dashboard Generator
Tufte-style HTML dashboard visualizing quantitative data extracted from the corpus
"""

import json
import os
from datetime import datetime
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')

# Data file paths
corpus_data_file = os.path.join(base_dir, 'Analysis', 'Results', 'extracted_corpus_data.json')
output_file = os.path.join(base_dir, 'Dashboards', 'Extracted_Evidence.html')

# Gap metadata (15 gaps)
GAPS_METADATA = {
    "1": {"title": "Gene Therapy for LADA", "tier": "SILVER"},
    "2": {"title": "Health Equity in Beta Cell Therapies", "tier": "GOLD"},
    "3": {"title": "LADA Phenotyping in Clinical Trials", "tier": "SILVER"},
    "4": {"title": "GLP-1/SGLT2i + Beta Cell Synergy", "tier": "BRONZE"},
    "5": {"title": "Islet Transplant Immunosuppression Optimization", "tier": "SILVER"},
    "6": {"title": "CAR-T Diabetes Safety Signals", "tier": "BRONZE"},
    "7": {"title": "Cardiovascular-Inflammation Intersection", "tier": "GOLD"},
    "8": {"title": "Drug Repurposing for Beta Cell Protection", "tier": "SILVER"},
    "9": {"title": "Autoimmune Beta Cell Epitopes in LADA", "tier": "SILVER"},
    "10": {"title": "Remission Sustainability Beyond 2 Years", "tier": "BRONZE"},
    "11": {"title": "Immunomodulation in Type 2 Diabetes", "tier": "BRONZE"},
    "12": {"title": "GLP-1 Effects on Beta Cell Function", "tier": "GOLD"},
    "13": {"title": "LADA Progression Markers", "tier": "SILVER"},
    "14": {"title": "Islet Allotransplant Rejection Prediction", "tier": "BRONZE"},
    "15": {"title": "Combination Therapy Synergies", "tier": "BRONZE"},
}

def truncate(text, length=300):
    """Truncate text to specified length."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + "…"

def load_corpus_data():
    """Load extracted corpus data from JSON."""
    with open(corpus_data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_evidence_strength(count):
    """Classify evidence strength based on data point count."""
    if count > 50:
        return ("STRONG", "Strong corpus-backed evidence")
    elif count >= 10:
        return ("MODERATE", "Moderate evidence present")
    elif count > 0:
        return ("WEAK", "Limited evidence found")
    else:
        return ("NONE", "No evidence in corpus")

def extract_inflammatory_markers(inflammatory_data):
    """Categorize inflammatory markers by type."""
    markers = defaultdict(list)

    for item in inflammatory_data:
        matched = item.get('matched_text', '').upper()

        if 'CRP' in matched or 'C-REACTIVE' in matched:
            markers['CRP'].append(item)
        elif 'TNF' in matched:
            markers['TNF-alpha'].append(item)
        elif 'IL-1' in matched:
            markers['IL-1'].append(item)
        elif 'IL-6' in matched:
            markers['IL-6'].append(item)
        elif 'NLRP3' in matched or 'INFLAMMASOME' in matched:
            markers['NLRP3'].append(item)
        else:
            markers['Other'].append(item)

    return markers

def build_cross_gap_network(data):
    """Find PMIDs that bridge multiple gaps."""
    pmid_to_gaps = defaultdict(set)

    for category, items in data['extractions'].items():
        for item in items:
            pmid = item.get('pmid')
            gap_relevance = item.get('gap_relevance', [])
            for gap_id in gap_relevance:
                pmid_to_gaps[pmid].add(gap_id)

    # Find PMIDs that bridge 2+ gaps
    bridges = []
    for pmid, gaps in pmid_to_gaps.items():
        if len(gaps) > 1:
            bridges.append({
                'pmid': pmid,
                'gap_count': len(gaps),
                'gaps': sorted(list(gaps))
            })

    return sorted(bridges, key=lambda x: x['gap_count'], reverse=True)

def generate_html(data):
    """Generate the complete HTML dashboard."""

    # Prepare summary stats
    total_extractions = data['metadata']['total_extractions']
    papers_with_data = len(data['paper_stats'])

    # Build gap evidence map
    gap_evidence = defaultdict(lambda: defaultdict(list))
    for category, items in data['extractions'].items():
        for item in items:
            gap_ids = item.get('gap_relevance', [])
            for gap_id in gap_ids:
                gap_evidence[gap_id][category].append(item)

    # Get cross-gap bridges
    bridges = build_cross_gap_network(data)

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extracted Evidence Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: #fafaf7;
            color: #333;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        header { margin-bottom: 40px; border-bottom: 1px solid #ddd; padding-bottom: 20px; }
        h1 { font-family: Georgia, serif; font-size: 2.5em; margin-bottom: 10px; color: #1a1a1a; }
        h2 { font-family: Georgia, serif; font-size: 1.8em; margin: 30px 0 15px 0; color: #1a1a1a; }
        h3 { font-family: Georgia, serif; font-size: 1.3em; margin: 20px 0 10px 0; color: #1a1a1a; }
        h4 { font-family: Georgia, serif; font-size: 1.1em; margin: 15px 0 8px 0; color: #1a1a1a; }
        .subtitle { font-size: 1.1em; color: #666; margin-bottom: 20px; }
        .tabs { display: flex; gap: 10px; margin-bottom: 30px; border-bottom: 2px solid #ddd; flex-wrap: wrap; }
        .tab-button { background: none; border: none; padding: 12px 20px; font-size: 1em; cursor: pointer; color: #666; border-bottom: 3px solid transparent; transition: all 0.3s ease; font-family: Georgia, serif; }
        .tab-button:hover { color: #1a1a1a; }
        .tab-button.active { color: #1a1a1a; border-bottom-color: #1a1a1a; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; font-family: "Segoe UI", sans-serif; }
        th { background-color: #f5f5f5; padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #ddd; font-family: Georgia, serif; }
        td { padding: 12px; border-bottom: 1px solid #eee; }
        tr:hover { background-color: #fafaf7; }
        .tier-badge { display: inline-block; padding: 4px 8px; font-size: 0.85em; font-weight: 600; font-family: "Courier New", monospace; margin-right: 8px; }
        .tier-gold { background-color: #fef3c7; color: #92400e; }
        .tier-silver { background-color: #e5e7eb; color: #374151; }
        .tier-bronze { background-color: #fed7aa; color: #92400e; }
        .evidence-strong { background-color: #dcfce7; color: #15803d; }
        .evidence-moderate { background-color: #fef3c7; color: #92400e; }
        .evidence-weak { background-color: #fecaca; color: #991b1b; }
        .evidence-none { background-color: #f3f4f6; color: #6b7280; }
        .stats-box { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat-card { background: white; padding: 20px; border: 1px solid #eee; border-left: 4px solid #9ca3af; }
        .stat-label { font-size: 0.9em; color: #666; margin-bottom: 8px; }
        .stat-value { font-family: "Courier New", monospace; font-size: 1.8em; font-weight: 600; color: #1a1a1a; }
        .gap-section { background: white; border: 1px solid #eee; padding: 20px; margin: 20px 0; border-left: 4px solid #ccc; }
        .gap-section.gold { border-left-color: #d4a574; }
        .gap-section.silver { border-left-color: #9ca3af; }
        .gap-section.bronze { border-left-color: #b8936d; }
        .gap-title { font-family: Georgia, serif; font-size: 1.2em; font-weight: 600; color: #1a1a1a; margin-bottom: 10px; }
        .context-block { background-color: #ffffff; border-left: 4px solid #2c5f8a; padding: 1.5rem 2rem; margin: 0 0 2rem 0; line-height: 1.8; }
        .context-block h3 { font-family: Georgia, serif; font-size: 1.1rem; color: #2c5f8a; margin: 0 0 0.75rem 0; font-weight: normal; }
        .context-block p { margin: 0.5rem 0; font-size: 0.95rem; color: #333; }
        .context-block .context-label { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #666; margin-top: 1rem; margin-bottom: 0.25rem; }
        .data-point { background: white; border-left: 3px solid #ddd; padding: 12px; margin: 10px 0; font-size: 0.95em; }
        .pmid-link { color: #2563eb; text-decoration: none; font-weight: 500; }
        .pmid-link:hover { text-decoration: underline; }
        .context-snippet { font-style: italic; color: #666; font-size: 0.9em; margin-top: 8px; padding: 8px; background-color: #f9f9f9; border-left: 2px solid #ddd; }
        .meta-small { font-size: 0.85em; color: #999; margin-top: 5px; }
        .footer { margin-top: 60px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #999; font-size: 0.9em; }
        .breakdown-table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.95em; }
        .breakdown-table td { padding: 8px; border-bottom: 1px solid #eee; }
    </style>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-JGMD5VRYPH');
    </script>
</head>
<body>
    <div class="container">
        <header>
            <h1>Extracted Evidence Dashboard</h1>
            <p class="subtitle">Quantitative data extraction from 61 full-text diabetes research papers</p>
            <p class="subtitle">Generated: ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
        </header>

        <div class="context-block">
            <h3>What This Dashboard Answers</h3>
            <p>This dashboard visualizes quantitative data that we actually extracted from ''' + str(papers_with_data) + ''' full-text papers using regex patterns and NLP-assisted identification. It answers: What quantitative data can we actually extract from our corpus? Which research gaps have the strongest corpus-backed evidence?</p>

            <div class="context-label">How to Use This</div>
            <p>Each data point links back to its source PMID with surrounding context. Click any PMID to verify the claim in the original paper. Use this dashboard to validate claims made in other research dashboards and to identify which gaps have direct quantitative support in the published literature.</p>

            <div class="context-label">What This Cannot Tell You</div>
            <p>Regex extraction is approximate. Numbers may come from different contexts (e.g., a C-peptide value from a control group, not a treatment group). Context snippets are truncated to 300 characters. Always verify the full context in the original paper before citing data. Missing papers in PubMed or non-English literature will not appear here.</p>
        </div>

        <div class="tabs">
            <button class="tab-button active" onclick="showTab('summary')">Executive Summary</button>
            <button class="tab-button" onclick="showTab('by-gap')">Evidence by Gap</button>
            <button class="tab-button" onclick="showTab('cpeptide')">C-Peptide Evidence</button>
            <button class="tab-button" onclick="showTab('survival')">Survival & Remission</button>
            <button class="tab-button" onclick="showTab('inflammatory')">Inflammatory Markers</button>
            <button class="tab-button" onclick="showTab('drugs')">Drug Dose-Response</button>
            <button class="tab-button" onclick="showTab('network')">Cross-Gap Network</button>
        </div>

        <div id="summary" class="tab-content active">
            <h2>Executive Summary</h2>
            <div class="stats-box">
                <div class="stat-card">
                    <div class="stat-label">Total Data Points Extracted</div>
                    <div class="stat-value">''' + str(total_extractions) + '''</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Papers Yielding Data</div>
                    <div class="stat-value">''' + str(papers_with_data) + '''</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Extraction Categories</div>
                    <div class="stat-value">''' + str(len(data['extractions'])) + '''</div>
                </div>
            </div>

            <h3>Extraction Categories</h3>
            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Count</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
'''

    # Add extraction type breakdown
    for category, count in sorted(data['metadata']['extraction_types'].items(), key=lambda x: x[1], reverse=True):
        category_name = category.replace('_', ' ').title()
        html += f'''                    <tr>
                        <td>{category_name}</td>
                        <td>{count}</td>
                        <td>{"Quantitative clinical measurements and thresholds" if category != "dose_response" else "Drug dosage and administration data"}</td>
                    </tr>
'''

    html += '''                </tbody>
            </table>
        </div>

        <div id="by-gap" class="tab-content">
            <h2>Evidence by Gap</h2>
            <p>Evidence strength ratings and top extractions for each of the 15 research gaps.</p>
'''

    # Add gap evidence sections
    for gap_id in sorted(GAPS_METADATA.keys(), key=lambda x: int(x)):
        gap_meta = GAPS_METADATA[gap_id]
        gap_evidence_data = gap_evidence.get(int(gap_id), {})

        total_gap_evidence = sum(len(items) for items in gap_evidence_data.values())
        strength, strength_label = get_evidence_strength(total_gap_evidence)
        strength_class = f"evidence-{strength.lower()}"
        tier_class = f"tier-{gap_meta['tier'].lower()}"
        gap_class = gap_meta['tier'].lower()

        html += f'''            <div class="gap-section {gap_class}">
                <div class="gap-title">
                    Gap {gap_id}: {gap_meta['title']}
                    <span class="tier-badge {tier_class}">{gap_meta['tier']}</span>
                    <span class="tier-badge {strength_class}">{strength}: {total_gap_evidence} points</span>
                </div>

                <h4>Evidence Strength: {strength_label}</h4>
                <p>This gap has <strong>{total_gap_evidence}</strong> data points in the corpus.</p>
'''

        if total_gap_evidence > 0:
            html += '''                <h4>Breakdown by Data Type</h4>
                <table class="breakdown-table">
'''
            for data_type, items in sorted(gap_evidence_data.items(), key=lambda x: len(x[1]), reverse=True):
                type_name = data_type.replace('_', ' ').title()
                html += f'''                    <tr>
                        <td>{type_name}</td>
                        <td style="text-align: right;">{len(items)} items</td>
                    </tr>
'''
            html += '''                </table>
'''

            # Top 3-5 most relevant values
            all_gap_items = []
            for category, items in gap_evidence_data.items():
                all_gap_items.extend(items)

            top_items = all_gap_items[:5]

            html += '''                <h4>Top Extracted Values with Context</h4>
'''
            for item in top_items:
                pmid = item.get('pmid', 'N/A')
                year = item.get('year', 'N/A')
                journal = item.get('journal', 'N/A')
                value = item.get('matched_text', 'N/A')
                context = truncate(item.get('context', ''), 300)

                html += f'''                <div class="data-point">
                    <strong>Value:</strong> {value}<br>
                    <strong>Source:</strong> <a class="pmid-link" href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank">PMID:{pmid}</a> ({year}, <em>{journal}</em>)<br>
                    <div class="context-snippet">{context}</div>
                </div>
'''
        else:
            html += '''                <p><em>No data points found in corpus for this gap.</em></p>
'''

        html += '''            </div>
'''

    html += '''        </div>

        <div id="cpeptide" class="tab-content">
            <h2>C-Peptide Evidence</h2>
            <p>All ''' + str(len(data['extractions'].get('c_peptide', []))) + ''' C-peptide extractions with full context. Critical for LADA/islet/immunomodulation gaps.</p>
'''

    for item in data['extractions'].get('c_peptide', []):
        pmid = item.get('pmid', 'N/A')
        year = item.get('year', 'N/A')
        journal = item.get('journal', 'N/A')
        title = item.get('title', 'N/A')
        value = item.get('matched_text', 'N/A')
        context = truncate(item.get('context', ''), 300)
        gap_ids = item.get('gap_relevance', [])

        html += f'''            <div class="data-point">
                <strong>C-Peptide Value:</strong> {value}<br>
                <strong>Source:</strong> <a class="pmid-link" href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank">PMID:{pmid}</a> ({year})<br>
                <strong>Journal:</strong> {journal}<br>
                <strong>Title:</strong> {title}<br>
                <strong>Relevant Gaps:</strong> {", ".join(str(g) for g in gap_ids) if gap_ids else "N/A"}<br>
                <div class="context-snippet">{context}</div>
            </div>
'''

    html += '''        </div>

        <div id="survival" class="tab-content">
            <h2>Survival & Remission Data</h2>
            <p>All graft survival and remission rate extractions. Validates islet transplant outcomes.</p>
            <h3>Graft Survival (''' + str(len(data['extractions'].get('survival_graft', []))) + ''' entries)</h3>
'''

    for item in data['extractions'].get('survival_graft', []):
        pmid = item.get('pmid', 'N/A')
        year = item.get('year', 'N/A')
        journal = item.get('journal', 'N/A')
        value = item.get('matched_text', 'N/A')
        context = truncate(item.get('context', ''), 300)

        html += f'''            <div class="data-point">
                <strong>Survival Data:</strong> {value}<br>
                <strong>Source:</strong> <a class="pmid-link" href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank">PMID:{pmid}</a> ({year}, {journal})<br>
                <div class="context-snippet">{context}</div>
            </div>
'''

    html += '''            <h3>Remission Rates (''' + str(len(data['extractions'].get('remission', []))) + ''' entries)</h3>
'''

    for item in data['extractions'].get('remission', [])[:10]:  # Top 10
        pmid = item.get('pmid', 'N/A')
        year = item.get('year', 'N/A')
        journal = item.get('journal', 'N/A')
        value = item.get('matched_text', 'N/A')
        context = truncate(item.get('context', ''), 300)

        html += f'''            <div class="data-point">
                <strong>Remission Rate:</strong> {value}<br>
                <strong>Source:</strong> <a class="pmid-link" href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank">PMID:{pmid}</a> ({year}, {journal})<br>
                <div class="context-snippet">{context}</div>
            </div>
'''

    html += '''        </div>

        <div id="inflammatory" class="tab-content">
            <h2>Inflammatory Marker Evidence</h2>
            <p>All ''' + str(len(data['extractions'].get('inflammatory_markers', []))) + ''' inflammatory marker extractions grouped by marker type.</p>
'''

    inflammatory_by_type = extract_inflammatory_markers(data['extractions'].get('inflammatory_markers', []))

    for marker_type in sorted(inflammatory_by_type.keys()):
        items = inflammatory_by_type[marker_type]
        html += f'''            <h3>{marker_type} ({len(items)} entries)</h3>
'''
        for item in items[:5]:  # Top 5 per marker type
            pmid = item.get('pmid', 'N/A')
            year = item.get('year', 'N/A')
            journal = item.get('journal', 'N/A')
            value = item.get('matched_text', 'N/A')
            context = truncate(item.get('context', ''), 300)

            html += f'''            <div class="data-point">
                <strong>{marker_type}:</strong> {value}<br>
                <strong>Source:</strong> <a class="pmid-link" href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank">PMID:{pmid}</a> ({year}, {journal})<br>
                <div class="context-snippet">{context}</div>
            </div>
'''

    html += '''        </div>

        <div id="drugs" class="tab-content">
            <h2>Drug Dose-Response Data</h2>
            <p>Top 20 most relevant dose extractions. Especially for drugs in repurposing screen.</p>
            <table>
                <thead>
                    <tr>
                        <th>Drug/Dose</th>
                        <th>PMID (Year)</th>
                        <th>Journal</th>
                        <th>Context</th>
                    </tr>
                </thead>
                <tbody>
'''

    dose_items = data['extractions'].get('dose_response', [])[:20]

    for item in dose_items:
        pmid = item.get('pmid', 'N/A')
        year = item.get('year', 'N/A')
        journal = item.get('journal', 'N/A')
        value = item.get('matched_text', 'N/A')
        context = truncate(item.get('context', ''), 150)

        html += f'''                <tr>
                    <td>{value}</td>
                    <td><a class="pmid-link" href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank">PMID:{pmid}</a> ({year})</td>
                    <td>{journal}</td>
                    <td>{context}</td>
                </tr>
'''

    html += '''                </tbody>
            </table>
        </div>

        <div id="network" class="tab-content">
            <h2>Cross-Gap Evidence Network</h2>
            <p>Papers that provide evidence relevant to 2 or more research gaps. These bridges show where evidence overlaps.</p>
            <table>
                <thead>
                    <tr>
                        <th>PMID</th>
                        <th>Gap Count</th>
                        <th>Gaps Bridged</th>
                    </tr>
                </thead>
                <tbody>
'''

    for bridge in bridges[:50]:  # Top 50 bridges
        pmid = bridge['pmid']
        gap_count = bridge['gap_count']
        gap_ids = bridge['gaps']

        html += f'''                <tr>
                    <td><a class="pmid-link" href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank">PMID:{pmid}</a></td>
                    <td>{gap_count}</td>
                    <td>{", ".join(str(g) for g in gap_ids)}</td>
                </tr>
'''

    html += '''                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Extracted Evidence Dashboard | Diabetes Research Platform | Generated ''' + datetime.now().strftime("%Y-%m-%d") + '''</p>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(c => c.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');

            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
        }
    </script>
</body>
</html>
'''

    return html

def main():
    """Generate and write the HTML dashboard."""
    print("Loading corpus data...")
    data = load_corpus_data()

    print(f"Processing {data['metadata']['total_extractions']} extractions...")
    html_content = generate_html(data)

    print(f"Writing dashboard to {output_file}...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Success! Dashboard generated: {output_file}")
    print(f"Papers processed: {len(data['paper_stats'])}")
    print(f"Total data points: {data['metadata']['total_extractions']}")

if __name__ == '__main__':
    main()
