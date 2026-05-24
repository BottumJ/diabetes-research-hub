# Diabetes Research Hub — Monitor Report

**Run date:** 2026-05-21
**Scope:** Automated review of hub outputs since 2026-05-20 (24h) with 7-day context
**Reviewer:** Scheduled monitor (read-only run)

---

## File System Status

All four script-output families are present. Three of the four were refreshed within the last 24 hours; the gap-analysis data file remains stale (now 30 days old) — this is the main actionable file-system finding.

| File | Last modified | Status |
|---|---|---|
| hub_monitor_report.md | 2026-05-21 | Fresh |
| clinical_trials_latest.json | 2026-05-21 | Fresh |
| clinical_trials_summary.md | 2026-05-21 | Fresh |
| pubmed_recent_latest.json | 2026-05-21 | Fresh |
| pubmed_recent_summary.md | 2026-05-21 | Fresh |
| literature_gap_report.md | 2026-05-20 | Fresh |
| **literature_gap_data.json** | **2026-04-20** | **STALE (30d)** |

The hub_monitor.py scan flagged **592 result files older than 14 days** as candidates for refresh — most are historical snapshots that are expected to remain frozen. The actionable item is the gap-analysis JSON, which has now crossed the one-month mark since its last regeneration.

## Clinical Trial Changes

The clinical_trials_latest.json snapshot now contains **795 unique trials** (153 T1D Cure/Cell Therapy, 71 T1D Immunotherapy/Prevention, 141 T2D Novel Therapies, 223 Devices, 280 Completed-with-Results). Status mix: 264 RECRUITING, 136 NOT_YET_RECRUITING, 108 ACTIVE_NOT_RECRUITING, 280 COMPLETED. **122 trials are PHASE3.**

### Last 24h (vs. 2026-05-20 snapshot)
- **1 new trial.** NCT07599982 — *Safety Evaluation of MODI, an Insulin Titration Algorithm, in Adults With Diabetes* (DreaMed Diabetes; NOT_YET_RECRUITING, NA). Algorithm-validation study — relevant to the AID / closed-loop watchlist.
- **3 trials dropped** from the active set (registry-side reclassification rather than completion events):
  - NCT03895437 — *Diabetes Autoimmunity Withdrawn In New Onset and In Established Patients* (was ACTIVE_NOT_RECRUITING)
  - NCT06613711 — *MagDI Italian Study* (was ACTIVE_NOT_RECRUITING)
  - NCT04545151 — *Verapamil SR in Adults With Type 1 Diabetes* (was ACTIVE_NOT_RECRUITING) — note this removal; verapamil/T1D was a watchlist item.
- **2 status changes**, both Magnetic Gastro-Ileal Diversion follow-on studies completing enrollment:
  - NCT06073457: RECRUITING → ACTIVE_NOT_RECRUITING — *MGI/MGJ Study*
  - NCT06467955: RECRUITING → ACTIVE_NOT_RECRUITING — *MagDI Canada Study*
- 0 newly posted results in the last 24h.

### Key Phase 3 trials — current status (no changes today)

| Sponsor | NCT | Therapy | Status |
|---|---|---|---|
| Vertex | NCT04786262 | VX-880 / zimislecel (T1D) | RECRUITING |
| Vertex | NCT06832410 | VX-880 / zimislecel (T1D) | RECRUITING |
| Eli Lilly | NCT07222332 | Baricitinib in children/adolescents (T1D beta-cell preservation) | RECRUITING |
| Eli Lilly | NCT07222137 | Baricitinib to delay Stage 3 T1D | RECRUITING |
| Eli Lilly | NCT06739122 | Dulaglutide 3.0/4.5 mg pediatric T2D | RECRUITING |
| Novo Nordisk | NCT07076199 | Insulin icodec (T2D HbA1c reduction) | RECRUITING |

**Sana Biotechnology:** 0 trials in current snapshot (unchanged).

## PubMed Highlights

The recent-publications snapshot tracks **147 unique papers** across 16 alert domains over a 30-day lookback (up from 145 yesterday). Net: **17 new, 15 dropped** vs. yesterday's snapshot.

### Cross-domain papers (highest-priority signal — 14 papers)
The single new cross-domain paper in the last 24h is:

- **[PMID 42157461]** *Nanostructured High-Entropy Yolk-Shell Oxides Platform for Efficient Metabolic Profiling of Diabetic Retinopathy* (Analytical Chemistry, 2026-May-19) — Domains: **Diabetes AI/ML × Diabetes Biomarker × Diabetes Complications New**. This is a methods/platform paper rather than a clinical finding — relevant to the Biomarker-discovery thread for diabetic retinopathy. Evidence level: BRONZE (single primary methods paper).

Other notable cross-domain papers carried over from the 30-day window:

| PMID | Title (truncated) | Domains |
|---|---|---|
| 42148104 | Adapting CAR-T and CAR-Treg cancer therapies for autoimmunity | T1D Stem Cell Cure × T1D Immunotherapy |
| 42143506 | Evolution of CAR therapies across oncology and autoimmunity | T1D Immunotherapy × Gene Therapy |
| 42138126 | US patterns in islet autoantibody ordering after teplizumab approval | T1D Immunotherapy × Teplizumab |
| 42138080 | New and emerging therapies in T1D (J Clin Invest review) | T1D Immunotherapy × Teplizumab |
| 42051156 | British Society consensus statement on teplizumab in Stage 2 T1D | T1D Immunotherapy × Teplizumab |
| 42154370 | Ocular/extraocular microbiome impact on ophthalmic care | Biomarker × Microbiome × Complications |
| 42152039 | Multi-omics profiling of the diabetic human heart (Genome Medicine) | Biomarker × Multi-Omics |
| 42142983 | Bariatric surgery weight-loss outcomes audit | Retatrutide × CagriSema |

### Key therapy mentions (last 30 days)

| Therapy | Papers | Note |
|---|---|---|
| dapagliflozin | 5 | Mechanism + nanoparticle delivery; first generic dapagliflozin also approved by FDA (see Breaking News) |
| teplizumab | 4 (3 distinct cross-domain) | Real-world utilization and a major society consensus statement |
| retatrutide | 2 | Phase-program follow-on analyses (lipid/metabolite, CKM syndrome) |
| icodec | 2 | ONWARDS-pooled safety + China cost-utility |
| orforglipron | 2 | ATTAIN-MAINTAIN Phase 3b; gastrointestinal safety pooled analysis |
| CagriSema | 1 | Meta-analysis vs. semaglutide monotherapy |
| baricitinib | 1 | Off-label dermatology case report (not T1D) |
| zimislecel | **0** | No PubMed-indexed hits in last 30 days — surprising given the Phase 3 cadence; consider expanding query to "VX-880" and "stem-cell-derived islets" |

### Publication volume — domain deltas (today vs. yesterday)

Up:
- Diabetes AI/ML: 222 (Δ +7)
- Diabetes Biomarker: 159 (Δ +3)
- Diabetes Health Equity: 60 (Δ +2)
- T1D Stem Cell Cure: 23 (Δ +1)
- Diabetes Multi-Omics: 57 (Δ +1)

Down:
- T2D GLP-1 New: 145 (Δ −3)
- T1D Immunotherapy: 22 (Δ −1)
- T2D Remission: 65 (Δ −1)
- Diabetes Gene Therapy: 40 (Δ −1)

The AI/ML uptick continues a multi-day trend and matches the pattern of new papers today (8 of 17 new papers were tagged Diabetes AI/ML — heavy concentration on retinopathy screening models and risk prediction).

## Gap Analysis Summary

The literature_gap_report.md was refreshed on 2026-05-20 but the underlying data JSON is from 2026-04-20 — the report appears to be a re-render rather than a re-query. Top 5 under-researched intersections (unchanged from prior runs; BRONZE validation):

| Rank | Intersection | Gap Score | Joint Pubs |
|---|---|---|---|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 |
| 3 | Islet Transplant × GWAS / Polygenic | 100.0 | 0 |
| 4 | Islet Transplant × Personalized Nutrition | 100.0 | 0 |
| 5 | Islet Transplant × Drug Repurposing | 100.0 | 0 |

**Alignment with Tier 1 contribution areas:**
- **Islet Transplant × Drug Repurposing** (#5) aligns directly with the active *Islet Drug Repurposing* deliverables (islet_repurposing_*.json + reports from 2026-04-03). The existing pipeline is the natural place to close this gap.
- **Beta Cell Regen × Health Equity** (#1) and **Islet Transplant × Health Equity** (#4) remain candidates for an equity-of-access companion synthesis to existing Tier-1 work; no in-flight artifact addresses this yet.
- The teplizumab cross-domain papers above (consensus statement + real-world utilization) provide fresh inputs for the *Autoimmunity T1D × Health Equity* gap (rank not in top 5 but persistent in the unclassified pool).

## Breaking News (last 7 days, web)

Significant items only — routine news skipped.

- **FDA approves first generic dapagliflozin tablets** (Pharmtech / AJMC coverage). Affects affordability of one of our most-cited T2D agents; relevant to the Drug Repurposing × Health Equity thread. Evidence level: SILVER (multiple independent reports).
- **Mazdutide Phase 3 results presented at ADA 2026 (May 2026)** — Innovent presented head-to-head vs. semaglutide in Chinese adults with T2D + obesity, plus a Phase 3 obesity readout. This is a new entrant to the GLP-1/GIP/glucagon co-agonist class not currently tracked in our key-therapy list; consider adding "mazdutide" to baseline_pubmed_alerts.py therapy queries. Evidence level: SILVER (conference results, peer-reviewed manuscript pending).
- **MannKind Afrezza pediatric sNDA — PDUFA May 29, 2026.** Decision expected next week. If approved, would be the first needle-free insulin for pediatric patients. Worth a tracker entry under Youth Diabetes / Insulin Delivery. Evidence level: SILVER (regulatory filing public).
- **Vertex VX-880 / zimislecel:** ongoing Phase 3 cadence (no new readout in last 7 days). Notable that the zimislecel PubMed query returned zero hits — confirm the alert string captures both "VX-880" and "zimislecel" so we don't miss a peer-reviewed readout when it arrives.

No FDA actions or Phase 3 readouts flagged in the last 7 days that contradict items already in the tracker.

## Recommended Actions

1. **Re-run gap analysis.** `python project1_literature_gap_analysis.py` — literature_gap_data.json is 30 days old; the report rendered on 2026-05-20 appears to be a re-render of stale data.
2. **Add mazdutide to alert queries.** Update `baseline_pubmed_alerts.py` to include "mazdutide" alongside the existing 8 key therapies; Phase 3 ADA readout just occurred and we have no current coverage.
3. **Verify zimislecel alert breadth.** Zero PubMed hits in last 30 days for zimislecel despite an active Phase 3 program is suspicious — confirm the query also matches "VX-880" and "stem-cell-derived islets".
4. **Review cross-domain paper PMID 42157461.** *Nanostructured platform for diabetic retinopathy metabolic profiling* — relevant to Biomarker discovery deliverable; add to paper_library if novel.
5. **Tracker updates needed:**
   - Mark NCT06073457 and NCT06467955 (MGI/MGJ + MagDI Canada) as moved to ACTIVE_NOT_RECRUITING.
   - Note NCT04545151 (Verapamil SR T1D) removal from the active set — confirm whether this was deliberate (completion/withdrawal) before deleting from internal trackers.
   - Add NCT07599982 (DreaMed MODI insulin-titration algorithm) under the Device / AID watch.
6. **Watch list — week ahead:** MannKind Afrezza pediatric PDUFA decision expected 2026-05-29; flag for follow-up next Monday's monitor run.

---

*Generated by scheduled hub monitor on 2026-05-21. This is a read-only review — no source files were modified.*
