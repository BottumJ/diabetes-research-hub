# Diabetes Research Hub — Monitor Report

**Run:** 2026-09-20 (automated, sandbox)
**Mode:** review only — no existing files modified
**Previous report:** `monitor_report_2026-09-19.md`

---

## Headline

**The pipeline did not run last night — zero files in the entire hub changed in the last
36 hours — but that is the smaller story. The bigger one: the trial collector has been
structurally blind since it was written, and it is not a staleness problem.**

Every one of the five collector queries filters on `AREA[Condition](...)`. That field matches
only the *exact* condition strings a sponsor typed at registration. Roughly a fifth of diabetes
trials are registered with run-together or non-English condition strings — `Type1diabetes`,
`type1diabetes`, `Diabete Type 1` — and **those trials cannot be returned by any query the hub
runs, at any freshness.** Re-running the collector would not have found them. I measured the
loss live against the API today: **+261 trials across the five queries — a 26.7% increase on
what the hub currently sees, i.e. 21.1% of the reachable universe is invisible.** `[Certain]`

This resolves the open Sana question from three prior reports. Sana's first-in-human
hypoimmune islet trial is **NCT06239636** — RECRUITING, intervention type BIOLOGICAL, exactly
inside query 1's stated scope. It is missing because its condition field is the single token
`Type1diabetes`. I confirmed by direct API test that `AREA[Condition](diabetes)` returns **zero**
rows for it. The trial was never absent from ClinicalTrials.gov. It was absent from the hub's
field of view.

Second correction, also `[Certain]`: yesterday's report said **zero** results postings occurred
between 07-17 and 09-06 and flagged a suspected parser fault. That is wrong. There were **22**,
and the extraction is fine. The diff logic is what is broken — details in §2.

---

## 0. Yesterday's predictions, resolved

| # | Prediction (from 09-19) | Outcome |
|---|---|---|
| **A** | Trials refresh runs → `_latest` ≥ 894, generated after 09-19 | **NOT RUN.** `_latest` still 858 trials, generated 2026-07-17. Now **65 days**. No new snapshot. |
| **B** | Push executed → ahead-count 0, `origin/main` moves off `f7e976f` | **FALSE branch.** Ahead = **115** (up 2). `origin/main` still `f7e976f`, **2026-04-20**. **153 days** unpublished. |
| **C** | `VX-880` alias added → zimislecel hits > 0 | **NOT RUN.** `baseline_pubmed_alerts.py` line 67 still lists `zimislecel` alone. No new PubMed pull to test against. |
| **D** | Next trial snapshot ≥ 4 finerenone trials | **UNRESOLVED — no new snapshot.** But see §2: a live API probe surfaced **NCT07592000, "Breakthrough — T1DM and Chronic Kidney Disease"**, which is invisible to the current queries. |

The §1a diagnostic script recommended yesterday was not created (`Analysis/Scripts/diag_latest_write.py`
does not exist). The write-failure question is therefore still open — but it has dropped in
priority, because §1 below shows nothing ran at all last night, and §2 shows that fixing the
write would still leave a quarter of the trial universe unreachable.

---

## 1. File System Status

**Zero pipeline outputs written hub-wide since 2026-09-19 04:00.** `find` over the whole tree,
excluding `.git`, returns only this report. The next-newest file in the hub is
`ACTION_REQUIRED_2026-09-19.md` at 2026-09-19 03:36. The nightly pipeline did not execute.
`[Certain]`

| File | Last modified | Age | Status |
|---|---|---|---|
| `literature_gap_report.md` | 2026-09-19 | 1 d | FRESH |
| `literature_gap_data.json` | 2026-09-19 | 1 d | FRESH |
| `literature_gap_matrix.xlsx` | 2026-09-19 | 1 d | FRESH |
| `agent_state.json` | 2026-09-19 | 1 d | FRESH |
| `pubmed_recent_latest.json` | 2026-09-18 | 2 d | FRESH (did not re-run last night) |
| `pubmed_recent_summary.md` | 2026-09-18 | 2 d | FRESH |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 | **14 d** | Newest real trial data — now at the staleness threshold |
| `clinical_trials_latest.json` | 2026-07-17 | **65 d** | STALE — and see §2, staleness is the lesser problem |
| `clinical_trials_summary.md` | 2026-07-17 | **65 d** | STALE |
| `hub_monitor_report.md` | 2026-07-17 | **65 d** | STALE — file-change detection blind 9 weeks |
| `Diabetes_Research_Tracker.xlsx` | 2026-07-17 | **65 d** | STALE — master tracker |
| `literature_gap_report_enriched.md` | 2026-04-03 | **170 d** | STALE — citation hazard beside a 1-day-old base report |

Trial-data age, daily, since the last successful collector write:

```
07-17  ▏0 d   ████ snapshot written
08-27  ▏      ████ snapshot written (41 d gap)
08-28  ▏      ████ snapshot written
09-01  ▏      ████ snapshot written
09-06  ▏      ████ snapshot written   ← last real trial data
09-19  ▏13 d  ░░░░ nothing
09-20  ▏14 d  ░░░░ nothing
```

Working tree is clean (porcelain = 0, down from 1). The git-hygiene problem from earlier
reports is fully resolved; only the push remains.

---

## 2. Clinical Trial Changes

### 2a. The collector cannot see roughly a quarter of the trial universe

This is the finding that matters, and it is measurable, so here is the measurement.

`AREA[Condition](x)` matches the condition strings a sponsor entered verbatim.
`AREA[ConditionSearch](x)` matches ClinicalTrials.gov's own indexed condition terms, which
normalise spacing and common variants. I ran both forms of all five collector queries against
the live API today (2026-09-20):

| # | Collector query | `Condition` | `ConditionSearch` | Δ | % missed |
|---|---|---:|---:|---:|---:|
| 1 | T1D Cure & Cell Therapy | 158 | 187 | **+29** | 15.5% |
| 2 | T1D Immunotherapy & Prevention | 77 | 99 | **+22** | 22.2% |
| 3 | T2D Novel Therapies (Ph 2–3) | 151 | 210 | **+59** | 28.1% |
| 4 | Diabetes Technology (Devices) | 244 | 319 | **+75** | 23.5% |
| 5 | Recently Completed with Results | 348 | 424 | **+76** | 17.9% |
| | **Total (pre-dedupe)** | **978** | **1239** | **+261** | **21.1%** |

```
Q1  ████████████████████████████████ 158  │ +29
Q2  ███████████████ 77                    │ +22
Q3  ██████████████████████████████ 151    │ +59
Q4  ████████████████████████████████████████████████ 244 │ +75
Q5  ████████████████████████████████████████████████████████████████████ 348 │ +76
    ── visible today            ── recoverable by field change
```

`[Certain]` on every count — each is a `countTotal=true` API response read this run.

**Do not adopt `ConditionSearch` blindly.** I pulled the 29 trials that query 1 gains and read
every one. Twenty are unambiguously on-topic T1D, three are adjacent (ketosis-prone diabetes,
post-pancreatitis diabetes, injection-pain), and **six are oncology trials** — melanoma, NSCLC,
RCC, sarcoma CAR-T — that match through the broader index. Precision ≈ **79%**. Dropping the
bare `T1D` token does not help: the same six survive, and the variant returns 30 rather than 29.
The correct fix is a **union plus a relevance filter**, not a field swap. §6 action 1 gives it.

### 2b. What the hub is actually missing — and it is the worst possible subset

Four of the twenty recovered T1D trials are **islet transplantation** studies:

| NCT | Trial | Why it matters |
|---|---|---|
| **NCT06239636** | Hypoimmune islet transplantation, no immunosuppression (UP421) | The Sana trial. Sponsor of record is **Per-Ola Carlsson / Uppsala University Hospital**, which is a second reason sponsor-name search never found it. RECRUITING, Early Phase 1, n=2. |
| **NCT05973734** | Islet transplant + recipient T-reg cells / donor vertebral bone marrow | Sits on Treg/CAR-T × Islet Transplant |
| **NCT02846571** | Islet transplantation into the anterior chamber of the eye | Novel site, imaging-accessible graft |
| **NCT00706420** | Islet transplant alone, glucocorticoid-free immunosuppression | Immunosuppressant regimen — directly on gap #3 |

**Islet Transplant appears in four of the top six literature gaps** (§4). The hub has been
ranking that domain as under-researched while holding a trial view that systematically excludes
islet trials. The gap ranking is not thereby refuted — it is a *literature* measure, not a trial
measure — but any claim that pairs the two is currently resting on a censored denominator.
`[Certain]` that the trials are missing; `[Likely]` that this materially weakens the
trial-side corroboration of gaps #2–#6.

Also recovered, and timely: **NCT07592000, "Breakthrough — T1DM and Chronic Kidney Disease"** —
the exact cell the finerenone T1D-CKD approval will drive literature into, and invisible to the
hub today.

### 2c. Correction to the 09-19 report: results postings are fine, the diff is not

Yesterday's report: *"**Zero** new results postings between 07-17 and 09-06 across all 894 trials
… `[Likely]` an extraction issue rather than a true zero."*

Direct recount of the two snapshots: **22 trials carry `results_posted` dates on or after
2026-07-17.** Examples — NCT05035082 (Novo, RYBELSUS comparison, 08-10), NCT04596631 (Novo, oral
semaglutide, 08-21), NCT05428943 (Op-T, OPT101 in T1D, 08-10), NCT03899883 (U Colorado, uric acid
lowering in youth-onset T2D, 07-28).

All 22 are **new NCT IDs**, absent from the 07-17 snapshot. That is the mechanism: query 5 only
retrieves COMPLETED trials that *already have results posted*, so a trial enters the snapshot at
the moment its results post — it is never present-and-then-updated. A diff that looks for changed
`results_posted` values on trials in **both** snapshots can never fire for this category. The
parser is correct; the comparison is structurally incapable of detecting the event it was written
to detect. `[Certain]`

Withdraw action 6 from the 09-19 report. Replace it with: count results postings as
`new IDs in category 5`, or diff on `results_posted` across the union of IDs, not the intersection.

Live cross-check: query 5 returns **348** today against 343 in the 09-06 snapshot and 321 on
07-17. Results are posting steadily. There was never a stall.

### 2d. Key-organization Phase 3 status

Unchanged from 09-19 — no new trial data arrived, so this is reproduced from the 09-06 snapshot
and is **14 days old**. Vertex VX-880/zimislecel NCT06832410 and NCT04786262 RECRUITING; Lilly
baricitinib NCT07222137 and NCT07222332 RECRUITING; Lilly orforglipron master NCT06993792
ACTIVE_NOT_RECRUITING; Novo CagriSema NCT07564414 RECRUITING, NCT07282613 NOT_YET_RECRUITING.

---

## 3. PubMed Highlights

`pubmed_recent_latest.json` did not refresh last night — it remains the **2026-09-18** pull
(151 papers, 16 domains, 30-day lookback). Everything in this section was reported on 09-19.
**No new PubMed content this run.** Carried forward only because it is still the current data:

- 14 of 151 papers are cross-domain. Highest value unchanged: **PMID 42751271** (mitochondrial
  dysfunction in DKD, omics era — Biomarker × Microbiome × Multi-Omics, Tier 1 #1) and
  **PMID 42720752** (Diabetologia, pediatric beta-cell preservation — T1D Immunotherapy ×
  teplizumab).
- `domain_retmax` is 10 and eleven of sixteen domains hit that ceiling. You are reading 10 of
  202 GLP-1 papers. Five domains sit below the cap — T2D Remission (9), LADA (9), Drug
  Repurpose (3), GLP-1 Pharmacogenomics (3), Epigenetics (2) — and only those five have counts
  that mean anything. The bottom three are genuinely thin, not under-sampled.
- **zimislecel: 0 papers**, second consecutive window, while two Phase 3 trials run. The
  `VX-880` alias was not added. This is the same class of failure as §2a — a query that cannot
  see what it is looking for — and it is one line to fix.

---

## 4. Gap Analysis Summary

`literature_gap_report.md` and `literature_gap_data.json` both regenerated **2026-09-19**.
30 domains, 435 pairs. **Validation level: BRONZE.**

### Top 5 under-researched intersections

| # | Intersection | Gap score | Joint pubs | Tier 1 alignment |
|---|---|---:|---:|---|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | **Tier 1 #6** — Epidemiological / disparity (17/20) |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | Tier 2 |
| 3 | Islet Transplant × Drug Repurposing | 100.0 | 0 | **Tier 1 #4** — Drug Repurposing (18/20) |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | **Tier 1 #6** |
| 5 | Gene Therapy × LADA | 100.0 | 0 | Tier 2 |

(Rank 3 in the JSON is `Islet Transplant × GWAS/Polygenic`; the report correctly reclassifies it
as methodologically distinct and promotes `Islet Transplant × Drug Repurposing` into the top
five. I follow the report's ranking.)

### A ceiling problem worth naming

**21 of 435 pairs score exactly 100.0, and 18 have a joint count of zero.** The formula
`max(0, 1 − joint/geomean) × 100` saturates the moment `joint = 0`, so every empty cell ties at
100 regardless of how large the two parent literatures are. Beta Cell Regen × Health Equity
(expected 1766) and Islet Transplant × Personalized Nutr (expected 421) are not equally
surprising absences, but the score cannot distinguish them.

A ratio-free ordering — rank by **expected joint count** among the zero cells — is one line of
code and would separate the genuinely striking voids from the merely small ones. Ranking the 18
zero-cells by expected joint count gives a materially different order:

| Rank by expected | Intersection | Expected | Report's own classification |
|---|---|---:|---|
| 1 | GWAS/Polygenic × Closed Loop/AP | 3290.0 | Methodologically distinct |
| 2 | Drug Repurposing × CGM Technology | 2094.5 | Methodologically distinct |
| 3 | **Beta Cell Regen × Health Equity** | 1765.6 | **Meaningful gap #1** |
| 4 | Glucokinase × Health Equity | 1337.1 | Meaningful gap #7 |
| 5 | Gene Therapy × LADA | 1201.7 | Meaningful gap #5 |
| 6 | Islet Transplant × GWAS/Polygenic | 1178.1 | Methodologically distinct |

The two largest voids are both already reclassified as methodologically distinct, which is
reassuring — the classifier is doing real work. But note that **Beta Cell Regen × Health Equity
is the largest expected void the report calls meaningful**, roughly 4× the expected count of
Islet Transplant × Personalized Nutr (420.5), which the saturated score ties with it at 100.0.
`[Likely]` this ordering is a better prioritisation signal than the score; cheap to test.

### Where gaps and doctrine converge — with one new caveat

Unchanged: gaps #1, #3, #4, plus #6, #7, #10 and #12 route to **Tier 1 #4 (Drug Repurposing)**
and **Tier 1 #6 (Health Equity)**, and §3 independently shows Drug Repurpose is the thinnest
domain in the 30-day literature. Two independent signals, same target.

**New caveat from §2b:** four of the top six gaps involve Islet Transplant, and the hub's trial
view of that domain is provably incomplete. Before promoting any Islet Transplant gap past
BRONZE, the date-unbounded manual confirmation that gap #3 already models must now *also* cover
the trial registry with the corrected query. An "absence" claim built on a censored query is the
failure mode the doctrine's absence-claim gate exists to catch.

Note also that `NCT05973734` (islet transplant + recipient T-regs) is live and invisible to the
hub — which bears directly on **gap #14, Treg/CAR-T × Neuropathy** and on the Treg gaps generally.

---

## 5. Breaking News

**Nothing new clears the significance bar in the last 7 days.** `[Certain]` on the search
results; `[Likely]` that coverage is complete.

The finerenone (Kerendia) approval for CKD associated with type 1 diabetes — **2026-09-17**,
first new agent for that population in 30+ years, UACR ratio 0.75 vs placebo at 6 months,
hyperkalemia 10.1% vs 3.3% — was reported in full in the 09-19 report and remains the standing
item. It is still unlogged in the tracker, which has not been touched in 65 days.

Two forward-looking items, `[Guessing]`, unchanged: insulin efsitora alfa possibly the second
weekly basal insulin approved in the US later in 2026; a tirzepatide CV-indication decision
possibly in H2 2026.

On zimislecel specifically: Vertex has stated it accelerated regulatory submission to **2026**
(FDA, EMA, MHRA) with fast-track designation, which would put availability as early as 2027.
That is a company timeline, not a filing announcement — `[Likely]` that no submission has been
publicly confirmed as of today. When it is confirmed it will be the single most consequential
event for the T1D cure track, and the hub will miss the accompanying literature unless the
`VX-880` alias lands first.

Sana, separately from NCT06239636: 14-month data from the investigator-sponsored study reported
sustained C-peptide and met the primary safety endpoint in its single participant, and Sana has
a Mayo Clinic collaboration on **SC451** (iPSC-derived hypoimmune islets) with an IND targeted
later in 2026. `[Likely]` — company communications, n=1, evidence level low; log it as a watch
item, not a finding.

---

## 6. Recommended Actions

Ranked by how much each changes what the hub can know. Action 1 is new and outranks everything
carried over.

**1. Fix the collector's condition filter — this is worth more than any refresh.**
No amount of re-running recovers these trials. Patch, then re-run. Script below; save as
`Analysis/Scripts/patch_condition_queries.py` and run locally:

```python
# Measures the recovery, writes a review file, and does NOT modify the collector.
# Run: python Analysis/Scripts/patch_condition_queries.py
import urllib.request, urllib.parse, json, os

API = "https://clinicaltrials.gov/api/v2/studies"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Results",
                   "condition_query_recovery.json")

# Oncology / unrelated terms that leak in through the broader ConditionSearch index.
EXCLUDE = ("melanoma", "carcinoma", "sarcoma", "lung cancer", "solid tumor",
           "solid tumour", "lymphoma", "leukemia", "leukaemia", "myeloma")

PAIRS = {
    "T1D Cure & Cell Therapy": (
        'AREA[Condition](type 1 diabetes)',
        '(AREA[Condition](type 1 diabetes) OR AREA[ConditionSearch]("type 1 diabetes" OR "type1diabetes" OR "diabete type 1"))',
        ' AND AREA[InterventionType](BIOLOGICAL OR DEVICE) AND AREA[OverallStatus](RECRUITING OR NOT_YET_RECRUITING OR ACTIVE_NOT_RECRUITING OR ENROLLING_BY_INVITATION)'),
    "T1D Immunotherapy & Prevention": (
        'AREA[Condition](type 1 diabetes)',
        '(AREA[Condition](type 1 diabetes) OR AREA[ConditionSearch]("type 1 diabetes" OR "type1diabetes" OR "diabete type 1"))',
        ' AND AREA[InterventionType](DRUG) AND AREA[Phase](PHASE3 OR PHASE2) AND AREA[OverallStatus](RECRUITING OR NOT_YET_RECRUITING OR ACTIVE_NOT_RECRUITING)'),
    "T2D Novel Therapies (Phase 2-3)": (
        'AREA[Condition](type 2 diabetes)',
        '(AREA[Condition](type 2 diabetes) OR AREA[ConditionSearch]("type 2 diabetes" OR "type2diabetes" OR "diabete type 2"))',
        ' AND AREA[Phase](PHASE3 OR PHASE2) AND AREA[OverallStatus](RECRUITING OR NOT_YET_RECRUITING OR ACTIVE_NOT_RECRUITING) AND AREA[StudyFirstPostDate]RANGE[2023-01-01, MAX]'),
    "Diabetes Technology (Devices)": (
        'AREA[Condition](diabetes)',
        '(AREA[Condition](diabetes) OR AREA[ConditionSearch](diabetes))',
        ' AND AREA[InterventionType](DEVICE) AND AREA[Phase](NA) AND AREA[OverallStatus](RECRUITING OR NOT_YET_RECRUITING OR ACTIVE_NOT_RECRUITING) AND AREA[StudyFirstPostDate]RANGE[2023-01-01, MAX]'),
    "Diabetes Recently Completed with Results": (
        'AREA[Condition](diabetes)',
        '(AREA[Condition](diabetes) OR AREA[ConditionSearch](diabetes))',
        ' AND AREA[OverallStatus](COMPLETED) AND AREA[ResultsFirstPostDate]RANGE[2025-01-01, MAX]'),
}

def fetch(flt, fields="NCTId,BriefTitle,Condition", cap=20):
    out, tok = [], None
    for _ in range(cap):
        p = {"format": "json", "pageSize": 100, "filter.advanced": flt, "fields": fields}
        if tok:
            p["pageToken"] = tok
        url = API + "?" + urllib.parse.urlencode(p)
        req = urllib.request.Request(url, headers={"User-Agent": "DiabetesResearchHub/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode())
        out += d.get("studies", [])
        tok = d.get("nextPageToken")
        if not tok:
            break
    return out

def nct(s):
    return s["protocolSection"]["identificationModule"]["nctId"]

def offtopic(s):
    conds = " ".join(s["protocolSection"].get("conditionsModule", {}).get("conditions", [])).lower()
    title = s["protocolSection"]["identificationModule"].get("briefTitle", "").lower()
    return any(t in conds or t in title for t in EXCLUDE)

report = {}
for label, (narrow, wide, tail) in PAIRS.items():
    a = {nct(s) for s in fetch(narrow + tail)}
    wide_studies = fetch(wide + tail)
    kept = [s for s in wide_studies if not offtopic(s)]
    dropped = [nct(s) for s in wide_studies if offtopic(s)]
    b = {nct(s) for s in kept}
    gained = sorted(b - a)
    report[label] = {
        "narrow": len(a), "wide_raw": len(wide_studies), "wide_filtered": len(b),
        "gained": len(gained), "dropped_offtopic": len(dropped),
        "gained_ids": gained, "dropped_ids": dropped,
    }
    print(f"{label:42} {len(a):4} -> {len(b):4}  (+{len(gained)}, filtered {len(dropped)})")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)
print("\nwrote", os.path.abspath(OUT))
print("Review gained_ids before editing baseline_clinical_trials.py QUERIES.")
```

Read `condition_query_recovery.json`, confirm the gained IDs are on-topic, *then* paste the
widened filters into the `QUERIES` list in `baseline_clinical_trials.py`. Expect the snapshot to
land near **1100–1150 unique trials** rather than 894 — `[Likely]`, since the 1239 pre-dedupe
total overlaps across queries at roughly the 8% rate the 09-06 snapshot shows.

**2. Find out why the pipeline did not run last night.** Zero files changed hub-wide in 36 hours.
This is a scheduler or `RUN_PIPELINE_AND_PUSH.ps1` failure, not a script bug — PubMed, gaps, and
the agent state all stopped together. Check the task-scheduler history and the last lines of
`Analysis/Logs/` before doing anything else, because every other action below assumes the
pipeline can run.

**3. Fix the results-posting diff (§2c), and delete the parser-audit action from the 09-19 list.**
Count new results as new IDs entering category 5. The current comparison is incapable of firing.

**4. Add `VX-880` as a zimislecel alias** in `baseline_pubmed_alerts.py` (line 67). One line.
Two Phase 3 trials, zero papers across two windows, and a possible 2026 regulatory submission
that the hub would currently miss.

**5. Push. 115 commits, `origin/main` frozen at 2026-04-20 — 153 days.** Working tree clean,
porcelain 0, three consecutive clean nights. There is no remaining safety argument.
```
git push origin main
```

**6. Log the finerenone T1D-CKD approval in the tracker** with the UACR and hyperkalemia figures
from §5 — evidence level: regulatory approval, Level 1 per doctrine. The tracker is 65 days old.

**7. Run `hub_monitor.py`.** Its report is 65 days old; file-change detection has been blind for
nine weeks, which is why the §2a defect went unflagged this long.

**8. Rank the zero-cells by expected joint count** (§4) as a second gap ordering. One line;
separates striking voids from small ones that the saturated score ties at 100.

**9. Resolve `literature_gap_report_enriched.md` (170 days).** Re-run or delete. A stale enriched
report sitting beside a 1-day-old base report is a citation hazard.

**10. Scope the Drug Repurposing × Islet Transplant screen (gap #3)** — still the best-evidenced
gap, still Tier 1 #4, still fully open data. But per §4, redo the absence confirmation against
the *corrected* trial query first. NCT00706420 (glucocorticoid-free immunosuppression regimen) is
directly on-topic and was invisible until today.

---

## 7. Predictions for the next run (falsifiable)

| # | Prediction |
|---|---|
| **A** | If action 1 runs → the recovery script reports ≥ +200 gained IDs across the five queries after off-topic filtering, and the next snapshot exceeds **1050** unique trials. If it lands under 950, my dedupe assumption is wrong and the 21% figure needs restating as a pre-dedupe upper bound. |
| **B** | If action 1 runs → **NCT06239636, NCT05973734, NCT02846571, NCT00706420 and NCT07592000** all appear in the next snapshot. Any absentee means the condition filter is not the only exclusion mechanism. |
| **C** | If action 2 finds nothing wrong with the scheduler → the pipeline ran and failed silently, and `Analysis/Logs/` will hold a traceback dated 2026-09-20. If the logs are also empty, the job never started. |
| **D** | If action 4 runs → zimislecel therapy hits > 0 on the next PubMed pull. Still 0 with the alias in place → the absence is real and publishable. |
| **E** | If action 3 runs → the next snapshot diff reports a **non-zero** results-posting count for the 09-06 → present window. Live query 5 stands at 348 vs 343 on 09-06, so the floor is ≥ 5. |

---

*Generated by the automated hub monitor, 2026-09-20. Review only — no existing files were
modified. All file ages, snapshot diffs and API counts verified by direct read or direct query
this run. Confidence levels per Research Doctrine: `[Certain]` = hard evidence in hand,
`[Likely]` = strong inference, `[Guessing]` = gap-filling.*
