# OSF Pre-Registration Protocol
## Diabetes Research Hub: Systematic Cross-Domain Analysis of Diabetes Research Landscape

**Registration date:** March 15, 2026
**Registrant:** Justin Bottum (justin.bottum@gmail.com)
**Affiliation:** Independent Researcher
**License:** MIT (code), CC-BY 4.0 (content)

---

## 1. Study Information

### 1.1 Title
*Systematic Cross-Domain Analysis of the Diabetes Research Landscape: Identifying Gaps, Emerging Trends, and Opportunities for Computational Contribution*

### 1.2 Authors
Justin Bottum, Independent Researcher

### 1.3 Description
This project applies computational methods to systematically map the global diabetes research landscape across 35 research domains spanning Type 1 diabetes, Type 2 diabetes, gestational diabetes, and related conditions. The work synthesizes publicly available literature (PubMed), clinical trial registries (ClinicalTrials.gov), and biomedical datasets to identify research gaps, emerging trends, cross-domain opportunities, and high-value areas where independent computational analysis can contribute to advancing diabetes prevention, treatment, and cure.

### 1.4 Hypotheses
This is primarily an exploratory, descriptive study. However, we pre-register the following specific hypotheses:

**H1:** Cross-domain research gaps exist between diabetes research domains that are individually active but rarely studied together. Specifically, we hypothesize that fewer than 5% of domain pairs will have co-publication rates exceeding the geometric mean of their individual publication rates.

**H2:** The clinical trial pipeline for T1D curative therapies (stem cell, immunotherapy, gene therapy) has accelerated since 2023, with a greater proportion of trials in Phase 2-3 compared to the 2018-2022 period.

**H3:** Computational methods (AI/ML, multi-omics integration, network analysis) applied to diabetes are concentrated in a small number of institutions, leaving significant opportunity for independent computational contributions.

**H4:** Cross-domain papers (appearing in multiple PubMed search domains simultaneously) represent higher-impact work, as measured by journal impact factor and citation rate.

---

## 2. Design Plan

### 2.1 Study Type
Systematic computational analysis of publicly available biomedical data sources. No human subjects, no clinical intervention.

### 2.2 Blinding
Not applicable (observational/computational study).

### 2.3 Study Design
Multi-component observational study with four integrated analysis modules:

**Module A: Literature Gap Analysis**
- Systematic PubMed query of 30 diabetes research domains
- Pairwise co-publication analysis (435 domain pairs)
- Gap scoring using normalized inverse overlap metric
- Identification of underexplored cross-domain opportunities

**Module B: Clinical Trial Intelligence**
- Snapshot of all active diabetes clinical trials from ClinicalTrials.gov API v2
- Categorization by type (T1D cure, immunotherapy, T2D novel, technology, completed with results)
- Temporal trend analysis of trial initiation, completion, and results posting
- Sponsor landscape mapping

**Module C: PubMed Publication Monitoring**
- 15 high-priority alert queries across diabetes research frontiers
- 30-day rolling window of recent publications
- Cross-domain paper identification
- Publication volume trend tracking

**Module D: Integrated Dashboard and Synthesis**
- Interactive visualization combining all data sources
- Research Domain scoring and priority ranking
- Continuous monitoring via automated daily data pulls

---

## 3. Sampling Plan

### 3.1 Data Sources

| Source | Access Method | Scope |
|--------|-------------|-------|
| PubMed / MEDLINE | E-utilities API (esearch.fcgi, efetch.fcgi) | All indexed biomedical literature |
| ClinicalTrials.gov | REST API v2 | All registered clinical trials |
| Open Targets | REST API | Target-disease associations |
| GWAS Catalog | REST API / Download | Genome-wide association studies |
| GEO / ArrayExpress | API / Download | Gene expression datasets |

### 3.2 Inclusion Criteria
- **Literature:** PubMed-indexed publications matching domain-specific search queries; no date restriction for gap analysis; 30-day rolling window for monitoring
- **Clinical Trials:** Trials with diabetes-related conditions registered on ClinicalTrials.gov; actively recruiting, not yet recruiting, active not recruiting, enrolling by invitation, or recently completed with posted results (2025+)
- **Datasets:** Publicly available, no access restrictions, human subjects data only from de-identified public repositories

### 3.3 Exclusion Criteria
- Animal-only studies (for clinical synthesis; included in basic science mapping)
- Retracted publications
- Withdrawn clinical trials
- Datasets requiring institutional data use agreements (for initial analyses; may be added later)

### 3.4 Sample Size
Not pre-specified. We analyze all records matching our inclusion criteria from each data source. As of initial baseline (March 15, 2026): approximately 746 unique clinical trials and 15 PubMed monitoring domains.

---

## 4. Variables

### 4.1 Measured Variables

**Literature Analysis:**
- Publication count per domain (single and pairwise)
- Gap score: `max(0, 1 - (pair_count / geometric_mean(d1_count, d2_count))) * 100`
- Cross-domain paper frequency
- Publication volume trends (30-day rolling)

**Clinical Trials:**
- Trial status (recruiting, active, completed, etc.)
- Phase (1, 2, 3, 4, N/A)
- Enrollment count
- Sponsor identity and type (industry, academic, government)
- Intervention type (drug, biological, device, behavioral)
- Start date, completion date, results posting date
- Category assignment (T1D cure, T1D immunotherapy, T2D novel, technology, completed with results)

**Synthesis Metrics:**
- Research Domain Activity Score (composite of publication volume, trial activity, dataset availability)
- Niche Evaluation Score (Data Access × Computational Value × Gap Size × Impact, each 1-5)
- Triple-Source Validation Level (Gold, Silver, Bronze, Unverified)

### 4.2 Indices
- **Gap Score:** Normalized inverse overlap, 0 (fully saturated) to 100 (completely unexplored)
- **Niche Score:** Product of four 1-5 ratings, binned into Tier 1 (16-20), Tier 2 (13-16), Tier 3 (8-12)
- **Evidence Level:** Oxford CEBM Levels 1a-5

---

## 5. Analysis Plan

### 5.1 Statistical Models
This study is primarily descriptive and uses the following analytical approaches:

- **Pairwise gap analysis:** Geometric mean normalization of co-publication counts
- **Trend analysis:** Time-series comparison of trial initiation rates by category (pre/post 2023)
- **Clustering:** Hierarchical clustering of domains by co-publication profile
- **Network analysis:** Domain co-occurrence network with edge weights proportional to co-publication frequency

### 5.2 Transformations
- Publication counts: log-transformed for visualization when distributions are highly skewed
- Gap scores: Capped at 100 (complete gap) and floored at 0 (no gap)
- Enrollment counts: Treated as ordinal when exact counts unavailable

### 5.3 Inference Criteria
We do not perform null hypothesis significance testing for the primary descriptive analyses. For H1-H4, we report observed proportions and confidence intervals. We interpret:
- **H1 supported** if <5% of domain pairs exceed the geometric mean overlap threshold
- **H2 supported** if the proportion of Phase 2-3 T1D curative trials posted after 2023 exceeds the 2018-2022 rate
- **H3 supported** if the top 10 institutions account for >50% of AI/ML diabetes publications
- **H4 supported** if cross-domain papers have higher median citation counts than single-domain papers

### 5.4 Data Exclusion
Records with missing critical fields (no title, no NCT ID) are excluded from analysis but counted in completeness metrics. No outlier removal is performed on publication counts or enrollment figures.

### 5.5 Exploratory Analyses
The following are explicitly marked as exploratory (not pre-registered predictions):
- Drug repurposing candidate identification via network pharmacology
- Multi-omics biomarker integration across public datasets
- Natural language processing of clinical trial descriptions for thematic clustering

---

## 6. Validation Framework

All findings are validated using the triple-source framework defined in our Research Doctrine:

| Level | Requirement | Confidence |
|-------|------------|------------|
| GOLD | 3+ independent sources corroborate | High — actionable |
| SILVER | 2 independent sources | Moderate — report with caveat |
| BRONZE | 1 source only | Low — flag for follow-up |
| UNVERIFIED | No independent validation | Do not publish as finding |

All claims in published outputs carry explicit validation levels. GRADE certainty assessment is applied to synthesized findings. Cochrane Risk of Bias (RoB 2) domains are assessed where applicable.

---

## 7. Scripts and Code

All analysis code is open-source (MIT License) and available in the project repository:

| Script | Purpose |
|--------|---------|
| `project1_literature_gap_analysis.py` | PubMed pairwise domain gap analysis |
| `baseline_clinical_trials.py` | ClinicalTrials.gov snapshot and summary |
| `baseline_pubmed_alerts.py` | PubMed recent publication monitoring |
| `hub_monitor.py` | Research hub file and dataset change tracking |
| `run_all.py` | Master runner for all analysis scripts |

**Runtime environment:** Python 3.10+, standard library only (urllib, json, xml, hashlib, collections). No external dependencies required.

---

## 8. Timeline

| Phase | Dates | Deliverables |
|-------|-------|-------------|
| Baseline data collection | March 2026 | Clinical trial snapshot, PubMed baseline, literature gap matrix |
| Dashboard and visualization | March 2026 | Interactive research dashboard, clinical trial intelligence dashboard |
| OSF registration and GitHub publication | March 2026 | This document, public repository |
| Multi-omics pilot analysis | April 2026 | Biomarker integration analysis |
| T1D landscape comparison | April 2026 | Triple-verified systematic comparison |
| Drug repurposing screen | May 2026 | Network pharmacology analysis |
| First preprint submission | April-May 2026 | bioRxiv/medRxiv preprint |
| Journal submission | May-June 2026 | Open-access journal submission |

---

## 9. Ethics and Data Governance

- No human subjects recruitment or intervention
- All data sourced from publicly accessible databases and APIs
- No personally identifiable information processed
- All analysis code and methods are fully transparent and reproducible
- IRB review is not required for analysis of publicly available, de-identified data
- Outputs are shared under open licenses (MIT for code, CC-BY 4.0 for content)

---

## 10. How to Register This Protocol on OSF

1. Go to [osf.io](https://osf.io) and create a free account
2. Click **"Create new project"** → Title: "Diabetes Research Hub"
3. Add this document as a component: **Components → Create Component → "Pre-Registration Protocol"**
4. Upload all analysis scripts to the project Files section
5. Go to **Registrations → New Registration** → Select **"Open-Ended Registration"** template
6. Paste the content of Sections 1-9 into the registration form
7. Submit for registration (this creates a frozen, timestamped, DOI-bearing record)
8. The DOI can then be cited in all future publications from this project

---

*Pre-registration protocol for the Diabetes Research Hub project*
*Version 1.0 — March 15, 2026*
