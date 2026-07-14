# Diabetes Research Hub — Monitor Report

**Run date:** 2026-07-14 (automated monitor)
**Data as of:** clinical_trials_latest.json & pubmed_recent_latest.json generated 2026-07-14 02:05
**Bottom line:** Two new trials appeared (net 855→857). The one worth your attention is a **Bayer combination trial (finerenone + empagliflozin in CKD + T2D) that posted results 2026-07-13** — a live Tier 1 #3 combination-mapping input. One Lilly Phase 3 flipped RECRUITING→ACTIVE_NOT_RECRUITING. PubMed churned +42/−41 with 4 new cross-domain papers. Only genuinely new external item: **Foundayo (orforglipron) FDA approval, 2026-07-01** — first oral GLP-1 pill (obesity indication). Gap set unchanged, still BRONZE.

---

## File System Status

All pipeline outputs present and fresh. [Certain] — verified file mtimes directly.

| File | Last generated | Age | Status |
|------|----------------|-----|--------|
| clinical_trials_latest.json | 2026-07-14 02:05 | today | Fresh |
| pubmed_recent_latest.json | 2026-07-14 02:05 | today | Fresh |
| hub_monitor_report.md | 2026-07-14 02:14 | today | Fresh |
| literature_gap_report.md | 2026-07-13 03:13 | 1 day | Fresh |
| literature_gap_data.json | 2026-07-10 02:17 | **4 days** | Aging — re-run this week |

Daily snapshots for clinical trials and PubMed exist through 2026-07-14. No missing critical files. hub_monitor.py flags 817 result files >14 days old — these are historical daily snapshots and agent_state backups, expected, not a problem.

---

## Clinical Trial Changes (07-13 → 07-14)

Total tracked: **857 trials** (was 855). Category counts: T1D Cure & Cell Therapy 152 · T1D Immunotherapy & Prevention 76 · T2D Novel Therapies 147 · Diabetes Technology 237 · Recently Completed w/ Results 319.

- New trials: **2**
- Removed trials: **0**
- Status changes: **1**
- Newly posted results on existing trials: **0**

### New trials

| NCT | Sponsor | Phase / Status | Focus |
|-----|---------|----------------|-------|
| **NCT05254002** | Bayer | Phase 2 / **COMPLETED, results posted 2026-07-13** | Finerenone + empagliflozin **combination** vs each alone, CKD + T2D |
| NCT07699380 | U. of Washington | Phase 2 / RECRUITING | MetMod-T1D — metabolic modulation to enhance insulin sensitivity & mitochondrial function in T1D |

**NCT05254002 is the actionable one.** A head-to-head of a combination (finerenone + empagliflozin) against each monotherapy, with results already posted, is exactly the cross-mechanism combination signal Tier 1 #3 (Clinical Trial Intelligence) exists to catch. Both agents have independent CV/renal outcome pedigrees; the combination arm is the value.

### Status change

- **NCT07215312 (Eli Lilly, LY3938577)** — RECRUITING → **ACTIVE_NOT_RECRUITING**. T2D previously treated with basal insulin. Enrollment closed; watch for topline in a future cycle. [Certain] — confirmed by snapshot diff.

### Phase 3 RECRUITING watchlist (42 active; key-org programs)

| NCT | Sponsor | Therapy / focus |
|-----|---------|-----------------|
| NCT04786262 | Vertex | VX-880 (zimislecel) islet cell therapy, T1D |
| NCT06832410 | Vertex | VX-880 efficacy/safety, T1D |
| NCT07222137 | Eli Lilly | Baricitinib — delay Stage 3 T1D |
| NCT07222332 | Eli Lilly | Baricitinib — preserve beta-cell function (peds) |
| NCT06739122 | Eli Lilly | Dulaglutide 3.0/4.5 mg, pediatric T2D |
| NCT07076199 | Novo Nordisk | Insulin icodec, T1D |
| NCT07564414 | Novo Nordisk | CagriSema, T2D |
| NCT06334133 | vTv Therapeutics | Cadisegliatin (glucokinase activator), T1D adjunct |

No Sana Biotechnology trials present in the current pull. [Certain] — filtered sponsor field, zero matches.

### Recently posted results worth a look (last ~12 days)

- **NCT05254002 (Bayer)** — finerenone + empagliflozin combination, posted **07-13** *(new this cycle; see above)*.
- **NCT04255433 (Eli Lilly)** — Tirzepatide vs Dulaglutide, posted **07-08**. Phase 3, key-org — feed the cross-trial combination map.
- **NCT03263494 (Jaeb)** — CGM in teens/young adults w/ T1D, posted 07-09.
- **NCT06340854 (Novo Nordisk)** — daily basal → weekly insulin switch, posted 07-02.

---

## PubMed Highlights (07-13 → 07-14)

Corpus: **159 unique papers** across 16 alert domains, 30-day lookback. Churn this cycle: **+42 new / −41 dropped** (rolling window — high churn is normal at the 30-day boundary, not a surge).

### New cross-domain papers today (highest priority — 4)

- **[42439827]** Stem cell-derived islets & emerging experimental platforms — *T1D Stem Cell Cure + Diabetes Multi-Omics*
- **[42440498]** Urinary proteomics + metabolomics biomarkers for T2D nephropathy — *Diabetes Biomarker + Complications* (maps to Tier 1 #1 multi-omics)
- **[42440805]** Glycogen dysfunction in T2DM + MASLD, α-hydroxybutyrate → GYS2 — *Biomarker + Multi-Omics*
- **[42443264]** Gut microbiome signatures ↔ DNA-methylation biological aging — *AI/ML + Biomarker*

### Strongest cross-domain signal in the current corpus

- **[42419792]** Comparative effects of obesity drugs — spans **orforglipron + retatrutide + CagriSema** (triple key-therapy overlap; strongest standing signal, carried from prior cycles).
- **[42394981]** Incretin-based therapies in T2D — orforglipron + retatrutide.
- **[42332392]** Teplizumab (Tzield) for T1D delay — T1D Immunotherapy + teplizumab.

### Key-therapy tracker (papers in 30-day window)

orforglipron 5 · CagriSema 5 · dapagliflozin 5 · retatrutide 4 · teplizumab 4 · icodec 3 · baricitinib 2 · **zimislecel 0**.

zimislecel remains at zero despite two active Vertex Phase 3 trials — a persistent literature/trial mismatch worth noting (publications lag the program). [Likely] this is timing, not absence of activity.

---

## Gap Analysis Summary (literature_gap_report.md, 2026-07-13)

Validation level **BRONZE** per Research Doctrine (single analytical source; needs expert confirmation). Top under-researched intersections (Gap Score 100 = zero/near-zero joint publications) — **unchanged from last cycle**:

1. **Beta Cell Regen × Health Equity** (0 joint) — equity of access to regenerative therapies absent
2. **Insulin Resistance × Islet Transplant** (1 joint) — affects graft survival, barely studied
3. **Islet Transplant × Drug Repurposing** (0 joint) — immunosuppressant repurposing for islet protection unexplored
4. **Islet Transplant × Health Equity** (0 joint) — access equity at select centers absent
5. **Gene Therapy × LADA** (0 joint) — no crossover despite autoimmune mechanism

**Tier 1 alignment (RESEARCH_DOCTRINE.md):** these map onto Tier 1 #2 (Literature Synthesis & Gap Analysis), #3 (Clinical Trial Intelligence), #4 (Drug Repurposing Computational Screening), and #6 (Health-Equity). Gaps #1, #3, #4 are actionable computational targets we are positioned to fill. Today's cross-domain biomarker papers ([42440498], [42440805]) reinforce Tier 1 #1 (Multi-Omics Biomarker Integration).

---

## Breaking News (web check, last 7 days)

One genuinely recent item; the Phase 3 headlines are all June/ADA 2026 and already in the hub.

- **Foundayo (orforglipron) — FDA approval 2026-07-01.** First **oral** GLP-1 pill, approved for obesity/overweight-with-comorbidity (weight management indication, not yet a standalone T2D label). New vs. prior reports; orforglipron was tracked in trials/PubMed but this specific approval is fresh. [Certain]
- **Atacicept (Trutakna) — FDA accelerated approval 2026-07-07** for IgA nephropathy. Not a diabetes drug, but DKD-adjacent (kidney complications). Minor flag. [Certain]
- Already-captured June/ADA items (no action): retatrutide Phase 3 topline (06-06), orforglipron ACHIEVE-2/-4, teplizumab pediatric Stage 3 approval (06-12), first generic dapagliflozin (04-07).

No Phase 3 topline, major publication, or diabetes-specific FDA action in the strict **07-07 → 07-14** window beyond the above. [Likely] — web-date resolution is coarse; nothing surfaced that the trial/PubMed pipelines missed.

---

## Recommended Actions

1. **Log NCT05254002 (Bayer finerenone + empagliflozin combination, results 07-13)** into the cross-trial combination map — Tier 1 #3. This is the single highest-value new item this cycle.
2. **Re-run gap analysis** — `python project1_literature_gap_analysis.py`. literature_gap_data.json is 4 days old (07-10); refresh before any expert-review pass on the BRONZE set.
3. **Tag Foundayo (orforglipron) 07-01 approval** in the therapy/equity tracker — an oral GLP-1 is a cost/access story feeding Tier 1 #6 (Health-Equity) and the recurring affordability thread.
4. **Route new multi-omics biomarker papers [42440498], [42440805]** to the Tier 1 #1 pipeline (T2D nephropathy proteomics/metabolomics; MASLD glycogen axis).
5. **Watch NCT07215312 (Lilly LY3938577)** — now ACTIVE_NOT_RECRUITING; enrollment closed, topline pending.
6. No tracker edits strictly required beyond #1 — trial universe change is +2 with one status flip.

---
*Generated by the automated Diabetes Hub monitor. Read-only review run — no existing files were modified. Evidence levels noted per Research Doctrine; all gap findings remain BRONZE pending expert confirmation.*
