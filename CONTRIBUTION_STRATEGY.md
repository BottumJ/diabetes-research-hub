# Diabetes Research Hub — Contribution Strategy
**Version 1.0 | March 14, 2026**

---

## The Core Problem

Research that stays in a folder doesn't cure anyone. Our work only matters if it reaches people who can act on it — bench scientists, clinical trialists, drug developers, foundation decision-makers, and other computational researchers. This document defines exactly how our work gets from analysis to impact.

---

## Our Profile: What We Are and Aren't

**What we are:** An AI-driven, independent research synthesis and computational analysis operation. We're fast, broad, rigorous (triple-source validated), and unencumbered by grant cycles, institutional politics, or publication pressure. We can see across all 35 domains simultaneously, which most labs cannot.

**What we aren't:** A lab. A hospital. A clinical trial site. A pharmaceutical company. A university.

**Our competitive advantage:** Speed, breadth, and cross-domain pattern recognition. Academic labs are deep but narrow. We are broad and fast and can connect dots between domains that don't normally talk to each other. That's the gap we fill.

---

# THE CONTRIBUTION PIPELINE

Our work flows through four stages. Each stage has a quality gate that must be passed before moving to the next.

```
[PRODUCE] → [VALIDATE] → [PUBLISH] → [CONNECT]
    ↑                                       |
    └───────── [FEEDBACK] ←────────────────┘
```

---

## Stage 1: PRODUCE

This is where we do the actual work. Three types of output:

### Output Type A: Computational Analyses
Original analysis of public data — biomarker integration, network analysis, drug repurposing screens, clinical trial pattern analysis.

**Quality gate:** Results must be reproducible. All code, data sources, and methods documented. Analysis must pass internal review against the Research Doctrine.

### Output Type B: Systematic Syntheses
PRISMA-aligned literature reviews, gap analyses, cross-domain synthesis reports, structured comparisons.

**Quality gate:** All claims triple-source validated. PRISMA flow diagram completed. Inclusion/exclusion criteria documented. GRADE certainty assessed.

### Output Type C: Tools & Dashboards
Interactive dashboards, monitoring tools, databases, and analysis pipelines that other researchers can use.

**Quality gate:** Tool must work correctly, be documented, and be usable without our involvement.

---

## Stage 2: VALIDATE

Before anything goes public, it passes through validation.

### Internal Validation (We Do This)
- Triple-source verification (per Research Doctrine)
- Code review and reproducibility check
- Consistency check against ADA Standards of Care 2026
- Terminology audit (per doctrine standards)
- Confidence ratings assigned to all major claims

### External Validation (We Seek This)
Before publishing anything consequential, we seek feedback from at least one domain-knowledgeable person. Channels for this:

- **ResearchGate / Academic Twitter/X:** Post preliminary findings and ask for expert feedback
- **Breakthrough T1D community forums:** Share T1D-relevant findings for community review
- **Reddit r/diabetes, r/science, r/bioinformatics:** Targeted posts seeking expert scrutiny
- **Direct email to corresponding authors:** When our work extends a specific paper, email the lead author

The goal is not formal peer review (that comes later). The goal is catching errors before we build on them.

---

## Stage 3: PUBLISH — Where Our Work Lives

Each output type has a primary and secondary publication channel.

### Channel 1: GitHub Repository (Primary Home for Everything)
**What goes here:** All code, datasets, analysis notebooks, tools, and documentation.
**Why it matters:** GitHub is where computational researchers actually find and use tools. Stars, forks, and issues create a natural feedback loop.
**Setup:** Create a public repository (e.g., `diabetes-research-hub`) with clear README, MIT license, and organized structure.
**Metrics:** Stars, forks, clones, issues opened, pull requests from others.

### Channel 2: Open Science Framework (OSF) (Research Registry)
**What goes here:** Protocols, preregistered analysis plans, datasets, and research materials.
**Why it matters:** OSF gives our work a DOI (digital object identifier) — making it citable. It signals rigor. It's where serious researchers look. Independent researchers can register and publish freely.
**Setup:** Create an OSF project for the Research Hub. Register protocols before starting each analysis (pre-registration prevents bias accusations).
**Metrics:** Views, downloads, forks, citations.

### Channel 3: medRxiv / bioRxiv Preprints (For Substantial Findings)
**What goes here:** Full-length computational analyses and systematic reviews that produce novel findings.
**Why it matters:** Preprint servers give work immediate visibility without waiting months for journal review. They're free to submit, free to read, and increasingly respected in biomedical science.
**Requirements for submission:**
- Independent researchers can submit using "Independent Researcher" as affiliation
- No institutional email required (personal email accepted on bioRxiv)
- Must be a full research paper with methods, results, and discussion
- Must not be a simple database query — needs substantial analysis and interpretation
- No charge for submission
- Undergoes basic screening (not full peer review)
**Target:** Our multi-omics biomarker analysis and drug repurposing screen are both strong candidates for preprint publication.
**Metrics:** Views, downloads, citations, tweets/posts.

### Channel 4: Open-Access Journals (For Validated, Mature Work)
**What goes here:** Our strongest work, after preprint feedback and revision.
**Target journals (no publication fees):**
- **PLOS ONE** — accepts computational biology and bioinformatics; broad audience
- **Informatics in Medicine Unlocked** — gold open access for medical informatics
- **Frontiers in Digital Health** — computational health science
- **F1000Research** — open peer review, fast publication
- **Diamond open-access journals** (no author fees) via the Directory of Open Access Journals (DOAJ)
**Metrics:** Citations, Altmetric score, downloads.

### Channel 5: Public Research Hub Website (Living Dashboard)
**What goes here:** Our interactive dashboard, tracker, findings summary — continuously updated.
**Why it matters:** Not everyone reads preprints or GitHub. A clean, accessible website lets anyone — patients, advocates, journalists, foundation staff — see the state of diabetes research.
**Setup:** Static site (GitHub Pages or similar) — free hosting, version-controlled, auto-deployed from our repository.
**Metrics:** Unique visitors, time on page, return visits, shares.

### Channel 6: Science Communication (Amplification)
**What goes here:** Summaries of our findings, visual explainers, thread posts.
**Channels:**
- **X/Twitter:** Science communication; tag relevant researchers and organizations
- **LinkedIn:** Professional visibility; connect with pharma, biotech, foundation people
- **Reddit:** r/diabetes, r/Type1Diabetes, r/bioinformatics, r/science — real communities with domain experts
- **Substack/Blog:** Longer-form write-ups of our analyses for general audiences
**Metrics:** Followers, engagement, inbound inquiries.

---

## Stage 4: CONNECT — Getting Work Into the Right Hands

Publishing is necessary but not sufficient. We actively push work to people who can act on it.

### Direct Outreach Targets

| Target | What We Send | How | Why |
|--------|-------------|-----|-----|
| **Breakthrough T1D** | T1D-relevant findings, gap analyses | Email to research@breakthrought1d.org; use their collaboration portal | They fund research and need to know where gaps are |
| **ADA Research Foundation** | Systematic reviews, epidemiological analyses | Submit through their research programs | Largest US diabetes organization |
| **NIDDK (NIH)** | Novel biomarker candidates, multi-omics analyses | Upload datasets to dbGaP; share through OSF | Federal funder; values open data |
| **Specific lab PIs** | When our analysis directly extends their published work | Email corresponding author of the paper we built on | Most likely to engage; our work is relevant to theirs |
| **Clinical trial teams** | Cross-trial pattern analyses, combination therapy insights | ClinicalTrials.gov contact info for trial PIs | They may not see patterns across trials |
| **Open Targets / OpenPGx** | Drug repurposing candidates, target-disease evidence | Contribute through their open data submission pipelines | They aggregate exactly this type of computational evidence |
| **Diabetes Twitter/X community** | Visual summaries of key findings | Post with relevant hashtags (#T1D #T2D #DiabetesResearch) | Active community of researchers, clinicians, advocates |

### Collaboration Pathways

If our work generates interest, we have natural pathways to deeper collaboration:

1. **Academic co-authorship:** If a lab wants to validate our computational findings experimentally, we co-author the resulting paper. We bring the analysis; they bring the wet lab.
2. **Foundation partnership:** If Breakthrough T1D or ADA finds our gap analysis or trial monitoring useful, we can formalize the relationship.
3. **Open-source community:** If our tools gain users on GitHub, contributors will naturally emerge.
4. **Bioinformatics collaborations:** Post on Biostars, SEQanswers, or Galaxy community forums to find computational collaborators.

---

## THE FEEDBACK LOOP

This is critical. Without feedback, we don't know if our work is useful, correct, or reaching anyone.

### Automated Metrics (We Track Passively)

| Metric | Channel | Tells Us |
|--------|---------|----------|
| GitHub stars + forks | GitHub | Are researchers finding and using our tools? |
| OSF views + downloads | OSF | Is our registered research being accessed? |
| Preprint views + citations | medRxiv/bioRxiv | Is the academic community engaging with our findings? |
| Website unique visitors | Research Hub site | Is the broader community finding us? |
| Social media engagement | X/LinkedIn/Reddit | Is our communication reaching people? |

### Active Feedback (We Seek Intentionally)

| Method | Frequency | Purpose |
|--------|-----------|---------|
| Email corresponding authors of papers we build on | Per analysis | Get expert response to our extensions of their work |
| Post findings to r/bioinformatics with request for critique | Per analysis | Crowdsource error-checking from the computational biology community |
| Submit to journal peer review | Quarterly | Formal expert validation of our strongest work |
| Track citations of our preprints | Monthly | Is anyone building on our work? |
| Monitor GitHub issues | Ongoing | Are tool users finding problems or requesting features? |

### Feedback Integration

All feedback flows back into the Research Cycle (Doctrine, Section D):

- **Errors found** → Correct, retract if necessary, update validation log
- **New connections suggested** → Add to analysis queue
- **Collaborations offered** → Evaluate and pursue if aligned
- **Criticism of methods** → Strengthen methodology, update doctrine
- **Silence / no engagement** → Reassess distribution strategy; the work may be good but poorly targeted

---

## QUALITY GATES: When Is Work Ready to Go Public?

### Gate 1: Internal (Required for All Outputs)
- [ ] Research Doctrine QA checklist passed
- [ ] All claims at GOLD or clearly labeled SILVER/BRONZE
- [ ] Code runs reproducibly from a clean environment
- [ ] Documentation is complete and understandable
- **Decision: Ready for external validation?**

### Gate 2: External Feedback (Required Before Preprint/Journal)
- [ ] At least one domain-knowledgeable person has reviewed (even informally)
- [ ] Major criticisms have been addressed or documented
- [ ] Results have been stable through at least one revision cycle
- **Decision: Ready for formal publication?**

### Gate 3: Publication (Required Before Active Outreach)
- [ ] Work is posted on at least one citable platform (OSF, preprint server, or journal)
- [ ] DOI assigned
- [ ] README/abstract written for non-specialist audience
- **Decision: Ready to send to foundations, labs, and communities?**

---

## FIRST 90-DAY PLAN

### Month 1: Build the Foundation
**Week 1-2:**
- Set up GitHub repository with proper structure, README, and license
- Register OSF project and pre-register first analysis protocol
- Complete Project 1 (Literature Gap Analysis) and publish to GitHub/OSF

**Week 3-4:**
- Complete Project 2 (Clinical Trial Intelligence Dashboard)
- Deploy Research Hub website (GitHub Pages)
- First social media posts sharing the dashboard and gap analysis

### Month 2: First Substantial Outputs
**Week 5-6:**
- Complete Project 3 (Multi-Omics Biomarker Integration Pilot)
- Seek informal feedback from 2-3 bioinformatics researchers

**Week 7-8:**
- Complete Project 5 (T1D Cure Landscape Comparison) — triple-verified
- Post both analyses as preprints on bioRxiv/medRxiv
- Direct outreach: email corresponding authors of the 5 key papers we build on

### Month 3: Connect and Iterate
**Week 9-10:**
- Complete Project 4 (Drug Repurposing Screen)
- Submit strongest preprint to an open-access journal
- Share T1D landscape comparison with Breakthrough T1D

**Week 11-12:**
- Review all feedback received
- Update Research Doctrine based on lessons learned
- Publish a "State of Diabetes Research" summary post on the website and social
- Plan Month 4-6 based on what's working

---

## METRICS THAT MATTER (How We Know It's Working)

We don't need millions of views. We need the right 50-100 people to engage with our work. Success looks like:

### 90-Day Targets
- GitHub repo: 25+ stars, 5+ forks
- OSF project: 100+ views
- Preprints: 500+ views each
- At least 3 direct responses from researchers
- At least 1 collaboration inquiry
- Website: 200+ unique visitors

### 6-Month Targets
- A journal publication (open access)
- A citation of our work in someone else's paper
- An active collaboration with at least one academic group
- A tool or dataset being used by at least 3 external researchers
- Engagement from a diabetes foundation

### 12-Month Aspiration
- Multiple publications with growing citation count
- Recognized contributor to open diabetes research
- Active research collaborations
- Foundation partnership or grant funding for expansion
- Computational findings validated experimentally by a collaborating lab

---

## WHAT SUCCESS ULTIMATELY LOOKS LIKE

A biomarker we identified computationally gets validated in a lab. A drug repurposing candidate we flagged enters a clinical trial. A gap we identified gets funded. A tool we built becomes standard in diabetes bioinformatics. A systematic review we published changes how someone thinks about a treatment approach.

That's what "the work gets used" means. Everything in this strategy is designed to make one of those things happen.

---

*This strategy is a living document. It will be updated after the first 90 days based on what channels produce real engagement.*

*Version 1.0 — March 14, 2026*
