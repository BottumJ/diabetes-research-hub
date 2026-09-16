# Daily iteration — 2026-09-10

**Environment: degraded, second consecutive day.** The Linux sandbox failed to mount on
three attempts with the same error as 2026-09-09 (`source path ... is under Plan9 share
"c" which is not mounted`). No Python ran. Steps 3 and 5 of the task — extraction pipeline
and `run_quality_improvements.py` — were not executed. Step 4, the credibility sweep, was
executed by grep instead of by script and is clean. Everything below was done with file
tools, grep and web search.

---

## The headline: the sweep found something bigger than the PMID it was looking for

The P1 item asked for the remaining ~28 attachments of **PMID 32175717** (Khan MAB et al.,
*J Epidemiol Glob Health* 2020;10(1):107-111 — a Global Burden of Disease analysis of type 2
diabetes **prevalence**, containing no cost data and no type 1 data).

Its proposed test was mechanical: flag any attachment whose surrounding text contains a
currency symbol or "T1D". **The test worked perfectly — 19 live attachments across seven
builders, every one a true positive, no false positives.**

Then four of those 19 turned out to sit inside something else.

### Four "methodology references" blocks, 18 of 19 citations false

Four dashboards each carry a small block of small grey text near the footer, titled
*Statistical Methodology References*, *Corpus Methodology & References*, *Key References*,
or *Platform References*. Across all four, **eighteen of nineteen citations were false**,
and the falseness has one shape: a few health-economics papers from this corpus, attached
to whatever method the sentence happened to name.

| Sentence claims | PMID cited | What the PMID actually is |
|---|---|---|
| DerSimonian-Laird estimators | 29710129 | Total Costs of CAR-T Immunotherapy, *JAMA Oncol* 2018 |
| Pooled HbA1c effect sizes | 34763823 | Why is Insulin So Expensive (pricing review), 2021 |
| Pooled HbA1c effect sizes | 37909353 | Economic Costs of Diabetes in the U.S. in 2022 |
| Bayesian priors from systematic review evidence | 32175717 | GBD analysis of T2D prevalence, 2020 |
| Biomedical text-mining methodology | 29710129 | CAR-T costs (again) |
| WHO research taxonomy / mapping reviews | 34763823; 37909353; 32175717 | the same three cost papers |
| Term frequency & network analysis | 37105208 | CITR islet graft-function cohort, *Lancet D&E* 2023 |
| **"IDF Atlas 10th ed."** | **37105208** | **the same CITR cohort study** |
| STRING protein-interaction database | 36449148 | Dorzagliatin: First Approval, *Drugs* 2022 |
| Network-pharmacology methodology | 30899369 | Metformin / M2 macrophage / NLRP3 bench study |
| Islet immunosuppression & IBMIR | 29710129; 32175717 | CAR-T costs; T2D prevalence |
| Calcineurin-sparing combination rationale | 37359825 | **correct** — retained |

Two are worse than loose attachment; they **name a source the PMID is not**, in text a
reader sees. The main Research Dashboard labels PMID 37105208 as *"IDF Atlas 10th ed."*
It is a Collaborative Islet Transplant Registry cohort study.

And one is worse still. The same dashboard cited PMID 32175717 for:

> Validation methodology follows triple-source framework aligned with Oxford CEBM evidence levels

The triple-source framework is **this project's own construct**, defined in
`RESEARCH_DOCTRINE.md` — and that definition is itself under an open queue item since
2026-08-31, for counting three documents about one 12-patient trial as three independent
sources. Putting an unrelated PMID beside a house rule made it look externally validated.
All four blocks were withdrawn and replaced with plain statements of what the pipeline
actually does.

**Why the existing gate missed all of this:** `audit_prose_citation_titles.py` only checks
references that assert an identity. "Methodology adapted from biomedical text mining
approaches (PMID X)" asserts nothing about what X *is*. This is the 73.7% coverage blind
spot recorded on 2026-09-08, hit again — and it is the reason the pattern survived in four
files for months.

---

## Two claims corrected rather than stripped

Both had the right source already in the paper library, and both were **also misstated** —
each converted a *relative risk reduction* into a *proportion of patients benefiting*.

**Fenofibrate / FIELD.** Was: "prevents retinopathy progression in 30% of patients
(FIELD trial) [PMID:32175717]". Now sourced to **PMID 16310551** (Keech, *Lancet* 2005) and
restated: reduced the proportion needing retinopathy laser treatment from **5.2% to 3.6%**
over 5 years — a 31% relative reduction, **1.6 percentage points absolute, NNT ≈ 63**
(n=9795, p=0.0003).

**Losartan / RENAAL.** Was: "prevents doubling of creatinine in 25% of patients (RENAAL)
[PMID:32175717]". Now sourced to **PMID 11565518** (Brenner, *NEJM* 2001) and restated: a
**25% risk reduction** in doubling of serum creatinine (n=1513, mean 3.4 years, p=0.006).

The two "cost per year of protection" ratios beneath them (<$100 vision, <$150 renal) were
withdrawn: both divided an unsourced drug price by an unsourced complication cost.

---

## Incidental find: the LADA screening table contradicts itself

`build_lada_diagnostic_model.py` prints a base of **28,000,000** annual global adult-onset
diabetes diagnoses, applies 9.7% LADA prevalence, and prints **4,850,000**.

    9.7% of 28,000,000 = 2,716,000
    4,850,000 / 0.097   = 50,000,000

Every row below — detected cases, additional cases found by screening, $1B screening cost,
$42.5B complications averted, $32.5B net savings, 11.9M QALYs — inherits an undisplayed base
of 50 million. The table's impact numbers are ~1.8× what its own stated base supports.
Flagged in place with `[BASE MISMATCH]`, **not reconciled** — choosing the base is a
modelling decision, not a repair. The 28,000,000 figure is now unsourced anyway (it was
falsely cited to 32175717, which reports prevalence and no incidence count), so sourcing
the base is the first step and may settle it.

---

## Yesterday's P1 item was fixed three weeks ago

The 2026-09-09 run queued at P1: replace the stale *"PMIDs above 42000000 are fabricated"*
rule with a live resolution check. **That work landed on 2026-08-25/08-31.**
`pmid_ceiling.py` resolves the ceiling from PubMed at runtime; `audit_impossible_pmids.py:99`
reads it; `run_quality_improvements.py:292` wires it in. The only surviving literal
`42000000` is in the report's `superseded_rule` metadata, where recording a retired rule is
correct. **Item closed as already done.**

The mechanism matters more than the item. The stale rule lives in the **scheduled task
file**, which every run reads and no run can edit. So each run re-derives that it is stale
and re-queues the fix — and a run without Python (two days now) cannot inspect the gate to
discover the fix already exists. **This will repeat daily until the task file's Step 4 is
edited.** Raised as P0.

---

## External check: Ver-A-T1D unchanged; a new meta-analysis is missing from the corpus

NCT04545151 is COMPLETED (registry verified May 2026); results were presented at EASD
Vienna, September 2025; coverage describes the adult C-peptide effect as uncertain-to-modest
against a positive pediatric result. **Still no PubMed-indexed primary-results paper.** The
four standing human-call items that depend on it remain blocked.

New and actionable: **PMID 37583402**, *"Verapamil improves One-Year C-Peptide Levels in
Recent Onset Type-1 Diabetes: A Meta-Analysis"* — directly on the #4/#5 paths' own question
and **not in this corpus**. It appears only in two citation caches, meaning a citation tool
has seen the PMID without the paper ever being ingested. Added as UNVETTED, high priority.
Deliberately not wired into the paths: before it can count, it must be checked for **trial
overlap with PMID 40111679** (the existing external anchor). Two meta-analyses pooling the
same RCTs are not two independent sources — that is precisely the defect the 2026-08-31
doctrine item names.

---

## Files changed

| File | Change |
|---|---|
| `build_generic_drug_catalog.py` | 9 false attachments removed; 2 claims re-sourced and restated; 2 ratios withdrawn; `.unsourced` CSS added |
| `build_cart_access.py` | T1D lifetime-insulin denominator unsourced; "The Math" caveated; CSS added |
| `build_lada_diagnostic_model.py` | 3 attachments removed; `[BASE MISMATCH]` flag; CSS added |
| `build_lada_prevalence.py` | dialysis cost unsourced; CSS added |
| `build_gka_landscape.py` | metformin price unsourced; CSS added |
| `build_statistical_analysis.py` | methodology block withdrawn (4 of 5 false) |
| `build_corpus_analysis.py` | methodology block withdrawn (5 of 5 false) |
| `build_repurposing_dashboard_v2.py` | references block repaired (4 of 5 false) |
| `rebuild_research_dashboard.py` | platform references withdrawn (5 of 5 false) |
| `agent_state.json` | run entry, 2 items resolved, 5 items queued, 1 paper added |
| `verify_2026_09_10_repairs.py` | **new** — host-side verification |

**34 citations removed. 2 re-sourced. 9 files.**

Five of those builders emitted `class="unsourced"` without ever defining a `.unsourced` CSS
rule — so `[UNSOURCED]` markers placed by earlier runs were rendering as unstyled text. Rule
added to each. Brace escaping checked per file (`build_lada_diagnostic_model.py` uses an
f-string stylesheet and takes doubled braces; the rest are plain strings).

---

## ⚠ Read this before trusting any of the above

**The builders were repaired but never executed.** No Python has run since 2026-09-08. The
generated HTML in `Dashboards/` and `docs/Dashboards/` still contains every false citation
removed on 2026-09-09 and 2026-09-10.

That is a worse state than uniform wrongness: a reader sees the old text while a grep of the
scripts reports it fixed.

Run on Windows, in order:

```
cd C:\Users\justi\OneDrive\Diabetes_Research
python Analysis\Scripts\verify_2026_09_10_repairs.py
python Analysis\Scripts\verify_2026_09_09_repairs.py
python Analysis\Scripts\run_quality_improvements.py
git add -A ; git commit -m "Citation repairs 2026-09-10" ; git push origin main
```

`agent_state.json` was hand-edited **without a JSON parser available**. Check 1 of the
verification script parses it; a dated `.bak_*` sibling is the recovery path if it fails.

**The push is still blocked — origin/main frozen at 2026-04-20, now 143 days.** Four days
running, this agent's entire substantive output has been reader-facing corrections that no
reader can reach. Today's batch raises the stakes: the live site currently shows a research
hub whose main dashboard cites a registry cohort study as the IDF Diabetes Atlas.
