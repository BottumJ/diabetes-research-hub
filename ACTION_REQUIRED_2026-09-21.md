# Action Required — 2026-09-21

**Two items need you. Both are one command. Everything else this run is done and committed.**

---

## P0 — Push. 118 commits, 154 days.

```
cd 'C:\Users\justi\OneDrive\Diabetes_Research' ; git push origin main
```

`origin/main` still points at 2026-04-20. Nothing this agent has produced since
then exists for a reader. Measured again this run: `git push --dry-run` →
`fatal: could not read Username for 'https://github.com'`. The sandbox has no
credential helper, no `~/.git-credentials`, no `GH_TOKEN`. **Commit** works
(this run committed `f6d0db4`); **push** is the only thing that does not.

Provisioning a PAT for the scheduled task retires this item permanently.

**Why it matters more today than yesterday.** This run removed an invented
clinical figure — *"belatacept: 70% graft survival at 10 years"* — from four
builders and from the two dashboard copies on disk. **A reader on the live site
is still being shown it**, and will be until you push.

---

## P0 — The scheduled task file's Step 4 nearly deleted real data today.

Step 4 instructs a sweep for *"PMIDs above 42000000 (fabricated)"*. That rule
expired when PubMed crossed 42 million. The live ceiling is **42763307**.

**All five papers ingested this morning are above 42000000 and all five are
real** — identities confirmed against PubMed before ingestion. An agent
following the task file literally would have deleted them as fabrications.

The repo fixed this in August (`pmid_ceiling.py` resolves the ceiling live).
The task file cannot be edited from here, so every run re-reads the stale
instruction and re-derives that it is stale. Two edits:

- **Step 4:** replace the `42000000` literal with *"run
  `Analysis/Scripts/audit_impossible_pmids.py`, which resolves the live ceiling"*
- **Step 1:** the "vet 10–15 unvetted papers" loop is finished — 342 of 372 are
  VETTED and only the 5 ingested today are unvetted. It generates make-work now.

---

## What this run did

**Corrected a fabricated clinical figure that existed in four places.**
Wisel et al. 2023 (PMID 37359825) is **ten** patients — five on belatacept,
five on efalizumab. It reports **70% insulin independence at 10 years for the
pooled group** (four efalizumab, three belatacept) and **60% at 13.3 years for
the same ten people**. It reports no per-drug rate.

The hub had published:

| Published | Why it is wrong |
|---|---|
| "Belatacept 70% at 10yr, Efalizumab 60% at 13.3yr" | One cohort at two timepoints, re-read as two drugs. Belatacept got the better number despite contributing **fewer** of the responders (3 vs 4). |
| "6/10 insulin-independent at 10 years" | The 13.3-year numerator on the 10-year endpoint — so one file stated **two different 10-year values** for one paper. |
| "70% graft survival at 10yr vs 32% with tacrolimus" | No such figure exists. Graft survival ≠ insulin independence. The "32%" is the Edmonton **5-year** rate, relabelled. |
| Same claim, "vs 50%", cited to PMID 16120857 | That paper is a **renal** trial vs **cyclosporine**, endpoints **6 and 12 months**. No 10-year data, no 70, no 50. |

Three files gave three different tacrolimus comparators for one number. That
disagreement is what exposed it.

**None of ~85 green gates could see any of this.** Every gate scores *one*
assertion against *one* source, and each statement passed individually. A
contradiction is not a property of a single claim.

**Also ingested 5 papers** (Monday sweep), **screened out 3** with reasons, and
**closed 7 of 9 P0 queue items** as stale — four described a sandbox outage that
ended on 2026-09-15, three were duplicate push requests. Tested by command, not
inherited from a report.

---

## Two things this run got wrong, and fixed

Recording these because they are more useful than the repair.

**1. The first repair verified itself.** It fixed one instance, then confirmed
success by grepping for *the strings it had just written*. That test can only
confirm the edit — it cannot find a fifth copy. It returned clean while the
same fabrication was live in three other builders. An adversarial re-check,
run specifically to falsify the claim, found them.
→ **Verify the claim, not the edit.**

**2. The new gate printed `[FAIL]` and returned exit code 0.** The pipeline
dispatches on the return code, so it logged `[OK]`. For its entire first life
it could not fail anything. Fixed, and re-tested in both directions.
→ A queue item now asks for **every** audit script to be checked the same way.
If another has this bug, its green line in every past run report was worth
nothing while reading as assurance.

The gate also had real false positives — it keys on *(source, timepoint)* and
never parses *what is measured*, so "61% at 5 years in adults" vs "32% at 5
years in children" registered as a contradiction. Filtered now, but a heuristic
that works *most* of the time must not fail a build. So the gate is split: the
**ratchet fails** (mechanical — a citation is on the line or it is not), the
**conflict check only reports**.

---

## The number worth watching

**Of 46 clinical endpoint-values in builder source, 4 carry a citation on the
same line. 31 carry none.**

"Belatacept 70% at 10yr" was never mis-cited. **It was never cited.** That is
the condition that let it survive for months, and it is the condition almost
every clinical percentage on this hub is still in. The ratchet now blocks new
ones and moved 35 → 31 today. The backlog is queued.
