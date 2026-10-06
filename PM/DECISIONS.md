# Diabetes Research Hub: Decisions for Justin

These are the decisions that belong to Justin: gap tier rulings, withdrawals, publishing path, scope. The PM mirrors
rulings and never makes them. Rulings are recorded in `gap_owner_rulings.json` / `gap_tiers.json` by the main
session. Days waiting are as of 2026-10-05.

## Open (oldest first)

| # | Decision | First raised | Brief / source | Recommendation | Days waiting |
|---|---|---|---|---|---|
| D-01 | Ratify the de facto answers to charter §7: (1) first meta-analysis = incretin HbA1c; (2) claims and predictions live in JSON in `Analysis/Results/`; (3) Phase 1 verification = independent second AI extraction + span check; (4) scoring cadence = monitor-triggered | 2026-06-23 | `SCIENCE_ARM_BUILD_CHARTER.md` §7 | Ratify 1-3 as built. Answer 4 explicitly. For (2), retire the tracker xlsx (I-11) | 104 |
| D-02 | GOLD requires 3 independent *datasets*, not 3 documents (commentary on a trial is not confirmation of it) | 2026-08-31 | `DECISION_BRIEF_2026-08-31.md`; doctrine Lesson 7 "open contradiction, queued 2026-08-31" | Adopt. The brief shows it settles several standing P1 items; cost: some GOLD claims demote | 35 |
| D-03 | Gap #8: state on the card that its axes are joined by inference, or find an intersection paper | 2026-09-07 | `DECISION_BRIEF_2026-09-07.md` §2 Q4 | No ruling recorded. The gate no longer flags #8 (`gap_subject_coverage_audit.json` 2026-10-01). Ratify the current card text, then re-derive under Lesson 9 (I-26) | 28 |
| D-04 | Gaps #14 and #15 BRONZE → EXPLORATORY | 2026-09-07 | Same brief, Q3; applied by the agent 2026-09-27 | Ratify. Already applied in `gap_tiers.json`, but no entry in `gap_owner_rulings.json` | 28 |
| D-05 | Edit the cloud agent's task file: Step 4 "PMIDs above 42000000 (fabricated)" is obsolete (the live ceiling is resolved by `audit_impossible_pmids.py`); Step 1's vet loop makes busy-work | 2026-09-10 | work_queue P0 (2026-09-10); `ACTION_REQUIRED_2026-09-21.md` | Make both edits. Only Justin can edit the task. Current task text not verified by the PM | 25 |
| D-06 | How unattended pushes happen: a credential for the scheduled task (PAT / gh) vs. manual pushes from Windows | 2026-09-16 | work_queue P0 push item; `publish_reachability_audit.json` action line; open_findings N-07 | Keep pushes manual, behind a full gate run (I-10), until the stale-index hazard and the JS-literal defect are fixed. Revisit after. [Likely the safer choice for a public repo] | 19 |
| D-07 | **Gap #2 tier**: A BRONZE "Beta Cell Therapies" / B EXPLORATORY / C retire "Health Equity in Diabetes" / D leave GOLD | Concern 2026-08-16 (agent); "premise falsified twice" 2026-09-04; brief 2026-10-01 | `DECISION_BRIEF_2026-10-01_Gap2.md` | **A** (the brief's recommendation). D is not supportable under either reading. After any ruling, no gap is GOLD | 4 on the brief (50 since first raised) |

## Ruled (mirrored from `gap_owner_rulings.json` and the run reports)

| # | Decision | Raised | Ruled | Answer |
|---|---|---|---|---|
| R-01 | Gap #1 tier | 2026-09-07 (brief Q1) | 2026-09-30 | EXPLORATORY (was SILVER): no stored paper concerns gene therapy |
| R-02 | Gap #13 tier | 2026-09-07 (brief Q1) | 2026-09-30 | EXPLORATORY (was BRONZE): evidence was berberine trials in T2D |
| R-03 | Gap #3 tier and claim | 2026-09-05 (brief §4) | 2026-09-30 | SILVER (was GOLD); claim restated as "rarely measured, not tracked"; clamp data (PMIDs 24085506, 24691031) contradicted the original |
| R-04 | Gaps #4 and #7: does drug-level evidence count? | 2026-09-07 (brief Q2) | 2026-09-30 | Yes, labelled as the hub's inference; reader notes on the pages |
| R-05 | Gap #11 tier | 2026-09-05 (brief §5) | 2026-09-30 | SILVER under Lesson 9 (absence: PubMed + CITR report/bibliography; premise: CITR Exhibit 2-1 vs PMID 30181166) |
| R-06 | Absence claims tiered by null searches (Lesson 9, BRONZE → SILVER rule) | 2026-09-30 | 2026-09-30 | Adopted (RESEARCH_DOCTRINE.md v1.2) |
| R-07 | Bayesian path ranking | open_findings N-01 | 2026-09-30 | Withdrawn (decision A); replaced by a status table, explicitly not a ranking |
