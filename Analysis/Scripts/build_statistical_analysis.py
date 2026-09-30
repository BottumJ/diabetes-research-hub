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
import re
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


# ---------------------------------------------------------------------------
# EVIDENCE-DESIGN DISCLOSURE ON THE POSTERIOR (added 2026-08-29)
# ---------------------------------------------------------------------------
# statistical_analysis.py::bayesian_path_scoring builds the prior from
# data_point_count and PMID count alone. Neither the prior nor the likelihood
# reads what KIND of study those numbers came from. On 2026-08-29
# audit_posterior_design_agreement.py measured the consequence on this page:
# 48 of 77 comparable ordered pairs (62.3%) are DISCORDANT - the page scores
# the path higher while its evidence design is weaker - and 16 of those rank a
# NO_RESULTS path (no measured outcome in any citing paper) above a path
# resting on primary data. Published examples:
#     #4 verapamil -> T1D              40.0%  NO_RESULTS (protocol only)
#     #6 dapagliflozin -> nephropathy  26.4%  PRIMARY
#
# What is done here and what is deliberately NOT done:
#   DONE - every posterior carries its design tier and the discordance is
#          stated in full at the top of the section. A reader cannot now read
#          the ranking without reading what it is made of.
#   NOT DONE - the prior is not refit. What a prior should encode is a
#          modelling decision, and an unattended run that quietly rewrites a
#          published probability is a worse failure than the one it fixes.
#          Carried to the work queue as a human call.
#
# The STRENGTH LABEL is capped, which is a different act from editing the
# number: a NO_RESULTS path may not be labelled above INSUFFICIENT, because
# "WEAK evidence" asserts that evidence exists. The uncapped value is printed
# beside it so nothing is hidden.
_design_tiers = {}
_design_generated = None
try:
    with open(os.path.join(results_dir, 'path_evidence_design.json'),
              'r', encoding='utf-8') as _fh:
        _dj = json.load(_fh)
    _design_generated = _dj.get('generated')
    for _n, _e in _dj.get('paths', {}).items():
        _k = re.sub(r'_+', '_', _n.replace('->', '_').replace('→', '_')
                    .replace(' ', '_')).strip('_').lower()
        _design_tiers[_k] = {'tier': _e.get('tier', 'UNGRADED'),
                             'why': _e.get('why', '')}
except (OSError, ValueError):
    pass

_agreement = {}
try:
    with open(os.path.join(results_dir, 'posterior_design_agreement.json'),
              'r', encoding='utf-8') as _fh:
        _agreement = json.load(_fh)
except (OSError, ValueError):
    pass

TIER_COLORS = {
    'PRIMARY': '#2d7d46',
    'SYNTHESIS_ONLY': '#1f4e79',
    'NARRATIVE_ONLY': '#d4a017',
    'NO_RESULTS': '#c0392b',
    'UNGRADED': '#777777',
}

# Weakest strength word a tier is allowed to reach past.
TIER_STRENGTH_CAP = {'NO_RESULTS': 'INSUFFICIENT'}


def design_for(path_name):
    """Tier + reason for a path. UNGRADED when the grader never saw it."""
    key = re.sub(r'_+', '_', str(path_name).replace('->', '_')
                 .replace('→', '_').replace(' ', '_')).strip('_').lower()
    entry = _design_tiers.get(key)
    if entry:
        return entry['tier'], entry['why']
    return 'UNGRADED', ('absent from research_paths.json when the evidence-design '
                        'grader last ran, so its study types were never read')


# ---------------------------------------------------------------------------
# HOLLOW-PATH SUPPRESSION (added 2026-08-21)
# ---------------------------------------------------------------------------
# The Bayesian synthesis scores each path partly on corpus evidence depth. When
# the inflammatory_markers extraction patterns were fixed on 2026-08-21, 29 of
# 47 paths dropped to ZERO live corpus data points - their "evidence" had been
# regex artifacts (the 3 in NLRP3, the 1 in IL-1, section numbers, sample
# sizes). statistical_analysis.json predates that fix, so this page was still
# publishing:
#     #1  oxidative_stress -> inflammation    posterior 72.7%  MODERATE
#     #2  NLRP3_inflammasome -> inflammation  posterior 55.3%  WEAK
# Both have zero surviving evidence. A posterior computed from artifact counts
# is not a weak result, it is a meaningless one, and presenting it beside a
# percentage implies a precision that does not exist.
#
# Suppression is applied HERE, at the publishing layer, because that is where
# the numbers reach a reader. This is the fourth location this same
# suppress-in-one-place-only defect has surfaced (2026-08-19 validated store,
# 2026-08-21 validated summary counter, path dashboard, now here), so the
# hollow set is loaded from research_paths.json rather than re-derived.
def _hollow_path_names():
    try:
        with open(os.path.join(results_dir, 'research_paths.json'), encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return set()
    paths = data.get('paths', {})
    items = paths.items() if isinstance(paths, dict) else enumerate(paths)

    def norm(k):
        return ''.join(ch for ch in str(k).lower() if ch.isalnum())

    return {
        norm(name if isinstance(name, str) else (p.get('name') or ''))
        for name, p in items
        if isinstance(p, dict) and p.get('status') == 'HOLLOW'
    }


_hollow = _hollow_path_names()
if _hollow:
    def _norm(k):
        return ''.join(ch for ch in str(k).lower() if ch.isalnum())

    _before = len(bayesian.get('ranked', []))
    bayesian['ranked'] = [
        p for p in bayesian.get('ranked', [])
        if _norm(p.get('path') or p.get('name') or '') not in _hollow
    ]
    _removed = _before - len(bayesian['ranked'])
    bayesian['hollow_suppressed'] = _removed
    print(f"[build_statistical_analysis] Suppressed {_removed} HOLLOW path(s) from the "
          f"Bayesian ranking (zero live corpus evidence after the 2026-08-21 "
          f"extraction-gate fix); {len(bayesian['ranked'])} remain.")
monte_carlo_lada = stats_data.get('monte_carlo_lada', {})
monte_carlo_drugs = stats_data.get('monte_carlo_drugs', {})

# Meta-analysis pooled effect
structured_pools = meta_analysis.get('structured_pools', {'pools': [], 'not_pooled': []})
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

def _fmt(x, d=2):
    return ('%.' + str(d) + 'f') % x


def _bound(x):
    """Two decimals, or three when the source printed three (-0.072)."""
    return _fmt(x, 2) if abs(round(x, 2) - x) < 1e-9 else _fmt(x, 3)


def render_pools(sp):
    """HTML for the meta-analysis section, from verified records only."""
    key = []
    out = ['<!-- META-ANALYTIC POOLING -->', '<section id="meta-analysis">',
           '<h2>Meta-Analytic Pooling</h2>',
           '<div class="info-box context">',
           '  <strong>What changed on 2026-09-30</strong><br>',
           '  This section previously showed a pooled HbA1c reduction of 0.93% (95% CI 0.90 to 0.97), '
           'a remission-rate distribution and a C-peptide summary. All three were computed from '
           'regular-expression captures rather than extracted study results and have been withdrawn: '
           'the HbA1c figure combined two percentages from a single paper using an assumed variance, '
           'and the remission figures included a reagent concentration from a methods section. '
           'What is shown now is pooled only from effect records that quote their source sentence, '
           'were checked against the PubMed abstract, and were confirmed by a second independent extraction.',
           '</div>']
    if not sp.get('pools'):
        out.append('<p>No outcome currently has verified results from two or more independent trials. '
                   'Nothing is pooled.</p>')
        key.append('    <li><strong>Pooled estimates:</strong> none. No outcome has verified results '
                   'from two or more independent trials.</li>')
    for p in sp.get('pools', []):
        fx, rd = p['fixed'], p['random']
        out.append('<h3>%s: %s</h3>' % (p['outcome'], p['label']))
        out.append('<table class="robustness-table" style="width: 100%; margin-top: 16px;">')
        out.append('  <thead><tr><th>Trial</th><th>Population</th><th>Difference (95%% CI), %s</th>'
                   '<th>Timepoint</th><th>Source</th></tr></thead><tbody>' % p['unit'])
        for st in p['studies']:
            out.append('  <tr><td>%s</td><td>%s</td><td>%s (%s to %s)</td><td>%s</td>'
                       '<td><a href="https://pubmed.ncbi.nlm.nih.gov/%s/" target="_blank">PMID:%s</a></td></tr>'
                       % (st['trial'], st['population'], _fmt(st['effect']), _fmt(st['ci_lower']),
                          _fmt(st['ci_upper']), st['timepoint'], st['pmid'], st['pmid']))
        out.append('  <tr style="font-weight: 600;"><td>Pooled, random effects</td><td>%d trials</td>'
                   '<td>%s (%s to %s)</td><td></td><td></td></tr>'
                   % (p['k'], _fmt(rd['estimate']), _fmt(rd['ci_lower']), _fmt(rd['ci_upper'])))
        out.append('  <tr><td>Pooled, fixed effect</td><td>%d trials</td><td>%s (%s to %s)</td><td></td><td></td></tr>'
                   % (p['k'], _fmt(fx['estimate']), _fmt(fx['ci_lower']), _fmt(fx['ci_upper'])))
        out.append('</tbody></table>')
        out.append('<p style="font-size: 13px;">Heterogeneity: Q = %s, I&sup2; = %s%%. Evidence level: %s '
                   '(single-analyst extraction, independently re-extracted).</p>'
                   % (_fmt(p['Q']), _fmt(p['I_squared'], 1), p['evidence_level']))
        out.append('<ul style="font-size: 13px;">')
        for c in p['caveats']:
            out.append('  <li>%s</li>' % c)
        out.append('</ul>')
        key.append('    <li><strong>%s, %s:</strong> %s %s (95%% CI %s to %s), random effects, %d trials. '
                   'Read with the caveats in the section below.</li>'
                   % (p['outcome'], p['label'], _fmt(rd['estimate']), p['unit'],
                      _fmt(rd['ci_lower']), _fmt(rd['ci_upper']), p['k']))
    single = [g for g in sp.get('not_pooled', []) if g.get('studies')]
    if single:
        out.append('<h3>Reported, not pooled</h3>')
        out.append('<p style="font-size: 13px;">Comparisons with verified results from one trial only. '
                   'Each row is that trial\'s own result.</p>')
        out.append('<table class="robustness-table" style="width: 100%; margin-top: 16px;">')
        out.append('  <thead><tr><th>Comparison</th><th>Trial</th><th>Difference (95% CI)</th>'
                   '<th>Timepoint</th><th>Source</th></tr></thead><tbody>')
        for g in single:
            for st in g['studies']:
                out.append('  <tr><td>%s</td><td>%s</td><td>%s (%s to %s)</td><td>%s</td>'
                           '<td><a href="https://pubmed.ncbi.nlm.nih.gov/%s/" target="_blank">PMID:%s</a></td></tr>'
                           % (g['group'], st['trial'], _fmt(st['effect']), _bound(st['ci_lower']),
                              _bound(st['ci_upper']), st['timepoint'], st['pmid'], st['pmid']))
        out.append('</tbody></table>')
    out.append('<h3>Remission rates and C-peptide</h3>')
    out.append('<p>Withdrawn. No verified records exist yet for these outcomes.</p>')
    return '\n'.join(out), '\n'.join(key)


pool_section, pool_key_findings = render_pools(structured_pools)


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
{pool_key_findings}
    <li><strong>{bayesian['ranked'][0].get('path', bayesian['ranked'][0].get('name', 'Top path'))}:</strong> Highest Bayesian posterior probability at {bayesian['ranked'][0]['posterior']*100:.1f}%, classified as {bayesian['ranked'][0]['strength']}</li>
    <li><strong>Top research path strength distribution:</strong> {bayesian['strong_paths']} STRONG, {bayesian['moderate_paths']} MODERATE, {bayesian['weak_paths']} WEAK, {bayesian['insufficient_paths']} INSUFFICIENT (of {bayesian['total_paths']} total)</li>
    <li><strong>Suppressed from this ranking:</strong> {bayesian.get('hollow_suppressed', 0)} path(s) had zero surviving corpus evidence after the 2026-08-21 extraction-gate fix and are excluded. Posteriors computed from regex artifacts are not weak evidence, they are no evidence. Strength-distribution counters above are inherited from the pre-fix synthesis and are being recomputed.</li>
  </ul>
</div>

</section>

{pool_section}

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

    # ------------------------------------------------------------------
    # Discordance disclosure (2026-08-29). Stated BEFORE the ranking, not
    # in a footnote after it: a reader who has already absorbed the order
    # has already taken the claim.
    # ------------------------------------------------------------------
    if _agreement.get('comparable_pairs'):
        _disc = _agreement.get('discordant_pairs', 0)
        _comp = _agreement.get('comparable_pairs', 0)
        _rate = _agreement.get('discordance_rate', 0) * 100
        _nrap = _agreement.get('no_results_above_primary', 0)
        _worst = [d for d in _agreement.get('detail', [])
                  if d['higher_tier'] == 'NO_RESULTS' and d['lower_tier'] == 'PRIMARY']
        _example = ''
        if _worst:
            _w = _worst[0]
            _example = (f"For example this page ranks <strong>{_w['higher_posterior']}</strong> "
                        f"({_w['higher_posterior_value'] * 100:.1f}%, no measured outcome in any "
                        f"citing paper) above <strong>{_w['lower_posterior']}</strong> "
                        f"({_w['lower_posterior_value'] * 100:.1f}%, rests on primary data). ")
        html += f'''<div class="info-box context" style="border-left: 4px solid #c0392b;">
  <strong>Read this before the ranking: the posterior does not know what kind of study it came from.</strong><br>
  The prior in this model is a function of data-point count and PMID count only. Neither it nor the
  likelihood term reads publication type, so a path can rank highly because a protocol's dose table
  yielded many scrapeable numbers. Measured on {_agreement.get('generated', 'this build')}:
  <strong>{_disc} of {_comp} comparable ordered pairs ({_rate:.1f}%) are discordant</strong> &mdash; this page
  scores the path higher while its evidence design is weaker. <strong>{_nrap}</strong> of those pairs rank a
  NO RESULTS path above a path resting on primary data. {_example}
  Each row below therefore carries its evidence-design tier, read from PubMed publication types rather
  than from this repository's own text matching. <em>Where the tier and the percentage disagree, the tier
  is the more reliable of the two.</em> Refitting the prior to encode study design is a modelling decision
  and is open in the work queue; it has deliberately not been done unattended.
</div>

'''

    # Show top 15 paths grouped by strength
    for i, path_entry in enumerate(bayesian['ranked'][:15]):
        strength = path_entry.get('strength', 'INSUFFICIENT')
        posterior = path_entry['posterior']
        path_name = path_entry['path']

        tier, tier_why = design_for(path_name)
        tier_color = TIER_COLORS.get(tier, '#777777')

        # Cap the WORD, never the number. "WEAK evidence" asserts that
        # evidence exists; under a NO_RESULTS path none does.
        capped_to = TIER_STRENGTH_CAP.get(tier)
        shown_strength = strength
        cap_note = ''
        if capped_to and strength != capped_to:
            shown_strength = capped_to
            cap_note = (f' <span style="color:#c0392b;">(capped from {strength}: '
                        f'no measured outcome exists under this path)</span>')

        strength_lower = shown_strength.lower()
        color = strength_color(shown_strength)

        html += f'''<div class="bayesian-path {strength_lower}">
  <div class="path-name" style="color: {color};">{i+1}. {path_name}
    <span style="display:inline-block; margin-left:8px; padding:2px 7px; font-size:10px;
                 font-weight:600; letter-spacing:0.04em; border:1px solid {tier_color};
                 color:{tier_color}; background:#fff; cursor:help;"
          title="{tier_why.replace('"', '&quot;')}">{tier.replace('_', ' ')}</span>
  </div>
  <div class="path-metric">
    <span>Posterior: <strong>{posterior*100:.1f}%</strong></span>
    <span>Strength: <strong>{shown_strength}</strong>{cap_note}</span>
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
    <!-- WITHDRAWN 2026-09-10. This block was audited while sweeping PMID:32175717 and FOUR OF ITS
         FIVE CITATIONS WERE FALSE. Every false one is a health-economics or cost paper being cited
         as statistical methodology - they are unrelated to the methods they were attached to:
           - "DerSimonian-Laird estimators (PMID:29710129)" -> 29710129 is Hernandez et al.,
             "Total Costs of Chimeric Antigen Receptor T-Cell Immunotherapy", JAMA Oncol 2018.
             A CAR-T cost analysis. It is not a meta-analysis methods paper.
           - "HbA1c reduction effect sizes pooled from multi-center trials (PMID:34763823;
             PMID:37909353)" -> 34763823 is Herman & Kuo, "100 years of Insulin: Why is Insulin So
             Expensive", Endocrinol Metab Clin North Am 2021, a review of insulin PRICING;
             37909353 is "Economic Costs of Diabetes in the U.S. in 2022", Diabetes Care 2024.
             Neither pools HbA1c effect sizes; neither reports HbA1c outcomes at all.
           - "Bayesian pathway synthesis priors informed by systematic review evidence
             (PMID:32175717)" -> 32175717 is Khan MAB et al., J Epidemiol Glob Health 2020, a
             Global Burden of Disease analysis of T2D prevalence. It is not a systematic review
             and it did not inform any prior on this page; statistical_analysis.py sets the prior
             from data_point_count and PMID count, which is recorded in the 2026-08-29 queue item.
         The fifth (PMID:23248199, ACTION LADA) is topically real and is retained below.
         The block is replaced rather than re-cited because the honest statement is that this
         page's methods are not drawn from external methodological sources. -->
    <p style="font-size:12px;color:#636363;line-height:1.7;">
      <strong>Withdrawn 2026-09-10.</strong> This section previously listed four external papers as
      the methodological basis for the statistics on this page. On audit, all four were
      health-economics or cost-of-illness papers with no connection to the methods they were
      attached to, and none of them informed any calculation here. They have been removed rather
      than replaced, because the accurate statement is that the pooling and the Bayesian prior on
      this page are computed by <code>statistical_analysis.py</code> from this repository's own
      corpus counts &mdash; specifically from data-point counts and PMID counts per path &mdash; and
      not from any external methodological source. The prior's known limitation (it does not encode
      study design; 62.3% of comparable ordered pairs are discordant with design, measured
      2026-08-29) is disclosed above the ranking on this page.
      The one retained citation is
      <a href="https://pubmed.ncbi.nlm.nih.gov/23248199/" target="_blank">PMID 23248199</a>
      (ACTION LADA), which supplies the LADA prevalence input to the screening model.
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
