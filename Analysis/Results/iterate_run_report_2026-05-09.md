# Diabetes Research Hub — Iterate Run Report
**Date:** 2026-05-09 (Saturday)
**Operator:** automated agent (scheduled task `diabetes-research-iterate`)
**Last successful run:** 2026-05-08
**Run status:** completed; commit/push still blocked by stale `.git/*.lock` files (sandbox EPERM persists)

## Queue items resolved (4)

1. **P4 — extract_evidence: BANDIT trial primary publication (baricitinib phase 2 stage 3 T1D)** — RESOLVED. Primary publication identified: Waibel et al, NEJM 2023 Dec 7;389(23):2140-2150 (PMID 38055252). Protocol: Trials 2022 May 23;23(1):433 (PMID 35606820). NCT04774224.
2. **P4 — extract_evidence: "T1DAL" trial primary publication (golimumab anti-TNF stage 3 T1D)** — RESOLVED **with critical credibility correction** (see below). The trial is **T1GER**, not T1DAL. Primary: Quattrin et al, NEJM 2020;383:2007-2017 (PMID 33207093). 2-yr follow-up: Rigby et al, Diabetes Care 2023 Mar 1;46(3):561-569 (PMID 36576974). NCT02846545.
3. **P4 — audit_gap: re-grep all build_*.py for "rituximab" + "11/42"/"11 of 42"** — CLEAN. Five rituximab mentions across `build_data_dictionary.py` and `build_gap_deep_dives.py`; none contain "11/42" or "11 of 42" wording. All cite real PMIDs (19940299 Pescovitz NEJM 2009; 17965721 NHP transplant). No correction needed; the 2026-05-08 fix has not regressed.
4. **P4 — check_combination: SAFEGUARD NCT07187531 enrollment milestones** — UPDATED. SAFEGUARD = SAB-142 (human anti-thymocyte immunoglobulin) phase 2b in stage 3 new-onset T1D. First patient dosed 2025-12-18. Multi-center: US, Australia, New Zealand; European sites joining. Per SAB Biotherapeutics FY25 results announcement (March 2026), enrollment is on track to complete by year-end 2026; topline data expected H2 2027. Press-release / company-guidance tier only — must NOT be cited as VETTED.

## Critical credibility correction — T1DAL ≠ T1GER

The 2026-05-08 path notes (`golimumab_t1d_beta_cell.notes`) and the corresponding queue item both referenced "T1DAL" as the golimumab trial. **This is wrong.**

- **T1DAL** = Targeting effector memory T cells with **alefacept** in new-onset T1D. Different drug entirely (LFA-3/Fc fusion). Primary: Rigby MR et al, *J Clin Invest* 2015.
- **T1GER** = A Study of SIMPONI to ARrest beta-cell loss in **Type 1 diabetes** (NCT02846545). Drug: golimumab (anti-TNF/Simponi). Sponsor: Janssen.

The error appears to have entered the state when paraphrasing the BMC Med 2025 NMA on 2026-05-08; no build script or dashboard ever picked it up (verified by grep — only the run report and state metadata reference T1DAL, and now in corrected context). Today's update:

- `golimumab_t1d_beta_cell` path: `trial_name` set to "T1GER (A Study of SIMPONI to Arrest Beta-Cell Loss in Type 1 Diabetes)", `trial_id` "NCT02846545", PMIDs `[33207093, 36576974, 40598585]`, status upgraded **PARTIALLY_VALIDATED → VALIDATED**.
- `audit_notes` entry added documenting the T1DAL→T1GER correction and the trial-distinction it implies for future paraphrase work.

## Path status changes

| Path | Before | After | New PMIDs |
|---|---|---|---|
| `baricitinib_t1d_beta_cell` | PARTIALLY_VALIDATED (NMA-only) | **VALIDATED** | 38055252 (BANDIT primary, NEJM 2023), 35606820 (BANDIT protocol) |
| `golimumab_t1d_beta_cell` | PARTIALLY_VALIDATED (NMA-only, mis-named "T1DAL") | **VALIDATED** (correctly named T1GER) | 33207093 (T1GER primary, NEJM 2020), 36576974 (T1GER 2-yr FU, Diabetes Care 2023) |

## Key trial details ingested

### BANDIT — baricitinib phase 2 T1D (Australian)
- n=91 (60 baricitinib 4 mg/d vs 31 placebo), age 10–30 yrs, recent-onset T1D
- 48-week treatment, 2:1 randomization
- Primary: mixed-meal-stimulated mean C-peptide AUC at week 48 — **0.65 vs 0.43 nmol/L/min, P=0.001**
- HbA1c and exogenous insulin use also favored treatment
- Mechanism: JAK1/JAK2 inhibition → reduced IFN-γ signaling, suppressed Th1/Th17 cytokine output
- **Caveats:** single phase 2 RCT; long-term safety in T1D unestablished; durability after stopping unknown; needs replication

### T1GER — golimumab phase 2 T1D (Janssen-sponsored)
- n=84 (56 golimumab vs 28 placebo, 2:1), age 6–21 yrs, new-onset T1D within 100 d of randomization
- 52-week subcutaneous treatment
- Primary: 4-h C-peptide AUC at week 52 — **0.64 vs 0.43 pmol/mL, mean diff 0.21 (P<0.001)**
- 2-year follow-up: off-therapy benefits persisted; subpopulation showed continued metabolic improvement (PMID 36576974)
- **Caveats:** phase 2; not powered for long-term safety; no phase 3 confirmation; NMA reported substantial heterogeneity across 60 trials/42 interventions

### SAFEGUARD (SAB-142) — anti-thymocyte immunoglobulin phase 2b
- NCT07187531; first patient dosed 2025-12-18
- Stage 3 new-onset T1D
- Sponsor SAB Biotherapeutics (FY25 announcement, March 2026): enrollment on track for year-end 2026; topline H2 2027
- **Tier:** press-release / company guidance only — phase 1 healthy-volunteer data still only at EASD 2025 abstract level; not VETTED

## Pipeline status

- `run_quality_improvements.py`: **41/41 [OK]** (after fixing one regression — see below)
- Credibility sweep: clean (no fabricated PMIDs >42M; no unflagged "zero SAEs"/"curative"/"breakthrough" claims in scripts; only legitimate guard-list mention in `verify_before_deploy.py`)

### Pipeline regression fixed
`Analysis/Scripts/validate_citations.py` had a duplicated/corrupted tail block (truncated `datetime.now()` rendered as `ime.now()` after the proper `sys.exit(main())` at line 430), causing `IndentationError: unexpected indent`. Corrected by truncating the file at the legitimate `sys.exit(main())` line (430 → 430 lines total). Backup retained at `Analysis/Scripts/validate_citations.py.bak_2026-05-09`. Script now produces:
- 248 papers in evidence network, 162 citation links, 30 topic clusters
- Validation: CONFIRMED/PLAUSIBLE/WEAK/MISMATCH/NO_DATA distribution generated
- 8 MISMATCH PMIDs flagged (off-topic content vs claim — pre-existing items, not new failures)

## Outstanding blockers

- **`.git/HEAD.lock`, `.git/index.lock`, `.git/objects/maintenance.lock`** (0-byte, dated 2026-05-05) — `os.remove()` and `rm -f` both return EPERM on the OneDrive mount. Same root cause as 2026-05-08. Commits/pushes pending since 2026-05-05.
  - **User action required:** from PowerShell on host:
    ```powershell
    cd $HOME\OneDrive\Diabetes_Research
    Remove-Item -Force .git\HEAD.lock, .git\index.lock, .git\objects\maintenance.lock
    git add -A
    git commit -m "Catch-up commit (2026-05-05 through 2026-05-09 iterations)"
    git push
    ```

## New queue items added (3)

- P5: search_pubmed — SAB-142 phase 1 healthy-volunteer peer-reviewed publication (still only EASD 2025 abstract; recheck)
- P5: check_combination — SAFEGUARD NCT07187531 next quarterly enrollment milestone (next check 2026-08-09)
- P5: search_pubmed — BANDIT 2-year off-therapy follow-up (after 48-week primary endpoint)

## Files touched

- `Analysis/Results/agent_state.json` (validated_paths: 2 upgraded; audit_notes: +3; queue: 4 resolved + 3 added; run_history: +1)
- `Analysis/Scripts/validate_citations.py` (truncated at line 430 to remove corrupted duplicate tail)
- `Analysis/Scripts/validate_citations.py.bak_2026-05-09` (new, backup of broken version)
- `Analysis/Results/citation_validation.json` (regenerated; was last rebuilt 2026-05-08)
- `Analysis/Results/evidence_network.json` (regenerated)
- All 34 dashboards re-post-processed via `run_quality_improvements.py`
- `Analysis/Results/iterate_run_report_2026-05-09.md` (this file)

## Sources cited (peer-reviewed PMIDs and clinical-trial registry IDs only)

- BANDIT primary (Waibel et al, NEJM 2023): PMID **38055252**
- BANDIT protocol (Trials 2022): PMID **35606820**
- BANDIT registry: NCT04774224
- T1GER primary (Quattrin et al, NEJM 2020): PMID **33207093**
- T1GER 2-yr follow-up (Rigby et al, Diabetes Care 2023): PMID **36576974**
- T1GER registry: NCT02846545
- BMC Med 2025 NMA (Beese SE et al): PMID **40598585**
- SAFEGUARD registry: NCT07187531 (no peer-reviewed publication yet)
- Pescovitz rituximab T1D NEJM 2009: PMID 19940299 (cited only to confirm clean re-grep)
