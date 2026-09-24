# Diabetes Research Hub — Monitor Report
**Run date:** 2026-09-24 (scheduled review)
**Prior report on file:** 2026-07-17 (hub_monitor.py has not been re-run in 69 days)

---

## File System Status

| File | Last modified | Age | Status |
|---|---|---|---|
| `hub_monitor_report.md` | 2026-07-17 | 69 days | **STALE** — hub_monitor.py hasn't run since Jul 17 |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | 69 days | **STALE** |
| `clinical_trials_latest.json` | 2026-07-17 | 69 days | **STALE** — see anomaly below |
| `pubmed_recent_latest.json` | 2026-09-23 | 1 day | Fresh |
| `literature_gap_data.json` | 2026-09-19 | 5 days | Fresh |
| `literature_gap_report.md` | 2026-09-23 | 1 day | Fresh |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 | 24 days | OK |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 | 193 days | Stale but doctrinal (not expected to change often) |

**Anomaly worth flagging:** `clinical_trials_latest.json` is stuck at the Jul 17 run even though dated snapshot files kept being generated after that (`clinical_trials_snapshot_2026-08-27.json`, `-08-28`, `-09-01`, `-09-06`). So the snapshot step is running intermittently, but whatever step promotes a snapshot to "latest" stopped updating on Jul 17 — and even the snapshot cadence itself broke down: daily through Jul 17, then a single scattered run on 8/27, 8/28, 9/1, 9/6, and nothing for the 18 days since. PubMed's pipeline, by contrast, is still running close to daily. Recommend checking `baseline_clinical_trials.py` / whatever cron entry drives it — this looks like a broken or disabled job, not routine staleness.

---

## Clinical Trial Changes
*Comparing the last two available snapshots: 2026-07-17 (the current "latest") vs. 2026-09-06 (newest snapshot on disk, 894 trials vs. 858 — still 18 days old itself).*

- **57 new trials** appeared, **21** dropped out of the tracked set, since Jul 17.
- **26 status changes**, notably:
  - **NCT07076199** (Novo Nordisk, Phase 3, weekly insulin icodec) — RECRUITING → ACTIVE_NOT_RECRUITING
  - **NCT07613307** (Eli Lilly, Phase 3, orforglipron) — NOT_YET_RECRUITING → RECRUITING
  - **NCT07664553** (AstraZeneca, Phase III) and **NCT07684144** (Amgen) — both moved NOT_YET_RECRUITING → RECRUITING (new Phase 3 activity from two orgs outside the "key" watchlist — may be worth adding AstraZeneca/Amgen to that list given Phase 3 diabetes activity)
  - **NCT06845202** (Alnylam, ALN-4324) — RECRUITING → ACTIVE_NOT_RECRUITING
- **0 trials show `has_results: true`** in the current dataset — either no key-org trial has posted results, or the results-posted field isn't being captured correctly by the scraper. Worth a spot check given the volume of completed Phase 3 trials in this list (Lilly/Novo have dozens of COMPLETED Phase 3 trials with no results flag set).
- **Phase 3 RECRUITING trials (as of Jul 17 data):** 52, including Vertex's two VX-880 trials (NCT06832410, NCT04786262), Lilly's baricitinib prevention trials (NCT07222332, NCT07222137), and Sanofi's teplizumab combination trial (NCT07088068).
- Because the underlying data is 69–83 days old, treat all of the above as directional, not current — a fresh pull is needed before acting on any of it.

---

## PubMed Highlights (fresh data, 2026-09-23, last 30 days)

- **154 unique papers**, 1,105 query matches across 16 domains queried.
- **17 cross-domain papers** — top ones:
  - PMID 42739778 — *Clinical Evolution, Outcomes, and Emerging Preservation Technologies in Pancreas [Transplant]* (T1D Stem Cell Cure × T1D Immunotherapy)
  - PMID 42626948 — *Gene-edited hypoimmune islets as a cure for type 1 diabetes* (T1D Stem Cell Cure × teplizumab)
  - PMID 42643804 — *Teplizumab in stage 2 type 1 diabetes – pediatric considerations* (T1D Immunotherapy × teplizumab)
  - PMID 42751099 — *Sustained weight loss exceeding 100 kg with sequential incretin-based therapy* (T2D Remission × retatrutide)
- **Key therapy mention counts (30-day window):** dapagliflozin 45 (5 papers), orforglipron 13 (5 papers), retatrutide 13 (5 papers), icodec 7 (5 papers), teplizumab 7 (5 papers), CagriSema 4 (4 papers), baricitinib 2 (2 papers), **zimislecel 0** — no recent PubMed activity on zimislecel at all, worth a manual check given it's a tracked cell-therapy candidate.

---

## Gap Analysis Summary
*Data from 2026-09-19/09-23, 30 domains, 435 pairs analyzed — fresh.*

Top curated gaps (Bronze validation — single analytical source, needs expert review):

1. **Beta Cell Regen × Health Equity** (gap 100, 0 joint pubs) — access/equity analysis of emerging cell therapies is essentially absent.
2. **Insulin Resistance × Islet Transplant** (gap 100, 1 joint pub) — graft survival implications of insulin resistance barely studied.
3. **Islet Transplant × Drug Repurposing** (gap 100, 0 joint pubs) — existing immunosuppressants as islet-protective agents unexplored computationally.
4. **Islet Transplant × Health Equity** (gap 100, 0 joint pubs) — access to transplant limited to select centers, no equity literature.
5. **Gene Therapy × LADA** (gap 100, 0 joint pubs) — no gene-therapy crossover work for LADA's autoimmune mechanism.

**Alignment with Tier 1 doctrine areas:** Gap #3 (Islet Transplant × Drug Repurposing) maps directly onto Tier 1 area #4, "Drug Repurposing Computational Screening" — this is the single gap on the list that's both high-scoring and already inside your declared highest-value lane. The other four sit closer to Tier 1 #6 (Epidemiological/Health Equity) and Tier 2 territory (gene therapy, transplant-specific work) rather than the core Tier 1 six.

---

## Breaking News

**FDA approved Eli Lilly's Onswik (insulin efsitora alfa-gobe)** — a once-weekly basal insulin for adults with type 2 diabetes — announced 2026-09-24 (today). This is a genuine Phase 3-backed approval, not routine trade press, and it's a direct competitor move against Novo Nordisk's insulin icodec (which just went RECRUITING → ACTIVE_NOT_RECRUITING in Phase 3 per the trial data above — Lilly landing approval while Novo's competing program shifts out of recruiting is a timing angle worth a note in the tracker). [HCPLive](https://www.hcplive.com/view/insulin-efsitora-alfa-onswik-gains-fda-approval-for-type-2-diabetes) | [Lilly investor release](https://investor.lilly.com/news-releases/news-release-details/us-food-and-drug-administration-fda-approves-lillys-onswiktm)

(Checked separately: Lilly's oral GLP-1 orforglipron/Foundayo obesity approval was April 1, 2026 — old news, already reflected in your PubMed therapy tracking, not a new item this cycle.)

---

## Recommended Actions

1. **Diagnose the clinical-trials pipeline** — `clinical_trials_latest.json` hasn't updated since Jul 17 despite scattered snapshots appearing through Sep 6, and even those stopped 18 days ago. Run `python baseline_clinical_trials.py` and check whatever promotes a snapshot to "latest."
2. **Re-run `hub_monitor.py`** — its own report is 69 days stale, so you're currently flying blind on file-level changes across the whole hub, not just clinical trials.
3. **Add a line to the tracker for NCT07076199** (icodec Phase 3, now ACTIVE_NOT_RECRUITING) and **Onswik's FDA approval** — both bear on the same insulin-icodec-vs-efsitora competitive story.
4. **Spot-check the `has_results` field** in the trial scraper — zero results-posted flags across 858 trials (many COMPLETED Phase 3) looks like a parsing gap, not reality.
5. **Consider adding AstraZeneca and Amgen** to the "key organizations" watchlist — both moved Phase 3 trials into RECRUITING since Jul 17.
6. **Manual check on zimislecel** — zero PubMed hits in 30 days for a tracked cell-therapy candidate; confirm whether that's expected (e.g., between publication cycles) or a query-term problem.
7. Gap analysis and PubMed pipelines are current — no action needed there beyond the Tier 1 alignment note above.

*This is a review-only run. No existing files were modified.*
