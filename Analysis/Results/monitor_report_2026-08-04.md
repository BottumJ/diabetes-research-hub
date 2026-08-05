# Diabetes Research Hub — Monitor Review

**Run date:** 2026-08-04 (automated, unattended)
**Reviewer:** Hub monitor (scheduled task)
**Bottom line:** The core data feeds are stale. Trials, PubMed, and the hub-monitor scan all last refreshed **2026-07-17 (18 days ago)**. Everything below is read off that 18-day-old snapshot except the web check. The single most useful action today is to **re-run the three baseline scripts** before trusting any "latest" figure.

---

## File System Status

| File | Last modified | Age (days) | State |
|------|---------------|-----------|-------|
| `clinical_trials_latest.json` | 2026-07-17 | 18 | **STALE (>14d)** |
| `pubmed_recent_latest.json` | 2026-07-17 | 18 | **STALE (>14d)** |
| `hub_monitor_report.md` | 2026-07-17 | 18 | **STALE (>14d)** |
| `literature_gap_data.json` | 2026-07-18 | 17 | **STALE (>14d)** |
| `literature_gap_report.md` | 2026-08-03 | 1 | Fresh file, **stale inputs** |

Caveat on the gap report: it was *regenerated* 2026-08-03, but its own header still reads "Date range: 2020/01/01 to **2026/07/17**." It re-ran the analysis on the 18-day-old PubMed pull — new file, old data. Don't read the fresh timestamp as fresh evidence.

Newest dated snapshots on disk: `clinical_trials_snapshot_2026-07-17.json`, `pubmed_recent_snapshot_2026-07-17.json`. No snapshot exists after 2026-07-17, which confirms the pipeline has not run in 18 days. The daily `monitor_report_*.md` cadence also has gaps (last daily: 2026-08-03).

**Action:** the hub_monitor's own review flag already warned "827 result files older than 14 days." That count is now larger. Refresh before contributing anything downstream.

---

## Clinical Trial Changes

Snapshot as of 2026-07-17: **858 trials tracked.**

Category counts: T1D Cure & Cell Therapy 152 · T1D Immunotherapy & Prevention 76 · T2D Novel Therapies (Ph2-3) 147 · Diabetes Technology 236 · Recently Completed w/ Results 321.
Status mix: 321 COMPLETED · 269 RECRUITING · 151 NOT_YET_RECRUITING · 110 ACTIVE_NOT_RECRUITING · 7 ENROLLING_BY_INVITATION. **52 trials are Phase 3 + RECRUITING.**

### Key Phase 3 trials from priority sponsors (current status as of 07-17)

| NCT | Sponsor | Therapy | Phase | Status |
|-----|---------|---------|-------|--------|
| NCT06832410 | Vertex | **VX-880 / zimislecel** (T1D + kidney transplant) | 3 | RECRUITING |
| NCT04786262 | Vertex | **VX-880 / zimislecel** (T1D) | 3 | RECRUITING |
| NCT07222332 | Eli Lilly | **Baricitinib** — preserve beta-cell function, children | 3 | RECRUITING |
| NCT07222137 | Eli Lilly | **Baricitinib** — delay Stage 3 T1D | 3 | RECRUITING |
| NCT07564414 | Novo Nordisk | **CagriSema** + oral | 3 | RECRUITING |
| NCT06962280 | Eli Lilly | Tirzepatide in T1D (long-term) | 3 | ACTIVE_NOT_RECRUITING |
| NCT06260722 | Eli Lilly | **Retatrutide** vs semaglutide | 3 | ACTIVE_NOT_RECRUITING |
| NCT06993792 | Eli Lilly | **Orforglipron** master protocol | 3 | ACTIVE_NOT_RECRUITING |

Highest-signal items: Vertex's zimislecel is now in **two Phase 3 trials, both recruiting** — the cell-therapy cure program has crossed into pivotal stage. Lilly has moved **baricitinib (a repurposed JAK inhibitor) into two Phase 3 T1D-prevention trials** — directly relevant to Tier 1 Drug Repurposing.

### Recently posted results worth a look (posted 2026)

- **NCT06010004** — Orforglipron long-term safety (Phase 3, Lilly), results posted 2026-06-30.
- **NCT05514535** — Semaglutide + lower-dose combo (Phase 3, Novo), 2026-05-11.
- **NCT05254002** — Finerenone combination (Phase 2, Bayer), 2026-07-13.
- **NCT05925920** — ENT-03 (Phase 1), 2026-06-01.

### Net-new trials in the final week of data (07-10 → 07-17): 8

Mostly completed device/behavioral studies. New/upcoming interventional ones: NCT07699380 (UW, Phase 2, metabolic modulation for insulin sensitivity, RECRUITING), NCT07702890 (Gubra A/S, Phase 1/2 first-in-human, NOT_YET_RECRUITING). Nothing here overrides the staleness problem — there is simply **no local trial data after 07-17 to review.**

---

## PubMed Highlights

Snapshot 2026-07-17: 158 unique papers, 30-day lookback, 16 domains.

### Cross-domain papers (highest value — appear in ≥2 alert domains)

- **[42459945]** A framework for assessing algorithmic discrimination risks in training data (pediatric T1D) — **AI/ML × Closed-Loop AP × Health Equity** (triple-domain; the standout).
- **[42458730]** Multi-omic modelling of BMI response to dietary weight-loss — Microbiome × Multi-Omics.
- **[42459212]** Precision nutrition in Asian populations, multi-omics review — Microbiome × Multi-Omics.
- **[42411999]** T1D driven by residual recipient T cells after hematopoietic cell transplant — Stem Cell Cure × Immunotherapy.
- **[42436543]** Healthcare inequalities in T2D over time — Remission × Health Equity.
- **[42453334]** Noncoding RNAs for diabetes, in silico to clinic — Biomarker × LADA.
- **[42419792] / [42394981] / [42444567]** Incretin/obesity comparative-effectiveness reviews spanning orforglipron / retatrutide / CagriSema.

### Key-therapy mentions (30-day window)

zimislecel **0** · orforglipron 10 (5 papers) · retatrutide 4 · CagriSema 6 · baricitinib 2 · teplizumab 4 · icodec 3 · dapagliflozin 52 (5 papers).
Note: zimislecel had zero publication hits despite two active Phase 3 trials — a genuine literature gap around the lead cell-therapy candidate.

### Volume note

Domain totals are capped at 10 returned papers each, so use `total_count` for trend, not `paper_count`. Highest-activity domains by total_count: AI/ML (260), Microbiome (186), GLP-1 New (167), Biomarker (166). All figures are 18 days old.

---

## Gap Analysis Summary

Top 5 under-researched intersections (Gap Score, BRONZE / single-source, expert confirmation required):

1. **Treg / CAR-T × Neuropathy** — 100.0, 0 joint pubs
2. **Beta Cell Regen × Health Equity** — 100.0, 0
3. **Treg / CAR-T × Health Equity** — 100.0, 0
4. **Glucokinase × Health Equity** — 100.0, 0
5. **Gene Therapy × LADA** — 100.0, 0
(6th: Drug Repurposing × Health Equity — 100.0, 0; 7th: Insulin Resistance × Islet Transplant — 91.9, 1)

### Tier 1 alignment

Four of the top six gaps are **Health-Equity intersections**, which maps directly to Tier 1 area #6 (Epidemiological / Health-Equity Analysis) and #4 (Drug Repurposing). **Drug Repurposing × Health Equity** sits in both Tier 1 lanes at once — the strongest doctrine-aligned opening on the board. Beta Cell Regen × Health Equity is timely given zimislecel entering Phase 3: nobody is analyzing *who will get access* to cell-therapy cures.

Standard caveat per the Research Doctrine: gap scores are keyword-based and BRONZE. A zero-joint-pub score can mean genuine white space *or* terminology mismatch. Verify each with a combined-term PubMed query and a Cochrane/PROSPERO check before treating as a real gap.

---

## Breaking News (web check, last ~7 days / ADA 2026 cycle)

- **[Likely] Teplizumab (Tzield) — pediatric Stage 3 T1D.** Reported FDA action July 2026 on the Phase 3 PROTECT trial (328 patients, ages 8–17, recently-diagnosed Stage 3). The hub already tracks teplizumab and has a prior `teplizumab_sNDA_decision_prep.md`. **Verify the exact approval/label scope directly on FDA.gov before logging as fact.**
- **[Certain] Retatrutide Phase 3 T2D + obesity** results presented at ADA 2026 (June): HbA1c −1.7 to −1.9% vs −0.8% placebo; weight loss ~11.5–15.3% vs 2.6% at 40 weeks; secondary benefits in OSA and knee OA pain. Matches locally-tracked NCT06260722 / NCT06297603.
- **[Certain] Orforglipron ACHIEVE-2** — superiority over dapagliflozin in adults inadequately controlled on metformin.
- **[Likely] Zimislecel (VX-880)** — Phase 3 underway (matches local NCT06832410/NCT04786262); Vertex global regulatory filings planned 2026, realistic FDA approval window 2027–2028.

None of these contradict the local data; they confirm it and are 2–6 weeks ahead of the frozen 07-17 snapshot.

---

## Recommended Actions

1. **Refresh the pipeline — this is the priority.** Data is 18 days stale. Run, in order:
   - `python baseline_clinical_trials.py`
   - `python baseline_pubmed_alerts.py`
   - `python project1_literature_gap_analysis.py`
   - `python hub_monitor.py`
2. **Re-run the gap analysis specifically** — the 2026-08-03 report re-computed on 07-17 inputs (range still ends 2026/07/17). It needs a fresh PubMed pull to be meaningful.
3. **Confirm the teplizumab pediatric FDA action** on FDA.gov, then update `Diabetes_Research_Tracker.xlsx` and the teplizumab prep note. Evidence level: promote to Silver/Gold only after primary-source confirmation.
4. **Log zimislecel Phase 3 dual-recruitment** (NCT06832410 + NCT04786262) in the tracker — the cure program is at pivotal stage and has **zero** supporting literature hits (publication gap worth flagging).
5. **Pursue Drug Repurposing × Health Equity** as the lead Tier-1-aligned gap (both Tier 1 #4 and #6). Baricitinib's move into two Phase 3 T1D trials is a live, concrete repurposing case to anchor it.
6. **Review cross-domain paper [42459945]** (algorithmic-discrimination framework, pediatric T1D) — sits across AI/ML, Closed-Loop, and Health Equity, all Tier 1 / near-Tier-1.

*No existing files were modified. This is a review-only run. All counts are read from the 2026-07-17 snapshot unless marked as web-sourced.*
