# Diabetes Research Hub — Monitor Report
**Run date:** 2026-10-03 (automated review; no existing files modified)

**Headline:** No new pipeline data since 2026-10-02. All key outputs were generated 2026-10-02; no 2026-10-03 snapshot exists yet. Clinical-trial diff 10-01 → 10-02 is zero real changes (906 trials; the only 32 "differences" are reordered `intervention_types` strings). [Certain — verified by programmatic diff of the two snapshots.] Nothing urgent to escalate.

## File System Status
| File | Last modified | Status |
|---|---|---|
| hub_monitor_report.md | 2026-10-02 | Fresh (1 day) |
| clinical_trials_latest.json | 2026-10-02 | Fresh; byte-identical to snapshot_2026-10-02 |
| pubmed_recent_latest.json | 2026-10-02 | Fresh; byte-identical to snapshot_2026-10-02 |
| literature_gap_data.json / literature_gap_report.md | 2026-10-02 | Fresh |
| Diabetes_Research_Tracker.xlsx | 2026-07-17 | **STALE — 78 days** |
| hub_monitor flag | — | 834 live result files >14 days old (mostly audit/cache JSONs; not all need refresh) |

## Clinical Trial Changes
- 906 unique trials; new 0, removed 0, status changes 0, new results 0 (10-01 → 10-02).
- 143 Phase 3 trials; 282 RECRUITING; 10 Phase 3 RECRUITING trials from Vertex/Lilly/Novo/Sana.
- Vertex VX-880 (zimislecel) Phase 3: NCT06832410 and NCT04786262 both RECRUITING. VX-264 (NCT05791201) ACTIVE_NOT_RECRUITING.
- Registry results posted recently (unreviewed = BRONZE until tied to a verified paper): NCT06109311 (Lilly orforglipron, 2026-10-01); NCT06045221 (orforglipron vs semaglutide, 2026-09-15); NCT06370715 (Lilly LY900014, 09-28); NCT05872620 (orforglipron obesity, 09-04).
- Open carry-over: NCT05757713 (Sanofi teplizumab pediatric) not confirmed in registry pull.

## PubMed Highlights (156 papers, 17 domains, 30-day lookback)
Cross-domain papers (highest value):
- 42815506 — Lancet, orforglipron CV safety vs insulin glargine in T2D (T2D GLP-1 × orforglipron). Highest-value item; verify HR/abstract before any claim.
- 42810372 — Lancet, retatrutide TRIUMPH-2 in obesity + T2D; 42814954 — NEJM, retatrutide in obesity (note: appear as therapy hits).
- 42810355 / 42810353 — Lancet Diabetes Endocrinol, petrelintide ZUPREME-1 + commentary (Amylin × petrelintide).
- 42822398 — 10-year bariatric surgery remission extension RCT (T2D GLP-1 × Remission).
- 42822623 — automated anti-IA2 ELISA (Biomarker × LADA) — relevant to LADA focus.
- 42720752 (Diabetologia, teplizumab β-cell preservation in stage 3 children), 42767751 (SIRENA teplizumab protocol, BMJ Open), 42520060 (HLH after teplizumab, case report — safety signal, low evidence).
- Amylin/obesity reviews: 42803913, 42812898, 42808923, 42763732.
Key-therapy volumes (30d): zimislecel 0; orforglipron 15; retatrutide 12; CagriSema 3; teplizumab 7; baricitinib 2; finerenone 37. Domain activity is flat (all domains capped at retmax 10, so volume trends are not measurable from this script — see actions).

## Gap Analysis Summary
Top five (22 of 435 pairs tie at 100.0, so ranking is tie order only): Beta Cell Regen × Health Equity (0 joint), Insulin Resistance × Islet Transplant (1), Islet Transplant × GWAS (0), Islet Transplant × Personalized Nutr (0), Islet Transplant × Drug Repurposing (0).
Doctrine alignment: Tier 1 includes Multi-Omics Biomarker Integration and Literature Synthesis & Gap Analysis. Gap Analysis is itself Tier 1, so the saturated score is a method defect, not just noise. Many top pairs involve small domains (Islet Transplant 255 pubs, LADA 615), so keyword/terminology mismatch is plausible. [Likely]

## Breaking News (web, last ~7 days)
Two searches returned thin/low-quality results; no new Phase 3 readout or FDA action surfaced beyond items already tracked (Kerendia T1D-CKD, Onswik/efsitora, Beta Bionics Mint). [Guessing — search snippets only; not verified against primary sources.]

## Recommended Actions
1. Update Diabetes_Research_Tracker.xlsx (78 days stale) with NCT06109311, NCT06045221, TRIUMPH-2 (42810372), ZUPREME-1 (42810355).
2. Read abstract of PMID 42815506 and verify numbers/PMID before adding to Research_Findings_Summary.md (Evidence level: unreviewed until verified).
3. Manually check NCT05757713 on ClinicalTrials.gov.
4. Replace saturated gap score with observed/expected ratio + CI to break the 22-way tie.
5. Raise `domain_retmax` in baseline_pubmed_alerts.py if you want real publication-volume trends.
6. Run `python baseline_clinical_trials.py` and `python baseline_pubmed_alerts.py` to produce a 2026-10-03 snapshot (none today).
