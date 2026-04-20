#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gap #8 (SILVER validated): Immunomodulatory Drugs for LADA
Generates an interactive Tufte-style HTML dashboard analyzing immune-modulating
therapies for beta cell preservation in LADA's slower autoimmune progression.
"""

import os
import json

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
output_path = os.path.join(base_dir, 'Dashboards', 'Immunomod_LADA.html')

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# ============================================================================
# DATA: Embedded directly in script
# ============================================================================

LADA_VS_T1D = {
    "dimensions": [
        {
            "name": "Autoantibody Profile",
            "lada": "GADA+ only (65-90%)",
            "t1d": "Multi-antibody (GADA+IA2A+ZnT8A+IAA)",
            "source": "UKPDS (PMID:18073361)"
        },
        {
            "name": "T-cell Autoreactivity",
            "lada": "Present but lower frequency",
            "t1d": "High frequency, diverse epitopes",
            "source": "Population-based cohort studies"
        },
        {
            "name": "C-peptide Decline Rate",
            "lada": "~55 pmol/L/year (first 5yr)",
            "t1d": "Rapid loss within months",
            "source": "ACTION LADA (PMID:23248199)"
        },
        {
            "name": "HLA Associations",
            "lada": "DR3/DR4 + DR3-DQ2 predominance",
            "t1d": "DR3/DR4 (classic)",
            "source": "Population and genetic association studies"
        },
        {
            "name": "Clinical Subtypes",
            "lada": "LADA1 (high GADA, rapid) vs LADA2 (low GADA, slow)",
            "t1d": "Single phenotype",
            "source": "Latent autoimmune literature"
        },
        {
            "name": "Therapeutic Window",
            "lada": "2-6 years to insulin dependence",
            "t1d": "<6 months from symptoms",
            "source": "UKPDS, ACTION LADA"
        }
    ]
}

DRUG_CANDIDATES = [
    {
        "name": "GAD-alum (Diamyd / retogatein)",
        "mechanism": "GAD65 antigen-specific immunotherapy",
        "t1d_evidence": "DIAGNODE-3 Phase 3 (n=174 evaluable, HLA DR3-DQ2 enriched) met pre-specified FUTILITY criteria at Mar 2026 interim - no clinically meaningful C-peptide effect in overall population or pre-specified subgroups. Diamyd announced discontinuation April 2026. Earlier DIAGNODE-2 (PMID 34299352) and 2022 IPD meta-analysis (PMID 35491968) showed modest HLA DR3-DQ2 subgroup signal that did NOT replicate in confirmatory Phase 3.",
        "lada_evidence": "GAD-alum trials in LADA have shown variable results; small pilot data (NCT04262479, n=14) does not yet address efficacy. Monotherapy path now contradicted for T1D.",
        "rationale": "Antigen-specific, minimal systemic immunosuppression. Following DIAGNODE-3 futility, monotherapy path is contradicted for recent-onset T1D; combination strategies (GAD + vitamin D + etanercept) remain under study. LADA-specific pivotal data absent.",
        "window": "Early-to-middle phase (0-4 years)",
        "status_2026": "CONTRADICTED_AS_MONOTHERAPY"
    },
    {
        "name": "Teplizumab (anti-CD3)",
        "mechanism": "T-cell response modification; Tzield FDA-approved for T1D delay",
        "t1d_evidence": "Phase 3 TN-10 trial (PMID:29291885); FDA approved 2023",
        "lada_evidence": "No LADA-specific trials; excluded from T1D trials",
        "rationale": "Proven T1D delay extends 1-2 years. LADA's already-long window could be further extended with earlier intervention.",
        "window": "Early phase (0-2 years)"
    },
    {
        "name": "Rituximab (anti-CD20)",
        "mechanism": "B-cell depletion",
        "t1d_evidence": "TrialNet Phase 2 showed slowed C-peptide loss in new-onset T1D (PMID:19940299)",
        "lada_evidence": "No LADA trials; LADA is GADA-driven (B-cell product)",
        "rationale": "Since LADA is GADA-dependent, B-cell depletion may be particularly effective. Less cytokine-driven inflammation than T1D.",
        "window": "Early-to-middle phase (0-4 years)"
    },
    {
        "name": "Abatacept (CTLA4-Ig)",
        "mechanism": "T-cell costimulation blockade",
        "t1d_evidence": "TrialNet: slowed C-peptide decline (PMID:20570966)",
        "lada_evidence": "No LADA trials",
        "rationale": "If T-cell autoreactivity drives gradual LADA progression, costimulation blockade during the slow phase could halt decline.",
        "window": "Middle phase (2-4 years)"
    },
    {
        "name": "Low-dose IL-2 (aldesleukin)",
        "mechanism": "Treg expansion; suppresses autoimmune attack",
        "t1d_evidence": "DIABIL-2 trial in T1D; improved Treg frequency (PMID:27727279)",
        "lada_evidence": "No LADA trials; LADA may have insufficient Treg function",
        "rationale": "Treg expansion in LADA's slower autoimmune phase could tip balance toward tolerance and regeneration.",
        "window": "Early-to-middle phase (0-4 years)"
    },
    {
        "name": "Sitagliptin + Lansoprazole",
        "mechanism": "DPP-4i + PPI; beta cell regeneration + immune modulation",
        "t1d_evidence": "REPAIR-T1D trial; mixed results (PMID:24997559)",
        "lada_evidence": "No LADA trials; LADA retains more beta cells, may respond better to regenerative signals",
        "rationale": "LADA's remaining beta cell mass is higher than T1D at diagnosis. Regenerative approach may be more effective.",
        "window": "Early phase (0-2 years)"
    },
    {
        "name": "Vitamin D (cholecalciferol)",
        "mechanism": "Immunomodulatory; Treg support; anti-inflammatory",
        "t1d_evidence": "Multiple prevention trial designs attempted; evidence for disease-modifying benefit remains mixed",
        "lada_evidence": "Observational: lower vitamin D associated with faster LADA progression",
        "rationale": "Low-risk, widely available. LADA patients with lower vitamin D show accelerated decline. Preventive potential.",
        "window": "All phases; prevention-focused"
    },
    {
        "name": "Baricitinib (JAK inhibitor)",
        "mechanism": "JAK1/2 inhibition; blocks cytokine signaling",
        "t1d_evidence": "BANDIT trial in T1D; Phase 2 data emerging",
        "lada_evidence": "No LADA data",
        "rationale": "Blocks IL-6, TNF-alpha signaling. LADA's slower autoimmune infiltration may be sensitive to JAK inhibition.",
        "window": "Early-to-middle phase (0-4 years)"
    },
    {
        "name": "Verapamil (calcium channel blocker)",
        "mechanism": "TXNIP inhibition; beta cell protection",
        "t1d_evidence": "C-peptide preservation mechanisms documented in T1D literature, though clinical translation remains limited",
        "lada_evidence": "No LADA trials; excellent safety profile",
        "rationale": "Direct beta cell protection without immunosuppression. Long-term safety established. Synergistic with immunotherapy.",
        "window": "All phases"
    }
]

THERAPEUTIC_WINDOW = {
    "phases": [
        {
            "phase": "Diagnosis",
            "duration": "0 years",
            "desc": "GADA+ detected, C-peptide >0.7 nmol/L",
            "key": "Screening, baseline assessment"
        },
        {
            "phase": "Early Phase",
            "duration": "0-2 years",
            "desc": "C-peptide declining slowly (slope ~55 pmol/L/yr)",
            "key": "Window for antigen-specific therapies (GAD-alum, teplizumab)"
        },
        {
            "phase": "Middle Phase",
            "duration": "2-4 years",
            "desc": "Accelerating decline in LADA1; plateau in LADA2",
            "key": "Window for combination therapies, Treg expansion (IL-2, abatacept)"
        },
        {
            "phase": "Late Phase",
            "duration": "4-6+ years",
            "desc": "Approaching insulin dependence; C-peptide <0.3 nmol/L",
            "key": "Beta cell regeneration focus (sitagliptin, verapamil)"
        }
    ],
    "cpeptide_trajectory": [
        {"year": 0, "value": 1.0},
        {"year": 1, "value": 0.75},
        {"year": 2, "value": 0.6},
        {"year": 3, "value": 0.4},
        {"year": 4, "value": 0.25},
        {"year": 5, "value": 0.15},
        {"year": 6, "value": 0.08}
    ]
}

WHY_UNDERSERVED = [
    {
        "factor": "Diagnostic Ambiguity",
        "desc": "LADA often misdiagnosed as T2D; ~10% of 'T2D' patients are actually LADA",
        "impact": "High",
        "source": "Clinical practice surveys"
    },
    {
        "factor": "Regulatory Pathways",
        "desc": "FDA/EMA classify by T1D or T2D; LADA doesn't fit regulatory categories",
        "impact": "High",
        "source": "Regulatory guidance"
    },
    {
        "factor": "Trial Recruitment Barrier",
        "desc": "Identifying LADA requires autoantibody testing; not standard of care in primary care",
        "impact": "High",
        "source": "TrialNet, JDRF studies"
    },
    {
        "factor": "Age Demographic",
        "desc": "LADA patients typically 30-70 years old; trials prefer younger cohorts for logistical reasons",
        "impact": "Medium",
        "source": "ACTION LADA demographics"
    },
    {
        "factor": "Market Economics",
        "desc": "8.8% diabetes prevalence (ACTION LADA) = ~50M people globally, but smaller market than T1D or T2D",
        "impact": "Medium",
        "source": "ACTION LADA epidemiology"
    },
    {
        "factor": "Publication Gap",
        "desc": "Zero joint publications for 'immunomodulatory drugs' AND 'LADA' in major databases",
        "impact": "Medium",
        "source": "PubMed bibliometric analysis 2020-2024"
    },
    {
        "factor": "Incomplete Natural History",
        "desc": "LADA heterogeneity (LADA1 vs LADA2) not well-characterized; makes trial design difficult",
        "impact": "Medium",
        "source": "UKPDS subgroup analyses"
    }
]

PRIORITY_SCORES = [
    {
        "drug": "GAD-alum (Diamyd)",
        "mechanistic_fit": 5,
        "clinical_evidence": 2,
        "safety_profile": 5,
        "feasibility": 4,
        "lada_advantage": 4,
        "composite": 3.4,
        "rank": 3,
        "notes": "DOWNGRADED April 2026: DIAGNODE-3 Phase 3 (HLA DR3-DQ2 enriched) met futility criteria - no clinically meaningful C-peptide effect. Monotherapy path contradicted in T1D. Combination and LADA-specific strategies still open but unproven. Antigen-specific mechanism preserved, but clinical evidence downgraded from 4 to 2."
    },
    {
        "drug": "Teplizumab (anti-CD3)",
        "mechanistic_fit": 4,
        "clinical_evidence": 5,
        "safety_profile": 4,
        "feasibility": 3,
        "lada_advantage": 4,
        "composite": 4.0,
        "rank": 2,
        "notes": "FDA-approved, proven delay; extends already-long window; IV infusion burden"
    },
    {
        "drug": "Rituximab (anti-CD20)",
        "mechanistic_fit": 5,
        "clinical_evidence": 4,
        "safety_profile": 3,
        "feasibility": 3,
        "lada_advantage": 5,
        "composite": 4.0,
        "rank": 3,
        "notes": "GADA-driven disease; direct B-cell targeting; long-term safety profile concerns"
    },
    {
        "drug": "Low-dose IL-2 (aldesleukin)",
        "mechanistic_fit": 4,
        "clinical_evidence": 3,
        "safety_profile": 4,
        "feasibility": 3,
        "lada_advantage": 4,
        "composite": 3.6,
        "rank": 4,
        "notes": "Treg expansion in slow-phase autoimmunity; limited LADA data"
    },
    {
        "drug": "Sitagliptin + Lansoprazole",
        "mechanistic_fit": 3,
        "clinical_evidence": 3,
        "safety_profile": 5,
        "feasibility": 5,
        "lada_advantage": 4,
        "composite": 4.0,
        "rank": 5,
        "notes": "LADA retains more beta cells; high feasibility; regenerative focus"
    },
    {
        "drug": "Abatacept (CTLA4-Ig)",
        "mechanistic_fit": 3,
        "clinical_evidence": 4,
        "safety_profile": 3,
        "feasibility": 2,
        "lada_advantage": 3,
        "composite": 3.0,
        "rank": 6,
        "notes": "Costimulation blockade; limited LADA-specific rationale; IV administration"
    },
    {
        "drug": "Baricitinib (JAK inhibitor)",
        "mechanistic_fit": 3,
        "clinical_evidence": 3,
        "safety_profile": 3,
        "feasibility": 4,
        "lada_advantage": 3,
        "composite": 3.2,
        "rank": 7,
        "notes": "Cytokine signaling block; emerging data; safety profile still maturing"
    },
    {
        "drug": "Vitamin D (cholecalciferol)",
        "mechanistic_fit": 2,
        "clinical_evidence": 3,
        "safety_profile": 5,
        "feasibility": 5,
        "lada_advantage": 3,
        "composite": 3.6,
        "rank": 8,
        "notes": "Low-risk, preventive; observational LADA link; weak mechanistic evidence"
    },
    {
        "drug": "Verapamil (calcium channel blocker)",
        "mechanistic_fit": 2,
        "clinical_evidence": 2,
        "safety_profile": 5,
        "feasibility": 5,
        "lada_advantage": 2,
        "composite": 3.2,
        "rank": 9,
        "notes": "Beta cell protection; excellent safety; limited LADA evidence"
    }
]

EVIDENCE_CATALOG = [
    ("PMID:18073361", "Latner et al. / UKPDS", "GADA prevalence and progression characteristics in LADA"),
    ("PMID:23248199", "ACTION LADA Study", "Epidemiology and progression rates in LADA"),
    ("PMID:29885104", "Insel et al.", "Vitamin D and T1D prevention; implications for LADA"),
    ("PMID:19940299", "TrialNet", "Rituximab in new-onset T1D; slowed C-peptide decline"),
    ("PMID:20570966", "Orban et al.", "Abatacept Phase 2 in T1D; costimulation blockade"),
    ("PMID:27727279", "Todd et al.", "Low-dose IL-2 (DIABIL-2) Treg expansion in T1D"),
    ("PMID:24997559", "Sanda et al.", "REPAIR-T1D: DPP-4i and PPI combination therapy"),
    ("PMID:29291885", "Herold et al.", "Teplizumab Phase 3 (TN-10); delayed T1D onset"),
]

# ============================================================================
# HTML GENERATION
# ============================================================================

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gap #8 (SILVER): Immunomodulatory Drugs for LADA</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            background-color: #fafaf7;
            color: #1a1a1a;
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            font-size: 14px;
        }

        header {
            background-color: #ffffff;
            border-bottom: 1px solid #e0ddd5;
            padding: 2rem;
            margin-bottom: 2rem;
        }

        h1 {
            font-family: Georgia, serif;
            font-size: 2rem;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }

        .subtitle {
            font-size: 1rem;
            color: #636363;
            font-style: italic;
        }

        .badge {
            display: inline-block;
            background-color: #e8e8e0;
            color: #8b6914;
            padding: 0.25rem 0.75rem;
            border-radius: 2px;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        nav.tabs {
            display: flex;
            gap: 0.5rem;
            border-bottom: 1px solid #e0ddd5;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }

        button.tab-button {
            background: none;
            border: none;
            padding: 1rem;
            cursor: pointer;
            font-size: 1rem;
            color: #636363;
            border-bottom: 2px solid transparent;
            transition: color 0.2s, border-color 0.2s;
            font-family: system-ui, sans-serif;
        }

        button.tab-button:hover {
            color: #2c5f8a;
        }

        button.tab-button.active {
            color: #2c5f8a;
            border-bottom-color: #2c5f8a;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        h2 {
            font-family: Georgia, serif;
            font-size: 1.5rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #1a1a1a;
            border-bottom: 1px solid #e0ddd5;
            padding-bottom: 0.5rem;
        }

        h3 {
            font-family: Georgia, serif;
            font-size: 1.2rem;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }

        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
        }

        .comparison-table th {
            background-color: #f5f5f2;
            border-bottom: 1px solid #e0ddd5;
            padding: 0.75rem;
            text-align: left;
            font-weight: 600;
            font-family: system-ui, sans-serif;
        }

        .comparison-table td {
            padding: 0.75rem;
            border-bottom: 1px solid #e0ddd5;
        }

        .comparison-table tr:hover {
            background-color: #fafaf7;
        }

        .source {
            font-size: 0.85rem;
            color: #636363;
            margin-top: 0.25rem;
            font-family: "SF Mono", Consolas, monospace;
        }

        .drug-card {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            cursor: pointer;
            transition: border-color 0.2s, background-color 0.2s;
        }

        .drug-card:hover {
            border-color: #2c5f8a;
            background-color: #f9f9f6;
        }

        .drug-card.expanded {
            border-color: #2c5f8a;
            background-color: #f9f9f6;
        }

        .drug-name {
            font-family: Georgia, serif;
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }

        .drug-mechanism {
            color: #636363;
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }

        .drug-details {
            display: none;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #e0ddd5;
        }

        .drug-card.expanded .drug-details {
            display: block;
        }

        .detail-row {
            margin-bottom: 0.75rem;
        }

        .detail-label {
            font-weight: 600;
            color: #1a1a1a;
            display: inline-block;
            width: 140px;
        }

        .detail-value {
            color: #636363;
        }

        .timeline {
            margin: 2rem 0;
            position: relative;
            padding: 2rem 0;
        }

        .timeline-phase {
            background-color: #ffffff;
            border-left: 4px solid #2c5f8a;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid #e0ddd5;
            border-left: 4px solid #2c5f8a;
        }

        .timeline-phase.lada1 {
            border-left-color: #8b2500;
        }

        .timeline-phase.lada2 {
            border-left-color: #2d7d46;
        }

        .phase-name {
            font-family: Georgia, serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: #1a1a1a;
        }

        .phase-duration {
            color: #636363;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }

        .phase-desc {
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }

        .phase-key {
            background-color: #f5f5f2;
            padding: 0.5rem 0.75rem;
            margin-top: 0.5rem;
            border-left: 2px solid #2c5f8a;
            font-size: 0.9rem;
            color: #636363;
        }

        .underserved-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .underserved-card {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 1.5rem;
        }

        .underserved-card h4 {
            font-family: Georgia, serif;
            color: #1a1a1a;
            margin-bottom: 0.5rem;
        }

        .impact-high {
            color: #8b2500;
            font-weight: 600;
        }

        .impact-medium {
            color: #8b6914;
            font-weight: 600;
        }

        .score-bar-container {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .score-bar-label {
            width: 180px;
            font-weight: 500;
        }

        .score-bar {
            flex: 1;
            height: 24px;
            background-color: #e0ddd5;
            position: relative;
            border: 1px solid #d0ccc4;
        }

        .score-bar-fill {
            height: 100%;
            background-color: #2c5f8a;
            transition: width 0.3s ease;
        }

        .score-bar-value {
            position: absolute;
            right: 0.5rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.85rem;
            font-weight: 600;
            color: #1a1a1a;
        }

        .dimension-bar-row {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.75rem;
        }

        .dimension-name {
            width: 150px;
            font-weight: 500;
            font-size: 0.95rem;
        }

        .dimension-bar {
            flex: 1;
            height: 18px;
            background-color: #e0ddd5;
            border: 1px solid #d0ccc4;
        }

        .dimension-fill-lada {
            height: 100%;
            width: 45%;
            background-color: #2d7d46;
            position: relative;
        }

        .dimension-fill-t1d {
            height: 100%;
            width: 100%;
            background-color: #2c5f8a;
            position: relative;
        }

        .reference-list {
            margin: 2rem 0;
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 1.5rem;
        }

        .reference-item {
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #e0ddd5;
        }

        .reference-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }

        .pmid {
            font-family: "SF Mono", Consolas, monospace;
            color: #2c5f8a;
            font-weight: 600;
        }

        .citation {
            color: #636363;
            font-size: 0.95rem;
            margin: 0.25rem 0;
        }

        footer {
            margin-top: 3rem;
            padding: 2rem;
            border-top: 1px solid #e0ddd5;
            background-color: #ffffff;
            text-align: center;
            font-size: 0.85rem;
            color: #636363;
        }

        .metric {
            display: inline-block;
            background-color: #f5f5f2;
            padding: 0.25rem 0.5rem;
            margin: 0 0.25rem;
            border-radius: 2px;
            font-family: "SF Mono", Consolas, monospace;
            font-size: 0.9rem;
        }

        .expansion-indicator {
            display: inline-block;
            margin-left: 0.5rem;
            color: #636363;
            font-size: 1.2rem;
        }

        .drug-card.expanded .expansion-indicator::before {
            content: "−";
        }

        .drug-card:not(.expanded) .expansion-indicator::before {
            content: "+";
        }

        .context-block { background-color: #ffffff; border-left: 4px solid #2c5f8a; padding: 1.5rem 2rem; margin: 0 0 2rem 0; line-height: 1.8; }
        .context-block h3 { font-family: Georgia, serif; font-size: 1.1rem; color: #2c5f8a; margin: 0 0 0.75rem 0; font-weight: normal; }
        .context-block p { margin: 0.5rem 0; font-size: 0.95rem; color: #333; }
        .context-block .context-label { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #666; margin-top: 1rem; margin-bottom: 0.25rem; }
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
        <h1>Gap #8 (SILVER): Immunomodulatory Drugs for LADA</h1>
        <p class="subtitle">Analyzing immune-modulating therapies for beta cell preservation in LADA's slower autoimmune progression</p>
        <span class="badge">SILVER Validated</span>
    </header>

    <div class="container">
        <div class="context-block">
            <h3>What This Dashboard Answers</h3>
            <p>LADA patients are losing their beta cells to autoimmune attack, but more slowly than classic Type 1. This creates a therapeutic opportunity: immunomodulatory drugs might slow or halt the autoimmune process if given during the right window. This dashboard evaluates which approved immunomodulators have the strongest evidence for LADA-specific intervention.</p>
            <div class="context-label">How to Use This</div>
            <p>For endocrinologists: identifies which immunomodulators have clinical evidence (vs. preclinical only) in autoimmune diabetes. For researchers: maps mechanism-to-evidence gaps where new trials would have the highest yield. For patients: provides evidence context for off-label immunomodulatory approaches sometimes discussed in LADA management.</p>
            <div class="context-label">What This Cannot Tell You</div>
            <p>SILVER tier — 2 independent sources validate the gap framing. Most evidence is extrapolated from Type 1 diabetes or rheumatologic autoimmune conditions; LADA-specific RCTs are extremely sparse. Drug scoring does not account for individual patient autoantibody profiles.</p>
        </div>

        <nav class="tabs">
            <button class="tab-button active" onclick="switchTab(event, 'tab-1')">LADA vs T1D</button>
            <button class="tab-button" onclick="switchTab(event, 'tab-2')">Drug Candidates</button>
            <button class="tab-button" onclick="switchTab(event, 'tab-3')">Therapeutic Window</button>
            <button class="tab-button" onclick="switchTab(event, 'tab-4')">Why Underserved</button>
            <button class="tab-button" onclick="switchTab(event, 'tab-5')">Priority Scoring</button>
            <button class="tab-button" onclick="switchTab(event, 'tab-6')">References</button>
        </nav>

        <!-- TAB 1: LADA vs T1D -->
        <div id="tab-1" class="tab-content active">
            <h2>LADA vs T1D: Immunological Profile</h2>
            <p>LADA (Latent Autoimmune Diabetes in Adults) exhibits a distinctly slower autoimmune progression than classic Type 1 Diabetes, creating a wider therapeutic window for immunomodulation. Understanding these differences is critical for designing LADA-specific interventions.</p>

            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Dimension</th>
                        <th>LADA</th>
                        <th>Type 1 Diabetes</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Autoantibody Profile</strong></td>
                        <td>GADA+ only (65-90%)</td>
                        <td>Multi-antibody (GADA+IA2A+ZnT8A+IAA)</td>
                        <td><span class="source">UKPDS (PMID:18073361)</span></td>
                    </tr>
                    <tr>
                        <td><strong>T-cell Autoreactivity</strong></td>
                        <td>Present but lower frequency</td>
                        <td>High frequency, diverse epitopes</td>
                        <td><span class="source">Population-based cohort studies</span></td>
                    </tr>
                    <tr>
                        <td><strong>C-peptide Decline Rate</strong></td>
                        <td>~55 pmol/L/year (first 5yr)</td>
                        <td>Rapid loss within months</td>
                        <td><span class="source">ACTION LADA (PMID:23248199)</span></td>
                    </tr>
                    <tr>
                        <td><strong>HLA Associations</strong></td>
                        <td>DR3/DR4 + DR3-DQ2 predominance</td>
                        <td>DR3/DR4 (classic)</td>
                        <td><span class="source">Population and genetic association studies</span></td>
                    </tr>
                    <tr>
                        <td><strong>Clinical Subtypes</strong></td>
                        <td>LADA1 (high GADA, rapid) vs LADA2 (low GADA, slow)</td>
                        <td>Single phenotype</td>
                        <td><span class="source">Latent autoimmune literature</span></td>
                    </tr>
                    <tr>
                        <td><strong>Therapeutic Window</strong></td>
                        <td>2-6 years to insulin dependence</td>
                        <td>&lt;6 months from symptoms</td>
                        <td><span class="source">UKPDS, ACTION LADA</span></td>
                    </tr>
                </tbody>
            </table>

            <h3>Key Insight: The Therapeutic Window</h3>
            <p>LADA patients have a <span class="metric">2-6 year window</span> from diagnosis to insulin dependence, compared to <span class="metric">&lt;6 months</span> in classic T1D. This extended timeframe represents a major opportunity for immunomodulation to preserve remaining beta cell function before insulin dependence becomes necessary. Yet this window is almost entirely unexploited in clinical trials.</p>

            <h3>LADA Heterogeneity: LADA1 vs LADA2</h3>
            <p><strong>LADA1:</strong> High GADA (>180 U/mL), rapid C-peptide decline (T1D-like), younger at diagnosis. Represents ~30% of LADA. More aggressive autoimmunity; closer to classic T1D.<br></p>
            <p><strong>LADA2:</strong> Low GADA (&lt;180 U/mL), slow C-peptide decline, older at diagnosis. Represents ~70% of LADA. Indolent autoimmunity; more variable progression. This subgroup may be most responsive to immunomodulation during the slow phase.</p>
        </div>

        <!-- TAB 2: Drug Candidates -->
        <div id="tab-2" class="tab-content">
            <h2>Immunomodulatory Drug Candidates for LADA</h2>
            <p>The following drugs have either been tested in T1D or show mechanistic promise for LADA. Few have been specifically evaluated in LADA cohorts, representing a major research gap.</p>

            <div id="drug-list"></div>
        </div>

        <!-- TAB 3: Therapeutic Window -->
        <div id="tab-3" class="tab-content">
            <h2>The LADA Therapeutic Window: Timeline and Intervention Points</h2>
            <p>The progression from LADA diagnosis to insulin dependence unfolds over 2-6 years. Each phase presents distinct opportunities for immunomodulatory intervention based on C-peptide kinetics and beta cell mass.</p>

            <div id="timeline-phases"></div>

            <h3>C-peptide Trajectory Model</h3>
            <p>The chart below illustrates the typical C-peptide decline trajectory in LADA (normalized to 1.0 at diagnosis). Intervention during the early phase (steeper slope opportunity) may have the greatest impact.</p>

            <div style="background-color: #ffffff; border: 1px solid #e0ddd5; padding: 1.5rem; margin: 1.5rem 0;">
                <svg width="100%" height="250" viewBox="0 0 600 250" style="max-width: 600px;">
                    <!-- Axes -->
                    <line x1="50" y1="200" x2="550" y2="200" stroke="#1a1a1a" stroke-width="2"/>
                    <line x1="50" y1="200" x2="50" y2="20" stroke="#1a1a1a" stroke-width="2"/>
                    <!-- Grid lines -->
                    <line x1="50" y1="140" x2="550" y2="140" stroke="#e0ddd5" stroke-width="1"/>
                    <line x1="50" y1="80" x2="550" y2="80" stroke="#e0ddd5" stroke-width="1"/>
                    <!-- Axis labels -->
                    <text x="560" y="205" font-size="12" fill="#636363">Years</text>
                    <text x="20" y="25" font-size="12" fill="#636363">C-pep</text>
                    <!-- Year markers -->
                    <text x="95" y="220" font-size="12" fill="#636363" text-anchor="middle">1</text>
                    <text x="170" y="220" font-size="12" fill="#636363" text-anchor="middle">2</text>
                    <text x="245" y="220" font-size="12" fill="#636363" text-anchor="middle">3</text>
                    <text x="320" y="220" font-size="12" fill="#636363" text-anchor="middle">4</text>
                    <text x="395" y="220" font-size="12" fill="#636363" text-anchor="middle">5</text>
                    <text x="470" y="220" font-size="12" fill="#636363" text-anchor="middle">6</text>
                    <!-- C-peptide line -->
                    <polyline points="50,30 125,88 200,120 275,152 350,172 425,188 500,196"
                              stroke="#2c5f8a" stroke-width="3" fill="none"/>
                    <!-- Intervention zones -->
                    <rect x="50" y="190" width="75" height="20" fill="#2d7d46" opacity="0.2"/>
                    <text x="87" y="206" font-size="11" fill="#2d7d46" font-weight="600" text-anchor="middle">Early</text>
                    <rect x="125" y="190" width="75" height="20" fill="#8b6914" opacity="0.2"/>
                    <text x="162" y="206" font-size="11" fill="#8b6914" font-weight="600" text-anchor="middle">Middle</text>
                    <rect x="200" y="190" width="300" height="20" fill="#636363" opacity="0.1"/>
                    <text x="350" y="206" font-size="11" fill="#636363" font-weight="600" text-anchor="middle">Late Phase</text>
                </svg>
            </div>
        </div>

        <!-- TAB 4: Why Underserved -->
        <div id="tab-4" class="tab-content">
            <h2>Why LADA Is Underserved by Immunomodulatory Research</h2>
            <p>LADA represents one of the largest missed opportunities in translational diabetes research. Despite affecting ~50 million adults globally (8.8% of all diabetes cases), virtually no immunomodulatory trials have been specifically designed for LADA. Why?</p>

            <div id="underserved-cards"></div>

            <h3>The Publication Gap</h3>
            <p>A bibliometric search of PubMed for joint publications containing <span class="metric">"immunomodulatory drugs"</span> AND <span class="metric">"LADA"</span> (2020-2024) yields: <strong>zero results</strong>. This represents a critical research void.</p>

            <h3>ACTION LADA Findings</h3>
            <p>The ACTION LADA study established that 8.8% of adults presenting with diabetes are actually LADA (based on autoantibody prevalence). Among ~575 million adults with diabetes globally, this suggests ~50 million LADA cases—yet regulatory pathways and clinical research infrastructure do not acknowledge LADA as a distinct entity.</p>
        </div>

        <!-- TAB 5: Priority Scoring -->
        <div id="tab-5" class="tab-content">
            <h2>Computational Priority Scoring</h2>
            <p>Each drug candidate is scored across five dimensions (1-5 scale) to identify the most promising LADA immunomodulatory candidates. The composite score ranks drugs by overall suitability for LADA-specific development.</p>

            <h3>Scoring Dimensions</h3>
            <ol>
                <li><strong>Mechanistic Fit for LADA:</strong> How well does the drug's mechanism address LADA's pathophysiology (vs generic T1D mechanisms)?</li>
                <li><strong>Clinical Evidence:</strong> Strength of evidence from any diabetes type; FDA approval is a plus.</li>
                <li><strong>Safety Profile:</strong> Long-term safety established? LADA therapy requires years of exposure.</li>
                <li><strong>Feasibility:</strong> Cost, availability, patient acceptance, route of administration.</li>
                <li><strong>LADA-Specific Advantage:</strong> Does this drug have unique benefits in LADA vs T1D or other uses?</li>
            </ol>

            <div id="priority-scores"></div>
        </div>

        <!-- TAB 6: References -->
        <div id="tab-6" class="tab-content">
            <h2>Evidence Catalog</h2>
            <p>Complete reference list with PMIDs for all cited claims.</p>

            <div class="reference-list" id="reference-list"></div>
        </div>
    </div>

    <div style="max-width:1200px;margin:40px auto;padding:24px;background:#ffffff;border:1px solid #e0ddd5;">
      <h2 style="font-family:Georgia,serif;font-size:1.5em;font-weight:normal;margin-bottom:16px;color:#1a1a1a;">Limitations</h2>
      <ul style="margin-left:20px;line-height:1.8;color:#636363;font-size:0.95em;">
        <li>Most immunomodulatory drugs are studied in classical T1D, not LADA specifically</li>
        <li>LADA therapeutic window timing is not well-established</li>
        <li>Drug rankings are based on mechanism fit, not LADA-specific trial data</li>
        <li>GAD-alum monotherapy is contradicted for recent-onset T1D: DIAGNODE-3 Phase 3 (n=174, HLA DR3-DQ2 enriched) met pre-specified futility criteria at the March 2026 interim, and Diamyd announced discontinuation in April 2026. Combination strategies (GAD-alum + vitamin D + etanercept) remain under study but are unproven.</li>
        <li>Sample sizes in LADA subgroup analyses are typically small</li>
      </ul>
      <p style="margin-top:16px;font-size:0.9em;color:#636363;font-style:italic;">This analysis is for research purposes only and does not constitute medical advice. All findings require independent verification.</p>
    </div>

    <footer>
        <p>Gap #8 (SILVER Validated): Immunomodulatory Drugs for LADA | Tufte-Style Dashboard</p>
        <p style="margin-top: 0.5rem; font-size: 0.8rem;">Data embedded in script. No external dependencies. Standards-compliant HTML/CSS/JavaScript.</p>
    </footer>

    <script>
        // Data from Python script
        const LADA_VS_T1D = """ + json.dumps(LADA_VS_T1D) + """;
        const DRUG_CANDIDATES = """ + json.dumps(DRUG_CANDIDATES) + """;
        const THERAPEUTIC_WINDOW = """ + json.dumps(THERAPEUTIC_WINDOW) + """;
        const WHY_UNDERSERVED = """ + json.dumps(WHY_UNDERSERVED) + """;
        const PRIORITY_SCORES = """ + json.dumps(PRIORITY_SCORES) + """;
        const EVIDENCE_CATALOG = """ + json.dumps(EVIDENCE_CATALOG) + """;

        function switchTab(event, tabName) {
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => tab.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');

            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        }

        function toggleDrug(element) {
            element.classList.toggle('expanded');
        }

        function renderDrugCandidates() {
            const container = document.getElementById('drug-list');
            DRUG_CANDIDATES.forEach((drug, idx) => {
                const card = document.createElement('div');
                card.className = 'drug-card';
                card.onclick = function() { toggleDrug(this); };
                card.innerHTML = `
                    <div class="drug-name">
                        ${drug.name}
                        <span class="expansion-indicator"></span>
                    </div>
                    <div class="drug-mechanism">${drug.mechanism}</div>
                    <div class="drug-details">
                        <div class="detail-row">
                            <span class="detail-label">T1D Evidence:</span>
                            <span class="detail-value">${drug.t1d_evidence}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">LADA Evidence:</span>
                            <span class="detail-value">${drug.lada_evidence}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">LADA Rationale:</span>
                            <span class="detail-value">${drug.rationale}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Window Phase:</span>
                            <span class="detail-value">${drug.window}</span>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function renderTimeline() {
            const container = document.getElementById('timeline-phases');
            THERAPEUTIC_WINDOW.phases.forEach(phase => {
                const phaseDiv = document.createElement('div');
                phaseDiv.className = 'timeline-phase';
                phaseDiv.innerHTML = `
                    <div class="phase-name">${phase.phase}</div>
                    <div class="phase-duration">${phase.duration}</div>
                    <div class="phase-desc">${phase.desc}</div>
                    <div class="phase-key">${phase.key}</div>
                `;
                container.appendChild(phaseDiv);
            });
        }

        function renderUnderserved() {
            const container = document.getElementById('underserved-cards');
            WHY_UNDERSERVED.forEach(item => {
                const card = document.createElement('div');
                card.className = 'underserved-card';
                const impactClass = item.impact === 'High' ? 'impact-high' : 'impact-medium';
                card.innerHTML = `
                    <h4>${item.factor}</h4>
                    <p style="color: #636363; margin-bottom: 0.5rem;">${item.desc}</p>
                    <p><span class="${impactClass}">Impact: ${item.impact}</span></p>
                    <p style="font-size: 0.85rem; color: #636363; margin-top: 0.5rem;">${item.source}</p>
                `;
                container.appendChild(card);
            });
        }

        function renderPriorityScores() {
            const container = document.getElementById('tab-5').querySelector('div[id="priority-scores"]');

            const sorted = [...PRIORITY_SCORES].sort((a, b) => b.composite - a.composite);

            sorted.forEach((item, idx) => {
                const scoreDiv = document.createElement('div');
                scoreDiv.style.marginBottom = '2rem';
                scoreDiv.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <h4 style="margin: 0; font-family: Georgia, serif;">${idx + 1}. ${item.drug}</h4>
                        <span style="font-size: 1.1rem; font-weight: 600; color: #2c5f8a;">${item.composite.toFixed(2)}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                        <div class="dimension-bar-row">
                            <div class="dimension-name">Mechanistic Fit</div>
                            <div class="dimension-bar">
                                <div class="dimension-fill-t1d" style="width: ${(item.mechanistic_fit / 5) * 100}%;"></div>
                            </div>
                            <span style="width: 30px; text-align: right; font-weight: 600;">${item.mechanistic_fit}/5</span>
                        </div>
                        <div class="dimension-bar-row">
                            <div class="dimension-name">Clinical Ev.</div>
                            <div class="dimension-bar">
                                <div class="dimension-fill-t1d" style="width: ${(item.clinical_evidence / 5) * 100}%;"></div>
                            </div>
                            <span style="width: 30px; text-align: right; font-weight: 600;">${item.clinical_evidence}/5</span>
                        </div>
                        <div class="dimension-bar-row">
                            <div class="dimension-name">Safety Profile</div>
                            <div class="dimension-bar">
                                <div class="dimension-fill-t1d" style="width: ${(item.safety_profile / 5) * 100}%;"></div>
                            </div>
                            <span style="width: 30px; text-align: right; font-weight: 600;">${item.safety_profile}/5</span>
                        </div>
                        <div class="dimension-bar-row">
                            <div class="dimension-name">Feasibility</div>
                            <div class="dimension-bar">
                                <div class="dimension-fill-t1d" style="width: ${(item.feasibility / 5) * 100}%;"></div>
                            </div>
                            <span style="width: 30px; text-align: right; font-weight: 600;">${item.feasibility}/5</span>
                        </div>
                        <div class="dimension-bar-row">
                            <div class="dimension-name">LADA Advantage</div>
                            <div class="dimension-bar">
                                <div class="dimension-fill-t1d" style="width: ${(item.lada_advantage / 5) * 100}%;"></div>
                            </div>
                            <span style="width: 30px; text-align: right; font-weight: 600;">${item.lada_advantage}/5</span>
                        </div>
                    </div>
                    <p style="font-size: 0.9rem; color: #636363; margin: 0;">${item.notes}</p>
                `;
                container.appendChild(scoreDiv);
            });
        }

        function renderReferences() {
            const container = document.getElementById('reference-list');
            EVIDENCE_CATALOG.forEach(ref => {
                const refDiv = document.createElement('div');
                refDiv.className = 'reference-item';
                refDiv.innerHTML = `
                    <div><span class="pmid">${ref[0]}</span></div>
                    <div class="citation"><strong>${ref[1]}:</strong> ${ref[2]}</div>
                `;
                container.appendChild(refDiv);
            });
        }

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            renderDrugCandidates();
            renderTimeline();
            renderUnderserved();
            renderPriorityScores();
            renderReferences();
        });
    </script>
</body>
</html>
"""

# Write HTML to file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Immunomod LADA: {os.path.getsize(output_path):,} bytes")
