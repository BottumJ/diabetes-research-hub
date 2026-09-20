# ACTION REQUIRED — 2026-09-20

## The one thing only you can do

**`git push`.** Everything below is committed and green in the working tree. None of it
is on the site.

```powershell
cd C:\Users\justi\OneDrive\Diabetes_Research ; git push origin main
```

- 116 commits unpushed. `origin/main` tip is **2026-04-20 — 153 days old**.
- 38 of 39 files under `docs/` are wrong for a real reader (4 return 404, 34 are stale).
- The commit path itself is no longer blocked: this run renamed two stale lock files and
  committed normally (`e988bbc`). Only the push lacks credentials.

A second, smaller ask is at the bottom: a **one-line edit to the scheduled task file**,
now on its ninth day of asking, which is actively generating false work.

---

## What this run found

Three defects. All three were invisible to 80+ green stages for the same reason, and the
reason is worth stating once because it predicts where the next one will be:

> Every gate in this repository checks the **content** of an assertion against the words
> beside it. All three of today's defects were defects of **form** — a correct rule stored
> in a shape no gate was reading.

### 1. A blank field deleted three primary studies

`corpus_membership.py` says, in its own source:

> `UNCLASSIFIED = 'FLAGGED_UNCLASSIFIED'` — *"A FLAGGED paper with no membership_class is a
> bug, not a default."* … *"Should always be empty; an audit fails on this rather than
> letting a consumer guess a meaning."*

**That audit did not exist.** `unclassified()` had no caller anywhere in the repo. So the
module used the missing field *as* the default, and on 2026-09-19 a reconcile run deleted
four papers from the index. The eviction ledger records the reason verbatim:

> `"FLAGGED in agent_state.json with no class recorded"`

A blank field, offered as the justification for deleting three primary human studies:

| PMID | What it is | Why it was flagged |
|---|---|---|
| 34021020 | DIAGNODE-2 — Phase IIb double-blind RCT, *Diabetes Care* 2021, n=109 | a page called a **type 1** trial a **LADA** trial |
| 25940230 | PREDIMED overview, *Prog Cardiovasc Dis* 2015 | a page published the **CVD** hazard as the **diabetes** number |
| 37026004 | CITR HLA-DR registry analysis — state calls it **load-bearing for Gap #11** | its own record reads *"Flagged, not rejected — the finding stands, the framing did not"* |
| 42674789 | Quebec cohorts — **study protocol, no results** | correctly excluded from evidence |

Every gate here writes its findings back as `status=FLAGGED`. So **correcting a paper's
prose is what removed the paper from the corpus.**

All four were cited on live pages the whole time, while `corpus_membership` answered
`citable() == False` for them — because **`citable()` also had zero call sites.** A module
declaring a paper uncitable while the site cites it is not a gate, it is a comment.

**Fixed:**

- Added a `CORPUS` class so a repair note can be recorded without becoming a disqualifier.
- Classified all four from their own vetting records (3 CORPUS, 1 BACKGROUND). All four
  PMIDs re-verified live against NCBI the same day.
- **Eviction now requires an affirmative code.** Exclusion is reversible — the record
  survives and tomorrow can reverse it. Deletion leaves nothing to reverse. A blank field
  is a question, and a question must never be answered by destroying the thing it is about.
- New gate `audit_flagged_membership_class.py`, wired into the pipeline, asks both
  unasked questions. Its first draft produced six hits and **all six were false positives**
  (repair comments, and the rejection-ledger page doing its job); both exemptions are
  structural rather than a filename list, and the gate is proven in both directions by a
  permanent fixture, `probe_flagged_membership_gate.py`.
- Found and fixed a **sixth divergent membership loader** inside `reconcile_paper_index.py`
  itself — the one file that already imports `corpus_membership` for eviction was still
  hand-rolling the topic screen, and had just labelled a *Diabetes Care* Phase IIb RCT
  `OFF_TOPIC`, quoting its own repair note as the evidence.

### 2. Two published pages carried 14 gap titles this hub does not study

`build_extracted_evidence.py` and `build_research_paths.py` each held a byte-identical
hard-coded gap registry. Against the canonical store:

**14 of 15 titles disagreed. 9 of 15 tiers disagreed. Only Gap #1 matched on both.**

Not drift — a different set of research questions. A reader of Extracted_Evidence.html saw:

> **Gap 11: Immunomodulation in Type 2 Diabetes — BRONZE — 39 points**

…above correctly extracted, correctly cited dorzagliatin / MK-0941 / TPP399 / PB-201 odds
ratios. Canonical Gap #11 is **Islet Transplant Registry Equity, GOLD**. Real numbers,
real PMIDs, filed under a question this project does not ask. Zero canonical gap names
appeared on the page at all.

`audit_gap_numbering.py` reads the prose form `Gap #N (TIER)` with a regex. **A dict
literal is not a sentence**, so the file was invisible to the one audit whose entire job is
gap-numbering agreement — while that audit reported confidently on the four stores it does
read.

**Fixed:** taught the audit the dict form. It went from **4 stores to 69 hardcoded tier
sites across 15 gaps** — and the *second* stale registry was found only by that change,
which is the argument against hand-correcting the first one. Both builders now read the
canonical store and carry no answer of their own. Verified end-to-end: the phantom titles
are gone from `docs/`, the canonical names are present, and the heading now reads
*"Gap 11: Islet Transplant Registry Equity."*

### 3. Gap #11's open question, answered from full text — and the answer is *no*

Queued 2026-09-07, open 13 days: *does the CITR HLA-DR analysis report recipient race or
ethnicity at all?* The full text (PMC10070978) was on disk the whole time.

**No.** In 39,486 characters — including the complete Table 3 baseline and the full 19-row
potential-confounder table — the paper contains **zero** occurrences of *race, ethnicity,
Hispanic, Black, African American, Caucasian,* or *demographic*. It reports % Female, age,
BMI, donor gender and cause of death.

So the Gap #11 equity intersection is not merely unevidenced in this corpus — **the
load-bearing paper cannot evidence it, because it never collected the variable.** That
settles the item's own framing: this needs a CITR data request, not another PubMed sweep.
Two real options are now filed at priority 1, and **option (b) is defensible today with no
data request**: restate the gap as what the evidence supports — that the registry does not
*publish* recipient race — which is itself an equity finding, and a stronger one than an
inferred disparity.

*Secondary finding, recorded because it bears on how the paper may be cited at all:* group B
(n=11) is better matched at HLA-A (73% vs 48%) and HLA-B (45% vs 17%) than group A, and
neither variable appears in the paper's confounder table. The authors' own group D vs E
comparison (≥3 vs <3 average A,B,DR matches; insulin independence p=0.8) argues against
general matching explaining the result — a real defence. But maintenance immunosuppression
with mTOR+CNI differs **90% vs 14% at p=0.2**, and a 6.4-fold difference reported
non-significant on n=11 is a power artifact, not evidence of comparability. Any downstream
use must carry n=11 and must not be phrased causally.

---

## A backlog that turned out to be zero

The queue carried *"INDEX THE 17 PAPERS WHOSE FULL TEXT IS ALREADY ON DISK"* at priority 1.
`repair_index_pmcid_map.py` now splits that count through `corpus_membership` instead of
printing it undifferentiated:

| | |
|---|---|
| Excluded **on purpose** — index correct, file on disk is residue | **16** (8 PROVENANCE, 5 OFF_TOPIC, 1 RETRACTED, 2 BACKGROUND) |
| Genuinely missing | **1** — PMID 37026004, fixed above by classification |

**Ingestion backlog: zero.** The item was sized from a number that could not tell a
deliberate exclusion from an accidental one.

---

## Second ask: one line in the scheduled task file

Step 4 still instructs a sweep for *"PMIDs above 42000000 (fabricated)."* Measured live
today:

| | |
|---|---|
| Real PubMed ceiling | **42,763,307** |
| Correct flag line (`pmid_ceiling.py`) | **43,013,307** |
| Highest PMID anywhere in this repo | **42,698,953** — a real paper |

That genuine 2026 citation sits **698,953 above the task file's line** and **314,354 below
the correct one**. Anyone following the task file literally would open a fabrication
investigation into a real paper. The repo fixed this on 2026-08-25/31; the task file has
carried the stale rule since. Ninth day of asking.

---

## Pipeline status

All stages green except two that are **red on purpose**:

- **`publishgate`** — fails because `origin` is 153 days stale. It is reporting the push
  blocker at the top of this document. A pipeline that reported a successful publish it did
  not perform would be the defect; the red stage is the fix.
- **`gapsubject`** — the standing Gap #14/#15 tier question (both BRONZE with zero evidence
  papers) plus the Gap #7/#11/#13 intersection findings. Now on its sixth asking, and today
  made the edit *bigger*: the tier is written in **69 places**, not the 24 previously
  counted. Do not hand-edit 69 sites — demote in the canonical store and convert the
  renderers to read it, which is the same work item as the dict-literal sweep.

`membershipgate` failed mid-run on `repair_index_pmcid_map.py` (unguarded since yesterday,
unrelated to today's changes) and is now green.

---

## Doctrine note filed today

> **A gate that names its own missing enforcement is not enforced.**
>
> `corpus_membership.py` contained both the rule and the remedy in its own source — and the
> audit did not exist. The docstring read as if it did, which is worse than silence: it made
> every reader of that module, human and agent, believe the check was running. Two of the
> three defects found today were of this form.
>
> **The test to apply:** for every invariant a module *describes*, grep for a caller of the
> function that checks it. A documented invariant with zero call sites is a comment.
>
> **Second, narrower rule:** exclusion and deletion must not share a predicate. Deletion
> must require an affirmative adjudication and must never be triggered by the *absence* of
> one.
