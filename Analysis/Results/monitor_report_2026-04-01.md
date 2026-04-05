# Diabetes Research Hub — Monitor Report
**Date:** 2026-04-01
**Automated scan by:** Cowork Scheduled Task (diabetes-hub-monitor)

---

## File System Status

| File | Last Modified | Status |
|------|--------------|--------|
| hub_monitor_report.md | 2026-04-01 02:06 | Fresh (today) |
| clinical_trials_latest.json | 2026-04-01 02:05 | Fresh (today) |
| pubmed_recent_latest.json | 2026-04-01 02:05 | Fresh (today) |
| literature_gap_data.json | 2026-03-15 00:45 | **STALE — 17 days old (past 14-day threshold)** |
| literature_gap_report.md | 2026-03-31 03:07 | Fresh (1 day old) |
| hub_monitor_state.json | 2026-04-01 02:06 | Fresh (today) |

**Hub monitor detected:** 607 total files tracked, 45 new files, 97 modified files, 0 removed.

**Significant new files since last scan:**
- `clinical_trials_snapshot_2026-04-01.json` — Daily trial snapshot
- `pubmed_recent_snapshot_2026-04-01.json` — Daily PubMed snapshot
- `monitor_report_2026-03-31.md` — Yesterday's monitor report
- 33 new paper library abstracts (PMIDs: 11484077, 12202461, 15266224, 15793177, 18794064, 19133409, 21864487, 2189759, 25324018, 26106223, 26404926, 29710129, 29909913, 30586620, 31157579, 32175717, 32535920, 33515517, 34256014, 34763823, 35203496, 35551292, 35551294, 36109639, 36288281, 36449148, 37223016, 37748491, 38078589, 38639547, 39629068, 40249888, 40272935)
- 9 new full-text papers in paper library (PMCs: 10200948, 11612564, 12278794, 5321245, 7310804, 8597930, 8869296, 9020749, 9117147)

**Review flags:** 287 result files are older than 14 days and may need refresh (mostly paper library abstracts/fulltext from initial build).

---

## Clinical Trial Changes

### Snapshot Comparison (2026-03-31 → 2026-04-01)

| Metric | Count |
|--------|-------|
| Total trials | 750 (down from 757 — net loss of 7) |
| New trials | 2 |
| Removed trials | 9 |
| Status changes | 1 |
| New results posted | 0 |

### New Trials

| NCT ID | Title | Sponsor | Status | Category |
|--------|-------|---------|--------|----------|
| **NCT07502495** | Phase 2 Trial of Icovamenib in Participants With T2D Not Achieving Adequate Glycemic Control | **Biomea Fusion Inc.** | RECRUITING | T2D Novel Therapies |
| **NCT07502508** | Phase 2 Trial of Icovamenib in Participants With T2D | **Biomea Fusion Inc.** | RECRUITING | T2D Novel Therapies |

**Note:** Icovamenib (BMF-219) is Biomea Fusion's menin inhibitor being studied for T2D — a novel mechanism of action targeting beta cell regeneration. Two new Phase 2 trials appearing simultaneously suggests the program is expanding. Worth tracking as a potential beta cell regeneration approach.

### Status Changes

| NCT ID | Old Status | New Status | Sponsor | Title |
|--------|-----------|------------|---------|-------|
| **NCT07271251** | RECRUITING | **ACTIVE_NOT_RECRUITING** | Novo Nordisk | Oral Semaglutide Formulation Comparison Study |

**Interpretation:** Enrollment complete for this Novo Nordisk formulation study. Normal trial lifecycle progression.

### Removed Trials (9)

Trials that fell out of the monitoring window (likely due to API query changes or completion):
- NCT05826678 — CGM in Asian Americans with T2D (was RECRUITING)
- NCT06305377 — Rapid glucose control in adolescents (T1D)
- NCT06326489 — Transitioning to Advanced HCL (T1D)
- NCT06334484 — Advanced HCL with adjunctive CGM (T1D)
- NCT06338086 — Semaglutide injection in T2D
- NCT06357728 — CGM during pregnancy
- NCT06623708 — SMARTCLOTH wearable study (T1D)
- NCT06258148 — TG103 injection for T2D
- NCT06310980 — Smartpen + glucose sensor pilot

### Key Phase 3 Recruiting Trials — Priority Watch List

**Total recruiting Phase 3 trials: 100**

#### Vertex Pharmaceuticals (Cell Therapy — Tier 1)
| NCT ID | Title | Status |
|--------|-------|--------|
| NCT04786262 | VX-880 Safety, Tolerability, and Efficacy in T1D | RECRUITING |
| NCT06832410 | VX-880 in T1D with Kidney Transplant | RECRUITING |

#### Eli Lilly (Immunotherapy + Novel Therapies — Tier 1)
| NCT ID | Title | Status |
|--------|-------|--------|
| NCT07222137 | Baricitinib for Delay of Stage 3 T1D | RECRUITING |
| NCT07222332 | Baricitinib to Preserve Beta Cell Function | RECRUITING |
| NCT06972472 | Orforglipron in Obesity/Overweight | RECRUITING |
| NCT06993792 | Orforglipron Master Protocol | RECRUITING |
| NCT06738122 | Dulaglutide 3.0/4.5 mg in Pediatric T2D | RECRUITING |

#### Novo Nordisk (Weekly Insulin + GLP-1 — Tier 1)
| NCT ID | Title | Status |
|--------|-------|--------|
| NCT07076199 | Insulin Icodec (weekly insulin) | RECRUITING |

### Overall Trial Portfolio

| Category | Count | Change vs. Yesterday |
|----------|-------|---------------------|
| T1D Cure & Cell Therapy | 149 | -5 |
| T1D Immunotherapy & Prevention | 71 | — |
| T2D Novel Therapies (Phase 2-3) | 137 | — |
| Diabetes Technology (Devices) | 215 | -3 |
| Recently Completed with Results | 250 | — |

---

## PubMed Highlights

### Publication Volume (Last 30 Days) — 127 unique papers across 15 domains

| Domain | Total Papers | Trend vs. Yesterday |
|--------|-------------|---------------------|
| Diabetes AI/ML | 178 | Down (was 221 yesterday — returning to normal range) |
| T2D GLP-1 New | 157 | Slight decrease (was 164) |
| Diabetes Microbiome | 147 | Slight decrease (was 172) |
| Diabetes Biomarker | 115 | Slight decrease (was 145) |
| Diabetes Health Equity | 73 | Slight decrease (was 77) |
| Diabetes Multi-Omics | 49 | Stable |
| Diabetes Complications New | 46 | Slight decrease (was 60) |
| T2D Remission | 42 | Slight decrease (was 56) |
| Diabetes Gene Therapy | 37 | Slight decrease (was 45) |
| T1D Immunotherapy | 20 | Slight decrease (was 27) |
| T1D Stem Cell Cure | 19 | Stable |
| Closed Loop AP | 19 | Slight decrease (was 23) |
| Diabetes Drug Repurpose | 5 | Slight decrease (was 6) |
| LADA New Research | 5 | Slight decrease (was 9) |
| Diabetes Epigenetics | 4 | Stable |

**Key observation:** Most domains show slight decreases as the 30-day rolling window advances. AI/ML dropped from 221 back to 178 — yesterday's 221 may have been a brief recovery overshoot after the prior API issue. All domains are within normal ranges. No anomalies detected.

### Cross-Domain Papers (6 total — highest priority)

| PMID | Title | Domains | Significance |
|------|-------|---------|-------------|
| **41907858** | Oral and cardiometabolic health through the lens of biobanks and large-scale epidemiologic research | **T2D Remission + Microbiome + Multi-Omics** | **Triple-domain cross-over** — aligns with Tier 1 Multi-Omics Biomarker Integration |
| **41910593** | Whole Metagenomic Profiling Identifies a Gut Microbial Signature for Chronic Pancreatitis via ML | AI/ML + Microbiome | ML applied to microbiome data — Tier 1 alignment |
| **41909676** | Unveiling the immune microenvironment in diabetic nephropathy: from mechanisms to therapeutics | Microbiome + Multi-Omics | Cross-domain immunity/complications |
| **41872174** | Antigen-specific immunotherapy with a CD4 T-cell approach for T1D | Stem Cell Cure + Immunotherapy | Key islet transplant + immunotherapy bridge paper |
| **41899527** | Systems-Level Transcriptomic Integration: T2D + HBV → Cholangiocarcinoma | Biomarker + Drug Repurpose | Tier 1 Drug Repurposing alignment |
| **41850943** | Corrigendum: ProHCL patient-reported outcomes in T1D | Immunotherapy + Closed Loop AP | Minor (corrigendum — low priority) |

### New Papers Since Yesterday (26 new, 30 dropped from rolling window)

Notable new additions:
- **PMID 41913320** — "From Screening to Delivery of Disease-Modifying Therapy: Real World Follow-Up of Children With Early-Stage T1D" (T1D Immunotherapy) — Timely given teplizumab April 29 PDUFA
- **PMID 41913548** — "Artificial Intelligence in Diabetes Care" (AI/ML) — Review paper
- **PMID 41913542** — "Glycaemic Outcomes of a Novel MPC-Based Hybrid Closed-Loop System in Adults With T1D" (Closed Loop AP) — New AID system data
- **PMID 41896712** — "Multi-Omics and ML-Driven Discovery of ABCC8 (SUR1) for Diabetes Mellitus" (Multi-Omics) — Tier 1 alignment
- **PMID 41915531** — "Federated Learning Framework for Privacy-Preserving Explainable AI-Driven Clinical Decision Support" (Complications) — Novel ML methodology
- **PMID 41239775** — "Computer-aided drug repurposing: antibacterial agents targeting GroEL" (Drug Repurpose) — Computational repurposing methodology

### Key Therapy Mentions

No papers in the current 30-day window mention zimislecel, orforglipron, retatrutide, CagriSema, baricitinib, or teplizumab in their titles or abstracts. This is consistent with yesterday's report (only PMID 41796109 for teplizumab appeared in the March 31 window but has now dropped out of the 30-day rolling window).

---

## Gap Analysis Summary

**Data freshness:** Gap data is from 2026-03-15 — **now 17 days old, past the 14-day stale threshold. Re-run is overdue.**

### Top 5 Under-Researched Intersections (by Gap Score)

| Rank | Domain Pair | Gap Score | Joint Pubs | Tier 1 Alignment |
|------|------------|-----------|------------|------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | Yes — Epidemiological Data Analysis |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | Yes — Literature Synthesis |
| 3 | Islet Transplant × Drug Repurposing | 100.0 | 0 | Yes — Drug Repurposing Screening |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | Yes — Epidemiological Data Analysis |
| 5 | Gene Therapy × LADA | 100.0 | 0 | Partial — Literature Synthesis |

**Doctrine Alignment:** Gaps #3 and #1/#4 directly map to Tier 1 contribution areas. Gap #5 is relevant given LADA's persistently low publication activity (only 5 papers in 30-day PubMed window — lowest activity domain).

**Validation level:** BRONZE (single analytical source — per Research Doctrine, requires expert confirmation).

---

## Breaking News (Web Search — Last 7 Days)

### ⚠️ CRITICAL: FDA Decision Dates Now Imminent

| Drug | Sponsor | PDUFA Date | Days Away | Significance |
|------|---------|------------|-----------|-------------|
| **Orforglipron** | Eli Lilly | **April 10, 2026** | **9 days** | First-in-class oral non-peptide GLP-1 RA for T2D. ACHIEVE-3 showed superior weight loss and glycemic control vs. oral semaglutide. Game-changing if approved. |
| **Teplizumab (Tzield) sNDA** | Sanofi | **April 29, 2026** | **28 days** | Expanded indication: delay Stage 3 T1D in at-risk patients ≥8 yrs. PMID 41913312 (new today) reports real-world follow-up of screened children — directly relevant. |
| **Afrezza (pediatric)** | MannKind | **May 29, 2026** | ~58 days | First inhaled insulin for children ages 4–17. Relevant to Youth Diabetes domain. |

### New Developments

**Biomea Fusion Icovamenib Expansion:** Two new Phase 2 trials (NCT07502495, NCT07502508) appeared today for icovamenib, a menin inhibitor for T2D. This is a novel beta cell regeneration mechanism — distinct from GLP-1 and cell therapy approaches. Evidence Level: 2b (Phase 2 trials).

**ATTD 2026 Conference Highlights:** The Advanced Technologies & Treatments for Diabetes (ATTD) 2026 conference featured breakthroughs in T1D management including new closed-loop systems and immunotherapy updates. Relevant papers may appear in PubMed over the coming weeks.

### Previously Reported (Still Active)

| Item | Date | Status |
|------|------|--------|
| Awiqli (Insulin Icodec) FDA Approved | Mar 27 | First weekly basal insulin for T2D. Novo Nordisk. Launch H2 2026. |
| Wegovy HD (Semaglutide 7.2 mg) FDA Approved | Mar 19 | Higher-dose semaglutide for weight management. |
| Retatrutide Phase 3 (TRANSCEND-T2D-1) | Mar 19 | Triple agonist: 2.0% A1C reduction, 16.8% weight loss. |
| Stanford T1D Remission (preclinical) | Mar 28 | Double cell transplant: 100% remission in mice. Human trials planned. |
| ADA Standards of Care 2026 | Late Mar | Expanded CGM, GLP-1 RA for obesity in T1D, SGLT2i/GLP-1 in CKD. |
| Oral Insulin Pill (Kumamoto University) | Mar 24 | Preclinical — peptide enables oral insulin absorption. |

---

## Recommended Actions

### 🔴 Immediate (This Week)

1. **Re-run gap analysis — data is now 17 days old, well past threshold.**
   → `Run: python project1_literature_gap_analysis.py`

2. **Prepare for orforglipron FDA decision (April 10 — 9 days away):**
   - Ensure tracker has orforglipron PDUFA date flagged
   - Prepare two tracker update templates (approval vs. CRL)
   - Note: NCT06972472 and NCT06993792 (Lilly orforglipron trials) are still actively recruiting

3. **Review new Biomea Fusion icovamenib trials (NCT07502495, NCT07502508):**
   - Novel menin inhibitor mechanism for T2D beta cell regeneration
   - Add to tracker under T2D Novel Therapies
   - Cross-reference with Beta Cell Regen gap analysis

4. **Review cross-domain paper PMID 41907858** — "Oral and cardiometabolic health through the lens of biobanks" spans T2D Remission + Microbiome + Multi-Omics. Directly aligns with Tier 1 Multi-Omics Biomarker Integration.

### 🟡 This Week

5. **Review PMID 41913312** — "From Screening to Delivery of Disease-Modifying Therapy: Real World Follow-Up of Children With Early-Stage T1D" — Directly relevant to teplizumab expanded indication (PDUFA April 29).

6. **Review PMID 41896712** — "Multi-Omics and ML-Driven Discovery of ABCC8 (SUR1)" — Aligns with Tier 1 Multi-Omics Biomarker Integration and AI/ML Prediction Model Development.

7. **Monitor ATTD 2026 conference publications** — Expect a wave of new PubMed papers from the conference over the next 2–4 weeks, particularly in closed-loop/AP and immunotherapy domains.

8. **Investigate 9 removed trials** — Several removed trials were actively recruiting (NCT05826678 CGM in Asian Americans, NCT06326489 Advanced HCL transition, NCT06357728 CGM in pregnancy). Determine if these were completed, withdrawn, or fell out of the monitoring query.

### 🟢 Ongoing Monitoring

9. **All automated scripts ran successfully** — hub_monitor.py, baseline_clinical_trials.py, and baseline_pubmed_alerts.py all produced fresh outputs today. No script re-runs needed except gap analysis.

10. **Baricitinib Phase 3 trials** (NCT07222137, NCT07222332) — Still actively recruiting. Continue high-priority tracking.

11. **Watch for Stanford T1D human trial registration** — Following preclinical announcement March 28.

12. **Watch for CagriSema FDA filing update** — Novo Nordisk trials NCT06221969 and NCT06534411 are active but not recruiting. Filing expected 2026.

---

*Report generated: 2026-04-01 | Next scheduled scan: 2026-04-02*
*Methodology: Research Doctrine v1.1 | Validation standards applied to all new claims*

Sources:
- [6 FDA Decisions To Watch in Q2 2026](https://www.biospace.com/fda/6-fda-decisions-to-watch-in-q2-2026)
- [5 FDA Decisions to Watch For: Q2 2026](https://www.patientcareonline.com/view/5-fda-decisions-to-watch-for-q2-2026)
- [ATTD 2026 Days 3 and 4 – Breakthroughs Transforming T1D](https://www.breakthrought1d.org/news-and-updates/attd-2026-days-3-and-4-breakthroughs-transforming-t1d/)
- [2026 Predictions for New Diabetes Drugs](https://tcoyd.org/2025/12/diabetes-predictions-2026/)
- [ADA Standards of Care 2026](https://diabetes.org/newsroom/press-releases/american-diabetes-association-releases-standards-care-diabetes-2026)
- [Novel Drug Approvals for 2026 — FDA](https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026)
