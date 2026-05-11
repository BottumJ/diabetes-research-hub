# Diabetes Research Hub — Monitor Report

**Generated:** 2026-05-01 (automated scheduled run)
**Comparison window:** 2026-04-24 → 2026-05-01 (7 days)
**Hub root:** `Diabetes_Research/`

---

## Executive Summary

The hub is healthy and freshly populated: clinical trial and PubMed snapshots ran this morning at 07:04–07:05 UTC. Eight trials entered the tracked set this week (mostly newly-completed with results), five trials changed status, and 104 net-new PubMed papers landed across 16 alert domains. The biggest signal is on the T2D oral GLP-1 / triple-agonist front: orforglipron, retatrutide, and CagriSema all have new Phase 3 activity, and external news confirms a positive ACHIEVE-1 readout for orforglipron and an expanded FDA approval for Sanofi's Tzield (teplizumab) to delay stage 3 T1D in young children. Literature-gap data is now 11 days old and should be re-run before the 14-day stale threshold.

---

## File System Status

| File | Last modified | Age | Status |
|---|---|---|---|
| `clinical_trials_latest.json` | 2026-05-01 07:04 | <1 day | OK |
| `clinical_trials_summary.md` | 2026-05-01 07:04 | <1 day | OK |
| `pubmed_recent_latest.json` | 2026-05-01 07:05 | <1 day | OK |
| `pubmed_recent_summary.md` | 2026-05-01 07:05 | <1 day | OK |
| `hub_monitor_report.md` | 2026-05-01 07:05 | <1 day | OK |
| `hub_monitor_state.json` | 2026-05-01 07:05 | <1 day | OK |
| `literature_gap_report.md` | 2026-04-30 08:09 | 1 day | OK |
| `literature_gap_data.json` | 2026-04-20 15:35 | 11 days | Aging — rerun before 14-day threshold |

Hub-monitor scan tracked 775 files (4 new, 49 modified, 0 removed since 2026-04-30). The script flagged 509 result files as older than 14 days — most are dated daily snapshots and don't need rotation, but the underlying gap-analysis pipeline does.

---

## Clinical Trial Changes (7-day diff)

| Metric | Value |
|---|---|
| Total tracked trials | 776 (was 771) |
| New in snapshot | 8 |
| Removed | 3 |
| Status changes | 5 |
| Net change | +5 |

### New trials in tracked set

Most entries are trials that newly meet the "Recently Completed with Results" criteria, not new registrations.

- **NCT05823948** — Novo Nordisk, Phase 3, COMPLETED — Insulin icodec with flash-glucose monitoring (results posted 2026-04-30)
- **NCT05649137** — Novo Nordisk, Phase 3, COMPLETED — Semaglutide for excess weight + T2D (results posted 2026-04-27)
- **NCT07552389** — Hanlim Pharm, Phase 3, RECRUITING — HL1113R1 monotherapy
- **NCT04831697** — Medical College of Wisconsin, NA, COMPLETED — Diabetes outcomes in older African-American women with caregiving burden (results posted 2026-04-28)
- **NCT05734989** — Duke, COMPLETED — Hispanic/Latinx CKD screening + therapy (results posted 2026-04-24)
- **NCT07554443** — RxFunction, NA, NOT_YET_RECRUITING — Wearable sensory prosthesis for neuropathy
- **NCT07558291** — Hospital Clinic of Barcelona, NA, NOT_YET_RECRUITING — CGM vs SMBG in gestational diabetes
- **NCT03887936** — VA Office of Research, Phase 4, COMPLETED — Testosterone + bone quality in diabetic men with hypogonadism

### Status changes

| NCT | From → To | Sponsor / Notes |
|---|---|---|
| NCT06993792 | RECRUITING → ACTIVE_NOT_RECRUITING | Eli Lilly — Orforglipron master protocol (consistent with positive Phase 3 readout) |
| NCT07355270 | NOT_YET_RECRUITING → RECRUITING | Aqua Medical — RF vapor ablation pilot |
| NCT07321678 | RECRUITING → ACTIVE_NOT_RECRUITING | Ascletis Pharma — ASC30 tablets (Phase 2 enrollment closed) |
| NCT07400588 | RECRUITING → ACTIVE_NOT_RECRUITING | Gasherbrum Bio — Aleniglipron Phase 2 in T2D |
| NCT07422831 | NOT_YET_RECRUITING → ENROLLING_BY_INVITATION | Univ. of Colorado Denver — T2D nonprescription CGM |

### Phase 3 RECRUITING — high-priority watchlist

The latest snapshot has **43 Phase 3 RECRUITING** diabetes trials. Notable entries from key sponsors:

- **NCT06832410** — Vertex — VX-880 (zimislecel) in T1D + kidney transplant
- **NCT04786262** — Vertex — VX-880 (zimislecel) in T1D, primary Phase 3 cohort
- **NCT07222137** — Eli Lilly — Baricitinib (LY3009104) to delay stage 3 T1D
- **NCT07222332** — Eli Lilly — Baricitinib to preserve beta-cell function in newly-diagnosed T1D
- **NCT07088068** — Sanofi — Teplizumab efficacy/safety in stage 2 T1D, ages 1–25
- **NCT06334133** — vTv Therapeutics — Cadisegliatin (glucokinase activator) adjunctive to insulin in T1D
- **NCT07076199** — Novo Nordisk — Insulin icodec weekly vs daily in T1D
- **NCT06217302** — Sotagliflozin to slow kidney function decline in T1D + DKD
- **NCT06739122** — Eli Lilly — Dulaglutide in pediatric T2D

### Recently posted results worth a look

15 trials posted results in the last 4 weeks. Highlights:

- **NCT05971940** — Eli Lilly orforglipron in T2D (results posted 2026-04-22) — pairs with the topline ACHIEVE-1 announcement
- **NCT05823948** — Novo Nordisk insulin icodec flash-glucose study (2026-04-30)
- **NCT05649137** — Novo Nordisk semaglutide for weight loss in T2D (2026-04-27)
- **NCT05238142** — Medtronic MiniMed 780G in adults with T2D (2026-04-16)
- **NCT05923827** — Insulet Omnipod 5 + Libre 2 vs MDI in T1D (2026-04-14)
- **NCT05144984** — Novo Nordisk semaglutide + NNC0480-0389 combination (2026-04-09)

---

## PubMed Highlights

| Metric | Value |
|---|---|
| Unique papers in latest snapshot | 150 |
| New since 2026-04-24 | 104 |
| Dropped from 30-day window | 94 |
| Cross-domain papers | 12 |

### Cross-domain papers (highest priority)

| PMID | Domains | Title (truncated) |
|---|---|---|
| 42050914 | T1D Stem Cell, T1D Immunotherapy, Gene Therapy, Teplizumab | Emerging therapies for type 1 diabetes: Immunotherapy and gene editing advances |
| 41297910 | Orforglipron, Retatrutide, CagriSema | Engineered nutrient-stimulated hormonal multi-agonists for obesity / metabolic disorders |
| 42051156 | T1D Immunotherapy, Teplizumab | BSPED/ABCD Consensus on clinical use of teplizumab in stage 2 T1D |
| 42023429 | T1D Immunotherapy, Gene Therapy | CRISPR-based β-cell replacement and Treg immune-modulation in T1D |
| 42056522 | T2D GLP-1, GLP-1 Pharmacogenomics | GLP-1R-GIPR-PPARα/γ/δ quintuple agonism corrects obesity/diabetes in mice (Nature) |
| 42061392 | AI/ML, Biomarker | From prediction to navigation for AI in medicine (Lancet) |
| 42062589 | Microbiome, Health Equity | Gestational diabetes → T2D risk and the gut microbiome in HCHS/SOL Hispanic cohort (Diabetologia) |
| 42061668 | Microbiome, Multi-Omics | Low-carb diet in autoimmune diseases — mechanisms and clinical translation |
| 42032109 | Gene Therapy, Epigenetics | Cell-specific DNA methylation in α/β cells regulates gene expression in T2D (Nature Metabolism) |
| 42059147 | Biomarker, Multi-Omics | Sepsis-related cardiac dysfunction mechanisms |
| 42053144 | Biomarker, Microbiome | First-in-human pyroligneous extract for wound healing |
| 42046753 | T1D Immunotherapy, Closed-Loop AP | Sitting breaks + glucose management in T1D using hybrid closed-loop |

### Papers mentioning key tracked therapies

- **Orforglipron** (3 papers) — incl. Pharmacokinetic Bioequivalence (Diabetes Obes Metab) and a GRADE meta-analysis (Acta Diabetologica)
- **Teplizumab** (2 papers) — BSPED/ABCD Consensus Statement (Diabetic Medicine, 2026-Apr-29) plus a clinical-practice case series
- **Tirzepatide** (3 papers) — incl. systematic review of multisystem benefits (Endocrine Practice)
- **Semaglutide** (4 papers) — incl. carbon-emission impact study (Value in Health)
- **Retatrutide** (1 paper) — overview in Expert Review of Clinical Pharmacology
- **Insulin icodec** (1 paper) — cost-utility vs daily basal in China
- **Zimislecel / VX-880** — 0 papers in latest 30-day PubMed window (despite Phase 3 activity); Vertex data is being communicated through investor releases and ADA presentations rather than journals this cycle

### Domain volume trends (week-over-week, total PubMed counts)

| Domain | Week ago | Today | Δ |
|---|---:|---:|---:|
| Diabetes AI/ML | 175 | 211 | **+36** |
| Diabetes Biomarker | 142 | 173 | **+31** |
| T2D GLP-1 New | 162 | 192 | **+30** |
| Diabetes Microbiome | 145 | 168 | **+23** |
| T2D Remission | 56 | 71 | +15 |
| Diabetes Health Equity | 63 | 74 | +11 |
| Diabetes Multi-Omics | 52 | 62 | +10 |
| Diabetes Complications | 33 | 43 | +10 |
| Diabetes Epigenetics | 8 | 12 | +4 |
| T1D Stem Cell Cure | 14 | 17 | +3 |
| Closed Loop AP | 23 | 25 | +2 |
| LADA New Research | 5 | 4 | −1 |
| T1D Immunotherapy | 22 | 21 | −1 |
| Drug Repurposing | 4 | 4 | 0 |
| Gene Therapy | 45 | 45 | 0 |
| GLP-1 Pharmacogenomics | 1 | 1 | 0 |

LADA, Drug Repurposing, and GLP-1 Pharmacogenomics remain at extremely low publication activity — consistent with the gap analysis identifying these as Tier 1 contribution opportunities.

---

## Gap Analysis Summary

Top 5 under-researched intersections (Gap Score = 100, BRONZE validation):

1. **Beta Cell Regen × Health Equity** (0 joint pubs) — equity analysis of emerging cell therapies absent
2. **Insulin Resistance × Islet Transplant** (1 joint pub) — IR in transplant recipients affects graft survival
3. **Islet Transplant × Drug Repurposing** (0 joint pubs) — computational repurposing for islet protection unexplored
4. **Islet Transplant × Health Equity** (0 joint pubs) — access equity research absent
5. **Gene Therapy × LADA** (0 joint pubs) — LADA's autoimmune mechanism is a candidate for gene-therapy approaches

### Alignment with Tier 1 contribution areas

Several top gaps map directly to the Research Doctrine's Tier 1 priorities:

- *Drug Repurposing × Health Equity* (rank 12) and *Drug Repurposing × LADA* (rank 13) intersect with **Tier 1: Drug Repurposing Computational Screening** — fits our "thousands of approved drugs with untested diabetes mechanisms" thesis.
- The Hispanic-cohort microbiome paper (PMID 42062589) directly bridges **Tier 1: Multi-Omics Biomarker Integration** with Health Equity — a candidate for cross-domain synthesis.
- *Glucokinase × Drug Repurposing* (rank 8) is timely given the cadisegliatin Phase 3 (NCT06334133) — repurposing screens against the same target are unexplored.

---

## Breaking News (web check, last 7 days)

- **Sanofi Tzield (teplizumab)** — FDA approved on 2026-04-22 to delay onset of stage 3 T1D in patients as young as 1 year, supported by 1-year PETITE-T1D Phase 4 data. **Significant.** ([Sanofi press release](https://www.sanofi.com/en/media-room/press-releases/2026/2026-04-22-05-05-00-3278650))
- **Eli Lilly orforglipron** — positive topline Phase 3 ACHIEVE-1 readout in T2D; weight-management submission expected by year-end, T2D submission in 2026. Consistent with the NCT06993792 status flip to ACTIVE_NOT_RECRUITING. ([Lilly investor release](https://investor.lilly.com/news-releases/news-release-details/lillys-oral-glp-1-orforglipron-demonstrated-statistically))
- **Vertex zimislecel** — FORWARD-101 Phase 1/2 1-year data in NEJM (12/12 patients restored endogenous insulin secretion, hit A1C <7% / TIR >70%); Phase 3 underway, regulatory submissions targeted in 2026. ([Vertex newsroom](https://news.vrtx.com/news-releases/news-release-details/vertex-presents-positive-data-zimislecel-type-1-diabetes), [NEJM](https://www.nejm.org/doi/abs/10.1056/NEJMoa2506549))
- **Stanford GLP-1 resistance study** — published April 10 in Genome Medicine, finding ~1 in 10 people may be resistant to GLP-1 drugs. Worth checking whether it was captured in our T2D GLP-1 / Pharmacogenomics domain alerts. ([Stanford Med news](https://med.stanford.edu/news/all-news/2026/04/glp-1-diabetes.html))

Routine product / device coverage skipped.

---

## Recommended Actions

1. **Re-run literature gap analysis.** `literature_gap_data.json` is 11 days old; refresh before the 14-day threshold to keep gap-tier scoring current. Command: `python project1_literature_gap_analysis.py`.
2. **Review the Lilly orforglipron Phase 3 result set.** Pull NCT05971940 results (posted 2026-04-22) and compare to the topline ACHIEVE-1 communication. Update tracker entry for orforglipron with evidence-level annotation per Doctrine.
3. **Add Tzield FDA-approval expansion to the tracker.** New indication (ages 1+) is a regulatory inflection — add to the T1D Immunotherapy section with a SILVER+ evidence label (peer-reviewed PETITE-T1D + FDA action).
4. **Synthesize the Diabetologia HCHS/SOL paper** (PMID 42062589) into the Microbiome × Health Equity intersection — it's a rare cross-domain hit on what the gap analysis ranks as a high-value area.
5. **Pull the Nature quintuple-agonist paper** (PMID 42056522) and the Nature Metabolism α/β methylation paper (PMID 42032109) into the paper library — both are high-impact and span our Tier 1 domains.
6. **Investigate cross-domain paper on CRISPR β-cell replacement + Treg modulation** (PMID 42023429) — relevant to the Treg × Health Equity and Gene Therapy × LADA gaps.
7. **Stage zimislecel-specific PubMed alert** — current PubMed query returns 0 hits for "zimislecel" / "VX-880" despite active Phase 3 program; consider broadening the search to capture the NEJM paper and conference abstracts.
8. **No file deletions, modifications, or transmission actions taken** — this run is review-only per task spec.

---
*Generated by automated diabetes-hub-monitor scheduled task.*

Sources:
- [Sanofi: Tzield approved to delay stage 3 T1D in young children](https://www.sanofi.com/en/media-room/press-releases/2026/2026-04-22-05-05-00-3278650)
- [Eli Lilly: Orforglipron Phase 3 ACHIEVE-1 topline](https://investor.lilly.com/news-releases/news-release-details/lillys-oral-glp-1-orforglipron-demonstrated-statistically)
- [Vertex: Positive zimislecel data at ADA](https://news.vrtx.com/news-releases/news-release-details/vertex-presents-positive-data-zimislecel-type-1-diabetes)
- [NEJM: Stem cell-derived islets for T1D](https://www.nejm.org/doi/abs/10.1056/NEJMoa2506549)
- [Stanford Medicine: GLP-1 drug resistance](https://med.stanford.edu/news/all-news/2026/04/glp-1-diabetes.html)
