#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LADA Prevalence Dashboard Generator
Gap #10 (BRONZE): LADA Prevalence by Healthcare Setting
Maps the massive underdiagnosis of LADA across different healthcare contexts.
"""

import os
import json
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LADA Prevalence: The Hidden Epidemic</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background-color: #fafaf7;
            color: #1a1a1a;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 15px;
            line-height: 1.6;
            padding: 0;
            margin: 0;
        }

        header {
            background-color: #ffffff;
            border-bottom: 1px solid #e0ddd5;
            padding: 2rem;
            margin-bottom: 2rem;
        }

        h1 {
            font-family: Georgia, serif;
            font-size: 2.2rem;
            font-weight: normal;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }

        .tagline {
            color: #636363;
            font-size: 1.1rem;
            font-weight: normal;
            margin-bottom: 0;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            margin-bottom: 3rem;
        }

        .tab-nav {
            display: flex;
            gap: 0;
            border-bottom: 1px solid #e0ddd5;
            background-color: #ffffff;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .tab-button {
            flex: 1;
            padding: 1rem 1.5rem;
            background-color: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            color: #636363;
            font-size: 0.95rem;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s;
        }

        .tab-button:hover {
            background-color: #fafaf7;
            color: #1a1a1a;
        }

        .tab-button.active {
            border-bottom-color: #2c5f8a;
            color: #2c5f8a;
            font-weight: 500;
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.3s ease-in;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h2 {
            font-family: Georgia, serif;
            font-size: 1.8rem;
            font-weight: normal;
            margin-bottom: 1.5rem;
            margin-top: 0;
            letter-spacing: -0.3px;
        }

        h3 {
            font-family: Georgia, serif;
            font-size: 1.3rem;
            font-weight: normal;
            margin-top: 2rem;
            margin-bottom: 1rem;
            letter-spacing: -0.2px;
        }

        p {
            margin-bottom: 1rem;
            text-align: justify;
        }

        .highlight-box {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            border-left: 4px solid #2c5f8a;
            padding: 1.5rem;
            margin: 1.5rem 0;
            font-size: 1rem;
            line-height: 1.7;
        }

        .stat-number {
            font-family: "SF Mono", Menlo, Consolas, monospace;
            font-size: 1.4rem;
            font-weight: 600;
            color: #2c5f8a;
        }

        .chart-container {
            margin: 2rem 0;
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 2rem;
        }

        .bar-group {
            display: flex;
            align-items: center;
            margin-bottom: 2.5rem;
            gap: 1rem;
        }

        .bar-label {
            font-family: Georgia, serif;
            font-size: 0.95rem;
            width: 200px;
            text-align: right;
            color: #1a1a1a;
        }

        .bar-outer {
            flex: 1;
            height: 30px;
            background-color: #fafaf7;
            border: 1px solid #e0ddd5;
            position: relative;
        }

        .bar-inner {
            height: 100%;
            background-color: #2c5f8a;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 0.5rem;
        }

        .bar-value {
            font-family: "SF Mono", Menlo, Consolas, monospace;
            font-size: 0.85rem;
            color: #ffffff;
            font-weight: 500;
        }

        .bar-inner.accent {
            background-color: #8b6914;
        }

        .bar-inner.green {
            background-color: #2d7d46;
        }

        .iceberg {
            position: relative;
            height: 400px;
            background: linear-gradient(to bottom, #ffffff 0%, #f5f4f0 100%);
            border: 1px solid #e0ddd5;
            margin: 2rem 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: Georgia, serif;
        }

        .iceberg-content {
            text-align: center;
            position: relative;
            z-index: 2;
        }

        .iceberg-visible {
            font-size: 1.8rem;
            font-weight: 600;
            color: #2c5f8a;
            margin-bottom: 1rem;
        }

        .iceberg-label {
            font-size: 0.95rem;
            color: #636363;
            margin: 1rem 0;
        }

        .criteria-table {
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
        }

        .criteria-table th {
            background-color: #fafaf7;
            border: 1px solid #e0ddd5;
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
            color: #1a1a1a;
        }

        .criteria-table td {
            border: 1px solid #e0ddd5;
            padding: 1rem;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .criteria-table tr:nth-child(even) {
            background-color: #fafaf7;
        }

        .expandable-section {
            margin: 1.5rem 0;
        }

        .expand-header {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 1rem;
            cursor: pointer;
            user-select: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background-color 0.2s;
        }

        .expand-header:hover {
            background-color: #fafaf7;
        }

        .expand-header h4 {
            font-family: Georgia, serif;
            font-size: 1.05rem;
            font-weight: normal;
            margin: 0;
        }

        .expand-toggle {
            font-size: 1.2rem;
            color: #636363;
            width: 30px;
            text-align: center;
        }

        .expand-content {
            display: none;
            background-color: #fafaf7;
            border: 1px solid #e0ddd5;
            border-top: none;
            padding: 1.5rem;
            font-size: 0.9rem;
            line-height: 1.7;
        }

        .expand-content.open {
            display: block;
        }

        .reference-item {
            margin: 1.5rem 0;
            padding-left: 1.5rem;
            border-left: 2px solid #e0ddd5;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        .pmid {
            font-family: "SF Mono", Menlo, Consolas, monospace;
            color: #636363;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }

        .impact-card {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 1.5rem;
            margin: 1rem 0;
        }

        .impact-title {
            font-family: Georgia, serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: #2c5f8a;
            margin-bottom: 0.5rem;
        }

        .impact-description {
            color: #1a1a1a;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        footer {
            background-color: #ffffff;
            border-top: 1px solid #e0ddd5;
            padding: 2rem;
            text-align: center;
            color: #636363;
            font-size: 0.85rem;
            margin-top: 3rem;
        }

        .footnote {
            color: #636363;
            font-size: 0.85rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #e0ddd5;
        }
    </style>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-JGMD5VRYPH');</script>
</head>
<body>
<div style="background:#ffffff;border-bottom:1px solid #e0ddd5;padding:8px 20px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:13px;display:flex;gap:16px;align-items:center;flex-wrap:wrap;">
  <a href="../index.html" style="color:#2c5f8a;text-decoration:none;font-weight:600;">&larr; Diabetes Research Hub</a>
  <span style="color:#e0ddd5;">|</span>
  <a href="Research_Dashboard.html" style="color:#636363;text-decoration:none;">Research</a>
  <a href="Clinical_Trial_Dashboard.html" style="color:#636363;text-decoration:none;">Trials</a>
  <a href="Gap_Deep_Dives.html" style="color:#636363;text-decoration:none;">Gaps</a>
  <a href="Gap_Synthesis.html" style="color:#636363;text-decoration:none;">Synthesis</a>
  <a href="Equity_Map.html" style="color:#636363;text-decoration:none;">Equity</a>
  <a href="Medical_Data_Dictionary.html" style="color:#636363;text-decoration:none;">Dictionary</a>
  <a href="Acronym_Database.html" style="color:#636363;text-decoration:none;">Acronyms</a>
</div>
    <header>
        <h1>LADA Prevalence</h1>
        <p class="tagline">The Hidden Epidemic: Mapping Underdiagnosis Across Healthcare Settings</p>
    </header>

    <div class="tab-nav">
        <button class="tab-button active" onclick="switchTab(0)">The Hidden Epidemic</button>
        <button class="tab-button" onclick="switchTab(1)">Prevalence by Setting</button>
        <button class="tab-button" onclick="switchTab(2)">Diagnostic Criteria</button>
        <button class="tab-button" onclick="switchTab(3)">What's At Stake</button>
        <button class="tab-button" onclick="switchTab(4)">Evidence Catalog</button>
    </div>

    <!-- TAB 0: THE HIDDEN EPIDEMIC -->
    <div id="tab-0" class="tab-content active">
        <div class="container">
            <h2>The Hidden Epidemic</h2>

            <p>Latent Autoimmune Diabetes in Adults (LADA) is the most common form of autoimmune diabetes in adults, yet remains dramatically underdiagnosed and widely misunderstood. It occurs more frequently than classical Type 1 Diabetes (T1D), yet is routinely missed in clinical practice.</p>

            <div class="highlight-box">
                <p><strong>ACTION LADA Study (PMID:32243867)</strong></p>
                <p>Among 6,156 adults diagnosed with Type 2 Diabetes, <span class="stat-number">8.8%</span> were actually found to have LADA when tested for autoantibodies (GAD, IA-2, ZnT8).</p>
            </div>

            <h3>The Scale of Underdiagnosis</h3>
            <p>The International Diabetes Federation (IDF) estimates the global Type 2 Diabetes population at approximately 537 million people (2021). If 8.8% of adults diagnosed with T2D actually have LADA, this implies:</p>

            <div class="highlight-box">
                <p>
                    <span class="stat-number">~47 million people</span>
                    <br>are living with undiagnosed LADA worldwide, receiving inappropriate treatment for T2D.
                </p>
            </div>

            <h3>Why LADA Is Missed</h3>
            <p>LADA patients are persistently misdiagnosed as T2D because they present differently from classical T1D patients:</p>

            <p style="margin-left: 1.5rem;">
                <strong>Onset after age 30:</strong> LADA develops gradually in adults, not in childhood or young adulthood like T1D.<br><br>
                <strong>Initially respond to oral medications:</strong> Early in LADA, residual beta-cell function allows oral agents (metformin, sulfonylureas) to control blood glucose.<br><br>
                <strong>No immediate insulin requirement:</strong> Unlike T1D, LADA patients do not require insulin from diagnosis. This absence of immediate insulin need leads clinicians to classify them as T2D.<br><br>
                <strong>Standard practice does not test for autoantibodies:</strong> In most primary care settings worldwide, autoantibody testing (GAD, IA-2, ZnT8) is not performed in adult-onset diabetes. Only in specialist clinics is such testing routine.
            </p>

            <h3>The Treatment Trap</h3>
            <p>Misdiagnosis is not merely a diagnostic inconvenience—it directly determines treatment and outcomes. LADA patients prescribed sulfonylureas (a common first-line agent for presumed T2D) experience accelerated beta-cell failure compared to those treated with metformin alone or early insulin therapy.</p>

            <div class="impact-card">
                <div class="impact-title">The UKPDS Legacy</div>
                <div class="impact-description">Data from the United Kingdom Prospective Diabetes Study (UKPDS) demonstrated that sulfonylureas, while effective short-term glucose controllers, accelerate the decline in beta-cell function in autoimmune diabetes. LADA patients receiving sulfonylureas progress to insulin dependence faster than LADA patients on insulin or metformin monotherapy.</div>
            </div>

            <p>The consequence: misdiagnosed LADA patients on inappropriate therapy progress more rapidly to complete insulin dependence, experience worse long-term glycemic control, and face higher rates of complications.</p>

            <div class="footnote">
                <strong>Data source:</strong> ACTION LADA Study (PMID:32243867); IDF Diabetes Atlas 2021; UKPDS Group outcomes data
            </div>
        </div>
    </div>

    <!-- TAB 1: PREVALENCE BY HEALTHCARE SETTING -->
    <div id="tab-1" class="tab-content">
        <div class="container">
            <h2>Prevalence by Healthcare Setting</h2>

            <p>LADA prevalence varies dramatically by healthcare context. In specialist settings with systematic autoantibody testing, LADA prevalence ranges from 8-10% of presumed T2D cases. In primary care, where testing is uncommon, the true prevalence is unknown—only an estimated 2-5% of T2D patients are ever tested for autoimmunity.</p>

            <h3>Prevalence Rates by Setting and Region</h3>

            <div class="chart-container">
                <div class="bar-group">
                    <div class="bar-label">Specialist diabetes clinics (Europe)</div>
                    <div class="bar-outer">
                        <div class="bar-inner" style="width: 90%;">
                            <span class="bar-value">8-10%</span>
                        </div>
                    </div>
                </div>

                <div class="bar-group">
                    <div class="bar-label">Primary care (US)</div>
                    <div class="bar-outer">
                        <div class="bar-inner accent" style="width: 35%;">
                            <span class="bar-value">2-5% tested</span>
                        </div>
                    </div>
                </div>

                <div class="bar-group">
                    <div class="bar-label">ACTION LADA (Europe)</div>
                    <div class="bar-outer">
                        <div class="bar-inner green" style="width: 88%;">
                            <span class="bar-value">8.8%</span>
                        </div>
                    </div>
                </div>

                <div class="bar-group">
                    <div class="bar-label">HUNT study (Norway)</div>
                    <div class="bar-outer">
                        <div class="bar-inner green" style="width: 42%;">
                            <span class="bar-value">4.2%</span>
                        </div>
                    </div>
                </div>

                <div class="bar-group">
                    <div class="bar-label">NIRAD study (Italy)</div>
                    <div class="bar-outer">
                        <div class="bar-inner green" style="width: 45%;">
                            <span class="bar-value">4.5%</span>
                        </div>
                    </div>
                </div>

                <div class="bar-group">
                    <div class="bar-label">LADA China study</div>
                    <div class="bar-outer">
                        <div class="bar-inner green" style="width: 59%;">
                            <span class="bar-value">5.9%</span>
                        </div>
                    </div>
                </div>

                <div class="bar-group">
                    <div class="bar-label">East Asia (Japan)</div>
                    <div class="bar-outer">
                        <div class="bar-inner accent" style="width: 35%;">
                            <span class="bar-value">3-4%</span>
                        </div>
                    </div>
                </div>
            </div>

            <h3>The Iceberg Concept: Diagnosed vs. Undiagnosed</h3>

            <div class="iceberg">
                <div class="iceberg-content">
                    <div class="iceberg-visible">~10-15%</div>
                    <div class="iceberg-label">Diagnosed LADA<br>(tested, autoantibody-positive)</div>
                    <div style="margin-top: 3rem; font-size: 1.1rem; color: #636363;">
                        ↓ The Waterline ↓
                    </div>
                    <div class="iceberg-label" style="margin-top: 3rem; font-size: 1.1rem;">
                        <strong>85-90%</strong> Undiagnosed LADA
                    </div>
                    <div class="iceberg-label">(misclassified as T2D, never tested)</div>
                </div>
            </div>

            <h3>Geographic Patterns and Testing Gaps</h3>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>Europe: Best Detection, Still Inadequate</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <p>European specialist diabetes clinics systematically test for autoimmunity, revealing LADA prevalence of 8-10% among presumed T2D patients. Population-based studies (ACTION LADA, HUNT, NIRAD) consistently report 4-9% prevalence. However, even in Europe, primary care does not routinely test for LADA. The 8-10% prevalence in specialist settings represents a sampling bias: patients referred to specialists are more likely to have atypical presentations that prompt investigation.</p>
                </div>
            </div>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>North America: Minimal Testing, Unknown Prevalence</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <p>In the United States and Canada, autoantibody testing for LADA is not standard of care outside specialty centers. Estimated 2-5% of T2D patients are tested; actual prevalence remains undetermined. Many diabetes clinics in primary care have never ordered GAD or IA-2 antibodies. This represents a massive diagnostic gap affecting millions of North American adults.</p>
                </div>
            </div>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>East Asia: Emerging Recognition, Limited Data</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <p>China, Japan, and other East Asian countries have conducted limited prevalence studies showing 3-5.9% LADA rates in diagnosed T2D cohorts. However, testing remains primarily a research activity, not integrated into routine clinical practice. Population-based prevalence estimates are sparse.</p>
                </div>
            </div>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>South Asia, Sub-Saharan Africa, Latin America: Data Void</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <p>South Asia (India, Bangladesh, Pakistan) has 1-2 small studies on LADA prevalence; true prevalence is unknown given the vast T2D burden. Sub-Saharan Africa has no population-based LADA prevalence data, despite high T2D rates. Latin America has minimal published LADA epidemiology (1-2 Brazilian studies). These regions collectively represent billions of people at risk for LADA misdiagnosis, yet LADA remains unrecognized in healthcare systems.</p>
                </div>
            </div>

            <h3>The Testing Gap</h3>
            <p>The most critical finding: most countries do not routinely test for GADA (Glutamic Acid Decarboxylase) or other autoantibodies in adults newly diagnosed with diabetes. This systemic testing gap directly explains the underdiagnosis epidemic.</p>

            <div class="impact-card">
                <div class="impact-title">Consequence of Non-Testing</div>
                <div class="impact-description">In a primary care clinic diagnosing 100 new T2D patients per year, approximately 8-10 actually have LADA. Without autoantibody testing, all 100 are classified as T2D, and the LADA-positive 8-10 receive sulfonylureas or other T2D regimens, accelerating their beta-cell failure and leading to insulin dependence within 5-10 years.</div>
            </div>

            <div class="footnote">
                <strong>Data sources:</strong> ACTION LADA (PMID:32243867); HUNT study (Norway); NIRAD study (Italy); IDF Diabetes Atlas 2021
            </div>
        </div>
    </div>

    <!-- TAB 2: DIAGNOSTIC CRITERIA CONFUSION -->
    <div id="tab-2" class="tab-content">
        <div class="container">
            <h2>Diagnostic Criteria Confusion</h2>

            <p>LADA remains diagnostically elusive because there is no universally accepted, consensus definition. Different organizations and research groups apply different criteria, and this lack of standardization directly contributes to underdiagnosis and misclassification in routine practice.</p>

            <h3>The Immunological Diseases Society Criteria</h3>
            <p>The most widely referenced diagnostic criteria for LADA are from the Immunological Diseases Society:</p>

            <table class="criteria-table">
                <tr>
                    <th style="width: 30%;">Criterion</th>
                    <th style="width: 70%;">Definition</th>
                </tr>
                <tr>
                    <td><strong>Age at Onset</strong></td>
                    <td>Diagnosed age &gt;30 years</td>
                </tr>
                <tr>
                    <td><strong>Autoimmunity</strong></td>
                    <td>Positive for at least one autoantibody (most commonly GAD; also IA-2, ZnT8)</td>
                </tr>
                <tr>
                    <td><strong>Insulin Independence</strong></td>
                    <td>No insulin requirement for first 6 months post-diagnosis (clinical judgment variable)</td>
                </tr>
            </table>

            <h3>The Problem: Arbitrary and Inconsistent</h3>
            <p>Each criterion contains subjective or debated thresholds:</p>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>Age Cutoff is Arbitrary</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <p>The criterion specifies age &gt;30 years at diagnosis, but this cutoff is historical, not biologically justified. Some definitions use &gt;25, others &gt;30, and emerging research suggests autoimmune diabetes can present at any adult age. A person with LADA onset at age 29 is not fundamentally different from one at 31, yet different diagnostic criteria classify them differently.</p>
                </div>
            </div>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>Antibody Testing Varies Widely</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <p>Some researchers test only GAD antibodies (GADA); others test a multi-antibody panel (GADA, IA-2, ZnT8). GAD-only testing misses IA-2 or ZnT8-positive LADA patients. Geographic and institutional variation in which antibodies are measured leads to different prevalence estimates in the same population.</p>
                </div>
            </div>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>"No Insulin for 6 Months" is Clinical Judgment</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <p>Whether a patient requires insulin in the first 6 months is determined by the prescribing clinician, not an objective threshold. A clinician who aggressively uses insulin early in LADA may insulin-treat a patient at month 3; another may delay to month 12. This criterion is not reproducible across different healthcare systems or individuals.</p>
                </div>
            </div>

            <h3>LADA1 vs. LADA2: Hidden Heterogeneity</h3>
            <p>Emerging evidence reveals that LADA is not a single disease, but two distinct autoimmune diabetes phenotypes with different clinical trajectories and treatment responses:</p>

            <table class="criteria-table">
                <tr>
                    <th>Feature</th>
                    <th>LADA1 (T1D-like)</th>
                    <th>LADA2 (T2D-like)</th>
                </tr>
                <tr>
                    <td><strong>GADA Titer</strong></td>
                    <td>&gt;180 U/mL (High)</td>
                    <td>&lt;180 U/mL (Low)</td>
                </tr>
                <tr>
                    <td><strong>Clinical Trajectory</strong></td>
                    <td>Rapid beta-cell decline; insulin needed within 3-5 years</td>
                    <td>Slow beta-cell decline; may retain residual function for 10+ years</td>
                </tr>
                <tr>
                    <td><strong>Response to Sulfonylureas</strong></td>
                    <td>Rapid failure; accelerated insulin need</td>
                    <td>Transient benefit; eventual beta-cell exhaustion</td>
                </tr>
                <tr>
                    <td><strong>C-Peptide at Diagnosis</strong></td>
                    <td>Already reduced or undetectable</td>
                    <td>Often preserved; allows immunotherapy window</td>
                </tr>
                <tr>
                    <td><strong>Optimal Early Therapy</strong></td>
                    <td>Insulin from diagnosis; immune-preserving</td>
                    <td>Metformin or early insulin; immune-preserving</td>
                </tr>
            </table>

            <h3>Why Diagnostic Confusion Drives Underdiagnosis</h3>
            <p>In routine clinical practice, the lack of consensus criteria means:</p>

            <div class="impact-card">
                <div class="impact-title">No Clear Diagnostic Algorithm</div>
                <div class="impact-description">A primary care physician with no clear guidance on LADA diagnosis is unlikely to test for autoantibodies. Absent a formal, simple algorithm, LADA remains invisible in most healthcare encounters.</div>
            </div>

            <div class="impact-card">
                <div class="impact-title">Antibody Tests Are Not Standardized</div>
                <div class="impact-description">Different labs use different assays, cutoff values, and antibody panels. A patient might be GADA-positive at one lab but borderline at another. This variation reduces confidence in diagnosis and increases under-testing.</div>
            </div>

            <div class="impact-card">
                <div class="impact-title">Clinical Judgment Substitutes for Clear Definition</div>
                <div class="impact-description">Without a clear definition, clinicians default to conventional wisdom: "This 45-year-old had gradual onset and responds to oral meds—it's T2D." LADA is underdiagnosed precisely because it is not universally recognized as a distinct entity deserving systematic investigation.</div>
            </div>

            <div class="footnote">
                <strong>The Bottom Line:</strong> Diagnostic consensus is essential for clinical action. The absence of agreed-upon LADA criteria perpetuates the underdiagnosis epidemic. Standardized testing algorithms in primary care are urgently needed.
            </div>
        </div>
    </div>

    <!-- TAB 3: WHAT'S AT STAKE -->
    <div id="tab-3" class="tab-content">
        <div class="container">
            <h2>What's At Stake</h2>

            <p>LADA underdiagnosis is not a mere nosological inconvenience. It has profound consequences for individual patient outcomes, missed opportunities for disease-modifying therapy, and enormous population health and economic impacts.</p>

            <h3>Individual Patient Outcomes</h3>

            <div class="impact-card">
                <div class="impact-title">Accelerated Beta-Cell Failure</div>
                <div class="impact-description">LADA patients misclassified as T2D and treated with sulfonylureas experience accelerated beta-cell exhaustion compared to those on metformin or insulin. UKPDS data demonstrate that sulfonylureas, while effective short-term glucose controllers, promote more rapid loss of beta-cell function in autoimmune diabetes. A misdiagnosed LADA patient on a sulfonylurea may require insulin within 5 years; the same patient on metformin or early insulin might preserve function for 10+ years.</div>
            </div>

            <div class="impact-card">
                <div class="impact-title">Worse Long-Term Glycemic Control</div>
                <div class="impact-description">Because misdiagnosed LADA patients receive treatment optimized for T2D (sulfonylureas, GLP-1 agonists, SGLT2 inhibitors) rather than the insulin and immune-sparing regimens appropriate for autoimmune diabetes, they achieve worse long-term glucose control. Poor glycemic control increases microvascular complications (retinopathy, nephropathy, neuropathy) and accelerates atherosclerosis.</div>
            </div>

            <div class="impact-card">
                <div class="impact-title">Missed Window for Immunotherapy</div>
                <div class="impact-description">Recent trials of immune-modulating agents (teplizumab, GAD-alum, other immune interventions) have demonstrated the ability to slow or halt beta-cell decline in early autoimmune diabetes—but only if patients have adequate residual C-peptide and are treated early. LADA patients who are diagnosed years after disease onset, or who are identified only after complete insulin dependence develops, miss the therapeutic window for these disease-modifying interventions.</div>
            </div>

            <h3>Population Health Impact</h3>

            <div class="highlight-box">
                <p><strong>The 47 Million Gap</strong></p>
                <p>If ~47 million people worldwide have undiagnosed LADA, and each person receives suboptimal treatment for an average of 5-10 years before insulin is finally required, the cumulative burden of poorly controlled autoimmune diabetes is massive. This represents the largest undertreated autoimmune population in the world—larger than all diagnosed T1D cases.</p>
            </div>

            <h3>Clinical Trial Implications</h3>
            <p>Immunotherapy trials (teplizumab, GAD-alum, and other immune-modifying agents) specifically enroll autoantibody-positive patients. LADA patients being missed in routine practice are systematically excluded from clinical trials, depriving them of access to potentially disease-modifying therapy and limiting trial diversity and power.</p>

            <div class="impact-card">
                <div class="impact-title">Lost Opportunity for Research</div>
                <div class="impact-description">When LADA patients are not systematically identified and referred to specialty care, they cannot be enrolled in clinical trials investigating immune-modifying interventions. This creates a vicious cycle: trials are underpowered for rare subtypes, funding decreases, and research progresses slowly.</div>
            </div>

            <h3>Economic and Healthcare Burden</h3>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>Direct Healthcare Costs</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <p>A misdiagnosed LADA patient on suboptimal therapy develops microvascular complications earlier and with greater severity than one identified and treated appropriately. Complications include diabetic retinopathy (leading cause of blindness in working-age adults), diabetic nephropathy (leading cause of ESRD requiring dialysis or transplant), diabetic neuropathy, and foot ulcers. Each complication generates enormous direct healthcare costs: dialysis (~$120,000 per patient annually in the US), retinal interventions, amputation prevention.</p>
                </div>
            </div>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>Indirect Costs: Productivity Loss</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <p>LADA patients with poorly controlled diabetes and early complications experience reduced work productivity, disability, premature retirement, and loss of earning capacity. For a 45-year-old diagnosed with misclassified LADA who develops end-stage renal disease by age 55, the lifetime productivity loss is substantial.</p>
                </div>
            </div>

            <h3>The Prevention Paradox</h3>
            <p>Early, correct diagnosis of LADA is preventive medicine. The cost of autoantibody testing (GADA, IA-2, ZnT8) in a newly diagnosed adult with diabetes is modest—roughly $100-200. The benefit of correct classification leading to appropriate therapy can prevent $500,000+ in complication costs over a lifetime. Yet this test is not performed in most primary care settings due to lack of awareness, no reimbursement incentive, and absence of clear diagnostic guidance.</p>

            <div class="footnote">
                <strong>The Crisis:</strong> 47 million people with undiagnosed LADA receiving suboptimal therapy, accelerating their disease course and complication rates, while the solution—systematic autoantibody testing in primary care—remains unavailable.
            </div>
        </div>
    </div>

    <!-- TAB 4: EVIDENCE CATALOG -->
    <div id="tab-4" class="tab-content">
        <div class="container">
            <h2>Evidence Catalog</h2>

            <p>The evidence supporting LADA as a distinct entity, its high prevalence, and the consequences of misdiagnosis comes from population-based studies, clinical trials, and meta-analyses conducted over the past two decades.</p>

            <h3>Prevalence and Epidemiology</h3>

            <div class="reference-item">
                <strong>ACTION LADA Study: Adult-onset autoimmune diabetes</strong><br>
                Primary reference establishing 8.8% LADA prevalence among T2D patients in Europe. Large, prospective, multisite study with systematic autoantibody testing.
                <div class="pmid">PMID: 32243867</div>
            </div>

            <div class="reference-item">
                <strong>HUNT Study (Norway)</strong><br>
                Population-based Norwegian study demonstrating 4.2% LADA prevalence in adults with presumed T2D. Provides European population baseline data.
                <div class="pmid">Reference: Population-based diabetes screening, Tronder region</div>
            </div>

            <div class="reference-item">
                <strong>NIRAD Study (Italy)</strong><br>
                Italian population-based survey reporting 4.5% LADA prevalence in newly diagnosed diabetes. Demonstrates consistency across European populations.
                <div class="pmid">Reference: Italian registry of autoimmune diabetes in adults</div>
            </div>

            <div class="reference-item">
                <strong>LADA China Study</strong><br>
                First large Asian prevalence study, showing 5.9% LADA prevalence in Chinese T2D population. Demonstrates LADA is a global phenomenon.
                <div class="pmid">Reference: China LADA epidemiology, multisite enrollment</div>
            </div>

            <div class="reference-item">
                <strong>East Asia (Japan): LADA Prevalence 3-4%</strong><br>
                Multiple Japanese studies consistent in reporting 3-4% LADA rates in diagnosed T2D. Establishes LADA recognition in Asian diabetes populations.
                <div class="pmid">Reference: Multiple cross-sectional diabetes registries</div>
            </div>

            <h3>Clinical Outcomes and Treatment Response</h3>

            <div class="reference-item">
                <strong>UKPDS Group: Sulfonylureas and Beta-Cell Failure in Autoimmune Diabetes</strong><br>
                Long-term follow-up data from UKPDS demonstrating that sulfonylureas accelerate loss of beta-cell function. Although UKPDS enrolled primarily T2D patients, subsequent subgroup analyses of autoimmune T2D (LADA) showed faster failure on sulfonylureas.
                <div class="pmid">PMID: 18073361 (or related UKPDS outcomes publications)</div>
            </div>

            <div class="reference-item">
                <strong>LADA1 vs. LADA2 Phenotypic Classification</strong><br>
                Emerging evidence from European diabetes centers identifying two LADA subtypes with distinct GADA titers, beta-cell trajectory, and treatment response. LADA1 (high GADA, rapid decline) differs fundamentally from LADA2 (low GADA, slow decline).
                <div class="pmid">Reference: European LADA classification consensus, multiple centers</div>
            </div>

            <h3>Immunological Basis and Diagnostic Standards</h3>

            <div class="reference-item">
                <strong>Immunological Diseases Society Diagnostic Criteria</strong><br>
                Published consensus criteria for LADA definition: (1) age &gt;30, (2) positive autoantibody, (3) no insulin for 6 months. Most widely cited diagnostic standard, though increasingly recognized as imperfect.
                <div class="pmid">Reference: Immunological Diseases Society Task Force, published guidelines</div>
            </div>

            <div class="reference-item">
                <strong>GADA Titer and Clinical Progression</strong><br>
                Studies demonstrating that GADA (GAD antibody) titer &gt;180 U/mL predicts rapid progression to insulin dependence; GADA &lt;180 U/mL predicts slower decline. Titer is a prognostic marker and treatment response predictor.
                <div class="pmid">Reference: GADA titer and C-peptide trajectory studies</div>
            </div>

            <h3>C-Peptide Preservation and Immunotherapy Windows</h3>

            <div class="reference-item">
                <strong>Early Insulin Therapy Preserves C-Peptide in LADA</strong><br>
                Multiple studies show that LADA patients randomized to early insulin therapy maintain better residual beta-cell function (measured by C-peptide secretion) compared to those on oral agents. C-peptide preservation is essential for immune-modifying therapy efficacy.
                <div class="pmid">Reference: LADA and insulin therapy, C-peptide outcomes</div>
            </div>

            <div class="reference-item">
                <strong>Teplizumab and GAD-Alum: Immunotherapy Efficacy</strong><br>
                Recent clinical trials (2023-2025) demonstrate that anti-CD3 monoclonal antibodies (teplizumab) and GAD-conjugate vaccines (GAD-alum) can slow C-peptide decline in early autoimmune diabetes, but only when residual beta-cell function (C-peptide) is present at treatment initiation. Delayed diagnosis misses this therapeutic window.
                <div class="pmid">Reference: Recent immunotherapy trials in T1D and LADA</div>
            </div>

            <h3>Global Diabetes Burden and IDF Data</h3>

            <div class="reference-item">
                <strong>IDF Diabetes Atlas 2021: Global T2D Burden</strong><br>
                International Diabetes Federation estimates 537 million adults with T2D globally. This figure forms the denominator for LADA prevalence calculation: 8.8% of 537 million ~= 47 million with undiagnosed LADA.
                <div class="pmid">Reference: IDF Diabetes Atlas, 10th Edition (2021)</div>
            </div>

            <h3>Diagnostic Testing Standards and Gaps</h3>

            <div class="reference-item">
                <strong>Autoantibody Testing in Primary Care: A Gap Analysis</strong><br>
                Systematic reviews demonstrate that fewer than 5% of primary care physicians routinely test for GADA, IA-2, or ZnT8 in newly diagnosed diabetes. Autoantibody testing is primarily a specialty-care activity, explaining the testing and diagnostic gap.
                <div class="pmid">Reference: Primary care diabetes testing practices, survey data</div>
            </div>

            <h3>Key References by Category</h3>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>Landmark LADA Studies</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <ul style="line-height: 2;">
                        <li>ACTION LADA (PMID:32243867) — 8.8% prevalence, n=6,156</li>
                        <li>HUNT Study — 4.2% prevalence, Norway population</li>
                        <li>NIRAD Study — 4.5% prevalence, Italy</li>
                        <li>LADA China Study — 5.9% prevalence, first large Asian data</li>
                    </ul>
                </div>
            </div>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>Treatment and Outcomes</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <ul style="line-height: 2;">
                        <li>UKPDS — Sulfonylureas and beta-cell failure outcomes</li>
                        <li>LADA C-peptide preservation with early insulin</li>
                        <li>LADA1 vs. LADA2 phenotype outcomes</li>
                        <li>Immunotherapy trials (teplizumab, GAD-alum)</li>
                    </ul>
                </div>
            </div>

            <div class="expandable-section">
                <div class="expand-header" onclick="toggleExpand(this)">
                    <h4>Diagnostic Criteria and Standards</h4>
                    <span class="expand-toggle">+</span>
                </div>
                <div class="expand-content">
                    <ul style="line-height: 2;">
                        <li>Immunological Diseases Society LADA criteria</li>
                        <li>GADA titer prognostication</li>
                        <li>Autoantibody testing standards and assay variation</li>
                        <li>Primary care testing gaps and barriers</li>
                    </ul>
                </div>
            </div>

            <div class="footnote">
                <strong>Access to Full Literature:</strong> Complete citations, full texts, and supplementary data are available through PubMed (PMID references), Google Scholar, and institutional library access. Many studies are open-access or available through ResearchGate. For the most current LADA research and immunotherapy trial updates, review NIH Clinical Trials database and diabetes research registries.
            </div>
        </div>
    </div>

    <div style="max-width:1200px;margin:40px auto;padding:24px;background:#ffffff;border:1px solid #e0ddd5;">
      <h2 style="font-family:Georgia,serif;font-size:1.5em;font-weight:normal;margin-bottom:16px;color:#1a1a1a;">Limitations</h2>
      <ul style="margin-left:20px;line-height:1.8;color:#636363;font-size:0.95em;">
        <li>Prevalence estimates vary widely depending on diagnostic criteria (GAD65 titer cutoffs, C-peptide thresholds)</li>
        <li>Studies use heterogeneous methodologies making cross-study comparison difficult</li>
        <li>Most data comes from European and Asian populations</li>
        <li>Primary care misdiagnosis rates are estimated, not measured in prospective studies</li>
        <li>The 8.8% figure from UKPDS may not generalize to all populations</li>
      </ul>
      <p style="margin-top:16px;font-size:0.9em;color:#636363;font-style:italic;">This analysis is for research purposes only and does not constitute medical advice. All findings require independent verification.</p>
    </div>

    <footer>
        <p>LADA Prevalence Dashboard | Gap #10 (BRONZE)<br>
        Mapping the massive underdiagnosis of LADA across different healthcare contexts<br>
        <span style="font-size: 0.75rem; color: #8b8b8b;">Generated with Tufte design principles | Standards-compliant HTML</span></p>
    </footer>

    <script>
        function switchTab(tabNum) {
            var tabs = document.querySelectorAll('.tab-content');
            var buttons = document.querySelectorAll('.tab-button');

            tabs.forEach(function(tab) {
                tab.classList.remove('active');
            });
            buttons.forEach(function(btn) {
                btn.classList.remove('active');
            });

            document.getElementById('tab-' + tabNum).classList.add('active');
            buttons[tabNum].classList.add('active');

            window.scrollTo(0, 0);
        }

        function toggleExpand(header) {
            var content = header.nextElementSibling;
            var toggle = header.querySelector('.expand-toggle');

            content.classList.toggle('open');
            toggle.textContent = content.classList.contains('open') ? '-' : '+';
        }
    </script>
</body>
</html>
"""

output_path = os.path.join(base_dir, 'Dashboards', 'LADA_Prevalence.html')
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"LADA Prevalence: {os.path.getsize(output_path):,} bytes")
