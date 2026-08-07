# Diabetes Research Hub — Monitor Report
**Run date:** 2026-08-07 (automated review run)
**Reviewer:** Hub monitor (read-only; no source files modified)

---

## TL;DR — What's Actionable

**The pipeline is stale.** Your data-collection scripts stopped producing new output on **2026-07-17 — 21 days ago**. Every "latest" file (trials, PubMed) is frozen at that date. The only thing that refreshed since is `literature_gap_report.md` (2026-08-06), and it is re-analyzing the *same* frozen 2026-07-17 PubMed data, so its "fresh" timestamp is misleading.

Three FDA actions and three Phase 3 readouts on therapies you actively track (teplizumab, orforglipron, retatrutide) landed **before** your data froze or in the gap since — none are reflected in the current snapshots. **Re-run the three baseline scripts before trusting any downstream dashboard.**

---

## File System Status

| File | Last modified | Age | Status |
|------|--------------|-----|--------|
| `clinical_trials_latest.json` | 2026-07-17 | 21 d | ⚠️ STALE (>14 d) |
| `pubmed_recent_latest.json` | 2026-07-17 | 21 d | ⚠️ STALE (>14 d) |
| `hub_monitor_report.md` | 2026-07-17 | 21 d | ⚠️ STALE (>14 d) |
| `literature_gap_data.json` | 2026-07-18 | 20 d | ⚠️ STALE (>14 d) |
| `literature_gap_report.md` | 2026-08-06 | 1 d | Fresh file, but built on 2026-07-17 PubMed data |
| `agent_state.json` | 2026-08-06 | 1 d | Current |

Dated snapshots run continuously from 2026-03-15 through **2026-07-17**, then stop. No trial or PubMed snapshot exists for the last three weeks. This is a collection outage, not a quiet news period — see Breaking News below.

**Root cause [Likely]:** `baseline_clinical_trials.py` and `baseline_pubmed_alerts.py` have not executed since 2026-07-17. The gap-analysis script ran once more (2026-08-06) against cached data. `hub_monitor.py` itself has not run since 2026-07-17.

---

## Clinical Trial Changes

Because no snapshot exists after 2026-07-17, the comparison below is the **last full month of movement captured in the frozen data** (2026-06-16 → 2026-07-17), not activity since the last check.

**Totals:** 858 trials tracked (813 a month earlier). Categories: T1D Cure & Cell Therapy 152 · T1D Immunotherapy & Prevention 76 · T2D Novel Therapies 147 · Devices 236 · Recently Completed w/ Results 321.
**Movement in that window:** 62 new trials, 17 removed, 12 status changes, 0 newly posted results.

**Notable status changes (captured):**
- `NCT01897688` (Northwestern) Islet Transplantation Phase 3 → **COMPLETED**
- `NCT06111586` (Sanofi) Frexalimab, T1D insulin preservation → ACTIVE_NOT_RECRUITING
- `NCT05594563` (Emily Sims) TADPOL polyamines T1D → ACTIVE_NOT_RECRUITING
- `NCT05866536` / `NCT05180591` (Mass General) BCG vaccination T1D → ACTIVE_NOT_RECRUITING
- `NCT07215312` (Eli Lilly) LY3938577 T2D → ACTIVE_NOT_RECRUITING

**Key Phase 3 trials actively RECRUITING (52 total) — highest priority to watch:**
- **Vertex** `NCT06832410` & `NCT04786262` — VX-880 (zimislecel) islet cell therapy, T1D
- **Eli Lilly** `NCT07222137` & `NCT07222332` — Baricitinib for Stage 3 T1D delay / beta-cell preservation
- **Sanofi** `NCT07088068` — Teplizumab vs placebo (see FDA action below)
- **Novo Nordisk** `NCT07564414` — CagriSema dosing; `NCT07076199` — insulin icodec
- **AstraZeneca** `NCT07662135/07662044/07662213` — Elecoglipron Phase 3 program (new oral incretin)

**Key-org Phase 3 ACTIVE (results pending):** Lilly retatrutide `NCT05929079`, `NCT06260722`, `NCT06297603`; Lilly orforglipron master protocols `NCT06972472`, `NCT06993792`; Novo CagriSema `NCT06534411`.

**Most recent results posted (within frozen data):** Lilly orforglipron long-term safety `NCT06010004` (2026-06-30); Lilly tirzepatide vs dulaglutide CV `NCT04255433` (2026-07-08); Novo icodec switch study `NCT06340854` (2026-07-02). Worth a read if not yet logged in the tracker.

---

## PubMed Highlights

Frozen at 2026-07-17: 158 unique papers over a 30-day lookback, 16 domains, 8 tracked therapies.

**Cross-domain papers (highest value — 12 total).** These bridge domains and map directly onto Tier 1 gap targets:
- `[42459945]` Algorithmic discrimination risk in pediatric T1D training data — **AI/ML × Closed-Loop AP × Health Equity** (triple-domain)
- `[42419792]` Comparative effects of obesity drugs — **orforglipron × retatrutide × CagriSema** (triple-therapy review)
- `[42458730]` / `[42459212]` Multi-omic BMI modelling & precision nutrition — **Microbiome × Multi-Omics**
- `[42437645]` GLP-1R variant pharmacophore shifts — **GLP-1 Pharmacogenomics × orforglipron**
- `[42453334]` Noncoding RNAs for diabetes — **Biomarker × LADA**

**Tracked-therapy signal:** all 8 therapies (zimislecel, orforglipron, retatrutide, CagriSema, baricitinib, teplizumab, icodec, dapagliflozin) registered hits, but the collector caps at 2 papers/therapy, so counts understate real volume — do not read the "2" as a trend.

**Volume caveat:** the `domain_results` per-domain counts render as 0 in the current file (the counts live only in the `papers[]` domain tags). If you rely on per-domain volume, that field looks broken and is worth checking when you re-run the collector.

---

## Gap Analysis Summary

From `literature_gap_report.md` (re-run 2026-08-06 on 2026-07-17 data; **validation level BRONZE** — single analytical source, expert confirmation required).

**Top under-researched intersections (Gap Score 100, zero joint publications):**
1. **Treg / CAR-T × Neuropathy** — immune-mediated neuropathy as a Treg-modulation target
2. **Beta Cell Regen × Health Equity** — no access analysis of emerging cell therapies
3. **Treg / CAR-T × Health Equity** — no equity analysis of CAR-Treg access
4. **Glucokinase × Health Equity** — no equity analysis for the GKA drug class
5. **Gene Therapy × LADA** — autoimmune LADA as a gene-therapy candidate, no crossover work
   *(6. Drug Repurposing × Health Equity; 7. Insulin Resistance × Islet Transplant, Gap 91.9)*

**Alignment with your Tier 1 contribution areas (RESEARCH_DOCTRINE v1.1):**
- **#6 Drug Repurposing × Health Equity** maps onto **Tier 1 #4 (Drug Repurposing Computational Screening)** — a gap you are specifically resourced to attack.
- The multi-omic cross-domain PubMed papers above map onto **Tier 1 #1 (Multi-Omics Biomarker Integration)**.
- The gap analysis itself is **Tier 1 #2 (Literature Synthesis & Gap Analysis)** — but running it on 3-week-old data undercuts its value.

Every Gap-100 pair carries the standard caveat: zero joint pubs may mean genuine white space *or* terminology mismatch. Verify with a combined-term PubMed search before treating any as a real opportunity.

---

## Breaking News (web check)

The 7-day window is quiet, but the outage means several **material items from the preceding weeks are not in your data** — all touch therapies you track:

- **Teplizumab (Tzield) — new FDA indication, 2026-06-12.** Accelerated approval to delay insulin decline in pediatric Stage 3 T1D (ages 8–17). Directly relevant to Sanofi trial `NCT07088068` and Lilly's baricitinib Stage 3 program. [Significant]
- **Orforglipron (Foundayo) — FDA approval 2026-04-01** for obesity/overweight; **ACHIEVE-3** head-to-head positioned it as a superior oral GLP-1 for T2D. You track 6+ orforglipron Phase 3 trials. [Significant]
- **Retatrutide — first Phase 3 T2D+obesity readout, June 2026** (ADA Scientific Sessions): HbA1c −1.7 to −1.9% and 11.5–15.3% weight loss vs placebo. Your retatrutide Phase 3 trials are still marked ACTIVE_NOT_RECRUITING. [Significant]
- **Garzulys (insulin aspart-fsan biosimilar) — FDA approval 2026-07-24.** [Moderate]
- **Generic dapagliflozin — first FDA approval 2026-04-07.** [Moderate]

None of these had posted results reflected in the frozen `clinical_trials_latest.json`. Re-running the collector should pull the updated statuses and any newly posted results.

---

## Recommended Actions

**Do first (unblock the pipeline):**
1. `python baseline_clinical_trials.py` — trial data is 21 days stale.
2. `python baseline_pubmed_alerts.py` — PubMed data is 21 days stale.
3. `python hub_monitor.py` — regenerate the file-change baseline (last run 2026-07-17).
4. Re-run `python project1_literature_gap_analysis.py` **after** the PubMed refresh so the gap scores reflect current literature rather than 2026-07-17 data.

**Then review / log in the tracker:**
5. Update the tracker for the three FDA actions above (teplizumab pediatric indication, orforglipron approval, retatrutide Phase 3 readout) — confirm whether trial statuses/results changed once the collector re-runs.
6. Read the three most-recent posted results (`NCT06010004`, `NCT04255433`, `NCT06340854`) and confirm they're captured.
7. Watch the **AstraZeneca elecoglipron Phase 3 program** (`NCT07662044/135/213`) — a new oral incretin cluster that entered your Phase 3 recruiting set.

**Optional (analysis):**
8. Prioritize **Drug Repurposing × Health Equity** for computational work — it is both a Gap-100 intersection and a Tier 1 contribution area.
9. Investigate the `domain_results` zero-count field in the PubMed collector — appears to have stopped populating per-domain counts.

---

## Data Integrity Notes (per Research Doctrine)
- All gap classifications remain **BRONZE** (single-source; expert validation pending).
- Breaking-news items are sourced from web search and are **not yet verified against primary trial records** — treat as leads until the collector confirms.
- No source files were modified in this review run.

---
*Automated monitor review — 2026-08-07. Read-only. If the workspace looks stale on the next run and scripts still haven't re-run, the collection job itself may have failed and needs manual attention.*
