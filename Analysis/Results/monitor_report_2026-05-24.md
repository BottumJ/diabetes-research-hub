# Diabetes Research Hub — Monitor Review Report

**Run date:** 2026-05-24
**Scope:** Automated review of script outputs in `Analysis/Results/`
**Run mode:** Scheduled (read-only — no files modified)
**Previous review:** `monitor_report_2026-05-23.md`

---

## File System Status

All daily-refresh data files are current (regenerated 2026-05-24). The only stale data file is the literature gap analysis, which has not been re-run for 33 days.

| File | Last modified | Age | Status |
|---|---|---|---|
| hub_monitor_report.md | 2026-05-24 | 0d | Fresh |
| clinical_trials_latest.json | 2026-05-24 | 0d | Fresh |
| clinical_trials_summary.md | 2026-05-24 | 0d | Fresh |
| pubmed_recent_latest.json | 2026-05-24 | 0d | Fresh |
| pubmed_recent_summary.md | 2026-05-24 | 0d | Fresh |
| literature_gap_report.md | 2026-05-23 | 1d | Fresh |
| literature_gap_data.json | 2026-04-20 | **33d** | **STALE (>14d)** |
| literature_gap_matrix.xlsx | 2026-04-20 | **33d** | **STALE (>14d)** |
| agent_state.json | 2026-05-23 | 1d | Fresh |
| evidence_network.json | 2026-05-23 | 1d | Fresh |

Workspace inventory (per `hub_monitor_report.md`, 2026-05-24 scan): 859 tracked files, 6 new, 30 modified, 0 removed since the 2026-05-23 scan. 602 result files are flagged as >14 days old — most are dated snapshots and iterate reports that are expected to age.

---

## Clinical Trial Changes

Universe: **797 unique trials** (153 T1D Cure & Cell Therapy, 71 T1D Immunotherapy/Prevention, 140 T2D Novel Phase 2–3, 225 Devices, 281 Recently Completed). Status mix: 265 RECRUITING, 137 NOT_YET_RECRUITING, 107 ACTIVE_NOT_RECRUITING, 281 COMPLETED. Phase mix: 121 PHASE3, 124 PHASE2.

**Delta vs. 2026-05-23 (per `hub_monitor_report.md`):** 0 new trials, 0 removed, 0 status changes, 0 new results posted in the past 24 h. The snapshot is unchanged day-over-day.

**Delta vs. 2026-05-17 (past 7 days, computed from snapshots):**

- 7 new trials added; 5 trials removed from the active universe.
- 5 trials changed status — summarized below.

| NCT ID | Sponsor | Title (truncated) | Change |
|---|---|---|---|
| NCT07372872 | Hong Kong Metropolitan University | MyGlucoCare smartphone app feasibility | NOT_YET → RECRUITING |
| NCT05950659 | Orpyx Medical Technologies | WIREDUP wearable insoles for diabetic ulcer prevention | NOT_YET → RECRUITING |
| NCT06730906 | Mayo Clinic | PACTAID app for exercise in T1D | RECRUITING → ENROLLING_BY_INVITATION |
| NCT06073457 | GT Metabolic Solutions | MagDI magnetic gastro-ileal diversion | RECRUITING → ACTIVE_NOT_RECRUITING |
| NCT06467955 | GT Metabolic Solutions | MagDI Canada study | RECRUITING → ACTIVE_NOT_RECRUITING |

The two GT Metabolic transitions (RECRUITING → ACTIVE_NOT_RECRUITING) indicate the magnetic gastro-ileal diversion device program has finished enrollment — worth flagging for the device-vs-pharmacotherapy line of analysis.

**Phase 3 RECRUITING:** 46 trials currently. No Phase 3 status flips this week.

**Recently posted results (last 30 days, top items):**

| Date | NCT | Sponsor | Title (truncated) |
|---|---|---|---|
| 2026-05-22 | NCT03919877 | Stanford University | Precision Diets for Diabetes Prevention |
| 2026-05-13 | NCT04286555 | Johns Hopkins | DASH for Diabetes |
| 2026-05-13 | NCT04226027 | Columbia | Dynamically Tailored Behavioral Interventions |
| 2026-05-12 | NCT05454891 | UCSF | Extended Bolus for Meals in Closed-loop System |
| 2026-05-11 | NCT05514535 | Novo Nordisk | Semaglutide + lower-dose insulin |
| 2026-04-30 | NCT05823948 | Novo Nordisk | Flash glucose with once-weekly insulin icodec |

The two Novo Nordisk result postings (NCT05514535 semaglutide + insulin; NCT05823948 icodec + flash CGM) are most relevant to ongoing tracker themes. Note: 0 results-postings occurred in the past 7 days specifically — the items above span the full 30-day window.

**Key-sponsor footprint:** Eli Lilly 27 trials (6 recruiting, 13 completed), Novo Nordisk 26 (2 recruiting, 16 completed), Vertex 3 (2 recruiting). Sana Biotechnology still has no trials in the tracked universe — worth confirming this is by design.

---

## PubMed Highlights

Universe: 156 unique papers across 16 alert domains and 8 key therapies (30-day lookback).

**Volume deltas:** 25 new papers since 2026-05-23 (19 dropped from the rolling window); **109 new since 2026-05-17**. PubMed flow is steady.

**Domain volume (paper count in current rolling window / total PubMed match):**

The hottest current domain is Diabetes AI/ML (229 total matches, sampled to 10). Quiet domains: GLP-1 Pharmacogenomics (1), Drug Repurposing (6), LADA New Research (6), Epigenetics (9). The Pharmacogenomics quietness is consistent with the Tier 1 contribution opportunity flagged in `CONTRIBUTION_STRATEGY.md`.

**Cross-domain papers (highest-priority signal — 13 in current window):**

| PMID | Date | Journal | Title | Domains |
|---|---|---|---|---|
| 42171301 | 2026-05-21 | Food & Function | Dietary diversity and T2D in two Chinese cohorts: multi-omics | Biomarker / Microbiome / Multi-Omics |
| 42163482 | 2026-05-20 | Proteomics | Extracellular Vesicle proteins as T1D predictive biomarkers | T1D Stem Cell / T1D Immunotherapy / teplizumab |
| 42174929 | 2026-05-21 | Stud Health Tech Inf | Clinical predictors of diabetes/prediabetes — Explainable AI | T2D Remission / AI-ML |
| 42171711 | 2026-05-22 | Acta Diabetologica | Epigenetic signatures in T2D — therapy + lifestyle | T2D Remission / Epigenetics |
| 42171425 | 2026-05-01 | Transl Vis Sci Tech | HDGF marker for proliferative diabetic retinopathy (MR) | Biomarker / Complications |
| 42168638 | 2026-05-22 | Eur J Clin Pharm | Dysesthesia with GLP-1 agonists — data-mining + review | T2D GLP-1 / retatrutide |
| 42163256 | 2026-05-21 | BMC Medicine | Glucose-lowering drug targets and aging via DNA methylation | Epigenetics / Multi-Omics |
| 42148104 | 2026 | Front Immunol | CAR-T / CAR-Treg adapted for autoimmunity | T1D Stem Cell / T1D Immunotherapy |
| 42143506 | 2026-Aug | Int Immunopharmacol | CAR therapy evolution: oncology to autoimmunity | T1D Immunotherapy / Gene Therapy |
| 42138126 | 2026-05-15 | JCEM | US patterns in islet autoantibody ordering — post-teplizumab | T1D Immunotherapy / teplizumab |
| 42138080 | 2026-05-15 | J Clin Invest | New and emerging therapies in T1D | T1D Immunotherapy / teplizumab |
| 42142983 | 2026-05-17 | Obes Res Clin Pract | Weight loss after bariatric surgery — multi-site audit | retatrutide / CagriSema |
| 42161872 | 2026-05-21 | Zhonghua Yi Xue | Basal insulin/GLP-1RA weekly preparation in T2D | T2D GLP-1 / icodec |

The 2026-05-23 → 2026-05-24 delta included one new cross-domain paper (PMID 42174929, T2D Remission × AI/ML).

**Key-therapy mentions (in title/abstract, current rolling window):** teplizumab 3, icodec 3, dapagliflozin 3, semaglutide 6, orforglipron 2, retatrutide 2, CagriSema 1, baricitinib 1, tirzepatide 1, **zimislecel 0**. Notable items:

- *Orforglipron for maintenance of body weight reduction* (PMID 42120723, **Nature Medicine**, 2026-05-13) — the Phase 3 maintenance readout for Lilly's oral GLP-1.
- *Considerations for the clinical use of teplizumab in Stage 2 T1D — Consensus* (PMID 42051156, Diabetic Medicine).
- *Retatrutide lipid and metabolite profiles in obesity* (PMID 42135195, JCEM, 2026-05-14).
- *Triple Hormone Receptor Agonism: Retatrutide* (PMID 42108533, Cardiology in Review).
- *Simplified switching to once-weekly insulin icodec* (PMID 42168822, Diabetes Obes Metab, 2026-05-21).

Zimislecel's absence from the recent PubMed window is worth a manual cross-check — the therapy is high-profile and the previous month had a Phase 1/2 NEJM publication.

---

## Gap Analysis Summary

Source: `literature_gap_report.md` (2026-05-23) and `literature_gap_data.json` (2026-04-20 — **stale; recommend refresh**).

**Top 5 under-researched intersections (Gap Score = 100, joint pubs ≤ 1):**

1. **Beta Cell Regen × Health Equity** — Equity dimension of regenerative therapies absent.
2. **Insulin Resistance × Islet Transplant** — Affects graft survival; barely studied.
3. **Islet Transplant × Drug Repurposing** — Existing immunosuppressants for islet protection unscreened.
4. **Islet Transplant × Health Equity** — Access disparities at the few transplant centers unanalyzed.
5. **Gene Therapy × LADA** — Autoimmune profile makes LADA a candidate; no crossover work exists.

Alignment with Tier 1 contribution areas (per `CONTRIBUTION_STRATEGY.md` / `RESEARCH_DOCTRINE.md`): Gaps 3, 4, and 5 directly support the islet-repurposing and LADA-underdiagnosis programs already in flight (see `islet_repurposing_report.md` and `Project 1` literature gap analysis). Gaps 1 and 4 cluster with the Health Equity contribution thrust.

Per the Research Doctrine these classifications carry **BRONZE** validation (single analytical source). Any claim derived from them must be labeled as preliminary until cross-referenced with Cochrane/PROSPERO and a domain expert.

---

## Breaking News (Last 7 Days — Web Check)

Significant items only; routine product launches and clinical commentary skipped.

- **Vertex zimislecel (VX-880) Phase 3 — Program on track.** Vertex confirmed dosing completion in the Phase 3 FORWARD trial with global regulatory submissions (FDA / EMA / MHRA) expected in 2026. Phase 1/2 NEJM data: 83% of participants insulin-independent at 1 year; all achieved HbA1c <7% and TIR >70%. Relevance: cluster directly with the hub's T1D Cure & Cell Therapy and Islet Transplant tracks. Evidence level: **GOLD** (peer-reviewed NEJM + sponsor disclosure).
- **Eli Lilly orforglipron — Phase 3 ATTAIN-MAINTAIN positive topline.** Long-term weight-maintenance readout reported positive. Pairs with PMID 42120723 (Nature Medicine, 2026-05-13) in the PubMed window. Evidence level: **SILVER** (peer-reviewed + sponsor press; full results pending).
- **FDA approvals in window:** Langlara (insulin glargine-aldy, interchangeable Lantus biosimilar) approved 2026-04-29; Awiqli (insulin icodec) confirmed approved 2026-03-26 as first/only once-weekly basal insulin for T2D. Both align with existing tracker rows.
- **Stem-cell-derived islet cells reverse diabetes in mice (Sweden, Stem Cell Reports, 2026-05-06).** A more reliable stem-cell differentiation protocol. Preclinical only — evidence level **BRONZE** for any clinical claim, but methodologically relevant to the cell-therapy variability discussion.

Nothing in the past 7 days qualifies as a binary, practice-changing event beyond the Vertex and Lilly program updates above.

---

## Recommended Actions

1. **Refresh the gap analysis.** `literature_gap_data.json` and `literature_gap_matrix.xlsx` are 33 days old. Run: `python project1_literature_gap_analysis.py`. The `literature_gap_report.md` was regenerated 2026-05-23 from this stale matrix, so its numbers may already be drifting.
2. **Verify zimislecel PubMed coverage.** Zero hits in the 30-day window despite known Phase 3 milestones. Likely a query-term issue (try `VX-880` and `Vertex islet cell therapy` alongside `zimislecel`). Consider widening the alert in `baseline_pubmed_alerts.py`.
3. **Add to tracker — three trial-state changes worth recording.**
   - GT Metabolic NCT06073457 + NCT06467955: MagDI enrollment complete (RECRUITING → ACTIVE_NOT_RECRUITING).
   - Mayo NCT06730906: PACTAID T1D app moved to ENROLLING_BY_INVITATION.
4. **Triage cross-domain PubMed papers (highest priority).** Read PMID 42163482 (EV proteins as T1D predictive biomarkers — bridges Stem Cell, Immunotherapy, and teplizumab tracks) and PMID 42138080 (J Clin Invest review of new T1D therapies). Both are squarely on Tier 1 contribution paths.
5. **Action the orforglipron Phase 3 maintenance result.** Add NCT-level lookup and PMID 42120723 to the Tracker under T2D Novel Therapies; flag for the contribution synthesis on long-term GLP-1 outcomes.
6. **Record Novo Nordisk result-posts.** NCT05514535 (semaglutide + lower-dose insulin) and NCT05823948 (icodec + flash CGM) results were posted in the past 30 days but are not yet in the curated "Notable Trials to Watch" table in `clinical_trials_summary.md`.
7. **Investigate the Sana Biotechnology zero-trial count** in the universe (key org per task spec but no matches). If Sana's pipeline is registered under a contract organization name, the sponsor-match string in `baseline_clinical_trials.py` may need updating.
8. **Confirm the 602 "stale" results files** flagged by hub_monitor are intentional snapshots (most are dated daily snapshots and iterate reports — expected to age). No action unless a refresh of older programs is desired.

---

## Notes on Methodology and Doctrine

All findings above are derived from the in-workspace JSON/MD outputs as of 2026-05-24 plus a bounded web check. No files were modified. Per `RESEARCH_DOCTRINE.md`, evidence levels are noted inline for any claim that goes beyond automated counts. Gap-analysis classifications remain at **BRONZE** validation; any contribution that cites them should add a Cochrane/PROSPERO cross-check.

---

*Generated by automated `diabetes-hub-monitor` task — 2026-05-24*
*Inputs: hub_monitor_report.md (2026-05-24), clinical_trials_latest.json (2026-05-24), pubmed_recent_latest.json (2026-05-24), literature_gap_report.md (2026-05-23), 7-day snapshot diff vs. 2026-05-17.*
