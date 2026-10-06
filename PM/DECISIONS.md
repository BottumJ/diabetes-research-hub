# Diabetes Research Hub: Decisions for Justin

These are the decisions that belong to Justin: what the project values, how strict it is, what it publishes, its scope,
and gap tier rulings. The PM mirrors rulings and never makes them. Rulings are recorded in `gap_owner_rulings.json` /
`gap_tiers.json` by the main session. Days waiting are as of 2026-10-06.

**Standing preference (owner, 2026-10-06; memory `diabetes-owner-not-clinician`; charter §7 note).** Justin is not a
clinician. Methods and feasibility calls (what to pool, what counts as a source, how to verify, how a gate works) are
made by the analyst, stated with reasoning and confidence, and recorded in the doctrine or charter. Only value and
scope decisions come to Justin, in plain language, recommendation first. Open items that were really methods calls
have been handed back to the analyst below (marked "Reassigned").

## Open (oldest first)

| # | Decision (plain language) | First raised | Brief / source | Recommendation | Days waiting |
|---|---|---|---|---|---|
| D-02 | **How strict is GOLD?** Should GOLD mean three separate studies (separate data) agree, or is three papers enough even if two of them only discuss the first study? | 2026-08-31 | `DECISION_BRIEF_2026-08-31.md`; doctrine Lesson 7 "open contradiction" | Three separate studies. Since 2026-10-06 no gap is GOLD, so this now mainly affects GOLD entries in `Research_Findings_Summary.md`; some would drop to SILVER | 36 |
| D-04 | **Gaps #14 and #15 BRONZE → EXPLORATORY**: confirm the cloud agent's demotion (applied 2026-09-27; no entry in `gap_owner_rulings.json`) | 2026-09-07 | Brief 2026-09-07 Q3 | Confirm. Better: settle it through D-08, so the claim-by-claim rollout handles #14/#15 under one rule | 29 |
| D-05 | **Edit the cloud agent's task file** (only Justin can): drop Step 4's obsolete "PMIDs above 42000000 are fabricated" rule (real PMIDs are now above 42.8 million, e.g. 42822480, verified 2026-10-06); trim Step 1's busy-work vet loop; tell it the Excel tracker is retired (charter §7 Q2) so it stops escalating it (6 runs running) | 2026-09-10 | work_queue P0 2026-09-10; `ACTION_REQUIRED_2026-09-21.md` | Make the edits. An action, not a judgement; the PM has not seen the current task text | 26 |
| D-06 | **How pushes happen**: keep pushing by hand from Windows (current practice; e0c6cb7 pushed 2026-10-06), or give the scheduled task a GitHub credential | 2026-09-16 | `publish_reachability_audit.json` action line; open_findings N-07 | Keep manual, with a full gate run first (one ran 2026-10-06 12:37). A credential on an unattended task in a public repo is the riskier choice [Likely] | 20 |
| D-08 | **New. Claim-by-claim rollout to the other 14 gaps**: when re-rating a gap claim by claim moves its headline tier (as Gap #2 went GOLD → BRONZE), should the analyst apply it under the 2026-10-06 rule and report it, or bring each one to you first? | 2026-10-06 | INTAKE row 5; `gap_tiers.json` `claim_rule`; doctrine 1.3 | Apply under the rule and report each change in the run report with its claim table; you can reverse any of them. Otherwise tier rulings stall (D-04 has waited 29 days) | 0 |

## Reassigned to the analyst (methods calls, per the standing preference)

| # | Item | First raised | Reassigned | Where it goes now |
|---|---|---|---|---|
| D-03 | Gap #8: say on the card that its two axes are linked by the hub's inference, or find a paper on both | 2026-09-07 | 2026-10-06 | IDEAS I-35 (claim-by-claim rollout, Gap #8 in the first batch). A claim table states which claims are inference |

## Ruled (mirrored from `gap_owner_rulings.json`, the charter and the run reports)

| # | Decision | Raised | Ruled | Answer |
|---|---|---|---|---|
| R-01 | Gap #1 tier | 2026-09-07 (brief Q1) | 2026-09-30 | EXPLORATORY (was SILVER): no stored paper concerns gene therapy |
| R-02 | Gap #13 tier | 2026-09-07 (brief Q1) | 2026-09-30 | EXPLORATORY (was BRONZE): evidence was berberine trials in T2D |
| R-03 | Gap #3 tier and claim | 2026-09-05 (brief §4) | 2026-09-30 | SILVER (was GOLD); restated "rarely measured, not tracked"; clamp data (PMIDs 24085506, 24691031) contradicted the original |
| R-04 | Gaps #4 and #7: does drug-level evidence count? | 2026-09-07 (brief Q2) | 2026-09-30 | Yes, labelled as the hub's inference; reader notes on the pages |
| R-05 | Gap #11 tier | 2026-09-05 (brief §5) | 2026-09-30 | SILVER under Lesson 9 (absence: PubMed + CITR report/bibliography; premise: CITR Exhibit 2-1 vs PMID 30181166) |
| R-06 | Absence claims tiered by null searches (Lesson 9) | 2026-09-30 | 2026-09-30 | Adopted (RESEARCH_DOCTRINE.md v1.2) |
| R-07 | Bayesian path ranking | open_findings N-01 | 2026-09-30 | Withdrawn (decision A); replaced by a status table, explicitly not a ranking |
| R-08 (was D-01) | Charter §7: first meta-analysis target, store, verification method, scoring cadence | 2026-06-23 | 2026-10-06 (105 days) | All four recommended options: incretin HbA1c; JSON in `Analysis/Results/` (the Excel tracker is not a store); independent second AI extraction + verbatim span check; the daily run flags predictions, a person resolves. Recorded in `SCIENCE_ARM_BUILD_CHARTER.md` §7 (commit b482c4d, not yet on origin); INTAKE row 6. Owner asked that methods calls go to the analyst from now on |
| R-09 (was D-07) | Gap #2 question and tier | Concern 2026-08-16; brief 2026-10-01 | 2026-10-06 (51 days after the first concern) | Gap #2 = "Health Equity in Beta Cell Therapies", rated claim by claim: 5 claims, profile 0% GOLD / 20% SILVER / 80% BRONZE / 0% unverified, headline BRONZE (median claim). `gap_owner_rulings.json` tier_rulings."2"; `gap_tiers.json`; doctrine v1.3; commit e0c6cb7 (on origin). After this, no gap is GOLD |
