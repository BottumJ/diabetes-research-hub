# Diabetes Hub Monitor Review — 2026-04-27

**Generated:** 2026-04-27 (automated review run)
**Hub root:** `Diabetes_Research/`
**Comparison windows:** today vs. 2026-04-26 (1d) and 2026-04-20 (7d)

---

## File System Status

All four core data files are present and fresh.

| File | Last modified | Age | Status |
|------|---------------|-----|--------|
| `Analysis/Results/hub_monitor_report.md` | 2026-04-27 07:05 | <1 d | Fresh |
| `Analysis/Results/clinical_trials_latest.json` | 2026-04-27 07:04 | <1 d | Fresh |
| `Analysis/Results/pubmed_recent_latest.json` | 2026-04-27 07:05 | <1 d | Fresh |
| `Analysis/Results/literature_gap_report.md` | 2026-04-26 14:06 | <1 d | Fresh |
| `Analysis/Results/literature_gap_data.json` | 2026-04-20 15:35 | 6.7 d | Approaching staleness (refresh by ~May 4) |

`hub_monitor.py` flagged 497 result files older than 14 days — consistent with normal long-tail snapshot accumulation, no action required. 762 files tracked overall (4 new today, 30 modified, 0 removed).

---

## Clinical Trial Changes

**Snapshot totals (2026-04-27):** 771 unique trials — 263 RECRUITING, 130 NOT_YET_RECRUITING, 109 ACTIVE_NOT_RECRUITING, 264 COMPLETED, 5 ENROLLING_BY_INVITATION. 115 are PHASE3.

### Day-over-day (2026-04-26 → 2026-04-27)
- New trials: 0
- Status changes: 0
- New results posted: 0

### Week-over-week (2026-04-20 → 2026-04-27)
- New trials: **6**
- Removed trials: 2
- Status changes: **4** (all RECRUITING → ACTIVE_NOT_RECRUITING — enrollment closed)
- New results posted: 0

**Status changes worth noting (RECRUITING → ACTIVE_NOT_RECRUITING):**

| NCT ID | Title (truncated) | Sponsor |
|--------|-------------------|---------|
| NCT06972472 | A Study of Orforglipron (LY3502970) in Participants With Obesity or Overweight... | Eli Lilly |
| NCT06993792 | A Master Protocol for Orforglipron (LY3502970) in Participants With Obesity... | Eli Lilly |
| NCT04061746 | Cellular Therapy for Type 1 Diabetes Using Mesenchymal Stem Cells | Medical Univ. of South Carolina |
| NCT05683990 | Diamyd® in Individuals at Risk for T1D | Diamyd Medical AB |

The two Lilly orforglipron trials closing enrollment in the same week is consistent with the FDA's Foundayo (orforglipron) approval announced 2026-04-01 — the late-stage program is now in readout phase rather than recruitment. Worth flagging for the tracker.

### New trials added in last 7 days (sample)

| NCT ID | Status | Phase | Sponsor | Topic |
|--------|--------|-------|---------|-------|
| NCT07546929 | RECRUITING | PHASE2 | Housey Healthcare | HP-211 dose-ranging |
| NCT07548996 | RECRUITING | PHASE2/3 | Nanjing Medical Univ. | Dimethyl fumarate in adult T1D (drug repurposing — Tier 1 area) |
| NCT05971940 | COMPLETED | PHASE3 | Eli Lilly | Orforglipron (LY3502970) in adult T2D |
| NCT05734989 | COMPLETED | NA | Duke University | Hispanic/Latinx CKD screening (health-equity intersection) |
| NCT05144737 | COMPLETED | NA | Johns Hopkins | Virtual cardiometabolic program for African immigrants (health equity) |
| NCT03898206 | COMPLETED | NA | Univ. of Bedfordshire | Sitting-break postprandial cardiometabolic |

NCT07548996 (dimethyl fumarate in T1D) is a potential touchpoint for the **Drug Repurposing × T1D Immunotherapy** intersection in our gap analysis — flag for follow-up.

### Key Phase 3 trials currently RECRUITING (from priority sponsors)
- **NCT06832410 / NCT04786262** — VX-880 (zimislecel, Vertex) in T1D
- **NCT07076199** — Insulin icodec weekly (Novo Nordisk)
- **NCT07222332 / NCT07222137** — Baricitinib in T1D (Eli Lilly) — both for beta-cell preservation and Stage 3 delay
- **NCT06739122** — Dulaglutide pediatric T2D (Eli Lilly)
- **NCT07088068** — Teplizumab vs placebo (Sanofi) — relevant to today's Tzield <8y label expansion (see Breaking News)

---

## PubMed Highlights

**Latest snapshot (2026-04-27):** 148 unique papers across 30-day window, 16 domains queried.

### Day-over-day (2026-04-26 → 2026-04-27)
- New papers: **30**
- Dropped (out of 30-day window): 28
- Cross-domain new today: **1** — see below

### Week-over-week (2026-04-20 → 2026-04-27)
- New papers: **98** in 7 days
- Cross-domain new this week: **10**

### Cross-domain papers (highest priority — multiple alert domains)

These are the highest-value items because they bridge research silos.

1. **PMID 42035781** — *Continuous glucose monitoring vs. self-monitoring of blood glucose in T2D: a randomised, multicentre, open-label trial.* (2026-Apr-23) — Domains: T1D Stem Cell Cure ∩ T2D GLP-1 New. **(Today's only new cross-domain paper.)**
2. **PMID 42023429** — *Gene Therapy and Gene Editing in T1D: CRISPR-Based β-Cell Replacement and Treg Immune Modulation Approaches.* (2026-Apr-23) — T1D Immunotherapy ∩ Gene Therapy. Highly relevant to **Treg/CAR-T × Gene Therapy** focus.
3. **PMID 42032109** — *Cell-specific DNA methylation in human alpha and beta cells regulates gene expression in T2D.* (2026-Apr-24) — Gene Therapy ∩ Epigenetics.
4. **PMID 42032377** — *Causal relationship between epigenetic markers and T2D in West African populations: Mendelian randomisation.* (2026-Apr-24) — Biomarker ∩ Epigenetics. **Relevant to Tier 1 Multi-Omics Integration AND to the Epigenetics × Health Equity gap (rank 16, 99.9).**
5. **PMID 42002040** — *Ketosis-Prone T2D: Three Decades of Clinical, Pathophysiologic, and Therapeutic Insights.* (2026-Apr-17) — T2D Remission ∩ LADA.
6. **PMID 41297910** — *Engineered nutrient-stimulated hormonal multi-agonists for precision targeting of obesity and metabolic disorders.* (2026-Apr) — orforglipron ∩ retatrutide ∩ CagriSema (triple-therapy review).
7. **PMID 42026776** — *Gut microbiome and pregnancy complications.* (2026-Dec-31 dated) — Microbiome ∩ Multi-Omics.
8. **PMID 42023215** — *Extracellular vesicles from [...]* (2026) — T1D Immunotherapy ∩ Microbiome.
9. **PMID 42022378** — *PPP1R14A in male erectile dysfunction.* (2026-Jun) — Biomarker ∩ Multi-Omics. Likely peripheral to diabetes; review for relevance.
10. **PMID 42003658** — *New Horizons in Metabolic Health: Future of Drug Discovery.* (2026-Apr-13) — Gene Therapy ∩ dapagliflozin.

### Key-therapy mentions (new this week, by therapy)
- **orforglipron:** 4 papers — bioequivalence (PMID 41994902), GLP-1 cardiometabolic profile (41992023), methodological critique (41984238), GRADE meta-analysis (41498807)
- **retatrutide:** 3 — GIPR:GCGR co-agonism rodent data (41997446), MAFLD/MASH review (41823054), T2D/obesity overview (41785010)
- **tirzepatide:** real-world cardio-metabolic-kidney outcomes (42029986); head-to-head vs. semaglutide (42030208)
- **semaglutide:** Indian phase trial (42026662); plus the comparison above
- **dapagliflozin:** podocyte/lactylation mechanism (42030222), HFmrEF outcomes vs empagliflozin (42034323), lipidomic remodeling (41998678), FAERS ketoacidosis disproportionality (42010884)
- **baricitinib:** hematopoietic chimerism / islet tolerance (42013280) — **directly relevant to NCT07222332/NCT07222137**
- **teplizumab:** 3 — personalized medicine review (41913320), 2× T1D screening editorials in *Diabetologia* (41572011, 41572010)
- **zimislecel:** no new papers this week (only baseline 2 in tracking)
- **CagriSema:** 1 (the multi-agonist review above)

### Volume trend
30 papers/day in/out is consistent with normal flow — no anomalous spike or drop in any single domain. Domain queries returned the standard cap of ~10 papers each, so apparent "low" domains (LADA: 4, Drug Repurposing: 4, GLP-1 Pharmacogenomics: 1) reflect genuinely lower indexing rather than query failure.

---

## Gap Analysis Summary

Source: `literature_gap_report.md` (v 2026-04-26) and `literature_gap_data.json` (v 2026-04-20).

**Top 5 under-researched intersections (Gap Score 100, BRONZE validation):**

| Rank | Pair | Joint Pubs | Why it matters |
|------|------|------------|----------------|
| 1 | Beta Cell Regen × Health Equity | 0 | Equity dimension of regenerative therapies (zimislecel, VX-880) is absent from literature. |
| 2 | Insulin Resistance × Islet Transplant | 1 | IR in islet recipients affects graft survival; barely studied. |
| 3 | Islet Transplant × Drug Repurposing | 0 | Repurposing existing immunosuppressants for islet protection — computational screening unattempted. |
| 4 | Islet Transplant × Health Equity | 0 | Few-center availability with no equity work. |
| 5 | Gene Therapy × LADA | 0 | LADA's autoimmunity makes it a candidate for gene therapy but no crossover. |

**Alignment with Tier 1 contribution areas (RESEARCH_DOCTRINE.md):**
- Tier 1 #2 (Literature Synthesis & Gap Analysis) — directly executed by this analysis.
- Tier 1 #4 (Drug Repurposing Computational Screening) — gap ranks 3 and 12 (Islet Transplant × Drug Repurposing, Drug Repurposing × Health Equity) are the most promotable to active workstreams. **NCT07548996 (dimethyl fumarate in T1D, posted this week) is a real-world signal that Drug Repurposing × T1D is becoming active.**
- Tier 1 #1 (Multi-Omics Biomarker Integration) — PMID 42032377 (West African MR study) is a concrete touchpoint.

---

## Breaking News (web check, last 7 days)

Three FDA actions and several Phase 3 readouts in April 2026 are highly relevant to the hub:

1. **2026-04-22 — FDA approves Tzield (teplizumab-mzwv) down to age 1** (was ≥8 years) for delaying Stage 3 T1D in Stage 2 patients. Supported by 1-year PETITE-T1D Phase 4 data, priority review. Sanofi press release. **Action: update tracker; note that NCT07088068 (Sanofi teplizumab Phase 3) is now post-label-expansion context.**
2. **2026-04-07 — FDA approves first generic dapagliflozin tablets** (HF hospitalization risk reduction in T2D + glycemic control). Pricing/access implications for the SGLT2-Inhibitor × Health-Equity gap.
3. **2026-04-01 — FDA approves Lilly's Foundayo (orforglipron)** as first time-flexible oral GLP-1 for weight loss in obesity / overweight with comorbidities. Explains the orforglipron Phase 3 enrollment closures observed in the trial-status diff above.
4. **2026-03 (still in 7-day discussion window) — Retatrutide met Phase 3 primary endpoint** in T2D (1.9 percentage point HbA1c reduction at top doses, 15% body weight loss at 12 mg). Lilly press release.
5. **Novo Nordisk PIONEER TEENS** — positive topline for oral semaglutide in pediatric T2D (April 2026).

These are aligned with what we're already tracking in the trial snapshot; primary action is a tracker update rather than scope expansion.

---

## Recommended Actions

1. **Update `Diabetes_Research_Tracker.xlsx`** with:
   - Tzield label expansion to age 1+ (FDA, 2026-04-22) — affects T1D Immunotherapy & Prevention category.
   - Foundayo (orforglipron) approval (2026-04-01) — and matching status changes on NCT06972472, NCT06993792.
   - Generic dapagliflozin approval (2026-04-07) — equity/pricing axis.
   - Add NCT07548996 (dimethyl fumarate in T1D) and NCT05971940 (Lilly orforglipron Phase 3 COMPLETED) as Notable Trials to Watch.
2. **Re-run gap analysis soon.** `literature_gap_data.json` is 6.7 days old; re-run on or before 2026-05-04: `python project1_literature_gap_analysis.py`
3. **Cross-domain paper deep dives** — write structured notes for the 3 highest-leverage cross-domain papers from this week:
   - PMID 42023429 (CRISPR β-cell + Treg) → maps to Tier 1 Drug Repurposing-adjacent + Cell Therapy.
   - PMID 42032377 (West African MR / epigenetics × T2D) → Tier 1 Multi-Omics, also bridges Health Equity gap.
   - PMID 42013280 (baricitinib + hematopoietic chimerism / islet tolerance) → directly relevant to Lilly NCT07222332/NCT07222137 Phase 3 trials.
4. **Verify gap entry #3 (Islet Transplant × Drug Repurposing)** with a targeted PubMed query — the score is 100 but worth confirming no terminology miss before promoting to a contribution workstream.
5. **No need to re-run** clinical-trials, PubMed, or hub-monitor scripts — all ran today and are fresh.

---

## Evidence Levels (per RESEARCH_DOCTRINE)

| Claim type | Level | Notes |
|------------|-------|-------|
| File-system facts (counts, mtimes) | DIRECT OBSERVATION | Read from filesystem this run. |
| Trial status changes | DIRECT OBSERVATION | Diffed snapshot JSONs locally. |
| Cross-domain paper classifications | BRONZE | From PubMed E-utilities domain hits (keyword-based). |
| Gap intersections | BRONZE | Geometric-mean bibliometric formula; needs expert validation. |
| Web-sourced FDA approvals | SECONDARY | Verify against FDA primary press release before tracker entry. |

---

*Generated automatically by the Diabetes Hub Monitor scheduled task. Source files: hub_monitor_report.md, clinical_trials_latest.json, pubmed_recent_latest.json, literature_gap_report.md, literature_gap_data.json. No files were modified during this run other than the creation of this report.*
