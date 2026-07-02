#!/usr/bin/env python3
"""
run_daily_local.py — Run the Diabetes Research Hub daily data pull on YOUR machine.

WHY THIS EXISTS:
The scheduled Cowork run executes each shell command in a sandbox that (a) kills any
process after ~45 seconds and (b) destroys background processes when the call returns.
The literature gap analysis needs ~35-40 minutes (465 sequential PubMed queries), so it
can NEVER finish in the sandbox — that is why literature_gap_data.json was frozen since
2026-06-23. Run this script locally, where there is no time cap.

USAGE:
    cd Analysis/Scripts
    python run_daily_local.py            # runs all four in order
    python run_daily_local.py --only gap # runs just the gap analysis

Set NCBI_API_KEY first to raise PubMed's limit from 3 to 10 req/sec (much faster/safer):
    Windows (PowerShell):  $env:NCBI_API_KEY="your_key_here"
    macOS/Linux:           export NCBI_API_KEY="your_key_here"
Get a free key at https://www.ncbi.nlm.nih.gov/account/ -> Settings -> API Key Management.
"""
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

# (label, filename) in required execution order
PIPELINE = [
    ("clinical_trials", "baseline_clinical_trials.py"),
    ("pubmed",          "baseline_pubmed_alerts.py"),
    ("gap",             "project1_literature_gap_analysis.py"),
    ("hub_monitor",     "hub_monitor.py"),
]


def run_one(label, filename):
    path = SCRIPTS_DIR / filename
    if not path.exists():
        print(f"  !! MISSING: {filename} — skipped")
        return False
    print(f"\n{'='*64}\n  RUNNING: {filename}  ({label})\n{'='*64}")
    t0 = time.time()
    # No timeout: let the long gap analysis run to completion.
    result = subprocess.run([sys.executable, "-u", str(path)], cwd=str(SCRIPTS_DIR))
    dt = time.time() - t0
    ok = result.returncode == 0
    print(f"  -> {'OK' if ok else 'FAILED (exit %d)' % result.returncode} in {dt:,.0f}s")
    return ok


def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]

    results = {}
    for label, filename in PIPELINE:
        if only and label != only:
            continue
        results[label] = run_one(label, filename)
        time.sleep(1)

    print(f"\n{'='*64}\n  SUMMARY\n{'='*64}")
    for label, ok in results.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
