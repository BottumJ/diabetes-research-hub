# Diabetes Hub Monitor Report — 2026-04-21

**Generated:** 2026-04-21 (automated scheduled run)
**Previous report:** monitor_report_2026-04-20.md
**Scope:** Review of Analysis/Results/ against prior snapshots, plus web scan for breaking news.

---

## File System Status

All expected script outputs are present and current.

| File | Last Modified | Status |
|------|---------------|--------|
| clinical_trials_latest.json | 2026-04-21 07:05 | Fresh (today) |
| pubmed_recent_latest.json | 2026-04-21 07:05 | Fresh (today) |
| literature_gap_data.json | 2026-04-20 15:35 | 1 day old — OK |
| literature_gap_report.md | 2026-04-20 15:35 | 1 day old — OK |
| hub_monitor_report.md | 2026-04-21 07:05 | Fresh (today) |
| Diabetes_Research_Tracker.xlsx | 2026-04-17 14:50 | 4 days old |
| RESEARCH_DOCTRINE.md | 2026-04-01 | 20 days old |

No stale files (>14 days) among active monitoring outputs. Tracker is within normal update cadence.

**Note on hub_monitor_report.md:** This run flagged 723 "new" files and 720 "removed" files. This is a session-path artifact (previous scan ran under `/sessions/optimistic-happy-einstein/...`, current session is `/sessions/confident-blissful-goldberg/...`). Actual file inventory is unchanged — no action needed, but the hub_monitor_state.json could be rebased to avoid the false diff on the next run.

---

## Clinical Trial Changes

**Snapshot totals:** 767 unique trials tracked (151 T1D cure/cell, 71 T1D immunotherapy, 137 T2D novel, 222 tech, 260 completed-with-results). 263 RECRUITING, 130 NOT_YET_RECRUITING, 109 ACTIVE_NOT_RECRUITING.

### Changes since 2026-04-20 (yesterday)

- **2 status transitions** (both meaningful):
  - **NCT06972472** — *Orforglipron (LY3502970) in Obesity+T2D* (Eli Lilly, Phase 3, n=600): **RECRUITING → ACTIVE_NOT_RECRUITING**. Enrollment closed; readout window now relevant. Completion target 2027-08.
  - **NCT05683990** — *Diamyd® in at-risk T1D* (Diamyd Medical, Phase 2, n=5): **RECRUITING → ACTIVE_NOT_RECRUITING**. Small cohort; feasibility endpoint.
- **0 new trials registered** in the past 24 hours.
- **0 newly posted results** in the past 24 hours.

### Changes since 2026-04-14 (7-day window)

- **7 new trials** appeared in scope. Highlights:
  - **NCT05727579** — *DiEtary Sodium Intake Effects on Ertugliflozin-induced GFR changes* (Amsterdam UMC, Phase 4, now COMPLETED). Worth watching for results post — relevant to SGLT2-kidney mechanism (Tier 1 area 10).
  - **NCT05238142** — *MiniMed™ 780G Pump Automated Control in T2D* (Medtronic, COMPLETED). First major hybrid closed-loop T2D study to close.
  - **NCT07533604** — *SnapDandCGMinType2Diabetes* (Ramathibodi Hospital, RECRUITING). New T2D CGM study.
- **3 status transitions:**
  - NCT07340320 — CX11 tablets in T2D (Corxel Pharma, Phase 2): NOT_YET → RECRUITING.
  - Plus the two listed above (NCT06972472, NCT05683990).
- **2 trials dropped from scope** (NCT06897202 Metsera MET097 obesity, NCT05803421 Lilly orforglipron vs insulin glargine) — likely category reclassification or sponsor-side record changes; not a signal by themselves.

### Phase 3 priority watchlist (key sponsors, currently RECRUITING)

| NCT | Sponsor | Intervention | Relevance |
|-----|---------|--------------|-----------|
| NCT06832410 | Vertex | VX-880 (zimislecel) | Lead islet-cell therapy Phase 3 |
| NCT04786262 | Vertex | VX-880 | Earlier Phase 3 cohort |
| NCT07222332 | Eli Lilly | Baricitinib to preserve β-cell function | Tier 1 drug repurposing intersection |
| NCT07222137 | Eli Lilly | Baricitinib to delay Stage 3 T1D (at-risk) | Prevention window |
| NCT07076199 | Novo Nordisk | Insulin Icodec | Weekly basal insulin |
| NCT06739122 | Eli Lilly | Dulaglutide 3.0/4.5 mg pediatric T2D | Pediatric GLP-1 |
| NCT06993792 | Eli Lilly | Orforglipron master protocol | Companion to the just-closed NCT06972472 |
| NCT07088068 | Sanofi | Teplizumab Phase 3 | Head-to-head window |

Vertex has 3 active trials (2 Phase 3 VX-880, 1 Phase 1/2 VX-264). Eli Lilly has 14 active, Novo Nordisk 10, Sana 0.

### Newly posted results

**None** in the latest snapshot. The corpus currently contains 260 completed-with-results trials; no new results postings captured in the past 7 days. (Consistent with industry pattern — bulk result postings typically cluster around ADA/EASD meetings.)

---

## PubMed Highlights

**Last 30 days:** 139 unique papers across 16 alert domains + 8 key-therapy trackers.

### Cross-domain papers (highest priority — 10 total)

Papers indexed across ≥2 domains are the richest signal. Top examples from this window:

- **[PMID 42002040](https://pubmed.ncbi.nlm.nih.gov/42002040/)** — *Ketosis-Prone Type 2 Diabetes Mellitus: Three Decades of Clinical, Pathophysiologic, and Therapeutic Insights* (Umpierrez et al., *Endocrine Practice*, 2026-Apr-17). **3 domains:** T2D GLP-1 New, T2D Remission, LADA New Research. Directly relevant to the diabetes subtype misdiagnosis workstream (Doctrine area 11).
- **[PMID 41997446](https://pubmed.ncbi.nlm.nih.gov/41997446/)** — *GIPR:GCGR co-agonism restores normal weight in obese rodents* (Perez-Tilve et al., *Molecular Metabolism*, 2026-Apr-15). **3 domains** including retatrutide. Preclinical — label accordingly per Doctrine rules.
- **[PMID 42003658](https://pubmed.ncbi.nlm.nih.gov/42003658/)** — *New Horizons in Metabolic Health: Unveiling the Future of Drug Discovery and Development* (Zhao et al., 2026-Apr-13). **3 domains:** Microbiome, Gene Therapy, dapagliflozin.
- **[PMID 41995155](https://pubmed.ncbi.nlm.nih.gov/41995155/)** — *Engineering immune-evasive islet replacement: cell-intrinsic and peri-graft strategies* (Kim et al., *Biomaterials Science*, 2026-Apr-17). T1D Stem Cell + Gene Therapy.
- **[PMID 41913320](https://pubmed.ncbi.nlm.nih.gov/41913320/)** — *Toward Personalized Medicine in Type 1 Diabetes: Patient Heterogeneity and Therapeutic Response* (2026-Mar-30). T1D Immunotherapy + teplizumab.
- **[PMID 41986815](https://pubmed.ncbi.nlm.nih.gov/41986815/)** — *Multi-tissue multi-omics integration reveals tissue-specific pathways, gene networks and drug candidates for T2D* (*Diabetologia*, 2026-Apr-15). Drug Repurposing + Multi-Omics — direct hit on Tier 1 areas 1 and 4.

### Key therapy mentions

- **orforglipron** — 2 new papers, including **[PMID 41984238](https://pubmed.ncbi.nlm.nih.gov/41984238/)** *"Methodological and statistical inconsistencies compromise the efficacy and safety analyses of orforglipron"* (2026-Apr-15). Warrants review before citing ACHIEVE-1/2 results in any synthesis.
- **retatrutide** — 3 papers including [PMID 41785010](https://pubmed.ncbi.nlm.nih.gov/41785010/) clinical overview.
- **teplizumab** — 4 papers; heterogeneity-in-response paper (PMID 41913320) is most actionable.
- **zimislecel, CagriSema, baricitinib, icodec** — 0 PubMed hits in the 30-day window (trials are active but publications lag; expected).

### Domain volume signals

High activity (10+ papers / 30 days): T1D Stem Cell Cure, T1D Immunotherapy, T2D GLP-1 New, T2D Remission, Gene Therapy, AI/ML, Biomarker, Health Equity, Multi-Omics, Microbiome, Closed Loop AP, Complications. Low/flat: GLP-1 Pharmacogenomics (1), LADA (4), Drug Repurpose (4), Epigenetics (7). GLP-1 Pharmacogenomics remains the weakest signal — consistent with prior reports and with the doctrine-flagged gap.

### New papers since the 2026-04-20 snapshot

27 papers entered the corpus overnight. Most notable:
- [PMID 42002040](https://pubmed.ncbi.nlm.nih.gov/42002040/) — KPDM review (already highlighted above, cross-domain).
- [PMID 42007565](https://pubmed.ncbi.nlm.nih.gov/42007565/) — *Replication of 10 novel loci involved in plasma protein N-glycosylation* (Glycobiology, 2026-Apr-20). Relevant to Tier 1 multi-omics biomarker work.
- [PMID 42000722](https://pubmed.ncbi.nlm.nih.gov/42000722/) — *Glycaemic variability underlies myocyte dysfunction and myocardial injury risk in diabetes* (*Nature Communications*, 2026-Apr-18). Strong mechanism paper linking CGM-derived variability to cardiac risk — relevant to complications prediction.
- [PMID 42002107](https://pubmed.ncbi.nlm.nih.gov/42002107/) — *Depressed mood and suicidal thoughts reporting with GLP-1 RAs: WHO VigiBase study* (*J Affect Disord*, 2026-Apr-17). Pharmacovigilance signal worth flagging in the GLP-1 synthesis.

---

## Gap Analysis Summary

Source: `literature_gap_report.md` (generated 2026-04-20; age 1 day — no re-run needed).

**Top 5 under-researched intersections** (all gap score = 100.0, meaning essentially zero joint publications vs. expected):

1. **Beta Cell Regen × Health Equity** — 0 joint, 1,614 expected.
2. **Insulin Resistance × Islet Transplant** — 1 joint, 2,138 expected.
3. **Islet Transplant × GWAS/Polygenic** — 0 joint, 1,103 expected.
4. **Islet Transplant × Personalized Nutrition** — 0 joint, 378 expected.
5. **Islet Transplant × Drug Repurposing** — 0 joint, 373 expected.

### Alignment with Tier 1 contribution areas

Several top gaps sit inside our Tier 1 wheelhouse per RESEARCH_DOCTRINE.md:

- **Islet Transplant × Drug Repurposing** (Tier 1 area 4 — Drug Repurposing Computational Screening). Direct match: no one is systematically screening approved drugs against islet-graft survival targets. This is a candidate for Project 2 expansion.
- **Beta Cell Regen × Health Equity** (Tier 1 area 6 — Epidemiological / Health Equity). Who is benefiting from β-cell regeneration trial access? Answerable from ClinicalTrials.gov + demographic overlays.
- **Gap #8 GWAS × CGM Technology** and **#13 Treg × CGM** — cross Tier 1 AI/ML (area 5) with tech accessibility.

Islet Transplant appears in 5 of the top 10 gaps, because its own publication base is only 242 papers (smallest domain by volume). This is partly a denominator effect — worth noting in any gap-derived narrative.

---

## Breaking News (Web Scan, Last 7 Days)

Filtered to items that are genuinely significant for this hub:

- **FDA approved first generic versions of dapagliflozin (2026-04-07).** Expands access to SGLT2 inhibitors; relevant to cost-effectiveness analyses and health-equity workstreams. *Evidence: regulatory action (Level 1-equivalent for the fact of approval; downstream clinical impact is projected, not measured).*
- **Karolinska/KTH stem-cell islet protocol published this week** (covered by ScienceDaily and Medical Xpress). Improved derivation method reverses diabetes in diabetic mice when transplanted into the anterior chamber of the eye. *Evidence level: preclinical (animal model). Per Doctrine: must be labeled "demonstrated in mouse model; human relevance unconfirmed" in any derivative output.* This aligns with PubMed hit [PMID 41997152](https://pubmed.ncbi.nlm.nih.gov/41997152/) already captured.
- **No FDA approval actions or Phase 3 readouts for the Vertex / Lilly / Novo Nordisk key-therapy set** in the past 7 days. The zimislecel 83%-insulin-independence figure circulating in news summaries is an older 2025 readout, not a new event.

No other items rising above the "routine" threshold this week.

---

## Recommended Actions

1. **Tracker update:** Record the two status transitions — **NCT06972472** (orforglipron T2D/obesity Phase 3) and **NCT05683990** (Diamyd at-risk T1D) — as `RECRUITING → ACTIVE_NOT_RECRUITING` in `Diabetes_Research_Tracker.xlsx` (last updated 2026-04-17).
2. **Synthesis priority:** Read and annotate **[PMID 41984238](https://pubmed.ncbi.nlm.nih.gov/41984238/)** (methodology critique of orforglipron analyses) *before* any next orforglipron-related output. This directly affects validation-tier assignment for any claim citing ACHIEVE trial efficacy.
3. **Tier 1 opportunity to scope:** The **Islet Transplant × Drug Repurposing** gap is a concrete Project 2 candidate. An artifact-sized deliverable: cross-reference the 242 islet-transplant papers against the islet_repurposing_drug_candidates.json catalog (already in Results/, dated 2026-04-03) to surface drugs with mechanistic rationale but no joint publication. Suggested script name: `project2_islet_rx_gap.py`.
4. **Review cross-domain papers now:** [PMID 42002040](https://pubmed.ncbi.nlm.nih.gov/42002040/) (KPDM — 3 domains) and [PMID 41986815](https://pubmed.ncbi.nlm.nih.gov/41986815/) (multi-tissue multi-omics T2D — Diabetologia) are the two highest-value new papers for Tier 1 synthesis this week.
5. **Optional rebase:** The session path changed — next `hub_monitor.py` run will again show 700+ spurious "new" files. If this is distracting, rebase `hub_monitor_state.json` once after confirming file integrity.
6. **No re-runs needed this cycle.** Literature gap data is 1 day old. All other inputs refreshed today. Next natural re-run of `project1_literature_gap_analysis.py` suggested in ~5–7 days.

---

## Evidence Notes (per RESEARCH_DOCTRINE.md)

- All clinical-trial status changes and PMIDs above are **Silver-tier** (primary registry record / indexed PubMed). Appropriate for tracking; not yet triple-validated.
- The 83% zimislecel efficacy figure cited in web summaries was NOT included in recommendations above because it is a secondhand restatement, not a fresh readout. Claim-level validation remains pending Vertex's formal 2026 regulatory submission.
- Preclinical (mouse) islet-cell results from Karolinska/KTH are labeled as such above.

---

*Automated run. No files were modified except creation of this report.*

## Sources

- [FDA Generic Dapagliflozin Approval 2026](https://www.mavenrs.com/blog/fda-generic-dapagliflozin-approval-2026-sglt2-inhibitor)
- [Novel Drug Approvals for 2026 (FDA)](https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026)
- [Karolinska/KTH stem-cell islet protocol — Medical Xpress](https://medicalxpress.com/news/2026-04-lab-grown-insulin-cells-reverse.html)
- [Karolinska/KTH stem-cell islet protocol — EurekAlert](https://www.eurekalert.org/news-releases/1123903)
- [Breakthrough T1D — News and Updates](https://www.breakthrought1d.org/news-and-updates/)
