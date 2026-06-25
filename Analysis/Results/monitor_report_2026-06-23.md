# Diabetes Research Hub — Monitor Review

**Run date:** 2026-06-23 (automated, no user present)
**Previous monitor report:** 2026-06-22
**Scope:** Read-only review of latest script outputs + snapshot diffs + web check. No files modified.

---

## Bottom line (what's actionable)

1. **One Tier-1 therapy moved status:** NCT05594563 (TADPOL, polyamines in T1D) flipped RECRUITING → ACTIVE_NOT_RECRUITING. Minor — enrollment closed, not a result.
2. **Six new trials ingested**, but only **one is forward-looking and Tier-1 relevant**: NCT07659574 — a *Phase 3* T2D trial of UBT251 (United Bio-Technology), a new triple-agonist-class entrant worth adding to the watch list. The other five are completed studies or low-N device/lifestyle pilots.
3. **The one real maintenance item is unchanged from yesterday:** `literature_gap_data.json` is now **64 days stale (2026-04-20)**. The gap *report* is re-rendered daily off old data. Re-run the gap analysis or stop trusting the rendered ranks as current.
4. **No breaking news in the last 7 days.** Web items that surface (Tzield Stage-3 expansion, retatrutide TRIUMPH-1, weekly icodec) are weeks-to-months old and already in the corpus.

---

## File System Status

All four expected script outputs are present and today-fresh:

| File | Status |
|------|--------|
| `clinical_trials_latest.json` | Fresh — 2026-06-23 07:05 (**827 trials**) |
| `pubmed_recent_latest.json` | Fresh — 2026-06-23 07:06 (**173 papers**, 30-day window, 16 domains) |
| `hub_monitor_report.md` | Fresh — 2026-06-23 07:06 |
| `literature_gap_report.md` | Re-rendered 2026-06-22 08:10 |
| `literature_gap_data.json` | **STALE — 2026-04-20 (64 days).** Underlying gap matrix not recomputed; only the `.md` is re-rendered. |

Hub monitor flagged **740 result files older than 14 days**. Almost all are dated daily snapshots (expected archive growth, not a problem). The one stale file that actually feeds a live deliverable is `literature_gap_data.json`.

Today's scan vs. 2026-06-22: 3 new files (today's two snapshots + yesterday's report), 49 modified (dashboards re-rendered in the 06-22 08:10 batch), 0 removed.

---

## Clinical Trial Changes

**Day-over-day diff (2026-06-22 → 2026-06-23): 6 new, 0 removed, 1 status change, 0 new results posted.** [Certain — from snapshot diff]

**Status change:**

- **NCT05594563 — TADPOL** (TArgeting T1D Using POLyamines): RECRUITING → ACTIVE_NOT_RECRUITING. Enrollment closed; no results yet. Low-urgency, but it sits in the T1D immunomodulation space we track.

**New trials (6) — only one is forward-looking + on-thesis:**

| NCT | Phase / Status | Note |
|-----|----------------|------|
| **NCT07659574** | **PHASE3 / NOT_YET_RECRUITING** | UBT251 (United Bio-Technology) in T2D, UNIGUIDE-1, n=360. New triple-agonist-class candidate — **add to watch list.** |
| NCT07465926 | N/A / COMPLETED | Large (n≈451k) real-world GLP-1+SGLT2 early-combination study in CKM stage 2–3. Worth a read for combination-therapy evidence. |
| NCT07507708 | NA / RECRUITING | Predictive closed-loop insulin pilot, n=20. Low priority. |
| NCT07661381 | NA / NOT_YET_RECRUITING | AI lifestyle coach + CGM in T2D, n=160. Low priority. |
| NCT00248352 | NA / COMPLETED | 2005 case-managed-care CAD/diabetes study (back-fill). |
| NCT04334109 | NA / COMPLETED | Family vs. standard DSMES study (back-fill). |

**Snapshot totals:** 827 unique trials — 263 RECRUITING, 145 NOT_YET_RECRUITING, 303 COMPLETED-with-results, 125 PHASE3 (+15 PHASE2/3). Top sponsors unchanged: Eli Lilly (29), Novo Nordisk (27).

**Tier-1 Phase-3 watch list — all stable, no movement** [Certain — from latest snapshot]:

| NCT | Sponsor | Therapy / Focus |
|-----|---------|-----------------|
| NCT04786262 / NCT06832410 | Vertex | VX-880 (zimislecel) islet cell therapy, T1D |
| NCT07222137 / NCT07222332 | Eli Lilly | Baricitinib — delay Stage 3 / preserve beta-cell function, T1D |
| NCT07076199 | Novo Nordisk | Weekly insulin icodec |
| NCT07564414 | Novo Nordisk | CagriSema dose-ranging |
| NCT06739122 | Eli Lilly | Dulaglutide in pediatrics |

No new results posted in the last 7 days across any tracked Phase-3 program.

---

## PubMed Highlights

173 unique papers, 30-day lookback. Snapshot diff vs. 06-22: **43 new papers, 42 dropped** (rolling window).

**Cross-domain papers (highest value, 5 total; 3 are new today):** [Certain]

- **[42327726]** scFv-based biologics in diabetes: therapeutic potential to clinical prospects — *T1D Immunotherapy × Key Therapy: teplizumab* **(new)**
- **[42325613]** Decoding type 5 diabetes using spatial omics (malnutrition-related) — *Microbiome × Health Equity* **(new)**
- **[42325385]** Multi-omics: goat milk improves glucose homeostasis via gut–liver axis (mouse) — *Microbiome × Multi-Omics* **(new)**
- **[42295172]** An expanded indication for teplizumab (Tzield) — *T1D Immunotherapy × teplizumab*
- **[42296503]** Benefits/harms of pharmacologic obesity treatments (living review) — *orforglipron × retatrutide*

**Key-therapy mentions** (8 therapies tracked; all with hits): teplizumab (CGM-based early treatment-response assessment, 42267680; Tzield expansion brief, 42295172), **orforglipron** (head-to-head vs. dapagliflozin 42259339; ACHIEVE-5 + insulin glargine 42251769/766; vs. mazdutide commentary 42251768), **retatrutide** (triple-agonist Phase-3-class efficacy/safety 42250575), **CagriSema** (multiple T2D add-on / dose papers 42251856-860), icodec (once-weekly basal, 42254168/42277362), baricitinib (off-target: VEXAS/RA/COVID — not diabetes-specific this cycle), dapagliflozin (cardiac/renal structure papers).

**Volume:** even ~10 papers/domain across the 13 core domains (query cap), so no domain is anomalously hot or cold this cycle. GLP-1 Pharmacogenomics is the thinnest (2). The orforglipron/retatrutide/CagriSema cluster continues to dominate the T2D-therapy signal.

---

## Gap Analysis Summary

Top 5 under-researched intersections (Gap Score 100, BRONZE — single-source, expert confirmation pending) [from `literature_gap_report.md`; **note underlying data is 64 days old**]:

| Rank | Intersection | Joint Pubs | Tier-1 alignment |
|------|-------------|-----------|------------------|
| 1 | Beta Cell Regen × Health Equity | 0 | **Yes** — Epidemiology/Health-Equity (Tier 1 #6) |
| 2 | Insulin Resistance × Islet Transplant | 1 | Partial |
| 3 | Islet Transplant × Drug Repurposing | 0 | **Yes** — Drug Repurposing (Tier 1 #4) |
| 4 | Islet Transplant × Health Equity | 0 | **Yes** — Health Equity (Tier 1 #6) |
| 5 | Gene Therapy × LADA | 0 | Partial |

**Tier-1-aligned opportunities** worth queuing: gaps #1, #3, #4 map directly onto our Drug-Repurposing and Health-Equity contribution areas. #3 (repurposing immunosuppressants for islet-graft protection via computational screening) is the cleanest match to existing tooling (islet_repurposing pipeline already in the hub). Caveat: these ranks are computed on April data — re-running the gap analysis may reshuffle them.

---

## Breaking News (web check, last 7 days)

**Nothing genuinely new.** Searches for "diabetes breakthrough 2026" / "FDA diabetes approval 2026" returned only items already weeks-to-months old and already represented in the corpus: [Likely — based on dated sources]

- Tzield (teplizumab) Stage-3 / young-children expansion — Sanofi press release dated 2026-04-22; already captured (PubMed 42295172).
- Retatrutide TRIUMPH-1 (28.3% weight loss) — reported 2026-05-21; already in corpus (42250575).
- Awiqli (insulin icodec) once-weekly basal approval — 2026-03-26.

No Phase-3 readouts, FDA actions, or major publications in the trailing 7 days that warrant escalation.

---

## Recommended Actions

1. **Add NCT07659574 (UBT251 Phase-3 T2D) to the "Notable Trials to Watch" table** in `clinical_trials_summary.md` — new triple-agonist-class entrant, currently NOT_YET_RECRUITING. *(Manual edit; not done in this read-only run.)*
2. **Re-run the gap analysis** — `literature_gap_data.json` is 64 days stale and feeds the gap dashboards/report. Run: `python project1_literature_gap_analysis.py`. Until then, treat gap ranks as April-vintage.
3. **Read cross-domain paper 42325613** (type-5 diabetes spatial omics × health equity) — relevant to both Multi-Omics (Tier 1 #1) and Health Equity (Tier 1 #6); type-5 (malnutrition-related) is an under-covered category for us.
4. **Skim NCT07465926** (n≈451k GLP-1+SGLT2 early-combination, CKM stage 2–3) for the Clinical-Trial-Intelligence combination-mapping workstream (Tier 1 #3).
5. **Log the TADPOL status change** (NCT05594563 → ACTIVE_NOT_RECRUITING) in the tracker; no further action needed.
6. **No refresh needed** for clinical-trials or PubMed pipelines — both ran cleanly today.

---
*Evidence levels per Research Doctrine v1.0. New cross-domain and gap findings are BRONZE (single computational source) pending expert/triple-source validation. Read-only run — no existing files modified.*
