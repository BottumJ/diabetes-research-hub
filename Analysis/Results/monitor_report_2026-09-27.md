# Diabetes Research Hub — Monitor Report
**Run date:** 2026-09-27 (automated Cowork review — no files modified)

---

## File System Status

| File | Last modified | Age | Status |
|---|---|---|---|
| `hub_monitor_report.md` | 2026-07-17 | **72 days** | 🔴 STALE — local `hub_monitor.py` has not run since mid-July |
| `clinical_trials_latest.json` | 2026-07-17 | **72 days** | 🔴 STALE — never overwritten since |
| `clinical_trials_summary.md` | 2026-07-17 | **72 days** | 🔴 STALE |
| `Diabetes_Research_Tracker.xlsx` (master tracker) | 2026-07-17 | **72 days** | 🔴 STALE — same day everything else stopped |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 | 21 days | 🟡 Stale but usable — newer data exists, just never promoted to "latest" |
| `literature_gap_data.json` | 2026-09-19 | 8 days | 🟢 OK (under 14-day threshold) |
| `literature_gap_report.md` | 2026-09-26 | 1 day | 🟢 Fresh |
| `pubmed_recent_latest.json` | 2026-09-26 | 1 day | 🟢 Fresh |

**Root cause pattern:** Four files that all depend on the user's local Python scripts (`hub_monitor.py`, `baseline_clinical_trials.py`, and whatever writes the tracker) stopped updating on the *same day*, 2026-07-17, and haven't moved since — 72 days. Meanwhile the PubMed-alert and gap-analysis pipeline kept running on its own cadence (most recently yesterday), so it looks like the **local-machine half of the pipeline stalled** while the hosted/scheduled half kept going.

Separately: four snapshot files *do* exist for clinical trials between the July gap (`clinical_trials_snapshot_2026-08-27.json`, `08-28`, `09-01`, `09-06`) tagged `"acquired_by": "cowork scheduled monitor (sandbox) - replicates baseline_clinical_trials.py"` — i.e., a prior automated run fetched fresh trial data itself, but **never wrote it into `clinical_trials_latest.json`**, so every downstream report reading "latest" is still reading July 17th data. Nothing has refreshed clinical trial data at all in the last 21 days.

**Git status (bears directly on the above):** the local repo is **124 commits ahead of `origin/main`**, unpushed since 2026-04-20 (per the repo's own `ACTION_REQUIRED_2026-09-15/16/17/18/19/20/21.md` files, which have flagged this every day for at least a week). One of the unpushed corrections removes a fabricated clinical figure ("belatacept: 70% graft survival at 10 years") that a fix already exists for locally but that readers of the live site are still seeing, because it was never pushed. This was not fixed by this run — pushing requires credentials this review has no way to verify or supply, and publishing to the live site is outside what an unattended review should do unilaterally.

---

## Clinical Trial Changes
*(comparing `clinical_trials_snapshot_2026-09-06.json`, the newest data that exists, against `clinical_trials_snapshot_2026-07-17.json` = current "latest")*

- Total trials: 858 → 894 (+57 new, -21 dropped from category criteria)
- 26 status changes, including several notable ones:
  - **RECRUITING → ACTIVE_NOT_RECRUITING** (enrollment closed): GATEWAY (Medtronic NMX8 AID system, NCT07228117); Cadisegliatin adjunct to insulin in T1D (NCT06334133); CD40L monoclonal + islet transplant in brittle T1D (NCT06305286); Revita DMR retreatment in T2D (NCT06092476)
  - **NOT_YET_RECRUITING → RECRUITING**: Orforglipron in T2D patients observing Ramadan fasting (NCT07613307, Eli Lilly); Maridebart Cafraglutide extension trial MARITIME-2-EXTENSION (NCT07684144); Medtronic NMX8 NEXUS system (NCT07227805); Next-gen AID algorithm in adults with T1D (NCT07593625)
- **58 Phase 3 RECRUITING trials** currently open, including from tracked organizations:
  - Vertex: VX-880 pivotal studies (NCT06832410, NCT04786262)
  - Eli Lilly: Baricitinib BARICADE-DELAY and beta-cell-preservation trials (NCT07222137, NCT07222332); Orforglipron Ramadan-fasting study (NCT07613307)
  - Novo Nordisk: CagriSema dose-finding (NCT07564414); AMBITION 7 / zenagamtide (NCT07797335)
  - No Sana Biotechnology trials found in the registry (SC451 program is still pre-registration company disclosure per `Research_Findings_Summary.md`)
- **36 trials posted new results since 2026-07-01** in the 09-06 snapshot; most notable: **Orforglipron in adults with obesity/overweight + T2D (NCT05872620, Eli Lilly)** posted results 2026-09-04 — worth a look given orforglipron is one of the eight key therapies this hub tracks.
- No zimislecel (Vertex VX-880) results postings found beyond what's already logged in `Research_Findings_Summary.md`.

---

## PubMed Highlights
*(`pubmed_recent_latest.json`, generated 2026-09-26, 155 unique papers across 16 domains, 30-day lookback)*

**Cross-domain papers (15 of 155 — highest priority):**
- [PMID 42767751] SIRENA protocol — Italian multicentre cohort — *T1D Immunotherapy × teplizumab*
- [PMID 42720752] Preserving beta-cell function in newly-diagnosed stage 3 T1D children/adolescents — *T1D Immunotherapy × teplizumab*
- [PMID 42626948] Gene-edited hypoimmune islets as a T1D cure (review) — *T1D Immunotherapy × teplizumab*
- [PMID 42751099] Sustained >100kg weight loss with sequential incretin therapy in Prader-Willi syndrome — *T2D Remission × retatrutide*
- [PMID 42785112] Evoke(+) trials of semaglutide for early Alzheimer's disease — *T2D GLP-1 × Diabetes Biomarker* (not diabetes-specific but semaglutide-relevant)
- [PMID 42787243] AI-driven diabetic retinopathy research mapping — *Diabetes AI/ML × Diabetes Multi-Omics*
- Remaining 9 are microbiome/multi-omics/epigenetics crossovers — none individually urgent, full list retained in the data file.

**Key-therapy publication counts (30-day window):** dapagliflozin 46 (5 shown), orforglipron 13 (5), retatrutide 12 (5), icodec 8 (5), teplizumab 6 (5), CagriSema 4 (4), baricitinib 2 (2), **zimislecel 0** — no PubMed activity at all on Vertex's lead cell-therapy candidate in the last 30 days.

**Volume trend:** 155 unique papers matched from 1,095 total query hits across 16 domains — consistent with recent snapshots (09-18 through 09-26 all landed in a similar range); no anomalous spike or drop.

---

## Gap Analysis Summary
*(`literature_gap_report.md`, regenerated 2026-09-26 from data generated 2026-09-19 — 30 domains, 435 pairs)*

**Top 5 "meaningful" gaps (Gap Score, all BRONZE — single-source, need expert confirmation):**
1. Beta Cell Regen × Health Equity — 100.0 (0 joint pubs)
2. Insulin Resistance × Islet Transplant — 100.0 (1 joint pub)
3. Islet Transplant × Drug Repurposing — 100.0 (0 joint pubs; re-verified 2026-09-06, all-time PubMed search returns 7 unrelated records)
4. Islet Transplant × Health Equity — 100.0 (0 joint pubs)
5. Gene Therapy × LADA — 100.0 (0 joint pubs)

**Alignment with RESEARCH_DOCTRINE.md Tier 1 areas:** Three of the top five gaps sit directly on Tier 1 territory — #4 Drug Repurposing Computational Screening (score 18/20) and #6 Epidemiological/Health Equity analysis (score 17/20) each appear in 3 of the top 5 pairs (#1, #3, #4). Islet Transplant × Drug Repurposing (#3) is the strongest candidate for immediate computational work: it has Data Access 4-5 on both axes and zero competing literature.

---

## Breaking News (web search, last 7 days)

**FDA approved Eli Lilly's Onswik (insulin efsitora alfa-gobe) on 2026-09-24** — the **second** once-weekly basal insulin for adults with type 2 diabetes (after Novo Nordisk's Awiqli/icodec). Based on the QWINT-1 through -4 Phase 3 program (>3,400 adults, NCT05662332/05362058/05275400/05462756), each trial met its primary endpoint of non-inferior A1C reduction vs. daily glargine or degludec, with a similar safety profile. Not indicated for T1D. This directly affects the "icodec" key-therapy track this hub already monitors — Onswik is icodec's direct once-weekly competitor and isn't yet in any tracked file.

No other Phase 3 result or FDA action in the last 7 days cleared the bar for "genuinely significant."

---

## Recommended Actions

1. **Push the 124 unpushed commits** (`git push origin main` from the Diabetes_Research folder) — this has been flagged as P0 for at least a week and a fabricated-figure correction is sitting unpublished on the live site because of it. This review did not attempt it (requires credentials and is a live-site publish action outside an unattended review's remit).
2. **Investigate why the local pipeline stopped on 2026-07-17** — `hub_monitor.py`, `baseline_clinical_trials.py`, and the Excel tracker all went silent that day and never resumed, even though PubMed/gap analysis kept running on a separate (hosted) cadence. Check whatever scheduled the local scripts (Task Scheduler / cron equivalent on the Windows machine).
3. **Re-run `baseline_clinical_trials.py` and overwrite `clinical_trials_latest.json`** — real data exists as recently as 2026-09-06 (in the dated snapshot) but was never promoted to "latest," so every dashboard and report reading "latest" is 72 days stale on top of the 21-day snapshot gap.
4. **Add Onswik/insulin efsitora to the tracked key-therapy list** — it's now a direct competitor to icodec, which is already tracked.
5. **Review the orforglipron obesity/T2D results posting (NCT05872620, posted 2026-09-04)** for the Research Findings Summary.
6. Re-run the full gap analysis (`project1_literature_gap_analysis.py`) — data is 8 days old, still within the 14-day threshold but the 30-domain × 435-pair query is compute-heavy, so refreshing before the 14-day mark avoids doing it twice in a rush.
7. Note for future runs: the task file's Step 4 PMID-fabrication check should use `Analysis/Scripts/audit_impossible_pmids.py` (live-resolves the PubMed ID ceiling) rather than a hardcoded threshold — flagged in `ACTION_REQUIRED_2026-09-21.md` and still applicable.

---
*Generated by automated Cowork review. No files were modified. All data read from `Analysis/Results/`, `RESEARCH_DOCTRINE.md`, and one web search pass.*
