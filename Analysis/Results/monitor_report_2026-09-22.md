# Hub Monitor Review — 2026-09-22

**Run type:** automated review (read-only; no existing files modified)
**Workspace:** `Diabetes_Research`
**Previous review:** `monitor_report_2026-09-21.md`
**Scan time:** 2026-09-22 07:37 UTC

---

## 0. Lead findings

**1. Yesterday's lead finding was wrong, and the error is a timing artifact you should fix.**
`[Certain]` Yesterday's report (written 02:41) declared *"the nightly pipeline did not run last
night. Zero files carry a 2026-09-21 timestamp."* Four files carry a 2026-09-21 timestamp:

```
2026-09-21 03:18  builder_compile_audit.json
2026-09-21 03:18  endpoint_value_agreement_audit.json
2026-09-21 03:18  endpoint_value_unsourced_baseline.json
2026-09-21 03:19  agent_state.json
2026-09-21 03:21  ACTION_REQUIRED_2026-09-21.md   (repo root)
```

The monitor ran at **02:41**; the pipeline ran at **03:18–03:21**. The monitor is scheduled
*ahead of* the job it is supposed to audit, so it can only ever see the previous day's output
and will keep reporting false "pipeline down" alarms. **This is a scheduling bug, not a
pipeline failure.** Move the monitor to ≥ 04:00, or have it read `agent_state.json`'s own
timestamp rather than inferring from file mtimes.

**2. The pipeline is running, but only half of it is.**
`[Certain]` The 09-21 run wrote state and audit artifacts. It did **not** write
`pubmed_recent_*` (newest 09-20), any `clinical_trials_snapshot_*` (newest **09-06**), or
`literature_gap_*` (newest 09-20). The acquisition stage has been silent for 16 days on trials
and 2 days on PubMed. Diagnosis is unchanged from yesterday and still correct.

**3. Nothing has been written today.**
`[Certain]` Zero files in the hub carry a 2026-09-22 timestamp as of 07:37 UTC — and today the
inference is sound, because 07:37 is four hours past the pipeline's usual 03:1x window.

---

## 1. File system status

| File | Age | Last modified | Verdict |
|---|---:|---|---|
| `agent_state.json` | 1d | 2026-09-21 03:19 | current |
| `pubmed_recent_latest.json` | 2d | 2026-09-20 03:20 | current |
| `literature_gap_report.md` | 2d | 2026-09-20 03:16 | current |
| `literature_gap_data.json` | 3d | 2026-09-19 03:26 | current |
| `clinical_trials_snapshot_2026-09-06.json` | **16d** | 2026-09-06 02:38 | **stale** |
| `clinical_trials_latest.json` | **67d** | 2026-07-17 02:05 | **broken pointer** |
| `clinical_trials_summary.md` | 67d | 2026-07-17 02:05 | **stale** |
| `hub_monitor_report.md` | **67d** | 2026-07-17 02:16 | **stale — script not running** |
| `Diabetes_Research_Tracker.xlsx` | 67d | 2026-07-17 10:07 | **stale** |
| `RESEARCH_DOCTRINE.md` | 22d | 2026-08-31 03:12 | reference doc, expected |
| `CONTRIBUTION_STRATEGY.md` | 191d | 2026-03-15 | reference doc, expected |

**827 result files flagged >14 days old** by the last `hub_monitor.py` run — that count is
itself 67 days stale and should be treated as a floor, not a measurement.

### 1a. `clinical_trials_latest.json` — root cause confirmed, unchanged

`[Certain]` The `_latest` alias is 67 days old while dated snapshots run through 2026-09-06:

```
clinical_trials_latest.json            generated 2026-07-17T02:05   858 trials
clinical_trials_snapshot_2026-09-06    generated 2026-09-06T02:38   894 trials
```

September snapshots carry `"acquired_by": "cowork scheduled monitor (sandbox) - replicates
baseline_clinical_trials..."` — a *replica* of the acquisition script that writes the dated
snapshot but never updates the alias or `clinical_trials_summary.md`. **Every downstream
consumer reading `_latest` is working from July data.**

PubMed does not have this defect: `pubmed_recent_snapshot_2026-09-20.json` and
`pubmed_recent_latest.json` are byte-identical in content (154 papers, zero set difference).

---

## 2. Clinical trial changes

Diffed `clinical_trials_latest.json` (07-17, n=858) → `clinical_trials_snapshot_2026-09-06.json`
(09-06, n=894). This is a **51-day** diff, not a daily one, because no trial data has been
acquired since 09-06.

```
Trial corpus growth (total registered trials tracked)

07-17  ████████████████████████████████████████      858
08-27  ██████████████████████████████████████████    892
08-28  ██████████████████████████████████████████    893
09-01  █████████████████████████████████████████     887
09-06  ██████████████████████████████████████████    894
       ├─────────────────────── 51 days ──────────────┤   no data after this point
```

**57 new trials · 21 dropped · 26 status changes · 0 new results posted**

### New Phase 3 entrants (highest priority)

| NCT | Sponsor | Status | Title |
|---|---|---|---|
| NCT07797335 | **Novo Nordisk** | RECRUITING | AMBITION 7 — zenagamtide vs. insulin glargine, n=1778, completes 2028-09 |
| NCT07784270 | AstraZeneca | NOT_YET_RECRUITING | AZD6234 in T2D + obesity, n=1500 |
| NCT07776509 | AstraZeneca | NOT_YET_RECRUITING | AZD6234 adjunct to incretin therapy, n=500 |

### Notable Phase 2 entrants

- **NCT07804849** (Ain Shams Univ, Phase 2/3, RECRUITING) — oral **verapamil** in newly
  diagnosed children/adolescents with T1D. Beta-cell preservation via a repurposed
  antihypertensive; sits directly on the **Drug Repurposing** Tier 1 axis.
- **NCT07783802** (Eli Lilly, Phase 2) — clazakizumab (IL-6) in elevated hsCRP / CV risk.
- **NCT07768631** (Endogenex) — pulsENDO duodenal therapy in T2D.

### Status changes worth attention

| NCT | Change | Why it matters |
|---|---|---|
| NCT06334133 | RECRUITING → ACTIVE_NOT_RECRUITING | **Cadisegliatin** (glucokinase activator) Ph3 in T1D fully enrolled — readout pipeline |
| NCT07400653 | RECRUITING → ACTIVE_NOT_RECRUITING | Pfizer PF-08653944 Ph3, n=1044, enrollment closed |
| NCT07076199 | RECRUITING → ACTIVE_NOT_RECRUITING | **Insulin icodec** Ph3 (Novo), n=877, closed |
| NCT07502495 | RECRUITING → ACTIVE_NOT_RECRUITING | **Icovamenib** Ph2 T2D closed |
| NCT07613307 | NOT_YET → RECRUITING | **Orforglipron** in T2D patients observing Ramadan fasting |
| NCT07664553 | NOT_YET → RECRUITING | **Elecoglipron** Ph3 (AstraZeneca) opened |
| NCT07222137 / NCT07222332 | active | **Baricitinib** Ph3 pair (Lilly): delay of Stage 3 T1D (n=150) + beta-cell preservation (n=300) |
| NCT07495956 | RECRUITING → **NOT_YET_RECRUITING** | cfMSC therapy for diabetes *regressed* — possible hold or protocol amendment; worth checking |

### Key-organization Phase 3 watchlist (status as of 09-06)

- **Vertex** — NCT04786262 (VX-880 + VX-017, n=57, completes 2031) and NCT06832410
  (VX-880 in kidney-transplant recipients, n=10, completes 2027-09). Both RECRUITING.
- **Sana Biotechnology** — `[Certain]` **zero** trials in the corpus. Either the query set
  misses them or Sana's hypoimmune islet work is not yet registered. Worth a targeted check.
- **"zimislecel"** — `[Certain]` **zero** string matches in the trial corpus and **zero**
  PubMed hits in the 30-day window. The corpus indexes it only as VX-880. If you are tracking
  zimislecel by name, the tracker will silently return nothing.
- **Sanofi** NCT07088068 — teplizumab Ph3, n=723, RECRUITING, completes 2028-12.
- **0 of 894 trials have posted results** in this corpus. `[Likely]` The "Recently Completed
  with Results" category (n=343) is being populated by completion status rather than by an
  actual `hasResults` flag — the field is present but never true. Worth auditing the query.

---

## 3. PubMed highlights

Window: 30-day lookback, generated 2026-09-20. 154 unique papers, 1,059 query matches,
16 domains, 8 tracked therapies.

### Cross-domain papers (14 of 154 — highest value)

| PMID | Date | Domains | Title |
|---|---|---|---|
| **42759644** | Sep-18 | **3** — T2D GLP-1, Gene Therapy, Multi-Omics | Immunometabolic regulation of macrophage function in cardio-hepatic-renal comorbidities |
| 42720752 | Sep-10 | T1D Immunotherapy + teplizumab | Preserving beta-cell function in children/adolescents with new-onset stage 3 T1D (per-protocol) — *Diabetologia* |
| 42627334 | Aug-21 | T1D Immunotherapy + baricitinib | **Beta-cell function 1 year after stopping oral baricitinib** — *Diabetes Care* |
| 42739778 | Aug-31 | T1D Stem Cell + T1D Immunotherapy | Emerging preservation technologies in pancreas and islet transplantation |
| 42738899 | Sep-03 | T1D Immunotherapy + LADA | BCG immunotherapy: metabolic and immune reprogramming |
| 42756821 | 2026 | Microbiome + Multi-Omics | Multi-omics prioritization of gut-metabolite targets in diabetic kidney disease |
| 42751271 | 2026 | Biomarker + Multi-Omics | Mitochondrial dysfunction in DKD in the omics era |
| 42762173 | Sep-19 | Closed Loop AP + Health Equity | Sustained glycemic outcomes with the MiniMed system |
| 42761395 | 2026 | AI/ML + Drug Repurposing | Digital twins × AI in diabetes: mechanism to full-cycle precision management |
| 42688617 | 2026 | retatrutide + CagriSema | Comparative efficacy/safety of GLP-1-based drugs for weight loss — *BMJ Medicine* |
| 42760621 | Sep-18 | T2D GLP-1 + orforglipron | Orforglipron: an oral GLP-1 RA for obesity |
| 42753877 | Sep-17 | T2D Remission + Multi-Omics | Pharmacological intersections between T2D and cancer |
| 42751099 | Oct | T2D Remission + retatrutide | >100 kg sustained loss with sequential incretin therapy in Prader-Willi |
| 42643804 | 2026 | T1D Immunotherapy + teplizumab | Teplizumab in stage 2 T1D — pediatric considerations |

**Three of these sit squarely on Tier 1 axes** (42759644, 42756821, 42751271 → Multi-Omics
Biomarker Integration; 42761395 → AI/ML + Drug Repurposing). These are the ones to read.

### Key-therapy tracker

```
dapagliflozin  ██████████████████████████████████████████████  46
retatrutide    █████████████  13
orforglipron   ████████████  12
icodec         ███████  7
teplizumab     ██████  6
CagriSema      ███  3
baricitinib    ███  3
zimislecel     ·  0        ← tracked by name only; corpus indexes VX-880
```

`[Certain]` **zimislecel returns 0 across both trials and literature.** This is an alias bug in
the tracker, not an absence of activity — Vertex's Phase 3 program is live (see §5).

### Domain publication volume (30-day PubMed matches)

```
T2D GLP-1 New            ████████████████████████████████████████████  198
Diabetes AI/ML           ██████████████████████████████████████████    188
Diabetes Microbiome      ██████████████████████████████                135
Diabetes Biomarker       ████████████████████████                      110
Diabetes Health Equity   ██████████████                                 61
Diabetes Gene Therapy    █████████████                                  57
Diabetes Multi-Omics     █████████████                                  57
T2D Remission            ████████████                                   55
Closed Loop AP           ██████                                         26
Diabetes Complications   ██████                                         26
T1D Immunotherapy        █████                                          22
T1D Stem Cell Cure       ███                                            15
LADA New Research        ██                                             10
Diabetes Drug Repurpose  ·                                               3
Diabetes Epigenetics     ·                                               3
GLP-1 Pharmacogenomics   ·                                               3
```

**Read this chart twice.** The three domains at the bottom — Drug Repurposing, Epigenetics,
GLP-1 Pharmacogenomics — return **3 matches each**, an implausibly round triple. `[Likely]`
These three queries are malformed or over-constrained rather than genuinely empty; PubMed
returning exactly 3 for three unrelated topics in a 30-day window is a query artifact, not a
signal about the field. Drug Repurposing is a **Tier 1** area, so a broken query there is a
live blind spot. **Verify before treating any of these as evidence of a gap.**

### Volume trend

```
snapshot     papers   new vs. prior
09-01          160    —
09-05          141    78
09-06          139    18
09-18          151   104
09-20          154    46
```

Turnover is high relative to corpus size (46 new papers in a 2-day gap) because the 30-day
window slides. No anomaly.

---

## 4. Gap analysis summary

Source: `literature_gap_data.json` (09-19) + `literature_gap_report.md` (09-20).
30 domains, 435 pairs, PubMed 2020-01-01 → 2026-09-19. **Validation level: BRONZE** — single
analytical source, per doctrine §BRONZE, must not be presented as established fact.

### Top 5 under-researched intersections (report's *meaningful* ranking, not raw gap score)

| # | Intersection | Gap | Joint pubs | Tier 1 alignment |
|---|---|---:|---:|---|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | **Tier 1 #6** — Epidemiological / disparity analysis |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | — |
| 3 | Islet Transplant × Drug Repurposing | 100.0 | 0 | **Tier 1 #4** — Drug Repurposing Screening |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | **Tier 1 #6** |
| 5 | Gene Therapy × LADA | 100.0 | 0 | — |

Also on Tier 1 axes, ranked 6–12: Glucokinase × Drug Repurposing (#6), Drug Repurposing ×
Health Equity (#10), Drug Repurposing × LADA (#11).

**Seven of the top twelve meaningful gaps involve either Drug Repurposing or Health Equity** —
Tier 1 areas #4 and #6. That concentration is the actionable finding: the gap analysis and the
doctrine agree on where to work.

### Caveat with teeth

`[Certain]` The raw `ranked_gaps` array is **not** the same as the report's meaningful ranking.
Raw rank #3 (`Islet Transplant × GWAS/Polygenic`), #7 (`GWAS × Closed Loop`), #8 (`GWAS × CGM`)
are all classified in the report as *methodologically distinct* — expected low overlap, not
opportunity. Any script that consumes `literature_gap_data.json` directly and takes the top-N
by `gap_score` will surface these as findings. **That is a live risk to any downstream builder.**

One entry — Islet Transplant × Drug Repurposing — carries a manual re-verification note dated
2026-09-06 (7 all-time records, none a computational drug screen). That is the only gap in the
list with verification beyond the automated count. The rest remain BRONZE.

---

## 5. Breaking news (web check, last ~7 days)

Three items clear the significance bar. Evidence level noted per doctrine.

1. **Retatrutide Phase 3 TRANSCEND-T2D-1 published in *The Lancet*.** `[Likely — SILVER]`
   Once-weekly retatrutide vs. placebo, n=537, T2D. HbA1c −18.5 / −20.3 / −21.2 mmol/mol
   (4/9/12 mg) vs. −8.9 placebo at 40 weeks; weight −11.5% to −15.3% vs. −2.6%. Two independent
   secondary sources; primary abstract not yet read into the corpus.
   → **Our corpus has NCT06260722 (retatrutide vs. semaglutide, n=1250) as
   ACTIVE_NOT_RECRUITING with `has_results: false`.** The registry-based results flag is not
   catching publications. This is the gap between trial intelligence and literature intelligence.

2. **CagriSema Phase 3a REIMAGINE 1.** `[Likely — SILVER]` n=189 T2D adults; HbA1c
   −19.7 / −16.4 mmol/mol vs. −1.1 placebo at 40 weeks. Corpus has NCT07564414 (n=2500,
   RECRUITING) and NCT07282613 (pediatric, NOT_YET_RECRUITING).

3. **Zimislecel (VX-880) regulatory submissions expected in 2026.** `[Likely — SILVER]` FDA /
   EMA / MHRA. Fast Track + RMAT designations held. Phase 1/2: 10 of 12 participants insulin-
   independent at ≥1 year. Availability possibly as early as 2027.
   → Note the doctrine's own §GOLD discussion already demotes the zimislecel insulin-
   independence finding to SILVER (three sources, one underlying cohort). **Do not re-promote
   it.** The corpus's zero-match on the name is a separate, mechanical problem (§3).

Nothing found constituting an FDA *approval* action on a diabetes drug in the last 7 days.
Pending 2H-2026 decisions referenced in secondary sources: insulin efsitora alfa (weekly basal),
tirzepatide CV-risk-reduction indication. `[Guessing]` on timing — no primary FDA source read.

---

## 6. Recommended actions

**P0 — fix the monitor's own schedule.** The monitor runs at 02:41, the pipeline at 03:18.
Every run is auditing yesterday and two consecutive reports have now opened with a
false "pipeline down" headline. Move the monitor to ≥ 04:00 UTC, or key staleness off
`agent_state.json.generated` instead of file mtimes.

**P0 — repair the `_latest` alias.** Trial data is 67 days old for every consumer reading
`clinical_trials_latest.json`. Two options, in order of preference:
```
# (a) fix the replica to write the alias, or
# (b) stopgap, run locally:
cd 'C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Results'
copy clinical_trials_snapshot_2026-09-06.json clinical_trials_latest.json
```
Then re-run the real acquisition to close the 16-day trial gap:
```
python baseline_clinical_trials.py
```

**P1 — refresh the stalled scripts.**
```
python hub_monitor.py                        # 67 days stale — file-change tracking is blind
python baseline_clinical_trials.py           # 16 days stale
python project1_literature_gap_analysis.py   # 3 days — refresh within the week
```

**P1 — fix the zimislecel alias.** Add `VX-880` (and `VX-264`, `VX-017`) as synonyms wherever
`zimislecel` is tracked. Today the tracker reports 0/0 while Vertex runs two Phase 3 studies
and files for approval.

**P1 — audit three PubMed queries returning exactly 3 hits.** `Diabetes Drug Repurpose`,
`Diabetes Epigenetics`, `GLP-1 Pharmacogenomics`. Drug Repurposing is Tier 1; a malformed
query there manufactures a false gap.

**P1 — audit the `has_results` field.** 0 of 894 trials report results while
343 are categorized "Recently Completed with Results," and retatrutide Phase 3 results are in
*The Lancet* this month. The flag is not being populated.

**P2 — read these three cross-domain papers** (all Tier 1 aligned):
- PMID 42759644 — macrophage immunometabolism across cardio-hepatic-renal comorbidities (3 domains)
- PMID 42756821 — multi-omics gut-metabolite targets in DKD
- PMID 42627334 — beta-cell function 1 yr after stopping baricitinib, *Diabetes Care*

**P2 — add NCT07804849 to the tracker.** Oral verapamil in newly diagnosed pediatric T1D
(Phase 2/3, recruiting). A repurposed drug for beta-cell preservation is a direct Tier 1 #4
data point and an anchor for the Islet Transplant × Drug Repurposing gap.

**P2 — check NCT07495956** (cfMSC therapy): regressed RECRUITING → NOT_YET_RECRUITING. Status
regression usually means a hold or protocol amendment.

**P2 — verify Sana Biotechnology coverage.** Zero trials in a 894-trial diabetes corpus for a
named key organization is more likely a query gap than an absence.

**Carried forward from `ACTION_REQUIRED_2026-09-21.md`** — still open, not re-derived here:
git push (118 commits, 154 days behind `origin/main`), and the stale PMID-ceiling rule in the
scheduled task file (live ceiling 42763307, not 42000000).

---

## Sources

- [TRANSCEND-T2D-1, *The Lancet*](https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(26)00967-0/abstract)
- [ADA 2026 highlights — therapies in development](https://diabetesonthenet.com/diabetes-primary-care/ada-2026/)
- [Vertex — T1D portfolio program updates](https://investors.vrtx.com/news-releases/news-release-details/vertex-announces-program-updates-type-1-diabetes-portfolio)
- [Vertex — zimislecel data at ADA 85th Scientific Sessions](https://news.vrtx.com/news-releases/news-release-details/vertex-presents-positive-data-zimislecel-type-1-diabetes)
- [Phase 3 trial of Vertex's islet cell therapy under way](https://www.managedhealthcareexecutive.com/view/phase-3-trial-of-vertex-s-islet-cell-therapy-for-type-1-diabetes-in-under-way)
- [ADA Standards of Care in Diabetes — 2026](https://diabetes.org/newsroom/press-releases/american-diabetes-association-releases-standards-care-diabetes-2026)

*Read-only review. No existing files were modified. Local files read:
`clinical_trials_latest.json`, `clinical_trials_snapshot_{2026-07-17,08-27,08-28,09-01,09-06}.json`,
`pubmed_recent_latest.json`, `pubmed_recent_snapshot_{09-01,09-05,09-06,09-18,09-20}.json`,
`literature_gap_data.json`, `literature_gap_report.md`, `hub_monitor_report.md`,
`monitor_report_2026-09-21.md`, `ACTION_REQUIRED_2026-09-21.md`, `RESEARCH_DOCTRINE.md`.*
