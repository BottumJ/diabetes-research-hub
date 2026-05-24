# Diabetes Research Hub — Monitor Report

**Date:** 2026-05-22
**Scan time:** 07:04:55 (hub_monitor.py) + scheduled review run
**Previous monitor report:** monitor_report_2026-05-21.md
**Comparison snapshots:** clinical_trials_snapshot_2026-05-14 → 2026-05-22 (8 days); pubmed_recent_snapshot_2026-05-21 → 2026-05-22 (1 day)

---

## File System Status

All four daily pipeline outputs ran successfully this morning. The hub now tracks 848 files; 3 new and 28 modified since yesterday's scan.

| File | Last modified | Status |
|------|---------------|--------|
| hub_monitor_report.md | 2026-05-22 07:04 | Fresh |
| clinical_trials_latest.json | 2026-05-22 07:04 | Fresh (795 trials) |
| pubmed_recent_latest.json | 2026-05-22 07:04 | Fresh (148 papers, 30-day window) |
| literature_gap_report.md | 2026-05-21 08:08 | Fresh (regenerated yesterday) |
| literature_gap_data.json | 2026-04-20 15:35 | **STALE — 31 days old** |
| literature_gap_matrix.xlsx | 2026-04-20 15:35 | **STALE — 31 days old** |
| agent_state.json | 2026-05-21 08:10 | Fresh |
| citation_validation.json | 2026-05-21 08:08 | Fresh |

Note: hub_monitor flags 594 result files older than 14 days, but most are dated snapshot files (clinical_trials_snapshot_*, pubmed_recent_snapshot_*) intentionally retained for trend analysis — not actionable staleness.

**True staleness:** the underlying gap-analysis numerical data (`literature_gap_data.json`, `literature_gap_matrix.xlsx`) has not been regenerated since 2026-04-20. The human-readable `literature_gap_report.md` was rewritten yesterday but is still based on the April 20 data.

---

## Clinical Trial Changes

### Snapshot diff (2026-05-21 → 2026-05-22)
Per `hub_monitor_report.md`: **0 new trials, 0 removed, 0 status changes, 0 new results posted.** No day-over-day activity.

### 8-day diff (2026-05-14 → 2026-05-22)
- **New trials: 6** (all `NOT_YET_RECRUITING`)
  - `NCT07585630` (Phase 2) — A1Cantus vs. Placebo, UC Riverside
  - `NCT07589387` (NA) — Hypertension-Diabetes Integration Study, Nigeria — Washington University
  - `NCT07593625` (NA) — Next-Gen AID Algorithm in Adults — Insulet Corporation
  - `NCT07594145` (Phase 2) — Precision T1D Platform: New Therapies for Cardio-Renal Complications — OHSU
  - `NCT07595289` (NA) — DP-DCT 1.0: Dapagliflozin combined with… — Third Xiangya Hospital
  - `NCT07599982` (NA) — MODI Insulin Titration Algorithm Safety — DreaMed Diabetes
- **Removed: 4** (likely re-categorized or completion-aged out)
- **Status changes: 4**
  - `NCT05950659` `NOT_YET_RECRUITING → RECRUITING` (WIREDUP — insoles for ulcer prevention)
  - `NCT06730906` `RECRUITING → ENROLLING_BY_INVITATION` (PACTAID T1D exercise app)
  - `NCT06073457` `RECRUITING → ACTIVE_NOT_RECRUITING` (Magnetic Gastro-Ileal Diversion Study)
  - `NCT06467955` `RECRUITING → ACTIVE_NOT_RECRUITING` (MagDI Canada Study)
- **New results posted (in this 8-day window): 0.** Last batch of newly-posted results was around May 4–13 and was captured in earlier monitor reports.

### Key Phase 3 trials — current status (sponsor-screened)
| Trial | Drug/Therapy | Sponsor | Phase | Status |
|-------|--------------|---------|-------|--------|
| NCT06832410 | VX-880 (zimislecel) | Vertex | 3 | RECRUITING |
| NCT04786262 | VX-880 (long-running) | Vertex | 3 | RECRUITING |
| NCT07222137 | Baricitinib — delay stage 3 T1D | Eli Lilly | 3 | RECRUITING |
| NCT07222332 | Baricitinib — preserve β-cell in children | Eli Lilly | 3 | RECRUITING |
| NCT07076199 | Insulin icodec | Novo Nordisk | 3 | RECRUITING |
| NCT06914895 | Tirzepatide in T1D | Eli Lilly | 3 | ACTIVE_NOT_RECRUITING |
| NCT06962280 | Long-term tirzepatide in T1D | Eli Lilly | 3 | ACTIVE_NOT_RECRUITING |
| NCT05929079 | Retatrutide in T2D | Eli Lilly | 3 | ACTIVE_NOT_RECRUITING |
| NCT06297603 | Retatrutide vs placebo, T2D | Eli Lilly | 3 | ACTIVE_NOT_RECRUITING |
| NCT06260722 | Retatrutide vs semaglutide, T2D | Eli Lilly | 3 | ACTIVE_NOT_RECRUITING |
| NCT06972472 | Orforglipron in obesity + T2D | Eli Lilly | 3 | ACTIVE_NOT_RECRUITING |
| NCT06534411 | CagriSema, T2D | Novo Nordisk | 3 | ACTIVE_NOT_RECRUITING |

Total Phase 3 RECRUITING trials in the hub: **46.** Total trials with posted results: **281.**

### Recently-posted results worth a look (top 5, from `clinical_trials_latest.json`)
1. `NCT04286555` (posted 2026-05-13) — DASH for Diabetes, Johns Hopkins
2. `NCT04226027` (2026-05-13) — Dynamically Tailored Behavioral Interventions in Diabetes, Columbia
3. `NCT05454891` (2026-05-12) — Extended Bolus for Meals in a Closed-loop System, UCSF
4. `NCT05514535` (2026-05-11) — Semaglutide + Lower-Dose Insulin Glargine, **Novo Nordisk** *(key org)*
5. `NCT02107976` (2026-05-12) — Vitamin C, RBC Fragility, and Diabetes, NIH

---

## PubMed Highlights

### Volume trends (today vs yesterday)
Biggest day-over-day increases in total-hit counts (30-day rolling window):

| Domain | Yesterday | Today | Δ |
|--------|-----------|-------|---|
| Diabetes Biomarker | 159 | 171 | **+12** |
| Diabetes AI/ML | 222 | 226 | +4 |
| Closed Loop AP | 17 | 21 | +4 |
| T2D GLP-1 New | 145 | 148 | +3 |
| T2D Remission | 65 | 67 | +2 |

41 new papers / 40 dropped from the rolling 30-day window. Net: +1.

### Cross-domain papers (highest priority) — 9 new today
The standout is `42163482` (5 domains): **Extracellular Vesicle Proteins as Predictive Biomarkers for Developing T1D** — *Proteomics*, 2026-May-20. Links T1D Stem Cell Cure, T1D Immunotherapy, Diabetes AI/ML, Diabetes Biomarker, and Key Therapy: teplizumab. Highest-value paper this week.

Other multi-domain new papers (≥2 domains):
- `42148104` — Adapting CAR-T and CAR-Treg cancer therapies for autoimmunity (T1D Stem Cell Cure + T1D Immunotherapy)
- `42167392` — Precise staging of diabetic retinopathy via ML (AI/ML + Biomarker + Complications)
- `42167398` — Multi-omics atlas of multisystem T2D complications (AI/ML + Multi-Omics)
- `42163256` — Tissue-specific glucose-lowering drug effects on aging via DNA methylation (Epigenetics + Multi-Omics)
- `42162795` — Yogurt, gut microbiota, and glucose dynamics (AI/ML + Microbiome)
- `42161877` — FGL2 in diabetic nephropathy (Biomarker + Complications)
- `42161723` — Predicting complications in South Asians (AI/ML + Biomarker)
- `42168638` — Dysesthesia with GLP-1 agonists, data-mining review (T2D GLP-1 + retatrutide)

### Key therapy mentions (rolling 30 days)
- **teplizumab**: 5 papers — incl. `42138126` (post-approval autoantibody ordering patterns, *JCEM*) and `42138080` (review of new/emerging T1D therapies, *JCI*)
- **retatrutide**: 5 papers — incl. `42135195` (lipid/metabolite profiles in obesity ± T2D) and `42108533` (triple-hormone receptor agonism in cardiovascular-kidney-metabolic disease)
- **dapagliflozin**: 35 total mentions
- **icodec**: 4 papers — incl. `42119975` (safety pooled analysis) and `41705603` (cost-utility analysis)
- **orforglipron**: 3 papers — incl. `42120723` (ATTAIN-MAINTAIN Phase 3b weight maintenance) and `42116665` (GI safety in adults ± T2D)
- **CagriSema**: 2 papers — incl. `41759565` (systematic review/meta-analysis vs semaglutide)
- **baricitinib**: 2 papers (1 diabetes-relevant — `41761435` is dermatologic)
- **zimislecel**: 0 papers (still no published direct evidence on this PMI-search; relevant signal sits in `42163482` re: T1D biomarker prediction)

---

## Gap Analysis Summary

Source: `literature_gap_report.md` (regenerated 2026-05-21) over **April-20 underlying data**. Top under-researched intersections (Gap Score 100.0, BRONZE validation):

1. **Beta Cell Regen × Health Equity** (joint pubs: 0)
2. **Insulin Resistance × Islet Transplant** (1)
3. **Islet Transplant × Drug Repurposing** (0)
4. **Islet Transplant × Health Equity** (0)
5. **Gene Therapy × LADA** (0)

These align directly with the hub's Tier 1 contribution areas: **LADA** (gaps #5, #10, #11, #13, #14) and **Islet Transplant** (#2, #3, #4) dominate the top-15 list, so the current research priorities remain well-targeted at genuinely under-explored intersections. Drug Repurposing × LADA (#13) and Glucokinase × LADA (#10) are particularly actionable for computational work.

---

## Breaking News (web check, last 7 days)

Two items worth tracking; nothing surprising:

- **Baricitinib slows T1D progression (TrialNet, posted May 12, 2026)** — JAK inhibitor results published; next step is testing earlier-stage disease and larger cohorts. This aligns with Lilly's two new Phase 3 baricitinib trials (`NCT07222137`, `NCT07222332`) — both still RECRUITING. The TrialNet announcement is consistent with PubMed cross-domain interest in T1D Immunotherapy.
- **Retatrutide TRANSCEND-T2D-1** — top-dose group lost 16.8% body weight on average with weight loss still ongoing at study end. Lilly's Phase 3 retatrutide trials in the hub remain `ACTIVE_NOT_RECRUITING` — results posting is plausible in the next 30–90 days; worth a manual check on ClinicalTrials.gov.

Not actionable but worth context:
- FDA PDUFA date **May 29, 2026** for **Afrezza pediatric expansion** (MannKind). Would be the first needle-free insulin for kids.
- FDA approved **first generic dapagliflozin** earlier in May.
- Recap: **Awiqli (icodec)** was approved March 26, 2026; **Foundayo (orforglipron)** approval is referenced in news as the only any-time-of-day GLP-1 pill for weight loss.

---

## Recommended Actions

1. **Refresh gap analysis numerical data.** `literature_gap_data.json` and `literature_gap_matrix.xlsx` are 31 days old. Run: `python project1_literature_gap_analysis.py` so the May `literature_gap_report.md` is backed by current PubMed counts.
2. **Pull PMID 42163482 into the paper library.** The 5-domain T1D biomarker paper is the highest-value cross-domain hit this week — relevant to T1D Stem Cell Cure, T1D Immunotherapy, AI/ML, Biomarker, and teplizumab. Add to `paper_library/abstracts/` and enrich `evidence_network.json` on the next agent run.
3. **Update tracker with the 6 new trials** (NCT07585630, NCT07589387, NCT07593625, NCT07594145, NCT07595289, NCT07599982) in `Diabetes_Research_Tracker.xlsx`. NCT07594145 (OHSU Precision T1D — cardio-renal complications) and NCT07585630 (A1Cantus Phase 2) merit short tracker entries.
4. **Monitor retatrutide Phase 3 results posting.** Three Lilly retatrutide trials sit in `ACTIVE_NOT_RECRUITING` (NCT05929079, NCT06297603, NCT06260722). With TRANSCEND-T2D-1 results circulating in trade press, ClinicalTrials.gov results may post imminently — set a manual reminder for late May.
5. **Review baricitinib T1D Phase 3 enrollment.** Both `NCT07222137` and `NCT07222332` are currently RECRUITING; relevant to the hub's T1D Immunotherapy domain and the new TrialNet announcement. No action needed beyond watching for status changes.
6. **Cross-check** `Research_Findings_Summary.md` (regenerated 2026-05-21) against today's new cross-domain papers — particularly the multi-omics atlas (PMID 42167398) and the South Asian complications-prediction paper (PMID 42161723), both of which intersect the AI/ML + Biomarker tier the doctrine prioritizes.

---

## Notes on this run

- This is an automated review; no files were modified.
- Evidence levels: per the Research Doctrine, all gap classifications remain **BRONZE** (single-source bibliometric). Trial/PubMed numerical counts are verifiable against the source APIs.
- The "new results posted: 0" in the 8-day clinical-trials diff likely reflects that the previously-flagged May 4–13 results batch has now stabilized in older snapshots — confirm by spot-checking yesterday's monitor report.

*Generated by automated Diabetes Hub Monitor — 2026-05-22*
