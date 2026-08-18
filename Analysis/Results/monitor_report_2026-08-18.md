# Monitor Report — 2026-08-18

**Run type:** Automated review (read-only). No existing hub files were modified.
**Scan scope:** `Analysis/Results/`, `Analysis/Logs/`, `Analysis/Scripts/`, `RESEARCH_DOCTRINE.md`, web check.
**Prior report:** `monitor_report_2026-08-17.md` — read in full and cross-checked. This report does **not** restate it.

---

## HEADLINE: The window closed unused. 18 July 2026 is now permanently outside automated reach.

Yesterday's report was correct and it did not work. The P0 was to run one command before midnight. `pubmed_recent_latest.json` still reads `generated: 2026-07-17T02:06:39`, and no file anywhere in the hub has been modified on 2026-08-18. **[Certain]** — `find -newermt` returns 0 files; in-file metadata unchanged.

So the arithmetic has now resolved to the losing branch:

| Run date | Coverage window | Days permanently lost |
|---|---|---|
| 2026-08-17 (yesterday, not taken) | 2026-07-18 → 2026-08-17 | 0 |
| **2026-08-18 (today)** | **2026-07-19 → 2026-08-18** | **1 — 18 Jul** |
| 2026-08-25 | 2026-07-26 → 2026-08-25 | 8 |
| 2026-09-01 | 2026-08-02 → 2026-09-01 | 15 |

One day is gone. That is the smallest loss still available — **the cost of running the collector today is one day of literature; the cost of running it a week from now is eight.** The loss is linear and it is one day per day, so this report will say the same thing tomorrow with a bigger number. Nothing else in this document is more urgent than the command in §6.1.

Worth stating plainly: the collector stopping was a failure. The window closing is a *second, separate* failure, and it is the one that is repeating. Yesterday's report had the right answer 24 hours in advance and the pipeline still lost a day. That gap between "monitor identifies the action" and "action is taken" is now the binding constraint on this hub, not any defect in the code.

---

## 1. File System Status — day 32, and yesterday's decision rule just produced a false positive

**Fetch layer**, unchanged. All four collectors stopped 2026-07-17. **[Certain]** — mtimes, in-file `metadata.generated`, and `Analysis/Logs/` agree.

| Layer | Last real data | Age |
|---|---|---|
| `baseline_clinical_trials.py` | 2026-07-17 02:05 | **32 d** |
| `baseline_pubmed_alerts.py` | 2026-07-17 02:06 | **32 d** |
| `hub_monitor.py` | 2026-07-17 02:16 | **32 d** |
| `gap_analysis_daily.py` (data) | 2026-07-18 03:11 | **31 d** |

Snapshot series still terminate at `clinical_trials_snapshot_2026-07-17.json` (121 files) and `pubmed_recent_snapshot_2026-07-17.json` (113 files). `Analysis/Logs/` last write remains `gap_analysis_2026-07-17.log`.

### The 04:00 rule is wrong, and today is the proof case

Yesterday's §1 proposed: *"if no `agent_state.json.bak_<today>` exists after 04:00 CDT, the render layer has failed too."*

Applying it as written: sandbox clock at this scan is **06:37 CDT**. No `agent_state.json.bak_2026-08-18`, no `monitor_report_2026-08-18.md` prior to this one. Past 04:00, both absent → rule fires → "render layer has failed."

**The rule is firing incorrectly.** This report — the *first* link in the nightly chain — is being written at 06:37, not at its usual 02:38–02:41. The downstream `agent_state` job runs 25–40 minutes after the monitor, so its absence at 06:37 is fully explained by the chain starting late, not by the chain being dead. The rule assumed the chain's start time was fixed and inferred failure from a wall-clock deadline. It isn't fixed:

| Date | monitor_report write | agent_state.bak write | Chain lag |
|---|---|---|---|
| 01–11 Aug, 13–17 Aug | 02:38–02:41 | 03:07–03:23 | ~25–40 min |
| **12 Aug** | **07:27** | **07:26** | chain ran ~4.8 h late, completed normally |
| 14 Aug | 02:39 | *(absent)* | — |
| **18 Aug (today)** | **06:37** | pending | — |

12 August is the precedent: the whole chain shifted ~4.8 hours and completed fine. Today matches that pattern, not a failure pattern. **[Likely]** — the render layer is late, not broken; confirmable by checking whether `agent_state.json.bak_2026-08-18` appears by ~07:15.

**Revised rule — key off relative lag, not absolute clock:**

> The render layer has failed if no `agent_state.json.bak_<today>` exists **60 minutes after this report's own mtime**. Absolute wall-clock deadlines produce false positives on late-chain days (12 Aug, 18 Aug).

I am flagging this because a monitoring rule that cries failure on a merely-late run is worse than no rule: it trains you to ignore it, on exactly the days when the signal matters. Recommendation 7 from yesterday should be adopted in this revised form, not as originally written.

### The false-freshness defect recurred again

`literature_gap_report.md` now stamps **"Generated: 2026-08-17 03:13"** over a body that still declares **"Date range: 2020/01/01 to 2026/07/17."** Third consecutive day. **[Certain]** — both strings read from the file. The render date has advanced 32 days past its input and the document says nothing about it.

---

## 2. Primary finding — the hub missed an FDA approval *while fully operational*. The defect is schema, not staleness.

This is the most consequential item in this report, and it changes what the last 32 days mean.

**Foundayo™ is the brand name of orforglipron. The FDA approved it on 1 April 2026.** **[Certain]** — fetched Lilly's investor release directly; dateline "INDIANAPOLIS, April 1, 2026", document code `CMAT-04552 04/2026`.

Search the hub for it:

| Term | `clinical_trials_latest.json` | `pubmed_recent_latest.json` |
|---|---|---|
| `Foundayo` | **0** | **0** |
| `orforglipron` | 12 | 13 |

Now the part that matters. **1 April 2026 is 107 days before the collectors stopped.** The hub was running nightly, without fault, for over three months after this approval. `orforglipron` is on the 8-item `KEY_THERAPY_TERMS` watchlist and returned 13 PubMed hits. The drug was tracked. The approval was still invisible.

That severs two explanations that have been running together in these reports:

- "We are missing things because the data is 32 days stale" — **insufficient**. This was missed during full operation.
- "We are missing things because the hub cannot represent the event class" — **supported**. Restarting the collectors tomorrow would not have caught this and will not catch the next one.

### Root cause: there is no regulatory-event collector, and there never was

I searched all 69 Python scripts in `Analysis/Scripts/` for any FDA or regulatory data source — `fda.gov`, `accessdata`, `drugsfda`, `openfda` — and for any filename matching `fda|approv|regulat|label`. **Zero hits in both.** **[Certain]** — grep across the full script directory.

The hub has three collectors: registry trials, PubMed literature, and file-change monitoring. **Regulatory approval is not a category the system can observe.** It surfaces only by accident, when a web check happens to run the right query — which is how both this item and yesterday's Lantidra false-positive came to light.

### Brand names are a fourth alias class, and the knowledge is already in the codebase — as a comment

Yesterday's §2 identified three alias classes: generic name, development code, trial-program acronym. Foundayo is a fourth: **marketed brand name**. This is the class that press releases, FDA announcements, and clinical practice actually use — precisely the sources where approvals appear.

The watchlist source shows the author already knew:

```python
KEY_THERAPY_TERMS = [
    "zimislecel", "orforglipron", "retatrutide", "CagriSema",
    "baricitinib", "teplizumab",
    "icodec",        # Awiqli / insulin icodec
    "dapagliflozin", # generic now approved
]
```

`Awiqli` is a brand name, written as a comment on line 62. Comments are not searched. The hub knows the alias and cannot use it. Extend the alias table to four columns — generic | development code | trial-program acronym | **brand name** — and populate at minimum:

| Generic | Dev code | Program acronym | Brand |
|---|---|---|---|
| orforglipron | LY3502970 | ACHIEVE / ATTAIN | **Foundayo** (FDA 2026-04-01) |
| zimislecel | VX-880 | — | — |
| retatrutide | LY3437943 | TRIUMPH / TRANSCEND | — |
| CagriSema | cagrilintide+semaglutide | REIMAGINE | — |
| insulin icodec | NN1436 | ONWARDS | **Awiqli** |
| teplizumab | PRV-031 | PROTECT | **Tzield** |
| insulin aspart-fsan | — | — | **Garzulys** (FDA 2026-07-30) |
| frexalimab | SAR441344 | — | — |

Doctrine framing: this is a **Tier 1 #3** failure ("Clinical Trial Intelligence — automated monitoring… flag trials with unexpected results"). An approval is the most consequential status change a tracked asset can undergo, and it is the one event class the hub structurally cannot see.

---

## 3. Clinical Trials & PubMed — baseline restated only where load-bearing

Both files are byte-identical to yesterday's read. Re-tabulating the 30-day diff would manufacture the false-freshness signal §1 criticizes. Baseline, for reference only:

| Metric | Value (2026-07-17 baseline) |
|---|---|
| Total trials | 858 |
| RECRUITING / COMPLETED / NOT_YET / ACTIVE_NOT | 269 / 321 / 151 / 110 |
| Phase 3, exact `PHASE3` (any status) | 136 |
| Phase 3, incl. `PHASE2, PHASE3` | 152 |
| **Phase 3 + RECRUITING** (46 exact + 6 combined) | **52** |
| Trials with results posted | 322 (most recent: NCT05086445, 2026-07-16) |
| Unique PubMed papers | 158 |
| Cross-domain papers | 12 |

Key-sponsor coverage: Lilly 33, Novo Nordisk 28, Vertex 3 (NCT06832410 + NCT04786262 Phase 3 RECRUITING; NCT05791201 VX-264 Ph1/2 active), **Sana Biotechnology 0** — Sana is a named watch organization with zero registry coverage, unchanged and still unexplained.

One correction to carry forward: `domain_results` reports `paper_count` and `total_count`, and `paper_count` is a retrieval cap (`max_results=10`, and 5 for therapy terms), not a volume measure. Yesterday's recommendation 5 stands. Note the therapy searches are capped at **5**, tighter than the 10 for domains — so therapy volume is the least reliable number in the file.

---

## 4. Gap Analysis — unchanged, still BRONZE, still untestable from here

Data date range still ends 2026-07-17. 30 domains, 435 pairs, 372 ranked. Top 5 meaningful gaps against Doctrine Tier 1:

| Rank | Pair | Gap Score | Joint Pubs | Tier 1 alignment |
|---|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 | — |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 | #6 Epidemiological / disparities |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 | #6 |
| 4 | Glucokinase × Health Equity | 100.0 | 0 | #6 |
| 5 | Gene Therapy × LADA | 100.0 | 0 | — |
| 6 | Drug Repurposing × Health Equity | 100.0 | 0 | **#4 + #6 — strongest alignment** |
| 7 | Insulin Resistance × Islet Transplant | 91.9 | 1 | #1 Multi-omics |

Four of the top six involve Health Equity, whose individual volume is only 1,990 — 10th-smallest of the 30 domains, and roughly 40× smaller than Prevention/DPP (80,135). A cluster this concentrated in one low-volume domain is the signature of a **term-coverage artifact** at least as much as a real gap. Note the same concern applies to the other domains in the top 7: Treg/CAR-T (953), Glucokinase (854), Drug Repurposing (609), LADA (582) and Islet Transplant (248) are the 6th, 5th, 3rd, 2nd and 1st smallest domains respectively. **Every pair in the top 7 is composed of at least one bottom-10 domain.** That is what a geometric-mean gap score is expected to do to sparse domains, and it is the reason these remain BRONZE. `falsify_equity_gaps.py` (delivered yesterday, 10,230 bytes, present and unrun) tests exactly this. The pre-committed decision rule in yesterday's §4 stands unchanged — run it before promoting any of these to an active project.

Reminder of a structural fact: NCBI E-utilities is unreachable from the Cowork sandbox, so **the monitor can never validate its own gap scores.** That work only happens on your machine.

---

## 5. Breaking News — three items, one of them an approval the hub should have had

Web check scoped 11–18 Aug, plus targeted verification of the §2 finding.

1. **Foundayo (orforglipron) — FDA approved 2026-04-01 for obesity/overweight.** ATTAIN-1: 12.4% mean weight loss at top dose (efficacy estimand, n=3,127). **[Certain]** — Lilly primary source fetched. Not new news; new *to the hub*, which is the point of §2.
2. **Orforglipron T2D filing + ACHIEVE program.** Lilly reported ACHIEVE-3 as a head-to-head win over **oral semaglutide** on primary and all key secondary endpoints; ACHIEVE-2 and ACHIEVE-5 met primary endpoints vs. dapagliflozin and vs. placebo added to insulin glargine. T2D submission filed under a Commissioner's National Priority Review Voucher. **[Likely]** — company release via search; ACHIEVE-3 not independently verified. Yesterday's report tracked ACHIEVE-2 only; **ACHIEVE-3 and ACHIEVE-5 are new to the hub.**
3. **Retatrutide TRANSCEND-T2D-1** — n=537, ~85% treatment-naive, HbA1c reduction up to 2.0% and weight loss up to 16.8% at 40 weeks, no plateau. **[Likely]** — secondary sources only; distinct from the TRIUMPH-2/-3 readouts already logged. Note `TRANSCEND` returns 2 hits in the trial JSON but `TRIUMPH` returns 0 — the acronym-field defect again.

Also surfaced, not yet in the hub, lower confidence: **amycretin** (Novo, Phase 3 enabling data), **ecnoglutide** (EECOH-1 Phase 3, published). Both return **0 hits** in both hub files. **[Guessing]** on significance — logged so they are not rediscovered as "new" in a future run.

No new item in the 17–18 Aug increment specifically.

---

## 6. Recommended Actions

### P0 — cost increases by one day of literature every day

1. **Run the PubMed collector today.**
   ```powershell
   $env:NCBI_API_KEY="<your key>"
   python run_daily_local.py --only pubmed
   ```
   Loss is 1 day if run today, 8 if run 25 Aug. Trials are cumulative and lose nothing by waiting; PubMed does not.
2. **Then the full pipeline** — `python run_daily_local.py` (40–60 min, 465 sequential queries; cannot run in the Cowork sandbox).
3. **Check Windows Task Scheduler history** for the `register_daily_task.ps1` task. This is day 32 and root cause is still **[Likely]**, not [Certain]. Until it is settled, restarting the pipeline restarts a pipeline that will stop again.

### P1 — new today

4. **Add a regulatory-event collector.** The gap in §2 is not fixable by alias work alone. openFDA's drug label and NDA endpoints are free and unauthenticated; a nightly query for the tracked asset list would have caught Foundayo on 1 April. This is the single highest-value *new* script the hub could gain, and it is small.
5. **Extend the alias table to four columns** (generic | dev code | program acronym | **brand**) and seed it from the table in §2. Move `Awiqli` out of a code comment and into data.
6. **Adopt the revised render-layer rule** from §1 — 60 minutes after this report's mtime, not 04:00 wall clock. The original fires falsely on late-chain days.

### P1 — carried forward, still open

7. Freshness guard on `improve_gap_analysis.py` — stamp the input data date or refuse to render on input older than 48 h. Third consecutive false-fresh file.
8. Stop reporting `paper_count` as volume; use `total_count`. Note therapy searches cap at 5, domains at 10.
9. Add to the PubMed watchlist: **zenagamtide, elecoglipron, enicepatide, UBT251, frexalimab, amycretin, ecnoglutide** — all currently returning 0 PubMed hits, several with double-digit trial presence.

### P2 — research

10. **Run `falsify_equity_gaps.py`.** Still the highest information-per-minute action available and still unrun. Four of the top six gaps depend on its outcome.
11. **Pull full text: PMID 42419792** — BMJ network meta-analysis covering orforglipron × retatrutide × CagriSema. Top unretrieved literature item; now more relevant given ACHIEVE-3.
12. **Review PMID 42459945** — JAMIA Open, algorithmic discrimination in pediatric T1D training data. Only 3-domain hit in the corpus; serves Tier 1 #5 and #6.
13. **Pull NCT01897688 results** (Northwestern Phase 3 islet transplantation) to anchor gap rank 7.
14. **Tracker entries** — GOLD: Foundayo FDA approval 2026-04-01 (primary source verified). BRONZE: ACHIEVE-3/-5, TRANSCEND-T2D-1, amycretin, ecnoglutide, plus items carried from yesterday.
15. **Clear `.~lock.Diabetes_Research_Tracker.xlsx#`** in the hub root. Present since 14 Mar — five months.

---

## Confidence Summary

| Claim | Level | Basis |
|---|---|---|
| No hub file modified 2026-08-18; PubMed collector not run | **Certain** | `find -newermt` = 0 files; `metadata.generated` unchanged |
| 18 July 2026 now permanently outside collector reach | **Certain** | Arithmetic on `lookback_days: 30` + today's date |
| Fetch layer stopped 2026-07-17 (day 32) | **Certain** | mtimes + in-file metadata + log dir — three agreeing sources |
| Foundayo = orforglipron, FDA approved 2026-04-01 | **Certain** | Lilly investor release fetched directly; dateline + doc code |
| `Foundayo` returns 0 hits in both hub data files | **Certain** | Direct term search of both JSONs |
| Approval predates collector failure by 107 days | **Certain** | 2026-04-01 vs. 2026-07-17 |
| No regulatory/FDA collector exists in the hub | **Certain** | grep for `fda.gov\|accessdata\|drugsfda\|openfda` across 69 scripts = 0 |
| `Awiqli` present only as a code comment | **Certain** | `baseline_pubmed_alerts.py` line 62 |
| Render layer stamped a third false-fresh gap report | **Certain** | Render date 2026-08-17 vs. self-declared range ending 2026-07-17 |
| Trial/PubMed baselines (858 / 52 Ph3 recruiting / 158 / 12) | **Certain** | Recomputed from the JSONs this run and re-verified against source |
| Every top-7 gap pair contains a bottom-10-volume domain | **Certain** | Ranked `individual_counts` from `literature_gap_data.json` |
| Yesterday's 04:00 rule produces a false positive today | **Likely** | Chain-lag pattern across 16 days + 12 Aug precedent |
| Render layer is late, not failed | **Likely** | Same; confirmable by ~07:15 today |
| ACHIEVE-3 beat oral semaglutide; T2D filing submitted | **Likely** | Company release via search; not independently verified |
| TRANSCEND-T2D-1 efficacy figures | **Likely** | Secondary sources only |
| Health Equity gap cluster real vs. keyword artifact | **Unresolved** | Untestable from sandbox; script delivered, decision rule pre-committed |
| Root cause is the local scheduled task | **Likely** | Consistent with script docstring + log pattern; Task Scheduler history unchecked, day 32 |
| Significance of amycretin / ecnoglutide | **Guessing** | Logged to prevent future false-novelty |

---

*Generated by the Diabetes Hub Monitor — automated review run, 2026-08-18. Read-only: no existing hub files were modified.*
*Doctrine compliance: all new claims carry evidence levels. Gap classifications remain BRONZE pending the falsification run.*
