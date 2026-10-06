# Diabetes Research Hub: Roadmap

Maintained by the `diabetes-hub-pm` agent. It plans and documents only. Edits, rebuilds, tier changes, prediction
locks and pushes stay with the main session, on Justin's say-so. Companion files: `IDEAS.md` (ranked backlog),
`DECISIONS.md` (value/scope rulings that belong to Justin), `INTAKE.md` (Justin's questions, triaged).

---

## Status note: as of 2026-10-06 12:55 CT

**The thing you probably don't want to hear first.** Today's fixes are not public yet. The teplizumab correction, the
repaired data tables, the dashboard Source column and the two mis-cited GOLD entries sit in 2 commits (3facaa1,
b482c4d) that have not been pushed. Until they are, readers still see the wrong versions, some of them live for 169+
days. [Certain: `git ls-remote origin main` = e0c6cb7] And one wrong claim the fixes missed is live on origin today: the
Gap Deep Dives page still says "AZD1656: Phase 3", and it tells readers to "screen GCKR before AZD1656 initiation" on
mouse-only evidence. That string has been in git since 2026-03-16. [Certain: found by PM with `git show origin/main`]

**What changed since the 2026-10-05 22:02 note.**
- Gap #2 ruled 2026-10-06: "Health Equity in Beta Cell Therapies", rated claim by claim, 0/20/80/0, BRONZE. No gap is
  GOLD now. Pushed (e0c6cb7).
- Charter §7 answered (all four recommended options). Standing preference: the analyst makes methods calls; Justin
  gets value and scope calls only, in plain language.
- Fixed and committed, not pushed: teplizumab (TN-10 phase II), 5 broken tables plus a JSON-literal gate, Research
  Dashboard Source column (21 sourced, 36 "no source on file"), the prevalence and youth-incidence mis-citations, the
  endpoint gate reading weeks.
- A full gate run at 12:37: 87 stages OK; 1 red = the publish gate, red by design until the push.
- The cloud agent's 4 commits went public with e0c6cb7.

**Top 3 next actions**
1. **Main, on Justin's say-so:** push 3facaa1 and b482c4d (I-40).
2. **Main:** remove the AZD1656 "Phase 3", the GCKR screening line, the unsourced "~50M into remission" and the 29
   "(PMID requires verification)" placeholders from `build_gap_deep_dives.py` (I-34). Rebuild, gate, push.
3. **Main:** Gap #6 claim table (I-35a). It is the gap most likely to fail the way Gap #2 did. Then do #5, #8, #10
   and #12 (I-35).

**Open decisions for Justin** (plain language, oldest first; `DECISIONS.md`):
- D-02, 36 days: how strict GOLD is.
- D-04, 29 days: gaps #14/#15.
- D-05, 26 days: an edit to the cloud task.
- D-06, 20 days: how pushes happen.
- D-08, new: whether tier changes from the claim-by-claim rollout apply under the rule or come to you one at a time.

---

## Flags (unsoftened)

### Public claims that are false, unsourced or contradicted (origin/main = e0c6cb7, checked 2026-10-06)
| Claim | Where | Live since | Status |
|---|---|---|---|
| "AZD1656: Phase 3 (tachyphylaxis barrier identified), 885 patients across 23 RCTs" | `docs/Dashboards/Gap_Deep_Dives.html` (builder `build_gap_deep_dives.py` L536) | in git since 8ceb4d4, 2026-03-16 (204 d) | **Not fixed anywhere.** The GKA table on the same page was corrected 2026-09-30 (phase 2 completed, no phase 3 registered). I-34 |
| "Genetic stratification: screen GCKR before AZD1656 initiation", which reads as a treatment instruction; the basis is mouse models only (restated 10-06 in the summary) | same page, L572 | same era | **Not fixed.** I-34 |
| "expected to shift ~50M Chinese T2D patients into remission if efficacy replicated", no source | same page, L572 | same era | **Not fixed.** I-34 |
| 29 "(PMID requires verification)" placeholders | same page | same era | Honest labels, but unsourced claims all the same. I-34 |
| Teplizumab GOLD "Phase 3 RCT"; PETITE "active"; no safety statement | `Research_Findings_Summary.md` L44 | on origin by 2026-04-20 (169+ d) | Fixed in 3facaa1; **not pushed** |
| Research Dashboard pipeline: 29 of 57 rows uncited, some wrong (retatrutide 28.7%/68wk, Tzield "Phase 3", dorzagliatin "Phase 1b", three "FDA 2026") | `Research_Dashboard.html` | on origin by 2026-04-20 (169+ d) | Fixed or marked in b482c4d; **not pushed**. Afterwards, 36 rows still read "no source on file" (I-37) |
| "589 million in 2021" cited to a paper that reports 529 million; youth "Black and Hispanic 2-3x T2D" cited to PMID 37016949 (a J Pediatr Psychol systematic review of type 1 behavioural studies, verified live 2026-10-06) | `Research_Findings_Summary.md` (both rated GOLD) | not dated by PM | Fixed in b482c4d; **not pushed**. The citation gate passed the second one (I-36) |
| Five data tables on 3 dashboards did not render (unescaped quotes) | Research_Dashboard, Generic_Drug_Catalog, Immunomod_LADA | live since the 2026-09-30 push (6 d) | Fixed in 3facaa1 + `jsdatagate`; **not pushed** |
| Gap #2 GOLD with two questions | site | closed 2026-10-06 | **Fixed and public** (e0c6cb7) |
| N-04 CITR "20% at 10 years"; N-06 FDA approvals from the press | builders / summary | closed 2026-09-30 | Fixed and public; ledger rows still say open (I-39) |

### Committed work not yet pushed
- **2 commits** ahead of origin (`git log --oneline origin/main..main`): 3facaa1 (2026-10-06 12:32 CT, the oldest, <1 h
  at the time of writing) and b482c4d (12:47 CT). They hold every reader-visible fix made today except Gap #2.
- 4 untracked `Analysis/Logs/daily_pipeline_2026-10-0{3,4,5,6}.log`; no tracked file modified.
- The stale-index hazard from the last note is gone (index clean; stale locks cleared per the e0c6cb7 message).
  Recurrence guard: I-38.

### Decisions waiting on Justin (oldest first)
- D-02: GOLD = 3 separate studies (2026-08-31, 36 d).
- D-04: gaps #14/#15 (2026-09-07, 29 d).
- D-05: cloud task edit (2026-09-10, 26 d).
- D-06: push path (2026-09-16, 20 d).
- D-08: rollout tier changes, rule or case by case (2026-10-06, 0 d).
- D-03 (gap #8 card wording) has been reassigned to the analyst as a methods call (I-35).

### Gates (latest: `Analysis/Logs/pipeline_2026-10-06.log`, full run 12:37-12:46 CT, 88 stages)
- **Red:** 1. "Asserting the published SITE matches what this pipeline audits": PUBLISH_BEHIND (1 commit unpushed at
  run time; 35 of 39 `docs/` files stale for a reader). It is red by design until the push, and is now 2 commits behind.
  Everything else is OK, including `jsdatagate` (37 literals, 0 broken), endpoint gate (0 unsourced of 101 files),
  NCT gate (38/38 OK), absence-scope (78 files), gap numbering (tiers agree; 40 hardcoded copies tracked) and gap
  subject coverage (4 findings, all ACKNOWLEDGED, 0 blocking).
- **Gates that cannot fail:** 5 gate-role stages still return NO_VERDICT (`gate_exit_code_audit.json` 2026-10-06:
  42 gates, 37 can fail): `audit_path_evidence_design`, `audit_pubtype_title_disagreement`,
  `audit_gap_evidence_design`, `audit_citation_semantic_support`, `statistical_analysis`. The audit reports "0
  defects" because it does not count NO_VERDICT as one. I-20.
- **A gate that passed a wrong answer:** the markdown citation gate (81 sites, 0 flagged) passed PMID 37016949 cited as
  an MMWR report. It checks only 6 title-asserted sites against PubMed; the other 75 are checked for existence only.
  [Likely] I-36.
- The daily 05:00 task ran at 05:01 today, exit 0, 4 PASS (`daily_pipeline_2026-10-06.log`). The cloud monitor's
  "pipeline appears to have skipped 10-06" is wrong; it read the data before the pull landed, or read the wrong file.
  [Likely]

### Absence-claim scope and tier copies
- `absence_claim_scope_audit.json` (2026-10-06): 78 files, clean. Gap #2's claim 2a carries its scope: PubMed + CT.gov,
  2026-10-06, queries in `gap2_null_searches.json`; Embase and conference abstracts not searched.
- Tier copies agree (`gap_numbering_audit.json` 2026-10-06). Only Gap #2 has a claim table. Every other SILVER label is
  a gap-level tier, and five of them (#5, #6, #8, #10, #12) predate Lesson 9 with no null-search record in
  `gap_audits`. [Likely] Some will not hold up once rated claim by claim. I-35.
- Doctrine version table row 1.2 still says "Gap #11 set to BRONZE" (later promoted to SILVER the same day).
  Historical wording, but a reader can take it as current.

### Cloud agent repeating itself with no action (3+ runs)
| Escalation | Runs | Status |
|---|---|---|
| Update `Diabetes_Research_Tracker.xlsx` (81 d stale) | 10-01 to 10-06 (6) | Superseded: charter §7 Q2 says the tracker is not a store. The agent needs telling (D-05, I-11) |
| Gap-score saturation (22 of 435 at 100.0) | 10-01 to 10-06 (6) | No action; I-25 |
| Raise `domain_retmax` | 10-01 to 10-06 | No action; I-19 |
| Read abstracts 42815506, 42822480 (+ 42810355 from 10-06) | 10-01, 02, 03, 05, 06 | PMIDs verified live 2026-10-06; abstracts not screened; I-17 |
| "Confirm git push was done" (ACTION_REQUIRED 09-21 P0) | recurring | Done for the cloud commits (origin = e0c6cb7); a new backlog of 2 (I-40) |

---

## Workstreams

Stages: Observed / Understood / Integrated / Gated / Published / Retired.

### Science arm (SCIENCE_ARM_BUILD_CHARTER.md; §7 answered 2026-10-06)
| WS | Stage | Latest measured result (source) | Next step |
|---|---|---|---|
| S1 Verified effect substrate | Published | 18 records, all poolable: orforglipron 13, CagriSema 5 (`structured_effects_report.md`); the span-verification stage passed in the 10-06 full run. Verification method ratified (charter §7 Q3) | Screen ACHIEVE-4, DIABIL-2, ZUPREME 1 abstracts (I-17); DIABIL-2 would open the first T1D C-peptide cluster |
| S2 Hypothesis ledger | Observed | No ledger file. `gap_tiers.json` claim records (Gap #2: 5 claims with kind, tier, sources, scope) are most of the schema | Grow from the claim tables (I-35 → I-27) |
| S3 Prediction ledger | Integrated | 4 locked, 1 resolved, mean Brier 0.1225 (n=1) (`prediction_ledger_report.md`, 2026-10-06 12:37). The daily run now flags results postings and provisional resolutions (b482c4d, unpushed). NCT06534411 still no registry results (CT.gov v2, 2026-10-06) | Lock 2-3 more (I-08); external timestamps (I-22) |
| S4 Pooled estimates | Published | Incretin HbA1c ratified as the first target (charter §7 Q1). Pools from verified records only, k=2 per pool; `statistical_analysis.py` cannot fail (I-20) | State the path to GOLD on the page; widen once I-17 adds records |
| S5 Self-updating doctrine | Observed | Doctrine v1.3 (2026-10-06) came from an owner ruling, not a scored outcome | First entry tied to PRED-004 (I-15) |

### Research gaps (`gap_tiers.json` as_of 2026-10-06; Lesson 9 + claim rule)
| Gap | Tier | Lesson 9 evidence on file | Open ruling | Next step to next tier |
|---|---|---|---|---|
| G1 Gene Therapy for LADA | EXPLORATORY | Ruled 2026-09-30; no paper on gene therapy | none | Claim table + dated null search → BRONZE |
| G2 Health Equity in Beta Cell Therapies | BRONZE (0/20/80/0) | Ruled 2026-10-06. 2a absence SILVER (PubMed 34 hits, CT.gov 32 studies, 2026-10-06; Embase not searched); 2b-2c trial-site counts BRONZE (CT.gov 2026-10-01); 2d-2e burden BRONZE (PMIDs 36113507, 40412624: one model) | none | A burden source independent of the T1D Index, and a second site-count source, would make 2d/2b SILVER |
| G3 Insulin Resistance in Islet Tx | SILVER | Ruled 2026-09-30 (restated). Absence: PubMed 2026-09-05 + CITR 12th report. Premise weak (PMID 19584681, proxy, n=5) | none | Claim table (I-35, batch 2) |
| G4 Drug Repurposing for Islet Tx | SILVER | Ruled 2026-09-30, drug-level evidence labelled. No null-search record in `gap_audits` | none | Claim table with dated searches (I-35) |
| G5 Treg in Diabetic Neuropathy | SILVER | Pre-Lesson 9; no null-search record | none | Claim table (I-35 batch 1) |
| G6 CAR-T Access Barriers | SILVER | Pre-Lesson 9; 7 papers on both axes, so the absence may be false | none | **Claim table first (I-35a)**; may need restating, as G2 did |
| G7 GKA Drug Repurposing | SILVER | Ruled 2026-09-30; dated null search 2026-09-28 | none | Claim table; second independent source |
| G8 Immunomodulatory Drugs for LADA | SILVER | Pre-Lesson 9; 1 paper at the intersection | Reassigned to the analyst (was D-03) | Claim table marks the inferred link (I-35 batch 1) |
| G9 GKA in LADA | EXPLORATORY | 0 papers | none | Claim table + dated null search |
| G10 LADA Prevalence by Setting | SILVER | Pre-Lesson 9; 2026-10-04 audit: web-search negatives only | none | Record database/date/query first (I-35 batch 1) |
| G11 Islet Transplant Registry Equity | SILVER | Ruled 2026-09-30. Absence: PubMed + CITR report/bibliography. Premise: CITR Exhibit 2-1 vs PMID 30181166 | none | Claim table; Embase/abstracts → GOLD (I-29) |
| G12 Generic Drug x Mechanism Catalog | SILVER | Pre-Lesson 9; no null-search record | none | Claim table (I-35 batch 1) |
| G13 Personalized Nutrition for Beta Cells | EXPLORATORY | Ruled 2026-09-30; dated web null search 2026-09-28 | none | Database scope on that search → BRONZE |
| G14 Personalized Nutrition for LADA | EXPLORATORY | Agent demotion 2026-09-27; no owner ruling | **D-04 / D-08** | Claim table |
| G15 GKA Pricing Trajectory | EXPLORATORY | Same as G14 | **D-04 / D-08** | Claim table |

### Cross-cutting
| WS | Stage | Latest measured result (source) | Next step |
|---|---|---|---|
| C Credibility | Gated, with known holes | Full run 2026-10-06: every content gate OK. Holes: the AZD1656 "Phase 3" string in a `clinical_pipeline` list (no gate reads it); the markdown citation gate checks 6 of 81 sites against PubMed; 5 gates cannot fail | I-34, I-36, I-37, I-20, I-39 |
| D Data collection | Integrated | Daily task 2026-10-06 05:01, exit 0, 4 PASS. Stale git locks cleared by hand 10-06. retmax still 10 per domain; completed-without-results trials invisible | I-38, I-19, I-28, I-18 |
| P Publishing and ops | Gated, 2 behind | origin/main = e0c6cb7. 2 unpushed commits (oldest 3facaa1, 2026-10-06 12:32 CT). Publish gate red by design. Work queue: 166 of 192 items carry no status | I-40, I-10, I-24 |
| O Outreach | Observed | `CONTRIBUTION_STRATEGY.md` 182+ d stale; predictions not externally timestamped | I-22, I-30 |

---

### Commands for the main session (none run by the PM)
```
git -C C:\Users\justi\OneDrive\Diabetes_Research log --oneline origin/main..main      # 3facaa1, b482c4d
git -C C:\Users\justi\OneDrive\Diabetes_Research push origin main                    # I-40, on Justin's say-so
git -C C:\Users\justi\OneDrive\Diabetes_Research show origin/main:docs/Dashboards/Gap_Deep_Dives.html | grep -n "AZD1656: Phase 3\|screen GCKR\|50M Chinese"   # I-34
grep -n "AZD1656: Phase 3\|screen GCKR\|50M Chinese\|PMID requires verification" C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts\build_gap_deep_dives.py
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=37016949"   # I-36 test case
```
