# Diabetes Research Hub — Monitor Report

**Generated:** 2026-05-31 (automated scheduled task)
**Scope:** Review of latest pipeline outputs in `Analysis/Results/`, 7-day snapshot comparison, web check for breaking news.
**Validation level:** BRONZE (single-source automated review; expert validation required before any tracker write).

---

## File System Status

All four expected primary pipelines produced fresh files today:

| File | Last modified | Status |
|------|--------------|--------|
| `hub_monitor_report.md` | 2026-05-31 07:05 | Current |
| `clinical_trials_latest.json` | 2026-05-31 07:05 | Current (804 trials) |
| `pubmed_recent_latest.json` | 2026-05-31 07:05 | Current (165 unique papers, 30-day lookback) |
| `literature_gap_report.md` | 2026-05-30 08:09 | Current (1 day) |
| `literature_gap_data.json` | 2026-04-20 15:35 | **STALE — 41 days old** |

Snapshot history is dense (daily snapshots present for both clinical trials and PubMed through 2026-05-31).

**Stale-file flag from hub_monitor.py:** 658 result files older than 14 days. The two material gaps are the raw `literature_gap_data.json` (41 days) and most non-snapshot derivative files — the gap-analysis markdown was regenerated 2026-05-30 but the underlying counts JSON has not been refreshed.

---

## Clinical Trial Changes (7-day diff: 2026-05-24 → 2026-05-31)

**Volume:** 797 → 804 trials (+7 net; no removals).

**Category counts (today):** T1D Cure & Cell Therapy 154 · T1D Immunotherapy & Prevention 72 · T2D Novel Therapies (Phase 2-3) 141 · Diabetes Technology 226 · Recently Completed w/ Results 284.

**New trials this week (7):**
- `NCT07613307` PHASE3 NOT_YET_RECRUITING — Orforglipron (LY3502970) in T2D patients observing Ramadan — **Eli Lilly** (key org, Tier-1 therapy)
- `NCT07614412` PHASE2 NOT_YET_RECRUITING — SHIELD-T1D: Shingrix + GLP-1 agonist for beta-cell preservation in recent-onset T1D — Saudi MoH (cross-cuts T1D Immunotherapy × Drug Repurposing — relevant to a Tier-1 gap)
- `NCT07610213` PHASE1 NOT_YET_RECRUITING — Sequential immune modulation + antigen-specific tolerance induction
- `NCT07611721` NA RECRUITING — Dexcom G7 CGM performance evaluation
- `NCT07613489` NA ACTIVE_NOT_RECRUITING — Photobiomodulation for diabetic peripheral neuropathy
- `NCT04426474` PHASE1 COMPLETED — Orforglipron in T2D (results posted 2026-05-26) — **Eli Lilly**
- `NCT03242343` NA COMPLETED — VasQ AV fistula support (peripheral relevance)

**Notable status changes (9):**
- `NCT07564414` **CagriSema** Phase 3 (Novo Nordisk) → moved NOT_YET_RECRUITING → **RECRUITING**
- `NCT07284511` Tirzepatide adjunct in T1D AID — Phase 2/3 → RECRUITING
- `NCT07527650` HM15275 in T2D — Phase 2 → RECRUITING
- `NCT06728059` ML bolus priming (T1D) → COMPLETED with results
- `NCT07599982` MODI insulin titration algorithm → RECRUITING
- Three others moved RECRUITING → ACTIVE_NOT_RECRUITING (routine progression)
- `NCT07124208` Biophoton T2D therapy went RECRUITING → NOT_YET_RECRUITING (review for anomaly)

**Phase 3 RECRUITING with key sponsors (current snapshot, all worth tracking):**
- Vertex: `NCT06832410` and `NCT04786262` — VX-880 T1D islet cell therapy (both Phase 3, recruiting)
- Eli Lilly: `NCT07222137` and `NCT07222332` (Baricitinib for T1D delay/preservation), `NCT06739122` (Dulaglutide pediatric T2D), `NCT07613307` (Orforglipron Ramadan, new this week)
- Novo Nordisk: `NCT07076199` (Insulin icodec), `NCT07564414` (CagriSema, newly recruiting)
- Sana Biotechnology: **0 trials** currently captured. If active trials are expected, verify the search query in `baseline_clinical_trials.py`.

**Recent results posted (since 2026-05-24, 1 new):**
- `NCT06728059` (2026-05-28) — ML bolus priming feasibility (small T1D study)

**Recent Phase 3 results worth review (since 2026-05-01):**
- `NCT05514535` (2026-05-11) **Novo Nordisk** — Semaglutide + lower insulin dose in T2D (Phase 3)

---

## PubMed Highlights (30-day lookback, 165 unique papers)

**7-day delta (May 24 → May 31):** 156 → 165 unique papers; 107 new PMIDs entered the rolling 30-day window (rotation, not net growth).

**Domain volume snapshot — every domain at the per-query cap (10) except:**
- LADA New Research: 8
- Diabetes Drug Repurpose: 7
- GLP-1 Pharmacogenomics: **2** (persistent low signal — verify query terms)

**Cross-domain papers (13 total; highest-value items):**

| PMID | Date | Domains | Title |
|------|------|---------|-------|
| 42163482 | 2026-05-20 | T1D Stem Cell Cure × T1D Immunotherapy × teplizumab | Extracellular Vesicle Proteins as Predictive Biomarkers |
| 42198313 | 2026-05-19 | orforglipron × retatrutide × CagriSema | Diabetes Mellitus and Stroke: Pathophysiological Connections |
| 42208956 | 2026-05-28 | T2D GLP-1 New × retatrutide | Beyond weight loss: multisystem benefits of obesity medications |
| 42208537 | 2026-05-28 | Diabetes AI/ML × Gene Therapy | Capturing multi-disease states with machine learning |
| 42206849 | 2026-05-28 | Diabetes AI/ML × Microbiome | Early-life proteomic + microbiome features signal obesity risk |
| 42211453 | 2026 | Microbiome × Multi-Omics | Gut microbiota–diabetic peripheral neuropathy research landscape |
| 42208844 | 2026-05-28 | Biomarker × Complications | Comprehensive proteomic meta-analysis for diabetic complications |
| 42209585 | 2026-05-28 | Biomarker × Complications | Thrombin in diabetic retinal pathology (STZ mice) |
| 42199945 | 2026 | Epigenetics × Multi-Omics | Multi-omics MR + colocalization, glycolipid traits |
| 42199793 | 2026 | T2D Remission × dapagliflozin | Dapagliflozin + linagliptin for time-in-range |
| 42138126 | 2026-05-15 | T1D Immunotherapy × teplizumab | US patterns in clinical islet autoantibody ordering |
| 42138080 | 2026-05-15 | T1D Immunotherapy × teplizumab | New and emerging therapies in T1D |
| 42142983 | 2026-05-17 | retatrutide × CagriSema | Bariatric weight-loss audit |

**Key therapy hits (last 30 days):**
- zimislecel: **0** (verify query — drug exists in literature)
- orforglipron: 4 · retatrutide: 5 · CagriSema: 5 · baricitinib: 4 · teplizumab: 5 · icodec: 5 · dapagliflozin: 5

**Notable new therapy paper:** PMID **41535597** (2026-May) — *Teplizumab treatment for stage 2 T1D: a real-world evaluation* — first post-label real-world data; worth pulling full text.

---

## Gap Analysis Summary

`literature_gap_data.json` was last regenerated 2026-04-20 (41 days old). The interpreted `literature_gap_report.md` (2026-05-30) reflects those same underlying counts. **Recommend re-running `project1_literature_gap_analysis.py` to refresh counts.**

**Top 5 meaningful under-researched intersections (from current interpreted report):**

1. **Beta Cell Regen × Health Equity** — gap 100, 0 joint pubs
2. **Insulin Resistance × Islet Transplant** — gap 100, 1 joint pub
3. **Islet Transplant × Drug Repurposing** — gap 100, 0 joint pubs
4. **Islet Transplant × Health Equity** — gap 100, 0 joint pubs
5. **Gene Therapy × LADA** — gap 100, 0 joint pubs

**Alignment with Tier-1 contribution areas (per RESEARCH_DOCTRINE.md / CONTRIBUTION_STRATEGY.md):** Multiple top gaps fall into LADA-focused and equity-focused tiers (gaps #5, #10–#14 all touch LADA, Health Equity, or Drug Repurposing). The new trial `NCT07614412` (SHIELD-T1D: Shingrix + GLP-1) operationally exemplifies the *Drug Repurposing × Autoimmunity* intersection that the gap report flags — a natural cross-reference candidate.

---

## Breaking News (web check, last 7 days)

- **ADA 2026 Scientific Sessions** kick off June 5–8 in New Orleans. Multiple Phase 2/3 readouts expected — including Zealand Pharma's **ZUPREME-1** (petrelintide amylin analog with Roche) in the ADA Official Press Program. Anticipate a large batch of new high-impact items in next week's run.
- **Awiqli (insulin icodec-abae)** was FDA-approved as the first once-weekly basal insulin for T2D earlier in 2026 (March 26); this is already reflected in the PubMed icodec signal but should be cross-checked against tracker entries.
- **Langlara (insulin glargine-aldy)** — interchangeable Lantus biosimilar — approved 2026-04-29.
- **Orforglipron** (Eli Lilly oral GLP-1) — approval path active; matches the new Phase 3 trial NCT07613307 added this week.

No urgent breaking findings from the last 7 days that require immediate tracker updates beyond the items above.

---

## Recommended Actions

1. **Re-run gap analysis:** `python project1_literature_gap_analysis.py` — underlying `literature_gap_data.json` is 41 days old; ADA Scientific Sessions next week will further stale it.
2. **Verify two zero-hit queries:**
   - `zimislecel` returned 0 PubMed hits and `Sana` returned 0 trials. Either the term coverage or the sponsor matching in `baseline_pubmed_alerts.py` / `baseline_clinical_trials.py` needs a check.
3. **GLP-1 Pharmacogenomics** domain at 2 papers vs. cap 10 — likely query mismatch; review search terms.
4. **Tracker candidates (no writes performed — for justin to review and add):**
   - `NCT07564414` CagriSema Phase 3 moved to RECRUITING (Novo Nordisk).
   - `NCT07613307` Orforglipron Ramadan Phase 3 (Eli Lilly, new).
   - `NCT07614412` SHIELD-T1D Shingrix + GLP-1 for beta-cell preservation — directly addresses a Tier-1 cross-domain gap; consider for the LADA/Drug-Repurposing watch list.
5. **Pull full text:** PMID 41535597 (teplizumab real-world stage-2 T1D evaluation) and PMID 42138080 (T1D emerging therapies review) — both high cross-relevance.
6. **Pre-ADA prep:** Add a manual flag for next week's monitor run to expect 3–5× normal PubMed inflow from ADA 2026 abstracts (June 5–8); consider extending the PubMed cap from 10 to 25/domain temporarily.

---

## Sources

- [Awiqli (insulin icodec-abae) FDA approval — Drugs.com](https://www.drugs.com/newdrugs.html)
- [Five drug approvals to watch in 2026 — Drug Discovery News](https://www.drugdiscoverynews.com/five-drug-approvals-to-watch-in-2026-16982)
- [ADA 2026 Scientific Sessions announcement](https://www.prnewswire.com/news-releases/the-american-diabetes-association-debuts-the-2026-scientific-sessions-driving-the-future-of-diabetes-care-302780358.html)
- [Zealand Pharma — ADA 2026 ZUPREME-1 presentation](https://www.globenewswire.com/news-release/2026/05/27/3301635/0/en/Zealand-Pharma-to-Present-Data-at-the-American-Diabetes-Association-s-2026-Scientific-Sessions.html)
- [ADA Standards of Care in Diabetes — 2026](https://diabetes.org/newsroom/press-releases/american-diabetes-association-releases-standards-care-diabetes-2026)

*Generated by Diabetes Hub Monitor (automated). No source files were modified.*
