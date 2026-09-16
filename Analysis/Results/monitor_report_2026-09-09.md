# Diabetes Research Hub — Monitor Report

**Run date:** 2026-09-09 (automated)
**Prior report:** monitor_report_2026-09-08.md
**Mode:** Review run. No existing hub files modified.
**Environment note:** The Linux sandbox failed to mount this run, so no Python executed. All
registry and PubMed figures below come from direct API calls; all file facts come from reading
the files. OS modification timestamps were **not** readable — the file table uses each file's
own internal `generated` field instead. This is stated wherever it matters.

---

## Headline

**The registry moved today, and yesterday's report said it wouldn't have.** The freshness gate
recommended in 09-08 §8 item 1 was run before diffing, it returned non-zero, and the diff that
followed found real change: 4 status transitions, 2 new records, 1 new results posting — the
first informative delta since 09-01.

But the more useful finding is a defect in the instrument yesterday built to fix the instrument.

Yesterday's headline chart printed `Tue 09-08 · 0 new 0` and its evidence table rated the
whole series **[Certain]**. Re-queried today:

```
  LastUpdatePostDate    09-08 report    today's query    delta
  ──────────────────────────────────────────────────────────────
  Fri 2026-09-04              983             842        −141
  Sat 2026-09-05                0               0           0
  Sun 2026-09-06                0               0           0
  Mon 2026-09-07 (Labor Day)    0               0           0
  Tue 2026-09-08                0           1,033      +1,033
  Wed 2026-09-09                —           1,297           —
```

Two things are wrong with the old series, and they are different problems.

**1. The 09-08 row was a false zero.** ClinicalTrials.gov published 1,033 updates on 09-08.
The 03:40 ET run read zero because the batch had not posted yet. Yesterday's report *correctly
diagnosed* this failure mode — and then printed the zero as data anyway, inside a chart it
rated [Certain]. The diagnosis and the table contradicted each other and the table won.

**2. `LastUpdatePostDate` is not an event log — it is a "most recent update" field, and
historical day-counts decay.** 09-04 read 983 yesterday and 842 today. Those 141 records did
not vanish; they were updated again on 09-08 or 09-09 and moved forward into the newer bucket.
Any bar chart of past days built on this field will keep shrinking retroactively and can never
be reproduced. [Certain — same query, two dates, 141-record difference.]

The consequence for the freshness gate: **it is valid for today and only for today.** A
non-zero count for the current date proves the source published. A zero for a *past* date
proves nothing — it may mean every record from that day has since been re-updated. Gate on
`today`, and never reconstruct history from this field.

---

## 1. File System Status

Ages measured from each file's internal `generated` timestamp (OS mtimes unavailable this run).

| File | Internal generated | Age | State |
|------|--------------------|-----|-------|
| `literature_gap_data.json` | 2026-09-08 03:17:27 | 1d | **Current** |
| `literature_gap_report.md` | 2026-09-08 03:17 | 1d | **Current** |
| `pubmed_recent_latest.json` | 2026-09-06 09:18:08 | 3d | Current (139 papers, 16 domains) |
| `clinical_trials_snapshot_2026-09-06.json` | 2026-09-06 02:38:16 | 3d | Newest trial snapshot (894 trials, sandbox-acquired) |
| `RESEARCH_DOCTRINE.md` | 2026-08-31 | 9d | Current |
| `clinical_trials_latest.json` | 2026-07-17 02:05:53 | **54d** | **BROKEN POINTER** — 858 trials |
| `hub_monitor_report.md` | 2026-07-17 02:16:51 | **54d** | **STALE** |
| `hub_monitor_state.json` / `clinical_trials_summary.md` | 2026-07-17 | **54d** | **STALE** |
| `Diabetes_Research_Tracker.xlsx` | — | **54d** | **STALE**, still lock-held |
| `CONTRIBUTION_STRATEGY.md` | 2026-03-15 | **178d** | **STALE** |

### Correction to yesterday's file table

Yesterday listed `literature_gap_data.json` and `literature_gap_report.md` at **2026-09-06
09:12**. Both files carry `"generated": "2026-09-08T03:17:27"` and a date range ending
2026-09-08. **The gap analysis is one day old, not three.** Recommended action "re-run gap
analysis — results are X days old" should be dropped from the queue. [Certain — read from the
files.]

### Snapshot coverage gap

`clinical_trials_snapshot_*.json` exists daily from 2026-03-15 through **2026-07-17**, then:
08-27, 08-28, 09-01, 09-06. Nothing for 07-18→08-26, 09-02→09-05, 09-07, 09-08.

This is why today's "since last snapshot" window is 3 days wide, and why the two CagriSema
completions below cannot be dated. **The hub's trial history has a 41-day hole and is now
sampled roughly weekly.** Consecutive-day diffing was never going to work on this; that is a
data-collection problem, not a detector problem.

### Residue from the 09-07 run — still present

`Analysis/Results/_wtest.txt`, `.gap_checkpoint.json.__unlinktest`,
`.gap_checkpoint.json.testbak`, and root `.wtest`. Zero value, safe to delete.

---

## 2. Clinical Trial Changes

**Freshness gate: PASS.** 1,297 records last-updated 2026-09-09; 412 studies first-posted
09-08→09-09. The source is live and this diff is meaningful.

### Category counts, 2026-09-06 snapshot → 2026-09-09 live

| Category | 09-06 | 09-09 | Δ |
|----------|------:|------:|---:|
| T1D Cure & Cell Therapy | 156 | 157 | +1 |
| T1D Immunotherapy & Prevention | 77 | 77 | 0 |
| T2D Novel Therapies (Ph 2–3) | 152 | 151 | **−1** |
| Diabetes Technology (Devices) | 245 | 246 | +1 |
| Diabetes Recently Completed w/ Results | 343 | 344 | +1 |

Reconciles exactly to **894 → 895 unique trials**: two records in, one out. Every delta is
accounted for by a named NCT below — no unexplained drift. [Certain]

### New records (2)

| NCT | Sponsor | Study | Phase | Status | First posted |
|-----|---------|-------|-------|--------|--------------|
| **NCT07808385** | Mayo Clinic | DEKA TWIIST insulin pump w/ Tidepool Loop algorithm in **pregnant people with pre-existing T1D** | NA | NOT_YET_RECRUITING | 2026-09-08 |
| **NCT05232071** | Inventiva Pharma | Lanifibranor ± empagliflozin in **NASH + T2D** — results first posted **2026-09-09** | PHASE2 | COMPLETED | (results new) |

NCT07808385 satisfies both the T1D-cell-therapy and device filters, which is why two categories
each gained one from a single record.

### Status changes (4)

| NCT | Sponsor | 09-06 | 09-09 | Note |
|-----|---------|-------|-------|------|
| **NCT07216391** | NIDDK | NOT_YET_RECRUITING | **RECRUITING** | Platform trial delaying Stage 3 T1D: **teplizumab vs ATG**, PHASE2 |
| **NCT07282613** | Novo Nordisk | NOT_YET_RECRUITING | **RECRUITING** | **CagriSema in children/adolescents with T2D**, PHASE3 |
| **NCT07219602** | NewAmsterdam Pharma | RECRUITING | ACTIVE_NOT_RECRUITING | Obicetrapib/ezetimibe in T2D + metabolic syndrome, PHASE3 — enrollment closed |
| **NCT06926842** | Zealand Pharma | ACTIVE_NOT_RECRUITING | **COMPLETED** | **Petrelintide ZUPREME-2**, PHASE2b — see below |

### The item worth acting on: ZUPREME-2 completed

NCT06926842 (petrelintide, amylin analog, Zealand/Roche) flipped to COMPLETED on 09-09.
Zealand has guided to **topline ZUPREME-2 results in H2 2026**. A registry status flip to
COMPLETED ahead of a guided readout is the one signal class where the registry genuinely leads
the press — unlike ATTAIN-2 last week, which the registry *trailed*.

This is a **watch item, not a finding**: completion means data collection ended, not that
results exist. Set a watch on Zealand/Roche IR and on `ResultsFirstPostDate` for NCT06926842.
[Likely — registry status is Certain; the inference that readout is near rests on company
guidance retrieved by web search.]

### Two CagriSema trials that look like news and are not

`NCT06534411` (CagriSema **vs tirzepatide**, head-to-head in T2D) and `NCT06323161` (CagriSema
vs placebo on basal insulin) both show COMPLETED with a 09-09 update. Neither is in the 09-06
snapshot. Grepped across all **125** stored snapshots: both appear in 121 of them, and **the
most recent snapshot containing either is 2026-07-17.** They left the active corpus somewhere in the 41-day collection hole, and today's
update is routine record maintenance, not a completion event.

Reporting a completion date for these would be a guess. The honest statement is: *both
completed between 2026-07-17 and 2026-09-06, exact date unknown, because the hub was not
collecting.* A CagriSema-vs-tirzepatide head-to-head completing is the kind of event this hub
exists to catch, and it was missed by 54 days of not running the script. [Certain that they are
absent from all snapshots after 07-17; the completion date itself is unknown.]

### Reference counts

- Diabetes PHASE3 + RECRUITING, registry-wide, no date filter: **81**. (Yesterday's "58" was
  measured inside the 894-trial corpus. Different denominator, not a contradiction — but the
  hub should pick one and label it.)
- Results posted in the trailing 14 days (`ResultsFirstPostDate >= 2026-08-26`): **4** —
  NCT05232071 (09-09, new), NCT05872620 ATTAIN-2 (09-04), NCT04828785 (09-02), NCT04506151
  (08-27).

---

## 3. Data Quality — `has_results` root cause found

Yesterday established the symptom ([Certain], 344/344 wrong) and guessed the cause: *"almost
certainly looking inside `protocolSection` for a flag that lives one level up."*

Reading `baseline_clinical_trials.py`, the actual cause is adjacent but different, and it
changes the fix:

```python
# line 64-67 — the fields request. No results section is asked for.
"fields": "NCTId,BriefTitle,OverallStatus,Phase,EnrollmentCount,..."

# line 88
results_sec = study.get("resultsSection")     # correct level — but never returned
# line 115
"has_results": results_sec is not None,       # therefore always False
```

The lookup level is right. **The field is never requested, so the API never sends it, so the
expression is a constant `False` by construction.** Adding `HasResults` to the `fields` list and
reading `study.get("hasResults")` fixes it — confirmed working: today's results query returned
`"hasResults": true` on all four records. Moving the lookup without changing the `fields` list —
the fix implied by yesterday's wording — would not have worked. [Certain — script read + live
API response.]

---

## 4. PubMed Highlights

Corpus unchanged since 09-06: **139 papers, 16 alert domains** (the task spec says 15; the
script defines 16).

**Cross-domain papers: 20 of 139 — independently recounted from the JSON this run, not
inherited.** [Certain]

Reading priority unchanged:

1. **PMID 42694848** — COL1A2/APOLD1 dual-axis framework for diabetic nephropathy–retinopathy
   comorbidity. Only 4-domain paper on record (AI/ML + Biomarker + Complications + Multi-Omics).
   Hits Doctrine Tier 1 §1 (19/20) and §5 (18/20). Flagged 09-06, still unread.
2. **PMID 42627334** — β-cell function 1 year after stopping oral baricitinib in T1D
   (*Diabetes Care*).
3. **PMID 42626948** — gene-edited hypoimmune islets as a T1D cure.
4. **PMID 42673585** — GLP-1 RAs and co-agonists for weight loss without diabetes (*Ann Intern Med*).
5. **PMID 42694300** — oral microbiome + metabolome in Alström / Bardet-Biedl.

### How stale is the corpus? Measured, not assumed

New PubMed records, Entrez-dated 2026-09-06→09-09:

| Query | New records |
|-------|------------:|
| `diabetes` (all) | 482 |
| T1D Stem Cell Cure (as coded) | 1 |
| T1D Immunotherapy (as coded) | 1 |

**Re-running `baseline_pubmed_alerts.py` is low urgency.** Diabetes-wide volume looks large,
but the two highest-value T1D domains added one paper each in three days. Nothing is being
missed by waiting. [Certain — E-utilities `esearch`, `datetype=edat`.]

### Correction: the zimislecel alert fix does not "double recall" in practice

Yesterday's recommendation #7 was to change the alert term to `VX-880 OR zimislecel`, described
as *"one line, doubles recall on the hub's most strategically important asset."*

Verified today:

| Query | All-time | Last 30 days |
|-------|---------:|-------------:|
| `zimislecel` | 3 | 0 |
| `"VX-880"` | 6 | 0 |
| `"VX-880" OR zimislecel` | — | **0** |

The lifetime counts are right (3 and 6). But the alert runs on a 30-day window, and **the union
returns zero papers in that window.** The edit is still correct and should be made — it will
matter the moment Vertex publishes — but it changes no current output and does not belong above
items that do. Priority reduced. [Certain]

### Epigenetics over-filter — independently reproduced

| Query | 30-day count |
|-------|-------------:|
| `diabetes AND (epigenetic OR methylation)` | **129** |
| `... AND (GWAS OR "genome-wide")` (as coded) | **1** |

129× recall loss, reproduced on a fresh window (yesterday measured 126× on a window one day
earlier). Yesterday's diagnosis holds. This remains a two-line edit. [Certain]

---

## 5. Gap Analysis Summary

Regenerated **2026-09-08 03:17**, 30 domains, 435 pairs. Validation level **BRONZE** per
Doctrine — single analytical source, expert confirmation outstanding.

### Top 5 by gap score ("potentially meaningful")

| # | Intersection | Gap | Joint pubs | Tier 1 alignment |
|---|--------------|----:|-----------:|------------------|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | §6 Epidemiological (17/20) |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | §2 Literature Synthesis (19/20) |
| 3 | **Islet Transplant × Drug Repurposing** | 100.0 | 0 | **§4 Drug Repurposing (18/20)** |
| 4 | Islet Transplant × Health Equity | 100.0 | 0 | §6 (17/20) |
| 5 | Gene Therapy × LADA | 100.0 | 0 | §2 (19/20) |

### Gap #3 — the hub has now cited three different counts for the same claim

| Source | All-time joint records |
|--------|----------------------:|
| `literature_gap_report.md` (09-08), rationale text | **7** |
| `monitor_report_2026-09-08.md` §4 | **1** ("verified 09-07 at exactly 1") |
| This run, `("islet transplantation" OR "islet transplant") AND ("drug repurposing" OR "drug repositioning")` | **2** (PMIDs 29018828, 27821710) |

None of these is wrong; they are three different query strings, and none of the three artifacts
records which string it used. **The direction is robust — this intersection holds single-digit
all-time records and has no incumbent — but the hub cannot currently reproduce its own headline
number.** Before this gap is written into a preregistration or a manuscript, the exact query
string must be pinned in the artifact next to the count. That is a Doctrine provenance
requirement, and gap #3 is the hub's lead candidate. [Certain that three counts are cited;
[Guessing] as to which query produced the 7.]

The 09-08 caveat still stands: five of the top twelve gaps pair a domain against Health Equity,
a keyword-brittle concept. Verify #1, #4, #7, #10, #12 by free-text query before committing —
and record the query string this time.

---

## 6. Breaking News

**Nothing in the last 7 days changes hub priorities.** Two sweeps run (Phase 3 readouts, FDA
actions). Background, none of it new this week:

- **Mounjaro / tirzepatide CV indication expansion** (late Aug 2026) — still the most
  consequential recent FDA action in scope, still **not recorded in the hub**. Links to
  NCT04255433 (SURPASS-CVOT, results posted 07-08). [Likely — FDA primary source still not
  fetched; confirm on fda.gov before logging.]
- **Insulin efsitora alfa** — possible FDA decision in H2 2026; would be the second weekly basal
  insulin approved in the US. Not in the hub's watch list. [Likely]
- **Vertex zimislecel** — FDA/EMA/MHRA submissions still guided for 2026; no filing
  announcement found. RMAT + Fast Track + PRIME + ILAP designations confirmed. Single event most
  likely to reset hub priorities; keep the dedicated watch. [Likely — negative result]
- Prior-2026 and already recorded: retatrutide TRANSCEND-T2D-1 and TRIUMPH-2/3, oral semaglutide
  25 mg, first generic dapagliflozin, first generic liraglutide, Garzulys (07-30).

One item within the 7-day window worth a skim, not a reprioritisation: a 2026-09-08 release
titled *"Replacing Insulin Cells Works. Keeping The Cells Alive Is the Trick"* — promotional
framing, topic-relevant to the islet/beta-cell line. [Guessing as to substance; not read.]

---

## 7. Data Quality Defects — Current List

| # | Defect | Status |
|---|--------|--------|
| 1 | `clinical_trials_latest.json` is a 54-day-old duplicate of the 07-17 snapshot | Open |
| 2 | `has_results` constant `False` — `resultsSection` never requested in `fields` | **Root cause corrected today (§3)** |
| 3 | Null `title` on PMID 42698931 in `pubmed_recent_latest.json` | Open, 1 of 139 — re-verified today, `"title": null`, *Biochem Biophys Rep* 2026-Sep |
| 4 | Epigenetics + Drug Repurpose alert queries over-filtered (129× / 6×) | Diagnosed; two-line edit pending |
| 5 | `phase` uses two null encodings, `"NA"` and `"N/A"` | Open |
| 6 | No source-freshness gate in the shipped scripts | Open — gate run manually today, PASS |
| 7 | Scheduled run time precedes the daily registry batch | Open — caused yesterday's false 09-08 zero |
| 8 | **`LastUpdatePostDate` day-counts decay retroactively; historical series are not reproducible** | **New today (headline)** |
| 9 | **Gap-analysis artifacts cite counts without recording the query string** | **New today (§5)** |
| 10 | **41-day trial-snapshot hole (07-18→08-26); collection now ~weekly** | **New today (§1)** |

---

## 8. Recommended Actions

Ranked. ▲ = new or re-ranked today.

1. ▲ **Run the two dead local scripts.** Promoted to #1. Yesterday ranked instrumentation fixes
   above collection; today showed why that is backwards — a CagriSema-vs-tirzepatide head-to-head
   completed inside the collection hole and the hub cannot date it. A perfectly instrumented
   monitor over a corpus that is not being collected still misses the event.
   ```
   python Analysis/Scripts/baseline_clinical_trials.py
   python Analysis/Scripts/hub_monitor.py
   ```
   Both 54 days stale. This also repairs `clinical_trials_latest.json`.

2. ▲ **Gate on freshness for *today only*.** Query `AREA[LastUpdatePostDate]RANGE[<today>,<today>]`;
   if `totalCount == 0`, report "source not yet published today" and skip the diff. **Do not**
   build or store historical day-series from this field — they decay (§ headline). Delete the
   13-day bar chart from the 09-08 report's lineage rather than extending it.

3. **Move the scheduled run past the daily batch.** 03:40 ET is before it; mid-morning ET or
   later reads the same day. Combined with #2 this eliminates the false-null class entirely.

4. ▲ **Fix `has_results` correctly** — add `HasResults` to the `fields` string in
   `baseline_clinical_trials.py` *and* read `study.get("hasResults")`. Changing only the lookup
   level, per yesterday's wording, would not have worked (§3).

5. **Fix the two over-filtered alert queries** — delete the trailing AND-clause from both:
   ```
   "Diabetes Epigenetics":    'diabetes AND (epigenetic OR methylation)'
   "Diabetes Drug Repurpose": 'diabetes AND ("drug repurposing" OR "drug repositioning")'
   ```

6. ▲ **Watch NCT06926842 (petrelintide ZUPREME-2)** — completed 09-09, topline guided for H2
   2026. Set an alert on its `ResultsFirstPostDate`. Highest-probability near-term readout the
   hub can see before the press does.

7. ▲ **Pin the query string next to every gap count** in `literature_gap_report.md` and any
   downstream artifact. Gap #3 currently carries three incompatible numbers (7 / 1 / 2) across
   hub documents (§5). Resolve before it reaches a preregistration.

8. **Replace consecutive-day diffing with a persistent seen-set** keyed on `results_posted` and
   `last_update_posted`. Now more valuable than it was yesterday, because #1 will restore daily
   collection and a weekly-sampled corpus needs event keys, not day-to-day diffs.

9. **Log the Mounjaro CV indication expansion** in the tracker, linked to NCT04255433. Confirm
   on fda.gov first.

10. **Read PMID 42694848** (COL1A2/APOLD1 multi-omics, only 4-domain paper) then **PMID 42627334**
    (post-baricitinib β-cell durability, *Diabetes Care*).

11. **Update the tracker** — 54 days stale. Warranted: NCT06926842 (ZUPREME-2 completed),
    NCT07216391 (teplizumab vs ATG now recruiting), NCT07282613 (pediatric CagriSema now
    recruiting), NCT05232071 (lanifibranor results), NCT07808385 (pump-in-pregnancy),
    NCT05872620 (ATTAIN-2 effect sizes), NCT06534411 / NCT06323161 (CagriSema completions,
    date unknown), plus the Mounjaro CV label. Clear `.~lock.Diabetes_Research_Tracker.xlsx#`
    first.

12. **Track NCT06239636 by NCT ID** (Carlsson/Uppsala, not Sana). Sponsor-string watches miss
    investigator-sponsored first-in-human work structurally.

13. **Add `zenagamtide` to the tracked-therapy list** (NCT07797335, Novo, PHASE3 as of 09-01).

14. ▼ **Change the zimislecel alert term to `"VX-880" OR zimislecel`.** Still correct, now
    demoted: the union returns 0 papers in the 30-day alert window (§4). Do it, but not first.

15. **Add insulin efsitora alfa to the FDA watch list** — possible H2 2026 decision, currently
    untracked.

16. **Broaden `report_freshness_audit`** to cover the trial pipeline; it passes 2 files while the
    trial pointer sits 54 days stale.

17. **Delete the 09-07 test residue** (`_wtest.txt`, `.gap_checkpoint.json.__unlinktest`,
    `.gap_checkpoint.json.testbak`, root `.wtest`).

18. **Refresh `CONTRIBUTION_STRATEGY.md`** — 178 days old, predates the 08-31 doctrine.

**Dropped from yesterday's queue:** "re-run gap analysis — results are X days old." The gap
analysis regenerated 2026-09-08 03:17 (§1).

---

## Evidence & Provenance

| Claim | Basis | Level |
|-------|-------|-------|
| Registry published 09-08 (1,033) and 09-09 (1,297); 09-05/06/07 = 0 | ClinicalTrials.gov API v2, `AREA[LastUpdatePostDate]RANGE[d,d]`, whole registry, 09-09 | **Certain** |
| Yesterday's 09-08 zero was a false negative | Same query, same date, non-zero today | **Certain** |
| `LastUpdatePostDate` counts decay retroactively | 09-04 bucket: 983 (per 09-08 report) → 842 (today) | **Certain** |
| Category counts 157/77/151/246/344 | Five `filter.advanced` queries replicating `baseline_clinical_trials.py` verbatim, `countTotal=true`, 09-09 | **Certain** |
| 894 → 895 reconciliation | Deltas fully attributed to NCT07808385, NCT05232071, NCT06926842 | **Certain** |
| 4 status changes | Live API status vs `clinical_trials_snapshot_2026-09-06.json` field read | **Certain** |
| NCT06534411 / NCT06323161 absent after 07-17 | Grep across all 125 stored snapshots (present in 121, none after 07-17) | **Certain** (completion date itself unknown) |
| ZUPREME-2 readout is near | Registry COMPLETED (Certain) + Zealand H2-2026 guidance via web search | **Likely** |
| `has_results` root cause is the `fields` omission | Source read of `baseline_clinical_trials.py` L64–115 + live `hasResults: true` | **Certain** |
| 20 of 139 cross-domain papers | Recounted from `pubmed_recent_latest.json` this run | **Certain** |
| PubMed staleness: 482 / 1 / 1 in 09-06→09-09 | E-utilities `esearch`, `datetype=edat` | **Certain** |
| zimislecel 3 / VX-880 6 all-time; 0 in 30d | E-utilities `esearch`, unbounded and 30-day | **Certain** |
| Epigenetics 129 vs 1 (30d) | E-utilities `esearch`, both variants | **Certain** |
| Gap analysis regenerated 09-08 03:17 | `"generated"` field in `literature_gap_data.json` | **Certain** |
| Three conflicting gap-#3 counts | Direct read of both artifacts + own query | **Certain** |
| Mounjaro CV expansion; efsitora H2-2026 | Web search, FDA primary source not fetched | **Likely** |
| No significant breaking news in 7d | Web search, 4 queries, negative result | **Likely** |
| Gap classifications | Inherited from `literature_gap_report.md` | **BRONZE** (per Doctrine) |
| File ages | Internal `generated` fields; OS mtimes unreadable (sandbox down) | Certain for files carrying the field; unknown for `.xlsx` and `CONTRIBUTION_STRATEGY.md` |

No snapshot was written this run — no Python executed, and review runs do not modify hub files.

*Generated by the Diabetes Research Hub automated monitor — 2026-09-09*
