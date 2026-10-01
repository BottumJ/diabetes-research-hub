# Run Report — 2026-10-01 (overnight, owner asleep; committed locally, NOT pushed)

Five workstreams, chosen because each either closes a loop the hub opened or
removes a way it keeps being wrong.

## 1. First scored prediction

PRED-2026-004 (CagriSema non-inferior to tirzepatide on HbA1c, p=0.65, locked
2026-06-23) resolved **TRUE** from Novo Nordisk's topline release of 2026-09-23:
REIMAGINE 5, HbA1c 1.71% vs 1.67% at week 60. Brier 0.1225. The ledger has its
first real score. Caveats recorded with the resolution: sponsor-reported, not
peer-reviewed, no registry results yet, and the comparator was the lowest
tirzepatide dose. The June report that already showed this as "RESOLVED TRUE"
had been written before any readout existed.

## 2. CagriSema in the verified substrate

Five records from REIMAGINE 1-3 (PMIDs 42251860, 42251856, 42251859), each
span-verified against the live abstract and agreed by an independent second
extraction. The pooling page gains CagriSema 2.4/2.4 mg and 1.0/1.0 mg vs placebo
(two trials each). REIMAGINE 2 has a PubMed-listed erratum not yet read; noted
on its record.

## 3. New literature in the findings summary

- Retatrutide TRIUMPH-2 (PMID 42810372), first phase 3 in type 2 diabetes.
  HbA1c is not in the abstract and is not stated.
- CagriSema REIMAGINE 1-3 results; REIMAGINE 5 as sponsor topline. Now GOLD for
  HbA1c vs placebo. An unsourced "FDA review anticipated 2026" removed.
- Petrelintide ZUPREME 1 (PMID 42810355, obesity without diabetes) and the new
  Roche phase 3 in type 2 diabetes (NCT07843485). BRONZE.

## 4. Gap #2: errors fixed, ruling prepared

`DECISION_BRIEF_2026-10-01_Gap2.md`. Gap #2 is two questions under one number
("Health Equity in Diabetes" in the evidence store; "...in Beta Cell Therapies"
on the page). Neither supports GOLD under Lesson 9. Tier NOT changed.

Fixed regardless, because they were false:
- **Zimislecel was published as "FDA approved"** in three places. It is in phase 3.
- An HLA-matched iPSC mechanism with potency figures, unsourced and inconsistent
  with an allogeneic product.
- A trial-site country list that named four countries with no site. Replaced by
  ClinicalTrials.gov counts: 36 listings, 10 high-income countries.
- Total diabetes counts labelled as type 1 / LADA burden.

## 5. One tier store

`Analysis/Results/gap_tiers.json` is now THE tier. `gap_tier_copies.py` finds
typed copies in seven forms (106 found); `audit_gap_numbering.py` fails if any
disagrees with the store; `set_gap_tier.py GAP TIER --reason ...` applies a
ruling to the store, agent state, every builder copy and the README in one
command. On its first scan it found three wrong copies the old audit could not
see, including a published header calling Gap #13 "SILVER-Validated". A trial
ruling (Gap #15 to BRONZE) rewrote 9 files and `--sync` restored all of them.

## Not done

- No push (owner asleep).
- Gap #2 tier awaits the ruling in the brief.
