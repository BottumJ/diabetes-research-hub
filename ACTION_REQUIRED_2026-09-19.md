# Action Required — 2026-09-19

**Run:** automated (sandbox). Python healthy, git writable, 4 pipeline chunks run.
**Previous:** `ACTION_REQUIRED_2026-09-18.md`

---

## Headline

**Correcting a paper is what deletes it from the corpus.** The 2026-09-18 run corrected
PREDIMED (PMID 25940230) and DIAGNODE-2 (34021020) and flagged them both. Today both were
evicted from the paper index as "adjudicated not a corpus paper," and nothing reported it —
`metadata.total_indexed` kept saying 347 against a papers dict of 345.

It surfaced only because a gate written this morning for an unrelated bug happens to check
arithmetic. Two other papers are already out on the same basis, one of which
`agent_state.json` itself calls **load-bearing for the Gap #11 hypothesis**.

Separately: **the FDA approved finerenone (Kerendia) for CKD in type 1 diabetes on
2026-09-16** — first new agent for that population in 30+ years. This hub tracked no
finerenone at all, while simultaneously citing a finerenone trial as its *spironolactone*
evidence.

---

## 1. Your call, in priority order

### 1a. Should "FLAGGED" mean "not a corpus paper"? — BLOCKING the corpus count

`corpus_membership.excluded_pmids()` codes any paper FLAGGED in `agent_state` with no
`membership_class` as `FLAGGED_UNCLASSIFIED` and treats it as adjudicated non-corpus.
`reconcile_paper_index.py` then deletes it from `index.json`.

"Flag for review" and "adjudicate as off-topic" are opposite judgements and this pipeline
performs them with the same act.

| PMID | Paper | Evicted | Why it matters |
|---|---|---|---|
| 25940230 | PREDIMED (Mediterranean diet) | **today** | Flagged by yesterday's correction run |
| 34021020 | DIAGNODE-2 (intralymphatic GAD) | **today** | Same — yesterday corrected it, today it vanished |
| 37026004 | HLA-DR matching / islet | before today, date unrecorded | State calls it **load-bearing for Gap #11**; its full text is on disk as PMC10070978 |
| 42674789 | Retrospective cohort performance | before today, date unrecorded | FLAGGED PROTOCOL, relevant to Gap #10 |

19 more papers are FLAGGED without a membership class. Each is one reconcile run from
leaving the corpus.

Three options: **(a)** flagged papers stay indexed and carry a flag field, exclusion
reserved for explicit off-topic adjudication; **(b)** classify the 4 individually now;
**(c)** keep the behaviour and say so on the methodology page, since the headline corpus
count depends on it.

Applied today without touching the semantics: eviction now writes a **ledger** (pmid, date,
adjudication code, reason, title) into index metadata, `total_indexed` is repaired to 345,
and the invariant gate passes. The eviction is no longer silent. It is still happening.

### 1b. Re-grade or re-evidence Spironolactone

Its only citation was **PMID 33264825 = FIDELIO-DKD**, a *finerenone* trial — different
molecule, branded, on-patent, and so ineligible for a catalog of off-patent generics.
Withdrawn today; the row now publishes MODERATE with a visible `[NO CITED EVIDENCE]`
marker. Grading is your call (2026-08-20 precedent).

Real evidence exists and was **not** inserted because neither PMID was verified: a low-dose
12.5 mg/day open-label multicentre RCT in T2D with albuminuria (*J Clin Endocrinol Metab*
2023;108(9):2203, positive on UACR) and **PRIORITY** (*Lancet Diabetes Endocrinol* 2020,
**null** for preventing microalbuminuria). A positive surrogate trial plus a null prevention
trial is a grading judgement, not a lookup.

### 1c. Where does finerenone belong?

PMID **41780000** (FINE-ONE, *NEJM* 2026, DOI 10.1056/NEJMoa2512854) ingested UNVETTED,
identity verified against the live PubMed record. Three constraints that must hold:

- The primary endpoint is **relative change in UACR at 6 months** — a surrogate. No
  hard-outcome endpoint was met because none was powered. Hyperkalaemia was more frequent.
  Hub text may say "reduced albuminuria over 6 months"; never "protects kidneys."
- Finerenone is **branded and on-patent**. It must not enter the generic catalog. The row it
  was wrongly propping up (spironolactone) is the steroidal MRA that *is* generic, and that
  distinction is now load-bearing.
- A newly approved comparator changes what counts as an unmet need for the NLRP3 /
  diabetic-kidney paths.

### 1d. Push — and it is now the *only* thing that needs you for git

114 commits unpushed; `origin/main` still at 2026-04-20 (152 days). `publishgate` fails on
purpose until this is done.

**The commit half is solved, and it was never a write limitation.** Today's commit (`9b6b6a3`,
127 files, porcelain 0) went through with a plain `git add -A && git commit` using the
*default* index. What had been blocking was two **stale lock files** — `.git/HEAD.lock` (left
2026-09-18) and `.git/index.lock` (left 2026-09-17). `unlink` is forbidden on this OneDrive
mount but **rename is not**, so `mv .git/HEAD.lock .git/HEAD.lock.stale` clears it.

The 2026-09-16 `GIT_INDEX_FILE` workaround was treating the wrong lock, and actively hid the
real one: with it set, `git add` succeeded and `git commit` still failed, because the lock git
could not take was `HEAD.lock`. Three runs diagnosed this as an index problem for that reason.

`.git` now holds **203 renamed lock files** going back to 2026-04-10 (`HEAD.lock.gone2`,
`index.lock.delete-me`, `index.lock.evicted4`…). Every run since April has fought this and
left debris. Queued: fold the two `mv` lines into the run preamble, drop `GIT_INDEX_FILE`,
sweep the debris, and retire the priority-0 "SANDBOX FAILURE" queue items — all but this one.

**What still needs you:** `git push` fails with *"could not read Username for
https://github.com: No such device or address"*. No credential helper in the sandbox. That is
credentials, not locks, and no amount of agent work reaches it.

---

## 2. Found and fixed today

### 2a. The repository held 150 full texts and its index recorded none of them — 33+ days

| | Before | After |
|---|---|---|
| `metadata.pmc_available` | 174 | 174 |
| `metadata.fulltext_fetched` | 150 | 150 |
| records with a `pmcid` | **1** of 347 | **133** |
| records with `has_fulltext` | **0** of 347 | **132** |
| Paper Library rows reading "Full Text" | **0** | **133** |

**Root cause, proven not inferred:** `ingest_papers.convert_pmids_to_pmcids()` returns a map
keyed by **int** (the NCBI ID converter sends `pmid` as a JSON number); `build_index()` looks
it up with a **str**. Every per-paper lookup missed. Confirmed by calling the function
directly: `{37026004: 'PMC10070978', ...}`. The download loop iterates the map directly,
which is why 150 full texts were fetched and saved while the index recorded none.

Three consequences, all live until today:

1. The published Paper Library showed "PMC Available: 174" above 347 rows of which not one
   said "Full Text"; its Full Text filter matched nothing.
2. The scheduled task's own vetting step — *"if the paper has full text, scan for red
   flags"* — evaluated False for all 347 papers. Full-text red-flag scanning has never run.
3. The 2026-09-07 queue item on PMCID→PMID normalisation is the same bug. PMC12211534 was
   carried four days as a novel find while already in corpus as PMID 40598585 — whose full
   text was on disk as `PMC12211534.json` the entire time.

Fixed at source, plus `repair_index_pmcid_map.py` (rebuilds the fields from
`fulltext/*.json`, authoritative and local) and `pmcid_to_pmid.json` (150 entries) for
intake normalisation. `PMC12211534 → 40598585` verified.

### 2b. Two catalog rows graded on papers about something else

- **Spironolactone** ← FIDELIO-DKD, a finerenone trial (§1b).
- **Minocycline** ← PMID 25714673 = *"Loss of survival factors and activation of inflammatory
  cascades in brain sympathetic centers in type 1 diabetic mice."* A mouse study. No
  minocycline. Described in the catalog as "Hu et al. 2015 diabetic neuropathy," carrying the
  claim "MIND trial showed neuropathy improvement." Claim now suspended; the real MIND study
  appears to be Syngle et al., *Neurol Sci* 2014, and whether the retained PMID 24497205 is
  that paper is **not** established.

**Why every citation gate here was correctly green on both:** they all score a PMID against
the prose beside it, and the prose was written *from* the wrong paper — so it matches it
perfectly. For Spironolactone the reference text read "FIDELIO-DKD (Bakris et al. 2020)",
which is exactly what 33264825 is. Title, author, journal and year gates were all right to
pass. What disagreed was the **subject of the record**.

---

## 3. Gates added (both proven in both directions on live data, not fixtures)

| Gate | Asks | Proof |
|---|---|---|
| `audit_catalog_entity_agreement.py` | Does the cited paper mention the drug this row is *about*? | Fired on 2 live defects, green after repair (ABSENT 2 → 0) |
| `audit_index_field_invariants.py` | Does a summary count agree with the records it summarises? | Fires on the pre-repair index (exit 1), clean on the repaired one; **then caught the eviction in §1a** |

A render guard was also added: an emptied `key_pmids` used to publish
`https://pubmed.ncbi.nlm.nih.gov//` labelled "PMID:", so withdrawing a citation would have
shipped a dead link that still looked like one. Withdrawal now reads as withdrawal.

---

## 4. Pipeline state

**Chunks run: 4 (80 stages split to fit the sandbox call limit). Two stages not green, both known:**

- `gapsubject` — fails, **as it has since 2026-09-07**. 7 findings, down from 9.
- `publishgate` — fails on purpose. That is §1d.

Credibility sweep clean: 0 impossible PMIDs (highest in repo 42,698,953; flag line
42,994,765), 0 unhedged preclinical overclaims. All builders parse.

`ingest` was **not** run this session — it is the slowest stage and the sandbox caps a call at
~10 minutes. The index repair was applied locally instead, which does not need the network.
Running `ingest` is queued: it should now index the 18 papers whose full text is already on
disk, which will close the `I3` note.

---

## 5. Next run picks up

1. Classify or protect the 19 remaining FLAGGED papers (§1a) — highest, because it is
   actively removing evidence.
2. Ingest the 11 catalog PMIDs no gate has ever been able to check; start with 24497205,
   now the Minocycline row's only citation.
3. Run `ingest` and confirm `I3` closes.
4. Widen the entity gate: it found parseable records in exactly **one** builder.
   `build_drug_repurposing_screen.py` (34 drugs), `build_drug_repurposing_islet.py` and
   `build_gka_landscape.py` hold the same kind of record in a shape the AST walk misses, so
   its green line covers less than it appears to. A gate with unstated reach was the
   2026-09-08 finding, restated.
5. Vet PMID 41780000 and decide the finerenone placement (§1c).

---

*Research synthesis, not medical advice. Every claim above traces to a source in the
repository or to a record fetched and named on 2026-09-19.*
