# Daily Monitor Report — 2026-03-17

**Scan time:** 2026-03-17 09:06 UTC
**Previous report:** 2026-03-16
**Data sources:** hub_monitor.py, baseline_clinical_trials.py, baseline_pubmed_alerts.py, literature gap analysis, web search

---

## File System Status

| File | Last Modified | Status |
|------|--------------|--------|
| clinical_trials_latest.json (503 KB) | 2026-03-17 08:05 | Fresh |
| clinical_trials_snapshot_2026-03-17.json | 2026-03-17 08:04 | Fresh |
| pubmed_recent_latest.json (95 KB) | 2026-03-17 08:05 | Fresh |
| pubmed_recent_snapshot_2026-03-17.json | 2026-03-17 08:05 | Fresh |
| hub_monitor_report.md | 2026-03-17 08:05 | Fresh |
| literature_gap_data.json (132 KB) | 2026-03-15 00:45 | 2 days old |
| literature_gap_report.md | 2026-03-17 07:42 | Fresh |
| literature_gap_matrix.xlsx | 2026-03-15 00:45 | 2 days old |
| Diabetes_Research_Tracker.xlsx | 2026-03-16 12:16 | 1 day old |
| citation_validation.json | 2026-03-17 07:43 | Fresh |
| evidence_network.json | 2026-03-17 07:43 | Fresh |
| paper_library/index.json | 2026-03-17 | Fresh |

**Hub inventory:** 384 total files tracked (337 new since last hub_monitor scan, 29 modified, 0 removed). Major growth from paper_library additions (197 abstracts, 80 full texts) and new dashboard HTMLs.

**No stale files detected** — all key data files are within the 14-day freshness window.

---

## Clinical Trial Changes

**Total trials tracked:** 748 (up from 746 yesterday)

### New Trials (2)

| NCT ID | Title | Phase | Status | Sponsor | Category |
|--------|-------|-------|--------|---------|----------|
| NCT07472725 | SHR-3167 Fixed-Dose vs. Individualized-Dose Titration | Phase 2 | Not Yet Recruiting | Jiangsu HengRui Medicine | T2D Novel Therapies |
| NCT07474155 | Steno780G Follow-up Study | N/A | Not Yet Recruiting | Steno Diabetes Center Copenhagen | T1D/Devices |

### Status Changes (2)

| NCT ID | Old Status | New Status | Title |
|--------|-----------|-----------|-------|
| NCT07061574 | NOT_YET_RECRUITING | **RECRUITING** | Low Dose ATG With Subsequent Adalimumab — Phase 1/2 immunotherapy trial |
| NCT07212179 | NOT_YET_RECRUITING | **RECRUITING** | Self-Learning Bolus Calculator With Simplified Meal Announcement in Adolescents |

**New results posted:** None

### Key Phase 3 Recruiting Trials (42 total)

Notable active Phase 3 trials by key sponsors:

**Vertex Pharmaceuticals (2 recruiting):**
- NCT04786262: VX-880 cell therapy for T1D (Phase 3) — *flagship islet cell replacement trial*
- NCT06832410: VX-880 efficacy/safety study (Phase 3)

**Eli Lilly (8 recruiting):**
- NCT07222137: **Baricitinib** to delay Stage 3 T1D in adults (Phase 3) — *high priority: key therapy*
- NCT07222332: **Baricitinib** to preserve beta cell function in children/adolescents (Phase 3) — *high priority: key therapy*
- NCT06993792: **Orforglipron** master protocol for obesity (Phase 3) — *FDA approval expected March 2026*
- NCT06971472: Orforglipron for obesity/overweight (Phase 3)
- NCT06739122: Dulaglutide 3.0/4.5 mg in pediatric T2D (Phase 3)
- 3 additional Phase 2 trials (LY3457263, macupatide/eloralintide combo, LY3938577)

**Novo Nordisk (2 recruiting):**
- NCT07076199: Insulin icodec (Awiqli) weekly insulin for T2D (Phase 3) — *FDA approval expected March 2026*
- NCT07271251: Oral semaglutide bioequivalence study (Phase 3)

**Sana Biotechnology:** 0 trials in current dataset

### Trial Counts by Category

| Category | Count |
|----------|-------|
| Diabetes Technology (Devices) | 217 |
| T1D Cure & Cell Therapy | 155 |
| T2D Novel Therapies (Phase 2-3) | 134 |
| T1D Immunotherapy & Prevention | 71 |
| Recently Completed with Results | 244 |

---

## PubMed Highlights

**Unique papers in current window:** 125 (30-day lookback)
**New since yesterday:** 27 papers added, 26 dropped (normal rotation)

### Cross-Domain Papers (Highest Priority)

These papers span multiple research domains — highest synthesis value:

1. **[41836445] Integrated multi-omics profiling reveals immune-related biomarkers and regulatory networks for early prediction of tuberculosis in T2D**
   - Domains: T2D Remission, Diabetes Biomarker, Diabetes Multi-Omics (3 domains)
   - *Significance:* Multi-omics approach to T2D immune biomarkers — relevant to our biomarker and multi-omics gap analysis interests

2. **[41838266] Association of Social Determinants of Health with Utilization of SGLT2 Inhibitors and GLP1 Receptor Agonists: Systematic Review & Meta-Analysis**
   - Domains: T2D GLP-1 New, Diabetes Health Equity (2 domains)
   - *Significance:* Directly relevant to our health equity gap area — quantifies disparities in novel therapy access

3. **[41838755] An inflammatory biomarker panel for prediabetes classification using interpretable machine learning**
   - Domains: Diabetes AI/ML, Diabetes Biomarker (2 domains)
   - *Significance:* AI/ML + biomarker intersection — aligns with high-activity publication domains

### Key Therapy Mentions

| Therapy | Papers in Current Window |
|---------|------------------------|
| Teplizumab | 1 — Clinical practice experience in Stage 2 T1D (PMID 41796109) |
| Zimislecel | 0 |
| Orforglipron | 0 (but FDA approval imminent — see Breaking News) |
| Retatrutide | 0 |
| CagriSema | 0 |
| Baricitinib | 0 (but 2 Phase 3 Lilly trials now recruiting) |

### Publication Volume Trends (30-Day)

| Signal | Domains |
|--------|---------|
| **HIGH ACTIVITY** (>50 papers) | Diabetes AI/ML (193), T2D GLP-1 (147), Microbiome (141), Biomarker (132), Health Equity (62), T2D Remission (52), Multi-Omics (51) |
| **ACTIVE** (10–50) | Complications (44), Gene Therapy (39), T1D Immunotherapy (24), Closed Loop AP (24), T1D Stem Cell (14) |
| **LOW** (<10) | LADA (8), Epigenetics (6), Drug Repurposing (2) |

**Notable:** Diabetes Drug Repurposing has only 2 publications in the 30-day window — this domain remains under-published and aligns with multiple high-scoring gaps in our analysis.

---

## Gap Analysis Summary

**Data freshness:** Gap data from 2026-03-15 (2 days old); report regenerated 2026-03-17
**Domains analyzed:** 30 | **Pairs analyzed:** 435

### Top 5 Under-Researched Intersections

| Rank | Domain Pair | Gap Score | Joint Pubs | Tier 1 Alignment |
|------|------------|-----------|------------|------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | Yes — equity of emerging cell therapies |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | Yes — graft survival mechanism |
| 3 | Islet Transplant × Drug Repurposing | 100.0 | 0 | Yes — computational drug screening opportunity |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | Yes — access equity research absent |
| 5 | Gene Therapy × LADA | 100.0 | 0 | Yes — LADA autoimmune mechanism candidate |

**Convergence with today's data:** The new cross-domain paper [41838266] on social determinants of SGLT2i/GLP-1RA utilization directly supports the Drug Repurposing × Health Equity gap (Rank 12, Score 100.0). This is a potential seed paper for a gap synthesis contribution.

---

## Breaking News

### FDA Actions — March 2026

| Drug | Company | Status | Significance |
|------|---------|--------|-------------|
| **Orforglipron** | Eli Lilly | FDA approval expected March 2026 | First oral non-peptide GLP-1 RA; can be taken with food; A1C reduction ~1.3–1.6%; ~8% body weight loss |
| **Awiqli (insulin icodec)** | Novo Nordisk | FDA approval expected ~March 2026 | First once-weekly basal insulin; reduces injections from 365 to 52/year |
| **CagriSema** | Novo Nordisk | FDA decision expected 2026 | Semaglutide + cagrilintide combination; next-gen GLP-1 |
| **Oral Wegovy (semaglutide 25mg)** | Novo Nordisk | Approved Jan 2026 | First oral GLP-1 for weight loss; now launched in US |
| **AMP-004 (insulin aspart biosimilar)** | Amphastar | FDA decision Q1 2026 | Third insulin aspart biosimilar if approved |
| **ASC30** | Ascletis | IND cleared, Phase II starting Q1 2026 | Oral small molecule GLP-1 |

**Assessment:** Orforglipron and Awiqli are the two most significant imminent approvals. Orforglipron especially could reshape the oral GLP-1 landscape and is directly relevant to our T2D GLP-1 tracking domain (147 papers in 30-day window — highest activity after AI/ML). The baricitinib T1D delay trials (Lilly) moving to recruiting status is also significant for our T1D immunotherapy tracking.

---

## Recommended Actions

### Immediate (Today)

1. **Review cross-domain paper [41838266]** — "Association of Social Determinants of Health with SGLT2i/GLP-1RA Utilization." This systematic review directly maps to our Health Equity gap analysis. Consider adding to tracker as a Tier 1 reference.

2. **Review teplizumab clinical practice paper [41796109]** — Real-world Stage 2 T1D experience with teplizumab in 3 adult patients. Relevant to our T1D immunotherapy monitoring and the active PROTECT extension trial (NCT04598893).

3. **Track NCT07061574 status change** — Low-dose ATG + adalimumab Phase 1/2 trial has begun recruiting. This is a novel immunotherapy combination for T1D worth adding to the tracker's "Notable Trials to Watch" section.

### This Week

4. **Update tracker with orforglipron FDA status** — FDA approval is expected this month. When announced, update the Diabetes_Research_Tracker.xlsx with the approval date and add orforglipron to the key therapies monitoring list.

5. **Update tracker with Awiqli FDA status** — Once-weekly insulin icodec decision also expected imminently.

6. **Monitor Vertex VX-880 Phase 3 trials** — Both NCT04786262 and NCT06832410 are actively recruiting. These are the most advanced islet cell replacement trials globally.

### Data Maintenance

7. **Gap analysis data is 2 days old** — Still within freshness window but consider refreshing later this week:
   `Run: python project1_literature_gap_analysis.py`

8. **All other data pipelines are current** — No scripts need to be re-run today.

---

*Generated by Diabetes Research Hub Daily Monitor — 2026-03-17*
*Evidence classification per Research Doctrine v1.0: All gap scores are BRONZE level (single analytical source)*
