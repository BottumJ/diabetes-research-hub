# Diabetes Research Hub — Monitor Report

**Run date:** 2026-09-12 (automated)
**Prior report:** monitor_report_2026-09-11.md
**Mode:** Review run. No existing hub file modified. Two new files written (this report, `open_findings.md`).
**Environment note:** Linux sandbox failed to mount — **5th consecutive day**, same Plan9 error,
same 2026-09-08 Windows update. No Python executed. Every registry and PubMed figure below is a
live API read made through the browser today; every file fact comes from reading the file. OS
mtimes remain unreadable — file ages use each file's internal `generated` field.

---

## Headline

**The ZUPREME-2 watch fired three days ago. Two reports checked the wrong field and recorded it
as unfired.**

`NCT06926842` (petrelintide, Zealand/Roche, Phase 2, n = 221) was **`ACTIVE_NOT_RECRUITING` in the
hub's own 09-06 snapshot**. It is `COMPLETED` today, and has been since **2026-09-09**. The 09-10
and 09-11 reports both checked it, both saw `hasResults: false` and no `ResultsFirstPostDate`, and
both concluded the watch was "correctly placed" and unfired.

```
  NCT06926842 — what each report looked at
  ───────────────────────────────────────────────────────────────
  09-06 snapshot   overallStatus = ACTIVE_NOT_RECRUITING   ← baseline, in-hub
  09-09 registry   overallStatus = COMPLETED               ← the event
  09-10 report     read ResultsFirstPostDate → null        → "unfired"
  09-11 report     read hasResults → false                 → "unfired"
  09-12 (today)    read overallStatus, diffed vs snapshot   → FIRED, 3d ago
```

A Phase 2 flips to `COMPLETED` months before it posts results. Watching `ResultsFirstPostDate` on
a trial that has not completed yet is watching the second event and missing the first. Zealand
guides ZUPREME-2 topline for H2 2026; the status flip is the closest thing to a public leading
indicator that exists, and the hub held both halves of the diff — the snapshot and the live
record — for three days without subtracting them. [Certain for the registry states; Certain that
`ACTIVE_NOT_RECRUITING` is what the 09-06 snapshot holds — grepped, line 4031]

**And the same status clause hides far more than the 34 records the hub has been counting.**
Defect #11 has been scoped as "`TERMINATED`/`SUSPENDED`/`WITHDRAWN` are missing." That
undercounts the hole by a factor of seven, because the fifth collector requires
`COMPLETED **AND** ResultsFirstPostDate ≥ 2025`. A trial that finishes and has not yet posted
results is in neither set.

```
  Diabetes trials with a 2026 completion date, status COMPLETED
  ──────────────────────────────────────────────────────────────────
  total                                                    246
  …of which have results posted (visible to collector #5)   12   ▏
  …structurally invisible to all five collectors           234   ████████████████████

  The hub's flagship lane — T2D, Phase 2–3, first posted ≥2023
  ──────────────────────────────────────────────────────────────────
  completed in 2026                                         22
  …with results posted                                       0
  …invisible                                                22   (100%)
```

[Certain — four `countTotal` reads, query strings in the Evidence table]

Three named casualties, all in the hub's core lane, all invisible to a fresh run today:

| NCT | Study | Phase | n | Status |
|---|---|---|---:|---|
| `NCT06534411` | **CagriSema vs tirzepatide, head-to-head in T2D** | 3 | 1,023 | COMPLETED, no results |
| `NCT06323161` | CagriSema vs placebo in T2D | 3 | 274 | COMPLETED, no results |
| `NCT06926842` | ZUPREME-2, petrelintide | 2 | 221 | COMPLETED 09-09, no results |

`NCT06534411` is a 1,023-patient Phase 3 head-to-head between the two leading incretin combinations
in type 2 diabetes. It is arguably the single most consequential trial in this hub's declared scope,
and there is no query in `baseline_clinical_trials.py` that can see it.

---

## 1. File System Status

| File | Internal `generated` | Age | Δ vs 09-11 |
|------|----------------------|-----|-----------|
| `literature_gap_data.json` / `_report.md` | 2026-09-08 03:17 | 4d | — |
| `pubmed_recent_latest.json` | 2026-09-06 09:18:08 | **6d** | +1d |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 02:38:16 | **6d** | +1d |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 | 12d | — |
| `clinical_trials_latest.json` | 2026-07-17 02:05:53 | **57d** | still a broken pointer |
| `hub_monitor_report.md` / `hub_monitor_state.json` / `clinical_trials_summary.md` | 2026-07-17 | **57d** | still stale |
| `Diabetes_Research_Tracker.xlsx` | — | **57d** | **still lock-held** |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 | 181d | — |

**No file in `Analysis/Results/` carries a 2026-09-12 date before this run.** Newest prior artifact
is `monitor_report_2026-09-11.md`. The scripts did not run. Sixth consecutive day.

- `.~lock.Diabetes_Research_Tracker.xlsx#` still present. Tracker backlog now **eleven days**,
  covering ATTAIN-2, ladarixin, ZUPREME-2's completion, the Mounjaro CV label, and — new today —
  the CagriSema completion cluster.
- **09-07 test residue: all four files still present, now 5 days old** — `_wtest.txt`,
  `.gap_checkpoint.json.testbak`, `.gap_checkpoint.json.__unlinktest`, root `.wtest`. Verified by
  directory listing today.
- `open_findings.md` did not exist at the start of this run. Prescribed 09-10, 09-11. **Written
  today** (see §7 note).
- Dashboards still carry the false citations removed from their source scripts on 09-09/09-10;
  builders still unexecuted. `origin/main` frozen at 2026-04-20 — **145 days**.

---

## 2. Clinical Trial Changes

### Freshness gate: **PASS** — and yesterday's proposed D−1 fix is empirically confirmed

| Query, run 2026-09-12 | Count |
|---|---:|
| `LastUpdatePostDate` = 2026-09-12 (D+0) | **0** |
| `LastUpdatePostDate` = 2026-09-11 (D−1) | **1,165** |
| …diabetes-only slice, 09-11 | **24** |
| …diabetes-only slice, 09-12 | 0 |

Yesterday's diagnosis holds exactly. D+0 reads 0 again — second consecutive observation, so the
lag is now n = 2 and no longer a single-day curiosity. D−1 returns a full day's batch. **The gate
should query D−1; as written it returns FAIL unconditionally.** This is the cheapest open item in
the hub and it has now cost one false finding (09-10) and one wasted gate (09-11). [Certain]

### Decay, third consecutive day of measurement

```
  bucket      09-10 rdg   09-11 rdg   09-12 rdg     Δ(24h)
  ─────────────────────────────────────────────────────────
  Fri 09-04       842         826         799         −27
  Tue 09-08     1,033         998         979         −19
  Wed 09-09     1,297       1,189       1,165         −24
  Thu 09-10         0       1,221       1,104        −117
  Fri 09-11         —           0       1,165      +1,165
  Sat 09-12         —           —           0           —
```

Two regularities now have three days of support:

1. **A bucket reads 0 on day D and fills on D+1.** Observed for 09-10, 09-11. [Certain]
2. **Decay is fastest immediately after the D+1 peak, then flattens.** 09-10 lost 117 in its first
   post-peak day; the older buckets are losing 19–27/day. This is *descriptive*. A one-time
   re-dating correction at D+2 would produce it; so would several other mechanisms. I am not
   proposing one. [Certain for the numbers; mechanism **Guessing**]

The operational rule is unchanged and is the only thing that should be carried forward: **a
historical `LastUpdatePostDate` day-count is not reproducible and must never be stored.**

### Category counts: composition changed, the total lied about it

Five live queries replicating `baseline_clinical_trials.py` verbatim.

| Category | 09-06 snap | 09-09 | 09-10 | 09-11 | **09-12** | Δ 24h |
|----------|-----------:|------:|------:|------:|----------:|------:|
| T1D Cure & Cell Therapy | 156 | 157 | 157 | 157 | **158** | +1 |
| T1D Immunotherapy & Prevention | 77 | 77 | 77 | 77 | **77** | 0 |
| T2D Novel Therapies (Ph 2–3) | 152 | 151 | 151 | 150 | **151** | **+1** |
| Diabetes Technology (Devices) | 245 | 246 | 246 | 246 | **244** | **−2** |
| Diabetes Recently Completed w/ Results | 343 | 344 | 344 | 344 | **344** | 0 |

Yesterday's report flagged T2D −1 as an unexplained departure it could not identify. **Today it
reads 151 again, and that recovery is not a reversal.** A new Phase 3 (`NCT07816198`, Addpharma,
n = 354) was first-posted on 09-11 and indexed today. The departure and the arrival are different
trials; the count is back where it started and the set is not.

```
  T2D Novel Therapies — what the count hides, 09-06 → 09-12
  ─────────────────────────────────────────────────────────
  09-06 snapshot                                152
    − departures (status → COMPLETED, ≥1 confirmed)
    + 4 new registrations (09-01 … 09-11)
  09-12 live                                    151      net −1, gross ≥5 changed
```

**This is the concrete cost of not writing NCT-ID snapshots.** A flat count is not a quiet week.

### Departures recovered without a snapshot — a method that works today

Yesterday's report treated "which trial left?" as unanswerable without a fresh snapshot. It is
answerable. Query the category's *own filter* with the terminal statuses substituted and a
`LastUpdatePostDate` window:

```
  AREA[Condition](type 2 diabetes) AND AREA[Phase](PHASE3 OR PHASE2)
    AND AREA[StudyFirstPostDate]RANGE[2023-01-01, MAX]
    AND AREA[OverallStatus](COMPLETED OR TERMINATED OR WITHDRAWN OR SUSPENDED OR UNKNOWN)
    AND AREA[LastUpdatePostDate]RANGE[2026-09-06,2026-09-12]
```

Four hits, cross-checked by grep against the 09-06 snapshot to separate genuine departures from
trials that were already terminal:

| NCT | Study | Status in 09-06 snapshot | Now | Verdict |
|---|---|---|---|---|
| `NCT06926842` | ZUPREME-2, petrelintide, n=221 | **ACTIVE_NOT_RECRUITING** | COMPLETED | **departed — the headline** |
| `NCT06797869` | CagriSema, T2D + painful neuropathy, Ph2, n=142 | **ACTIVE_NOT_RECRUITING** | COMPLETED | **departed** |
| `NCT06534411` | CagriSema vs tirzepatide, Ph3, n=1,023 | *absent* | COMPLETED | already invisible |
| `NCT06323161` | CagriSema vs placebo, Ph3, n=274 | *absent* | COMPLETED | already invisible |

Same method on the device lane returns `NCT07778121` (RECRUITING → COMPLETED), `NCT06473831` and
`NCT07085741` (both ACTIVE_NOT_RECRUITING → COMPLETED, GT Metabolic), and on T1D Cure returns
`NCT06948760` (already terminal). This accounts for the device −2 and one T1D item.
[Certain — 3 API queries + 8-ID grep of the 09-06 snapshot]

**Three of the four T2D departures are amylin-class.** The hub does not track the amylin class in
any PubMed alert query (defect #13, open) and cannot see completed-without-results trials
(defect #11, re-scoped above). The cluster is invisible from both sides simultaneously.

### New registrations since 09-01

| NCT | Posted | Phase | n | Sponsor | Study |
|---|---|---|---:|---|---|
| `NCT07797335` | 09-01 | 3 | 1,778 | Novo Nordisk | AMBITION 7 — **zenagamtide** vs insulin glargine, T2D + CV risk |
| `NCT07796477` | 09-01 | 2 | 240 | CSPC Ouyi | SYH2069 injection, T2DM |
| `NCT07801820` | 09-03 | 2 | 240 | Shanghai Minwei | MWN109 tablets, T2DM |
| `NCT07816198` | **09-11** | 3 | 354 | Addpharma | AD-233A/B/C/D combination therapy |
| `NCT07796802` | 09-01 | NA | 314 | Steno Copenhagen | CGM for in-hospital T2D management |
| `NCT07802327` | 09-03 | NA | 100 | MicroTech Medical | GX-01S CGM PMCF |
| `NCT07808385` | 09-08 | NA | 32 | Mayo Clinic | DEKA TWIIST pump + Tidepool Loop **in pregnancy with T1D** |
| `NCT07814508` | **09-11** | NA | 89 | FIDAM RDC | Accu-Chek SmartGuide CGM + Predict app |

`NCT07797335` (zenagamtide) has been action item #21 for a day; it is confirmed in the live set.
`NCT07808385` is worth a second look — closed-loop delivery in pregnancy is thin literature and
sits adjacent to two Tier 1 lanes.

### Results window: nothing new since 09-09

`AREA[Condition](diabetes) AND AREA[ResultsFirstPostDate]RANGE[2026-09-04,MAX]` → **2 records**:
`NCT05872620` (ATTAIN-2, 09-04) and `NCT05232071` (lanifibranor, 09-09). Both already in the
ledger. No new postings in 72 hours. [Certain]

### Blind spot as previously measured: unchanged

378 diabetes results-posted records any status − 344 `COMPLETED` = **34**; T1D 89 − 80 = **9**.
Identical to 09-10 and 09-11. **This number should be retired** — it measures only the terminated
slice of a 234-record hole (see Headline). Keeping both numbers in circulation invites the hub to
quote the small one.

---

## 3. PubMed Highlights

Corpus unchanged since 2026-09-06 09:18: **139 papers, 16 alert domains, 30-day lookback**. Now
**6 days stale**. (Task spec says 15 domains; the script defines 16. Fifth report to note this.)

### Volume

`diabetes` (all), Entrez-dated 2026-09-06 → 2026-09-12: **1,071** records; 09-11 → 09-12 alone:
**208**. Running ~178/day, flat. The corpus has seen none of them. [Certain]

### New in-window papers the corpus cannot show — ranked

| PMID | What | Why it matters |
|---|---|---|
| **42720752** | **PROTECT trial per-protocol analysis — preserving β-cell function in children/adolescents with new-onset stage 3 T1D.** *Diabetologia*, 2026-09-10 | Tracked therapy (**teplizumab**), secondary analysis of a randomised trial, pediatric. Highest-value new item in the window. |
| 42722448 | Diabetes-related genetics and outcomes after total pancreatectomy with islet autotransplantation. *JCEM*, 2026-09-11 | Sits squarely on **Islet Transplant × GWAS/Polygenic**, which the gap analysis classifies as "methodologically distinct, expected low overlap, 0 joint pubs." See §4. |
| 42712437 | Hypoimmune platforms: from rejection to immune evasion and regulatory implications. *Transpl Int*, 2026 | Direct companion to unread queue item #4 (gene-edited hypoimmune islets, PMID 42626948). |
| 42608559 | Maximizing weight loss with CagriSema: systematic review + GRADE meta-analysis. *Naunyn Schmiedebergs Arch Pharmacol* | The evidence synthesis for the drug class whose four trials completed this week (§2). |
| 42706941 | Weight maintenance after GLP-1 discontinuation (orforglipron). *Expert Rev Clin Pharmacol*, editorial | Carried from 09-11; still outside the corpus. |
| 42711287 | Islet cell cluster size heterogeneity, early postnatal porcine pancreas. *Xenotransplantation* | Xenotransplant supply-side; adjacent to Tier 1. |

### Amylin class: still zero coverage, and now the most urgent gap in the hub

| Query, 30-day window | Count |
|---|---:|
| `(amylin OR petrelintide OR cagrilintide OR amycretin) AND (obesity OR "type 2 diabetes")` | **11** |
| `cagrisema OR cagrilintide` | **6** |
| `cagrisema OR cagrilintide`, all-time | **131** |
| `petrelintide`, all-time | **6** |

None of the 16 alert domains contains any of these terms; none is in `therapy_hits`. A drug class
with 131 papers, four trials completing this week, an NDA under FDA review, and a Phase 2 topline
guided for this half-year is completely absent from the hub's literature surveillance.
(The 30-day count reads 11 today vs 15 on 09-11 — `reldate=30` is a rolling window, not a
contradiction.) [Certain]

### Tracked-therapy pulse, 30-day

```
  retatrutide    15  ███████████████
  amylin class   11  ███████████
  orforglipron    6  ██████
  teplizumab      6  ██████
  cagrilintide    6  ██████
  ladarixin       1  ▏            (the Int J Radiat Biol term-expansion artifact — not diabetes)
  zimislecel      0
```

Ladarixin's 289-patient null Phase 2 remains unwritten-up by anyone, 12 days after termination
posted. [Certain]

### Reading queue: now ten deep

| # | PMID | What | Flagged | Days unread |
|---|------|------|---------|------------:|
| 1 | **42720752** | PROTECT per-protocol, teplizumab, pediatric — *Diabetologia* | new today | 0 |
| 2 | 42607698 | ACHIEVE-J Phase 3, *Lancet D&E* — promoted to top on 09-11, still unread | 09-11 | **1** |
| 3 | 42694848 | COL1A2/APOLD1 dual-axis, nephropathy–retinopathy. Only 4-domain paper on record | 09-06 | **6** |
| 4 | 42627334 | β-cell function 1 yr after stopping oral baricitinib, *Diabetes Care* | 09-06 | 6 |
| 5 | 42626948 | Gene-edited hypoimmune islets | 09-06 | 6 |
| 6 | 42673585 | GLP-1 RAs / co-agonists without diabetes, *Ann Intern Med* | 09-06 | 6 |
| 7 | 42586227 | Amylin pharmacotherapy review | 09-10 | 2 |
| 8 | 42722448 | TP-IAT genetics, *JCEM* | new today | 0 |
| 9 | 42712437 | Hypoimmune platforms review | new today | 0 |
| 10 | 42608559 | CagriSema GRADE meta-analysis | new today | 0 |

The queue has grown every day since 09-06 and nothing has left it. Cross-domain count inherited:
**20 of 139** (corpus byte-identical, no recount performed). [Certain by inheritance]

---

## 4. Gap Analysis Summary

Unchanged since 2026-09-08 03:17 (**4 days**). 30 domains, 435 pairs. Validation **BRONZE**.

| # | Intersection | Gap | Joint pubs | Doctrine Tier 1 alignment |
|---|--------------|----:|-----------:|---------------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | §6 Epidemiological (17/20) |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | §2 Literature Synthesis (19/20) |
| 3 | **Islet Transplant × Drug Repurposing** | 100.0 | 0 | **§4 Drug Repurposing (18/20)** |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | §6 (17/20) |
| 5 | Gene Therapy × LADA | 100.0 | 0 | §2 (19/20) |

### ★ Defect #9 resolved for Gap #3 — and the resolution is not reassuring

The hub has carried four different joint-publication counts for its lead contribution candidate.
I pulled the query strings out of `gap_analysis_daily.py` (lines 90, 104) and ran them verbatim:

```
  "Islet Transplant"  = ("islet transplant" OR "islet cell transplant")
  "Drug Repurposing"  = (diabetes AND ("drug repurposing" OR "drug repositioning"))
  joint, 2020–2026    = 0        ← this is the number the script produces
  joint, all-time     = 0
  Islet Transplant alone, 2020+  = 253   ✓ reproduces the report's table exactly
  Drug Repurposing alone, 2020+  = 621   ✓ reproduces the report's table exactly
```

Both domain counts reproduce to the digit, so these are the right strings.

```
  Gap #3, joint publications — one intersection, four answers
  ──────────────────────────────────────────────────────────────────────
  gap_analysis_daily.py, verbatim          0   (recorded today, reproducible)
  monitor_report 2026-09-08                1   (query string not recorded)
  monitor_report 2026-09-09, "re-query"    2   (query string not recorded)
  literature_gap_report.md rationale       7   (prose; "re-run 2026-09-06")
```

The machine number is **0**. The other three are hand-run ad-hoc queries whose strings were never
written down — exactly the failure defect #9 describes. **The conflict is resolved in favour of 0,
and the rationale text in `literature_gap_report.md` that claims 7 is wrong as a statement about
the script's output.**

The uncomfortable half: my own independent query using `"islet transplantation"` (the -ation form
the literature actually uses) returns **2 all-time**, and the script's string returns 0. So the
script's 0 is partly a terminology artifact, and a gap score of 100.0 built on a joint count of 0
is **softer than BRONZE implies**. The right correction is not to raise the count — it is to stop
treating a keyword-AND of 0 as evidence of an empty field. [Certain for all four counts and the
strings; **Likely** that the -ation form is the more faithful query]

### Carried, untouched

- **Gap numbering conflict.** `build_drug_repurposing_islet.py` header calls this intersection
  "**Gap #4**" and asserts **SILVER** ("11 independent papers… Shapiro, Alejandro, CITR…").
  `literature_gap_report.md` calls it **Gap #3, BRONZE**. `gap_numbering_audit.json` exists in
  `Results/` and was not consulted by any recent report. Two identifiers and two evidence tiers for
  one finding, in artifacts that both ship. **New today.**
- **Five of the top twelve gaps pair a domain against Health Equity**, keyword-brittle. The
  circularity test flagged P1 on 09-01 is still unrun — **eleven days**. Note that
  `Analysis/Scripts/falsify_equity_gaps.py` exists and is exactly this test. It has never been run.
- Beta Cell Regen × Health Equity joint count re-verified with the script's strings today: **0**.
  Reproduces.

### A live counterexample to a "methodologically distinct" classification

`Islet Transplant × GWAS/Polygenic` is filed under *expected low overlap, 0 joint pubs, deprioritize*.
**PMID 42722448** (*JCEM*, 2026-09-11) is diabetes-related genetics predicting outcomes after islet
autotransplantation — that intersection, in a top endocrine journal, four days after the gap file
was generated. My own query at that intersection returns 2 for 2020+. The "methodologically
distinct" bucket is a judgement call made once by one analyst and never revisited; this is the
first evidence against any entry in it. [**Likely** — I have read the title and journal, not the
paper, and have not confirmed it matches the script's exact domain strings]

---

## 5. Breaking News

**Nothing in the 7-day window (09-05 → 09-12) changes hub priorities.** Five searches run. The
registry events in §2 are the week's real news and they did not surface in any news search — which
is itself the argument for the collector fix. [Likely — negative result; five queries is not
exhaustive]

- **Novo / CagriSema** — NDA submitted 2025-12-18 on REDEFINE-1/-2; **no PDUFA date publicly
  confirmed**; decision expected Q4 2026. REIMAGINE program data presented at ADA 2026. Four
  CagriSema-family registry records flipped to COMPLETED this week (§2). Not in the tracker.
  [Likely — secondary sources; no primary Novo IR page or fda.gov document fetched]
- **Zealand / petrelintide ZUPREME-2** — topline still guided H2 2026, **not released**. Registry
  status is now COMPLETED (09-09), which is new information the prior two reports missed.
  ZUPREME-1 calibration: −10.7% vs −1.7% at 42 weeks; vomiting 3% vs 6.2% placebo. [Likely]
- **Vertex zimislecel** — no filing announcement; submissions still guided 2026. Zero PubMed
  records in 30 days. FORWARD Phase 1/2 (NEJM, PMID 40544428, **12 patients, SILVER**) remains the
  whole evidence base. Watch stands.
- **Orforglipron / Foundayo** — approved 2026-04-01, chronic weight management only, **not** T2D.
  No T2D filing announcement. ATTAIN-2's glycemic data (09-11 report §2) is still the strongest
  public argument for one.
- **Mounjaro / tirzepatide CV indication** (2026-08-28) — still the most consequential recent FDA
  action in scope, still **not in the tracker**, **12 days** outstanding. Primary fda.gov source
  still not fetched. Search results today describe it as expected in H2 2026, which conflicts with
  the hub's own 08-28 logging of it as done; **unresolved, and worth one primary fetch.**
- **Insulin efsitora alfa** — FDA decision possible H2 2026; still not on the watch list.
- **Retatrutide** — 15 papers in 30 days, the highest of any tracked therapy. TRANSCEND-T2D-1
  Phase 3 reported June 2026. The hub tracks the molecule but has not logged the Phase 3.

---

## 6. Data Quality Defects — Current List

| # | Defect | Status | Age |
|---|--------|--------|----:|
| 1 | `clinical_trials_latest.json` is a 57-day-old duplicate of the 07-17 snapshot | Open | 57d |
| 2 | `has_results` constant `False` — `HasResults` never requested in `fields` | Open | 6d |
| 3 | Null `title` on PMID 42698931 | Open, 1 of 139 | 6d |
| 4 | Epigenetics + Drug Repurpose alert queries over-filtered | Open | 4d |
| 5 | `phase` uses two null encodings, `"NA"` and `"N/A"` | Open | — |
| 6 | Freshness gate queries D+0, which always reads 0 | **Confirmed a 2nd day; fix is one date offset** | 4d |
| 7 | Scheduled run precedes the daily registry batch | Open — same root cause as #6 | 4d |
| 8 | `LastUpdatePostDate` history is not reproducible | Rule holds; mechanism still unknown | 3d |
| 9 | Gap counts cited without recording the query string | **Resolved for Gap #3 today** (§4); open elsewhere | 3d |
| 10 | 41-day trial-snapshot hole (07-18→08-26) | Open | 3d |
| 11 | **Terminal statuses absent from collectors** — **re-scoped today: the hole is 234 records, not 34; 22 of 22 in the T2D Ph2–3 lane** | **Open, severity raised** | **11d** |
| 12 | retmax ceiling discards 85.9% of matching records | Open | 11d |
| 13 | Amylin class uncovered in `therapy_hits` and all 16 alert queries | **Severity raised: 4 trials in the class completed this week** | 2d |
| 14 | Findings are not carried forward between reports | **`open_findings.md` written today** — partially retired | 2d |
| 15 | No `estimand` field anywhere in the trial schema | Open | 1d |
| 16 | Dashboard builders repaired but never executed; `origin/main` frozen 145d | Open | 3d |
| 17 | **Watches are keyed on `ResultsFirstPostDate`, so they cannot fire on completion** — ZUPREME-2 missed for 3 days | **New today** | — |
| 18 | **Gap #3 / Gap #4 numbering and tier conflict across shipped artifacts** (BRONZE vs SILVER) | **New today** | — |

---

## 7. Recommended Actions

Ranked. ▲ = new or re-ranked today. The top four are together under two hours and retire five
defects.

1. ▲ **Add the terminal statuses to collector #5 — and drop the results requirement.**
   Two edits in `baseline_clinical_trials.py`:
   ```
   'AREA[Condition](diabetes)
      AND AREA[OverallStatus](COMPLETED OR TERMINATED OR SUSPENDED OR WITHDRAWN)
      AND AREA[LastUpdatePostDate]RANGE[2025-01-01, MAX]'
   ```
   The status clause alone recovers 34. Replacing `ResultsFirstPostDate` with
   `LastUpdatePostDate` as the recency anchor recovers the other 200. Without this, running the
   scripts re-buries a 1,023-patient Phase 3 head-to-head.

2. ▲ **Re-key the watch list on `OverallStatus`, not `ResultsFirstPostDate`.** Defect #17. A
   trial's completion is the early signal; results are the late one. Watch both; alert on the
   first. ZUPREME-2 proves the cost, and the CagriSema Phase 3s are the next instance queued up.

3. **Fix the freshness gate to query D−1.** One date offset. Two consecutive days of confirming
   evidence. Cheapest item in the hub.

4. ▲ **Log the week's registry events in the tracker.** Clear
   `.~lock.Diabetes_Research_Tracker.xlsx#` first. Backlog, oldest first: Mounjaro CV label
   (08-28), ATTAIN-2 + estimand (09-04), ladarixin **BRONZE** not SILVER (08-31), ZUPREME-2
   completion (09-09), CagriSema cluster `NCT06534411` / `NCT06323161` / `NCT06797869` (09-09/10),
   zenagamtide `NCT07797335` (09-01).

5. **Run the two dead scripts — after #1.**
   ```
   python Analysis/Scripts/baseline_clinical_trials.py
   python Analysis/Scripts/hub_monitor.py
   ```
   57 days stale; repairs `clinical_trials_latest.json`; restores NCT-ID diffing, without which
   §2's departure analysis has to be re-derived by hand every day.

6. ▲ **Run `falsify_equity_gaps.py`.** The circularity test has been P1 for eleven days and
   **the script already exists in `Analysis/Scripts/`**. Nobody has run the thing that is blocking
   five of the top twelve gaps.

7. ▲ **Reconcile Gap #3 vs Gap #4 and BRONZE vs SILVER.** Defect #18. `gap_numbering_audit.json`
   is already in `Results/` and has not been consulted. Two shipped artifacts assert different
   tiers for one finding; that cannot reach a preregistration.

8. **Read PMID 42720752 (PROTECT per-protocol) and 42607698 (ACHIEVE-J).** Both Level 1b, both
   tracked therapies, both unread. The queue is ten deep and grew by four today.

9. **Cover the amylin class** — add `petrelintide`, `cagrilintide`, `amycretin`, `CagriSema` to
   `KEY_THERAPY_TERMS` **and** add an alert query. 131 papers all-time, 11 in-window, four trials
   completed this week, an NDA under review. This is no longer a tidiness item.

10. **Add an `estimand` field to the trial schema.** Defect #15.

11. **Raise `retmax` and page the alert queries** — before re-running `baseline_pubmed_alerts.py`.

12. **Execute the repaired dashboard builders and push.** 145 days frozen; the live site still
    cites a registry cohort study as the IDF Diabetes Atlas.

13. **Pin the query string next to every gap count.** Gap #3 is done (§4); 434 pairs remain.

14. **Fix the two over-filtered alert queries** — drop the trailing AND-clause from `Diabetes
    Epigenetics` and `Diabetes Drug Repurpose`.

15. **Fix `has_results`** — add `HasResults` to `fields` *and* read `study.get("hasResults")`.

16. **Move the scheduled run past the daily registry batch.** Same root cause as #3.

17. **Fetch one primary fda.gov source.** The Mounjaro CV label is recorded as done (08-28) and
    described by today's search results as pending. Four days of reports have flagged "no primary
    source fetched"; this is the specific case where it now matters.

18. **Read the blind-spot records** — starting with `NCT06534411`, the CagriSema/tirzepatide
    head-to-head. One of 34 has been read; the population is really 234.

19. **Replace consecutive-day diffing with a persistent seen-set** keyed on `overall_status`,
    `results_posted` and `last_update_posted`.

20. **Retire the "34 invisible records" figure** from circulation in favour of the 234/22 framing.

21. **Add insulin efsitora alfa to the FDA watch list.** Standing.

22. **Track `NCT06239636` by NCT ID** (Carlsson/Uppsala) — sponsor-string watches miss
    investigator-sponsored work structurally.

23. **Look at `NCT07808385`** (Mayo, DEKA TWIIST + Tidepool Loop in pregnancy with T1D) — thin
    literature, adjacent to two Tier 1 lanes.

24. **Delete the 09-07 test residue** — 4 files, 5 days, zero value.

25. **Refresh `CONTRIBUTION_STRATEGY.md`** — 181 days.

26. **Fix the sandbox mount.** Five consecutive failed runs. Browser-driven API reads sustain
    review but cannot write snapshots, so the collection hole widens every day and §2's departure
    analysis has to be hand-derived.

> **Note on item 14 of yesterday's defect list.** `open_findings.md` was prescribed on 09-10 and
> again on 09-11 and did not exist at the start of this run. It exists now:
> `Analysis/Results/open_findings.md`. Writing a new file is not modifying a hub file, so it is
> inside the review-run rule. It is the only prescription in this list that could be executed
> without Python, and leaving it unwritten for a third day while adding two more defects would
> have been the same failure the item describes.

---

## 8. Self-Audit

- **The ZUPREME-2 miss was available to both prior reports and I only found it because I diffed
  against the snapshot instead of re-reading the live record.** The 09-11 report reported
  `NCT06926842` as "COMPLETED, `hasResults` false, unchanged for 48 hours" — every word true, and
  the comparison was against yesterday's live read rather than against the hub's own stored state.
  The finding was one grep away for three days. **The lesson is not "check harder," it is that a
  watch defined on the wrong field cannot fire no matter how often it is checked.**

- **The 234-record figure is a count, not a reading, and I want to be precise about what it
  claims.** It is the number of diabetes trials with a 2026 completion date, status `COMPLETED`,
  and no results posted since 2025 — i.e. matched by none of the five collector queries. It does
  **not** claim 234 interesting trials. Most will be small and unremarkable. The claim is
  structural: the hub has no query that can see any of them, including the ones that matter.

- **I did not verify that all five collectors miss each of the 234 individually.** I verified the
  query logic (queries 1–4 require active statuses; query 5 requires `COMPLETED` **and** a results
  date) and spot-checked three named records against the 09-06 snapshot by grep. That is
  demonstration, not enumeration.

- **On Gap #3 I resolved a conflict and then undercut my own resolution, in that order.** The
  script's answer is 0 and that is now reproducible. But my alternative query returns 2, which
  means the 0 is partly an artifact of the `"islet transplant"` phrasing. Reporting only the
  resolution would have been cleaner and would have overstated what the hub knows.

- **The `Islet Transplant × GWAS` counterexample is [Likely], not [Certain].** I read a title and a
  journal, not a paper, and I did not confirm PMID 42722448 matches the script's exact domain
  strings — "total pancreatectomy with islet autotransplantation" may not match
  `"islet transplant" OR "islet cell transplant"` at all, which would make it a counterexample to
  the *classification* but not to the *count*. That distinction is not resolved.

- **The Mounjaro CV item is now internally contradictory in the hub's own record** — logged as done
  on 08-28, described as pending by today's search. I did not resolve it, and I have flagged it
  rather than picked a side. As with the last four reports: **no primary web source was fetched
  this run.** FDA, Novo and Zealand claims all rest on search summaries. This is the weakest
  evidence in the report and it has been the weakest evidence for five days running.

- **Three of the four "departures" required a grep to classify, and I only grepped eight IDs.**
  The method in §2 finds candidates; the snapshot cross-check is what separates a real departure
  from a trial that was already terminal. If I had skipped the grep I would have reported four T2D
  departures instead of two. The method is sound and it is not automatic.

- **This report has 26 action items, one more than yesterday.** That is a symptom, not a plan.
  Items 1–4 take under two hours and retire defects #6, #11, #13, #17 and most of the tracker
  backlog. If exactly one thing happens before the next run, it should be item 1.

---

## Evidence & Provenance

| Claim | Basis | Level |
|-------|-------|-------|
| `NCT06926842` = `ACTIVE_NOT_RECRUITING` in the 09-06 snapshot | Grep of `clinical_trials_snapshot_2026-09-06.json`, line 4031 | **Certain** |
| `NCT06926842` = `COMPLETED`, last update 2026-09-09, `hasResults` false | CT.gov API v2, full record read today | **Certain** |
| 246 diabetes trials `COMPLETED` with 2026 completion date; 12 with results → 234 invisible | 2 `countTotal` reads: `AREA[Condition](diabetes) AND AREA[OverallStatus](COMPLETED) AND AREA[CompletionDate]RANGE[2026-01-01,MAX]` ± `AND AREA[ResultsFirstPostDate]RANGE[2025-01-01,MAX]` | **Certain** |
| T2D Ph2–3 first-posted ≥2023, completed 2026: 22; with results 0 | Same pattern, 2 reads | **Certain** |
| All five collectors miss `COMPLETED` + no-results records | Read of `baseline_clinical_trials.py` QUERIES lines 31–52 | **Certain** |
| `NCT06534411` Ph3 n=1,023 CagriSema vs tirzepatide, COMPLETED, `hasResults` false, absent from 09-06 snapshot | Full record read + grep (0 matches) | **Certain** |
| `NCT06323161`, `NCT06797869` identity and status | Full records read today | **Certain** |
| `LastUpdatePostDate` 09-12 → 0; 09-11 → 1,165; diabetes slice 09-11 → 24 | 4 `countTotal` reads | **Certain** |
| Buckets 09-04/09-08/09-09/09-10 = 799 / 979 / 1,165 / 1,104 | 4 `countTotal` reads today | **Certain** |
| Prior-day bucket readings (842/826, 1,033/998, 1,297/1,189, 1,221) | `monitor_report_2026-09-10.md`, `_09-11.md`, read directly | Inherited — not re-verifiable |
| Category counts 158 / 77 / 151 / 244 / 344 | 5 `filter.advanced` queries replicating the script verbatim | **Certain** |
| 09-06 snapshot category counts 156 / 77 / 152 / 245 / 343 | `metadata.category_counts`, read directly | **Certain** |
| Departure candidates and their statuses | 3 `filter.advanced` queries with terminal statuses + `LastUpdatePostDate`RANGE[2026-09-06,2026-09-12]; 8-ID grep of the 09-06 snapshot | **Certain** |
| 8 new registrations since 09-01 with dates, sponsors, n | 3 `filter.advanced` queries, full rows read | **Certain** |
| Results window since 09-04 = 2 records | `AREA[Condition](diabetes) AND AREA[ResultsFirstPostDate]RANGE[2026-09-04,MAX]` | **Certain** |
| Blind spot 378 − 344 = 34; T1D 89 − 80 = 9 | 4 `countTotal` reads | **Certain** |
| 1,071 new `diabetes` PubMed records 09-06→09-12; 208 on 09-11→09-12 | E-utilities `esearch`, `datetype=edat` | **Certain** |
| Therapy 30-day counts: retatrutide 15, amylin 11, orforglipron 6, teplizumab 6, cagrilintide 6, ladarixin 1, zimislecel 0 | 7 `esearch` calls, `reldate=30` | **Certain** |
| `cagrisema OR cagrilintide` = 131 all-time; `petrelintide` = 6 all-time | 2 `esearch` calls | **Certain** |
| None of the 16 alert domains covers the amylin class | Full read of the query dictionary, inherited from 09-11 | **Certain** by inheritance |
| PMIDs 42720752, 42722448, 42712437, 42608559, 42706941, 42711287 — titles, journals, dates | `esearch` + `esummary` | **Certain** |
| Gap #3 script strings (lines 90, 104 of `gap_analysis_daily.py`) | Grep of the script | **Certain** |
| Gap #3 joint = 0 (2020+ and all-time); domains 253 / 621 reproduce | 5 `esearch` calls with the script's verbatim strings | **Certain** |
| Gap #3 = 2 all-time under `"islet transplantation"` | 1 `esearch` call | **Certain** |
| Conflicting counts 7 / 1 / 2 | `literature_gap_report.md` + prior reports, read directly | **Certain** (that the conflict exists) |
| Gap #3/#4 and BRONZE/SILVER conflict | `build_drug_repurposing_islet.py` header lines 4–6 vs `literature_gap_report.md` | **Certain** |
| `falsify_equity_gaps.py` exists and implements the circularity test | Grep of `Analysis/Scripts/` | **Certain** for existence; **Likely** that it is the right test |
| PMID 42722448 is a counterexample to the Islet Transplant × GWAS classification | Title + journal only; domain-string match unconfirmed | **Likely** |
| CagriSema NDA submitted 2025-12-18, no public PDUFA, decision expected Q4 2026 | Web search, secondary sources | **Likely** — no primary IR or fda.gov fetch |
| ZUPREME-2 topline guided H2 2026, unreleased | Web search: Zealand pipeline page + H1-2026 release | **Likely** |
| No significant breaking news in 7d | Web search, 5 queries, negative result | **Likely** |
| File ages and residue | Directory listing + internal `generated` fields; OS mtimes unreadable | **Certain** where the field exists |

No snapshot was written this run — no Python executed, and review runs do not modify hub files.

**Sources.** ClinicalTrials.gov API v2 (`https://clinicaltrials.gov/api/v2/studies`) — 28 live
queries. PubMed E-utilities `esearch`/`esummary`
(`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`) — 24 queries. Web search — 5 queries
(diabetes Phase 3 2026, FDA diabetes approvals Sept 2026, CagriSema completion, CagriSema PDUFA,
ZUPREME-2 topline). Local: `monitor_report_2026-09-11.md`, `hub_monitor_report.md`,
`clinical_trials_snapshot_2026-09-06.json`, `pubmed_recent_latest.json`,
`literature_gap_report.md`, `baseline_clinical_trials.py`, `gap_analysis_daily.py`,
`build_drug_repurposing_islet.py`, `falsify_equity_gaps.py`, directory listings.

*Generated by the Diabetes Research Hub automated monitor — 2026-09-12*
