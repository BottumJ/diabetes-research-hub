# Monitor Report — 2026-05-27

**Generated:** 2026-05-27 (automated scheduled run)
**Comparison baselines:** 1 day prior (2026-05-26) and 7 days prior (2026-05-20)
**Validation level:** BRONZE (single-source automated scan; expert review required before any contribution claim)

---

## File System Status

| File | Status | Last Modified | Notes |
|------|--------|---------------|-------|
| Analysis/Results/hub_monitor_report.md | OK | 2026-05-27 07:06 | Fresh |
| Analysis/Results/clinical_trials_latest.json | OK | 2026-05-27 07:05 | Fresh — 798 trials |
| Analysis/Results/clinical_trials_summary.md | OK | 2026-05-27 07:05 | Fresh |
| Analysis/Results/pubmed_recent_latest.json | OK | 2026-05-27 07:05 | Fresh — 160 papers, 16 domains |
| Analysis/Results/pubmed_recent_summary.md | OK | 2026-05-27 07:05 | Fresh |
| Analysis/Results/literature_gap_report.md | OK | 2026-05-26 08:07 | 1 day old |
| **Analysis/Results/literature_gap_data.json** | **STALE** | **2026-04-20 15:35** | **36 days old — re-run `project1_literature_gap_analysis.py`** |
| Analysis/Results/agent_state.json | OK | 2026-05-26 08:09 | 1 day old |
| Analysis/Results/citation_validation.json | OK | 2026-05-26 08:07 | 1 day old |
| Analysis/Results/evidence_network.json | OK | 2026-05-26 08:07 | 1 day old |
| Analysis/Results/gap_evidence.json | OK | 2026-05-26 08:07 | 1 day old |
| Analysis/Results/pmid_verification.json | OK | 2026-05-26 08:07 | 1 day old |

Hub-monitor scan summary: **869 tracked files**, 3 new, 29 modified, 0 removed. The hub_monitor itself flagged **648 result files older than 14 days** — most are historical snapshot files (`clinical_trials_snapshot_*` and `pubmed_recent_snapshot_*`), which is expected. The one functionally stale file is `literature_gap_data.json`.

---

## Clinical Trial Changes

### Day-over-day (vs 2026-05-26)
- **New trials added:** 1
  - **NCT04426474** — *A Study of LY3502970 (orforglipron) in Participants With Type 2 Diabetes* — Eli Lilly — Phase 1 — **COMPLETED** — **results posted 2026-05-26**. This is a backfill of an older Lilly orforglipron Phase 1 trial that just posted results; not a new prospective trial.
- **Status changes:** 2
  - NCT07527650 — *HM15275 in T2D* — `NOT_YET_RECRUITING → RECRUITING` (Hanmi long-acting GLP-1/GIP/glucagon tri-agonist competitor)
  - NCT07124208 — *Biophoton Therapy for T2D* — `RECRUITING → NOT_YET_RECRUITING` (regressed; low priority — non-mechanistic intervention)

### 7-day rolling additions (vs 2026-05-20)
5 new trial records, including:
- NCT07599982 — DreaMed Diabetes — MODI insulin titration algorithm safety study
- NCT07604922 — INSERM — vascular/HEMI–SPG signal study in diabetes
- NCT07602036 — Poznan U. Medical — T2D & pregnancy single-arm interventional
- NCT03919877 — Stanford — Precision Diets for Diabetes Prevention — **results posted 2026-05-22**
- NCT04426474 — Lilly orforglipron Phase 1 (as above)

### Snapshot totals (latest)
- 798 unique trials, broken down: 153 T1D cure/cell, 71 T1D immunotherapy, 140 T2D novel therapy, 225 device, 282 completed-with-results
- Active recruiting: 265 | Phase 3: 121 | Phase 3 + RECRUITING: **46**
- Key org footprint: Lilly 28, Novo Nordisk 26, **Vertex 3** (VX-880 Phase 3 still RECRUITING in NCT06832410 and NCT04786262; VX-264 Phase 1/2 ACTIVE_NOT_RECRUITING in NCT05791201)

### Key-therapy trials (status snapshot, no changes from yesterday for these)
| Therapy | Notable trials |
|---------|----------------|
| Teplizumab | NCT07088068 Phase 3 RECRUITING (Sanofi, head-to-head); NCT07216391 Phase 2 NOT_YET_RECRUITING (NIDDK platform trial); NCT06791291 Phase 2 RECRUITING (Japanese pop.) |
| Baricitinib | NCT07222137 / NCT07222332 — Phase 3 RECRUITING (Lilly, T1D delay & beta-cell preservation) |
| Orforglipron (LY3502970) | NCT06993792, NCT06972472 — Phase 3 ACTIVE_NOT_RECRUITING (Lilly obesity/T2D master protocols); NCT05971940 Phase 3 COMPLETED |
| Retatrutide (LY3437943) | NCT06297603, NCT05929079, NCT06260722 — Phase 3 ACTIVE_NOT_RECRUITING (Lilly T2D) |
| CagriSema | NCT06534411 Phase 3 ACTIVE_NOT_RECRUITING; NCT07564414, NCT07282613 Phase 3 NOT_YET_RECRUITING (Novo) |
| Zimislecel (VX-880) | Vertex Phase 3 RECRUITING (NCT06832410, NCT04786262) |

### Most-recent results postings (top 8)
1. **2026-05-26** NCT04426474 — Lilly — *LY3502970 (orforglipron) in T2D* (Phase 1)
2. 2026-05-22 NCT03919877 — Stanford — *Precision Diets for Diabetes Prevention*
3. 2026-05-13 NCT04286555 — Johns Hopkins — *DASH for Diabetes*
4. 2026-05-13 NCT04226027 — Columbia — *Dynamically Tailored Behavioral Interventions*
5. 2026-05-12 NCT02107976 — NIH — *Vitamin C, RBC fragility, diabetes*
6. 2026-05-12 NCT05454891 — UCSF — *Extended Bolus for Meals in Closed-loop*
7. 2026-05-11 NCT05514535 — Novo Nordisk — *Semaglutide + lower-dose insulin*
8. 2026-05-05 NCT03859401 — *Exercise-induced hypoglycemia prevention (T1D, AID)*

---

## PubMed Highlights (last 30-day lookback; latest snapshot dated 2026-05-27)

**Total unique papers tracked:** 160 across 16 alert domains.
**New papers since yesterday:** 27. **New since 7 days ago:** 99.

### Cross-domain papers (highest priority — 12 papers spanning ≥2 alert domains)

The **top 5** by domain coverage and substantive relevance:

1. **PMID 42163482** — *Assessing Extracellular Vesicle Proteins as Predictive Biomarkers for Developing Type 1 Diabetes* — Proteomics, 2026-05-20 — **3 domains: T1D Stem Cell Cure, T1D Immunotherapy, Key Therapy: teplizumab**. Directly relevant to predicting teplizumab responders.
2. **PMID 42190810** — *Multi-omics insights into uric acid metabolism: from genetics to epigenetics, transcriptomics, and metabolomics in cardiometabolic disease* — Biomedical Journal, 2026-05-25 — **3 domains: Biomarker, Epigenetics, Multi-omics**. Brand new (added today).
3. **PMID 42148104** — *Adapting CAR-T and CAR-Treg cancer therapies for autoimmunity: innovations and challenges* — Frontiers in Immunology, 2026 — **T1D Stem Cell Cure + T1D Immunotherapy**. Relevant to Treg/CAR-T gap area.
4. **PMID 42138080** — *New and emerging therapies in type 1 diabetes mellitus* — J Clinical Investigation, 2026-05-15 — **T1D Immunotherapy + Key Therapy: teplizumab**. High-impact review.
5. **PMID 42138126** — *US Patterns in Clinical Islet Autoantibody Ordering and Results — Key Differences After Teplizumab Regulatory Approval* — JCEM, 2026-05-15 — **T1D Immunotherapy + Key Therapy: teplizumab**. Real-world post-approval surveillance — relevant to teplizumab adoption-equity questions.

Other cross-domain hits worth a scan: PMID 42185046 (incretin × lipid/gene-therapy), PMID 42168638 (GLP-1 dysesthesia × retatrutide), PMID 42171711 (T2D remission × epigenetics), PMID 42184924 (AI/ML × multi-omics for diabetic osteoporosis), PMID 42186308 (biomarker × multi-omics — lipid dysregulation), PMID 42178167 (epigenetics × multi-omics — diabetic nephropathy circadian genes), PMID 42142983 (retatrutide × CagriSema — bariatric audit).

### Key-therapy paper activity (last ~30 days)
- **Teplizumab:** 5 papers — including the JCI review (PMID 42138080), the JCEM real-world utilization study (42138126), the BSPED consensus statement (PMID 42051156), and a UK clinical experience case series (PMID 41796109).
- **Retatrutide:** 5 papers — most notably **PMID 42135195** (*Retatrutide And Lipid And Metabolite Profiles in Obesity ± T2D*, JCEM, 2026-05-14) and **PMID 42108533** (triple-hormone agonism for CKM syndrome review).
- **Orforglipron:** 3 papers — **PMID 42120723** (*ATTAIN-MAINTAIN Phase 3b weight-maintenance trial*, Nature Medicine, 2026-05-13) — high-impact; also GI safety meta-analysis (PMID 42116665).
- **CagriSema:** 4 papers — systematic reviews of CagriSema vs. semaglutide (PMID 41759565, 42180166, 42175595).
- **Baricitinib:** 3 papers — kidney EV proteomics (PMID 42173279) plus two off-target dermatology/autoimmune case reports.
- **Zimislecel:** 0 papers in the 30-day window (no flagged PubMed activity).
- **Icodec (Awiqli):** 5 papers — relevant given the recent once-weekly basal insulin FDA approval.
- **Dapagliflozin:** 5 papers — including **PMID 42191874** (SGLT2i & epicardial adipose tissue, IJ Obesity, 2026-05-27).

### Domain volume notes
All 14 of the 16 core domains hit the per-query cap of 10 retrieved papers — i.e., publication volume is at ceiling and the script's sampling is not deep enough to compare relative activity. **GLP-1 Pharmacogenomics returned only 1 paper** and **LADA only 7** — these are the two genuinely quieter domains in the last 30 days. (Recommend: bump the per-domain `retmax` to ~25 in `baseline_pubmed_alerts.py` if you want trend analysis rather than just headline detection.)

---

## Gap Analysis Summary

`literature_gap_data.json` is **36 days old** — top-5 figures below are from the 2026-04-20 generation and have not been refreshed. The interpreted `literature_gap_report.md` (2026-05-26) is freshly re-rendered but still relies on the underlying April 20 counts.

**Top 5 under-researched intersections (all Gap Score 100.0; "Potentially Meaningful" classification):**

1. **Beta Cell Regen × Health Equity** (0 joint pubs) — equity analysis of emerging regenerative therapies is absent. **Tier 1 alignment.**
2. **Insulin Resistance × Islet Transplant** (1 joint pub) — IR in islet recipients affecting graft survival is barely studied.
3. **Islet Transplant × Drug Repurposing** (0 joint pubs) — computational repurposing for islet protection unexplored.
4. **Islet Transplant × Health Equity** (0 joint pubs) — center-of-excellence access disparities undocumented. **Tier 1 alignment.**
5. **Gene Therapy × LADA** (0 joint pubs) — autoimmune-mechanism overlap unstudied. **Tier 1 alignment.**

Three of the top 5 ("× Health Equity" and the LADA gap) directly map to the Tier 1 contribution areas in `RESEARCH_DOCTRINE.md` (per the doctrine's emphasis on equity-of-access analysis and LADA underdiagnosis).

---

## Breaking News (last 7 days)

- **2026-05-21 — Eli Lilly TRIUMPH-1 Phase 3 topline** for retatrutide: at 12 mg dose, ~28.3% average weight loss at 80 weeks (up to ~30.3% at 104 weeks) in obesity/overweight without diabetes. TRIUMPH-2 (T2D) and TRIUMPH-3 (established CVD) topline expected later in 2026. **High priority** — likely to drive a wave of follow-up publications in the Key-Therapy: retatrutide alert domain over the coming weeks, and reframes the GLP-1/GIP/glucagon class.
- **2026-04-22 — FDA expanded Tzield (teplizumab) label** to children as young as 1 year (down from ≥8) for stage 2 T1D. Older than the 7-day window but explains why the **JCEM real-world ordering paper (PMID 42138126)** is showing up now and why pediatric platform-trial NCT07216391 is in the new-trials list. The pediatric Phase 2 (NCT06791291) and Phase 3 head-to-head (NCT07088068) Sanofi trials are the ones to watch for follow-on evidence.
- Earlier-2026 context: Novo Nordisk's **Awiqli (insulin icodec)** once-weekly basal insulin approval and a **generic dapagliflozin** approval explain the 5-paper bursts in those Key-Therapy domains.

No FDA-action items, no Vertex/zimislecel news, and no Sana announcements in the last 7 days.

---

## Recommended Actions

1. **Refresh stale gap data — highest priority.** Run `python project1_literature_gap_analysis.py` to regenerate `literature_gap_data.json` (currently 36 days old). The interpreted report depends on it.
2. **Read PMID 42138080** (*New and emerging therapies in T1D*, JCI 2026-05-15) — high-impact review that crosses two tracked domains; likely the right anchor citation for any T1D-immunotherapy contribution piece.
3. **Read PMID 42135195** (Retatrutide lipid/metabolite profiles, JCEM 2026-05-14) and queue retatrutide follow-up — TRIUMPH-1 topline announcement on 2026-05-21 means a publication wave is imminent. Set an explicit alert for "retatrutide" + "TRIUMPH" PubMed indexing.
4. **Cross-reference PMID 42163482** (EV-protein biomarkers for T1D progression) — sits at T1D Stem Cell Cure × T1D Immunotherapy × teplizumab; matches the doctrine's interest in pre-clinical T1D biomarkers for teplizumab responder selection.
5. **Investigate NCT04426474 results** (orforglipron Phase 1 T2D, results posted 2026-05-26) — Lilly back-filled an older small trial. Worth checking whether the dose-finding data adds anything to the orforglipron pharmacology evidence base, even though the headline action is in the Phase 3 program.
6. **Update Diabetes_Research_Tracker.xlsx** with the two status changes (NCT07527650, NCT07124208) and the orforglipron Phase 1 result.
7. **Optional config tweak:** bump per-domain `retmax` in `baseline_pubmed_alerts.py` from 10 to ~25 so the snapshot can support volume-trend analysis (right now nearly every domain hits the cap).

---

*Generated by the diabetes-hub-monitor scheduled task. Validation level **BRONZE** — single-source automated review; cross-check before any external contribution.*
