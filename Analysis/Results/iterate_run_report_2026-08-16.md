# Daily Iteration Report — 2026-08-16 (Sunday)

**Headline:** Two working detectors were found reporting into a void. Seven real
miscitations — two of them plant-biology papers cited as diabetes trials — had
been sitting in the build scripts and on the live public site. Both loops are
now closed with hard gates.

---

## 1. Citation integrity breach

The daily credibility sweep passed, as it has every run: no PMIDs ≥ 42,000,000,
no forbidden phrases. It has been passing while seven genuine miscitations sat
in the build scripts.

`validate_citations.py` had been scoring them correctly as `MISMATCH` and
writing them to `citation_validation.json` for months. Nothing read that field.

| Cited PMID | Actually resolves to | Was cited as | Corrected to |
|---|---|---|---|
| 34299352 | *Medicago sativa* GRAS gene family | DIAGNODE-2 | **34021020** |
| 35491968 | *Capsicum* bacterial wilt resistance | GAD-alum meta-analysis | **35665810** |
| 19237585 | Nicotinic receptors / epilepsy | Lamkanfi glyburide–NLRP3 | **19805629** |
| 23223116 | Anesthesiology resident education survey | TINSAL-T2D salsalate RCT | **23817699** |
| 33515517 | Paediatric pneumococcal disease, Belgium | DIAGNODE-2 | **34021020** |
| 18794064 | Metastatic colon cancer treatment | Ludvigsson NEJM 2008 | **18843118** |
| 32243867 | Multiple sclerosis / MMP / vitamin D | ACTION LADA | **23248199** |

Every replacement was round-tripped through NCBI esummary and matched on author,
journal, year and topic before being written.

One claim was **de-cited rather than re-cited**: the "$100–200 autoantibody
testing cost" figure in `build_lada_prevalence.py` was attributed to ACTION LADA,
which does not establish it. No source was found that does, so the claim now
carries an explicit *uncited pending verification* marker instead of borrowing
authority from an unrelated paper.

**Root cause.** Detection was decoupled from enforcement. The sweep tested for
*fabricated* identifiers via a range check. A real PMID pointing at the wrong
paper passes every range check ever written.

**Side effect resolved.** This also explains a long-open question in the state
file: several off-topic oncology and infectious-disease papers sat in the corpus
flagged "unclear relevance to diabetes research." They were ingested *because*
they were miscited. The flagged papers were the symptom, not the disease.

**Fix.** `check_citation_mismatches.py` — reads `citation_validation.json`,
exits non-zero on any unwhitelisted MISMATCH, registered in the runner directly
after `validate`. Suppression requires a written reason. One entry currently:
`12345678`, a regex example inside a comment, not a citation.

Unresolved mismatches: **7 → 0**.

> Ordering matters and cost a debugging cycle: the claim inventory is cached in
> `pmid_verification.json` and `paper_library/index.json`. Editing a build script
> is not enough. `verify_pmids → ingest_papers → build_paper_library →
> validate_citations` must be re-run in that order or the validator re-reports
> already-fixed mismatches.

---

## 2. The public site had been frozen for four months

`docs/Dashboards/` is what GitHub Pages serves. It had not changed since
2026-03-29 / 2026-04-20.

```
stale = 33     missing = 2     in-sync = 0
```

Meanwhile `run_quality_improvements.py` reported *"All 42 improvements completed
successfully"* every single day. `rebuild_website.py` only ever wrote
`docs/index.html`; nothing copied the rebuilt dashboards across.

So the seven corrected miscitations were still live publicly, alongside a
DIAGNODE-3 description already superseded by the trial's futility closure.

**Fix.** `sync_docs_dashboards.py` — copies, then re-verifies byte equality, and
exits non-zero if anything failed to land. Registered **last** in the runner,
after `postprocess_dashboards.py`, which rewrites `Dashboards/*.html`. Now 35/35
in sync, and `--check` reports drift without writing.

This is the same failure class as the citation gap, found the same day: **a step
reporting success while the artifact a reader actually sees goes untouched.**
Verify the output changed, not that the producer exited zero.

---

## 3. GAD65 → T1D: **CONTRADICTED**

Confirmed by fetching two Diamyd primary-source press releases directly, rather
than relying on search summaries.

- **2026-03-27** — DIAGNODE-3 interim (174 of 321 randomised, 15 months, HLA
  DR3-DQ2 enriched) did not reach statistical significance on the primary
  C-peptide endpoint; pre-specified continuation criteria not met.
- **2026-07-27** — trial **closed for futility**. Structured review found no
  single cause, no material protocol violations, no new safety concerns.

Sponsor-offered contributing hypotheses — intralymphatic administration burden
at low-volume sites, longer diagnosis-to-treatment interval, lower drug-product
potency than DIAGNODE-2 — are **explicitly labelled hypothesis-generating by the
sponsor** and are recorded that way. They must not be reported as explanations.

**Scope discipline.** This contradicts *monotherapy in recent-onset T1D*. It does
not directly test LADA (no pivotal data exist), combination regimens, or
Stage 1/2 prevention. GAD65-targeted CAR-Treg work is a different modality and
is unaffected.

A dashboard claim was corrected: it had dated the discontinuation to April 2026
(unsupported) and overstated the subgroup finding as showing no effect in
pre-specified subgroups, where the sponsor reported underpowered numerical trends.

No peer-reviewed DIAGNODE-3 publication exists yet — queued as a monthly watch.

---

## 4. Paths validated

Chosen from the 14 that had **never** been validated, not from the re-validation
rotation.

**`colchicine → inflammation` — VALIDATED**
PMID 40083306 (Eur J Prev Cardiol 2026, randomised placebo-controlled, high-risk
T2D). Honest limits recorded: the CRP reduction is statistically significant but
numerically small, and adjusting for IL-1β change did not alter the
arterial-stiffness result — which argues against presenting NLRP3 → IL-1β as the
demonstrated causal chain for the vascular endpoint. No trial shows colchicine
preserves β-cell function.

**`alpha_lipoic_acid → diabetic_neuropathy` — PARTIALLY_VALIDATED**
PMIDs 22837391, 22331979, 37630823. The finding *is* the route split: IV 600 mg/day
× 3 weeks gives a clinically relevant reduction in neuropathic pain; oral — the
practically relevant route for chronic outpatient care — has unclear clinical
relevance. Not promoted, because the pivotal meta-analyses are 2012-vintage and
all endpoints are symptom scores and nerve-conduction velocity, with no hard
outcome such as ulceration or amputation.

---

## 5. Gap audits

**Gap #1 (Gene therapy for LADA) — REMAINS SILVER.** A 2026 *Diabetes Obes Metab*
review on CRISPR β-cell replacement and Treg modulation is T1D-scoped; LADA
appears only as a conceptual extension. Still zero LADA-specific gene-therapy
trials. The DIAGNODE-3 failure removes the most advanced antigen-specific
immunotherapy a LADA extension would have leaned on, which arguably *widens*
this gap.

**Gap #2 (Health equity) — REMAINS GOLD, now a demotion candidate.**
First concrete counter-evidence since the gap opened: **PMID 41587834**
(Ann Fam Med 2026;24(1):28-35) — a completed equity RCT, conditional pharmacy
vouchers in low-SES adults with uncontrolled T2D, n=186, HbA1c difference
0.7 pp (95% CI 0.3–1.2; P=.001). Added to the corpus as VETTED.

Held at GOLD: one 186-patient, 6-month, single-country trial on a surrogate
endpoint does not close a gap defined by the scarcity of equity interventions
with hard endpoints. Everything else surfaced is still protocol-stage. An
explicit demotion trigger is now recorded rather than left to drift: *a second
independent equity RCT reporting a hard clinical endpoint.*

> A secondary web source reported this paper as 24(2):140-148, DOI
> 10.1370/afm.250446. Both wrong. The live PubMed round-trip caught it.

---

## 6. Process defect: the queue could not see its own blind spot

14 of 57 paths had **never** been validated while the queue kept re-validating
paths already rated VALIDATED. The "pick the stalest path" heuristic ranks by
validation date — so a path with no date at all is invisible to it, permanently.

Never-validated paths now hold priority 2. A suspected alias-collision problem
was checked and dismissed: only `dorzagliatin → T2D` is double-keyed.

---

## Verification

| Check | Result |
|---|---|
| Citation MISMATCH gate | **0 unresolved** (was 7) |
| Published-site drift | **stale 0, missing 0, in-sync 35** |
| Fabricated PMIDs (≥ 42M) | none |
| Forbidden phrases | none |
| Miscited PMIDs in `docs/` | none |
| Pipeline | **43/43 [OK]** |
| Corpus | 288 papers — 275 VETTED, 13 FLAGGED |

---

## Blocked — needs you

`git` commit and push remain blocked by a stale 0-byte `.git/index.lock`
(2026-08-15). It cannot be removed from the sandbox: `rm` returns *Operation not
permitted* on the OneDrive mount.

**79 commits ahead of origin, 87 uncommitted files.** This run's corrections are
not backed up until this clears. On the Windows host:

```powershell
del "C:\Users\justi\OneDrive\Diabetes_Research\.git\index.lock"
git add -A ; git commit -m "Citation integrity + publish gates" ; git push
```

---

## Next run

1. Validate never-validated paths: `SGLT2i_NLRP3_DKD`, `NLRP3_inflammasome → DKD` — both are load-bearing for the SGLT2i/BHB/NLRP3 thesis and have never been externally checked.
2. Re-examine the 13 FLAGGED papers now that the root cause is known. Some should be purged; the CAR-T cost papers legitimately underpin Gap #6 access barriers and should be retained.
3. Run both new gates every run.
4. Watch for a peer-reviewed DIAGNODE-3 publication.
