# Diabetes Research Hub — Monitor Report

**Run date:** 2026-08-03 (automated, unattended)
**Scope:** Review-only. No existing files modified.

---

## ⚠️ Headline: Your data pipeline stalled ~17 days ago

The lead you probably don't want: **the data-collection scripts stopped producing fresh output on 2026-07-17/18.** Everything downstream (gap report, monitor reports) has kept running on that stale snapshot, which can create a false sense that the hub is current. It isn't.

`[Certain]` — file timestamps below are direct evidence.

| File | Last refreshed | Age (as of 08-03) | Status |
|------|---------------|-------------------|--------|
| `clinical_trials_latest.json` | 2026-07-17 | 17 days | STALE |
| `pubmed_recent_latest.json` | 2026-07-17 | 17 days | STALE |
| `literature_gap_data.json` | 2026-07-18 | 16 days | STALE |
| `hub_monitor_report.md` | 2026-07-17 | 17 days | STALE |
| latest `clinical_trials_snapshot_*` | 2026-07-17 | 17 days | STALE |
| latest `pubmed_recent_snapshot_*` | 2026-07-17 | 17 days | STALE |
| `literature_gap_report.md` | 2026-08-02 | 1 day | Re-rendered, but **on 07-17 data** (its own date range ends 2026/07/17) |

The 07-17 `hub_monitor_report.md` itself already flagged **827 result files older than 14 days**. That count is now worse.

**Fix first, read second.** The findings below are the best available, but they describe the world as of mid-July. Refresh before acting:

```
python baseline_clinical_trials.py     # refresh trials
python baseline_pubmed_alerts.py       # refresh PubMed alerts
python project1_literature_gap_analysis.py   # refresh gap analysis
python hub_monitor.py                  # refresh change tracking
```

---

## File System Status

All five expected input files exist and were read in full. None are missing. The problem is age, not absence. Snapshot history is dense and continuous from 2026-03-15 through 2026-07-17, then stops. Daily `agent_state.json` backups continue through 2026-08-02, so the orchestration wrapper is alive — only the data-fetch steps appear to have silently stopped.

`[Likely]` — the fetch scripts are erroring or being skipped while the wrapper keeps running. Worth checking `_gap_run.log` and any scheduler/cron output on your machine.

---

## Clinical Trial Changes

Trial corpus as of 2026-07-17: **858 trials** across 5 categories (T1D Cure & Cell Therapy 152, T1D Immunotherapy & Prevention 76, T2D Novel Therapies 147, Diabetes Technology 236, Recently Completed w/ Results 321).

Because no snapshot exists after 07-17, there are **zero day-over-day changes to report since the last run.** To show real movement I diffed the earliest retained snapshot (2026-03-15, 746 trials) against the latest (2026-07-17, 858 trials):

- **+174 new trials, −62 dropped, 55 status changes** over that ~4-month window.

### Key Phase-3 trials from tracked organizations (status as of 07-17)

| NCT | Sponsor | Therapy | Status |
|-----|---------|---------|--------|
| NCT06832410 | Vertex | zimislecel (islet cell) | RECRUITING |
| NCT04786262 | Vertex | zimislecel (islet cell) | RECRUITING |
| NCT07222332 | Eli Lilly | **baricitinib** (T1D preservation) | RECRUITING |
| NCT07222137 | Eli Lilly | **baricitinib** (T1D delay) | RECRUITING |
| NCT06993792 | Eli Lilly | **orforglipron** master protocol | ACTIVE, not recruiting |
| NCT06260722 | Eli Lilly | **retatrutide** vs semaglutide | ACTIVE, not recruiting |
| NCT07564414 | Novo Nordisk | **CagriSema** (new, since 03-15) | RECRUITING |
| NCT07076199 | Novo Nordisk | weekly insulin (icodec-class) | RECRUITING |

`[Certain]` — pulled directly from `clinical_trials_latest.json`. Note: two new Lilly **baricitinib** Phase-3 T1D trials are in the corpus — baricitinib is on your key-therapy watch list, so these two deserve tracker entries.

### Recently posted results
109 trials carry a 2026 `results_posted` date, newest 2026-07-16 (NCT05086445, Lilly orforglipron Ph1 Japan). None of these are *new* relative to the 07-16→07-17 diff the hub already logged (1 new / 1 dropped trial, 0 new results that day).

---

## PubMed Highlights

Snapshot: 158 unique papers, 30-day lookback, 16 domains, as of 2026-07-17.

### Key-therapy mention counts (last 30 days of that snapshot)

| Therapy | Papers | Note |
|---------|--------|------|
| dapagliflozin | 5 | 52 raw hits |
| orforglipron | 5 | |
| CagriSema | 5 | |
| retatrutide | 4 | |
| teplizumab | 4 | |
| icodec | 3 | |
| baricitinib | 2 | |
| **zimislecel** | **0** | No publications — watch, given Vertex Ph3 activity |

### Cross-domain papers (highest value — 12 total)
Top picks worth a human read:

- **[42459945]** Framework for assessing algorithmic discrimination risks in training data — pediatric T1D → *AI/ML × Closed-Loop AP × Health Equity* (3 domains). Directly on the equity intersections your gap analysis keeps flagging.
- **[42419792]** Comparative effects of obesity drugs (systematic review) → *orforglipron × retatrutide × CagriSema* — all three tracked therapies in one paper.
- **[42411999]** T1D driven by residual recipient T cells after HSCT → *Stem Cell Cure × Immunotherapy*.
- **[42453334]** Noncoding RNAs for diabetes (in silico → clinic) → *Biomarker × LADA*.
- **[42458730] / [42459212]** Multi-omic BMI-response modelling & precision-nutrition multi-omics → *Microbiome × Multi-Omics* (Tier-1 aligned, see below).

---

## Gap Analysis Summary

From `literature_gap_report.md` (re-rendered 08-02, but on 07-17 data; 30 domains, 435 pairs). Validation level **BRONZE** — single analytic source, needs expert confirmation per the Doctrine.

Top under-researched intersections (Gap Score / joint pubs):

1. Treg / CAR-T × Neuropathy — 100.0 / 0
2. Beta Cell Regen × Health Equity — 100.0 / 0
3. Treg / CAR-T × Health Equity — 100.0 / 0
4. Glucokinase × Health Equity — 100.0 / 0
5. Gene Therapy × LADA — 100.0 / 0

(Also flagged: Drug Repurposing × Health Equity — 100.0 / 0.)

### Alignment with Tier-1 contribution areas (from RESEARCH_DOCTRINE.md)
Tier-1 areas are Multi-Omics Biomarker Integration, Literature Synthesis & Gap Analysis, Clinical-Trial Intelligence, Drug-Repurposing Screening, AI/ML Prediction, and Epidemiology.

- **Drug Repurposing × Health Equity (gap 100)** maps onto Tier-1 #4 (Drug Repurposing) — a genuine white-space that fits your stated capability.
- The **Multi-Omics × Microbiome** cross-domain papers above map onto Tier-1 #1 (Multi-Omics Integration).
- The **AI/ML × Health Equity** discrimination-risk paper maps onto Tier-1 #5 (AI/ML) + #2 (Synthesis).

Caveat `[Guessing→Bronze]`: several gap-100 pairs (e.g., Treg/CAR-T × Neuropathy) may be terminology artifacts, not real white-space. The report itself says to verify each with a combined-term PubMed query before committing effort.

---

## Breaking News (web, significant items only)

Note on timing: the task asks for last-7-days news, but the freshest *significant* diabetes items sit slightly outside that window. Flagging them because they're material and involve therapies you track. `[Certain]` on the facts; dates verified against FDA/ADA sources.

- **Retatrutide Phase-3 positive (TRANSCEND-T2D-1), announced ADA, June 2026.** Triple GIP/GLP-1/glucagon agonist. HbA1c −18.5 to −21.2 mmol/mol and 11.5–15.3% weight loss vs placebo at 40 wks. Retatrutide is on your watch list and has ACTIVE Ph3 trials in-corpus (NCT06260722, NCT06297603, NCT05929079).
- **Tzield (teplizumab) — FDA approved new pediatric indication, June 12, 2026**, to delay insulin decline in ages 8–17 with recently-diagnosed Stage-3 T1D; backed by the Phase-3 PROTECT trial (328 patients). Teplizumab is tracked. This is the most consequential regulatory action for your T1D-immunotherapy category.
- **First generic dapagliflozin approved (April 7, 2026).** Access/equity implication for a tracked therapy — relevant to the Drug-Repurposing × Health-Equity gap theme.

No Phase-3 readouts or FDA actions found in the strict 2026-07-27→08-03 window that clear the "genuinely significant" bar.

---

## Recommended Actions (ranked)

1. **Refresh the pipeline before anything else.** Run the four scripts listed at the top. The whole hub is operating on 17-day-old data while looking current. Diagnose *why* fetches stopped on 07-17 (check `_gap_run.log` and scheduler logs) — a re-run that silently fails again wastes the next cycle.
2. **Add tracker entries for the two Lilly baricitinib Phase-3 T1D trials** (NCT07222332, NCT07222137) — tracked therapy, new since March, not yet obviously in the tracker.
3. **Log the June regulatory/readout events in the tracker:** Tzield pediatric approval (06-12) and retatrutide TRANSCEND-T2D-1 Ph3 readout (ADA, June). Both are tracked therapies; both are Evidence Level: regulatory/Phase-3 (higher than the Bronze gap findings).
4. **Verify, don't act on, the gap-100 pairs.** Run combined-term PubMed queries for Drug Repurposing × Health Equity and Beta Cell Regen × Health Equity (Tier-1 aligned) to confirm real white-space vs terminology artifact. Promote from Bronze only after a second source.
5. **Watch zimislecel:** 0 publications despite Vertex Phase-3 recruitment (NCT06832410, NCT04786262). Any first publication is a high-signal event.
6. **Housekeeping:** 827+ result files are >14 days old and daily `agent_state.json.bak_*` files are accumulating — consider a retention policy so the monitor isn't wading through 459 files in `Analysis/Results`.

---

*Generated by the Diabetes Research Hub automated monitor. Review-only run — no files were modified. Evidence levels noted per RESEARCH_DOCTRINE.md; all gap findings remain BRONZE pending expert confirmation.*
