# Daily Iteration Report — 2026-08-15 (Saturday)

**Focus:** corpus integrity. Two findings that change what the hub claims.

---

## 1. Full-corpus PMID verification sweep — 287/287 verified

All 287 corpus PMIDs were bulk round-tripped through NCBI E-utilities `esummary`
(100 IDs per request, 3 requests total) and matched against the stored
title/journal/year.

| Check | Result |
|---|---|
| PMIDs resolved on live PubMed | **287 / 287** |
| Unresolvable / fabricated | **0** |
| Real title drift | **0** |
| Papers newly flipped to `pmid_verified: true` | **111** |

The single title mismatch, PMID 35098372, is a house abbreviation
(`"Intra-lymphatic GAD-alum in T1D: long-term follow-up + late booster (DIAGNODE Ext)"`
vs the full PubMed title) — same record, annotated, not drift. Eleven papers had
been carried with `pmid_verified: false` since 2026-05-02/03; all eleven are real.

**Method note:** bulk `esummary` is dramatically cheaper than per-paper web search
and should be the default vetting path going forward. Paper vetting is now caught up.

---

## 2. Systematic extraction artifact — 5 paths, one source paper

**Finding:** five research paths drew *100%* of their corpus support from
comparator-arm dose labels in a single paper.

The paper is **PMID 35466661** — Dutta D et al., *J Postgrad Med* 2022;68(2):85-92,
a systematic review and meta-analysis of hydroxychloroquine in T2DM (11 RCTs,
n=2723). Its trial-characteristics table lists comparator and background drugs
with dose strings. The extractor read those dose strings as mechanistic claims and
minted drug → outcome edges from them.

| Path | dpc | Backing text | Caught by old filter? |
|---|---|---|---|
| atorvastatin → T2D | 1 | `"400 Mg in"` | yes |
| metformin → inflammation | 1 | `"on metformin 1000 mg/day"` | yes |
| pioglitazone → inflammation | 1 | `"400 mg OD"` | yes |
| **hydroxychloroquine → inflammation** | 2 | `"on metformin 1000 mg/day"`, `"400 mg OD"` | **no** |
| **pioglitazone → T2D** | 3 | `"400 mg OD"`, `"45 mg OD"`, `"400 mg OD"` | **no** |

The 2026-05-14 filter required `data_point_count == 1`, so the last two escaped.
Note that `pioglitazone → T2D` reached dpc=3 partly on an **exact duplicate** —
`"400 mg OD"` counted twice. Data-point count is not a proxy for evidential weight
when the points can be duplicates from one table.

**Fix applied** to `build_research_paths.py`:
`is_dose_fragment_artifact()` now fires whenever *every* key_claim is a
non-mechanistic dose fragment, at any dpc. Conservative by design — one mechanistic
snippet anywhere exempts the path.

Regression-checked: `rapamycin → islet_transplant`, `oxidative_stress → T1D`,
`oxidative_stress → beta_cell`, `metformin → T2D`, `hydroxychloroquine → T2D` all retained.
Dashboard goes 47 → 42 paths.

**Scope limit:** this removes only the unsupported *corpus-side* signal. Four of the
five paths have independent external validation with real meta-analysis PMIDs; those
ratings are sourced separately and are unaffected.

Also corrected a factual mis-annotation in the script comment: PMID 35466661 had been
labelled "HCQ HYQ-Real-World Study." It is a systematic review and meta-analysis.

---

## 3. Path downgrade — pioglitazone → inflammation

**VALIDATED (HIGH) → PARTIALLY_VALIDATED (MEDIUM).**

The stored claim was *"PPARγ activation reduces hs-CRP, IL-6, TNF-α independently of
glucose lowering,"* supported by four bare URLs. Checked against the pooled evidence:

**What holds — CRP lowering, replicated across three independent meta-analyses:**

| Source | Design | Result |
|---|---|---|
| PMID 25897968 (PLoS One 2015) | 27 RCTs, TZD vs placebo, T2DM | hsCRP SMD **−0.65** (95% CI −0.98, −0.32) |
| PMID 20926154 (Diabetes Res Clin Pract 2010) | 36 pioglitazone studies | Pioglitazone CRP SMD **−0.577** (−0.732, −0.421) |
| PMID 16490432 (Am J Cardiol 2006) | TZD vs placebo | CRP **−0.82 mg/L**; diabetic subgroup **−1.24 mg/L** (p=0.008) |

**What does not hold:**

- **IL-6 — null.** PMID 25897968 finds IL-6 not significantly affected; for
  pioglitazone specifically the authors state it *"reduced serum hsCRP and MCP-1 but
  had no marked effects on MMP-9, IL-6 and ICAM-1."*
- **TNF-α — no source.** It was never a pooled endpoint in any of the three MAs.
  This claim traced to nothing.
- **PAI-1 / vWF / fibrinogen reductions are rosiglitazone-specific**, not pioglitazone.
- *"Independent of glucose lowering"* rests on PIONEER (JACC 2005, pioglitazone vs
  glimepiride at matched HbA1c) — a single trial, not pooled.

The MA's own conclusion is *"limited evidence."* The four bare URLs were replaced with
the three real MA PMIDs. Next revalidation due 2026-11-15.

---

## 4. Stale hardcoded counts removed

`run_quality_improvements.py` stage labels asserted counts that no longer matched reality:

| Label claimed | Actual |
|---|---|
| "48 paths, 25 validated" | 42 paths, 22 validated |
| "202 papers" | 287 |
| "472 data points from 61 papers" | 490 from 62 |

Replaced with pointers to the builder's own printed output so they cannot drift again.

---

## 5. Credibility sweep — CLEAN

- No PMIDs above the 42M tripwire cited in any `.py` (max script-cited value unchanged).
- The 13 corpus PMIDs above 42M (42021540–42160884) all resolve as real 2026 records —
  **6th consecutive reconfirmation that the numeric cutoff heuristic is stale.** Correct
  test remains: does it round-trip through `esummary`, and does title/journal/year match.
- `"curative"` / `"zero rejection"` hits occur only inside the `verify_before_deploy.py`
  detector regex, not as claims.

## 6. Pipeline — 41/41 `[OK]`

---

## Blocker requiring your action

**Git commit and push remain blocked.** The sandbox cannot write to `.git/`:

```
warning: unable to unlink '.git/objects/7d/tmp_obj_P5BoYe': Operation not permitted
fatal: Unable to create '.../.git/index.lock': File exists.
```

`.git/index.lock` does not appear in a directory listing but git still sees it — consistent
with OneDrive sync holding a phantom entry. All work is saved to the workspace folder.
To publish, run locally:

```powershell
cd C:\Users\justi\OneDrive\Diabetes_Research
Remove-Item .git\index.lock -Force -ErrorAction SilentlyContinue
git add -A
git commit -m "Daily iteration 2026-08-15: 287-PMID verification sweep; fix comparator-arm extraction artifact; downgrade pioglitazone->inflammation"
git push
```

---

## Next run queue (top items)

1. **[P2]** Audit every path whose corpus support is a single SR/MA — the 35466661
   pattern is unlikely to be unique. Also de-duplicate identical `matched_text` within
   a path; `data_point_count` is currently inflated by exact duplicates.
2. **[P4]** Re-validate `oxidative_stress → T1D` and `oxidative_stress → beta_cell` —
   both VALIDATED/HIGH on one corpus PMID each with external support recorded as bare
   URLs, the same weakness just found in pioglitazone → inflammation.
3. **[P5]** Gap #2 audit due ~2026-08-27; Gap #1 due ~2026-08-29.
4. **[P6]** Resolve the 13 FLAGGED papers — 10 off-topic oncology/neurology, 27512794
   missing title/journal, and 35437333 / 41827829 have empty `issues_found` and need a
   reason recorded or should be un-flagged.

*Research synthesis, not medical advice.*
