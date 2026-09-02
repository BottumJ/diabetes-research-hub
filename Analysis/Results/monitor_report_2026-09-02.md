# Diabetes Hub Monitor — 2026-09-02 (Wednesday)

**Run type:** review only. No existing file was modified.
**Freshest data available:** 2026-09-01 snapshots. Nothing has been acquired today.
**Files read:** `hub_monitor_report.md`, `clinical_trials_latest.json`, `pubmed_recent_latest.json`, `literature_gap_data.json`, `literature_gap_report.md`, snapshots for 2026-08-27 / 08-28 / 09-01, `clinical_trials_summary.md`, `baseline_clinical_trials.py`, `RESEARCH_DOCTRINE.md`, `monitor_report_2026-09-01_iteration.md`.

---

## Headline: `has_results` is hardcoded to False by the collection script, and it has been for every script-generated snapshot in the hub.

Not a stale-data problem. A code defect. `baseline_clinical_trials.py` line 115 reads:

```python
"has_results": results_sec is not None,     # results_sec = study.get("resultsSection")
```

But the API request on lines 64–67 never asks for `resultsSection`:

```
"fields": "NCTId,BriefTitle,OverallStatus,Phase,EnrollmentCount,"
          "StartDate,CompletionDate,LeadSponsorName,InterventionName,"
          "InterventionType,StudyFirstPostDate,ResultsFirstPostDate,"
          "Condition,StudyType",
```

`resultsSection` is never in the payload, so `results_sec` is always `None`, so `has_results` is always `False` — even for the 342 trials whose `results_posted` date is populated in the same record.

```
has_results vs results_posted, by snapshot          (n trials)

 2026-07-17  script  ░░░░░░░░░░░░░░░░░░░░   0        858
             actual  ███████░░░░░░░░░░░░░  322
 2026-08-27  sandbox ████████░░░░░░░░░░░░  341        892
             actual  ████████░░░░░░░░░░░░  341   ✓ agree
 2026-08-28  sandbox ████████░░░░░░░░░░░░  342        893
             actual  ████████░░░░░░░░░░░░  342   ✓ agree
 2026-09-01  sandbox ░░░░░░░░░░░░░░░░░░░░   0        887
             actual  ████████░░░░░░░░░░░░  342   ✗ regression
                     └────┴────┴────┴────┘
                     0   100  200  300  400
```

**Two separate faults, same field.** The user's script has never populated it (Jul-17). The sandbox monitor derived it correctly on 08-27 and 08-28, then regressed to the script's behaviour on 09-01. The 09-01 snapshot's own metadata claims `"has_results derived from results_posted"` — that claim is false for the file it is attached to.

**Blast radius.** In `baseline_clinical_trials.py` line 177, `with_results = [t for t in all_trials.values() if t["has_results"]]` is the input to the "Recently Posted Results" table. That table is absent from `clinical_trials_summary.md` entirely — I checked, there is no results section in the file. So the hub's trial summary has silently shown zero posted results for its whole life. Any monitor diff keyed on `has_results` also returns a false zero; mine did on the first pass until I re-ran it against `results_posted`.

**Fix (one line, line 115):**

```python
"has_results": bool(status.get("resultsFirstPostDateStruct", {}).get("date", "")),
```

**Evidence level: SILVER.** Source code read directly, and the defect reproduced against four snapshot files with the missing downstream table confirmed. But per the doctrine's own GOLD post-mortem — *"GOLD requires three groups reporting the finding, not three documents mentioning it"* — the code, the snapshots it produced, and the table missing because of it are **three consequences of one mechanism, not three independent sources.** GOLD would require someone reproducing this against a live API call. The mechanism is not in doubt; the tier is.

This is the same class of failure the 09-01 iteration report documented for NCT identifiers — a field that resolves to something plausible (`False` is a legal value) and therefore never trips an error. Nine gates guard PMIDs, one gate now guards NCT ids, and nothing checks that a boolean agrees with the date field it is derived from.

---

## File System Status

| File | Modified | Age | Status |
|---|---|---|---|
| `hub_monitor_report.md` | 2026-07-17 | 47 d | **STALE** — still reports hub root as `/sessions/intelligent-bold-bardeen/...` |
| `clinical_trials_latest.json` | 2026-07-17 | 47 d | **STALE POINTER** — snapshots run through 09-01 |
| `pubmed_recent_latest.json` | 2026-07-17 | 47 d | **STALE POINTER** — snapshots run through 09-01 |
| `literature_gap_data.json` | mtime 2026-07-18 | 46 d | **STALE** — internal `generated` stamp is 2026-07-17T10:14, `date_range` ends 2026/07/17, so 47 d by its own clock |
| `literature_gap_report.md` | 2026-09-01 | 1 d | Fresh render of **47-day-old data** |
| `clinical_trials_snapshot_2026-09-01.json` | 2026-09-01 | 1 d | Current |
| `pubmed_recent_snapshot_2026-09-01.json` | 2026-09-01 | 1 d | Current |
| `clinical_trials_summary.md` | 2026-07-17 | 47 d | Stale, and missing its results table (see above) |

**552 of 628 files in `Analysis/Results/` are older than 14 days.** That number is not alarming by itself — 513 of them are date-stamped archives that are *supposed* to be frozen — but the two `*_latest.*` pointer files being 47 days old is a real problem, because anything downstream reading "latest" is reading July. Those two files (`clinical_trials_latest.json`, `pubmed_recent_latest.json`) are the only `*_latest.*` files anywhere in the hub.

**Collection gap.** Snapshots run daily 03-15 → 07-17, then stop for 41 days, then resume 08-27. The dated snapshots since 08-27 carry `"acquired_by": "cowork scheduled monitor (sandbox)"` — the scheduled task has been collecting the data, and the local scripts have not run since 2026-07-17. That explains why `*_latest.*` is frozen: the sandbox monitor writes dated snapshots but never updates the pointer files.

**`literature_gap_report.md` is misleading as it stands.** It was regenerated 09-01 03:17 and carries that timestamp, but every number in it comes from `literature_gap_data.json`, whose own `date_range` ends 2026/07/17. A reader sees a one-day-old report over a 47-day-old corpus. The report does state its date range internally, which is the only reason this is a caution rather than a defect.

---

## Clinical Trial Changes

**09-01 vs 08-28:** 0 new, 0 status changes, 6 dropped. The 6 dropped are query-window churn, not withdrawals — five ordinary RECRUITING/NOT_YET_RECRUITING records plus one ACTIVE_NOT_RECRUITING (Tandem NCT07325461), alongside Gan & Lee, Tonghua Dongbao, Sleepiz, Kangbuk Samsung and Beijing Supreme Life, all of which fell off the edge of a capped result set. Category totals moved -1/-3/-3, consistent with the drops. **Not actionable.**

The meaningful diff is against the last script-generated baseline.

**09-01 vs 07-17 (47 days):** 858 → 887 trials · **49 new** · 20 dropped · **23 status changes** · **20 newly posted results**.

### Status changes worth attention

| NCT | Change | Phase | Sponsor | Study |
|---|---|---|---|---|
| NCT07613307 | NOT_YET → **RECRUITING** | 3 | Eli Lilly | Orforglipron in T2D |
| NCT07664553 | NOT_YET → **RECRUITING** | 3 | AstraZeneca | (efficacy/safety) |
| NCT07684144 | NOT_YET → **RECRUITING** | 3 | Amgen | Long-term extension, n=950 |
| NCT07448974 | NOT_YET → **RECRUITING** | 3 | Tufts | Vitamin D and T2D, treat-to-target |
| NCT06334133 | RECRUITING → ACTIVE_NOT_REC | 3 | vTv Therapeutics | **Cadisegliatin** adjunctive to insulin — glucokinase activator, enrollment closed |
| NCT07400653 | RECRUITING → ACTIVE_NOT_REC | 3 | Pfizer | PF-08653944 |
| NCT07502495 | RECRUITING → ACTIVE_NOT_REC | 2 | Biomea Fusion | **Icovamenib** in T2D — enrollment closed, readout pending |
| NCT06305286 | RECRUITING → ACTIVE_NOT_REC | 1/2 | U. Chicago | Immunomodulation |
| NCT06845202 | RECRUITING → ACTIVE_NOT_REC | 1/2 | Alnylam | ALN-4324 |
| NCT07495956 | RECRUITING → **NOT_YET_REC** | 1/2 | Shenzhen Geno-Immune | cfMSC therapy — **reverse transition, worth a look** |

NCT06334133 (cadisegliatin) matters more than its row suggests: **Glucokinase × Health Equity** is rank 6 in the gap matrix with zero joint publications. A Phase 3 glucokinase activator closing enrollment is the kind of event that changes whether "no equity analysis exists for this drug class" is an interesting gap or an urgent one.

### New Phase 3 trials since 07-17

| NCT | Status | n | Sponsor | Study |
|---|---|---|---|---|
| NCT07743450 | RECRUITING | 1,560 | Ascletis Pharma | Once-daily oral ASC30 |
| NCT07784270 | NOT_YET_REC | 1,500 | AstraZeneca | AZD6234 |
| NCT07776509 | NOT_YET_REC | 500 | AstraZeneca | AZD6234 adjunct to incretin |
| NCT07754461 | RECRUITING | 600 | Boehringer Ingelheim | Survodutide in T2D |
| NCT07743983 | RECRUITING | 372 | BrightGene | BGM0504 in early T2DM with obesity |

**Newly posted results since 07-17: 20.** Only two are Phase 2+ industry trials — **NCT04596631** (Novo, Phase 3, oral semaglutide, posted 08-21) and **NCT05035082** (Novo, **Phase 4**, RYBELSUS comparative, n=1,018, posted 08-10). One more is an industry Phase 1: **NCT05428943** (Op-T LLC, OPT101 in T1D, n=24, posted 08-10). The largest academic drug trial is **NCT03899883** (U. Colorado, Phase 2, uric acid lowering in youth-onset T2D, n=11, posted 07-28) — n=11, so treat with care. The remainder are academic behavioural and device studies. Two large observational datasets also posted results: **NCT07513259** (n=203,424, pre-diagnosis GLP-1 RA use and post-cancer mortality) and **NCT03955952** (Cleveland Clinic, n=91,700, CV outcomes in bariatric surgery patients with diabetes). Those two are big enough to be worth a look on their own merits.

### Phase 3 recruiting landscape (n=57)

```
T2D Novel Therapies      █████████████████████████████████████████  41
T1D Immunotherapy/Prev   █████████████                              13
T1D Cure & Cell Therapy  ███                                         3
                         └────────┴────────┴────────┴────────┴────┘
                         0       10       20       30       40
```

**The 13.7:1 ratio of T2D-drug to T1D-cure Phase 3 activity is not static — it has widened all year.** Recomputed across the hub's own archived snapshots (RECRUITING ∧ PHASE3, by category):

```
T2D Novel : T1D Cure, Phase 3 recruiting

 2026-03-15   26 : 3    ████████▋            8.7
 2026-04-24   27 : 3    █████████            9.0
 2026-05-16   30 : 3    ██████████          10.0
 2026-06-27   30 : 3    ██████████          10.0
 2026-07-17   35 : 3    ███████████▋        11.7
 2026-09-01   41 : 3    █████████████▋      13.7
                        └────┴────┴────┴──┘
                        0    5   10   15
```

The T1D-cure denominator has been pinned at exactly 3 for six months while the T2D numerator grew 26 → 41. This is a **58% widening in the funding-attention gap between treating T2D and curing T1D**, visible only because the hub keeps daily archives. **Evidence level: SILVER** — one data source (ClinicalTrials.gov), but six independent time points and a monotone trend.

### Key organizations

- **Vertex — 3 trials.** NCT04786262 (Ph3, n=52) and NCT06832410 (Ph3, n=10) both RECRUITING for VX-880/zimislecel; NCT05791201 (VX-264, n=7) ACTIVE_NOT_RECRUITING. **No results posted on any of the three.**
- **Eli Lilly — 33 trials.** Two Phase 3 **baricitinib** studies now RECRUITING: NCT07222332 (beta-cell preservation, n=300) and NCT07222137 (delay of Stage 3 T1D, n=150). NCT04255433 (SURPASS-CVOT, tirzepatide vs dulaglutide, **n=13,299**) posted results 2026-07-08 — see Breaking News, this is the trial behind the Mounjaro CV approval.
- **Novo Nordisk — 28 trials.** NCT07564414 (CagriSema, Ph3, n=2,500) RECRUITING. Two results posted in-window: NCT04596631 (Phase 3) and NCT05035082 (Phase 4).
- **Sana Biotechnology — 0 trials in snapshot.** Nothing under that sponsor name is captured by the current ClinicalTrials.gov queries. **The string "Sana" also appears nowhere in the 160-paper PubMed corpus** — the gene-edited hypoimmune islet review (PMID 42626948) names no company. So the hub has zero visibility on a monitored key organization from either sensor. Either Sana has no registered diabetes trial, or both query sets miss it. Worth one manual check — a monitored key organization returning zero on two independent channels should not pass silently.

---

## PubMed Highlights

Window: 2026/08/02 → 2026/09/01, 30-day lookback, 160 unique papers across 16 domains + 8 tracked therapies.

### Cross-domain papers (17 of 160)

Highest-value first — papers spanning three domains:

- **PMID 42626948** — *Gene-edited hypoimmune islets as a cure for type 1 diabetes: a review of the immunological challenges.* (Expert Opin Biol Ther, 08-21) — T1D Stem Cell Cure × T1D Immunotherapy × teplizumab. Directly on the Tier 1 cell-therapy axis and the only paper this window bridging the cure and immunotherapy literatures.
- **PMID 42673585** — *Efficacy and Safety of GLP-1 RAs and Co-agonists for Weight Loss Among Adults Without Diabetes.* (**Annals of Internal Medicine**, 09-01) — orforglipron × retatrutide × CagriSema. Highest-impact venue in the window, and the only paper touching all three tracked incretin agents.
- **PMID 42670002** — *Targeting Autoimmunity in Type 1 Diabetes: Emerging Immunomodulatory Therapies.* (Curr Top Med Chem, 08-18) — Microbiome × Gene Therapy × Closed Loop AP. **Caution: the domain assignment looks wrong.** An immunomodulation review tagged Closed Loop AP is a keyword-match artifact, not a genuine three-way bridge. Read before citing.

Two-domain papers of note:

- **PMID 42627334** — *β-Cell Function and Diabetes Outcomes 1 Year After Stopping Oral Baricitinib Immunotherapy for T1D.* (**Diabetes Care**, 08-21). This is durability-after-withdrawal data on baricitinib, published while Lilly's two Phase 3 baricitinib trials (NCT07222332, NCT07222137) are recruiting. Trial-plus-literature convergence on the same agent in the same window — the highest-signal item in this report after the code defect.
- **PMID 42610933** — *Baseline Serum Metabolites as Predictors of Teplizumab Response.* (**Diabetes**, 08-18). Metabolomic predictors of immunotherapy response — sits squarely in Tier 1 Multi-Omics Biomarker Integration.
- **PMID 42582350** — Anti-GAD65 cerebellar ataxia in a young adult with T1D — T1D Immunotherapy × LADA.
- **PMID 42674789** — Retrospective population-based cohorts for assessing algorithmic diabetes classification (BMJ Open, 08-31) — AI/ML × LADA. **This is a study protocol, not results.** Relevant to the hub's LADA diagnostic model work as a design reference, not as evidence.
- **PMID 42437645** — Variant-specific pharmacophoric shifts in GLP-1R–orforglipron complexes (Boltz-2 co-folding) — GLP-1 Pharmacogenomics × orforglipron.

### Publication volume

13 of 16 domains *returned* 10 papers, but that is only the `retmax` display cap. Each domain record also carries `true_count` — the uncapped PubMed hit total — so volume **is** measurable. Trend over the four available snapshots (30-day rolling window each):

```
domain                      07-17  08-27  08-28  09-01     move
Diabetes AI/ML                260    168    167    168    ▼ -35%
Diabetes Microbiome           186    159    137    147    ▼ -21%
T2D GLP-1 New                 167    184    192    174    ▲  +4%
Diabetes Biomarker            166    129    133    123    ▼ -26%
Diabetes Health Equity         72     77     76     64    ▼ -11%
Diabetes Multi-Omics           65     62     62     54    ▼ -17%
T2D Remission                  59     57     61     48    ▼ -19%
Diabetes Gene Therapy          42     47     48     44    ▲  +5%
Closed Loop AP                 38     24     25     21    ▼ -45%
Diabetes Complications New     34     27     27     26    ▼ -24%
T1D Immunotherapy              25     20     17     20    ▼ -20%
T1D Stem Cell Cure             17     19     18     14    ▼ -18%
LADA New Research              12     14      9     10    ▼ -17%
Diabetes Drug Repurpose         8      1      1      0    ▼ ZERO
Diabetes Epigenetics            5      3      4      3    ▼ -40%
GLP-1 Pharmacogenomics          1      2      2      3    ▲ +200%
```

**`Diabetes Drug Repurpose` returned zero papers on 09-01** — down 8 → 1 → 1 → 0. That domain is **Tier 1 #4 in the doctrine (Drug Repurposing Computational Screening, score 18/20)**, described there as *"Massively under-explored."* A Tier 1 domain going to zero in a 30-day window is either the strongest possible confirmation of that assessment or a broken query. The query is narrow — `diabetes AND ("drug repurposing" OR "drug repositioning") AND (computational OR network OR screening)` — three required concept clusters, which will produce zeroes on scarce months. **Check the query before concluding the field went silent.**

The broad decline across most domains (AI/ML -35%, Closed Loop -45%) is likely a PubMed indexing-lag artifact: the 09-01 window ends the day it was pulled, and recent papers index late. Do not read it as a real slowdown without a re-pull.

**GLP-1 Pharmacogenomics is the only domain rising off a near-zero base** (1 → 3). Both it and Epigenetics (5 → 3) show real scarcity, and both appear in the gap matrix (Epigenetics × LADA 90.9; Epigenetics × Health Equity 84.0). Consistent signal from two independent methods.

### Tracked therapy trend (total_count)

```
                07-17  08-27  08-28  09-01
zimislecel          0      0      0      0    ← flat zero, 47 days
orforglipron       10     13     12     12
retatrutide         4      9     10      8
CagriSema           6      4      4      3
baricitinib         2      4      3      2
teplizumab          4      6      4      4
icodec              3      5      6      8    ← rising
dapagliflozin      52     34     34     32
```

**Zimislecel: 0 hits for 47 consecutive days.** Vertex has two Phase 3 trials recruiting and press coverage exists, so zero is implausible as a literature fact. Most likely explanation: the corpus indexes it as VX-880, not zimislecel. `baseline_pubmed_alerts.py` should query `(zimislecel OR VX-880)`. Until then, treat the zimislecel row as a broken sensor rather than as evidence of publication silence. **Evidence level: SILVER** — the alternate-name hypothesis is well-supported but I have not run the VX-880 query to confirm.

Insulin icodec is the only therapy rising monotonically (3 → 5 → 6 → 8), consistent with Novo's icodec Phase 3 results posting through this period. Retatrutide (4 → 8) and orforglipron (10 → 12) are also net up over the window but non-monotone.

*Note on the "79 new papers vs 08-28" figure: that count is inflated by the rolling 30-day window sliding forward 4 days, which retires old papers and admits new ones wholesale. It is not 79 papers of new research.*

---

## Gap Analysis Summary

**Source data is 47 days old** (`literature_gap_data.json`, internally stamped `generated: 2026-07-17T10:14`, corpus through 2026/07/17). 372 ranked pairs, all flagged `reliable`. Read accordingly.

Top 5 by gap score, **excluding pairs the report itself classifies as methodologically distinct** (GWAS × Closed Loop, Drug Repurposing × CGM, Islet Transplant × GWAS, Personalized Nutrition × Closed Loop — low overlap there reflects field structure, not a missed opportunity):

| # | Intersection | Gap | Joint | Expected |
|---|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 | 7.53 |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 | 7.28 |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 | 4.74 |
| 4 | Glucokinase × Health Equity | 100.0 | 0 | 4.25 |
| 5 | Gene Therapy × LADA | 100.0 | 0 | 3.34 |

### Alignment with Tier 1 doctrine areas

Three of the five (rows 2, 3, 4 — all the Health Equity pairs) map onto **Tier 1 #6, Epidemiological Data Analysis** (score 17/20), whose stated remit is *"Health equity analysis is under-resourced; disparity data exists but is rarely systematically analyzed."* The gap analysis independently found Health Equity as the single most under-connected domain in the matrix — it appears in 3 of the top 6 gaps and recurs throughout the unclassified list (Insulin Resistance × Health Equity 93.0, Metabolomics × 87.1, Autoimmunity T1D × 86.8, Microbiome × 84.5, Epigenetics × 84.0, Neuropathy × 80.9).

Two methods, one conclusion: **equity analysis of emerging therapies is the hub's clearest open lane.** The doctrine picked it on data access and impact; the gap analysis found it empirically. That convergence is the strongest argument in this report for what to work on next.

**#5 Gene Therapy × LADA** aligns with Tier 1 #2 (Literature Synthesis) and connects to two live signals this window — PMID 42582350 and PMID 42674789 both touch LADA, and Epigenetics × LADA sits at 90.9. **#1 Treg/CAR-T × Neuropathy has no equity or epidemiological dimension** and maps to no Tier 1 area cleanly; it is the top-scoring gap but the least aligned with what this hub is equipped to do.

**Evidence level: BRONZE**, as the gap report itself states. Single analytical source, keyword-based PubMed matching, no expert confirmation. The report's own caveat is correct and should travel with any downstream use: low co-publication may mean unexplored territory, terminology mismatch, or fields that simply do not overlap.

---

## Breaking News

**FDA approved Mounjaro (tirzepatide) for cardiovascular risk reduction in adults with T2D — announced 2026-08-30.** Indication covers reduction of MACE (CV death, non-fatal MI, non-fatal stroke) in high-risk adults; Lilly reports an 8% relative MACE reduction vs dulaglutide.

**This is directly traceable in the hub's own data.** NCT04255433 — *A Study of Tirzepatide (LY3298176) Compared With Dulaglutide*, n=13,299, Phase 3 — posted results 2026-07-08 and is sitting in the current snapshot. The registry record preceded the approval by seven weeks. A working `has_results` field plus an enrollment threshold would have surfaced this trial as a watch item in mid-July. **This is the concrete cost of the defect at the top of this report.** Evidence level: **SILVER** — the FDA action is reported by Lilly's investor release and independent wire coverage, but the in-hub registry record is *also* Lilly's own trial, so this is one primary source group plus secondary coverage, not three independent groups. The 8% figure is Lilly's own.

**Zimislecel regulatory submissions to FDA/EMA/MHRA expected during 2026** (Vertex program updates). Phase 3 enrollment ~50 patients; RMAT, Fast Track, PRIME, and ILAP designations already granted. Both Vertex Phase 3 records remain RECRUITING with no results posted. Evidence level: SILVER — company guidance plus secondary coverage; no filing confirmed.

**Greenstone Biosciences awarded a Breakthrough T1D grant (2026-08-18)** for a T1D-derived islet platform, alongside a Breakthrough T1D publication laying out a preclinical/manufacturing roadmap for islet cell therapies. Evidence level: BRONZE — single-source foundation announcement, no peer-reviewed output yet. Noted, not actioned.

Nothing else in the last 7 days clears the "genuinely significant" bar. No new FDA diabetes approvals, no unexpected Phase 3 readouts, no retractions.

---

## Recommended Actions

**Do first — data integrity**

1. **Patch `baseline_clinical_trials.py` line 115** to `"has_results": bool(status.get("resultsFirstPostDateStruct", {}).get("date", ""))`. One line. Restores the "Recently Posted Results" table in `clinical_trials_summary.md` and un-breaks every downstream results diff.
2. **Add an invariant gate** asserting `has_results == bool(results_posted)` for every trial at write time, and fail the snapshot loudly if it does not hold. This defect survived 47 days and one sandbox regression precisely because a wrong boolean is a legal boolean. Same lesson as the NCT audit gate from 09-01.
3. **Fix the sandbox monitor's has_results derivation** — it worked on 08-27 and 08-28 and regressed on 09-01. Whatever changed between those runs should be identified, not just patched.

**Do next — refresh the frozen pointers**

4. `python baseline_clinical_trials.py` — after the line-115 fix. `clinical_trials_latest.json` and `clinical_trials_summary.md` are 47 days stale.
5. `python baseline_pubmed_alerts.py` — `pubmed_recent_latest.json` is 47 days stale. **Change the zimislecel query to `(zimislecel OR VX-880)` first**, or the 0-hit row persists.
6. `python project1_literature_gap_analysis.py` — gap data is **47 days old** and `literature_gap_report.md` currently renders fresh-looking output over a July corpus.
7. `python hub_monitor.py` — the file-change report is 47 days old and still records the hub root as a previous session path.
8. **Decide who owns the two `*_latest.*` pointers.** The sandbox monitor has been the only thing collecting since 07-17 and it writes dated snapshots without updating the pointers. Either it should update them or the hub should stop treating them as authoritative.
9. **Check the `Diabetes Drug Repurpose` query in `baseline_pubmed_alerts.py`.** It returned 0 papers on 09-01, down from 8. The query requires three concept clusters to co-occur (`diabetes` AND repurposing-terms AND computational-terms), which is fragile. Distinguish "the field went quiet" from "the query is too narrow" before drawing any conclusion about a Tier 1 domain.

**Review — literature**

10. **PMID 42627334** (Diabetes Care, baricitinib β-cell function 1 year after withdrawal) against Lilly's two recruiting Phase 3 baricitinib trials NCT07222332 and NCT07222137. Trial and literature converging on one agent in one window.
11. **PMID 42610933** (Diabetes, serum metabolite predictors of teplizumab response) — Tier 1 Multi-Omics.
12. **PMID 42626948** (gene-edited hypoimmune islets review) — Tier 1 cell-therapy axis; the closest thing in the corpus to the Sana blind spot below, though it names no company.
13. **PMID 42673585** (Annals of Internal Medicine, GLP-1 RA/co-agonist weight loss without diabetes) — highest-impact venue in the window.
14. **Verify PMID 42670002's domain tags before citing.** Microbiome × Gene Therapy × Closed Loop AP on an immunomodulation review is almost certainly a keyword artifact.

**Verify — monitoring coverage**

15. **Sana Biotechnology returns 0 on both sensors** — 0 trials in the registry snapshot, 0 mentions across 160 PubMed papers. Confirm by hand whether that is a true zero or a two-way query-coverage failure. A monitored key organization silently returning nothing is the same failure mode as `has_results`.
16. **Watch NCT07495956** (Shenzhen Geno-Immune, cfMSC therapy) — RECRUITING → NOT_YET_RECRUITING is a backwards transition and usually means something.
17. **Watch NCT06334133** (vTv cadisegliatin, Phase 3, enrollment now closed). Glucokinase × Health Equity is rank 6 with zero joint publications; a Phase 3 readout would move that lane from theoretical to live.

**Consider — contribution**

18. Health Equity is the top gap by two independent methods (doctrine Tier 1 #6 scoring and the gap matrix, where it appears in 3 of the top 6 and 6 more in the unclassified list). Beta Cell Regen × Health Equity and Glucokinase × Health Equity both have joint_pubs = 0 against live Phase 3 programs. That is the clearest open lane in the hub. Any output must carry the BRONZE label until the gap finding is expert-confirmed.
19. **The widening T2D:T1D-cure Phase 3 ratio (8.7 → 13.7 over six months) is a publishable observation in its own right** and sits directly in Tier 1 #3, Clinical Trial Intelligence. The hub already holds the daily archive needed to compute it. Extending the series back to 2026-03-15 across all 124 snapshots would take one script and would be the hub's own data answering a question nobody else can answer from a single ClinicalTrials.gov pull.

---

## Caveats

- All gap findings are **BRONZE** — single analytical source, keyword-matched, unconfirmed by domain experts, and computed over a 47-day-old corpus.
- The 09-01 clinical trial and PubMed snapshots were acquired by the scheduled sandbox monitor, not by the user's local scripts. They replicate the script queries but are not script output. The `has_results` regression is direct evidence that the replication is not exact.
- Domain assignments in the PubMed data are keyword-derived and demonstrably produce false cross-domain hits (PMID 42670002). Cross-domain counts are an upper bound.
- Per-domain *returned* papers are capped at `retmax=10`, but `true_count` in each domain record is uncapped and is what the volume table above uses. The 09-01 window ends on its own pull date, so recent-month counts are depressed by PubMed indexing lag — the cross-snapshot declines are probably artifact, not signal.
- **This report corrects nine numerical errors found in its own first draft by an adversarial verification pass** (gap expected-value, `*_latest.*` file count, the below-ceiling domain chart, the T2D:T1D ratio trend claim, a Phase 3/Phase 4 mislabel, the industry-trial count, Glucokinase's top-6 frequency, the gap-data generation date, and the stale-file count). Two evidence tiers were also demoted from GOLD to SILVER for failing the doctrine's independent-source test. The verification pass is why those numbers can be trusted; it is not a reason to trust unverified numbers elsewhere.
- No file in the hub was modified by this run.

---
*Review-only run. Generated 2026-09-02 by the diabetes-hub-monitor scheduled task.*
