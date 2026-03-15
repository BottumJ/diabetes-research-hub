# Diabetes Research Hub — Research Doctrine
**Version 1.0 | Established March 14, 2026**
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

# APPENDIX: Validation Log Template

| Claim ID | Claim Statement | Source 1 (Primary) | Evidence Level | Source 2 (Independent) | Evidence Level | Source 3 (Cross-Val) | Evidence Level | Validation Tier | Date Verified | Notes |
|----------|----------------|-------------------|----------------|----------------------|----------------|---------------------|----------------|-----------------|---------------|-------|
| C001 | 10/12 Zimislecel patients insulin-independent at 1yr | NEJM 2025 | 1b | Breakthrough T1D summary | G | Lancet T1D review | 2a | GOLD | 2026-03-14 | Vertex Phase 3 |
| C002 | Sana islets produce insulin at 6mo without immunosuppression | Breakthrough T1D | 2b | DiaTribe report | 4 | — | — | SILVER | 2026-03-14 | Single patient; awaiting Phase 1 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

*This doctrine is a living document. It will be updated as our research processes mature and as we learn from applying these standards to real analyses.*

*Version 1.0 — March 14, 2026*
