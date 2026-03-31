# Roadmap: Fixing the Three Vulnerabilities
**Date:** March 30, 2026 | **Source:** 10-Question Self-Audit findings

---

## The Problem in One Sentence

We built a research platform with rigorous standards on paper (PRISMA, GRADE, triple-source validation) and a build pipeline that bypasses them (35 Python scripts generating 33 dashboards with no verification gate between generation and deployment).

## What We're Fixing

1. **The Verification Gap** — Content deploys before it's verified
2. **The Breadth-Depth Tradeoff** — 33 dashboards, variable quality, no triage
3. **The Credibility-Scale Paradox** — Public before trustworthy

## What Already Exists (and What Doesn't)

**We have:**
- `validate_citations.py` — checks PMID existence against PubMed API
- `agent_state.py` — tracks paper vetting status, gap audit history, work queue
- `pmid_verification.json` — results of PMID verification runs
- `AUDIT_REPORT.txt` + `AUDIT_FINDINGS.txt` — manual audit results
- Daily iteration loop (10 runs logged) vetting ~15-20 papers per run
- Context blocks on all dashboards ("what/how/limits" framing)

**We don't have:**
- A gate that blocks dashboard deployment if verification fails
- Semantic verification (does the cited paper actually support the claim?)
- External expert review of any output
- Analytics data on which dashboards anyone visits
- A triage ranking of which dashboards to keep vs. archive
- A way to distinguish "verified" dashboards from "unverified" ones in the UI

---

# PHASE 1: STOP THE BLEEDING (Week 1)

*Goal: No new unverified content goes public. Fix the most dangerous existing content.*

## 1.1 Add a Verification Gate to the Build Pipeline

**What:** Modify `run_quality_improvements.py` so that each build script's output is checked before the dashboard file is written.

**How:** Create a new script, `verify_before_deploy.py`, that runs after each build script and before the HTML file is written to `Dashboards/`. The verifier checks:

- Every PMID in the HTML resolves to a real PubMed record (already done by `validate_citations.py`)
- Every specific statistic (percentages, dollar amounts, sample sizes) has an inline citation
- No "Nature 2024" or "Lancet 2024" style citations without PMIDs
- No "AUC 1.0" or other implausible perfect-discrimination claims
- No financial projections without labeled methodology

**Pass/Fail:** If the verifier finds any CRITICAL issue, the dashboard is written to `Dashboards/_quarantine/` instead of `Dashboards/`. The quarantined file is visible to us but not deployed to docs/ or the public site.

**Concrete deliverable:** A modified `run_quality_improvements.py` that includes a verification step and a quarantine directory.

**Kill criteria for the gate itself:** If the gate produces >50% false positives (flagging legitimate content), simplify the checks rather than removing the gate.

## 1.2 Quarantine the Three Worst Dashboards

The audit identified three files with CRITICAL credibility issues. Quarantine them immediately — move from `Dashboards/` and `docs/Dashboards/` to `Dashboards/_quarantine/`:

| Dashboard | Reason | Action Required Before Restoring |
|-----------|--------|----------------------------------|
| `GKA_Pricing.html` | build_gka_pricing.py rated HIGHLY UNRELIABLE; unsourced $5B claim, fabricated pricing scenarios | Source every financial claim or remove; add explicit "author estimate" labels |
| `Gap_Deep_Dives.html` | 20+ unverifiable citations, fabricated AUC 1.0 claim, fabricated digital twin trial | Remove all unverifiable citations; rebuild affected sections from verified sources only |
| `LADA_Prevalence.html` | "$500K+" unsourced lifetime cost; "47M people" extrapolation from single study | Source cost claims or remove; present prevalence as range (2-12%), not point estimate |

**Note:** These dashboards are *not deleted* — they're quarantined. They come back when they pass verification.

## 1.3 Add Verification Status Badges to All Dashboards

**What:** Every dashboard gets a visible badge in its header:

- **VERIFIED** (green) — All claims traced to verified sources; passed audit
- **PARTIALLY VERIFIED** (amber) — Core claims verified; some sections pending
- **UNVERIFIED** (red) — Has not passed verification audit; treat as preliminary

**How:** Modify each build script to include a `verification_status` variable that the HTML template renders as a colored badge. Default is UNVERIFIED. Status upgrades require a documented audit.

**Current estimated status of all 33 dashboards:**

| Status | Count | Examples |
|--------|-------|---------|
| VERIFIED | ~5 | Nutrition_Beta_Cells, GKA_LADA, Acronym_Database, Medical_Data_Dictionary, Methodology |
| PARTIALLY VERIFIED | ~20 | Drug_Repurposing_Screen, LADA_Diagnostic_Model, most gap dashboards |
| UNVERIFIED | ~5 | GKA_Pricing (quarantined), Gap_Deep_Dives (quarantined), Statistical_Analysis |
| QUARANTINED | 3 | See 1.2 above |

---

# PHASE 2: TRIAGE AND FOCUS (Weeks 2-3)

*Goal: Identify the 10 dashboards that matter most. Fully verify those 10. Deprioritize the rest.*

## 2.1 Rank Dashboards by Value

We don't yet have Google Analytics data (GA4 was added in commit `8a392ab` but the project is 16 days old). Until we have traffic data, rank dashboards by:

**Tier A — Core identity (must be flawless):**
These define what the project is. They're the first things visitors see.

1. Research_Dashboard.html — landing page / overview
2. Paper_Library.html — the searchable evidence base
3. Clinical_Trial_Dashboard.html — the live trial tracker
4. Drug_Repurposing_Screen.html — flagship actionable tool
5. LADA_Diagnostic_Model.html — flagship actionable tool

**Tier B — Strong supporting content (should be verified):**
These add depth and are useful if someone drills in.

6. Gap_Synthesis.html — overview of all 15 gaps
7. Extracted_Evidence.html — 472 data points from 61 papers
8. Corpus_Analysis.html — co-occurrence network
9. Trial_Equity_Mapper.html — equity analysis (after expanding from 12 trials)
10. Health_Equity.html — disparity analysis

**Tier C — Specialist deep dives (verify on demand):**
These are useful for specific audiences but don't need to be perfect immediately.

11-25. Individual gap dashboards, LADA natural history, islet outcomes, etc.

**Tier D — Reference material (lowest priority):**
26-33. Acronym database, data dictionary, methodology, PMID verification, etc.

## 2.2 Full Verification Audit of Tier A Dashboards

For each Tier A dashboard, conduct a line-by-line audit:

1. **Extract every specific claim** (numbers, percentages, outcomes, costs)
2. **For each claim, verify:** Does the cited PMID exist? Does the paper actually state this? Is the claim accurately represented (not overstated, not out of context)?
3. **For uncited claims:** Find a source or mark as "author estimate" or remove
4. **Document the audit** in a verification log (JSON file per dashboard)
5. **Update the badge** to VERIFIED when complete

**Target:** 5 Tier A dashboards fully verified by end of Week 3.

**Verification log format** (stored in `Analysis/Results/verification_logs/`):
```json
{
  "dashboard": "Drug_Repurposing_Screen.html",
  "audit_date": "2026-04-XX",
  "auditor": "human_review",
  "claims_checked": 87,
  "claims_verified": 82,
  "claims_corrected": 3,
  "claims_removed": 2,
  "status": "VERIFIED",
  "notes": "..."
}
```

## 2.3 Build the Semantic Citation Checker

The current `validate_citations.py` checks PMID existence. We need a second layer:

**What:** A script that, for each claim-PMID pair, fetches the paper's abstract from PubMed and checks whether the abstract plausibly supports the claim.

**How:**
1. Extract claim-PMID pairs from each build script's data structures
2. For each pair, fetch the abstract via PubMed E-utilities
3. Run a similarity/relevance check: does the abstract mention the topic of the claim?
4. Flag mismatches for human review

**This catches:** Valid PMIDs cited for claims they don't support (the failure mode the audit found repeatedly).

**This doesn't catch:** Claims that are subtly overstated relative to the source (requires human judgment).

**Deliverable:** `verify_claim_source_match.py` that outputs a match report.

---

# PHASE 3: DEPTH OVER BREADTH (Weeks 4-6)

*Goal: Produce one publication-quality output. Use it as the template for everything else.*

## 3.1 Pick One Paper and Write It Properly

Instead of trying to fix all 33 dashboards simultaneously, pick the single strongest candidate for a preprint and make it excellent.

**Recommended candidate:** The Drug Repurposing Screen.

**Why this one:**
- Already pressure-tested against WHO EML and PubMed
- All 34 drugs have verified mechanisms
- Rated as one of the more credible outputs in the audit
- Has a clear audience (computational pharmacology, drug repurposing community)
- Fits a standard paper format (methods → results → discussion)

**What "publication quality" means:**
- Every claim has a verified PMID that the paper actually supports
- The scoring methodology is explicitly documented with sensitivity analysis
- Limitations are stated upfront (no wet-lab validation, subjective weights, etc.)
- The paper has been reviewed by at least one person with pharmacology or diabetes expertise
- Formatted for bioRxiv submission

**Target:** One preprint submitted by end of Week 6.

## 3.2 External Review — Get One Expert to Look at One Thing

The self-audit identified that we've had zero external validation. Fix this with the smallest viable step:

**Action:** Email 3-5 corresponding authors of papers we cite heavily in the Drug Repurposing Screen. The email:

> Subject: Independent computational drug repurposing screen for diabetes — requesting brief feedback
>
> Dear Dr. [Name],
>
> I'm an independent researcher building an open-source diabetes research synthesis platform. Our computational drug repurposing screen scores 34 generic drugs for diabetes-related mechanisms, and your work on [specific paper] is one of our key references.
>
> Would you be willing to glance at our scoring methodology and flag anything that seems wrong or naive? The full screen is at [GitHub link]. I'm specifically interested in whether our characterization of [specific drug's mechanism] is accurate.
>
> Any feedback — even a one-line "this looks fine" or "you've misunderstood X" — would be extremely valuable.

**Success metric:** At least 1 substantive response.

**Why this works:** Researchers are far more likely to respond to a specific, bounded request ("is this one thing right?") than to a general request ("review my whole platform").

## 3.3 Implement the "One In, One Out" Rule for Dashboards

**New rule:** No new dashboard is created until an existing dashboard is either (a) fully verified and promoted to VERIFIED status, or (b) archived to `Dashboards/_archive/`.

This directly addresses the breadth-depth tradeoff. The build pipeline makes it easy to generate dashboards, so the constraint needs to be policy, not technology.

**Operationally:** Remove dashboards that add the least value. Candidates for archiving:

| Dashboard | Reason to Archive |
|-----------|------------------|
| Statistical_Analysis.html | Meta-analytic pooling on small, heterogeneous samples may lend false precision |
| PMID_Verification.html | Internal tool, not for external audiences |
| GKA_Pricing.html | Already quarantined; financial projections without sources |

---

# PHASE 4: REBUILD TRUST (Weeks 7-12)

*Goal: The public-facing project reflects only verified content. External engagement begins.*

## 4.1 Rebuild the Public Website with Verified Content Only

The `docs/` directory (GitHub Pages) should only serve dashboards that have VERIFIED or PARTIALLY VERIFIED status. Quarantined and unverified dashboards are excluded from the public site.

**How:** Modify `rebuild_website.py` to check each dashboard's verification status before copying to `docs/Dashboards/`. The public site gets a "Verification Status" page showing which dashboards have been audited and their status.

## 4.2 Rewrite the Research Findings Summary from Verified Sources Only

`Research_Findings_Summary.md` is the project's public face. It currently contains 5 references marked "PMID requires verification" and several "No DOI — reference pending" markers.

**Action:** Go through every claim in the summary. For each:
- If the PMID is verified and the claim is accurate: keep
- If the PMID is unverified: either verify it now or remove the claim
- If "No DOI": either find the source or remove the claim and note it was removed

**Target:** Zero "requires verification" and zero "reference pending" markers in the summary.

## 4.3 Update the Research Doctrine with Lessons Learned

The self-audit revealed several gaps in the Doctrine. Update it to v1.1:

**Add to Section A (Ingest Standard):**
- AI-generated content follows the same ingest process as external sources — it is not trusted by default
- Every specific statistic (percentage, dollar amount, sample size, effect size) requires an inline citation at the point of generation, not retroactively

**Add to Section B (Validation):**
- "Independent" requires: different funding source OR different research group with no co-authorship overlap in the last 5 years
- Tracing the evidence chain: for GOLD claims, document the primary data source behind all three citations (to catch cases where three citations all trace to one trial)

**Add a new Section H (Build Pipeline Standards):**
- No dashboard deploys to `docs/` without passing `verify_before_deploy.py`
- Quarantine protocol for dashboards that fail verification
- Verification badge requirements

**Add a new Section I (Known Limitations):**
- AI-generated content has a documented error rate of ~20-40% for specific claims in data-sparse topics
- The project is maintained by one person with AI assistance; it has not received formal peer review
- Computational drug repurposing screens require wet-lab validation before clinical relevance can be claimed
- Cost-effectiveness models use published parameter estimates, not primary claims data

## 4.4 Launch Targeted Outreach (Verified Content Only)

Only promote content that has VERIFIED status. Sequence:

1. **Week 8:** Post the Drug Repurposing Screen preprint to bioRxiv
2. **Week 9:** Share on r/bioinformatics and r/diabetes with a specific request for feedback
3. **Week 10:** Email PIs of papers we cite, as described in 3.2
4. **Week 11-12:** Share the GitHub repo with Breakthrough T1D and ADA via their collaboration portals

**Do not promote:** Dashboards with UNVERIFIED or QUARANTINED status. Any outreach that gets someone to a page with fabricated content does lasting reputational damage.

---

# PHASE 5: SUSTAINABLE OPERATIONS (Ongoing)

*Goal: The system maintains itself without accumulating new debt.*

## 5.1 Weekly Verification Cycle

Integrate verification into the existing daily iteration loop:

| Day | Activity |
|-----|----------|
| Monday | Run PubMed and ClinicalTrials.gov snapshots (already exists) |
| Tuesday-Thursday | Vet 15-20 papers per day (already exists via agent_state.py work queue) |
| Friday | Run `verify_before_deploy.py` on all dashboards; review quarantine list; update verification badges |

## 5.2 Monthly Self-Audit

Run a focused version of the 10-question audit on whatever was produced that month:

- Pick the 3 most consequential claims added this month
- Apply questions 1, 3, 7, and 8 (definition, mechanism, simplest explanation, right metric)
- Document findings in `Analysis/Results/monthly_audits/`

## 5.3 Quarterly External Review

Every 3 months, send the single most important finding to at least one external expert for review. Track whether the feedback changes anything.

## 5.4 Analytics-Driven Dashboard Pruning

After 90 days of Google Analytics data (around late June 2026):

- Archive any dashboard with <10 total visits
- Investigate any dashboard with high bounce rate (>80%) — it may be confusing or low-quality
- Double down on dashboards that show engagement (>2 min average session, return visits)

---

# DECISION LOG

These are pre-committed decisions. If the conditions are met, we act without debate.

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Audit finds fabricated PMID in content generated *after* Phase 1 gate was implemented | Halt all new content generation; investigate why the gate failed | The gate is our primary defense; if it fails, everything downstream is compromised |
| >50% of GOLD claims have traceable errors when audited | Redesign the tier system from scratch | The tiers aren't separating signal from noise |
| Preprint receives <50 views after 3 months | Pivot from academic publication to direct outreach (PI emails, community forums) | The audience isn't on preprint servers |
| Zero substantive expert responses after 10 outreach emails | Seek a collaborator with domain credentials before further outreach | Independent researchers without credentials face a credibility wall |
| After 90 days, total unique dashboard visitors <50 | Consolidate to 5 dashboards max; consider switching format entirely (blog, newsletter, or direct data contributions to existing platforms like Open Targets) | The dashboard format isn't reaching anyone |
| Drug Repurposing Screen — 8/10 top candidates already in active diabetes clinical trials | Redesign scoring to penalize well-known candidates and reward novelty | The screen is confirming what's known, not discovering what's new |
| LADA reclassified by ADA/WHO (no longer a distinct entity) | Archive the LADA Diagnostic Model and all LADA-specific dashboards | The clinical rationale collapses |

---

# SUMMARY: What Changes Immediately

1. **Today:** Quarantine GKA_Pricing, Gap_Deep_Dives, and LADA_Prevalence dashboards
2. **This week:** Build `verify_before_deploy.py` and integrate into the build pipeline
3. **This week:** Add verification status badges (VERIFIED/PARTIALLY VERIFIED/UNVERIFIED) to all 33 dashboards
4. **Next 2 weeks:** Full verification audit of the 5 Tier A dashboards
5. **Next 4 weeks:** Write and submit the Drug Repurposing Screen as a preprint
6. **Next 4 weeks:** Send 3-5 targeted expert feedback requests
7. **Next 6 weeks:** Update Research Doctrine to v1.1 with lessons from the self-audit

---

*This roadmap is itself subject to revision. If Phase 1 reveals that the problems are deeper than expected (e.g., >50% of dashboards need quarantine), we should contract the scope further and focus on making 3-5 things excellent rather than 33 things mediocre.*

*Version 1.0 — March 30, 2026*
