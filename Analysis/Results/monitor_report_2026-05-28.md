# Diabetes Research Hub — Monitor Report
**Generated:** 2026-05-28 (automated scheduled review)
**Compared against:** 2026-05-27 snapshot
**Evidence level for any new claims:** BRONZE (single-source, automated; awaiting human/expert review per Research Doctrine v1.1)

---

## File System Status

All four expected pipeline outputs are present and were refreshed on today's run.

| File | Last Modified | Status |
|------|---------------|--------|
| `hub_monitor_report.md` | 2026-05-28 07:05 | Fresh |
| `clinical_trials_latest.json` | 2026-05-28 07:05 | Fresh |
| `clinical_trials_snapshot_2026-05-28.json` | 2026-05-28 07:05 | Fresh |
| `pubmed_recent_latest.json` | 2026-05-28 07:05 | Fresh |
| `pubmed_recent_snapshot_2026-05-28.json` | 2026-05-28 07:05 | Fresh |
| `literature_gap_report.md` | 2026-05-27 14:22 | Fresh (1 day old) |
| `literature_gap_data.json` | 2026-04-20 15:35 | **STALE — 38 days old** |
| `agent_state.json` | 2026-05-27 14:25 | Fresh |
| `evidence_network.json` | 2026-05-27 14:23 | Fresh |

The hub_monitor scan tracked 873 files: 4 new, 29 modified, 0 removed. The monitor's own review flag reports 652 result files older than 14 days — that count is dominated by historical snapshots and one-off analytical artifacts, but `literature_gap_data.json` is the one Tier 1 file that genuinely needs to be regenerated.

---

## Clinical Trial Changes (vs. 2026-05-27 snapshot)

The overall corpus grew from 798 to 800 trials. The change set is small but contains one item worth tracking.

**New trials (2):**

- NCT07610213 — *Sequential Immune Modulation and Antigen-Specific Tolerance Induction for Disease …* — Abdullah Kars, Phase 1, NOT_YET_RECRUITING. Mentions teplizumab in the program description, which is why it was picked up by the T1D Immunotherapy domain crawler.
- NCT03242343 — *VasQ External Support for Arteriovenous Fistula* — Laminate Medical Technologies, NA phase, COMPLETED. Picked up because its results were posted today (2026-05-27); relevance to diabetes is via dialysis-access in DKD patients, marginal.

**Status changes (2):**

- **NCT07284511 — McGill, Phase 3 tirzepatide-in-T1D trial — moved NOT_YET_RECRUITING → RECRUITING.** This is the more notable change. Tirzepatide as adjunctive therapy in T1D with closed-loop is a Tier 1-adjacent area (Clinical Trial Intelligence + Combination Therapy mapping).
- NCT07408141 — Medtronic MiniMed Fit Payload Wear Study — moved RECRUITING → ACTIVE_NOT_RECRUITING. Routine enrollment completion.

**New results posted (delta vs. yesterday):** 0. However, 47 trials have results posted in the trailing 90-day window. Highlights worth a closer look (from `clinical_trials_latest.json`):

- NCT05514535 — Novo Nordisk **Phase 3 semaglutide + low-dose insulin** (results posted 2026-05-11). Relevant to the Combination Therapy theme. Not yet reviewed in the hub.
- NCT04426474 — Eli Lilly **Phase 1 LY3502970 (orforglipron) in T2D** (results posted 2026-05-26).
- NCT05971940 — Eli Lilly orforglipron Phase 3 in T2D — COMPLETED (older but a touchstone for the broader orforglipron program).

### Active Phase 3 Recruiting Trials — Tier 1 Priority Watchlist

A full re-scan shows 47 Phase 3 trials currently RECRUITING. These remain the highest-priority items for Clinical Trial Intelligence:

T1D Cure & Cell Therapy:
- **NCT06832410** — Vertex VX-880 (zimislecel), Phase 3 in T1D with kidney transplant. RECRUITING.
- **NCT04786262** — Vertex VX-880, Phase 3 in T1D. RECRUITING.
- NCT06951074 — Ain Shams University insulin-producing stem cell transplant. RECRUITING.

T1D Immunotherapy & Prevention:
- **NCT07222332 / NCT07222137** — Eli Lilly **baricitinib (LY3009104)** Phase 3 — one for preserving beta-cell function in children & adolescents, one for delaying Stage 3 T1D in adults. Both RECRUITING. These two studies are the headline T1D-immunotherapy items in the snapshot.
- NCT07284511 — McGill tirzepatide-in-T1D, Phase 3. Newly RECRUITING (see above).
- NCT06217302 — Sotagliflozin in T1D with kidney impairment. RECRUITING.
- NCT07548996 / NCT07258394 — Nanjing Medical University, dimethyl fumarate to preserve beta-cell function in T1D. Both RECRUITING.

T2D Novel Therapies (Phase 2-3): 30 RECRUITING trials, dominated by BrightGene BGM0504 (incretin), Boehringer vicadrostat + empagliflozin, and several SGLT2/DPP-4 combination programs.

### Key-Sponsor Activity

| Sponsor | Total trials in snapshot | RECRUITING |
|---------|------|------------|
| Eli Lilly | 28 | 6 |
| Novo Nordisk | 26 | 2 |
| Vertex Pharmaceuticals | 3 | 2 (both Phase 3 VX-880) |
| Sana Biotechnology | 0 | 0 (still absent from ClinicalTrials.gov diabetes corpus — flag for tracker note) |

**Therapy mentions across the trial corpus** (titles + interventions): orforglipron 3, retatrutide 3, CagriSema 5, baricitinib 2, teplizumab 7, zimislecel 0 (search by VX-880 finds 2 active Phase 3 trials — see Vertex line above). The "zimislecel" string is not yet propagated in ClinicalTrials.gov titles; queries should continue to use both "zimislecel" and "VX-880".

---

## PubMed Highlights (last 30 days, 162 unique papers)

68 papers are new since the 2026-05-27 snapshot, the largest single-day delta in the recent moving window. Domain volume signals are HIGH ACTIVITY for AI/ML (248), Biomarker (178), Microbiome (158), and T2D GLP-1 New (140); LOW for Drug Repurposing (7), LADA (7), and GLP-1 Pharmacogenomics (2). The persistent LOW signal on GLP-1 Pharmacogenomics and Drug Repurposing reinforces the corresponding gap-analysis findings below.

### Cross-Domain Papers (highest priority for review)

15 papers appear in 2+ alert domains. Top items:

- **PMID 42163482** — *Assessing Extracellular Vesicle Proteins as Predictive Biomarkers for Developing Type 1 Diabetes* (Proteomics, 2026-05-20). Three domains: T1D Stem Cell Cure, T1D Immunotherapy, Key Therapy: teplizumab. Tier 1 fit (Multi-Omics Biomarker).
- **PMID 42198313** — *Diabetes Mellitus and Stroke: Pathophysiological Connections and Therapeutic Potential of GLP-1 and GLP-1/GIP Receptor Agonists* (Pharmaceutics, 2026-05-19). Three domains: orforglipron + retatrutide + CagriSema — first review picking up all three next-gen incretins together. Strong candidate for the combination-therapy mapping work.
- **PMID 42148104** — *Adapting CAR-T and CAR-Treg cancer therapies for autoimmunity: innovations and challenges* (Frontiers in Immunology, 2026). T1D Stem Cell Cure + T1D Immunotherapy.
- **PMID 42138126** — *US Patterns in Clinical Islet Autoantibody Ordering and Results Show Key Differences After Teplizumab Regulatory Approval* (JCEM, 2026-05-15). T1D Immunotherapy + Key Therapy: teplizumab. Health-equity-adjacent — worth pulling into the Teplizumab access narrative.
- **PMID 42138080** — *New and emerging therapies in type 1 diabetes mellitus* (J Clin Invest, 2026-05-15). Review covering T1D Immunotherapy + teplizumab.
- **PMID 42195239** — *Metabolic Dysfunction-Associated Steatotic Liver Disease and Incretin Receptor Agonists* (Medicina, 2026-05-18). Biomarker + retatrutide.

### Key-Therapy Mentions (paper-level, current 30-day window)

- **teplizumab** — 5 papers (incl. consensus statement from British Society of Paediatric Endocrinology, PMID 42051156).
- **orforglipron** — 4 papers. Notable: PMID 42120723, *ATTAIN-MAINTAIN Phase 3b* (maintenance trial, 2026-05-13). PMID 42116665, GI-safety network meta-analysis.
- **CagriSema** — 5 papers, including a meta-analysis vs. semaglutide monotherapy (PMID 41759565).
- **retatrutide** — 5 papers; PMID 42135195 covers lipid/metabolite profiles in obesity ± T2D.
- **baricitinib** — 4 papers; only one is in a diabetes-relevant context (a dermatology case report). The two Phase 3 T1D baricitinib trials (NCT07222332/NCT07222137) have **not** yet produced PubMed-indexed publications.
- **icodec** — 5 papers, 6 hits across topics.
- **dapagliflozin** — broadest footprint (43 total counts).
- **zimislecel** — **0 papers in the 30-day window.** Even after the recent NEJM piece on stem-cell-derived islets, there is no PubMed-indexed publication using the "zimislecel" string in this window. Flag for terminology check.

---

## Gap Analysis Summary

`literature_gap_report.md` was regenerated 2026-05-27; the underlying `literature_gap_data.json` is from 2026-04-20 (38 days old — re-run recommended).

### Top 5 under-researched intersections (Gap Score 100.0)

1. **Beta Cell Regen × Health Equity** (joint pubs: 0). Regenerative therapies vs. access equity.
2. **Insulin Resistance × Islet Transplant** (joint pubs: 1). Graft-survival biology vs. metabolic background.
3. **Islet Transplant × Drug Repurposing** (joint pubs: 0). Repurposable immunosuppressants/cytoprotectants for islet protection.
4. **Islet Transplant × Health Equity** (joint pubs: 0). Geographic and demographic access to islet-cell programs.
5. **Gene Therapy × LADA** (joint pubs: 0). LADA's slow-burn autoimmunity is a candidate substrate for gene therapy.

### Alignment with Tier 1 Contribution Areas (per RESEARCH_DOCTRINE.md)

The gaps map directly onto our Tier 1 strengths:

- **Drug Repurposing × Islet Transplant**, **Drug Repurposing × Health Equity**, **Drug Repurposing × LADA**, **Glucokinase × Drug Repurposing** — all Tier 1 (Drug Repurposing Computational Screening, score 18/20).
- **Beta Cell Regen × Health Equity**, **Islet Transplant × Health Equity**, **Health Equity × LADA** — Tier 1 (Epidemiological Data Analysis, score 17/20).
- **Insulin Resistance × Islet Transplant** — straddles Tier 1 Clinical Trial Intelligence and Multi-Omics work.

These are the gap pairs where the hub has the data access and the computational tooling to produce a meaningful, expert-validatable contribution.

---

## Breaking News (last 7 days, web check)

Two items rise above the routine noise:

1. **Retatrutide TRIUMPH-1 Phase 3 obesity results disclosed by Eli Lilly on 2026-05-21.** Up to ~30% mean weight loss at 12 mg over 80 weeks; 45.3% of participants ≥30% weight loss. The full multi-trial program (TRIUMPH-2 in T2D, TRIUMPH-3 in established CVD) is expected later this year. Likely to drive a wave of follow-on PubMed activity in the next 30-day window.
2. **MannKind Afrezza pediatric sBLA — PDUFA 2026-05-29 (tomorrow).** If approved, first needle-free insulin option for pediatric T1D/T2D. Worth a same-week tracker entry. Approval status should be verified by the next scheduled run.

Vertex VX-880 (zimislecel) Phase 3 readout is still expected within 2026 but no May results were announced in this window.

---

## Recommended Actions

Concrete, prioritized:

1. **Re-run gap analysis.** `literature_gap_data.json` is 38 days old. Run `python project1_literature_gap_analysis.py` to refresh the underlying counts; the report is already current but the data file backs the dashboards.
2. **Update tracker** with the McGill tirzepatide-in-T1D Phase 3 status change (NCT07284511 → RECRUITING) and the two new Vertex Phase 3 zimislecel rows (NCT06832410, NCT04786262) if not already on the watchlist.
3. **Add a tracker row for the two Phase 3 baricitinib trials** (NCT07222332, NCT07222137) — both Eli Lilly, both RECRUITING. These are the most novel Phase 3 immunotherapy entries in the current snapshot and currently lack PubMed coverage.
4. **Pull and review the four highest-priority cross-domain PubMed papers** (PMIDs 42163482, 42198313, 42138126, 42138080). The Pharmaceutics review (42198313) is the strongest candidate for the GLP-1 combination-therapy mapping work.
5. **Investigate the "zimislecel" naming gap.** Zero PubMed hits in 30 days despite active Phase 3 trials. Likely a terminology issue — verify queries are running on both "zimislecel" and "VX-880" in `baseline_pubmed_alerts.py`, and confirm the NEJM stem-cell islet article (Vertex) is being captured.
6. **Pick one Tier 1 gap to prosecute.** *Drug Repurposing × Islet Transplant* (gap score 100, joint pubs 0) maps cleanly to the Tier 1 Drug Repurposing pipeline (DrugBank + OpenTargets + STRING network analysis). The existing `islet_repurposing_drug_candidates.json` and `islet_repurposing_network_analysis.json` from April are an obvious starting point — extending them into a formal gap-fill writeup would be the highest-leverage next deliverable.
7. **Verify Afrezza pediatric PDUFA outcome** on 2026-05-29; add to tracker if approved.
8. **Re-run pubmed alerts** in 7 days to capture the post-TRIUMPH-1 publication wave.

---

## Evidence & Validation Notes (per Research Doctrine v1.1)

- File reads above are direct from the live JSON / MD outputs as of 2026-05-28 07:05.
- Web-search findings on retatrutide TRIUMPH-1 and the Afrezza PDUFA are **single-source** and BRONZE-level — confirm against ClinicalTrials.gov results posting and FDA approvals page before adding to the tracker as established facts.
- Gap-analysis intersections remain BRONZE pending domain-expert classification; cross-reference Cochrane and PROSPERO before publishing any "no work exists" claim externally.
- The "zero zimislecel papers" finding is a query artifact, not a research finding — do not propagate.

---

*Generated by Diabetes Research Hub automated monitor — 2026-05-28*
