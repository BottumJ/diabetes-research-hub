# Diabetes Research Hub — Monitor Report

**Generated:** 2026-05-11 (automated scheduled run)
**Scope:** Review of latest script outputs in `Analysis/Results/`, snapshot diffs since 2026-05-04 and 2026-05-10, and a brief web check for breaking news.
**Validation level (per Research Doctrine):** BRONZE for analytical findings; observational diffs are direct (verifiable from snapshot files).

---

## File System Status

All four primary data products are present.

| File | Last modified | Status |
|------|---------------|--------|
| `hub_monitor_report.md` | 2026-05-11 07:05 | Fresh |
| `clinical_trials_latest.json` | 2026-05-11 07:04 | Fresh (786 trials) |
| `pubmed_recent_latest.json` | 2026-05-11 07:04 | Fresh (141 unique papers, multi-domain lookback) |
| `literature_gap_report.md` | 2026-05-10 08:09 | Fresh (≤14 days) |
| `literature_gap_data.json` | **2026-04-20 15:35** | **STALE — 21 days old, exceeds 14-day refresh threshold** |

`hub_monitor.py` flagged 552 result files older than 14 days. The vast majority are dated snapshot archives (expected by design). The only material concern is `literature_gap_data.json`: the gap *report* was regenerated on 2026-05-10 but is still backed by the April 20 underlying counts. **Recommended:** rerun `python project1_literature_gap_analysis.py` to refresh the underlying PubMed counts; gap scores may have drifted as several previously-empty intersections (e.g., Gene Therapy × LADA, Drug Repurposing × LADA) continue to receive zero new joint publications.

---

## Clinical Trial Changes

**Source:** `clinical_trials_latest.json` (generated 2026-05-11T07:04:20, ClinicalTrials.gov API v2)

### Headline category counts (unchanged shape from yesterday)
- T1D Cure & Cell Therapy: 151
- T1D Immunotherapy & Prevention: 71
- T2D Novel Therapies (Phase 2-3): 139
- Diabetes Technology (Devices): 222
- Diabetes Recently Completed with Results: 275
- **Total: 786 trials** (up from 778 on 2026-05-04; +10 added, -2 removed)

### Day-over-day diff (per hub_monitor)
- New trials: 0
- Status changes: 0
- New results posted: 0

### 7-day diff (vs. 2026-05-04 snapshot)
**10 new trials added in the past week.** Notable additions:

| NCT ID | Phase / Status | Sponsor | Brief |
|--------|----------------|---------|-------|
| **NCT07564414** | Phase 3 / Not Yet Recruiting | Novo Nordisk | CagriSema dose comparison vs. semaglutide in obesity — **fills our previously-noted gap on CagriSema activity (0 papers / 0 trial entries in earlier reports)** |
| NCT07571343 | NA / Not Yet Recruiting | Medical College of Wisconsin | Protein supplementation for intrapartum glucose control |
| NCT07563699 | Phase 1/2 / Not Yet Recruiting | Mapi Pharma | Semaglutide Depot (long-acting injectable) in T2D |
| NCT07575438 | Phase 2 / Not Yet Recruiting | May Faraj (Université de Montréal) | Different fish oil types on T2D risk factors |
| NCT07564752 | N/A / Recruiting | CHU Dijon | Glycemic control effects on HDL composition in T1D |
| NCT03734107, NCT03859401, NCT03940209, NCT04066959, NCT04557228 | Completed (newly indexed with results) | Various academic sites | Now appearing in "Recently Completed with Results" bucket |

### Status transitions (2 in past week)
- **NCT07135531** — Tulane CGM in underserved population: `NOT_YET_RECRUITING → RECRUITING`. Relevant to our Health Equity tier.
- **NCT07415954** — Novo Nordisk NNC0662-0419 dose comparison: `NOT_YET_RECRUITING → RECRUITING`.

### Phase 3 trials of strategic interest (RECRUITING)
- **Vertex / VX-880** (zimislecel): NCT04786262 + NCT06832410 — both Phase 3 recruiting (T1D cell therapy).
- **Vertex / VX-264** (encapsulated islets): NCT05791201 — Phase 1/2 active (not recruiting).
- **Eli Lilly / Baricitinib**: NCT07222137 (Stage 3 T1D delay in at-risk children) + NCT07222332 (beta cell preservation in newly diagnosed) — both Phase 3 recruiting.
- **Eli Lilly / Tirzepatide in T1D**: NCT06962280 (Phase 3 active), NCT06914895 (Phase 3 active).
- **Eli Lilly / Retatrutide T2D**: NCT06260722, NCT05929079 — Phase 3 active not recruiting.
- **Eli Lilly / Orforglipron**: NCT06972472 — Phase 3 active (obesity + T2D).
- **Sanofi / Teplizumab**: NCT07088068 — Phase 3 recruiting (efficacy and safety vs. placebo).
- **Novo Nordisk / Insulin Icodec**: NCT07076199 — Phase 3 recruiting in T1D adjunctive use.
- **Novo Nordisk / CagriSema**: NCT07564414 (new this week, see above).

### Recently posted results (since 2026-04-11) — items to consider reviewing
- **NCT05971940** (2026-04-22, Eli Lilly): Orforglipron in adults with T2D — Phase 3 readout. **High priority for evidence file.**
- **NCT05823948** (2026-04-30, Novo Nordisk): Flash glucose measurements with once-weekly insulin (icodec).
- **NCT05649137** (2026-04-27, Novo Nordisk): Semaglutide in excess weight and T2D.
- **NCT05923827** (2026-04-14, Insulet): Omnipod 5 + Libre 2 vs. MDI in T1D children/adults.
- **NCT05238142** (2026-04-16, Medtronic): MiniMed 780G AID in T2D.

No newly posted results in the past 7 days (consistent with hub_monitor diff).

---

## PubMed Highlights

**Source:** `pubmed_recent_latest.json` (generated 2026-05-11T07:04:57, 141 papers across 16 alert domains).

### Publication volume by domain (top vs. quiet)
- **High volume:** Diabetes AI/ML (194 total hits), Diabetes Biomarker (143), T2D GLP-1 New (128), Diabetes Microbiome (119).
- **Mid volume:** T2D Remission (62), Diabetes Health Equity (52), Diabetes Multi-Omics (51), Diabetes Gene Therapy (37), Diabetes Complications New (34).
- **Quiet domains:** T1D Stem Cell Cure (18), T1D Immunotherapy (18), Closed Loop AP (18), Diabetes Epigenetics (8), **Diabetes Drug Repurpose (4), LADA New Research (4), GLP-1 Pharmacogenomics (1)**.

The persistent low signal in Drug Repurposing, LADA, and GLP-1 Pharmacogenomics aligns directly with our Tier 1 contribution areas — these are real research-volume gaps, not just keyword artifacts.

### Cross-domain papers (12 of 141 — highest priority)

| PMID | Domains | Title |
|------|---------|-------|
| **42108331** | T2D GLP-1 New, T2D Remission, Closed Loop AP | The impact of automated insulin delivery on glucose management in people with diabetes and advanced CKD (*Diabetologia*, 2026-May-11). **Three-domain hit — review for Closed-Loop / Remission evidence files.** |
| 42051156 | T1D Immunotherapy, Key Therapy: teplizumab | British Society Consensus Statement on clinical use of teplizumab in stage 2 T1D (*Diabetic Medicine*, 2026-Apr-29) |
| 42104727 | T1D Stem Cell Cure, Gene Therapy | Stem cell-based therapies for T1D: differentiation, clinical translation, immune protection (review) |
| 42034968 | T1D Stem Cell Cure, T1D Immunotherapy | Bone marrow-derived cells in experimental autoimmune T1D |
| 42046753 | T1D Immunotherapy, Closed Loop AP | Active-break sitting intervention on glucose and vascular function in adults |
| 42078397 | T2D Remission, Gene Therapy | Loss-of-function variant analysis (medRxiv preprint) |
| 42101353 | T2D Remission, Biomarker | Causal effects of CRP via multivariable Mendelian randomization |
| 42103860 | Diabetes AI/ML, Multi-Omics | Ubiquitination-driven fibroblast dysfunction in diabetic foot ulcer (*Scientific Reports*) |
| 42101085 | Microbiome, Multi-Omics | (Off-target — autism methods paper; safe to deprioritize) |
| 42099240 | Gene Therapy, Complications New | NLRP3 inflammasome in diabetic nephropathy (review) |
| 42089665 | Gene Therapy, Complications New | VEGFA-targeted M3-F4 LNPs for diabetic retinopathy |
| 42070230 | Gene Therapy, Multi-Omics | DES-AAV-Foxo1 delivery system for corneal endothelial dysfunction |

### Key therapy mentions
- **Teplizumab:** 3 papers (most actionable: PMID 42051156 BSPED consensus statement).
- **Orforglipron:** 2 papers (PMID 41994902 PK bioequivalence; PMID 41984238 critique of efficacy/safety analyses — worth reviewing the latter for methodological caveats).
- **Baricitinib:** 1 paper (dermatology case report, not diabetes-relevant).
- **Retatrutide, zimislecel, CagriSema:** 0–1 hits each — drug-name PubMed signal remains weak relative to trial-pipeline activity.
- **Dapagliflozin (background reference):** 26 hits — large body of work consistent with the new FDA generic approval (see Breaking News).

### 7-day PubMed churn
- 92 new papers / 90 dropped since 2026-05-04 (high turnover within the rolling 30-day window).
- 8 of the 12 cross-domain papers above were new in the past week.

---

## Gap Analysis Summary

**Source:** `literature_gap_data.json` (2026-04-20 — stale) + `literature_gap_report.md` (2026-05-10).

### Top 5 under-researched intersections (highest gap scores, classified meaningful)

| Rank | Intersection | Joint Pubs | Gap Score | Tier alignment |
|------|--------------|-----------|-----------|----------------|
| 1 | **Beta Cell Regen × Health Equity** | 0 | 100 | Tier 1 (Health Equity is a doctrine priority) |
| 2 | **Insulin Resistance × Islet Transplant** | 1 | 100 | Tier 2 |
| 3 | **Islet Transplant × Drug Repurposing** | 0 | 100 | Tier 1 (Drug Repurposing is doctrine focus) |
| 4 | **Islet Transplant × Health Equity** | 0 | 100 | Tier 1 |
| 5 | **Gene Therapy × LADA** | 0 | 100 | Tier 1 (LADA is doctrine focus) |

Additional doctrine-aligned gaps from the same ranked list: Treg/CAR-T × Health Equity (#7), Glucokinase × Drug Repurposing (#8), Personalized Nutrition × LADA (#11), Drug Repurposing × Health Equity (#12), Drug Repurposing × LADA (#13), Health Equity × LADA (#14). The intersection of our three doctrine pillars (Drug Repurposing / LADA / Health Equity) remains essentially empty in the PubMed corpus — same finding as last week's report. No new joint publications appeared in the past 7 days that would close any of these gaps.

---

## Breaking News (web check, last ~7 days)

**Major signals — all relevant to the hub:**

1. **FDA: First generic dapagliflozin approval (May 2026).** Adds a meaningful equity/access angle — relevant to our Generic Drug Catalog and Health Equity dashboards. *Evidence level: FDA primary source.*

2. **FDA Tzield (teplizumab-mzwv) sBLA approved** (Sanofi press release dated 2026-04-22) — pediatric indication extended down to age 1 for Stage 2 T1D delay. **This pairs directly with PMID 42051156 (BSPED consensus statement on teplizumab in stage 2)** flagged in the cross-domain section above. The new label expansion was the subject of `teplizumab_sNDA_decision_prep.md` (Apr 3) — that prep doc may now warrant a "decision outcome" update.

3. **Foundayo (orforglipron) — Lilly's oral GLP-1, FDA approved 2026-04-01 for obesity.** T2D approval is anticipated late 2026. PMID 41994902 (PK bioequivalence) and PMID 41984238 (methodological critique) are the new associated PubMed entries — worth folding into the GLP-1 evidence file with appropriate caveat per PMID 41984238.

4. **Preclinical T1D cure work (mouse models, May 2026):** Combined hematopoietic stem cell + islet transplant inducing tolerance (ScienceDaily / propakistani). Interesting but preclinical — *Evidence level: PRECLINICAL only; do not elevate.* Worth a Notes-folder pointer; not yet actionable for the hub.

5. **ADA "Standards of Care in Diabetes — 2026" published.** Likely triggers downstream guideline updates across the hub — review for any guideline-anchored claims in dashboards and Research_Findings_Summary.md.

Routine ATTD 2026 conference recap and JDCA outlook pieces are noted but skipped (not material).

---

## Recommended Actions

1. **Refresh stale gap-analysis data:**
   `python project1_literature_gap_analysis.py`
   `literature_gap_data.json` is 21 days old; the gap report should be regenerated from fresh PubMed counts before any decision is taken on top-ranked intersections.

2. **Review new Phase 3 trial NCT07564414 (CagriSema dose comparison).** Add to `Diabetes_Research_Tracker.xlsx` under the T2D Novel Therapies tab; this is the first CagriSema entry in the tracker.

3. **Review three-domain cross-hit PMID 42108331** (AID in diabetes + advanced CKD, *Diabetologia*). Spans Closed-Loop, Remission, and GLP-1 alerts — strong candidate for Extracted_Evidence ingestion. (Validation: SILVER if confirmed primary clinical evidence.)

4. **Update teplizumab artifacts** to reflect (a) FDA sBLA pediatric label expansion and (b) the BSPED consensus statement (PMID 42051156). `teplizumab_sNDA_decision_prep.md` is now a historical doc — append a one-line outcome note.

5. **Append a methodological caveat to any orforglipron evidence rows** referencing PMID 41984238 (critique of efficacy/safety analyses) before publishing further orforglipron claims downstream.

6. **Generic dapagliflozin approval:** Add a line in the Generic_Drug_Catalog dashboard and Health_Equity material.

7. **Status-change pickups for the tracker:** flip NCT07135531 (Tulane CGM, underserved pop.) and NCT07415954 (Novo Nordisk NNC0662-0419) to RECRUITING.

8. **Newly indexed completed trials with results** (NCT04066959, NCT03734107, NCT03859401, NCT03940209, NCT04557228) — verify whether any belong in the Drug Repurposing / Health Equity dashboards before they age out of the rolling window.

9. **2026 ADA Standards of Care:** schedule a focused pass through dashboards and `Research_Findings_Summary.md` for guideline-anchored claims that may need updating.

---

*Compiled automatically. No source files were modified by this monitor run.*

## Sources

- [FDA Approves First Generic Dapagliflozin Tablets — FDA](https://www.fda.gov/drugs/drug-alerts-and-statements/fda-approves-first-generic-dapagliflozin-tablets)
- [Sanofi press release — Tzield (teplizumab) approved to delay onset of stage 3 T1D in young children](https://www.sanofi.com/en/media-room/press-releases/2026/2026-04-22-05-05-00-3278650)
- [FDA approves Lilly's Foundayo (orforglipron) — Eli Lilly investor release](https://investor.lilly.com/news-releases/news-release-details/fda-approves-lillys-foundayotm-orforglipron-only-glp-1-pill)
- [FDA Drug Approval Decisions Expected in May 2026 — The Cardiology Advisor](https://www.thecardiologyadvisor.com/news/fda-drug-approval-decisions-expected-in-may-2026/)
- [ADA Standards of Care in Diabetes — 2026 (American Diabetes Association)](https://diabetes.org/newsroom/press-releases/american-diabetes-association-releases-standards-care-diabetes-2026)
- [Lab-grown insulin cells reverse diabetes in mice — ScienceDaily, May 2026](https://www.sciencedaily.com/releases/2026/05/260505234620.htm)
