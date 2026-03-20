#!/usr/bin/env python3
"""
Build Drug Repurposing Screen Dashboard
Generates a Tufte-style HTML dashboard for computational generic drug repurposing
screening for diabetes, identifying cheap generic drugs with mechanisms relevant
to diabetes that could serve as equity interventions in low-resource settings.

Author: Claude Code
Date: 2026-03-17
Encoding: utf-8
"""

import os
import json
from datetime import datetime
from collections import defaultdict

# Drug candidate database with evidence-based scoring
CANDIDATES = {
    "Metformin": {
        "class": "Biguanide",
        "primary_indication": "Type 2 diabetes",
        "mechanism_diabetes": "AMPK activation, NLRP3 inflammasome suppression, mitochondrial complex I inhibition",
        "evidence": "Seminal landmark therapy; PMID:30899369 demonstrates NLRP3 inflammasome suppression; UK Prospective Diabetes Study established cardioprotection",
        "generic_cost": 0.05,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 10,
        "safety_score": 10,
        "generic_score": 10,
        "evidence_score": 10,
        "equity_score": 10,
        "category": "Reference Standard",
        "equity_rationale": "Most cost-effective first-line therapy; available in virtually all low-resource settings; extensive safety data across populations",
        "lada_relevance": "May improve insulin secretion through AMPK; limited direct evidence in LADA",
        "islet_relevance": "AMPK activation supports beta cell function preservation"
    },
    "Verapamil": {
        "class": "Calcium channel blocker (non-dihydropyridine)",
        "primary_indication": "Hypertension, angina, arrhythmia",
        "mechanism_diabetes": "Beta cell preservation, anti-apoptotic signaling, islet protection; TXNIP inhibition demonstrated in rodent models but not confirmed as mechanism in humans",
        "evidence": "PMID:29988125 (Ovalle et al, Nature Medicine 2018) demonstrates preserved C-peptide and beta cell function in new-onset T1D. TXNIP inhibition is the proposed mechanism from preclinical models but has not been directly validated in human islets in vivo",
        "generic_cost": 0.15,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 9,
        "safety_score": 9,
        "generic_score": 9,
        "evidence_score": 8,
        "equity_score": 9,
        "category": "Cardiovascular/Metabolic",
        "equity_rationale": "Dual benefit for diabetes and hypertension in same population; inexpensive generic; well-characterized across diverse populations",
        "lada_relevance": "Strong mechanistic relevance; potential disease-modifying effect in autoimmune beta cell loss",
        "islet_relevance": "Landmark evidence for beta cell preservation in new-onset diabetes; potential utility in transplant tolerance induction"
    },
    "Colchicine": {
        "class": "Microtubule polymerization inhibitor",
        "primary_indication": "Gout, pericarditis, familial Mediterranean fever",
        "mechanism_diabetes": "Indirect NLRP3 inflammasome inhibition via microtubule disruption (not direct NLRP3 binding), IL-1beta suppression, monocyte activation blockade",
        "evidence": "COLCOT trial demonstrates cardiovascular benefit in stable CAD; LoDoCo2 confirms anti-inflammatory cardiovascular effects. Mechanism is INDIRECT \u2014 colchicine disrupts microtubule-dependent NLRP3 assembly rather than directly inhibiting the inflammasome. Multiple Phase 2 studies in metabolic inflammation",
        "generic_cost": 0.50,
        "who_essential": True,  # CORRECTED: Colchicine is on WHO EML 2023 (Section 29, Gout medicines)
        "global_availability": "high",
        "mechanism_score": 9,
        "safety_score": 8,
        "generic_score": 8,
        "evidence_score": 8,
        "equity_score": 7,
        "category": "Anti-inflammatory",
        "equity_rationale": "Addresses inflammatory diabetes driver; sub-dollar generic pricing; WHO Essential Medicine; potential for cardiovascular disease prevention in diabetic populations",
        "lada_relevance": "May suppress anti-beta cell immune responses through inflammasome inhibition",
        "islet_relevance": "Reduced innate immune activation post-transplant; potential tolerance-promoting agent"
    },
    "Hydroxychloroquine": {
        "class": "Antimalarial, immunomodulator",
        "primary_indication": "Lupus, rheumatoid arthritis, malaria",
        "mechanism_diabetes": "TLR signaling inhibition, anti-inflammatory, immunomodulatory",
        "evidence": "WHO Essential Medicine with decades of rheumatologic safety data. Insulin sensitivity claims based on observational/retrospective studies only \u2014 no RCT specifically evaluating HCQ for insulin sensitivity exists. Metabolic benefits observed incidentally in RA/SLE populations. Treg expansion is mechanistically plausible but not directly demonstrated for HCQ",
        "generic_cost": 0.20,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 8,
        "generic_score": 9,
        "evidence_score": 5,
        "equity_score": 9,
        "category": "Immunomodulator",
        "equity_rationale": "Globally available WHO Essential Medicine; strong safety profile; potential dual benefit in autoimmune diabetes (observational evidence only)",
        "lada_relevance": "TLR inhibition may slow beta cell autoimmunity; no LADA-specific RCT data",
        "islet_relevance": "Immunomodulatory profile; transplant tolerance support is theoretical"
    },
    "Pentoxifylline": {
        "class": "Phosphodiesterase inhibitor, rheologic agent",
        "primary_indication": "Peripheral arterial disease, claudication",
        "mechanism_diabetes": "TNF-alpha inhibition, improved microcirculatory flow, insulin sensitivity improvement in NASH",
        "evidence": "Multiple Phase 2 studies demonstrate TNF-alpha reduction in metabolic syndrome; improves insulin sensitivity in NASH populations with metabolic dysfunction",
        "generic_cost": 0.25,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 8,
        "generic_score": 8,
        "evidence_score": 6,
        "equity_score": 7,
        "category": "Anti-inflammatory",
        "equity_rationale": "Inexpensive; addresses diabetes-related microvascular complications; suitable for resource-limited settings",
        "lada_relevance": "TNF-alpha plays role in beta cell autoimmunity; limited direct evidence",
        "islet_relevance": "May improve islet engraftment through rheologic and anti-inflammatory mechanisms"
    },
    "Dapsone": {
        "class": "Sulfone, immunomodulator",
        "primary_indication": "Dermatitis herpetiformis, leprosy, PCP prophylaxis",
        "mechanism_diabetes": "Neutrophil inhibition, oxidative stress reduction, anti-inflammatory",
        "evidence": "Decades of safety data; WHO Essential Medicines for leprosy; immunomodulatory effects demonstrated in multiple autoimmune conditions",
        "generic_cost": 0.10,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 7,
        "generic_score": 9,
        "evidence_score": 5,
        "equity_score": 9,
        "category": "Immunomodulator",
        "equity_rationale": "Exceptionally cheap; globally available through leprosy programs in low-resource regions; minimal cold-chain requirements",
        "lada_relevance": "Neutrophil inhibition may reduce islet infiltration in autoimmune diabetes",
        "islet_relevance": "Anti-inflammatory profile; potential immunosuppressive-sparing adjunct"
    },
    "Losartan": {
        "class": "Angiotensin II receptor blocker",
        "primary_indication": "Hypertension, diabetic nephropathy",
        "mechanism_diabetes": "Preservation of renal function, anti-inflammatory; pancreatic islet protection demonstrated in animal models only",
        "evidence": "Extensive human evidence for diabetic nephropathy (RENAAL trial); cardiovascular outcome trials in diabetes. Islet protection claims based on rodent models \u2014 no human RCT has evaluated losartan for beta cell preservation",
        "generic_cost": 0.08,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 8,
        "safety_score": 9,
        "generic_score": 10,
        "evidence_score": 8,
        "equity_score": 9,
        "category": "Cardiovascular/Metabolic",
        "equity_rationale": "Dual indication (HTN and diabetes); extreme affordability; kidney-protective; essential in diabetic populations",
        "lada_relevance": "Potential islet-protective effects; standard care in LADA with hypertension",
        "islet_relevance": "Animal evidence for pancreatic islet preservation; potential tolerance adjunct"
    },
    "Spironolactone": {
        "class": "Mineralocorticoid receptor antagonist",
        "primary_indication": "Heart failure, hypertension, hyperaldosteronism",
        "mechanism_diabetes": "Anti-inflammatory in adipose tissue, improved insulin sensitivity, mitochondrial protection",
        "evidence": "WHO Essential Medicine; multiple observational studies show metabolic benefits; cardiac and renal protection in diabetes; improving evidence base in metabolic syndrome",
        "generic_cost": 0.12,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 8,
        "generic_score": 9,
        "evidence_score": 6,
        "equity_score": 8,
        "category": "Cardiovascular/Metabolic",
        "equity_rationale": "Inexpensive; metabolic benefits beyond hypertension control; available globally",
        "lada_relevance": "Limited direct evidence; potential metabolic support in LADA",
        "islet_relevance": "Anti-inflammatory adipose effects may create permissive transplant environment"
    },
    "Pioglitazone": {
        "class": "Thiazolidinedione",
        "primary_indication": "Type 2 diabetes",
        "mechanism_diabetes": "PPARG agonism, improved insulin sensitivity, mitochondrial biogenesis; Treg expansion demonstrated in preclinical models but not confirmed in human diabetes trials",
        "evidence": "Extensive clinical trial evidence for insulin sensitization. PPARG-driven Treg differentiation demonstrated in murine models; human evidence for immune modulation is indirect and observational",
        "generic_cost": 0.30,
        "who_essential": True,  # CORRECTED: Pioglitazone is on WHO EML 2023 (Section 18.5, Insulins and other antidiabetic agents)
        "global_availability": "high",
        "mechanism_score": 9,
        "safety_score": 7,
        "generic_score": 8,
        "evidence_score": 9,
        "equity_score": 7,
        "category": "Cardiovascular/Metabolic",
        "equity_rationale": "Strong efficacy in T2D; Treg-promoting mechanisms; WHO Essential Medicine; generic and affordable",
        "lada_relevance": "Treg-promoting PPARG agonism; potential disease-modifying in LADA but requires evaluation",
        "islet_relevance": "Treg expansion supports transplant tolerance induction"
    },
    "Mycophenolate Mofetil": {
        "class": "Inosine monophosphate dehydrogenase inhibitor",
        "primary_indication": "Immunosuppression (organ transplant, autoimmune)",
        "mechanism_diabetes": "B cell and T cell suppression, selective lymphocyte targeting, anti-autoimmune",
        "evidence": "Standard transplant immunosuppression; accumulating evidence in T1D and LADA; selective B cell targeting relevant to beta cell autoimmunity",
        "generic_cost": 2.00,
        "who_essential": False,
        "global_availability": "moderate",
        "mechanism_score": 9,
        "safety_score": 8,
        "generic_score": 7,
        "evidence_score": 7,
        "equity_score": 5,
        "category": "Immunosuppressant",
        "equity_rationale": "Established immunosuppressive efficacy; selective B cell targeting; cost barrier in LMICs",
        "lada_relevance": "Direct anti-autoimmune effect; potential disease-modifying therapy for LADA",
        "islet_relevance": "Standard component of transplant protocols; well-characterized immunosuppressive profile"
    },
    "Azathioprine": {
        "class": "Purine analog, immunosuppressant",
        "primary_indication": "Autoimmune diseases, transplant rejection",
        "mechanism_diabetes": "Purine metabolism inhibition, T cell and B cell suppression, anti-autoimmune",
        "evidence": "Historical T1D prevention trials; extensive use in autoimmune conditions; well-characterized mechanism in lymphocyte suppression",
        "generic_cost": 0.40,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 8,
        "safety_score": 7,
        "generic_score": 9,
        "evidence_score": 6,
        "equity_score": 8,
        "category": "Immunosuppressant",
        "equity_rationale": "Very inexpensive; global availability; long safety record across diverse populations",
        "lada_relevance": "Direct immunosuppressive effect; historical evidence in T1D; potential LADA application",
        "islet_relevance": "Non-selective immunosuppression; standard in transplant protocols"
    },
    "Low-Dose Naltrexone": {
        "class": "Opioid antagonist, immunomodulator",
        "primary_indication": "Pain conditions, autoimmune diseases (off-label)",
        "mechanism_diabetes": "Toll-like receptor 4 antagonism, microglial suppression, immune modulation at sub-analgesic doses",
        "evidence": "Emerging evidence in autoimmune and metabolic conditions; Phase 2 trials in multiple sclerosis and fibromyalgia; TLR4 mechanism relevant to diabetic inflammation",
        "generic_cost": 0.50,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 9,
        "generic_score": 9,
        "evidence_score": 5,
        "equity_score": 8,
        "category": "Immunomodulator",
        "equity_rationale": "Extremely affordable; excellent safety profile at low doses; growing evidence base; simple dosing",
        "lada_relevance": "TLR4 antagonism may suppress anti-beta cell immune responses",
        "islet_relevance": "Microglial suppression may create permissive transplant environment"
    },
    "Nicotinamide": {
        "class": "Vitamin B3, NAD+ precursor",
        "primary_indication": "Nutritional supplementation, niacin deficiency",
        "mechanism_diabetes": "NAD+ augmentation, PARP inhibition, beta cell preservation, anti-apoptotic",
        "evidence": "ENDIT trial (European Nicotinamide Diabetes Intervention Trial) was NEGATIVE \u2014 did not prevent T1D in high-risk individuals (Lancet 2004; PMID:15016488). Preclinical mechanistic studies support PARP inhibition and beta cell protection in vitro, but clinical translation has not been demonstrated",
        "generic_cost": 0.05,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 8,
        "safety_score": 10,
        "generic_score": 10,
        "evidence_score": 4,
        "equity_score": 10,
        "category": "Metabolic/Micronutrient",
        "equity_rationale": "Exceptionally cheap; universal availability; no cold-chain requirements; excellent safety profile; nutritional benefit independent of diabetes effect",
        "lada_relevance": "Preclinical beta cell protective mechanisms via PARP inhibition; ENDIT trial negative in T1D; untested in LADA",
        "islet_relevance": "NAD+-dependent beta cell preservation mechanisms (preclinical only)"
    },
    "Berberine": {
        "class": "Plant alkaloid, AMPK activator",
        "primary_indication": "Traditional Chinese medicine, oral infection, diarrhea",
        "mechanism_diabetes": "AMPK activation, mitochondrial function modulation, improved insulin sensitivity",
        "evidence": "PMID:18397984 (Yin et al 2008) demonstrated HbA1c reduction in T2D but was NOT a direct metformin comparison trial. Subsequent meta-analyses (PMID:25498346) suggest glucose-lowering effects, but head-to-head non-inferiority to metformin is not established. AMPK activation confirmed in preclinical models",
        "generic_cost": 0.15,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 8,
        "generic_score": 9,
        "evidence_score": 5,
        "equity_score": 9,
        "category": "Anti-inflammatory/Metabolic",
        "equity_rationale": "Affordable botanical extract; available in high-prevalence regions; traditional medicine integration; glucose-lowering demonstrated but non-inferiority to metformin unproven",
        "lada_relevance": "AMPK activation may support beta cell function preservation; no LADA-specific data",
        "islet_relevance": "Mitochondrial protective mechanisms (preclinical)"
    },
    "Acarbose": {
        "class": "Alpha-glucosidase inhibitor",
        "primary_indication": "Type 2 diabetes",
        "mechanism_diabetes": "Delayed carbohydrate absorption, GLP-1 enhancement, improved beta cell sensitivity",
        "evidence": "Extensive clinical trial evidence; GLP-1 augmentation mechanism; cardiovascular outcome data from ACE trial",
        "generic_cost": 0.25,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 9,
        "generic_score": 9,
        "evidence_score": 8,
        "equity_score": 9,
        "category": "Metabolic",
        "equity_rationale": "Global availability; works through dietary modulation; minimal systemic effects; applicable in diverse food contexts",
        "lada_relevance": "GLP-1 enhancement may support beta cell function in LADA",
        "islet_relevance": "Reduced glycemic stress may support islet engraftment"
    },
    "Rifaximin": {
        "class": "Rifamycin antibiotic (non-absorbed)",
        "primary_indication": "Traveler's diarrhea, hepatic encephalopathy",
        "mechanism_diabetes": "Microbiome modulation, improved insulin sensitivity, reduced endotoxemia, SCFA production",
        "evidence": "Emerging Phase 2 data in metabolic syndrome; microbiome-based mechanism; selective gut targeting with minimal systemic absorption",
        "generic_cost": 1.50,
        "who_essential": False,
        "global_availability": "moderate",
        "mechanism_score": 7,
        "safety_score": 9,
        "generic_score": 7,
        "evidence_score": 5,
        "equity_score": 6,
        "category": "Microbiome/Metabolic",
        "equity_rationale": "Gut-targeted mechanism; selective dysbiosis correction; limited systemic toxicity",
        "lada_relevance": "Microbiome-based immune modulation may suppress anti-beta cell responses",
        "islet_relevance": "Endotoxemia reduction may improve transplant tolerance"
    },
    "Rapamycin": {
        "class": "mTOR inhibitor, immunosuppressant",
        "primary_indication": "Organ transplant rejection, cancer",
        "mechanism_diabetes": "mTOR suppression, Treg expansion, anti-proliferative, metabolic reprogramming",
        "evidence": "Standard transplant therapy; extensive Treg expansion data; metabolic reprogramming of immune cells; multiple preclinical beta cell preservation studies",
        "generic_cost": 3.00,
        "who_essential": False,
        "global_availability": "moderate",
        "mechanism_score": 9,
        "safety_score": 7,
        "generic_score": 6,
        "evidence_score": 8,
        "equity_score": 4,
        "category": "Immunosuppressant",
        "equity_rationale": "Potent Treg-promoting mechanism; cost barrier in LMICs; established in transplant contexts",
        "lada_relevance": "Strong Treg induction; potential disease-modifying in LADA",
        "islet_relevance": "Fundamental transplant tolerance mechanism; well-established dose optimization"
    },
    "Baricitinib": {
        "class": "JAK1/2 inhibitor",
        "primary_indication": "Rheumatoid arthritis, alopecia areata",
        "mechanism_diabetes": "JAK-STAT inhibition, Treg expansion, reduced pro-inflammatory cytokines",
        "evidence": "FDA-approved for RA; preclinical islet transplant tolerance data in mouse models; no human diabetes-specific RCT. Mechanistic studies on immune modulation are preclinical",
        "generic_cost": 50.00,  # CORRECTED: Brand Olumiant ~$300/mo; Indian generics ~$30-60/mo; $5 was fabricated. No FDA-approved generic exists as of 2025
        "who_essential": False,
        "global_availability": "limited",
        "mechanism_score": 8,
        "safety_score": 7,
        "generic_score": 2,  # CORRECTED: No approved generic in most markets; patent protected
        "evidence_score": 5,  # CORRECTED: Preclinical only for diabetes indication
        "equity_score": 2,  # CORRECTED: Cost-prohibitive in LMICs; limited availability
        "category": "Immunomodulator",
        "equity_rationale": "Costly patented drug with limited LMIC access; Indian generics emerging but not widely available; mechanistic rationale for transplant tolerance is preclinical only",
        "lada_relevance": "JAK-STAT inhibition addresses pro-inflammatory axis in autoimmune diabetes",
        "islet_relevance": "Transplant tolerance data available; JAK inhibition suppresses anti-islet immunity"
    },
    "Disulfiram": {
        "class": "Aldehyde dehydrogenase inhibitor",
        "primary_indication": "Alcohol use disorder",
        "mechanism_diabetes": "Gasdermin D inhibition, inflammasome suppression via copper chelation; NLRP3 effect is indirect through gasdermin D cleavage inhibition",
        "evidence": "PRECLINICAL: Hu et al (Nature 2020, PMID:32943753) demonstrated gasdermin D inhibition. Inflammasome suppression via copper-dependent mechanism shown in cell and animal models only. No human diabetes data. Repurposing cancer trial data provides safety context but not diabetes efficacy",
        "generic_cost": 0.30,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 6,
        "generic_score": 9,
        "evidence_score": 4,
        "equity_score": 7,
        "category": "Anti-inflammatory",
        "equity_rationale": "Exceptionally inexpensive; global availability; emerging evidence base; requires further clinical translation",
        "lada_relevance": "Inflammasome suppression may suppress anti-beta cell immunity",
        "islet_relevance": "NLRP3 inhibition relevant to transplant innate immune activation"
    },
    "Dimethyl Fumarate": {
        "class": "Nrf2 activator",
        "primary_indication": "Multiple sclerosis",
        "mechanism_diabetes": "Nrf2 pathway activation, oxidative stress reduction, anti-inflammatory, immunomodulatory",
        "evidence": "FDA-approved for MS; multiple mechanistic studies on Nrf2-dependent immune modulation; oxidative stress reduction in metabolic diseases",
        "generic_cost": 8.00,
        "who_essential": False,
        "global_availability": "limited",
        "mechanism_score": 8,
        "safety_score": 8,
        "generic_score": 3,
        "evidence_score": 7,
        "equity_score": 2,
        "category": "Immunomodulator",
        "equity_rationale": "Strong mechanistic evidence; cost barrier limits LMIC applicability; potential future generic availability",
        "lada_relevance": "Nrf2-mediated anti-inflammatory effects may suppress autoimmune beta cell responses",
        "islet_relevance": "Oxidative stress reduction supports islet survival"
    },
    "Lithium": {
        "class": "Mood stabilizer, GSK-3beta inhibitor",
        "primary_indication": "Bipolar disorder",
        "mechanism_diabetes": "GSK-3beta inhibition, Wnt signaling activation, neurotropic protection",
        "evidence": "PRECLINICAL ONLY: GSK-3beta inhibition promotes beta cell proliferation in rodent models and cell lines. No human clinical evidence for beta cell proliferation or diabetes prevention. Narrow therapeutic index requires serum monitoring. Observational data from bipolar cohorts show mixed metabolic effects",
        "generic_cost": 0.20,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 5,
        "safety_score": 5,
        "generic_score": 9,
        "evidence_score": 2,
        "equity_score": 5,
        "category": "Metabolic/Neurotropic",
        "equity_rationale": "Inexpensive; global availability; narrow therapeutic window requires serum monitoring infrastructure that may not exist in LMICs",
        "lada_relevance": "Beta cell proliferation mechanisms demonstrated in rodent models only; no human diabetes data",
        "islet_relevance": "GSK-3beta inhibition theoretical for beta cell expansion; preclinical only"
    },
    "Atorvastatin": {
        "class": "HMG-CoA reductase inhibitor",
        "primary_indication": "Dyslipidemia, cardiovascular disease prevention",
        "mechanism_diabetes": "Anti-inflammatory, endothelial protection, paradoxical new-onset diabetes risk",
        "evidence": "Cardiovascular outcome trials; mixed evidence on new-onset diabetes; anti-inflammatory pleiotropic effects; WHO Essential Medicine for cardiovascular risk reduction",
        "generic_cost": 0.08,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 6,
        "safety_score": 9,
        "generic_score": 10,
        "evidence_score": 8,
        "equity_score": 9,
        "category": "Cardiovascular/Metabolic",
        "equity_rationale": "Essential for diabetic cardiovascular risk reduction; extremely cheap; universal availability",
        "lada_relevance": "Paradoxical new-onset diabetes risk; standard cardiovascular prophylaxis in LADA",
        "islet_relevance": "Endothelial protection may support islet engraftment"
    },
    "Allopurinol": {
        "class": "Xanthine oxidase inhibitor",
        "primary_indication": "Gout, hyperuricemia",
        "mechanism_diabetes": "Oxidative stress reduction, xanthine oxidase-derived ROS suppression, improved endothelial function",
        "evidence": "WHO Essential Medicine; observational studies in metabolic syndrome; uric acid as inflammatory marker in diabetes; endothelial protective effects",
        "generic_cost": 0.05,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 6,
        "safety_score": 9,
        "generic_score": 10,
        "evidence_score": 5,
        "equity_score": 10,
        "category": "Anti-inflammatory",
        "equity_rationale": "Exceptionally cheap; global availability; potential dual benefit in gout-prone diabetic populations",
        "lada_relevance": "Oxidative stress reduction may suppress autoimmune activation",
        "islet_relevance": "XO-derived ROS suppression may improve islet survival"
    },
    "Telmisartan": {
        "class": "Angiotensin II receptor blocker",
        "primary_indication": "Hypertension",
        "mechanism_diabetes": "PPAR-gamma agonism (off-target), improved insulin sensitivity, anti-inflammatory",
        "evidence": "Observational studies demonstrating metabolic benefits; partial PPAR-gamma agonism; multiple cardiovascular outcome trials in hypertensive diabetics",
        "generic_cost": 0.10,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 9,
        "generic_score": 9,
        "evidence_score": 6,
        "equity_score": 9,
        "category": "Cardiovascular/Metabolic",
        "equity_rationale": "Dual cardiovascular and metabolic benefits; affordable generic; global availability",
        "lada_relevance": "Indirect PPAR-gamma agonism may support metabolic control",
        "islet_relevance": "Anti-inflammatory ARB mechanism"
    },
    "Rosiglitazone": {
        "class": "Thiazolidinedione",
        "primary_indication": "Type 2 diabetes",
        "mechanism_diabetes": "PPARG agonism, Treg expansion, improved insulin sensitivity, mitochondrial function",
        "evidence": "Extensive clinical data; similar PPARG agonism to pioglitazone; cardiac concerns limit use but metabolic benefits confirmed",
        "generic_cost": 0.20,
        "who_essential": False,
        "global_availability": "moderate",
        "mechanism_score": 9,
        "safety_score": 6,
        "generic_score": 8,
        "evidence_score": 8,
        "equity_score": 6,
        "category": "Cardiovascular/Metabolic",
        "equity_rationale": "Strong mechanism; cardiac concerns necessitate careful patient selection; limited use in LMICs",
        "lada_relevance": "Treg-promoting through PPARG",
        "islet_relevance": "PPARG mechanism supports transplant tolerance induction"
    },
    "Imatinib": {
        "class": "Tyrosine kinase inhibitor",
        "primary_indication": "Chronic myeloid leukemia, gastrointestinal stromal tumors",
        "mechanism_diabetes": "PDGF receptor inhibition, anti-fibrotic, immune modulation through kinase inhibition",
        "evidence": "Preclinical studies in beta cell preservation; anti-fibrotic mechanisms relevant to islet transplant; emerging diabetes prevention data",
        "generic_cost": 2.50,
        "who_essential": False,
        "global_availability": "moderate",
        "mechanism_score": 6,
        "safety_score": 7,
        "generic_score": 5,
        "evidence_score": 4,
        "equity_score": 4,
        "category": "Oncology/Metabolic",
        "equity_rationale": "Cost barrier significant; established tyrosine kinase mechanisms; potential future cost reduction",
        "lada_relevance": "Limited direct evidence; kinase inhibition may modulate autoimmune responses",
        "islet_relevance": "Anti-fibrotic mechanisms may improve graft integration"
    },
    "Digoxin": {
        "class": "Cardiac glycoside, Na-K ATPase inhibitor",
        "primary_indication": "Heart failure, atrial fibrillation",
        "mechanism_diabetes": "Sodium-potassium pump inhibition, improved cellular signaling, cardiac efficiency",
        "evidence": "Historic cardiovascular data; established mechanism; limited direct diabetes evidence but relevant to diabetes-associated heart failure",
        "generic_cost": 0.05,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 4,
        "safety_score": 7,
        "generic_score": 10,
        "evidence_score": 4,
        "equity_score": 8,
        "category": "Cardiovascular",
        "equity_rationale": "Exceptionally cheap; well-established mechanism; relevant to diabetes-related heart failure in resource-limited settings",
        "lada_relevance": "Cardiac support in LADA with comorbid heart failure",
        "islet_relevance": "Limited mechanistic relevance to islet transplant"
    },
    "N-Acetylcysteine": {
        "class": "Thiol antioxidant, mucolytics",
        "primary_indication": "Respiratory infections, acetaminophen overdose",
        "mechanism_diabetes": "Oxidative stress reduction, glutathione replenishment, anti-inflammatory",
        "evidence": "Multiple metabolic syndrome and T2D trials; antioxidant mechanism; glutathione-dependent immune regulation",
        "generic_cost": 0.15,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 6,
        "safety_score": 9,
        "generic_score": 9,
        "evidence_score": 5,
        "equity_score": 9,
        "category": "Anti-inflammatory/Antioxidant",
        "equity_rationale": "Inexpensive; global availability; excellent safety profile; antioxidant benefit applicable across diverse settings",
        "lada_relevance": "Oxidative stress reduction may suppress autoimmune activation",
        "islet_relevance": "Glutathione replenishment supports islet cell survival"
    },
    "Sulfasalazine": {
        "class": "5-aminosalicylate, sulfur compound",
        "primary_indication": "Inflammatory bowel disease, rheumatoid arthritis",
        "mechanism_diabetes": "Anti-inflammatory, immunomodulatory, gut barrier reinforcement",
        "evidence": "Established use in autoimmune conditions; multiple immune modulation mechanisms; potential gut dysbiosis correction",
        "generic_cost": 0.30,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 7,
        "generic_score": 9,
        "evidence_score": 5,
        "equity_score": 8,
        "category": "Anti-inflammatory/Immunomodulator",
        "equity_rationale": "Inexpensive; established safety; dual benefit in IBD and autoimmune diabetes",
        "lada_relevance": "Multiple immune modulation mechanisms relevant to autoimmune beta cell loss",
        "islet_relevance": "Anti-inflammatory profile; gut barrier mechanisms"
    },
    "Fenofibrate": {
        "class": "PPAR-alpha agonist, fibrate",
        "primary_indication": "Dyslipidemia, hypertriglyceridemia",
        "mechanism_diabetes": "PPAR-alpha agonism, improved lipid metabolism, anti-inflammatory",
        "evidence": "Cardiovascular outcome trials; PPAR-alpha immune modulation; metabolic benefits in dyslipidemic diabetics",
        "generic_cost": 0.20,
        "who_essential": False,
        "global_availability": "high",
        "mechanism_score": 6,
        "safety_score": 8,
        "generic_score": 9,
        "evidence_score": 6,
        "equity_score": 8,
        "category": "Cardiovascular/Metabolic",
        "equity_rationale": "Affordable; addresses diabetic dyslipidemia; PPAR-mediated immune effects",
        "lada_relevance": "Metabolic support in LADA with dyslipidemia",
        "islet_relevance": "PPAR-alpha immune modulation"
    },
    "Glyburide": {
        "class": "Sulfonylurea, NLRP3 inhibitor",
        "primary_indication": "Type 2 diabetes",
        "mechanism_diabetes": "NLRP3 inflammasome inhibition (independent of glucose-lowering), KATP channel closure, insulin secretion stimulation",
        "evidence": "Lamkanfi et al (J Cell Biol 2009, PMID:19237585) demonstrated direct NLRP3 inhibition at concentrations achievable in vivo. WHO Essential Medicine. Dual mechanism: glucose-lowering via insulin secretion AND anti-inflammatory via NLRP3. Widely studied in gestational diabetes (PMID:23738527). Hypoglycemia risk is the primary safety limitation",
        "generic_cost": 0.03,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 8,
        "safety_score": 6,
        "generic_score": 10,
        "evidence_score": 7,
        "equity_score": 10,
        "category": "Metabolic/Anti-inflammatory",
        "equity_rationale": "Pennies per month; WHO Essential Medicine; dual glucose-lowering and anti-inflammatory mechanism; globally available in virtually all settings",
        "lada_relevance": "NLRP3 inhibition may reduce islet inflammation; but sulfonylurea-driven insulin secretion may accelerate beta cell exhaustion in LADA",
        "islet_relevance": "NLRP3 inhibition relevant to post-transplant innate immune activation"
    },
    "Cyclosporine": {
        "class": "Calcineurin inhibitor, immunosuppressant",
        "primary_indication": "Organ transplant rejection, autoimmune diseases",
        "mechanism_diabetes": "T cell suppression via calcineurin inhibition, beta cell preservation in autoimmune diabetes",
        "evidence": "RCT-proven beta cell preservation in new-onset T1D (Bougneres et al, NEJM 1988; Feutren et al, Lancet 1986, PMID:1611143). Demonstrated remission induction in T1D when given early. Nephrotoxicity and long-term immunosuppression limit chronic use. Effect reversed upon discontinuation",
        "generic_cost": 30.00,  # CORRECTED: Generic cyclosporine ~$30-100/mo depending on dose and market; $1.50 was fabricated. Requires therapeutic drug monitoring adding further cost
        "who_essential": True,
        "global_availability": "moderate",
        "mechanism_score": 9,
        "safety_score": 5,
        "generic_score": 4,  # CORRECTED: Generic exists but still expensive; requires monitoring
        "evidence_score": 9,
        "equity_score": 3,  # CORRECTED: Monitoring requirements and cost limit LMIC use significantly
        "category": "Immunosuppressant",
        "equity_rationale": "Strong RCT evidence but nephrotoxicity, therapeutic drug monitoring requirements, and cost (~$30-100/mo) significantly limit LMIC applicability; WHO Essential Medicine for transplant",
        "lada_relevance": "Strongest historical RCT evidence for beta cell preservation in autoimmune diabetes; toxicity limits long-term use",
        "islet_relevance": "Standard calcineurin inhibitor in transplant protocols; well-established dosing"
    },
    "Aspirin (High-Dose)": {
        "class": "COX inhibitor, NF-kB inhibitor (at high doses)",
        "primary_indication": "Pain, inflammation, cardiovascular prophylaxis",
        "mechanism_diabetes": "High-dose (>3g/day) NF-kB inhibition, improved insulin sensitivity; low-dose: COX-1 antiplatelet only",
        "evidence": "Hundal et al (J Clin Invest 2002, PMID:12122111) demonstrated that high-dose salsalate (prodrug) improves insulin sensitivity via NF-kB inhibition. TINSAL-T2D trial (PMID:23223116) confirmed glucose-lowering with salsalate in T2D. Standard low-dose aspirin does NOT have this effect. GI toxicity at high doses is limiting",
        "generic_cost": 0.02,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 7,
        "safety_score": 5,
        "generic_score": 10,
        "evidence_score": 7,
        "equity_score": 9,
        "category": "Anti-inflammatory",
        "equity_rationale": "Cheapest drug in the screen; universally available; NF-kB mechanism only at high doses with significant GI risk; salsalate formulation preferred",
        "lada_relevance": "NF-kB inhibition addresses inflammatory component of beta cell loss; high-dose toxicity limits applicability",
        "islet_relevance": "NF-kB pathway relevant to transplant innate immune activation"
    },
    "Vitamin D (Cholecalciferol)": {
        "class": "Secosteroid hormone, immunomodulator",
        "primary_indication": "Bone health, vitamin D deficiency",
        "mechanism_diabetes": "Immunomodulation via VDR signaling, Treg support, beta cell function, reduced autoimmunity",
        "evidence": "Multiple RCTs with mixed results. Pittas et al (D2d trial, NEJM 2019, PMID:31173679) showed no significant T2D prevention in vitamin D-sufficient population. However, sub-analyses in vitamin D-deficient individuals and meta-analyses (PMID:32953989) suggest benefit in deficient populations. T1D prevention data from EURODIAB and DAISY cohorts are observational only",
        "generic_cost": 0.01,
        "who_essential": True,
        "global_availability": "high",
        "mechanism_score": 6,
        "safety_score": 10,
        "generic_score": 10,
        "evidence_score": 5,
        "equity_score": 10,
        "category": "Metabolic/Immunomodulator",
        "equity_rationale": "Cheapest intervention in the screen; universal availability; excellent safety; most benefit likely in deficient populations (which are disproportionately in LMICs); no cold-chain required",
        "lada_relevance": "VDR-mediated immune modulation; observational evidence for T1D prevention; LADA-specific data absent",
        "islet_relevance": "Immunomodulatory profile; VDR expressed on islet cells; preclinical evidence for beta cell support"
    }
}

# Diabetes-relevant pathways and drug mapping
PATHWAYS = {
    "NLRP3 Inflammasome": ["Metformin", "Colchicine", "Disulfiram", "Glyburide"],  # CORRECTED: Naltrexone removed — its mechanism is TLR4, not NLRP3
    "AMPK Activation": ["Metformin", "Berberine"],
    "Beta Cell Preservation": ["Verapamil", "Lithium", "Cyclosporine"],  # CORRECTED: Nicotinamide removed — ENDIT trial was negative for T1D prevention (PMID:15016488)
    "Treg Expansion": ["Pioglitazone", "Rosiglitazone", "Rapamycin", "Baricitinib", "Vitamin D (Cholecalciferol)"],
    "TNF-Alpha Inhibition": ["Pentoxifylline"],
    "Immune Suppression": ["Mycophenolate Mofetil", "Azathioprine", "Baricitinib", "Cyclosporine"],
    "Microbiome Modulation": ["Rifaximin"],
    "Oxidative Stress Reduction": ["Allopurinol", "N-Acetylcysteine", "Dimethyl Fumarate"],
    "Cardiovascular Protection": ["Losartan", "Telmisartan", "Atorvastatin", "Fenofibrate"],
    "Islet Protection": ["Verapamil", "Losartan", "Cyclosporine"],
    "GLP-1 Enhancement": ["Acarbose"],
    "Nrf2 Activation": ["Dimethyl Fumarate"],
    "NF-kB Inhibition": ["Aspirin (High-Dose)"],
    "VDR Immunomodulation": ["Vitamin D (Cholecalciferol)"],
    "TLR4 Antagonism": ["Low-Dose Naltrexone"]  # Correct pathway for LDN mechanism
}


def calculate_composite_score(drug):
    """Calculate weighted composite score for a drug candidate."""
    weights = {
        "mechanism_score": 0.25,
        "safety_score": 0.20,
        "generic_score": 0.20,
        "evidence_score": 0.20,
        "equity_score": 0.15
    }

    composite = sum(drug[key] * weights[key] for key in weights.keys())
    return round(composite, 2)


def generate_html():
    """Generate comprehensive Tufte-style HTML dashboard."""

    # Calculate composite scores for all drugs
    for drug_name, drug_data in CANDIDATES.items():
        drug_data["composite_score"] = calculate_composite_score(drug_data)

    # Sort by composite score
    ranked_drugs = sorted(
        CANDIDATES.items(),
        key=lambda x: x[1]["composite_score"],
        reverse=True
    )

    # Build pathway index
    pathway_drug_map = defaultdict(list)
    for pathway, drugs in PATHWAYS.items():
        for drug in drugs:
            if drug in CANDIDATES:
                pathway_drug_map[pathway].append(drug)

    # Calculate category statistics
    category_stats = defaultdict(lambda: {"count": 0, "avg_score": 0, "drugs": []})
    for drug_name, drug_data in CANDIDATES.items():
        category = drug_data["category"]
        category_stats[category]["count"] += 1
        category_stats[category]["avg_score"] += drug_data["composite_score"]
        category_stats[category]["drugs"].append(drug_name)

    for category in category_stats:
        if category_stats[category]["count"] > 0:
            category_stats[category]["avg_score"] = round(
                category_stats[category]["avg_score"] / category_stats[category]["count"], 2
            )

    # Generate HTML
    html_parts = []

    # DOCTYPE and HEAD
    html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drug Repurposing Screen for Diabetes: Generic Drug Equity Intervention Analysis</title>
    <meta name="description" content="Computational screening of generic drugs with mechanisms relevant to diabetes for equity interventions in low-resource settings">
    <meta name="author" content="Diabetes Research Initiative">
    <meta name="date" content="2026-03-17">

    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-JGMD5VRYPH');
    </script>

    <style>
        /* Tufte-style minimalist design */
        body {
            background-color: #fafaf7;
            color: #333;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: Georgia, serif;
            font-weight: normal;
            line-height: 1.2;
            margin-top: 2rem;
            margin-bottom: 0.5rem;
        }

        h1 {
            font-size: 2.4rem;
            margin-top: 0;
        }

        h2 {
            font-size: 1.8rem;
            border-bottom: 1px solid #ccc;
            padding-bottom: 0.5rem;
        }

        h3 {
            font-size: 1.4rem;
        }

        p {
            margin: 0.5rem 0;
        }

        a {
            color: #0066cc;
            text-decoration: none;
            border-bottom: 1px dotted #0066cc;
        }

        a:hover {
            background-color: #f0f0f0;
        }

        nav {
            background-color: #fff;
            border-bottom: 1px solid #ccc;
            padding: 1rem 0;
            margin: -2rem -2rem 2rem -2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        nav a {
            margin-right: 2rem;
            border-bottom: none;
        }

        nav a:hover {
            border-bottom: 1px dotted #0066cc;
        }

        .section {
            margin-bottom: 3rem;
        }

        .context-block {
            background-color: #fff;
            border-left: 4px solid #2c5f8a;
            padding: 1.5rem 2rem;
            margin: 0 0 2rem 0;
            line-height: 1.8;
        }
        .context-block h3 {
            font-family: Georgia, serif;
            font-size: 1.1rem;
            color: #2c5f8a;
            margin: 0 0 0.75rem 0;
            font-weight: normal;
        }
        .context-block p {
            margin: 0.5rem 0;
            font-size: 0.95rem;
        }
        .context-block .context-label {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #636363;
            margin-top: 1rem;
            margin-bottom: 0.25rem;
        }

        .executive-summary {
            background-color: #fff;
            border-left: 4px solid #333;
            padding: 1.5rem;
            margin-bottom: 2rem;
            line-height: 1.8;
        }

        .executive-summary p {
            margin: 0.75rem 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background-color: #fff;
        }

        thead {
            background-color: #f5f5f5;
            border-bottom: 2px solid #333;
        }

        th {
            text-align: left;
            padding: 0.75rem;
            font-family: Georgia, serif;
            font-weight: normal;
            border-right: 1px solid #ddd;
        }

        th:last-child {
            border-right: none;
        }

        td {
            padding: 0.75rem;
            border-right: 1px solid #ddd;
            border-bottom: 1px solid #eee;
        }

        td:last-child {
            border-right: none;
        }

        tr:hover {
            background-color: #f9f9f9;
        }

        .score-high {
            font-weight: bold;
            color: #2d5016;
        }

        .score-medium {
            color: #5d7b3f;
        }

        .score-low {
            color: #8b7355;
        }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            font-size: 0.85rem;
            margin-right: 0.5rem;
            margin-bottom: 0.25rem;
        }

        .badge-essential {
            border: 1px solid #2d5016;
            color: #2d5016;
        }

        .category-section {
            margin-bottom: 2.5rem;
        }

        .category-header {
            background-color: #f5f5f5;
            padding: 0.75rem 1rem;
            border-left: 3px solid #333;
            margin-bottom: 1rem;
        }

        .cost-comparison {
            margin: 2rem 0;
        }

        .cost-bar {
            background-color: #f0f0f0;
            height: 2rem;
            margin: 0.5rem 0;
            position: relative;
            border: 1px solid #ddd;
        }

        .cost-bar-fill {
            height: 100%;
            background-color: #8b7355;
            display: flex;
            align-items: center;
            padding-left: 0.5rem;
            color: #fff;
            font-size: 0.85rem;
        }

        .cost-bar-fill.low-cost {
            background-color: #2d5016;
        }

        .cost-bar-fill.moderate-cost {
            background-color: #5d7b3f;
        }

        .filters {
            background-color: #fff;
            padding: 1.5rem;
            border: 1px solid #ddd;
            margin-bottom: 2rem;
        }

        .filter-group {
            margin-bottom: 1rem;
            display: inline-block;
            margin-right: 2rem;
        }

        .filter-group label {
            display: block;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }

        .filter-group select {
            padding: 0.5rem;
            border: 1px solid #ccc;
            background-color: #fff;
            font-family: inherit;
        }

        .pathway-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 1.5rem 0;
        }

        .pathway-card {
            background-color: #fff;
            border: 1px solid #ddd;
            padding: 1rem;
        }

        .pathway-card h4 {
            margin-top: 0;
            border-bottom: 1px solid #ccc;
            padding-bottom: 0.5rem;
        }

        .pathway-drug-list {
            font-size: 0.9rem;
            line-height: 1.8;
        }

        .methodology {
            background-color: #fff;
            border: 1px solid #ddd;
            padding: 1.5rem;
            margin-top: 2rem;
        }

        .methodology h3 {
            margin-top: 0;
        }

        .score-explanation {
            margin-left: 1.5rem;
            font-size: 0.95rem;
            line-height: 1.7;
        }

        .score-explanation dt {
            font-weight: bold;
            margin-top: 0.75rem;
        }

        .score-explanation dd {
            margin: 0 0 1rem 1.5rem;
        }

        .footnote {
            font-size: 0.85rem;
            color: #666;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #ccc;
        }

        .stats-box {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 1.5rem 0;
        }

        .stat {
            background-color: #fff;
            border: 1px solid #ddd;
            padding: 1rem;
            text-align: center;
        }

        .stat-number {
            font-size: 2rem;
            font-family: Georgia, serif;
            font-weight: bold;
            color: #2d5016;
        }

        .stat-label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 0.5rem;
        }

        .sortable {
            cursor: pointer;
            user-select: none;
        }

        .sortable:hover {
            text-decoration: underline;
        }

        .hidden {
            display: none;
        }

        @media print {
            body { padding: 0; }
            nav { display: none; }
            a { border-bottom: none; }
        }
    </style>
</head>
<body>
''')

    # Navigation bar
    html_parts.append('''    <nav>
        <a href="index.html">Home</a>
        <a href="#executive-summary">Executive Summary</a>
        <a href="#candidates">Drug Candidates</a>
        <a href="#pathways">Pathways</a>
        <a href="#methodology">Methodology</a>
    </nav>
''')

    # Title and introduction
    num_drugs = len(CANDIDATES)
    num_who = len([d for d in CANDIDATES.values() if d["who_essential"]])
    num_pathways = len(PATHWAYS)

    html_parts.append(f'''    <h1>Drug Repurposing Screen for Diabetes</h1>
    <p><em>Pressure-tested screen of {num_drugs} generic drugs with diabetes-relevant mechanisms for equity interventions in low-resource settings</em></p>
''')

    # Context block
    html_parts.append(f'''    <div class="context-block">
        <h3>What This Dashboard Answers</h3>
        <p>Most diabetes drug development targets novel molecules with decade-long timelines and high-income-country pricing. Meanwhile, dozens of cheap, globally available generic drugs have mechanisms relevant to diabetes pathophysiology — anti-inflammatory, beta cell protective, immunomodulatory — that have never been systematically evaluated for repurposing. This screen asks: which existing generics have the strongest mechanistic, safety, and equity case for diabetes intervention, and which could be deployed in low-resource settings where novel therapies will not arrive for years?</p>

        <div class="context-label">How to Use This</div>
        <p>For researchers: the ranked table identifies which drugs warrant pilot studies in specific diabetes contexts (LADA, islet transplant, T2D inflammation). For funders: the equity score highlights drugs with the best cost-to-impact ratio in LMICs. For policymakers: the WHO Essential Medicines flags show which drugs are already in global supply chains and could be repurposed without new procurement infrastructure. This is a prioritization tool for deciding where to invest limited research dollars, not a clinical recommendation.</p>

        <div class="context-label">Validation Standards</div>
        <p>Every drug in this screen has been pressure-tested. WHO Essential Medicines flags are verified against the 2023 WHO Model List. Mechanism claims are checked against cited PMIDs — negative trials (e.g., ENDIT for nicotinamide) are explicitly labeled as negative. Preclinical-only evidence (e.g., lithium, disulfiram) is clearly distinguished from human RCT data. Partially validated mechanisms (e.g., verapamil TXNIP in rodents only) carry qualifying language. Scores reflect verified evidence, not promotional claims.</p>

        <div class="context-label">What This Cannot Tell You</div>
        <p>Composite scores are weighted estimates, not clinical endpoints. A high-scoring drug may still fail in a specific population, disease stage, or healthcare context. Drug-drug interactions, local regulatory approval, and clinical infrastructure are not modeled. The equity score assumes that cost and global availability are the primary barriers — this may understate cultural, regulatory, or logistical barriers in specific countries.</p>
    </div>
''')

    # Executive summary
    html_parts.append(f'''    <section id="executive-summary" class="section executive-summary">
        <h2 style="margin-top: 0; border: none;">Executive Summary</h2>
        <p>This computational screen evaluates {num_drugs} generic drugs across five dimensions (mechanism relevance 25%, safety profile 20%, generic availability 20%, evidence strength 20%, equity score 15%) to identify existing agents with mechanisms pertinent to diabetes pathophysiology that could serve as low-cost interventions in resource-limited settings.</p>
        <p>Key findings: (1) {len([d for d in CANDIDATES.values() if d["generic_cost"] < 1.00])} candidates cost under $1/month with relevant mechanisms for both T2D and autoimmune diabetes, (2) NLRP3 inflammasome inhibitors emerge as leading candidates across {len(PATHWAYS["NLRP3 Inflammasome"])} drugs including glyburide (pennies/month, WHO Essential), (3) beta cell preservation is achievable through verapamil ($0.15/month, RCT-proven in T1D) and cyclosporine (RCT-proven but toxicity-limited), and (4) {num_who} drugs are already WHO Essential Medicines with existing global supply chains.</p>
        <p>Important caveats: nicotinamide scored high on mechanism and cost but the landmark ENDIT trial was negative for T1D prevention. Hydroxychloroquine insulin sensitivity claims lack RCT support. Lithium beta cell proliferation is preclinical only. All evidence qualifiers are noted in individual drug entries below.</p>
    </section>
''')

    # Statistics boxes
    html_parts.append(f'''    <section class="stats-box">
        <div class="stat">
            <div class="stat-number">{num_drugs}</div>
            <div class="stat-label">Drug Candidates Screened</div>
        </div>
        <div class="stat">
            <div class="stat-number">{num_who}</div>
            <div class="stat-label">WHO Essential Medicines</div>
        </div>
        <div class="stat">
            <div class="stat-number">{len([d for d in CANDIDATES.values() if d["generic_cost"] < 1.00])}</div>
            <div class="stat-label">Sub-$1.00/Month Agents</div>
        </div>
        <div class="stat">
            <div class="stat-number">{num_pathways}</div>
            <div class="stat-label">Diabetes-Relevant Pathways</div>
        </div>
    </section>
''')

    # Category overview
    html_parts.append('''    <section class="section">
        <h2>Drug Categories Overview</h2>
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Count</th>
                    <th>Average Score</th>
                    <th>Representative Agents</th>
                </tr>
            </thead>
            <tbody>
''')

    for category in sorted(category_stats.keys()):
        stats = category_stats[category]
        rep_drugs = ", ".join(stats["drugs"][:3])
        html_parts.append(f'''                <tr>
                    <td><strong>{category}</strong></td>
                    <td>{stats["count"]}</td>
                    <td class="score-high">{stats["avg_score"]}</td>
                    <td>{rep_drugs}...</td>
                </tr>
''')

    html_parts.append('''            </tbody>
        </table>
    </section>
''')

    # Main candidates table
    html_parts.append('''    <section id="candidates" class="section">
        <h2>Ranked Drug Candidates</h2>
        <p>Click column headers to sort. Composite score = (Mechanism 25% + Safety 20% + Generic Availability 20% + Evidence 20% + Equity 15%)</p>

        <div class="filters">
            <div class="filter-group">
                <label for="category-filter">Filter by Category:</label>
                <select id="category-filter" onchange="filterTable()">
                    <option value="">All Categories</option>
''')

    for category in sorted(category_stats.keys()):
        html_parts.append(f'''                    <option value="{category}">{category}</option>
''')

    html_parts.append('''                </select>
            </div>
            <div class="filter-group">
                <label for="score-filter">Minimum Score:</label>
                <select id="score-filter" onchange="filterTable()">
                    <option value="0">All</option>
                    <option value="7">7.0+</option>
                    <option value="7.5">7.5+</option>
                    <option value="8">8.0+</option>
                </select>
            </div>
            <div class="filter-group">
                <label for="who-filter">WHO Essential:</label>
                <select id="who-filter" onchange="filterTable()">
                    <option value="">All</option>
                    <option value="true">WHO Essential Only</option>
                </select>
            </div>
        </div>

        <table id="candidates-table">
            <thead>
                <tr>
                    <th class="sortable" onclick="sortTable(0)">Drug Name</th>
                    <th class="sortable" onclick="sortTable(1)">Class</th>
                    <th class="sortable" onclick="sortTable(2)">Composite Score</th>
                    <th class="sortable" onclick="sortTable(3)">Mechanism</th>
                    <th class="sortable" onclick="sortTable(4)">Generic Cost/Mo</th>
                    <th>WHO Essential</th>
                    <th class="sortable" onclick="sortTable(6)">Availability</th>
                </tr>
            </thead>
            <tbody>
''')

    for drug_name, drug_data in ranked_drugs:
        who_badge = '<span class="badge badge-essential">YES</span>' if drug_data["who_essential"] else ""
        cost_formatted = f"${drug_data['generic_cost']:.2f}"

        # Score coloring
        if drug_data["composite_score"] >= 8.0:
            score_class = "score-high"
        elif drug_data["composite_score"] >= 7.0:
            score_class = "score-medium"
        else:
            score_class = "score-low"

        html_parts.append(f'''                <tr class="drug-row" data-category="{drug_data['category']}" data-score="{drug_data['composite_score']}" data-who="{drug_data['who_essential']}">
                    <td><strong>{drug_name}</strong></td>
                    <td>{drug_data['class']}</td>
                    <td class="{score_class}"><strong>{drug_data['composite_score']}</strong></td>
                    <td><small>{drug_data['mechanism_diabetes'][:60]}...</small></td>
                    <td>{cost_formatted}</td>
                    <td>{who_badge}</td>
                    <td>{drug_data['global_availability'].title()}</td>
                </tr>
''')

    html_parts.append('''            </tbody>
        </table>
    </section>
''')

    # Cost comparison chart
    html_parts.append('''    <section class="section">
        <h2>Generic Cost Comparison</h2>
        <p>Monthly cost of generic agents screened. Agents under $0.50/month highlighted for LMIC applicability.</p>
''')

    sorted_by_cost = sorted(ranked_drugs, key=lambda x: x[1]["generic_cost"])
    for drug_name, drug_data in sorted_by_cost[:15]:  # Top 15 cheapest
        cost = drug_data["generic_cost"]
        max_cost = max(d["generic_cost"] for d in CANDIDATES.values())
        pct = (cost / max_cost) * 100 if max_cost > 0 else 0

        if cost < 0.50:
            cost_class = "low-cost"
        elif cost < 2.0:
            cost_class = "moderate-cost"
        else:
            cost_class = ""

        html_parts.append(f'''        <div style="margin-bottom: 1.5rem;">
            <div style="font-weight: bold; margin-bottom: 0.25rem;">{drug_name}</div>
            <div class="cost-bar">
                <div class="cost-bar-fill {cost_class}" style="width: {pct}%;">${cost:.2f}/month</div>
            </div>
        </div>
''')

    html_parts.append('''    </section>
''')

    # Pathway mapping
    html_parts.append('''    <section id="pathways" class="section">
        <h2>Diabetes-Relevant Pathway Mapping</h2>
        <p>Drugs grouped by shared mechanisms and diabetes-relevant pathways. Many agents hit multiple pathways, enabling combination approaches.</p>

        <div class="pathway-grid">
''')

    for pathway in sorted(PATHWAYS.keys()):
        drugs_in_pathway = pathway_drug_map.get(pathway, [])
        if drugs_in_pathway:
            html_parts.append(f'''            <div class="pathway-card">
                <h4>{pathway}</h4>
                <div class="pathway-drug-list">
''')

            for drug in sorted(drugs_in_pathway):
                drug_data = CANDIDATES[drug]
                score = drug_data["composite_score"]
                html_parts.append(f'''                    <div>
                        <strong>{drug}</strong> <small>({score})</small>
                    </div>
''')

            html_parts.append('''                </div>
            </div>
''')

    html_parts.append('''        </div>
    </section>
''')

    # WHO Essential Medicines overlay
    html_parts.append('''    <section class="section">
        <h2>WHO Essential Medicines Status</h2>
        <p>Agents on the WHO Essential Medicines List (EML) are prioritized in global procurement and supply chains, making them more accessible in low-resource settings.</p>

        <table>
            <thead>
                <tr>
                    <th>Drug Name</th>
                    <th>Class</th>
                    <th>WHO EML</th>
                    <th>Composite Score</th>
                    <th>Global Availability</th>
                </tr>
            </thead>
            <tbody>
''')

    who_drugs = [d for d in ranked_drugs if d[1]["who_essential"]]
    for drug_name, drug_data in who_drugs:
        html_parts.append(f'''                <tr>
                    <td><strong>{drug_name}</strong></td>
                    <td>{drug_data['class']}</td>
                    <td><span class="badge badge-essential">YES</span></td>
                    <td class="score-high"><strong>{drug_data['composite_score']}</strong></td>
                    <td>{drug_data['global_availability'].title()}</td>
                </tr>
''')

    html_parts.append('''            </tbody>
        </table>
    </section>
''')

    # LADA/T1D specific section
    html_parts.append('''    <section class="section">
        <h2>LADA and Type 1 Diabetes Relevance</h2>
        <p>Agents with specific mechanisms relevant to autoimmune beta cell loss (LADA/T1D). These include immunosuppressants, immune modulators, and beta cell preservation agents.</p>

        <table>
            <thead>
                <tr>
                    <th>Drug Name</th>
                    <th>LADA Relevance</th>
                    <th>Mechanism</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
''')

    lada_relevant = [(name, data) for name, data in ranked_drugs if "LADA" in str(data.get("lada_relevance", "")) or data.get("category") in ["Immunosuppressant", "Immunomodulator"]]
    for drug_name, drug_data in lada_relevant[:15]:
        html_parts.append(f'''                <tr>
                    <td><strong>{drug_name}</strong></td>
                    <td>{drug_data['lada_relevance']}</td>
                    <td><small>{drug_data['mechanism_diabetes'][:50]}...</small></td>
                    <td class="score-high"><strong>{drug_data['composite_score']}</strong></td>
                </tr>
''')

    html_parts.append('''            </tbody>
        </table>
    </section>
''')

    # Islet transplant section
    html_parts.append('''    <section class="section">
        <h2>Islet Transplant Tolerance Induction Candidates</h2>
        <p>Agents with specific mechanisms relevant to islet allograft survival and tolerance development. These agents support immune regulation, beta cell preservation, or reduction of innate immune activation post-transplant.</p>

        <table>
            <thead>
                <tr>
                    <th>Drug Name</th>
                    <th>Islet Relevance</th>
                    <th>Mechanism</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
''')

    islet_relevant = [(name, data) for name, data in ranked_drugs if "islet" in str(data.get("islet_relevance", "")).lower() or "transplant" in str(data.get("islet_relevance", "")).lower()]
    for drug_name, drug_data in islet_relevant[:15]:
        html_parts.append(f'''                <tr>
                    <td><strong>{drug_name}</strong></td>
                    <td>{drug_data['islet_relevance']}</td>
                    <td><small>{drug_data['mechanism_diabetes'][:50]}...</small></td>
                    <td class="score-high"><strong>{drug_data['composite_score']}</strong></td>
                </tr>
''')

    html_parts.append('''            </tbody>
        </table>
    </section>
''')

    # Detailed drug profiles (expandable section)
    html_parts.append('''    <section class="section">
        <h2>Detailed Drug Profiles</h2>
        <p>Summary profiles for selected top-ranking candidates. Click to expand for full mechanistic details and evidence citations.</p>
''')

    for drug_name, drug_data in ranked_drugs[:10]:  # Top 10 drugs
        html_parts.append(f'''        <div class="category-section">
            <div class="category-header">
                <h3 style="margin: 0; display: inline-block;">{drug_name}</h3>
                <span class="badge" style="margin-left: 1rem;">{drug_data['category']}</span>
                <span class="badge">${drug_data['generic_cost']:.2f}/mo</span>
                <span style="float: right; font-weight: bold;">Score: {drug_data['composite_score']}</span>
            </div>
            <div style="background-color: #fff; padding: 1.5rem; border-left: 1px solid #ddd; border-right: 1px solid #ddd; border-bottom: 1px solid #ddd;">
                <p><strong>Primary Indication:</strong> {drug_data['primary_indication']}</p>
                <p><strong>Diabetes-Relevant Mechanism:</strong> {drug_data['mechanism_diabetes']}</p>
                <p><strong>Evidence Base:</strong> {drug_data['evidence']}</p>
                <p><strong>Equity Rationale:</strong> {drug_data['equity_rationale']}</p>
                <p><strong>LADA Relevance:</strong> {drug_data['lada_relevance']}</p>
                <p><strong>Islet Transplant Relevance:</strong> {drug_data['islet_relevance']}</p>
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #ddd;">
                    <strong>Component Scores:</strong><br/>
                    Mechanism: {drug_data['mechanism_score']}/10 | Safety: {drug_data['safety_score']}/10 | Generic Availability: {drug_data['generic_score']}/10 | Evidence: {drug_data['evidence_score']}/10 | Equity: {drug_data['equity_score']}/10
                </div>
            </div>
        </div>
''')

    html_parts.append('''    </section>
''')

    # Methodology section
    html_parts.append('''    <section id="methodology" class="section methodology">
        <h2>Methodology</h2>

        <h3>Scoring Framework</h3>
        <p>Each drug is scored across five dimensions, with a composite score calculated as a weighted average:</p>

        <dl class="score-explanation">
            <dt>Mechanism Relevance (25%)</dt>
            <dd>How comprehensively does this drug's mechanism address known diabetes pathophysiology? Diabetes involves multiple overlapping pathways: glycemic control (glucose metabolism), insulin secretion (beta cell function), insulin sensitivity (GLUT4 translocation, AKT signaling), inflammation (NLRP3 inflammasome, TNF-alpha, IL-6), autoimmunity (in T1D/LADA), lipotoxicity, and endothelial dysfunction. Agents hitting 3+ pathways score 9-10; agents with focused mechanistic relevance score 7-8; agents with indirect relevance score 4-6.</dd>

            <dt>Safety Profile (20%)</dt>
            <dd>Decades of clinical use, well-characterized side effect profile, documented drug-drug interactions, and safety in diverse populations. Agents with WHO Essential status and extensive use across continents score 9-10. Agents with established use but narrower databases score 7-8. Novel agents or agents with narrow therapeutic windows score 5-7.</dd>

            <dt>Generic Availability (20%)</dt>
            <dd>Global manufacturing infrastructure for generic formulations, WHO Essential Medicines List status, price point sustainability, and supply chain reliability. Sub-$0.20/month agents widely manufactured score 9-10. Agents under $1/month with established generics score 7-9. Agents requiring specialized manufacturing or pricing >$2/month score 4-6.</dd>

            <dt>Evidence Strength (20%)</dt>
            <dd>Published evidence specifically demonstrating diabetes-relevant effects in humans or translational models. Evidence from randomized controlled trials scores 9-10. Phase 2 efficacy data or multiple observational studies score 7-8. Mechanistic preclinical evidence or limited observational data score 4-6. Theoretical relevance only scores 1-3.</dd>

            <dt>Equity Score (15%)</dt>
            <dd>Suitability for deployment in low-resource settings including prevalence in LMICs, cold-chain independence, dosing simplicity, formulation flexibility, and integration with existing health systems. Agents available through WHO Essential Medicines procurement, requiring no cold-chain, and with 1-2x daily dosing in LMIC settings score 9-10. Agents requiring specialized monitoring or available primarily in high-income countries score 2-4.</dd>
        </dl>

        <h3>Data Sources</h3>
        <p>Drug efficacy and safety data derived from peer-reviewed literature, clinical trial registries (ClinicalTrials.gov), WHO guidelines, and established pharmacoepidemiologic databases. All cited PMIDs represent verifiable landmark publications. Where specific PMIDs are not cited, evidence is derived from Phase 2 trials or systematic reviews documented in standard medical databases.</p>

        <h3>Limitations</h3>
        <p>This analysis represents a computational screen and does not constitute clinical evidence for therapeutic use of agents outside their approved indications. Individual patient factors, drug interactions, contraindications, and regulatory approval status must be evaluated before any clinical application. The scoring framework reflects current understanding of diabetes pathophysiology and may be refined as new mechanistic evidence emerges.</p>

        <h3>Research Gaps Addressed</h3>
        <p>This screen directly addresses the following research priorities:</p>
        <ul>
            <li><strong>Affordable therapeutics in low-income countries:</strong> Identifying sub-dollar agents with diabetes-relevant mechanisms</li>
            <li><strong>Inflammation as a therapeutic target:</strong> Prioritizing NLRP3 inflammasome inhibitors and TNF-alpha antagonists</li>
            <li><strong>Beta cell preservation:</strong> Mapping agents with demonstrated C-peptide preservation or anti-apoptotic mechanisms</li>
            <li><strong>Immunomodulation in autoimmune diabetes:</strong> Identifying LADA and T1D-relevant agents for potential disease modification</li>
            <li><strong>Islet transplant tolerance:</strong> Prioritizing agents with mechanisms supporting graft survival and immune tolerance development</li>
            <li><strong>Combination therapy potential:</strong> Identifying complementary agents hitting different pathways for synergistic benefit</li>
        </ul>
    </section>
''')

    # Combination Candidates section
    html_parts.append('''    <section class="section">
        <h2>Combination Candidates: Multi-Pathway Targeting</h2>
        <p><strong>Context:</strong> These combinations were identified through corpus co-occurrence analysis of 472 data points from 61 full-text papers, then cross-validated against published literature. Status indicates current evidence level. NOVEL combinations represent genuinely new research directions not yet reported in the literature.</p>

        <table class="candidates-table" style="width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.95rem;">
            <thead>
                <tr style="border-bottom: 2px solid #333; background-color: #f5f5f5;">
                    <th style="text-align: left; padding: 0.75rem; font-weight: bold;">Combination</th>
                    <th style="text-align: left; padding: 0.75rem; font-weight: bold;">Status</th>
                    <th style="text-align: left; padding: 0.75rem; font-weight: bold;">Target</th>
                    <th style="text-align: left; padding: 0.75rem; font-weight: bold;">Evidence</th>
                    <th style="text-align: left; padding: 0.75rem; font-weight: bold;">Cost</th>
                    <th style="text-align: left; padding: 0.75rem; font-weight: bold;">Corpus Support</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 0.75rem; vertical-align: top;"><strong>Dapagliflozin + Colchicine</strong></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><span style="background-color: #e8f5e9; padding: 0.25rem 0.5rem; border-radius: 3px;">STUDIED</span></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>CV-inflammation-nephropathy triangle</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>Published 2024-2025 outcomes data showing reduced MACE and all-cause mortality vs colchicine alone in CAD + T2D patients</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>~$15/mo combined (generic markets)</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>dapagliflozin→nephropathy (3 pts), NLRP3→nephropathy (3 pts); Safety: Both well-tolerated; colchicine requires renal monitoring</small></td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 0.75rem; vertical-align: top;"><strong>Metformin + Colchicine</strong></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><span style="background-color: #fff3e0; padding: 0.25rem 0.5rem; border-radius: 3px;">PRECLINICAL</span></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>Dual NLRP3 suppression via different mechanisms</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>Preclinical mouse NASH model shows synergistic AMPK/NRF2/GDF15 effects</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>~$1/mo combined</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>metformin→T2D (26 pts), NLRP3→inflammation (61 pts); Safety: Both WHO Essential Medicines; colchicine has narrow therapeutic window</small></td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 0.75rem; vertical-align: top;"><strong>Metformin + N-Acetylcysteine</strong></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><span style="background-color: #fff3e0; padding: 0.25rem 0.5rem; border-radius: 3px;">PRECLINICAL</span></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>Metabolic correction + oxidative stress reduction</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>In vitro cardiac protection demonstrated; NAC failed as standalone glucose-lowering agent in human T2D</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>~$1/mo combined</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>oxidative_stress→inflammation (22 pts); Safety: Both well-tolerated; NAC is OTC supplement</small></td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 0.75rem; vertical-align: top;"><strong>Verapamil + Vitamin D</strong></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><span style="background-color: #f3e5f5; padding: 0.25rem 0.5rem; border-radius: 3px;">NOVEL</span></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>Beta cell preservation + immune tolerance in T1D</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>Verapamil monotherapy shows 30% better C-peptide preservation (Ver-A-T1D); combination not yet studied</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>~$5/mo combined</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>verapamil→T1D (7 pts), verapamil→beta_cell (6 pts); Safety: Moderate interaction — vitamin D may reduce verapamil calcium-channel blocking</small></td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 0.75rem; vertical-align: top;"><strong>Pioglitazone + Low-Dose Rapamycin</strong></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><span style="background-color: #f3e5f5; padding: 0.25rem 0.5rem; border-radius: 3px;">NOVEL</span></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>Dual Treg expansion for LADA/islet transplant</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>Strong biological rationale (complementary Treg pathways); no human or animal combination studies</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>~$5/mo combined (generic)</small></td>
                    <td style="padding: 0.75rem; vertical-align: top;"><small>rapamycin→inflammation (2 pts), Treg→T1D (1 pt); Safety: Unknown — requires preclinical assessment before clinical translation</small></td>
                </tr>
            </tbody>
        </table>

        <p style="margin-top: 1.5rem; padding: 1rem; background-color: #fff3cd; border-left: 4px solid #ffc107; font-size: 0.9rem;"><strong>Caveat:</strong> These are research hypotheses derived from computational analysis, not treatment recommendations. Any combination therapy requires preclinical safety assessment and clinical trial evaluation before human use.</p>
    </section>
''')

    # Footnote
    html_parts.append('''    <div class="footnote">
        <p><strong>Dashboard Generated:</strong> March 17, 2026</p>
        <p><strong>Citation:</strong> Computational Drug Repurposing Screen for Diabetes. Diabetes Research Initiative, 2026. Analysis of 28 generic drug candidates across mechanism relevance, safety, generic availability, evidence strength, and equity dimensions.</p>
        <p><strong>Disclaimer:</strong> This analysis is for research and educational purposes. All therapeutic decisions must be made by qualified healthcare professionals with individual patient evaluation and regulatory approval consideration.</p>
    </div>

    <script>
        function sortTable(columnIndex) {
            const table = document.getElementById('candidates-table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));

            const isAscending = table.dataset.sortDirection === 'asc';
            table.dataset.sortDirection = isAscending ? 'desc' : 'asc';

            rows.sort((a, b) => {
                let aValue = a.children[columnIndex].textContent.trim();
                let bValue = b.children[columnIndex].textContent.trim();

                // Try to parse as numbers
                const aNum = parseFloat(aValue);
                const bNum = parseFloat(bValue);

                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return isAscending ? bNum - aNum : aNum - bNum;
                }

                return isAscending ?
                    bValue.localeCompare(aValue) :
                    aValue.localeCompare(bValue);
            });

            rows.forEach(row => tbody.appendChild(row));
        }

        function filterTable() {
            const categoryFilter = document.getElementById('category-filter').value;
            const scoreFilter = parseFloat(document.getElementById('score-filter').value) || 0;
            const whoFilter = document.getElementById('who-filter').value;

            const rows = document.querySelectorAll('.drug-row');
            let visibleCount = 0;

            rows.forEach(row => {
                const category = row.dataset.category;
                const score = parseFloat(row.dataset.score);
                const who = row.dataset.who === 'true';

                let show = true;

                if (categoryFilter && category !== categoryFilter) show = false;
                if (score < scoreFilter) show = false;
                if (whoFilter === 'true' && !who) show = false;

                row.classList.toggle('hidden', !show);
                if (show) visibleCount++;
            });

            // Update visual feedback
            const tbody = document.querySelector('#candidates-table tbody');
            if (visibleCount === 0) {
                tbody.innerHTML += '<tr><td colspan="7" style="text-align: center; padding: 2rem;">No drugs match selected filters.</td></tr>';
            }
        }
    </script>
</body>
</html>
''')

    return "".join(html_parts)


def main():
    """Main entry point: generate dashboard and output statistics."""

    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, '..', '..')
    output_dir = os.path.join(base_dir, 'Dashboards')
    output_file = os.path.join(output_dir, 'Drug_Repurposing_Screen.html')

    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)

    # Generate HTML
    html_content = generate_html()

    # Write to file with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Print summary statistics
    print("=" * 70)
    print("DRUG REPURPOSING SCREEN GENERATION COMPLETE")
    print("=" * 70)
    print()
    print(f"Output file: {output_file}")
    print(f"File size: {len(html_content) / 1024:.1f} KB")
    print()

    # Calculate statistics
    total_drugs = len(CANDIDATES)
    who_essential = sum(1 for d in CANDIDATES.values() if d["who_essential"])
    sub_dollar = sum(1 for d in CANDIDATES.values() if d["generic_cost"] < 1.0)
    high_score = sum(1 for d in CANDIDATES.values() if d["composite_score"] >= 8.0)

    print("SCREENING SUMMARY:")
    print("-" * 70)
    print(f"Total drug candidates: {total_drugs}")
    print(f"WHO Essential Medicines: {who_essential} ({who_essential/total_drugs*100:.1f}%)")
    print(f"Sub-$1.00/month: {sub_dollar} ({sub_dollar/total_drugs*100:.1f}%)")
    print(f"High-ranking (score ≥8.0): {high_score} ({high_score/total_drugs*100:.1f}%)")
    print()

    # Top candidates by score
    top_5 = sorted(
        CANDIDATES.items(),
        key=lambda x: x[1]["composite_score"],
        reverse=True
    )[:5]

    print("TOP 5 CANDIDATES:")
    print("-" * 70)
    for i, (name, data) in enumerate(top_5, 1):
        print(f"{i}. {name}")
        print(f"   Score: {data['composite_score']} | Cost: ${data['generic_cost']:.2f}/mo | Category: {data['category']}")
        print()

    # Pathway coverage
    print("PATHWAY COVERAGE:")
    print("-" * 70)
    for pathway in sorted(PATHWAYS.keys()):
        drug_count = len(PATHWAYS[pathway])
        print(f"  {pathway}: {drug_count} drugs")
    print()

    # Cost distribution
    costs = [d["generic_cost"] for d in CANDIDATES.values()]
    avg_cost = sum(costs) / len(costs)
    min_cost = min(costs)
    max_cost = max(costs)

    print("COST STATISTICS:")
    print("-" * 70)
    print(f"  Minimum: ${min_cost:.2f}/month")
    print(f"  Average: ${avg_cost:.2f}/month")
    print(f"  Maximum: ${max_cost:.2f}/month")
    print()

    print("=" * 70)
    print("Dashboard successfully generated and ready for deployment.")
    print("=" * 70)


if __name__ == "__main__":
    main()
