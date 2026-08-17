# Monitor Report — 2026-08-15

**Run type:** Automated review (read-only). No files were modified.
**Scan scope:** `Analysis/Results/`, `RESEARCH_DOCTRINE.md`, `Analysis/Scripts/`, web check.

---

## HEADLINE: The ingestion pipeline has been dead for 29 days, but the hub still looks alive

This is the only finding that matters today. Everything below it is a consequence.

| Layer | Script | Last real data | Age (days) | State |
|---|---|---|---|---|
| Clinical trials | `baseline_clinical_trials.py` | 2026-07-17 02:05 | **29** | **STOPPED** |
| PubMed alerts | `baseline_pubmed_alerts.py` | 2026-07-17 02:06 | **29** | **STOPPED** |
| Gap analysis (data) | `gap_analysis_daily.py` | 2026-07-18 03:11 | **28** | **STOPPED** |
| Hub monitor | `hub_monitor.py` | 2026-07-17 02:16 | **29** | **STOPPED** |
| Gap report (render) | `improve_gap_analysis.py` | 2026-08-14 03:07 | 1 | RUNNING on stale input |
| Citation validation | `validate_citations.py` | 2026-08-14 03:08 | 1 | RUNNING |
| Agent state | `agent_state.py` | 2026-08-14 03:09 | 1 | RUNNING (daily, unbroken) |

**The failure mode is worse than a clean outage.** The *fetch* half of the pipeline stopped on 17 July; the *render* half kept running nightly through 14 August. `literature_gap_report.md` carries a **"Generated: 2026-08-14"** timestamp while its own body declares **"Date range: 2020/01/01 to 2026/07/17."** A fresh-looking file, built from a month-old corpus. Anything consuming that report — dashboards, `Research_Findings_Summary.md`, downstream claims — has been inheriting a false currency signal for four weeks.

**[Certain]** — mtimes, in-file metadata timestamps, and `metadata.date_range` fields all agree independently.

### Where the break is
`Analysis/Logs/` last wrote `gap_analysis_2026-07-17.log` (2026-07-17 09:30). Steps 1–4 logs (`1_trials.log` … `4_hub.log`) are frozen at 2026-07-03. `run_daily_local.py`'s own docstring documents the root cause: the sandbox kills processes at ~45s, and the gap analysis needs 35–40 minutes for 465 sequential PubMed queries. **The four fetch scripts can only run on your machine.** They stopped when the local run stopped. The nightly Cowork-side jobs — which are short enough to survive the sandbox — never noticed.

**[Likely]** — the local scheduled task (`register_daily_task.ps1` / `run_daily_pipeline.ps1`) is disabled, erroring, or the machine has not been running the job. To move this to [Certain], check Windows Task Scheduler history for the registered task.

### Blind-spot arithmetic
`pubmed_recent_latest.json` uses a rolling **30-day lookback** ending 2026-07-17, so it covers ~17 Jun – 17 Jul. Publications from **18 Jul – 15 Aug 2026 have never been ingested by any alert domain.** At the observed rate (~28 new papers/day across 16 domains, from the last hub_monitor diff), that is roughly **800 unreviewed papers**, including any cross-domain hits.

---

## File System Status

- `Analysis/Results/` holds **459 files**; last hub_monitor inventory counted **1,057 files** hub-wide.
- Snapshot series are continuous and then stop hard:
  - `clinical_trials_snapshot_*.json` — daily 2026-03-15 → **2026-07-17**, then nothing.
  - `pubmed_recent_snapshot_*.json` — daily 2026-05-23 → **2026-07-17**, then nothing.
- `agent_state.json.bak_*` continues daily through 2026-08-13 — confirming the nightly job runs, just not the fetch half.
- The last hub_monitor run already flagged **827 result files older than 14 days**. That count is now materially higher and no longer meaningful as a signal; it needs a re-baseline after the pipeline restarts.
- Housekeeping: `.~lock.Diabetes_Research_Tracker.xlsx#` is present in the hub root — a stale LibreOffice lock file. The tracker itself was last modified 2026-07-17, the same day the pipeline stopped.

**Missing files:** none of the five target monitor files are absent. All five exist; four are stale.

---

## Clinical Trial Changes

Diff computed as `clinical_trials_snapshot_2026-06-17.json → clinical_trials_latest.json` (2026-07-17), a 30-day window. **This is history, not news** — it was already reported before the pipeline stopped. Included for completeness.

- **New trials: 62 · Removed: 17 · Status changes: 12 · Newly posted results: 0**
- Current corpus: **858 trials** — 269 RECRUITING, 321 COMPLETED, 151 NOT_YET_RECRUITING, 110 ACTIVE_NOT_RECRUITING, 7 ENROLLING_BY_INVITATION.
- Phase distribution: 136 PHASE3, 126 PHASE2, 16 PHASE2/3, 23 PHASE4.
- **52 Phase 3 trials are RECRUITING.**

### Notable new entrants in that window

| NCT | Sponsor | Phase | What it is |
|---|---|---|---|
| NCT07662135 / 07662044 / 07662109 / 07662213 / 07664553 | AstraZeneca | 3 | **Five-trial elecoglipron Phase 3 program launched simultaneously** (posted 2026-06-23) |
| NCT07670416 | Hoffmann-La Roche | 3 | Enicepatide, obesity/overweight |
| NCT07683026 | NIDDK | 2 | Platform trial in **Stage 1** diabetes: golimumab vs placebo |
| NCT07670650 | Univ. of Florida | 3 | PRISE — personalized response / immunologic surveillance of endogenous... |
| NCT07680673 | Encellin | 1 | ENCRT-103-hPI immune-protected encapsulated cell product |
| NCT07684144 | Amgen | 3 | Long-term extension |
| NCT07668336 | Eli Lilly | 3 | Orforglipron vs dulaglutide, **pediatric** |

The AstraZeneca elecoglipron block is the single most significant entry: a five-arm simultaneous Phase 3 launch signals a late-stage oral incretin competitor entering the field alongside orforglipron.

### Status changes worth noting
- `NCT01897688` ACTIVE_NOT_RECRUITING → **COMPLETED** — Phase 3 single-center islet transplantation.
- `NCT05866536` and `NCT05180591` (BCG revaccination, adult and pediatric T1D) both RECRUITING → ACTIVE_NOT_RECRUITING — enrollment closed on both arms of that program.
- `NCT06111586` (frexalimab, beta-cell preservation) RECRUITING → ACTIVE_NOT_RECRUITING — **readout-relevant; this program is now fully enrolled.**

### Key-organization Phase 3 status (as of 2026-07-17)

| Program | NCT | Status |
|---|---|---|
| Vertex VX-880 (zimislecel) | NCT06832410, NCT04786262 | RECRUITING (both) |
| Vertex VX-264 | NCT05791201 | ACTIVE_NOT_RECRUITING (Ph1/2) |
| Lilly baricitinib — beta-cell preservation | NCT07222332 | RECRUITING |
| Lilly baricitinib — delay of Stage 3 T1D | NCT07222137 | RECRUITING |
| Lilly retatrutide vs semaglutide | NCT06260722 | ACTIVE_NOT_RECRUITING |
| Lilly retatrutide vs placebo (T2D) | NCT06297603 | ACTIVE_NOT_RECRUITING |
| Lilly orforglipron master protocol | NCT06993792 | ACTIVE_NOT_RECRUITING |
| Novo CagriSema | NCT07564414 (R), NCT06534411, NCT07282613 | RECRUITING / ACTIVE / NOT_YET |

**No Vertex, Lilly, or Novo trial has posted new results since 2026-07-16.** Most recent results postings in the corpus: NCT04255433 (Lilly, tirzepatide vs dulaglutide MACE) 2026-07-08; NCT06340854 (Novo, weekly insulin switch) 2026-07-02; NCT06010004 (Lilly, orforglipron long-term safety) 2026-06-30.

---

## PubMed Highlights

From `pubmed_recent_latest.json` — 158 unique papers, 16 domains, 30-day lookback ending 2026-07-17.

### Cross-domain papers (12 of 158) — highest value per the doctrine

| PMID | Domains | Title |
|---|---|---|
| 42459945 | AI/ML · Closed Loop AP · **Health Equity** | A framework for assessing algorithmic discrimination risks in training data: a case of pediatric type 1 diabetes *(JAMIA Open, Aug 2026)* |
| 42419792 | orforglipron · retatrutide · CagriSema | Comparative effects of drugs for adults with overweight/obesity: systematic review and network meta-analysis *(BMJ, 2026-07-08)* |
| 42411999 | T1D Stem Cell Cure · T1D Immunotherapy | T1D driven by residual recipient T cells after hematopoietic cell transplantation *(Diabetes Care, 2026-07-07)* |
| 42437645 | GLP-1 Pharmacogenomics · orforglipron | Variant-specific pharmacophoric shifts in GLP-1R–orforglipron complexes |
| 42453334 | Biomarker · **LADA** | Harnessing noncoding RNAs for diabetes research and therapy |
| 42436543 | T2D Remission · Health Equity | Healthcare inequality dynamics in T2D across the COVID-19 pandemic |
| 42458730 / 42459212 | Microbiome · Multi-Omics | Multi-omic BMI response modelling; precision nutrition in Asian populations |
| 42452353 | GLP-1 · T2D Remission | Glucose-lowering therapy and myocardial work recovery after STEMI |
| 42458355 | AI/ML · Health Equity | Socioeconomic gradients in hypertension prevalence and management |
| 42394981 | orforglipron · retatrutide | Incretin-based therapies network meta-analysis |
| 42444567 | retatrutide · CagriSema | Medical treatments for obesity: what does the future have in store? |

**Three of these sit directly on Tier 1 territory.** PMID 42459945 is the strongest single item in the batch — it lands on Multi-Omics/AI (Tier 1 #1, #5) *and* Epidemiological/Health Equity (Tier 1 #6) simultaneously, and is a methods framework rather than a result, meaning it is directly reusable in our own pipelines. PMID 42419792 (BMJ network meta-analysis) triangulates all three key GLP-1 therapies in one paper — that is a citation anchor for any comparative claim we make.

### Key therapies
All eight tracked therapies (zimislecel, orforglipron, retatrutide, CagriSema, baricitinib, teplizumab, icodec, dapagliflozin) returned hits in the window. Domain volumes were flat and uniform across all 16 alert domains — no anomalous spikes or dropouts in the last successful run.

---

## Gap Analysis Summary

Source: `literature_gap_data.json` (2026-07-18) and `literature_gap_report.md` (rendered 2026-08-14 from that same stale input). 30 domains, 435 pairs, 372 ranked gaps. Validation level: **BRONZE** per the Research Doctrine — single analytical source, expert confirmation pending.

### Top 5 *meaningful* gaps (methodologically-distinct pairs excluded)

| # | Intersection | Gap Score | Joint Pubs | Tier 1 alignment |
|---|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 | — |
| 2 | Beta Cell Regen × **Health Equity** | 100.0 | 0 | **Tier 1 #6** (Epidemiological / disparity analysis) |
| 3 | Treg / CAR-T × **Health Equity** | 100.0 | 0 | **Tier 1 #6** |
| 4 | Glucokinase × **Health Equity** | 100.0 | 0 | **Tier 1 #6** |
| 5 | **Drug Repurposing** × **Health Equity** | 100.0 | 0 | **Tier 1 #4 + #6 — double hit** |

Runners-up: Gene Therapy × LADA (100.0, 0 pubs); Insulin Resistance × Islet Transplant (91.9, 1 pub).

**The pattern is the finding.** Four of the top five meaningful gaps share one axis: **Health Equity**. Health Equity has 1,990 publications since 2020 — enough volume that zero co-publication with four separate therapeutic domains is not a sampling artifact. Tier 1 #6 (Epidemiological Data Analysis, score 17/20) explicitly names "health equity analysis is under-resourced; disparity data exists but is rarely systematically analyzed." The gap analysis independently converged on the same conclusion the doctrine reached by expert judgment. **Two independent methods agreeing raises this from BRONZE toward SILVER on the specific claim that equity-crossed therapeutic analysis is under-published** — though the *individual pair* classifications remain BRONZE.

**Caveat [Likely]:** zero-joint-publication counts are the most terminology-fragile results in the whole analysis. "Health Equity" as a keyword string will miss papers using "disparities," "access," "socioeconomic," or "social determinants." Before treating any of these five as a real gap, each needs a manual PubMed check with synonym expansion — the gap report's own "How to Use" section says exactly this.

**Rank instability warning:** the raw `ranked_gaps` list puts *methodologically distinct* pairs (GWAS × Closed Loop, Drug Repurposing × CGM) at ranks 1–2. Only the curated `literature_gap_report.md` filters them out. Any downstream consumer reading the JSON directly rather than the report will get a misleading top-5.

---

## Breaking News (web check, last ~7 days)

Two items clear the "genuinely significant" bar; both are regulatory, not scientific.

1. **[Likely] Inhaled insulin (Afrezza) — FDA action for pediatric use, ~2026-08-12.** Reported as an FDA acceptance/approval for children and adolescents. Search snippets conflict on whether this is an acceptance or a full approval; **verify against the FDA press-announcement page directly before entering it in the tracker.** Relevant to Tier 2 #12 (Technology Accessibility).
2. **[Certain] Garzulys (insulin aspart-fsan) approved 2026-07-30** — first/among-first rapid-acting insulin biosimilars. Falls inside the pipeline blind spot; the trial monitor never saw it. Directly relevant to Tier 1 #6 and Tier 2 #12 (biosimilar entry is an access/pricing event).

Also noted, lower priority: **[Likely]** a prediabetes-remission framework paper (~2026-08-10) proposing a 10-point life-course prevention framework that explicitly prioritizes reducing inequities. This intersects the Health Equity gap cluster above and should be pulled once PubMed ingestion resumes.

**Nothing found** indicating new Phase 3 readouts from Vertex (zimislecel), Lilly (orforglipron/retatrutide/baricitinib), or Novo (CagriSema) in the last 7 days. Searches surfaced only 2025-vintage results for these programs.

---

## Recommended Actions

### P0 — restore the pipeline (everything else is blocked on this)

1. **Check Windows Task Scheduler history** for the task registered by `Analysis/Scripts/register_daily_task.ps1`. Determine whether it is disabled, failing, or simply not firing. This single check converts the [Likely] root cause to [Certain].
2. **Run the full local pipeline.** From `Analysis/Scripts/`:
   ```
   $env:NCBI_API_KEY="<your key>"     # 3 -> 10 req/sec; the gap step needs it
   python run_daily_local.py
   ```
   Expect 40–60 minutes, dominated by the 465 sequential PubMed queries in the gap step. Do **not** attempt this in the Cowork sandbox — the 45s process cap makes it structurally impossible, which is documented in the script's own header.
3. **If you only have time for one step, run PubMed first:** `python run_daily_local.py --only pubmed`. The 30-day rolling lookback means a run today recovers 18 Jul – 15 Aug in a single pass. Trials are cumulative and lose nothing by waiting; PubMed's window is the only thing that can permanently drop coverage.

### P1 — fix the silent-staleness failure mode

4. **Add a freshness guard to the render layer.** `improve_gap_analysis.py` should refuse to stamp a fresh "Generated" date when its input `literature_gap_data.json` is older than ~48 hours — or should stamp the *input* date instead of the *render* date. As written, the hub can report confidently from a corpus of arbitrary age. This is a Research Doctrine problem, not a cosmetic one.
5. **Add a staleness banner to the dashboards.** Same reasoning: any dashboard built from `clinical_trials_latest.json` should display that file's `metadata.generated`, not the build time.
6. **Re-baseline the 827-stale-file flag** after the pipeline restarts. That counter is currently noise.

### P2 — research actions

7. **Review PMID 42459945** (JAMIA Open, algorithmic discrimination in pediatric T1D training data) — three-domain cross-hit, directly reusable as methodology for Tier 1 #5 model work and Tier 1 #6 equity work. Highest-value single item in the last successful PubMed pull.
8. **Verify the Health Equity gap cluster before acting on it.** Run manual PubMed searches for the top 5 pairs using synonym-expanded equity terms (disparities / access / socioeconomic / social determinants). If the gaps survive synonym expansion, the Drug Repurposing × Health Equity pair is the strongest Tier 1 candidate in the whole matrix (hits doctrine areas #4 and #6 simultaneously). If they collapse, the gap-scoring keyword set needs revision — which is itself a valuable finding.
9. **Add to the tracker** (after independent verification): the AstraZeneca elecoglipron five-trial Phase 3 block (NCT07662135, NCT07662044, NCT07662109, NCT07662213, NCT07664553); NCT06111586 frexalimab status change to ACTIVE_NOT_RECRUITING; the Garzulys biosimilar approval. Note evidence level per doctrine — trial registry data is verifiable/GOLD; the web-sourced FDA items are BRONZE until confirmed against the FDA primary source.
10. **Clear the stale lock file** `.~lock.Diabetes_Research_Tracker.xlsx#` in the hub root.

---

## Confidence Summary

| Claim | Level | Basis |
|---|---|---|
| Pipeline fetch layer stopped 2026-07-17 | **Certain** | mtimes + in-file metadata + log directory, three independent agreeing sources |
| Render layer running on stale input | **Certain** | `literature_gap_report.md` render date 2026-08-14 vs. self-declared date range ending 2026-07-17 |
| ~800 unreviewed papers in the blind spot | **Likely** | Extrapolated from ~28 new papers/day in the last hub_monitor diff; actual count unknown until PubMed is re-run |
| Root cause is the local scheduled task | **Likely** | Consistent with script docstring + log pattern; not yet confirmed against Task Scheduler history |
| Trial counts and status changes as reported | **Certain** | Computed directly from snapshot JSON diffs |
| Health Equity is a systematically under-crossed axis | **Likely** | Two independent methods (bibliometric gap scoring + doctrine expert scoring) converge; individual pairs remain BRONZE pending synonym-expansion checks |
| Inhaled insulin pediatric FDA action ~2026-08-12 | **Likely** | Web search snippets conflict on acceptance vs. approval; needs FDA primary source |
| Garzulys biosimilar approval 2026-07-30 | **Certain** | Consistent across sources |

---

*Generated by the Diabetes Hub Monitor — automated review run, 2026-08-15. Read-only: no hub files were modified.*
*Doctrine compliance: all new claims carry evidence levels. Gap classifications remain BRONZE pending expert validation.*
