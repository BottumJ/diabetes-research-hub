# Research Plan: Multi-Omic Microbiome ML Diagnostic Pipeline
**Inspired by:** PMID 41921761 — "The oral-gut microbiome axis in diabetes mellitus"
**Tier 1 Alignment:** AI/ML Prediction Model Development (18/20) + Multi-Omics Biomarker Integration (19/20)
**Date:** 2026-04-03
**Status:** PROPOSED — Requires review before execution

---

## 1. Problem Statement

PMID 41921761 (Nee et al., Diabetes Research and Clinical Practice, 2026) demonstrated that machine learning models using combined oral-gut microbiome signatures can diagnose diabetes with AUC >0.83. This represents a clinically meaningful threshold — but the study has limitations we can address:

1. **Single-axis focus:** Only microbiome data used; no integration with genomic, proteomic, or metabolomic layers
2. **Binary classification:** Diabetes vs. no diabetes; doesn't distinguish subtypes (T1D, T2D, LADA, gestational)
3. **Limited population diversity:** Unclear whether models generalize across populations
4. **No public pipeline:** Methods described but code not publicly available for replication

**Our research question:** Can we build an open, reproducible multi-omic pipeline that extends the oral-gut microbiome diagnostic approach by integrating additional omic layers and testing across diverse populations?

This directly serves two Tier 1 areas simultaneously — the highest-value overlap in our Research Doctrine.

---

## 2. What PMID 41921761 Established

| Finding | Detail | Evidence Level |
|---------|--------|---------------|
| Oral-gut axis disruption | Oral bacteria (Streptococcus, Prevotella) detected in gut samples of diabetes patients | 1a (systematic review) |
| Shared metabolic pathways | Inflammation and insulin resistance pathways disrupted in both compartments | 1a |
| ML diagnostic model | AUC >0.83 using combined oral-gut microbiome features | 2b (model development) |
| HbA1c correlation | Microbiome signatures correlate with HbA1c levels | 2b |

**What's missing:** Cross-omic integration, subtype discrimination, population validation, open-source tooling.

---

## 3. Data Sources

### Publicly Available Microbiome Datasets

| Dataset | What | Size | Access |
|---------|------|------|--------|
| **Human Microbiome Project (HMP)** | Reference microbiomes + disease associations | 4,788 samples | Free via portal.hmpdacc.org |
| **curatedMetagenomicData** (Bioconductor) | Curated metagenomic profiles from 50+ studies | >20,000 samples | Free R/Python package |
| **GMrepo** | Curated gut microbiome database with phenotype data | 58,000+ samples | Free API |
| **MicrobiomeDB** | Integrated microbiome studies with metadata | Multiple studies | Free |

### Multi-Omic Integration Layers

| Layer | Source | Diabetes Relevance |
|-------|--------|-------------------|
| **Genomic (GWAS)** | DIAGRAM Consortium, T1D/T2D Knowledge Portals | Risk variants affecting microbiome-host interactions |
| **Proteomic** | UK Biobank Proteomics (Olink), Human Protein Atlas | Inflammatory markers, gut barrier proteins |
| **Metabolomic** | Metabolomics Workbench, HMDB | Short-chain fatty acids, bile acids, tryptophan metabolites |
| **Transcriptomic** | GEO (Gene Expression Omnibus) | Gut epithelial gene expression in diabetes |

### Population Diversity Sources

| Population | Dataset | Value |
|-----------|---------|-------|
| Multi-ethnic US | All of Us Research Program | Diverse population microbiome data |
| East Asian | China National GeneBank | Cross-population validation |
| European | MetaHIT | European reference microbiomes |
| African | H3Africa | Under-represented population data |

---

## 4. Methodology

### Phase 1: Data Acquisition & Harmonization (Week 1-3)

**Goal:** Assemble a multi-omic dataset linking microbiome profiles with diabetes status and covariates.

**Steps:**
1. Download curated metagenomic profiles from curatedMetagenomicData, filtering for studies with diabetes phenotype data
2. Harmonize taxonomic annotations to a common reference (GTDB or NCBI taxonomy)
3. Download matched metabolomic data from Metabolomics Workbench (SCFA, bile acid profiles)
4. Pull GWAS summary statistics from DIAGRAM for diabetes risk loci known to affect gut biology (FUT2, NOD2, IL-23R etc.)
5. Build a unified sample × feature matrix with microbiome + metabolomic + genomic features

**Output:** Harmonized multi-omic dataset with metadata (diabetes status, subtype, demographics)

**Python tools:** `pandas`, `biom-format`, `scikit-bio`, `requests`

### Phase 2: Feature Engineering (Week 3-4)

**Goal:** Extract meaningful cross-omic features that capture microbiome-metabolism-genetics interactions.

**Steps:**
1. **Microbiome features:** Species abundance, alpha/beta diversity, oral-associated species in gut (replicating PMID 41921761's approach)
2. **Metabolomic features:** SCFA ratios, bile acid profiles, tryptophan pathway metabolites
3. **Genomic features:** Polygenic risk scores for T1D/T2D from public GWAS, variant burden in microbiome-interaction genes
4. **Cross-omic features:** Microbiome species × metabolite correlations, species × genetic variant interactions
5. Feature selection via mutual information + LASSO to reduce dimensionality

**Output:** Feature matrix with single-omic and cross-omic features, feature importance rankings

### Phase 3: Model Development (Week 4-6)

**Goal:** Build and validate diagnostic/subtyping models.

**Models to test:**
1. **Baseline (replication):** Microbiome-only random forest (target: AUC >0.83 matching PMID 41921761)
2. **Extended:** Multi-omic random forest, gradient boosting (XGBoost), and logistic regression
3. **Deep integration:** Multi-modal neural network with separate encoders per omic layer
4. **Subtype model:** Multi-class classifier (T1D vs. T2D vs. LADA vs. control)

**Validation strategy:**
- 5-fold cross-validation within each dataset
- Leave-one-study-out cross-validation (key test: does the model generalize?)
- Cross-population validation (train on one population, test on another)

**Key metrics:** AUC-ROC, AUC-PR, sensitivity, specificity, calibration plots

**Python tools:** `scikit-learn`, `xgboost`, `pytorch` (for neural network), `shap` (interpretability)

### Phase 4: Interpretability & Biological Validation (Week 6-7)

**Goal:** Ensure results are biologically meaningful, not just statistically significant.

**Steps:**
1. SHAP analysis for feature importance across all models
2. Map top features to known biological pathways using Reactome/KEGG
3. Cross-reference top microbiome features with existing T1D/T2D literature
4. Check if multi-omic model identifies features invisible to single-omic analysis (the key value proposition)
5. Validate that top features are consistent across populations

**Output:** Interpretability report with biological pathway mapping

### Phase 5: Open Pipeline & Dashboard (Week 7-8)

**Goal:** Package as reproducible, open-source pipeline with interactive results.

**Steps:**
1. Package all code as a Python module with clear API
2. Write Jupyter notebooks for each phase (reproducibility)
3. Build interactive HTML dashboard showing: model performance comparison, feature importance, population generalization
4. Prepare methods section following TRIPOD guidelines for prediction model reporting

**Output:** Code repository + dashboard + methods documentation

---

## 5. Expected Deliverables

| Deliverable | Format | Location |
|-------------|--------|----------|
| Harmonized multi-omic dataset | Parquet/CSV | Analysis/Results/ |
| Feature engineering pipeline | Python scripts | Analysis/Scripts/ |
| Trained models + evaluation | Pickle + JSON metrics | Analysis/Results/ |
| SHAP interpretability report | Markdown + figures | Analysis/Results/ |
| Interactive dashboard | HTML | Dashboards/ |
| Reproducibility notebooks | Jupyter (.ipynb) | Analysis/Scripts/ |
| Methods documentation (TRIPOD) | Markdown | Analysis/Results/ |

---

## 6. Technical Requirements

### Python Environment
```
pandas>=1.5
scikit-learn>=1.2
xgboost>=1.7
shap>=0.42
matplotlib>=3.6
seaborn>=0.12
biom-format>=2.1
scikit-bio>=0.5
requests>=2.28
pytorch>=2.0  # optional, for deep learning models
openpyxl
```

### Compute Requirements
- Standard laptop for Phases 1-2, 4-5
- GPU recommended for Phase 3 neural network (optional — tree-based models work on CPU)
- Disk: ~5-10 GB for microbiome datasets
- Primary bottleneck: dataset download and harmonization

### Data Access
- All Tier 1 sources are free and public
- UK Biobank Proteomics requires application (6-8 week approval)
- All of Us requires registration (free for researchers)

---

## 7. Success Criteria

| Criterion | Target | Rationale |
|-----------|--------|-----------|
| Replication | AUC ≥0.80 on microbiome-only model | Validates PMID 41921761 approach |
| Multi-omic improvement | AUC ≥0.88 (≥5 point gain over single-omic) | Justifies multi-omic integration effort |
| Cross-population generalization | AUC ≥0.75 on held-out population | Clinically meaningful generalization |
| Subtype discrimination | AUC ≥0.70 for T1D vs. T2D | Novel contribution beyond binary classification |
| Novel features | ≥3 cross-omic features not in top-20 of any single-omic model | Demonstrates value of integration |

---

## 8. Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Insufficient matched multi-omic data | Medium | Start with microbiome + metabolomics (best overlap); add genomics as available |
| Overfitting to small datasets | High | Strict cross-validation; leave-one-study-out; no test set peeking |
| Cross-population performance drops significantly | High | Expected — document honestly; analyze which features transfer |
| Results don't improve on single-omic baseline | Medium | Still valuable — negative result establishes the boundary of microbiome-only approaches |
| Compute limitations for neural network | Low | Fall back to XGBoost (comparable performance in tabular settings) |

---

## 9. Research Doctrine Compliance

| Requirement | How We Comply |
|-------------|---------------|
| Evidence levels | Model outputs labeled Level 4 (computational); systematic review replication is Level 1a |
| Source recording | All datasets documented with accession IDs, download dates, versions |
| Reproducibility | Jupyter notebooks + requirements.txt + random seeds |
| Confidence tags | Model predictions tagged with calibrated confidence intervals |
| Limitations | Explicitly state: in silico validation only; prospective clinical validation required |
| TRIPOD compliance | Methods section follows TRIPOD checklist for prediction model studies |

---

## 10. Connection to Gap Analysis

This pipeline addresses multiple gaps from our analysis:

| Gap | How This Helps |
|-----|---------------|
| Microbiome Gut × Drug Repurposing (99.9) | Microbiome signatures could identify drug-responsive subtypes |
| Autoimmunity T1D × Personalized Nutr (99.9) | Microbiome-guided nutrition for autoimmune patients |
| Health Equity × LADA (100.0) | Cross-population validation directly addresses equity |
| Epigenetics × LADA (99.9) | Multi-omic approach could integrate epigenetic markers for LADA detection |

---

## 11. Timeline

| Week | Phase | Key Milestone |
|------|-------|---------------|
| 1-3 | Data Acquisition | Multi-omic dataset assembled |
| 3-4 | Feature Engineering | Cross-omic features computed |
| 4-6 | Model Development | Models trained and validated |
| 6-7 | Interpretability | SHAP analysis and pathway mapping complete |
| 7-8 | Packaging | Dashboard and documentation published |

**Total estimated duration:** 8 weeks
**Can begin immediately:** Yes — curatedMetagenomicData and Metabolomics Workbench are freely downloadable today

---

## 12. Next Step

**To begin Phase 1, run:**
```bash
python Analysis/Scripts/project_microbiome_ml_phase1_data.py
```
*(Script to be created upon approval of this plan)*

---

*Prepared by Diabetes Research Hub | Research Doctrine v1.1*
*Paper Reference: PMID 41921761 — Nee et al., Diabetes Research and Clinical Practice (2026)*
*Tier 1 Areas: AI/ML Prediction (18/20) + Multi-Omics Biomarker Integration (19/20)*
