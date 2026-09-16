# Diabetes Research Hub — Monitor Report

**Run date:** 2026-09-13 (Sunday, automated)
**Prior report:** monitor_report_2026-09-12.md
**Mode:** Review run. No existing hub file modified. One new file written (this report).
**Environment note:** Linux sandbox failed to mount — **6th consecutive day**, same Plan9
`share "c" is not mounted` error, same 2026-09-08 Windows update. No Python executed. Every
registry and PubMed figure below is a live API read made through the browser today. OS mtimes
remain unreadable — file ages use each file's internal `generated` field.

---

## Headline

**Yesterday's "cheapest item in the hub" is wrong, and today is the day it would have failed.**

Recommendation #3 of the 09-12 report was: fix the freshness gate to query **D−1**. Two days of
evidence supported it. Today D−1 is Saturday 09-12, and it reads **0**. The proposed fix would
have returned FAIL, exactly like the bug it replaces.

The reason is not a lag. It is that **ClinicalTrials.gov does not post updates on non-business
days at all**, and the hub has been modelling a five-day batch cycle as a continuous process with
a mysterious one-day delay.

```
  AREA[LastUpdatePostDate]RANGE[D,D], all conditions, read 2026-09-13
  ────────────────────────────────────────────────────────────────────
  Fri 09-04    799  ████████████████
  Sat 09-05      0
  Sun 09-06      0
  Mon 09-07      0   ← US Labor Day (federal holiday)
  Tue 09-08    979  ███████████████████
  Wed 09-09  1,165  ███████████████████████
  Thu 09-10  1,104  ██████████████████████
  Fri 09-11  1,165  ███████████████████████
  Sat 09-12      0
  Sun 09-13      0   ← today
  ─── control ───
  Sat 08-29      0
  Sun 08-30      0
  Tue 09-01    931  ██████████████████
```

Every weekend day and the one federal holiday in the window read exactly 0; every business day
reads 799–1,165. **[Certain — 13 `countTotal` reads today.]**

The corrected rule: **query the most recent completed business day, excluding US federal
holidays.** On a Monday that is the previous Friday, not Sunday. D−1 is right four days out of
seven and wrong three.

**And the decay is a batch artifact too.** Every bucket read today is byte-identical to
yesterday's reading:

| bucket | 09-11 rdg | 09-12 rdg | **09-13 rdg** | Δ 24h |
|---|---:|---:|---:|---:|
| Fri 09-04 | 826 | 799 | **799** | **0** |
| Tue 09-08 | 998 | 979 | **979** | **0** |
| Wed 09-09 | 1,189 | 1,165 | **1,165** | **0** |
| Thu 09-10 | 1,221 | 1,104 | **1,104** | **0** |
| Fri 09-11 | 0 | 1,165 | **1,165** | **0** |

Three days of 19–117/day decay, then a flat zero across a Saturday→Sunday interval. Decay does not
happen on days the batch does not run. That moves M-06's mechanism from **Guessing** to **Likely**:
historical buckets are re-dated during business-day batch runs, not by elapsed time.

**Falsifiable prediction for the 09-14 run:** on Monday the 09-11 bucket will read **below 1,165**
and the 09-10 bucket **below 1,104**, while 09-12 and 09-13 will still read **0** and will never
fill. If the buckets are unchanged again on Monday, this explanation is wrong.

**The standing rule is unchanged and still binds:** a historical `LastUpdatePostDate` day-count is
not reproducible and must never be stored.

---

## 1. File System Status

| File | Internal `generated` | Age | Δ vs 09-12 |
|------|----------------------|-----|-----------|
| `literature_gap_data.json` / `_report.md` | 2026-09-08 03:17:27 | **5d** | +1d |
| `pubmed_recent_latest.json` | 2026-09-06 09:18:08 | **7d** | +1d |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 02:38:16 | **7d** | +1d |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 | 13d | — |
| `clinical_trials_latest.json` | **2026-07-17 02:05:53** | **58d** | still a broken pointer |
| `hub_monitor_report.md` / `hub_monitor_state.json` / `clinical_trials_summary.md` | 2026-07-17 | **58d** | still stale |
| `Diabetes_Research_Tracker.xlsx` | — | — | **still lock-held** |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 | 182d | — |

`clinical_trials_latest.json` metadata read today: `total_trials: 858`, categories
152/76/147/236/321 — the 07-17 figures, not the 09-06 ones. Confirmed a duplicate pointer, D-01.

**No file in `Analysis/Results/` carries a 2026-09-13 date before this run.** Newest prior
artifacts are `monitor_report_2026-09-12.md` and `run_report_2026-09-12.md`. Seventh consecutive
day with no script execution.

- `.~lock.Diabetes_Research_Tracker.xlsx#` still present. Tracker backlog now **twelve days**.
- **09-07 test residue: all four files still present, now 6 days old** — `_wtest.txt`,
  `.gap_checkpoint.json.testbak`, `.gap_checkpoint.json.__unlinktest`, root `.wtest`.
  Verified by directory listing today.
- `open_findings.md` exists (written 09-12) and is re-emitted below in condensed form. **Second of
  the three consecutive runs required to retire M-08.**
- Dashboard builders still unexecuted; `origin/main` frozen at 2026-04-20 — **146 days**.

---

## 2. Clinical Trial Changes

### Freshness gate: FAIL by construction, and the proposed fix also fails today

| Query, run 2026-09-13 | Count |
|---|---:|
| diabetes, `LastUpdatePostDate` = 2026-09-13 (D+0) | **0** |
| diabetes, `LastUpdatePostDate` = 2026-09-12 (D−1) | **0** |
| diabetes, `LastUpdatePostDate` = 2026-09-11 (last business day) | **24** |

See Headline. The fix is "last business day," not "D−1."

### Category counts: frozen, exactly as the batch model predicts

| Category | 09-06 snap | 09-11 | 09-12 | **09-13** | Δ 24h |
|----------|-----------:|------:|------:|----------:|------:|
| T1D Cure & Cell Therapy | 156 | 157 | 158 | **158** | 0 |
| T1D Immunotherapy & Prevention | 77 | 77 | 77 | **77** | 0 |
| T2D Novel Therapies (Ph 2–3) | 152 | 150 | 151 | **151** | 0 |
| Diabetes Technology (Devices) | 245 | 246 | 244 | **244** | 0 |
| Diabetes Recently Completed w/ Results | 343 | 344 | 344 | **344** | 0 |

Five live queries replicating `baseline_clinical_trials.py` verbatim. All five unchanged.
**This is the first day in the series where a flat count genuinely means a quiet day** — and the
only reason we can say so is the batch finding. On a business day, a flat total still hides
gross change (09-12: net −1, gross ≥5). **[Certain]**

### Departures and new registrations: none

- Terminal-status query on the T2D Ph2–3 lane, `LastUpdatePostDate`RANGE[2026-09-12, 2026-09-13]
  → **0 records**.
- `AREA[Condition](diabetes) AND AREA[StudyFirstPostDate]RANGE[2026-09-12,MAX]` → **0 records**.

### Watch list: all seven records re-read in full, none changed

| NCT | Study | Status | Last update | Results |
|---|---|---|---|---|
| `NCT06926842` | ZUPREME-2, petrelintide, Ph2, n=221 | COMPLETED | 09-09 | none |
| `NCT06534411` | CagriSema vs tirzepatide, Ph3, n=1,023 | COMPLETED | 09-09 | none |
| `NCT06323161` | CagriSema vs placebo, Ph3, n=274 | COMPLETED | 09-09 | none |
| `NCT06797869` | CagriSema, T2D + neuropathy, Ph2, n=142 | COMPLETED | 09-10 | none |
| `NCT05872620` | ATTAIN-2, orforglipron, Ph3, n=1,613 | COMPLETED | 09-04 | **posted 09-04** |
| `NCT07797335` | AMBITION 7, zenagamtide, Ph3, n=1,778 | RECRUITING | 09-01 | — |
| `NCT04628481` | Ladarixin, T1D, Ph2, n=289 | TERMINATED | 08-31 | **posted 08-31** |

### ★ New: the ladarixin results are already public and the hub has been waiting for a paper

F-03 has read since 08-31 as "TERMINATED for futility; **still unpublished by anyone**." True of
the literature — `ladarixin` returns **0** PubMed records in 30 days. But `NCT04628481` carries
`hasResults: true` with `ResultsFirstPostDate = 2026-08-31`. **The 289-patient primary outcome
data has been publicly readable on the registry for 13 days.**

This is D-17 in a second costume. The hub keys "do we know the answer?" on publication, and the
registry results section is the earlier, freely available source. Reading it requires no paper, no
sandbox and no script. It is the single highest-value hour available today.

### Results window and blind spot: unchanged

`AREA[Condition](diabetes) AND AREA[ResultsFirstPostDate]RANGE[2026-09-09,MAX]` → **1** record
(`NCT05232071`, lanifibranor). Nothing new in 4 days.

```
  Structural invisibility, re-measured today — identical to 09-12
  ──────────────────────────────────────────────────────────────────
  diabetes, COMPLETED, completion date in 2026            246
    …with results posted (visible to collector #5)         12   ▏
    …invisible to all five collectors                     234   ████████████████████

  T2D Ph2–3 lane, first posted ≥2023, completed in 2026     22
    …with results posted                                    0
    …invisible                                             22   (100%)

  Legacy "blind spot" figure: 378 − 344 = 34; T1D 89 − 80 = 9   (retire — see D-11)
```

**[Certain — 8 `countTotal` reads today.]**

---

## 3. PubMed Highlights

Corpus unchanged since 2026-09-06 09:18: **139 papers, 16 alert domains, 30-day lookback**. Now
**7 days stale**. (Task spec says 15 domains; the script defines 16. Sixth report to note this.)

### PubMed does *not* share the registry's weekend pause

| `diabetes`, Entrez date | Count |
|---|---:|
| 2026-09-06 → 2026-09-13 | **1,223** |
| Fri 09-11 | 208 |
| Sat 09-12 | 3 |
| Sun 09-13 (today, D+0) | **141** |

PubMed has no D+0 lag and no weekend blackout — today's bucket is already populated. **The hub's
two upstream sources have different availability calendars, and a single freshness gate applied to
both will be wrong for one of them.** [Certain]

The corpus has seen none of the 1,223.

### New in the 09-12 → 09-13 window: thin, one item worth noting

Five targeted searches (tracked therapies; islet/beta-cell; T1D immunotherapy; health equity;
drug repurposing) over the two-day window returned six papers total, and the islet, T1D-immunology
and drug-repurposing sets were **empty**.

| PMID | What | Note |
|---|---|---|
| 42729683 | Oral small-molecule GLP-1 receptor agonists: a new frontier in cardiometabolic medicine. *Front Pharmacol* | Review; adjacent to the orforglipron file. Low priority — not primary evidence |
| 42730922 | Social determinants of health and dementia risk in people with and without T2D. *Aging (Albany NY)* | Equity × complications; two large cohorts |

Nothing at a Tier 1 intersection. Nothing on a tracked therapy that changes a tier.

### Tracked-therapy pulse, 30-day rolling

```
                  09-12   09-13
  retatrutide       15      14   ██████████████
  amylin class      11      11   ███████████
  orforglipron       6       7   ███████
  teplizumab         6       5   █████
  cagrilintide       6       4   ████
  ladarixin          1       0   ▏
  zimislecel         0       0
  ─────────────────────────────
  tirzepatide        —     126   (untracked; for scale)
```

Movement in both directions is expected — `reldate=30` is a rolling window, not a cumulative
count. **Do not read these deltas as publication events.** [Certain for the counts; the
09-12 column is inherited]

`tirzepatide` at **126** is shown deliberately: the molecule that received the most consequential
FDA action in the hub's scope this month is not in `KEY_THERAPY_TERMS`, and it out-publishes every
tracked therapy combined by roughly 3×. **New defect, D-23.**

### Amylin class: still zero coverage (D-13, unchanged)

`cagrisema OR cagrilintide` = **131** all-time, **4** in the last 30 days. None of the 16 alert
domains contains any amylin term.

### Reading queue: eleven deep, nothing left it

Carried verbatim from 09-12 plus one. Days unread as of today: PMID 42694848 (**7d**), 42627334
(7d), 42626948 (7d), 42673585 (7d), 42586227 (3d), 42607698 (**2d**), 42720752 (1d), 42722448
(1d), 42712437 (1d), 42608559 (1d), 42729683 (0d). The queue has grown every day since 09-06.

---

## 4. Gap Analysis Summary

Unchanged since 2026-09-08 03:17:27 (**5 days**). 30 domains, 435 pairs. Validation **BRONZE**.

| # (report) | Intersection | Gap | Joint | Doctrine Tier 1 |
|---|--------------|----:|------:|---|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | §6 Epidemiological (17/20) |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | §2 Literature Synthesis (19/20) |
| 3 | **Islet Transplant × Drug Repurposing** | 100.0 | 0 | **§4 Drug Repurposing (18/20)** |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | §6 (17/20) |
| 5 | Gene Therapy × LADA | 100.0 | 0 | §2 (19/20) |

### ★ M-04 resolved: the rank is not a ranking, and that is why three artifacts give three numbers

`gap_analysis_daily.py` line 294:

```python
ranked = sorted(gap_scores.values(), key=lambda x: x["gap_score"], reverse=True)
```

One sort key, no tie-break. **Twenty-one pairs score exactly 100.0** (grep of
`literature_gap_data.json`). Python's sort is stable, so all 21 come back in dictionary-insertion
order — i.e. the order the domains happen to be typed into the source file.

The three conflicting identifiers now have a single explanation:

```
  "Islet Transplant × Drug Repurposing" — one intersection, three ranks
  ──────────────────────────────────────────────────────────────────────
  literature_gap_data.json,  ranked_gaps[]           #5
  literature_gap_report.md,  after the filter        #3   ← drops IT×GWAS, IT×Personalized Nutr
  build_drug_repurposing_islet.py header             #4   ← an earlier run's ordering
```

All three are internally correct. **The rank is an artifact of insertion order and of which pairs
a downstream filter removes; it carries no information about relative research need.**
[Certain — code read, 21 ties counted, all three artifacts read]

*Resolution is not "pick a number."* It is: **stop using rank as an identifier.** Key each
intersection on the domain pair itself. Ranks among a 21-way tie must not be printed as though
ordered — and the report should say "21 pairs tied at the ceiling," not "top 5."

### ★ The score saturates, so it cannot discriminate

`Gap Score = max(0, 1 − joint / geomean(d1, d2)) × 100`

With joint counts of 0–3 and geometric means of 396–6,180, every one of the top 21 rounds to
100.0. `GWAS × CGM Technology` has **3** joint publications and still scores 100.0
(3 / 6,180.3 → 99.95). A metric on which 21 of 435 pairs tie at the maximum is not ranking them.

### ★ M-02 escalated: the Islet Transplant domain string sees 22% of its field

M-02 was logged as one anecdote ("islet transplantation" returns 2 where "islet transplant"
returns 0). Measured properly today, it is a domain-sizing error, not a rounding error.

```
  "Islet Transplant" field size, PubMed 2020-01-01 → 2026-09-13
  ─────────────────────────────────────────────────────────────────────────
  script string:  "islet transplant" OR "islet cell transplant"
                                                          253   ████
  "islet transplant"[Title/Abstract]                       145   ██
  "islet transplantation"[Title/Abstract]                1,134   ███████████████████
  "Islets of Langerhans Transplantation"[MeSH Terms]     1,131   ███████████████████
  union of TA forms + MeSH                               1,616   ███████████████████████████

  script captures 253 / 1,131 = 22% of the MeSH-indexed field
```

The script's 253 reproduces `individual_counts` exactly, so this is the right string — and the
right string is wrong. PubMed phrase matching does not stem *transplant* → *transplantation*, and
*transplantation* is the term the field uses. **Islet Transplant appears in four of the top six
gaps; all four rest on a denominator that is 4.5× too small.** [Certain]

`Health Equity` has the same shape, less severely: script string **2,067** today vs **6,189** when
widened with `"healthcare disparities"[MeSH]` and `"social determinants of health"` — **3.0×**.
Health Equity appears in five of the top twelve gaps (M-03).

### ★ But widening does not rescue the gaps — and that is the more important result

I ran narrow and widened joint counts for all five reported top gaps:

| Gap | Joint, script strings | Joint, widened | Verdict |
|---|---:|---:|---|
| 1 Beta Cell Regen × Health Equity | 0 | 1 | robust |
| 2 Insulin Resistance × Islet Transplant | 1 | **24** | **not robust** |
| 3 Islet Transplant × Drug Repurposing | 0 | **0** | **robust** |
| 4 Islet Transplant × Health Equity | 0 | 3 | marginal |
| 5 Gene Therapy × LADA | 0 | **0** | **robust** (see below) |

Gap #5 was tested four ways — narrow×narrow, wide×narrow, narrow×wide, wide×wide — and returns
**0 in all four**. Its two domain strings are also the only ones tested today that are *not*
badly undersized: Gene Therapy 2,366 → 2,956 (+25%), LADA 605 → 646 (+7%). **The undersizing
problem is domain-specific, not universal**, which matters: it means M-09 is a per-domain audit,
not a blanket rewrite.

Then I read the titles of the widened hits, and the widening is largely false positives. Of the
24 for Gap #2, the retrieved sample is dominated by broad reviews that mention both concepts —
*Regenerative medicine approaches for treating diabetes*, *Alternative therapeutic strategies in
diabetes management*, *Role of Cell-Based Therapies in T2D* — not studies of insulin resistance in
islet-transplant recipients. The closest genuine hit is PMID 41955087 (pre-transplant aerobic
exercise and glycemic outcomes after marginal islet mass transplantation, in rats). All three
widened hits for Gap #4 are similarly off-target; the nearest is *Ethical Considerations in Islet
Xenotransplantation*.

**So neither 0 nor 24 measures whether the intersection is under-researched.** Keyword-AND counts
co-mention, not co-investigation. Narrow strings undercount by missing the field's own vocabulary;
wide strings overcount by catching reviews. This is a **construct-validity** problem, and it
cannot be fixed by choosing better strings.

What survives: **Gap #3 and Gap #5 return 0 under both narrow and widened strings.** That is the
first evidence that distinguishes any gap from any other, and it favours the hub's lead
contribution candidate. It is a weak signal, but it is a real one and it is the right kind.

[Certain for all counts and for the code; **Likely** that the widened strings are more faithful
domain definitions; **Certain** that the widened *joint* hits are mostly not true intersections —
I read the titles]

### Carried, untouched

- **M-03 circularity test still unrun — twelve days.** `Analysis/Scripts/falsify_equity_gaps.py`
  exists and has never been executed. Today's Health Equity 3.0× finding makes it more urgent, not
  less: if the domain string is brittle *and* untested for circularity, five of the top twelve
  gaps have two independent unquantified errors.
- **F-12** (Islet Transplant × GWAS classification vs PMID 42722448) unresolved. Note it is
  `ranked_gaps[3]` in the JSON and absent from the report — the filter drops it.

---

## 5. Breaking News

**Nothing in the 7-day window (09-06 → 09-13) changes hub priorities.** Four searches run.
[Likely — negative result]

### ★ F-04 RESOLVED, with a primary source — the first fetched since 09-08

The Mounjaro CV contradiction is settled. **Eli Lilly investor release, dated August 28, 2026**,
fetched in full today: the FDA approved Mounjaro (tirzepatide) to lower the risk of MACE-3 in
adults with T2D at high CV risk. **The hub's 08-28 logging was correct.** The "expected H2 2026"
phrasing in 09-12's search results was stale secondary reporting. **E-01 also closes.**

**But the primary source corrects a claim the secondary coverage gets wrong**, and the hub would
have inherited it:

> SURPASS-CVOT (`NCT04255433`, n = 13,299, 30 countries, median follow-up 210.1 weeks) was a
> **non-inferiority** trial against Trulicity (dulaglutide), not placebo. Tirzepatide was
> non-inferior. **"Superiority to dulaglutide was not established."** HR 0.92, **95.3% CI
> 0.83–1.01** — the interval crosses 1.

The "8% lower rate of MACE" repeated across every secondary outlet is the point estimate of a
comparison that did not reach superiority. **Do not log this as an 8% benefit.** The defensible
statement is: non-inferior to an active comparator with established CV benefit, superiority not
demonstrated. New standing caution **E-06**. [Certain — primary source read in full]

### ★ A trap avoided, recorded so the next run does not re-flag it

A search for FDA diabetes approvals surfaced *"FDA Approves First Cellular Therapy to Treat
Patients with Type 1 Diabetes."* Fetched: it is **Lantidra (donislecel, CellTrans), approved
June 28, 2023**. It is **not** zimislecel and **not** news. Undated search snippets of this page
will keep resurfacing. [Certain — FDA press release read, dateline confirmed]

### Otherwise unchanged

- **Vertex zimislecel** — no filing announcement. Guidance remains "global regulatory submissions
  expected in 2026." Zero PubMed records in 30 days. FORWARD Phase 1/2 (NEJM, PMID 40544428,
  **12 patients, SILVER**) remains the entire evidence base. Watch stands. [Likely]
- **Novo / CagriSema** — NDA submitted 2025-12-18 (REDEFINE-1/-2), **no public PDUFA date**,
  decision anticipated late 2026. Four CagriSema-family registry records completed 09-09/09-10.
  Not in the tracker. [Likely — secondary sources; no primary Novo IR fetch this run]
- **Zealand / petrelintide ZUPREME-2** — topline still guided H2 2026, not released. Registry
  COMPLETED 09-09. [Likely]
- **Orforglipron / Foundayo** — approved 2026-04-01, chronic weight management only, not T2D.
- **Insulin efsitora alfa** — FDA decision possible H2 2026; still not on the watch list.
- **Retatrutide** — TRANSCEND-T2D-1 Phase 3 reported June 2026; still not logged.

---

## 6. Data Quality Defects — Current List

| # | Defect | Status | Age |
|---|--------|--------|----:|
| 6 | Freshness gate queries D+0 | **Re-scoped today: the D−1 fix is also wrong. Query the last business day, excluding federal holidays** | 5d |
| 8 | `LastUpdatePostDate` history not reproducible | Rule holds. **Mechanism now [Likely]: business-day batch re-dating.** Prediction logged for 09-14 | 4d |
| 11 | Terminal statuses absent from collectors — hole is 234, not 34 | Open, severity raised | 12d |
| 17 | Watches keyed on `ResultsFirstPostDate` cannot fire on completion | **Second instance found today: ladarixin registry results public 13 days** | 1d |
| 18 | Gap #3 / #4 / #5 numbering + BRONZE/SILVER conflict | **RESOLVED today: 21-way tie, no tie-break, insertion order. Fix is to stop using rank as an ID** | 1d |
| 23 | **`tirzepatide` absent from `KEY_THERAPY_TERMS`** — 126 papers/30d, and the month's biggest FDA action in scope | **New today** | — |
| 24 | **Gap domain strings undersize their fields** — Islet Transplant 22% of MeSH; Health Equity 33%. Four of the top six gaps affected | **New today; supersedes M-02** | — |
| 25 | **Gap Score saturates** — 21 of 435 pairs tie at exactly 100.0; the metric cannot discriminate at the top | **New today** | — |
| 26 | **Gap Score measures co-mention, not co-investigation** — construct validity, not calibration. Not fixable by better strings | **New today** | — |
| 1 | `clinical_trials_latest.json` a 58-day-old duplicate | Open | 58d |
| 12 | retmax ceiling discards 85.9% of matching records | Open | 12d |
| 13 | Amylin class uncovered in `therapy_hits` and all 16 alerts | Open | 3d |
| 16 | Dashboard builders repaired, never executed; `origin/main` frozen 146d | Open | 4d |
| 2 | `has_results` constant `False` in the snapshot schema | Open | 7d |
| 4 | Epigenetics + Drug Repurpose alert queries over-filtered | Open | 5d |
| 7 | Scheduled run precedes the daily registry batch | Open — same root cause as #6 | 5d |
| 10 | 41-day trial-snapshot hole (07-18 → 08-26) | Open, unbackfillable | 4d |
| 15 | No `estimand` field in the trial schema | Open | 2d |
| 3 | Null `title` on PMID 42698931 | Open, 1 of 139 | 7d |
| 5 | `phase` uses two null encodings | Open | — |
| 9 | Gap counts cited without the query string | Resolved for Gap #3; 434 pairs remain | 4d |
| 14 | Findings not carried forward | `open_findings.md` re-emitted, 2nd of 3 runs | 3d |
| 19 | **Sandbox mount failed 6 consecutive days** | Blocks every script item below | 6d |
| 20 | Tracker lock-held; backlog 12 days | Open | 12d |
| 21 | 09-07 test residue, 4 files | Open | 6d |
| 22 | `CONTRIBUTION_STRATEGY.md` 182 days old | Open | 182d |

---

## 7. Recommended Actions

Ranked. ▲ = new or re-ranked today. **Items 1–3 need no Python and no sandbox.**

1. ▲ **Read the ladarixin registry results** — `NCT04628481`, results posted **2026-08-31**,
   n = 289, TERMINATED for futility. The primary outcome data is public and free. Thirteen days of
   reports have described this trial as "unpublished." It is unpublished *in the literature*; the
   numbers are on the registry. One hour, closes F-03, no dependencies.

2. ▲ **Correct the freshness-gate fix before anyone implements it.** Not D−1 —
   **the last completed business day, excluding US federal holidays.** Implementing yesterday's
   version would have shipped a bug that fails every Sunday, Monday, and post-holiday run. One
   date function.

3. ▲ **Stop printing gap ranks as a ranking.** 21 pairs tie at 100.0; the order is insertion
   order. Replace the numeric ID with the domain pair, and have the report state the tie
   explicitly. This is a text-and-key change, and it is the thing that most obviously cannot
   survive peer review of a preregistration.

4. **Add the terminal statuses to collector #5 and drop the results requirement.** Two edits in
   `baseline_clinical_trials.py`. The status clause recovers 34; re-anchoring on
   `LastUpdatePostDate` instead of `ResultsFirstPostDate` recovers the other 200. Without it,
   running the scripts re-buries `NCT06534411`, a 1,023-patient Phase 3 head-to-head.

5. **Re-key the watch list on `OverallStatus`, and add a third key on `HasResults`.** D-17 has now
   produced two misses (ZUPREME-2 completion; ladarixin results). Three events matter —
   completion, results posting, publication — and the hub watches only the last.

6. ▲ **Re-derive every gap score with MeSH-anchored domain strings, then re-validate.** Islet
   Transplant is 4.5× larger than the script believes; Health Equity 3.0×. Do not just widen and
   re-run: **report the score under both string sets** and treat any gap that does not survive
   both as unsupported. Gap #3 and Gap #5 survive; Gap #2 does not.

7. ▲ **Record D-26 in the doctrine as a known limitation of the gap method.** Keyword-AND measures
   co-mention. Widening Gap #2 from 1 to 24 pulled in general reviews, not intersection studies —
   I read the titles. Any gap claim that reaches a preregistration needs a hand-screened
   denominator, not a count.

8. **Log the week's registry events in the tracker.** Clear
   `.~lock.Diabetes_Research_Tracker.xlsx#` first. Oldest first: Mounjaro CV label (08-28,
   **now confirmed against the primary source — log as non-inferiority, not an 8% benefit**),
   ladarixin BRONZE + results-posted (08-31), ATTAIN-2 + estimand (09-04), ZUPREME-2 completion
   (09-09), CagriSema cluster `NCT06534411` / `NCT06323161` / `NCT06797869` (09-09/10),
   zenagamtide `NCT07797335` (09-01).

9. **Run `falsify_equity_gaps.py`.** Twelve days P1; the script already exists.

10. ▲ **Add `tirzepatide`, `dulaglutide` and `semaglutide` to `KEY_THERAPY_TERMS`** (D-23), and the
    amylin class (`petrelintide`, `cagrilintide`, `amycretin`, `CagriSema`) with its own alert
    query (D-13).

11. **Run the two dead scripts — after #4.**
    ```
    python Analysis/Scripts/baseline_clinical_trials.py
    python Analysis/Scripts/hub_monitor.py
    ```
    58 days stale; repairs `clinical_trials_latest.json`; restores NCT-ID diffing.

12. ▲ **Give the freshness gate a per-source calendar.** PubMed indexes on Sundays (141 records
    today); the registry does not. One gate cannot serve both. D-06/D-07.

13. **Read PMID 42720752 (PROTECT per-protocol, teplizumab) and 42607698 (ACHIEVE-J).** Both
    Level 1b, both tracked therapies, both unread. Queue is eleven deep.

14. **Add an `estimand` field to the trial schema** (D-15); backfill ATTAIN-2.

15. **Raise `retmax` and page the alert queries** before re-running `baseline_pubmed_alerts.py`.

16. **Execute the repaired dashboard builders and push.** 146 days frozen.
    `verify_2026_09_12_repairs.py` first, then `run_quality_improvements.py`.

17. **Pin the query string next to every gap count** (D-09). 434 pairs remain.

18. **Fix the two over-filtered alert queries** and **`has_results`** (D-04, D-02).

19. **Read the blind-spot records**, starting with `NCT06534411`.

20. **Replace consecutive-day diffing with a persistent seen-set** keyed on `overall_status`,
    `results_posted`, `last_update_posted`.

21. **Retire the "34 invisible records" figure** in favour of 234/22.

22. **Delete the 09-07 test residue** (4 files, 6 days). **Refresh `CONTRIBUTION_STRATEGY.md`**
    (182 days). **Add insulin efsitora alfa to the watch list.** **Track `NCT06239636` by NCT ID.**
    **Look at `NCT07808385`** (Mayo, closed-loop in pregnancy with T1D).

23. **Fix the sandbox mount.** Six consecutive failed runs. Browser-driven API reads sustain review
    but cannot write snapshots, so the collection hole widens daily.

> **Note on the scheduled-task file.** `run_report_2026-09-12.md` asks, for the third day, that
> step 4 be repointed from the expired "PMIDs above 42000000" rule to
> `python Analysis/Scripts/audit_impossible_pmids.py`. Still outstanding. That file is outside the
> hub and only the user can edit it.

---

## 8. Self-Audit

- **I contradicted yesterday's top-three recommendation, and yesterday's evidence was not bad —
  it was insufficient in a specific, predictable way.** Two observations, both taken on weekdays,
  supported "D−1." A third weekday observation would have supported it again. Only a *weekend*
  observation could falsify it, and the schedule guaranteed one would arrive within days. The
  lesson is not that the 09-12 report was careless; it is that **a two-point trend read on
  consecutive business days cannot distinguish a lag from a calendar**, and the hub should have
  said so rather than calling it "the cheapest item."

- **I have logged a falsifiable prediction for Monday.** If the 09-11 and 09-10 buckets are
  unchanged again on 09-14, the batch explanation is wrong and I should be held to that.

- **The 22% figure for Islet Transplant is the strongest claim in this report and the one I would
  defend hardest.** MeSH `"Islets of Langerhans Transplantation"` is a curated field definition,
  not my phrasing, and it returns 1,131 against the script's 253. That is not a judgement call.

- **The widened *joint* counts are the weakest, and I said so before anyone asked.** I built those
  strings myself and then read the titles they returned, and most are not true intersections. If I
  had reported "Gap #2's joint count is really 24, not 1" and stopped there, it would have looked
  like a cleaner finding and been a worse one. The honest version — that neither number measures
  the thing — is less satisfying and more useful.

- **My first pass at the Gap #5 test was invalid and I caught it on review, not in the design.**
  I set the "widened" Gene Therapy and LADA strings equal to the narrow ones, then reported Gap #5
  as "robust to widening." It was robust to nothing — I had run the same query twice. Re-tested
  properly with four string combinations, it does hold at 0. **The conclusion survived; the
  evidence for it did not exist when I first wrote it down.** This is the exact failure M-05
  describes — a count asserted without its query string — committed while writing the section that
  complains about it.

- **Gap #3 and Gap #5 surviving both string sets is a genuinely positive result and I want to be
  careful not to oversell it.** Robustness to one alternative operationalisation is weak evidence.
  It is better than what the hub had this morning, which was nothing.

- **The 21-way tie was visible in every gap report ever generated.** Ten consecutive rows reading
  `100.0` is on the face of the artifact. Nobody looked at the column, including me until today.
  The Gap #3/#4/#5 conflict was tracked as a numbering bug for four days when it was a symptom.

- **One primary source fetched today, after five days of flagging that none had been.** It closed
  F-04 *and* overturned a figure — the "8% MACE reduction" — that four days of secondary-source
  reading had left standing. The cost of E-01 was not abstract.

- **The Lantidra false positive is worth as much as a real finding.** An undated 2023 FDA press
  release ranking in a 2026 search is a recurring failure mode for the news step, and the only
  reason it did not become a headline is that I fetched it.

- **What I did not do:** I did not verify the business-day pattern beyond one holiday and four
  weekend days, so "excluding federal holidays" generalises from n = 1 (Labor Day). I did not
  re-count cross-domain papers in the PubMed corpus (byte-identical, inherited: 20 of 139). I did
  not re-read `RESEARCH_DOCTRINE.md` this run. Novo, Zealand and Vertex claims rest on search
  summaries, not primary fetches.

- **This report has 23 action items. Items 1–3 need no Python, no sandbox and no unlock, and
  together they close one open finding, prevent one bug from being written, and remove one
  invalid claim from a preregistration-bound artifact.** If exactly one thing happens before the
  next run, it should be item 1 — because it is the only one that produces new knowledge about
  diabetes rather than about the hub.

---

## 9. Open Findings — condensed re-emission (2nd of 3 required runs)

Full ledger: `Analysis/Results/open_findings.md`. Changes today only.

**Closed today**

| ID | Finding | Resolution |
|----|---------|-----------|
| F-04 | Mounjaro CV indication — internally contradictory record | **FDA approved 2026-08-28.** Lilly IR primary source fetched. Hub's 08-28 log was correct. Secondary "expected H2 2026" reporting was stale |
| E-01 | No primary web source fetched since 09-08 | **Closed.** Two fetched today (Lilly IR; FDA Lantidra release) |
| M-04 | Gap numbering + tier conflict across artifacts | **Explained.** 21-way tie at 100.0, stable sort, insertion order. Three artifacts, three ranks, all internally correct |

**New today**

| ID | Finding |
|----|---------|
| F-14 | **Ladarixin registry results public since 2026-08-31** (`NCT04628481`, n=289). Hub has recorded it as "unpublished" for 13 days. Second instance of D-17 |
| E-06 | **SURPASS-CVOT did not establish superiority.** HR 0.92, 95.3% CI 0.83–1.01, non-inferiority vs dulaglutide. **Never quote "8% MACE reduction" as a benefit** |
| E-07 | **Undated FDA press releases resurface in dated news searches.** Lantidra (2023-06-28) surfaced today as a 2026 result. Verify datelines by fetch |
| M-09 | **Domain strings undersize their fields** — Islet Transplant 253 vs 1,131 MeSH (22%); Health Equity 2,067 vs 6,189 (33%). Supersedes M-02 |
| M-10 | **Gap Score saturates** — 21 of 435 pairs at exactly 100.0. No discrimination at the top |
| M-11 | **Gap Score measures co-mention, not co-investigation.** Widened joint hits are mostly general reviews. Construct validity, not calibration |
| M-12 | **Registry decay is business-day batch re-dating** [Likely]. Prediction logged for 09-14 |
| D-23 | **`tirzepatide` absent from `KEY_THERAPY_TERMS`** — 126 papers/30d |

**Unchanged and ageing:** F-01, F-02, F-03 (superseded by F-14), F-05 … F-13; M-03 (**12 days**),
M-05, M-06, M-07, M-08 (2 of 3); E-02 … E-05; D-01, D-02, D-04, D-05, D-06, D-07, D-10, D-11,
D-12, D-13, D-16, D-17, D-19 (**6 days**), D-20, D-21, D-22.

---

## Evidence & Provenance

| Claim | Basis | Level |
|-------|-------|-------|
| Weekend/holiday buckets read 0: 09-05, 09-06, 09-07, 09-12, 09-13, 08-29, 08-30 | 7 `countTotal` reads, `AREA[LastUpdatePostDate]RANGE[D,D]` | **Certain** |
| Business-day buckets: 09-04=799, 09-08=979, 09-09=1,165, 09-10=1,104, 09-11=1,165, 09-01=931 | 6 `countTotal` reads today | **Certain** |
| All five carried buckets identical to 09-12 readings | This report's reads vs `monitor_report_2026-09-12.md` §2, read directly | **Certain** |
| Batch re-dating is the decay mechanism | Inference from zero decay across a non-batch interval, n=1 interval | **Likely** |
| "Excluding federal holidays" | Generalised from Labor Day 2026-09-07 alone | **Likely**, n=1 |
| Diabetes slice: 09-13=0, 09-12=0, 09-11=24 | 3 `countTotal` reads | **Certain** |
| Category counts 158 / 77 / 151 / 244 / 344 | 5 `filter.advanced` queries replicating `baseline_clinical_trials.py` lines 34–51 verbatim | **Certain** |
| 0 departures, 0 new registrations in the 09-12→09-13 window | 2 `filter.advanced` queries | **Certain** |
| Seven watch records: status, last-update, results dates | Full record read today, `AREA[NCTId](…)`, 7 records | **Certain** |
| `NCT04628481` `hasResults: true`, `ResultsFirstPostDate` 2026-08-31 | Same read | **Certain** |
| 246 / 12 / 234; T2D lane 22 / 0 / 22; 378 − 344 = 34; T1D 89 − 80 = 9 | 8 `countTotal` reads | **Certain** |
| Results window since 09-09 = 1 record | 1 `countTotal` read | **Certain** |
| PubMed: 1,223 records 09-06→09-13; 09-11=208, 09-12=3, 09-13=141 | 5 `esearch` calls, `datetype=edat` | **Certain** |
| Therapy 30-day counts incl. tirzepatide 126 | 9 `esearch` calls, `reldate=30` | **Certain** |
| PMIDs 42729683, 42730922 — titles, journals | `esearch` + `esummary`, 5 windowed searches | **Certain** |
| Islet Transplant: script 253, TA-transplant 145, TA-transplantation 1,134, MeSH 1,131, union 1,616 | 6 `esearch` calls, 2020-01-01→2026-09-13 | **Certain** |
| Script string reproduces `individual_counts["Islet Transplant"] = 253` exactly | `literature_gap_data.json` read today | **Certain** |
| Health Equity 2,067 narrow / 6,189 widened | 2 `esearch` calls | **Certain** |
| Widened joint counts 1 / 24 / 0 / 3 / 0 | 5 `esearch` calls | **Certain** |
| Gap #5 = 0 under all four string combinations; GT 2,366→2,956, LADA 605→646 | 8 `esearch` calls (re-run after the first attempt reused the narrow strings) | **Certain** |
| Widened joint hits are mostly general reviews, not intersection studies | `esummary` titles read for the Gap #2 and Gap #4 widened sets | **Certain** for the titles; **Likely** as a characterisation of all 24 |
| Widened strings are the more faithful domain definitions | My construction; MeSH-anchored for Islet Transplant only | **Likely** |
| Sort has one key, no tie-break | `gap_analysis_daily.py` line 294, read | **Certain** |
| 21 pairs score exactly 100.0 | Grep of `literature_gap_data.json`, `"gap_score": 100.0` | **Certain** |
| `ranked_gaps[]` order: BCR×HE, IR×IT, IT×GWAS, IT×PersNutr, IT×DR, IT×HE, … | `literature_gap_data.json` lines 912–999, read | **Certain** |
| Report order drops IT×GWAS and IT×PersNutr | `literature_gap_report.md` lines 35–44, read | **Certain** |
| `build_drug_repurposing_islet.py` says "Gap #4" | Inherited from `monitor_report_2026-09-12.md` §4 — **not re-read today** | Inherited |
| Gap Score formula | `literature_gap_report.md` line 15 + `gap_analysis_daily.py` line 289 | **Certain** |
| Mounjaro CV indication approved 2026-08-28; SURPASS-CVOT non-inferiority, HR 0.92 (95.3% CI 0.83–1.01), superiority not established, n=13,299 | **Eli Lilly investor release, fetched in full today** | **Certain** — primary |
| Lantidra approved 2023-06-28, CellTrans, n=30 | **FDA press release, fetched in full today**, dateline confirmed | **Certain** — primary |
| Vertex, Novo/CagriSema, Zealand status | Web search, secondary sources | **Likely** |
| Cross-domain count 20 of 139 | Corpus byte-identical; **not recounted** | Inherited |
| File ages | Internal `generated` fields read today + directory listings; OS mtimes unreadable | **Certain** where the field exists |

No snapshot was written this run — no Python executed, and review runs do not modify hub files.

**Sources.** ClinicalTrials.gov API v2 (`https://clinicaltrials.gov/api/v2/studies`) — 31 live
queries. PubMed E-utilities `esearch`/`esummary`
(`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`) — 39 queries. Primary web fetches — 2
([Eli Lilly investor release, 2026-08-28](https://investor.lilly.com/news-releases/news-release-details/fda-approves-lillys-mounjaro-tirzepatide-reduce-cardiovascular);
[FDA press release, Lantidra, 2023-06-28](https://www.fda.gov/news-events/press-announcements/fda-approves-first-cellular-therapy-treat-patients-type-1-diabetes)).
Web search — 4 queries. Local files read: `monitor_report_2026-09-12.md`,
`run_report_2026-09-12.md`, `open_findings.md`, `clinical_trials_latest.json`,
`pubmed_recent_latest.json`, `literature_gap_data.json`, `literature_gap_report.md`,
`baseline_clinical_trials.py`, `gap_analysis_daily.py`, directory listings.

*Generated by the Diabetes Research Hub automated monitor — 2026-09-13*
