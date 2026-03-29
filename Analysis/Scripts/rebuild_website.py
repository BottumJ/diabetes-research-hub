#!/usr/bin/env python3
"""
Rebuild GitHub Pages site — Tufte-informed design.

Generates a clean, research-credible landing page following Tufte principles:
  - Light background, restrained typography
  - No emoji icons (replaced with text/nothing)
  - Source citations visible
  - Professional, not promotional
  - Accurate statistics with source dates

Output: docs/index.html
"""

import os
import json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RESULTS_DIR = os.path.join(BASE_DIR, 'Analysis', 'Results')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

def get_trial_count():
    """Get actual trial count from data."""
    try:
        path = os.path.join(RESULTS_DIR, 'clinical_trials_latest.json')
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        return data['metadata']['total_trials']
    except Exception:
        return 746

def generate_site():
    trial_count = get_trial_count()
    now = datetime.now().strftime('%Y-%m-%d')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diabetes Research Hub</title>
<meta name="description" content="Open-source computational analysis of the global diabetes research landscape. Triple-source validated, PRISMA-aligned.">
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
  --serif: Georgia, 'Times New Roman', serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --mono: 'SF Mono', Consolas, Monaco, monospace;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: var(--sans); background: var(--bg); color: var(--text); line-height: 1.65; }}

.header {{ max-width: 900px; margin: 0 auto; padding: 48px 32px 32px; }}
.header h1 {{ font-family: var(--serif); font-size: 32px; font-weight: 400; }}
.header .desc {{ font-size: 15px; color: var(--muted); margin-top: 10px; max-width: 680px; }}
.header .figures {{ display: flex; gap: 28px; margin-top: 20px; flex-wrap: wrap; }}
.header .fig {{ }}
.header .fig .num {{ font-family: var(--mono); font-size: 24px; font-weight: 700; }}
.header .fig .label {{ font-size: 11px; color: var(--muted); }}

nav {{ max-width: 900px; margin: 0 auto; padding: 0 32px; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); display: flex; gap: 20px; }}
nav a {{ color: var(--muted); text-decoration: none; font-size: 13px; padding: 10px 0; }}
nav a:hover {{ color: var(--text); }}

.container {{ max-width: 900px; margin: 0 auto; padding: 32px; }}

h2 {{ font-family: var(--serif); font-size: 20px; font-weight: 400; margin-bottom: 16px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }}

.cards {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 36px; }}
@media (max-width: 700px) {{ .cards {{ grid-template-columns: 1fr; }} }}
.card {{ background: var(--surface); border: 1px solid var(--border); padding: 20px; }}
.card .status {{ font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }}
.card .status.live {{ color: var(--green); }}
.card .status.upcoming {{ color: var(--light); }}
.card h3 {{ font-family: var(--serif); font-size: 16px; font-weight: 400; margin-bottom: 6px; }}
.card p {{ font-size: 13px; color: var(--muted); margin-bottom: 12px; }}
.card a {{ color: var(--accent); font-size: 13px; text-decoration: none; }}
.card a:hover {{ text-decoration: underline; }}

.approach {{ background: var(--surface); border: 1px solid var(--border); padding: 24px; margin-bottom: 36px; }}
.approach h3 {{ font-family: var(--serif); font-size: 16px; font-weight: 400; margin-bottom: 14px; }}
.pipeline-flow {{ display: flex; align-items: center; gap: 6px; margin-bottom: 18px; flex-wrap: wrap; font-size: 13px; }}
.pipeline-flow .stage {{ border: 1px solid var(--border); padding: 8px 16px; text-align: center; }}
.pipeline-flow .stage strong {{ display: block; font-size: 12px; letter-spacing: 0.5px; }}
.pipeline-flow .stage span {{ font-size: 11px; color: var(--muted); }}
.pipeline-flow .arrow {{ color: var(--light); }}
.principles {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
@media (max-width: 700px) {{ .principles {{ grid-template-columns: 1fr; }} }}
.principle {{ padding-left: 12px; border-left: 2px solid var(--border); font-size: 13px; }}
.principle strong {{ display: block; margin-bottom: 2px; }}
.principle span {{ color: var(--muted); }}

.domains {{ margin-bottom: 36px; }}
.domain-list {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.domain-tag {{ border: 1px solid var(--border); padding: 4px 10px; font-size: 12px; color: var(--muted); }}

.cta {{ text-align: center; padding: 32px; margin-bottom: 36px; border: 1px solid var(--border); background: var(--surface); }}
.cta h2 {{ border: none; margin-bottom: 8px; }}
.cta p {{ font-size: 14px; color: var(--muted); margin-bottom: 16px; max-width: 500px; margin-left: auto; margin-right: auto; }}
.cta .btns {{ display: flex; gap: 12px; justify-content: center; }}
.cta .btn {{ padding: 10px 22px; text-decoration: none; font-size: 13px; font-weight: 600; }}
.cta .btn-primary {{ background: var(--accent); color: #fff; }}
.cta .btn-secondary {{ border: 1px solid var(--accent); color: var(--accent); }}

.footer {{ max-width: 900px; margin: 0 auto; padding: 20px 32px; border-top: 1px solid var(--border); font-size: 11px; color: var(--light); }}
.footer a {{ color: var(--accent); text-decoration: none; }}
</style>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-JGMD5VRYPH');</script>
</head>
<body>

<div class="header">
  <h1>Diabetes Research Hub</h1>
  <div class="desc">Open-source computational analysis of the global diabetes research landscape. Mapping gaps, tracking clinical trials, and synthesizing findings across 35 research domains to accelerate progress toward prevention, treatment, and cure.</div>
  <div class="figures">
    <div class="fig"><div class="num">{trial_count}</div><div class="label">Clinical trials tracked</div></div>
    <div class="fig"><div class="num">35</div><div class="label">Research domains mapped</div></div>
    <div class="fig"><div class="num">435</div><div class="label">Domain pairs analyzed</div></div>
    <div class="fig"><div class="num">15</div><div class="label">PubMed alert queries</div></div>
  </div>
</div>

<nav>
  <a href="#dashboards">Dashboards</a>
  <a href="#approach">Approach</a>
  <a href="#domains">Domains</a>
  <a href="#contribute">Contribute</a>
  <a href="https://github.com/BottumJ/diabetes-research-hub" target="_blank">GitHub</a>
  <a href="https://osf.io/hu9ga" target="_blank">OSF</a>
</nav>

<div class="container">

<section id="dashboards">
<h2>Analysis &amp; Dashboards</h2>

<h3 style="font-family:var(--serif);font-size:16px;font-weight:400;margin:24px 0 12px;color:var(--muted);">Core Platform Tools</h3>
<div class="cards">
  <div class="card">
    <div class="status live">Available</div>
    <h3>Research Dashboard</h3>
    <p>Interactive overview of the diabetes research landscape: 55 pipeline entries, 35 research domains, 22 datasets, 25 tracked papers across 12 categories.</p>
    <a href="Dashboards/Research_Dashboard.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Clinical Trial Intelligence</h3>
    <p>{trial_count} diabetes clinical trials from ClinicalTrials.gov. Searchable, filterable, with pipeline analysis and sponsor landscape. Data updated via automated scripts.</p>
    <a href="Dashboards/Clinical_Trial_Dashboard.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Medical Data Dictionary</h3>
    <p>100 medical terms with journal-cited definitions (86 PMIDs), body system maps, 6 biological pathway diagrams, and gap connections. Built for non-clinicians.</p>
    <a href="Dashboards/Medical_Data_Dictionary.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Acronym Database</h3>
    <p>147 curated diabetes research acronyms across 10 categories. Instant search, category filters, alphabet navigation.</p>
    <a href="Dashboards/Acronym_Database.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Literature Gap Analysis</h3>
    <p>Pairwise analysis of 30 PubMed domains (435 pairs) with interpreted classifications: meaningful opportunities vs. methodologically distinct pairs.</p>
    <a href="Analysis/Results/literature_gap_report.md">View report &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Publication Monitor</h3>
    <p>Rolling 30-day PubMed snapshot across 15 high-priority research domains. Cross-domain papers flagged for synthesis potential.</p>
    <a href="Analysis/Results/pubmed_recent_summary.md">View report &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Methodology &amp; Validation Framework</h3>
    <p>Triple-source validation, gap identification methodology, citation standards, and data sources. Complete documentation of research methods and validation tiers (GOLD/SILVER/BRONZE).</p>
    <a href="Dashboards/Methodology.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Paper Library</h3>
    <p>Ingested library of 226 research papers with abstracts, full text (91 papers), citation validation scores, cross-citation network (90 links), and 30 topic clusters. Searchable and sortable.</p>
    <a href="Dashboards/Paper_Library.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>PMID Verification Report</h3>
    <p>Automated citation verification against NCBI PubMed — every PMID checked for accuracy. Complete audit trail of all citations across the project.</p>
    <a href="Dashboards/PMID_Verification.html">Open dashboard &rarr;</a>
  </div>
</div>

<h3 style="font-family:var(--serif);font-size:16px;font-weight:400;margin:24px 0 12px;color:var(--muted);">Actionable Research Tools</h3>
<div class="cards">
  <div class="card">
    <div class="status live">Available</div>
    <h3>Generic Drug Repurposing Screen</h3>
    <p>Pressure-tested screen of 34 generic drugs scored across mechanism relevance, safety, generic availability, evidence strength, and equity impact. WHO flags verified, negative trials labeled, preclinical claims distinguished. 27 candidates under $1/month.</p>
    <a href="Dashboards/Drug_Repurposing_Screen.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>LADA Diagnostic Cost-Effectiveness Model</h3>
    <p>Four screening scenarios modeled across 4 healthcare tiers over 10- and 20-year horizons. Universal GAD screening: $36,554/QALY. 4.85M LADA cases detectable per year worldwide.</p>
    <a href="Dashboards/LADA_Diagnostic_Model.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Clinical Trial Equity Mapper</h3>
    <p>Geographic mismatch between diabetes burden and advanced therapy trial sites across 40+ countries. 19 real clinical trials mapped against IDF burden data. Priority expansion rankings.</p>
    <a href="Dashboards/Trial_Equity_Mapper.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Corpus Analysis</h3>
    <p>Term frequency, co-occurrence networks, and gap coverage analysis across 202 indexed papers. Identifies uncovered research intersections and surprising cross-domain connections.</p>
    <a href="Dashboards/Corpus_Analysis.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Extracted Evidence Dashboard</h3>
    <p>Quantitative data extracted from 61 full-text papers: 472 data points across 9 categories. C-peptide, survival rates, inflammatory markers, and drug doses with direct links to source PMIDs and context.</p>
    <a href="Dashboards/Extracted_Evidence.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Research Paths Validation</h3>
    <p>48 mechanistic pathways extracted from corpus. 25 cross-validated against PubMed/systematic reviews: 18 VALIDATED, 6 PARTIALLY_VALIDATED, 1 UNVALIDATED. Oxidative stress emerges as central hub connecting inflammation, T2D, nephropathy, cardiovascular disease.</p>
    <a href="Dashboards/Research_Paths.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Statistical Analysis Dashboard</h3>
    <p>Meta-analytic pooling (HbA1c reduction: -0.93%, 95% CI: -0.97 to -0.90), Bayesian evidence synthesis (48 pathways, oxidative stress → inflammation highest posterior), Monte Carlo sensitivity for LADA screening and drug robustness across 5,000 simulations.</p>
    <a href="Dashboards/Statistical_Analysis.html">Open dashboard &rarr;</a>
  </div>
</div>

<h3 style="font-family:var(--serif);font-size:16px;font-weight:400;margin:24px 0 12px;color:var(--muted);">GOLD-Validated Research (3+ independent sources)</h3>
<div class="cards">
  <div class="card">
    <div class="status live">Available</div>
    <h3>LADA Natural History Model</h3>
    <p>Computational model of C-peptide decline trajectories for LADA1 vs LADA2. Autoantibody risk stratification, intervention windows, and genetic markers. Gap #1 (SILVER).</p>
    <a href="Dashboards/LADA_Natural_History.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Islet Transplant Outcomes</h3>
    <p>Graft survival analysis by immunosuppression protocol. The tacrolimus paradox, calcineurin-sparing alternatives, IEQ/kg dose-response, and VX-880 next-generation data. Gap #3 (GOLD).</p>
    <a href="Dashboards/Islet_Transplant_Analysis.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Beta Cell Equity Analysis</h3>
    <p>Geographic mismatch between beta cell therapy trial sites and diabetes burden. 88% of trials in HICs; 81% of burden in LMICs. Supply, demand, and gap analysis.</p>
    <a href="Dashboards/Equity_Map.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Health Equity in Diabetes Research</h3>
    <p>Systemic disparities in clinical trial representation, geographic access, and socioeconomic barriers. Comprehensive analysis of equity gaps across the diabetes research landscape. Gap #2 (GOLD).</p>
    <a href="Dashboards/Health_Equity.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Gap Deep Dives</h3>
    <p>Comprehensive analysis of 15 cross-domain research gaps. 71 PMIDs, drug immunomodulatory catalog, CAR-Treg pipeline, GKA landscape, health equity data. 202KB of evidence.</p>
    <a href="Dashboards/Gap_Deep_Dives.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Gap Synthesis</h3>
    <p>15 research gaps framed through the scientific method with GOLD/SILVER/BRONZE validation tiers. Observation, question, hypothesis, proposed investigation for each.</p>
    <a href="Dashboards/Gap_Synthesis.html">Open dashboard &rarr;</a>
  </div>
</div>

<h3 style="font-family:var(--serif);font-size:16px;font-weight:400;margin:24px 0 12px;color:var(--muted);">SILVER-Validated Research (2 independent sources)</h3>
<div class="cards">
  <div class="card">
    <div class="status live">Available</div>
    <h3>Drug Repurposing for Islet Transplant</h3>
    <p>13 repurposable drugs scored across 5 dimensions. IBMIR mechanism, clinical trials, computational priority model. Gap #4 (SILVER - promoted with 11 independent papers from multiple research groups).</p>
    <a href="Dashboards/Drug_Repurposing_Islet.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Treg in Diabetic Neuropathy</h3>
    <p>Novel hypothesis: Treg-based immunotherapy for the neuroinflammatory component of diabetic neuropathy. Publication gap analysis, therapeutic approaches. Gap #5 (SILVER - promoted with 12 independent papers confirming both Treg immunology and neuropathy manifestations).</p>
    <a href="Dashboards/Treg_Neuropathy.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>CAR-T Access Barriers</h3>
    <p>Cost ($373K-$475K per treatment), manufacturing bottlenecks, infrastructure requirements, and 8 cost-reduction pathways for CAR-Treg diabetes therapy. Gap #6 (SILVER).</p>
    <a href="Dashboards/CART_Access_Barriers.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>GKA Drug Repurposing Landscape</h3>
    <p>Complete glucokinase activator landscape. Dorzagliatin (only approved GKA), TTP399 for T1D, why most GKAs failed, and repurposing opportunities. Gap #7 (SILVER).</p>
    <a href="Dashboards/GKA_Landscape.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Immunomodulatory Drugs for LADA</h3>
    <p>9 immunomodulatory candidates for LADA therapeutic window. GAD-alum, teplizumab, rituximab priority analysis. Why LADA is underserved. Gap #8 (SILVER).</p>
    <a href="Dashboards/Immunomod_LADA.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Islet Transplant Registry Equity</h3>
    <p>CITR demographic analysis: 85% White recipients vs 62% T1D population. Geographic, financial, and referral barriers to equitable islet transplant access. Gap #11 (SILVER).</p>
    <a href="Dashboards/Islet_Transplant_Equity.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Generic Drug x Diabetes Catalog</h3>
    <p>20 off-patent drugs with diabetes evidence. Verapamil (beta cell protection), fenofibrate (retinopathy), colchicine (CV risk). Evidence heat map across 7 complications. Gap #12 (SILVER).</p>
    <a href="Dashboards/Generic_Drug_Catalog.html">Open dashboard &rarr;</a>
  </div>
</div>

<h3 style="font-family:var(--serif);font-size:16px;font-weight:400;margin:24px 0 12px;color:var(--muted);">BRONZE / Under Review (Preliminary analysis)</h3>
<div class="cards">
  <div class="card">
    <div class="status live">Available</div>
    <h3>GKA in LADA (Exploratory)</h3>
    <p>Can glucokinase activators preserve beta cell function during LADA decline? Biological plausibility assessment, the "accelerated burnout" concern, TTP399 counter-evidence. Gap #9 (EXPLORATORY).</p>
    <a href="Dashboards/GKA_LADA.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>LADA Prevalence</h3>
    <p>The hidden epidemic: 8.8% of adults diagnosed with T2D actually have LADA (~47M globally). Prevalence by healthcare setting, diagnostic confusion, the sulfonylurea trap. Gap #10 (BRONZE).</p>
    <a href="Dashboards/LADA_Prevalence.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Nutrition for Beta Cells</h3>
    <p>Nutrient-beta cell evidence map: zinc, omega-3, vitamin D, magnesium. Nutrigenomics and microbiome personalization gap. C-peptide preservation endpoints. Gap #13 (BRONZE).</p>
    <a href="Dashboards/Nutrition_Beta_Cells.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>Nutrition for LADA</h3>
    <p>Why LADA needs its own nutrition strategy (not T1D, not T2D). Mediterranean anti-inflammatory base, gut barrier integrity, LAMENS trial design. Gap #14 (BRONZE).</p>
    <a href="Dashboards/Nutrition_LADA.html">Open dashboard &rarr;</a>
  </div>
  <div class="card">
    <div class="status live">Available</div>
    <h3>GKA Pricing Trajectory</h3>
    <p>Three pricing scenarios for glucokinase activators. Dorzagliatin (China), TTP399 T1D pipeline, patent cliff timeline, generic GKA projections 2038-2045. Gap #15 (BRONZE).</p>
    <a href="Dashboards/GKA_Pricing.html">Open dashboard &rarr;</a>
  </div>
</div>

<h3 style="font-family:var(--serif);font-size:16px;font-weight:400;margin:24px 0 12px;color:var(--muted);">Upcoming</h3>
<div class="cards">
  <div class="card">
    <div class="status upcoming">April 2026</div>
    <h3>Multi-Omics Biomarker Integration</h3>
    <p>Pilot analysis integrating public genomics, proteomics, and metabolomics datasets (UK Biobank, DIAGRAM, T1D Knowledge Portal) to identify novel biomarker candidates for diabetes subtypes.</p>
  </div>
  <div class="card">
    <div class="status upcoming">April 2026</div>
    <h3>Pressure Test: LADA Model + Trial Mapper</h3>
    <p>Systematic verification of LADA Diagnostic Model assumptions and Trial Equity Mapper country-level data against WHO, IDF Atlas, and ClinicalTrials.gov primary sources.</p>
  </div>
  <div class="card">
    <div class="status live">Completed</div>
    <h3>BRONZE-to-SILVER Gap Promotion</h3>
    <p>Gap #4 (Drug Repurposing for Islet Transplant) and Gap #5 (Treg in Diabetic Neuropathy) promoted to SILVER tier through validation with 11 and 12 independent papers respectively from multiple research groups confirming both sides of each gap.</p>
  </div>
</div>
</section>

<section id="approach">
<div class="approach">
  <h3>Methodology</h3>
  <div class="pipeline-flow">
    <div class="stage"><strong>PRODUCE</strong><span>Computational analysis<br>of public data</span></div>
    <div class="arrow">&rarr;</div>
    <div class="stage"><strong>VALIDATE</strong><span>Triple-source verified<br>PRISMA/GRADE aligned</span></div>
    <div class="arrow">&rarr;</div>
    <div class="stage"><strong>PUBLISH</strong><span>GitHub, OSF, preprints<br>open access</span></div>
    <div class="arrow">&rarr;</div>
    <div class="stage"><strong>CONNECT</strong><span>Researchers, foundations<br>clinical teams</span></div>
  </div>
  <div class="principles">
    <div class="principle"><strong>Triple-Source Validation</strong><span>Major claims require 3 independent sources (Gold), 2 (Silver), or are labeled as preliminary (Bronze). Aligned with Oxford CEBM evidence levels 1a&ndash;5.</span></div>
    <div class="principle"><strong>PRISMA 2020 Compliance</strong><span>Systematic work follows PRISMA 2020 with pre-registered protocols, documented search strategies, and explicit inclusion/exclusion criteria.</span></div>
    <div class="principle"><strong>Fully Open &amp; Reproducible</strong><span>All code (MIT), data sources, and methods are public. Analyses can be independently reproduced. Pre-registered on OSF.</span></div>
    <div class="principle"><strong>Cross-Domain Synthesis</strong><span>Analysis spans 35 domains simultaneously, finding connections and gaps that single-domain research programs may miss.</span></div>
  </div>
</div>
</section>

<section id="domains">
<h2>Research Domains</h2>
<div class="domain-list">
  <span class="domain-tag">T1D Immunotherapy</span>
  <span class="domain-tag">Stem Cell / Islet</span>
  <span class="domain-tag">Beta Cell Regeneration</span>
  <span class="domain-tag">Gene Therapy</span>
  <span class="domain-tag">GLP-1 Agonists</span>
  <span class="domain-tag">T2D Remission</span>
  <span class="domain-tag">SGLT2 Inhibitors</span>
  <span class="domain-tag">Insulin Resistance</span>
  <span class="domain-tag">Closed-Loop Systems</span>
  <span class="domain-tag">CGM Technology</span>
  <span class="domain-tag">AI/ML Prediction</span>
  <span class="domain-tag">Multi-Omics</span>
  <span class="domain-tag">Biomarkers</span>
  <span class="domain-tag">Epigenetics</span>
  <span class="domain-tag">GWAS / Genetics</span>
  <span class="domain-tag">Microbiome</span>
  <span class="domain-tag">Drug Repurposing</span>
  <span class="domain-tag">Nephropathy</span>
  <span class="domain-tag">Retinopathy</span>
  <span class="domain-tag">Neuropathy</span>
  <span class="domain-tag">Cardiovascular</span>
  <span class="domain-tag">Gestational DM</span>
  <span class="domain-tag">LADA</span>
  <span class="domain-tag">MODY</span>
  <span class="domain-tag">Pediatric</span>
  <span class="domain-tag">Health Equity</span>
  <span class="domain-tag">Epidemiology</span>
  <span class="domain-tag">Prevention</span>
  <span class="domain-tag">Proteomics</span>
  <span class="domain-tag">Metabolomics</span>
  <span class="domain-tag">Network Pharmacology</span>
  <span class="domain-tag">Clinical Decision Support</span>
  <span class="domain-tag">Patient-Reported Outcomes</span>
  <span class="domain-tag">Autoimmunity</span>
  <span class="domain-tag">Personalized Nutrition</span>
</div>
</section>

<div style="height:24px"></div>

<section id="contribute">
<div class="cta">
  <h2>Contribute</h2>
  <p>Open research project. All code, data, and findings freely available under MIT and CC-BY 4.0 licenses. Feedback, critique, and collaboration welcome.</p>
  <div class="btns">
    <a class="btn btn-primary" href="https://github.com/BottumJ/diabetes-research-hub" target="_blank">GitHub Repository</a>
    <a class="btn btn-secondary" href="https://osf.io/hu9ga" target="_blank">OSF Registration</a>
  </div>
</div>
</section>

</div>

<div class="footer">
  Diabetes Research Hub &copy; 2026 Justin Bottum &middot; <a href="https://github.com/BottumJ/diabetes-research-hub">GitHub</a> &middot; <a href="https://osf.io/hu9ga">OSF</a> &middot; MIT License (code), CC-BY 4.0 (content)<br>
  Independent research project. Not medical advice. All findings require independent verification before clinical application. Last updated: {now}
</div>

</body>
</html>'''

def main():
    print("Generating Tufte-style GitHub Pages site...")
    html = generate_site()

    os.makedirs(DOCS_DIR, exist_ok=True)
    out_path = os.path.join(DOCS_DIR, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Written: {out_path} ({len(html)/1024:.0f} KB)")
    print("Done.")

if __name__ == '__main__':
    main()
