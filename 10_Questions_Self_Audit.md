# Diabetes Research Hub — 10-Question Self-Audit
## Applying Critical Thinking to Every Step of Our Pipeline
**Date:** March 30, 2026 | **Author:** Justin Bottum + AI Research Assistant

---

This document applies 10 critical thinking questions — originally developed from a DFS analytics case study where a statistically significant finding (p=0.027) was built on a backwards definition — to every major step of the Diabetes Research Hub. The goal is to catch the moment where we fall in love with our own framework and stop noticing that the foundation is wrong.

---

## The 10 Questions

1. What definition am I using, and is it measuring what I think it's measuring?
2. What would it look like if this assumption were wrong?
3. Am I confusing correlation with the mechanism I think is causing it?
4. What's the base rate, and am I beating it?
5. Who actually succeeds at this, and do they look like what I expect?
6. Does my signal survive when I change the definition threshold?
7. What's the simplest explanation for what I'm seeing?
8. Am I optimizing the right metric?
9. Can I actually act on this finding prospectively, or only retroactively?
10. What would make me abandon this approach entirely?

---

# STEP 1: Research Doctrine & Evidence Framework

*Establishing the triple-source validation system, CEBM evidence hierarchy, GRADE certainty, and the 4-tier confidence system (GOLD/SILVER/BRONZE/UNVERIFIED).*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We define "GOLD" as 3+ independent sources from different research groups. But "independent" is doing enormous work here. In diabetes research, the same handful of groups — Vertex, Novo Nordisk, the DIAMANTE consortium — produce the lion's share of primary data. A Cochrane review, a Lancet editorial, and an ADA guideline might all trace back to the same Phase 3 trial. That's three sources, but is it really three independent confirmations? In many cases, our "GOLD" standard is actually measuring "how many times the same primary data has been re-cited," not "how many independent observations confirm this claim." This is the same trap as defining "sharp" by volume — the metric looks rigorous but may be measuring the wrong thing.

**What we should do:** For each GOLD-rated claim, trace the evidence chain backward to count truly independent primary data sources, not just publications that reference the same trial.

### Q2: What would it look like if this assumption were wrong?

If the triple-source framework doesn't actually separate reliable from unreliable claims, we'd expect to find GOLD-rated claims that later get revised or contradicted at similar rates to SILVER claims. We'd also expect to find BRONZE claims that turn out to be robust. Look at our own data: the Zimislecel VX-880 finding is rated SILVER (two independent trial reports), but it's arguably more reliable than some GOLD claims that rest on meta-analyses of heterogeneous small studies. Meanwhile, the urine metabolomics "100% accuracy" claim was only BRONZE — and it was indeed overblown. So the tiers are doing *some* work, but they may be measuring citation density rather than epistemic reliability.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

The mechanism behind the triple-source framework is: "More independent confirmations → more likely to be true." But there's a confound: claims that get cited three times are often claims about well-funded, high-profile topics (GLP-1 agonists, stem cells). Claims that stay at BRONZE are often in neglected areas (personalized nutrition for LADA, GKA pricing). So our confidence tiers may correlate with topic popularity rather than truth. A well-funded false claim will accumulate three sources faster than a true claim in an obscure niche.

### Q4: What's the base rate, and am I beating it?

What's the base rate of a peer-reviewed claim surviving 5 years without significant revision? In fast-moving fields like diabetes therapeutics, it's probably 60-70%. Our GOLD standard aspires to be higher, but we haven't measured whether our GOLD claims actually hold up better than a random sample of peer-reviewed claims. Without this comparison, we don't know if our framework adds value or just adds bureaucracy.

### Q5: Who actually succeeds at this, and do they look like what I expect?

The gold standard for evidence synthesis is Cochrane Reviews — formal teams with librarians, methodologists, and domain experts who spend 12-18 months on a single review. We're an independent researcher with AI assistance producing 15 gap analyses, 33 dashboards, and a 34-drug screen in about two weeks. Successful evidence synthesis at this scale usually comes from funded consortia (DIAMANTE, DIAGRAM) or specialized evidence synthesis centers. We don't look like them. That's not necessarily fatal — speed and breadth are our competitive advantage — but we should be honest that the people who do this well have capabilities (wet-lab validation, biostatistician review, clinical domain expertise) that we structurally lack.

### Q6: Does my signal survive when I change the definition threshold?

If we changed GOLD from 3+ sources to 4+ sources, how many claims survive? If we tightened "independent" to mean "different funding sources and no co-authorship overlap," how many GOLD claims drop to SILVER? We haven't tested this. The thresholds (3/2/1) were chosen by convention, not by optimization. They might be right — but we haven't pressure-tested whether the framework is robust to threshold changes.

### Q7: What's the simplest explanation for what I'm seeing?

The simplest explanation for why we have 4 GOLD, 7 SILVER, and 3 BRONZE gaps is: well-studied topics have more sources, neglected topics have fewer. The tier system may just be reflecting the state of the literature rather than adding analytical value. A simpler alternative to the 4-tier system might be: "Is there at least one RCT? Yes/No." That single binary might partition claims into reliable and unreliable just as effectively.

### Q8: Am I optimizing the right metric?

We're optimizing for *number of sources confirming a claim.* But the audit findings (AUDIT_REPORT.txt, AUDIT_FINDINGS.txt) revealed that the real quality problems weren't claims with too few sources — they were claims with fabricated sources, unsourced statistics, and overstated preclinical data. The metric we should optimize for might be "percentage of claims with verified, traceable citations" rather than "number of sources per claim." Our audit caught AUC 1.0 claims, fabricated trial descriptions, and "$5 billion" unsourced financial statistics — none of which the triple-source framework would have caught because they were never going through the validation pipeline to begin with.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

The triple-source framework is prospective in theory: new claims must pass through validation before entering deliverables. In practice, the build scripts (35 Python scripts generating dashboards) embed claims directly in code, and the validation happens retroactively via audits. The March 2026 credibility audit (commits `69d36bc`, `c57221b`) found fabricated PMIDs, unsourced statistics, and overstated language — all of which were already live in dashboards. The framework exists on paper but the enforcement loop has gaps.

### Q10: What would make me abandon this approach entirely?

If we found that the majority of our GOLD-rated claims had fundamental flaws that the triple-source framework missed, or if the framework consumed more time than it saved in error correction, we should scrap it. More specifically: if the next credibility audit reveals that GOLD claims have similar error rates to SILVER/BRONZE claims, the tier system isn't adding signal. Kill criteria: >20% of GOLD claims have traceable errors that the framework should have caught.

---

# STEP 2: Literature Gap Analysis

*Querying PubMed for 30 domains × 435 pairwise combinations to find under-researched intersections.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We define a "research gap" as a domain pair with low co-publication counts on PubMed relative to the geometric mean of each domain's individual publication count. But PubMed co-publication counts measure *how often two terms appear in the same paper's metadata*, not *how under-researched a topic actually is*. "Gene Therapy × LADA" returns 0 joint publications — but is that because nobody has studied it, or because it's called something different ("AAV vector delivery in autoimmune diabetes"), or because the work is published in journals that use different MeSH terms? We might be measuring PubMed indexing patterns rather than actual research activity.

### Q2: What would it look like if this assumption were wrong?

If our PubMed gap scores don't reflect actual research gaps, we'd expect to find active research programs in areas we've labeled as "gaps." For instance, "Beta Cell Regeneration × Health Equity" shows 0 joint publications, but there may be active programs addressing equitable access to beta cell therapies that don't use those exact terms. Check: are there clinical trial registrations, conference abstracts, or non-indexed reports in our "zero" gap areas?

### Q3: Am I confusing correlation with the mechanism I think is causing it?

The assumed mechanism: low co-publication count → few researchers working on this intersection → genuine opportunity for contribution. Alternative mechanism: low co-publication count → the intersection is biologically implausible or clinically irrelevant → nobody works on it because there's nothing there. "GKA in LADA" (Gap 9, EXPLORATORY) may be a genuine case of the alternative — the intersection might not make biological sense, which is why it has zero publications, not because it's neglected.

### Q4: What's the base rate, and am I beating it?

What's the base rate for a random domain pair having zero co-publications? With 435 pairs, many of which are between non-adjacent fields, the base rate of zero overlap might be quite high (perhaps 20-30%). If we're identifying 15 "gaps" from 435 pairs, we need to confirm that these gaps are actually unusual rather than just typical of domain pairs that are conceptually distant.

### Q5: Who actually succeeds at this, and do they look like what I expect?

Successful research gap identification typically comes from domain experts who know the field intimately enough to recognize what's missing. Bibliometric gap analysis (our approach) is a known technique, but the literature on it (Boyack & Klavans, etc.) emphasizes that computational gap detection requires expert validation to filter out false positives. We have not done this external validation step.

### Q6: Does my signal survive when I change the definition threshold?

We use a normalized inverse overlap metric with gaps scored 0-100. Do the same 15 gaps emerge if we use a different normalization (e.g., Jaccard index instead of geometric mean)? If "Gene Therapy × LADA" only appears as a gap with one formula but not another, the finding is method-dependent, not robust.

### Q7: What's the simplest explanation for what I'm seeing?

The simplest explanation for 0 co-publications in many domain pairs: the fields use different vocabularies. "Autoimmunity T1D" and "Gene Therapy" papers probably exist but use terms like "immune tolerance induction" and "viral vector delivery" that don't trigger both our PubMed queries simultaneously. The gap might be in our search strategy, not in the research landscape.

### Q8: Am I optimizing the right metric?

We're optimizing for identifying the maximum number of under-researched intersections. But the right metric might be: "which gaps, if addressed, would have the highest clinical impact?" A gap that exists because the intersection is clinically irrelevant has zero value. We should rank gaps by potential impact, not just by size.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

This is a strength of this step. Gap identification is inherently prospective — it tells us where to focus future work. We've used it to prioritize 15 research deep dives, a drug repurposing screen, and targeted literature monitoring. The finding is actionable.

### Q10: What would make me abandon this approach entirely?

If expert validation (which we haven't done) reveals that >50% of our identified gaps are false positives — either because the research exists under different terminology, or because the intersection is biologically implausible — we should abandon bibliometric gap detection as a primary tool and switch to expert-guided gap identification.

---

# STEP 3: Clinical Trial Intelligence

*Pulling live snapshots from ClinicalTrials.gov API v2, tracking 746 trials across five categories.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We categorize trials into five buckets: T1D cure, T1D immunotherapy, T2D novel therapies, diabetes devices, and recently completed with results. These categories are assigned by our search queries and manual classification. But the boundary between "T1D cure" and "T1D immunotherapy" is blurry — is teplizumab (delay of onset) a "cure" or an "immunotherapy"? Miscategorization could make one category look more active than it is while hiding activity in another.

### Q2: What would it look like if this assumption were wrong?

If our categorization is wrong, we'd see trials that clearly belong in one category showing up in another, or important trials missed entirely because they don't match our search terms. We should sample 20 trials and verify their categorization manually.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

We hypothesize (H2 in the OSF pre-registration) that T1D curative trial activity has accelerated since 2023. If we find more Phase 2-3 trials, is that because the field is genuinely accelerating, or because COVID-era trial delays are resolving and these trials were always planned? The mechanism matters for whether the trend continues.

### Q4: What's the base rate, and am I beating it?

What's the base rate of clinical trial success in diabetes? Phase 2-3 success rates in oncology are ~30-35%. In diabetes, they may be higher for incremental therapies (GLP-1 variants) but much lower for curative approaches (stem cells, gene therapy). We should benchmark our trial pipeline projections against historical success rates rather than assuming most tracked trials will reach market.

### Q5: Who actually succeeds at this, and do they look like what I expect?

Successful clinical trial intelligence comes from services like Citeline, GlobalData, and Evaluate — organizations with dedicated analysts, proprietary databases, and pharma industry relationships. Our advantage is being free and open, but our coverage may have systematic blind spots (e.g., trials registered on non-US registries like EudraCT or CTRI that aren't on ClinicalTrials.gov).

### Q6: Does my signal survive when I change the definition threshold?

If we changed "recently completed" from 2025+ to 2024+, does our picture of the field change meaningfully? If we expanded from ClinicalTrials.gov to include EU and Chinese registries, how many new trials appear? Our conclusions are bounded by our data source.

### Q7: What's the simplest explanation for what I'm seeing?

We track 746 trials. The simplest explanation for any trend we observe: ClinicalTrials.gov registration requirements have expanded, so more trials are registered, making the field look more active even if the actual pace of innovation hasn't changed.

### Q8: Am I optimizing the right metric?

We're optimizing for comprehensive coverage (number of trials tracked). The better metric might be: "How quickly do we detect clinically meaningful status changes?" If a Phase 3 trial fails and we don't flag it for two weeks because our monitoring cycle is biweekly, we're optimizing breadth at the expense of timeliness.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

Trial intelligence is prospective by design — it tells us what's coming. But our ability to act is limited: we can update dashboards and adjust research priorities, but we can't influence trial outcomes. The prospective value is in prioritization, not intervention.

### Q10: What would make me abandon this approach entirely?

If ClinicalTrials.gov data quality is too poor (missing results, delayed status updates, incomplete enrollment data) for our snapshot approach to detect meaningful signals, the monitoring adds noise rather than insight. Kill criteria: if >30% of "completed" trials have no results posted within 12 months of completion, our "results tracking" step is unreliable.

---

# STEP 4: Paper Ingestion & Citation Validation

*226 papers ingested, 91 full text, with PMID cross-referencing against PubMed API. Every citation scored CONFIRMED/PLAUSIBLE/WEAK/MISMATCH.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We define "ingested" as having a PMID recorded and basic metadata extracted. But 226 papers with 91 full text means 135 papers (60%) are abstracts only. When we cite these abstract-only papers to support a claim, we're relying on the abstract's summary rather than the full data. Abstracts are known to overstate findings relative to full texts. Our "ingested" count may overstate our evidence base.

### Q2: What would it look like if this assumption were wrong?

If abstract-only ingestion leads to systematically inflated claims, we'd expect to find cases where our summary of a paper's findings is more positive than what the full text supports. The audit found exactly this — several claims were traced to papers that didn't support them as strongly as stated.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

We assume that PMID validation (confirming a PMID exists and points to a real paper) means the citation supports our claim. But PMID validation checks *existence*, not *relevance*. The credibility audit (AUDIT_FINDINGS.txt) found papers with valid PMIDs that were cited for claims the paper didn't actually make. A valid PMID ≠ a valid citation.

### Q4: What's the base rate, and am I beating it?

The PMID verification rate was 184/184 pass on verified PMIDs. But the audit found 20+ "unverifiable journal citations without PMIDs" in the gap deep dives, plus fabricated trial descriptions. The base rate of citation accuracy in published systematic reviews is typically 25-40% having some error. Our error rate, caught in the audit, appears to be in that range or worse for certain files (build_gka_pricing.py rated "HIGHLY UNRELIABLE").

### Q5: Who actually succeeds at this, and do they look like what I expect?

Systematic review teams typically have a dedicated librarian performing citation verification. AI-assisted literature synthesis is a newer approach, and the known failure mode is "hallucinated citations" — which is exactly what our audit caught (fabricated Nature 2024 citations, a digital twin trial that appears to be fabricated). The people who succeed at citation accuracy use human verification loops, which we implemented retroactively via the audit.

### Q6: Does my signal survive when I change the definition threshold?

If we moved from "PMID exists" to "PMID exists AND the paper's abstract contains the specific claim we attribute to it," how many citations survive? The audit suggests the drop would be significant, particularly in the gap deep dives.

### Q7: What's the simplest explanation for what I'm seeing?

The simplest explanation for our citation quality problems: AI-generated content includes plausible-sounding but fabricated references, and our initial pipeline had no systematic check for this. The March 2026 audit caught the problem, but the issue was structural — the pipeline allowed content to flow from generation to dashboard without a human-in-the-loop verification step.

### Q8: Am I optimizing the right metric?

We optimized for paper count (226 ingested). The better metric: percentage of claims with fully verified, traceable, accurate citations. A library of 100 papers with 100% citation accuracy is more valuable than 226 papers where 15-20% have citation problems.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

The current pipeline is partially prospective (the validate_citations.py script checks PMIDs against PubMed API), but the deeper semantic check (does the paper actually support the claim?) is still retroactive. We need a prospective semantic verification step before claims enter dashboards.

### Q10: What would make me abandon this approach entirely?

If the rate of AI-hallucinated citations makes automated paper ingestion unreliable without 100% human verification, the automated pipeline adds cost (auditing time) without reducing total effort. Kill criteria: if >10% of ingested citations require correction after audit, the pipeline needs fundamental redesign before scaling further.

---

# STEP 5: Drug Repurposing Screen

*34 generic drugs scored across 5 dimensions (mechanism 25%, safety 20%, generic availability 20%, evidence 20%, equity 15%). Pressure-tested against WHO EML and PubMed.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We define "repurposing candidate" using a 5-dimension composite score. But the weights (25/20/20/20/15) are subjective. Why is mechanism evidence weighted 1.67× more than equity? These weights embed a value judgment about what matters — and different stakeholders (a pharma company, a global health NGO, a patient) would weight them differently. Our top candidate, Metformin (10.0), is already the most-prescribed diabetes drug in the world. Is our screen just rediscovering what's already known?

### Q2: What would it look like if this assumption were wrong?

If the composite scoring doesn't identify genuinely promising repurposing candidates, we'd expect to see: (a) the top candidates are obvious and already being pursued, and (b) genuinely novel candidates are buried in the middle of the list. Metformin scoring 10.0 and Verapamil scoring 8.8 suggests our screen may be measuring "existing evidence base" rather than "untapped repurposing potential." A drug with strong evidence will score high, but that's because it's already been studied — the repurposing opportunity may actually be lower.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

Drugs with high composite scores correlate with drugs that have been well-studied for diabetes. We interpret this as "these are the best candidates." But the correlation might mean: "these are the most-studied candidates, which is why they have the most evidence." The actual best repurposing opportunities might be drugs with moderate mechanism scores but no one has tested them yet — the drugs that would score lower precisely because the evidence gap exists.

### Q4: What's the base rate, and am I beating it?

What's the base rate of a computationally identified drug repurposing candidate actually reaching a clinical trial? Historically very low — perhaps 1-5% of computational predictions advance to human testing. Of our 34 drugs, many (Metformin, Verapamil, Losartan) are already in diabetes-related trials. For the truly novel candidates, the historical base rate suggests maybe 1-2 might ever be tested.

### Q5: Who actually succeeds at this, and do they look like what I expect?

Successful drug repurposing screens come from teams with: (a) access to proprietary drug-target databases, (b) computational chemistry expertise, (c) wet-lab validation capability, and (d) pharma partnerships to advance candidates. We have (a) partially via OpenTargets but lack (b), (c), and (d). The teams that succeed at this (e.g., the Broad Institute's Drug Repurposing Hub) have capabilities we structurally cannot match. Our screen is a starting point, not an endpoint.

### Q6: Does my signal survive when I change the definition threshold?

If we changed the weight of "equity" from 15% to 30% (emphasizing global access), does the top-10 list change? If we removed "generic availability" (since some patented drugs might be excellent candidates), do different drugs emerge? The sensitivity of our rankings to weight changes is untested.

### Q7: What's the simplest explanation for what I'm seeing?

The simplest explanation for Metformin ranking #1: it's the most-studied, cheapest, most available diabetes drug in history. Any scoring system that includes evidence, safety, and availability will rank it first. Our screen may just be an elaborate way of confirming that Metformin is a good drug. The question is whether the screen tells us anything we didn't already know.

### Q8: Am I optimizing the right metric?

We're optimizing for composite score. But the metric that matters is "novelty × feasibility" — how surprising is this candidate, and how likely is someone to act on it? A metric that penalizes well-known candidates and rewards unexpected ones would be more useful for identifying genuinely new repurposing opportunities.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

The screen identifies candidates, but we cannot run clinical trials. The prospective action is: share the screen with researchers who can. This is built into the Contribution Strategy. But the actionability depends entirely on whether domain experts find our computational screen credible enough to pursue, which requires external validation we haven't obtained.

### Q10: What would make me abandon this approach entirely?

If domain expert review reveals that our scoring methodology is naive relative to established drug repurposing frameworks, or if the top-ranked candidates are all already in active clinical trials (meaning our screen adds no information), we should either fundamentally redesign the scoring or redirect effort to areas where computational analysis adds genuine novelty. Kill criteria: if 8/10 of our top candidates are already in diabetes clinical trials, the screen is telling us what's already known.

---

# STEP 6: LADA Diagnostic Cost-Effectiveness Model

*4 screening scenarios across 4 healthcare tiers. Uses GAD antibody sensitivity (82%, DASP standardized) and Medicare complication costs.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We define LADA using GAD antibody positivity. But "LADA" itself is a contested definition — some experts consider it a subtype of T1D, others a distinct entity, others a misdiagnosis category. The diagnostic accuracy of GAD antibodies depends on the cutoff titer used, the assay method, and the population tested. Our 82% sensitivity is from the DASP-standardized assay, but many clinical labs use different assays with different performance characteristics. Our model may be more precise than the underlying diagnostic uncertainty warrants.

### Q2: What would it look like if this assumption were wrong?

If GAD sensitivity is actually 70% instead of 82% (plausible with non-DASP assays), our cost-per-QALY estimates shift significantly. Targeted screening at $40,614/QALY might move above the $50,000 threshold that many payers use, changing the conclusion from "cost-effective" to "borderline." We should run the model at 70%, 82%, and 90% to test sensitivity.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

The model assumes that early LADA diagnosis leads to better outcomes (earlier insulin initiation, fewer complications). But the evidence for this causal pathway is limited — most of it is observational, comparing patients diagnosed early vs. late. Observational studies conflate early diagnosis with generally better healthcare access. The mechanism might not be "early diagnosis → better treatment" but rather "patients with better healthcare access → both earlier diagnosis AND fewer complications."

### Q4: What's the base rate, and am I beating it?

Cost-effectiveness analyses in diabetes typically use $50,000-$100,000/QALY as the willingness-to-pay threshold. Our targeted screening estimate ($40,614/QALY) falls below $50K, which looks favorable. But what's the base rate of CEA models that conclude their intervention is cost-effective? In the literature, it's very high (>80%), which suggests publication bias. Our model reaching a favorable conclusion is typical, not exceptional.

### Q5: Who actually succeeds at this, and do they look like what I expect?

Successful CEA models that influence clinical guidelines come from health economics groups with: (a) access to real-world claims data, (b) formal health economics training, (c) validated Markov or microsimulation models, and (d) peer-reviewed publication. We have none of these. Our model uses published parameter estimates rather than primary data. The models that actually change screening policy (like USPSTF recommendations) involve multi-year modeling efforts with extensive sensitivity analysis and stakeholder input.

### Q6: Does my signal survive when I change the definition threshold?

The audit noted that GAD sensitivity was corrected from an earlier value to 82% (DASP standardized). But the LADA prevalence range in the literature is 2-12% — an enormous range. If true prevalence is 2% instead of 8.8%, the number needed to screen increases dramatically, potentially making all four scenarios cost-ineffective. Our model should report results across the full 2-12% prevalence range, not just at 8.8%.

### Q7: What's the simplest explanation for what I'm seeing?

The simplest explanation for our favorable cost-effectiveness result: we used a single-point prevalence estimate (8.8%) that happens to be toward the high end of the published range. Higher prevalence → more true positives → better cost-effectiveness. If we used the median estimate (~5%), the results might be less favorable.

### Q8: Am I optimizing the right metric?

We're optimizing for $/QALY. But the metric that matters for clinical adoption might be "probability that screening changes clinical management within 6 months." If a LADA diagnosis doesn't change the treatment plan for most patients (many would eventually get insulin anyway), the QALY gain is smaller than our model assumes.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

This is one of our most actionable outputs. The model could inform screening recommendations if validated by health economists. But the action requires external actors (guideline committees, healthcare systems) to adopt our findings, which requires the credibility we haven't yet established.

### Q10: What would make me abandon this approach entirely?

If LADA as a diagnostic category is formally abandoned (some experts argue it should be classified simply as T1D), the screening model becomes moot. Kill criteria: if major guideline bodies (ADA, WHO) stop recognizing LADA as a distinct entity, or if RCTs show that early insulin in LADA patients doesn't improve outcomes compared to standard T2D management, the entire model's clinical rationale collapses.

---

# STEP 7: Trial Equity Mapper

*12 verified clinical trials mapped against IDF Diabetes Atlas 2024 burden data for 40 countries.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We define "equity" using a custom composite score combining trial access, disease burden, and healthcare infrastructure. But "equity" in clinical trials is a complex concept involving representation, geographic access, economic barriers, and cultural factors. Our composite score might measure geographic distribution of trial sites (which we can observe) while missing the deeper equity issues (who within those countries actually enrolls). A trial in India might still only enroll urban, English-speaking, high-SES patients.

### Q2: What would it look like if this assumption were wrong?

If our equity mapper doesn't capture real inequity, we'd expect to see countries we rate as "high access" still having low enrollment of underrepresented populations. Check: do the trials in our 40-country map report demographic breakdowns? If not, our equity assessment is based on trial *location*, not trial *access*.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

We observe that high-burden countries (sub-Saharan Africa, South Asia) have fewer trial sites. We assume the mechanism is: lack of research infrastructure → fewer trials → inequitable access to cutting-edge therapies. But the mechanism might be: regulatory complexity → pharma companies avoid certain markets → fewer trials, regardless of infrastructure availability. The intervention implied by each mechanism is completely different.

### Q4: What's the base rate, and am I beating it?

What's the base rate of clinical trial geographic concentration? Most diabetes trials are conducted in the US, EU, and Japan — this is true across all therapeutic areas. Our finding that trial sites don't match disease burden is a well-documented phenomenon, not a novel discovery. The question is whether our mapper adds anything beyond confirming what's already known.

### Q5: Who actually succeeds at this, and do they look like what I expect?

Organizations that have successfully improved trial equity include the NIH (diversity requirements), the African Academy of Sciences, and patient advocacy groups. They succeed through policy mandates and funding mechanisms, not through mapping exercises. Our mapper is informational, not interventional.

### Q6: Does my signal survive when I change the definition threshold?

The audit revealed a critical problem: the previous version "contained fabricated sponsor names and wrong NCT attributions." After correction, we have 12 verified trials — a very small sample. With only 12 trials, any equity metric is highly sensitive to which trials are included. Adding or removing 2-3 trials could substantially change the geographic distribution picture.

### Q7: What's the simplest explanation for what I'm seeing?

The simplest explanation for geographic mismatch between trials and disease burden: pharma companies run trials where regulatory approval is fastest and most commercially valuable (US, EU, Japan). This is a business decision, not an oversight. Our mapper documents the consequence but doesn't address the cause.

### Q8: Am I optimizing the right metric?

We're optimizing for geographic coverage of trial mapping. The better metric: "What specific policy or funding changes would reduce the trial equity gap, and can we quantify their impact?" A map is descriptive; an intervention model is actionable.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

The mapper is descriptive of past and current trials. We can use it to advocate for more equitable future trial design, but we cannot change where trials are conducted. Prospective action requires connecting our analysis to organizations that fund or design trials.

### Q10: What would make me abandon this approach entirely?

If the equity mapper, after correction of fabricated data, has too few verified trials (12) to draw meaningful conclusions, we should either dramatically expand the verified trial set or acknowledge that this output is illustrative rather than analytical. Kill criteria: if we cannot verify at least 30 trials with geographic data, the mapper is too sparse to support equity conclusions.

---

# STEP 8: 15 Research Gap Deep Dives

*Individual deep-dive dashboards for each identified gap, with literature synthesis, clinical evidence, and open questions.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We define each "gap" as a bibliometrically identified intersection with low PubMed co-publication. The deep dives aim to characterize the gap with current evidence. But the audit (AUDIT_FINDINGS.txt) revealed that 20+ journal citations in the deep dives were unverifiable — no PMIDs, no DOIs, just "Nature 2024" or "Lancet 2024." The deep dives contained fabricated content dressed up as evidence synthesis. What we thought we were measuring (the state of evidence in each gap) was, in several cases, AI-generated plausible-sounding but unreal literature.

### Q2: What would it look like if this assumption were wrong?

It did look wrong, and we found it. The credibility audit identified: a fabricated AUC 1.0 biomarker claim, a fabricated digital twin trial (n=297, 72.7% remission), 5 post-marketing safety cases with no FDA source, and "curative" language for mouse models. This is exactly what a wrong assumption looks like — content that reads as authoritative but dissolves under verification.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

The gap deep dives present research findings within each gap area. But the mechanism connecting individual findings to the "gap" narrative may be forced. For example, Gap 9 (GKA in LADA) synthesizes findings about GKAs and findings about LADA, but the connection between them is speculative. We may be confusing "these two topics exist" with "these two topics should intersect."

### Q4: What's the base rate, and am I beating it?

What's the base rate of accuracy for AI-generated research synthesis? The audit found that files ranged from HIGH credibility (build_nutrition_beta.py: all 7 PMIDs valid) to HIGHLY UNRELIABLE (build_gka_pricing.py: major unsourced financial claims). The base rate appears to be roughly 60% of files are credible, 40% have significant problems. That's not good enough for a project claiming to follow PRISMA and GRADE standards.

### Q5: Who actually succeeds at this, and do they look like what I expect?

Successful research gap characterization comes from domain experts writing narrative reviews or systematic reviews with librarian assistance. The teams that do this well spend weeks on a single gap. We produced 15 gap deep dives computationally. The output quality maps exactly to what you'd expect: some are good (nutrition_beta), and some contain fabricated content (gap_deep_dives). Volume was prioritized over verification.

### Q6: Does my signal survive when I change the definition threshold?

Two gaps were promoted from BRONZE to SILVER during daily iteration runs (Gaps 4 and 5). Does the promotion reflect genuinely new evidence, or does it reflect finding additional citations for claims that were already in the system? If the tier promotions are based on finding more citations rather than finding genuinely new independent evidence, the signal isn't strengthening — we're just accumulating references.

### Q7: What's the simplest explanation for what I'm seeing?

The simplest explanation for the quality variation across deep dives: AI generates more reliable content when there's a larger literature base to draw from (nutrition/beta cells, LADA prevalence) and generates more fabricated content when the literature is sparse (GKA pricing, digital twins). The gaps where we have the least real evidence are exactly the gaps where AI hallucination risk is highest. This is a fundamental structural problem — we need the deep dives most where they're least reliable.

### Q8: Am I optimizing the right metric?

We optimized for coverage (15 gaps × comprehensive deep dive). We should have optimized for accuracy per gap. Five deeply verified gap analyses would be more valuable than 15 with variable credibility.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

The credibility audit was retroactive — it caught problems after they were already in dashboards. For prospective use, every future gap deep dive needs a mandatory verification step before dashboard deployment. The daily iteration process (vetting 15-20 papers per run) is a step toward this, but it's still catching up on existing debt.

### Q10: What would make me abandon this approach entirely?

If the cost of auditing AI-generated deep dives exceeds the cost of writing them from scratch with verified sources, the computational approach is net negative. Kill criteria: if >30% of claims in any deep dive require correction after audit, that deep dive should be rebuilt from scratch rather than patched.

---

# STEP 9: Dashboard & Visualization Platform

*33 Tufte-style HTML dashboards covering every research gap, the full paper library, corpus analysis, evidence browser, and all three actionable tools.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We define quality using "Tufte-style" principles: high data density, minimal decoration, integrated evidence annotations. But Tufte's principles were designed for presenting verified data to informed audiences. We're applying them to content with variable verification status. A beautifully formatted dashboard presenting a fabricated AUC 1.0 claim is worse than an ugly dashboard with a caveat — because the design lends false authority to the content.

### Q2: What would it look like if this assumption were wrong?

If our dashboards are lending false authority, we'd expect visitors to assume the content is more reliable than it is. We added context blocks to all 27 dashboards (commit `26d3100`: "what/how/limits framing"), which is good. But the dashboards still present BRONZE claims alongside GOLD claims in the same visual format. A visitor might not notice the tier labels.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

We assume that more dashboards = more value. But 33 dashboards might mean 33 surfaces where errors can appear and need maintenance. The mechanism connecting dashboards to impact isn't "more dashboards → more visibility" — it's "dashboards that specific people use → those people take action." If nobody is using the GKA Pricing dashboard, it's maintenance cost without value.

### Q4: What's the base rate, and am I beating it?

What's the base rate of research dashboards being used by their intended audience? For most academic projects, it's very low. Most research tools get created, published, and forgotten. Our 90-day target is 200 unique visitors. Without analytics data yet, we don't know if we're beating the base rate.

### Q5: Who actually succeeds at this, and do they look like what I expect?

Successful research dashboards include: Our World in Data (COVID tracker), ClinicalTrials.gov itself, and the Global Burden of Disease visualization. They succeed through: institutional backing, continuous data updates, and being *the* definitive source for a specific question. We have 33 dashboards covering a wide range of topics — breadth that makes it hard to be definitive about any single one.

### Q6: Does my signal survive when I change the definition threshold?

If we reduced from 33 dashboards to the 10 most validated and useful, would the project's impact decrease? Probably not — it might increase, because we'd have more time for verification and the remaining dashboards would be higher quality. The signal (research value) might be stronger with fewer, better dashboards.

### Q7: What's the simplest explanation for what I'm seeing?

The simplest explanation for having 33 dashboards: the build pipeline makes it easy to generate dashboards, so we generated one for everything. The number of dashboards reflects our production capability, not our verification capability or audience demand.

### Q8: Am I optimizing the right metric?

We're optimizing for dashboard count and visual quality. The right metrics: (a) number of external users, (b) time spent on each dashboard, (c) citations or references to dashboard content. We've added Google Analytics (commit `8a392ab`), which is the right move, but we need to use the data to prune dashboards that nobody visits.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

We can prospectively decide to stop building new dashboards until the existing 33 are fully verified and show usage. This is actionable now.

### Q10: What would make me abandon this approach entirely?

If analytics show that <5% of dashboards account for >80% of traffic, we should consolidate into a focused set. Kill criteria: if total unique visitors across all dashboards remains below 50 after 90 days, the dashboard approach isn't reaching our audience and we should try a different format (preprints, blog posts, direct outreach).

---

# STEP 10: Credibility Audit & Pressure Testing

*Systematic audit of build scripts, PMID validation, fabrication risk assessment, and correction of unsourced claims.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We define credibility using a multi-level severity system (CRITICAL/HIGH/MEDIUM) applied to individual claims. But the audit itself was conducted by the same AI system that generated the original content. An AI auditing its own output is better than no audit, but it's structurally limited — it can catch logical inconsistencies and verify PMIDs against PubMed, but it may not catch plausible-sounding claims that happen to be wrong in ways the AI doesn't recognize.

### Q2: What would it look like if this assumption were wrong?

If the AI audit missed important errors, we'd expect a human domain expert to find problems the audit didn't flag. We haven't tested this. The audit found obvious problems (fabricated PMIDs, AUC 1.0 claims), but subtler errors — misinterpreted study designs, wrong effect size directions, inappropriate population generalizations — might survive the audit.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

The audit found that files with fewer PMIDs had more problems. We might conclude: "more citations → more credible." But the mechanism might be: "files about data-rich topics (nutrition, well-studied drugs) are easier to cite correctly AND happen to have more PMIDs," while "files about data-sparse topics (pricing, equity) are harder to verify AND happen to have fewer PMIDs." The PMIDs aren't causing credibility — topic data density causes both.

### Q4: What's the base rate, and am I beating it?

The audit found 2 of 5 files (40%) were CREDIBLE, 1 was MOSTLY CREDIBLE, 1 was PROBLEMATIC, and 1 was HIGHLY UNRELIABLE. The more detailed gap deep dives audit found "LOW-MEDIUM" overall quality with "high fabrication risk." As a base rate for AI-generated research content, this is concerning but consistent with published findings on LLM factual accuracy in medical domains (typically 60-80% accuracy depending on topic complexity).

### Q5: Who actually succeeds at this, and do they look like what I expect?

Successful research auditing involves: independent replication, external peer review, and structured checklists applied by people who weren't involved in the original work. The best practice is the Cochrane Risk of Bias tool applied by two independent reviewers. We used one AI system reviewing its own work. The gap between our approach and best practice is large.

### Q6: Does my signal survive when I change the definition threshold?

If we changed "CRITICAL" from "fabricated data or unsourced major claims" to include "any specific statistic without an inline PMID," the number of CRITICAL findings would increase dramatically. Our severity thresholds are arguably too lenient — many MEDIUM issues (unsourced cost estimates, missing PMIDs for specific statistics) would be CRITICAL in a peer-reviewed publication.

### Q7: What's the simplest explanation for what I'm seeing?

The simplest explanation for the audit findings: AI content generation produces plausible text that sometimes contains fabricated details, and the probability of fabrication increases as the available training data decreases. The audit is catching a known, well-documented failure mode of LLMs. The solution isn't just auditing — it's changing the generation process to reduce fabrication in the first place.

### Q8: Am I optimizing the right metric?

The audit optimizes for finding errors. The better metric: "What percentage of errors were actually fixed, and did the fixes hold?" The commits show corrections were made (fabricated trials removed, PMIDs fixed), but we should track the before/after error rates across audit cycles to confirm improvement.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

The audit was retroactive by nature. To make it prospective, we need to integrate audit checks into the build pipeline — no dashboard deploys without passing automated PMID verification, unsourced-claim detection, and implausible-number flagging. Some of this exists (validate_citations.py), but the gap deep dives show it's not comprehensive.

### Q10: What would make me abandon this approach entirely?

If repeated audits show the same types of errors recurring (fabricated citations, unsourced statistics), it means the audit is catching problems but not preventing them. Kill criteria: if the third audit finds fabricated PMIDs in newly generated content (not legacy), the generation pipeline needs fundamental changes, not more auditing.

---

# STEP 11: OSF Pre-Registration & Publication Pipeline

*Open Science Framework protocol, GitHub repository, preprint targets, journal submission plan.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We pre-registered four hypotheses (H1-H4). But the pre-registration was written after the gap analysis and trial monitoring were already substantially complete. A pre-registration that follows the analysis isn't pre-registration — it's post-hoc rationalization with a timestamp. The value of pre-registration is preventing outcome-switching and selective reporting, which requires the protocol to genuinely precede the analysis.

### Q2: What would it look like if this assumption were wrong?

If our pre-registration doesn't add credibility, reviewers would note that the hypotheses are safe (likely to be confirmed by design) and that the "exploratory analyses" caveat covers everything interesting. H1 ("fewer than 5% of domain pairs will have co-publication rates exceeding the geometric mean") is almost tautological — with 435 pairs spanning very different fields, this is virtually guaranteed.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

We assume that pre-registration + OSF + GitHub signals rigor. But the mechanism connecting these signals to actual rigor requires that the protocols genuinely constrain our analysis. If we can classify any finding as "exploratory" (Section 5.5 of the pre-registration explicitly allows this), the pre-registration doesn't actually constrain anything.

### Q4: What's the base rate, and am I beating it?

What percentage of OSF pre-registrations from independent researchers lead to peer-reviewed publications? Probably quite low. The 90-day target includes a preprint submission and 6-month target includes a journal publication. These are ambitious for an independent researcher, and the base rate of success should calibrate our expectations.

### Q5: Who actually succeeds at this, and do they look like what I expect?

Independent researchers who successfully publish computational biology papers typically have: (a) a PhD in a relevant field, (b) a university affiliation (even adjunct), (c) at least one collaborator with domain expertise, and (d) a focused, single-question paper rather than a comprehensive platform. Our profile (independent researcher, AI-assisted, platform-scale) is unusual. That's not necessarily bad — but we should be realistic about the publication pathway.

### Q6: Does my signal survive when I change the definition threshold?

If we narrowed the pre-registration from "35 domains" to the 5 most validated areas, would the project's publication prospects improve? Almost certainly yes — a focused paper on one well-validated gap analysis is more publishable than a 35-domain platform overview.

### Q7: What's the simplest explanation for what I'm seeing?

The simplest explanation for our comprehensive pre-registration: it was easier to register everything than to make hard choices about what to focus on. Breadth feels productive, but journals reward depth.

### Q8: Am I optimizing the right metric?

We're optimizing for completeness of the pre-registration protocol. The right metric: "Does this pre-registration make a specific, falsifiable prediction that we could be wrong about?" If all predictions are safe bets, the pre-registration doesn't add epistemic value.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

We can prospectively narrow our publication strategy to focus on 1-2 strong papers rather than trying to publish the entire platform. This is actionable now.

### Q10: What would make me abandon this approach entirely?

If preprint submissions receive no engagement (zero comments, <100 views after 3 months), the academic publication pathway may not be the right channel for our work. Kill criteria: if two preprint submissions receive <50 views each, we should redirect effort to direct outreach (emailing PIs, posting to community forums) rather than formal publication.

---

# STEP 12: Contribution & Outreach Strategy

*Distribution plan targeting Breakthrough T1D, ADA, NIDDK, specific lab PIs, and open-source communities.*

### Q1: What definition am I using, and is it measuring what I think it's measuring?

We define success as "the right 50-100 people engage with our work." But "engage" is undefined. Is it a GitHub star? An email response? A citation? A collaboration offer? Different definitions of engagement lead to very different assessments of success. GitHub stars might measure developer interest, not research impact.

### Q2: What would it look like if this assumption were wrong?

If our outreach strategy doesn't reach the right people, we'd see: high generic traffic (bots, random visitors) but no substantive responses from domain experts. Or: researchers visit but don't return, suggesting the content isn't useful enough to bookmark.

### Q3: Am I confusing correlation with the mechanism I think is causing it?

We assume: "publish openly → researchers find it → they use it → impact occurs." But the mechanism connecting open publication to research impact requires: (a) discoverability (does anyone know we exist?), (b) credibility (does our work meet their quality bar?), and (c) relevance (does our work answer a question they have?). Open publication is necessary but not sufficient for any of these.

### Q4: What's the base rate, and am I beating it?

90-day target: 25 GitHub stars, 5 forks. For a new computational biology repo from an independent researcher, this is achievable but not automatic. The base rate for new bioinformatics repos getting >10 stars in 90 days is probably ~5-10%. We need active promotion, not just publication.

### Q5: Who actually succeeds at this, and do they look like what I expect?

The Contribution Strategy identifies the right targets (foundations, PIs, communities). But the organizations that succeed at research-to-impact translation (translational research centers, NCATS, disease foundations) have dedicated staff for this. Our strategy relies on Justin doing outreach while also running analyses. The people who succeed at this have division of labor.

### Q6: Does my signal survive when I change the definition threshold?

If we changed success from "3 direct researcher responses" to "1 concrete action taken based on our work" (e.g., a PI citing our screen in a grant application), the bar is much higher. The gap between engagement metrics and actual impact is usually large.

### Q7: What's the simplest explanation for what I'm seeing?

We haven't launched the outreach yet (the project is 16 days old as of March 30). The simplest explanation for any future engagement or lack thereof: most independent research projects fail to gain traction because the research community is enormous and attention is scarce. Success will require persistent, targeted effort over months.

### Q8: Am I optimizing the right metric?

The strategy optimizes for breadth of channels (GitHub, OSF, preprints, journals, social media, Reddit, email). The better optimization: depth on one channel. Being excellent on GitHub (comprehensive README, working code, responsive to issues) is better than being mediocre across six platforms.

### Q9: Can I actually act on this finding prospectively, or only retroactively?

The entire outreach strategy is prospective — it's a plan for future action. The question is sequencing: we should verify content quality before amplifying it. Promoting dashboards that contain fabricated citations would be worse than not promoting at all.

### Q10: What would make me abandon this approach entirely?

If after 6 months of active outreach, we have zero collaboration inquiries and zero citations, the outreach strategy needs fundamental rethinking. Kill criteria: if 6 months pass with zero substantive expert engagement (not GitHub stars — actual conversation with a domain expert), we should pivot to a fundamentally different approach (e.g., joining an existing research group rather than operating independently).

---

# CROSS-CUTTING FINDINGS

## The Three Biggest Vulnerabilities

**1. The Verification Gap.** Our most critical vulnerability, appearing in Steps 4, 8, and 10: AI-generated content flows into dashboards faster than it can be verified. The credibility audit caught fabricated PMIDs, unsourced statistics, and a fake clinical trial — all of which were live in dashboards before being caught. The Research Doctrine requires triple-source validation, but the build pipeline doesn't enforce it. This is the "backwards definition" problem from the DFS case — our framework looks rigorous on paper but the execution has a structural gap.

**2. The Breadth-Depth Tradeoff.** Appearing in Steps 2, 8, 9, and 11: we have 15 gap analyses, 33 dashboards, 34 drugs screened, 226 papers ingested — but the quality is uneven. The gap deep dives range from HIGH credibility to HIGHLY UNRELIABLE. The dashboards range from well-verified to containing fabricated content. Every additional output we produce is another surface that needs verification and maintenance. We're optimizing for breadth when the constraint is verification capacity.

**3. The Credibility-Scale Paradox.** Appearing in Steps 5, 6, 7, and 12: our work's value depends on domain experts finding it credible enough to use. But credibility requires: verified citations, external validation, publication, and track record — all of which take time. Meanwhile, the dashboards are public, the GitHub is live, and the content has known quality issues. Every day the project is visible with unresolved credibility issues is a day that first impressions are forming.

## The One Thing That Would Fix the Most

A mandatory pre-deployment verification gate: no content enters a dashboard or public document until every specific claim has been traced to a verified source with a confirmed PMID/DOI and the source has been checked to actually support the claim as stated. This single change addresses vulnerabilities 1 and 3 simultaneously, and naturally slows the pace of new output (addressing vulnerability 2).

---

*This audit is itself subject to the same questions. The analysis was generated by the same AI system that produced the original content. External domain expert review of this self-audit would catch errors that we, by definition, cannot see in our own work.*

*Version 1.0 — March 30, 2026*
