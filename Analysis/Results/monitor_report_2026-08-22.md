# Diabetes Research Hub — Monitor Report
**Run date:** 2026-08-22 (automated, review-only — no files modified)
**Prior monitor report:** 2026-08-21
**Data vintage under review:** 2026-07-17

---

## Headline: the hub is busy, and that is the problem

This is the **13th consecutive day** this monitor has reported the same dead collection pipeline — and the streak is longer than that: every report since 2026-07-18 references the 07-17 freeze. Nothing was fixed. But the framing in the prior reports — "the pipeline has been dead for N days" — is incomplete, and the incomplete version is why it keeps getting ignored.

The hub is **not** dormant. On 2026-08-21 at 07:39–07:53, forty-plus files were rewritten: `research_paths.json`, `citation_validation.json`, `gap_evidence.json`, `literature_gap_report.md`, `agent_state.json`, and **every dashboard in `Dashboards/` and `docs/Dashboards/`**. Scripts were authored and run. Work happened.

What did *not* run: `baseline_clinical_trials.py`, `baseline_pubmed_alerts.py`, `project1_literature_gap_analysis.py`.

**So the failure is selective, not global.** The derived layer keeps regenerating; the acquisition layer stopped. The result is worse than an obviously dead hub:

```
                        last acquired      last rendered
Clinical_Trial_Dashboard.html   ──────────────────────┐
  reads clinical_trials_latest.json   2026-07-17      │
  file itself rewritten                          2026-08-21
                                                       ▲
  36-day gap, invisible to anyone opening the dashboard ┘

literature_gap_report.md
  header "Generated: 2026-08-21 07:53"
  body   "Date range: 2020/01/01 to 2026/07/17"
  source literature_gap_data.json  "generated": 2026-07-17T10:14:41
```

Every dashboard in this hub currently carries a 2026-08-21 file date and 2026-07-17 content. [Certain — `md5sum` confirms `clinical_trials_latest.json` is byte-identical to `clinical_trials_snapshot_2026-07-17.json`; same for the PubMed pair. Dashboard mtimes from `find -newermt`.]

**The question worth answering before the next run:** what invokes the three baseline scripts, and why did that invoker stop on 2026-07-17 while the rest of the automation kept firing? Fixing the symptom by hand today means this report says the same thing on 2026-09-22. Nothing in the workspace tells me the answer — this needs a look at the local scheduler / `refresh.ps1`.

**Immediate refresh:**
```
python baseline_clinical_trials.py
python baseline_pubmed_alerts.py
python project1_literature_gap_analysis.py
python hub_monitor.py
```

---

## Correction to the 2026-08-21 report

The prior report claimed: *"PubMed domain counts are ceiling-capped at 10 and are not a volume signal."*

**Half right, and the wrong half is the load-bearing one.** [Certain — read `baseline_pubmed_alerts.py` lines 66–96, 205–216.]

There are two different numbers per domain:

| Field | Capped? | Usable as volume signal? |
|---|---|---|
| `paper_count` | Yes — `retmax=10` (therapies: `retmax=5`) | No |
| `total_count` | **No** — it is PubMed esearch `<Count>`, the full hit count | **Yes** |

`total_count` is uncapped and ranges 1 → 260 across the 16 domains. Discarding domain volume as unusable would throw away the one PubMed metric that *is* clean. The real defect is presentational: the summary tables sort on `total_count` but the snapshot exposes both fields side by side with similar names, which is how the confusion arose. Recommend renaming `paper_count` → `sampled_count` in the snapshot schema.

**Confirmed from the prior report:** `has_results == True` for **0 of 858** trials while `results_posted` is populated for **322**. The boolean is dead. Any diff logic keyed on it silently returns zero. Fix: derive `has_results = bool(results_posted)` at parse time. [Certain]

---

## New defect: `zimislecel` is tracked under a name the literature does not use

`KEY_THERAPY_TERMS` in `baseline_pubmed_alerts.py` includes `"zimislecel"`. It returns **0 papers, 0 total_count** — and has for every snapshot in the archive.

Meanwhile `clinical_trials_latest.json` carries two Vertex Phase 3 trials for the same molecule, both indexed under **VX-880**, neither under `zimislecel`. The trial collector and the literature collector are watching the same therapy under two names and neither can see the other's hits.

| Collector | Term used | Hits |
|---|---|---|
| `baseline_pubmed_alerts.py` | `zimislecel` | 0 |
| ClinicalTrials.gov snapshot | `VX-880` | 2 (both PHASE3, both RECRUITING) |

This is the hub's single highest-priority T1D cure asset and the alerting is blind to it. Fix: search `"zimislecel OR VX-880"`. Same class of problem likely affects `icodec` (trials index it as *insulin icodec* / *Awiqli*). [Certain for zimislecel — verified by keyword scan of both JSON files. Likely for icodec — not separately confirmed.]

---

## Clinical trial signals sitting unread in the 07-17 snapshot

858 trials. Phase 3 RECRUITING = **46** on a strict `phase == "PHASE3"` match, or **52** if the six `"PHASE2, PHASE3"` records are included; the seven below are all strict PHASE3. These seven are the key-sponsor subset, and none of them appear in the `clinical_trials_summary.md` "Notable Trials to Watch" table — **which has been empty since the file was created.** The collector generates it as a stub awaiting manual curation and no one has ever curated it.

| NCT | Sponsor | Therapy | n | Est. completion |
|---|---|---|---|---|
| NCT07222332 | Eli Lilly | Baricitinib — preserve beta cell function, children/adolescents | 300 | 2028-07 |
| NCT07222137 | Eli Lilly | Baricitinib — delay Stage 3 T1D | 150 | 2031-07 |
| NCT06832410 | Vertex | VX-880 (zimislecel) | 10 | 2027-09 |
| NCT04786262 | Vertex | VX-880 (zimislecel) | 52 | 2030-06 |
| NCT07564414 | Novo Nordisk | CagriSema, two doses | 2,500 | 2028-04 |
| NCT07076199 | Novo Nordisk | Insulin icodec, weekly | 877 | 2027-03 |
| NCT06739122 | Eli Lilly | Dulaglutide 3.0/4.5 mg, pediatric | 55 | 2027-12 |

**Most actionable:** the baricitinib pair. Two Phase 3 T1D immunomodulation trials from Lilly, one prevention and one preservation, 450 participants combined. An oral JAK inhibitor with an existing safety database being taken into T1D prevention is a materially different risk/access profile from teplizumab or cell therapy — and it lands directly on Tier 1 area #3 (Clinical Trial Intelligence) and Tier 2 immunomodulation work. The hub already has `build_immunomod_lada.py`. [Likely — trial records are Certain; the strategic read is my inference, not sourced.]

Also present: **NCT07088068**, Sanofi, teplizumab Phase 3, RECRUITING — see Breaking News below.

**Most recent results postings in-snapshot** (all pre-07-17, listed because the `has_results` bug means the diff never surfaced them):

- 2026-07-09 — NCT03263494, Jaeb Center, PHASE3, CGM in teens/young adults with T1D
- 2026-07-08 — NCT04255433, Eli Lilly, PHASE3, tirzepatide vs dulaglutide on major CV events
- 2026-07-13 — NCT05254002, Bayer, PHASE2, finerenone combination

---

## PubMed highlights (30-day window ending 2026-07-17, 158 papers)

**Cross-domain papers — 12 of 158.** Highest value, per doctrine Tier 1 #2 (Literature Synthesis):

| PMID | Domains | Title |
|---|---|---|
| 42459945 | AI/ML + Closed Loop AP + Health Equity | Framework for assessing algorithmic discrimination risks in training data: pediatric T1D case |
| 42419792 | orforglipron + retatrutide + CagriSema | Comparative effects of drugs for adults with overweight or obesity: SR + network meta-analysis |
| 42411999 | T1D Stem Cell Cure + T1D Immunotherapy | T1D driven by residual recipient T cells after hematopoietic cell transplantation |
| 42453334 | Biomarker + LADA | Noncoding RNAs for diabetes research and therapy |
| 42436543 | T2D Remission + Health Equity | Healthcare inequalities in T2D across the COVID-19 pandemic |

**PMID 42459945 is the one to read.** A three-domain paper hitting AI/ML, closed-loop, and health equity simultaneously — that triple is exactly the intersection the gap analysis keeps flagging as empty, which means the gap may already be closing while our data is frozen. It also directly informs Tier 1 #5 (AI/ML Prediction Models) and Tier 1 #6 (Epidemiological/Equity Analysis).

**Domain volume** (`total_count`, uncapped):

```
Diabetes AI/ML        ████████████████████████ 260
Diabetes Microbiome   █████████████████ 186
T2D GLP-1 New         ███████████████ 167
Diabetes Biomarker    ███████████████ 166
Diabetes Health Equity ██████ 72
Diabetes Multi-Omics  ██████ 65
T2D Remission         █████ 59
Diabetes Gene Therapy ████ 42
Closed Loop AP        ███ 38
Complications New     ███ 34
T1D Immunotherapy     ██ 25
T1D Stem Cell Cure    █ 17
LADA New Research     █ 12
Drug Repurpose        ▌ 8
Diabetes Epigenetics  ▌ 5
GLP-1 Pharmacogenomics  1
```

Two structural notes, both stable across the archive rather than one-month noise: **Diabetes AI/ML at 260 is 3.6× Health Equity at 72** — the field is building models faster than it is checking who they work for, which is the empirical backing for the equity gaps ranked below. And **LADA at 12 / Epigenetics at 5 / Drug Repurposing at 8** are thin enough that a single competent synthesis paper measurably moves the literature — consistent with the hub's existing LADA focus. [Likely — one 30-day window; would want 3+ windows to call it Certain, and the archive has them if someone wants to run the trend.]

---

## Gap analysis (data vintage 2026-07-17, 30 domains, 435 pairs)

Top 5 by gap score, excluding pairs the report itself classifies as methodologically distinct:

| # | Intersection | Gap | Joint pubs | Expected | Tier 1 alignment |
|---|---|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 | 7.5 | — |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 | 7.3 | **#6 Epidemiological/Equity** |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 | 4.7 | **#6** |
| 4 | Glucokinase × Health Equity | 100.0 | 0 | 4.3 | **#6** — hub already has GKA assets |
| 5 | Gene Therapy × LADA | 100.0 | 0 | 3.3 | **#2 Literature Synthesis** |
| 6 | Drug Repurposing × Health Equity | 100.0 | 0 | 3.0 | **#4 Drug Repurposing** + **#6** |

**Four of the top six are `X × Health Equity`.** That is not six independent findings — it is one finding with four faces: *no advanced-therapy modality in diabetes has an access analysis attached to it.* The hub is unusually well positioned here. `build_gka_pricing.py`, `build_gka_landscape.py`, `build_health_equity.py`, `build_equity_map.py`, and `build_islet_equity.py` already exist. Rank 4 (Glucokinase × Health Equity) is the shortest path from current assets to a defensible contribution.

Caveat carried from the source report and worth restating: gap score is a *relative* co-publication measure. A score of 100 with 0 joint publications and an expected value of 3.0 is a weak signal in absolute terms — three expected papers is within noise. Ranks 1–6 are all BRONZE. [Certain that the scores are as stated; the interpretation is BRONZE per doctrine and needs expert confirmation before it becomes a work commitment.]

---

## Breaking news check (7-day window, 2026-08-15 → 2026-08-22)

**Nothing in the last 7 days clears the bar** for Phase 3 results, FDA action, or major publication in core diabetes. The one item in-window — Amylyx's 2026-08-18 LUCIDITY topline for avexitide — is post-bariatric hypoglycemia, adjacent rather than core, and does not warrant tracker action.

Two items **outside** the 7-day window matter because our snapshot predates or straddles them and the tracker has not absorbed them:

1. **Tzield (teplizumab) — new FDA indication, 2026-06-12.** Accelerated approval to delay decline of insulin production in pediatric patients 8–17 recently diagnosed with Stage 3 T1D. Our snapshot holds seven teplizumab trials including NCT07088068 (Sanofi, Phase 3, RECRUITING) and NCT05757713 (Sanofi, Phase 4, ACTIVE_NOT_RECRUITING). The regulatory status change is not reflected anywhere in the hub. [Certain — FDA press announcement.]

2. **Zimislecel regulatory submissions expected during 2026.** Vertex holds RMAT, Fast Track, EMA PRIME, and MHRA Innovation Passport. Phase 1/2 read: 10 of 12 full-dose patients insulin-free at one year, all 12 at HbA1c <7% and >70% time-in-range. Combined with the naming defect above, the hub would not detect a zimislecel BLA filing or approval through its own alerting. **This is the single highest-consequence blind spot in the monitor.** [Certain on designations and Phase 1/2 figures; timing of any submission is not confirmed.]

---

## Recommended actions

**Ordered by consequence, not by effort.**

1. **Diagnose the invoker, not the data.** Find what was supposed to call the three baseline scripts and why it stopped on 2026-07-17 while the rest of the automation kept running. Check `refresh.ps1` and the local scheduler. Re-running by hand today fixes one day.

2. **Patch `baseline_pubmed_alerts.py` before the next collection run** — change `"zimislecel"` to `"zimislecel OR VX-880"`, and check `icodec` against *insulin icodec* / *Awiqli*. Running the collector before this patch bakes another blind snapshot into the archive.

3. **Patch `has_results = bool(results_posted)`** in the trial collector. Until then the "New results posted" diff line is meaningless, not zero.

4. **Then refresh:** `baseline_clinical_trials.py` → `baseline_pubmed_alerts.py` → `project1_literature_gap_analysis.py` → `hub_monitor.py`.

5. **Stop rendering dashboards from stale sources.** Add a freshness assertion to the dashboard builders — if the source JSON is >7 days old, stamp the age on the rendered page. A dashboard that silently shows 36-day-old data is worse than one that fails to build.

6. **Fill in "Notable Trials to Watch"** in `clinical_trials_summary.md` with the seven Phase 3 trials tabled above. It has never had an entry.

7. **Update the tracker** with the Tzield pediatric Stage 3 indication (2026-06-12) against NCT07088068 and NCT05757713.

8. **Read PMID 42459945** (algorithmic discrimination in pediatric T1D training data) — three-domain paper, directly on Tier 1 #5 and #6.

9. **Scope Glucokinase × Health Equity** as the next contribution candidate. Shortest distance from existing GKA + equity assets to a BRONZE→SILVER promotion. Confirm the gap is real against domain expertise before committing, per doctrine.

---

*No files were modified by this run. All figures verified by direct read of the source JSON; evidence levels labeled per RESEARCH_DOCTRINE.md.*
