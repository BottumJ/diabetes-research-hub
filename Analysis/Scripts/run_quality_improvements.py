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
    'dictionary': ('build_data_dictionary.py', 'Building Medical Data Dictionary (117 terms, cited)'),
    'lada': ('build_lada_model.py', 'Building LADA Natural History Model (Gap #1 SILVER)'),
    'islet': ('build_islet_outcomes.py', 'Building Islet Transplant Outcomes Analysis (Gap #3 GOLD)'),
    'drugrepurpose': ('build_drug_repurposing_islet.py', 'Building Drug Repurposing for Islet Transplant (Gap #4 SILVER)'),  # Promoted to SILVER: 11 independent papers from multiple research groups confirm this gap exists.
    'immunomod': ('build_immunomod_lada.py', 'Building Immunomodulatory Drugs for LADA (Gap #8 SILVER)'),
    'treg': ('build_treg_neuropathy.py', 'Building Treg in Diabetic Neuropathy (Gap #5 SILVER)'),  # Promoted to SILVER: 12 papers from independent groups confirm both sides of the gap.
    'cartaccess': ('build_cart_access.py', 'Building CAR-T Access Barriers Analysis (Gap #6 GOLD)'),
    'gka': ('build_gka_landscape.py', 'Building GKA Drug Repurposing Landscape (Gap #7 SILVER)'),
    'isletequity': ('build_islet_equity.py', 'Building Islet Transplant Registry Equity (Gap #11 GOLD)'),
    'genericdrug': ('build_generic_drug_catalog.py', 'Building Generic Drug x Diabetes Mechanism Catalog (Gap #12 SILVER)'),
    'gkalada': ('build_gka_lada.py', 'Building GKA in LADA Analysis (Gap #9 EXPLORATORY)'),
    'ladaprev': ('build_lada_prevalence.py', 'Building LADA Prevalence by Healthcare Setting (Gap #10 SILVER)'),
    'nutribeta': ('build_nutrition_beta.py', 'Building Personalized Nutrition for Beta Cells (Gap #13 SILVER)'),
    'nutrilada': ('build_nutrition_lada.py', 'Building Personalized Nutrition for LADA (Gap #14 BRONZE)'),
    'gkapricing': ('build_gka_pricing.py', 'Building GKA Pricing Trajectory Model (Gap #15 BRONZE)'),
    'healthequity': ('build_health_equity.py', 'Building Health Equity Dashboard (Gap #2 GOLD)'),
    'methodology': ('build_methodology.py', 'Building Methodology & Validation Framework'),
    'pmidverify': ('verify_pmids.py', 'Verifying PMIDs against PubMed API'),
    'pmidtracker': ('track_unfound_pmids.py', 'Tracking unfound PMIDs (Verify-* markers)'),
    'citations': ('add_citations.py', 'Adding source citations to Research Findings Summary'),
    'ingest': ('ingest_papers.py', 'Ingesting paper abstracts and full text from PubMed/PMC'),
    # Must run AFTER ingest and BEFORE validate. verify_pmids.py only scans .py
    # source literals, so any paper that entered via extraction output or a
    # PubMed sweep never reached index.json and the citation gate was blind to
    # it. 39 such orphans were found on 2026-08-18 (13% of fetched abstracts),
    # including the sole source for NLRP3_inflammasome -> nephropathy.
    'orphans': ('reconcile_paper_index.py', 'Folding un-indexed corpus papers into the audit gate'),
    'validate': ('validate_citations.py', 'Validating citations and building evidence network'),
    # Gate: consumes validate_citations.py output. Added 2026-08-16 after 7 real
    # miscitations were found sitting unactioned in citation_validation.json.
    # Must run immediately after 'validate'.
    'mismatchgate': ('check_citation_mismatches.py', 'Gating on unresolved citation MISMATCHes'),
    'evidence': ('extract_evidence.py', 'Extracting evidence from papers for 15 research gaps'),
    'paperlibrary': ('build_paper_library.py', 'Building Paper Library Dashboard'),
    'drugscreen': ('build_drug_repurposing_screen.py', 'Building Generic Drug Repurposing Screen (34 drugs, pressure-tested)'),
    'ladadiagnostic': ('build_lada_diagnostic_model.py', 'Building LADA Diagnostic Cost-Effectiveness Model'),
    'trialequity': ('build_trial_equity_mapper.py', 'Building Clinical Trial Site Equity Mapper'),
    'corpus': ('build_corpus_analysis.py', 'Building Corpus Analysis Dashboard (co-occurrence network; counts printed by the builder)'),
    'extracted': ('build_extracted_evidence.py', 'Building Extracted Evidence Dashboard (counts printed by the builder)'),
    'researchpaths': ('build_research_paths.py', 'Building Research Paths Dashboard (post-artifact-filter counts printed by the builder)'),
    # Resolves state.paths / state.validated_paths / validated_research_paths.json
    # into one canonical store. Reading any single store directly is what emitted
    # six false "NEVER-VALIDATED" work items on 2026-08-16.
    'pathstore': ('path_store.py', 'Resolving the canonical research-path store (merge rule: recency, conservative tie-break)'),
    'statistics': ('build_statistical_analysis.py', 'Building Statistical Analysis Dashboard (meta-analysis, Bayesian synthesis, Monte Carlo)'),
    'repurposev2': ('build_repurposing_dashboard_v2.py', 'Building Islet Drug Repurposing Pipeline v2'),
    'website': ('rebuild_website.py', 'Rebuilding GitHub Pages site (Tufte style)'),
    'postprocess': ('postprocess_dashboards.py', 'Post-processing dashboards (nav, PMID links, ARIA)'),
    # Publish step. MUST run last: postprocess_dashboards.py rewrites
    # Dashboards/*.html, so syncing before it would publish pre-processed files.
    # Added 2026-08-16 after docs/Dashboards/ was found frozen since 2026-03-29
    # (33 stale, 2 missing, 0 in sync) while this runner reported all-green,
    # because rebuild_website.py only ever wrote docs/index.html.
    'syncdocs': ('sync_docs_dashboards.py', 'Publishing rebuilt dashboards to docs/ (GitHub Pages)'),
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


def commit_changes(message):
    """Commit via git_commit_safe.py rather than plain `git commit`.

    The mount denies unlink() inside .git/ at every file age, so git's standard
    create-lock/rename-over-then-delete cycle leaves a fresh lock on EVERY
    invocation and `git commit` only succeeds intermittently (~150 lock corpses
    had accumulated since April, one per daily run). git_commit_safe.py builds
    the commit with plumbing against an index held off the mount, which is
    deterministic. Push still requires host credentials -- see that script.
    """
    safe = os.path.join(SCRIPT_DIR, 'git_commit_safe.py')
    if not os.path.exists(safe):
        print('  ! git_commit_safe.py not found; skipping commit')
        return False
    print(f"\n{'='*60}")
    print('  Committing via git_commit_safe.py (deterministic plumbing path)')
    print(f"{'='*60}")
    try:
        # Must run from the repo root: git_commit_safe.py resolves the repository
        # from the current working directory, and a bare subprocess inherits the
        # caller's cwd (often Analysis/Scripts) -> "not a git repository".
        repo_root = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
        result = subprocess.run([sys.executable, safe, '-m', message],
                                capture_output=True, text=True, timeout=180,
                                cwd=repo_root)
        for line in (result.stdout or '').strip().split('\n'):
            if line:
                print(f'  {line}')
        if result.returncode != 0:
            for line in (result.stderr or '').strip().split('\n')[:10]:
                print(f'  ! {line}')
            print('  COMMIT FAILED')
            return False
        print('  [OK] committed')
        return True
    except Exception as e:
        print(f'  EXCEPTION during commit: {e}')
        return False


def main():
    args = sys.argv[1:]

    commit_msg = None
    if '--commit' in args:
        i = args.index('--commit')
        if i + 1 < len(args) and not args[i + 1].startswith('-'):
            commit_msg = args[i + 1]
            del args[i:i + 2]
        else:
            commit_msg = 'Automated pipeline rebuild'
            del args[i]

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
        # Only commit a green build. A failed build must never be committed.
        if commit_msg:
            commit_changes(commit_msg)
        print(f"\n  NEXT STEPS:")
        print(f"  1. Review the updated files in your project folder")
        print(f"  2. Verify placeholder citations marked 'verify' in Research_Findings_Summary.md")
        print(f"  3. Open the dashboards in a browser to confirm visual quality")
        if commit_msg:
            print(f"  4. Push from the Windows host (sandbox has no credential):")
            print(f"     cd C:\\Users\\justi\\OneDrive\\Diabetes_Research ; git push origin main")
        else:
            print(f"  4. To commit automatically next time, pass --commit \"message\"")


if __name__ == '__main__':
    main()
