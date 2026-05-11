# Diabetes Research Hub — Scheduled Iteration Report
**Date:** 2026-05-05
**Run type:** Automated (state-aware)
**Pipeline status:** 41/41 [OK]

## Work queue items processed

### 1. Vet last 9 UNVETTED papers — DONE
All 9 PMIDs verified via NCBI esummary; no red flags found. Marked VETTED with notes on preclinical scope where relevant.

| PMID | Source | Disposition |
|---|---|---|
| 41172147 | Pancreas 2026 | VETTED — TPIAT GI outcomes, clinical |
| 42021540 | J Biochem Mol Toxicol 2026 | VETTED — preclinical (rat) |
| 42045904 | J Nanobiotechnology 2026 | VETTED — preclinical (microneedle) |
| 42045987 | Stem Cell Res Ther 2026 | VETTED — review (MSC for DFU) |
| 42050925 | Immunopharmacol Immunotoxicol 2026 | VETTED — preclinical (ezetimibe NO pathway) |
| 42057440 | Ren Fail 2026 | VETTED — preclinical (β-thujaplicin DKD) |
| 42065920 | Aging Dis 2026 | VETTED — review (senescence + diabetic atherosclerosis) |
| 42066937 | Arch Biochem Biophys 2026 | VETTED — preclinical (SGLT2i + exercise pyroptosis) |
| 42070055 | BMC Pharmacol Toxicol 2026 | VETTED — preclinical (purslane + metformin) |

UNVETTED queue: **9 → 0**.

### 2. Validate research path: dapagliflozin → nephropathy — VALIDATED
- DAPA-CKD trial (NEJM 2020, PMID 32970396, n=4,304): primary composite HR 0.61 (95% CI 0.51–0.72)
- 9-RCT meta-analysis (PMC11370938, ~30k participants): OR 0.61 for kidney composite, OR 0.69 mortality, UACR −23.99%
- Effect present in patients with and without T2D
- Both alias keys updated; added to validated_paths registry

### 3. Audit Gap #15 (SGLT2i × personalized nutrition) — BRONZE retained
- Found adjacent precision-medicine literature (Lancet Reg Health Europe 2025 selection model; Diabetologia 2026 SGLT2i precision medicine)
- ADA 2026 Standards of Care endorse personalized SGLT2i deployment but cite no nutrition RCT
- Direct intersection trial still absent
- promotion_candidate retained = TRUE; next audit due ~2026-06-05

### 4. Credibility sweep — 1 issue found and fixed
- **Bug:** PMID 37133585 (a 2023 NEJM colorectal-cancer trial) was wrongly cited for teplizumab in two places.
- **Fix:** Replaced with PMID 31180194 (Herold KC et al., NEJM 2019, TN-10 trial) in:
  - `Analysis/Scripts/add_citations.py` line 63
  - `Research_Findings_Summary.md` line 38
- **Followup queued:** the same off-topic PMID is still a node in `evidence_network.json` — added new queue item to drop FLAGGED PMIDs from the published evidence network at extraction time.

### 5. Pipeline rebuild — 41/41 [OK]
All build scripts executed successfully after fixes.

### 6. Doctrine note added
SKILL.md credibility heuristic "PMIDs > 42,000,000 = fabricated" is stale: NCBI is now legitimately assigning IDs in the 42M+ range. Replaced internal practice with NCBI esummary verification. Added to `state['doctrine_notes']['pmid_range_2026']` and queued doctrine_update item to revise SKILL.md text.

## Corpus state at end of run
- Papers: **267 VETTED / 13 FLAGGED / 0 UNVETTED** (total 280)
- Paths: **27 VALIDATED**, 11 PARTIALLY_VALIDATED, 42 UNVALIDATED, 1 CONTRADICTED (total 82)
- Gaps: 15 tracked; 6 GOLD audits now overdue (queued)

## Git
- Local commit `226ec8e` recorded with 34 files changed.
- Push to origin failed (no GitHub credentials in sandbox); branch is 4 commits ahead. Next interactive push will sync.
- Cleared stale `.git/index.lock` and `.git/HEAD.lock` (renamed to `.stale`); residual lock-file warnings remain but no longer block commits.

## Next-run priorities (queue head)
1. Tighten extraction filter to exclude FLAGGED PMIDs from evidence network (#37133585, #35437333)
2. Extract C-peptide-preserving intervention data from PMID 40598585 NMA
3. Audit overdue GOLD gaps #2, #3, #6 (last audited 2026-03-20)
4. Validate `verapamil → T1D` and `dapagliflozin → T2D` paths
5. Update SKILL.md credibility-sweep doctrine
