"""
DIABETES RESEARCH HUB - Master Runner
Runs all analysis scripts in sequence and generates a consolidated report.

USAGE (PowerShell):
    python run_all.py              # Run everything
    python run_all.py --monitor    # Only run the hub monitor
    python run_all.py --project1   # Only run the gap analysis
    python run_all.py --trials     # Only pull clinical trial snapshot
    python run_all.py --pubmed     # Only pull recent PubMed papers
"""

import subprocess
import sys
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "Results")
os.makedirs(RESULTS_DIR, exist_ok=True)

SCRIPTS = {
    "monitor": {
        "file": "hub_monitor.py",
        "name": "Hub File Monitor",
        "flag": "--monitor",
    },
    "project1": {
        "file": "project1_literature_gap_analysis.py",
        "name": "Project 1: Literature Gap Analysis",
        "flag": "--project1",
    },
    "trials": {
        "file": "baseline_clinical_trials.py",
        "name": "Clinical Trial Snapshot",
        "flag": "--trials",
    },
    "pubmed": {
        "file": "baseline_pubmed_alerts.py",
        "name": "PubMed Recent Papers Tracker",
        "flag": "--pubmed",
    },
}

def run_script(script_info):
    """Run a script and capture output."""
    script_path = os.path.join(SCRIPT_DIR, script_info["file"])
    if not os.path.exists(script_path):
        print(f"  [SKIP] {script_info['name']} — file not found: {script_path}")
        return False

    print(f"\n{'='*60}")
    print(f"Running: {script_info['name']}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=SCRIPT_DIR,
            capture_output=False,
            timeout=600,  # 10 minute timeout
        )
        if result.returncode == 0:
            print(f"  [OK] {script_info['name']} completed successfully.")
            return True
        else:
            print(f"  [FAIL] {script_info['name']} exited with code {result.returncode}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  [TIMEOUT] {script_info['name']} exceeded 10 minute limit.")
        return False
    except Exception as e:
        print(f"  [ERROR] {script_info['name']}: {e}")
        return False

def main():
    args = set(sys.argv[1:])
    start = datetime.now()

    print(f"Diabetes Research Hub — Master Runner")
    print(f"Started: {start.strftime('%Y-%m-%d %H:%M:%S')}")

    # Determine which scripts to run
    if not args:
        to_run = list(SCRIPTS.values())
    else:
        to_run = [v for v in SCRIPTS.values() if v["flag"] in args]

    if not to_run:
        print("No matching scripts found. Available flags:")
        for v in SCRIPTS.values():
            print(f"  {v['flag']:15s} — {v['name']}")
        return

    results = {}
    for script in to_run:
        results[script["name"]] = run_script(script)

    elapsed = (datetime.now() - start).total_seconds()
    print(f"\n{'='*60}")
    print(f"All tasks complete. Elapsed: {elapsed:.1f}s")
    print(f"{'='*60}")
    for name, ok in results.items():
        status = "OK" if ok else "FAILED"
        print(f"  [{status}] {name}")

if __name__ == "__main__":
    main()
