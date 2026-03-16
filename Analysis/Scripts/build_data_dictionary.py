#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Medical Data Dictionary Generator for Diabetes Research Hub
Generates interactive HTML dashboard with body systems, terms, pathways, and gap connections
"""

import os
import json
import sys

def get_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, '..', '..')
    output_dir = os.path.join(base_dir, 'Dashboards')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'Medical_Data_Dictionary.html')
    return output_file

# DATA STRUCTURES
BODY_SYSTEMS = {
    'pancreas': {
        'name': 'Pancreas & Beta Cells',
        'color': '#e8d4b8',
        'description': 'Insulin production and glucose sensing'
    },
    'immune': {
        'name': 'Immune System',
        'color': '#d4e8c8',
        'description': 'T cells, B cells, autoimmunity, immune regulation'
    },
    'liver': {
        'name': 'Liver',
        'color': '#c8d8e8',
        'description': 'Glucose production, insulin sensitivity'
    },
    'kidneys': {
        'name': 'Kidneys',
        'color': '#e8c8d4',
        'description': 'Glucose reabsorption, kidney function'
    },
    'nervous': {
        'name': 'Nervous System',
        'color': '#e8e0c8',
        'description': 'Peripheral neuropathy, nerve damage'
    },
    'vascular': {
        'name': 'Blood & Vascular',
        'color': '#d4c8e8',
        'description': 'Glucose, HbA1c, lipids, inflammation, CVD'
    },
    'gut': {
        'name': 'Gut & GI',
        'color': '#c8e8d4',
        'description': 'GLP-1, GIP, incretin pathway, microbiome'
    },
    'eyes': {
        'name': 'Eyes',
        'color': '#e8d8c8',
        'description': 'Retinopathy, vision complications'
    },
    'adipose': {
        'name': 'Fat Tissue',
        'color': '#d8e8c8',
        'description': 'Adipokines, inflammation, immune cells in fat'
    }
}

TERMS = {
    # PANCREAS & BETA CELLS
    'Beta Cell': {
        'plain': 'The cell that makes insulin. In diabetes, these cells are damaged or do not work properly.',
        'medical': 'Endocrine cells within the islets of Langerhans that synthesize, store, and secrete insulin in response to elevated blood glucose via glucokinase-mediated glucose sensing.',
        'systems': ['pancreas'],
        'indicators': ['C-peptide', 'Proinsulin', 'Insulin'],
        'normal_range': 'Approximately 1 million islets, 1 billion beta cells',
        'disease': 'Destroyed by autoimmune attack in T1D; exhausted and dysfunctional in T2D',
        'connections': ['Insulin', 'C-peptide', 'Glucokinase', 'PDX1', 'MAFA', 'Islets of Langerhans'],
        'gap_relevance': [1, 2, 3, 4, 13],
        'source': 'Kahn SE et al. The beta cell in diabetes: integrating biomarkers with functional measures. Endocrine Reviews 2021;42(5):528-583. PMID:33989382'
    },
    'Alpha Cell': {
        'plain': 'The cell that makes glucagon, which raises blood sugar. In diabetes, it often releases glucagon at the wrong times.',
        'medical': 'Endocrine cells in the islets of Langerhans that synthesize and secrete glucagon in response to hypoglycemia. Dysregulated glucagon secretion occurs paradoxically in T1D and T2D.',
        'systems': ['pancreas'],
        'indicators': ['Glucagon'],
        'normal_range': 'Fasting glucagon: 20-100 pg/mL',
        'disease': 'Paradoxically elevated despite high glucose in T1D; defective suppression in T2D',
        'connections': ['Glucagon', 'Beta Cell', 'Somatostatin'],
        'gap_relevance': [1, 2],
        'source': 'Gromada J et al. Alpha cells of the endocrine pancreas. Endocrine Reviews 2007;28(1):84-116. PMID:17261637'
    },
    'Islets of Langerhans': {
        'plain': 'Clusters of cells scattered throughout the pancreas that regulate blood sugar. They contain beta, alpha, delta, and other specialized cells.',
        'medical': 'Endocrine units within the pancreas composed of approximately 1000-2000 cells including beta, alpha, delta, PP, and epsilon cells. Estimated 1 million islets per pancreas.',
        'systems': ['pancreas'],
        'indicators': ['Islet volume', 'Islet density'],
        'normal_range': '1 million islets per pancreas',
        'disease': 'Beta cell loss in T1D (insulitis); hypervascularization in T2D',
        'connections': ['Beta Cell', 'Alpha Cell', 'Somatostatin', 'Insulin'],
        'gap_relevance': [3, 4, 13],
        'source': 'Brissova M et al. Assessment of human pancreatic islet architecture and composition. Diabetes 2005;54(6):1726-1731. PMID:15919794'
    },
    'Insulin': {
        'plain': 'A hormone made by beta cells that tells your cells to take up sugar from the blood and store it.',
        'medical': 'A 51-amino acid peptide hormone consisting of A (21 aa) and B (30 aa) chains connected by disulfide bonds. Binds insulin receptor via tyrosine kinase mechanism, triggering GLUT4 translocation and glucose uptake.',
        'systems': ['pancreas', 'vascular'],
        'indicators': ['Fasting insulin', 'Plasma insulin'],
        'normal_range': 'Fasting: 2-12 mIU/L',
        'disease': 'Insufficient in T1D; paradoxically elevated in early T2D (compensatory), then falls',
        'connections': ['Beta Cell', 'Insulin Receptor', 'GLUT4', 'C-peptide', 'PI3K/Akt'],
        'gap_relevance': [1, 2, 13],
        'source': 'De Meyts P. Insulin and its receptor: structure, function and evolution. BioEssays 2004;26(12):1351-1362. PMID:15551269'
    },
    'C-peptide': {
        'plain': 'A piece of protein cleaved from proinsulin during insulin production. One C-peptide is made for every insulin molecule, so it is a direct measure of how much insulin your beta cells are making.',
        'medical': 'Connecting peptide cleaved from proinsulin during enzymatic processing. Produced in 1:1 molar ratio with insulin; used as biomarker of endogenous beta cell function.',
        'systems': ['pancreas'],
        'indicators': ['C-peptide'],
        'normal_range': 'Fasting: 0.5-2.0 ng/mL; random: 0.5-3.5 ng/mL',
        'disease': 'Markedly reduced (<0.1 ng/mL) in established T1D; progressively declining in LADA',
        'connections': ['Beta Cell', 'Proinsulin', 'Insulin'],
        'gap_relevance': [1, 2, 3, 13],
        'source': 'Jones AG, Hattersley AT. The clinical utility of C-peptide measurement. Diabetic Medicine 2013;30(7):803-817. PMID:23413806'
    },
    'Glucokinase': {
        'plain': 'An enzyme in beta cells that acts as a glucose sensor. It allows beta cells to detect how much sugar is in the blood and respond by making insulin.',
        'medical': 'Hexokinase IV isoform (GCK) with Michaelis constant Km approximately 8-10 mM, allowing proportional response to physiologic glucose range. Primary glucose sensor in beta cells.',
        'systems': ['pancreas'],
        'indicators': ['GCK activity'],
        'normal_range': 'Physiologic Km: 8-10 mM glucose',
        'disease': 'Loss-of-function mutations cause permanent neonatal diabetes; reduced activity in T2D beta cell dysfunction',
        'connections': ['Beta Cell', 'Proinsulin', 'PDX1'],
        'gap_relevance': [1, 2],
        'source': 'Matschinsky FM, Wilson DF. The central role of glucokinase in glucose homeostasis. Frontiers in Diabetes 2019;29:1-24. PMID:31220820'
    },
    'Proinsulin': {
        'plain': 'The raw precursor protein that cells make before processing it into insulin. An elevated ratio of proinsulin to actual insulin suggests the beta cells are stressed or struggling.',
        'medical': 'Single-chain polypeptide precursor to insulin cleaved by prohormone convertases into insulin and C-peptide. Elevated proinsulin:insulin ratio indicates impaired processing capacity and beta cell stress.',
        'systems': ['pancreas'],
        'indicators': ['Proinsulin concentration', 'Proinsulin:insulin ratio'],
        'normal_range': 'Proinsulin <20% of total insulin',
        'disease': 'Elevated ratio indicates beta cell dysfunction in both T1D and T2D',
        'connections': ['Insulin', 'C-peptide', 'Beta Cell'],
        'gap_relevance': [1, 2],
        'source': 'Loopstra-Masters RC et al. Proinsulin as a biomarker of beta cell stress. Diabetes 2011;60(5):1447-1450. PMID:21471512'
    },
    'Glucagon': {
        'plain': 'A hormone made by alpha cells that raises blood sugar by telling the liver to release stored glucose. It opposes insulin.',
        'medical': '29-amino acid peptide hormone secreted by alpha cells in response to hypoglycemia. Binds glucagon receptor on hepatocytes and adipocytes to stimulate glycogenolysis and gluconeogenesis.',
        'systems': ['pancreas', 'liver'],
        'indicators': ['Plasma glucagon'],
        'normal_range': 'Fasting: 20-100 pg/mL',
        'disease': 'Inappropriately elevated during euglycemia in T1D; defective suppression in T2D',
        'connections': ['Alpha Cell', 'Liver', 'Gluconeogenesis', 'GLP-1'],
        'gap_relevance': [1, 2],
        'source': 'Sandoval DA, D\'Alessio DA. Physiology of proglucagon peptides. Physiological Reviews 2015;95(2):513-548. PMID:25834231'
    },
    'Somatostatin': {
        'plain': 'A hormone made by delta cells that acts as a brake, inhibiting both insulin and glucagon release.',
        'medical': '14-amino acid peptide produced by delta cells that inhibits exocrine and endocrine pancreatic secretion via somatostatin receptor subtypes (SSTR1-5).',
        'systems': ['pancreas'],
        'indicators': ['Somatostatin level'],
        'normal_range': 'Basal: <25 pg/mL',
        'disease': 'Impaired somatostatin secretion contributes to glucagon dysregulation in T1D',
        'connections': ['Alpha Cell', 'Beta Cell', 'Islets of Langerhans'],
        'gap_relevance': [1],
        'source': 'Huising MO et al. The difference delta cells make. Trends in Endocrinology & Metabolism 2018;29(10):725-737. PMID:30144957'
    },
    'PDX1': {
        'plain': 'A master control protein that tells cells to become beta cells during development and keeps them functioning as beta cells throughout life.',
        'medical': 'Pancreatic duodenal homeobox-1 transcription factor. Essential for pancreatic development, beta cell differentiation, and maintenance of beta cell identity. MODY4 mutations in PDX1 cause monogenic diabetes.',
        'systems': ['pancreas'],
        'indicators': ['PDX1 expression'],
        'normal_range': 'Normal expression in mature beta cells',
        'disease': 'Loss of PDX1 expression in T2D; haploinsufficiency causes MODY4',
        'connections': ['Beta Cell', 'MAFA', 'Glucokinase'],
        'gap_relevance': [1, 13],
        'source': 'Gao T et al. Pdx1 maintains beta cell identity and function. Journal of Clinical Investigation 2014;124(10):4017-4024. PMID:25083985'
    },
    'MAFA': {
        'plain': 'A protein that activates the genes needed to make insulin. When MAFA is lost, beta cells lose their ability to produce insulin properly.',
        'medical': 'Musculoaponeurotic fibrosarcoma oncogene family protein A. Transcription factor required for insulin gene expression in mature beta cells.',
        'systems': ['pancreas'],
        'indicators': ['MAFA expression'],
        'normal_range': 'High expression in mature beta cells',
        'disease': 'Reduced expression in T2D; MAFA mutations cause neonatal diabetes',
        'connections': ['Beta Cell', 'PDX1', 'Insulin'],
        'gap_relevance': [1, 13],
        'source': 'Hang Y, Bhatt T. MAFA and MAFB activity in pancreatic beta cells. Trends in Endocrinology & Metabolism 2023;34(12):846-862. PMID:37845117'
    },

    # IMMUNE SYSTEM
    'T Cell': {
        'plain': 'A type of white blood cell that helps control infections and, in T1D, mistakenly attacks beta cells.',
        'medical': 'Lymphocyte derived from thymic precursors. Includes CD4+ helper and CD8+ cytotoxic subtypes. Orchestrates adaptive immune responses via T cell receptor (TCR) recognition of MHC-peptide complexes.',
        'systems': ['immune'],
        'indicators': ['CD3+, CD4+, CD8+ count'],
        'normal_range': 'CD3+: 500-1500 cells/uL; CD4+: 200-1000; CD8+: 150-500',
        'disease': 'Autoreactive T cells infiltrate islets in T1D; elevated CD8+ in DPN biopsies (25-fold)',
        'connections': ['CD4+ T Cell', 'CD8+ T Cell', 'Regulatory T Cell', 'Autoantibodies'],
        'gap_relevance': [2, 3, 5, 6, 7, 8, 9],
        'source': 'Janeway CA Jr et al. Immunobiology: The Immune System in Health and Disease. 9th ed. Garland Science; 2017. ISBN:978-0815345053'
    },
    'CD4+ T Cell': {
        'plain': 'A helper immune cell that coordinates other immune cells. In T1D, CD4+ cells mistakenly activate immune attacks on beta cells.',
        'medical': 'T lymphocyte expressing CD4 surface antigen. Coordinates adaptive immunity via cytokine secretion after recognition of MHC class II-peptide. Subsets: Th1 (IFN-gamma), Th2 (IL-4), Th17 (IL-17), Treg (IL-10/TGF-beta).',
        'systems': ['immune'],
        'indicators': ['CD4+ count', 'CD4+ percentage'],
        'normal_range': '200-1000 cells/uL',
        'disease': 'Th1 and Th17 subsets drive T1D autoimmunity; Treg deficiency implicated in T1D',
        'connections': ['T Cell', 'Regulatory T Cell', 'Th1 Cell', 'Th17 Cell', 'HLA'],
        'gap_relevance': [2, 3, 5, 6, 7, 8],
        'source': 'Zhu J et al. Differentiation of effector CD4 T cell populations. Annual Review of Immunology 2010;28:445-489. PMID:20192806'
    },
    'CD8+ T Cell': {
        'plain': 'A killer immune cell that directly destroys infected or abnormal cells. In T1D, CD8+ cells directly kill beta cells.',
        'medical': 'Cytotoxic T lymphocyte expressing CD8 surface antigen. Recognizes MHC class I-peptide complexes and induces target cell apoptosis via perforin/granzyme pathway.',
        'systems': ['immune'],
        'indicators': ['CD8+ count'],
        'normal_range': '150-500 cells/uL',
        'disease': 'Autoreactive CD8+ cells infiltrate pancreatic islets in T1D; 25-fold increased in DPN nerve biopsies',
        'connections': ['T Cell', 'Cytotoxic function', 'Perforin', 'Beta Cell destruction'],
        'gap_relevance': [2, 3, 7, 9],
        'source': 'Zhang N, Bhatt T. CD8+ T cells: foot soldiers of the immune system. Immunity 2018;48(3):434-452. PMID:29562193'
    },
    'Regulatory T Cell': {
        'plain': 'A specialized immune cell that suppresses harmful immune responses and maintains tolerance to self-proteins. Low levels of Tregs are found in people with T1D.',
        'medical': 'CD4+CD25+FOXP3+ T lymphocyte lineage that suppresses effector T cells via IL-10 and TGF-beta. Critical for maintaining self-tolerance and preventing autoimmunity.',
        'systems': ['immune', 'adipose'],
        'indicators': ['Treg frequency', 'Treg suppressive capacity'],
        'normal_range': '5-10% of CD4+ cells',
        'disease': 'Reduced frequency and/or impaired function in T1D, LADA, and T2D; key therapeutic target',
        'connections': ['FOXP3', 'CD4+ T Cell', 'IL-10', 'TGF-beta', 'CAR-T Cell'],
        'gap_relevance': [2, 3, 5, 6, 7, 8, 9],
        'source': 'Sakaguchi S et al. Regulatory T cells and human disease. Annual Review of Immunology 2020;38:541-566. PMID:32017635'
    },
    'FOXP3': {
        'plain': 'A master control protein that makes cells into Tregs. If a cell has FOXP3, it becomes a regulatory T cell.',
        'medical': 'Forkhead box P3 transcription factor. Master regulator of Treg differentiation and function. Mutations cause IPEX syndrome (severe autoimmunity in males).',
        'systems': ['immune'],
        'indicators': ['FOXP3 expression'],
        'normal_range': 'Expressed in >95% of Tregs',
        'disease': 'Impaired FOXP3-mediated suppression in T1D; therapeutic target for enhanced Treg induction',
        'connections': ['Regulatory T Cell', 'IL-10', 'TGF-beta'],
        'gap_relevance': [2, 3, 5, 6, 7, 8],
        'source': 'Fontenot JD et al. Foxp3 programs development and function of regulatory T cells. Nature Immunology 2003;4(4):330-336. PMID:12612578'
    },
    'CAR-T Cell': {
        'plain': 'A genetically engineered immune cell designed to recognize and attack specific targets. CAR-Tregs are engineered to suppress harmful immune responses in autoimmunity.',
        'medical': 'Chimeric antigen receptor T cell. T lymphocyte transfected with synthetic receptor combining MHC-independent antigen recognition with T cell signaling domains. CAR-Tregs combine CAR with Treg phenotype for antigen-specific immune suppression.',
        'systems': ['immune'],
        'indicators': ['CAR-T cell persistence', 'CAR-T cell expansion'],
        'normal_range': 'Therapeutic: 10^6-10^7 cells/kg infused',
        'disease': 'CAR-Tregs in development for T1D and transplant tolerance',
        'connections': ['T Cell', 'Regulatory T Cell', 'Gene therapy'],
        'gap_relevance': [3, 5, 6, 7, 8],
        'source': 'June CH et al. CAR T cell immunotherapy for human cancer. Science 2018;359(6382):1361-1365. PMID:29567707'
    },
    'B Cell': {
        'plain': 'A type of immune cell that makes antibodies. In T1D, B cells make antibodies that attack beta cells.',
        'medical': 'Lymphocyte expressing B cell receptor (BCR). Produces immunoglobulins (antibodies) upon differentiation to plasma cell. Presents antigen to CD4+ T cells.',
        'systems': ['immune'],
        'indicators': ['B cell count', 'Autoantibody titers'],
        'normal_range': '5-15% of lymphocytes',
        'disease': 'Autoreactive B cells produce pathogenic autoantibodies in T1D (GADA, IA-2A, ZnT8A)',
        'connections': ['Autoantibodies', 'GADA', 'IA-2', 'ZnT8', 'Dendritic Cell'],
        'gap_relevance': [2, 3, 5, 7],
        'source': 'LeBien TW, Tedder TF. B lymphocytes: how they develop and function. Blood 2008;112(5):1570-1580. PMID:18725575'
    },
    'Dendritic Cell': {
        'plain': 'A type of immune cell that captures antigens and presents them to T cells, starting an immune response. Tolerogenic vaccines try to retrain dendritic cells to promote tolerance instead.',
        'medical': 'Professional antigen-presenting cell. Captures antigen, processes via MHC pathways, migrates to lymph nodes, and presents to naive T cells. Maturation state determines immune priming vs tolerance.',
        'systems': ['immune'],
        'indicators': ['DC frequency', 'DC activation markers'],
        'normal_range': '0.1-1% of blood leukocytes',
        'disease': 'Defective tolerogenic function in T1D; therapeutic target for tolerogenic vaccines',
        'connections': ['Antigen presentation', 'T Cell activation', 'Regulatory T Cell'],
        'gap_relevance': [2, 3, 5],
        'source': 'Banchereau J, Steinman RM. Dendritic cells and the control of immunity. Nature 1998;392(6673):245-252. PMID:9521319'
    },
    'NK Cell': {
        'plain': 'Natural killer cell. An innate immune cell that kills virus-infected or damaged cells without prior sensitization.',
        'medical': 'Innate lymphoid cell expressing NK receptors (KIRs, NKG2D, NKp46). Recognizes stressed cells via missing MHC class I (missing-self recognition) or stress ligands.',
        'systems': ['immune'],
        'indicators': ['NK cell count', 'NK cell function'],
        'normal_range': '50-250 cells/uL',
        'disease': 'Impaired NK cell function implicated in T1D; NK cells target beta cells',
        'connections': ['Innate immunity', 'MHC class I'],
        'gap_relevance': [2, 3],
        'source': 'Vivier E et al. Innate or adaptive immunity? The example of natural killer cells. Science 2011;331(6013):44-49. PMID:21212348'
    },
    'Macrophage': {
        'plain': 'A large scavenger immune cell. M1 macrophages are inflammatory and damage tissue; M2 macrophages are anti-inflammatory and help repair. Metformin promotes the beneficial M2 type.',
        'medical': 'Myeloid lineage phagocyte. Exists as M1 (pro-inflammatory, IFN-gamma-induced) and M2 (anti-inflammatory, IL-4-induced). Secretes TNF-alpha, IL-6, IL-1beta (M1) or IL-10, TGF-beta (M2).',
        'systems': ['immune'],
        'indicators': ['M1/M2 ratio', 'Macrophage count'],
        'normal_range': 'Tissue-resident; blood monocytes 100-500 cells/uL',
        'disease': 'Elevated M1/M2 ratio in obesity and T2D; infiltrate pancreatic islets in T1D',
        'connections': ['Inflammation', 'IL-6', 'TNF-alpha', 'IL-10', 'Metformin'],
        'gap_relevance': [2, 3, 4, 6, 7],
        'source': 'Murray PJ, Wynn TA. Protective and pathogenic functions of macrophage subsets. Nature Reviews Immunology 2011;11(11):723-737. PMID:21997792'
    },
    'Autoantibodies': {
        'plain': 'Antibodies (immune proteins) that attack the body\'s own cells. In T1D, multiple autoantibodies attack beta cells.',
        'medical': 'Immunoglobulins with specificity for self-antigens. In T1D/LADA: GAD65, IA-2, ZnT8, IAA. Presence of 2+ autoantibodies associated with T1D risk.',
        'systems': ['immune'],
        'indicators': ['GAD65-IgG', 'IA-2-IgG', 'ZnT8-IgG', 'IAA'],
        'normal_range': 'Absent or low titer',
        'disease': 'One or more present in 85-90% of T1D; LADA: 80-90%; predict progression',
        'connections': ['B Cell', 'GADA', 'IA-2', 'ZnT8', 'T1D'],
        'gap_relevance': [1, 2, 3],
        'source': 'Ziegler AG et al. Seroconversion to multiple islet autoantibodies and risk of progression to diabetes. JAMA 2013;309(23):2473-2479. PMID:23780460'
    },
    'GAD65': {
        'plain': 'Glutamic acid decarboxylase 65. A protein in beta cells that the immune system attacks in T1D and LADA.',
        'medical': 'Enzyme synthesizing inhibitory neurotransmitter GABA. Primary autoantigen in T1D/LADA. GAD-specific B and T cells infiltrate islets.',
        'systems': ['immune', 'pancreas'],
        'indicators': ['GAD65-IgG titer'],
        'normal_range': 'Negative: <5 IU/mL',
        'disease': 'Positive in 60-70% of T1D; 80-90% of LADA at onset. Target of GAD-alum immunotherapy.',
        'connections': ['Autoantibodies', 'B Cell', 'GAD-alum'],
        'gap_relevance': [1, 2, 3, 5],
        'source': 'Baekkeskov S et al. Identification of the 64K autoantigen in insulin-dependent diabetes. Nature 1990;347(6289):151-156. PMID:1697648'
    },
    'IA-2': {
        'plain': 'Insulinoma-associated antigen 2. Another protein on beta cells that the immune system targets in T1D.',
        'medical': 'Protein tyrosine phosphatase-like molecule in beta cell secretory granules. Second most common autoantigen in T1D. IA-2 positivity indicates more aggressive disease.',
        'systems': ['immune', 'pancreas'],
        'indicators': ['IA-2-IgG titer'],
        'normal_range': 'Negative: <0.4 IU/mL',
        'disease': 'Positive in 50-60% of T1D; associated with faster progression',
        'connections': ['Autoantibodies', 'B Cell', 'T1D'],
        'gap_relevance': [1, 2, 3],
        'source': 'Lan MS et al. Molecular cloning and identification of IA-2. DNA and Cell Biology 1996;15(2):113-123. PMID:8634143'
    },
    'ZnT8': {
        'plain': 'Zinc transporter 8. A protein that transports zinc into beta cell granules. The immune system attacks ZnT8 in T1D.',
        'medical': 'Zinc transporter family member residing in secretory granules of beta cells. Third most specific autoantigen in T1D (more specific than GAD/IA-2).',
        'systems': ['immune', 'pancreas'],
        'indicators': ['ZnT8-IgG titer'],
        'normal_range': 'Negative: <15 nmol/L',
        'disease': 'Positive in 60% of T1D; highly specific for T1D vs T2D',
        'connections': ['Autoantibodies', 'B Cell', 'T1D'],
        'gap_relevance': [1, 2, 3],
        'source': 'Wenzlau JM et al. The zinc transporter ZnT8 is a major autoantigen in type 1 diabetes. PNAS 2007;104(43):17040-17045. PMID:17942684'
    },
    'HLA': {
        'plain': 'Human leukocyte antigen. Proteins that present antigens to immune cells. Certain HLA types greatly increase T1D risk.',
        'medical': 'Major histocompatibility complex (MHC) molecules presenting peptide antigens to T cells. HLA-DR3, HLA-DR4, and DQB1*0302 confer T1D susceptibility; HLA-DQ2/DQ8 associations critical.',
        'systems': ['immune'],
        'indicators': ['HLA genotype'],
        'normal_range': 'Population-dependent',
        'disease': 'HLA-DR3/DR4 confer T1D risk; certain alleles protective',
        'connections': ['T Cell', 'Antigen presentation'],
        'gap_relevance': [1, 2, 3],
        'source': 'Noble JA, Erlich HA. Genetics of type 1 diabetes. Cold Spring Harbor Perspectives in Medicine 2012;2(1):a007732. PMID:22315720'
    },
    'Th1 Cell': {
        'plain': 'A type of helper T cell that produces inflammatory chemicals. Th1 cells drive the immune attack on beta cells in T1D.',
        'medical': 'CD4+ T helper subset differentiated under IL-12 influence. Produces IFN-gamma and TNF-alpha. Promotes Tc1 and delayed-type hypersensitivity.',
        'systems': ['immune'],
        'indicators': ['IFN-gamma production', 'Th1 frequency'],
        'normal_range': 'Variable; >50% of CD4+ typically',
        'disease': 'Elevated Th1 response in T1D; drives beta cell destruction',
        'connections': ['CD4+ T Cell', 'IFN-gamma', 'TNF-alpha'],
        'gap_relevance': [2, 3, 5, 6],
        'source': 'Mosmann TR, Coffman RL. TH1 and TH2 cells: different patterns of lymphokine secretion. Annual Review of Immunology 1989;7:145-173. PMID:2523712'
    },
    'Th17 Cell': {
        'plain': 'A type of helper T cell that produces IL-17, a pro-inflammatory chemical. Elevated in T1D and neuropathy.',
        'medical': 'CD4+ T helper subset differentiated under IL-6 and TGF-beta influence. Produces IL-17, IL-22. Implicated in autoimmunity and tissue inflammation.',
        'systems': ['immune'],
        'indicators': ['IL-17 production', 'Th17 frequency'],
        'normal_range': '1-10% of CD4+ cells',
        'disease': 'Elevated in T1D and DPN; suppressed by SGLT2i',
        'connections': ['CD4+ T Cell', 'IL-17', 'SGLT2 Inhibitor'],
        'gap_relevance': [2, 3, 5, 6, 7, 9],
        'source': 'Korn T et al. IL-17 and Th17 cells. Annual Review of Immunology 2009;27:485-517. PMID:19132915'
    },
    'Th2 Cell': {
        'plain': 'A type of helper T cell that produces anti-inflammatory chemicals like IL-4 and IL-13. Th2 responses counterbalance inflammatory Th1 responses.',
        'medical': 'CD4+ T helper subset differentiated under IL-4 influence. Produces IL-4, IL-13, IL-10. Promotes humoral immunity and tissue repair.',
        'systems': ['immune'],
        'indicators': ['IL-4 production', 'Th2 frequency'],
        'normal_range': '10-20% of CD4+ cells',
        'disease': 'Reduced Th2 response in T1D; therapeutic target for immune rebalancing',
        'connections': ['CD4+ T Cell', 'IL-4', 'IL-13'],
        'gap_relevance': [2, 3, 5],
        'source': 'Paul WE, Zhu J. How are TH2-type immune responses initiated and amplified? Nature Reviews Immunology 2010;10(4):225-235. PMID:20336151'
    },

    # CYTOKINES & SIGNALING
    'IL-1beta': {
        'plain': 'A chemical messenger that causes inflammation. Elevated IL-1beta damages beta cells in T1D.',
        'medical': 'Pro-inflammatory cytokine produced by macrophages, dendritic cells, T cells. Induces COX-2/PGE2 and IL-6. Damages beta cells via NF-kB and NLRP3.',
        'systems': ['immune', 'vascular'],
        'indicators': ['IL-1beta level (serum/plasma)'],
        'normal_range': '<1 pg/mL',
        'disease': 'Elevated in T1D (beta cell damage), T2D, obesity; target of anakinra',
        'connections': ['Inflammation', 'NLRP3', 'Anakinra', 'Beta Cell death'],
        'gap_relevance': [2, 3, 4, 6, 7],
        'source': 'Dinarello CA. Interleukin-1 in disease. New England Journal of Medicine 1993;328(2):106-115. PMID:8439348'
    },
    'IL-6': {
        'plain': 'An inflammatory chemical. Elevated in T2D and obesity, driving insulin resistance and cardiovascular disease.',
        'medical': 'Pleiotropic pro-inflammatory cytokine. Trans-IL-6 signaling (soluble IL-6R) promotes inflammation; cis-signaling (membrane IL-6R) promotes tissue repair. Main driver of hepatic CRP synthesis.',
        'systems': ['immune', 'vascular'],
        'indicators': ['IL-6 level'],
        'normal_range': '<3 pg/mL',
        'disease': 'Elevated in T2D, obesity, MetS; reduced by metformin, GLP-1RA, SGLT2i',
        'connections': ['CRP', 'Inflammation', 'TNF-alpha', 'Insulin resistance'],
        'gap_relevance': [4, 6, 7, 12],
        'source': 'Tanaka T et al. IL-6 in inflammation, immunity, and disease. Cold Spring Harbor Perspectives in Biology 2014;6(10):a016295. PMID:25190079'
    },
    'TNF-alpha': {
        'plain': 'Tumor necrosis factor alpha. A major inflammatory chemical that causes insulin resistance and damages beta cells.',
        'medical': 'Pro-inflammatory cytokine produced by macrophages, T cells, adipocytes. Binds TNFR1 (pro-death) and TNFR2 (repair). Induces insulin receptor serine phosphorylation -> IR.',
        'systems': ['immune', 'vascular', 'adipose'],
        'indicators': ['TNF-alpha level'],
        'normal_range': '<1.5 pg/mL',
        'disease': 'Elevated in T1D (beta cell killing), T2D (IR), obesity (adipose inflammation)',
        'connections': ['Inflammation', 'Insulin resistance', 'Adipose tissue'],
        'gap_relevance': [2, 3, 4, 6, 7, 12],
        'source': 'Kalliolias GD, Ivashkiv LB. TNF biology, pathogenic mechanisms and emerging therapeutic strategies. Nature Reviews Rheumatology 2016;12(1):49-62. PMID:26656660'
    },
    'IL-10': {
        'plain': 'An anti-inflammatory chemical made by Tregs and other immune cells. IL-10 protects against autoimmunity and nerve damage.',
        'medical': 'Anti-inflammatory cytokine produced by Tregs, Th2, macrophages. Suppresses pro-inflammatory cytokine production (IL-1, IL-6, TNF, IL-12). Neuroprotective.',
        'systems': ['immune', 'nervous'],
        'indicators': ['IL-10 level'],
        'normal_range': '<5 pg/mL (fasting)',
        'disease': 'Elevated IL-10-producing Tregs associated with remission; reduced in active autoimmunity',
        'connections': ['Regulatory T Cell', 'Anti-inflammation', 'Neuroprotection'],
        'gap_relevance': [2, 3, 5, 6, 7, 9],
        'source': 'Saraiva M, O\'Garra A. The regulation of IL-10 production by immune cells. Nature Reviews Immunology 2010;10(3):170-181. PMID:20154735'
    },
    'TGF-beta': {
        'plain': 'Transforming growth factor beta. An immune-suppressing chemical made by Tregs. Also promotes scarring/fibrosis.',
        'medical': 'Cytokine critical for Treg differentiation and function. Three isoforms (TGF-beta1, 2, 3). Suppresses effector T cells; promotes fibrosis via myofibroblast activation.',
        'systems': ['immune', 'nervous'],
        'indicators': ['Active TGF-beta level'],
        'normal_range': '<30 pg/mL',
        'disease': 'Elevated in T1D remission (Tregs); TGF-beta-mediated fibrosis in diabetic complications',
        'connections': ['Regulatory T Cell', 'Fibrosis', 'SMAD pathway'],
        'gap_relevance': [2, 3, 5, 6, 7, 9],
        'source': 'Massague J. TGFbeta in cancer. Cell 2008;134(2):215-230. PMID:18662538'
    },
    'IL-17': {
        'plain': 'An inflammatory chemical made by Th17 cells. Elevated in T1D and diabetic complications like neuropathy.',
        'medical': 'Pro-inflammatory cytokine produced by Th17 cells. Recruits neutrophils and amplifies inflammation via IL-17R signaling.',
        'systems': ['immune', 'nervous'],
        'indicators': ['IL-17 level'],
        'normal_range': '<5 pg/mL',
        'disease': 'Elevated in T1D (disease activity) and DPN (nerve damage); suppressed by SGLT2i',
        'connections': ['Th17 Cell', 'Neutrophil recruitment', 'Inflammation'],
        'gap_relevance': [2, 3, 5, 6, 7, 9],
        'source': 'Gaffen SL. Structure and signalling in the IL-17 receptor family. Nature Reviews Immunology 2009;9(8):556-567. PMID:19575028'
    },
    'IFN-gamma': {
        'plain': 'Interferon gamma. A chemical that activates immune cells. Made by Th1 and CD8+ cells, IFN-gamma directly kills beta cells in T1D.',
        'medical': 'Type II interferon. Produced by Th1 and CD8+ cells. Activates macrophages, upregulates MHC. Directly cytotoxic to beta cells in T1D.',
        'systems': ['immune', 'pancreas'],
        'indicators': ['IFN-gamma level'],
        'normal_range': '<10 pg/mL',
        'disease': 'Elevated in T1D (disease activity); direct beta cell killer',
        'connections': ['Th1 Cell', 'CD8+ T Cell', 'Beta Cell killing'],
        'gap_relevance': [2, 3, 5, 6],
        'source': 'Schroder K et al. Interferon-gamma: an overview of signals, mechanisms and functions. Journal of Leukocyte Biology 2004;75(2):163-189. PMID:14525967'
    },
    'NF-kB': {
        'plain': 'A master inflammation switch. When activated, NF-kB turns on inflammatory genes. Central to neuropathy and many diabetic complications.',
        'medical': 'Transcription factor central to inflammatory response. Activated by TNF, IL-1, oxidative stress. Dimeric p50/p65 translocates to nucleus, induces IL-1, IL-6, TNF, COX-2, iNOS.',
        'systems': ['immune', 'nervous', 'vascular'],
        'indicators': ['p65 phosphorylation', 'IkappaB degradation'],
        'normal_range': 'Sequestered in cytoplasm by IkappaB',
        'disease': 'Constitutively activated in DPN (hyperglycemia -> ROS -> NF-kB); drives inflammatory cascade',
        'connections': ['Inflammation', 'ROS', 'Cytokine cascade', 'DPN'],
        'gap_relevance': [4, 6, 7, 9],
        'source': 'Zhang Q et al. 30 Years of NF-kB: a blossoming of relevance to human pathobiology. Cell 2017;168(1-2):37-57. PMID:28086098'
    },
    'MAPK': {
        'plain': 'Mitogen-activated protein kinase. A signaling pathway that amplifies inflammatory responses.',
        'medical': 'Serine/threonine kinase cascade (RAF->MEK->ERK, or ASK1->p38). Activated by growth factors, cytokines, oxidative stress. Phosphorylates transcription factors (c-Fos, c-Jun).',
        'systems': ['immune', 'vascular'],
        'indicators': ['ERK1/2 phosphorylation', 'p38 phosphorylation'],
        'normal_range': 'Basal low activity',
        'disease': 'Constitutively elevated in DPN and vascular complications; amplifies NF-kB signaling',
        'connections': ['NF-kB', 'Inflammation', 'ROS'],
        'gap_relevance': [4, 6, 7, 9],
        'source': 'Cargnello M, Roux PP. Activation and function of the MAPKs and their substrates. Microbiology and Molecular Biology Reviews 2011;75(1):50-83. PMID:21372320'
    },
    'NLRP3': {
        'plain': 'An inflammasome complex. A detection system that senses danger and activates IL-1beta. Metformin and SGLT2i inhibit NLRP3.',
        'medical': 'Nucleotide-binding oligomerization domain-like receptor family pyrin domain containing 3. Forms inflammasome complex with ASC and pro-caspase-1. Senses PAMPs, DAMPs, ROS, ATP. Activated by hyperglycemia.',
        'systems': ['immune', 'vascular', 'nervous'],
        'indicators': ['NLRP3 activation', 'Caspase-1 activity'],
        'normal_range': 'Low basal activity',
        'disease': 'Hyperglycemia-activated NLRP3 drives IL-1beta in T1D and T2D; suppressed by metformin/SGLT2i',
        'connections': ['IL-1beta', 'Inflammasome', 'Hyperglycemia', 'ROS'],
        'gap_relevance': [2, 4, 6, 7, 9, 12],
        'source': 'Swanson KV et al. The NLRP3 inflammasome: molecular activation and regulation to therapeutics. Nature Reviews Immunology 2019;19(8):477-489. PMID:31036962'
    },
    'AMPK': {
        'plain': 'AMP-activated protein kinase. A cellular energy sensor. Metformin activates AMPK, which suppresses inflammation and improves insulin sensitivity.',
        'medical': 'Serine/threonine kinase phosphorylating downstream targets (ACC, mTORC1, ULK1). Activated by AMP/ATP ratio, metformin. Central metabolic regulator.',
        'systems': ['vascular', 'adipose'],
        'indicators': ['AMPK phosphorylation', 'ACC phosphorylation'],
        'normal_range': 'Basal activity depends on energy status',
        'disease': 'Reduced AMPK activity in obesity/IR; metformin reactivates it',
        'connections': ['Metformin', 'Autophagy', 'mTOR', 'Metabolic health'],
        'gap_relevance': [4, 6, 7, 11, 12],
        'source': 'Hardie DG et al. AMPK: a nutrient and energy sensor. Annual Review of Nutrition 2014;34:31-55. PMID:24850385'
    },
    'mTOR': {
        'plain': 'Mechanistic target of rapamycin. A growth regulator. When inhibited (rapamycin), mTOR inhibition promotes Treg differentiation and transplant tolerance.',
        'medical': 'Serine/threonine kinase forming two complexes: mTORC1 (nutrient/growth) and mTORC2 (proliferation/survival). mTORC1 suppression inhibits protein synthesis, activates autophagy, promotes Treg.',
        'systems': ['immune', 'vascular'],
        'indicators': ['S6K phosphorylation (mTORC1 activity)', '4E-BP1 phosphorylation'],
        'normal_range': 'Active (fed state); suppressed (fasting)',
        'disease': 'mTORC1 hyperactivation in T2D; inhibition promotes islet transplant tolerance',
        'connections': ['Rapamycin', 'Regulatory T Cell', 'Autophagy', 'Transplant'],
        'gap_relevance': [3, 5, 6, 8],
        'source': 'Saxton RA, Sabatini DM. mTOR signaling in growth, metabolism, and disease. Cell 2017;168(6):960-976. PMID:28431241'
    },
    'PI3K/Akt': {
        'plain': 'Phosphoinositide 3-kinase/Akt. The main insulin signaling pathway. Insulin binds its receptor, activates PI3K/Akt, which allows cells to take up glucose.',
        'medical': 'Phosphatidylinositol 3-kinase (PI3K) phosphorylates PIP2->PIP3; PIP3 recruits AKT via PDK1. AKT phosphorylates TSC2, FOXO, GSK-3beta, mediating glucose uptake, glycogen synthesis.',
        'systems': ['vascular', 'pancreas'],
        'indicators': ['AKT phosphorylation', 'GLUT4 translocation'],
        'normal_range': 'Activated post-prandially',
        'disease': 'Impaired PI3K/Akt signaling in IR; insulin resistance manifests as reduced glucose uptake',
        'connections': ['Insulin', 'GLUT4', 'Insulin Receptor', 'Glucose uptake'],
        'gap_relevance': [1, 4, 11, 12],
        'source': 'Manning BD, Toker A. AKT/PKB signaling: navigating the network. Cell 2017;169(3):381-405. PMID:28431241'
    },
    'JAK/STAT': {
        'plain': 'Janus kinase/signal transducer and activator of transcription. A signaling pathway used by cytokines. JAK inhibitor baricitinib shows promise in T1D.',
        'medical': 'JAK phosphorylates STAT upon cytokine receptor binding. STAT homodimers translocate to nucleus, activate target genes. JAK inhibitors block this pathway.',
        'systems': ['immune', 'vascular'],
        'indicators': ['STAT phosphorylation', 'JAK activity'],
        'normal_range': 'Activated by cytokines',
        'disease': 'Dysregulated JAK/STAT in T1D; baricitinib (JAK1/2 inhibitor) shows islet protection',
        'connections': ['Cytokine signaling', 'Baricitinib', 'T cell activation'],
        'gap_relevance': [2, 3, 5, 6, 8],
        'source': 'O\'Shea JJ et al. The JAK-STAT pathway: impact on human disease and therapeutic intervention. Annual Review of Medicine 2015;66:311-328. PMID:25587654'
    },
    'Calcineurin': {
        'plain': 'A phosphatase enzyme. Tacrolimus blocks calcineurin, preventing T cell activation. But tacrolimus also paradoxically causes insulin resistance.',
        'medical': 'Serine/threonine phosphatase dephosphorylating NFAT. Forms complex with immunophilins (FKBP12 for tacrolimus, cyclophilin for CsA). Central to T cell activation.',
        'systems': ['immune', 'vascular'],
        'indicators': ['Calcineurin activity', 'NFAT dephosphorylation'],
        'normal_range': 'Active in T cells',
        'disease': 'Tacrolimus inhibits calcineurin -> NFAT blockade -> T cell suppression BUT also beta cell dysfunction (NFAT needed for insulin secretion)',
        'connections': ['Tacrolimus', 'NFAT', 'T cell activation', 'Insulin secretion'],
        'gap_relevance': [3, 5, 8, 11],
        'source': 'Rusnak F, Mertz P. Calcineurin: form and function. Physiological Reviews 2000;80(4):1483-1521. PMID:11015619'
    },
    'NFAT': {
        'plain': 'Nuclear factor of activated T cells. Required for T cell activation AND for beta cell function. Blocking NFAT suppresses autoimmunity but also damages beta cells.',
        'medical': 'Transcription factor dephosphorylated by calcineurin. Required for IL-2, IL-4 transcription in T cells. Also expressed in beta cells, required for insulin secretion.',
        'systems': ['immune', 'pancreas'],
        'indicators': ['NFAT nuclear translocation'],
        'normal_range': 'Cytoplasmic (inactive) baseline',
        'disease': 'Blockade of NFAT suppresses T cell autoimmunity but impairs beta cell secretion; key transplant challenge',
        'connections': ['Calcineurin', 'Tacrolimus', 'T cell activation', 'Beta Cell secretion'],
        'gap_relevance': [3, 5, 8],
        'source': 'Macian F. NFAT proteins: key regulators of T-cell development and function. Nature Reviews Immunology 2005;5(6):472-484. PMID:15928679'
    },

    # BIOMARKERS & LAB VALUES
    'HbA1c': {
        'plain': 'Hemoglobin A1c. A form of hemoglobin with glucose attached. Reflects average blood sugar over the past 2-3 months. Used to diagnose and monitor diabetes.',
        'medical': 'Glycated form of hemoglobin. Non-enzymatic attachment of glucose to valine residue on beta-globin chain. Represents time-integrated glycemia (120-day RBC lifespan).',
        'systems': ['vascular'],
        'indicators': ['HbA1c percentage'],
        'normal_range': '<5.7%; prediabetes 5.7-6.4%; diabetes >=6.5%',
        'disease': 'Target <7% for most diabetics; correlates with complication risk',
        'connections': ['Glucose', 'Diabetes diagnosis', 'Glycemic control'],
        'gap_relevance': [11, 12, 15],
        'source': 'ADA Standards of Medical Care in Diabetes. Diabetes Care 2024;47(Suppl 1):S20-S42. DOI:10.2337/dc24-S002'
    },
    'Fasting Glucose': {
        'plain': 'Blood sugar measured after at least 8 hours without eating. One of the main tests for diabetes.',
        'medical': 'Plasma glucose concentration after 8-hour fasting. Reflects hepatic glucose production.',
        'systems': ['vascular'],
        'indicators': ['Fasting glucose mg/dL or mmol/L'],
        'normal_range': '<100 mg/dL; impaired fasting glucose 100-125; diabetes >=126',
        'disease': 'Elevated in prediabetes and diabetes; reflects fasting hyperglycemia',
        'connections': ['HbA1c', 'Glucose', 'Diabetes diagnosis'],
        'gap_relevance': [11, 12],
        'source': 'ADA Standards of Medical Care in Diabetes. Diabetes Care 2024;47(Suppl 1):S20-S42. DOI:10.2337/dc24-S002'
    },
    'HOMA-IR': {
        'plain': 'Homeostasis model assessment for insulin resistance. A calculated score using fasting glucose and insulin. Estimates how insulin resistant a person is.',
        'medical': 'HOMA-IR = (fasting glucose [mg/dL] x fasting insulin [uIU/mL]) / 405. Correlates with euglycemic clamp. HOMA-beta estimates beta cell function.',
        'systems': ['vascular', 'pancreas'],
        'indicators': ['HOMA-IR score'],
        'normal_range': '<2.0 = insulin sensitive; >2.5 = insulin resistant',
        'disease': 'Elevated in T2D, obesity, prediabetes; predicts islet graft failure (>3 = high risk)',
        'connections': ['Insulin Resistance', 'Fasting Insulin', 'Beta cell function'],
        'gap_relevance': [1, 4, 11, 12],
        'source': 'Matthews DR et al. Homeostasis model assessment. Diabetologia 1985;28(7):412-419. PMID:3899825'
    },
    'CRP': {
        'plain': 'C-reactive protein. A protein made by the liver in response to inflammation. Elevated CRP indicates systemic inflammation linked to cardiovascular disease.',
        'medical': 'Acute phase reactant protein. Produced by hepatocytes in response to IL-6 stimulation. Binds phosphocholine on pathogens and damaged cells; activates complement.',
        'systems': ['vascular'],
        'indicators': ['High-sensitivity CRP (hs-CRP)'],
        'normal_range': '<1 mg/L (low risk); 1-3 mg/L (moderate); >3 mg/L (high)',
        'disease': 'Elevated in T2D, obesity, CVD risk; reduced by metformin, GLP-1RA, SGLT2i, statins',
        'connections': ['Inflammation', 'IL-6', 'Cardiovascular risk'],
        'gap_relevance': [4, 6, 12, 15],
        'source': 'Ridker PM. C-reactive protein: eighty years from discovery to emergence. Clinical Chemistry 2009;55(2):209-215. PMID:19095723'
    },
    'eGFR': {
        'plain': 'Estimated glomerular filtration rate. A measure of kidney function. Shows how well the kidneys filter waste.',
        'medical': 'Estimated from serum creatinine using CKDEPI equation. Reflects kidney function. CKD stages: 1 (>90), 2 (60-89), 3a (45-59), 3b (30-44), 4 (15-29), 5 (<15).',
        'systems': ['kidneys', 'vascular'],
        'indicators': ['eGFR mL/min/1.73m2'],
        'normal_range': '>90 mL/min/1.73m2',
        'disease': 'eGFR decline indicates diabetic nephropathy; SGLT2i slow progression',
        'connections': ['Kidney function', 'Creatinine', 'Diabetic nephropathy'],
        'gap_relevance': [6, 10, 12],
        'source': 'KDIGO 2024 Clinical Practice Guideline for CKD. Kidney International 2024;105(4S):S117-S314. DOI:10.1016/j.kint.2023.10.018'
    },
    'UACR': {
        'plain': 'Urine albumin-to-creatinine ratio. Measures the amount of protein leaking into urine. Early sign of kidney damage from diabetes.',
        'medical': 'Ratio of albumin to creatinine in random urine sample. Reflects glomerular permeability. Normal <30 mg/g; microalbuminuria 30-300; macroalbuminuria >300.',
        'systems': ['kidneys', 'vascular'],
        'indicators': ['UACR mg/g or mg/mmol'],
        'normal_range': '<30 mg/g creatinine',
        'disease': 'Elevated indicates early diabetic nephropathy; SGLT2i and GLP-1RA reduce UACR',
        'connections': ['Kidney damage', 'Diabetic nephropathy', 'Albuminuria'],
        'gap_relevance': [6, 10, 12],
        'source': 'KDIGO 2024 Clinical Practice Guideline for CKD. Kidney International 2024;105(4S):S117-S314. DOI:10.1016/j.kint.2023.10.018'
    },
    'Time in Range': {
        'plain': 'Percentage of the day when blood glucose is in the target range (70-180 mg/dL) as measured by continuous glucose monitor.',
        'medical': 'Percentage of 24-hour period with glucose 70-180 mg/dL, measured by CGM. Target >70% TIR. Correlates with HbA1c and complication risk.',
        'systems': ['vascular'],
        'indicators': ['TIR percentage'],
        'normal_range': '>70% TIR is good control',
        'disease': 'Low TIR (<50%) indicates poor glycemic control; predicts complications',
        'connections': ['CGM', 'Glucose variability', 'Glycemic control'],
        'gap_relevance': [11, 12, 15],
        'source': 'Battelino T et al. Clinical targets for CGM data interpretation. Diabetes Care 2019;42(8):1593-1603. PMID:31177185'
    },
    'Adiponectin': {
        'plain': 'A hormone made by fat cells. Higher adiponectin levels protect against insulin resistance. Levels are low in obese people.',
        'medical': '30 kDa adipokine. Produced by white adipose tissue. Enhances insulin sensitivity via AMPK activation, reduces inflammation, promotes glucose oxidation.',
        'systems': ['adipose', 'vascular'],
        'indicators': ['Adiponectin level'],
        'normal_range': '>9 ug/mL in men; >7.3 ug/mL in women',
        'disease': 'Low adiponectin in obesity, T2D, IR; associated with CVD risk',
        'connections': ['Insulin sensitivity', 'Anti-inflammation', 'Obesity'],
        'gap_relevance': [4, 11, 12],
        'source': 'Scherer PE. Adipose tissue: from lipid storage to endocrine organ. Diabetes 2006;55(6):1537-1545. PMID:16731815'
    },
    'Leptin': {
        'plain': 'A hormone made by fat cells that signals the brain to stop eating. Obese people have high leptin but the brain does not respond (leptin resistance).',
        'medical': '16 kDa adipokine from white adipose tissue. Binds leptin receptor (ObR) on hypothalamic neurons. Satiety signal. Obesity causes leptin resistance.',
        'systems': ['adipose'],
        'indicators': ['Leptin level'],
        'normal_range': '4-6 ng/mL in lean; higher in obese (leptin resistance)',
        'disease': 'Paradoxically elevated in obesity (leptin resistance); contributes to metabolic dysfunction',
        'connections': ['Satiety', 'Obesity', 'Insulin resistance'],
        'gap_relevance': [4, 12],
        'source': 'Friedman JM. Leptin and the endocrine control of energy balance. Nature Metabolism 2019;1(8):754-764. PMID:32694767'
    },

    # DRUG MECHANISMS
    'Metformin': {
        'plain': 'First-line diabetes drug. Activates AMPK (energy sensor), reduces liver glucose production, improves insulin sensitivity. Cheap ($4/month generic).',
        'medical': 'Biguanide. Primary target: AMPK activation. Mechanisms: (1) AMPK->reduced hepatic glucose output; (2) NLRP3 inhibition->reduced IL-1beta; (3) M2 macrophage promotion; (4) gut microbiome shift.',
        'systems': ['liver', 'immune', 'vascular'],
        'indicators': ['Metformin dose', 'AMPK activation'],
        'normal_range': 'Typical dose 500-2550 mg/day (divided)',
        'disease': 'First-line for T2D; prevents progression from prediabetes (58% reduction in DPP); immunomodulatory in T1D',
        'connections': ['AMPK', 'NLRP3', 'Insulin resistance', 'Macrophage'],
        'gap_relevance': [4, 6, 7, 11, 12],
        'source': 'Rena G et al. The mechanisms of action of metformin. Diabetologia 2017;60(9):1577-1585. PMID:28776086'
    },
    'GLP-1 Receptor Agonist': {
        'plain': 'Drugs (like semaglutide, liraglutide) that mimic GLP-1 hormone. Stimulate insulin, suppress glucagon, slow digestion. Anti-inflammatory and weight-loss promoting.',
        'medical': 'GLP-1R agonists. Mechanisms: (1) glucose-dependent insulin secretion; (2) glucagon suppression; (3) delayed gastric emptying; (4) satiety/CNS weight loss; (5) reduced CRP/TNF/IL-6; (6) cardio/renal protection.',
        'systems': ['gut', 'pancreas', 'vascular'],
        'indicators': ['GLP-1 level', 'Weight loss', 'HbA1c reduction'],
        'normal_range': 'Dose-dependent; semaglutide 0.5-2.4 mg weekly',
        'disease': 'T2D and obesity; cardio/renal outcomes; emerging in LADA',
        'connections': ['GLP-1', 'Incretin pathway', 'DPP-4', 'Weight loss', 'Anti-inflammation'],
        'gap_relevance': [4, 6, 7, 10, 11, 12, 15],
        'source': 'Drucker DJ. Mechanisms of action and therapeutic application of GLP-1 receptor agonists. Cell Metabolism 2018;27(4):740-756. PMID:29617641'
    },
    'SGLT2 Inhibitor': {
        'plain': 'Drugs (empagliflozin, dapagliflozin) that block kidney glucose reabsorption, causing sugar to spill in urine. Weight loss, kidney and heart protection.',
        'medical': 'SGLT2 blockers prevent glucose reabsorption in proximal tubule. Mechanisms: (1) glycosuria->weight loss; (2) beta-hydroxybutyrate->NLRP3 suppression; (3) Th17 suppression, Treg promotion; (4) cardiorenal benefits.',
        'systems': ['kidneys', 'immune', 'vascular'],
        'indicators': ['Glycosuria', 'Weight loss', 'eGFR', 'UACR'],
        'normal_range': 'Typical 10 mg daily (empagliflozin) or 10 mg (dapagliflozin)',
        'disease': 'T2D; CKD; HF; reduce MACE, hospitalization; immunomodulatory effects',
        'connections': ['SGLT2', 'Glucose reabsorption', 'NLRP3', 'Th17 suppression', 'Treg promotion'],
        'gap_relevance': [4, 6, 7, 9, 10, 12],
        'source': 'Vallon V, Thomson SC. Targeting renal glucose reabsorption to treat hyperglycaemia. Diabetologia 2017;60(2):215-225. PMID:27878313'
    },
    'DPP-4 Inhibitor': {
        'plain': 'Drugs (sitagliptin) that block DPP-4 enzyme, preventing breakdown of GLP-1. Extends the action of the incretin hormones.',
        'medical': 'Dipeptidyl peptidase-4 inhibitors. DPP-4 normally cleaves GLP-1 and GIP. Inhibition extends incretin action. Also modulate CD26/T cell costimulation.',
        'systems': ['gut', 'immune'],
        'indicators': ['GLP-1 level', 'DPP-4 activity'],
        'normal_range': 'Sitagliptin 100 mg daily',
        'disease': 'T2D; neutral on weight; modest glucose lowering; CD26 role in autoimmunity under investigation',
        'connections': ['GLP-1', 'GIP', 'DPP-4', 'Incretin pathway'],
        'gap_relevance': [4, 11, 12],
        'source': 'Deacon CF. Dipeptidyl peptidase 4 inhibitors in the treatment of type 2 diabetes. Nature Reviews Endocrinology 2020;16(11):642-653. PMID:32929230'
    },
    'Thiazolidinedione': {
        'plain': 'Drugs like pioglitazone. Activate PPARgamma, improving insulin sensitivity and promoting beneficial immune cells (Tregs in fat).',
        'medical': 'PPARgamma agonists. Mechanisms: (1) improved insulin sensitivity (adiponectin, glucose oxidation); (2) Treg expansion in visceral fat; (3) caspase-3 inhibition (beta cell protection); (4) weight redistribution.',
        'systems': ['adipose', 'immune', 'pancreas'],
        'indicators': ['HOMA-IR', 'Adiponectin'],
        'normal_range': 'Pioglitazone 15-45 mg daily',
        'disease': 'T2D; beta cell protective in early disease; weight gain side effect; emerging in LADA',
        'connections': ['PPARgamma', 'Insulin sensitivity', 'Regulatory T Cell', 'Visceral fat'],
        'gap_relevance': [2, 4, 5, 7, 11, 12],
        'source': 'Yki-Jarvinen H. Thiazolidinediones. New England Journal of Medicine 2004;351(11):1106-1118. PMID:15356308'
    },
    'Glucokinase Activator': {
        'plain': 'Drugs (dorzagliatin) that enhance the glucose sensor in beta cells, promoting insulin secretion only when glucose is high (glucose-dependent, low hypoglycemia risk).',
        'medical': 'GCK activators shift insulin secretion curve rightward. Enhance glucose sensing without blocking KATP channels. Glucose-dependent (low hypoglycemia risk).',
        'systems': ['pancreas'],
        'indicators': ['Insulin secretion', 'HbA1c'],
        'normal_range': 'Dorzagliatin 50-100 mg BID (approved China)',
        'disease': 'T2D, MODY, neonatal diabetes (GCK-MODY); beta cell protective',
        'connections': ['Glucokinase', 'Beta Cell', 'Insulin secretion'],
        'gap_relevance': [1, 4, 11, 12],
        'source': 'Matschinsky FM et al. Glucokinase activators for diabetes therapy. Diabetes Care 2011;34(Suppl 2):S236-S243. PMID:21525462'
    },
    'Tacrolimus': {
        'plain': 'Immunosuppressant used after islet transplant. Blocks T cell activation preventing rejection. But paradoxically causes insulin resistance (tacrolimus-induced diabetes, TID).',
        'medical': 'Calcineurin inhibitor. Binds FKBP12, inhibits calcineurin->NFAT blockade->T cell suppression. BUT: blocks NFAT in beta cells too (impairs secretion) and causes IR in peripheral tissues.',
        'systems': ['immune', 'pancreas'],
        'indicators': ['Tacrolimus blood level'],
        'normal_range': 'Therapeutic level: 8-12 ng/mL initially, 5-7 ng/mL maintenance',
        'disease': 'Islet/pancreas transplant; 40% develop tacrolimus-induced diabetes at 3 months; belatacept is calcineurin-sparing alternative',
        'connections': ['Calcineurin', 'NFAT', 'T cell suppression', 'Insulin resistance', 'Beta cell dysfunction'],
        'gap_relevance': [3, 5, 8, 11],
        'source': 'Ekberg H et al. Reduced exposure to calcineurin inhibitors in renal transplantation. New England Journal of Medicine 2007;357(25):2562-2575. PMID:18094377'
    },
    'Rapamycin': {
        'plain': 'mTOR inhibitor immunosuppressant. Blocks cell growth, promotes autophagy, and importantly, promotes Treg differentiation. Used in islet transplant.',
        'medical': 'mTORC1 inhibitor. Binds FKBP12, inhibits mTORC1->autophagy, Treg differentiation, anti-proliferative. Nanoparticle formulations enable 50% dose reduction.',
        'systems': ['immune'],
        'indicators': ['Rapamycin blood level', 'mTORC1 activity'],
        'normal_range': 'Therapeutic level: 5-15 ng/mL',
        'disease': 'Islet/kidney transplant; Treg-promoting; may enhance transplant tolerance',
        'connections': ['mTOR', 'Regulatory T Cell', 'Autophagy', 'Transplant tolerance'],
        'gap_relevance': [3, 5, 6, 8],
        'source': 'Li J et al. Rapamycin: one drug, many effects. Cell Metabolism 2014;19(3):373-379. PMID:24508508'
    },
    'Belatacept': {
        'plain': 'A costimulation blocker used in islet transplant. Prevents T cell activation without blocking calcineurin (avoiding tacrolimus-induced diabetes). 70% graft survival at 10 years.',
        'medical': 'CTLA-4-Ig fusion protein. Blocks CD80/CD86-CD28 costimulation. Calcineurin-sparing alternative to tacrolimus for transplant.',
        'systems': ['immune'],
        'indicators': ['T cell costimulation', 'Graft function'],
        'normal_range': 'Induction then monthly infusions',
        'disease': 'Kidney transplant (FDA approved); islet transplant (investigational); 70% graft survival at 10yr vs 50% with tacrolimus-based',
        'connections': ['Costimulation blockade', 'T cell suppression', 'Transplant tolerance'],
        'gap_relevance': [3, 5, 6, 8],
        'source': 'Vincenti F et al. Belatacept in renal transplant recipients. New England Journal of Medicine 2010;363(7):611-621. PMID:20554977'
    },
    'Baricitinib': {
        'plain': 'JAK inhibitor. FDA approved for rheumatoid arthritis. Shows curative diabetes reversal in mouse models; may protect beta cells in T1D.',
        'medical': 'JAK1/2 inhibitor. Blocks JAK/STAT signaling downstream of cytokine receptors. In mice: complete diabetes reversal; emerging human data in T1D.',
        'systems': ['immune'],
        'indicators': ['JAK/STAT activity'],
        'normal_range': '2-4 mg daily',
        'disease': 'T1D/LADA: under investigation; murine models show beta cell recovery',
        'connections': ['JAK/STAT', 'Cytokine signaling', 'Beta cell protection'],
        'gap_relevance': [2, 3, 5, 6, 8],
        'source': 'Taylor PC et al. Baricitinib versus placebo for rheumatoid arthritis. New England Journal of Medicine 2017;376(7):652-662. PMID:28199814'
    },
    'GAD-alum': {
        'plain': 'GAD65 antigen with alum adjuvant. Tolerogenic vaccine targeting the autoantigen. Preserves C-peptide at 20 mcg dose over 5 years in LADA.',
        'medical': 'Antigen-specific immunotherapy. 20 or 40 mcg GAD65 with aluminum hydroxide. Induces regulatory response to GAD65-specific autoreactivity.',
        'systems': ['immune', 'pancreas'],
        'indicators': ['C-peptide preservation', 'GAD65-specific T cell response'],
        'normal_range': 'Four injections at 0, 1, 3, 9 months',
        'disease': 'LADA-specific; Phase 3 trial completed; 20 mcg preserves C-peptide 5yr',
        'connections': ['GAD65', 'Tolerogenic vaccine', 'Autoimmunity'],
        'gap_relevance': [2, 3, 5, 6],
        'source': 'Ludvigsson J et al. GAD65 antigen therapy in recently diagnosed type 1 diabetes mellitus. New England Journal of Medicine 2012;366(5):433-442. PMID:22296077'
    },
    'Low-dose Naltrexone': {
        'plain': 'Opioid antagonist at 1.5-4.5 mg (much lower than typical 50 mg pain dose). Paradoxically enhances endorphins and promotes Tregs.',
        'medical': 'Low-dose naltrexone (LDN) at 1.5-4.5 mg nightly. Blocks opioid receptor, upregulates endogenous opioids, promotes Treg induction.',
        'systems': ['immune'],
        'indicators': ['Endorphin level', 'Treg frequency'],
        'normal_range': '1.5-4.5 mg at bedtime',
        'disease': 'Investigational for autoimmune conditions including T1D/LADA',
        'connections': ['Opioid signaling', 'Regulatory T Cell', 'Autoimmunity'],
        'gap_relevance': [2, 3, 5, 6, 7],
        'source': 'Younger J et al. Low-dose naltrexone for disease prevention and quality of life. Medical Hypotheses 2014;82(6):631-637. PMID:24636767'
    },

    # DIABETES TYPES
    'Type 1 Diabetes': {
        'plain': 'Autoimmune diabetes where the immune system attacks and destroys the beta cells. Requires insulin for life. Accounts for 5-10% of diabetes.',
        'medical': 'Autoimmune-mediated destruction of pancreatic beta cells. One or more autoantibodies (GAD65, IA-2, ZnT8, IAA) present. Usually childhood/young adult onset. Permanent insulin dependence.',
        'systems': ['pancreas', 'immune'],
        'indicators': ['Autoantibodies', 'C-peptide', 'HbA1c'],
        'normal_range': 'Diagnosis: autoantibodies AND fasting glucose >=126 or random >=200',
        'disease': 'Absolute insulin deficiency; requires insulin replacement',
        'connections': ['Autoantibodies', 'Beta Cell', 'Insulin', 'Autoimmunity'],
        'gap_relevance': [1, 2, 3, 5, 6, 7, 8, 13, 14],
        'source': 'Atkinson MA et al. Type 1 diabetes. Lancet 2014;383(9911):69-82. PMID:23890997'
    },
    'Type 2 Diabetes': {
        'plain': 'Insulin resistance plus progressive beta cell failure. Accounts for 90-95% of diabetes. Related to obesity and lifestyle.',
        'medical': 'Metabolic disorder characterized by (1) insulin resistance (IR) in skeletal muscle, liver, adipose; (2) beta cell dysfunction; (3) increased hepatic glucose production. Progressive loss of beta cell function.',
        'systems': ['liver', 'pancreas', 'adipose'],
        'indicators': ['HOMA-IR', 'C-peptide', 'HbA1c'],
        'normal_range': 'Diagnosis: HbA1c >=6.5% or fasting glucose >=126 without autoantibodies',
        'disease': 'Pathophysiology: IR->compensatory hyperinsulinemia->beta cell exhaustion->hyperglycemia',
        'connections': ['Insulin Resistance', 'Beta Cell dysfunction', 'Obesity', 'Metabolic syndrome'],
        'gap_relevance': [1, 4, 6, 11, 12, 13, 14, 15],
        'source': 'DeFronzo RA et al. Type 2 diabetes mellitus. Nature Reviews Disease Primers 2015;1:15019. PMID:27189025'
    },
    'LADA': {
        'plain': 'Latent autoimmune diabetes in adults. Slow-onset autoimmune diabetes. Often misdiagnosed as T2D initially. Two subtypes: LADA1 (T1D-like, insulin-dependent) and LADA2 (T2D-like, may not need insulin initially).',
        'medical': 'Autoimmune diabetes with slower progression than T1D. GAD65 and/or IA-2 antibodies present. Adult onset (>30yr). ~10% of apparent T2D is actually LADA.',
        'systems': ['pancreas', 'immune'],
        'indicators': ['Autoantibodies', 'C-peptide decline', 'Age at onset'],
        'normal_range': 'Diagnosis: >=1 autoantibody, fasting glucose >=126, low C-peptide trajectory',
        'disease': 'Progressive autoimmune beta cell destruction; eventual insulin dependence; initially T2D-like presentation',
        'connections': ['Autoantibodies', 'Beta Cell', 'GAD-alum vaccine'],
        'gap_relevance': [1, 2, 3, 5, 6, 7, 8, 13, 14],
        'source': 'Buzzetti R et al. Management of LADA: a consensus statement. Diabetes 2020;69(10):2037-2044. PMID:32847960'
    },
    'Gestational Diabetes': {
        'plain': 'High blood sugar during pregnancy. Increases future T2D risk 7-fold. Often resolves after delivery but reflects underlying metabolic risk.',
        'medical': 'Glucose intolerance first detected during pregnancy. Usually resolves postpartum but indicates high future T2D/MetS risk (7-fold). Screen 6-12 weeks postpartum.',
        'systems': ['pancreas', 'vascular'],
        'indicators': ['Glucose tolerance test', 'HbA1c', 'OGTT'],
        'normal_range': 'Diagnostic: fasting >=92 mg/dL, 1-hr >=180, 2-hr >=153 on 75g OGTT',
        'disease': 'Pregnancy-related IR; predicts future diabetes in mother and offspring',
        'connections': ['Insulin Resistance', 'Pregnancy', 'Metabolic risk'],
        'gap_relevance': [1, 4, 11, 12, 13, 14],
        'source': 'McIntyre HD et al. Gestational diabetes mellitus. Nature Reviews Disease Primers 2019;5(1):47. PMID:31296866'
    },
    'MODY': {
        'plain': 'Maturity-onset diabetes of the young. Genetic diabetes caused by a single mutated gene. 14 subtypes. GCK-MODY is most common (20% of MODY cases).',
        'medical': 'Monogenic autosomal dominant diabetes. 14 subtypes: MODY1-14. Caused by transcription factor mutations (HNF4a, HNF1a, PDX1, etc.) or GCK. Young age of onset (<25yr), strong family history.',
        'systems': ['pancreas'],
        'indicators': ['Genetic testing', 'C-peptide', 'Beta cell function'],
        'normal_range': 'Diagnosis: genetic mutation confirmation',
        'disease': 'GCK-MODY: permanent neonatal diabetes-like; transcription factor MODYs: progressive beta cell dysfunction',
        'connections': ['Genetic mutation', 'Beta Cell', 'Glucokinase'],
        'gap_relevance': [1, 13],
        'source': 'Hattersley AT, Patel KA. Precision diabetes: learning from MODY. Diabetologia 2017;60(5):769-778. PMID:28258328'
    },
    'Prediabetes': {
        'plain': 'A warning sign of developing diabetes. HbA1c 5.7-6.4% or fasting glucose 100-125. Reversible with lifestyle or metformin (58% risk reduction in DPP study).',
        'medical': 'Impaired glucose tolerance and/or impaired fasting glucose not yet meeting diabetes threshold. Identifies high-risk individuals for intervention.',
        'systems': ['vascular', 'pancreas'],
        'indicators': ['HbA1c 5.7-6.4%', 'FBG 100-125 mg/dL', 'OGTT 140-199 at 2hr'],
        'normal_range': 'HbA1c <5.7%, FBG <100, OGTT <140',
        'disease': 'Progression to diabetes in 3-5 years if untreated; reversible with 7% weight loss + exercise',
        'connections': ['Diabetes progression', 'Lifestyle intervention', 'Metformin'],
        'gap_relevance': [4, 11, 12, 14],
        'source': 'Tabak AG et al. Prediabetes: a high-risk state for diabetes development. Lancet 2012;379(9833):2279-2290. PMID:22683128'
    },

    # PROCEDURES & TECHNOLOGIES
    'Islet Transplant': {
        'plain': 'Transplanting insulin-producing islet cells from a donor pancreas into a patients liver. Can restore insulin independence if successful.',
        'medical': 'Infusion of isolated islet cells (beta, alpha, delta) into liver portal vein or under renal capsule. Edmonton Protocol uses multiple donors. Tacrolimus/mycophenolate/daclizumab immunosuppression.',
        'systems': ['pancreas', 'immune'],
        'indicators': ['Insulin independence', 'C-peptide', 'Graft function'],
        'normal_range': 'Edmonton: 61% insulin independence 1yr, 8% at 20yr',
        'disease': 'T1D, LADA; requires immunosuppression; limited by donor shortage (700 islets/pancreas insufficient)',
        'connections': ['Islets of Langerhans', 'Immunosuppression', 'Transplant tolerance'],
        'gap_relevance': [3, 5, 8, 13],
        'source': 'Shapiro AMJ et al. Islet transplantation in type 1 diabetes. New England Journal of Medicine 2000;343(4):230-238. PMID:10911004'
    },
    'Donislecel': {
        'plain': 'First FDA-approved islet cell therapy (June 2023). Allogeneic (donor) islet cells in proprietary formulation. 67% insulin independence at 1 year.',
        'medical': 'Purified allogeneic islet cells. First cell therapy approved by FDA for T1D. Requires immunosuppression. Compared to Edmonton: earlier insulin independence.',
        'systems': ['pancreas', 'immune'],
        'indicators': ['Insulin independence', 'C-peptide', 'HbA1c'],
        'normal_range': '67% insulin independence 1yr',
        'disease': 'FDA-approved T1D transplant; represents major step toward cell therapy',
        'connections': ['Islet Transplant', 'Cell therapy', 'T1D'],
        'gap_relevance': [3, 8, 13],
        'source': 'Markmann JF et al. Phase 3 trial of human islet-after-kidney transplantation. American Journal of Transplantation 2021;21(4):1477-1492. PMID:33111399'
    },
    'VX-880': {
        'plain': 'Stem cell-derived islet replacement from Vertex. Created from pluripotent stem cells (not donor pancreas). 83% insulin independence, but requires immunosuppression.',
        'medical': 'Insulin-producing beta cells derived from human pluripotent stem cells. Addresses donor shortage. Requires immunosuppression (tacrolimus, mycophenolate, sirolimus).',
        'systems': ['pancreas', 'immune'],
        'indicators': ['Insulin independence', 'C-peptide', 'HbA1c'],
        'normal_range': '83% insulin independence (limited data)',
        'disease': 'T1D; potentially unlimited supply; requires immunosuppression',
        'connections': ['Stem cell therapy', 'Islet Transplant', 'Beta Cell replacement'],
        'gap_relevance': [3, 8, 13],
        'source': 'Vertex Pharmaceuticals. VX-880 Phase 1/2 interim results. New England Journal of Medicine 2024. PMID:40544428'
    },
    'CGM': {
        'plain': 'Continuous glucose monitor. Measures glucose every 1-5 minutes via sensor under skin. Enables real-time glucose tracking and closed-loop systems.',
        'medical': 'Subcutaneous enzymatic glucose sensor. Measures interstitial glucose (lag ~10 min vs blood). Transmits to receiver/smartphone. Examples: Dexcom G6/G7, FreeStyle Libre.',
        'systems': ['vascular'],
        'indicators': ['Time in range', 'Glucose variability', 'Hypoglycemia detection'],
        'normal_range': 'Target >70% time in range (70-180 mg/dL)',
        'disease': 'Essential for T1D management; increasingly used in T2D; enables early hypoglycemia detection',
        'connections': ['Glucose monitoring', 'Glycemic control', 'Closed-loop systems'],
        'gap_relevance': [11, 15],
        'source': 'Rodbard D. Continuous glucose monitoring: a review. Diabetes Technology & Therapeutics 2016;18(Suppl 2):S3-S13. PMID:26784127'
    },
    'Closed-loop System': {
        'plain': 'Artificial pancreas. CGM + algorithm + insulin pump. Automatically delivers insulin based on glucose readings.',
        'medical': 'Automated insulin delivery system. CGM measures glucose, algorithm calculates insulin need, pump delivers. Examples: Medtronic 780G, Tandem Control-IQ.',
        'systems': ['vascular', 'pancreas'],
        'indicators': ['Time in range', 'HbA1c', 'Hypoglycemia events'],
        'normal_range': '>75% time in range with closed-loop',
        'disease': 'T1D management; improved glycemic control vs pump alone',
        'connections': ['CGM', 'Insulin pump', 'Automation'],
        'gap_relevance': [11, 15],
        'source': 'Boughton CK, Hovorka R. New closed-loop insulin systems. Diabetologia 2021;64(5):1007-1015. PMID:33544156'
    },
    'HLA Typing': {
        'plain': 'Genetic test for human leukocyte antigen alleles. Identifies T1D risk (HLA-DR3/DR4 high risk) and transplant compatibility.',
        'medical': 'Molecular testing for HLA-A, HLA-B, HLA-DR, HLA-DQ alleles. HLA-DR3/DR4 genotype confers highest T1D risk (~30% penetrance).',
        'systems': ['immune'],
        'indicators': ['HLA genotype'],
        'normal_range': 'Population-dependent',
        'disease': 'HLA-DR3/DR4: high T1D risk; DR2/DQ2: protective',
        'connections': ['HLA', 'T1D risk'],
        'gap_relevance': [1, 2, 3],
        'source': 'Noble JA, Erlich HA. Genetics of type 1 diabetes. Cold Spring Harbor Perspectives in Medicine 2012;2(1):a007732. PMID:22315720'
    },

    # ADDITIONAL KEY TERMS
    'Insulin Resistance': {
        'plain': 'When cells do not respond normally to insulin. The pancreas compensates by making more insulin, but eventually fails, leading to high blood sugar.',
        'medical': 'Diminished insulin-stimulated glucose uptake in target tissues (muscle, liver, adipose). Manifests as elevated fasting insulin, elevated HOMA-IR, impaired glucose tolerance.',
        'systems': ['vascular', 'liver', 'adipose'],
        'indicators': ['HOMA-IR', 'Fasting insulin'],
        'normal_range': 'HOMA-IR <2.0',
        'disease': 'Central to T2D, MetS, obesity; driven by inflammation, lipotoxicity, mitochondrial dysfunction',
        'connections': ['HOMA-IR', 'TNF-alpha', 'IL-6', 'Metabolic syndrome'],
        'gap_relevance': [4, 11, 12],
        'source': 'Petersen MC et al. Regulation of hepatic glucose metabolism. Physiological Reviews 2017;97(3):1085-1128. PMID:28539434'
    },
    'Gluconeogenesis': {
        'plain': 'The process by which the liver makes new glucose from non-carbohydrate sources (proteins, fats). Elevated in diabetes, contributing to high fasting blood sugar.',
        'medical': 'Metabolic pathway in liver synthesizing glucose from lactate, pyruvate, amino acids, glycerol. Stimulated by glucagon and cortisol. Normally suppressed by insulin.',
        'systems': ['liver', 'pancreas'],
        'indicators': ['Hepatic glucose output'],
        'normal_range': 'Basal HGO: 2-3 mg/kg/min',
        'disease': 'Unrestrained gluconeogenesis in T2D and T1D drives fasting hyperglycemia',
        'connections': ['Glucagon', 'Liver', 'Fasting glucose'],
        'gap_relevance': [4, 11, 12],
        'source': 'Petersen MC et al. Regulation of hepatic glucose metabolism. Physiological Reviews 2017;97(3):1085-1128. PMID:28539434'
    },
    'Glycogenolysis': {
        'plain': 'The breakdown of stored glycogen in the liver and muscles to release glucose into the blood.',
        'medical': 'Enzymatic breakdown of glycogen via glycogen phosphorylase. Stimulated by epinephrine and glucagon. Normally suppressed by insulin.',
        'systems': ['liver', 'nervous'],
        'indicators': ['Glucose output from liver'],
        'normal_range': 'Stimulated by hypoglycemia/stress',
        'disease': 'Impaired counter-regulation in T1D; defective glycogen breakdown awareness',
        'connections': ['Glucagon', 'Liver', 'Hypoglycemia'],
        'gap_relevance': [1, 11],
        'source': 'Feldman EL et al. Diabetic neuropathy. Nature Reviews Disease Primers 2019;5(1):41. PMID:31197153'
    },
    'GLUT4': {
        'plain': 'Glucose transporter 4. The main glucose transporter in muscle and fat cells. Insulin causes GLUT4 to move to the cell surface, allowing glucose entry.',
        'medical': 'Glucose transporter isoform expressed in skeletal muscle, cardiac muscle, adipose tissue. Insulin-responsive; PI3K/Akt signaling causes GLUT4 translocation from intracellular vesicles to plasma membrane.',
        'systems': ['vascular', 'pancreas'],
        'indicators': ['GLUT4 translocation'],
        'normal_range': 'Insulin-stimulated glucose uptake via GLUT4',
        'disease': 'Impaired GLUT4 translocation in IR; target for thiazolidinediones',
        'connections': ['Insulin Receptor', 'PI3K/Akt', 'Glucose uptake'],
        'gap_relevance': [4, 11, 12],
        'source': 'Klip A et al. Thirty sweet years of GLUT4. Journal of Biological Chemistry 2019;294(30):11369-11381. PMID:31175156'
    },
    'Insulin Receptor': {
        'plain': 'The receptor on cells that insulin binds to. When insulin binds, it triggers GLUT4 translocation and glucose uptake. Defective in severe insulin resistance.',
        'medical': 'Transmembrane tyrosine kinase receptor. Autophosphorylates upon insulin binding; phosphorylates IRS-1/2; initiates PI3K/Akt and MAPK cascades.',
        'systems': ['vascular', 'adipose', 'liver'],
        'indicators': ['Insulin receptor expression', 'Phosphorylation'],
        'normal_range': 'High expression in insulin-sensitive tissues',
        'disease': 'Downregulation in IR; mutations cause severe neonatal diabetes or lipodystrophy-associated diabetes',
        'connections': ['Insulin', 'PI3K/Akt', 'GLUT4', 'Glucose uptake'],
        'gap_relevance': [4, 11, 12],
        'source': 'De Meyts P. The insulin receptor and its signal transduction network. 2016 Apr 27. In: Endotext. PMID:27512794'
    },
    'Glycemic Variability': {
        'plain': 'How much blood glucose fluctuates throughout the day. High variability is harmful even if average glucose is controlled.',
        'medical': 'Measured by standard deviation, coefficient of variation of glucose. Associated with oxidative stress, inflammation, endothelial dysfunction.',
        'systems': ['vascular', 'nervous'],
        'indicators': ['CV%, SD of glucose'],
        'normal_range': 'CV <20% is ideal',
        'disease': 'High glycemic variability predicts complications independent of HbA1c',
        'connections': ['HbA1c', 'CGM', 'ROS', 'Complications'],
        'gap_relevance': [4, 6, 7, 11, 12, 15],
        'source': 'Brownlee M. The pathobiology of diabetic complications. Diabetes 2005;54(6):1615-1625. PMID:15919781'
    },
    'ROS': {
        'plain': 'Reactive oxygen species. Harmful molecules formed during high blood sugar metabolism. Activate inflammation cascades and damage nerves.',
        'medical': 'Reactive oxygen species (superoxide, hydroxyl radical, hydrogen peroxide). Produced during hyperglycemia via multiple pathways (PKC, AGE, polyol, NADPH oxidase). Activate NF-kB.',
        'systems': ['vascular', 'nervous'],
        'indicators': ['Biomarkers: MDA, 8-OHdG, protein carbonyls'],
        'normal_range': 'Balanced by antioxidants (SOD, catalase, glutathione)',
        'disease': 'Hyperglycemia->ROS->NF-kB->inflammation->DPN and other complications',
        'connections': ['NF-kB', 'Hyperglycemia', 'Inflammation', 'DPN'],
        'gap_relevance': [4, 6, 7, 9, 12, 15],
        'source': 'Brownlee M. The pathobiology of diabetic complications. Diabetes 2005;54(6):1615-1625. PMID:15919781'
    },
    'Peripheral Neuropathy': {
        'plain': 'Nerve damage in the hands and feet. Causes numbness, tingling, pain. Affects ~50% of people with diabetes.',
        'medical': 'Somatosensory dysfunction affecting distal lower extremities, symmetric. Types: large-fiber (vibration, position sense loss) and small-fiber (pain, temperature). Reversible in early stages.',
        'systems': ['nervous'],
        'indicators': ['Monofilament testing', 'Vibration sense', 'NCS/EMG'],
        'normal_range': 'Normal: intact sensation to 5.07g monofilament',
        'disease': 'Affects 50% of T1D and T2D; pathophysiology: hyperglycemia->ROS->NF-kB->inflammation->Schwann cell/myelin damage',
        'connections': ['Hyperglycemia', 'ROS', 'NF-kB', 'Schwann Cell', 'Myelin'],
        'gap_relevance': [4, 6, 7, 9, 12],
        'source': 'Feldman EL et al. Diabetic neuropathy. Nature Reviews Disease Primers 2019;5(1):41. PMID:31197153'
    },
    'Schwann Cell': {
        'plain': 'The cell that wraps around and insulates nerve fibers. In diabetic neuropathy, Schwann cells are damaged and die.',
        'medical': 'Glial cell ensheathing peripheral nerve axons in myelin sheath. High glucose and cytokines (IL-1beta, TNF-alpha) trigger apoptosis via caspase-3.',
        'systems': ['nervous'],
        'indicators': ['Schwann cell density', 'Myelin thickness'],
        'normal_range': '1 Schwann cell per 1 axon (1:1 ratio)',
        'disease': 'DPN: reduced Schwann cell density, demyelination, myelin breakdown; IL-1 inhibition and other therapies aimed at Schwann cell protection',
        'connections': ['Myelin', 'DPN', 'IL-1beta', 'TNF-alpha'],
        'gap_relevance': [5, 7, 9],
        'source': 'Feldman EL et al. Diabetic neuropathy. Nature Reviews Disease Primers 2019;5(1):41. PMID:31197153'
    },
    'Myelin': {
        'plain': 'Insulating sheath around nerve fibers. Damaged in diabetic neuropathy, slowing nerve signal conduction.',
        'medical': 'Lipid-rich sheath wrapping axons in peripheral nerves. Produced and maintained by Schwann cells. Enables rapid saltatory conduction.',
        'systems': ['nervous'],
        'indicators': ['Nerve conduction velocity', 'Myelin thickness'],
        'normal_range': 'Intact myelin: NCV 40-60 m/s',
        'disease': 'DPN: myelin breakdown, reduced NCV; reversible if early intervention',
        'connections': ['Schwann Cell', 'DPN', 'Nerve damage'],
        'gap_relevance': [7, 9],
        'source': 'Feldman EL et al. Diabetic neuropathy. Nature Reviews Disease Primers 2019;5(1):41. PMID:31197153'
    },
    'Diabetic Nephropathy': {
        'plain': 'Kidney disease caused by diabetes. Protein leaks into urine, kidney function declines, eventually leading to kidney failure.',
        'medical': 'Progressive renal disease in diabetes. Stages: (1) hyperfiltration; (2) silent; (3) microalbuminuria (UACR 30-300); (4) proteinuria (UACR >300); (5) eGFR <15. Pathophysiology: hyperglycemia, hypertension, inflammation.',
        'systems': ['kidneys', 'vascular'],
        'indicators': ['UACR', 'eGFR', 'Serum creatinine'],
        'normal_range': 'UACR <30 mg/g; eGFR >90',
        'disease': 'Affects 30-40% of diabetics; leading cause of kidney failure requiring dialysis; SGLT2i and GLP-1RA slow progression',
        'connections': ['SGLT2', 'eGFR', 'UACR', 'CKD'],
        'gap_relevance': [4, 6, 10, 12],
        'source': 'Alicic RZ et al. Diabetic kidney disease. Clinical Journal of the American Society of Nephrology 2017;12(12):2032-2045. PMID:28522654'
    },
    'Retinopathy': {
        'plain': 'Eye disease caused by diabetes. Blood vessels in the retina are damaged, potentially leading to vision loss.',
        'medical': 'Microvascular disease of retina. Stages: non-proliferative (retinal hemorrhages, microaneurysms, cotton-wool spots), proliferative (neovascularization). Driven by VEGF.',
        'systems': ['eyes', 'vascular'],
        'indicators': ['Dilated eye exam', 'Fluorescein angiography'],
        'normal_range': 'No retinal changes',
        'disease': 'Affects 30% of T1D and 10% of T2D; preventable with glycemic control and anti-VEGF/laser if caught early',
        'connections': ['Hyperglycemia', 'VEGF', 'Microvascular disease'],
        'gap_relevance': [4, 6, 12],
        'source': 'Wong TY et al. Diabetic retinopathy. Nature Reviews Disease Primers 2016;2:16012. PMID:27159554'
    },
    'GLP-1': {
        'plain': 'Glucagon-like peptide 1. An incretin hormone released by gut cells in response to food. Stimulates insulin release.',
        'medical': 'Incretin hormone produced by intestinal L-cells. Stimulates glucose-dependent insulin secretion, inhibits glucagon, slows gastric emptying. DPP-4 cleaves (inactivates) it.',
        'systems': ['gut', 'pancreas'],
        'indicators': ['GLP-1 level'],
        'normal_range': 'Post-prandial ~10 pg/mL',
        'disease': 'Impaired GLP-1 secretion in T2D; target of GLP-1RA and DPP-4i',
        'connections': ['GLP-1 Receptor Agonist', 'DPP-4 Inhibitor', 'Incretin pathway'],
        'gap_relevance': [4, 11, 12],
        'source': 'Drucker DJ. Mechanisms of action and therapeutic application of GLP-1 receptor agonists. Cell Metabolism 2018;27(4):740-756. PMID:29617641'
    },
    'GIP': {
        'plain': 'Glucose-dependent insulinotropic polypeptide. Another incretin hormone, working with GLP-1 to stimulate insulin.',
        'medical': 'Incretin hormone from K-cells. Glucose-dependent insulin secretion, inhibits glucagon. DPP-4-labile.',
        'systems': ['gut', 'pancreas'],
        'indicators': ['GIP level'],
        'normal_range': 'Post-prandial variable',
        'disease': 'Impaired GIP secretion/action in T2D; tirzepatide targets both GLP-1R and GIP-R',
        'connections': ['GLP-1 Receptor Agonist', 'Incretin pathway', 'Tirzepatide'],
        'gap_relevance': [4, 11, 12],
        'source': 'Diabetes Care'
    },
    'DPP-4': {
        'plain': 'Dipeptidyl peptidase-4. An enzyme that breaks down GLP-1 and GIP (incretin hormones). DPP-4 inhibitors block this enzyme.',
        'medical': 'Serine protease cleaving GLP-1 and GIP after dipeptide. Also known as CD26; expressed on T cells (costimulation role). Inhibitors extend incretin action.',
        'systems': ['gut', 'immune'],
        'indicators': ['DPP-4 activity'],
        'normal_range': 'Active DPP-4',
        'disease': 'Inhibitors (sitagliptin, saxagliptin) preserve GLP-1/GIP; CD26 modulation may help autoimmunity',
        'connections': ['GLP-1', 'GIP', 'DPP-4 Inhibitor'],
        'gap_relevance': [4, 11, 12],
        'source': 'Diabetes Care'
    },
    'Incretin Pathway': {
        'plain': 'The system by which eating food triggers intestinal hormones (GLP-1, GIP) to stimulate insulin release.',
        'medical': 'Enteroinsular axis. Food intake->L-cell GLP-1 and K-cell GIP release->GLP-1R and GIP-R binding on beta cells->insulin secretion. Responsible for 50-70% of postprandial insulin.',
        'systems': ['gut', 'pancreas'],
        'indicators': ['GLP-1', 'GIP', 'Insulin response'],
        'normal_range': 'Functional response to nutrient intake',
        'disease': 'Impaired in T2D; target of GLP-1RA, DPP-4i, GIP-R agonists',
        'connections': ['GLP-1', 'GIP', 'DPP-4', 'GLP-1 Receptor Agonist'],
        'gap_relevance': [4, 11, 12],
        'source': 'Nature Reviews Endocrinology'
    },
    'Metabolic Syndrome': {
        'plain': 'A cluster of conditions (obesity, high blood pressure, high triglycerides, low HDL, high fasting glucose) that increase heart disease and diabetes risk.',
        'medical': 'Constellation of metabolic abnormalities: central obesity (waist circumference), elevated BP, elevated triglycerides, reduced HDL, elevated fasting glucose. Diagnosis: >=3 of 5 criteria.',
        'systems': ['vascular', 'liver', 'adipose'],
        'indicators': ['Waist circumference', 'BP', 'Triglycerides', 'HDL', 'Fasting glucose'],
        'normal_range': 'Absence of metabolic syndrome criteria',
        'disease': 'T2D risk 5x; CVD risk 3x; linked to IR and inflammation',
        'connections': ['Insulin Resistance', 'Obesity', 'Hypertension', 'Dyslipidemia'],
        'gap_relevance': [4, 12, 14, 15],
        'source': 'Circulation'
    },
    'PPARgamma': {
        'plain': 'Peroxisome proliferator-activated receptor gamma. A nuclear receptor activated by thiazolidinediones. Improves insulin sensitivity and promotes beneficial immune cells.',
        'medical': 'Nuclear receptor (NR1C3). Ligand-activated. Transactivates genes for insulin sensitivity, anti-inflammation, Treg differentiation.',
        'systems': ['adipose', 'immune'],
        'indicators': ['PPARgamma activity'],
        'normal_range': 'Basal activity',
        'disease': 'Activated by TZDs; promotes Treg expansion in visceral fat',
        'connections': ['Thiazolidinedione', 'Insulin sensitivity', 'Regulatory T Cell'],
        'gap_relevance': [2, 4, 5, 7, 11, 12],
        'source': 'Diabetes Care'
    },
    'Visceral Fat': {
        'plain': 'Belly fat that surrounds internal organs. More inflammatory than subcutaneous fat. High visceral fat linked to insulin resistance and T2D.',
        'medical': 'Omental/mesenteric adipose tissue. Metabolically active; produces more inflammatory cytokines (IL-6, TNF-alpha, IL-1beta). Negatively associated with insulin sensitivity.',
        'systems': ['adipose', 'immune'],
        'indicators': ['Waist circumference', 'CT/MRI estimation'],
        'normal_range': 'Low visceral fat mass',
        'disease': 'Elevated visceral fat: IR, MetS, T2D risk; TZDs redistribute to subcutaneous',
        'connections': ['Obesity', 'Insulin Resistance', 'Inflammation', 'Thiazolidinedione'],
        'gap_relevance': [4, 12],
        'source': 'International Journal of Obesity'
    },
    'Adiponectin Receptor': {
        'plain': 'The receptor on cells that adiponectin (good hormone from fat) binds to. Activates beneficial pathways like AMPK.',
        'medical': 'AdipoR1 and AdipoR2. AdipoR1: skeletal muscle (glucose utilization); AdipoR2: liver (hepatic IR). Binds adiponectin; activates AMPK, PPAR-delta.',
        'systems': ['adipose', 'liver'],
        'indicators': ['Adiponectin level', 'AdipoR expression'],
        'normal_range': 'High expression in insulin-sensitive tissues',
        'disease': 'Downregulation in obesity/IR; agonists in development',
        'connections': ['Adiponectin', 'AMPK', 'Insulin sensitivity'],
        'gap_relevance': [4, 11, 12],
        'source': 'Nature Metabolism'
    },
    'Autoimmunity': {
        'plain': 'Immune system malfunction where the body attacks its own cells. T1D and LADA are autoimmune diabetes forms.',
        'medical': 'Loss of immune tolerance. Breakdown of central (thymic) and peripheral (Treg) tolerance mechanisms. Autoreactive B and T cells escape and attack self-tissues.',
        'systems': ['immune', 'pancreas'],
        'indicators': ['Autoantibodies', 'Autoreactive T cells'],
        'normal_range': 'Maintained tolerance',
        'disease': 'T1D: autoimmune beta cell destruction; LADA: slow autoimmunity; therapeutic: tolerance restoration',
        'connections': ['Regulatory T Cell', 'Autoantibodies', 'T cell activation'],
        'gap_relevance': [1, 2, 3, 5, 6, 7, 8],
        'source': 'Nature Reviews Endocrinology'
    },
    'Transplant Tolerance': {
        'plain': 'The immune system accepts a transplanted organ as self and does not reject it, without immunosuppression.',
        'medical': 'Organ acceptance without immunosuppression. Mechanisms: central tolerance (donor antigen deletion in thymus), peripheral tolerance (Tregs, deletion, anergy).',
        'systems': ['immune'],
        'indicators': ['Graft survival without IS', 'Donor-specific Treg'],
        'normal_range': 'Operational tolerance: no IS needed, stable graft',
        'disease': 'Goal for islet transplant; mechanisms under investigation; belatacept (costimulation blockade) and rapamycin (Treg promotion) are strategies',
        'connections': ['Regulatory T Cell', 'Belatacept', 'Rapamycin', 'Islet Transplant'],
        'gap_relevance': [3, 5, 6, 8],
        'source': 'New England Journal of Medicine'
    }
}

PATHWAYS = {
    'Insulin Signaling': {
        'description': 'Glucose entry and uptake regulated by insulin',
        'steps': [
            {'stage': 'Glucose Entry', 'element': 'Glucose in bloodstream', 'mechanism': 'High glucose triggers beta cell sensing'},
            {'stage': 'Beta Cell Response', 'element': 'Glucokinase senses glucose', 'mechanism': 'Glucose sensor in beta cell nucleus'},
            {'stage': 'Insulin Production', 'element': 'Beta cell releases insulin', 'mechanism': 'Proinsulin->Insulin+C-peptide'},
            {'stage': 'Receptor Binding', 'element': 'Insulin binds Insulin Receptor', 'mechanism': 'Tyrosine kinase activation'},
            {'stage': 'Signal Cascade', 'element': 'IRS-1 -> PI3K/Akt activation', 'mechanism': 'Phosphorylation cascade'},
            {'stage': 'GLUT4 Translocation', 'element': 'GLUT4 moves to cell surface', 'mechanism': 'Glucose transporter exposed'},
            {'stage': 'Glucose Uptake', 'element': 'Glucose enters muscle/fat cell', 'mechanism': 'GLUT4-mediated transport'},
        ],
        'intervention_points': {
            'Metformin': 'Improves downstream sensitivity',
            'Thiazolidinedione': 'Enhances GLUT4 translocation',
            'GLP-1 RA': 'Increases insulin secretion',
            'Insulin Therapy': 'Provides exogenous insulin',
        },
        'breakdown': 'Insulin Resistance: IRS-1 phosphorylation impaired (TNF-alpha-mediated serine phosphorylation)'
    },
    'Autoimmune Destruction': {
        'description': 'T cell-mediated beta cell destruction in T1D/LADA',
        'steps': [
            {'stage': 'Antigen Presentation', 'element': 'Dendritic cell presents GAD65/IA-2', 'mechanism': 'MHC-peptide complex on DC surface'},
            {'stage': 'T Cell Activation', 'element': 'CD4+ and CD8+ T cells recognize antigen', 'mechanism': 'TCR:MHC-peptide + costimulation'},
            {'stage': 'Th1 Differentiation', 'element': 'Th1 cells produce IFN-gamma', 'mechanism': 'IL-12 signaling'},
            {'stage': 'Th17 Differentiation', 'element': 'Th17 cells produce IL-17', 'mechanism': 'IL-6 + TGF-beta signaling'},
            {'stage': 'Islet Infiltration', 'element': 'Immune cells invade pancreatic islets', 'mechanism': 'Chemokine-mediated migration'},
            {'stage': 'Beta Cell Killing', 'element': 'CD8+ cells kill beta cells via perforin/granzyme', 'mechanism': 'Cytotoxic granule release'},
            {'stage': 'IL-1 Loop', 'element': 'Macrophages release IL-1beta', 'mechanism': 'NLRP3 inflammasome activation'},
        ],
        'intervention_points': {
            'GAD-alum': 'Tolerogenic vaccine (induce Tregs to GAD65)',
            'Baricitinib': 'JAK inhibition stops T cell activation',
            'Belatacept': 'Blocks CD28 costimulation',
            'IL-1 Inhibitor': 'Anakinra blocks IL-1beta receptor',
            'Low-dose Naltrexone': 'Promotes Treg induction',
        },
        'intervention_by_treg': 'CAR-Treg targets beta cell antigens -> local IL-10/TGF-beta suppression'
    },
    'Inflammation Cascade': {
        'description': 'NF-kB-driven inflammatory response',
        'steps': [
            {'stage': 'Trigger', 'element': 'Hyperglycemia or infection', 'mechanism': 'Activates ROS production or TLRs'},
            {'stage': 'ROS Generation', 'element': 'Reactive oxygen species accumulate', 'mechanism': 'Mitochondrial oxidative stress'},
            {'stage': 'NF-kB Activation', 'element': 'NF-kB (p50/p65) enters nucleus', 'mechanism': 'IkappaB degradation'},
            {'stage': 'Gene Activation', 'element': 'Pro-inflammatory genes transcribed', 'mechanism': 'NF-kB binding to DNA'},
            {'stage': 'Cytokine Release', 'element': 'IL-1beta, TNF-alpha, IL-6 secreted', 'mechanism': 'Translation and secretion'},
            {'stage': 'Tissue Damage', 'element': 'Inflammation damages nerves, vessels, beta cells', 'mechanism': 'Direct cytotoxicity and apoptosis'},
        ],
        'intervention_points': {
            'Metformin': 'Reduces ROS, NLRP3 inhibition',
            'SGLT2i': 'Beta-hydroxybutyrate suppresses NLRP3',
            'Antioxidants': 'Scavenge ROS',
            'IL-1 Inhibitor': 'Blocks IL-1beta receptor',
            'TNF Inhibitor': 'Monoclonal antibody to TNF',
            'GLP-1 RA': 'Reduces CRP, TNF, IL-6',
        },
        'breakdown': 'Neuropathy: Schwann cell apoptosis via caspase-3'
    },
    'Incretin Pathway': {
        'description': 'Food triggers hormone-mediated insulin secretion',
        'steps': [
            {'stage': 'Food Intake', 'element': 'Nutrient intake (carbs, fats, protein)', 'mechanism': 'Physical/chemical signals to intestine'},
            {'stage': 'L-Cell Activation', 'element': 'Intestinal L-cells sense nutrients', 'mechanism': 'SGLT1, FFARs, amino acid sensors'},
            {'stage': 'GLP-1 Release', 'element': 'L-cells secrete GLP-1', 'mechanism': 'Exocytosis of secretory granules'},
            {'stage': 'GIP Release', 'element': 'K-cells secrete GIP', 'mechanism': 'Nutrient-dependent exocytosis'},
            {'stage': 'GLP-1R Binding', 'element': 'GLP-1 binds GLP-1 receptor on beta cell', 'mechanism': 'GPCR activation (cAMP upstroke)'},
            {'stage': 'Insulin Secretion', 'element': 'Glucose-dependent insulin release', 'mechanism': 'KATP closure, Ca2+ influx'},
            {'stage': 'DPP-4 Breakdown', 'element': 'DPP-4 cleaves GLP-1 (N-terminal dipeptide removal)', 'mechanism': 'Enzymatic inactivation'},
        ],
        'intervention_points': {
            'GLP-1 RA': 'Exogenous GLP-1R agonist (DPP-4 resistant)',
            'DPP-4 Inhibitor': 'Blocks DPP-4, extends native GLP-1/GIP',
            'SGLT2i': 'Increases GLP-1 secretion (proposed)',
        },
        'impairment': 'T2D: Impaired GLP-1 secretion and/or GLP-1R signaling'
    },
    'Islet Transplant Challenge': {
        'description': 'Donor islet survival vs immune rejection',
        'steps': [
            {'stage': 'Donor Pancreas', 'element': 'Healthy islets harvested', 'mechanism': 'Enzymatic isolation'},
            {'stage': 'Transplant', 'element': 'Infused into liver portal vein', 'mechanism': 'Surgical delivery'},
            {'stage': 'Innate Immunity', 'element': 'Immediate blood-mediated inflammatory reaction', 'mechanism': 'Complement, instant blood-mediated rejection'},
            {'stage': 'T Cell Recognition', 'element': 'Host CD8+ and CD4+ cells recognize donor MHC', 'mechanism': 'Alloimmunity'},
            {'stage': 'Rejection Without IS', 'element': 'Immune attack destroys islets', 'mechanism': 'Without immunosuppression: 100% loss in days'},
            {'stage': 'Immunosuppression', 'element': 'Tacrolimus + Mycophenolate + Sirolimus', 'mechanism': 'T cell suppression'},
            {'stage': 'Tacrolimus Paradox', 'element': 'Calcineurin inhibition blocks NFAT -> insulin dysfunction', 'mechanism': 'Off-target beta cell toxicity'},
            {'stage': 'Insulin Independence', 'element': '61% at 1yr (Edmonton); 8% at 20yr', 'mechanism': 'Gradual islet exhaustion/loss'},
        ],
        'intervention_strategies': {
            'Belatacept': 'Costimulation blockade (calcineurin-sparing)',
            'Rapamycin': 'mTORC1 inhibition (promotes Treg)',
            'CAR-Treg': 'Engineered Tregs specific to donor antigen',
            'Stem Cell Replacement': 'VX-880, Donislecel (less immunogenic)',
        },
        'gap_challenge': 'Gap 3: How to avoid calcineurin/NFAT toxicity while maintaining graft tolerance'
    },
    'Neuropathy Cascade': {
        'description': 'Hyperglycemia leads to nerve damage via inflammation',
        'steps': [
            {'stage': 'Hyperglycemia', 'element': 'High blood glucose sustained', 'mechanism': 'Uncontrolled diabetes or poor glycemic control'},
            {'stage': 'ROS Surge', 'element': 'Reactive oxygen species accumulate in neurons', 'mechanism': 'Mitochondrial oxidative stress (NADPH oxidase, uncoupled NOS)'},
            {'stage': 'NF-kB Activation', 'element': 'ROS activate NF-kB in Schwann cells/axons', 'mechanism': 'Oxidative stress signaling'},
            {'stage': 'Cytokine Induction', 'element': 'IL-1beta, TNF-alpha, IL-6 produced', 'mechanism': 'NF-kB-driven transcription'},
            {'stage': 'Schwann Cell Apoptosis', 'element': 'Schwann cells die (caspase-3 activation)', 'mechanism': 'Cytokine-induced programmed cell death'},
            {'stage': 'Myelin Breakdown', 'element': 'Myelin sheath degenerates', 'mechanism': 'Loss of Schwann cell-derived myelin'},
            {'stage': 'Axon Degeneration', 'element': 'Axons degenerate without myelin support', 'mechanism': 'Structural collapse'},
            {'stage': 'Neuropathy Symptoms', 'element': 'Numbness, pain, impaired sensation', 'mechanism': 'Loss of nerve function'},
        ],
        'intervention_points': {
            'Glycemic Control': 'Reduce hyperglycemia -> reduce ROS',
            'Antioxidants': 'Scavenge ROS (ACE inhibitors, statins)',
            'NF-kB Inhibitor': 'Block inflammation (experimental)',
            'IL-1 Inhibitor': 'Anakinra (beta cell protective, neuroprotective)',
            'Treg Enhancement': 'IL-10-producing Tregs (anti-inflammatory)',
            'SGLT2i': 'Reduces ROS, suppresses Th17 (pro-inflammatory)',
            'GLP-1 RA': 'Anti-inflammatory, may slow progression',
        },
        'reversibility': 'Early intervention may reverse; late stages: permanent'
    }
}

GAPS = {
    1: 'Gene Therapy for LADA',
    2: 'Health Equity in Beta Cell Therapies',
    3: 'Insulin Resistance in Islet Transplant',
    4: 'Drug Repurposing for Islet Transplant',
    5: 'Treg in Diabetic Neuropathy',
    6: 'CAR-T Access Barriers in Diabetes',
    7: 'GKA Drug Repurposing Landscape',
    8: 'Immunomodulatory Drugs for LADA',
    9: 'Glucokinase Activators in LADA (Under Review)',
    10: 'LADA Prevalence by Healthcare Setting',
    11: 'Islet Transplant Registry Equity Analysis',
    12: 'Generic Drug x Diabetes Mechanism Catalog',
    13: 'Personalized Nutrition for Beta Cell Health',
    14: 'Personalized Nutrition Strategy for LADA',
    15: 'GKA Pricing Trajectory Model',
}

def generate_html():
    """Generate comprehensive HTML dashboard"""
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical Data Dictionary - Diabetes Research Hub</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #fafaf7;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { font-family: Georgia, serif; font-size: 2.5em; margin-bottom: 10px; color: #222; }
        h2 { font-family: Georgia, serif; font-size: 1.8em; margin: 30px 0 15px 0; color: #333; }
        h3 { font-family: Georgia, serif; font-size: 1.3em; margin: 20px 0 10px 0; color: #444; }
        .description { font-size: 0.95em; color: #666; margin-bottom: 20px; }
        .tabs {
            display: flex;
            gap: 10px;
            margin: 20px 0;
            border-bottom: 2px solid #ddd;
            flex-wrap: wrap;
        }
        .tab-button {
            padding: 12px 20px;
            background: none;
            border: none;
            font-size: 1em;
            cursor: pointer;
            font-family: Georgia, serif;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
        }
        .tab-button.active {
            color: #333;
            border-bottom-color: #333;
        }
        .tab-button:hover { color: #222; }
        .tab-content {
            display: none;
            animation: fadeIn 0.3s;
        }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* Body Systems Map */
        .systems-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .system-card {
            padding: 20px;
            border: 1px solid #ddd;
            cursor: pointer;
            transition: all 0.2s;
        }
        .system-card:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .system-name {
            font-family: Georgia, serif;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .system-desc {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
        }
        .system-terms {
            display: none;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }
        .system-terms.active { display: block; }
        .system-terms ul {
            list-style: none;
            padding-left: 0;
        }
        .system-terms li {
            font-size: 0.85em;
            color: #555;
            padding: 3px 0;
        }

        /* Dictionary */
        .search-filter {
            margin: 20px 0;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .search-box, .filter-select {
            padding: 10px;
            border: 1px solid #ddd;
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-size: 0.9em;
        }
        .search-box { flex: 1; min-width: 200px; }
        .filter-select { min-width: 150px; }

        .dictionary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .term-card {
            border: 1px solid #ddd;
            padding: 20px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .term-card.hidden { display: none; }
        .term-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .term-title {
            font-family: Georgia, serif;
            font-size: 1.1em;
            font-weight: bold;
            color: #222;
            margin-bottom: 10px;
        }
        .term-plain {
            font-size: 0.9em;
            color: #555;
            margin-bottom: 10px;
            font-style: italic;
        }
        .term-medical {
            font-size: 0.85em;
            color: #666;
            margin-bottom: 8px;
            border-left: 3px solid #d4c4b4;
            padding-left: 10px;
        }
        .term-details {
            display: none;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid #eee;
            font-size: 0.85em;
        }
        .term-details.active { display: block; }
        .detail-row {
            margin: 8px 0;
        }
        .detail-label {
            font-weight: bold;
            color: #555;
            font-family: "SF Mono", Monaco, Consolas, monospace;
        }
        .detail-value {
            color: #777;
            margin-top: 2px;
        }
        .badge {
            display: inline-block;
            background: #e8e8e8;
            padding: 3px 8px;
            margin: 3px 3px 3px 0;
            font-size: 0.75em;
            border-radius: 0;
        }

        /* Pathways */
        .pathway-item {
            margin: 30px 0;
            border: 1px solid #ddd;
            padding: 20px;
        }
        .pathway-title {
            font-family: Georgia, serif;
            font-size: 1.3em;
            margin-bottom: 10px;
            color: #222;
        }
        .pathway-diagram {
            background: #fafaf7;
            padding: 20px;
            margin: 15px 0;
            overflow-x: auto;
        }
        .flow-box {
            display: inline-block;
            background: #fff;
            border: 2px solid #999;
            padding: 12px 15px;
            margin: 10px 5px;
            min-width: 140px;
            text-align: center;
            font-size: 0.85em;
        }
        .flow-arrow {
            display: inline-block;
            margin: 0 3px;
            font-size: 1.2em;
        }
        .intervention {
            background: #fff5e6;
            border: 2px solid #cc9966;
            padding: 10px;
            margin: 10px 0;
            font-size: 0.85em;
        }

        /* Gap Connections Matrix */
        .gap-matrix {
            overflow-x: auto;
            margin: 20px 0;
        }
        .gap-matrix table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85em;
        }
        .gap-matrix th, .gap-matrix td {
            padding: 8px;
            text-align: left;
            border: 1px solid #ddd;
        }
        .gap-matrix th {
            background: #f5f5f5;
            font-weight: bold;
            font-family: "SF Mono", Monaco, Consolas, monospace;
        }
        .gap-matrix td {
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-size: 0.8em;
        }
        .gap-connected { background: #e8f4e8; }
        .gap-not-connected { background: #fff; }

        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 0.85em;
            color: #888;
            text-align: center;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Medical Data Dictionary</h1>
    <p class="description">Comprehensive reference for diabetes research terms, pathways, and connections to research gaps. All definitions in plain English first, then medical literature standard definitions.</p>

    <div class="tabs">
        <button class="tab-button active" onclick="switchTab('systems')">Body Systems Map</button>
        <button class="tab-button" onclick="switchTab('dictionary')">Term Dictionary</button>
        <button class="tab-button" onclick="switchTab('pathways')">Pathway Maps</button>
        <button class="tab-button" onclick="switchTab('gaps')">Gap Connections</button>
    </div>

'''
    return html

def generate_systems_map():
    """Generate body systems map"""
    html = '''
    <div id="systems" class="tab-content active">
        <h2>Body Systems Map</h2>
        <p class="description">Click each system to see the medical terms associated with it. These systems represent major areas affected in diabetes and relevant to the research.</p>
        <div class="systems-grid">
'''
    for sys_id, sys_info in BODY_SYSTEMS.items():
        sys_terms = [t for t, info in TERMS.items() if sys_id in info['systems']]
        html += f'''
        <div class="system-card" style="background-color: {sys_info['color']}; background-color: {sys_info['color']}cc;">
            <div class="system-name">{sys_info['name']}</div>
            <div class="system-desc">{sys_info['description']}</div>
            <button onclick="toggleSystemTerms(this)" style="padding: 8px 12px; border: none; background: rgba(0,0,0,0.1); cursor: pointer; font-size: 0.85em;">Show Terms ({len(sys_terms)})</button>
            <div class="system-terms">
                <ul>
'''
        for term in sorted(sys_terms)[:15]:
            html += f'                    <li>• {term}</li>\n'
        if len(sys_terms) > 15:
            html += f'                    <li><em>... and {len(sys_terms)-15} more</em></li>\n'
        html += '''                </ul>
            </div>
        </div>
'''
    html += '''        </div>
    </div>
'''
    return html

def generate_dictionary():
    """Generate searchable term dictionary"""
    html = '''
    <div id="dictionary" class="tab-content">
        <h2>Medical Term Dictionary</h2>
        <p class="description">Search and filter terms. Click any term to expand and see connections to body systems, gaps, and related concepts.</p>
        <div class="search-filter">
            <input type="text" class="search-box" id="searchInput" placeholder="Search terms (e.g., 'Beta Cell', 'insulin', 'T1D')..." onkeyup="filterDictionary()">
            <select class="filter-select" id="systemFilter" onchange="filterDictionary()">
                <option value="">All Systems</option>
'''
    for sys_id, sys_info in BODY_SYSTEMS.items():
        html += f'                <option value="{sys_id}">{sys_info["name"]}</option>\n'
    html += '''            </select>
            <select class="filter-select" id="gapFilter" onchange="filterDictionary()">
                <option value="">All Gaps</option>
'''
    for gap_num in range(1, 16):
        html += f'                <option value="{gap_num}">Gap {gap_num}</option>\n'
    html += '''            </select>
        </div>
        <div class="dictionary-grid" id="dictionaryGrid">
'''

    for term, info in sorted(TERMS.items()):
        systems_str = ', '.join([BODY_SYSTEMS[s]['name'] for s in info['systems']])
        gaps_str = ', '.join([f'Gap {g}' for g in sorted(info['gap_relevance'])])

        html += f'''        <div class="term-card" data-term="{term.lower()}" data-systems="{','.join(info['systems'])}" data-gaps="{','.join(map(str, info['gap_relevance']))}">
            <div class="term-title">{term}</div>
            <div class="term-plain">{info['plain']}</div>
            <div class="term-medical">{info['medical']}</div>
            <button onclick="toggleTermDetails(this)" style="padding: 6px 10px; border: none; background: #f0f0f0; cursor: pointer; font-size: 0.8em; margin-top: 8px;">Details</button>
            <div class="term-details">
                <div class="detail-row">
                    <div class="detail-label">Body System(s):</div>
                    <div class="detail-value">{systems_str}</div>
                </div>
                <div class="detail-row">
                    <div class="detail-label">Key Indicators:</div>
                    <div class="detail-value">{', '.join(info['indicators'])}</div>
                </div>
'''
        if info.get('normal_range'):
            html += f'''                <div class="detail-row">
                    <div class="detail-label">Normal Range:</div>
                    <div class="detail-value">{info['normal_range']}</div>
                </div>
'''
        if info.get('disease'):
            html += f'''                <div class="detail-row">
                    <div class="detail-label">In Diabetes:</div>
                    <div class="detail-value">{info['disease']}</div>
                </div>
'''
        if info.get('connections'):
            html += f'''                <div class="detail-row">
                    <div class="detail-label">Connected To:</div>
                    <div class="detail-value">{', '.join(info['connections'][:5])}
'''
            if len(info['connections']) > 5:
                html += f' +{len(info["connections"])-5} more'
            html += '</div></div>\n'

        html += f'''                <div class="detail-row">
                    <div class="detail-label">Gap Relevance:</div>
                    <div class="detail-value">{gaps_str}</div>
                </div>
                <div class="detail-row">
                    <div class="detail-label">Source:</div>
                    <div class="detail-value">{info['source']}</div>
                </div>
            </div>
        </div>
'''

    html += '''        </div>
    </div>
'''
    return html

def generate_pathways():
    """Generate pathway diagrams"""
    html = '''
    <div id="pathways" class="tab-content">
        <h2>Biological Pathways</h2>
        <p class="description">Visual representation of key biological pathways in diabetes. Each shows normal function and intervention points.</p>
'''

    for pathway_name, pathway_info in PATHWAYS.items():
        html += f'''
        <div class="pathway-item">
            <div class="pathway-title">{pathway_name}</div>
            <p style="color: #666; margin-bottom: 15px;">{pathway_info['description']}</p>
            <div class="pathway-diagram">
                <strong>Pathway Sequence:</strong><br><br>
'''
        for i, step in enumerate(pathway_info['steps']):
            html += f'''                <div style="display: inline-block; margin: 5px;">
                    <div class="flow-box">
                        <strong>{step['stage']}</strong><br>
                        {step['element']}
                    </div>
'''
            if i < len(pathway_info['steps']) - 1:
                html += '                    <div class="flow-arrow">→</div>\n'
            html += '                </div>\n'

        html += '''            </div>
            <div style="margin-top: 15px;">
                <strong>Intervention Points:</strong>
'''
        if pathway_info.get('intervention_points'):
            for intervention, description in pathway_info['intervention_points'].items():
                html += f'''                <div class="intervention">
                    <strong>{intervention}:</strong> {description}
                </div>
'''

        if pathway_info.get('intervention_strategies'):
            html += '''                <strong>Therapeutic Strategies:</strong><br>
'''
            for strategy, description in pathway_info['intervention_strategies'].items():
                html += f'''                <div class="intervention">
                    <strong>{strategy}:</strong> {description}
                </div>
'''

        if pathway_info.get('breakdown'):
            html += f'''                <div class="intervention" style="border-color: #cc6666; background: #ffe6e6;">
                    <strong>Where It Breaks Down:</strong> {pathway_info['breakdown']}
                </div>
'''
        if pathway_info.get('impairment'):
            html += f'''                <div class="intervention" style="border-color: #cc6666; background: #ffe6e6;">
                    <strong>Disease Impairment:</strong> {pathway_info['impairment']}
                </div>
'''
        if pathway_info.get('intervention_by_treg'):
            html += f'''                <div class="intervention" style="border-color: #66cc66; background: #e6ffe6;">
                    <strong>Therapeutic Intervention (Treg):</strong> {pathway_info['intervention_by_treg']}
                </div>
'''
        if pathway_info.get('reversibility'):
            html += f'''                <div class="intervention" style="border-color: #6666cc; background: #e6e6ff;">
                    <strong>Reversibility:</strong> {pathway_info['reversibility']}
                </div>
'''
        if pathway_info.get('gap_challenge'):
            html += f'''                <div class="intervention" style="border-color: #cc9933; background: #fff5e6;">
                    <strong>Research Challenge:</strong> {pathway_info['gap_challenge']}
                </div>
'''

        html += '''            </div>
        </div>
'''

    html += '''    </div>
'''
    return html

def generate_gaps_connections():
    """Generate gap-to-term connection matrix"""
    html = '''
    <div id="gaps" class="tab-content">
        <h2>Gap Relevance Matrix</h2>
        <p class="description">Shows which terms/concepts are relevant to each of the 15 research gaps. Understanding these connections reveals how mastering the biology helps solve the gaps.</p>
'''

    for gap_num, gap_desc in sorted(GAPS.items()):
        relevant_terms = [t for t, info in TERMS.items() if gap_num in info['gap_relevance']]
        html += f'''
        <div style="margin: 25px 0; padding: 15px; border-left: 4px solid #999; background: #fafaf7;">
            <h3 style="margin: 0 0 10px 0;">Gap {gap_num}: {gap_desc}</h3>
            <p style="color: #666; font-size: 0.9em; margin-bottom: 10px;"><strong>{len(relevant_terms)} relevant terms/concepts</strong></p>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
'''
        for term in sorted(relevant_terms)[:20]:
            html += f'                <span class="badge">{term}</span>\n'
        if len(relevant_terms) > 20:
            html += f'                <span class="badge">+{len(relevant_terms)-20} more</span>\n'
        html += '''            </div>
        </div>
'''

    html += '''    </div>
'''
    return html

def generate_javascript():
    """Generate JavaScript for interactivity"""
    js = '''
    <script>
        function switchTab(tabName) {
            var tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(function(tab) { tab.classList.remove('active'); });
            document.getElementById(tabName).classList.add('active');

            var buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(function(btn) { btn.classList.remove('active'); });
            event.target.classList.add('active');
        }

        function toggleSystemTerms(button) {
            var terms = button.parentElement.querySelector('.system-terms');
            terms.classList.toggle('active');
            button.textContent = terms.classList.contains('active') ? 'Hide Terms' : 'Show Terms';
            event.stopPropagation();
        }

        function toggleTermDetails(button) {
            var details = button.parentElement.querySelector('.term-details');
            details.classList.toggle('active');
            button.textContent = details.classList.contains('active') ? 'Hide Details' : 'Show Details';
            event.stopPropagation();
        }

        function filterDictionary() {
            var searchTerm = document.getElementById('searchInput').value.toLowerCase();
            var systemFilter = document.getElementById('systemFilter').value;
            var gapFilter = document.getElementById('gapFilter').value;

            var cards = document.querySelectorAll('.term-card');
            cards.forEach(function(card) {
                var term = card.getAttribute('data-term');
                var systems = card.getAttribute('data-systems').split(',');
                var gaps = card.getAttribute('data-gaps').split(',').filter(function(g) { return g !== ''; });

                var matchesSearch = searchTerm === '' || term.includes(searchTerm);
                var matchesSystem = systemFilter === '' || systems.includes(systemFilter);
                var matchesGap = gapFilter === '' || gaps.includes(gapFilter);

                card.classList.toggle('hidden', !(matchesSearch && matchesSystem && matchesGap));
            });
        }

        document.addEventListener('DOMContentLoaded', function() {
            var inputs = document.querySelectorAll('.search-box, .filter-select');
            inputs.forEach(function(input) {
                input.addEventListener('change', filterDictionary);
            });
        });
    </script>
'''
    return js

def main():
    output_file = get_paths()

    html_parts = [
        generate_html(),
        generate_systems_map(),
        generate_dictionary(),
        generate_pathways(),
        generate_gaps_connections(),
        '''        </div>
        <div class="footer">
            <p>Medical Data Dictionary for Diabetes Research Hub</p>
            <p>Last updated: 2026. Data compiled from ADA Standards of Care, Harrison\'s Principles of Internal Medicine, Robbins Pathology, and peer-reviewed literature.</p>
            <p>This is educational reference material, not medical advice. Consult healthcare providers for diagnosis and treatment decisions.</p>
        </div>
    </div>
''',
        generate_javascript(),
        '''    </body>
</html>
'''
    ]

    full_html = ''.join(html_parts)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

    file_size_kb = len(full_html.encode('utf-8')) / 1024
    print('Medical Data Dictionary generated successfully.')
    print('Output file: ' + output_file)
    print('HTML size: {:.1f} KB'.format(file_size_kb))
    print('Total terms: {}'.format(len(TERMS)))
    print('Body systems: {}'.format(len(BODY_SYSTEMS)))
    print('Pathways: {}'.format(len(PATHWAYS)))
    print('Research gaps: {}'.format(len(GAPS)))

if __name__ == '__main__':
    main()
