# Open Findings Ledger

**Created:** 2026-09-12 — prescribed by `monitor_report_2026-09-10.md` (meta-defect #14) and
re-prescribed 09-11.

**Purpose.** A recommended-action list gets re-ranked and items fall off it silently. This file
does not get re-ranked. One line per unresolved finding, with the date it was found and the date
it closes. **Re-emit this file verbatim in every monitor run.** Nothing leaves it except by being
resolved, with the resolution recorded.

**Rule.** If a finding appears in a monitor report and is not resolved in that same report, it
belongs here before the report ships.

---

## A. Open findings — substantive (about the world)

| ID | Found | Finding | Status | Closes when |
|----|-------|---------|--------|-------------|
| F-01 | 09-06 | **ATTAIN-2** (`NCT05872620`, orforglipron Ph3, n=1,613) results posted 09-04 | Read 09-11; **not in tracker** | Logged in tracker with estimand |
| F-02 | 09-11 | **ATTAIN-2 estimand discrepancy** — registry 5.50/7.78/10.54 vs published 5.1/7.0/9.6; registry uses the efficacy (on-treatment) estimand | Open; explanation **[Likely]**, *Lancet* primary unread | *Lancet* `S0140-6736(25)02165-8` read and both estimands recorded |
| F-03 | 08-31 | **Ladarixin** (`NCT04628481`, n=289) TERMINATED for futility; still unpublished by anyone | Open; **tier corrected to BRONZE** on 09-11 | Logged in tracker as BRONZE |
| F-04 | 08-28 | **Mounjaro/tirzepatide CV indication** — hub logged it as an FDA action on 08-28; 09-12 search describes it as expected H2 2026. **Internally contradictory.** | Open, unresolved | One primary fda.gov fetch settles it |
| F-05 | **09-12** | **ZUPREME-2** (`NCT06926842`) went `ACTIVE_NOT_RECRUITING` → `COMPLETED` on **09-09**. Missed for 3 days because the watch was keyed on `ResultsFirstPostDate` | Open | Logged in tracker; watch re-keyed (see D-17) |
| F-06 | **09-12** | **CagriSema completion cluster** — `NCT06534411` (Ph3, n=1,023, vs tirzepatide), `NCT06323161` (Ph3, n=274), `NCT06797869` (Ph2, n=142) all COMPLETED, none with results, none visible to the hub | Open | Logged in tracker; collector fixed (D-11) |
| F-07 | 09-01 | **Zenagamtide** `NCT07797335` (Novo, AMBITION 7, Ph3, n=1,778) — new Ph3 in a tracked sponsor's pipeline | Confirmed live 09-12; not tracked | Added to watch list by NCT ID |
| F-08 | 09-11 | **Renal-outcomes signal on orforglipron appearing twice in one month** (PMIDs 42715144, 42582425) — the kind of cluster the hub exists to notice; `retmax` hid it | Open | Both read, or retmax raised and re-run |
| F-09 | 09-06 | **PMID 42694848** — COL1A2/APOLD1 dual-axis, nephropathy–retinopathy. The **only 4-domain cross-domain paper on record** | Unread, 6 days | Read |
| F-10 | **09-12** | **PMID 42720752** — PROTECT per-protocol, teplizumab, pediatric new-onset T1D, *Diabetologia* 09-10. Level 1b on a tracked therapy | Unread | Read |
| F-11 | 09-11 | **PMID 42607698** — ACHIEVE-J Ph3, *Lancet D&E*. Independent companion to ATTAIN-2; the cheapest route to a defensible orforglipron tier | Unread, promoted to top 09-11 | Read |
| F-12 | **09-12** | **Islet Transplant × GWAS/Polygenic** is classified "methodologically distinct, deprioritize" but **PMID 42722448** (*JCEM*, 09-11) sits on it | Open, **[Likely]** — domain-string match unconfirmed | Classification re-tested against the script's strings |
| F-13 | 09-11 | **Vertex zimislecel** is a **12-patient Phase 1/2 (SILVER)**, not the Phase 3 the superseded doctrine text claimed | Corrected 08-31; watch open | Regulatory filing announced or watch retired |

---

## B. Open findings — methodological (about the hub's own numbers)

| ID | Found | Finding | Status | Closes when |
|----|-------|---------|--------|-------------|
| M-01 | 09-09 | **Gap #3 joint-publication count** carried four values: 0 / 1 / 2 / 7 | **RESOLVED 09-12.** Script's verbatim strings give **0**; domain counts 253/621 reproduce exactly. The 1/2/7 were unrecorded ad-hoc queries | — |
| M-02 | **09-12** | **Gap #3's 0 is partly a terminology artifact.** `"islet transplantation"` returns 2 all-time where `"islet transplant"` returns 0. A gap score of 100.0 on a joint count of 0 is softer than BRONZE implies | Open | Domain strings widened and gap scores re-derived |
| M-03 | 09-01 | **Five of the top twelve gaps pair a domain against Health Equity**, a keyword-brittle concept. Circularity test unrun — **11 days** | Open. **`Analysis/Scripts/falsify_equity_gaps.py` already exists and has never been run** | Script run, results recorded |
| M-04 | **09-12** | **Gap numbering + tier conflict.** `build_drug_repurposing_islet.py` says "Gap #4, SILVER"; `literature_gap_report.md` says "Gap #3, BRONZE". Both artifacts ship. `gap_numbering_audit.json` exists and is unconsulted | Open | One identifier, one tier, across all artifacts |
| M-05 | 09-09 | **Gap counts are cited without recording the query string** (defect #9) | Resolved for Gap #3 only; 434 pairs remain | Query string pinned next to every count |
| M-06 | 09-10 | **`LastUpdatePostDate` history is not reproducible** — a day-bucket reads 0 on D, peaks D+1, then decays | Rule holds and must never be violated. **Mechanism unknown** (event-driven explanation withdrawn 09-11) | Never — this is a standing rule, not a task |
| M-07 | 09-11 | **No `estimand` field anywhere in the trial schema.** Two people can cite one arm as 9.6% and 10.5% and both be right | Open | Field added; ATTAIN-2 backfilled |
| M-08 | 09-11 | **Findings are not carried forward between reports** (meta-defect #14). ATTAIN-2 was the third instance in 11 days | **This file is the fix.** Partially retired | This file is re-emitted in 3 consecutive runs |

---

## C. Open findings — evidence-quality standing cautions

| ID | Found | Caution | Status |
|----|-------|---------|--------|
| E-01 | 09-08 | **No primary web source has been fetched in any run since 09-08.** All FDA, Lilly, Novo and Zealand claims rest on search summaries | Open, 5 days |
| E-02 | 09-11 | **PMID 42577069 is not independent evidence for ATTAIN-2** — same patients, post hoc subgroup. Counting it violates Doctrine Lesson 7 | Standing caution |
| E-03 | 09-11 | **ATTAIN-2 participant-flow discontinuations are not drug-discontinuation rates.** 3/322 AE discontinuations at top dose is implausible as a tolerability figure | Standing caution — **do not quote as tolerability** |
| E-04 | 09-11 | **Bucket readings inherited across reports are not re-verifiable.** If a prior column was mislabelled, downstream deltas are wrong undetectably | Standing caution |
| E-05 | **09-12** | **"234 invisible records" is a count, not a reading.** It claims no collector query can see them — not that 234 are interesting | Standing caution |

---

## D. Open defects — hub machinery

Condensed from the daily defect table. Age as of 2026-09-12.

| ID | Defect | Age | Fix |
|----|--------|----:|-----|
| D-11 | **Terminal statuses absent from collectors. Re-scoped 09-12: the hole is 234 records, not 34 — and 22 of 22 in the T2D Ph2–3 lane** | 11d | Add terminal statuses **and** anchor collector #5 on `LastUpdatePostDate`, not `ResultsFirstPostDate` |
| D-17 | **Watches keyed on `ResultsFirstPostDate` cannot fire on completion** | new | Re-key on `OverallStatus`; alert on the first of the two events |
| D-06 | **Freshness gate queries D+0, which always reads 0** — returns FAIL every day by construction | 4d | Query D−1. One date offset |
| D-13 | **Amylin class uncovered** in `therapy_hits` and all 16 alert queries — 131 papers all-time, 4 trials completed this week | 2d | Add `petrelintide`, `cagrilintide`, `amycretin`, `CagriSema`; add an alert query |
| D-12 | **retmax ceiling discards 85.9%** of matching records | 11d | Raise and page, *before* re-running `baseline_pubmed_alerts.py` |
| D-01 | `clinical_trials_latest.json` is a 57-day-old duplicate | 57d | Fixed by running the collector (after D-11) |
| D-16 | **Dashboard builders repaired 09-09/09-10, never executed; `origin/main` frozen 145 days.** Live site still cites a registry cohort study as the IDF Diabetes Atlas | 3d | Run the three verify scripts; commit; push |
| D-02 | `has_results` constant `False` | 6d | Add `HasResults` to `fields` **and** read `study.get("hasResults")` |
| D-04 | Epigenetics + Drug Repurpose alert queries over-filtered | 4d | Drop the trailing AND-clause |
| D-07 | Scheduled run precedes the daily registry batch | 4d | Move the schedule; same root cause as D-06 |
| D-10 | 41-day trial-snapshot hole (07-18 → 08-26) | 3d | Cannot be backfilled; document it |
| D-03 | Null `title` on PMID 42698931 | 6d | One-record patch |
| D-05 | `phase` uses two null encodings, `"NA"` and `"N/A"` | — | Normalize |
| D-19 | **Sandbox mount failed 5 consecutive days** (2026-09-08 Windows update). No Python since 09-07 | 5d | Blocks every item above that needs a script run |
| D-20 | Tracker lock-held since 09-01; backlog 11 days | 11d | Close `.~lock.Diabetes_Research_Tracker.xlsx#` |
| D-21 | 09-07 test residue: `_wtest.txt`, `.wtest`, `.gap_checkpoint.json.testbak`, `.gap_checkpoint.json.__unlinktest` | 5d | Delete |
| D-22 | `CONTRIBUTION_STRATEGY.md` 181 days old, predates the 08-31 doctrine edits | 181d | Refresh |

---

## Closed

| ID | Finding | Closed | Resolution |
|----|---------|--------|------------|
| M-01 | Gap #3 joint count conflict (0/1/2/7) | 2026-09-12 | Script's verbatim strings give **0**; domain counts 253/621 reproduce the report's table exactly. The other three values were hand-run queries with unrecorded strings. Superseded by M-02, which questions whether 0 is the right number at all. |

---

## Update 2026-09-30 (local session)

This file was not re-emitted between 2026-09-12 and today, which is the defect
it was created to prevent (M-08). Sections A–C above are unchanged and were
**not re-verified** today; treat their ages as 18 days older than printed.

### Closed today

| ID | Finding | Resolution |
|----|---------|------------|
| D-16 | `origin/main` frozen | Pushed from the owner's machine; publish gate green. |
| D-01 | `clinical_trials_latest.json` stale | Refreshed (907 trials). |
| D-02 | `has_results` constant `False` | `HasResults` requested; `study.get("hasResults")` read. 356 of 907 now true. |
| D-05 | `phase` two null encodings | Registry `["NA"]` normalised to `N/A`. |
| D-13 | Amylin class uncovered | Alert query added; `cagrilintide`, `amycretin`, `petrelintide` tracked, plus `efsitora` and `finerenone`. |
| D-19 | Sandbox mount failure | Ended 2026-09-15 per the 09-21 report. |

### Narrowed, not closed

| ID | Finding | State |
|----|---------|-------|
| D-11 / D-17 | Terminal statuses absent from collectors | Trials in the prediction ledger are now fetched by identifier whatever their status (NCT06534411, COMPLETED, no results, is visible again). The general hole — completed trials without results in the T2D Phase 2–3 lane — is unchanged. |
| F-06 | CagriSema completion cluster | NCT06534411 visible via the ledger watch; NCT06323161 and NCT06797869 still are not. |

### New

| ID | Finding | Closes when |
|----|---------|-------------|
| N-01 | ~~Bayesian path ranking does not survive a recompute~~ **Closed 2026-09-30: withdrawn (owner decision A).** Root cause: validation lookups never matched (key format), counts were regex artefacts, and a recompute read a renamed field. Replaced on the Statistical Analysis page by a table of each path's reconciled status, live evidence count and study design, explicitly not a ranking. `posterioragree` stage retired. | — |
| N-02 | ~~Gap #11 unruled~~ **Closed 2026-09-30: SILVER** under Lesson 9. Absence: PubMed + registry report and bibliography. Premise: recipients 98% White of recorded race vs national type 1 prevalence by race (PMID 30181166), with the comparison's limits stated on the page. | GOLD needs a third independent source (Embase or conference abstracts). |
| N-03 | ~~12 uncited endpoint values~~ **Closed 2026-09-30: 0 remain.** Each sourced, corrected or removed; see run report section 9. | — |
| N-09 | **Gap #3 (Insulin Resistance in Islet Transplant, GOLD) published a key finding with no source, contradicted by the one human clamp study** (PMID 24085506: insulin sensitivity improved after transplant). Finding removed 2026-09-30. Gap #3 has not been re-tiered under Lesson 9 (absence claims). | Owner reviews #3 under Lesson 9: what has been searched, and is the premise sourced? |
| N-04 | `build_islet_outcomes.py` attributes "20% at 10 years" to CITR annual reports and a 1,477-recipient registry. 20% at 10 years is the Edmonton single-centre estimate (n=255, PMID 35588757). **[Likely]** misattributed; CITR reports not read. | CITR report read. |
| N-05 | Tier is hardcoded in 39+ places and read from the store in none. Reconciled by hand today; it will drift again. | Builders read one store. |
| N-06 | FDA approvals of finerenone (T1D CKD) and efsitora are reported from press coverage only and marked `[UNSOURCED]` in the findings summary. Continues E-01. | One fda.gov or sponsor document fetched for each. |
| N-07 | Windows task `DiabetesHub_GapAnalysis` points at a deleted script; unattended publishing has no path. | Owner runs `register_daily_task.ps1` and chooses how pushes happen. |
| N-08 | AZD1656 row in the GKA table says "Phase 3 (tachyphylaxis) … Development ongoing" with no source. Not checked. | Checked against the registry. |

---

*Maintained by the Diabetes Research Hub monitor. Re-emit verbatim each run; append, never silently drop.*
