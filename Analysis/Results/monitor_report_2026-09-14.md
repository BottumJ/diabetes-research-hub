# Diabetes Research Hub — Monitor Report

**Run date:** 2026-09-14 (Monday, automated)
**Run window:** 07:36:59 → 07:41:32 UTC (02:36 US Central)
**Prior report:** monitor_report_2026-09-13.md
**Mode:** Review run. No existing hub file modified. One new file written (this report).
**Environment note:** Linux sandbox failed to mount — **7th consecutive day**, identical Plan9
`share "c" is not mounted` error. Two attempts, then stopped per the retry guidance. No Python
executed. Every registry and PubMed figure below is a live API read made through the browser
today. OS mtimes remain unreadable — file ages use each file's internal `generated` field.

---

## Headline

### 1. Yesterday's falsifiable prediction failed. The reason makes the whole question obsolete.

The 09-13 report predicted: *on Monday the 09-11 bucket will read below 1,165 and the 09-10
bucket below 1,104.* Both were re-read twice today, five minutes apart.

```
  AREA[LastUpdatePostDate]RANGE[D,D] — predicted vs observed, 2026-09-14
  ─────────────────────────────────────────────────────────────────────────
  bucket      09-13 rdg   predicted   observed 07:36   observed 07:41
  Thu 09-10     1,104      < 1,104        1,104            1,104
  Fri 09-11     1,165      < 1,165        1,165            1,165
  Sat 09-12         0          0              0                0
  Sun 09-13         0          0              0                0
  Mon 09-14         —          —              0                0
```

**Prediction falsified as stated.** I said I should be held to it, so: the batch-re-dating
mechanism (M-12) is not what today's data shows.

**What today's data shows instead is a single API field that answers the question outright.**
`GET /api/v2/version` returns:

```json
{ "apiVersion": "2.0.5", "dataTimestamp": "2026-09-11T09:00:04" }
```

The registry API serves a **static database snapshot**, and it publishes the snapshot's own
timestamp. At 07:41 UTC on Monday 09-14 the served snapshot was still **Friday 09-11 09:00:04**.

Everything the last three reports have been reasoning about falls out of that one field:

| Observation, 09-11 → 09-14 | Explanation |
|---|---|
| 09-12, 09-13, 09-14 buckets read 0 | Those days are not in the served snapshot |
| All five category counts byte-identical for 3 days | Same snapshot, same answers |
| All five day-buckets byte-identical for 3 days | Same snapshot, same answers |
| Decay seen 09-11 → 09-12 (826 → 799) | Snapshot advanced 09-10 → 09-11 |
| No decay 09-12 → 09-14 | Snapshot did not advance |
| "Weekend blackout" | Snapshot does not advance on non-business days |

**The corrected freshness rule is neither D−1 nor a business-day-with-holiday-table calendar.
It is: read `dataTimestamp` from `/api/v2/version` and use its date as the reference day.**
No holiday table. No timezone reasoning. No n=1 generalisation from Labor Day. One HTTP call.

Verification today: the newest populated bucket is exactly `date(dataTimestamp)` = 09-11.
Freshness gate under each candidate rule:

```
  D+0  (current code)     09-14 →     0 records   FAIL
  D−1  (09-12 proposal)   09-13 →     0 records   FAIL
  last business day       09-11 →    24 records   pass  (by luck — see below)
  date(dataTimestamp)     09-11 →    24 records   pass  (by construction)
```

"Last business day" and `dataTimestamp` agree today. They will diverge the moment the batch
is late, skipped, or run twice — which is exactly the failure a freshness gate exists to catch.
A gate that computes the expected date from a calendar cannot detect a stale upstream; a gate
that reads the upstream's own timestamp can. **[Certain — version endpoint read twice, 5 min
apart, plus 13 bucket reads.]**

**The standing rule is unchanged and now has a mechanism:** a historical `LastUpdatePostDate`
day-count is not reproducible, because it is a property of whichever snapshot answered you.
Never store one without storing the `dataTimestamp` beside it.

**New falsifiable prediction for the 09-15 run:** `dataTimestamp` will read `2026-09-14T09:00:0x`,
the 09-14 bucket will be populated (800–1,200), 09-12 and 09-13 will still read 0 and will never
fill, and the 09-11 bucket will read **below** 1,165. If `dataTimestamp` has not advanced by
tomorrow's run, the batch is not daily and the snapshot cadence needs re-measuring.

### 2. GLADIATOR is read. The hub has had the trial's size wrong by 2×, in the unsafe direction.

Yesterday's item 1 — read the ladarixin registry results — is done. Details in §2. The short
version:

- **`EnrollmentCount` = 289 is the run-in cohort, not the randomized population.**
  289 entered a 180-day run-in; **148 (51%) never randomized**; **141 were randomized**
  (95 ladarixin / 46 placebo); **140 analyzed**. Thirteen days of hub reports have described
  this as a 289-patient trial. It is a 141-patient trial. **[Certain — participant flow read]**
- The primary endpoint **missed, and the point estimate favours placebo**: adjusted mean
  difference in change from baseline in log(2-h C-peptide AUC+1) at Month 6 =
  **−0.133 (95% CI −0.334 to 0.068), p = 0.196**, ladarixin declining *more* than placebo.
- Safety was clean: **1 SAE per arm, 0 deaths**. Ladarixin failed on efficacy, not tolerability.

This is the first new *diabetes* knowledge the hub has acquired in a review run since 09-08, and
it cost one API call.

---

## 1. File System Status

| File | Internal `generated` | Age | Δ vs 09-13 |
|------|----------------------|-----|-----------|
| `literature_gap_data.json` / `_report.md` | 2026-09-08 03:17:27 | **6d** | +1d |
| `pubmed_recent_latest.json` | 2026-09-06 09:18:08 | **8d** | +1d |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 02:38:16 | **8d** | +1d |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 | 14d | +1d |
| `clinical_trials_latest.json` | **2026-07-17 02:05:53** | **59d** | still a broken pointer |
| `hub_monitor_report.md` / `hub_monitor_state.json` / `clinical_trials_summary.md` | 2026-07-17 | **59d** | still stale |
| `teplizumab_sNDA_decision_prep.md` | 2026-04-03 | **164d** | **newly flagged — see §5** |
| `Diabetes_Research_Tracker.xlsx` | — | — | **still lock-held** |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 | 183d | +1d |

`clinical_trials_latest.json` metadata read today: `total_trials: 858`, categories
152/76/147/236/321 — the 07-17 figures, not the 09-06 ones. D-01 confirmed for the 9th day.

**No file in `Analysis/Results/` carries a 2026-09-14 date before this run.** Newest prior
artifact is `monitor_report_2026-09-13.md`. **Eighth consecutive day with no script execution.**

- `.~lock.Diabetes_Research_Tracker.xlsx#` still present. Tracker backlog now **thirteen days**.
- **09-07 test residue: all four files still present, now 7 days old** — verified by directory
  listing today: `Analysis/Results/_wtest.txt`, `Analysis/Results/.gap_checkpoint.json.testbak`,
  `Analysis/Results/.gap_checkpoint.json.__unlinktest`, root `.wtest`.
- `open_findings.md` re-emitted below in condensed form. **Third of the three consecutive runs
  required to retire M-08 — M-08 is retired with this report.**
- Dashboard builders still unexecuted; `origin/main` frozen at 2026-04-20 — **147 days**.

---

## 2. Clinical Trial Changes

### ★ GLADIATOR (`NCT04628481`) — full results read

Phase 2, multicenter, randomized, double-blind, placebo-controlled. Sponsor **Dompé
Farmaceutici S.p.A**. Recent-onset T1D with low residual β-cell function.
Actual completion **2025-10-21**. Results first posted **2026-08-31**. Stopped for
**"futility as per protocol."**

**Population — this is the correction that matters**

```
  Participant flow, NCT04628481
  ──────────────────────────────────────────────────────────────────
  Entered 180-day run-in         289   ████████████████████████████
    did not complete run-in      148   ██████████████▌      (51.2%)
    randomized                   141   █████████████▌
      ladarixin 400 mg b.i.d.     95   █████████▌
      placebo                     46   ████▌
    analyzed (Full Analysis Set) 140   █████████████▌  (94 / 46)
    completed 12-mo treatment     91   ████████▌       (65 / 26, 64.5%)

  Registry EnrollmentCount field = 289  ← what the hub stored
  Randomized population          = 141  ← what "n" means in a trial
```

**Primary outcome** — change from baseline in 2-h C-peptide AUC (MMTT) at Month 6, adjusted
ANCOVA on log(AUC+1), multiple imputation with retrieved-dropout:

| Arm | n | Adjusted mean change | 95% CI |
|---|---:|---:|---|
| Ladarixin | 94 | **−0.284** | −0.453 to −0.114 |
| Placebo | 46 | **−0.151** | −0.373 to 0.071 |
| **Difference** | | **−0.133** | **−0.334 to 0.068**, p = **0.196** |

The point estimate is **negative**, i.e. the ladarixin arm lost *more* C-peptide than placebo.
On the log scale used by the model this corresponds to roughly a 12% lower geometric-mean
(AUC+1) change in the treated arm; the CI spans both directions and the result is not
significant. **The defensible statement is: ladarixin did not preserve β-cell function, and the
point estimate numerically favoured placebo. It is not "a trend toward benefit."**
[**Certain** for the numbers and the direction; **Likely** for the 12% back-transformation,
which assumes the standard reading of the stated log-scale model.]

**Secondary outcomes — uniformly null**

```
  Adjusted mean difference (ladarixin − placebo), 95% CI, p
  ─────────────────────────────────────────────────────────────────────
  C-peptide AUC   Mo 12    +0.021  [−0.398, 0.440]   p=0.921
                  Mo 18    −0.050  [−0.652, 0.552]   p=0.871
                  Mo 24    +0.182  [−8.570, 8.934]   p=0.967
  HbA1c           Mo  6    +0.468  [−0.985, 1.921]   p=0.528
                  Mo 12    +0.013  [−0.450, 0.476]   p=0.955
                  Mo 18    +0.149  [−0.926, 1.225]   p=0.785
                  Mo 24    −0.087  [−2.233, 2.059]   p=0.937
```

Note the Month-24 C-peptide interval (±8.9 on a scale where Month-12 effects are ±0.4). That
width is a sample-size artifact of a terminated trial, not a signal. Do not quote Month-24.

**Safety**

| | Ladarixin (94) | Placebo (46) | Run-in (289) |
|---|---:|---:|---:|
| Deaths | 0 | 0 | 0 |
| Serious AEs | 1 (spontaneous abortion) | 1 (gastroenteritis) | 0 |
| Other AEs ≥5% | 71 | 33 | 10 |

**Evidence grade: SILVER.** Randomized, double-blind, placebo-controlled, primary-source
sponsor-reported results — but not peer-reviewed, and terminated early for futility. Promote to
GOLD only on publication. **F-03 and F-14 both close.** `ladarixin` still returns **0** PubMed
records at 30 days, so the registry remains the only source.

**Why this matters beyond ladarixin.** The hub keys "do we know the answer?" on publication.
For this trial the registry held the full primary-outcome table, the flow diagram, and the
safety tables **14 days** before any paper existed — and would have continued to, indefinitely,
since nothing obliges a futility-terminated Phase 2 to be published at all.

### ★ New defect D-27 — `EnrollmentCount` is not the randomized population

The snapshot schema stores `EnrollmentCount` and nothing else about sample size. In any design
with a run-in, screening phase, or open-label lead-in, that field is the *entered* count.
GLADIATOR: 289 stored vs 141 randomized, a **2.05× overstatement**. Every hub artifact that
prints "n = 289" for this trial is wrong, and the error direction is always the same —
**trials look better powered than they are.** This is a schema defect, not a transcription
slip, and it is not specific to ladarixin.

### Freshness gate

| Query, run 2026-09-14 07:36 UTC | Count |
|---|---:|
| diabetes, `LastUpdatePostDate` = 2026-09-14 (D+0) | **0** |
| diabetes, `LastUpdatePostDate` = 2026-09-13 (D−1) | **0** |
| diabetes, `LastUpdatePostDate` = 2026-09-11 (`date(dataTimestamp)`) | **24** |

See Headline. The fix is `date(dataTimestamp)`.

### Category counts: byte-identical for the third consecutive day, and now that is expected

| Category | 09-06 snap | 09-11 | 09-12 | 09-13 | **09-14** | Δ 24h |
|----------|-----------:|------:|------:|------:|----------:|------:|
| T1D Cure & Cell Therapy | 156 | 157 | 158 | 158 | **158** | 0 |
| T1D Immunotherapy & Prevention | 77 | 77 | 77 | 77 | **77** | 0 |
| T2D Novel Therapies (Ph 2–3) | 152 | 150 | 151 | 151 | **151** | 0 |
| Diabetes Technology (Devices) | 245 | 246 | 244 | 244 | **244** | 0 |
| Diabetes Recently Completed w/ Results | 343 | 344 | 344 | 344 | **344** | 0 |

Five live `filter.advanced` queries replicating `baseline_clinical_trials.py` lines 34–51
verbatim (the script file was re-read today to confirm the strings). All five unchanged.

**Correction to 09-13.** Yesterday called this "the first day in the series where a flat count
genuinely means a quiet day." That was right for the wrong reason and is worth restating
precisely: a flat count means **the snapshot did not advance**. It carries no information about
whether the registry was quiet. Three days of flat counts here represent **one** observation of
the registry, not three. **[Certain]**

### Departures and new registrations: none — and this is uninformative today

- T2D Ph2–3 terminal-status, `LastUpdatePostDate`RANGE[2026-09-11, 2026-09-14] → **0 records**.
- `AREA[Condition](diabetes) AND AREA[StudyFirstPostDate]RANGE[2026-09-13,MAX]` → **0 records**.

Both windows extend past `dataTimestamp`, so a null result was guaranteed before the query ran.
**Any diff whose window ends after `date(dataTimestamp)` is structurally incapable of returning
a change.** The hub has been running such diffs daily since 09-12. **New defect D-28.**

### Watch list: all seven re-read in full, plus `NCT05232071`. Nothing changed.

| NCT | Study | Status | Last update | Results |
|---|---|---|---|---|
| `NCT06926842` | ZUPREME-2, petrelintide, Ph2, n=221, Zealand | COMPLETED | 09-09 | none |
| `NCT06534411` | CagriSema vs tirzepatide, Ph3, n=1,023, Novo | COMPLETED | 09-09 | none |
| `NCT06323161` | CagriSema vs placebo, Ph3, n=274, Novo | COMPLETED | 09-09 | none |
| `NCT06797869` | CagriSema, T2D + neuropathy, Ph2, n=142, Novo | COMPLETED | 09-10 | none |
| `NCT05872620` | ATTAIN-2, orforglipron, Ph3, n=1,613, Lilly | COMPLETED | 09-04 | **posted 09-04** |
| `NCT07797335` | AMBITION 7, zenagamtide, Ph3, n=1,778, Novo | RECRUITING | 09-01 | — |
| `NCT04628481` | GLADIATOR, ladarixin, Ph2, **n=141 randomized** | TERMINATED | 08-31 | **posted 08-31** |
| `NCT05232071` | Lanifibranor, n=39, Inventiva | COMPLETED | 09-09 | **posted 09-09** |

Caveat per D-28: "nothing changed" here means "nothing changed as of the 09-11 snapshot."

### Structural invisibility: unchanged, same snapshot

```
  diabetes, COMPLETED, completion date in 2026            246
    …with results posted (visible to collector #5)         12   ▏
    …invisible to all five collectors                     234   ████████████████████
```

`ResultsFirstPostDate` ≥ 2026-09-09 → **1** record (`NCT05232071`); ≥ 2026-09-12 → **0**.
**[Certain — 9 `countTotal` reads today.]**

---

## 3. PubMed Highlights

Corpus unchanged since 2026-09-06 09:18: **139 papers, 16 alert domains, 30-day lookback**. Now
**8 days stale**. (Task spec says 15 domains; the script defines 16. Seventh report to note this.)

### ★ Correction: yesterday's "PubMed has no D+0 lag" was wrong, and it was marked [Certain]

The 09-13 report recorded `2026-09-13 = 141` and concluded PubMed's same-day bucket is already
populated. Re-read today:

```
  diabetes, Entrez date — same buckets, read 24 h apart
  ──────────────────────────────────────────────────────────────
  bucket        09-13 rdg   09-14 rdg    Δ
  Wed 09-09         —          210
  Thu 09-10         —          195
  Fri 09-11        208         208       0    ← stable
  Sat 09-12          3           3       0    ← stable
  Sun 09-13        141         178     +37    ← +26%, still filling
  Mon 09-14          —           0       —    ← D+0 empty at 07:41 UTC
```

Two things follow. **PubMed day-buckets fill retrospectively and stabilise after ~24 h** — the
141 read yesterday was a partially-loaded bucket. And at the hour this monitor actually runs
(**07:41 UTC / 02:41 US Central**) the D+0 bucket is **empty**, so PubMed does have a D+0 lag
at monitor runtime. The correct PubMed reference day is **D−1**, which is stable.

So the two sources need two different rules — yesterday's instinct (#12) was right, its specific
rule was not:

| Source | Reference day | How it is obtained |
|---|---|---|
| ClinicalTrials.gov | `date(dataTimestamp)` | read from `/api/v2/version` |
| PubMed | D−1 | computed; stable by ~24 h, no weekend gap |

**New standing caution E-08:** a count taken from a still-filling bucket is not comparable to
the same count taken later. **No prior report has recorded the hour of its reads.** Every
inter-day delta in this hub's history compares readings taken at unknown, possibly different
hours. **New defect D-29.** This report records its window in the header; future ones must too.

### New in the 09-13 → 09-14 window

Six targeted searches. Tier 1 intersections returned **nothing**: islet/β-cell **0**, T1D
immunotherapy **0**, drug repurposing **0**, LADA/gene therapy **0**.

The tracked-therapy search returned **11** papers — but only because I ran it with `tirzepatide`
and the GLP-1 class included, per D-23. Under the hub's actual `KEY_THERAPY_TERMS` this window
would have yielded **2**.

```
  09-13 → 09-14 tracked-therapy yield
  ─────────────────────────────────────────────────────
  hub's current KEY_THERAPY_TERMS      2   ██
  + tirzepatide / semaglutide class   11   ███████████
```

That is D-23 measured rather than asserted: the missing terms are **82%** of the day's yield.

Worth queueing (all Level 1a–2b, all on tracked or should-be-tracked therapies):

| PMID | What | Why |
|---|---|---|
| 42730869 | GLP-1 RAs and musculoskeletal outcomes — SR + meta-analysis, *Drugs* | **Level 1a**, class-wide safety |
| 42729958 | Weight regain after GLP-1 discontinuation — SR + meta-analysis, *PeerJ* | **Level 1a**, durability |
| 42730051 | Tirzepatide vs semaglutide and asthma exacerbation — US multicentre retrospective cohort, T2D | Head-to-head comparative effectiveness |
| 42730922 | Social determinants of health and dementia risk in T2D — two national cohorts, *Aging* | Equity × complications; nearest thing to a Tier 1 hit |

Nothing at a Tier 1 intersection. Nothing that changes a therapy's tier.

### Tracked-therapy pulse, 30-day rolling

```
                  09-13   09-14
  semaglutide       —      192   ████████████████████  (untracked)
  tirzepatide      126     123   █████████████         (untracked)
  ─────────────────────────────
  retatrutide       14      14   █▌
  orforglipron       7       7   ▊
  amylin class       4       6   ▋
  teplizumab         5       5   ▌
  baricitinib×T1D    —       1   ▏
  ladarixin          0       0
  zimislecel         0       0
```

`reldate=30` is a rolling window. **Do not read these deltas as publication events.** The two
untracked molecules out-publish every tracked therapy combined by **~10×**. [Certain for the
counts]

### Amylin class: still zero alert coverage (D-13, unchanged, 4 days)

### Reading queue: fifteen deep, nothing left it

Days unread as of today: PMID 42694848 (**8d**), 42627334 (8d), 42626948 (8d), 42673585 (8d),
42586227 (4d), 42607698 (**3d**), 42720752 (2d), 42722448 (2d), 42712437 (2d), 42608559 (2d),
42729683 (1d), and four added today. The queue has grown every day since 09-06 and has never
shrunk.

**42720752 has become more important, not less** — see §5.

---

## 4. Gap Analysis Summary

Unchanged since 2026-09-08 03:17:27 (**6 days**). 30 domains, 435 pairs. Validation **BRONZE**.
`individual_counts["Islet Transplant"] = 253` re-confirmed by direct file read today.

| Intersection (rank suppressed — see below) | Gap | Joint, narrow | Joint, widened | Doctrine Tier 1 |
|--------------|----:|------:|------:|---|
| Beta Cell Regen × Health Equity | 100.0 | 0 | 1 | §6 Epidemiological (17/20) |
| Insulin Resistance × Islet Transplant | 100.0 | 1 | **24** | §2 Literature Synthesis (19/20) |
| **Islet Transplant × Drug Repurposing** | 100.0 | 0 | **0** | **§4 Drug Repurposing (18/20)** |
| Islet Transplant × Health Equity | 100.0 | 0 | 3 | §6 (17/20) |
| Gene Therapy × LADA | 100.0 | 0 | **0** | §2 (19/20) |

Nothing re-measured today — the underlying file has not changed and re-running yesterday's
esearch calls would produce yesterday's numbers at additional cost. Carried findings, all
established 09-13 and all still standing:

- **M-10 — the score saturates.** 21 of 435 pairs tie at exactly 100.0. Ranks are
  insertion-order artifacts of a stable sort with no tie-break (`gap_analysis_daily.py` line 294).
  **Ranks are suppressed in the table above and should be suppressed everywhere.**
- **M-09 — domain strings undersize their fields.** Islet Transplant captures 253 of 1,131
  MeSH-indexed records (**22%**); Health Equity 2,067 of 6,189 (**33%**). Four of the top six
  gaps rest on the Islet Transplant denominator.
- **M-11 — the score measures co-mention, not co-investigation.** Widening Gap #2 from 1 to 24
  pulled in general reviews, not intersection studies. Construct validity, not calibration.
- **Two gaps survive both operationalisations at 0: Islet Transplant × Drug Repurposing and
  Gene Therapy × LADA.** Weak evidence, but the only evidence that distinguishes any gap from
  any other, and it favours the hub's lead contribution candidate (§4 Tier 1, 18/20).

**Carried, untouched:**

- **M-03 circularity test still unrun — thirteen days.** `Analysis/Scripts/falsify_equity_gaps.py`
  exists and has never been executed.
- **F-12** (Islet Transplant × GWAS classification vs PMID 42722448) unresolved; the pair is
  `ranked_gaps[3]` in the JSON and absent from the report, dropped by a downstream filter.

---

## 5. Breaking News

**Nothing in the 7-day window (09-07 → 09-14) changes hub priorities.** Two searches, three
primary fetches. [Likely — negative result]

### ★ A 91-day-old open action, found by checking a search result against the hub

The news search surfaced the Tzield pediatric approval. Fetched to verify the dateline per E-07:

> **FDA, dated 2026-06-12** — Tzield (teplizumab) approved to delay loss of endogenous insulin
> production in **pediatric patients aged 8–17 recently diagnosed with Stage 3 T1D**. Granted
> under **accelerated approval**. Basis: **PROTECT** (`NCT03875729`), randomized, double-blind,
> placebo-controlled, **n = 328**, diagnosed within 6 weeks, two 12-day IV courses six months
> apart, primary endpoint **C-peptide at 78 weeks** — a **surrogate**. Boxed warning for EBV/CMV
> reactivation. A **required post-approval confirmatory study is ongoing**.

The approval itself is correctly logged — `monitor_report_2026-06-16.md` caught it same-week and
graded it GOLD. Three things are not:

1. **`teplizumab_sNDA_decision_prep.md` was never closed.** It is dated 2026-04-03 and still
   reads *"PDUFA April 29, 2026 — Days until decision: 26"*, with unfilled `[DATE]` and
   `[NEW POPULATION]` placeholders. `monitor_report_2026-06-15.md` explicitly said the doc
   "should be marked closed/updated." That was **91 days ago**. A live hub artifact currently
   states a future decision date that passed four and a half months ago.
2. **The hub's own date record disagrees with itself.** `monitor_report_2026-06-15.md` records
   the approval as **June 13** (sourced to STAT); `monitor_report_2026-06-16.md` records
   **2026-06-12** (sourced to FDA). The FDA primary source, fetched today, says **June 12**.
   The 06-15 entry is wrong and was never corrected.
3. **`NCT03875729` (PROTECT) is not on the watch list**, nor is the required confirmatory study.
   This is the trial that supports an accelerated approval — the one registration in the hub's
   scope where a negative confirmatory readout could *withdraw* an indication.

**New standing caution E-09 — accelerated approval is not demonstrated clinical benefit.**
Tzield's pediatric Stage 3 indication rests on a C-peptide surrogate with a confirmatory study
pending. Log it as *accelerated approval on a surrogate endpoint, clinical benefit not yet
verified*, exactly as E-06 requires for SURPASS-CVOT. Two tracked therapies now carry claims
that secondary coverage routinely overstates.

**This also re-prices the reading queue.** PMID 42720752 is the PROTECT per-protocol analysis.
It is the per-protocol read of the pivotal trial behind an accelerated approval with an open
confirmatory obligation. It has sat unread for two days and was ranked 13th yesterday.

### ★ Two more E-07 traps, both caught by fetching

| Search result | Actual dateline | Verdict |
|---|---|---|
| "FDA Approves First Generic of Once-Daily GLP-1 Injection…" | **2024-12-23** (generic liraglutide, Hikma) | Not news. Second confirmed E-07 instance |
| "FDA Approves First Generic Dapagliflozin Tablets" | **2026-04-07** | Real, but 5 months old — outside the window |

I initially flagged the dapagliflozin generic as a hub miss. **It is not.** A grep of
`agent_state.json` found it already recorded: *"FDA approved; first generic approved 2026-04-07."*
The hypothesis was wrong and is withdrawn.

### Otherwise unchanged

- **Vertex zimislecel** — no filing announcement. Guidance remains "global regulatory submissions
  expected in 2026." Zero PubMed records in 30 days. FORWARD Phase 1/2 (NEJM, PMID 40544428,
  **12 patients, SILVER**) remains the entire evidence base. Watch stands. [Likely]
- **Novo / CagriSema** — NDA submitted 2025-12-18 (REDEFINE-1/-2), **no public PDUFA date**.
  Four CagriSema-family registry records completed 09-09/09-10. Not in the tracker.
  [Likely — secondary; no primary Novo IR fetch this run]
- **Zealand / petrelintide ZUPREME-2** — topline still guided H2 2026, not released. [Likely]
- **Mounjaro CV indication** — approved 2026-08-28. **E-06 binds: SURPASS-CVOT was
  non-inferiority vs dulaglutide, HR 0.92 (95.3% CI 0.83–1.01), superiority not established.
  Never quote "8% MACE reduction" as a benefit.**
- **Orforglipron / Foundayo** — approved 2026-04-01, chronic weight management only, not T2D.
- **Insulin efsitora alfa** — FDA decision possible H2 2026; still not on the watch list.
- **Retatrutide** — TRANSCEND-T2D-1 Phase 3 reported June 2026; still not logged.

---

## 6. Data Quality Defects — Current List

| # | Defect | Status | Age |
|---|--------|--------|----:|
| 6 | Freshness gate queries D+0 | **RESOLVED in principle today: use `date(dataTimestamp)` from `/api/v2/version`. Awaiting a one-line code change** | 6d |
| 7 | Scheduled run precedes the daily registry batch | **Explained today:** run at 07:41 UTC, snapshot at 09:00. Made harmless by the D-06 fix | 6d |
| 8 | `LastUpdatePostDate` history not reproducible | **Mechanism now [Certain]: the answer is a property of the served snapshot.** Store `dataTimestamp` with every count | 5d |
| 27 | **`EnrollmentCount` ≠ randomized population** — GLADIATOR 289 stored vs 141 randomized (2.05×); bias always inflates apparent power | **New today** | — |
| 28 | **Diffs with windows extending past `date(dataTimestamp)` cannot return a change** — run daily since 09-12 | **New today** | — |
| 29 | **No report records the hour of its reads**, so every historical inter-day delta is uncontrolled | **New today** | — |
| 17 | Watches keyed on `ResultsFirstPostDate` cannot fire on completion | Open. GLADIATOR cost 14 days | 2d |
| 23 | `tirzepatide` / `semaglutide` absent from `KEY_THERAPY_TERMS` | **Quantified today: 82% of the day's tracked-therapy yield** | 1d |
| 24 | Gap domain strings undersize their fields (M-09) | Open | 1d |
| 25 | Gap Score saturates — 21 of 435 at 100.0 (M-10) | Open | 1d |
| 26 | Gap Score measures co-mention, not co-investigation (M-11) | Open | 1d |
| 11 | Terminal statuses absent from collectors — hole is 234, not 34 | Open | 13d |
| 1 | `clinical_trials_latest.json` a 59-day-old duplicate | Open | 59d |
| 12 | retmax ceiling discards 85.9% of matching records | Open | 13d |
| 13 | Amylin class uncovered in `therapy_hits` and all 16 alerts | Open | 4d |
| 16 | Dashboard builders repaired, never executed; `origin/main` frozen 147d | Open | 5d |
| 2 | `has_results` constant `False` in the snapshot schema | Open | 8d |
| 4 | Epigenetics + Drug Repurpose alert queries over-filtered | Open | 6d |
| 10 | 41-day trial-snapshot hole (07-18 → 08-26) | Open, unbackfillable | 5d |
| 15 | No `estimand` field in the trial schema | Open | 3d |
| 3 | Null `title` on PMID 42698931 | Open, 1 of 139 | 8d |
| 5 | `phase` uses two null encodings | Open | — |
| 9 | Gap counts cited without the query string | 434 pairs remain | 5d |
| 14 | Findings not carried forward | **M-08 retired this run** | 4d |
| 19 | **Sandbox mount failed 7 consecutive days** | Blocks every script item below | 7d |
| 20 | Tracker lock-held; backlog 13 days | Open | 13d |
| 21 | 09-07 test residue, 4 files | Open | 7d |
| 22 | `CONTRIBUTION_STRATEGY.md` 183 days old | Open | 183d |
| 30 | **`teplizumab_sNDA_decision_prep.md` unresolved 91 days after the decision**; states a passed future PDUFA date | **New today** | 91d |

---

## 7. Recommended Actions

Ranked. ▲ = new or re-ranked today. **Items 1–5 need no Python and no sandbox.**

1. ▲ **Correct GLADIATOR's n everywhere it appears, and log the result.** n = **141
   randomized** (95/46), 140 analyzed, not 289. Primary endpoint missed: adjusted mean
   difference **−0.133 (95% CI −0.334 to 0.068), p = 0.196**, direction favouring placebo.
   Grade **SILVER**. Closes F-03 and F-14. This is a correction to a number already published
   in thirteen hub reports — it should go first.

2. ▲ **Implement the freshness gate as `date(dataTimestamp)` from `/api/v2/version`.** Not D+0,
   not D−1, not a business-day calendar with a holiday table. One HTTP call, one date parse.
   It also detects a stale upstream, which no calendar-based rule can. Closes D-06 and D-07.

3. ▲ **Store `dataTimestamp` beside every registry count the hub writes**, and refuse to diff
   two counts whose `dataTimestamp` values match — that diff is guaranteed zero (D-28). Record
   the UTC hour of every read (D-29).

4. ▲ **Close `teplizumab_sNDA_decision_prep.md`.** 91 days overdue, states a PDUFA date that
   passed on 2026-04-29, contains unfilled placeholders. Record: FDA accelerated approval
   **2026-06-12** (not June 13 — correct `monitor_report_2026-06-15.md`), ages 8–17, Stage 3,
   PROTECT `NCT03875729` n=328, C-peptide surrogate at 78 weeks, confirmatory study ongoing.
   Add **E-09** to the doctrine.

5. ▲ **Add `NCT03875729` (PROTECT) and its required confirmatory study to the watch list.**
   The only accelerated approval in the hub's scope; the only place a negative readout could
   remove an indication.

6. ▲ **Fix `EnrollmentCount` (D-27).** Store randomized-population count from the participant
   flow where results exist, and flag run-in / lead-in designs. Backfill GLADIATOR. The bias
   is one-directional and always makes trials look better powered.

7. **Re-key the watch list on `OverallStatus` and add a third key on `HasResults`** (D-17).
   Three events matter — completion, results posting, publication — and the hub watches only
   the last. GLADIATOR cost 14 days; ZUPREME-2 cost a completion.

8. **Add the terminal statuses to collector #5 and drop the results requirement.** Two edits in
   `baseline_clinical_trials.py`. Recovers 34 via the status clause and ~200 more by
   re-anchoring on `LastUpdatePostDate`. Without it, re-running the scripts re-buries
   `NCT06534411`, a 1,023-patient Phase 3 head-to-head.

9. ▲ **Add `tirzepatide`, `semaglutide` and `dulaglutide` to `KEY_THERAPY_TERMS`** (D-23) and the
   amylin class (`petrelintide`, `cagrilintide`, `amycretin`, `CagriSema`) with its own alert
   query (D-13). Measured cost of the omission today: 82% of the window's yield.

10. **Stop printing gap ranks as a ranking** (M-10). 21 pairs tie at 100.0; the order is
    insertion order. Key each intersection on the domain pair and state the tie explicitly.

11. **Re-derive every gap score with MeSH-anchored domain strings and report both string sets**
    (M-09). Treat any gap that does not survive both as unsupported. Two survive.

12. **Record M-11 in the doctrine as a known limitation of the gap method.** Any gap claim
    reaching a preregistration needs a hand-screened denominator, not a keyword-AND count.

13. **Log the week's registry events in the tracker.** Clear
    `.~lock.Diabetes_Research_Tracker.xlsx#` first. Oldest first: Mounjaro CV label (08-28,
    **log as non-inferiority per E-06, not an 8% benefit**), **GLADIATOR results with the
    corrected n (08-31)**, ATTAIN-2 + estimand (09-04), ZUPREME-2 completion (09-09),
    CagriSema cluster `NCT06534411`/`NCT06323161`/`NCT06797869` (09-09/10), zenagamtide
    `NCT07797335` (09-01), lanifibranor `NCT05232071` results (09-09).

14. **Run `falsify_equity_gaps.py`.** Thirteen days P1; the script already exists.

15. **Use D−1 for PubMed freshness**, separately from the registry rule (E-08). Do not apply
    one gate to both sources.

16. **Read PMID 42720752 (PROTECT per-protocol)** — now the highest-value unread paper, see §5 —
    then 42730869 and 42729958 (both Level 1a meta-analyses on the untracked GLP-1 class).

17. **Run the two dead scripts — after #8.**
    ```
    python Analysis/Scripts/baseline_clinical_trials.py
    python Analysis/Scripts/hub_monitor.py
    ```
    59 days stale; repairs `clinical_trials_latest.json`; restores NCT-ID diffing.

18. **Add an `estimand` field to the trial schema** (D-15); backfill ATTAIN-2.

19. **Raise `retmax` and page the alert queries** before re-running `baseline_pubmed_alerts.py`.

20. **Execute the repaired dashboard builders and push.** 147 days frozen.
    `verify_2026_09_12_repairs.py` first, then `run_quality_improvements.py`.

21. **Pin the query string next to every gap count** (D-09). 434 pairs remain.

22. **Fix the two over-filtered alert queries** and **`has_results`** (D-04, D-02).
    **Retire the "34 invisible records" figure** in favour of 234/22.
    **Replace consecutive-day diffing with a persistent seen-set** keyed on `overall_status`,
    `results_posted`, `last_update_posted`.

23. **Delete the 09-07 test residue** (4 files, 7 days). **Refresh `CONTRIBUTION_STRATEGY.md`**
    (183 days). **Add insulin efsitora alfa to the watch list.** **Track `NCT06239636` by NCT
    ID.** **Look at `NCT07808385`** (Mayo, closed-loop in pregnancy with T1D).

24. **Fix the sandbox mount.** Seven consecutive failed runs. Browser-driven API reads sustain
    review but cannot write snapshots, so the collection hole widens daily.

> **Note on the scheduled-task file.** `run_report_2026-09-12.md` asks, for the fifth day, that
> step 4 be repointed from the expired "PMIDs above 42000000" rule to
> `python Analysis/Scripts/audit_impossible_pmids.py`. Still outstanding. That file is outside
> the hub and only the user can edit it.

---

## 8. Self-Audit

- **My prediction failed and I am recording it as a failure, not a near-miss.** I said the
  09-11 bucket would read below 1,165 on Monday. It read 1,165, twice. The batch-re-dating
  model (M-12) was a reasonable inference from the data available on 09-13 and it was wrong.

- **But the more useful lesson is that I spent three reports inferring something the API
  publishes.** `dataTimestamp` was in `/api/v2/version` the entire time. Reports 09-11, 09-12
  and 09-13 built successively more elaborate theories — a lag, then a lag with decay, then a
  business-day batch calendar with a federal-holiday exception generalised from n=1 — to explain
  a number the server states outright. **Three days of inference replaced by one field.** The
  general lesson for this hub: before modelling an upstream's behaviour, read its metadata
  endpoints. I did not check whether the API had a version or status endpoint until today.

- **That is two consecutive days of overturning the prior day's top-three recommendation.**
  09-12 proposed D−1; 09-13 falsified it and proposed a business-day calendar; 09-14 shows both
  were unnecessary. The pattern is not bad luck — it is what happens when a daily process
  generates fixes from single-day observations and ranks them "cheapest first." **Cheap and
  wrong is not cheap.** I would rather this report be judged on whether #2 is still correct on
  09-21 than on how many items it contains.

- **I made a claim today and withdrew it before publishing.** I flagged the 2026-04-07 generic
  dapagliflozin approval as a hub miss caused by the 7-day news window, wrote it up as a
  structural finding, then grepped the hub and found it already recorded in `agent_state.json`.
  The finding was deleted. I am noting it because the near-miss is the interesting part: the
  reasoning was plausible, the conclusion was false, and only checking the hub's own files
  caught it.

- **The GLADIATOR n error is the most consequential thing in this report and it was trivially
  discoverable.** The participant-flow module was in the same JSON response as the results the
  hub has been waiting on. Thirteen reports printed "n=289." The number was never wrong in the
  registry — the hub read the wrong field, and no one checked the field's meaning.

- **I did not verify that `dataTimestamp` advances daily.** I have two reads, five minutes apart,
  both showing 09-11T09:00:04. The claim that it advances on business days at ~09:00 is
  **[Likely]**, inferred from the bucket pattern, not observed. Tomorrow's run tests it directly,
  and I have written the prediction down.

- **I did not re-measure anything in §4.** The gap file has not changed since 09-08 and
  re-running yesterday's 30-odd esearch calls would have reproduced yesterday's numbers. I
  re-read `literature_gap_data.json` to confirm `individual_counts["Islet Transplant"] = 253`
  and stopped there. Everything else in §4 is explicitly carried, not re-verified.

- **What else I did not do:** no primary fetch for Novo, Zealand or Vertex — those remain
  [Likely] on secondary sources, now for the second consecutive day. I did not recount
  cross-domain papers in the corpus (byte-identical, inherited: 20 of 139). I did not re-read
  `RESEARCH_DOCTRINE.md` this run — second consecutive omission, and §4's Tier 1 mappings are
  inherited from it.

- **One thing worth saying plainly:** this report contains 24 action items and the hub has
  executed approximately none of them in eight days, because the sandbox has been down for seven
  and the tracker locked for thirteen. Items 1–5 need neither. If exactly one thing happens
  before the next run, it should be **item 1** — correcting a published number that is wrong by
  2×, in a hub bound for preregistration.

---

## 9. Open Findings — condensed re-emission (3rd of 3 — **M-08 retired**)

Full ledger: `Analysis/Results/open_findings.md`. Changes today only.

**Closed today**

| ID | Finding | Resolution |
|----|---------|-----------|
| F-03 / F-14 | Ladarixin GLADIATOR result unknown to the hub | **Read in full.** Primary endpoint missed, difference −0.133 (95% CI −0.334 to 0.068), p=0.196, direction favours placebo. n=141 randomized, not 289. SILVER |
| D-06 / D-07 | Freshness gate wrong; scheduled run precedes the batch | **Both explained and fixed in principle:** `date(dataTimestamp)`. Awaiting implementation |
| M-08 | Findings not carried forward between runs | **Retired** — three consecutive re-emissions complete |
| M-12 | Registry decay = business-day batch re-dating | **Falsified.** Superseded by the snapshot-timestamp explanation |

**New today**

| ID | Finding |
|----|---------|
| M-13 | **The registry API serves a static snapshot and publishes its timestamp.** Every count is a property of that snapshot. Mechanism now [Certain]; supersedes M-06 and M-12 |
| D-27 | **`EnrollmentCount` is the entered, not randomized, population.** GLADIATOR 289 vs 141 (2.05×). One-directional bias toward apparent over-powering |
| D-28 | **Any diff whose window extends past `date(dataTimestamp)` returns zero by construction.** Run daily since 09-12 |
| D-29 | **No report records the hour of its reads.** All historical inter-day deltas are uncontrolled |
| D-30 | **`teplizumab_sNDA_decision_prep.md` unresolved 91 days after the decision**, stating a passed future PDUFA date with unfilled placeholders |
| E-08 | **PubMed day-buckets fill retrospectively** (09-13: 141 → 178 in 24 h) and are empty at D+0 at monitor runtime. **Use D−1.** Corrects a [Certain]-labelled claim in the 09-13 report |
| E-09 | **Tzield pediatric Stage 3 is an accelerated approval on a C-peptide surrogate** with a confirmatory study pending. Not demonstrated clinical benefit. Companion to E-06 |
| F-15 | **The hub's internal date for the Tzield approval is inconsistent** — 06-15 report says June 13 (STAT), 06-16 says June 12 (FDA). FDA primary, fetched today: **June 12** |
| F-16 | **`NCT03875729` (PROTECT) and its required confirmatory study are not on the watch list** |

**Unchanged and ageing:** F-01, F-02, F-05 … F-13; M-03 (**13 days**), M-05, M-07, M-09, M-10,
M-11; E-02 … E-07; D-01 (59d), D-02, D-04, D-05, D-10, D-11, D-12, D-13, D-15, D-16, D-17,
D-19 (**7 days**), D-20 (13d), D-21 (7d), D-22 (183d), D-23, D-24, D-25, D-26.

---

## Evidence & Provenance

| Claim | Basis | Level |
|-------|-------|-------|
| `dataTimestamp` = 2026-09-11T09:00:04 at 07:36 and 07:41 UTC | `/api/v2/version`, 2 reads | **Certain** |
| Buckets 09-10=1,104 / 09-11=1,165 / 09-12=0 / 09-13=0 / 09-14=0, stable across the run | 13 `countTotal` reads, `AREA[LastUpdatePostDate]RANGE[D,D]` | **Certain** |
| Prediction (09-11 < 1,165, 09-10 < 1,104) falsified | Same reads vs `monitor_report_2026-09-13.md` Headline | **Certain** |
| Newest populated bucket = `date(dataTimestamp)` | Bucket reads + version read | **Certain** |
| The API serves a static snapshot; all frozen counts follow from it | Inference from the above, no counter-example in 13 reads | **Certain** for the timestamp; **Likely** that the snapshot is the sole cause of every frozen count |
| `dataTimestamp` advances on business days at ~09:00 | **Not observed** — inferred from the bucket pattern | **Likely** |
| Diabetes slice: 09-14=0, 09-13=0, 09-11=24 | 3 `countTotal` reads | **Certain** |
| Category counts 158 / 77 / 151 / 244 / 344 | 5 `filter.advanced` queries replicating `baseline_clinical_trials.py` lines 34–51, script re-read today | **Certain** |
| 0 departures, 0 new registrations | 2 `filter.advanced` queries — **windows extend past `dataTimestamp`; result is structurally forced** | **Certain** the query returned 0; **uninformative** as a finding |
| Watch list: 8 records, status / last-update / results dates | Full record reads, 8 studies | **Certain** as of the 09-11 snapshot |
| GLADIATOR flow: 289 run-in, 148 not completed, 141 randomized (95/46), 140 analyzed, 91 completed | `resultsSection.participantFlowModule` + `baselineCharacteristicsModule.denoms` | **Certain** |
| GLADIATOR primary: −0.284 vs −0.151; difference −0.133 (95% CI −0.334, 0.068), p=0.19582, adjusted ANCOVA | `outcomeMeasuresModule.outcomeMeasures[0]` | **Certain** |
| ≈12% relative back-transformation of −0.133 | Standard reading of the stated log(AUC+1) model | **Likely** |
| GLADIATOR secondaries all null (p 0.528–0.967) | `outcomeMeasures[1..2]` | **Certain** |
| GLADIATOR safety: 0 deaths, 1 SAE per arm | `adverseEventsModule.eventGroups` | **Certain** |
| `whyStopped` = "stopped due to futility as per protocol" | `statusModule.whyStopped` | **Certain** |
| 246 / 12 / 234 structural invisibility | 2 `countTotal` reads | **Certain** |
| PubMed 09-13 grew 141 → 178 in 24 h; 09-11 and 09-12 stable; 09-14 = 0 at 07:41 UTC | 5 `esearch` calls today vs `monitor_report_2026-09-13.md` §3 | **Certain** |
| PubMed buckets stabilise after ~24 h | 2 stable buckets (09-11, 09-12), 1 growing (09-13) | **Likely**, n=3 |
| Therapy 30-day counts incl. semaglutide 192, tirzepatide 123 | 9 `esearch` calls, `reldate=30` | **Certain** |
| Tracked-therapy window yield 2 vs 11 | 1 windowed `esearch` + term-set comparison against `KEY_THERAPY_TERMS` | **Certain** |
| Tier 1 intersections returned 0 in the 09-13→09-14 window | 4 windowed `esearch` calls | **Certain** |
| PMIDs 42730869, 42729958, 42730051, 42730922 — titles, journals | `esearch` + `esummary` | **Certain** |
| Tzield pediatric Stage 3: approved 2026-06-12, accelerated, ages 8–17, PROTECT NCT03875729 n=328, C-peptide at 78 wk, confirmatory study ongoing | **FDA page fetched in full today**, dateline 06/12/2026 | **Certain** — primary |
| Hub records June 13 (06-15) and June 12 (06-16) | Both files grepped today | **Certain** |
| `teplizumab_sNDA_decision_prep.md` still states "PDUFA April 29, 2026 / Days until decision: 26" with unfilled placeholders | File read today, lines 1–40 | **Certain** |
| Generic liraglutide dated 2024-12-23; generic dapagliflozin dated 2026-04-07 | **Both FDA pages fetched in full today** | **Certain** — primary |
| Generic dapagliflozin already recorded in the hub | Grep of `agent_state.json` — "first generic approved 2026-04-07" | **Certain** |
| `individual_counts["Islet Transplant"] = 253` | `literature_gap_data.json` read today | **Certain** |
| All other §4 content (M-09, M-10, M-11, the widened joint counts, the 21-way tie) | `monitor_report_2026-09-13.md` — **not re-measured today** | Inherited |
| Cross-domain count 20 of 139 | Corpus byte-identical; **not recounted** | Inherited |
| Vertex, Novo, Zealand status | Secondary sources, not re-fetched this run | **Likely** |
| File ages | Internal `generated` fields read today + directory listings; OS mtimes unreadable | **Certain** where the field exists |

No snapshot was written this run — no Python executed, and review runs do not modify hub files.

**Sources.** ClinicalTrials.gov API v2 — 1 version read, 29 study/count queries. PubMed
E-utilities `esearch`/`esummary` — 26 queries. Primary web fetches — 3
([FDA, Tzield pediatric Stage 3, 2026-06-12](https://www.fda.gov/drugs/news-events-human-drugs/fda-approves-drug-pediatric-stage-3-type-i-diabetes);
[FDA, first generic dapagliflozin, 2026-04-07](https://www.fda.gov/drugs/drug-alerts-and-statements/fda-approves-first-generic-dapagliflozin-tablets);
[FDA, first generic liraglutide, 2024-12-23](https://www.fda.gov/news-events/press-announcements/fda-approves-first-generic-once-daily-glp-1-injection-lower-blood-sugar-patients-type-2-diabetes)).
Web search — 3 queries. Local files read: `monitor_report_2026-09-13.md`,
`baseline_clinical_trials.py`, `literature_gap_data.json`, `pubmed_recent_latest.json`,
`clinical_trials_latest.json`, `teplizumab_sNDA_decision_prep.md`, greps of `agent_state.json`
and the 2026-06 monitor reports, directory listings.

*Generated by the Diabetes Research Hub automated monitor — 2026-09-14*
