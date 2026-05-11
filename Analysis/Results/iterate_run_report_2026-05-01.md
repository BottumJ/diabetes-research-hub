# Iteration Run Report — 2026-05-01

## Summary
Vetted 12 papers, validated 1 research path (rituximab → T1D), audited 1 EXPLORATORY gap (Gap 9 GKA × LADA), tracked dapansutrile DKD development.

## Work Queue Items Completed

### 1. vet_papers_batch (12 papers — all VETTED)
| PMID | Title | Journal | Year | Status |
|------|-------|---------|------|--------|
| 37217319 | Disparities in Diabetes Care: Rural vs Urban | Ann Fam Med | 2023 | VETTED |
| 37223016 | Glucokinase activators: systematic review and meta-analysis | Front Endocrinol | 2023 | VETTED |
| 37351171 | Metabolomics + peptidomics in diabetic kidney disease | Theranostics | 2023 | VETTED |
| 37356445 | Diabetes disparities by race/ethnicity in USA | Lancet Diabetes Endocrinol | 2023 | VETTED |
| 37356446 | Global burden of diabetes 1990–2021, projections to 2050 (GBD) | Lancet | 2023 | VETTED |
| 37356449 | Measuring global burden of diabetes (commentary) | Lancet | 2023 | VETTED |
| 37359825 | Multi-modal islet + pancreas transplant w/ CNI-sparing | Transpl Int | 2023 | VETTED |
| 37366315 | Retatrutide phase 2 trial for obesity | NEJM | 2023 | VETTED |
| 37385277 | Optimal semaglutide dosing in T2D (commentary) | Lancet | 2023 | VETTED |
| 37428296 | Worldwide LADA prevalence systematic review | Endocrine | 2023 | VETTED |
| 37748491 | CAR T-cell therapy in autoimmune diseases | Lancet | 2023 | VETTED |
| 37845117 | Residual cardiovascular risk: when to treat | Eur J Intern Med | 2024 | VETTED |

All 12 PMIDs verified in `paper_library/index.json` with full PubMed metadata. All on-topic for diabetes corpus. No fulltext available; abstracts present except 2 commentaries (37356449, 37385277) where empty abstract is normal/expected. No red flags (no implausible numbers, no off-topic content like the previous CRC papers that were FLAGGED).

### 2. validate_path: rituximab → T1D — **PARTIALLY_VALIDATED**

**Evidence found:**
- **Pescovitz et al., NEJM 2009 (PMID 19940299):** Randomized double-blind RCT, n=87 patients aged 8–40 with newly diagnosed T1D. Four-dose rituximab (days 1, 8, 15, 22) vs placebo. **At 1 year:** mean C-peptide AUC significantly higher in rituximab group; lower HbA1c; lower insulin requirements. CD19+ B cells depleted, recovered to 69% of baseline by 12 months.
- **Pescovitz et al., Diabetes Care 2014 (PMID 24026563):** 30-month extension. **Rate of C-peptide decline became parallel to placebo, just shifted by ~8.2 months.** Over 30 months, AUC, insulin dose, and HbA1c were similar across groups. OR for loss of C-peptide to <0.2 nmol/L = 0.565 (P=0.064).

**Conclusion:** Rituximab DELAYS but does not ARREST beta-cell loss in recent-onset T1D. The underlying autoimmunity is not fundamentally altered. PARTIALLY_VALIDATED — real but transient effect.

**Caveat for downstream uses:** Any dashboard claim involving rituximab + T1D must reflect the time-limited nature of the effect; do not present as disease-modifying.

### 3. audit_gap: Gap 9 — GKA × LADA (EXPLORATORY → unchanged)

Searches performed:
- "glucokinase activator dorzagliatin LADA latent autoimmune diabetes adults clinical trial 2026"
- "glucokinase LADA OR latent autoimmune diabetes 2025 2026 clinical study"

**Finding:** No new GKA-in-LADA human evidence. Available GKA trials (DAWN, SEED) all in T2D or GCK-MODY. LADA literature focuses on autoantibody testing, insulin therapy, and disease progression — not GKA mechanism. Gap remains EXPLORATORY (corpus_evidence_points = 0).

**Hallucination note:** One web-search snippet claimed "dorzagliatin has gained approval for treating type 1 diabetes mellitus." This contradicts known regulatory status (dorzagliatin approved by China NMPA 2022 for T2D only) and was NOT adopted into the corpus. Flagged as model hallucination.

### 4. search_pubmed: dapansutrile DKD phase 2

**Finding:** No DKD-specific dapansutrile Phase 2 trial registered. However, **DAPAN-DIA** (Olatec, Basel, Switzerland) is an active randomized double-blind placebo-controlled multi-center Phase 2 enrolling ~300 T2D patients with diabetes-related complications, treated for 6 months. First patient enrolled 2024 per Olatec PR. This is the closest analog and may yield kidney-relevant subgroup data. Recheck Q3 2026 for DKD-specific registrations.

## Credibility Sweep
- Fabricated PMIDs (>42M): **0 found** in Scripts/
- "zero SAEs" / "zero rejection" claims: **0 found**
- "achieves" / "curative" preclinical overstatements: **0 found**

## Pipeline Rebuild
`python3 Analysis/Scripts/run_quality_improvements.py` — **all 41 [OK]**.

## State Updates
- 12 papers moved UNVETTED → VETTED (now 227 vetted, 31 unvetted, 12 flagged)
- `paths['rituximab -> T1D']`: status set to PARTIALLY_VALIDATED with external PMIDs and notes
- `validated_paths['rituximab -> T1D']`: full evidence record added
- `gaps['9'].last_audited` → 2026-05-01 with audit_history entry
- `topic_checks['dapansutrile_dkd']`: snapshot recorded
- Work queue reprioritized: completed items removed; new items added (next 12 unvetted batch, rituximab → beta_cell + nephropathy validation)

## Next Run Priorities (top 5)
1. **[pri 2]** ingest_papers: PMIDs 41935855, 41994768
2. **[pri 3]** extraction_filter_review: tighten extract_corpus_data.py topic filter
3. **[pri 3]** vet_papers_batch: next 12 UNVETTED PMIDs
4. **[pri 4]** audit_gap: Gap 1
5. **[pri 4]** validate_path: rituximab → beta_cell (adjacent to today's work)
