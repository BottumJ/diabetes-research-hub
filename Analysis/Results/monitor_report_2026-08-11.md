# Diabetes Research Hub — Monitor Report
**Run date:** 2026-08-11 (automated review run)
**Reviewer:** Hub monitor (read-only; no source files modified)

---

## TL;DR — What's Actionable

**Collector outage, day 25. The problem is no longer the outage — it's that five daily reports have flagged it and nothing has been restarted.** Every "latest" data file is still frozen at **2026-07-17**. This is the **fifth consecutive** report raising the identical freeze (08-07 → 08-11). The recommended one-line fix has been repeated for five days without action. If a human is reading these, the signal to act on is not "data is stale" — it's "the automated monitor cannot fix a collector outage on its own, and it has now been waiting 25 days." [Certain — no `clinical_trials_snapshot_*` or `pubmed_recent_snapshot_*` file exists after 2026-07-17; `clinical_trials_latest.json` metadata reads `generated: 2026-07-17T02:05:53`, `pubmed_recent_latest.json` reads `2026-07-17T02:06:39`.]

**Restart the collectors and capture *how* they fail:**

```
python baseline_clinical_trials.py
python baseline_pubmed_alerts.py
python hub_monitor.py
```

Run clean but write no new snapshot → the collector scheduler/cron is disabled (an ops problem, not a code problem). Throw a traceback → capture it; the failure boundary is exactly 2026-07-17, which points at an API/endpoint/auth break. Either way, one manual run tells you which. [Certain — analysis pipeline files carry recent mtimes while the three baseline collectors have not written since 2026-07-17; the fault is isolated to the collectors.]

**Everything below is reference state carried forward from the 2026-07-17 freeze. It has not changed and should not be treated as current intelligence.**

---

## File System Status

| File | Last modified | Age | Status |
|------|--------------|-----|--------|
| `clinical_trials_latest.json` | 2026-07-17 | 25 d | ⚠️ STALE (>14 d) |
| `pubmed_recent_latest.json` | 2026-07-17 | 25 d | ⚠️ STALE (>14 d) |
| `hub_monitor_report.md` | 2026-07-17 | 25 d | ⚠️ STALE (>14 d) |
| `literature_gap_data.json` | 2026-07-18 | 24 d | ⚠️ STALE (>14 d) |
| `literature_gap_report.md` | 2026-08-10 | 1 d | Fresh file — but still re-analyzes frozen 2026-07-17 PubMed data (header: "Date range: 2020/01/01 to 2026/07/17") |
| `agent_state.json` | 2026-08-10 | 1 d | Current (backup rotation still running) |

**Two schedulers, one broken.** The *analysis/iterate* pipeline is alive — `literature_gap_report.md`, `citation_validation.json`, and the `agent_state.json` backup rotation all carry 2026-08-10 mtimes. The *collector* pipeline (`baseline_clinical_trials.py`, `baseline_pubmed_alerts.py`, `hub_monitor.py`) has produced nothing since 2026-07-17. The daily gap report looks fresh but is cosmetic: it re-runs on the cached 2026-07-17 corpus and reproduces identical rankings. Do not mistake a fresh mtime for fresh data. [Certain]

**Latest genuine hub scan (`hub_monitor_report.md`, 2026-07-17):** 1,057 files tracked; 5 new, 33 modified, 0 removed; flagged 827 result files >14 days old. That 827 figure will only grow until the collectors restart.

---

## Clinical Trial Changes

**No new snapshot since 2026-07-17 → nothing new to diff.** The numbers below are the frozen 2026-07-17 state (`clinical_trials_latest.json`, 858 trials), carried for reference only.

Category counts (frozen): T1D Cure & Cell Therapy 152 · T1D Immunotherapy & Prevention 76 · T2D Novel Therapies 147 · Diabetes Technology 236 · Recently Completed w/ Results 321.
Status mix (frozen): 321 COMPLETED · 269 RECRUITING · 151 NOT_YET_RECRUITING · 110 ACTIVE_NOT_RECRUITING · 7 ENROLLING_BY_INVITATION. 52 trials are Phase 3 + RECRUITING.

**Key Phase 3 trials from tracked sponsors (status as of 2026-07-17 — verify live before citing):**

| NCT | Sponsor | Therapy | Status (frozen) |
|-----|---------|---------|-----------------|
| NCT06832410 | Vertex | VX-880 / zimislecel (islet cell) | RECRUITING |
| NCT04786262 | Vertex | VX-880 / zimislecel | RECRUITING |
| NCT07222332 | Eli Lilly | Baricitinib — preserve beta-cell fn (new-onset T1D) | RECRUITING |
| NCT07222137 | Eli Lilly | Baricitinib — delay Stage 3 T1D | RECRUITING |
| NCT07564414 | Novo Nordisk | CagriSema | RECRUITING |
| NCT07076199 | Novo Nordisk | Insulin icodec (weekly) | RECRUITING |
| NCT06739122 | Eli Lilly | Dulaglutide (pediatric) | RECRUITING |

**Last real week of movement (07-10 → 07-17), for reference:** 8 trials added (mostly newly-COMPLETED records with results, plus new device/Phase-2 recruits incl. Gubra GUB-UCN2 first-in-human, NCT07702890), 2 removed, 6 status changes (5 NOT_YET_RECRUITING → RECRUITING; NCT07215312 RECRUITING → ACTIVE_NOT_RECRUITING). 14 trials posted results in the first half of July (incl. Lilly tirzepatide vs dulaglutide NCT04255433, and LY3502970/orforglipron Japanese T2D NCT05086445). **None of this is new — it is the last data the collectors captured before going dark.**

---

## PubMed Highlights

**Frozen at 2026-07-17** (`pubmed_recent_latest.json`: 158 unique papers, 16 domains, 30-day lookback). Carried for reference; no new papers have entered the corpus in 25 days.

Cross-domain papers (highest value) from the frozen set:

- **[42459945]** *Algorithmic discrimination risks in training data — pediatric type 1 diabetes* — spans Diabetes AI/ML × Closed Loop AP × Health Equity (triple-domain — the single most cross-cutting paper in the set).
- **[42458730]** *Multi-omic modelling of BMI response to dietary weight-loss* — Microbiome × Multi-Omics.
- **[42459212]** *Precision nutrition in Asian populations: multi-omics review* — Microbiome × Multi-Omics.
- **[42419792]** *Comparative effects of obesity drugs (systematic review)* — orforglipron × retatrutide × CagriSema (three tracked therapies in one head-to-head).
- **[42453334]** *Noncoding RNAs for diabetes* — Biomarker × LADA.

Key-therapy mentions (frozen 30-day window): dapagliflozin 52 · orforglipron 10 · CagriSema 6 · retatrutide 4 · teplizumab 4 · icodec 3 · baricitinib 2 · **zimislecel 0**. The zero for zimislecel is expected (cell therapy, sparse literature) but worth watching given the manufacturing news below.

---

## Gap Analysis Summary

Top intersections from `literature_gap_report.md` (regenerated 2026-08-10 but on the frozen 2026-07-17 corpus — **validation level BRONZE**, single analytical source, expert confirmation required):

1. Treg / CAR-T × Neuropathy — 100.0 (0 joint pubs)
2. Beta Cell Regen × Health Equity — 100.0 (0)
3. Treg / CAR-T × Health Equity — 100.0 (0)
4. Glucokinase × Health Equity — 100.0 (0)
5. Gene Therapy × LADA — 100.0 (0)

**Alignment with Tier 1 doctrine areas:** Health Equity (Doctrine Tier 1 #6) sits in four of the top seven gaps (#2, #3, #4, and Drug Repurposing × Health Equity #6). Drug Repurposing is itself Tier 1 #4, so **Drug Repurposing × Health Equity is a double-Tier-1 intersection** and the strongest candidate for a computational contribution. Multi-Omics (Tier 1 #1) surfaces in the unclassified tier via Metabolomics × Health Equity (87.1) and Proteomics × Closed Loop (86.9). Caveat per doctrine: 100.0 gap scores with 0 joint pubs are as likely to be terminology artifacts as real gaps — each needs a manual combined-term PubMed search before it earns Silver.

---

## Breaking News (web check, last ~7 days)

Most 2026 diabetes headlines still trace to ADA Scientific Sessions (June 2026) and are already reflected in the tracker; skipped as routine. One item is genuinely significant and maps to a tracked therapy:

- **Vertex has temporarily postponed completion of dosing in the zimislecel (VX-880) Phase 1/2/3 program pending an internal manufacturing analysis.** [Likely — reported via secondary coverage, not yet confirmed against a Vertex primary release]. This directly affects the two Phase 3 trials the tracker lists as RECRUITING (NCT06832410, NCT04786262). If confirmed, their frozen "RECRUITING" status is likely already outdated — a concrete reason the 25-day trial-data freeze is not harmless. **Verify against Vertex investor relations before acting.**

No new FDA diabetes approval in the last 7 days. Most recent was Garzulys (insulin aspart-fsan biosimilar), approved 2026-07-24 — routine. Orforglipron and zimislecel FDA decisions are both tracked for late 2026 / 2027.

---

## Recommended Actions

1. **[Escalated — 5th day] Restart the three collectors manually and capture the failure mode.** `python baseline_clinical_trials.py && python baseline_pubmed_alerts.py && python hub_monitor.py`. This is the only action that moves anything; every downstream report is blocked on it.
2. **Check the collector scheduler/cron separately from the analysis scheduler.** The analysis pipeline runs daily; the collectors do not. The fault is in the collector job, not the codebase generally — look there first.
3. **Verify the zimislecel dosing-postponement report** against Vertex IR, then flag NCT06832410 / NCT04786262 in the tracker for status re-check once collectors are live.
4. **Do not act on the gap rankings yet.** They are BRONZE and computed on a 25-day-old corpus; refreshing the PubMed collector may change them. Re-run `project1_literature_gap_analysis.py` *after* the collectors restart, not before.
5. **If the collectors cannot be restored soon,** consider pausing this daily monitor or switching it to weekly — five identical reports add noise without adding signal, and a stale-data warning loses urgency when repeated unchanged.

---

*Automated review run — read-only. No source files were modified. Web claims labeled [Likely] require primary-source confirmation. Gap classifications are BRONZE pending expert validation per Research Doctrine v1.0.*
