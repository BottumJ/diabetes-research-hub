# Diabetes Research Hub — Monitor Review Report
**Run date:** 2026-06-05 (automated)
**Reviewer:** Hub monitor (scheduled task)
**Scope:** Read-only review of latest script outputs + 7-day web check. No existing files modified.

---

## Executive Summary

Data pipeline is healthy: clinical-trial and PubMed snapshots both refreshed **2026-06-04** (1 day old). The one stale input is the **literature gap analysis** — the human-readable report (`literature_gap_report.md`) regenerated 2026-06-03, but its underlying data file (`literature_gap_data.json`) has not been rebuilt since **2026-04-20 (46 days old)**; the report appears to reuse old computations and should be re-run.

Most actionable items this week: a new **Phase 3 orforglipron T2D trial** (Eli Lilly, NCT07613307) and a **CagriSema Phase 3** flipping to RECRUITING (Novo Nordisk, NCT07564414) — both relevant given orforglipron's April 1 FDA approval and Lilly's planned T2D filing. The **ADA 2026 Scientific Sessions run June 5–8 (starting today)**, so expect a wave of late-breaking data on zimislecel, CagriSema, and orforglipron over the next several days.

---

## File System Status

| File | Last modified | Status |
|------|---------------|--------|
| clinical_trials_latest.json | 2026-06-04 | Fresh |
| pubmed_recent_latest.json | 2026-06-04 | Fresh |
| hub_monitor_report.md | 2026-06-04 | Fresh |
| literature_gap_report.md | 2026-06-03 | Current report, but… |
| literature_gap_data.json | **2026-04-20** | **Stale (46 days)** — underlying data not regenerated |
| Latest dated trial snapshot | clinical_trials_snapshot_2026-06-04.json | Present |
| Latest dated PubMed snapshot | pubmed_recent_snapshot_2026-06-04.json | Present |

All five expected input files exist; no scripts need a cold start. The hub monitor's own run flags **674 result files older than 14 days** — almost all are archival dated snapshots (expected) and not a concern, with the single exception of the gap data noted above.

---

## Clinical Trial Changes

**Totals:** 801 unique trials (263 RECRUITING, 134 NOT_YET_RECRUITING, 289 COMPLETED-with-results, 108 ACTIVE_NOT_RECRUITING). 123 are Phase 3; **46 Phase 3 trials are currently RECRUITING.**

**Change vs. one week ago (2026-05-28 snapshot):** 11 new trials, 10 removed, 10 status changes, 1 new results posting.

Notable status changes (→ RECRUITING):
- **NCT07564414** — CagriSema, two-dose study (Novo Nordisk), **PHASE3** — NOT_YET_RECRUITING → RECRUITING
- **NCT07599982** — MODI insulin-titration algorithm safety, adults
- **NCT07521475** — Fully closed-loop Omnipod in T2D
- **NCT07579702** — Omnipod 6 vs Omnipod 5
- **NCT07303803** — Chiglitazar in MASH (Phase 2)

Notable new trials:
- **NCT07613307** — Orforglipron (LY3502970) in T2D, **PHASE3** (Eli Lilly, not-yet-recruiting) — aligns with Lilly's stated plan to file orforglipron for T2D this year
- **NCT05813912** — Weekly insulin **icodec**, **PHASE3 COMPLETED** (Novo Nordisk)
- **NCT07614412** — **SHIELD-T1D**: Shingrix + GLP-1 agonist for beta-cell preservation in recent-onset T1D (Phase 2) — novel repurposing-style combination
- **NCT07616206** — Cadisegliatin (glucokinase activator) adjunct to insulin in T1D, Phase 2 (vTv Therapeutics)
- **NCT07619833** — Initial combination therapy, Phase 3 (Daewoong)
- **NCT05925920** — ENT-03 for obesity, Phase 1 COMPLETED (Metabolics Pharma)

**New results posted (1):** NCT06728059 — ML bolus-priming added to closed-loop (results posted 2026-05-28).

**Key Phase 3 programs being tracked (all RECRUITING unless noted):**
- **Zimislecel / VX-880** (Vertex) — NCT04786262 and NCT06832410, both Phase 3 RECRUITING (kidney-transplant cohort in the latter)
- **Baricitinib** (Eli Lilly) — NCT07222332 (preserve beta-cell function) and NCT07222137 (delay Stage 3), both Phase 3 RECRUITING
- **Teplizumab** (Sanofi) — NCT07088068, Phase 3 RECRUITING (7 teplizumab trials total across phases)
- **Retatrutide** (Eli Lilly) — 3 Phase 3 trials, all ACTIVE_NOT_RECRUITING

---

## PubMed Highlights

162 unique papers across 16 alert domains (30-day lookback). Domain volumes are evenly capped (~10 papers/domain), so volume-trend signal is limited this cycle; the value is in cross-domain and key-therapy hits.

**Cross-domain papers (highest priority — 15 total). Most relevant:**
- **[42163482]** *Extracellular vesicle proteins as predictive biomarkers for developing T1D* (Proteomics) — T1D Stem Cell + Immunotherapy + teplizumab. Directly relevant to our biomarker/immunotherapy intersection.
- **[42230773]** *Integrative analyses of transcriptional regulatory functions of risk alleles for metabolic disease* (**Nature Genetics**) — AI/ML + Gene Therapy. High-impact venue; relevant to Tier 1 Multi-Omics.
- **[42228639]** *Proteomic signatures of early retinal neurodegeneration in T2D* (**PLoS Medicine**) — AI/ML + Biomarker.
- **[42138080]** *New and emerging therapies in T1D* (**J Clin Invest**) — Immunotherapy + teplizumab review.
- **[42221148]** *Efficacy and safety of teplizumab in Stage 3 T1D: systematic review* — Immunotherapy + teplizumab.
- **[42235729] / [42232971] / [42225355]** — three Biomarker × Complications papers on diabetic kidney disease and retinopathy biomarkers (two newly cross-domain per the 06-04 hub diff).

**Key-therapy publication activity (last 30 days):** teplizumab 5, CagriSema 5, retatrutide 5, icodec 5, dapagliflozin 5, orforglipron 4, baricitinib 3. All eight tracked therapies (incl. zimislecel) are appearing — no domain went dark.

---

## Gap Analysis Summary

Top 5 under-researched intersections (Gap Score, Validation level **BRONZE** — single analytical source, requires expert confirmation):

| Rank | Intersection | Gap Score | Joint Pubs |
|------|--------------|-----------|------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 |
| 3 | Islet Transplant × Drug Repurposing | 100.0 | 0 |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 |
| 5 | Gene Therapy × LADA | 100.0 | 0 |

**Alignment with Research Doctrine Tier 1 areas:**
- **#3 Islet Transplant × Drug Repurposing** maps directly to Tier 1 **Drug Repurposing Computational Screening** (Doctrine §4) — strongest candidate for an actionable contribution.
- Gaps **#1 and #4 (Health Equity intersections)** map to Tier 1 **Epidemiological / Health Equity Analysis** (Doctrine §6).
- The gap analysis exercise itself is Tier 1 **Literature Synthesis & Gap Analysis** (Doctrine §2).

Caveat per doctrine: these are keyword-based, BRONZE-level findings. Before acting, verify each with a combined-term PubMed search and check Cochrane/PROSPERO for existing reviews.

---

## Breaking News (7-day web check)

- **ADA 2026 Scientific Sessions — June 5–8, New Orleans (begins today).** Expect late-breaking readouts; Vertex has historically released zimislecel data at ADA. Worth monitoring daily this week. *(Evidence: conference announcement — Level: news/pending data.)*
- **Orforglipron (Foundayo) — FDA approved April 1, 2026** for chronic weight management (first oral GLP-1 with no food/water timing restrictions; based on ATTAIN-1/-2). Eli Lilly plans a **T2D filing this year** off the ACHIEVE Phase 3 program — consistent with the new Phase 3 T2D trial NCT07613307 seen above. *(Level: regulatory action, confirmed.)*
- **Zimislecel (VX-880) — regulatory submission expected in 2026** (timeline accelerated from 2030; fast-track designation; potential availability ~2027). No BLA decision yet reported. *(Level: company guidance, unconfirmed timing.)*
- **Stem-cell beta-cell advance (Sweden)** — more reliable derivation of insulin-producing cells from human stem cells, reversed diabetes in mice. *(Level: preclinical/animal — low actionability, monitor only.)*

Nothing this week constitutes a confirmed Phase 3 human-efficacy readout or new FDA approval beyond the already-known April orforglipron action.

---

## Recommended Actions

1. **Re-run the gap analysis.** `literature_gap_data.json` is 46 days old (2026-04-20); the 06-03 report likely reused stale computations. Run: `python project1_literature_gap_analysis.py`.
2. **Prioritize Islet Transplant × Drug Repurposing (Gap #3)** as the next Tier 1 computational contribution — it aligns with Doctrine §4 and has zero joint publications. Verify with a combined-term PubMed search first.
3. **Add to tracker watch list:** the new Phase 3 orforglipron T2D trial (NCT07613307) and the CagriSema Phase 3 now recruiting (NCT07564414); confirm zimislecel/VX-880 (NCT04786262, NCT06832410), baricitinib (NCT07222332, NCT07222137), and teplizumab (NCT07088068) are flagged as Phase 3 priorities.
4. **Monitor ADA 2026 (June 5–8) daily this week** for zimislecel, CagriSema, and orforglipron late-breaking data; capture any Phase 3 readouts into the next snapshot review.
5. **Review cross-domain papers** [42230773] (Nature Genetics) and [42163482] (EV biomarkers/T1D) — both intersect Tier 1 Multi-Omics and the T1D immunotherapy program.
6. **No file cleanup needed** for the 674 "stale" results — they are archival dated snapshots. Only the gap data file warrants a refresh.

---
*Generated by the Diabetes Hub scheduled monitor. Read-only review; no source files were modified. New external claims are tagged with evidence level per Research Doctrine v1.1.*
