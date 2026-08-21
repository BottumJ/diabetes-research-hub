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

# Load agent state to identify FLAGGED off-topic papers that must be excluded
# from the published evidence pipeline (e.g., CRC, smoking-cessation, melanoma
# papers that survived the original PubMed pull but are not diabetes-relevant).
FLAGGED_PMIDS = set()
_state_path = os.path.join(results_dir, 'agent_state.json')
if os.path.exists(_state_path):
    try:
        with open(_state_path, encoding='utf-8') as _f:
            _state = json.load(_f)
        FLAGGED_PMIDS = {
            str(pmid) for pmid, p in _state.get('papers', {}).items()
            if p.get('status') == 'FLAGGED'
        }
    except Exception as _e:
        print(f"  WARNING: could not load agent_state.json FLAGGED list: {_e}")

# Section types in PubMed Open-Access XML that should NOT be scanned for
# quantitative claims about the corpus drugs/conditions:
#   REF       - bibliography/references (cites unrelated papers)
#   AUTH_CONT - author contribution statements
#   COMP_INT  - competing interest declarations
#   ACK_FUND  - acknowledgements / funding
#   FIG       - figure captions (numeric values usually not extractable claims)
#   TABLE     - table captions AND tab-delimited table bodies
#   SUPPL     - supplementary material headers
#   ABBR      - abbreviation glossaries ("TNF= Tumor Necrosis Factor; m-TOR=...")
#
# 2026-08-21: FIG, TABLE and ABBR were DOCUMENTED as skip-worthy in this comment
# block since the file was written, but were never added to the set below. That
# implementation-vs-intent gap is the single root cause of BOTH defects logged
# on 2026-08-18:
#   (a) "extractor double-counts bilingual papers" - PMID 39412512 (J Bras
#       Nefrol) carries its results table twice, English at section 60 and
#       Portuguese at section 247, both typed TABLE. That is where "10 mg or"
#       and "10 mg ou" came from. The paper's Portuguese *prose* was already
#       excluded because this journal tags the whole translation as REF; only
#       the duplicated TABLE/FIG leaked through.
#   (b) "extractor scrapes table fragments as data points" - a tab-delimited
#       table body has no sentence boundaries, so a sentence-shaped regex runs
#       across cell borders and returns fragments like
#       "NLRP3 activation in diabetic mice\tDapagliflozinMixed in diet (1".
# Adding the three types closes both. Rejections are still logged individually
# (see REJECT_REASONS) so the decision stays auditable rather than silent.
SKIP_SECTION_TYPES = {
    'REF', 'AUTH_CONT', 'COMP_INT', 'ACK_FUND', 'SUPPL',
    'FIG', 'TABLE', 'ABBR',
}

# ---------------------------------------------------------------------------
# EXTRACTION REJECTION GATE (added 2026-08-21)
# ---------------------------------------------------------------------------
# Section skipping removes bad SOURCES. This gate removes bad MATCHES that
# survive in legitimate prose. Every rejection is recorded with a reason.
#
# Defect found 2026-08-21 while auditing item (b) above: 52 of the 92
# inflammatory_markers extractions (57%) were not measurements at all. The
# patterns end in `.*?(\d+\.?\d*)` - an unbounded lazy wildcard with no unit
# requirement - so the capture group takes the first digit ANYWHERE downstream.
# In immunology prose the nearest digit is almost always part of a molecule
# name or a year:
#     "NLRP3 activation ... Canagliflozin Ameliorates NLRP3"   -> value "3"
#     "NLRP3 expression, Caspase-1"                            -> value "1"
#     "IL-1beta levels and mROS. In 2014"                      -> value "2014"
# A "value" of 3 here is the 3 in NLRP3. These were being counted as
# inflammatory-marker evidence on the published dashboard.

# Molecule/receptor/gene stems whose trailing digit is part of the NAME.
_NAME_STEMS = (
    r'IL|NLRP|NLRC|NLR|NF|TNF|caspase|GSDMD|ASC|TXNIP|CCR|CXCL|CCL|CD|TLR|'
    r'SGLT|GLUT|NOD|P2X|Nrf|AIM|IKK|HOIL|TRAF|IkB|I[kK]appaB|MyD|STAT|JAK|'
    r'SMAD|TGF|IFN|MCP|VEGF|PD-L|PD|GLP|DPP|ACE|AT|S1P|mTORC|AMPK|SIRT|'
    r'HIF|BCL|TREM|LRR|PYD|CARD|ATP|COX|MMP|TIMP|GAD|IA|ZnT|HbA'
)


def rejection_reason(matched_text, values):
    """Return a rejection reason string, or None if the match is acceptable.

    Order matters: the cheapest, most certain checks run first.
    """
    if not values:
        return None
    value = str(values[-1])

    # 1. Tab characters mean the regex crossed table-cell boundaries. Requested
    #    explicitly by the 2026-08-18 work-queue item. Kept even though section
    #    skipping now removes most sources, because some journals inline
    #    tab-delimited blocks inside RESULTS.
    if '\t' in matched_text:
        return 'TAB_FRAGMENT'

    # 2. A bare 4-digit 1900-2099 capture is a publication/study year.
    if re.fullmatch(r'(?:19|20)\d\d', value):
        return 'YEAR_AS_VALUE'

    # 3. The captured digit is the trailing digit of a molecule name.
    #    Anchored to the END of the match because that is where the capture
    #    group sits in every affected pattern.
    if re.search(
        r'(?:' + _NAME_STEMS + r')\s*[-‐-―αβ\s]?' + re.escape(value) + r'\s*$',
        matched_text, re.IGNORECASE,
    ):
        return 'MOLECULE_NAME_DIGIT'

    # 4. Value ends the match while an opening parenthesis is still unclosed:
    #    "...Mixed in diet (1" - a truncated dose string, not a measurement.
    if matched_text.count('(') > matched_text.count(')') and matched_text.rstrip().endswith(value):
        return 'UNCLOSED_PAREN_FRAGMENT'

    return None


def numeric_fingerprint(text):
    """Ordered tuple of numeric tokens in a section.

    Used to detect translated duplicates: a Portuguese rendering of an English
    section restates every number in the same order, so the fingerprints match
    even though almost no words do. This is defence-in-depth behind the
    FIG/TABLE skip - other bilingual journals tag the translation as CONCL or
    METHODS rather than REF, and those types are legitimately scanned.
    """
    return tuple(re.findall(r'\d+(?:\.\d+)?', text))

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
    # ------------------------------------------------------------------
    # inflammatory_markers - REWRITTEN 2026-08-21
    #
    # The previous patterns ended in `.*?(\d+\.?\d*)`: an UNBOUNDED lazy
    # wildcard, no unit requirement, no sentence boundary. The capture group
    # therefore took the first digit anywhere downstream of the marker name.
    # In immunology prose that digit is essentially never a measurement. Audit
    # of all 92 extractions the old patterns produced:
    #     "NLRP3 activation ... Canagliflozin Ameliorates NLRP3"  -> "3"
    #     "NLRP3 expression, Caspase-1"                           -> "1"
    #     "IL-1beta levels and mROS. In 2014"                     -> "2014"
    #     "NLRP3 activation in diabetic models. 7.2"              -> "7.2"  (section number)
    #     "IL-10 levels ... In a cross-sectional sample of 500"   -> "500"  (sample size)
    # A "value" of 3 is the 3 in NLRP3. None of these are inflammatory-marker
    # levels, and all of them were being served on the published dashboard as
    # extracted corpus evidence.
    #
    # The rewrite enforces three things the old patterns did not:
    #   1. the gap between marker name and number may not cross a sentence
    #      boundary or newline  -> [^.\n]{0,60}?
    #   2. the number must be followed by a CONCENTRATION UNIT, a percent sign
    #      attached to an explicit change verb, or a fold-change token
    #   3. marker names are matched as whole alternatives, so the trailing
    #      digit of the name cannot itself be the capture
    # ------------------------------------------------------------------
    'inflammatory_markers': {
        'patterns': [
            # (1) Absolute level with a concentration unit.
            r'(?:CRP|C-reactive\s+protein|TNF-?[αa]|TNF[- ]alpha|tumor\s+necrosis\s+factor|'
            r'IL-?1\s?[βb]|IL-?6|IL-?10|IL-?18|interleukin[- ]?\d*|NLRP3|NF-?[κk]B)'
            r'[^.\n]{0,60}?(\d+\.?\d*)\s*(pg/m[Ll]|ng/m[Ll]|mg/[Ll]|mg/dL|µg/m[Ll]|ug/m[Ll]|pmol/[Ll]|nmol/[Ll])',
            # (2) Relative change, tied to an explicit direction verb.
            r'(?:CRP|C-reactive\s+protein|TNF-?[αa]|TNF[- ]alpha|IL-?1\s?[βb]|IL-?6|IL-?10|IL-?18|'
            r'NLRP3|NF-?[κk]B)'
            r'[^.\n]{0,60}?(?:increased|decreased|reduced|reduction|elevated|lowered|declined|'
            r'attenuated|suppressed|inhibited|rose|fell)'
            r'[^.\n]{0,40}?(\d+\.?\d*)\s*%',
            # (3) Fold change.
            r'(?:CRP|TNF-?[αa]|IL-?1\s?[βb]|IL-?6|IL-?10|IL-?18|NLRP3|NF-?[κk]B)'
            r'[^.\n]{0,60}?(\d+\.?\d*)[-\s]?fold',
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
    """Extract full text from sections.

    Skips sections that are bibliography/admin (REF, AUTH_CONT, COMP_INT,
    ACK_FUND, SUPPL) so that drug/condition co-occurrences in cited paper
    titles do not generate spurious extractions (root cause of PMID 19940299
    rituximab->nephropathy false positive and other reference-section
    contamination bugs).
    """
    sections = paper_data.get('sections', [])
    parts = []
    # Heuristic fallback: if the paper has unstructured strings, also stop
    # scanning once we hit a 'References' / 'Bibliography' header.
    stop_headers = re.compile(r'^\s*(references|bibliography|works cited)\s*$', re.IGNORECASE)
    # Translated-duplicate suppression (2026-08-21). Only sections carrying at
    # least MIN_FP_NUMBERS numeric tokens are fingerprinted; short sections
    # share fingerprints by coincidence far too often to be safe.
    MIN_FP_NUMBERS = 4
    seen_fingerprints = set()
    dup_sections = 0
    for sec in sections:
        if isinstance(sec, dict):
            sec_type = (sec.get('section_type') or '').upper()
            if sec_type in SKIP_SECTION_TYPES:
                continue
            text = sec.get('text', sec.get('content', ''))
            if text:
                fp = numeric_fingerprint(text)
                if len(fp) >= MIN_FP_NUMBERS:
                    if fp in seen_fingerprints:
                        dup_sections += 1
                        continue
                    seen_fingerprints.add(fp)
                parts.append(text)
        elif isinstance(sec, str):
            if stop_headers.match(sec or ''):
                break
            parts.append(sec)
    return ' '.join(parts), dup_sections


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
    dedupe_log = []
    rejected_log = []
    dup_section_log = []

    ft_dir = os.path.join(library_dir, 'fulltext')
    ft_files = sorted(Path(ft_dir).glob('*.json'))

    print(f"Processing {len(ft_files)} full-text papers...")
    print(f"  Excluding {len(FLAGGED_PMIDS)} FLAGGED off-topic PMIDs from extraction.")

    skipped_flagged = 0
    for fp in ft_files:
        with open(fp, encoding='utf-8') as f:
            paper_data = json.load(f)

        pmcid = paper_data.get('pmcid', fp.stem)
        pmid = str(paper_data.get('pmid', ''))

        # Hard-exclude FLAGGED off-topic papers (e.g., CRC, smoking-cessation,
        # melanoma) — they generate spurious drug/condition co-occurrences in
        # the published evidence pipeline. Vetting decisions live in
        # agent_state.json so this stays a single source of truth.
        if pmid and pmid in FLAGGED_PMIDS:
            skipped_flagged += 1
            continue

        full_text, dup_sections = get_full_text(paper_data)
        if dup_sections:
            dup_section_log.append({'pmid': pmid, 'duplicate_sections': dup_sections})

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
                    matched_text = match.group(0)[:200]
                    groups = [g for g in match.groups() if g]

                    # Rejection gate (2026-08-21): drop matches that are
                    # provably not measurements. Logged, never silent.
                    reason = rejection_reason(matched_text, groups)
                    if reason:
                        rejected_log.append({
                            'pmid': pmid,
                            'data_type': data_type,
                            'reason': reason,
                            'matched_text': matched_text[:160],
                            'value': str(groups[-1]) if groups else '',
                        })
                        continue

                    context = extract_context(
                        full_text, match.start(), match.end(),
                        config['context_window']
                    )
                    matches_found.append({
                        'matched_text': matched_text,
                        'groups': groups,
                        'context': context[:500],
                        'position': match.start(),
                    })

            if matches_found:
                # Pass 1: deduplicate by position (within 50 chars)
                deduped = []
                seen_positions = set()
                for m in sorted(matches_found, key=lambda x: x['position']):
                    pos_bucket = m['position'] // 50
                    if pos_bucket not in seen_positions:
                        deduped.append(m)
                        seen_positions.add(pos_bucket)

                # Pass 2: deduplicate by NORMALIZED MATCHED TEXT within this
                # (paper, data_type).
                #
                # Added 2026-08-19 after audit found 113/490 corpus data points
                # (23.1%) were the same fact restated in different parts of the
                # same paper. Position bucketing alone cannot catch this: e.g.
                # "360 mg verapamil" occurs 18x in PMID 39613428 at 18 distinct
                # positions and was counted as 18 independent data points. That
                # is one dose, one fact. Counting restatements as evidence
                # inflates data_point_count and makes a single paper look like a
                # body of literature.
                #
                # The first occurrence is kept (with its context); repeat
                # occurrences are recorded as `occurrences` so nothing is lost
                # and the collapse remains auditable.
                text_deduped = []
                by_text = {}
                for m in deduped:
                    norm_text = re.sub(r'\s+', ' ', m['matched_text']).strip().lower()
                    if norm_text in by_text:
                        first = by_text[norm_text]
                        first['occurrences'] += 1
                        first['occurrence_positions'].append(m['position'])
                        continue
                    m['occurrences'] = 1
                    m['occurrence_positions'] = [m['position']]
                    by_text[norm_text] = m
                    text_deduped.append(m)

                dupes_collapsed = len(deduped) - len(text_deduped)
                if dupes_collapsed:
                    dedupe_log.append({
                        'pmid': pmid,
                        'data_type': data_type,
                        'raw': len(deduped),
                        'unique': len(text_deduped),
                        'collapsed': dupes_collapsed,
                    })

                paper_extractions[data_type] = text_deduped
                for m in text_deduped:
                    all_extractions[data_type].append({
                        'pmid': pmid,
                        'pmcid': pmcid,
                        'title': title,
                        'year': year,
                        'journal': journal,
                        'matched_text': m['matched_text'],
                        'values': m['groups'],
                        'context': m['context'],
                        'occurrences': m['occurrences'],
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

    if skipped_flagged:
        print(f"  Skipped {skipped_flagged} FLAGGED off-topic full-text papers.")
    return dict(all_extractions), paper_stats, dedupe_log, rejected_log, dup_section_log


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

    all_extractions, paper_stats, dedupe_log, rejected_log, dup_section_log = run_extraction()

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
    collapsed_total = sum(d['collapsed'] for d in dedupe_log)
    print(f"\n  TEXT DEDUPE (added 2026-08-19):")
    print(f"    repeat restatements collapsed: {collapsed_total}")
    print(f"    papers affected              : {len({d['pmid'] for d in dedupe_log})}")
    for d in sorted(dedupe_log, key=lambda x: -x['collapsed'])[:8]:
        print(f"      PMID {d['pmid']} {d['data_type']}: {d['raw']} -> {d['unique']}")

    # Rejection-gate summary
    reason_counts = defaultdict(int)
    for r in rejected_log:
        reason_counts[r['reason']] += 1
    print(f"\n  REJECTION GATE (added 2026-08-21):")
    print(f"    matches rejected as non-measurements: {len(rejected_log)}")
    for reason, n in sorted(reason_counts.items(), key=lambda x: -x[1]):
        print(f"      {reason:<26} {n}")
    dup_total = sum(d['duplicate_sections'] for d in dup_section_log)
    print(f"    translated/duplicate sections dropped: {dup_total} "
          f"across {len(dup_section_log)} papers")

    output = {
        'metadata': {
            'papers_processed': len(paper_stats),
            'total_extractions': total_extractions,
            'extraction_types': {k: len(v) for k, v in all_extractions.items()},
            'rejection_gate': {
                'enabled': True,
                'added': '2026-08-21',
                'rule': 'reject matches that are provably not measurements: tab-crossed '
                        'table fragments, 4-digit years, digits belonging to molecule '
                        'names (the 3 in NLRP3), and values ending inside an unclosed '
                        'parenthesis. Section types FIG/TABLE/ABBR also added to '
                        'SKIP_SECTION_TYPES, matching the intent documented in the '
                        'source comment since the file was written.',
                'rejected_total': len(rejected_log),
                'rejected_by_reason': dict(reason_counts),
                'duplicate_sections_dropped': dup_total,
                'duplicate_section_papers': len(dup_section_log),
            },
            'text_dedupe': {
                'enabled': True,
                'added': '2026-08-19',
                'rule': 'collapse identical normalized matched_text within (pmid, data_type); '
                        'repeat count preserved in the "occurrences" field',
                'restatements_collapsed': collapsed_total,
                'papers_affected': len({d['pmid'] for d in dedupe_log}),
            },
        },
        'dedupe_log': dedupe_log,
        'rejected_log': rejected_log,
        'duplicate_section_log': dup_section_log,
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
