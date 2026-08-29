# Diabetes Research Hub — Monitor Report

**Run:** 2026-08-29 (scheduled, review-only — no files modified)
**Data read:** `clinical_trials_snapshot_2026-08-28.json`, `pubmed_recent_snapshot_2026-08-28.json`,
`literature_gap_data.json`, `literature_gap_report.md`, `hub_monitor_report.md`, prior monitor reports
**No new data was pulled this run.** Everything below is read from disk plus a web check.

---

## Headline: the hub had SURPASS-CVOT results on disk for 51 days. The FDA approved the label yesterday. The hub still does not know.

On **2026-08-28** the FDA approved Mounjaro (tirzepatide) to reduce MACE in adults with T2D and
established ASCVD — the first dual GIP/GLP-1 agonist to get a CV risk-reduction indication.
**[Certain]** — Lilly investor release plus four concordant secondary outlets.

The trial behind it is **NCT04255433**, and it is sitting in this hub's corpus:

```
NCT04255433 | SURPASS-CVOT | Eli Lilly | PHASE3 | COMPLETED
enrollment 13,299 | completed 2025-06-12 | results_posted 2026-07-08
```

Enrollment 13,299 matches the "more than 13,000 participants" in Lilly's release. This is the trial.
**[Certain]** — snapshot record on disk, cross-checked against the sponsor's own description.

The 08-23 report *did* list it, once, in a results-posted table:

> `| 2026-07-08 | NCT04255433 | 3 | Eli Lilly | Tirzepatide vs dulaglutide, MACE (SURPASS-CVOT) |`

So the pipeline surfaced the fact and then dropped it. **The failure is not detection — it is that
nothing in this hub converts "Phase 3 CVOT, 13,299 patients, results just posted" into a watch item.**
A results posting on a 13,000-patient CVOT from a sponsor with a pending sNDA is about as strong a
regulatory leading indicator as registry data produces, and the hub had 51 days of it.

This is the **third instance in seven days** of the same pattern:

| Event | Date | NCT already on disk | Lead time wasted |
|---|---|---|---|
| Abbott Libre Duo De Novo | 2026-08-25 | NCT07739342 | 28 days |
| Diamyd DIAGNODE-3 halt | (logged 08-27) | NCT05018585 | 138 days |
| **Mounjaro CV indication** | **2026-08-28** | **NCT04255433** | **51 days** |

Yesterday's report recommended building "an event feed keyed to NCTs already on disk" and ranked it
P1-#4. Today is the argument for moving it to P0. Three hits in a week is not a coincidence; it is a
measurement telling you which single missing component costs the most.

**What the feed needs, minimally:** for the ~900 tracked NCTs, watch `lastUpdatePostDate`,
`whyStopped`, and the `results_posted` → *regulatory action* transition. Cross the results-posted set
against FDA approvals/De Novo/CRL announcements weekly. That is one join over data you already have.

---

## File System Status

| File | Modified | Age | Status |
|---|---|---|---|
| `clinical_trials_snapshot_2026-08-28.json` | 08-28 08:24 | 1d | current |
| `pubmed_recent_snapshot_2026-08-28.json` | 08-28 08:28 | 1d | current |
| `literature_gap_report.md` | 08-28 08:43 | 1d | **misleading — see below** |
| `clinical_trials_latest.json` | 07-17 02:05 | **43d** | **stale** |
| `pubmed_recent_latest.json` | 07-17 02:06 | **43d** | **stale** |
| `literature_gap_data.json` | 07-18 03:11 | **42d** | **stale** |
| `hub_monitor_report.md` | 07-17 02:16 | **43d** | **stale** |
| `Diabetes_Research_Tracker.xlsx` | 07-17 10:07 | **43d** | **stale** |
| `Research_Findings_Summary.md` | 08-28 08:43 | 1d | current |

**The canonical files have not moved in 43 days.** Dated snapshots keep landing; the `*_latest.json`
pointers do not get written. This is the same P0 as 08-27 and 08-28 — third consecutive flag.

**`literature_gap_report.md` is dated 08-28 but its data ends 2026-07-17.** The header says
"Generated: 2026-08-28 08:43"; the body says "Date range: 2020/01/01 to 2026/07/17", and
`literature_gap_data.json` carries `generated: 2026-07-17T10:14:41`. Something re-renders the report
over unchanged data and stamps the render time. **[Certain]** — both timestamps read directly.
**Sixth consecutive day flagged.** A file that advertises freshness it does not have is worse than a
file that is visibly stale, because it defeats exactly the staleness check above.

---

## Clinical Trial Changes (08-27 → 08-28 snapshots)

893 trials, up 1. Genuinely quiet.

| | |
|---|---|
| New trials | 1 |
| Status changes | 2 |
| Newly posted results | 0 |

**New:** `NCT04506151` — Sleep Optimization to Improve Glycemic Control in Adults With T1D
(U. Illinois Chicago, NA, COMPLETED, results posted 2026-08-27). Entered the corpus *because* results
posted, not because the trial is new.

**Status changes** — both are backwards, and that is the interesting part:

- `NCT07495956` RECRUITING → **NOT_YET_RECRUITING**
- `NCT07502495` RECRUITING → **ACTIVE_NOT_RECRUITING**

Neither is a trial starting. One un-started, one closed enrollment. **[Likely]** that the first is a
registry correction rather than a real reversal — sponsors rarely walk a trial back to
not-yet-recruiting — but I did not fetch the change history to confirm. To move this to [Certain]:
pull `lastUpdatePostDate` and the version history for NCT07495956 from the API.

**Current composition** (893 trials): COMPLETED 341 · RECRUITING 280 · NOT_YET_RECRUITING 152 ·
ACTIVE_NOT_RECRUITING 114 · ENROLLING_BY_INVITATION 6. **57 are Phase 3 and recruiting.**

### Key organizations — the T1D cure programs

| NCT | Sponsor | Phase | Status | Asset |
|---|---|---|---|---|
| NCT04786262 | Vertex | 3 | RECRUITING | VX-880 (zimislecel) |
| NCT06832410 | Vertex | 3 | RECRUITING | VX-880 (zimislecel) |
| NCT05791201 | Vertex | 1/2 | ACTIVE_NOT_RECRUITING | VX-264 (encapsulated) |
| NCT07222332 | Lilly | 3 | RECRUITING | Baricitinib, β-cell preservation |
| NCT07222137 | Lilly | 3 | RECRUITING | Baricitinib, delay Stage 3 |

**Sana Biotechnology returns zero trials.** The doctrine names Sana as a key organization to track;
the query set does not find it. Either Sana has no registered diabetes trial under a sponsor-name
match, or the query misses it (collaborator-role registration would be invisible — every query is
sponsor-scoped). **[Guessing]** which. To resolve: one `AREA[CollaboratorName]Sana` query, plus a
direct sponsor lookup. This has been silently zero for months.

---

## PubMed Highlights (08-28 snapshot, 30-day window)

163 unique papers, 45 not in the 08-27 snapshot. **Do not read that 45 as "45 new papers."**
Yesterday's report established that 12 of 16 domains are `retmax`-capped, so day-over-day set
differences are substantially sampling churn, not literature flow. That finding stands and this
report does not restate the total as a metric.

### Cross-domain papers — 16 of 163

The T1D cure cluster is where the density is:

| PMID | Domains | Paper |
|---|---|---|
| 42626948 | **4** — Stem Cell, Immunotherapy, Gene Therapy, teplizumab | Gene-edited hypoimmune islets as a cure for T1D: immunological challenges *(Expert Opin Biol Ther)* |
| 42613697 | 3 — Stem Cell, Immunotherapy, Gene Therapy | Regenerative approaches in T1D: β-cell replacement *(Recent Adv Inflamm Allergy)* |
| 42627334 | 2 — Immunotherapy, baricitinib | **β-cell function 1 year after stopping oral baricitinib** *(Diabetes Care)* |
| 42610933 | 2 — Immunotherapy, teplizumab | Baseline serum metabolites predicting teplizumab response *(Diabetes)* |
| 42643804 | 2 — Immunotherapy, teplizumab | Teplizumab in stage 2 T1D — pediatric considerations |
| 42649514 | 2 — Remission, retatrutide | DMADDs: disease interception framing *(Cardiovasc Diabetol)* |

**PMID 42626948 is the highest-value item in this corpus** and is new-ish to the cross-domain set —
four domains including a named therapy, in a review that sits exactly on the Vertex/Sana axis. It is
the paper to read if you read one.

At least one of the 16 is a string-match artifact (a fungal-disease consensus statement tagged
Microbiome × Health Equity, PMID 42657100). **1/16 false-positive rate, unchanged from yesterday.**
Cross-domain output is the hub's most valuable product and its least validated — the precision audit
recommended yesterday is still open.

### Key therapies

| Therapy | Papers (08-28) | Prev | Note |
|---|---|---|---|
| orforglipron | 10 | 13 | |
| retatrutide | 10 | 9 | |
| dapagliflozin | 10 of 34 | 34 | capped |
| icodec | 6 | 5 | |
| CagriSema | 4 | 4 | |
| teplizumab | 4 | 6 | |
| baricitinib | 3 | 4 | bare-term query inflates this ~10× — see 08-28 |
| **zimislecel** | **0** | **0** | |

**Zimislecel has returned zero for the entire tracking period while two Phase 3 trials of the same
asset are actively recruiting.** The literature uses "VX-880." The query does not. Widening the term
to `zimislecel OR "VX-880"` was recommended 08-27 and is still open — it is a one-line fix that
un-blinds the hub's single most important asset.

---

## Gap Analysis Summary

**Data is 43 days old** (`literature_gap_data.json`, generated 2026-07-17). Nothing has changed; the
top five are unchanged from every report since.

| Rank | Intersection | Gap | Joint | Expected |
|---|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 | 7.53 |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 | 7.28 |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 | 4.74 |
| 4 | Glucokinase × Health Equity | 100.0 | 0 | 4.25 |
| 5 | Gene Therapy × LADA | 100.0 | 0 | 3.34 |

**The gap score cannot rank these.** Seven pairs score exactly 100.0 with `pair_count = 0`; the
ordering above is `expected` doing the work, not `gap_score`. Re-rank by `expected − joint`. The
field is already in the file. *(Second consecutive recommendation.)*

### Tier 1 alignment

Four of the top five touch **Health Equity** (Doctrine Tier 1 #6, Epidemiological Data Analysis,
17/20) crossed with a cell/gene therapy domain. That is a coherent, defensible program — *who gets
access to the cures currently in Phase 3* — and it aligns with Tier 1 #2 (Literature Synthesis,
19/20) and #3 (Clinical Trial Intelligence, 18/20).

**But do not act on it yet.** Health Equity has 1,990 publications on the current query and the
19-term expansion recommended on 08-28 has not been run. Four of the top five gaps hang on a query
that is known to be under-specified. Widen it, re-run, *then* rank. Acting now risks building a
literature synthesis on an artifact of one narrow search string. **[Likely]** the equity gaps survive
expansion — 0 joint publications is a large hole to fill — but "likely" is not the bar the Doctrine
sets for a Tier 1 commitment.

---

## Breaking News (08-28 → 08-29)

**One item clears the bar.**

**FDA approves Mounjaro (tirzepatide) for CV risk reduction in T2D — 2026-08-28.** MACE-3 reduction
in adults with T2D and established ASCVD; based on SURPASS-CVOT (NCT04255433, n=13,299, 30 countries,
median 4-year follow-up), which showed non-inferiority to dulaglutide with an 8% lower MACE rate.
First dual GIP/GLP-1 agonist with this indication. **[Certain]** on the approval and trial design —
Lilly investor release plus Medscape, Fierce Pharma, Cardiovascular Business, Healio. **[Likely]** on
the 8% figure — consistent across outlets, primary label not fetched this run.

Why it matters beyond the label: this was a **head-to-head incretin CVOT**, not placebo-controlled.
Read against the ZEUS null (ziltivekimab, HR 0.99) logged on 08-28, the two results together sharpen
the same question — incretin-axis CV benefit is holding up while the anti-inflammatory hypothesis is
not. That contrast is a synthesis opportunity under Tier 1 #2, and it is the kind of cross-trial
pattern the Doctrine's Clinical Trial Intelligence section explicitly asks for.

Checked, no action: retatrutide TRANSCEND-T2D-1 (Lancet, logged), Abbott Libre Duo (logged 08-28),
amycretin Phase 3 setup, ecnoglutide EECOH-1, setmelanotide (not diabetes).

---

## Recommended Actions

**P0**

1. **Build the NCT event feed. Promote from P1.** Three misses in seven days
   (Libre Duo / DIAGNODE-3 / SURPASS-CVOT) is a measurement, not a run of bad luck. One weekly join:
   ~900 tracked NCTs × (`lastUpdatePostDate`, `whyStopped`, `results_posted`) × FDA approvals feed.
   Smaller than any query rewrite on this list and it is now the highest-yield thing in the backlog.
2. **`*_latest.json` is at day 43.** Third consecutive P0. Snapshots land, pointers do not.
   Run locally: `python "C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts\run_daily_local.py"`
3. **Tracker update — SURPASS-CVOT / NCT04255433.** Record the 2026-08-28 CV indication against the
   trial record. This is the concrete deliverable from finding #1.

**P1**

4. **Widen key-therapy terms to development codes** — `zimislecel OR "VX-880"` first. The hub is blind
   to its own headline asset while two Phase 3s recruit. Third consecutive recommendation, one line of code.
5. **Stop `literature_gap_report.md` stamping render time over 42-day-old data.** Sixth consecutive
   flag. Start with `gap_analysis_daily.py` and `refresh.ps1`.
6. **Resolve the Sana zero.** One `AREA[CollaboratorName]` query answers whether it is a real absence
   or a query hole. A named key organization returning zero for months should not go unexamined.
7. **Re-rank gaps by `expected − joint`.** `gap_score` saturates at 100.0 and cannot order the top seven.
8. **Widen the Health Equity query (19-term expansion) before the next gap run,** then re-rank.
   Four of five top gaps depend on it.
9. Carry forward, still open: fix PubMed `retmax` sampling before any longitudinal literature claim;
   add condition-adjacent trial queries (CKD/ASCVD/HF); record per-domain *and* per-therapy query
   strings in snapshot metadata; audit cross-domain precision (1/16 artifact rate).

**P2 — reading**

10. **PMID 42626948** — gene-edited hypoimmune islets, *Expert Opin Biol Ther*. Four domains. Directly
    on the Vertex/Sana axis. **Top of the queue.**
11. **PMID 42627334** — baricitinib 1 year off-treatment, *Diabetes Care*. Third recommendation.
12. **PMID 42610933** — metabolite predictors of teplizumab response, *Diabetes*. Precision-medicine
    angle on an approved T1D immunotherapy.

---

## Evidence Levels (per Research Doctrine)

| Claim | Level | Basis |
|---|---|---|
| FDA approved Mounjaro CV indication 2026-08-28 | **[Certain]** | Lilly investor release + 4 concordant outlets |
| NCT04255433 = SURPASS-CVOT, results posted 2026-07-08, held on disk | **[Certain]** | snapshot record; n=13,299 matches sponsor description |
| Canonical `*_latest.json` unwritten for 43 days | **[Certain]** | mtimes on disk |
| `literature_gap_report.md` renders 07-17 data under an 08-28 stamp | **[Certain]** | report header vs `metadata.generated` in gap data |
| 893 trials, +1, 2 status changes, 0 new results 08-27→08-28 | **[Certain]** | set diff over both snapshots |
| 16/163 cross-domain, ≥1 string-match artifact | **[Certain]** | `domains` field count; artifact inspected |
| Zimislecel literature invisible due to term mismatch | **[Likely]** | 0 hits across all snapshots while VX-880 Phase 3s recruit; not confirmed by running the VX-880 form |
| NCT07495956 reversal is a registry correction | **[Likely]** | direction is atypical; version history not fetched |
| Sana absence is a query hole vs. genuine absence | **[Guessing]** | zero sponsor-name matches; collaborator-role query not run |
| Health Equity gaps survive query expansion | **[Likely]** | 0 joint pubs is a large hole; 19-term expansion unrun |

---

## Sources consulted

- Eli Lilly investor release — FDA approves Mounjaro to reduce CV risk in T2D
  <https://investor.lilly.com/news-releases/news-release-details/fda-approves-lillys-mounjaro-tirzepatide-reduce-cardiovascular>
- Medscape — Mounjaro FDA-approved to reduce CV risk in T2D
  <https://www.medscape.com/viewarticle/lillys-mounjaro-now-approved-reduce-cardiovascular-risk-t2d-2026a1000uk4>
- Fierce Pharma — FDA approves Lilly's Mounjaro to reduce risk of cardio events
  <https://www.fiercepharma.com/pharma/lilly-scores-fda-expansion-mounjaro-reduce-risk-heart-attack-stroke>
- Healio — Mounjaro approved to reduce cardiovascular events in adults with diabetes
  <https://www.healio.com/news/endocrinology/20260828/mounjaro-approved-to-reduce-cardiovascular-events-in-adults-with-diabetes>
- The Lancet — retatrutide TRANSCEND-T2D-1 (checked, already logged)
  <https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(26)00967-0/abstract>

## Self-audit

- **No files were modified.** Review-only run, per the task charter. No data pull was performed, so
  no 08-29 snapshot exists; all trial/PubMed figures are the 08-28 snapshots, one day old.
- The Healio URL returned an empty body on fetch; the approval rests on the Lilly primary release and
  three other outlets, not on that page.
- The "45 new PMIDs" figure is reported but explicitly not used as a literature-flow metric, because
  the `retmax` cap finding from 08-28 invalidates that reading.
- Trial and gap figures are reproducible: set operations over the two named snapshot files.
