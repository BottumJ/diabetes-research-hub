# Daily iteration — 2026-09-12

**Environment: degraded, fourth consecutive day.** The Linux sandbox failed to mount twice with
the same Plan9 `share 'c' is not mounted` error, attributed to the Windows update of 2026-09-08.
No Python ran. Steps 3 and 5 were not executed and no git operation was attempted. Step 2 was
skipped (Saturday; the weekly sweep is Mondays). Everything below was done with file tools, grep
and web search.

---

## The one thing worth reading

Four days of citation repairs now exist **only in the `.py` sources**. Not one builder has been
executed. Concretely, here is what a reader sees today versus what the source says:

| Published page shows | Source now says | Wrong by |
|---|---|---|
| UKPDS: 7% Hispanic | *(cell removed)* | UK classification has no Hispanic category |
| EMPA-REG: 4% Asian | 21.6% Asian | 5.4× understated |
| ACCORD: 25% Black, 12% Hispanic | 19.0%, 7.2% | +6 pts, +5 pts |
| 20 drug prices "from WHO model pricing (PMID:34763823)" | 20 prices `[UNSOURCED]` | Cited to an *insulin*-pricing review; no WHO extract exists in this repo |

One command closes that gap:

```
python Analysis/Scripts/verify_2026_09_12_repairs.py
python Analysis/Scripts/run_quality_improvements.py
```

---

## 1. The gate proposed yesterday would have made things worse

Yesterday's P1 item asked for a build gate firing on `needs manual verification`,
`needs verification`, `unverified`, `TODO`, `FIXME` in emitted HTML, and claimed it "would have
had a 100% hit rate" with "no false-positive class." It instructed that the pattern be measured
repo-wide first. That instruction is the reason this was caught.

**Measured. As specified, the gate is unsafe.** The bare term `unverified` is this repository's
own disclosure vocabulary. It fires on roughly eleven reader-facing strings, and none is a defect:

- the `UNVERIFIED` validation tier in the doctrine legend (`add_citations.py`, `verify_before_deploy.py`)
- the pricing-provenance disclosures the 2026-08-29 repair deliberately added (`build_drug_repurposing_screen.py`)
- the honest `[unverified]` label on the PROSPERO registration (`build_gap_synthesis.py`)

A gate failing the build on those punishes exactly the candour the 2026-08-27 and 2026-09-09 items
asked for.

**Narrowed — dropping bare `unverified` — the count is 3 repo-wide, all in tooling, and 0 in
builder-emitted text.** The four `(PMID needs manual verification)` parentheticals were one
author's habit in one block, removed yesterday. Nothing else ever used that phrasing. The 100% hit
rate was a sample of one.

*Recommendation:* wire in the narrowed pattern as a cheap regression stop, at **P2 not P1**,
expecting it to find nothing. Do not include bare `unverified`.

---

## 2. All four trial-demographics claims were unsourced; two were materially wrong

Every figure was attributed to the trial's **primary outcomes paper**, and none of those four
abstracts contains race or ethnicity data at all. So no cell was sourced, correct or not.

| Trial | Dashboard said | Published composition | Source it should have carried |
|---|---|---|---|
| ACCORD | 60 / 25 / 12 | 62.4 / 19.0 / 7.2 (+11.4 other), n=10,244 | PMID 37715820 |
| EMPA-REG | 75 W, 4 Asian | ~72 W, **21.6 Asian** (1,517/7,020) | PMID 28025462 |
| UKPDS | 81 W, 7 Hispanic | 82 White Caucasian, 10 Asian Indian, 8 Afro-Caribbean | PMID 7955993 |
| DCCT | 96 W | 96.5 W | doi 10.2337/dc24-0299 |

Three things worth flagging beyond the numbers:

- **The ACCORD error runs against the dashboard's own thesis.** Overstating Black and Hispanic
  enrolment makes the trial look *more* diverse. That rules out motivated reasoning and leaves
  invention.
- **UKPDS "7% Hispanic" is the one provably fabricated cell.** UK ethnicity classification has no
  such category, so no source could exist.
- **Two claims were withdrawn rather than re-sourced:** ACCORD's "heterogeneous treatment effects
  by race" (a results claim the paper does not make) and EMPA-REG's "subgroup analyses by race not
  consistently reported" (false — a dedicated Asian subgroup paper exists).

Also removed: DCCT's uncited "US Prevalence" column, and an entire **"SGLT2i Trials (2013+)"** row
that named no trial and carried no citation of any kind.

Confidence: **LIKELY, not CERTAIN** — replacements were read from named published analyses via web
search, not round-tripped through eutils, because there is no Python.

---

## 3. The 2026-09-10 sweep missed the largest target in a file it had already swept

`build_generic_drug_catalog.py` was swept two days ago: nine attachments of PMID 32175717 removed,
two prices marked `[UNSOURCED]` in the recommendation cards. **It left the main drug table alone.**

Under that table sat one line: *"Drug costs derived from WHO model pricing and generic
manufacturing data (PMID:34763823)."* Both halves false — that PMID is Herman & Kuo, *100 Years of
Insulin: Why Is Insulin So Expensive*, holding no price for colchicine, doxycycline or allopurinol;
and no WHO extract exists in this repo, as established on 2026-08-29.

That single note was sourcing **twenty prices**. For two days the page showed `$60/yr [UNSOURCED]`
in a card and `$60` presented as WHO-sourced in the table above it. A reader would believe the table.

Ten further live attachments of 34763823 were found in the same file and repaired: verapamil
$50/yr; the $2.6B / $300M development-cost figures (4 attachments); GLP-1 $10–15K and SGLT2i $5–8K
(4 attachments); generic $30/yr; India EML "below $1/month". **The file's own comment at line 991
already conceded the PMID was an insulin review being used beyond its scope** — known, written
down, shipped anyway.

---

## 4. A clean negative that should retarget the sweep

Two files on the sweep list came back clean:

- **`build_methodology.py` contains no PMIDs at all** — zero. It was flagged as "the
  highest-consequence one to be wrong" on account of 14 reference headings. Strike it from the list.
- **The drug catalog's structured per-paper data is clean**: 33 PMIDs across 20 drugs, no duplicate
  PMID anywhere (the mechanical no-lookup check), and four spot-checked trial-name assertions all
  correct — PROactive, CARDS, ENDIT, Cochrane pentoxifylline.

Yet the *same file* carried eleven false citations in its hand-written prose. The inference:
structured data was entered once, deliberately, per paper; prose citations were attached later to
numbers that already existed. **Future sweeps should go to the prose first.**

---

## 5. New defect class, flagged not fixed

`build_generic_drug_catalog.py` grades pentoxifylline **MODERATE**, citing the Cochrane review
(PMID 22336824) — whose own conclusion is that *"Evidence to support the use of pentoxifylline for
DKD was insufficient to develop recommendations for its use"*, with 13 of 17 studies not reporting
randomisation method.

The citation is correctly identified, so no existing gate catches it. The problem is **direction**:
a correctly-attributed source pointing the opposite way to the claim it supports. Neither
`audit_prose_citation_titles.py` (identity) nor the 32175717-style content test (topic) can see this.

Not regraded — that is a scientific judgement, and this is an unattended run. Queued at P2.

---

## Ledger

| | |
|---|---|
| Citations removed / re-sourced | 15 / 4 |
| Files repaired | `build_health_equity.py`, `build_generic_drug_catalog.py` |
| Queue items processed | 3 (2 resolved, 1 refuted-and-requeued) |
| Queue items added | 5 |
| Papers vetted | 0 (all 287 remain VETTED/FLAGGED; 0 unvetted) |
| Credibility sweep | CLEAN by grep — no `curative`, no `zero SAEs`, no cure claims |
| Pipeline rebuild | **NOT RUN** — no Python, fourth day |
| Git push | **NOT ATTEMPTED** — still blocked, origin/main frozen 145 days |

## Two things only you can do

1. **Run the pipeline on Windows.** `verify_2026_09_12_repairs.py` first (cheap, checks that four
   days of unexecuted edits still parse), then `run_quality_improvements.py`, then push.
2. **Edit the scheduled task file.** Step 4 still instructs a sweep for "PMIDs above 42000000",
   a rule that expired when PubMed crossed 42 million and that the repo fixed on 2026-08-25.
   Every run re-derives that it is stale and re-queues the fix. Point that step at
   `python Analysis/Scripts/audit_impossible_pmids.py` instead. Third day this has been asked.
