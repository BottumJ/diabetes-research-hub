#!/usr/bin/env python3
"""Regression gate: adjudicated-artifact paths must never reach the published site.

WHY THIS EXISTS
---------------
On 2026-08-19 the path `insulin_glargine -> T2D` -- adjudicated
EXTRACTION_ARTIFACT in the canonical store -- reached
docs/Dashboards/Research_Paths.html TWICE in the same day:

  1. The dashboard filtered on matched_text patterns only and never consulted
     the adjudicated status. Heuristic beat decision.
  2. After that was fixed it published again, because research_paths.json keys
     the edge in ARROW spelling (`insulin_glargine -> T2D`) while
     validated_research_paths.json keys it in UNDERSCORE spelling
     (`insulin_glargine_T2D`), and only the first store was being suppressed.

Both fixes live in build_research_paths.py. Neither fix is self-verifying: a
future builder, a third key spelling, or a new render site would reintroduce
the same class of defect silently. This script is the assertion that closes
that loop. It does not trust the builder -- it reads the PUBLISHED HTML and
asserts the suppressed edges are absent from it.

WHAT IT CHECKS
--------------
For every path in canonical_paths.json whose status is in SUPPRESSED_STATUSES,
assert its edge does not appear as a RENDERED PATH ENTRY in any docs/ dashboard,
under any key spelling (arrow, underscore, HTML-escaped arrow, unicode arrow).

Deliberately NOT a raw substring scan of the HTML: a suppressed edge may be
legitimately DISCUSSED in prose (e.g. the methodology note explaining why
GAD65 -> T1D was adjudicated CONTRADICTED). Suppression means "not presented as
a live finding", not "unmentionable". So the gate extracts only the tokens that
sit in path-entry positions and compares those.

Exit 0 = clean, exit 1 = a suppressed path is live on the published site.
"""

import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANONICAL = os.path.join(BASE_DIR, 'Analysis', 'Results', 'canonical_paths.json')
DOCS_DASH = os.path.join(BASE_DIR, 'docs', 'Dashboards')

# Must stay in sync with build_research_paths.SUPPRESSED_STATUSES.
SUPPRESSED_STATUSES = {
    'EXTRACTION_ARTIFACT',
    'CONTRADICTED',
    'CONTRADICTED_FOR_DIABETIC_NEPHROPATHY',
}

# Positions in the HTML where a token means "this is a path we are presenting".
# Each pattern must capture the path token in group 1.
PATH_ENTRY_PATTERNS = [
    re.compile(r'class="path-name"[^>]*>\s*([^<]{1,80}?)\s*<', re.IGNORECASE),
    re.compile(r'class="path-title"[^>]*>\s*([^<]{1,80}?)\s*<', re.IGNORECASE),
    re.compile(r'data-path="([^"]{1,80})"', re.IGNORECASE),
    # Table cells that hold a bare edge, e.g. <td>verapamil -> beta_cell</td>.
    # Constrained to edge-shaped content so prose cells are not swept in.
    re.compile(r'<t[dh][^>]*>\s*([A-Za-z0-9_()\-]{2,40}\s*(?:->|&gt;|&#62;|→)\s*'
               r'[A-Za-z0-9_()\- ]{2,40}?)\s*</t[dh]>'),
]


def norm_key(key):
    """Fold every spelling of one edge onto a single comparable token.

    Strips arrows (ascii, escaped, unicode), underscores, hyphens, whitespace
    and case. `insulin_glargine -> T2D`, `insulin_glargine_T2D` and
    `Insulin Glargine &gt; T2D` all resolve to `insulinglarginet2d`.
    """
    k = (key or '')
    k = k.replace('&gt;', '>').replace('&#62;', '>').replace('→', '>')
    k = re.sub(r'[\s_>\-]+', '', k)
    return k.lower()


def load_suppressed():
    """Return {normalised_key: (display_key, status)} for adjudicated artifacts."""
    with open(CANONICAL, encoding='utf-8') as f:
        payload = json.load(f)
    out = {}
    for key, rec in (payload.get('paths') or {}).items():
        if not isinstance(rec, dict):
            continue
        status = rec.get('status')
        if status not in SUPPRESSED_STATUSES:
            continue
        display = rec.get('display_key') or key
        for variant in (display, key):
            nk = norm_key(variant)
            if nk:
                out[nk] = (display, status)
    return out


def rendered_paths(html):
    """Extract tokens occupying path-entry positions in one HTML file."""
    found = set()
    for pat in PATH_ENTRY_PATTERNS:
        for m in pat.finditer(html):
            token = m.group(1).strip()
            if token:
                found.add(token)
    return found


def main():
    if not os.path.isdir(DOCS_DASH):
        print(f'[FAIL] published dashboards not found: {DOCS_DASH}')
        return 1

    suppressed = load_suppressed()
    if not suppressed:
        print('[WARN] canonical store lists no suppressed paths - gate is vacuous.')
        return 0

    violations = []
    files_scanned = 0
    entries_scanned = 0

    for name in sorted(os.listdir(DOCS_DASH)):
        if not name.endswith('.html'):
            continue
        path = os.path.join(DOCS_DASH, name)
        with open(path, encoding='utf-8', errors='replace') as f:
            html = f.read()
        files_scanned += 1
        for token in rendered_paths(html):
            entries_scanned += 1
            hit = suppressed.get(norm_key(token))
            if hit:
                violations.append((name, token, hit[0], hit[1]))

    distinct = len({norm_key(d) for d, _ in suppressed.values()})
    print('Suppression-gate regression test')
    print(f'  canonical store  : {CANONICAL}')
    print(f'  suppressed edges : {distinct} '
          f'({", ".join(sorted({d for d, _ in suppressed.values()}))})')
    print(f'  files scanned    : {files_scanned}')
    print(f'  path entries seen: {entries_scanned}')

    if violations:
        print(f'\n[FAIL] {len(violations)} suppressed path(s) are LIVE on the published site:')
        for fname, token, display, status in violations:
            print(f'  - {fname}: rendered "{token}" == {display} (adjudicated {status})')
        print('\nFix in build_research_paths.py, rebuild, and re-run this gate.')
        return 1

    print('\n[OK] No adjudicated-artifact path appears on the published site '
          'under any key spelling.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
