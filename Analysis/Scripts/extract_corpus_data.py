#!/usr/bin/env python3
"""
Corpus Data Extraction Pipeline
Extracts structured quantitative data from 91 full-text papers:
- C-peptide measurements (beta cell function)
- Graft/patient survival rates (islet transplant outcomes)
- HbA1c changes (glycemic efficacy)
- Drug dose-response data (repurposing screen validation)
- Cost/QALY data (health economics)
- Hazard ratios and odds ratios (risk quantification)
- Remission rates (treatment efficacy)

Outputs: extracted_corpus_data.json for use by dashboard build scripts.
"""
import json
import os
import re
from collections import defaultdict
from pathlib import Path

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
results_dir = os.path.join(base_dir, 'Analysis', 'Results')
library_dir = os.path.join(results_dir, 'paper_library')

# Load index
with open(os.path.join(library_dir, 'index.json'), encoding='utf-8') as f:
    index = json.load(f)
papers_meta = index['papers']

# ============================================================================
# EXTRACTION PATTERNS
# ============================================================================

EXTRACTORS = {
    'c_peptide': {
        'patterns': [
            r'[Cc]-peptide\s+(?:level|concentration|was|of|=)\s*(\d+\.?\d*)\s*(pmol/[Ll]|ng/m[Ll]|nmol/[Ll])',
            r'[Cc]-peptide\s+(\d+\.?\d*)\s*±\s*(\d+\.?\d*)\s*(pmol/[Ll]|ng/m[Ll])',
            r'fasting\s+[Cc]-peptide\s*[=:]\s*(\d+\.?\d*)',
            r'[Cc]-peptide\s+(?:increased|decreased|declined|preserved).*?(\d+\.?\d*)\s*%',
            r'stimulated\s+[Cc]-peptide.*?(\d+\.?\d*)\s*(pmol/[Ll]|ng/m[Ll])',
        ],
        'context_window': 200,
        'gap_relevance': [1, 3, 5, 8, 10],
    },
    'hba1c_change': {
        'patterns': [
            r'HbA1c\s*(?:reduction|decrease|change|lowering)\s*(?:of|was|=)\s*[-−]?\s*(\d+\.?\d*)\s*%',
            r'HbA1c\s*[-−]\s*(\d+\.?\d*)\s*%',
            r'A1c\s+(?:from|was)\s+(\d+\.?\d*)\s*%?\s+to\s+(\d+\.?\d*)\s*%',
            r'glycated\s+hemoglobin.*?(\d+\.?\d*)\s*±\s*(\d+\.?\d*)',
            r'HbA1c\s*(\d+\.?\d*)\s*±\s*(\d+\.?\d*)\s*%',
        ],
        'context_window': 200,
        'gap_relevance': [7, 8, 9, 12],
    },
    'survival_graft': {
        'patterns': [
            r'(?:graft|islet|transplant)\s+survival\s*(?:rate|was|of|=)\s*(\d+\.?\d*)\s*%',
            r'insulin\s+independence\s*(?:rate|was|at|of).*?(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*%\s*(?:of\s+)?(?:patients?|recipients?)\s+(?:achieved|maintained|remained)\s+insulin\s+independence',
            r'(?:at|after)\s+(\d+)\s*(?:year|yr|month|mo).*?(\d+\.?\d*)\s*%\s*(?:graft|insulin|survival)',
            r'(\d+)/(\d+)\s*(?:patients?|recipients?)\s+(?:achieved|were)\s+insulin[- ]independent',
        ],
        'context_window': 300,
        'gap_relevance': [2, 3, 4, 11],
    },
    'dose_response': {
        'patterns': [
            r'(\w+(?:\s+\w+)?)\s+(\d+\.?\d*)\s*(mg|µg|mcg|IU|units?)\s*(?:/day|daily|once daily|twice daily|BID|QD)',
            r'(?:dose|dosage)\s+(?:of|was)\s+(\d+\.?\d*)\s*(mg|µg|mcg)',
            r'(\d+\.?\d*)\s*(mg|µg)\s+(?:of\s+)?(\w+)',
        ],
        'context_window': 150,
        'gap_relevance': [4, 7, 8, 12],
    },
    'hazard_ratio': {
        'patterns': [
            r'(?:HR|hazard\s+ratio)\s*[=:]\s*(\d+\.?\d*)\s*(?:\(|,)\s*95%\s*CI\s*[=:,]?\s*(\d+\.?\d*)\s*[-–to]+\s*(\d+\.?\d*)',
            r'(?:HR|hazard\s+ratio)\s*[=:]\s*(\d+\.?\d*)',
        ],
        'context_window': 200,
        'gap_relevance': [2, 6, 11],
    },
    'odds_ratio': {
        'patterns': [
            r'(?:OR|odds\s+ratio)\s*[=:]\s*(\d+\.?\d*)\s*(?:\(|,)\s*95%\s*CI\s*[=:,]?\s*(\d+\.?\d*)\s*[-–to]+\s*(\d+\.?\d*)',
            r'(?:OR|odds\s+ratio)\s*[=:]\s*(\d+\.?\d*)',
        ],
        'context_window': 200,
        'gap_relevance': [2, 6, 10, 11],
    },
    'remission': {
        'patterns': [
            r'(?:remission|complete\s+response)\s*(?:rate|was|of|in).*?(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*%\s*(?:remission|complete\s+response)',
            r'(\d+)/(\d+).*?(?:remission|complete\s+response)',
        ],
        'context_window': 200,
        'gap_relevance': [7, 8, 9],
    },
    'cost_qaly': {
        'patterns': [
            r'\$\s*(\d[\d,]*\.?\d*)\s*(?:per|/)\s*QALY',
            r'ICER\s*(?:of|was|=)\s*\$?\s*(\d[\d,]*\.?\d*)',
            r'cost[- ]effective(?:ness)?\s*(?:ratio|threshold).*?\$\s*(\d[\d,]*\.?\d*)',
            r'\$\s*(\d[\d,]*\.?\d*)\s*(?:per\s+patient|annually|per\s+year)',
        ],
        'context_window': 250,
        'gap_relevance': [6, 10, 11, 15],
    },
    'inflammatory_markers': {
        'patterns': [
            r'(?:CRP|C-reactive\s+protein)\s*(?:level|was|=|of)\s*(\d+\.?\d*)\s*(mg/[Ll]|mg/dL)',
            r'(?:TNF-?α?|TNF[- ]alpha|tumor\s+necrosis)\s*(?:level|was|=).*?(\d+\.?\d*)',
            r'(?:IL-1β?|IL-6|IL-10|interleukin)\s*(?:level|was|=|concentration).*?(\d+\.?\d*)',
            r'(?:NF-κB|NF-kB|NLRP3)\s+(?:activation|expression|level).*?(\d+\.?\d*)',
        ],
        'context_window': 200,
        'gap_relevance': [4, 5, 8, 12],
    },
    'autoantibody': {
        'patterns': [
            r'(?:GAD65?|GADA?|GAD\s+antibod)\s*(?:positive|titer|level|>|=)\s*(\d+\.?\d*)',
            r'(?:IA-2A?|IA-2\s+antibod)\s*(?:positive|titer|level).*?(\d+\.?\d*)',
            r'(?:ZnT8A?|ZnT8\s+antibod)\s*(?:positive|titer|level).*?(\d+\.?\d*)',
            r'autoantibod\w*\s+(?:positive|prevalence).*?(\d+\.?\d*)\s*%',
        ],
        'context_window': 200,
        'gap_relevance': [1, 8, 10],
    },
}


def get_full_text(paper_data):
    """Extract full text from sections."""
    sections = paper_data.get('sections', [])
    parts = []
    for sec in sections:
        if isinstance(sec, dict):
            text = sec.get('text', sec.get('content', ''))
            if text:
                parts.append(text)
        elif isinstance(sec, str):
            parts.append(sec)
    return ' '.join(parts)


def extract_context(text, match_start, match_end, window=200):
    """Get surrounding context for a match."""
    start = max(0, match_start - window)
    end = min(len(text), match_end + window)
    context = text[start:end].strip()
    # Clean up
    context = re.sub(r'\s+', ' ', context)
    return context


def run_extraction():
    """Run all extractors across the corpus."""
    all_extractions = defaultdict(list)
    paper_stats = {}

    ft_dir = os.path.join(library_dir, 'fulltext')
    ft_files = sorted(Path(ft_dir).glob('*.json'))

    print(f"Processing {len(ft_files)} full-text papers...")

    for fp in ft_files:
        with open(fp, encoding='utf-8') as f:
            paper_data = json.load(f)

        pmcid = paper_data.get('pmcid', fp.stem)
        pmid = str(paper_data.get('pmid', ''))
        full_text = get_full_text(paper_data)

        if not full_text or len(full_text) < 100:
            continue

        meta = papers_meta.get(pmid, {})
        title = meta.get('title', 'Unknown')
        year = meta.get('year', 'Unknown')
        journal = meta.get('journal', 'Unknown')

        paper_extractions = {}

        for data_type, config in EXTRACTORS.items():
            matches_found = []
            for pattern in config['patterns']:
                for match in re.finditer(pattern, full_text, re.IGNORECASE):
                    context = extract_context(
                        full_text, match.start(), match.end(),
                        config['context_window']
                    )
                    matches_found.append({
                        'matched_text': match.group(0)[:200],
                        'groups': [g for g in match.groups() if g],
                        'context': context[:500],
                        'position': match.start(),
                    })

            if matches_found:
                # Deduplicate by position (within 50 chars)
                deduped = []
                seen_positions = set()
                for m in sorted(matches_found, key=lambda x: x['position']):
                    pos_bucket = m['position'] // 50
                    if pos_bucket not in seen_positions:
                        deduped.append(m)
                        seen_positions.add(pos_bucket)

                paper_extractions[data_type] = deduped
                for m in deduped:
                    all_extractions[data_type].append({
                        'pmid': pmid,
                        'pmcid': pmcid,
                        'title': title,
                        'year': year,
                        'journal': journal,
                        'matched_text': m['matched_text'],
                        'values': m['groups'],
                        'context': m['context'],
                        'gap_relevance': config['gap_relevance'],
                    })

        if paper_extractions:
            paper_stats[pmid] = {
                'title': title,
                'year': year,
                'journal': journal,
                'pmcid': pmcid,
                'extraction_types': list(paper_extractions.keys()),
                'total_extractions': sum(len(v) for v in paper_extractions.values()),
            }

    return dict(all_extractions), paper_stats


def build_cross_gap_evidence(all_extractions):
    """Map extracted data to research gaps."""
    gap_evidence = defaultdict(lambda: defaultdict(list))

    for data_type, extractions in all_extractions.items():
        gap_relevance = EXTRACTORS[data_type]['gap_relevance']
        for ext in extractions:
            for gap_num in gap_relevance:
                gap_evidence[gap_num][data_type].append({
                    'pmid': ext['pmid'],
                    'title': ext['title'],
                    'year': ext['year'],
                    'value': ext['matched_text'][:100],
                    'context': ext['context'][:300],
                })

    return {k: dict(v) for k, v in gap_evidence.items()}


if __name__ == '__main__':
    print("=" * 60)
    print("  CORPUS DATA EXTRACTION PIPELINE")
    print("=" * 60)

    all_extractions, paper_stats = run_extraction()

    # Build cross-gap evidence map
    gap_evidence = build_cross_gap_evidence(all_extractions)

    # Summary
    print(f"\n{'=' * 60}")
    print(f"  EXTRACTION SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Papers yielding data: {len(paper_stats)}")
    print()

    total_extractions = 0
    for data_type, extractions in sorted(all_extractions.items(), key=lambda x: -len(x[1])):
        count = len(extractions)
        total_extractions += count
        papers_count = len(set(e['pmid'] for e in extractions))
        print(f"  {data_type:<25} {count:4d} extractions from {papers_count:2d} papers")

    print(f"\n  TOTAL: {total_extractions} data points extracted")

    # Gap evidence summary
    print(f"\n  EVIDENCE BY GAP:")
    gap_names = {
        1: "Gene Therapy LADA", 2: "Health Equity Beta Cell", 3: "Islet Transplant IR",
        4: "Drug Repurposing Islet", 5: "Treg Neuropathy", 6: "CAR-T Access",
        7: "GKA Repurposing", 8: "Immunomod LADA", 9: "GKA LADA",
        10: "LADA Prevalence", 11: "Islet Equity", 12: "Generic Drug Catalog",
        13: "Nutrition Beta", 14: "Nutrition LADA", 15: "GKA Pricing",
    }
    for gap_num in sorted(gap_evidence.keys()):
        types = gap_evidence[gap_num]
        total = sum(len(v) for v in types.values())
        type_list = ', '.join(f"{k}({len(v)})" for k, v in types.items())
        name = gap_names.get(gap_num, f"Gap {gap_num}")
        print(f"    Gap {gap_num:2d} ({name}): {total} data points [{type_list}]")

    # Save output
    output = {
        'metadata': {
            'papers_processed': len(paper_stats),
            'total_extractions': total_extractions,
            'extraction_types': {k: len(v) for k, v in all_extractions.items()},
        },
        'extractions': all_extractions,
        'paper_stats': paper_stats,
        'gap_evidence_map': gap_evidence,
    }

    output_path = os.path.join(results_dir, 'extracted_corpus_data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n  Output: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    print(f"\n  Done.")
