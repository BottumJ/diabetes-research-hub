# Diabetes Research Hub — Monitor Report
**Generated:** 2026-04-18
**Scan window:** 2026-04-17 14:45 → 2026-04-18 07:05
**Previous report:** monitor_report_2026-04-17.md

---

## File System Status

| File | Last Modified | Age | Status |
|------|--------------|-----|--------|
| hub_monitor_report.md | 2026-04-18 07:04 | fresh | OK |
| clinical_trials_latest.json | 2026-04-18 07:04 | fresh | OK |
| pubmed_recent_latest.json | 2026-04-18 07:04 | fresh | OK |
| pubmed_recent_summary.md | 2026-04-18 07:04 | fresh | OK |
| literature_gap_report.md | 2026-04-17 14:50 | 1 day | OK |
| literature_gap_data.json | 2026-04-14 14:26 | 4 days | OK (underlying run) |
| Diabetes_Research_Tracker.xlsx | 2026-04-17 14:50 | 1 day | OK |

Hub monitor counted 724 tracked files (11 new, 93 modified, 0 removed since previous scan). 451 result files are flagged as older than 14 days — these are mostly historical dated snapshots and do not require individual refresh.

**New files this cycle:** `clinical_trials_snapshot_2026-04-18.json`, `pubmed_recent_snapshot_2026-04-18.json`, `cross_reference_diabetologia_islet_repurposing.md`, `glp1_pharmacogenomics_equity_synthesis.md`, `paper_library/abstracts/12345678.json`, `verification_reports/verify_Islet_Drug_Repurposing.json`, `Analysis/Scripts/postprocess_dashboards.py`, and four `.github/ISSUE_TEMPLATE` files.

---

## Clinical Trial Changes

**Total trials tracked:** 767 across five categories (T1D Cure & Cell Therapy 151, T1D Immunotherapy & Prevention 71, T2D Novel Therapies P2-3 137, Devices 222, Recently Completed w/ Results 260).

### Day-over-day diff (2026-04-17 → 2026-04-18)

- **New trials (1):** NCT07536516 — "Measurement of Ocular Blood Flow and Retinal Oxygen Extraction in Diabetic Patients" (Medical University of Vienna, observational, RECRUITING). Low strategic relevance — retinal physiology study.
- **Removed (2):**
  - NCT06897202 — MET097 once-weekly, Phase 2 (ACTIVE_NOT_RECRUITING) — likely transitioned off the active-recruitment query.
  - NCT05803421 — Orforglipron vs. insulin glargine, Phase 3 (ACTIVE_NOT_RECRUITING) — this is the ACHIEVE-4 study; its removal is consistent with the April 16 topline readout (see Breaking News).
- **Status change (1):** NCT07340320 — "CX11 Tablets in T2D" moved NOT_YET_RECRUITING → RECRUITING.
- **New results posted:** 0 in this 24-hour window.

### Monthly delta (vs 2026-03-15)

39 new trials, 18 removed, 19 status changes. Notable newly-COMPLETED trials include:

- NCT05923827 — Omnipod 5 + Libre 2 vs MDI (T1D, pediatric+adult) — results posted 2026-04-14.
- NCT06141941 — CGM use in immediate postpartum period — results posted 2026-04-09.

### Key-sponsor Phase 3 RECRUITING roster (unchanged from yesterday)

- **Vertex:** NCT06832410, NCT04786262 (both VX-880 / zimislecel in T1D).
- **Eli Lilly:** NCT07222137, NCT07222332 (baricitinib in T1D — stage-3 delay and beta-cell preservation); NCT06993792, NCT06972472 (orforglipron obesity master protocol + OSA cohort); NCT06739122 (dulaglutide pediatric).
- **Novo Nordisk:** NCT07076199 (insulin icodec weekly).

Summary totals by key sponsor: Eli Lilly 26, Novo Nordisk 23, Vertex 3. Aggregate phase split: PHASE3 = 116, PHASE2 = 123, PHASE2/3 = 16.

### Recent trial results worth reviewing

Top 5 results posted in the last 14 days:

1. NCT05238142 (2026-04-16) — MiniMed 780G AHCL in T2D, in-home study.
2. NCT05727579 (2026-04-15) — Dietary sodium × ertugliflozin on GFR/renal oxygenation.
3. NCT06206525 (2026-04-15) — Inpatient insulin dosing calculator feasibility.
4. NCT05923827 (2026-04-14) — Omnipod 5 + Libre 2 vs MDI, T1D pediatric+adult.
5. NCT05144984 (2026-04-09) — Semaglutide + NNC0487 combination.

---

## PubMed Highlights

**Lookback:** 30 days. **Unique papers in snapshot:** 142. **Day-over-day:** +29 new / −18 dropped. **Week-over-week (vs 2026-04-11):** +99 new / −88 dropped (normal churn for 30-day rolling window).

### Cross-domain papers (highest priority)

11 papers with ≥2 domain tags. Top picks:

- **[PMID 41997446]** (3 domains) "GIPR:GCGR co-agonism restores normal weight in obese rodents." — *T2D GLP-1 New / T2D Remission / Key Therapy: retatrutide*. New cross-domain, directly relevant to triple-agonist mechanism.
- **[PMID 41995155]** (2 domains) "Engineering immune-evasive islet replacement: cell-intrinsic and peri-graft strategies." — *T1D Stem Cell Cure / Diabetes Gene Therapy*. New cross-domain, relevant to zimislecel and hypoimmune islet programs.
- **[PMID 41913320]** (2 domains) "Toward Personalized Medicine in Type 1 Diabetes" — *T1D Immunotherapy / teplizumab*.
- **[PMID 41984016]** (2 domains) "Comparative CV Effectiveness of GLP-1 RAs and SGLT2 inhibitors" — *T2D GLP-1 New / dapagliflozin*.
- **[PMID 41993554]** Colonic metabolomic/transcriptomic alterations in metabolic syndrome — *Biomarker / Microbiome*.
- **[PMID 41986815]** Multi-tissue multi-omics integration for T2D — *Drug Repurposing / Multi-Omics* (directly relevant to Tier 1 Drug Repurposing and Multi-Omics contribution areas).
- **[PMID 41988036]** Gut microbiome-epigenetic crosstalk in obesity/T2D — *Microbiome / Multi-Omics*.

### Key-therapy mentions in the 30-day corpus

| Therapy | Total count | Highlight |
|---------|-------------|-----------|
| orforglipron | 5 | PMID 41765029 (head-to-head vs oral semaglutide), PMID 41994902 (tablet/capsule bioequivalence), PMID 41984238 (methodological critique — **worth reading for Ingest Standard**) |
| retatrutide | 3 | PMID 41785010 (T2D/obesity overview), PMID 41997446 (GIPR:GCGR co-agonism, rodents) |
| teplizumab | 4 | PMID 41572010/41572011 (screening / clinician-patient partnership series), PMID 39929732 (immunologic interventions review) |
| dapagliflozin | 34 | Volume driven by CKD/CVD lit; PMID 41975024 on eGFR slope is notable for DKD modeling |
| zimislecel, CagriSema, baricitinib, icodec | 0 | No direct hits in 30-day window (strategic gap — baricitinib has active P3 trials NCT07222137/NCT07222332 but no recent PubMed chatter) |

### Publication volume trends (30-day counts by domain)

High: Diabetes AI/ML 174, T2D GLP-1 New 153, Diabetes Microbiome 149, Biomarker 139. Low: GLP-1 Pharmacogenomics 1, LADA New Research 3, Drug Repurposing 5, Epigenetics 8. The low-volume domains continue to match Tier 1 contribution opportunities (Literature Synthesis, Drug Repurposing, LADA misdiagnosis).

---

## Gap Analysis Summary

Gap analysis run date: 2026-04-14 (data), with narrative regenerated 2026-04-17. Top 5 gaps (all score = 100.0, BRONZE evidence):

1. **Beta Cell Regen × Health Equity** (d1=1,394 / d2=1,865 / joint=0) — equity analysis of regenerative therapies is absent.
2. **Insulin Resistance × Islet Transplant** (d1=18,844 / d2=242 / joint=1) — IR in graft recipients affecting survival.
3. **Islet Transplant × GWAS / Polygenic** (flagged as methodologically distinct in interpreted report).
4. **Islet Transplant × Personalized Nutrition** (methodologically distinct).
5. **Islet Transplant × Drug Repurposing** (d1=242 / d2=574 / joint=0) — repurposing immunosuppressants/islet-protective drugs. **This aligns directly with Tier 1 Drug Repurposing.**

### Tier 1 alignment

Tier 1 areas per Research Doctrine: Multi-Omics Biomarker Integration, Literature Synthesis & Gap Analysis, Clinical Trial Intelligence, Drug Repurposing Computational Screening, AI/ML Prediction, Epidemiological Data. The following top gaps map to Tier 1:

- Islet Transplant × Drug Repurposing → **Drug Repurposing** (directly) and **Literature Synthesis** (framing).
- Beta Cell Regen × Health Equity → **Epidemiological Data Analysis** (equity axis).
- Drug Repurposing × Health Equity, Drug Repurposing × LADA (ranks 12–13) → **Drug Repurposing** + **LADA-misdiagnosis** (Tier 2 #11).
- Glucokinase × Drug Repurposing (rank 8) → **Drug Repurposing** — existing repurposing corpus already covers islet GK activators (cross-ref `cross_reference_diabetologia_islet_repurposing.md`, new this cycle).

---

## Breaking News (web, last 7 days)

- **Lilly orforglipron — ACHIEVE-4 Phase 3 topline (Apr 16, 2026):** Met primary non-inferiority vs insulin glargine on MACE-4 (HR 0.84), with significantly greater A1C and weight reductions. Lilly remains on track to submit an NDA for T2D by end of Q2 2026. **Significance: high** — this is the first oral small-molecule GLP-1 RA to complete a Phase 3 with a cardiovascular outcome. Consistent with the removal of NCT05803421 from the active-trial list this cycle.
- **FDA approvals (April 2026):**
  - **Foundayo (orforglipron)** approved Apr 1, 2026 for obesity / overweight-with-comorbidity. First oral non-peptide GLP-1 RA without food/water timing restrictions.
  - **First generic dapagliflozin** approved Apr 7, 2026 (Biocon and others) for T2D HF-hospitalization reduction + glycemic control. **Significance: high for health-equity analyses** — generic availability materially changes access economics.

These two items are material for the Clinical Trial Intelligence and Drug Repurposing/Health Equity workstreams.

---

## Recommended Actions

1. **Update tracker with orforglipron regulatory status** — Diabetes_Research_Tracker.xlsx currently lists orforglipron as investigational; add Foundayo FDA approval (2026-04-01, obesity) and ACHIEVE-4 P3 T2D topline (2026-04-16, NDA planned Q2). Add PMIDs 41765029, 41994902, 41984238, 41870800.
2. **Add generic-dapagliflozin row to Health Equity / Generic Drug Catalog dashboards** — FDA approval 2026-04-07 changes access assumptions for SGLT2i equity analyses.
3. **Re-run literature gap analysis** — `literature_gap_data.json` is 4 days old. Suggested: `python project1_literature_gap_analysis.py`. Not urgent but will pick up the 29 new papers from today's PubMed delta.
4. **Review cross-domain paper PMID 41997446** (GIPR:GCGR co-agonism, 3-domain) — candidate for ingest into retatrutide evidence thread and T2D Remission dashboard.
5. **Review cross-domain paper PMID 41995155** (immune-evasive islet replacement) — ingest into T1D Stem Cell Cure and Gene Therapy threads; directly relevant to `cross_reference_diabetologia_islet_repurposing.md`.
6. **Ingest the orforglipron methodological critique (PMID 41984238)** — apply the Ingest Standard; this is a peer-reviewed challenge to prior efficacy/safety analyses and should be tagged as contradicting-evidence in any orforglipron synthesis.
7. **Watch the Vertex VX-880 Phase 3s (NCT06832410, NCT04786262)** — no status or results change today, but these are the only Phase 3 zimislecel listings; flag for weekly re-check.
8. **No action needed** on NCT07536516 (new ocular blood flow observational) — low strategic priority.
9. **Baricitinib PubMed silence** despite two active Phase 3 trials (NCT07222137, NCT07222332) — consider a targeted PubMed/bioRxiv query next week to confirm no preprint coverage was missed.

---

## Validation Notes

All findings above are BRONZE (single-source analytic) or WEB-SEARCH-BRONZE (single-source media) per Research Doctrine v1.0. No existing files were modified in this run. Source PMIDs and NCT IDs are provided so each claim is independently verifiable. Trial counts, phase splits, and day-over-day diffs are computed directly from `clinical_trials_latest.json` and the 2026-04-17 snapshot. Gap score quotations come from `literature_gap_data.json` ranked_gaps and `literature_gap_report.md`.

---
*Generated by automated monitor run — 2026-04-18*
