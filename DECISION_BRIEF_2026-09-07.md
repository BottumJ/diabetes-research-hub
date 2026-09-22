# Decision Brief — Monday 2026-09-07

**Lead finding:** nine of your fifteen research gaps are tiered on evidence that never
mentions the gap's own question. Three of those are outright mis-files. This was found
by chasing one suspicious gap and then asking the same question of all fifteen.

Nothing was demoted. Nine tier changes to the hub's headline claims is not an
unattended decision.

---

## 1. What broke, and how I know

Canonical **Gap #11 — Islet Transplant Registry Equity** is published GOLD. Its entire
evidentiary basis in `gap_evidence.json` is two papers:

| PMID | Paper | About equity? |
|---|---|---|
| 19104422 | 2008 Update from the Collaborative Islet Transplant Registry | No |
| 37105208 | Primary graft function vs 5-year outcomes, CITR, n=1210 | No |

Neither contains the words *equity, race, ethnicity, socioeconomic* or *access* anywhere
in its stored title or findings. An absence claim — "nobody has analysed islet transplant
equity" — was being carried by two papers that are not about the thing claimed absent.

**The correct evidence for an absence claim is a dated, reproducible search that returns
nothing.** Until today, no such search had ever been run for this gap.

### So I ran it

| Query | Window | Hits | Result |
|---|---|---|---|
| `islet transplantation AND (disparities OR equity OR inequity OR racial OR socioeconomic)[tiab]` | all time | 23 | 10 highest-relevance screened; **0** are equity analyses of islet transplantation |
| `"Collaborative Islet Transplant Registry"` | all time | 31 | **0** titled on equity, disparity, race or access |

The 23 hits are other people's fields: racial disparities in *living-donor kidney*
transplant, kidney allocation fairness, xenotransplantation consensus, global aortic
aneurysm mortality, pancreatic nerve anatomy.

**The gap survives.** Verdict VALID, confidence **[Likely]** — not [Certain], and the
distinction matters. What is supportable is *"no PubMed-indexed analysis of equity in
islet transplantation exists."* What is **not** supportable is *"no such analysis exists"* —
CITR annual reports, NIDDK data-request outputs and conference abstracts are grey
literature these searches do not reach. **Every publication of this claim must carry the
"PubMed-indexed" scope.** To reach [Certain]: read the CITR annual report scientific
summaries at citregistry.org and search Embase. Neither was reachable this run.

### Then I asked the same question of all fifteen

New gate: `Analysis/Scripts/audit_gap_subject_coverage.py`. Every gap here is an
*intersection* — an X domain crossed with a Y lens. Gap #11 is islet transplant × equity.
Its evidence covered X fully and Y not once, and nothing failed because nothing had asked.

```
GAP  NAME                                   TIER     PAPERS      X      Y   BOTH
 1   Gene Therapy for LADA                  SILVER       31      0     15      0   <-- HARD FAIL
 2   Health Equity in Diabetes              GOLD         13     12     13     12       ok
 3   Insulin Resistance in Islet Transplant GOLD         23     21      2      2       thin
 4   Drug Repurposing for Islet Transplant  SILVER       16     15      0      0   <-- judgement
 5   Treg in Diabetic Neuropathy            SILVER       17      4     15      2       thin
 6   CAR-T Access Barriers                  GOLD         15     15      6      6       ok
 7   GKA Drug Repurposing                   SILVER       18     17      0      0   <-- judgement
 8   Immunomodulatory Drugs for LADA        SILVER       27      7     15      0   <-- inference only
 9   GKA in LADA                            EXPLOR        0      0      0      0       honest
10   LADA Prevalence by Healthcare Setting  SILVER        1      1      0      0   <-- 1 paper
11   Islet Transplant Registry Equity       GOLD          2      2      0      0   <-- HARD FAIL
12   Generic Drug x Diabetes Mechanism      SILVER        8      3      7      2       thin
13   Personalized Nutrition for Beta Cells  BRONZE        3      0      0      0   <-- HARD FAIL
14   Personalized Nutrition for LADA        BRONZE        0      0      0      0   <-- tier w/o evidence
15   GKA Pricing Trajectory                 BRONZE        0      0      0      0   <-- tier w/o evidence
```

**X** = papers mentioning the domain. **Y** = papers mentioning the lens. **BOTH** = papers at the intersection.

### The three hard failures — verified by hand, not just by regex

I read the stored titles directly rather than trusting my own gate:

- **#1 Gene Therapy for LADA — SILVER on 31 papers, zero about gene therapy.** They are
  GAD-autoantibody affinity studies, ICA titre discrimination, Action LADA prevalence,
  C-peptide screening. The gap is rated on LADA epidemiology. [Certain]
- **#13 Personalized Nutrition for Beta Cells — BRONZE on three berberine trials.** All
  three are berberine in *type 2 diabetes* for glycaemic control and dyslipidaemia.
  Berberine is a plant alkaloid *drug*, not personalized nutrition, and none of the three
  concerns beta-cell preservation. This is a mis-file, not a thin evidence base. [Certain]
- **#11** as above. [Certain]

### Where my gate is weak, stated plainly

It detects the presence of a **word**, not of an **analysis**. Two consequences:

- **Passing is weak news.** One incidental mention lets a gap through.
- **#4 and #7 are judgement calls, not defects.** They fail on "repurposing" while citing
  anakinra, etanercept, rapamycin, dorzagliatin — drugs that *are* repurposed, in papers
  that never use the word. Whether drug-level evidence counts as repurposing-question
  evidence is your call, not the gate's.

It also reads only stored titles and finding snippets — no abstracts fetched. Misses are
an **upper bound**: a prompt to read the paper, not a proven defect. That is exactly why
I hand-checked the three I state as fact.

---

## 2. Decisions I need from you

1. **#1 and #13** — demote to EXPLORATORY, or re-found on a recorded null search? Their
   gaps may well be real, as #11's turned out to be. Their *current citation lists* are
   not evidence of them either way.
2. **#4 and #7** — does the hub count drug-level evidence as repurposing-question evidence?
3. **#14 and #15** — BRONZE with zero papers. Demote to EXPLORATORY, like #9, which holds
   zero papers and is labelled honestly?
4. **#8** — joins its two axes by inference across 27 papers with none at the intersection.
   That may be the point of the gap. State it on the card, or find an intersection paper?

---

## 3. A circular absence claim, caught before publication

`PMC12211534` was logged on 2026-09-03 as supporting Gap #13 *"as a NEGATIVE (no nutrition
arm)."* I read the actual abstract today. The review's stated inclusion criterion is
**RCTs of immunomodulatory therapies**. Nutrition was excluded *by design*, so its absence
from the network says nothing about whether nutrition has been trialled.

Publishing that would have manufactured an evidence gap out of another study's scope.

Two further limits on any citation of it: the search stopped **2024-07-31**, and the
authors themselves report I² = 66% and call the rankings hypothesis-generating.

**And it was already in your corpus** as PMID 40598585, VETTED. The novelty check runs
before PMCID→PMID normalisation, so a paper you already held was carried as an external
find for four days.

New doctrine: *an absence inside another study's inclusion criteria is not an evidence gap.*
Before publishing any "X was absent from Y", confirm X was **eligible and missing**, not
**excluded**.

---

## 4. The other three parked identifiers — all resolved

NCBI and ClinicalTrials.gov were both reachable this run (JSON APIs via web_fetch), which
is what failed on 2026-09-03.

| Was | Is | Correction |
|---|---|---|
| `Diabetes 2025;74(8):1339` "candidate authoritative source" | **PMID 40690616** | PubMed types it **Editorial + Comment**. Two pages of commentary on PMID 40272935 — which is already in your corpus. Citable as an editorial, never as evidence. |
| `NCT06976658` "allosteric GKA in monogenic diabetes from inactivating GCK mutations" | Verified | Drug is **dorzagliatin**. Phase 2, n=44, CUHK, recruiting, completes 2026-12-31. The *"inactivating GCK mutations"* restriction is **not in the registry fields** and was asserted without support. |
| `NCT07360080` "PROTECT extension watch" | Verified | Real, but **observational**, Sanofi, n=1000, primary completion **2035-10-29**. Cannot inform any verdict this decade. Demoted from active watch. |

**Dorzagliatin convergence:** NCT06976658 (registered Phase 2, "Glucokinase Activator in Monogenic Diabetes"; corrected 2026-09-22 — this line previously let the "Phase I" descriptor below read as a label on the NCT), PMID 42014686 (Phase I DDI with empagliflozin)
and the GKA paths under Gaps #7 and #15 are all the same molecule, tracked as separate
threads. Reconcile before the GKA line is presented as independent evidence.

---

## 5. Papers

**5 vetted** (all round-tripped against live PubMed; titles, journals and years matched
the intake notes verbatim). Two — 42698953, 39084449 — are **preclinical** and are flagged
so they can never be cited as human evidence. They falsify *"Treg therapy has never been
tested for diabetic neuropathy"* **at the preclinical level only**.

**7 ingested, 7 screened out** from six sweep queries returning 12 hits. The seven rejects
were query artifacts — a gout review matching "colchicine", SGLT2i in pulmonary
hypertension matching "repurposing", telmisartan synthesis chemistry — each recorded with
a reason so the sweep stays auditable. Verapamil returned **zero** over 30 days.

Corpus: **338 VETTED / 19 FLAGGED / 7 UNVETTED**.

---

## 6. Two things this run could not do — and does not claim it did

**The pipeline did not run.** `run_quality_improvements.py` exceeded the sandbox's ~178s
call limit twice. Background execution is impossible there: every call gets its own PID
namespace, so a `nohup`'d process dies when the call returns — confirmed by a 0-byte log
and no surviving process. **The 67 existing gates are unverified today.** The new
`gapsubject` stage is registered but has only ever run standalone.

**The push still fails.** `git push` → *"could not read Username for https://github.com"*.
No credential helper, no `~/.git-credentials`, no `GH_TOKEN`. **main is 103 commits ahead
of origin/main; origin's tip is f7e976f, 2026-04-20 — 140 days.**

The honest status of this repository: work is accumulating in a working tree no reader can
reach, and no full gate run has confirmed it.

**`RUN_PIPELINE_AND_PUSH.ps1`** (new, in the repo root) does both on your machine: runs the
gates, shows you what would ship, prompts before committing, prompts before pushing, then
verifies `docs/Reports/` actually exists on the published branch. It expects `gapsubject`
to fail — that's the finding above, not a bug. Don't fix it by loosening the gate.

Until a PAT or `gh` credential is reachable from the scheduled task's environment, publishing
stays a manual step forever.

---

*Research synthesis, not medical advice. Every claim above traces to a source; confidence is
marked where it is below certain.*
