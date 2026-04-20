#!/usr/bin/env python3
"""
Build interactive HTML dashboard for Islet × Drug Repurposing results.
v2: Includes Phase 3 network pharmacology analysis, validation tiers, and combination predictions.
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

with open(RESULTS_DIR / "islet_repurposing_network_analysis.json") as f:
    network_data = json.load(f)

targets = targets_data["targets"]
novel = drugs_data["novel_candidates"][:50]
standard = drugs_data["standard_drugs"]
interactions = targets_data.get("interactions", [])[:200]
kegg = targets_data.get("enrichment_kegg", [])[:20]

# Network analysis data
hub_targets = network_data.get("network_metrics", {}).get("top_hub_targets", [])
drug_np_scores = network_data.get("network_metrics", {}).get("drug_pharmacology_scores", [])
combos = network_data.get("combination_predictions", [])
validation_status = network_data.get("validation_status", {})
pathway_defs = network_data.get("pathway_analysis", {}).get("pathway_definitions", {})
string_enrichment = network_data.get("string_enrichment", {})
string_interactions = network_data.get("string_interactions", [])

# Build validation lookup
def get_validation(drug_name):
    v = validation_status.get(drug_name, {})
    return v.get("tier", 0), v.get("status", "UNRANKED"), v.get("note", "")

# NP score lookup
np_lookup = {d["drug"]: d for d in drug_np_scores}

date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
date_short = datetime.now().strftime('%Y-%m-%d')

# Tier badge colors
TIER_COLORS = {
    1: ("#238636", "Tier 1"),
    2: ("#d29922", "Tier 2"),
    3: ("#8b949e", "Tier 3"),
    -1: ("#f85149", "CONTRA"),
    0: ("#30363d", "—"),
}

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Islet Transplant × Drug Repurposing Dashboard v2</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0e17; color: #e0e6f0; line-height: 1.6; }}
.header {{ background: linear-gradient(135deg, #1a1f35 0%, #0d1117 100%); padding: 30px 40px; border-bottom: 2px solid #2d3555; }}
.header h1 {{ font-size: 28px; color: #58a6ff; margin-bottom: 6px; }}
.header .subtitle {{ color: #8b949e; font-size: 14px; }}
.badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; margin-right: 8px; }}
.badge-silver {{ background: #c0c0c0; color: #000; }}
.badge-gap {{ background: #f85149; color: #fff; }}
.badge-phase {{ background: #58a6ff; color: #fff; }}
.badge-combo {{ background: #a371f7; color: #fff; }}
.container {{ max-width: 1500px; margin: 0 auto; padding: 20px 40px; }}
.stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin: 24px 0; }}
.stat-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 18px; text-align: center; }}
.stat-card .number {{ font-size: 32px; font-weight: 700; color: #58a6ff; }}
.stat-card .label {{ font-size: 12px; color: #8b949e; margin-top: 4px; }}
.section {{ margin: 30px 0; }}
.section h2 {{ font-size: 20px; color: #c9d1d9; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid #21262d; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th {{ background: #161b22; color: #58a6ff; padding: 10px 12px; text-align: left; position: sticky; top: 0; border-bottom: 2px solid #30363d; cursor: pointer; }}
th:hover {{ color: #79c0ff; }}
td {{ padding: 8px 12px; border-bottom: 1px solid #21262d; }}
tr:hover {{ background: #161b22; }}
.drug-name {{ color: #58a6ff; font-weight: 600; }}
.target-tag {{ display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 11px; margin: 1px; background: #1f2937; color: #7ee787; border: 1px solid #2d3555; }}
.tier-badge {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 700; color: #fff; }}
.score-bar {{ height: 6px; border-radius: 3px; background: #21262d; position: relative; width: 100px; display: inline-block; }}
.score-fill {{ height: 100%; border-radius: 3px; }}
.tab-container {{ display: flex; gap: 0; margin-bottom: 0; flex-wrap: wrap; }}
.tab {{ padding: 10px 18px; cursor: pointer; background: #0d1117; border: 1px solid #30363d; border-bottom: none; color: #8b949e; font-size: 13px; border-radius: 8px 8px 0 0; }}
.tab.active {{ background: #161b22; color: #58a6ff; font-weight: 600; }}
.tab-content {{ display: none; background: #161b22; border: 1px solid #30363d; border-radius: 0 8px 8px 8px; padding: 20px; overflow-x: auto; }}
.tab-content.active {{ display: block; }}
.pathway-bar {{ display: flex; align-items: center; margin: 4px 0; }}
.pathway-name {{ width: 300px; font-size: 12px; text-align: right; padding-right: 12px; color: #c9d1d9; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.pathway-fill {{ height: 18px; border-radius: 3px; min-width: 2px; display: flex; align-items: center; justify-content: flex-end; padding-right: 6px; font-size: 10px; color: #fff; }}
.combo-card {{ background: #0d1117; border: 1px solid #30363d; border-radius: 10px; padding: 18px; margin: 12px 0; }}
.combo-card h3 {{ font-size: 15px; color: #a371f7; margin-bottom: 8px; }}
.combo-detail {{ font-size: 12px; color: #8b949e; }}
.combo-score {{ font-size: 24px; font-weight: 700; color: #a371f7; float: right; }}
.interaction-edge {{ font-size: 12px; color: #8b949e; padding: 4px 0; }}
.interaction-edge strong {{ color: #58a6ff; }}
.filter-bar {{ margin: 12px 0; display: flex; gap: 10px; align-items: center; }}
.filter-bar label {{ font-size: 12px; color: #8b949e; }}
.filter-bar select, .filter-bar input {{ background: #0d1117; color: #e0e6f0; border: 1px solid #30363d; padding: 6px 10px; border-radius: 6px; font-size: 12px; }}
.footer {{ text-align: center; padding: 30px; color: #484f58; font-size: 12px; border-top: 1px solid #21262d; margin-top: 40px; }}
</style>
</head>
<body>

<div class="header">
  <h1>Islet Transplant &times; Drug Repurposing</h1>
  <div class="subtitle">
    Network pharmacology analysis for novel islet graft protection candidates
    <br>
    <span class="badge badge-gap">Gap Score: 100.0</span>
    <span class="badge badge-silver">Evidence: SILVER</span>
    <span class="badge badge-phase">Phase 3 Complete</span>
    <span class="badge badge-combo">{len(combos)} Combinations Predicted</span>
    &nbsp; Generated: {date_str}
  </div>
</div>

<div class="container">

  <div class="stats-grid">
    <div class="stat-card">
      <div class="number">{len(targets)}</div>
      <div class="label">Protein Targets</div>
    </div>
    <div class="stat-card">
      <div class="number">{drugs_data['metadata']['total_drugs_found']}</div>
      <div class="label">Total Drug Candidates</div>
    </div>
    <div class="stat-card">
      <div class="number">{len(hub_targets)}</div>
      <div class="label">Hub Targets</div>
    </div>
    <div class="stat-card">
      <div class="number">{len(string_interactions)}</div>
      <div class="label">PPI Interactions</div>
    </div>
    <div class="stat-card">
      <div class="number">{sum(1 for v in validation_status.values() if v.get('tier', 0) in [1, 2])}</div>
      <div class="label">Validated Candidates</div>
    </div>
    <div class="stat-card">
      <div class="number">{sum(1 for v in validation_status.values() if v.get('tier', 0) == -1)}</div>
      <div class="label">Contraindicated</div>
    </div>
    <div class="stat-card">
      <div class="number">{len(combos)}</div>
      <div class="label">Combination Predictions</div>
    </div>
    <div class="stat-card">
      <div class="number">0</div>
      <div class="label">Joint Publications</div>
    </div>
  </div>

  <div class="section">
    <h2>Analysis Pipeline</h2>
    <div class="tab-container">
      <div class="tab active" onclick="switchTab(event, 'candidates')">Drug Candidates</div>
      <div class="tab" onclick="switchTab(event, 'network')">Network Pharmacology</div>
      <div class="tab" onclick="switchTab(event, 'hubs')">Hub Targets</div>
      <div class="tab" onclick="switchTab(event, 'combos')">Combinations</div>
      <div class="tab" onclick="switchTab(event, 'ppi')">Protein Interactions</div>
      <div class="tab" onclick="switchTab(event, 'enrichment')">Pathway Enrichment</div>
    </div>

    <!-- ═══ CANDIDATES TAB ═══ -->
    <div id="candidates" class="tab-content active">
      <div class="filter-bar">
        <label>Filter by tier:</label>
        <select id="tierFilter" onchange="filterCandidates()">
          <option value="all">All</option>
          <option value="1">Tier 1 (Clinical Translation)</option>
          <option value="2">Tier 2 (Validated with Caveats)</option>
          <option value="3">Tier 3 (Preclinical)</option>
          <option value="0">Unranked</option>
        </select>
        <label>Search:</label>
        <input type="text" id="drugSearch" oninput="filterCandidates()" placeholder="Drug name...">
      </div>
      <table id="candidateTable">
        <thead>
          <tr>
            <th onclick="sortTable('candidateTable', 0)">#</th>
            <th onclick="sortTable('candidateTable', 1)">Drug</th>
            <th>Tier</th>
            <th onclick="sortTable('candidateTable', 3)">Phase 2 Score</th>
            <th onclick="sortTable('candidateTable', 4)">NP Score</th>
            <th>Pathways</th>
            <th>Targets</th>
            <th>Validation Note</th>
          </tr>
        </thead>
        <tbody>
"""

# Build candidate rows — merge novel candidates with NP scores
for i, c in enumerate(novel, 1):
    name = c["drug_name"]
    tier, status, note = get_validation(name)
    np_data = np_lookup.get(name, {})
    np_score = np_data.get("network_pharmacology_score", 0)
    pathways = np_data.get("pathways_covered", [])
    beneficial = np_data.get("beneficial_pathways", 0)
    risky = np_data.get("risky_pathways", 0)

    tier_color, tier_label = TIER_COLORS.get(tier, ("#30363d", "—"))
    targets_html = " ".join(f'<span class="target-tag">{t}</span>' for t in c["targets_hit"][:6])
    if len(c["targets_hit"]) > 6:
        targets_html += f' <span class="target-tag">+{len(c["targets_hit"])-6}</span>'

    pw_html = f'{len(pathways)} ({beneficial}✓ {risky}✗)' if pathways else "—"
    score_pct = min(c["repurposing_score"] / 22 * 100, 100)
    np_pct = min(np_score / 30 * 100, 100)

    row_class = f'data-tier="{tier}" data-name="{name.lower()}"'

    html += f"""          <tr {row_class}>
            <td>{i}</td>
            <td class="drug-name">{name}</td>
            <td><span class="tier-badge" style="background:{tier_color}">{tier_label}</span></td>
            <td><div class="score-bar"><div class="score-fill" style="width:{score_pct}%;background:linear-gradient(90deg,#388bfd,#58a6ff)"></div></div> {c["repurposing_score"]}</td>
            <td><div class="score-bar"><div class="score-fill" style="width:{np_pct}%;background:linear-gradient(90deg,#a371f7,#d2a8ff)"></div></div> {np_score:.1f}</td>
            <td>{pw_html}</td>
            <td>{targets_html}</td>
            <td style="font-size:11px;color:#8b949e;max-width:250px">{note[:60] if note else status}</td>
          </tr>
"""

html += """        </tbody>
      </table>
    </div>

    <!-- ═══ NETWORK PHARMACOLOGY TAB ═══ -->
    <div id="network" class="tab-content">
      <h3 style="color:#a371f7;margin-bottom:12px">Drug × Pathway Coverage Matrix</h3>
      <p style="font-size:12px;color:#8b949e;margin-bottom:16px">Each drug mapped to 6 islet-relevant biological processes. ✓ = beneficial pathway, ⚠ = risky pathway.</p>
      <table>
        <thead>
          <tr>
            <th>Drug</th>
            <th>Tier</th>
            <th>Immune Rejection</th>
            <th>Beta Cell Survival</th>
            <th>Inflammation</th>
            <th>Angiogenesis</th>
            <th>Fibrosis</th>
            <th>Oncogenic</th>
            <th>NP Score</th>
          </tr>
        </thead>
        <tbody>
"""

pathway_keys = ["immune_rejection", "beta_cell_survival", "inflammation_cytokine",
                "angiogenesis_revascularization", "fibrosis_remodeling", "oncogenic_proliferation"]
pw_colors = {"immune_rejection": "#238636", "beta_cell_survival": "#238636",
             "inflammation_cytokine": "#238636", "angiogenesis_revascularization": "#d29922",
             "fibrosis_remodeling": "#d29922", "oncogenic_proliferation": "#f85149"}

for d in drug_np_scores[:30]:
    name = d["drug"]
    tier = d.get("validation", {}).get("tier", 0)
    tier_color, tier_label = TIER_COLORS.get(tier, ("#30363d", "—"))
    pathways = d.get("pathways_covered", [])
    np_score = d.get("network_pharmacology_score", 0)

    html += f'          <tr><td class="drug-name">{name}</td>'
    html += f'<td><span class="tier-badge" style="background:{tier_color}">{tier_label}</span></td>'

    for pk in pathway_keys:
        if pk in pathways:
            c = pw_colors[pk]
            symbol = "⚠" if pk == "oncogenic_proliferation" else "✓"
            html += f'<td style="text-align:center;color:{c};font-weight:700">{symbol}</td>'
        else:
            html += '<td style="text-align:center;color:#30363d">—</td>'

    html += f'<td style="font-weight:600;color:#a371f7">{np_score:.1f}</td></tr>\n'

html += """        </tbody>
      </table>
    </div>

    <!-- ═══ HUB TARGETS TAB ═══ -->
    <div id="hubs" class="tab-content">
      <h3 style="color:#7ee787;margin-bottom:12px">Network Hub Targets</h3>
      <p style="font-size:12px;color:#8b949e;margin-bottom:16px">Proteins targeted by the most drug candidates. Higher hub score = more robust therapeutic axis.</p>
      <table>
        <thead>
          <tr><th>#</th><th>Target</th><th>Drug Degree</th><th>Pathways</th><th>Hub Score</th><th>Key Drugs</th></tr>
        </thead>
        <tbody>
"""

for i, ht in enumerate(hub_targets[:20], 1):
    target = ht["target"]
    degree = ht["degree"]
    pw_count = ht["pathway_membership"]
    hub_score = ht["hub_score"]
    drugs_list = ", ".join(ht.get("drugs", [])[:5])
    hub_pct = min(hub_score / 75 * 100, 100)

    html += f"""          <tr>
            <td>{i}</td>
            <td class="drug-name">{target}</td>
            <td>{degree}</td>
            <td>{pw_count}</td>
            <td><div class="score-bar"><div class="score-fill" style="width:{hub_pct}%;background:linear-gradient(90deg,#238636,#7ee787)"></div></div> {hub_score:.1f}</td>
            <td style="font-size:11px;color:#8b949e">{drugs_list}</td>
          </tr>
"""

html += """        </tbody>
      </table>
    </div>

    <!-- ═══ COMBINATIONS TAB ═══ -->
    <div id="combos" class="tab-content">
      <h3 style="color:#a371f7;margin-bottom:12px">Predicted Synergistic Combinations</h3>
      <p style="font-size:12px;color:#8b949e;margin-bottom:16px">Drug pairs ranked by complementary target coverage across beneficial pathways. Higher score = more synergistic.</p>
"""

for i, combo in enumerate(combos[:15], 1):
    tier_a = combo.get("tier_a", 0)
    tier_b = combo.get("tier_b", 0)
    color_a, label_a = TIER_COLORS.get(tier_a, ("#30363d", "—"))
    color_b, label_b = TIER_COLORS.get(tier_b, ("#30363d", "—"))

    html += f"""      <div class="combo-card">
        <div class="combo-score">#{i} &mdash; {combo['total_score']:.1f}</div>
        <h3>
          <span class="drug-name">{combo['drug_a']}</span>
          <span class="tier-badge" style="background:{color_a}">{label_a}</span>
          &nbsp;+&nbsp;
          <span class="drug-name">{combo['drug_b']}</span>
          <span class="tier-badge" style="background:{color_b}">{label_b}</span>
        </h3>
        <div class="combo-detail">
          <strong>Pathways:</strong> {combo['pathway_count']}/6 &nbsp;|&nbsp;
          <strong>Beneficial:</strong> {combo['beneficial_pathways']} &nbsp;|&nbsp;
          <strong>Targets (union):</strong> {combo['targets_union']} &nbsp;|&nbsp;
          <strong>Complementary:</strong> {combo['targets_complementary']} &nbsp;|&nbsp;
          <strong>Overlap:</strong> {combo['targets_overlap']}
          <br><strong>Rationale:</strong> {combo.get('rationale', '—')}
        </div>
      </div>
"""

html += """    </div>

    <!-- ═══ PPI TAB ═══ -->
    <div id="ppi" class="tab-content">
      <h3 style="color:#58a6ff;margin-bottom:12px">Protein-Protein Interactions (STRING, score ≥ 700)</h3>
      <p style="font-size:12px;color:#8b949e;margin-bottom:16px">High-confidence functional interactions among validated drug targets.</p>
"""

if string_interactions:
    html += """      <table>
        <thead><tr><th>Protein A</th><th>Protein B</th><th>Score</th><th>Implication</th></tr></thead>
        <tbody>
"""
    for ix in string_interactions:
        score = ix.get("score", 0)
        score_pct = min(score * 100, 100)
        html += f"""          <tr>
            <td class="drug-name">{ix['protein_a']}</td>
            <td class="drug-name">{ix['protein_b']}</td>
            <td><div class="score-bar"><div class="score-fill" style="width:{score_pct}%;background:linear-gradient(90deg,#d29922,#f0c040)"></div></div> {score:.3f}</td>
            <td style="font-size:11px;color:#8b949e">Co-functional; shared drug targeting may amplify therapeutic effect</td>
          </tr>
"""
    html += "        </tbody>\n      </table>\n"
else:
    html += "      <p style='color:#8b949e'>No interactions available.</p>\n"

html += """    </div>

    <!-- ═══ ENRICHMENT TAB ═══ -->
    <div id="enrichment" class="tab-content">
      <h3 style="color:#7ee787;margin-bottom:12px">Functional Enrichment (STRING)</h3>
      <p style="font-size:12px;color:#8b949e;margin-bottom:16px">Enriched biological processes among validated drug targets (FDR &lt; 0.05).</p>
"""

# Show KEGG enrichment from Phase 3
kegg_enrichment = string_enrichment.get("KEGG", [])
if kegg_enrichment:
    sig_kegg = [t for t in kegg_enrichment if t.get("fdr", 1) < 0.05][:15]
    if sig_kegg:
        max_genes = max(t.get("gene_count", 1) for t in sig_kegg)
        html += "      <h4 style='color:#58a6ff;margin:12px 0 8px'>KEGG Pathways</h4>\n"
        for k in sig_kegg:
            desc = k.get("description", k.get("term", ""))[:55]
            count = k.get("gene_count", 0)
            fdr = k.get("fdr", 1)
            width = max(count / max_genes * 300, 10)
            html += f"""      <div class="pathway-bar">
        <div class="pathway-name" title="{k.get('description', '')}">{desc}</div>
        <div class="pathway-fill" style="width:{width}px;background:linear-gradient(90deg,#238636,#2ea043)">{count} genes</div>
        <span style="font-size:10px;color:#8b949e;margin-left:8px">FDR={fdr:.1e}</span>
      </div>
"""

# Show GO Process enrichment
go_enrichment = string_enrichment.get("Process", [])
if go_enrichment:
    sig_go = [t for t in go_enrichment if t.get("fdr", 1) < 0.05][:10]
    if sig_go:
        max_genes = max(t.get("gene_count", 1) for t in sig_go)
        html += "      <h4 style='color:#58a6ff;margin:20px 0 8px'>GO Biological Process</h4>\n"
        for g in sig_go:
            desc = g.get("description", g.get("term", ""))[:55]
            count = g.get("gene_count", 0)
            fdr = g.get("fdr", 1)
            width = max(count / max_genes * 300, 10)
            html += f"""      <div class="pathway-bar">
        <div class="pathway-name" title="{g.get('description', '')}">{desc}</div>
        <div class="pathway-fill" style="width:{width}px;background:linear-gradient(90deg,#a371f7,#d2a8ff)">{count} genes</div>
        <span style="font-size:10px;color:#8b949e;margin-left:8px">FDR={fdr:.1e}</span>
      </div>
"""

html += """    </div>
  </div>

  <!-- ═══ METHODOLOGY ═══ -->
  <div class="section">
    <h2>Methodology</h2>
    <div style="background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:20px;font-size:13px;color:#8b949e">
      <p><strong style="color:#58a6ff">Phase 1 — Target Identification:</strong> Queried OpenTargets for targets associated with graft rejection, T1D autoimmunity, beta cell apoptosis, immune tolerance, and GvHD. Added 40 curated seed targets from islet transplant literature. Expanded via STRING protein-protein interactions (score &ge;700). <strong>1,372 targets identified.</strong></p>
      <br>
      <p><strong style="color:#58a6ff">Phase 2 — Drug Mapping:</strong> Mapped all Phase 3+ and FDA-approved drugs to the target list via OpenTargets drugAndClinicalCandidates API and ChEMBL mechanisms. Scored by multi-target coverage with novelty bonus. <strong>436 drugs found, 429 novel candidates.</strong></p>
      <br>
      <p><strong style="color:#a371f7">Phase 3 — Network Pharmacology:</strong> Built drug-target-pathway bipartite network. Computed hub target centrality, drug pathway coverage across 6 islet-relevant biological processes, and synergy scores for pairwise combinations. STRING functional enrichment and PPI analysis for validated targets.</p>
      <br>
      <p><strong style="color:#238636">Phase 4 — Literature Validation:</strong> Top 10 candidates validated against clinical/preclinical literature. 3 drugs confirmed with real evidence (tofacitinib, sorafenib, imatinib), 2 contraindicated (regorafenib, pazopanib).</p>
      <br>
      <p><strong>Validation Level:</strong> <span class="badge badge-silver">SILVER</span> per Research Doctrine v1.1. Computational predictions + literature validation + network analysis (2.5 of 3 required sources). Third source needed: domain expert review.</p>
    </div>
  </div>
"""

html += f"""
  <div class="footer">
    Diabetes Research Hub &mdash; Islet Transplant &times; Drug Repurposing Pipeline<br>
    Research Doctrine v1.1 | Generated {date_short} | Phases 1-4 Complete
  </div>

</div>

<script>
function switchTab(e, tabId) {{
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  e.target.classList.add('active');
  document.getElementById(tabId).classList.add('active');
}}

function filterCandidates() {{
  const tier = document.getElementById('tierFilter').value;
  const search = document.getElementById('drugSearch').value.toLowerCase();
  const rows = document.querySelectorAll('#candidateTable tbody tr');
  rows.forEach(row => {{
    const rowTier = row.getAttribute('data-tier');
    const rowName = row.getAttribute('data-name') || '';
    const tierMatch = tier === 'all' || rowTier === tier;
    const searchMatch = !search || rowName.includes(search);
    row.style.display = (tierMatch && searchMatch) ? '' : 'none';
  }});
}}

function sortTable(tableId, colIdx) {{
  const table = document.getElementById(tableId);
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  const asc = table.getAttribute('data-sort-asc') !== 'true';
  table.setAttribute('data-sort-asc', asc);

  rows.sort((a, b) => {{
    let aVal = a.cells[colIdx].textContent.trim();
    let bVal = b.cells[colIdx].textContent.trim();
    const aNum = parseFloat(aVal);
    const bNum = parseFloat(bVal);
    if (!isNaN(aNum) && !isNaN(bNum)) {{
      return asc ? aNum - bNum : bNum - aNum;
    }}
    return asc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
  }});

  rows.forEach(row => tbody.appendChild(row));
}}
</script>

<div style="max-width:1100px;margin:2rem auto;padding:0 2rem;">
  <div style="border-top:1px solid #e0ddd5;padding-top:1rem;">
    <h3 style="font-family:Georgia,serif;font-size:1rem;font-weight:400;margin-bottom:0.5rem;">Key References</h3>
    <p style="font-size:12px;color:#636363;line-height:1.7;">
      Drug repurposing methodology based on mechanism-target mapping and network pharmacology approaches
      (<a href="https://pubmed.ncbi.nlm.nih.gov/30899369/" target="_blank">PMID 30899369</a>).
      Islet transplant immunosuppression protocols and IBMIR mechanisms reviewed in
      (<a href="https://pubmed.ncbi.nlm.nih.gov/29710129/" target="_blank">PMID 29710129</a>;
       <a href="https://pubmed.ncbi.nlm.nih.gov/32175717/" target="_blank">PMID 32175717</a>).
      Protein-protein interaction network data from STRING database
      (<a href="https://pubmed.ncbi.nlm.nih.gov/36449148/" target="_blank">PMID 36449148</a>).
      Combination therapy rationale informed by calcineurin-sparing approaches
      (<a href="https://pubmed.ncbi.nlm.nih.gov/37359825/" target="_blank">PMID 37359825</a>).
    </p>
  </div>
</div>

</body>
</html>"""

output_path = DASH_DIR / "Islet_Drug_Repurposing.html"
with open(output_path, "w") as f:
    f.write(html)

print(f"Dashboard v2 saved to: {output_path}")
print(f"  Candidates: {len(novel)}")
print(f"  Hub targets: {len(hub_targets)}")
print(f"  Combinations: {len(combos)}")
print(f"  PPI interactions: {len(string_interactions)}")
print(f"  KEGG enrichment terms: {len(kegg_enrichment)}")
