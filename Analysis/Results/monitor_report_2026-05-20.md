# Diabetes Research Hub — Monitor Report

**Run date:** 2026-05-20
**Scope:** Automated review of hub outputs since 2026-05-19 (24h) with 7-day context
**Reviewer:** Scheduled monitor (read-only run)

---

## File System Status

All four script-output families are present. Three of the four were refreshed within the last 24 hours; the gap-analysis data file is stale.

| File | Last modified | Status |
|---|---|---|
| hub_monitor_report.md | 2026-05-20 | Fresh |
| clinical_trials_latest.json | 2026-05-20 | Fresh |
| clinical_trials_summary.md | 2026-05-20 | Fresh |
| pubmed_recent_latest.json | 2026-05-20 | Fresh |
| pubmed_recent_summary.md | 2026-05-20 | Fresh |
| literature_gap_report.md | 2026-05-19 | Fresh |
| **literature_gap_data.json** | **2026-04-20** | **STALE (29d)** |

The hub_monitor.py scan flagged **589 result files older than 14 days** as candidates for refresh — most are historical snapshots and are expected to stay frozen, but the gap-data JSON above is the actionable one.

## Clinical Trial Changes

The clinical_trials_latest.json snapshot now contains **797 unique trials** (153 T1D Cure/Cell Therapy, 72 T1D Immunotherapy/Prevention, 141 T2D Novel Therapies, 223 Devices, 280 Completed-with-Results). Status mix: 266 RECRUITING, 135 NOT_YET_RECRUITING, 109 ACTIVE_NOT_RECRUITING, 280 COMPLETED. 122 trials are PHASE3.

### Last 24h (vs. 2026-05-19 snapshot)
- **1 new trial.** NCT07595289 (Third Xiangya Hospital) — *DP-DCT 1.0: Dapagliflozin Combined With CGM* (NOT_YET_RECRUITING, NA).
- 0 removed, 0 status changes, 0 newly posted results.

### Last 7 days (vs. 2026-05-13 snapshot)
Eight new trials registered, two of them Phase 2 and one notable Phase 3:
- NCT07594145 — **Precision T1D Platform** (PHASE2, NOT_YET_RECRUITING).
- NCT07585630 — **A1Cantus vs. Placebo** (PHASE2, NOT_YET_RECRUITING).
- NCT04333823 — **Adolescent T1D Treatment with SGLT2i for Hyperglycemia & Hyperfiltration** (PHASE3, ACTIVE_NOT_RECRUITING) — a pediatric SGLT2i trial worth flagging given the Health Equity / Youth Diabetes overlap.
- NCT07593625 — Next-generation AID algorithm in adults with T1D (NA).
- NCT07589387 — Hypertension–Diabetes integration in Nigeria (formative aim).
- NCT04286555, NCT04226027 — both moved to COMPLETED with results posted (see below).
- NCT07595289 — Dapagliflozin + CGM (as above).

### Recently posted results worth reviewing (Phase 2/3 only)
Pulled from `has_results=true` with results_posted dates in the last 30 days:

| Date | NCT | Phase | Title (truncated) |
|---|---|---|---|
| 2026-05-13 | NCT05514535 | PHASE3 | Semaglutide + lower-dose insulin glargine (T2D) |
| 2026-05-04 | NCT03940209 | PHASE2 | Addressing Basic Needs to Improve Diabetes Outcomes in Medicaid Beneficiaries |
| 2026-04-30 | NCT05823948 | PHASE3 | Flash Glucose + once-weekly insulin Icodec |
| 2026-04-27 | NCT05649137 | PHASE3 | Semaglutide for excess weight + T2D |

### Key sponsor watchlist
- **Vertex:** 3 trials. Both **VX-880 / zimislecel** Phase 3 studies are RECRUITING (NCT04786262, NCT06832410). VX-264 (encapsulated) Phase 1/2 is ACTIVE_NOT_RECRUITING (NCT05791201). No status changes today.
- **Eli Lilly:** 27 trials including PHASE3 **baricitinib** programs in T1D (NCT07222137 adults; NCT07222332 children/adolescents) — both RECRUITING. **Orforglipron** Phase 3 obesity/T2D (NCT06972472) ACTIVE_NOT_RECRUITING. Tirzepatide T1D Phase 3 (NCT06962280, NCT06914895) ACTIVE_NOT_RECRUITING.
- **Novo Nordisk:** 26 trials. Active Phase 3 for **insulin icodec** (NCT07076199 RECRUITING) and multiple **CagriSema** Phase 3 studies (NCT06534411, NCT07220759 ACTIVE_NOT_RECRUITING).
- **Sana Biotechnology:** 0 trials in current snapshot (unchanged).

## PubMed Highlights

The latest pull surfaced **145 unique recent papers** across 16 alert domains and 8 tracked therapies. 28 papers are new since yesterday; 102 are new in the last 7 days.

### Cross-domain papers — highest priority

The three-domain hits are the headline items:

- **PMID 42154370** — *An Update and Overview of the Ocular and Extraocular Microbiome and Its Impact on Ophthalmic Care* (Advances in Therapy). Spans Diabetes Biomarker × Microbiome × Complications New. Directly relevant to the microbiome-ML pipeline and to the Retinopathy/Microbiome gap (currently flagged as low-overlap).
- **PMID 42148322** — *Metabolomics in Traditional Chinese Medicine for Diabetes Mellitus: Mechanistic Insights, Biomarker Discovery* — Biomarker × Microbiome × Multi-Omics.
- **PMID 42142983** — *Retrospective audit of weight loss and health outcomes following bariatric surgery* — GLP-1 × retatrutide × CagriSema cross-tags.

Two-domain hits worth reading:

- **PMID 42148104** — *Adapting CAR-T and CAR-Treg cancer therapies for autoimmunity* (T1D Stem Cell × T1D Immunotherapy). Directly relevant to the Treg/CAR-T research path.
- **PMID 42143506** — *Evolution of CAR therapies across oncology and autoimmunity* (T1D Immunotherapy × Gene Therapy).
- **PMID 42152039** — *Multi-omics profiling of the diabetic human heart* (Biomarker × Multi-Omics) — Genome Medicine.
- **PMID 42155730** — *Proteomic Analysis on Human Islets Suggests Nucleocytoplasmic Transport as a Mechanism of PERK Attenuation Effects in Diabetes* (T2D Remission × Biomarker) — Mol & Cell Proteomics.
- **PMID 42138126**, **42138080**, **42051156** — three teplizumab clinical-use papers (T1D Immunotherapy × Key Therapy: teplizumab), including a British Society consensus statement on Stage 2 T1D use and a US autoantibody-ordering pattern study.

### Key-therapy mentions (last 30 days)

- **Zimislecel:** 0 new papers — quiet on PubMed despite Phase 3 enrollment activity.
- **Orforglipron:** 3 (incl. PMID 42120723 — *Phase 3b ATTAIN-MAINTAIN trial for weight-loss maintenance*, and PMID 42116665 — GI safety meta-analysis). Lilly also disclosed positive ACHIEVE-2 / ACHIEVE-5 topline (see Breaking News).
- **Retatrutide:** 4 (lipid/metabolite profiling PMID 42135195; triple-hormone CKM review PMID 42108533).
- **CagriSema:** 2 (incl. PMID 41759565 — meta-analysis vs. semaglutide/placebo).
- **Baricitinib:** 2 — diabetes-relevance is indirect; the Phase 3 T1D programs (Lilly) are not yet showing up in indexed literature.
- **Teplizumab:** 5 — strong real-world / consensus output continuing.
- **Insulin icodec:** 3.
- **Dapagliflozin:** 35 indexed; 5 fetched.

### Publication volume trends
Net change is roughly steady (28 in / 27 out vs. yesterday). Diabetes AI/ML, Biomarker, and Microbiome continue to dominate (≥10 papers each in the lookback). LADA New Research and Diabetes Drug Repurpose remain the thinnest domains (5–6 each), consistent with the gap-analysis Tier 1 priorities.

## Gap Analysis Summary

Source: literature_gap_report.md (2026-05-19) and literature_gap_data.json (2026-04-20 — **29 days stale**).

Top 5 under-researched intersections (Gap Score = 100, BRONZE validation):

1. **Beta Cell Regen × Health Equity** (0 joint pubs / expected ~1,615)
2. **Insulin Resistance × Islet Transplant** (1 / ~2,138)
3. **Islet Transplant × GWAS / Polygenic** (0 / ~1,104) — classified as methodologically distinct
4. **Islet Transplant × Personalized Nutrition** (0 / ~378)
5. **Islet Transplant × Drug Repurposing** (0 / ~374)

Several of these align with the hub's existing Tier 1 contribution areas: the Islet Drug Repurposing analysis (Apr 3 outputs) already addresses #5, and the GLP-1 Pharmacogenomics Equity synthesis (Apr 17) touches #1. The Insulin-Resistance-in-Islet-Transplant-Recipients gap (#2) is the most actionable that has *no* existing hub artifact.

## Breaking News (web check, last 7 days)

Three items rise above routine news:

- **Afrezza (inhaled insulin) pediatric expansion** — PDUFA date **May 29, 2026**. If approved, the first needle-free insulin option for pediatric patients with T1D/T2D. Worth pre-staging tracker entries.
- **Eli Lilly orforglipron** — positive Phase 3 topline from **ACHIEVE-2 and ACHIEVE-5** in adults with T2D. Consistent with the new ATTAIN-MAINTAIN paper (PMID 42120723).
- **Vertex zimislecel Phase 3** — on track to support global regulatory submissions in 2026 per Vertex investor communications; Phase 1/2 follow-up data (12/12 engraftment, 10/12 insulin-independent at full dose) reaffirmed at ADA 85th Scientific Sessions.

Earlier in the year but still relevant context: Awiqli (insulin icodec) approved 2026-03-26 (first weekly basal); Langlara (insulin glargine-aldy biosimilar) approved 2026-04-29.

## Recommended Actions

1. **Refresh gap data — it's 29 days old.** Run `python project1_literature_gap_analysis.py` to regenerate literature_gap_data.json so the next monitor run has fresh inputs.
2. **Add Vertex zimislecel Phase 3 trials (NCT04786262, NCT06832410) to the tracker watchlist** with the latest enrollment status. The clinical_trials_summary.md "Notable Trials to Watch" table is currently empty — these are the obvious first entries, alongside the two Lilly baricitinib Phase 3 T1D studies (NCT07222137, NCT07222332).
3. **Open a deep-dive task on PMID 42154370** (ocular microbiome) — it spans three alert domains and connects directly to the existing microbiome-ML pipeline.
4. **Pre-stage Afrezza pediatric entry** ahead of the May 29 PDUFA date.
5. **Cross-reference PMID 42155730** (PERK attenuation in human islets) against the islet-repurposing target set (islet_repurposing_targets.json) — proteomic evidence may add to existing target rationale.
6. **Review PMID 42148104** (CAR-T/CAR-Treg for autoimmunity) for the Treg/CAR-T research path — Bronze-level addition to the evidence base.
7. **Investigate the unstudied intersection Insulin Resistance × Islet Transplant** — top-5 gap with no current hub artifact and a plausible clinical mechanism (graft survival in metabolically active recipients).

## Validation Notes (per RESEARCH_DOCTRINE)

- Clinical-trial change counts derive from snapshot JSON diffs (single source — GOLD for record-level facts, BRONZE for trend interpretation).
- PubMed counts are E-utilities snapshots; matching is keyword-based and may overcount.
- Web search items are SILVER until confirmed against sponsor press releases / FDA pages; the dates above are from secondary aggregators.
- Gap-analysis scores remain BRONZE pending domain-expert classification.

---

*Generated by the diabetes-hub-monitor scheduled task — 2026-05-20. No files were modified; this is a read-only review run.*

## Sources

- [Vertex Presents Positive Data for Zimislecel in Type 1 Diabetes (ADA 85th)](https://news.vrtx.com/news-releases/news-release-details/vertex-presents-positive-data-zimislecel-type-1-diabetes)
- [Phase 3 Trial of Vertex's Islet Cell Therapy for Type 1 Diabetes Under Way](https://www.managedhealthcareexecutive.com/view/phase-3-trial-of-vertex-s-islet-cell-therapy-for-type-1-diabetes-in-under-way)
- [2026 Predictions for New Diabetes Drugs (TCOYD)](https://tcoyd.org/2025/12/diabetes-predictions-2026/)
- [New FDA Drug Approvals for 2026 (Drugs.com)](https://www.drugs.com/newdrugs.html)
- [FDA Drug Approval Decisions Expected in May 2026 (Cardiology Advisor)](https://www.thecardiologyadvisor.com/news/fda-drug-approval-decisions-expected-in-may-2026/)
- [Novel Drug Approvals for 2026 (FDA)](https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026)
