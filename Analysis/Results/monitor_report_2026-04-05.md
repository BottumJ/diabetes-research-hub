# Diabetes Research Hub — Monitor Report
**Date:** 2026-04-05
**Scan window:** 2026-04-04 → 2026-04-05
**Report type:** Automated daily review

---

## File System Status

All key data files are **current** (updated today, April 5):

| File | Last Modified | Status |
|------|--------------|--------|
| hub_monitor_report.md | 2026-04-05 02:04 | ✅ Fresh |
| clinical_trials_latest.json | 2026-04-05 02:04 | ✅ Fresh |
| pubmed_recent_latest.json | 2026-04-05 02:04 | ✅ Fresh |
| literature_gap_data.json | 2026-04-03 09:31 | ✅ Fresh (2 days) |
| literature_gap_report.md | 2026-04-04 03:07 | ✅ Fresh (1 day) |

**Hub summary:** 675 files tracked. 5 new files, 28 modified files, 0 removed since last scan. 344 result files older than 14 days (mostly historical snapshots and paper library — expected).

**New files since last scan:**
- clinical_trials_snapshot_2026-04-05.json
- pubmed_recent_snapshot_2026-04-05.json
- monitor_report_2026-04-04.md
- 2 new paper library abstracts (PMIDs 16898223, 41921761)

**All Python scripts are running on schedule — no re-runs needed.**

---

## Clinical Trial Changes

### Snapshot Diff (Apr 4 → Apr 5): No changes

- New trials: 0
- Removed trials: 0
- Status changes: 0
- New results posted: 0

This is a quiet day for trial registry changes (expected on weekends).

### Overall Trial Portfolio

- **754 unique trials** tracked across 5 categories
- T1D Cure & Cell Therapy: 150 | T1D Immunotherapy & Prevention: 71 | T2D Novel Therapies: 136 | Diabetes Technology: 217 | Completed with Results: 253
- **44 Phase 3 RECRUITING trials** actively enrolling

### Key Sponsor Phase 3 Trials (Active)

| NCT ID | Sponsor | Trial | Status |
|--------|---------|-------|--------|
| NCT04786262 | **Vertex** | VX-880 for T1D (stem cell-derived islets) | RECRUITING |
| NCT06832410 | **Vertex** | VX-880 in T1D with kidney transplant | RECRUITING |
| NCT07222137 | **Eli Lilly** | Baricitinib to delay Stage 3 T1D (at-risk) | RECRUITING |
| NCT07222332 | **Eli Lilly** | Baricitinib to preserve beta cells (new-onset T1D) | RECRUITING |
| NCT06993792 | **Eli Lilly** | Orforglipron master protocol (obesity ± T2D) | RECRUITING |
| NCT06972472 | **Eli Lilly** | Orforglipron in obesity + T2D | RECRUITING |
| NCT06739122 | **Eli Lilly** | Dulaglutide 3.0/4.5 mg pediatric T2D | RECRUITING |
| NCT07076199 | **Novo Nordisk** | Insulin Icodec vs Glargine | RECRUITING |
| NCT06260722 | **Eli Lilly** | Retatrutide vs Semaglutide (T2D) | ACTIVE_NOT_RECRUITING |
| NCT06296603 | **Eli Lilly** | Retatrutide vs Placebo (T2D) | ACTIVE_NOT_RECRUITING |
| NCT07088068 | **Sanofi** | Teplizumab in pediatric T1D | RECRUITING |

**Notable Eli Lilly Phase 2 additions in pipeline:**
- LY3457263 (T2D + cardiorenal) — RECRUITING
- LY3938577 (T2D, insulin-experienced) — RECRUITING
- Macupatide + Eloralintide combo (diabetic retinopathy) — RECRUITING

---

## PubMed Highlights

### Publication Volume (Last 30 Days)

| Activity Level | Domains |
|----------------|---------|
| **HIGH** (>100 papers) | Diabetes AI/ML (172), T2D GLP-1 New (149), Diabetes Microbiome (143), Diabetes Biomarker (119) |
| **HIGH** (>50) | Diabetes Health Equity (68) |
| **ACTIVE** (20-50) | Multi-Omics (47), T2D Remission (42), Complications (37), Gene Therapy (36), T1D Immunotherapy (22) |
| **LOW** (<10) | Drug Repurpose (5), Epigenetics (5), LADA (5) |

### Snapshot Diff (Apr 4 → Apr 5): 6 new papers, 6 dropped (rolling window)

**New papers today:**
1. PMID 41933490 [T1D Immunotherapy] — Psychosocial implications of general population screening for paediatric T1D
2. PMID 41933482 [Diabetes AI/ML] — Improving Diabetic Foot Care With Infrared Thermography and AI
3. PMID 41933721 [Diabetes Gene Therapy] — NAA25 as regulator of insulin signaling (FOXO1 CRISPRi screen + Mendelian Randomization)
4. PMID 41933665 [T2D Remission] — Immunometabolic dysregulation drives selective cognitive dysfunction in db/db mice
5. PMID 41933465 [T2D Remission] — Electroacupuncture ameliorates colonic mucosal barrier damage in T2DM rats
6. PMID 41933839 [T2D Remission] — Maternal Nutrition and Hypothalamic Programming of Offspring Metabolic Health

### Cross-Domain Papers (7 total — Highest Priority)

| PMID | Domains | Title | Priority |
|------|---------|-------|----------|
| 41930333 | Biomarker + Microbiome | Microbiome-Based Clustering Identifies Glycemic Control-Related Subtypes in Youth With Recent-Onset T1D | ⭐ HIGH — aligns with Microbiome ML pipeline |
| 41931049 | GLP-1 + Microbiome | GLP-1 Receptor Agonists (NEJM review) | ⭐ HIGH — major review, likely highly cited |
| 41928460 | Remission + AI/ML | Interpretable ML in T2D prediction + Mendelian randomization | Methodological template |
| 41872174 | Stem Cell + Immunotherapy | Antigen-specific immunotherapy with CD4 | Cross-cutting T1D cure |
| 41907858 | Remission + Multi-Omics | Oral and cardiometabolic health through biobanks | Multi-omics methodology |
| 41921761 | Biomarker + Microbiome | Oral-gut microbiome axis in diabetes (systematic review) | Microbiome pipeline relevant |
| 41921728 | Biomarker + Complications | Novel biomarkers for diabetic retinopathy | Complications track |

### Key Therapy Mentions
- **Teplizumab** — PMID 41913320: "Toward Personalized Medicine in Type 1 Diabetes: Understanding How Patient Heterogeneity Influences Therapeutic Efficacy" (relevant to teplizumab sNDA prep)
- No new papers mentioning zimislecel, orforglipron, retatrutide, CagriSema, or baricitinib by name in titles/abstracts this cycle

---

## Gap Analysis Summary

**Analysis date:** 2026-04-03 | 30 domains, 435 pairs analyzed | Validation: BRONZE

### Top 5 Under-Researched Intersections

| Rank | Domain 1 | Domain 2 | Gap Score | Joint Pubs | Tier 1 Alignment |
|------|----------|----------|-----------|------------|------------------|
| 1 | Beta Cell Regen | Health Equity | 100.0 | 0 | Tier 1 (Epidemiology) |
| 2 | Insulin Resistance | Islet Transplant | 100.0 | 1 | Tier 1 (Multi-Omics) |
| 3 | Islet Transplant | GWAS/Polygenic | 100.0 | 0 | Tier 1 (AI/ML) |
| 4 | Islet Transplant | Personalized Nutr | 100.0 | 0 | — |
| 5 | Islet Transplant | Drug Repurposing | 100.0 | 0 | **Tier 1 — Active project** |

**Key alignment:** Gap #5 (Islet Transplant × Drug Repurposing) continues to validate our active Islet Drug Repurposing pipeline. The gap analysis data is unchanged since April 3 — consider refreshing in 4-5 days.

Additional Tier 1-aligned gaps in top 15:
- Gene Therapy × LADA (rank 9, 0 joint pubs)
- Drug Repurposing × Health Equity (rank 12, 0 joint pubs)
- Drug Repurposing × LADA (rank 13, 0 joint pubs)
- Health Equity × LADA (rank 14, 0 joint pubs)

---

## Breaking News (Web Search — Last 7 Days)

### 🔴 UPDATE: Foundayo (Orforglipron) — Now Available via LillyDirect

Eli Lilly's oral GLP-1 receptor agonist **orforglipron (Foundayo)**, approved April 1, began shipping via LillyDirect on April 6. Key facts:
- First oral GLP-1 pill for weight management with no meal/water timing restrictions
- Fastest NME approval since 2002 (50-day review under Priority Voucher program)
- Highest dose achieved ~12% body weight loss over 72 weeks vs 0.9% placebo
- Our tracker includes active Lilly orforglipron trials: NCT06993792, NCT06972472

**Action needed:** Tracker should already reflect the April 1 approval (flagged in yesterday's report). Verify this has been updated.

### 🟡 Awiqli (Insulin Icodec) — FDA Approved, US Launch H2 2026

Novo Nordisk's once-weekly basal insulin **Awiqli** was approved March 26 for adults with T2D. US launch now expected in H2 2026 (not April as earlier projected). Our tracker includes the Phase 3 trial NCT07076199.

### 🟡 Q2 2026 FDA Decisions to Watch
- **Afrezza pediatric sBLA** (MannKind) — May 2026 PDUFA; first needle-free insulin for ages 4-17
- **Portal Diabetes insulin pump** — received FDA Breakthrough Device designation (March 2026)
- Retatrutide FDA approval market prediction: ~27% for 2026

---

## Recommended Actions

### Immediate
1. **Verify Foundayo (orforglipron) tracker update** — Confirm the April 1 FDA approval has been recorded in Diabetes_Research_Tracker.xlsx with indication, brand name, and links to active trials.
2. **Add Awiqli (insulin icodec) approval to tracker** — March 26 FDA approval; H2 2026 US launch expected; link NCT07076199.

### This Week
3. **Review cross-domain paper PMID 41930333** — "Microbiome-Based Clustering in Youth T1D" directly aligns with the Microbiome ML pipeline. Compare their clustering approach and datasets with our feature matrix.
4. **Review NEJM GLP-1 review PMID 41931049** — Major review article; extract key claims for the evidence network.
5. **Review new gene therapy paper PMID 41933721** — NAA25/FOXO1 CRISPRi screen with Mendelian Randomization integration; novel methodology for insulin signaling research.
6. **Review teplizumab personalized medicine paper PMID 41913320** — Relevant to teplizumab sNDA decision prep and patient heterogeneity analysis.

### Data Refresh Schedule
7. **All feeds current — no script re-runs needed today.**
8. **Re-run gap analysis by April 8** to capture any publication shifts: `python project1_literature_gap_analysis.py`
9. **Monitor Afrezza pediatric decision** — add May 2026 PDUFA date to watchlist.

---

*Generated by Diabetes Research Hub automated monitor — 2026-04-05*
*Evidence standards: per RESEARCH_DOCTRINE v1.1*
