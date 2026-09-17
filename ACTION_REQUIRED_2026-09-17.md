# Action required — 2026-09-17

## Still one command. It has not changed since yesterday.

```powershell
cd 'C:\Users\justi\OneDrive\Diabetes_Research'
git push
```

**109 commits unpushed. `origin/main` is still at 2026-04-20.** The sandbox can commit
but cannot authenticate — HTTPS remote, no credential helper, no `GH_TOKEN`. A PAT
provisioned for the scheduled task retires this permanently.

---

## Before you push: a landmine was sitting in the index, and it is now defused

`git status` this morning reported **87 files staged**, including deletions of files
that were present on disk — both `ACTION_REQUIRED` notes, two agent-state backups, two
run reports. `git diff --cached` totalled **39,594 deletions**. Any `git commit` run in
that state would have carried them out.

The cause is yesterday's own workaround. The 2026-09-16 run committed by pointing
`GIT_INDEX_FILE` at a path outside the mount, which is correct and clever — but it left
`.git/index` untouched at its stale 2026-09-15 contents. The index and HEAD then
disagreed, and the disagreement reads as staged deletions.

Rebuilt from HEAD using only renames (unlink is still the one forbidden operation on
this mount). Status is now truthful: **11 changes, 0 staged deletions.** The two phantom
branches in `refs/heads` left by five months of lock-renaming were also moved out.

Nothing was lost. `git push` was never the dangerous command; `git commit` was.

---

## The finding: a builder in this repository has not parsed since yesterday's commit

`Analysis/Scripts/build_gap_deep_dives.py` is **syntactically invalid at HEAD**. Line 982
holds a correction note that pastes the text it replaced, in double quotes, inside a
double-quoted string:

> `... This note first read "all seven ... in this gap record" and was corrected ...`

It was introduced by commit `ea91a26` — **the 2026-09-16 run, whose report states that
the rebuild cleared stale rows from this dashboard.** It cannot have. The file does not
execute, so `Gap_Deep_Dives.html` has been frozen at its last good build while seven
correction passes went on editing the source that generates it.

Two things are worth separating here.

**Nothing in this repository could see it.** Every gate built over five months checks the
*content* of an assertion — does this PMID exist, is the surname right, is the number
sourced. Not one checks whether the file making the assertion can run. So the most
complete failure available, a builder producing no output whatever, was the only one
invisible. `audit_builders_compile.py` now runs first in the pipeline: 143 files, under a
second, and zero possible false positives, because a file either parses or it does not.

**The habit that caused it is this project's own care.** Correction notes here are long,
they quote the text being replaced, and they live inside string literals. That is exactly
the practice that produces unescaped quotes. The more carefully a run documents a repair,
the likelier it is to break the file it is repairing.

---

## The new gate found nothing. Its unknown bucket found four things.

`audit_trial_phase.py` compares every "Phase N" asserted next to a PMID against what
PubMed says that paper is. Final measurement: **39 pairs · 29 correct · 0 flagged · 10
unknown · 11 ambiguous.**

Zero flagged. All four of today's live defects came out of the **unknown** list — the
papers the gate could not decide about. That is the lesson, not the gate.

### 1. Yesterday's repair did not sweep its own file

`build_immunomod_lada.py:83` still read `"Phase 3 TN-10 trial (PMID:29291885)"`. The
2026-09-16 run fixed the identical defect ~280 lines below in the same file and left this
one live for a day. Three errors on one line:

| Asserted | Actually |
|---|---|
| PMID 29291885 | Zanelli & Rogol, growth hormone in short children. TN-10 is **31180194** |
| Phase 3 | TN-10 is **phase 2**, n=76 |
| FDA approved 2023 | Tzield approved **17 Nov 2022** |

This is the 2026-09-09 correction-scope defect — repairs scoped to the passage that
triggered them rather than to the file — recurring *on a correction*.

### 2. Three studies fused under a trial name that does not exist

`build_gap_deep_dives.py` published:

> Dorzagliatin Phase 3 (DAWN-1, n=360): HbA1c −1.07%, TIR 83.7%, 65.2% remission
> (HbA1c <5.5% off metformin) (PMID:36449148)

Every element of that is wrong.

| Element | Reality |
|---|---|
| "DAWN-1" | Not a trial. SEED (n=463, PMID 35551294) and DAWN (n=767, PMID 35551292) |
| n=360 | Matches neither |
| −1.07% | SEED's monotherapy figure. DAWN's was −0.66% placebo-adjusted |
| 65.2% remission | Kaplan–Meier *probability* at 52 wks in a 69-patient drug-free cohort (PMID 37385967). The same paper reports **52.0%** by the ADA definition |
| TIR 83.7% | SEED CGM substudy, **n=16** |
| "off metformin" | SEED is drug-naïve; the cohort was off *all* medication |
| PMID 36449148 | Syed YY, "Dorzagliatin: First Approval", *Drugs* 2022 — a **Review** |

All re-sourced with denominators now visible in the published text.

### 3. A trial design that was never run

`build_gka_landscape.py` published "DAWN trial tested the combination of dorzagliatin
with **empagliflozin**", with an uncited result of "additive HbA1c reduction with
favorable safety profile". DAWN is dorzagliatin **add-on to metformin**. Empagliflozin
does not appear in it.

`build_gka_pricing.py` and `build_gka_lada.py` both described DAWN correctly — so the
site published two incompatible definitions of the same trial. The uncited result
described a study that does not exist and was **withdrawn, not replaced**.

### 4. A fifth load-bearing concentration

**PMID 21323736** — Beckwith J et al., *Clin Transplant* 2012 — is a Markov-model
cost-effectiveness analysis of **cadaveric** islet transplantation. It reports exactly
five money figures: $663,000, $519,000, $71,000/QALY, $47,800/QALY, $240,000 break-even.

It was carrying: CAR-T dose prices ($170–220K and $300–500K), cGMP facility build costs
($50–100M), per-procedure islet prices ($100–139K, $100K–300K), a pancreas-transplant
price ($300–408K), a copay figure, and a >$500K/patient price for Vertex's stem-cell
islet product. It contains none of them. It was also twice called "CITR registry
outcomes" — it is a model, not a registry.

**9 live attachments withdrawn or corrected across 5 builders.** The whole-file re-grep
caught 3 the passage-level pass had missed, which is the 2026-09-09 doctrine earning its
keep in the same run that saw it fail.

Note what this means for the concentration list: `citation_load_bearing.json` tracks
34763823 (91), 29710129 (81), 37909353 (47) and 32175717 (39) and **has never counted
21323736**. That list is not a census of the problem — it is a census of the PMIDs
someone happened to look at. Queued as P2.

---

## The clearance re-examination asked for yesterday

Seven records re-resolved against NCBI esummary, field by field, recording **which fields
were checked** — because fields not named are not verified.

- **5 clean** on every field named (17065674, 37105208, 34763823, 29710129, 22336824)
- **1 false**: 37359825 was recorded as "Voglova et al."; it is **Wisel SA** et al.
- **1 never checked on a field**: 37909353's record named no author at all

The important half: yesterday's run fixed the *files* carrying the Voglova error but left
the **state record** saying Voglova — and that record is what future runs read, and its
stated purpose was to stop them looking. It is corrected in place today, with the
original text retained for the audit trail.

---

## Measure-before-wiring paid a fifth time

The trial-phase gate's first run reported 5 mismatches. **All five were gate defects.**

- The resolver read phases out of papers' **bibliographies** — efetch returns
  `<ReferenceList>`, so a review was assigned the phase of a study it cited.
- It assigned phases to **Reviews, Letters and mouse studies**, which have none.
- It bound a phase to a PMID when the phase belonged to an **NCT id** in the same sentence.
- It read "Phase 2 constructed a feature-engineered dataset" — this project's own
  workflow stages — as trial phases.

Each is documented in the script as a named false-positive class so the next extension
does not reintroduce it. After the fixes: 0 flagged, and the known-positive test (the
TN-10 string) still fires.

---

## One line for whoever edits the scheduled task file

Unchanged from yesterday and still true: Step 1's `vet_papers_batch` branch is dead — all
366 papers are VETTED or FLAGGED, zero unvetted, so it can never fire. Step 4's integer
PMID threshold is still stale; `audit_impossible_pmids.py` was run instead (0 impossible,
0 overclaims, ceiling 42,994,765 against a repo high of 42,698,953).

Add one thing: the host caps a single sandbox command at roughly **three minutes**, and
background processes do **not** survive between commands. `run_quality_improvements.py`
cannot complete in one call and was run stage by stage today. Either the task file should
say so, or the pipeline needs a resumable driver.
