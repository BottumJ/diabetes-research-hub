# Daily Iteration Run Report — 2026-05-14 (Thursday)

## Summary
Completed 2 work-queue items, 4 path validations, 1 extraction-artifact identification, full pipeline rebuild. Credibility sweep clean.

## Work-queue items resolved
1. **Item 14 (validate_path)** — Remaining 4 dpc=1 UNVALIDATED paths
2. **Item 20 (validate_path, priority 3)** — Atorvastatin->T2D direction audit

## Path validations
| Path | Status | Corpus dpc | Corpus PMID(s) | External evidence summary |
|---|---|---|---|---|
| metformin -> inflammation | VALIDATED | 1 | 35466661 | AMPK/NLRP3 suppression; clinical 2-mo metformin reversed caspase-1 + IL-1β/IL-18 in T2D myeloid cells; suppresses IL-6, TNF-α |
| pioglitazone -> inflammation | VALIDATED | 1 | 35466661 | PPARγ → ↓hs-CRP, IL-6, TNF-α independent of glucose lowering; replicated in multiple T2D RCTs |
| oxidative_stress -> beta_cell | VALIDATED | 1 | 29885104 | β-cells express ~5% of liver CAT/Gpx; canonical ROS pathogenesis; therapeutic translation MIXED (bardoxolone/sulforaphane some signal; vitamins limited) |
| oxidative_stress -> T1D | VALIDATED | 1 | 26897744 | Elevated reactive O metabolites in T1D youth; antioxidant-enzyme spike precedes islet autoimmunity; macrophage/DC ROS → APC activation → T-cell autoimmunity |
| atorvastatin -> T2D | EXTRACTION_ARTIFACT | 1 | 35466661 | PMID 35466661 is the HYQ-Real-World hydroxychloroquine T2D dyslipidemia study; atorvastatin appears only as a comparator drug. External evidence shows statins INCREASE T2D risk (Sattar 19794004 +9%; Navarese 27277934 +15% atorva-specific). Path direction wrong |

**Note**: All 4 newly-validated paths have weak corpus support (single PMID, dpc=1). External web evidence carries the validation. The mechanisms themselves are well-established in the literature; this is a corpus-coverage limitation, not a validity concern about the underlying biology.

## Extraction-quality finding
PMID 35466661 alone seeded THREE spurious dpc=1 research paths (`atorvastatin->T2D`, `metformin->inflammation`, `pioglitazone->inflammation`) because the extractor pattern-matches drug names against condition keywords without mechanistic context. Of these three, two happen to be externally TRUE (metformin and pioglitazone really do reduce inflammation), but the atorvastatin one is FALSE in direction. Filter would prevent both false positives and false negatives.

**Queued work item** (priority 3): `fix_extraction_filter` — drop dpc=1 paths whose only key_claims are short non-mechanistic dose fragments (e.g., "400 mg", "1000 mg/day").

## Credibility sweep
- No PMIDs >42000000 in scripts ✓
- No "zero SAEs" / "zero rejection" ✓
- "achieves" hits reviewed: all are model-performance or design-property statements (TTP399 tissue selectivity, LADA model cost-effectiveness, microbiome ML AUC) — not preclinical-efficacy overclaims ✓
- "curative" hit is only in `verify_before_deploy.py` as a guardrail regex ✓

## Pipeline
`run_quality_improvements.py` — all 41 steps `[OK]`.

## Git
- Cleared stale lock files (`.git/index.lock`, `.git/HEAD.lock`, `.git/objects/maintenance.lock`) via rename workaround
- Commit `f78f9d7` recorded today's changes (33 files, +12169/-11194)
- **6 unpushed commits remain** (`f78f9d7`, `267cbf5`, `226ec8e`, `e6e7bb2`, `bcca463`, `be682ef`, going back to 2026-04-21). Sandbox has no git credentials; user push required from local machine.

## Queue state for next run
- 19 items (priority-ordered)
- Top of queue: stale git-lock blocker note (now resolved, will reprioritize), then June audit_gap items (#10, #8, #2, #3, #6, etc.) coming due ~2026-06-02 onward.
- New item added: `fix_extraction_filter` (priority 3) to prevent recurrence of the atorvastatin-style artifact.

## State
- Papers tracked: 280 (267 VETTED / 13 FLAGGED / 0 UNVETTED — corpus fully vetted)
- Paths tracked: 47 in research_paths.json; validated_paths state now has 23 entries
- Audit notes: 14 entries
- Run history: 33 entries (last 2 weeks of daily runs)
