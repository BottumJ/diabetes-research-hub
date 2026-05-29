# Diabetes Research Hub — Monitor Report
**Date:** 2026-05-29
**Run type:** Scheduled automated monitor
**Previous report:** monitor_report_2026-05-28.md

---

## File System Status

All four expected data products refreshed today (2026-05-29 07:04–07:05). Hub state is healthy.

| File | Last modified | Status |
|------|---------------|--------|
| `hub_monitor_report.md` | 2026-05-29 07:05 | Fresh |
| `clinical_trials_latest.json` | 2026-05-29 07:04 | Fresh |
| `pubmed_recent_latest.json` | 2026-05-29 07:05 | Fresh |
| `literature_gap_report.md` | 2026-05-28 08:10 | Fresh (1d) |
| `literature_gap_data.json` | 2026-04-20 15:35 | **STALE (39d)** |

**Inventory:** 876 files tracked (3 new, 28 modified, 0 removed vs. yesterday). 655 result files are older than 14 days per `hub_monitor.py`. The `literature_gap_data.json` is the most consequential stale file — gap report runs read it, but the underlying JSON has not been regenerated since April 20.

---

## Clinical Trial Changes

**Snapshot diff (2026-05-28 → 2026-05-29):**
- New trials: **1**
- Removed: 0
- Status changes: **2**
- New results posted: 0 (since yesterday's snapshot; see "Recent results" below for last-week activity)

### Status Changes Today
- **NCT06728059** — RECRUITING → COMPLETED. *Safety and Feasibility of a Machine-Learning Bolus Priming Added to Existing Control Algorithm.* Results were also posted 2026-05-28 — worth pulling the readout if not already captured.
- **NCT06888687** — RECRUITING → ACTIVE_NOT_RECRUITING. *Comparison of Dietetics Support With and Without Continuous Glucose Monitoring.*

### Key Phase 3 RECRUITING Trials (highest priority watchlist)
47 trials currently Phase 3 + RECRUITING. Headline items:

| NCT | Sponsor | Topic |
|-----|---------|-------|
| NCT06832410 | Vertex | **VX-880** efficacy/safety/tolerability, T1D |
| NCT04786262 | Vertex | **VX-880** safety/tolerability/efficacy, T1D |
| NCT07222332 | Eli Lilly | **Baricitinib** to preserve beta cell function (pediatric/adult new-onset T1D) |
| NCT07222137 | Eli Lilly | **Baricitinib** to delay stage 3 T1D |
| NCT07088068 | (per snapshot) | **Teplizumab** vs. placebo (Phase 3) |
| NCT06334133 | vTv Therapeutics | Cadisegliatin (glucokinase activator) adjunct to insulin, T1D |
| NCT06217302 | Alessandro Doria (JDC) | Sotagliflozin for renal decline in T1D |
| NCT06630585 | Univ. of Bern | GIP/GLP-1RA + AID in T1D |

### Recently Posted Results (this week — review candidates)
- NCT06728059 (2026-05-28) — ML bolus priming closed-loop
- NCT04426474 (2026-05-26) — **LY3502970 / orforglipron** in T2D
- NCT03919877 (2026-05-22) — Precision Diets for Diabetes Prevention
- NCT05514535 (2026-05-11) — Semaglutide + lower-dose insulin glargine

### Category & Sponsor Snapshot
801 unique trials. Eli Lilly leads sponsors (28), Novo Nordisk (26), Vertex (3 — small but highly leveraged). 121 Phase 3 trials total; 264 RECRUITING.

---

## PubMed Highlights (last 30 days, 161 unique papers)

### Cross-Domain Papers (highest priority — appear in ≥2 alert domains)
16 cross-domain papers this cycle. Top picks:

- **[PMID 42163482]** *Assessing Extracellular Vesicle Proteins as Predictive Biomarkers for Developing Type 1 Diabetes.* Proteomics (2026-May-20). Domains: T1D Stem Cell Cure + T1D Immunotherapy + Key Therapy: teplizumab. **High value** — biomarker work directly relevant to teplizumab patient selection.
- **[PMID 42198313]** *Diabetes Mellitus and Stroke: Pathophysiological Connections and Therapeutic Potential of GLP-1 and Triple-Agonist Therapies.* Domains: orforglipron + retatrutide + CagriSema. Cross-references three of our key therapies in one paper.
- **[PMID 42206849]** *Early-life proteomic and microbiome features signal obesity risk across 26 years of follow-up.* Domains: AI/ML + Microbiome. **New since yesterday** — directly relevant to our microbiome ML pipeline (Phase 2 already completed). Worth pulling for the Research_Findings_Summary.
- **[PMID 42138126]** *US Patterns in Clinical Islet Autoantibody Ordering and Results Show Key Differences After Teplizumab*. Domains: T1D Immunotherapy + Teplizumab. Real-world adoption signal.
- **[PMID 42148104]** *Adapting CAR-T and CAR-Treg cancer therapies for autoimmunity: innovations and challenges.* Bridges T1D Stem Cell Cure + T1D Immunotherapy — relevant to Treg/CAR-T gap row in the gap analysis.
- **[PMID 42199390]** *Lactylation-related diagnostic biomarkers for T2D by WGCNA.* AI/ML + Biomarker.
- **[PMID 42199945]** + **[PMID 42190810]** — Two Multi-Omics × Epigenetics papers in 2 days (uric acid metabolism, glycolipid metabolism).

### Key Therapy Hits This Cycle
| Therapy | Total mentions | Unique papers |
|---------|---------------|---------------|
| dapagliflozin | 45 | 5 |
| retatrutide | 7 | 5 |
| teplizumab | 6 | 5 |
| icodec | 6 | 5 |
| CagriSema | 5 | 5 |
| orforglipron | 4 | 4 |
| baricitinib | 4 | 4 |
| **zimislecel** | **0** | **0** ← still no publication signal |

### Publication Volume Trends
HIGH ACTIVITY: AI/ML (247), Biomarker (175), Microbiome (154), GLP-1 New (136), T2D Remission (80). LOW: Drug Repurposing (7), LADA (7), GLP-1 Pharmacogenomics (2). The Pharmacogenomics and LADA underactivity is consistent with our Tier 1 contribution thesis — these are genuinely undercrowded.

---

## Gap Analysis Summary

Top 5 under-researched intersections (Gap Score = 100, joint pubs = 0–1; BRONZE validation):

1. **Beta Cell Regen × Health Equity** — 0 joint pubs. Aligns with Tier 1 (equity).
2. **Insulin Resistance × Islet Transplant** — 1 joint pub.
3. **Islet Transplant × Drug Repurposing** — 0 joint pubs. Aligns with Tier 1 (drug repurposing pipeline).
4. **Islet Transplant × Health Equity** — 0 joint pubs.
5. **Gene Therapy × LADA** — 0 joint pubs. Aligns with Tier 1 (LADA).

Multiple Tier 1 doctrine areas (LADA, drug repurposing, health equity) appear repeatedly in the top 15. The gap dataset itself is 39 days old, however — refresh recommended before drawing newer conclusions.

---

## Breaking News (web check, last 7 days)

- **Retatrutide TRIUMPH-1 Phase 3 readout (Eli Lilly, May 21, 2026)** — First registrational Phase 3 obesity trial for retatrutide (GIP/GLP-1/glucagon triple agonist). At 80 weeks: 28.3% average weight loss at 12 mg, 25.9% at 9 mg, 19.0% at 4 mg. Extension to 104 weeks pushed BMI ≥35 cohort up to 30.3%. TRIUMPH-2 (obesity + T2D) and TRIUMPH-3 (CVD) data still pending later in 2026. **High significance** — directly relevant to our key-therapy watchlist; consider adding to tracker.
- **Innovent mazdutide Phase 3 obesity/diabetes data presented at ADA 2026 (May 13, 2026)** — Worth checking whether mazdutide should be promoted into the key-therapy watchlist.

Awiqli (insulin icodec) and Ozempic tablets noted as FDA actions earlier in 2026; not breaking-this-week.

---

## Recommended Actions

1. **Refresh literature gap data** — `python project1_literature_gap_analysis.py` (current `literature_gap_data.json` is 39 days old).
2. **Capture NCT06728059 results readout** (ML bolus priming) — posted yesterday, status flipped to COMPLETED.
3. **Capture NCT04426474 results readout** (LY3502970/orforglipron in T2D) — posted 2026-05-26.
4. **Add retatrutide TRIUMPH-1 readout** to Research_Findings_Summary.md and tracker. Evidence level: SILVER (single Phase 3 topline; full publication pending).
5. **Add Vertex NCT06832410** to "Notable Trials to Watch" section of `clinical_trials_summary.md` (Phase 3 VX-880 RECRUITING — table is currently empty).
6. **Pull full text for PMID 42206849** (early-life proteomic + microbiome obesity signal) into `paper_library/` — cross-domain with our microbiome ML pipeline.
7. **Pull full text for PMID 42163482** (EV proteins predictive biomarkers for T1D) — three-domain crossover including teplizumab.
8. **Consider adding mazdutide to key-therapy list** — Phase 3 data at ADA 2026; currently absent from tracker.
9. No script failures detected; all daily exports ran cleanly.

---

## Evidence Levels Used
- Trial status changes from ClinicalTrials.gov API: **GOLD** (primary source).
- PubMed bibliometrics: **SILVER** (third-party indexed; matching is keyword-approximate).
- Gap classifications: **BRONZE** (single analytical source, no expert validation yet).
- Retatrutide TRIUMPH-1 readout: **SILVER** (sponsor topline; peer-reviewed publication pending).

---
*Generated automatically by diabetes-hub-monitor scheduled task — 2026-05-29*
