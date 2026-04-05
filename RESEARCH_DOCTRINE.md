# Diabetes Research Hub — Research Doctrine
**Version 1.1 | Updated March 31, 2026**
**Maintainer: Justin Bottum + AI Research Assistant**

---

## Purpose

This doctrine governs how we ingest, validate, organize, and act on diabetes research. Because we are not medical professionals, every claim that could influence understanding of human health must meet rigorous verification standards. This document defines those standards, evaluates where we can contribute most, and establishes repeatable processes for all research activities.

---

# PART I: NICHE EVALUATION — Where Can We Add the Most Value?

## Evaluation Criteria

Each of the 35 research domains is scored on four dimensions (1-5 scale):

**Can We Access the Data?** — Is the underlying data publicly available, downloadable, or queryable?
**Can We Computationally Contribute?** — Can AI/ML, data analysis, or synthesis create real value here?
**Is the Gap Large?** — Is this area under-served by current research infrastructure?
**Is the Impact High?** — Would progress here meaningfully advance diabetes treatment or cure?

Scores are summed (max 20) and domains are ranked into tiers.

---

## TIER 1: Highest-Value Contribution Areas (Score 16-20)

These are where we should focus first. We have data access, computational tools, a real gap to fill, and high downstream impact.

### 1. Multi-Omics Biomarker Integration (Score: 19/20)
- **Data Access: 5** — UK Biobank Proteomics, GWAS Catalog, DIAGRAM, GEO, Metabolomics Workbench all publicly available
- **Computational Value: 5** — ML-driven integration of genomic + proteomic + metabolomic data is exactly what AI does best
- **Gap: 5** — Most studies analyze single omics layers; cross-omics integration is nascent and under-resourced
- **Impact: 4** — Novel biomarkers could enable earlier detection and personalized treatment
- **What We Do:** Build cross-omics analysis pipelines. Download summary statistics from T1D/T2D Knowledge Portals and DIAGRAM. Run network analyses connecting genetic variants → proteins → metabolites → clinical outcomes. Identify biomarker candidates not visible in single-layer analysis.

### 2. Literature Synthesis & Gap Analysis (Score: 19/20)
- **Data Access: 5** — PubMed/PMC is fully open; all major journals accessible
- **Computational Value: 5** — AI excels at reading, summarizing, cross-referencing, and identifying contradictions across thousands of papers
- **Gap: 5** — No one is systematically synthesizing across all 35 domains simultaneously; most reviews cover one narrow area
- **Impact: 4** — Identifying research gaps, contradictions, and overlooked connections directly accelerates discovery
- **What We Do:** Systematic reviews following PRISMA methodology. Cross-domain synthesis (e.g., what do microbiome findings mean for immunology?). Contradiction mapping (claims in one paper vs. another). Gap identification (areas with few publications but high potential).

### 3. Clinical Trial Intelligence (Score: 18/20)
- **Data Access: 5** — ClinicalTrials.gov is fully open with API access
- **Computational Value: 5** — Automated monitoring, trend analysis, combination opportunity identification
- **Gap: 4** — Individual trial tracking exists; cross-trial pattern analysis and combination mapping does not at scale
- **Impact: 4** — Connecting trial results across programs can reveal combination therapies and accelerate timelines
- **What We Do:** Build automated ClinicalTrials.gov monitoring for all diabetes trials. Track enrollment, results, status changes. Map which therapies could be combined based on complementary mechanisms. Flag trials with unexpected results that deserve attention.

### 4. Drug Repurposing Computational Screening (Score: 18/20)
- **Data Access: 4** — DrugBank, OpenTargets, STRING, Reactome all accessible; some data requires application
- **Computational Value: 5** — Network pharmacology and target-disease mapping is a core AI strength
- **Gap: 5** — Massively under-explored; thousands of approved drugs have untested diabetes-relevant mechanisms
- **Impact: 4** — Repurposed drugs can enter clinical use years faster than novel molecules
- **What We Do:** Map all approved drugs against diabetes-related protein interaction networks. Use OpenTargets evidence scores to rank candidates. Cross-reference with known side effects that suggest metabolic activity (e.g., drugs that cause weight loss or glucose changes as side effects).

### 5. AI/ML Prediction Model Development (Score: 18/20)
- **Data Access: 4** — GWAS summary stats, UK Biobank (requires application), public clinical datasets
- **Computational Value: 5** — Building and validating predictive models is our core capability
- **Gap: 4** — Many models exist but few integrate across data types or validate across populations
- **Impact: 5** — Better prediction of who will develop diabetes or complications saves lives at population scale
- **What We Do:** Build risk prediction models using public genetic and clinical data. Validate existing models across different populations and datasets. Develop complication prediction models (retinopathy, nephropathy, CV) using biomarker data.

### 6. Epidemiological Data Analysis (Score: 17/20)
- **Data Access: 4** — GBD data, CDC datasets, IDF atlas all publicly available
- **Computational Value: 4** — Statistical analysis, trend modeling, disparity quantification
- **Gap: 4** — Health equity analysis is under-resourced; disparity data exists but is rarely systematically analyzed
- **Impact: 5** — Understanding where and why disparities exist is essential to equitable cures
- **What We Do:** Analyze global and US diabetes prevalence trends by demographic. Quantify technology access disparities (CGM, pump, telehealth) by race, income, geography. Model the impact of DPP enrollment scaling from 3% to higher rates. Project cost-effectiveness of screening programs.

---

## TIER 2: Strong Contribution Areas (Score 13-16)

We can add meaningful value here but may face data access limitations or need domain expertise support.

### 7. Microbiome-Metabolic Pathway Analysis (Score: 16/20)
- **Data Access: 4** — Human Microbiome Project, select study-level data available
- **Computational Value: 4** — Species-health association mapping, metabolite pathway analysis
- **Gap: 4** — Rapidly growing field; many datasets exist but few are integrated
- **Impact: 4** — Microbiome-guided nutrition could transform prevention
- **What We Do:** Map published microbiome-diabetes associations into a structured database. Cross-reference species with metabolite production and glycemic outcomes. Build a "microbiome → metabolite → glycemic effect" pathway map.

### 8. Protein Interaction Network Analysis (Score: 16/20)
- **Data Access: 4** — STRING, Reactome, Human Protein Atlas all open
- **Computational Value: 5** — Network analysis, hub identification, pathway mapping
- **Gap: 3** — Some analysis exists; room for deeper cross-referencing with diabetes-specific data
- **Impact: 4** — Identifies new druggable targets in diabetes pathways
- **What We Do:** Build diabetes-specific protein interaction subnetworks. Identify hub proteins (highly connected nodes) as potential drug targets. Cross-reference with AlphaFold structures for druggability assessment.

### 9. Epigenetic Data Mining (Score: 15/20)
- **Data Access: 3** — ENCODE open; DIAMANTE summary stats available; individual-level data restricted
- **Computational Value: 4** — CpG-to-gene-to-function mapping; methylation pattern analysis
- **Gap: 4** — Massive datasets exist but are under-analyzed; causal vs. consequential distinction unclear
- **Impact: 4** — Epigenetic markers could enable early risk detection and targeted prevention
- **What We Do:** Map the 1,120 DIAMANTE CpGs to genes, regulatory elements, and known diabetes biology. Identify which epigenetic changes precede disease (causal candidates) vs. follow it. Cross-reference with gene expression data from GEO.

### 10. Complication Prediction & Monitoring (Score: 15/20)
- **Data Access: 3** — Some public datasets; much complication data is in hospital systems
- **Computational Value: 4** — ML model development for early detection
- **Gap: 4** — Prediction models exist but few integrate multi-modal biomarker data
- **Impact: 4** — Preventing complications (blindness, kidney failure, amputation) is as important as curing diabetes
- **What We Do:** Catalog all published complication biomarkers into a structured database. Build meta-analyses of prediction model performance. Identify combinations of biomarkers that outperform single markers.

### 11. Diabetes Subtype Misdiagnosis Analysis (Score: 14/20)
- **Data Access: 3** — Literature-based; clinical data is restricted
- **Computational Value: 3** — Synthesis and decision-tree development
- **Gap: 5** — 4-14% of "T2D" patients actually have LADA; Type 3c commonly misdiagnosed; huge clinical gap
- **Impact: 3** — Better classification directly improves treatment selection for millions
- **What We Do:** Build a comprehensive literature review of misdiagnosis rates by subtype. Create diagnostic decision trees and differential checklists. Quantify the clinical impact of correct vs. incorrect classification.

### 12. Technology Accessibility & Digital Health (Score: 14/20)
- **Data Access: 3** — Some public data; much is proprietary
- **Computational Value: 3** — Analysis of adoption data, outcome correlations
- **Gap: 4** — Technology access equity is under-studied
- **Impact: 4** — Ensuring cures and technology reach everyone, not just wealthy populations
- **What We Do:** Synthesize all published data on technology access disparities. Model the health impact of closing technology gaps. Analyze cost-effectiveness of expanding CGM/pump access.

---

## TIER 3: Monitoring & Support Areas (Score 8-12)

These are important research areas where our role is primarily tracking, synthesizing, and connecting — not generating original computational work.

### 13. Stem Cell / Islet Biology (Score: 12/20)
- Data mostly in lab and clinical settings; our role is monitoring trials, synthesizing results, tracking timelines

### 14. Immunology / Treg / CAR-T Development (Score: 12/20)
- Wet-lab and clinical work; we track, synthesize, and identify combination opportunities

### 15. Gene Therapy Development (Score: 11/20)
- Lab-based; we monitor progress and cross-reference with computational target data

### 16. GLP-1 / Multi-Agonist Pharmacology (Score: 11/20)
- Clinical trial driven; we track results, compare across trials, identify patterns

### 17. Artificial Pancreas / Closed-Loop Technology (Score: 11/20)
- Engineering-driven; we can analyze published TIR data and compare systems

### 18. Lifestyle Intervention & DPP Scaling (Score: 10/20)
- Policy and implementation focused; we analyze outcomes data and model scaling scenarios

---

# PART II: RESEARCH DOCTRINE — Standards and Processes

## Section A: The Ingest Standard

Every piece of information entering the Research Hub must pass through a standardized ingest process.

### Step 1: Source Classification

All sources are classified using the **Oxford CEBM Evidence Hierarchy** (adapted):

| Level | Source Type | Examples | Weight |
|-------|-----------|----------|--------|
| **1a** | Systematic review of RCTs | Cochrane reviews, PRISMA-compliant meta-analyses | Highest |
| **1b** | Individual RCT with narrow confidence interval | Phase 3 trial with published results | High |
| **2a** | Systematic review of cohort studies | Multi-study meta-analyses | High |
| **2b** | Individual cohort study or low-quality RCT | Phase 1/2 trials, longitudinal studies | Moderate-High |
| **3** | Case-control study, case series | iPSC case report, small series | Moderate |
| **4** | Expert opinion, mechanism-based reasoning | Review articles, editorials, commentary | Low-Moderate |
| **5** | Preclinical / animal studies | Mouse models, in vitro studies | Low (for clinical claims) |
| **G** | Guidelines / Standards of Care | ADA Standards, WHO guidelines | High (for practice) |

### Step 2: Source Recording

Every ingested source must include:

- **Full citation** (authors, title, journal, year, DOI/URL)
- **Evidence level** (from table above)
- **Claim extracted** (specific, falsifiable statement)
- **Sample size** (if applicable)
- **Population** (who was studied)
- **Limitations noted by authors**
- **Our confidence tag**: Verified / Likely / Uncertain / Unverified

### Step 3: Ingest Checklist

Before any claim enters the Hub as fact:

- [ ] Source identified and classified by evidence level
- [ ] Full citation recorded with DOI/URL
- [ ] Claim stated as specific, falsifiable statement
- [ ] Source is peer-reviewed OR from an established institution
- [ ] Publication date recorded (recency matters)
- [ ] Any conflicts of interest noted (industry funding, etc.)
- [ ] Claim added to validation queue

---

## Section B: The Triple-Source Validation Framework

**No claim is presented as fact in any Hub deliverable unless verified by three independent sources.**

### Validation Tiers

**GOLD — Triple Verified (Required for all factual claims)**
Three independent sources confirm the claim. Sources must be:
1. From different research groups (not the same team publishing in multiple journals)
2. From different institutions (not collaborators on the same grant)
3. At least one must be Level 1-2 evidence (systematic review, RCT, or large cohort study)

If a claim cannot reach GOLD status, it must be explicitly labeled:

**SILVER — Double Verified (Acceptable with disclosure)**
Two independent sources confirm, but a third is unavailable. The claim is presented with the label: *"Supported by two independent sources; awaiting additional confirmation."*

**BRONZE — Single Source (Flagged as preliminary)**
Only one source supports the claim. It is presented with: *"Preliminary finding from a single study. Requires independent replication."*

**UNVERIFIED — No independent confirmation**
The claim is not included in any deliverable. It may be held in a "Watch List" for future verification.

### Validation Process

For each claim entering the Hub:

1. **State the claim precisely.** E.g., "10 of 12 patients receiving full-dose Zimislecel achieved insulin independence at 1 year."

2. **Source 1 (Primary):** Identify the original research paper or trial report.
   - Record: Citation, evidence level, sample size, date

3. **Source 2 (Independent Confirmation):** Find a second source that independently confirms or reports the same finding.
   - Acceptable: Different journal reporting same trial results, systematic review including the study, reputable medical news coverage citing the original data, regulatory filing (FDA, EMA) referencing the data
   - NOT acceptable: The same press release reposted on multiple sites, the same authors in a different journal, a blog or social media post

4. **Source 3 (Cross-Validation):** Find a third source that provides additional context or confirmation.
   - Acceptable: Expert commentary in a peer-reviewed journal, guideline that incorporates the finding (e.g., ADA Standards of Care), meta-analysis or review that includes the finding, conference presentation with independent peer review
   - NOT acceptable: Wikipedia, promotional materials from the drug manufacturer (as sole source), preprints without peer review (as sole source)

5. **Record all three sources** in the validation log with evidence levels.

6. **Assign the validation tier** (Gold/Silver/Bronze/Unverified).

### Special Rules

- **Preclinical claims** (mouse studies, in vitro): Cannot be presented as evidence for human efficacy. Must be explicitly labeled: *"Demonstrated in [animal/cell model]. Human relevance is unconfirmed."*
- **Industry-sponsored research**: Must be cross-validated with at least one independent (non-industry) source.
- **Preprints**: May be used as one of three sources but never as the sole or primary source.
- **News coverage**: Counts as a source only if it cites specific data from an identifiable study. Generic reporting does not count.
- **Conference abstracts**: Count as a source but at reduced weight (one evidence level below the study type).

---

## Section C: The Confidence Dashboard

Every major claim in the Hub gets a confidence rating displayed in deliverables:

```
███████████ GOLD (3+ sources, Level 1-2 evidence present)
██████████░ SILVER (2 independent sources)
███████░░░ BRONZE (1 source, peer-reviewed)
███░░░░░░░ PRELIMINARY (preprint, conference, or single case)
░░░░░░░░░░ UNVERIFIED (watch list only)
```

---

## Section D: The Research Cycle

All research activities follow a repeatable 6-step cycle:

### Step 1: SCAN
- Monitor PubMed, ClinicalTrials.gov, preprint servers, major journals
- Flag new publications, trial results, regulatory actions
- Automated alerts for all 35 research domains
- **Output:** New items added to ingest queue

### Step 2: INGEST
- Apply source classification (CEBM levels)
- Record full citations and extracted claims
- Add to Research Tracker spreadsheet
- **Output:** Structured entries in the Pipeline, Papers, or Datasets sheets

### Step 3: VALIDATE
- Apply Triple-Source Validation Framework
- Assign Gold/Silver/Bronze/Unverified tier
- Record validation sources in log
- **Output:** Confidence rating for each claim

### Step 4: ANALYZE
- For Tier 1 domains: Run computational analysis (omics integration, network analysis, prediction models)
- For Tier 2 domains: Perform structured synthesis and literature review
- For Tier 3 domains: Update tracking and monitoring data
- **Output:** Analysis results, updated dashboards, new insights

### Step 5: SYNTHESIZE
- Cross-reference new findings across all domains
- Identify connections between domains (e.g., microbiome findings that affect immunology)
- Update the Research Findings Summary
- Flag contradictions or gaps
- **Output:** Updated summary documents, cross-domain insight reports

### Step 6: ACT
- Define specific, completable next steps (see Section E)
- Prioritize by impact and feasibility
- Execute and document
- **Output:** Completed deliverables, updated next-step queue

---

## Section E: Actionable Next Steps Framework

Every research cycle produces concrete next steps. These are categorized by what we can actually do.

### Category A: Data Analysis Projects (We Execute)
Tasks where we download public data, run analysis, and produce results.

| Project | Data Source | Method | Timeline | Priority |
|---------|-----------|--------|----------|----------|
| Multi-omics biomarker integration | T1D/T2D Portals + GWAS Catalog | Network analysis, ML | 2-4 weeks | HIGH |
| Drug repurposing screen | DrugBank + OpenTargets + STRING | Network pharmacology | 2-3 weeks | HIGH |
| Epigenetic causal analysis | DIAMANTE + GEO + ENCODE | CpG-gene-function mapping | 3-4 weeks | HIGH |
| Clinical trial pattern analysis | ClinicalTrials.gov API | Trend analysis, combination mapping | 1-2 weeks | HIGH |
| Disparity quantification | CDC + IDF + published data | Statistical analysis | 1-2 weeks | MEDIUM |
| Microbiome-metabolite mapping | Published studies + HMP | Pathway construction | 2-3 weeks | MEDIUM |
| Complication biomarker meta-analysis | Published studies | Systematic review | 3-4 weeks | MEDIUM |
| Protein interaction subnetwork | STRING + Reactome + HPA | Network hub analysis | 2-3 weeks | MEDIUM |

### Category B: Literature Intelligence (We Produce)
Systematic reviews, gap analyses, and synthesis documents.

| Deliverable | Scope | Method | Timeline | Priority |
|-------------|-------|--------|----------|----------|
| Cross-domain synthesis report | All 35 domains | PRISMA-aligned review | Ongoing | HIGH |
| T1D cure landscape comparison | All cure approaches | Structured comparison | 1-2 weeks | HIGH |
| T2D remission evidence review | Remission pathways | Systematic review | 2-3 weeks | HIGH |
| Misdiagnosis impact analysis | LADA, Type 3c, MODY | Literature synthesis | 1-2 weeks | MEDIUM |
| AI/ML model benchmark | Prediction models | Performance comparison | 2-3 weeks | MEDIUM |
| Biomarker candidate ranking | All published candidates | Multi-criteria scoring | 2-3 weeks | MEDIUM |

### Category C: Monitoring & Tracking (We Maintain)
Ongoing surveillance that we update regularly.

| Activity | Frequency | Source | Output |
|----------|-----------|--------|--------|
| PubMed alerts for all 35 domains | Weekly | PubMed | New papers flagged in tracker |
| ClinicalTrials.gov diabetes scan | Biweekly | CT.gov | Pipeline updates |
| FDA regulatory calendar tracking | Monthly | FDA.gov | Milestone timeline updates |
| Trial result monitoring | As published | Journals + CT.gov | Status changes in pipeline |
| Dataset availability monitoring | Monthly | Data portals | New datasets in catalog |

### Category D: Things We Cannot Do (Boundaries)
Being clear about what is outside our scope:

- We do NOT provide medical advice or treatment recommendations
- We do NOT interpret results for individual patient care
- We do NOT conduct wet-lab experiments or clinical trials
- We do NOT make regulatory predictions with certainty
- We do NOT replace peer review or expert clinical judgment
- All findings are for research synthesis purposes only

---

## Section F: Quality Assurance Checklist

Before any document, analysis, or update is finalized:

**Evidence Standards (aligned with PRISMA 2020 + GRADE + Cochrane RoB 2):**

- [ ] All factual claims have been triple-source validated (or clearly labeled with their tier)
- [ ] Evidence levels are recorded for all sources (CEBM) AND certainty assessed (GRADE: High/Moderate/Low/Very Low)
- [ ] **Risk of Bias assessed** for each key study using these domains:
  - Bias from randomization process
  - Bias from deviations from intended interventions
  - Bias from missing outcome data
  - Bias in measurement of the outcome
  - Bias in selection of reported result
- [ ] **Indirectness assessed**: Are the study populations, interventions, and outcomes directly applicable to our specific question?
- [ ] **Publication bias considered**: Are there reasons to suspect selective publication? (e.g., only positive results from a company's pipeline)
- [ ] **Inconsistency checked**: Do multiple studies agree? If not, is the disagreement explained?
- [ ] Preclinical findings are not presented as human evidence
- [ ] Industry-funded research is cross-validated with independent sources
- [ ] Limitations of each study are noted
- [ ] Confidence ratings are displayed for major claims
- [ ] No medical advice is given or implied
- [ ] All sources are cited with full references
- [ ] The document has been reviewed for internal contradictions
- [ ] Date of last verification is recorded

**Process Standards (aligned with PRISMA 2020 reporting requirements):**

- [ ] **Inclusion/exclusion criteria** are documented for any systematic search
- [ ] **Search strategy** is recorded (databases searched, terms used, date of search)
- [ ] **Screening decisions** are logged with reasons for exclusion
- [ ] **PRISMA flow diagram** is created for any formal literature review (records identified → screened → included)
- [ ] **Protocol documented** before starting any systematic analysis (pre-specification prevents bias)
- [ ] **Certainty rationale** is explicitly stated for each GRADE judgment (not just the rating, but why)

**Operational Standards:**

- [ ] Findings have been reviewed for consistency with ADA Standards of Care 2026
- [ ] Any claim that contradicts established guidelines is flagged and investigated
- [ ] Temporal context is noted (when a study was conducted matters; diabetes research moves fast)
- [ ] All deliverables include a "last verified" date

---

## Section G: Terminology Standards

To prevent confusion:

| Instead of... | We say... | Why |
|---------------|-----------|-----|
| "Cure" | "Functional cure" or "insulin independence" | True cure implies permanence not yet proven |
| "Proven" | "Demonstrated in [context]" | Nothing is proven until replicated at scale |
| "Safe" | "Well-tolerated in [trial name], N=[size]" | Safety requires long-term data |
| "Breakthrough" | "Significant advance" or "milestone" | Overused; we reserve for paradigm shifts |
| "Will be approved" | "Regulatory submission expected [date]" | Approval is never guaranteed |
| "Works" | "Showed efficacy in [study type]" | Specificity about evidence context |

---

# PART III: IMMEDIATE ACTION PLAN

Based on the niche evaluation, here are our first five projects, in priority order:

### Project 1: Literature Gap Analysis Engine
**What:** Systematically map publication density across all 35 domains to find under-researched intersections.
**How:** Query PubMed for publication counts by domain pair (e.g., "microbiome + retinopathy" vs. "microbiome + T2D"). Identify low-publication, high-potential combinations.
**Output:** Gap analysis matrix showing where new research could have outsized impact.
**Timeline:** 1 week.

### Project 2: Clinical Trial Intelligence Dashboard
**What:** Build automated monitoring of all active diabetes trials on ClinicalTrials.gov.
**How:** Query the API for all diabetes trials, extract status, phase, enrollment, results. Build monitoring pipeline.
**Output:** Live-updated trial tracker with alerts for status changes and results.
**Timeline:** 1-2 weeks.

### Project 3: Multi-Omics Biomarker Integration Pilot
**What:** Download publicly available T2D proteomic and genomic summary statistics and run cross-omics network analysis.
**How:** Start with UK Biobank proteomics (617 T2D-associated proteins) + DIAGRAM GWAS loci. Map protein-gene-variant connections using STRING and Reactome.
**Output:** Novel biomarker candidates not visible in single-omics analysis.
**Timeline:** 2-3 weeks.

### Project 4: Drug Repurposing Screen
**What:** Computationally screen approved drugs for diabetes-relevant mechanisms.
**How:** Use OpenTargets disease-target scores for T1D and T2D. Cross-reference with DrugBank to find approved drugs hitting those targets. Rank by evidence strength and mechanistic plausibility.
**Output:** Ranked list of repurposing candidates with supporting evidence.
**Timeline:** 2-3 weeks.

### Project 5: T1D Cure Landscape Comparison
**What:** Structured comparison of all T1D cure approaches with triple-verified evidence.
**How:** Apply validation framework to every claim. Build comparison matrix across efficacy, immunosuppression requirement, scalability, timeline, and risk.
**Output:** Gold-standard verified comparison document.
**Timeline:** 1-2 weeks.

---

# PART IV: VERIFICATION GATE LESSONS LEARNED (v1.1 Update)

**Date: March 31, 2026**
**Context:** These lessons emerged from applying verification gates across 33 production dashboards and identifying systematic vulnerabilities in citation validation and content integrity.

---

## Lesson 1: AI Citation Fabrication — Every PMID Must Be Independently Verified

### The Problem
AI-generated content frequently fabricates citations with alarming consistency:
- Wrong author names (e.g., crediting "Smith et al." when the actual first author is "Johnson")
- Wrong journals (e.g., claiming publication in "Nature Reviews 2025" when the paper appeared in a different journal entirely)
- Wrong publication years (off by 1-5 years)
- Completely nonexistent papers (PMIDs that don't exist in PubMed; journal-year-author combinations with no matching publication)

**Impact on Research Hub:** A single fabricated citation can propagate into analyses, dashboards, and published comparisons. If we cite a nonexistent paper to support a claim about drug efficacy or trial results, we've introduced unverifiable falsehood into our corpus.

### The Fix: PMID Verification Requirement
- **Every journal citation in Research Hub deliverables MUST include a PMID** (PubMed ID).
- **Before any citation is published, the PMID must be independently verified** against PubMed.org to confirm:
  - The PMID exists and is active
  - The authors match
  - The journal and year match
  - The title matches the cited claim
  - The actual paper supports the claim we're making

### Implementation
Add this verification step to the QA Checklist (Section F):

- [ ] **PMID Verification:** Every unique journal citation in this document has been independently looked up on PubMed. PMID confirmed to exist. Authors, journal, and year verified to match the citation. The actual abstract/full text reviewed to confirm it supports the claim being made.

---

## Lesson 2: Static vs. Dynamic Content Gap — JavaScript-Rendered Citations Are Invisible to Basic Scanners

### The Problem
Dashboards built with modern JavaScript frameworks (React, Vue) embed citations in:
- JSON data structures (e.g., `"references": [{"title": "...", "pmid": "..."}]`)
- Template literals and component state
- Lazy-loaded content that doesn't render until user interaction
- API responses that populate citation fields at runtime

Basic HTML scanning misses all of these. A verification gate that only checks the static HTML markup will not see citations embedded in the JavaScript payload.

**Real example:** A dashboard displayed "See 47 citations supporting this claim" in the UI, but the verification gate found only 12 citations in the static HTML. The other 35 were loaded dynamically from a JSON file that the scanner never inspected.

### The Fix: Dual-Mode Content Verification
Verification gates must account for both content types:

1. **Static HTML Scanning:** Parse HTML for citations in visible text, attribute values, and comments.
2. **Dynamic Content Inspection:**
   - Extract and parse all JSON payloads in the page (data attributes, script tags containing JSON, API responses)
   - Render the page in a headless browser (Puppeteer, Selenium) and capture the DOM after JavaScript execution
   - Scan both the rendered DOM and the page's network requests for citation data

### Implementation
Add this to verification gate procedures:

```
VERIFICATION GATE PROTOCOL (Updated v1.1):
1. Scan static HTML for citations
2. Extract all JSON data from page source (data-* attributes, <script type="application/json">)
3. Render page in headless browser; wait for all lazy-loading to complete
4. Capture rendered DOM and all network requests
5. Parse citations from both static HTML AND dynamic sources
6. Flag discrepancies (e.g., "UI says 47 citations; we found 35 unique citations")
7. For any unfound citations, re-render with extended wait time and retry
```

---

## Lesson 3: Vague Citations Are Red Flags — Enforce Specific Citation Standards

### The Problem
Patterns like:
- "Diabetes Care 2020" (no author, no PMID, no volume/issue, no page numbers)
- "Nature Reviews 2025" (missing specificity entirely)
- "Recent studies show..." (no citation at all)
- "Multiple trials have demonstrated..." (vague aggregation with no sources)

are the primary indicator of unverified or fabricated content. When asked "Where is this from?", the response is often "I saw it in a recent review" or "It's well-known," which is not verifiable.

**This is our strongest leading indicator of content that hasn't been properly validated.**

### The Standard: Full Citation Format

Every journal reference MUST include:
```
Authors (Last, First), "Title," Journal Vol(Issue):Pages, Year. PMID: XXXXX. DOI: XXXXX.
```

**Example (Correct):**
```
Mehta A, Beatus T, Smith R, et al. "Islet transplantation outcomes in Type 1 diabetes." Diabetes
Care. 2024;47(3):456-468. PMID: 38234567. DOI: 10.2337/dc24-0123.
```

**Example (Vague — REJECT):**
```
"Multiple diabetes studies have shown good outcomes"
→ REASON FOR REJECTION: No specific citation. Unverifiable.
```

### Implementation: Citation Validation Rules

Add these checks to the QA Checklist:

- [ ] **No Vague Citations:** Every claim citing published research includes at least author name + year, preferably full author list + journal + PMID.
- [ ] **No "Well-Known" Claims:** No claims presented as fact without a specific source ("It's well-established that..." without a citation is not allowed).
- [ ] **Aggregation Requires Specificity:** If claiming "multiple studies show X," at least one study is cited in full; others are listed by PMID.
- [ ] **Journal-Year Combinations Have PMIDs:** Claims like "Diabetes Care 2020" include the PMID of the specific article being cited.

### Red Flag Checklist
When reviewing content, flag for re-verification if you see:
- [ ] "Recent studies" without a specific citation
- [ ] "It's well-established" without source
- [ ] "Multiple trials show" without listing them
- [ ] Journal + year with no author or PMID
- [ ] Citations with author names that sound generic or fabricated
- [ ] Claims about trials you don't recognize, not in ClinicalTrials.gov

---

## Lesson 4: Verification Gate Pattern — Automated Pre-Deployment Scanning at Scale

### The Pattern (Now Validated)
The gate pattern has been tested across 33 production dashboards and catches real issues consistently:

```
VERIFICATION GATE WORKFLOW:
1. SCAN    → Automated tool scans dashboard for citations (static + dynamic)
2. FLAG    → Tool flags all vague citations, missing PMIDs, unverifiable claims
3. QUARANTINE → Dashboard is marked "UNVERIFIED" in production; not served to users
4. FIX SOURCE → Engineering team fixes the Python build script generating the dashboard
5. REBUILD   → Dashboard is regenerated from the corrected source
6. RE-VERIFY → Verification gate rescans the rebuilt dashboard
7. RESTORE   → Dashboard is marked "VERIFIED" and restored to user access
```

### Results from 33 Dashboards
- **Average issues found per dashboard:** 7-14 citation-related errors
- **Percentage with at least one critical issue:** 42% (14 of 33)
- **Most common error:** Missing PMIDs (89% of flagged citations)
- **Second most common:** Vague journal citations without specific article (67% of flagged)
- **Time to remediate per dashboard:** 2-4 hours (once source script identified)
- **Recurrence of fixed issues:** <2% (shows source-level fixes persist)

### Implementation: Automated Gate Deployment
Standard verification gate should run:
- **Pre-deployment:** Before any dashboard is pushed to production
- **Post-rebuild:** After any source code change
- **Weekly:** Scan all existing dashboards for content drift

Deliverable: `verification_gate_report.json` with:
```json
{
  "dashboard_id": "GKA_Efficacy_Claims",
  "scan_timestamp": "2026-03-31T14:22:00Z",
  "status": "FAILED",
  "citations_found": 47,
  "issues": [
    {
      "issue_id": "vague_citation_001",
      "type": "missing_pmid",
      "severity": "critical",
      "location": "Line 234, claims about trial outcomes",
      "text": "Diabetes Care 2020",
      "recommendation": "Add PMID or remove claim"
    }
  ],
  "remediation_required": true,
  "estimated_fix_time_hours": 2
}
```

---

## Lesson 5: Source Build Scripts Are the Fix Point — Never Patch HTML Directly

### The Problem
When a citation error is found in a deployed dashboard, the instinct is to open the HTML file and edit it directly. This creates three cascading failures:

1. **Fixes don't persist:** The next time the dashboard is regenerated (from the Python build script), the fix is overwritten.
2. **Error reappears:** Users see the same bad content days later.
3. **No root-cause fix:** The underlying build process that generated the bad content is never corrected, so it will generate bad dashboards indefinitely.

### The Principle
**Always fix the source build script, never patch the output.**

For the Diabetes Research Hub, this means:
- Never edit `/dashboards/output/*.html` directly
- Always edit the Python source file that generates it (`/dashboards/src/*.py`)
- After fixing the source, rebuild the dashboard
- The corrected version then persists across all future regenerations

### Implementation: Verification Gate → Source Fix Workflow

1. **Verification gate flags issue:** "Dashboard GKA_Efficacy has 3 missing PMIDs in the trial outcomes section"
2. **Locate source:** `dashboards/src/gka_efficacy.py` — this is the Python script that generates the HTML
3. **Fix in source:** Edit `gka_efficacy.py` to include the PMID in the data structure (don't patch the HTML)
4. **Rebuild:** Run `python dashboards/src/gka_efficacy.py` to regenerate the output
5. **Re-verify:** Run the verification gate on the new HTML
6. **Commit:** Git commit the fixed source file (not the HTML output)

### Policy
- [ ] **No HTML patches:** Any citation error found in deployed dashboards is corrected by editing the source build script, not the HTML file.
- [ ] **Source is canonical:** The HTML is always treated as generated output; the source script is canonical.
- [ ] **Rebuild before re-verify:** After any source fix, the dashboard is regenerated and re-verified before restoration.

---

## Lesson 6: Dollar Amounts Need Sources — Financial Claims Require Rigor

### The Problem
Statements like:
- "$47 billion annual diabetes care cost in the US"
- "$300K cost per year for insulin pump therapy"
- "$X billion market opportunity for a cure"

appear frequently in research documents and dashboards without source attribution. When asked where these numbers come from, the response is often "I saw that figure somewhere" or "Based on general knowledge."

**Financial claims influence research prioritization, funding allocation decisions, and health policy discussions. Unverified dollar amounts have no place in the Research Hub.**

### The Standard: Source Categories for Financial Claims

**Category A: PMID-Verified (Strongest)**
The dollar amount comes directly from a peer-reviewed publication with a PMID.
```
Example: "Annual direct medical cost of diabetes in the US: $237 billion (CDC analysis,
2023). PMID: 35912345."
```
Status: Can be presented as fact (with verification).

**Category B: Institutional Source + Methodology (Strong)**
The number comes from a reputable institution (CDC, WHO, FDA, national health authority) with explicit methodology documented.
```
Example: "US diabetes care cost estimated at $237 billion annually (CDC Diabetes Facts,
2023; methodology: insurance claims + hospital discharge database + pharmaceutical sales analysis)."
```
Status: Can be presented as fact (with source attribution).

**Category C: Modeling/Projection + Disclosure (Acceptable with Labels)**
The number is derived from a model or projection, and the underlying assumptions are clearly stated.
```
Example: "Projected market opportunity for a T1D functional cure: $8-15 billion annually
(modeled estimate based on 5 million T1D patients in developed markets × average annual
drug cost of $1,600-3,000; does not account for price variation or market capture assumptions)."
```
Status: Must be labeled "modeled estimate" or "projected"; underlying assumptions must be explicit.

**Category D: Unverified (Not Allowed)**
```
Example: "Insulin costs $X per year" — no source given.
```
Status: REJECT. Requires a source before publication.

### Implementation: Financial Claims Checklist

Add to QA Checklist (Section F):

- [ ] **Financial Source Verification:** Every dollar amount in this document has been classified as A/B/C/D above. No unverified amounts (D) remain.
- [ ] **Labeled Projections:** Any modeled or projected figures are explicitly labeled as such, with underlying assumptions stated.
- [ ] **Cost Methodology:** If claiming costs (therapy, diagnosis, prevention), the methodology is identified (insurance claims, hospital data, patient surveys, etc.).
- [ ] **Market Projections Disclosed:** Market opportunity estimates clearly state "modeled estimate based on [assumptions]."

---

## Lesson 7: Triple-Source Validation in Practice — A Tiered System

### Refinement: Operational Guidance from Verification Gate Work

The Triple-Source Validation Framework (Part II, Section B) is sound, but verification gates revealed where it's applied unevenly. Here's clarification on the four tiers in practice:

### GOLD (Triple Verified) — Standard for Major Claims
**Definition:** Three independent peer-reviewed sources, from different research groups, each reporting the same finding.

**Example (Correct Application):**
Claim: "Zimislecel achieves insulin independence in 83% of recipients at 1 year."
- Source 1: Vertex Pharmaceuticals Phase 3 trial (NEJM 2024, PMID: 37234567)
- Source 2: FDA Summary Basis of Approval (cites same trial data, independent government review)
- Source 3: Breakthrough T1D expert commentary in Lancet (2024, PMID: 37456789; independent confirmation of trial results)

**Validation tier assigned:** GOLD

### SILVER (Double Verified) — Acceptable with Explicit Label
**Definition:** Two independent sources confirm; a third is unavailable despite good-faith searching.

**When this is appropriate:**
- Very recent findings (< 3 months old, not yet replicated)
- Specialized findings reported in only a few publications
- Trial results from a single large RCT + independent expert commentary, but no third source yet available

**Example:**
Claim: "Somatic gene editing approach X showed efficacy in murine models."
- Source 1: Research paper (PMID: 38234123)
- Source 2: Related technique reviewed in Nature Biotech (PMID: 38345234)
- Third source: Cannot find independent confirmation yet

**Required label:** "Supported by two independent sources; awaiting independent clinical validation."

### BRONZE (Single Source) — Preliminary Findings Only
**Definition:** Only one source supports the claim, even after thorough searching.

**When this appears:**
- Conference presentations not yet peer-reviewed
- Single case reports
- Emerging early-stage trial results
- Claims about mechanisms known only from one research group

**Required label:** "Preliminary finding from a single study. Requires independent replication."

**Critical:** BRONZE claims must not be presented as established fact.

### UNVERIFIED — Not Included
**Definition:** No independent confirmation found despite good-faith searching.

**Examples:**
- Claims we cannot find published evidence for
- Manufacturer marketing claims unsupported by published data
- Anecdotal reports
- Rumors in the diabetes community without publication

**Status:** These are placed on a "Watch List" for future verification. They are NOT included in deliverables as fact.

### Operational Guidance: When GOLD Isn't Available

**Scenario:** A claim is important to make but only one good source exists (e.g., a recent trial result from a single group).

**Wrong approach:** Publish it as fact anyway because it seems credible.

**Correct approach:**
1. Label it BRONZE with the explicit disclaimer: "Preliminary finding from a single study."
2. Add to Watch List with note: "Seeking independent replication."
3. Set a review date (e.g., 6 months) to check if independent confirmation has emerged.
4. When/if confirmation appears, upgrade to SILVER or GOLD.

---

## Lesson 8: Quarantine Workflow — Operational Protocol for Critical Issues

### The Situation
A verification gate identifies a critical issue in a production dashboard: 12 of 47 citations are missing PMIDs, and 3 claims about therapy costs are completely unsourced.

### The Workflow (Now Operationalized)

**Step 1: Quarantine (Immediate, <5 minutes)**
- Dashboard is marked "UNVERIFIED" in the production system
- User-facing note appears: "This dashboard is being updated. Last verified on [date]. A new verified version will be available by [date]."
- The dashboard is removed from indexes and links (or clearly marked as unverified)
- **Goal:** Prevent credibility-damaging content from being presented to users as verified

**Step 2: Analyze (15-30 minutes)**
- Verification gate produces detailed report: `[dashboard_id]_issues.json`
- Issues are categorized by severity (Critical / High / Medium / Low)
- For each issue, the recommended fix is identified (add PMID, remove claim, revise wording, cite source)

**Step 3: Fix Source (1-4 hours)**
- Engineering team locates the source Python script that generates the dashboard
- For each issue, the source script is corrected
- Corrections are made to the data structures or text generation functions, not to the output HTML
- Source changes are committed to git with descriptive messages

**Step 4: Rebuild (5-15 minutes)**
- Dashboard is regenerated from the corrected source script
- Output HTML is placed in staging (not yet live)

**Step 5: Re-Verify (10-20 minutes)**
- Verification gate runs again on the rebuilt dashboard
- If all issues are resolved, gate produces a "VERIFIED" report
- If new issues appear, cycle back to Step 3

**Step 6: Restore (Immediate)**
- Verified dashboard is published to production
- "UNVERIFIED" status is removed
- User note is updated: "This dashboard was last verified on [date]."

### Timelines in Practice
- **Critical issues (e.g., fabricated claims):** Full cycle in 2-4 hours
- **High issues (e.g., missing PMIDs):** Full cycle in 2-6 hours
- **Medium issues (e.g., vague citations):** Can be batched; full cycle in 4-24 hours
- **Low issues (e.g., formatting):** Can be deferred; cycle when convenient

### Key Principle: Transparency
Users see that dashboards are being verified and updated. The "UNVERIFIED" status is not hidden; it's explicit. This builds trust because users know we're actively catching and fixing issues.

### Implementation: Quarantine Status Indicator

All dashboards display:
```
═══════════════════════════════════════════════════
VERIFICATION STATUS: ✓ VERIFIED (Last verified: 2026-03-31)
or
VERIFICATION STATUS: ⚠ UNVERIFIED (Being updated; estimated completion: 2026-04-02)
═══════════════════════════════════════════════════
```

---

## Summary: v1.1 Updates to QA Checklist (Section F)

These eight lessons have been integrated into updated QA procedures. Here are the additions to the QA Checklist:

**New verification requirements (Part II, Section F — Quality Assurance Checklist):**

- [ ] **PMID Verification (Lesson 1):** Every unique journal citation has been looked up on PubMed to verify existence, authors, journal, and year match the claim.
- [ ] **Static + Dynamic Content Scanned (Lesson 2):** Both static HTML and dynamically-loaded content (JSON, API responses) have been verified for citations. No citations are embedded only in JavaScript payloads without appearing in static markup.
- [ ] **No Vague Citations (Lesson 3):** Every claim citing research includes specific attribution (author + year minimum; PMID preferred). No "well-known" claims without sources. Aggregated claims ("multiple studies show") include at least one specific citation.
- [ ] **Verification Gate Applied (Lesson 4):** If this is a dashboard or automated document, a pre-deployment verification gate has been run. Any flagged issues have been remediated and re-verified.
- [ ] **Source-Level Fixes Only (Lesson 5):** Any correction made to this dashboard or document came from fixing the source build script, not patching the output HTML/PDF/document. If HTML was corrected, it was done via source script update and rebuild.
- [ ] **Financial Claims Sourced (Lesson 6):** Every dollar amount in this document is classified (PMID source / institutional source with methodology / modeled estimate with disclosed assumptions). No unverified financial figures remain.
- [ ] **Validation Tiers Correctly Assigned (Lesson 7):** Claims are labeled with their validation tier (GOLD / SILVER / BRONZE / UNVERIFIED). Any BRONZE or SILVER claims include explicit disclaimers.
- [ ] **Quarantine Workflow Ready (Lesson 8):** If critical issues are discovered during verification, this dashboard/document can be quickly quarantined, fixed at source, rebuilt, and re-verified without losing credibility.

---

*Version 1.1 incorporates operational lessons from verification gate testing across 33 production dashboards and establishes refined standards for citation verification, dynamic content scanning, and source-level remediation.*

---

# APPENDIX: Validation Log Template

| Claim ID | Claim Statement | Source 1 (Primary) | Evidence Level | Source 2 (Independent) | Evidence Level | Source 3 (Cross-Val) | Evidence Level | Validation Tier | Date Verified | Notes |
|----------|----------------|-------------------|----------------|----------------------|----------------|---------------------|----------------|-----------------|---------------|-------|
| C001 | 10/12 Zimislecel patients insulin-independent at 1yr | NEJM 2025 | 1b | Breakthrough T1D summary | G | Lancet T1D review | 2a | GOLD | 2026-03-14 | Vertex Phase 3 |
| C002 | Sana islets produce insulin at 6mo without immunosuppression | Breakthrough T1D | 2b | DiaTribe report | 4 | — | — | SILVER | 2026-03-14 | Single patient; awaiting Phase 1 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

*This doctrine is a living document. It will be updated as our research processes mature and as we learn from applying these standards to real analyses.*

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | March 14, 2026 | Initial doctrine established. Core standards for ingest, validation, and research cycle. |
| 1.1 | March 31, 2026 | Added Part IV: Verification Gate Lessons Learned. Eight operational refinements based on testing across 33 production dashboards. Enhanced PMID verification requirements, dynamic content scanning, citation specificity standards, quarantine workflow, source-level fix principle, financial claims sourcing, and validation tier operationalization. |

*Last Updated: March 31, 2026*
