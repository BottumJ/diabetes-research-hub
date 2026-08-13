# Diabetes Research Hub — Monitor Report
**Run date:** 2026-08-10 (automated review run)
**Reviewer:** Hub monitor (read-only; no source files modified)

---

## TL;DR — What's Actionable

**Collector outage, day 24. Nothing has changed.** Every "latest" data file is still frozen at **2026-07-17**. No `clinical_trials_snapshot_*` or `pubmed_recent_snapshot_*` file exists after that date. This is the **fourth consecutive** daily report flagging the same freeze (08-07, 08-08, 08-09, now). [Certain — directory scan returns no snapshot after 2026-07-17; `clinical_trials_latest.json` metadata reads `generated: 2026-07-17T02:05:53`, `pubmed_recent_latest.json` reads `2026-07-17T02:06:39`.]

**One clarifying data point since yesterday:** on 2026-08-09 the *analysis/iterate* pipeline ran (`literature_gap_report.md`, `citation_validation.json`, `evidence_network.json`, `gap_evidence.json`, `pmid_verification.json`, `iterate_run_report_2026-08-09.md` all touched), but the **three baseline collectors did not.** This narrows the root cause: the analysis scheduler is alive; the *collector* scheduler (or the collector scripts themselves) is the fault. [Certain — those files carry 2026-08-09 mtimes; no new snapshot was produced.]

**Do this first — restart the collectors and capture whether they fail on execution or just produce no new data:**

```
python baseline_clinical_trials.py
python baseline_pubmed_alerts.py
python hub_monitor.py
```

If they run clean but write no new snapshot → the collector scheduler/cron is disabled. If they throw → capture the traceback; likely an API/endpoint or auth break at the 2026-07-17 boundary.

---

## File System Status

| File | Last modified | Age | Status |
|------|--------------|-----|--------|
| `clinical_trials_latest.json` | 2026-07-17 | 24 d | ⚠️ STALE (>14 d) |
| `pubmed_recent_latest.json` | 2026-07-17 | 24 d | ⚠️ STALE (>14 d) |
| `hub_monitor_report.md` | 2026-07-17 | 24 d | ⚠️ STALE (>14 d) |
| `literature_gap_data.json` | 2026-07-18 | 23 d | ⚠️ STALE (>14 d) |
| `literature_gap_report.md` | 2026-08-09 | 1 d | Fresh file — but still re-analyzes frozen 2026-07-17 PubMed data (header: "Date range: 2020/01/01 to 2026/07/17") |
| `agent_state.json` | 2026-08-09 | 1 d | Current (backup rotation still running) |

**How I know the freeze is real, not a filesystem artifact:**
- Dated snapshots run continuously **2026-03-15 → 2026-07-17, then stop.** No snapshot of either type exists after 2026-07-17. [Certain]
- Internal metadata confirms it: CT `total_trials: 858`, `generated 2026-07-17T02:05:53`; PubMed `total_unique_papers: 158`, `generated 2026-07-17T02:06:39`, 16 domains, 30-day lookback. [Certain]
- The 2026-08-09 gap report is cosmetically fresh only — it re-ran on the cached 2026-07-17 corpus and reproduced identical rankings. [Certain]

**Root cause [Likely]:** collector scheduler failed/disabled on or about 2026-07-17. The analysis and backup jobs still fire (proven by 08-09 activity); the collectors do not. A 24-day gap against a previously *daily* cadence is a stopped job, not a quiet news period.

---

## Clinical Trial Changes

**No new snapshot since 2026-07-17 → nothing to diff.** Frozen state carried for reference (`clinical_trials_latest.json`, 858 trials):

| Category | Trials |
|----------|--------|
| Diabetes Technology (Devices) | 236 |
| Recently Completed with Results | 321 |
| T1D Cure & Cell Therapy | 152 |
| T2D Novel Therapies (Ph 2–3) | 147 |
| T1D Immunotherapy & Prevention | 76 |

**Key Phase 3 trials still flagged RECRUITING (frozen 2026-07-17):**
- **NCT06832410 / NCT04786262** — Vertex, VX-880 (zimislecel), Ph 3 — islet cell therapy, T1D
- **NCT07222332 / NCT07222137** — Eli Lilly, baricitinib, Ph 3 — beta-cell preservation / Stage 3 T1D delay
- **NCT07076199** — Novo Nordisk, insulin icodec (weekly), Ph 3
- **NCT07564414** — Novo Nordisk, CagriSema, Ph 3
- **NCT07088068** — Sanofi, teplizumab comparison, Ph 3

Everything after 2026-07-17 — new trials, status changes, results postings — is **unobserved**. Backfill the gap once collectors restart.

---

## PubMed Highlights

**Frozen at 2026-07-17** — 158 unique papers, 16 domains. Nothing new. Highest-value cross-domain items carried forward:
- **[42459945]** *Framework for assessing algorithmic discrimination risks in training data: pediatric T1D* — AI/ML + Closed Loop AP + Health Equity (3 domains; Tier 1 Areas 5 & 6).
- **[42419792]** *Comparative effects of drugs for adults with overweight/obesity* — orforglipron + retatrutide + CagriSema.
- **[42411999]** *T1D Driven by Residual Recipient T Cells After Hematopoietic Transplant* — Stem Cell Cure + Immunotherapy.
- **[42458730] / [42459212]** two multi-omics precision-nutrition papers — Microbiome + Multi-Omics (Tier 1 Area 1).

**Key-therapy mention counts (frozen):** dapagliflozin 52 / orforglipron 10 / CagriSema 6 / retatrutide 4 / teplizumab 4 / icodec 3 / baricitinib 2 / **zimislecel 0**. The zimislecel zero-count persists — the alert query almost certainly misses the **"VX-880"** synonym. Fix in `baseline_pubmed_alerts.py`. [Likely]

---

## Gap Analysis Summary

From `literature_gap_report.md` (re-run 2026-08-09, but on frozen 2026-07-17 PubMed data; rankings unchanged). **Validation level: BRONZE** — single analytical source; requires expert confirmation per Research Doctrine.

**Top 5 under-researched intersections (Gap Score 100, zero joint pubs):**

| # | Intersection | Tier 1 alignment |
|---|--------------|------------------|
| 1 | Treg / CAR-T × Neuropathy | — |
| 2 | Beta Cell Regen × Health Equity | ✅ Area 6 (equity) |
| 3 | Treg / CAR-T × Health Equity | ✅ Area 6 |
| 4 | Glucokinase × Health Equity | ✅ Area 6 |
| 5 | Gene Therapy × LADA | partial (Area 2 synthesis) |
| (6) | Drug Repurposing × Health Equity | ✅ Areas 4 + 6 |

**Doctrine note:** four of the top six gaps involve **Health Equity** (Tier 1 Area 6 — public-data, computationally tractable). Strongest candidates for a literature-synthesis contribution, but each is BRONZE and must be checked against Cochrane/PROSPERO for existing reviews before any claim. Unchanged from 08-09 because the underlying corpus is frozen.

---

## Breaking News (web check, last 7 days: 2026-08-03 → 08-10)

**No confirmed brand-new Phase 3 readout or FDA action inside the 08-03 → 08-10 window.** [Likely — absence is harder to prove than presence.]

Two concrete items that fell **inside the outage window** and are therefore missing from your snapshots:

- **Garzulys (insulin aspart-fsan)** — FDA-approved **2026-07-24**, a rapid-acting biosimilar to NovoLog for adults and pediatric patients. Inside the outage window; absent from `clinical_trials_latest.json` and PubMed data. [Likely]
- **Retatrutide TRIUMPH Phase 3 (T2D), ~2026-07-23** — Lilly's triple GIP/GLP-1/glucagon agonist: ~1.7–1.9% HbA1c reduction and ~11.5–15.3% weight loss at 40 weeks vs placebo; secondary benefits in OSA and knee OA pain. Now carries an official **ADA newsroom** press release (previously secondary-source only). Still BRONZE until the primary publication is PubMed-indexed. [Likely]

Adjacent, likely near/pre-outage (flagged to avoid double-counting): Lilly **ACHIEVE-3** head-to-head positioning orforglipron as a superior oral GLP-1 for T2D; Novo Nordisk **amycretin/zenagamtide** Phase 2 data. Verify capture-date when the pipeline restarts.

Pre-outage FDA actions already noted in prior reports (no action needed): orforglipron weight-management approval (~2026-04-01); teplizumab pediatric Stage 3 T1D (2026-06-12).

---

## Recommended Actions

1. **Restart the three baseline collectors — highest priority, unchanged from 08-07 onward.** Run `baseline_clinical_trials.py`, `baseline_pubmed_alerts.py`, `hub_monitor.py`. The 08-09 evidence (analysis pipeline ran, collectors didn't) points the investigation at the **collector scheduler specifically** — check its cron/task entry first. [Certain this is the top action.]
2. **Backfill the 24-day gap.** Diff the first fresh snapshot against `clinical_trials_snapshot_2026-07-17.json` and `pubmed_recent_snapshot_2026-07-17.json` to recover missed trials, status changes, results, and papers in one pass.
3. **Log two outage-window externals into `Diabetes_Research_Tracker.xlsx` now**, tagged external/unverified (BRONZE): the **Garzulys** approval (2026-07-24) and the **retatrutide TRIUMPH** T2D readout (~2026-07-23, now ADA-sourced).
4. **Fix the zimislecel PubMed query** — add the **"VX-880"** synonym in `baseline_pubmed_alerts.py`; 0 hits despite Vertex's active Phase 3 is a terminology-coverage gap.
5. **After collectors restart, re-run `project1_literature_gap_analysis.py`** and confirm its header date range advances past 2026-07-17 — otherwise the gap report stays cosmetically fresh on stale data.
6. **Prioritize the Health-Equity gaps** (4 of top 6) for a Tier 1 synthesis contribution — verify each against Cochrane/PROSPERO first; all BRONZE.

---

*Generated by Diabetes Research Hub automated monitor — read-only review run. No source files were modified. Confidence tags follow Research Doctrine v1.0: [Certain] = verified from files/primary evidence, [Likely] = strong inference, [Guessing] = gap-fill.*
