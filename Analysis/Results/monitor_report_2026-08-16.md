# Monitor Report — 2026-08-16

**Run type:** Automated review (read-only). No hub files were modified.
**Scan scope:** `Analysis/Results/`, `Analysis/Logs/`, `RESEARCH_DOCTRINE.md`, web check.
**Prior report:** `monitor_report_2026-08-15.md` — read and cross-checked. This report does **not** restate it.

---

## HEADLINE: Yesterday's report gave you a false negative. There *was* a major Phase 3 readout inside the blind spot.

Yesterday's monitor concluded: *"Nothing found indicating new Phase 3 readouts from Vertex, Lilly, or Novo in the last 7 days."* That was correct for a 7-day window and wrong as a signal about the blind spot.

Today's web check found **Lilly's TRIUMPH-2 and TRIUMPH-3 retatrutide confirmatory Phase 3 readouts, both dated 2026-07-23** — six days *after* the pipeline died, and never ingested by any hub layer.

| Trial | Date | Result | In hub? |
|---|---|---|---|
| TRIUMPH-2 (n=1,152, obesity + T2D) | 2026-07-23 | up to 20.8% weight loss, −1.6 pp HbA1c | **No** |
| TRIUMPH-3 (n=1,949, obesity + established CVD) | 2026-07-23 | up to 22.6% weight loss | **No** |
| ACHIEVE-2 (orforglipron vs dapagliflozin) | ADA 2026 | superiority at all doses | **No** |

**[Likely]** — consistent across multiple secondary sources; **not yet verified against Lilly's own investor release.** BRONZE until confirmed at the primary source.

**The lesson is about method, not about retatrutide.** A 7-day web check cannot audit a 30-day blind spot. As long as the pipeline is down, the web check window must equal the outage window, not the report cadence. Yesterday's search was scoped to the last 7 days and therefore structurally could not see 18 Jul – 09 Aug.

---

## 1. File System Status — day 30 of the outage

| Layer | Script | Last real data | Age | State |
|---|---|---|---|---|
| Clinical trials | `baseline_clinical_trials.py` | 2026-07-17 02:05 | **30 d** | STOPPED |
| PubMed alerts | `baseline_pubmed_alerts.py` | 2026-07-17 02:06 | **30 d** | STOPPED |
| Gap analysis (data) | `gap_analysis_daily.py` | 2026-07-18 03:11 | **29 d** | STOPPED |
| Hub monitor | `hub_monitor.py` | 2026-07-17 02:16 | **30 d** | STOPPED |
| Gap report (render) | `improve_gap_analysis.py` | 2026-08-15 03:12 | 1 d | RUNNING on stale input |
| Citation validation | `validate_citations.py` | 2026-08-15 03:11 | 1 d | RUNNING |
| Agent state | `agent_state.py` | 2026-08-15 03:14 | 1 d | RUNNING |

**Correction to a hypothesis I formed mid-run and discarded:** no hub file has been modified on 2026-08-16. I initially read that as "the render layer has now stopped too." It is not. Sandbox clock at scan time was **02:37 CDT**; the nightly Cowork-side jobs fire at ~03:07–03:16. **They have not missed today — today has not reached them yet.** [Certain] — `date` vs. the mtime distribution across 30 days of prior runs.

Snapshot series confirm the hard stop:
- `clinical_trials_snapshot_*.json` — daily 2026-03-15 → **2026-07-17**, then nothing.
- `pubmed_recent_snapshot_*.json` — same terminal date.
- `Analysis/Logs/` — last write `gap_analysis_2026-07-17.log`; steps 1–4 logs frozen at 2026-07-03.

**Report cadence** (unaffected by the data outage, both are Cowork-side):
- `monitor_report_*.md` — unbroken daily through 08-15.
- `iterate_run_report_*.md` — intermittent (missing 08-04, 08-05, 08-08, 08-14). Not alarming on its own, but worth knowing it is not a daily guarantee.

The `827 stale result files` flag in `hub_monitor_report.md` remains noise until the pipeline restarts. Ignore it.

---

## 2. Two monitoring defects found in the configuration itself

These are not data problems. They are bugs in how the hub looks at data, and they will silently corrupt every future run even after the pipeline is restored.

### Defect A — the Vertex program is invisible to therapy tracking (alias mismatch)

`pubmed_recent_latest.json` tracks 8 key therapies. `zimislecel` returns **0 papers, 0 total** — and has for weeks. Meanwhile `clinical_trials_latest.json` contains **three Vertex trials**, every one of them findable only under a code name:

| NCT | Status | Phase | n | Asset |
|---|---|---|---|---|
| NCT04786262 | RECRUITING | PHASE3 | 52 | VX-880 |
| NCT06832410 | RECRUITING | PHASE3 | 10 | VX-880 |
| NCT05791201 | ACTIVE_NOT_RECRUITING | PHASE1/2 | — | VX-264 (encapsulated) |

ClinicalTrials.gov indexes these as **VX-880**. PubMed increasingly indexes the same asset as **zimislecel**. Neither collector searches both strings, so the flagship T1D cure program registers as a zero on one side of the hub. **[Certain]** — grep of both files, shown above.

The reverse also holds: **elecoglipron** (5 Phase 3 trials, AstraZeneca) and **frexalimab** (Sanofi) appear in the trial data but are **not in the 8-therapy PubMed watchlist at all**. New Phase 3 assets are entering the trial registry without ever being added to the literature watchlist.

**Fix:** make the therapy list an alias table (`zimislecel|VX-880`, `orforglipron|LY3502970`, `retatrutide|LY3437943`, …) shared by both collectors, and add elecoglipron + frexalimab + enicepatide + UBT251.

### Defect B — `paper_count` is a cap, not a measurement. Do not trend on it.

The task brief asks for "domains with unusually high or low publication activity." That question **cannot be answered from this file as currently written**:

```
T1D Stem Cell Cure        papers= 10   pubmed_total= 17
Diabetes AI/ML            papers= 10   pubmed_total=260
Diabetes Microbiome       papers= 10   pubmed_total=186
Diabetes Biomarker        papers= 10   pubmed_total=166
T2D GLP-1 New             papers= 10   pubmed_total=167
   ... 13 of 16 domains sit at exactly 10 ...
Diabetes Drug Repurpose   papers=  8   pubmed_total=  8
Diabetes Epigenetics      papers=  5   pubmed_total=  5
GLP-1 Pharmacogenomics    papers=  1   pubmed_total=  1
```

Thirteen of sixteen domains return **exactly 10** because the collector caps retrieval at 10 per domain. `paper_count` measures the cap; only the three domains *below* the cap are reporting real volume. **Any volume trend built on `paper_count` is an artifact.** Use `total_count`. **[Certain]** — the distribution is self-evidently truncated.

On `total_count`, the real 30-day signal (17 Jun – 17 Jul) is:

| Domain | 30-day PubMed volume | Read |
|---|---|---|
| Diabetes AI/ML | 260 | saturated field |
| Diabetes Microbiome | 186 | saturated |
| T2D GLP-1 New | 167 | saturated |
| Diabetes Biomarker | 166 | saturated |
| Diabetes Health Equity | 72 | moderate |
| Diabetes Multi-Omics | 65 | moderate |
| Diabetes Gene Therapy | 42 | thin |
| Closed Loop AP | 38 | thin |
| T1D Immunotherapy | 25 | thin |
| **T1D Stem Cell Cure** | **17** | **thin — and this is the flagship domain** |
| LADA New Research | 12 | very thin |
| **Diabetes Drug Repurpose** | **8** | **very thin — Tier 1 #4** |
| **Diabetes Epigenetics** | **5** | **very thin — Tier 2 #9** |
| **GLP-1 Pharmacogenomics** | **1** | **near-empty** |

The bottom four are the interesting ones. Two of them (Drug Repurpose, Epigenetics) are named contribution areas in the doctrine, and both are producing under 10 papers a month worldwide. That is either a genuine open field or a query-specificity problem — and distinguishing those two is a cheap, high-value check.

*Minor:* file metadata declares `domains_queried: 16`; the task brief says 15 alert domains. The file is authoritative; the brief is stale.

---

## 3. Clinical Trial Changes — 30-day diff, not day-over-day

Prior reports diffed consecutive daily snapshots (1 new trial, 0 status changes — noise). Comparing across the full month gives the real picture.

**`clinical_trials_snapshot_2026-06-17.json` → `clinical_trials_latest.json` (2026-07-17): 813 → 858 trials**

| Change | Count |
|---|---|
| New trials | 62 |
| Removed | 17 |
| Status changes | 12 |
| New results posted | 1 |

**[Certain]** — computed directly from the two JSON files.

### Corpus composition (2026-07-17 baseline)

| Status | n | | Category | n |
|---|---|---|---|---|
| COMPLETED | 321 | | Diabetes Technology (Devices) | 236 |
| RECRUITING | 269 | | Recently Completed with Results | 321 |
| NOT_YET_RECRUITING | 151 | | T2D Novel Therapies (Ph 2–3) | 147 |
| ACTIVE_NOT_RECRUITING | 110 | | T1D Cure & Cell Therapy | 152 |
| ENROLLING_BY_INVITATION | 7 | | T1D Immunotherapy & Prevention | 76 |

152 trials carry a Phase 3 designation; **52 of those are actively RECRUITING.**

### New Phase 3 entrants in the window — beyond the AstraZeneca block

Prior reports flagged the five elecoglipron trials. The same window brought **five more Phase 3 programs that have not been mentioned in any monitor report to date**:

| NCT | Sponsor | Status | Note |
|---|---|---|---|
| NCT07670416 | Hoffmann-La Roche | RECRUITING | Enicepatide — Roche entering the incretin Phase 3 field |
| NCT07684144 | Amgen | NOT_YET_RECRUITING | Long-term extension trial |
| NCT07659574 | United Bio-Technology | NOT_YET_RECRUITING | UBT251, T2D |
| NCT07653477 | United Bio-Technology | NOT_YET_RECRUITING | UBT251, T2D (second) |
| NCT07668336 | Eli Lilly | NOT_YET_RECRUITING | Orforglipron vs dulaglutide |
| NCT07670650 | University of Florida | NOT_YET_RECRUITING | PRISE — immunologic surveillance of endogenous fn |

Two early-stage entries worth watching for the T1D cure thesis:

- **NCT07683026** — NIDDK **platform trial in Stage 1 diabetes**, golimumab vs. placebo, Phase 2. A platform design in Stage 1 is a structural change in how prevention gets tested, not just another arm.
- **NCT07680673** — **Encellin ENCRT-103-hPI**, Phase 1, immune-protected encapsulated cell construct. Direct competitive read on the encapsulation approach vs. Vertex's immunosuppression-dependent one.

### Status changes worth entering in the tracker

| NCT | Change | Sponsor | Why it matters |
|---|---|---|---|
| **NCT01897688** | ACTIVE_NOT_RECRUITING → **COMPLETED**, **results posted 2026-06-18** | Northwestern | Phase 3 islet transplantation. **Only new results posting in the whole 30-day window.** Directly feeds gap #7 below. |
| NCT06111586 | RECRUITING → ACTIVE_NOT_RECRUITING | Sanofi | Frexalimab; enrollment complete → readout clock started |
| NCT05180591 | RECRUITING → ACTIVE_NOT_RECRUITING | Mass General | Repeat BCG, pediatric |
| NCT05866536 | RECRUITING → ACTIVE_NOT_RECRUITING | Mass General | Repeat BCG, new-onset — **both BCG arms closed in the same window** |
| NCT05594563 | RECRUITING → ACTIVE_NOT_RECRUITING | Emily K. Sims | TADPOL polyamines |
| NCT07215312 | RECRUITING → ACTIVE_NOT_RECRUITING | Eli Lilly | LY3938577 |

**NCT01897688 is the single highest-value item in the trial data.** A completed Phase 3 islet transplantation trial *with posted results* is exactly the Tier 1 #3 ("flag trials with unexpected results") mandate, and it is the empirical anchor the Insulin-Resistance × Islet-Transplant gap (rank 7, only 1 joint publication) is missing.

---

## 4. PubMed Highlights — 158 papers, 12 cross-domain

Corpus covers ~17 Jun – 17 Jul 2026. **Nothing after 17 Jul has been ingested.**

### Cross-domain papers (highest value per doctrine Tier 1 #2)

**Three-domain hits (2):**

- **[42459945]** *A framework for assessing algorithmic discrimination risks in training data: a case of pediatric type 1 diabetes* — JAMIA Open, Aug 2026
  Domains: **Diabetes AI/ML × Closed Loop AP × Diabetes Health Equity**
  Flagged in prior reports and still the top item. Reusable as methodology for Tier 1 #5 (prediction models) and Tier 1 #6 (disparities) simultaneously.

- **[42419792]** *Comparative effects of drugs for adults with overweight or obesity: systematic review and network meta-analysis* — BMJ, 2026-07-08
  Domains: **orforglipron × retatrutide × CagriSema**
  **Not previously flagged.** A BMJ network meta-analysis putting all three lead assets in one comparative frame — the single most useful reference for cross-trial comparison work, and precisely the "cross-trial pattern analysis" the doctrine says does not exist at scale (Tier 1 #3). Pull the full text.

**Two-domain hits (10):** 42459212 (Microbiome × Multi-Omics), 42458730 (Microbiome × Multi-Omics), 42411999 (Stem Cell Cure × Immunotherapy — T1D driven by residual recipient T cells post-HCT, *Diabetes Care*), 42453334 (Biomarker × LADA), 42436543 (T2D Remission × Health Equity), 42437645 (GLP-1 Pharmacogenomics × orforglipron), 42444567 (retatrutide × CagriSema), 42458355 (AI/ML × Health Equity), 42394981 (orforglipron × retatrutide), 42452353 (T2D GLP-1 × T2D Remission).

### Key-therapy mentions

| Therapy | Papers | PubMed total |
|---|---|---|
| orforglipron | 5 | 10 |
| CagriSema | 5 | 6 |
| dapagliflozin | 5 | 52 |
| retatrutide | 4 | 4 |
| teplizumab | 4 | 4 |
| icodec | 3 | 3 |
| baricitinib | 2 | 2 |
| **zimislecel** | **0** | **0** ← see Defect A |

---

## 5. Gap Analysis Summary

`literature_gap_report.md` carries **"Generated: 2026-08-15"** while its own body declares **"Date range: 2020/01/01 to 2026/07/17."** The freshness signal is still false. 30 domains, 435 pairs.

### Top 5 under-researched intersections

| Rank | Pair | Gap Score | Joint Pubs |
|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | **0** |
| 2 | Beta Cell Regen × Health Equity | 100.0 | **0** |
| 3 | Treg / CAR-T × Health Equity | 100.0 | **0** |
| 4 | Glucokinase × Health Equity | 100.0 | **0** |
| 5 | Gene Therapy × LADA | 100.0 | **0** |
| 6 | Drug Repurposing × Health Equity | 100.0 | **0** |
| 7 | Insulin Resistance × Islet Transplant | 91.9 | 1 |

**Validation level: BRONZE** (single analytical source, keyword-based PubMed matching).

### Alignment with Tier 1 contribution areas

**Health Equity appears in 4 of the top 6 gaps.** Two independent methods now converge on it: bibliometric gap scoring, and the doctrine's own expert scoring (Tier 1 #6, Impact 5/5, *"health equity analysis is under-resourced"*).

The highest-value single target is **Drug Repurposing × Health Equity** — it hits **Tier 1 #4** (Drug Repurposing, Gap 5/5) and **Tier 1 #6** (Epidemiological/equity, Impact 5/5) simultaneously, with zero joint publications.

**But run the falsification test before committing.** Every one of these pairs scores exactly 100.0 with exactly 0 joint publications. A cluster of perfect zeros is as consistent with a terminology mismatch as with an open field — "health equity" as a literal string is a young term, while the same work publishes under *disparities*, *access*, *socioeconomic*, *social determinants*. If the gaps survive synonym expansion, this is the strongest Tier 1 candidate in the matrix. If they collapse, the gap-scoring keyword set is broken — which is itself a finding worth more than the gap.

Note the empirical convergence on rank 7: **NCT01897688 (Phase 3 islet transplantation) just posted results**, and Insulin Resistance × Islet Transplant has exactly 1 joint publication. Registry data for a gap with almost no literature is the cheapest evidence available in this report.

---

## 6. Breaking News

**Scope note:** search was widened to the full 18 Jul – 16 Aug outage window, not the 7-day report cadence. That widening is what surfaced item 1.

1. **[Likely] Retatrutide TRIUMPH-2 and TRIUMPH-3 Phase 3 readouts, 2026-07-23.** See headline. Five Phase 3 trials now complete; BLA reported as expected Q1 2027. Verify against Lilly's investor release before tracker entry.
2. **[Likely] Orforglipron ACHIEVE-2** — superiority over dapagliflozin at all doses in adults inadequately controlled on metformin, presented ADA 2026. Note the hub already holds NCT06010004 (orforglipron long-term safety, COMPLETED, results posted 2026-06-30) — the registry side is captured; the readout narrative is not.
3. **[Likely] Zimislecel regulatory submissions expected during 2026** to FDA / EMA / MHRA; holds RMAT + Fast Track + PRIME + ILAP. **No submission confirmed as filed.** If it files, the hub currently cannot see it (Defect A).
4. **[Likely] Tzield (teplizumab) — new pediatric indication**, accelerated approval reported 2026-06-12, ages 8–17 recently diagnosed Stage 3 T1D. Confirm against the FDA press announcement; this is a label expansion for an asset the hub tracks in 7 trials.
5. Carried forward from 08-15 and **still unverified**: inhaled insulin (Afrezza) pediatric FDA action ~2026-08-12 — sources conflict on acceptance vs. approval. Garzulys (insulin aspart-fsan) biosimilar approval 2026-07-30 — [Certain], consistent across sources.

**Not found:** any new Novo Nordisk CagriSema Phase 3 readout, or any Sana Biotechnology diabetes announcement, in the outage window.

---

## 7. Recommended Actions

### P0 — restore the pipeline (unchanged from 08-15, now 30 days overdue)

1. **Check Windows Task Scheduler history** for the task from `Analysis/Scripts/register_daily_task.ps1`. This one check converts the root cause from [Likely] to [Certain].
2. **Run the full local pipeline** from `Analysis/Scripts/`:
   ```
   $env:NCBI_API_KEY="<your key>"
   python run_daily_local.py
   ```
   40–60 min, dominated by 465 sequential PubMed queries. Cannot run in the Cowork sandbox (45 s process cap).
3. **If only one step: run PubMed first** — `python run_daily_local.py --only pubmed`. The 30-day rolling lookback means the window 18 Jul – 16 Aug is the only coverage that can be **permanently** lost. Trials are cumulative and lose nothing by waiting. **You are now at the edge of that window — a run today still recovers 18 Jul onward; a run after 17 Aug does not.**

### P1 — fix the monitoring defects (new today; these persist after restart)

4. **Build a therapy alias table** shared by both collectors: `zimislecel|VX-880`, `orforglipron|LY3502970`, `retatrutide|LY3437943`, `CagriSema|cagrilintide|semaglutide`, `frexalimab|SAR441344`. Add elecoglipron, frexalimab, enicepatide, UBT251 to the PubMed watchlist. Without this, the flagship T1D cure asset stays a zero.
5. **Raise or remove the 10-paper-per-domain retrieval cap**, or stop reporting `paper_count` as a volume metric. As written it silently answers a different question than the one asked.
6. **Add a freshness guard to the render layer** — `improve_gap_analysis.py` should stamp the *input* data date, not the render date, or refuse to render on input older than 48 h. Same for dashboards built from `clinical_trials_latest.json`. This is a doctrine problem, not cosmetics.
7. **Widen the monitor's web-check window to match the outage age**, not the report cadence. Today's headline is the direct cost of not doing this.

### P2 — research actions

8. **Pull full text: PMID 42419792** (BMJ network meta-analysis, orforglipron × retatrutide × CagriSema). Highest-value new literature item; directly enables the cross-trial comparison work under Tier 1 #3.
9. **Review PMID 42459945** (JAMIA Open, algorithmic discrimination in pediatric T1D training data). Three-domain hit; methodology reusable for Tier 1 #5 and #6.
10. **Falsify the Health Equity gap cluster.** Manual PubMed searches on the top 6 pairs with synonym-expanded terms (disparities / access / socioeconomic / social determinants). Decision rule stated in §5. This is the cheapest high-information action available.
11. **Pull the NCT01897688 results** (Northwestern Phase 3 islet transplantation, posted 2026-06-18) and use them to anchor the Insulin Resistance × Islet Transplant gap.
12. **Tracker entries** (evidence level per doctrine — registry data GOLD, web-sourced BRONZE until primary-source confirmed):
    - GOLD: NCT07670416 (Roche enicepatide Ph3), NCT07684144 (Amgen Ph3), NCT07659574 + NCT07653477 (UBT251 Ph3), NCT07668336 (Lilly orforglipron Ph3), NCT07683026 (NIDDK Stage-1 platform trial), NCT07680673 (Encellin Ph1), NCT01897688 status → COMPLETED + results 2026-06-18, NCT06111586 → ACTIVE_NOT_RECRUITING, NCT05180591 + NCT05866536 (BCG arms) → ACTIVE_NOT_RECRUITING
    - BRONZE: TRIUMPH-2/-3 readouts, ACHIEVE-2, Tzield pediatric indication, Afrezza pediatric action, Garzulys approval
13. **Clear the stale lock file** `.~lock.Diabetes_Research_Tracker.xlsx#` in the hub root. Still present.

---

## Confidence Summary

| Claim | Level | Basis |
|---|---|---|
| Pipeline fetch layer stopped 2026-07-17 (day 30) | **Certain** | mtimes + in-file `metadata.generated` + log directory — three independent agreeing sources |
| No hub file modified on 2026-08-16 — but jobs are *not* late | **Certain** | `find -newermt` + sandbox clock 02:37 CDT vs. 30-day mtime distribution at ~03:07–03:16 |
| Render layer stamping fresh dates on 30-day-old input | **Certain** | `literature_gap_report.md` render date 2026-08-15 vs. self-declared range ending 2026-07-17 |
| Trial counts, status changes, results postings as reported | **Certain** | Computed directly from snapshot JSON diffs (813 → 858) |
| `zimislecel` invisible to trial tracking; VX-880 present | **Certain** | Direct grep of both files; all 3 Vertex trials indexed only by code name (VX-880 ×2, VX-264 ×1) |
| `paper_count` is a retrieval cap, not a volume measure | **Certain** | 13 of 16 domains return exactly 10; distribution is truncated |
| elecoglipron/frexalimab absent from PubMed watchlist | **Certain** | 8-key `therapy_hits` dict enumerated in full |
| TRIUMPH-2/-3 readouts 2026-07-23 | **Likely** | Multiple consistent secondary sources; primary investor release not yet checked |
| ACHIEVE-2 orforglipron superiority | **Likely** | Conference-report sources; primary not checked |
| Tzield pediatric indication 2026-06-12 | **Likely** | FDA announcement referenced in search results but page not directly fetched |
| Zimislecel regulatory filing during 2026 | **Guessing** | Company guidance only; no confirmed filing found |
| Health Equity is a systematically under-crossed axis | **Likely** | Bibliometric gap scoring + doctrine expert scoring converge; individual pairs BRONZE pending synonym expansion |
| Root cause is the local scheduled task | **Likely** | Consistent with script docstring + log pattern; unconfirmed against Task Scheduler history |
| ~800 unreviewed papers in the blind spot | **Likely** | Extrapolated from ~28 new papers/day in the last hub_monitor diff |

---

*Generated by the Diabetes Hub Monitor — automated review run, 2026-08-16. Read-only: no hub files were modified.*
*Doctrine compliance: all new claims carry evidence levels. Gap classifications remain BRONZE pending expert validation.*
