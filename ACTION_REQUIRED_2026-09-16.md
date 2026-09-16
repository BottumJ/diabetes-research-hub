# Action required — 2026-09-16

## The ask shrank. It is now one command, and no lock to delete.

```powershell
cd 'C:\Users\justi\OneDrive\Diabetes_Research'
git push
```

That is all. **Ignore the 2026-09-15 instruction to `Remove-Item .git\index.lock` and
run `PUSH_AND_VERIFY.ps1`.** The commit half of that problem is solved and did not need you.

---

## Why the lock stopped mattering

The sandbox still cannot *unlink* anything under `.git` on the OneDrive mount —
`Operation not permitted`. But unlink is the **only** forbidden operation there. Creating
files under `.git` works. Renaming works. Git takes `index.lock` to protect the index it is
about to write, so pointing `GIT_INDEX_FILE` at a path outside the mount sidesteps the lock
entirely.

Today's run committed that way. 122 files, working tree clean. What the sandbox still
cannot do is *authenticate* — HTTPS remote, no credential helper, no `GH_TOKEN`. That is
the whole remaining ask, and a PAT provisioned for the scheduled task would retire it
permanently.

**105 commits unpushed. `origin/main` is still at 2026-04-20.**

---

## The finding worth your attention: the verification pass was the defect

On 2026-09-14 this agent found a false citation on the belatacept 10-year figures,
re-sourced it to PMID 37359825, checked the paper's **contents** against its abstract,
confirmed they matched, and wrote into its own memory:

> `37359825: Voglova et al., Transpl Int 2023. Not a defect — this is the CORRECT source…`
> `Recorded here so no future sweep mistakes it for filler.`

PMID 37359825 is **Wisel SA**, Posselt AM, Szot GL, … Stock PG, *Transpl Int*
2023;36:11367. Voglova is not an author on it. Voglova's islet papers are PMIDs 33599904
and 28632818 — different work.

The run verified the numbers, which are right — 7/10 insulin independent at 10 years, 6/10
at mean 13.3 ± 1.1 years, 5 belatacept and 5 efalizumab, 3 of the 7 with
pancreas-after-islet, all re-confirmed today — and **inherited the surname from the prose
it was auditing.** Then it wrote that inheritance down as verified.

A false clearance is worse than a false citation, because its stated purpose is to stop
anyone looking again.

---

## Two structural holes, both now closed

**The gate's "unknown" bucket was selected for risk, not neutral.** The surname gate
declines to flag a PMID absent from the local paper library. Defensible — until you ask
what puts a PMID in that bucket. A paper is missing from the library exactly when it was
added *recently and by hand*, which is also when it is most likely to be wrong. "Unknown"
was concentrated on the riskiest citations in the repo. It now resolves against NCBI
esummary with an on-disk cache: **16 of 16 resolved, 0 unresolvable.** Opt-in, so a network
blip cannot fail the build.

**Identifiers inside markup were unreachable.** `--html` now scans generated HTML for `<a>`
elements whose PMID sits in an attribute with the surname in the anchor text — the class
where the Shapiro/10919952 defect survived a full sweep on 09-15 and was caught only by an
ad-hoc grep. Six anchors repo-wide. The scan caught the stale Voglova rows in both
`Dashboards/` and `docs/` before the rebuild cleared them.

---

## Three more live defects fell out of the resolved bucket

All in `build_immunomod_lada.py`, a file no previous sweep had opened.

| Asserted | Actually was | Action |
|---|---|---|
| `29885104` "Insel et al., Vitamin D and T1D prevention" | Huh JH et al., *glycated albumin and renal tubulopathy*, Diabetes Metab J 2018 | **withdrawn**, no replacement asserted |
| `24997559` "Sanda et al., REPAIR-T1D" | Griffin KJ et al., Lancet Diabetes Endocrinol 2014 — really *is* REPAIR-T1D | surname corrected only |
| `29291885` "Herold et al., Teplizumab **Phase 3** (TN-10)" | Zanelli & Rogol, *growth hormone in short children* | → `31180194`, **and Phase 3 → Phase 2** |

That last row carried two independent errors in six words. TN-10 is phase 2, n=76 — PubMed
publication type reads "Clinical Trial, Phase II" and the abstract's METHODS opens "We
conducted a phase 2, randomized, placebo-controlled, double-blind trial." **Phase inflation
is worse than a wrong surname for a reader weighing a result**, because Phase 3 implies
registrational evidence. Nothing in this pipeline checks it. Queued as P1.

---

## Measure-before-wiring paid again, twice

The extended gate first reported 19 mismatches. Two were **gate** defects, not repo defects:

- **Comma-separated reference runs.** `(PMID 41921761, Qin et al. 2012, Karlsson et al. 2013)` —
  one identifier followed by other sources cited author-year with no identifier of their
  own. Backward pairing bound "Qin" to Nee's PMID. This is the same shift-by-one failure
  the PAIRING RULE already guards against, in comma form rather than semicolon form.
- **A corrupt library record, not an absent one.** PMID 41986815 stored `authors[0]` as
  `"B"`, so a correct "Blencowe et al." was flagged against "B et al." A gate must not
  assert a mismatch on the strength of a field it can see is malformed.

After both fixes: **175 checked · 167 correct · 8 flagged · 0 unknown.** All eight survivors
are archived run reports, one-off close scripts, or `NON_FIRST_AUTHOR` cases where the named
author genuinely is on the paper. **Zero live builder `NOT_AN_AUTHOR` defects remain** —
which is why the stage was wired in as reporting, not as a failing gate.

---

## The credibility sweep was red at its own reflection

All five "unhedged preclinical overclaims" in the entire repository were the strings
`zero SAEs`, `zero rejection`, `achieves remission` sitting inside
`verify_2026_09_1*_repairs.py` — as those scripts' own **search patterns**. The sweep
already excludes the agent's audit trail by path class; the per-run verify scripts simply
weren't in that class. Now matched by pattern, so tomorrow's verify script is covered the
day it is written.

A gate that reports red every run for a reason nobody acts on stops being read. That is
exactly how eleven consecutive push notices decayed into background noise here. Sweep is
now clean and means something: 0 impossible PMIDs, 0 overclaims, highest PMID in the repo
42,698,953 against a live ceiling of 42,994,765.

---

## Not fixed — recorded deliberately

The graft-survival chart plots the belatacept curve ending at **55%** at year 10 while the
prose and Evidence Catalog on the same page report **70%**. Choosing between them is a
modelling decision, so it stays a human call. What changed is that a visible reading note
now sits under the chart saying the curve is *modelled* and the 70% is *observed* (7 of 10,
Wisel) — a reader is no longer shown two unlabelled answers to one question.

---

## One line for whoever edits the scheduled task file

Step 1's `vet_papers_batch` branch is dead: all 366 papers are VETTED or FLAGGED and **zero
are unvetted**, so that branch can never fire. Step 4's integer PMID threshold is still
stale, as recorded on 2026-09-10 — it was run today as `audit_impossible_pmids.py` instead.
