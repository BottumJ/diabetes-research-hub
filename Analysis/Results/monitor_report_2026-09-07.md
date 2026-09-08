# Diabetes Research Hub — Monitor Report

**Run date:** 2026-09-07 (automated, sandbox)
**Prior report:** monitor_report_2026-09-06.md
**Mode:** Review run. No existing hub files modified.

---

## Headline

**The registry did not move in 24 hours. Zero new trials, zero status changes, zero
new results postings between the 09-06 and the 09-07 snapshot.** I acquired a fresh
snapshot specifically to test this rather than reporting "no change" from a stale file.

That null result is itself the most useful thing in this report, because it is the
second independent confirmation of yesterday's finding #2: **consecutive-day diffing is
the wrong detector.** A same-window 14-day scan of `results_posted` on today's snapshot
returns **4 postings**; the consecutive-day diff returns **0**. The signal exists; the
method throws it away.

Three open questions from the 09-06 report are now **closed with hard data** — zimislecel,
zenagamtide, and Sana. See §6.

---

## 1. File System Status

| File | Last modified | Age | State |
|------|--------------|-----|-------|
| `pubmed_recent_latest.json` | 2026-09-06 09:18 | 1d | Current |
| `pubmed_recent_summary.md` | 2026-09-06 09:18 | 1d | Current |
| `literature_gap_data.json` | 2026-09-06 09:12 | 1d | Current |
| `literature_gap_report.md` | 2026-09-06 09:12 | 1d | Current |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 02:38 | 1d | Current (sandbox-acquired) |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 | 7d | Current |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | **52d** | **STALE** |
| `clinical_trials_latest.json` | 2026-07-17 | **52d** | **BROKEN POINTER** |
| `clinical_trials_summary.md` | 2026-07-17 | **52d** | **STALE** |
| `hub_monitor_report.md` | 2026-07-17 | **52d** | **STALE** |
| `hub_monitor_state.json` | 2026-07-17 | **52d** | **STALE** |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 | **176d** | **STALE** |

**Evidence for "broken pointer" (Certain):** `clinical_trials_latest.json` and
`clinical_trials_snapshot_2026-07-17.json` are byte-identical —
`md5 = b7c4eff4329a85b75c34f2657246442b` for both. The pointer has not been rewritten
since July 17. Anything reading `_latest` is reading July.

**Staleness census:** 561 of 661 files in `Analysis/Results/` are older than 14 days.
That number is dominated by dated snapshot archives and is not by itself a problem;
the twelve rows above are the ones that matter.

**Freshness audit agrees, but only sees two files.** `report_freshness_audit.json`
(09-06) checked 2 reports, 0 failing. It does not cover the trial pipeline, which is
where the actual staleness is. The audit's clean bill of health is scoped too narrowly
to be reassuring.

**Sandbox note:** the workspace container's `/sessions` device is at **100% capacity**.
Writes to the mounted folder still succeed; deletes do not. Two zero-value probe files
(`_wtest.txt`) were created during a write test in `Analysis/Results/` and in the outputs
folder and could not be removed. Delete them at your convenience — they contain the word
"test" and nothing else.

---

## 2. Clinical Trial Changes

### 09-06 → 09-07 (24 hours)

| Metric | Count |
|--------|-------|
| Total trials | 894 → 894 |
| New | 0 |
| Removed | 0 |
| Status changes | 0 |
| New results posted | 0 |

Category counts identical: T1D Cure & Cell Therapy 156 · T1D Immunotherapy 77 ·
T2D Novel Therapies 152 · Diabetes Technology 245 · Recently Completed with Results 343.

### The same-window scan the diff misses

Scanning `results_posted >= 2026-08-24` on today's snapshot — 4 postings, of which the
consecutive-day diff surfaced **one**, and only because the trial happened to enter the
corpus on the same day:

| Posted | NCT | Phase | Sponsor | Study |
|--------|-----|-------|---------|-------|
| 2026-09-04 | NCT05872620 | PHASE3 | Eli Lilly | Orforglipron in obesity/overweight **with T2D** (ATTAIN-2) |
| 2026-09-02 | NCT04828785 | NA | UNC Chapel Hill | Food As MedicinE for Diabetes |
| 2026-08-27 | NCT04506151 | NA | Univ. of Illinois Chicago | Sleep optimization for glycemic control in T1D |
| 2026-08-24 | NCT05530356 | N/A | Univ. of Colorado Denver | Renal hemodynamics, energetics, insulin resistance |

**NCT05872620 remains the highest-value open item and is now 3 days old.** It is a
Phase 3 registry results posting from Lilly on the oral GLP-1 in the T2D-plus-obesity
population, and it is still ahead of press coverage — my web sweep (§5) surfaced nothing
on it.

### Six-day context (09-01 → 09-06), carried forward

8 new trials, 1 removed, 3 status changes. Worth keeping visible:

- **NCT07797335** — Novo Nordisk, AMBITION 7, **zenagamtide**, PHASE3, RECRUITING
- **NCT07804849** — Ain Shams Univ., oral **verapamil** in newly diagnosed children/adolescents with T1D, PHASE2/3, RECRUITING
- **NCT07796477** — CSPC Ouyi, SYH2069, PHASE2, not yet recruiting
- **NCT07801820** — Shanghai Minwei, MWN109, PHASE2, recruiting
- **NCT07282639** NOT_YET_RECRUITING → RECRUITING; **NCT07228117** and **NCT07076199** (Novo, insulin icodec PHASE3) RECRUITING → ACTIVE_NOT_RECRUITING

### Key-organization standing

| Org | Trials in corpus | Notable |
|-----|------------------|---------|
| Eli Lilly | 34 | 2 baricitinib T1D PHASE3 recruiting (NCT07222137, NCT07222332); retatrutide + orforglipron PHASE3 cluster |
| Novo Nordisk | 29 | CagriSema PHASE3 ×3; zenagamtide PHASE3 new; icodec program moving to ACTIVE_NOT_RECRUITING |
| Vertex | 3 | **VX-880/zimislecel PHASE3 recruiting** (NCT06832410, NCT04786262); VX-264 PHASE1/2 active |
| Sana Biotechnology | **0** | Sana has 3 registered trials registry-wide, none in diabetes — see §6 |

58 PHASE3 trials are currently RECRUITING across the corpus.

---

## 3. PubMed Highlights

Corpus: 139 unique papers, 30-day lookback, generated 2026-09-06 09:18.
**18 papers new since the 09-05 snapshot.**

### Cross-domain papers (20 of 139)

Highest-value first — a paper spanning four alert domains is the rarest object the
monitor produces:

1. **PMID 42694848** — *COL1A2 and APOLD1 Define a Dual-Axis Molecular Framework for
   Diabetic Nephropathy–Retinopathy Comorbidity* (Int J Med Sci). Four domains:
   AI/ML + Biomarker + Complications + Multi-Omics. **Still unread since it was flagged
   09-06.** Hits Doctrine Tier 1 §1 (Multi-Omics Integration, 19/20) and §5 (AI/ML
   Prediction, 18/20) simultaneously, and is testable against GEO / Metabolomics
   Workbench, which the doctrine already names as accessible.
2. **PMID 42626948** — Gene-edited hypoimmune islets as a cure for T1D (Expert Opin
   Biol Ther, 09-03). T1D Stem Cell Cure + T1D Immunotherapy + teplizumab. Directly
   relevant to the Vertex VX-264 and UP421 lines.
3. **PMID 42627334** — β-cell function 1 year after **stopping** oral baricitinib
   immunotherapy for T1D (*Diabetes Care*, 08-21). This is the durability question for
   the two Lilly PHASE3 baricitinib trials now recruiting. Highest-journal-quality item
   in the current corpus.
4. **PMID 42673585** — GLP-1 RAs and co-agonists for weight loss in adults **without**
   diabetes (*Ann Intern Med*, 09-01). Triple therapy hit: orforglipron + retatrutide +
   CagriSema.
5. **PMID 42694300** — Integrated oral microbiome + metabolome in Alström and
   Bardet-Biedl (Comput Struct Biotechnol J). Biomarker + Microbiome + Multi-Omics.

New cross-domain arrivals since 09-05: **42701157** (diabetes ↔ prostate cancer metabolic
convergence), **42700824** (gut microbiome / bile acid metabolomics, cordycepin in
diabetic NAFLD), **42698931** (Biomarker + Multi-Omics — **title field is empty in the
JSON**; extraction defect, see §7).

### Key-therapy tracking (30-day counts)

| Therapy | PubMed hits |
|---------|-------------|
| dapagliflozin | 41 |
| retatrutide | 11 |
| icodec | 10 |
| orforglipron | 8 |
| teplizumab | 5 |
| CagriSema | 4 |
| baricitinib | 3 |
| **zimislecel** | **0** |

### Domain volume — two dead channels

| Domain | 09-01 | 09-05 | 09-06 |
|--------|-------|-------|-------|
| T2D GLP-1 New | — | 190 | 188 |
| Diabetes AI/ML | — | 182 | 182 |
| Diabetes Microbiome | — | 144 | 139 |
| Diabetes Biomarker | — | 127 | 121 |
| Diabetes Health Equity | — | 58 | 56 |
| Diabetes Multi-Omics | — | 53 | 55 |
| LADA New Research | — | 9 | 8 |
| GLP-1 Pharmacogenomics | — | 3 | 3 |
| **Diabetes Epigenetics** | — | **2** | **1** |
| **Diabetes Drug Repurpose** | — | **1** | **1** |

*(09-01 column empty: that snapshot uses an older schema without per-domain
`total_count`. Not a data loss — a schema change.)*

**Epigenetics at 1/month and Drug Repurposing at 1/month are not credible.** Baseline
all-time volumes from the gap analysis are Epigenetics 7,770 and Drug Repurposing 621
since 2020 — roughly 100/mo and 8/mo respectively. Two of sixteen alert channels are
returning ~1% and ~12% of expected volume. [Likely] a query-construction fault, not a
real publication drought. Confirming requires running the two query strings from
`baseline_pubmed_alerts.py` directly against E-utilities and comparing counts — a
5-minute check that would move this from Likely to Certain.

---

## 4. Gap Analysis Summary

Generated 2026-09-06. 30 domains, 435 pairs. Validation level **BRONZE** per Doctrine —
single analytical source, expert confirmation still outstanding.

### Top 5 by gap score, restricted to "potentially meaningful"

| # | Intersection | Gap | Joint pubs | Tier 1 alignment |
|---|--------------|-----|------------|------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | **§6 Epidemiological/Equity (17/20)** |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | §2 Literature Synthesis |
| 3 | **Islet Transplant × Drug Repurposing** | 100.0 | 0 | **§4 Drug Repurposing (18/20)** |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | **§6 (17/20)** |
| 5 | Gene Therapy × LADA | 100.0 | 0 | §2 |

**Gap #3 independently verified this run (Certain).** A direct all-time PubMed query for
`"islet transplantation" AND "drug repurposing"` returns **exactly 1 record — PMID
27821710, from 2016.** This corroborates the gap report's own re-run note and makes #3
the strongest candidate in the list: it sits on the highest-scoring Tier 1 area the hub
can execute unilaterally (§4, 18/20, DrugBank/OpenTargets/STRING all open), and there is
no incumbent.

**Caution the report itself raises and I am repeating because it constrains action:**
a gap score of 100 with 0 joint publications can mean terminology mismatch as easily as
open territory. Gaps #1, #4, #7, #10 and #12 all pair a domain against Health Equity,
which is a keyword-brittle concept. Before committing to any of them, run the pair as a
free-text PubMed query the way I ran #3.

---

## 5. Breaking News

**Nothing that changes hub priorities.** Web sweep found no coverage of the ATTAIN-2
results posting, no new FDA diabetes action in the last 7 days, and no new Phase 3
readout announcements. Confirmed background, none of it new this week:

- Vertex: regulatory submissions for zimislecel to FDA/EMA/MHRA expected during 2026;
  fast-track designation in hand. No filing announcement found this week. Worth a
  dedicated watch — it is the single event most likely to reset this hub's priorities.
- Prior-2026 items already in the record: retatrutide TRANSCEND-T2D-1 (Mar), TRIUMPH-2/3
  (Jul), oral semaglutide approval, first generic dapagliflozin.

Confidence: [Likely] that nothing significant broke. Search coverage of registry-first
events is structurally poor — ATTAIN-2 is the proof — so registry monitoring, not news
monitoring, is the edge here.

---

## 6. Questions Closed This Run

Three items carried on the open list are now resolved against live sources.

### zimislecel alert — the query is fine, the literature is empty [Certain]

Direct E-utilities counts:

| Query | All-time count |
|-------|---------------|
| `zimislecel` | **3** |
| `zimislecel[tiab]` | 3 |
| `VX-880` | **6** |
| `zimislecel` restricted to 2026-08-07 → 2026-09-07 | **0** |

The alert is not broken. The INN genuinely has 3 lifetime PubMed records and zero in the
30-day window, which is why the tracker reports 0. **The fix is coverage, not repair:**
the literature is indexed under the code name. Change the tracked term to
`VX-880 OR zimislecel` and the channel doubles its recall immediately.

### zenagamtide — literature exists, the hub just isn't looking [Certain]

`zenagamtide` returns **5 PubMed records**. Yesterday's report characterised hub coverage
as zero; that is a tracking gap, not an evidence gap. Adding it to
`baseline_pubmed_alerts.py` pulls in 5 papers on day one for a compound that entered
Phase 3 six days ago.

### Sana Biotechnology — the sponsor query is correct and will never match [Certain]

`AREA[LeadSponsorName](Sana Biotechnology)` returns **3 trials — SC291 ×2 and SC262, all
B-cell oncology/autoimmune. Sana sponsors no registered diabetes trial.** The islet work
the doctrine cares about is **NCT06239636**, *First-in-human Safety Study of Hypoimmune
Pancreatic Islet Transplantation* — **lead sponsor Per-Ola Carlsson (Uppsala)**, not Sana.

So the recommendation in the 09-06 report ("add a Sana/UP421 query path") was aimed at
the wrong mechanism. Sponsor-string matching cannot find this trial because Sana is not
the sponsor. **Track NCT06239636 by NCT ID.** Any key-organization watch built on sponsor
strings will keep missing investigator-sponsored first-in-human work, which is exactly
the category the hub most wants to catch early.

---

## 7. Data Quality Defects Observed

1. **`clinical_trials_latest.json` is a 52-day-old duplicate** of the 07-17 snapshot
   (md5-identical). Consumers reading `_latest` get July data with no error signal.
2. **`has_results` contradicts `results_posted`.** NCT05872620 carries
   `results_posted: "2026-09-04"` and `has_results: false` in the same record. Any
   detector filtering on `has_results` misses real postings. Filter on `results_posted`.
3. **Null `title` field** on PMID 42698931 in `pubmed_recent_latest.json` — `title` is
   JSON `null` while `journal` ("Biochemistry and biophysics reports") and `domains`
   are populated. Extraction defect, single instance observed in 139 papers.
4. **Two alert channels returning implausible volume** (Epigenetics, Drug Repurposing) —
   see §3.
5. **`phase` field uses two null encodings** — `"NA"` and `"N/A"` appear across records
   for the same meaning (compare NCT04506151 vs NCT05530356). Any phase-based grouping
   will split these.

---

## 8. Recommended Actions

Ranked. Items 1–3 are unchanged from 09-06 and are getting older, not less important.

1. **Read the ATTAIN-2 results.** `https://clinicaltrials.gov/study/NCT05872620?tab=results`
   Posted 09-04, still no press coverage as of today. Log in the tracker. The information
   edge is real and decaying.

2. **Replace consecutive-day diffing with a persistent seen-set** keyed on
   `results_posted`. Today's run is the second consecutive demonstration: 24h diff = 0
   findings, 14-day same-window scan = 4. Filter on `results_posted`, never on
   `has_results` (defect #2). This is still the highest-value code change in the hub.

3. **Run the two dead local scripts.** On your machine:
   ```
   python Analysis/Scripts/baseline_clinical_trials.py
   python Analysis/Scripts/hub_monitor.py
   ```
   `hub_monitor.py` has not run in 52 days, so there is no local file-change tracking at
   all right now. The snapshots this monitor writes are a sandbox stopgap — they do not
   update `clinical_trials_latest.json`, `clinical_trials_summary.md`, or
   `hub_monitor_state.json`.

4. **Change the zimislecel alert term to `VX-880 OR zimislecel`** in
   `baseline_pubmed_alerts.py`. One-line change, doubles recall on the hub's most
   strategically important asset. (§6)

5. **Track NCT06239636 by NCT ID, not by sponsor string.** Sana is not the sponsor of the
   hypoimmune islet trial; Per-Ola Carlsson is. Add an explicit NCT watchlist to
   `baseline_clinical_trials.py` for doctrine-named assets that are investigator-sponsored.
   (§6)

6. **Add `zenagamtide` to the tracked-therapy list.** 5 existing PubMed records, Phase 3
   as of 09-01 (NCT07797335, Novo, insulin-glargine comparator). (§6)

7. **Audit the Epigenetics and Drug Repurposing query strings.** Run both directly against
   E-utilities and compare to the ~100/mo and ~8/mo the gap-analysis baselines predict.
   Moves §3 from Likely to Certain in about five minutes.

8. **Read PMID 42694848** (COL1A2/APOLD1 nephropathy–retinopathy multi-omics). Carried
   from 09-06, still the only 4-domain paper on record, still the cleanest Tier 1 §1 + §5
   opportunity in the corpus. Add **PMID 42627334** (post-baricitinib β-cell durability,
   *Diabetes Care*) — it is the follow-on question for two Lilly Phase 3 trials now
   recruiting.

9. **Update the tracker** — 52 days stale. Warranted entries: NCT05872620 (results),
   NCT07797335 (zenagamtide Ph3), NCT07804849 (pediatric verapamil), NCT06239636
   (hypoimmune islets), plus the two Lilly baricitinib T1D trials. Clear
   `.~lock.Diabetes_Research_Tracker.xlsx#` first.

10. **Repair or retire `clinical_trials_latest.json`.** Either write it atomically at the
    end of each baseline run or delete it and point consumers at the newest dated
    snapshot. A silently-52-days-stale pointer is worse than a missing file.

11. **Promote gap #3 (Islet Transplant × Drug Repurposing) to a work item.** Verified this
    run at 1 all-time PubMed record. Tier 1 §4 (18/20), all required resources open
    (DrugBank, OpenTargets, STRING, Reactome), no incumbent. Before starting, run the same
    free-text verification on the four Health-Equity-paired gaps to separate real
    territory from keyword brittleness.

12. **Broaden `report_freshness_audit`** to cover the trial pipeline. It currently checks
    2 files and passes both while the trial pointer sits 52 days stale — a clean audit
    that cannot see the failure.

13. **Refresh `CONTRIBUTION_STRATEGY.md`** — 176 days old, predates the 08-31 doctrine.

---

## Evidence & Provenance

| Claim class | Basis | Level |
|-------------|-------|-------|
| 24h registry delta = 0 | Fresh ClinicalTrials.gov API v2 pull 09-07, same 5 filters as `baseline_clinical_trials.py`, diffed against 09-06 snapshot | Certain |
| `_latest` pointer stale | md5 collision with 07-17 snapshot | Certain |
| zimislecel / zenagamtide / islet×repurposing counts | Direct PubMed E-utilities esearch, 09-07 | Certain |
| Sana sponsors no diabetes trial | ClinicalTrials.gov `AREA[LeadSponsorName]` query, 09-07 | Certain |
| Two alert channels under-returning | Volume comparison against gap-analysis baselines; queries not yet inspected | Likely |
| No significant breaking news | Web search, 3 queries, negative result | Likely |
| Gap classifications | Inherited from `literature_gap_report.md` | BRONZE (per Doctrine) |

Today's snapshot was written to sandbox scratch, not to the hub, per the review-run rule.
It is byte-equivalent in content to `clinical_trials_snapshot_2026-09-06.json` (894 trials,
identical category counts), so nothing is lost by not persisting it.

*Generated by the Diabetes Research Hub automated monitor — 2026-09-07*
