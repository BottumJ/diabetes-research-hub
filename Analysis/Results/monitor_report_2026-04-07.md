# Diabetes Research Hub — Monitor Report
**Date:** 2026-04-07
**Scan window:** 2026-04-06 → 2026-04-07
**Report type:** Automated daily review

---

## File System Status

All key data files are **current** (updated today, April 7):

| File | Last Modified | Status |
|------|--------------|--------|
| hub_monitor_report.md | 2026-04-07 02:05 | ✅ Fresh |
| clinical_trials_latest.json | 2026-04-07 02:05 | ✅ Fresh |
| pubmed_recent_latest.json | 2026-04-07 02:05 | ✅ Fresh |
| literature_gap_data.json | 2026-04-03 09:31 | ⚠️ 4 days old |
| literature_gap_report.md | 2026-04-06 03:07 | ✅ Fresh |

**Hub summary:** 681 files tracked. 3 new files, 27 modified files, 0 removed since last scan. 349 result files older than 14 days (mostly historical snapshots and paper library — expected).

**New files since last scan:**
- clinical_trials_snapshot_2026-04-07.json (507.3 KB)
- pubmed_recent_snapshot_2026-04-07.json (97.8 KB)
- monitor_report_2026-04-06.md (9.6 KB)

**All Python scripts are running on schedule — no re-runs needed for daily feeds.**

⚠️ **Gap analysis data is now 4 days old** — refresh recommended today (see Actions below).

---

## Clinical Trial Changes

### Snapshot Diff (Apr 6 → Apr 7)

| Metric | Count |
|--------|-------|
| New trials | 2 |
| Removed trials | 1 |
| Status changes | 1 |
| New results posted | 0 |

### New Trials

1. **NCT07026968** — *Prusogliptin + Dapagliflozin + Metformin in T2D* (CSPC Ouyi Pharmaceutical)
   - Phase 3 | Status: ACTIVE_NOT_RECRUITING | Enrollment: 815
   - Category: T2D Novel Therapies
   - **Note:** Triple combination study (GKA + SGLT2i + metformin). Relevant to our glucokinase activator tracking and drug combination analysis.

2. **NCT07510919** — *CGM in Acute Ischemic Stroke* (Isala)
   - Phase: N/A (device) | Status: NOT_YET_RECRUITING | Enrollment: 82
   - Category: Diabetes Technology
   - **Note:** Novel application of CGM beyond standard diabetes management — stroke monitoring.

### Removed Trials

- **NCT07118475** — No longer appearing in tracked queries (likely reclassified or withdrawn).

### Status Changes

- **NCT06964087**: ACTIVE_NOT_RECRUITING → **RECRUITING** | *Pharmacokinetic and Early Efficacy of OPT101 in Patients With Type 1 Diabetes Mellitus* (Op-T LLC, Phase 2)
  - **Note:** OPT101 is now actively recruiting for T1D. Start date listed as April 10, 2026. Novel immunotherapy candidate — worth adding to the watch list.

### Overall Trial Portfolio (Unchanged)

- **755 unique trials** tracked across 5 categories
- T1D Cure & Cell Therapy: 149 | T1D Immunotherapy & Prevention: 71 | T2D Novel Therapies: 137 | Diabetes Technology: 218 | Completed with Results: 253
- Top sponsors: Eli Lilly (27), Novo Nordisk (23), Medtronic (10), Insulet (9)

### Key Sponsor Trials — No Status Changes

All previously tracked key sponsor trials (Vertex VX-880, Eli Lilly baricitinib/orforglipron/retatrutide, Novo Nordisk CagriSema/icodec) remain at their prior statuses. See April 6 report for full table.

---

## PubMed Highlights

### Publication Volume (Last 30 Days) — 129 Unique Papers

| Activity Level | Domains |
|----------------|---------|
| **HIGH** (>100 papers) | Diabetes AI/ML (173), T2D GLP-1 New (149), Diabetes Microbiome (140), Diabetes Biomarker (118) |
| **HIGH** (>50) | Diabetes Health Equity (66) |
| **ACTIVE** (20-50) | Multi-Omics (45), T2D Remission (41), Gene Therapy (38), Complications (38), T1D Immunotherapy (21) |
| **MODERATE** (10-20) | Closed Loop AP (20), T1D Stem Cell Cure (19) |
| **LOW** (<10) | Diabetes Epigenetics (6), Drug Repurpose (5), LADA (4) |

Volumes are stable. LADA remains the lowest-activity domain at 4 papers.

### Snapshot Diff (Apr 6 → Apr 7): 15 new papers, 15 dropped (rolling window)

### Cross-Domain Papers (Highest Priority)

These papers appear in multiple alert domains — highest value for synthesis:

1. **PMID 41872174** — *Antigen-specific immunotherapy with a CD4...*
   Domains: T1D Stem Cell Cure, T1D Immunotherapy
   Bridges immunotherapy and cell therapy — review for combination strategy insights.

2. **PMID 41931049** — *GLP-1 Receptor Agonists*
   Domains: T2D GLP-1 New, Diabetes Microbiome
   Cross-domain GLP-1/microbiome link — relevant to our microbiome ML pipeline.

3. **PMID 41907858** — *Oral and cardiometabolic health through the lens of biobanks and large-scale epidemiologic research*
   Domains: T2D Remission, Diabetes Multi-Omics
   Biobank-based multi-omics approach — aligns with Tier 1 Multi-Omics priority.

4. **PMID 41930333** — *Microbiome-Based Clustering Identifies Glycemic Control-Related Subtypes in Youth With Recent-Onset T1D*
   Domains: Diabetes Biomarker, Diabetes Microbiome
   **High priority:** Directly relevant to our microbiome ML pipeline project. Youth T1D + microbiome subtypes = actionable for our research plans.

### Key Therapy Mentions

No new papers mentioning zimislecel, orforglipron, retatrutide, CagriSema, or baricitinib by name in titles/abstracts this cycle. Previously flagged teplizumab paper (PMID 41913320, "Toward Personalized Medicine in T1D") remains in the 30-day window.

### Notable New Papers

- **PMID 41939711** — *Impact of glucokinase activators on the gut microbiome of high-fat diet-induced obese and T2D mice* (Frontiers in Microbiology). Bridges glucokinase and microbiome — relevant to gap analysis (Glucokinase × Microbiome Gut, gap score 99.9).

- **PMID 41919986** — *Unraveling the Molecular Pathways of Insulin-Producing Cells Derived From Placenta Multipotent Stem Cells via Multi-Omics Analysis* (Proteomics). Multi-omics + stem cell islets — relevant to Tier 1 areas.

- **PMID 41938608** — *Technology-driven diabetes care: innovation without equity?* (Frontiers in Digital Health). Health equity + technology — speaks to multiple top gaps.

---

## Gap Analysis Summary

**Analysis date:** 2026-04-03 (4 days old) | 30 domains, 435 pairs analyzed | Validation: BRONZE

### Top 5 Under-Researched Intersections (Unchanged)

| Rank | Domain 1 | Domain 2 | Gap Score | Joint Pubs | Tier 1 Alignment |
|------|----------|----------|-----------|------------|------------------|
| 1 | Beta Cell Regen | Health Equity | 100.0 | 0 | Tier 1 (Epidemiology) |
| 2 | Insulin Resistance | Islet Transplant | 100.0 | 1 | Tier 1 (Multi-Omics) |
| 3 | Islet Transplant | Drug Repurposing | 100.0 | 0 | **Tier 1 — Active project** |
| 4 | Islet Transplant | Health Equity | 100.0 | 0 | Tier 1 (Epidemiology) |
| 5 | Gene Therapy | LADA | 100.0 | 0 | Emerging |

**Key alignment:** Gap #3 (Islet Transplant × Drug Repurposing) continues to validate our active islet repurposing pipeline project.

**New observation today:** PMID 41939711 (glucokinase activators × gut microbiome) directly addresses the Glucokinase × Microbiome Gut gap (ranked with 99.9 score, 2 joint pubs). This paper could reduce the gap score when the analysis is refreshed.

---

## Breaking News (Web Search — April 7, 2026)

### 🔴 CRITICAL: Teplizumab (Tzield) sBLA — PDUFA Date April 29, 2026

The FDA has accepted Sanofi's supplemental BLA for **teplizumab-mzwv (Tzield)** with a **priority review PDUFA date of April 29, 2026**. The sBLA seeks to expand the indication from age 8+ to **children as young as 1 year** for delay of Stage 3 T1D in at-risk patients. This is a **major regulatory milestone** — approval would dramatically expand the eligible population for the only FDA-approved disease-modifying therapy for T1D.

**Action:** Add April 29 PDUFA date to tracker; prepare monitoring for decision announcement.

### 🟢 Stanford Functional Cure Research (April 6, 2026)

Stanford researchers pursuing a "functional cure" for T1D combining stem cell-derived islets with immune modulation strategies. Published via Stanford Today. Complements the MUSC Breakthrough T1D grant reported in last cycle.

### 🟢 Foundayo (Orforglipron) — Confirmed Shipping

Eli Lilly's oral GLP-1 (Foundayo) is now being shipped via LillyDirect following April 1 FDA approval. No new regulatory developments since last report. Tracker update verification still recommended.

### 🟡 Awiqli (Insulin Icodec) — US Availability Expected April 2026

Novo Nordisk's once-weekly insulin Awiqli (approved March 26) is expected to become available in the US this month. Watch for launch announcements.

### 🟡 Ascletis ASC30 — Still Pending

FDA IND clearance for Phase II of oral GLP-1 ASC30 confirmed. No new updates since last report.

### 🔵 Q2 2026 FDA Decisions to Watch (Updated)

| Drug | Sponsor | PDUFA / Decision | Significance |
|------|---------|-----------------|--------------|
| **Tzield sBLA (teplizumab)** | Sanofi | **April 29, 2026** | Expand to age 1+ for T1D delay |
| Afrezza pediatric sBLA | MannKind | May 2026 | First needle-free insulin for ages 4-17 |
| CagriSema | Novo Nordisk | 2026 (timing TBD) | Amylin/GLP-1 combo for T2D/obesity |

---

## Recommended Actions

### Immediate (Today)

1. **🔴 Add Tzield sBLA PDUFA date (April 29) to tracker** — This is the highest-priority near-term regulatory event. Expansion to age 1+ would be transformative for T1D prevention.

2. **⚠️ Re-run gap analysis today** — Data is now 4 days old: `python project1_literature_gap_analysis.py`

### This Week

3. **Review cross-domain paper PMID 41930333** — *Microbiome-Based Clustering in Youth T1D*. Directly relevant to our microbiome ML pipeline and biomarker projects. High priority for integration.

4. **Review PMID 41939711** — *Glucokinase activators × gut microbiome*. Addresses a tracked literature gap (Glucokinase × Microbiome). Could inform gap classification updates.

5. **Review PMID 41872174** — *CD4 antigen-specific immunotherapy*. Cross-domain (stem cell + immunotherapy). Relevant to combination therapy mapping.

6. **Add NCT06964087 (OPT101) to watch list** — New T1D immunotherapy now recruiting. Novel candidate worth tracking.

7. **Add NCT07026968 (Prusogliptin triple combo) to tracker** — Phase 3 GKA + SGLT2i + metformin study with 815 enrolled. Relevant to glucokinase domain tracking.

### Data Refresh Schedule

8. **Gap analysis refresh overdue** — Run today: `python project1_literature_gap_analysis.py`
9. **All daily feeds current** — No script re-runs needed for clinical trials or PubMed.
10. **Monitor Tzield PDUFA April 29** — Set up alert or calendar reminder.
11. **Watch for Awiqli US launch** — Expected this month.

---

*Generated by Diabetes Research Hub automated monitor — 2026-04-07*
*Evidence standards: per RESEARCH_DOCTRINE v1.1*
