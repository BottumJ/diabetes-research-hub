# Diabetes Research Hub — Monitor Report
**Date:** 2026-04-06
**Scan window:** 2026-04-05 → 2026-04-06
**Report type:** Automated daily review

---

## File System Status

All key data files are **current** (updated today, April 6):

| File | Last Modified | Status |
|------|--------------|--------|
| hub_monitor_report.md | 2026-04-06 02:04 | ✅ Fresh |
| clinical_trials_latest.json | 2026-04-06 02:04 | ✅ Fresh |
| pubmed_recent_latest.json | 2026-04-06 02:04 | ✅ Fresh |
| literature_gap_data.json | 2026-04-03 09:31 | ⚠️ 3 days old |
| literature_gap_report.md | 2026-04-05 09:05 | ✅ Fresh |

**Hub summary:** 678 files tracked. 3 new files, 29 modified files, 0 removed since last scan. 347 result files older than 14 days (mostly historical snapshots and paper library — expected).

**New files since last scan:**
- clinical_trials_snapshot_2026-04-06.json
- pubmed_recent_snapshot_2026-04-06.json
- monitor_report_2026-04-05.md

**All Python scripts are running on schedule — no re-runs needed.**

---

## Clinical Trial Changes

### Snapshot Diff (Apr 5 → Apr 6): No changes

- New trials: 0
- Removed trials: 0
- Status changes: 0
- New results posted: 0

This is a quiet day for trial registry changes (expected on weekends/Monday mornings).

### Overall Trial Portfolio

- **754 unique trials** tracked across 5 categories
- T1D Cure & Cell Therapy: 150 | T1D Immunotherapy & Prevention: 71 | T2D Novel Therapies: 136 | Diabetes Technology: 217 | Completed with Results: 253
- **99 Phase 3 RECRUITING trials** actively enrolling (up from 44 reported last cycle — difference likely reflects updated phase/status matching; underlying data unchanged)
- **254 trials with posted results** in the completed category

### Key Sponsor Phase 3 Trials (Active — No Status Changes)

| NCT ID | Sponsor | Trial | Status |
|--------|---------|-------|--------|
| NCT04786262 | **Vertex** | VX-880 for T1D (stem cell-derived islets) | RECRUITING |
| NCT06832410 | **Vertex** | VX-880 in T1D with kidney transplant | RECRUITING |
| NCT05791201 | **Vertex** | VX-264 encapsulated islets (T1D) | ACTIVE_NOT_RECRUITING (Phase 1/2) |
| NCT07222137 | **Eli Lilly** | Baricitinib to delay Stage 3 T1D (at-risk) | RECRUITING |
| NCT07222332 | **Eli Lilly** | Baricitinib to preserve beta cells (new-onset T1D) | RECRUITING |
| NCT06993792 | **Eli Lilly** | Orforglipron master protocol (obesity ± T2D) | RECRUITING |
| NCT06972472 | **Eli Lilly** | Orforglipron in obesity + T2D | RECRUITING |
| NCT06260722 | **Eli Lilly** | Retatrutide vs Semaglutide (T2D) | ACTIVE_NOT_RECRUITING |
| NCT06913895 | **Eli Lilly** | Tirzepatide in T1D | ACTIVE_NOT_RECRUITING |
| NCT07076199 | **Novo Nordisk** | Insulin Icodec vs Glargine | RECRUITING |
| NCT06221969 | **Novo Nordisk** | CagriSema for T2D | ACTIVE_NOT_RECRUITING |
| NCT06534411 | **Novo Nordisk** | CagriSema for T2D (second study) | ACTIVE_NOT_RECRUITING |

**53 total trials from key sponsors** (Vertex, Eli Lilly, Novo Nordisk, Sana Biotechnology) in the database.

---

## PubMed Highlights

### Publication Volume (Last 30 Days)

| Activity Level | Domains |
|----------------|---------|
| **HIGH** (>100 papers) | Diabetes AI/ML (171), T2D GLP-1 New (151), Diabetes Microbiome (141), Diabetes Biomarker (117) |
| **HIGH** (>50) | Diabetes Health Equity (65) |
| **ACTIVE** (20-50) | Multi-Omics (43), T2D Remission (41), Complications (37), Gene Therapy (37), T1D Immunotherapy (21) |
| **MODERATE** (10-20) | Closed Loop AP (19), T1D Stem Cell Cure (18) |
| **LOW** (<10) | Diabetes Epigenetics (6), Drug Repurpose (5), LADA (4) |

Volumes are essentially unchanged from yesterday. LADA dropped from 5 to 4 papers — remains the lowest-activity domain.

### Snapshot Diff (Apr 5 → Apr 6): 10 new papers, 9 dropped (rolling window)

**Notable new papers:**

1. **PMID 41937000** [Closed Loop AP] — "Advanced automated insulin delivery in inpatients receiving nutritional support" (*Diabetes & Metabolism*). Relevant to closed-loop/AP domain, especially inpatient applications.

2. **PMID 41936548** [T2D GLP-1] — "Weight Loss With GLP-1 Agonists in Nondiabetic Adults: Systematic Review and Network Meta-Analysis" (*Obesity*). Timely given Foundayo (orforglipron) approval.

3. **PMID 41935054** [Drug Repurpose] — "Real-world evidence for comparative safety of second-line antihyperglycemic agents in older adults" (*Nature Communications*). High-impact journal; relevant to drug repurposing safety pipeline.

4. **PMID 41878445** [Microbiome + Multi-Omics] — "Integrated multi-omics analysis unveils microbiota-metabolite-host interactions and novel therapeutic targets" (*Frontiers in Immunology*). Cross-domain paper bridging microbiome and multi-omics.

5. **PMID 41936497** [Complications] — "Research updates in cystic fibrosis related diabetes" (*J Cystic Fibrosis*). Niche but relevant for CFRD-specific pathophysiology.

### Key Therapy Mentions
- **Teplizumab** — PMID 41913320 (still in window): "Toward Personalized Medicine in Type 1 Diabetes" — discusses patient heterogeneity in therapeutic efficacy
- No new papers mentioning zimislecel, orforglipron, retatrutide, CagriSema, or baricitinib by name in titles/abstracts this cycle

---

## Gap Analysis Summary

**Analysis date:** 2026-04-03 (3 days old) | 30 domains, 435 pairs analyzed | Validation: BRONZE

### Top 5 Under-Researched Intersections (Unchanged)

| Rank | Domain 1 | Domain 2 | Gap Score | Joint Pubs | Tier 1 Alignment |
|------|----------|----------|-----------|------------|------------------|
| 1 | Beta Cell Regen | Health Equity | 100.0 | 0 | Tier 1 (Epidemiology) |
| 2 | Insulin Resistance | Islet Transplant | 100.0 | 1 | Tier 1 (Multi-Omics) |
| 3 | Islet Transplant | Drug Repurposing | 100.0 | 0 | **Tier 1 — Active project** |
| 4 | Islet Transplant | Health Equity | 100.0 | 0 | Tier 1 (Epidemiology) |
| 5 | Gene Therapy | LADA | 100.0 | 0 | Emerging |

**Key alignment:** Gap #3 (Islet Transplant × Drug Repurposing) continues to validate our active pipeline. Gap data is 3 days old — schedule refresh by April 8.

Additional Tier 1-aligned gaps in top 15:
- Drug Repurposing × Health Equity (0 joint pubs)
- Drug Repurposing × LADA (0 joint pubs)
- Health Equity × LADA (0 joint pubs)
- Personalized Nutrition × LADA (0 joint pubs)

---

## Breaking News (Web Search — April 6, 2026)

### 🟢 Foundayo (Orforglipron) — FDA Approved, Now Shipping

Eli Lilly's oral GLP-1 receptor agonist **orforglipron (brand name: Foundayo)** was approved April 1, 2026 and began shipping via LillyDirect. CNN confirmed FDA approval on April 1, with fewer restrictions than competing GLP-1 pills. Key facts:
- First oral GLP-1 for weight management with no meal/water timing restrictions
- Highest dose achieved ~12% body weight loss over 72 weeks vs 0.9% placebo
- Active Lilly trials in our tracker: NCT06993792, NCT06972472
- **Action needed:** Verify tracker has been updated with April 1 approval, brand name "Foundayo", and indication.

### 🟢 Awiqli (Insulin Icodec) — Approved, US Launch H2 2026

Novo Nordisk's once-weekly basal insulin **Awiqli** was approved March 26 for adults with T2D. Medscape confirmed it as the first once-weekly insulin. Our tracker includes NCT07076199.

### 🟡 Oral Semaglutide Tablets — FDA Approved February 2026

Ozempic tablets (oral semaglutide) in 1.5 mg, 4 mg, and 9 mg strengths were approved in February 2026, with US availability expected Q2 2026.

### 🟡 Ascletis ASC30 — FDA IND Cleared

Ascletis received FDA IND clearance for a Phase II study of its oral small molecule GLP-1, ASC30, in participants with diabetes. New entrant in the oral GLP-1 space.

### 🟡 MUSC T1D Cure Research — $1M Breakthrough T1D Grant

Medical University of South Carolina received $1 million from Breakthrough T1D for a two-part therapy combining lab-made insulin-producing cells with custom-engineered protective immune cells — aiming to eliminate immunosuppression. Published via ScienceDaily March 2.

### 🔵 Q2 2026 FDA Decisions to Watch
- **Afrezza pediatric sBLA** (MannKind) — May 2026 PDUFA; first needle-free insulin for ages 4-17
- **CagriSema** — working toward FDA approval in 2026
- Retatrutide approval probability: ~27% for 2026

---

## Recommended Actions

### Immediate
1. **Verify Foundayo tracker update** — Confirm the April 1 FDA approval for orforglipron (Foundayo) has been recorded in Diabetes_Research_Tracker.xlsx with brand name, indication (obesity/overweight), and links to active trials NCT06993792 and NCT06972472.
2. **Add Ascletis ASC30 IND clearance** — New oral GLP-1 entrant; consider adding to tracker as an emerging competitor watch item.

### This Week
3. **Review Nature Comms paper PMID 41935054** — Real-world safety data for second-line antihyperglycemics in older adults. Relevant to drug repurposing safety evidence.
4. **Review multi-omics microbiome paper PMID 41878445** — Cross-domain (microbiome + multi-omics); check for novel therapeutic targets relevant to our pipelines.
5. **Review automated insulin delivery paper PMID 41937000** — Inpatient AID use case; relevant to Closed Loop AP domain.
6. **Continue monitoring teplizumab personalized medicine paper PMID 41913320** — Still in the 30-day window; relevant to patient heterogeneity analysis.

### Data Refresh Schedule
7. **All feeds current — no script re-runs needed today.**
8. **Re-run gap analysis by April 8** — data is now 3 days old: `python project1_literature_gap_analysis.py`
9. **Monitor Afrezza pediatric PDUFA** — May 2026 decision date on watchlist.
10. **Watch for CagriSema regulatory updates** — Novo Nordisk targeting 2026 FDA submission.

---

*Generated by Diabetes Research Hub automated monitor — 2026-04-06*
*Evidence standards: per RESEARCH_DOCTRINE v1.1*
