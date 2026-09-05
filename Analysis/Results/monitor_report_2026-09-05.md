# Diabetes Hub Monitor Report — 2026-09-05

**Run type:** Scheduled automated review (read-only; no existing files modified)
**Effective data date:** 2026-09-01 snapshots — **4 days old, unchanged since the 09-02 report**
**Evidence levels per Research Doctrine:** file-derived facts [Certain]; web-derived [Likely] pending primary-source confirmation.

---

## 0. Lead finding — the monitor is now measuring itself, not the field

**Fifth consecutive report on the same frozen snapshot pair. The acquisition step has
not run since 2026-09-01.** [Certain]

```
Snapshot acquisition cadence
2026-07-16  ██
2026-07-17  ██
            ······ 41-day outage (07-18 → 08-26) ······
2026-08-27  ██
2026-08-28  ██
            ··· 3-day gap ···
2026-09-01  ██
2026-09-02  ─
2026-09-03  ─
2026-09-04  ─
2026-09-05  ─   ← today
```

Reports written: 09-01, 09-02, 09-03, 09-04, 09-05 (5)
Data refreshes behind them: 1

**This is the finding.** Sections 2–4 below contain no change from the 09-04 report,
because there is no new input to change them. The one genuinely new item this run is
the FDA action in §5, which the hub's *own trial corpus already contained the evidence
for* — see §5 for why that matters.

**Recommendation stands and is now overdue: either restore acquisition or drop this
task to weekly.** Running daily against a static file manufactures the appearance of
surveillance. [Certain]

---

## 1. File System Status

| File | Last modified | Age (d) | Status |
|---|---|---|---|
| `clinical_trials_snapshot_2026-09-01.json` | 09-01 02:37 | 4 | Newest trial data |
| `pubmed_recent_snapshot_2026-09-01.json` | 09-01 02:38 | 4 | Newest PubMed data |
| `clinical_trials_latest.json` | 07-17 02:05 | **50** | **STALE pointer** |
| `pubmed_recent_latest.json` | 07-17 02:06 | **50** | **STALE pointer** |
| `hub_monitor_report.md` | 07-17 02:16 | **50** | **STALE** |
| `literature_gap_data.json` | 07-18 03:11 | **49** | **STALE** |
| `literature_gap_report.md` | 09-04 08:22 | 1 | Fresh render, **July input** — §4 |
| `Diabetes_Research_Tracker.xlsx` | 07-17 10:07 | **50** | **STALE** |
| `RESEARCH_DOCTRINE.md` | 08-31 03:12 | 5 | Current |
| `CONTRIBUTION_STRATEGY.md` | 03-15 00:06 | 174 | 6 months old |

**Two versions of "current" still coexist.** The dated snapshots advanced to 09-01; the
`*_latest.json` pointers did not. Anything downstream reading `*_latest.json` —
dashboards, tracker refresh, gap analysis — is consuming **July 17 data**. This report
deliberately reads the dated 09-01 files instead. [Certain]

**Proof the divergence is real, not a timestamp artifact:** `clinical_trials_latest.json`
is byte-identical in size to `clinical_trials_snapshot_2026-07-17.json` (593,584 B), and
`pubmed_recent_latest.json` matches `pubmed_recent_snapshot_2026-07-17.json` (123,881 B).
The pointer files are literal copies of the July 17 run. [Certain]

`hub_monitor_report.md` records its hub root as `/sessions/intelligent-bold-bardeen/...`
— a prior sandbox session path, confirming it was last written by a sandbox run rather
than your local machine. [Certain]

**Stale lock file** `.~lock.Diabetes_Research_Tracker.xlsx#` (2026-03-14) still present;
will block lock-aware writers. [Certain]

---

## 2. Clinical Trial Changes

Corpus: 892 (08-27) → 893 (08-28) → **887 (09-01)**.

Diff 08-28 → 09-01:

| Metric | Count |
|---|---|
| New trials | **0** |
| Removed trials | 6 |
| Status changes | **0** |
| New results posted | **0** |

Zero status changes across four days on an 887-trial corpus is itself worth a note.
Over the 07-16 → 07-17 pair the script logged 1 new / 1 removed / 0 status changes, so
low churn is normal for this query set — but 0/0 with 6 removals suggests the removals
are query-boundary drift (trials falling out of the recruiting/date filters) rather
than real registry deletions. [Likely — would need the removed NCT IDs re-queried
individually to confirm; `baseline_clinical_trials.py` does not log them.]

**Category composition (09-01):**

| Category | n |
|---|---|
| Diabetes Recently Completed with Results | 341 |
| Diabetes Technology (Devices) | 243 |
| T1D Cure & Cell Therapy | 156 |
| T2D Novel Therapies (Phase 2-3) | 149 |
| T1D Immunotherapy & Prevention | 76 |

**Phase 3 RECRUITING: 57 trials.** Newest postings:

| NCT | First posted | Sponsor | Agent / focus |
|---|---|---|---|
| NCT07754461 | 2026-08-10 | Boehringer Ingelheim | Survodutide, T2D |
| NCT07743983 | 2026-08-04 | BrightGene | BGM0504, early T2DM + obesity |
| NCT07743450 | 2026-08-03 | Ascletis | ASC30, oral once-daily |
| NCT07684144 | 2026-07-06 | Amgen | (MariTide extension) |
| NCT07670416 | 2026-06-26 | Roche | Enicepatide, obesity |
| NCT07664553 / 62044 / 62109 / 62213 / 62135 | 2026-06-23/24 | AstraZeneca | **Elecoglipron — 5 simultaneous Ph3 starts** |

The AstraZeneca elecoglipron cluster (5 Phase 3 trials registered within 48 hours) is
the single largest coordinated program entry in the corpus this quarter and is not
represented in the tracker. [Certain — from corpus]

**Key-organization status (09-01):**

- **Vertex — 3 trials.** NCT04786262 (VX-880, Ph3, RECRUITING), NCT06832410 (VX-880, Ph3,
  RECRUITING), NCT05791201 (VX-264, Ph1/2, ACTIVE_NOT_RECRUITING). No results posted on
  any. Note: zimislecel is VX-880's INN — **0 PubMed hits for "zimislecel" this window**,
  so the literature has not caught up to the registry name. [Certain]
- **Eli Lilly — 33 trials.** Two Ph3 baricitinib T1D trials recruiting (NCT07222332
  beta-cell preservation; NCT07222137 delay of Stage 3). Orforglipron Ph3 NCT07613307
  recruiting. NCT04255433 (SURPASS-CVOT) COMPLETED, **results posted 2026-07-08** — see §5.
- **Novo Nordisk — 28 trials.** CagriSema Ph3 NCT07564414 recruiting; insulin icodec Ph3
  NCT07076199 recruiting; NCT04596631 (oral semaglutide) results posted **2026-08-21**.
- **Sana Biotechnology — 0 trials** in corpus. Sana's UP421 hypoimmune islet work is
  investigator-initiated in Sweden and not registered under a Sana sponsor string, so the
  keyword query misses it. **This is a known blind spot in `baseline_clinical_trials.py`,
  not an absence of activity.** [Likely]

---

## 3. PubMed Highlights

Window 2026/08/02 → 2026/09/01 · 160 unique papers · 16 domains · 8 tracked therapies.
Diff vs 08-28 snapshot: **79 new, 82 dropped** (rolling 30-day window, so churn is expected).

### Cross-domain papers — highest priority

17 papers in the current window span ≥2 alert domains; 9 are new since 08-28.

**Three-domain (highest value):**

| PMID | Domains | Title |
|---|---|---|
| 42626948 | T1D Stem Cell Cure · T1D Immunotherapy · teplizumab | Gene-edited hypoimmune islets as a cure for T1D: immunology review |
| 42670002 | Microbiome · Gene Therapy · Closed Loop AP | Targeting Autoimmunity in T1D: Emerging Immunomodulatory Therapies |
| 42673585 | orforglipron · retatrutide · CagriSema | GLP-1 RA and co-agonists for weight loss — *Ann Intern Med*, 2026-09-01 |

**PMID 42626948 is the one to read first.** It sits directly on the Vertex/Sana axis
(hypoimmune gene-edited islets) and is the only paper this window connecting the stem-cell
cure literature to immunotherapy *and* to a tracked therapy. Tier 1 §3 (Clinical Trial
Intelligence) + Tier 1 §2 (Literature Synthesis) both apply. [Certain]

**PMID 42673585** (*Annals of Internal Medicine*, Sep 1) is a head-to-head synthesis
across all three of the hub's tracked incretin agents in one paper — the closest thing
to a ready-made comparator table the corpus has surfaced. [Certain]

**Two-domain, new this window:**

- 42674789 — AI/ML · LADA — algorithmic diabetes classification in population cohorts (*BMJ Open*).
  **Directly on the LADA diagnostic model work.** Also relevant to gap-report row "AI/ML Predict × LADA" (score 82.0).
- 42667586 — AI/ML · Multi-Omics — non-oncology biomarkers in precision medicine.
- 42661879 — Biomarker · Multi-Omics — supervised contrastive learning for multi-omics prediction.
  **Tier 1 §1 (Multi-Omics Biomarker Integration, 19/20) — method paper, directly usable.**
- 42666243 — Gene Therapy · Complications — LepR knockout hamster T2D model.
- 42668961 — Biomarker · Complications — DKD pathogenesis + TCM intervention.
- 42661785 — GLP-1 · Remission — Potentilla discolor flavonoids, gut microbiota.
- 42437645 — GLP-1 Pharmacogenomics · orforglipron — variant-specific pharmacophoric shifts in GLP-1R.

### Tracked-therapy volume (30-day window, count vs prior snapshot)

| Therapy | 09-01 | 08-28 | Δ |
|---|---|---|---|
| dapagliflozin | 32 | 34 | −2 |
| orforglipron | 12 | 12 | 0 |
| retatrutide | 8 | 10 | −2 |
| icodec | 8 | 6 | **+2** |
| teplizumab | 4 | 4 | 0 |
| CagriSema | 3 | 4 | −1 |
| baricitinib | 2 | 3 | −1 |
| **zimislecel** | **0** | **0** | **0** |

`zimislecel` has returned 0 for every snapshot on record. Either the literature genuinely
has not adopted the INN, or the query is wrong. **Verify by hand once** — a permanently
zero alert is indistinguishable from a broken one. [Guessing on cause; the zero itself is Certain.]

`baricitinib` at 2 papers is low given two active Lilly Phase 3 T1D trials. PMID 42627334
(β-cell function 1 year after stopping oral baricitinib) is the substantive one and is
cross-domain (T1D Immunotherapy × baricitinib). [Certain]

---

## 4. Gap Analysis Summary

**Input is stale.** `literature_gap_report.md` was re-rendered 2026-09-04, but
`literature_gap_data.json` is dated 2026-07-18 with `date_range: 2020/01/01 to 2026/07/17`.
The report is a fresh presentation of 49-day-old counts. Treat the numbers as of July 17. [Certain]

**Top 5 raw gap scores (all 100.0, ranked by expected-count magnitude):**

| # | Intersection | d1 pubs | d2 pubs | Expected | Actual | Doctrine tier |
|---|---|---|---|---|---|---|
| 1 | GWAS/Polygenic × Closed Loop AP | 5,335 | 1,906 | 25.4 | 0 | *classified methodologically distinct* |
| 2 | Drug Repurposing × CGM Technology | 609 | 6,729 | 10.2 | 0 | *classified methodologically distinct* |
| 3 | **Treg/CAR-T × Neuropathy** | 953 | 3,160 | 7.5 | 0 | meaningful |
| 4 | **Beta Cell Regen × Health Equity** | 1,463 | 1,990 | 7.3 | 0 | meaningful — **Tier 1 §6** |
| 5 | **Treg/CAR-T × Health Equity** | 953 | 1,990 | 4.7 | 0 | meaningful — **Tier 1 §6** |

Also 100.0 with zero joint pubs: Glucokinase × Health Equity, Gene Therapy × LADA,
Islet Transplant × GWAS.

**Alignment with Tier 1 contribution areas (RESEARCH_DOCTRINE.md):**

- **Tier 1 §6 Epidemiological Data Analysis (17/20)** — four of the top eight gaps are
  `X × Health Equity` with literally zero joint publications (Beta Cell Regen, Treg/CAR-T,
  Glucokinase, Drug Repurposing). Health Equity is a small domain (1,990 pubs) so the
  geometric-mean denominator is forgiving, but *zero* is not a normalization artifact.
  **This is the strongest doctrine-aligned cluster in the gap table.** [Certain on counts;
  BRONZE on interpretation per the report's own validation status.]
- **Tier 1 §2 Literature Synthesis (19/20)** — Gene Therapy × LADA (0 joint) pairs with
  new PMID 42674789 (AI/ML × LADA) and the existing LADA diagnostic model work.
- **Tier 1 §4 Drug Repurposing (18/20)** — Drug Repurposing × Health Equity (0 joint) is
  the doctrine's own stated thesis (repurposed drugs reach underserved populations faster)
  and has no literature behind it.

**Caveat carried forward from the gap report itself:** all classifications are BRONZE
(single analytical source). Zero joint publications is as consistent with terminology
mismatch as with a real gap. Do not promote any of these to a claim without the
PubMed hand-verification step the report's §"How to Use" prescribes.

---

## 5. Breaking News (last 7 days)

**FDA approved Mounjaro (tirzepatide) to reduce cardiovascular risk in adults with T2D —
2026-08-28.** Based on SURPASS-CVOT: 13,299 participants, 640 sites, 30 countries, >4.5
years; head-to-head vs Trulicity (dulaglutide) rather than placebo. MACE-3 12.2% vs 13.1%,
an 8% relative reduction; non-inferiority met. [Likely — multiple concordant secondary
sources incl. Lilly investor release and FDA-adjacent trade press; primary label not
retrieved.]

**Why this is the most important line in this report:** SURPASS-CVOT is **NCT04255433**,
which has been sitting in the hub's own corpus as COMPLETED with **results posted
2026-07-08** — 51 days before the approval and 9 days before the last `*_latest.json`
refresh. The hub had the leading indicator and did not surface it. A monitor whose job
is Tier 1 §3 ("flag trials with unexpected results that deserve attention") should have
raised NCT04255433 in July. It did not, because the results-posted diff only compares
consecutive snapshots and the July 8 posting fell inside the 41-day acquisition outage.

**Fix, concretely:** the results-diff should run against a persistent set of
already-seen `results_posted` NCT IDs, not against the immediately prior snapshot.
Otherwise every posting during any outage window is silently lost forever. [Certain —
this is a logic property of the current diff, verified against the 08-28 → 09-01 run
which reported 0 new results while the corpus contains postings dated 08-21.]

Also within window, lower priority:

- Novo Nordisk NCT04596631 (oral semaglutide) results posted **2026-08-21** — in corpus,
  not surfaced by the diff for the same reason. [Certain]
- Insulin efsitora alfa FDA decision anticipated H2 2026; would be the second weekly
  basal insulin in the US. Lilly NCT05275400 (efsitora Ph3) is COMPLETED with results
  posted 2025-06-03 in the corpus. [Likely]
- Retatrutide: 7 further Phase 3 readouts expected before end of 2026. [Likely]

Nothing else in the 7-day window meets the significance bar.

---

## 6. Recommended Actions

**Ranked. The first two are process; nothing below them matters until they're done.**

1. **Restore acquisition, or change the schedule.** Run on your machine:
   ```
   python Analysis/Scripts/baseline_clinical_trials.py
   python Analysis/Scripts/baseline_pubmed_alerts.py
   python Analysis/Scripts/hub_monitor.py
   ```
   If these can't run daily, set this monitor to weekly. Five reports on one snapshot is
   worse than one report on one snapshot — it buries the staleness signal in volume.

2. **Fix the results-posted diff to use a persistent seen-set.** §5 shows two real
   results postings (NCT04255433 on 07-08, NCT04596631 on 08-21) were lost because the
   diff is snapshot-to-snapshot. One of them preceded an FDA approval. This is the
   highest-value code change available in the hub right now.

3. **Repair or retire the `*_latest.json` pointers.** They are byte-identical copies of
   the July 17 snapshot. Either have the baseline scripts rewrite them atomically, or
   delete them and point all consumers at the newest dated snapshot. Two versions of
   "current" is a correctness hazard for the dashboards and the tracker.

4. **Re-run gap analysis** — input is 49 days old:
   ```
   python Analysis/Scripts/project1_literature_gap_analysis.py
   ```
   Re-rendering the report from stale JSON (as happened 09-04) produces a fresh
   timestamp on old numbers, which is worse than an obviously old file.

5. **Update the tracker** with the AstraZeneca elecoglipron Phase 3 cluster
   (NCT07664553, NCT07662044, NCT07662109, NCT07662213, NCT07662135) and the two Lilly
   baricitinib T1D Phase 3 trials (NCT07222332, NCT07222137). Tracker is 50 days stale.
   Clear `.~lock.Diabetes_Research_Tracker.xlsx#` first.

6. **Read PMID 42626948** (gene-edited hypoimmune islets — Stem Cell Cure × Immunotherapy
   × teplizumab). Highest-value cross-domain paper this window; directly informs the
   Vertex/Sana landscape where the trial corpus is blind.

7. **Read PMID 42661879** (supervised contrastive learning for multi-omics prediction).
   Method paper landing squarely on Tier 1 §1 (19/20).

8. **Hand-verify the `zimislecel` PubMed query.** Zero hits on every snapshot ever taken.
   Confirm it's a real absence, not a broken alert.

9. **Add a Sana Biotechnology / UP421 query path** to `baseline_clinical_trials.py`.
   Sponsor-string matching returns 0; the doctrine names Sana as a key organization.

10. **Refresh `CONTRIBUTION_STRATEGY.md`** — 174 days old and predates the current
    doctrine (08-31).

---

## Evidence Ledger

| Claim | Level | Basis |
|---|---|---|
| Snapshot cadence and file ages | Certain | `stat` on Analysis/Results |
| `*_latest.json` are July 17 copies | Certain | byte-size identity with dated snapshots |
| Trial diff 0 new / 0 status / 0 results | Certain | key-set + field diff, 08-28 vs 09-01 |
| 57 Phase 3 RECRUITING; sponsor counts | Certain | field filter on 09-01 corpus |
| Cross-domain paper list | Certain | `domains` array length >1 in 09-01 corpus |
| Gap scores and rankings | Certain (numbers) / BRONZE (interpretation) | `literature_gap_data.json`, 07-18 |
| Mounjaro CV indication, 08-28 | Likely | multiple concordant secondary sources; label not retrieved |
| SURPASS-CVOT = NCT04255433, results 07-08 | Certain | 09-01 trial corpus |
| Removals are query-boundary drift | Likely | inference; removed NCT IDs not logged |
| `zimislecel` zero is a query fault | Guessing | zero is Certain; cause is not |
| Sana absence is a query blind spot | Likely | 0 sponsor-string matches vs known public activity |

---

*Automated review run — 2026-09-05. Read-only: no existing hub files were modified.*
*Sources for §5: [Lilly investor release](https://investor.lilly.com/news-releases/news-release-details/fda-approves-lillys-mounjaro-tirzepatide-reduce-cardiovascular) · [BioPharm International](https://www.biopharminternational.com/view/fda-approves-mounjaro-to-lower-cardiovascular-risk-in-type-2-diabetes-based-on-surpass-cvot) · [ADA newsroom, retatrutide](https://diabetes.org/newsroom/press-releases/breakthrough-studies-demonstrate-effectiveness-first-triple-hormone-therapy) · [GoodRx upcoming approvals](https://www.goodrx.com/drugs/news/upcoming-fda-approvals)*
