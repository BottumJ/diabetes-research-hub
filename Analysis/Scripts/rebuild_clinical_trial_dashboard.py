#!/usr/bin/env python3
"""
Rebuild Clinical Trial Intelligence Dashboard — Tufte-informed design.

Reads clinical_trials_latest.json and generates a clean, data-dense,
scientifically credible HTML dashboard following Tufte principles:
  - Light background, high data-ink ratio
  - No donut/pie charts (horizontal bars with direct labels)
  - Serif typography for headers, monospace for data
  - Muted functional color palette
  - Minimal gridlines, no chartjunk
  - Source citations on every data element
  - Phase normalization (NA/N/A → Not Applicable)

Output: Dashboards/Clinical_Trial_Dashboard.html
"""

import json
import os
from collections import Counter
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RESULTS_DIR = os.path.join(BASE_DIR, 'Analysis', 'Results')
DASH_DIR = os.path.join(BASE_DIR, 'Dashboards')

def load_trials():
    path = os.path.join(RESULTS_DIR, 'clinical_trials_latest.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def normalize_phase(phase):
    """Fix inconsistent phase naming."""
    mapping = {
        'NA': 'Not Applicable',
        'N/A': 'Not Applicable',
        'EARLY_PHASE1': 'Early Phase 1',
        'PHASE1': 'Phase 1',
        'PHASE1, PHASE2': 'Phase 1/2',
        'PHASE2': 'Phase 2',
        'PHASE2, PHASE3': 'Phase 2/3',
        'PHASE3': 'Phase 3',
        'PHASE4': 'Phase 4',
    }
    return mapping.get(phase, phase)

def normalize_status(status):
    return status.replace('_', ' ').title()

def build_compact_trials(trials):
    """Build compact trial list for embedding, with normalized fields."""
    compact = []
    for t in trials.values():
        compact.append({
            'id': t['nct_id'],
            'title': t['title'][:140],
            'status': t['status'],
            'statusLabel': normalize_status(t['status']),
            'phase': t['phase'],
            'phaseLabel': normalize_phase(t['phase']),
            'enrollment': t.get('enrollment', ''),
            'start': t.get('start_date', ''),
            'end': t.get('completion_date', ''),
            'sponsor': t.get('sponsor', '')[:60],
            'interventions': t.get('interventions', '')[:120],
            'types': t.get('intervention_types', ''),
            'conditions': t.get('conditions', '')[:100],
            'category': t.get('category', ''),
            'posted': t.get('first_posted', ''),
            'results': t.get('results_posted', ''),
        })
    return compact

def generate_dashboard(data):
    trials = data['trials']
    meta = data['metadata']
    compact = build_compact_trials(trials)
    trials_json = json.dumps(compact, separators=(',', ':'))
    generated = meta.get('generated', datetime.now().isoformat())[:10]

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Clinical Trial Intelligence — Diabetes Research Hub</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
/* === TUFTE-INFORMED DESIGN SYSTEM === */
:root {{
  --bg: #fafaf7;
  --surface: #ffffff;
  --text: #1a1a1a;
  --muted: #636363;
  --light: #999999;
  --border: #e0ddd5;
  --border-light: #eeebe3;
  --accent: #2c5f8a;
  --accent-light: #d4e2ef;
  --green: #2d7d46;
  --green-light: #d4edda;
  --amber: #8b6914;
  --amber-light: #fef3cd;
  --red: #8b2500;
  --red-light: #f5d5cc;
  --purple: #5b4a8a;
  --purple-light: #e2daf0;
  --teal: #1a7a6d;
  --teal-light: #cce8e4;
  --serif: Georgia, 'Times New Roman', serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --mono: 'SF Mono', 'Consolas', 'Monaco', monospace;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: var(--sans); background: var(--bg); color: var(--text); line-height: 1.55; font-size: 14px; }}

/* Header: restrained, informative */
.header {{ padding: 32px 40px 24px; border-bottom: 1px solid var(--border); max-width: 1300px; margin: 0 auto; }}
.header h1 {{ font-family: var(--serif); font-size: 26px; font-weight: 400; color: var(--text); letter-spacing: -0.3px; }}
.header .source {{ font-size: 12px; color: var(--muted); margin-top: 6px; }}
.header .source a {{ color: var(--accent); text-decoration: none; }}
.header .source a:hover {{ text-decoration: underline; }}

/* Key figures: dense, functional */
.key-figures {{ display: flex; gap: 32px; margin-top: 16px; flex-wrap: wrap; }}
.key-figure {{ }}
.key-figure .num {{ font-family: var(--mono); font-size: 28px; font-weight: 700; color: var(--text); line-height: 1; }}
.key-figure .label {{ font-size: 11px; color: var(--muted); margin-top: 2px; letter-spacing: 0.3px; }}

/* Tabs: minimal */
.tabs {{ display: flex; gap: 0; max-width: 1300px; margin: 0 auto; padding: 0 40px; border-bottom: 1px solid var(--border); }}
.tab {{ padding: 10px 18px; cursor: pointer; font-size: 13px; color: var(--muted); border-bottom: 2px solid transparent; transition: all 0.15s; }}
.tab:hover {{ color: var(--text); }}
.tab.active {{ color: var(--text); border-bottom-color: var(--text); font-weight: 600; }}

/* Content */
.content {{ max-width: 1300px; margin: 0 auto; padding: 24px 40px 48px; }}
.panel {{ display: none; }}
.panel.active {{ display: block; }}

/* Cards: minimal borders, maximum data */
.card {{ background: var(--surface); border: 1px solid var(--border-light); padding: 20px 24px; margin-bottom: 20px; }}
.card h3 {{ font-family: var(--serif); font-size: 15px; font-weight: 400; color: var(--text); margin-bottom: 14px; }}
.card .note {{ font-size: 11px; color: var(--light); font-style: italic; margin-top: 8px; }}

.row {{ display: grid; gap: 20px; margin-bottom: 20px; }}
.row-2 {{ grid-template-columns: 1fr 1fr; }}
.row-3 {{ grid-template-columns: 1fr 1fr 1fr; }}
@media (max-width: 900px) {{ .row-2, .row-3 {{ grid-template-columns: 1fr; }} }}

/* Chart containers */
.chart-wrap {{ position: relative; height: 280px; }}

/* Data table: clean, scannable */
.controls {{ display: flex; gap: 10px; margin-bottom: 14px; flex-wrap: wrap; align-items: center; }}
.search {{ background: var(--bg); border: 1px solid var(--border); padding: 7px 12px; font-size: 13px; color: var(--text); width: 260px; font-family: var(--sans); }}
.search:focus {{ outline: none; border-color: var(--accent); }}
.filter {{ background: var(--bg); border: 1px solid var(--border); padding: 7px 10px; font-size: 12px; color: var(--text); font-family: var(--sans); }}
.count {{ font-size: 12px; color: var(--muted); margin-left: auto; font-family: var(--mono); }}

table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; }}
thead th {{ text-align: left; padding: 8px 10px; border-bottom: 2px solid var(--text); font-size: 11px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer; white-space: nowrap; }}
thead th:hover {{ color: var(--text); }}
tbody td {{ padding: 7px 10px; border-bottom: 1px solid var(--border-light); vertical-align: top; }}
tbody tr:hover {{ background: #f5f4ef; }}

/* Links */
.nct {{ color: var(--accent); text-decoration: none; font-family: var(--mono); font-size: 11.5px; }}
.nct:hover {{ text-decoration: underline; }}

/* Tags: minimal, functional */
.tag {{ display: inline-block; padding: 1px 7px; font-size: 11px; font-weight: 500; border-radius: 2px; }}
.tag-recruiting {{ background: var(--green-light); color: var(--green); }}
.tag-completed {{ background: var(--accent-light); color: var(--accent); }}
.tag-active {{ background: var(--amber-light); color: var(--amber); }}
.tag-pending {{ background: var(--purple-light); color: var(--purple); }}
.tag-enrolling {{ background: var(--teal-light); color: var(--teal); }}
.tag-phase {{ background: #f0ede5; color: var(--muted); }}
.tag-cat {{ background: var(--bg); color: var(--muted); font-size: 10px; }}

/* Horizontal bar chart (non-canvas, pure CSS) */
.hbar {{ margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }}
.hbar .label {{ width: 160px; font-size: 12px; color: var(--text); text-align: right; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.hbar .bar {{ height: 16px; background: var(--accent); min-width: 2px; transition: width 0.3s; }}
.hbar .val {{ font-family: var(--mono); font-size: 11px; color: var(--muted); min-width: 35px; }}

/* Pagination */
.pager {{ display: flex; gap: 6px; margin-top: 14px; justify-content: center; align-items: center; }}
.pager button {{ background: var(--bg); border: 1px solid var(--border); padding: 5px 12px; font-size: 12px; color: var(--muted); cursor: pointer; }}
.pager button:hover {{ border-color: var(--accent); color: var(--accent); }}
.pager button:disabled {{ opacity: 0.3; cursor: default; }}
.pager .info {{ font-size: 12px; color: var(--muted); }}

/* Results list */
.result-item {{ padding: 8px 0; border-bottom: 1px solid var(--border-light); }}
.result-item:last-child {{ border-bottom: none; }}
.result-title {{ font-size: 13px; }}
.result-meta {{ font-size: 11.5px; color: var(--muted); margin-top: 2px; }}

/* Footer */
.footer {{ max-width: 1300px; margin: 0 auto; padding: 20px 40px; border-top: 1px solid var(--border); font-size: 11px; color: var(--light); }}
.footer a {{ color: var(--accent); text-decoration: none; }}
</style>
</head>
<body>

<div class="header">
  <h1>Clinical Trial Intelligence</h1>
  <div class="source">
    Diabetes Research Hub &middot; Data: <a href="https://clinicaltrials.gov/" target="_blank">ClinicalTrials.gov</a> API v2 &middot; Snapshot: {generated} &middot; <a href="https://osf.io/hu9ga" target="_blank">OSF Registration</a>
  </div>
  <div class="key-figures" id="keyFigures"></div>
</div>

<div class="tabs" id="tabs"></div>

<div class="content" id="content"></div>

<div class="footer">
  Source: ClinicalTrials.gov REST API v2. Trial counts reflect snapshot date and search criteria; totals may differ from site queries due to filter parameters.
  Phase "Not Applicable" includes observational studies, device trials without drug phases, and behavioral interventions.
  Enrollment figures are target enrollment as registered, not actual enrollment. &middot;
  <a href="https://github.com/BottumJ/diabetes-research-hub">GitHub</a> &middot;
  <a href="https://osf.io/hu9ga">OSF</a> &middot;
  MIT License &copy; 2026 Justin Bottum
</div>

<script>
const TRIALS = {trials_json};

// === COMPUTED DATA ===
const statusCounts = {{}};
const phaseCounts = {{}};
const categoryCounts = {{}};
const sponsorCounts = {{}};

TRIALS.forEach(t => {{
  statusCounts[t.statusLabel] = (statusCounts[t.statusLabel]||0) + 1;
  phaseCounts[t.phaseLabel] = (phaseCounts[t.phaseLabel]||0) + 1;
  categoryCounts[t.category] = (categoryCounts[t.category]||0) + 1;
  sponsorCounts[t.sponsor] = (sponsorCounts[t.sponsor]||0) + 1;
}});

const recruiting = TRIALS.filter(t => t.status === 'RECRUITING').length;
const completed = TRIALS.filter(t => t.status === 'COMPLETED').length;
const withResults = TRIALS.filter(t => t.results).length;
const totalEnrollment = TRIALS.reduce((s,t) => s + (typeof t.enrollment === 'number' ? t.enrollment : 0), 0);

// Key figures
document.getElementById('keyFigures').innerHTML = [
  {{n: TRIALS.length, l: 'Total trials'}},
  {{n: recruiting, l: 'Actively recruiting'}},
  {{n: completed, l: 'Completed'}},
  {{n: withResults, l: 'Results posted'}},
  {{n: totalEnrollment.toLocaleString(), l: 'Target enrollment'}},
].map(m => `<div class="key-figure"><div class="num">${{m.n}}</div><div class="label">${{m.l}}</div></div>`).join('');

// === TABS ===
const tabNames = ['Overview','Trial Explorer','Pipeline','Sponsors','Recent Results'];
document.getElementById('tabs').innerHTML = tabNames.map((t,i) =>
  `<div class="tab${{i===0?' active':''}}" onclick="switchTab(${{i}})">${{t}}</div>`
).join('');

function switchTab(idx) {{
  document.querySelectorAll('.tab').forEach((t,i) => t.classList.toggle('active', i===idx));
  document.querySelectorAll('.panel').forEach((p,i) => p.classList.toggle('active', i===idx));
}}

const content = document.getElementById('content');

// === HELPER: Pure CSS horizontal bar chart ===
function hbarChart(data, maxVal, color) {{
  if (!maxVal) maxVal = Math.max(...data.map(d => d[1]));
  return data.map(([label, val]) =>
    `<div class="hbar">
      <div class="label" title="${{label}}">${{label}}</div>
      <div class="bar" style="width:${{Math.max(2, (val/maxVal)*280)}}px;background:${{color||'var(--accent)'}}"></div>
      <div class="val">${{val}}</div>
    </div>`
  ).join('');
}}

// === TAB 0: OVERVIEW ===
const p0 = document.createElement('div');
p0.className = 'panel active';

// Status distribution
const statusOrder = ['Recruiting','Completed','Not Yet Recruiting','Active Not Recruiting','Enrolling By Invitation'];
const statusColors = {{'Recruiting':'var(--green)','Completed':'var(--accent)','Not Yet Recruiting':'var(--purple)','Active Not Recruiting':'var(--amber)','Enrolling By Invitation':'var(--teal)'}};
const statusBars = statusOrder.filter(s => statusCounts[s]).map(s => [s, statusCounts[s]]);

// Phase distribution
const phaseOrder = ['Early Phase 1','Phase 1','Phase 1/2','Phase 2','Phase 2/3','Phase 3','Phase 4','Not Applicable'];
const phaseBars = phaseOrder.filter(p => phaseCounts[p]).map(p => [p, phaseCounts[p]]);

// Category distribution
const catBars = Object.entries(categoryCounts).sort((a,b) => b[1]-a[1]);

p0.innerHTML = `
<div class="row row-3">
  <div class="card">
    <h3>Trials by Status</h3>
    ${{statusBars.map(([s,v]) => `<div class="hbar"><div class="label">${{s}}</div><div class="bar" style="width:${{Math.max(2,(v/statusBars[0][1])*200)}}px;background:${{statusColors[s]||'var(--accent)'}}"></div><div class="val">${{v}}</div></div>`).join('')}}
    <div class="note">Status as registered on ClinicalTrials.gov at snapshot date.</div>
  </div>
  <div class="card">
    <h3>Trials by Phase</h3>
    ${{hbarChart(phaseBars, null, 'var(--accent)')}}
    <div class="note">"Not Applicable" includes observational, device, and behavioral studies.</div>
  </div>
  <div class="card">
    <h3>Trials by Category</h3>
    ${{catBars.map(([c,v]) => `<div class="hbar"><div class="label" style="width:220px" title="${{c}}">${{c.length > 30 ? c.slice(0,28)+'\\u2026' : c}}</div><div class="bar" style="width:${{Math.max(2,(v/catBars[0][1])*160)}}px;background:var(--teal)"></div><div class="val">${{v}}</div></div>`).join('')}}
    <div class="note">Categories defined by search query grouping. Trials may match multiple queries.</div>
  </div>
</div>
<div class="card">
  <h3>Largest Actively Recruiting Trials</h3>
  <table>
    <thead><tr><th>NCT ID</th><th>Title</th><th>Phase</th><th style="text-align:right">Enrollment</th><th>Sponsor</th><th>Category</th></tr></thead>
    <tbody id="topTrials"></tbody>
  </table>
  <div class="note">Enrollment figures represent target enrollment as registered, not confirmed participants. Sorted by target enrollment descending.</div>
</div>
`;
content.appendChild(p0);

// Top recruiting
const topRecruiting = TRIALS.filter(t => t.status==='RECRUITING' && typeof t.enrollment==='number').sort((a,b) => b.enrollment - a.enrollment).slice(0,12);
document.getElementById('topTrials').innerHTML = topRecruiting.map(t => `
  <tr>
    <td><a class="nct" href="https://clinicaltrials.gov/study/${{t.id}}" target="_blank">${{t.id}}</a></td>
    <td>${{t.title}}</td>
    <td><span class="tag tag-phase">${{t.phaseLabel}}</span></td>
    <td style="text-align:right;font-family:var(--mono)">${{t.enrollment.toLocaleString()}}</td>
    <td>${{t.sponsor}}</td>
    <td><span class="tag tag-cat">${{t.category.length>25?t.category.slice(0,23)+'\\u2026':t.category}}</span></td>
  </tr>
`).join('');

// === TAB 1: TRIAL EXPLORER ===
const p1 = document.createElement('div');
p1.className = 'panel';
p1.innerHTML = `
<div class="card">
  <h3>Full Trial Database &mdash; ${{TRIALS.length}} trials</h3>
  <div class="controls">
    <input type="text" class="search" id="searchInput" placeholder="Search by title, sponsor, NCT ID\\u2026">
    <select class="filter" id="fStatus"><option value="">All statuses</option></select>
    <select class="filter" id="fCategory"><option value="">All categories</option></select>
    <select class="filter" id="fPhase"><option value="">All phases</option></select>
    <span class="count" id="resultCount"></span>
  </div>
  <table>
    <thead><tr>
      <th onclick="sortTable('id')">NCT ID</th>
      <th onclick="sortTable('title')">Title</th>
      <th onclick="sortTable('statusLabel')">Status</th>
      <th onclick="sortTable('phaseLabel')">Phase</th>
      <th onclick="sortTable('enrollment')" style="text-align:right">Enrollment</th>
      <th onclick="sortTable('sponsor')">Sponsor</th>
      <th onclick="sortTable('category')">Category</th>
    </tr></thead>
    <tbody id="explorerBody"></tbody>
  </table>
  <div class="pager" id="pager"></div>
  <div class="note">Click column headers to sort. All trials link to ClinicalTrials.gov for full details.</div>
</div>
`;
content.appendChild(p1);

// Populate filters
const allStatuses = [...new Set(TRIALS.map(t=>t.statusLabel))].sort();
const allCategories = [...new Set(TRIALS.map(t=>t.category))].sort();
const allPhases = [...new Set(TRIALS.map(t=>t.phaseLabel))].sort();
document.getElementById('fStatus').innerHTML += allStatuses.map(s => `<option value="${{s}}">${{s}}</option>`).join('');
document.getElementById('fCategory').innerHTML += allCategories.map(c => `<option value="${{c}}">${{c}}</option>`).join('');
document.getElementById('fPhase').innerHTML += allPhases.map(p => `<option value="${{p}}">${{p}}</option>`).join('');

let page = 0, pageSize = 30, sortField = 'enrollment', sortDir = -1, filtered = [...TRIALS];

function getStatusTag(s) {{
  const cls = s==='Recruiting'?'tag-recruiting':s==='Completed'?'tag-completed':(s.includes('Active')?'tag-active':(s.includes('Not Yet')?'tag-pending':'tag-enrolling'));
  return `<span class="tag ${{cls}}">${{s}}</span>`;
}}

function applyFilters() {{
  const q = document.getElementById('searchInput').value.toLowerCase();
  const fs = document.getElementById('fStatus').value;
  const fc = document.getElementById('fCategory').value;
  const fp = document.getElementById('fPhase').value;
  filtered = TRIALS.filter(t => {{
    if(fs && t.statusLabel !== fs) return false;
    if(fc && t.category !== fc) return false;
    if(fp && t.phaseLabel !== fp) return false;
    if(q && !(t.title.toLowerCase().includes(q) || t.sponsor.toLowerCase().includes(q) || t.id.toLowerCase().includes(q) || (t.interventions||'').toLowerCase().includes(q))) return false;
    return true;
  }});
  filtered.sort((a,b) => {{
    let va = a[sortField], vb = b[sortField];
    if(typeof va==='number' && typeof vb==='number') return (va-vb)*sortDir;
    return String(va||'').localeCompare(String(vb||''))*sortDir;
  }});
  page = 0;
  renderExplorer();
}}

function sortTable(f) {{ if(sortField===f) sortDir*=-1; else {{ sortField=f; sortDir=1; }} applyFilters(); }}

function renderExplorer() {{
  const start = page * pageSize;
  const rows = filtered.slice(start, start + pageSize);
  document.getElementById('resultCount').textContent = filtered.length + ' trials';
  document.getElementById('explorerBody').innerHTML = rows.map(t => `
    <tr>
      <td><a class="nct" href="https://clinicaltrials.gov/study/${{t.id}}" target="_blank">${{t.id}}</a></td>
      <td style="max-width:320px">${{t.title}}</td>
      <td>${{getStatusTag(t.statusLabel)}}</td>
      <td><span class="tag tag-phase">${{t.phaseLabel}}</span></td>
      <td style="text-align:right;font-family:var(--mono)">${{typeof t.enrollment==='number'?t.enrollment.toLocaleString():'\\u2014'}}</td>
      <td style="max-width:180px">${{t.sponsor}}</td>
      <td><span class="tag tag-cat">${{t.category.length>25?t.category.slice(0,23)+'\\u2026':t.category}}</span></td>
    </tr>
  `).join('');
  const tp = Math.ceil(filtered.length / pageSize);
  document.getElementById('pager').innerHTML = `
    <button onclick="goPage(${{page-1}})" ${{page===0?'disabled':''}}>\\u2190 Prev</button>
    <span class="info">Page ${{page+1}} of ${{tp}}</span>
    <button onclick="goPage(${{page+1}})" ${{page>=tp-1?'disabled':''}}>Next \\u2192</button>
  `;
}}

window.goPage = function(p) {{ page = p; renderExplorer(); }};
['searchInput','fStatus','fCategory','fPhase'].forEach(id => {{
  document.getElementById(id).addEventListener(id==='searchInput'?'input':'change', applyFilters);
}});
applyFilters();

// === TAB 2: PIPELINE ===
const p2 = document.createElement('div');
p2.className = 'panel';

// T1D pipeline
const t1d = TRIALS.filter(t => t.category.includes('T1D'));
const t1dPhase = {{}};
t1d.forEach(t => {{ t1dPhase[t.phaseLabel] = (t1dPhase[t.phaseLabel]||0)+1; }});
const t1dBars = phaseOrder.filter(p => t1dPhase[p]).map(p => [p, t1dPhase[p]]);

// T2D pipeline
const t2d = TRIALS.filter(t => t.category.includes('T2D'));
const t2dPhase = {{}};
t2d.forEach(t => {{ t2dPhase[t.phaseLabel] = (t2dPhase[t.phaseLabel]||0)+1; }});
const t2dBars = phaseOrder.filter(p => t2dPhase[p]).map(p => [p, t2dPhase[p]]);

// Intervention types
const intvCounts = {{}};
TRIALS.forEach(t => {{
  (t.types||'').split(';').map(s=>s.trim()).filter(Boolean).forEach(type => {{
    intvCounts[type] = (intvCounts[type]||0)+1;
  }});
}});
const intvBars = Object.entries(intvCounts).sort((a,b) => b[1]-a[1]);

const phase3 = TRIALS.filter(t => t.phaseLabel.includes('Phase 3'));
const bigTrials = TRIALS.filter(t => typeof t.enrollment==='number' && t.enrollment >= 1000);

p2.innerHTML = `
<div class="row row-2">
  <div class="card">
    <h3>T1D Pipeline by Phase (${{t1d.length}} trials)</h3>
    ${{hbarChart(t1dBars, null, 'var(--green)')}}
    <div class="note">Includes T1D Cure & Cell Therapy (${{categoryCounts['T1D Cure & Cell Therapy']||0}}) and T1D Immunotherapy & Prevention (${{categoryCounts['T1D Immunotherapy & Prevention']||0}}) categories.</div>
  </div>
  <div class="card">
    <h3>T2D Novel Therapies by Phase (${{t2d.length}} trials)</h3>
    ${{hbarChart(t2dBars, null, 'var(--amber)')}}
    <div class="note">Phase 2\\u20133 novel therapies only. Does not include standard-of-care or device trials.</div>
  </div>
</div>
<div class="row row-2">
  <div class="card">
    <h3>Intervention Types</h3>
    ${{hbarChart(intvBars, null, 'var(--teal)')}}
    <div class="note">Trials may have multiple intervention types. "Other" includes behavioral, dietary, and educational interventions.</div>
  </div>
  <div class="card">
    <h3>Pipeline Summary</h3>
    <div style="font-size:13px;line-height:2;">
      <div><strong style="font-family:var(--mono)">${{recruiting}}</strong> <span style="color:var(--muted)">trials actively recruiting participants</span></div>
      <div><strong style="font-family:var(--mono)">${{phase3.length}}</strong> <span style="color:var(--muted)">Phase 3 trials (closest to regulatory decision)</span></div>
      <div><strong style="font-family:var(--mono)">${{bigTrials.length}}</strong> <span style="color:var(--muted)">large-scale trials (1,000+ target enrollment)</span></div>
      <div><strong style="font-family:var(--mono)">${{withResults}}</strong> <span style="color:var(--muted)">trials with posted results available for analysis</span></div>
      <div><strong style="font-family:var(--mono)">${{categoryCounts['Diabetes Technology (Devices)']||0}}</strong> <span style="color:var(--muted)">device/technology trials (CGM, pumps, AI-assisted)</span></div>
    </div>
    <div class="note">All figures from ClinicalTrials.gov snapshot. Phase counts use registered phase; some trials may advance between snapshot dates.</div>
  </div>
</div>
`;
content.appendChild(p2);

// === TAB 3: SPONSORS ===
const p3 = document.createElement('div');
p3.className = 'panel';

const topSponsors = Object.entries(sponsorCounts).sort((a,b) => b[1]-a[1]).slice(0,20);

// Classify sponsors
const industryKw = ['Inc','Corp','Ltd','LLC','Company','A/S','GmbH','S.A','Sanofi','Pfizer','AstraZeneca','Lilly','Novo Nordisk','Medtronic','Insulet','Tandem','Dexcom','Abbott','Roche','Boehringer','Bayer','Merck','Amgen','Vertex','Beta Bionics'];
const govKw = ['NIH','NIDDK','VA ','Veterans','CDC','FDA','Department','Ministry','NIHR'];

let industry=0, academic=0, govt=0, other=0;
Object.entries(sponsorCounts).forEach(([name,count]) => {{
  if(industryKw.some(k => name.includes(k))) industry += count;
  else if(govKw.some(k => name.includes(k))) govt += count;
  else if(name.includes('University')||name.includes('Hospital')||name.includes('Medical Center')||name.includes('Centre')||name.includes('Institute')||name.includes('Clinic')) academic += count;
  else other += count;
}});

const sponsorTypeBars = [['Academic/Medical Center', academic],['Industry', industry],['Other', other],['Government', govt]].sort((a,b) => b[1]-a[1]);

p3.innerHTML = `
<div class="row row-2">
  <div class="card">
    <h3>Top 20 Sponsors</h3>
    ${{topSponsors.map(([name,count]) => `<div class="hbar"><div class="label" title="${{name}}">${{name.length>28?name.slice(0,26)+'\\u2026':name}}</div><div class="bar" style="width:${{Math.max(2,(count/topSponsors[0][1])*200)}}px;background:var(--accent)"></div><div class="val">${{count}}</div></div>`).join('')}}
    <div class="note">Sponsor as registered on ClinicalTrials.gov. Lead sponsor only; does not reflect collaborators.</div>
  </div>
  <div class="card">
    <h3>Sponsor Type Distribution</h3>
    ${{hbarChart(sponsorTypeBars, null, 'var(--purple)')}}
    <div class="note">Classification based on keyword matching of sponsor names. "Other" includes non-profits, foundations, and unclassified entities. Classification is approximate.</div>
  </div>
</div>
`;
content.appendChild(p3);

// === TAB 4: RECENT RESULTS ===
const p4 = document.createElement('div');
p4.className = 'panel';
p4.innerHTML = `
<div class="card">
  <h3>Recently Posted Results</h3>
  <div id="recentResults"></div>
  <div class="note">Results posted dates from ClinicalTrials.gov. Click NCT ID for full results including outcome measures, adverse events, and statistical analyses.</div>
</div>
`;
content.appendChild(p4);

const recent = TRIALS.filter(t => t.results).sort((a,b) => (b.results||'').localeCompare(a.results||'')).slice(0,30);
document.getElementById('recentResults').innerHTML = recent.map(t => `
  <div class="result-item">
    <div class="result-title">
      <a class="nct" href="https://clinicaltrials.gov/study/${{t.id}}" target="_blank">${{t.id}}</a> &mdash; ${{t.title}}
    </div>
    <div class="result-meta">
      Results posted: <strong>${{t.results}}</strong> &middot; ${{t.sponsor}} &middot; ${{t.phaseLabel}}
      ${{t.interventions ? ' &middot; '+t.interventions : ''}}
    </div>
  </div>
`).join('');
</script>
</body>
</html>'''
    return html

def main():
    print("Loading clinical trial data...")
    data = load_trials()
    total = data['metadata']['total_trials']
    print(f"  {total} trials loaded")

    print("Generating Tufte-style dashboard...")
    html = generate_dashboard(data)

    os.makedirs(DASH_DIR, exist_ok=True)
    out_path = os.path.join(DASH_DIR, 'Clinical_Trial_Dashboard.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"  Dashboard written: {out_path} ({size_kb:.0f} KB)")
    print("Done.")

if __name__ == '__main__':
    main()
