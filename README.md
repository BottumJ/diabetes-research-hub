# Diabetes Research Hub

An open, AI-driven research synthesis and computational analysis platform focused on accelerating cures for Type 1 and Type 2 diabetes.

This project systematically tracks, validates, and analyzes diabetes research across 35 domains — from stem cell therapies and immunology to microbiome science, AI/ML applications, and health equity. All claims are triple-source verified following a formal Research Doctrine aligned with PRISMA 2020, GRADE, and Oxford CEBM evidence standards.

---

## What This Project Does

**Literature Gap Analysis** — Queries PubMed to map publication density across all 30 research domain pairs, identifying under-researched intersections where new work could have outsized impact. 15 research gaps are tracked with tiered validation: 4 GOLD (3+ sources), 7 SILVER (2 sources), 3 BRONZE (computational analysis), 1 EXPLORATORY.

**Clinical Trial Intelligence** — Pulls live snapshots from ClinicalTrials.gov API v2 across five categories (T1D cure, T1D immunotherapy, T2D novel therapies, diabetes devices, recently completed trials). Diffs snapshots over time to detect new trials, status changes, and freshly posted results.

**PubMed Surveillance** — Monitors 15 high-priority alert channels for recent publications. Flags cross-domain papers and tracks publication volume trends.

**Paper Library & Citation Validation** — 199 ingested papers (198 abstracts, 86 full text) with PMID cross-referencing against PubMed API. Every citation is scored CONFIRMED/PLAUSIBLE/WEAK/MISMATCH.

**Research Tracker** — A structured spreadsheet tracking 55 pipeline entries, 25 high-impact papers, 22 public datasets, and 35 mapped research domains with key open questions.

**Actionable Research Tools** — Three equity-focused tools that go beyond documenting gaps to producing actionable intervention frameworks:
- Generic Drug Repurposing Screen (34 drugs, pressure-tested against WHO EML and PubMed)
- LADA Diagnostic Cost-Effectiveness Model (4 screening scenarios across 4 healthcare tiers)
- Clinical Trial Site Equity Mapper (40+ countries, 12 verified trials with NCT numbers)

**29 Interactive Dashboards** — Tufte-style HTML dashboards covering every research gap, the full paper library, medical data dictionary (116 terms), acronym database, methodology framework, and all three actionable tools.

---

## Repository Structure

```
Diabetes_Research/
├── README.md                          # This file
├── RESEARCH_DOCTRINE.md               # Governing standards for ingest, validation, and action
├── CONTRIBUTION_STRATEGY.md           # How findings get distributed and the feedback loop
├── CONTRIBUTING.md                    # Contributor guidelines
├── OSF_PREREGISTRATION.md             # Open Science Framework protocol
├── Research_Findings_Summary.md       # Comprehensive findings across all 12 domains
├── Diabetes_Research_Tracker.xlsx     # Master tracker (5 sheets, 55 pipeline entries)
│
├── Analysis/
│   ├── Scripts/                       # 35 Python build scripts + 8 utility scripts
│   │   ├── run_quality_improvements.py        # Master runner (35 scripts)
│   │   ├── run_all.py                         # Legacy runner for baseline scripts
│   │   ├── build_drug_repurposing_screen.py   # 34-drug equity screen (pressure-tested)
│   │   ├── build_lada_diagnostic_model.py     # LADA screening cost-effectiveness
│   │   ├── build_trial_equity_mapper.py       # Global trial equity mapper
│   │   ├── build_data_dictionary.py           # 116-term medical dictionary
│   │   ├── build_gap_deep_dives.py            # All 15 gap deep dives
│   │   ├── ingest_papers.py                   # PubMed/PMC paper ingestion
│   │   ├── validate_citations.py              # Citation cross-referencing
│   │   └── ... (35 total build scripts)
│   ├── Results/                       # Script outputs, paper library, evidence cache
│   └── Notebooks/                     # Future: Jupyter analysis notebooks
│
├── Dashboards/                        # 29 Tufte-style HTML dashboards
│   ├── Drug_Repurposing_Screen.html   # 34-drug equity intervention screen
│   ├── LADA_Diagnostic_Model.html     # Screening cost-effectiveness model
│   ├── Trial_Equity_Mapper.html       # Global trial site equity analysis
│   ├── Medical_Data_Dictionary.html   # 116 terms, 9 body systems
│   ├── Paper_Library.html             # Searchable paper library
│   ├── Gap_Deep_Dives.html            # All 15 research gaps
│   └── ... (29 total dashboards)
│
├── docs/
│   ├── index.html                    # GitHub Pages public website
│   └── Dashboards/                   # Deployed dashboard copies
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

### Run the Full Build Suite (35 scripts)
```powershell
cd Diabetes_Research/Analysis/Scripts
python run_quality_improvements.py
```

### Run Baseline Scripts Only
```powershell
python run_all.py --project1   # Literature gap analysis
python run_all.py --trials     # Clinical trial snapshot
python run_all.py --pubmed     # PubMed recent papers
python run_all.py --monitor    # Hub file monitor
```

### Outputs
All results are saved to `Analysis/Results/` as JSON snapshots, Excel workbooks, and Markdown reports. Dashboards are generated to `Dashboards/` as self-contained HTML files. Dated snapshots enable diffing over time to detect changes.

---

## Validation Framework

This project uses a 4-tier evidence classification system:

| Tier | Requirement | Count |
|------|------------|-------|
| **GOLD** | 3+ independent sources from different research groups | 4 gaps |
| **SILVER** | 2 independent sources | 7 gaps |
| **BRONZE** | Computational analysis with single-source basis | 3 gaps |
| **EXPLORATORY** | Biological plausibility uncertain | 1 gap |

All claims in the Drug Repurposing Screen have been pressure-tested: WHO Essential Medicines flags verified against the 2023 EML, mechanism claims checked against cited PMIDs, negative trials explicitly labeled, preclinical-only evidence clearly distinguished from human RCT data.

See [RESEARCH_DOCTRINE.md](RESEARCH_DOCTRINE.md) for the full framework (PRISMA 2020, GRADE, Oxford CEBM).

---

## The 15 Research Gaps

| # | Gap | Tier |
|---|-----|------|
| 1 | Gene Therapy for LADA | SILVER |
| 2 | Health Equity in Beta Cell Therapies | GOLD |
| 3 | Insulin Resistance in Islet Transplant | GOLD |
| 4 | Drug Repurposing for Islet Transplant | SILVER |
| 5 | Treg in Diabetic Neuropathy | SILVER |
| 6 | CAR-T Access Barriers in Diabetes | GOLD |
| 7 | GKA Drug Repurposing | SILVER |
| 8 | Immunomodulatory Drugs for LADA | SILVER |
| 9 | GKA in LADA | EXPLORATORY |
| 10 | LADA Prevalence | SILVER |
| 11 | Islet Transplant Equity | GOLD |
| 12 | Generic Drug x Diabetes Mechanism Catalog | SILVER |
| 13 | Personalized Nutrition for Beta Cells | BRONZE |
| 14 | Personalized Nutrition for LADA | BRONZE |
| 15 | GKA Pricing Trajectory | BRONZE |

---

## Contribution Areas

Based on systematic niche evaluation, our highest-value contribution areas are:

1. **Multi-Omics Biomarker Integration** — Cross-omics network analysis using public datasets
2. **Literature Synthesis & Gap Analysis** — Systematic reviews and cross-domain pattern identification
3. **Clinical Trial Intelligence** — Automated monitoring and cross-trial pattern analysis
4. **Drug Repurposing Screening** — Computational screening of approved drugs against diabetes targets (SHIPPED: 34-drug screen)
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

### Literature Gap Analysis
Queried PubMed for 30 domains x 435 pairwise combinations. Top under-researched intersections include: Autoimmunity T1D x Gene Therapy (0 joint publications), Beta Cell Regeneration x Health Equity (0 joint publications), Islet Transplant x Drug Repurposing (0 joint publications), GWAS/Polygenic x Closed Loop/Artificial Pancreas (0 joint publications).

### Drug Repurposing Screen (Pressure-Tested)
34 generic drugs scored across 5 dimensions (mechanism 25%, safety 20%, generic availability 20%, evidence 20%, equity 15%). Top candidates: Metformin (10.0), Verapamil (8.8), Losartan (8.75). 12 WHO Essential Medicines, 27 sub-$1/month, 14 biological pathways mapped. All mechanism claims verified against source PMIDs; negative trials explicitly labeled.

### LADA Diagnostic Model (Pressure-Tested)
Targeted screening is most cost-effective at $40,614/QALY, detecting 2,730 cases. Universal screening detects 7,953 cases at $56,063/QALY. Two-stage screening balances cost and detection at $47,745/QALY. Model uses corrected GAD antibody sensitivity (82%, DASP standardized) and Medicare complication costs ($5,876, PMID:37909353). All parameters pressure-tested against published literature.

### Trial Equity Mapper (Pressure-Tested)
12 verified clinical trials (all NCTs confirmed on ClinicalTrials.gov) mapped against IDF Diabetes Atlas 2024 burden data for 40 countries. Previous version contained fabricated sponsor names and wrong NCT attributions; all removed in March 2026 credibility audit. Insulin access scores documented as custom composite estimates.

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
