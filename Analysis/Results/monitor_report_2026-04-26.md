# Diabetes Research Hub — Monitor Report
**Generated:** 2026-04-26
**Run type:** Scheduled automated review (read-only)
**Compared against:** Previous snapshot (2026-04-25) and 7-day-prior snapshot (2026-04-19)

---

## TL;DR

- **No new clinical trials and no status changes** in the last 24 hours; activity is small but meaningful when looking at the past week (6 new trials, 4 status changes, 0 new posted results).
- **PubMed cohort refreshed today** with 3 new / 4 dropped papers in the rolling 30-day window. Over the past week, 94 of the 146 currently tracked papers are new, with 12 cross-domain papers — including a Nature Metabolism paper on cell-specific DNA methylation in alpha/beta cells (epigenetics × gene therapy), and a Lancet Diabetes & Endocrinology report on stem-cell-derived islet therapy in three T1D recipients with complete loss of endogenous insulin (T1D Stem Cell Cure).
- **Major external news (last 7 days)**: FDA expanded Sanofi's Tzield (teplizumab) label down to age 1 on April 22; Eli Lilly's oral GLP-1 Foundayo (orforglipron) was approved April 1; first generic dapagliflozin cleared April 7; Novo Nordisk reported positive PIONEER TEENS Phase 3 results for oral semaglutide in pediatric T2D.
- **Gap analysis is 6 days old (Apr 20)** — within the freshness window but worth re-running before next week's planning. Top under-researched intersections are dominated by Islet Transplant × {Health Equity, Drug Repurposing, GWAS}, all of which align with our Tier 1 contribution areas.
- **Hub-wide freshness flag**: 495 result files are older than 14 days. No corrupt/missing files in the core monitor pipeline.

---

## File System Status

All core monitor pipeline files are present and current:

| File | Last Modified | Status |
|------|---------------|--------|
| `hub_monitor_report.md` | 2026-04-26 07:04 | Fresh |
| `hub_monitor_state.json` | 2026-04-26 07:04 | Fresh |
| `clinical_trials_latest.json` | 2026-04-26 07:04 | Fresh |
| `clinical_trials_summary.md` | 2026-04-26 07:04 | Fresh |
| `pubmed_recent_latest.json` | 2026-04-26 07:04 | Fresh |
| `pubmed_recent_summary.md` | 2026-04-26 07:04 | Fresh |
| `literature_gap_data.json` | 2026-04-20 15:35 | 6 days old (still within 14-day window) |
| `literature_gap_report.md` | 2026-04-25 08:08 | Fresh |

`hub_monitor_report.md` flagged 495 result files older than 14 days. These are mostly historical snapshots and per-project artefacts, not the active pipeline; no immediate action needed unless a downstream dashboard depends on a specific stale file.

---

## Clinical Trial Changes

**Snapshot:** 771 unique trials tracked (151 T1D Cure & Cell Therapy / 72 T1D Immunotherapy / 136 T2D Novel Therapies / 222 Devices / 264 Recently Completed). 263 currently RECRUITING, 130 NOT_YET_RECRUITING, 109 ACTIVE_NOT_RECRUITING, 264 COMPLETED.

### 24-hour diff (2026-04-25 → 2026-04-26)
No changes — 0 new, 0 removed, 0 status changes, 0 newly posted results.

### 7-day diff (2026-04-19 → 2026-04-26)

**6 new trials added:**
- `NCT05971940` — *Orforglipron in T2D* (Eli Lilly, Phase 3, COMPLETED). Strategically important: orforglipron just received FDA approval April 1.
- `NCT07548996` — *Open-Label Dimethyl Fumarate in Adult T1D* (Nanjing Medical University, Phase 2/3, RECRUITING). Repurposing angle — DMF is approved for MS.
- `NCT07546929` — *HP-211 Safety/Proof-of-Concept Dose Ranging* (Housey Healthcare, Phase 2, RECRUITING).
- `NCT05144737` — Afro-DPP virtual cardiometabolic program for African immigrants (Johns Hopkins, COMPLETED).
- `NCT05734989` — Hispanic/Latinx CKD screening (Duke, COMPLETED).
- `NCT03898206` — Sitting interruption / postprandial cardiometabolic disease (U of Bedfordshire, COMPLETED).

**4 status changes (all RECRUITING → ACTIVE_NOT_RECRUITING — i.e., enrollment closed):**
- `NCT06972472` — Orforglipron in obesity/CKD (Eli Lilly, Phase 3)
- `NCT06993792` — Master protocol for Orforglipron (Eli Lilly, Phase 3)
- `NCT04061746` — MSC cell therapy in T1D (Phase ≤2)
- `NCT05683990` — Diamyd (GAD-alum) in islet autoimmunity (Phase 3)

The two Eli Lilly Orforglipron status changes coincide with the FDA approval (Apr 1) — enrollment closure is the expected next step.

### Phase 3 RECRUITING (43 total) — strategic watch list

Most notable currently recruiting Phase 3 trials in our priority areas:

| NCT | Sponsor | Trial |
|-----|---------|-------|
| NCT06832410 | **Vertex** | VX-880 (zimislecel) efficacy/safety in T1D |
| NCT04786262 | **Vertex** | VX-880 safety/tolerability/efficacy in T1D |
| NCT07088068 | Sanofi | Teplizumab vs placebo in stage-2 T1D |
| NCT07222332 | **Eli Lilly** | Baricitinib for beta-cell preservation, new-onset T1D |
| NCT07222137 | **Eli Lilly** | Baricitinib to delay stage-3 T1D in at-risk children |
| NCT07076199 | **Novo Nordisk** | Insulin Icodec (weekly) in pediatric T2D |
| NCT06334133 | vTv Therapeutics | Cadisegliatin (glucokinase activator) adjunct in T1D |
| NCT06217302 | A. Doria | Sotagliflozin to slow CKD in T1D + DKD |

### Recently posted results (since Apr 1)
14 trials posted results in April. Highlights:
- `NCT05971940` (Eli Lilly, Apr 22) — Orforglipron in T2D **with results posted**, parallel to FDA approval timeline.
- `NCT05144984` (Novo Nordisk, Apr 9) — semaglutide combination study results.
- `NCT05923827` (Insulet, Apr 14) — Omnipod 5 + Libre 2 vs MDI in T1D.
- `NCT05238142` (Medtronic, Apr 16) — MiniMed 780G in T2D.

### Key-org footprint
26 trials currently active/recruiting/not-yet-recruiting from Vertex, Eli Lilly, Novo Nordisk, or Sana. **No Sana Biotechnology trials present in the snapshot** — worth verifying that the upstream search is hitting Sana's gene-edited islet program.

---

## PubMed Highlights

**Snapshot:** 146 unique papers across 16 alert domains (rolling 30-day lookback). 94 papers are new vs. last week's snapshot; 90 dropped out as they aged past 30 days.

### Cross-domain papers (highest priority — 12 total)

The single cross-3-domain paper:
- **PMID 41297910** *Engineered nutrient-stimulated hormonal multi-agonists for precision targeting of obesity and metabolic diseases* — Clinical and Molecular Hepatology. Spans orforglipron, retatrutide, and CagriSema — a rare integrative review of incretin multi-agonists.

Notable 2-domain papers:
- **PMID 42032109** *Cell-specific DNA methylation in human alpha and beta cells regulates gene expression in type 2 diabetes* — **Nature Metabolism**. Spans Gene Therapy + Epigenetics. Bronze-evidence interest: aligns with our Tier 1 multi-omics work.
- **PMID 42023429** *Gene Therapy and Gene Editing in Type 1 Diabetes: CRISPR-Based β-Cell Replacement and Treg Immune Modulation Approaches* — Diabetes, Obesity & Metabolism. Spans T1D Immunotherapy + Gene Therapy.
- **PMID 42032377** *Causal relationship between epigenetic markers and T2D in West African populations: Mendelian Randomization* — Diabetologia. Biomarker + Epigenetics, with health-equity relevance.
- **PMID 42017289** *Integrative Proteomic and ML Analysis Identifies Novel Predictors and Risk Model for Diabetic [Complications]* — Diabetes, Obesity & Metabolism. Biomarker + Multi-Omics — directly maps to our AI/ML model-building tier.
- **PMID 42021523** *Integrating novel T2D progression & OSA economic modelling* — J Med Economics. T2D GLP-1 New + T2D Remission.

### Key-therapy mentions in current 30-day window
| Therapy | Papers |
|---------|--------|
| dapagliflozin | 5 |
| orforglipron | 5 |
| retatrutide | 4 |
| teplizumab | 4 |
| baricitinib | 1 |
| CagriSema | 1 |
| zimislecel | 0 |
| icodec | 0 |

The standout new paper this week: **PMID 41498807** *Efficacy and safety of orforglipron in T2D and obesity: a GRADE-assessed meta-analysis* — given Foundayo just got FDA approval, this is timely Bronze-evidence to capture.

### New papers in priority domains (since 7 days ago)
- **PMID 41765034** *Autologous and allogeneic stem cell-derived islet therapy in three recipients with T1D and complete loss of endogenous insulin* — **Lancet Diabetes & Endocrinology**. Material for the T1D Stem Cell Cure tracker.
- **PMID 41763233** *From survival to freedom: redefining success in T1D* — Lancet D&E commentary — likely paired with the islet-therapy paper.
- **PMID 42012980** *Durable control of autoimmunity requires sustained stimulation of regulatory T cells* — **Cell Reports**. Treg/CAR-T relevance.
- **PMID 41999654** *Leveraging a naturally occurring IgM autoantibody to target diabetogenic T cells* — Journal of Immunology. T1D precision-immunotherapy candidate.
- **PMID 42012986** *Frequency of islet autoantibody seropositivity among adults with newly diagnosed T2D in the Kazakh population* — LADA-relevant — directly maps to our flagged "Health Equity × LADA" gap.
- **PMID 42011518** *Combination Gene Therapy with AAV-Based Vectors Ameliorates the Phenotype of T2D in Diet-Induced Obese* — Molecular Pharmaceutics.

### Domain volume notes
- "T2D GLP-1 New" remains massively oversubscribed at the source (158 PubMed hits in 30 days, 10 captured) — sampling cap is hiding signal.
- "GLP-1 Pharmacogenomics" only had 1 paper this 30-day window — long tail confirms our gap finding.
- "Diabetes Drug Repurpose" (4 papers) and "LADA New Research" (4 papers) returned all available hits.

---

## Gap Analysis Summary

Source: `literature_gap_data.json` (generated 2026-04-20). 30 domains, 435 pairs analyzed.

**Top 5 under-researched intersections (Gap Score 100, 0–1 joint papers):**

| Rank | Pair | Joint Pubs | Tier-1 Alignment |
|------|------|------------|------------------|
| 1 | Beta Cell Regen × Health Equity | 0 | ✓ Epidemiological / Health Equity (Tier 1) |
| 2 | Insulin Resistance × Islet Transplant | 1 | Indirect — clinical trial intelligence |
| 3 | Islet Transplant × GWAS / Polygenic | 0 | ✓ AI/ML Prediction (Tier 1) |
| 4 | Islet Transplant × Personalized Nutr | 0 | Tier 2 |
| 5 | Islet Transplant × Drug Repurposing | 0 | ✓ Drug Repurposing (Tier 1) |

These continue last week's pattern: Islet Transplant is the central under-connected node. Two of the top five intersections (Beta Cell Regen × Health Equity, Islet Transplant × Drug Repurposing) directly map to our Tier 1 contribution doctrine — both are credible computational targets given accessible data.

The newly published paper on islet autoantibodies in Kazakh adults (PMID 42012986) is a small but real data point against the **Health Equity × LADA** gap (also Gap Score 100 in last week's run).

---

## Breaking News (Web Check, last 7 days)

**FDA actions:**
- **Apr 22, 2026** — FDA approved Sanofi's Tzield (teplizumab-mzwv) label expansion to children **as young as age 1** (down from age 8) for delaying onset of stage-3 T1D. Supported by PETITE-T1D Phase 4 data. Major implication for stage-2 screening pipelines and pediatric immunotherapy access.
- **Apr 7, 2026** — FDA approved the **first generic dapagliflozin** tablets (T2D + HF hospitalization risk reduction). Significant cost-of-care implication; relevant to Health Equity tracker.
- **Apr 1, 2026** — FDA approved Eli Lilly's **Foundayo (orforglipron)** — first GLP-1 pill that can be taken any time without food/water restriction (initial indication weight loss; T2D filings in 40+ countries).

**Phase 3 readouts:**
- **Novo Nordisk's PIONEER TEENS** — positive Phase 3a topline for oral semaglutide in **pediatric T2D**: 0.83% placebo-adjusted HbA1c reduction. Regulatory filing planned H2 2026.

All four items align with active trials already in our snapshot and should be cross-referenced into the tracker's "Notable Trials to Watch" section, which is currently empty.

---

## Recommended Actions

**Immediate (this week):**
1. Add the four FDA / Phase-3 items above to `clinical_trials_summary.md` under "Notable Trials to Watch" — that section is currently empty (`| | | |`).
2. Pull full text for **PMID 41765034** (Lancet D&E islet therapy) and **PMID 42032109** (Nature Metabolism alpha/beta cell methylation) into the paper library — both are Tier-1-aligned and likely to be cited repeatedly.
3. Update the tracker (`Diabetes_Research_Tracker.xlsx`) with the 4 status changes (Orforglipron x2, MSC T1D, Diamyd) — all moved to ACTIVE_NOT_RECRUITING.

**Within ~1 week:**
4. Re-run `python project1_literature_gap_analysis.py` — current gap data is 6 days old; refresh is appropriate before any new gap-driven synthesis work.
5. Verify the PubMed sampling cap. 13 of 16 domains hit the 10-paper cap, so we're under-sampling busy domains (T2D GLP-1 returns 158 candidates → 10 captured). Consider raising the per-domain limit or stratifying by impact factor.
6. Investigate why **Sana Biotechnology** has no trials in the snapshot — may need to add an explicit sponsor query in `baseline_clinical_trials.py`.

**Optional / lower priority:**
7. Sweep the 495 result files >14 days old to identify any that should be archived vs. refreshed.
8. Cross-reference the Kazakh LADA seropositivity paper (PMID 42012986) against the Health Equity × LADA gap to see if it changes the gap-score classification.

---

## Doctrine Compliance

- All claims above are sourced to either (a) files in `Analysis/Results/` or (b) the cited web search. No new clinical claims are made in this report.
- New literature findings are flagged at **BRONZE** evidence level pending further verification per the Research Doctrine.
- This run is read-only: no files in the workspace were modified except this report.

---

## Sources

- [Sanofi — Tzield approved in the US to delay stage-3 T1D in young children (Apr 22, 2026)](https://www.sanofi.com/en/media-room/press-releases/2026/2026-04-22-05-05-00-3278650)
- [Eli Lilly — FDA Approves Foundayo (orforglipron) (Apr 1, 2026)](https://investor.lilly.com/news-releases/news-release-details/fda-approves-lillys-foundayotm-orforglipron-only-glp-1-pill)
- [FDA — First Generic Dapagliflozin Tablets Approved (Apr 7, 2026)](https://www.fda.gov/drugs/drug-alerts-and-statements/fda-approves-first-generic-dapagliflozin-tablets)
- [Novo Nordisk — PIONEER TEENS Phase 3a Topline for Oral Semaglutide in Pediatric T2D](https://www.biotechreality.com/2026/04/novo-nordisk-oral-semaglutide-for-type-2-diabetes-in-children.html)
- [Endocrine News — Pharma Friday, April 24, 2026](https://endocrinenews.endocrine.org/pharma-friday-april-24-2026)

*Generated by automated diabetes-hub-monitor scheduled task — 2026-04-26.*
