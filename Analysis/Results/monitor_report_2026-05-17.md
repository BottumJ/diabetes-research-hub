# Diabetes Research Hub — Monitor Report
**Generated:** 2026-05-17 (automated scheduled run)
**Comparison window:** 2026-05-10 → 2026-05-17 (last 7 days)
**Previous monitor report:** monitor_report_2026-05-16.md

---

## File System Status

All four expected pipeline outputs are present and fresh (regenerated within the last 24 hours by hub_monitor.py at 07:05 today).

| File | Size | Last modified | Status |
|------|------|---------------|--------|
| `hub_monitor_report.md` | 2.2 KB | 2026-05-17 07:05 | Fresh |
| `clinical_trials_latest.json` | 534.8 KB | 2026-05-17 07:05 | Fresh |
| `pubmed_recent_latest.json` | 115.9 KB | 2026-05-17 07:05 | Fresh |
| `literature_gap_data.json` | 128.7 KB | 2026-04-20 15:35 | **STALE — 27 days old** |
| `literature_gap_report.md` | 11.4 KB | 2026-05-16 08:10 | Fresh (report was regenerated, underlying JSON was not) |

Hub-wide signal from `hub_monitor.py`:
- 832 files tracked, 2 new (today's daily snapshots), 6 modified, 0 removed.
- Flag from the script: **575 result file(s) older than 14 days — may need refresh.** This number is consistent with the long tail of one-off analyses (islet repurposing, microbiome ML, validation reports) that are not on the daily refresh cadence and is not necessarily actionable on its own.

---

## Clinical Trial Changes (2026-05-10 → 2026-05-17)

Snapshot deltas computed by diffing `clinical_trials_snapshot_2026-05-10.json` against `clinical_trials_snapshot_2026-05-17.json`. Total trials tracked: 795.

### New trials added (11)
The week-over-week diff added 11 trials; the most notable are:

- **NCT07581197** — Seraxis, Phase 1/2, NOT_YET_RECRUITING — Study of the Safety and Efficacy of Pancreatic Endocrine Cells in Adult Patients (T1D cell-therapy domain — direct competitor / parallel to VX-880/VX-264).
- **NCT07579702** — Insulet Corporation — Efficacy of the Omnipod® 6 System Compared With the Omnipod® 5 System (next-gen AID device head-to-head).
- **NCT07581145** — Phase 3, RECRUITING — Effect of Semaglutide on Healing of Foot Ulcers in T2D Patients (GLP-1 repurposing into complications space).
- **NCT07585630** — Phase 2 — RCT of A1Cantus vs. Placebo (UC Riverside).
- **NCT04333823** — SickKids, Phase 3, ACTIVE_NOT_RECRUITING — SGLT2i in adolescent T1D (ATTEMPT trial; previously tracked under a different ID by the API).
- Several completed/legacy trials (NCT04226027, NCT05454891, NCT02107976, NCT04286555, NCT05514535) were re-indexed because results were just posted (see below).

### Status changes (2)
- **NCT07059377** NOT_YET_RECRUITING → RECRUITING — Semaglutide for Smoking Cessation in Patients With Diabetes.
- **NCT07379333** NOT_YET_RECRUITING → RECRUITING — HM11260C in Patients With T2D (Hanmi long-acting GLP-1 candidate).

### Results recently posted (5 in past 7 days, 19 in past 30 days)
Highest-priority recent postings:

- **NCT05514535** (Novo Nordisk, Phase 3, posted 2026-05-11) — Semaglutide + lower-dose insulin glargine vs. semaglutide or glargine alone in T2D. **Worth pulling outcome data into the tracker.**
- **NCT05823948** (Novo Nordisk, Phase 3, posted 2026-04-30) — Flash glucose measurements with once-weekly insulin icodec.
- **NCT05649137** (Novo Nordisk, Phase 3, posted 2026-04-27) — Semaglutide for excess weight and T2D weight loss outcomes.
- **NCT05454891** (UCSF, posted 2026-05-12) — Extended bolus for meals in a closed-loop system.
- **NCT04286555** (Johns Hopkins, posted 2026-05-13) — DASH for Diabetes.

### Key Phase 3 trials being watched (RECRUITING)
46 total Phase 3 RECRUITING trials in the corpus. Highest-impact for the hub's Tier 1 areas:

- **VX-880 / Vertex** — NCT06832410 (with kidney transplant) and NCT04786262 (standalone) both RECRUITING — directly relevant to the T1D Stem Cell Cure domain.
- **Baricitinib / Eli Lilly** — NCT07222137 (delay of Stage 3 T1D in at-risk children) and NCT07222332 (preserve beta-cell function in newly-diagnosed) — paired Phase 3 program in immunotherapy.
- **Teplizumab / Sanofi** — NCT07088068 — Phase 3 in pediatric patients.
- **Cadisegliatin / vTv Therapeutics** — NCT06334133 — glucokinase activator as T1D adjunct (relevant to the Glucokinase gap pairs flagged below).
- **Insulin icodec / Novo Nordisk** — NCT07076199 — Phase 3 in a new T2D population.

---

## PubMed Highlights (2026-05-10 → 2026-05-17)

- New papers added to the rolling 30-day window: **98**
- Papers dropped (rolled out of the 30-day window): per hub_monitor today's run, 3 dropped vs yesterday; over the week, the corpus grew from 140 to 148 papers.

### Cross-domain papers (highest synthesis value)
Ten of the 98 new papers tag multiple domains. Top picks:

- **Machine learning–driven identification of circulating biomarkers and therapeutic compounds for diabetic retinopathy** (Hum Genomics, May 14) — PMID 42129911 — spans AI/ML + Biomarker + Complications. **This is a triple-domain paper and a direct match for Tier 1 (Multi-Omics Biomarker Integration).**
- **Microbial dysbiosis in metabolic disorders: linking epigenomic regulation and pathological mechanisms** (Drug Discov Today, May 13) — PMID 42134452 — Microbiome + Multi-Omics.
- **Underperformance of ML algorithms predicting LOS / readmission in underrepresented cohorts after THA** (J Arthroplasty, May 13) — PMID 42134630 — AI/ML + Health Equity. (Caveat: orthopedic outcome paper, but its algorithmic-fairness lens is portable to diabetes prediction work.)
- **Novel GLP-1RA-like effects of Bafetinib** (Toxicol Appl Pharmacol, May 12) — PMID 42128231 — GLP-1 + Drug Repurposing — kinase inhibitor showing GLP-1 receptor agonist-like activity. Notable repurposing signal.
- **Recent Investigations on Pathogenesis, Biomarkers, Epigenetics, and Emerging Therapeutic Strategies in Diabetic Retinopathy** (J Ophthalmol, 2026) — PMID 42137619 — Biomarker + Complications synthesis review.

### Key therapy mentions in past 30 days
| Therapy | Papers | Notable item |
|---------|--------|--------------|
| dapagliflozin | 30 | SGLT2i CV outcome target-trial emulation (PMID 42132163) |
| teplizumab | 5 | Three new this week — including KCM Herold/Evans-Molina "New and emerging therapies in T1D" overview in JCI (PMID 42138080) and UK BSPED/ABCD consensus (PMID 42051156). |
| orforglipron | 4 | **ATTAIN-MAINTAIN Phase 3b in Nat Med (May 13, PMID 42120723)** — weight-loss maintenance data; high priority. |
| retatrutide | 3 | Lipid/metabolite profile data in JCEM (PMID 42135195); CKM-syndrome review. |
| icodec | 3 | Pooled safety analysis of ONWARDS 1–6 (Endocr Pract, PMID 42119975). |
| baricitinib | 2 | Off-target T1D-relevant work limited; mostly dermatology case reports. |
| CagriSema | 1 | Systematic review/meta-analysis vs. semaglutide monotherapy (Am J Cardiol, PMID 41759565). |
| zimislecel | 0 | No new mentions this period. |

### Publication volume trends (30-day rolling)
The pattern remains stable vs. last week: AI/ML (198), Biomarker (143), and T2D GLP-1 New (140) continue to dominate. LOW-activity domains (Diabetes Epigenetics 7, Drug Repurposing 6, LADA 5, GLP-1 Pharmacogenomics 1) show the same volumes as last week — these are the persistent under-publication signals that align with the gap analysis below.

---

## Gap Analysis Summary

Source: `literature_gap_report.md` (regenerated 2026-05-16). Underlying JSON (`literature_gap_data.json`) is 27 days old. Top 5 actionable gaps (BRONZE validation level — single analytical source):

1. **Beta Cell Regen × Health Equity** — Gap Score 100, 0 joint pubs. Regenerative therapies and access equity have no overlap.
2. **Insulin Resistance × Islet Transplant** — Gap Score 100, 1 joint pub. IR in islet-transplant recipients affects graft survival but is barely studied.
3. **Islet Transplant × Drug Repurposing** — Gap Score 100, 0 joint pubs. Computational screening of existing immunosuppressants for islet protection is unexplored.
4. **Islet Transplant × Health Equity** — Gap Score 100, 0 joint pubs. Center-limited availability with no equity research.
5. **Gene Therapy × LADA** — Gap Score 100, 0 joint pubs. LADA's autoimmune mechanism is a candidate for gene-therapy approaches with no crossover work.

Tier-1 alignment (per RESEARCH_DOCTRINE.md):
- Gaps #2 and #3 (both involving **Islet Transplant**) are direct matches for **Tier 1 Clinical Trial Intelligence** — the Vertex VX-880 and Seraxis NCT07581197 trials newly tracked above give us a corpus to anchor that synthesis on.
- Gap #5 (**Gene Therapy × LADA**) and the persistent low-volume LADA signal in PubMed (5 papers/30d) reinforce LADA as an under-served domain. Cross-reference with `extract_pmid_40598585.md` already in the hub.
- The new cross-domain **Drug Repurposing** signal (Bafetinib, PMID 42128231) is a concrete data point that nudges gaps #3 and #12 (Drug Repurposing × Health Equity) toward actionability.

---

## Breaking News (Web Check, Last 7 Days)

Two items worth surfacing; no Phase 3 readouts or FDA approvals landed in the last 7 days, but two near-term items are in the window:

1. **MannKind Afrezza pediatric expansion — PDUFA date May 29, 2026 (12 days out).** If approved, this would be the first needle-free inhaled insulin option for pediatric T1D/T2D patients. *Evidence level: regulatory calendar item (verified to PDUFA list). Worth queueing for monitoring on/around May 29.* ([Source](https://www.thecardiologyadvisor.com/news/fda-drug-approval-decisions-expected-in-may-2026/))
2. **Swedish stem-cell T1D mouse reversal study (ScienceDaily, May 6, 2026).** Pre-clinical animal data on improved stem-cell–derived insulin-producing cells; just outside the strict 7-day window but relevant to the T1D Stem Cell Cure domain. *Evidence level: pre-clinical / pop-press summary; locate primary publication before incorporating.* ([Source](https://www.sciencedaily.com/releases/2026/05/260505234620.htm))

No FDA new molecular entity approvals in diabetes in the last 7 days (Awiqli/icodec was approved March 26, 2026; Langlara insulin glargine biosimilar April 29, 2026 — both predate this window).

---

## Recommended Actions

In priority order:

1. **Refresh literature gap data.** `literature_gap_data.json` is 27 days old; the human-readable report was regenerated but the underlying counts are not current. → `Run: python project1_literature_gap_analysis.py` to bring the BRONZE-tier gap scores up to date before any further synthesis builds on them.
2. **Update tracker with newly posted Novo Nordisk Phase 3 results (NCT05514535, NCT05823948, NCT05649137).** Extract outcome tables into `Diabetes_Research_Tracker.xlsx` and the relevant Notes file.
3. **Add Seraxis NCT07581197 to T1D Cell Therapy tracking.** New competitor/parallel to VX-880; should be in the Vertex-anchored watch list.
4. **Pull primary references for the three high-priority cross-domain papers** (PMID 42129911, 42134452, 42128231) into `paper_library/abstracts/` and flag for synthesis under Tier 1 (Multi-Omics Biomarker Integration) and Drug Repurposing.
5. **Watchlist Afrezza PDUFA (May 29, 2026).** Add a check-in on or after that date to capture the regulatory outcome.
6. **Locate the primary publication for the Swedish stem-cell T1D reversal report** before drawing any inferences from the ScienceDaily summary; downgrade to "monitoring" status until a peer-reviewed source is identified.
7. **Two newly-RECRUITING trials to flag:** NCT07059377 (semaglutide for smoking cessation) and NCT07379333 (HM11260C, Hanmi long-acting GLP-1) — minor priority but worth a row in the tracker.

No file modifications were made by this run (review-only per task spec).

---
*Generated automatically by the Diabetes Research Hub monitor. Confidence levels noted per RESEARCH_DOCTRINE.md. Gap-analysis findings remain BRONZE until expert validation.*
