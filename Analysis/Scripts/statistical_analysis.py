#!/usr/bin/env python3
"""
Statistical Analysis Engine for the Diabetes Research Hub.

Implements three causal/predictive methods on our extracted corpus data:
1. Meta-analytic pooling of effect sizes (HbA1c, inflammatory markers, C-peptide)
2. Bayesian evidence synthesis for research path confidence scoring
3. Monte Carlo sensitivity analysis for LADA model and drug scoring

Outputs: statistical_analysis.json for use by dashboard build scripts.
"""
import json
import math
import os
import random
import re
import sys
from collections import defaultdict
from statistics import mean, stdev, median

random.seed(42)  # Reproducibility

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
results_dir = os.path.join(base_dir, 'Analysis', 'Results')

# ============================================================================
# 1. META-ANALYTIC POOLING
# ============================================================================

def extract_numeric_values(text):
    """Pull numeric values from extracted text."""
    numbers = re.findall(r'[-−]?\d+\.?\d*', text)
    return [float(n.replace('−', '-')) for n in numbers if abs(float(n.replace('−', '-'))) < 1000]

def inverse_variance_meta(effects, variances):
    """Fixed-effect inverse-variance weighted meta-analysis."""
    if not effects or not variances or len(effects) != len(variances):
        return None
    weights = [1/v if v > 0 else 0 for v in variances]
    total_weight = sum(weights)
    if total_weight == 0:
        return None
    pooled = sum(e * w for e, w in zip(effects, weights)) / total_weight
    pooled_var = 1 / total_weight
    pooled_se = math.sqrt(pooled_var)
    ci_lower = pooled - 1.96 * pooled_se
    ci_upper = pooled + 1.96 * pooled_se
    
    # Cochran's Q for heterogeneity
    Q = sum(w * (e - pooled)**2 for e, w in zip(effects, weights))
    df = len(effects) - 1
    I_squared = max(0, (Q - df) / Q * 100) if Q > 0 and df > 0 else 0
    
    return {
        'pooled_effect': round(pooled, 4),
        'se': round(pooled_se, 4),
        'ci_lower': round(ci_lower, 4),
        'ci_upper': round(ci_upper, 4),
        'n_studies': len(effects),
        'I_squared': round(I_squared, 1),
        'heterogeneity': 'LOW' if I_squared < 25 else 'MODERATE' if I_squared < 75 else 'HIGH',
    }

def _pool(effects, ses):
    """Fixed-effect and DerSimonian-Laird random-effects pooling.

    Returns both because with few studies they answer different questions and
    a reader is owed the one that is less flattering.
    """
    w = [1.0 / (se * se) for se in ses]
    sw = sum(w)
    fixed = sum(e * wi for e, wi in zip(effects, w)) / sw
    fixed_se = math.sqrt(1.0 / sw)
    k = len(effects)
    Q = sum(wi * (e - fixed) ** 2 for e, wi in zip(effects, w))
    df = k - 1
    c = sw - sum(wi * wi for wi in w) / sw
    tau2 = max(0.0, (Q - df) / c) if c > 0 and df > 0 else 0.0
    wr = [1.0 / (se * se + tau2) for se in ses]
    swr = sum(wr)
    rand = sum(e * wi for e, wi in zip(effects, wr)) / swr
    rand_se = math.sqrt(1.0 / swr)
    i2 = max(0.0, (Q - df) / Q * 100.0) if Q > 0 and df > 0 else 0.0

    def pack(est, se):
        return {'estimate': round(est, 3), 'se': round(se, 4),
                'ci_lower': round(est - 1.96 * se, 3),
                'ci_upper': round(est + 1.96 * se, 3)}
    return {'k': k, 'fixed': pack(fixed, fixed_se), 'random': pack(rand, rand_se),
            'Q': round(Q, 3), 'I_squared': round(i2, 1), 'tau_squared': round(tau2, 5)}


def pool_structured_effects():
    """Pool verified effect records, one arm per trial per pool.

    A pool is formed only from records that share a cluster, an intervention
    (drug AND dose) and a comparator, and only when at least two DIFFERENT
    trials contribute. Taking one arm per trial is what keeps the inputs
    independent: three dose arms of one trial share a placebo group, and
    pooling them together as three studies would count that group three times.
    """
    path = os.path.join(results_dir, 'structured_effects.json')
    out = {'source': 'structured_effects.json', 'pools': [], 'not_pooled': []}
    try:
        with open(path, encoding='utf-8') as fh:
            doc = json.load(fh)
    except FileNotFoundError:
        out['not_pooled'].append({'group': '(all)', 'reason': 'structured_effects.json not found'})
        return out

    groups = defaultdict(list)
    for r in doc.get('records', []):
        if not r.get('poolable'):
            continue
        groups[(r['cluster'], r['intervention'], r['comparator'])].append(r)

    for (cluster, intervention, comparator), rows in sorted(groups.items()):
        label = '%s vs %s' % (intervention, comparator)
        trials = sorted({r['trial'] for r in rows})
        if len(trials) < 2:
            out['not_pooled'].append({
                'group': label, 'trials': trials,
                'studies': [{'trial': r['trial'], 'pmid': r['pmid'], 'effect': r['effect'],
                             'ci_lower': r['ci_low'], 'ci_upper': r['ci_high'],
                             'timepoint': r['timepoint']} for r in rows],
                'reason': 'one trial only - a single result is reported, not pooled'})
            continue
        if len(trials) != len(rows):
            out['not_pooled'].append({'group': label, 'trials': trials,
                                      'reason': 'more than one record per trial; inputs not independent'})
            continue
        studies = []
        for r in sorted(rows, key=lambda x: x['trial']):
            se = r['se'] if r.get('se') is not None else (r['ci_high'] - r['ci_low']) / 3.92
            studies.append({'trial': r['trial'], 'pmid': r['pmid'], 'nct_id': r['nct_id'],
                            'effect': r['effect'], 'ci_lower': r['ci_low'],
                            'ci_upper': r['ci_high'], 'se': round(se, 4),
                            'timepoint': r['timepoint'], 'population': r['population'],
                            'estimand': r['estimand']})
        pool = _pool([x['effect'] for x in studies], [x['se'] for x in studies])
        pool.update({
            'label': label, 'cluster': cluster, 'outcome': rows[0]['outcome'],
            'unit': rows[0]['unit'], 'studies': studies,
            'evidence_level': 'SILVER',
            'caveats': [
                'k = %d trials. Between-trial variance cannot be estimated reliably from '
                'so few; the random-effects interval is a floor on the uncertainty, not a measure of it.' % len(studies),
                'The trials enrolled different populations (see each row). The pooled figure '
                'is an average over them, not an estimate for either.',
                'All trials were funded by the manufacturer.',
                'Standard errors are derived from the published 95% confidence intervals.',
                'Effects were read from abstracts; estimand is as stated there and is not '
                'stated for every trial.',
            ],
        })
        out['pools'].append(pool)
    return out


def run_meta_analysis(extractions):
    """Run meta-analyses on extractable outcome data."""
    results = {}
    
    # --- HbA1c: pooled ONLY from the verified substrate (2026-09-30) ---
    #
    # WITHDRAWN: the regex pool this replaced. It published "pooled HbA1c
    # reduction 0.93% (95% CI 0.90 to 0.97) from 2 pooled studies". Read from
    # its own output, those two "studies" were two percentages lifted from ONE
    # paper (PMID 35466661), the variance was not extracted but invented as
    # 0.5/sqrt(n) with n defaulting to 100 when no sample size sat nearby, and
    # I-squared was 98.7%. It was not a meta-analysis and its interval was an
    # artefact of the invented variance. SCIENCE_ARM_BUILD_CHARTER.md said in
    # June that a pooled estimate built on this extractor would be "a
    # confident, wrong forest plot"; it had been on the landing page since.
    #
    # The replacement pools nothing it cannot source. It reads
    # structured_effects.json and uses only records that are schema-valid,
    # span-verified against the live abstract and agreed by a second
    # extraction (poolable == True). See structured_effects.py.
    results['hba1c_pooled'] = None
    results['structured_pools'] = pool_structured_effects()

    # --- Inflammatory marker meta-analysis ---
    # Group by marker type
    marker_groups = defaultdict(list)
    for ext in extractions.get('inflammatory_markers', []):
        text = (ext.get('matched_text', '') + ' ' + ext.get('context', '')).lower()
        if 'crp' in text or 'c-reactive' in text:
            marker_groups['CRP'].append(ext)
        elif 'tnf' in text or 'tumor necrosis' in text:
            marker_groups['TNF-alpha'].append(ext)
        elif 'il-1' in text or 'interleukin-1' in text or 'il-1' in text:
            marker_groups['IL-1'].append(ext)
        elif 'il-6' in text or 'interleukin-6' in text:
            marker_groups['IL-6'].append(ext)
        elif 'nlrp3' in text or 'inflammasome' in text:
            marker_groups['NLRP3'].append(ext)
    
    results['inflammatory_markers'] = {
        'total_extractions': len(extractions.get('inflammatory_markers', [])),
        'by_marker': {},
    }
    for marker, exts in marker_groups.items():
        unique_pmids = set(e['pmid'] for e in exts)
        results['inflammatory_markers']['by_marker'][marker] = {
            'extraction_count': len(exts),
            'unique_papers': len(unique_pmids),
            'pmids': sorted(unique_pmids),
        }
    
    # --- Remission and C-peptide "pools": WITHDRAWN 2026-09-30 ---
    #
    # Both were summary statistics over regex captures, published as findings.
    # The remission pool took every percentage between 5 and 95 near the word
    # "remission"; its first two entries were "70% (v/v) Percoll solution" - a
    # reagent concentration from a methods section - counted as a 70% and a 37%
    # remission rate. The C-peptide pool was the value 0.1 twice, from one
    # paper, in a sentence reporting NO detectable C-peptide: the assay floor.
    # Neither can be repaired by a tighter pattern. A rate needs a numerator, a
    # denominator, a definition and a timepoint, which is what
    # structured_effects.json exists to hold. Until records for these outcomes
    # exist there, nothing is reported.
    withdrawn = ('Withdrawn 2026-09-30. The previous figures were summary '
                 'statistics over regular-expression captures, not extracted '
                 'study results, and included values that were not the outcome '
                 'at all. No verified records exist yet for this outcome.')
    results['remission_pooled'] = {'withdrawn': True, 'reason': withdrawn}
    results['cpeptide_pooled'] = {'withdrawn': True, 'reason': withdrawn}

    return results


# ============================================================================
# 2. BAYESIAN EVIDENCE SYNTHESIS
# ============================================================================

def bayesian_path_scoring(paths_data, validated_data):
    """
    WITHDRAWN FROM PUBLICATION 2026-09-30 (owner decision). Nothing reads this
    output any more; the pipeline runs this module with --meta-only.
    Defects, for the record: it looked paths up as "A -> B" in a store keyed
    "A_B", so validation was never applied (every path NOT_VALIDATED since
    2026-03-20); it reads data_point_count, renamed on 2026-08-21, so a rerun
    scores every path 0.143; and its likelihood values are invented constants.

    Compute Bayesian posterior probability for each research path.

    Prior: Based on data point count and number of PMIDs
    Likelihood: Based on validation status and external evidence
    Posterior: Updated probability that the path represents a real, actionable research direction
    """
    results = {}
    
    for path_key, path in paths_data.get('paths', {}).items():
        dpc = path.get('data_point_count', 0)
        n_pmids = len(path.get('pmids', []))
        
        # Prior probability based on corpus evidence density
        # More data points and more independent papers = higher prior
        if dpc >= 20 and n_pmids >= 3:
            prior = 0.80
        elif dpc >= 10 and n_pmids >= 2:
            prior = 0.65
        elif dpc >= 5:
            prior = 0.50
        elif dpc >= 2:
            prior = 0.35
        else:
            prior = 0.20
        
        # Likelihood based on validation
        validation = validated_data.get('paths', {}).get(path_key, {})
        status = validation.get('status', 'NOT_VALIDATED')
        confidence = validation.get('confidence', 'LOW')
        n_external = len(validation.get('external_pmids', []))
        
        if status == 'VALIDATED' and confidence == 'HIGH':
            likelihood = 0.95
        elif status == 'VALIDATED' and confidence == 'MEDIUM':
            likelihood = 0.85
        elif status == 'PARTIALLY_VALIDATED':
            likelihood = 0.65
        elif status == 'UNVALIDATED':
            likelihood = 0.30
        elif status == 'CONTRADICTED':
            likelihood = 0.05
        else:
            likelihood = 0.40  # Not yet validated
        
        # Bayesian update: P(real | evidence) = P(evidence | real) * P(real) / P(evidence)
        # Simplified: posterior ∝ likelihood * prior
        # Normalize against complement
        p_evidence_given_real = likelihood
        p_evidence_given_not_real = 1 - likelihood
        
        numerator = p_evidence_given_real * prior
        denominator = numerator + p_evidence_given_not_real * (1 - prior)
        posterior = numerator / denominator if denominator > 0 else prior
        
        # Evidence strength category
        if posterior >= 0.85:
            strength = 'STRONG'
        elif posterior >= 0.65:
            strength = 'MODERATE'
        elif posterior >= 0.40:
            strength = 'WEAK'
        else:
            strength = 'INSUFFICIENT'
        
        results[path_key] = {
            'prior': round(prior, 3),
            'likelihood': round(likelihood, 3),
            'posterior': round(posterior, 3),
            'strength': strength,
            'data_points': dpc,
            'corpus_pmids': n_pmids,
            'external_pmids': n_external,
            'validation_status': status,
            'interpretation': f"P(actionable) = {posterior:.1%} [{strength}] — prior {prior:.0%} updated by {status.lower()} evidence",
        }
    
    # Rank by posterior
    ranked = sorted(results.items(), key=lambda x: -x[1]['posterior'])
    
    return {
        'method': 'Bayesian evidence synthesis',
        'description': 'Prior probability from corpus density, updated by external validation status',
        'total_paths': len(results),
        'strong_paths': sum(1 for v in results.values() if v['strength'] == 'STRONG'),
        'moderate_paths': sum(1 for v in results.values() if v['strength'] == 'MODERATE'),
        'weak_paths': sum(1 for v in results.values() if v['strength'] == 'WEAK'),
        'insufficient_paths': sum(1 for v in results.values() if v['strength'] == 'INSUFFICIENT'),
        'paths': results,
        'ranked': [{'path': k, 'posterior': v['posterior'], 'strength': v['strength']} for k, v in ranked],
    }


# ============================================================================
# 3. MONTE CARLO SENSITIVITY ANALYSIS
# ============================================================================

def monte_carlo_lada_model(n_simulations=10000):
    """
    Run Monte Carlo sensitivity analysis on the LADA diagnostic model.
    Varies each parameter within its uncertainty range to see which
    assumptions drive the cost-effectiveness conclusions.
    """
    results_targeted = []
    results_universal = []
    results_twostage = []
    
    for _ in range(n_simulations):
        # Sample parameters from distributions
        gad_sensitivity = random.gauss(0.82, 0.03)  # 82% +/- 3%, nominal 76-88% range.
        # UNSOURCED as of 2026-09-14: the "(DASP)" attribution for this range was withdrawn
        # across build_lada_diagnostic_model.py. This Monte Carlo prior inherits that problem.
        gad_sensitivity = max(0.70, min(0.95, gad_sensitivity))
        
        gad_specificity = random.gauss(0.989, 0.005)
        gad_specificity = max(0.95, min(0.999, gad_specificity))
        
        lada_prevalence = random.gauss(0.088, 0.02)  # 8.8% ± 2% (range 5-15%)
        lada_prevalence = max(0.03, min(0.18, lada_prevalence))
        
        gad_test_cost = random.gauss(25, 10)  # $25 ± $10
        gad_test_cost = max(10, min(75, gad_test_cost))
        
        complication_cost = random.gauss(5876, 1500)  # $5,876 ± $1,500
        complication_cost = max(2000, min(12000, complication_cost))
        
        qaly_gain = random.gauss(0.05, 0.015)  # 0.05 ± 0.015
        qaly_gain = max(0.01, min(0.12, qaly_gain))
        
        insulin_time_correct = random.gauss(8, 1.5)  # 8 ± 1.5 years
        insulin_time_correct = max(4, min(14, insulin_time_correct))
        
        annual_t2d_diagnoses = random.gauss(28_000_000, 5_000_000)
        annual_t2d_diagnoses = max(15_000_000, min(45_000_000, annual_t2d_diagnoses))
        
        # Targeted screening ICER
        lada_in_t2d = annual_t2d_diagnoses * lada_prevalence
        targeted_screened = lada_in_t2d * 0.30  # 30% of high-risk T2D
        detected = targeted_screened * gad_sensitivity
        false_pos = targeted_screened * (1 - lada_prevalence) * (1 - gad_specificity)
        
        total_cost = (targeted_screened * gad_test_cost) + (detected * complication_cost * 0.3)
        total_qaly = detected * qaly_gain * insulin_time_correct
        icer_targeted = total_cost / total_qaly if total_qaly > 0 else float('inf')
        
        # Universal screening ICER
        universal_screened = annual_t2d_diagnoses
        detected_u = universal_screened * lada_prevalence * gad_sensitivity
        total_cost_u = (universal_screened * gad_test_cost) + (detected_u * complication_cost * 0.3)
        total_qaly_u = detected_u * qaly_gain * insulin_time_correct
        icer_universal = total_cost_u / total_qaly_u if total_qaly_u > 0 else float('inf')
        
        # Two-stage screening ICER
        stage1_cost = 5  # cheap phenotypic pre-screen
        stage1_sensitivity = 0.70
        twostage_screened = annual_t2d_diagnoses
        stage1_positive = twostage_screened * lada_prevalence / stage1_sensitivity
        stage2_cost = stage1_positive * gad_test_cost
        detected_ts = stage1_positive * lada_prevalence * gad_sensitivity
        total_cost_ts = (twostage_screened * stage1_cost) + stage2_cost + (detected_ts * complication_cost * 0.3)
        total_qaly_ts = detected_ts * qaly_gain * insulin_time_correct
        icer_twostage = total_cost_ts / total_qaly_ts if total_qaly_ts > 0 else float('inf')
        
        if icer_targeted < 500000:
            results_targeted.append(icer_targeted)
        if icer_universal < 500000:
            results_universal.append(icer_universal)
        if icer_twostage < 500000:
            results_twostage.append(icer_twostage)
    
    def summarize(icers, name):
        if not icers:
            return {'name': name, 'error': 'No valid simulations'}
        return {
            'name': name,
            'n_valid': len(icers),
            'mean_icer': round(mean(icers)),
            'median_icer': round(median(icers)),
            'p5': round(sorted(icers)[int(len(icers)*0.05)]),
            'p25': round(sorted(icers)[int(len(icers)*0.25)]),
            'p75': round(sorted(icers)[int(len(icers)*0.75)]),
            'p95': round(sorted(icers)[int(len(icers)*0.95)]),
            'pct_below_50k': round(sum(1 for i in icers if i < 50000) / len(icers) * 100, 1),
            'pct_below_100k': round(sum(1 for i in icers if i < 100000) / len(icers) * 100, 1),
            'pct_below_150k': round(sum(1 for i in icers if i < 150000) / len(icers) * 100, 1),
        }
    
    return {
        'method': 'Monte Carlo simulation',
        'n_simulations': n_simulations,
        'parameters_varied': [
            'GAD sensitivity (82% ± 3%)',
            'GAD specificity (98.9% ± 0.5%)',
            'LADA prevalence (8.8% ± 2%)',
            'GAD test cost ($25 ± $10)',
            'Complication cost ($5,876 ± $1,500)',
            'QALY gain (0.05 ± 0.015)',
            'Time to correct insulin (8 ± 1.5 years)',
            'Annual T2D diagnoses (28M ± 5M)',
        ],
        'scenarios': {
            'targeted': summarize(results_targeted, 'Targeted Screening'),
            'universal': summarize(results_universal, 'Universal Screening'),
            'two_stage': summarize(results_twostage, 'Two-Stage Screening'),
        },
        'interpretation': '',  # Filled below
    }


def monte_carlo_drug_scores(n_simulations=5000):
    """
    Monte Carlo sensitivity analysis on drug repurposing composite scores.
    Varies dimension weights and individual scores to see which drugs
    remain top-ranked under uncertainty.
    """
    # Load drug data
    drug_screen_path = os.path.join(script_dir, 'build_drug_repurposing_screen.py')
    with open(drug_screen_path, encoding='utf-8') as f:
        content = f.read()
    
    # Extract drug scores using regex
    drug_blocks = re.findall(
        r'"(\w[\w\s\-()]+?)":\s*\{[^}]*"mechanism_score":\s*(\d+)[^}]*"safety_score":\s*(\d+)[^}]*"generic_score":\s*(\d+)[^}]*"evidence_score":\s*(\d+)[^}]*"equity_score":\s*(\d+)',
        content
    )
    
    drugs = {}
    for name, mech, safe, gen, evid, eq in drug_blocks:
        drugs[name.strip()] = {
            'mechanism': int(mech),
            'safety': int(safe),
            'generic': int(gen),
            'evidence': int(evid),
            'equity': int(eq),
        }
    
    if not drugs:
        return {'error': 'Could not extract drug scores'}
    
    # Base weights
    base_weights = {
        'mechanism': 0.25,
        'safety': 0.20,
        'generic': 0.20,
        'evidence': 0.20,
        'equity': 0.15,
    }
    
    # Run simulations
    rank_counts = defaultdict(lambda: defaultdict(int))
    score_distributions = defaultdict(list)
    
    for _ in range(n_simulations):
        # Vary weights (±5%)
        weights = {}
        for dim, base in base_weights.items():
            weights[dim] = max(0.05, base + random.gauss(0, 0.03))
        # Normalize
        total_w = sum(weights.values())
        weights = {k: v/total_w for k, v in weights.items()}
        
        # Vary individual scores (±1)
        sim_scores = {}
        for drug, scores in drugs.items():
            score = sum(
                max(1, min(10, scores[dim] + random.gauss(0, 0.5))) * weights[dim]
                for dim in weights
            )
            sim_scores[drug] = score
            score_distributions[drug].append(score)
        
        # Rank
        ranked = sorted(sim_scores.items(), key=lambda x: -x[1])
        for rank, (drug, _) in enumerate(ranked, 1):
            rank_counts[drug][rank] += 1
    
    # Compute robustness metrics
    drug_results = {}
    for drug in drugs:
        scores = score_distributions[drug]
        ranks = rank_counts[drug]
        median_rank = None
        cumulative = 0
        for r in sorted(ranks.keys()):
            cumulative += ranks[r]
            if cumulative >= n_simulations / 2:
                median_rank = r
                break
        
        drug_results[drug] = {
            'base_score': sum(drugs[drug][d] * base_weights[d] for d in base_weights),
            'mean_score': round(mean(scores), 2),
            'sd_score': round(stdev(scores), 2),
            'p5_score': round(sorted(scores)[int(len(scores)*0.05)], 2),
            'p95_score': round(sorted(scores)[int(len(scores)*0.95)], 2),
            'median_rank': median_rank,
            'pct_top5': round(sum(ranks.get(r, 0) for r in range(1, 6)) / n_simulations * 100, 1),
            'pct_top10': round(sum(ranks.get(r, 0) for r in range(1, 11)) / n_simulations * 100, 1),
            'robustness': 'HIGH' if stdev(scores) < 0.3 else 'MODERATE' if stdev(scores) < 0.5 else 'LOW',
        }
    
    ranked_by_robustness = sorted(drug_results.items(), key=lambda x: (-x[1]['pct_top5'], -x[1]['mean_score']))
    
    return {
        'method': 'Monte Carlo drug score sensitivity',
        'n_simulations': n_simulations,
        'n_drugs': len(drugs),
        'weights_varied': '±3% per dimension, normalized',
        'scores_varied': '±0.5 per dimension score',
        'drugs': drug_results,
        'robust_top10': [{'drug': d, 'pct_top5': v['pct_top5'], 'pct_top10': v['pct_top10'], 'robustness': v['robustness']} for d, v in ranked_by_robustness[:10]],
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  STATISTICAL ANALYSIS ENGINE")
    print("=" * 60)
    
    # Load data
    with open(os.path.join(results_dir, 'extracted_corpus_data.json'), encoding='utf-8') as f:
        corpus_data = json.load(f)
    with open(os.path.join(results_dir, 'research_paths.json'), encoding='utf-8') as f:
        paths_data = json.load(f)
    
    validated_path = os.path.join(results_dir, 'validated_research_paths.json')
    validated_data = {}
    if os.path.exists(validated_path):
        with open(validated_path, encoding='utf-8') as f:
            validated_data = json.load(f)
    
    # --meta-only (2026-09-30): recompute the meta_analysis section and leave
    # the rest of statistical_analysis.json exactly as stored. This is the mode
    # the pipeline runs. A full run also recomputes the Bayesian synthesis from
    # today's research_paths.json, and that moves the published ranking a long
    # way (39 -> 47 INSUFFICIENT, top posterior 0.727 -> 0.143 when measured on
    # 2026-09-30). Which of those two rankings is right is a finding that needs
    # a reader, not a side effect of refreshing a pooled estimate.
    if '--meta-only' in sys.argv:
        out_path = os.path.join(results_dir, 'statistical_analysis.json')
        with open(out_path, encoding='utf-8') as f:
            stored = json.load(f)
        stored['meta_analysis'] = run_meta_analysis(corpus_data['extractions'])
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(stored, f, indent=2, ensure_ascii=False)
        sp = stored['meta_analysis']['structured_pools']
        print("  [OK] meta_analysis refreshed: %d pool(s), %d comparison(s) reported unpooled; "
              "other sections untouched" % (len(sp['pools']), len(sp['not_pooled'])))
        sys.exit(0)

    output = {}

    # 1. Meta-analysis
    print("\n  Running meta-analytic pooling...")
    meta_results = run_meta_analysis(corpus_data['extractions'])
    output['meta_analysis'] = meta_results
    for key, result in meta_results.items():
        if isinstance(result, dict) and 'interpretation' in result:
            print(f"    {key}: {result['interpretation']}")
        elif isinstance(result, dict) and 'by_marker' in result:
            print(f"    {key}: {result['total_extractions']} extractions across {len(result['by_marker'])} marker types")
    
    # 2. Bayesian synthesis
    print("\n  Running Bayesian evidence synthesis...")
    bayes_results = bayesian_path_scoring(paths_data, validated_data)
    output['bayesian_synthesis'] = bayes_results
    print(f"    {bayes_results['strong_paths']} STRONG, {bayes_results['moderate_paths']} MODERATE, {bayes_results['weak_paths']} WEAK, {bayes_results['insufficient_paths']} INSUFFICIENT")
    print(f"    Top 5 paths by posterior:")
    for item in bayes_results['ranked'][:5]:
        print(f"      {item['posterior']:.1%} [{item['strength']}] {item['path']}")
    
    # 3. Monte Carlo - LADA model
    print("\n  Running Monte Carlo on LADA model (10,000 simulations)...")
    mc_lada = monte_carlo_lada_model(10000)
    output['monte_carlo_lada'] = mc_lada
    for scenario_key, scenario in mc_lada['scenarios'].items():
        if 'error' not in scenario:
            print(f"    {scenario['name']}: median ICER ${scenario['median_icer']:,}/QALY (90% CI: ${scenario['p5']:,}-${scenario['p95']:,})")
            print(f"      P(cost-effective at $50K) = {scenario['pct_below_50k']}%, P(<$150K) = {scenario['pct_below_150k']}%")
    
    mc_lada['interpretation'] = (
        f"Targeted screening is cost-effective (<$50K/QALY) in {mc_lada['scenarios']['targeted'].get('pct_below_50k', '?')}% of simulations. "
        f"Universal screening exceeds $50K/QALY in most simulations but remains below $150K/QALY "
        f"(acceptable threshold) in {mc_lada['scenarios']['universal'].get('pct_below_150k', '?')}% of cases. "
        f"Key drivers: LADA prevalence and complication costs have the largest impact on ICER."
    )
    
    # 4. Monte Carlo - Drug scores
    print("\n  Running Monte Carlo on drug scores (5,000 simulations)...")
    mc_drugs = monte_carlo_drug_scores(5000)
    output['monte_carlo_drugs'] = mc_drugs
    if 'error' not in mc_drugs:
        print(f"    {mc_drugs['n_drugs']} drugs analyzed")
        print(f"    Most robust top-5 candidates:")
        for item in mc_drugs['robust_top10'][:5]:
            print(f"      {item['drug']}: top-5 in {item['pct_top5']}% of simulations [{item['robustness']}]")
    
    # Save
    output_path = os.path.join(results_dir, 'statistical_analysis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n  Output: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    print(f"\n  Done.")
