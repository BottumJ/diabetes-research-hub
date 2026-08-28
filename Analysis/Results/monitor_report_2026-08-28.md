# Diabetes Research Hub — Monitor Report

**Run date:** 2026-08-28 (automated)
**Prior monitor report:** 2026-08-27
**Data acquired this run:** `clinical_trials_snapshot_2026-08-28.json` (893 trials), `pubmed_recent_snapshot_2026-08-28.json` (163 papers)
**Existing files modified:** none — verified by mtime after write

---

## Headline: the metric this hub has been reporting for five months as "new papers" is measuring its own `retmax` cap, not the literature.

Yesterday broke the 41-day acquisition freeze. Today is the first run with two consecutive
same-provenance snapshots one day apart, which makes a test possible that has never been runnable
before: **shift a 30-day window by exactly one day and see what moves.**

A 30-day window advanced one day should lose roughly 1/30 of its contents and gain about as many.
Observed:

```
  pubmed corpus, 08-27 → 08-28   (window 07/28–08/27 → 07/29–08/28)

  carried over      118  ████████████████████████
  dropped            49  ██████████
  new                45  █████████
                    ───
  total 08-28       163      churn = 28% of the corpus, from a one-day shift
```

That is ~8× the churn a one-day shift can produce. So I took the papers that left the top-10 slots of
the **four highest-volume domains** and asked PubMed whether they still satisfy **today's** window:

```
  domain                  true count   left the slots   still inside today's window
  T2D GLP-1 New                  192          10                    9
  Diabetes AI/ML                 167          10                   10
  Diabetes Microbiome            137           7                    6
  Diabetes Biomarker             133           5                    5
                                             ──                   ──
                                             32                   30   (94%)
```

**[Certain]** — 30 of 32 papers the hub recorded as "dropped" are still in scope. They did not leave
the window. They were **pushed off the bottom of a `retmax=10`, `sort=date` result set** by papers
indexed overnight. (Measured on `domain_results.pmids` set differences, which is the exact quantity
the cap governs.)

### Why this invalidates a whole class of prior reporting

`T2D GLP-1 New` returns 192 papers into a 10-slot bucket. At ~6.4 new papers/day, the top-10 by
date turns over completely in about **1.6 days**.

```
  domain                  true count   slots   days to full turnover of the sample
  T2D GLP-1 New                  192      10    1.6   ▏
  Diabetes AI/ML                 167      10    1.8   ▏
  Diabetes Microbiome            137      10    2.2   ▎
  Diabetes Biomarker             133      10    2.3   ▎
  Diabetes Health Equity          76      10    3.9   ▌
  Diabetes Multi-Omics            62      10    4.8   ▋
  Diabetes Gene Therapy           48      10    6.3   ▉
  Diabetes Complications New      27      10   11.1   ██
  Closed Loop AP                  25      10   12.0   ██
  T2D Remission                   61      10    4.9   ▋
  T1D Stem Cell Cure              18      10   16.7   ███
  T1D Immunotherapy               17      10   17.6   ███
  ──────────────────────────────────────────────────────
  LADA New Research                9       9     —    complete, stable
  Diabetes Epigenetics             4       4     —    complete, stable
  GLP-1 Pharmacogenomics           2       2     —    complete, stable
  Diabetes Drug Repurpose          1       1     —    complete, stable
```

Every "N new papers today" and "N dropped" figure in the 03-15 → 07-17 report series was computed
this way. **Twelve of sixteen domains are capped**; in those the numbers are **cap churn, not
discovery**. In the four uncapped domains they are real. The hub has been mixing the two in a single
total. Note the split is not benign: the four honest domains are the four smallest.

This is worse than yesterday's finding that the hub sees 5–7% of its busiest domains. Undersampling
is a coverage problem you can reason about. **Unstable sampling means consecutive snapshots are not
comparable at all**, and every longitudinal claim built on them inherits the defect.

**Fix:** `retmax` alone is not sufficient — a fixed cap under a moving window is unstable at any
size. Page to the full count per domain, or make the window non-overlapping (query `today` only and
accumulate). The second is cheaper and makes "new" mean new.

---

## Finding 2 — I made a query error, caught it, and it exposed the precision half of the same problem

My first acquisition pass searched the eight key therapies as **bare terms**, because
`KEY_THERAPY_TERMS` is a bare list. The script actually builds `f'diabetes AND {therapy}'` at
line 232. The gap between those two forms:

```
  window 2026/07/28–08/27, both forms measured in the same session

  term                       bare    "diabetes AND …"    bare is inflated by
  baricitinib                  39                   4          9.8×
  dapagliflozin                70                  34          2.1×
  retatrutide                  12                  10          1.2×
  teplizumab                    7                   6          1.2×
```

The bare `baricitinib` set is dominated by dermatology — alopecia areata and atopic dermatitis, where
baricitinib is a mainstream therapy. **[Certain]** — PMID 42647672, top hit, is *"Hair loss: A
systematic approach to evaluation, diagnosis…"*.

I re-ran with the script's form and rewrote the snapshot. The corrected numbers are what appears
below. But three things are worth keeping from the error:

1. **The 08-27 snapshot's therapy counts stand** — it used the script's form. Re-measured today for
   that snapshot's window: teplizumab 6 (recorded 6), dapagliflozin 34 (34), baricitinib 4 (4),
   retatrutide 10 (recorded 9 — one paper indexed overnight, which is the expected magnitude).
   My deviation was catchable only because I could re-query both forms side by side.
   **Provenance is asymmetric and both snapshots are half-blind:** 08-27 records the `query` string
   per *domain* but not per therapy; 08-28 records it per *therapy* and **dropped the per-domain
   field** (and renamed `total_count` → `true_count`, an undocumented schema change I introduced).
   Neither file is fully auditable. Fix both directions.
2. **`pdat` filtering is leaky in the other direction too.** PMID 42647672 carries `pubdate 2026 Sep 1`
   / `sortpubdate 2026/09/01` and is returned by a window ending 08/27. **[Certain]** — the date
   filter admits out-of-window records, so window boundaries are approximate on both edges. The same
   effect is visible *inside* today's corpus: PMID 42656588 (SURMOUNT-1 post hoc) is dated
   **2026-Sep** yet sits in a window ending 08/28. (42647672 itself came from a live probe and is not
   in either snapshot — it is a dermatology paper the diabetes-qualified query correctly excludes.)
3. Re-querying the *same* term and *same* window six times returned 39 every time. The instability is
   in the index over days, not in the API within a session. **[Certain]**

---

## Finding 3 — ZEUS: a null Phase 3 from Novo Nordisk, public for 28 days, invisible to this hub

Novo Nordisk announced ZEUS headline results on **2026-07-31**. Ziltivekimab (once-monthly IL-6
inhibition) hit its pharmacodynamic targets — free IL-6 and hsCRP both fell as expected — and
produced **no MACE reduction**: hazard ratio **0.99 (95% CI 0.88–1.11)** in >6,300 people with
ASCVD, CKD and inflammation. HERMES (heart failure) and ARTEMIS (post-MI) continue, reading out H1
2027. Novo booked a non-cash impairment in Q3.

The hub has never mentioned it. Not in any monitor report; `ziltivekimab` returns **0 records** in
both the 08-27 and 08-28 trial snapshots.

**Cause — [Certain].** Every trial query is scoped `AREA[Condition](diabetes)`. ZEUS is registered on
ASCVD/CKD/inflammation. And no PubMed alert domain covers anti-inflammatory cardiovascular outcomes.
The trial is invisible to both halves of the pipeline simultaneously.

**Why it should not have been invisible.** CKD and CV outcomes are two of the hub's own 30 gap
domains (`Nephropathy DKD`, `CV Complications`). A large fraction of a CKD+ASCVD+inflammation cohort
is diabetic. And a null result on IL-6 inhibition is directly informative about the
anti-inflammatory hypothesis that also underwrites **baricitinib in T1D** — which is one of the
hub's eight tracked therapies with two Lilly Phase 3 trials recruiting.

This is a different failure from yesterday's Sana finding. That one was a *field*-scoping error
(`LeadSponsorName` only). This is a *condition*-scoping error: **the hub cannot see diabetes-relevant
trials run in comorbid populations.** Same consequence, different line of code.

---

## Finding 4 — the hub was holding the Libre Duo trial while the FDA authorized the device

On **2026-08-25** the FDA granted Abbott **De Novo authorization** for **Libre Duo 10 Day**, the
first wearable continuously measuring both glucose and ketones, indicated ages 2+, following
breakthrough-device designation and six studies in >600 participants. Abbott plans a US launch this
year.

```
  NCT07739342   "Evaluating the Occurrence of DKA in People With Type I Diabetes"
                lead sponsor : Abbott Diabetes Care
                intervention : Abbott Continuous Dual Glucose Ketone Monitoring System
                n = 1200 · NOT_YET_RECRUITING · first posted 2026-07-31

  in 07-17 latest.json   NO
  in 08-27 snapshot      YES
  in 08-28 snapshot      YES
  flagged by the hub     never
```

**[Certain]** on all four rows — direct membership tests plus a live record fetch.

`Diabetes Technology (Devices)` holds **176** of the 893 deduplicated trials (246 raw hits before
deduplication; the five category queries return 972 rows for 893 distinct trials). It is the hub's
second-largest category after `Diabetes Recently Completed with Results` at 341. It produced no
signal on the most consequential diabetes-device regulatory event of the month, while holding the
sponsor's own trial of the authorized system.

Yesterday's DIAGNODE-3 finding said registry status lags sponsor disclosure. Today's says something
sharper: **the hub's corpus already contained the entity. What it lacks is any channel that carries
events about entities it holds.** A trial record is a static row; approvals, terminations and
readouts arrive elsewhere. Adding a sponsor/FDA event feed keyed to the ~900 NCTs already on disk is
a smaller job than any query fix on the P1 list, and it would have caught both DIAGNODE-3 and this.

---

## File System Status

| File | Modified | Age | State |
|---|---|---|---|
| `clinical_trials_snapshot_2026-08-28.json` | 2026-08-28 | 0 d | **NEW this run** — 893 trials |
| `pubmed_recent_snapshot_2026-08-28.json` | 2026-08-28 | 0 d | **NEW this run** — 163 papers |
| `clinical_trials_snapshot_2026-08-27.json` | 2026-08-27 | 1 d | unchanged |
| `pubmed_recent_snapshot_2026-08-27.json` | 2026-08-27 | 1 d | unchanged |
| `clinical_trials_latest.json` | 2026-07-17 | **42 d** | STALE — deliberately not overwritten |
| `pubmed_recent_latest.json` | 2026-07-17 | **42 d** | STALE — deliberately not overwritten |
| `hub_monitor_report.md` | 2026-07-17 | **42 d** | STALE — no file-change scan since |
| `literature_gap_data.json` | 2026-07-18 | **41 d** | STALE — `date_range` ends 2026/07/17 |
| `literature_gap_report.md` | **2026-08-28 08:41** | 0 d | **MISLEADING — and it re-rendered during this run.** See below |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | 42 d | unchanged |

**The freshness illusion, day 5 — and this run caught it happening.**

At the start of this run `literature_gap_report.md` was dated 2026-08-27 03:27. At the end of this
run — same file, **identical byte count (10,570)**, and I never wrote to it — it read:

```
  **Generated:**  2026-08-28 08:41     ← advanced mid-run, by something else
  **Date range:** 2020/01/01 to 2026/07/17    ← unchanged; data still 42 days old
  md5  f7e3cc1e2ede4247496e8a4833252602
```

**[Certain]** — mtime observed before and after, content header re-read, and no write to this path
appears in this run. Some other process re-renders this report's header **without re-running the
analysis**. That is the mechanism behind the illusion, observed directly rather than inferred, and it
is a stronger statement than the previous four reports could make: the file does not merely *look*
fresh, something is actively *making* it look fresh every day.

A reader scanning the header sees a file generated minutes ago over data frozen since 17 July.
Flagged 08-24, 08-25, 08-26, 08-27, and now caught in the act. Find the writer — the likely
candidates are `gap_analysis_daily.py` and `refresh.ps1` — and make it either re-run the analysis or
stamp the data vintage instead of the render time.

Today's snapshots carry an `acquired_by` provenance string naming the sandbox, the source script,
and every deviation from it — including, per therapy, the literal query string used. Copy that
pattern into the gap report header.

---

## Clinical Trial Changes — a genuinely quiet day

```
                        08-27      08-28     Δ
  total trials            892        893     +1
  new trials                            1
  dropped                               0
  status changes                        2
  RECRUITING              282        280     −2
  Phase 3 RECRUITING       57         57      0
  with results_posted     341        342     +1
  new results on trials already in corpus    0
```

The zero on the last row is expected, not a failure — the "Recently Completed with Results" filter
admits trials only once results exist, so no trial can ever be *observed* transitioning. Established
[Certain] yesterday; confirmed again.

The single new trial is **NCT04506151** (Sleep-Opt, U. Illinois Chicago, completed, first posted
2020) entering via the results filter. Not a new study — a five-year-old one whose results posted.

### Both status changes are worth a note

| NCT | Sponsor | Phase | 08-27 → 08-28 | |
|---|---|---|---|---|
| NCT07502495 | Biomea Fusion | 2 | RECRUITING → **ACTIVE_NOT_RECRUITING** | enrollment closed |
| NCT07495956 | Shenzhen Geno-Immune | 1/2 | RECRUITING → **NOT_YET_RECRUITING** | *backwards* |

**NCT07502495 — icovamenib, and it belongs in the tracker.** Biomea Fusion's oral covalent menin
inhibitor in T2D not achieving glycaemic targets; n=64, completion 2027-09; `lastUpdatePostDate`
**2026-08-28**, i.e. today. Menin inhibition is a **β-cell regeneration** mechanism, which is the
hub's Beta Cell Regen domain and half of confirmed-SILVER gap #2. Its sibling **NCT07502508** remains
RECRUITING, so the program is not stopping — one arm closed enrollment.

**NCT07495956 moved backwards.** RECRUITING → NOT_YET_RECRUITING, verified live
(`lastUpdatePostDate 2026-08-27`). This is a real registry edit, not a diff artifact. Any monitor
logic that models trial status as a forward-only state machine will mishandle it. Worth checking
`hub_monitor.py` before it silently swallows one of these.

### Registry drift — stop quoting the number

Trials whose completion date has passed but whose status is not COMPLETED:

```
  measured 2026-08-28
  on the 08-27 file    106
  on the 08-28 file    106     no movement in 24 h
```

Yesterday's report gave **105** on the 08-27 file. I get 106 on the identical file. The difference
is how month-only completion dates (`2026-08`) are coerced to a day. **The metric is
definition-sensitive at the ±1% level and three different values (119, 105, 106) have now been
published in four days.** Fix the definition in code, or drop the figure. Do not keep quoting it.

### Key organizations

```
  Vertex           3 → 3      VX-880 Ph3 ×2 RECRUITING, VX-264 Ph1/2
  Eli Lilly       33 → 33
  Novo Nordisk    28 → 28     ← does NOT include ZEUS; see Finding 3
  AstraZeneca      9 → 9
  Boehringer       4 → 4
  Sana Biotech     0 → 0      correct as lead sponsor; UP421 still invisible (08-27 Finding 2)
```

---

## PubMed Highlights

163 unique papers, 16 domains, window **2026/07/29 – 2026/08/28**. Read the "45 new" with
Finding 1 in hand: in the twelve capped domains it is not a discovery count.

### Cross-domain papers — 16 of 163 (9.8%), 5 new

The two highest-value carryovers are unchanged and still unread:

- **4 domains — PMID 42626948**, *"Gene-edited hypoimmune islets as a cure for type 1 diabetes: a
  review"* (Expert Opin Biol Ther, 2026-08-21). T1D Stem Cell Cure × T1D Immunotherapy × Gene
  Therapy × teplizumab. Covers exactly the technology in the trial the hub cannot see (UP421,
  NCT06239636).
- **PMID 42627334** — *"β-Cell Function and Diabetes Outcomes 1 Year After Stopping Oral
  Baricitinib"*, **Diabetes Care** 2026-08-21. Second consecutive recommendation. Now sharper: with
  ZEUS null on IL-6 (Finding 3), off-treatment durability of JAK inhibition in T1D is the live
  question in immunomodulation. **Level 1b–2b pending full text.**

New this run, worth a look:

- **PMID 42649514** — *"Disease-modifying anti-diabetic drugs (DMADDs): bridging the SIMPLE approach
  to disease interception"*, **Cardiovascular Diabetology** 2026-08-26. T2D Remission × retatrutide.
  A disease-interception framing is directly usable by the hub's gap-to-hypothesis pipeline.
- **PMID 42654248** — *"The Gut Microbiota-Host Epigenetic Axis: … Ethnic Disparities"* (Nutrients,
  2026-08-15). Biomarker × Microbiome, and its subject is disparities — which is **Microbiome Gut ×
  Health Equity**, an unclassified gap at 84.5. A paper landing inside a claimed gap is a falsifier;
  it belongs in the gap review queue, not the reading queue.
- **PMID 42656588** — SURMOUNT-1 post hoc, glycaemia-based predictors of T2D development
  (J Endocr Soc, dated **2026-Sep**). Tier 1 #5 (prediction models) on a Phase 3 dataset. Its future
  publication date is itself an instance of the leaky `pdat` boundary in Finding 2.

**One of the 16 "cross-domain" papers is a query artifact.** PMID 42657100 is an Asian consensus on
**invasive pulmonary fungal disease**, tagged Microbiome × Health Equity — 1/16, a **6.3%**
false-positive rate on the hub's highest-priority output. (Arguably 42650724, *"Endophytic Fungal
Metabolites… Chronic Diseases and Aging"*, tagged Biomarker × Microbiome, is a second weak hit; call
it 6–13% and treat the range as the finding.)

Separately, in the **single**-domain set, PMID 42653347 — *"Smart Polymeric Wound Dressings"* — is
tagged `Closed Loop AP`, matched on the string "closed loop" in a materials-science sense. So query
imprecision is present in both the cross-domain and single-domain streams, and the cross-domain
stream is the cleaner of the two. Precision is worth auditing before the next gap run.

### Key therapies — day-over-day, and why you should not read it

```
                 08-27   08-28
  orforglipron      13      12
  retatrutide        9      10
  dapagliflozin     34      34
  icodec             5       6
  CagriSema          4       4
  teplizumab         6       4
  baricitinib        4       3
  zimislecel         0       0
```

These are `Count` values, not capped samples, so they are honest. But a one-day shift of a 30-day
window moves ±1–2 on small integers by construction. **[Certain]** — no trend is readable at this
resolution and none should be reported. Yesterday's "retatrutide more than doubled ▲▲" compared two
windows 41 days apart, which was legitimate; comparing consecutive days is not. Report these
weekly or not at all.

---

## Gap Analysis Summary

Unchanged — `literature_gap_data.json` is still the 2026-07-17 run. `project1_literature_gap_analysis.py`
overwrites existing files, which this run's charter forbids, so it remains yours to run.

**Note a discrepancy between the two gap artifacts.** Ranked by raw `gap_score`, the top of
`literature_gap_data.json` is *not* the top of `literature_gap_report.md`:

| # | `literature_gap_data.json` (raw) | expected | | `literature_gap_report.md` (curated) |
|---|---|---:|---|---|
| 1 | GWAS × Closed Loop/AP | 25.42 | → | *filtered out as methodologically distinct* |
| 2 | Drug Repurposing × CGM | 10.24 | → | *filtered out as methodologically distinct* |
| 3 | Treg/CAR-T × Neuropathy | 7.53 | = | #1 |
| 4 | Beta Cell Regen × Health Equity | 7.28 | = | #2 — **CONFIRMED SILVER** |
| 5 | Treg/CAR-T × Health Equity | 4.74 | = | #3 — **CONFIRMED SILVER** |
| 6 | Glucokinase × Health Equity | 4.25 | = | #4 — **CONFIRMED SILVER** |
| 7 | Gene Therapy × LADA | 3.34 | = | #5 |

The report's curation is correct and the raw ranking should not be quoted as "the top 5." Also note
every one of these has `pair_count = 0` and `gap_score = 100.0` — **gap score cannot rank them.**
The `expected` column already in the file does, and it separates a 25-paper shortfall from a
3-paper one. Ranking by `expected − joint` (P2 item 11) is not a refinement; it is the only ordering
the data supports.

### Tier 1 alignment

- **#4 Drug Repurposing (18/20) × #6 Epidemiological/equity (17/20)** — Drug Repurposing × Health
  Equity remains the strongest confirmed target, double Tier 1. Unchanged.
- **#3 Clinical Trial Intelligence (18/20)** — Findings 3 and 4 are direct contributions and they
  now converge with yesterday's Finding 1 on one publishable claim: *trial registries are a lagging,
  incomplete index of trial state, and condition-scoped queries systematically miss comorbid-population
  trials.* Three worked examples in two days (DIAGNODE-3, ZEUS, Libre Duo). That is enough for a
  methods paper if the cohort study in yesterday's P1.2 is run.
- **#2 Literature Synthesis (19/20)** — Finding 1 is a methodological result about automated
  literature surveillance itself: **a fixed `retmax` under a sliding window produces a sample that
  rotates faster than the window advances.** Any group running PubMed alert pipelines has this bug.
  It is small, checkable, and nobody appears to have written it down.
- **#13 Stem Cell / Islet Biology (12/20)** — Beta Cell Regen gained a second live hook:
  icovamenib (NCT07502495) closed enrollment today, alongside cadisegliatin (NCT06334133) yesterday.
  Two late-ish-stage β-cell-function assets reaching enrollment close in 48 hours.

---

## Breaking News (web check, 08-21 → 08-28)

**Two items clear the bar. Both were already public and neither was in the hub.**

1. **Abbott Libre Duo 10 Day — FDA De Novo authorization, 2026-08-25.** First wearable continuously
   monitoring glucose *and* ketones; ages 2+; breakthrough-device designation; six studies, >600
   participants; US launch planned this year. See Finding 4. **[Certain]** — Abbott newsroom release
   plus concordant trade coverage.
2. **Novo Nordisk ZEUS — Phase 3 null, announced 2026-07-31.** Ziltivekimab, HR 0.99 (0.88–1.11) for
   MACE. See Finding 3. **[Certain]** on the topline; **[Likely]** on the impairment charge and
   HERMES/ARTEMIS timing — company statement relayed by secondary outlets, primary release not
   fetched this run.

Checked, already logged, no action: orforglipron/Foundayo (weight management only, **not** T2D),
teplizumab pediatric Stage 3, Garzulys insulin aspart-fsan, retatrutide TRANSCEND-T2D-1,
DIAGNODE-3 discontinuation, avexitide LUCIDITY.

---

## Recommended Actions

**P0 — the pipeline**

1. `*_latest.json` is at **day 42**. Two same-provenance snapshots now exist one day apart and diff
   cleanly, so the scheduled job is producing usable data — it just cannot write the canonical files.
   Either amend `diabetes-data-pull`'s charter to permit writing when its own freshness check fails,
   or run locally:
   `python "C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts\run_daily_local.py"`

**P1 — what today proved**

2. **Fix the PubMed sampling before trusting any longitudinal literature claim.** Raising `retmax`
   is not enough; a fixed cap under a sliding window is unstable at any size. Either page to the
   full `Count` per domain, or switch to a non-overlapping daily window and accumulate. Until then,
   treat "new papers" in the **twelve** capped domains as meaningless and stop publishing the total.
3. **Add condition-adjacent trial queries.** ZEUS was invisible because every query is scoped
   `AREA[Condition](diabetes)`. Add CKD, ASCVD and heart-failure cohorts where diabetes prevalence is
   high, or query the ~20 tracked *assets* by intervention name instead of by condition.
4. **Build an event feed keyed to NCTs already on disk.** The hub held NCT07739342 for 28 days while
   its device was authorized, and carried NCT05018585 as active for 138 days after its sponsor killed
   it (that record is in the stale 07-17 `latest.json`, not in today's corpus — it has since left
   query scope). One weekly pass over `lastUpdatePostDate` + `whyStopped` for the ~900 tracked NCTs,
   plus an FDA approvals/De Novo check, closes both. Smaller than any query rewrite on this list.
5. **Record the query string in snapshot metadata, per domain *and* per therapy.** Neither existing
   snapshot does both: 08-27 has per-domain only, 08-28 has per-therapy only. Restore the per-domain
   field the 08-28 snapshot dropped and keep the per-therapy one, and revert or document the
   `total_count` → `true_count` rename in `domain_results`. Retroactively unauditable data is worse
   than absent data — my own bare-term error was catchable only by re-running both forms live.
6. **Fix or drop the drift metric.** 119 → 105 → 106 in four days on a definitional difference.
7. **Find whatever re-rendered `literature_gap_report.md` at 08:41 today** and stop it stamping
   render time over 42-day-old data. Start with `gap_analysis_daily.py` and `refresh.ps1`. Fifth
   consecutive day this has been flagged, first time it has been observed mid-run.
8. Carry forward, still open from 08-27: widen trial queries to `EARLY_PHASE1` + `CollaboratorName`;
   add a completed-without-results filter; widen key-therapy terms to development codes
   (`zimislecel OR "VX-880"`); correct the 07-26 report's Diamyd entry.

**P2**

9. **Re-rank gaps by `expected − joint`, not `gap_score`.** Seven top pairs all score exactly 100.0
   with `pair_count = 0` — the score cannot order them. `expected` is already in the file.
10. **Audit query precision.** 1 of 16 cross-domain hits is a string-match artifact (a fungal-disease
    consensus tagged Microbiome × Health Equity), and the single-domain stream carries at least one
    more (polymeric wound dressings matching "closed loop"). Cross-domain output is the hub's
    highest-value product and its least-validated one.
11. Widen the Health Equity query to the 19-term expansion **before** the next gap run, then re-run
    and reclassify.
12. **Tracker updates:** icovamenib NCT07502495 → ACTIVE_NOT_RECRUITING (β-cell regen, enrollment
    closed); Abbott NCT07739342 → link to Libre Duo De Novo authorization 2026-08-25; add
    ziltivekimab/ZEUS as a null-result reference for the anti-inflammatory hypothesis.

**P3 — reading**

13. **PMID 42627334** — baricitinib 1-year off-treatment, *Diabetes Care*. Second recommendation;
    now the direct counterpart to the ZEUS null.
14. **PMID 42649514** — DMADD / disease-interception framing, *Cardiovascular Diabetology*.
15. **PMID 42459945** — algorithmic discrimination in pediatric T1D training data. **Sixth
    consecutive recommendation.** Twenty minutes. Note it is **no longer in the corpus** — it entered
    on 2026-07-17 and has since aged out of the 30-day window, so nothing will surface it again.
    Read it now or drop it from the queue.

---

## Evidence Levels (per Research Doctrine)

| Claim | Level | Basis |
|---|---|---|
| 893 trials / 163 papers acquired to new dated snapshots; no existing file modified | **[Certain]** | files on disk; mtimes of `*_latest.json`, gap data and tracker verified unchanged after write |
| 30 of 32 slot-displaced papers in the 4 highest-volume domains are still inside today's window | **[Certain]** | live esearch at `retmax=250` per domain, `domain_results.pmids` set difference vs the 08-27 snapshot |
| 12 of 16 domains are capped; capped samples rotate fully in 1.6–17.6 days | **[Certain]** | `returned` vs `true_count`; turnover = 10 ÷ (`true_count`/30) |
| Bare-term therapy search inflates baricitinib 9.8× via dermatology literature | **[Certain]** | 39 vs 4 on identical window, same session; top hit is an alopecia review |
| `pdat` window admits out-of-window records | **[Certain]** | PMID 42647672 (`sortpubdate 2026/09/01`) returned by a window ending 08/27; PMID 42656588 dated 2026-Sep sits in the 08-28 corpus |
| esearch is deterministic within a session | **[Certain]** | 6 identical repeats returned 39 |
| ZEUS topline: HR 0.99 (0.88–1.11), no MACE reduction | **[Certain]** | Novo Nordisk company announcement 2026-07-31, concordant across four outlets |
| ZEUS impairment charge; HERMES/ARTEMIS read out H1 2027 | **[Likely]** | secondary relay of company statement; primary release not fetched |
| `ziltivekimab` absent from both trial snapshots | **[Certain]** | direct substring test on both files |
| Libre Duo De Novo authorization 2026-08-25, ages 2+, 6 studies / >600 participants | **[Certain]** | Abbott newsroom release; concordant trade coverage |
| NCT07739342 in corpus since 08-27 snapshot, absent from 07-17 file | **[Certain]** | membership tests on all three files |
| NCT07502495 icovamenib closed enrollment, `lastUpdatePostDate` 2026-08-28 | **[Certain]** | live record fetch |
| NCT07495956 moved RECRUITING → NOT_YET_RECRUITING | **[Certain]** | live record fetch, `lastUpdatePostDate` 2026-08-27 |
| Drift metric is definition-sensitive; 105/106 on the same file | **[Certain]** | recomputation of the identical metric |
| 1 of 16 cross-domain papers is a string-match artifact (6.3%) | **[Certain]** | PMID 42657100, subject is invasive pulmonary fungal disease |
| `Diabetes Technology (Devices)` = 176 of 893 deduped (246 of 972 raw); not the largest category | **[Certain]** | category counts in snapshot metadata vs dedup by `category` field |
| PMIDs 42459945 and 42647672 and NCT05018585 are **not** in this run's snapshots | **[Certain]** | membership tests; 42647672 and NCT05018585 are live-probe / historical only |
| `literature_gap_report.md` re-rendered during this run, header only, data unchanged | **[Certain]** | mtime 08-27 03:27 → 08-28 08:41, size identical at 10,570 B, `date_range` still 2026/07/17, no write from this run |
| The re-render comes from `gap_analysis_daily.py` or `refresh.ps1` | **[Guessing]** | not traced to a process; named as the two plausible candidates only |
| Gap score cannot order the top 7 pairs | **[Certain]** | all have `pair_count=0`, `gap_score=100.0` in the file |
| PMID 42627334 baricitinib durability | **Level 1b–2b** | *Diabetes Care*; abstract only |
| The `retmax`-under-sliding-window defect is general to PubMed alert pipelines | **[Guessing]** | demonstrated on this hub only; n=1 implementation |

**Path from [Guessing] to [Likely] on that last row:** the claim is about a *class* of pipeline, so
it needs either (a) a published alert-tool survey showing fixed-`retmax` sliding windows are the
common pattern, or (b) a simulation over the 16 domain queries showing sample turnover as a function
of `retmax` and window length, which turns an observation into a closed-form instability condition.
(b) is a short script against data already on disk and is the stronger result — it would say exactly
when a given `retmax` is safe.

---

## Sources consulted this run

- [Abbott receives FDA authorization for world's first dual glucose-ketone sensing technology (2026-08-25)](https://abbott.mediaroom.com/2026-08-25-Abbott-receives-FDA-authorization-for-worlds-first-dual-glucose-ketone-sensing-technology-for-people-with-diabetes)
- [FDA Authorizes First Wearable Device to Continuously Monitor Glucose, Ketones — Patient Care Online](https://www.patientcareonline.com/view/fda-authorizes-first-wearable-device-to-continuously-monitor-glucose-ketones)
- [First device to continuously monitor ketone and glucose levels receives FDA authorization — Healio](https://www.healio.com/news/endocrinology/20260826/first-device-to-continuously-monitor-ketone-and-glucose-levels-receives-fda-authorization)
- [Novo Nordisk provides update on the ZEUS phase 3 trial in people with ASCVD, CKD and inflammation (2026-07-31)](https://www.globenewswire.com/news-release/2026/07/31/3336733/0/en/novo-nordisk-provides-update-on-the-zeus-phase-3-trial-in-people-with-ascvd-ckd-and-inflammation.html)
- [Ziltivekimab Fails to Reduce MACE Risk in Phase 3 ZEUS Trial — HCPLive](https://www.hcplive.com/view/ziltivekimab-fails-to-reduce-mace-risk-in-phase-3-zeus-trial)
- ClinicalTrials.gov API v2 — 5 category queries (893 records), 3 direct record fetches
- NCBI E-utilities esearch/efetch — 24 alert queries (163 papers), 22 vocabulary and window-stability probes

---

## Self-audit

Every numeric claim above was re-computed against the files on disk by an independent pass before
publication. It found **seven errors in the first draft**, all now corrected: the capped/uncapped
domain split (stated 9/3, actually 12/4, in three places); the Devices category size (stated "largest,
246 of 893", actually 176 of 893 deduped and second-largest); the dropped-papers table (a wrong
domain row and a wrong total); the cross-domain false-positive rate (stated 2/16, actually 1/16); the
snapshot-provenance claim (stated backwards — 08-27 has per-domain queries, 08-28 has per-therapy);
two untested cells in the Finding 2 bare-vs-qualified table; and three identifiers presented as
current corpus members that are not (PMID 42459945, PMID 42647672, NCT05018585).

Recording this because a monitor that reports on the reliability of its own instruments has no
standing unless it applies the same test to itself. The corrections do not change any of the four
findings; they change the numbers attached to two of them.

---

*Generated by the Diabetes Research Hub monitor — 2026-08-28. Three new files written: two dated snapshots and this report. No existing file modified by this run; `*_latest.json`, `literature_gap_data.json`, `Diabetes_Research_Tracker.xlsx`, `hub_monitor_report.md` and both 08-27 snapshots verified unchanged by mtime after the write. `literature_gap_report.md` changed during the run — not by this monitor; see File System Status.*
