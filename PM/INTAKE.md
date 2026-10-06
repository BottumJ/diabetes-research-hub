# Diabetes Research Hub: Intake

Justin's questions about the hub, logged by the main session as they are asked. The PM triages each untriaged row into
IDEAS / ROADMAP / DECISIONS and fills in "Routed to". Rows are never deleted.

| # | Date | From | Question / request | Routed to | Status |
|---|---|---|---|---|---|
| 1 | 2026-10-05 | Justin | "What else can we improve upon?" | IDEAS.md: full ranked backlog (33 ideas; top: I-01 Gap #2 ruling, I-02 GOLD datasets rule, I-03 teplizumab entry, I-16a uncited pipeline rows). ROADMAP.md status note: top 3 next actions | Answered 2026-10-05 |
| 2 | 2026-10-05 | Justin | "What's the status of our project manager's projects?" | ROADMAP.md: status note + workstream tables (S1-S5, G1-G15, C, D, P, O); DECISIONS.md: 7 open decisions | Answered 2026-10-05 |
| 3 | 2026-10-05 | Justin | "Build a project manager agent separate from NFL and the others to manage this" | Done: `diabetes-hub-pm` agent (C:\Users\justi\.claude\agents\diabetes-hub-pm.md) and this PM\ folder; IDEAS I-00 | Done 2026-10-05 |
| 4 | 2026-10-06 | Justin | "Please describe what you're expecting me to rule on" (Gap #2) | Answered in session: two decisions (which question, which tier); brief DECISION_BRIEF_2026-10-01_Gap2.md | Answered 2026-10-06 |
| 5 | 2026-10-06 | Justin | "Be as specific as possible; parts of titles can have differing levels of validation and a cumulative percentage rating of bronze/silver/gold" (e.g. 8 of 10 subjects triple-verified, 1 double, 1 none = 80/10/0/10) | RULED: Gap #2 = Health Equity in Beta Cell Therapies, claim-by-claim, 0/20/80/0, BRONZE (gap_tiers.json, gap_owner_rulings.json, doctrine 1.3). DECISIONS D-07 closed. Rollout of claim tables to the other 14 gaps = new idea for the PM to rank | Applied 2026-10-06 (main session) |
| 6 | 2026-10-06 | Justin | Charter s7: "Confirm or change what?" then chose all four recommended options; "I am not a doctor ... looking to have AI help improve the science" | RULED: incretin HbA1c; JSON store; AI second pass + span check; daily run flags predictions (implemented). Recorded in SCIENCE_ARM_BUILD_CHARTER.md s7. DECISIONS D-01 closed. Standing preference: analyst makes methods calls, owner gets value calls | Applied 2026-10-06 |
| 7 | 2026-10-06 | Justin | "Fix all" (teplizumab entry, Research Dashboard uncited rows, broken JS tables) | Done 2026-10-06: teplizumab re-rated claim by claim from FDA letters + TN-10 + PROTECT + HLH case report; pipeline table gets a Source column (21 sourced, 36 marked no source); PMID linker escaped in scripts + jsdatagate; endpoint gate reads weeks. Also found: global prevalence and youth-incidence entries mis-cited (fixed); markdown citation gate passed a wrong-paper citation (new idea) | Done 2026-10-06 |
