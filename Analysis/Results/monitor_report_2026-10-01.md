# Diabetes Research Hub — Monitor Report
**Run date:** 2026-10-01 (automated Cowork review — no existing files modified)

**Headline:** All five key outputs were regenerated today (12:28–12:30 local clock). Biggest new signals: **Lancet CV-safety paper for orforglipron vs insulin glargine (PMID 42815506, 09-30)**, **Lilly orforglipron Phase 3 results posted (NCT06109311)**, and a **Phase 1 gingiva-derived MSC trial in T1D (PMID 42816465)**. The literature-gap ranking is saturated (22 pairs tied at 100.0) and no longer discriminates.

---

## File System Status

| File | Last modified | Status |
|---|---|---|
| hub_monitor_report.md | 2026-10-01 12:30 | Fresh (scan stamp 07:30; timestamp offset between scripts) |
| clinical_trials_latest.json | 2026-10-01 12:28 | Fresh (906 trials) |
| pubmed_recent_latest.json | 2026-10-01 12:29 | Fresh (168 papers, 17 domains) |
| literature_gap_data.json / literature_gap_report.md | 2026-10-01 12:30 | Fresh (30 domains, 435 pairs) |
| Diabetes_Research_Tracker.xlsx | 2026-07-17 | **STALE — 76 days** |
| .~lock.Diabetes_Research_Tracker.xlsx# | 2026-03-15 | Stale lock file (199 d) |

hub_monitor_report.md: 39 new / 165 modified / 0 removed of 1,532 tracked files. The path-separator false-churn seen 09-30 is gone. Real new items: DECISION_BRIEF_2026-10-01_Gap2.md, run_report_2026-10-01.md, gap_tiers.json, structured_effects*.json, verify_fda_approval.py, set_gap_tier.py.
Git: `git status` shows branch main = origin/main at the time of this run (the 2 unpushed commits from 09-30 are gone, but the 10-01 run_report says overnight work was committed locally and NOT pushed — verify with `git log origin/main..`).

## Clinical Trial Changes (906 vs 907 in 09-30 snapshot)
**New (4):** NCT06109311 (Lilly, **Phase 3 COMPLETED**, orforglipron in T2D with inadequate control, N=546, **results posted 2026-10-01**); NCT05120544 (Duke, nurse-delivered care, results); NCT06156696 (Astellas, treatment-support system, results); NCT07849725 (U. Antonio Nariño, eHealth, not yet recruiting).
**Dropped from pull (5, all device/tech):** NCT06272136 (Liom niCGM), NCT06587087, NCT06600776 (URLi on 780G), NCT06621030, NCT06709729 (AndroidAPS). Likely query-window churn; not verified individually.
**Status change (1):** NCT07817251 (Novo, CagriSema, T2D switching tolerability, Ph3, N=210) NOT_YET_RECRUITING → RECRUITING.
**Not reconfirmed:** NCT05757713 (Sanofi teplizumab pediatric Stage 2) flagged missing 09-30 — still needs a manual registry check.

**Phase 3 RECRUITING, tracked orgs (10):** Vertex 2 (NCT04786262, NCT06832410 — VX-880 programs); Lilly 4 (baricitinib NCT07222137/NCT07222332; dulaglutide peds NCT06739122; orforglipron NCT07613307); Novo 4 (CagriSema NCT07817251, NCT07282613, NCT07564414; zenagamtide NCT07797335, N=1,778). Sana: 0. Roche petrelintide Ph3 NCT07843485 (flagged 09-30) is not-yet-recruiting.
**Results posted this month worth review:** NCT06045221 (orforglipron vs semaglutide, N=1,698, 09-15), NCT05872620 (orforglipron obesity+T2D, 09-04), NCT06109311 (orforglipron, 10-01), NCT06370715 (Lilly LY900014, 09-28), NCT05232071 (Inventiva, 09-09).
**Evidence level:** registry-posted results = unreviewed (BRONZE at best). Do not cite until a paper/PMID is verified.
Category counts: T1D Cure & Cell Therapy 155; T1D Immunotherapy & Prevention 78; T2D Novel Therapies 152; Devices 242; Recently Completed with Results 358; Prediction Ledger 1.

## PubMed Highlights (30-day lookback; 168 papers; 18 new vs 09-30)
**Key-therapy papers (new today):**
- **PMID 42815506** — *Lancet* 09-30, cardiovascular safety of orforglipron vs insulin glargine in T2D at elevated CV risk. Peer-reviewed RCT; highest-priority new item. Read abstract, verify PMID and HR before adding to Research_Findings_Summary.md.
- PMID 42594928 — *Lancet Diabetes Endocrinol*, once-weekly IcoSema vs glargine U100 (COMBINE-type trial).
- PMID 42503495 — CagriSema anthropometric targets / cardiometabolic outcomes (DOM).
- PMID 42816465 — **Phase 1** RCT, gingiva-derived MSCs in T1D (*Signal Transduct Target Ther*). Early-phase; evidence level BRONZE/low; relevant to T1D Cure track.
**Cross-domain (≥3 domains; 4 papers, all on incretin/amylin axis):** 42808923 (GI adverse effects of GLP-1/dual agonists; 5 domains), 42803913 (amylin-based agonists; 5), 42812898 (anti-obesity medication scoping review; 5), 42763732 (CagriSema meta-analysis; 3). All are reviews/meta-analyses — useful for synthesis, not new primary evidence. (09-30 report's islet/hypoimmune cross-domain papers are not in today's ≥3 list.)
**Therapy counts (hits in lookback):** dapagliflozin 56, finerenone 49, orforglipron 20, retatrutide 16, icodec 12, teplizumab 10, cagrilintide 8, efsitora 6, CagriSema 5, amycretin 3, petrelintide 3, baricitinib 3, **zimislecel 0** (zero for the 3rd+ consecutive run; consistent with Phase 3 stage).
**Volume:** highest by total_count: T2D GLP-1 (250), AI/ML (242), Microbiome (172), Biomarker (151). Thinnest: Drug Repurposing (3), GLP-1 Pharmacogenomics (3), Epigenetics (8). Note retmax caps papers at 10/domain, so volume is read from total_count, not paper_count.

## Gap Analysis Summary
Top 5 (all score 100.0, ranks 1–5 are ties broken by order): 1) Beta Cell Regen × Health Equity (0 joint pubs); 2) Insulin Resistance × Islet Transplant (1); 3) Islet Transplant × GWAS/Polygenic (0); 4) Islet Transplant × Personalized Nutrition (0); 5) Islet Transplant × Drug Repurposing (0).
**Methodological problem:** 22 of 25 listed pairs are tied at 100.0 and most involve Islet Transplant (254 pubs), Glucokinase (865) or LADA (613) — small domains where the expected-count model overshoots. The score is saturating; rank order within the top ~22 is arbitrary. Treat as BRONZE, keyword-based, single source (PubMed counts). Fix suggestion: report a log-ratio or observed/expected with CI instead of a capped 0–100 score.
**Tier 1 alignment (RESEARCH_DOCTRINE.md):** Drug Repurposing pairs (Islet Transplant, LADA, Health Equity, Glucokinase, CGM, Closed Loop) → Tier 1 #4 (Drug Repurposing Computational Screening). Health Equity / Beta Cell Regen × Health Equity → #2 (Literature Synthesis); note the 10-01 DECISION_BRIEF says Gap #2 is two questions under one number and does not support GOLD — a ruling from you is pending. GWAS/Polygenic × CGM/Closed Loop → #1 (Multi-omics) loosely.

## Breaking News (web, ~7 days)
Search returned headline/URL lists only (no page text), so nothing below is verified beyond the headline:
- Lilly announced EASD 2026 presentations for retatrutide, Foundayo (orforglipron brand) and eloraTZP — sponsor press release; data are Bronze until abstracts/papers are verified.
- Novo CagriSema/zenagamtide ADA 2026 data (June) — older, context only.
- No new FDA diabetes approval for the last 7 days could be confirmed from results. (efsitora and finerenone T1D-CKD actions were logged 09-28/29.)
Sources: [Lilly EASD 2026 press release](https://www.prnewswire.com/news-releases/lilly-to-present-new-data-on-foundayo-retatrutide-and-eloratzp-at-easd-2026-as-it-strives-to-change-the-course-of-cardiometabolic-health-302878341.html), [Lilly EASD coverage (RTTNews)](https://www.rttnews.com/3691098/eli-lilly-to-showcase-retatrutide-foundayo-eloratzp-data-at-easd-2026.aspx), [GLP-1 pipeline 2026 (Drug Discovery News)](https://www.drugdiscoverynews.com/glp-1-agonist-clinical-pipeline-2026-semaglutide-tirzepatide-and-what-s-in-phase-2-17286)

## Recommended Actions
1. **Verify and log PMID 42815506** (orforglipron CV safety, *Lancet*) — pull abstract, confirm HR/CI, then add to Research_Findings_Summary.md with evidence level.
2. **Rule on Gap #2** (DECISION_BRIEF_2026-10-01_Gap2.md) — tier unchanged until you decide.
3. Update Diabetes_Research_Tracker.xlsx (76 d stale): NCT07843485, NCT07845955, NCT06534411, NCT06109311; remove the March `.~lock` file.
4. Review orforglipron results NCT06109311 / NCT06045221 / NCT05872620 once linked publications exist.
5. Manually check NCT05757713 (teplizumab peds) on ClinicalTrials.gov.
6. Fix gap scoring saturation in `project1_literature_gap_analysis.py` (22 ties at 100.0).
7. Confirm push state: `git log origin/main..` ; push if overnight commits are unpushed.
8. No script re-runs needed: all data <1 day old.

---
*Generated by automated Cowork review. Sources: Analysis/Results files, web searches.*
