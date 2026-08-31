# Diabetes Research Hub — Monitor Report

**Run:** 2026-08-31 (Monday) · automated review run · 02:38 CT
**Scope:** `Analysis/Results` file review + live ClinicalTrials.gov queries + live PubMed esearch + web check
**Files modified:** none. This report is the only new file.

---

## Headline: the alert system sees 14% of the cross-domain signal it exists to find

The hub's stated highest-value literature signal is the cross-domain paper. I measured how many
of them the alert pipeline actually retrieves. I re-ran all 24 alert queries — the 16 domain
queries and 8 key-therapy queries, verbatim from `baseline_pubmed_alerts.py` — over the
**exact window of the 08-28 snapshot** (`2026/07/29–2026/08/28`, `datetype=pdat`), once at the
script's `retmax` and once with the ceiling removed.

| | retmax=10 (script) | retmax=300 (no ceiling) | recovered |
|---|---:|---:|---:|
| Unique PMIDs | **160** *(snapshot recorded 163)* | **1,010** | 15.8% |
| Cross-domain papers | **19** | **132** | **14.4%** |
| Domains pinned at the ceiling | **16 of 24** | — | — |

Of the 132 cross-domain papers in that window:

- **86 were never retrieved at all** — they sit below the `retmax` cut in every query that matches them.
- **27 were retrieved but seen as single-domain** — the paper came back under one query and was cut
  from the second, so the intersection that makes it valuable was invisible.
- **19 were correctly identified as cross-domain.**

**[Certain]** — same queries, same date type, same window, run live today; 160 vs the snapshot's
recorded 163 confirms the replication is faithful.

```
Cross-domain papers in window 2026/07/29 – 2026/08/28
                                                         n = 132
seen as cross-domain   ███                                    19
seen, mis-typed 1-dom  ████                                   27
never retrieved        ███████████████                        86
                       └────┴────┴────┴────┴────┴────┴────┴───┘
                       0   20   40   60   80  100  120
```

This reframes standing recommendation #8. It has been carried as a P1 sampling-hygiene item —
*"fix retmax before any longitudinal literature claim."* That framing is too weak. The ceiling is
not degrading a secondary metric; it is removing 86% of the primary output. **Promote to P0,
second only to running the pipeline at all.**

### What the ceiling cost, specifically

Five papers from that window that map onto Tier 1 doctrine areas and are absent from the snapshot:

| PMID | Paper | Journal | Domains | Tier 1 fit |
|---|---|---|---|---|
| **42390946** | A validated, modifiable proteomic score from the EXSCEL trial predicts cardiovascular events in diabetes | JCI Insight, 08-24 | AI/ML, Biomarker, GLP-1 | **#1 Multi-Omics Biomarker Integration** + **#5 Prediction Models** |
| **42143506** | The evolution of CAR therapies across oncology and autoimmunity | Int Immunopharmacol, 08-01 | Gene Therapy, T1D Immunotherapy | Treg/CAR-T axis — Gaps **#1** and **#3** |
| **42459945** | A framework for assessing algorithmic discrimination risks in training data: pediatric type 1 diabetes | JAMIA Open, 08 | Closed Loop AP, AI/ML, Health Equity | **#6 Epidemiological / equity** |
| **42290908** | Beyond eGFR and Albuminuria: Biological Pathways and Multiomics in Cardiovascular-Kidney-Metabolic Disease | Kidney Int Rep, 08 | AI/ML, Biomarker, Multi-Omics | **#1 Multi-Omics** |
| **42359629** | GLP-1 Gene Therapy Trial for Obesity and Type 2 Diabetes | J Cardiovasc Pharmacol, 08-01 | Gene Therapy, GLP-1 | **#3 Clinical Trial Intelligence** |

**42390946 is the one to read first.** A validated proteomic → cardiovascular-outcome score built on
a completed Phase 3 cohort (EXSCEL) is the exact object Tier 1 area #1 exists to produce. The hub
did not see it. **[Certain]** — retrieved live, absent from `pubmed_recent_snapshot_2026-08-28.json`
by set membership.

**Caveat, stated plainly:** raising `retmax` also admits marginal papers. 1,010 is what these
queries match, not 1,010 papers worth reading. The claim I am making is narrower and survives that
caveat: **cross-domain intersection is the hub's own high-value filter, and the ceiling destroys it
before the filter runs.**

---

## I ran the collaborator audit that 08-30 left open — and it argues for *demoting* its own P0

The 08-30 self-audit said: *"Sana's absence is now resolved; Sana's coverage is not. I did not
enumerate whether other key organizations are similarly hidden behind collaborator roles. That
audit is unrun."* It is run now. Six organizations, `AREA[CollaboratorName]`, full pagination,
diffed against the 893-trial 08-28 snapshot.

| Collaborator | Trials found | Missing from snapshot **and** active |
|---|---:|---:|
| Novo Nordisk | 173 | 19 |
| Eli Lilly | 188 | 5 |
| AstraZeneca | 86 | 8 |
| Boehringer Ingelheim | 40 | 4 |
| Vertex Pharmaceuticals | 2 | 0 |
| Sana Biotechnology | 1 | **1** |
| **Total** | **490** | **37** |

**Now the part that cuts against the prior recommendation.** Of those 37 active missed trials,
I read every title. **One** is on a scientific axis the hub cares about:

> **NCT06239636** — First-in-human Safety Study of Hypoimmune Pancreatic Islet Transplantation
> **RECRUITING** · EARLY_PHASE1 · n=2 · lead sponsor Per-Ola Carlsson (Uppsala) · Sana = collaborator
> Confirmed live today: still RECRUITING, last registry update 2024-12-11, still absent from the snapshot.

The other 36 are academic nephropathy cohorts, lifestyle and screening studies, CKD implementation
programs, and a 2010 insulin-detemir obesity study. Legitimate trials; not cure-axis, not
Phase 2/3 novel-therapy, not things the hub is built to track. One historical item is worth a note:
**NCT03163511** (ViaCyte VC-02, Phase 1/2, COMPLETED, Vertex as collaborator) — the predecessor
program on the encapsulation axis, also outside the snapshot.

**Therefore:** the 08-30 report ranked "fix the collaborator query hole" as **P0**. On the evidence
I gathered today, the entire yield of that architecture change is **one trial**, which is already
identified by NCT number in four consecutive reports. Adding `AREA[CollaboratorName]` to the sponsor
queries returns 490 records to filter for a signal you can obtain by typing one NCT ID into the
tracker. **Demote to P2. Add NCT06239636 by hand today.** **[Certain]** on the counts (full
pagination, no truncation); **[Likely]** on the relevance triage, since I judged the other 36 from
titles alone — re-read them if you disagree with the cut.

---

## The registry feed is not suspect. The 08-30 falsification test was mis-specified.

08-30 wrote: *"The weekend explanation is [Likely], not [Certain]... If Monday 08-31 also returns
zero, the feed itself is suspect."* Monday 08-31 returned zero. **The feed is fine; the test was
wrong.** Here is the daily posting histogram, `AREA[LastUpdatePostDate]`, condition = diabetes,
15 consecutive days, queried live today:

```
        Mon  Tue  Wed  Thu  Fri  Sat  Sun
Aug 17   25   26   20   28   48    0    0
         ██▌  ██▌  ██   ██▊ ████▊
Aug 24   20   29   23   34   36    0    0
         ██   ██▊  ██▎  ███▍ ███▌
Aug 31    0    ·    ·    ·    ·    ·    ·
         ↑ queried 02:38 CT — before the day's posting batch
```

Weekends are true zeros, both weekends, no exceptions — **[Certain]**, upgraded from the prior
[Likely]. Mondays are *not* zero: 08-17 posted 25 and 08-24 posted 20. So a zero on Monday cannot
mean "Mondays are quiet." It means this monitor runs at **02:38 Central**, before ClinicalTrials.gov
has posted anything for the calendar day it is asking about. **[Likely]** — the two nonzero Mondays
establish that Mondays post; I have not measured the registry's posting hour directly, which is what
would make this [Certain].

**Fix:** stop diffing against *today*. Diff against **the last completed business day**. A monitor
that runs pre-dawn will read zero for the current date every single day of the week, and that zero
carries no information at all.

### Live event feed, run today

893/893 tracked NCTs resolved, 18 batched calls, zero fetch failures.

| Check vs. 08-28 snapshot | Result |
|---|---:|
| Status changes | **0** |
| Newly posted results | **0** |
| `whyStopped` newly populated | **0** |
| Registry updates dated 08-29, 08-30, or 08-31 | **0** |
| New diabetes registrations first-posted since 08-29 | **0** |

**The trial side of the hub is current through the last business day (08-28).** It is the fourth
consecutive day this has been true. The daily trial-diff is, for now, a null check.

---

## File system status

| File | Modified | Age | Status |
|---|---|---:|---|
| `clinical_trials_snapshot_2026-08-28.json` | 08-28 08:24 | 3d | current |
| `pubmed_recent_snapshot_2026-08-28.json` | 08-28 08:28 | 3d | current |
| `Research_Findings_Summary.md` | 08-30 09:06 | 1d | current |
| `literature_gap_report.md` | 08-30 09:06 | 1d | **misleading — underlying data is 45d old** |
| `clinical_trials_latest.json` | 07-17 02:05 | **45d** | **stale** |
| `pubmed_recent_latest.json` | 07-17 02:06 | **45d** | **stale** |
| `hub_monitor_report.md` | 07-17 02:16 | **45d** | **stale** |
| `Diabetes_Research_Tracker.xlsx` | 07-17 10:07 | **45d** | **stale** |
| `literature_gap_data.json` | 07-18 03:11 | **44d** | **stale** |

`literature_gap_report.md` stamps *"Generated: 2026-08-30 09:06"* over a body that reads
*"Date range: 2020/01/01 to 2026/07/17"*, sourced from `literature_gap_data.json` carrying
`generated: 2026-07-17T10:14:41`. **Eighth consecutive day flagged.** **[Certain]** — three
timestamps read directly.

**Day 45 of acquisition-arm downtime.** Nothing ran locally today. Git log shows daily quality
iterations unbroken through 08-30 (gap evidence-design audit, semantic citation support, pubtype
cache expiry). The four acquisition scripts have not run locally since 07-17. **[Certain]** —
git log plus output mtimes. The 08-27/08-28 snapshots are sandbox stopgaps, not local runs, and
they are labelled as such in their own metadata.

---

## Clinical trials — state of the board

No changes since 08-28 (see live feed above). Carried forward for continuity:

**Phase 3 recruiting, T1D cure/immunotherapy axis:** NCT04786262 and NCT06832410 (Vertex,
zimislecel/VX-880); NCT07222332 and NCT07222137 (Lilly, baricitinib — preserve beta-cell function
and delay Stage 3). Plus **NCT06239636** (Sana/Carlsson, UP421 hypoimmune islets, EARLY_PHASE1),
which remains outside the snapshot.

**Newest Phase 3 entrants, first posted in August:** NCT07754461 (Boehringer, survodutide, n=600,
08-10); NCT07743983 (BrightGene BGM0504, n=372, 08-04); NCT07743450 (Ascletis ASC30 oral, n=1,560,
08-03). AstraZeneca's five-trial elecoglipron Phase 3 build-out (registered 06-23/06-24) is still
uncharacterised in the hub.

**Results postings still unlogged:** 22 tracked trials have posted results since 2026-07-15; the
tracker was last written 07-17, so 21 cannot be logged. Highest priority remains **NCT04596631**
(Novo Nordisk, Phase 3 oral semaglutide, results posted 08-21) and **NCT04255433** (SURPASS-CVOT,
now the basis of the 08-28 Mounjaro CV indication).

*Data-quality note:* the `has_results` field is `false` for all 858 trials in the 07-17 snapshot
while `results_posted` is populated for 322 of them. The field was broken then and is correct now
(342/342 agreement in the 08-28 snapshot). Any diff spanning 07-17 will report ~322 phantom
"new results." **[Certain]** — counted both fields in both snapshots. Do not trust `has_results`
in any pre-08-27 snapshot.

---

## PubMed — 08-28 snapshot plus today's live check

Within what the alert did capture (163 papers, 16 cross-domain), the T1D-cure cluster is the
substantive one and is unchanged from 08-30:

- **42626948** — Gene-edited hypoimmune islets as a cure for T1D: immunological challenges.
  *Expert Opin Biol Ther*, 08-21. Four domains. **Read alongside NCT06239636** — same scientific
  axis, review and trial. Fourth day at the top of the queue.
- **42627334** — Beta-cell function 1 year after stopping oral baricitinib. *Diabetes Care*, 08-21.
  Directly informs the two recruiting Lilly baricitinib Phase 3s.
- **42610933** — Baseline serum metabolites as predictors of teplizumab response. *Diabetes*, 08-18.

**Key therapy counts, run live today** (`diabetes AND <term>`, Aug 2026 pdat / all-time):

| Term | Aug 2026 | All-time |
|---|---:|---:|
| dapagliflozin | 32 | 3,477 |
| orforglipron | 12 | 105 |
| retatrutide | 10 | 124 |
| icodec | 6 | 160 |
| CagriSema | 4 | 50 |
| teplizumab | 4 | 270 |
| baricitinib | 3 | 73 |
| **zimislecel** | **0** | **3** |

The zimislecel zero is confirmed again and remains **not** a term-mismatch problem — the corpus
already holds PMID 40544428 (the NEJM pivotal paper). The 08-30 finding stands: the fix is an
ingestion check joining `therapy_hits` against `paper_library/index.json`, not a term expansion.

---

## Gap analysis

Unchanged and unrunnable without a local pass — `literature_gap_data.json` is 44 days old and the
gap step needs ~35–40 minutes, which is why it is a local script.

**Top 5 by gap score** (all gap score 100.0, joint publications 0, all **BRONZE**):

| Rank | Intersection | d1 count | d2 count | expected |
|---|---|---:|---:|---:|
| 1 | Treg / CAR-T × Neuropathy | 953 | 3,160 | 7.53 |
| 2 | Beta Cell Regen × Health Equity | 1,463 | 1,990 | 7.28 |
| 3 | Treg / CAR-T × Health Equity | 953 | 1,990 | 4.74 |
| 4 | Glucokinase × Health Equity | 854 | 1,990 | 4.25 |
| 5 | Gene Therapy × LADA | 2,296 | 582 | 3.34 |

**Tier 1 alignment.** Four of the five sit on the Health Equity or Treg/CAR-T axes, which map to
doctrine Tier 1 areas #6 (Epidemiological / disparity analysis) and #2 (Literature synthesis).
Two things about that convergence should temper it:

1. **Health Equity appears in three of five because its individual count is low (1,990),** which
   inflates every gap score it touches. The standing recommendation to widen the Health Equity
   query (19-term expansion) and re-rank by `expected − joint` rather than by ratio is a
   prerequisite to any Tier 1 commitment here, not a refinement of one.
2. **Today's finding makes it worse, not better.** With `retmax` capped, Health Equity returned 10
   of 73 matching August papers. Any equity-axis gap claim is being made on a 14% sample of the
   very literature that would falsify it.

Two of today's ceiling-missed papers land directly on these gaps: **42143506** (CAR therapies in
autoimmunity — gaps #1 and #3) and **42459945** (algorithmic discrimination in pediatric T1D —
the AI/ML × equity intersection). Neither would change a gap score, but both are evidence that
"zero joint publications" is partly a retrieval artifact and should be re-tested after the
`retmax` fix.

---

## Breaking news

**Nothing new since 08-28.** The FDA approval of Mounjaro (tirzepatide) to reduce MACE risk in
adults with T2D — approved 2026-08-28, on SURPASS-CVOT (NCT04255433) — was logged in the 08-30
report and remains the last significant action. Pending decisions unchanged: Novo Nordisk's
cagrilintide/semaglutide fixed-dose combination, and insulin efsitora alfa (potential second weekly
basal insulin, decision expected H2 2026). No Phase 3 readouts, regulatory actions, or major
publications in the 08-29 → 08-31 window. **[Likely]** — two web searches, negative result;
absence of news is weaker evidence than presence.

---

## Recommended actions

**P0**

1. **Run the acquisition pipeline locally. Day 45.** Everything below is downstream of it.
   ```
   cd C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts
   python run_daily_local.py
   ```
   Set `NCBI_API_KEY` first (3 → 10 req/sec). The gap step needs ~35–40 min and cannot run in the
   sandbox — that is why it is a local script.

2. **Raise `retmax` in `baseline_pubmed_alerts.py` before the next run.** `LOOKBACK_DAYS` stays 30;
   change `max_results` from 10 (domains) and 5 (therapies) to 200, and paginate above that.
   Measured cost of not doing it: **86% of cross-domain papers**, including a validated EXSCEL
   proteomic CV-risk score sitting squarely in Tier 1 area #1. This is now the highest-value
   single-file edit in the hub. *(Promoted from P1 #8 on today's measurement.)*

3. **Add NCT06239636 to the tracker by hand.** Five minutes. It has been named in five consecutive
   reports and is still not recorded. Do not wait on the query-architecture change.

4. **Log NCT04596631** (Novo Nordisk Phase 3, results 08-21) and **NCT04255433** (SURPASS-CVOT,
   basis of the 08-28 Mounjaro CV approval). 21 results postings are unlogged.

**P1**

5. **Diff the event feed against the last completed business day, not the current date.** A 02:38 CT
   run reads zero for "today" on every day of the week. Weekend zeros are real and should be
   skipped, not flagged.

6. **Add an ingestion check to the therapy alerts.** Join `therapy_hits` against
   `paper_library/index.json` so a therapy already in the corpus never reports as absent. Still the
   correct fix for the zimislecel zero.

7. **Stop `literature_gap_report.md` stamping render time over 45-day-old data.** Eighth
   consecutive flag. Start at `gap_analysis_daily.py` and `refresh.ps1`.

8. **Widen the Health Equity query, then re-rank gaps by `expected − joint`.** Prerequisite to any
   Tier 1 equity commitment — and now doubly so, since the ranking currently rests on a 14% sample.

9. **Carry a findings ledger between runs.** NCT06239636 has been found, lost, and re-derived four
   times across five reports. This is the second consecutive report to raise it.

**P2**

10. **`AREA[CollaboratorName]` in the sponsor queries.** *Demoted from P0.* Full audit today: 490
    collaborator trials across six organizations, 37 active and missing, one worth having. Do it
    when convenient; do not let it block anything.

11. **Distrust `has_results` in any snapshot before 08-27.** Broken (0/858) in the 07-17 file.
    Guard any longitudinal diff that spans it, or you will report ~322 phantom results postings.

**Reading queue**

12. **42390946** — EXSCEL proteomic CV-risk score, *JCI Insight*. New today. Tier 1 #1 and #5.
13. **42626948** — gene-edited hypoimmune islets, *Expert Opin Biol Ther*. Read with NCT06239636.
14. **42627334** — baricitinib one year after stopping, *Diabetes Care*. Informs two live Lilly Phase 3s.
15. **42143506** — CAR therapies across oncology and autoimmunity. Sits on gap #1 and #3.

---

## Evidence levels (per Research Doctrine)

| Claim | Level | Basis |
|---|---|---|
| Alert pipeline recovers 19 of 132 cross-domain papers | **[Certain]** | 24 queries re-run live, exact snapshot window, both retmax settings; 160 vs recorded 163 |
| 16 of 24 domains pinned at the retmax ceiling | **[Certain]** | per-query result counts, measured |
| Five named Tier 1 papers absent from the 08-28 snapshot | **[Certain]** | set membership against snapshot `papers` keys |
| Collaborator axis yields 37 active missed trials, 1 relevant | **[Certain]** counts / **[Likely]** triage | full pagination; relevance judged from titles only |
| Weekend registry zeros are real | **[Certain]** | two consecutive weekends, four days, all zero |
| Monday zero is a run-time artifact, not feed failure | **[Likely]** | Mondays 08-17 (25) and 08-24 (20) nonzero; posting hour not directly measured |
| Trial side current through 08-28 | **[Certain]** | 893/893 live resolution, zero deltas |
| `has_results` broken in pre-08-27 snapshots | **[Certain]** | 0/858 vs 342/342, both fields counted |
| Acquisition arm down 45 days | **[Certain]** | git log + output mtimes |
| No breaking news 08-29 → 08-31 | **[Likely]** | two web searches, negative result |

---

## Self-audit

- **No existing file was modified.** This report is the only write, per the review-only charter.
- **All live queries were read-only** (ClinicalTrials.gov GET, PubMed esearch/esummary). No snapshot
  was written, so no 08-31 snapshot exists. Every snapshot-derived figure is from 08-28 and labelled.
  The event-feed and PubMed diffs *are* current as of today.
- **I demoted a P0 from yesterday's report.** The collaborator fix was ranked P0 on 08-30 largely on
  NCT06239636's importance. I agree the *trial* matters; I disagree that a query-architecture change
  is the way to get it, having now measured the yield. If you think 36 academic nephropathy and
  implementation trials belong in the hub, my triage is the thing to overturn, not the count.
- **I falsified a prediction this monitor made yesterday.** 08-30 said a zero on Monday 08-31 would
  make the feed suspect. It returned zero and the feed is fine. The test did not account for the
  monitor's own run time. Two prior Mondays are the whole basis for that conclusion — check them.
- **The `retmax` finding is the load-bearing claim in this report and it is one measurement.**
  It is reproducible in about four minutes: re-run the 24 queries at `retmax=10` and `retmax=300`
  over `2026/07/29–2026/08/28` with `datetype=pdat`. Do that before acting on P0 #2.
- **1,010 is not 1,010 papers worth reading.** The domain queries are broad. I deliberately made the
  narrower cross-domain claim instead, which does not depend on the total being meaningful.
- **The five "Tier 1 papers missed" are my judgment of fit, not the doctrine's.** I matched them to
  Tier 1 areas by reading titles and journal against the doctrine text. Reasonable people could cut
  42290908 or 42359629 from that list.
- **Unrun, and now two days old:** whether the 2026 Health Equity individual count (1,990) is
  genuinely low or an artifact of the same narrow query that produces the gap ranking. That is a
  circularity risk in the top 5 and nobody has tested it.

---

## Sources

- ClinicalTrials.gov API v2 — <https://clinicaltrials.gov/api/v2/studies> (893-NCT event feed;
  `LastUpdatePostDate` histogram 08-17→08-31; `AREA[CollaboratorName]` audit, 6 organizations)
- PubMed E-utilities esearch/esummary — <https://eutils.ncbi.nlm.nih.gov/entrez/eutils/>
  (24 alert queries at two retmax settings; 8 key-therapy counts)
- Local: `clinical_trials_snapshot_2026-08-28.json`, `pubmed_recent_snapshot_2026-08-28.json`,
  `clinical_trials_snapshot_2026-07-17.json`, `literature_gap_data.json`, `literature_gap_report.md`,
  `hub_monitor_report.md`, `monitor_report_2026-08-30.md`, `RESEARCH_DOCTRINE.md`,
  `Analysis/Scripts/baseline_pubmed_alerts.py`, git log
- FDA — Mounjaro CV indication, approved 2026-08-28
  <https://investor.lilly.com/news-releases/news-release-details/fda-approves-lillys-mounjaro-tirzepatide-reduce-cardiovascular>
- Prime Therapeutics — GLP-1 pipeline update, August 2026
  <https://www.primetherapeutics.com/glp-1-pipeline-update-august-2026>

---
*Automated review run — no files modified. Generated 2026-08-31.*
