# Decision Brief — 2026-08-31

**One decision unblocks seven.** The P1 queue has held 6–7 untouched HUMAN CALL items
since 2026-08-20. Each daily run has added one and resolved none. They are not seven
questions.

---

## The finding that reframes the queue

`RESEARCH_DOCTRINE.md` — the document that defines this project's citation standard —
contained **six misattributed PMIDs inside its own worked examples of correct citation.**
All six resolve on PubMed. That is why five months of automated runs walked past them.

| Where in the doctrine | Cited as | Actually is |
|---|---|---|
| "PMID-Verified (**Strongest**)" exemplar | $237bn US diabetes cost, CDC 2023 · PMID 35912345 | *Solvent Gaming Chemistry … Halide Perovskite Thin Films for Photovoltaics*, ACS Cent Sci 2022 |
| Correct-citation-**format** exemplar | Mehta et al., islet transplantation, Diabetes Care 2024 · PMID 38234567 | **RETRACTED**: *Ginsenoside Rg1 … Renal Ischemia/Reperfusion Injury*, Oxid Med Cell Longev 2024 |
| **GOLD**-tier exemplar, source 1 | Vertex Phase 3 zimislecel, NEJM 2024 · PMID 37234567 | *HPV self-sampling preferences among women in Minnesota*, Prev Med Rep 2023 |
| **GOLD**-tier exemplar, source 3 | Lancet expert commentary · PMID 37456789 | *Contact Guidance Drives Upward Cellular Migration*, Cell Mol Bioeng 2023 |
| **SILVER** exemplar, sources 1–2 | gene-editing papers · PMID 38234123 / 38345234 | HeartLogic heart-failure algorithm study; JoVE peptide-binding prediction |

`Research_Findings_Summary.md` — the public-facing summary — held four more, including a
**GOLD-rated** insulin icodec claim resting on a Lancet health-policy essay that contains
no icodec data, and a retatrutide weight-loss figure (28.7% at 68 weeks) that **appears
nowhere in the paper cited for it** (the trial ran 48 weeks and reported 24.2%).

All ten are repaired and re-sourced against the live PubMed API.

**Why nothing caught this:** every citation gate in the repo scans `.py` and only `.py`
(`verify_pmids.py:44`, `audit_prose_citation_titles.py:349`). The governing document and
the public summary had never been audited by anything.

---

## The decision

Re-sourcing the GOLD exemplar to the real trial exposed a defect in the **framework**, not
just the citation:

```
GOLD = "three independent peer-reviewed sources"

  Source 1  PMID 40544428  NEJM 2025    the FORWARD trial    ── 12 patients
  Source 2  PMID 41559876  Diabet Med   commentary ON it     ── same 12 patients
  Source 3  PMID 41638426  Diabetes Metab  review OF it      ── same 12 patients
                                                                ───────────────
                                          "three sources"       12 patients, ×3
```

The primary source is a **phase 1-2 trial of 12 full-dose patients** with interim,
non-prespecified analyses and two deaths — the doctrine called it "Phase 3". The two
confirming sources are commentary on it. The definition permits counting one study three
times, and did.

*(Separately: `10_Questions_Self_Audit.md` §38 had rated this same claim SILVER all along.
Two governing documents disagreed about the tier of the same claim and nothing noticed.)*

### → **Change GOLD to require three independent *datasets*, not three independent *documents*.**

This is the question all seven P1 items are asking. Answer it once here and most resolve
downstream:

| Standing P1 item | What it reduces to under the new definition |
|---|---|
| 2026-08-20 · 192/414 headline points are bare dose labels | Dose labels carry no dataset → not evidence |
| 2026-08-21 · 29/47 paths went hollow | Hollow = no dataset behind them → the suppression was correct |
| 2026-08-22/28/29 · verapamil ranks on a protocol | A protocol has no dataset → re-source onto CLVer (36826844), which is sitting unused in the library |
| 2026-08-27 · one review carries 91 claims | One document ≠ 91 sources |
| 2026-08-29 · Bayesian prior 62.3% discordant with design | The prior counts documents; make it count datasets |
| 2026-08-30 · three GOLD/SILVER gaps rest on one primary paper | Exactly what the new definition forbids |

**Cost of the change:** several GOLD claims demote to SILVER. **Cost of not making it:**
the tier labels measure citation density, which `10_Questions_Self_Audit.md` §38 already
suspected in writing.

---

## Shipped this run

- **`pmid_ceiling.py`** — the task file's "PMIDs above 42,000,000 are fabricated" rule was
  stale by 669,647 (live ceiling measured **42,669,647**). Now read from PubMed at runtime.
- **`audit_markdown_citations.py`** — closes the `.py`-only blind spot. It caught my own
  first round of fixes being silently reverted, because
  `Research_Findings_Summary.md` is *generated* by `add_citations.py`. Fixes moved into
  the generator.
- **`test_markdown_citation_gate.py`** — the new gate reports 0 findings, which proves
  nothing when the same run repaired everything it hunts. This replays the verbatim
  pre-repair text: 4 defects it must catch, 4 correct citations it must not. **8/8.**

The gate's first draft flagged **71 of 73 sites** — the same false-positive failure
`audit_prose_citation_titles.py` hit on 2026-08-26 and `audit_gap_evidence_design.py` hit
on 2026-08-30. A corpus-derived journal lexicon was then tried, measured (235 tokens,
14 findings, **all 14 false** — "drug" and "kidney" appear in journal names), and rejected
for a hand-verified alias list. Final: **0 of 61 flagged**, 8/8 on the fixture.

---

## Also worth your attention

**Baricitinib's benefit wanes.** PMID 42627334 (*Diabetes Care* 2026, BANDIT
post-treatment follow-up): C-peptide significantly greater at week 72 (0.54 vs 0.38
pmol/mL, P=0.015) but **not at week 96** (P=0.336). Authors conclude durable benefit
likely requires continuous treatment. The hub currently lists baricitinib as "Phase 2 data
promising" with no mention of this.

**The sweep did not find it.** It surfaced by accident while rechecking an unrelated watch
item. It published 2026-08-21, outside the 7-day window, and no active query covers
baricitinib or JAK inhibition.

**Three watch items sat 18–41 days past their recheck dates** while eight daily runs went
by. All three resolved on the first DOI query. Nothing reads the `next_recheck` field.

---

*Research synthesis, not medical advice. All claims trace to a source; all PMIDs verified
against the live PubMed API on 2026-08-31.*
