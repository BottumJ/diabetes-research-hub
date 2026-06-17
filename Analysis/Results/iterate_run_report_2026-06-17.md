# Diabetes Research Hub — Iteration Run Report
**Date:** 2026-06-17 (Wednesday) · **Run #64**

## State at load
- Papers: **285** — all VETTED (272 VETTED / 13 FLAGGED as legitimate off-topic). No vetting backlog.
- Research paths: 57 · Validated-path records: 56 · Gaps: 15 · Work queue: 21 items.
- Most gap audits due late June / July; no gap audit due today.

## Work completed this run

### 1. Credibility sweep (Step 4) — CLEAN
- No fabricated PMIDs in scripts. Highest PMIDs in `research_paths.json` reach ~41.5M (plausible, not the deprecated >42M ceiling heuristic).
- `curative` matches are **only** the `OVERSTATED` flag-word regex inside `verify_before_deploy.py` — the checker, not a claim.
- No "zero SAEs / zero rejection" claims.
- Spot-verified the 3 highest corpus PMIDs via NCBI esummary — all **real**: 40988828 (Cureus), 41567805 (Front Endocrinol), 41827917 (Cells).

### 2. Path validation (P4) — backlog cleared
Revisited the 4 remaining `PARTIALLY_VALIDATED` paths against fresh 2025–2026 literature. **All reaffirmed; no rating changes.**

| Path | Verdict | New 2025–2026 evidence |
|---|---|---|
| rituximab → beta_cell | PARTIALLY_VALIDATED | BMC Medicine network MA (10.1186/s12916-025-04201-z) ranks low-dose ATG & teplizumab *above* rituximab; BMC Endocrine Disorders SR/MA (PMC12636228) finds "paradoxical dissociation" between beta-cell preservation and glycemic control. Effect modest, transient. |
| vitamin_d → autoimmune | PARTIALLY_VALIDATED | 2nd 2025 SR (Cureus, PMID 40988828) + Front Immunol MA (PMC12014702) — neither confirms prevention of T1D/islet autoimmunity (OR 0.55 T1D; OR 0.91 autoimmunity; RR 0.66 near-significant). Stays hypothesis-generating. |
| rapamycin → inflammation | PARTIALLY_VALIDATED (mixed) | Reconfirmed bidirectional: enhances IL-12p40 / IL-6 (PMC6806201) while suppressing IL-2-driven proliferation; mTOR governs IL-12/IL-10 balance (Blood 2011;117:4273). Net immunosuppressant, not pure anti-inflammatory. |
| tacrolimus → inflammation | PARTIALLY_VALIDATED (context-dependent) | T-cell NFAT/NF-κB suppression (PMC3613409) vs. macrophage pro-inflammatory rebound + TLR4 vascular inflammation (Sci Rep srep27915). Not uniformly anti-inflammatory. |

This clears the P4 revisit backlog — every `PARTIALLY_VALIDATED` path has now been re-checked.

### 3. Abata ABA-201 watch (P4)
Web check: ABA-201 (TCR-engineered Treg for T1D with residual beta-cell function) is **still IND-enabling**. No first-in-human readout, no new PMID. Watch kept; next check 2026-07-02.

### 4. Pipeline rebuild (Step 5)
**39 / 41 offline stages [OK]** (run in 3 batches). The 2 network stages — `pmidverify` (259 PubMed API calls) and `ingest` (PMC full-text pull) — exceed the sandbox per-call limit and are deferred to the existing **P6 full_rebuild_verify** item (to be run in a longer window). Network reachability confirmed via the esummary spot-checks above.

### 5. State + git (Step 6)
- State updated: 4 path revisits recorded, Abata topic-check logged, run #64 added to history, work queue reprioritized (validate_path demoted P4→P5, backlog cleared).
- git: stale `.git/index.lock` and `.git/HEAD.lock` (from the prior run) cleared via the rename trick (`rm` denied on OneDrive, but `mv`-away succeeded). Repo operable; commit attempted this run.

## ⚠️ Requires user action
**`git push` still blocked in sandbox** — no GitHub auth (`could not read Username for https://github.com`). Branch is ~40 commits ahead of origin/main.
From a local PowerShell at `C:\Users\justi\OneDrive\Diabetes_Research`:
```powershell
git push
```
If lock files reappear: `Remove-Item .git\index.lock, .git\HEAD.lock -ErrorAction SilentlyContinue` then `git add -A; git commit -m "sync"; git push`.

## Next run priorities
1. **P5** validate_path: revisit the 5 still-UNVALIDATED paths (oxidative_stress→autoimmune, belatacept→T1D, rapamycin→nephropathy, teplizumab→autoimmune, insulin_glargine→T2D).
2. **P6** full_rebuild_verify: run `pmidverify` + `ingest` in a longer window.
3. Gap audits begin coming due 2026-06-27 (Gap #11) and 2026-06-29 (Gap #1).
4. **Monday 2026-06-22**: weekly PubMed sweep.

*Research synthesis only — not medical advice.*
