# Diabetes Research Hub — Iteration Run Report

**Date:** 2026-07-15 (Wednesday)
**Mode:** Automated scheduled run (no Monday weekly PubMed sweep)

## Summary

Routine maintenance run with two substantive validations and a clean rebuild. No net-new papers; corpus unchanged at **285 papers (272 VETTED / 13 FLAGGED, 0 unvetted)** and **57 research paths**. All papers remain vetted, so no `vet_papers_batch` was needed.

## Work Queue Items Processed

### 1. validate_path — metformin → inflammation (reaffirmed VALIDATED)
Web recheck confirms the anti-inflammatory / NLRP3 mechanism. Added one confirming external citation:
- **PMID 31182921** — *Metformin Inhibits the NLRP3 Inflammasome via AMPK/mTOR-dependent Effects in Diabetic Cardiomyopathy* (Int J Biol Sci, 2019; preclinical).
- 2025–2026 NLRP3-in-diabetes reviews (e.g. PMC12395217) are consistent.
- **Caveat retained:** mechanism is preclinical + limited clinical (myeloid caspase-1 / IL-1β suppression in drug-naïve T2D); there is **no metformin RCT with an NLRP3 clinical endpoint**. Rating held at VALIDATED on independent external evidence, not on the weak corpus co-mention (PMID 35466661, a HCQ trial — flagged as an extraction artifact).
- external_pmids now: 30851273, 32398655, 34107285, **31182921**.

### 2. search_pubmed — Tegoprubart islet transplant (evidence tier UNCHANGED)
UChicago investigator-initiated islet-transplant trial (Witkowski) reports **all 12/12 participants insulin-independent**, mean recent HbA1c ~5.4%, no rejection, no de novo DSA, no nephrotoxicity. Presented at ATTD (Mar 2026) and ADA (Jun 2026).
- **STILL no peer-reviewed journal publication.** Sources remain conference presentations + press release (GlobeNewswire 2026-06-08), HCPLive, BioTuesdays, MedicalDialogues.
- Evidence tier unchanged (conference / press-release). Next check 2026-08-02.

### 3. search_pubmed — metformin NLRP3 systematic-review scan
Confirmed a real, growing supporting literature (mechanistic reviews + 2026 NLRP3-diabetes systematic review). Fed directly into item 1.

## Credibility Sweep (every run) — CLEAN
- 0 fabricated PMIDs (≥42,000,000) in scripts.
- 0 "zero SAEs" / "zero rejection" claims.
- "achieves" matches all legitimate and contextual: TTP399 tissue-selectivity (mechanism), LADA cost-effectiveness figure, ML macro-AUC, and the `verify_before_deploy.py` checker's own pattern list. No overstated preclinical/clinical language.

## Rebuild (Step 5)
Core Tufte rebuild stages run and confirmed **all [OK], RC=0**: clinical-trial dashboard, research dashboard, gap analysis, citations, GitHub Pages site, post-processing.

**Known issue:** the default full `run_quality_improvements.py` **hangs on the network PMID-verify stage** (`verify_pmids.py`) because the sandbox is throttled/blocked by the NCBI E-utilities endpoint. The full network verify is a **periodic** item (queue p7, last completed 2026-07-02) and is not part of the daily dashboard rebuild. Left in queue for a run where the endpoint responds.

## Git (Step 6) — BLOCKED, requires user
- Stale `.git/index.lock` (0-byte) **cannot be removed** from the OneDrive-mounted working tree (`Operation not permitted`). Confirmed again this run.
- Push auth also unresolved (`could not read Username for https://github.com`).
- All rebuilt dashboards + updated `agent_state.json` are saved and staged in the working tree. **User action:** delete `.git/index.lock` manually and commit/push. No unauthorized git operations were attempted.

## State
`agent_state.json` updated (run recorded, metformin path reaffirmed, Tegoprubart note refreshed, queue rotated) and validated as well-formed. Backup written: `agent_state.json.bak_2026-07-15`.
