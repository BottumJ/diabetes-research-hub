# Research Plan: Islet Transplant × Drug Repurposing Computational Screening
**Gap #3 from Literature Gap Analysis | Gap Score: 100.0 | Joint Publications: 0**
**Tier 1 Alignment:** Drug Repurposing Computational Screening (Score 18/20)
**Date:** 2026-04-03
**Status:** PROPOSED — Requires review before execution

---

## 1. Problem Statement

Islet transplantation is a promising treatment for T1D, but graft survival depends on lifelong immunosuppression with significant side effects. Our gap analysis found **zero joint publications** at the intersection of Islet Transplant and Drug Repurposing — despite the obvious potential for existing approved drugs to protect islets through alternative mechanisms. This plan outlines a purely computational screening approach to identify repurposing candidates.

**Research question:** Which FDA-approved drugs have mechanisms of action that could protect transplanted islets from immune rejection or improve graft survival, beyond the standard immunosuppressive regimen?

---

## 2. Prior Work (What's Already Been Done)

The web research identified several existing computational repurposing efforts in adjacent areas — these inform our approach but none directly address our gap:

| Study | Approach | Finding | Gap Remaining |
|-------|----------|---------|---------------|
| JAK inhibitor repurposing (Science Advances) | Computational target analysis | Baricitinib preserves beta cell function in T1D | Focused on native beta cells, not transplanted islets |
| CXCR3 targeting (PMID 16898223, 18622291) | Chemokine receptor pathway mapping | Anti-CXCR3 antibodies prolong islet allograft survival | Not drug repurposing — novel biologics |
| EZH2 inhibitor repurposing | FDA drug screening | GSK126, tazemetostat promote beta-like cell regeneration | Regeneration, not graft protection |
| Islet microenvironment proteomics (PMC7483621) | Longitudinal proteomics | Identified biomarkers for rejection stages | Targets identified but not mapped to drugs |
| Adenosine kinase inhibitors | Screening | Induce beta cell replication across species | Replication, not immune protection |

**Our unique contribution:** Systematic mapping of ALL approved drugs against islet graft rejection targets using network pharmacology — filling the zero-publication gap.

---

## 3. Data Sources & Access

### Tier 1: Immediately Available (Free, No Application)

| Source | What We Get | Access Method | Status |
|--------|------------|---------------|--------|
| **OpenTargets Platform** | Target-disease associations for graft rejection, autoimmunity, beta cell biology | GraphQL API (`api.platform.opentargets.org/api/v4/graphql`) | Free, documented |
| **STRING Database** | Protein-protein interactions for islet-relevant pathways (TGF-beta, MAPK, VEGF signaling) | REST API (`string-db.org/api`) | Free, no auth |
| **PubChem** | Drug structures, bioactivity data, target annotations | REST API | Free |
| **ChEMBL** | Bioactivity measurements, target-drug associations | REST API | Free |
| **UniProt** | Protein function annotations for target characterization | REST API | Free |

### Tier 2: Requires Application (Free for Academic Use)

| Source | What We Get | Access Method | Status |
|--------|------------|---------------|--------|
| **DrugBank** | Comprehensive drug-target mappings for all FDA-approved drugs | Academic license (application required) | Apply at go.drugbank.com/academic_research |

### Tier 3: Supplementary

| Source | What We Get | Access Method |
|--------|------------|---------------|
| **Reactome** | Curated biological pathway data | Free API |
| **Human Protein Atlas** | Tissue expression data (islet-specific expression) | Free download |
| **ClinicalTrials.gov** | Active trials using repurposed drugs in transplant | Already monitored by our scripts |

---

## 4. Methodology

### Phase 1: Target Identification (Week 1-2)

**Goal:** Build a comprehensive list of protein targets involved in islet graft rejection and protection.

**Steps:**
1. Query OpenTargets for targets associated with: "graft rejection", "allograft rejection", "islet transplantation", "beta cell apoptosis", "immune tolerance"
2. Query STRING for protein interaction networks around key seed targets: CXCR3, ICAM-1, TNF-alpha, IL-1beta, FAS/FASL, PD-L1
3. Expand network to include islet-specific survival pathways: insulin signaling, GLP-1R pathway, beta cell identity genes (PDX1, NKX6.1, MAFA)
4. Filter by druggability score from OpenTargets tractability data

**Output:** Curated target list (estimated 50-200 targets) with evidence scores and druggability ratings.

**Python tools:** `requests` (API queries), `networkx` (network construction), `pandas` (data management)

### Phase 2: Drug-Target Mapping (Week 2-3)

**Goal:** Map all FDA-approved drugs to the target list from Phase 1.

**Steps:**
1. Query DrugBank (or ChEMBL if DrugBank application pending) for all drugs targeting proteins in our network
2. Filter to FDA-approved drugs only (repurposing requires existing approval)
3. Annotate each drug with: mechanism of action, current indications, known side effects, route of administration
4. Score drug-target associations by: binding affinity, selectivity, known in-vivo activity

**Output:** Drug-target matrix mapping ~2,000+ approved drugs against our islet protection targets.

### Phase 3: Network Pharmacology Analysis (Week 3-4)

**Goal:** Identify drugs with multi-target activity across the islet protection network.

**Steps:**
1. Build bipartite drug-target network using NetworkX
2. Calculate network metrics: drug degree (how many targets hit), target betweenness centrality (pathway importance), module membership
3. Identify drugs hitting multiple high-centrality targets — these are the strongest repurposing candidates
4. Rank candidates by composite score: target count × target importance × drug safety profile
5. Cross-reference top candidates against known immunosuppressant side effects to identify candidates with FEWER side effects

**Output:** Ranked list of repurposing candidates with network pharmacology evidence.

**Python tools:** `networkx`, `rdkit` (chemical similarity), `matplotlib`/`seaborn` (visualization)

### Phase 4: Validation & Literature Check (Week 4-5)

**Goal:** Validate computational findings against existing evidence.

**Steps:**
1. For each top-10 candidate, search PubMed for any existing evidence of islet-relevant activity
2. Check ClinicalTrials.gov for any trials using the candidate in diabetes/transplant settings
3. Cross-reference with our existing paper library and gap analysis data
4. Assign evidence levels per Research Doctrine (most will be Level 4 or 5)
5. Flag candidates that have existing clinical evidence (Level 2b+) vs. purely computational (Level 4)

**Output:** Validated candidate list with evidence levels and confidence tags.

### Phase 5: Report & Dashboard (Week 5-6)

**Goal:** Produce a publishable-quality report and interactive dashboard.

**Steps:**
1. Write up methodology, results, and limitations following PRISMA-ScR guidelines
2. Build interactive HTML dashboard (add to existing Dashboards/ folder)
3. Generate network visualization of top candidates
4. Prepare supplementary data files for reproducibility

**Output:** Report + dashboard + data files.

---

## 5. Expected Deliverables

| Deliverable | Format | Location |
|-------------|--------|----------|
| Target list with evidence scores | JSON + CSV | Analysis/Results/ |
| Drug-target interaction matrix | JSON + XLSX | Analysis/Results/ |
| Network pharmacology results | JSON | Analysis/Results/ |
| Ranked candidate list | Markdown report | Analysis/Results/ |
| Interactive dashboard | HTML | Dashboards/ |
| Python analysis scripts | .py files | Analysis/Scripts/ |
| Methodology documentation | Markdown | Analysis/Results/ |

---

## 6. Technical Requirements

### Python Environment
```
networkx>=2.8
pandas>=1.5
requests>=2.28
matplotlib>=3.6
seaborn>=0.12
rdkit  # optional, for chemical similarity
openpyxl  # for Excel output
```

### API Access Needed
- OpenTargets GraphQL: No key needed
- STRING REST: No key needed
- ChEMBL REST: No key needed
- DrugBank: Academic license application (submit ASAP — variable turnaround)

### Compute Requirements
- Standard laptop sufficient
- No GPU needed
- Primary bottleneck: API rate limits (STRING: 1 request/second)

---

## 7. Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| DrugBank license delay | Medium | Use ChEMBL as primary source; DrugBank as supplementary |
| Too few druggable targets | Low | Expand seed targets to include broader immune pathways |
| API rate limiting | Medium | Implement caching and polite request intervals |
| Results are trivially obvious (e.g., "use tacrolimus") | Medium | Explicitly exclude current standard-of-care immunosuppressants; focus on novel mechanisms |
| Findings are not clinically actionable | Medium | This is expected — computational screening identifies candidates for wet-lab validation. Frame as hypothesis generation. |

---

## 8. Research Doctrine Compliance

| Requirement | How We Comply |
|-------------|---------------|
| Evidence levels | All findings labeled Level 4 (computational/mechanism-based) until validated |
| Source recording | All data sources, query parameters, and API versions documented |
| Reproducibility | All scripts saved to Analysis/Scripts/ with parameters |
| Confidence tags | Initial findings tagged "Unverified" per Doctrine |
| Limitations | Explicitly state: computational only, requires experimental validation |
| Triple-source validation | Pending — first source is this analysis; second/third require expert review |

---

## 9. Timeline

| Week | Phase | Key Milestone |
|------|-------|---------------|
| 1-2 | Target Identification | Target list finalized |
| 2-3 | Drug-Target Mapping | Drug matrix complete |
| 3-4 | Network Analysis | Candidate ranking done |
| 4-5 | Validation | Literature cross-check complete |
| 5-6 | Reporting | Dashboard and report published |

**Total estimated duration:** 6 weeks
**Can begin immediately:** Yes — Tier 1 data sources require no application

---

## 10. Next Step

**To begin Phase 1, run:**
```bash
python Analysis/Scripts/project_islet_drug_repurposing_phase1.py
```
*(Script to be created upon approval of this plan)*

---

*Prepared by Diabetes Research Hub | Research Doctrine v1.1*
*Gap Analysis Reference: Islet Transplant × Drug Repurposing — Gap Score 100.0, 0 joint publications*
