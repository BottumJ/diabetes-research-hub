# Diabetes Research Hub — Iteration Run Report
**Date:** 2026-04-25 (Saturday) · Run #14

## Summary
Vetted 12 papers, validated a new research-path axis (BHB → NLRP3 inflammasome inhibition), searched for the Abata ABA-201 CAR-Treg readout, ran the credibility sweep + 41-step pipeline rebuild, and updated agent state.

## Work queue items processed
| Priority | Item | Outcome |
|---|---|---|
| 1 | Vet 10–15 papers from batch | Done — 12 papers vetted, all VETTED |
| 2 | Validate BHB → NLRP3 inhibition path | Done — VALIDATED (HIGH preclinical / MEDIUM clinical) |
| 2 | Search ABA-201 CAR-Treg T1D | Done — no new PMID readout; watch logged for 2026-07-25 |
| Std | Credibility sweep + rebuild | Done — clean; all 41 steps [OK] |

## Paper vetting (12 papers)
All in-library entries verified against `paper_library/index.json`. Abstracts scanned for red flags (claims-without-context, abstract↔result mismatch, suspicious precision). All 12 marked **VETTED**.

| PMID | Journal · Year | Title (abridged) | Note |
|---|---|---|---|
| 30303773 | Physiology · 2018 | The Difference δ-Cells Make in Glucose Control | Review; supports glucose set-point/GCK context |
| 30415610 | NEJM · 2019 | Low-Dose Methotrexate for Atherosclerotic Events (CIRT) | Real RCT; tangential to T2D but MTX = repurposing candidate |
| 30586620 | BBMT · 2019 | Cytokine Release Syndrome with CAR-T Therapy | Tangential oncology; informs CAR-Treg safety profile |
| 30657336 | Diab Tech Ther · 2019 | T1D Exchange 2016–2018 | Landmark US registry epi snapshot |
| 30899369 | Am J Transl Res · 2019 | Metformin → M2 polarization, AMPK/mTOR/NLRP3 | Preclinical; relevant to NLRP3 axis |
| 30949058 | Front Physiol · 2019 | Central Role of Glucokinase (50-yr review) | Supports GKA repurposing context |
| 31036962 | Nat Rev Immunol · 2019 | NLRP3 Inflammasome (cornerstone review) | Already used as path anchor |
| 31157579 | JCO · 2019 | CAR-T Cost-Effectiveness in DLBCL | Tangential oncology; supports CAR-Treg cost-barrier narrative |
| 31173679 | NEJM · 2019 | Vit D Supplementation, T2D Prevention (D2d) | Pivotal trial |
| 31175156 | J Biol Chem · 2019 | Thirty Sweet Years of GLUT4 | Historical/mechanistic review |
| 31177185 | Diabetes Care · 2019 | International Consensus on Time in Range (ATTD) | Landmark CGM target consensus |
| 31180194 | NEJM · 2019 | Teplizumab in At-Risk Relatives (TN-10, Herold) | Pivotal T1D-delay trial |

Two oncology papers (30586620, 31157579) noted as tangential but kept — both directly inform the CAR-Treg safety/access narratives in the hub.

## New validated research path: BHB → NLRP3 inflammasome inhibition

**Status:** VALIDATED · Preclinical confidence HIGH · Clinical confidence MEDIUM

**Mechanism:** β-hydroxybutyrate inhibits NLRP3 inflammasome assembly by blocking K⁺ efflux and ASC oligomerization — independent of UCP2/Sirt2/Gpr109a/HDAC activity. SGLT2 inhibitors raise serum BHB, providing a candidate mechanistic link between SGLT2i and the NLRP3 suppression observed in DKD/CV outcomes.

**Cornerstone PMIDs (external, confirming):**
- **25686106** — Youm et al. *Nat Med* 2015. Foundational: BHB blocks NLRP3-mediated inflammatory disease in human monocytes + mouse models (MWS, FCAS, urate crystal).
- **28794421** — Yamanashi et al. *Sci Rep* 2017. BHB as endogenic NLRP3 inhibitor; anti-inflammatory in stress-induced behavior model.
- **32358544** — Kim et al. *Nat Commun* 2020. 30-day RCT in T2D+CVD: SGLT2i vs sulfonylurea — SGLT2i ↑serum BHB, ↓insulin, ↓NLRP3-IL-1β in human macrophages independent of glucose lowering.
- **34918381** — already-in-library Front Pharmacol/FASEB J 2022. Itaconate alternate axis.
- **39412512** — already-in-library Braz J Nephrol 2024 review.

**Caveats explicitly recorded:**
1. Most evidence is in vitro / mouse. Kim 2020 is the strongest in-human study and is a *biomarker-PD* readout, not a clinical-outcome RCT.
2. SGLT2i-induced BHB rise is modest (~0.1–0.5 mmol/L). Whether this magnitude is sufficient to drive clinically meaningful NLRP3 suppression in humans is unproven.
3. 2025 BMC Nephrol review and ADA 2025 abstract 389-P (BHB-mitigates-DKD) are without confirmed PMIDs in our library — weighted cautiously.
4. **Mechanistic plurality:** SGLT2i → NLRP3 also plausibly proceeds via itaconate, RIP1-RIP3-MLKL, and TXNIP-NLRP3. BHB is one of several proposed axes, not the sole mechanism.

**Recommendation:** Wire BHB→NLRP3 as an explicit named path in `research_paths.json` next pipeline iteration, and update SGLT2i→DKD storyline to reflect mechanistic plurality rather than a single linear story. Added as priority-2 item in queue.

## ABA-201 (Abata Therapeutics) — watch
Searched: company comms, 2025 reviews (Eur J Immunol Passerini 2025; Frontiers Endo 2025; PMC12661798 CAR-T-in-T1D 2025). **No first-in-human readout published.** Per Abata announcements + 2024-08 BMS strategic investment, IND-enabling/Phase 1 initiation flagged for 2025; no patient outcome data yet. Re-check scheduled for 2026-07-25 — watch ASGCT 2026 + ADA 2026 abstracts.

## Credibility sweep
- Fabricated PMIDs (>42M): **none**
- "zero SAEs / zero rejection" patterns: **none**
- "achieves / curative" scan: 7 hits, all benign on review (molecular-design language for TTP399, methodological "achieves 80% cost-effectiveness", microbiome-model AUC, public 2025 milestones in dashboard timeline, regex patterns inside the linter itself).

## Pipeline rebuild
`run_quality_improvements.py`: **all 41 steps [OK]**. No regressions.

## Running totals
- Papers: **VETTED 164** · FLAGGED 9 · UNVETTED 94
- Validated paths log: +1 (BHB→NLRP3)
- Topic checks: +1 (Abata ABA-201)
- Run history: 14 entries

## Next run will pick up
1. **Vet next 10 papers** (priority 1) — top of unvetted PMID list
2. **Search PubMed: DIAMYD/DIAGNODE Extension** (priority 2)
3. **Validate path: TXNIP → NLRP3 → β-cell loss / DKD** (priority 2 — third axis emerging from today's work)
4. **Wire BHB→NLRP3 into research_paths.json** (priority 2)
5. Rolling gap audits (Gap 14 monthly BRONZE; Gap 1 quarterly SILVER; Gap 9 exploratory)

---
*Automated agent run · state persisted to `Analysis/Results/agent_state.json`*
