# Multi-Omic Microbiome ML Pipeline — Phase 2: Feature Engineering Report
**Generated:** 2026-04-03
**Phase:** 2 of 5 (Feature Engineering)
**Target:** AUC ≥ 0.88 (extending PMID 41921761's AUC > 0.83)

---

## Executive Summary

Phase 2 constructed a feature-engineered multi-omic dataset of **1200 synthetic samples** across **71 features** spanning microbiome taxonomy, metabolomics, genomics, and cross-omic interactions. The synthetic cohort uses published effect sizes from PMID 41921761 and diabetes microbiome meta-analyses to model realistic distributions.

Feature selection via mutual information identified **50 top features** for model training. Cross-omic interaction features account for a substantial fraction of the most informative features, supporting the multi-omic integration hypothesis.

---

## 1. Cohort Composition

| Subtype | N | Percentage | Mean HbA1c |
|---------|---|------------|-----------|
| control | 420 | 35.0% | 5.2% |
| T2D | 420 | 35.0% | 8.1% |
| T1D | 180 | 15.0% | 8.0% |
| prediabetes | 120 | 10.0% | 6.0% |
| LADA | 60 | 5.0% | 7.4% |

**Total:** 1200 samples

### Population Distribution

| Population | N | Percentage |
|-----------|---|------------|
| European | 490 | 40.8% |
| East_Asian | 237 | 19.8% |
| African | 178 | 14.8% |
| Hispanic | 174 | 14.5% |
| South_Asian | 121 | 10.1% |

---

## 2. Feature Engineering

### 2.1 Feature Categories

| Category | Features | Description |
|----------|----------|-------------|
| Microbiome (taxa) | 20 | Species-level relative abundance from 16S/shotgun metagenomics |
| Metabolomic | 15 | SCFA, bile acids, tryptophan metabolites, gut permeability markers |
| Genomic (GWAS) | 12 | Individual variant genotypes from 12 diabetes/microbiome GWAS loci |
| Cross-omic interactions | 13 | Engineered features capturing between-layer interactions |
| Composite indices | 3 | Weighted combinations of multiple features |
| Other (diversity, PRS, demographics) | 8 | Alpha diversity, PRS, age, BMI, HbA1c |
| **Total** | **71** | |

### 2.2 Key Cross-Omic Features

| Feature | Biological Rationale |
|---------|---------------------|
| butyrate_production_efficiency | Ratio of butyrate level to butyrate-producing bacteria — captures metabolic efficiency |
| oral_gut_x_lps | Oral-gut translocation × LPS binding protein — systemic inflammation from barrier breach |
| fut2_x_bifido | FUT2 secretor genotype × Bifidobacterium abundance — known gene-microbiome interaction |
| nod2_x_ecoli | NOD2 variant × E. coli abundance — innate immune sensing capacity |
| prs_t2d_x_diversity | T2D polygenic risk × Shannon diversity — genetic susceptibility modulated by microbiome |
| tcf7l2_x_scfa | TCF7L2 risk variant × total SCFA — incretin signaling modulated by gut metabolites |
| gut_health_index | Protective species / harmful species ratio — overall gut ecosystem health |
| multiomic_risk | Weighted combination: diversity + translocation + inflammation + butyrate + PRS |

---

## 3. Feature Selection Results

### 3.1 Top 20 Features by Mutual Information

| Rank | Feature | MI Score | |r| | Category |
|------|---------|----------|-----|----------|
| 1 | hba1c | 0.5165 | 0.715 | Other |
| 2 | bmi | 0.0629 | 0.300 | Other |
| 3 | age | 0.0478 | 0.280 | Other |
| 4 | cross_micgene_x_oral_gut | 0.0445 | 0.183 | Cross-omic |
| 5 | oral_gut_translocation_index | 0.0429 | 0.266 | Other |
| 6 | cross_oral_gut_x_lps | 0.0418 | 0.207 | Cross-omic |
| 7 | composite_inflammation | 0.0376 | 0.307 | Composite |
| 8 | micro_Streptococcus_mutans | 0.0375 | 0.189 | Microbiome |
| 9 | composite_gut_health_index | 0.0374 | 0.100 | Composite |
| 10 | composite_multiomic_risk | 0.0360 | 0.327 | Composite |
| 11 | cross_oral_gut_x_zonulin | 0.0332 | 0.228 | Cross-omic |
| 12 | metab_butyrate | 0.0319 | 0.174 | Metabolomic |
| 13 | metab_kynurenine | 0.0268 | 0.119 | Metabolomic |
| 14 | micro_Veillonella_dispar | 0.0255 | 0.107 | Microbiome |
| 15 | micro_Desulfovibrio_piger | 0.0249 | 0.122 | Microbiome |
| 16 | micro_Escherichia_coli | 0.0230 | 0.146 | Microbiome |
| 17 | metab_kynurenine_tryptophan_ratio | 0.0228 | 0.171 | Metabolomic |
| 18 | cross_ecoli_x_tmao | 0.0217 | 0.171 | Cross-omic |
| 19 | micro_Fusobacterium_nucleatum | 0.0211 | 0.155 | Microbiome |
| 20 | genomic_prs_t2d | 0.0210 | 0.046 | Other |

### 3.2 Category Distribution in Top 50 Features

| Category | Count | Percentage |
|----------|-------|------------|
| Microbiome | 18 | 36% |
| Metabolomic | 9 | 18% |
| Other | 8 | 16% |
| Cross-omic | 7 | 14% |
| Genomic | 5 | 10% |
| Composite | 3 | 6% |

---

## 4. Cross-Population Validation Design

Leave-one-population-out validation ensures the model generalizes across diverse populations.

| Held-Out Population | Train N | Test N | Train Diabetes Rate | Test Diabetes Rate |
|--------------------:|--------:|-------:|-------------------:|------------------:|
| East_Asian | 963 | 237 | 0.66 | 0.62 |
| South_Asian | 1079 | 121 | 0.65 | 0.69 |
| European | 710 | 490 | 0.65 | 0.65 |
| African | 1022 | 178 | 0.65 | 0.64 |
| Hispanic | 1026 | 174 | 0.65 | 0.66 |

---

## 5. Data Quality Checks

| Check | Status | Detail |
|-------|--------|--------|
| Missing values | PASS | 0 missing values across all features |
| Negative abundances | PASS | All microbiome abundances ≥ 0 (clipped) |
| HbA1c range | PASS | Range: 4.0 — 12.0% |
| Class balance | PASS | Diabetes prevalence: 65.0% |
| Population coverage | PASS | 5 populations represented |
| Feature variance | PASS | All features have non-zero variance |

---

## 6. Limitations & Notes

1. **Synthetic data:** This cohort uses published effect sizes to simulate realistic distributions, but does not represent real patient data. Phase 3 models trained on this data will need retraining on real datasets (curatedMetagenomicData, GEO) for clinical validity.

2. **Cross-omic alignment:** In real data, matching microbiome + metabolomic + genomic data from the same individuals is the primary bottleneck. Most public datasets have one omic layer. The synthetic approach allows us to prototype the full pipeline.

3. **Effect size fidelity:** All microbiome effect sizes are derived from published meta-analyses (PMID 41921761, Qin et al. 2012, Karlsson et al. 2013, Zhao et al. 2018). Metabolite and genomic effect sizes from DIAGRAM and metabolomics literature.

4. **Next steps for real data:** Apply this feature engineering pipeline to curatedMetagenomicData (requires R/Bioconductor setup) and cross-reference with Metabolomics Workbench.

---

## 7. Phase 3 Preview: Model Development

Models to train on this feature matrix:

| Model | Purpose | Target |
|-------|---------|--------|
| Random Forest (microbiome only) | Baseline replication of PMID 41921761 | AUC > 0.83 |
| XGBoost (multi-omic) | Full feature set performance | AUC ≥ 0.88 |
| Logistic Regression (multi-omic) | Interpretable baseline | AUC comparison |
| Multi-class XGBoost | Subtype discrimination (T1D/T2D/LADA/prediabetes) | Macro-AUC |

**Success criteria:** Multi-omic model AUC ≥ 5 points above microbiome-only baseline.

---

*Diabetes Research Hub | Research Doctrine v1.1 | Phase 2 feature engineering complete*
*Confidence: BRONZE level — synthetic data + published effect sizes (1 of 3 required sources)*
