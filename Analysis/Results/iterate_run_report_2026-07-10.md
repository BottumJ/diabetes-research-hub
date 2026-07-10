# Diabetes Research Hub — Automated Iteration Report

**Date:** 2026-07-10 (Friday) · **Mode:** autonomous scheduled run · No Monday weekly literature sweep.

## Work completed this run

### 1. Credibility sweep (Step 4) — CLEAN
- 0 fabricated PMIDs (numeric) in `Analysis/Scripts/*.py`.
- No "zero SAEs" / "zero rejection" language.
- "achieves" hits reviewed and benign (TTP399 tissue-selectivity design claim; diagnostic-model cost-effectiveness ratio; ML macro-AUC metric; verifier keyword list).

### 2. Gap audits — 2 overdue gaps cleared (both 40 days stale)
The visible queue text was stale; recomputing due-dates from `last_audited` fields showed **Gap #4** and **Gap #12** (both last audited 2026-05-31) as the genuinely overdue items, not the queue's top entries. Retargeted to those.

**Gap #4 — Islet Transplant x Personalized Nutrition (SILVER retained).**
No RCT combining islet transplant with a personalized-nutrition intervention as a single protocol. Adjacent/parallel evidence only: RSC *Food & Function* 2026 personalized-nutrition RCT review (DOI 10.1039/D5FO02969D); gluten-free diet in multiple-islet-autoantibody-positive persons (PMC12146266); established post-transplant nutrition considerations (PMID 33002260; long-term diet/anthropometry/exercise adherence PMID 23769100). Direct intersection remains empty. No promotion.

**Gap #12 — Treg/CAR-T x Diabetic Neuropathy (SILVER retained).**
Still no Treg/CAR-T intervention trial in DPN. New adjacent cell-therapy trial logged as a watch item: **NCT07183761** (umbilical-cord MSC RCT in moderate-to-severe DPN; started Oct 2025, primary completion Apr 2028) — cell therapy but **not** Treg. Treg biology reviews continue (Cell 2025 S0092-8674(25)01370-4; PMC12615433). Biological plausibility strengthening; no direct intervention. No promotion.

### 3. Path re-validation — verapamil -> T1D (PARTIALLY_VALIDATED retained, now leaning cautious)
Stalest dated PARTIAL path (last validated 2026-04-22). Re-checked for a Ver-A-T1D 24-month / Ver-A-Long extension readout — none yet published (trial continues to 24 mo then a 3-year open-label extension; the Pieber group is planning an RCT meta-analysis and a larger/longer repeat).

Net evidence picture is slightly more cautious than before: the earliest small RCTs (Ovalle 2018, PMID 29988125; Forlenza pediatric 2023) and a 112-patient 2023 meta-analysis were positive for 1-year C-peptide, but the largest, most rigorous adult RCT — **Ver-A-T1D (n=136, 21 sites)** — **missed** its primary 2h-MMTT C-peptide AUC endpoint at 3/6/9/12 months (EASD Sep 2025; only a non-significant favorable trend). Status held PARTIALLY_VALIDATED. The peer-reviewed *Diabetologia* primary DOI remains **UNVERIFIED** (per 2026-07-02 note; not directly hit this run).

### 4. PMID verification — 262/262 verified against live PubMed API
`run_quality_improvements.py` completed **41/41 stages [OK]**.

### 5. Doctrine reconfirmation (already-known, not novel)
The final grep surfaced PMIDs >=42M in the non-published scratch file `_audit_2026-06-02_gap_2_3_6.json`. Live NCBI esummary confirmed **42220535** (Front Immunol 2026), **42203900** (Bone Marrow Transplant 2026), **42218679** (Magyar Onkologia 2026) are **real**. This restates prior doctrine notes (`pmid_threshold_2026-05-04`, `pmid_range_2026`): the ">42M PMID = fabricated" heuristic is stale as of 2026. The threshold is **not hardcoded** in any script, so no code fix is needed; the operative fabrication gate is live-API verification. These IDs are referenced by no live script/dashboard/doc — **do not delete them**.

## State changes
- `run_history`: +1 (now 87 entries)
- `gaps[4].last_audited` / `gaps[12].last_audited` -> 2026-07-10; audit_history appended; Gap #12 watch item NCT07183761 added
- `paths['verapamil -> T1D'].validated_date` -> 2026-07-10; validation_notes refreshed
- `doctrine_notes`: +`pmid_range_reconfirm_2026_07_10`
- `work_queue`: removed 1 stale Gap #14 duplicate + refreshed Gap #4 / Gap #12 / verapamil pointers (30 -> 31)

## Nothing changed externally
No new confirmatory or contradictory evidence altered any tier or path status this run. The only material shift is the more cautious framing of verapamil->T1D following the negative Ver-A-T1D primary readout.
