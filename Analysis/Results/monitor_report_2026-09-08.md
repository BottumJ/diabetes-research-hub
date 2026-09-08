# Diabetes Research Hub — Monitor Report

**Run date:** 2026-09-08 03:40 ET (automated, sandbox)
**Prior report:** monitor_report_2026-09-07.md
**Mode:** Review run. No existing hub files modified.

---

## Headline

**The last three monitor reports concluded "the registry did not move." That conclusion
was never testable. ClinicalTrials.gov has not published a batch since Friday 2026-09-04,
and this monitor runs at 03:40 ET — before each day's batch posts.**

Registry-wide, unfiltered by condition, counting every study in ClinicalTrials.gov:

```
        Thu 08-27  ████████████████ 831        new 199
        Fri 08-28  ███████████████████ 980     new 179
        Sat 08-29  ·  0                        new   0
        Sun 08-30  ·  0                        new   0
        Mon 08-31  █████████████████ 890       new 186
        Tue 09-01  ████████████████████ 1050   new 210
        Wed 09-02  ██████████████████ 973      new 165
        Thu 09-03  ███████████████████ 1001    new 202
        Fri 09-04  ██████████████████ 983      new 170   <- last published batch
        Sat 09-05  ·  0                        new   0
        Sun 09-06  ·  0                        new   0   <- 09-06 monitor run read this
        Mon 09-07  ·  0                        new   0   <- Labor Day; 09-07 run read this
        Tue 09-08  ·  0                        new   0   <- this run, 03:40 ET
                   records last-updated that day
```

Every one of those zeros is explained without any reference to diabetes research: two
weekends, one US federal holiday, and a run time that precedes the daily batch. **The
09-06 and 09-07 "zero delta" findings were structurally guaranteed by the schedule, not
observed in the data.** So was today's.

This supersedes yesterday's framing. Yesterday concluded that *consecutive-day diffing is
the wrong detector*. True, but downstream of the real problem: **the monitor has no
freshness gate on its source**, so a source that is not publishing is indistinguishable
from a source that is publishing nothing new. [Certain — see §7 for the query.]

Two claims in yesterday's report are corrected below (§6). One is the top-ranked
recommended action.

---

## 1. File System Status

| File | Last modified | Age | State |
|------|--------------|-----|-------|
| `pubmed_recent_latest.json` | 2026-09-06 09:18 | 2d | Current |
| `pubmed_recent_summary.md` | 2026-09-06 09:18 | 2d | Current |
| `literature_gap_data.json` | 2026-09-06 09:12 | 2d | Current |
| `literature_gap_report.md` | 2026-09-06 09:12 | 2d | Current |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 02:38 | 2d | Current (sandbox-acquired) |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 | 8d | Current |
| `agent_state.json` | 2026-09-07 03:28 | 1d | Current |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | **53d** | **STALE** |
| `clinical_trials_latest.json` | 2026-07-17 | **53d** | **BROKEN POINTER** |
| `clinical_trials_summary.md` | 2026-07-17 | **53d** | **STALE** |
| `hub_monitor_report.md` | 2026-07-17 | **53d** | **STALE** |
| `hub_monitor_state.json` | 2026-07-17 | **53d** | **STALE** |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 | **177d** | **STALE** |

Unchanged from yesterday except the day count. `clinical_trials_latest.json` still carries
`"generated": "2026-07-17T02:05:53"` and `total_trials: 858`; the 09-06 snapshot carries
894. Anything reading `_latest` is reading July and is 36 trials short.

Residue from the 09-07 run that could not be deleted (sandbox `/sessions` at capacity):
`Analysis/Results/_wtest.txt`, `.gap_checkpoint.json.__unlinktest`,
`.gap_checkpoint.json.testbak`, and root `.wtest`. All zero-value. Delete at your
convenience.

---

## 2. Clinical Trial Changes

### 09-06 → 09-08 (48h)

| Metric | Count |
|--------|-------|
| Total trials | 894 → 894 |
| New | 0 |
| Removed | 0 |
| Status changes | 0 |
| New results posted | 0 |

**Do not read this as a finding.** Per the headline, the source has published nothing
since 09-04. A fresh pull replicating all five `baseline_clinical_trials.py` filters
returns identical totals and identical category counts (156 / 77 / 152 / 245 / 343),
which is what a frozen source looks like.

The last real registry movement the hub has on record is still the 09-01 → 09-06 window:
8 new trials, 1 removed, 3 status changes. Carried forward unchanged —

- **NCT07797335** — Novo Nordisk, AMBITION 7, **zenagamtide**, PHASE3, RECRUITING (posted 09-01)
- **NCT07804849** — Ain Shams Univ., oral **verapamil**, newly diagnosed children/adolescents with T1D, PHASE2/3, RECRUITING (posted 09-04)
- **NCT07796477** — CSPC Ouyi, SYH2069, PHASE2, not yet recruiting
- **NCT07801820** — Shanghai Minwei, MWN109, PHASE2, recruiting
- **NCT07282639** NOT_YET_RECRUITING → RECRUITING; **NCT07228117** (Medtronic MiniMed NMX8-AID) and **NCT07076199** (Novo, insulin icodec PHASE3) RECRUITING → ACTIVE_NOT_RECRUITING

### 14-day same-window scan (`results_posted >= 2026-08-25`)

| Posted | NCT | Phase | Sponsor | Study |
|--------|-----|-------|---------|-------|
| 2026-09-04 | NCT05872620 | PHASE3 | Eli Lilly | Orforglipron in obesity/overweight **with T2D** (ATTAIN-2) |
| 2026-09-02 | NCT04828785 | NA | UNC Chapel Hill | Food As MedicinE for Diabetes |
| 2026-08-27 | NCT04506151 | NA | Univ. of Illinois Chicago | Sleep optimization for glycemic control in T1D |

Three, down from four, purely because the window slid past NCT05530356 (08-24). The
same-window scan still beats consecutive-day diffing 3–0, and that remains the correct
detector — but see §6 for what the ATTAIN-2 row is actually worth.

### Key-organization standing (unchanged)

| Org | Trials in corpus | Notable |
|-----|------------------|---------|
| Eli Lilly | 34 | 2 baricitinib T1D PHASE3 recruiting (NCT07222137, NCT07222332); retatrutide + orforglipron PHASE3 cluster |
| Novo Nordisk | 29 | CagriSema PHASE3 ×3; zenagamtide PHASE3; icodec program moved to ACTIVE_NOT_RECRUITING |
| Vertex | 3 | **VX-880 / zimislecel PHASE3 recruiting** (NCT06832410, NCT04786262); VX-264 PHASE1/2 active |
| Sana Biotechnology | 0 | Not a diabetes sponsor. Track **NCT06239636** (Carlsson/Uppsala) by NCT ID — see 09-07 §6 |

58 PHASE3 trials currently RECRUITING.

---

## 3. PubMed Highlights

Corpus: 139 unique papers, 30-day lookback, generated 2026-09-06 09:18. Not refreshed
since; 18 papers were new in the 09-05 → 09-06 step.

### Cross-domain papers (20 of 139)

Unchanged from yesterday. Reading priority, highest first:

1. **PMID 42694848** — *COL1A2 and APOLD1 Define a Dual-Axis Molecular Framework for
   Diabetic Nephropathy–Retinopathy Comorbidity* (Int J Med Sci). **Four domains** —
   AI/ML + Biomarker + Complications + Multi-Omics. The only 4-domain paper on record.
   Flagged 09-06, still unread. Hits Doctrine Tier 1 §1 (Multi-Omics, 19/20) and §5
   (AI/ML, 18/20) simultaneously; testable against GEO / Metabolomics Workbench.
2. **PMID 42627334** — β-cell function 1 year after **stopping** oral baricitinib in T1D
   (*Diabetes Care*). The durability question for the two Lilly PHASE3 baricitinib trials
   now recruiting. Highest journal quality in the corpus.
3. **PMID 42626948** — Gene-edited hypoimmune islets as a T1D cure (Expert Opin Biol Ther).
   Relevant to VX-264 and the UP421 / NCT06239636 line.
4. **PMID 42673585** — GLP-1 RAs and co-agonists for weight loss without diabetes
   (*Ann Intern Med*). Triple therapy hit: orforglipron + retatrutide + CagriSema.
5. **PMID 42694300** — Oral microbiome + metabolome in Alström / Bardet-Biedl
   (Comput Struct Biotechnol J). Biomarker + Microbiome + Multi-Omics.

### Key-therapy tracking (30-day counts, as of 09-06)

| Therapy | Hits |
|---------|------|
| dapagliflozin | 41 |
| retatrutide | 11 |
| icodec | 10 |
| orforglipron | 8 |
| teplizumab | 5 |
| CagriSema | 4 |
| baricitinib | 3 |
| **zimislecel** | **0** (INN has 3 lifetime records; literature indexes under **VX-880**, 6 records — fix is `VX-880 OR zimislecel`) |

### Two dead alert channels — now diagnosed [Certain]

Yesterday flagged Epigenetics (1/mo) and Drug Repurpose (1/mo) as implausible and rated it
[Likely] a query fault. I ran the decomposition. It is a query fault, and the failing
clause is identified.

Counts from E-utilities, 2026-09-08, same date-window logic as `baseline_pubmed_alerts.py`:

| Query | 30d | 90d | 365d |
|-------|----:|----:|-----:|
| **Epigenetics as coded** — `diabetes AND (epigenetic OR methylation) AND (GWAS OR "genome-wide")` | **1** | 13 | 94 |
| Epigenetics, third clause removed | **126** | 401 | 1569 |
| Epigenetics, third clause widened to include `EWAS OR "epigenome-wide"` | 3 | 18 | 113 |
| **Drug Repurpose as coded** — `... AND (computational OR network OR screening)` | **1** | 17 | 65 |
| Drug Repurpose, third clause removed | **6** | 33 | 146 |

**Epigenetics loses 126× of its recall to the `AND (GWAS OR "genome-wide")` clause.**
Widening that clause to include EWAS terms recovers almost nothing (1 → 3), which rules
out "wrong genomics keyword" and establishes the real cause: diabetes epigenetics
literature is overwhelmingly *not* framed as genome-wide association work. The clause
does not narrow the domain — it deletes it.

Drug Repurpose loses 6×. Smaller in absolute terms because the domain is genuinely small
(146/yr unrestricted), but it is still returning 17% of available volume.

Both numbers match the predictions made from the gap-analysis baselines yesterday
(~100/mo epigenetics, ~8/mo repurposing) almost exactly, which is independent corroboration
that the unrestricted counts are the right reference. **This closes 09-07 recommended
action #7.** The fix is to delete the third AND-clause from both queries.

---

## 4. Gap Analysis Summary

Generated 2026-09-06. 30 domains, 435 pairs, 870 pair counts. Validation level **BRONZE**
per Doctrine — single analytical source, expert confirmation outstanding. Unchanged.

### Top 5 by gap score, restricted to "potentially meaningful"

| # | Intersection | Gap | Joint pubs | Tier 1 alignment |
|---|--------------|-----|------------|------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | **§6 Epidemiological/Equity (17/20)** |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | §2 Literature Synthesis |
| 3 | **Islet Transplant × Drug Repurposing** | 100.0 | 0 | **§4 Drug Repurposing (18/20)** |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | **§6 (17/20)** |
| 5 | Gene Therapy × LADA | 100.0 | 0 | §2 |

**Gap #3 remains the strongest candidate** — verified 09-07 at exactly 1 all-time PubMed
record (PMID 27821710, 2016), sits on the highest-scoring Tier 1 area the hub can execute
unilaterally, all required resources open (DrugBank, OpenTargets, STRING, Reactome), no
incumbent.

**New caveat worth holding against it.** §3 just showed that the hub's own Drug Repurpose
*alert* query is over-filtered by 6×. The gap analysis uses a different, unrestricted
query string, so gap #3's count is not contaminated — but the pattern is a warning. Five of
the top twelve gaps pair a domain against Health Equity, a keyword-brittle concept.
Before committing to #1, #4, #7, #10 or #12, run each as a free-text PubMed query the way
#3 was run. That is a 10-minute check that separates real territory from vocabulary
mismatch, and §3 is evidence that this hub's query strings do fail this way.

Domain volume floor for reference: Islet Transplant 253 pubs since 2020, LADA 602,
Drug Repurposing 621, Personalized Nutr 693 — these are the small domains driving the
100.0 scores, and small denominators make gap scores fragile.

---

## 5. Breaking News

**Nothing that changes hub priorities this week.** Two sweeps run (Phase 3 readouts,
FDA actions). Confirmed background, none of it new in the last 7 days:

- **Mounjaro / tirzepatide CV indication expansion** — FDA approved expanded use to reduce
  heart attack and stroke risk in high-risk adults with T2D, **late August 2026**. This is
  the most consequential recent FDA action in the corpus's scope and it is **not recorded
  in the hub**. It connects directly to NCT04255433 (SURPASS-CVOT, results posted 07-08),
  which the hub already holds.
- Garzulys (insulin aspart-fsan, NovoLog biosimilar) approved 2026-07-30.
- Prior-2026, already in the record: retatrutide TRANSCEND-T2D-1 (Mar), TRIUMPH-2/3 (Jul),
  oral semaglutide 25 mg approval, first generic dapagliflozin, first generic liraglutide.
- **Vertex zimislecel** — regulatory submissions to FDA/EMA/MHRA still expected during 2026;
  no filing announcement found. Single event most likely to reset hub priorities. Keep the
  dedicated watch.

Confidence [Likely] that nothing significant broke. Note the asymmetry established in §6:
web sweeps have now produced both a false negative (ATTAIN-2, missed for two days) and a
gap the registry monitor cannot see (Mounjaro CV label). Neither channel alone is
sufficient.

---

## 6. Corrections to the 09-07 Report

Two claims from yesterday do not survive checking. Both were mine.

### Correction 1 — ATTAIN-2 is not an information edge. It is fully published. [Certain]

Yesterday's **top-ranked recommended action** read: *"Read the ATTAIN-2 results… Posted
09-04, still no press coverage as of today. The information edge is real and decaying."*

That is wrong. ATTAIN-2 is published in **The Lancet**
(`S0140-6736(25)02165-8`), with Lilly investor releases and secondary coverage in Medscape,
Cardiology Advisor and Docwire. Headline results: 72 weeks, n≈1,613, orforglipron 6/12/36 mg
vs placebo, mean weight reduction **5.1% / 7.0% / 9.6% vs 2.5%**, primary and all key
secondary endpoints met, global regulatory submissions triggered.

The 09-04 registry posting was the *tail* of a publication that had already happened. My
web sweep on 09-07 used a query that did not surface it, and I reported the negative result
as evidence of absence. It was evidence of a bad query.

**The item is still worth reading — the effect sizes matter for the T2D-plus-obesity
population and belong in the tracker — but it is a literature-review task, not a
time-sensitive one.** Anyone who reprioritised their day around a decaying edge yesterday
was reacting to my error.

### Correction 2 — the `has_results` defect is systematic, not a single record [Certain]

Yesterday reported `has_results: false` alongside `results_posted: "2026-09-04"` on
NCT05872620 as a one-record contradiction.

The scope is total. In `clinical_trials_snapshot_2026-09-06.json`, **344 of 344 records
that carry a `results_posted` date also carry `has_results: false`.** Not one is correct.

A fresh pull reading `hasResults` from the API's top-level study object returns
`has_results: true` for NCT05872620 and produces **zero** contradictions across the same
894 trials. **The API is fine; the hub's parser is reading the wrong field.** It is
almost certainly looking inside `protocolSection` for a flag that lives one level up.

Consequence: `has_results` is not a partially unreliable field, it is a constant `false`.
Any filter, dashboard facet or count built on it returns zero and always has.

---

## 7. Data Quality Defects — Current List

| # | Defect | Status |
|---|--------|--------|
| 1 | `clinical_trials_latest.json` is a 53-day-old md5-duplicate of the 07-17 snapshot | Open, unchanged |
| 2 | `has_results` is constant `false` across all 344 results-bearing records — parser reads wrong field | **Scope corrected today (§6)** |
| 3 | Null `title` on PMID 42698931 in `pubmed_recent_latest.json` | Open, 1 of 139 |
| 4 | Epigenetics + Drug Repurpose alert queries over-filtered by 126× and 6× | **Diagnosed today (§3)** — failing clause identified |
| 5 | `phase` uses two null encodings, `"NA"` and `"N/A"` | Open |
| 6 | **No source-freshness gate.** Monitor cannot distinguish "source published nothing new" from "source published nothing" | **New today (headline)** |
| 7 | **Run time precedes the daily batch.** 03:40 ET run reads at best the previous publishing day | **New today** |

**Detector for #6, one call, no auth:**

```
GET https://clinicaltrials.gov/api/v2/studies
    ?filter.advanced=AREA[LastUpdatePostDate]RANGE[YYYY-MM-DD, MAX]
    &countTotal=true&pageSize=1
```
Returns `totalCount`. If it is 0 for the date of the snapshot you are about to diff
against, the source has not published and the diff is meaningless. Gate the report on it.

---

## 8. Recommended Actions

Ranked. Items marked ▲ are new or re-ranked today.

1. ▲ **Gate the monitor on source freshness before diffing.** Query
   `AREA[LastUpdatePostDate]` for the current date; if `totalCount == 0`, report
   "source not published since <last publishing day>" instead of "no change." Three
   consecutive reports have now asserted a null result that the method could not have
   detected. This is the highest-value change in the hub and it displaces the
   seen-set item below it. (§7 defect 6)

2. ▲ **Move the scheduled run to after the daily batch posts** — 03:40 ET is before it.
   Any weekday time from mid-morning ET onward reads the same day's data. Combined with
   item 1, this eliminates the entire class of false nulls. (§7 defect 7)

3. ▲ **Fix the two over-filtered alert queries** in `baseline_pubmed_alerts.py` — delete
   the trailing AND-clause from both:
   ```
   "Diabetes Epigenetics":     'diabetes AND (epigenetic OR methylation)'
   "Diabetes Drug Repurpose":  'diabetes AND ("drug repurposing" OR "drug repositioning")'
   ```
   Recovers 126× and 6× recall respectively. Diagnosis is complete; this is now a
   two-line edit, not an investigation. (§3)

4. ▲ **Fix the `has_results` parser.** Read `hasResults` from the top level of each study
   object, not from inside `protocolSection`. Verified working in a fresh pull: 0
   contradictions vs 344. Until then, filter on `results_posted` and never on
   `has_results`. (§6)

5. **Replace consecutive-day diffing with a persistent seen-set** keyed on
   `results_posted`. Still correct, still worth doing — but items 1 and 2 must land first,
   or the seen-set will simply record the frozen state more efficiently.

6. **Run the two dead local scripts** on your machine:
   ```
   python Analysis/Scripts/baseline_clinical_trials.py
   python Analysis/Scripts/hub_monitor.py
   ```
   `hub_monitor.py` has not run in 53 days; there is no local file-change tracking at all
   right now. The sandbox snapshots this monitor writes do not update
   `clinical_trials_latest.json`, `clinical_trials_summary.md`, or `hub_monitor_state.json`.

7. **Change the zimislecel alert term to `VX-880 OR zimislecel`.** One line, doubles recall
   on the hub's most strategically important asset.

8. **Track NCT06239636 by NCT ID.** Sana does not sponsor it; Per-Ola Carlsson (Uppsala)
   does. Sponsor-string watches structurally miss investigator-sponsored first-in-human
   work, which is the category the hub most wants to catch early.

9. **Add `zenagamtide` to the tracked-therapy list.** 5 existing PubMed records, PHASE3 as
   of 09-01 (NCT07797335, Novo).

10. ▲ **Log the Mounjaro CV indication expansion** (late Aug 2026) in the tracker, linked to
    NCT04255433 (SURPASS-CVOT, results posted 07-08). It is the most consequential FDA
    action in scope this quarter and the registry monitor cannot see label changes at all.
    (§5)

11. **Read PMID 42694848** (COL1A2/APOLD1 nephropathy–retinopathy multi-omics) — carried
    from 09-06, still the only 4-domain paper on record, still the cleanest Tier 1 §1 + §5
    opportunity. Then **PMID 42627334** (post-baricitinib β-cell durability, *Diabetes Care*).

12. **Read ATTAIN-2 as literature, not as breaking news** — The Lancet paper, not the
    registry tab. Log effect sizes (9.6% vs 2.5% at 36 mg, 72 wk) in the tracker. Priority
    reduced from #1 per §6.

13. **Update the tracker** — 53 days stale. Warranted: NCT05872620 (ATTAIN-2 results),
    NCT07797335 (zenagamtide Ph3), NCT07804849 (pediatric verapamil), NCT06239636
    (hypoimmune islets), the two Lilly baricitinib T1D trials, and the Mounjaro CV label.
    Clear `.~lock.Diabetes_Research_Tracker.xlsx#` first.

14. **Repair or retire `clinical_trials_latest.json`.** Write it atomically at the end of
    each baseline run, or delete it and point consumers at the newest dated snapshot.

15. **Verify the Health-Equity-paired gaps by free-text query** before committing to gap #1
    or #4, the way gap #3 was verified. §3 is direct evidence that this hub's query strings
    fail in exactly this way.

16. **Broaden `report_freshness_audit`** to cover the trial pipeline — it checks 2 files
    and passes both while the trial pointer sits 53 days stale.

17. **Refresh `CONTRIBUTION_STRATEGY.md`** — 177 days old, predates the 08-31 doctrine.

---

## Evidence & Provenance

| Claim | Basis | Level |
|-------|-------|-------|
| Registry has not published since 09-04 | `AREA[LastUpdatePostDate]RANGE[d,d]` and `AREA[StudyFirstPostDate]RANGE[d,d]`, whole registry, no condition filter, 13 consecutive days 08-27→09-08. Weekend control: 08-29/08-30 also 0 | **Certain** |
| Weekend/holiday explains the zeros | Same series; every Sat/Sun in the window is 0, every business day is 730–1050. 09-07 was US Labor Day | **Certain** |
| 48h trial delta = 0 | Fresh ClinicalTrials.gov API v2 pull 09-08, same 5 filters as `baseline_clinical_trials.py`, 894 trials, diffed against 09-06 snapshot | Certain (but see headline — uninformative) |
| Epigenetics query loses 126× recall | E-utilities `esearch` count, 3 query variants × 3 windows, 09-08 | **Certain** |
| Drug Repurpose query loses 6× recall | Same method | **Certain** |
| `has_results` false on 344/344 | Field scan of `clinical_trials_snapshot_2026-09-06.json` vs fresh API pull reading top-level `hasResults` | **Certain** |
| ATTAIN-2 published in The Lancet | Web search returning Lancet/ScienceDirect abstract, Lilly investor releases, 3 secondary outlets | **Certain** |
| ATTAIN-2 effect sizes | Lancet abstract via search result text; **not** read from the primary paper | Likely — verify against the paper before entering in the tracker |
| Mounjaro CV indication expansion, late Aug 2026 | Web search, multiple outlets; **FDA primary source not fetched** | Likely — confirm on fda.gov before logging |
| `_latest` pointer stale | Metadata `generated` field + 36-trial count difference | Certain |
| No significant breaking news | Web search, 2 queries, negative result | Likely |
| Gap classifications | Inherited from `literature_gap_report.md` | BRONZE (per Doctrine) |

Today's snapshot was written to sandbox scratch, not to the hub, per the review-run rule.
It is byte-equivalent in content to `clinical_trials_snapshot_2026-09-06.json`.

*Generated by the Diabetes Research Hub automated monitor — 2026-09-08*
