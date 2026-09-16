# Diabetes Research Hub — Monitor Report

**Run date:** 2026-09-11 (automated)
**Prior report:** monitor_report_2026-09-10.md
**Mode:** Review run. No existing hub files modified.
**Environment note:** The Linux sandbox failed to mount again — 4th consecutive day, same Plan9
error, now attributed to a Windows update released 2026-09-08. No Python executed. All registry
and PubMed figures below are live API reads made through the browser; all file facts come from
reading the files. OS mtimes remain unreadable — file ages use each file's internal `generated`
field.

---

## Headline

**The 09-06 report's #1 action was executed today, five days late. The results are below. And
yesterday's central methodological finding was built on a premise that one query falsifies.**

Two things happened, and they are the same thing seen twice.

**First: ATTAIN-2 was read.** On 2026-09-06 this hub caught `NCT05872620` — orforglipron
Phase 3, n=1,613 — within two days of its registry posting, made reading the results section
recommended action **#1**, and wrote *"act on it while it is still an information edge."* The
09-08 report corrected the "edge" framing (the trial is published in *The Lancet*) but kept the
item, noting *"the effect sizes matter."* On 09-09 it appears once, in a list. On 09-10 the same
seven-record results window was re-derived from scratch and the report discussed only the three
`TERMINATED` records in it, walking past a 1,613-patient Phase 3 of a tracked therapy sitting in
the same list.

Nobody had opened the results section. It has now been opened (§2). Reading it produced a
discrepancy nobody had noticed.

**Second: yesterday's "clean natural experiment" had no experiment in it.** The 09-10 report
concluded that `LastUpdatePostDate` decay is event-driven rather than time-driven, on the
strength of 2026-09-10 being a zero-publication day. It was not a zero-publication day. The
registry posted **1,221 updates** on 09-10; they were simply not visible yet when the query ran.

```
  AREA[LastUpdatePostDate] = 2026-09-10
  ────────────────────────────────────────────────
  read on 09-10 (the gate, D+0)         0
  read on 09-11 (today, D+1)        1,221
```

The gate said FAIL and the gate was right not to diff. Its *reason* was wrong, and the report
built a conclusion on the reason. [Certain — both counts are direct `countTotal` reads]

The common shape: **this hub is better at generating findings than at spending them.** Yesterday
named that as meta-defect #14 and prescribed an open-findings ledger. The prescription is right;
today is the second consecutive day it went unwritten while a third instance accumulated.

---

## 1. File System Status

| File | Internal `generated` | Age | Δ vs 09-10 |
|------|----------------------|-----|-----------|
| `literature_gap_data.json` | 2026-09-08 03:17:27 | 3d | — |
| `literature_gap_report.md` | 2026-09-08 03:17 | 3d | — |
| `pubmed_recent_latest.json` | 2026-09-06 09:18:08 | 5d | — |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 02:38:16 | 5d | — |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 (v1.1 hdr says Mar 31) | 11d | — |
| `clinical_trials_latest.json` | 2026-07-17 02:05:53 | **56d** | **still a broken pointer** |
| `hub_monitor_report.md` | 2026-07-17 02:16:51 | **56d** | still stale |
| `hub_monitor_state.json` / `clinical_trials_summary.md` | 2026-07-17 | **56d** | still stale |
| `Diabetes_Research_Tracker.xlsx` | — | **56d** | **still lock-held** |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 | 180d | — |

**No file in `Analysis/Results/` carries a 2026-09-11 date.** Newest artifacts of any kind are
`monitor_report_2026-09-10.md` and `iterate_run_report_2026-09-10.md`. The scripts did not run.

`.~lock.Diabetes_Research_Tracker.xlsx#` still present. The tracker update has been outstanding
since 09-01 — **ten days**, now covering ATTAIN-2, ladarixin, ZUPREME-2, and the Mounjaro CV
label.

**09-07 test residue: all four files still present**, unchanged for four days — `_wtest.txt`,
`.gap_checkpoint.json.__unlinktest`, `.gap_checkpoint.json.testbak`, root `.wtest`.

One item from `iterate_run_report_2026-09-10.md` deserves restating here because it is not a
monitor finding and will otherwise be lost: **the dashboard builders were repaired on 09-09 and
09-10 but never executed.** The HTML in `Dashboards/` and `docs/Dashboards/` still contains every
false citation that was removed from the source scripts. A grep of the scripts reports the hub
clean; a reader sees the old text. `origin/main` remains frozen at 2026-04-20 — **144 days**.

---

## 2. Clinical Trial Changes

### Freshness gate: **FAIL for today — and the gate itself needs a one-word fix**

| Query, run 2026-09-11 | Count |
|---|---:|
| `LastUpdatePostDate` = 2026-09-11 (D+0) | **0** |
| `StudyFirstPostDate` = 2026-09-11 (D+0) | **0** |
| `LastUpdatePostDate` = 2026-09-10 (D+1) | **1,221** |
| …diabetes-only slice, 09-10 | **27** |
| …diabetes-only slice, 09-11 | **0** |

A `LastUpdatePostDate` bucket reads **0 on its own day** and fills the next. So "today = 0" is a
lag artifact and carries no information about whether the registry is publishing. The gate should
query **D−1, not D**. As written it will return FAIL every single day, forever, and yesterday it
was read as a substantive finding about the world. [Certain]

### The decay rule, corrected

Yesterday's table is reproduced with today's column added. The 09-09 and 09-10 readings are
inherited from the prior report and were not re-verifiable today; the 09-11 column is mine.

```
  bucket      09-09 rdg   09-10 rdg   09-11 rdg      Δ (24h)
  ──────────────────────────────────────────────────────────
  Fri 09-04       842         842         826          −16
  Tue 09-08     1,033       1,033         998          −35
  Wed 09-09     1,297       1,297       1,189         −108
  Thu 09-10       —             0       1,221       +1,221
  Fri 09-11       —           —             0            —
```

Three buckets that yesterday were called "byte-identical, 24 hours apart" all moved in the
following 24 hours. Yesterday's report flagged this as n = 1 and said a second quiet day would
confirm it. The second observation does not confirm it — and the first observation's premise is
void, because 09-10 published 1,221 records.

The operational rule is **unchanged and now better supported**: a historical `LastUpdatePostDate`
day-count is not reproducible and must never be stored. What is withdrawn is the *explanation*
(event-driven vs time-driven decay), which is once again unresolved. The shape that survives is
descriptive: **a bucket reads 0 on day D, peaks on D+1, then decays.** [Certain for the shape;
the mechanism is now Guessing again]

There is a loose end I cannot close: if D+0 reads 0, the prior report's "09-09 reading = 1,297"
column cannot have been a same-day read. Either the lag is sub-daily and depends on run time, or
that column was inherited rather than measured. Flagged, not resolved.

### ★ NCT05872620 — ATTAIN-2, read at last

| | |
|---|---|
| Official title | Phase 3, randomized, double-blind, once-daily oral LY3502970 vs placebo in adults with obesity or overweight **and type 2 diabetes** (ATTAIN-2) |
| Sponsor | Eli Lilly and Company |
| Design | PHASE3, n = 1,613 randomized (placebo 630 / 6 mg 329 / 12 mg 332 / 36 mg 322) |
| Status | COMPLETED 2025-08-08 |
| Results first posted | **2026-09-04** |
| Regulatory context | Orforglipron approved **2026-04-01** as **Foundayo**, chronic weight management only — **not** a T2D indication |

**Primary endpoint — percent change in body weight, baseline to Week 72 (LS mean, MMRM):**

```
  placebo   ─2.21%   ▏▏
  6 mg      ─5.50%   ▏▏▏▏▏▏
  12 mg     ─7.78%   ▏▏▏▏▏▏▏▏
  36 mg    ─10.54%   ▏▏▏▏▏▏▏▏▏▏▏

  vs placebo    Δ        95% CI            p
  6 mg       −3.28   [−4.10, −2.47]     <.001
  12 mg      −5.56   [−6.48, −4.65]     <.001
  36 mg      −8.33   [−9.34, −7.32]     <.001
```

**Glycemic endpoints (secondary) — the ones this hub actually exists for:**

| Endpoint, Week 72 | Placebo | 6 mg | 12 mg | 36 mg |
|---|---:|---:|---:|---:|
| ΔHbA1c (%) | −0.14 | −1.29 | −1.60 | **−1.79** |
| ΔHbA1c vs placebo | — | −1.16 [−1.34, −0.98] | −1.46 [−1.62, −1.30] | −1.65 [−1.82, −1.49] |
| HbA1c < 7.0% (%) | 23.0 | 70.0 | 78.0 | **85.1** |
| HbA1c < 6.5% (%) | 10.6 | 56.2 | 67.5 | **75.0** |
| ΔFasting glucose (mg/dL) | +1.2 | −33.0 | −41.1 | **−45.8** |
| ≥5% weight loss (%) | 24.4 | 49.8 | 60.2 | 72.8 |
| ≥10% weight loss (%) | 7.0 | 23.9 | 35.5 | 50.1 |
| ≥15% weight loss (%) | 1.9 | 7.3 | 17.7 | 28.4 |

All comparisons p < .001. An HbA1c reduction of **1.79 percentage points** with **75% of
participants reaching < 6.5%** is, on its face, a strong oral-agent glycemic result in a
population with established T2D.

**Participant flow, discontinuations (placebo / 6 / 12 / 36):**

```
  Withdrawal by subject   38 / 20 / 10 / 10
  Lost to follow-up       17 /  4 /  5 /  2
  Adverse event            5 /  7 /  6 /  3
  Death                    4 /  0 /  4 /  2
  Lack of efficacy         4 /  0 /  0 /  0
```

Dropout is *higher on placebo* on every category except AE and death. **Caveat:** these are
study-level discontinuations in the participant-flow module, not study-drug discontinuations.
An AE-discontinuation count of 3/322 at the top dose is far below what GLP-1 class experience
would predict, which is itself evidence that this field is not measuring drug discontinuation.
Do not quote it as a tolerability figure. [Certain that these are the posted flow numbers;
Certain that they are not a drug-discontinuation rate]

### ★ The estimand discrepancy — new, and it matters for how the hub cites this trial

The 09-08 report recorded ATTAIN-2's published headline as **5.1% / 7.0% / 9.6% vs 2.5%**, from
*The Lancet* (`S0140-6736(25)02165-8`) via Lilly investor releases and secondary coverage. The
registry posts **5.50 / 7.78 / 10.54 vs 2.21**. Same trial, same doses, same 72 weeks, four
different numbers.

```
  arm        published   registry      Δ
  ─────────────────────────────────────────
  placebo      −2.5%      −2.21%     +0.29
  6 mg         −5.1%      −5.50%     +0.40
  12 mg        −7.0%      −7.78%     +0.78
  36 mg        −9.6%     −10.54%     +0.94
```

The registry's own population description names the cause: *"All data points obtained during the
treatment period, defined as at or after baseline up to the earliest date of discontinuation of
study drug or initiation of prohibited weight management treatments."* That is an **efficacy
(on-treatment) estimand**. The published figures are almost certainly the **treatment-regimen
estimand** — all randomized participants, discontinuers included. Censoring discontinuers removes
people who stopped and regained, so the on-treatment estimate is larger, and larger by more at
higher doses. The gap widens monotonically with dose, which is exactly what that mechanism
predicts.

**Only one body-weight primary is posted to the registry, and it is the efficacy estimand.** The
treatment-regimen figures appear nowhere in the registry record.

Why this is worth the hub's time: two people can cite ATTAIN-2 36 mg as "9.6%" and "10.5%" and
both be correct. Under the Doctrine's QA checklist this is a *bias in selection of reported
result* question, and the hub has no field anywhere in its schema for which estimand a number
came from. Any number the hub carries forward must travel with its estimand.

**Evidence rating:** the registry figures are **BRONZE** — a single registry-posted source,
unpublished in that form. Note that the hub's corpus also holds **PMID 42577069** (*Obesity
Pillars*, Sept 2026), a post hoc subgroup analysis of ATTAIN-1 and ATTAIN-2 in patients ≥ 65.
That is **not** an independent second source: it is the same patients. Per Doctrine Lesson 7,
counting it would be counting one trial twice. Reaching SILVER requires reading the *Lancet*
primary itself. [Certain for the registry values; **Likely** for the estimand explanation —
I have not read the *Lancet* paper, and the published figures are inherited from the 09-08
report's secondary sources, not verified today]

*This also means the 09-10 report's SILVER rating for ladarixin was one tier generous by the
Doctrine's own definition — a single registry posting plus this hub's own prior reading of it
is one source, not two. Ladarixin should read BRONZE until someone publishes it.*

### Blind spot: stable at 34, unchanged in 24h

| Query, run today | Count |
|---|---:|
| Diabetes, results posted since 2025-01-01, **any status** | **378** |
| …restricted to `COMPLETED` (what the hub collects) | 344 |
| **Structurally invisible to the hub** | **34 (9.0%)** |
| Type 1 diabetes, any status | 89 |
| Type 1 diabetes, `COMPLETED` | 80 |
| **T1D records invisible** | **9** |

No movement since 09-10 (32 on 09-01 → 34 on 09-10 → 34 today). Empirically confirmed against the
hub's own data: `NCT04628481` (ladarixin) and `NCT07030868` (LY3549492, Lilly, terminated for
business reasons) are both in today's results window and **neither appears anywhere in
`clinical_trials_snapshot_2026-09-06.json`**. ATTAIN-2 does appear, because it is COMPLETED. The
status clause is the whole explanation. [Certain — grep of the snapshot, 0 matches each]

### The full 7-record results window, named

Yesterday's report established the count and discussed three of them. All seven, for the ledger:

| Posted | NCT | Phase | n | Status | Sponsor | Study |
|---|---|---|---:|---|---|---|
| 09-09 | NCT05232071 | 2 | 39 | COMPLETED | Inventiva | Lanifibranor ± empagliflozin, NASH + T2D |
| **09-04** | **NCT05872620** | **3** | **1,613** | COMPLETED | **Eli Lilly** | **ATTAIN-2 — orforglipron, obesity/overweight + T2D** |
| 09-02 | NCT04828785 | NA | 215 | COMPLETED | UNC Chapel Hill | Food As Medicine for Diabetes |
| 08-31 | NCT04628481 | 2 | 289 | **TERMINATED** (futility) | Dompé | Ladarixin, recent-onset T1D |
| 08-31 | NCT04416269 | 4 | 85 | **TERMINATED** | Emory | Oral antidiabetics in hospital |
| 08-31 | NCT07030868 | 2 | 1 | **TERMINATED** (business) | Eli Lilly | LY3549492, obesity/overweight + T2D |
| 08-27 | NCT04506151 | NA | 144 | COMPLETED | UIC | Sleep optimization, T1D glycemic control |

`NCT07030868` is worth one line: a Lilly Phase 2 terminated for strategic business reasons with
**one participant enrolled**. Not science, but it is a pipeline signal the hub cannot currently
see.

### Category counts: one trial left the T2D active set

| Category | 09-09 | 09-10 | 09-11 | Δ |
|----------|------:|------:|------:|---:|
| T1D Cure & Cell Therapy | 157 | 157 | 157 | 0 |
| T1D Immunotherapy & Prevention | 77 | 77 | 77 | 0 |
| T2D Novel Therapies (Ph 2–3) | 151 | 151 | **150** | **−1** |
| Diabetes Technology (Devices) | 246 | 246 | 246 | 0 |
| Diabetes Recently Completed w/ Results | 344 | 344 | 344 | 0 |

Five live queries replicating `baseline_clinical_trials.py` verbatim. **Which trial left cannot
be determined** — no NCT-ID snapshot has been written since 09-06, so there is nothing to diff
against but a 5-day-old file. This is the first time the collector outage has cost a concrete
answer rather than a hypothetical one. [Certain for the counts; the cause of the −1 is unknown]

### ZUPREME-2 watch: still open, unfired

`NCT06926842` (petrelintide, Zealand/Roche, Phase 2, n = 221) re-checked today: `overallStatus`
**COMPLETED**, `hasResults` **false**, last update 2026-09-09 — unchanged for 48 hours. Zealand's
H2-2026 topline guidance confirmed today against the company pipeline page and the H1-2026
results release. No readout. The watch is correctly placed. [Certain for registry state;
**Likely** for readout timing]

---

## 3. PubMed Highlights

Corpus unchanged since 2026-09-06: **139 papers, 16 alert domains, 30-day lookback**. Now **5
days stale**. (Task spec says 15 domains; the script defines 16. Fourth report to note this.)

### Volume

`diabetes` (all), Entrez-dated 2026-09-06 → 2026-09-11: **874** new records, up from 674 over the
4-day window yesterday — ~175/day, flat. The corpus has missed all of them.

### The orforglipron literature is thicker than the corpus shows

Seven orforglipron papers carry Entrez dates in the trailing 30 days; the corpus holds four
(`therapy_hits.orforglipron`: total_count 8, paper_count 5 — the `retmax: 5` ceiling again).
What is in the corpus, and worth reading in this order:

1. **PMID 42607698** — *Long-term safety of oral orforglipron in Japanese participants with type
   2 diabetes (ACHIEVE-J): a multicentre, randomised, open-label, parallel-group phase 3 trial.*
   *Lancet Diabetes Endocrinol*, 2026 Aug 17. DOI `10.1016/S2213-8587(26)00138-5`. Yabe D,
   Shiraiwa T, Ugai H. PubMed pubtype: **Randomized Controlled Trial / Clinical Trial, Phase III**.
   **This is a Level 1b source on a tracked therapy in an East Asian T2D population, and it has
   been in the corpus since 09-06 unmentioned.** It is the natural independent companion to the
   ATTAIN-2 read above — different trial, different population, same molecule.
2. **PMID 42577069** — post hoc ATTAIN-1/ATTAIN-2 subgroup, age ≥ 65. *Obesity Pillars*, Sep 2026.
   Same patients as ATTAIN-2; see the independence caveat in §2.
3. **PMID 42607699** — accompanying commentary on ACHIEVE-J, same issue.
4. **PMID 42696191** — *Oral Incretin-Based Therapies for Weight Management*, review.

Outside the corpus, in window, and not retrieved: PMID 42715144 (*Am J Nephrol*, orforglipron and
renal outcomes, 09-09), PMID 42706941 (*Expert Rev Clin Pharmacol* editorial on weight
maintenance after GLP-1 discontinuation, 09-08), PMID 42582425 (*Front Pharmacol*,
nephroprotective mechanisms). A renal-outcomes signal appearing twice in one month on a tracked
oral agent is the kind of cluster the hub is built to notice, and the ceiling hid it.

### Amylin coverage gap: quantified

Defect #13, raised yesterday, measured today. The query
`(amylin OR petrelintide OR cagrilintide OR amycretin) AND (obesity OR "type 2 diabetes")`,
30-day window, returns **15 records**. None of the 16 alert domains contains any of those terms;
`petrelintide` returns **6 records all-time** and is not in `therapy_hits`. So the hub's
highest-probability near-term readout (§2) has a 15-paper background literature it cannot see and
a molecule it does not track. One new query string and three new terms fix it. [Certain]

### Ladarixin: still unpublished

`ladarixin` + 30-day window returns exactly **1** record — PMID 42594352, the *Int J Radiat Biol*
term-expansion artifact the 09-10 report correctly identified as not a diabetes paper. The
289-patient null Phase 2 remains unwritten-up by anyone. [Certain]

### Reading queue — now six deep, still unread

| # | PMID | What | Flagged | Days unread |
|---|------|------|---------|------------:|
| 1 | **42607698** | ACHIEVE-J Phase 3, *Lancet D&E* — **promote to top** | new today | 0 |
| 2 | 42694848 | COL1A2/APOLD1 dual-axis, nephropathy–retinopathy. Only 4-domain paper on record | 09-06 | **5** |
| 3 | 42627334 | β-cell function 1 yr after stopping oral baricitinib, *Diabetes Care* | 09-06 | 5 |
| 4 | 42626948 | Gene-edited hypoimmune islets | 09-06 | 5 |
| 5 | 42673585 | GLP-1 RAs / co-agonists, weight loss without diabetes, *Ann Intern Med* | 09-06 | 5 |
| 6 | 42586227 | Amylin pharmacotherapy review — background for the ZUPREME-2 watch | 09-10 | 1 |

Cross-domain count inherited: **20 of 139**. Corpus byte-identical, so no recount performed.
[Certain by inheritance]

---

## 4. Gap Analysis Summary

Unchanged since 2026-09-08 03:17 (3 days). 30 domains, 435 pairs. Validation **BRONZE**.

| # | Intersection | Gap | Joint pubs | Doctrine Tier 1 alignment |
|---|--------------|----:|-----------:|---------------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | §6 Epidemiological (17/20) |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | §2 Literature Synthesis (19/20) |
| 3 | **Islet Transplant × Drug Repurposing** | 100.0 | 0 | **§4 Drug Repurposing (18/20)** |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | §6 (17/20) |
| 5 | Gene Therapy × LADA | 100.0 | 0 | §2 (19/20) |

All five sit on Tier 1 lanes, which is the point of the exercise. Two open defects carried,
neither touched:

- **Gap #3 carries three incompatible counts** across hub artifacts — 7 (`literature_gap_report.md`
  rationale), 1 (09-08 report), 2 (09-09 re-query). Three query strings, none recorded. The hub's
  lead contribution candidate cannot reproduce its own headline number. **Unresolved 3 days.**
- **Five of the top twelve gaps pair a domain against Health Equity**, a keyword-brittle concept.
  The circularity test flagged P1 on 09-01 is still unrun — **ten days**.

The §3 interaction stands: `Diabetes Drug Repurpose` returns `total_count: 1` in the alert corpus
because of the over-filter defect. The hub's top drug-repurposing *gap* and its broken
drug-repurposing *alert* are one blind spot seen from two sides.

---

## 5. Breaking News

**Nothing in the 7-day window (09-04 → 09-11) changes hub priorities.** Four searches run; every
substantive hit predates the window or is already recorded. [Likely — negative result; absence of
news is weaker evidence than presence, and four queries is not exhaustive]

- **Zealand / petrelintide ZUPREME-2** — topline still guided H2 2026, **not released**. Confirmed
  today against the Zealand pipeline page and the 2026-08-13 H1 results release. ZUPREME-1 context
  for calibration: −10.7% vs −1.7% at 42 weeks, vomiting 3% vs 6.2% placebo.
- **Vertex zimislecel** — regulatory submissions still guided for 2026; no filing announcement.
  FORWARD Phase 1/2 remains the evidence base (NEJM, PMID 40544428). Watch stands. Note the
  Doctrine's own correction of 2026-08-31: this is a **12-patient Phase 1/2**, rated SILVER, not
  the Phase 3 the superseded text claimed.
- **Orforglipron / Foundayo** — approved 2026-04-01 for chronic weight management only, **not**
  T2D. Already logged on 08-28. ATTAIN-2's glycemic data (§2) is the strongest public argument for
  a future T2D indication and there is no filing announcement for one.
- **Mounjaro / tirzepatide CV indication expansion** (2026-08-28) — still the most consequential
  recent FDA action in scope, still **not in the tracker**. Outstanding since 08-31, **11 days**.
  Primary fda.gov source still not fetched.
- **Insulin efsitora alfa** — FDA decision possible H2 2026; still not on the hub's watch list.

---

## 6. Data Quality Defects — Current List

| # | Defect | Status | Age |
|---|--------|--------|----:|
| 1 | `clinical_trials_latest.json` is a 56-day-old duplicate of the 07-17 snapshot | Open | 56d |
| 2 | `has_results` constant `False` — `HasResults` never requested in `fields` | Diagnosed 09-06; fix re-confirmed live | 5d |
| 3 | Null `title` on PMID 42698931 in `pubmed_recent_latest.json` | Open, 1 of 139 | 5d |
| 4 | Epigenetics + Drug Repurpose alert queries over-filtered | Diagnosed; two-line edit pending | 3d |
| 5 | `phase` uses two null encodings, `"NA"` and `"N/A"` | Open | — |
| 6 | **Freshness gate queries D+0, which always reads 0** — gate returns FAIL every day by construction | **Re-diagnosed today; was read yesterday as a finding** | 3d |
| 7 | Scheduled run time precedes the daily registry batch | Open — same root cause as #6 | 3d |
| 8 | `LastUpdatePostDate` history is not reproducible | Rule holds; **yesterday's mechanism explanation withdrawn** (§2) | 2d |
| 9 | Gap artifacts cite counts without recording the query string | Open | 2d |
| 10 | 41-day trial-snapshot hole (07-18→08-26); collection ~weekly | Open | 2d |
| 11 | `TERMINATED`/`SUSPENDED`/`WITHDRAWN` absent from all five collectors — 34 records invisible, 9 T1D | Open; **confirmed empirically today** against the 09-06 snapshot | **10d** |
| 12 | retmax ceiling discards 85.9% of matching records | Open; **cost demonstrated today** (3 orforglipron papers lost, §3) | 10d |
| 13 | Amylin class uncovered in `therapy_hits` and all 16 alert queries | **Quantified today: 15 in-window papers invisible** | 1d |
| 14 | Findings are not carried forward between reports | **Third instance today: ATTAIN-2** | 1d |
| 15 | **No estimand field anywhere in the hub's schema** — trial effect sizes are stored as bare numbers | **New today** (§2) | — |
| 16 | **Dashboard builders repaired 09-09/09-10 but never executed; `origin/main` frozen 144 days** | Open — carried from the iterate run | 2d |

---

## 7. Recommended Actions

Ranked. ▲ = new or re-ranked today.

1. ▲ **Fix the freshness gate to query D−1.** One-character change to a date offset. As written it
   returns FAIL unconditionally and yesterday it produced a false finding about the registry. This
   is both the cheapest and the highest-leverage item in the list.

2. ▲ **Log ATTAIN-2 in the tracker with its estimand recorded.** The numbers are in §2 and were
   read today; the item has been P1 since 09-06. Record **efficacy estimand, registry-posted,
   BRONZE**, and record separately that the published *Lancet* figures differ and are the
   treatment-regimen estimand. Clear `.~lock.Diabetes_Research_Tracker.xlsx#` first. Log ladarixin
   (BRONZE, not SILVER) and the Mounjaro CV label in the same pass.

3. ▲ **Add an `estimand` field to the trial schema.** Defect #15. Any weight or HbA1c effect size
   without it is not reproducible, and the hub is one preregistration away from citing two
   different correct numbers for the same arm.

4. **Add the terminated statuses to the collector.** One clause in `baseline_clinical_trials.py`
   query #5: `AREA[OverallStatus](COMPLETED OR TERMINATED OR SUSPENDED OR WITHDRAWN)`. Still ahead
   of "run the scripts", because running them unmodified re-buries 34 records. 10 days open.

5. **Run the two dead scripts** — after #4.
   ```
   python Analysis/Scripts/baseline_clinical_trials.py
   python Analysis/Scripts/hub_monitor.py
   ```
   56 days stale; also repairs `clinical_trials_latest.json` and restores the ability to answer
   "which trial left the T2D set" (§2).

6. ▲ **Execute the repaired dashboard builders and push.** From `iterate_run_report_2026-09-10.md`:
   ```
   python Analysis\Scripts\verify_2026_09_10_repairs.py
   python Analysis\Scripts\verify_2026_09_09_repairs.py
   python Analysis\Scripts\run_quality_improvements.py
   git add -A ; git commit -m "Citation repairs 2026-09-10" ; git push origin main
   ```
   The live site currently cites a registry cohort study as the IDF Diabetes Atlas. 144 days
   frozen.

7. ▲ **Write `open_findings.md` and re-emit it verbatim each run.** Prescribed yesterday, unwritten
   today, and ATTAIN-2 is the third item to fall through in eleven days. One line per unresolved
   finding. This report's §7 is not a substitute — actions get re-ranked, findings get dropped.

8. ▲ **Read PMID 42607698 (ACHIEVE-J).** Level 1b, Phase 3, tracked therapy, in the corpus since
   09-06, never mentioned. It is the independent companion to ATTAIN-2 and the cheapest available
   step toward a defensible orforglipron evidence tier.

9. **Cover the amylin class in both places.** Add `petrelintide`, `cagrilintide`, `amycretin` to
   `KEY_THERAPY_TERMS` **and** add an alert query. 15 in-window papers are currently invisible.
   Independent of #10 — terms alone will not build the cross-domain graph.

10. **Raise `retmax` and page the alert queries.** 85.9% discarded. Do this *before* re-running
    `baseline_pubmed_alerts.py`. Today's demonstrated cost: three orforglipron papers including a
    second renal-outcomes signal.

11. **Fix the two over-filtered alert queries** — drop the trailing AND-clause from `Diabetes
    Epigenetics` and `Diabetes Drug Repurpose`.

12. **Fix `has_results`** — add `HasResults` to `fields` *and* read `study.get("hasResults")`.
    Until then, detect new postings on `results_posted`, never on the boolean.

13. **Move the scheduled run past the daily registry batch.** Same root cause as #1.

14. **Pin the query string next to every gap count.** Gap #3 carries 7 / 1 / 2 across three
    artifacts. Resolve before it reaches a preregistration.

15. **Run the Health Equity circularity test.** P1 since 09-01, unrun for 10 days; it undermines
    5 of the top 12 gaps.

16. **Read the other 33 blind-spot records.** One has been read. It was worth reading.

17. **Keep the NCT06926842 watch on `ResultsFirstPostDate`.** Verified unchanged today.

18. **Replace consecutive-day diffing with a persistent seen-set** keyed on `results_posted` and
    `last_update_posted`.

19. **Add insulin efsitora alfa to the FDA watch list.** Standing item.

20. **Track NCT06239636 by NCT ID** (Carlsson/Uppsala) — sponsor-string watches miss
    investigator-sponsored work structurally.

21. **Add `zenagamtide`** (NCT07797335, Novo, PHASE3).

22. **Delete the 09-07 test residue** — 4 files, 4 days old, zero value.

23. **Refresh `CONTRIBUTION_STRATEGY.md`** — 180 days, predates the 08-31 doctrine edits.

24. **Fix the sandbox mount.** Four consecutive failed runs, now attributed to a 2026-09-08 Windows
    update. Every report since 09-08 has been produced by hand-querying APIs through a browser.
    That works for review but cannot write snapshots, so the collection hole widens daily —
    and today it cost a concrete answer (§2, category −1).

---

## 8. Self-Audit

- **The ATTAIN-2 read is this report's only new science, and it is five days late.** The finding
  belongs to 09-06, which caught it inside the window and ranked it correctly. Today's
  contribution is opening the file the 09-06 report told us to open, plus the estimand
  discrepancy that only appears once you do.

- **I got the ATTAIN-2 story wrong on the first pass, in the direction that flattered this
  report.** My draft headline read "the hub never saw it" — I had confirmed the record was in the
  09-06 snapshot with `results_posted` populated and `has_results: false`, and constructed a clean
  causal story in which defect #2 suppressed it. Grepping the prior reports before writing killed
  it: the hub saw ATTAIN-2, headlined it, corrected its own framing on 09-08, and then let it go
  cold. The true failure is less mechanical and more embarrassing than the one I nearly shipped.
  **Two days running, the adversarial pass has caught the primary claim.** That is now a pattern
  worth trusting more than any individual finding in these reports.

- **The estimand explanation is [Likely], not [Certain].** The registry values are read directly.
  The published values are inherited from the 09-08 report's secondary sources — I have not opened
  the *Lancet* paper. The monotonic dose-gradient in the deltas is consistent with an on-treatment
  estimand and I know of no competing explanation, but "consistent with" is not "demonstrated."
  Reading the primary would settle it and is not in the action list above because it belongs
  inside item #2.

- **Withdrawing yesterday's decay explanation is not the same as refuting it.** Decay may still be
  event-driven. What collapsed is the evidence: the test required a zero-publication day and there
  wasn't one. The operational rule — never store this field — was never at risk either way.

- **Three of today's numbers are inherited and unverifiable.** The 09-09 and 09-10 bucket readings
  come from the prior report. If they were themselves mislabelled, the Δ column in §2 is wrong in
  a way I cannot detect from here.

- **"34 invisible records" is still a count, not a reading.** Today added an empirical
  confirmation of the *mechanism* — two of the 34 are provably absent from the hub's own snapshot
  — but 32 remain unread.

- **No primary web source was fetched.** FDA, Lilly and Zealand claims rest on search summaries.
  Unchanged for four days, and still the weakest evidence in the report.

- **This report is long and its action list has 24 items, which is itself a symptom.** A list that
  long is a list nobody executes, which is how items reach 10 days old. Items 1–3 take under an
  hour combined and would retire the two defects that caused today's findings.

---

## Evidence & Provenance

| Claim | Basis | Level |
|-------|-------|-------|
| `LastUpdatePostDate` = 09-11 → 0; = 09-10 → 1,221 | CT.gov API v2, two `countTotal` reads today | **Certain** |
| Registry published 1,221 records on 09-10; the "quiet day" premise is false | Above | **Certain** |
| Buckets 09-04 / 09-08 / 09-09 now read 826 / 998 / 1,189 | Three `countTotal` reads today | **Certain** |
| Prior readings 842 / 1,033 / 1,297 | `monitor_report_2026-09-10.md`, read directly | Inherited — not re-verifiable |
| Category counts 157/77/**150**/246/344 | 5 `filter.advanced` queries replicating the script verbatim | **Certain** |
| ATTAIN-2 identity: Phase 3, n=1,613, completed 2025-08-08, results posted 2026-09-04 | CT.gov record read today | **Certain** |
| ATTAIN-2 weight −2.21 / −5.50 / −7.78 / −10.54, all p<.001 | `outcomeMeasuresModule`, read today | **Certain** |
| ATTAIN-2 HbA1c −0.14 / −1.29 / −1.60 / −1.79; <6.5% in 10.6/56.2/67.5/75.0 | Same | **Certain** |
| ATTAIN-2 registry primary uses the efficacy (on-treatment) estimand | `populationDescription` quoted verbatim from the record | **Certain** |
| Published figures 5.1 / 7.0 / 9.6 vs 2.5 | `monitor_report_2026-09-08.md` §6, sourced to *Lancet* + secondary coverage | Inherited — **not verified today** |
| The discrepancy is an estimand difference | Dose-monotonic delta + the quoted population description; *Lancet* primary not read | **Likely** |
| ATTAIN-2 evidence tier | Single registry posting; PMID 42577069 is the same patients, not independent | **BRONZE** |
| ATTAIN-2 was caught on 09-06 and ranked action #1 | `monitor_report_2026-09-06.md` §"Results posted — the headline" and §6 item 1, read directly | **Certain** |
| Orforglipron approved 2026-04-01 as Foundayo, weight management only | Web search; hub's own 08-28 report concurs | **Likely** — primary fda.gov not fetched |
| Blind spot = 34 (378 − 344); 9 of 89 T1D | 4 live `countTotal` queries + script text | **Certain** |
| NCT04628481 and NCT07030868 absent from the 09-06 snapshot | Grep of `clinical_trials_snapshot_2026-09-06.json`, 0 matches each | **Certain** |
| NCT05872620 present in the 09-06 snapshot with `results_posted: 2026-09-04`, `has_results: false` | Grep, lines 12154–12170 | **Certain** |
| Full 7-record results window as tabulated | `AREA[Condition](diabetes) AND AREA[ResultsFirstPostDate]RANGE[2026-08-26,MAX]`, 7 records read | **Certain** |
| NCT06926842 COMPLETED, `hasResults` false, updated 09-09 | CT.gov record read today | **Certain** |
| ZUPREME-2 topline not released, guided H2 2026 | Zealand pipeline page + H1-2026 release via web search; IR page not fetched | **Likely** |
| 874 new `diabetes` records 09-06 → 09-11 | E-utilities `esearch`, `datetype=edat` | **Certain** |
| 7 orforglipron papers in 30d; 4 in corpus | `esearch` + grep of `pubmed_recent_latest.json` | **Certain** |
| PMID 42607698 is ACHIEVE-J, Phase 3 RCT, *Lancet D&E* | `esummary`; pubtype read from PubMed | **Certain** |
| 15 amylin-class papers in 30d; none of 16 alert queries covers the class | `esearch` + full read of the query dictionary | **Certain** |
| `petrelintide` = 6 records all-time | `esearch` | **Certain** |
| Ladarixin still unpublished; the 1 hit is a term-expansion artifact | `esearch` + the 09-10 report's identification | **Certain** |
| No hub file written 2026-09-11; residue still present | Directory listing + internal `generated` fields | **Certain** |
| Gap top-5 and the three conflicting #3 counts | `literature_gap_report.md` + prior reports, read directly | **BRONZE** / Certain for the conflict |
| No significant breaking news in 7d | Web search, 4 queries, negative result | **Likely** |
| File ages | Internal `generated` fields; OS mtimes unreadable (sandbox down) | Certain where the field exists; unknown for `.xlsx` and `CONTRIBUTION_STRATEGY.md` |

No snapshot was written this run — no Python executed, and review runs do not modify hub files.

**Sources.** ClinicalTrials.gov API v2 (`https://clinicaltrials.gov/api/v2/studies`) — 20 live
queries including the full `outcomeMeasuresModule` and `participantFlowModule` for NCT05872620.
PubMed E-utilities `esearch`/`esummary` (`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`) —
7 queries. Web search — 4 queries (Lilly/Foundayo FDA approval, September 2026 FDA diabetes
decisions, Vertex zimislecel, Zealand ZUPREME-2). Local: `monitor_report_2026-09-10.md`,
`monitor_report_2026-09-09.md`, `monitor_report_2026-09-08.md`, `monitor_report_2026-09-06.md`,
`monitor_report_2026-08-28.md`, `iterate_run_report_2026-09-10.md`, `pubmed_recent_latest.json`,
`clinical_trials_latest.json`, `clinical_trials_snapshot_2026-09-06.json`,
`literature_gap_report.md`, `literature_gap_data.json`, `hub_monitor_report.md`,
`baseline_clinical_trials.py`, `RESEARCH_DOCTRINE.md`.

*Generated by the Diabetes Research Hub automated monitor — 2026-09-11*
