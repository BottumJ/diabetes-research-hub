# Diabetes Research Hub — Monitor Report

**Run date:** 2026-07-31 (automated, unattended)
**Scope:** Review of latest script outputs in `Analysis/Results/`, snapshot comparison, and web breaking-news check. No existing files were modified (review-only run).

Confidence tags follow the Research Doctrine: **[Certain]** = read directly from files / independently verifiable, **[Likely]** = strong inference, **[Guessing]** = gap-filling.

---

## Headline (read this first)

**The two baseline data pipelines are now frozen at 2026-07-17 — 14 days stale, third consecutive stale cycle.** `clinical_trials_latest.json` and `pubmed_recent_latest.json` have not regenerated since 07-17, and no new trial or PubMed snapshots have appeared in that window. **There is no genuinely new trial or publication activity this cycle** — every trial/paper detail below is the frozen 07-17 state carried forward and re-verified against the source files.

What is still running: the gap analysis re-ran again (`literature_gap_report.md` regenerated **07-30**, one day newer than yesterday), and `agent_state.json` was backed up **07-30**. But the gap report's own data range still ends **2026/07/17** — it is re-chewing the same frozen PubMed corpus. **The action is unchanged and now more urgent: manually re-run `baseline_clinical_trials.py` and `baseline_pubmed_alerts.py` and check their logs.** Three silent stale cycles is a failed or disabled job, not a skip. This has crossed the doctrine's own 14-day staleness threshold.

---

## File System Status

| File | Last modified | Age | Status |
|------|---------------|-----|--------|
| `clinical_trials_latest.json` | 2026-07-17 | 14 d | **Stale (at threshold)** |
| `pubmed_recent_latest.json` | 2026-07-17 | 14 d | **Stale (at threshold)** |
| `hub_monitor_report.md` | 2026-07-17 | 14 d | **Stale** |
| `literature_gap_data.json` | 2026-07-18 | 13 d | Aging |
| `literature_gap_report.md` | 2026-07-30 | 1 d | Fresh wrapper, **07-17 source data** |
| `agent_state.json` | 2026-07-30 | 1 d | Fresh |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | 14 d | **Stale** |

- Latest trial snapshot: `clinical_trials_snapshot_2026-07-17.json` — **no new snapshot in 14 days.** [Certain]
- Latest PubMed snapshot: `pubmed_recent_snapshot_2026-07-17.json` — same 14-day gap. [Certain]
- `agent_state.json` backups exist for 07-27, 07-29, 07-30 but **not 07-28 or 07-31** — the state/backup job is also skipping days, worth noting alongside the baseline failures. [Certain]
- The 07-17 hub monitor already flagged **827 result files older than 14 days**; that backlog has only grown. [Certain]

**Interpretation [Likely]:** `hub_monitor.py`, the gap runner, and the agent-state backup still fire (mostly). `baseline_clinical_trials.py` and `baseline_pubmed_alerts.py` stopped producing output after 07-17 and have not recovered across three cycles.

---

## Clinical Trial Changes

Source: `clinical_trials_latest.json` (generated 2026-07-17T02:05:53, ClinicalTrials.gov API v2). **858 trials** — T1D Cure & Cell Therapy 152, T1D Immunotherapy & Prevention 76, T2D Novel Therapies 147, Devices 236, Recently Completed w/ Results 321. [Certain, re-read from file this run]

**No snapshot diff exists since 07-17** — no new/changed/removed trials can be computed this cycle. [Certain]

### Phase 3 RECRUITING — key-organization trials to watch [Certain, re-verified from file]

| NCT | Sponsor | Therapy / focus |
|-----|---------|-----------------|
| NCT06832410 | Vertex | Islet cell therapy (biologic) — Phase 3 |
| NCT04786262 | Vertex | VX-880 / zimislecel — Phase 3 |
| NCT07076199 | Novo Nordisk | Insulin icodec (weekly) vs glargine/aspart |
| NCT07564414 | Novo Nordisk | CagriSema vs semaglutide |
| NCT07222332 | Eli Lilly | Baricitinib vs placebo (preserve beta-cell function) |
| NCT07222137 | Eli Lilly | Baricitinib vs placebo (delay Stage 3 T1D) |
| NCT07088068 | Sanofi | Teplizumab vs placebo |
| NCT06739122 | Eli Lilly | Dulaglutide |
| NCT07662044 / 07662109 / 07662213 / 07662135 | AstraZeneca | Elecoglipron (± dapagliflozin / semaglutide) |

Both Vertex zimislecel trials, both Lilly baricitinib trials, the Sanofi teplizumab trial, and the Novo CagriSema trial are all on the therapy watchlist. The four AstraZeneca elecoglipron Phase 3 trials (moved to RECRUITING in the last real data week, 07-10→07-17) are the newest key-org activity but are now two weeks unrefreshed.

### Recently posted results (frozen list, newest first) [Certain, re-read from file]

- NCT05086445 — **Eli Lilly, LY3502970 (orforglipron)** — posted 2026-07-16. Watchlist hit.
- NCT05574699 — Johns Hopkins, social-risk score + clinical decision support — posted 2026-07-15.
- NCT05254002 — Bayer, finerenone + empagliflozin — posted 2026-07-13.
- NCT04255433 — **Eli Lilly, tirzepatide vs dulaglutide** — posted 2026-07-08.
- NCT06340854 — Novo Nordisk, insulin icodec vs glargine — posted 2026-07-02.

All are ~2–4 weeks old; treat as reviewed unless the tracker still lists them open.

---

## PubMed Highlights

Source: `pubmed_recent_latest.json` (generated 2026-07-17T02:06:39, 30-day lookback, **158 unique papers**, 16 domains). Frozen — identical corpus to the last two cycles. [Certain, re-read from file]

**Cross-domain papers (highest value, 12 total).** Top hits [Certain]:

- **[42459945]** *A framework for assessing algorithmic discrimination risks in training data: pediatric type 1 diabetes* — **AI/ML + Closed Loop AP + Health Equity** (3 domains). Directly on our Tier-1 equity/epidemiology focus.
- **[42419792]** *Comparative effects of drugs for adults with overweight or obesity (systematic review)* — **orforglipron + retatrutide + CagriSema** (3 key therapies at once).
- [42437645] Variant-specific pharmacophoric shifts in GLP-1 receptor — **GLP-1 Pharmacogenomics + orforglipron**.
- [42411999] T1D driven by residual recipient T cells after HSCT — **T1D Stem Cell Cure + Immunotherapy**.
- [42436543] Dynamics of healthcare inequalities in T2D — **T2D Remission + Health Equity**.
- [42458355] Socioeconomic gradients in hypertension/diabetes management — **AI/ML + Health Equity**.

**Key-therapy mentions (30-day counts):** dapagliflozin 52, orforglipron 10, CagriSema 6, retatrutide 4, teplizumab 4, icodec 3, baricitinib 2, **zimislecel 0**. [Certain] The zimislecel gap persists — 0 hits despite two active Phase 3 trials. Almost certainly a query/terminology miss (search likely still keyed to "VX-880"); worth patching in `baseline_pubmed_alerts.py`.

No volume-trend read is meaningful while the feed is frozen. [Certain]

---

## Gap Analysis Summary

Source: `literature_gap_report.md` (regenerated 2026-07-30, data range through 2026/07/17). Validation level **BRONZE** — single analytical source, requires expert confirmation. [Certain]

Top under-researched intersections (Gap Score 100 = zero joint publications):

1. **Treg / CAR-T × Neuropathy** — 100.0, 0 joint pubs
2. **Beta Cell Regen × Health Equity** — 100.0, 0
3. **Treg / CAR-T × Health Equity** — 100.0, 0
4. **Glucokinase × Health Equity** — 100.0, 0
5. **Gene Therapy × LADA** — 100.0, 0

(Also flagged: Drug Repurposing × Health Equity 100.0; Insulin Resistance × Islet Transplant 91.9.)

**Tier-1 alignment [Likely] — correcting a prior overstatement:** The Research Doctrine's named Tier-1 areas are Multi-Omics Integration, Literature Synthesis/Gap Analysis, Clinical Trial Intelligence, Drug Repurposing, AI/ML Prediction, and Epidemiology/Health Equity. **Beta Cell Regen is *not* itself a named Tier-1 area** (earlier cycles implied it was — that was imprecise). The intersection that best maps to *two* genuine Tier-1 capabilities is **Drug Repurposing × Health Equity (100.0)** — repurposing (Tier-1 #4) plus epidemiology/equity (Tier-1 #6), both areas where we have data access and computational tooling. The **Health Equity-linked gaps generally** (ranks 2, 3, 4, plus Drug Repurposing × Health Equity) are the strongest fit for a computational literature-synthesis contribution. Per doctrine, verify each is a real gap (combined-term PubMed search + Cochrane/PROSPERO check) before acting — do not treat BRONZE findings as actionable.

---

## Breaking News (web check, last 7 days)

**No genuinely new (last-7-day) major event confirmed.** [Certain]

Standing context, not new this week:

- **Tzield (teplizumab, Sanofi) accelerated approval for Stage 3 T1D in children 8–17** — granted ~June 2026 on the Phase III PROTECT trial (n=328, C-peptide preservation). First disease-modifying therapy for newly diagnosed Stage 3 pediatric T1D. Confirm the tracker records this; if not, it graduates teplizumab from watchlist to approved for this indication. [Certain]
- **Vertex zimislecel (VX-880):** still investigational. Global regulatory submissions expected during 2026; realistic approval window 2027–2028 under expedited pathways (RMAT, Fast Track, PRIME, Innovation Passport). No confirmed new July-2026 filing or decision found this cycle. [Likely]
- Minor/routine: a first **generic dapagliflozin** approval surfaced in search results — low priority, noting only for completeness. [Guessing on recency — not date-verified]

---

## Recommended Actions

1. **Re-run the two stalled baseline scripts now — third consecutive stale cycle, past the 14-day threshold:**
   - `python baseline_clinical_trials.py`
   - `python baseline_pubmed_alerts.py`
   Then read their logs. Silent failure across 14 days points to an expired API key, network block, or a disabled scheduler entry — not a one-off skip.
2. **Diagnose the scheduler.** The gap and agent-state jobs run but the two baseline jobs do not, and agent-state itself skipped 07-28/07-31. If they share a runner, check for one disabled entry or a changed hub-root path (the 07-17 monitor referenced `/sessions/intelligent-bold-bardeen/...`, a different session root).
3. **Patch the zimislecel query** in `baseline_pubmed_alerts.py` — 0 hits despite two active Phase 3 trials strongly suggests the alert is still keyed to "VX-880" and missing the "zimislecel" INN.
4. **Update the tracker** with the Tzield Stage 3 pediatric approval if not already logged.
5. **Do not action gap findings yet** — they are BRONZE. If pursuing the Health-Equity intersections (esp. Drug Repurposing × Health Equity), run the doctrine's verification (combined-term search + Cochrane/PROSPERO) to lift toward SILVER.
6. **Re-run `project1_literature_gap_analysis.py` only after the PubMed feed recovers** — the current gap report is built on 07-17 data, so re-running it now would just reproduce today's result.

---

*Generated by the Diabetes Research Hub automated monitor — 2026-07-31. Review-only run; no source files modified. All trial/paper figures re-read directly from the source JSON this cycle.*
