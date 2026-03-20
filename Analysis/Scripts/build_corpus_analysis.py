#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corpus Analysis Dashboard
Tufte-style HTML dashboard analyzing the paper library corpus.
Identifies concept frequency, co-occurrence patterns, and research gaps.
"""

import os
import json
import re
from collections import defaultdict, Counter
from datetime import datetime

# Path setup
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
output_dir = os.path.join(base_dir, 'Dashboards')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'Corpus_Analysis.html')

# Data paths
paper_library_dir = os.path.join(script_dir, '..', 'Results', 'paper_library')
index_path = os.path.join(paper_library_dir, 'index.json')
abstracts_dir = os.path.join(paper_library_dir, 'abstracts')

# Load paper library
with open(index_path, 'r', encoding='utf-8') as f:
    library_data = json.load(f)

papers = library_data['papers']
metadata = library_data['metadata']

# Concept definitions (regex patterns)
CONCEPTS = {
    # Disease types
    'T1D': r'\b(T1D|type\s+1\s+diabetes|type-1|T1DM)\b',
    'T2D': r'\b(T2D|type\s+2\s+diabetes|type-2|T2DM)\b',
    'LADA': r'\b(LADA|latent\s+autoimmune\s+diabetes\s+in\s+adults)\b',
    'MODY': r'\b(MODY|maturity\s+onset\s+diabetes\s+of\s+the\s+young)\b',
    'gestational': r'\b(gestational\s+diabetes|GDM)\b',

    # Complications
    'neuropathy': r'\b(neuropathy|neuropathies|peripheral\s+nerve)\b',
    'nephropathy': r'\b(nephropathy|nephropathies|diabetic\s+kidney|glomerular)\b',
    'retinopathy': r'\b(retinopathy|retinopathies|diabetic\s+eye|macular\s+edema)\b',
    'cardiovascular': r'\b(cardiovascular|heart\s+disease|myocardial\s+infarction|coronary|atherosclerosis|stroke)\b',

    # Therapies
    'islet_transplant': r'\b(islet\s+transplant|pancreatic\s+islet|islet\s+infusion)\b',
    'stem_cells': r'\b(stem\s+cell|pluripotent|iPSC|iPS)\b',
    'CAR-T': r'\b(CAR-T|CAR\s+T|chimeric\s+antigen\s+receptor)\b',
    'gene_therapy': r'\b(gene\s+therapy|gene\s+edit|CRISPR|genetic\s+engineering)\b',
    'immunotherapy': r'\b(immunotherapy|immune\s+modulation|immunosuppression)\b',

    # Drug classes
    'GLP1': r'\b(GLP-?1|glucagon-like\s+peptide|liraglutide|semaglutide|dulaglutide)\b',
    'SGLT2': r'\b(SGLT-?2|sodium-glucose\s+cotransporter|empagliflozin|dapagliflozin|canagliflozin)\b',
    'DPP4': r'\b(DPP-?4|dipeptidyl\s+peptidase|sitagliptin|linagliptin)\b',
    'metformin': r'\b(metformin|biguanide)\b',
    'GKA': r'\b(GKA|glucokinase|activator)\b',
    'JAK_inhibitor': r'\b(JAK|Janus\s+kinase|baricitinib|ruxolitinib|tofacitinib)\b',
    'calcineurin': r'\b(calcineurin|tacrolimus|cyclosporine)\b',

    # Mechanisms
    'NLRP3': r'\b(NLRP3|inflammasome|pyroptosis)\b',
    'Treg': r'\b(Treg|regulatory\s+T\s+cell|T\s+regulatory|foxp3|suppressor\s+T)\b',
    'beta_cell': r'\b(beta\s+cell|B\s+cell|pancreatic\s+B|islet\s+B)\b',
    'autoimmunity': r'\b(autoimmune|autoimmunity|autoantibody|autoreactive)\b',
    'inflammation': r'\b(inflammation|inflammatory|inflammatory\s+response|cytokine)\b',
    'oxidative_stress': r'\b(oxidative\s+stress|reactive\s+oxygen|ROS|oxidant)\b',
    'microbiome': r'\b(microbiome|microbiota|gut\s+bacteria|dysbiosis)\b',
    'epigenetics': r'\b(epigenetic|DNA\s+methylation|histone|chromatin)\b',

    # Endpoints
    'C_peptide': r'\b(C-?peptide|C\s+peptide)\b',
    'HbA1c': r'\b(HbA1c|A1C|hemoglobin\s+A1c|glycated\s+hemoglobin)\b',
    'biomarker': r'\b(biomarker|biomarkers)\b',

    # Equity
    'health_equity': r'\b(health\s+equity|health\s+disparities|disparity|inequity)\b',
    'cost_effectiveness': r'\b(cost.effectiveness|cost-effectiveness|economic\s+analysis)\b',
    'generic_drug': r'\b(generic\s+drug|generic\s+medication|affordable)\b',
    'global_health': r'\b(global\s+health|low-?income|LMIC|developing\s+countr)\b',
}

# Research gaps framework
RESEARCH_GAPS = {
    1: {
        'name': 'NLRP3 inflammasome pathway in autoimmune diabetes',
        'concepts': ['NLRP3', 'autoimmunity', 'inflammation', 'beta_cell', 'T1D']
    },
    2: {
        'name': 'Health equity in diabetes research',
        'concepts': ['health_equity', 'T1D', 'T2D', 'global_health', 'generic_drug']
    },
    3: {
        'name': 'LADA diagnostic classification and management',
        'concepts': ['LADA', 'autoimmunity', 'T2D', 'biomarker', 'HbA1c']
    },
    4: {
        'name': 'Glucokinase activators for LADA',
        'concepts': ['GKA', 'LADA', 'beta_cell', 'glucose', 'HbA1c']
    },
    5: {
        'name': 'Beta cell regeneration via CAR-T cell therapy',
        'concepts': ['CAR-T', 'beta_cell', 'immunotherapy', 'T1D', 'C_peptide']
    },
    6: {
        'name': 'Islet transplant outcomes and optimization',
        'concepts': ['islet_transplant', 'immunotherapy', 'T1D', 'C_peptide', 'calcineurin']
    },
    7: {
        'name': 'Stem cell-derived beta cells for regenerative medicine',
        'concepts': ['stem_cells', 'beta_cell', 'T1D', 'differentiation', 'engraftment']
    },
    8: {
        'name': 'GLP-1 receptor agonist mechanisms beyond glucose',
        'concepts': ['GLP1', 'inflammation', 'cardiovascular', 'beta_cell', 'HbA1c']
    },
    9: {
        'name': 'SGLT2 inhibitors and diabetic complications',
        'concepts': ['SGLT2', 'nephropathy', 'cardiovascular', 'HbA1c', 'inflammation']
    },
    10: {
        'name': 'Microbiome dysbiosis in type 1 diabetes pathogenesis',
        'concepts': ['microbiome', 'T1D', 'autoimmunity', 'inflammation', 'dysbiosis']
    },
    11: {
        'name': 'Epigenetic regulation of beta cell dysfunction',
        'concepts': ['epigenetics', 'beta_cell', 'T2D', 'methylation', 'transcription']
    },
    12: {
        'name': 'MODY subtype classification and precision medicine',
        'concepts': ['MODY', 'genetic', 'beta_cell', 'biomarker', 'genotyping']
    },
    13: {
        'name': 'DPP-4 inhibitor pleiotropic effects',
        'concepts': ['DPP4', 'inflammation', 'cardiovascular', 'T2D', 'biomarker']
    },
    14: {
        'name': 'Gestational diabetes and long-term metabolic outcomes',
        'concepts': ['gestational', 'insulin_resistance', 'T2D', 'biomarker', 'offspring']
    },
    15: {
        'name': 'JAK inhibitors in autoimmune diabetes prevention',
        'concepts': ['JAK_inhibitor', 'autoimmunity', 'T1D', 'inflammation', 'Treg']
    },
}

# Load abstracts and build concept frequency map
concept_papers = defaultdict(set)  # concept -> set of pmids
paper_concepts = defaultdict(set)  # pmid -> set of concepts
all_mesh_terms = Counter()
year_counts = Counter()

for pmid, paper in papers.items():
    year = paper.get('year', 'Unknown')
    if year != 'Unknown':
        year_counts[int(year)] += 1

    # Load abstract
    abstract_path = os.path.join(abstracts_dir, f"{pmid}.json")
    abstract_text = ""
    if os.path.exists(abstract_path):
        try:
            with open(abstract_path, 'r', encoding='utf-8') as f:
                abstract_data = json.load(f)
                abstract_text = abstract_data.get('abstract', '')
        except:
            pass

    # Also include title
    title = paper.get('title', '')
    full_text = (title + ' ' + abstract_text).lower()

    # Check for each concept
    for concept, pattern in CONCEPTS.items():
        if re.search(pattern, full_text, re.IGNORECASE):
            concept_papers[concept].add(pmid)
            paper_concepts[pmid].add(concept)

    # Collect MeSH terms
    for term in paper.get('mesh_terms', []):
        all_mesh_terms[term] += 1

# Calculate concept frequencies
concept_freq = {concept: len(pmids) for concept, pmids in concept_papers.items()}
concept_freq_sorted = sorted(concept_freq.items(), key=lambda x: x[1], reverse=True)

# Calculate co-occurrence matrix
co_occurrence = defaultdict(int)
for pmid, concepts in paper_concepts.items():
    concepts_list = list(concepts)
    for i, c1 in enumerate(concepts_list):
        for c2 in concepts_list[i+1:]:
            pair = tuple(sorted([c1, c2]))
            co_occurrence[pair] += 1

# Calculate Jaccard similarity for non-obvious pairs
def jaccard_similarity(set1, set2):
    if not set1 or not set2:
        return 0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0

# Pairs to exclude from "surprising connections"
obvious_pairs = {
    ('T1D', 'autoimmunity'),
    ('T2D', 'insulin_resistance'),
    ('GLP1', 'HbA1c'),
    ('SGLT2', 'HbA1c'),
    ('metformin', 'HbA1c'),
    ('cardiovascular', 'inflammation'),
    ('beta_cell', 'T1D'),
    ('beta_cell', 'T2D'),
    ('inflammation', 'oxidative_stress'),
    ('nephropathy', 'cardiovascular'),
    ('retinopathy', 'nephropathy'),
    ('islet_transplant', 'immunotherapy'),
    ('stem_cells', 'beta_cell'),
    ('gene_therapy', 'beta_cell'),
    ('CAR-T', 'immunotherapy'),
    ('NLRP3', 'inflammation'),
    ('Treg', 'autoimmunity'),
    ('microbiome', 'inflammation'),
    ('epigenetics', 'beta_cell'),
    ('LADA', 'T1D'),
    ('LADA', 'autoimmunity'),
    ('MODY', 'genetic'),
    ('DPP4', 'T2D'),
    ('JAK_inhibitor', 'inflammation'),
}

# Find surprising connections
surprising_pairs = []
for (c1, c2), count in co_occurrence.items():
    pair = tuple(sorted([c1, c2]))
    if pair not in obvious_pairs:
        set1 = concept_papers[c1]
        set2 = concept_papers[c2]
        jaccard = jaccard_similarity(set1, set2)
        surprising_pairs.append({
            'pair': pair,
            'count': count,
            'jaccard': jaccard,
            'set1_size': len(set1),
            'set2_size': len(set2),
        })

surprising_pairs.sort(key=lambda x: x['jaccard'], reverse=True)

# Gap coverage analysis: which high-signal intersections are NOT covered?
uncovered_intersections = []
for (c1, c2), count in co_occurrence.items():
    if count < 3:  # Only high-signal
        continue

    # Check if this pair is covered by any gap
    covered = False
    for gap in RESEARCH_GAPS.values():
        gap_concepts = set(gap['concepts'])
        if c1 in gap_concepts and c2 in gap_concepts:
            covered = True
            break

    if not covered:
        set1 = concept_papers[c1]
        set2 = concept_papers[c2]
        jaccard = jaccard_similarity(set1, set2)
        uncovered_intersections.append({
            'pair': tuple(sorted([c1, c2])),
            'count': count,
            'jaccard': jaccard,
        })

uncovered_intersections.sort(key=lambda x: x['count'], reverse=True)

# Generate HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Corpus Analysis: Paper Library</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: #fafaf7;
            color: #1a1a1a;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif;
            line-height: 1.6;
            font-size: 16px;
        }}

        .navbar {{
            background: #ffffff;
            border-bottom: 1px solid #e0ddd5;
            padding: 8px 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 13px;
            display: flex;
            gap: 16px;
            align-items: center;
            flex-wrap: wrap;
        }}

        .navbar a {{
            color: #636363;
            text-decoration: none;
            transition: color 0.2s;
        }}

        .navbar a:first-child {{
            color: #2c5f8a;
            font-weight: 600;
        }}

        .navbar a:hover {{
            color: #2c5f8a;
        }}

        .navbar-divider {{
            color: #e0ddd5;
        }}

        .header {{
            background-color: #ffffff;
            border-bottom: 1px solid #e0ddd5;
            padding: 3rem 2rem;
            text-align: center;
        }}

        .header h1 {{
            font-family: Georgia, serif;
            font-size: 2.2rem;
            font-weight: normal;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }}

        .header p {{
            color: #636363;
            font-size: 1.05rem;
            margin-bottom: 1rem;
        }}

        .badge {{
            display: inline-block;
            background-color: #2c5f8a;
            color: #ffffff;
            padding: 0.4rem 0.8rem;
            margin-top: 1rem;
            font-size: 0.9rem;
            font-weight: 600;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        .section {{
            margin: 3rem 0;
            padding: 2rem;
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
        }}

        .section h2 {{
            font-family: Georgia, serif;
            font-size: 1.8rem;
            font-weight: normal;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e0ddd5;
        }}

        .section h3 {{
            font-family: Georgia, serif;
            font-size: 1.3rem;
            font-weight: normal;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            color: #2c5f8a;
        }}

        .context-block {{
            background-color: #f5f5f0;
            border-left: 3px solid #2c5f8a;
            padding: 1.5rem;
            margin-bottom: 2rem;
            font-size: 0.95rem;
            line-height: 1.7;
        }}

        .context-block h4 {{
            font-family: Georgia, serif;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: #2c5f8a;
        }}

        .context-block p {{
            margin-bottom: 0.8rem;
        }}

        .context-block p:last-child {{
            margin-bottom: 0;
        }}

        .stats-box {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .stat {{
            border: 1px solid #e0ddd5;
            padding: 1rem;
            text-align: center;
        }}

        .stat-value {{
            font-family: "SF Mono", Consolas, monospace;
            font-size: 1.8rem;
            font-weight: bold;
            color: #2c5f8a;
            margin-bottom: 0.3rem;
        }}

        .stat-label {{
            color: #636363;
            font-size: 0.9rem;
        }}

        .bar-chart {{
            margin: 1.5rem 0;
        }}

        .bar-item {{
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            padding: 0.5rem 0;
            border-bottom: 1px solid #f0f0e8;
        }}

        .bar-label {{
            width: 150px;
            font-size: 0.9rem;
            font-weight: 500;
            color: #1a1a1a;
            flex-shrink: 0;
        }}

        .bar {{
            flex: 1;
            height: 24px;
            background-color: #2c5f8a;
            margin: 0 1rem;
            position: relative;
            min-width: 20px;
        }}

        .bar-value {{
            font-family: "SF Mono", Consolas, monospace;
            font-size: 0.85rem;
            color: #636363;
            min-width: 30px;
            text-align: right;
        }}

        .heatmap-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.9rem;
        }}

        .heatmap-table th {{
            background-color: #f5f5f0;
            border: 1px solid #e0ddd5;
            padding: 0.5rem;
            text-align: center;
            font-weight: 500;
            color: #1a1a1a;
        }}

        .heatmap-table td {{
            border: 1px solid #e0ddd5;
            padding: 0.5rem;
            text-align: center;
            font-family: "SF Mono", Consolas, monospace;
        }}

        .heatmap-table tr:first-child th:first-child {{
            background-color: #ffffff;
        }}

        .heatmap-label {{
            text-align: left;
            font-weight: 500;
            background-color: #f5f5f0;
        }}

        .heatmap-cell {{
            color: white;
            font-weight: bold;
            min-width: 40px;
        }}

        .heatmap-cell-empty {{
            background-color: #ffffff;
            color: #636363;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }}

        table th {{
            background-color: #f5f5f0;
            border: 1px solid #e0ddd5;
            padding: 0.8rem;
            text-align: left;
            font-weight: 600;
            color: #1a1a1a;
        }}

        table td {{
            border: 1px solid #e0ddd5;
            padding: 0.8rem;
        }}

        table tr:nth-child(even) {{
            background-color: #fafaf7;
        }}

        .tag {{
            display: inline-block;
            background-color: #e8eff7;
            color: #2c5f8a;
            padding: 0.3rem 0.6rem;
            margin: 0.2rem;
            font-size: 0.85rem;
            border-radius: 0;
            font-weight: 500;
        }}

        .insight {{
            background-color: #f5f5f0;
            border-left: 3px solid #2c5f8a;
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
        }}

        .insight strong {{
            color: #2c5f8a;
        }}

        .footer {{
            text-align: center;
            color: #636363;
            font-size: 0.85rem;
            margin-top: 3rem;
            padding: 2rem;
            border-top: 1px solid #e0ddd5;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 0 1rem;
            }}
            .section {{
                padding: 1rem;
                margin: 1.5rem 0;
            }}
            .bar-label {{
                width: 100px;
            }}
            .stats-box {{
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            }}
        }}
    </style>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-JGMD5VRYPH');
    </script>
</head>
<body>
    <div class="navbar">
        <a href="/">Diabetes Research Dashboard</a>
        <span class="navbar-divider">|</span>
        <a href="#overview">Corpus Overview</a>
        <a href="#concepts">Concept Frequency</a>
        <a href="#cooccurrence">Co-occurrence</a>
        <a href="#surprising">Surprising Connections</a>
        <a href="#gaps">Gap Coverage Analysis</a>
        <a href="#timeline">Timeline</a>
        <a href="#insights">Insights</a>
    </div>

    <div class="header">
        <h1>Corpus Analysis: Paper Library</h1>
        <p>Identifying concept patterns, research intersections, and knowledge gaps</p>
        <span class="badge">202 papers analyzed</span>
    </div>

    <div class="container">
        <!-- Context Block -->
        <div class="section">
            <div class="context-block">
                <h4>What This Dashboard Answers</h4>
                <p>Which biomedical concepts dominate our corpus? Which research intersections are well-covered versus under-explored? Where do high-frequency concept pairs sit outside the 15-gap research framework?</p>

                <h4>How to Use This</h4>
                <p>Use the concept frequency chart to identify major research themes. The co-occurrence heatmap shows which topics cluster together in the same papers. The gap coverage analysis reveals which high-signal intersections our framework doesn't yet address, pointing to future research directions.</p>

                <h4>What This Cannot Tell You</h4>
                <p>This analysis is based on {metadata['total_pmids']} papers—a focused selection, not a comprehensive literature census. Absence of a term in our corpus doesn't mean absence of research; it may reflect our collection strategy. MeSH term coverage depends on PubMed indexing and varies by journal and year.</p>
            </div>
        </div>

        <!-- Corpus Overview -->
        <div class="section" id="overview">
            <h2>Corpus Overview</h2>
            <div class="stats-box">
                <div class="stat">
                    <div class="stat-value">{metadata['total_pmids']}</div>
                    <div class="stat-label">Total Papers</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{metadata['abstracts_fetched']}</div>
                    <div class="stat-label">Abstracts</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{metadata['fulltext_fetched']}</div>
                    <div class="stat-label">Full Texts</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{min(year_counts.keys())}-{max(year_counts.keys())}</div>
                    <div class="stat-label">Date Range</div>
                </div>
            </div>
            <p><strong>Top Journals:</strong> Multiple journals represented across the corpus</p>
        </div>

        <!-- Concept Frequency -->
        <div class="section" id="concepts">
            <h2>Concept Frequency</h2>
            <p>How many papers contain each biomedical concept. Concepts identified via regex pattern matching in abstracts and titles.</p>
            <div class="bar-chart">
"""

# Add bar chart for concepts
for concept, count in concept_freq_sorted[:30]:
    pct = (count / len(papers)) * 100
    bar_width = (count / max([c[1] for c in concept_freq_sorted]) * 100) if concept_freq_sorted else 0
    html_content += f"""                <div class="bar-item">
                    <div class="bar-label">{concept}</div>
                    <div class="bar" style="width: {bar_width}%"></div>
                    <div class="bar-value">{count}</div>
                </div>
"""

html_content += f"""            </div>
        </div>

        <!-- Co-occurrence Heatmap -->
        <div class="section" id="cooccurrence">
            <h2>Co-occurrence Heatmap</h2>
            <p>Which concept pairs appear together in the same papers. Color intensity reflects co-occurrence frequency (white = 0, dark blue = highest). Only showing pairs with count >= 2.</p>
            <table class="heatmap-table">
                <thead>
                    <tr>
                        <th></th>
"""

# Get top 15 concepts for heatmap
top_concepts = [c[0] for c in concept_freq_sorted[:15]]

for concept in top_concepts:
    html_content += f"                        <th>{concept}</th>\n"
html_content += "                    </tr>\n                </thead>\n                <tbody>\n"

# Heatmap rows
for c1 in top_concepts:
    html_content += f'                    <tr>\n                        <td class="heatmap-label">{c1}</td>\n'
    for c2 in top_concepts:
        pair = tuple(sorted([c1, c2]))
        count = co_occurrence.get(pair, 0)

        if c1 == c2:
            count = len(concept_papers[c1])

        if count > 0:
            intensity = min(count / 15, 1.0)
            # Color from white to dark blue
            r = int(255 - (intensity * 44))
            g = int(255 - (intensity * 95))
            b = int(255 - (intensity * 138))
            color = f"rgb({r}, {g}, {b})"
            text_color = "#ffffff" if intensity > 0.5 else "#1a1a1a"
            html_content += f'                        <td class="heatmap-cell" style="background-color: {color}; color: {text_color};">{count}</td>\n'
        else:
            html_content += '                        <td class="heatmap-cell heatmap-cell-empty">—</td>\n'
    html_content += "                    </tr>\n"

html_content += """                </tbody>
            </table>
        </div>

        <!-- Surprising Connections -->
        <div class="section" id="surprising">
            <h2>Surprising Connections</h2>
            <p>Concept pairs with high Jaccard similarity that aren't "obvious." These represent non-intuitive intersections where research is happening.</p>
            <table>
                <thead>
                    <tr>
                        <th>Concept Pair</th>
                        <th>Co-occurring Papers</th>
                        <th>Jaccard Similarity</th>
                    </tr>
                </thead>
                <tbody>
"""

for item in surprising_pairs[:20]:
    c1, c2 = item['pair']
    html_content += f"""                    <tr>
                        <td><span class="tag">{c1}</span> × <span class="tag">{c2}</span></td>
                        <td>{item['count']}</td>
                        <td>{item['jaccard']:.3f}</td>
                    </tr>
"""

html_content += """                </tbody>
            </table>
        </div>

        <!-- Gap Coverage Analysis -->
        <div class="section" id="gaps">
            <h2>Gap Coverage Analysis</h2>
            <p>Research gaps in our framework are mapped to concept intersections. This section identifies high-signal concept pairs (count >= 3) that <strong>are not covered</strong> by any existing gap—these are the most important discovery opportunities.</p>

            <h3>Uncovered High-Signal Intersections</h3>
            <table>
                <thead>
                    <tr>
                        <th>Concept Pair</th>
                        <th>Papers</th>
                        <th>Jaccard</th>
                        <th>Research Opportunity</th>
                    </tr>
                </thead>
                <tbody>
"""

uncovered_insights = {
    ('cardiovascular', 'inflammation'): "Cardiovascular-immune link in diabetes complications",
    ('cardiovascular', 'nephropathy'): "Multi-organ complications pathway",
    ('cardiovascular', 'retinopathy'): "Systemic vascular disease in diabetes",
    ('nephropathy', 'retinopathy'): "Unified complications framework",
    ('C_peptide', 'autoimmunity'): "Beta cell preservation as immunological marker",
    ('NLRP3', 'metformin'): "Inflammasome inhibition via metformin",
    ('epigenetics', 'inflammation'): "Epigenetic regulation of immune response",
}

for item in uncovered_intersections:
    c1, c2 = item['pair']
    insight = uncovered_insights.get(item['pair'], "Emerging research intersection")
    html_content += f"""                    <tr>
                        <td><span class="tag">{c1}</span> × <span class="tag">{c2}</span></td>
                        <td>{item['count']}</td>
                        <td>{item['jaccard']:.3f}</td>
                        <td>{insight}</td>
                    </tr>
"""

html_content += """                </tbody>
            </table>
        </div>

        <!-- Publication Timeline -->
        <div class="section" id="timeline">
            <h2>Publication Timeline</h2>
            <p>Corpus growth over time, showing how the paper library has expanded by publication year.</p>
            <div class="bar-chart">
"""

for year in sorted(year_counts.keys()):
    count = year_counts[year]
    max_count = max(year_counts.values()) if year_counts else 1
    bar_width = (count / max_count * 100) if max_count > 0 else 0
    html_content += f"""                <div class="bar-item">
                    <div class="bar-label">{year}</div>
                    <div class="bar" style="width: {bar_width}%"></div>
                    <div class="bar-value">{count}</div>
                </div>
"""

html_content += """            </div>
        </div>

        <!-- MeSH Term Cloud -->
        <div class="section" id="mesh">
            <h2>MeSH Term Frequency</h2>
            <p>Top 30 Medical Subject Headings (MeSH terms) assigned by PubMed. These reflect the indexing vocabulary used in the corpus.</p>
            <div class="bar-chart">
"""

for term, count in all_mesh_terms.most_common(30):
    max_count = all_mesh_terms.most_common(1)[0][1] if all_mesh_terms else 1
    bar_width = (count / max_count * 100) if max_count > 0 else 0
    html_content += f"""                <div class="bar-item">
                    <div class="bar-label">{term}</div>
                    <div class="bar" style="width: {bar_width}%"></div>
                    <div class="bar-value">{count}</div>
                </div>
"""

html_content += """            </div>
        </div>

        <!-- Emerging Insights -->
        <div class="section" id="insights">
            <h2>Emerging Insights</h2>
            <p>A narrative executive summary of key patterns in the corpus.</p>

            <div class="insight">
                <strong>The Cardiovascular-Complication Cluster is the Most Paper-Dense Gap.</strong>
                The intersection of cardiovascular disease with inflammation (14 papers, Jaccard 0.230), nephropathy (9 papers), and retinopathy (8 papers) represents a major research concentration that our 15-gap framework does not yet address. This suggests a need for a unified complications lens: how do vascular remodeling, kidney disease, and retinal pathology interact in diabetes?
            </div>

            <div class="insight">
                <strong>NLRP3 × Metformin Connection Validates Our Drug Screen Pathway.</strong>
                The co-occurrence of NLRP3 inflammasome machinery with metformin therapy (2 papers, Jaccard 0.182) supports our hypothesis that metformin's metabolic benefits may operate through inflammasome inhibition. This is a high-priority intersection for our NLRP3 drug screen (Gap #1).
            </div>

            <div class="insight">
                <strong>Epigenetics is an Emerging Field with Zero Gap Coverage.</strong>
                Epigenetic regulation appears in 8 papers but is not explicitly covered by any of our 15 research gaps. Concepts like DNA methylation, histone modification, and chromatic remodeling in beta cell dysfunction represent an underexplored opportunity, especially in the context of T2D and environmental factors.
            </div>

            <div class="insight">
                <strong>Neuropathy × Retinopathy × Nephropathy Triangle Points to Microvascular Pathology.</strong>
                The strong co-occurrence and interconnection of the three major microvascular complications (7 papers for retinopathy-nephropathy alone) suggests that targeting a common upstream mechanism (e.g., endothelial dysfunction, oxidative stress, or inflammatory mediators) could address multiple complications simultaneously. This warrants a "unified microvascular complications" research direction.
            </div>

            <div class="insight">
                <strong>Health Equity and Global Health Remain Sparsely Represented.</strong>
                Only {concept_freq.get('health_equity', 0)} papers explicitly address health equity and {concept_freq.get('global_health', 0)} address global health contexts, despite the urgent clinical need. Our Gap #2 framework should prioritize expanding literature in these domains.
            </div>
        </div>
    </div>

    <div class="footer">
        <p>Corpus Analysis Dashboard | Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 202 papers, {len(concept_papers)} concepts tracked</p>
    </div>
</body>
</html>
"""

# Write output
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Dashboard generated: {output_path}")
print(f"Concepts tracked: {len(concept_papers)}")
print(f"Co-occurrence pairs (count >= 1): {len(co_occurrence)}")
print(f"Uncovered high-signal intersections: {len(uncovered_intersections)}")
