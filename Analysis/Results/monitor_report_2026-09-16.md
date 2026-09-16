# Diabetes Research Hub — Monitor Report

**Run:** 2026-09-16 (automated, sandbox)
**Mode:** review only — no existing files modified
**Previous report:** `monitor_report_2026-09-15.md`

---

## Headline

**Nothing in the data pipeline moved in the last 24 hours, and the 09-15 falsifiable
prediction resolved on its failure branch.**

Yesterday's report predicted: *if the scripts are run, `clinical_trials_latest.json` reads
≥894 trials with a `generated` date after 2026-09-15; if not, all three files read 61+ days
and the headline repeats verbatim.*

They were not run. All three files read exactly **61 days**. The headline repeats.

This is now the **second consecutive day** the same three actions have been carried forward
unexecuted, and the **eighth day** the git commit has been blocked. The substantive findings
below are unchanged from 09-15 and are summarized rather than restated — read this report for
what is *new*, and `monitor_report_2026-09-15.md` for the full evidence.

---

## 1. File System Status

| File | Last modified | Age | Status |
|---|---|---|---|
| `clinical_trials_latest.json` | 2026-07-17 | **61 d** | STALE — write-path split (§1a) |
| `clinical_trials_summary.md` | 2026-07-17 | **61 d** | STALE — same cause |
| `hub_monitor_report.md` | 2026-07-17 | **61 d** | STALE — `hub_monitor.py` not run |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | **61 d** | STALE — master tracker |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 | 10 d | Newest real trial data |
| `pubmed_recent_latest.json` | 2026-09-06 | 10 d | Aging; re-run at 14 d (≈09-20) |
| `literature_gap_data.json` | 2026-09-08 | 8 d | OK — re-run at 14 d (≈09-22) |
| `literature_gap_report.md` | 2026-09-08 | 8 d | OK |
| `agent_state.json` | 2026-09-15 | 1 d | Fresh |

Staleness, to scale (each `█` = 5 days; dotted line = the 14-day re-run threshold):

```
                              ┊14d
clinical_trials_latest   ████████████▌           61
clinical_trials_summary  ████████████▌           61
hub_monitor_report       ████████████▌           61
Tracker.xlsx             ████████████▌           61
trials_snapshot_09-06    ██                      10
pubmed_recent_latest     ██                      10
literature_gap_data      █▌                       8
agent_state              ▏                        1
                         0    ┊    25   50    75 days
```

Four files sit at 61 days. Four sit under 11. There is no middle — which is the shape of a
**write-path split**, not of gradual neglect.

### 1a. Root cause (carried forward, unchanged)

The cowork sandbox monitor writes `clinical_trials_snapshot_<date>.json` but never updates
`clinical_trials_latest.json` or `clinical_trials_summary.md`. Only the local
`baseline_clinical_trials.py` writes those. Since the local script last ran 2026-07-17, every
consumer reading `_latest` has been served **two-month-old data with no error raised**.

Confirmed again this run: snapshots exist for 08-27, 08-28, 09-01, 09-06 — all newer than
`_latest`, none reflected in it. `_latest` holds 858 trials; the 09-06 snapshot holds 894.
**36 trials are invisible to every `_latest` consumer, including the dashboards.**

`[Certain]` — file mtimes and record counts read directly this run.

### 1b. Git commit still blocked — day 8

```
.git/index.lock   present, 0 bytes, created 2026-09-15 10:46
HEAD              227f606  "Daily iteration 2026-09-08"
Uncommitted       78 paths (8 new monitor reports incl. this one,
                            1 new audit script, ~60 modified builders/dashboards)
```

`ACTION_REQUIRED_2026-09-15.md` asked for one command. It has not been run. The published
site remains frozen at 2026-04-20 — **149 days**, on top of a 100+ commit backlog.

Eight days of citation repairs — including the eight false-PMID corrections documented on
09-15, four of which cited papers on entirely unrelated subjects — exist **only in the
working tree on your disk**. Nothing is lost, but nothing is durable either.

---

## 2. Clinical Trial Changes

**No new snapshot since 09-06.** The delta below is 09-01 → 09-06, already reported on 09-15
and repeated here only in compressed form. There is no 09-16 delta to compute.

- **New trials:** 8 · **Dropped:** 1 · **Status changes:** 3 · **New results posted:** 0
- Of the 8 new: `NCT07797335` (Novo, **Phase 3 RECRUITING**, AMBITION 7 / zenagamtide),
  `NCT07804849` (Ain Shams, **Phase 2/3 RECRUITING**, oral verapamil in newly-diagnosed
  children — beta-cell preservation, Tier 1 adjacent), `NCT05872620` (Lilly, Phase 3
  orforglipron, **COMPLETED with results posted 2026-09-04**).
- Status changes: `NCT07228117` Medtronic RECRUITING→ACTIVE_NOT_RECRUITING;
  `NCT07076199` Novo icodec RECRUITING→ACTIVE_NOT_RECRUITING; `NCT07282639` OHSU
  NOT_YET_RECRUITING→RECRUITING.

### Phase 3 recruiting, by category (09-06 snapshot, n=58)

```
T2D Novel Therapies      ██████████████████████████████████████████  42
T1D Immunotherapy/Prev   █████████████                               13
T1D Cure & Cell Therapy  ███                                          3
```

The cure track is **3 recruiting Phase 3 trials out of 58**. That ratio is the strategic
picture the hub exists to act on, and it has not changed.

### Cure-track and key-sponsor status (09-06)

| NCT | Program | Phase | Status |
|---|---|---|---|
| NCT04786262 | Vertex VX-880 + VX-018 (zimislecel) | PHASE3 | **RECRUITING** |
| NCT06832410 | Vertex VX-880 | PHASE3 | **RECRUITING** |
| NCT05791201 | Vertex VX-264 (device-encapsulated) | PHASE1/2 | ACTIVE_NOT_RECRUITING |
| NCT07222137 | Lilly baricitinib — delay Stage 3 T1D | PHASE3 | **RECRUITING** |
| NCT07222332 | Lilly baricitinib — preserve beta cell | PHASE3 | **RECRUITING** |
| NCT07088068 | Teplizumab efficacy/safety | PHASE3 | **RECRUITING** |
| NCT04598893 | Provention/Sanofi teplizumab extension | N/A | ACTIVE_NOT_RECRUITING |
| NCT07564414 | Novo CagriSema dose comparison | PHASE3 | **RECRUITING** |
| NCT07613307 | Lilly orforglipron in T2D | PHASE3 | **RECRUITING** |
| NCT07797335 | Novo zenagamtide (AMBITION 7) | PHASE3 | **RECRUITING** (new) |

**Sana Biotechnology: still 0 hits across all 894 trials.** Repeating yesterday's read —
this is a sponsor-string filter failure, not programme absence. Sana's hypoimmune islet work
runs under academic and partner sponsors (Uppsala, among others). Filter on
intervention/keyword, not sponsor.

`[Likely]` — zero hits across a 894-record registry snapshot for a program with published
6-month human data is far better explained by a query defect than by absence. To reach
`[Certain]`: run one ClinicalTrials.gov query on `UP421` / `hypoimmune islet` with no sponsor
filter.

### Pipeline defect: the therapy matcher misses its own flagship (carried forward)

`zimislecel` returns **0 trial hits and 0 PubMed hits**. ClinicalTrials.gov still registers
the program as **VX-880**, which returns 2 Phase 3 trials, both recruiting. The matcher has
no alias table.

This is a one-line fix and it matters more this week than last — see §5.

---

## 3. PubMed Highlights

Snapshot 2026-09-06, 30-day lookback, 139 unique papers from 1,025 query matches across 16
domains. **No newer pull exists.** 18 papers were new vs. the 09-05 snapshot.

### Cross-domain papers — 20 of 139 (14%)

Highest-value reads, ranked by domain span:

| Domains | PMID | Paper | Journal |
|---|---|---|---|
| **4** | 42694848 | COL1A2 and APOLD1: dual-axis framework for diabetic nephropathy–retinopathy comorbidity (multi-omics + ML) | Int J Med Sci |
| **3** | 42626948 | Gene-edited **hypoimmune islets** as a cure for T1D: immunological challenges | Expert Opin Biol Ther |
| **3** | 42673585 | GLP-1 RAs and co-agonists for weight loss without diabetes — updated systematic review | **Ann Intern Med** |
| **3** | 42694300 | Oral microbiome + metabolome in Alström / Bardet-Biedl | Comput Struct Biotechnol J |
| 2 | 42627334 | **β-cell function 1 year after stopping oral baricitinib** | **Diabetes Care** |
| 2 | 42688560 | Decoding Treg diversity and dysfunction for Treg-based therapies | Front Immunol |
| 2 | 42643804 | Teplizumab in stage 2 T1D — pediatric considerations | Ther Adv Endocrinol |

Two of these bear directly on trials listed in §2 and should be read before the tracker is
updated:

- **PMID 42627334** (*Diabetes Care*) is durability evidence for baricitinib withdrawal.
  Two Lilly Phase 3 baricitinib trials are actively recruiting. This is the single
  highest-leverage read in the pull.
- **PMID 42626948** is a direct review of the hypoimmune-islet approach — i.e. exactly the
  Sana program the trial filter cannot see (§2).

### Additional high-impact journals in window

`Diabetologia` ×3 (incl. **PMID 42608595**, multi-centre belatacept + sirolimus for islet
transplantation — relevant to gap #3; **PMID 42360463**, metabolomic profile distinguishing
LADA from T1D via tryptophan — relevant to the hub's LADA track) · *Nature* ×1 ·
*Science Transl Med* ×1 · *Lancet Diab Endo* ×2 (both orforglipron, Japanese cohorts) ·
*Nat Rev Nephrol* ×1.

### Key-therapy hits (30-day window)

```
dapagliflozin  ████████████████████████████████████████  41
retatrutide    ███████████                               11
icodec         ██████████                                10
orforglipron   ████████                                   8
teplizumab     █████                                      5
CagriSema      ████                                       4
baricitinib    ███                                        3
zimislecel     ·                                          0   ← alias defect
```

### Domain volume — two queries are broken

```
T2D GLP-1 New          188  ████████████████████
Diabetes AI/ML         182  ███████████████████
Diabetes Microbiome    139  ██████████████
Diabetes Biomarker     121  ████████████
Diabetes Health Equity  56  ██████
Diabetes Multi-Omics    55  ██████
T2D Remission           50  █████
Diabetes Gene Therapy   45  █████
Diabetes Complications  32  ███
Closed Loop AP          24  ██
T1D Immunotherapy       23  ██
T1D Stem Cell Cure      15  █▌
LADA New Research        8  ▉
GLP-1 Pharmacogenomics   3  ▎
Diabetes Epigenetics     1  ▏  ← implausible
Diabetes Drug Repurpose  1  ▏  ← implausible, and Tier 1 (18/20)
```

`[Certain]` that the counts are 1. `[Likely]` that the queries are malformed rather than the
fields being empty — diabetes epigenetics and drug repurposing each publish dozens of papers
a month. **Drug Repurposing is Tier 1 and is also gap intersection #3** (§4), so a broken
query there corrupts both the alerting and the gap analysis that feeds the contribution
strategy. This is not a cosmetic defect.

---

## 4. Gap Analysis Summary

From `literature_gap_report.md` (2026-09-08, 8 days old, 30 domains / 435 pairs).
**Validation level: BRONZE** — single analytical source, per Research Doctrine. These are
preliminary and must not be presented as established fact.

### Top 5 potentially meaningful gaps

| # | Intersection | Gap score | Joint pubs | Tier 1 alignment |
|---|---|---|---|---|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | **#6 Epidemiological / equity (17/20)** |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | — |
| 3 | **Islet Transplant × Drug Repurposing** | 100.0 | 0 | **#4 Drug repurposing (18/20)** |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | **#6 (17/20)** |
| 5 | Gene Therapy × LADA | 100.0 | 0 | — |

**Gap #3 remains the most defensible original-contribution opening.** An all-time unbounded
PubMed search (re-run 09-06) returns 7 records, **none** of which is a computational drug
screen for islet protection — the nearest work is bioengineering (immunoisolation,
bioartificial pancreas) or single-molecule in-silico structure work. It aligns with Tier 1
area #4 (18/20), the hub already holds `Drug_Repurposing_Islet.html` and
`Islet_Transplant_Analysis.html` as scaffolding, and PMID 42608595 (*Diabetologia*,
belatacept + sirolimus) landed in this very PubMed window as adjacent evidence.

**Caveat that has not been discharged:** gap #3's own feeding query (`Diabetes Drug
Repurpose`) returned 1 paper in 30 days (§3). Until that query is inspected, the gap score
for intersection #3 is measuring the query as much as the literature. **Fix the query before
opening work on gap #3**, or the contribution rests on an artifact.

Gaps #1, #3 and #4 all align with Tier 1 areas. Gaps #2 and #5 do not, and should be
deprioritized despite identical scores.

---

## 5. Breaking News (last 7 days)

**One item worth attention; nothing requiring same-day action.**

**Vertex / zimislecel (VX-880) — regulatory submission window is open now.**
Zimislecel holds FDA **RMAT** and **Fast Track** designations; Vertex has stated global
regulatory submissions to FDA, EMA and MHRA are **expected in 2026**, following completion of
Phase 3 enrollment and dosing. No submission announcement has been located as of 2026-09-16.
`[Likely]` — sourced from Vertex investor communications and secondary trade coverage, not
from an FDA docket. To reach `[Certain]`: check the FDA BLA/RMAT listings directly.

A 2026-09-08 industry release on islet-cell graft **survival** (as distinct from efficacy)
reinforces the same theme as PMID 42626948 — the field's bottleneck has moved from *making*
islet cells to *keeping them alive without lifelong immunosuppression*.

**Why this compounds the §2 defect:** the hub's therapy matcher scores zimislecel at zero in
both trial and literature alerting, at precisely the moment its regulatory event is most
likely. If the FDA submission lands this quarter, the current pipeline **will not flag it**.

Screened and excluded as not-new: oral semaglutide 25 mg approval (January 2026), first
generic dapagliflozin (April 2026), ADA 2026 orforglipron and retatrutide readouts (already
in the corpus).

---

## 6. Recommended Actions

Ranked by cost-to-fix against consequence-if-ignored. Items 1–3 are **carried forward
unexecuted from 09-15**.

**1. ⚠️ Unblock the commit. One command, eight days outstanding.**
```powershell
Remove-Item 'C:\Users\justi\OneDrive\Diabetes_Research\.git\index.lock' -Force
cd 'C:\Users\justi\OneDrive\Diabetes_Research'
.\PUSH_AND_VERIFY.ps1
```
78 uncommitted paths including eight verified false-citation repairs. Site frozen 149 days.

**2. ⚠️ Run the three dead scripts. Nothing else in this report matters until data moves.**
```
python baseline_clinical_trials.py      # last real run 2026-07-17 — 61 days
python hub_monitor.py                   # last run 2026-07-17 — 61 days
python baseline_pubmed_alerts.py        # last run 2026-09-06 — 10 days
```
`project1_literature_gap_analysis.py` does **not** need a re-run until ≈2026-09-22 (14 d).

**3. ⚠️ Fix the `_latest` write path in `baseline_clinical_trials.py` — or stop trusting it.**
Either point consumers at `max(glob('clinical_trials_snapshot_*.json'))`, or have the sandbox
monitor update `_latest` atomically when it writes a snapshot. Add a silent-staleness
assertion: refuse to serve `_latest` when a newer snapshot exists. That assertion would have
fired on 2026-08-27 and saved 20 days of wrong data.

**4. Add `VX-880` / `VX-264` as aliases for `zimislecel` in the therapy matcher.**
One line. Escalated from #3 yesterday to #4 today only because §5 makes the cost of *not*
doing it concrete: a plausible Q4 FDA submission that the pipeline cannot see.

**5. Inspect the `Diabetes Drug Repurpose` and `Diabetes Epigenetics` query strings.**
Counts of 1 over 30 days are implausible. Blocks action #9 below.

**6. Review PMID 42627334** — *β-Cell Function 1 Year After Stopping Oral Baricitinib*,
*Diabetes Care*. Directly informs NCT07222137 and NCT07222332, both recruiting.

**7. Review PMID 42694848** (four-domain: AI/ML × Biomarker × Complications × Multi-Omics) —
tightest match to Tier 1 area #1 (19/20) this cycle. And **PMID 42626948** (hypoimmune
islets) — bears on both the Sana filter gap and gap #3.

**8. Pull results for NCT05872620** (orforglipron, Lilly, Phase 3, results posted 2026-09-04)
into the tracker. Still the only new results record in the delta.

**9. Open work on gap #3 (Islet Transplant × Drug Repurposing) — *after* action 5.**
Most defensible original contribution surfaced so far. Do not start it on a query that
returns 1 paper per month.

**10. Re-query Sana Biotechnology by intervention keyword, not sponsor string.**
Try `UP421`, `hypoimmune`, `gene-edited islet` with no sponsor filter.

**11. Backfill or formally accept the 2026-07-17 → 2026-08-27 snapshot hole (41 days).**
Trials that opened and closed inside it are unrecoverable locally. A ClinicalTrials.gov
historical query by `LastUpdatePostDate` is the only route.

---

## 7. Falsifiable prediction for the next run

**Prediction A.** If action 2 is executed before the next pass, `clinical_trials_latest.json`
will read **≥ 894 trials** with a `generated` timestamp after 2026-09-16, and
`clinical_trials_summary.md` mtime will move off 2026-07-17. If not, all four 61-day files
read **62+ days** and this headline repeats a third time.

**Prediction B.** If action 1 is executed, `git log` will show a commit dated ≥2026-09-16 and
`git status --porcelain` will return **< 10** paths. If not, the count will read **79 or
more** at the next pass — it grows by roughly one monitor report per day (77 → 78 today).

**Prediction C.** If action 5 is executed and the query is in fact malformed, the repaired
`Diabetes Drug Repurpose` 30-day count will return **> 10**, not 1. If it returns 1 again
after repair, the gap-#3 score is real and the Tier 1 opening is confirmed rather than
undermined — either outcome is informative, which is why this is the cheapest high-value
action on the list.

---

*Generated by the automated hub monitor. Review-only run — no existing files were modified.
All evidence levels labeled per RESEARCH_DOCTRINE.md §Validation Tiers. Gap analysis findings
are BRONZE (single analytical source) and preliminary.*
