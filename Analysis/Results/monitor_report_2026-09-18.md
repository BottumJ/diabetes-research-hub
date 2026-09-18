# Diabetes Research Hub — Monitor Report

**Run:** 2026-09-18 (automated, sandbox)
**Mode:** review only — no existing files modified
**Previous report:** `monitor_report_2026-09-17.md`

---

## Headline

**The git trap is closed. The data collectors are still not running, and the publish is now
151 days old.**

Yesterday's headline hazard — 95–101 phantom dirty paths and eight staged deletions of
committed files — is gone. `git status --porcelain` reads **2**. Zero staged deletions.
The index resync worked.

That was the blocker that justified not touching anything else. It is resolved. What remains
is the backlog it was hiding:

- **112 commits** sit unpushed. `origin/main` last moved **2026-04-20**.
- `clinical_trials_latest.json` reads **63 days old** for the fourth consecutive run.
- The only thing that ran in the last 24 h is the gap analysis — which ran, and produced a
  clean result.

There is no longer a safety argument for waiting. `[Certain]` — verified by direct read of
`.git/index`, `git rev-list`, and file mtimes this run.

---

## 0. Yesterday's predictions, resolved

| # | Prediction | Outcome |
|---|---|---|
| **A** | Action 3 executed → porcelain ≤6, index mtime past 2026-09-16. Else ≥101. | **TRUE branch.** Porcelain = **2**. Index mtime **2026-09-17 08:53**. Four commits landed (HEAD `ca62dc2`). The staged-deletion trap did not recur. |
| **B** | Action 2 executed → ahead-count 0 and site build date moves off 2026-04-20. Else ≥110. | **FALSE branch, as specified.** Ahead-count = **112**. `origin/main` HEAD is still `f7e976f`, dated **2026-04-20**. |
| **C** | Action 4 executed → `_latest` ≥894 trials, `generated` after 09-17. Else all four stale files read 63 d. | **FALSE branch, as specified.** `_latest` holds **858** trials, `generated` **2026-07-17**. All four read exactly **63 days**. |
| **D** | Repaired `Diabetes Drug Repurpose` query returns >10; if still 1, gap #3 is real. | **Not resolvable this run.** No new PubMed pull, and direct E-utilities access is blocked from the sandbox (see §4a). Script provided below. |

Prediction A is the first clean TRUE branch in four runs. The fix held overnight and survived
a second commit cycle — which is the part that mattered, since the previous workaround
re-armed the trap on every run.

`[Certain]` — A, B, C resolved against direct reads.

---

## 1. File System Status

| File | Last modified | Age | Status |
|---|---|---|---|
| `clinical_trials_latest.json` | 2026-07-17 | **63 d** | STALE — write-path split |
| `clinical_trials_summary.md` | 2026-07-17 | **63 d** | STALE — same cause |
| `hub_monitor_report.md` | 2026-07-17 | **63 d** | STALE — `hub_monitor.py` not run |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | **63 d** | STALE — master tracker |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 | 12 d | Newest real trial data |
| `pubmed_recent_latest.json` | 2026-09-06 | **12 d** | Re-run due now (30 d lookback) |
| `pubmed_recent_summary.md` | 2026-09-06 | 12 d | Same |
| `open_findings.md` | 2026-09-12 | 6 d | Not re-emitted since 09-12 |
| `literature_gap_data.json` | 2026-09-17 | **1 d** | FRESH — ran overnight |
| `literature_gap_report.md` | 2026-09-17 | **1 d** | FRESH |
| `agent_state.json` | 2026-09-17 | 1 d | Fresh |

```
                              ┊14d stale threshold
clinical_trials_latest   ████████████▉            63
clinical_trials_summary  ████████████▉            63
hub_monitor_report       ████████████▉            63
Tracker.xlsx             ████████████▉            63
trials_snapshot_09-06    ██▍                      12
pubmed_recent_latest     ██▍                      12
open_findings            █▏                        6
literature_gap_data      ▎                         1
agent_state              ▎                         1
                         0    ┊    25   50    75 days
```

The two-cluster structure is unchanged. `_latest` holds **858** trials; the 09-06 snapshot
holds **894**. Every dashboard consumer reading `_latest` is served two-month-old data with
no error raised. Root cause documented in `monitor_report_2026-09-16.md` §1a.

**One thing moved:** the gap analysis re-ran overnight (09-08 → 09-17) after nine days idle.
It is the only collector that is currently healthy.

---

## 2. Clinical Trial Changes

**No new snapshot since 2026-09-06.** There is no 09-18 delta to compute. Nothing in this
section is new information; it is the standing drift, recomputed to confirm it has not moved.

Accumulated drift, `_latest` (07-17) → newest snapshot (09-06):

```
new trials         ████████████████████████████████████████████████████████  57
removed trials     █████████████████████                                     21
status changes     ██████████████████████████                                26
```

Status distribution, 09-06 snapshot (n = 894):

```
COMPLETED               ████████████████████████████████████████  343
RECRUITING              ████████████████████████████████          278
NOT_YET_RECRUITING      ██████████████████                        153
ACTIVE_NOT_RECRUITING   █████████████                             114
ENROLLING_BY_INVITATION ▊                                           6
```

Phase 3 recruiting: **52** on a strict `phase == "PHASE3"` test, **58** if `PHASE2, PHASE3`
trials are folded in. Both figures carried forward from yesterday with the counting rule
stated. Cure-track share: **3**, either way.

### Key-sponsor cure track (09-06, unchanged from 09-17)

| NCT | Program | Phase | Status |
|---|---|---|---|
| NCT04786262 | Vertex VX-880 + VX-017 (zimislecel) | PHASE3 | **RECRUITING** |
| NCT06832410 | Vertex VX-880 | PHASE3 | **RECRUITING** |
| NCT05791201 | Vertex VX-264 (encapsulated) | PHASE1/2 | ACTIVE_NOT_RECRUITING |
| NCT07222137 | Lilly baricitinib — delay Stage 3 T1D | PHASE3 | **RECRUITING** |
| NCT07222332 | Lilly baricitinib — preserve beta cell | PHASE3 | **RECRUITING** |
| NCT07088068 | Sanofi teplizumab vs. comparator | PHASE3 | **RECRUITING** |

### Data-integrity defect, re-confirmed

In the 09-06 snapshot, the `Diabetes Recently Completed with Results` category holds **343**
trials. **All 343 carry a populated `results_posted` date. Zero have `has_results == true`.**
(In the stale `_latest`, the same category holds 321, with the identical 321 / 0 split.)

```
results_posted populated  ████████████████████████████████████████  343
has_results == true       ·                                           0
```

Any downstream filter written as `if trial["has_results"]` sees an empty set. This is not a
collection failure — the dates are present in the record. It is a field the collector never
writes. `[Certain]` — counted directly from the snapshot this run.

This is the mechanism behind **F-05** (ZUPREME-2 missed for three days because the watch was
keyed on the wrong field). It is one line in `baseline_clinical_trials.py`.

### Results posted since `_latest` went stale — still unseen by every dashboard

22 trials posted results between 07-17 and 09-06. Two are tracked-sponsor Phase 3/4:

| NCT | Posted | Phase | Sponsor | Trial |
|---|---|---|---|---|
| NCT05872620 | **2026-09-04** | PHASE3 | Eli Lilly | ATTAIN-2 — orforglipron, n = 1,613 (**F-01**, open since 09-06) |
| NCT04596631 | 2026-08-21 | PHASE3 | Novo Nordisk | Oral semaglutide vs. placebo, n = 132 |
| NCT05035082 | 2026-08-10 | PHASE4 | Novo Nordisk | RYBELSUS® comparative, n = 1,018 |

The remaining 19 are academic behavioural, nutrition and care-delivery trials. Three of them
sit on **Tier 1 area 6 (health equity / epidemiology)** and are cheap to read:
`NCT04876053` (rural home food delivery), `NCT04828785` (Food as Medicine, UNC),
`NCT06029517` (SSB reduction, Native American communities).

---

## 3. PubMed Highlights

**No new pull since 2026-09-06.** 139 unique papers, 30-day lookback, 16 domains,
1,025 query matches. Everything below is from that snapshot and was reported on 09-17.
It is repeated only where an action depends on it.

Domain volume, 30-day window:

```
T2D GLP-1 New              ████████████████████████████████████████  188
Diabetes AI/ML             ██████████████████████████████████████    182
Diabetes Microbiome        █████████████████████████████             139
Diabetes Biomarker         █████████████████████████                 121
Diabetes Health Equity     ███████████                                56
Diabetes Multi-Omics       ███████████                                55
T2D Remission              ██████████                                 50
Diabetes Gene Therapy      █████████                                  45
Diabetes Complications New ██████                                     32
Closed Loop AP             █████                                      24
T1D Immunotherapy          ████                                       23
T1D Stem Cell Cure         ███                                        15
LADA New Research          █                                           8
GLP-1 Pharmacogenomics     ▋                                           3
Diabetes Drug Repurpose    ▎                                           1  ← suspect
Diabetes Epigenetics       ▎                                           1  ← suspect
```

### 3a. The two suspect queries — a quantitative prior

Both low-count queries are **triple conjunctions** with a narrow third clause:

```
Diabetes Drug Repurpose: diabetes AND ("drug repurposing" OR "drug repositioning")
                                  AND (computational OR network OR screening)
Diabetes Epigenetics:    diabetes AND (epigenetic OR methylation)
                                  AND (GWAS OR "genome-wide")
```

The gap analysis, run independently against the same API, gives Drug Repurposing **622**
publications since 2020 and Epigenetics **7,811**. Converted to a 30-day expectation:

| Domain | 2020+ total | Expected / 30 d | Observed | Ratio |
|---|---|---|---|---|
| Drug Repurposing | 622 | ≈ 7.6 | 1 | 0.13× |
| Epigenetics | 7,811 | ≈ 95.5 | 1 | **0.01×** |

Drug Repurposing at 0.13× is low but survivable as a genuine narrowing effect. Epigenetics at
**0.01×** is not — a two-order-of-magnitude shortfall on a 7,811-paper domain is a query
defect, not a quiet month. `[Likely]` — the arithmetic is `[Certain]`, but the two queries use
different domain strings than the gap script, so the comparison is not strictly like-for-like.

**This matters for the gap analysis, not just the alert feed.** Gap #3
(Islet Transplant × Drug Repurposing, score 100.0, a Tier 1 opening) rests on a Drug
Repurposing domain count. If the alert-side query is under-returning, the question of whether
the gap-side query does the same is open and unanswered.

**Resolving it requires one PubMed call that the sandbox cannot make.** E-utilities is outside
the sandbox's allowed fetch set. Script to run locally is in §6.

### 3b. Cross-domain papers (highest-value, unchanged)

20 of 139 papers hit multiple domains. The standouts, all still unread:

| PMID | Domains | Paper |
|---|---|---|
| **42694848** | 4 — AI/ML, Biomarker, Complications, Multi-Omics | COL1A2 / APOLD1 dual-axis framework, diabetic nephropathy–retinopathy comorbidity. **The only 4-domain paper on record** (**F-09**, unread 12 days) |
| 42626948 | 3 — Stem Cell Cure, Immunotherapy, teplizumab | Gene-edited hypoimmune islets as a T1D cure — immunological challenges |
| 42694300 | 3 — Biomarker, Microbiome, Multi-Omics | Oral microbiome + metabolome, Alström / Bardet-Biedl |
| 42673585 | 3 — orforglipron, retatrutide, CagriSema | GLP-1 RA and co-agonists for weight loss, *Ann Intern Med* 09-01 |
| 42627334 | 2 — Immunotherapy, baricitinib | β-cell function 1 year after **stopping** oral baricitinib, *Diabetes Care* 08-21 |

PMID 42627334 is the one to read first among the two-domain set. Lilly has two Phase 3
baricitinib trials recruiting (NCT07222137, NCT07222332); a one-year-post-withdrawal
durability result is directly load-bearing on how those read out.

### 3c. Data-quality note

PMID **42698931** carries `title: null` and `abstract_snippet: null` with a valid DOI and
journal. One record of 139 — a parse failure, not systematic. Logged, not urgent.

---

## 4. Gap Analysis Summary

**Re-ran 2026-09-17 08:45**, first refresh in nine days. Date range 2020/01/01 → 2026/09/17,
30 domains, 435 pairs. **Validation level: BRONZE** throughout.

### Top 5 under-researched intersections

| Rank | Intersection | Gap Score | Joint Pubs | Tier 1 alignment |
|---|---|---|---|---|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | **Tier 1 #6** (epidemiology / equity) |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | Tier 1 #2 (literature synthesis) |
| 3 | Islet Transplant × Drug Repurposing | 100.0 | 0 | **Tier 1 #4** (repurposing screen) |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | **Tier 1 #6** |
| 5 | Gene Therapy × LADA | 100.0 | 0 | Tier 1 #2 |

Four of the top five touch a Tier 1 contribution area. Gap #3 remains the single best-scoped
computational opening — Tier 1 #4 is explicitly "map approved drugs against diabetes protein
interaction networks," and the gap report's own verification (re-run unbounded 09-06) found
7 all-time records, **none of which is a computational drug screen for islet protection**.

Caveat carried forward: gap #3's score depends on the Drug Repurposing domain count, which
§3a puts under question.

### What changed 09-08 → 09-17

Almost nothing, and that is the useful finding. All 30 domain counts rose by the expected
9-day increment (Prevention/DPP 82,027 → 82,343; LADA 603 → 607). Two pair counts moved:
Epigenetics × LADA 2 → 3, Neuropathy × Gestational DM entered the unclassified table at 4.
**No ranking changed. No gap was created or closed.**

**Correction to a tempting reading.** `SGLT2 Inhibitors × Gestational DM` disappeared from
the unclassified table between the two runs. That is **not** a data change: the pair is still
in `literature_gap_data.json` with `pair_count = 17` and `gap_score = 99.8`. It fell off the
rendered table because the table filters at ≥ 99.9 and the score moved 99.9 → 99.8 as
Gestational DM's denominator grew. A reader diffing the two reports would conclude a gap had
closed. It had not. `[Certain]` — read from `ranked_gaps` directly.

The rendering threshold is doing silent work on a published artifact. Worth a footnote in the
report generator.

---

## 5. Breaking News (last 7 days)

**Nothing genuinely new.** Web search for the 7-day window returned ADA-2026 (June) material
and 2026 forecast pieces — retatrutide TRANSCEND-T2D-1 and the orforglipron ACHIEVE programme,
both already in the hub. No Phase 3 readout, no FDA action, no major publication dated
09-11 → 09-18.

### F-04 — RESOLVED

The one thing the search did settle is an open finding, not new news.

**F-04** recorded an internal contradiction: the hub logged a Mounjaro/tirzepatide CV
indication as an FDA action on 08-28, while a 09-12 search described it as *expected* H2 2026.

**The 08-28 logging was correct.** Lilly's own investor release states the FDA approved
Mounjaro on **2026-08-28** to lower the risk of major adverse cardiovascular events (CV death,
non-fatal MI, non-fatal stroke) in adults with T2D at high CV risk. The "expected H2 2026"
language came from a secondary forecast page written before the approval and never updated.

`[Certain]` on the fact and the date, sourced to the sponsor's own announcement.
Not yet pinned to an `accessdata.fda.gov` approval-letter number — do that before the claim
goes in a published artifact, per doctrine.

**F-04 closes.** The hub was right; the contradiction was in the secondary source.

---

## 6. Recommended Actions

Ranked by value ÷ cost. Items 1–3 are the whole backlog; everything below is normal work.

**1. Push. `git push origin main`.**
112 commits, 151 days. The hazard that justified holding is gone — porcelain is 2 and there
are no staged deletions. This is now a one-command action with nothing blocking it, and it is
the only action that makes any of the last five months' work visible outside this machine.

**2. Run the collectors.** Three commands, in this order:

```
python Analysis/Scripts/baseline_clinical_trials.py     # clears the 63-day trial staleness
python Analysis/Scripts/baseline_pubmed_alerts.py       # 12 days, 30-day window — due now
python Analysis/Scripts/hub_monitor.py                  # 63 days — file-change report
```

`project1_literature_gap_analysis.py` does **not** need re-running; it ran 09-17.

**3. Fix `has_results` in `baseline_clinical_trials.py`.** One line. Set it from
`results_posted` being non-empty. 343 records currently disagree with themselves, and this is
the mechanism behind F-05. Do this *before* step 2 so the fresh pull is correct.

**4. Settle the two suspect PubMed queries (§3a).** Cheapest high-value item on the list, and
it feeds gap #3. The sandbox cannot reach E-utilities; run this locally:

```python
# Analysis/Scripts/_probe_query_narrowing.py
import json, time, urllib.parse, urllib.request

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

PROBES = {
    "Drug Repurpose (current, triple)":
        'diabetes AND ("drug repurposing" OR "drug repositioning") '
        'AND (computational OR network OR screening)',
    "Drug Repurpose (drop 3rd clause)":
        'diabetes AND ("drug repurposing" OR "drug repositioning")',
    "Epigenetics (current, triple)":
        'diabetes AND (epigenetic OR methylation) AND (GWAS OR "genome-wide")',
    "Epigenetics (drop 3rd clause)":
        'diabetes AND (epigenetic OR methylation)',
    # gap-script strings, for the like-for-like the report could not make:
    "Gap script: Drug Repurposing":
        '"drug repurposing" AND diabetes',
    "Gap script: Islet Transplant":
        '"islet transplantation"',
}

def count(term, reldate=30):
    q = urllib.parse.urlencode({
        "db": "pubmed", "term": term, "retmax": 0, "retmode": "json",
        "reldate": reldate, "datetype": "pdat",
    })
    with urllib.request.urlopen(f"{BASE}?{q}", timeout=30) as r:
        return int(json.load(r)["esearchresult"]["count"])

print(f"{'probe':38} {'30d':>7} {'all-time':>9}")
for label, term in PROBES.items():
    c30 = count(term, 30)
    time.sleep(0.4)                      # NCBI: <=3 req/s unauthenticated
    call = count(term, 100000)
    time.sleep(0.4)
    print(f"{label:38} {c30:7} {call:9}")
```

Decision rule, fixed in advance: if dropping the third clause raises the 30-day count by
**more than 5×**, the query is over-narrowed and should be widened. If it does not, the low
counts are real and gap #3's Tier 1 opening is **strengthened**, not undermined. Either
result is worth having.

**5. Read PMID 42627334** — β-cell function one year after stopping oral baricitinib,
*Diabetes Care* 08-21. Two Lilly Phase 3 baricitinib trials are recruiting; a durability
result post-withdrawal is load-bearing on how they read out. Closest thing to a decision-
relevant paper in the current snapshot.

**6. Read PMID 42694848** (F-09, unread 12 days) — the only 4-domain cross-domain paper the
hub has ever logged, and it sits on Tier 1 areas 1 and 5.

**7. Log ATTAIN-2 (NCT05872620) in the tracker** — F-01, open 12 days. Blocked on the tracker
being 63 days stale, which action 2 fixes. F-02 (the 5.50/7.78/10.54 vs 5.1/7.0/9.6 estimand
discrepancy) stays open until the *Lancet* primary is read.

**8. Footnote the gap report's ≥99.9 render threshold** (§4). A pair silently leaving a
published table without its underlying number changing is a reader-facing defect.

**9. Re-emit `open_findings.md`.** Its own rule says every monitor run re-emits it; it has not
moved since 09-12. This run is review-only and did not write it. F-04 closes; F-05's mechanism
is now identified (action 3).

---

## 7. Open findings — status delta

This run did not modify `open_findings.md`. Changes it should absorb:

| ID | Change this run |
|---|---|
| **F-04** | **CLOSES.** FDA approved the Mounjaro CV indication 2026-08-28; sponsor announcement confirms. Contradiction was in the secondary source. |
| **F-05** | Mechanism identified: `has_results` is never written despite `results_posted` being populated in all 343 records. One-line fix (action 3). |
| F-01, F-02, F-08–F-12 | Unchanged, unread. F-09 now 12 days open. |
| F-07 | Zenagamtide `NCT07797335` still not in a watch list; blocked on the collector run. |
| **New (M)** | Gap report's unclassified table filters at ≥99.9; pairs leave it on denominator growth alone, with no data change. Reader-facing. |

---

## 8. Falsifiable predictions for the next run

**Prediction A.** If action 1 is executed, `git rev-list --count origin/main..HEAD` returns
**0** and `origin/main` HEAD moves off `f7e976f` / 2026-04-20. If not, the ahead-count reads
**114 or more** — each run adds a report and a state backup.

**Prediction B.** If action 2 is executed, `clinical_trials_latest.json` reads **≥ 894**
trials with `generated` after 2026-09-18, and `hub_monitor_report.md` reports a very large
new/modified count (60+ days of accumulation). If not, all four stale files read **64 days**
and this headline repeats a fifth time.

**Prediction C.** If actions 2 *and* 3 are both executed, the count of trials with
`has_results == true` in the fresh pull is **> 300**. If action 2 runs without action 3, it
stays at **exactly 0** — which is the cleanest available test that the fix landed.

**Prediction D.** If action 4 is executed, dropping the third clause raises the Epigenetics
30-day count above **20** (current: 1). A result under 5 would falsify the over-narrowing
hypothesis in §3a and send the low count back to "genuinely quiet domain."

---

*Generated by the automated hub monitor. Review-only run — no existing files were modified.
Evidence levels labeled per RESEARCH_DOCTRINE.md §Validation Tiers. Gap analysis findings are
BRONZE (single analytical source) and preliminary. Trial and PubMed figures are read from the
2026-09-06 snapshots, not from `_latest`, and are labeled as such. Git-state claims are
`[Certain]`, verified by direct index and rev-list reads rather than by `git status`.*

**Sources consulted this run (web):**
- [FDA approves Lilly's Mounjaro (tirzepatide) to reduce cardiovascular risk in adults with type 2 diabetes — Eli Lilly](https://investor.lilly.com/news-releases/news-release-details/fda-approves-lillys-mounjaro-tirzepatide-reduce-cardiovascular)
- [ADA 2026 highlights: therapies in development — Diabetes on the Net](https://diabetesonthenet.com/diabetes-primary-care/ada-2026/)
- [Breakthrough studies: first triple-hormone therapy — American Diabetes Association](https://diabetes.org/newsroom/press-releases/breakthrough-studies-demonstrate-effectiveness-first-triple-hormone-therapy)
- [Cell therapies in clinical trials for type 1 diabetes — Breakthrough T1D](https://www.breakthrought1d.org/news-and-updates/cell-therapies-in-clinical-trials/)
