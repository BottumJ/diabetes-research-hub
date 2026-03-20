# Diabetes Research Hub — Daily Monitor Report
**Date:** 2026-03-19
**Previous report:** 2026-03-18
**Automated scan by: diabetes-hub-monitor**

---

## File System Status

| File | Last Modified | Status |
|------|--------------|--------|
| hub_monitor_report.md | Mar 18 09:08 | Fresh (1 day) |
| clinical_trials_latest.json | Mar 18 09:08 | Fresh (1 day) |
| clinical_trials_snapshot_2026-03-18.json | Mar 18 09:07 | Fresh (1 day) |
| pubmed_recent_latest.json | Mar 18 09:08 | Fresh (1 day) |
| pubmed_recent_summary.md | Mar 18 09:08 | Fresh (1 day) |
| literature_gap_data.json | Mar 15 00:45 | Stale (4 days) |
| literature_gap_report.md | Mar 17 19:22 | OK (2 days) |
| hub_monitor_state.json | Mar 18 09:08 | Fresh (1 day) |
| RESEARCH_DOCTRINE.md | Mar 14 | OK |

**Total files tracked:** 438 (54 new, 67 modified since Mar 17 scan)

**Notable new files since last scan:**
- AUDIT_FINDINGS.txt and AUDIT_REPORT.txt added to root
- 4 new analysis scripts: build_drug_repurposing_screen.py, build_lada_diagnostic_model.py, build_trial_equity_mapper.py, extract_evidence.py
- 4 new dashboards: Drug_Repurposing_Screen, Gap_Evidence, LADA_Diagnostic_Model, Trial_Equity_Mapper
- 11 new full-text papers and 29 new abstracts added to paper_library

---

## Clinical Trial Changes

**Snapshot comparison: Mar 17 vs Mar 18**
- Trials in Mar-17 snapshot: 748
- Trials in Mar-18 snapshot: 749
- **New trial added:** 1 (NCT06096506 — Culinary Medicine program in Acres Homes, Houston; completed behavioral intervention; newly posted results)
- Status changes: 0
- Removed trials: 0

### Key Sponsor Phase 3 Trials (Active)

| NCT ID | Title | Sponsor | Status |
|--------|-------|---------|--------|
| NCT06832410 | VX-880 efficacy/safety in T1D | Vertex Pharmaceuticals | RECRUITING |
| NCT04786262 | VX-880 safety/tolerability in T1D | Vertex Pharmaceuticals | RECRUITING |
| NCT07076199 | Weekly insulin icodec (Awiqli) | Novo Nordisk | RECRUITING |
| NCT07222137 | Baricitinib for Stage 3 T1D delay (adults) | Eli Lilly | RECRUITING |
| NCT07222332 | Baricitinib for beta cell preservation (pediatric) | Eli Lilly | RECRUITING |
| NCT06993792 | Orforglipron master protocol (obesity) | Eli Lilly | RECRUITING |
| NCT06971472 | Orforglipron (obesity/overweight) | Eli Lilly | RECRUITING |
| NCT06296603 | Retatrutide vs placebo in T2D | Eli Lilly | ACTIVE_NOT_RECRUITING |
| NCT06259722 | Retatrutide vs semaglutide in T2D | Eli Lilly | ACTIVE_NOT_RECRUITING |
| NCT06221969 | CagriSema blood sugar/weight | Novo Nordisk | ACTIVE_NOT_RECRUITING |
| NCT06534411 | CagriSema blood sugar/weight | Novo Nordisk | ACTIVE_NOT_RECRUITING |

**Trials with posted results:** 246 total across all categories.

### Trial Summary by Category
| Category | Count |
|----------|-------|
| T1D Cure & Cell Therapy | 155 |
| T1D Immunotherapy & Prevention | 71 |
| T2D Novel Therapies (Phase 2-3) | 134 |
| Diabetes Technology (Devices) | 217 |
| Recently Completed with Results | 245 |
| **Total unique trials** | **749** |

---

## PubMed Highlights

**121 unique papers found** across 15 alert domains (30-day lookback).

### High-Activity Domains
- **Diabetes AI/ML:** 200 papers — highest volume domain
- **Diabetes Microbiome:** 148 papers
- **T2D GLP-1 New:** 145 papers — reflecting massive industry/research activity around GLP-1 agents
- **Diabetes Biomarker:** 133 papers
- **Diabetes Health Equity:** 62 papers
- **Diabetes Multi-Omics:** 53 papers

### Low-Activity Domains (potential monitoring gaps or genuinely quiet)
- **LADA New Research:** 8 papers — remains an under-researched area
- **Diabetes Epigenetics:** 6 papers
- **Diabetes Drug Repurpose:** 2 papers — extremely low given Tier 1 priority status

### Cross-Domain Papers (Highest Priority for Review)
These papers span multiple research domains and are highest-value for synthesis:

1. **Integrated multi-omics profiling — TB prediction in T2D** (Ye et al., 2026)
   Domains: T2D Remission, Biomarker, Multi-Omics | [PMID 41836445](https://pubmed.ncbi.nlm.nih.gov/41836445/)

2. **Exosomes in diabetic kidney disease** (Ding et al., 2026)
   Domains: AI/ML, Biomarker, Multi-Omics | [PMID 41845912](https://pubmed.ncbi.nlm.nih.gov/41845912/)

3. **Modulating immune response for T1D prevention/treatment** (Vohidova et al., 2026)
   Domains: T1D Stem Cell Cure, T1D Immunotherapy | [PMID 41777899](https://pubmed.ncbi.nlm.nih.gov/41777899/)

4. **Social determinants of health & SGLT2i/GLP-1RA utilization** (Shah et al., 2026)
   Domains: T2D GLP-1 New, Health Equity | [PMID 41838266](https://pubmed.ncbi.nlm.nih.gov/41838266/)

5. **AI methods for glycemic control in ICU** (Sarwar et al., 2026)
   Domains: AI/ML, Closed Loop AP | [PMID 41844000](https://pubmed.ncbi.nlm.nih.gov/41844000/)

### Papers Mentioning Key Therapies

| Therapy | Paper | PMID |
|---------|-------|------|
| Teplizumab | "Teplizumab in Stage 2 T1D: Clinical Practice Experience" (Guarnotta et al.) | [41796109](https://pubmed.ncbi.nlm.nih.gov/41796109/) |
| Semaglutide (LADA) | "Semaglutide as add-on therapy in LADA" (Lunati et al.) | [41729594](https://pubmed.ncbi.nlm.nih.gov/41729594/) |

No new papers found mentioning zimislecel, orforglipron, retatrutide, CagriSema, or baricitinib in the PubMed alert domains during this cycle.

---

## Gap Analysis Summary

**Last updated:** Mar 17 (literature_gap_report.md) / Mar 15 (literature_gap_data.json)
**Domains analyzed:** 30 | **Pairs analyzed:** 435

### Top 5 Under-Researched Intersections (All Gap Score 100.0)

| Rank | Domain Pair | Joint Pubs | Tier 1 Alignment |
|------|------------|------------|-------------------|
| 1 | Beta Cell Regen + Health Equity | 0 | Yes — Epidemiological Data Analysis |
| 2 | Insulin Resistance + Islet Transplant | 1 | Partial — Clinical Trial Intelligence |
| 3 | Islet Transplant + Drug Repurposing | 0 | Yes — Drug Repurposing Screening |
| 4 | Islet Transplant + Health Equity | 0 | Yes — Epidemiological Data Analysis |
| 5 | Gene Therapy + LADA | 0 | Partial — Literature Synthesis |

### Gaps Aligned with Tier 1 Contribution Areas

- **Drug Repurposing + LADA** (Gap 100.0, 0 joint pubs) — Directly aligns with Tier 1 #4 (Drug Repurposing Computational Screening). LADA patients are treated with generic T2D drugs; systematic repurposing is absent.
- **Drug Repurposing + Health Equity** (Gap 100.0, 0 joint pubs) — Repurposed drugs could yield affordable treatments for underserved populations. Aligns with Tier 1 #4 + #6.
- **Glucokinase + Drug Repurposing** (Gap 100.0, 0 joint pubs) — Screening existing drugs for GK activity is unexplored. Aligns with Tier 1 #4.
- **Health Equity + LADA** (Gap 100.0, 0 joint pubs) — LADA is massively underdiagnosed in minority populations. Aligns with Tier 1 #6.

**Validation level:** BRONZE (single analytical source; requires expert confirmation)

---

## Breaking News

### Significant developments from the past 7 days:

1. **ATTD 2026 Conference (Mar 11-14):** Major sessions on islet cell therapy for T1D cure. Researchers highlighted a two-part approach: lab-made insulin-producing cells paired with custom-engineered immune cells, backed by $1M from Breakthrough T1D. The session focused on manufactured islets at scale without chronic immunosuppression — directly relevant to VX-880 (Vertex) trials in our tracker.

2. **Orforglipron FDA decision expected March 2026:** Eli Lilly's oral GLP-1 is in the FDA's National Priority Voucher program for accelerated review. In trials, it reduced A1C by 1.3-1.6% and ~8% body weight. This would be the first non-peptide oral GLP-1RA.

3. **Awiqli (insulin icodec) FDA decision Mar 29, 2026:** Novo Nordisk's once-weekly basal insulin awaiting approval. Would be first weekly insulin.

4. **Oral semaglutide (Ozempic tablets) approved Feb 2026:** FDA approved 1.5mg, 4mg, 9mg oral semaglutide tablets. US availability expected Q2 2026.

5. **T1D two-part cure approach gaining momentum:** $1M Breakthrough T1D grant for lab-made islets + engineered immune cells. Represents convergence of stem cell and immunotherapy approaches tracked in our Cell Therapy and Immunotherapy categories.

---

## Recommended Actions

### Immediate (Today)

1. **Run scripts to refresh data:**
   - `python hub_monitor.py` — last run Mar 18; due for daily refresh
   - `python baseline_clinical_trials.py` — refresh clinical trial snapshot for Mar 19
   - `python baseline_pubmed_alerts.py` — refresh PubMed alerts

2. **Re-run gap analysis** — literature_gap_data.json is 4 days old (Mar 15):
   - `python project1_literature_gap_analysis.py`

### Review Tasks

3. **Review cross-domain paper on exosomes in DKD** ([PMID 41845912](https://pubmed.ncbi.nlm.nih.gov/41845912/)) — spans AI/ML, Biomarker, and Multi-Omics; relevant to Tier 1 #1 (Multi-Omics Biomarker Integration).

4. **Review teplizumab clinical practice paper** ([PMID 41796109](https://pubmed.ncbi.nlm.nih.gov/41796109/)) — real-world Stage 2 T1D data from 3 adult patients. Relevant to baricitinib Phase 3 trials (NCT07222137, NCT07222332) as disease-modifying comparator.

5. **Review LADA + semaglutide paper** ([PMID 41729594](https://pubmed.ncbi.nlm.nih.gov/41729594/)) — directly addresses the LADA treatment gap (Gap Score 100.0 for Drug Repurposing + LADA).

### Strategic

6. **Track Awiqli FDA decision (Mar 29)** — Add to Notable Trials to Watch in clinical_trials_summary.md if approved.

7. **Track orforglipron FDA decision (March 2026)** — Eli Lilly's oral GLP-1; monitor NCT06993792 and NCT05803421 for updated results.

8. **Monitor ATTD 2026 proceedings** — Conference proceedings from Mar 11-14 may yield new publications in the coming weeks relevant to T1D Stem Cell Cure and T1D Immunotherapy domains.

9. **Drug Repurposing alert volume critically low** — Only 2 papers in 30 days despite being a Tier 1 priority. Consider expanding PubMed alert keywords or running a targeted search.

---

*Generated by diabetes-hub-monitor — 2026-03-19*
*Next scheduled run: 2026-03-20*
