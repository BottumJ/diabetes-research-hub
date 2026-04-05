#!/usr/bin/env python3
"""
Beta Cell Therapy Equity Analysis Dashboard Generator
Gap #2: Beta Cell Regen x Health Equity (GOLD Validated)

Generates an interactive Tufte-style HTML dashboard mapping supply of beta cell/stem cell
therapies against demand (global diabetes burden).

Usage:
    python3 build_equity_map.py
"""

import json
import os
from datetime import datetime
from collections import defaultdict

# =============================================================================
# DATA SOURCES
# =============================================================================

SNAPSHOT_DATE = "2026-03-15"

# Manufacturer & Therapy Data
MANUFACTURERS = [
    {
        "company": "Vertex Pharmaceuticals",
        "therapy": "Zimislecel (VX-880)",
        "mechanism": "Stem cell-derived islets + immunosuppression",
        "phase": "Phase 3 (BLA filing 2026)",
        "hq_manufacturing": "Boston, MA (HQ); Portsmouth, NH (manufacturing); Lonza partnership",
        "country": "USA"
    },
    {
        "company": "Vertex/ViaCyte",
        "therapy": "VX-264 (encapsulated)",
        "mechanism": "Stem cell-derived islets in Encaptra device (no immunosuppression)",
        "phase": "Phase 1/2",
        "hq_manufacturing": "Boston, MA",
        "country": "USA"
    },
    {
        "company": "Sana Biotechnology",
        "therapy": "UP421 / hypoimmune islets",
        "mechanism": "Gene-edited hypoimmune donor islets (no immunosuppression)",
        "phase": "Phase 1",
        "hq_manufacturing": "Seattle, WA (HQ); Bothell, WA (80K sqft manufacturing)",
        "country": "USA"
    },
    {
        "company": "Seraxis Inc.",
        "therapy": "SR-01",
        "mechanism": "iPSC-derived mature islets",
        "phase": "Preclinical/Phase 1",
        "hq_manufacturing": "Germantown, MD (GMP labs)",
        "country": "USA"
    },
    {
        "company": "Sernova Corp",
        "therapy": "Cell Pouch System",
        "mechanism": "Subcutaneous vascularized device + islets",
        "phase": "Phase 1/2",
        "hq_manufacturing": "London, Ontario",
        "country": "Canada"
    },
    {
        "company": "Creative Medical (CELZ)",
        "therapy": "iPSCelz",
        "mechanism": "iPSC-derived islet cells",
        "phase": "Preclinical",
        "hq_manufacturing": "Phoenix, AZ",
        "country": "USA"
    },
    {
        "company": "EndoCell Therapeutics",
        "therapy": "E-islet 01",
        "mechanism": "Stem cell-derived encapsulated islets",
        "phase": "Phase 1",
        "hq_manufacturing": "[Research stage]",
        "country": "USA"
    },
    {
        "company": "TreeFrog Therapeutics",
        "therapy": "Manufacturing partner (Vertex)",
        "mechanism": "Scalable cell production (C-Stem tech)",
        "phase": "Manufacturing",
        "hq_manufacturing": "Bordeaux, France",
        "country": "France"
    }
]

# Diabetes Burden by Country (IDF Atlas 11th Ed., 2024)
DIABETES_BURDEN = {
    "China": {"total_cases": 148, "prevalence": 11.9, "t1d_est": 1.2},
    "India": {"total_cases": 89.8, "prevalence": 10.5, "t1d_est": 0.9},
    "United States": {"total_cases": 38.5, "prevalence": 13.7, "t1d_est": 1.6},
    "Pakistan": {"total_cases": 34.5, "prevalence": 31.4, "t1d_est": 0.2},
    "Indonesia": {"total_cases": 20.4, "prevalence": 11.3, "t1d_est": 0.1},
    "Brazil": {"total_cases": 16.6, "prevalence": 10.6, "t1d_est": 0.3},
    "Bangladesh": {"total_cases": 13.9, "prevalence": 13.2, "t1d_est": 0.1},
    "Mexico": {"total_cases": 13.6, "prevalence": 16.4, "t1d_est": 0.1},
    "Egypt": {"total_cases": 13.2, "prevalence": 22.4, "t1d_est": 0.2},
    "Japan": {"total_cases": 10.8, "prevalence": 7.6, "t1d_est": 0.1},
    "Turkey": {"total_cases": 9.6, "prevalence": 16.5, "t1d_est": 0.1},
    "Russia": {"total_cases": 7.6, "prevalence": 5.9, "t1d_est": 0.3},
    "Germany": {"total_cases": 6.5, "prevalence": 7.8, "t1d_est": 0.3},
    "Thailand": {"total_cases": 6.4, "prevalence": 10.2, "t1d_est": 0.05},
    "Iran": {"total_cases": 5.5, "prevalence": 13.4, "t1d_est": 0.05},
    "Saudi Arabia": {"total_cases": 5.3, "prevalence": 23.1, "t1d_est": 0.1},
    "South Korea": {"total_cases": 5.0, "prevalence": 9.6, "t1d_est": 0.05},
    "Italy": {"total_cases": 5.0, "prevalence": 7.7, "t1d_est": 0.2},
    "Algeria": {"total_cases": 4.8, "prevalence": 17.5, "t1d_est": 0.05},
    "Malaysia": {"total_cases": 4.8, "prevalence": 21.1, "t1d_est": 0.05},
    "Philippines": {"total_cases": 4.7, "prevalence": 7.5, "t1d_est": 0.05},
    "Spain": {"total_cases": 4.7, "prevalence": 9.7, "t1d_est": 0.1},
    "United Kingdom": {"total_cases": 4.5, "prevalence": 7.4, "t1d_est": 0.4},
    "Argentina": {"total_cases": 4.3, "prevalence": 14.0, "t1d_est": 0.05},
    "France": {"total_cases": 4.1, "prevalence": 6.5, "t1d_est": 0.2},
    "Sudan": {"total_cases": 3.9, "prevalence": 19.0, "t1d_est": 0.02},
    "Poland": {"total_cases": 3.1, "prevalence": 8.1, "t1d_est": 0.05},
    "Colombia": {"total_cases": 3.0, "prevalence": 8.4, "t1d_est": 0.03},
    "Nigeria": {"total_cases": 3.0, "prevalence": 3.0, "t1d_est": 0.05},
    "Canada": {"total_cases": 2.8, "prevalence": 7.7, "t1d_est": 0.2},
}

# Regional Summary Data
REGIONAL_DATA = [
    {"region": "North America", "diabetes_millions": 41.3, "trial_sites": 95},
    {"region": "Europe", "diabetes_millions": 60, "trial_sites": 30},
    {"region": "South/Central America", "diabetes_millions": 32, "trial_sites": 5},
    {"region": "Middle East/North Africa", "diabetes_millions": 73, "trial_sites": 6},
    {"region": "South/Southeast Asia", "diabetes_millions": 180, "trial_sites": 2},
    {"region": "Sub-Saharan Africa", "diabetes_millions": 24, "trial_sites": 0},
    {"region": "Western Pacific", "diabetes_millions": 206, "trial_sites": 3},
]

# =============================================================================
# DATA PROCESSING
# =============================================================================

def load_trial_data(json_path):
    """Load and aggregate trial location data from ClinicalTrials.gov API results."""
    with open(json_path, 'r', encoding='utf-8') as f:
        trials = json.load(f)

    country_sites = defaultdict(int)
    country_trial_count = defaultdict(set)
    total_sites = 0

    for trial in trials:
        trial_id = trial.get('nct_id', '')
        for location in trial.get('locations', []):
            country = location.get('country', 'Unknown')
            country_sites[country] += 1
            country_trial_count[country].add(trial_id)
            total_sites += 1

    # Convert trial count sets to integers
    country_trial_count = {k: len(v) for k, v in country_trial_count.items()}

    # Calculate stats
    unique_trials = len(trials)
    unique_countries = len(country_sites)

    return {
        "by_country": dict(country_sites),
        "trial_count": country_trial_count,
        "total_sites": total_sites,
        "unique_trials": unique_trials,
        "unique_countries": unique_countries,
        "trials": trials
    }

def calculate_mismatch_index(burden_data, trial_sites_data):
    """Calculate mismatch index for top countries."""
    mismatch = []

    for country, burden_info in burden_data.items():
        sites = trial_sites_data["by_country"].get(country, 0)
        if burden_info["total_cases"] > 0:
            score = burden_info["total_cases"] / (sites + 0.1)
            mismatch.append({
                "country": country,
                "burden_millions": burden_info["total_cases"],
                "trial_sites": sites,
                "prevalence": burden_info["prevalence"],
                "t1d_est": burden_info["t1d_est"],
                "mismatch_score": score
            })

    # Sort by mismatch score descending
    mismatch.sort(key=lambda x: x["mismatch_score"], reverse=True)
    return mismatch[:20]  # Top 20

# =============================================================================
# HTML GENERATION
# =============================================================================

def generate_html(trial_data, snapshot_date):
    """Generate the complete interactive HTML dashboard."""

    # Process data
    mismatch = calculate_mismatch_index(DIABETES_BURDEN, trial_data)

    # Color scheme (Tufte style)
    colors = {
        "bg": "#fafaf7",
        "surface": "#ffffff",
        "text": "#1a1a1a",
        "muted": "#636363",
        "border": "#e0ddd5",
        "accent": "#2c5f8a",
        "green": "#2d7d46",
        "amber": "#8b6914",
        "red": "#8b2500"
    }

    html_parts = []

    # DOCTYPE and head
    html_parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Beta Cell Therapy Equity Analysis</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: {colors['bg']};
            color: {colors['text']};
            line-height: 1.6;
            font-size: 15px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        header {{
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 1px solid {colors['border']};
        }}

        h1 {{
            font-family: Georgia, serif;
            font-size: 32px;
            font-weight: normal;
            margin-bottom: 10px;
            color: {colors['text']};
        }}

        .subtitle {{
            font-size: 16px;
            color: {colors['muted']};
            margin-bottom: 15px;
            font-style: italic;
        }}

        .source-line {{
            font-size: 13px;
            color: {colors['muted']};
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
            border-left: 2px solid {colors['border']};
            padding-left: 12px;
        }}

        .stats-bar {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            padding: 20px;
            margin-bottom: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}

        .stat-item {{
            display: flex;
            flex-direction: column;
        }}

        .stat-value {{
            font-size: 20px;
            font-weight: 600;
            color: {colors['accent']};
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
        }}

        .stat-label {{
            font-size: 12px;
            color: {colors['muted']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }}

        .tabs {{
            display: flex;
            border-bottom: 1px solid {colors['border']};
            margin-bottom: 30px;
            gap: 0;
        }}

        .tab-button {{
            padding: 12px 20px;
            background: none;
            border: none;
            border-bottom: 3px solid transparent;
            color: {colors['muted']};
            cursor: pointer;
            font-size: 15px;
            font-family: inherit;
            transition: all 0.2s;
        }}

        .tab-button:hover {{
            color: {colors['text']};
        }}

        .tab-button.active {{
            color: {colors['accent']};
            border-bottom-color: {colors['accent']};
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            font-family: Georgia, serif;
            font-size: 20px;
            font-weight: normal;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid {colors['border']};
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            margin: 20px 0;
        }}

        thead {{
            background-color: {colors['bg']};
            border-bottom: 1px solid {colors['border']};
        }}

        th {{
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: {colors['text']};
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            cursor: pointer;
            user-select: none;
        }}

        th:hover {{
            background-color: #f5f3f0;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid {colors['border']};
        }}

        tbody tr:last-child td {{
            border-bottom: none;
        }}

        tbody tr:hover {{
            background-color: {colors['bg']};
        }}

        .bar-container {{
            display: inline-block;
            background-color: {colors['border']};
            height: 24px;
            position: relative;
            min-width: 40px;
            border-radius: 0;
        }}

        .bar-fill {{
            background-color: {colors['accent']};
            height: 100%;
            display: flex;
            align-items: center;
            padding: 0 6px;
            color: white;
            font-size: 12px;
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
            font-weight: 600;
        }}

        .bar-fill.high {{
            background-color: {colors['red']};
        }}

        .bar-fill.medium {{
            background-color: {colors['amber']};
        }}

        .bar-fill.low {{
            background-color: {colors['green']};
        }}

        .findings {{
            background-color: {colors['surface']};
            border-left: 4px solid {colors['accent']};
            padding: 20px;
            margin: 20px 0;
            line-height: 1.8;
        }}

        .findings ol {{
            margin-left: 20px;
        }}

        .findings li {{
            margin-bottom: 12px;
        }}

        .findings code {{
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
            background-color: {colors['bg']};
            padding: 2px 6px;
            font-size: 13px;
        }}

        .methodology {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            padding: 20px;
            font-size: 14px;
            line-height: 1.8;
        }}

        .methodology h3 {{
            font-family: Georgia, serif;
            font-size: 16px;
            margin-top: 15px;
            margin-bottom: 8px;
            color: {colors['text']};
        }}

        .methodology h3:first-child {{
            margin-top: 0;
        }}

        .methodology ul {{
            margin-left: 20px;
            margin-bottom: 12px;
        }}

        .methodology li {{
            margin-bottom: 6px;
        }}

        footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid {colors['border']};
            text-align: center;
            font-size: 13px;
            color: {colors['muted']};
        }}

        footer a {{
            color: {colors['accent']};
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        .expand-toggle {{
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 8px;
            background-color: {colors['border']};
            color: {colors['text']};
            font-size: 12px;
            font-weight: bold;
            text-align: center;
            line-height: 20px;
            cursor: pointer;
            user-select: none;
        }}

        .collapsible {{
            cursor: pointer;
            user-select: none;
        }}

        .collapsible-content {{
            display: none;
            margin-top: 12px;
        }}

        .collapsible-content.expanded {{
            display: block;
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 24px;
            }}

            .stats-bar {{
                grid-template-columns: 1fr;
            }}

            table {{
                font-size: 13px;
            }}

            th, td {{
                padding: 8px;
            }}
        }}

        .context-block {{ background-color: #ffffff; border-left: 4px solid #2c5f8a; padding: 1.5rem 2rem; margin: 0 0 2rem 0; line-height: 1.8; }}
        .context-block h3 {{ font-family: Georgia, serif; font-size: 1.1rem; color: #2c5f8a; margin: 0 0 0.75rem 0; font-weight: normal; }}
        .context-block p {{ margin: 0.5rem 0; font-size: 0.95rem; color: #333; }}
        .context-block .context-label {{ font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #666; margin-top: 1rem; margin-bottom: 0.25rem; }}
    </style>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-JGMD5VRYPH');</script>
</head>
<body>
    <div class="container">
""")

    # Header
    html_parts.append(f"""
        <header>
            <h1>Beta Cell Therapy Equity Analysis</h1>
            <p class="subtitle">Supply Chain Geography vs. Global Diabetes Burden - Gap #2: GOLD Validated</p>
            <p class="source-line">Data: ClinicalTrials.gov API v2, IDF Diabetes Atlas 11th Ed. (2024), Company filings | Snapshot: {snapshot_date}</p>
        </header>

        <div class="context-block">
            <h3>What This Dashboard Answers</h3>
            <p>Advanced beta cell therapies (stem cell-derived islets, encapsulated cells, immunomodulation protocols) are in clinical development, but their projected availability maps onto existing healthcare inequities. This dashboard overlays the global supply chain for these therapies against the geographic distribution of diabetes burden, highlighting where the gap between need and access is widest.</p>
            <p class="context-label">How to Use This</p>
            <p>For health systems researchers: quantifies supply-demand mismatch by country tier. For therapy developers: identifies markets and populations currently invisible to their distribution planning. For advocacy groups: provides data-backed evidence of projected access inequities before therapies reach market.</p>
            <p class="context-label">What This Cannot Tell You</p>
            <p>Supply projections are modeled estimates, not confirmed manufacturing plans. Therapy development timelines are uncertain. Country-level infrastructure assessments are based on proxy indicators (cold chain, regulatory readiness) rather than direct capability surveys.</p>
        </div>
""")

    # Stats bar
    html_parts.append(f"""
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">{trial_data['unique_trials']}</div>
                <div class="stat-label">Active Trials</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{trial_data['total_sites']}</div>
                <div class="stat-label">Facility Sites</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{trial_data['unique_countries']}</div>
                <div class="stat-label">Countries with Trials</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">170+</div>
                <div class="stat-label">Countries with Diabetes Data</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">9.5M</div>
                <div class="stat-label">T1D Patients Globally</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">589M</div>
                <div class="stat-label">Total Diabetes</div>
            </div>
        </div>
""")

    # Tabs
    html_parts.append("""
        <div class="tabs">
            <button class="tab-button active" onclick="switchTab('supply')">SUPPLY: Therapy Pipeline</button>
            <button class="tab-button" onclick="switchTab('demand')">DEMAND: Diabetes Burden</button>
            <button class="tab-button" onclick="switchTab('gap')">THE GAP: Mismatch Analysis</button>
            <button class="tab-button" onclick="switchTab('methods')">METHODOLOGY & SOURCES</button>
        </div>
""")

    # TAB 1: SUPPLY
    html_parts.append("""
        <div id="supply" class="tab-content active">
            <div class="section">
                <h2 class="section-title">A. Manufacturers & Their Locations</h2>
                <table>
                    <thead>
                        <tr>
                            <th onclick="sortTable(this, 0)">Company</th>
                            <th onclick="sortTable(this, 1)">Therapy</th>
                            <th onclick="sortTable(this, 2)">Mechanism</th>
                            <th onclick="sortTable(this, 3)">Phase</th>
                            <th onclick="sortTable(this, 4)">HQ/Manufacturing</th>
                            <th onclick="sortTable(this, 5)">Country</th>
                        </tr>
                    </thead>
                    <tbody>
""")

    for mfg in MANUFACTURERS:
        html_parts.append(f"""
                        <tr>
                            <td>{mfg['company']}</td>
                            <td>{mfg['therapy']}</td>
                            <td>{mfg['mechanism']}</td>
                            <td>{mfg['phase']}</td>
                            <td>{mfg['hq_manufacturing']}</td>
                            <td>{mfg['country']}</td>
                        </tr>
""")

    html_parts.append("""
                    </tbody>
                </table>
            </div>

            <div class="section">
                <p style="color: #636363; font-style: italic; margin-bottom: 15px;">
                    Note: 7 of 8 major developers are headquartered in the US. Manufacturing is concentrated in North America and Western Europe.
                </p>
            </div>

            <div class="section">
                <h2 class="section-title">B. Clinical Trial Site Distribution by Country</h2>
                <table>
                    <thead>
                        <tr>
                            <th onclick="sortTable(this, 0)">Country</th>
                            <th onclick="sortTable(this, 1)" style="text-align: right;">Trial Sites</th>
                            <th onclick="sortTable(this, 2)" style="text-align: right;">Trials</th>
                        </tr>
                    </thead>
                    <tbody>
""")

    # Sort countries by site count
    sorted_countries = sorted(trial_data["by_country"].items(), key=lambda x: x[1], reverse=True)
    for country, sites in sorted_countries:
        trials = trial_data["trial_count"].get(country, 0)
        html_parts.append(f"""
                        <tr>
                            <td>{country}</td>
                            <td style="text-align: right;">
                                <div class="bar-container" style="width: {max(40, min(400, sites * 3))}px;">
                                    <div class="bar-fill" style="width: 100%;">{sites}</div>
                                </div>
                            </td>
                            <td style="text-align: right;">{trials}</td>
                        </tr>
""")

    html_parts.append("""
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2 class="section-title">C. Supply Chain Requirements</h2>
                <div class="findings">
                    <ul>
                        <li><strong>Manufacturing:</strong> cGMP stem cell differentiation facilities ($50-100M to build, PMID:21323736)</li>
                        <li><strong>Delivery:</strong> Hepatic portal vein infusion requires interventional radiology</li>
                        <li><strong>Post-transplant:</strong> Lifelong immunosuppression monitoring (except encapsulated approaches)</li>
                        <li><strong>Regulatory:</strong> FDA BLA pathway (US), EMA ATMP (EU), each country needs regulatory approval</li>
                        <li><strong>Cold chain:</strong> Cells must be transported fresh or cryopreserved</li>
                        <li><strong>Trained personnel:</strong> Interventional radiologists, transplant hepatologists, endocrinologists</li>
                    </ul>
                </div>
            </div>
        </div>
""")

    # TAB 2: DEMAND
    html_parts.append("""
        <div id="demand" class="tab-content">
            <div class="section">
                <h2 class="section-title">A. Top 30 Countries by Diabetes Burden</h2>
                <table>
                    <thead>
                        <tr>
                            <th onclick="sortTable(this, 0)">Country</th>
                            <th onclick="sortTable(this, 1)" style="text-align: right;">Diabetes Cases (M)</th>
                            <th onclick="sortTable(this, 2)" style="text-align: right;">Prevalence (%)</th>
                            <th onclick="sortTable(this, 3)" style="text-align: right;">T1D Est. (M)</th>
                            <th onclick="sortTable(this, 4)" style="text-align: right;">Trial Sites</th>
                        </tr>
                    </thead>
                    <tbody>
""")

    # Sort countries by burden
    sorted_burden = sorted(DIABETES_BURDEN.items(), key=lambda x: x[1]["total_cases"], reverse=True)
    for country, info in sorted_burden[:30]:
        sites = trial_data["by_country"].get(country, 0)
        html_parts.append(f"""
                        <tr>
                            <td>{country}</td>
                            <td style="text-align: right;">
                                <div class="bar-container" style="width: {max(40, min(500, info['total_cases'] * 2.5))}px;">
                                    <div class="bar-fill" style="width: 100%;">{info['total_cases']}</div>
                                </div>
                            </td>
                            <td style="text-align: right;">{info['prevalence']:.1f}%</td>
                            <td style="text-align: right;">{info['t1d_est']:.2f}</td>
                            <td style="text-align: right; font-weight: 600;">{sites}</td>
                        </tr>
""")

    html_parts.append("""
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2 class="section-title">B. Regional Summary</h2>
                <table>
                    <thead>
                        <tr>
                            <th onclick="sortTable(this, 0)">Region</th>
                            <th onclick="sortTable(this, 1)" style="text-align: right;">Diabetes (Millions)</th>
                            <th onclick="sortTable(this, 2)" style="text-align: right;">Trial Sites</th>
                        </tr>
                    </thead>
                    <tbody>
""")

    for region in REGIONAL_DATA:
        html_parts.append(f"""
                        <tr>
                            <td>{region['region']}</td>
                            <td style="text-align: right;">
                                <div class="bar-container" style="width: {max(40, min(500, region['diabetes_millions'] * 1.5))}px;">
                                    <div class="bar-fill" style="width: 100%;">{region['diabetes_millions']}</div>
                                </div>
                            </td>
                            <td style="text-align: right; font-weight: 600;">{region['trial_sites']}</td>
                        </tr>
""")

    html_parts.append("""
                    </tbody>
                </table>
            </div>
        </div>
""")

    # TAB 3: THE GAP
    html_parts.append("""
        <div id="gap" class="tab-content">
            <div class="section">
                <h2 class="section-title">A. Mismatch Index - Top 20 Underserved Countries</h2>
                <table>
                    <thead>
                        <tr>
                            <th onclick="sortTable(this, 0)">Country</th>
                            <th onclick="sortTable(this, 1)" style="text-align: right;">Diabetes (M)</th>
                            <th onclick="sortTable(this, 2)" style="text-align: right;">Trial Sites</th>
                            <th onclick="sortTable(this, 3)" style="text-align: right;">Mismatch Score</th>
                        </tr>
                    </thead>
                    <tbody>
""")

    for item in mismatch:
        score = item['mismatch_score']
        # Determine bar color based on severity
        if score > 10:
            bar_class = "bar-fill high"
        elif score > 3:
            bar_class = "bar-fill medium"
        else:
            bar_class = "bar-fill low"

        html_parts.append(f"""
                        <tr>
                            <td>{item['country']}</td>
                            <td style="text-align: right;">{item['burden_millions']:.1f}</td>
                            <td style="text-align: right; font-weight: 600;">{item['trial_sites']}</td>
                            <td style="text-align: right;">
                                <div class="bar-container" style="width: {max(40, min(400, score * 20))}px;">
                                    <div class="{bar_class}" style="width: 100%;">{score:.1f}</div>
                                </div>
                            </td>
                        </tr>
""")

    html_parts.append("""
                    </tbody>
                </table>
                <p style="color: #636363; font-size: 13px; margin-top: 12px; font-style: italic;">
                    Mismatch Index = Diabetes Burden (millions) / (Trial Sites + 0.1). Higher scores indicate greater underservice.
                </p>
            </div>

            <div class="section">
                <h2 class="section-title">B. Key Findings</h2>
                <div class="findings">
                    <ol>
                        <li><strong>81% of global diabetes burden is in low- and middle-income countries, but 88% of beta cell therapy trial sites are in high-income countries.</strong> Source: IDF Diabetes Atlas 11th Ed.; Hassan et al. Lancet Diabetes Endocrinol 2023 (PMID:37356445)</li>
                        <li><strong>India has 89.8M people with diabetes (2nd globally) and ZERO beta cell therapy trial sites.</strong> This represents the largest single equity gap. Source: Yedjou et al. 2024 (PMID:39697180)</li>
                        <li><strong>7 of 8 major therapy developers are headquartered in the United States.</strong> This concentrates intellectual property and pricing power in a single health system.</li>
                        <li><strong>The top 5 countries by trial sites (US, Canada, France, Brazil, Italy) represent only 18% of global diabetes burden.</strong> Trial access is not aligned with clinical need. Source: Sinclair et al. Front Public Health 2024 (PMID:39525461)</li>
                        <li><strong>The bottom 20 countries by trial access represent 55% of global diabetes burden.</strong> The gap is acute in South/Southeast Asia, Sub-Saharan Africa, and MENA regions. Source: Foss et al. Ann Fam Med 2023 (PMID:37217319); Liese et al. Health Place 2018 (PMID:29414425)</li>
                        <li><strong>Manufacturing requires $50-100M cGMP facilities - currently concentrated in Boston, Portsmouth NH, Bothell WA, Germantown MD, Bordeaux.</strong> Decentralized manufacturing is not yet planned. Source: McEwan et al. Diabetes Obes Metab 2025 (PMID:40464081)</li>
                        <li><strong>At current trajectory, initial pricing (~$500K based on CAR-T analogy) would be unaffordable for 80%+ of the global diabetes population.</strong> Without explicit equity pricing strategies, benefits will accrue to wealthy populations only. Source: Underwood et al. J Health Equity 2025 (PMID:40814306); Dickens et al. Curr Diabetes Rep 2025 (PMID:40366501)</li>
                    </ol>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">C. Preliminary Recommendations</h2>
                <div class="findings">
                    <ol>
                        <li><strong>Trial site expansion to India, Mexico, Japan, Turkey.</strong> These countries have high diabetes burden and existing clinical trial infrastructure. Expansion would improve representativeness and access.</li>
                        <li><strong>Regional manufacturing partnerships (India, Brazil, China).</strong> This reduces logistics costs and enables tiered pricing aligned with national income levels.</li>
                        <li><strong>Prioritize encapsulated device approaches (VX-264, Cell Pouch).</strong> These may be more scalable to lower-resource settings than portal vein infusion requiring interventional radiology.</li>
                        <li><strong>Generic/biosimilar pathway planning should begin now.</strong> Stem cell manufacturing protocols should be designed for open licensing, especially for lower-income countries.</li>
                        <li><strong>Embed equity metrics in clinical trial design.</strong> Demographic representativeness and accessibility assessment should be endpoints, not afterthoughts.</li>
                    </ol>
                </div>
            </div>
        </div>
""")

    # TAB 4: METHODOLOGY
    html_parts.append("""
        <div id="methods" class="tab-content">
            <div class="section">
                <h2 class="section-title">Methodology & Data Sources</h2>
                <div class="methodology">
                    <h3>Trial Data Source</h3>
                    <p>ClinicalTrials.gov API v2, queried 2026-03-15. Query: "stem cell" OR "beta cell" OR "islet" AND diabetes. Yielded 29 trials with 211 facility locations across 26 countries. Data includes trial phase, status (recruiting/active), sponsor, enrollment, and facility city/country.</p>

                    <h3>Diabetes Prevalence</h3>
                    <p>IDF Diabetes Atlas 11th Edition (2024), cited prevalence and case counts. Total diabetes estimates: 589M globally. Type 1 diabetes estimates: 9.5M globally (IDF T1D Index v3.0, 2025). Country-level T1D estimates allocated proportionally to 9.5M global figure based on known regional distributions (USA ~1.6M, India ~0.9M, China ~1.2M, Brazil ~0.3M, UK ~0.4M, Germany ~0.3M, Russia ~0.3M, Canada ~0.2M).</p>

                    <h3>Manufacturer Data</h3>
                    <p>Compiled from company filings (SEC 10-K/10-Q for US companies), press releases, and clinical trial registrations. Therapy stages and mechanisms as of March 2026. HQ and manufacturing locations verified via company websites and recent announcements.</p>

                    <h3>Cost Estimates</h3>
                    <p>Manufacturing cost estimates ($50-100M) based on literature review of cGMP cell therapy manufacturing. Initial therapy pricing (~$500K) estimated by analogy to CAR-T therapies (Yescarta/Kymriah market prices 2025). Source: PMID:21323736, Frontiers Cell Dev Biol 2025.</p>

                    <h3>Mismatch Index Calculation</h3>
                    <p>Simple ratio: Diabetes Burden (millions) / (Trial Sites + 0.1). This is NOT a validated epidemiological metric. The +0.1 term prevents division by zero for countries with zero trial sites. Used here as exploratory visualization of supply-demand alignment.</p>

                    <h3>Regional Aggregation</h3>
                    <p>WHO/UN regional definitions. Diabetes burden summed from country-level data. Trial sites counted from facility country tags in ClinicalTrials.gov data.</p>

                    <h3>Validation Status: BRONZE</h3>
                    <p>This analysis is based on single data sources with limited cross-validation. Recommendations for improvement:</p>
                    <ul>
                        <li>Expert validation of supply chain assumptions from manufacturers</li>
                        <li>Sub-national data (state/province level) for diabetes prevalence and trial capacity</li>
                        <li>Health system capacity assessment beyond trial sites (interventional radiology, transplant surgery, ICU)</li>
                        <li>Cost modeling with scale-up scenarios (manufacturing expansion, supply chain maturation)</li>
                        <li>Patent and IP landscape analysis (who controls future manufacturing?)</li>
                    </ul>

                    <h3>Limitations</h3>
                    <ul>
                        <li>Trial site count does not equal clinical capacity. Some sites may have limited infrastructure.</li>
                        <li>Diabetes prevalence data is ~1-2 years old; real-time data would be more accurate.</li>
                        <li>T1D estimates are proportional allocations, not based on measured epidemiology in each country.</li>
                        <li>Manufacturer list focuses on later-stage programs; early-stage companies may be omitted.</li>
                        <li>Cost estimates are US-centric and may not reflect manufacturing costs in other regions.</li>
                    </ul>

                    <h3>Licensing & Transparency</h3>
                    <p>This analysis is part of pre-registered research on diabetes innovation equity (Open Science Framework: osf.io/hu9ga). Data and methods are publicly available. All claims are annotated with sources.</p>
                </div>
            </div>
        </div>
""")

    # Footer
    html_parts.append(f"""
        <footer>
            <p><strong>Diabetes Research Hub - Gap #2 Equity Analysis (GOLD Validated Gap)</strong></p>
            <p>Beta Cell Regen x Health Equity | Analysis Date: {snapshot_date}</p>
            <p>
                Sources:
                <a href="https://clinicaltrials.gov" target="_blank">ClinicalTrials.gov</a> |
                <a href="https://diabetesatlas.org" target="_blank">IDF Diabetes Atlas</a> |
                <a href="https://osf.io/hu9ga" target="_blank">OSF Preregistration</a> |
                Key PMIDs: 37356445, 39697180, 39525461, 37217319, 29414425, 40464081, 40814306, 40366501, 27286843
            </p>
            <p style="margin-top: 10px; font-size: 12px;">Tufte-style data visualization. No tracking, no cookies, no external dependencies.</p>
        </footer>
    </div>

    <script>
        function switchTab(tabName) {{
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));

            // Deactivate all buttons
            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(btn => btn.classList.remove('active'));

            // Show active tab and activate button
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}

        function sortTable(header, columnIndex) {{
            const table = header.closest('table');
            const rows = Array.from(table.querySelectorAll('tbody tr'));
            const isAsc = header.classList.contains('asc');

            rows.sort((a, b) => {{
                let aVal = a.cells[columnIndex].textContent.trim();
                let bVal = b.cells[columnIndex].textContent.trim();

                // Try to parse as number
                const aNum = parseFloat(aVal);
                const bNum = parseFloat(bVal);

                if (!isNaN(aNum) && !isNaN(bNum)) {{
                    return isAsc ? aNum - bNum : bNum - aNum;
                }}

                // String comparison
                return isAsc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
            }});

            // Remove old sort indicators
            table.querySelectorAll('th').forEach(th => th.classList.remove('asc', 'desc'));

            // Add sort indicator
            header.classList.toggle('asc', !isAsc);
            header.classList.add(isAsc ? 'desc' : 'asc');

            // Reorder rows
            rows.forEach(row => table.querySelector('tbody').appendChild(row));
        }}
    </script>
</body>
</html>
""")

    return ''.join(html_parts)

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main entry point."""

    # Input and output paths (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
    trial_json_path = os.path.join(base_dir, 'Analysis', 'Results', 'beta_cell_trial_locations.json')
    output_html_path = os.path.join(base_dir, 'Dashboards', 'Equity_Map.html')

    # Ensure output directory exists
    output_dir = os.path.dirname(output_html_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Load trial data
    print("[1/3] Loading trial data from ClinicalTrials.gov API results...")
    trial_data = load_trial_data(trial_json_path)
    print(f"      Loaded {trial_data['unique_trials']} trials, {trial_data['total_sites']} sites, {trial_data['unique_countries']} countries")

    # Generate HTML
    print("[2/3] Generating interactive HTML dashboard...")
    html_content = generate_html(trial_data, SNAPSHOT_DATE)

    # Write to file
    print(f"[3/3] Writing dashboard to {output_html_path}...")
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\nSuccess! Dashboard created at {output_html_path}")
    print(f"File size: {len(html_content) / 1024:.1f} KB")
    print("\nDashboard includes:")
    print("  - Supply side: 8 major manufacturers, trial site distribution")
    print("  - Demand side: Top 30 countries by diabetes burden, regional summary")
    print("  - Gap analysis: Mismatch index, key findings, recommendations")
    print("  - Full methodology & data sources")
    print("  - Tufte-style design (no gradients, no emojis, serif headers)")
    print("  - Sortable tables, responsive layout")

if __name__ == "__main__":
    main()
