# Diabetes Hub Monitor Report — 2026-09-03

**Run type:** Scheduled automated review (read-only; no existing files modified)
**Effective data date:** 2026-09-01 snapshots (2 days old)
**Evidence levels per Research Doctrine:** file-derived facts marked [Certain]; web-derived marked [Likely] pending primary-source confirmation.

---

## 0. Lead finding — read this first

**Your local Python pipeline has not run since 2026-07-17.** The `_latest` pointer files
(`clinical_trials_latest.json`, `pubmed_recent_latest.json`, `hub_monitor_report.md`) are **48 days stale**.
The only reason this report has current data is that a prior *sandbox* monitor run wrote
`clinical_trials_snapshot_2026-09-01.json` and `pubmed_recent_snapshot_2026-09-01.json` directly —
that snapshot's metadata self-identifies as `"acquired_by": "cowork scheduled monitor (sandbox)"`,
not as output of your scripts. [Certain]

Consequence: anything downstream that reads `*_latest.json` — dashboards, tracker updates,
the gap analysis — is operating on **July 17 data**. See §5.

---

## 1. File System Status

| File | Last modified | Age (days) | Status |
|---|---|---|---|
| `hub_monitor_report.md` | 2026-07-17 02:16 | 48 | **STALE** |
| `clinical_trials_latest.json` | 2026-07-17 02:05 | 48 | **STALE** |
| `pubmed_recent_latest.json` | 2026-07-17 02:06 | 48 | **STALE** |
| `literature_gap_data.json` | 2026-07-18 03:11 | 47 | **STALE** |
| `literature_gap_report.md` | 2026-09-02 03:22 | 1 | Fresh file, **stale content** — see §4 |
| `clinical_trials_snapshot_2026-09-01.json` | 2026-09-01 02:37 | 2 | Current (sandbox-acquired) |
| `pubmed_recent_snapshot_2026-09-01.json` | 2026-09-01 02:38 | 2 | Current (sandbox-acquired) |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 10:07 | 48 | **STALE** |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 03:12 | 3 | Current |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 00:06 | 172 | Very old — intentional? |

**Snapshot cadence gap.** Clinical-trial snapshots ran near-daily 2026-03-15 → 2026-07-17
(**121 files**; four days missing: 05-06, 05-15, 06-01, 06-08), then **stopped for 41 days**,
resuming only on 08-27, 08-28, 09-01 (124 total). There is no snapshot for
2026-07-18 → 2026-08-26, nor for 08-29 → 08-31, nor 09-02 → 09-03. Day-over-day diffing is
not possible across that window; the 07-17 → 09-01 comparisons below are 46-day aggregates. [Certain]

**Lock file present:** `.~lock.Diabetes_Research_Tracker.xlsx#` (2026-03-14). A stale LibreOffice
lock file. Harmless, but it will block programmatic writes to the tracker if a script uses a
lock-aware writer. Worth deleting. [Certain]

---

## 2. Clinical Trial Changes

**Corpus size:** 858 trials (07-17) → 892 (08-27) → 893 (08-28) → **887 (09-01)**. [Certain]

### 2a. Data quality flag — the corpus shrank

08-28 → 09-01 shows **0 new trials and 6 removed**. A ClinicalTrials.gov corpus that adds nothing
in four days while dropping six records is more consistent with a **truncated or partially-failed
fetch** than with real registry activity. Dropped records:

| NCT | Status | Phase | Sponsor |
|---|---|---|---|
| NCT06542627 | RECRUITING | N/A | Kangbuk Samsung Hospital |
| NCT06558708 | RECRUITING | Phase 2 | Gan and Lee Pharmaceuticals |
| NCT06559722 | NOT_YET_RECRUITING | Phase 3 | Tonghua Dongbao Pharmaceutical |
| NCT06569940 | RECRUITING | N/A | Sleepiz AG |
| NCT06575478 | RECRUITING | Phase 2 | Beijing Supreme Life Pharmaceutical |
| NCT07325461 | ACTIVE_NOT_RECRUITING | N/A | Tandem Diabetes Care |

Five of the six cluster within the narrow NCT06542–06575 ID band, plus one outlier — a pattern more
consistent with a dropped result page than with six independent withdrawals. **Do not treat these
as real removals until verified against the registry.** [Likely]

### 2b. Phase 3 RECRUITING — 57 trials

*(57 counts trials tagged `PHASE2, PHASE3`; strict PHASE3-only is **52**.)*

Selected large trials — **not** a strict top-9. Six trials with enrollment above the 723 shown are
omitted for brevity: NCT06825182 (1,000), NCT07684144 (950), NCT07662135 (900), NCT07076199 (877),
NCT07662044 (800), NCT07082114 (800).

| NCT | n | Sponsor | Program |
|---|---|---|---|
| NCT07064473 | 11,800 | Boehringer Ingelheim | Vicadrostat + empagliflozin (EASi-PROTKT) |
| NCT07481747 | 2,539 | Hudson Biotech | Tirzepatide vs placebo |
| NCT07564414 | 2,500 | Novo Nordisk | **CagriSema**, two doses |
| NCT06082063 | 2,000 | Steno Diabetes Center | Multifactorial CVD reduction in T1D |
| NCT07662109 | 2,000 | AstraZeneca | Elecoglipron combination |
| NCT07351058 | 1,600 | Hoffmann-La Roche | Enicepatide (RO7795068) |
| NCT07743450 | 1,560 | Ascletis Pharma | Oral ASC30 |
| NCT07662213 | 1,200 | AstraZeneca | Elecoglipron |
| NCT07088068 | 723 | Sanofi | **Teplizumab** vs placebo |

**Notable:** AstraZeneca now has **five** Phase 3 elecoglipron trials recruiting
(NCT07662109 n=2,000 / NCT07662213 n=1,200 / NCT07662135 n=900 / NCT07662044 n=800 /
NCT07664553 n=600 — **5,500 combined**). That is a full Phase 3 program launch and is not yet
represented in the tracker. [Certain]

**Also notable:** Teplizumab Phase 3 (NCT07088068) is sponsored by **Sanofi**, not Provention/Sanofi
legacy naming — confirm the tracker's sponsor field matches. [Certain]

### 2c. Key-organization trials (09-01 snapshot)

| Org | Trials in corpus | Phase 3 recruiting |
|---|---|---|
| Eli Lilly | 33 | NCT07222332 (baricitinib, children), NCT07222137 (baricitinib, delay stage 3), NCT07613307 (orforglipron), NCT06739122 (dulaglutide peds) |
| Novo Nordisk | 28 | NCT07564414 (CagriSema), NCT07076199 (icodec) |
| Vertex | 3 | NCT06832410 + NCT04786262 (VX-880 / zimislecel) |
| Sana Biotechnology | **0** | — |

**Gap:** Sana Biotechnology appears in **zero** trials in the corpus despite being on your
key-organization watchlist. Either Sana's UP421/SC451 hypoimmune islet work is registered under a
sponsor name the query doesn't match, or it is not on ClinicalTrials.gov under diabetes terms.
This is a **query coverage bug, not an absence of activity** — worth a manual check. [Likely]

### 2d. Status changes, 07-17 → 09-01 (23 total)

Most consequential (Phase 3 / Phase 2 entering or leaving recruitment):

| NCT | Change | Program |
|---|---|---|
| NCT07613307 | NOT_YET → **RECRUITING** | Eli Lilly orforglipron, T2D |
| NCT07664553 | NOT_YET → **RECRUITING** | AstraZeneca elecoglipron Ph3 |
| NCT07684144 | NOT_YET → **RECRUITING** | Amgen extension trial Ph3 |
| NCT06820281 | NOT_YET → **RECRUITING** | Tirzepatide in T1D (Victor Chang) |
| NCT06334133 | RECRUITING → ACTIVE_NOT_RECRUITING | vTv **cadisegliatin** Ph3 (glucokinase activator) |
| NCT07400653 | RECRUITING → ACTIVE_NOT_RECRUITING | Pfizer PF-08653944 Ph3 |
| NCT07502495 | RECRUITING → ACTIVE_NOT_RECRUITING | Biomea **icovamenib** Ph2 |
| NCT06305286 | RECRUITING → ACTIVE_NOT_RECRUITING | U. Chicago immunomodulation Ph1/2 |
| NCT07495956 | RECRUITING → **NOT_YET_RECRUITING** (reversal) | Shenzhen cfMSC therapy — status regression, verify |

**vTv cadisegliatin (NCT06334133) closing enrollment is the highest-signal item here** —
it is the lead glucokinase activator in Phase 3, and Glucokinase is a domain in your gap analysis
(854 pubs, three top-7 gap pairs). Readout timing now becomes trackable. [Certain]

### 2e. Newly posted results, 07-17 → 09-01 (20 trials)

Zero pre-existing trials flipped `has_results` false→true. All 20 are trials **new to the corpus**
that arrived carrying results — i.e. they entered via the "Recently Completed with Results"
category (321 → 341). Industry-sponsored ones worth reviewing:

| NCT | Posted | Sponsor | Phase | Study |
|---|---|---|---|---|
| NCT04596631 | 2026-08-21 | Novo Nordisk | 3 | Oral semaglutide vs placebo |
| NCT05035082 | 2026-08-10 | Novo Nordisk | 4 | RYBELSUS® vs other oral agents |
| NCT05428943 | 2026-08-10 | Op-T LLC | 1 | OPT101 in T1D |
| NCT03899883 | 2026-07-28 | U. Colorado Denver | 2 | Uric-acid lowering in youth-onset T2D |

The remaining 16 are academic investigator-initiated trials (Yale, Michigan, Emory, Dartmouth,
Jaeb, Roswell Park, Colorado, Cleveland Clinic). Most are behavioral/health-services studies
relevant to the **Health Equity** Tier 1 area (see §4), but four are not: NCT05530356 (renal
hemodynamics / insulin resistance), NCT04114903 (cannabis anti-inflammatory), NCT03955952
(bariatric surgery CV outcomes), NCT07513259 (GLP-1 RA pharmacoepidemiology). [Certain]

**Also in-corpus and directly relevant to §5 breaking news:** NCT04255433 (SURPASS-CVOT,
tirzepatide vs dulaglutide MACE, Eli Lilly, Phase 3) shows `results_posted = 2026-07-08`. [Certain]

---

## 3. PubMed Highlights

**Window:** 30-day lookback, 2026/08/02 → 2026/09/01. 160 unique papers, 16 domains,
8 tracked therapies. [Certain]

### 3a. Cross-domain papers — 17 total, 9 new since 08-28

Highest priority (3 domains each):

1. **PMID 42673585** — *Efficacy and Safety of GLP-1 Receptor Agonists and Co-agonists for Weight
   Loss Among Adults Without Diabetes* — **Annals of Internal Medicine, 2026 Sep 01**. **NEW.**
   Hits orforglipron + retatrutide + CagriSema simultaneously — the only paper in the corpus
   touching all three tracked incretin programs. High-impact journal, published the day of the
   snapshot. **Read this one first.**

2. **PMID 42670002** — *Targeting Autoimmunity in Type 1 Diabetes: Emerging Immunomodulatory
   Therapies* — Curr Top Med Chem, 2026 Aug 18. **NEW.** Microbiome + Gene Therapy + Closed Loop AP.

3. **PMID 42626948** — *Gene-edited hypoimmune islets as a cure for type 1 diabetes: a review of
   the immunological challenges* — Expert Opin Biol Ther, 2026 Aug 21. Stem Cell Cure +
   Immunotherapy + teplizumab. **This is the Sana-adjacent literature** that §2c says is missing
   from your trial corpus.

Other new cross-domain papers: 42661785 (GLP-1/remission), 42674789 (AI/ML + LADA — algorithmic
diabetes classification, *BMJ Open*), 42667586 (AI/ML + Multi-Omics), 42668961 (Biomarker +
Complications), 42661879 (Biomarker + Multi-Omics), 42666243 (Gene Therapy + Complications),
42437645 (GLP-1 Pharmacogenomics + orforglipron).

**PMID 42674789 deserves a second look** — algorithmic diabetes classification performance in
population cohorts sits exactly on the AI/ML × LADA intersection, which your own gap table scores
at **82.0 with only 3 joint publications**. Note it is a **study protocol**, not a results paper —
so the gap is being *claimed*, not yet filled. That is arguably more actionable: the results are
still years out. [Certain]

### 3b. Key-therapy tracking

| Therapy | Papers (09-01) | Total PubMed hits | Note |
|---|---|---|---|
| orforglipron | 10 | 12 | Highest volume |
| retatrutide | 8 | 8 | |
| icodec | 8 | 8 | |
| dapagliflozin | 10 | — | |
| teplizumab | 4 | — | |
| CagriSema | 3 | 3 | |
| baricitinib | 2 | 2 | |
| **zimislecel** | **0** | **0** | See below |

**zimislecel returns literally zero PubMed results** for query `diabetes AND zimislecel`. [Certain]
This is a real finding, not a bug: the compound is published under **VX-880** in most of the
literature (cf. PMID 42626948 above, and Vertex's own trial titles NCT06832410 / NCT04786262 which
say "VX-880"). **Your PubMed alert query is missing the entire Vertex program.**
Fix: change the query to `diabetes AND (zimislecel OR VX-880)`. [Certain]

Single highest-value therapy paper this window:
**PMID 42627334** — *β-Cell Function and Diabetes Outcomes 1 Year After Stopping Oral Baricitinib
Immunotherapy for Type 1 Diabetes* — **Diabetes Care, 2026 Aug 21.** Off-treatment durability data
for baricitinib, published while Lilly is actively recruiting two Phase 3 baricitinib trials
(NCT07222332, NCT07222137). Directly decision-relevant. [Certain]

Also: **PMID 42610933** — *Baseline Serum Metabolites as Predictors of Teplizumab Response*
(*Diabetes*, 2026 Aug 18). A metabolomic responder-prediction study — sits squarely in Tier 1
Multi-Omics Biomarker Integration. [Certain]

### 3c. Volume trends

13 of 16 domains are **pinned at exactly 10 papers** — the retmax ceiling. Domain-level volume is
therefore **censored and cannot be trended**. Only three domains fall below the ceiling on 09-01
and carry real signal:

| Domain | 07-17 | 08-28 | 09-01 | Read |
|---|---|---|---|---|
| Diabetes Epigenetics | 5 | 4 | **3** | Declining, genuinely low-volume |
| GLP-1 Pharmacogenomics | 1 | 2 | **3** | Rising, still very thin |
| **Diabetes Drug Repurpose** | 8 | 1 | **0** | **Collapsed to zero — investigate** |

**Diabetes Drug Repurpose going 8 → 1 → 0 is the most alarming number in this section.** Drug
Repurposing is **Tier 1 #4 (18/20)** in the Doctrine. Either the field genuinely published nothing
in the 30-day window, or the query broke. Given the 8 → 1 → 0 shape across three snapshots, a
broken or over-narrow query is the likelier explanation. Check it. [Likely]

(LADA New Research ran 10 / 9 / 10 — at the ceiling, so not trendable either.)

**Methodological caution:** any statement of the form "domain X publication activity increased"
derived from this dataset is unsupportable for the 13 censored domains. Raise `retmax` before
claiming any volume trend. [Certain]

---

## 4. Gap Analysis Summary

### 4a. Provenance warning

`literature_gap_report.md` carries a generation timestamp of **2026-09-02 03:22** but its own
metadata states **date range 2020/01/01 to 2026/07/17**, and the underlying
`literature_gap_data.json` was last written **2026-07-18**. The report was **re-rendered from stale
data**, not recomputed. Anyone reading the header date will believe these gap scores are current.
They reflect the literature as of July 17. [Certain]

### 4b. Top under-researched intersections (BRONZE — single analytical source)

| Rank | Intersection | Gap Score | Joint Pubs |
|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 |
| 4 | Glucokinase × Health Equity | 100.0 | 0 |
| 5 | Gene Therapy × LADA | 100.0 | 0 |
| 6 | Drug Repurposing × Health Equity | 100.0 | 0 |
| 7 | Insulin Resistance × Islet Transplant | 91.9 | 1 |

### 4c. Alignment with Tier 1 contribution areas

Read against `RESEARCH_DOCTRINE.md` §Tier 1:

- **Four of the top seven gaps involve Health Equity** (ranks 2, 3, 4, 6) — and a fifth,
  Insulin Resistance × Health Equity (93.0), sits just below in the Unclassified section.
  Health Equity maps to **Tier 1 #6, Epidemiological Data Analysis (17/20)**, and its total corpus
  is only 1,990 papers. This is the single most concentrated Tier-1-aligned opportunity in the
  dataset. [Certain]
- **Beta Cell Regen × Health Equity (rank 2)** and **Glucokinase × Health Equity (rank 4)** are now
  *time-sensitive*: Vertex's zimislecel Phase 3 is recruiting (§2c) and vTv's cadisegliatin Phase 3
  just closed enrollment (§2d). Access/equity analysis of a therapy class is most useful **before**
  approval, not after. The window on both is roughly 12–24 months. [Likely]
- **Gene Therapy × LADA (rank 5, 0 joint pubs)** intersects with two live signals this window:
  PMID 42661296 (B lymphocytes in LADA, *Diabetes Metab Res Rev*) and PMID 42360463 (metabolomic
  profile distinguishing LADA from T1D, *Diabetologia*). LADA's total corpus is 582 papers —
  small enough for a genuinely complete synthesis. [Certain]
- **Drug Repurposing × Health Equity (rank 6)** maps to **Tier 1 #4 (18/20)** and **#6** jointly —
  the only top-7 gap that hits two Tier 1 areas at once.

**Caveat carried forward from the source report:** these are BRONZE. A gap score of 100 with 0 joint
publications is equally consistent with terminology mismatch as with unexplored territory. Per the
report's own §"How to Use This Analysis", each requires a manual combined-term PubMed search plus a
Cochrane/PROSPERO check before it is treated as real.

---

## 5. Breaking News (web, last 7 days)

**1. FDA approved Mounjaro (tirzepatide) for cardiovascular risk reduction in T2D — 2026-08-28.** [Likely]
Indication: reduction of MACE (CV death, non-fatal MI, non-fatal stroke) in adults with T2D at high
CV risk. Reported effect: ~8% additional MACE reduction vs dulaglutide.
**This connects directly to your corpus:** the supporting trial is almost certainly **NCT04255433**
(SURPASS-CVOT, tirzepatide vs dulaglutide on MACE, Eli Lilly, Phase 3, COMPLETED), whose results
posted **2026-07-08** — a month before the approval, and already sitting in your 09-01 snapshot
unflagged. Your trial-intelligence pipeline had the leading indicator and did not surface it.
*Confidence note: the NCT↔approval link is inferred from trial design match, not from the FDA
label. Verify against the approval letter before citing.* [Likely → needs primary source for Certain]

**2. Retatrutide TRANSCEND-T2D-1 Phase 3 published in The Lancet.** [Likely]
537 participants; HbA1c reduction 18.5 / 20.3 / 21.2 mmol/mol at 4/9/12 mg vs 8.9 mmol/mol placebo;
weight loss 11.5–15.3% vs 2.6%. Presented at ADA 2026 (New Orleans, 5–8 June).
Not in your 30-day PubMed window — it predates it. Retatrutide has 8 papers in-window but not
the pivotal trial itself. **Your alert window is too short to catch pivotal publications.**

**3. Zimislecel regulatory status — no FDA decision yet.** [Likely]
Vertex guidance is for FDA/EMA/MHRA submissions during 2026; realistic approval window 2027–2028
under RMAT + Fast Track. Pivotal data: 10/12 (83%) insulin-independent at Month 12, all 12 with
durable glucose-responsive C-peptide, no severe hypoglycemia from day 90.
**No approval action to report.** Combined with §3b, note that you are currently blind to this
program in PubMed alerts.

Nothing else in the last 7 days met the significance bar (Phase 3 readout / FDA action / major
publication). Routine news skipped.

---

## 6. Recommended Actions

**P0 — pipeline is not running**

1. Investigate why the local scheduler stopped after 2026-07-17. The 41-day snapshot gap
   (07-18 → 08-26) is the primary defect; everything else in this report is downstream of it.
2. Re-run the full refresh to restore the `_latest` pointers:
   ```
   python baseline_clinical_trials.py
   python baseline_pubmed_alerts.py
   python project1_literature_gap_analysis.py
   python hub_monitor.py
   ```
   Run in that order — `hub_monitor.py` last, so it diffs against refreshed inputs.
3. Delete the stale lock file `Diabetes_Research/.~lock.Diabetes_Research_Tracker.xlsx#`.

**P1 — data-quality fixes (each is a silent blind spot)**

4. **Fix the zimislecel PubMed query** → `diabetes AND (zimislecel OR VX-880)`. Currently returning
   0 results and hiding the entire Vertex program. (§3b)
5. **Fix or explain the Sana Biotechnology trial gap** — 0 trials in an 887-trial corpus for a
   watchlist organization. Check sponsor-name matching in `baseline_clinical_trials.py`. (§2c)
6. **Raise PubMed `retmax` above 10.** 13 of 16 domains are censored at the ceiling; no volume
   trend claim is currently defensible. (§3c)
6b. **Check the `Diabetes Drug Repurpose` query** — it returned 8 → 1 → **0** papers across the
   07-17 / 08-28 / 09-01 snapshots. Drug Repurposing is Tier 1 #4 (18/20); a silently broken query
   there is expensive. (§3c)
7. **Verify the 6 "removed" trials** (NCT06542627, NCT06558708, NCT06559722, NCT06569940,
   NCT06575478, NCT07325461) against ClinicalTrials.gov before recording them as withdrawn.
   Contiguous NCT IDs suggest a dropped fetch page. (§2a)
8. **Make `project1_literature_gap_analysis.py` fail loudly on stale input**, or stamp the report
   with the *data* date rather than the *render* date. A report headed 2026-09-02 containing
   2026-07-17 data is the kind of error that propagates into a manuscript. (§4a)

**P2 — analysis, ordered by value**

9. **Read PMID 42673585** (*Ann Intern Med*, Sep 1) — only paper spanning orforglipron +
   retatrutide + CagriSema.
10. **Read PMID 42627334** (*Diabetes Care*, Aug 21) — baricitinib off-treatment durability, while
    two Lilly Phase 3 baricitinib trials recruit.
11. **Read PMID 42674789** (*BMJ Open*, Aug 31) — AI/ML × LADA algorithmic classification. It is a
    *protocol*, so a gap you scored at 82.0 / 3 joint pubs has been claimed but not yet filled.
    Determine whether to collaborate or move first.
12. **Scope a Health Equity × emerging-cell-therapy access analysis.** Four of your top seven gaps
    route through Health Equity; two of them (Beta Cell Regen, Glucokinase) have Phase 3 programs
    in flight, making the pre-approval window finite. This is the highest Tier-1-aligned,
    lowest-competition move available. Start with Beta Cell Regen × Health Equity (rank 2, 0 joint
    pubs, Tier 1 #6).
13. **Manually validate the top 7 gaps** with combined-term PubMed + Cochrane/PROSPERO searches
    before treating any as real. They are BRONZE. Doctrine requires triple-source before promotion.

**P3 — tracker updates**

14. Add the **AstraZeneca elecoglipron Phase 3 program** (NCT07662109, NCT07662213, NCT07662135,
    NCT07662044, NCT07664553) — five Phase 3 trials, **5,500** combined enrollment, absent from
    the tracker.
15. Add **NCT04255433 / SURPASS-CVOT** with the 2026-08-28 FDA CV-risk-reduction approval linked,
    once the label link is confirmed.
16. Update **NCT06334133 (vTv cadisegliatin)** to ACTIVE_NOT_RECRUITING and set a readout watch.
17. Log the 20 newly-results-posted trials (§2e); the 16 investigator-initiated behavioral studies
    are candidate inputs to the Health Equity work in action 12.

---

## Autonomous choices made during this run

- Treated `clinical_trials_snapshot_2026-09-01.json` / `pubmed_recent_snapshot_2026-09-01.json` as
  the effective "latest" data, since the `_latest` pointers were 48 days stale. All §2–§3 findings
  derive from the 09-01 snapshots, not from `*_latest.json`.
- Used 2026-07-17 as the comparison baseline for trial diffs (the last snapshot before the 41-day
  gap), so "changes" are 46-day aggregates, not day-over-day.
- Did not refresh any data from live APIs and did not modify any existing file. This was a
  read-only review run per the task definition. The only file written is this report.

---

## Verification

All numeric claims in §1–§4 were independently recomputed from the source JSON/MD files by a
second pass before this report was finalized. That pass caught and corrected eight errors in the
draft (snapshot file count and cadence, Eli Lilly and Novo Nordisk sponsor counts, elecoglipron
program size, cross-domain new-paper count, icodec paper count, a false claim that 08-28 recorded
zero key-therapy papers, and a "five of seven gaps" miscount). The corrected values are what
appear above.

Claims **not** independently verified, and their status:
- The NCT04255433 ↔ Mounjaro CV-approval link (§5) is **inferred from trial design match**, not read
  off the FDA label. Verify before citing.
- All §5 items are web-sourced [Likely].
- The Sana Biotechnology zero-trial finding (§2c) is verified *within the corpus*; whether Sana has
  registered trials that the query missed was **not** checked against ClinicalTrials.gov directly.
- Gap scores (§4) are BRONZE by the source report's own classification and were not re-derived.

---

*Generated 2026-09-03 by the Diabetes Hub scheduled monitor. Read-only review run.*
*Evidence levels per RESEARCH_DOCTRINE.md. Web-derived items are [Likely] pending primary-source verification.*
