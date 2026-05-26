# Diabetes Hub Monitor Report — 2026-05-26

**Scan time:** 2026-05-26 (Tuesday)
**Previous report:** monitor_report_2026-05-25.md
**Scope:** Daily review of script outputs + 7-day web scan
**Evidence level:** BRONZE (single analytical pass; web items unverified beyond press releases)

---

## TL;DR — Actionable Items

1. **MannKind Afrezza pediatric PDUFA is THIS FRIDAY (May 29).** First potential needle-free insulin for T1D/T2D kids 4–17. Trial missed primary noninferiority in full ITT but met it in mITT — outcome is uncertain. Add Friday calendar reminder and prep tracker entry to capture decision either way.
2. **5 cross-domain PubMed papers in today's snapshot diff** — highest value review targets (PMIDs 42181212, 42181960, 42184024, 42184924, 42185046). Three intersect Tier 1 areas (Multi-Omics, AI/ML, Microbiome).
3. **`literature_gap_data.json` is 36 days old** (last refresh 2026-04-20). Same flag carried from yesterday — re-run `python project1_literature_gap_analysis.py`. Also stale: `islet_repurposing_*` (52d) and `microbiome_ml_*` (51d).
4. **Closed-Loop AP publication volume jumped +44% week-over-week** (16 → 23). Small absolute number but largest single-week % move — worth a quick scan for whether this signals a real cluster or a few prolific groups.
5. **No new trial results posted in last 7 days; only 3 trial status changes; 5 new trials.** Trial pipeline is quiet — focus the week on literature follow-through and the stale gap-analysis refresh.

---

## File System Status

| File | Modified | Age | Status |
|------|----------|-----|--------|
| hub_monitor_report.md | 2026-05-26 07:04 | fresh | OK |
| clinical_trials_latest.json | 2026-05-26 07:04 | fresh | OK |
| clinical_trials_summary.md | 2026-05-26 07:04 | fresh | OK |
| pubmed_recent_latest.json | 2026-05-26 07:04 | fresh | OK |
| pubmed_recent_summary.md | 2026-05-26 07:04 | fresh | OK |
| literature_gap_report.md | 2026-05-25 08:13 | 1d | OK |
| **literature_gap_data.json** | **2026-04-20 15:35** | **36d** | **STALE — refresh recommended** |
| **literature_gap_matrix.xlsx** | **2026-04-20 15:35** | **36d** | **STALE — same pipeline** |
| **islet_repurposing_targets.json** | **2026-04-03** | **52d** | **STALE** |
| **islet_repurposing_drug_candidates.json** | **2026-04-03** | **52d** | **STALE** |
| **microbiome_ml_feature_importance.json** | **2026-04-04** | **51d** | **STALE** |
| agent_state.json | 2026-05-25 08:17 | 1d | OK |
| citation_validation.json | 2026-05-25 08:13 | 1d | OK |
| evidence_network.json | 2026-05-25 08:13 | 1d | OK |
| gap_evidence.json | 2026-05-25 08:13 | 1d | OK |
| pmid_verification.json | 2026-05-25 08:13 | 1d | OK |
| extracted_corpus_data.json | 2026-05-18 08:11 | 8d | OK |

Hub monitor flagged **644 result files older than 14 days** (up from 606 yesterday). The vast majority are daily snapshot archives that should be left alone. The salient stale files are the five above; the gap-analysis pipeline and the two project-specific pipelines (islet drug repurposing, microbiome ML) have not been re-run for over a month.

**Hub-monitor file summary (today's scan):**
- 4 new files (today's clinical_trials, pubmed, and monitor report snapshots + yesterday's iterate_run_report)
- 30 modified files (state files and yesterday's dashboard refresh outputs)
- 0 removed files; 866 total tracked (+4 vs. yesterday)

---

## Clinical Trial Changes

**Total trials tracked: 797** (unchanged vs. yesterday; +2 vs. 2026-05-18)

### Category distribution (current)

| Category | Count |
|----------|-------|
| Diabetes Recently Completed with Results | 281 |
| Diabetes Technology (Devices) | 225 |
| T1D Cure & Cell Therapy | 153 |
| T2D Novel Therapies (Phase 2-3) | 140 |
| T1D Immunotherapy & Prevention | 71 |

### Phase 3 RECRUITING — 46 active trials

No change in headline Tier 1 watchlist since yesterday. Anchor trials:

**Beta-cell / cell therapy**
- **NCT06832410** — Vertex VX-880 (zimislecel) Phase 3 in T1D + kidney transplant (enroll 10)
- **NCT04786262** — Vertex VX-880 (zimislecel) Phase 3 in T1D (enroll 52)
- NCT05791201 — Vertex VX-264 Phase 1/2 (status: ACTIVE_NOT_RECRUITING; encapsulated islets, enroll 7)

**T1D immunotherapy**
- NCT07088068 — Sanofi teplizumab vs placebo (enroll 723; ages 1–25)
- Lilly baricitinib pediatric β-cell preservation trials remain in watch list

**T2D novel therapies (largest Phase 3 enrollments)**
- **NCT07064473** — Boehringer Ingelheim vicadrostat + empagliflozin (enroll 11,800)
- NCT07481747 — Hudson Biotech tirzepatide vs placebo (enroll 2,539)
- NCT07351058 — Roche enicepatide RO7795068 in obesity/T2D (enroll 1,600)
- NCT07400653 — Pfizer PF-08653944 in obesity/T2D (enroll 999)
- NCT07088068 — Sanofi teplizumab (cross-listed above)
- NCT06082063 — Steno multifactorial CV intervention in T1D (Aspirin + semaglutide + sotagliflozin; enroll 2,000)
- NCT07076199 — Novo Nordisk weekly insulin icodec in T1D (enroll 877)

**Sponsor concentration**
- Eli Lilly: 27 trials | Novo Nordisk: 26 | Vertex: 3 | **Sana Biotechnology: 0 in tracked dataset** (recurring flag — manual ClinicalTrials.gov search recommended; carried from yesterday)

### Week-over-week changes (2026-05-19 → 2026-05-26)

- **5 new trials** (small additions, all early-stage)
- **3 status changes** (all administrative — no Phase 3 results conversions)
- **0 new results posted**
- **4 trials removed** from query result set (likely withdrawn or recategorized; worth a sample-check)

**New trials this week**

| NCT | Phase / Status | Sponsor | Title |
|-----|----------------|---------|-------|
| NCT07599982 | NA / Not Yet Recruiting | DreaMed Diabetes | Safety Eval of MODI insulin titration algorithm |
| NCT07595289 | NA / Not Yet Recruiting | Third Xiangya Hospital | DP-DCT 1.0 — Dapagliflozin + CGM vs SMBG |
| NCT07604922 | NA / Not Yet Recruiting | INSERM (France) | HEMI/SPG vascular signal study |
| NCT07602036 | NA / Not Yet Recruiting | Poznan U. Med. Sci. | T2D and pregnancy single-arm interventional |
| NCT03919877 | NA / Completed | Stanford | Precision Diets for Diabetes Prevention (results posted 2026-05-22) |

**Status changes**

- **NCT07372872** — "MyGlucoCare" smartphone app for gestational diabetes: NOT_YET_RECRUITING → **RECRUITING** (positive — new enrollment)
- NCT06467955 (MagDI Canada): RECRUITING → ACTIVE_NOT_RECRUITING
- NCT06073457 (MGI/MGJ magnetic gastro-ileal diversion): RECRUITING → ACTIVE_NOT_RECRUITING

### Recently posted results (last 30 days, ranked by date — for review queue)

| NCT | Posted | Phase | Sponsor | Topic |
|-----|--------|-------|---------|-------|
| NCT03919877 | 2026-05-22 | NA | Stanford | Precision Diets for Diabetes Prevention |
| NCT05514535 | 2026-05-11 | **PHASE3** | **Novo Nordisk** | Semaglutide + lower-dose insulin glargine vs higher-dose glargine |
| NCT05823948 | 2026-04-30 | **PHASE3** | **Novo Nordisk** | Insulin icodec + Flash Glucose Measurements in T2D not at goal |
| NCT05649137 | 2026-04-27 | **PHASE3** | **Novo Nordisk** | Semaglutide in excess weight + T2D weight loss |
| NCT05454891 | 2026-05-12 | NA | UCSF | Extended bolus for meals in closed-loop |
| (11 additional NA / Phase 2 NIH and academic results — see clinical_trials_latest.json) |

→ Three Novo Nordisk Phase 3 result postings cluster around the **insulin icodec / weekly basal franchise** — these align directly with the March 2026 Awiqli FDA approval. Worth a focused synthesis if any are not yet in the tracker.

---

## PubMed Highlights

**Unique papers in 30-day window:** 158 (vs. 158 in 2026-05-19 snapshot — flat headline count; 101 new PMIDs, 87 dropped)

### Domain volume (week-over-week deltas)

| Domain | Last week | Today | Δ | % |
|--------|----------:|------:|---:|--:|
| Diabetes AI/ML | 208 | **233** | +25 | +12% |
| Diabetes Biomarker | 149 | **170** | +21 | +14% |
| T2D GLP-1 New | 147 | 136 | −11 | −7% |
| T2D Remission | 62 | 71 | +9 | +15% |
| Diabetes Microbiome | 121 | 127 | +6 | +5% |
| Diabetes Health Equity | 56 | 62 | +6 | +11% |
| **Closed Loop AP** | **16** | **23** | **+7** | **+44%** |
| **LADA New Research** | **4** | **7** | **+3** | **+75%** |
| Diabetes Epigenetics | 7 | 9 | +2 | +29% |
| Diabetes Complications | 37 | 41 | +4 | +11% |
| T1D Immunotherapy | 23 | 19 | −4 | −17% |

> **Worth flagging:** Closed Loop AP and LADA both moved >40% week-over-week. Absolute numbers are small (small-base effect) but LADA is a Tier 2 contribution area where every new paper matters; queue a manual scan of the 3 new LADA PMIDs.

### Cross-domain papers (today's snapshot)

The hub-monitor diff identified **5 new cross-domain PubMed papers** between yesterday and today (highest-value targets):

| PMID | Domains | Title (truncated) |
|------|---------|-------------------|
| **42181212** | Diabetes AI/ML × Diabetes Microbiome | Therapeutic targets for diabetic nephropathy via druggable genome Mendelian randomization — role of gut microbiota |
| **42181960** | Diabetes AI/ML × Diabetes Multi-Omics | Molecular basis of precision nutrition: food components, microbiome-derived metabolites, multi-omics modeling |
| **42184024** | Diabetes AI/ML × Diabetes Biomarker | Quantum dot–based fluorescent biosensors for enzyme detection — applications in disease |
| **42184924** | Diabetes AI/ML × Diabetes Multi-Omics | Targeting dysregulated glycolysis in T2D osteoporosis — calcifediol validation |
| **42185046** | T2D GLP-1 New × Diabetes Gene Therapy | Impact of incretin analogues on lipid and lipoprotein metabolism in obesity and diabetes |

**Relevance to Research Doctrine Tier 1 contribution areas:**

- **42181212** intersects Tier 1 #1 (Multi-Omics Biomarker Integration) and Tier 2 #7 (Microbiome) — direct fit for the microbiome-metabolic pathway database project. **Highest review priority today.**
- **42181960** intersects Tier 1 #1 (Multi-Omics) and Tier 2 #7 (Microbiome) — review for inclusion in microbiome ML feature catalog.
- **42184924** intersects Tier 1 #1 (Multi-Omics) and Tier 1 #5 (AI/ML prediction) — review for biomarker pipeline.

### Full cross-domain set in current 30-day window (14 papers)

The latest `pubmed_recent_latest.json` contains 14 papers that hit ≥2 alert domains. Beyond today's 5 above, noteworthy carry-overs include:
- **PMID 42138080** — "New and emerging therapies in T1D" (T1D Immuno × teplizumab) in J Clin Invest, May 15 — a likely review-of-the-field paper deserving citation in the T1D portfolio.
- **PMID 42138126** — "US Patterns in Islet Autoantibody Ordering after Teplizumab Approval" — relevant to the Tzield rollout / equity narrative.
- **PMID 42163482** — "Extracellular Vesicle Proteins as T1D Predictive Biomarkers" (T1D Stem Cell × T1D Immuno × teplizumab) in Proteomics — directly relevant to Tier 1 #1.

### Key-therapy hit changes (week-over-week)

| Therapy | Last week | Today | Δ |
|---------|----------:|------:|--:|
| zimislecel | 0 | 0 | 0 |
| orforglipron | 3 | 3 | 0 |
| retatrutide | 4 | 5 | +1 |
| **CagriSema** | 2 | 4 | **+2** |
| baricitinib | 2 | 3 | +1 |
| teplizumab | 5 | 5 | 0 |
| **icodec** | 3 | 5 | **+2** |
| dapagliflozin | 5 | 5 | 0 |

→ CagriSema and icodec each picked up two new papers — consistent with the Novo Nordisk Phase 3 results pulses noted in the trials section.
→ **zimislecel remains at 0 PubMed hits in 30-day window** despite ongoing Vertex Phase 3 trials — likely a keyword issue (papers may use "stem cell-derived islet" or "VX-880" instead). Recommend adding "VX-880" as an alternate query term in `baseline_pubmed_alerts.py`.

---

## Gap Analysis Summary

The gap report from 2026-05-25 is fresh, but the underlying `literature_gap_data.json` is **36 days old** — the rankings below reflect the April 20 PubMed query, not current literature.

### Top 5 under-researched intersections (gap score 100, multiple ties)

| Rank | Intersection | Joint Pubs | Rationale |
|------|--------------|-----------:|-----------|
| 1 | **Beta Cell Regen × Health Equity** | 0 | Regenerative therapies must address access; equity analysis of emerging cell therapies absent. |
| 2 | **Insulin Resistance × Islet Transplant** | 1 | IR in islet-transplant recipients affects graft survival but is barely studied. |
| 3 | **Islet Transplant × Drug Repurposing** | 0 | Existing immunosuppressants could be repurposed for islet protection; computational screen unapplied. |
| 4 | **Islet Transplant × Health Equity** | 0 | Islet transplant available only at select centers; access equity research absent. |
| 5 | **Gene Therapy × LADA** | 0 | LADA's autoimmune mechanism is a candidate for gene therapy; no crossover work exists. |

### Alignment with Tier 1 contribution areas

Of the top 15 gaps in the May 25 report, the strongest matches for our Tier 1 capabilities are:

- **#3 Islet Transplant × Drug Repurposing** → directly fits Tier 1 #4 (Drug Repurposing Computational Screening). The existing `islet_repurposing_drug_candidates.json` (52d stale) was built for the broader islet protection question and likely contains relevant candidates. **Recommendation:** re-run the islet repurposing pipeline and explicitly filter for immunosuppressant repositioning candidates relevant to graft survival.
- **#1, #4, #7, #9, #12, #14 (Health Equity intersections)** → Tier 1 #6 (Epidemiological Data Analysis) and Tier 2 #12 (Technology Accessibility). The recurring "Health Equity × [advanced therapy]" pattern argues for one consolidated equity-of-access synthesis covering: stem cell therapy, CAR-Treg, glucokinase activators, drug repurposing, and LADA diagnosis.
- **#5, #10, #11, #13, #14 (LADA intersections)** → Tier 2 #11 (Subtype Misdiagnosis). The +75% LADA publication-volume jump this week is a small but suggestive signal — even three new papers in this small field could refresh the synthesis case.

---

## Breaking News (web check, last 7 days)

Limited net-new since yesterday's report:

- **MannKind Afrezza pediatric PDUFA date: May 29, 2026** (3 days from today). Phase 3 INHALE-1 missed primary HbA1c noninferiority in full ITT but met it in modified ITT (one protocol-noncompliant patient excluded). FDA approval would make this the first needle-free insulin option for pediatric T1D/T2D. *Source: Drugs.com new approvals tracker, Cardiology Advisor PDUFA roundup.*
- **Eli Lilly retatrutide Phase 3 TRIUMPH-1 (May 21)** — 28% weight loss at 80 weeks across pooled doses; TRIUMPH-2 (T2D) and TRIUMPH-3 (CVD) expected later this year. (Carried from yesterday — already in tracker discussion; verify NCT05929079 / NCT06260722 / NCT06297603 entries are current.)
- **Vertex zimislecel** — no fresh announcement in last 7 days. Pivotal Phase 3 enrollment is ongoing per earlier 2026 disclosures; next major catalyst is ADA Scientific Sessions (typically late June).
- **CagriSema** — no new FDA action reported; remains "working toward 2026 approval" per Novo Nordisk. The two new PubMed hits this week are clinical-literature, not regulatory.
- **No FDA approval actions, advisory committee meetings, or Phase 3 readouts in the diabetes space have surfaced in the last 24 hours.**

---

## Recommended Actions (priority order)

1. **THIS FRIDAY (May 29):** Watch for MannKind Afrezza pediatric PDUFA decision. Add a manual tracker entry the moment the decision is announced, regardless of direction.
2. **Re-run stale pipelines today or tomorrow.** Run, in order:
   - `python project1_literature_gap_analysis.py` (will refresh `literature_gap_data.json` + `literature_gap_matrix.xlsx`; 36 days stale)
   - The islet repurposing pipeline (52 days stale — `islet_repurposing_targets.json` and `islet_repurposing_drug_candidates.json`)
   - The microbiome ML pipeline (51 days stale)
3. **Review the 5 new cross-domain PMIDs today** — especially **42181212** (microbiome × AI/ML × diabetic nephropathy, fits Tier 1 #1) and **42181960** (precision nutrition multi-omics, fits Tier 1 #1). Add to `extracted_corpus_data.json` workflow.
4. **Add "VX-880" as an explicit alternate query term** in `baseline_pubmed_alerts.py` — zimislecel remains stuck at 0 hits in the 30-day window, almost certainly a keyword-coverage issue rather than absence of literature.
5. **Manual ClinicalTrials.gov check for Sana Biotechnology trials.** Recurring zero-result issue across the last several monitor reports — confirm whether Sana has no active diabetes trials or whether the query terms miss them.
6. **Quick scan of the 3 new LADA papers** and the 7 new Closed-Loop AP papers — both domains spiked >40% week-over-week and the LADA domain is a Tier 2 priority where new signal is rare.
7. **Synthesis opportunity:** Consider building a one-page "Health Equity × Advanced Diabetes Therapy" framing piece that bundles top-ranked gap intersections #1, #4, #7, #9, #12, #14. Six of the top 15 gap intersections share this pattern — it's an unusually concentrated signal in the gap report.

---

## Validation & Caveats

- **Web-search items** are BRONZE (single source, press-release-tier reporting). PDUFA dates and Phase 3 readouts should be reconfirmed against Drugs.com / company IR pages before being entered as fact in the tracker.
- **Gap rankings** reflect April 20 PubMed queries; today's high week-over-week movements in Closed Loop AP and LADA are not yet reflected in `literature_gap_data.json` (one reason to refresh).
- **Cross-domain paper identification** relies on the alert-domain query system in `baseline_pubmed_alerts.py`. Papers may genuinely span more domains than the query catches — manual review is the gold-standard verification step.
- No files were modified during this run (review-only).

---

*Generated by Diabetes Hub Monitor — automated daily review pass*
*Next scheduled run: 2026-05-27 ~07:00*
