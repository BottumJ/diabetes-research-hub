# Diabetes Hub Monitor Report — 2026-09-06

**Run type:** Scheduled automated review
**Data acquired this run:** `clinical_trials_snapshot_2026-09-06.json` (new file; no existing file modified)
**Evidence levels per Research Doctrine:** file-derived facts [Certain]; web-derived [Likely] pending primary-source confirmation.

---

## 0. Lead finding — the drought broke, and it immediately produced a real signal

**Acquisition restarted. Five consecutive reports said "nothing changed"; this one has actual
changes to report.** [Certain]

```
Acquisition cadence, trials vs PubMed/gap
              trials   pubmed   gap
2026-07-17      ██       ██      ██
   ·········· 41-day outage ··········
2026-08-27      ██       ██       ─
2026-08-28      ██       ██       ─
2026-09-01      ██       ██       ─
2026-09-02      ─        ─        ─
2026-09-03      ─        ─        ─
2026-09-04      ─        ─        ─
2026-09-05      ─        ██      ██   ← you ran the PubMed + gap scripts
2026-09-06      ██*      ─        ─   ← this run acquired trials
                 * acquired by this monitor, not by your local script
```

Two things happened since the 09-05 report was written (02:39):

1. **At 03:24–03:32 on 09-05 you ran `baseline_pubmed_alerts.py` and
   `project1_literature_gap_analysis.py`.** The gap corpus is now dated
   `2020/01/01 → 2026/09/05` instead of `→ 2026/07/17`, and `pubmed_recent_latest.json`
   is fresh for the first time since July. Two of the five open recommendations from
   yesterday are closed. [Certain]
2. **This run acquired a fresh trial snapshot** (ClinicalTrials.gov reachable from the
   sandbox; 894 trials). That gave a real 09-01 → 09-06 diff instead of another null.

**What the real diff found immediately: orforglipron Phase 3 T2D results posted 09-04.**
See §2. This is the first substantive registry event the monitor has caught in-window
rather than in hindsight.

**Still broken:** `clinical_trials_latest.json` remains the July 17 copy, and
`hub_monitor.py` has not run since July 17. See §1.

---

## 1. File System Status

| File | Last modified | Age (d) | Status |
|---|---|---|---|
| `clinical_trials_snapshot_2026-09-06.json` | 09-06 02:38 | 0 | **New — acquired this run** |
| `pubmed_recent_snapshot_2026-09-05.json` | 09-05 03:32 | 1 | Fresh |
| `pubmed_recent_latest.json` | 09-05 03:32 | 1 | **Fixed — now current** |
| `literature_gap_data.json` | 09-05 03:24 | 1 | **Fixed — corpus through 09-05** |
| `literature_gap_report.md` | 09-05 03:24 | 1 | Fresh render, fresh input |
| `clinical_trials_latest.json` | 07-17 02:05 | **51** | **STALE pointer — still July copy** |
| `hub_monitor_report.md` | 07-17 02:16 | **51** | **STALE — `hub_monitor.py` not run** |
| `Diabetes_Research_Tracker.xlsx` | 07-17 10:07 | **51** | **STALE** |
| `RESEARCH_DOCTRINE.md` | 08-31 03:12 | 6 | Current |
| `CONTRIBUTION_STRATEGY.md` | 03-15 00:06 | 175 | 6 months old |

**Progress since 09-05:** the PubMed and gap pointers were repaired by your 09-05 run.
`pubmed_recent_latest.json` and `pubmed_recent_snapshot_2026-09-05.json` are now identical
in size (113,661 B) *and* both current — the pointer is doing its job again. [Certain]

**Remaining divergence — trials only.** `clinical_trials_latest.json` is still
593,584 B, byte-size identical to `clinical_trials_snapshot_2026-07-17.json`. Anything
downstream reading the trial pointer (dashboards, tracker refresh) is consuming **July 17
data — now 51 days old**, while the newest snapshot has 894 trials vs the pointer's 858.
This report reads the dated 09-06 file. [Certain]

**Stale lock file** `.~lock.Diabetes_Research_Tracker.xlsx#` (2026-03-14) still present —
176 days old, will block lock-aware writers. [Certain]

---

## 2. Clinical Trial Changes — 09-01 → 09-06

Corpus: 887 (09-01) → **894 (09-06)**.

| Metric | Count |
|---|---|
| New trials | **8** |
| Removed trials | 1 (`NCT06717451`) |
| Status changes | **3** |
| New results posted | **2** |

Compare to the last four reports, which showed 0/0/0. The nulls were an acquisition
artifact, not a quiet registry. [Certain]

### ★ Results posted — the headline

**`NCT05872620` — Orforglipron in adults with obesity/overweight **and Type 2 Diabetes**
(ATTAIN-2 design), Eli Lilly, Phase 3, n=1,613, completed 2025-08-08. Results posted
2026-09-04 — two days ago.** [Certain — from corpus]

Why this matters more than the raw entry suggests:

- Orforglipron is the hub's most-tracked oral incretin (12 PubMed hits at 09-01, 10 at
  09-05) and the only tracked therapy with an oral route. Registry results for the
  **T2D** population — as opposed to the obesity-only ATTAIN-1 readout published in
  *NEJM* — are the ones relevant to this hub's scope.
- It is the **first Phase 3 results posting the monitor has caught inside the reporting
  window** rather than discovering after the fact. §5 of the 09-05 report documented the
  opposite failure mode (SURPASS-CVOT results sat unsurfaced for 51 days until the FDA
  approval made it news). The difference is entirely that acquisition ran.
- `has_results: false` in the record while `results_posted: 2026-09-04` is populated.
  That field pair is inconsistent; the API's `resultsSection` had not yet propagated at
  fetch time. **Do not filter on `has_results` when scanning for new postings** — use
  `results_posted`. [Certain — observed in this snapshot]

`NCT04828785` — Food As MedicinE for Diabetes (UNC, n=215) results posted 2026-09-02.
Food-as-medicine RCT, relevant to Tier 1 §6 (Epidemiological / health equity). [Certain]

### ★ New Phase 3 registrations

| NCT | First posted | Sponsor | Agent | Note |
|---|---|---|---|---|
| **NCT07797335** | 2026-09-01 | Novo Nordisk | **Zenagamtide** vs insulin glargine | **AMBITION 7**, n=1,778, T2D + CV risk, completes 2028-09 |
| **NCT07804849** | 2026-09-04 | Ain Shams University | **Oral verapamil** vs placebo | Ph2/3, n=70, *newly diagnosed children/adolescents T1D* |
| NCT07801820 | 2026-09-03 | Shanghai Minwei | MWN109 tablets | Ph2, T2D |
| NCT07796477 | 2026-09-01 | CSPC Ouyi | SYH2069 injection | Ph2, T2D, not yet recruiting |

**Zenagamtide is a new tracked-therapy candidate the hub does not currently follow.**
It is Novo's GLP-1/amylin unimolecular co-agonist; Phase 2 at ADA 2026 reported HbA1c
−1.71 pp at 36 weeks with up to 14.6% weight loss, and AMBITION is the Phase 3 program.
[Likely — Phase 2 figures from Novo press release via secondary coverage; trial record
itself is Certain.] **Recommend adding `zenagamtide` to the eight tracked therapies in
`baseline_pubmed_alerts.py`** — it is now a registered Phase 3 program with a head-to-head
insulin comparator, which is exactly the profile of the agents already tracked.

**NCT07804849 (verapamil in pediatric new-onset T1D)** is the more interesting scientific
entry. Verapamil for beta-cell preservation is a repurposing story (TXNIP inhibition) and
lands on **two** Tier 1 areas at once: §4 Drug Repurposing (18/20) and §3 Clinical Trial
Intelligence. A 70-patient academic trial in Egypt is also a population the pediatric
verapamil literature does not cover. [Certain on the record; interpretation is mine]

### Status changes

| NCT | Change | Sponsor | Note |
|---|---|---|---|
| NCT07076199 | RECRUITING → ACTIVE_NOT_RECRUITING | Novo Nordisk | Insulin icodec Ph3 in **T1D**, n=877 — **fully enrolled**, completes 2027-03 |
| NCT07228117 | RECRUITING → ACTIVE_NOT_RECRUITING | Medtronic | GATEWAY, MiniMed NMX8-AID, n=389 — enrollment closed |
| NCT07282639 | NOT_YET_RECRUITING → RECRUITING | OHSU | App-based diabetes education |

The icodec T1D transition is the notable one: the 09-05 report listed NCT07076199 as
recruiting. It closed enrollment within the last five days. `icodec` PubMed volume also
moved 8 → 10 over the same window. [Certain]

### Phase 3 RECRUITING: 58 (was 57)

Key-organization status (09-06 corpus):

- **Vertex — 3 trials**, unchanged. NCT04786262 and NCT06832410 (VX-880/zimislecel, Ph3,
  RECRUITING), NCT05791201 (VX-264, Ph1/2). No results posted on any.
- **Eli Lilly — 34** (was 33). The +1 is NCT05872620 entering via the results-posted query.
- **Novo Nordisk — 29** (was 28). The +1 is AMBITION 7.
- **Sana Biotechnology — 0.** Unchanged blind spot; sponsor-string matching misses the
  investigator-initiated UP421 work. [Likely]

### Persistent seen-set — the fix recommended yesterday, run manually here

Yesterday's §5 argued the results-diff should run against a persistent set of already-seen
`results_posted` NCT IDs rather than the prior snapshot. I computed that set across **all**
historical snapshots: **36 trials have results postings dated on or after 2026-07-01.**
Of those, only 2 would have been caught by consecutive-snapshot diffing. The ones the
snapshot-to-snapshot method lost include:

| NCT | Posted | Sponsor | Trial |
|---|---|---|---|
| NCT04596631 | 2026-08-21 | Novo Nordisk | Oral semaglutide vs placebo, Ph3 |
| NCT04255433 | 2026-07-08 | Eli Lilly | **SURPASS-CVOT** — preceded the 08-28 FDA approval |
| NCT06340854 | 2026-07-02 | Novo Nordisk | Switching daily basal → weekly, Ph3 |
| NCT03263494 | 2026-07-09 | Jaeb Center | CGM in teens/young adults T1D, Ph3 |
| NCT05254002 | 2026-07-13 | Bayer | Finerenone combination, Ph2 |
| NCT03899883 | 2026-07-28 | U. Colorado | Uric acid lowering in youth-onset T2D, Ph2 |

**Confirms the diagnosis: 34 of 36 postings in the last ~10 weeks were invisible to the
current diff.** This is the highest-value code change in the hub and it is a ~10-line
change. [Certain — computed over all 125 dated snapshot files in Analysis/Results]

---

## 3. PubMed Highlights — 09-01 → 09-05 snapshot

Window: rolling 30 days · **141 unique papers** (was 160) · 16 domains · 8 tracked therapies.
Diff vs 09-01: **78 new, 97 dropped.** Net shrinkage of 19 papers on a rolling window is
worth a glance but not alarming — `domain_retmax` is 10 and `therapy_retmax` is 5, so the
corpus size is query-capped, not a measure of field activity. **Do not read the 160 → 141
drop as "the field slowed down."** [Certain]

### Cross-domain papers — 18 total, **13 new since 09-01**

**Four-domain — new and the top read this window:**

| PMID | Domains | Title |
|---|---|---|
| **42694848** | AI/ML · Biomarker · Complications · Multi-Omics | COL1A2 and APOLD1 Define a Dual-Axis Molecular Framework for Diabetic Nephropathy–Retinopathy Comorbidity |

**This is the highest-value paper the hub has surfaced in either of the last two windows.**
It is the only 4-domain hit on record, and it sits on **three** Tier 1 areas simultaneously:
§1 Multi-Omics Biomarker Integration (19/20), §5 AI/ML Prediction Models (18/20), and the
complications-prediction use case named explicitly in §5's "What We Do." A named two-gene
axis spanning nephropathy *and* retinopathy is directly testable against GEO / UK Biobank
proteomics, which the doctrine lists as available. **Read this first.** [Certain that it is
4-domain; the priority call is mine]

**Three-domain:**

| PMID | Domains | Title | Status |
|---|---|---|---|
| 42694300 | Biomarker · Microbiome · Multi-Omics | Integrated oral microbiome + metabolome multi-omics signatures | NEW |
| 42688815 | Biomarker · Microbiome · Multi-Omics | Multi-omics integration for precision risk stratification | NEW |
| 42626948 | Stem Cell Cure · Immunotherapy · teplizumab | Gene-edited hypoimmune islets — immunological challenges | carried |
| 42673585 | orforglipron · retatrutide · CagriSema | GLP-1 RA/co-agonists for weight loss (*Ann Intern Med*) | carried |

Two independent multi-omics-integration reviews appearing in the same 4-day window, both
crossing Biomarker × Microbiome, is a cluster rather than a coincidence — **Tier 1 §1 is
where the literature is currently moving.** [Likely — two papers is a thin basis; check
whether the pattern holds in the next window before acting on it.]

**Two-domain, new this window (selected):**

- **42688560** — T1D Immunotherapy × Biomarker — *Decoding Treg diversity and dysfunction
  to advance Treg-based therapies.* Pairs directly with gap-table rows Treg/CAR-T ×
  Neuropathy (rank 6) and Treg/CAR-T × Health Equity (rank 15). A review of Treg
  heterogeneity is exactly the input needed to judge whether those zeros are real gaps
  or terminology mismatch.
- 42695140 — T2D GLP-1 × dapagliflozin — adjunctive therapy in T1D on AID systems.
- 42688617 / 42683980 — retatrutide × CagriSema — two more head-to-head incretin syntheses,
  joining 42673585. Three comparator papers in one window.
- 42685619 — T2D Remission × Microbiome — periodontitis → insulin resistance via TLR4/NF-κB.
- 42695342 — Biomarker × dapagliflozin — SGLT2i and the CYP4A/20-HETE pathway.
- 42690471 — Microbiome × Multi-Omics — microbial signals across obesity/T2DM/MASLD.
- 42676327 — Stem Cell Cure × Immunotherapy — dupilumab case report (likely a keyword
  false-positive on the stem-cell domain; low priority).
- **42695488** — AI/ML × Multi-Omics — *ROS in Breast Cancer.* **False positive.** A breast
  cancer redox review has no diabetes content; it matched on method keywords. One
  off-topic hit in 18 cross-domain papers is a ~6% precision leak — tolerable, but the
  `adjudicated_offtopic_pmids.json` mechanism should absorb it. [Certain]

### Tracked-therapy volume (30-day window)

| Therapy | 09-01 | 09-05 | Δ |
|---|---|---|---|
| dapagliflozin | 32 | 41 | **+9** |
| retatrutide | 8 | 12 | **+4** |
| icodec | 8 | 10 | +2 |
| CagriSema | 3 | 5 | +2 |
| orforglipron | 12 | 10 | −2 |
| teplizumab | 4 | 4 | 0 |
| baricitinib | 2 | 2 | 0 |
| **zimislecel** | **0** | **0** | **0** |

`zimislecel` remains 0 on every snapshot ever taken — now confirmed across a *freshly
queried* corpus, not a stale copy, which removes the "stale file" explanation. Either the
INN genuinely has no PubMed presence or the query is malformed. **Hand-verify once.**
[Certain that the zero is real in the current query; Guessing on cause.]

`orforglipron` falling 12 → 10 in the same window its Phase 3 T2D results posted is the
kind of registry/literature lag the doctrine's §3 exists to exploit — the registry leads
the literature by weeks to months. [Certain on counts]

---

## 4. Gap Analysis Summary — **now on fresh data**

`literature_gap_data.json` regenerated 2026-09-05 03:24, `date_range: 2020/01/01 to
2026/09/05`. 30 domains, 435 pairs. **The 49-day staleness flagged in the last five
reports is resolved.** [Certain]

### Top 5 meaningful gaps (report's own classification, BRONZE)

| # | Intersection | d1 pubs | d2 pubs | Joint | Score | Doctrine tier |
|---|---|---|---|---|---|---|
| 1 | **Beta Cell Regen × Health Equity** | 1,497 | 2,061 | **0** | 100.0 | **Tier 1 §6** |
| 2 | **Insulin Resistance × Islet Transplant** | 20,604 | 253 | 1 | 100.0 | §3 / mechanistic |
| 3 | **Islet Transplant × Drug Repurposing** | 253 | 621 | **0** | 100.0 | **Tier 1 §4** |
| 4 | **Islet Transplant × Health Equity** | 253 | 2,061 | **0** | 100.0 | **Tier 1 §6** |
| 5 | **Gene Therapy × LADA** | 2,358 | 602 | **0** | 100.0 | **Tier 1 §2** |

### What changed vs the July corpus

The individual domain counts grew as expected over 49 days — Beta Cell Regen 1,463 → 1,497,
Health Equity 1,990 → 2,061, Treg/CAR-T 953 → 983 — **and every top-ranked joint count is
still 0.** Seven weeks of new diabetes literature added nothing to any of these
intersections. That is a meaningfully stronger result than the July run: the gaps are
persistent, not a sampling artifact of one query date. [Certain on counts]

**Ranking did shift.** Islet Transplant now occupies four of the top six rows, displacing
the GWAS/Polygenic and Drug Repurposing × CGM pairs the July report led with — and the
script's own classifier moved those two into "methodologically distinct," so they no longer
contaminate the meaningful list. The top of the table is cleaner than it was in July.
[Certain]

### Alignment with Tier 1 contribution areas

- **Tier 1 §6 Epidemiological Data Analysis (17/20)** — `X × Health Equity` with zero joint
  pubs now covers Beta Cell Regen, Islet Transplant, Glucokinase, Drug Repurposing, and
  LADA. Five zeros against a 2,061-paper domain. **Still the strongest doctrine-aligned
  cluster.** The new UNC food-as-medicine results posting (NCT04828785, §2) is a concrete
  data point on this axis.
- **Tier 1 §4 Drug Repurposing (18/20)** — Islet Transplant × Drug Repurposing (0 joint)
  is new to the top 5 and the report's own rationale — repurposing existing
  immunosuppressants for islet protection via computational screening — is a
  well-specified, tractable project. It also now has a live registry analogue: the
  verapamil pediatric T1D trial registered 09-04 (§2).
- **Tier 1 §2 Literature Synthesis (19/20)** — Gene Therapy × LADA (0 joint) holds from
  July, and LADA also appears in four other zero-joint pairs (Glucokinase, Personalized
  Nutr, Drug Repurposing, Health Equity). LADA is the most systematically isolated domain
  in the table.

**Caveat, unchanged and load-bearing:** every classification is **BRONZE** (single
analytical source). Zero joint publications is as consistent with terminology mismatch as
with a real gap — and Islet Transplant at 253 total papers is a small enough domain that
keyword recall is a live concern. Do not promote any of these to a claim without the
PubMed hand-verification the gap report's own "How to Use" section prescribes.

---

## 5. Breaking News (last 7 days)

**Nothing new clears the significance bar this week.** The 08-28 FDA approval of Mounjaro
(tirzepatide) for cardiovascular risk reduction in T2D — reported in full in the 09-05
report — remains the most recent major regulatory action. Searches for FDA diabetes
approvals and diabetes breakthroughs in the 09-01 → 09-06 window returned only that item
plus routine journal-issue coverage. [Likely — absence of news is weaker evidence than
presence; two searches is not exhaustive.]

**The one thing worth noting is a registry-vs-press asymmetry.** The orforglipron
Phase 3 **T2D** results (NCT05872620) posted to ClinicalTrials.gov on 09-04 and have no
corresponding press coverage in the search results — Lilly's public orforglipron
communications remain focused on the obesity indications (ATTAIN-1, ATTAIN-MAINTAIN). The
registry is ahead of the press release here by at least two days. **This is precisely the
edge Tier 1 §3 is supposed to generate, and it only exists because acquisition ran.**
[Certain that the registry posting exists and predates the searched coverage; Likely that
no press release has issued — absence of search hits is not proof.]

Carried forward, unchanged: insulin efsitora alfa FDA decision anticipated H2 2026;
retatrutide Phase 3 readouts expected before year-end. [Likely]

---

## 6. Recommended Actions

**Ranked. Items 1–2 are the ones with a deadline attached.**

1. **Pull the orforglipron ATTAIN-2 results.** NCT05872620 posted 09-04; registry is ahead
   of the press. Read the results section directly at
   `https://clinicaltrials.gov/study/NCT05872620?tab=results` and log it in the tracker.
   This is the first in-window Phase 3 catch the monitor has made — act on it while it is
   still an information edge.

2. **Fix the results-posted diff to use a persistent seen-set.** I computed the set
   manually this run: **36 results postings since 2026-07-01, of which the current
   consecutive-snapshot diff would have caught 2.** The fix is small and the loss is
   permanent for anything posted during an outage. Highest-value code change in the hub.

3. **Run `hub_monitor.py` and `baseline_clinical_trials.py` locally.** You restored the
   PubMed and gap scripts on 09-05 — finish the set. `hub_monitor.py` has not run since
   July 17, and `clinical_trials_latest.json` is still the July copy. On your machine:
   ```
   python Analysis/Scripts/baseline_clinical_trials.py
   python Analysis/Scripts/hub_monitor.py
   ```
   The snapshot this monitor wrote (`clinical_trials_snapshot_2026-09-06.json`) is a
   sandbox stopgap; it does not update the pointer or the summary.

4. **Read PMID 42694848** — COL1A2/APOLD1 dual-axis framework for diabetic
   nephropathy–retinopathy comorbidity. Only 4-domain paper on record; hits Tier 1 §1 and
   §5 together; directly testable against the public omics resources the doctrine names.

5. **Add `zenagamtide` to the tracked-therapy list** in `baseline_pubmed_alerts.py`.
   Novo's GLP-1/amylin co-agonist entered Phase 3 (AMBITION 7, NCT07797335, n=1,778) on
   09-01 with an insulin-glargine comparator. It now matches the profile of every other
   tracked agent and the hub has zero literature coverage of it.

6. **Repair or retire `clinical_trials_latest.json`.** Byte-identical to the July 17
   snapshot; 36 trials behind. Either have the baseline script rewrite it atomically or
   delete it and point consumers at the newest dated snapshot.

7. **Update the tracker** — 51 days stale. New entries warranted: NCT05872620 (results),
   NCT07797335 (zenagamtide Ph3), NCT07804849 (pediatric verapamil), plus the AstraZeneca
   elecoglipron cluster and the two Lilly baricitinib T1D trials carried from 09-05.
   Clear `.~lock.Diabetes_Research_Tracker.xlsx#` first.

8. **Do not filter on `has_results` when detecting new postings.** NCT05872620 has
   `results_posted: 2026-09-04` and `has_results: false` in the same record. Use
   `results_posted`. One-line guard in whatever consumes the snapshot.

9. **Hand-verify the `zimislecel` PubMed query.** Now confirmed zero on a freshly acquired
   corpus, so the stale-file explanation is eliminated. Either the alert is broken or
   the finding is that the INN has no literature — both are worth knowing definitively.

10. **Add PMID 42695488 to `adjudicated_offtopic_pmids.json`** (ROS in breast cancer;
    matched AI/ML × Multi-Omics on method keywords with no diabetes content).

11. **Add a Sana Biotechnology / UP421 query path** to `baseline_clinical_trials.py` —
    sponsor-string matching still returns 0 for a doctrine-named key organization.

12. **Refresh `CONTRIBUTION_STRATEGY.md`** — 175 days old, predates the 08-31 doctrine.

---

## Evidence Ledger

| Claim | Level | Basis |
|---|---|---|
| File ages and acquisition cadence | Certain | `stat` on Analysis/Results |
| PubMed + gap pointers repaired 09-05 | Certain | mtimes 03:24/03:32 + metadata `date_range` |
| `clinical_trials_latest.json` is a July 17 copy | Certain | byte-size identity (593,584 B) |
| Trial diff 8 new / 1 removed / 3 status / 2 results | Certain | key-set + field diff, 09-01 vs 09-06 |
| NCT05872620 results posted 2026-09-04 | Certain | 09-06 corpus, `results_posted` field |
| 36 results postings since 07-01; 2 catchable by pairwise diff | Certain | seen-set computed over all 125 dated snapshot files |
| 58 Phase 3 RECRUITING; sponsor counts | Certain | field filter on 09-06 corpus |
| 18 cross-domain papers, 13 new | Certain | `domains` array length >1, 09-05 vs 09-01 |
| PMID 42694848 is the only 4-domain paper on record | Certain | `domains` length across both snapshots |
| PMID 42695488 is off-topic | Certain | breast-cancer redox review, no diabetes content |
| Gap joint counts still 0 after 49 days of new literature | Certain | 09-05 `literature_gap_data.json` vs July figures |
| Multi-omics cluster is a real trend | Likely | n=2 papers in one window; needs next-window confirmation |
| Zenagamtide Ph2 efficacy figures | Likely | Novo press release via secondary coverage; primary not retrieved |
| No press release yet for NCT05872620 results | Likely | absence in two web searches; not proof |
| Gap interpretations | BRONZE | single analytical source, per the gap report's own status |
| `zimislecel` zero is a query fault | Guessing | zero is Certain; cause is not |
| Sana absence is a query blind spot | Likely | 0 sponsor-string matches vs known public activity |

---

*Automated review run — 2026-09-06. One new file written*
*(`clinical_trials_snapshot_2026-09-06.json`); no existing hub file was modified.*

*Sources for §5: [Lilly ATTAIN-1 NEJM release](https://lilly.gcs-web.com/news-releases/news-release-details/lillys-oral-glp-1-orforglipron-demonstrated-meaningful-weight) · [Lilly ATTAIN-MAINTAIN](https://www.prnewswire.com/news-releases/lillys-orforglipron-helped-people-maintain-weight-loss-after-switching-from-injectable-incretins-to-oral-glp-1-therapy-in-first-of-its-kind-phase-3-trial-302645471.html) · [Novo Nordisk zenagamtide, ADA 2026](https://www.prnewswire.com/news-releases/novo-nordisks-investigational-zenagamtide-shows-significant-a1c-reductions-with-up-to-14-6-weight-loss-in-adults-with-type-2-diabetespresented-at-ada-2026--302793124.html) · [FDA Novel Drug Approvals 2026](https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026) · [Mounjaro CV indication coverage](https://www.fox5vegas.com/2026/08/30/fda-approves-new-use-popular-diabetes-drug/)*
