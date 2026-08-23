# Diabetes Research Hub — Monitor Report
**Run date:** 2026-08-23 (automated, review-only — no files modified)
**Prior monitor report:** 2026-08-22
**Data vintage under review:** 2026-07-17 (day **37** of the acquisition freeze)

---

## Headline: the 08-22 report asked "what invokes the baseline scripts, and why did it stop?" — here is the answer

The invoker is a **Windows Task Scheduler job named `DiabetesHub_DailyPipeline`**, defined in
`Analysis/Scripts/register_daily_task.ps1`, which launches `run_daily_pipeline.ps1` daily at 5:00 AM.
That wrapper calls `run_daily_local.py`, which runs the four acquisition scripts in order.

**The evidence says that wrapper has never executed — not once.**

`run_daily_pipeline.ps1` writes `Analysis/Logs/daily_pipeline_<yyyy-MM-dd>.log` unconditionally
on *every* invocation, before it does anything else, and appends even on the failure paths
(Python-not-found, orchestrator-missing). A run that fails still leaves a log.

```
find . -iname "daily_pipeline*"     ->  (zero results)
git log --all -- "**/daily_pipeline*" ->  (zero results)
Analysis/Logs/ contents:
    1_trials.log              2026-07-03
    2_pubmed.log              2026-07-03
    3_gap.log                 2026-07-03
    4_hub.log                 2026-07-03
    gap_analysis_2026-07-17.log  2026-07-17   <- last acquisition, hand-run
```

Zero `daily_pipeline_*.log` files have ever existed anywhere in the repo or its history.
**[Certain]** — the wrapper never ran. **[Likely]** — because `register_daily_task.ps1` was
never executed, so the scheduled task was never created. It is a "run this ONCE" script that
appears to have been written and then not run.

### The timeline lines up exactly

`git log` puts the last commit touching any pipeline script at **7715b48, 2026-07-18**:

```
Analysis/Scripts/gap_analysis_daily.py
Analysis/Scripts/hub_monitor.py
Analysis/Scripts/project1_literature_gap_analysis.py
Analysis/Scripts/register_daily_task.ps1     <- new orchestration
Analysis/Scripts/run_daily_local.py          <- new orchestration
Analysis/Scripts/run_daily_pipeline.ps1      <- new orchestration
```

That commit message ends "pipeline 41/41 OK" — the 07-17 data was pulled *by hand* during that
session (`gap_analysis_2026-07-17.log`), the new automation was authored to replace whatever ran
before, and then nothing invoked it. The hub has been running on that one manual pull for 37 days.

```
   scripts rewritten to a new orchestrator
                  |
  ...──data──data──╳────────── 37 days, no data ──────────▶  2026-08-23
   07-15  07-16  07-17/18                                     (today)
                  |
         new orchestrator never registered
```

### A second, independent orchestrator is also dead

`refresh.ps1` (repo root, wrapping `refresh_hub.py`, last touched 2026-06-23) logs to
`Analysis\Results\logs\` and creates that directory with `-Force` on startup.
**That directory does not exist.** [Certain] `refresh.ps1` has not run either.

So the hub has **two** competing daily orchestrators, both inert, plus a live derived layer
(dashboards, gap reports, corpus extraction) that keeps regenerating from frozen inputs.
That is the whole failure in one sentence.

### Fix

```powershell
cd "C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts"
powershell -ExecutionPolicy Bypass -File "register_daily_task.ps1"
Get-ScheduledTaskInfo -TaskName "DiabetesHub_DailyPipeline"   # confirm LastRunTime / LastTaskResult
Start-ScheduledTask   -TaskName "DiabetesHub_DailyPipeline"   # catch up today
```

Two caveats on the task definition before you register it:

1. `-ExecutionTimeLimit 1h30m` against a gap analysis the docstring puts at 35–40 min, plus
   trials + PubMed. Tight if PubMed throttles. Set `NCBI_API_KEY` (line 30 of
   `run_daily_pipeline.ps1`, currently commented out) to move 3 → 10 req/sec.
2. `-LogonType Interactive` means it runs **only when you are logged on**. If the machine
   sits at the lock screen at 5 AM, `-StartWhenAvailable` covers it; if you are logged out
   entirely, it does not fire. Worth verifying `LastTaskResult` for a week.

Then decide which orchestrator survives and delete the other. Two dead schedulers is how this
stayed invisible for five weeks.

---

## File System Status

| File | Modified | Age | Status |
|---|---|---|---|
| `clinical_trials_latest.json` | 2026-07-17 | 37d | **STALE** — byte-identical to `..._snapshot_2026-07-17.json` (md5 match) |
| `pubmed_recent_latest.json` | 2026-07-17 | 37d | **STALE** — byte-identical to its 07-17 snapshot |
| `literature_gap_data.json` | 2026-07-18 | 36d | **STALE** |
| `hub_monitor_report.md` | 2026-07-17 | 37d | **STALE** |
| `literature_gap_report.md` | 2026-08-22 | 1d | Regenerated, but body reads `Date range: 2020/01/01 to 2026/07/17` |
| Newest trial snapshot | `clinical_trials_snapshot_2026-07-17.json` | 37d | last snapshot in series |
| Newest PubMed snapshot | `pubmed_recent_snapshot_2026-07-17.json` | 37d | last snapshot in series |

The hub's own 07-17 monitor already flagged **827 result files older than 14 days**. That number
has only grown. `agent_state.json` is current (2026-08-22) and dashboards carry 08-21/08-22 file
dates over 07-17 content — a viewer has no way to see the 37-day gap.

---

## Clinical Trial Changes

**No changes to report.** Zero new snapshots since 2026-07-17, so there is nothing to diff.
For context, the 30-day window that *was* captured (06-17 → 07-17) added 45 trials
(813 → 858), which is roughly the volume now unmeasured for a comparable stretch.

Current standing state (all as of 2026-07-17):

| Status | Count |
|---|---|
| COMPLETED | 321 |
| RECRUITING | 269 (52 of them Phase 3) |
| NOT_YET_RECRUITING | 151 |
| ACTIVE_NOT_RECRUITING | 110 |
| ENROLLING_BY_INVITATION | 7 |

**Key-organization trials (64 total).** Vertex — 3, and the two Phase 3 zimislecel/VX-880 arms
are the ones to watch:

| NCT | Status | Phase | n | Program |
|---|---|---|---|---|
| NCT04786262 | RECRUITING | Phase 3 | 52 | VX-880 (zimislecel) |
| NCT06832410 | RECRUITING | Phase 3 | 10 | VX-880 (zimislecel) |
| NCT05791201 | ACTIVE_NOT_RECRUITING | Phase 1/2 | 7 | VX-264 (encapsulated) |

**Sana Biotechnology — 0 trials matched.** Sana's UP421 work is investigator-initiated
(Uppsala) and would not carry Sana as `sponsor`. This is a **query defect, not an absence**:
`baseline_clinical_trials.py` matches sponsor strings only. Recommend adding collaborator-field
and intervention-name matching.

**Results posted in the final captured week (07-10 → 07-16)** — reviewed, nothing overturned:

| Posted | NCT | Phase | Sponsor | Study |
|---|---|---|---|---|
| 2026-07-16 | NCT05086445 | 1 | Eli Lilly | LY3502970 (orforglipron), Japanese T2D |
| 2026-07-15 | NCT05574699 | N/A | Johns Hopkins | Social risk score + CDS + closed-loop referral |
| 2026-07-13 | NCT05254002 | 2 | Bayer | Finerenone combination |
| 2026-07-09 | NCT03263494 | 3 | Jaeb Center | CGM in teens/young adults with T1D |
| 2026-07-08 | NCT04255433 | 3 | Eli Lilly | **Tirzepatide vs dulaglutide, MACE (SURPASS-CVOT)** |

NCT04255433 is the one worth a read — a Phase 3 cardiovascular outcomes trial with results
now posted. [Guessing] on whether the posted tables add anything beyond the published readout;
confirming requires pulling the results module, which the frozen snapshot does not contain.

---

## PubMed Highlights

Frozen at 158 unique papers across 16 domains, 30-day lookback ending 2026-07-17.

**Domain volume** (using `total_count`, the uncapped esearch `<Count>` — per the 08-22
correction, `paper_count` is retmax-capped and is not a volume signal):

```
Diabetes AI/ML             ████████████████████████ 260
Diabetes Microbiome        █████████████████ 186
T2D GLP-1 New              ███████████████ 167
Diabetes Biomarker         ███████████████ 166
Diabetes Health Equity     ██████ 72
Diabetes Multi-Omics       ██████ 65
T2D Remission              █████ 59
Diabetes Gene Therapy      ███ 42
Closed Loop AP             ███ 38
Diabetes Complications     ███ 34
T1D Immunotherapy          ██ 25
T1D Stem Cell Cure         █ 17
LADA New Research          █ 12
Diabetes Drug Repurpose    ▌ 8
Diabetes Epigenetics       ▌ 5
GLP-1 Pharmacogenomics     ▏ 1
```

The bottom four are Tier 1 doctrine areas (Drug Repurposing #4, and pharmacogenomics feeding
Multi-Omics #1) sitting at single-digit monthly volume. That is the intended signal — thin
fields are where a computational contribution moves the needle — but at n=1 for GLP-1
Pharmacogenomics the count is as likely a **query-specificity artifact** as a real gap.
[Guessing] which. Worth auditing the query string before treating it as an opportunity.

**Key therapies** (`total_count` / `paper_count`):
dapagliflozin 52/5 · orforglipron 10/5 · CagriSema 6/5 · retatrutide 4/4 · teplizumab 4/4 ·
icodec 3/3 · baricitinib 2/2 · **zimislecel 0/0**.

Zimislecel at zero, while Vertex runs two Phase 3 arms, is the same defect as the Sana miss:
the literature still says VX-880. Recommend the therapy tracker query become
`zimislecel OR VX-880`.

**Cross-domain papers** — the last three captured (07-16 → 07-17), still the most recent the
hub knows about:

- PMID **42459945** — *A framework for assessing algorithmic discrimination risks in training data: a case of pediatric type 1 diabetes* — Diabetes AI/ML ∩ Closed Loop AP ∩ Diabetes Health Equity. Three domains, and it sits directly on the Tier 1 #5 (AI/ML prediction) ∩ Tier 1 #6 (health equity) seam. **Highest-priority read in this report.**
- PMID **42458730** — *Multi-omic modelling of body mass index response to a dietary weight loss intervention* — Microbiome ∩ Multi-Omics.
- PMID **42459212** — *Precision nutrition in Asian populations: a multi-omics review* — Microbiome ∩ Multi-Omics.

---

## Gap Analysis Summary

From `literature_gap_report.md` (regenerated 2026-08-22, but computed over data ending
2026-07-17). Validation level **BRONZE** — single analytical source, requires expert
confirmation, per the Research Doctrine.

Top 5 "potentially meaningful" intersections:

| # | Pair | Gap | Joint pubs | Tier 1 alignment |
|---|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 | — |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 | **Tier 1 #6** (Epidemiological / equity) |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 | **Tier 1 #6** |
| 4 | Glucokinase × Health Equity | 100.0 | 0 | **Tier 1 #6** |
| 5 | Gene Therapy × LADA | 100.0 | 0 | — |
| 6 | Drug Repurposing × Health Equity | 100.0 | 0 | **Tier 1 #4 ∩ #6** |

**Four of the top six are the same pair with a rotating partner: `× Health Equity`.**
That is worth naming as a pattern rather than six findings. Two readings, and they are not
equally flattering:

- *Real:* equity analysis genuinely does not follow advanced therapies into the literature — which is exactly the Tier 1 #6 thesis, and #6 (Drug Repurposing × Health Equity) is a clean two-Tier-1 intersection.
- *Artifact:* "Health Equity" is a broad, terminology-unstable field, and the gap formula punishes any pair where one side's vocabulary does not co-occur with the other's. A gap score of 100 with **0 joint publications** cannot distinguish "unexplored" from "wrong keyword."

The report's own caveats say this. `falsify_equity_gaps.py` (2026-08-17) exists in Scripts and
appears aimed at precisely this question — I did not run it (review-only). **[Likely]** the
equity cluster is at least partly a terminology artifact; resolving it is a prerequisite to
promoting any of these past BRONZE.

Rank 7, **Insulin Resistance × Islet Transplant** (gap 91.9, 1 joint pub), is the most
defensible of the set — narrow, mechanistically specific, and both sides have stable MeSH
vocabulary. It is the one I would take to a domain expert first.

---

## Breaking News

Three items from the last 30 days that the hub **did not capture** because acquisition stopped
on 07-17. Each is a concrete cost of the outage.

- **Retatrutide TRIUMPH-2 Phase 3 read out 2026-07-23** — six days after the freeze. n=1,152, obesity with T2D: 20.8% weight loss at 12 mg, HbA1c −1.5% at 12 mg (−1.6% at 9 mg) from 7.7% baseline. Lilly stated it will file a BLA in Q1 2027. Hub therapy tracker still shows retatrutide at 4 papers / 4 hits.
- **CagriSema REIMAGINE 1 Phase 3a presented** — n=189 adults with T2D, 40 weeks: HbA1c −19.7 / −16.4 mmol/mol vs −1.1 placebo; weight −13.8% / −11.8% vs −1.4%.
- **Orforglipron — three further ACHIEVE Phase 3 studies presented.** The hub holds one Phase 1 Japanese result (NCT05086445, posted 07-16) and nothing after.
- **Zimislecel:** no FDA action located as of 2026-08-23. Holds RMAT + Fast Track (FDA), PRIME (EMA), ILAP Innovation Passport (MHRA); Vertex has guided to FDA/EMA/MHRA submissions during 2026. Worth a standing watch — this is Tier 1 #3 territory and the single highest-impact T1D event on the horizon.

Evidence level for all four: **secondary reporting, not primary source.** Per the Research
Doctrine these are BRONZE at best and must be re-derived from ClinicalTrials.gov / PubMed
before entering the tracker.

---

## Recommended Actions

**1 — Register the scheduled task. This is the only action that matters today.**
```powershell
cd "C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts"
powershell -ExecutionPolicy Bypass -File "register_daily_task.ps1"
Get-ScheduledTaskInfo -TaskName "DiabetesHub_DailyPipeline"
```
Everything below is downstream of this. If it is not done, this report is identical on 2026-09-23.

**2 — Catch up the 37-day gap manually, now:**
```powershell
cd "C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts"
$env:NCBI_API_KEY = "<your key>"     # 3 -> 10 req/sec; the gap step is 465 sequential queries
python run_daily_local.py
```
(~40–50 min. Do not run this in the Cowork sandbox — the 45 s command cap is why this pipeline
was moved local in the first place, per `run_daily_local.py`'s own docstring.)

**3 — Delete one of the two orchestrators.** `refresh.ps1` + `refresh_hub.py` (06-23) and
`run_daily_pipeline.ps1` + `run_daily_local.py` (07-17) both claim the daily slot; neither runs.
Keep the 07-17 pair, retire the other, so the next failure has one place to look.

**4 — Add a staleness gate to the derived layer.** Dashboard builders and
`project1_literature_gap_analysis.py` should refuse to write — or stamp a visible warning banner —
when their input JSON is more than N days old. The reason this ran 37 days unnoticed is that
every dashboard kept reporting a fresh *file* date over stale *content*. A gate turns a silent
failure into a loud one. `regression_suppression_gate.py` (08-20) is a working precedent.

**5 — Fix two query defects surfaced above:**
   - `baseline_clinical_trials.py`: match collaborator + intervention fields, not sponsor alone (Sana → 0 trials is a false negative).
   - `baseline_pubmed_alerts.py`: therapy tracker should query `zimislecel OR VX-880`; audit the `GLP-1 Pharmacogenomics` query string, which returns n=1.

**6 — Read PMID 42459945** (algorithmic discrimination in pediatric T1D training data) — 3-domain
cross-hit on the Tier 1 #5 ∩ #6 seam, and the most actionable single paper in the frozen set.

**7 — Run `falsify_equity_gaps.py`** before promoting any `× Health Equity` gap above BRONZE.
Four of the top six gaps share that one term; if it is a terminology artifact, four findings
collapse at once.

**8 — Re-derive the three Phase 3 readouts** (retatrutide TRIUMPH-2, CagriSema REIMAGINE 1,
orforglipron ACHIEVE) from primary sources before they enter `Diabetes_Research_Tracker.xlsx`.
Web-search secondary reporting does not clear the Doctrine's evidence bar.

---

*Review-only run. No files in the hub were modified.*
