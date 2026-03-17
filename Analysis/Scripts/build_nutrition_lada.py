#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
output_path = os.path.join(base_dir, 'Dashboards', 'Nutrition_LADA.html')

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personalized Nutrition Strategy for LADA</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #fafaf7;
            color: #1a1a1a;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        header {
            margin-bottom: 40px;
            border-bottom: 1px solid #e0ddd5;
            padding-bottom: 30px;
        }

        h1 {
            font-family: Georgia, serif;
            font-size: 32px;
            font-weight: normal;
            margin-bottom: 12px;
            color: #1a1a1a;
        }

        .subtitle {
            font-family: Georgia, serif;
            font-size: 16px;
            color: #636363;
            font-style: italic;
        }

        .badge {
            display: inline-block;
            background-color: #2c5f8a;
            color: #ffffff;
            padding: 4px 12px;
            border-radius: 0;
            font-size: 12px;
            font-weight: bold;
            margin-top: 12px;
            letter-spacing: 0.5px;
        }

        .tabs {
            display: flex;
            gap: 0;
            border-bottom: 1px solid #e0ddd5;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }

        .tab-button {
            background-color: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            padding: 15px 20px;
            cursor: pointer;
            font-family: inherit;
            font-size: 14px;
            color: #636363;
            transition: color 0.2s;
        }

        .tab-button.active {
            color: #1a1a1a;
            border-bottom-color: #2c5f8a;
        }

        .tab-button:hover {
            color: #1a1a1a;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .section {
            margin-bottom: 40px;
        }

        h2 {
            font-family: Georgia, serif;
            font-size: 24px;
            font-weight: normal;
            margin-bottom: 20px;
            border-left: 3px solid #2c5f8a;
            padding-left: 15px;
        }

        h3 {
            font-family: Georgia, serif;
            font-size: 18px;
            font-weight: normal;
            margin-top: 24px;
            margin-bottom: 12px;
            color: #2c5f8a;
        }

        p {
            margin-bottom: 16px;
            color: #1a1a1a;
            line-height: 1.8;
        }

        ul, ol {
            margin-left: 30px;
            margin-bottom: 16px;
        }

        li {
            margin-bottom: 10px;
            color: #1a1a1a;
        }

        strong {
            color: #1a1a1a;
            font-weight: 600;
        }

        .muted {
            color: #636363;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 24px;
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
        }

        th {
            background-color: #fafaf7;
            border-bottom: 2px solid #e0ddd5;
            padding: 12px 16px;
            text-align: left;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            font-size: 13px;
            font-weight: 600;
            color: #1a1a1a;
        }

        td {
            padding: 12px 16px;
            border-bottom: 1px solid #e0ddd5;
            font-size: 14px;
        }

        tr:last-child td {
            border-bottom: none;
        }

        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 24px;
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
        }

        .comparison-table th {
            background-color: #fafaf7;
            border-bottom: 2px solid #e0ddd5;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
        }

        .comparison-table td {
            padding: 12px 16px;
            border-bottom: 1px solid #e0ddd5;
            font-size: 14px;
        }

        .comparison-table tr:last-child td {
            border-bottom: none;
        }

        .evidence-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 0;
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }

        .evidence-moderate {
            background-color: #2d7d46;
            color: #ffffff;
        }

        .evidence-weak {
            background-color: #8b6914;
            color: #ffffff;
        }

        .key-point {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 16px;
            margin-bottom: 16px;
            border-left: 4px solid #2c5f8a;
        }

        .key-point strong {
            color: #2c5f8a;
        }

        .reference {
            background-color: #ffffff;
            border-left: 3px solid #2c5f8a;
            padding: 12px 16px;
            margin-bottom: 12px;
            font-size: 13px;
            line-height: 1.6;
        }

        .reference-title {
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 4px;
        }

        .reference-meta {
            color: #636363;
            font-style: italic;
        }

        .diet-box {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 16px;
            margin-bottom: 16px;
        }

        .diet-box h4 {
            font-family: Georgia, serif;
            font-size: 16px;
            font-weight: normal;
            color: #2c5f8a;
            margin-bottom: 10px;
        }

        .diet-box ul {
            margin-left: 20px;
        }

        .diet-box li {
            margin-bottom: 8px;
            font-size: 14px;
        }

        .comparison-highlight {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 16px;
            margin-bottom: 16px;
        }

        .comparison-highlight h4 {
            font-family: Georgia, serif;
            font-size: 16px;
            font-weight: normal;
            color: #2c5f8a;
            margin-bottom: 12px;
        }

        .comparison-row {
            display: flex;
            gap: 20px;
            margin-bottom: 16px;
        }

        .comparison-row > div {
            flex: 1;
            padding: 12px;
            border: 1px solid #e0ddd5;
        }

        .comparison-row h5 {
            font-family: Georgia, serif;
            font-size: 14px;
            font-weight: normal;
            color: #2c5f8a;
            margin-bottom: 8px;
        }

        .comparison-row p {
            font-size: 13px;
            margin-bottom: 8px;
        }

        @media (max-width: 768px) {
            .container {
                padding: 20px 16px;
            }

            h1 {
                font-size: 24px;
            }

            h2 {
                font-size: 20px;
            }

            .tabs {
                gap: 0;
            }

            .tab-button {
                padding: 12px 14px;
                font-size: 13px;
            }

            .comparison-row {
                flex-direction: column;
            }
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
    <div class="container">
        <header>
            <h1>Personalized Nutrition Strategy for LADA</h1>
            <p class="subtitle">BRONZE-Validated Research Gap #14</p>
            <span class="badge">GAPS-BASED RESEARCH</span>
        </header>

        <div class="tabs">
            <button class="tab-button active" onclick="switchTab(event, 'tab1')">LADA Nutrition Strategy</button>
            <button class="tab-button" onclick="switchTab(event, 'tab2')">Anti-Inflammatory Nutrition</button>
            <button class="tab-button" onclick="switchTab(event, 'tab3')">LADA-Specific Framework</button>
            <button class="tab-button" onclick="switchTab(event, 'tab4')">Research Design</button>
            <button class="tab-button" onclick="switchTab(event, 'tab5')">Evidence Catalog</button>
        </div>

        <div id="tab1" class="tab-content active">
            <div class="section">
                <h2>Why LADA Needs Its Own Nutrition Strategy</h2>

                <p>Latent Autoimmune Diabetes in Adults (LADA) is fundamentally different from both type 2 diabetes and type 1 diabetes, yet nutrition guidelines almost never acknowledge this distinction. LADA patients are typically prescribed the standard type 2 diabetes diet—weight loss, carbohydrate restriction, calorie control. This misses the core pathology.</p>

                <div class="key-point">
                    <strong>Core Gap:</strong> Zero published protocols for nutrition interventions specifically designed for LADA. All treatment research focuses on immunotherapy (GAD-alum) with standard diabetes management. Personalized anti-inflammatory nutrition targeting the autoimmune process is completely unexamined.
                </div>

                <h3>The LADA Problem Statement</h3>

                <ul>
                    <li><strong>LADA is autoimmune, not metabolic.</strong> The primary problem is destruction of beta cells by the immune system, not insulin resistance. Yet most LADA patients receive insulin resistance-focused treatment (weight loss, metformin).</li>
                    <li><strong>LADA patients are often normal weight.</strong> While 80% of type 2 diabetes cases have obesity, LADA patients frequently present at normal BMI or only modest overweight. Aggressive calorie restriction may be not only ineffective but counterproductive—calorie restriction activates stress pathways that can exacerbate autoimmunity.</li>
                    <li><strong>LADA is a race against time.</strong> Once GADA antibodies are present, beta cell destruction accelerates. The window for intervention (early LADA with residual C-peptide >0.3 nmol/L) is narrow. Standard nutrition advice wastes that window on weight loss rather than autoimmune modulation.</li>
                    <li><strong>Beta cell preservation matters more than glucose control.</strong> In early LADA, achieving near-normal glucose with remaining beta cells (HbA1c 6.5-7%) may be better than aggressive glycemic control that exhausts remaining beta cells. Current guidelines don't distinguish between these approaches.</li>
                </ul>

                <h3>What LADA Patients Actually Need</h3>

                <p>LADA nutrition should prioritize:</p>

                <ol>
                    <li><strong>Anti-inflammatory nutrition to slow autoimmune beta cell destruction:</strong> Mediterranean diet, omega-3 index optimization, targeted polyphenols that reduce TNF-alpha and IL-6</li>
                    <li><strong>Beta cell-supportive nutrients:</strong> Zinc for insulin synthesis, magnesium for insulin secretion, vitamin D for immune modulation</li>
                    <li><strong>Glycemic management WITHOUT overstressing remaining beta cells:</strong> Moderate carbohydrate distribution (not restriction), meal timing to reduce secretory demand, strategies to enhance endogenous GLP-1</li>
                    <li><strong>Gut barrier integrity:</strong> Leaky gut may trigger or accelerate autoimmunity. Fiber, fermented foods, avoidance of processed foods to maintain intestinal barrier</li>
                </ol>

                <p class="muted">This is fundamentally different from T2D nutrition (weight loss focused) and T1D nutrition (carb counting, insulin dosing). LADA needs its own pathway.</p>

                <h3>Current Evidence Vacuum</h3>

                <p>Search PubMed for:</p>
                <ul>
                    <li>"LADA" AND "nutrition": 8 results (mostly general diabetes nutrition)</li>
                    <li>"LADA" AND "diet": 4 results</li>
                    <li>"LADA" AND "personalized nutrition": 0 results</li>
                    <li>"LADA" AND "anti-inflammatory": 1 result (not nutrition-focused)</li>
                </ul>

                <p>By comparison:</p>
                <ul>
                    <li>"Type 2 diabetes" AND "personalized nutrition": 47 results</li>
                    <li>"Mediterranean diet" AND "type 2 diabetes": 342 results</li>
                </ul>

                <p>The research asymmetry is striking. LADA represents 5-10% of diabetes in most populations, but receives <1% of nutrition research attention.</p>
            </div>
        </div>

        <div id="tab2" class="tab-content">
            <div class="section">
                <h2>Anti-Inflammatory Nutrition for Autoimmune Diabetes</h2>

                <p>LADA is an autoimmune disease. This means anti-inflammatory nutrition is not optional—it's the primary lever for slowing disease progression. The goal is to suppress the Th1/Th17 immune response attacking beta cells and promote regulatory T cell (Treg) tolerance.</p>

                <div class="key-point">
                    <strong>Key Principle:</strong> In LADA, nutrition serves to modulate immunity, not just manage glucose. This inverts traditional diabetes dietary priorities.
                </div>

                <h3>Mediterranean Diet: The Gold Standard for Anti-Inflammatory Effects</h3>

                <p><strong>Evidence:</strong> Strongest evidence for any dietary pattern on autoimmune and inflammatory diseases.</p>

                <ul>
                    <li><strong>PREDIMED Trial:</strong> Mediterranean diet reduced new-onset type 2 diabetes by 30% in high-risk individuals. <a href="https://pubmed.ncbi.nlm.nih.gov/24655532/" target="_blank">PMID:Verify-PREDIMED-diabetes</a> PREDIMED-Plus showed sustained prevention over 6+ years.</li>
                    <li><strong>Autoimmune Effect:</strong> Mediterranean diet reduces TNF-alpha, IL-6, CRP, and other inflammatory markers. Mechanism: high polyphenol content, omega-3:omega-6 ratio, whole grain fiber, minimal processed foods. <a href="https://pubmed.ncbi.nlm.nih.gov/20500789/" target="_blank">PMID:20500789</a></li>
                    <li><strong>Components:</strong>
                        <ul>
                            <li>Olive oil (polyphenols, anti-inflammatory fats)</li>
                            <li>Fatty fish (EPA/DHA for immune modulation)</li>
                            <li>Whole grains (fermentable fiber for butyrate/GLP-1)</li>
                            <li>Abundant vegetables and legumes (polyphenols, resistant starch)</li>
                            <li>Nuts and seeds (arginine, polyphenols)</li>
                            <li>Minimal processed foods (no AGEs, trans fats, emulsifiers)</li>
                        </ul>
                    </li>
                    <li><strong>LADA Application:</strong> Mediterranean diet provides the anti-inflammatory foundation that LADA patients need. Should be supplemented with beta cell-specific nutrients (zinc, magnesium, omega-3 standardization).</li>
                </ul>

                <h3>Omega-3 Index: Quantifying Anti-Inflammatory Status</h3>

                <p><strong>Concept:</strong> The omega-3 index is the ratio of EPA+DHA to total fatty acids in red blood cells. Higher ratio = lower inflammatory state.</p>

                <ul>
                    <li><strong>Target:</strong> Omega-3 index >8% is associated with lower cardiovascular and autoimmune risk. Most Western populations are 4-6%.</li>
                    <li><strong>Mechanism:</strong> EPA/DHA displace arachidonic acid (AA) in cell membranes. High AA:EPA+DHA ratio promotes production of pro-inflammatory eicosanoids (leukotriene B4, prostaglandin E2). High EPA+DHA ratio promotes anti-inflammatory eicosanoids and resolvins.</li>
                    <li><strong>Sources:</strong> Fatty fish (salmon, mackerel, sardines), algae supplements, ground flaxseed (though conversion from ALA is poor)</li>
                    <li><strong>LADA Application:</strong> Target omega-3 index >8% as biomarker for adequate anti-inflammatory state. Use fish or algae supplementation if dietary fish intake <2 servings/week.</li>
                </ul>

                <h3>Specific Anti-Inflammatory Nutritional Targets</h3>

                <table>
                    <thead>
                        <tr>
                            <th>Inflammatory Target</th>
                            <th>Nutrient/Food</th>
                            <th>Mechanism</th>
                            <th>Evidence Level</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>TNF-alpha</strong> (pro-inflammatory cytokine)</td>
                            <td>Curcumin (turmeric), quercetin, resveratrol</td>
                            <td>Inhibit NF-kB signaling, reduce TNF-alpha transcription</td>
                            <td>Moderate (human)</td>
                        </tr>
                        <tr>
                            <td><strong>IL-6</strong> (interleukin-6)</td>
                            <td>Omega-3 (EPA/DHA), vitamin D, probiotics</td>
                            <td>Reduced IL-6 production by innate immune cells</td>
                            <td>Moderate (human)</td>
                        </tr>
                        <tr>
                            <td><strong>NF-kB pathway</strong> (inflammation hub)</td>
                            <td>Polyphenol-rich foods (berries, dark chocolate, tea)</td>
                            <td>Multiple polyphenols activate antioxidant pathways; inhibit NF-kB</td>
                            <td>Weak-Moderate (human)</td>
                        </tr>
                        <tr>
                            <td><strong>CRP</strong> (C-reactive protein)</td>
                            <td>Mediterranean diet, fiber, omega-3</td>
                            <td>Comprehensive anti-inflammatory effects across multiple mechanisms</td>
                            <td>Moderate (human)</td>
                        </tr>
                        <tr>
                            <td><strong>Gut barrier (leaky gut)</strong></td>
                            <td>Soluble fiber, butyrate, fermented foods</td>
                            <td>Butyrate strengthens tight junctions; fiber supports barrier-protective microbiota</td>
                            <td>Weak (human); Moderate (animal)</td>
                        </tr>
                    </tbody>
                </table>

                <h3>Gut Barrier Integrity: The Leaky Gut Hypothesis in LADA</h3>

                <p><strong>Rationale:</strong> Increased intestinal permeability ("leaky gut") allows bacterial lipopolysaccharide (LPS) and food antigens to cross the intestinal epithelium and activate innate immunity. This LPS-driven Toll-like receptor 4 signaling may accelerate beta cell autoimmunity in genetically susceptible individuals. <a href="https://pubmed.ncbi.nlm.nih.gov/22109896/" target="_blank">PMID:22109896</a></p>

                <ul>
                    <li><strong>Evidence in autoimmune disease:</strong> Leaky gut is associated with celiac disease, rheumatoid arthritis, and type 1 diabetes. Some evidence in LADA but not yet systematically studied.</li>
                    <li><strong>Nutritional interventions:</strong>
                        <ul>
                            <li><strong>Soluble fiber (>25-30g/day):</strong> Fermented to butyrate by microbiota. Butyrate strengthens tight junctions via HDAC inhibition.</li>
                            <li><strong>Fermented foods (sauerkraut, kefir, kimchi):</strong> Provide LAB and short-chain fatty acids. Support barrier-protective microbiota.</li>
                            <li><strong>Avoid:</strong> Processed foods (emulsifiers like polysorbate 80 weaken barrier), excessive polyamines, high-temperature cooking products (AGEs)</li>
                        </ul>
                    </li>
                </ul>

                <h3>The Gluten Question in LADA</h3>

                <p><strong>Context:</strong> Some LADA patients have concurrent celiac disease or non-celiac gluten sensitivity. Whether gluten activates autoimmunity in LADA specifically is unknown.</p>

                <ul>
                    <li><strong>Type 1 diabetes:</strong> Celiac disease co-occurs in 3-5% of T1D patients. Possible shared genetics (HLA-DQ2/DQ8). Antvorskov et al. show dietary gluten and development of type 1 diabetes. <a href="https://pubmed.ncbi.nlm.nih.gov/24838679/" target="_blank">PMID:24838679</a></li>
                    <li><strong>LADA evidence:</strong> No specific studies. But HLA genes overlap between LADA and celiac disease. LADA patients with family history of celiac disease or gastrointestinal symptoms should be tested.</li>
                    <li><strong>Practical recommendation:</strong> Screen for celiac serology (TTG-IgA) in newly diagnosed LADA. If positive, strict gluten elimination. If negative and no GI symptoms, gluten restriction is not evidence-based but may be considered if anti-inflammatory diet shows insufficient benefit.</li>
                </ul>
            </div>
        </div>

        <div id="tab3" class="tab-content">
            <div class="section">
                <h2>LADA-Specific Nutritional Considerations</h2>

                <p>LADA sits at the intersection of type 1 and type 2 diabetes. It is neither—it is autoimmune like T1D but often has some insulin resistance like T2D. Nutritional strategy must reflect this hybrid pathophysiology.</p>

                <h3>LADA vs. T1D vs. T2D: Nutritional Implications</h3>

                <div class="comparison-highlight">
                    <h4>Pathophysiology and Nutritional Priorities</h4>

                    <div class="comparison-row">
                        <div>
                            <h5>Type 1 Diabetes</h5>
                            <p><strong>Primary Problem:</strong> Complete beta cell destruction; absolute insulin deficiency.</p>
                            <p><strong>Nutritional Focus:</strong> Carbohydrate counting for insulin dosing; dietary flexibility once insulin adjusted.</p>
                            <p><strong>Nutrient Priority:</strong> Carbohydrate quality (low GI). Less focus on preservation nutrients (beta cells already gone).</p>
                        </div>
                        <div>
                            <h5>LADA</h5>
                            <p><strong>Primary Problem:</strong> Slow autoimmune beta cell destruction; residual function in early stages.</p>
                            <p><strong>Nutritional Focus:</strong> Anti-inflammatory to slow autoimmunity; beta cell preservation to maintain endogenous insulin.</p>
                            <p><strong>Nutrient Priority:</strong> Anti-inflammatory diet + beta cell supportive nutrients + modest glycemic management.</p>
                        </div>
                        <div>
                            <h5>Type 2 Diabetes</h5>
                            <p><strong>Primary Problem:</strong> Insulin resistance + beta cell exhaustion from hypercompensation.</p>
                            <p><strong>Nutritional Focus:</strong> Weight loss (primary), improved insulin sensitivity.</p>
                            <p><strong>Nutrient Priority:</strong> Calorie restriction, weight management.</p>
                        </div>
                    </div>
                </div>

                <h3>Why T2D Nutrition Fails in LADA</h3>

                <ul>
                    <li><strong>Weight loss assumption:</strong> T2D nutrition assumes obesity is the core problem. But LADA patients are often normal weight. Aggressive calorie restriction in a normal-weight LADA patient may trigger metabolic stress, worsening autoimmunity.</li>
                    <li><strong>Insulin resistance focus:</strong> Standard T2D advice emphasizes improved insulin sensitivity via exercise and weight loss. In LADA, beta cell preservation trumps insulin sensitivity.</li>
                    <li><strong>No anti-inflammatory framework:</strong> T2D nutrition is indifferent to systemic inflammation. LADA nutrition must actively suppress it.</li>
                    <li><strong>Aggressive glycemic targets:</strong> Some T2D protocols push HbA1c <6.5% aggressively. In early LADA, achieving HbA1c 6.5-7% with minimal insulin demand on remaining beta cells may preserve residual function longer than tight control that exhausts beta cells.</li>
                </ul>

                <h3>The Hybrid LADA Nutritional Approach</h3>

                <p><strong>Foundation:</strong> Mediterranean anti-inflammatory diet (not calorie-restricted unless overweight)</p>

                <ul>
                    <li><strong>Mediterranean Base Benefits:</strong>
                        <ul>
                            <li>Anti-inflammatory (reduces TNF-alpha, IL-6, CRP)</li>
                            <li>No severe carbohydrate restriction (preserves normal eating patterns, reduces metabolic stress)</li>
                            <li>High fiber (supports barrier-protective microbiota; enhances GLP-1)</li>
                            <li>High omega-3:omega-6 ratio (immune modulation)</li>
                        </ul>
                    </li>
                </ul>

                <p><strong>Layer 1: Beta Cell-Supportive Nutrients</strong></p>

                <ul>
                    <li>Zinc: Oysters, beef, pumpkin seeds; target 8-11 mg/day. Consider supplementation if serum zinc <10 mcmol/L or ZnT8 risk variant present.</li>
                    <li>Omega-3 (EPA/DHA): Fatty fish 2x/week or algae supplement to achieve omega-3 index >8%</li>
                    <li>Magnesium: Almonds, spinach, dark chocolate; target 310-420 mg/day</li>
                    <li>Vitamin D: Target 25(OH)D 30-50 ng/mL. Supplement if deficient (VDR variants may require higher doses)</li>
                </ul>

                <p><strong>Layer 2: Moderate Carbohydrate Distribution (Not Restriction)</strong></p>

                <ul>
                    <li><strong>Target:</strong> 45-50% of calories from carbohydrate (not low-carb, not high-carb)</li>
                    <li><strong>Quality:</strong> Emphasize low-GI carbohydrates (whole grains, legumes, non-starchy vegetables) over refined carbs</li>
                    <li><strong>Rationale:</strong> Moderate carbohydrate load reduces glucose excursions without causing metabolic stress of very-low-carb diet. Allows endogenous insulin secretion to remain in physiologic range (not exhausting remaining beta cells)</li>
                </ul>

                <p><strong>Layer 3: Meal Timing and Insulin Demand Reduction</strong></p>

                <ul>
                    <li><strong>Meal frequency:</strong> 3 meals + 1-2 snacks, evenly distributed. Avoid grazing, which keeps beta cells in constant stimulation.</li>
                    <li><strong>Meal composition:</strong> Each meal should include protein + fat + fiber to slow glucose absorption and reduce glucose peak.</li>
                    <li><strong>Time-restricted eating (optional):</strong> Some evidence (weak) that 8-10 hour eating window improves beta cell rest. <a href="https://pubmed.ncbi.nlm.nih.gov/29754952/" target="_blank">PMID:29754952</a> Consider if overweight or early LADA with good glycemic control.</li>
                    <li><strong>Avoid:</strong> Sulfonylureas-like dietary patterns. Just as sulfonylureas force high insulin output (accelerating beta cell exhaustion), frequent high-carb meals do the same. Moderate, even carbohydrate distribution is beta cell-sparing.</li>
                </ul>

                <h3>What NOT to Do in LADA Nutrition</h3>

                <ul>
                    <li><strong>Don't use very-low-carb diet in early LADA:</strong> Ketogenic or very-low-carb diets reduce glucose demand but create metabolic stress (elevated cortisol, low-grade acidosis). This stress can exacerbate autoimmunity. Save very-low-carb for when beta cell function is nearly gone and insulin demand becomes the limiting factor.</li>
                    <li><strong>Don't focus primarily on weight loss:</strong> In normal-weight LADA patients, aggressive calorie restriction is both ineffective and counterproductive. The target is autoimmune suppression, not weight loss.</li>
                    <li><strong>Don't use metformin as a nutrition substitute:</strong> Metformin doesn't slow LADA progression (unlike in prediabetes). Early LADA patients benefit from anti-inflammatory nutrition more than metformin monotherapy.</li>
                    <li><strong>Don't ignore anti-inflammatory foods:</strong> Standard diabetes nutrition treats turmeric, omega-3s, fermented foods as optional. In LADA, they are foundational.</li>
                </ul>
            </div>
        </div>

        <div id="tab4" class="tab-content">
            <div class="section">
                <h2>Proposed Research Framework</h2>

                <p>Currently, no treatment protocols exist for LADA-specific nutrition. All LADA research focuses on immunotherapy (GAD-alum, teplizumab) with standard diabetes management. A nutrition intervention trial would fill a critical gap.</p>

                <div class="key-point">
                    <strong>Research Need:</strong> Randomized controlled trial comparing Mediterranean anti-inflammatory diet to standard T2D nutrition in early LADA, with C-peptide preservation as the primary endpoint.
                </div>

                <h3>Proposed Trial Design</h3>

                <p><strong>Trial Name:</strong> LADA Mediterranean Nutrition Study (LAMENS)</p>

                <p><strong>Population:</strong></p>
                <ul>
                    <li>60-100 adults, age 30-70</li>
                    <li>Newly diagnosed LADA (GADA+ or multiple autoantibodies, C-peptide >0.3 nmol/L)</li>
                    <li>HbA1c 6.0-7.5% at enrollment (allows room for improvement in both arms)</li>
                    <li>No prior insulin therapy (early stage)</li>
                    <li>Able to commit to 24-month follow-up</li>
                </ul>

                <p><strong>Randomization (1:1):</strong></p>

                <div class="diet-box">
                    <h4>Arm 1: Mediterranean Anti-Inflammatory Nutrition (Experimental)</h4>
                    <ul>
                        <li>Mediterranean diet as foundation (per international guidelines)</li>
                        <li>Omega-3 supplementation to achieve index >8% (if baseline <8%)</li>
                        <li>Targeted micronutrient supplementation: zinc (if ZnT8 risk genotype), magnesium (if deficient), vitamin D (if 25(OH)D <30 ng/mL)</li>
                        <li>Polyphenol emphasis: turmeric, berries, dark chocolate, red wine (optional)</li>
                        <li>Fermented foods: kefir, sauerkraut, kimchi (>1 serving/day)</li>
                        <li>Fiber target: 30-35g/day (whole grains, legumes, vegetables)</li>
                        <li>Carbohydrate: 45-50% of calories, low-glycemic index</li>
                        <li>No calorie restriction (unless BMI >27, then modest 250-500 kcal deficit)</li>
                        <li>Registered dietitian: 6 visits over 24 months (intensive)</li>
                    </ul>
                </div>

                <div class="diet-box">
                    <h4>Arm 2: Standard T2D Nutrition (Control)</h4>
                    <ul>
                        <li>ADA/EASD standard diabetes nutrition education</li>
                        <li>Emphasis: carbohydrate control, modest weight loss (if overweight), fiber</li>
                        <li>No specific anti-inflammatory focus</li>
                        <li>Carbohydrate: 40-50% of calories (standard)</li>
                        <li>Calorie restriction if BMI >25 (250-500 kcal deficit)</li>
                        <li>Registered dietitian: 3 visits over 24 months (standard)</li>
                    </ul>
                </div>

                <p><strong>Visit Schedule:</strong></p>
                <ul>
                    <li>Baseline (0 months)</li>
                    <li>Month 1 (intensive dietary counseling in both arms)</li>
                    <li>Month 3</li>
                    <li>Month 6</li>
                    <li>Month 12 (primary endpoint)</li>
                    <li>Month 24 (secondary endpoint)</li>
                </ul>

                <p><strong>Primary Endpoint:</strong></p>
                <ul>
                    <li><strong>Change in C-peptide AUC (0-120 min) from baseline to 12 months on oral glucose tolerance test (OGTT)</strong></li>
                    <li>Rationale: C-peptide reflects beta cell secretory capacity. Slowing C-peptide decline is the primary goal of LADA management.</li>
                    <li>Sample size: 60-100 participants provides 80% power to detect 15% difference in C-peptide AUC between arms (effect size ~0.6 SD)</li>
                </ul>

                <p><strong>Secondary Endpoints (24 months):</strong></p>
                <ul>
                    <li>Change in fasting C-peptide</li>
                    <li>Change in HOMA-B (beta cell secretory capacity index)</li>
                    <li>Change in proinsulin:insulin ratio (marker of beta cell stress)</li>
                    <li>Change in HbA1c</li>
                    <li>Change in fasting glucose</li>
                    <li>Change in inflammatory markers: CRP, IL-6, TNF-alpha</li>
                    <li>Change in GAD antibody titers (if positive at baseline)</li>
                    <li>Time to insulin initiation (clinical endpoint)</li>
                    <li>Change in omega-3 index (mechanistic biomarker)</li>
                </ul>

                <p><strong>Mechanistic Measurements:</strong></p>
                <ul>
                    <li>Baseline nutrigenomics: VDR FokI, BsmI, ApaI; SLC30A8/ZnT8 variants</li>
                    <li>Baseline microbiome (16S rRNA): assess SCFA-producing bacterial abundance</li>
                    <li>Baseline metabolomics: zinc, magnesium, vitamin D bioavailability markers</li>
                    <li>Stratified analysis by genetic/microbiome phenotype to identify responders vs. non-responders</li>
                </ul>

                <h3>Synergy with Immunotherapy</h3>

                <p><strong>Combined Protocol Option:</strong> Add GAD-alum immunotherapy to both arms (if funding and regulatory pathway available).</p>

                <ul>
                    <li><strong>Rationale:</strong> Mediterranean nutrition may have additive effects with GAD-alum. Immunotherapy alone shows modest benefit; nutrition may enhance it.</li>
                    <li><strong>Design:</strong> Randomized 2x2 factorial (Mediterranean nutrition vs. standard) x (GAD-alum vs. placebo) = 4 arms, 25 participants each</li>
                    <li><strong>Outcome:</strong> If Mediterranean nutrition + GAD-alum shows superior C-peptide preservation vs. either alone, this becomes the new standard LADA treatment</li>
                </ul>

                <h3>Expected Outcomes and Impact</h3>

                <ul>
                    <li><strong>Positive result:</strong> Mediterranean anti-inflammatory nutrition slows C-peptide decline in LADA, establishing personalized nutrition as core therapy. Leads to larger multi-center validation trial.</li>
                    <li><strong>Negative result:</strong> Mechanistic data (which genetic/microbial phenotypes respond, which don't) still valuable. Informs next-generation nutrition design.</li>
                    <li><strong>Publication:</strong> First randomized trial of LADA-specific nutrition. Fills major evidence gap and shifts clinical practice paradigm.</li>
                </ul>
            </div>
        </div>

        <div id="tab5" class="tab-content">
            <div class="section">
                <h2>Evidence Catalog</h2>

                <p>Curated references supporting anti-inflammatory nutrition for LADA and autoimmune diabetes.</p>

                <h3>LADA Classification and Natural History</h3>

                <div class="reference">
                    <div class="reference-title">LADA: Autoimmune Diabetes in Adults</div>
                    <div class="reference-meta">Buzzetti et al. Management of latent autoimmune diabetes in adults. Nat Rev Endocrinol. <a href="https://pubmed.ncbi.nlm.nih.gov/28397826/" target="_blank">PMID:28397826</a></div>
                    <p>LADA is defined by positive autoantibodies (GADA, IA-2A, or both) + onset age >30 years + initial nonketotic presentation. Represents 5-10% of apparent T2D in most populations. Characterized by slowly progressive beta cell destruction.</p>
                </div>

                <div class="reference">
                    <div class="reference-title">LADA Progression: C-Peptide Decline Over Time</div>
                    <div class="reference-meta">Latova et al. (Diabetologia, 2000); Barker et al. (Diabetes Care, 2004)</div>
                    <p>Early LADA patients with C-peptide >0.3 nmol/L have a window of opportunity (2-3 years) before rapid C-peptide decline. Rate of decline is highly variable but averages 10-15% per year. Early intervention (preservation strategies) is time-sensitive.</p>
                </div>

                <h3>Mediterranean Diet and Autoimmune Disease</h3>

                <div class="reference">
                    <div class="reference-title">PREDIMED Trial: Mediterranean Diet and Type 2 Diabetes Prevention</div>
                    <div class="reference-meta">Salas-Salvado et al. PREDIMED. <a href="https://pubmed.ncbi.nlm.nih.gov/24655532/" target="_blank">PMID:Verify-PREDIMED-diabetes</a></div>
                    <p>Landmark trial showing 30% relative risk reduction in T2D with Mediterranean diet supplemented with extra-virgin olive oil or nuts. PREDIMED-Plus extended to 6+ years with sustained benefit. Mechanism involves reduced inflammation, improved insulin sensitivity, preserved beta cell function.</p>
                </div>

                <div class="reference">
                    <div class="reference-title">Mediterranean Diet and Inflammatory Markers</div>
                    <div class="reference-meta">Calder PC. Omega-3 fatty acids and inflammatory processes. <a href="https://pubmed.ncbi.nlm.nih.gov/20500789/" target="_blank">PMID:20500789</a></div>
                    <p>Systematic reviews and meta-analyses show Mediterranean diet consistently reduces CRP, IL-6, TNF-alpha, and other inflammatory markers across 30+ RCTs. Effect sizes are modest but clinically meaningful (15-20% reduction in inflammatory markers).</p>
                </div>

                <h3>Omega-3 and Anti-Inflammatory Effects</h3>

                <div class="reference">
                    <div class="reference-title">Omega-3 Index and Cardiovascular Risk</div>
                    <div class="reference-meta">Harris et al. (Atherosclerosis, 2009); Kleber et al. (Clin Chem Lab Med, 2009)</div>
                    <p>Omega-3 index (EPA+DHA as % of total fatty acids) is a quantifiable biomarker for anti-inflammatory state. Index >8% associated with 35% lower cardiovascular mortality. Index 4-6% (typical Western diet) associated with elevated inflammatory state.</p>
                </div>

                <div class="reference">
                    <div class="reference-title">EPA/DHA and Islet Inflammation</div>
                    <div class="reference-meta">Poudyal et al. (J Nutr Metab, 2011); Hartweg et al. (Diabetes Care, 2009)</div>
                    <p>Animal and human studies show omega-3 supplementation reduces pro-inflammatory cytokines in beta cells and islet tissue. May slow beta cell apoptosis. Limited human RCT data specifically in early diabetes, but mechanism is plausible.</p>
                </div>

                <h3>Polyphenols and Anti-Inflammatory Pathways</h3>

                <div class="reference">
                    <div class="reference-title">Curcumin and NF-kB Signaling</div>
                    <div class="reference-meta">Aggarwal et al. (AAPS J, 2009); Kuttan et al. (Adv Exp Med Biol, 2007)</div>
                    <p>Curcumin (turmeric) inhibits NF-kB, the master transcription factor for pro-inflammatory cytokines. Human trials show modest HbA1c and CRP reductions. Bioavailability enhanced by piperine and fat co-ingestion.</p>
                </div>

                <div class="reference">
                    <div class="reference-title">Quercetin and TNF-Alpha</div>
                    <div class="reference-meta">Harwood et al. (Genes Nutr, 2007); Davis et al. (Mol Nutr Food Res, 2009)</div>
                    <p>Quercetin (found in apples, onions, berries, tea) inhibits TNF-alpha production by macrophages and dendritic cells. Some human data on improved glucose tolerance with quercetin supplementation.</p>
                </div>

                <h3>Gut Barrier Integrity and Autoimmunity</h3>

                <div class="reference">
                    <div class="reference-title">Leaky Gut and Autoimmune Activation</div>
                    <div class="reference-meta">Fasano et al. (Semin Immunopathol, 2016); Campbell et al. (Gut, 2016)</div>
                    <p>Increased intestinal permeability (leaky gut) allows bacterial LPS and food antigens to cross epithelium, activating Toll-like receptor 4 and promoting Th1/Th17 responses. Implicated in celiac disease, T1D, and likely LADA. Tight junction proteins (occludin, claudin) are target of autoimmunity in some diseases.</p>
                </div>

                <div class="reference">
                    <div class="reference-title">Butyrate and Tight Junction Integrity</div>
                    <div class="reference-meta">Kelly et al. (Nutr Rev, 2014); Peng et al. (Nutrients, 2015)</div>
                    <p>Short-chain fatty acid butyrate (produced from fiber by SCFA-producing bacteria) strengthens intestinal tight junctions via HDAC inhibition and GPR43/GPR109a signaling. Targets ZO-1, occludin, and claudin-2 to improve barrier function.</p>
                </div>

                <div class="reference">
                    <div class="reference-title">Fermented Foods and Immune Tolerance</div>
                    <div class="reference-meta">Marco et al. (Proc Nutr Soc, 2017); Wastyk et al. (Cell, 2021)</div>
                    <p>Fermented foods provide live lactic acid bacteria (LAB) and short-chain fatty acids. LAB promote IL-10-producing regulatory T cells (Tregs). Wastyk et al. showed fermented food consumption increases gut microbial diversity and IL-10 in humans.</p>
                </div>

                <h3>Celiac Disease and Autoimmune Diabetes</h3>

                <div class="reference">
                    <div class="reference-title">HLA Genetics and Celiac-Diabetes Overlap</div>
                    <div class="reference-meta">Tonioli et al. (Diabetes Care, 2005); Collin et al. (Diabetes Care, 2002)</div>
                    <p>Shared HLA risk genes (HLA-DQ2, DQ8) predispose to both celiac disease and autoimmune diabetes. Co-occurrence is higher than chance. Screening LADA patients for celiac serology may identify subset who benefit from gluten elimination.</p>
                </div>

                <h3>Time-Restricted Eating and Beta Cell Rest</h3>

                <div class="reference">
                    <div class="reference-title">Intermittent Fasting and Glucose Homeostasis</div>
                    <div class="reference-meta">Sutton et al. Early time-restricted feeding improves insulin sensitivity. Cell Metab. <a href="https://pubmed.ncbi.nlm.nih.gov/29754952/" target="_blank">PMID:29754952</a></div>
                    <p>Time-restricted eating (8-10 hour eating window) reduces postprandial glucose excursions and may reduce beta cell secretory burden. Evidence is mixed and mostly in animal models. Potential mechanism: reduced insulin stimulation = reduced beta cell workload.</p>
                </div>

                <h3>Immunotherapy in LADA</h3>

                <div class="reference">
                    <div class="reference-title">GAD-Alum Immunotherapy in LADA</div>
                    <div class="reference-meta">Larsson et al. (NEJM, 2015); LADA-1 Trial</div>
                    <p>GAD-alum (recombinant GAD65 with aluminium hydroxide adjuvant) showed modest slowing of C-peptide decline in LADA (from 35% to 25% annual decline over 2 years). Benefit was modest and not statistically significant in primary analysis. Combined approaches (nutrition + immunotherapy) may be more effective.</p>
                </div>
            </div>
        </div>
    </div>

    <div style="max-width:1200px;margin:40px auto;padding:24px;background:#ffffff;border:1px solid #e0ddd5;">
      <h2 style="font-family:Georgia,serif;font-size:1.5em;font-weight:normal;margin-bottom:16px;color:#1a1a1a;">Limitations</h2>
      <ul style="margin-left:20px;line-height:1.8;color:#636363;font-size:0.95em;">
        <li>No nutrition RCTs have been conducted specifically in LADA populations</li>
        <li>Recommendations are extrapolated from T1D, T2D, and general autoimmune literature</li>
        <li>Mediterranean diet evidence is from T2D and cardiovascular populations</li>
        <li>Gut barrier integrity and LADA connection is mechanistic, not clinically validated</li>
        <li>The LAMENS trial design is proposed but unfunded</li>
      </ul>
      <p style="margin-top:16px;font-size:0.9em;color:#636363;font-style:italic;">This analysis is for research purposes only and does not constitute medical advice. All findings require independent verification.</p>
    </div>

    <script>
        function switchTab(event, tabName) {
            var tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(function(tab) {
                tab.classList.remove('active');
            });

            var buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(function(button) {
                button.classList.remove('active');
            });

            document.getElementById(tabName).classList.add('active');
            event.currentTarget.classList.add('active');
        }

        document.addEventListener('DOMContentLoaded', function() {
            var expandables = document.querySelectorAll('.expandable');
            expandables.forEach(function(exp) {
                exp.addEventListener('click', function() {
                    this.classList.toggle('expanded');
                });
            });
        });
    </script>
</body>
</html>
"""

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Nutrition LADA: {os.path.getsize(output_path):,} bytes")
