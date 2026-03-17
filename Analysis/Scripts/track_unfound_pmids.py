#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unfound PMID Tracker
Scans all build scripts for remaining Verify-* markers (PMIDs that still need
to be resolved) and reports them as part of the daily build process.

Outputs:
  1. Console report showing count and details of unfound PMIDs
  2. JSON tracking file at Analysis/Results/unfound_pmids.json

This script is designed to run as part of the 28-script daily build suite.
When all Verify-* markers are resolved, it reports "0 unfound" and exits clean.
"""

import os
import re
import json
from datetime import datetime

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
results_dir = os.path.join(base_dir, 'Analysis', 'Results')
os.makedirs(results_dir, exist_ok=True)


def scan_for_verify_markers():
    """Scan all Python build scripts for Verify-* markers."""
    markers = {}  # marker_text -> list of {file, line, context}

    for fname in sorted(os.listdir(script_dir)):
        if not fname.endswith('.py'):
            continue
        # Skip this script itself and utility scripts
        if fname in ('track_unfound_pmids.py', 'fix_pmids.py'):
            continue

        fpath = os.path.join(script_dir, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue

        for i, line in enumerate(lines, 1):
            # Match Verify-* patterns
            matches = re.findall(r'Verify-[\w-]+', line)
            for marker in matches:
                if marker not in markers:
                    markers[marker] = []
                context = line.strip()[:150]
                markers[marker].append({
                    'file': fname,
                    'line': i,
                    'context': context
                })

    return markers


def main():
    print("Unfound PMID Tracker")
    print("=" * 60)

    markers = scan_for_verify_markers()

    # Count unique markers and total occurrences
    unique_count = len(markers)
    total_occurrences = sum(len(locs) for locs in markers.values())

    # Save JSON tracking file
    json_path = os.path.join(results_dir, 'unfound_pmids.json')
    json_output = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'unique_markers': unique_count,
            'total_occurrences': total_occurrences
        },
        'markers': {}
    }
    for marker, locs in sorted(markers.items()):
        json_output['markers'][marker] = {
            'occurrences': len(locs),
            'files': list(set(l['file'] for l in locs)),
            'locations': locs
        }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2, ensure_ascii=False)

    # Console output
    if unique_count == 0:
        print("  All PMIDs resolved. No Verify-* markers remaining.")
        print(f"  Tracking file: {json_path}")
        print(f"\n  Unfound PMID Tracker: 0 remaining")
        return 0

    print(f"  Found {unique_count} unresolved PMID marker(s) ({total_occurrences} total occurrences)")
    print()

    for marker in sorted(markers.keys()):
        locs = markers[marker]
        files = sorted(set(l['file'] for l in locs))
        print(f"  [{marker}]")
        print(f"    Files: {', '.join(files)}")
        print(f"    Occurrences: {len(locs)}")
        print()

    print(f"  Tracking file: {json_path}")
    print(f"\n  Unfound PMID Tracker: {unique_count} remaining")

    # Return count (non-zero signals work remaining, but NOT a failure)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
