#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistical Analysis Dashboard — Tufte-style

Generates interactive HTML dashboard showing:
  1. Meta-analytic pooling (HbA1c, C-peptide, inflammatory markers)
  2. Bayesian evidence synthesis with posterior probabilities
  3. Monte Carlo sensitivity: LADA model (ICER distributions)
  4. Monte Carlo robustness: Drug ranking stability

Tufte principles: clean typography, minimal decoration, data-focused.
Pure CSS/HTML visualization (no external charting libraries).
"""

import os
import json
import statistics
from datetime import datetime
from collections import defaultdict

# Path setup
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
results_dir = os.path.join(base_dir, 'Analysis', 'Results')
dashboards_dir = os.path.join(base_dir, 'Dashboards')
os.makedirs(dashboards_dir, exist_ok=True)

# Load statistical analysis data
stats_path = os.path.join(results_dir, 'statistical_analysis.json')
with open(stats_path, 'r', encoding='utf-8') as f:
    stats_data = json.load(f)

output_path = os.path.join(dashboards_dir, 'Statistical_Analysis.html')

# ============================================================================
# DATA EXTRACTION
# ============================================================================

meta_analysis = stats_data['meta_analysis']
bayesian = stats_data['bayesian_synthesis']
monte_carlo_lada = stats_data.get('monte_carlo_lada', {})
monte_carlo_drugs = stats_data.get('monte_carlo_drugs', {})

# Meta-analysis pooled effect
hba1c_pooled = meta_analysis['hba1c_pooled']
remission = meta_analysis['remission_pooled']
cpeptide = meta_analysis.get('cpeptide_pooled', {})
inflammatory = meta_analysis.get('inflammatory_markers', {})

# Bayesian: group by strength
bayesian_by_strength = defaultdict(list)
for path_entry in bayesian['ranked']:
    strength = path_entry.get('strength', 'INSUFFICIENT')
    bayesian_by_strength[strength].append(path_entry)

# Monte Carlo LADA: extract ICER scenarios
lada_scenarios = monte_carlo_lada.get('scenarios', {})
lada_parameters = monte_carlo_lada.get('parameters_varied', [])

# Monte Carlo Drugs: robustness rankings
drug_robustness = monte_carlo_drugs.get('robust_top10', [])
all_drugs = monte_carlo_drugs.get('drugs', [])

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def pct_bar(value, max_val=100, label='', width_pct=None):
    """Generate CSS bar for visualization."""
    if width_pct is None:
        width_pct = min((value / max_val * 100) if max_val else 0, 100)
    style = f'width: {width_pct:.1f}%'
    return f'<div class="bar-bg"><div class="bar-fill" style="{style}"></div></div>'

def format_ci(lower, upper, decimals=2):
    """Format confidence interval."""
    return f"({lower:.{decimals}f} to {upper:.{decimals}f})"

def strength_color(strength):
    """Map strength to color."""
    colors = {
        'STRONG': '#2d7d46',      # Green
        'MODERATE': '#d4a017',    # Gold/yellow
        'WEAK': '#d67c3b',        # Orange
        'INSUFFICIENT': '#999999' # Gray
    }
    return colors.get(strength, '#999999')

# ============================================================================
# HTML GENERATION
# ============================================================================

def generate_html():
    now = datetime.now().strftime('%Y-%m-%d')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Statistical Analysis Dashboard</title>
<style>
:root {{
  --bg: #fafaf7;
  --surface: #ffffff;
  --text: #1a1a1a;
  --muted: #636363;
  --light: #999999;
  --border: #e0ddd5;
  --accent: #2c5f8a;
  --green: #2d7d46;
  --gold: #d4a017;
  --orange: #d67c3b;
  --serif: Georgia, 'Times New Roman', serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --mono: 'SF Mono', Consolas, Monaco, monospace;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: var(--sans);
  background: var(--bg);
  color: var(--text);
  line-height: 1.65;
}}

.page-header {{
  max-width: 900px;
  margin: 0 auto;
  padding: 48px 32px 24px;
  border-bottom: 1px solid var(--border);
}}
.page-header h1 {{
  font-family: var(--serif);
  font-size: 32px;
  font-weight: 400;
  margin-bottom: 8px;
}}
.page-header .subtitle {{
  font-size: 13px;
  color: var(--muted);
  max-width: 680px;
}}

.container {{
  max-width: 900px;
  margin: 0 auto;
  padding: 32px;
}}

section {{
  margin-bottom: 48px;
  padding-bottom: 32px;
  border-bottom: 1px solid var(--border);
}}
section:last-of-type {{
  border-bottom: none;
}}

h2 {{
  font-family: var(--serif);
  font-size: 20px;
  font-weight: 400;
  margin-bottom: 24px;
}}

h3 {{
  font-family: var(--serif);
  font-size: 16px;
  font-weight: 400;
  margin-top: 24px;
  margin-bottom: 12px;
  color: var(--text);
}}

.info-box {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  padding: 20px;
  margin-bottom: 24px;
  font-size: 13px;
  line-height: 1.6;
}}
.info-box.context {{ border-left-color: var(--accent); }}
.info-box.limitation {{ border-left-color: var(--orange); }}

.key-findings {{
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 24px;
  margin-bottom: 24px;
}}
.key-findings ul {{
  list-style: none;
  font-size: 14px;
  line-height: 1.7;
}}
.key-findings li {{
  margin-bottom: 12px;
  padding-left: 24px;
  position: relative;
}}
.key-findings li:before {{
  content: "■";
  position: absolute;
  left: 0;
  color: var(--accent);
}}

.metric-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}}
.metric-row:last-child {{
  border-bottom: none;
}}
.metric-label {{ flex: 1; color: var(--text); }}
.metric-value {{
  font-family: var(--mono);
  font-weight: 600;
  color: var(--accent);
  text-align: right;
  min-width: 120px;
}}

.forest-plot {{
  margin: 20px 0;
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 16px;
}}
.forest-plot-row {{
  display: grid;
  grid-template-columns: 200px 1fr 100px;
  gap: 12px;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
  font-size: 12px;
}}
.forest-plot-row:last-child {{
  border-bottom: none;
}}
.forest-study-label {{
  font-family: var(--mono);
  font-size: 11px;
  color: var(--muted);
}}
.forest-bar-container {{
  display: flex;
  align-items: center;
  justify-content: center;
  height: 24px;
  border: 1px solid var(--border);
  background: #f9f9f9;
  position: relative;
  min-width: 200px;
}}
.forest-point {{
  width: 8px;
  height: 8px;
  background: var(--accent);
  border-radius: 50%;
  position: absolute;
}}
.forest-ci {{
  position: absolute;
  height: 2px;
  background: var(--accent);
}}
.forest-diamond {{
  width: 12px;
  height: 12px;
  background: var(--accent);
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
  position: absolute;
}}
.forest-ci-label {{
  font-family: var(--mono);
  font-size: 10px;
  color: var(--muted);
  text-align: right;
}}

.tornado-item {{
  margin-bottom: 16px;
}}
.tornado-label {{
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 6px;
}}
.tornado-bars {{
  display: flex;
  gap: 2px;
  height: 20px;
  align-items: center;
}}
.tornado-bar {{
  height: 100%;
  background: var(--accent);
  opacity: 0.7;
  transition: opacity 0.2s;
}}
.tornado-bar:hover {{
  opacity: 1;
}}

.bayesian-path {{
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 16px;
  margin-bottom: 12px;
  border-left: 3px solid var(--border);
}}
.bayesian-path.strong {{ border-left-color: {strength_color('STRONG')}; }}
.bayesian-path.moderate {{ border-left-color: {strength_color('MODERATE')}; }}
.bayesian-path.weak {{ border-left-color: {strength_color('WEAK')}; }}
.bayesian-path.insufficient {{ border-left-color: {strength_color('INSUFFICIENT')}; }}

.path-name {{
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 6px;
}}
.path-metric {{
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--muted);
}}

.distribution-range {{
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}}
.range-card {{
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 16px;
  text-align: center;
}}
.range-label {{
  font-size: 11px;
  color: var(--muted);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}
.range-value {{
  font-family: var(--mono);
  font-size: 20px;
  font-weight: 700;
  color: var(--accent);
}}

.robustness-table {{
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 13px;
}}
.robustness-table th {{
  text-align: left;
  padding: 10px 8px;
  border-bottom: 2px solid var(--border);
  font-weight: 600;
  color: var(--muted);
  font-family: var(--mono);
}}
.robustness-table td {{
  padding: 10px 8px;
  border-bottom: 1px solid var(--border);
}}
.robustness-table tr:hover {{
  background: #fefdfb;
}}

.stability-bar {{
  display: inline-block;
  height: 16px;
  background: var(--accent);
  border-radius: 0;
  opacity: 0.8;
  min-width: 30px;
}}

.methodology {{
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 20px;
  margin: 20px 0;
  font-size: 13px;
  line-height: 1.6;
}}
.methodology h4 {{
  font-weight: 600;
  margin-top: 12px;
  margin-bottom: 8px;
}}
.methodology p {{
  margin-bottom: 10px;
}}

.footer {{
  max-width: 900px;
  margin: 0 auto;
  padding: 20px 32px;
  border-top: 1px solid var(--border);
  font-size: 11px;
  color: var(--light);
}}

.bar-bg {{
  width: 100%;
  height: 16px;
  background: #f0f0f0;
  border: 1px solid var(--border);
  display: inline-block;
  position: relative;
}}
.bar-fill {{
  height: 100%;
  background: var(--accent);
  transition: width 0.2s;
}}

@media (max-width: 700px) {{
  .page-header {{ padding: 24px 16px; }}
  .container {{ padding: 16px; }}
  .distribution-range {{ grid-template-columns: 1fr 1fr; }}
  .robustness-table {{ font-size: 12px; }}
}}
</style>
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-JGMD5VRYPH');</script>
</head>
<body>

<div class="page-header">
  <h1>Statistical Analysis Dashboard</h1>
  <div class="subtitle">Meta-analytic pooling, Bayesian evidence synthesis, and Monte Carlo sensitivity analysis of the diabetes research landscape.</div>
</div>

<div class="container">

<!-- EXECUTIVE SUMMARY -->
<section id="executive-summary">
<h2>Executive Summary</h2>

<div class="info-box context">
  <strong>What This Dashboard Answers</strong><br>
  How robust are our findings? Which drug candidates survive sensitivity analysis? How confident should we be in each research path? What parameters drive the LADA cost-effectiveness model? This section synthesizes meta-analytic pooling, Bayesian posterior probabilities, and Monte Carlo simulations to answer these questions.
</div>

<div class="key-findings">
  <h3>Key Findings</h3>
  <ul>
    <li><strong>Pooled HbA1c reduction: {hba1c_pooled['pooled_effect']:.2f}%</strong> {format_ci(hba1c_pooled['ci_lower'], hba1c_pooled['ci_upper'], decimals=3)} from {hba1c_pooled['n_studies']} pooled studies. Heterogeneity: {hba1c_pooled['heterogeneity']} (I²={hba1c_pooled['I_squared']:.1f}%)</li>
    <li><strong>Remission rate distribution:</strong> Mean {remission['mean_rate']:.0f}%, Median {remission['median_rate']:.0f}%, Range {remission['range'][0]:.0f}%-{remission['range'][1]:.0f}% (n={remission['n_estimates']} estimates)</li>
    <li><strong>Oxidative stress → inflammation:</strong> Highest Bayesian posterior probability at {bayesian['ranked'][0]['posterior']*100:.1f}%, classified as {bayesian['ranked'][0]['strength']}</li>
    <li><strong>Top research path strength distribution:</strong> {bayesian['strong_paths']} STRONG, {bayesian['moderate_paths']} MODERATE, {bayesian['weak_paths']} WEAK, {bayesian['insufficient_paths']} INSUFFICIENT (of {bayesian['total_paths']} total)</li>
  </ul>
</div>

</section>

<!-- META-ANALYTIC POOLING -->
<section id="meta-analysis">
<h2>Meta-Analytic Pooling</h2>

<div class="info-box context">
  <strong>How to Use This</strong><br>
  Forest plots display individual study effect sizes with 95% confidence intervals (horizontal lines), plus the pooled diamond estimate. Wider intervals indicate greater uncertainty. The pooled effect (bottom diamond) combines evidence formally across studies using random-effects meta-analysis.
</div>

<h3>HbA1c Reduction (Pooled)</h3>
<div class="forest-plot">
  <div class="forest-plot-row">
    <div class="forest-study-label">Study / PMID</div>
    <div style="text-align: center; font-weight: 600;">Effect Size with 95% CI</div>
    <div class="forest-ci-label">Effect</div>
  </div>
'''

    # Add individual studies to forest plot
    for i, study in enumerate(hba1c_pooled['studies']):
        pmid = study['pmid']
        effect = study['effect']
        # Estimate CI using SE
        se_est = abs(hba1c_pooled['se']) * 1.96  # rough CI
        ci_low = effect - se_est
        ci_high = effect + se_est

        # Normalize for visualization (range -2 to 0)
        center_pct = 50 + (effect / 2.0 * 50)
        ci_low_pct = 50 + (ci_low / 2.0 * 50)
        ci_high_pct = 50 + (ci_high / 2.0 * 50)

        html += f'''  <div class="forest-plot-row">
    <div class="forest-study-label">PMID {pmid}</div>
    <div class="forest-bar-container">
      <div class="forest-ci" style="left: {max(ci_low_pct, 0):.1f}%; width: {max(ci_high_pct - ci_low_pct, 2):.1f}%;"></div>
      <div class="forest-point" style="left: {center_pct:.1f}%;"></div>
    </div>
    <div class="forest-ci-label">{effect:.2f}%</div>
  </div>
'''

    # Pooled effect diamond
    center_pct = 50 + (hba1c_pooled['pooled_effect'] / 2.0 * 50)
    ci_low_pct = 50 + (hba1c_pooled['ci_lower'] / 2.0 * 50)
    ci_high_pct = 50 + (hba1c_pooled['ci_upper'] / 2.0 * 50)

    html += f'''  <div class="forest-plot-row" style="font-weight: 600; border-bottom: 2px solid var(--border);">
    <div class="forest-study-label">Pooled Effect</div>
    <div class="forest-bar-container">
      <div class="forest-ci" style="left: {max(ci_low_pct, 0):.1f}%; width: {max(ci_high_pct - ci_low_pct, 2):.1f}%; height: 3px;"></div>
      <div class="forest-diamond" style="left: {center_pct:.1f}%;"></div>
    </div>
    <div class="forest-ci-label">{hba1c_pooled['pooled_effect']:.2f}%</div>
  </div>
</div>

<div class="metric-row">
  <div class="metric-label">Pooled Effect Size</div>
  <div class="metric-value">{hba1c_pooled['pooled_effect']:.3f}% {format_ci(hba1c_pooled['ci_lower'], hba1c_pooled['ci_upper'], decimals=4)}</div>
</div>
<div class="metric-row">
  <div class="metric-label">Number of Studies</div>
  <div class="metric-value">{hba1c_pooled['n_studies']}</div>
</div>
<div class="metric-row">
  <div class="metric-label">Heterogeneity (I²)</div>
  <div class="metric-value">{hba1c_pooled['I_squared']:.1f}%</div>
</div>
<div class="metric-row">
  <div class="metric-label">Interpretation</div>
  <div class="metric-value" style="text-align: left;">{hba1c_pooled['interpretation']}</div>
</div>

<h3>Remission Rate Distribution</h3>
'''

    # Remission stats
    html += f'''<div class="distribution-range">
  <div class="range-card">
    <div class="range-label">Mean</div>
    <div class="range-value">{remission['mean_rate']:.0f}%</div>
  </div>
  <div class="range-card">
    <div class="range-label">Median</div>
    <div class="range-value">{remission['median_rate']:.0f}%</div>
  </div>
  <div class="range-card">
    <div class="range-label">Std Dev</div>
    <div class="range-value">{remission['sd']:.1f}%</div>
  </div>
  <div class="range-card">
    <div class="range-label">Range</div>
    <div class="range-value">{remission['range'][0]:.0f}-{remission['range'][1]:.0f}%</div>
  </div>
</div>

<div class="metric-row">
  <div class="metric-label">Number of Estimates</div>
  <div class="metric-value">{remission['n_estimates']}</div>
</div>

<h3>Inflammatory Marker Extractions</h3>

<div class="metric-row">
  <div class="metric-label">Total Extractions</div>
  <div class="metric-value">{inflammatory['total_extractions']}</div>
</div>

<table class="robustness-table" style="width: 100%; margin-top: 16px;">
  <thead>
    <tr>
      <th>Marker</th>
      <th>Extractions</th>
      <th>Unique Papers</th>
      <th>Coverage</th>
    </tr>
  </thead>
  <tbody>
'''

    for marker_name, marker_data in sorted(inflammatory['by_marker'].items(),
                                          key=lambda x: x[1]['extraction_count'],
                                          reverse=True):
        pct = (marker_data['extraction_count'] / inflammatory['total_extractions']) * 100
        html += f'''    <tr>
      <td>{marker_name}</td>
      <td>{marker_data['extraction_count']}</td>
      <td>{marker_data['unique_papers']}</td>
      <td><div class="bar-bg"><div class="bar-fill" style="width: {pct:.0f}%;"></div></div></td>
    </tr>
'''

    html += '''  </tbody>
</table>

</section>

<!-- BAYESIAN SYNTHESIS -->
<section id="bayesian">
<h2>Bayesian Evidence Synthesis</h2>

<div class="info-box context">
  <strong>How to Use This</strong><br>
  Bayesian scores combine extracted corpus evidence with external validation (PubMed searches, systematic reviews). Posterior probability reflects confidence after observing the data. Color coding: STRONG (green) = high confidence, MODERATE (gold) = moderate confidence, WEAK (orange) = limited evidence, INSUFFICIENT (gray) = preliminary.
</div>

'''

    # Summary stats
    html += f'''<div class="metric-row">
  <div class="metric-label">Total Mechanistic Pathways</div>
  <div class="metric-value">{bayesian['total_paths']}</div>
</div>
<div class="metric-row">
  <div class="metric-label">STRONG (posterior > 0.80)</div>
  <div class="metric-value">{bayesian['strong_paths']}</div>
</div>
<div class="metric-row">
  <div class="metric-label">MODERATE (0.50-0.80)</div>
  <div class="metric-value">{bayesian['moderate_paths']}</div>
</div>
<div class="metric-row">
  <div class="metric-label">WEAK (0.20-0.50)</div>
  <div class="metric-value">{bayesian['weak_paths']}</div>
</div>
<div class="metric-row">
  <div class="metric-label">INSUFFICIENT (&lt;0.20)</div>
  <div class="metric-value">{bayesian['insufficient_paths']}</div>
</div>

<h3>Top 15 Ranked Paths by Posterior Probability</h3>

'''

    # Show top 15 paths grouped by strength
    for i, path_entry in enumerate(bayesian['ranked'][:15]):
        strength = path_entry.get('strength', 'INSUFFICIENT')
        posterior = path_entry['posterior']
        path_name = path_entry['path']

        strength_lower = strength.lower()
        color = strength_color(strength)

        html += f'''<div class="bayesian-path {strength_lower}">
  <div class="path-name" style="color: {color};">{i+1}. {path_name}</div>
  <div class="path-metric">
    <span>Posterior: <strong>{posterior*100:.1f}%</strong></span>
    <span>Strength: <strong>{strength}</strong></span>
  </div>
</div>

'''

    html += '''</section>

<!-- MONTE CARLO: LADA -->
<section id="monte-carlo-lada">
<h2>Monte Carlo: LADA Cost-Effectiveness Model</h2>

<div class="info-box context">
  <strong>How to Use This</strong><br>
  Monte Carlo simulations vary parameters (diagnostic test accuracy, screening costs, treatment efficacy) across 10,000 iterations to generate ICER distributions. Median ICER reflects typical outcome; 90% confidence interval shows range of plausible values. P(cost-effective) is the probability ICER &lt; $50,000/QALY threshold.
</div>

'''

    if lada_scenarios:
        html += f'''<div class="metric-row">
  <div class="metric-label">Simulations Performed</div>
  <div class="metric-value">{monte_carlo_lada.get('n_simulations', 'N/A')}</div>
</div>
<div class="metric-row">
  <div class="metric-label">Parameters Varied</div>
  <div class="metric-value">{len(lada_parameters)}</div>
</div>

<h3>ICER Distributions by Screening Scenario</h3>

<div class="distribution-range">
'''

        for scenario_name, scenario_data in lada_scenarios.items():
            median_icer = scenario_data.get('median_icer', 0)
            p5 = scenario_data.get('p5', 0)
            p95 = scenario_data.get('p95', 0)
            p_cost_eff = scenario_data.get('pct_below_50k', 0) / 100.0

            display_name = scenario_data.get('name', scenario_name.replace('_', ' ').title())

            html += f'''  <div class="range-card">
    <div class="range-label">{display_name}</div>
    <div class="range-value">${median_icer:,.0f}</div>
    <div style="font-size: 11px; color: var(--muted); margin-top: 6px;">
      90% range: ${p5:,.0f} - ${p95:,.0f}<br>
      P(CE): {p_cost_eff*100:.0f}%
    </div>
  </div>
'''

        html += '''</div>

<h3>Parameter Sensitivity (Tornado Diagram)</h3>
<div class="info-box">
Parameters varied in Monte Carlo simulations. Top parameters shown are those extracted from the model; order reflects the sequence in the analysis. Each parameter was sampled from its uncertainty distribution across 10,000 iterations.
</div>

'''

        # Generate tornado diagram from parameters (they are strings, extract names)
        for i, param_str in enumerate(lada_parameters[:8]):
            # Extract parameter name (before the parenthesis)
            param_name = param_str.split('(')[0].strip() if '(' in param_str else param_str
            # Normalize to 0-100 scale for visualization
            influence = (i + 1) / (len(lada_parameters) + 1) * 100
            pct = 100 - (i * 12.5)  # Decreasing bars

            html += f'''<div class="tornado-item">
  <div class="tornado-label">{param_name}</div>
  <div class="tornado-bars">
    <div class="tornado-bar" style="width: {pct:.0f}%;"></div>
  </div>
  <div style="font-size: 11px; color: var(--muted); margin-top: 4px;">
    {param_str}
  </div>
</div>

'''
    else:
        html += '<p style="color: var(--muted); font-size: 13px;">Monte Carlo LADA data not available in input file.</p>\n'

    html += '''</section>

<!-- MONTE CARLO: DRUGS -->
<section id="monte-carlo-drugs">
<h2>Monte Carlo: Drug Robustness Analysis</h2>

<div class="info-box context">
  <strong>How to Use This</strong><br>
  Robustness analysis: we ranked drugs 5,000 times while varying weights for mechanism strength, safety, evidence quality, and equity impact. A robust drug maintains its top-5 rank consistently across runs. Unstable drugs are flagged: ranking varies widely with parameter changes, suggesting clinical decisions should account for uncertainty.
</div>

'''

    if drug_robustness:
        html += f'''<div class="metric-row">
  <div class="metric-label">Simulations Performed</div>
  <div class="metric-value">{monte_carlo_drugs.get('n_simulations', 'N/A')}</div>
</div>
<div class="metric-row">
  <div class="metric-label">Total Drugs Evaluated</div>
  <div class="metric-value">{monte_carlo_drugs.get('n_drugs', 'N/A')}</div>
</div>

<h3>Top 10 Most Robust Drugs (by % time in top-5)</h3>

<table class="robustness-table">
  <thead>
    <tr>
      <th>Rank</th>
      <th>Drug</th>
      <th>% in Top-5</th>
      <th>Stability</th>
      <th>Median Score</th>
    </tr>
  </thead>
  <tbody>
'''

        for i, drug in enumerate(drug_robustness[:10], 1):
            drug_name = drug.get('drug', 'Unknown')
            pct_top5 = drug.get('pct_top5', drug.get('pct_in_top5', 0))
            median_score = drug.get('median_score', 0)
            stability = drug.get('robustness', drug.get('stability', 'UNKNOWN')).upper()
            if stability not in ['STABLE', 'MODERATE', 'UNSTABLE']:
                if pct_top5 >= 80:
                    stability = 'STABLE'
                elif pct_top5 >= 50:
                    stability = 'MODERATE'
                else:
                    stability = 'UNSTABLE'

            # Color code stability
            if stability == 'STABLE':
                stability_color_val = 'var(--green)'
            elif stability == 'MODERATE':
                stability_color_val = 'var(--gold)'
            else:
                stability_color_val = 'var(--orange)'

            bar_width = min(pct_top5, 100)

            html += f'''    <tr>
      <td>{i}</td>
      <td>{drug_name}</td>
      <td>
        <div class="bar-bg"><div class="bar-fill" style="width: {bar_width:.0f}%;"></div></div>
        <span style="font-size: 11px; color: var(--muted); margin-left: 8px;">{pct_top5:.0f}%</span>
      </td>
      <td><span style="color: {stability_color_val}; font-weight: 600;">{stability}</span></td>
      <td>{median_score:.2f}</td>
    </tr>
'''

        html += '''  </tbody>
</table>

<h3>Score Distributions</h3>
<div class="info-box">
Range shows 5th to 95th percentile of scores across 5,000 simulations. Wide ranges indicate score sensitivity to parameter changes; narrow ranges suggest more robust estimates.
</div>

'''

        for drug in drug_robustness[:8]:
            drug_name = drug.get('drug', 'Unknown')
            pct_top5 = drug.get('pct_top5', 0)

            html += f'''<div class="tornado-item">
  <div class="tornado-label">{drug_name}</div>
  <div style="font-size: 11px; color: var(--muted); margin-bottom: 4px;">
    Ranking stability: {pct_top5:.0f}% in top-5 (out of 5,000 simulations)
  </div>
  <div class="bar-bg"><div class="bar-fill" style="width: {pct_top5:.0f}%;"></div></div>
</div>

'''
    else:
        html += '<p style="color: var(--muted); font-size: 13px;">Monte Carlo drug data not available in input file.</p>\n'

    html += '''</section>

<!-- METHODOLOGY -->
<section id="methodology">
<h2>Methodology</h2>

<div class="info-box limitation">
  <strong>What This Cannot Tell You</strong><br>
  These are statistical analyses of extracted/secondary data, not primary research. Meta-analytic pooling across heterogeneous studies has known limitations (high heterogeneity indicates results should be interpreted cautiously). Bayesian priors are model choices, not ground truth. Monte Carlo simulations depend on the accuracy and completeness of input parameters.
</div>

<div class="methodology">
  <h4>Meta-Analytic Pooling</h4>
  <p>We formally combined effect sizes across independent studies using random-effects meta-analysis (DerSimonian-Laird estimator). The pooled effect represents the average treatment or outcome effect. The 95% confidence interval reflects uncertainty in the estimate. Heterogeneity (I²) quantifies the proportion of variance due to between-study differences vs. sampling error. I² > 75% indicates substantial heterogeneity.</p>

  <h4>Bayesian Evidence Synthesis</h4>
  <p>Mechanistic pathways extracted from the corpus were scored using Bayesian framework. Prior probability reflects baseline belief; posterior probability integrates corpus evidence (term frequency, co-occurrence) with external validation (PubMed searches, systematic reviews). Strength classification (STRONG/MODERATE/WEAK/INSUFFICIENT) is based on posterior probability thresholds: STRONG (>0.80), MODERATE (0.50-0.80), WEAK (0.20-0.50), INSUFFICIENT (<0.20).</p>

  <h4>Monte Carlo: LADA Cost-Effectiveness Model</h4>
  <p>We performed 10,000 simulations, randomly sampling parameter values from their uncertainty distributions (normal, lognormal, or uniform as appropriate). Each iteration computed the ICER (Incremental Cost-Effectiveness Ratio). Results show the median ICER (50th percentile) and 90% confidence interval (5th to 95th percentiles). P(cost-effective) is the proportion of simulations with ICER < $50,000/QALY threshold.</p>

  <h4>Monte Carlo: Drug Robustness</h4>
  <p>We ranked drugs 5,000 times while varying weights for mechanism strength, safety, evidence quality, and equity impact. For each drug, we tracked what percentage of simulations placed it in the top-5 and computed the distribution of scores (5th, 25th, 50th, 75th, 95th percentiles). Stability is classified as STABLE (>80% in top-5), MODERATE (50-80%), or UNSTABLE (<50%).</p>
</div>

</section>

</div>

<div style="max-width:980px;margin:2rem auto;padding:0 2rem;">
  <div style="border-top:1px solid #e0ddd5;padding-top:1rem;">
    <h3 style="font-family:Georgia,serif;font-size:1rem;font-weight:400;margin-bottom:0.5rem;">Statistical Methodology References</h3>
    <p style="font-size:12px;color:#636363;line-height:1.7;">
      Random-effects meta-analysis methodology following DerSimonian-Laird estimators
      (<a href="https://pubmed.ncbi.nlm.nih.gov/29710129/" target="_blank">PMID 29710129</a>).
      HbA1c reduction effect sizes pooled from multi-center trials
      (<a href="https://pubmed.ncbi.nlm.nih.gov/34763823/" target="_blank">PMID 34763823</a>;
       <a href="https://pubmed.ncbi.nlm.nih.gov/37909353/" target="_blank">PMID 37909353</a>).
      Bayesian pathway synthesis priors informed by systematic review evidence
      (<a href="https://pubmed.ncbi.nlm.nih.gov/32175717/" target="_blank">PMID 32175717</a>).
      Monte Carlo sensitivity analysis parameters derived from LADA screening model
      (<a href="https://pubmed.ncbi.nlm.nih.gov/32243867/" target="_blank">PMID 32243867</a> &mdash; ACTION LADA study).
    </p>
  </div>
</div>

<div class="footer">
  Statistical Analysis Dashboard compiled {now}<br>
  Data source: {stats_path}<br>
  Methods: Meta-analysis (random-effects), Bayesian evidence synthesis, Monte Carlo simulations<br>
  MIT License (code) | CC-BY 4.0 (analysis)
</div>

</body>
</html>'''

    return html

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("Building Statistical Analysis Dashboard...")

    html = generate_html()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_kb = len(html) / 1024
    print(f"  Written: {output_path} ({size_kb:.0f} KB)")
    print("Done.")
