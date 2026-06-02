# Diabetes Research Hub — Monitor Report

**Run date:** 2026-06-02
**Run type:** Automated scheduled scan (`diabetes-hub-monitor`)
**Comparison window:** 7 days (2026-05-24 → 2026-05-31 latest snapshots)
**Evidence level:** BRONZE for derived gap/cross-domain claims; PRIMARY for ClinicalTrials.gov & PubMed counts

---

## File System Status

Latest pipeline outputs in `Analysis/Results/`:

| File | Last modified | Age (days) | Status |
|---|---|---|---|
| `hub_monitor_report.md` | 2026-05-31 07:05 | 2 | OK |
| `clinical_trials_latest.json` | 2026-05-31 07:05 | 2 | OK |
| `pubmed_recent_latest.json` | 2026-05-31 07:05 | 2 | OK |
| `literature_gap_report.md` | 2026-05-31 14:09 | 2 | OK |
| `literature_gap_data.json` | 2026-04-20 15:35 | 43 | **STALE — data file >14d** |
| `pubmed_recent_summary.md` | 2026-05-31 07:05 | 2 | OK |
| `hub_monitor_state.json` | 2026-05-31 07:05 | 2 | OK |

**Daily snapshots are current** through 2026-05-31 for both clinical trials and PubMed. No snapshot exists for 2026-06-01 or 2026-06-02 — the daily scheduled run that normally produces these has not fired yet for this period.

**Review flag from hub_monitor:** 658 result files are >14 days old (expected — these are historical daily snapshots kept for diff history).

---

## Clinical Trial Changes (7-day window, May 24 → May 31)

- **Old total:** 797 trials → **New total:** 804 trials (+7)
- **New trials:** 7
- **Removed:** 0
- **Status changes:** 9
- **New results posted:** 1

### New trials worth attention

| NCT | Title | Phase | Status | Sponsor |
|---|---|---|---|---|
| NCT07613307 | Orforglipron (LY3502970) in T2D Insulin-Naive | PHASE3 | NOT_YET_RECRUITING | **Eli Lilly** |
| NCT07614412 | SHIELD-T1D: Shingrix + GLP-1 Agonist for Beta-Cell Preservation in Recent-Onset T1D | PHASE2 | NOT_YET_RECRUITING | Ministry of Health, Saudi Arabia |
| NCT07610213 | Sequential Immune Modulation & Antigen-Specific Tolerance Induction | PHASE1 | NOT_YET_RECRUITING | Abdullah Kars |
| NCT07611721 | Dexcom G7 CGM Performance Study | n/a | RECRUITING | ICEM Prague |
| NCT07613489 | Photobiomodulation for Diabetic Peripheral Neuropathy | n/a | ACTIVE_NOT_RECRUITING | Univ. of Faisalabad |
| NCT04426474 | LY3502970 (orforglipron) in T2D — completed Phase 1 | PHASE1 | COMPLETED (results posted 2026-05-26) | Eli Lilly |
| NCT03242343 | VasQ External Support for AV Fistula | n/a | COMPLETED (results posted 2026-05-27) | Laminate Medical |

### Notable status changes

- **NCT07564414** (CagriSema Phase 3, Novo Nordisk-adjacent): NOT_YET_RECRUITING → **RECRUITING**
- **NCT07284511** (Tirzepatide automation in T1D, McGill): NOT_YET_RECRUITING → **RECRUITING**
- **NCT06728059** (ML bolus priming, closed-loop): RECRUITING → **COMPLETED with results posted 2026-05-28**

### Key Phase 3 recruiting overview (n=48 in dataset)

Tier 1 cohort still active:

- **VX-880 (Vertex)** — NCT04786262 (Phase 3 RECRUITING) and NCT06832410 (efficacy/safety, RECRUITING). Both progressing.
- **Baricitinib (Eli Lilly)** — NCT07222137 (Stage 3 delay) and NCT07222332 (beta-cell preservation), both RECRUITING.
- **Cadisegliatin (vTv Therapeutics)** — NCT06334133, Phase 3 RECRUITING (glucokinase activator — note alignment with gap #8 below).
- **CagriSema (Novo Nordisk)** — NCT07564414 newly opened to recruiting in this window.

### Key organization activity

| Sponsor | Total tracked | Recruiting |
|---|---|---|
| Eli Lilly | 29 | 6 |
| Novo Nordisk | 26 | 3 |
| Vertex | 3 | 2 |
| Sana Biotechnology | 0 | 0 |

Sana Biotechnology remains absent from the ClinicalTrials.gov dataset under direct sponsorship — confirm whether their hypoimmune islet programs are filed under an academic collaborator.

### Key therapy presence in trials

| Therapy | Trials in dataset |
|---|---|
| teplizumab | 7 |
| CagriSema | 5 |
| orforglipron | 4 (incl. 1 new this window) |
| retatrutide | 3 |
| baricitinib | 2 |
| zimislecel | **0** — not appearing under this string; check INDA / Vertex naming |

---

## PubMed Highlights (165 papers, 30-day rolling window ending 2026-05-31)

- **Total unique papers:** 165 across 16 alert domains
- **7-day churn (vs May 24 snapshot):** +107 new / −98 dropped — heavy refresh, consistent with rolling-window behavior

### Cross-domain papers (highest priority — 13 found)

| PMID | Domains | Title | Journal |
|---|---|---|---|
| 42163482 | T1D Stem Cell Cure + T1D Immunotherapy + teplizumab | Extracellular vesicle proteins as predictive biomarkers for T1D | Proteomics, May 20 |
| 42198313 | orforglipron + retatrutide + CagriSema | Diabetes & stroke: GLP-1 / GLP-1/GIP RAs therapeutic potential | Pharmaceutics, May 19 |
| 42138080 | T1D Immunotherapy + teplizumab | New and emerging therapies in T1DM | J Clin Investigation, May 15 |
| 42138126 | T1D Immunotherapy + teplizumab | Islet autoantibody ordering patterns after teplizumab approval | JCEM, May 15 |
| 42208956 | T2D GLP-1 New + retatrutide | Beyond weight loss: multisystem benefits of obesity meds | Lancet Diab Endo, May 28 |
| 42208537 | AI/ML + Gene Therapy | Capturing multi-disease states with ML on routine clinical data | Med, May 28 |
| 42206849 | AI/ML + Microbiome | Early-life proteomic & microbiome features signal obesity over 26y | mSystems, May 28 |
| 42209585 | Biomarker + Complications | Thrombin in diabetic retinopathy + PARIN5 inhibition | Sci Reports, May 28 |
| 42208844 | Biomarker + Complications | Proteomic meta-analysis of proliferative diabetic retinopathy | Exp Eye Research, May 27 |
| 42211453 | Microbiome + Multi-Omics | Gut microbiota–diabetic peripheral neuropathy bibliometric | Front Endo, 2026 |
| 42199945 | Epigenetics + Multi-Omics | Multi-omics MR on glycolipid genes in GDM | IJWH, 2026 |
| 42199793 | T2D Remission + dapagliflozin | Dapagliflozin + linagliptin reverses hepatic steatosis in T2D | Front Endo, 2026 |
| 42142983 | retatrutide + CagriSema | Bariatric surgery weight loss/health outcomes audit | Obesity Res Clin Pract, May 17 |

### Key therapy paper hits this window

| Therapy | Paper count |
|---|---|
| dapagliflozin | 5 (43 total mentions) |
| retatrutide | 5 (9 mentions) |
| CagriSema | 5 |
| teplizumab | 5 |
| icodec | 5 |
| orforglipron | 4 |
| baricitinib | 4 |
| zimislecel | **0** |

### Domain volume (all domains active)

All 15 substantive alert domains returned 8–10 papers each in the 30-day window. **GLP-1 Pharmacogenomics** is consistently the lowest-volume domain (2 papers) — confirm whether the query is well-tuned or whether this is a real signal that pharmacogenomics work on GLP-1s is sparse.

### Most recent papers (top 5)

- 2026-May-30 — PMID 42216665 — *GFAP & NfL with retinal cell layer thickness*
- 2026-May-30 — PMID 42215751 — *Behavioral interventions for equity in pediatric T1D*
- 2026-May-30 — PMID 42215843 — *MASLD pathogenesis & novel treatment options*
- 2026-May-29 — PMID 42216430 — *Logistic regression for non-proliferative DR risk*
- 2026-May-29 — PMID 42216361 — *BAR index for sepsis in acute pancreatitis*

---

## Gap Analysis Summary

Latest interpreted report dated 2026-05-31; underlying `literature_gap_data.json` is 43 days old (run before this window). **Recommend re-running `project1_literature_gap_analysis.py` to refresh the data layer.**

### Top 5 under-researched intersections (Gap Score = 100, BRONZE)

1. **Beta Cell Regen × Health Equity** (0 joint pubs) — equity analysis of emerging cell therapies absent
2. **Insulin Resistance × Islet Transplant** (1 joint pub) — IR impact on graft survival barely studied
3. **Islet Transplant × Drug Repurposing** (0) — computational drug screening for islet protection unexplored
4. **Islet Transplant × Health Equity** (0) — center access disparity unstudied
5. **Gene Therapy × LADA** (0) — autoimmune mechanism + gene therapy crossover absent

### Alignment with Tier 1 contribution areas

Gap #3 (Islet Transplant × Drug Repurposing) and Gap #8 (Glucokinase × Drug Repurposing) align directly with the active Islet Drug Repurposing research path under `research_plan_islet_drug_repurposing.md`. Gap #1 and Gap #4 (Health Equity intersections) align with the Trial Equity Mapper dashboard.

---

## Breaking News (web check, last 7 days)

**Confirmed significant items:**

- **Retatrutide TRIUMPH-1 Phase 3 readout (2026-05-21, Eli Lilly):** Triple GIP/GLP-1/glucagon agonist; 12 mg arm produced 28.3% body weight loss over 80 weeks in obesity/overweight without diabetes; 45.3% achieved ≥30% weight loss. Diabetes-arm TRIUMPH trials still ahead. This will likely flow into the PubMed alert stream in coming weeks.
- **MannKind Afrezza pediatric approval (2026-05-29):** FDA expanded inhaled mealtime insulin to ages 6+. INHALE-1 trial as pivotal evidence. Affects pediatric T1D treatment landscape.
- **Novo Nordisk amycretin Phase 3 program announced (early May 2026):** Phase 2 data supported decision to advance into Phase 3 across multiple indications including diabetes — first eval in a diabetic population reported positive weight loss and glucose control vs placebo. Worth adding to tracker.

(Sanofi Tzield pediatric approval surfaced in search results but is dated 2026-04-22, outside the 7-day window — not flagged as new.)

---

## Recommended Actions

1. **Refresh gap analysis** — `literature_gap_data.json` is 43 days old. Run: `python project1_literature_gap_analysis.py`
2. **Update tracker with new Eli Lilly Phase 3 trial** — NCT07613307 (Orforglipron in insulin-naive T2D); add to Tier 1 GLP-1 program tracking.
3. **Add new SHIELD-T1D trial to tracker** — NCT07614412; pairs Shingrix with GLP-1 for beta-cell preservation in recent-onset T1D — relevant to Beta Cell Regen × Immunotherapy intersection.
4. **Add retatrutide TRIUMPH-1 result to tracker** — Phase 3 readout from 2026-05-21 not yet in the dataset; supporting publications will follow.
5. **Add Novo Nordisk amycretin Phase 3 program to tracker** — new pipeline entry under T2D Novel Therapies.
6. **Review cross-domain paper PMID 42163482** (EV proteins + teplizumab biomarkers) — relevant to Autoimmunity T1D × Multi-Omics and to teplizumab response prediction.
7. **Review cross-domain paper PMID 42138080** (J Clin Investigation review on emerging T1D therapies) — likely cite-worthy reference for the Research Findings Summary.
8. **Confirm Sana Biotechnology trial tracking** — Sana sponsors 0 trials in the current dataset; verify whether their hypoimmune islet programs are filed under an academic partner sponsor.
9. **Investigate "zimislecel" naming** — 0 hits in trials, 0 in PubMed alerts; confirm whether the alert string is correct (Vertex's program may file under VX-880/VX-264/zimislecel selectively).
10. **Trigger 2026-06-01 / 2026-06-02 snapshots** — daily snapshot files for June not yet present; run `python baseline_clinical_trials.py` and `python baseline_pubmed_alerts.py` to bring snapshots current before next monitor pass.

---

## Doctrine notes

- All cross-domain paper highlights and gap intersections are reported at **BRONZE** evidence level (single source / single analytical pass).
- Trial-status changes and counts are **PRIMARY** (sourced directly from ClinicalTrials.gov via the daily snapshot).
- Breaking news items derived from press releases and trade press are **REPORTED** only; do not promote to FINDINGS until peer-reviewed publication or FDA documentation appears.

---

*Generated by automated `diabetes-hub-monitor` task — review-only run; no source files modified.*
