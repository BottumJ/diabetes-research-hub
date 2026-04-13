# Diabetes Research Hub — Monitor Report
**Date:** 2026-04-03
**Automated scan by:** Cowork Scheduled Task (diabetes-hub-monitor)

---

## File System Status

| File | Last Modified | Status |
|------|--------------|--------|
| hub_monitor_report.md | 2026-04-03 02:05 | Fresh (today) |
| clinical_trials_latest.json | 2026-04-03 02:04 | Fresh (today) |
| clinical_trials_snapshot_2026-04-03.json | 2026-04-03 02:04 | Fresh (today) |
| pubmed_recent_latest.json | 2026-04-03 02:05 | Fresh (today) |
| pubmed_recent_summary.md | 2026-04-03 02:05 | Fresh (today) |
| literature_gap_data.json | 2026-03-15 00:45 | **STALE — 19 days old (past 14-day threshold)** |
| literature_gap_report.md | 2026-04-02 03:07 | Fresh (1 day old) |
| hub_monitor_state.json | 2026-04-03 02:05 | Fresh (today) |

**Hub monitor detected:** 640 total files tracked, 3 new files, 27 modified files, 0 removed.

**New files since last scan:**
- `clinical_trials_snapshot_2026-04-03.json` — Daily trial snapshot
- `pubmed_recent_snapshot_2026-04-03.json` — Daily PubMed snapshot
- `monitor_report_2026-04-02.md` — Yesterday's monitor report

**Review flags:** 333 result files older than 14 days — mostly paper library abstracts/fulltext from initial build. Not urgent.

---

## Clinical Trial Changes

### Snapshot Comparison (2026-04-02 → 2026-04-03)

| Metric | Count |
|--------|-------|
| Total unique trials | 751 (+1 from yesterday's 750) |
| New trials | 1 |
| Removed trials | 0 |
| Status changes | 1 |
| New results posted | 0 |

### NEW: Rezpegaldesleukin (NKTR-358) Now Recruiting

**NCT07142252** changed status from **NOT_YET_RECRUITING → RECRUITING**

- **Drug:** Rezpegaldesleukin (NKTR-358) — an IL-2 conjugate designed to selectively expand regulatory T cells (Tregs)
- **Indication:** New Onset Type 1 Diabetes Mellitus
- **Significance:** This is an immunomodulatory approach directly relevant to the Treg/CAR-T domain and T1D immunotherapy. Treg expansion is a mechanism complementary to teplizumab's T-cell depletion approach.
- **Tier 1 alignment:** Clinical Trial Intelligence + Literature Synthesis
- **Evidence Level:** Phase information pending review; mechanism aligns with Treg/CAR-T gap domain
- **Action:** Add to tracker Priority Watch List. Cross-reference with Gap #6 (Treg/CAR-T × Neuropathy) and Gap #7 (Treg/CAR-T × Health Equity).

### Trial Portfolio Summary (Stable)

| Category | Count |
|----------|-------|
| T1D Cure & Cell Therapy | 149 |
| T1D Immunotherapy & Prevention | 71 |
| T2D Novel Therapies (Phase 2-3) | 137 |
| Diabetes Technology (Devices) | 215 |
| Recently Completed with Results | 251 (+1) |

### Trial Status Distribution

| Status | Count |
|--------|-------|
| RECRUITING | 260 |
| COMPLETED | 251 |
| NOT_YET_RECRUITING | 126 |
| ACTIVE_NOT_RECRUITING | 108 |
| ENROLLING_BY_INVITATION | 6 |

### Key Phase 3 Recruiting Trials — Priority Watch List

| Sponsor | NCT ID | Title | Status | Notes |
|---------|--------|-------|--------|-------|
| Vertex | NCT04786262 | VX-880 in T1D | RECRUITING | Cell therapy — pivotal |
| Vertex | NCT06832410 | VX-880 in T1D with Kidney Transplant | RECRUITING | Expanded population |
| Eli Lilly | NCT07222137 | Baricitinib for Delay of Stage 3 T1D | RECRUITING | JAK inhibitor immunotherapy |
| Eli Lilly | NCT07222332 | Baricitinib to Preserve Beta Cell Function | RECRUITING | Companion to above |
| Eli Lilly | NCT06972472 | Orforglipron in Obesity/Overweight | RECRUITING | Post-approval expansion |
| Novo Nordisk | NCT07076199 | Insulin Icodec (weekly insulin) | RECRUITING | Awiqli follow-on studies |
| Sanofi | NCT07088068 | Teplizumab-related | RECRUITING | sNDA pending Apr 29 |
| **NEW** | NCT07142252 | Rezpegaldesleukin in New Onset T1D | **RECRUITING** | IL-2 Treg expansion — just activated |

### Upcoming FDA Decisions

| Drug | Sponsor | PDUFA Date | Days Away |
|------|---------|------------|-----------|
| **Teplizumab sNDA** | Sanofi | April 29, 2026 | **26 days** |
| **Afrezza (pediatric)** | MannKind | May 29, 2026 | ~56 days |

---

## PubMed Highlights

### Publication Volume (Last 30 Days) — 129 unique papers across 15 domains

| Domain | Total Papers | Trend vs. Yesterday | Signal |
|--------|-------------|---------------------|--------|
| Diabetes AI/ML | 179 | -2 | HIGH ACTIVITY |
| T2D GLP-1 New | 156 | +1 | HIGH ACTIVITY |
| Diabetes Microbiome | 147 | stable | HIGH ACTIVITY |
| Diabetes Biomarker | 117 | -1 | HIGH ACTIVITY |
| Diabetes Health Equity | 71 | stable | HIGH ACTIVITY |
| Diabetes Multi-Omics | 50 | stable | ACTIVE |
| Diabetes Complications New | 42 | -1 | ACTIVE |
| T2D Remission | 41 | -1 | ACTIVE |
| Diabetes Gene Therapy | 36 | -2 | ACTIVE |
| T1D Immunotherapy | 20 | stable | ACTIVE |
| Closed Loop AP | 19 | +1 | ACTIVE |
| T1D Stem Cell Cure | 18 | -1 | ACTIVE |
| Diabetes Drug Repurpose | 5 | stable | LOW |
| LADA New Research | 5 | stable | LOW |
| Diabetes Epigenetics | 4 | stable | LOW |

**Key observation:** All domains remain stable. No anomalies or spikes. Drug Repurposing, LADA, and Epigenetics continue at LOW activity levels — consistent with gap analysis findings showing these as under-researched areas.

### Rolling Window Changes (21 new papers, 20 dropped)

Net +1 paper in the rolling window. Normal daily churn.

### Cross-Domain Papers (Highest Priority)

5 cross-domain papers active in the current window:

| PMID | Title | Domains | Tier 1 Alignment |
|------|-------|---------|------------------|
| 41872174 | Antigen-specific immunotherapy with a CD4... | T1D Stem Cell + T1D Immunotherapy | Literature Synthesis |
| 41907858 | Oral and cardiometabolic health through biobanks | T2D Remission + Multi-Omics | Multi-Omics Biomarker Integration |
| 41921761 | The oral-gut microbiome axis in diabetes mellitus | Biomarker + Microbiome | Literature Synthesis |
| 41921728 | Novel biomarkers for diabetic retinopathy | Biomarker + Complications | AI/ML Prediction Models |
| 41918874 | Probiotic-induced microbiota shifts in gestational diabetes | Microbiome + Multi-Omics | Multi-Omics Biomarker Integration |

### Notable New Papers Today

| PMID | Title | Domain | Why It Matters |
|------|-------|--------|----------------|
| 41927536 | Multi-cohort metagenome analysis for T2D: universal gut microbiota signatures | Microbiome | Cross-population validation — aligns with AI/ML Prediction tier |
| 41927455 | The 3M roles of gut microbiome in pharmacotherapy for diabetes | Microbiome | Comprehensive review of microbiome as mediator/modifier/marker — Drug Repurposing relevance |
| 41926562 | Molecular insights into immunogenetic pathways of DKD | Biomarker | Multi-omics approach to diabetic kidney disease |
| 41928011 | AI-guided optimization of liposomal linagliptin | AI/ML | Novel AI-guided drug delivery |
| 41927291 | Retinal vascular phenotyping for CAD early detection | AI/ML | Cross-disease retinal imaging biomarker |
| 41925329 | Lifestyle intervention induces glycemic control, HbA1c >10 | Remission | Powerful case report for T2D remission potential |

### Key Therapy Mentions

No papers in the current 30-day window mention **zimislecel, orforglipron, retatrutide, CagriSema, baricitinib, or teplizumab** by name in titles. Post-Foundayo approval publication surge expected in 2–4 weeks.

---

## Gap Analysis Summary

**Data freshness:** Gap data is from 2026-03-15 — **now 19 days old, past the 14-day stale threshold. Re-run is overdue.**

### Top 5 Under-Researched Intersections (by Gap Score)

| Rank | Domain Pair | Gap Score | Joint Pubs | Tier 1 Alignment |
|------|------------|-----------|------------|------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | Yes — Epidemiological Data Analysis |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | Yes — Literature Synthesis |
| 3 | Islet Transplant × Drug Repurposing | 100.0 | 0 | Yes — Drug Repurposing Screening |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | Yes — Epidemiological Data Analysis |
| 5 | Gene Therapy × LADA | 100.0 | 0 | Partial — Literature Synthesis |

All top 5 gaps continue to align with Tier 1 contribution areas. Gap #3 (Islet Transplant × Drug Repurposing) remains the most computationally actionable.

**Validation level:** BRONZE (single analytical source — per Research Doctrine, requires expert confirmation).

**Today's connection:** The new NCT07142252 (Rezpegaldesleukin/NKTR-358 for T1D) is relevant to Gap #6 (Treg/CAR-T × Neuropathy) and Gap #7 (Treg/CAR-T × Health Equity) from the gap analysis, as it's a Treg-modulating therapy. If this trial publishes results, it could partially address the Treg research gaps.

---

## Breaking News

### NEW: Awiqli (Insulin Icodec) — Coverage Expanding

Multiple news outlets on April 2, 2026 are reporting on the FDA approval of Novo Nordisk's Awiqli, the first once-weekly basal insulin for adults with T2D. While the approval occurred on March 27, the expanded coverage suggests growing clinical awareness. Nationwide availability expected in coming months.

- **Evidence Level:** 1a (FDA-approved)
- **Action:** Already in tracker; monitor for launch date and real-world uptake data

### NEW: Merilog (Biosimilar Insulin Aspart) FDA Approved

The FDA approved Merilog, a biosimilar of insulin aspart (Novolog), for diabetes treatment. This expands insulin access options.

- **Evidence Level:** 1a (FDA-approved biosimilar)
- **Action:** Add to tracker under Diabetes Technology/Access

### NEW: ASC30 (Ascletis Oral GLP-1) Receives FDA IND Clearance

Ascletis announced US FDA IND clearance for a 13-week Phase II study of ASC30, another oral small molecule GLP-1 receptor agonist, in participants with diabetes. This is now the second oral GLP-1 in clinical development following Foundayo's approval.

- **Evidence Level:** Early (Phase II IND clearance)
- **Action:** Add to tracker as emerging competitor to orforglipron

### Previously Reported (Still Active)

| Item | Date | Status |
|------|------|--------|
| Foundayo (Orforglipron) FDA Approved | Apr 1 | First oral non-peptide GLP-1 for weight management. Watch for T2D filing. |
| Awiqli (Insulin Icodec) FDA Approved | Mar 27 | First weekly basal insulin for T2D. Launch H2 2026. |
| Wegovy HD (Semaglutide 7.2 mg) Approved | Mar 19 | Higher-dose semaglutide for weight management. |
| Retatrutide Phase 3 (TRANSCEND-T2D-1) | Mar 19 | Triple agonist: 2.0% A1C reduction, 16.8% weight loss. |
| Stanford T1D Remission (preclinical) | Mar 28 | Double cell transplant: 100% remission in mice. |
| Biomea Fusion Icovamenib Phase 2 expansion | Apr 1 | NCT07502495, NCT07502508 — menin inhibitor for T2D. |

---

## Recommended Actions

### Immediate (Today/Tomorrow)

1. **ADD NCT07142252 (Rezpegaldesleukin/NKTR-358) to tracker Priority Watch List.**
   - New Onset T1D immunotherapy via Treg expansion — just began recruiting
   - Cross-reference with Treg/CAR-T gap domains (#6, #7)

2. **Add Merilog (biosimilar insulin aspart) and ASC30 (oral GLP-1) to tracker.**
   - Merilog: FDA-approved biosimilar — relevant to Health Equity/Access domain
   - ASC30: Phase II IND cleared — second oral GLP-1 entrant after Foundayo

3. **Re-run gap analysis — data is now 19 days old, well past threshold.**
   → `Run: python project1_literature_gap_analysis.py`

### This Week

4. **Prepare for teplizumab sNDA decision (April 29 — 26 days away):**
   - Review latest safety/PK data (PMID 41196293)
   - Prepare two tracker update templates (approval vs. CRL)
   - Monitor baricitinib Phase 3 trials (NCT07222137, NCT07222332) as alternative T1D immunotherapy

5. **Review cross-domain papers (5 active):**
   - PMID 41918874 — Probiotic multi-omics in gestational diabetes (Microbiome + Multi-Omics)
   - PMID 41921728 — Diabetic retinopathy biomarkers (Biomarker + Complications)
   - PMID 41921761 — Oral-gut microbiome axis in diabetes (Biomarker + Microbiome)
   - PMID 41907858 — Cardiometabolic health via biobanks (T2D Remission + Multi-Omics)
   - PMID 41872174 — Antigen-specific immunotherapy (Stem Cell + Immunotherapy)

6. **Monitor for post-Foundayo orforglipron publications** — Expect a publication surge within 2–4 weeks. T2D GLP-1 domain (currently 156 papers/30 days) may spike.

### Ongoing Monitoring

7. **All automated scripts ran successfully today.** hub_monitor.py, baseline_clinical_trials.py, and baseline_pubmed_alerts.py all produced fresh outputs. No script re-runs needed except gap analysis.

8. **Watch for Stanford T1D human trial registration** — Following preclinical announcement March 28.

9. **Watch for CagriSema FDA filing update** — Novo Nordisk trials NCT06221969 and NCT06534411 are active but not recruiting.

10. **Continue monitoring Biomea Fusion icovamenib** (NCT07502495, NCT07502508) — Menin inhibitor T2D trials.

11. **Track retatrutide FDA approval timeline** — Prediction markets currently at 27% for 2026 approval per BioSpace. PDUFA date not yet assigned.

---

*Report generated: 2026-04-03 | Next scheduled scan: 2026-04-04*
*Methodology: Research Doctrine v1.1 | Validation standards applied to all new claims*

Sources:
- [FDA Approves Awiqli — ROI-NJ](https://www.roi-nj.com/2026/04/02/healthcare/fda-approves-novo-nordisks-awiqli-a-once-weekly-basal-insulin-treatment-for-adults-with-type-2-diabetes/)
- [Orforglipron Receives FDA Approval — HCPLive](https://www.hcplive.com/view/diabetes-dialogue-orforglipron-receives-fda-approval-for-chronic-weight-management)
- [FDA Approves Merilog Biosimilar — HCPLive](https://www.hcplive.com/view/fda-approves-merilog-biosimilar-product-insulin-aspart-novolog-diabetes)
- [ASC30 IND Clearance — PR Newswire](https://www.prnewswire.com/news-releases/ascletis-announces-us-fda-ind-clearance-for-13-week-phase-ii-study-of-its-oral-small-molecule-glp-1-asc30-in-participants-with-diabetes-302652107.html)
- [6 FDA Decisions To Watch in Q2 2026 — BioSpace](https://www.biospace.com/fda/6-fda-decisions-to-watch-in-q2-2026)
- [Bold New Plan to Cure T1D — ScienceDaily](https://www.sciencedaily.com/releases/2026/03/260302030648.htm)
- [FDA Retatrutide Approval Prediction — Lines.com](https://www.lines.com/prediction-markets/science/fda-approves-retatrutide-this-year)
