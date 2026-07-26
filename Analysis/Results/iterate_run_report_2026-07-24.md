# Iterate Run Report — 2026-07-24 (Friday)

**Agent:** Diabetes Research Hub automated iteration
**Mode:** Autonomous scheduled run (user not present)

## Work Queue Items Processed

1. **Git blocker (P1) — reassessed, STILL BLOCKED.** `.git/index.lock` (0-byte, dated 2026-07-20) remains unremovable from the sandbox: `rm` returns "Operation not permitted" on the OneDrive mount. Commit/push cannot proceed from the agent. **User action required:** delete `.git/index.lock` locally, then `git add -A && git commit && git push`.

2. **validate_path: metformin → cardiovascular — DONE.** Rating **PARTIALLY_VALIDATED maintained** (honest). No new placebo-controlled hard-MACE RCT overturns Griffin 2017 (PMID 28776086). 2020 NMCD updated MA shows a MACE association but pools active comparators (not clean placebo). Added supporting **2023 umbrella review** (J Diabetes Metab Disord, DOI 10.1007/s40200-023-01309-y). 2025 literature is atrial-fibrillation sub-outcome + observational; does not establish hard-MACE benefit. Recorded as `refresh_2026-07-24`.

3. **Recheck 2 UNVETTED_NO_PMID watch items — DONE.** Both reconfirmed DOI-verified real but still NOT PubMed-indexed:
   - IJMS ferroptosis / DKD (DOI 10.3390/ijms27104257) — MDPI, no retrievable PMID.
   - Zhao et al., NLRP3 hub genes in diabetic nephropathy (DOI 10.1002/iid3.70424) — Wiley *Immunity, Inflammation and Disease* 2026, no PMID.
   Both remain `pmid=PENDING` (NOT fabricated). Next recheck 2026-08-07.

4. **Credibility sweep (every run) — CLEAN.** No fabricated PMIDs (nothing ≥42000000), no "zero SAEs/rejection" claims. The only "curative" matches are inside the guardrail detector regex in `verify_before_deploy.py`, not actual claims.

5. **Pipeline rebuild — local stages [OK].** All non-network stages rebuilt successfully with fresh dashboards (Clinical Trial, Research, Gaps, Corpus, Extracted Evidence, Research Paths, Statistics, Islet Repurposing v2, website, post-processing). **Network-dependent stages (pmidverify, pmidtracker, citations, trialequity) hang in the sandbox** — eutils and clinicaltrials.gov are unreachable here. These require the local weekly run (queue item P7).

## Corpus Status
- Papers: **285 total — 272 VETTED, 13 FLAGGED (100% triaged).** Vetting backlog cleared.
- Paths: 57 tracked, 56 validated entries.
- Gaps: 15 tracked; next monthly audits cluster in August (Gaps #10/#8/#9/#15 due ~2026-08-05).

## Blockers for User
1. **Clear `.git/index.lock` and commit/push manually** — the agent has uncommitted changes (updated `agent_state.json`, rebuilt dashboards) it cannot push.
2. **Run the full pipeline locally** (where network is available) to complete PMID/trial verification stages.

## Notes
- No fabricated data introduced. All claims trace to sources.
- State saved; run recorded in history (run #100).
