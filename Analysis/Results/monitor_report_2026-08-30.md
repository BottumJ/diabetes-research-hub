# Diabetes Research Hub — Monitor Report

**Run:** 2026-08-30 (Sunday) · automated review run
**Scope:** Analysis/Results file review + live ClinicalTrials.gov event feed + live PubMed term tests + web check
**Files modified:** none (this report is the only new file)

---

## Headline: a standing P1 recommendation is wrong, and I can now show it

For three consecutive days (08-27, 08-28, 08-29) this monitor has recommended widening the
key-therapy alert term to `zimislecel OR "VX-880"`, describing it as "one line of code" to fix the
hub's blindness to its own headline asset. **I ran that query today. It returns zero. The
recommendation would have changed nothing.**

| Query actually run against PubMed today | Count |
|---|---:|
| `diabetes AND zimislecel AND 2026/07/29:2026/08/28[edat]` — current alert form | **0** |
| `diabetes AND (zimislecel OR "VX-880") AND [same window]` — the recommended fix | **0** |
| `diabetes AND zimislecel` — no date window | 3 |
| `diabetes AND (zimislecel OR "VX-880")` — no date window | **7** |

The zero was never a term-mismatch. It is the **30-day `[edat]` window**. All seven zimislecel/VX-880
papers were indexed between 2025-07 and 2026-04; none fall inside any recent 30-day window, so no
term expansion can surface them. **[Certain]** — all four counts run live today, reproducible.

The diagnosis in the 08-29 evidence table — *"Zimislecel literature invisible due to term mismatch,
[Likely]"* — is now **[Certain] false as stated**. The term widening is still mildly worth doing
(3 → 7 on the unwindowed corpus) but it is a P3 cleanup, not the P1 it has been ranked as.

**And the premise behind it was also wrong.** The hub is *not* blind to zimislecel. The pivotal
NEJM paper is already in the corpus:

> **PMID 40544428** — *Stem Cell-Derived, Fully Differentiated Islets for Type 1 Diabetes.*
> N Engl J Med, 2025-09-04. Present at `Analysis/Results/paper_library/abstracts/40544428.json`,
> and in `index.json`, `evidence_network.json`, `gap_evidence.json`, `pmid_verification.json`.

The **alert channel** is blind; the **corpus** is not. Those are different failures with different
fixes, and conflating them sent three days of P1 effort at the wrong one.

*The real gap:* the therapy alert has no "have we ever ingested this?" check. It answers "what is new
in 30 days," and is being read as if it answered "what does the hub know." A one-line join of
`therapy_hits` against `paper_library/index.json` would have caught this on 08-27.

---

## Second finding: I resolved the Sana question, and it is a real hole

08-29 rated the Sana absence **[Guessing]** and recommended an `AREA[CollaboratorName]` query.
I ran it. **The trial exists and the hub cannot see it.**

> **NCT06239636** — *First-in-human Safety Study of Hypoimmune Pancreatic Islet Transplantation in
> Adult Subjects With Type 1 Diabetes*
> Status **RECRUITING** · EARLY_PHASE1 · n=2 · first posted 2024-02-02 · intervention **UP421**
> **Lead sponsor: Per-Ola Carlsson** (Uppsala) — **Sana Biotechnology is a *collaborator*, not lead.**

Three independent reasons the hub's queries miss it, all confirmed live:

1. Sponsor queries match **lead sponsor only** → Sana never matches.
2. Its condition string is `Type1diabetes` — **one token, no spaces** → condition-text matching fails.
3. It is **absent from the 893-trial 08-28 snapshot**. Verified by set membership, not inference.

This is the allogeneic-islet-without-immunosuppression trial — the one program on a different
scientific axis from Vertex's (which still requires ongoing immunosuppression). It is directly
adjacent to **PMID 42626948** (gene-edited hypoimmune islets), already queued for reading. **[Certain]**

*Note:* NCT06239636 was named in the 08-27 and 08-28 reports and then dropped out of 08-29. Findings
are being re-derived and lost rather than carried. That is a workflow defect, not a data defect.

---

## The structural problem: the pipeline is running on one lung

```
                              Jul 17                            Aug 30
                                 │                                 │
 REPAIR / QUALITY ARM            ├─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─●─┤  daily, 44/44 days
   validate_citations.py         │                                 │
   verify_pmids.py               │                                 │
   repair_*_20260829.py          │                                 │
                                 │                                 │
 DATA ACQUISITION ARM            ●                             ○ ○ │  last run Jul 17
   baseline_clinical_trials.py   │                                 │  (○ = sandbox stopgap 8/27–8/28)
   baseline_pubmed_alerts.py     │                                 │
   gap_analysis_daily.py         │                                 │
   hub_monitor.py                │                                 │
                                 └──────────── 44 days ────────────┘
```

Git log confirms an unbroken run of daily quality iterations through 08-29 (citation repair, design
grading, provenance fixes). Over the same 44 days the four acquisition scripts have not run once
locally. **The hub has been polishing the citations of a corpus it stopped feeding.** **[Certain]** —
git log + script/output mtimes.

That reframes the `*_latest.json` flag, now on its **fourth consecutive day**. It is not a file-writing
bug. It is the visible symptom of the acquisition arm being down, and it will not be fixed by
anything except running the pipeline.

### File system status

| File | Modified | Age | Status |
|---|---|---:|---|
| `clinical_trials_snapshot_2026-08-28.json` | 08-28 08:24 | 2d | current |
| `pubmed_recent_snapshot_2026-08-28.json` | 08-28 08:28 | 2d | current |
| `Research_Findings_Summary.md` | 08-29 03:20 | 1d | current |
| `literature_gap_report.md` | 08-29 03:20 | 1d | **misleading — data is 44d old** |
| `clinical_trials_latest.json` | 07-17 02:05 | **44d** | **stale** |
| `pubmed_recent_latest.json` | 07-17 02:06 | **44d** | **stale** |
| `hub_monitor_report.md` | 07-17 02:16 | **44d** | **stale** |
| `Diabetes_Research_Tracker.xlsx` | 07-17 10:07 | **44d** | **stale** |
| `literature_gap_data.json` | 07-18 03:11 | **43d** | **stale** |

`literature_gap_report.md` stamps *"Generated: 2026-08-29 03:20"* while its own body reads
*"Date range: 2020/01/01 to 2026/07/17"* and `literature_gap_data.json` carries
`generated: 2026-07-17T10:14:41`. **Seventh consecutive day flagged.** **[Certain]** — three
timestamps read directly.

---

## Clinical trial changes — live event feed, run today

I built and ran the NCT event feed that has been P0/P1 for three days. **893/893 tracked NCTs
resolved, zero fetch failures, ~25 seconds.** It is 18 batched API calls; it is not a large project.

| Live check vs. 08-28 snapshot | Result |
|---|---:|
| Status changes | **0** |
| Newly posted results | **0** |
| `whyStopped` newly populated | **0** |
| Registry updates dated 08-29 or 08-30 | **0** |

The zero is real, and benign: ClinicalTrials.gov posts on business days, and 08-29/08-30 were
Saturday and Sunday. Last update activity was 08-28 (4 records), 08-27 (6), 08-25 (5), 08-21 (15).
**The 08-28 snapshot is not stale — it is complete through the last business day.** **[Certain]**

**This is the useful result.** Trial-side, the hub is current and the daily-diff anxiety of the past
week is unwarranted. The staleness that matters is on the PubMed and gap side.

### Results postings not yet in the tracker

22 tracked trials have posted results since 2026-07-15. The tracker was last written 07-17, so **21
of the 22 cannot possibly be logged.** **[Certain]** by mtime.

| Results posted | NCT | Sponsor | Phase | Trial |
|---|---|---|---|---|
| 2026-08-27 | NCT04506151 | Univ. of Illinois at Chicago | NA | Sleep Optimization for Glycemic Control in T1D |
| 2026-08-24 | NCT05530356 | Univ. of Colorado Denver | NA | Renal Hemodynamics, Energetics & Insulin Resistance |
| 2026-08-21 | **NCT04596631** | **Novo Nordisk** | **PHASE3** | **Oral semaglutide comparator study** |
| 2026-08-21 | NCT04876053 | Univ. of Arkansas | NA | Home Food Delivery for Rural Diabetes Management |
| 2026-08-19 | NCT06015685 | Emory | NA | Embedded Primary Care Multidisciplinary Diabetes Clinic |
| 2026-08-10 | NCT05035082 | Novo Nordisk | PHASE4 | RYBELSUS vs other glucose-lowering |
| 2026-08-10 | NCT05428943 | Op-T LLC | PHASE1 | OPT101 in Type 1 Diabetes |
| 2026-07-16 | NCT05086445 | Eli Lilly | PHASE1 | LY3502970 (orforglipron), Japanese participants |

*(remaining 14 are academic/behavioral NA-phase; full list reproducible from the feed)*

**NCT04596631** is the one to log first — Novo Nordisk, Phase 3, results nine days old, unrecorded.

### Phase 3 recruiting — 57 trials; the T1D cure axis

| NCT | Sponsor | Status | Note |
|---|---|---|---|
| NCT04786262 | Vertex | RECRUITING | VX-880 / zimislecel, Phase 3 |
| NCT06832410 | Vertex | RECRUITING | VX-880 / zimislecel, Phase 3 |
| NCT07222332 | Eli Lilly | RECRUITING | Baricitinib, preserve beta-cell function |
| NCT07222137 | Eli Lilly | RECRUITING | Baricitinib, delay Stage 3 T1D |
| **NCT06239636** | **Carlsson / Sana** | **RECRUITING** | **UP421 hypoimmune islets — not in snapshot** |

Newest Phase 3 entrants (first posted August): NCT07754461 Boehringer survodutide (08-10),
NCT07743983 BrightGene BGM0504 (08-04), NCT07743450 Ascletis ASC30 oral (08-03).
AstraZeneca has stood up **five** elecoglipron Phase 3s in a single week (06-23/06-24) — a program
build-out the hub has not characterised.

### New registrations the category queries missed

6 diabetes studies were first-posted 08-27/08-28; **none entered the snapshot.** All are
behavioral/education/device (Sultan Qaboos telehealth, Toronto nutrition video, Wayne State VR,
WVU ENLIGHT ESG, CGM outcomes, Taiwan precision education). Individually low priority — but 6/6
missed confirms the category filters are narrow, consistent with the NCT06239636 hole.

---

## PubMed highlights — 08-28 snapshot (30-day window, 163 papers)

**Nothing new since.** Live check of all seven tracked therapies over 08-28→08-30 returns 0 new
papers except tirzepatide (2: PMIDs 42666183, 42660161 — routine, no Phase 3 readout).

### Cross-domain papers — 16 of 163

Highest value, unchanged from 08-29's queue and still unread:

| PMID | Domains | Journal | Paper |
|---|---|---|---|
| **42626948** | 4 (Stem Cell / Immunotherapy / Gene Therapy / teplizumab) | Expert Opin Biol Ther | Gene-edited hypoimmune islets as a cure for T1D |
| 42613697 | 3 | Recent Adv Inflamm Allergy Drug Discov | Regenerative approaches in T1D: β-cell replacement |
| 42627334 | 2 (Immunotherapy / baricitinib) | **Diabetes Care** | β-cell function 1 year after **stopping** oral baricitinib |
| 42610933 | 2 (Immunotherapy / teplizumab) | **Diabetes** | Baseline metabolites predict teplizumab response |
| 42636140 | 2 | Human Gene Therapy | Engineering HSPCs for antigen expression in APCs |
| 42643804 | 2 | Ther Adv Endocrinol Metab | Teplizumab in stage 2 T1D — pediatric |

**42626948 is now doubly urgent:** it is the literature counterpart to NCT06239636, the Sana trial
found today. Read them as a pair.

### Key therapies (08-28 snapshot, 30-day window)

| Therapy | Hits | | Therapy | Hits |
|---|---:|---|---|---:|
| dapagliflozin | 34 | | icodec | 6 |
| orforglipron | 12 | | CagriSema | 4 |
| retatrutide | 10 | | teplizumab | 4 |
| baricitinib | 3 | | **zimislecel** | **0 — window artifact, see headline** |

### Volume caveat, restated

45 of 163 papers are "new" vs the 08-27 snapshot on a window that moved **one day**, and ~49 dropped
out. This is `retmax` resampling, not publication activity. **No longitudinal literature claim should
be made from these snapshots until retmax sampling is fixed.** Carried from 08-29; still open.
Domain counts saturate at exactly 10 for 15 of 23 domains — the ceiling, not a measurement.

---

## Gap analysis summary

**The underlying data is 44 days old** (`literature_gap_data.json`, generated 2026-07-17) regardless
of the report's 08-29 stamp. 372 ranked pairs, 30 domains.

### Top 5 by gap score

| # | Pair | Gap | Joint | Expected |
|---|---|---:|---:|---:|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 | 7.53 |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 | 7.28 |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 | 4.74 |
| 4 | Glucokinase × Health Equity | 100.0 | 0 | 4.25 |
| 5 | Gene Therapy × LADA | 100.0 | 0 | 3.34 |

*(GWAS×Closed-Loop and Drug Repurposing×CGM score 100.0 with higher `expected` but are correctly
classified methodologically-distinct — genomics vs. device engineering.)*

**The score still cannot rank these.** All five are exactly 100.0 with `pair_count = 0`; the ordering
is `expected` doing the work. Re-rank by `expected − joint`. Third consecutive recommendation; the
field is already in the file.

### Tier 1 alignment

Four of five touch **Health Equity** (Doctrine Tier 1 #6, 17/20) crossed with a cell/gene therapy
domain — *who gets access to the cures now in Phase 3*. Coherent, and it aligns with Tier 1 #2
(Literature Synthesis, 19/20) and #3 (Clinical Trial Intelligence, 18/20).

**Still do not commit.** Health Equity rests on a query returning 1,990 publications; the 19-term
expansion recommended on 08-28 has not run. Four of five top gaps hang on a known under-specified
string. **[Likely]** they survive expansion — 0 joint publications is a large hole — but "likely" is
below the Doctrine's bar for a Tier 1 commitment. Expand, re-run, *then* rank.

Note the convergence worth watching: **Gene Therapy × LADA** (#5) and the hypoimmune-islet axis
(NCT06239636 + PMID 42626948) are pointing at the same territory from two directions.

---

## Breaking news

**Nothing new in the last 48 hours.** Verified against ClinicalTrials.gov (0 weekend registry
activity), PubMed (0 new therapy papers), and web search.

The **Mounjaro (tirzepatide) CV indication, FDA-approved 2026-08-28** on SURPASS-CVOT (n>13,000,
MACE-3 HR 0.92, 95.3% CI 0.83–1.01, non-inferior to dulaglutide) was fully covered in the 08-29
report. **Not re-reported.** It remains an open tracker action against **NCT04255433**, whose results
have been on disk since 2026-07-08 — 53 days.

No FDA action, Phase 3 readout, or major publication dated 08-29 or 08-30 was found. Prior August
item, already logged: Garzulys (insulin aspart-fsan), NovoLog biosimilar, approved 07-30.

---

## Recommended actions

**P0**

1. **Run the acquisition pipeline locally. Day 44.** Everything below is downstream of this.
   ```
   cd C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts
   python run_daily_local.py
   ```
   Set `NCBI_API_KEY` first (3→10 req/sec). The gap step needs ~35–40 min and *cannot* run in the
   sandbox — that is why it is a local script.

2. **Fix the Sana/collaborator query hole.** NCT06239636 is a recruiting T1D cure trial invisible to
   the hub. Add `AREA[CollaboratorName]` to the sponsor queries and stop relying on condition-text
   matching (`Type1diabetes` tokenises as one word). Concrete, verified, one query change.

3. **Log NCT04596631** (Novo Nordisk Phase 3, results posted 08-21) and **NCT04255433**
   (SURPASS-CVOT CV indication) in the tracker. 21 results postings are currently unlogged.

**P1**

4. **Add an ingestion check to the therapy alerts.** Join `therapy_hits` against
   `paper_library/index.json` so a therapy already in the corpus never reports as absent. This is the
   actual fix for the zimislecel zero. **Replaces the term-widening recommendation, which is now
   demonstrated to be a no-op.**

5. **Adopt the NCT event feed.** Written and validated today: 893/893 in ~25 s, 18 batched calls,
   fields `OverallStatus / LastUpdatePostDate / ResultsFirstPostDate / WhyStopped`. Run it daily
   *before* the full snapshot pull; it is ~50× cheaper and catches the events that matter. Note the
   weekday/weekend pattern — expect legitimate zeros Sat/Sun and do not treat them as failures.

6. **Stop `literature_gap_report.md` stamping render time over 44-day-old data.** Seventh consecutive
   flag. Start at `gap_analysis_daily.py` and `refresh.ps1`.

7. **Widen the Health Equity query (19-term expansion), then re-rank gaps by `expected − joint`.**
   Both are prerequisites to any Tier 1 commitment on the equity axis.

8. **Fix PubMed `retmax` sampling** before any longitudinal literature claim. 15 of 23 domains are
   pinned at the ceiling.

9. **Carry a findings ledger between runs.** NCT06239636 was found on 08-27, repeated 08-28, lost on
   08-29, and re-derived today. Three of the last four reports spent effort on a question that had
   already been half-answered.

**P2 — reading queue**

10. **PMID 42626948** — gene-edited hypoimmune islets, *Expert Opin Biol Ther*. Four domains.
    **Read alongside NCT06239636.** Top of queue, third day running.
11. **PMID 42627334** — baricitinib 1 year after stopping, *Diabetes Care*. Directly informs the two
    recruiting Lilly baricitinib Phase 3s. Fourth recommendation.
12. **PMID 42610933** — metabolite predictors of teplizumab response, *Diabetes*.

---

## Evidence levels (per Research Doctrine)

| Claim | Level | Basis |
|---|---|---|
| Zimislecel alert zero is a date-window artifact, not term mismatch | **[Certain]** | 4 live PubMed counts run today; both windowed forms return 0 |
| NEJM zimislecel pivotal (40544428) already in hub corpus | **[Certain]** | file present at `paper_library/abstracts/40544428.json` + 8 indices |
| Term-widening recommendation is a no-op in-window | **[Certain]** | recommended query run verbatim; count 0 |
| NCT06239636 exists, RECRUITING, Sana as collaborator, absent from snapshot | **[Certain]** | ClinicalTrials.gov record fetched; set membership tested |
| 0 status changes / 0 new results across 893 NCTs since 08-28 | **[Certain]** | full live event feed, 893/893 resolved |
| Weekend zero is business-day pattern, not pipeline failure | **[Likely]** | update-date histogram shows weekday clustering; not confirmed against a registry calendar |
| Acquisition arm down 44 days while repair arm ran daily | **[Certain]** | git log 08-20→08-29 vs. script/output mtimes |
| 21 of 22 results postings unlogged in tracker | **[Certain]** | tracker mtime 07-17 precedes 21 posting dates |
| `literature_gap_report.md` renders 07-17 data under 08-29 stamp | **[Certain]** | 3 timestamps read directly |
| Mounjaro CV indication approved 2026-08-28 | **[Certain]** | Lilly investor release + 4 concordant outlets (logged 08-29) |
| Health Equity gaps survive query expansion | **[Likely]** | 0 joint pubs is a large hole; 19-term expansion still unrun |
| Category queries systematically miss behavioral/device registrations | **[Likely]** | 6/6 new 08-27/08-28 registrations absent; single 2-day sample |

---

## Sources

- ClinicalTrials.gov API v2 — event feed over 893 tracked NCTs; NCT06239636 full record; new
  registrations 08-27→08-30. <https://clinicaltrials.gov/api/v2/studies>
- PubMed E-utilities — zimislecel/VX-880 term and window tests; therapy deltas 08-28→08-30.
  <https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi>
- Local: `clinical_trials_snapshot_2026-08-28.json`, `pubmed_recent_snapshot_2026-08-28.json`,
  `literature_gap_data.json`, `literature_gap_report.md`, `hub_monitor_report.md`,
  `monitor_report_2026-08-29.md`, `Analysis/Scripts/`, git log
- Eli Lilly — FDA approves Mounjaro to reduce CV risk in T2D (logged 08-29)
  <https://investor.lilly.com/news-releases/news-release-details/fda-approves-lillys-mounjaro-tirzepatide-reduce-cardiovascular>
- BioPharm International — FDA approves Mounjaro on SURPASS-CVOT
  <https://www.biopharminternational.com/view/fda-approves-mounjaro-to-lower-cardiovascular-risk-in-type-2-diabetes-based-on-surpass-cvot>
- Vertex — T1D portfolio program updates (zimislecel regulatory timeline)
  <https://investors.vrtx.com/news-releases/news-release-details/vertex-announces-program-updates-type-1-diabetes-portfolio>

---

## Self-audit

- **No existing file was modified.** This report is the only write. Review-only run, per charter.
- **Live queries were read-only** (ClinicalTrials.gov GET, PubMed esearch/esummary). No snapshot was
  written, so no 08-30 snapshot exists; all snapshot-derived figures are from 08-28 and are labelled
  as such. The event-feed diff *is* current as of today.
- **I contradicted a prior finding of this monitor and should be checked on it.** The 08-29 report
  rated the zimislecel term-mismatch diagnosis [Likely]; I rate it [Certain] false. The four counts
  in the headline table are the whole basis — re-run them before acting.
- **The window claim was verified at source, not inferred.** `baseline_pubmed_alerts.py` line 233
  calls `search_pubmed(f'diabetes AND {therapy}', max_results=5, days_back=LOOKBACK_DAYS)` with
  `LOOKBACK_DAYS = 30` (line 29) and `datetype: "pdat"` (line 76). I re-ran both zimislecel forms
  using **pdat** over the snapshot's exact window (2026/07/29–2026/08/28): both return **0**. The
  finding holds under the script's own parameters, not just the `edat` form I tested first.
- One cosmetic defect noticed in passing: line 324 of that script prints *"tracked by name across all
  PubMed abstracts (not just titles)"* — accurate for esearch's default all-fields behaviour, but the
  wording invites exactly the misreading that produced the term-widening recommendation. Consider
  restating it as "within the 30-day window."
- **The weekend explanation is [Likely], not [Certain].** Zero registry activity on a Sat/Sun fits
  the weekday histogram, but I did not verify against a ClinicalTrials.gov posting calendar. If
  Monday 08-31 also returns zero, the feed itself is suspect.
- **Sana's absence is now resolved; Sana's *coverage* is not.** I found one collaborator trial. I did
  not enumerate whether other key organizations are similarly hidden behind collaborator roles. That
  audit is unrun.
- The 6 missed new registrations are a 2-day sample. Do not generalise the "narrow filters" claim
  without a longer window.
