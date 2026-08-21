# Diabetes Research Hub — Monitor Report
**Run date:** 2026-08-21 (automated, review-only — no files modified)
**Prior monitor report:** 2026-07-16

---

## Headline: the pipeline has been dead for 35 days

Every data-collection script stopped producing output on **2026-07-17**. This is not a "some files are stale" situation — it is a total collection halt. Everything below is analysis of a month-old dataset, and should be read with that caveat attached.

### Freshness at a glance

```
File                            Last written    Age      Status
─────────────────────────────────────────────────────────────────
literature_gap_report.md        2026-08-20       1d      FRESH (see note)
agent_state.json                2026-08-20       1d      FRESH
validated_research_paths.json   2026-08-20       1d      FRESH
literature_gap_data.json        2026-07-18      34d      STALE ███████
hub_monitor_report.md           2026-07-17      35d      STALE ███████
clinical_trials_latest.json     2026-07-17      35d      STALE ███████
pubmed_recent_latest.json       2026-07-17      35d      STALE ███████
clinical_trials_snapshot_*      2026-07-17      35d      STALE ███████  (last dated snapshot)
pubmed_recent_snapshot_*        2026-07-17      35d      STALE ███████  (last dated snapshot)
```

**Note on `literature_gap_report.md`:** its header says `Generated: 2026-08-20 03:20`, but the body says `Date range: 2020/01/01 to 2026/07/17` and the underlying `literature_gap_data.json` carries `"generated": "2026-07-17T10:14:41"`. The report was **re-rendered** on 08-20; the data behind it was **not** re-queried. Treat the 08-20 timestamp as cosmetic. [Certain — verified by reading both files' metadata blocks.]

The last hub_monitor.py run itself flagged **827 result files older than 14 days**. That number is now materially worse.

**Fix first:**
```
python baseline_clinical_trials.py
python baseline_pubmed_alerts.py
python project1_literature_gap_analysis.py
python hub_monitor.py
```

---

## Two data-quality bugs worth fixing before the next run

**1. `has_results` is broken in the clinical trials collector.** [Certain]

In `clinical_trials_latest.json`, 858 trials:

| Field | Value |
|---|---|
| `has_results == True` | **0** |
| `results_posted` non-empty | **322** |
| Category "Diabetes Recently Completed with Results" | 321 trials |

The boolean is unconditionally `False` while the date string it should be derived from is populated 322 times. Any downstream logic keying on `has_results` — including the "New results posted" line in the hub_monitor snapshot diff — is silently returning zero. That diff reported `New results posted: 0` for 07-16→07-17; I cannot tell whether that's true or an artifact of this bug. Recommend deriving `has_results = bool(results_posted)` at parse time.

**2. PubMed domain counts are ceiling-capped at 10 and are not a volume signal.** [Certain]

13 of the 16 alert domains returned exactly 10 papers. That is a `retmax` cap, not research activity. Only three domains fell below the cap and therefore carry any information:

| Domain | Papers | Read as |
|---|---|---|
| Diabetes Drug Repurpose | 8 | below cap |
| Diabetes Epigenetics | 5 | below cap — thin 30-day window |
| GLP-1 Pharmacogenomics | 1 | below cap — near-silent |

The task brief asks for "domains with unusually high or low publication activity." With the current cap, **high activity is unmeasurable**. To get a real trend line, the collector needs to record `esearch` total `Count` alongside the capped record list.

---

## Clinical trials — 30-day change (2026-06-17 → 2026-07-17)

The daily 07-16→07-17 diff in `hub_monitor_report.md` is too narrow to be useful (1 new, 1 removed, 0 status changes). I ran a 30-day diff instead against the oldest still-comparable snapshot.

| Metric | Count |
|---|---|
| New trials | 62 |
| Removed trials | 17 |
| Status changes | 12 |
| New results posted | 1 |

**Corpus composition (858 trials):**

```
COMPLETED               321  ████████████████████████
RECRUITING              269  ████████████████████
NOT_YET_RECRUITING      151  ███████████
ACTIVE_NOT_RECRUITING   110  ████████
ENROLLING_BY_INVITATION   7  ▌
```

52 trials are Phase 3 + RECRUITING.

### Status changes worth noting

| NCT | Change | Sponsor / Trial |
|---|---|---|
| NCT01897688 | ACTIVE → **COMPLETED**, results posted 2026-06-18 | Northwestern — Phase 3 islet transplantation in non-uremic T1D |
| NCT06111586 | RECRUITING → ACTIVE_NOT_RECRUITING | Sanofi — Frexalimab, beta-cell preservation |
| NCT05866536 / NCT05180591 | RECRUITING → ACTIVE_NOT_RECRUITING | MGH — repeat BCG vaccination (adult + pediatric) |
| NCT05594563 | RECRUITING → ACTIVE_NOT_RECRUITING | TADPOL — polyamines in T1D |
| NCT07215312 | RECRUITING → ACTIVE_NOT_RECRUITING | Eli Lilly — LY3938577 |

**NCT01897688 is the single actionable trial event in the window** — a completed Phase 3 islet transplant study with results actually posted. Islet Transplant is also the lowest-volume domain in the gap analysis (248 publications since 2020), so a fresh Phase 3 readout there is disproportionately valuable.

### New Phase 3 entrants (last 30 days of data)

A cluster of **four new AstraZeneca Phase 3 elecoglipron trials** appeared simultaneously (NCT07662044, NCT07662109, NCT07662135, NCT07662213; a fifth, NCT07664553, is NOT_YET_RECRUITING). Combined target enrollment across the recruiting four is ~4,900. This is a full Phase 3 program launch and is not yet represented in the tracker.

Also new: NCT07668336 (Lilly, orforglipron vs. dulaglutide, Phase 3), NCT07670416 (Roche, enicepatide, Phase 3, n=300), NCT07659574 + NCT07653477 (United Bio-Technology, UBT251, Phase 3), NCT07670650 (U. Florida, PRISE, Phase 3), NCT07684144 (Amgen extension).

### Key-organization watchlist

| Sponsor | Trials in corpus | Notable |
|---|---|---|
| Eli Lilly | 33 | Baricitinib NCT07222332 + NCT07222137 both Phase 3 RECRUITING (beta-cell preservation and Stage 3 delay) |
| Novo Nordisk | 28 | CagriSema NCT07564414 Phase 3 RECRUITING n=2,500; icodec NCT07076199 Phase 3 RECRUITING n=877 |
| Vertex | 3 | VX-880/zimislecel NCT04786262 + NCT06832410 both Phase 3 RECRUITING; VX-264 NCT05791201 ACTIVE_NOT_RECRUITING |
| Sana Biotechnology | **0** | Not present in corpus at all — see below |

**Sana returns zero hits.** Sana's hypoimmune islet cell work (UP421 and successors) is squarely in scope for the "T1D Cure & Cell Therapy" category. Either their trials aren't indexed under the search terms `baseline_clinical_trials.py` uses, or the sponsor-name matching is missing them. Worth a manual ClinicalTrials.gov check before assuming there's nothing to track. [Likely — absence from a keyword-driven corpus is weak evidence of true absence.]

---

## PubMed highlights (30-day window ending 2026-07-17, 158 unique papers)

### Cross-domain papers — 12 of 158

Highest-value first (3-domain hits):

**[42459945] A framework for assessing algorithmic discrimination risks in training data: a case of pediatric type 1 diabetes.** *JAMIA open*, 2026-Aug.
Domains: Diabetes AI/ML × Closed Loop AP × Diabetes Health Equity.
This is the one to read. It sits directly on the Health Equity intersections that dominate the gap analysis, and Tier 1 of the Research Doctrine names literature synthesis across domains as a top contribution area.

**[42419792] Comparative effects of drugs for adults with overweight or obesity: systematic review and network meta-analysis.** *BMJ*, 2026-Jul-08.
Domains: orforglipron × retatrutide × CagriSema — a three-way head-to-head synthesis of the exact therapies on the watchlist.

Two-domain papers:

| PMID | Domains | Title (abbrev.) | Journal |
|---|---|---|---|
| 42411999 | Stem Cell Cure × Immunotherapy | T1D driven by residual recipient T cells after HCT (case report) | Diabetes Care |
| 42453334 | Biomarker × LADA | Noncoding RNAs for diabetes research and therapy | ACS Pharmacol Transl Sci |
| 42436543 | T2D Remission × Health Equity | Healthcare inequalities in T2D across COVID-19 | BMC Health Serv Res |
| 42458355 | AI/ML × Health Equity | Socioeconomic gradients in hypertension prevalence | BMC Public Health |
| 42452353 | GLP-1 × T2D Remission | Glucose-lowering therapy and myocardial work recovery post-STEMI | J Clin Med |
| 42459212 | Microbiome × Multi-Omics | Precision nutrition in Asian populations | J Nutr Sci |
| 42458730 | Microbiome × Multi-Omics | Multi-omic modelling of BMI response to weight loss | Gut Microbes |
| 42437645 | Pharmacogenomics × orforglipron | Variant-specific pharmacophoric shifts in GLP-1R–orforglipron | Int J Biol Macromol |
| 42394981 | orforglipron × retatrutide | Incretin therapies network meta-analysis | Front Pharmacol |
| 42444567 | retatrutide × CagriSema | Medical treatments for obesity: what's in store | JCEM |

Note the pattern: **the microbiome × multi-omics pair produced two independent cross-domain papers in a single 30-day window.** Multi-Omics Biomarker Integration is Tier 1 #1 in the Doctrine (19/20). This intersection is heating up, which cuts both ways — more relevant, but less of a gap.

### Key-therapy tracking

| Therapy | Papers | Notable |
|---|---|---|
| orforglipron | 5 | incl. drug-drug interaction characterization (*Clin Pharmacol Ther*) and a GRADE-assessed meta-analysis |
| CagriSema | 5 | **REIMAGINE 3** — CagriSema add-on to basal insulin in T2D, randomised double-blind, *Lancet* 2026-Jul-04 (PMID 42251856) |
| teplizumab | 4 | BSPED consensus statement on clinical use in Stage 2 T1D (*Diabet Med*); expanded-indication brief (*Med Lett*) |
| retatrutide | 4 | mostly preclinical this window (learning/memory in STZ rats) |
| baricitinib | 2 | **neither is diabetes-related** — a VEXAS syndrome case report (*Mod Rheumatol Case Rep*) and an RA drug-safety study (*Drug Safety*). The keyword filter is catching off-target rheumatology hits despite two Lilly Phase 3 baricitinib T1D trials actively recruiting. |
| **zimislecel** | **0** | zero hits — see below |

**Zimislecel returning zero is the anomaly to investigate.** [Likely] Vertex has two Phase 3 zimislecel trials recruiting in our own corpus, and the program is on an accelerated path toward 2026 global regulatory submissions. Zero publications in a 30-day window is plausible for a single INN, but the alert should probably also track **"VX-880"** and **"islet cell therapy"** as synonyms — the literature may be indexing it under the development code rather than the INN.

---

## Gap analysis — top intersections

Source data generated 2026-07-17; 30 domains, 435 pairs, 372 ranked. **Validation level: BRONZE** per Research Doctrine — single analytical source, expert confirmation not yet obtained.

### Top 5 meaningful gaps (script-classified as scientifically plausible)

| Rank | Intersection | Gap Score | Joint Pubs | Expected |
|---|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 | 7.5 |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 | 7.3 |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 | 4.7 |
| 4 | Glucokinase × Health Equity | 100.0 | 0 | 4.3 |
| 5 | Gene Therapy × LADA | 100.0 | 0 | 3.3 |

(6th: Drug Repurposing × Health Equity, 100.0, 0 joint. 7th: Insulin Resistance × Islet Transplant, 91.9, 1 joint.)

### Alignment with Tier 1 contribution areas

Doctrine Tier 1 #2 is **Literature Synthesis & Gap Analysis (19/20)** — "no one is systematically synthesizing across all 35 domains simultaneously." Four of the top six gaps share **Health Equity** as one axis, and Health Equity has only 1,990 publications since 2020 (10th-lowest of 30 domains, and the lowest among domains that intersect broadly with clinical practice). That is a coherent, defensible synthesis target: *equity analysis of emerging high-cost diabetes therapies* — spanning beta-cell regeneration, CAR-Treg, glucokinase activators, and drug repurposing in one paper.

**A caution against over-reading this.** [Likely] A gap score of 100.0 with an *expected* value of 3–7 papers is a weak signal. The formula's own denominator says we'd only expect a handful of joint papers even under normal cross-pollination; observing zero is roughly what you'd get from Poisson noise plus keyword mismatch. The genuinely informative rows are the ones with high expected counts and large shortfalls — e.g. Insulin Resistance × Closed Loop (expected 95, observed 3) and Neuropathy × Gestational DM (expected 120, observed 4), both sitting in the **Unclassified** bucket. Those deserve expert triage more than the 100.0 rows do.

---

## Breaking news (web check, last ~30 days)

Broader than 7 days because the local corpus is 35 days stale and the two windows need to connect.

**[Likely] Retatrutide TRIUMPH-2 and TRIUMPH-3 Phase 3 results, confirmed 2026-07-23.** TRIUMPH-2 (obesity + T2D, n=1,152): up to 20.8% weight loss, up to 1.6 pp HbA1c reduction at 80 weeks. TRIUMPH-3 (obesity + established CVD, n=1,949): up to 22.6% weight loss at 80 weeks. Sourced from secondary trackers, not the primary publication — verify against the Lilly release or the primary paper before entering in the tracker.

**[Likely] Novo Nordisk zenagamtide** presented at ADA 2026 — significant A1C reductions with up to 14.6% weight loss in T2D. **This compound does not appear anywhere in our key-therapy watchlist.** Candidate for addition.

**[Certain] Garzulys (insulin aspart-fsan)** approved 2026-07-24 — rapid-acting insulin biosimilar to NovoLog. Routine biosimilar approval; low research relevance, noted for completeness.

**[Likely] Insulin efsitora alfa** FDA decision possible in H2 2026 — would be the second weekly basal insulin approved in the US. Our corpus already holds four completed Lilly efsitora Phase 3 trials (NCT05462756, NCT05362058, NCT05662332, NCT05463744, NCT05275400). Worth a calendar flag.

**[Likely] Zimislecel** remains on an accelerated timeline toward global regulatory submissions in 2026, with RMAT + Fast Track (FDA), PRIME (EMA), and ILAP Innovation Passport (MHRA). Potential availability as early as 2027.

No FDA action, Phase 3 readout, or major publication in the last 7 days specifically that clears the "genuinely significant" bar.

---

## Recommended actions

**Priority 1 — restart collection (blocks everything else)**
1. Run `python baseline_clinical_trials.py` — trial data is 35 days old.
2. Run `python baseline_pubmed_alerts.py` — PubMed alerts are 35 days old; the 30-day lookback window means **days 2026-07-17 through 2026-07-22 will be permanently missed** if the next run uses the default lookback. Consider a one-time widened lookback (`--lookback_days 40`) to backfill.
3. Run `python project1_literature_gap_analysis.py` — gap data is 34 days old despite the report's misleading 08-20 header.
4. Run `python hub_monitor.py` last, so its diff sees the refreshed files.

**Priority 2 — fix collector bugs**
5. `has_results` → derive from `results_posted`; 322 trials currently misreported. Re-check the snapshot-diff "new results" logic after fixing.
6. Record `esearch` total counts, not just capped record lists, so domain volume becomes a real trend signal.
7. Add `VX-880` and `islet cell therapy` as zimislecel synonyms; scope the `baricitinib` query to diabetes context (both current hits are off-target rheumatology).
8. Add `zenagamtide` and `elecoglipron` to the key-therapy watchlist.

**Priority 3 — tracker updates**
9. Add the AstraZeneca elecoglipron Phase 3 program (NCT07662044 / 07662109 / 07662135 / 07662213, plus NCT07664553).
10. Add NCT01897688 (Northwestern islet transplant Phase 3, **completed with results posted 2026-06-18**) — highest-value single trial event in the window.
11. Manually verify Sana Biotechnology's ClinicalTrials.gov presence; if trials exist, fix the collector's search terms.

**Priority 4 — research follow-up**
12. Read PMID 42459945 (algorithmic discrimination in pediatric T1D training data) — 3-domain, on-thesis for Tier 1 synthesis work.
13. Read PMID 42251856 (REIMAGINE 3, *Lancet*) — CagriSema Phase 3 readout, primary literature.
14. Reclassify the high-expected-count gaps (Insulin Resistance × Closed Loop; Neuropathy × Gestational DM) out of "Unclassified" — they carry more statistical weight than the 100.0-score rows currently topping the list.

---

## Evidence levels for claims in this report

Per Research Doctrine v1.0:

| Claim class | Level | Basis |
|---|---|---|
| File timestamps, staleness, counts | **Certain** | Direct filesystem + JSON metadata reads |
| Trial IDs, statuses, sponsors, diffs | **Certain** | Parsed from `clinical_trials_latest.json` and dated snapshots |
| PubMed PMIDs, domains, journals | **Certain** | Parsed from `pubmed_recent_latest.json` |
| Gap scores and rankings | **Bronze** | Inherited from source analysis; single analytical source, unvalidated |
| Sana absence is meaningful | **Likely** | Absence from keyword corpus ≠ absence in reality |
| Zimislecel zero-hit is a query artifact | **Likely** | Plausible alternative: genuinely no publications in 30d |
| Web-sourced trial results (TRIUMPH-2/3) | **Likely** | Secondary trackers; primary source not verified |
| Garzulys approval | **Certain** | FDA source |

---

*Generated by scheduled monitor run — 2026-08-21. Review-only; no workspace files were modified.*
