#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evidence Extractor
==================
Maps every ingested paper to the 15 research gaps, extracts specific findings
from abstracts and full text, and builds a structured evidence database.

This is the core research engine: it reads the paper library and produces
a gap-by-gap evidence map showing exactly what each paper contributes.

Process:
  1. Define keyword signatures for each of the 15 research gaps
  2. For each paper, score relevance to each gap using abstract + MeSH + keywords
  3. For relevant papers, extract key sentences (findings, conclusions, methods)
  4. Build a structured evidence database: gap -> papers -> extracted findings
  5. Generate an enriched evidence dashboard

Outputs:
  - Analysis/Results/gap_evidence.json     - structured evidence per gap
  - Dashboards/Gap_Evidence.html           - interactive evidence browser
  - Console summary of evidence coverage

This script is designed to run as part of the daily build suite.
"""

import os
import re
import json
import sys
from datetime import datetime
from collections import defaultdict

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
results_dir = os.path.join(base_dir, 'Analysis', 'Results')
library_dir = os.path.join(results_dir, 'paper_library')
abstracts_dir = os.path.join(library_dir, 'abstracts')
fulltext_dir = os.path.join(library_dir, 'fulltext')
output_dir = os.path.join(base_dir, 'Dashboards')
os.makedirs(output_dir, exist_ok=True)

# ---------------------------------------------------------------------------
# The 15 Research Gaps with keyword signatures
# ---------------------------------------------------------------------------
GAPS = {
    1: {
        'name': 'Gene Therapy for LADA',
        'tier': 'SILVER',
        'keywords': [
            'lada', 'latent autoimmune diabetes', 'gene therapy', 'gada',
            'gad65', 'gad antibod', 'autoimmune diabetes adult',
            'slowly progressive', 'type 1.5', 'c-peptide decline',
            'hla-dr', 'autoantibod', 'immune preservation',
            'beta cell preservation lada', 'insulin independence lada'
        ],
        'mesh_sig': ['Diabetes Mellitus, Type 1', 'Autoantibodies', 'Genetic Therapy'],
    },
    2: {
        'name': 'Health Equity in Diabetes',
        'tier': 'GOLD',
        'keywords': [
            'health equity', 'health disparit', 'racial disparit', 'ethnic disparit',
            'social determinant', 'access to care', 'socioeconomic',
            'underserved', 'minorit', 'inequit', 'insurance coverage',
            'diabetes technology access', 'cgm access', 'pump access',
            'rural diabetes', 'food desert', 'food insecur',
        ],
        'mesh_sig': ['Healthcare Disparities', 'Health Equity', 'Social Determinants of Health'],
    },
    3: {
        'name': 'Insulin Resistance in Islet Transplant',
        'tier': 'GOLD',
        'keywords': [
            'islet transplant', 'islet graft', 'edmonton protocol',
            'insulin resistance transplant', 'graft function',
            'beta cell replacement', 'immunosuppress', 'tacrolimus',
            'sirolimus', 'belatacept', 'calcineurin',
            'ibmir', 'instant blood mediated', 'islet isolation',
            'stem cell derived islet', 'encapsulat',
        ],
        'mesh_sig': ['Islets of Langerhans Transplantation', 'Insulin Resistance'],
    },
    4: {
        'name': 'Drug Repurposing for Islet Transplant',
        'tier': 'BRONZE',
        'keywords': [
            'drug repurpos', 'islet transplant', 'immunosuppress',
            'anti-inflammatory islet', 'etanercept', 'anakinra',
            'alpha-1 antitrypsin', 'tnf-alpha islet', 'ibmir',
            'islet survival drug', 'anti-rejection',
        ],
        'mesh_sig': ['Drug Repositioning', 'Islets of Langerhans Transplantation'],
    },
    5: {
        'name': 'Treg in Diabetic Neuropathy',
        'tier': 'BRONZE',
        'keywords': [
            'regulatory t cell', 'treg', 'foxp3', 'diabetic neuropathy',
            'neuroinflammation diabetes', 'neuroprotect', 'nerve repair',
            'peripheral neuropathy', 'neuroimmun', 'schwann cell',
            'nerve conduction', 'neuropathic pain diabetes',
        ],
        'mesh_sig': ['T-Lymphocytes, Regulatory', 'Diabetic Neuropathies'],
    },
    6: {
        'name': 'CAR-T Access Barriers',
        'tier': 'GOLD',
        'keywords': [
            'car-t', 'car t cell', 'chimeric antigen receptor',
            'car-treg', 'adoptive cell', 'cell therapy cost',
            'manufacturing cost', 'cell therapy access',
            'autologous cell', 'allogeneic cell therapy',
        ],
        'mesh_sig': ['Receptors, Chimeric Antigen', 'Immunotherapy, Adoptive'],
    },
    7: {
        'name': 'GKA Drug Repurposing',
        'tier': 'SILVER',
        'keywords': [
            'glucokinase activator', 'gka', 'dorzagliatin',
            'glucokinase', 'glucose sensor', 'hepatic glucose',
            'beta cell glucose sensing', 'matschinsky',
        ],
        'mesh_sig': ['Glucokinase'],
    },
    8: {
        'name': 'Immunomodulatory Drugs for LADA',
        'tier': 'SILVER',
        'keywords': [
            'immunomodulat', 'lada', 'latent autoimmune',
            'rituximab', 'teplizumab', 'anti-cd3', 'anti-cd20',
            'gad-alum', 'abatacept', 'immune interven',
            'disease modif', 'preserve beta cell',
        ],
        'mesh_sig': ['Immunologic Factors', 'Diabetes Mellitus, Type 1'],
    },
    9: {
        'name': 'GKA in LADA',
        'tier': 'EXPLORATORY',
        'keywords': [
            'glucokinase lada', 'gka autoimmune', 'glucokinase beta cell',
            'glucose sensing lada', 'dorzagliatin autoimmune',
            'glucokinase activator type 1',
        ],
        'mesh_sig': ['Glucokinase', 'Diabetes Mellitus, Type 1'],
    },
    10: {
        'name': 'LADA Prevalence by Healthcare Setting',
        'tier': 'SILVER',
        'keywords': [
            'lada prevalence', 'lada epidemiolog', 'lada misdiagnos',
            'latent autoimmune prevalence', 'lada primary care',
            'autoimmune diabetes screening', 'gad antibody screening',
            'lada underdiagnos', 'action lada',
        ],
        'mesh_sig': ['Prevalence', 'Latent Autoimmune Diabetes in Adults'],
    },
    11: {
        'name': 'Islet Transplant Registry Equity',
        'tier': 'GOLD',
        'keywords': [
            'islet transplant registry', 'citr', 'transplant equity',
            'transplant access', 'organ allocation', 'transplant disparit',
            'waitlist', 'donor match', 'transplant demographics',
        ],
        'mesh_sig': ['Islets of Langerhans Transplantation', 'Registries'],
    },
    12: {
        'name': 'Generic Drug x Diabetes Mechanism Catalog',
        'tier': 'BRONZE',
        'keywords': [
            'generic drug diabetes', 'off-label diabetes', 'metformin mechanism',
            'repurpos', 'colchicine diabetes', 'hydroxychloroquine diabetes',
            'pentoxifylline diabetes', 'allopurinol diabetes',
            'dapsone diabetes', 'verapamil diabetes', 'doxycycline diabetes',
            'nlrp3 inflammasome', 'ampk activat',
        ],
        'mesh_sig': ['Drugs, Generic', 'Diabetes Mellitus'],
    },
    13: {
        'name': 'Personalized Nutrition for Beta Cells',
        'tier': 'BRONZE',
        'keywords': [
            'nutrition beta cell', 'diet beta cell', 'nutrient sensing',
            'zinc beta cell', 'magnesium diabetes', 'berberine',
            'omega-3 diabetes', 'vitamin d diabetes', 'chromium diabetes',
            'intermittent fasting beta', 'glycemic response personali',
            'microbiome diet diabetes', 'fiber diabetes',
        ],
        'mesh_sig': ['Diet', 'Insulin-Secreting Cells', 'Nutritional Sciences'],
    },
    14: {
        'name': 'Personalized Nutrition for LADA',
        'tier': 'BRONZE',
        'keywords': [
            'nutrition lada', 'diet autoimmune diabetes', 'mediterranean diet diabetes',
            'predimed diabetes', 'anti-inflammatory diet', 'gut microbiome autoimmun',
            'nutrition immune modulation', 'food autoimmun',
        ],
        'mesh_sig': ['Diet, Mediterranean', 'Autoimmunity', 'Diabetes Mellitus, Type 1'],
    },
    15: {
        'name': 'GKA Pricing Trajectory',
        'tier': 'BRONZE',
        'keywords': [
            'gka price', 'gka cost', 'glucokinase cost', 'dorzagliatin price',
            'diabetes drug pricing', 'drug access cost', 'diabetes pharmacoeconom',
            'insulin affordab',
        ],
        'mesh_sig': ['Drug Costs', 'Glucokinase'],
    },
}


# ---------------------------------------------------------------------------
# Sentence extraction
# ---------------------------------------------------------------------------
def split_sentences(text):
    """Split text into sentences, handling common abbreviations."""
    # Protect common abbreviations
    text = re.sub(r'(?<=[A-Z])\.(?=[A-Z])', '@DOT@', text)  # U.S., N.I.H.
    for abbr in ['Dr', 'Mr', 'Ms', 'vs', 'al', 'et', 'Fig', 'Ref', 'No', 'Vol']:
        text = text.replace(abbr + '.', abbr + '@DOT@')
    text = re.sub(r'(?<=\d)\.(?=\d)', '@DOT@', text)  # 3.5, p<0.05

    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    return [s.replace('@DOT@', '.').strip() for s in sentences if len(s.strip()) > 20]


def extract_key_findings(text, gap_keywords):
    """Extract sentences from text that contain gap-relevant terms."""
    if not text:
        return []

    sentences = split_sentences(text)
    findings = []
    text_lower_cache = {}

    # Finding indicators - sentences that report results or conclusions
    finding_signals = [
        'found that', 'showed that', 'demonstrated', 'resulted in',
        'associated with', 'correlated with', 'significantly',
        'reduced', 'increased', 'improved', 'decreased',
        'effective', 'efficacy', 'outcome', 'concluded',
        'suggests that', 'indicates that', 'revealed',
        'compared with', 'versus', 'vs.', 'hazard ratio',
        'odds ratio', 'confidence interval', 'p <', 'p=',
        'relative risk', 'absolute risk', 'number needed',
        'median', 'mean difference', 'effect size',
    ]

    for sent in sentences:
        sent_lower = sent.lower()

        # Check if sentence contains gap keywords
        keyword_hits = sum(1 for kw in gap_keywords if kw in sent_lower)
        if keyword_hits == 0:
            continue

        # Check if it's a finding/result sentence (not just background)
        is_finding = any(sig in sent_lower for sig in finding_signals)

        # Score: keywords * 2 + finding_bonus
        score = keyword_hits * 2 + (3 if is_finding else 0)

        if score >= 2:
            # Clean up the sentence
            clean = re.sub(r'<[^>]+>', '', sent)
            clean = re.sub(r'&#x[0-9a-f]+;', '', clean)
            clean = re.sub(r'\s+', ' ', clean).strip()
            if 20 < len(clean) < 500:
                findings.append({
                    'text': clean,
                    'score': score,
                    'is_finding': is_finding,
                    'keyword_hits': keyword_hits,
                })

    # Sort by score, deduplicate, take top findings
    findings.sort(key=lambda x: -x['score'])
    seen = set()
    unique = []
    for f in findings:
        key = f['text'][:80]
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique[:5]  # Top 5 per paper per gap


# ---------------------------------------------------------------------------
# Gap relevance scoring
# ---------------------------------------------------------------------------
def score_paper_for_gap(paper_data, abstract_data, gap):
    """Score how relevant a paper is to a specific research gap."""
    title = (abstract_data.get('title', '') or paper_data.get('title', '')).lower()
    abstract = (abstract_data.get('abstract', '') or '').lower()
    mesh = [m.lower() for m in abstract_data.get('mesh_terms', [])]
    keywords = [k.lower() for k in abstract_data.get('keywords', [])]
    corpus = f'{title} {abstract} {" ".join(mesh)} {" ".join(keywords)}'

    score = 0

    # Keyword matches in corpus
    for kw in gap['keywords']:
        if kw in corpus:
            # Title match is worth more
            if kw in title:
                score += 3
            elif kw in abstract:
                score += 2
            else:
                score += 1

    # MeSH signature matches
    mesh_set = set(mesh)
    for sig_term in gap.get('mesh_sig', []):
        if sig_term.lower() in mesh_set:
            score += 3

    return score


# ---------------------------------------------------------------------------
# Main extraction pipeline
# ---------------------------------------------------------------------------
def load_papers():
    """Load all paper data from the library."""
    index_path = os.path.join(library_dir, 'index.json')
    if not os.path.exists(index_path):
        return None, {}

    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)

    abstracts = {}
    for fname in os.listdir(abstracts_dir):
        if fname.endswith('.json'):
            pmid = fname.replace('.json', '')
            try:
                with open(os.path.join(abstracts_dir, fname), 'r', encoding='utf-8') as f:
                    abstracts[pmid] = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

    return index, abstracts


def load_fulltext(pmcid):
    """Load full text for a paper."""
    ft_path = os.path.join(fulltext_dir, f'{pmcid}.json')
    if not os.path.exists(ft_path):
        return ''
    try:
        with open(ft_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Combine all sections into one text
        return ' '.join(s.get('text', '') for s in data.get('sections', []))
    except (json.JSONDecodeError, IOError):
        return ''


def extract_all_evidence(index, abstracts):
    """Run the full extraction pipeline across all papers and gaps."""
    papers = index.get('papers', {})
    gap_evidence = {}

    for gap_id, gap in sorted(GAPS.items()):
        gap_results = {
            'gap_id': gap_id,
            'name': gap['name'],
            'tier': gap['tier'],
            'papers': [],
            'total_findings': 0,
        }

        for pmid in sorted(papers.keys()):
            paper = papers[pmid]
            abstract_data = abstracts.get(pmid, {})

            # Score relevance
            relevance = score_paper_for_gap(paper, abstract_data, gap)
            if relevance < 3:  # Minimum threshold
                continue

            # Extract findings from abstract
            abstract_text = abstract_data.get('abstract', '')
            abstract_findings = extract_key_findings(abstract_text, gap['keywords'])

            # Extract findings from full text if available
            fulltext_findings = []
            pmcid = paper.get('pmcid', '')
            if pmcid:
                ft_text = load_fulltext(pmcid)
                if ft_text:
                    fulltext_findings = extract_key_findings(ft_text, gap['keywords'])

            # Combine and deduplicate findings
            all_findings = []
            seen_prefixes = set()
            for f in abstract_findings + fulltext_findings:
                prefix = f['text'][:60]
                if prefix not in seen_prefixes:
                    seen_prefixes.add(prefix)
                    all_findings.append(f)

            all_findings = sorted(all_findings, key=lambda x: -x['score'])[:5]

            if all_findings:
                gap_results['papers'].append({
                    'pmid': pmid,
                    'title': abstract_data.get('title', paper.get('title', '')),
                    'journal': abstract_data.get('journal', paper.get('journal', '')),
                    'year': abstract_data.get('year', paper.get('year', '')),
                    'authors': abstract_data.get('authors', [])[:3],
                    'relevance_score': relevance,
                    'findings': all_findings,
                    'has_fulltext': bool(pmcid and os.path.exists(
                        os.path.join(fulltext_dir, f'{pmcid}.json'))),
                })
                gap_results['total_findings'] += len(all_findings)

        # Sort papers by relevance score
        gap_results['papers'].sort(key=lambda x: -x['relevance_score'])
        gap_evidence[gap_id] = gap_results

    return gap_evidence


# ---------------------------------------------------------------------------
# Dashboard generation
# ---------------------------------------------------------------------------
def build_dashboard(gap_evidence):
    """Generate the interactive gap evidence HTML dashboard."""
    COLORS = {
        'bg': '#fafaf7', 'text': '#333333', 'muted': '#636363',
        'border': '#e0ddd5', 'accent': '#2c5f8a', 'header_bg': '#ffffff',
        'gold': '#8B6914', 'silver': '#5a6a7a', 'bronze': '#8B5E3C',
        'exploratory': '#6a5a8a', 'finding': '#2d6a2e',
    }

    # Build gap cards
    gap_cards = []
    for gap_id in sorted(gap_evidence.keys()):
        gap = gap_evidence[gap_id]
        tier_color = COLORS.get(gap['tier'].lower(), COLORS['muted'])
        paper_count = len(gap['papers'])
        finding_count = gap['total_findings']

        # Build paper evidence rows
        paper_rows = []
        for p in gap['papers'][:10]:
            title = re.sub(r'<[^>]+>', '', p.get('title', ''))
            title = re.sub(r'&#x[0-9a-f]+;', '', title)[:100]
            authors = ', '.join(a if isinstance(a, str) else str(a) for a in p.get('authors', [])[:2])
            year = p.get('year', '')
            journal = p.get('journal', '')
            pmid = p.get('pmid', '')
            ft_badge = ' [Full Text]' if p.get('has_fulltext') else ''

            finding_items = []
            for f in p.get('findings', []):
                ft = re.sub(r'&#x[0-9a-f]+;', '', f['text'])
                badge = '<span style="color:#2d6a2e;font-weight:600;font-size:0.75rem;">FINDING</span> ' if f.get('is_finding') else ''
                finding_items.append(
                    f'<li style="margin-bottom:6px;line-height:1.4;">{badge}{_esc(ft)}</li>'
                )
            findings_html = '\n'.join(finding_items)

            paper_rows.append(f'''
            <div style="margin-bottom:16px;padding:12px;border:1px solid {COLORS['border']};background:{COLORS['header_bg']};">
                <div style="font-weight:600;margin-bottom:4px;">
                    <a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank" style="color:{COLORS['accent']};">{_esc(title)}</a>{ft_badge}
                </div>
                <div style="font-size:0.82rem;color:{COLORS['muted']};margin-bottom:8px;">
                    {_esc(authors)} | {_esc(journal)} {year} | PMID:{pmid} | Relevance: {p.get('relevance_score', 0)}
                </div>
                <ul style="margin:0;padding-left:18px;font-size:0.88rem;">
                    {findings_html}
                </ul>
            </div>''')

        papers_html = '\n'.join(paper_rows) if paper_rows else '<p style="color:#999;">No papers with extractable findings mapped to this gap yet.</p>'

        gap_cards.append(f'''
        <div class="gap-section" id="gap-{gap_id}">
            <h2 style="cursor:pointer;" onclick="toggleGap({gap_id})">
                <span style="color:{tier_color};font-size:0.8rem;font-weight:600;letter-spacing:0.05em;">[{gap['tier']}]</span>
                Gap #{gap_id}: {_esc(gap['name'])}
                <span style="font-size:0.85rem;color:{COLORS['muted']};font-weight:normal;margin-left:12px;">
                    {paper_count} papers | {finding_count} findings
                </span>
            </h2>
            <div class="gap-content" id="gap-content-{gap_id}" style="display:{'block' if gap_id <= 3 else 'none'};">
                {papers_html}
            </div>
        </div>''')

    gap_cards_html = '\n'.join(gap_cards)

    # Summary stats
    total_papers_mapped = sum(len(g['papers']) for g in gap_evidence.values())
    total_findings = sum(g['total_findings'] for g in gap_evidence.values())
    unique_pmids = set()
    for g in gap_evidence.values():
        for p in g['papers']:
            unique_pmids.add(p['pmid'])
    gaps_with_evidence = sum(1 for g in gap_evidence.values() if g['papers'])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gap Evidence Browser - Diabetes Research Hub</title>
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
        h2 {{ font-size: 1.2rem; margin: 0 0 0.8rem 0; color: {COLORS['text']}; border-bottom: 1px solid {COLORS['border']}; padding-bottom: 0.3rem; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px 30px 40px 30px; }}
        .description {{ color: {COLORS['muted']}; font-size: 0.9rem; margin-bottom: 1.5rem; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
            margin-bottom: 1.5rem;
        }}
        .stat-card {{
            background: {COLORS['header_bg']};
            border: 1px solid {COLORS['border']};
            padding: 12px 16px;
        }}
        .stat-value {{ font-family: "SF Mono", Consolas, monospace; font-size: 1.6rem; font-weight: 600; }}
        .stat-label {{ font-size: 0.8rem; color: {COLORS['muted']}; text-transform: uppercase; letter-spacing: 0.05em; }}
        a {{ color: {COLORS['accent']}; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .gap-section {{ margin-bottom: 8px; }}
        .gap-content {{ padding: 12px 0; }}
        .timestamp {{ font-size: 0.75rem; color: {COLORS['muted']}; margin-top: 2rem; }}
    </style>
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
  <a href="Paper_Library.html" style="color:#636363;text-decoration:none;">Paper Library</a>
  <a href="Gap_Evidence.html" style="color:#2c5f8a;text-decoration:none;font-weight:600;">Evidence</a>
</div>
<div class="container">
    <h1>Gap Evidence Browser</h1>
    <p class="description">Extracted findings from ingested papers, mapped to each of the 15 research gaps. Each finding is a specific sentence from the paper's abstract or full text that contains relevant evidence. Click any gap to expand.</p>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{gaps_with_evidence}</div>
            <div class="stat-label">Gaps with Evidence</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(unique_pmids)}</div>
            <div class="stat-label">Unique Papers</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{total_papers_mapped}</div>
            <div class="stat-label">Paper-Gap Mappings</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{total_findings}</div>
            <div class="stat-label">Extracted Findings</div>
        </div>
    </div>

    {gap_cards_html}

    <p class="timestamp">Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} | Evidence extracted from PubMed abstracts and PMC Open Access full text</p>
</div>
<script>
function toggleGap(id) {{
    var el = document.getElementById('gap-content-' + id);
    el.style.display = el.style.display === 'none' ? 'block' : 'none';
}}
</script>
</body>
</html>'''
    return html


def _esc(text):
    """Escape HTML."""
    return (str(text).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print('Evidence Extractor')
    print('=' * 60)

    # Load data
    print('  Loading paper library...')
    index, abstracts = load_papers()
    if not index:
        print('  ERROR: Paper library not found. Run ingest_papers.py first.')
        return 1

    papers = index.get('papers', {})
    print(f'  {len(papers)} papers, {len(abstracts)} abstracts loaded.')

    # Extract evidence
    print('  Extracting evidence across 15 research gaps...')
    gap_evidence = extract_all_evidence(index, abstracts)

    # Save JSON
    json_path = os.path.join(results_dir, 'gap_evidence.json')
    # Convert for JSON serialization
    serializable = {}
    for gid, gdata in gap_evidence.items():
        serializable[str(gid)] = gdata
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'gaps': serializable,
        }, f, indent=2, ensure_ascii=False)

    # Build dashboard
    print('  Building evidence dashboard...')
    html = build_dashboard(gap_evidence)
    html_path = os.path.join(output_dir, 'Gap_Evidence.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Console summary
    print()
    print('  Evidence Summary by Gap')
    print('  ' + '-' * 50)
    total_findings = 0
    for gap_id in sorted(gap_evidence.keys()):
        gap = gap_evidence[gap_id]
        pc = len(gap['papers'])
        fc = gap['total_findings']
        total_findings += fc
        tier = gap['tier']
        print(f'  #{gap_id:2d} [{tier:11s}] {gap["name"][:35]:35s} {pc:3d} papers, {fc:3d} findings')

    unique_pmids = set()
    for g in gap_evidence.values():
        for p in g['papers']:
            unique_pmids.add(p['pmid'])

    print()
    print(f'  Total: {len(unique_pmids)} unique papers, {total_findings} findings')
    print(f'  JSON:  {json_path}')
    print(f'  HTML:  {html_path} ({os.path.getsize(html_path)/1024:.1f} KB)')

    return 0


if __name__ == '__main__':
    sys.exit(main())
