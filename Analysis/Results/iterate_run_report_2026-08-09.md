# Diabetes Research Hub — Iteration Run Report
**Date:** 2026-08-09 (Sunday) · Automated agent run · Not Monday → no weekly new-paper sweep

## Corpus status
- **Papers:** 286 total — 273 VETTED / 13 FLAGGED / **0 UNVETTED**
- **Research paths:** 57 · **Gaps:** 15 · **Work queue:** 40 items

## Work queue items processed (4)

**1. Gap #5 audit (SILVER → SILVER retained)**
Islet transplant × systematic *generic*-drug repurposing. Direct intersection (a systematic generic-drug repurposing screen with an islet-transplant primary endpoint) still ~0. Web search surfaced only adjacent, non-qualifying work: rosiglitazone+rapamycin synergy (older mechanistic; drug-eluting islets TLR4/NF-κB, PMID 29309990, 2018), BCG immunomodulation (not a screen), and tegoprubart (a biologic anti-CD40L, not generic repurposing). No promotion. `last_audited` → 2026-08-09.

**2. Gap #11 audit (GOLD → GOLD retained)**
CAR-Treg × prescribed personalized-nutrition protocol as a single study. Still ~0 integrated studies. Update: the diet/gut-microbiome/T1D review previously logged as PMC12818812 is now PubMed-indexed as **PMID 41536244** (Gut Microbes 2026, doi 10.1080/19490976.2026.2614039) — but it is a review, not an integrated CAR-Treg+diet study. New adjacent CAR-T-in-T1D review PMC12661798. High-SCFA-diet-protects-NOD evidence is diet-only (no CAR-Treg arm). Signals remain **parallel, not integrated**. Promotion still requires ≥1 preclinical in-vivo paper testing CAR-Treg + defined-diet/SCFA co-intervention. `last_audited` → 2026-08-09.

**3. NLRP3 → ferroptosis PMID re-verification (RESOLVED-PENDING)**
MDPI *IJMS* 27(10):4257 (DOI 10.3390/ijms27104257, "NLRP3 Inflammasome Inhibition Attenuates Diabetic Kidney Injury via Suppression of Ferroptosis," Tian et al., STZ NLRP3-KO mice + HK-2 cells, preclinical, pub 2026-05-10) **re-confirmed REAL via DOI/MDPI** but **still not PubMed-indexed** (search returns mdpi.com + unrelated PMC only; no pubmed.ncbi.nlm.nih.gov record). Remains **UNVETTED_NO_PMID (pmid=PENDING, not fabricated)**. Adjacent indexed support now exists: PMC12206412 (NLRP3 pyroptosis in diabetic nephropathy review) + PMC11906378 (ferroptosis/innate-immune crosstalk DKD). Next re-verify 2026-09-01.

**4. Path validation — `teplizumab_long_term_followup` (PARTIALLY_VALIDATED)**
Mid-term **VALIDATED**: PROTECT primary (NEJMoa2308743, NEJM 2023, n~300 peds 8–17, 2:1) showed significant preservation of stimulated C-peptide at week 78 vs placebo; TN-10 prevention (Sci Transl Med 2021) supports durability of the anti-CD3 effect. Long-term durability **PENDING**: PROTECT Extension (NCT04598893) is observational (q6mo through Month 42; 60mo combined) with **no peer-reviewed long-term readout published** as of 2026-08-09.

## Credibility sweep — CLEAN
- Max PMID cited in `.py`: **41921761** (< 42,000,000 fabrication threshold); no bare 42M–43M numbers.
- No "zero SAEs / zero rejection / no DSA" claims.
- All `cure`/`curative`/`achieves` hits are legitimate: category labels ("Cure – Stem Cell"), cost-math, mechanism copy, or caveated BRONZE preclinical claims ("human translation uncertain").

## Pipeline rebuild
- **38/38 offline scripts `[OK]`, 0 failures** (24 in first pass + 14 in second pass).
- Network-bound scripts **skipped**: `pmidverify`, `pmidtracker`, `ingest` — live PubMed API rate-limited/stalled in sandbox (non-destructive; stalled after 214 PMIDs verified).

## Git
- Commit **5215c56** succeeded in sandbox (21 files; locks cleared via rename trick).
- **PUSH BLOCKED**: `could not read Username for 'https://github.com'` (no GitHub auth in sandbox). **Now 75 commits ahead of origin/main.**
- **USER ACTION:** from local PowerShell at `C:\Users\justi\OneDrive\Diabetes_Research`, run `git push` (and, if it complains, `Remove-Item .git\*.lock` first). All research changes are persisted to working files on disk regardless of git.

## Next run priorities
- Gap #3 / #6 (GOLD) monthly audits due ~2026-08-16.
- BANDIT / DAPAN-DIA / PROTECT-extension / SAB-142 / Tegoprubart publication watches (next ~2026-09-01/02).
- NLRP3→ferroptosis PubMed-indexing re-verify 2026-09-01.
