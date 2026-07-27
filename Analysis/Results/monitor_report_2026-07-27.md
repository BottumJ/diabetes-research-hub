# Diabetes Research Hub — Monitor Report

**Run date:** 2026-07-27 (automated, unattended)
**Reviewer:** Hub Monitor (scheduled task)
**Scope:** Review of latest script outputs in `Analysis/Results/`, snapshot diffs, web scan for breaking news.

---

## Headline (read this first)

**The data pipeline is frozen. Your core intelligence feeds last refreshed on 2026-07-17 — 10 days ago.** The review job (this task) has kept running daily and writing reports through 2026-07-26, but it has been reviewing the *same* 2026-07-17 data for ten days. Every "finding" below the fold is really a finding as of July 17. Nothing new has entered the hub since.

`[Certain]` — file modification times and the absence of any `clinical_trials_snapshot_*` / `pubmed_recent_snapshot_*` file dated after 2026-07-17 confirm this directly.

**Fix before anything else:**
```
python baseline_clinical_trials.py      # last real refresh 2026-07-17
python baseline_pubmed_alerts.py        # last real refresh 2026-07-17
python hub_monitor.py                   # last scan 2026-07-17
python project1_literature_gap_analysis.py   # gap data 2026-07-18; report regenerated 07-26
```

---

## File System Status

| File | Last modified | Age (days) | State |
|------|---------------|-----------:|-------|
| `clinical_trials_latest.json` | 2026-07-17 | 10 | **STALE** |
| `pubmed_recent_latest.json` | 2026-07-17 | 10 | **STALE** |
| `hub_monitor_report.md` | 2026-07-17 | 10 | **STALE** |
| `literature_gap_data.json` | 2026-07-18 | 9 | Aging |
| `literature_gap_report.md` | 2026-07-26 | 1 | Fresh (built on 07-18 data) |
| Latest CT snapshot | `..._2026-07-17.json` | 10 | Cadence broken after 07-17 |
| Latest PubMed snapshot | `..._2026-07-17.json` | 10 | Cadence broken after 07-17 |

All five expected input files exist — none are missing. The problem is not absence, it is staleness: the daily snapshot cadence that ran cleanly Mar 15 → Jul 17 stopped producing new snapshots after 2026-07-17. The hub_monitor's own last scan (07-17) already flagged **827 result files older than 14 days**; that count only grows while the pipeline is down.

`[Likely]` The scheduled *review* task and the scheduled *data-collection* scripts are decoupled — the review kept firing while the collectors silently stopped. Worth checking the collector cron/scheduler and its logs (`_gap_run.log` last wrote 2026-06-29).

---

## Clinical Trial Changes

Baseline (2026-07-17): **858 unique trials** — 269 RECRUITING, 151 NOT_YET_RECRUITING, 110 ACTIVE_NOT_RECRUITING, 321 COMPLETED. 136 Phase 3, 126 Phase 2. **52 trials are Phase 3 + RECRUITING** (highest monitoring priority).

Changes are measured across the last real refresh window (snapshot **2026-07-01 → 2026-07-17**): 29 trials added, 8 removed, 10 status changes, 0 newly-posted results on pre-existing trials.

### Notable — new Phase 3 activations (NOT_YET_RECRUITING → RECRUITING)

- **AstraZeneca — coordinated Elecoglipron Phase 3 program (4 trials):** NCT07662044, NCT07662109, NCT07662135, NCT07662213. All Type 2 Diabetes (one also T2D + CKD). A four-trial simultaneous Phase 3 launch of an oral GLP-1 is a serious new entrant to the oral-incretin race. **Recommend adding to the "Notable Trials to Watch" table** (currently empty in `clinical_trials_summary.md`).
- **Gan & Lee Pharmaceuticals** — NCT07527078, Phase 3 → RECRUITING.
- **Novo Nordisk** — NCT07668388, Phase 2 (CagriSema-family dose comparison) → RECRUITING.
- **Medtronic MiniMed** — NCT07675161, device → RECRUITING.

### Key Phase 3 programs from tracked organizations (status as of 07-17)

- **Vertex — zimislecel / VX-880 (islet cell therapy for T1D):** two Phase 3 trials RECRUITING — NCT04786262 and NCT06832410. This is the flagship T1D cell-cure program; keep on close watch for results posting.
- **Eli Lilly — baricitinib for T1D beta-cell preservation:** NCT07222137 and NCT07222332, both Phase 3 RECRUITING. Baricitinib (a tracked therapy) moving into Phase 3 for *T1D beta-cell function* — not just T2D — is strategically relevant to the immunotherapy/prevention domain.
- **Eli Lilly — orforglipron & retatrutide:** multiple Phase 3 (mostly ACTIVE_NOT_RECRUITING or NOT_YET_RECRUITING), consistent with the ADA 2026 readouts (see Breaking News).
- **Novo Nordisk — CagriSema & oral semaglutide/icodec:** several Phase 3 ongoing.

### Recently posted results (surfaced in the 07-17 dataset)
Notable 2026 results postings include Lilly tirzepatide vs dulaglutide (NCT04255433, posted 07-08), Lilly orforglipron long-term safety (NCT06010004, posted 06-30), and Novo icodec switch study (NCT06340854, posted 07-02). No *new* results appeared on pre-existing trials within the 07-01→07-17 diff window — these entered via the "Recently Completed with Results" category.

**Sana Biotechnology:** 0 trials in the current dataset. `[Likely]` Either Sana's hypoimmune islet programs aren't yet on ClinicalTrials.gov under a matching sponsor string, or the query filter misses them. Worth a targeted manual check.

---

## PubMed Highlights

Baseline (2026-07-17): 158 unique papers over a 30-day lookback across 16 alert domains; 8 key therapies tracked.

### Cross-domain papers (highest value — appear in ≥2 alert domains)

- **[42459945]** *A framework for assessing algorithmic discrimination risks in training data: a case of pediatric type 1 diabetes* — **AI/ML × Closed-Loop AP × Health Equity** (triple-domain — the single highest-value hit). Directly on the Tier 1 "Health Equity" + "AI/ML" fault line.
- **[42419792]** *Comparative effects of drugs for adults with overweight or obesity* — **orforglipron × retatrutide × CagriSema** (three tracked therapies in one paper).
- **[42458730]** *Multi-omic modelling of BMI response to a dietary weight-loss intervention* — **Microbiome × Multi-Omics** (Tier 1 #1).
- **[42459212]** *Precision nutrition in Asian populations: a multi-omics review* — **Microbiome × Multi-Omics**.
- **[42453334]** *From In Silico to Clinic: Noncoding RNAs for Diabetes* — **Biomarker × LADA**.
- **[42452353]** Glucose-lowering therapy × myocardial work recovery — **GLP-1 × Remission**.
- **[42436543]** Healthcare inequalities in T2D — **Remission × Health Equity**.
- **[42458355]** Socioeconomic gradients in hypertension — **AI/ML × Health Equity**.
- **[42437645]** Variant-specific pharmacophoric shifts in GLP-1 receptor — **GLP-1 Pharmacogenomics × orforglipron**.

### Key-therapy publication activity (30-day, as of 07-17)

| Therapy | Mentions | Papers |
|---------|---------:|-------:|
| dapagliflozin | 52 | 5 |
| orforglipron | 10 | 5 |
| CagriSema | 6 | 5 |
| retatrutide | 4 | 4 |
| teplizumab | 4 | 4 |
| icodec | 3 | 3 |
| baricitinib | 2 | 2 |
| **zimislecel** | **0** | **0** |

`[Certain]` **zimislecel had zero literature hits** — notable given Vertex has two Phase 3 trials recruiting under the VX-880 name. `[Likely]` the literature indexes it under "VX-880" rather than the INN "zimislecel"; recommend adding "VX-880" as a search alias in `baseline_pubmed_alerts.py`.

### Volume trend
Day-over-day PubMed diff (07-16→07-17) was +28 / −27 papers — normal churn. No domain showed anomalous spikes or blackouts in the last real refresh.

---

## Gap Analysis Summary

Source: `literature_gap_report.md` (regenerated 2026-07-26 on 07-18 gap data). 30 domains, 435 pairs. **Validation level: BRONZE** (single analytical source; requires expert confirmation per Research Doctrine).

### Top 5 under-researched intersections (Gap Score 100 = zero joint publications)

| Rank | Intersection | Gap | Joint pubs |
|------|--------------|----:|-----------:|
| 1 | Treg/CAR-T × Neuropathy | 100 | 0 |
| 2 | Beta Cell Regen × Health Equity | 100 | 0 |
| 3 | Treg/CAR-T × Health Equity | 100 | 0 |
| 4 | Glucokinase × Health Equity | 100 | 0 |
| 5 | Gene Therapy × LADA | 100 | 0 |
| (6) | Drug Repurposing × Health Equity | 100 | 0 |

### Alignment with Tier 1 contribution areas (from RESEARCH_DOCTRINE.md)

The gap findings cluster hard on **Health Equity**, which is Tier 1 #6 (Epidemiological/Equity analysis, score 17/20). Four of the top six gaps are an emerging-therapy domain × Health Equity. That is exactly the kind of pure-computational, publicly-sourced synthesis the doctrine says we are positioned to own — no wet lab, no restricted data.

**Strongest actionable candidate:** **Drug Repurposing × Health Equity** (Gap 100). It sits at the intersection of *two* Tier 1 areas — #4 (Drug Repurposing Computational Screening, 18/20) and #6 (Equity, 17/20) — and both feed off already-open data (DrugBank/OpenTargets + GBD/CDC/IDF). This is the one gap where we have both the tooling and the mandate.

**Caveat `[Likely]`:** several of these zero-pub gaps are terminology artifacts, not true white space. Before committing, run the doctrine's verification step — combined-term PubMed search + a Cochrane/PROSPERO check — to confirm no existing review already covers the intersection.

---

## Breaking News (web scan, ~last 7 days)

Honest read: **nothing genuinely broke in the trailing 7-day window (Jul 20–27).** The significant recent items all cluster around ADA 2026 (June) and a mid-June FDA action. Reporting them because they bear directly on tracked therapies, with correct dates:

- **Teplizumab (Tzield) — FDA approval, pediatric Stage 3 T1D (announced 2026-06-12).** First approved therapy to delay insulin-production decline in ages 8–17 recently diagnosed with Stage 3 T1D. Tracked therapy; directly relevant to the T1D Immunotherapy/Prevention domain. `[Certain]` per FDA press release.
- **Retatrutide — TRANSCEND-T2D-1 Phase 3 (ADA 2026, June).** Triple-hormone (GIP/GLP-1/glucagon); ~1.7–1.9% HbA1c reduction and ~11.5–15.3% weight loss at 40 weeks vs placebo, plus signals in OSA and knee OA pain. Tracked therapy.
- **Orforglipron — Lilly ACHIEVE-3 (ADA 2026).** Positioned as a superior oral GLP-1 for T2D. Tracked therapy; corroborated by the PubMed cross-domain hit [42437645] and the AstraZeneca Elecoglipron Phase 3 launch — the oral-incretin field is heating up.

No verified Phase 3 readout, FDA action, or major publication dated within Jul 20–27 surfaced. Do not treat the above as "new since last report" — they predate the stale 07-17 snapshot and would already be partially captured once the pipeline is re-run.

---

## Recommended Actions

1. **[Priority 1] Restart the data pipeline.** Run `baseline_clinical_trials.py`, `baseline_pubmed_alerts.py`, `hub_monitor.py`, then `project1_literature_gap_analysis.py`. Then investigate *why* collection stopped after 2026-07-17 while the review task kept running (decoupled scheduler — check collector logs).
2. **[Priority 2] Add VX-880 as a PubMed alias for zimislecel** in `baseline_pubmed_alerts.py`. Zero hits on a therapy with two recruiting Phase 3 trials is almost certainly an indexing miss, not a real absence.
3. **Populate "Notable Trials to Watch"** in `clinical_trials_summary.md` (currently empty). Seed it with: Vertex VX-880 Phase 3 (NCT04786262, NCT06832410); Lilly baricitinib T1D beta-cell Phase 3 (NCT07222137, NCT07222332); AstraZeneca Elecoglipron Phase 3 program (NCT07662044/109/135/213).
4. **Verify the Drug Repurposing × Health Equity gap** — it double-hits Tier 1 (#4 + #6) and is the best-founded synthesis target. Run combined-term PubMed + Cochrane/PROSPERO checks before committing, per doctrine.
5. **Review cross-domain paper [42459945]** (algorithmic discrimination in pediatric T1D training data) — triple-domain AI/ML × Closed-Loop × Health Equity, squarely on our Tier 1 equity/AI thesis.
6. **Manual check for Sana Biotechnology trials** — zero in dataset; likely a sponsor-string filter miss.

---

*Evidence conventions per RESEARCH_DOCTRINE.md: gap classifications are BRONZE (single source, expert confirmation pending). File-state and snapshot-diff claims are [Certain] (derived directly from file timestamps and JSON contents). Web/breaking-news items carry their own confidence tags and source dates. This was a review-only run — no existing files were modified.*
