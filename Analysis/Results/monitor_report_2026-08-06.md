# Diabetes Research Hub — Monitor Report

**Generated:** 2026-08-06 (automated scheduled run)
**Scope:** Review of latest script outputs in `Analysis/Results/` + web breaking-news check
**Mode:** Read-only review. No existing files modified.

---

## ⚠️ Headline: The data pipeline stalled on July 17

The single most actionable finding this run is that the **baseline data scripts have not refreshed in ~20 days**, even though the daily monitor kept running through Aug 5.

| File | Last refreshed | Age (as of Aug 6) | Status |
|------|----------------|-------------------|--------|
| `clinical_trials_latest.json` | 2026-07-17 | 20 days | **STALE** |
| `pubmed_recent_latest.json` | 2026-07-17 | 20 days | **STALE** |
| `hub_monitor_report.md` | 2026-07-17 | 20 days | **STALE** |
| `literature_gap_data.json` | 2026-07-18 | 19 days | **STALE** |
| `literature_gap_report.md` | 2026-08-05 | 1 day | Fresh output, **stale input** |

The gap report is dated Aug 5 but its own header shows `Date range: 2020/01/01 to 2026/07/17` — it re-ran on the *old* PubMed corpus. The latest dated trial and PubMed snapshots are both `2026-07-17`; nothing newer exists to compare against. **Fix first:**

```
python baseline_clinical_trials.py        # refresh trials (last: Jul 17)
python baseline_pubmed_alerts.py          # refresh PubMed alerts (last: Jul 17)
python project1_literature_gap_analysis.py # re-run gaps on fresh corpus
python hub_monitor.py                     # regenerate file-change report
```

---

## File System Status

The hub tracks **1,057 files** (last full inventory Jul 17). `Analysis/Results/` holds 459 files, plus a healthy backup chain of `agent_state.json.bak_*` running daily through Aug 5 (so the *scheduler* is alive; the *data collectors* are not).

Review flag carried from the last hub scan: **827 result files older than 14 days.** That count is now worse, not better. No files were removed or corrupted.

---

## Clinical Trial Changes

**Corpus (as of Jul 17 snapshot):** 858 trials.

| Category | Count |
|----------|-------|
| Diabetes Technology (Devices) | 236 |
| T1D Cure & Cell Therapy | 152 |
| T2D Novel Therapies (Ph 2–3) | 147 |
| T1D Immunotherapy & Prevention | 76 |
| Recently Completed w/ Results | 321 |

**Status mix:** 269 RECRUITING · 151 NOT_YET_RECRUITING · 110 ACTIVE_NOT_RECRUITING · 321 COMPLETED. **136 trials are Phase 3** (plus 16 Phase 2/3).

**Snapshot movement (Jul 03 → Jul 17, the last two weeks of live data):** +23 new trials, −4 removed (net 839 → 858). New arrivals were mostly newly-registered protocols (NCT076–077 series) plus older device/behavioral trials posting results.

### Key Phase 3 trials to watch (RECRUITING)

- **Vertex — VX-880 (zimislecel):** two Phase 3 trials active — `NCT04786262` (T1D) and `NCT06832410` (T1D + kidney transplant). This is the flagship cell-therapy program.
- **Eli Lilly — baricitinib (BARICADE):** `NCT07222332` (preserve beta-cell function, new-onset) and `NCT07222137` (delay Stage 3 in at-risk). Baricitinib beta-cell preservation moving to Phase 3 is notable.
- **Sanofi — teplizumab:** `NCT07088068`, Phase 3 vs placebo, ages 1–25 with Stage 3 T1D. **See Breaking News — teplizumab just gained a new FDA pediatric indication.**
- **Novo Nordisk — insulin icodec:** `NCT07076199` (weekly insulin in T1D); **CagriSema** `NCT07564414` (obesity ± T2D).

### Recently posted results worth a look

- **`NCT04255433` (Lilly, tirzepatide CV outcomes vs dulaglutide, Phase 3)** — results posted 2026-07-08. A cardiovascular-outcomes readout for tirzepatide is high-value given the 2026 ADA Standards elevating CV/kidney risk to a co-primary goal.
- **`NCT03263494` (Jaeb, CGM in teens/young adults T1D, Phase 3)** — results posted 2026-07-09.
- **`NCT05254002` (Bayer, finerenone + empagliflozin combo, CKD + T2D, Phase 2)** — results posted 2026-07-13; relevant to combination-therapy mapping (Tier 1 #3).

*Note: no trials in the snapshot carry `has_results=true` in the structured field; "results posted" dates above come from the `results_posted` field.*

---

## PubMed Highlights

**Corpus (Jul 17):** 158 unique papers, 30-day lookback across 16 alert domains. Evidence level for anything below: **BRONZE** (single automated source, keyword-matched).

**Key-therapy mentions:** orforglipron (5 papers) · CagriSema (5) · retatrutide (4) · teplizumab (4) · icodec (3) · baricitinib (2) · dapagliflozin (52 hits / 5 papers) · **zimislecel: 0** — worth noting given Vertex's Phase 3 activity; the literature hasn't caught up to the trial program.

**Cross-domain papers (highest value — appear in ≥2 alert domains):**

- `[42459945]` *A framework for assessing algorithmic discrimination risks in training data: pediatric type 1 diabetes* — spans **AI/ML + Closed-Loop AP + Health Equity** (3 domains). Directly on the intersection of two Tier-1 areas.
- `[42419792]` *Comparative effects of obesity drugs: systematic review & network meta-analysis* — orforglipron + retatrutide + CagriSema together.
- `[42453334]` *Noncoding RNAs for diabetes research and therapy* — Biomarker + LADA.
- `[42411999]` *T1D driven by residual recipient T cells after HCT* — Stem-Cell Cure + Immunotherapy.

**Volume note:** the per-domain `domain_results` counts render as low/zero in the current file structure (counts sit in nested `total_count`/`paper_count` objects, not the top level) — a data-shape quirk to confirm on the next refresh, not necessarily a real drop.

---

## Gap Analysis Summary

Top under-researched intersections (from `literature_gap_report.md`, **BRONZE**, requires expert confirmation):

| Rank | Intersection | Gap Score | Joint Pubs |
|------|--------------|-----------|------------|
| 1 | Treg / CAR-T × Neuropathy | 100 | 0 |
| 2 | Beta Cell Regen × Health Equity | 100 | 0 |
| 3 | Treg / CAR-T × Health Equity | 100 | 0 |
| 4 | Glucokinase × Health Equity | 100 | 0 |
| 5 | Gene Therapy × LADA | 100 | 0 |
| (6) | Drug Repurposing × Health Equity | 100 | 0 |

**Alignment with Tier 1 contribution areas (RESEARCH_DOCTRINE):** four of the top six intersect **Health Equity (Tier 1 #6, Epidemiological/Disparity Analysis)** — Beta Cell Regen, Treg/CAR-T, Glucokinase, and Drug Repurposing all vs. equity. The Drug Repurposing × Health Equity gap also touches **Tier 1 #4 (Drug Repurposing Screening)**. These are the strongest candidates for a computational literature-synthesis contribution (Tier 1 #2), because they combine a real gap with domains where the hub already has data access and tooling.

**Caveat per doctrine:** a gap score of 100 with 0 joint pubs can reflect genuine white space *or* terminology mismatch. Verify each with a combined-term PubMed query and a Cochrane/PROSPERO check before treating as a contribution target.

---

## Breaking News (web check, last ~30 days — flagged because all post-date the Jul 17 data cutoff)

All items below are **secondary-source / news-tier evidence (SILVER at best)** pending primary confirmation:

- **Teplizumab (Tzield) — new FDA indication, June 12, 2026:** accelerated approval to delay insulin decline in pediatric patients (ages 8–17) recently diagnosed with **Stage 3** T1D. This directly maps to Sanofi's Phase 3 `NCT07088068` in the tracker and to the 4 teplizumab papers in the PubMed feed. First approved therapy for that indication.
- **Insulin efsitora alfa (Lilly) — near/at FDA decision** for T2D. The QWINT Phase 3 trials (`NCT05662332`, `NCT05362058`, `NCT05462756`) already show COMPLETED in the snapshot.
- **Garzulys (insulin aspart-fsan) biosimilar — FDA approved July 30, 2026** (rapid-acting, biosimilar to NovoLog).
- **First generic dapagliflozin tablets — FDA approved.** Relevant to affordability/equity gap analysis and to the 52 dapagliflozin PubMed hits.
- **Retatrutide (triple-hormone GIP/GLP-1/glucagon) — Phase 3 T2D + obesity results at ADA 2026 (June):** ~1.7–1.9% HbA1c reduction and up to ~30% body-weight loss on longest/highest-dose arms. Tracked as ACTIVE trials (`NCT05929079`, TRANSCEND series). Context: 2026 ADA Standards now treat CV/kidney risk as a co-primary goal alongside A1C.

---

## Recommended Actions

1. **Refresh the data pipeline first — everything else is downstream of stale inputs.** Run `baseline_clinical_trials.py`, `baseline_pubmed_alerts.py`, then `project1_literature_gap_analysis.py`, then `hub_monitor.py`. Investigate *why* the two baseline collectors stopped on Jul 17 while the scheduler/backup kept running (likely a silent failure in the two `baseline_*.py` jobs).
2. **Update the tracker with the teplizumab FDA indication** and cross-link Sanofi `NCT07088068`. This is the most significant real-world change since the last live data and is not yet reflected in the corpus.
3. **Verify the four Health-Equity gap intersections** (Beta Cell Regen, Treg/CAR-T, Glucokinase, Drug Repurposing × Equity) with combined-term PubMed + Cochrane/PROSPERO checks. These are the best-aligned Tier-1 contribution candidates.
4. **Review cross-domain paper `[42459945]`** (algorithmic discrimination in pediatric T1D) — sits on AI/ML + Closed-Loop + Health Equity, three tracked domains, and is directly relevant to the equity gaps above.
5. **Confirm the `domain_results` count structure** on the next PubMed refresh — current top-level counts read as zero because values are nested; rule out a real reporting regression.
6. **Flag zimislecel/VX-880 literature lag:** Vertex has two Phase 3 trials but 0 PubMed hits for zimislecel in the feed — consider a targeted literature pull once data refreshes.

---

*Report by automated Diabetes Hub monitor. Evidence levels noted per RESEARCH_DOCTRINE (BRONZE = single/automated source; SILVER = news/secondary). No claims here are GOLD-verified — treat as leads, not conclusions.*
