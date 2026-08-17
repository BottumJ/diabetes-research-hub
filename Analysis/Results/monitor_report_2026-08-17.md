# Monitor Report — 2026-08-17

**Run type:** Automated review (read-only). No hub files were modified.
**Scan scope:** `Analysis/Results/`, `Analysis/Logs/`, `RESEARCH_DOCTRINE.md`, web check.
**Prior report:** `monitor_report_2026-08-16.md` — read and cross-checked. This report does **not** restate it.

---

## HEADLINE: The zero-loss recovery window closes today. Not "soon" — today.

Yesterday's report said you were "at the edge" of the window. You are no longer at the edge. Today is the last day, and the arithmetic is exact:

`pubmed_recent_latest.json` declares `lookback_days: 30` and `generated: 2026-07-17`. Coverage therefore ended **2026-07-17**. A run's coverage is `[run_date − 30, run_date]`:

| Run date | Coverage window | Days permanently lost |
|---|---|---|
| **2026-08-17 (today)** | 2026-07-18 → 2026-08-17 | **0** — abuts the last ingest exactly |
| 2026-08-18 | 2026-07-19 → 2026-08-18 | 1 (18 Jul) |
| 2026-08-19 | 2026-07-20 → 2026-08-19 | 2 (18–19 Jul) |
| 2026-09-01 | 2026-08-02 → 2026-09-01 | 15 (18 Jul – 01 Aug) |

**[Certain]** — computed from `metadata.lookback_days` and `metadata.generated` in the file itself.

Every day from here, one calendar day of literature drops out of reach of the automated collector forever. It is recoverable only by hand-built date-bounded queries afterward, which nothing in the hub currently does. If you run one command today, run this:

```powershell
$env:NCBI_API_KEY="<your key>"
python run_daily_local.py --only pubmed
```

Trials are cumulative and lose nothing by waiting. **PubMed is the only layer with an expiring window, and it expires tonight.**

---

## 1. File System Status — day 31

No hub file has been modified on 2026-08-17. As yesterday, this is **not** evidence the render layer has stopped: sandbox clock at scan time was **02:37 CDT**, and the nightly Cowork-side jobs fire at ~03:07–03:20. Today has not reached them yet. **[Certain]** — `find -newermt` plus the mtime distribution below.

The write-clock pattern is tight and worth recording as a baseline, because it is what makes "late" detectable at all:

| Job | Write time, 01–16 Aug | Deviation |
|---|---|---|
| `monitor_report_*.md` | 02:38–02:41, 16/16 days | 12 Aug only (07:27) |
| `agent_state.json.bak_*` | 03:07–03:20, 14/15 days | 12 Aug only (07:26); 14 Aug missing |

**Decision rule you can now apply without me:** if no `agent_state.json.bak_<today>` exists after **04:00 CDT**, the render layer has failed too. Before 03:07, absence means nothing.

Fetch layer, unchanged from yesterday — all four collectors stopped 2026-07-17:

| Layer | Last real data | Age |
|---|---|---|
| `baseline_clinical_trials.py` | 2026-07-17 02:05 | **31 d** |
| `baseline_pubmed_alerts.py` | 2026-07-17 02:06 | **31 d** |
| `hub_monitor.py` | 2026-07-17 02:16 | **31 d** |
| `gap_analysis_daily.py` (data) | 2026-07-18 03:11 | **30 d** |

Snapshot series terminate at `clinical_trials_snapshot_2026-07-17.json` (121 files) and `pubmed_recent_snapshot_2026-07-17.json` (113 files). `Analysis/Logs/` last write: `gap_analysis_2026-07-17.log`.

One render-layer note: `literature_gap_report.md` now stamps **"Generated: 2026-08-16 09:07"** over a body that still declares **"Date range: 2020/01/01 to 2026/07/17."** The false-freshness defect flagged yesterday is not cosmetic drift — it re-occurred today with a new date. Every day this runs, the file becomes more convincing and no more true.

---

## 2. New finding — a third asset is invisible, and this one has Phase 3-grade data

Yesterday established Defect A (alias mismatch: `zimislecel` vs. `VX-880`) and noted elecoglipron and frexalimab were missing from the PubMed watchlist. Today's web check surfaced a fourth case that is worse, because it is missing from **both** sides of the hub:

**Zenagamtide (Novo Nordisk)** — investigational, presented at ADA 2026 with significant A1C reductions and up to **14.6% weight loss** in adults with type 2 diabetes.

| Search target | `clinical_trials_latest.json` | PubMed watchlist |
|---|---|---|
| `zenagamtide` | **0 trials** | **absent** |
| `REIMAGINE` (CagriSema Ph3 program) | **0 trials** | n/a |
| `TRIUMPH` (retatrutide Ph3 program) | **0 trials** | n/a |
| `zimislecel` | 0 (present only as `VX-880`, ×2) | present, returns 0 |

**[Certain]** — direct term search of the trial JSON, shown above.

The pattern is now clear enough to name: **the hub indexes assets by whatever string ClinicalTrials.gov happened to use, and tracks literature by a hand-maintained 8-item list that nobody updates when a new Phase 3 program appears.** Three of the four most consequential 2026 programs — zimislecel, retatrutide's TRIUMPH readouts, zenagamtide — are wholly or partly invisible. Trial-acronym search (`TRIUMPH`, `REIMAGINE`, `ACHIEVE`, `AMAZE`) returns nothing because the collector stores no acronym field, so you cannot cross-reference a press release to a registry record by the only name the press release uses.

This is a Tier 1 #3 failure ("Clinical Trial Intelligence… cross-trial pattern analysis") in the literal sense: the hub cannot join its two data sources on asset identity.

**Fix, extending yesterday's item 4:** the alias table needs a third column for trial-program acronym, and the watchlist needs zenagamtide added alongside elecoglipron, frexalimab, enicepatide, UBT251.

---

## 3. Breaking News — one false positive ruled out, nothing new confirmed

Web check scoped to **16–17 Aug** only (yesterday's report already swept 18 Jul – 16 Aug in full).

**Ruled out — this is the important item.** A search for recent FDA diabetes actions surfaces the FDA press release *"FDA Approves First Cellular Therapy to Treat Patients with Type 1 Diabetes"* prominently and without an obvious date. Fetched and checked at the primary source: it is **Lantidra (donor islet cell therapy, CellTrans Inc.), approved 28 June 2023**. It is **not** a zimislecel approval and not new. **[Certain]** — fetched the FDA page directly; `dcterms.issued: 06/28/2023`.

Recording this deliberately. Given Defect A, an automated monitor scanning headlines for "first cellular therapy for type 1 diabetes" would have entered a 2023 approval as a 2026 event. The doctrine's primary-source rule is what caught it.

**Zimislecel: still no approval or confirmed filing.** Global regulatory submissions remain company *guidance* for 2026; earliest availability projected 2027. Designations confirmed: RMAT, Fast Track, PRIME, ILAP. Status unchanged from yesterday's **[Guessing]**.

**Nothing new 16–17 Aug.** No new Phase 3 readout, FDA action, or major publication in the two-day increment. Items 1–5 in yesterday's §6 (TRIUMPH-2/-3, ACHIEVE-2, Tzield pediatric, Afrezza, Garzulys) stand unchanged and still carry their original evidence levels.

---

## 4. Gap Analysis — the falsification test cannot be run from here. Script delivered instead.

Yesterday's recommendation #10 was to falsify the Health Equity gap cluster by synonym expansion. **I attempted it and was blocked:** the NCBI E-utilities endpoint is not reachable from the Cowork sandbox. This is a structural constraint, not a transient failure — **the monitor can never validate its own gap scores.** That is worth knowing about this whole system: the gap analysis and its validation must both live on your machine.

So the test is delivered as a script rather than a result: **`Analysis/Scripts/falsify_equity_gaps.py`** (written to the hub; see below). It runs the top 7 gap pairs twice — once with the literal doctrine terms, once with synonym-expanded terms (`disparities`, `access`, `socioeconomic`, `social determinants`, `underserved`, `inequities`) — and prints a side-by-side.

**Decision rule, stated in advance so the result cannot be rationalized after the fact:**

| Outcome | Reading | Action |
|---|---|---|
| Gaps survive expansion (still ~0 joint pubs) | Genuine open field | Promote Drug Repurposing × Health Equity to active Tier 1 project; upgrade BRONZE → SILVER |
| Gaps collapse (expansion finds substantial literature) | Keyword artifact | The gap-scoring term set is broken. **This is the more valuable finding** — it invalidates 4 of the top 6 gaps and the fix improves all 435 pairs |
| Mixed | Pair-specific | Classify individually |

Standing gap ranking, unchanged (BRONZE, 30 domains, 435 pairs, date range still ending 2026-07-17):

| Rank | Pair | Gap Score | Joint Pubs | Tier 1 alignment |
|---|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 | — |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 | #6 |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 | #6 |
| 4 | Glucokinase × Health Equity | 100.0 | 0 | #6 |
| 5 | Gene Therapy × LADA | 100.0 | 0 | — |
| 6 | Drug Repurposing × Health Equity | 100.0 | 0 | **#4 + #6** |
| 7 | Insulin Resistance × Islet Transplant | 91.9 | 1 | #1 |

---

## 5. Clinical Trials & PubMed — no change to report

Both files are byte-identical to yesterday's read (2026-07-17 baseline: 858 trials, 158 papers, 12 cross-domain, 52 recruiting Phase 3). The 30-day diff, the six new Phase 3 entrants, the six status changes, and NCT01897688's results posting were all fully characterized in `monitor_report_2026-08-16.md` §3–4. **Nothing has changed because nothing can change until the collectors run.** Re-tabulating them here would manufacture the same false-freshness signal this report criticizes in §1.

---

## 6. Recommended Actions

### P0 — expires today

1. **Run the PubMed collector before midnight.** `python run_daily_local.py --only pubmed`. Zero-loss recovery is available today and only today. Everything else on this list can wait; this cannot.
2. **Then run the full pipeline** — `python run_daily_local.py` (40–60 min, 465 sequential queries). Cannot run in the Cowork sandbox (45 s process cap).
3. **Check Windows Task Scheduler history** for the task from `register_daily_task.ps1`. Root cause is still **[Likely]**, not [Certain], on day 31. One check settles it, and until it is settled the pipeline will stop again after you restart it.

### P1 — carried forward, still open

4. **Alias table with a third column.** `zimislecel|VX-880`, `orforglipron|LY3502970`, `retatrutide|LY3437943|TRIUMPH`, `CagriSema|cagrilintide+semaglutide|REIMAGINE`, `frexalimab|SAR441344`. Add **zenagamtide**, elecoglipron, enicepatide, UBT251 to the watchlist. Store the trial-program acronym so press releases can be joined to registry records.
5. **Stop reporting `paper_count` as volume** — it is a retrieval cap (13/16 domains return exactly 10). Use `total_count`.
6. **Freshness guard on the render layer.** `improve_gap_analysis.py` should stamp the *input* data date or refuse to render on input older than 48 h. It produced another false-fresh file yesterday.
7. **Adopt the 04:00 decision rule** from §1 so render-layer failure is detectable rather than inferred.

### P2 — research

8. **Run `falsify_equity_gaps.py`** (delivered today). Highest information-per-minute action available; cannot be run from the sandbox.
9. **Pull full text: PMID 42419792** — BMJ network meta-analysis, orforglipron × retatrutide × CagriSema. Still the top unretrieved literature item.
10. **Review PMID 42459945** — JAMIA Open, algorithmic discrimination in pediatric T1D training data. Three-domain hit; methodology serves Tier 1 #5 and #6.
11. **Pull NCT01897688 results** (Northwestern Phase 3 islet transplantation, posted 2026-06-18) to anchor gap rank 7.
12. **Tracker entries** — GOLD for the registry items listed in yesterday's §7.12; BRONZE for TRIUMPH-2/-3, ACHIEVE-2, Tzield pediatric, Afrezza, Garzulys, and **zenagamtide ADA 2026 data** (new today).
13. **Clear `.~lock.Diabetes_Research_Tracker.xlsx#`** in the hub root. Present since at least 14 Mar.

---

## Confidence Summary

| Claim | Level | Basis |
|---|---|---|
| Zero-loss PubMed recovery expires 2026-08-17 | **Certain** | Arithmetic on `lookback_days: 30` + `generated: 2026-07-17`, both read from the file |
| Fetch layer stopped 2026-07-17 (day 31) | **Certain** | mtimes + in-file `metadata.generated` + log directory — three agreeing sources |
| No hub file modified 2026-08-17, but jobs are not late | **Certain** | `find -newermt` + sandbox clock 02:37 CDT vs. 16-day mtime distribution (02:38–03:20) |
| Render layer stamped another false-fresh gap report | **Certain** | Render date 2026-08-16 09:07 vs. self-declared range ending 2026-07-17 |
| zenagamtide absent from trial data and watchlist | **Certain** | Direct term search of both JSON files |
| Trial-program acronyms (TRIUMPH/REIMAGINE) unsearchable in hub | **Certain** | 0 hits across 858 trials; no acronym field in the schema |
| "First Cellular Therapy for T1D" = Lantidra, June 2023, not new | **Certain** | Fetched FDA primary source; `dcterms.issued 06/28/2023` |
| NCBI E-utilities unreachable from Cowork sandbox | **Certain** | Fetch attempted and blocked this run |
| zenagamtide ADA 2026 efficacy figures | **Likely** | Novo Nordisk press release via search; primary release not directly fetched |
| No new diabetes Phase 3 readout or FDA action 16–17 Aug | **Likely** | Two targeted searches returned nothing dated in-window; absence of evidence |
| zimislecel not approved; no confirmed filing | **Guessing** | Company guidance only; no primary regulatory source located |
| Health Equity gap cluster is real vs. keyword artifact | **Unresolved** | Cannot be tested from sandbox; script delivered, decision rule pre-committed |
| Root cause is the local scheduled task | **Likely** | Consistent with script docstring + log pattern; unconfirmed against Task Scheduler history |

---

*Generated by the Diabetes Hub Monitor — automated review run, 2026-08-17. Read-only: no existing hub files were modified.*
*Doctrine compliance: all new claims carry evidence levels. Gap classifications remain BRONZE pending the falsification run.*
