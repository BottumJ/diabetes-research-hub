# Diabetes Research Hub — Daily Iteration, 2026-09-01 (Tuesday)

**Scope:** agent-state work queue · live PubMed E-utilities · live ClinicalTrials.gov v2 · full pipeline rebuild
**Papers vetted:** 6 (the last 6 — the corpus is now 331 VETTED / 19 FLAGGED / **0 UNVETTED**)
**New gate:** `audit_nct_identifiers.py`
**Pipeline:** 57 of 58 `[OK]`; the one failure is the new gate reporting a real backlog

---

## Headline: nine gates guard PMIDs. Nothing guarded the trial numbers, and a third of them point at the wrong study.

`Research_Findings_Summary.md`, the public-facing summary, said this until today:

> **Baricitinib (BARICADE):** JAK inhibitor entering Phase 3 trials for T1D beta cell
> preservation. Enrollment anticipated 2026. **[NCT:NCT06640413]**
> **Validation: BRONZE** (Phase 2 data promising; Phase 3 not yet enrolled)

NCT06640413 is **TheraTri** — a Phase 1 study of `[177Lu]Lu-OncoFAP-23`, a radioligand
oncology agent, in FAP-expressing tumours. Not baricitinib. Not diabetes. Not Phase 3.

The identifier resolves. A reader clicks through, lands on a genuine ClinicalTrials.gov
record, and has no reason to doubt it unless they read the title. This is the same failure
mode the runs of 2026-08-27 through 08-31 found eight times over with PMIDs — and the repo
had **already found it once in an NCT and never generalised it.**
`build_trial_equity_mapper.py` still carries the comment:

```
# Trials removed in 2026-03-17 audit: NCT03812588 (wrong study), ...
```

One wrong trial number, found by hand in March, removed, no gate built. Five months later
the first systematic pass finds this:

```
HAND-AUTHORED TRIAL CITATIONS vs ClinicalTrials.gov   ·   32 distinct ids, 64 sites

  agrees with registry      ███████████                    11
  attribute disagreement    ████                            4
  weak topic overlap        ███████                         7
  TOPIC MISMATCH            █████████                       9
  NOT FOUND IN REGISTRY     █                               1
                            └────┴────┴────┴────┴────┴────┘
                            0    2    4    6    8   10   12

  hard failures (wrong study or no such study):  10 of 32  =  31%
```

**[Certain]** — 32 identifiers, each fetched live from ClinicalTrials.gov v2 today, compared
against the text asserting them. Report: `Analysis/Results/nct_identifier_audit.json`.

### The ten hard failures

| cited as | NCT | what the registry actually says |
|---|---|---|
| Baricitinib BARICADE Phase 3 | NCT06640413 | `[177Lu]Lu-OncoFAP-23` radioligand, oncology, Ph1 |
| Teplizumab PETITE (children <8) | NCT06176573 | chlorhexidine vaginal cleansing, post-cesarean infection |
| Tirzepatide SURPASS-T1D | NCT06316895 | thermal ablation for papillary thyroid carcinoma |
| VX-880 Phase 3 programme | NCT05794503 | postoperative urinary retention, neostigmine vs sugammadex |
| LANTIDRA Phase 3 | NCT04582669 | intralesional triamcinolone for hidradenitis suppurativa |
| Edmonton Protocol islet transplant | NCT01508429 | misoprostol for postpartum haemorrhage in home births |
| CIT-07 islet transplantation | NCT02974660 | protamine sulfate during TAVI |
| Etanercept, islet transplant | NCT02232165 | mean arterial pressure in acute spinal cord injury |
| GLP-1 RA adjunct, islet transplant | NCT00750178 | vorinostat (MK0683) in advanced cancer, Ph1 |
| LADA natural history, 300 pts, 5 yr | NCT06098729 | digital exercise intervention, n=24 |
| Abata ABA-201 TCR-Treg Ph1 | NCT06234898 | **no such study exists** |

Two of these sit on the published summary under ratings: the teplizumab entry is rated
**GOLD** and was carrying an obstetrics trial as one of its two identifiers. (The GOLD
rating itself survives — it rests on the Phase 3 teplizumab evidence and the FDA approval,
not on PETITE — but a GOLD entry should not be able to hold a wrong identifier for months.)

### Repaired today (4), verified against the registry before writing

- **Baricitinib** → NCT07222137 (BARICADE-DELAY, n=150, recruiting since 2026-01-12) and
  NCT07222332 (n=300, recruiting since 2026-02-05).
- **PETITE** → NCT05757713 (PETITE-T1D, Sanofi, single-arm open-label, n=20).
- **SURPASS-T1D** → NCT06914895 (SURPASS-T1D-1) and NCT06962280 (SURPASS-T1D-2), both
  Phase 3, both active/not-recruiting.
- **ABA-201** → marked `[NCT: UNSOURCED]`. No substitute found, none invented — the
  2026-08-29 house rule.

The remaining six topic mismatches live in builder scripts and are queued, not silently
rewritten: choosing the right islet-transplant trial is research, not repair.

---

## The baricitinib sentence was wrong three ways, and only one of them was the identifier

Queue item of 2026-08-31 asked for the BANDIT follow-up to be reflected. Doing so exposed
that the identifier and the status were stale too:

1. wrong NCT (above);
2. **"Enrollment anticipated 2026"** — both Phase 3 trials had been recruiting since
   January and February;
3. **"Phase 2 data promising"** — omitting that the effect does not survive stopping.

PMID 42627334 (So et al., *Diabetes Care* 2026, BANDIT post-treatment follow-up, 88 of 91
completed week 96): C-peptide significantly greater at week 72 (0.54 ± 0.05 vs
0.38 ± 0.06 pmol/mL, P=0.015) but **not at week 96 (P=0.336)**; no between-group difference
in insulin dose, HbA1c or CGM during follow-up; the week-48 effector-memory CD8+ changes had
resolved by week 96. Authors' conclusion: durable benefit likely requires continuous
treatment. The entry now says so.

**A source-side defect worth recording:** that abstract reports week-72 C-peptide in
`pmol/mL` and week-96 C-peptide in `nmol/L` **in the same sentence** — values 100× apart if
read literally. The week-96 figures are almost certainly pmol/mL. Flagged on the paper
record so nobody quotes the printed unit. This is the journal's error, not the repo's, but
it is exactly the kind of thing that becomes the repo's error on the next copy-paste.

---

## Vetting is complete for the first time

The last 6 UNVETTED papers were claim-checked against freshly fetched abstracts. All 6 pass
on existence and numbers; three carry caveats that must travel with any future use:

- **42283716** (TrialNet extended follow-up) — the title says "benign side effect profile";
  the paper reports **no detected difference** at 47% participation, 209–473 responses per
  question, self-reported, median 1.78 years. Absence of a detected difference is not
  evidence of safety, and the two must not be interchanged.
- **42642774** (CoQ10 meta-analysis, 20 RCTs) — CRP down (P<0.001), **malondialdehyde
  unchanged**. MDA is the oxidative-stress marker here. This is an inflammation result and a
  **null** oxidative-stress result; also null on total cholesterol, LDL and blood pressure.
- **42196240** (NLRP3/ferroptosis) — STZ mice and HK-2 cells only. Opens PRECLINICAL.

Corpus status: **331 VETTED / 19 FLAGGED / 0 UNVETTED**, out of 350.

---

## The largest risk in this project is not a research risk

```
git rev-list --count origin/main..main   ->   96
```

**Ninety-six commits have never been pushed.** The oldest is dated 2026-04-21.
`.git/FETCH_HEAD` does not exist, so the remote has never been contacted since clone. Four
and a half months of vetting, gate construction and citation repair exists in exactly one
place: this disk. The 2026-08-17 run diagnosed it correctly ("push blocked by credentials
only") and eleven runs since then have logged `changes_pushed: false` without the count ever
going down.

Two more findings in the same area, both measured today:

- **60 files are staged for deletion while present on disk.** They are the outputs of the
  last four runs, including all four monitor reports and the paper-library abstracts written
  by the 2026-08-28 miscitation repair. Cause: `git add -A` ran while OneDrive had them
  dehydrated to cloud-only placeholders, so git staged deletions for files it could not see.
  **The next `git commit` would delete all 60.**
- **176 junk lock files (141 MB `.git`) and two phantom branches.** Because the mount denies
  `unlink` inside `.git`, five months of runs each *renamed* the lock they could not delete.
  Two of those renames landed in `.git/refs/heads/`, so git now reports
  `main.lock.old_1786608612` and `main.lock.z_1786954612656090835` as branches.

None of this is fixable from the agent sandbox — the unlink denial is the whole problem, and
the push needs credentials that an unattended run should not have. So it is written as a
script for you to run:

**`Analysis/Scripts/repair_git_state.py`** — report-only by default, `--apply` to act. It
clears the locks, retires the phantom refs, unstages the 60 phantom deletions (backing up
`.git/index` first), and then **stops** and prints the push commands rather than running
them. It also explains the OneDrive setting that caused problem 2, so it does not recur.

---

## Self-audit: the new gate was wrong twice before it was right

Recording this because the 2026-08-30 run established that an audit which is not itself
audited just reproduces the defect it was built to catch. First draft flagged 14; two of
those were artefacts of the gate, not the repo.

1. **The context window bled across records.** Attributes were read from a flat ±320-char
   window. In `build_trial_equity_mapper.py` the trials are dict literals of roughly that
   size, so the window reached into the *neighbouring* trial. NCT05210530 was flagged "text
   says Phase 3, registry says PHASE1" — the text says Phase 1, correctly; the "Phase 3"
   belonged to the record above. Attributes now read the enclosing record only, and any
   asserted phase or enrollment must sit within 100 characters of the identifier.
2. **One shared word counted as topical agreement.** The chlorhexidine trial *passed* the
   topic check as PETITE on the single shared word "prevention"; VCTX210A passed as Sana
   SC451 on "type". A threshold of one is not a threshold. Raised to two, with the one-token
   case surfaced as `WEAK_TOPIC_OVERLAP` rather than dropped into OK — that bucket is where
   the AZD1656-vs-AK119 and PolTREG-vs-CLBS03 mismatches now sit.

The acronym check also offered `CD20`, `CTLA-4`, `VERIFIED` and `PRED-2026-002` as "trial
acronyms the text asserts". It now fires only on a parenthesised name in an explicit `name`
field — which is what catches the one that matters, below.

---

## A finding that lands directly on a standing HUMAN CALL

The acronym check flagged **NCT04233034**, labelled in `build_trial_equity_mapper.py` as
*"Verapamil for beta cell preservation in T1D (Ver-A-T1D)"*. The registry says it is
**CLVer** — *Hybrid Closed Loop Therapy and Verapamil for Beta Cell Preservation in New
Onset Type 1 Diabetes*, n=113.

CLVer is PMID 36826844 — the JAMA RCT that the 2026-08-29 queue item flagged as sitting in
the paper library, supplying **zero** extractions, while the two top-ranked verapamil paths
rest entirely on a protocol that reports no outcomes.

So the repo has held CLVer's trial registration all along, filed under the name of the
protocol trial it has been complaining about. That does not answer the human call, but it
removes the last excuse that answering it needs new evidence: **the trial, its publication
and its registration are all already in the repo.**

---

## Pipeline

57 of 58 `[OK]`. The failure is `nctgate` — the new audit, reporting the 17 unrepaired trial
citations honestly. It was left failing rather than allowlisted: a gate that goes green over
a known backlog is how the March 2026 NCT finding got lost in the first place.

## What was NOT done, and why

- **The seven standing P1 HUMAN CALLs were again not touched.** Twelve days now. Every one
  restates a published number, re-tiers a rated claim, or delists ranked content. Today
  added evidence to one of them (verapamil, above) rather than an eighth item to the pile.
- **BRONZE gap audits (#14, #15) deferred.** The NCT finding was larger and live.
- The `Analysis/Results/*.md` markdown-gate extension was deferred for the same reason.
