# Hub Monitor Review — 2026-09-21

**Run type:** automated review (read-only; no existing files modified)
**Workspace:** `Diabetes_Research`
**Previous review:** `monitor_report_2026-09-20.md`

---

## 0. Lead finding

**The nightly pipeline did not run last night. Zero files in the entire hub carry a
2026-09-21 timestamp.** `[Certain]` — `find . -newermt "2026-09-21 00:00" -type f` returns 0
across 692 Results files plus every other folder. The newest artifact in the hub is
`Platform_Audit_Report.docx` at 2026-09-20 09:21.

This directly resolves prediction **C** from yesterday's report, and it resolves it on the
worse branch: `Analysis/Logs/` holds no traceback dated 2026-09-20 or 2026-09-21. The newest
log file in that directory is `gap_analysis_2026-07-17.log`, 65 days old. There is no crash
record because **the job never started** — or it started somewhere that does not write to
`Analysis/Logs/`.

Everything else in this report is therefore a review of **yesterday's** data, aged one day,
against live APIs queried this run.

---

## 1. File system status

| File | Age | Last modified | Verdict |
|---|---:|---|---|
| `pubmed_recent_latest.json` | 1d | 2026-09-20 03:20 | current |
| `pubmed_recent_summary.md` | 1d | 2026-09-20 03:20 | current |
| `literature_gap_report.md` | 1d | 2026-09-20 03:16 | current |
| `literature_gap_data.json` | 2d | 2026-09-19 03:26 | current |
| `agent_state.json` | 1d | 2026-09-20 03:25 | current |
| `clinical_trials_snapshot_2026-09-06.json` | 15d | 2026-09-06 02:38 | **stale** |
| `clinical_trials_latest.json` | **66d** | 2026-07-17 02:05 | **broken pointer** |
| `clinical_trials_summary.md` | 66d | 2026-07-17 02:05 | **stale** |
| `hub_monitor_report.md` | 66d | 2026-07-17 02:16 | **stale** |
| `Diabetes_Research_Tracker.xlsx` | 66d | 2026-07-17 10:07 | **stale** |
| `literature_gap_report_enriched.md` | 171d | 2026-04-03 10:05 | **abandoned** |
| `CONTRIBUTION_STRATEGY.md` | 190d | 2026-03-15 | reference doc, expected |

**609 of 692 files in `Analysis/Results/` are older than 14 days.**

### 1a. `clinical_trials_latest.json` is not the latest — still

`[Certain]` The `latest` pointer is 66 days old while dated snapshots exist through 2026-09-06:

```
clinical_trials_latest.json           metadata.generated = 2026-07-17T02:05:53   858 trials
clinical_trials_snapshot_2026-09-06   metadata.generated = 2026-09-06T02:38:16   894 trials
```

The September snapshots carry an extra metadata key the July file lacks:
`"acquired_by": "cowork scheduled monitor (sandbox) - replicates baseline_clinical_trials..."`.

That is the diagnosis. Since mid-July the trial data has been acquired by a *replica* of
`baseline_clinical_trials.py` running in the scheduled-monitor sandbox, and that replica writes
the dated snapshot but **does not update the `_latest` alias or `clinical_trials_summary.md`**.
Any downstream consumer that reads `clinical_trials_latest.json` — dashboards, the tracker, the
gap pipeline — has been reading July data for nine weeks.

Anything built on this file since 2026-07-17 should be re-derived before it is cited.

---

## 2. Clinical trial changes

Nothing new since yesterday (no run). The material change remains the **2026-07-17 → 2026-09-06
window**, which is what the stale `latest` pointer has been hiding:

| Metric | Count |
|---|---:|
| Trials, 07-17 | 858 |
| Trials, 09-06 | 894 |
| New trials | **57** |
| Removed trials | 21 |
| Status changes | **26** |
| New results posted (within snapshot pair) | 0 |

### Phase 3 recruiting — 52 trials in the current file

Highest-signal new or newly-recruiting entries:

| NCT | Sponsor | Status change / first posted | Note |
|---|---|---|---|
| NCT07797335 | Novo Nordisk | new, 2026-09-01 | AMBITION 7 — Phase 3 |
| NCT07784270 | AstraZeneca | new, 2026-08-25 | AZD6234, Phase 3 |
| NCT07776509 | AstraZeneca | new, 2026-08-20 | AZD6234 adjunct, Phase 3 |
| NCT07754461 | Boehringer Ingelheim | new, 2026-08-10 | survodutide, Phase 3 |
| NCT07613307 | Eli Lilly | NOT_YET_RECRUITING → **RECRUITING** | orforglipron, T2D |
| NCT07664553 | AstraZeneca | NOT_YET_RECRUITING → **RECRUITING** | elecoglipron, Phase 3 |
| NCT07804849 | Ain Shams University | new, 2026-09-04 | oral verapamil, newly-dx pediatric T1D, Ph2/3 |
| NCT07076199 | Novo Nordisk | RECRUITING → ACTIVE_NOT_RECRUITING | insulin icodec — enrollment closed |
| NCT06334133 | vTv Therapeutics | RECRUITING → ACTIVE_NOT_RECRUITING | **cadisegliatin** — glucokinase activator, T1D adjunct |
| NCT07502495 | Biomea Fusion | RECRUITING → ACTIVE_NOT_RECRUITING | icovamenib, Phase 2 |
| NCT06305286 | Univ. of Chicago | RECRUITING → ACTIVE_NOT_RECRUITING | T1D immunomodulation |

`NCT06334133` deserves a flag beyond its row. Cadisegliatin is the only glucokinase-activator
trial in the file, and Glucokinase is one of only two domains that appear in **four** of the top
15 literature gaps (§4). It has just closed enrollment, which means a readout is the next event.

### Key-organization Phase 3 positions (unchanged from the 09-06 file)

- **Vertex** — NCT06832410 and NCT04786262, both zimislecel/VX-880, both RECRUITING. VX-264 (NCT05791201, Ph1/2) ACTIVE_NOT_RECRUITING.
- **Eli Lilly** — baricitinib NCT07222332 / NCT07222137 (beta-cell preservation and Stage 3 delay), both RECRUITING; retatrutide and orforglipron programs across ACTIVE_NOT_RECRUITING and RECRUITING.
- **Novo Nordisk** — CagriSema NCT07564414 RECRUITING; NCT07282613 and NCT07400107 NOT_YET_RECRUITING.
- **Sana Biotechnology** — **zero trials** in the file. Either Sana has no registered diabetes trial matching the five queries, or the query set misses it. Unresolved from prior runs.

### Results postings the hub has not seen — prediction E confirmed

`[Certain]` Live ClinicalTrials.gov counts, queried this run against the five
`baseline_clinical_trials.py` filters:

| Query | Live 09-21 | Snapshot 09-06 | Δ |
|---|---:|---:|---:|
| T1D Cure & Cell Therapy | 158 | 156 | **+2** |
| T1D Immunotherapy & Prevention | 77 | 77 | 0 |
| T2D Novel Therapies (Ph2-3) | 151 | 152 | −1 |
| Diabetes Technology (Devices) | 244 | 245 | −1 |
| **Diabetes Recently Completed with Results** | **348** | **343** | **+5** |

At least **5 diabetes trials have posted results since 2026-09-06** that are not in any hub
snapshot. Prediction E called for a non-zero count with a floor of 5; the floor holds exactly,
and the number has not moved since yesterday's check — consistent with no pipeline run.

---

## 3. PubMed highlights

Data current as of 2026-09-20 03:20. 154 unique papers, 30-day lookback, 16 domains.
Diff vs. `pubmed_recent_snapshot_2026-09-18`: **46 new, 43 dropped**.

### Cross-domain papers — highest priority

New since 09-18:

- **[42759644]** *Immunometabolic Regulation of Macrophage Function in Cardio-Hepatic-Renal Comorbidities* — **3 domains**: T2D GLP-1 New, Gene Therapy, Multi-Omics. *Mol Cell Endocrinol*, 2026-09-18. The only 3-domain paper in this window.
- **[42762173]** *Sustained Glycemic Outcomes with the MiniMed…* — Closed Loop AP × **Health Equity**. *Diabetes Technol Ther*, 2026-09-19. Device-outcome work carrying an equity axis is rare and maps onto Tier 1 #6.
- **[42756821]** *Integrative multi-omics analysis prioritizes compartment-specific candidate targets…* — Microbiome × Multi-Omics. *Front Immunol*.
- **[42761395]** *Cross-fusion of digital twins and artificial intelligence in diabetes* — AI/ML × **Drug Repurposing**. *Front Endocrinol*. Drug Repurposing is a 3-paper domain; any cross-link into it is worth reading.
- **[42760621]** *Orforglipron: An Oral GLP-1 Receptor Agonist for Obesity Treatment* — *Ann Pharmacother*, 2026-09-18.

Carried forward, still unactioned: **[42627334]** β-cell function 1 year after stopping oral
baricitinib (*Diabetes Care*) and **[42720752]** beta-cell preservation in newly-diagnosed
pediatric stage 3 T1D (*Diabetologia*) — both pair directly with the two Lilly baricitinib
Phase 3 trials above.

### Key therapy tracking

| Therapy | Papers | Note |
|---|---:|---|
| dapagliflozin | 46 | highest volume |
| retatrutide | 13 | |
| orforglipron | 12 | |
| icodec | 7 | |
| teplizumab | 6 | |
| baricitinib | 3 | |
| CagriSema | 3 | |
| **zimislecel** | **0** | |

**zimislecel remains at 0 across every window, and the `VX-880` alias was still not added.**
`[Certain]` — `grep` of `baseline_pubmed_alerts.py` line 67 shows only `"zimislecel"`. This was
action item 4 yesterday. Two Vertex Phase 3 trials are recruiting and Vertex has publicly
accelerated its FDA submission target to 2026; the hub's literature channel is blind to the
program under its older name. Prediction D remains untested because the one-line change was not
made.

### Domain volumes (30-day counts, 09-20 vs 09-18)

Largest movers: Biomarker 116→110, Microbiome 140→135, Gene Therapy 53→**57**, Closed Loop
23→**26**. Nothing anomalous. Floor domains unchanged: **Drug Repurposing 3**, **Epigenetics 3**,
**GLP-1 Pharmacogenomics 3** — these three have sat at 2–3 papers per 30 days for weeks, which
is the recurring publication-volume evidence behind the gap scores in §4.

---

## 4. Gap analysis

Source: `literature_gap_data.json`, generated 2026-09-19, 30 domains / 435 pairs, PubMed 2020+.

### Top 5 by raw gap score

| # | Pair | Gap | Joint | Expected |
|---|---|---:|---:|---:|
| 1 | Beta Cell Regen × Health Equity | 100.0 | 0 | 1766 |
| 2 | Insulin Resistance × Islet Transplant | 100.0 | 1 | 2291 |
| 3 | Islet Transplant × GWAS / Polygenic | 100.0 | 0 | 1178 |
| 4 | Islet Transplant × Personalized Nutr | 100.0 | 0 | 421 |
| 5 | Islet Transplant × Drug Repurposing | 100.0 | 0 | 397 |

The score saturates at 100.0 across dozens of pairs and cannot rank them. Ranking by **expected
joint count** instead separates a striking void from a small one: pair 2 (expected 2291, observed
1) is a far larger absence than pair 5 (expected 397, observed 0). This was action item 8
yesterday and is still not implemented. Note that the interpreted report already demotes pairs 3
and 4 to "methodologically distinct" — they are artifacts of the saturated score, not
opportunities.

### Alignment with Tier 1 doctrine areas

| Gap | Tier 1 match | Assessment |
|---|---|---|
| Islet Transplant × Drug Repurposing | **#4 Drug Repurposing Screening (18/20)** + #2 Literature Synthesis | **Strongest.** Absence confirmed by an unbounded all-time PubMed re-run (2026-09-06): 7 records, none a computational screen. Fully open data — DrugBank, OpenTargets, STRING. |
| Beta Cell Regen × Health Equity | **#6 Epidemiological Analysis (17/20)** | Strong. GBD/CDC data open; a 0-paper intersection against 1503 and 2074 single-domain counts. |
| Glucokinase × Drug Repurposing | **#4 (18/20)** | Strong, and newly time-sensitive — cadisegliatin (NCT06334133) just closed enrollment. |
| Insulin Resistance × Islet Transplant | #1 Multi-Omics / #3 Trial Intelligence | Largest absolute void, but needs graft-outcome data the hub does not hold. |
| Islet Transplant × GWAS, × Personalized Nutr | — | Classified methodologically distinct. Deprioritize. |

**Validation level: BRONZE** for all gap classifications, per the report's own header — single
analytical source, expert confirmation outstanding.

---

## 5. Breaking news check

Web search, last 7 days. Nothing that changes the hub's posture this week; the significant 2026
items were already in the record:

- **Retatrutide** — first Phase 3 T2D + obesity results reported June 2026. HbA1c −18.5/−20.3/−21.2 mmol/mol at 4/9/12 mg vs −8.9 placebo at 40 weeks; weight −11.5% to −15.3% vs −2.6%. *Evidence level: Level 1 (randomized Phase 3), conference-reported.*
- **Orforglipron** — ACHIEVE Phase 3 program reported; oral non-peptide GLP-1 RA.
- **Zimislecel** — 12/12 full-dose patients with ≥1yr follow-up reached HbA1c <7% and >70% TIR; 10/12 insulin-free. RMAT and Fast Track held. FDA submission target pulled forward to 2026. *Evidence level: Level 1, single-arm, n=12.*
- **FDA, 2026** — Garzulys (insulin aspart-fsan, NovoLog biosimilar) approved 2026-07-24. Insulin efsitora alfa decision expected H2 2026. No new diabetes approval identified in the last 7 days.

No item this week meets the "genuinely significant" bar for a new tracker entry beyond what
prior reports already logged.

---

## 6. Repository state

`[Certain]` `git log`: local `main` at `533f588`; `origin/main` at `f7e976f`,
*"Monitor artifacts, dashboards, and analysis refresh through 2026-04-20"*.

- **117 commits unpushed.** Origin frozen for **154 days.**
- 7 files uncommitted in the working tree (was 0 for three consecutive nights — these are yesterday's 09:xx audit artifacts).

The unpushed count grew from 115 to 117 since yesterday. Nothing published from this hub since
April is visible to anyone but this machine.

---

## 7. Recommended actions

Ordered by cost-to-value, with the cheapest first.

**1. Find out why last night's job did not run.** `[Certain]` that it produced nothing;
`[Guessing]` as to why. Check the scheduled-task status and whether it is still enabled. This is
the second consecutive day the scheduler has been the top finding, and `Analysis/Logs/` has
recorded nothing since July — so add a log write to the sandbox replica regardless of what the
scheduler says, or the next failure will be equally silent.

**2. Fix the `_latest` pointer.** The sandbox replica must copy its dated snapshot to
`clinical_trials_latest.json` and regenerate `clinical_trials_summary.md`. Until then, every
consumer of that file reads 2026-07-17 data. One line in the replica.

Manual stopgap:
```powershell
Copy-Item Analysis\Results\clinical_trials_snapshot_2026-09-06.json `
          Analysis\Results\clinical_trials_latest.json
```

**3. Refresh trial data — it is 15 days old and ≥5 results postings are missing.**
```powershell
python Analysis\Scripts\baseline_clinical_trials.py
```

**4. Add the `VX-880` alias** to `baseline_pubmed_alerts.py` line 67. One line. Third time this
has been carried forward. Until it lands, prediction D cannot be tested and the zimislecel zero
cannot be claimed as a real absence.

**5. Push.** 117 commits, 154 days, working tree effectively clean.
```powershell
git push origin main
```

**6. Update the tracker.** `Diabetes_Research_Tracker.xlsx` is 66 days old and predates all 57
new trials and 26 status changes in §2. Priority rows: NCT06334133 (cadisegliatin, enrollment
closed), NCT07613307 (orforglipron now recruiting), the two AstraZeneca AZD6234 Phase 3 starts.

**7. Run `hub_monitor.py`** — its report is 66 days old, so file-change detection has been blind
for nine weeks. That blindness is why the §1a pointer defect persisted.

**8. Rank zero-cells by expected joint count** as a secondary gap ordering (§4). One line;
carried forward from yesterday.

**9. Read the two baricitinib papers** — [42627334] and [42720752] — against the two Lilly Phase
3 baricitinib trials. Trial-to-literature linkage is Tier 1 #3, and this is the cleanest
available instance of it.

**10. Resolve `literature_gap_report_enriched.md`** (171 days). Re-run or delete. A stale
enriched report beside a 1-day-old base report is a citation hazard.

**11. Scope the Drug Repurposing × Islet Transplant screen** (gap #5 by score, #1 by evidence
quality). Still the best-evidenced gap, still Tier 1 #4, still fully open data. Redo the absence
confirmation against the corrected trial query before committing.

---

## 8. Predictions for the next run (falsifiable)

| # | Prediction |
|---|---|
| **A** | If action 1 finds the scheduler disabled or misconfigured → `Analysis/Logs/` stays empty and files reappear only after a manual re-enable. If it finds the scheduler *enabled and reporting success* → the replica is writing somewhere outside this workspace, and a second copy of the hub exists. |
| **B** | If action 3 runs → the new snapshot's "Recently Completed with Results" category lands at **348 ± 3**, and the snapshot diff reports **≥ 5** newly-posted results against 09-06. A zero here means the diff logic compares against `_latest` (66d) rather than the newest dated snapshot, which would be a second instance of the §1a defect. |
| **C** | If action 4 runs → zimislecel therapy hits go **> 0** on the next PubMed pull. Still 0 with the alias in place → the absence is real and publishable as a negative finding. |
| **D** | If action 2 runs → the next gap and dashboard builds will shift, because they have been consuming July trial data. Expect non-trivial diffs in `Dashboards/Clinical_Trial_Dashboard.html` and any trial-derived gap cell. If nothing shifts, no downstream consumer actually reads `clinical_trials_latest.json` and the pointer is cosmetic. |
| **E** | NCT06334133 (cadisegliatin) moves to COMPLETED within 90 days, and a glucokinase-activator readout follows within 180. If so, the Glucokinase × Drug Repurposing gap acquires a live comparator and should be re-scoped as time-sensitive rather than exploratory. |

---

*Generated by the automated hub monitor, 2026-09-21. Review only — no existing files were
modified. All file ages, snapshot diffs, git state and ClinicalTrials.gov counts verified by
direct read or direct API query this run. Confidence levels per Research Doctrine: `[Certain]` =
hard evidence in hand, `[Likely]` = strong inference, `[Guessing]` = gap-filling. Gap
classifications remain BRONZE pending expert validation.*
