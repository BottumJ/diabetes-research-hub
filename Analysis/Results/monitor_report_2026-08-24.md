# Diabetes Research Hub — Monitor Report
**Run date:** 2026-08-24 (automated, review-only — no files modified)
**Prior monitor report:** 2026-08-23
**Data vintage under review:** 2026-07-17 — day **38** of the acquisition freeze

---

## Headline: the fix prescribed on 08-23 was not applied. Nothing acquired today either.

The 08-23 report identified the root cause and gave a four-line PowerShell fix. Re-checked this
morning, all four failure signatures are byte-for-byte unchanged:

| Check | 08-23 | 08-24 | Meaning |
|---|---|---|---|
| `find . -iname "daily_pipeline*"` | 0 results | **0 results** | wrapper still never invoked |
| `Analysis/Results/logs/` exists | no | **no** | `refresh.ps1` still never invoked |
| newest `Analysis/Logs/*` | `gap_analysis_2026-07-17.log` | **same file** | no acquisition since 07-17 |
| newest trial/PubMed snapshot | `..._2026-07-17.json` | **same file** | no new snapshot |

`md5sum` confirms `clinical_trials_latest.json` is bit-identical to
`clinical_trials_snapshot_2026-07-17.json`, and likewise for PubMed. These are not "latest"
files; they are 38-day-old files wearing the name.

**[Certain]** — the daily pipeline has not run. **[Certain]** — the 08-23 remediation was not executed.
This is now the only finding on this page that matters; everything below is a description of data
that has not moved.

**Run this. It is 30 seconds:**

```powershell
cd "C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts"
powershell -ExecutionPolicy Bypass -File "register_daily_task.ps1"
Get-ScheduledTaskInfo -TaskName "DiabetesHub_DailyPipeline"
Start-ScheduledTask   -TaskName "DiabetesHub_DailyPipeline"
```

---

## The freeze is no longer cost-free — here is the receipt

Until now the freeze was an availability problem. It is now a **correctness** problem: the frozen
snapshot asserts trial statuses that are provably wrong as of today.

Counting trials in the 07-17 snapshot whose own recorded `completion_date` has since passed while
their recorded `status` is still not `COMPLETED`:

```
118  trials  total, completion date passed, status still not COMPLETED
 14  of those crossed the line DURING the freeze (07-17 → 08-24)
  6  of those 14 are Phase 2 or Phase 3
```

The six Phase 2/3 records the hub is currently reporting incorrectly:

| NCT | Recorded completion | Status the hub still reports | Phase | Sponsor |
|---|---|---|---|---|
| NCT07064486 | 2026-07-31 | RECRUITING | 3 | BrightGene (BGM0504, T2D) |
| NCT07271251 | 2026-08-03 | ACTIVE_NOT_RECRUITING | 3 | Novo Nordisk (oral semaglutide formulations) |
| NCT06926842 | 2026-08-13 | ACTIVE_NOT_RECRUITING | 2 | Zealand Pharma (petrelintide) |
| NCT06810726 | 2026-08-15 | RECRUITING | 2 | Estar Medical (Tropocells PRF) |
| NCT06797869 | 2026-08-21 | ACTIVE_NOT_RECRUITING | 2 | Novo Nordisk (CagriSema) |
| NCT07321678 | 2026-08 | ACTIVE_NOT_RECRUITING | 2 | Ascletis Pharma |

```
completion dates crossing during the freeze
07-17                                                    08-24
  |                                                        |
  |     07-31      08-03   08-13  08-15        08-21       |
  |       ▌          ▌       ▌      ▌            ▌         |
  ├───────┴──────────┴───────┴──────┴────────────┴─────────┤
  ╳ last acquisition          14 records silently went wrong
```

Note the direction of the error: **all 118 drift in the same direction** (toward under-reporting
completion). A frozen trial registry does not produce random noise, it produces a systematic bias
that always understates how far the field has moved. Any downstream count of "active Phase 3
programs" published from this hub today is inflated.

---

## File System Status

| File | Last modified | Age | State |
|---|---|---|---|
| `clinical_trials_latest.json` | 2026-07-17 | 38 d | **STALE** — identical to 07-17 snapshot |
| `pubmed_recent_latest.json` | 2026-07-17 | 38 d | **STALE** — identical to 07-17 snapshot |
| `literature_gap_data.json` | 2026-07-18 | 37 d | **STALE** |
| `hub_monitor_report.md` | 2026-07-17 | 38 d | **STALE** — reports a scan that is 38 days old |
| `literature_gap_report.md` | 2026-08-23 | 1 d | **MISLEADING** — see below |
| `agent_state.json` | 2026-08-23 | 1 d | live (derived layer) |

### Freshness illusion — flag this

`literature_gap_report.md` carries **"Generated: 2026-08-23 09:05"** in its header. Its underlying
`literature_gap_data.json` has `"generated": "2026-07-17T10:14:41"` and
`"date_range": "2020/01/01 to 2026/07/17"`.

The derived layer is re-rendering frozen inputs and stamping them with today's date. A reader who
checks the header — which is what a header is for — concludes the analysis is one day old. It is
thirty-eight. The same pattern applies to every dashboard in `Dashboards/` regenerated since 07-17.

**Recommendation:** report generators should stamp *source data vintage*, not render time, or print
both. This is a one-line change in the generator and it removes a whole class of silent error.

Also: `hub_monitor_report.md` still says *"827 result file(s) older than 14 days — may need refresh"* —
a number computed on 2026-07-17 and now itself 38 days stale. The staleness detector is stale.

---

## Clinical Trial Changes

**New/changed since last snapshot: zero.** No snapshot has been taken to diff against. The last real
diff on record (07-16 → 07-17) was 1 new trial, 1 removed, 0 status changes, 0 new results.

Snapshot composition, for reference only (858 trials, all figures 38 days old):

| Category | n |  | Status | n |
|---|---:|---|---|---:|
| Diabetes Recently Completed with Results | 321 | | COMPLETED | 321 |
| Diabetes Technology (Devices) | 236 | | RECRUITING | 269 |
| T1D Cure & Cell Therapy | 152 | | NOT_YET_RECRUITING | 151 |
| T2D Novel Therapies (Ph 2-3) | 147 | | ACTIVE_NOT_RECRUITING | 110 |
| T1D Immunotherapy & Prevention | 76 | | ENROLLING_BY_INVITATION | 7 |

52 Phase 3 trials recruiting. Key-organization programs being tracked (Vertex, Lilly, Novo, Sana):

- **Vertex** — NCT06832410 (VX-880 Ph3, RECRUITING, completion 2027-09), NCT04786262 (VX-880 Ph3,
  RECRUITING, completion 2030-06), NCT05791201 (VX-264 Ph1/2, ACTIVE_NOT_RECRUITING)
- **Lilly** — baricitinib beta-cell preservation NCT07222332 and Stage-3 delay NCT07222137 (both Ph3
  RECRUITING); retatrutide NCT05929079 / NCT06297603 / NCT06260722; orforglipron NCT06993792 /
  NCT06972472 / NCT07668336 / NCT07613307; tirzepatide T1D NCT06962280
- **Novo Nordisk** — CagriSema NCT06534411 / NCT07282613 / NCT07564414 / NCT06797869; icodec
  NCT07076199; AMAZE-8 NCT07400107
- **Sana Biotechnology** — **zero trials matched.** Also zero trials mention "zimislecel" by name
  (Vertex's programs are indexed under "VX-880" only), while `pubmed_recent_latest.json` does track
  zimislecel as a key therapy. The trial and literature trackers are using different vocabularies for
  the same asset. Worth a synonym map in `baseline_clinical_trials.py`.

---

## PubMed Highlights

158 unique papers, 16 domains, 30-day lookback — all ending 2026-07-17. Domain volumes are flat
across all 16 domains, so no volume-trend signal can be read from a single frozen pull.

**Cross-domain papers (12 of 158, 7.6%)** — highest-value per the doctrine:

| PMID | Domains | Title (trunc.) |
|---|---|---|
| 42459945 | AI/ML × Closed Loop AP × **Health Equity** | Framework for assessing algorithmic discrimination risks in training data: pediatric T1D case |
| 42411999 | T1D Stem Cell Cure × T1D Immunotherapy | T1D driven by residual recipient T cells after hematopoietic cell transplant |
| 42453334 | Biomarker × LADA | From in silico to clinic: noncoding RNAs for diabetes |
| 42452353 | GLP-1 New × T2D Remission | Glucose-lowering therapy & myocardial work recovery |
| 42436543 | T2D Remission × Health Equity | Healthcare inequality dynamics in T2D across COVID |
| 42458355 | AI/ML × Health Equity | Socioeconomic gradients in hypertension prevalence/management |
| 42459212 | Microbiome × Multi-Omics | Precision nutrition in Asian populations |
| 42458730 | Microbiome × Multi-Omics | Multi-omic modelling of BMI response to dietary intervention |
| 42437645 | GLP-1 Pharmacogenomics × orforglipron | Variant-specific pharmacophoric shifts in GLP-1R–orforglipron |
| 42419792 | orforglipron × retatrutide × CagriSema | Comparative drug effects in overweight/obesity: systematic review |
| 42394981 | orforglipron × retatrutide | Incretin-based therapies in T2D |
| 42444567 | retatrutide × CagriSema | Medical treatments for obesity: what the future holds |

**PMID 42459945 is the standout.** It is the only triple-domain hit, and it lands on the exact seam
between Tier 1 #5 (AI/ML Prediction) and Tier 1 #6 (Epidemiology / Health Equity). It has been
sitting unreviewed in the frozen pull for 38 days.

Key-therapy tracking is uninformative in its present form — all eight tracked therapies (zimislecel,
orforglipron, retatrutide, CagriSema, baricitinib, teplizumab, icodec, dapagliflozin) return exactly
`2` hits. Eight distinct queries returning an identical count is not a plausible literature signal;
it is a **capped `retmax=2`** in the therapy-hit query. **[Likely]** — worth confirming in
`baseline_pubmed_alerts.py` and raising the cap, because as written the field cannot detect a surge
in publication on any therapy, which is the one thing it exists to do.

---

## Gap Analysis Summary

Top gaps as the report ranks them (BRONZE, 435 pairs, 30 domains):

| Rank | Pair | Gap | Joint |
|---|---|---:|---:|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 |
| 4 | Glucokinase × Health Equity | 100.0 | 0 |
| 5 | Gene Therapy × LADA | 100.0 | 0 |
| 6 | Drug Repurposing × Health Equity | 100.0 | 0 |
| 7 | Insulin Resistance × Islet Transplant | 91.9 | 1 |

### Challenge: ranks 1–6 are not a ranking

Ten pairs in `literature_gap_data.json` score **exactly 100.0**. The formula
`max(0, 1 − joint/geomean) × 100` saturates at 100 the instant `joint == 0`, and carries no
information about *how much* was expected. The tie-break producing "rank 1" versus "rank 6" is
undefined — presenting them as an ordered list implies a precision the metric does not have.

The discriminating quantity is already in the data (`expected`) and is not being used. Re-ranking
the ten tied pairs by **absolute expected shortfall**:

```
GWAS/Polygenic  × Closed Loop/AP    expected 25.4  ████████████████████████
Drug Repurposing× CGM Technology    expected 10.2  ██████████
Treg/CAR-T      × Neuropathy        expected  7.5  ███████        <- report's "rank 1"
Beta Cell Regen × Health Equity     expected  7.3  ███████
Treg/CAR-T      × Health Equity     expected  4.7  █████
Glucokinase     × Health Equity     expected  4.3  ████
Gene Therapy    × LADA              expected  3.3  ███
Islet Transplant× GWAS/Polygenic    expected  3.3  ███
Personalized Nut× Closed Loop/AP    expected  3.2  ███
Drug Repurposing× Health Equity     expected  3.0  ███        <- report's "rank 6"
```

The two largest genuine shortfalls are both already filed under *"methodologically distinct — expect
low overlap."* That classification may well be correct, but it is doing a lot of work: it removes the
two biggest anomalies from consideration on a judgement call, leaving a top-6 whose members differ by
a factor of 2.5 in expected shortfall while being presented as equivalent-and-ordered. **[Likely]** —
the "meaningful vs. methodologically distinct" split is the highest-leverage thing to get expert eyes
on, ahead of any individual gap.

Second observation: **5 of the top 20 gaps involve Health Equity**, a domain with only 1,990
publications — the 6th smallest of 30. Small domains with distinct vocabulary will mechanically
produce zero-overlap pairs. Before treating any Health Equity gap as real, it needs the terminology
check the report's own caveats call for (search the intersection with *disparity*, *access*,
*socioeconomic*, *underserved* rather than the domain's canonical string). Untested, these look as
much like a keyword artifact as a research gap.

### Tier 1 alignment

| Gap | Tier 1 area | Doctrine score |
|---|---|---|
| Drug Repurposing × Health Equity | #4 Drug Repurposing (18/20) + #6 Epi/Equity (17/20) | double Tier 1 |
| Beta Cell Regen × Health Equity | #6 Epi/Equity (17/20) | Tier 1 |
| Treg/CAR-T × Health Equity | #6 Epi/Equity (17/20) | Tier 1 |
| Glucokinase × Health Equity | #6 Epi/Equity (17/20) | Tier 1 |
| Drug Repurposing × CGM *(currently deprioritized)* | #4 Drug Repurposing (18/20) | Tier 1, 2nd-largest shortfall |
| Treg/CAR-T × Neuropathy | none directly | — |
| Gene Therapy × LADA | none directly | — |

Every equity-adjacent gap routes to the same Tier 1 area (#6), which is why the terminology-artifact
question above is not academic — if Health Equity's query string is the problem, four of seven top
gaps evaporate at once.

---

## Breaking News (web check, freeze window 07-17 → 08-24)

Three items post-date the frozen data and are therefore **absent from the hub**:

1. **Garzulys (insulin aspart-fsan) FDA approval — 2026-07-30.** First rapid-acting insulin
   biosimilar to NovoLog. Thirteen days after the freeze. *Evidence: regulatory action, hard.*
2. **Retatrutide TRIUMPH-2 and TRIUMPH-3 Phase 3 completions confirmed — 2026-07-23**, completing all
   four core Phase 3 trials. TRANSCEND-T2D-1 (T2D, n=537, −2.0% HbA1c, 16.8% weight loss) published
   in *The Lancet*. The hub still lists retatrutide Phase 3s as ACTIVE_NOT_RECRUITING with a 2026-05
   completion date it has already passed. *Evidence: Level 1b RCT, peer-reviewed.*
3. **CagriSema REIMAGINE 2** (PMID 42251859, *Lancet*) — already present in the corpus via the
   2026-06-10 pull, so this one is covered; noting it only to confirm the June pipeline worked.

Zimislecel (VX-880) remains **not FDA-approved**; regulatory submission guided for 2026, potential
availability 2027. No change to the hub's Vertex records is warranted on that basis.

Nothing found rises to the level of contradicting an existing hub claim. Items 1 and 2 are additive.

---

## Recommended Actions

**P0 — unblocks everything else**

1. Run `register_daily_task.ps1`, then `Start-ScheduledTask -TaskName "DiabetesHub_DailyPipeline"`.
   Confirm with `Get-ScheduledTaskInfo`. Verify success by the existence of
   `Analysis/Logs/daily_pipeline_2026-08-24.log` — if that file does not appear, the wrapper still
   is not being invoked and the diagnosis needs to move to Task Scheduler itself (principal, stored
   credentials, "run whether user is logged on or not", OneDrive path resolution under the task's
   user context).
2. Decide between the two competing dead orchestrators (`run_daily_pipeline.ps1` vs. `refresh.ps1`)
   and delete the loser. Two inert schedulers is how this failure hid for 38 days.

**P1 — after data flows again**

3. Re-run `python baseline_clinical_trials.py` and diff against `clinical_trials_snapshot_2026-07-17.json`.
   Expect ≥118 status corrections; the six Phase 2/3 records tabled above are the verification set —
   if they do not flip to COMPLETED, the acquisition is not actually refreshing.
4. Re-run `python baseline_pubmed_alerts.py` (38 days × ~28 papers/day ≈ **1,060 papers** are missing,
   of which ~7.6% cross-domain ≈ **80 cross-domain papers unreviewed**).
5. Re-run `python project1_literature_gap_analysis.py` — data is 37 days old.
6. Re-run `python hub_monitor.py` — its file-change baseline is 38 days old, so its first post-fix
   run will report a large spurious "modified" set. Expect that and do not treat it as signal.

**P2 — defects surfaced today, none blocking**

7. Add a **source-data-vintage** stamp to every report and dashboard generator. Render time alone is
   actively misleading (`literature_gap_report.md` is the live example).
8. Raise the therapy-hit `retmax` in `baseline_pubmed_alerts.py` — all 8 therapies returning exactly
   2 hits means the field cannot detect a publication surge.
9. Add a synonym map to `baseline_clinical_trials.py` (zimislecel ↔ VX-880 at minimum) so trial and
   literature trackers share a vocabulary. Also confirm Sana Biotechnology's queries are correct —
   zero matched trials for a tracked key organization is more likely a query defect than a real zero.
10. Re-rank `literature_gap_data.json` by absolute expected shortfall alongside gap score, and stop
    presenting the ten 100.0-tied pairs as an ordered list.
11. Route the Health Equity domain's query string to expert review before acting on any of the four
    equity gaps.

**P3 — highest-value item that requires no pipeline fix at all**

12. Review **PMID 42459945** — *"A framework for assessing algorithmic discrimination risks in
    training data: a case of pediatric type 1 diabetes."* Only triple-domain paper in the pull
    (AI/ML × Closed Loop AP × Health Equity), sitting on the Tier 1 #5 / #6 seam. Readable today.

---

## Evidence Levels (per Research Doctrine)

| Claim | Level | Basis |
|---|---|---|
| Pipeline has not run since 2026-07-17 | **[Certain]** | zero `daily_pipeline_*.log`; `Analysis/Results/logs/` absent; md5 identity of latest↔07-17 snapshots |
| 08-23 remediation not executed | **[Certain]** | all four failure signatures unchanged in 24 h |
| 118 trials now mis-stated, 14 during freeze | **[Certain]** | computed from snapshot's own `completion_date` vs. `status` |
| Retatrutide Ph3 program complete; Garzulys approved | **Level 1b / regulatory** | *Lancet*; FDA announcement |
| Therapy-hit counts capped at 2 | **[Likely]** | 8/8 identical counts; needs source read of `baseline_pubmed_alerts.py` |
| Health Equity gaps are terminology artifacts | **[Guessing]** | plausible mechanism (small domain, distinct vocabulary), untested — resolve by re-querying the intersection with synonym expansion |
| Gap classifications | **BRONZE** | single analytical source, expert confirmation pending |

---

*Generated by the Diabetes Research Hub monitor — review-only run, 2026-08-24. No files were modified.*
