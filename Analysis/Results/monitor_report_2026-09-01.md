# Diabetes Research Hub — Monitor Report

**Run:** 2026-09-01 (Tuesday) · automated review run
**Scope:** `Analysis/Results` file review · live ClinicalTrials.gov v2 · live PubMed E-utilities · web check
**Files written:** 3 new (this report + two dated snapshots). **No existing file modified.** See Self-audit.

---

## Headline: yesterday's finding replicated. Stop verifying it and go fix it.

The 08-31 report made one load-bearing claim and asked to have it checked before anyone acted:
the alert pipeline's `retmax=10` ceiling destroys ~86% of the cross-domain signal. It called
itself "one measurement" and gave a four-minute reproduction recipe.

I ran that recipe. It replicates — and it replicates on a *second, different* window.

```
CROSS-DOMAIN PAPER RECOVERY AT retmax=10  ·  two independent runs

                          claimed 08-31   my run (same window)   my run (today's window)
                          07/29–08/28     07/29–08/28            08/02–09/01
unique PMIDs                160 / 1,010        162 / 1,018            161 /   846
cross-domain papers          19 /   132         19 /   133             17 /   115
recovery                       14.4%              14.3%                  14.8%
queries pinned at ceiling     16 of 24           16 of 24               14 of 24

fate of the true cross-domain set (today's window, n = 115)
  seen as cross-domain   ███                                       17
  seen, typed 1-domain   █████                                     28
  never retrieved        ████████████                              70
                         └────┴────┴────┴────┴────┴────┴────┴────┘
                         0   10   20   30   40   50   60   70   80
```

**[Certain]** — 24 verbatim query strings, `datetype=pdat`, two `retmax` settings, two windows,
run live today. The two cross-domain lines agree with 08-31 within **1 paper** (19 vs 19, 132 vs
133); the unique-PMID lines agree within **8 of 1,018 (0.8%)**. This is now an independently
replicated measurement, not a single one. **The verification task is closed. The fix is not.**

Two caveats on my own replication, both of which make the production loss *worse* than the table
shows, not better:

- I ran all 24 queries at `retmax=10`. The real script uses **`retmax=5`** for the 8 therapy
  queries (line 233). "16 of 24 pinned" therefore understates the production pipeline.
- Two `retmax=10` runs over the same window ~20 minutes apart returned **different** sets. PMIDs
  **42390946** and **42429765** were retrieved by the ceiling test and *not* by the snapshot run.
  With `sort=date` and a hard cut at 10, which papers survive is non-deterministic at the tie
  boundary. A ceiling that drops a different 85% each run is worse than one that drops a fixed 85%:
  it makes day-to-day "new paper" diffs partly noise.

**And I inherited the defect.** The 09-01 snapshot I wrote today runs at `retmax=10` for
comparability with 08-27/08-28. It is missing the same 85%. Every snapshot in this folder is.
Longitudinal PubMed comparisons across this series are comparisons of a biased sample to itself —
internally consistent, externally wrong.

The one paper 08-31 named as most important, **PMID 42390946** (validated proteomic → CV-event
score from EXSCEL, *JCI Insight*, Tier 1 area #1), is **still absent from today's snapshot** —
it appears in no `domain_results` or `therapy_hits` list. At `retmax=300` it carries 3 domains.
Four days, two snapshots, still invisible. **[Certain]** — set membership in
`pubmed_recent_snapshot_2026-09-01.json`.

---

## New finding: a second blind spot, and `retmax` will not touch it

The ceiling is a *literature*-side defect. There is a *trial*-side one nobody has measured, and it
cost the hub a real result yesterday.

`baseline_clinical_trials.py` conditions every query on status. Queries #1–#4 take active statuses
(`RECRUITING / NOT_YET_RECRUITING / ACTIVE_NOT_RECRUITING`, plus `ENROLLING_BY_INVITATION` in #1
only); query #5 takes `COMPLETED`. **`TERMINATED`, `SUSPENDED` and `WITHDRAWN` appear in no
query.** A trial that stops early and posts its data is structurally invisible to this hub.

On **2026-08-31** one did.

### NCT04628481 — Ladarixin in recent-onset T1D — stopped for futility, results posted

| | |
|---|---|
| Sponsor | Dompé Farmaceutici S.p.A |
| Design | Phase 2, randomised, placebo-controlled; n = 289 enrolled |
| Ran | 2021-01-12 → 2025-10-21 |
| Status | **TERMINATED** — *"stopped due to futility as per protocol"* |
| Results first posted | **2026-08-31** |
| Primary endpoint | Change from baseline in 2-h C-peptide AUC (MMTT), Month 6 |
| Ladarixin (n=94) | **−0.284** nmol·hr/L (95% CI −0.453, −0.114) |
| Placebo (n=46) | **−0.151** nmol·hr/L (95% CI −0.373, 0.071) |
| Adjusted difference | **−0.133** (95% CI −0.334, 0.068), **p = 0.196** |

**Read it precisely:** this is a *null* result, not a harm result. The point estimate numerically
favours placebo, the confidence interval crosses zero, and the trial was stopped by its own
pre-specified futility rule. CXCR1/2 blockade did not preserve β-cell function in this population.
**[Certain]** — pulled live from the CT.gov results section, group-level values and the ANCOVA
analysis block read directly.

This matters to the hub specifically: **T1D Immunotherapy** is an active alert domain, β-cell
preservation sits under Tier 1 area #3 (Clinical Trial Intelligence), and negative Phase 2 data at
n=289 is exactly the kind of evidence that should *stop* a research path rather than start one.
The hub would never have seen it.

### Sizing the trial-side blind spot (live counts, today)

```
Diabetes trials with results posted since 2025-01-01

COMPLETED      — hub query #5 captures   ████████████████████████████████  341
TERM/SUSP/WDRW — hub captures none       ███                                32
   ...of those, Phase 2 or 3                                                12

Active trials excluded by the phase filters
T1D Phase 1 drug        — T1D immuno query is PHASE2/3 only   21
T2D Phase 1 biological  — T2D query is PHASE2/3 only           5
```

**[Certain]** — five `countTotal` queries against CT.gov v2, run today.

32 result-posting trials is ~9% on top of the 341 the hub does see, and the 12 Phase 2/3 ones are
disproportionately informative: trials stop early for futility, for safety, or for business
reasons, and the first two are findings. The Phase 1 exclusion is the smaller issue but caught a
live example — **NCT07794254**, an islet-cell infusion for **type 2** diabetes (Hangzhou Reprogenix,
first posted 2026-08-29), falls through both the T1D query (wrong condition) and the T2D query
(wrong phase). Islet therapy aimed at T2D is unusual enough to be worth a look.

---

## File system status

| File | Last written | Age | Verdict |
|---|---|---|---|
| `clinical_trials_snapshot_2026-09-01.json` | today | 0 d | written this run |
| `pubmed_recent_snapshot_2026-09-01.json` | today | 0 d | written this run |
| `monitor_report_2026-08-31.md` | 2026-08-31 | 1 d | current |
| `literature_gap_report.md` | 2026-08-31 | 1 d | **misleading — see below** |
| `clinical_trials_latest.json` | 2026-07-17 | **46 d** | **stale** |
| `pubmed_recent_latest.json` | 2026-07-17 | **46 d** | **stale** |
| `literature_gap_data.json` | 2026-07-18 | **45 d** | **stale** |
| `hub_monitor_report.md` | 2026-07-17 | **46 d** | **stale** |

**The acquisition arm has now been down 46 days.** `git log` shows daily analysis commits through
08-31 without interruption, so the hub is not idle — but every `*_latest.json` was last written by
`baseline_*.py` on 07-17. The 08-27, 08-28 and 09-01 snapshots were all written by this sandbox
monitor, which is a stopgap and should not be the collection mechanism. **[Certain]** — mtimes plus
the `acquired_by` field carried in each snapshot's metadata.

**`literature_gap_report.md` has a freshness illusion.** Its header reads *"Generated: 2026-08-31
03:31"* — but its own body reads *"Date range: 2020/01/01 to 2026/07/17"*, and the file it renders,
`literature_gap_data.json`, carries `"generated": "2026-07-17T10:14:41"`. The 08-31 timestamp is a
re-render of 45-day-old counts. Anyone reading the header will over-trust it. **[Certain]** — both
files read directly. This is a labelling defect, not a data defect; the numbers are fine *for
2026-07-17*.

---

## Clinical trials — 08-28 → 09-01

| | |
|---|---|
| Total | 893 → **887** |
| New trials | **0** |
| Dropped | **6** |
| Status changes (within cohort) | **0** |
| New results posted (within cohort) | **0** |

Zero new trials over four days looks like a broken feed. It isn't. **Five of the six drops are an
administrative artifact, not science.**

```
Why 6 trials left the cohort

NCT06542627  →  UNKNOWN   last sponsor update 2024-08-07  ┐
NCT06558708  →  UNKNOWN   last sponsor update 2024-08-19  │  CT.gov auto-flips a study to
NCT06559722  →  UNKNOWN   last sponsor update 2024-08-19  ├─ "Unknown status" ~2 years after
NCT06569940  →  UNKNOWN   last sponsor update 2024-08-26  │  the last sponsor update. These
NCT06575478  →  UNKNOWN   last sponsor update 2024-08-28  ┘  five aged out on schedule.

NCT07325461  →  COMPLETED last update 2026-08-31  ← the only real change
```

**[Certain]** — each of the six queried individually against CT.gov today.

**Practical consequence:** the "dropped trials" line in this monitor is dominated by the 2-year
staleness clock — 5 of 6 drops over this 4-day interval. It should be triaged on
`overallStatus == UNKNOWN` before a human ever reads it. (One interval is not a rate; I am not
claiming a weekly figure.)

The live event feed (any diabetes trial with `LastUpdatePostDate ≥ 2026-08-29`) returned **38**
records: 12 COMPLETED, 9 RECRUITING, 7 NOT_YET_RECRUITING, 6 ACTIVE_NOT_RECRUITING, 3 TERMINATED,
1 SUSPENDED. Three posted first results (NCT04628481 above; NCT07030868, a Lilly Phase 2 terminated
"for strategic business reasons" with **n = 1 actual** and therefore no interpretable data;
NCT04416269, an Emory Phase 4 inpatient oral-agent study).

### Board state, unchanged but worth restating

16 Phase 3 T1D trials are RECRUITING. The ones that move the field:

| NCT | n | Sponsor | Programme |
|---|---:|---|---|
| NCT04786262 | 52 | Vertex | VX-880 / zimislecel — islet cell therapy |
| NCT06832410 | 10 | Vertex | VX-880 — second Phase 3 |
| NCT07088068 | 723 | Sanofi | Teplizumab vs placebo |
| NCT07222137 | 150 | Eli Lilly | Baricitinib — delay of Stage 3 T1D |
| NCT07222332 | 300 | Eli Lilly | Baricitinib — β-cell preservation, children |

Novo (CagriSema NCT07564414, n=2,500; AMAZE 8 NCT07400107, n=1,000) and AstraZeneca's five-trial
elecoglipron Phase 3 programme (NCT07664553 n=600, NCT07662044 n=800, NCT07662135 n=900,
NCT07662213 n=1,200, NCT07662109 n=2,000) are the large T2D reads in flight. No status change in
any of them since 08-28.

---

## PubMed — 09-01 snapshot

163 → **160** unique papers in the rolling 30-day window; **79 papers are new** relative to 08-28.

Domain counts fell almost across the board — GLP-1 −18, Remission −13, Health Equity −12,
Biomarker −10, Multi-Omics −8. **This is the window sliding, not a publication slowdown.** The
30-day window dropped 07/29–08/01 and gained 08/29–09/01 — four days out, four days in, but
PubMed indexing lags, so the incoming days are thinner than the outgoing ones. Reading these
deltas as research-activity signal would be a mistake. **[Certain]** — window bounds are in each
snapshot's metadata. Eleven domains fell and five rose; Microbiome (+10) and T1D Immunotherapy
(+3) rose meaningfully against that headwind, while AI/ML, LADA and GLP-1 Pharmacogenomics moved
+1 each, which is nothing.

### Cross-domain papers worth your time

At `retmax=10` the snapshot found 17. At `retmax=300` there are 115. From the full set — the last
column reports how the **09-01 snapshot** handled each, which is the thing that matters:

| PMID | Paper | True domains (retmax=300) | Snapshot outcome |
|---|---|---|---|
| **42626948** | Gene-edited hypoimmune islets as a cure for T1D — immunological challenges (*Expert Opin Biol Ther*) | 4 — Gene Therapy, T1D Immuno, T1D Stem Cell, teplizumab | correct, 4 domains |
| **42673585** | GLP-1 RAs and co-agonists for weight loss in adults without diabetes — systematic review (*Ann Intern Med*, 09-01) | 3 — orforglipron, retatrutide, CagriSema | correct, 3 domains |
| **42610933** | Baseline serum metabolites predict teplizumab response in T1D (*Diabetes*) | 3 — Biomarker, teplizumab, T1D Immuno | correct, 3 domains |
| **42634284** | Responders vs non-responders: predicting response to GLP-1 / GLP-1-GIP RA therapy (*DOM*) | 3 — Microbiome, GLP-1 Pharmacogenomics, T2D GLP-1 | **present but typed 1-domain** (GLP-1 Pharmacogenomics only) |
| **42390946** | **Validated proteomic score from EXSCEL predicts CV events in diabetes** (*JCI Insight*) | 3 — AI/ML, Biomarker, GLP-1 | **absent — never retrieved** |
| **42568080** | Three-metabolite microbiota signature for early GDM risk stratification (*Cardiovasc Diabetol*) | 3 — AI/ML, Microbiome, Multi-Omics | **absent — never retrieved** |
| **42429765** | Adaptive graph learning of microbial phylogeny for host-phenotype prediction (*Appl Environ Microbiol*) | 3 — AI/ML, Biomarker, Microbiome | **absent — never retrieved** |
| **42627334** | β-cell function 1 year after **stopping** oral baricitinib in T1D (*Diabetes Care*) | 2 — T1D Immuno, baricitinib | correct, 2 domains |

**42610933 and 42627334 are the two to read this week.** Metabolite prediction of teplizumab
response is Tier 1 area #1 executed on a Tier 1 area #3 asset; the baricitinib withdrawal paper is
the durability question for the two Lilly Phase 3s now recruiting. **42390946 remains the standing
recommendation from 08-31 and is still unread by the pipeline.**

### Key therapies

`zimislecel` returned **0 papers again** — at least the fifth consecutive check (08-27, 08-28
snapshots; 08-30, 08-31 live; today).

**I drafted a naming hypothesis here and I am retracting it before it reaches you.** My first pass
argued the term list tracks the INN while the registry uses "VX-880", and recommended adding the
code to `KEY_THERAPY_TERMS`. The 08-31 report already tested and rejected that: the corpus
*already holds* PMID 40544428, the NEJM zimislecel paper, so the term is not the failure point.
08-30/08-31 root-caused it to ingestion, and the standing fix is a join of `therapy_hits` against
`paper_library/index.json`. **That fix stands; my term-expansion suggestion was wrong and would
have wasted a cycle.** **[Certain]** — 08-31 report, lines 236–238.

Otherwise flat: orforglipron 12, retatrutide 10→8, CagriSema 4→3, baricitinib 3→2, teplizumab 4,
icodec 6→8, dapagliflozin 34→32. All within window-slide noise.

---

## Gap analysis

No re-run since 2026-07-17. Below are the top five of the **"potentially meaningful"** subset —
*not* the raw ranking. In `ranked_gaps` these sit at **#3–#7**; positions #1 and #2 (GWAS/Polygenic
× Closed Loop AP, Drug Repurposing × CGM Technology, both 100.0 / 0 joint) were filtered out as
methodologically distinct. All remain **BRONZE** (single analytical source, expert confirmation
pending) per the Research Doctrine:

| Meaningful-set rank | Intersection | Gap score | Joint pubs | Tier 1 alignment |
|---|---|---:|---:|---|
| 1 (raw #3) | Treg / CAR-T × Neuropathy | 100.0 | 0 | — |
| 2 (raw #4) | Beta Cell Regen × Health Equity | 100.0 | 0 | **#6 Epidemiological / equity** |
| 3 (raw #5) | Treg / CAR-T × Health Equity | 100.0 | 0 | **#6** |
| 4 (raw #6) | Glucokinase × Health Equity | 100.0 | 0 | **#6** |
| 5 (raw #7) | Gene Therapy × LADA | 100.0 | 0 | **#2 Literature synthesis** |

*(Tier 1 mapping note: 08-31 mapped the Treg/CAR-T axis to Tier 1 #2. I have not carried that
across — these mappings are judgment calls about fit, not doctrine text, and the two runs disagree.
Worth one human decision rather than a third opinion from a monitor.)*

Three of the top five run through **Health Equity**, whose 2020+ individual count is 1,990 — the
**10th-lowest** of 30 domains (below it: Islet Transplant 248, LADA 582, Drug Repurposing 609,
Personalized Nutr 661, Glucokinase 854, Treg/CAR-T 953, Beta Cell Regen 1,463, Multi-Omics 1,694,
Closed Loop/AP 1,906). It is low, but not the outlier a first look suggests — and it is low
*alongside* the very domains it pairs with in gaps #2–#4, which is exactly the shape a shared
query-narrowness artifact would produce. The 08-31 report flagged the circularity risk and it is
still unrun:
**if the Health Equity query is narrow, it depresses both the individual count and every pairwise
count, manufacturing gap scores wherever it appears.** Until that is tested, treat gaps #2, #3 and
#4 as *unvalidated by construction*, not merely BRONZE. This is the cheapest open item in the
folder and it has now been carried for two days.

---

## Breaking news

**Nothing new since the 08-31 report.** Four searches run. The one August action —
**FDA approval of Mounjaro (tirzepatide) to reduce MACE in high-risk adults with T2D, 2026-08-28** —
was already captured on 08-31. No FDA action, Phase 3 topline, or major publication landed
2026-08-29 → 09-01. Vertex's zimislecel regulatory submission remains *expected* in 2026 with no
decision announced. **[Likely]** — negative result from four searches; absence of news is weaker
evidence than presence of it.

The only substantive event in the window came from the registry, not the press: the ladarixin
futility readout above. Nobody wrote it up.

---

## Recommended actions

**P0 — restart the acquisition arm.** 46 days. Everything else in this list is downstream of it.
```
python baseline_clinical_trials.py
python baseline_pubmed_alerts.py
python hub_monitor.py
```

**P0 — raise `retmax` in `baseline_pubmed_alerts.py`.** Replicated twice now; the verification
condition 08-31 set has been met. Two edits:

- **line 66** — `def search_pubmed(query, max_results=10, ...)` → `max_results=300`. This default
  is what the 16 domain queries use; line 205 calls it with no `max_results` argument.
- **line 233** — `search_pubmed(query, max_results=5, ...)` → `max_results=300` for the 8 therapy
  queries.

Expect ~850–1,000 PMIDs per window instead of ~160, and ~115 cross-domain papers instead of ~17.
Re-run the last four snapshots at the new setting before making any longitudinal literature claim
from this series.

**P1 — add the missing trial statuses.** Append a sixth query to `baseline_clinical_trials.py`:
`AREA[Condition](diabetes) AND AREA[OverallStatus](TERMINATED OR SUSPENDED OR WITHDRAWN) AND
AREA[ResultsFirstPostDate]RANGE[2025-01-01, MAX]` — 32 trials today, 12 of them Phase 2/3.
Early stops are findings.

**P1 — triage drops on `UNKNOWN`.** Before reporting a dropped trial, re-query it; if
`overallStatus == UNKNOWN`, label it *aged out*, not *changed*. Removes ~5 of 6 weekly false alarms.

**P1 — test the Health Equity query for circularity.** Re-run the individual count with a broader
term set (add `disparities`, `social determinants`, `access to care`, `underserved`) and see whether
1,990 moves. If it does, gaps #2/#3/#4 are artifacts and the top of the gap ranking is wrong.
Cheapest open item in the hub. Carried two days.

**P2 — read these three.** PMID **42610933** (metabolite prediction of teplizumab response),
**42627334** (β-cell function after stopping baricitinib), **42390946** (EXSCEL proteomic CV score,
outstanding from 08-31).

**P2 — update the tracker** with NCT04628481 as a *null* Phase 2 result in T1D β-cell
preservation. (The zimislecel zero is **not** a term-list problem — see PubMed section; the
standing 08-30/08-31 fix, joining `therapy_hits` against `paper_library/index.json`, is still the
right one.)

**P2 — re-run the gap analysis.** `python project1_literature_gap_analysis.py` — data is 45 days
old, and fix the report header so it prints the *data* date, not the render date.

---

## Evidence levels (per Research Doctrine)

| Claim | Level | Basis |
|---|---|---|
| `retmax` ceiling costs ~85% of cross-domain signal | **[Certain]** | Independently replicated, 2 windows; cross-domain lines agree within 1 paper, PMID totals within 0.8% |
| Which papers the ceiling drops is non-deterministic | **[Likely]** | Two `retmax=10` runs, same window, 20 min apart, different sets (n=2 runs) |
| Ladarixin failed its primary endpoint / stopped for futility | **[Certain]** | CT.gov results section, group values + ANCOVA read directly |
| TERM/SUSP/WDRW trials invisible to hub; 32 with results | **[Certain]** | Script query text + 5 live `countTotal` queries |
| 5 of 6 dropped trials are the 2-year UNKNOWN auto-flip | **[Certain]** | Six individual live queries |
| PubMed domain declines are window-slide, not slowdown | **[Certain]** | Window bounds in snapshot metadata |
| Acquisition arm down 46 days | **[Certain]** | mtimes + `acquired_by` metadata + git log |
| `literature_gap_report.md` header misstates data age | **[Certain]** | Header vs body vs source JSON |
| zimislecel 0-hits are an ingestion defect, not a term-list defect | **[Certain]** | 08-31 report; corpus already holds PMID 40544428 |
| No breaking news 08-29 → 09-01 | **[Likely]** | Four searches, negative result |
| Health Equity gap scores are circular | **[Guessing]** | Plausible mechanism, **untested** — this is why it's a P1 |

Gap classifications remain **BRONZE**. The ladarixin result is Level 2 evidence (randomised
controlled Phase 2, registry-posted, not yet peer-reviewed) — **SILVER at best until a publication
appears**; do not cite it as GOLD on the strength of the registry alone.

---

## Self-audit

- **I wrote files, and the 08-31 run deliberately did not.** Two new dated snapshots
  (`clinical_trials_snapshot_2026-09-01.json`, `pubmed_recent_snapshot_2026-09-01.json`) plus this
  report. No existing file was modified, renamed or deleted; in particular `*_latest.json` were
  left at their 07-17 state so the acquisition arm's outage stays visible. My reasoning: the last
  snapshot was 4 days old and a change report with no current snapshot to diff against is a report
  about nothing. **If the charter means "write nothing at all," this was the wrong call and it is
  trivially reversible** — delete the two JSONs.
- **My snapshots carry the defect I am reporting.** I used `retmax=10` for comparability with
  08-27/08-28. That was a deliberate trade — comparability over completeness — and it means the
  09-01 snapshot understates cross-domain papers by ~85%. Do not treat it as a corrected baseline.
  It also uses `retmax=10` for the therapy queries where the production script uses 5, so it is
  not byte-identical to what `baseline_pubmed_alerts.py` would have written either.
- **The two scripts I ran are not in the hub.** `acquire_snapshots.py` and `ceiling_test.py` live
  in the sandbox outputs folder, not `Analysis/Scripts/`, so this run is not reproducible from the
  repository. If the `retmax` and status-filter fixes land in the real scripts, that stops
  mattering; until then, the 08-27/08-28/09-01 snapshots have no checked-in provenance.
- **I closed a verification the previous run left open, and it survived.** That is the useful
  outcome here, but note the failure mode it hides: two runs of the *same code path by the same
  kind of agent* is weaker than two independent implementations. A human re-running the recipe
  would be worth more than my replication.
- **My first draft of this report had 14 errors and an adversarial check caught them.** The ones
  that would have cost you something: I said Health Equity was the *third*-lowest domain count
  (it is **10th**), which was the strongest-sounding support for the circularity argument and was
  simply wrong. I labelled two PMIDs "typed 1-domain" when the snapshot never retrieved them at
  all. I claimed agreement with 08-31 "within 1 paper on every line" when two lines differ by 2
  and 8. I cited the wrong line number for the `retmax` fix. And **I re-proposed the zimislecel
  term-expansion that 08-31 had already tested and rejected** — the exact "found, lost, re-derived"
  failure that report's recommendation #9 warns about. All are corrected above. The lesson is not
  that I caught them; it is that a monitor without an adversarial pass ships them.
- **Zero new trials in four days is still slightly odd** even after the UNKNOWN explanation. The
  registry-wide feed shows 3 brand-new diabetes registrations since 08-29, none of which match the
  hub's five category filters. That is consistent with narrow filters rather than a broken feed,
  but I did not test it hard enough to rule out a pagination truncation at 10 pages × 100.
  **Unresolved.**
- **The ladarixin difference is not statistically significant** (p = 0.196, CI crosses zero). I
  have called it a null result, not a harm result. If anyone summarises this as "ladarixin was
  worse than placebo," that is my table being misread — the point estimate favours placebo, the
  interval does not exclude the opposite.
- **The 32-trial blind spot is a count, not a reading.** I have read exactly one of those 32. The
  other 31 may be mostly enrolment failures and business terminations with nothing in them. The
  claim I am defending is that the hub cannot see them, not that they are all valuable.
- **Still unrun after two days:** the Health Equity circularity test. It undermines three of the
  top five gaps and takes minutes. Its continued absence is the weakest point in this report.

---

## Sources

- ClinicalTrials.gov API v2 — <https://clinicaltrials.gov/api/v2/studies>
  (5 category queries → 887-trial snapshot; 38-record event feed `LastUpdatePostDate ≥ 2026-08-29`;
  6 individual drop queries; NCT04628481 / NCT07030868 / NCT07794254 full records; 5 blind-spot counts)
- PubMed E-utilities esearch/efetch — <https://eutils.ncbi.nlm.nih.gov/entrez/eutils/>
  (24 alert queries × 2 `retmax` settings × 2 windows = 96 searches; 160-paper snapshot).
  Run via two sandbox scripts, `acquire_snapshots.py` and `ceiling_test.py` — **not checked in.**
- Local: `clinical_trials_snapshot_2026-08-27.json`, `clinical_trials_snapshot_2026-08-28.json`,
  `pubmed_recent_snapshot_2026-08-28.json`, `literature_gap_data.json`, `literature_gap_report.md`,
  `hub_monitor_report.md`, `monitor_report_2026-08-31.md`, `RESEARCH_DOCTRINE.md`,
  `Analysis/Scripts/baseline_clinical_trials.py`, `Analysis/Scripts/baseline_pubmed_alerts.py`, git log
- FDA / Eli Lilly — Mounjaro CV risk-reduction indication, approved 2026-08-28
  <https://investor.lilly.com/news-releases/news-release-details/fda-approves-lillys-mounjaro-tirzepatide-reduce-cardiovascular>
- Vertex Pharmaceuticals — zimislecel pipeline status
  <https://news.vrtx.com/news-releases/news-release-details/vertex-presents-positive-data-zimislecel-type-1-diabetes>

---
*Automated review run — 2026-09-01. No existing file modified.*
