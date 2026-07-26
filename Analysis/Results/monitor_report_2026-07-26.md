# Diabetes Research Hub — Monitor Report

**Run date:** 2026-07-26 (automated, unattended)
**Scope:** Review-only. No existing files were modified.
**Headline:** Core data ingestion is frozen at 2026-07-17 — the trial and PubMed feeds are 9 days stale. The daily monitor and gap analysis kept running on top of stale inputs. **Re-run the two baseline collectors before trusting any "latest" file.**

---

## 1. File System Status

| File | Last modified | Age | State |
|------|--------------|-----|-------|
| `clinical_trials_latest.json` | 2026-07-17 | 9 d | **Stale** |
| `pubmed_recent_latest.json` | 2026-07-17 | 9 d | **Stale** |
| `hub_monitor_report.md` | 2026-07-17 | 9 d | **Stale** |
| Newest `clinical_trials_snapshot_*.json` | 2026-07-17 | 9 d | **Stale** — no daily pulls since |
| Newest `pubmed_recent_snapshot_*.json` | 2026-07-17 | 9 d | **Stale** |
| `literature_gap_data.json` | 2026-07-18 | 8 d | Aging |
| `literature_gap_report.md` | 2026-07-25 | 1 d | Fresh — but built on the 2026-07-17 PubMed window |
| `agent_state.json` | 2026-07-25 | 1 d | Fresh (daily backups continue) |

Interpretation: the state file and gap report update daily, but the two data collectors (`baseline_clinical_trials.py`, `baseline_pubmed_alerts.py`) have not produced a new snapshot since 2026-07-17. The last hub_monitor scan itself flagged **827 result files older than 14 days**. The gap report regenerated on 07-25 but its date range still ends 2026/07/17, confirming it reused the frozen PubMed pull rather than fresh data.

**Confidence: [Certain]** — based on file modification timestamps and the date ranges embedded in the files themselves.

---

## 2. Clinical Trial Changes

Latest corpus: **858 trials** (generated 2026-07-17). Category split: T1D Cure & Cell Therapy 152, T1D Immunotherapy & Prevention 76, T2D Novel Therapies 147, Diabetes Technology 236, Recently Completed w/ Results 321.

**Day-over-day (07-16 → 07-17, per hub_monitor):** 1 new trial, 1 removed, 0 status changes, 0 new results. Quiet.

**Period drift since the 2026-03-15 baseline** (746 → 858 trials): **174 trials appeared, 62 dropped, 55 status changes, 4 newly-posted results.** No comparison is possible past 07-17 because collection stopped.

Key Phase 3 trials still recruiting, by tracked sponsor:

- **Vertex** — VX-880 / zimislecel islet cell therapy: two Phase 3 trials recruiting (NCT06832410, NCT04786262). VX-264 (encapsulated) is Phase 1/2 active, not recruiting.
- **Eli Lilly** — Two Phase 3 **baricitinib** beta-cell-preservation trials recruiting (NCT07222332, NCT07222137); orforglipron and retatrutide master protocols active/not-recruiting.
- **Novo Nordisk** — Insulin icodec weekly Phase 3 recruiting (NCT07076199); multiple CagriSema Phase 3 trials active/not-yet-recruiting.
- **Sanofi** — Phase 3 **teplizumab** head-to-head (NCT07088068) recruiting — directly relevant to this week's FDA news (§5).
- **Diamyd Medical** — Phase 3 Diamyd antigen therapy recruiting (NCT05018585).
- New in-period: a wave of **AstraZeneca** Phase 3 incretin trials (NCT07662044/109/135/213) plus Roche enicepatide and Amgen extension trials.

Recently posted results worth a look (most recent): Lilly LY3502970/orforglipron Japanese T2D (2026-07-16), Johns Hopkins social-risk-score CGM decision support (2026-07-15), Bayer combination trial (2026-07-13).

**Confidence: [Certain]** for counts and statuses in the 07-17 file; **[Likely]** that additional trials/results have appeared in the 9-day blackout and are simply not captured.

---

## 3. PubMed Highlights

Latest pull: **158 unique papers**, 30-day lookback ending 2026-07-17, 16 domains.

**Cross-domain papers (12 total — highest value).** Most notable:

- **[42459945]** *A framework for assessing algorithmic discrimination risks in training data: a case of pediatric type 1 diabetes* — spans **AI/ML + Closed-Loop AP + Health Equity**. Triple-domain; directly on a Tier 1 theme (see §4).
- **[42419792]** Comparative effects of obesity drugs — orforglipron + retatrutide + CagriSema in one head-to-head synthesis.
- **[42411999]** T1D driven by residual recipient T cells after HSCT — Stem Cell Cure + Immunotherapy.
- **[42437645]** Variant-specific pharmacophoric shifts in GLP-1 receptor — GLP-1 Pharmacogenomics + orforglipron.

**Key-therapy mention counts:** orforglipron 10 (5 papers), CagriSema 6, retatrutide 4, teplizumab 4, icodec 3, baricitinib 2, dapagliflozin 52 (5 papers). **zimislecel: 0** — Vertex's cell therapy has active Phase 3 trials but no indexed publications in the window, a watch item.

**Confidence: [Certain]** for the counts; the 158-paper set is frozen and does not reflect the last 9 days.

---

## 4. Gap Analysis Summary

Top under-researched intersections (Gap Score, joint publications), BRONZE validation:

| Rank | Intersection | Gap | Joint pubs |
|------|-------------|-----|-----------|
| 1 | Treg / CAR-T × Neuropathy | 100 | 0 |
| 2 | Beta Cell Regen × Health Equity | 100 | 0 |
| 3 | Treg / CAR-T × Health Equity | 100 | 0 |
| 4 | Glucokinase × Health Equity | 100 | 0 |
| 5 | Gene Therapy × LADA | 100 | 0 |

**Tier 1 alignment (from RESEARCH_DOCTRINE.md):** The gap engine itself is Tier 1 #2 (Literature Synthesis & Gap Analysis, 19/20). Three of the top five gaps route through **Health Equity**, which maps to Tier 1 #12 (Technology Accessibility & Digital Health). Gene Therapy × LADA touches Tier 1 #11 (Subtype Misdiagnosis). These remain single-source (BRONZE) and need the doctrine's expert confirmation before any claim is made — a 0-joint-pub result can equally mean "terminology mismatch," not "unexplored."

**Confidence: [Likely]** that these are real gaps; **[Guessing]** on which are genuinely actionable vs. keyword artifacts — the report explicitly flags this and asks for expert review. Path to [Certain]: run combined-term PubMed verification queries + check Cochrane/PROSPERO for existing reviews per the doctrine.

---

## 5. Breaking News (web check, last ~7 days)

Genuinely significant, and each maps to a therapy/trial already tracked here:

- **FDA — Tzield (teplizumab) pediatric indication.** FDA granted a new indication (accelerated approval, June 12, 2026) to delay insulin decline in children 8–17 recently diagnosed with Stage 3 T1D, supported by the Phase 3 PROTECT trial (328 patients). Directly relevant to the tracked Sanofi Phase 3 teplizumab trial NCT07088068.
- **Retatrutide** — first Phase 3 T2D + obesity results (GIP/GLP-1/glucagon triple agonist) reported around ADA (June 2026): ~1.7–1.9% HbA1c reduction and ~11–15% weight loss vs placebo. Tracked therapy.
- **Orforglipron (Foundayo)** — oral small-molecule GLP-1 received FDA approval (April 2026); three Phase 3 datasets presented at ADA 2026. Tracked therapy.
- **Insulin efsitora alfa (Lilly)** — FDA decision was expected in July 2026; worth confirming outcome on next run. Multiple efsitora Phase 3 trials are already in the corpus as completed.

**Confidence: [Likely]** — from reputable secondary sources (FDA, ADA, Pharmacy Times). Verify efsitora decision status directly before recording it as a claim.

---

## 6. Recommended Actions

1. **Refresh the frozen feeds first.** Run `python baseline_clinical_trials.py` and `python baseline_pubmed_alerts.py`. All "latest" trial/PubMed data is 9 days old; today's day-over-day diffs are meaningless until these run.
2. **Re-run the monitor after refresh** so hub_monitor.py diffs fresh 07-26 snapshots against 07-17 (the real 9-day delta is uncaptured).
3. **Confirm and log the Tzield pediatric approval** against tracked trial NCT07088068 (Sanofi teplizumab) and update `Diabetes_Research_Tracker.xlsx` — this is a concrete regulatory event on a tracked therapy.
4. **Verify the insulin efsitora alfa FDA decision** (expected July 2026); record outcome with an evidence level.
5. **Review cross-domain paper [42459945]** (algorithmic discrimination in pediatric T1D — AI/ML + Closed-Loop + Health Equity); it sits on a Tier 1 theme and three of the top-five gaps involve Health Equity.
6. **Validate the top-5 gaps** with combined-term PubMed queries + Cochrane/PROSPERO before promoting any from BRONZE — several may be terminology artifacts.
7. **Watch zimislecel:** active Vertex Phase 3 trials but 0 indexed publications in the window.

---

*Generated by the Diabetes Research Hub automated monitor. Evidence levels follow RESEARCH_DOCTRINE.md. This was a review-only run; no source files were altered.*
