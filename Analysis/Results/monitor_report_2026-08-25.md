# Diabetes Research Hub — Monitor Report

**Run date:** 2026-08-25 (automated, review-only — no files modified)
**Prior monitor report:** 2026-08-24
**Data vintage under review:** 2026-07-17 — day **39** of the acquisition freeze

---

## Headline: the prescription has been wrong for three days. It asked you to fix the *scheduler*. The data problem needs one command and no scheduler at all.

The 08-23 and 08-24 reports both led with `register_daily_task.ps1` — register a Windows scheduled
task, then start it. That has now failed to happen three mornings running. Rather than print it a
fourth time, this report asks the question the last three avoided: *why has a 30-second fix not been
executed in 72 hours?*

The likely answer is that it isn't a 30-second fix. It has dependencies — being at the machine, an
unblocked PowerShell execution policy, Task Scheduler registering under the right principal, and a
verification step that requires waiting until the next 5 AM to confirm. It is a **scheduling** fix
being prescribed for a **data** problem.

The data problem is separable and smaller:

```
python "C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts\run_daily_local.py"
```

That is the whole thing. `run_daily_local.py` is the orchestrator that Task Scheduler was *going* to
call. It runs all four acquisition steps in order, and it does not need PowerShell, Task Scheduler,
registration, admin rights, or a 5 AM window. Verified present and intact this morning:

| Step | Script | Present | Last modified |
|---|---|---|---|
| 1 | `baseline_clinical_trials.py` | yes | 2026-03-15 |
| 2 | `baseline_pubmed_alerts.py` | yes | 2026-04-17 |
| 3 | `gap_analysis_daily.py` | yes | 2026-07-18 |
| 4 | `hub_monitor.py` | yes | 2026-07-17 |
| — | `run_daily_local.py` (orchestrator) | yes | 2026-07-17 |

**[Certain]** — nothing in the acquisition layer is broken. No script is missing, no import is
failing, no API is refusing. Thirty-nine days of frozen data are the result of nobody typing one
line. Fix the data today; fix the schedule whenever it is convenient.

---

## What actually broke — the orchestration audit (new today)

Previous reports diagnosed this at the Windows layer. Looking one level up, at the Cowork scheduled
tasks, the failure is more structural than "a task didn't register."

**Five automations touch this hub. Four of them read. The one that runs scripts is set to Manual.**

| Task | Schedule | Enabled | Does it acquire data? |
|---|---|---|---|
| `diabetes-data-pull` | daily 06:04 | yes | **No** — charter says "Read-only, runs no scripts" |
| `diabetes-hub-monitor` (this) | daily 02:36 | yes | **No** — review-only by design |
| `diabetes-research-iterate` | daily 03:05 | yes | **No** — vets/audits the existing corpus |
| `weekly-platform-audit` | Sunday 09:05 | yes | **No** — dashboard/citation audit |
| `diabetes-hub-daily-build` | **Manual only** | yes | see below |

Two consequences fall out of that table.

### 1. `diabetes-hub-daily-build` would not have fixed this either

It is tempting to look at that table, see the one task that runs Python, and set it to daily. That
would not have helped. It runs `run_quality_improvements.py`, and that file contains **zero**
references to `baseline_clinical_trials.py`, `baseline_pubmed_alerts.py`, `gap_analysis_daily.py`,
or `hub_monitor.py`:

```
grep -icE 'baseline_clinical|baseline_pubmed|gap_analysis_daily|hub_monitor' run_quality_improvements.py
0
```

Its 31 scripts rebuild dashboards, verify PMIDs, ingest papers and validate citations — the derived
layer, exclusively. **[Certain]** — the "build suite" builds; it does not fetch. Setting it to daily
would produce more re-renders of 39-day-old inputs, which is precisely the failure mode already in
progress.

This is the same defect class the 08-22 iteration logged: *"extraction step was never in the
pipeline."* A step that everyone assumes is in the orchestrator is not in the orchestrator. It has
now happened twice. **Recommendation:** print the executed step list at the top of every
orchestrator's log, so the assumption is checkable without reading source.

### 2. The read layer is running perfectly and that is the problem

```
              acquisition                            reporting
    ┌───────────────────────────────┐   ┌──────────────────────────────────┐
    │  run_daily_local.py           │   │  diabetes-data-pull      ✓ daily │
    │    ↑ never invoked            │   │  diabetes-hub-monitor    ✓ daily │
    │  run_daily_pipeline.ps1       │   │  diabetes-research-iterate ✓ daily│
    │    ↑ never invoked            │   │  weekly-platform-audit   ✓ weekly│
    │  DiabetesHub_DailyPipeline    │   └──────────────────────────────────┘
    │    ✗ never registered         │              39 days × 4 tasks
    └───────────────────────────────┘         ≈ 150 correct failure reports
         0 runs in 39 days                         0 acted upon
```

`diabetes-data-pull` has fired every morning for 39 days. Its charter tells it to check whether
`literature_gap_data.json`'s `date_range` ends today, and to call it a FAILURE if not. It ends
`2026/07/17`. So that task has correctly returned **NO** roughly 39 times.

**[Likely]** — the hub does not have a detection problem, it has an escalation problem. Four
independent monitors agreeing daily, for over a month, with no state change, is not redundancy; it
is four copies of the same unread message. Adding a fifth monitor would not help. Two options worth
weighing:

- **Give one task write authority.** Change `diabetes-data-pull` from verifier to fixer: if the
  9-file freshness check fails, run `run_daily_local.py` rather than describing the failure. It
  already computes the exact trigger condition.
- **Or make silence expensive.** If nothing else, have the monitor stack escalate out of band after
  N consecutive failures instead of writing report N+1 into the same folder.

Not a recommendation between the two — that is your call on how much autonomy these tasks get. But
the status quo, four read-only tasks watching a dead pipeline, is the one option that is definitely
not working.

---

## File System Status

| File | Last modified | Age | State |
|---|---|---|---|
| `clinical_trials_latest.json` | 2026-07-17 | 39 d | **STALE** — md5-identical to 07-17 snapshot |
| `pubmed_recent_latest.json` | 2026-07-17 | 39 d | **STALE** — md5-identical to 07-17 snapshot |
| `hub_monitor_report.md` | 2026-07-17 | 39 d | **STALE** |
| `literature_gap_data.json` | 2026-07-18 | 38 d | **STALE** — `date_range` ends 2026/07/17 |
| `literature_gap_report.md` | 2026-08-24 03:36 | 1 d | **MISLEADING** — re-stamped again, see below |
| `agent_state.json` | 2026-08-24 03:36 | 1 d | live (derived layer) |
| newest `Analysis/Logs/*` | `gap_analysis_2026-07-17.log` | 39 d | no acquisition log since |

Freeze signatures, re-checked this morning against 08-24 — all four unchanged:

| Check | 08-24 | 08-25 |
|---|---|---|
| `find . -iname "daily_pipeline*"` | 0 | **0** |
| `Analysis/Results/logs/` exists | no | **no** |
| newest `Analysis/Logs/*` | `gap_analysis_2026-07-17.log` | **same** |
| newest trial / PubMed snapshot | `..._2026-07-17.json` | **same** |

```
md5  b7c4eff4329a85b75c34f2657246442b  clinical_trials_latest.json
md5  b7c4eff4329a85b75c34f2657246442b  clinical_trials_snapshot_2026-07-17.json
md5  432dedad31fd1ae26788e9025c0fcfc7  pubmed_recent_latest.json
md5  432dedad31fd1ae26788e9025c0fcfc7  pubmed_recent_snapshot_2026-07-17.json
```

### The freshness illusion recurred on schedule

08-24's report flagged that `literature_gap_report.md` was stamping render time instead of source
vintage. This morning it carries **"Generated: 2026-08-24 03:36"** — one day newer than yesterday —
over a `date_range` of `2020/01/01 to 2026/07/17` that has not moved.

That confirms it is not a one-off artifact: `diabetes-research-iterate` re-renders and re-stamps the
file every night at 03:05. The header advances daily; the data does not. Anyone auditing this hub by
file header — which is what headers are for — will read a 39-day-old analysis as one day old, and
will do so every single day until the generator is changed. Elevating this from P2 to **P1**: the
staleness is now self-concealing, and a defect that hides itself outranks a defect that merely
exists.

---

## Clinical Trial Changes

**New or changed trials since last snapshot: zero.** No snapshot has been taken to diff against. The
last real diff on record remains 07-16 → 07-17 (1 new, 1 removed, 0 status changes, 0 new results).

Composition, unchanged and 39 days old — 858 trials, 269 RECRUITING, 52 Phase 3 recruiting, 321 with
results posted. Newest `results_posted` date in the file is 2026-07-16.

### Correctness drift, recounted as of today

Trials in the frozen snapshot whose own recorded `completion_date` has passed while their recorded
`status` is still not COMPLETED:

```
119  total  (was 118 on 08-24)
 15  crossed the line during the freeze  (was 14)
  7  of those are Phase 2 or Phase 3     (was 6)
```

One new record went wrong overnight:

| NCT | Recorded completion | Status hub still reports | Phase | Sponsor |
|---|---|---|---|---|
| **NCT06716203** | **2026-08-25** | RECRUITING | 3 | BrightGene (BGM0504, T2D) |

Full Phase 2/3 drift set — this is the verification list for the first post-fix pull:

| NCT | Completion | Reported status | Phase | Sponsor |
|---|---|---|---|---|
| NCT07064486 | 2026-07-31 | RECRUITING | 3 | BrightGene (BGM0504) |
| NCT07321678 | 2026-08 | ACTIVE_NOT_RECRUITING | 2 | Ascletis Pharma |
| NCT07271251 | 2026-08-03 | ACTIVE_NOT_RECRUITING | 3 | Novo Nordisk (oral semaglutide) |
| NCT06926842 | 2026-08-13 | ACTIVE_NOT_RECRUITING | 2 | Zealand Pharma (petrelintide) |
| NCT06810726 | 2026-08-15 | RECRUITING | 2 | Estar Medical |
| NCT06797869 | 2026-08-21 | ACTIVE_NOT_RECRUITING | 2 | Novo Nordisk (CagriSema) |
| NCT06716203 | 2026-08-25 | RECRUITING | 3 | BrightGene (BGM0504) |

The drift accrues at roughly **one record every two days**, all in the same direction — toward
under-reporting completion. A frozen registry does not generate noise, it generates a monotone bias
that always overstates how much of the field is still open.

### Nine more cross in the next fourteen days

```
      today                                                        +14d
   08-25 │ 08-27  08-30 08-31   09-01                              │
         │   ▌      ▌     ▌       ▌▌            ▌   ▌   ▌   ▌      │
         ├───┴──────┴─────┴───────┴┴────────────┴───┴───┴───┴──────┤
           Sanofi Insulet  2nd   Ain Shams   Gasherbrum  UCSF  Aalborg
           Ph4    (dev)   Affil.  Ramathibodi  Ph2       SAVA
```

| Completion | NCT | Phase | Status | Sponsor |
|---|---|---|---|---|
| 2026-08-27 | NCT05757713 | 4 | ACTIVE_NOT_RECRUITING | Sanofi |
| 2026-08-30 | NCT07593625 | N/A | NOT_YET_RECRUITING | Insulet |
| 2026-08-31 | NCT07374328 | 1/2 | RECRUITING | 2nd Affiliated Hospital |
| 2026-09-01 | NCT06951074 | 2/3 | RECRUITING | Ain Shams University |
| 2026-09-01 | NCT07533604 | N/A | RECRUITING | Ramathibodi Hospital |
| 2026-09 | NCT07400588 | 2 | ACTIVE_NOT_RECRUITING | Gasherbrum Bio |
| 2026-09 | NCT07679347 | N/A | NOT_YET_RECRUITING | SAVA Technologies |
| 2026-09 | NCT07116902 | N/A | NOT_YET_RECRUITING | UCSF |
| 2026-09 | NCT06185296 | N/A | RECRUITING | Aalborg University Hospital |

If the pull does not run, all nine join the drift set and the Phase 2/3 error count reaches 9 by
mid-September.

Key-organization programs are unchanged from 08-24 (Vertex 3 trials, Lilly 33, Novo Nordisk 28,
**Sana Biotechnology 0**). The Sana zero and the zimislecel↔VX-880 vocabulary split both remain
open — see actions 8 and 9.

---

## PubMed Highlights

158 unique papers, 16 domains, 30-day lookback ending 2026-07-17. Thirteen of the sixteen domains
return exactly 10 papers and the rest return 8 or fewer, so per-domain volume is capped, not
measured. **No publication-volume trend can be read from this file**, and none should be quoted from
it.

Cross-domain papers: **12 of 158 (7.6%)** — unchanged, since the file is unchanged. The full list is
tabled in the 08-24 report and is not reproduced here.

**Still unreviewed after 39 days — PMID 42459945**, *"A framework for assessing algorithmic
discrimination risks in training data: a case of pediatric type 1 diabetes"* (JAMIA open, 2026-Aug).
The only triple-domain hit in the corpus (AI/ML × Closed Loop AP × Health Equity), landing exactly on
the Tier 1 #5 / #6 seam. It requires no pipeline, no script and no scheduler — only a reader. It has
now been recommended three mornings in a row.

Key-therapy tracking is still uninformative: `therapy_hits` reports `paper_count` of 5, 4, 5, 2, 4,
3, 5 and 0 across the eight tracked therapies, with zimislecel at 0 — which is a vocabulary artifact
(the literature indexes it as VX-880 in trial contexts), not an absence of literature. Confirmed the
08-24 read: the therapy-hit query cannot detect a publication surge as written.

---

## Gap Analysis Summary

Unchanged — `literature_gap_data.json` still carries `"generated": "2026-07-17T10:14:41"`. Top
gaps, BRONZE, 435 pairs across 30 domains:

| Rank | Pair | Gap | Joint | Expected |
|---|---|---:|---:|---:|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 | 7.5 |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 | 7.3 |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 | 4.7 |
| 4 | Glucokinase × Health Equity | 100.0 | 0 | 4.3 |
| 5 | Gene Therapy × LADA | 100.0 | 0 | 3.3 |

Two open methodological challenges from 08-24 stand, neither addressed:

1. **Ten pairs tie at exactly 100.0.** The formula saturates the instant `joint == 0`, so ranks 1–6
   are an arbitrary tie-break presented as an ordering. `expected` is already in the data and
   discriminates cleanly (25.4 down to 3.0) — it is simply not used for ranking.
2. **Five of the top 20 gaps involve Health Equity**, a 1,990-publication domain, 6th smallest of
   30. Small domains with distinct vocabulary mechanically produce zero-overlap pairs.
   **[Guessing]** — these may be terminology artifacts. Path to resolution is cheap and specific:
   re-query each intersection with *disparity / access / socioeconomic / underserved* substituted
   for the canonical Health Equity string. If counts jump, the gaps evaporate. That test needs no
   new data and could be run against the frozen file today.

### Tier 1 alignment

Unchanged from 08-24: Drug Repurposing × Health Equity is double-Tier-1 (#4 at 18/20, #6 at 17/20);
Beta Cell Regen, Treg/CAR-T and Glucokinase × Health Equity each route to Tier 1 #6. Because all
four equity gaps depend on the same query string, challenge 2 above governs all of them at once —
which is why it outranks any individual gap.

---

## Breaking News (web check, 08-18 → 08-25)

**Nothing new clears the significance bar this week.** Searches for Phase 3 diabetes results and FDA
diabetes approvals in the last seven days returned only material already logged on 08-24 or earlier:

- **Garzulys (insulin aspart-fsan)** — first rapid-acting insulin biosimilar to NovoLog, still
  absent from the hub because it post-dates the freeze. **Date discrepancy to resolve:** the 08-24
  report records the approval as 2026-07-30; this morning's search of FDA new-approvals material
  returns 2026-07-24. Both are secondary reads, neither is a direct fetch of the FDA approval
  record. Do not cite a date for this until one of us pulls the primary source.
- **Retatrutide Phase 3 program** — all four core trials complete; TRANSCEND-T2D-1 published
  (HbA1c −18.5 to −21.2 mmol/mol vs −8.9 placebo; weight −11.5% to −15.3% vs −2.6%). *Level 1b.*
- **CagriSema REIMAGINE 1/2** — already in the corpus from the 2026-06-10 pull. No action.
- **Zimislecel (VX-880)** — still not FDA-approved. Regulatory submissions guided for 2026,
  potential availability 2027. No change to Vertex records warranted.

No item found this week contradicts an existing hub claim.

---

## Recommended Actions

**P0 — do this one thing**

1. Run the pull directly. No scheduler, no PowerShell, no admin:
   ```
   python "C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts\run_daily_local.py"
   ```
   Success criterion: `literature_gap_data.json` shows `date_range` ending `2026/08/25`, and
   `Analysis/Results/clinical_trials_snapshot_2026-08-25.json` exists. Expect it to take a while —
   the gap step queries 435 pairs and is the long pole.

**P1 — after data flows**

2. Diff the fresh trial pull against `clinical_trials_snapshot_2026-07-17.json`. Expect ≥119 status
   corrections. The seven Phase 2/3 records tabled above are the verification set: if they do not
   flip to COMPLETED, acquisition ran but is not actually refreshing.
3. Stamp **source-data vintage**, not render time, in every report and dashboard generator. The
   `literature_gap_report.md` header has now advanced two days over static data; every dashboard
   regenerated since 07-17 has the same defect. This is self-concealing staleness and it is why it
   moved up from P2.
4. Print the executed step list at the top of every orchestrator log. Two "step was never in the
   pipeline" defects in four days (extraction on 08-22, acquisition today) share one root cause: the
   orchestrator's contents are not observable without reading source.
5. Decide the escalation question — either grant `diabetes-data-pull` authority to run
   `run_daily_local.py` when its own freshness check fails, or add out-of-band escalation after N
   consecutive failures. Four read-only monitors reporting the same failure for 39 days is the
   status quo to be replaced.

**P2 — separable, lower urgency than previously stated**

6. Register the scheduled task (`register_daily_task.ps1`, then `Start-ScheduledTask`). Worth doing,
   but it is a convenience fix, not the data fix — and note the registration uses
   `-LogonType Interactive`, so it will only fire while you are logged on; `-WakeToRun` will not
   cover a logged-off machine.
7. Resolve the two competing dead orchestrators (`run_daily_pipeline.ps1` vs. root `refresh.ps1`).
   Two inert schedulers is how this hid for 39 days.
8. Raise the therapy-hit result cap in `baseline_pubmed_alerts.py`.
9. Add a synonym map to `baseline_clinical_trials.py` (zimislecel ↔ VX-880 at minimum) and re-check
   the Sana Biotechnology query — zero matched trials for a tracked key organization is more likely
   a query defect than a real zero.
10. Re-rank `literature_gap_data.json` by absolute expected shortfall alongside gap score; stop
    presenting the ten 100.0-tied pairs as an ordered list.
11. Run the Health Equity terminology test described above. **Runs against frozen data — available
    today, no pipeline required.**

**P3 — requires nothing but twenty minutes**

12. Read **PMID 42459945**. Third consecutive recommendation.

---

## Evidence Levels (per Research Doctrine)

| Claim | Level | Basis |
|---|---|---|
| Pipeline has not run since 2026-07-17 | **[Certain]** | zero `daily_pipeline_*.log`; `Analysis/Results/logs/` absent; md5 identity of latest ↔ 07-17 snapshots |
| All four acquisition scripts present and intact | **[Certain]** | direct `stat` of each file in `Analysis/Scripts/` |
| `run_quality_improvements.py` contains no acquisition step | **[Certain]** | `grep -icE 'baseline_clinical\|baseline_pubmed\|gap_analysis_daily\|hub_monitor'` returns 0 |
| `diabetes-hub-daily-build` is Manual-only; other four diabetes tasks are read-only | **[Certain]** | scheduled-task listing + each task's own SKILL.md charter |
| 119 trials mis-stated, 15 during freeze, 7 Phase 2/3 | **[Certain]** | computed from the snapshot's own `completion_date` vs. `status` |
| Gap report re-stamps render time nightly over static data | **[Certain]** | header 2026-08-24 03:36 vs. `date_range` ending 2026/07/17; matches `diabetes-research-iterate` 03:05 schedule |
| Garzulys approved (date disputed: 07-24 vs 07-30) | **[Guessing]** on date, **Regulatory** on the approval itself | two secondary reads disagree; neither is a primary FDA record — resolve by fetching the FDA approval entry directly |
| Retatrutide Ph3 program complete | **Level 1b** | TRANSCEND-T2D-1, peer-reviewed |
| Monitor stack has an escalation problem, not a detection problem | **[Likely]** | 4 enabled monitors × 39 days, all correctly reporting failure, zero state change |
| Health Equity gaps are terminology artifacts | **[Guessing]** | plausible mechanism (small domain, distinct vocabulary), untested — resolve via synonym-expanded re-query |
| Gap classifications | **BRONZE** | single analytical source; expert confirmation pending |

---

*Generated by the Diabetes Research Hub monitor — review-only run, 2026-08-25. No files were modified.*
