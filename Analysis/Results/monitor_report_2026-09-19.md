# Diabetes Research Hub — Monitor Report

**Run:** 2026-09-19 (automated, sandbox)
**Mode:** review only — no existing files modified
**Previous report:** `monitor_report_2026-09-18.md`

---

## Headline

**The collector backlog broke in your favor overnight — PubMed and the gap analysis are now
both fresh. Trials are the only collector still dark, and the standing diagnosis for why is
wrong.**

Four prior reports have attributed the frozen `clinical_trials_latest.json` to a "write-path
split." That diagnosis does not survive a direct test. The file is writable (`test -w` passes),
the script has no conditional guard around the write, and `baseline_pubmed_alerts.py` — which
writes its `_latest` with byte-identical logic — succeeded on 2026-09-18. Whatever is stopping
the trials write, it is not a read-only path or a code-level split. `[Certain]` on the
falsification; `[Guessing]` on the replacement cause. §1a gives the script that settles it.

Separately, and more important than any of the plumbing: **the FDA approved finerenone
(Kerendia) for CKD associated with type 1 diabetes on 2026-09-17** — first new agent for that
population in 30+ years. Two days old. Nothing in the hub tracks it yet. See §5.

---

## 0. Yesterday's predictions, resolved

| # | Prediction (from 09-18) | Outcome |
|---|---|---|
| **A** | Git index fix holds; porcelain stays low | **TRUE.** Porcelain = **1** (one modified audit JSON). No staged deletions. Fix held a second night. |
| **B** | Push executed → ahead-count 0, site date moves off 2026-04-20 | **FALSE branch.** Ahead = **113** (up 1). `origin/main` still `f7e976f`, **2026-04-20**. 152 days unpublished. |
| **C** | Trials refresh executed → `_latest` ≥894, generated after 09-17 | **FALSE branch.** `_latest` holds **858** trials, generated **2026-07-17**. Now **64 days**. |
| **D** | Repaired `Diabetes Drug Repurpose` query returns >10 | **RESOLVED — gap #3 is real.** The 09-18 PubMed pull returned `total_count = 3` for that domain over a 30-day window. The query is not broken; the field is genuinely thin. See §4. |

Prediction D had been open for four runs. It is now closed on data, not inference.

---

## 1. File System Status

| File | Last modified | Age | Status |
|---|---|---|---|
| `pubmed_recent_latest.json` | 2026-09-18 | 1 d | **FRESH — ran overnight** |
| `pubmed_recent_summary.md` | 2026-09-18 | 1 d | **FRESH** |
| `literature_gap_report.md` | 2026-09-18 | 1 d | **FRESH** |
| `literature_gap_data.json` | 2026-09-17 | 2 d | FRESH |
| `literature_gap_matrix.xlsx` | 2026-09-17 | 2 d | FRESH |
| `agent_state.json` | 2026-09-18 | 1 d | FRESH |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 | 13 d | Newest real trial data |
| `clinical_trials_latest.json` | 2026-07-17 | **64 d** | **STALE — cause misdiagnosed, see §1a** |
| `clinical_trials_summary.md` | 2026-07-17 | **64 d** | STALE — same failure point |
| `hub_monitor_report.md` | 2026-07-17 | **64 d** | STALE — `hub_monitor.py` not run since |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | **64 d** | STALE — master tracker |
| `literature_gap_report_enriched.md` | 2026-04-03 | **169 d** | STALE — enrichment pass abandoned |

Net change from 09-18: three files moved from stale to fresh. The PubMed collector is back.
`[Certain]` — all ages from direct `stat` reads this run.

### 1a. The `_latest` diagnosis is wrong — here is the evidence and the test

What the four prior reports asserted: a "write-path split" — the snapshot and the `_latest`
file resolve to different destinations.

What the code actually does (`baseline_clinical_trials.py`, lines 162–170):

```python
json_path   = os.path.join(RESULTS_DIR, f"clinical_trials_snapshot_{TODAY}.json")   # line 162
with open(json_path, "w", encoding="utf-8") as f: json.dump(snapshot, f, indent=2)  # succeeded

latest_path = os.path.join(RESULTS_DIR, "clinical_trials_latest.json")              # line 168
with open(latest_path, "w", encoding="utf-8") as f: json.dump(snapshot, f, indent=2) # did not
```

Same `RESULTS_DIR`. Same mode. No conditional. There is no split.

Three facts that rule out the leading alternatives:

| Test | Result | Rules out |
|---|---|---|
| `test -w clinical_trials_latest.json` | **writable**, perms 700 | Read-only file / permissions |
| `md5sum` latest vs `snapshot_2026-07-17` | **identical** (`b7c4eff4…`) | Partial/corrupt write — it is a clean frozen copy |
| `pubmed_recent_latest.json` vs its 09-18 snapshot | **identical**, both 2026-09-18 04:32 | Code-level bug in the shared `_latest` pattern |

The surviving signature: **`clinical_trials_summary.md` is frozen at the same date.** That file
is written at line 252 — *after* the `_latest` write. So the run is terminating at or just
after line 169, four consecutive times (08-27, 08-28, 09-01, 09-06), each time after the
snapshot landed. `[Likely]` — an exception or kill between lines 165 and 252, not a path problem.

Two candidates I cannot distinguish from the sandbox, because neither leaves a trace here:
OneDrive holding a sync lock on the two *fixed-name* files (dated snapshot names are new files
each run and would sidestep it), or the scheduled run being killed on a wall-clock timeout
immediately after the 600 KB snapshot write. Note `.~lock.Diabetes_Research_Tracker.xlsx#`
sits in the hub root — a stale LibreOffice lock — which is at least circumstantial evidence
that file locking is live in this folder. `[Guessing]`.

**To get this to `[Certain]`, run this on your machine** (read-only except for one temp file
it deletes; it does not touch `_latest`):

```python
# save as Analysis/Scripts/diag_latest_write.py — run: python diag_latest_write.py
import os, json, time, traceback
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Results")
target = os.path.join(R, "clinical_trials_latest.json")
probe  = os.path.join(R, "clinical_trials_latest.json.__probe")

print("exists      :", os.path.exists(target))
print("writable    :", os.access(target, os.W_OK))
print("size        :", os.path.getsize(target))
print("mtime       :", time.ctime(os.path.getmtime(target)))

# 1. can we create a NEW fixed-name file in Results?
try:
    with open(probe, "w") as f: json.dump({"probe": True}, f)
    print("new-file write: OK"); os.remove(probe)
except Exception:
    print("new-file write: FAILED"); traceback.print_exc()

# 2. can we OPEN the real target for write without truncating it?
#    'r+' opens for write but writes nothing -> file content unchanged.
try:
    with open(target, "r+", encoding="utf-8") as f:
        pass
    print("open-for-write on _latest: OK  -> lock theory DEAD, suspect timeout/kill")
except Exception:
    print("open-for-write on _latest: FAILED -> lock theory ALIVE")
    traceback.print_exc()
```

If test 2 fails, the fix is to write `_latest` atomically (write to `.tmp`, then
`os.replace`), which sidesteps a lock on the existing inode. If test 2 passes, the fix is to
reorder: write `_latest` and the summary *before* the 600 KB snapshot, so a timeout costs you
the cheapest artifact instead of the two you actually read.

---

## 2. Clinical Trial Changes

Data below is from `clinical_trials_snapshot_2026-09-06.json` diffed against
`clinical_trials_snapshot_2026-07-17.json` — the two real endpoints. The stale `_latest` was
not used. **All trial intelligence in this section is 13 days old.** `[Certain]` on the diff,
`[Certain]` that it is incomplete for 09-07 → 09-19.

**Volume:** 858 → **894** trials (+36 net; **57 added, 21 dropped**).

| Category | 07-17 | 09-06 | Δ |
|---|---|---|---|
| T1D Cure & Cell Therapy | 152 | 156 | +4 |
| T1D Immunotherapy & Prevention | 76 | 77 | +1 |
| T2D Novel Therapies (Ph 2–3) | 147 | 152 | +5 |
| Diabetes Technology (Devices) | 236 | 245 | +9 |
| Recently Completed with Results | 321 | 343 | +22 |

### New Phase 3 trials (8)

| NCT | Sponsor | Status | Trial |
|---|---|---|---|
| NCT07797335 | **Novo Nordisk** | RECRUITING | AMBITION 7 — zenagamtide |
| NCT07754461 | Boehringer Ingelheim | RECRUITING | Survodutide in T2D |
| NCT07776509 | AstraZeneca | NOT_YET_RECRUITING | AZD6234 adjunct to incretin |
| NCT07784270 | AstraZeneca | NOT_YET_RECRUITING | AZD6234 monotherapy |
| NCT07743450 | Ascletis Pharma | RECRUITING | Oral ASC30 |
| NCT07743983 | BrightGene | RECRUITING | BGM0504 in early T2DM + obesity |
| NCT07804849 | Ain Shams University | RECRUITING | **Oral verapamil, newly-dx pediatric T1D** (Ph 2/3) |
| NCT04596631 | Novo Nordisk | COMPLETED | Oral semaglutide comparator |

NCT07804849 is the one worth a second look: verapamil is a **drug-repurposing** play in
**pediatric T1D beta-cell preservation** — it sits directly on two Tier 1 doctrine areas
(Drug Repurposing Computational Screening, score 18/20) and an academic sponsor means the
protocol will be readable.

### Status changes (26 total; Phase 3 shown)

| NCT | Sponsor | From → To |
|---|---|---|
| NCT07613307 | **Eli Lilly** | NOT_YET_RECRUITING → **RECRUITING** (orforglipron, T2D) |
| NCT07664553 | AstraZeneca | NOT_YET_RECRUITING → RECRUITING (elecoglipron) |
| NCT07684144 | Amgen | NOT_YET_RECRUITING → RECRUITING (extension trial) |
| NCT06334133 | vTv Therapeutics | RECRUITING → ACTIVE_NOT_RECRUITING (**cadisegliatin — glucokinase activator, enrollment closed**) |
| NCT07400653 | Pfizer | RECRUITING → ACTIVE_NOT_RECRUITING (PF-08653944) |
| NCT07076199 | Novo Nordisk | RECRUITING → ACTIVE_NOT_RECRUITING (insulin icodec) |
| NCT07448974 | Tufts | NOT_YET_RECRUITING → RECRUITING (vitamin D, treat-to-target) |
| NCT07428746 | Emory | NOT_YET_RECRUITING → RECRUITING (GLP-1 RA & osteosarcopenia) |

Also notable: **NCT07502495** (Biomea Fusion, icovamenib, Ph2) closed enrollment, and
**NCT06305286** (U Chicago, monoclonal immunomodulation, Ph1/2) closed enrollment.

**Cadisegliatin closing enrollment matters for the gap analysis.** Gap #6 (Glucokinase ×
Drug Repurposing, score 100.0) and gap #8 (Glucokinase × LADA) both rest on glucokinase being
an under-studied class. A Phase 3 GKA finishing enrollment means readout-driven literature is
coming. The window to publish a repurposing screen *ahead of* that literature is closing.
`[Likely]`.

### Results posted

**Zero** new results postings between 07-17 and 09-06 across all 894 trials. That is unusual
for a 51-day window over 343 completed-with-results trials and is worth a sanity check on the
`results_posted` / `has_results` extraction. `[Likely]` an extraction issue rather than a true
zero.

### Key-organization Phase 3 status (as of 09-06)

| Sponsor | Trial | NCT | Status |
|---|---|---|---|
| **Vertex** | VX-880 (zimislecel) | NCT06832410 | RECRUITING |
| **Vertex** | VX-880 + VX-264 | NCT04786262 | RECRUITING |
| **Lilly** | Baricitinib — delay stage 3 T1D | NCT07222137 | RECRUITING |
| **Lilly** | Baricitinib — beta-cell preservation | NCT07222332 | RECRUITING |
| **Lilly** | Orforglipron (ACHIEVE master) | NCT06993792 | ACTIVE_NOT_RECRUITING |
| **Lilly** | Retatrutide vs semaglutide | NCT06260722 | ACTIVE_NOT_RECRUITING |
| **Novo** | CagriSema (glycemic) | NCT07282613 | NOT_YET_RECRUITING |
| **Novo** | CagriSema dose comparison | NCT07564414 | RECRUITING |

**Sana Biotechnology: zero trials in the snapshot.** Either they have no registered diabetes
trial in the queried categories, or the query set misses them. Worth one manual check —
they are on the watch list but have never appeared in the data.

---

## 3. PubMed Highlights

From `pubmed_recent_latest.json`, generated **2026-09-18**, 30-day lookback, 151 unique papers
across 16 domains + 8 tracked therapies. Diff vs the 09-06 snapshot: **104 of 151 papers are
new**. `[Certain]`.

### Cross-domain papers (14 of 151) — highest priority

Three-domain hits first:

1. **PMID 42751099** — *Sustained weight loss exceeding 100 kg with sequential incretin-based
   therapy in Prader-Willi syndrome* · JCEM Case Reports, 2026-Oct
   → T2D GLP-1 New × T2D Remission × **retatrutide**. n=1 case report — evidence level is low,
   but it is the only retatrutide paper this window touching a monogenic obesity syndrome.

2. **PMID 42751271** — *New Insights into the Role of Mitochondrial Dysfunction in Diabetic
   Kidney Disease in the Omics Era* · Diabetes Metab Syndr Obes, 2026
   → Biomarker × Microbiome × **Multi-Omics**. This is the single most doctrine-aligned paper
   in the pull: Tier 1 area #1 (Multi-Omics Biomarker Integration, 19/20), and it lands the
   same week as the finerenone T1D-CKD approval. **Read this one first.**

Two-domain hits worth attention:

- **PMID 42720752** · *Preserving beta cell function in children/adolescents with newly
  diagnosed stage 3 T1D* · **Diabetologia**, 2026-09-10 → T1D Immunotherapy × teplizumab.
  Highest-impact journal in the set. Pairs directly with new trial NCT07804849 (pediatric
  verapamil) above.
- **PMID 42750540** · *Predicting long-term risk of T2D and CVD with orforglipron* ·
  Diabetes Obes Metab, 2026-09-17 → GLP-1 × orforglipron. Modeling study — Tier 1 area #5.
- **PMID 42738899** · *Diabetic immunotherapy advances with BCG* · Cells, 2026-09-03
  → T1D Immunotherapy × **LADA**. LADA crossover is rare; 4 of the top-15 gaps involve LADA.
- **PMID 42750649** · Finerenone vs SGLT2i vs semaglutide cardiorenal comparison ·
  Diabetes Obes Metab, 2026-09-17 → **directly relevant to the finerenone news in §5**.
- **PMID 42688617** · GLP-1 comparative efficacy network meta-analysis · BMJ Medicine, 2026
  → retatrutide × CagriSema. Only paper hitting two tracked therapies.
- **PMID 42739778** · Pancreas/islet transplant preservation technologies · J Clin Med, 2026-08-31
  → T1D Stem Cell Cure × T1D Immunotherapy. Relevant to gaps #2, #3, #4 (all Islet Transplant).

### Publication volume by domain (30-day totals)

| Domain | Total | Read |
|---|---|---|
| T2D GLP-1 New | 202 | 10 |
| Diabetes AI/ML | 190 | 10 |
| Diabetes Microbiome | 140 | 10 |
| Diabetes Biomarker | 116 | 10 |
| Diabetes Health Equity | 59 | 10 |
| T2D Remission | 57 | 9 |
| Diabetes Multi-Omics | 56 | 10 |
| Diabetes Gene Therapy | 53 | 10 |
| Diabetes Complications New | 29 | 10 |
| T1D Immunotherapy | 24 | 10 |
| Closed Loop AP | 23 | 10 |
| T1D Stem Cell Cure | 15 | 10 |
| LADA New Research | 9 | 9 |
| **Diabetes Drug Repurpose** | **3** | 3 |
| **GLP-1 Pharmacogenomics** | **3** | 3 |
| **Diabetes Epigenetics** | **2** | 2 |

**`domain_retmax` is 10 and eleven domains hit that ceiling.** You are reading 10 of 202 GLP-1
papers — 5%. The retrieval is capped, not the field. For the three domains at the bottom the
cap is not binding, which is exactly what makes them informative: **Drug Repurpose (3),
GLP-1 Pharmacogenomics (3) and Epigenetics (2) are genuinely thin, not under-sampled.**
That closes prediction D. `[Certain]`.

### Tracked therapies

| Therapy | 30-day papers |
|---|---|
| dapagliflozin | 46 |
| retatrutide | 13 |
| orforglipron | 10 |
| icodec | 7 |
| teplizumab | 6 |
| CagriSema | 3 |
| baricitinib | 3 |
| **zimislecel** | **0** |

Zimislecel returned **zero** papers for the second consecutive window despite Vertex running
two Phase 3 trials. `[Likely]` the literature still uses "VX-880" rather than the INN.
Recommend adding `VX-880` as an alias in the therapy query set — otherwise the hub will miss
the pivotal publication when it lands.

---

## 4. Gap Analysis Summary

From `literature_gap_report.md` (2026-09-18) and `literature_gap_data.json` (2026-09-17).
30 domains, 435 pairs. **Validation level: BRONZE** — single analytical source, requires
expert confirmation per the Research Doctrine.

### Top 5 under-researched intersections

| # | Intersection | Gap | Joint pubs | Tier 1 alignment |
|---|---|---|---|---|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | **Tier 1 #6** (Epidemiological / disparity analysis, 17/20) |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | Tier 2 |
| 3 | Islet Transplant × Drug Repurposing | 100.0 | 0 | **Tier 1 #4** (Drug Repurposing, 18/20) |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | **Tier 1 #6** |
| 5 | Gene Therapy × LADA | 100.0 | 0 | Tier 2 |

Gap #3 carries the strongest provenance in the report: an all-time unbounded PubMed search
re-run 2026-09-06 returned 7 records, **none** a computational drug screen for islet
protection — the nearest work is bioengineering or single-molecule in-silico structure work.
That is a documented absence, not an inferred one.

### Where the gaps and the doctrine actually converge

Three of the top five, plus #6, #7, #10 and #12, route to **Tier 1 areas #4 (Drug Repurposing,
18/20) and #6 (Epidemiological/Health Equity, 17/20)**. And §3 independently shows Drug
Repurposing is the thinnest domain in the 30-day literature (3 papers). Two independent
signals — gap scores and raw publication volume — point at the same target. `[Likely]` this
is the highest-yield direction available, and it is the one you have full open data access
for (DrugBank, OpenTargets, STRING, Reactome per doctrine).

The counter-argument worth holding: low co-publication in Health Equity × anything may reflect
that equity work is published in health-services journals PubMed indexes under different
terms, not that the work is absent. The report's own caveats flag this. Gap #3's unbounded
re-run is the model — **no gap should be promoted past BRONZE without that kind of
date-unbounded manual confirmation.**

---

## 5. Breaking News

**FDA approves finerenone (Kerendia) for CKD associated with type 1 diabetes — 2026-09-17.**

- First new FDA-approved treatment for this population in **more than 30 years**.
- 10 mg / 20 mg tablets, indicated to reduce urinary albumin-to-creatinine ratio (UACR).
- Reported effect: LS geometric mean UACR ratio **0.75 vs placebo at 6 months**; 22% and 28%
  reductions at months 3 and 6.
- Safety: hyperkalemia **10.1% vs 3.3%** placebo; discontinuation in 1.7%.
- Bayer; selective non-steroidal mineralocorticoid receptor antagonist.

Why it matters to the hub: T1D nephropathy has been a thin cell in the tracker, and the gap
report lists **Islet Transplant × Nephropathy DKD** (99.9, 2 joint pubs) among unclassified
gaps. A first-in-30-years approval will generate a literature wave in that exact cell within
two quarters. It is also independently corroborated inside your own data — **PMID 42750649**
(Diabetes Obes Metab, 2026-09-17) is a finerenone/SGLT2i/semaglutide cardiorenal comparison
that surfaced in the same PubMed pull. The 09-06 snapshot already carries **3 finerenone
trials** — NCT07594145 (Ph2, T1D cardio-renal, not yet recruiting), NCT06906081 (Ph2, T2D
autonomic neuropathy, recruiting), NCT05254002 (Ph2, T2D-CKD, completed) — none of them the
T1D-CKD registration trial behind this approval, which means the hub's trial coverage of
finerenone is incomplete. `[Certain]`.

Secondary, lower confidence: reports indicate insulin efsitora alfa may become the second
weekly basal insulin approved in the US later in 2026, and an FDA decision on tirzepatide
CV benefits in T2D may come in H2 2026. `[Guessing]` — forward-looking, not an action.

Nothing else from the last 7 days clears the significance bar. The retatrutide and
orforglipron Phase 3 readouts circulating in search results are the **June 2026** ADA
presentations, already in the hub — not new.

---

## 6. Recommended Actions

Ranked. Top three are the ones that change what the hub knows.

1. **Refresh trial data — it is 13 days stale and the last two weeks included an FDA approval.**
   ```
   python Analysis/Scripts/baseline_clinical_trials.py
   ```
   Then check immediately whether `clinical_trials_latest.json` moved off 2026-07-17. If it
   did not, run the diagnostic in §1a in the same session while the failure is warm.

2. **Run the §1a diagnostic and fix the write, not the symptom.** Four reports have now
   recommended re-running the collector; the collector has run four times and `_latest` has
   not moved. Re-running without diagnosing is the definition of the loop you are in. The
   likely fix is two lines: write to `.tmp` and `os.replace`, plus move the `_latest` and
   summary writes *above* the 600 KB snapshot write.

3. **Read PMID 42751271** (mitochondrial dysfunction in DKD, omics era) — Tier 1 #1, 3-domain
   cross-hit, and it lands the same week as the finerenone T1D-CKD approval. Then **PMID
   42720752** (Diabetologia, pediatric beta-cell preservation), which pairs with new trial
   NCT07804849.

4. **Add `VX-880` as a query alias for zimislecel** in `baseline_pubmed_alerts.py`. Zero hits
   across two windows while two Phase 3 trials run is a query problem, not a literature fact.

5. **Log the finerenone T1D-CKD approval in the tracker** with the UACR and hyperkalemia
   figures from §5 — evidence level: regulatory approval, Level 1 per doctrine. The tracker
   itself is 64 days stale.

6. **Audit the `results_posted` extraction.** Zero new results postings across 51 days and 343
   completed-with-results trials is more likely a parser fault than a true zero.

7. **Push. 113 commits, `origin/main` frozen at 2026-04-20 — 152 days.** No safety argument
   remains: porcelain is 1, zero staged deletions, two clean nights.
   ```
   git push origin main
   ```

8. **Run `hub_monitor.py`** — its report is 64 days old, so file-change detection has been
   blind for two months.
   ```
   python Analysis/Scripts/hub_monitor.py
   ```

9. **Decide on `literature_gap_report_enriched.md` (169 days).** Either re-run the enrichment
   or delete it — a stale enriched report next to a fresh base report is a citation hazard.

10. **Scope the Drug Repurposing × Islet Transplant screen** (gap #3). It is the best-evidenced
    gap in the report, sits on Tier 1 #4, and §3 independently confirms the domain is thin.
    Data access is fully open. Before any claim, do the date-unbounded manual confirmation
    that gap #3 already models.

---

## 7. Predictions for the next run (falsifiable)

| # | Prediction |
|---|---|
| **A** | If action 1 runs → `clinical_trials_latest.json` ≥ 894 trials, generated after 09-19. If it runs and `_latest` still reads 858/2026-07-17, the lock theory is confirmed and the atomic-write fix is mandatory. |
| **B** | If action 7 runs → ahead-count 0 and `origin/main` moves off `f7e976f`. Else ≥ 114. |
| **C** | If action 4 runs → zimislecel therapy hits > 0 on the next PubMed pull. If still 0 with the `VX-880` alias in place, the absence is real and publishable. |
| **D** | Next trial snapshot will contain ≥ 4 finerenone trials (baseline at 09-06 is **3**: NCT07594145 Ph2 T1D cardio-renal, NCT06906081 Ph2 T2D autonomic neuropathy, NCT05254002 Ph2 T2D-CKD completed) — i.e. ≥ 1 new registration or label-expansion study posted after 2026-09-17. |

---

*Generated by the automated hub monitor, 2026-09-19. Review only — no existing files were
modified. All file ages, counts, and diffs verified by direct read this run. Confidence levels
per Research Doctrine: `[Certain]` = hard evidence in hand, `[Likely]` = strong inference,
`[Guessing]` = gap-filling.*
