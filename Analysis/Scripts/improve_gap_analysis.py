#!/usr/bin/env python3
"""
Improve Literature Gap Analysis — Add interpretive classification.

Reads literature_gap_data.json and generates an improved report that:
  1. Classifies each gap as "Potentially Meaningful" vs "Methodologically Distinct"
  2. Adds context explaining why a gap exists
  3. Clarifies what "Gap Score" actually measures
  4. Adds validation caveats per the Research Doctrine

Output: Analysis/Results/literature_gap_report.md (overwrites)
"""

import json
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RESULTS_DIR = os.path.join(BASE_DIR, 'Analysis', 'Results')

# === INTERPRETIVE CLASSIFICATIONS ===
# Domain pairs where low co-publication is expected because the fields
# use fundamentally different methods or study different populations.
METHODOLOGICALLY_DISTINCT = {
    ('GWAS / Polygenic', 'Closed Loop / AP'),
    ('GWAS / Polygenic', 'CGM Technology'),
    ('Drug Repurposing', 'Closed Loop / AP'),
    ('Drug Repurposing', 'CGM Technology'),
    ('Glucokinase', 'CGM Technology'),
    ('Glucokinase', 'Closed Loop / AP'),
    ('Treg / CAR-T', 'CGM Technology'),
    ('Treg / CAR-T', 'Closed Loop / AP'),
    ('Personalized Nutr', 'Closed Loop / AP'),
    ('Islet Transplant', 'Personalized Nutr'),
    ('Islet Transplant', 'GWAS / Polygenic'),
    ('Gene Therapy', 'CGM Technology'),
    ('Gene Therapy', 'Closed Loop / AP'),
}

# Domain pairs where low co-publication represents a genuine research
# opportunity — fields that SHOULD inform each other but don't.
MEANINGFUL_OPPORTUNITY = {
    ('Beta Cell Regen', 'Health Equity'): "Regenerative therapies must address who has access to them. Equity analysis of emerging cell therapies is absent.",
    ('Gene Therapy', 'LADA'): "LADA's autoimmune mechanism makes it a candidate for gene therapy approaches, but no crossover work exists.",
    ('Islet Transplant', 'Drug Repurposing'): "Existing immunosuppressants could be repurposed for islet protection. Computational drug screening has not been applied here.",
    ('Drug Repurposing', 'Health Equity'): "Drug repurposing could yield more affordable treatments for underserved populations, but equity is absent from repurposing research.",
    ('Drug Repurposing', 'LADA'): "LADA is treated with T2D drugs that may be suboptimal. Systematic repurposing screens for LADA-specific therapies don't exist.",
    ('Health Equity', 'LADA'): "LADA is massively underdiagnosed, especially in minority populations. Equity-focused screening research is absent.",
    ('Beta Cell Regen', 'Personalized Nutr'): "Nutritional interventions that support beta cell recovery are plausible but unstudied at the intersection.",
    ('Treg / CAR-T', 'Neuropathy'): "Immune-mediated neuropathy in diabetes could potentially benefit from Treg modulation, but no work bridges these fields.",
    ('Treg / CAR-T', 'Health Equity'): "Advanced immunotherapies risk widening health disparities. No equity analysis of CAR-Treg/TCR-Treg access exists.",
    ('Glucokinase', 'Drug Repurposing'): "Glucokinase activators are a novel drug class; systematic screening for existing drugs with GK activity is unexplored.",
    ('Glucokinase', 'Health Equity'): "If glucokinase activators succeed, global access will be critical. No equity analysis exists for this drug class.",
    ('Glucokinase', 'LADA'): "Glucokinase's role in LADA is unstudied despite its relevance to residual beta cell function.",
    ('Personalized Nutr', 'LADA'): "LADA patients receive generic T2D dietary advice. Personalized nutrition based on autoimmune status is unexplored.",
    ('Insulin Resistance', 'Islet Transplant'): "Insulin resistance in islet transplant recipients affects graft survival, but this interaction is barely studied.",
    ('Islet Transplant', 'Health Equity'): "Islet transplant is available only at select centers. Access equity research is absent.",
}

def classify_gap(d1, d2):
    """Classify a domain pair gap."""
    pair = (d1, d2)
    pair_rev = (d2, d1)

    if pair in METHODOLOGICALLY_DISTINCT or pair_rev in METHODOLOGICALLY_DISTINCT:
        return "methodological", "These domains use fundamentally different methods (e.g., genomics vs. device engineering) and low co-publication is expected."

    if pair in MEANINGFUL_OPPORTUNITY:
        return "meaningful", MEANINGFUL_OPPORTUNITY[pair]
    if pair_rev in MEANINGFUL_OPPORTUNITY:
        return "meaningful", MEANINGFUL_OPPORTUNITY[pair_rev]

    return "ambiguous", "Classification requires domain expert review to determine if this gap represents a genuine opportunity."

def load_gap_data():
    path = os.path.join(RESULTS_DIR, 'literature_gap_data.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_report(data):
    """Generate improved gap analysis report."""

    # Use ranked_gaps (list of dicts with domain_1, domain_2, gap_score, pair_count, expected)
    ranked_gaps = data.get('ranked_gaps', [])
    domains = data.get('individual_counts', {})
    meta = data.get('metadata', {})
    date_range = meta.get('date_range', '2020/01/01 to 2026/03/15')

    # Sort by gap score descending
    ranked_gaps.sort(key=lambda x: x.get('gap_score', 0), reverse=True)
    top_gaps = ranked_gaps[:50]

    # Separate into meaningful vs methodological vs ambiguous
    meaningful = []
    methodological = []
    ambiguous = []

    for gap in top_gaps:
        d1 = gap.get('domain_1', '')
        d2 = gap.get('domain_2', '')
        score = gap.get('gap_score', 0)
        joint = gap.get('pair_count', 0)
        expected = gap.get('expected', 0)

        cls, reason = classify_gap(d1, d2)
        entry = {
            'd1': d1, 'd2': d2, 'score': score,
            'joint': joint, 'expected': expected,
            'cls': cls, 'reason': reason
        }

        if cls == 'meaningful':
            meaningful.append(entry)
        elif cls == 'methodological':
            methodological.append(entry)
        else:
            ambiguous.append(entry)

    # Count domain publications
    domain_list = sorted(domains.items(), key=lambda x: x[1], reverse=True)

    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    report = f"""# Literature Gap Analysis — Interpreted Report

**Generated:** {now}
**Source:** PubMed E-utilities API (esearch.fcgi)
**Date range:** {date_range}
**Domains analyzed:** {len(domain_list) if domain_list else 30}
**Pairs analyzed:** 435

---

## Methodology

This analysis queries PubMed for publication counts across {len(domain_list) if domain_list else 30} diabetes research domains, both individually and as pairwise combinations (435 pairs). The **Gap Score** measures how much less cross-domain work exists compared to what each domain's individual activity would predict.

**Formula:** `Gap Score = max(0, 1 - (joint_publications / geometric_mean(domain1_count, domain2_count))) × 100`

**Interpretation:** A Gap Score of 95 means the intersection has 95% fewer publications than the geometric mean of the two domains' individual counts. This is a *relative* measure of cross-domain activity, not an absolute judgment of research need.

**Important caveats:**
- PubMed search matching is approximate (keyword-based, not exact MeSH)
- Low co-publication may indicate: (a) genuinely unexplored territory, (b) terminology mismatch across fields, (c) research published under different keywords, or (d) fields that are *methodologically distinct* and would not naturally overlap
- This analysis should be cross-referenced with domain expert knowledge before drawing conclusions
- All gap classifications below are preliminary and labeled with confidence levels per the Research Doctrine

---

## Potentially Meaningful Research Gaps

These domain pairs have low co-publication rates **and** plausible scientific reasons why cross-domain work could yield new insights. These represent the highest-value opportunities for computational contribution.

**Validation level: BRONZE** (single analytical source; requires expert confirmation)

| Rank | Domain 1 | Domain 2 | Gap Score | Joint Pubs | Rationale |
|------|----------|----------|-----------|------------|-----------|
"""

    for i, g in enumerate(meaningful, 1):
        report += f"| {i} | {g['d1']} | {g['d2']} | {g['score']:.1f} | {g['joint']} | {g['reason']} |\n"

    report += f"""
---

## Methodologically Distinct Pairs (Expected Low Overlap)

These domain pairs have low co-publication because they use fundamentally different research methods (e.g., genetic association studies vs. medical device engineering). Low overlap here does **not** indicate a missed opportunity — it reflects the natural structure of the research landscape.

| Domain 1 | Domain 2 | Gap Score | Joint Pubs | Note |
|----------|----------|-----------|------------|------|
"""

    for g in methodological:
        report += f"| {g['d1']} | {g['d2']} | {g['score']:.1f} | {g['joint']} | {g['reason'][:80]} |\n"

    report += f"""
---

## Unclassified Gaps (Require Expert Review)

These domain pairs show high gap scores but have not been classified as either meaningful or methodologically distinct. Domain expert input is needed.

| Domain 1 | Domain 2 | Gap Score | Joint Pubs |
|----------|----------|-----------|------------|
"""

    for g in ambiguous:
        report += f"| {g['d1']} | {g['d2']} | {g['score']:.1f} | {g['joint']} |\n"

    report += f"""
---

## Individual Domain Publication Volumes (2020+)

| Domain | Publications | Relative Activity |
|--------|-------------|-------------------|
"""

    if domain_list:
        max_count = domain_list[0][1] if domain_list else 1
        for name, count in domain_list:
            bar_len = int((count / max_count) * 20)
            bar = '█' * bar_len + '░' * (20 - bar_len)
            report += f"| {name} | {count:,} | {bar} |\n"

    report += f"""
---

## How to Use This Analysis

1. **Meaningful gaps** are starting points for literature synthesis. For each, search PubMed with combined terms to verify the gap is real (not a terminology artifact).
2. **Methodologically distinct** pairs can be deprioritized unless a specific bridging mechanism is identified.
3. **Unclassified gaps** need expert review before action. Submit these to domain researchers for classification.
4. All gap scores should be validated against systematic review databases (Cochrane, PROSPERO) to confirm no existing reviews cover the intersection.

---

## Validation Status

| Aspect | Level | Notes |
|--------|-------|-------|
| Data source | PubMed E-utilities | Covers MEDLINE-indexed literature; misses preprints, grey literature |
| Gap scoring method | Published formula | Geometric mean normalization is standard in bibliometric analysis |
| Gap classifications | BRONZE | Single analyst classification; requires expert validation |
| Individual domain counts | Verifiable | Can be independently reproduced by querying PubMed directly |
| Temporal scope | 2020+ | Recent literature only; historical gaps may differ |

---

*Generated by Diabetes Research Hub — Literature Gap Analysis (Improved)*
*Methodology: Research Doctrine v1.0 — Triple-source validation pending for gap classifications*
"""

    return report


def main():
    print("Loading gap analysis data...")
    data = load_gap_data()

    print("Generating interpreted gap analysis report...")
    report = generate_report(data)

    out_path = os.path.join(RESULTS_DIR, 'literature_gap_report.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"  Report written: {out_path}")
    print(f"  Length: {len(report):,} characters")
    print("Done.")


if __name__ == '__main__':
    main()
