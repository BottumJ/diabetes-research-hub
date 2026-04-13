# Diabetes Research Hub — Monitor Report
**Date:** 2026-04-04
**Scan window:** 2026-04-03 → 2026-04-04
**Report type:** Automated daily review

---

## File System Status

All key data files are **current** (updated within the last 24 hours):

| File | Last Modified | Status |
|------|--------------|--------|
| hub_monitor_report.md | 2026-04-04 02:05 | ✅ Fresh |
| clinical_trials_latest.json | 2026-04-04 02:04 | ✅ Fresh |
| pubmed_recent_latest.json | 2026-04-04 02:05 | ✅ Fresh |
| literature_gap_data.json | 2026-04-03 09:31 | ✅ Fresh (1 day) |
| literature_gap_report.md | 2026-04-03 09:31 | ✅ Fresh (1 day) |

**Hub summary:** 670 files tracked. 30 new files, 31 modified files, 0 removed since last scan. 334 result files older than 14 days (mostly historical snapshots and paper library — expected).

**New project outputs since last report:**
- Islet Drug Repurposing pipeline (Phase 1-3 scripts + reports + network analysis + dashboard)
- Microbiome ML pipeline (Phase 1-3 scripts + feature matrix + model results)
- Teplizumab sNDA decision prep document
- Enriched literature gap report
- Cross-domain paper review (2026-04-03)

---

## Clinical Trial Changes

### Snapshot Diff (Apr 3 → Apr 4): 4 new, 1 removed, 0 status changes

**New trials added:**
- **NCT07509060** — HCL in Adults With T1DM, Markedly Elevated HbA1c, and Psychological Vulnerability (ACTIVE_NOT_RECRUITING)
- **NCT07510386** — CGM After Discharge From Hospital (NOT_YET_RECRUITING) — Icahn School of Medicine at Mount Sinai
- **NCT01633177** — Study of Vitamin D and Omega-3 Supplementation for Preventing Diabetes (COMPLETED, Phase 3) — Brigham and Women's Hospital
- **NCT04663061** — Diabetes Data-Assisted Remission Trial / DDART (COMPLETED) — Wake Forest University

**Removed:**
- NCT06235086 — TG103 Injection + Metformin for T2D (likely status change made it fall outside query window)

### Key Phase 3 Recruiting Trials (from key sponsors)

| NCT ID | Sponsor | Trial | Notes |
|--------|---------|-------|-------|
| NCT04786262 | **Vertex** | VX-880 for T1D | Flagship stem cell–derived islet therapy |
| NCT06832410 | **Vertex** | VX-880 in T1D with kidney transplant | Extension cohort |
| NCT07076199 | **Novo Nordisk** | Insulin Icodec vs Glargine | Once-weekly insulin |
| NCT07222137 | **Eli Lilly** | Baricitinib to delay Stage 3 T1D | Disease modification (at-risk) |
| NCT07222332 | **Eli Lilly** | Baricitinib to preserve beta cells (new-onset T1D) | Disease modification |
| NCT06993792 | **Eli Lilly** | Orforglipron master protocol (obesity ± T2D) | Oral GLP-1 |
| NCT06972472 | **Eli Lilly** | Orforglipron in obesity + T2D | Oral GLP-1 |
| NCT06739122 | **Eli Lilly** | Dulaglutide 3.0/4.5 mg in pediatric T2D | AWARD-PEDS PLUS |

**No new results posted** since last snapshot.

### Overall Trial Portfolio
- **754 unique trials** tracked across 5 categories
- 260 RECRUITING | 253 COMPLETED | 127 NOT_YET_RECRUITING | 108 ACTIVE_NOT_RECRUITING
- 115 Phase 3 trials | 122 Phase 2 trials
- Top sponsors: Eli Lilly (27), Novo Nordisk (23), Medtronic (10), Insulet (9)

---

## PubMed Highlights

### Publication Volume (Last 30 Days)
**High-activity domains:** Diabetes AI/ML (176), T2D GLP-1 New (152), Diabetes Microbiome (147), Diabetes Biomarker (119), Health Equity (72)
**Low-activity domains:** Drug Repurpose (5), Epigenetics (5), LADA (5)

### Snapshot Diff (Apr 3 → Apr 4): 22 new papers, 23 dropped (rolling window)

### Cross-Domain Papers (Highest Priority)

These papers span multiple research domains — high synthesis value:

1. **"Interpretable machine learning in type-2 diabetes prediction in patients with depressive symptoms"** (PMID 41928460)
   - Domains: T2D Remission + Diabetes AI/ML
   - Combines Mendelian randomization with ML; potential methodological template

2. **"Microbiome-Based Clustering Identifies Glycemic Control-Related Subtypes in Youth With Recent-Onset T1D"** (PMID 41930333)
   - Domains: Diabetes Biomarker + Diabetes Microbiome
   - **HIGH RELEVANCE:** Directly aligns with our Microbiome ML pipeline and Tier 2 microbiome research

3. **"GLP-1 Receptor Agonists" (NEJM review)** (PMID 41931049)
   - Domains: T2D GLP-1 New + Diabetes Microbiome
   - Major NEJM review article; likely to be highly cited

4. **"The oral-gut microbiome axis in diabetes mellitus"** (PMID 41921761)
   - Domains: Diabetes Biomarker + Diabetes Microbiome

5. **"Novel biomarkers for early diagnosis and treatment strategies of diabetic retinopathy"** (PMID 41921728)
   - Domains: Diabetes Biomarker + Diabetes Complications New

6. **"Antigen-specific immunotherapy with a CD4..."** (PMID 41872174)
   - Domains: T1D Stem Cell Cure + T1D Immunotherapy

7. **"Oral and cardiometabolic health through the lens of biobanks"** (PMID 41907858)
   - Domains: T2D Remission + Diabetes Multi-Omics

### Key Therapy Mentions
No new papers in this cycle specifically mentioning zimislecel, orforglipron, retatrutide, CagriSema, baricitinib, or teplizumab by name in titles. (Note: the NEJM GLP-1 review likely covers orforglipron in the body text.)

### Notable Individual Papers
- **Epigenetic control of PDX1 and NGN3 by a computationally designed PRC2 inhibitor** — enforces pancreatic endocrine differentiation from pluripotent stem cells (PMID 41928786). Relevant to beta cell regeneration.
- **Alpha-1 Antitrypsin Overexpressing MSCs Promote Tregs to Reverse Diabetes** (PMID 41918165) — relevant to immunotherapy pipeline.
- **Tirzepatide dose-response and acute pancreatitis meta-analysis** (PMID 41927408) — safety signal monitoring for GLP-1/GIP class.

---

## Gap Analysis Summary

**Analysis date:** 2026-04-03 | 30 domains, 435 pairs analyzed

### Top 5 Under-Researched Intersections (Gap Score: 100/100)

| Rank | Domain 1 | Domain 2 | Joint Pubs | Expected | Alignment with Tier 1 |
|------|----------|----------|------------|----------|----------------------|
| 1 | Beta Cell Regen | Health Equity | 0 | 1,603 | Tier 1 (Epidemiology) |
| 2 | Insulin Resistance | Islet Transplant | 1 | 2,116 | Tier 1 (Multi-Omics) |
| 3 | Islet Transplant | GWAS/Polygenic | 0 | 1,093 | Tier 1 (AI/ML Predict) |
| 4 | Islet Transplant | Personalized Nutr | 0 | 375 | — |
| 5 | Islet Transplant | Drug Repurposing | 0 | 369 | **Tier 1 (Drug Repurposing)** ← Active project |

**Key alignment note:** Gap #5 (Islet Transplant × Drug Repurposing) directly aligns with the new Islet Drug Repurposing pipeline that was just completed. This validates our project selection.

Other notable gaps aligning with Tier 1 priorities:
- Drug Repurposing × LADA (rank 24, 0 joint pubs) — aligns with Tier 1 Drug Repurposing
- GWAS/Polygenic × CGM Technology (rank 8, 2 joint pubs vs 5,556 expected) — aligns with Tier 1 AI/ML

---

## Breaking News (Web Search — Last 7 Days)

### 🔴 MAJOR: Orforglipron (Foundayo) FDA Approval — April 1, 2026
Eli Lilly's oral GLP-1 receptor agonist **orforglipron** (brand name **Foundayo**) received FDA approval on April 1, 2026 for obesity/overweight with weight-related conditions. In trials, the highest dose achieved ~12% body weight loss over 72 weeks. This is the first oral GLP-1 pill approved for weight management — a landmark for the class.

**Relevance:** Our tracker includes multiple Lilly orforglipron trials (NCT06993792, NCT06972472). This approval may trigger expanded Phase 3 trials for T2D-specific indications.

### Upcoming: Afrezza Pediatric Decision — May 2026
The FDA will decide on MannKind's sBLA for **inhaled insulin (Afrezza) in pediatric patients ages 4–17**, based on the Phase 3 INHALE-1 study. If approved, this would be the first needle-free insulin for children.

### Other Notable:
- **Insulin Icodec (Awiqli)** — once-weekly insulin from Novo Nordisk — scheduled for release in Q2 2026
- **MUSC receives $1M from Breakthrough T1D** for lab-made insulin-producing cells + engineered protective immune cells strategy
- ADA released **Standards of Care in Diabetes — 2026**
- Retatrutide FDA approval market prediction sits at 27% for 2026

---

## Recommended Actions

### Immediate (Today)
1. **Update tracker with Foundayo (orforglipron) FDA approval** — This is a Tier 1 event. Add approval date, indication, and link to Lilly's related recruiting trials.
2. **Review cross-domain paper: "Microbiome-Based Clustering Identifies Glycemic Control-Related Subtypes in Youth With Recent-Onset T1D" (PMID 41930333)** — Directly relevant to the Microbiome ML pipeline. Check if their clustering approach or datasets overlap with or complement our feature matrix.
3. **Review the NEJM GLP-1 Receptor Agonists review (PMID 41931049)** — Major review article; extract key claims for evidence network.

### This Week
4. **Review Islet Drug Repurposing pipeline outputs** — The islet_repurposing_network_report.md and validation report are new; confirm alignment with Gap #5 (Islet Transplant × Drug Repurposing).
5. **Review Microbiome ML Phase 3 model results** — microbiome_ml_model_results.json and phase3 report are new; assess model performance and next steps.
6. **Monitor Afrezza pediatric FDA decision** — Expected May 2026; add to watchlist.

### Data Refresh Needed
7. All primary data feeds (clinical trials, PubMed, gap analysis) are current — **no script re-runs needed today.**
8. Consider re-running gap analysis in ~1 week to capture any shifts from new publications.

---

*Generated by Diabetes Research Hub automated monitor — 2026-04-04*
*Evidence standards: per RESEARCH_DOCTRINE v1.1*
