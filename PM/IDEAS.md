# Diabetes Research Hub: Ideas Backlog

Ranked by **score = (impact x confidence) / cost**. Impact is 1-10, confidence 0-1, cost in half-day units (0.5 =
under an hour). Impact weighting: removing a false or unsourced claim a reader can see today ranks highest. Closing a
science-arm loop (a scored prediction, a verified record) ranks next. Surveillance and tooling rank last.

This list never shrinks. Ideas are marked Done or Rejected with the reason, never deleted. Owner: "Justin" means a
ruling or an action only he can take. "Main" means the main session. "Cloud" means the scheduled cloud agent.

Seeded 2026-10-05 22:02 CT (first PM pass). Sources: monitor reports 10-01 to 10-05; `open_findings.md`;
`agent_state.json` work_queue; decision briefs 08-31, 09-07 and 10-01; ACTION_REQUIRED 09-21; gate outputs; the
charter's undone phases; INTAKE rows 1-2; PM checks run 2026-10-05.

## Ranked backlog

| # | ID | Idea (one line) | Test or fix | Data needed (have?) | Stage | Owner | Cost | Impact | Conf | Score |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | I-01 | Rule on Gap #2, the last GOLD gap, then apply the ruling | Justin picks A-D in `DECISION_BRIEF_2026-10-01_Gap2.md`; main runs `set_gap_tier.py 2 <TIER> --reason ...` and re-points the evidence store at one question | Brief (have) | Understood | Justin → Main | 0.5 | 9 | 0.9 | **16.2** |
| 2 | I-02 | Decide whether GOLD needs 3 independent *datasets*, not 3 documents (doctrine Lesson 7 open contradiction) | Justin rules; main writes the rule into Lesson 7 and re-runs the design audits | `DECISION_BRIEF_2026-08-31.md` (have) | Understood | Justin | 0.5 | 7 | 0.8 | **11.2** |
| 3 | I-03 | Correct the teplizumab GOLD entry: phase II, not phase 3; PETITE completed; no safety statement | Fix `Research_Findings_Summary.md` L44 at source: TN-10 = phase II (PMID 31180194 pubtype); NCT05757713 COMPLETED, no results; add a sourced safety statement; cite 42520060 as a single case report (low evidence level, not a rate); re-check the GOLD tier against Lesson 7 | All verified live 2026-10-05 (have). A sourced label safety statement (need) | Observed | Main | 1 | 9 | 0.95 | **8.55** |
| 4 | I-16a | Mark or remove the 29 uncited rows in the Research Dashboard pipeline table | In `rebuild_research_dashboard.py`, give each figure, approval or "FDA 2026" status a PMID/NCT/fda.gov source, or mark it UNSOURCED, or drop it. Example: "8-15% NPDR reduction" sits ahead of FOCUS (NCT03811561, primary completion 2027-11-07) | Row list from the PM parse of origin/main (have) | Observed | Main | 1 | 9 | 0.85 | **7.65** |
| 5 | I-04 | Treat PRED-2026-004's resolution as provisional until REIMAGINE 5 has registry results or a paper | Add a watch on NCT06534411 (COMPLETED, hasResults false, CT.gov 2026-10-05); re-check resolution and Brier when it posts | Ledger (have) | Integrated | Cloud | 0.5 | 4 | 0.9 | **7.2** |
| 6 | I-05 | Run `falsify_equity_gaps.py` (M-03; it exists and has never run) | Run it and record whether the equity-paired top gaps survive a synonym-expanded query | Script (have) | Observed | Main | 0.5 | 5 | 0.7 | **7.0** |
| 7 | I-06 | N-08: the AZD1656 row "Phase 3 ... Development ongoing" has no source | Check the registry and fix or remove the row | CT.gov (have) | Observed | Main | 0.5 | 5 | 0.6 | **6.0** |
| 8 | I-09 | Reset the stale git index, then push the 3 cloud commits | `git reset` (mixed), confirm `git status`, push from Windows | Repo (have) | Integrated | Main (Justin's say-so) | 0.5 | 3 | 0.95 | **5.7** |
| 9 | I-07 | Escape quotes in JS data literals on 3 published dashboards and gate it | Fix the PMID linker in post-processing so it escapes `"` inside JS strings. Add a gate that parses every `const X = [...]` literal in `docs/`. Pages: Research_Dashboard, Generic_Drug_Catalog, Immunomod_LADA | origin/main HTML (have) | Observed | Main | 1 | 8 | 0.7 | **5.6** |
| 10 | I-08 | Lock 2-3 more predictions on verified future readouts | Candidates: FOCUS semaglutide retinopathy (NCT03811561, ACTIVE_NOT_RECRUITING, primary completion 2027-11-07); VA PTXRx pentoxifylline DKD (NCT03625648, primary completion 2028-01-03). Both checked 2026-10-05. Lock with probability, reasoning and lock date before any readout | Registry (have); priors (need) | Observed | Main | 1 | 7 | 0.8 | **5.6** |
| 11 | I-10 | Run the full gate pipeline before every push and at least weekly | Schedule `run_quality_improvements.py` weekly. Make "full run ≤ 24 h old" a precondition of pushing. Last full run 2026-10-01 01:10 | Runner (have) | Integrated | Main | 1 | 6 | 0.9 | 5.4 |
| 12 | I-31 | Ratify the de facto answers to charter §7 (meta target = incretin; JSON store; second-pass AI verification; scoring cadence) | Justin confirms or flips; main records it in the charter | Charter (have) | Understood | Justin | 0.5 | 3 | 0.9 | 5.4 |
| 13 | I-32 | Ratify the gap #14/#15 demotions to EXPLORATORY (agent, 2026-09-27) | Justin confirms; main writes them into `gap_owner_rulings.json` | 09-07 brief Q3 (have) | Integrated | Justin | 0.5 | 3 | 0.9 | 5.4 |
| 14 | I-11 | Retire or refresh `Diabetes_Research_Tracker.xlsx` (80 d stale, escalated 5 runs) | Recommend retiring it with a README note (JSON is the de facto store). Otherwise refresh with NCT07817251 RECRUITING and NCT06109311 results posted | Snapshots (have) | Observed | Justin → Main | 0.5 | 3 | 0.8 | 4.8 |
| 15 | I-12 | Edit the cloud task file: Step 4's "PMIDs above 42000000" rule; Step 1's vet loop | Justin edits the scheduled task (repo cannot) | ACTION_REQUIRED_2026-09-21 (have); current task text unverified | Understood | Justin | 0.5 | 4 | 0.6 | 4.8 |
| 16 | I-16b | Widen the endpoint-value gate to JavaScript data literals and JSON embedded in `docs/` | Extend `audit_endpoint_value_agreement.py`; expect a nonzero count on first run | Gate (have) | Observed | Main | 1 | 6 | 0.8 | 4.8 |
| 17 | I-13 | N-04: "20% at 10 years" attributed to CITR is probably the Edmonton single-centre figure (PMID 35588757) | Read the CITR report; fix the attribution in `build_islet_outcomes.py` | CITR 12th report (have per the G11 ruling) | Observed | Main | 1 | 7 | 0.6 | 4.2 |
| 18 | I-14 | N-06: finerenone (T1D CKD) and efsitora FDA approvals rest on press coverage | Fetch one fda.gov or sponsor document each; source or keep `[UNSOURCED]` | Web (need) | Observed | Main | 1 | 6 | 0.7 | 4.2 |
| 19 | I-15 | S5: first doctrine changelog entry tied to a scored outcome | From PRED-004: a rule on resolving from a sponsor topline (provisional flag, re-score on peer review) | Ledger (have) | Observed | Main | 1 | 5 | 0.8 | 4.0 |
| 20 | I-17 | S1 intake from new tier-1 papers | Read the abstracts of ACHIEVE-4 (42815506), DIABIL-2 (42822480) and semaglutide kidney (42823485); admit records only with an effect + CI + span. DIABIL-2 opens a T1D C-peptide cluster. TRIUMPH-2 (42810372) gives no HbA1c in its abstract (run report 10-01) | PMIDs verified 2026-10-05 (have); abstracts (fetch) | Observed | Main/Cloud | 1 | 6 | 0.6 | 3.6 |
| 21 | I-18 | Sort `intervention_types` in `baseline_clinical_trials.py` to stop false diffs | One sort | Script (have) | Observed | Main | 0.5 | 2 | 0.9 | 3.6 |
| 22 | I-23 | Restore the `open_findings.md` re-emit (M-08 has regressed: no monitor report since 10-01 references it) | Add "re-emit open_findings" to the monitor's checklist, or have the PM own the re-emit | Ledger (have) | Integrated | Cloud | 1 | 4 | 0.9 | 3.6 |
| 23 | I-19 | Raise or page `domain_retmax` (D-12): 161 of 1,023 matches read | Page the E-utilities results; then volume trends become measurable | Script (have) | Observed | Main | 1 | 4 | 0.8 | 3.2 |
| 24 | I-20 | Label or wire the 5 gate-role stages that cannot fail | `audit_path_evidence_design`, `audit_pubtype_title_disagreement`, `audit_gap_evidence_design`, `audit_citation_semantic_support`, `statistical_analysis`: REPORT ONLY tag or nonzero exit | `gate_exit_code_audit.json` (have) | Observed | Main | 1 | 4 | 0.8 | 3.2 |
| 25 | I-21 | Find the parent paper Amendolara et al. (Diabetes 2026), LADA beta-cell function vs IR; two letters already in the hub (42766777, 42766770, verified 2026-10-05) | PubMed search | (fetch) | Observed | Cloud | 0.5 | 2 | 0.8 | 3.2 |
| 26 | I-22 | Externally timestamp prediction locks (OSF or a pushed tag per lock) | Locks are only provable after a push; register each lock on OSF per `OSF_PREREGISTRATION.md` | (have) | Observed | Justin | 1 | 5 | 0.6 | 3.0 |
| 27 | I-24 | Clean up the work queue: 168 of 192 items have no closed status; 11 open with "DONE/RESOLVED"; 79 predate September or are undated | Close, merge or re-date; the PM proposes the list, the cloud agent applies it | `agent_state.json` (have) | Observed | Cloud | 1 | 3 | 0.9 | 2.7 |
| 28 | I-25 | Fix gap-score saturation (22 of 435 pairs tie at 100.0; escalated 5 runs; M-02) | Observed/expected ratio with a CI; synonym-expanded domain strings ("islet transplantation" vs "islet transplant") | Gap data (have) | Understood | Main | 2 | 6 | 0.8 | 2.4 |
| 29 | I-26 | Re-derive the SILVER tiers of gaps #5, #6, #8, #10 and #12 under Lesson 9 | Record dated null searches (database/date/query/hits) in `gap_audits`; source the premise; bring proposed tiers to Justin. G6 has 7 papers on both axes, so it may not be an absence | Searches (need) | Observed | Cloud → Justin | 3 | 8 | 0.7 | 1.9 |
| 30 | I-27 | S2 hypothesis ledger: one falsifiable claim record per gap | Schema: statement, absence sources, premise source, contradicting PMIDs, next promoting test; seeded from `gap_tiers.json` + `gap_audits` | (have) | Observed | Main | 3 | 7 | 0.8 | 1.9 |
| 31 | I-28 | D-11/D-17: completed trials without results are invisible to the collectors (e.g. CagriSema NCT06323161 and NCT06797869 per F-06) | Add terminal statuses; key watches on OverallStatus | Collector (have) | Understood | Main | 2 | 5 | 0.7 | 1.75 |
| 32 | I-30 | Refresh `CONTRIBUTION_STRATEGY.md` (181+ d stale, predates Lessons 7-9) | Rewrite against the doctrine | (have) | Observed | Main | 1 | 2 | 0.6 | 1.2 |
| 33 | I-29 | Gap #11 to GOLD: a third independent absence source | Embase or conference-abstract search; Embase access probably unavailable | Access (need) | Observed | Cloud | 3 | 4 | 0.5 | 0.67 |

## Done / Rejected

| ID | Idea | Verdict | Date | Reason / evidence |
|---|---|---|---|---|
| I-00 | Build a hub PM separate from NFL and hockey | Done | 2026-10-05 | `diabetes-hub-pm` agent; this PM\ folder (INTAKE row 3) |
| I-x1 | "Manually check NCT05757713" (cloud agent, 5 runs) | Done | 2026-10-05 | CT.gov v2: Teplizumab in Pediatric Stage 2 T1D, Sanofi, PHASE4, COMPLETED, hasResults false. Feeds I-03 |
