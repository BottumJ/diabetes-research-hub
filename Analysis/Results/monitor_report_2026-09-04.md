# Diabetes Hub Monitor Report — 2026-09-04

**Run type:** Scheduled automated review (read-only; no existing files modified)
**Effective data date:** 2026-09-01 snapshots — **3 days old, unchanged since the 09-03 report**
**Evidence levels per Research Doctrine:** file-derived facts marked [Certain]; web-derived marked [Likely] pending primary-source confirmation.

---

## 0. Lead finding — read this first

**No new data has entered the hub since 2026-09-01. This is the fourth consecutive
report drawing on the same snapshot pair.** [Certain]

Snapshot cadence, last 8 files:

```
2026-07-16  ██
2026-07-17  ██
            ····· 41-day outage (07-18 → 08-26), 0 snapshots ·····
2026-08-27  ██
2026-08-28  ██
            ··· 3-day gap ···
2026-09-01  ██
2026-09-02  ─  none
2026-09-03  ─  none
2026-09-04  ─  none  (today)
```

The 09-02/09-03/09-04 blanks mean the monitor is now re-reading stale inputs and
re-deriving the same conclusions. Continuing to run it daily against a frozen snapshot
produces the appearance of surveillance without the substance. **Either restore the
acquisition step or drop this task to weekly.** [Certain]

Nothing in §2–§4 below is new information relative to the 2026-09-03 report except
§2a, which *corrects* it.

---

## 1. File System Status

| File | Last modified | Age (d) | Status |
|---|---|---|---|
| `clinical_trials_snapshot_2026-09-01.json` | 2026-09-01 02:37 | 3 | Newest trial data |
| `pubmed_recent_snapshot_2026-09-01.json` | 2026-09-01 02:38 | 3 | Newest PubMed data |
| `clinical_trials_latest.json` | 2026-07-17 02:05 | **49** | **STALE pointer** |
| `pubmed_recent_latest.json` | 2026-07-17 02:06 | **49** | **STALE pointer** |
| `hub_monitor_report.md` | 2026-07-17 02:16 | **49** | **STALE** |
| `literature_gap_data.json` | 2026-07-18 03:11 | **48** | **STALE** |
| `literature_gap_report.md` | 2026-09-03 07:17 | 1 | Fresh file, **July data** — see §4 |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 10:07 | **49** | **STALE** |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 03:12 | 4 | Current |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 00:06 | 173 | 6 months old |

**The `*_latest.json` divergence is the structural problem.** The dated snapshots
advanced to 09-01; the pointer files did not. Anything reading `*_latest.json` —
dashboards, tracker updates, gap analysis — is consuming **July 17 data** while this
report consumes September 1 data. Two versions of "current" now coexist in the hub. [Certain]

`hub_monitor_report.md` records its hub root as `/sessions/intelligent-bold-bardeen/...`,
a prior sandbox session path — confirming it was written by a sandbox run, not your
local machine. [Certain]

**Stale lock file** `.~lock.Diabetes_Research_Tracker.xlsx#` (2026-03-14) still present.
Will block lock-aware writers. [Certain]

---

## 2. Clinical Trial Changes

**Corpus:** 892 (08-27) → 893 (08-28) → **887 (09-01)**.
**09-01 vs 08-28 diff: 0 new, 0 in-place status changes, 0 newly posted results, 6 dropped.** [Certain]

Status distribution (09-01): COMPLETED 341 · RECRUITING 276 · NOT_YET_RECRUITING 151 ·
ACTIVE_NOT_RECRUITING 113 · ENROLLING_BY_INVITATION 6. Phase 3 RECRUITING: 57. [Certain]

### 2a. Correction to the 2026-09-03 report — the 6 dropped trials are *not* an API glitch

Yesterday's report called the 6 disappearances "more consistent with a dropped result page
than with six independent withdrawals" and advised not treating them as status changes.
**The historical base rate contradicts that.** [Certain]

I tested every drop event across all 124 snapshots (2026-03-15 → 2026-09-01): for each
trial present in snapshot *i* and absent in *i+1*, did it return within the next 3 snapshots?

```
Drop events observed                        76
  → reappeared within 3 snapshots            0     0.0%
  → never returned                          76   100.0%

Restricted to daily-cadence era only        62 events,  0 transient  (0.0%)
Lifetime trials with a gap-then-return       1  (NCT06357728, of 968 tracked NCT IDs)
```

Transient drops essentially do not happen in this pipeline. With 0/76, the rule-of-three
95% upper bound on the per-event transient rate is ~3.9%; the probability that all six
09-01 drops are simultaneously transient is on the order of 10⁻⁸. **The glitch hypothesis
is not supportable.** [Certain — arithmetic on local files]

**What a "drop" actually means.** Four of the five queries in `baseline_clinical_trials.py`
filter on `AREA[OverallStatus](RECRUITING OR NOT_YET_RECRUITING OR ACTIVE_NOT_RECRUITING
OR ENROLLING_BY_INVITATION)`. A trial that moves to COMPLETED, TERMINATED, WITHDRAWN,
SUSPENDED, or UNKNOWN **leaves the result set entirely** rather than appearing with a new
status. [Certain — read from script source, lines 31–52]

So: **drops are the status-change signal, and the diff logic cannot see them.** The monitor
reports "0 status changes" precisely when the most consequential transitions — termination
and withdrawal — occur. This is a systematic blind spot, not a one-day anomaly. It also
means the "23 status changes" reported for 07-17 → 09-01 is an undercount.

Secondary explanation, not excluded: a sponsor editing Condition / InterventionType / Phase
fields can also push a trial out of a filter. Distinguishing termination from re-scoping
requires querying each NCT directly. [Likely]

**The 6 trials needing individual lookup** (their last-seen status is *stale*, not current):

| NCT | Last-seen status | Phase | Sponsor |
|---|---|---|---|
| NCT06542627 | RECRUITING | N/A | Kangbuk Samsung Hospital |
| NCT06558708 | RECRUITING | Phase 2 | Gan and Lee Pharmaceuticals (GZR101) |
| NCT06559722 | NOT_YET_RECRUITING | **Phase 3** | Tonghua Dongbao (degludec/liraglutide) |
| NCT06569940 | RECRUITING | N/A | Sleepiz AG |
| NCT06575478 | RECRUITING | Phase 2 | Beijing Supreme Life Pharmaceutical |
| NCT07325461 | ACTIVE_NOT_RECRUITING | N/A | Tandem Diabetes Care |

I could not resolve these against the live registry from this run — the ClinicalTrials.gov
API URL was outside the fetch provenance set. See §6 for the one-line script that resolves it.

### 2b. Key-organization trials (09-01, unchanged from 09-03)

- **Vertex** — NCT04786262 (VX-880/zimislecel, Phase 3, RECRUITING, n=52);
  NCT06832410 (VX-880, Phase 3, RECRUITING, n=10); NCT05791201 (VX-264, Ph1/2, ACTIVE_NOT_RECRUITING, n=7) [Certain]
- **Eli Lilly** — baricitinib Phase 3 pair now recruiting in T1D: NCT07222137 (delay of
  Stage 3, n=150) and NCT07222332 (beta-cell preservation in children, n=300). Retatrutide
  Ph3 NCT06260722 (n=1,250) and NCT06297603 (n=320) both ACTIVE_NOT_RECRUITING. [Certain]
- **Novo Nordisk** — CagriSema Ph3 NCT07564414 (n=2,500, RECRUITING); NCT07282613 (n=80,
  NOT_YET); AMAZE 8 NCT07400107 (n=1,000, NOT_YET). [Certain]
- **Sana Biotechnology — zero trials in the corpus**, despite being a named watch target.
  Repeat of a 09-03 finding; still unaddressed. Sana's hypoimmune islet work is likely
  filed under conditions/interventions your five queries don't match. **Add a sponsor-name
  query.** [Certain that it is absent; Likely as to cause]

### 2c. Results posted since 2026-07-05 — 31 trials, none new since 08-28

Most recent: NCT04506151 (08-27, sleep optimization in T1D, n=144), NCT05530356 (08-24),
NCT04876053 (08-21, rural food delivery, n=416), **NCT04596631 (08-21, Novo Nordisk oral
semaglutide Ph3, n=132)**, NCT07513259 (08-17, GLP-1 RA pre-diagnosis and post-cancer
mortality, **n=203,424** — large observational, worth a look for the GLP-1/complications
intersection). [Certain]

---

## 3. PubMed Highlights

Window 2026/08/02 → 2026/09/01, 30-day lookback, 160 unique papers across 16 domains. [Certain]

**Volume is flat; cross-domain yield is drifting up:**

```
snapshot     papers   cross-domain
2026-07-17     158        12   ████████████
2026-08-27     167        14   ██████████████
2026-08-28     163        16   ████████████████
2026-09-01     160        17   █████████████████
```

Domain counts are uniform at 3 per domain across all 16 domains — that is a `retmax` ceiling,
not a measurement of field activity. **Do not read domain-level "publication volume trends"
off these snapshots; the instrument is saturated.** Only the therapy queries and the
cross-domain overlap carry signal. [Certain]

### Cross-domain papers — 17 total, 9 new since 08-28

Highest priority (genuine multi-field bridges):

| PMID | Domains | Paper |
|---|---|---|
| 42626948 | T1D Stem Cell Cure · T1D Immunotherapy · teplizumab | Gene-edited **hypoimmune islets** as a cure for T1D: immunological challenges. *Expert Opin Biol Ther*, 08-21 |
| 42627334 | T1D Immunotherapy · baricitinib | **β-cell function 1 year after stopping oral baricitinib** in T1D. *Diabetes Care*, 08-21 |
| 42610933 | T1D Immunotherapy · teplizumab | Baseline serum metabolites as **predictors of teplizumab response**. *Diabetes*, 08-18 |
| 42674789 | Diabetes AI/ML · **LADA** | Algorithmic diabetes classification performance in population cohorts. *BMJ Open*, 08-31 |
| 42582350 | T1D Immunotherapy · LADA | Anti-GAD65 cerebellar ataxia in young adult with T1D. *Diabetol Int* |
| 42673585 | orforglipron · retatrutide · CagriSema | GLP-1 RA and co-agonists for weight loss in adults **without** diabetes. *Ann Intern Med*, 09-01 |

**PMID 42627334 is the single most actionable item in this window.** Post-cessation β-cell
data directly informs the durability question that the Tier-1 immunotherapy work depends on,
and it lands while Lilly's two baricitinib Phase 3s (§2b) are actively recruiting. [Certain]

**PMID 42674789** bridges AI/ML × LADA — matching gap-report row "AI / ML Predict × LADA"
(gap score 82.0, 3 joint pubs). This is a live gap closing in real time; if you intend to
contribute there, the window is narrowing. [Certain]

**Classifier false positive to fix:** PMID 42670002 ("Targeting Autoimmunity in Type 1
Diabetes: Emerging Immunomodulatory Therapies") is tagged **Microbiome · Gene Therapy ·
Closed Loop AP**. An immunotherapy review is not a closed-loop paper. Keyword queries are
matching background-section mentions, which inflates the cross-domain count — the metric
I just charted as trending up. Treat the 12→17 rise as suspect until domain queries are
tightened. [Certain]

### Key therapies (paper counts, 30-day window)

`dapagliflozin` 32 · `orforglipron` 12 · `retatrutide` 8 · `icodec` 8 · `teplizumab` 4 ·
`CagriSema` 3 · `baricitinib` 2 · **`zimislecel` 0**. [Certain]

(These are `total_count`. Note `dapagliflozin` and `orforglipron` both return only 10 PMIDs —
the `retmax=10` therapy ceiling — so their *retrieved* sets are truncated even though the
counts are accurate.) [Certain]

**Zimislecel returns 0 hits on `diabetes AND zimislecel`.** Given the NEJM publication and
ADA 85th Sessions presentation, a literal-zero result for the lead T1D cure candidate points
at the query, not the literature. Likely still indexed as VX-880. **Change the query to
`(zimislecel OR VX-880)`.** [Certain that count is 0; Likely as to cause]

---

## 4. Gap Analysis

**The gap report is fresh on disk and stale in content.** `literature_gap_report.md` was
regenerated 2026-09-03 07:17, but its header reads `Date range: 2020/01/01 to 2026/07/17`
and `literature_gap_data.json` carries `"generated": "2026-07-17T10:14:41"`. The regeneration
re-rendered the July cache (`.gap_cache.json`, last written 2026-07-15) without re-querying
PubMed. **A reader checking the file date would conclude the analysis is one day old. It is
48 days old.** This is the most likely place for a stale number to enter a manuscript. [Certain]

### Top gaps (BRONZE — single analytical source, expert confirmation required)

| Rank | Intersection | Gap | Joint pubs |
|---|---|---|---|
| 1 | Treg / CAR-T × Neuropathy | 100.0 | 0 |
| 2 | Beta Cell Regen × Health Equity | 100.0 | 0 |
| 3 | Treg / CAR-T × Health Equity | 100.0 | 0 |
| 4 | Glucokinase × Health Equity | 100.0 | 0 |
| 5 | Gene Therapy × LADA | 100.0 | 0 |
| 6 | Drug Repurposing × Health Equity | 100.0 | 0 |
| 7 | Insulin Resistance × Islet Transplant | 91.9 | 1 |

**Structural caution before anyone acts on these.** Four of the top six pair a small domain
with **Health Equity** (1,990 pubs), and the fifth pairs two of the three smallest domains
in the set (Gene Therapy 2,296 × LADA 582; Islet Transplant is 248). The gap score
normalizes by geometric mean, so small-N pairs are the ones most able to reach exactly 100.0
on a joint count of 0 — a single missing paper produces a perfect score. **These rankings
are partly an artifact of domain size, not purely of research neglect.** Before treating any
as a contribution target, check whether the intersection has enough addressable literature
to support a synthesis at all. [Certain — arithmetic follows from the stated formula and the
domain-volume table in the report]

**Tier-1 alignment:** `RESEARCH_DOCTRINE.md` names Tier 1 only once (line 286: "For Tier 1
domains: Run computational analysis") without enumerating which domains those are, and
`CONTRIBUTION_STRATEGY.md` has not been touched since March. **I cannot verify gap/Tier-1
alignment because the Tier-1 list is not written down anywhere machine-readable.** That is
a governance gap worth closing before the next contribution decision. [Certain]

---

## 5. Breaking News (web, last ~7 days)

Nothing in the last 7 days meets the "genuinely significant" bar. Context items, all [Likely]
pending primary-source confirmation:

- **Retatrutide** — TRIUMPH-1/-2/-3 have all reported; Lilly announced 2026-07-23 it intends
  a BLA submission in **Q1 2027**. TRIUMPH-2 reported 20.8% weight loss and −1.5% A1C at
  12 mg in obesity + T2D. Predates this window; noted because NCT06260722/NCT06297603 in
  your corpus are the trials behind it.
- **Avexitide** — positive Phase 3 in post-bariatric hypoglycemia (August 2026). Adjacent
  to, not within, the diabetes corpus.
- **Tirzepatide** — new cardiovascular indication approved (August 2026).
- **Zimislecel** — Phase 3 ongoing; FDA fast-track; submission timeline pulled forward, with
  availability discussed as early as 2027. No new readout this week. Matches NCT04786262 /
  NCT06832410 in your corpus.

No FDA diabetes approval action dated in the 08-28 → 09-04 window surfaced. [Likely — absence
of evidence from a single search pass, not a verified negative]

---

## 6. Recommended Actions

**Fix the pipeline before trusting another report** — in priority order:

1. **Resolve the 6 dropped NCTs.** They are the only unexplained change in this snapshot,
   and one is Phase 3. Single API call:
   ```
   https://clinicaltrials.gov/api/v2/studies?format=json&fields=NCTId,OverallStatus,WhyStopped,LastUpdatePostDate&filter.ids=NCT06542627,NCT06558708,NCT06559722,NCT06569940,NCT06575478,NCT07325461
   ```

2. **Patch the diff logic to treat drops as status changes.** Currently the monitor
   structurally cannot report terminations or withdrawals (§2a). Add a sixth "reconciliation"
   query that re-fetches every previously-seen NCT by ID regardless of status, so exits
   appear as transitions instead of disappearances.

3. **Repoint or delete `*_latest.json`.** Two conflicting definitions of "current" in one
   folder is how a July number ends up in a September manuscript. Either symlink them to the
   newest dated snapshot or remove them so downstream code fails loudly.

4. **Re-run gap analysis with a cold cache** — `python project1_literature_gap_analysis.py`
   after clearing `.gap_cache.json`. The current report is 48 days old while presenting as
   1 day old (§4).

5. **Fix two queries** — `zimislecel` → `(zimislecel OR VX-880)`; add a Sana Biotechnology
   sponsor query to `baseline_clinical_trials.py`. Both are named watch targets currently
   returning zero.

6. **Raise `retmax` above 3 for domain queries**, or stop reporting domain volume. The
   current setting makes all 16 domains report identically (§3).

7. **Read PMID 42627334** (baricitinib post-cessation β-cell function, *Diabetes Care*) —
   highest-value paper in the window, and it bears on two actively recruiting Phase 3s.

8. **Write the Tier-1 domain list into `RESEARCH_DOCTRINE.md`** as an explicit enumeration.
   Gap/Tier-1 alignment cannot be checked until it exists (§4).

9. **Delete** `.~lock.Diabetes_Research_Tracker.xlsx#`.

10. **Decide the cadence.** With acquisition stalled, daily runs generate reports that
    restate prior conclusions. Restore the acquisition step or move this task to weekly.

**Local scripts to run** (compute belongs on your machine, not the sandbox):

```
python Analysis/Scripts/baseline_clinical_trials.py     # refresh trials, repoint _latest
python Analysis/Scripts/baseline_pubmed_alerts.py       # refresh PubMed, repoint _latest
python Analysis/Scripts/project1_literature_gap_analysis.py   # after clearing .gap_cache.json
python Analysis/Scripts/hub_monitor.py                  # refresh file-change tracking
```

---

## Verification Note

Every file-derived number here was computed directly from the JSON in
`Analysis/Results/`; the drop-rate figures in §2a come from a full pass over all 124
`clinical_trials_snapshot_2026-*.json` files. The query-filter claim in §2a is read from
`baseline_clinical_trials.py` lines 31–52. The live status of the 6 dropped NCTs is the one
claim in this report that **could not be verified** — the registry lookup was blocked by
fetch provenance rules. It is flagged as unresolved, not asserted.

No existing files were modified by this run.

*Generated by Diabetes Hub Monitor — scheduled review, 2026-09-04*
