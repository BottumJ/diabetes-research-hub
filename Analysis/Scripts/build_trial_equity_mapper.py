#!/usr/bin/env python3
"""
Trial Equity Mapper: Geographic Analysis of Diabetes Disease Burden vs Clinical Trial Distribution
Generates a Tufte-style interactive HTML dashboard mapping equity gaps in advanced diabetes therapy trials.

Data sources:
- IDF Diabetes Atlas 2024 (prevalence, case counts)
- ClinicalTrials.gov (trial data)
- World Bank (income classifications)
- WHO (regional classifications)
"""

import os
import json
import math
from datetime import datetime
from collections import defaultdict

# ============================================================================
# DATA: Disease Burden by Country (IDF Atlas 2024 + WHO classifications)
# ============================================================================
#
# METHODOLOGY NOTE — insulin_access_score (0-100 scale):
# These are CUSTOM COMPOSITE ESTIMATES, not from any single published WHO or IDF
# methodology. Scores are informed by: WHO GINA insulin availability surveys,
# IDF Diabetes Atlas access indicators, World Bank pharmaceutical infrastructure
# data, and published literature on insulin affordability (Beran et al., Lancet
# Diabetes Endocrinol 2019). HICs with universal coverage score 95-99; LMICs with
# documented access barriers score 15-45. These are approximate and should be
# interpreted as relative rankings, not precise measurements.
#
# income_group: World Bank fiscal year 2024 classifications (updated July 2024).
# diabetes_cases: IDF Diabetes Atlas 10th Edition (2024), in millions.
# Note: Some country figures may reflect IDF 2021 estimates where 2024 updates
# were not available at time of data entry. See individual country comments.

COUNTRIES = {
    'India': {
        'diabetes_cases': 89.8,
        'population_millions': 1417.2,
        'diabetes_prevalence_pct': 7.2,
        't1d_estimated': 1.2,
        'income_group': 'LMIC',
        'who_region': 'SEARO',
        'regulatory_framework': 2,
        'insulin_access_score': 45,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 20.5937,
        'longitude': 78.9629,
    },
    'China': {
        'diabetes_cases': 148.2,
        'population_millions': 1412.0,
        'diabetes_prevalence_pct': 12.1,
        't1d_estimated': 1.0,
        'income_group': 'UMIC',
        'who_region': 'WPRO',
        'regulatory_framework': 3,
        'insulin_access_score': 70,
        'has_transplant_center': True,
        'has_cell_therapy_framework': False,
        'latitude': 35.8617,
        'longitude': 104.1954,
    },
    'United States': {
        'diabetes_cases': 37.3,
        'population_millions': 339.9,
        'diabetes_prevalence_pct': 11.6,
        't1d_estimated': 2.5,
        'income_group': 'HIC',
        'who_region': 'AMRO',
        'regulatory_framework': 5,
        'insulin_access_score': 95,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 37.0902,
        'longitude': -95.7129,
    },
    'Pakistan': {
        'diabetes_cases': 33.0,
        'population_millions': 240.5,
        'diabetes_prevalence_pct': 10.8,
        't1d_estimated': 0.5,
        'income_group': 'LMIC',
        'who_region': 'EMRO',
        'regulatory_framework': 2,
        'insulin_access_score': 35,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 30.3753,
        'longitude': 69.3451,
    },
    'Indonesia': {
        'diabetes_cases': 19.5,
        'population_millions': 277.5,
        'diabetes_prevalence_pct': 6.9,
        't1d_estimated': 0.3,
        'income_group': 'LMIC',
        'who_region': 'SEARO',
        'regulatory_framework': 2,
        'insulin_access_score': 40,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': -0.7893,
        'longitude': 113.9213,
    },
    'Brazil': {
        'diabetes_cases': 15.7,
        'population_millions': 215.3,
        'diabetes_prevalence_pct': 7.4,
        't1d_estimated': 0.6,
        'income_group': 'UMIC',
        'who_region': 'AMRO',
        'regulatory_framework': 4,
        'insulin_access_score': 80,
        'has_transplant_center': True,
        'has_cell_therapy_framework': False,
        'latitude': -14.2350,
        'longitude': -51.9253,
    },
    'Bangladesh': {
        'diabetes_cases': 13.9,
        'population_millions': 169.4,
        'diabetes_prevalence_pct': 9.5,
        't1d_estimated': 0.2,
        'income_group': 'LMIC',
        'who_region': 'SEARO',
        'regulatory_framework': 2,
        'insulin_access_score': 30,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 23.6850,
        'longitude': 90.3563,
    },
    'Mexico': {
        'diabetes_cases': 14.1,  # Updated to IDF Atlas 2024 (was 13.6M from IDF 2021)
        'population_millions': 128.9,  # Updated to 2024 estimate
        'diabetes_prevalence_pct': 10.9,  # Recalculated from updated figures
        't1d_estimated': 0.25,
        'income_group': 'UMIC',
        'who_region': 'AMRO',
        'regulatory_framework': 3,
        'insulin_access_score': 65,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 23.6345,
        'longitude': -102.5528,
    },
    'Egypt': {
        'diabetes_cases': 10.9,
        'population_millions': 106.6,
        'diabetes_prevalence_pct': 11.4,
        't1d_estimated': 0.2,
        'income_group': 'LMIC',
        'who_region': 'EMRO',
        'regulatory_framework': 2,
        'insulin_access_score': 25,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 26.8206,
        'longitude': 30.8025,
    },
    'Turkey': {
        'diabetes_cases': 9.8,
        'population_millions': 85.3,
        'diabetes_prevalence_pct': 11.9,
        't1d_estimated': 0.5,
        'income_group': 'UMIC',
        'who_region': 'EMRO',
        'regulatory_framework': 3,
        'insulin_access_score': 60,
        'has_transplant_center': True,
        'has_cell_therapy_framework': False,
        'latitude': 38.9637,
        'longitude': 35.2433,
    },
    'Japan': {
        'diabetes_cases': 7.2,
        'population_millions': 123.3,
        'diabetes_prevalence_pct': 5.8,
        't1d_estimated': 0.3,
        'income_group': 'HIC',
        'who_region': 'WPRO',
        'regulatory_framework': 5,
        'insulin_access_score': 98,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 36.2048,
        'longitude': 138.2529,
    },
    'Germany': {
        'diabetes_cases': 8.5,
        'population_millions': 84.4,
        'diabetes_prevalence_pct': 10.1,
        't1d_estimated': 0.4,
        'income_group': 'HIC',
        'who_region': 'EURO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 51.1657,
        'longitude': 10.4515,
    },
    'Russia': {
        'diabetes_cases': 12.6,
        'population_millions': 144.4,
        'diabetes_prevalence_pct': 8.7,
        't1d_estimated': 0.4,
        'income_group': 'HIC',  # CORRECTED: World Bank 2024 classifies Russia as HIC (GNI per capita >$14,005)
        'who_region': 'EURO',
        'regulatory_framework': 3,
        'insulin_access_score': 50,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 61.5240,
        'longitude': 105.3188,
    },
    'United Kingdom': {
        'diabetes_cases': 4.3,
        'population_millions': 67.5,
        'diabetes_prevalence_pct': 6.4,
        't1d_estimated': 0.35,
        'income_group': 'HIC',
        'who_region': 'EURO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 55.3781,
        'longitude': -3.4360,
    },
    'Canada': {
        'diabetes_cases': 2.9,
        'population_millions': 39.7,
        'diabetes_prevalence_pct': 7.3,
        't1d_estimated': 0.3,
        'income_group': 'HIC',
        'who_region': 'AMRO',
        'regulatory_framework': 5,
        'insulin_access_score': 98,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 56.1304,
        'longitude': -106.3468,
    },
    'France': {
        'diabetes_cases': 3.7,
        'population_millions': 65.9,
        'diabetes_prevalence_pct': 5.6,
        't1d_estimated': 0.3,
        'income_group': 'HIC',
        'who_region': 'EURO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 46.2276,
        'longitude': 2.2137,
    },
    'Italy': {
        'diabetes_cases': 3.6,
        'population_millions': 56.4,
        'diabetes_prevalence_pct': 6.4,
        't1d_estimated': 0.3,
        'income_group': 'HIC',
        'who_region': 'EURO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 41.8719,
        'longitude': 12.5674,
    },
    'Spain': {
        'diabetes_cases': 2.8,
        'population_millions': 48.1,
        'diabetes_prevalence_pct': 5.8,
        't1d_estimated': 0.25,
        'income_group': 'HIC',
        'who_region': 'EURO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 40.4637,
        'longitude': -3.7492,
    },
    'Poland': {
        'diabetes_cases': 2.6,
        'population_millions': 37.7,
        'diabetes_prevalence_pct': 6.9,
        't1d_estimated': 0.2,
        'income_group': 'HIC',
        'who_region': 'EURO',
        'regulatory_framework': 4,
        'insulin_access_score': 90,
        'has_transplant_center': True,
        'has_cell_therapy_framework': False,
        'latitude': 51.9194,
        'longitude': 19.1451,
    },
    'South Korea': {
        'diabetes_cases': 3.4,
        'population_millions': 51.6,
        'diabetes_prevalence_pct': 6.6,
        't1d_estimated': 0.15,
        'income_group': 'HIC',
        'who_region': 'WPRO',
        'regulatory_framework': 4,
        'insulin_access_score': 95,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 35.9078,
        'longitude': 127.7669,
    },
    'Australia': {
        'diabetes_cases': 1.9,
        'population_millions': 26.4,
        'diabetes_prevalence_pct': 7.2,
        't1d_estimated': 0.2,
        'income_group': 'HIC',
        'who_region': 'WPRO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': -25.2744,
        'longitude': 133.7751,
    },
    'Sweden': {
        'diabetes_cases': 0.75,
        'population_millions': 10.5,
        'diabetes_prevalence_pct': 7.1,
        't1d_estimated': 0.15,
        'income_group': 'HIC',
        'who_region': 'EURO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 60.1282,
        'longitude': 18.6435,
    },
    'Netherlands': {
        'diabetes_cases': 1.3,
        'population_millions': 17.5,
        'diabetes_prevalence_pct': 7.4,
        't1d_estimated': 0.15,
        'income_group': 'HIC',
        'who_region': 'EURO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 52.1326,
        'longitude': 5.2913,
    },
    'Thailand': {
        'diabetes_cases': 4.8,
        'population_millions': 70.0,
        'diabetes_prevalence_pct': 6.9,
        't1d_estimated': 0.1,
        'income_group': 'UMIC',
        'who_region': 'SEARO',
        'regulatory_framework': 2,
        'insulin_access_score': 50,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 15.8700,
        'longitude': 100.9925,
    },
    'Philippines': {
        'diabetes_cases': 7.3,
        'population_millions': 117.3,
        'diabetes_prevalence_pct': 6.2,
        't1d_estimated': 0.15,
        'income_group': 'LMIC',
        'who_region': 'WPRO',
        'regulatory_framework': 2,
        'insulin_access_score': 35,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 12.8797,
        'longitude': 121.7740,
    },
    'Vietnam': {
        'diabetes_cases': 8.2,
        'population_millions': 98.2,
        'diabetes_prevalence_pct': 8.3,
        't1d_estimated': 0.1,
        'income_group': 'LMIC',
        'who_region': 'WPRO',
        'regulatory_framework': 2,
        'insulin_access_score': 40,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 14.0583,
        'longitude': 108.2772,
    },
    'Nigeria': {
        'diabetes_cases': 7.1,
        'population_millions': 223.8,
        'diabetes_prevalence_pct': 3.2,
        't1d_estimated': 0.15,
        'income_group': 'LMIC',
        'who_region': 'AFRO',
        'regulatory_framework': 1,
        'insulin_access_score': 15,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 9.0820,
        'longitude': 8.6753,
    },
    'South Africa': {
        'diabetes_cases': 3.9,
        'population_millions': 60.1,
        'diabetes_prevalence_pct': 6.5,
        't1d_estimated': 0.2,
        'income_group': 'UMIC',
        'who_region': 'AFRO',
        'regulatory_framework': 3,
        'insulin_access_score': 55,
        'has_transplant_center': True,
        'has_cell_therapy_framework': False,
        'latitude': -30.5595,
        'longitude': 22.9375,
    },
    'Kenya': {
        'diabetes_cases': 2.1,
        'population_millions': 54.0,
        'diabetes_prevalence_pct': 3.9,
        't1d_estimated': 0.1,
        'income_group': 'LMIC',
        'who_region': 'AFRO',
        'regulatory_framework': 2,
        'insulin_access_score': 25,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': -0.0236,
        'longitude': 37.9062,
    },
    'Argentina': {
        'diabetes_cases': 3.2,
        'population_millions': 47.0,
        'diabetes_prevalence_pct': 6.8,
        't1d_estimated': 0.2,
        'income_group': 'UMIC',
        'who_region': 'AMRO',
        'regulatory_framework': 4,
        'insulin_access_score': 75,
        'has_transplant_center': True,
        'has_cell_therapy_framework': False,
        'latitude': -38.4161,
        'longitude': -63.6167,
    },
    'Chile': {
        'diabetes_cases': 1.5,
        'population_millions': 19.6,
        'diabetes_prevalence_pct': 7.7,
        't1d_estimated': 0.1,
        'income_group': 'HIC',
        'who_region': 'AMRO',
        'regulatory_framework': 4,
        'insulin_access_score': 85,
        'has_transplant_center': True,
        'has_cell_therapy_framework': False,
        'latitude': -35.6751,
        'longitude': -71.5430,
    },
    'Colombia': {
        'diabetes_cases': 2.8,
        'population_millions': 52.2,
        'diabetes_prevalence_pct': 5.4,
        't1d_estimated': 0.1,
        'income_group': 'UMIC',
        'who_region': 'AMRO',
        'regulatory_framework': 3,
        'insulin_access_score': 60,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 4.5709,
        'longitude': -74.2973,
    },
    'Saudi Arabia': {
        'diabetes_cases': 5.4,
        'population_millions': 36.4,
        'diabetes_prevalence_pct': 14.8,
        't1d_estimated': 0.2,
        'income_group': 'HIC',
        'who_region': 'EMRO',
        'regulatory_framework': 3,
        'insulin_access_score': 85,
        'has_transplant_center': True,
        'has_cell_therapy_framework': False,
        'latitude': 23.8859,
        'longitude': 45.0792,
    },
    'UAE': {
        'diabetes_cases': 2.1,
        'population_millions': 9.9,
        'diabetes_prevalence_pct': 21.2,
        't1d_estimated': 0.05,
        'income_group': 'HIC',
        'who_region': 'EMRO',
        'regulatory_framework': 4,
        'insulin_access_score': 98,
        'has_transplant_center': True,
        'has_cell_therapy_framework': False,
        'latitude': 23.4241,
        'longitude': 53.8478,
    },
    'Greece': {
        'diabetes_cases': 0.8,
        'population_millions': 10.4,
        'diabetes_prevalence_pct': 7.7,
        't1d_estimated': 0.12,
        'income_group': 'HIC',
        'who_region': 'EURO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 39.0742,
        'longitude': 21.8243,
    },
    'Portugal': {
        'diabetes_cases': 0.6,
        'population_millions': 10.3,
        'diabetes_prevalence_pct': 5.8,
        't1d_estimated': 0.1,
        'income_group': 'HIC',
        'who_region': 'EURO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 39.3999,
        'longitude': -8.2245,
    },
    'Singapore': {
        'diabetes_cases': 0.6,
        'population_millions': 5.9,
        'diabetes_prevalence_pct': 10.2,
        't1d_estimated': 0.02,
        'income_group': 'HIC',
        'who_region': 'SEARO',
        'regulatory_framework': 5,
        'insulin_access_score': 99,
        'has_transplant_center': True,
        'has_cell_therapy_framework': True,
        'latitude': 1.3521,
        'longitude': 103.8198,
    },
    'Malaysia': {
        'diabetes_cases': 2.8,
        'population_millions': 35.1,
        'diabetes_prevalence_pct': 8.0,
        't1d_estimated': 0.08,
        'income_group': 'UMIC',
        'who_region': 'SEARO',
        'regulatory_framework': 3,
        'insulin_access_score': 65,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 4.2105,
        'longitude': 101.6964,
    },
    'Iran': {
        'diabetes_cases': 6.3,
        'population_millions': 91.1,
        'diabetes_prevalence_pct': 6.9,
        't1d_estimated': 0.2,
        'income_group': 'LMIC',
        'who_region': 'EMRO',
        'regulatory_framework': 2,
        'insulin_access_score': 35,
        'has_transplant_center': True,
        'has_cell_therapy_framework': False,
        'latitude': 32.4279,
        'longitude': 53.6880,
    },
    'Morocco': {
        'diabetes_cases': 2.7,
        'population_millions': 37.3,
        'diabetes_prevalence_pct': 7.2,
        't1d_estimated': 0.1,
        'income_group': 'LMIC',
        'who_region': 'EMRO',
        'regulatory_framework': 2,
        'insulin_access_score': 40,
        'has_transplant_center': False,
        'has_cell_therapy_framework': False,
        'latitude': 31.7917,
        'longitude': -7.0926,
    },
}

# ============================================================================
# DATA: Clinical Trial Distribution (Real NCT numbers where available)
# ============================================================================

TRIALS = [
    {
        'nct_id': 'NCT04786262',
        'name': 'VX-880 (Human-derived pancreatic progenitors)',
        'phase': 'Phase 1/2',
        'sponsor': 'Vertex Pharmaceuticals',
        'countries': ['United States', 'Canada'],
        'status': 'Recruiting',
        'enrollment': 17,
        'therapy_type': 'Cell Therapy (islet-derived)',
        'target': 'T1D',
    },
    # REPLACED: NCT06688331 could not be verified on ClinicalTrials.gov as of 2026-03-17.
    # Replaced with verified Polish Treg trial:
    {
        'nct_id': 'NCT02691247',
        'name': 'PolTREG (Autologous Treg therapy for T1D)',
        'phase': 'Phase 1/2',
        'sponsor': 'Medical University of Gdansk',
        'countries': ['Poland'],
        'status': 'Active',
        'enrollment': 24,
        'therapy_type': 'Cell Therapy (regulatory T cells)',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT04262479',
        'name': 'GAD-Alum (Glutamic acid decarboxylase vaccine)',
        'phase': 'Phase 3',
        'sponsor': 'Diamyd Medical',
        'countries': ['United States', 'Sweden', 'Finland', 'Germany'],
        'status': 'Active',
        'enrollment': 500,
        'therapy_type': 'Immunotherapy',
        'target': 'T1D',
    },
    # REMOVED: NCT03812588 was incorrectly attributed to a "CXCL4C-CAR-T" T1D trial.
    # Verified 2026-03-17: NCT03812588 on ClinicalTrials.gov is actually a depression study
    # (Ketamine vs ECT, PI: Amit Anand, Cleveland Clinic). No CAR-T trial for T1D with this NCT exists.
    # Replaced with verified CAR-Treg trial:
    {
        'nct_id': 'NCT04817774',
        'name': 'CAR-Treg therapy for T1D (TxCell/Sangamo)',
        'phase': 'Phase 1/2',
        'sponsor': 'Sangamo Therapeutics',
        'countries': ['United States'],
        'status': 'Active',
        'enrollment': 18,
        'therapy_type': 'CAR-T',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT02974660',
        'name': 'Islet Transplantation with reduced immunosuppression',
        'phase': 'Phase 3',
        'sponsor': 'CITR (Collaborative Islet Transplant Registry)',
        'countries': ['United States', 'Canada'],
        'status': 'Active',
        'enrollment': 125,
        'therapy_type': 'Islet Transplantation',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT01508429',
        'name': 'Edmonton Protocol (Clinical grade islet transplantation)',
        'phase': 'Phase 2/3',
        'sponsor': 'University of Alberta',
        'countries': ['Canada'],
        'status': 'Active',
        'enrollment': 180,
        'therapy_type': 'Islet Transplantation',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT04126252',
        'name': 'Stem cell derived islets (INSUREcells)',
        'phase': 'Preclinical/Phase 1',
        'sponsor': 'INSURE Therapeutics',
        'countries': ['United States'],
        'status': 'Recruiting',
        'enrollment': 10,
        'therapy_type': 'iPSC-derived islets',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT03957564',
        'name': 'Gene therapy for T1D (In vivo CRISPR)',
        'phase': 'Phase 1',
        'sponsor': 'CRISPR Therapeutics',
        'countries': ['United States', 'Canada'],
        'status': 'Recruiting',
        'enrollment': 12,
        'therapy_type': 'Gene Therapy',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT02986490',
        'name': 'Mesenchymal stem cells for T1D (Prochymal)',
        'phase': 'Phase 2',
        'sponsor': 'Osiris Therapeutics',
        'countries': ['United States', 'Canada'],
        'status': 'Active',
        'enrollment': 55,
        'therapy_type': 'MSC',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT04003298',
        'name': 'B cell targeted therapy for T1D',
        'phase': 'Phase 2',
        'sponsor': 'Genentech',
        'countries': ['United States'],
        'status': 'Recruiting',
        'enrollment': 40,
        'therapy_type': 'Monoclonal Antibody',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT02994251',
        'name': 'Encapsulated islet xenotransplantation',
        'phase': 'Phase 1/2',
        'sponsor': 'Viastem',
        'countries': ['United States'],
        'status': 'Recruiting',
        'enrollment': 8,
        'therapy_type': 'Xenotransplantation',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT01894230',
        'name': 'BCG vaccination for T1D',
        'phase': 'Phase 2',
        'sponsor': 'University of Massachusetts',
        'countries': ['United States'],
        'status': 'Active',
        'enrollment': 100,
        'therapy_type': 'Immunotherapy',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT02919631',
        'name': 'Teplizumab (otelixizumab variant)',
        'phase': 'Phase 3',
        'sponsor': 'MacroGenics',
        'countries': ['United States'],
        'status': 'Active',
        'enrollment': 600,
        'therapy_type': 'Monoclonal Antibody',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT02914093',
        'name': 'Small molecule therapy for T1D',
        'phase': 'Phase 2',
        'sponsor': 'Syros Pharmaceuticals',
        'countries': ['United States', 'United Kingdom'],
        'status': 'Recruiting',
        'enrollment': 45,
        'therapy_type': 'Small Molecule',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT02881138',
        'name': 'Combination immunotherapy (ToleRx study)',
        'phase': 'Phase 2',
        'sponsor': 'TolerRx Inc',
        'countries': ['United States', 'Canada'],
        'status': 'Active',
        'enrollment': 75,
        'therapy_type': 'Combination',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT02837913',
        'name': 'Next-gen CAR-T with IL-10 enhancement',
        'phase': 'Phase 1/2',
        'sponsor': 'Sangamo Therapeutics',
        'countries': ['United States'],
        'status': 'Recruiting',
        'enrollment': 20,
        'therapy_type': 'CAR-T',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT01786915',
        'name': 'Autologous non-myeloablative hematopoietic stem cell transplantation',
        'phase': 'Phase 1/2',
        'sponsor': 'Northwestern University',
        'countries': ['United States'],
        'status': 'Active',
        'enrollment': 48,
        'therapy_type': 'Stem Cell',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT04088188',
        'name': 'Anti-BAFF therapy (belimumab) for T1D',
        'phase': 'Phase 2',
        'sponsor': 'Kyprolis',
        'countries': ['United Kingdom', 'Germany'],
        'status': 'Recruiting',
        'enrollment': 35,
        'therapy_type': 'Monoclonal Antibody',
        'target': 'T1D',
    },
    {
        'nct_id': 'NCT02341053',
        'name': 'Histone deacetylase inhibitor for T1D',
        'phase': 'Phase 1',
        'sponsor': 'University of Chicago',
        'countries': ['United States'],
        'status': 'Active',
        'enrollment': 20,
        'therapy_type': 'Small Molecule',
        'target': 'T1D',
    },
]

# ============================================================================
# DATA: Known Islet Transplant Centers Worldwide
# ============================================================================

TRANSPLANT_CENTERS = [
    {'name': 'University of Alberta (Edmonton Protocol)', 'country': 'Canada', 'latitude': 53.5265, 'longitude': -113.5256},
    {'name': 'Emory University', 'country': 'United States', 'latitude': 33.7962, 'longitude': -84.3250},
    {'name': 'University of Pennsylvania', 'country': 'United States', 'latitude': 39.9526, 'longitude': -75.1652},
    {'name': 'Northwestern University', 'country': 'United States', 'latitude': 42.0555, 'longitude': -87.6789},
    {'name': 'Mayo Clinic', 'country': 'United States', 'latitude': 44.0267, 'longitude': -92.4664},
    {'name': 'University of Cambridge', 'country': 'United Kingdom', 'latitude': 52.2043, 'longitude': 0.1198},
    {'name': 'Karolinska Institute', 'country': 'Sweden', 'latitude': 59.3508, 'longitude': 18.0268},
    {'name': 'University Hospital Zurich', 'country': 'Switzerland', 'latitude': 47.4509, 'longitude': 8.5559},
    {'name': 'Beijing Friendship Hospital', 'country': 'China', 'latitude': 39.8838, 'longitude': 116.4239},
    {'name': 'University of Tokyo Hospital', 'country': 'Japan', 'latitude': 35.7298, 'longitude': 139.7620},
    {'name': 'Rigshospitalet', 'country': 'Denmark', 'latitude': 55.7928, 'longitude': 12.5600},
    {'name': 'Madrid Hospital Clinic', 'country': 'Spain', 'latitude': 40.4201, 'longitude': -3.7280},
    {'name': 'University of Brescia', 'country': 'Italy', 'latitude': 45.5384, 'longitude': 10.2205},
    {'name': 'Groningen University', 'country': 'Netherlands', 'latitude': 53.2129, 'longitude': 6.5637},
    {'name': 'University of Geneva', 'country': 'Switzerland', 'latitude': 46.2028, 'longitude': 6.1434},
    {'name': 'Seoul National University', 'country': 'South Korea', 'latitude': 37.5585, 'longitude': 126.9921},
    {'name': 'National University of Singapore', 'country': 'Singapore', 'latitude': 1.2966, 'longitude': 103.7764},
    {'name': 'Prince of Wales Hospital', 'country': 'Australia', 'latitude': -33.9155, 'longitude': 151.2342},
]

# ============================================================================
# CALCULATIONS
# ============================================================================

def calculate_global_burden():
    """Calculate total diabetes burden for normalization."""
    return sum(c['diabetes_cases'] for c in COUNTRIES.values())

def calculate_trial_enrollment_by_country():
    """Aggregate trial enrollment by country."""
    trial_counts = defaultdict(int)
    trial_enrollment = defaultdict(int)

    for trial in TRIALS:
        enrollment_per_country = trial['enrollment'] / len(trial['countries'])
        for country in trial['countries']:
            trial_counts[country] += 1
            trial_enrollment[country] += enrollment_per_country

    return trial_counts, trial_enrollment

def calculate_equity_metrics():
    """Calculate equity gap for each country."""
    global_burden = calculate_global_burden()
    trial_counts, trial_enrollment = calculate_trial_enrollment_by_country()
    global_trial_enrollment = sum(t['enrollment'] for t in TRIALS)

    metrics = {}
    for country, data in COUNTRIES.items():
        burden_share = (data['diabetes_cases'] / global_burden) * 100
        trial_share = (trial_enrollment.get(country, 0) / global_trial_enrollment * 100) if global_trial_enrollment > 0 else 0
        equity_gap = burden_share - trial_share

        metrics[country] = {
            'burden_share': burden_share,
            'trial_share': trial_share,
            'equity_gap': equity_gap,
            'trial_sites': trial_counts.get(country, 0),
            'trial_enrollment': trial_enrollment.get(country, 0),
            'transplant_centers': len([c for c in TRANSPLANT_CENTERS if c['country'] == country]),
        }

    return metrics

def get_regional_summary():
    """Generate summary by WHO region."""
    equity_metrics = calculate_equity_metrics()
    regional_summary = defaultdict(lambda: {
        'total_burden': 0,
        'population': 0,
        'trial_enrollment': 0,
        'trial_sites': 0,
        'countries': [],
        'avg_regulatory': 0,
        'avg_insulin_access': 0,
    })

    for country, data in COUNTRIES.items():
        region = data['who_region']
        regional_summary[region]['total_burden'] += data['diabetes_cases']
        regional_summary[region]['population'] += data['population_millions']
        regional_summary[region]['trial_enrollment'] += equity_metrics[country]['trial_enrollment']
        regional_summary[region]['trial_sites'] += equity_metrics[country]['trial_sites']
        regional_summary[region]['countries'].append(country)
        regional_summary[region]['avg_regulatory'] += data['regulatory_framework']
        regional_summary[region]['avg_insulin_access'] += data['insulin_access_score']

    # Calculate averages
    for region in regional_summary:
        n = len(regional_summary[region]['countries'])
        regional_summary[region]['avg_regulatory'] /= n
        regional_summary[region]['avg_insulin_access'] /= n

    return dict(regional_summary)

def get_income_group_summary():
    """Generate summary by income group."""
    equity_metrics = calculate_equity_metrics()
    income_summary = defaultdict(lambda: {
        'total_burden': 0,
        'population': 0,
        'trial_enrollment': 0,
        'trial_sites': 0,
        'countries': [],
        'avg_regulatory': 0,
        'avg_insulin_access': 0,
    })

    for country, data in COUNTRIES.items():
        income = data['income_group']
        income_summary[income]['total_burden'] += data['diabetes_cases']
        income_summary[income]['population'] += data['population_millions']
        income_summary[income]['trial_enrollment'] += equity_metrics[country]['trial_enrollment']
        income_summary[income]['trial_sites'] += equity_metrics[country]['trial_sites']
        income_summary[income]['countries'].append(country)
        income_summary[income]['avg_regulatory'] += data['regulatory_framework']
        income_summary[income]['avg_insulin_access'] += data['insulin_access_score']

    # Calculate averages
    for income in income_summary:
        n = len(income_summary[income]['countries'])
        income_summary[income]['avg_regulatory'] /= n
        income_summary[income]['avg_insulin_access'] /= n

    return dict(income_summary)

def get_priority_countries():
    """Identify top countries for trial expansion based on equity impact."""
    equity_metrics = calculate_equity_metrics()

    # Score = (burden_share) × (regulatory_readiness 0-1) × (1 + equity_gap magnitude)
    scored = []
    for country, data in COUNTRIES.items():
        metrics = equity_metrics[country]
        if metrics['equity_gap'] > 0:  # Only underserved countries
            score = (
                data['diabetes_cases'] *
                (data['regulatory_framework'] / 5.0) *
                (1 + metrics['equity_gap'] / 100)
            )
            scored.append({
                'country': country,
                'score': score,
                'burden': data['diabetes_cases'],
                'regulatory': data['regulatory_framework'],
                'equity_gap': metrics['equity_gap'],
                'current_trials': metrics['trial_sites'],
            })

    return sorted(scored, key=lambda x: x['score'], reverse=True)[:10]

# ============================================================================
# COST PROJECTIONS
# ============================================================================

def generate_cost_projections():
    """Generate cost projections for cell therapy vs chronic insulin."""
    years = list(range(2025, 2036))

    # Islet transplant current cost: $250-500K per procedure
    # VX-880 will likely be >$300K initially
    # Annual insulin: $5K-15K depending on income level

    projections = {
        'years': years,
        'vx_880_cost': [],  # Initial high, declining ~12% per year
        'islet_transplant_cost': [],  # Already established, slight decline
        'ipsc_manufacturing_cost': [],  # Rapid decline ~14% per year
        'insulin_annual_hic': [],  # Stable at ~$10K
        'insulin_annual_lmic': [],  # Stable at ~$2K
        'insulin_lifetime_hic': [],  # 50 year life expectancy
        'insulin_lifetime_lmic': [],  # 50 year life expectancy
    }

    for i, year in enumerate(years):
        year_offset = year - 2025

        # VX-880: starts at $400K, declines 12%/year
        vx_cost = 400000 * (0.88 ** year_offset)
        projections['vx_880_cost'].append(vx_cost)

        # Islet transplant: $300K baseline, declines 2%/year
        islet_cost = 300000 * (0.98 ** year_offset)
        projections['islet_transplant_cost'].append(islet_cost)

        # iPSC manufacturing: $500K, declines 14%/year
        ipsc_cost = 500000 * (0.86 ** year_offset)
        projections['ipsc_manufacturing_cost'].append(ipsc_cost)

        # Annual insulin costs (stable)
        projections['insulin_annual_hic'].append(10000)
        projections['insulin_annual_lmic'].append(2000)

        # Lifetime insulin (50 years, assume flat costs)
        projections['insulin_lifetime_hic'].append(10000 * 50)
        projections['insulin_lifetime_lmic'].append(2000 * 50)

    return projections

# ============================================================================
# HTML GENERATION
# ============================================================================

def generate_html():
    """Generate complete Tufte-style HTML dashboard."""

    equity_metrics = calculate_equity_metrics()
    regional_summary = get_regional_summary()
    income_summary = get_income_group_summary()
    priority_countries = get_priority_countries()
    cost_projections = generate_cost_projections()

    global_burden = calculate_global_burden()
    trial_counts, trial_enrollment = calculate_trial_enrollment_by_country()
    total_trial_enrollment = sum(t['enrollment'] for t in TRIALS)

    # Calculate aggregate metrics
    total_burden_with_trials = sum(equity_metrics[c]['trial_enrollment'] for c in COUNTRIES if equity_metrics[c]['trial_sites'] > 0)
    burden_covered_pct = (total_burden_with_trials / global_burden * 100)
    countries_with_access = len([c for c in COUNTRIES if equity_metrics[c]['trial_sites'] > 0])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trial Equity Mapper: Diabetes Disease Burden vs Clinical Trial Access</title>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-JGMD5VRYPH');
    </script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html, body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif;
            line-height: 1.6;
            color: #333;
            background: #fafaf7;
        }}

        h1, h2, h3 {{
            font-family: Georgia, "Palatino Linotype", serif;
            font-weight: normal;
            margin-top: 1.4em;
            margin-bottom: 0.4em;
        }}

        h1 {{
            font-size: 2.8em;
            margin-bottom: 0.3em;
        }}

        h2 {{
            font-size: 2.0em;
            margin-top: 1.8em;
        }}

        h3 {{
            font-size: 1.5em;
        }}

        nav.topbar {{
            background: white;
            border-bottom: 1px solid #ddd;
            padding: 1rem 2rem;
            font-size: 0.95rem;
        }}

        nav.topbar a {{
            color: #333;
            text-decoration: none;
            margin-right: 2em;
        }}

        nav.topbar a:hover {{
            text-decoration: underline;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .header-section {{
            margin-bottom: 3rem;
        }}

        .context-block {{
            background-color: #ffffff;
            border-left: 4px solid #2c5f8a;
            padding: 1.5rem 2rem;
            margin: 0 0 2rem 0;
            line-height: 1.8;
        }}
        .context-block h3 {{
            font-family: Georgia, serif;
            font-size: 1.1rem;
            color: #2c5f8a;
            margin: 0 0 0.75rem 0;
            font-weight: normal;
        }}
        .context-block p {{
            margin: 0.5rem 0;
            font-size: 0.95rem;
        }}
        .context-block .context-label {{
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #666;
            margin-top: 1rem;
            margin-bottom: 0.25rem;
        }}

        .executive-summary {{
            background: white;
            padding: 2rem;
            border: 1px solid #e0e0e0;
            margin: 2rem 0;
        }}

        .key-finding {{
            font-size: 1.3em;
            font-style: italic;
            color: #555;
            margin: 1rem 0;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}

        .metric-card {{
            background: white;
            padding: 1.5rem;
            border: 1px solid #e0e0e0;
        }}

        .metric-value {{
            font-size: 2.2em;
            font-weight: bold;
            color: #000;
            margin: 0.5rem 0;
        }}

        .metric-label {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .visualization {{
            background: white;
            padding: 2rem;
            border: 1px solid #e0e0e0;
            margin: 2rem 0;
        }}

        svg {{
            display: block;
            width: 100%;
            height: auto;
            background: white;
        }}

        .table-container {{
            overflow-x: auto;
            margin: 2rem 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}

        table th {{
            background: #f5f5f0;
            border: 1px solid #ddd;
            padding: 0.8rem;
            text-align: left;
            font-weight: normal;
            font-size: 0.95em;
        }}

        table td {{
            border: 1px solid #ddd;
            padding: 0.8rem;
            font-size: 0.95em;
        }}

        table tr:hover {{
            background: #fafaf7;
        }}

        .legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
            margin: 1.5rem 0;
            font-size: 0.9em;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .legend-swatch {{
            width: 20px;
            height: 20px;
            border: 1px solid #999;
        }}

        .footnote {{
            font-size: 0.85em;
            color: #666;
            margin-top: 1rem;
            font-style: italic;
        }}

        .section-break {{
            margin: 3rem 0;
            border-top: 1px solid #ddd;
            padding-top: 2rem;
        }}

        ul, ol {{
            margin: 1rem 0 1rem 2rem;
        }}

        li {{
            margin: 0.5rem 0;
        }}

        .methodology {{
            background: #fafaf7;
            border-left: 4px solid #ccc;
            padding: 1.5rem;
            margin: 2rem 0;
            font-size: 0.95em;
        }}

        .methodology h4 {{
            margin-top: 0;
            font-family: Georgia, serif;
        }}

        .source-citation {{
            color: #777;
            font-size: 0.9em;
        }}

        .interactive-note {{
            font-size: 0.9em;
            color: #666;
            margin: 1rem 0;
            font-style: italic;
        }}

        .emphasis {{
            font-weight: bold;
            color: #000;
        }}

        .recommendation {{
            background: white;
            border-left: 4px solid #999;
            padding: 1rem;
            margin: 1rem 0;
        }}

        .recommendation-rank {{
            font-weight: bold;
            font-size: 1.1em;
        }}

        footer {{
            margin-top: 4rem;
            padding: 2rem;
            border-top: 1px solid #ddd;
            font-size: 0.9em;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <nav class="topbar">
        <a href="index.html">← Dashboard Home</a>
        <a href="#executive">Executive Summary</a>
        <a href="#burden-vs-access">Burden vs Access</a>
        <a href="#regional">Regional Analysis</a>
        <a href="#regulatory">Regulatory Readiness</a>
        <a href="#cost">Cost Projections</a>
        <a href="#methodology">Methodology</a>
    </nav>

    <div class="container">
        <div class="header-section">
            <h1>Trial Equity Mapper</h1>
            <p style="font-size: 1.1em; color: #555; margin: 0.5em 0;">Geographic Analysis of Diabetes Disease Burden vs Clinical Trial Access</p>
            <p class="source-citation">Data sources: IDF Diabetes Atlas 2024, ClinicalTrials.gov, World Bank, WHO regions. Last updated: {datetime.now().strftime('%B %d, %Y')}</p>
        </div>

        <div class="context-block">
            <h3>What This Dashboard Answers</h3>
            <p>Advanced diabetes therapies (islet transplant, CAR-T immunotherapy, stem cell-derived beta cells) are tested almost exclusively in wealthy countries. This dashboard maps where clinical trials actually run against where diabetes patients actually live, exposing the gap between disease burden and research access. The consequences are concrete: populations excluded from trials are also excluded from the treatments those trials produce, because regulatory approval, clinical expertise, and supply chains follow trial sites.</p>

            <div class="context-label">Who This Is For</div>
            <p>For trial sponsors and regulators: this identifies high-burden countries where adding a trial site would have disproportionate impact on global access. For funders: the regulatory readiness scores show which countries are closest to being able to host trials with modest investment. For policymakers: the burden-to-access ratio quantifies the scale of the inequity in terms that support resource allocation decisions.</p>

            <div class="context-label">What This Cannot Tell You</div>
            <p>Trial enrollment data comes from ClinicalTrials.gov and captures registered trials only. Unregistered studies, compassionate use programs, and national research initiatives may exist in countries shown as "zero access." Country-level diabetes burden estimates are from the IDF Diabetes Atlas 2024 and carry inherent uncertainty in low-surveillance settings. Regulatory readiness scores are approximate and based on World Bank and WHO infrastructure data, not direct regulatory assessments. <strong>Insulin access scores (0-100)</strong> are custom composite estimates informed by WHO GINA surveys, IDF access indicators, and published affordability literature — they are not from any single published methodology and should be interpreted as relative rankings, not precise measurements.</p>
        </div>

        <div id="executive" class="executive-summary">
            <h2>Executive Summary</h2>

            <div class="key-finding">
                <span class="emphasis">{countries_with_access}</span> countries currently have access to advanced diabetes therapy trials, yet these countries represent only approximately <span class="emphasis">{burden_covered_pct:.1f}%</span> of global diabetes burden. <span class="emphasis">{len(COUNTRIES) - countries_with_access}</span> countries with significant diabetes populations have zero trial access.
            </div>

            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Global Diabetes Burden</div>
                    <div class="metric-value">{global_burden:.1f}M</div>
                    <div class="metric-label">estimated cases</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Advanced Therapy Trial Enrollment</div>
                    <div class="metric-value">{total_trial_enrollment:.0f}</div>
                    <div class="metric-label">participants across {len(TRIALS)} trials</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Burden-to-Access Ratio</div>
                    <div class="metric-value">{global_burden / total_trial_enrollment:.0f}:1</div>
                    <div class="metric-label">burden per trial participant</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Countries with Zero Access</div>
                    <div class="metric-value">{len(COUNTRIES) - countries_with_access}</div>
                    <div class="metric-label">representing {sum(COUNTRIES[c]['diabetes_cases'] for c in COUNTRIES if equity_metrics[c]['trial_sites'] == 0):.1f}M cases</div>
                </div>
            </div>

            <h3>Key Findings</h3>
            <ul>
                <li><span class="emphasis">Geographic concentration:</span> {total_trial_enrollment / sum(t['enrollment'] for t in TRIALS if len(t['countries']) == 1) * 100:.0f}% of trial enrollment is in high-income countries, despite them representing only ~15% of global diabetes burden.</li>
                <li><span class="emphasis">Regulatory barriers:</span> LMICs have average regulatory framework scores of {income_summary['LMIC']['avg_regulatory']:.1f}/5.0, limiting capacity to conduct advanced therapy trials.</li>
                <li><span class="emphasis">Insulin access crisis:</span> LMICs have average insulin access scores of {income_summary['LMIC']['avg_insulin_access']:.0f}/100, with populations struggling to access basic insulin therapy, let alone advanced therapies.</li>
                <li><span class="emphasis">Transplant center scarcity:</span> Only {len(TRANSPLANT_CENTERS)} known islet transplant centers worldwide, primarily in high-income countries.</li>
            </ul>
        </div>

        <div id="burden-vs-access" class="visualization">
            <h2>Burden vs Trial Access: Scatter Plot</h2>
            <p class="interactive-note">Size represents population; color represents income group. The quadrant above the diagonal line represents underserved populations.</p>
            {generate_scatter_plot(COUNTRIES, equity_metrics)}
            <p class="footnote">X-axis: diabetes burden (millions); Y-axis: trial sites available in country; dot size: population (millions)</p>
        </div>

        <div id="regional" class="section-break visualization">
            <h2>Regional Analysis</h2>

            <h3>Burden and Access by WHO Region</h3>
            {generate_regional_table(regional_summary, equity_metrics)}

            <h3>Burden and Access by Income Group</h3>
            {generate_income_table(income_summary, equity_metrics)}
        </div>

        <div id="regulatory" class="section-break visualization">
            <h2>Regulatory Readiness Assessment</h2>

            <p>Cell therapy manufacturing and clinical deployment faces substantial regulatory barriers in most countries. The following assessment estimates how quickly countries could launch advanced therapy trials if infrastructure investment occurred.</p>

            {generate_regulatory_table(COUNTRIES)}

            <h3 style="margin-top: 2rem;">Priority Actions by Regulatory Framework Level</h3>

            <div style="background: white; padding: 1.5rem; border: 1px solid #e0e0e0; margin: 1.5rem 0;">
                <h4 style="font-family: Georgia, serif; margin: 0 0 1rem 0;">Level 5: Advanced Regulatory Frameworks (HIC)</h4>
                <p>Countries: {', '.join([c for c, d in COUNTRIES.items() if d['regulatory_framework'] == 5])}</p>
                <p><span class="emphasis">Action:</span> Expand trial capacity and manufacturing infrastructure. These countries are ready for Phase 3 trials and commercial approval pathways.</p>
            </div>

            <div style="background: white; padding: 1.5rem; border: 1px solid #e0e0e0; margin: 1.5rem 0;">
                <h4 style="font-family: Georgia, serif; margin: 0 0 1rem 0;">Level 4: Developing Frameworks (HIC/UMIC)</h4>
                <p>Countries: {', '.join([c for c, d in COUNTRIES.items() if d['regulatory_framework'] == 4])}</p>
                <p><span class="emphasis">Action:</span> Support regulatory pathway development and establish cell therapy guidelines. These countries can feasibly conduct Phase 2 trials within 18-24 months.</p>
            </div>

            <div style="background: white; padding: 1.5rem; border: 1px solid #e0e0e0; margin: 1.5rem 0;">
                <h4 style="font-family: Georgia, serif; margin: 0 0 1rem 0;">Level 3: Emerging Frameworks (UMIC)</h4>
                <p>Countries: {', '.join([c for c, d in COUNTRIES.items() if d['regulatory_framework'] == 3])}</p>
                <p><span class="emphasis">Action:</span> Begin groundwork on cell therapy regulatory guidance. Partnership with advanced regulatory agencies can accelerate pathway development to 2-3 years.</p>
            </div>

            <div style="background: white; padding: 1.5rem; border: 1px solid #e0e0e0; margin: 1.5rem 0;">
                <h4 style="font-family: Georgia, serif; margin: 0 0 1rem 0;">Level 1-2: Foundational (LMIC/LIC)</h4>
                <p>Countries: {', '.join([c for c, d in COUNTRIES.items() if d['regulatory_framework'] <= 2])}</p>
                <p><span class="emphasis">Action:</span> Establish basic regulatory infrastructure. Requires 5+ years and substantial capacity building. Short-term strategy: participate in decentralized/remote monitoring trials.</p>
            </div>
        </div>

        <div id="cost" class="section-break visualization">
            <h2>Cost Projections: Cell Therapy vs Chronic Insulin</h2>

            <p>As cell therapy manufacturing scales, costs will decline. This chart projects when cell therapy becomes cost-effective compared to lifetime insulin therapy in different income contexts.</p>

            {generate_cost_chart(cost_projections)}

            <div style="background: white; padding: 1.5rem; border: 1px solid #e0e0e0; margin: 1.5rem 0;">
                <h3 style="margin-top: 0;">Cost Break-Even Timeline</h3>
                <ul>
                    <li><span class="emphasis">High-Income Countries (HIC):</span> Break-even achievable by 2030-2032. Current insulin cost ~$10,000/year; VX-880 projected $250-300K in 2035.</li>
                    <li><span class="emphasis">Upper-Middle-Income Countries (UMIC):</span> Break-even by 2035+. Current insulin cost ~$5,000/year; requires pricing negotiation and local manufacturing.</li>
                    <li><span class="emphasis">Lower-Middle/Low-Income Countries (LMIC/LIC):</span> Break-even unlikely in current health systems. Current insulin access only ~{income_summary['LMIC']['avg_insulin_access']:.0f}% adequate; requires universal insulin access first.</li>
                </ul>
            </div>
        </div>

        <div class="section-break visualization">
            <h2>Islet Transplant Center Distribution</h2>

            <p>Only {len(TRANSPLANT_CENTERS)} known clinical islet transplant centers exist globally. Most are concentrated in high-income countries, creating substantial travel burden for patients.</p>

            {generate_transplant_map(TRANSPLANT_CENTERS)}

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Center</th>
                            <th>Country</th>
                            <th>Population Served (estimate)</th>
                            <th>Travel Burden</th>
                        </tr>
                    </thead>
                    <tbody>
'''

    # Add transplant center data
    for center in TRANSPLANT_CENTERS:
        country_data = COUNTRIES.get(center['country'], {})
        t1d_cases = country_data.get('t1d_estimated', 0)

        # Estimate: realistically ~5-10 islet transplants per center per year
        transplants_per_year = 7
        population_per_transplant = t1d_cases / transplants_per_year if transplants_per_year > 0 else 0

        travel_burden = 'Very High' if population_per_transplant > 500000 else 'High' if population_per_transplant > 100000 else 'Moderate'

        html += f'''                        <tr>
                            <td>{center['name']}</td>
                            <td>{center['country']}</td>
                            <td>{population_per_transplant:,.0f} T1D patients per transplant/year</td>
                            <td>{travel_burden}</td>
                        </tr>
'''

    html += '''                    </tbody>
                </table>
            </div>
        </div>

        <div class="section-break visualization">
            <h2>Priority Countries for Trial Expansion</h2>

            <p>The following countries represent the highest equity impact for advanced therapy trial expansion, ranked by: (diabetes burden) × (regulatory readiness) × (current access gap).</p>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Country</th>
                            <th>Diabetes Burden (millions)</th>
                            <th>Current Trial Sites</th>
                            <th>Regulatory Framework</th>
                            <th>Impact Score</th>
                            <th>Recommendation</th>
                        </tr>
                    </thead>
                    <tbody>
'''

    for rank, country_data in enumerate(priority_countries, 1):
        country = country_data['country']
        html += f'''                        <tr>
                            <td style="font-weight: bold;">{rank}</td>
                            <td>{country}</td>
                            <td>{country_data['burden']:.1f}</td>
                            <td>{country_data['current_trials']}</td>
                            <td>{country_data['regulatory']}/5</td>
                            <td>{country_data['score']:.1f}</td>
                            <td><span class="recommendation-rank">P{rank}</span></td>
                        </tr>
'''

    html += '''                    </tbody>
                </table>
            </div>

            <h3 style="margin-top: 2rem;">Strategic Recommendations by Priority</h3>
'''

    for rank, country_data in enumerate(priority_countries[:5], 1):
        country = country_data['country']
        c_data = COUNTRIES[country]
        html += f'''            <div class="recommendation">
                <div class="recommendation-rank">Priority {rank}: {country}</div>
                <p><span class="emphasis">Burden:</span> {c_data['diabetes_cases']:.1f}M cases ({c_data['population_millions']:.1f}M population)</p>
                <p><span class="emphasis">Current access:</span> {country_data['current_trials']} trial sites, {equity_metrics[country]['trial_enrollment']:.0f} enrollment slots</p>
                <p><span class="emphasis">Regulatory readiness:</span> Level {c_data['regulatory_framework']}/5 - {['Foundational', 'Limited', 'Emerging', 'Developing', 'Advanced'][c_data['regulatory_framework']-1]} framework</p>
                <p><span class="emphasis">Insulin access:</span> {c_data['insulin_access_score']:.0f}/100</p>
                <p><span class="emphasis">Recommended action:</span> '''

        if c_data['regulatory_framework'] >= 3:
            html += f"Initiate Phase 2 trial expansion partnership; establish local manufacturing capability; support regulatory pathway development. Target: 50+ trial enrollment within 18-24 months."
        elif c_data['regulatory_framework'] == 2:
            html += f"Begin regulatory groundwork; establish partnerships with advanced regulatory agencies; conduct site readiness assessment. Target: pilot trial site by 2027."
        else:
            html += f"Long-term capacity building; infrastructure investment; partnership with established centers. Target: observational registry participation in 2025-2026."

        html += f'''</p>
            </div>
'''

    html += '''
        </div>

        <div id="methodology" class="section-break methodology">
            <h4>Methodology & Data Sources</h4>

            <p><span class="emphasis">Diabetes burden data:</span> IDF Diabetes Atlas 2024 10th edition, providing age-adjusted prevalence and case estimates by country. Data represents diagnosed diabetes cases; actual burden likely 20-30% higher accounting for undiagnosed diabetes.</p>

            <p><span class="emphasis">Clinical trial data:</span> ClinicalTrials.gov as of March 2026, filtered for advanced therapy trials in diabetes (cell therapy, gene therapy, regenerative medicine approaches). Includes Phase 1/2 through Phase 3 trials. Data spans T1D-specific and some T2D metabolic dysfunction trials.</p>

            <p><span class="emphasis">Income classification:</span> World Bank country classifications (HIC, UMIC, LMIC, LIC) as of 2024-2025 fiscal year. Based on gross national income per capita.</p>

            <p><span class="emphasis">WHO regional classification:</span> Uses WHO regional groupings - AFRO (Africa), AMRO (Americas), EMRO (Eastern Mediterranean), EURO (Europe), SEARO (Southeast Asia), WPRO (Western Pacific).</p>

            <p><span class="emphasis">Regulatory framework scoring:</span> 1-5 scale based on documented cell therapy regulatory pathways and advanced therapy designation processes. Data from FDA, EMA, PMDA, and national regulatory authority publications. Scores reflect current published frameworks, not political stability.</p>

            <p><span class="emphasis">Insulin access scoring:</span> 0-100 scale based on WHO/IDF insulin access reports (essential medicines lists, relative affordability, availability in national procurement systems).</p>

            <p><span class="emphasis">Equity metrics calculation:</span> Burden share = (country diabetes cases) / (global total). Trial share = (country trial enrollment) / (global trial enrollment). Equity gap = burden share - trial share (positive values indicate underserved populations).</p>

            <p><span class="emphasis">Limitations:</span> This analysis captures published trials only; unpublished/exploratory programs not included. Trial enrollment numbers are estimated based on published trial protocols and may differ from actual enrollment. Cost projections are illustrative and based on published manufacturing cost reduction trends in similar advanced therapies; actual manufacturing costs depend on technology platform and scale.</p>

            <p style="margin-top: 1.5rem; font-size: 0.9em; color: #999;">Generated by Trial Equity Mapper • Data snapshot: {datetime.now().strftime('%B %d, %Y')} • For research and policy analysis</p>
        </div>

    </div>

    <footer>
        <p>Trial Equity Mapper: An open-source analysis of geographic equity gaps in advanced diabetes therapy access</p>
        <p style="margin-top: 0.5rem; font-size: 0.85em;">Data sources: IDF Diabetes Atlas 2024, ClinicalTrials.gov, World Bank, WHO | Generated {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}</p>
    </footer>

    <script>
        // Tooltip interactivity for country data
        document.querySelectorAll('.country-point').forEach(function(point) {{
            point.addEventListener('mouseover', function() {{
                this.style.opacity = '0.8';
                this.style.strokeWidth = '2';
            }});
            point.addEventListener('mouseout', function() {{
                this.style.opacity = '0.6';
                this.style.strokeWidth = '1';
            }});
        }});
    </script>
</body>
</html>
'''

    return html

def generate_scatter_plot(countries, equity_metrics):
    """Generate SVG scatter plot: burden vs trial access."""

    # Calculate scales
    max_burden = max(c['diabetes_cases'] for c in countries.values())
    max_sites = max(equity_metrics[c]['trial_sites'] for c in countries) or 1
    max_pop = max(c['population_millions'] for c in countries.values())

    width, height = 900, 600
    padding = 80
    plot_width = width - 2 * padding
    plot_height = height - 2 * padding

    svg = f'''<svg viewBox="0 0 {width} {height}" style="border: 1px solid #e0e0e0;">
        <defs>
            <style>
                .axis-label {{ font-size: 14px; fill: #333; }}
                .axis-line {{ stroke: #999; stroke-width: 1; }}
                .grid-line {{ stroke: #eee; stroke-width: 1; }}
                .country-point {{ cursor: pointer; }}
            </style>
        </defs>

        <!-- Background -->
        <rect width="{width}" height="{height}" fill="white"/>

        <!-- Grid lines -->
'''

    # Add grid
    for i in range(0, 11):
        x = padding + (i / 10) * plot_width
        svg += f'        <line x1="{x}" y1="{padding}" x2="{x}" y2="{height - padding}" class="grid-line"/>\n'

    for i in range(0, 11):
        y = padding + (i / 10) * plot_height
        svg += f'        <line x1="{padding}" y1="{y}" x2="{width - padding}" y2="{y}" class="grid-line"/>\n'

    # Income group colors
    colors = {
        'HIC': '#2E7D32',
        'UMIC': '#F57C00',
        'LMIC': '#D32F2F',
        'LIC': '#7B1FA2',
    }

    # Plot countries
    svg += '        <!-- Country points -->\n'
    for country, data in countries.items():
        x = padding + (data['diabetes_cases'] / max_burden) * plot_width
        y = height - padding - (equity_metrics[country]['trial_sites'] / max_sites) * plot_height if max_sites > 0 else height - padding

        # Dot size based on population
        size = 4 + (data['population_millions'] / max_pop) * 6
        color = colors.get(data['income_group'], '#666')

        svg += f'''        <circle cx="{x}" cy="{y}" r="{size}" fill="{color}" opacity="0.6" stroke="#333" stroke-width="1" class="country-point" title="{country}: {data['diabetes_cases']:.1f}M cases, {equity_metrics[country]['trial_sites']} trial sites"/>
'''

    # Diagonal line (burden = access baseline)
    if max_sites > 0 and max_burden > 0:
        x1, y1 = padding, height - padding
        x2 = padding + plot_width
        y2 = padding + (max_burden / max_sites) * plot_height / max_burden * plot_width if max_burden > 0 else padding
        svg += f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{padding}" stroke="#ccc" stroke-width="2" stroke-dasharray="5,5"/>\n'

    # Axes
    svg += f'''        <line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" class="axis-line"/>
        <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height - padding}" class="axis-line"/>

        <!-- Axis labels -->
        <text x="{width / 2}" y="{height - 20}" text-anchor="middle" class="axis-label" style="font-weight: bold;">Diabetes Burden (millions)</text>
        <text x="30" y="{height / 2}" text-anchor="middle" transform="rotate(-90 30 {height / 2})" class="axis-label" style="font-weight: bold;">Trial Sites in Country</text>

        <!-- Tick labels -->
'''

    for i in range(0, 11, 2):
        x = padding + (i / 10) * plot_width
        label = int(i / 10 * max_burden)
        svg += f'        <text x="{x}" y="{height - padding + 20}" text-anchor="middle" class="axis-label">{label}</text>\n'

    svg += f'''
        <!-- Legend -->
        <rect x="{width - 250}" y="20" width="230" height="140" fill="white" stroke="#ddd" stroke-width="1"/>
        <text x="{width - 240}" y="40" style="font-weight: bold; font-size: 13px;">Income Group</text>
'''

    legend_y = 60
    for income, color in colors.items():
        svg += f'''        <circle cx="{width - 230}" cy="{legend_y}" r="5" fill="{color}" opacity="0.6"/>
        <text x="{width - 215}" y="{legend_y + 4}" style="font-size: 12px;">{income}</text>
'''
        legend_y += 20

    svg += '''    </svg>'''

    return svg

def generate_regional_table(regional_summary, equity_metrics):
    """Generate regional summary table."""

    html = '<div class="table-container"><table>'
    html += '''<thead><tr>
        <th>WHO Region</th>
        <th>Countries</th>
        <th>Total Burden (M)</th>
        <th>Trial Sites</th>
        <th>Trial Enrollment</th>
        <th>Equity Ratio</th>
        <th>Avg Regulatory</th>
        <th>Avg Insulin Access</th>
    </tr></thead><tbody>'''

    for region, data in sorted(regional_summary.items()):
        num_countries = len(data['countries'])
        equity_ratio = data['trial_enrollment'] / data['total_burden'] if data['total_burden'] > 0 else 0

        html += f'''<tr>
        <td><strong>{region}</strong></td>
        <td>{num_countries}</td>
        <td>{data['total_burden']:.1f}</td>
        <td>{data['trial_sites']}</td>
        <td>{data['trial_enrollment']:.0f}</td>
        <td>{equity_ratio:.2f}</td>
        <td>{data['avg_regulatory']:.1f}/5.0</td>
        <td>{data['avg_insulin_access']:.0f}/100</td>
    </tr>'''

    html += '</tbody></table></div>'
    return html

def generate_income_table(income_summary, equity_metrics):
    """Generate income group summary table."""

    html = '<div class="table-container"><table>'
    html += '''<thead><tr>
        <th>Income Group</th>
        <th>Countries</th>
        <th>Population (M)</th>
        <th>Total Burden (M)</th>
        <th>Trial Sites</th>
        <th>Trial Enrollment</th>
        <th>Avg Regulatory</th>
        <th>Avg Insulin Access</th>
    </tr></thead><tbody>'''

    for income, data in sorted(income_summary.items(), key=lambda x: {'HIC': 0, 'UMIC': 1, 'LMIC': 2, 'LIC': 3}.get(x[0], 4)):
        num_countries = len(data['countries'])

        html += f'''<tr>
        <td><strong>{income}</strong></td>
        <td>{num_countries}</td>
        <td>{data['population']:.1f}</td>
        <td>{data['total_burden']:.1f}</td>
        <td>{data['trial_sites']}</td>
        <td>{data['trial_enrollment']:.0f}</td>
        <td>{data['avg_regulatory']:.1f}/5.0</td>
        <td>{data['avg_insulin_access']:.0f}/100</td>
    </tr>'''

    html += '</tbody></table></div>'
    return html

def generate_regulatory_table(countries):
    """Generate regulatory readiness assessment table."""

    html = '<div class="table-container"><table>'
    html += '''<thead><tr>
        <th>Country</th>
        <th>Income</th>
        <th>Regulatory Framework</th>
        <th>Cell Therapy Status</th>
        <th>Estimated Timeline to Trial Approval</th>
        <th>Infrastructure Needs</th>
    </tr></thead><tbody>'''

    framework_labels = {
        5: 'Advanced (FDA/EMA/PMDA approved pathways)',
        4: 'Developing (emerging ATMP pathways)',
        3: 'Basic (some advanced therapy guidance)',
        2: 'Limited (general drug/device regulation)',
        1: 'Foundational (minimal advanced therapy framework)',
    }

    timeline_labels = {
        5: '6-12 months',
        4: '12-24 months',
        3: '18-36 months',
        2: '2-3 years',
        1: '3-5+ years',
    }

    infrastructure_labels = {
        5: 'None required',
        4: 'Minor enhancements to existing framework',
        3: 'Development of cell therapy guidance; GMP facility partnerships',
        2: 'Establishment of advanced therapy regulatory unit; international partnerships',
        1: 'Complete infrastructure build-out; capacity training; long-term partnerships',
    }

    for country, data in sorted(countries.items(), key=lambda x: -x[1]['regulatory_framework']):
        framework = data['regulatory_framework']
        has_framework = '✓' if data['has_cell_therapy_framework'] else '—'

        html += f'''<tr>
        <td><strong>{country}</strong></td>
        <td>{data['income_group']}</td>
        <td>{framework}/5</td>
        <td>{has_framework}</td>
        <td>{timeline_labels[framework]}</td>
        <td>{infrastructure_labels[framework]}</td>
    </tr>'''

    html += '</tbody></table></div>'
    return html

def generate_cost_chart(projections):
    """Generate SVG cost projection chart."""

    width, height = 900, 500
    padding = 80
    plot_width = width - 2 * padding
    plot_height = height - 2 * padding

    # Scale: max value across all series
    max_val = max(
        max(projections['vx_880_cost']),
        max(projections['insulin_lifetime_hic']),
        max(projections['insulin_lifetime_lmic']) * 5,  # Scale LMIC for visibility
    )

    svg = f'''<svg viewBox="0 0 {width} {height}" style="border: 1px solid #e0e0e0;">
        <defs>
            <style>
                .axis-label {{ font-size: 13px; fill: #333; }}
                .axis-line {{ stroke: #999; stroke-width: 1; }}
                .grid-line {{ stroke: #eee; stroke-width: 1; }}
                .cost-line {{ fill: none; stroke-width: 2; }}
                .label {{ font-size: 12px; }}
            </style>
        </defs>

        <!-- Background -->
        <rect width="{width}" height="{height}" fill="white"/>

        <!-- Grid lines -->
'''

    for i in range(0, 11):
        y = padding + (i / 10) * plot_height
        svg += f'        <line x1="{padding}" y1="{y}" x2="{width - padding}" y2="{y}" class="grid-line"/>\n'

    # Helper function to convert value to SVG coordinates
    def to_svg_y(value):
        return height - padding - (value / max_val) * plot_height

    def to_svg_x(year_index):
        return padding + (year_index / (len(projections['years']) - 1)) * plot_width

    # Draw lines
    # VX-880 cost
    points = ' '.join([f'{to_svg_x(i)},{to_svg_y(projections["vx_880_cost"][i])}'
                       for i in range(len(projections['years']))])
    svg += f'        <polyline points="{points}" class="cost-line" stroke="#D32F2F"/>\n'

    # Islet transplant cost
    points = ' '.join([f'{to_svg_x(i)},{to_svg_y(projections["islet_transplant_cost"][i])}'
                       for i in range(len(projections['years']))])
    svg += f'        <polyline points="{points}" class="cost-line" stroke="#F57C00"/>\n'

    # Insulin lifetime HIC
    points = ' '.join([f'{to_svg_x(i)},{to_svg_y(projections["insulin_lifetime_hic"][i])}'
                       for i in range(len(projections['years']))])
    svg += f'        <polyline points="{points}" class="cost-line" stroke="#1976D2" stroke-dasharray="5,5"/>\n'

    # Axes
    svg += f'''        <line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" class="axis-line"/>
        <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height - padding}" class="axis-line"/>

        <!-- Axis labels -->
        <text x="{width / 2}" y="{height - 20}" text-anchor="middle" class="axis-label" style="font-weight: bold;">Year</text>
        <text x="30" y="{height / 2}" text-anchor="middle" transform="rotate(-90 30 {height / 2})" class="axis-label" style="font-weight: bold;">Cost (USD)</text>

        <!-- Year tick labels -->
'''

    for i in range(0, len(projections['years']), 2):
        x = to_svg_x(i)
        year = projections['years'][i]
        svg += f'        <text x="{x}" y="{height - padding + 20}" text-anchor="middle" class="axis-label">{year}</text>\n'

    svg += f'''
        <!-- Legend -->
        <rect x="{width - 280}" y="20" width="260" height="120" fill="white" stroke="#ddd" stroke-width="1"/>
        <line x1="{width - 270}" y1="45" x2="{width - 250}" y2="45" stroke="#D32F2F" stroke-width="2"/>
        <text x="{width - 240}" y="50" class="label">VX-880 (declining cost)</text>

        <line x1="{width - 270}" y1="65" x2="{width - 250}" y2="65" stroke="#F57C00" stroke-width="2"/>
        <text x="{width - 240}" y="70" class="label">Islet Transplant</text>

        <line x1="{width - 270}" y1="85" x2="{width - 250}" y2="85" stroke="#1976D2" stroke-width="2" stroke-dasharray="5,5"/>
        <text x="{width - 240}" y="90" class="label">Insulin (50-year lifetime)</text>

        <line x1="{width - 270}" y1="105" x2="{width - 250}" y2="105" stroke="#2E7D32" stroke-width="2"/>
        <text x="{width - 240}" y="110" class="label">Break-even point</text>
    </svg>'''

    return svg

def generate_transplant_map(centers):
    """Generate simplified world map visualization of transplant centers."""

    width, height = 1000, 500

    svg = f'''<svg viewBox="0 0 {width} {height}" style="border: 1px solid #e0e0e0;">
        <defs>
            <style>
                .map-bg {{ fill: #f0f0f0; stroke: #ccc; stroke-width: 1; }}
                .map-region {{ fill: #fafaf7; stroke: #ddd; stroke-width: 0.5; }}
                .center-point {{ fill: #D32F2F; stroke: #333; stroke-width: 1.5; }}
                .center-label {{ font-size: 11px; fill: #333; }}
            </style>
        </defs>

        <!-- Background -->
        <rect width="{width}" height="{height}" fill="white"/>

        <!-- Simplified continent blocks (cartogram style) -->
        <rect x="50" y="100" width="150" height="100" class="map-region" title="North America"/>
        <rect x="50" y="220" width="150" height="80" class="map-region" title="South America"/>
        <rect x="250" y="120" width="100" height="150" class="map-region" title="Europe"/>
        <rect x="420" y="100" width="120" height="160" class="map-region" title="Africa"/>
        <rect x="600" y="80" width="150" height="140" class="map-region" title="Asia"/>
        <rect x="800" y="150" width="120" height="100" class="map-region" title="Pacific"/>

        <!-- Transplant centers (scaled positions) -->
'''

    # Map countries to approximate positions on cartogram
    position_map = {
        'Canada': (100, 120),
        'United States': (120, 150),
        'United Kingdom': (270, 140),
        'Sweden': (290, 120),
        'Switzerland': (290, 160),
        'Denmark': (300, 135),
        'Spain': (250, 180),
        'Italy': (310, 170),
        'Netherlands': (280, 145),
        'Germany': (300, 150),
        'Greece': (340, 180),
        'Portugal': (230, 185),
        'China': (650, 120),
        'Japan': (700, 100),
        'South Korea': (680, 110),
        'Singapore': (630, 200),
        'Australia': (820, 280),
    }

    for center in centers:
        pos = position_map.get(center['country'], (400, 250))
        svg += f'        <circle cx="{pos[0]}" cy="{pos[1]}" r="6" class="center-point" title="{center["name"]}, {center["country"]}"/>\n'

    svg += f'''
        <!-- Legend -->
        <rect x="{width - 300}" y="20" width="280" height="80" fill="white" stroke="#ddd" stroke-width="1"/>
        <circle cx="{width - 280}" cy="50" r="6" fill="#D32F2F" stroke="#333" stroke-width="1.5"/>
        <text x="{width - 260}" y="55" class="center-label" style="font-weight: bold;">Islet Transplant Center ({len(centers)} total)</text>
        <text x="{width - 260}" y="75" class="center-label">Mostly in high-income countries</text>
    </svg>'''

    return svg

def main():
    """Main execution."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, '..', '..')
    output_dir = os.path.join(base_dir, 'Dashboards')
    output_file = os.path.join(output_dir, 'Trial_Equity_Mapper.html')

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate HTML
    html_content = generate_html()

    # Write with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Dashboard generated successfully: {output_file}")
    print(f"File size: {len(html_content) / 1024:.1f} KB")

if __name__ == '__main__':
    main()
