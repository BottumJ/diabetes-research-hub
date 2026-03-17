#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Citation Validator & Cross-Referencer
======================================
Reads the ingested paper library (abstracts + full text) and compares each
paper's actual content against the claims made in our dashboard build scripts
where that paper is cited.

This is the "validate sources and tie them together" step.

Pipeline stages:
  1. Load paper library index + abstract/fulltext data
  2. For each PMID, extract the claim context from our build scripts
     (what we SAY this paper shows)
  3. Compare claim context against actual paper abstract/content
  4. Score relevance: CONFIRMED / PLAUSIBLE / WEAK / MISMATCH
  5. Build cross-paper linkage map (papers that cite each other,
     shared MeSH terms, complementary evidence chains)
  6. Generate validation report

Scoring rubric:
  CONFIRMED  - Multiple key terms from our claim appear in the abstract
  PLAUSIBLE  - Some key terms match, topic area aligns
  WEAK       - Few matches, paper may be tangentially related
  MISMATCH   - Paper content does not support the cited claim

Outputs:
  1. Analysis/Results/citation_validation.json - full validation results
  2. Analysis/Results/evidence_network.json    - cross-paper linkage map
  3. Console summary report

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

# ---------------------------------------------------------------------------
# Diabetes domain vocabulary for relevance scoring
# ---------------------------------------------------------------------------
DIABETES_CORE_TERMS = {
    'diabetes', 'diabetic', 'insulin', 'glucose', 'glycemic', 'glycaemic',
    'hba1c', 'a1c', 'beta cell', 'beta-cell', 'islet', 'pancrea',
    'type 1', 'type 2', 't1d', 't2d', 'lada', 'autoimmune',
    'hyperglycemia', 'hypoglycemia', 'glucokinase', 'gka',
    'metformin', 'sulfonylurea', 'glp-1', 'sglt2', 'dpp-4',
    'transplant', 'immunotherapy', 'car-t', 'treg', 'regulatory t',
    'neuropathy', 'retinopathy', 'nephropathy', 'cardiovascular',
    'obesity', 'bmi', 'weight loss', 'metabolic', 'endocrine',
    'monogenic', 'mody', 'neonatal diabetes', 'precision medicine',
    'clinical trial', 'randomized', 'cohort', 'registry',
    'health equity', 'disparity', 'disparities', 'access',
    'berberine', 'ampk', 'zinc', 'magnesium', 'nutrition',
    'rituximab', 'teplizumab', 'otelixizumab', 'abatacept',
    'tacrolimus', 'sirolimus', 'belatacept', 'etanercept',
    'stem cell', 'gene therapy', 'crispr', 'gene edit',
}


def extract_claim_context(pmid, verification_data):
    """Extract what our dashboards claim about this paper.

    Returns a list of claim strings from the build scripts where this PMID
    is referenced, based on the 'context' field in pmid_verification.json.
    """
    locations = verification_data.get('locations', [])
    claims = []
    for loc in locations:
        context = loc.get('context', '')
        if context:
            # Clean HTML and extract the readable claim text
            clean = re.sub(r'<[^>]+>', ' ', context)
            clean = re.sub(r'\s+', ' ', clean).strip()
            if clean:
                claims.append({
                    'file': loc.get('file', ''),
                    'line': loc.get('line', 0),
                    'text': clean[:300]
                })
    return claims


def load_paper_content(pmid, pmcid=''):
    """Load abstract and (if available) full text for a paper."""
    content = {'abstract': '', 'fulltext_intro': '', 'fulltext_results': ''}

    # Load abstract
    abs_path = os.path.join(abstracts_dir, f'{pmid}.json')
    if os.path.exists(abs_path):
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            content['abstract'] = data.get('abstract', '')
            content['title'] = data.get('title', '')
            content['mesh_terms'] = data.get('mesh_terms', [])
            content['keywords'] = data.get('keywords', [])
        except (json.JSONDecodeError, KeyError):
            pass

    # Load full text sections (intro + results most relevant for validation)
    if pmcid:
        ft_path = os.path.join(fulltext_dir, f'{pmcid}.json')
        if os.path.exists(ft_path):
            try:
                with open(ft_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for section in data.get('sections', []):
                    stype = section.get('section_type', '').lower()
                    text = section.get('text', '')
                    if 'intro' in stype or 'background' in stype:
                        content['fulltext_intro'] += ' ' + text
                    elif 'result' in stype or 'finding' in stype:
                        content['fulltext_results'] += ' ' + text
            except (json.JSONDecodeError, KeyError):
                pass

    return content


def tokenize(text):
    """Simple word tokenization for matching."""
    return set(re.findall(r'[a-z0-9]+(?:-[a-z0-9]+)*', text.lower()))


def score_relevance(claims, paper_content):
    """Score how well the paper content matches our dashboard claims.

    Returns (score_label, confidence, details).
    """
    if not claims:
        return 'NO_CLAIM', 0, 'No claim context found in build scripts'

    abstract = paper_content.get('abstract', '')
    title = paper_content.get('title', '')
    mesh = paper_content.get('mesh_terms', [])
    keywords = paper_content.get('keywords', [])
    intro = paper_content.get('fulltext_intro', '')
    results = paper_content.get('fulltext_results', '')

    if not abstract and not title:
        return 'NO_DATA', 0, 'No abstract or title available for comparison'

    # Build the paper's full text corpus
    corpus = f'{title} {abstract} {" ".join(mesh)} {" ".join(keywords)}'
    if intro:
        corpus += f' {intro}'
    if results:
        corpus += f' {results}'
    corpus_lower = corpus.lower()
    corpus_tokens = tokenize(corpus)

    # Extract key terms from all claims
    all_claim_text = ' '.join(c['text'] for c in claims)
    claim_tokens = tokenize(all_claim_text)

    # Remove very common words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
        'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are',
        'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'can',
        'this', 'that', 'these', 'those', 'it', 'its', 'et', 'al',
        'not', 'no', 'yes', 'all', 'each', 'any', 'some', 'more',
        'other', 'than', 'such', 'very', 'just', 'also', 'only',
        'pmid', 'href', 'https', 'www', 'ncbi', 'nlm', 'nih', 'gov',
        'pubmed', 'html', 'class', 'style', 'span', 'div', 'ref',
        'key', 'pmids', 'python', 'str', 'true', 'false', 'none',
    }
    claim_terms = claim_tokens - stop_words
    if not claim_terms:
        return 'NO_CLAIM', 0, 'Claim context contains only stop words'

    # Count matching terms
    matches = claim_terms & corpus_tokens
    match_ratio = len(matches) / len(claim_terms) if claim_terms else 0

    # Check for diabetes-domain relevance
    diabetes_matches = sum(1 for term in DIABETES_CORE_TERMS if term in corpus_lower)

    # Check for specific key phrases from claims in the corpus
    # (more meaningful than individual word matches)
    phrase_matches = 0
    claim_lower = all_claim_text.lower()
    # Extract 2-3 word phrases from claim
    claim_words = claim_lower.split()
    for i in range(len(claim_words) - 1):
        bigram = f'{claim_words[i]} {claim_words[i+1]}'
        if len(bigram) > 5 and bigram in corpus_lower:
            phrase_matches += 1

    # Scoring decision
    details_parts = []
    details_parts.append(f'{len(matches)}/{len(claim_terms)} claim terms found in paper')
    details_parts.append(f'{diabetes_matches} diabetes domain terms')
    details_parts.append(f'{phrase_matches} phrase matches')

    if match_ratio >= 0.35 and diabetes_matches >= 3:
        return 'CONFIRMED', min(match_ratio + 0.1, 1.0), '; '.join(details_parts)
    elif match_ratio >= 0.20 and diabetes_matches >= 2:
        return 'PLAUSIBLE', match_ratio, '; '.join(details_parts)
    elif match_ratio >= 0.10 or diabetes_matches >= 2:
        return 'WEAK', match_ratio, '; '.join(details_parts)
    elif diabetes_matches >= 1:
        return 'WEAK', match_ratio, '; '.join(details_parts)
    else:
        return 'MISMATCH', match_ratio, '; '.join(details_parts)


def build_evidence_network(index_data):
    """Build a network of papers connected by citations and shared topics."""
    papers = index_data.get('papers', {})
    cross_refs = index_data.get('cross_references', {})

    network = {
        'nodes': [],
        'edges': [],
        'clusters': []
    }

    # Nodes = papers
    for pmid, paper in papers.items():
        network['nodes'].append({
            'pmid': pmid,
            'title': paper.get('title', '')[:100],
            'year': paper.get('year', ''),
            'journal': paper.get('journal', ''),
            'has_abstract': paper.get('has_abstract', False),
            'has_fulltext': paper.get('has_fulltext', False),
        })

    # Edges from intra-hub citations
    citing = cross_refs.get('papers_citing_each_other', {})
    for pmid, cited_list in citing.items():
        for cited in cited_list:
            network['edges'].append({
                'source': pmid,
                'target': cited,
                'type': 'cites'
            })

    # Build topic clusters from shared MeSH (clinical terms only)
    mesh_clusters = cross_refs.get('shared_mesh_terms', {})
    clinical_mesh = {
        term: pmids for term, pmids in mesh_clusters.items()
        if term not in ('Humans', 'Male', 'Female', 'Adult', 'Middle Aged',
                        'Aged', 'Animals', 'Young Adult', 'Adolescent',
                        'Child', 'Infant', 'Aged, 80 and over',
                        'Prospective Studies', 'Retrospective Studies',
                        'Cross-Sectional Studies', 'Treatment Outcome',
                        'Follow-Up Studies', 'Risk Factors', 'Prognosis')
        and len(pmids) >= 3
    }

    for term, pmids in sorted(clinical_mesh.items(), key=lambda x: -len(x[1]))[:30]:
        network['clusters'].append({
            'topic': term,
            'paper_count': len(pmids),
            'pmids': pmids
        })

    return network


def main():
    print('Citation Validator & Cross-Referencer')
    print('=' * 60)

    # Load index
    index_path = os.path.join(library_dir, 'index.json')
    if not os.path.exists(index_path):
        print('  ERROR: Paper library index not found. Run ingest_papers.py first.')
        return 1

    with open(index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    # Load verification data for claim contexts
    verif_path = os.path.join(results_dir, 'pmid_verification.json')
    with open(verif_path, 'r', encoding='utf-8') as f:
        verif_data = json.load(f)

    papers = index_data.get('papers', {})
    print(f'  Validating {len(papers)} papers...')

    # Validate each citation
    validation_results = {}
    score_counts = defaultdict(int)

    for pmid in sorted(papers.keys()):
        paper = papers[pmid]
        verif_info = verif_data.get('results', {}).get(pmid, {})

        # Extract claims from our build scripts
        claims = extract_claim_context(pmid, verif_info)

        # Load paper content
        pmcid = paper.get('pmcid', '')
        content = load_paper_content(pmid, pmcid)

        # Score relevance
        score, confidence, details = score_relevance(claims, content)
        score_counts[score] += 1

        validation_results[pmid] = {
            'pmid': pmid,
            'title': paper.get('title', ''),
            'score': score,
            'confidence': round(confidence, 3),
            'details': details,
            'claim_count': len(claims),
            'claims': claims[:3],  # Keep first 3 for the report
            'has_abstract': paper.get('has_abstract', False),
            'has_fulltext': paper.get('has_fulltext', False),
        }

    # Build evidence network
    print('  Building evidence network...')
    network = build_evidence_network(index_data)

    # Save results
    validation_path = os.path.join(results_dir, 'citation_validation.json')
    with open(validation_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'summary': dict(score_counts),
            'total_papers': len(papers),
            'results': validation_results
        }, f, indent=2, ensure_ascii=False)

    network_path = os.path.join(results_dir, 'evidence_network.json')
    with open(network_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'nodes': len(network['nodes']),
                'citation_edges': len(network['edges']),
                'topic_clusters': len(network['clusters']),
            },
            'network': network
        }, f, indent=2, ensure_ascii=False)

    # Console report
    print()
    print('  Citation Validation Summary')
    print('  ' + '-' * 40)
    for score in ['CONFIRMED', 'PLAUSIBLE', 'WEAK', 'MISMATCH', 'NO_CLAIM', 'NO_DATA']:
        count = score_counts.get(score, 0)
        if count:
            pct = count / len(papers) * 100
            print(f'  {score:12s}: {count:3d} ({pct:5.1f}%)')

    print()
    print('  Evidence Network')
    print('  ' + '-' * 40)
    print(f'  Papers:           {len(network["nodes"])}')
    print(f'  Citation links:   {len(network["edges"])}')
    print(f'  Topic clusters:   {len(network["clusters"])}')

    # Flag any mismatches for attention
    mismatches = [r for r in validation_results.values() if r['score'] == 'MISMATCH']
    if mismatches:
        print()
        print(f'  ATTENTION: {len(mismatches)} potential mismatch(es) need review:')
        for m in mismatches[:5]:
            title_short = m['title'][:60]
            print(f'    PMID:{m["pmid"]} - {title_short}...')
            print(f'      {m["details"]}')

    print(f'\n  Validation report: {validation_path}')
    print(f'  Evidence network:  {network_path}')
    print(f'\n  Citation Validator: complete')

    return 0


if __name__ == '__main__':
    sys.exit(main())
