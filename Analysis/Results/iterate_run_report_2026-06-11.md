# Diabetes Research Hub — Iterate Run Report

**Date:** 2026-06-11 (Thursday)
**Mode:** Autonomous scheduled run

## State Load
- Loaded `agent_state.json` (version-tracked, 285 papers).
- **Paper vetting backlog is fully cleared:** 272 VETTED / 13 FLAGGED, 0 unvetted. The 13 flags are all legitimate off-topic exclusions (oncology, epilepsy, septic-shock endotoxin, Crohn's/MS genetics) correctly kept out of the primary diabetes corpus.
- No gap audits due today — all 15 gaps are next due late June / July 2026.

## Credibility Sweep — CLEAN
- No fabricated PMIDs (none above 42,000,000).
- No "zero SAEs" / "zero rejection" claims.
- Only "curative" matches are inside `verify_before_deploy.py`'s own flag-word detection list (expected, benign).

## Path Validation (5 paths; validated_paths 46 → 51)
| Path | Rating | Key external evidence |
|---|---|---|
| canagliflozin → inflammation | **VALIDATED** | CANTATA-SU: IL-6 −22%, CRP −4.4% vs glimepiride (T2D); SGLT2i meta-analysis (18 studies, n=5,311) IL-6 reduction; mechanistic IL-6 suppression via hexokinase II/autophagy (PMID 29551587) |
| metformin → nephropathy | **VALIDATED** | Cohort/meta: ↓creatinine doubling (HR~0.71), ↓ESKD (HR~0.55), slower eGFR decline; AMPK/anti-inflammatory mechanism. Observational, not RCT-grade (PMID 38986038) |
| calcineurin → islet_transplant | **VALIDATED** | Tacrolimus core to Edmonton protocol but directly β-cell toxic/diabetogenic → loss of insulin independence; drives CNI-free efforts (PMID 17176613; PMC2759396) |
| Treg_expansion → T1D | **PARTIALLY_VALIDATED** | Low-dose IL-2 robustly expands FOXP3+ Tregs & cuts IL-21+ T cells, but clinical C-peptide/β-cell preservation unproven (ITAD ph2; Nat Commun 2022) |
| rapamycin → inflammation | **PARTIALLY_VALIDATED** | mTORC1 inhibition blocks IL-2-driven T/B proliferation, ↓TNF/IL-6 but ↑IL-12/↓IL-10 — mixed, context-dependent (PMC2847476) |

## Rebuild
`run_quality_improvements.py` — **all 41 stages [OK]**, including PMID verification, citation validation, evidence network, 15 gap dashboards, and GitHub Pages rebuild.

## Carried Forward / Blocked
- **Git commit+push remains BLOCKED from the sandbox** (the `.git` directory lives in OneDrive and is not writable here). Requires the user to run `git add -A && git commit && git push` to publish today's changes.
- Remaining unvalidated paths for next run: oxidative_stress→{T2D, nephropathy, autoimmune, beta_cell}, rapamycin→nephropathy, tacrolimus→inflammation, insulin_glargine→T2D, hydroxychloroquine→inflammation, belatacept→T1D, teplizumab→autoimmune, NF-κB→inflammation.
- Upcoming dated items: Gap #11 audit (~06-27), Gap #1 audit (06-29); several trial-readout PubMed checks due July–Sept.

*Research synthesis only — not medical advice. All claims trace to cited external sources.*
