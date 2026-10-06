# Diabetes Research Hub: Roadmap

Maintained by the `diabetes-hub-pm` agent. It plans and documents only. Edits, rebuilds, tier changes, prediction
locks and pushes stay with the main session, on Justin's say-so. Companion files: `IDEAS.md` (ranked backlog),
`DECISIONS.md` (rulings that belong to Justin), `INTAKE.md` (Justin's questions, triaged).

---

## Status note: as of 2026-10-05 22:02 CT (first PM pass)

**The thing you probably don't want to hear first.** Two claims that are wrong or unsourced have been on the public
site since at least 2026-04-20 (168+ days). No gate catches either.
1. The teplizumab entry in `Research_Findings_Summary.md` is rated GOLD as a "Phase 3 RCT". Its only cited trial
   (PMID 31180194, TN-10) is a phase II trial according to PubMed's own pubtype. It also lists PETITE-T1D
   (NCT05757713) as "active/not recruiting", but the registry says COMPLETED, with no results posted. It gives no
   safety statement, and a new case report has just appeared (fulminant HLH after teplizumab, PMID 42520060). All
   three were checked live today. [Certain]
2. On the Research Dashboard pipeline table, 29 of 57 rows give figures, approvals or "FDA 2026" statuses with no
   citation. Examples: "28.7% weight loss at 68wk", "Insulin independence >5 years", "8-15% NPDR reduction" (the
   semaglutide retinopathy trial NCT03811561 has not read out; its primary completion is 2027-11-07). The
   endpoint-value gate reports 0 unsourced values because it does not read JavaScript data literals. [Certain that
   the rows are uncited; Likely that the gate's scope is why]

**What changed since 2026-09-30.** (No earlier PM note exists, so this list is reconstructed.)
- Justin ruled on gaps #1, #3, #4, #7, #11 and #13 on 2026-09-30 (`gap_owner_rulings.json`). Lesson 9 was added to
  the doctrine.
- He also withdrew the Bayesian path ranking (decision A, 2026-09-30). Uncited endpoint values went from 31 to 0
  (`endpoint_value_agreement_audit.json`, 2026-10-01). Note that this gate cannot see item 2 above.
- On 2026-10-01: the first scored prediction, PRED-2026-004 (Brier 0.1225, resolved from a sponsor topline). The
  S1 substrate grew to 18 verified records. One tier store was built (`gap_tiers.json` + `set_gap_tier.py`).
  Zimislecel's "FDA approved" was corrected on Gap #2's page. All of this was pushed (origin/main = 5526140).
- The Gap #2 brief has been waiting since 2026-10-01.
- The cloud agent committed 3 daily iterations (10-01, 10-03, 10-05). None is pushed.

**Top 3 next actions**
1. **Justin:** rule on Gap #2 (`DECISION_BRIEF_2026-10-01_Gap2.md`, recommendation A = BRONZE). Also rule on the
   GOLD "datasets, not documents" question, which has been open since 2026-08-31. A GOLD tier whose premise the cloud
   agent called falsified on 2026-09-04 is still live.
2. **Main session:** correct the teplizumab entry: phase II label, PETITE COMPLETED, a sourced safety statement, and
   the HLH case report labelled as a single case report. Mark or remove the 29 uncited Research Dashboard rows.
   Escape the quotes in the JS data literals on 3 dashboards (see C below).
3. **Main session:** fix the stale git index (see P below). Then run the full gate pipeline, which last ran
   2026-10-01 01:10. Then push.

**Open decisions for Justin** (details in `DECISIONS.md`): Gap #2 tier (4 days on the brief; first flagged
2026-08-16, 50 days ago) · GOLD = 3 datasets, not 3 documents (35 days) · cloud task file Step 4/Step 1 edit
(25 days) · how unattended pushes happen (19 days) · ratify the gap #14/#15 demotions and the gap #8 card wording
(28 days) · ratify the de facto answers to the charter's §7 questions (104 days).

---

## Flags (unsoftened)

### Public claims that are false, unsourced or contradicted
| Claim | Where | Live since | Evidence |
|---|---|---|---|
| Teplizumab GOLD "(Phase 3 RCT + FDA approval ...)"; the cited trial is phase II | `Research_Findings_Summary.md` L44 (public repo) | added 2026-03-15; on origin by 2026-04-20 (168+ d) | PubMed esummary 31180194 pubtype "Clinical Trial, Phase II", checked 2026-10-05 |
| PETITE-T1D "active/not recruiting" | same line | same | ClinicalTrials.gov v2 NCT05757713: COMPLETED, hasResults false (2026-10-05) |
| No safety statement on GOLD teplizumab claims; new HLH case report | same line + 14 site pages that mention teplizumab, none citing 42520060 | n/a | PMID 42520060 (Diabetes Care 2026 Oct 1, pubtype Case Reports), checked 2026-10-05. A single case report: low evidence level, not a rate |
| 29 of 57 pipeline rows give figures, approvals or "FDA 2026" with no citation | `docs/Dashboards/Research_Dashboard.html` PIPELINE_DATA (builder `rebuild_research_dashboard.py`) | 2026-03-16; on origin by 2026-04-20 (168+ d) | PM parse of origin/main, 2026-10-05 |
| Gap #2 tier GOLD, with two different questions under one number | `gap_tiers.json`, site | GOLD premise called falsified 2026-09-04 (31 d) | `DECISION_BRIEF_2026-10-01_Gap2.md` |
| N-04: "20% at 10 years" attributed to CITR | `build_islet_outcomes.py` | open since 2026-09-30 | `open_findings.md` N-04 [Likely] |
| N-06: finerenone (T1D CKD) and efsitora FDA approvals rest on press coverage only | `Research_Findings_Summary.md` (marked `[UNSOURCED]`) | open since 2026-09-30 | `open_findings.md` N-06 |
| N-08: AZD1656 "Phase 3 ... Development ongoing" has no source | GKA table | open since 2026-09-30 | `open_findings.md` N-08 |

### Published pages whose data scripts are syntactically broken
Three published dashboards embed PubMed links with unescaped double quotes inside JavaScript data literals
(`"result": "... (<a href="https://pubmed...`). That is a syntax error in the data block. [Certain] The tables built
from that block probably do not render. [Likely: not yet seen in a browser] The pages are `Research_Dashboard.html`
(since 2026-08-17), `Generic_Drug_Catalog.html` (since 2026-09-18) and `Immunomod_LADA.html`. They went live with the
2026-09-30 push. The likely source is the PMID linker in the post-processing step ("Post-processing dashboards (nav,
PMID links, ARIA)"). No gate parses these literals.

### Committed work not yet pushed
- 3 commits ahead of origin (`git log --oneline origin/main..main`). Oldest: ce2bf84, 2026-10-01 12:36 UTC (4 days).
  They are cloud-agent iterations. Their 38 `docs/` changes are line endings only
  (`git diff --ignore-cr-at-eol HEAD~3 HEAD -- docs` is empty), so readers see no difference until something else
  changes.
- **Hazard [Certain]:** the git index is stale. It holds the pre-cloud-commit state of 166 paths
  (`git diff --cached --stat HEAD`: 17,001 insertions and 83,053 deletions, the mirror image of the cloud commits).
  A plain `git commit` from this checkout would quietly revert the cloud agent's three commits, including the
  agent_state backups and the 09-30 and 10-01 pipeline logs. Reset the index before committing anything:
  `git -C C:\Users\justi\OneDrive\Diabetes_Research reset` (mixed; it keeps the working tree). Then re-check
  `git status`.

### Decisions waiting on Justin (oldest first)
See `DECISIONS.md`: charter §7 (since 2026-06-23, 104 d) · GOLD datasets vs documents (2026-08-31, 35 d) · gap #8
card and #14/#15 ratification (2026-09-07, 28 d) · task file Step 4 (2026-09-10, 25 d) · push path (2026-09-16, 19 d)
· Gap #2 (brief 2026-10-01, 4 d; concern first raised 2026-08-16).

### Gates
- The last full gate run was `Analysis/Logs/pipeline_2026-10-01.log` (01:10), with 3 FAILED: gap numbering/tier
  agreement, the published site matching origin, and the publish fixture. The tier failure was fixed minutes later by
  the one-tier-store commit (`gap_numbering_audit.json` 01:17: `tier_defects: []`). The two publish failures predate
  the 01:19 push. No full run since, so **no gate has checked anything committed after 2026-10-01 01:10**. The daily
  05:00 task runs only the data pull, PubMed, gap analysis and the hub monitor (`daily_pipeline_2026-10-05.log`: 4
  PASS, exit 0).
- **Gates that cannot fail:** `gate_exit_code_audit.json` (2026-10-05) counts 41 gates, of which 36 can fail. The 5
  gate-role stages with NO_VERDICT are `audit_path_evidence_design.py`, `audit_pubtype_title_disagreement.py`,
  `audit_gap_evidence_design.py`, `audit_citation_semantic_support.py` and `statistical_analysis.py`. Either label
  them REPORT ONLY or wire up their exit codes. [Likely: the audit's classification]

### Absence-claim scope and tier copies
- `absence_claim_scope_audit.json` (2026-10-01): 0 findings across 78 files.
- Tier copies: `gap_numbering_audit.json`: `tier_defects` and `topic_defects` both empty. But the *question* differs
  between copies for Gap #2: "Health Equity in Diabetes" in `gap_tiers.json` and the evidence store, "...in Beta Cell
  Therapies" on the page. No gate compares questions. See the brief.
- Doctrine version table (RESEARCH_DOCTRINE.md L999) says "Gap #11 set to BRONZE". The store says SILVER (promoted
  later the same day). This is historical wording, but a reader can take it as current.
- Gaps #5, #6, #8, #10 and #12 still carry SILVER tiers set before Lesson 9. `agent_state.json` `gap_audits` holds
  dated null-search records only for gaps #7, #11 and #13. Gap #6 has 7 stored papers on both axes; as with Gap #2,
  that is not an absence. [Likely: these tiers do not survive Lesson 9 as they stand]

### Cloud agent repeating itself with no action (3+ runs)
| Escalation | Runs | Status |
|---|---|---|
| Update `Diabetes_Research_Tracker.xlsx` (80 d stale) | 10-01, 02, 03, 04, 05 | No action. Recommend retiring it (charter §7 Q2 was answered de facto: JSON) |
| Gap scores saturated (22 of 435 pairs at 100.0) | 10-01 to 10-05 | No action; idea I-25 |
| "Manually check NCT05757713" | 10-01 to 10-05 | **Resolved by PM 2026-10-05:** COMPLETED, no results posted (CT.gov v2). The agent should drop it |
| Read and verify PMID 42815506 | 10-01, 02, 03, 05 | Verified to exist today: ACHIEVE-4, Lancet 2026 Sep 30. Abstract not yet read for a substrate record (I-17) |
| `open_findings.md` "re-emit every run" | not re-emitted in any monitor report since 10-01 | M-08 has regressed; I-23 |

---

## Workstreams

Stages: Observed / Understood / Integrated / Gated / Published / Retired.

### Science arm (SCIENCE_ARM_BUILD_CHARTER.md)
| WS | Stage | Latest measured result (source) | Next step |
|---|---|---|---|
| S1 Verified effect substrate | Published | 18 records, all poolable (schema-valid, span-verified, second-pass agreed): orforglipron 13, CagriSema 5 (`structured_effects_report.md`, 2026-10-01). Done-when (≥5 in one cluster) met | Screen ACHIEVE-4 (42815506) and DIABIL-2 (42822480) abstracts for an effect with a CI. DIABIL-2 would open the first T1D C-peptide cluster |
| S2 Hypothesis ledger | Observed (not started) | No ledger file. Lesson 9 now defines the shape (absence + premise + next search) | Draft one claim record per gap from `gap_tiers.json` + `gap_audits` (I-27) |
| S3 Prediction ledger | Integrated | 4 locked, 1 resolved, mean Brier 0.1225 (n=1) (`prediction_ledger_report.md`, 2026-10-01). PRED-004 resolved from a sponsor topline; NCT06534411 has no registry results (CT.gov v2, 2026-10-05) | Lock 2-3 more on verified future readouts (I-08); watch PRED-004 for peer review (I-04) |
| S4 Pooled estimates | Published [Likely] | Only verified records pooled. E.g. CagriSema 2.4/2.4 mg vs placebo, k=2, -1.687 (95% CI -1.901 to -1.474), I² 0, caveats attached (`statistical_analysis.json` meta_analysis). `hba1c_pooled` null | With k=2 per pool, heterogeneity can't be estimated; state the path to GOLD on the page (charter done-when) |
| S5 Self-updating doctrine | Observed (not started) | The doctrine has a version table but no entry traced to a scored outcome | First entry from PRED-004 (rule for sponsor-topline resolutions) (I-15) |

### Research gaps (tier from `gap_tiers.json`, as_of 2026-10-01; Lesson 9 evidence)
| Gap | Tier | Lesson 9 evidence on file | Open ruling | Next step to next tier |
|---|---|---|---|---|
| G1 Gene Therapy for LADA | EXPLORATORY | Ruled 2026-09-30; 0 of 47 papers touch gene therapy | none | A dated, recorded null search → BRONZE |
| G2 Health Equity (two questions) | GOLD | Absence: 1 source (co-publication matrix). Premise: trial geography sourced (CT.gov 2026-10-01), burden split not | **Yes: brief 2026-10-01** | Ruling A → BRONZE; WHO/IDF burden + dated null search → SILVER |
| G3 Insulin Resistance in Islet Tx | SILVER | Ruled 2026-09-30 (restated). Absence: PubMed all-time 2026-09-05 + CITR 12th report. Premise weak (PMID 19584681, proxy, n=5) | none | Third independent source + a stronger premise → GOLD |
| G4 Drug Repurposing for Islet Tx | SILVER | Ruled 2026-09-30: drug-level evidence counts, labelled. 0 papers at the intersection | none | Dated null searches in 2 sources, recorded in `gap_audits` (none on file) |
| G5 Treg in Diabetic Neuropathy | SILVER | Pre-Lesson 9 tier; no `gap_audits` null-search record | none raised | Re-derive under Lesson 9 (I-26) |
| G6 CAR-T Access Barriers | SILVER | Pre-Lesson 9; 7 papers on both axes, so possibly not an absence | none raised | Re-derive; may need restating like G2 (I-26) |
| G7 GKA Drug Repurposing | SILVER | Ruled 2026-09-30; dated null search 2026-09-28 (`gap_audits`) | none | Second independent source + sourced premise |
| G8 Immunomodulatory Drugs for LADA | SILVER | Pre-Lesson 9; 1 paper at the intersection; 09-07 brief Q4 never ruled | **Ratify** | Re-derive (I-26) |
| G9 GKA in LADA | EXPLORATORY | 0 papers | none | Dated null search → BRONZE |
| G10 LADA Prevalence by Setting | SILVER | Pre-Lesson 9; 2026-10-04 audit: web-search negative only, "promotion_candidate" true | none raised | Record the null searches by database/date/query; promotion must wait for that |
| G11 Islet Transplant Registry Equity | SILVER | Ruled 2026-09-30. Absence: PubMed + CITR report/bibliography. Premise: CITR Exhibit 2-1 vs PMID 30181166 | none | Embase or conference abstracts → GOLD (I-29) |
| G12 Generic Drug x Mechanism Catalog | SILVER | Pre-Lesson 9; no null-search record | none raised | Re-derive (I-26) |
| G13 Personalized Nutrition for Beta Cells | EXPLORATORY | Ruled 2026-09-30; dated null search 2026-09-28 is on file (web) | none | Stating that search's database scope would support BRONZE |
| G14 Personalized Nutrition for LADA | EXPLORATORY | Demoted 2026-09-27 by the agent; no owner ruling recorded | **Ratify** | Dated null search → BRONZE |
| G15 GKA Pricing Trajectory | EXPLORATORY | Same as G14 | **Ratify** | Dated null search → BRONZE |

### Cross-cutting
| WS | Stage | Latest measured result (source) | Next step |
|---|---|---|---|
| C Credibility | Gated (with blind spots) | Endpoint gate 0 unsourced, NCT gate 37/37 OK, absence-scope 0 (audits 2026-10-01). Blind spots: JS data literals (29 uncited rows), teplizumab phase label | I-03, I-16a, I-16b, I-07 |
| D Data collection | Integrated | Daily 05:00 task re-registered by Justin; ran 2026-10-05, exit 0 (`daily_pipeline_2026-10-05.log`). 906 trials; PubMed reads 161 of 1,023 matches (retmax). Tracker xlsx 80 d stale. Completed trials without results still invisible (D-11) | I-11, I-19, I-28, I-18 |
| P Publishing and ops | Integrated, not Published | origin/main = 5526140 (2026-10-01). 3 unpushed commits, stale index, no full gate run since 10-01. Work queue: 168 of 192 items carry no closed status (`agent_state.json`) | Reset the index → full gate run → push (I-09, I-10); queue hygiene (I-24) |
| O Outreach | Observed | `CONTRIBUTION_STRATEGY.md` 181+ d stale (D-22); `OSF_PREREGISTRATION.md` exists, predictions not externally timestamped | I-22, I-30 |

---

### Commands for the main session (nothing here has been run by the PM)
```
git -C C:\Users\justi\OneDrive\Diabetes_Research diff --cached --stat HEAD | tail -1   # confirm the stale index
git -C C:\Users\justi\OneDrive\Diabetes_Research reset                                 # mixed reset; working tree kept
git -C C:\Users\justi\OneDrive\Diabetes_Research log --oneline origin/main..main       # 3 commits to publish
curl -s "https://clinicaltrials.gov/api/v2/studies/NCT05757713?fields=OverallStatus,HasResults"
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=31180194,42520060"
```
