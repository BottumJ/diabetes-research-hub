# Daily Iteration Report — 2026-05-18 (Monday)

## Run Summary
- **Day:** Monday — weekly PubMed search triggered.
- **Pipeline:** 41/41 quality-improvement steps [OK].
- **Credibility sweep:** clean (only a "curative" hit was inside `verify_before_deploy.py`'s own docstring, which lists patterns to flag).
- **Bug fixed:** `extract_corpus_data.py` had ~70 lines of orphan/duplicate code after its proper `__main__` block (lines 374–443). Truncated; `ast.parse` OK; extraction now yields 490 data points from 62 papers.

## Claims-Check Batch (12 papers)
Verified PMID + metadata-match via NCBI E-utilities for the next 12 lowest-PMID VETTED-but-unchecked papers. All are foundational/landmark citations:

| PMID | Year | Journal | Significance |
|---|---|---|---|
| 1611143 | 1992 | J Diabetes Complications | Cyclosporine T1D RCT |
| 1697648 | 1990 | Nature | GAD65 64K autoantigen (Baekkeskov) |
| 2189759 | 1990 | Diabetes | Glucokinase as glucose sensor (Matschinsky) |
| 3899825 | 1985 | Diabetologia | Original HOMA-IR/HOMA-B (Matthews) |
| 8366922 | 1993 | NEJM | DCCT primary outcome |
| 8439348 | 1993 | NEJM | IL-1 in disease (Dinarello) |
| 9521319 | 1998 | Nature | Dendritic cells & immunity (Banchereau & Steinman) |
| 9742976 | 1998 | Lancet | UKPDS 33 |
| 10415738 | 1999 | Ann NY Acad Sci | MMPs in diabetes |
| 10911004 | 2000 | NEJM | Edmonton Protocol (Shapiro) |
| 10919952 | 2000 | AJCN | Dietary supplementation metabolic basis |
| 11015619 | 2000 | Physiol Rev | Calcineurin (Rusnak & Mertz) |

Total claims-checked: **122 → 134 of 283 papers.**

## Monday PubMed Search (7 topics, last 7 days)
| Topic | New PMIDs |
|---|---|
| LADA latent autoimmune diabetes | 1 |
| islet transplant outcomes 2026 | 1 (off-topic — PRSS1 hereditary pancreatitis; not added) |
| NLRP3 inflammasome diabetic kidney | 0 |
| drug repurposing diabetes generic | 0 |
| oxidative stress diabetes combination | 11 (mostly nanotech/wound-healing; 2 added) |
| verapamil T1D beta cell | 0 |
| dapagliflozin colchicine combination | 0 |

**Added 3 papers as UNVETTED:**
- **PMID 42113684** (high) — "Distinct Interplay Between β-Cell Function and Insulin Resistance in LADA vs T2D" (Diabetes, May 2026, Buzzetti/Maddaloni group). Directly relevant to Gap #8 (LADA-specific evidence). Key finding: LADA shows reduced compensatory insulin secretion at matched insulin resistance vs T2D.
- **PMID 42108868** (med) — "Mitochondrial metabolism and dynamics in DKD" (Kidney Res Clin Pract, May 2026). Narrative review; supports oxidative_stress → nephropathy path.
- **PMID 42126264** (low) — "Novel SGLT2 inhibitors with endothelial-protective potential" (J Basic Clin Physiol Pharmacol, May 2026). Computational screen + cell experiments; tangential.

## Queue Movement
- Resolved: 2026-05-18 vet-papers batch (item 20).
- Added: 2026-05-19 vet-papers batch (next 12) + p3 vet-batch for the 3 new PMIDs.
- Unchanged: 9 unpushed commits (sandbox lacks GitHub auth — user push required).

## Next Run Priorities
1. **p2** — User to `git push` outstanding commits.
2. **p3** — Vet PMID 42113684 (and 42108868, 42126264). Could feed into Gap #8 audit due 2026-06-07.
3. **p3** — `fix_extraction_filter` (already verified in pipeline on 2026-05-16; may be closable).
4. **p4** — Gap #10 (SILVER → GOLD promotion review) due 2026-06-07.
5. **p4** — Gap #8 next monthly audit due 2026-06-07; new LADA paper above is a natural starting point.
