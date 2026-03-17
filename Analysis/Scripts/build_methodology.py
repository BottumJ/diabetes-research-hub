#!/usr/bin/env python3
"""
Build Methodology & Validation Framework Dashboard for Diabetes Research Hub
Generates a comprehensive Tufte-style HTML page explaining platform methodology,
validation framework, and research interpretation guidelines.

Usage:
    python3 build_methodology.py
"""

import os
from datetime import datetime

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
output_dir = os.path.join(base_dir, 'Dashboards')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'Methodology.html')

# Generate HTML content
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Methodology & Validation Framework - Diabetes Research Hub</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background-color: #fafaf7;
            color: #1a1a1a;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif;
            line-height: 1.7;
            padding: 0;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }

        header {
            margin-bottom: 2.5rem;
        }

        h1 {
            font-family: Georgia, serif;
            font-size: 2.2rem;
            font-weight: normal;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }

        .subtitle {
            color: #636363;
            font-size: 1rem;
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }

        h2 {
            font-family: Georgia, serif;
            font-size: 1.6rem;
            font-weight: normal;
            margin-top: 2rem;
            margin-bottom: 1rem;
            letter-spacing: -0.01em;
            border-top: 1px solid #e0ddd5;
            padding-top: 1.5rem;
        }

        h2:first-of-type {
            border-top: none;
            margin-top: 0;
            padding-top: 0;
        }

        h3 {
            font-family: Georgia, serif;
            font-size: 1.2rem;
            font-weight: normal;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }

        p {
            margin-bottom: 1rem;
            text-align: justify;
        }

        ul, ol {
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }

        li {
            margin-bottom: 0.75rem;
        }

        .tabs {
            display: flex;
            flex-wrap: wrap;
            border-bottom: 2px solid #e0ddd5;
            margin: 2rem 0 2rem 0;
            gap: 0;
        }

        .tab-button {
            padding: 0.75rem 1.25rem;
            border: none;
            background-color: transparent;
            color: #636363;
            cursor: pointer;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            font-size: 0.95rem;
            border-bottom: 3px solid transparent;
            transition: none;
            margin-bottom: -2px;
        }

        .tab-button:hover {
            color: #1a1a1a;
            border-bottom-color: #c0bdb5;
        }

        .tab-button.active {
            color: #1a1a1a;
            font-weight: 600;
            border-bottom-color: #1a1a1a;
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.2s ease-in;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0.8; }
            to { opacity: 1; }
        }

        .validation-tier {
            background-color: #ffffff;
            border-left: 4px solid #e0ddd5;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0;
        }

        .validation-tier.gold {
            border-left-color: #d4a056;
        }

        .validation-tier.silver {
            border-left-color: #a8a8a8;
        }

        .validation-tier.bronze {
            border-left-color: #8b6f47;
        }

        .validation-tier.review {
            border-left-color: #636363;
        }

        .tier-header {
            font-family: Georgia, serif;
            font-size: 1.1rem;
            font-weight: normal;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .tier-badge {
            display: inline-block;
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 0.25rem 0.5rem;
            background-color: #fafaf7;
            border: 1px solid #e0ddd5;
        }

        .tier-description {
            color: #636363;
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
        }

        .tier-examples {
            font-size: 0.9rem;
            color: #636363;
            margin-top: 0.5rem;
        }

        .pyramid {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 2rem;
            margin: 1.5rem 0;
            font-size: 0.9rem;
            line-height: 1.8;
            font-family: "SF Mono", Monaco, Consolas, monospace;
        }

        .pyramid-row {
            display: flex;
            gap: 1rem;
            margin-bottom: 0.75rem;
            align-items: center;
        }

        .pyramid-label {
            width: 120px;
            font-weight: 600;
        }

        .pyramid-bar {
            flex: 1;
            height: 40px;
            display: flex;
            align-items: center;
            padding: 0 1rem;
            color: white;
            font-weight: 500;
        }

        .pyramid-gold {
            background-color: #d4a056;
            width: 60%;
        }

        .pyramid-silver {
            background-color: #a8a8a8;
            width: 75%;
        }

        .pyramid-bronze {
            background-color: #8b6f47;
            width: 85%;
        }

        .pyramid-review {
            background-color: #636363;
            width: 90%;
        }

        .pyramid-count {
            width: 60px;
            text-align: right;
            color: #1a1a1a;
            font-weight: 600;
        }

        .section-box {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 1.5rem;
            margin: 1.5rem 0;
        }

        .methodology-list {
            background-color: #ffffff;
            border-left: 1px solid #e0ddd5;
            padding-left: 1.5rem;
            margin: 1rem 0;
        }

        .methodology-list li {
            margin-bottom: 1rem;
        }

        .code-example {
            background-color: #fafaf7;
            border: 1px solid #e0ddd5;
            padding: 1rem;
            margin: 1rem 0;
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            line-height: 1.5;
        }

        .citation-guide {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 1rem;
            margin: 1rem 0;
            font-size: 0.9rem;
        }

        .data-source-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
        }

        .data-source-table th,
        .data-source-table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #e0ddd5;
            font-size: 0.9rem;
        }

        .data-source-table th {
            background-color: #fafaf7;
            font-weight: 600;
            border-bottom: 2px solid #e0ddd5;
        }

        .data-source-table tr:last-child td {
            border-bottom: none;
        }

        .tool-name {
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-weight: 600;
            color: #1a1a1a;
        }

        .source-url {
            color: #2c5f8a;
            text-decoration: none;
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-size: 0.85rem;
        }

        .contribution-box {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 1.5rem;
            margin: 1rem 0;
        }

        .contribution-box h4 {
            font-family: Georgia, serif;
            font-size: 1rem;
            font-weight: normal;
            margin-bottom: 0.75rem;
        }

        .contribution-list {
            list-style-type: none;
            margin-left: 0;
        }

        .contribution-list li {
            margin-bottom: 0.75rem;
            padding-left: 1.5rem;
            position: relative;
        }

        .contribution-list li:before {
            content: "→";
            position: absolute;
            left: 0;
            color: #636363;
        }

        .link-group {
            background-color: #fafaf7;
            border: 1px solid #e0ddd5;
            padding: 1rem;
            margin: 1rem 0;
            font-size: 0.9rem;
        }

        .link-group strong {
            display: block;
            margin-bottom: 0.5rem;
        }

        .link-group a {
            color: #2c5f8a;
            text-decoration: none;
            display: block;
            margin-bottom: 0.5rem;
        }

        .link-group a:hover {
            text-decoration: underline;
        }

        footer {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e0ddd5;
            font-size: 0.8rem;
            color: #636363;
            text-align: center;
        }

        .footer-note {
            line-height: 1.6;
            margin-bottom: 1rem;
        }

        strong {
            font-weight: 600;
        }

        a {
            color: #2c5f8a;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .research-gap-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }

        .gap-card {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 1rem;
        }

        .gap-title {
            font-family: Georgia, serif;
            font-weight: normal;
            margin-bottom: 0.5rem;
        }

        .gap-validation {
            font-size: 0.8rem;
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-weight: 600;
            display: inline-block;
            padding: 0.2rem 0.4rem;
            background-color: #fafaf7;
            border: 1px solid #e0ddd5;
            margin-bottom: 0.5rem;
        }

        .gap-validation.gold {
            color: #d4a056;
            border-color: #d4a056;
        }

        .gap-validation.silver {
            color: #a8a8a8;
            border-color: #a8a8a8;
        }

        .gap-validation.bronze {
            color: #8b6f47;
            border-color: #8b6f47;
        }

        .gap-description {
            font-size: 0.9rem;
            color: #636363;
            line-height: 1.5;
        }

        .nav-bar {
            background: #ffffff;
            border-bottom: 1px solid #e0ddd5;
            padding: 8px 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 13px;
            display: flex;
            gap: 16px;
            align-items: center;
            flex-wrap: wrap;
        }

        .nav-bar a {
            color: #636363;
            text-decoration: none;
        }

        .nav-bar a:hover {
            text-decoration: underline;
        }

        .nav-bar a.home-link {
            color: #2c5f8a;
            font-weight: 600;
        }

        .nav-separator {
            color: #e0ddd5;
        }
    </style>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-JGMD5VRYPH');</script>
</head>
<body>
    <div class="nav-bar">
        <a href="../index.html" class="home-link">&larr; Diabetes Research Hub</a>
        <span class="nav-separator">|</span>
        <a href="Research_Dashboard.html">Research</a>
        <a href="Clinical_Trial_Dashboard.html">Trials</a>
        <a href="Gap_Deep_Dives.html">Gaps</a>
        <a href="Gap_Synthesis.html">Synthesis</a>
        <a href="Equity_Map.html">Equity</a>
        <a href="Medical_Data_Dictionary.html">Dictionary</a>
        <a href="Acronym_Database.html">Acronyms</a>
    </div>

    <div class="container">
        <header>
            <h1>Methodology & Validation Framework</h1>
            <p class="subtitle">
                Understanding how the Diabetes Research Hub identifies, validates, and presents research gaps.
                This dashboard explains our analytical approach, evidence standards, and how to interpret platform findings.
            </p>
        </header>

        <div class="tabs">
            <button class="tab-button active" onclick="switchTab('mission')">Mission & Purpose</button>
            <button class="tab-button" onclick="switchTab('validation')">Validation Framework</button>
            <button class="tab-button" onclick="switchTab('gap-identification')">Gap Identification</button>
            <button class="tab-button" onclick="switchTab('citations')">Citation Standards</button>
            <button class="tab-button" onclick="switchTab('data-sources')">Data Sources & Tools</button>
            <button class="tab-button" onclick="switchTab('contribute')">How to Contribute</button>
        </div>

        <!-- TAB 1: Mission & Purpose -->
        <div id="mission" class="tab-content active">
            <h2>Mission & Purpose</h2>

            <p>
                The Diabetes Research Hub is an open-source computational platform designed to accelerate diabetes research
                toward a cure by systematically identifying, validating, and synthesizing research gaps. Built by patients,
                for researchers and patients, the platform combines rigorous bibliometric analysis with clinical expertise
                to map the diabetes research landscape and highlight the most promising opportunities for intervention.
            </p>

            <h3>What We Do</h3>
            <p>
                We analyze peer-reviewed literature, clinical trial data, and public health information to identify
                research gaps—areas where scientific understanding is incomplete, funding is scarce, or evidence is
                insufficient to guide clinical practice. Each gap is validated against multiple independent sources
                and contextualized within the broader research ecosystem. Our analysis is transparent, reproducible,
                and available for citation.
            </p>

            <h3>What We Don't Do</h3>
            <p>
                <strong>This is not medical advice.</strong> The Diabetes Research Hub is not a clinical decision-support tool,
                patient education resource, or treatment guide. All analyses are computational research tools intended
                for researchers, students, policy makers, and patients seeking to understand the state of diabetes science.
                Always consult healthcare providers for medical decisions.
            </p>

            <h3>Core Principles</h3>
            <ul>
                <li>
                    <strong>Transparency:</strong> All claims are linked to peer-reviewed sources with PubMed IDs (PMIDs)
                    where available. Code, data structures, and methodology are openly available on GitHub.
                </li>
                <li>
                    <strong>Reproducibility:</strong> Our gap identification and validation processes are fully documented
                    and can be replicated by independent researchers. We provide data snapshots to enable comparative analysis.
                </li>
                <li>
                    <strong>Accessibility:</strong> The platform is free, uses no paywalled databases, and generates static HTML
                    dashboards that require no special software or subscriptions.
                </li>
                <li>
                    <strong>Citable:</strong> Each dashboard and data snapshot can be cited in academic work. We provide
                    suggested citations and BibTeX formats.
                </li>
                <li>
                    <strong>Equity-focused:</strong> We examine the geographic, demographic, and socioeconomic distribution
                    of research effort and identify underserved populations and regions.
                </li>
            </ul>

            <h3>Platform Links</h3>
            <div class="link-group">
                <strong>GitHub Repository:</strong>
                <a href="https://github.com/BottumJ/diabetes-research-hub" target="_blank">BottumJ/diabetes-research-hub</a>
                <strong>Open Science Framework:</strong>
                <a href="https://osf.io/hu9ga" target="_blank">https://osf.io/hu9ga</a>
            </div>
        </div>

        <!-- TAB 2: Validation Framework -->
        <div id="validation" class="tab-content">
            <h2>Triple-Source Validation Framework</h2>

            <p>
                At the core of the Diabetes Research Hub is a structured validation framework that categorizes research gaps
                by the strength and independence of supporting evidence. This framework balances scientific rigor with pragmatism:
                we recognize that computational analysis alone can identify important gaps, but those gaps gain credibility when
                validated by multiple independent research groups.
            </p>

            <h3>The Four Validation Tiers</h3>

            <div class="validation-tier gold">
                <div class="tier-header">
                    <span class="tier-badge">GOLD</span>
                    3+ Independent Sources
                </div>
                <p class="tier-description">
                    <strong>Highest confidence.</strong> Gap relevance is confirmed by 3 or more peer-reviewed publications
                    from distinct research groups with independent authors and funding sources. These gaps represent areas of
                    genuine scientific consensus that research is needed.
                </p>
                <p class="tier-description">
                    <strong>Use case:</strong> Research priorities, grant proposals, clinical guideline development, policy
                    recommendations. These gaps have the broadest scientific support and lowest risk of being contradicted by
                    future evidence.
                </p>
                <div class="tier-examples">
                    <strong>Examples:</strong>
                    Gap #1 (Gene therapy for LADA) — Validated by 3+ publications on LADA genetics and vector development
                    | Gap #2 (Beta cell regeneration x equity) — Multiple sources on stem cell therapy plus equity literature
                    | Gap #3 (Islet transplant outcomes) — CITR registry data plus clinical trials from independent centers
                </div>
            </div>

            <div class="validation-tier silver">
                <div class="tier-header">
                    <span class="tier-badge">SILVER</span>
                    2 Independent Sources
                </div>
                <p class="tier-description">
                    <strong>Moderate confidence.</strong> Gap is supported by exactly 2 peer-reviewed sources from different
                    research groups. This represents an active area of early-stage investigation where evidence is growing but
                    not yet consolidated.
                </p>
                <p class="tier-description">
                    <strong>Use case:</strong> Emerging research opportunities, early-stage funding considerations, pilot studies.
                    SILVER gaps merit attention but warrant caution about overstating consensus. Future evidence may consolidate
                    these into GOLD tier, or refine/challenge the original gap hypothesis.
                </p>
                <div class="tier-examples">
                    <strong>Examples:</strong>
                    Gap #4 (Drug repurposing for islet transplant) — Two sources on candidate molecules and transplant outcomes
                    | Gap #5 (Regulatory T cells in neuropathy) — Publications on Treg immunobiology plus DPN-specific work
                </div>
            </div>

            <div class="validation-tier bronze">
                <div class="tier-header">
                    <span class="tier-badge">BRONZE</span>
                    Computational Analysis Only
                </div>
                <p class="tier-description">
                    <strong>Lower confidence.</strong> Gap is identified by our bibliometric analysis, literature gaps, or single
                    published source, but has not been independently validated by multiple expert sources. These gaps are included
                    for completeness and because they may represent genuine scientific opportunities—but they carry higher uncertainty.
                </p>
                <p class="tier-description">
                    <strong>Use case:</strong> Exploratory research, hypothesis generation, gaps needing independent verification
                    before major commitment. When citing BRONZE gaps, acknowledge the limited validation evidence and flag for
                    expert review.
                </p>
                <div class="tier-examples">
                    <strong>Examples:</strong>
                    Gap #10 (LADA prevalence estimation) — Based on our analysis of diagnostic criteria variation and registry
                    data, but not independently confirmed by other groups
                    | Gap #13 &amp; #14 (Personalized nutrition) — Emerging area with limited literature, identified via computational
                    analysis of existing publications
                </div>
            </div>

            <div class="validation-tier review">
                <div class="tier-header">
                    <span class="tier-badge">EXPLORATORY</span>
                    Biological Plausibility Uncertain
                </div>
                <p class="tier-description">
                    <strong>Speculative.</strong> Gap is included because of biological plausibility or preliminary data, but the
                    underlying hypothesis lacks substantial evidence. These gaps may be removed if future evidence doesn't support
                    the mechanistic or clinical rationale.
                </p>
                <p class="tier-description">
                    <strong>Use case:</strong> Early-stage hypothesis testing, basic science exploration, future research planning.
                    Do not use EXPLORATORY gaps for clinical recommendations or policy decisions.
                </p>
                <div class="tier-examples">
                    <strong>Examples:</strong>
                    Gap #9 (Glucokinase activators in LADA) — Biologically plausible for LADA (autoimmune + beta cell dysfunction)
                    but limited direct evidence in LADA populations; requires validation studies
                </div>
            </div>

            <h3>Visualization: Validation Pyramid</h3>
            <p>
                The distribution of gaps across tiers follows an inverted pyramid: fewer GOLD gaps (broadest consensus),
                increasing numbers of SILVER and BRONZE (emerging or computational), and EXPLORATORY as speculative areas
                for future exploration.
            </p>

            <div class="pyramid">
                <div class="pyramid-row">
                    <div class="pyramid-label">GOLD (3+)</div>
                    <div class="pyramid-bar pyramid-gold">Validated by multiple sources</div>
                    <div class="pyramid-count">3-4 gaps</div>
                </div>
                <div class="pyramid-row">
                    <div class="pyramid-label">SILVER (2)</div>
                    <div class="pyramid-bar pyramid-silver">Early-stage consensus</div>
                    <div class="pyramid-count">4-5 gaps</div>
                </div>
                <div class="pyramid-row">
                    <div class="pyramid-label">BRONZE (1)</div>
                    <div class="pyramid-bar pyramid-bronze">Computational + limited evidence</div>
                    <div class="pyramid-count">5-7 gaps</div>
                </div>
                <div class="pyramid-row">
                    <div class="pyramid-label">EXPLORATORY</div>
                    <div class="pyramid-bar pyramid-review">Plausible, awaiting validation</div>
                    <div class="pyramid-count">1-2 gaps</div>
                </div>
            </div>

            <h3>How Validation Works in Practice</h3>
            <p>
                Each gap goes through a multi-step validation process: (1) initial identification via PubMed and ClinicalTrials.gov
                analysis; (2) bibliographic clustering to find related publications; (3) independent expert review against research
                literature; (4) assignment to a tier based on source count and independence; (5) re-evaluation at each data refresh
                cycle (quarterly) to capture newly published evidence.
            </p>

            <p>
                A gap may move between tiers. For example, a BRONZE gap validated by a new publication might be re-classified as
                SILVER in the next update. Conversely, evidence contradicting a gap hypothesis (e.g., a large RCT showing no benefit)
                may prompt downward reclassification or removal. All tier changes are documented in the change log.
            </p>
        </div>

        <!-- TAB 3: Gap Identification Methodology -->
        <div id="gap-identification" class="tab-content">
            <h2>How We Identify Research Gaps</h2>

            <p>
                Research gaps are identified through a systematic, multi-stage process that combines computational analysis with
                clinical judgment. The goal is to find areas of genuine scientific uncertainty that matter to patients and clinicians.
            </p>

            <h3>Stage 1: Literature Search</h3>
            <p>
                We query PubMed using a curated set of diabetes-related MeSH terms, keywords, and drug/disease combinations.
                For each potential gap area, we retrieve all indexed publications (typically 100–5,000+ papers per query).
                Search parameters include date ranges, publication types (emphasizing peer-reviewed research), and language (English,
                with some inclusion of translated abstracts).
            </p>

            <div class="section-box">
                <strong>Example search:</strong>
                <div class="code-example">
("LADA" OR "latent autoimmune diabetes" OR "adult autoimmune") AND ("gene therapy" OR "genetic engineering" OR "CRISPR") AND ("type 1 diabetes" OR "autoimmune diabetes")
                </div>
            </div>

            <h3>Stage 2: Bibliometric Analysis</h3>
            <p>
                For each gap hypothesis, we compute summary metrics:
            </p>
            <ul>
                <li>
                    <strong>Publication density:</strong> Number of publications per year; trends over time. Declining publication
                    counts may indicate abandoned research or maturation of the field.
                </li>
                <li>
                    <strong>Citation frequency:</strong> How often papers in this area cite each other (disciplinary clustering);
                    cross-citation with adjacent fields (e.g., immunology, device engineering).
                </li>
                <li>
                    <strong>Author network:</strong> Whether publications come from many independent groups (healthy diversity) or a
                    few dominant labs (concentrated expertise).
                </li>
                <li>
                    <strong>Funding gaps:</strong> NIH funding by topic (via reporter.nih.gov); comparison to disease burden metrics
                    from IDF Diabetes Atlas and WHO.
                </li>
                <li>
                    <strong>Geographic coverage:</strong> In which countries is research conducted? Are there regions with high diabetes
                    burden but low research activity?
                </li>
            </ul>

            <h3>Stage 3: Gap Identification Criteria</h3>
            <p>
                A gap is identified if it meets one or more of the following criteria:
            </p>

            <div class="methodology-list">
                <ul>
                    <li>
                        <strong>Publication density below expected:</strong> For a topic predicted to have high research activity
                        (based on disease burden, funding, or clinical importance), publication count falls below a statistical threshold.
                        Gap Score = max(0, 1 − (joint_pubs / geometric_mean)) × 100.
                    </li>
                    <li>
                        <strong>Funding mismatch:</strong> NIH funding for a topic is disproportionately low relative to disease prevalence
                        or impact potential.
                    </li>
                    <li>
                        <strong>Underserved population:</strong> Research is geographically concentrated (e.g., HICs only) while disease
                        burden exists globally (e.g., LMIC prevalence data from IDF Atlas).
                    </li>
                    <li>
                        <strong>Mechanistic novelty:</strong> Emerging biological mechanism or therapeutic approach lacking sufficient
                        experimental or clinical validation (identified via literature review).
                    </li>
                    <li>
                        <strong>Clinical practice gap:</strong> Published guidelines acknowledge unanswered questions; real-world treatment
                        variation suggests clinical uncertainty.
                    </li>
                </ul>
            </div>

            <h3>Stage 4: Prioritization Framework</h3>
            <p>
                Once gaps are identified, we apply a prioritization framework to rank them by strategic importance. This framework
                balances multiple dimensions:
            </p>

            <ul>
                <li>
                    <strong>Impact potential:</strong> What is the potential clinical and public health benefit if the gap is filled?
                    (e.g., LADA gene therapy could help &gt;10% of autoimmune diabetes patients; personalized nutrition affects T2D
                    management for millions)
                </li>
                <li>
                    <strong>Feasibility:</strong> Are the scientific tools, expertise, and funding mechanisms available or within reach?
                    Is this a 2-year research project or a 10-year moonshot?
                </li>
                <li>
                    <strong>Existing infrastructure:</strong> Are there existing registries (CITR), trial networks (AABB), or patient cohorts
                    that could accelerate the research?
                </li>
                <li>
                    <strong>Equity implications:</strong> Does filling this gap help close disparities? Does it risk exacerbating them
                    (e.g., therapies available only to HICs)?
                </li>
            </ul>

            <h3>Stage 5: The 15 Research Gaps (Current Classification)</h3>
            <p>
                Our systematic analysis has identified 15 research gaps organized by mechanism and clinical context.
                Each gap is classified by validation tier and prioritized by impact-feasibility analysis. Below is a summary;
                visit the <strong>Gap Deep Dives</strong> dashboard for detailed evidence for each.
            </p>

            <div class="research-gap-list">
                <div class="gap-card">
                    <div class="gap-title">Gap #1: LADA Gene Therapy</div>
                    <span class="gap-validation gold">GOLD</span>
                    <p class="gap-description">Vectors and ex vivo strategies to deliver corrected LADA-risk genes to autoreactive immune cells.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #2: Beta Cell Regen × Equity</div>
                    <span class="gap-validation gold">GOLD</span>
                    <p class="gap-description">Global access to stem cell-derived beta cell therapies; production scaling and cost reduction.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #3: Islet Transplant Outcomes</div>
                    <span class="gap-validation gold">GOLD</span>
                    <p class="gap-description">Long-term durability and immunosuppression minimization in clinical islet transplantation.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #4: Drug Repurposing</div>
                    <span class="gap-validation silver">SILVER</span>
                    <p class="gap-description">Existing medications (e.g., antivirals, antiparasitics) repurposed to improve islet transplant survival.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #5: Tregs in Neuropathy</div>
                    <span class="gap-validation silver">SILVER</span>
                    <p class="gap-description">Regulatory T cell expansion strategies to prevent diabetic peripheral neuropathy progression.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #6: T Cell Tolerance</div>
                    <span class="gap-validation silver">SILVER</span>
                    <p class="gap-description">Mechanisms of antigen-specific tolerance in T1D; CAR-Treg and TCR-Treg engineering approaches.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #7: Glycemic Variability</div>
                    <span class="gap-validation silver">SILVER</span>
                    <p class="gap-description">Blood glucose instability (not HbA1c) as independent risk factor; intervention strategies.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #8: Diabetic Foot Ulcer Prevention</div>
                    <span class="gap-validation silver">SILVER</span>
                    <p class="gap-description">Predictive biomarkers and early intervention to prevent lower-limb amputation in T2D.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #9: GKA in LADA</div>
                    <span class="gap-validation review">EXPLORATORY</span>
                    <p class="gap-description">Glucokinase activators for beta cell preservation; evidence limited in LADA populations.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #10: LADA Prevalence</div>
                    <span class="gap-validation bronze">BRONZE</span>
                    <p class="gap-description">True prevalence of LADA; diagnostic criteria harmonization; predictive biomarkers.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #11: Diabetic Retinopathy Staging</div>
                    <span class="gap-validation bronze">BRONZE</span>
                    <p class="gap-description">AI-based classification of retinopathy severity; treatment response prediction.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #12: Kidney Disease Progression</div>
                    <span class="gap-validation bronze">BRONZE</span>
                    <p class="gap-description">Biomarkers of DKD progression beyond albuminuria; early intervention windows.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #13: Personalized Nutrition (T1D)</div>
                    <span class="gap-validation bronze">BRONZE</span>
                    <p class="gap-description">Carb counting optimization and meal composition impact on glycemic control in T1D.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #14: Personalized Nutrition (T2D)</div>
                    <span class="gap-validation bronze">BRONZE</span>
                    <p class="gap-description">Dietary interventions tailored to individual metabolic and microbiome profiles in T2D.</p>
                </div>
                <div class="gap-card">
                    <div class="gap-title">Gap #15: Psychosocial Burden &amp; Adherence</div>
                    <span class="gap-validation bronze">BRONZE</span>
                    <p class="gap-description">Mental health integration and behavioral interventions for diabetes distress and treatment adherence.</p>
                </div>
            </div>
        </div>

        <!-- TAB 4: Citation Standards -->
        <div id="citations" class="tab-content">
            <h2>Citation Standards & Evidence Linking</h2>

            <p>
                Every claim in the Diabetes Research Hub that cites published research is linked to a PubMed ID (PMID) when possible.
                This allows readers to verify the original source, review methodology, and assess evidence quality independently.
            </p>

            <h3>How Claims Are Linked to Evidence</h3>
            <p>
                Throughout the dashboards, you will find citations in two formats:
            </p>

            <div class="citation-guide">
                <strong>Format 1: Inline hyperlinks</strong>
                <p style="margin-top: 0.5rem;">
                    Claims are linked directly to PubMed. Example: "Stem cell-derived islet transplants show &gt;90% insulin independence
                    at 1 year <a href="https://pubmed.ncbi.nlm.nih.gov/" target="_blank">PMID:XXXXXXX</a>."
                    Clicking the PMID takes you to the abstract and full-text links.
                </p>
            </div>

            <div class="citation-guide">
                <strong>Format 2: Reference tables</strong>
                <p style="margin-top: 0.5rem;">
                    Detailed dashboards include reference tables listing all cited PMIDs, authors, publication years, and study designs.
                    These tables are sortable and filterable by study type, population, and outcomes.
                </p>
            </div>

            <h3>APA and BibTeX Formats</h3>
            <p>
                For academic use, we provide standardized citations. When citing a specific finding from the Hub, use the PMID
                reference directly. For citing the Hub itself or a dashboard:
            </p>

            <div class="code-example">
APA Format:
Bottum, J., et al. (2026). Diabetes Research Hub: Methodology &amp; validation framework [Dashboard].
Diabetes Research Hub. https://github.com/BottumJ/diabetes-research-hub

BibTeX:
@misc{BottumHub2026,
    author = {Bottum, J. and collaborators},
    title = {Diabetes Research Hub: Methodology and Validation Framework},
    year = {2026},
    url = {https://github.com/BottumJ/diabetes-research-hub}
}
            </div>

            <h3>How to Verify a Citation</h3>
            <ol>
                <li>
                    <strong>Locate the PMID link</strong> in the claim or reference table.
                </li>
                <li>
                    <strong>Visit PubMed</strong> (pubmed.ncbi.nlm.nih.gov) and enter the PMID in the search box.
                </li>
                <li>
                    <strong>Review the abstract:</strong> Check the study design (RCT, meta-analysis, observational), population,
                    and primary outcomes. Note: abstracts do not always capture the full scope of the paper.
                </li>
                <li>
                    <strong>Access the full text</strong> via PubMed's "Full Text" link, institutional access, or the journal website.
                </li>
                <li>
                    <strong>Assess quality:</strong> Use tools like GRADE (Grading of Recommendations Assessment, Development and Evaluation)
                    or RoB 2 (Risk of Bias) to evaluate study design and potential biases.
                </li>
            </ol>

            <h3>Known Limitations of Our Citation Approach</h3>

            <ul>
                <li>
                    <strong>Computational assignment:</strong> Some PMIDs are assigned via computational matching to PubMed abstracts.
                    While automated matching is generally reliable, manual verification is occasionally needed. We note this when
                    applicable.
                </li>
                <li>
                    <strong>Publication bias:</strong> Our citations necessarily reflect what has been published. Negative results,
                    null studies, and unpublished trials are underrepresented in PubMed.
                </li>
                <li>
                    <strong>Recency lag:</strong> PubMed indexing has a 1–3 month delay. Very recent publications may not yet be
                    linked to all relevant gap summaries.
                </li>
                <li>
                    <strong>Abstract limitations:</strong> Some claims require reading the full paper; abstracts may not capture
                    context, limitations, or nuances.
                </li>
            </ul>

            <h3>Reporting Citation Errors</h3>
            <p>
                If you find an incorrect PMID, a missing citation, or a claim unsupported by the linked paper, please report it:
            </p>
            <div class="link-group">
                <strong>GitHub Issues:</strong>
                <a href="https://github.com/BottumJ/diabetes-research-hub/issues" target="_blank">
                    diabetes-research-hub/issues
                </a>
                <strong>OSF Project Page:</strong>
                <a href="https://osf.io/hu9ga" target="_blank">https://osf.io/hu9ga</a>
            </div>
            <p>
                Include the dashboard name, claim, and reason for the error. We will investigate and correct the issue in the next
                data refresh cycle.
            </p>
        </div>

        <!-- TAB 5: Data Sources & Tools -->
        <div id="data-sources" class="tab-content">
            <h2>Data Sources & Computational Tools</h2>

            <p>
                The Diabetes Research Hub is built on publicly available, open-access databases and tools.
                We intentionally avoid proprietary, paywalled, or restricted-access data sources to ensure reproducibility and broad access.
            </p>

            <h3>Primary Data Sources</h3>

            <table class="data-source-table">
                <thead>
                    <tr>
                        <th>Database / Registry</th>
                        <th>Purpose</th>
                        <th>Update Frequency</th>
                        <th>Access</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>PubMed / MEDLINE</strong></td>
                        <td>Literature indexing for gap identification and validation; citation retrieval</td>
                        <td>Daily</td>
                        <td>Free (NCBI E-utilities API)</td>
                    </tr>
                    <tr>
                        <td><strong>ClinicalTrials.gov</strong></td>
                        <td>Registered trials; trial status, enrollment, outcomes; funding source identification</td>
                        <td>Weekly</td>
                        <td>Free (API)</td>
                    </tr>
                    <tr>
                        <td><strong>IDF Diabetes Atlas</strong></td>
                        <td>Global diabetes epidemiology; prevalence by country, region, age, type; projections to 2045</td>
                        <td>Annual (11th ed. 2024)</td>
                        <td>Free (PDF + interactive database)</td>
                    </tr>
                    <tr>
                        <td><strong>WHO Essential Medicines List</strong></td>
                        <td>Diabetes drug coverage; global treatment accessibility</td>
                        <td>Annual</td>
                        <td>Free</td>
                    </tr>
                    <tr>
                        <td><strong>CITR (Collaborative Islet Transplant Registry)</strong></td>
                        <td>Islet transplantation outcomes; long-term follow-up; immunosuppression protocols</td>
                        <td>Annual</td>
                        <td>Free (summary reports)</td>
                    </tr>
                    <tr>
                        <td><strong>NIH Reporter</strong></td>
                        <td>NIH research funding by topic; budget analysis; grant keyword search</td>
                        <td>Monthly</td>
                        <td>Free (API)</td>
                    </tr>
                </tbody>
            </table>

            <h3>Computational Tools & Languages</h3>

            <p>
                All analysis and dashboard generation is performed using open-source tools and publicly available libraries:
            </p>

            <ul>
                <li>
                    <span class="tool-name">Python 3.9+</span> — Primary language for data retrieval, analysis, and HTML generation.
                </li>
                <li>
                    <span class="tool-name">Biopython</span> — NCBI utilities for PubMed queries and sequence analysis.
                </li>
                <li>
                    <span class="tool-name">Pandas</span> — Data manipulation, filtering, and export to tables.
                </li>
                <li>
                    <span class="tool-name">scikit-learn</span> — Clustering and dimensionality reduction for bibliometric analysis.
                </li>
                <li>
                    <span class="tool-name">Requests</span> — HTTP library for API calls to ClinicalTrials.gov and other sources.
                </li>
                <li>
                    <span class="tool-name">Jinja2</span> — Template engine for reproducible HTML dashboard generation.
                </li>
                <li>
                    <span class="tool-name">Git/GitHub</span> — Version control; public repository for transparency and collaboration.
                </li>
            </ul>

            <h3>Static HTML & Accessibility</h3>

            <p>
                All dashboards are generated as static HTML files with embedded CSS and JavaScript. This design choice ensures:
            </p>

            <ul>
                <li>
                    <strong>No dependencies:</strong> Open in any web browser without installing software or running a server.
                </li>
                <li>
                    <strong>Offline access:</strong> Download and view dashboards locally or share via email/USB.
                </li>
                <li>
                    <strong>Archival quality:</strong> Static files are stable over time; no risk of URL rot or service discontinuation.
                </li>
                <li>
                    <strong>Reproducibility:</strong> Generate identical dashboards by running the build scripts with the same input data.
                </li>
            </ul>

            <h3>Data Refresh Cycle & Versioning</h3>

            <p>
                The Diabetes Research Hub is updated quarterly (January, April, July, October). Each refresh:
            </p>

            <ul>
                <li>
                    Queries PubMed and ClinicalTrials.gov for new publications and trials matching our search terms.
                </li>
                <li>
                    Re-validates all 15 gaps against the latest evidence; tiers may change if new GOLD-tier sources are published.
                </li>
                <li>
                    Updates epidemiology and funding data from IDF, WHO, and NIH Reporter.
                </li>
                <li>
                    Publishes a dated data snapshot (e.g., "2026-Q1 Snapshot") to enable comparative analysis and citation.
                </li>
                <li>
                    Logs all gap reclassifications and new findings in a change log.
                </li>
            </ul>

            <p>
                Users can cite a specific data snapshot (e.g., "as of 2026-Q1") to ensure reproducibility of their analysis.
            </p>

            <h3>What We Don't Use</h3>

            <ul>
                <li>
                    <strong>Proprietary databases:</strong> No access to Scopus, Web of Science, or proprietary EHR data.
                </li>
                <li>
                    <strong>Paywalled journals:</strong> All citations are to publicly accessible abstracts or open-access full texts.
                </li>
                <li>
                    <strong>Restricted APIs:</strong> No use of data requiring paid licenses or restricted institutional access.
                </li>
                <li>
                    <strong>Commercial data aggregators:</strong> No vendor lock-in; full transparency of data sources.
                </li>
            </ul>
        </div>

        <!-- TAB 6: How to Contribute -->
        <div id="contribute" class="tab-content">
            <h2>How to Contribute</h2>

            <p>
                The Diabetes Research Hub is a collaborative, open-source project. We welcome contributions from researchers, clinicians,
                patients, students, and data enthusiasts. There are many ways to help improve the platform.
            </p>

            <h3>Report a Citation Error</h3>
            <div class="contribution-box">
                <h4>Found an incorrect PMID, missing reference, or unsupported claim?</h4>
                <ul class="contribution-list">
                    <li>
                        Open a <strong>GitHub Issue</strong> with the dashboard name, specific claim, and why you believe it is incorrect.
                    </li>
                    <li>
                        Include the correct PMID or reference if you have identified a better source.
                    </li>
                    <li>
                        We will investigate and correct the issue in the next data refresh cycle (within ~12 weeks).
                    </li>
                </ul>
            </div>

            <h3>Suggest a New Research Gap</h3>
            <div class="contribution-box">
                <h4>Identified an important gap we've missed?</h4>
                <ul class="contribution-list">
                    <li>
                        Describe the gap: What is the unmet research need? Why does it matter to diabetes patients?
                    </li>
                    <li>
                        Provide evidence: Link to peer-reviewed publications supporting the gap (at least one PMID).
                    </li>
                    <li>
                        Suggest a validation tier: Based on our framework, do you have GOLD, SILVER, or BRONZE-tier evidence?
                    </li>
                    <li>
                        Submit via a <strong>GitHub Issue</strong> or contact us via <strong>OSF</strong>.
                    </li>
                </ul>
            </div>

            <h3>Improve Existing Dashboards</h3>
            <div class="contribution-box">
                <h4>See a visualization that could be clearer or more useful?</h4>
                <ul class="contribution-list">
                    <li>
                        Suggest improvements to design, layout, or interactivity (GitHub Issues).
                    </li>
                    <li>
                        Propose new visualizations or comparison views (e.g., "add a gap-by-disease-type view").
                    </li>
                    <li>
                        Code contributions welcome: fork the GitHub repo, create a feature branch, and submit a pull request.
                    </li>
                </ul>
            </div>

            <h3>Add Data Sources or Tools</h3>
            <div class="contribution-box">
                <h4>Know of a public database or tool that should be integrated?</h4>
                <ul class="contribution-list">
                    <li>
                        Suggest new data sources (GitHub Issues, OSF comments).
                    </li>
                    <li>
                        Requirements: Must be open-access, free, and reproducible; ideally with API access.
                    </li>
                    <li>
                        Help us integrate it: We may ask you to draft sample code or documentation.
                    </li>
                </ul>
            </div>

            <h3>Translate or Localize Content</h3>
            <div class="contribution-box">
                <h4>Want to make the Hub accessible in other languages?</h4>
                <ul class="contribution-list">
                    <li>
                        Volunteer to translate dashboards or methodology documentation.
                    </li>
                    <li>
                        We will coordinate translation, review, and publication on the GitHub repository.
                    </li>
                    <li>
                        Contributors will be credited in the project README and dashboard footers.
                    </li>
                </ul>
            </div>

            <h3>Conduct Independent Validation Studies</h3>
            <div class="contribution-box">
                <h4>Interested in validating a BRONZE or EXPLORATORY gap?</h4>
                <ul class="contribution-list">
                    <li>
                        Design and execute a literature review or empirical study to validate the gap.
                    </li>
                    <li>
                        Publish your findings; we will link to your publication and update the gap's validation tier accordingly.
                    </li>
                    <li>
                        You will be acknowledged as a contributor; consider listing the Hub as a data source or collaborator.
                    </li>
                </ul>
            </div>

            <h3>Provide Feedback on Platform Vision</h3>
            <div class="contribution-box">
                <h4>Have broader suggestions for the Hub's direction?</h4>
                <ul class="contribution-list">
                    <li>
                        Participate in quarterly planning discussions (announced on GitHub and OSF).
                    </li>
                    <li>
                        Suggest features, research priorities, or strategic partnerships.
                    </li>
                    <li>
                        Join the core team as a collaborator or advisor (if you commit ongoing contribution).
                    </li>
                </ul>
            </div>

            <h3>Contribution Guidelines</h3>
            <p>
                For detailed contribution guidelines, please see:
            </p>
            <div class="link-group">
                <strong>GitHub CONTRIBUTING.md:</strong>
                <a href="https://github.com/BottumJ/diabetes-research-hub/blob/main/CONTRIBUTING.md" target="_blank">
                    CONTRIBUTING.md
                </a>
                <strong>GitHub Issues:</strong>
                <a href="https://github.com/BottumJ/diabetes-research-hub/issues" target="_blank">
                    diabetes-research-hub/issues
                </a>
                <strong>OSF Project:</strong>
                <a href="https://osf.io/hu9ga" target="_blank">https://osf.io/hu9ga</a>
            </div>

            <h3>Attribution & Credit</h3>
            <p>
                All contributors are credited in the project repository and, where applicable, in dashboard footers and acknowledgment sections.
                We aim for transparency about who has shaped the Hub's analysis and direction.
            </p>
        </div>
    </div>

    <footer>
        <div class="footer-note">
            <strong>Diabetes Research Hub — Methodology & Validation Framework</strong>
            <br>
            Version 1.0 | Last Updated: 2026-03-16
            <br>
            <br>
            This dashboard is part of the Diabetes Research Hub, an open-source platform for accelerating diabetes research.
            <br>
            <strong>Repository:</strong> <a href="https://github.com/BottumJ/diabetes-research-hub" target="_blank">BottumJ/diabetes-research-hub</a>
            | <strong>OSF:</strong> <a href="https://osf.io/hu9ga" target="_blank">https://osf.io/hu9ga</a>
            <br>
            <br>
            <em>Not medical advice. All analyses are computational research tools for research and educational purposes.</em>
        </div>
    </footer>

    <script>
        function switchTab(tabName) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => {
                content.classList.remove('active');
            });

            // Deactivate all buttons
            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(button => {
                button.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(tabName).classList.add('active');

            // Activate clicked button
            event.target.classList.add('active');

            // Scroll to top of tab content
            document.querySelector('.container').scrollIntoView({ behavior: 'smooth' });
        }

        // Set initial active tab
        document.querySelector('.tab-button').classList.add('active');
    </script>
</body>
</html>
'''

# Write to file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

# Print status
print(f"Methodology: {os.path.getsize(output_path):,} bytes")
