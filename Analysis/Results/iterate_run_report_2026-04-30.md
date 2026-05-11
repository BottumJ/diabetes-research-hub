# Iterate Run Report — 2026-04-30

## Summary
Vetted 12 papers (11 VETTED, 1 FLAGGED off-topic). Validated 1 research path. Logged 2 PubMed topic-checks. Credibility sweep clean. Pipeline 41/41 OK. Commit `e6e7bb2` made locally; push blocked (no credentials in sandbox) — user will need to push from their machine.

## Papers vetted (12)
| PMID | Year | Status | Note |
|---|---|---|---|
| 36109639 | 2022 | VETTED | Anti-CD19 CAR-T SLE (Nat Med) — autoimmune-platform precedent |
| 36109742 | 2022 | VETTED | Diabetes RCT racial/ethnic enrollment trends (BMC Med) — equity |
| 36113507 | 2022 | VETTED | Global T1D incidence/prevalence/mortality 2021 (Lancet Diab Endo) — canonical epi |
| 36288281 | 2022 | VETTED | CRISPR CAR19 universal T cells (Sci Transl Med) — platform tech |
| 36449148 | 2022 | VETTED | Dorzagliatin First Approval (Drugs) — core GKA reference |
| 36455116 | 2022 | VETTED | Computational nutrition optimization for T2D (Diabetes Care) |
| 36474045 | 2022 | VETTED | CAD risk variants (Nat Genet) — peripheral / PRS-adjacent |
| 37016949 | 2023 | VETTED | Minoritized youth in T1D RCTs (J Pediatr Psychol) — equity |
| 37105208 | 2023 | VETTED | Primary graft function ↔ 5y islet outcomes (Lancet Diab Endo) |
| 37122431 | 2023 | VETTED | Semaglutide editorial (World J Diabetes) — framing only |
| **37133585** | 2023 | **FLAGGED** | Trifluridine-Tipiracil + Bevacizumab in CRC (NEJM) — **off-topic oncology** |
| 37202589 | 2023 | VETTED | Teplizumab approval implications (Nat Rev Endocrinol) — core |

Status counts: 215 VETTED / 12 FLAGGED / 43 UNVETTED (270 total).

## Path validation
**Treg_expansion -> T1D → PARTIALLY_VALIDATED**
- Primary external evidence: T-Rex Phase 2 RCT (PMID 38718135, Sci Transl Med 2024). 110 children/adolescents new-onset T1D randomized to high-dose, low-dose, or placebo polyclonal autologous expanded Tregs. Tregs were SAFE but DID NOT preserve residual β-cell function over 12 months at either dose.
- Important nuance from the trial: lower fold-expansion Tregs and an associated gene signature correlated with better C-peptide preservation, suggesting Treg quality (not infused dose) may be the limiting factor.
- Continuing development: PolTREG PTG-007 received positive EMA Paediatric Investigation Plan opinion (May 2025); engineered/antigen-specific approaches (GNTI-122, Sonoma/Abata CAR-Treg) still in early development.
- External PMIDs: 38718135, 34324441, 26606968.

## PubMed topic-checks
**NLRP3 inhibitors in DKD** — no human DKD trial of selnoflast, dapansutrile, or MCC950 identified. MCC950 clinical development was terminated due to liver injury in a Phase 1 RA trial. Critically, in an interventional model of established DKD, MCC950 showed adverse renal effects (PMID 35048962) — caveat for any synthesis. Dapansutrile remains generally safe across 6 trials but no DKD-specific program. Selnoflast is in Parkinson Phase 1b. Recheck Q3 2026.

**SAB-142 (IDS 2026)** — Phase 1 HUMAN trial data presented April 22, 2026 at IDS Brisbane: C-peptide preservation in 3 of 4 participants ("super-responder" profile) correlated with CD4+ Tconv exhaustion and improved CGM time-in-range vs baseline. n=4, no controls — conference disclosure only, no peer-reviewed publication yet. SAFEGUARD Phase 2b trial NCT07187531 began dosing — 159 newly-diagnosed stage-3 T1D patients across two active doses + placebo, primary endpoint 1-yr C-peptide, expected H2 2027 readout. Track as ENROLLING; defer firm efficacy claims until SAFEGUARD.

## Credibility sweep
- No fabricated PMIDs above 42M.
- No "zero SAEs / zero rejection" claims.
- No "curative / achieves cure / achieves remission" claims outside the verify_before_deploy.py detector itself.

## Pipeline rebuild
`run_quality_improvements.py`: all 41 improvements [OK].

## Operational notes
- Stale .git/index.lock (zero-byte, dated 2026-04-24) cannot be deleted from the Linux sandbox (`Operation not permitted` — likely OneDrive-side lock). Workaround: `mv` rather than `rm` succeeds and unblocks git operations. Workaround applied during this run; commit succeeded. **Recommend the user delete the lock files manually from Windows so future automated runs do not depend on the workaround.**
- `git push` failed in sandbox (`could not read Username` — no credentials). Local commit `e6e7bb2` is on `main`, ahead of `origin/main` by 3 commits. The user will need to push from their machine: `git push origin main`.

## Queue (post-run, top items)
1. `ingest_papers` — PMIDs 41935855, 41994768 (priority 2)
2. `extraction_filter_review` — exclude oncology/CRC papers like 35437333 (priority 3)
3. `validate_path` — rituximab → T1D (priority 3)
4. `vet_papers_batch` — next 12 of remaining 43 UNVETTED (priority 3)
5. `audit_gap` Gap 1, `audit_gap` Gap 9 (priority 4)
6. `search_pubmed` — Abata ABA-201, dapansutrile DKD (priority 4)
7. `check_combination` — SAFEGUARD enrollment milestones (priority 4)
