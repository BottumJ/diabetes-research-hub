# Platform Audit — Week of 2026-09-13

Diabetes Research Hub · `bottumj.github.io/diabetes-research-hub`

> **The .docx was not generated this run, and the reason matters.** The remote
> sandbox could not mount the repository: a Windows update released 2026-09-08
> broke the Plan9 share the workspace uses. Three identical failures, then I
> stopped retrying. Every measurement below was taken with direct file reads
> instead, so the findings are real; only the Word rendering is missing.
>
> The fix is `Analysis/Scripts/weekly_platform_audit.py`, written this run. It
> re-derives everything here on your machine and emits `Platform_Audit_Report.docx`,
> archiving the previous copy. Run it:
>
> ```
> cd C:\Users\justi\OneDrive\Diabetes_Research
> pip install python-docx
> python Analysis/Scripts/weekly_platform_audit.py
> ```
>
> That also removes the sandbox from the weekly critical path permanently, which
> is worth more than this week's document.

---

## The finding that should change what you do next

**`Dashboards/` and `docs/Dashboards/` have diverged in both directions. There is
currently no single source of truth for a dashboard's content.**

Not "docs is stale" — that was the 2026-08-16 defect and it had one direction.
This one runs both ways at once:

| Direction | Measurement | Consequence |
|---|---|---|
| Source ahead of published | `Dashboards/Methodology.html` cites 13 PMIDs; `docs/Dashboards/Methodology.html` cites 14 but hyperlinks **zero** | The published page shows citations a reader cannot click |
| Published ahead of source | **35/35** published dashboards carry the nav bar; only **11/35** source files do | The next `syncdocs` deletes the nav bar from 24 dashboards |

The second row is the live hazard. `postprocess_dashboards.py` injects the nav
bar into `Dashboards/*.html`, and `sync_docs_dashboards.py` publishes afterwards.
For 24 files the source has been rewritten by a builder since the last
postprocess pass. Nothing detects this, because `linkgate` validates `docs/` —
which is correct today — and no gate validates the source that `docs/` is about
to be overwritten from.

**Source files missing the nav bar (24):**
Acronym_Database, CART_Access_Barriers, Clinical_Trial_Dashboard,
Drug_Repurposing_Islet, Equity_Map, GKA_LADA, GKA_Landscape, GKA_Pricing,
Gap_Deep_Dives, Gap_Synthesis, Generic_Drug_Catalog, Health_Equity,
Immunomod_LADA, Islet_Transplant_Analysis, Islet_Transplant_Equity,
LADA_Natural_History, LADA_Prevalence, Medical_Data_Dictionary, Methodology,
Nutrition_Beta_Cells, Nutrition_LADA, PMID_Verification, Research_Dashboard,
Treg_Neuropathy

This repo's own doctrine is to close the *class*, not the instance. The class
here is: **a post-processing pass whose output a later builder can silently
revert.** Two ways to close it, in order of preference —

1. Move nav injection into the shared builder template, so it cannot be absent
   from a freshly built file. Post-passes that can be reverted are the wrong
   shape for an invariant.
2. If (1) is too large this week: add a pre-sync assertion that every
   `Dashboards/*.html` contains `<!-- DRH-NAV-BAR -->`, and fail the run. That
   is three lines and it is already scaffolded in the new audit script.

---

## Summary

| Check | Result | Status |
|---|---|---|
| Dashboards published under `docs/` | 35 | — |
| Nav bar + back-link, published copies | 35/35 | pass |
| Nav bar, source copies | 11/35 | **FAIL** |
| Back-link depth (`../index.html`) | 35/35 correct | pass |
| Landing-page dashboard links resolving | 34/34 | pass |
| Dashboards listed on landing page | 34/35 | **FAIL** — 1 orphan |
| Published dashboards with zero PMID hyperlinks | 3 | **FAIL** |
| Markdown reports the hub advertises | 2/2 present, 7 days old | pass |
| Muted text contrast `#636363` on `#fafaf7` | 5.75 : 1 | pass (AA 4.5:1) |
| CONTRIBUTING.md | present | pass |
| GitHub issue templates | 4 | pass |
| CITATION.cff | absent | fail (low) |

Findings open: **3 HIGH · 5 MEDIUM · 3 LOW**

---

## Priority actions

### HIGH

**1. Nav bar will be deleted from 24 dashboards on the next publish** — Navigation

Detailed above. Evidence: `<!-- DRH-NAV-BAR -->` present in 11/35 `Dashboards/*.html`,
35/35 `docs/Dashboards/*.html`.

*Clears when:* a full pipeline run reaches `postprocess` → `syncdocs` **and** a
pre-sync nav assertion exists, so the next occurrence fails loudly instead of
shipping.

**2. Three published dashboards cite no clickable source** — Citations

`Acronym_Database.html`, `Methodology.html`, `Prediction_Ledger.html` contain
zero `pubmed.ncbi.nlm.nih.gov` hyperlinks.

Two of these are defensible and should be *named* rather than left to look like
oversights: Acronym_Database is a terminology reference that asserts nothing,
and Prediction_Ledger records this project's own forward predictions, whose
evidence arrives at resolution. Methodology is not defensible — it carries 14
PMID mentions in prose, none of them linked, on the page that defines the
project's evidence standard.

*Clears when:* `convert_pmid_to_links()` runs over Methodology, and the other two
are added to a written exemption list. An exemption list that grows silently is
how a gate stops meaning anything; write the reason next to each name.

**3. Clinical trial snapshot is 58 days old and three different totals are in circulation** — Freshness

| Source | Figure |
|---|---|
| `docs/Dashboards/Clinical_Trial_Dashboard.html` (snapshot 2026-07-17) | "748+ trials" |
| `docs/social_media_launch_posts.md` | "746 clinical trials" (×3) |
| `docs/Dashboards/Gap_Deep_Dives.html` | "General T2D: 744 trials" |

The scheduled task asked whether 746 should be refreshed. The answer is that 746
is not the number the platform currently publishes — the dashboard says 748+, and
the outreach copy was never re-synced. A single stale number is a freshness
problem; three numbers that disagree is a provenance problem, and it is the more
serious of the two because a reader who checks two pages finds the platform
contradicting itself.

*Clears when:* `baseline_clinical_trials.py` re-runs, and the outreach copy reads
its total from the same artefact the dashboard does rather than from a literal.

### MEDIUM

**4. `Prediction_Ledger.html` is published but not linked from the landing page** — Navigation.
34 dashboard cards on `docs/index.html`, 35 files on disk. Reachable only by
guessing the URL. Either add the card or move the file out of `docs/`.

**5. PMIDs published as bare text rather than links** — Citations. Beyond the three
zero-link pages, several dashboards mix linked and unlinked citations. The exact
per-file count is measured by the new script; the cause is the same unfinished
postprocess pass as finding 1.

**6. Daily pipeline has not run in 5 days** — Freshness. `docs/index.html` declares
`Last updated: 2026-09-08`; the published reports declare `Generated: 2026-09-06`.
The pipeline is registered as daily (`register_daily_task.ps1`). Check the host
task, not the scripts.

**7. Duplicate-PMID review candidates** — Citations. Flagged for human review, not
gated. The heuristic is "one PMID, two materially different surrounding blocks
on the same page", which mostly surfaces legitimate repeat citations. The
authoritative check remains `audit_citation_identifiers.py`.

**8. Published site reachability is unverified this run** — Build integrity.
`audit_publish_reachability.py` recorded origin/main at 2026-04-20 and 101
commits behind as of 2026-09-06. I could not confirm the current state: browser
access to `bottumj.github.io` was declined during this unattended run, and the
sandbox was down. **If that gate is still red, every other finding in this report
describes a site no reader has loaded.** Check it first.

### LOW

**9. No `CITATION.cff`.** `CONTRIBUTING.md` §63 tells researchers how to cite in
prose. A `CITATION.cff` with the OSF DOI makes it machine-readable and gives the
repo GitHub's "Cite this repository" button — the single cheapest credibility
signal available to an independent project.

**10. No pull request template.** Four issue templates exist; the PR path has no
equivalent checklist, and PRs are where a contributor can actually break a gate.

**11. No `CODE_OF_CONDUCT.md`.** Expected for an open collaboration invitation.

---

## Areas checked clean

**Accessibility.** `#636363` on `#fafaf7` measures **5.75 : 1** — passes WCAG 2.1
AA for normal text (4.5:1), fails AAA (7:1). Computed, not estimated:
relative luminance 0.1247 and 0.9541 respectively, per WCAG's sRGB
linearisation. At 13px nav labels this is adequate; if you ever want AAA, `#595959`
gets you there without a visible change in character.

Nav groups carry `aria-haspopup` / `aria-expanded`, tab buttons carry `role="tab"`,
and `add_aria_labels()` adds `role="table"` and search-input labels. Table header
markup is present on the dashboards that use tables.

**Collaboration infrastructure.** `CONTRIBUTING.md` present and substantive — it
specifies that all quantitative claims cite a peer-reviewed source, prefers PMIDs,
accepts DOIs as fallback, and requires source-and-date for pricing data. Four
issue templates: `bug_report`, `data_error`, `feature_request`, `new_gap`. The
`data_error` template is the right one to have and most projects don't.

**Landing page integrity.** All 34 dashboard hrefs resolve to files under
`docs/Dashboards/`. Both advertised markdown reports resolve under `docs/Reports/`
and are 7 days old against a 30-day declared window — inside the window that
`audit_report_freshness.py` gates on.

---

## Method and limits

Every figure above came from reading the working tree directly. Stated plainly so
nothing here is over-read:

- **The build pipeline was not executed.** `run_quality_improvements.py` defines
  71 stages making several hundred live PubMed and ClinicalTrials.gov calls and
  rewriting the repo. An audit must not do that. Build integrity is inferred from
  artefacts, and the inference is stated: the nav and PMID-link gaps are what a
  pipeline that has not completed a postprocess pass looks like from outside.
  Run it separately and read its own SUMMARY block for stage-level pass/fail.
- **No PMID was resolved, checked for topic, or checked for retraction.** The repo
  has fourteen gates for that and they are better than anything an audit would
  improvise. This report checks only that citations are present, well-formed and
  clickable.
- **This reads the working tree, not origin.** See finding 8. That distinction is
  the whole point of `audit_publish_reachability.py` and it is not decorative.

Confidence: findings 1, 2, 4, 9, 10, 11 are **[Certain]** — direct file
measurement, re-derivable by running the script. Findings 3, 5, 6, 7 are
**[Likely]** — measured, but the interpretation of cause rests on reading the
pipeline's own documented ordering rather than on watching it run. Finding 8 is
**[Guessing]** on current state and **[Certain]** on the 2026-09-06 state recorded
in the repo; it is the one item where I could not get the evidence I wanted.
