# Diabetes Research Hub — Monitor Report
**Run date:** 2026-07-17 (automated, scheduled)
**Previous report:** 2026-07-16
**Scope:** Review of latest script outputs + 7-day web scan. Follow-up edits this session: gap metric recalibrated & re-run, staleness check patched, tracker de-duplicated (see Recommended Actions).

---

## Bottom line (read this first)

Nothing in the last 24h is field-changing. The one genuinely new datapoint is **Eli Lilly posting results for an orforglipron (LY3502970) Japanese T2D trial on 2026-07-16** — consistent with the ADA-2026 orforglipron momentum already in the corpus. Everything else is noise-level churn (1 trial in, 1 out, normal PubMed rotation).

Two things worth your attention that the scripts won't flag on their own:
- **The gap analysis was saturated — now fixed and re-run.** The old metric scored all 25 top intersections at exactly 100.0 (non-discriminating). Recalibrated to an independence model (expected = c1·c2/N, N=400,007) with a reliability filter; the ranking now spreads and orders by gap magnitude. Gap section below reflects the 2026-07-17 10:14 re-run.
- **827 of ~459 tracked result files are >14 days stale** (hub_monitor flag). Most are snapshot archives, so this is expected — the staleness check has since been patched to exclude archives, so future flags will count only live results.

---

## File System Status

All five key inputs exist and are current (generated 2026-07-17):

| File | Size | Generated | Status |
|------|------|-----------|--------|
| hub_monitor_report.md | 5.3 KB | 2026-07-17 02:16 | Fresh |
| clinical_trials_latest.json | 580 KB | 2026-07-17 02:05 | Fresh |
| pubmed_recent_latest.json | 121 KB | 2026-07-17 02:06 | Fresh |
| literature_gap_data.json | 124 KB | 2026-07-17 02:16 | Fresh |
| literature_gap_report.md | 4.1 KB | 2026-07-17 02:16 | Fresh |

Daily snapshot chains intact for both trials and PubMed through 2026-07-17. No missing or removed core files. `agent_state.json` backup written 2026-07-15.

**Stale flag:** hub_monitor reports 827 result files >14 days old. Confirmed benign — dominated by `clinical_trials_snapshot_*` and `agent_state.json.bak_*` archives that are meant to persist. No action needed; consider excluding archive globs from the staleness check.

---

## Clinical Trial Changes

**Corpus:** 858 trials tracked (T1D Cure & Cell Therapy 152, T1D Immunotherapy & Prevention 76, T2D Novel Therapies 147, Diabetes Technology 236, Recently Completed w/ Results 321).

**Diff vs. 2026-07-16 snapshot** (1 new, 1 removed, 0 status changes, 0 new results in-snapshot):
- **NEW — NCT05086445** (Eli Lilly, Phase 1, COMPLETED): "A Study of LY3502970 in Japanese Participants With Type 2 Diabetes." LY3502970 = **orforglipron**. Entered the set because **results were posted 2026-07-16**. This is the single actionable trial change today.
- **REMOVED — NCT07087340** (RECRUITING): "UBLoop-Genesis" UniBE hybrid closed-loop feasibility study. Dropped from the diabetes-tech query result set; [Guessing] likely a query-boundary drop rather than a real trial deletion — worth a one-time confirm if closed-loop tech is a tracked priority.

**Phase 3 RECRUITING — 52 trials.** Highest-relevance to our Tier-1 cell-therapy / immunotherapy focus:

| NCT | Sponsor | Focus |
|-----|---------|-------|
| NCT04786262 | **Vertex** | VX-880 islet cell therapy, T1D (Phase 3 RECRUITING) |
| NCT06832410 | **Vertex** | VX-880 in T1D w/ kidney transplant |
| NCT07222332 | **Eli Lilly** | Baricitinib to preserve beta-cell function, new-onset T1D (BARICADE-PRESERVE) |
| NCT07222137 | **Eli Lilly** | Baricitinib to delay Stage 3 T1D in at-risk |
| NCT07088068 | **Sanofi** | Teplizumab vs placebo, Stage 3 T1D, ages 1–25 |
| NCT06334133 | vTv Therapeutics | Cadisegliatin (glucokinase activator) adjunct to insulin, T1D |
| NCT07564414 | **Novo Nordisk** | CagriSema dosing, obesity ± T2D |
| NCT07076199 | **Novo Nordisk** | Insulin icodec (weekly) in T1D |
| NCT07662135 / NCT07662044 | AstraZeneca | Elecoglipron (oral GLP-1), Phase III T2D |

*Note:* Vertex VX-264 (encapsulated islets, NCT) is ACTIVE_NOT_RECRUITING. No zimislecel/Sana T1D trials surfaced in the current query set.

**Recently posted results worth a look:**
- Lilly **orforglipron** Japanese T2D (2026-07-16) — new today.
- Lilly **tirzepatide vs dulaglutide** major CV events, T2D (2026-07-08) — cardiovascular outcome data.
- Lilly **orforglipron** long-term safety, T2D (2026-06-30).
- **Northwestern** Phase 3 single-center islet transplantation, non-uremic (2026-06-18) — relevant to islet-transplant gap cluster below.
- Novo **insulin icodec** switch study, T2D (2026-07-02).

---

## PubMed Highlights

**Corpus:** 158 unique papers, 16 domains, 30-day lookback. Snapshot diff vs. 2026-07-16: **+28 new / −27 dropped** papers (normal rotation).

**Cross-domain papers (highest value — multi-domain overlap):**
- **[42459945]** "A framework for assessing algorithmic discrimination risks in training data: pediatric type 1 diabetes." — spans **AI/ML + Closed Loop AP + Health Equity** (3 domains). Directly on the Tier-1 AI/ML × Health-Equity seam. **Top pick to review.**
- **[42419792]** Network meta-analysis: comparative effects of obesity drugs — spans **orforglipron + retatrutide + CagriSema**. Useful cross-therapy benchmark.
- **[42458730]** & **[42459212]** — Multi-omic BMI/dietary-response modelling and precision-nutrition multi-omics review — both span **Microbiome + Multi-Omics** (Tier-1 multi-omics integration).
- **[42437645]** orforglipron–GLP-1R co-folding (Boltz-2) molecular dynamics — pharmacogenomics × key therapy.
- **[42411999]** T1D driven by residual recipient T cells post-HCT — Stem Cell Cure × Immunotherapy.

**Key therapy mentions (30-day):** dapagliflozin 52 (5 papers), **orforglipron 10 (5 papers)**, CagriSema 6, retatrutide 4, teplizumab 4, icodec 3, baricitinib 2, **zimislecel 0**. Orforglipron is the most active novel agent in the literature this cycle; zimislecel remains publication-silent despite Vertex's active VX-880 program.

---

## Gap Analysis Summary

*Recalibrated metric, re-run 2026-07-17 10:14. Corpus N = 400,007. 33 low-base-rate pairs (expected < 3 joint papers) excluded. Read the **Expected** column, not the score — a 100.0 with expected 25 is a real gap; a 100.0 with expected 3 is marginal.*

Top gaps by magnitude (expected joint papers, all found 0 unless noted):

| Rank | Intersection | Joint Pubs | Expected | Read as |
|------|--------------|-----------|----------|---------|
| 1 | GWAS / Polygenic × Closed Loop / AP | 0 | 25.4 | Biggest true gap |
| 2 | Drug Repurposing × CGM Technology | 0 | 10.2 | Tier-1 #4 |
| 3 | Treg / CAR-T × Neuropathy | 0 | 7.5 | |
| 4 | Beta Cell Regen × Health Equity | 0 | 7.3 | Tier-1 #6 |
| 5 | Treg / CAR-T × Health Equity | 0 | 4.7 | Tier-1 #6 |
| 6 | Glucokinase × Health Equity | 0 | 4.3 | Tier-1 #6 |
| — | *(then Gene Therapy×LADA, Islet Transplant×GWAS, etc., expected ~3, marginal)* | | | |

Note the metric now discriminates below the zero-overlap cluster: e.g. Insulin Resistance × Closed Loop/AP scores 96.9 (3 found vs 95 expected), Retinopathy × Gestational DM 92.5 (48 vs 641) — real, ranked signal instead of a flat wall of 100s.

**Alignment with Tier-1 contribution areas (RESEARCH_DOCTRINE.md):**
- **GWAS/Polygenic × Closed-Loop/AP** is the standout — 25 papers expected, zero found. Largest genuine white space. [Likely] worth one manual PubMed check to rule out a terminology mismatch before treating as virgin territory.
- Strong overlap with **Tier-1 #4 Drug Repurposing** (×CGM #2, ×Health Equity) and **Tier-1 #6 Epidemiology/Health Equity** (Beta Cell Regen, Treg/CAR-T, Glucokinase all × Health Equity in the top 6).
- The old **Islet Transplant** dominance was largely a small-denominator artifact — the reliability filter now demotes most Islet-Transplant pairings (expected < 3) out of the actionable list, confirming they were metric noise, not opportunity.

---

## Breaking News (7-day web scan)

**No genuinely new (past-7-day) breakthrough or FDA action identified.** The significant 2026 developments the scan surfaced are all June-or-earlier and already reflected in the local corpus:
- Retatrutide first Phase 3 T2D/obesity results — ADA 2026 (June).
- Orforglipron ACHIEVE-2/-3 superiority data — ADA 2026 (June); FDA approval of Foundayo (orforglipron) April 2026.
- Teplizumab (Tzield) pediatric Stage-3 T1D indication — FDA, June 12 2026.
- Once-weekly insulin icodec (Awiqli) — FDA, March 2026.

These corroborate rather than update the hub. [Certain] Nothing requires tracker changes on news grounds this week.

---

## Recommended Actions

**Open:**
1. **Review cross-domain paper [42459945]** (algorithmic discrimination in pediatric T1D) — sits on the AI/ML × Health-Equity Tier-1 seam; strongest single candidate this cycle. Review note saved to `paper_review_42459945.md`.
2. **Manual-check GWAS/Polygenic × Closed-Loop/AP** — the #1 recalibrated gap (25 expected, 0 found). Confirm it's real white space vs. a keyword mismatch before scoping work.

**Resolved this session (2026-07-17):**
3. ~~Recalibrate the gap metric~~ — **done.** Replaced geometric-mean expected with independence model (c1·c2/N) + reliability filter + magnitude sort in `project1_literature_gap_analysis.py`; re-run at 10:14. See updated Gap section above.
4. ~~Confirm the NCT07087340 drop~~ — **done.** [Certain] Trial still RECRUITING on ClinicalTrials.gov (Univ. of Bern, UBLoop-Genesis). Snapshot drop was a query-boundary artifact, not a deletion.
5. ~~Trim the staleness check~~ — **done.** `hub_monitor.py` now excludes `*_snapshot_*`, `*.bak_*`, and logs.
6. ~~Log orforglipron result~~ — **superseded.** Orforglipron already tracked; instead consolidated 3 duplicate tracker rows into 1 accurate entry and fixed a stale "NDA Under Review" status (now "FDA Approved"). The Phase-1 Japanese result (NCT05086445) is not status-changing — no row added.

*Evidence framing (per Research Doctrine): trial and PubMed counts are [Certain] from local JSON. Gap rankings are recomputed under the recalibrated independence model. No new scientific claims asserted; results-posted trials are pointers to primary sources, not validated findings.*

---
*Generated by diabetes-hub-monitor (automated scheduled review) — 2026-07-17. Gap section and actions updated post-recalibration; tracker and scripts modified this session as noted.*
