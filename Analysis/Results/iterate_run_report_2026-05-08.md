# Diabetes Research Hub — Iterate Run Report
**Date:** 2026-05-08 (Friday)
**Operator:** automated agent (scheduled task `diabetes-research-iterate`)
**Last successful run:** 2026-05-07
**Run status:** completed; commit/push still blocked by stale `.git/*.lock` files (sandbox EPERM)

## Queue items resolved (4)
1. **P3 — extract_evidence: PMID 40598585** (Beese SE et al, BMC Med 2025 NMA of T1D immunotherapies) — `extract_pmid_40598585.md` written.
2. **P4 — validate_path: GLP-1 RA → CV outcomes** — VALIDATED.
3. **P5 — search_pubmed: tegoprubart islet transplant T1D long-term** — only conference/press-release evidence; PARTIALLY_VALIDATED with explicit overclaiming caveat.
4. **P5 — search_pubmed: teplizumab long-term follow-up PROTECT extension** — PROTECT extension is observational with no published readout yet; PARTIALLY_VALIDATED.

## Key findings

### PMID 40598585 — BMC Med 2025 NMA (Beese SE, Price MJ, Tomlinson C, Sharma P, Harris IM, Adriano A)
60 RCTs, 4,597 patients, 32 intervention classes; 41 trials of 42 interventions in NMA. **Eleven** interventions showed statistically significantly higher C-peptide vs placebo at 12 months:

| # | Intervention | Already in our paths? |
|---|---|---|
| 1 | Autologous mesenchymal stem cells | partial coverage |
| 2 | Wharton's jelly-derived MSCs | partial coverage |
| 3 | Azathioprine | no |
| 4 | Interferon-alpha (5000 IU) | no |
| 5 | Autologous dendritic cells | no |
| 6 | Anti-TNF golimumab | NEW path added |
| 7 | Low-dose ATG | already validated |
| 8 | Teplizumab 3 mg 1-course (anti-CD3) | already validated |
| 9 | Baricitinib (JAK1/2) | NEW path added |
| 10 | Cyclosporin | historical, no active path |
| 11 | Teplizumab 9/11 mg 2-course | already validated |

**Authors' caveats:** "substantial heterogeneity present"; small-study evidence for MSCs/azathioprine/autologous DCs flagged as hypothesis-generating.

### Credibility correction — rituximab
The 2026-05-06 audit_notes entry stated rituximab "is among 11/42 interventions." The published abstract enumerates exactly 11 interventions and rituximab is **not** among them. Corrected today:
- Rituximab → T1D path remains **PARTIALLY_VALIDATED**, but rationale now rests only on Pescovitz NEJM 2009 (PMID 19940299) and Pescovitz Diabetes Care 2014 (PMID 24026563) — i.e. one course transiently delays beta-cell decline by ~8 months but does not arrest autoimmunity.
- BMC Med 2025 NMA is no longer cited as supporting evidence for rituximab.
- Confirmed the inflated claim never propagated to `Analysis/Scripts/*.py` or `Dashboards/*.html` (grep clean).

### GLP-1 RA → CV outcomes — VALIDATED
Strong, multi-trial evidence:
- LEADER (liraglutide, NEJM 2016, PMID 27295427): 3-pt MACE HR 0.87 (0.78–0.97)
- SUSTAIN-6 (s.c. semaglutide, NEJM 2016, PMID 27633186): 3-pt MACE HR 0.74 (0.58–0.95)
- PIONEER 6 (oral semaglutide, NEJM 2019, PMID 31185157): MACE HR 0.79 (0.57–1.11), met noninferiority
- 2024 meta-analysis (PMID 38953365): 24 RCTs, ~94k patients, MACE reduction in patients with and without diabetes
- Class effect supported across 2024–2025 NMAs

Caveats: trial-level heterogeneity (REWIND had 31.5% baseline CVD vs ~70% elsewhere); dosing/follow-up duration vary.

### Tegoprubart (anti-CD40L) + islet transplant — PARTIALLY_VALIDATED with explicit caveat
ATTD 2025 conference + Eledon press releases + Transplantation 2025 abstract 04-3. Single-center investigator-initiated trial at UChicago (n=12, 10 evaluable >4 weeks; reported insulin-independent with HbA1c <6.0%; mean ~5.35%). **No peer-reviewed publication yet.** The "no rejection episodes / no de novo DSAs / no SAEs" framing aligns directly with our doctrine red flag for overclaiming preclinical/early-phase results. Conference data added with caveats; **must not** be cited as VETTED in dashboards. Re-audit when peer-reviewed publication appears.

### Teplizumab PROTECT extension — PARTIALLY_VALIDATED
- PROTECT primary results: PMID 37861217 (NEJM 2023). Met primary endpoint (slowed C-peptide AUC decline at week 78 in 8–17yo with stage 3 T1D).
- PROTECT extension (NCT04598893): observational long-term safety/clinical follow-up; no published readout yet.
- TN-10 extension at ADA 2025 (poster 840-P): not peer-reviewed.
- Sanofi sNDA accepted Oct 2025 for stage 3 T1D under FDA Priority Voucher pilot — regulatory milestone only.
- 2025 Frontiers Endocrinol review: PMID 40357199.

## New paths added (both NMA-evidence-only, need primary trial PMIDs)
- `golimumab_t1d_beta_cell` — PARTIALLY_VALIDATED via PMID 40598585 (T1DAL trial PMID still needed)
- `baricitinib_t1d_beta_cell` — PARTIALLY_VALIDATED via PMID 40598585 (BANDIT trial PMID still needed)

## New queue items added (5)
- P4: extract BANDIT trial primary publication (baricitinib phase 2 stage 3 T1D)
- P4: extract T1DAL trial primary publication (golimumab anti-TNF stage 3 T1D)
- P4: re-grep all build_*.py for any "rituximab" + "11/42" wording (precaution; today's pass clean)
- P5: tegoprubart peer-reviewed publication recheck — next 2026-08-08
- P5: PROTECT extension peer-reviewed readout recheck — next 2026-09-01

## Pipeline status
- `run_quality_improvements.py`: 41/41 [OK]
- Credibility sweep: clean (no fabricated PMIDs >42M; no unflagged "zero SAEs"/"curative" claims in scripts)

## Outstanding blockers
- **`.git/HEAD.lock`, `.git/index.lock`, `.git/objects/maintenance.lock`** (0-byte, dated 2026-05-05) — `rm -f` returns Operation not permitted on the OneDrive mount; commits/pushes since 2026-05-05 still pending. **User action required:** from PowerShell on host: `cd $HOME\OneDrive\Diabetes_Research; Remove-Item -Force .git\HEAD.lock, .git\index.lock, .git\objects\maintenance.lock; git add -A; git commit -m "Catch-up commit"; git push`.

## Files touched
- `Analysis/Results/agent_state.json` (validated_paths +5; audit_notes +1; queue updated; run_history +1)
- `Analysis/Results/extract_pmid_40598585.md` (new)
- `Analysis/Results/iterate_run_report_2026-05-08.md` (this file)
- All dashboards/JSON via `run_quality_improvements.py`

## Sources cited (peer-reviewed PMIDs only)
- Beese SE et al. BMC Med 2025: PMID 40598585
- LEADER (Marso et al, NEJM 2016): PMID 27295427
- SUSTAIN-6 (Marso et al, NEJM 2016): PMID 27633186
- PIONEER 6 (Husain et al, NEJM 2019): PMID 31185157
- GLP-1 RA MACE meta-analysis 2024: PMID 38953365
- PROTECT primary (Ramos et al, NEJM 2023): PMID 37861217
- Frontiers Endocrinol 2025 teplizumab review (Saleem & Khan): PMID 40357199
- Pescovitz NEJM 2009 (rituximab T1D): PMID 19940299
- Pescovitz Diabetes Care 2014 (2-yr follow-up): PMID 24026563
