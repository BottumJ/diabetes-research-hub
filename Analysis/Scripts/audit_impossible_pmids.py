#!/usr/bin/env python3
"""
Credibility sweep, versioned — impossible PMIDs and preclinical overclaim.

Replaces the ad-hoc grep the scheduled-task file describes ("PMIDs above
42000000 are fabricated; grep for 'zero SAEs', 'zero rejection', 'achieves',
'curative'"). Two problems with that sweep, both fixed here:

1. THE THRESHOLD EXPIRED. 42,000,000 was passed by PubMed months ago. Measured
   2026-08-31 the live ceiling is 42,669,647 and this corpus holds 30+ real
   PMIDs above 42,000,000. The gate now reads the ceiling from PubMed at
   runtime via pmid_ceiling.py. See that module for why the margin exists.

2. THE PHRASE SWEEP MATCHED ITS OWN AUDIT TRAIL. Every run report in
   Analysis/Results/ contains the sentence "no 'zero SAEs' / 'zero rejection'",
   so a naive grep returns dozens of hits that are records of absence. Those
   paths are excluded by class here, not by remembered filename.

WHAT THIS GATE DOES NOT DO
   It does not prove a PMID exists. A fabricated PMID below the ceiling passes.
   verify_pmids.py checks existence against the live API; this is the cheap
   offline pre-filter that catches the impossible ones.

Exit codes: 0 clean, 1 findings.
"""
import json
import os
import re
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RESULTS = os.path.join(BASE_DIR, 'Analysis', 'Results')
REPORT = os.path.join(RESULTS, 'impossible_pmid_audit.json')

import pmid_ceiling  # noqa: E402

PMID_RE = re.compile(r'\b(?:PMID[:\s#]*)?(\d{7,9})\b')
BARE_PMID_RE = re.compile(r'PMID[:\s#]*(\d{7,9})', re.IGNORECASE)

# Directories that hold this agent's own audit trail. Their whole content is
# statements ABOUT the gate, so scanning them re-detects the gate's own prose.
# Excluded by class (path role), never by individual filename.
EXCLUDED_DIRS = {
    os.path.join('.git'),
    os.path.join('Analysis', 'Results'),   # run reports + machine output
    os.path.join('Analysis', 'Logs'),
    os.path.join('Papers'),                # fetched abstracts: other people's words
    os.path.join('docs', '_site'),
}

# Files whose purpose is to DEFINE these patterns. Same class-based reasoning.
SELF_REFERENTIAL = {
    'audit_impossible_pmids.py',
    'pmid_ceiling.py',
    'verify_before_deploy.py',
    'audit_absolute_claims.py',
}

SCAN_EXTENSIONS = ('.py', '.html', '.md')

# Preclinical overclaim. Each pattern needs a finite verb or an unhedged
# absolute — bare nouns ("curative intent", "achievement") are not claims.
OVERCLAIM_PATTERNS = [
    (r'\bzero\s+(SAEs?|serious adverse events?|rejection(?:\s+episodes?)?)\b',
     'absolute safety/rejection claim'),
    (r'\b100\s*%\s+(insulin[- ]independen|protect|efficac|respon)',
     'absolute efficacy claim'),
    (r'\bis\s+curative\b|\bproves?\s+curative\b|\bcures?\s+(type\s*1\s*diabetes|T1D)\b',
     'cure claim'),
    (r'\bachieves?\s+(a\s+)?(cure|remission|insulin independence)\b',
     'achievement-of-cure claim'),
]
HEDGES = re.compile(
    r'\b(may|might|could|suggest|hypothes|potential|preclinical|in mice|in vitro|'
    r'unpublished|not (?:yet )?(?:published|peer[- ]reviewed)|press release|'
    r'conference|investigational|no[t]? (?:be )?restated|must not)\b',
    re.IGNORECASE)


def scannable_files():
    for root, dirs, files in os.walk(BASE_DIR):
        rel_root = os.path.relpath(root, BASE_DIR)
        if any(rel_root == d or rel_root.startswith(d + os.sep) for d in EXCLUDED_DIRS):
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
        for name in files:
            if not name.endswith(SCAN_EXTENSIONS):
                continue
            if name in SELF_REFERENTIAL:
                continue
            yield os.path.join(root, name)


def main():
    cap, prov = pmid_ceiling.ceiling()
    flag_above = cap + pmid_ceiling.MARGIN
    print('=' * 74)
    print('CREDIBILITY SWEEP - impossible PMIDs and preclinical overclaim')
    print('=' * 74)
    print(pmid_ceiling.explain())
    if prov['source'] in ('stale_cache', 'last_measured'):
        print(f"  WARNING: ceiling not measured live this run ({prov['source']}). "
              f"Reason: {prov.get('refresh_error', 'network disabled')}")

    impossible = []
    overclaims = []
    files_scanned = 0
    pmids_seen = set()

    for path in scannable_files():
        rel = os.path.relpath(path, BASE_DIR)
        try:
            with open(path, encoding='utf-8', errors='replace') as fh:
                lines = fh.readlines()
        except OSError:
            continue
        files_scanned += 1
        for num, line in enumerate(lines, 1):
            # PMIDs: only labelled ones in prose/markup, any 7-9 digit run in .py
            # literals would sweep in years, dollar amounts and NCT digits.
            for match in BARE_PMID_RE.finditer(line):
                value = match.group(1)
                pmids_seen.add(value)
                if pmid_ceiling.is_impossible(value, cap):
                    impossible.append({'pmid': value, 'file': rel, 'line': num,
                                       'context': line.strip()[:200]})
            for pattern, label in OVERCLAIM_PATTERNS:
                hit = re.search(pattern, line, re.IGNORECASE)
                if not hit:
                    continue
                window = ''.join(lines[max(0, num - 2):num + 1])
                if HEDGES.search(window):
                    continue
                overclaims.append({'file': rel, 'line': num, 'kind': label,
                                   'match': hit.group(0),
                                   'context': line.strip()[:220]})

    print(f'\nScanned {files_scanned} files, {len(pmids_seen)} distinct labelled PMIDs.')
    print(f'Impossible PMIDs (> {flag_above:,}): {len(impossible)}')
    for item in impossible:
        print(f"  {item['pmid']}  {item['file']}:{item['line']}")
        print(f"      {item['context']}")
    print(f'Unhedged preclinical overclaims: {len(overclaims)}')
    for item in overclaims:
        print(f"  [{item['kind']}] {item['file']}:{item['line']}  ->  {item['match']}")
        print(f"      {item['context']}")

    highest = max((int(p) for p in pmids_seen), default=0)
    report = {
        'generated': datetime.now().isoformat(),
        'ceiling': cap,
        'margin': pmid_ceiling.MARGIN,
        'flag_above': flag_above,
        'ceiling_provenance': prov,
        'files_scanned': files_scanned,
        'distinct_pmids': len(pmids_seen),
        'highest_pmid_in_repo': highest,
        'headroom_to_flag': flag_above - highest,
        'impossible_pmids': impossible,
        'overclaims': overclaims,
        'superseded_rule': {
            'rule': 'PMIDs above 42000000 are fabricated',
            'source': 'scheduled-task file, Step 4',
            'status': 'STALE',
            'evidence': (f'live ceiling {cap:,} measured {prov.get("measured")}; '
                         'repo holds real PMIDs above 42,000,000'),
        },
    }
    os.makedirs(RESULTS, exist_ok=True)
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print(f'\nHighest PMID anywhere in the repo: {highest:,} '
          f'({flag_above - highest:,} below the flag line)')
    print(f'Report: {os.path.relpath(REPORT, BASE_DIR)}')

    if impossible or overclaims:
        print('\n[FAIL] credibility sweep found issues')
        return 1
    print('\n[OK] credibility sweep clean')
    return 0


if __name__ == '__main__':
    sys.exit(main())
