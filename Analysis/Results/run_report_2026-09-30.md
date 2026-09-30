# Run Report — 2026-09-30 (local session on the owner's machine)

This run happened on the Windows host, with the owner present, not in the cloud
sandbox. That is why it could do three things no scheduled run has done since
April: push, run all stages in one process, and get rulings.

## 1. Pushed. The publish blocker is closed.

`origin/main` moved `f7e976f` (2026-04-20) → `1cb1d46`, 127 commits. The host's
git credential manager holds a GitHub credential; the sandbox never did.
Checked on the live site afterwards, not inferred from the push: landing page
reads "Last updated: 2026-09-29", `docs/Reports/literature_gap_report.md`
returns 200, and "70% graft survival" is absent from the three dashboards that
carried it.

The index was stale, not the tree. `git status` showed 66 `MM` files because
the sandbox commits through a private index; `git reset` (mixed) cleared it and
the tree was already identical to HEAD.

**Still open, and only the owner can do them:**

- The Windows scheduled task `DiabetesHub_GapAnalysis` points at
  `Analysis\Scripts\run_gap_analysis.ps1`, which no longer exists. It has exited
  `0xFFFD0000` every morning. `register_daily_task.ps1` (written 2026-07-17)
  replaces it with the full daily pull and was never run. The session was not
  permitted to register a scheduled task.
- Unattended publishing. The session was not permitted to add an automatic push
  to the daily task. Until the owner chooses a publishing path, pushing is a
  manual `git push origin main` from this machine.
- The cloud task file still instructs a sweep for "PMIDs above 42000000".

## 2. Owner rulings (DECISION_BRIEF_2026-09-07 §2), recorded in `gap_owner_rulings.json`

| Gap | Ruling | Effect |
|---|---|---|
| #1 Gene Therapy for LADA | Demote | SILVER → EXPLORATORY |
| #13 Personalized Nutrition for Beta Cells | Demote | BRONZE → EXPLORATORY |
| #4, #7 drug repurposing | Drug-level evidence counts, labelled | Tier unchanged; reader note published |
| PRED-2026-002, -003 | Lock as written | Locked 2026-09-30 at 0.50 and 0.85 |

Reconciled at the same time, because the tier lived in more places than any one
edit had reached: #6 and #11 were SILVER in agent state and on the site
(2026-09-08) but GOLD in `extract_evidence.py`, `build_gap_deep_dives.py`,
`build_methodology.py`, `build_cart_access.py`, `build_islet_equity.py` and the
README; #14 and #15 were EXPLORATORY in one builder (2026-09-27) and BRONZE
everywhere else. Tier counts are now 2 GOLD, 8 SILVER, 0 BRONZE, 5 EXPLORATORY.

`audit_gap_subject_coverage.py` changed in two ways. EXPLORATORY gaps are no
longer findings (the label claims no evidential standing). A finding covered by
a recorded ruling is reported as ACKNOWLEDGED and does not fail the build,
provided the ruling carries the sentence readers are shown.
**Gap #11 is still a real, unruled finding and the gate is still red on it.**

The caveat on the Extracted Evidence page had been printing the gate's
*remedy* text — a maintainer instruction — to readers, and that text ("record
that the gap has never been tested") was itself tripping the absence-claim
gate. It now prints a reader note only.

## 3. Citation backlog: 31 → 14 uncited endpoint values

Each source was read in PubMed or at fda.gov this run.

- **Edmonton 20-year cohort** — PMID 35588757 (Marfil-Garza, *Lancet Diabetes
  Endocrinol* 2022): 255 patients; Kaplan-Meier insulin independence 61% at
  1 year, 32% at 5, 20% at 10, 8% at 20. Attached to five statements.
- **Zimislecel** — PMID 40544428: 10 of 12 (83%) insulin-independent at day 365.
  Attached to two statements.
- **LANTIDRA "67% insulin independence at 1 year" was not supportable and has
  been replaced.** FDA's approval announcement (2023-06-28) says 21 of 30
  participants did not need insulin for a year or more. Six copies across two
  builders, one of which also claimed "vs 61% Edmonton, improved graft survival
  trajectory" and another projected "50% at 5yr, 30-40% at 10yr". No comparison
  with the Edmonton cohort exists and no such projection was published. The
  first repair fixed four copies; searching for the claim rather than the edit
  found two more.

**Not fixed, and why** (14 remain):

| Where | Value | Status |
|---|---|---|
| `build_data_dictionary.py` 763, 1232; `build_gap_deep_dives.py` 163, 177, 247 | Tacrolimus insulin resistance "40% at 3 months", "35% at 1yr" | Source not found. Do not cite until one is. |
| `build_gap_deep_dives.py` 177 | Edmonton 61% / 8% | Same line as the tacrolimus figure; one PMID on the line would mis-attribute it. Split the sentence first. |
| `build_gap_deep_dives.py` 1634 | HbA1c −0.8% at 3 months (GCKR carriers) | Source not found. |
| `build_lada_model.py` 874 | GAD-alum "30–40% preserved C-peptide at 4 years" | Not in the abstract of the PMID cited above it (32754804), which reports treatment-effect ratios in recent-onset type 1 diabetes, not a 4-year response rate. |
| `build_islet_outcomes.py` 904 | "20% at 10 years (CITR Annual Reports … 1,477-recipient registry)" | 20% at 10 years is exactly the Edmonton single-centre figure (n=255, PMID 35588757). The attribution to a 1,477-recipient registry looks wrong. **[Likely]** — CITR reports not read. |
| `build_islet_outcomes.py` 661, 691, 692 | 70% / 60% | HTML comment prose describing a past correction, not a claim. Gate false positive. |

**Also seen in `build_gap_deep_dives.py` line 247 and not verified:** "CryoLife
cryopreservation", "reduced ischemia time (8.6 vs 22 hours)", "Coverage by
United, Aetna, Cigna, Medicare as of 2025". None carries a source. The FDA
announcement does not mention cryopreservation.

## 4. Findings summary

- **Orforglipron: right paper, wrong trial name.** PMID 41765029 is ACHIEVE-3
  (NCT06045221), not ACHIEVE-4. ACHIEVE-4 is NCT05803421 (vs insulin glargine),
  completed, no results. The "newly posted NCT06045221 results" two monitor
  reports asked to have reviewed were already cited, under the other name.
- **Added:** finerenone in type 1 diabetes and CKD (FINE-ONE, PMID 41780000,
  BRONZE — one RCT, surrogate endpoint) and insulin efsitora (QWINT-1/3/4/5),
  including the higher severe-hypoglycaemia rate in type 1 diabetes.
- **Not verified:** the September 2026 FDA approvals for both. Marked
  [UNSOURCED]; no FDA or sponsor document was fetched.

## 5. Science arm, Phase 1: done for one cluster

`structured_effects.py` + `structured_effects.json`. 13 HbA1c treatment
differences from the four orforglipron phase 3 trials that report one in their
abstract (ACHIEVE-1, -2, -3, -5). Every record is schema-valid, its quoted span
is verbatim in the live PubMed abstract, and an independent second extraction
agreed on every number. ATTAIN-2 and ACHIEVE-J were considered and not
admitted. Negative controls were run on the verifier (wrong number, paraphrased
span, missing variance: all rejected).

No pooled estimate was produced. Arms within a trial share a comparator; pooling
them as independent would understate the variance. That is Phase 4.

`prediction_ledger_report.md` had been stating "PRED-2026-004 RESOLVED TRUE,
Brier 0.1225" since 2026-06-23 while the ledger itself held no resolution.
Regenerated: 4 locked, 0 resolved. The ledger dashboard was built only by refresh_hub.py, which the pipeline never calls, so the first push today published the two new locks as UNLOCKED. It is now a pipeline stage and the page was rebuilt and re-pushed.

## 6. Three things that only fail on Windows

- `build_repurposing_dashboard_v2.py` wrote with the platform default encoding
  (cp1252) and died on the first local run.
- `test_publish_reachability_gate.py` could not delete git's read-only object
  files.
- NCBI returned 429 while the pipeline and a verifier ran together;
  `structured_effects.py` now retries.

## 7. Not done

- `Diabetes_Research_Tracker.xlsx` (stale since 2026-07-17) and its March lock
  file were not touched.
- `open_findings.md` has not been re-emitted since 2026-09-12, which is the
  defect it was created to prevent.
- EASD 2026 abstracts were not reviewed.
