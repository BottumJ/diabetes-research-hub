#!/usr/bin/env python3
"""
Rebuild Research_Dashboard.html in Tufte-informed design style.
Extracts all data from the current dashboard and regenerates as a clean,
research-credible single-file HTML document.
"""

import json
import os
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# DATA: All 55 pipeline entries
# ═══════════════════════════════════════════════════════════════════════════

PIPELINE_DATA = [
    {"domain":"T1D","cat":"Cure - Stem Cell","name":"Zimislecel (VX-880)","org":"Vertex","mech":"Stem cell islets + immunosuppression","phase":"Phase 3","result":"10/12 insulin-independent at 1yr; 50 enrolled (PMID:40544428)","status":"Active","badge":"badge-green"},
    {"domain":"T1D","cat":"Cure - Stem Cell","name":"Engineered Islets (SC451)","org":"Sana Biotech","mech":"Gene-edited immune-evasive islets","phase":"Phase 1","result":"Insulin at 6 months without immunosuppression","status":"Active","badge":"badge-blue"},
    {"domain":"T1D","cat":"Cure - Stem Cell","name":"CRISPR-Edited Islets","org":"Sana / Uppsala","mech":"CRISPR immune evasion","phase":"Phase 1","result":"Patient producing insulin without immunosuppressants","status":"Active","badge":"badge-blue"},
    {"domain":"T1D","cat":"Cure - Stem Cell","name":"iPSC Autologous Islets","org":"Chinese Team","mech":"Patient's own iPSC reprogrammed","phase":"Case Study","result":"Insulin independence with own cells","status":"Monitoring","badge":"badge-orange"},
    {"domain":"T1D","cat":"Cure - Stem Cell","name":"Sernova Cell Pouch","org":"Sernova Corp","mech":"Implantable islet device","phase":"Phase 1/2","result":"Insulin independence >5 years","status":"Active","badge":"badge-blue"},
    {"domain":"T1D","cat":"Cure - Stem Cell","name":"3D Pancreatic Organoids","org":"Multiple","mech":"Vascularized 3D models","phase":"Research","result":"Enhanced beta cell maturation","status":"Research","badge":"badge-purple"},
    {"domain":"T1D","cat":"Cure - Stem Cell","name":"Autologous MSC Islets","org":"Clinical Trial","mech":"Adipose MSC → insulin cells","phase":"Phase 1","result":"Trial in youth T1D initiated 2025","status":"Enrolling","badge":"badge-orange"},
    {"domain":"T1D","cat":"Cure - Immune","name":"CAR-Treg Bodyguards","org":"MUSC / BT1D","mech":"CAR-Treg protection","phase":"Preclinical","result":"CAR-Tregs protect beta cells","status":"Active","badge":"badge-purple"},
    {"domain":"T1D","cat":"Cure - Immune","name":"Hybrid Immune System","org":"Stanford","mech":"Blood stem cell + islet co-transplant","phase":"Preclinical","result":"Early preclinical data show protection in animal models; human data pending","status":"Active","badge":"badge-cyan"},
    {"domain":"T1D","cat":"Cure - Immune","name":"ABA-201 TCR-Tregs","org":"Abata Therapeutics","mech":"T1D-specific engineered Tregs","phase":"Phase 1","result":"First T1D-specific Treg therapy","status":"Active","badge":"badge-blue"},
    {"domain":"T1D","cat":"Cure - Gene Therapy","name":"KRIYA-839","org":"Kriya Therapeutics","mech":"Insulin + glucokinase gene delivery","phase":"Preclinical","result":"Gene-based insulin in muscle","status":"Early Stage","badge":"badge-purple"},
    {"domain":"T1D","cat":"Prevention","name":"Tzield (Teplizumab)","org":"Provention/Sanofi","mech":"Anti-CD3 immunotherapy","phase":"Phase 3","result":"Approved Stage 2; PETITE in children","status":"Approved","badge":"badge-green"},
    {"domain":"T1D","cat":"Prevention","name":"Baricitinib (BARICADE)","org":"Eli Lilly","mech":"JAK inhibitor","phase":"Phase 3","result":"Oral pill; preserved C-peptide","status":"Enrolling 2026","badge":"badge-orange"},
    {"domain":"T1D","cat":"Prevention","name":"T1D Screening Programs","org":"TrialNet / ADA","mech":"Autoantibody screening","phase":"Clinical","result":"Population screening for pre-symptomatic T1D","status":"Active","badge":"badge-green"},
    {"domain":"T1D","cat":"Treatment","name":"Tegoprubart (AT-1501)","org":"Eledon Pharma","mech":"Anti-CD40L antibody","phase":"Phase 2","result":"Early clinical data reported insulin independence in initial cohort (small N, unconfirmed by peer review)","status":"Active","badge":"badge-green"},
    {"domain":"T1D","cat":"Technology","name":"Inreda Bihormonal AP","org":"Inreda Diabetic","mech":"Insulin + glucagon closed loop","phase":"Research","result":"80% TIR vs 60% standard","status":"Testing","badge":"badge-cyan"},
    {"domain":"T1D","cat":"Technology","name":"Eversense-3 CGM","org":"Senseonics","mech":"6-month implantable sensor","phase":"Approved","result":"6-month wear; FDA approved","status":"Approved","badge":"badge-green"},
    {"domain":"T1D","cat":"Technology","name":"Deep RL Controller","org":"Academic","mech":"Deep reinforcement learning","phase":"Research","result":"87.45% TIR; lower hypos","status":"Research","badge":"badge-purple"},
    {"domain":"T1D","cat":"Technology","name":"Omnipod 5 / CamAPS FX","org":"Insulet/CamDiab","mech":"Tubeless pump + CGM","phase":"Approved","result":"Tubeless automated delivery","status":"Approved","badge":"badge-green"},
    {"domain":"T2D","cat":"GLP-1 Therapy","name":"Retatrutide","org":"Eli Lilly","mech":"GLP-1/GIP/Glucagon triple","phase":"Phase 3","result":"28.7% weight loss at 68wk","status":"Active","badge":"badge-green"},
    {"domain":"T2D","cat":"GLP-1 Therapy","name":"Orforglipron","org":"Eli Lilly","mech":"Oral GLP-1","phase":"Phase 3","result":"Once-daily pill; strong results","status":"FDA 2026","badge":"badge-orange"},
    {"domain":"T2D","cat":"GLP-1 Therapy","name":"CagriSema","org":"Novo Nordisk","mech":"Semaglutide + cagrilintide","phase":"Phase 3","result":"Dual-hormone combination","status":"FDA 2026","badge":"badge-orange"},
    {"domain":"T2D","cat":"GLP-1 Therapy","name":"Tirzepatide for T1D","org":"Eli Lilly","mech":"GLP-1/GIP dual agonist","phase":"Phase 3","result":"SURPASS-T1D trials enrolling","status":"Enrolling","badge":"badge-orange"},
    {"domain":"T2D","cat":"Novel Therapy","name":"Dorzagliatin","org":"Hua Medicine","mech":"Glucokinase activator","phase":"Phase 1b","result":"First-in-class; GK sensor repair","status":"Active","badge":"badge-blue"},
    {"domain":"T2D","cat":"Novel Therapy","name":"Insulin Icodec","org":"Novo Nordisk","mech":"Once-weekly insulin","phase":"Phase 3","result":"Non-inferior to daily basal","status":"FDA 2026","badge":"badge-orange"},
    {"domain":"T2D","cat":"Novel Therapy","name":"Efsitora Alpha","org":"Eli Lilly","mech":"Once-weekly insulin","phase":"Phase 3","result":"Weekly insulin alternative","status":"Active","badge":"badge-green"},
    {"domain":"T2D","cat":"Novel Therapy","name":"Multi-Agonist Peptides","org":"Multiple","mech":"Incretin + amylin combos","phase":"Phase 2-3","result":"Hybrid metabolic therapy","status":"Active","badge":"badge-blue"},
    {"domain":"T2D","cat":"Novel Therapy","name":"miRNA Therapies","org":"Academic","mech":"MicroRNA modulation","phase":"Preclinical","result":"miRNA linked to T2D pathways","status":"Research","badge":"badge-purple"},
    {"domain":"T2D","cat":"Remission","name":"SGLT2i + Calorie Restriction","org":"Multiple","mech":"Metabolic reset combo","phase":"RCT","result":"Early trial data report ~44% remission rate with combination approach (peer-reviewed publication pending)","status":"Published","badge":"badge-cyan"},
    {"domain":"T2D","cat":"Remission","name":"Beta Cell Recovery","org":"Multiple","mech":"Dedifferentiation reversal","phase":"Research","result":"T2D remission via beta cell recovery","status":"Published","badge":"badge-cyan"},
    {"domain":"T2D","cat":"Prevention","name":"Diabetes Prevention Program","org":"CDC/NIDDK","mech":"Lifestyle intervention","phase":"Implemented","result":"58% risk reduction; 3% enrollment","status":"Active","badge":"badge-teal"},
    {"domain":"T2D","cat":"Prevention","name":"Multilevel Community Programs","org":"Public Health","mech":"Community + system interventions","phase":"Research","result":"Multi-level approach to reduce disparities","status":"Research","badge":"badge-teal"},
    {"domain":"Cross","cat":"Drug Repurposing","name":"Metformin for Cancer","org":"Multiple","mech":"Anti-cancer + metabolic","phase":"Research","result":"Antidiabetic drugs show anticancer effects","status":"Research","badge":"badge-indigo"},
    {"domain":"Cross","cat":"Drug Repurposing","name":"GLP-1RAs Beyond Diabetes","org":"Multiple","mech":"CV + renal protection","phase":"Phase 3","result":"Reduce CV events, slow CKD","status":"Active","badge":"badge-indigo"},
    {"domain":"Biomarkers","cat":"Proteomics","name":"UK Biobank Proteomics","org":"AstraZeneca/CGR","mech":"Proteomic profiling","phase":"Published","result":"617 proteins; FAM3D target","status":"Published","badge":"badge-pink"},
    {"domain":"Biomarkers","cat":"Multi-Omics","name":"AI Multi-Omics","org":"Multiple / AI","mech":"ML on combined omics","phase":"Research","result":"Integrated biomarker framework","status":"Active","badge":"badge-pink"},
    {"domain":"Biomarkers","cat":"Epigenetics","name":"DIAMANTE CpG Analysis","org":"Multi-Ethnic","mech":"DNA methylation mapping","phase":"Published","result":"1,120 CpGs; CAMK1D mechanisms","status":"Published","badge":"badge-pink"},
    {"domain":"Biomarkers","cat":"Metabolomics","name":"DN Metabolite Markers","org":"Multiple","mech":"Urine metabolomics","phase":"Published","result":"High accuracy in discovery cohort; external validation in larger cohorts pending","status":"Published","badge":"badge-pink"},
    {"domain":"Biomarkers","cat":"Inflammatory","name":"TNF-α Marker","org":"Multiple","mech":"Inflammatory profiling","phase":"Published","result":"Predicts DN, retinopathy, CVD","status":"Published","badge":"badge-pink"},
    {"domain":"AI/ML","cat":"Prediction","name":"ML Risk Models","org":"Multiple","mech":"XGBoost, RF, SVM, CNN","phase":"Research","result":"Non-obvious diabetes predictors","status":"Active","badge":"badge-indigo"},
    {"domain":"AI/ML","cat":"Complications","name":"AI Complication Forecast","org":"Multiple","mech":"Deep learning","phase":"Research","result":"FDA-approved detection models","status":"Active","badge":"badge-indigo"},
    {"domain":"AI/ML","cat":"Drug Discovery","name":"AI Drug Repurposing","org":"Multiple","mech":"Perturbation models","phase":"Research","result":"20 T2D drug connections found","status":"Research","badge":"badge-indigo"},
    {"domain":"AI/ML","cat":"Clinical","name":"AI Retinopathy Screen","org":"FDA-Approved","mech":"Deep learning imaging","phase":"Approved","result":"High sensitivity/specificity","status":"Approved","badge":"badge-green"},
    {"domain":"Complications","cat":"Kidney","name":"Triple Renoprotective","org":"ADA Guidelines","mech":"SGLT2i+MRA+GLP-1RA","phase":"Clinical","result":"Triple therapy for DKD","status":"Guideline","badge":"badge-teal"},
    {"domain":"Complications","cat":"Retinopathy","name":"GLP-1RA Retinal Protection","org":"Clinical","mech":"Anti-inflammatory","phase":"Phase 3","result":"8-15% NPDR reduction","status":"Active","badge":"badge-teal"},
    {"domain":"Complications","cat":"Cardiovascular","name":"Cell Therapy for CV","org":"Multiple","mech":"Stem cell CV repair","phase":"Research","result":"Cell-based diabetic CV therapy","status":"Research","badge":"badge-teal"},
    {"domain":"Microbiome","cat":"Therapeutics","name":"Akkermansia Probiotic","org":"Multiple","mech":"Probiotic supplementation","phase":"Clinical","result":"Improved glycemic + lipid markers","status":"Active","badge":"badge-teal"},
    {"domain":"Microbiome","cat":"Diagnostics","name":"Microbiome-Guided Nutrition","org":"Clinical Trial","mech":"Personalized fiber Rx","phase":"RCT","result":"Gut profile predicts response","status":"Published","badge":"badge-teal"},
    {"domain":"Microbiome","cat":"Biology","name":"Gut-Liver Axis","org":"Harvard","mech":"Microbial metabolites","phase":"Research","result":"Gut molecules control liver energy","status":"Published","badge":"badge-teal"},
    {"domain":"Microbiome","cat":"Biology","name":"Large-Scale Microbiome Map","org":"34,500 people","mech":"Species-level profiling","phase":"Published","result":"Hundreds of species → health links","status":"Published","badge":"badge-teal"},
    {"domain":"Subtypes","cat":"Classification","name":"LADA Recognition","org":"ADA 2026","mech":"Autoantibody testing","phase":"Guideline","result":"4-14% of 'T2D' is actually LADA","status":"Guideline","badge":"badge-cyan"},
    {"domain":"Subtypes","cat":"Classification","name":"GDM → LADA Link","org":"Multiple","mech":"Post-GDM screening","phase":"Research","result":"GDM + GAD → high LADA risk","status":"Published","badge":"badge-cyan"},
    {"domain":"Subtypes","cat":"Classification","name":"Type 3c Recognition","org":"ADA 2026","mech":"Exocrine + endocrine","phase":"Guideline","result":"Commonly misdiagnosed as T2D","status":"Guideline","badge":"badge-cyan"},
    {"domain":"Epidemiology","cat":"Global","name":"589M Prevalence","org":"IDF/Lancet","mech":"Surveillance","phase":"Published","result":"46% increase projected by 2050","status":"Published","badge":"badge-red"},
    {"domain":"Epidemiology","cat":"Equity","name":"Tech Access Disparities","org":"Scoping Review","mech":"Equity analysis","phase":"Published","result":"Consistent CGM/pump/telehealth gaps","status":"Published","badge":"badge-red"},
    {"domain":"Epidemiology","cat":"Equity","name":"Youth T2D Disparities","org":"CDC/Multiple","mech":"Epidemiology","phase":"Published","result":"2-3x higher in Black/Hispanic youth","status":"Published","badge":"badge-red"},
    {"domain":"Epidemiology","cat":"Treatment Gap","name":"Global Treatment Coverage","org":"Lancet/NCD-RisC","mech":"Access analysis","phase":"Published","result":"LMICs: treatment lags prevalence","status":"Published","badge":"badge-red"},
]

# ═══════════════════════════════════════════════════════════════════════════
# DATA: All 35 research domains
# ═══════════════════════════════════════════════════════════════════════════

DOMAIN_DATA = [
    {"domain":"Biology","area":"Beta Cell Regeneration","desc":"Restoring or replacing insulin-producing cells","q":"Can we regenerate beta cells in vivo? Can stem cell islets scale?","status":"Very Active","priority":"High"},
    {"domain":"Biology","area":"Insulin Resistance","desc":"Molecular basis of peripheral insulin resistance","q":"What drives IR at the cellular level? Can it be fully reversed?","status":"Active","priority":"High"},
    {"domain":"Biology","area":"Autoimmune Pathogenesis","desc":"How the immune system destroys beta cells in T1D","q":"What triggers autoimmunity? Can we stop it before symptoms?","status":"Very Active","priority":"High"},
    {"domain":"Biology","area":"Islet Microenvironment","desc":"Pancreatic niche supporting beta cell function","q":"How does the islet milieu affect cell survival and function?","status":"Active","priority":"Medium"},
    {"domain":"Genetics","area":"GWAS / Polygenic Risk","desc":"Genetic variants associated with diabetes risk","q":"Can polygenic risk scores predict diabetes reliably across all populations?","status":"Very Active","priority":"High"},
    {"domain":"Genetics","area":"Epigenetics / Methylation","desc":"DNA methylation and histone modifications in diabetes","q":"Which epigenetic changes are causal vs. consequential?","status":"Active","priority":"High"},
    {"domain":"Genetics","area":"Monogenic (MODY)","desc":"Single-gene forms of diabetes","q":"How many patients are misdiagnosed? Can screening improve?","status":"Active","priority":"Medium"},
    {"domain":"Genetics","area":"Gene-Environment","desc":"How genes and environment combine to cause diabetes","q":"What environmental factors trigger disease in susceptible individuals?","status":"Active","priority":"High"},
    {"domain":"Immunology","area":"T Cell / B Cell Biology","desc":"Adaptive immune response in T1D","q":"How do T and B cells coordinate beta cell destruction?","status":"Very Active","priority":"High"},
    {"domain":"Immunology","area":"Treg / CAR-Treg Therapy","desc":"Engineering immune tolerance for transplant protection","q":"Can engineered Tregs provide lasting protection without drugs?","status":"Very Active","priority":"High"},
    {"domain":"Immunology","area":"Inflammation in T2D","desc":"Chronic low-grade inflammation driving insulin resistance","q":"What are the key inflammatory mediators? Can they be targeted?","status":"Active","priority":"Medium"},
    {"domain":"Technology","area":"Closed-Loop / AP","desc":"Automated insulin delivery systems","q":"Can fully closed-loop eliminate all manual management?","status":"Very Active","priority":"High"},
    {"domain":"Technology","area":"CGM Advances","desc":"Continuous glucose monitoring improvements","q":"How far can accuracy, wearability, and duration improve?","status":"Active","priority":"Medium"},
    {"domain":"Technology","area":"Digital Health","desc":"Mobile health, telemedicine, remote monitoring","q":"Can digital tools improve outcomes at population scale?","status":"Active","priority":"Medium"},
    {"domain":"Pharmacology","area":"GLP-1 / Multi-Agonists","desc":"Incretin-based therapies and combinations","q":"What is the ceiling for multi-agonist efficacy and safety?","status":"Very Active","priority":"High"},
    {"domain":"Pharmacology","area":"Novel Targets","desc":"Glucokinase, miRNA, metabolic-inflammation modulators","q":"What non-incretin mechanisms can we target for T2D?","status":"Active","priority":"High"},
    {"domain":"Pharmacology","area":"Drug Repurposing","desc":"Existing drugs with diabetes-relevant effects","q":"Which approved drugs have untapped diabetes or complication benefits?","status":"Active","priority":"Medium"},
    {"domain":"Microbiome","area":"Gut-Pancreas Axis","desc":"How gut bacteria influence diabetes pathogenesis","q":"Which species are protective vs. harmful? Is this causal?","status":"Very Active","priority":"High"},
    {"domain":"Microbiome","area":"Personalized Nutrition","desc":"Microbiome-guided dietary interventions","q":"Can microbiome profiling reliably predict individual diet response?","status":"Active","priority":"High"},
    {"domain":"Biomarkers","area":"Proteomic / Metabolomic","desc":"Circulating protein and metabolite signatures","q":"Which biomarkers can predict diabetes onset or progression?","status":"Very Active","priority":"High"},
    {"domain":"Biomarkers","area":"Complication Prediction","desc":"Early markers for retinopathy, nephropathy, neuropathy","q":"Can we predict complications years before clinical onset?","status":"Active","priority":"High"},
    {"domain":"Complications","area":"Diabetic Kidney Disease","desc":"Renal damage from chronic diabetes","q":"Can triple therapy (SGLT2i+MRA+GLP-1RA) truly halt CKD?","status":"Very Active","priority":"High"},
    {"domain":"Complications","area":"Retinopathy","desc":"Progressive eye damage from diabetes","q":"Can GLP-1RAs provide meaningful retinal protection?","status":"Active","priority":"High"},
    {"domain":"Complications","area":"Cardiovascular Disease","desc":"Heart and vascular damage from diabetes","q":"How do new therapies reduce cardiovascular mortality?","status":"Very Active","priority":"High"},
    {"domain":"Complications","area":"Neuropathy","desc":"Peripheral and autonomic nerve damage","q":"Can we detect and reverse neuropathy at earlier stages?","status":"Active","priority":"Medium"},
    {"domain":"Epidemiology","area":"Global Burden","desc":"Worldwide prevalence, trends, and projections","q":"Where is growth fastest? What structural factors drive it?","status":"Published","priority":"High"},
    {"domain":"Epidemiology","area":"Health Equity","desc":"Disparities in access, outcomes, and technology","q":"How do we close racial, economic, and geographic gaps?","status":"Active","priority":"High"},
    {"domain":"Epidemiology","area":"Youth Diabetes","desc":"Rising T2D in children and adolescents","q":"What is driving the youth T2D epidemic globally?","status":"Active","priority":"High"},
    {"domain":"Subtypes","area":"LADA / Type 3c","desc":"Misdiagnosed and under-recognized forms","q":"How many patients are incorrectly classified? What changes?","status":"Active","priority":"Medium"},
    {"domain":"Subtypes","area":"Gestational Diabetes","desc":"Pregnancy-related diabetes and long-term risk","q":"How does GDM predict future T2D or LADA development?","status":"Active","priority":"Medium"},
    {"domain":"AI/ML","area":"Risk Prediction","desc":"Machine learning for diabetes onset prediction","q":"Can AI outperform traditional risk calculators at scale?","status":"Very Active","priority":"High"},
    {"domain":"AI/ML","area":"Drug Discovery","desc":"Computational approaches to find new treatments","q":"Can AI meaningfully accelerate target identification?","status":"Active","priority":"High"},
    {"domain":"AI/ML","area":"Clinical Decision Support","desc":"AI tools for treatment optimization","q":"Can AI personalize therapy selection in real time?","status":"Active","priority":"Medium"},
    {"domain":"Prevention","area":"Lifestyle Programs","desc":"Diet, exercise, behavioral interventions","q":"How do we scale DPP enrollment beyond the current 3%?","status":"Active","priority":"High"},
    {"domain":"Prevention","area":"Population Screening","desc":"Identifying at-risk individuals before diagnosis","q":"Should we screen universally for T1D autoantibodies?","status":"Active","priority":"High"},
]

# ═══════════════════════════════════════════════════════════════════════════
# DATA: All 22 datasets
# ═══════════════════════════════════════════════════════════════════════════

DATASET_DATA = [
    {"type":"Proteomics","name":"UK Biobank Proteomics Portal","desc":"2,922 proteins vs T2D polygenic scores. Interactive AstraZeneca/CGR portal."},
    {"type":"Genomics","name":"T1D Knowledge Portal","desc":"Aggregated genetic and genomic data for T1D. Free summary statistics."},
    {"type":"Genomics","name":"T2D Knowledge Portal (AMP-T2D)","desc":"Genetic, epigenomic, clinical data for T2D. Consortium integration."},
    {"type":"Genomics","name":"DIAGRAM Consortium","desc":"Large-scale GWAS meta-analyses for T2D. Downloadable summary stats."},
    {"type":"Genomics","name":"GWAS Catalog (EBI)","desc":"Curated genome-wide association studies. Search by diabetes traits."},
    {"type":"Genomics","name":"DIAMANTE Results","desc":"Multi-ethnic T2D GWAS meta-analysis. 1,120 CpGs identified."},
    {"type":"Multi-Omics","name":"UK Biobank","desc":"500K participants with genomic + phenotype data. Application required."},
    {"type":"Multi-Omics","name":"dbGaP (NIDDK)","desc":"NIDDK-funded diabetes genomic datasets. Controlled access."},
    {"type":"Clinical","name":"ClinicalTrials.gov","desc":"Global registry of all diabetes clinical trials. Filter by phase/status."},
    {"type":"Clinical","name":"TrialNet","desc":"T1D prevention trial network and autoantibody screening data."},
    {"type":"Clinical","name":"TEDDY Study","desc":"Environmental triggers of T1D in genetically at-risk birth cohort."},
    {"type":"Proteomics","name":"Human Protein Atlas","desc":"Protein expression across tissues including pancreatic islets."},
    {"type":"Genomics","name":"GEO (Gene Expression Omnibus)","desc":"Public gene expression datasets. Search: diabetes, islet, beta cell."},
    {"type":"Metabolomics","name":"Metabolomics Workbench","desc":"Repository for metabolomics data including diabetes-specific studies."},
    {"type":"Other","name":"ENCODE Project","desc":"Encyclopedia of DNA elements. Islet-specific regulatory element data."},
    {"type":"Other","name":"PubMed / PMC","desc":"Biomedical literature database. Use MeSH terms for precision."},
    {"type":"Other","name":"Microbiome Project","desc":"Human Microbiome Project reference datasets. Healthy + disease states."},
    {"type":"Other","name":"OpenTargets Platform","desc":"Evidence-based target identification for T1D and T2D."},
    {"type":"Other","name":"STRING Database","desc":"Protein-protein interaction networks for pathway analysis."},
    {"type":"Other","name":"Reactome","desc":"Biological pathway database. Insulin signaling pathways."},
    {"type":"Other","name":"AlphaFold DB","desc":"Predicted 3D protein structures for drug target analysis."},
    {"type":"Other","name":"DrugBank","desc":"Drug and target information database. Repurposing opportunities."},
]

# ═══════════════════════════════════════════════════════════════════════════
# DATA: All 25 papers
# ═══════════════════════════════════════════════════════════════════════════

PAPERS_DATA = [
    {"title":"Stem Cell-Derived Islets for T1D (Zimislecel)","journal":"NEJM","year":2025,"domain":"T1D","topic":"Stem Cell","finding":"Phase 3 results for zimislecel","rel":5},
    {"title":"The future of type 1 diabetes therapy","journal":"The Lancet","year":2025,"domain":"T1D","topic":"Overview","finding":"Comprehensive T1D therapeutic landscape review","rel":5},
    {"title":"Plasma proteomic markers & T2D polygenic risk","journal":"Nature Comms","year":2025,"domain":"T2D","topic":"Proteomics","finding":"617 proteins linked to T2D; FAM3D target","rel":5},
    {"title":"Role of beta cell in T2D: last 5 years","journal":"Diabetologia","year":2025,"domain":"T2D","topic":"Beta Cell","finding":"T2D remission via beta cell recovery","rel":5},
    {"title":"Global diabetes burden 1990-2021 + projections","journal":"The Lancet","year":2023,"domain":"Epi","topic":"Epidemiology","finding":"589M prevalence; 46% increase by 2050","rel":5},
    {"title":"Worldwide diabetes treatment 1990-2022","journal":"The Lancet","year":2024,"domain":"Epi","topic":"Treatment Gaps","finding":"Treatment not keeping pace in LMICs","rel":5},
    {"title":"Pharmacological therapies for T2D: future","journal":"Diabetologia","year":2025,"domain":"T2D","topic":"Drug Pipeline","finding":"Multi-agonists, inflammation modulators, ML discovery","rel":5},
    {"title":"ADA Standards of Care 2026","journal":"Diabetes Care","year":2026,"domain":"All","topic":"Guidelines","finding":"Comprehensive clinical practice guidelines","rel":5},
    {"title":"Multi-omics biomarker discovery in prediabetes","journal":"Front Endocrinol","year":2025,"domain":"T2D","topic":"Biomarkers","finding":"AI+ML multi-omics biomarker framework","rel":4},
    {"title":"Epigenetic landscape of T2D: CpG analysis","journal":"Diabetes Metab J","year":2025,"domain":"T2D","topic":"Epigenetics","finding":"1,120 CpGs; CAMK1D mechanisms","rel":4},
    {"title":"Regulatory T cell dysfunction in T1D","journal":"Front Endocrinol","year":2025,"domain":"T1D","topic":"Immunology","finding":"Treg dysfunction and therapeutic breakthroughs","rel":4},
    {"title":"CAR T cell therapy in type 1 diabetes","journal":"PMC","year":2025,"domain":"T1D","topic":"Immunotherapy","finding":"CAR-T approaches for T1D: current state","rel":4},
    {"title":"Gut microbiome predicts fiber response","journal":"Nature Comms","year":2025,"domain":"T2D","topic":"Microbiome","finding":"Microbiome predicts dietary intervention success","rel":4},
    {"title":"Diet, gut microbiome, and T1D","journal":"Gut Microbes","year":2026,"domain":"T1D","topic":"Microbiome","finding":"Diet shapes immunomodulatory metabolites","rel":4},
    {"title":"ML for diabetes complication diagnosis","journal":"J Diabetes Sci Tech","year":2025,"domain":"Cross","topic":"AI/Complications","finding":"ML reshaping DR, DN, neuropathy diagnosis","rel":4},
    {"title":"Advances in beta-cell regeneration","journal":"Front Endocrinol","year":2026,"domain":"T1D/T2D","topic":"Regeneration","finding":"In vitro + in vivo regeneration advances","rel":4},
    {"title":"Innovation without inclusion: tech equity","journal":"J Diabetes Metab","year":2026,"domain":"Equity","topic":"Disparities","finding":"Consistent CGM/pump/telehealth access gaps","rel":4},
    {"title":"Emerging immunotherapies for T1D","journal":"PMC","year":2025,"domain":"T1D","topic":"Immunotherapy","finding":"Review of immunotherapeutic approaches","rel":4},
    {"title":"Multilevel diabetes prevention for equity","journal":"JMIR Public Health","year":2025,"domain":"Prevention","topic":"Public Health","finding":"Multi-level interventions for disparities","rel":4},
    {"title":"Next-gen therapeutics: lessons learned","journal":"Innovation Drug Disc","year":2026,"domain":"T2D","topic":"Drug Design","finding":"Lessons for next-gen diabetes drugs","rel":4},
    {"title":"Safe deep RL closed-loop AP controller","journal":"PLOS ONE","year":2025,"domain":"T1D","topic":"AI/Tech","finding":"87.45% TIR; outperforms baselines","rel":3},
    {"title":"3D organoids for beta cell replacement","journal":"Int J Mol Sci","year":2025,"domain":"T1D/T2D","topic":"Organoids","finding":"Vascularization advances in organoid models","rel":3},
    {"title":"AI in diabetes prediction: 33-year review","journal":"Front Digital Health","year":2025,"domain":"AI/ML","topic":"Literature","finding":"Comprehensive AI/ML mapping in diabetes","rel":3},
    {"title":"Stem cell therapies: encapsulation advances","journal":"Cells","year":2025,"domain":"T1D","topic":"Encapsulation","finding":"Immunological hurdles in encapsulated islets","rel":3},
    {"title":"Reversing beta-cell dedifferentiation in T2D","journal":"Exp Mol Med","year":2023,"domain":"T2D","topic":"Beta Cell","finding":"Dedifferentiation mechanisms and reversal","rel":4},
]

# ═══════════════════════════════════════════════════════════════════════════
# TIMELINE DATA
# ═══════════════════════════════════════════════════════════════════════════

TIMELINE_2025 = [
    {"date":"2025","title":"Vertex Zimislecel Phase 3 enrolls 50 participants","desc":"First scalable stem cell therapy for T1D reaches pivotal trial. 10/12 full-dose patients insulin-independent at 1 year.","type":"milestone"},
    {"date":"Nov 2025","title":"Stanford preclinical: reversal of T1D in mice without immunosuppression","desc":"Preclinical (murine): hybrid immune system co-transplant reported reversal of hyperglycemia in 19/19 protected and 9/9 established-T1D mice. No human data yet; do not extrapolate.","type":"milestone"},
    {"date":"2025","title":"Sana engineered islets survive 6 months in humans","desc":"Gene-edited islet cells function without immunosuppression - the holy grail of islet therapy.","type":"milestone"},
    {"date":"2025","title":"Retatrutide: 28.7% weight loss in TRIUMPH-4","desc":"Eli Lilly's triple agonist (GLP-1/GIP/Glucagon) sets new efficacy benchmark for T2D.","type":"milestone"},
    {"date":"2025","title":"Chinese team achieves insulin independence with iPSC","desc":"Patient's own reprogrammed cells produce insulin - first autologous islet success.","type":"milestone"},
    {"date":"2025","title":"UK Biobank proteomics: 617 T2D-linked proteins identified","desc":"Largest proteomic study maps protein-disease network; FAM3D emerges as novel target.","type":"milestone"},
    {"date":"2025","title":"DIAMANTE epigenome: 1,120 CpGs associated with T2D","desc":"Multi-ethnic epigenetic analysis reveals CAMK1D, TP53INP1, ATP5G1 regulatory mechanisms.","type":"milestone"},
    {"date":"2025","title":"Abata ABA-201 TCR-Treg therapy enters trials","desc":"First T1D-specific TCR-engineered regulatory T cell therapy begins clinical testing.","type":"milestone"},
    {"date":"2025","title":"Inreda bihormonal AP: 80% time-in-range achieved","desc":"Fully closed-loop artificial pancreas with insulin + glucagon - no user input needed.","type":"milestone"},
    {"date":"2025","title":"Microbiome-guided nutrition predicts fiber response","desc":"RCT shows gut microbiome profiling predicts personalized dietary intervention success in prediabetes.","type":"milestone"},
    {"date":"2025","title":"44% T2D remission with SGLT2i + calorie restriction","desc":"Randomized study achieves near-half remission rate with combination approach.","type":"milestone"},
    {"date":"2025","title":"Tzield expanded: PETITE trial in children under 8","desc":"First immunotherapy to delay T1D now tested in youngest population yet.","type":"general"},
    {"date":"2025","title":"Harvard gut discovery: microbial molecules regulate liver","desc":"Gut bacterial metabolites travel to liver and control energy usage - diet-dependent pathway.","type":"general"},
    {"date":"2025","title":"Deep RL closed-loop controller: 87.45% TIR","desc":"AI-driven fully automated insulin dosing outperforms conventional algorithms in simulation.","type":"general"},
    {"date":"2025","title":"GLP-1RAs shown to reduce retinopathy progression 8-15%","desc":"Anti-inflammatory effects of GLP-1 drugs extend to retinal protection.","type":"general"},
]

TIMELINE_2026 = [
    {"date":"Q1 2026","title":"MUSC launches immune bodyguard program","desc":"$1M grant to pair stem cell islets with CAR-Treg bodyguards - no immunosuppression.","type":"upcoming"},
    {"date":"Q1 2026","title":"ADA Standards of Care 2026 published","desc":"Updated clinical guidelines with emphasis on earlier screening and individualized care.","type":"upcoming"},
    {"date":"Q2 2026","title":"Vertex Zimislecel regulatory submission","desc":"If approved, first stem cell-derived cure for Type 1 diabetes.","type":"upcoming"},
    {"date":"Q2 2026","title":"Orforglipron FDA decision","desc":"First convenient oral GLP-1 pill - could transform T2D treatment accessibility.","type":"upcoming"},
    {"date":"Q2 2026","title":"Baricitinib BARICADE trials open enrollment","desc":"Phase 3 testing oral JAK inhibitor for T1D prevention and beta cell preservation.","type":"upcoming"},
    {"date":"Q3 2026","title":"CagriSema FDA review","desc":"Next-gen dual-hormone injectable: semaglutide + cagrilintide.","type":"upcoming"},
    {"date":"Q3 2026","title":"Sana Biotechnology Phase 1 trial starts","desc":"Immune-evasive engineered islets without immunosuppression - human trials.","type":"upcoming"},
    {"date":"Q4 2026","title":"Insulin Icodec FDA approval target","desc":"Once-weekly basal insulin transforms T2D from daily to weekly injection.","type":"upcoming"},
    {"date":"2026","title":"Semaglutide patents expire","desc":"Opens door to biosimilars - major global accessibility implications.","type":"upcoming"},
    {"date":"2026","title":"Dorzagliatin glucokinase activator US trials","desc":"First-in-class glucose sensor repair drug enters US clinical testing.","type":"upcoming"},
]

def generate_html():
    """Generate the complete HTML file."""

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diabetes Research Hub — Comprehensive Dashboard</title>
<style>
/* === TUFTE-INFORMED DESIGN SYSTEM === */
:root {
  --bg: #fafaf7;
  --surface: #ffffff;
  --text: #1a1a1a;
  --muted: #636363;
  --light: #999999;
  --border: #e0ddd5;
  --border-light: #eeebe3;
  --accent: #2c5f8a;
  --accent-light: #d4e2ef;
  --green: #2d7d46;
  --green-light: #d4edda;
  --amber: #8b6914;
  --amber-light: #fef3cd;
  --red: #8b2500;
  --red-light: #f5d5cc;
  --purple: #5b4a8a;
  --purple-light: #e2daf0;
  --teal: #1a7a6d;
  --teal-light: #cce8e4;
  --cyan: #1a6b7d;
  --cyan-light: #cce0e8;
  --pink: #8b4969;
  --pink-light: #ead1d8;
  --indigo: #4a4a7a;
  --indigo-light: #dcdce8;
  --orange: #b8741a;
  --orange-light: #f0dcc3;
  --serif: Georgia, 'Times New Roman', serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --mono: 'SF Mono', 'Consolas', 'Monaco', monospace;
}

/* === CONTEXT BLOCK === */
.context-block { background-color: #ffffff; border-left: 4px solid #2c5f8a; padding: 1.5rem 2rem; margin: 0 0 2rem 0; line-height: 1.8; }
.context-block h3 { font-family: Georgia, serif; font-size: 1.1rem; color: #2c5f8a; margin: 0 0 0.75rem 0; font-weight: normal; }
.context-block p { margin: 0.5rem 0; font-size: 0.95rem; color: #333; }
.context-block .context-label { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #666; margin-top: 1rem; margin-bottom: 0.25rem; }

* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: var(--sans); background: var(--bg); color: var(--text); line-height: 1.55; font-size: 14px; }

/* Header */
.header { padding: 40px 48px; border-bottom: 1px solid var(--border); max-width: 1400px; margin: 0 auto; }
.header h1 { font-family: var(--serif); font-size: 32px; font-weight: 400; color: var(--text); letter-spacing: -0.3px; }
.header .desc { font-size: 14px; color: var(--muted); margin-top: 8px; }
.header .tagline { display: flex; gap: 24px; margin-top: 20px; flex-wrap: wrap; }
.header .tag { font-size: 12px; color: var(--muted); font-family: var(--mono); }
.header .tag .num { font-weight: 700; color: var(--text); }

/* Tabs */
.tabs { max-width: 1400px; margin: 0 auto; padding: 0 48px; border-bottom: 1px solid var(--border); display: flex; gap: 2px; overflow-x: auto; }
.tab { padding: 14px 18px; cursor: pointer; border: none; background: transparent; color: var(--muted); font-size: 13px; font-weight: 500; border-bottom: 2px solid transparent; transition: all 0.2s; white-space: nowrap; }
.tab:hover { color: var(--text); border-bottom-color: var(--border); }
.tab.active { color: var(--accent); border-bottom-color: var(--accent); }

/* Main content */
.content { max-width: 1400px; margin: 0 auto; padding: 32px 48px; }
.tab-content { display: none; }
.tab-content.active { display: block; }

/* Overview stats grid */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 28px; margin-bottom: 40px; }
.stat { }
.stat .num { font-family: var(--mono); font-size: 28px; font-weight: 700; color: var(--text); line-height: 1; }
.stat .label { font-size: 11px; color: var(--muted); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
.stat .sub { font-size: 12px; color: var(--muted); margin-top: 4px; }

/* Data bar charts (horizontal bars instead of pie/doughnut) */
.bar-chart { margin-bottom: 32px; }
.bar-chart h3 { font-family: var(--serif); font-size: 16px; font-weight: 400; margin-bottom: 16px; color: var(--text); }
.bar-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.bar-label { font-size: 12px; color: var(--muted); min-width: 120px; text-align: right; }
.bar-container { flex: 1; background: var(--border-light); height: 24px; border-radius: 0; overflow: hidden; }
.bar { background: var(--accent); height: 100%; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; color: white; font-size: 11px; font-weight: 600; }

/* Search and filter */
.search-bar { width: 100%; max-width: 400px; padding: 8px 12px; border: 1px solid var(--border); background: var(--surface); color: var(--text); font-size: 13px; margin-bottom: 16px; }
.search-bar:focus { outline: none; border-color: var(--accent); }

.filter-row { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
.filter-btn { padding: 6px 14px; border: 1px solid var(--border); background: var(--surface); color: var(--muted); font-size: 12px; cursor: pointer; border-radius: 0; transition: all 0.2s; }
.filter-btn:hover { color: var(--text); border-color: var(--accent); }
.filter-btn.active { background: var(--accent); color: white; border-color: var(--accent); }

/* Table */
.table-container { overflow-x: auto; border: 1px solid var(--border); margin-bottom: 32px; max-height: 600px; overflow-y: auto; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th { text-align: left; padding: 12px; background: var(--bg); color: var(--muted); font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid var(--border); position: sticky; top: 0; }
td { padding: 10px 12px; border-bottom: 1px solid var(--border-light); }
tr:hover { background: var(--accent-light); }

/* Badges */
.badge { display: inline-block; padding: 3px 8px; font-size: 10px; font-weight: 600; border-radius: 0; }
.badge-green { background: var(--green-light); color: var(--green); }
.badge-blue { background: var(--accent-light); color: var(--accent); }
.badge-purple { background: var(--purple-light); color: var(--purple); }
.badge-orange { background: var(--orange-light); color: var(--orange); }
.badge-pink { background: var(--pink-light); color: var(--pink); }
.badge-cyan { background: var(--cyan-light); color: var(--cyan); }
.badge-teal { background: var(--teal-light); color: var(--teal); }
.badge-indigo { background: var(--indigo-light); color: var(--indigo); }
.badge-red { background: var(--red-light); color: var(--red); }

/* Domain grid */
.domain-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 20px; margin-bottom: 32px; }
.domain-card { border: 1px solid var(--border); padding: 18px; border-left: 3px solid var(--accent); }
.domain-card.high { border-left-color: var(--red); }
.domain-card.medium { border-left-color: var(--orange); }
.domain-card.low { border-left-color: var(--light); }
.domain-card .tag { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.domain-card h3 { font-family: var(--serif); font-size: 15px; font-weight: 400; margin-bottom: 6px; color: var(--text); }
.domain-card .field { font-size: 12px; color: var(--muted); margin-bottom: 8px; }
.domain-card .question { font-size: 12px; color: var(--muted); font-style: italic; margin-top: 8px; line-height: 1.4; }
.domain-card .status-row { font-size: 11px; margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap; }

/* Timeline */
.timeline { position: relative; padding-left: 28px; }
.timeline::before { content: ''; position: absolute; left: 9px; top: 0; bottom: 0; width: 1px; background: var(--border); }
.tl-item { position: relative; margin-bottom: 24px; }
.tl-item::before { content: ''; position: absolute; left: -22px; top: 2px; width: 10px; height: 10px; border-radius: 50%; border: 1px solid var(--accent); background: var(--surface); }
.tl-item.milestone::before { background: var(--green); border-color: var(--green); }
.tl-item.upcoming::before { background: var(--amber); border-color: var(--amber); }
.tl-item .date { font-size: 10px; font-weight: 600; color: var(--accent); margin-bottom: 3px; text-transform: uppercase; letter-spacing: 0.5px; }
.tl-item h4 { font-family: var(--serif); font-size: 14px; font-weight: 400; color: var(--text); margin-bottom: 4px; }
.tl-item p { font-size: 12px; color: var(--muted); line-height: 1.5; }
.tl-section { font-family: var(--serif); font-size: 16px; font-weight: 400; margin-top: 28px; margin-bottom: 18px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }

/* Dataset/Paper grid */
.resource-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; margin-bottom: 32px; }
.resource-card { border: 1px solid var(--border); padding: 16px; }
.resource-card .type { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.resource-card h4 { font-family: var(--serif); font-size: 14px; font-weight: 400; color: var(--text); margin-bottom: 6px; }
.resource-card p { font-size: 12px; color: var(--muted); line-height: 1.5; }

/* Responsive */
@media (max-width: 1000px) {
  .header, .tabs, .content { padding-left: 24px; padding-right: 24px; }
  .domain-grid { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: 1fr 1fr; }
  .search-bar { max-width: 100%; }
}
@media (max-width: 600px) {
  .header { padding: 24px 16px; }
  .header h1 { font-size: 24px; }
  .tabs { padding: 0 16px; }
  .content { padding: 20px 16px; }
  .stats-grid { grid-template-columns: 1fr; }
  .filter-row { flex-direction: column; }
  .filter-btn { width: 100%; }
}
</style>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-JGMD5VRYPH');</script>
</head>
<body>

<div class="header">
  <h1>Diabetes Research Hub</h1>
  <p class="desc">Comprehensive AI-powered research tracker. All domains of diabetes research (2025–2026).</p>
  <div class="tagline">
    <span class="tag"><span class="num">55</span> Pipeline Entries</span>
    <span class="tag"><span class="num">35</span> Research Domains</span>
    <span class="tag"><span class="num">22</span> Datasets</span>
    <span class="tag"><span class="num">25</span> Papers</span>
  </div>
</div>

<div class="context-block">
  <h3>What This Dashboard Answers</h3>
  <p>The central research hub providing an overview of the entire diabetes research landscape tracked by this platform: 55 pipeline entries, 35 research domains, 22 public datasets, and 25 high-impact papers. This is the navigational starting point for the platform.</p>
  <div class="context-label">How to Use This</div>
  <p>For new visitors: provides orientation to the platform's scope and structure. For returning users: serves as a jump-off point to specific dashboards and analyses. For collaborators: summarizes what data and analyses are available.</p>
  <div class="context-label">What This Cannot Tell You</div>
  <p>This is an index and navigation tool, not an analysis. Statistics shown are counts from the tracker spreadsheet and may not reflect the most recent dashboard-level analyses.</p>
</div>

<div class="tabs">
  <button class="tab active" onclick="showTab('overview')">Overview</button>
  <button class="tab" onclick="showTab('pipeline')">Full Pipeline</button>
  <button class="tab" onclick="showTab('domains')">Research Domains</button>
  <button class="tab" onclick="showTab('timeline')">Timeline</button>
  <button class="tab" onclick="showTab('datasets')">Datasets</button>
  <button class="tab" onclick="showTab('papers')">Papers</button>
</div>

<div class="content">

  <!-- OVERVIEW -->
  <div id="overview" class="tab-content active">
    <div class="stats-grid">
      <div class="stat">
        <div class="num">55</div>
        <div class="label">Pipeline Entries</div>
        <div class="sub">All domains tracked</div>
      </div>
      <div class="stat">
        <div class="num">7</div>
        <div class="label">Phase 3 Trials</div>
        <div class="sub">Closest to approval</div>
      </div>
      <div class="stat">
        <div class="num">35</div>
        <div class="label">Research Domains</div>
        <div class="sub">Mapped with key questions</div>
      </div>
      <div class="stat">
        <div class="num">25</div>
        <div class="label">Papers Tracked</div>
        <div class="sub">High-impact journals</div>
      </div>
      <div class="stat">
        <div class="num">22</div>
        <div class="label">Datasets</div>
        <div class="sub">Genomics to clinical</div>
      </div>
      <div class="stat">
        <div class="num">589M</div>
        <div class="label">Global Prevalence</div>
        <div class="sub">Adults with diabetes</div>
      </div>
    </div>

    <div class="bar-chart">
      <h3>Pipeline by Research Domain</h3>
      <div id="domainBars"></div>
    </div>

    <div class="bar-chart">
      <h3>Clinical Phase Distribution</h3>
      <div id="phaseBars"></div>
    </div>

    <div class="bar-chart">
      <h3>Disease Focus Distribution</h3>
      <div id="diseaseBars"></div>
    </div>
  </div>

  <!-- PIPELINE -->
  <div id="pipeline" class="tab-content">
    <input type="text" class="search-bar" placeholder="Search therapies, organizations, mechanisms..." oninput="filterPipelineTable()">
    <div class="filter-row">
      <button class="filter-btn active" onclick="setPipelineFilter('all')">All (55)</button>
      <button class="filter-btn" onclick="setPipelineFilter('T1D')">T1D</button>
      <button class="filter-btn" onclick="setPipelineFilter('T2D')">T2D</button>
      <button class="filter-btn" onclick="setPipelineFilter('Biomarkers')">Biomarkers</button>
      <button class="filter-btn" onclick="setPipelineFilter('AI/ML')">AI/ML</button>
      <button class="filter-btn" onclick="setPipelineFilter('Complications')">Complications</button>
      <button class="filter-btn" onclick="setPipelineFilter('Microbiome')">Microbiome</button>
    </div>
    <div class="table-container">
      <table id="pipelineTable">
        <thead>
          <tr>
            <th>Domain</th>
            <th>Category</th>
            <th>Therapy</th>
            <th>Organization</th>
            <th>Mechanism</th>
            <th>Phase</th>
            <th>Key Result</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
  </div>

  <!-- RESEARCH DOMAINS -->
  <div id="domains" class="tab-content">
    <p style="font-size: 13px; color: var(--muted); margin-bottom: 20px;">35 research domains mapped with key open questions — sorted by priority</p>
    <div class="filter-row">
      <button class="filter-btn active" onclick="setDomainFilter('all')">All</button>
      <button class="filter-btn" onclick="setDomainFilter('Biology')">Biology</button>
      <button class="filter-btn" onclick="setDomainFilter('Genetics')">Genetics</button>
      <button class="filter-btn" onclick="setDomainFilter('Immunology')">Immunology</button>
      <button class="filter-btn" onclick="setDomainFilter('Technology')">Technology</button>
      <button class="filter-btn" onclick="setDomainFilter('Pharmacology')">Pharmacology</button>
      <button class="filter-btn" onclick="setDomainFilter('Microbiome')">Microbiome</button>
      <button class="filter-btn" onclick="setDomainFilter('Biomarkers')">Biomarkers</button>
      <button class="filter-btn" onclick="setDomainFilter('Complications')">Complications</button>
      <button class="filter-btn" onclick="setDomainFilter('AI/ML')">AI/ML</button>
    </div>
    <div class="domain-grid" id="domainGrid"></div>
  </div>

  <!-- TIMELINE -->
  <div id="timeline" class="tab-content">
    <p style="font-size: 13px; color: var(--muted); margin-bottom: 20px;">Research milestones achieved and upcoming events</p>

    <div class="tl-section" style="color: var(--green);">2025 — Breakthroughs Achieved</div>
    <div class="timeline" id="timeline2025"></div>

    <div class="tl-section" style="color: var(--orange);">2026 — Expected Milestones</div>
    <div class="timeline" id="timeline2026"></div>
  </div>

  <!-- DATASETS -->
  <div id="datasets" class="tab-content">
    <p style="font-size: 13px; color: var(--muted); margin-bottom: 20px;">22 key datasets, databases, and research tools for diabetes research</p>
    <div class="filter-row">
      <button class="filter-btn active" onclick="setDatasetFilter('all')">All</button>
      <button class="filter-btn" onclick="setDatasetFilter('Genomics')">Genomics</button>
      <button class="filter-btn" onclick="setDatasetFilter('Proteomics')">Proteomics</button>
      <button class="filter-btn" onclick="setDatasetFilter('Multi-Omics')">Multi-Omics</button>
      <button class="filter-btn" onclick="setDatasetFilter('Clinical')">Clinical</button>
      <button class="filter-btn" onclick="setDatasetFilter('Metabolomics')">Metabolomics</button>
      <button class="filter-btn" onclick="setDatasetFilter('Other')">Other</button>
    </div>
    <div class="resource-grid" id="datasetGrid"></div>
  </div>

  <!-- PAPERS -->
  <div id="papers" class="tab-content">
    <p style="font-size: 13px; color: var(--muted); margin-bottom: 20px;">25 high-impact papers across all research domains</p>
    <input type="text" class="search-bar" placeholder="Search papers by title, topic, journal..." oninput="filterPapersTable()">
    <div class="table-container">
      <table id="papersTable">
        <thead>
          <tr>
            <th>Title</th>
            <th>Journal</th>
            <th>Year</th>
            <th>Domain</th>
            <th>Topic</th>
            <th>Key Finding</th>
            <th>Relevance</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
  </div>

</div>

<script>
// Data (inline)
"""

    # Add inline data
    html += "const PIPELINE_DATA = " + json.dumps(PIPELINE_DATA) + ";\n"
    html += "const DOMAIN_DATA = " + json.dumps(DOMAIN_DATA) + ";\n"
    html += "const DATASET_DATA = " + json.dumps(DATASET_DATA) + ";\n"
    html += "const PAPERS_DATA = " + json.dumps(PAPERS_DATA) + ";\n"
    html += "const TIMELINE_2025 = " + json.dumps(TIMELINE_2025) + ";\n"
    html += "const TIMELINE_2026 = " + json.dumps(TIMELINE_2026) + ";\n"

    html += """

// Global state
let pipelineFilter = 'all';
let pipelineSearch = '';
let domainFilter = 'all';
let datasetFilter = 'all';
let papersSearch = '';

// Tab switching
function showTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}

// Overview: render bar charts
function renderOverview() {
  // Domain distribution
  const domainCounts = {};
  PIPELINE_DATA.forEach(d => {
    domainCounts[d.domain] = (domainCounts[d.domain] || 0) + 1;
  });

  let domainBarsHtml = '';
  Object.entries(domainCounts).sort((a, b) => b[1] - a[1]).forEach(([domain, count]) => {
    const pct = (count / PIPELINE_DATA.length * 100).toFixed(0);
    domainBarsHtml += `
      <div class="bar-row">
        <div class="bar-label">${domain}</div>
        <div class="bar-container">
          <div class="bar" style="width: ${pct}%">${count}</div>
        </div>
      </div>
    `;
  });
  document.getElementById('domainBars').innerHTML = domainBarsHtml;

  // Phase distribution
  const phaseCounts = {};
  PIPELINE_DATA.forEach(d => {
    phaseCounts[d.phase] = (phaseCounts[d.phase] || 0) + 1;
  });
  const phaseOrder = ['Preclinical','Phase 1','Phase 1/2','Phase 1b','Phase 2','Phase 2-3','Phase 3','Approved','Guideline','Published','RCT','Clinical','Research','Case Study','Enrolling'];

  let phaseBarsHtml = '';
  Object.entries(phaseCounts).sort((a, b) => phaseOrder.indexOf(a[0]) - phaseOrder.indexOf(b[0])).forEach(([phase, count]) => {
    const pct = (count / Math.max(...Object.values(phaseCounts)) * 100).toFixed(0);
    phaseBarsHtml += `
      <div class="bar-row">
        <div class="bar-label">${phase}</div>
        <div class="bar-container">
          <div class="bar" style="width: ${pct}%">${count}</div>
        </div>
      </div>
    `;
  });
  document.getElementById('phaseBars').innerHTML = phaseBarsHtml;

  // Disease distribution
  const t1d = PIPELINE_DATA.filter(d => d.domain === 'T1D').length;
  const t2d = PIPELINE_DATA.filter(d => d.domain === 'T2D').length;
  const other = PIPELINE_DATA.length - t1d - t2d;

  let diseaseBarsHtml = `
    <div class="bar-row">
      <div class="bar-label">Type 1</div>
      <div class="bar-container">
        <div class="bar" style="width: ${(t1d/PIPELINE_DATA.length*100).toFixed(0)}%">${t1d}</div>
      </div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Type 2</div>
      <div class="bar-container">
        <div class="bar" style="width: ${(t2d/PIPELINE_DATA.length*100).toFixed(0)}%">${t2d}</div>
      </div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Cross-Cutting</div>
      <div class="bar-container">
        <div class="bar" style="width: ${(other/PIPELINE_DATA.length*100).toFixed(0)}%">${other}</div>
      </div>
    </div>
  `;
  document.getElementById('diseaseBars').innerHTML = diseaseBarsHtml;
}

// Pipeline table
function setPipelineFilter(f) {
  pipelineFilter = f;
  document.querySelectorAll('#pipeline .filter-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  filterPipelineTable();
}

function filterPipelineTable() {
  const search = document.querySelector('#pipeline .search-bar').value.toLowerCase();
  pipelineSearch = search;

  let filtered = PIPELINE_DATA;
  if (pipelineFilter !== 'all') filtered = filtered.filter(d => d.domain === pipelineFilter);
  if (search) filtered = filtered.filter(d => (d.name + d.org + d.mech + d.cat + d.result).toLowerCase().includes(search));

  const tbody = document.querySelector('#pipelineTable tbody');
  tbody.innerHTML = '';
  filtered.forEach(d => {
    tbody.innerHTML += `
      <tr>
        <td><span class="badge badge-${d.badge === 'badge-green' ? 'green' : d.badge === 'badge-blue' ? 'blue' : d.badge === 'badge-cyan' ? 'cyan' : d.badge === 'badge-orange' ? 'orange' : d.badge === 'badge-purple' ? 'purple' : 'red'}">${d.domain}</span></td>
        <td>${d.cat}</td>
        <td><strong>${d.name}</strong></td>
        <td>${d.org}</td>
        <td>${d.mech}</td>
        <td>${d.phase}</td>
        <td>${d.result}</td>
        <td><span class="badge badge-${d.badge === 'badge-green' ? 'green' : d.badge === 'badge-blue' ? 'blue' : d.badge === 'badge-cyan' ? 'cyan' : d.badge === 'badge-orange' ? 'orange' : 'red'}">${d.status}</span></td>
      </tr>
    `;
  });
}

// Domain cards
function setDomainFilter(f) {
  domainFilter = f;
  document.querySelectorAll('#domains .filter-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  renderDomains();
}

function renderDomains() {
  let filtered = DOMAIN_DATA;
  if (domainFilter !== 'all') filtered = filtered.filter(d => d.domain === domainFilter);

  const grid = document.getElementById('domainGrid');
  grid.innerHTML = '';
  filtered.forEach(d => {
    const priorityClass = d.priority === 'High' ? 'high' : 'medium';
    grid.innerHTML += `
      <div class="domain-card ${priorityClass}">
        <div class="tag">${d.domain}</div>
        <h3>${d.area}</h3>
        <div class="field">${d.desc}</div>
        <div class="question">"${d.q}"</div>
        <div class="status-row">
          <span class="badge badge-${d.status === 'Very Active' ? 'green' : d.status === 'Active' ? 'blue' : 'cyan'}">${d.status}</span>
          <span class="badge badge-${d.priority === 'High' ? 'red' : 'orange'}">${d.priority} Priority</span>
        </div>
      </div>
    `;
  });
}

// Timeline
function renderTimeline() {
  let html2025 = '';
  TIMELINE_2025.forEach(item => {
    const type = item.type === 'milestone' ? 'milestone' : 'general';
    html2025 += `
      <div class="tl-item ${type}">
        <div class="date">${item.date}</div>
        <h4>${item.title}</h4>
        <p>${item.desc}</p>
      </div>
    `;
  });
  document.getElementById('timeline2025').innerHTML = html2025;

  let html2026 = '';
  TIMELINE_2026.forEach(item => {
    html2026 += `
      <div class="tl-item upcoming">
        <div class="date">${item.date}</div>
        <h4>${item.title}</h4>
        <p>${item.desc}</p>
      </div>
    `;
  });
  document.getElementById('timeline2026').innerHTML = html2026;
}

// Datasets
function setDatasetFilter(f) {
  datasetFilter = f;
  document.querySelectorAll('#datasets .filter-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  renderDatasets();
}

function renderDatasets() {
  let filtered = DATASET_DATA;
  if (datasetFilter !== 'all') filtered = filtered.filter(d => d.type === datasetFilter);

  const grid = document.getElementById('datasetGrid');
  grid.innerHTML = '';
  filtered.forEach(d => {
    grid.innerHTML += `
      <div class="resource-card">
        <div class="type">${d.type}</div>
        <h4>${d.name}</h4>
        <p>${d.desc}</p>
      </div>
    `;
  });
}

// Papers
function filterPapersTable() {
  const search = document.querySelector('#papers .search-bar').value.toLowerCase();
  papersSearch = search;

  let filtered = PAPERS_DATA;
  if (search) filtered = filtered.filter(p => (p.title + p.journal + p.topic + p.domain + p.finding).toLowerCase().includes(search));
  filtered.sort((a, b) => b.rel - a.rel);

  const tbody = document.querySelector('#papersTable tbody');
  tbody.innerHTML = '';
  filtered.forEach(p => {
    const stars = '★'.repeat(p.rel) + '☆'.repeat(5 - p.rel);
    tbody.innerHTML += `
      <tr>
        <td><strong>${p.title}</strong></td>
        <td>${p.journal}</td>
        <td>${p.year}</td>
        <td><span class="badge badge-blue">${p.domain}</span></td>
        <td>${p.topic}</td>
        <td>${p.finding}</td>
        <td style="color: var(--orange);">${stars}</td>
      </tr>
    `;
  });
}

// Initialize
renderOverview();
filterPipelineTable();
renderDomains();
renderTimeline();
renderDatasets();
filterPapersTable();
</script>

<div style="max-width:1100px;margin:2rem auto;padding:0 2rem;">
  <div style="border-top:1px solid #e0ddd5;padding-top:1rem;">
    <h3 style="font-family:Georgia,serif;font-size:1rem;font-weight:400;margin-bottom:0.5rem;">Platform References</h3>
    <p style="font-size:12px;color:#636363;line-height:1.7;">
      Research landscape mapped using PubMed, ClinicalTrials.gov, and IDF Diabetes Atlas data
      (<a href="https://pubmed.ncbi.nlm.nih.gov/37105208/" target="_blank">PMID 37105208</a> &mdash; IDF Atlas 10th ed.).
      Domain taxonomy informed by WHO classification of diabetes research areas and systematic mapping reviews
      (<a href="https://pubmed.ncbi.nlm.nih.gov/29710129/" target="_blank">PMID 29710129</a>;
       <a href="https://pubmed.ncbi.nlm.nih.gov/34763823/" target="_blank">PMID 34763823</a>;
       <a href="https://pubmed.ncbi.nlm.nih.gov/37909353/" target="_blank">PMID 37909353</a>).
      Validation methodology follows triple-source framework aligned with Oxford CEBM evidence levels
      (<a href="https://pubmed.ncbi.nlm.nih.gov/32175717/" target="_blank">PMID 32175717</a>).
    </p>
  </div>
</div>

</body>
</html>
"""
    return html

if __name__ == '__main__':
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Dashboards', 'Research_Dashboard.html')
    html_content = generate_html()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"  Generated Research_Dashboard.html ({len(html_content)} bytes)")
    print(f"  Location: {output_path}")
    print(f"  Data included:")
    print(f"    - {len(PIPELINE_DATA)} pipeline entries")
    print(f"    - {len(DOMAIN_DATA)} research domains")
    print(f"    - {len(DATASET_DATA)} datasets")
    print(f"    - {len(PAPERS_DATA)} papers")
    print(f"    - {len(TIMELINE_2025) + len(TIMELINE_2026)} timeline items")
    print(f"  Style: Tufte-informed (cream bg, serif headers, monospace data, no gradients/rounded corners)")
