# Diabetes Research Hub — Monitor Report

**Run date:** 2026-09-15 (Tuesday, automated)
**Prior report:** monitor_report_2026-09-14.md
**Mode:** Review run. No existing hub file modified. One new file written (this report).
**Environment:** Linux sandbox **mounted successfully** — first successful mount in 8 days
(09-07 → 09-14 all failed with the Plan9 `share "c" is not mounted` error). Python executed;
OS mtimes readable; every figure below comes from a file read on disk, not an API re-read.

---

## Headline

**Nothing in this hub has been refreshed since 2026-09-08. The last seven monitor reports were
written over a frozen dataset.**

That is the finding. The pipeline stopped, the monitor kept reporting, and because the sandbox
was down for eight consecutive days no run could read an mtime and notice. Today's mount makes
the gap visible for the first time.

```
  DATA AGE AT 2026-09-15  (bar = 1 char per day since last write)
  ──────────────────────────────────────────────────────────────────────
  agent_state.json             1d  █
  open_findings.md             3d  ███
  literature_gap_data.json     7d  ███████
  literature_gap_report.md     7d  ███████
  pubmed_recent_latest.json    9d  █████████
  clinical_trials_snap 09-06   9d  █████████
  clinical_trials_latest.json 60d  ████████████████████████████████████████████…
  clinical_trials_summary.md  60d  ████████████████████████████████████████████…
  hub_monitor_report.md       60d  ████████████████████████████████████████████…
                                   ▲ stale threshold (14d)
```

---

## 1. File System Status

| File | Last write | Age | Size | Status |
|------|-----------|-----|------|--------|
| `agent_state.json` | 2026-09-14 | 1d | 1,347 KB | OK |
| `open_findings.md` | 2026-09-12 | 3d | 9.6 KB | OK |
| `literature_gap_data.json` | 2026-09-08 | 7d | 124 KB | OK |
| `literature_gap_report.md` | 2026-09-08 | 7d | 11.6 KB | OK |
| `pubmed_recent_latest.json` | 2026-09-06 | 9d | 110 KB | Aging |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 | 9d | 604 KB | Aging |
| `clinical_trials_latest.json` | 2026-07-17 | **60d** | 580 KB | **STALE** |
| `clinical_trials_summary.md` | 2026-07-17 | **60d** | 1.6 KB | **STALE** |
| `hub_monitor_report.md` | 2026-07-17 | **60d** | 5.2 KB | **STALE** |

No target file is missing. All five files the task specifies exist and were read.

*mtime caveat:* this folder is OneDrive-synced, so an OS mtime can record hydration rather than a
write — `extracted_corpus_data.json` picked up a 2026-09-15 10:32 mtime during this run's
directory listing without being written. The staleness conclusions above therefore do **not** rest
on mtime alone: every load-bearing date is corroborated by the file's own internal `generated`
field (07-17T02:05:53 for `clinical_trials_latest.json`, 09-06T09:18:08 for
`pubmed_recent_latest.json`, 09-08T03:17:27 for the gap data).

### 1a. Root cause of the 60-day trial staleness — a silent write-path split

`clinical_trials_latest.json` is not merely old; it is **being bypassed**. Snapshot metadata
shows why:

```
  snapshot 2026-07-17   generated 07-17T02:05:53   858 trials   acquired_by: (none)
  snapshot 2026-08-27   generated 08-27T02:38:38   892 trials   acquired_by: cowork scheduled monitor (sandbox)
  snapshot 2026-09-01   generated 09-01T02:37:47   887 trials   acquired_by: cowork scheduled monitor (sandbox)
  snapshot 2026-09-06   generated 09-06T02:38:16   894 trials   acquired_by: cowork scheduled monitor (sandbox)
```

**`baseline_clinical_trials.py` has not run since 2026-07-17.** [Certain — the `generated`
timestamp inside `clinical_trials_latest.json` is 2026-07-17T02:05:53, and every snapshot after
that date carries an `acquired_by` field the script does not emit.] Since then the cowork
monitor has been replicating the queries and writing **snapshots only** — never updating
`_latest` or `clinical_trials_summary.md`.

Consequence: anything downstream that reads `clinical_trials_latest.json` (858 trials) is
36 trials and two months behind the newest snapshot (894 trials). Category drift over that
window:

| Category | 07-17 (`_latest`) | 09-06 (snapshot) | Δ |
|----------|------------------:|-----------------:|---:|
| T1D Cure & Cell Therapy | 152 | 156 | +4 |
| T1D Immunotherapy & Prevention | 76 | 77 | +1 |
| T2D Novel Therapies (Ph 2-3) | 147 | 152 | +5 |
| Diabetes Technology (Devices) | 236 | 245 | +9 |
| Recently Completed with Results | 321 | 343 | +22 |
| **Total** | **858** | **894** | **+36** |

There is also a **gap in the snapshot series itself**: 2026-07-17 → 2026-08-27, 41 days with no
trial snapshot. Any trial that appeared and disappeared inside that window is unrecoverable
from local data.

---

## 2. Clinical Trial Changes

Diff basis: `clinical_trials_snapshot_2026-09-06.json` vs `clinical_trials_snapshot_2026-09-01.json`.
This is a **09-01 → 09-06 delta, itself 9 days old.** No trial data exists for 09-07 → 09-15.

**Registry composition at 09-06** (n = 894): COMPLETED 343 · RECRUITING 278 ·
NOT_YET_RECRUITING 153 · ACTIVE_NOT_RECRUITING 114 · ENROLLING_BY_INVITATION 6.
Phase 3 RECRUITING: **58**.

### New trials (8)

| NCT | Phase | Status | Sponsor | Title |
|-----|-------|--------|---------|-------|
| NCT07797335 | **PHASE3** | RECRUITING | Novo Nordisk | AMBITION 7 — zenagamtide, blood glucose lowering |
| NCT05872620 | **PHASE3** | COMPLETED | Eli Lilly | Orforglipron in obesity/overweight — **results posted 2026-09-04** |
| NCT07804849 | PH2/3 | RECRUITING | Ain Shams Univ. | Oral verapamil, newly-diagnosed children/adolescents T1D |
| NCT07801820 | PHASE2 | RECRUITING | Shanghai Minwei | MWN109 tablets, T2D |
| NCT07796477 | PHASE2 | NOT_YET_REC. | CSPC Ouyi | SYH2069 injection, uncontrolled T2DM |
| NCT07802327 | NA | NOT_YET_REC. | MicroTech Medical | GX-01S CGM PMCF study |
| NCT07796802 | NA | NOT_YET_REC. | Steno Copenhagen | CGM for in-hospital T2D management |
| NCT04828785 | NA | COMPLETED | UNC Chapel Hill | Food As MedicinE for Diabetes |

### Status changes (3)

| NCT | From → To | Phase | Trial |
|-----|-----------|-------|-------|
| NCT07076199 | RECRUITING → ACTIVE_NOT_RECRUITING | PHASE3 | Insulin icodec, weekly basal (Novo) |
| NCT07228117 | RECRUITING → ACTIVE_NOT_RECRUITING | NA | GATEWAY — MiniMed NMX8-AID in children |
| NCT07282639 | NOT_YET_RECRUITING → RECRUITING | NA | App-Based Certified Diabetes Education |

One trial removed from the registry pull: NCT06717451.

### Newly posted results

**Zero new `results_posted` between 09-01 and 09-06 on already-tracked trials.** The single new
results record arrives attached to a newly-appearing trial: **NCT05872620 (orforglipron, Lilly,
Phase 3, results posted 2026-09-04)** — worth pulling, since orforglipron is on the hub's key-
therapy watch list and this is an obesity/overweight population rather than a T2D one.

### Key-sponsor Phase 3 status (09-06)

| Program | NCT | Phase | Status |
|---------|-----|-------|--------|
| VX-880 / zimislecel (Vertex) | NCT06832410 | PHASE3 | RECRUITING |
| VX-880 + VX-01x (Vertex) | NCT04786262 | PHASE3 | RECRUITING |
| VX-264 (Vertex) | NCT05791201 | PH1/2 | ACTIVE_NOT_RECRUITING |
| Baricitinib — delay Stage 3 T1D (Lilly) | NCT07222137 | PHASE3 | RECRUITING |
| Baricitinib — preserve beta cell fn (Lilly) | NCT07222332 | PHASE3 | RECRUITING |
| Teplizumab (Phase 3) | NCT07088068 | PHASE3 | RECRUITING |
| CagriSema (Novo) | NCT07564414 | PHASE3 | RECRUITING |
| CagriSema (Novo) | NCT07282613 | PHASE3 | NOT_YET_RECRUITING |
| Orforglipron T2D (Lilly) | NCT07613307 | PHASE3 | RECRUITING |
| Retatrutide vs semaglutide (Lilly) | NCT06260722 | PHASE3 | ACTIVE_NOT_RECRUITING |

**No Sana Biotechnology trial appears anywhere in the 894-trial registry.** [Certain for this
pull — the sponsor string never matches.] Sana's hypoimmune islet work is on the hub's watch
list; either it is registered under a partner/academic sponsor (UPMC and Uppsala have both run
Sana-supplied work) or the category queries do not reach it. Worth a targeted check.

### Pipeline defect: the therapy matcher misses its highest-priority target

`zimislecel` returns **0 trials and 0 PubMed papers** — not because the program is quiet, but
because ClinicalTrials.gov titles it **VX-880** and the matcher is a literal string search. The
hub's single most important cure-track asset is invisible to its own alerting. [Certain — both
`clinical_trials_snapshot_2026-09-06.json` and `pubmed_recent_latest.json.therapy_hits` show
zimislecel = 0 while VX-880 returns two active Phase 3 trials.]

---

## 3. PubMed Highlights

Source: `pubmed_recent_latest.json`, generated 2026-09-06, 30-day lookback, 139 unique papers
across 16 domains, 1,025 query matches.

**81 of 139 papers (58%) are new versus the 09-01 snapshot.** Publication turnover is healthy;
the monitoring is not.

### Cross-domain papers — 20 of 139 (14%)

Highest-value first (domain count in brackets):

- **[4] PMID 42694848** — *COL1A2 and APOLD1 Define a Dual-Axis Molecular Framework for Diabetic
  Nephropathy–Retinopathy* — Int J Med Sci.
  Domains: AI/ML · Biomarker · Complications · Multi-Omics.
  **Hits four Tier 1 doctrine areas at once (Multi-Omics Biomarker Integration, AI/ML
  Prediction). This is the single best-aligned paper in the pull.**
- **[3] PMID 42626948** — *Gene-edited hypoimmune islets as a cure for type 1 diabetes: an
  immunologic review* — Expert Opin Biol Ther.
  Domains: T1D Stem Cell Cure · T1D Immunotherapy · teplizumab.
  **Directly relevant to the Sana / hypoimmune question raised in §2.**
- **[3] PMID 42694300** — *Integrated Oral Microbiome and Metabolome Profiling* — Comput Struct
  Biotechnol J. Domains: Biomarker · Microbiome · Multi-Omics.
- **[3] PMID 42673585** — *Efficacy and Safety of GLP-1 RAs and Co-agonists for Weight* —
  **Annals of Internal Medicine**. Domains: orforglipron · retatrutide · CagriSema.
  Highest-impact venue in the pull; covers three watch-list therapies in one synthesis.
- **[2] PMID 42627334** — *β-Cell Function and Diabetes Outcomes 1 Year After Stopping Oral
  Baricitinib Immunotherapy* — **Diabetes Care**. Domains: T1D Immunotherapy · baricitinib.
  **Most actionable single paper.** It reports what happens after baricitinib withdrawal
  precisely while Lilly has two Phase 3 baricitinib trials recruiting (NCT07222137, NCT07222332).
  Durability-after-withdrawal is the open question those trials will be judged on.
- **[2] PMID 42643804** — Teplizumab in stage 2 T1D, pediatric considerations — Ther Adv
  Endocrinol Metab.
- **[2] PMID 42688560** — Treg diversity and dysfunction, Treg-based therapies — Front Immunol.
- **[2] PMID 42695140** — Adjunctive treatments for T1D on automated insulin delivery — Diabetes
  Technol Ther. Domains: T2D GLP-1 · dapagliflozin.
- **[2] PMID 42688617** — GLP-1-based drugs for weight, comparative efficacy — BMJ Medicine.
- Remaining [2]-domain papers: 42676327, 42685619, 42701157, 42695488, 42698931, 42695875,
  42695342, 42688815, 42700824, 42670002, 42683980.

### Key-therapy hit counts (30-day window)

```
  dapagliflozin  ████████████████████████████████████████  41
  retatrutide    ███████████                               11
  icodec         ██████████                                10
  orforglipron   ████████                                   8
  teplizumab     █████                                      5
  CagriSema      ████                                       4
  baricitinib    ███                                        3
  zimislecel                                                 0   ← matcher defect, see §2
```

### Domain volume

```
  T2D GLP-1 New            188 ████████████████████
  Diabetes AI/ML           182 ███████████████████
  Diabetes Microbiome      139 ██████████████
  Diabetes Biomarker       121 █████████████
  Health Equity             56 ██████
  Multi-Omics               55 ██████
  T2D Remission             50 █████
  Gene Therapy              45 █████
  Complications New         32 ███
  Closed Loop AP            24 ██
  T1D Immunotherapy         23 ██
  T1D Stem Cell Cure        15 ██
  LADA New Research          8 █
  GLP-1 Pharmacogenomics     3 ▏
  Diabetes Drug Repurpose    1 ▏
  Diabetes Epigenetics       1 ▏
```

**Anomaly:** `Diabetes Drug Repurpose` = 1 and `Diabetes Epigenetics` = 1 over 30 days.
[Likely] these are query defects, not genuine field silence — epigenetics in diabetes publishes
far more than one paper a month. Both counts should be treated as suspect until the query
strings are inspected. Drug Repurposing is a Tier 1 doctrine area (score 18/20), so a broken
query there is costly.

*Volume deltas vs. the 09-01 snapshot could not be computed — that snapshot's `domain_results`
block does not carry comparable `total_count` values. [Certain — key lookup returns None.]*

---

## 4. Gap Analysis Summary

Source: `literature_gap_data.json` / `literature_gap_report.md`, both generated 2026-09-08
(7 days old — inside the 14-day threshold, no re-run required yet).
30 domains, 435 pairs, PubMed 2020-01-01 → 2026-09-08. **Validation level: BRONZE.**

Using the **interpreted** ranking (the report's "Potentially Meaningful" table), not the raw
`ranked_gaps` array — the raw array's top 5 is contaminated with methodologically-distinct pairs
such as Islet Transplant × GWAS and GWAS × CGM, which the report correctly demotes.

| # | Intersection | Gap | Joint pubs | Tier 1 alignment |
|---|--------------|----:|-----------:|------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | Epidemiological Data Analysis (17/20) |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | Multi-Omics Biomarker Integration (19/20) |
| 3 | Islet Transplant × **Drug Repurposing** | 100.0 | 0 | **Drug Repurposing Comp. Screening (18/20)** |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | Epidemiological Data Analysis (17/20) |
| 5 | Gene Therapy × LADA | 100.0 | 0 | Literature Synthesis & Gap Analysis (19/20) |

**Gap 3 is the one to act on.** It is the only top-5 intersection that maps onto a Tier 1 area
where the hub has both the data access and the computational tooling to produce original work
rather than a review. The report notes an unbounded all-time PubMed re-run on 2026-09-06
returned 7 records, **none of which is a computational drug screen for islet protection** — the
nearest work is bioengineering (immunoisolation, bioartificial pancreas) or single-molecule
in-silico structure work. That is a well-characterised, defensible opening.

Caveat carried forward from the report: a gap score of 100 measures *relative* co-publication
absence, not research need, and BRONZE means single analytical source pending expert
confirmation.

---

## 5. Breaking News (last 7 days)

**Nothing confirmed inside the 7-day window.** [Likely — search returned no item datable to
2026-09-08 → 09-15.] Three items surfaced that are recent but fall outside the window, listed
so they are not re-flagged as new next run:

- **TRANSCEND-T2D-1** (retatrutide, GIP/GLP-1/glucagon tri-agonist, T2D) published in *The
  Lancet*: n = 537, HbA1c reduction up to 2.0%, weight loss up to 16.8% at 40 weeks.
  Registry-side, NCT06297603 and NCT06260722 both still read ACTIVE_NOT_RECRUITING in the 09-06
  snapshot — **the publication is ahead of the hub's registry status.** [Likely]
- **TRIUMPH-2** (retatrutide, obesity + T2D): reported ~July 23, 2026, n = 1,152, up to 20.8%
  weight loss, up to 1.6 pp HbA1c. Outside window; noted for tracker completeness.
- **Zimislecel (Vertex)**: FDA submission timeline accelerated to 2026 under RMAT + Fast Track;
  EMA PRIME; MHRA Innovation Passport. No filing confirmation found. Both Phase 3 trials read
  RECRUITING locally. **If a submission lands, it lands in this window — this is the highest-
  value thing to watch and the hub currently cannot see it (§2 matcher defect).** [Guessing on
  timing; Certain that no confirmation was found today.]

Nothing here meets the "genuinely significant, act today" bar. The significant risk this week is
internal, not external.

---

## 6. Recommended Actions

Ranked by cost-to-fix against consequence-if-ignored.

**1. Run the two dead scripts. Nothing else in this report matters until the data moves.**
```
python baseline_clinical_trials.py      # last real run 2026-07-17 — 60 days
python baseline_pubmed_alerts.py        # last run 2026-09-06 — 9 days
python hub_monitor.py                   # last run 2026-07-17 — 60 days
```
`literature_gap_data.json` is 7 days old and does **not** need a re-run yet; re-run
`project1_literature_gap_analysis.py` when it crosses 14 days (≈ 2026-09-22).

**2. Fix the `_latest` write path in `baseline_clinical_trials.py` — or stop trusting it.**
The cowork monitor writes snapshots but not `_latest`/`_summary`. Every consumer reading
`clinical_trials_latest.json` has been served 07-17 data for two months without any error being
raised. Either point consumers at `max(glob('clinical_trials_snapshot_*.json'))`, or have the
monitor update `_latest` atomically when it writes a snapshot. A silent-staleness assertion —
refuse to serve `_latest` when a newer snapshot exists — would have caught this on 2026-08-27.

**3. Add `VX-880` and `VX-264` as aliases for `zimislecel` in the therapy matcher.**
One-line change. Without it the hub's flagship cure-track program reads as zero activity in both
the trial and PubMed alerting, at exactly the moment a Vertex FDA submission is plausible.

**4. Pull results for NCT05872620** (orforglipron, Lilly, Phase 3 obesity/overweight, results
posted 2026-09-04) and add to the tracker. It is the only new results record in the delta.

**5. Review PMID 42627334** — *β-Cell Function 1 Year After Stopping Oral Baricitinib*,
*Diabetes Care*. Cross-domain (T1D Immunotherapy × baricitinib), directly informs the two
recruiting Lilly Phase 3 baricitinib trials. Highest-leverage read in the pull.

**6. Review PMID 42694848** — four-domain paper spanning AI/ML, Biomarker, Complications and
Multi-Omics; the tightest match to Tier 1 area #1 (score 19/20) in this cycle.

**7. Inspect the `Diabetes Drug Repurpose` and `Diabetes Epigenetics` query strings.**
Counts of 1 over 30 days are implausible. Drug Repurposing is Tier 1 (18/20) and is also gap
intersection #3 below — a broken query there corrupts both the alerting and the gap analysis.

**8. Targeted search for Sana Biotechnology trials under partner/academic sponsors.**
Zero hits across 894 trials means the sponsor-string filter is not reaching the program, not
that the program is absent.

**9. Open work on gap #3, Islet Transplant × Drug Repurposing.** Tier 1 alignment, zero joint
publications, a 7-record all-time search with no computational screen among them. This is the
most defensible original-contribution opening the gap analysis has surfaced.

**10. Backfill or accept the 2026-07-17 → 2026-08-27 snapshot hole (41 days).** Trials that
appeared and closed inside it cannot be recovered locally; a ClinicalTrials.gov historical query
by `LastUpdatePostDate` is the only route.

---

## 7. Falsifiable prediction for the next run

If the scripts in Action 1 are run before the next monitor pass:
`clinical_trials_latest.json` will read **≥ 894 trials** with a `generated` date after
2026-09-15, and `clinical_trials_summary.md` mtime will move off 2026-07-17.
If they are not run, all three 60-day files will read **61+ days** and this report's headline
repeats verbatim.

---

*Evidence levels per Research Doctrine: [Certain] = read directly from a hub file this run.
[Likely] = strong inference from file contents or web search. [Guessing] = gap-filling.
Gap analysis carries its own BRONZE validation level. No existing hub file was modified.*
