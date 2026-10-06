# Science Arm Build Charter
### Molding the Diabetes Research Hub from surveillance into a learning science engine

**Status:** Draft v0.1 — owner's working document (not a scheduled task)
**Created:** 2026-06-23
**Companion docs:** `RESEARCH_DOCTRINE.md` (evidence standards), `CONTRIBUTION_STRATEGY.md` (distribution), `OSF_PREREGISTRATION.md` (pre-registration practice)
**One-line purpose:** Keep the breadth — knowing what exists, collecting it, making it available — and add the depth: a closed-loop science arm that commits to falsifiable claims, gets scored against reality, and learns. Both in service of better understanding and working toward a diabetes cure.

---

## 0. The dual mandate (don't trade one for the other)

This hub does two jobs, and the goal is to make them feed each other — not to replace surveillance with science.

| Arm | Job | State today |
|-----|-----|-------------|
| **Surveillance** | Know what exists, collect it, make it available | Built and working — daily trials + PubMed pulls, paper library, dashboards, gap matrix |
| **Science** | Commit, test, score, update — produce defensible new claims | Hollow — the layer that should do this (extraction → analysis) currently emits noise |

The integration point that unifies them: **the same monitor that does surveillance is what scores the science arm's predictions.** Collecting trial readouts daily (surveillance) is exactly the signal needed to grade a prediction made months earlier (science). Build the loop so intake and learning are one system, not two.

---

## 1. Diagnosis — why this is needed (preserve this; it's the reason)

What exists today is a **surveillance and bookkeeping system**, not a science arm. It ingests, catalogs, counts, and re-renders. It accumulates — and accumulation is not learning. A system only learns if being *wrong* changes it, and nothing in the current loop can be wrong.

Hard evidence for this claim, found 2026-06-23:
- **The extractor emits noise.** `extracted_corpus_data.json` holds 490 regex-captured fragments, not structured effect sizes. Example: under `hba1c_change`, trial NCT/PMID 31618560 contributed values `[61, 17]` — that's a demographic table row ("% with private insurance"), not an HbA1c change. A meta-analysis built on this would produce a confident, wrong forest plot. **[Certain — records inspected.]**
- **The gap matrix measures absence, not opportunity.** Gap Score = how few co-publications exist relative to expectation. That flags *terminology gaps and methodologically-distinct pairs* as readily as real openings. It is a starting question, not a finding. **[Certain — by the formula in `literature_gap_report.md`.]**
- **The "vetting" loop is hygiene, not hypothesis.** `agent_state.json` tracks which papers are PMID-verified and which paths are checked. Useful, but it never commits to a prediction and never gets graded. **[Certain — per `diabetes-research-iterate` SKILL.]**

None of this is a criticism of the build quality — the surveillance arm is genuinely strong. It's a statement of what's missing: the commitment-and-scoring half.

---

## 2. Target architecture — the closed loop

The defining property of a science arm: **it commits to falsifiable claims in advance and is scored against outcomes it did not yet know.** Bend the current open pipeline into a loop:

```
   Evidence base  →  Commit  →  Test  →  Score
   (structured)     (dated     (vs      (Brier,
        ↑            claim)    readout)  calibration)
        └──────  Update beliefs + doctrine  ←──────┘
```

- **Surveillance arm** = everything left of and including "Evidence base" (intake, catalog, structured extraction, availability).
- **Science arm** = Commit → Test → Score → Update.
- They share the monitor: surveillance catches the readout; the science arm uses it to grade itself.

---

## 3. Build sequence (phased; each phase has a definition of done)

Ordered by dependency. Do not skip Phase 1 — everything downstream stands on it.

### Phase 1 — Fix the evidence substrate *(prerequisite)*
**Mold:** rebuild the extractor that feeds `extracted_corpus_data.json`.
- Replace regex capture with structured extraction: each record = `{intervention, comparator, population, outcome, effect, effect_type, ci_low, ci_high, n_arm, timepoint, pmid, source_span}`.
- Schema-validate on write; reject records missing effect or variance.
- Add a `verification` field: second-pass confirmation (independent re-extraction or human check) before a record is poolable.
**Done when:** ≥1 outcome cluster (e.g., HbA1c change in a defined trial set) has ≥5 clean, schema-valid, verified records.
**Evidence gate:** records are BRONZE until second-pass verified → SILVER.

### Phase 2 — Hypothesis ledger *(mold the gap matrix)*
**Mold:** convert gap-matrix entries from "co-publication counts" into falsifiable claims.
- Each claim: a statement, current evidence level, supporting PMIDs, contradicting PMIDs, and **the specific test that would promote it** Bronze→Silver→Gold.
- Seed from the curated 15 priority gaps already in `build_gap_synthesis.py`, plus Tier-1 areas in `RESEARCH_DOCTRINE.md`.
**Done when:** the gap dashboards render claims with promotion criteria, not just scores.

### Phase 3 — Prediction ledger *(the move that creates learning — see §4)*
**Mold:** ride the existing daily monitor to score dated predictions on tracked trials.
**Done when:** ≥3 pre-registered predictions exist with lock dates, and the monitor auto-flags when their trials post results.

### Phase 4 — First real pooled estimate
**Mold:** use Phase-1 clean data to run one true meta-analysis (random-effects, I² heterogeneity, sensitivity + risk-of-bias notes). Candidate question: **HbA1c reduction across new incretin Phase-3 RCTs** (most published, most comparable; likely a network meta-analysis given mixed comparators).
**Done when:** a forest plot + heterogeneity report exists, labeled SILVER (single-analyst extraction), with the path to GOLD stated.

### Phase 5 — Versioned, self-updating doctrine
**Mold:** add a changelog to `RESEARCH_DOCTRINE.md` that records *when a standard changed because a prediction or claim failed*, tied to calibration results from §4 of the prediction ledger.
**Done when:** the doctrine has at least one entry traceable to a scored outcome.

---

## 4. The wedge — Prediction Ledger spec (start here)

Smallest change that closes the loop. One file, no new ingestion. Rides `diabetes-data-pull` / `diabetes-hub-monitor`, which already catch `results_posted` daily.

### 4.1 Schema (`Analysis/Results/prediction_ledger.json`)
```json
{
  "prediction_id": "PRED-2026-001",
  "nct_id": "NCT04786262",
  "claim": "Trial meets its primary endpoint at primary analysis.",
  "outcome_metric": "primary endpoint met (Y/N)",
  "point_estimate": "string or number",
  "estimate_range": "e.g. 90% CI on the effect, if numeric",
  "probability": 0.00,                 // analyst probability the claim is TRUE
  "confidence_label": "Certain | Likely | Guessing",
  "reasoning": "why — mechanism, prior trials, base rates",
  "evidence_level_at_prediction": "BRONZE | SILVER | GOLD",
  "locked_date": "YYYY-MM-DD",         // before any readout — pre-registration
  "expected_readout": "YYYY-Qn",
  "resolution": null,                  // filled by monitor: TRUE | FALSE | PARTIAL
  "resolved_date": null,
  "brier_component": null              // (probability - outcome)^2, computed at resolution
}
```

### 4.2 Scoring
- On resolution, `brier_component = (probability − outcome)²` where outcome ∈ {1,0}.
- Track the running mean Brier score and a calibration curve (predicted prob vs observed frequency) across all resolved predictions. Lower Brier = better; calibration curve shows over/under-confidence.
- Feed systematic miscalibration back into the doctrine (Phase 5).

### 4.3 Three seeded predictions (illustrative priors — review and lock before they count)
> These are the analyst's reasoned priors as of 2026-06-23, **not** locked. Confirm expected readout dates and refine probabilities before pre-registering. All are forecasts, explicitly uncertain — they exist to make the system capable of being wrong, which is the point.

**PRED-2026-001 — Vertex VX-880 / zimislecel (NCT04786262, Phase 3, T1D islet cell therapy)**
- Claim: meets primary endpoint (insulin independence / severe-hypo elimination) at primary analysis.
- Probability TRUE: **0.70** · Confidence: **[Likely]**
- Reasoning: strong early-phase insulin-independence signals in prior VX-880 data; main risks are durability, immunosuppression burden, and enrollment scale, not mechanism. Prior probability for a Phase-3 in a program with positive Phase-1/2 is favorable but far from certain.

**PRED-2026-002 — Eli Lilly baricitinib (NCT07222137, Phase 3, delay of Stage 3 T1D)**
- Claim: meets primary endpoint (delay/prevention of progression to Stage 3).
- Probability TRUE: **0.45** · Confidence: **[Guessing → Likely after lit pull]**
- Reasoning: baricitinib (JAK inhibitor) preserved C-peptide in the BANDIT Phase-2 (new-onset T1D), but *delaying clinical onset in at-risk individuals* is a harder, different endpoint than preserving function post-diagnosis. Genuine uncertainty; needs the BANDIT effect sizes pulled before locking.

**PRED-2026-003 — Novo Nordisk CagriSema (NCT07564414, Phase 3 dose-ranging, T2D)**
- Claim: top dose achieves HbA1c reduction non-inferior or superior to semaglutide comparator.
- Probability TRUE: **0.80** · Confidence: **[Likely]**
- Reasoning: cagrilintide + semaglutide combination has shown additive metabolic effect across REDEFINE/earlier programs; the open question is the benefit-vs-tolerability tradeoff at higher doses, not whether glycemic efficacy clears the bar.

*(Effect ranges intentionally omitted until Phase-1 clean extraction exists — per the doctrine, don't state precision the data can't support.)*

---

## 5. Governance — keep it honest

- **Evidence levels on everything.** Bronze (single source) → Silver (independently confirmed / clean single-analyst pooled) → Gold (triangulated, replicated). Carry the level on every claim and prediction.
- **Pre-registration prevents hindsight.** Predictions are locked with a date *before* readout (use the `OSF_PREREGISTRATION.md` practice). A prediction edited after a readout is void.
- **Provenance or it doesn't exist.** Every effect, claim, and prediction traces to a PMID/NCT and a source span. Inherit the iterate agent's anti-fabrication rules (no invented PMIDs, no overstated preclinical).
- **Show the work.** Every pooled estimate ships with heterogeneity, sensitivity, and risk-of-bias notes — never a bare number.

---

## 6. Anti-goals (the failure mode to resist)

The gravitational pull here is toward **breadth that feels like progress and isn't**: more domains, more dashboards, more snapshots. A science arm gets *narrower and deeper* — a few falsifiable bets, scored ruthlessly. Resist:
- Adding alert domains before the extractor is fixed.
- Reporting gap scores as findings rather than questions.
- Producing pooled estimates from unverified extractions.
- Predictions without lock dates.

---

## 7. Open decisions for the owner

1. **First meta-analysis target** — HbA1c/incretin (most feasible) vs C-peptide/T1D-immunotherapy (higher cure-relevance, lower readiness). Charter assumes incretin first; flip if cure-relevance outweighs feasibility.
2. **Where claims/predictions live** — new JSON files in `Analysis/Results/` (assumed here) vs. tables in `Diabetes_Research_Tracker.xlsx`.
3. **Verification source for Phase 1** — second AI-extraction pass vs. human spot-check vs. both.
4. **Scoring cadence** — let the existing daily monitor resolve predictions, or a dedicated weekly scoring run.

**Answered 2026-10-06 by the owner** (each the recommended option; the owner asked that methods calls be made by the analyst and only value calls be brought to him):
1. First meta-analysis target: **incretin HbA1c**. Built: orforglipron and CagriSema placebo pools on the Statistical Analysis page.
2. Store: **JSON files in `Analysis/Results/`** (`structured_effects.json`, `prediction_ledger.json`, `gap_tiers.json`). The Excel tracker is not a store.
3. Verification: **independent second AI extraction plus an automatic verbatim-span check** against the live abstract (`structured_effects.py`).
4. Scoring: **the daily run flags** a locked prediction when its trial posts results, and a provisional (press-release) resolution for re-checking (`resolve_predictions.py` step in `run_daily_local.py`). Resolving remains a person's call.

---

## 8. First three concrete steps (to leave this charter and start building)

1. Stand up `prediction_ledger.json` with the three seeded predictions; confirm readout dates; lock them.
2. Add a resolution check to the monitor: when a ledger trial's `results_posted` flips, flag it and compute the Brier component.
3. Rebuild the extractor for one outcome cluster (HbA1c) to Phase-1 schema; get to ≥5 verified records.

Everything else in this charter builds off those three.

---
*Draft v0.1 — written to be edited. Evidence levels per Research Doctrine. Predictions in §4.3 are unlocked priors, not registered forecasts.*
