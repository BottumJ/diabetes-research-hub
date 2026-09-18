# ACTION REQUIRED — 2026-09-18

## The one thing only you can do

**Push.** From Windows:

```
cd 'C:\Users\justi\OneDrive\Diabetes_Research' ; git push
```

112 commits unpushed. `origin/main` tip is **2026-04-20 — 150 days old**. 38 of the
39 files under `docs/` are wrong for a reader: 4 return 404, 34 are stale.

The sandbox *can* commit — the `GIT_INDEX_FILE` workaround from 2026-09-16 still
holds and this run used it. What it cannot do is authenticate: HTTPS remote, no
credential helper, no `~/.git-credentials`, no `GH_TOKEN`. Provision a PAT for the
scheduled task and no human ever has to touch this again.

Everything below is real in the working tree and invisible on the site until you push.

---

## The finding of the day: a gate failed the pipeline on correct work, and its own output said so

`audit_citation_coordinates.py` failed the run with two live defects:

```
build_health_equity.py:1281        PMID 36215990
   ASSERTED  Lancet Diabetes Endocrinol 2022;10(10):741
   ACTUAL    Lancet Diabetes Endocrinol 2022;10(11):e11
   PROBE     coordinate resolves to PMID 36113507
```

Read the PROBE line. The gate had already gone to PubMed, resolved the disputed
coordinate, and found it belongs to **36113507** — which is the PMID of the very
reference block the coordinate sits in, five lines above. The repository wrote that
citation correctly. The gate cut its search window at the wrong boundary, handed
36113507's coordinate to the correction-note PMID that follows it, and then failed
the build. The second case, in `verify_2026_09_13_repairs.py:37`, is the same shape.

**The obvious response would have corrupted the repository.** A red coordinate gate
invites you to go fix the citation. Doing that here would have replaced two correct
citations with two wrong ones and turned the stage green.

Fixed by making the gate consult the answer it already had: `harvest()` now carries
every other PMID within 800 characters, and a coordinate the probe resolves to one of
them is `AMBIGUOUS_PAIRING` — printed in full, never failed. It does not mask
anything: a fabricated coordinate resolves to a paper that is *not* cited nearby, and
the neighbouring PMID's own coordinate is still harvested and checked on its own.

Gate now: **151 coordinates checked, 143 OK, 0 live failures.**

---

## Three live citations repaired — eight distinct errors inside them

The author-surname gate (built 2026-09-16, reporting only) had two live mismatches.
Neither turned out to be about a surname.

### 1. PREDIMED — `build_nutrition_lada.py`, two places

The page published:

> "PREDIMED Trial: Mediterranean diet reduced new-onset type 2 diabetes by **30%**…
> with extra-virgin olive oil **or nuts**. PREDIMED-Plus extended to 6+ years…"
> — *Salas-Salvado et al.*, cited as a **landmark trial**

Four errors. From this repository's own cached abstract of PMID 25940230:

| Claim on the page | What the cited paper says |
|---|---|
| "Salas-Salvado et al." | Martínez-González is first author; Salas-Salvadó is second |
| "landmark trial" | It is an **overview** of the trial in *Prog Cardiovasc Dis*, not the trial report |
| "reduced T2D by 30%" | **30% is the cardiovascular number** (HR 0.70, both diets). Diabetes: HR **0.60** (0.43–0.85) |
| "with EVOO **or nuts**" | The nut arm was **null**: HR 0.82 (0.61–1.10) |
| "PREDIMED-Plus … 6+ years" | A separate energy-restricted trial. Not in this citation. Withdrawn. |

Re-sourced with the denominator (273 cases among 3,541 participants) and both
confidence intervals visible.

### 2. DIAGNODE-2 — same file

Headed **"GAD-Alum Immunotherapy in LADA"**. PMID 34021020 enrolled **109 patients
aged 12–24 with recent-onset type 1 diabetes** (duration 7–193 days). LADA is
adult-onset. Also: attributed to "Casas/Ludvigsson" (Ludvigsson leads it), and
described as showing **"dose-dependent"** C-peptide preservation — the trial tested a
single dose and the subgroup was defined by **HLA DR3-DQ2 genotype**, not dose.

Re-sourced with the real result: primary endpoint **not met** (TER 1.091, 95% CI
0.845–1.408, P = 0.50); DR3-DQ2 subgroup TER 1.557 (1.126–2.153), P = 0.0078 on
n = 29 vs 17.

**Added, because two other files here already knew it and this one didn't:** the
confirmatory **DIAGNODE-3 Phase 3 was closed for futility in 2026**. The page was
publishing a promising subgroup signal with no mention that its replication failed.

### 3. The correction's own first draft was wrong

That repair initially asserted *"no GAD-alum trial in this repository's corpus
enrolled a LADA population."* `build_data_dictionary.py` names **Agardh et al.,
Diabetologia 2009 (PMID 19404608)**, n = 47 adult-onset autoimmune diabetes — primary
outcome **safety**, no between-group efficacy comparison. Caught by grepping the repo
for the claim before publishing it, and narrowed to the data dictionary's own precise
wording: *no adequately powered LADA-specific **efficacy** trial has reported.*

---

## New gate, and why it shipped with a fixture

The 2026-09-13 queue item asked for a gate on **a PMID attached to a number the
script computed itself** — a modelled cost dressed as a published one.

**First measurement: 13 hits. All 13 false.** The builders here write an entire HTML
page as one f-string, so `{COLORS['bg']}` at the top of the document was being paired
with a PMID four thousand characters below. Adding a 180-character proximity window
took it to 4; excluding `verify_`/`check_`/`reconcile_` diagnostics — which print
counts *about* PMIDs and are the opposite of the defect — took it to **1**, a
synthetic-data report whose PMID sources the effect sizes rather than the sample count.

Had this shipped on the first measurement it would have failed the build on 13
non-defects and been switched off within a day. **Measure-first has now earned its
keep four times.**

One further problem: the original live defect had already been repaired, so the gate
would have shipped having never caught anything — and a gate that has only ever
returned zero is indistinguishable from a broken one. The 2026-09-13 defect is now
reproduced verbatim in `_tmp_gate_known_positive.py`, excluded from normal runs,
which the gate must always flag. **Every gate added from here on should ship with a
fixture it must catch.**

---

## Pipeline

**76 of 79 stages run; 74 OK.** Zero builders fail to parse. Credibility sweep clean
(PMID ceiling is measured at runtime — 42,744,765 — so the task file's hard-coded
"42000000" is stale and the gate is right, not the doctrine).

Three stages not green, none of them new:

- `gapdata` — **skipped.** A 240 s network-bound slice; the host caps a tool call below that.
- `gapsubject` — **fails, and was already failing on 2026-09-07** with the same 9 findings.
- `publishgate` — **fails on purpose.** That is the push item at the top.

> **Worth knowing for the next run:** the full suite cannot run in one call — it
> exceeds the per-call cap. It was run here in four explicit stage batches. A run that
> invokes `run_quality_improvements.py` bare will time out and may report partial
> success as success.

---

## Top of the queue for next run

1. **Two evidence stores disagree about Gap #15.** `agent_state.json` says
   `corpus_evidence_points = 1`; `gap_evidence.json` — which is what the gate reads —
   says 0 papers. Decide which is canonical before any tier decision rests on it.
2. **Gap #14 and #15 tiers are overdue, not unknown.** Both BRONZE with zero stored
   evidence. Doctrine defines BRONZE as *single source*. Gap #14 has **five
   consecutive documented nulls**; its one PubMed record (PMID 35784546) is a
   *protocol*, which reports no results. Not decided today because demoting a
   published tier changes what the site asserts and Gap #15's count is disputed by (1).
3. **Two `POINTS_ELSEWHERE` remain** in `_run_2026_08_27.py` (audit-trail, non-failing)
   that the 800-char ownership scan did *not* excuse. Read them before widening the
   radius — widening a radius to empty a bucket is how a gate gets quietly disabled.
4. **Promote `surnames` and `computedcite` to `--gate`** — but only after one run
   where they stay green on work they did not themselves perform. Today's zero on
   `surnames` was produced by today's own repairs.

---

*Research synthesis. Not medical advice. Every claim above traces to a cited source;
where a source was not found, the claim was withdrawn or marked, not replaced.*
