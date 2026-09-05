# Decision Brief — 2026-09-05

**One thing needs you today. The rest is done.**

---

## 0. BLOCKING: the published site has been frozen for 138 days

`git push` has been failing in the sandbox since April. Nothing this agent has built
since then has reached a reader.

| | |
|---|---|
| Local `main` | 100 commits ahead of `origin/main` |
| `origin/main` tip | `f7e976f`, **2026-04-20** |
| Gap | **138 days** |
| Cause | HTTPS remote, no credential helper, no `~/.git-credentials`, no `GH_TOKEN` → `could not read Username for https://github.com` |

**What is false on the live site right now**

- `docs/Reports/` has *never existed* on `origin/main`. Both reports the hub advertises
  as "Available" return 404 for a real reader. Yesterday's run made them servable; the day
  before, it made them exist. Neither has reached anyone.
- The hub still reads "across 15 high-priority research domains" — the pre-2026-04-17 text.
- None of the 14 citation gates, the retraction gate, the NCT gate, or this week's freshness
  gate exist for anyone but this agent.

**Why no gate caught it.** Every publish-side assertion this repo owns — `audit_published_links.py`,
`sync_docs_dashboards.py`, `sync_docs_reports.py`, `regression_suppression_gate.py`, and the
freshness gate added today — reads `docs/` **on local disk**. All five were green today while
the live site served April content. "Published" has quietly meant "written to a local directory"
since the spring. The thing the gates audit and the thing a reader loads have been different
objects for 138 days.

**It was noticed eleven times.** Run summaries on 2026-05-24, 06-03, 06-06, 06-09, 07-01, 07-02,
07-11, 07-18, 07-25, 08-03 and 08-17 each mention a push failure, and each moved on. Noticing a
thing eleven times without it ever changing what the next run does is not memory.

**Two actions**

1. `git push` from Windows, or provision a PAT / `gh` credential the scheduled task can use.
2. Add a stage that **fails** when `origin/main` is behind `main`, so no future run can report
   a publish it did not perform. Queued as P1.

*Confidence: [Certain] — measured directly from the repo (`git rev-list --count origin/main..main`,
`git log origin/main -1`, `git ls-tree origin/main -- docs/Reports`).*

---

## 1. Yesterday's staleness finding cleared the wrong file

The 2026-09-04 run found `pubmed_recent_summary.md` 49 days into a declared 30-day window, and
in the same breath cleared the other report: *"literature_gap_report.md, which regenerates
(2026-09-03) and is therefore fine."*

It was not fine.

```
literature_gap_report.md   rendered 2026-09-04   <- fresh, and published
literature_gap_data.json   written  2026-07-17   <- 50 days old
```

`improve_gap_analysis.py` re-rendered the report from frozen JSON every day and stamped each copy
`**Generated:** <today>`. The file that *admitted* its age was the honest one; this one laundered
50-day-old data behind a fresh date. **"Does it regenerate" and "is its data current" are different
questions, and only the second one matters to a reader.**

Both are now fixed and gated. Gap data now covers through 2026/09/05.

*[Certain] — file dates and generator source read directly.*

---

## 2. The fix nearly reintroduced the defect through its own resume cache

The gap sweep is 465 PubMed queries (~6 min) against a 300s stage timeout, so it was given a
`--budget` flag and wired in as a resumable stage. Then:

After a **completed** sweep, `.gap_checkpoint.json` survived with all 465 answers in it.
`run_gap_analysis()` does call `os.remove()` on success — but it is wrapped in `except OSError: pass`,
and **this mount raises `PermissionError` on every unlink** (reproduced directly today).

A complete checkpoint that outlives its run is a permanent freeze: every later run loads 465 cached
answers, issues zero queries, and stamps today's date on counts that never change again. The same
defect, re-entering through its own fix.

Fixed by enforcing expiry on **read** (`CHECKPOINT_VALID_DAYS = 1`), not on cleanup — correctness
must not depend on a delete succeeding when the delete is the thing that failed. Three cases verified:
stale-1d discarded, same-day resumed, missing-timestamp discarded.

*[Certain] — `PermissionError` reproduced; all three expiry cases executed.*

---

## 3. The monitor's headline counted the wrong thing

`Unique papers found: 141` sat directly above a table row reading `T2D GLP-1 New | 190`.
Both numbers were right. They answered different questions.

| | |
|---|---|
| Papers the queries **matched** | 1,044 |
| Papers actually **retrieved** | 141 (13.5%) |

Worse, coverage is **inversely** related to activity, because the cap is constant and the matched
count is not:

```
T2D GLP-1 New        190 matched, 10 read    5.3%   <- busiest domain, thinnest sample
Diabetes AI/ML       182 matched, 10 read    5.5%
Diabetes Microbiome  144 matched, 10 read    6.9%
LADA New Research      9 matched,  9 read  100.0%   <- quietest domain, complete
Drug Repurpose         1 matched,  1 read  100.0%
```

The report sampled most thinly exactly where the field moves fastest. Header, table, per-section
counts, cross-domain caveat and JSON metadata now all state the sampling rate. The hub card derives
its own numbers from the snapshot instead of asserting them — which also corrected "15 domains"
(there have been 16 since 2026-04-17).

*[Certain] — counts from the live sweep.*

---

## 4. Gap #3 is GOLD on a claim its own all-time evidence contradicts

Every recorded audit of *Insulin Resistance in Islet Transplant* was bounded to 2020+. Its
counterevidence is pre-2020, so no sweep could ever have seen it.

- **PMID 24085506** — *J Clin Endocrinol Metab* 2013, "Improvement in insulin sensitivity after human
  islet transplantation for type 1 diabetes." PubMed publication type: **Clinical Trial**. NIH-funded.
- **PMID 24691031** — *Am J Physiol Endocrinol Metab* 2014, insulin sensitivity index, minimal model
  vs euglycemic clamp, in islet transplant recipients.

Both measure insulin sensitivity as an endpoint in human recipients. Neither is in the gap's paper set.

Separately: the gap's actual GOLD evidence is PMID 42608595, whose four extracted findings are about
immunosuppression regimens and lymphocyte subsets. **None mentions insulin resistance.**

**Your call, two parts:** (a) restate the gap as *"not a reported endpoint in multi-centre / registry
studies"* — which the evidence supports — rather than *"unmeasured,"* which it refutes; (b) decide
whether GOLD survives the restatement. Reported, not applied: re-tiering is a scientific judgement.

*[Certain] on the two papers and their publication types; [Likely] that the restated claim holds —
it rests on the absence of an IR endpoint in the registry/multi-centre literature, which is an
absence claim and needs the all-time sweep queued as P1.*

---

## 5. Gap #11 confirmed at the strongest level yet — via an acronym collision

All-time PubMed, no date bound:

```
("Collaborative Islet Transplant Registry" OR CITR)
  AND (race OR ethnicity OR disparity OR equity OR socioeconomic)
  -> 2 records
     PMID 30677344  Plant Dis 2017        wheat stem rust, landrace CItr 15026
     PMID 27544524  Theor Appl Genet 2016 wheat stem rust, landrace CItr 4311
```

**Zero biomedical hits.** `CItr` is the Cereal Introduction accession prefix for wheat landraces.
Broadening to `"islet transplantation" AND (race OR ethnicity)` returns 6 all-time, none an equity
analysis. Meanwhile the 12th CITR Allograft Report (2025) covers 1,477 recipients at 40 centres —
a registry large enough to support the analysis, with none published.

Recorded as a standing trap: any automated count on the bare acronym is contaminated by agronomy.

*[Certain] — both contaminating records fetched and read.*

---

## Also done

- **`tegoprubart_islet_t1d`** still rests on zero PMIDs, 73 days after being rated PARTIALLY_VALIDATED
  off conference abstracts and press releases. `tegoprubart` returns 8 records all-time, every one a
  review or secondary report. Measured and queued; not downgraded.
- **14/14 oldest-stamped papers re-verified live** against PubMed rather than against the title cache
  (a cached title cannot detect a cache that is wrong). All resolve, all titles match. No UNVETTED
  backlog remains — 352 records, all vetted or flagged with recorded reasons.
- **Credibility sweep clean**: 0 impossible PMIDs (live ceiling 42,694,033), 0 unhedged preclinical
  overclaims.
- **New**: `audit_report_freshness.py` + `test_report_freshness_gate.py`. A gate green on its first
  run proves nothing, so the fixture replays both real pre-repair texts plus two controls.
- **Pipeline**: 71/71 stages `[OK]` (was 68). 1,400/1,400 local links resolve — see §0 for what that
  does and does not mean.
- **Recorded**: this mount forbids `unlink` repo-wide. ~180 orphaned `.git/*.lock.*` files have
  accumulated since April under a dozen ad-hoc naming schemes because every run rediscovers this and
  renames around it. Now written down.

---

*Research synthesis, not medical advice.*
