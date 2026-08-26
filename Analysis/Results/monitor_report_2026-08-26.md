# Diabetes Research Hub — Monitor Report

**Run date:** 2026-08-26 (automated, review-only — no existing files modified)
**Prior monitor report:** 2026-08-25
**Data vintage under review:** 2026-07-17 — day **40** of the acquisition freeze

---

## Headline: the freeze is not a network problem, and this run proves it by using the network.

Four days of reports have prescribed a fix at the *machine* layer — register a scheduled task, run
PowerShell, run `run_daily_local.py` locally. That framing quietly carried an assumption nobody
tested: that acquisition has to happen on your desktop.

This automated session reached both source APIs directly, from the scheduled-task sandbox, with no
credentials, no VPN and no local machine involved:

```
eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi   →  200   count = 1,138,682
clinicaltrials.gov/api/v2/studies                    →  200   totalCount = 24,284
```

**[Certain]** — the data sources are reachable from the automation layer that is already running
every morning at 02:36. Forty days of frozen data are not a network failure, not an API failure, and
not a credential failure. They are a *write-authority* failure: five tasks touch this hub and none
of them is permitted to fetch.

That reframes yesterday's escalation question. It is no longer "grant `diabetes-data-pull` authority
to run a local script." It is: **the monitor stack can already do the acquisition itself.** It is
declining to, correctly, because its charter says review-only.

**Decision required from you (this is the whole report's ask):** either
(a) amend one task's charter to permit writing `clinical_trials_snapshot_*.json` /
`pubmed_recent_snapshot_*.json`, or (b) run the local pull. Option (a) removes the dependency on you
being at the keyboard, which is the dependency that has failed 40 times.

I did not do (a) unilaterally. This run's charter forbids modifying files, and a monitor that
rewrites its own permissions is a worse defect than the one it fixes.

---

## What this run contributed that a re-print would not

The 08-24 and 08-25 reports both listed a test that "runs against frozen data — available today, no
pipeline required": re-query the Health Equity intersections with expanded vocabulary to determine
whether the top gaps are terminology artifacts. It was listed twice and run zero times.

**I ran it.** 26 live PubMed queries, same date window as the frozen analysis
(2020/01/01–2026/07/17). Result below. It resolves a **[Guessing]** to **[Certain]** and it changes
what the gap table means.

---

## Finding 1 — The equity gaps split cleanly in two, and the hub had them merged

The canonical Health Equity query is `diabetes AND ("health equity" OR "health disparity" OR
"racial disparity")`. Expanding it to 19 standard equity terms (disparities, inequities, social
determinants, socioeconomic, access to care, underserved, minority health, vulnerable populations…)
changes the domain size:

```
Health Equity, canonical   2,016 pubs   ████
Health Equity, expanded   16,519 pubs   ████████████████████████████████   8.19×
```

**[Certain]** — the canonical string captures **12%** of diabetes equity literature. Every equity
pair count in `literature_gap_data.json` is built on that 12%.

The decisive test is not whether joint counts rise — they must — but whether they rise *faster* than
8.19×. A pair that grows proportionally was measuring real sparsity through a narrow lens. A pair
that grows disproportionately was never sparse; it was hidden.

| Partner domain | joint (canon) | joint (expanded) | growth | ÷8.19 | verdict |
|---|---:|---:|---:|---:|---|
| Beta Cell Regen | 0 | **2** | — | — | **real gap** |
| Treg / CAR-T | 1 | **5** | 5.0× | 0.61 | **real gap** |
| Glucokinase | 0 | **5** | — | — | **real gap** |
| Drug Repurposing | 0 | **5** | — | — | **real gap** |
| Islet Transplant | 0 | **0** | — | — | **hard zero** |
| Gene Therapy | 5 | 38 | 7.6× | 0.93 | proportional |
| Neuropathy | 3 | 41 | 13.7× | 1.67 | artifact |
| Autoimmunity T1D | 3 | 49 | 16.3× | 1.99 | artifact |
| Metabolomics | 8 | 133 | 16.6× | 2.03 | artifact |
| Microbiome Gut | 9 | 151 | 16.8× | 2.05 | artifact |
| Insulin Resistance | 7 | 127 | 18.1× | 2.21 | artifact |
| Epigenetics | 6 | 143 | 23.8× | 2.91 | artifact |

```
  lift vs. vocabulary expansion (1.0 = pair grew exactly as much as the domain)
                    0.5      1.0      1.5      2.0      2.5      3.0
  Treg/CAR-T         ●■■■■■■■■│
  Gene Therapy       ■■■■■■■■●│
  Neuropathy         ■■■■■■■■■■■■■■●
  Autoimmunity T1D   ■■■■■■■■■■■■■■■■■●
  Metabolomics       ■■■■■■■■■■■■■■■■■●
  Microbiome Gut     ■■■■■■■■■■■■■■■■■●
  Insulin Resistance ■■■■■■■■■■■■■■■■■■■●
  Epigenetics        ■■■■■■■■■■■■■■■■■■■■■■■■■■■●
                              │
                        real ←┼→ artifact
```

**What this means, concretely:**

1. **The four top-ranked equity gaps survive.** Beta Cell Regen, Treg/CAR-T, Glucokinase and Drug
   Repurposing × Health Equity remain at 2–5 joint publications against an equity corpus eight times
   larger. That is genuine absolute sparsity, not a vocabulary artifact. **Ranks 2, 3, 4 and 6 of the
   "Potentially Meaningful" table are confirmed.** Drug Repurposing × Health Equity is double-Tier-1
   (Doctrine #4, 18/20 and #6, 17/20) and is now the best-evidenced target in the hub.

2. **Six mid-tier "unclassified" equity gaps evaporate.** Insulin Resistance × HE (93.0),
   Metabolomics × HE (87.1), Autoimmunity T1D × HE (86.8), Microbiome × HE (84.5), Epigenetics × HE
   (84.0), Neuropathy × HE (80.9) each grew ~2–3× faster than the vocabulary. Their literature
   exists; the query could not see it. **[Certain]** — these six should be reclassified out of the
   gap table, not sent to expert review.

3. **A new hard zero worth recording:** Islet Transplant × Health Equity returns **0 papers even
   under the expanded query**. Islet Transplant is the smallest domain (248 pubs) so expectation is
   low, but a true zero against a 16,519-paper equity corpus is a different object than a zero
   against 2,016. Not currently ranked in the hub at all.

The tell for the whole class: `Gene Therapy × HE` sits at lift 0.93 — almost exactly proportional.
That is what "the query was narrow but the gap was real" looks like, and it validates the test as
discriminating rather than just inflating everything.

---

## Finding 2 — Correcting a claim the hub carried for two days

The 08-24 and 08-25 reports logged **Garzulys (insulin aspart-fsan)** as *"first rapid-acting insulin
biosimilar to NovoLog"*, with a date disputed between 07-24 and 07-30. Both parts needed fixing.

| | 08-25 report said | Corrected |
|---|---|---|
| Ordinal | "first rapid-acting insulin biosimilar" | **third** insulin aspart biosimilar referencing NovoLog, after Kirsty (aspart-xjhz) and Merilog (aspart-szjj) |
| Date | disputed 07-24 vs 07-30 | **2026-07-30**, Meitheal/BusinessWire announcement |
| Sponsor | not recorded | Meitheal Pharmaceuticals (US agent); Emerge holds the BLA |

Root cause of the "07-24" figure: a search result conflating Garzulys with the FDA press release
*"FDA Approves First Rapid-Acting Insulin Biosimilar Product"* — which I fetched directly. That
release is dated **February 14, 2025** and is about **Merilog** (Sanofi), not Garzulys. The "first"
language and a wrong date both came from the same mismatched source.

**[Certain]** on the Merilog release contents (primary FDA fetch). **[Likely]** on 2026-07-30 as the
approval date — the company announcement is corroborated by four independent trade outlets, but an
announcement date is not necessarily the FDA action date. Definitive resolution requires the Drugs@FDA
approval record; not treated as settled here.

Method note worth generalizing: this error survived two reports because a search snippet was treated
as a source. Fetching the underlying page took one call and reversed the claim.

---

## Finding 3 — The 100.0 tie, broken

`literature_gap_data.json` already contains `expected`, which discriminates cleanly across the ten
pairs the report presents as ranks 1–10. Re-ranking by **absolute shortfall** (`expected − joint`),
using only data already on disk:

| # | Pair | gap | joint | expected | shortfall |
|---:|---|---:|---:|---:|---:|
| 1 | Nephropathy DKD × Gestational DM | 95.5 | 24 | 535.1 | **511** |
| 2 | Neuropathy × Gestational DM | 96.7 | 4 | 120.3 | **116** |
| 3 | Insulin Resistance × Closed Loop / AP | 96.9 | 3 | 95.4 | **92** |
| 4 | GWAS / Polygenic × CGM Technology | 96.7 | 3 | 89.8 | **87** |
| 5 | GWAS / Polygenic × Closed Loop / AP | 100.0 | 0 | 25.4 | 25 |
| 6 | Drug Repurposing × CGM Technology | 100.0 | 0 | 10.2 | 10 |
| 7 | Treg / CAR-T × Neuropathy | 100.0 | 0 | 7.5 | 8 |
| 8 | Beta Cell Regen × Health Equity | 100.0 | 0 | 7.3 | 7 |

The current report's rank 1 (Treg/CAR-T × Neuropathy) falls to 7th. Four pairs with *larger absolute
missing literature* are ranked below it or omitted entirely, because a 95.5 sorts below a 100.0 even
when it represents 511 missing papers versus 8.

**[Certain]** — the gap score saturates at `joint == 0` and cannot rank beyond that point. Ranks 1–10
of the current output are an arbitrary tie-break presented as an ordering. Note that ranks 3 and 5
here are pairs the report files under *"Methodologically Distinct — deprioritize"*; that
classification may be right, but it is being applied to the two largest genuinely-unexplored
intersections in the set and deserves a second look rather than an automatic dismissal.

---

## File System Status

| File | Modified | Age | State |
|---|---|---|---|
| `clinical_trials_latest.json` | 2026-07-17 | 40 d | **STALE** |
| `pubmed_recent_latest.json` | 2026-07-17 | 40 d | **STALE** |
| `hub_monitor_report.md` | 2026-07-17 | 40 d | **STALE** |
| `literature_gap_data.json` | 2026-07-18 | 39 d | **STALE** — `date_range` ends 2026/07/17 |
| `literature_gap_report.md` | 2026-08-25 03:19 | 1 d | **MISLEADING** — header re-stamped, data static |
| newest snapshot of either kind | `*_2026-07-17.json` | 40 d | no new snapshot in 40 days |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | 40 d | unchanged |

The freshness illusion recurred on schedule for the third consecutive day: `literature_gap_report.md`
now reads **"Generated: 2026-08-25 03:19"** over **"Date range: 2020/01/01 to 2026/07/17"**. The
header has advanced three days over data that has not moved. Remains **P1** — self-concealing.

---

## Clinical Trial Changes

**Zero.** No snapshot taken to diff. Last real diff on record: 07-16 → 07-17 (1 new, 1 removed, 0
status changes, 0 new results). Composition unchanged: 858 trials, 269 RECRUITING, 52 Phase 3
RECRUITING, 322 with a `results_posted` date (newest 2026-07-16).

**New data-quality defect found this run:** the `has_results` boolean is **`false` on all 858
records**, including the 322 that carry a populated `results_posted` date. **[Certain]** — the field
is written but never set by `baseline_clinical_trials.py`. Any downstream filter or dashboard keyed
on `has_results` silently returns an empty set. Worth a grep before the next pull; the field is
cheap to derive from `results_posted` and should either be fixed or removed.

### Drift, recounted

```
119  trials whose recorded completion_date has passed but status ≠ COMPLETED   (08-25: 119)
 15  crossed during the freeze                                                 (08-25:  15)
  7  of those Phase 2 or Phase 3                                               (08-25:   7)
```

**No new record went wrong overnight.** This corrects yesterday's "roughly one every two days"
framing — the crossings are lumpy (four fell on 08-01 alone), not a steady rate. Projections from
that rate should not be quoted.

Phase 2/3 verification set for the first post-fix pull — if these do not flip to COMPLETED,
acquisition ran but is not refreshing:

| NCT | Completion | Reported status | Phase | Sponsor |
|---|---|---|---|---|
| NCT07064486 | 2026-07-31 | RECRUITING | 3 | BrightGene (BGM0504) |
| NCT07321678 | 2026-08-01 | ACTIVE_NOT_RECRUITING | 2 | Ascletis Pharma |
| NCT07271251 | 2026-08-03 | ACTIVE_NOT_RECRUITING | 3 | Novo Nordisk (oral semaglutide) |
| NCT06926842 | 2026-08-13 | ACTIVE_NOT_RECRUITING | 2 | Zealand Pharma (petrelintide) |
| NCT06810726 | 2026-08-15 | RECRUITING | 2 | Estar Medical |
| NCT06797869 | 2026-08-21 | ACTIVE_NOT_RECRUITING | 2 | Novo Nordisk (CagriSema) |
| NCT06716203 | 2026-08-25 | RECRUITING | 3 | BrightGene (BGM0504) |

Ten more cross by 09-09, six of them on 09-01 — Sanofi NCT05757713 (Ph4, 08-27), Insulet NCT07593625
(08-30), 2nd Affiliated Guangzhou NCT07374328 (Ph1/2, 08-31), then SAVA, Ain Shams (Ph2/3), Gasherbrum
(Ph2), UCSF, Ramathibodi, Aalborg on 09-01, and Hohendorff 09-09.

**Key organizations, unchanged:** Vertex 3 (VX-880 Ph3 ×2 RECRUITING, VX-264 Ph1/2), Lilly 33, Novo
Nordisk 28, **Sana Biotechnology 0**. The Sana zero and the zimislecel ↔ VX-880 vocabulary split both
remain open. Note the parallel: the Sana zero, the zimislecel zero and the equity gaps resolved above
are all the same defect class — a query string narrower than the literature it is meant to cover. The
equity test is now a template for testing the other two.

---

## PubMed Highlights

158 unique papers, 16 domains, 30-day lookback ending 2026-07-17. Thirteen domains return exactly 10
papers — the result cap, not a measurement. **No publication-volume trend can be read from this
file.**

Cross-domain: 12 of 158 (7.6%), unchanged. Key-therapy tracking still capped and still reporting
zimislecel = 0 (vocabulary artifact — indexed as VX-880 in trial contexts).

**Unreviewed for 40 days — PMID 42459945**, *"A framework for assessing algorithmic discrimination
risks in training data: a case of pediatric type 1 diabetes"* (JAMIA open, 2026-Aug). The only
triple-domain paper in the corpus: AI/ML × Closed Loop AP × Health Equity — the Doctrine #5 (18/20)
and #6 (17/20) seam. Given Finding 1, it is now more relevant, not less: it is a rare instance of the
equity-methods crossover the gap analysis says is missing. Fourth consecutive recommendation, and it
requires only twenty minutes of reading.

---

## Gap Analysis Summary — top 5, as revised by this run

| # | Pair | Status after today's test |
|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | untested (no equity term); gap score 100.0, expected 7.5 |
| 2 | Beta Cell Regen × Health Equity | **CONFIRMED** — 2 papers under 8.19× expanded query |
| 3 | Treg / CAR-T × Health Equity | **CONFIRMED** — 5 papers, lift 0.61 |
| 4 | Glucokinase × Health Equity | **CONFIRMED** — 5 papers |
| 5 | Gene Therapy × LADA | untested; both domains small (2,296 / 582) |
| 6 | Drug Repurposing × Health Equity | **CONFIRMED** — 5 papers; **double Tier 1 (#4 18/20, #6 17/20)** |

Validation level moves **BRONZE → SILVER** for the four confirmed equity pairs: two independent
query formulations, one deliberately adversarial to the finding, agree. Expert confirmation still
outstanding, which is what keeps it below GOLD.

### Tier 1 alignment

- **Doctrine #4 Drug Repurposing (18/20) × #6 Epidemiological/equity (17/20)** — the strongest
  confirmed target in the hub. Repurposing is a 609-publication domain; equity crossover is 5 papers.
  Both halves are explicitly in scope for computational contribution.
- **Doctrine #6** also owns Beta Cell Regen × HE, Treg/CAR-T × HE, Glucokinase × HE.
- **Doctrine #2 Literature Synthesis (19/20)** — the six reclassified artifact pairs are a finding in
  their own right: *equity work in diabetes subfields is systematically invisible to standard equity
  search terms.* That is a publishable methods observation, not merely a hub bug.

---

## Breaking News (web check, 08-19 → 08-26)

**Nothing new clears the significance bar.** Searches for Phase 3 diabetes results and FDA diabetes
approvals in the last seven days surfaced only previously-logged material:

- **Retatrutide TRANSCEND-T2D-1** (Lancet) — HbA1c −1.7 to −1.9% vs −0.8% placebo at 40 weeks;
  weight −11.5% to −15.3% vs −2.6%. *Level 1b.* Already logged 08-24. Seven further Phase 3 readouts
  guided before end of 2026.
- **Garzulys** — corrected above; see Finding 2.
- **Novo amycretin** — Phase 2 data reported as setting up Phase 3 in diabetes. **[Guessing]** on
  status; no NCT identified, and the hub's frozen registry cannot confirm. Flag for the first
  post-fix pull rather than logging as a claim.
- **CagriSema REIMAGINE 1/2** — in corpus since 2026-06-10. No action.
- **Zimislecel (VX-880)** — still not approved; submissions guided 2026, availability 2027. No change.

Nothing found this week contradicts an existing hub claim other than the Garzulys correction.

---

## Recommended Actions

**P0 — one decision, not one command**

1. **Choose the acquisition owner.** Both source APIs are reachable from the automation sandbox
   (proven this run). Either:
   - **(a)** amend `diabetes-data-pull`'s charter to write snapshots when its own freshness check
     fails — removes the dependency on you being at the keyboard, which has failed 40 times; or
   - **(b)** run locally: `python "C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts\run_daily_local.py"`

   Success criterion either way: `clinical_trials_snapshot_2026-08-26.json` exists and
   `literature_gap_data.json` `date_range` ends 2026/08/26.

**P1 — apply today's findings**

2. **Widen the Health Equity query** in `project1_literature_gap_analysis.py` to the 19-term
   expansion and re-run. Six pairs will drop out of the gap table; four will harden. Do this *before*
   the next gap run, or the next run re-computes the same six false gaps.
3. **Reclassify** Insulin Resistance, Metabolomics, Autoimmunity T1D, Microbiome, Epigenetics and
   Neuropathy × Health Equity out of "Unclassified — requires expert review." They do not need an
   expert; they needed a better query, and now have one.
4. **Stamp source-data vintage, not render time,** in every report and dashboard generator. Third
   consecutive day the gap report header advanced over static data.
5. **Re-rank by expected shortfall** alongside gap score. `expected` is already in the file; the
   change is a sort key.
6. Apply the same synonym test to the two other suspected query defects: **Sana Biotechnology** (0
   trials for a tracked key organization) and **zimislecel ↔ VX-880**. Same defect class, same fix,
   and both run against frozen data.

**P2**

7. Print the executed step list at the top of every orchestrator log.
8. Raise the therapy-hit and per-domain result caps in `baseline_pubmed_alerts.py` — the current caps
   make volume trends unreadable.
9. Resolve Garzulys's approval date against the Drugs@FDA record and correct the 08-24/08-25 entries.
10. Fix or drop the `has_results` field in `baseline_clinical_trials.py` — currently false on 100% of
    records, so any filter using it returns nothing.
11. Register the local scheduled task — optional if you take 1(a).

**P3**

11. Read **PMID 42459945**. Fourth consecutive recommendation; twenty minutes.

---

## Evidence Levels (per Research Doctrine)

| Claim | Level | Basis |
|---|---|---|
| Both source APIs reachable from the automation sandbox | **[Certain]** | live HTTP 200 from eutils (count 1,138,682) and CTG v2 (totalCount 24,284) this run |
| Pipeline has not acquired since 2026-07-17 | **[Certain]** | newest snapshot of either kind is `*_2026-07-17.json`; latest files unchanged |
| Canonical Health Equity query captures 12% of the domain | **[Certain]** | 2,016 vs 16,519 on identical date window, live esearch |
| Four top equity gaps are real, not vocabulary artifacts | **[Certain]** on counts, **SILVER** on interpretation | joint ≤5 under 8.19× expanded query; two independent formulations agree |
| Six mid-tier equity gaps are terminology artifacts | **[Certain]** | joint counts grew 1.7–2.9× faster than the domain itself |
| Islet Transplant × Health Equity is a hard zero | **[Certain]** | 0 under both canonical and expanded queries |
| Garzulys is the third aspart biosimilar, not the first | **[Certain]** | FDA press release fetched directly: "first rapid-acting" = Merilog, 2025-02-14 |
| Garzulys approved 2026-07-30 | **[Likely]** | company announcement + four trade outlets; not a Drugs@FDA primary record |
| 119 trials mis-stated, 15 during freeze, 7 Phase 2/3 | **[Certain]** | computed from the snapshot's own `completion_date` vs `status` |
| Gap score cannot rank pairs where joint == 0 | **[Certain]** | formula saturates; ten pairs tie at exactly 100.0 |
| Gap report re-stamps render time over static data | **[Certain]** | header 2026-08-25 03:19 vs `date_range` ending 2026/07/17 |
| `has_results` is false on all 858 trial records | **[Certain]** | direct count; 322 records carry `results_posted` yet none has `has_results == true` |
| Retatrutide TRANSCEND-T2D-1 results | **Level 1b** | peer-reviewed, The Lancet |
| Amycretin advancing to Phase 3 | **[Guessing]** | trade press only; no NCT identified |
| Sana zero and zimislecel zero are query defects | **[Likely]** | same defect class as the equity finding, now demonstrated; untested for these two specifically |

---

## Sources consulted this run

- [Retatrutide TRANSCEND-T2D-1 — The Lancet](https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(26)00967-0/abstract)
- [FDA Approves First Rapid-Acting Insulin Biosimilar Product (Merilog, 2025-02-14)](https://www.fda.gov/news-events/press-announcements/fda-approves-first-rapid-acting-insulin-biosimilar-product-treatment-diabetes)
- [Meitheal announces FDA approval of Garzulys (2026-07-30)](https://www.businesswire.com/news/home/20260730232521/en/Meitheal-Pharmaceuticals-Announces-FDA-Approval-of-Garzulys-insulin-aspart-fsan-Injection)
- [FDA Approves Garzulys (insulin aspart-fsan), a Biosimilar to NovoLog — Drugs.com](https://www.drugs.com/newdrugs/fda-approves-garzulys-insulin-aspart-fsan-biosimilar-novolog-6851.html)
- [FDA Approves Meitheal's Insulin Aspart Biosimilar Garzulys — Big Molecule Watch](http://www.bigmoleculewatch.com/2026/08/07/fda-approves-meitheal-pharmaceuticals-insulin-aspart-biosimilar-garzulys/)
- [Data sets up phase 3 trials for Novo's amycretin — pharmaphorum](https://pharmaphorum.com/news/data-sets-phase-3-trials-novos-amycretin-diabetes)
- NCBI E-utilities esearch (26 live queries, 2020/01/01–2026/07/17 window)
- ClinicalTrials.gov API v2 (reachability check only)

---

*Generated by the Diabetes Research Hub monitor — review-only run, 2026-08-26. No existing files were modified. This report is the only file written.*
