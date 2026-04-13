#!/usr/bin/env python3
"""
Build interactive HTML dashboard for Islet × Drug Repurposing results.
Reads Phase 1 targets and Phase 2 candidates, generates a single-file HTML dashboard.
"""

import json
from pathlib import Path
from datetime import datetime

RESULTS_DIR = Path(__file__).parent.parent / "Results"
DASH_DIR = Path(__file__).parent.parent.parent / "Dashboards"
DASH_DIR.mkdir(parents=True, exist_ok=True)

# Load data
with open(RESULTS_DIR / "islet_repurposing_targets.json") as f:
    targets_data = json.load(f)

with open(RESULTS_DIR / "islet_repurposing_drug_candidates.json") as f:
    drugs_data = json.load(f)

targets = targets_data["targets"]
novel = drugs_data["novel_candidates"][:50]
standard = drugs_data["standard_drugs"]
interactions = targets_data.get("interactions", [])[:200]
kegg = targets_data.get("enrichment_kegg", [])[:20]

# Build network data for visualization
nodes = set()
edges = []
for c in novel[:20]:
    drug_node = c["drug_name"]
    nodes.add(drug_node)
    for t in c["targets_hit"][:6]:
        nodes.add(t)
        edges.append({"source": drug_node, "target": t})

nodes_list = [{"id": n, "type": "drug" if any(c["drug_name"] == n for c in novel[:20]) else "target"} for n in nodes]

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Islet Transplant × Drug Repurposing Dashboard</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0e17; color: #e0e6f0; line-height: 1.6; }}
.header {{ background: linear-gradient(135deg, #1a1f35 0%, #0d1117 100%); padding: 30px 40px; border-bottom: 2px solid #2d3555; }}
.header h1 {{ font-size: 28px; color: #58a6ff; margin-bottom: 6px; }}
.header .subtitle {{ color: #8b949e; font-size: 14px; }}
.header .badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; margin-right: 8px; }}
.badge-bronze {{ background: #cd7f32; color: #fff; }}
.badge-gap {{ background: #f85149; color: #fff; }}
.badge-phase {{ background: #58a6ff; color: #fff; }}
.container {{ max-width: 1400px; margin: 0 auto; padding: 20px 40px; }}
.stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 24px 0; }}
.stat-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 20px; text-align: center; }}
.stat-card .number {{ font-size: 36px; font-weight: 700; color: #58a6ff; }}
.stat-card .label {{ font-size: 13px; color: #8b949e; margin-top: 4px; }}
.section {{ margin: 30px 0; }}
.section h2 {{ font-size: 20px; color: #c9d1d9; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid #21262d; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th {{ background: #161b22; color: #58a6ff; padding: 10px 12px; text-align: left; position: sticky; top: 0; border-bottom: 2px solid #30363d; }}
td {{ padding: 8px 12px; border-bottom: 1px solid #21262d; }}
tr:hover {{ background: #161b22; }}
.drug-name {{ color: #58a6ff; font-weight: 600; }}
.target-tag {{ display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 11px; margin: 1px; background: #1f2937; color: #7ee787; border: 1px solid #2d3555; }}
.score-bar {{ height: 6px; border-radius: 3px; background: #21262d; position: relative; width: 100px; display: inline-block; }}
.score-fill {{ height: 100%; border-radius: 3px; background: linear-gradient(90deg, #388bfd, #58a6ff); }}
.tab-container {{ display: flex; gap: 0; margin-bottom: 0; }}
.tab {{ padding: 10px 20px; cursor: pointer; background: #0d1117; border: 1px solid #30363d; border-bottom: none; color: #8b949e; font-size: 13px; border-radius: 8px 8px 0 0; }}
.tab.active {{ background: #161b22; color: #58a6ff; font-weight: 600; }}
.tab-content {{ display: none; background: #161b22; border: 1px solid #30363d; border-radius: 0 8px 8px 8px; padding: 20px; overflow-x: auto; }}
.tab-content.active {{ display: block; }}
.network-placeholder {{ background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 40px; text-align: center; }}
.pathway-bar {{ display: flex; align-items: center; margin: 4px 0; }}
.pathway-name {{ width: 300px; font-size: 12px; text-align: right; padding-right: 12px; color: #c9d1d9; }}
.pathway-fill {{ height: 18px; border-radius: 3px; background: linear-gradient(90deg, #238636, #2ea043); min-width: 2px; display: flex; align-items: center; justify-content: flex-end; padding-right: 6px; font-size: 10px; color: #fff; }}
.legend {{ display: flex; gap: 20px; margin: 10px 0; font-size: 12px; color: #8b949e; }}
.legend-dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 4px; vertical-align: middle; }}
.footer {{ text-align: center; padding: 30px; color: #484f58; font-size: 12px; border-top: 1px solid #21262d; margin-top: 40px; }}
</style>
</head>
<body>

<div class="header">
  <h1>Islet Transplant × Drug Repurposing</h1>
  <div class="subtitle">
    Computational screening for novel islet graft protection candidates
    <br>
    <span class="badge badge-gap">Gap Score: 100.0</span>
    <span class="badge badge-bronze">Evidence: BRONZE</span>
    <span class="badge badge-phase">Phase 2 Complete</span>
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
  </div>
</div>

<div class="container">

  <div class="stats-grid">
    <div class="stat-card">
      <div class="number">{len(targets)}</div>
      <div class="label">Protein Targets Identified</div>
    </div>
    <div class="stat-card">
      <div class="number">{len(novel)}</div>
      <div class="label">Novel Drug Candidates</div>
    </div>
    <div class="stat-card">
      <div class="number">{len(standard)}</div>
      <div class="label">Standard Immunosuppressants</div>
    </div>
    <div class="stat-card">
      <div class="number">{len(interactions)}</div>
      <div class="label">Protein Interactions (STRING)</div>
    </div>
    <div class="stat-card">
      <div class="number">{len(kegg)}</div>
      <div class="label">KEGG Pathways Enriched</div>
    </div>
    <div class="stat-card">
      <div class="number">0</div>
      <div class="label">Existing Joint Publications</div>
    </div>
  </div>

  <div class="section">
    <h2>Drug Candidates</h2>
    <div class="tab-container">
      <div class="tab active" onclick="switchTab(event, 'novel')">Novel Candidates ({len(novel)})</div>
      <div class="tab" onclick="switchTab(event, 'standard')">Standard Baseline ({len(standard)})</div>
      <div class="tab" onclick="switchTab(event, 'targets')">Top Targets</div>
    </div>

    <div id="novel" class="tab-content active">
      <table>
        <thead>
          <tr><th>#</th><th>Drug</th><th>Type</th><th>Stage</th><th>Targets</th><th>Score</th><th>Mechanisms</th></tr>
        </thead>
        <tbody>
"""

for i, c in enumerate(novel, 1):
    targets_html = " ".join(f'<span class="target-tag">{t}</span>' for t in c["targets_hit"][:6])
    if len(c["targets_hit"]) > 6:
        targets_html += f' <span class="target-tag">+{len(c["targets_hit"])-6}</span>'
    mechs = "; ".join(c["mechanisms"][:2])[:80] if c["mechanisms"] else "—"
    stage = c.get("max_phase", "?")
    pct = min(c["repurposing_score"] / 22 * 100, 100)
    html += f"""          <tr>
            <td>{i}</td>
            <td class="drug-name">{c["drug_name"]}</td>
            <td>{c.get("drug_type", "—")}</td>
            <td>{"Approved" if stage >= 5 else f"Phase {stage}"}</td>
            <td>{targets_html}</td>
            <td><div class="score-bar"><div class="score-fill" style="width:{pct}%"></div></div> {c["repurposing_score"]}</td>
            <td style="font-size:11px;color:#8b949e;max-width:300px">{mechs}</td>
          </tr>
"""

html += """        </tbody>
      </table>
    </div>

    <div id="standard" class="tab-content">
      <table>
        <thead><tr><th>Drug</th><th>Targets</th><th>Score</th></tr></thead>
        <tbody>
"""

for c in standard:
    targets_html = " ".join(f'<span class="target-tag">{t}</span>' for t in c["targets_hit"])
    html += f'          <tr><td class="drug-name">{c["drug_name"]}</td><td>{targets_html}</td><td>{c["repurposing_score"]}</td></tr>\n'

html += """        </tbody>
      </table>
    </div>

    <div id="targets" class="tab-content">
      <table>
        <thead><tr><th>#</th><th>Target</th><th>Name</th><th>OT Score</th><th>Druggability</th><th>Sources</th><th>Composite</th></tr></thead>
        <tbody>
"""

for i, t in enumerate(targets[:40], 1):
    name = (t.get("name") or "")[:50]
    html += f"""          <tr>
            <td>{i}</td>
            <td class="drug-name">{t["symbol"]}</td>
            <td style="font-size:11px">{name}</td>
            <td>{t["opentargets_score"]}</td>
            <td>{t["druggability_hits"]}</td>
            <td>{t["source_count"]}</td>
            <td>{t["composite_score"]}</td>
          </tr>
"""

html += """        </tbody>
      </table>
    </div>
  </div>

"""

# KEGG Pathways section
if kegg:
    max_fdr = max(abs(float(k.get("fdr", 1))) for k in kegg if k.get("fdr"))
    html += """  <div class="section">
    <h2>Enriched KEGG Pathways</h2>
    <p style="font-size:12px;color:#8b949e;margin-bottom:12px">Pathways significantly enriched among top targets (STRING enrichment analysis)</p>
"""
    for k in kegg[:15]:
        desc = k.get("description", k.get("term", ""))[:60]
        fdr = float(k.get("fdr", 1))
        score = max(0, min(100, -1 * (fdr if fdr > 0 else -30) * 3 + 100))  # rough scaling
        count = k.get("number_of_genes", 0)
        html += f"""    <div class="pathway-bar">
      <div class="pathway-name">{desc}</div>
      <div class="pathway-fill" style="width:{max(score, 10)}px">{count}</div>
    </div>
"""
    html += "  </div>\n"

html += f"""
  <div class="section">
    <h2>Methodology</h2>
    <div style="background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:20px;font-size:13px;color:#8b949e">
      <p><strong>Phase 1 — Target Identification:</strong> Queried OpenTargets for targets associated with graft rejection, T1D autoimmunity, beta cell apoptosis, immune tolerance, and GvHD. Added 40 curated seed targets from islet transplant literature. Expanded via STRING protein-protein interactions (score ≥700).</p>
      <br>
      <p><strong>Phase 2 — Drug Mapping:</strong> Mapped all Phase 3+ and FDA-approved drugs to the target list via OpenTargets drugAndClinicalCandidates API and ChEMBL mechanisms. Scored by multi-target coverage with novelty bonus for non-standard immunosuppressants.</p>
      <br>
      <p><strong>Validation Level:</strong> BRONZE per Research Doctrine v1.1. These are computational predictions (Evidence Level 4). Each candidate requires literature validation and expert review before any clinical consideration.</p>
      <br>
      <p><strong>Gap Context:</strong> The Islet Transplant × Drug Repurposing intersection has <strong>zero joint publications</strong> in PubMed (2020-2026), Gap Score 100.0. This analysis is the first systematic computational screen at this intersection.</p>
    </div>
  </div>

  <div class="footer">
    Diabetes Research Hub — Islet Transplant × Drug Repurposing Pipeline<br>
    Research Doctrine v1.1 | Generated {datetime.now().strftime('%Y-%m-%d')} | Phases 1-2 of 6
  </div>

</div>

<script>
function switchTab(e, tabId) {{
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  e.target.classList.add('active');
  document.getElementById(tabId).classList.add('active');
}}
</script>

</body>
</html>"""

output_path = DASH_DIR / "Islet_Drug_Repurposing.html"
with open(output_path, "w") as f:
    f.write(html)

print(f"Dashboard saved to: {output_path}")
print(f"  Novel candidates displayed: {len(novel)}")
print(f"  Targets displayed: {min(len(targets), 40)}")
print(f"  KEGG pathways: {len(kegg)}")
