# Diabetes Research Hub — Monitor Report
**Generated:** 2026-04-20 (refreshed after same-day Python runs — baselines + gap analysis)
**Scan window:** 2026-04-19 07:05 → 2026-04-20 10:35
**Previous report:** monitor_report_2026-04-19.md

---

## File System Status

| File | Last Modified | Age | Status |
|------|--------------|-----|--------|
| hub_monitor_report.md | 2026-04-20 10:23 | fresh | OK |
| clinical_trials_latest.json | 2026-04-20 10:22 | fresh | OK |
| clinical_trials_summary.md | 2026-04-20 10:22 | fresh | OK |
| pubmed_recent_latest.json | 2026-04-20 10:23 | fresh | OK |
| pubmed_recent_summary.md | 2026-04-20 10:23 | fresh | OK |
| literature_gap_report.md | 2026-04-20 10:35 | fresh | OK |
| literature_gap_data.json | 2026-04-20 10:35 | fresh | OK |
| Diabetes_Research_Tracker.xlsx | 2026-04-17 14:50 | 3 days | OK |

**Summary.** Daily Python scripts executed successfully on 2026-04-20. `hub_monitor_state.json` was re-baselined this run (likely because the state file recorded Linux-style mount paths from a prior scheduled-run environment and today's run wrote Windows paths), so the surface-level "720 added / 711 removed" figure reflects state rebaselining, *not* actual file churn. The authoritative signal is the automated snapshot-diff block at the end of `hub_monitor_report.md`, which shows the real change picture:

- **Clinical Trials (2026-04-19 → 2026-04-20):** 0 new, 0 removed, 0 status changes, 0 new results posted.
- **PubMed (2026-04-19 → 2026-04-20):** +15 new papers, −15 dropped (normal 30-day rolling-window churn; corpus stays at 142 unique papers).

One genuinely new artifact showed up in the scan today: `Analysis/Results/iterate_run_report_2026-04-20.md` and `Analysis/Results/scheduled_run_report_2026-04-20.md` (scheduled-run outputs — not in scope for this monitor pass).

---

## Clinical Trial Changes

**Total trials tracked:** 767 across five categories — T1D Cure & Cell Therapy 151, T1D Immunotherapy & Prevention 71, T2D Novel Therapies P2–3 137, Devices 222, Recently Completed w/ Results 260. Counts unchanged from yesterday.

### Day-over-day diff (2026-04-19 → 2026-04-20)

Quiet cycle. **0 new trials, 0 removed, 0 status changes, 0 new results posted.** Snapshot file sizes differ slightly (515.7 → 528.4 KB), reflecting whitespace/field re-ordering from ClinicalTrials.gov rather than content change.

### Status summary across the 767-trial corpus

| Status | Count |
|--------|-------|
| RECRUITING | 265 |
| COMPLETED | 260 |
| NOT_YET_RECRUITING | 130 |
| ACTIVE_NOT_RECRUITING | 107 |
| ENROLLING_BY_INVITATION | 5 |

Phase mix: PHASE3 = 116, PHASE2 = 123, PHASE2/3 = 16. Top sponsors: Eli Lilly 26, Novo Nordisk 23, Medtronic MiniMed 11, Insulet 10, University of Chicago 8.

### Key-sponsor Phase 3 RECRUITING roster (unchanged)

- **Vertex (3):** NCT06832410, NCT04786262 (VX-880 / zimislecel), NCT05791864 (VX-264).
- **Eli Lilly:** NCT07222137, NCT07222332 (baricitinib — stage-3 delay & BARICADE-PRESERVE); NCT06993792, NCT06972472 (orforglipron master protocol + OSA cohort); NCT06739122 (dulaglutide pediatric).
- **Novo Nordisk:** NCT07076199 (weekly insulin icodec); CagriSema Phase 3 series (NCT06221969, NCT06534411, NCT07282613).
- **Sana Biotechnology:** 0 trials in snapshot (unchanged).

### Recent results posted (last 14 days, most recent first)

1. NCT05238142 — 2026-04-16 — MiniMed 780G AHCL in T2D, in-home.
2. NCT05727579 — 2026-04-15 — Dietary sodium × ertugliflozin on GFR.
3. NCT06206525 — 2026-04-15 — Inpatient insulin dosing calculator.
4. NCT00690326 — 2026-04-15 — Behavioral change / physical activity, T2D.
5. NCT05923827 — 2026-04-14 — Omnipod 5 + Libre 2 vs MDI, T1D.
6. NCT05144984 — 2026-04-09 — Semaglutide + NNC0487 combination.
7. NCT06141941 — 2026-04-09 — CGM use in immediate postpartum period.

No new results posted since the 2026-04-19 snapshot.

---

## PubMed Highlights

**Lookback:** 30 days. **Unique papers (2026-04-20):** 142. **Day-over-day:** +15 new / −15 dropped. **Domains queried:** 16. **Key therapies tracked:** 8.

### New cross-domain paper today

- **PMID 41999447 (2 domains)** — *Advances in Therapy*, 2026-04-18. "Reconsidering Obesity in India Through a Gut-Metabolic Lens: Mechanistic Insights and the Emerging Role of Synbiotics in Individuals with the Thin-Fat Phenotype." **Tagged:** *Diabetes Microbiome / Diabetes Multi-Omics*. **Hub linkage:** feeds the currently-Unclassified Microbiome × Multi-Omics gap cell and is directly relevant to the `microbiome_ml_*` pipeline outputs. Candidate ingest for the phase-3 microbiome ML report.

### Full cross-domain set (11 papers, ≥2 domain tags) — unchanged except for above new entry

- **PMID 41997446 (3)** — GIPR:GCGR co-agonism in obese rodents — *T2D GLP-1 New / T2D Remission / retatrutide*.
- **PMID 41995155 (2)** — Immune-evasive islet replacement — *T1D Stem Cell Cure / Gene Therapy*.
- **PMID 41889910 (2)** — Donor-derived CD8 (bioRxiv) — *T1D Stem Cell Cure / T1D Immunotherapy*.
- **PMID 41913320 (2)** — Personalized medicine in T1D — *T1D Immunotherapy / teplizumab*.
- **PMID 41992023 (2)** — Oral vs SC GLP-1 cardiometabolic NMA — *T2D GLP-1 New / orforglipron*.
- **PMID 41987895 (2)** — Novel antidiabetics in T2D + CKD — *T2D GLP-1 New / dapagliflozin*.
- **PMID 41993554 (2)** — Colonic metabolomic/transcriptomic alterations, metabolic syndrome — *Biomarker / Microbiome*.
- **PMID 41990508 (2)** — Renal GGT imaging probe, DN — *Biomarker / Complications*.
- **PMID 41988036 (2)** — Gut microbiome–epigenetic crosstalk — *Microbiome / Multi-Omics*.
- **PMID 41986815 (2)** — Multi-tissue multi-omics → drug candidates, T1D (*Diabetologia*) — *Drug Repurposing / Multi-Omics*. **Tier 1 alignment.**

### Key-therapy mentions (30-day title/abstract)

| Therapy | Today | Yesterday | Notes |
|---------|-------|-----------|-------|
| orforglipron | 5 | 5 | Stable. PMIDs 41765029 (vs oral semaglutide), 41994902 (bioequivalence), 41984238 (methodological critique). |
| teplizumab | 4 | 4 | Stable. Key cross-domain PMID 41913320. |
| retatrutide | 3 | 3 | Stable. PMID 41997446 (triple-agonist mechanism). |
| dapagliflozin | **30** | 33 | Down 3 (corpus rolling out of 30-day window). Notable: PMID 41991273 (DAPA-ICU RCT protocol, BMJ Open); PMID 41984016 (JACC CV-effectiveness, cross-domain); PMID 41975024 (eGFR-slope real-world analysis). |
| zimislecel, CagriSema, baricitinib, icodec | 0 | 0 | Persistent zero — synonym expansion recommended (see Actions). |

### Domain publication-volume deltas (today vs yesterday)

| Domain | Today | Yesterday | Δ |
|--------|-------|-----------|---|
| Diabetes AI/ML | 166 | 169 | −3 |
| T2D GLP-1 New | 151 | 150 | +1 |
| Diabetes Microbiome | 137 | 145 | −8 |
| Diabetes Biomarker | 139 | 137 | +2 |
| Diabetes Health Equity | 59 | 62 | −3 |
| T2D Remission | 57 | 57 | 0 |
| Diabetes Multi-Omics | 47 | 47 | 0 |
| Diabetes Gene Therapy | 38 | 39 | −1 |
| Diabetes Complications New | 32 | 34 | −2 |
| T1D Immunotherapy | 22 | 21 | +1 |
| Closed Loop AP | 22 | 21 | +1 |
| T1D Stem Cell Cure | 16 | 17 | −1 |
| Diabetes Epigenetics | 7 | 8 | −1 |
| Diabetes Drug Repurpose | 4 | 5 | −1 |
| LADA New Research | 3 | 3 | 0 |
| GLP-1 Pharmacogenomics | 1 | 1 | 0 |

Net: ~1% volume drift — normal rolling-window behavior. No domain flagged as anomalous.

---

## Gap Analysis Summary

Source: `literature_gap_data.json` and `literature_gap_report.md` (both 2026-04-20 10:35 — **refreshed this cycle**). 30 domains, 435 pair queries against PubMed (2020/01/01 → 2026-04-20). Top 5 meaningful under-researched intersections (BRONZE validation; Gap Score = 100.0 — **top 5 unchanged from prior run**):

1. **Beta Cell Regen × Health Equity** — 0 joint pubs (d1=1,393 / d2=1,872). *(Tier 1: Epidemiological / Health Equity.)*
2. **Insulin Resistance × Islet Transplant** — 1 joint pub (d1=18,889 / d2=242).
3. **Islet Transplant × Drug Repurposing** — 0 joint (d1=242 / d2=577). ***Tier 1 Drug Repurposing; aligns with our `islet_repurposing_*` pipeline.***
4. **Islet Transplant × Health Equity** — 0 joint (d1=242 / d2=1,872).
5. **Gene Therapy × LADA** — 0 joint (d1=2,149 / d2=547).

**Domain-volume drift (this-run vs prior):** Beta Cell Regen 1,394→1,393; Insulin Resistance 18,844→18,889 (+45); Health Equity 1,865→1,872 (+7); LADA 543→547 (+4); Drug Repurposing 574→577 (+3); Gene Therapy 2,146→2,149 (+3); Microbiome Gut 9,741→9,770 (+29). Islet Transplant flat at 242. Drift is <1% across the board — **no domain has crossed a gap-threshold boundary**, which is why the top 25 ranking is effectively identical.

**Tier 1 alignment.** Three of the top 5 map to Tier 1 contribution areas. Today's new cross-domain paper **PMID 41999447** (Microbiome × Multi-Omics) landed after the PubMed baseline was built but is consistent with the refreshed Microbiome domain growth (+29). Combined with PMID 41988036 and PMID 41986815 already in the corpus, the Microbiome / Multi-Omics / Drug-Repurposing triangle now has three cross-tagged papers inside the 30-day window — these are the strongest signals for the next deep-dive queue.

---

## Breaking News (web, last 7 days)

Two items meet the "significant" threshold; the teplizumab item is the highest-stakes because a PDUFA decision is 9 days away.

- **FDA priority review of teplizumab (Tzield) sBLA for children as young as 1 year.** PDUFA target action date **2026-04-29**. The sBLA seeks to expand the current indication from ≥8 years to ≥1 year for delay of Stage 3 T1D in pediatric Stage 2 patients; supported by 1-year interim data from the Phase 4 PETITE-T1D study. **Hub linkage:** teplizumab is a tracked key therapy (4 papers in the current 30-day window; 2 active sponsored trials NCT05757713 and NCT04598893). *Evidence level: GOLD (FDA filing).*
- **Stanford meta-analysis: PAM gene variants predict reduced GLP-1 RA response** (n=1,119 across 3 trials). Carriers of peptidylglycine α-amidating monooxygenase variants showed smaller HbA1c reductions on GLP-1 RA therapy. **Hub linkage:** directly populates the *GLP-1 Pharmacogenomics* domain (total_count = 1 in our 30-day snapshot) and the `glp1_pharmacogenomics_equity_synthesis.md` artifact. *Evidence level: SILVER (peer-reviewed meta-analysis).*

Previously captured, restated for continuity: ACHIEVE-4 Phase 3 topline for orforglipron (2026-04-16); FDA approval of Foundayo (orforglipron) for weight management (early April); FDA first-generic dapagliflozin (2026-04-07); Apotex generic semaglutide ANDA tentative approval (2026-04-10, blocked by exclusivity).

---

## Recommended Actions

1. **Add teplizumab PDUFA date to tracker.** Diabetes_Research_Tracker.xlsx should carry a dated event for the **2026-04-29** FDA decision on Tzield pediatric sBLA (age ≥1 expansion). Flag GOLD. Cross-check `teplizumab_sNDA_decision_prep.md` — if it does not yet reference the ≥1-year population, update it.
2. **Ingest Stanford PAM-variant / GLP-1 resistance finding.** Add to `glp1_pharmacogenomics_equity_synthesis.md` (or create `glp1_pharmacogenomics_pam_variant_signal.md`); SILVER evidence; cross-link with our GLP-1 Pharmacogenomics domain (still n=1 after today's refresh).
3. **Promote PMID 41999447 to deep-dive queue.** Today's only new cross-domain paper (Microbiome × Multi-Omics); candidate for the phase-3 microbiome ML report and a row in `cross_domain_paper_review_2026-04-03.md`.
4. **Continue tracking PMIDs 41986815 and 41995155** already in the deep-dive queue — multi-omics→drug candidates (Diabetologia) and immune-evasive islet replacement. These are the highest-leverage Tier 1 signals in the 30-day corpus.
5. **Broaden PubMed therapy synonyms in `baseline_pubmed_alerts.py`.** Add `VX-880`, `cagrilintide + semaglutide`, `LY3009104` aliases. Current 30-day returns 0 hits for zimislecel, CagriSema, and baricitinib despite active Phase 3 activity (NCT06832410, NCT04786262, NCT06221969, NCT06534411, NCT07222137, NCT07222332).
6. **Seed `clinical_trials_summary.md` "Notable Trials to Watch" table** with Vertex VX-880, Lilly baricitinib, Lilly orforglipron, and Novo icodec entries. Still empty scaffold.
7. **Reset hub_monitor baseline expectation.** Today's 720/711 add/remove counts are a state-rebaselining artifact (Windows vs Linux paths in `hub_monitor_state.json`). Tomorrow's run should return to small-number differentials; if it does not, inspect `hub_monitor_state.json` for path drift.
8. **Watchlist (unchanged):** NCT07528105 (allogeneic anti-CD7 CAR-T for T1D); NCT07527078 (GZR33 Phase 3 T2D); NCT07527650 (HM15275 Phase 2, Hanmi).
9. **No action needed** on NCT07536516 (ocular-blood-flow observational).

---

## Validation Notes

All findings above are BRONZE (single-source analytic) or WEB-SEARCH-BRONZE/SILVER/GOLD per Research Doctrine v1.0 as labeled inline. Source PMIDs and NCT IDs are provided for independent verification. Trial counts and day-over-day diffs are taken from the automated `Snapshot Diffs` section at the tail of `hub_monitor_report.md` (2026-04-20 10:23 run). Cross-domain paper identification comes from `pubmed_recent_latest.json` `domains` array. No source files were modified in this run — this is a review-only artifact.

---
*Generated automatically by the Diabetes Research Hub monitor — 2026-04-20 (refresh after same-day Python runs: baseline_clinical_trials.py, baseline_pubmed_alerts.py, hub_monitor.py, project1_literature_gap_analysis.py).*
