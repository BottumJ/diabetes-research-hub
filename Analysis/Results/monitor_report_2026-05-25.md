# Diabetes Hub Monitor Report — 2026-05-25

**Scan time:** 2026-05-25 (Monday)
**Previous report:** monitor_report_2026-05-24.md
**Scope:** Daily review of script outputs + 7-day web scan
**Evidence level:** BRONZE (single analytical pass; web items unverified beyond press releases)

---

## TL;DR — Actionable Items

1. **Lilly retatrutide Phase 3 obesity readout (May 21):** ATTAIN-1/TRIUMPH-1 reported up to **28.3% weight loss at 80 weeks** with 12 mg dose; TRIUMPH-2 (T2D) and TRIUMPH-3 (CVD) expected later this year. Update tracker for NCT05929079, NCT06260722, NCT06297603.
2. **MannKind Afrezza pediatric PDUFA: May 29, 2026** (4 days out) — first potential needle-free insulin for kids with T1D/T2D. Add to watch list.
3. **literature_gap_data.json is 34 days old** (last refreshed 2026-04-20). Re-run `python project1_literature_gap_analysis.py` to refresh gap matrix.
4. **2 new cross-domain PubMed papers today** — both deserve review:
   - PMID 42176172 — gut microbiome / multi-omics
   - PMID 42178167 — circadian / multi-omics for diabetic nephropathy
5. **5 trial status changes** in last week; PACTAID (NCT06730906) moved from RECRUITING → ENROLLING_BY_INVITATION.

---

## File System Status

| File | Modified | Age | Status |
|------|----------|-----|--------|
| hub_monitor_report.md | 2026-05-25 07:05 | fresh | OK |
| clinical_trials_latest.json | 2026-05-25 07:04 | fresh | OK |
| pubmed_recent_latest.json | 2026-05-25 07:05 | fresh | OK |
| literature_gap_report.md | 2026-05-24 14:08 | 1d | OK |
| **literature_gap_data.json** | **2026-04-20 15:35** | **34d** | **STALE — refresh recommended** |
| agent_state.json | 2026-05-24 08:09 | 1d | OK |
| citation_validation.json | 2026-05-24 14:08 | 1d | OK |

Hub monitor flagged **606 result files older than 14 days** — most are daily snapshot archives and can be ignored; the salient stale file is the gap-analysis raw data above.

**Hub-monitor file summary (today's scan):**
- 3 new files (today's clinical_trials, pubmed, and monitor report snapshots)
- 29 modified files (dashboards + state files refreshed by yesterday's pipeline run)
- 0 removed files; 862 total tracked

---

## Clinical Trial Changes

**Total trials tracked: 797** (vs 795 on 2026-05-18)

### Category distribution (current)

| Category | Count |
|----------|-------|
| Diabetes Recently Completed with Results | 281 |
| Diabetes Technology (Devices) | 225 |
| T1D Cure & Cell Therapy | 153 |
| T2D Novel Therapies (Phase 2-3) | 140 |
| T1D Immunotherapy & Prevention | 71 |

### Phase 3 RECRUITING — 46 active trials

Highest-priority active recruitment by therapeutic area:

**Beta-cell / cell therapy**
- **NCT06832410** & **NCT04786262** — Vertex VX-880 (zimislecel) Phase 3
- NCT06951074 — Ain Shams stem-cell T1D
- NCT07258394 — Dimethyl fumarate β-cell preservation (Nanjing Medical)

**T1D immunotherapy**
- **NCT07222332** & **NCT07222137** — Lilly baricitinib (pediatric β-cell preservation + Stage 3 delay)
- NCT07088068 — Sanofi teplizumab vs placebo

**T1D adjunct therapy / closed loop**
- NCT06334133 — vTv cadisegliatin (glucokinase activator) adjunctive to insulin
- NCT06630585 — Bern GIP/GLP-1RA + AID
- NCT07076199 — Novo Nordisk weekly insulin icodec in T1D
- NCT06082063 — Steno multifactorial CV intervention in T1D
- NCT06217302 — Sotagliflozin slowing kidney decline in T1D+CKD

**T2D + GLP-1 program (Lilly/Novo concentration)**
- Lilly: 27 active trials (orforglipron, retatrutide, tirzepatide, baricitinib, dulaglutide)
- Novo Nordisk: 26 active trials (CagriSema, icodec, oral semaglutide, NNC0487)
- Vertex: 3 active trials (VX-880/VX-264)
- **Sana Biotechnology: 0** trials in tracked dataset — worth a manual ClinicalTrials.gov search

### Week-over-week changes (2026-05-18 → 2026-05-25)

**7 new trials added:**

| NCT | Phase / Status | Category | Title |
|-----|----------------|----------|-------|
| NCT07594145 | PHASE2 / Not Yet | T1D Immuno | Precision T1D Platform — Cardio-Renal Complications |
| NCT07602036 | NA / Not Yet | Devices | T2D and Pregnancy single-arm |
| NCT07599982 | NA / Not Yet | Devices | MODI insulin titration algorithm safety |
| NCT07593625 | NA / Not Yet | Devices | Next-Gen AID Algorithm in T1D |
| NCT07604922 | NA / Not Yet | Devices | HEMI & SPG vascular signals in diabetes |
| NCT07595289 | NA / Not Yet | Devices | DP-DCT 1.0: Dapagliflozin + CGM combination |
| NCT03919877 | NA / Completed | Completed | Precision Diets for Diabetes Prevention |

**5 status changes:**
- NCT06467955 (MagDI Canada): RECRUITING → ACTIVE_NOT_RECRUITING
- NCT06073457 (MGI/MGJ magnetic diversion): RECRUITING → ACTIVE_NOT_RECRUITING
- NCT06730906 (PACTAID T1D exercise app): RECRUITING → ENROLLING_BY_INVITATION
- NCT07372872 (MyGlucoCare GDM app): NOT_YET → RECRUITING
- NCT05950659 (WIREDUP wearable insoles): NOT_YET → RECRUITING

**5 trials dropped from feed:** NCT03961347 (Lactobacillus johnsonii in T1D), NCT06672172 (HRS-7535), NCT06613711 (MagDI Italy), NCT04545151 (verapamil SR in T1D), NCT03895437 (DAWN T1D). Worth checking ClinicalTrials.gov to determine if these were withdrawn, completed, or simply outside the search query window.

**No new results posted** in the past week.

---

## PubMed Highlights

**155 unique papers** in the rolling 30-day window across 16 alert domains. **106 new since 2026-05-18; 12 dropped from yesterday's window.**

### Cross-domain papers (14 total — highest priority)

These appear in ≥2 alert domains:

| PMID | Title | Domains | Date |
|------|-------|---------|------|
| **42171301** | Dietary diversity & T2D in Chinese cohorts: multi-omics | Biomarker + Microbiome + Multi-Omics | 2026-05-21 |
| **42163482** | Extracellular Vesicle Proteins as Predictive Biomarkers for T1D | T1D Stem Cell + T1D Immuno + teplizumab | 2026-05-20 |
| **42178167** | Circadian rhythm genes in diabetic nephropathy: multi-omics MR | Epigenetics + Multi-Omics | 2026-Dec (pre-print) |
| **42176172** | Gut microbiome bioactive ingredients in fermented foods | Microbiome + Multi-Omics | 2026-05-23 |
| **42171711** | Epigenetic signatures in T2D | T2D Remission + Epigenetics | 2026-05-22 |
| **42163256** | Tissue-specific effects of glucose-lowering drugs on aging via DNA methylation | Epigenetics + Multi-Omics | 2026-05-21 |
| **42148104** | CAR-T / CAR-Treg for autoimmunity | T1D Stem Cell + T1D Immuno | 2026 |
| **42143506** | Evolution of CAR therapies (oncology + autoimmunity) | T1D Immuno + Gene Therapy | 2026-Aug |
| **42138126** | US patterns in islet autoantibody ordering post-teplizumab | T1D Immuno + teplizumab | 2026-05-15 |
| **42138080** | New/emerging therapies in T1D (review) | T1D Immuno + teplizumab | 2026-05-15 |
| **42174929** | Clinical predictors of diabetes/prediabetes: explainable AI | T2D Remission + AI/ML | 2026-05-21 |
| **42168638** | Dysesthesia & GLP-1 agonist therapies: data-mining/literature | T2D GLP-1 + retatrutide | 2026-05-22 |
| **42171425** | HDGF as serological marker for proliferative DR (Mendelian) | Biomarker + Complications | 2026-05-01 |
| **42142983** | Bariatric surgery + GLP-1 audit | retatrutide + CagriSema | 2026-05-17 |

### Key therapy mentions (30-day window)

| Therapy | Papers | Notable |
|---------|--------|---------|
| **dapagliflozin** | 5 (36 total hits) | PMID 42175994 — corrects hypomagnesemia in kidney transplant; PMID 42172900 — klotho + dapagliflozin restores mitochondrial fxn in DKD |
| **teplizumab** | 5 | PMID 42051156 — Consensus statement on clinical use in Stage 2 T1D |
| **retatrutide** | 5 | PMID 42135195 — lipid/metabolite profiles in obesity ± T2D; PMID 42108533 — triple-receptor agonism for CKM |
| **icodec** | 5 | PMID 42168822 — simplified switching without one-time additional dose; PMID 42119975 — pooled safety in T1D + T2D |
| **orforglipron** | 3 | **PMID 42120723 — ATTAIN-1 Phase 3b body-weight maintenance** |
| **CagriSema** | 3 | PMID 41759565 — systematic review vs semaglutide monotherapy |
| **baricitinib** | 3 | All off-label/dermatologic case reports; no T1D-specific β-cell paper this window |
| **zimislecel** | **0** | No new PubMed papers in 30-day window — but Phase 3 (FORWARD-101) is enrolling (NCT06832410). NEJM paper published mid-2025. |

### Domain activity

Highest publication volume this 30-day window:
- T1D Stem Cell Cure / Immunotherapy / Gene Therapy: 10 each
- T2D GLP-1 / Remission / AI-ML / Biomarker / Complications / Microbiome: 10 each
- Closed Loop AP, Multi-Omics, Health Equity: 10 each
- Epigenetics: 9
- LADA, Drug Repurposing: 6 (notable: LADA gained PMID 42152488 — misclassification of T1D as T2D in adults, practical guidance)
- GLP-1 Pharmacogenomics: 1 (low — confirms persistent gap)

---

## Gap Analysis Summary

**Source:** `literature_gap_report.md` (regenerated 2026-05-24) — but underlying `literature_gap_data.json` is dated **2026-04-20** (34 days old). Recommend re-running before any external claims are derived from this.

### Top 5 under-researched intersections (Gap Score 100, 0–1 joint pubs)

| # | Pair | Joint Pubs | Why it matters (per report rationale) |
|---|------|-----------|---------------------------------------|
| 1 | **Beta Cell Regen × Health Equity** | 0 | Regenerative therapies need access analysis as VX-880-class products advance |
| 2 | **Insulin Resistance × Islet Transplant** | 1 | IR in graft recipients affects survival — barely studied |
| 3 | **Islet Transplant × Drug Repurposing** | 0 | Computational screening of existing immunosuppressants for islet protection unexplored |
| 4 | **Islet Transplant × Health Equity** | 0 | Only available at select centers; access equity literature absent |
| 5 | **Gene Therapy × LADA** | 0 | LADA's autoimmune mechanism could plausibly benefit from gene therapy |

**Tier-1 alignment note (per Research Doctrine):** Gaps #1, #3, and #4 cluster around the Tier-1 "Islet Transplant" focus area and provide three concrete review/synthesis angles. Gap #5 (Gene Therapy × LADA) aligns with the LADA Diagnostic Model Tier-2 work already in the hub.

---

## Breaking News (Web Scan — Last 7 Days)

Three items rose above the routine-noise threshold:

1. **Eli Lilly retatrutide Phase 3 obesity (TRIUMPH-1 / ATTAIN-1) readout — 2026-05-21.** Up to 28.3% weight loss at 80 weeks on 12 mg; 45.3% of participants achieved ≥30% loss. Confirmed by PubMed PMID 42120723 in today's snapshot (ATTAIN-1 weight-maintenance arm). TRIUMPH-2 (T2D) and TRIUMPH-3 (CVD) expected later 2026 — these will be the more directly diabetes-relevant readouts to watch.
2. **MannKind Afrezza pediatric sNDA — PDUFA May 29, 2026.** First potential needle-free inhaled insulin in pediatrics if approved. Decision is 4 days away from this report date.
3. **Vertex zimislecel — Phase 3 (FORWARD-101) confirmed enrolling.** Two NCT IDs in our tracker (NCT06832410, NCT04786262). Regulatory submissions still tracking to 2026. No new clinical readout this week, but worth flagging that zero new PubMed papers appeared in our 30-day window — likely a brief gap between the 2025 NEJM publication and the Phase 3 interim.

Earlier-month context (not in 7-day window but flagged for tracker context): Awiqli (insulin icodec) FDA approval 2026-03-26; Langlara (insulin glargine biosimilar) FDA approval 2026-04-29; first generic dapagliflozin tablets approved (date not pinned in this scan).

---

## Recommended Actions

Ranked by urgency:

1. **Re-run `python project1_literature_gap_analysis.py`** — `literature_gap_data.json` is 34 days old; refreshing now will incorporate the 5-week window of new publications before any external use of the gap rankings.
2. **Tracker update for Lilly retatrutide Phase 3 program** — annotate NCT05929079, NCT06260722, NCT06297603 with the 2026-05-21 ATTAIN-1/TRIUMPH-1 readout and forthcoming TRIUMPH-2 / TRIUMPH-3 expectations.
3. **Add MannKind Afrezza pediatric PDUFA (2026-05-29) to the watch list** — re-scan after May 29 to capture the FDA decision.
4. **Review cross-domain paper PMID 42171301** (multi-omics dietary diversity / T2D) — triple-domain hit (Biomarker + Microbiome + Multi-Omics) is unusual and likely worth full-text retrieval into `Analysis/Results/paper_library/fulltext/`.
5. **Investigate the 5 trials dropped from the feed** (NCT03961347, NCT06672172, NCT06613711, NCT04545151, NCT03895437) — confirm whether each was withdrawn, completed, or simply fell out of the search query, and update tracker notes accordingly.
6. **Add Sana Biotechnology to a manual ClinicalTrials.gov check** — zero hits in today's feed despite being listed as a key sponsor; the dataset's search query may not be catching their trial IDs.
7. **Manual review of new cross-domain papers PMID 42176172 & 42178167** — both flagged in today's hub_monitor automated diff; align with Tier-2 Microbiome and Epigenetics work.
8. **Note for Doctrine compliance:** All gap rankings above remain at BRONZE validation level. Any external publication or claim based on the top-5 gaps requires triple-source confirmation (Cochrane / PROSPERO + manual PubMed verification + domain-expert review) before promotion to SILVER or GOLD.

---

## Methodology & Validation

- File reads were performed directly; counts and diffs were computed programmatically against the on-disk JSON snapshots.
- Web scan used two targeted queries; only items confirmed by a primary source (Lilly press release, FDA / PDUFA calendar, Vertex investor materials) were retained.
- This is a **review-only** run — no existing files were modified.
- Per Research Doctrine, this report is BRONZE-level (single analytical pass) and is suitable for internal triage, not external citation.

---

*Generated by the Diabetes Hub Monitor scheduled task — 2026-05-25*
