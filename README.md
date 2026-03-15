# Diabetes Research Hub

An open, AI-driven research synthesis and computational analysis platform focused on accelerating cures for Type 1 and Type 2 diabetes.

This project systematically tracks, validates, and analyzes diabetes research across 35 domains — from stem cell therapies and immunology to microbiome science, AI/ML applications, and health equity. All claims are triple-source verified following a formal Research Doctrine aligned with PRISMA 2020, GRADE, and Oxford CEBM evidence standards.

---

## What This Project Does

**Literature Gap Analysis** — Queries PubMed to map publication density across all 30 research domain pairs, identifying under-researched intersections where new work could have outsized impact.

**Clinical Trial Intelligence** — Pulls live snapshots from ClinicalTrials.gov API v2 across five categories (T1D cure, T1D immunotherapy, T2D novel therapies, diabetes devices, recently completed trials). Diffs snapshots over time to detect new trials, status changes, and freshly posted results.

**PubMed Surveillance** — Monitors 15 high-priority alert channels for recent publications. Flags cross-domain papers and tracks publication volume trends.

**Research Tracker** — A structured spreadsheet tracking 55 pipeline entries, 25 high-impact papers, 22 public datasets, and 35 mapped research domains with key open questions.

**Interactive Dashboard** — A visual research command center with filterable pipeline, charts, timeline, and dataset catalog.

---

## Repository Structure

```
Diabetes_Research/
├── README.md                          # This file
├── RESEARCH_DOCTRINE.md               # Governing standards for ingest, validation, and action
├── CONTRIBUTION_STRATEGY.md           # How findings get distributed and the feedback loop
├── Research_Findings_Summary.md       # Comprehensive findings across all 12 domains
├── Diabetes_Research_Tracker.xlsx     # Master tracker (5 sheets, 55 pipeline entries)
│
├── Analysis/
│   ├── Scripts/
│   │   ├── run_all.py                         # Master runner for all scripts
│   │   ├── project1_literature_gap_analysis.py # PubMed gap analysis (Project 1)
│   │   ├── baseline_clinical_trials.py        # ClinicalTrials.gov snapshot
│   │   ├── baseline_pubmed_alerts.py          # PubMed recent papers tracker
│   │   └── hub_monitor.py                     # File change detector
│   ├── Results/                       # Script outputs (JSON snapshots, reports, matrices)
│   └── Notebooks/                     # Future: Jupyter analysis notebooks
│
├── Dashboards/
│   ├── Research_Dashboard.html        # Interactive visual dashboard (6 tabs)
│   └── Clinical_Trial_Dashboard.html  # Clinical trial intelligence (746 trials)
│
├── docs/
│   └── index.html                    # GitHub Pages public website
│
├── Papers/
│   ├── T1D/
│   ├── T2D/
│   └── Shared_Mechanisms/
│
├── Datasets/
│   ├── Genomics/
│   ├── Clinical_Trials/
│   ├── Metabolomics/
│   └── Proteomics/
│
└── Notes/
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- `openpyxl` (`pip install openpyxl`)
- Internet connection (for PubMed and ClinicalTrials.gov API queries)

### Run All Scripts
```powershell
cd Diabetes_Research/Analysis/Scripts
python run_all.py
```

### Run Individual Scripts
```powershell
python run_all.py --project1   # Literature gap analysis
python run_all.py --trials     # Clinical trial snapshot
python run_all.py --pubmed     # PubMed recent papers
python run_all.py --monitor    # Hub file monitor
```

### Outputs
All results are saved to `Analysis/Results/` as JSON snapshots, Excel workbooks, and Markdown reports. Dated snapshots enable diffing over time to detect changes.

---

## Research Doctrine

This project follows a formal Research Doctrine that governs how information is ingested, validated, and acted upon. Key principles:

- **Triple-Source Validation**: No claim is presented as fact without three independent sources from different research groups and institutions.
- **CEBM Evidence Levels**: All sources are classified using the Oxford Centre for Evidence-Based Medicine hierarchy (Level 1a through 5).
- **GRADE Certainty Assessment**: Evidence certainty is rated High, Moderate, Low, or Very Low with explicit rationale.
- **PRISMA 2020 Alignment**: Systematic searches follow PRISMA reporting requirements including pre-registration, flow diagrams, and documented inclusion/exclusion criteria.
- **Terminology Standards**: Precise language (e.g., "functional cure" not "cure", "demonstrated in [context]" not "proven").

See [RESEARCH_DOCTRINE.md](RESEARCH_DOCTRINE.md) for the full framework.

---

## Contribution Areas

Based on systematic niche evaluation, our highest-value contribution areas are:

1. **Multi-Omics Biomarker Integration** — Cross-omics network analysis using public datasets
2. **Literature Synthesis & Gap Analysis** — Systematic reviews and cross-domain pattern identification
3. **Clinical Trial Intelligence** — Automated monitoring and cross-trial pattern analysis
4. **Drug Repurposing Screening** — Computational screening of approved drugs against diabetes targets
5. **AI/ML Prediction Models** — Risk and complication prediction using public data
6. **Epidemiological Data Analysis** — Disparity quantification and prevention program modeling

See [CONTRIBUTION_STRATEGY.md](CONTRIBUTION_STRATEGY.md) for the full distribution and feedback loop plan.

---

## OSF Registration

This project is registered on the Open Science Framework with a pre-registered analysis protocol:

- **Project:** [osf.io/hu9ga](https://osf.io/hu9ga)
- **Registration Type:** OSF Preregistration
- **License:** CC-BY Attribution 4.0 International (research content), MIT (code)

---

## Key Findings So Far

### Literature Gap Analysis (Project 1)
Queried PubMed for 30 domains × 435 pairwise combinations. Top under-researched intersections include:
- Autoimmunity T1D × Gene Therapy (0 joint publications)
- Beta Cell Regeneration × Health Equity (0 joint publications)
- Islet Transplant × Drug Repurposing (0 joint publications)
- GWAS/Polygenic × Closed Loop/Artificial Pancreas (0 joint publications)

Full results: `Analysis/Results/literature_gap_report.md`

---

## Disclaimer

This project is an independent research synthesis operation. It does not provide medical advice, treatment recommendations, or clinical guidance. All findings are for research purposes only. We are not medical professionals. All claims are validated against published peer-reviewed literature and clearly labeled with their evidence level and confidence tier.

---

## License

MIT License. All code, analysis, and documentation in this repository are freely available for any use.

---

## Contact

Justin Bottum — justin.bottum@gmail.com

*Built with AI-assisted research synthesis. Governed by the Research Doctrine (v1.0, March 2026).*
