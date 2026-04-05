# Diabetes Research Hub — Monitor Report
**Date:** 2026-04-02
**Automated scan by:** Cowork Scheduled Task (diabetes-hub-monitor)

---

## File System Status

| File | Last Modified | Status |
|------|--------------|--------|
| hub_monitor_report.md | 2026-04-02 02:04 | Fresh (today) |
| clinical_trials_latest.json | 2026-04-02 02:04 | Fresh (today) |
| pubmed_recent_latest.json | 2026-04-02 02:04 | Fresh (today) |
| pubmed_recent_summary.md | 2026-04-02 02:04 | Fresh (today) |
| literature_gap_data.json | 2026-03-15 00:45 | **STALE — 18 days old (past 14-day threshold)** |
| literature_gap_report.md | 2026-04-01 08:08 | Fresh (1 day old) |
| hub_monitor_state.json | 2026-04-02 02:04 | Fresh (today) |

**Hub monitor detected:** 637 total files tracked, 30 new files, 28 modified files, 0 removed.

**Notable new files since last scan:**
- `clinical_trials_snapshot_2026-04-02.json` — Daily trial snapshot
- `pubmed_recent_snapshot_2026-04-02.json` — Daily PubMed snapshot
- `monitor_report_2026-04-01.md` — Yesterday's monitor report
- `new_pmids_gaps_1_5.json` — New PMIDs for gap analysis
- 19 new paper library abstracts
- 6 new full-text papers in paper library (PMCs: 11545964, 12078402, 12169077, 6936726, 7737672, 9479279)

**Review flags:** 330 result files are older than 14 days and may need refresh (mostly paper library abstracts/fulltext from initial build).

---

## BREAKING NEWS — Orforglipron (Foundayo) FDA Approved

### This is a critical update that supersedes yesterday's "PDUFA April 10" tracking.

**On April 1, 2026, the FDA approved Eli Lilly's Foundayo (orforglipron)** — the first oral non-peptide GLP-1 receptor agonist for weight loss. Key details:

- **Indication:** Weight reduction in adults with obesity or overweight with at least one weight-related comorbidity
- **Significance:** First-in-class oral GLP-1 pill that can be taken any time of day without food or water restrictions
- **Speed:** Approved 50 days after filing and 294 days before the PDUFA date — the fastest NME approval since 2002
- **Approved under:** Commissioner's National Priority Voucher (CNPV) pilot program (5th approval under program)
- **Dosing:** Starting dose 0.8 mg, titrated up to 2.5 mg → 5.5 mg → 9 mg → 14.5 mg → 17.2 mg
- **Evidence Level:** 1a (FDA-approved based on Phase 3 data)

**Note:** The approval is currently for obesity/overweight, NOT T2D. A separate T2D indication filing is expected. Active recruiting trials NCT06972472 and NCT06993792 continue.

**Action Required:** Update the Diabetes_Research_Tracker.xlsx to reflect the April 1 approval, and adjust monitoring from "pending PDUFA" to "approved — watch for T2D indication expansion."

---

## Clinical Trial Changes

### Snapshot Comparison (2026-04-01 → 2026-04-02)

| Metric | Count |
|--------|-------|
| Total trials | 750 (stable) |
| New trials | 0 |
| Removed trials | 0 |
| Status changes | 0 |
| New results posted | 0 |

**No changes in the trial database today.** This is a quiet day for ClinicalTrials.gov — likely due to the April 1 lag in registry updates.

### Overall Trial Portfolio (Stable)

| Category | Count |
|----------|-------|
| T1D Cure & Cell Therapy | 149 |
| T1D Immunotherapy & Prevention | 71 |
| T2D Novel Therapies (Phase 2-3) | 137 |
| Diabetes Technology (Devices) | 215 |
| Recently Completed with Results | 250 |

### Key Phase 3 Recruiting Trials — Priority Watch List (44 total)

| Sponsor | NCT ID | Title | Status |
|---------|--------|-------|--------|
| Vertex | NCT04786262 | VX-880 in T1D | RECRUITING |
| Vertex | NCT06832410 | VX-880 in T1D with Kidney Transplant | RECRUITING |
| Eli Lilly | NCT07222137 | Baricitinib for Delay of Stage 3 T1D | RECRUITING |
| Eli Lilly | NCT07222332 | Baricitinib to Preserve Beta Cell Function | RECRUITING |
| Eli Lilly | NCT06972472 | Orforglipron in Obesity/Overweight | RECRUITING |
| Novo Nordisk | NCT07076199 | Insulin Icodec (weekly insulin) | RECRUITING |
| Sanofi | NCT07088068 | [Teplizumab-related] | RECRUITING |

### Upcoming FDA Decisions Still Pending

| Drug | Sponsor | PDUFA Date | Days Away |
|------|---------|------------|-----------|
| **~~Orforglipron~~** | ~~Eli Lilly~~ | ~~April 10~~ | **APPROVED April 1** |
| **Teplizumab sNDA** | Sanofi | April 29, 2026 | **27 days** |
| **Afrezza (pediatric)** | MannKind | May 29, 2026 | ~57 days |

---

## PubMed Highlights

### Publication Volume (Last 30 Days) — 128 unique papers across 15 domains

| Domain | Total Papers | Trend Signal |
|--------|-------------|--------------|
| Diabetes AI/ML | 181 | HIGH ACTIVITY (stable vs. yesterday's 178) |
| T2D GLP-1 New | 155 | HIGH ACTIVITY (slight decrease from 157) |
| Diabetes Microbiome | 147 | HIGH ACTIVITY (stable) |
| Diabetes Biomarker | 118 | HIGH ACTIVITY (slight increase from 115) |
| Diabetes Health Equity | 71 | HIGH ACTIVITY (slight decrease from 73) |
| Diabetes Multi-Omics | 50 | ACTIVE (slight increase from 49) |
| Diabetes Complications New | 43 | ACTIVE (slight decrease from 46) |
| T2D Remission | 42 | ACTIVE (stable) |
| Diabetes Gene Therapy | 38 | ACTIVE (slight increase from 37) |
| T1D Immunotherapy | 20 | ACTIVE (stable) |
| T1D Stem Cell Cure | 19 | ACTIVE (stable) |
| Closed Loop AP | 18 | ACTIVE (slight decrease from 19) |
| Diabetes Drug Repurpose | 5 | LOW (stable) |
| LADA New Research | 5 | LOW (stable) |
| Diabetes Epigenetics | 4 | LOW (stable) |

**Key observation:** All domains stable. No anomalies. Drug Repurpose and LADA remain persistently low-activity domains — gap analysis alignment confirmed.

### New Papers Today (22 new, 21 dropped from rolling window)

Notable new additions:

| PMID | Title | Domain | Significance |
|------|-------|--------|-------------|
| **41918165** | Taming Autoimmunity: AAT-Overexpressing MSCs Promote Treg Crosstalk to Reverse Diabetes | T1D Immunotherapy | Novel MSC+Treg approach — aligns with Treg/CAR-T domain |
| **41919986** | Unraveling Molecular Pathways of Insulin-Producing Cells From Placenta MSCs via Multi-Omics | Stem Cell + Multi-Omics | Tier 1 Multi-Omics alignment |
| **41920710** | Fiber From Different Food Sources and T2D Risk: Epidemiological + Multiomic Data | Microbiome | Integrative multi-omics approach |
| **41922811** | GLP1-RA and Multi-agonist Incretin Therapies for Obesity-related Conditions | GLP-1 | Timely given Foundayo approval |
| **41917764** | Epidemiology of Obesity and MASLD/MASH Association | GLP-1 | Relevant to expanding GLP-1 indications |
| **41918874** | Probiotic-Induced Microbiota Shifts in Gestational Diabetes (Multi-Omics) | Microbiome + Multi-Omics | Cross-domain paper |
| **41784095** | Extended Use of Automated Insulin Delivery in Young People with T1D | Closed Loop AP | Long-term AID outcomes data |

### Cross-Domain Papers (Highest Priority — 3 new today)

| PMID | Title | Domains | Tier 1 Alignment |
|------|-------|---------|------------------|
| **41918874** | Integrative multi-omics analysis reveals probiotic-induced microbiota shifts in women with gestational diabetes | Microbiome + Multi-Omics | Yes — Multi-Omics Biomarker Integration |
| **41921728** | Novel biomarkers for early diagnosis and treatment strategies of diabetic retinopathy | Biomarker + Complications | Yes — AI/ML Prediction Model Dev |
| **41921761** | The oral-gut microbiome axis in diabetes mellitus: systematic review | Biomarker + Microbiome | Yes — Literature Synthesis |

### Key Therapy Mentions

No papers in the current 30-day window mention zimislecel, orforglipron, retatrutide, CagriSema, baricitinib, or teplizumab by name in titles or abstracts. This is notable given the Foundayo approval — expect a wave of orforglipron publications in the coming weeks.

---

## Gap Analysis Summary

**Data freshness:** Gap data is from 2026-03-15 — **now 18 days old, well past the 14-day stale threshold. Re-run is overdue.**

### Top 5 Under-Researched Intersections (by Gap Score)

| Rank | Domain Pair | Gap Score | Joint Pubs | Tier 1 Alignment |
|------|------------|-----------|------------|------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | Yes — Epidemiological Data Analysis |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | Yes — Literature Synthesis |
| 3 | Islet Transplant × Drug Repurposing | 100.0 | 0 | Yes — Drug Repurposing Screening |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | Yes — Epidemiological Data Analysis |
| 5 | Gene Therapy × LADA | 100.0 | 0 | Partial — Literature Synthesis |

**All top 5 gaps align with Tier 1 contribution areas.** Gap #3 (Islet Transplant × Drug Repurposing) remains the most actionable — computational drug screening pipelines could address this directly.

**Validation level:** BRONZE (single analytical source — per Research Doctrine, requires expert confirmation).

---

## Breaking News Summary

### Major: Foundayo (Orforglipron) FDA Approved — April 1, 2026

The FDA approved Eli Lilly's Foundayo (orforglipron) as the first oral non-peptide GLP-1 receptor agonist for weight management. This was approved under the National Priority Voucher program, 294 days ahead of the PDUFA date. This is the most significant diabetes/obesity drug approval of 2026 so far. Evidence Level: 1a.

### Teplizumab: Continued Progress

New real-world evidence for teplizumab continues to accumulate. The sNDA for expanded indication (delay Stage 3 T1D in patients ≥8 years) has a PDUFA date of April 29, 2026 — 27 days away. Recent publication in Diabetes Care (Feb 2026) provides comprehensive review of disease-modifying potential. Safety/PK data now available for children <8 years (PMID 41196293).

### Previously Reported (Still Active)

| Item | Date | Status |
|------|------|--------|
| Awiqli (Insulin Icodec) FDA Approved | Mar 27 | First weekly basal insulin for T2D. Launch H2 2026. |
| Wegovy HD (Semaglutide 7.2 mg) Approved | Mar 19 | Higher-dose semaglutide for weight management. |
| Retatrutide Phase 3 (TRANSCEND-T2D-1) | Mar 19 | Triple agonist: 2.0% A1C reduction, 16.8% weight loss. |
| Stanford T1D Remission (preclinical) | Mar 28 | Double cell transplant: 100% remission in mice. |
| Biomea Fusion Icovamenib Phase 2 expansion | Apr 1 | NCT07502495, NCT07502508 — menin inhibitor for T2D. |

---

## Recommended Actions

### Immediate (Today/Tomorrow)

1. **UPDATE TRACKER: Orforglipron (Foundayo) FDA approved April 1, 2026.**
   - Change status from "pending PDUFA" to "APPROVED — obesity indication"
   - Note: T2D indication not yet filed — continue monitoring
   - Active trials NCT06972472 and NCT06993792 continue recruiting

2. **Re-run gap analysis — data is now 18 days old, well past threshold.**
   → `Run: python project1_literature_gap_analysis.py`

3. **Review 3 new cross-domain papers:**
   - PMID 41918874 — Probiotic multi-omics in gestational diabetes (Microbiome + Multi-Omics)
   - PMID 41921728 — Diabetic retinopathy biomarkers (Biomarker + Complications)
   - PMID 41921761 — Oral-gut microbiome axis in diabetes (Biomarker + Microbiome)

### This Week

4. **Prepare for teplizumab sNDA decision (April 29 — 27 days away):**
   - Review PMID 41196293 (safety/PK in children <8 years)
   - Prepare two tracker update templates (approval vs. CRL)
   - Monitor Baricitinib Phase 3 trials (NCT07222137, NCT07222332) as alternative T1D immunotherapy

5. **Review PMID 41918165** — "Taming Autoimmunity: AAT-Overexpressing MSCs Promote Treg Crosstalk to Reverse Diabetes" — bridges Stem Cell and Treg/CAR-T domains, which are both gap analysis focus areas.

6. **Review PMID 41919986** — "Insulin-Producing Cells From Placenta MSCs via Multi-Omics" — directly aligns with Tier 1 Multi-Omics Biomarker Integration.

7. **Monitor for post-approval orforglipron publications** — Expect a surge in GLP-1 domain papers within 2-4 weeks following FDA approval. T2D GLP-1 domain (currently 155 papers/30 days) may spike.

### Ongoing Monitoring

8. **All automated scripts ran successfully.** hub_monitor.py, baseline_clinical_trials.py, and baseline_pubmed_alerts.py all produced fresh outputs today. No script re-runs needed except gap analysis.

9. **Watch for Stanford T1D human trial registration** — Following preclinical announcement March 28.

10. **Watch for CagriSema FDA filing update** — Novo Nordisk trials NCT06221969 and NCT06534411 are active but not recruiting.

11. **Biomea Fusion icovamenib** (NCT07502495, NCT07502508) — Continue monitoring these novel menin inhibitor T2D trials from yesterday's report.

---

*Report generated: 2026-04-02 | Next scheduled scan: 2026-04-03*
*Methodology: Research Doctrine v1.1 | Validation standards applied to all new claims*

Sources:
- [FDA Approves Lilly's Foundayo (orforglipron)](https://www.prnewswire.com/news-releases/fda-approves-lillys-foundayo-orforglipron-the-only-glp-1-pill-for-weight-loss-that-can-be-taken-any-time-of-day-without-food-or-water-restrictions-302731485.html)
- [FDA Approves Eli Lilly's Obesity Pill — TIME](https://time.com/article/2026/04/01/fda-approves-eli-lilly-obesity-pill/)
- [STAT News: Lilly obesity pill approved](https://www.statnews.com/2026/04/01/eli-lilly-obesity-pill-approved-orforglipron-foundayo/)
- [FDA Approves First NME Under National Priority Voucher Program](https://www.fda.gov/news-events/press-announcements/fda-approves-first-new-molecular-entity-under-national-priority-voucher-program)
- [Novel Drug Approvals for 2026 — FDA](https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026)
- [Teplizumab Disease-Modifying Review — Diabetes Care 2026](https://diabetesjournals.org/care/article/49/3/365/163760/Toward-Disease-Modifying-Therapies-in-Type-1)
- [Teplizumab Safety in Children <8 — PubMed](https://pubmed.ncbi.nlm.nih.gov/41196293/)
- [BioSpace: 6 FDA Decisions to Watch in Q2 2026](https://www.biospace.com/fda/6-fda-decisions-to-watch-in-q2-2026)
