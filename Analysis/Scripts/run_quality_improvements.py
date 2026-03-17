#!/usr/bin/env python3
"""
Master runner for all quality improvements.

Runs all improvement scripts in order:
  1. rebuild_clinical_trial_dashboard.py — Tufte-style trial dashboard
  2. rebuild_research_dashboard.py — Tufte-style research dashboard
  3. improve_gap_analysis.py — Interpreted gap classifications
  4. add_citations.py — Source citations for Research Findings Summary
  5. rebuild_website.py — Tufte-style GitHub Pages site

Usage:
  python run_quality_improvements.py           # Run all
  python run_quality_improvements.py --dashboard   # Trial dashboard only
  python run_quality_improvements.py --research    # Research dashboard only
  python run_quality_improvements.py --gaps        # Gap analysis only
  python run_quality_improvements.py --citations   # Citations only
  python run_quality_improvements.py --website     # Website only
"""

import subprocess
import sys
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = {
    'dashboard': ('rebuild_clinical_trial_dashboard.py', 'Rebuilding Clinical Trial Dashboard (Tufte style)'),
    'research': ('rebuild_research_dashboard.py', 'Rebuilding Research Dashboard (Tufte style)'),
    'gaps': ('improve_gap_analysis.py', 'Improving Literature Gap Analysis (interpretive classifications)'),
    'synthesis': ('build_gap_synthesis.py', 'Building Gap Synthesis Dashboard (scientific method framework)'),
    'equity': ('build_equity_map.py', 'Building Beta Cell Therapy Equity Analysis'),
    'deepdives': ('build_gap_deep_dives.py', 'Building Gap Deep Dives (all 15 gaps)'),
    'acronyms': ('build_acronym_db.py', 'Building Acronym & Abbreviation Database'),
    'dictionary': ('build_data_dictionary.py', 'Building Medical Data Dictionary (100 terms, cited)'),
    'lada': ('build_lada_model.py', 'Building LADA Natural History Model (Gap #1 GOLD)'),
    'islet': ('build_islet_outcomes.py', 'Building Islet Transplant Outcomes Analysis (Gap #3 GOLD)'),
    'drugrepurpose': ('build_drug_repurposing_islet.py', 'Building Drug Repurposing for Islet Transplant (Gap #4 SILVER)'),
    'immunomod': ('build_immunomod_lada.py', 'Building Immunomodulatory Drugs for LADA (Gap #8 SILVER)'),
    'treg': ('build_treg_neuropathy.py', 'Building Treg in Diabetic Neuropathy (Gap #5 SILVER)'),
    'cartaccess': ('build_cart_access.py', 'Building CAR-T Access Barriers Analysis (Gap #6 SILVER)'),
    'gka': ('build_gka_landscape.py', 'Building GKA Drug Repurposing Landscape (Gap #7 SILVER)'),
    'isletequity': ('build_islet_equity.py', 'Building Islet Transplant Registry Equity (Gap #11 SILVER)'),
    'genericdrug': ('build_generic_drug_catalog.py', 'Building Generic Drug x Diabetes Mechanism Catalog (Gap #12 SILVER)'),
    'gkalada': ('build_gka_lada.py', 'Building GKA in LADA Analysis (Gap #9 EXPLORATORY)'),
    'ladaprev': ('build_lada_prevalence.py', 'Building LADA Prevalence by Healthcare Setting (Gap #10 BRONZE)'),
    'nutribeta': ('build_nutrition_beta.py', 'Building Personalized Nutrition for Beta Cells (Gap #13 BRONZE)'),
    'nutrilada': ('build_nutrition_lada.py', 'Building Personalized Nutrition for LADA (Gap #14 BRONZE)'),
    'gkapricing': ('build_gka_pricing.py', 'Building GKA Pricing Trajectory Model (Gap #15 BRONZE)'),
    'healthequity': ('build_health_equity.py', 'Building Health Equity Dashboard (Gap #2 GOLD)'),
    'methodology': ('build_methodology.py', 'Building Methodology & Validation Framework'),
    'pmidverify': ('verify_pmids.py', 'Verifying PMIDs against PubMed API'),
    'citations': ('add_citations.py', 'Adding source citations to Research Findings Summary'),
    'website': ('rebuild_website.py', 'Rebuilding GitHub Pages site (Tufte style)'),
}

def run_script(name, desc):
    path = os.path.join(SCRIPT_DIR, name)
    print(f"\n{'='*60}")
    print(f"  {desc}")
    print(f"{'='*60}")
    start = time.time()

    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=300
        )
        elapsed = time.time() - start

        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                print(f"  {line}")

        if result.returncode != 0:
            print(f"  ERROR (exit code {result.returncode})")
            if result.stderr:
                for line in result.stderr.strip().split('\n')[:10]:
                    print(f"  ! {line}")
            return False

        print(f"  Completed in {elapsed:.1f}s")
        return True

    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT after 300s")
        return False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        return False


def main():
    args = sys.argv[1:]

    if not args:
        targets = list(SCRIPTS.keys())
    else:
        targets = [a.lstrip('-') for a in args if a.lstrip('-') in SCRIPTS]
        if not targets:
            print("Usage: python run_quality_improvements.py [--dashboard] [--research] [--gaps] [--citations] [--website]")
            print("  No flags = run all improvements")
            sys.exit(1)

    print("=" * 60)
    print("  DIABETES RESEARCH HUB — QUALITY IMPROVEMENTS")
    print("=" * 60)
    print(f"  Running {len(targets)} improvement(s): {', '.join(targets)}")

    results = {}
    for key in targets:
        name, desc = SCRIPTS[key]
        results[key] = run_script(name, desc)

    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    for key, success in results.items():
        status = "OK" if success else "FAILED"
        print(f"  [{status}] {SCRIPTS[key][1]}")

    failed = sum(1 for v in results.values() if not v)
    if failed:
        print(f"\n  {failed} script(s) failed. Check output above.")
        sys.exit(1)
    else:
        print(f"\n  All {len(results)} improvements completed successfully.")
        print(f"\n  NEXT STEPS:")
        print(f"  1. Review the updated files in your project folder")
        print(f"  2. Verify placeholder citations marked 'verify' in Research_Findings_Summary.md")
        print(f"  3. Open the dashboards in a browser to confirm visual quality")
        print(f"  4. When satisfied, commit and push: git add -A && git commit -m 'Quality improvements' && git push")


if __name__ == '__main__':
    main()
