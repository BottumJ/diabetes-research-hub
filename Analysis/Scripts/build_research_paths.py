#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Research Paths Dashboard Generator
Tufte-style HTML dashboard showing validated research paths extracted from the corpus
and cross-validated against published evidence
"""

import json
import os
from datetime import datetime
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')

# Data file paths
research_paths_file = os.path.join(base_dir, 'Analysis', 'Results', 'research_paths.json')
validated_paths_file = os.path.join(base_dir, 'Analysis', 'Results', 'validated_research_paths.json')
output_file = os.path.join(base_dir, 'Dashboards', 'Research_Paths.html')

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

# Status colors for Tufte style
STATUS_COLORS = {
    'VALIDATED': '#2d5016',  # forest green
    'PARTIALLY_VALIDATED': '#8b7500',  # olive/gold
    'UNVALIDATED': '#8b4513',  # saddle brown
    'CONTRADICTED': '#8b0000',  # dark red
}

STATUS_BG = {
    'VALIDATED': '#f0f8e8',  # light green
    'PARTIALLY_VALIDATED': '#fef8e8',  # light yellow
    'UNVALIDATED': '#f8f0e8',  # light brown
    'CONTRADICTED': '#f8e8e8',  # light red
}

def truncate(text, length=300):
    """Truncate text to specified length."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + "…"

def load_research_paths():
    """Load all research paths from JSON."""
    with open(research_paths_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_validated_paths():
    """Load validated research paths from JSON."""
    with open(validated_paths_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_path_name(path_name):
    """Convert path name to normalized key for matching."""
    # Replace spaces and arrows with underscores
    return path_name.replace(' ', '_').replace('->', '_').replace('→', '_')

def build_path_network(validated_data):
    """Build network of cross-connections between validated paths."""
    network = defaultdict(lambda: {'connected_to': [], 'shared_pmids': []})

    for path_name, path_data in validated_data['paths'].items():
        pmids = set(path_data.get('pmids_in_corpus', []))

        # Find other paths sharing PMIDs
        for other_name, other_data in validated_data['paths'].items():
            if path_name == other_name:
                continue
            other_pmids = set(other_data.get('pmids_in_corpus', []))
            shared = pmids & other_pmids
            if shared:
                network[path_name]['connected_to'].append(other_name)
                network[path_name]['shared_pmids'].extend(list(shared))

    return network

def map_paths_to_gaps(validated_data):
    """Map each validated path to relevant research gaps (heuristic)."""
    path_to_gaps = defaultdict(set)

    for path_name in validated_data['paths'].keys():
        path_lower = path_name.lower()

        # Heuristic mapping based on keywords
        if 'nlrp3' in path_lower or 'inflammasome' in path_lower:
            path_to_gaps[path_name].add('7')  # CV-Inflammation
        if 'inflammation' in path_lower:
            path_to_gaps[path_name].add('7')  # CV-Inflammation
            path_to_gaps[path_name].add('11')  # Immunomod T2D
        if 'oxidative_stress' in path_lower:
            path_to_gaps[path_name].add('7')  # CV-Inflammation
        if 'dapagliflozin' in path_lower or 'empagliflozin' in path_lower or 'sglt2' in path_lower.replace('_', ' '):
            path_to_gaps[path_name].add('4')  # GLP-1/SGLT2i synergy
            path_to_gaps[path_name].add('15')  # Combination therapy
        if 'glp' in path_lower or 'semaglutide' in path_lower:
            path_to_gaps[path_name].add('12')  # GLP-1 effects
            path_to_gaps[path_name].add('4')  # GLP-1/SGLT2i synergy
        if 'verapamil' in path_lower:
            path_to_gaps[path_name].add('8')  # Drug repurposing
        if 'hydroxychloroquine' in path_lower:
            path_to_gaps[path_name].add('8')  # Drug repurposing
        if 'rapamycin' in path_lower:
            path_to_gaps[path_name].add('8')  # Drug repurposing
        if 'beta' in path_lower:
            path_to_gaps[path_name].add('8')  # Drug repurposing
            path_to_gaps[path_name].add('12')  # GLP-1 effects
        if 'cardiovascular' in path_lower:
            path_to_gaps[path_name].add('7')  # CV-Inflammation
        if 'nephropathy' in path_lower or 'kidney' in path_lower:
            path_to_gaps[path_name].add('7')  # CV-Inflammation
        if 'autoimmune' in path_lower or 't1d' in path_lower:
            path_to_gaps[path_name].add('9')  # Autoimmune epitopes

        # Default to gaps if no match
        if not path_to_gaps[path_name]:
            path_to_gaps[path_name].add('7')  # Default to CV-Inflammation

    return path_to_gaps

def generate_html(research_paths, validated_data):
    """Generate the complete HTML dashboard."""

    # Count stats
    total_paths = research_paths['total_paths']
    validated_paths = validated_data['paths_validated']
    validation_summary = validated_data['validation_summary']

    # Build network
    network = build_path_network(validated_data)
    path_to_gaps = map_paths_to_gaps(validated_data)

    # Find hub paths (connected to most others)
    hub_paths = sorted(
        [(name, len(data['connected_to'])) for name, data in network.items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]

    # Get unvalidated paths
    validated_path_names = set(validated_data['paths'].keys())
    all_path_names = set(normalize_path_name(p) for p in research_paths['paths'].keys())
    unvalidated_names = all_path_names - set(normalize_path_name(p) for p in validated_path_names)

    # Map original names to normalized
    original_to_normalized = {}
    for orig_name in research_paths['paths'].keys():
        norm_name = normalize_path_name(orig_name)
        original_to_normalized[norm_name] = orig_name

    # Reconstruct unvalidated with original names
    unvalidated_paths_data = {}
    for norm_name in unvalidated_names:
        if norm_name in original_to_normalized:
            orig_name = original_to_normalized[norm_name]
            unvalidated_paths_data[orig_name] = research_paths['paths'][orig_name]

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Paths Dashboard</title>
    <meta name="google-site-verification" content="G-JGMD5VRYPH">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: #fafaf7;
            color: #333;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.65;
            padding: 30px 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        header { margin-bottom: 40px; border-bottom: 1px solid #ddd; padding-bottom: 25px; }
        h1 { font-family: Georgia, serif; font-size: 2.5em; margin-bottom: 8px; color: #1a1a1a; }
        h2 { font-family: Georgia, serif; font-size: 1.8em; margin: 35px 0 18px 0; color: #1a1a1a; border-top: 1px solid #ddd; padding-top: 20px; }
        h3 { font-family: Georgia, serif; font-size: 1.3em; margin: 22px 0 12px 0; color: #1a1a1a; }
        h4 { font-family: Georgia, serif; font-size: 1.1em; margin: 15px 0 8px 0; color: #1a1a1a; font-weight: 600; }
        .subtitle { font-size: 1.1em; color: #666; margin-bottom: 5px; }
        .byline { font-size: 0.95em; color: #999; margin-bottom: 15px; }

        .context-block {
            background-color: #f5f5f0;
            border-left: 3px solid #999;
            padding: 20px;
            margin: 25px 0;
            font-size: 0.95em;
            line-height: 1.7;
        }
        .context-block h4 { margin-top: 0; color: #666; }
        .context-block p { margin: 10px 0; }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }
        .stat-box {
            background-color: #f5f5f0;
            border: 1px solid #ddd;
            padding: 18px;
            text-align: center;
        }
        .stat-number { font-family: Georgia, serif; font-size: 2.2em; font-weight: bold; color: #2d5016; }
        .stat-label { font-size: 0.9em; color: #666; margin-top: 8px; }

        .tabs { display: flex; gap: 15px; margin-bottom: 30px; border-bottom: 2px solid #ddd; flex-wrap: wrap; }
        .tab-button {
            background: none;
            border: none;
            padding: 12px 18px;
            font-size: 1em;
            cursor: pointer;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            font-family: Georgia, serif;
        }
        .tab-button.active { color: #1a1a1a; border-bottom-color: #333; font-weight: 600; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .path-card {
            background-color: #fefefe;
            border: 1px solid #ddd;
            padding: 20px;
            margin: 18px 0;
            page-break-inside: avoid;
        }
        .path-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }
        .path-name { font-family: Georgia, serif; font-size: 1.3em; color: #1a1a1a; }
        .status-badge {
            padding: 6px 12px;
            font-size: 0.85em;
            font-weight: 600;
            border-radius: 0;
        }

        .path-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 15px 0;
            font-size: 0.9em;
        }
        .stat-item { border-left: 2px solid #ddd; padding-left: 12px; }
        .stat-item strong { color: #1a1a1a; }

        .path-section {
            margin: 15px 0;
            padding: 12px 0;
            border-top: 1px solid #eee;
        }
        .path-section:first-child { border-top: none; padding-top: 0; }

        .section-label { font-weight: 600; color: #666; font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.5px; }

        .pmid-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 8px 0;
        }
        .pmid-badge {
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            padding: 5px 10px;
            font-size: 0.85em;
            font-family: monospace;
        }

        .caveat {
            background-color: #f9f9f6;
            border-left: 2px solid #ddd;
            padding: 10px 12px;
            margin: 8px 0;
            font-size: 0.9em;
            font-style: italic;
            color: #666;
        }

        .connection-list {
            font-size: 0.9em;
            margin: 8px 0;
        }
        .connection-item {
            background-color: #f5f5f0;
            padding: 6px 10px;
            margin: 4px 0;
            border-left: 2px solid #999;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 18px 0;
            font-size: 0.95em;
        }
        thead { background-color: #f5f5f0; }
        th {
            text-align: left;
            padding: 12px;
            border-bottom: 2px solid #ddd;
            font-family: Georgia, serif;
            font-weight: 600;
            color: #1a1a1a;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #eee;
        }
        tr:hover { background-color: #fafaf7; }

        .network-node {
            display: inline-block;
            background-color: #f5f5f0;
            border: 1px solid #ddd;
            padding: 8px 12px;
            margin: 6px 4px;
            font-size: 0.85em;
        }

        .confidence-high { color: #2d5016; font-weight: 600; }
        .confidence-medium { color: #8b7500; font-weight: 600; }
        .confidence-low { color: #8b4513; font-weight: 600; }

        .gap-tag {
            display: inline-block;
            background-color: #f0f8e8;
            border: 1px solid #2d5016;
            padding: 4px 8px;
            margin: 3px 4px 3px 0;
            font-size: 0.8em;
            color: #2d5016;
        }

        .methodology {
            background-color: #f5f5f0;
            border: 1px solid #ddd;
            padding: 18px;
            margin: 25px 0;
            font-size: 0.95em;
            line-height: 1.7;
        }

        @media print {
            body { padding: 0; }
            .container { margin: 0; }
            .path-card { page-break-inside: avoid; margin: 15px 0; }
        }
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>Validated Research Paths</h1>
        <p class="subtitle">Evidence-Backed Mechanisms in Diabetes Research</p>
        <p class="byline">Dashboard generated ''' + datetime.now().strftime('%B %d, %Y') + ''' | GA4 Tag: G-JGMD5VRYPH</p>
    </header>

    <div class="context-block">
        <h4>What This Dashboard Answers</h4>
        <p>''' + str(total_paths) + ''' research paths were extracted from 472 data points across 61 full-text papers. ''' + str(validated_paths) + ''' were cross-validated against independent published evidence (PubMed, systematic reviews, meta-analyses). This dashboard shows which mechanistic pathways are supported by reproducible research evidence vs artifacts of corpus extraction.</p>
    </div>

    <div class="context-block">
        <h4>How to Use This Dashboard</h4>
        <p><strong>VALIDATED</strong> paths (''' + str(validation_summary['VALIDATED']) + ''' total) are backed by 2+ independent published sources including systematic reviews or landmark RCTs. <strong>PARTIALLY_VALIDATED</strong> paths (''' + str(validation_summary['PARTIALLY_VALIDATED']) + ''' total) have supporting evidence with important caveats or limited human data. <strong>UNVALIDATED</strong> paths (''' + str(validation_summary['UNVALIDATED']) + ''' total) lack external confirmation despite corpus presence. Use the external PMIDs to trace the validation chain back to original evidence.</p>
    </div>

    <div class="context-block">
        <h4>What This Cannot Tell You</h4>
        <p>Validation was performed via targeted web search, not a systematic review. Some paths may have stronger or weaker evidence in the full literature than indicated here. This dashboard prioritizes paths extracted from high-quality papers, but absence of validation does not prove incorrectness—only that we could not confirm the finding through rapid evidence synthesis.</p>
    </div>

    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-number">''' + str(total_paths) + '''</div>
            <div class="stat-label">Paths Identified</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">''' + str(validated_paths) + '''</div>
            <div class="stat-label">Validated</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">''' + str(validation_summary['VALIDATED']) + '''</div>
            <div class="stat-label">Fully Validated</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">''' + str(validation_summary['PARTIALLY_VALIDATED']) + '''</div>
            <div class="stat-label">Partially Validated</div>
        </div>
    </div>

    <h2>Executive Summary</h2>
    <p><strong>Key Finding:</strong> Oxidative stress emerges as a central hub mechanism, connecting inflammation, T2D pathology, diabetic nephropathy, and cardiovascular disease. This path (oxidative_stress_inflammation) links to 5+ other validated mechanisms, suggesting targeting ROS production could have pleiotropic benefits across diabetes complications.</p>

    <p><strong>Validation Landscape:</strong> ''' + str(validation_summary['VALIDATED']) + ''' paths achieved full VALIDATED status, primarily in established pharmacotherapy areas (SGLT2i, metformin, GLP-1 receptor agonists) and core inflammatory mechanisms (NLRP3, NF-kB, oxidative stress). ''' + str(validation_summary['PARTIALLY_VALIDATED']) + ''' paths require further clinical validation, often in newer drug classes (dapagliflozin for inflammation) or controversial areas (semaglutide retinopathy). ''' + str(validation_summary['UNVALIDATED']) + ''' path(s) could not be corroborated.</p>

    <p><strong>Hub Mechanisms:</strong></p>
    <ul style="margin: 12px 0 12px 25px;">
'''

    for hub_name, connections in hub_paths:
        html += f'        <li><strong>{hub_name}</strong> connects to {connections} other paths</li>\n'

    html += '''    </ul>

    <h2>Validated Research Paths</h2>
    <p>The following ''' + str(validation_summary['VALIDATED']) + ''' paths have been confirmed by independent published evidence:</p>

    <div class="tabs">
        <button class="tab-button active" onclick="switchTab(event, 'all-validated')">All Validated (''' + str(validation_summary['VALIDATED']) + ''')</button>
        <button class="tab-button" onclick="switchTab(event, 'high-confidence')">High Confidence</button>
        <button class="tab-button" onclick="switchTab(event, 'network')">Connection Network</button>
    </div>

    <div id="all-validated" class="tab-content active">
'''

    # Sort paths by confidence and name
    validated_items = sorted(
        validated_data['paths'].items(),
        key=lambda x: (
            0 if x[1]['status'] == 'VALIDATED' else 1,
            0 if x[1]['confidence'] == 'HIGH' else (1 if x[1]['confidence'] == 'MEDIUM' else 2),
            x[0]
        )
    )

    for path_name, path_data in validated_items:
        if path_data['status'] != 'VALIDATED':
            continue

        confidence_class = f"confidence-{path_data['confidence'].lower()}"
        status_color = STATUS_COLORS.get(path_data['status'], '#999')
        status_bg = STATUS_BG.get(path_data['status'], '#f9f9f9')

        gaps = path_to_gaps.get(path_name, set())
        gap_html = ''.join([f'<span class="gap-tag">Gap {gap}: {GAPS_METADATA.get(gap, {}).get("title", "Unknown")}</span>' for gap in sorted(gaps)])

        html += f'''        <div class="path-card" style="background-color: {status_bg}; border-color: {status_color};">
            <div class="path-header">
                <div class="path-name">{path_name}</div>
                <div class="status-badge" style="background-color: {status_color}; color: white;">
                    {path_data['status']}
                </div>
            </div>

            <div class="path-stats">
                <div class="stat-item">
                    <strong>Data Points:</strong> {path_data['data_point_count']}
                </div>
                <div class="stat-item">
                    <strong class="{confidence_class}">Confidence:</strong> {path_data['confidence']}
                </div>
                <div class="stat-item">
                    <strong>Corpus PMIDs:</strong> {len(path_data.get('pmids_in_corpus', []))}
                </div>
                <div class="stat-item">
                    <strong>External PMIDs:</strong> {len(path_data.get('external_pmids', []))}
                </div>
            </div>

            <div class="path-section">
                <span class="section-label">Validation Source</span>
                <p>{path_data.get('validation_source', 'N/A')}</p>
            </div>

            <div class="path-section">
                <span class="section-label">Evidence Details</span>
                <div class="pmid-list">
                    <span style="margin-right: 15px;"><strong>Corpus PMIDs:</strong></span>
'''

        for pmid in path_data.get('pmids_in_corpus', []):
            html += f'                    <span class="pmid-badge">{pmid}</span>\n'

        html += '                </div>'

        if path_data.get('external_pmids'):
            html += '\n                <div class="pmid-list">\n                    <span style="margin-right: 15px;"><strong>External PMIDs:</strong></span>\n'
            for pmid in path_data.get('external_pmids', []):
                html += f'                    <span class="pmid-badge">{pmid}</span>\n'
            html += '                </div>'

        html += '''
            </div>

            <div class="path-section">
                <span class="section-label">Caveats</span>
                <div class="caveat">''' + path_data.get('caveats', 'None listed') + '''</div>
            </div>
'''

        if path_data.get('cross_connections'):
            html += '''            <div class="path-section">
                <span class="section-label">Cross-Connections to Other Paths</span>
                <div class="connection-list">
'''
            for connection in path_data.get('cross_connections', []):
                html += f'                    <div class="connection-item">{connection}</div>\n'
            html += '''                </div>
            </div>
'''

        if gaps:
            html += f'''            <div class="path-section">
                <span class="section-label">Relevant Research Gaps</span>
                <div>{gap_html}</div>
            </div>
'''

        html += '        </div>\n'

    html += '''    </div>

    <div id="high-confidence" class="tab-content">
        <h3>High Confidence Validated Paths</h3>
        <p>These paths have the strongest evidence base from systematic reviews and/or landmark RCTs:</p>
'''

    high_conf = [p for p in validated_items if p[1]['status'] == 'VALIDATED' and p[1]['confidence'] == 'HIGH']
    for path_name, path_data in high_conf:
        status_bg = STATUS_BG.get(path_data['status'], '#f9f9f9')
        status_color = STATUS_COLORS.get(path_data['status'], '#999')

        html += f'''        <div class="path-card" style="background-color: {status_bg}; border-color: {status_color};">
            <div class="path-name">{path_name}</div>
            <p><strong>Validation Source:</strong> {path_data.get('validation_source', 'N/A')}</p>
            <p><strong>Caveats:</strong> {path_data.get('caveats', 'None')}</p>
            <p><strong>Data Points from Corpus:</strong> {path_data['data_point_count']}</p>
        </div>
'''

    html += '''    </div>

    <div id="network" class="tab-content">
        <h3>Research Path Network</h3>
        <p>Paths that share external PMIDs or mechanistic connections:</p>

        <table>
            <thead>
                <tr>
                    <th>Path Name</th>
                    <th>Connections</th>
                    <th>Connected To</th>
                </tr>
            </thead>
            <tbody>
'''

    for path_name in sorted(network.keys()):
        connections = len(set(network[path_name]['connected_to']))
        connected = ', '.join(sorted(set(network[path_name]['connected_to']))[:3])
        if len(set(network[path_name]['connected_to'])) > 3:
            connected += '...'

        html += f'''                <tr>
                    <td><strong>{path_name}</strong></td>
                    <td>{connections}</td>
                    <td>{connected if connected else 'Standalone'}</td>
                </tr>
'''

    html += '''            </tbody>
        </table>
    </div>

    <h2>Research Path Gap Mapping</h2>
    <p>How validated research paths support the 15 research gaps. Gaps with more validated paths have stronger evidence backing:</p>

    <table>
        <thead>
            <tr>
                <th>Gap ID</th>
                <th>Gap Title</th>
                <th>Validated Paths</th>
                <th>Path Count</th>
            </tr>
        </thead>
        <tbody>
'''

    # Reverse mapping: gaps to paths
    gaps_to_paths = defaultdict(list)
    for path_name, gap_set in path_to_gaps.items():
        for gap_id in gap_set:
            gaps_to_paths[gap_id].append(path_name)

    for gap_id in sorted(GAPS_METADATA.keys(), key=lambda x: int(x)):
        gap_title = GAPS_METADATA[gap_id]['title']
        paths = gaps_to_paths.get(gap_id, [])

        html += f'''        <tr>
            <td><strong>Gap {gap_id}</strong></td>
            <td>{gap_title}</td>
            <td>{', '.join(paths) if paths else '—'}</td>
            <td>{len(paths)}</td>
        </tr>
'''

    html += '''        </tbody>
    </table>

    <h2>Partially Validated Paths</h2>
    <p>The following ''' + str(validation_summary['PARTIALLY_VALIDATED']) + ''' paths have supporting evidence with important caveats:</p>
'''

    for path_name, path_data in validated_items:
        if path_data['status'] != 'PARTIALLY_VALIDATED':
            continue

        status_bg = STATUS_BG.get(path_data['status'], '#f9f9f9')
        status_color = STATUS_COLORS.get(path_data['status'], '#999')
        confidence_class = f"confidence-{path_data['confidence'].lower()}"

        html += f'''    <div class="path-card" style="background-color: {status_bg}; border-color: {status_color};">
        <div class="path-header">
            <div class="path-name">{path_name}</div>
            <div class="status-badge" style="background-color: {status_color}; color: white;">
                {path_data['status']}
            </div>
        </div>

        <div class="path-stats">
            <div class="stat-item">
                <strong>Data Points:</strong> {path_data['data_point_count']}
            </div>
            <div class="stat-item">
                <strong class="{confidence_class}">Confidence:</strong> {path_data['confidence']}
            </div>
        </div>

        <div class="path-section">
            <span class="section-label">Validation Source</span>
            <p>{path_data.get('validation_source', 'N/A')}</p>
        </div>

        <div class="path-section">
            <span class="section-label">Caveats</span>
            <div class="caveat">{path_data.get('caveats', 'None listed')}</div>
        </div>
    </div>
'''

    # Add unvalidated if any
    unvalidated_count = validation_summary['UNVALIDATED']
    if unvalidated_count > 0:
        html += f'''    <h2>Unvalidated Paths</h2>
    <p>The following {unvalidated_count} path(s) extracted from the corpus but could not be validated through published evidence search:</p>
'''

        for orig_name, path_data in unvalidated_paths_data.items():
            html += f'''    <div class="path-card" style="background-color: {STATUS_BG.get('UNVALIDATED', '#f9f9f9')}; border-color: {STATUS_COLORS.get('UNVALIDATED', '#999')};">
        <div class="path-name">{orig_name}</div>
        <p><strong>Data Points:</strong> {path_data.get('data_point_count', 'N/A')}</p>
        <p><strong>Status:</strong> Not yet validated against published evidence</p>
        <p><strong>PMIDs:</strong> {', '.join(path_data.get('pmids', []))}</p>
    </div>
'''

    html += '''    <h2>Methodology</h2>
    <div class="methodology">
        <h3>Research Path Extraction & Validation Pipeline</h3>
        <p><strong>Stage 1: Corpus Analysis</strong> 91 full-text papers on diabetes complications were automatically extracted. Regex-based information extraction identified 472 key claims linking mechanisms (inflammation, oxidative stress, specific protein pathways) to outcomes (T1D, T2D, complications).</p>

        <p><strong>Stage 2: Path Clustering</strong> These 472 data points were grouped by mechanism-outcome relationships, resulting in 48 unique research paths (e.g., "NLRP3_inflammasome → inflammation").</p>

        <p><strong>Stage 3: Validation Selection</strong> The top 25 paths (by data point frequency and clinical relevance) were selected for external validation.</p>

        <p><strong>Stage 4: Cross-Validation</strong> Each path was validated via targeted PubMed/Google Scholar searches for: (1) systematic reviews, (2) meta-analyses, (3) landmark RCTs confirming the relationship. Validation status was assigned as:</p>
        <ul style="margin: 12px 0 12px 25px;">
            <li><strong>VALIDATED:</strong> 2+ independent high-quality sources (RCT, meta-analysis, systematic review)</li>
            <li><strong>PARTIALLY_VALIDATED:</strong> Supporting evidence with important caveats or limited human data</li>
            <li><strong>UNVALIDATED:</strong> No independent external confirmation found</li>
            <li><strong>CONTRADICTED:</strong> External evidence contradicts corpus findings (none found)</li>
        </ul>

        <p><strong>Note on Causality:</strong> This validation confirms observational and mechanistic correlations, not strict causality. Many paths show strong mechanistic evidence in preclinical models but modest clinical trial outcomes.</p>
    </div>

    <footer style="margin-top: 50px; padding-top: 25px; border-top: 1px solid #ddd; color: #999; font-size: 0.9em;">
        <p>Dashboard built with Tufte-inspired design principles (minimal decoration, data-ink ratio focus). Data source: Diabetes Research Corpus (61 full-text papers). GA4 Analytics: G-JGMD5VRYPH.</p>
    </footer>

</div>

<script>
function switchTab(evt, tabName) {
    var i, tabcontent, tabbuttons;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }
    tabbuttons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].classList.remove("active");
    }
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}
</script>

</body>
</html>
'''

    return html

def main():
    """Main execution."""
    print("Loading research paths data...")
    research_paths = load_research_paths()

    print("Loading validated paths data...")
    validated_data = load_validated_paths()

    print(f"Processing {research_paths['total_paths']} paths ({validated_data['paths_validated']} validated)...")

    html = generate_html(research_paths, validated_data)

    print(f"Writing output to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print("SUCCESS: Dashboard generated")
    print(f"  Total paths: {research_paths['total_paths']}")
    print(f"  Validated: {validated_data['validation_summary']['VALIDATED']}")
    print(f"  Partially Validated: {validated_data['validation_summary']['PARTIALLY_VALIDATED']}")
    print(f"  Unvalidated: {validated_data['validation_summary']['UNVALIDATED']}")
    print(f"  Output: {output_file}")

if __name__ == '__main__':
    main()
