# Diabetes Research Hub — Monitor Report

**Run date:** 2026-09-10 (automated)
**Prior report:** monitor_report_2026-09-09.md
**Mode:** Review run. No existing hub files modified.
**Environment note:** The Linux sandbox failed to mount again (3rd consecutive attempt, same
Plan9 error). No Python executed. All registry and PubMed figures below are live API reads;
all file facts come from reading the files. OS mtimes remain unreadable — file ages use each
file's internal `generated` field.

---

## Headline

**Nothing ran, nothing changed, and the registry was closed. The finding is in the reports, not the data.**

Zero hub files were written in the last 24 hours. Yesterday's #1 action — run the two dead
scripts — was not executed. The registry published nothing today. Category counts are identical
to yesterday's to the record. On the surface this is the emptiest run in the series.

Underneath it is not. Re-deriving the "recently posted results" list from scratch instead of
inheriting it produced **7 records, not the 4 yesterday reported.**

```
  Diabetes trials, ResultsFirstPostDate >= 2026-08-26
  ───────────────────────────────────────────────────
  09-09 report                 4
  today, same date window      7      +3
```

The three missing records are all `TERMINATED`. One of them is **NCT04628481 — ladarixin in
recent-onset T1D, stopped for futility, n = 289, results posted 2026-08-31** — a null Phase 2
readout in β-cell preservation, the hub's Tier 1 lane.

**The hub already found it.** `monitor_report_2026-09-01.md` reads the full results section,
tabulates the primary endpoint, states the blind spot in plain language — *"A trial that stops
early and posts its data is structurally invisible to this hub"* — sizes it at 32 records, and
files a P2 to log it in the tracker.

Nine days later the tracker is unchanged and the 09-09 results table has silently reverted to
the COMPLETED-only view that cannot see it.

This is a different failure class from a stale file. A stale file announces itself. **A finding
that was made, written down, and then dropped out of the next report leaves no trace at all** —
the 09-09 report's "4" looks exactly like a correct answer. The hub's real risk is not that it
misses events; it is that it forgets the ones it caught. [Certain — both report texts read
directly; both counts re-queried today.]

---

## 1. File System Status

| File | Internal `generated` | Age | Δ vs 09-09 |
|------|----------------------|-----|-----------|
| `literature_gap_data.json` | 2026-09-08 03:17:27 | 2d | — |
| `literature_gap_report.md` | 2026-09-08 03:17 | 2d | — |
| `pubmed_recent_latest.json` | 2026-09-06 09:18:08 | 4d | — |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 02:38:16 | 4d | — |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 | 10d | — |
| `clinical_trials_latest.json` | 2026-07-17 02:05:53 | **55d** | **still a broken pointer** |
| `hub_monitor_report.md` | 2026-07-17 02:16:51 | **55d** | still stale |
| `hub_monitor_state.json` / `clinical_trials_summary.md` | 2026-07-17 | **55d** | still stale |
| `Diabetes_Research_Tracker.xlsx` | — | **55d** | **still lock-held** |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 | 179d | — |

**No file in `Analysis/Results/` carries a 2026-09-10 date.** Newest artifact of any kind is
`monitor_report_2026-09-09.md`. The scripts did not run.

`.~lock.Diabetes_Research_Tracker.xlsx#` is still present — the tracker is open in an editor
somewhere, or the lock is orphaned. Either way it blocks the tracker update that has now been
outstanding since 09-01.

**09-07 test residue: all four files still present**, unchanged for three days — `_wtest.txt`,
`.gap_checkpoint.json.__unlinktest`, `.gap_checkpoint.json.testbak`, root `.wtest`.

---

## 2. Clinical Trial Changes

### Freshness gate: **FAIL — do not diff**

| Query, run 2026-09-10 | Count |
|---|---:|
| `LastUpdatePostDate` = 2026-09-10 | **0** |
| `StudyFirstPostDate` = 2026-09-10 | **0** |

ClinicalTrials.gov has published nothing today as of this run. Per the rule established
yesterday, a zero on *today's* date means the source has not posted, not that the world is
quiet. **No same-day diff is attempted below.** The gate worked exactly as designed and this is
its first live catch. [Certain]

### The decay hypothesis, sharpened

Yesterday's headline was that `LastUpdatePostDate` day-counts decay retroactively. Today's
zero-publication day is a clean natural experiment on that claim:

```
  bucket        09-09 reading    09-10 reading    Δ
  ───────────────────────────────────────────────────
  Fri 09-04          842              842         0
  Tue 09-08        1,033            1,033         0
  Wed 09-09        1,297            1,297         0
```

Three buckets, 24 hours apart, byte-identical. **Decay is caused by subsequent update events,
not by elapsed time.** On a day the registry publishes nothing, history is stable. This does not
rescue the field — 09-04 still fell 983 → 842 across a publishing interval — but it narrows the
rule: *a historical bucket is reproducible only until the next publishing day touches it.* The
practical consequence is unchanged: never store a historical day-series from this field.
[Certain — same three queries, two consecutive days.]

### Category counts: unchanged, to the record

| Category | 09-09 | 09-10 | Δ |
|----------|------:|------:|---:|
| T1D Cure & Cell Therapy | 157 | 157 | 0 |
| T1D Immunotherapy & Prevention | 77 | 77 | 0 |
| T2D Novel Therapies (Ph 2–3) | 151 | 151 | 0 |
| Diabetes Technology (Devices) | 246 | 246 | 0 |
| Diabetes Recently Completed w/ Results | 344 | 344 | 0 |

Corpus **895 unique trials, unchanged**. Five live queries replicating
`baseline_clinical_trials.py` verbatim. [Certain]

### The blind spot, re-measured — and growing

The category-5 filter in the shipped script is:

```python
'AREA[Condition](diabetes) AND AREA[OverallStatus](COMPLETED)
 AND AREA[ResultsFirstPostDate]RANGE[2025-01-01, MAX]'
```

Drop the status clause and the same window returns more:

| Query | Count |
|---|---:|
| Diabetes, results posted since 2025-01-01, **any status** | **378** |
| …restricted to `COMPLETED` (what the hub collects) | 344 |
| **Structurally invisible to the hub** | **34 (9.0%)** |
| Same measurement on 2026-09-01 | 32 |

Two more records fell into the blind spot in nine days. Of these, **9 are Type 1 diabetes
trials** with posted results and a non-COMPLETED status. `TERMINATED`, `SUSPENDED` and
`WITHDRAWN` appear in none of the five category queries. [Certain — script text + 4 live
`countTotal` queries]

A terminated trial that posts results is not noise. It is the cheapest negative evidence in the
field: someone spent four years and 289 patients establishing that a mechanism does not work,
and the hub's collector is configured to skip it.

### NCT04628481 — ladarixin, re-verified today

| | |
|---|---|
| Sponsor | Dompé Farmaceutici S.p.A |
| Design | Phase 2, n = 289 enrolled; recent-onset T1D, low residual β-cell function |
| Status | **TERMINATED** — `whyStopped`: *"The study was stopped due to futility as per protocol"* |
| Completion | 2025-10-21 |
| Results first posted | **2026-08-31** |
| Last update posted | 2026-08-31 |

Endpoint values are in `monitor_report_2026-09-01.md` §NCT04628481 and are not restated here.
The reading stands: **null, not harmful** — the point estimate favours placebo, the interval
crosses zero, and the stop was pre-specified. CXCR1/2 blockade did not preserve β-cell function
in this population.

Evidence level per Doctrine: **SILVER at best** — registry-posted randomised Phase 2, not peer
reviewed. PubMed carries 33 ladarixin records all-time and **none in the last 30 days**; the
trial itself is still unpublished. Nobody has written it up. [Certain — CT.gov record read today
+ E-utilities]

### ZUPREME-2 watch: still open, now sharper

`NCT06926842` (petrelintide, Zealand/Roche) re-checked today: `overallStatus` **COMPLETED**,
`hasResults` **false**, last update 2026-09-09. Zealand's H2-2026 topline guidance is
unchanged and no readout has been announced. The watch set yesterday is correctly placed and
has not fired. [Certain for registry state; **Likely** for readout timing — company guidance]

Incidental confirmation of yesterday's §3: requesting `HasResults` in `fields` returns the flag
correctly on every record queried today. The fix is exactly the one specified.

---

## 3. PubMed Highlights

Corpus unchanged since 2026-09-06: **139 papers, 16 alert domains, 30-day lookback**. (Task spec
says 15 domains; the script defines 16. Third report to note this.)

### The retmax ceiling, quantified from the file itself

`pubmed_recent_latest.json` metadata: `domain_retmax: 10`, `therapy_retmax: 5`. Summing the
domain block:

```
  matching records available (Σ total_count, 16 domains)     943
  records actually retrieved (Σ paper_count)                 133
  ─────────────────────────────────────────────────────────────
  discarded by the ceiling                                   810   (85.9%)

  therapy block: 82 available → 31 retrieved                       (62.2% discarded)
```

The 09-01 report estimated ~85% from replication experiments. **The number is recoverable by
arithmetic from the shipped output file** — no experiment needed, and it has been sitting in the
metadata block since 09-06. [Certain — arithmetic on the file]

Two domains are ceiling-free because they are broken the other way: `Diabetes Drug Repurpose`
(total_count **1**) and `Diabetes Epigenetics` (total_count **1**) — the over-filter defect
diagnosed on 09-08/09-09, still unfixed, now visible in the corpus metadata as well.

### petrelintide is not a tracked therapy

The eight `therapy_hits` terms are: zimislecel, orforglipron, retatrutide, CagriSema,
baricitinib, teplizumab, icodec, dapagliflozin.

The hub's highest-probability near-term readout is an amylin analog that is not on that list.
Consequence, measured today: **PMID 42586227** — *"Beyond GLP-1: Amylin-based pharmacotherapy
and the search for better-tolerated weight-loss drugs"*, *Pharmacol Res* 232:108382, Entrez
2026-08-12 — is **absent from `pubmed_recent_latest.json`** despite falling inside the corpus's
own 30-day window.

**And the cause is not the retmax ceiling.** The obvious hypothesis was that `T2D GLP-1 New`
(188 available → 10 kept) matched it and truncated it. Tested directly:

```
  esearch: ("GLP-1" OR semaglutide OR tirzepatide OR retatrutide OR orforglipron)
           AND "type 2 diabetes" AND (trial OR results)
           AND 42586227[uid]
  → count: 0
```

It never matched. Reading all 16 alert query strings: **none contains `amylin`,
`cagrilintide`, `petrelintide`, `obesity` or `weight loss`.** This is a *coverage* gap, not a
sampling gap — raising `retmax` would not have retrieved this paper, and will not retrieve the
ZUPREME-2 publication when it appears. Two different fixes are needed, and #8 below does not
substitute for #10. [Certain — direct `esearch` test + full read of the query dictionary]

One term-expansion artifact worth knowing about: PubMed maps `ladarixin` onto a supplementary
concept, and the query surfaced **PMID 42594352** (*Int J Radiat Biol*, CXCL-mediated oxidative
DNA damage → Th2 responses) — mechanistically adjacent, not a diabetes paper. Do not let a
naive `ladarixin` alert land it in the corpus as a hit.

### Staleness: still low urgency

`diabetes` (all), Entrez-dated 2026-09-06 → 2026-09-10: **674** new records. Large in absolute
terms, but the same pattern as yesterday — volume is concentrated outside the two high-value T1D
domains. Re-running `baseline_pubmed_alerts.py` remains lower priority than fixing the two
over-filtered queries and the retmax ceiling, because re-running it *unfixed* re-imports the
same 86% loss. [Certain for the count]

### Reading queue — unchanged, still unread

1. **PMID 42694848** — COL1A2/APOLD1 dual-axis, diabetic nephropathy–retinopathy comorbidity.
   Only 4-domain paper on record. Flagged 09-06. **Unread for 4 days.**
2. **PMID 42627334** — β-cell function 1 yr after stopping oral baricitinib (*Diabetes Care*).
3. **PMID 42626948** — gene-edited hypoimmune islets.
4. **PMID 42673585** — GLP-1 RAs / co-agonists for weight loss without diabetes (*Ann Intern Med*).
5. **PMID 42586227** — amylin pharmacotherapy review (**new today**; promote — it is the
   background reading for the ZUPREME-2 watch).

Cross-domain count inherited from yesterday's independent recount: **20 of 139**. Corpus
unchanged, so no recount performed. [Certain by inheritance — file byte-identical]

---

## 4. Gap Analysis Summary

Unchanged since 2026-09-08 03:17. 30 domains, 435 pairs. Validation **BRONZE**.

| # | Intersection | Gap | Joint pubs | Doctrine Tier 1 alignment |
|---|--------------|----:|-----------:|---------------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | §6 Epidemiological (17/20) |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | §2 Literature Synthesis (19/20) |
| 3 | **Islet Transplant × Drug Repurposing** | 100.0 | 0 | **§4 Drug Repurposing (18/20)** |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | §6 (17/20) |
| 5 | Gene Therapy × LADA | 100.0 | 0 | §2 (19/20) |

Two open defects carried, neither touched:

- **Gap #3 carries three incompatible counts** across hub artifacts — 7 (`literature_gap_report.md`
  rationale text), 1 (09-08 report), 2 (09-09 re-query). Three different query strings, none
  recorded. This is the hub's lead contribution candidate and it cannot currently reproduce its
  own headline number. [Certain]
- **Five of the top twelve gaps pair a domain against Health Equity**, a keyword-brittle concept.
  The circularity test flagged as P1 on 09-01 is still unrun — **nine days**.

Note the interaction with §3: `Diabetes Drug Repurpose` returns `total_count: 1` in the alert
corpus because of the over-filter. The hub's top drug-repurposing *gap* and its broken
drug-repurposing *alert* are the same blind spot seen from two directions.

---

## 5. Breaking News

**Nothing in the 7-day window (09-03 → 09-10) changes hub priorities.** Three searches run;
every substantive hit predates the window and is already recorded. [Likely — negative result;
absence of news is weaker evidence than presence]

- **Zealand / petrelintide ZUPREME-2** — topline still guided H2 2026, **not released**.
  Confirms the registry-COMPLETED flip on 09-09 genuinely leads the press here.
- **Mounjaro / tirzepatide CV indication expansion** (2026-08-28) — still the most consequential
  recent FDA action in scope, still **not in the tracker**. Outstanding since 08-31. [Likely —
  fda.gov primary source still not fetched]
- **Insulin efsitora alfa** — possible FDA decision H2 2026; still not on the hub's watch list.
- **Vertex zimislecel** — 2026 submissions still guided, no filing announcement. Watch stands.

---

## 6. Data Quality Defects — Current List

| # | Defect | Status | Age |
|---|--------|--------|----:|
| 1 | `clinical_trials_latest.json` is a 55-day-old duplicate of the 07-17 snapshot | Open | 55d |
| 2 | `has_results` constant `False` — `HasResults` never requested in `fields` | Diagnosed; fix re-confirmed live today | 2d |
| 3 | Null `title` on PMID 42698931 in `pubmed_recent_latest.json` | Open, 1 of 139 | 4d |
| 4 | Epigenetics + Drug Repurpose alert queries over-filtered | Diagnosed; two-line edit pending | 2d |
| 5 | `phase` uses two null encodings, `"NA"` and `"N/A"` | Open | — |
| 6 | No source-freshness gate in the shipped scripts | Open — gate run manually today, **caught a real FAIL** | 2d |
| 7 | Scheduled run time precedes the daily registry batch | Open | 2d |
| 8 | `LastUpdatePostDate` history is not reproducible | **Narrowed today** — decay is event-driven, not time-driven (§2) | 1d |
| 9 | Gap artifacts cite counts without recording the query string | Open | 1d |
| 10 | 41-day trial-snapshot hole (07-18→08-26); collection ~weekly | Open | 1d |
| 11 | **`TERMINATED`/`SUSPENDED`/`WITHDRAWN` absent from all five collectors — 34 records invisible, 9 of them T1D** | **Re-opened today; first raised 09-01, unfixed** | **9d** |
| 12 | **retmax ceiling discards 85.9% of matching records — computable from the shipped metadata** | **Quantified today from the file** | 9d |
| 13 | **The amylin class is uncovered — absent from `therapy_hits` *and* from all 16 alert queries — while being the top near-term watch item** | **New today** | — |
| 14 | **Findings are not carried forward between reports** (§Headline) | **New today — meta-defect** | — |

---

## 7. Recommended Actions

Ranked. ▲ = new or re-ranked today.

1. ▲ **Add the terminated statuses to the collector.** One clause, in
   `baseline_clinical_trials.py` query #5:
   ```
   AREA[OverallStatus](COMPLETED OR TERMINATED OR SUSPENDED OR WITHDRAWN)
   ```
   Promoted over "run the scripts" because running them **unmodified** re-collects the same
   34-record blind spot and re-buries ladarixin. Fix first, then run. 9 days open.

2. **Run the two dead scripts** — after #1.
   ```
   python Analysis/Scripts/baseline_clinical_trials.py
   python Analysis/Scripts/hub_monitor.py
   ```
   55 days stale; also repairs `clinical_trials_latest.json`.

3. ▲ **Log NCT04628481 in the tracker as a null Phase 2 T1D β-cell-preservation result**,
   SILVER. Outstanding since 09-01. Clear `.~lock.Diabetes_Research_Tracker.xlsx#` first. This
   is the single cheapest item in the hub and it has survived nine reports.

4. ▲ **Carry an explicit open-findings ledger between reports.** The defect table above is
   already one; the *findings* have no equivalent, which is how ladarixin was dropped. A
   `open_findings.md` with one line per unresolved item, re-emitted verbatim each run, costs
   nothing and would have made yesterday's "4" impossible to print.

5. **Ship the freshness gate into the scripts** — `LastUpdatePostDate` = today only. It caught a
   genuine FAIL this morning; it should not depend on a human running it by hand.

6. **Move the scheduled run past the daily registry batch** — 03:40 ET reads a registry that has
   not published. Today's run would have returned useful data four hours later.

7. **Fix `has_results`** — add `HasResults` to `fields` *and* read `study.get("hasResults")`.
   Verified working live today.

8. **Raise `retmax` and page the alert queries.** 85.9% of matching records are being discarded
   before any analysis sees them (§3). Do this *before* re-running `baseline_pubmed_alerts.py`,
   for the same reason as #1.

9. **Fix the two over-filtered alert queries** — delete the trailing AND-clause from both
   `Diabetes Epigenetics` and `Diabetes Drug Repurpose`.

10. ▲ **Cover the amylin class in *both* places.** Add `petrelintide`, `cagrilintide`,
    `amycretin` to `KEY_THERAPY_TERMS`, **and** add an alert query — e.g.
    `(amylin OR petrelintide OR cagrilintide OR amycretin) AND (obesity OR "type 2 diabetes")`.
    Terms alone are not enough: the domain queries are what build the cross-domain graph, and
    none of the 16 can see this class (§3). Independent of #8. Start with **PMID 42586227**.

11. **Keep the NCT06926842 watch on `ResultsFirstPostDate`.** Registry-COMPLETED, results false,
    guidance H2 2026 — verified today.

12. ▲ **Read the other 33 blind-spot records.** The 09-01 self-audit was right that 32 was a
    count, not a reading. One has been read. It was worth reading.

13. **Pin the query string next to every gap count.** Gap #3 carries 7 / 1 / 2 across three
    artifacts. Resolve before it reaches a preregistration.

14. **Run the Health Equity circularity test.** P1 since 09-01, unrun for 9 days; it undermines
    5 of the top 12 gaps.

15. **Read PMID 42694848**, then 42627334.

16. **Log the Mounjaro CV indication expansion**, linked to NCT04255433. Confirm on fda.gov.

17. **Replace consecutive-day diffing with a persistent seen-set** keyed on `results_posted` and
    `last_update_posted`.

18. **Add insulin efsitora alfa to the FDA watch list.**

19. **Track NCT06239636 by NCT ID** (Carlsson/Uppsala) — sponsor-string watches miss
    investigator-sponsored work structurally.

20. **Add `zenagamtide`** (NCT07797335, Novo, PHASE3).

21. **Delete the 09-07 test residue** — 4 files, 3 days old, zero value.

22. **Refresh `CONTRIBUTION_STRATEGY.md`** — 179 days, predates the 08-31 doctrine.

23. **Fix the sandbox mount.** Three consecutive failed runs. Every report since 09-08 has been
    produced by hand-querying APIs through a browser; that works for review but cannot write
    snapshots, so the collection hole keeps widening.

---

## 8. Self-Audit

- **This report found no new science.** The registry was closed and the corpus did not move.
  Everything above is either a re-measurement or a defect. That is the honest characterisation.
- **The ladarixin "rediscovery" is not a discovery.** The 09-01 run did the hard work — read
  the results section, tabulated the endpoint, sized the blind spot. Today's contribution is
  noticing it fell out and that the blind spot grew 32 → 34. Credit belongs to 09-01.
- **"34 invisible records" is a count, not a reading.** One of the 34 has been read. The other
  33 may be enrolment failures with nothing in them. The defensible claim is that the hub cannot
  see them.
- **The 85.9% figure is arithmetic on `total_count` vs `paper_count`.** It assumes those fields
  mean what they appear to mean. It agrees with the 09-01 replication estimate (~85%) derived by
  a different method, which is why it is rated Certain rather than Likely.
- **The decay narrowing rests on one quiet day.** One zero-publication day is a clean test but
  it is n = 1. If a second quiet day also shows byte-identical buckets, the event-driven reading
  is confirmed.
- **I got the amylin diagnosis wrong on the first pass and the test caught it.** The draft
  attributed PMID 42586227's absence to the retmax ceiling, rated [Likely]. One `esearch`
  against the verbatim query string returned 0 — it was never matched at all. Coverage, not
  sampling. This is what the 09-01 self-audit meant: the value is not that the error was caught,
  it is that a monitor without an adversarial pass ships it.
- **No web primary source was fetched.** FDA and Zealand claims rest on search summaries.
  Unchanged from yesterday, and still the weakest evidence in the report.

---

## Evidence & Provenance

| Claim | Basis | Level |
|-------|-------|-------|
| Registry published nothing 2026-09-10 | CT.gov API v2, `LastUpdatePostDate` and `StudyFirstPostDate` = 0 for today | **Certain** |
| 09-04 / 09-08 / 09-09 buckets byte-identical across 24h | Same three queries, 09-09 and 09-10 | **Certain** |
| Category counts 157/77/151/246/344 unchanged; corpus 895 | 5 `filter.advanced` queries replicating the script verbatim | **Certain** |
| Results-window returns 7, not 4 | `AREA[Condition](diabetes) AND AREA[ResultsFirstPostDate]RANGE[2026-08-26, MAX]`, `countTotal` | **Certain** |
| Blind spot = 34 (378 any-status − 344 COMPLETED); 9 are T1D | 4 live `countTotal` queries + script text | **Certain** |
| Blind spot was 32 on 09-01 | `monitor_report_2026-09-01.md`, read directly | **Certain** |
| Ladarixin TERMINATED for futility, n=289, results 2026-08-31 | CT.gov full record incl. `whyStopped`, read today | **Certain** |
| Ladarixin result is null, not harmful | Endpoint table in `monitor_report_2026-09-01.md` | **SILVER** (registry-posted RCT, unpublished) |
| Ladarixin: 33 PubMed records all-time, 0 in 30d | E-utilities `esearch` | **Certain** |
| NCT06926842 COMPLETED, `hasResults` false, updated 09-09 | CT.gov record read today | **Certain** |
| ZUPREME-2 topline not yet released, guided H2 2026 | Web search, company guidance; primary IR page not fetched | **Likely** |
| retmax discards 85.9% (943 → 133) | Arithmetic on `pubmed_recent_latest.json` metadata + domain block | **Certain** |
| petrelintide absent from `therapy_hits` | Direct read of the 8 tracked terms | **Certain** |
| PMID 42586227 in-window and absent from corpus | `esearch` Entrez date 2026-08-12 + grep of the corpus file | **Certain** |
| …absent because **no alert query covers the amylin class**, not because of retmax | `esearch` of the verbatim `T2D GLP-1 New` string AND `42586227[uid]` → 0; full read of all 16 query strings | **Certain** |
| PMID 42594352 is a term-expansion artifact | `esearch` `querytranslation` shows supplementary-concept mapping | **Certain** |
| 674 new `diabetes` records 09-06 → 09-10 | E-utilities `esearch`, `datetype=edat` | **Certain** |
| No hub file written 2026-09-10; residue still present | Directory listing + internal `generated` fields | **Certain** |
| Three conflicting gap-#3 counts | Direct read of all three artifacts | **Certain** |
| No significant breaking news in 7d | Web search, 3 queries, negative result | **Likely** |
| Gap classifications | Inherited from `literature_gap_report.md` | **BRONZE** |
| File ages | Internal `generated` fields; OS mtimes unreadable (sandbox down) | Certain where the field exists; unknown for `.xlsx` and `CONTRIBUTION_STRATEGY.md` |

No snapshot was written this run — no Python executed, and review runs do not modify hub files.

**Sources:** ClinicalTrials.gov API v2 (`https://clinicaltrials.gov/api/v2/studies`) — 14 live
queries. PubMed E-utilities `esearch`/`esummary` (`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`)
— 5 queries. Local: `monitor_report_2026-09-09.md`, `monitor_report_2026-09-01.md`,
`pubmed_recent_latest.json`, `literature_gap_report.md`, `hub_monitor_report.md`,
`baseline_clinical_trials.py`, `RESEARCH_DOCTRINE.md`.

*Generated by the Diabetes Research Hub automated monitor — 2026-09-10*
