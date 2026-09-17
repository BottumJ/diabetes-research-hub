# Diabetes Research Hub — Monitor Report

**Run:** 2026-09-17 (automated, sandbox)
**Mode:** review only — no existing files modified
**Previous report:** `monitor_report_2026-09-16.md`

---

## Headline

**The commit backlog is gone. `git status` does not know that yet, and if you act on what it
tells you, you will delete yesterday's work.**

The working tree is **byte-identical to HEAD** — verified blob-by-blob, all 87 supposedly
dirty tracked paths. Yet `git status --porcelain` reports **95–101 paths** (the count rose
during this run; see §1), eight of them as **staged deletions of files that are already
committed and present on disk**.

A Windows-side `git commit -a` right now would commit those eight deletions, removing
`monitor_report_2026-09-16.md`, both `ACTION_REQUIRED` files, `iterate_run_report_2026-09-16.md`
and `sandbox_git_commit.sh` from the repository — and then push them into the first fresh
publish in 150 days.

This is new. It did not exist yesterday. It is a direct side effect of the fix that solved
the eight-day commit block.

---

## 0. Yesterday's predictions, resolved

| # | Prediction | Outcome |
|---|---|---|
| **A** | Scripts run → `_latest` ≥894 trials; else all four files read 62+ days | **Failure branch.** 858 trials, `generated` still 2026-07-17. All four read exactly **62 days**. Headline repeats a third time. |
| **B** | Commit → `git log` ≥2026-09-16 **and** porcelain <10; else porcelain ≥79 | **Neither branch.** Commit landed (4 commits, HEAD `37ba97b`, 2026-09-16 03:22). Porcelain reads **95→101**, not <10, and ≥79 for the wrong reason. The conjunction broke apart. |
| **C** | Repair `Diabetes Drug Repurpose` query → count >10 | **Not executed.** Query unchanged, still returns 1. |

Prediction B failing in a third, unanticipated direction is the most informative result this
run produced. Both branches assumed porcelain measures uncommitted work. It does not — it
measures the index, and the index is now lying.

`[Certain]` — all three resolved against direct reads this run.

---

## 1. The git state, in detail

### What is actually true

```
HEAD            37ba97b  2026-09-16 03:22  "Fix sandbox_git_commit.sh exit-code capture"
                a61287c, b86a39e, ea91a26 also landed 2026-09-16
origin/main     unchanged since 2026-04-20
ahead           108 commits
working tree    IDENTICAL to HEAD  (git diff HEAD → 0 real differences)
```

Verification performed this run, bypassing the index entirely:

```
git hash-object <file on disk>   vs   git rev-parse HEAD:<file>
  8 "staged deletion" files  ........ 8/8 MATCH
 79 "MM" files ..................... 79/79 MATCH
```

Every one of the 87 tracked paths `git status` calls modified is bit-for-bit what HEAD
already holds. There is **no uncommitted work in this repository.**

`[Certain]` — blob-hash comparison, not a status read.

### Why status disagrees

`.git/index` was last written **2026-09-15 10:46:15**. HEAD was written **2026-09-16 03:22:26**.
The index is **16h 36m** older than the commit it is supposed to describe.

That is by design. `sandbox_git_commit.sh` — the script that broke the eight-day deadlock —
works by pointing `GIT_INDEX_FILE` at `/tmp`, outside the OneDrive mount, precisely so git
never touches the unlinkable `.git/index.lock`. It commits correctly. It simply never writes
back to the real index, and cannot, because the lock is still there and unlink is still EPERM.

So the on-disk index still describes the world of 2026-09-15:

```
                        index says          reality
 8 files                absent  ─────────►  present on disk AND in HEAD
                        ∴ reported as  D  (staged deletion) AND ?? (untracked)
                          — these 8 are a strict SUBSET of the ?? bucket

79 files                old blob ────────►  HEAD blob (identical to disk)
                        ∴ reported as  MM (staged + unstaged modification)

 4+ files               absent  ─────────►  present on disk, NOT in HEAD
                        ∴ reported as  ?? only — these are genuinely new
                          (today's report + a concurrent run's output, §1a)
```

```
 what git status shows      ████████████████████████████████████████  101 paths
 of which really dirty      ██                                          4 paths (all new, untracked)
 of which are illusion      ██████████████████████████████████████     97 paths
```

The distinction matters for the repair: the 97 are index artifacts that `git reset` clears;
the 4 are real new files that `git reset` leaves untouched and that still need committing.

`[Certain]` — index mtime, HEAD commit time, and D ⊂ ?? all read directly this run.

### 1a. A concurrent process is writing to this repo

Three files not present at the start of this run appeared mid-run:

```
08:24:01  Analysis/Scripts/audit_trial_phase.py        24.7 KB
08:24:24  Analysis/Results/trial_phase_audit.json      34.1 KB
08:24:38  Analysis/Results/.trial_phase_cache.json     15.0 KB
```

This is the daily iteration agent acting on the **P1 phase-inflation defect** queued in
`ACTION_REQUIRED_2026-09-16.md` — the TN-10 "Phase 3 → actually Phase 2" error, which that
note recorded as *"Nothing in this pipeline checks it."* Something now does.

Two consequences. First, any porcelain count in this report is a **reading at an instant**,
not a stable figure; it will keep rising until the index is rebuilt. Second, `trial_phase_audit.json`
is unread by this run and should be reviewed on its own terms next pass.

### The hazard, stated plainly

`ACTION_REQUIRED_2026-09-16.md` tells you: *"That is all"* — just `git push`, and explicitly
*"Ignore the 2026-09-15 instruction to `Remove-Item .git\index.lock`."*

`git push` alone is **safe and correct**. Push never reads the index. That instruction stands.

But it is now incomplete, and the omission has teeth. Anyone who opens a terminal, sees 95
dirty paths, and reaches for the obvious `git add -A && git commit` — or a GUI client's
"commit all" — destroys eight committed files. The index must be rebuilt *before* any
Windows-side commit, and rebuilding it (`git reset`) **does** require removing `index.lock`.

The 09-16 note retired the lock as a blocker for *committing from the sandbox*. It is still a
blocker for *repairing the index from Windows*. Both statements are true; only one was
written down.

Housekeeping, while you are in there: `.git/` now holds **81** `HEAD.lock*` files, accumulated
by successive runs renaming the lock aside because they cannot unlink it.

---

## 2. File System Status

| File | Last modified | Age | Status |
|---|---|---|---|
| `clinical_trials_latest.json` | 2026-07-17 | **62 d** | STALE — write-path split |
| `clinical_trials_summary.md` | 2026-07-17 | **62 d** | STALE — same cause |
| `hub_monitor_report.md` | 2026-07-17 | **62 d** | STALE — `hub_monitor.py` not run |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | **62 d** | STALE — master tracker |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 | 11 d | Newest real trial data |
| `pubmed_recent_latest.json` | 2026-09-06 | **11 d** | Re-run due ≈09-20 |
| `literature_gap_data.json` | 2026-09-08 | 9 d | OK — re-run due ≈09-22 |
| `literature_gap_report.md` | 2026-09-08 | 9 d | OK |
| `agent_state.json` | 2026-09-16 | 1 d | Fresh |

```
                              ┊14d
clinical_trials_latest   ████████████▋            62
clinical_trials_summary  ████████████▋            62
hub_monitor_report       ████████████▋            62
Tracker.xlsx             ████████████▋            62
trials_snapshot_09-06    ██▏                      11
pubmed_recent_latest     ██▏                      11
literature_gap_data      █▊                        9
agent_state              ▏                         1
                         0    ┊    25   50    75 days
```

The gap between the two clusters widened by one day, as it will every day until the local
scripts run. `_latest` holds **858** trials; the 09-06 snapshot holds **894**. Every consumer
reading `_latest` — including all dashboards — is served two-month-old data with no error
raised. Root cause unchanged and documented in `monitor_report_2026-09-16.md` §1a.

---

## 3. Clinical Trial Changes

**No new snapshot since 2026-09-06.** There is no 09-17 delta to compute.

For scale, the accumulated drift `_latest` (07-17) → snapshot (09-06), recomputed this run:

```
new trials         ████████████████████████████████████████████████████████  57
removed trials     █████████████████████                                     21
status changes     ██████████████████████████                                26
new results posted ·                                                          0
```

Status distribution, 09-06 snapshot (n=894):

```
COMPLETED               ████████████████████████████████████████  343
RECRUITING              ████████████████████████████████          278
NOT_YET_RECRUITING      ██████████████████                        153
ACTIVE_NOT_RECRUITING   █████████████                             114
ENROLLING_BY_INVITATION ▊                                           6
```

Phase 3 recruiting: **58** — counting any trial whose `phase` field *contains* `PHASE3`,
which folds in 6 `PHASE2, PHASE3` trials. On a strict `phase == "PHASE3"` test the figure is
**52**. Prior reports quoted 58 without stating the rule; both numbers are correct under
their own definition, and the 6-trial spread is large enough to matter when the denominator
is used for strategic ratios. Cure-track share: **3** either way. Unchanged.

### Key-sponsor cure track (09-06, unchanged)

| NCT | Program | Phase | Status |
|---|---|---|---|
| NCT04786262 | Vertex VX-880 + VX-017 (zimislecel) | PHASE3 | **RECRUITING** |
| NCT06832410 | Vertex VX-880 | PHASE3 | **RECRUITING** |
| NCT05791201 | Vertex VX-264 (encapsulated) | PHASE1/2 | ACTIVE_NOT_RECRUITING |
| NCT07222137 | Lilly baricitinib — delay Stage 3 T1D | PHASE3 | **RECRUITING** |
| NCT07222332 | Lilly baricitinib — preserve beta cell | PHASE3 | **RECRUITING** |
| NCT07088068 | Sanofi teplizumab vs. comparator | PHASE3 | **RECRUITING** |

### Correction to the 2026-09-16 Sana finding

Yesterday's report rated it `[Likely]` that Sana's zero hits were a **sponsor-string filter
failure**, and recommended re-querying by intervention keyword. That recommendation was
tested this run against the 894-record snapshot:

```
uppsala      1 hit   (NCT02064309 — a different, older Uppsala pilot)
hypoimmune   0
UP421        0
gene-edited  0
sana         0
```

The keyword re-query **does not recover it**. Searching the full JSON record, not just the
sponsor field, still returns nothing. The proposed fix would not have worked.

The likelier explanation: Sana's UP421 work is an **investigator-sponsored study run with
Uppsala University Hospital**, and is either not registered on ClinicalTrials.gov at all or
sits outside the five category queries `baseline_clinical_trials.py` issues. Web sources
this run confirm the Uppsala partnership and the investigator-sponsored design, and describe
14-month sustained C-peptide without immunosuppression.

`[Likely]` — the sponsor-filter hypothesis is now falsified `[Certain]`; the
registry-absence hypothesis is the surviving explanation but is not yet directly confirmed.
To reach `[Certain]`: query ClinicalTrials.gov unfiltered for `UP421`, and check EU CTIS —
a Swedish investigator study would register there.

**Downgrade action 10 from yesterday's list.** The keyword re-query is done and it failed.

### Therapy matcher: alias defect confirmed again

`zimislecel` → **0** trial hits, **0** PubMed hits. `VX-880` → **2** Phase 3, both recruiting.
The registry still carries the program under its code name. One alias table entry fixes it.

---

## 4. PubMed Highlights

Snapshot 2026-09-06 (11 days), 30-day lookback, 139 unique papers from 1,025 query matches
across 16 domains. **No newer pull exists.** 18 papers new vs. the 09-05 snapshot.

Cross-domain papers: **20 of 139 (14%)**. Top reads unchanged from 09-16 and not restated —
see that report §3. The two highest-leverage remain:

- **PMID 42627334** — *β-Cell Function 1 Year After Stopping Oral Baricitinib*, **Diabetes Care**.
  Durability evidence bearing directly on NCT07222137 and NCT07222332, both recruiting.
- **PMID 42626948** — gene-edited **hypoimmune islets** review, *Expert Opin Biol Ther*.
  Now more relevant, not less: §3 shows the trial registry cannot see this programme at all,
  so the literature channel is the *only* channel through which it reaches the hub.

### Domain volume — two queries still broken

```
T2D GLP-1 New          188  ████████████████████
Diabetes AI/ML         182  ███████████████████
Diabetes Microbiome    139  ██████████████
Diabetes Biomarker     121  ████████████
Diabetes Health Equity  56  ██████
Diabetes Multi-Omics    55  ██████
T2D Remission           50  █████
Diabetes Gene Therapy   45  █████
Diabetes Complications  32  ███
Closed Loop AP          24  ██
T1D Immunotherapy       23  ██
T1D Stem Cell Cure      15  █▌
LADA New Research        8  ▉
GLP-1 Pharmacogenomics   3  ▎
Diabetes Epigenetics     1  ▏  ← implausible
Diabetes Drug Repurpose  1  ▏  ← implausible, AND Tier 1 (18/20), AND feeds gap #3
```

`[Certain]` the counts are 1. `[Likely]` the queries are malformed. Unchanged from 09-16 and
still the cheapest high-value fix on the board.

---

## 5. Gap Analysis Summary

From `literature_gap_report.md` (2026-09-08, 9 days, 30 domains / 435 pairs).
**Validation level: BRONZE** — single analytical source. Preliminary; not established fact.

These are the top 5 of the **interpreted** list — `literature_gap_report.md`'s "Potentially
Meaningful" section, which filters out pairs judged methodologically distinct. They are
**not** the top 5 of the raw `ranked_gaps` array, and previous reports have labelled them
"#1–#5" without saying so. Both rank columns are shown below to stop that ambiguity
propagating.

| Interp. # | Raw # | Intersection | Gap score | Joint pubs | Tier 1 alignment |
|---|---|---|---|---|---|
| 1 | 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | **#6 Epidemiological/equity (17/20)** |
| 2 | 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | — |
| 3 | **5** | **Islet Transplant × Drug Repurposing** | 100.0 | 0 | **#4 Drug repurposing (18/20)** |
| 4 | **6** | Islet Transplant × Health Equity | 100.0 | 0 | **#6 (17/20)** |
| 5 | **9** | Gene Therapy × LADA | 100.0 | 0 | — |

Raw ranks 3 and 4 — Islet Transplant × GWAS/Polygenic and Islet Transplant × Personalized
Nutrition, both 100.0 with 0 joint publications — are filtered out as methodologically
distinct. All five scores and joint-pub counts above reconcile exactly with
`literature_gap_data.json`. `[Certain]` on the numbers; the *filtering judgement* that
demotes raw 3 and 4 is itself BRONZE and unreviewed.

Interpreted gaps #1, #3, #4 align with Tier 1 areas; #2 and #5 do not and should be
deprioritized despite identical scores.

**Gap #3 remains the most defensible opening, and remains blocked by the same caveat:** its
feeding query (`Diabetes Drug Repurpose`) returns 1 paper per 30 days. Until that query is
inspected, the gap score measures the query as much as the literature. Do not open work on
gap #3 first — fix the query first. Either outcome settles it: a repaired count >10 means the
score was an artifact; a repaired count still at 1 confirms the opening.

---

## 6. Breaking News (last 7 days)

**Nothing new requiring action.** Four searches run; all significant hits predate the window.

- **Zimislecel (VX-880):** RMAT + Fast Track held; Vertex has stated global marketing
  applications to FDA/EMA/MHRA are **expected during 2026**, following completion of Phase 3
  enrollment and dosing. No submission announcement located as of 2026-09-17.
  `[Likely]` — investor communications and trade coverage, not an FDA docket.
  To reach `[Certain]`: check FDA BLA/RMAT listings directly.
- **Sana UP421:** 14-month sustained C-peptide without immunosuppression, Uppsala
  partnership. Published earlier in 2026; not new this week. Bears on §3.
- Screened and excluded as not-new: ADA 2026 retatrutide / CagriSema / orforglipron Phase 3
  readouts (June 2026, already in corpus); oral semaglutide approval (Jan 2026); first generic
  dapagliflozin (Apr 2026); Tzield pediatric expansion.
- Pending H2 2026 FDA decisions worth a calendar entry, not an action: **insulin efsitora alfa**
  (would be the second weekly basal insulin) and **tirzepatide CV-risk indication** (would be
  the first in its class approved for CV risk reduction).

---

## 7. Recommended Actions

Ranked by consequence-if-ignored against cost-to-fix.

**1. 🔴 Do not run `git commit -a` (or a GUI "commit all") in this repo until the index is rebuilt.**
Eight already-committed files would be committed as deletions:
`ACTION_REQUIRED_2026-09-15.md`, `ACTION_REQUIRED_2026-09-16.md`,
`Analysis/Results/monitor_report_2026-09-16.md`, `Analysis/Results/iterate_run_report_2026-09-16.md`,
`Analysis/Results/.surname_resolve_cache.json`, `Analysis/Results/agent_state.json.bak_2026-09-15`,
`Analysis/Results/agent_state.json.bak_2026-09-16`, `Analysis/Scripts/sandbox_git_commit.sh`.
This is the only genuinely new risk this run.

**2. ⚠️ Push. Still one command, still safe — push does not read the index.**
```powershell
cd 'C:\Users\justi\OneDrive\Diabetes_Research'
git push
```
108 commits. `origin/main` frozen at 2026-04-20 — **150 days**.

**3. Rebuild the index, after the push. This *does* need the lock removed.**
```powershell
cd 'C:\Users\justi\OneDrive\Diabetes_Research'
Remove-Item '.git\index.lock' -Force
git reset                                   # mixed — rebuilds index from HEAD, touches no file
git status --porcelain                      # expect: only genuinely-new untracked files
Remove-Item '.git\HEAD.lock*' -Force        # 81 accumulated rename-asides
```
`git reset` with no `--hard` and no paths cannot modify the working tree. After it, expect a
short list of real `??` paths (today's report, `audit_trial_phase.py`, `trial_phase_audit.json`,
`.trial_phase_cache.json`, and any later run's output) — **and nothing else**. If `D ` or `MM`
entries survive the reset, stop: the diagnosis in §1 is wrong and the tree is genuinely dirty.

**4. ⚠️ Run the three dead scripts. Nothing in §2–§4 moves until data moves.**
```
python baseline_clinical_trials.py      # last real run 2026-07-17 — 62 days
python hub_monitor.py                   # last run 2026-07-17 — 62 days
python baseline_pubmed_alerts.py        # last run 2026-09-06 — 11 days, due ≈09-20
```
`project1_literature_gap_analysis.py` is not due until ≈2026-09-22.

**5. Fix the `_latest` write path — or stop trusting it.**
Point consumers at `max(glob('clinical_trials_snapshot_*.json'))`, or have the sandbox monitor
update `_latest` atomically. Add a staleness assertion that refuses to serve `_latest` when a
newer snapshot exists; it would have fired 2026-08-27 and saved 21 days of wrong data.

**6. Have `sandbox_git_commit.sh` warn about the index it leaves behind.**
The script is correct and it unblocked eight days of work. It should print, on exit:
*"Real .git/index not updated — `git status` will over-report. Run `git reset` from Windows
before committing there."* The failure mode it creates is silent, and silent is how the
`_latest` split cost two months.

**7. Inspect the `Diabetes Drug Repurpose` and `Diabetes Epigenetics` query strings.**
Counts of 1 over 30 days are implausible. Blocks action 10.

**8. Add `VX-880` / `VX-264` aliases for `zimislecel` in the therapy matcher.** One line.

**9. Review PMID 42627334** (*Diabetes Care*, baricitinib withdrawal durability) — informs
NCT07222137 and NCT07222332, both recruiting. And **PMID 42694848** (four-domain:
AI/ML × Biomarker × Complications × Multi-Omics), tightest Tier 1 #1 match this cycle.

**10. Open gap #3 (Islet Transplant × Drug Repurposing) — *after* action 7.**

**11. Find Sana UP421 properly.** Yesterday's keyword re-query is done and failed (§3).
Next: unfiltered ClinicalTrials.gov query on `UP421`, then EU CTIS.

**12. Pull results for NCT05872620** (Lilly orforglipron Phase 3, results posted 2026-09-04)
into the tracker. Note a source-data inconsistency found this run: that record carries
`results_posted: "2026-09-04"` while `has_results: false`. Any downstream logic gating on
`has_results` will silently skip it — which is why the delta in §3 reports **0** newly-posted
results despite this trial existing. Check whether the same contradiction appears elsewhere
in the snapshot before trusting either field.

**13. Backfill or formally accept the 2026-07-17 → 2026-08-27 snapshot hole (41 days).**

---

## 8. Falsifiable predictions for the next run

**Prediction A.** If action 3 is executed, `git status --porcelain` drops to **at most the
handful of genuinely-new untracked files** (≤6, not 0 — `git reset` clears the 97 illusory
paths but leaves real untracked ones) and `.git/index` mtime moves past 2026-09-16. If not,
it reads **101 or more**, since each run adds a report, a state backup, and now audit output.

**Prediction B.** If action 2 is executed, `git rev-list --count origin/main..HEAD` returns
**0** and the published site's build date moves off 2026-04-20. If not, the ahead-count reads
**110 or more**.

**Prediction C.** If action 4 is executed, `clinical_trials_latest.json` reads **≥894** trials
with `generated` after 2026-09-17. If not, all four stale files read **63 days** and the §2
headline repeats a fourth time.

**Prediction D.** If action 7 is executed and the query is malformed, the repaired
`Diabetes Drug Repurpose` 30-day count returns **>10**. If it returns 1 again, gap #3's score
is real and the Tier 1 opening is confirmed rather than undermined. Either outcome is
informative — which is why this stays the cheapest high-value item on the list.

---

*Generated by the automated hub monitor. Review-only run — no existing files were modified.
Evidence levels labeled per RESEARCH_DOCTRINE.md §Validation Tiers. Gap analysis findings are
BRONZE (single analytical source) and preliminary. Git-state claims are `[Certain]`, verified
by blob-hash comparison rather than by `git status`.*
