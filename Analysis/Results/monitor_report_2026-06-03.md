# Diabetes Hub Monitor Report — 2026-06-03

**Run type:** Scheduled automated monitor
**Compared to:** clinical_trials_snapshot_2026-06-02.json, clinical_trials_snapshot_2026-05-27.json (week-over-week)
**Validation level:** BRONZE (single source, automated review)

---

## File System Status

| File | Last Modified | Status |
|------|---------------|--------|
| hub_monitor_report.md | 2026-06-03 07:04 | Fresh |
| clinical_trials_latest.json | 2026-06-03 07:04 | Fresh (800 trials) |
| pubmed_recent_latest.json | 2026-06-03 07:04 | Fresh (163 papers across 16 domains) |
| pubmed_recent_summary.md | 2026-06-03 07:04 | Fresh |
| literature_gap_report.md | 2026-06-02 08:08 | Fresh |
| literature_gap_data.json | **2026-04-20 15:35** | **STALE (>14 days)** — rerun gap script |
| hub_monitor_state.json | 2026-06-03 07:04 | Fresh |

The hub_monitor flagged 670 total result files older than 14 days — most are archived daily snapshots, which is expected.

---

## Clinical Trial Changes

### 24-hour diff (vs 2026-06-02)
- **New:** NCT07619833 — Daewoong Pharmaceutical, Phase 3, "Initial Combination Therapy With DWP16001" (NOT_YET_RECRUITING). DWP16001 is an SGLT2 inhibitor (enavogliflozin); worth tagging for the SGLT2 domain.
- **Removed:** NCT06853990 — Deka R&D, automated insulin delivery system for T2D.
- Total: 800 trials (unchanged).

### Week-over-week (vs 2026-05-27)
- **New trials (12)** — Notables:
  - **NCT07613307** — Eli Lilly, **Phase 3, Orforglipron (LY3502970)** in T2D patients with prior bariatric surgery. NOT_YET_RECRUITING. Tier 1 signal.
  - **NCT07614412** — SHIELD-T1D, Saudi MoH, Phase 2: Shingrix + GLP-1 agonist for beta-cell preservation in recent-onset T1D. Novel combination concept.
  - **NCT07616206** — vTv Therapeutics, Phase 2: Cadisegliatin (glucokinase activator) as adjunct to insulin in T1D. Relevant to gap matrix (Glucokinase × LADA/Beta Cell).
  - **NCT07610213** — Sequential immune modulation + antigen-specific tolerance for T1D (Phase 1).

- **Status changes (11)** — Key items:
  - **NCT07284511** RECRUITING (was NOT_YET) — McGill, Phase 2/3 tirzepatide adjunctive in T1D automated insulin delivery.
  - **NCT07564414** RECRUITING (was NOT_YET) — Novo Nordisk, Phase 3 CagriSema dose-comparison study.
  - **NCT06728059** COMPLETED (was RECRUITING) — ML bolus-priming feasibility; results posted 2026-05-28.

- **New results posted in last 7 days (1):** NCT06728059 (ML bolus-priming).
- **New results posted in last 14 days (8 total):** includes NCT04426474 (LY3502970/orforglipron Phase 1 in T2D, results 2026-05-26), NCT05925920 (ENT-03 obesity/diabetes Phase 1).

### Key-organization Phase 3 trials still active
- **Vertex VX-880 (T1D islet cell therapy):** NCT06832410 RECRUITING; NCT04786262 RECRUITING.
- **Eli Lilly baricitinib for T1D beta-cell preservation:** NCT07222332, NCT07222137 — both RECRUITING.
- **Eli Lilly retatrutide:** NCT05929079, NCT06260722, NCT06297603 — all ACTIVE_NOT_RECRUITING (readouts forthcoming).
- **Eli Lilly orforglipron:** NCT07613307 (new this week, NOT_YET); NCT07613307, NCT06993792, NCT06972472 in active Phase 3.
- **Novo Nordisk CagriSema:** NCT07564414, NCT07282613, NCT06534411, NCT07400107.

---

## PubMed Highlights (30-day lookback, 163 papers)

### Cross-domain papers (highest priority — 14 total)
Cross-domain papers from this week's diff worth surfacing:
- **PMID 42228334** — "Renal or Hepatic Impairment Does Not Affect Pharmacokinetics, Safety, or Tolerability of Subcutaneous [CagriSema]." Domains: T2D GLP-1 New + Key Therapy: CagriSema. Supports broader CagriSema labeling.
- **PMID 42230773** — "Integrative analyses elucidate transcriptional regulatory functions of risk alleles for metabolic [disease]." Domains: AI/ML + Gene Therapy.
- **PMID 42228639** — "Proteomic signatures of early retinal neurodegeneration in T2D." Domains: AI/ML + Biomarker.
- **PMID 42198313** — Diabetes Mellitus and Stroke review covering orforglipron + retatrutide + CagriSema together. Useful synthesis paper.
- **PMID 42221148** — Systematic review of teplizumab efficacy/safety in Stage 3 T1D.

### Key-therapy publication counts (last 30 days)
| Therapy | Papers | Notes |
|---------|--------|-------|
| dapagliflozin | 5 (50 total in PubMed) | High background activity |
| retatrutide | 5 (10 total) | Elevated — TRIUMPH-1 readout context |
| CagriSema | 5 (6 total) | Mostly Novo PK/PD papers |
| icodec | 5 (6 total) | Weekly basal insulin |
| teplizumab | 5 (6 total) | Tzield post-marketing focus |
| orforglipron | 4 (4 total) | Pre-approval activity |
| baricitinib | 3 (3 total) | T1D beta-cell preservation angle |
| **zimislecel** | **0 (0 total)** | **No new publications — monitor.** |

### Publication volume trends
- Diabetes AI/ML (227 total PubMed hits in window) and Biomarker (168) remain highest-volume domains.
- LADA New Research (9) and Drug Repurposing (5) remain low-volume — consistent with gap matrix.
- 24 new papers / 23 dropped vs prior day's snapshot — steady churn.

---

## Gap Analysis Summary (literature_gap_report.md, 2026-06-02)

**Top 5 under-researched intersections (Gap Score 100, 0–1 joint papers):**

1. Beta Cell Regen × Health Equity — no access/equity analysis of regenerative therapies.
2. Insulin Resistance × Islet Transplant — affects graft survival but barely studied.
3. Islet Transplant × Drug Repurposing — computational screening for immunosuppressant repurposing not applied.
4. Islet Transplant × Health Equity — access equity at select centers unstudied.
5. Gene Therapy × LADA — autoimmune mechanism makes LADA a plausible candidate; no crossover work.

**Alignment with Tier 1 doctrine areas:** Several gaps map directly to Tier 1 contribution areas (LADA, Beta Cell Regen, Drug Repurposing, Health Equity). These remain the highest-leverage targets for computational synthesis.

**Caveat:** Gap data underlying this report (literature_gap_data.json) is from **2026-04-20** — 44 days old. The gap counts may have shifted; rerun `project1_literature_gap_analysis.py` before acting on rankings.

---

## Breaking News (Last 7 Days)

1. **Lilly TRIUMPH-1 readout (May 21, 2026)** — Phase 3 retatrutide in obesity without T2D met primary endpoint; 12 mg arm averaged 28.3% weight loss at 80 weeks; 45.3% of participants achieved ≥30% loss. TRIUMPH-2 (T2D) and TRIUMPH-3 (CV disease) expected later in 2026. *Relevant trials in our tracker: NCT05929079, NCT06260722, NCT06297603.*

2. **MannKind Afrezza pediatric approval (May 29, 2026)** — FDA cleared inhaled mealtime insulin Afrezza for ages 6+. First inhaled insulin for pediatric use. Phase 3 INHALE-1 supported the approval.

No other major Phase 3 readouts or FDA actions in the 7-day window meet the "significant" threshold.

---

## Recommended Actions

1. **Re-run gap analysis** — `python project1_literature_gap_analysis.py` (data is 44 days stale).
2. **Update tracker** for:
   - NCT07613307 (orforglipron Phase 3 post-bariatric) — new this week.
   - NCT07614412 (SHIELD-T1D, Shingrix + GLP-1 for beta-cell preservation) — novel combo, T1D Cure & Cell Therapy category.
   - NCT07616206 (cadisegliatin in T1D) — Glucokinase domain.
   - NCT07619833 (DWP16001 / enavogliflozin Phase 3) — SGLT2 combination.
3. **Add Afrezza pediatric approval** to T1D Technology / Pediatrics tracker rows; cite FDA approval 2026-05-29.
4. **Add TRIUMPH-1 readout** to retatrutide row; reference NCT and Lilly press release (2026-05-21).
5. **Review cross-domain PubMed paper** PMID 42230773 (AI/ML × Gene Therapy) and PMID 42198313 (multi-therapy stroke review) — both candidate inputs for Tier 1 syntheses.
6. **Monitor zimislecel** — still zero PubMed activity; follow Vertex VX-880 NCT06832410 / NCT04786262 directly.
7. **No file modifications made** — this is a review run only.

---

*Generated by automated Diabetes Hub monitor — 2026-06-03. Per Research Doctrine v1.0, all findings here are BRONZE-level (single automated source) and require domain expert verification before incorporation into formal outputs.*

## Sources

- [MannKind FDA Approval of Afrezza pediatric, May 29, 2026](https://www.globenewswire.com/news-release/2026/05/29/3303734/29517/en/mannkind-announces-fda-approval-of-afrezza-the-first-and-only-inhaled-mealtime-insulin-for-use-in-children-and-adolescents-aged-6-and-older-living-with-diabetes.html)
- [Lilly TRIUMPH-1 retatrutide Phase 3 readout, May 21, 2026](https://www.prnewswire.com/news-releases/lillys-triple-agonist-retatrutide-delivered-powerful-weight-loss-in-pivotal-phase-3-obesity-trial-302778859.html)
- [FDA Novel Drug Approvals 2026](https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026)
