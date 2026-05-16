# Daily Iteration Run Report — 2026-05-16 (Saturday)

## Summary
Drained one outstanding work-queue item (`verify_filter_in_pipeline`), began the
new ongoing `claims_check_batch` pass (12 papers deep-vetted), credibility
sweep clean, pipeline rebuilt cleanly (41/41 [OK]).

## Work-queue items resolved
1. **Item 19 (verify_filter_in_pipeline, priority 4)** — verified
   `build_research_paths.py` correctly filters the three known dpc=1
   dose-fragment artifacts on every load:
   `Filtered 3 dpc=1 dose-fragment artifact path(s): ['metformin -> inflammation', 'pioglitazone -> inflammation', 'atorvastatin -> T2D']`.
   Pipeline output: 44 paths processed, 22 validated, 5 partially validated,
   1 unvalidated. No false negatives observed. `DOSE_FRAGMENT_PATTERNS` /
   `MECHANISM_KEYWORDS` do not need tuning. Item removed from queue.

## Claims-checked deep vet (new ongoing pass)
A batch of 12 recent VETTED papers that have PMC full text available were
re-examined beyond PMID verification. Full-text was scanned for red-flag
patterns: zero-event language, absolute-cure / curative claims, "achieves"
cure claims, and hype framing (miracle / breakthrough / revolutionary).

| PMID | Year | PMC | Title (abbrev.) | Result |
| --- | --- | --- | --- | --- |
| 41618067 | 2026 | PMC12901800 | AI Medical Devices for DR Screening | clean |
| 41827917 | 2026 | PMC12984146 | GENEPEDIAB atypical-diabetes characterization | clean |
| 40032831 | 2025 | PMC11876343 | Plasma proteomic markers, polygenic risk | clean |
| 40272935 | 2025 | PMC12278794 | Functional/mechanistic basis of clinical-success drug | clean |
| 40366501 | 2025 | PMC12078402 | Disparities in diabetes-in-pregnancy / SDoH | clean |
| 40464081 | 2025 | PMC12169077 | Health economics of insulin therapy | clean |
| 40573322 | 2025 | PMC12196043 | Dorzagliatin in vivo PK-PD / DDI study | clean |
| 40650745 | 2025 | PMC12423256 | Verapamil + low-dose anti-mouse thymoglobulin (preclinical) | clean |
| 41567805 | 2025 | PMC12815805 | Regulatory T-cell dysfunction & immunotherapy review | **FLAGGED (review language)** |
| 38783768 | 2024 | PMC11116947 | Dorzagliatin drug-development overview | clean |
| 39525461 | 2024 | PMC11545964 | Diabetes CV outcomes trials / racial-ethnic minorities | clean |
| 39629068 | 2024 | PMC11612564 | Glucokinase activator overall safety | clean |

**FLAGGED — PMID 41567805**: review uses "revolutionary" framing for
epigenetic-editing T-cell therapies and notes the "absence of curative
interventions." Not a fabricated claim and not an efficacy overstatement;
flagged so downstream dashboards do **not** echo this framing as authorial
position. Note appended to `papers[41567805].issues_found`.

All 12 papers now have `claims_checked = True` and `claims_checked_date = 2026-05-16`.

State counts after this batch:
- Papers with `claims_checked = True`: 110 / 280 (39.3%)
- VETTED: 267, FLAGGED: 13, UNVETTED: 0
- Eligible for full-text claims-check remaining: ~50

## Credibility sweep (Step 4)
Greppped all `Analysis/Scripts/*.py`:
- PMIDs ≥ 42000000 hard-coded in scripts: **none** ✓
- "zero SAEs" / "zero rejection": **none** ✓
- "achieves cure" / "achieves complete cure": **none** ✓
- "curative" hits: **1**, in `verify_before_deploy.py:14` — guardrail regex itself ✓

## Pipeline (Step 5)
`python Analysis/Scripts/run_quality_improvements.py` — all 41 improvements
report **[OK]**. 34 dashboards rebuilt and post-processed.

## Step 2 (weekly PubMed scan) — skipped
Today is Saturday. Weekly scan triggers on Mondays only.

## Step 3 (re-extract / re-cluster) — skipped
No new papers added to state during today's run.

## Queue state for next run
- 20 items (priority-ordered)
- Top: priority-1 stale `manual_cleanup_required` (`.git/index.lock` / `HEAD.lock` /
  `objects/maintenance.lock`) — still requires PowerShell remediation by user;
  unpushed commits continue to accumulate
- Next active block: priority-3/4 follow-up work
  - New `claims_check_batch` (priority 4, added today) — continue deep-vet pass,
    ~50 papers remaining, batch size 10–15 per run
  - Priority-4/5 audit_gap items begin coming due 2026-05-26 (Gap 14 BRONZE) and
    2026-06-02 onward
- Priority-5 `search_pubmed` items (SAB-142, Abata ABA-201, BANDIT, Tegoprubart,
  PROTECT-ext, DAPAN-DIA) all on quarterly cadence — next checks 2026-07-25
  through 2026-08-10

## Git
- `.git/index.lock` / `.git/HEAD.lock` / `.git/objects/maintenance.lock`
  blockers are tracked as priority-1 manual_cleanup_required — sandbox cannot
  reliably remove these from the OneDrive mount; user remediation from
  PowerShell is required to push the backlog of commits.
- Today's state-file update and dashboard rebuild are written to disk and will
  be captured by the next successful commit.

## State
- Papers tracked: 280 (267 VETTED / 13 FLAGGED / 0 UNVETTED)
- `claims_checked`: 110 / 280 (up from 98 yesterday)
- Paths tracked: 57 in state, 44 in pipeline (3 filtered as dose-fragment artifacts)
- Gaps tracked: 15 (4 GOLD, 8 SILVER, 2 BRONZE, 1 EXPLORATORY)
- Run history: 35 entries
- Last run: 2026-05-16
