#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_js_data_literals.py

NEW 2026-10-06. Gate: every JSON data literal a published page hands to its
JavaScript must parse.

WHY
    Builders write their tables as `const NAME = <json.dumps(...)>;` and the
    page's script renders them. The post-processing step that links PMIDs
    inserted <a href="..."> with bare double quotes INSIDE those JSON strings,
    which ends the string early. The browser then throws on the whole script
    and the table never appears. Five literals on three published pages
    (Research_Dashboard PIPELINE_DATA and TIMELINE_2025, Generic_Drug_Catalog
    drugsData, Immunomod_LADA DRUG_CANDIDATES and EVIDENCE_CATALOG) were broken
    this way, and every other gate passed: they all read the page as text.

WHAT IT CHECKS
    Every `const|let|var NAME = <literal>;` in docs/ and Dashboards/ whose
    literal starts the way json.dumps output does ([{", [[", [", {") must load
    with json.loads. Hand-written JavaScript arrays (single quotes, spreads,
    unquoted keys) are out of scope and skipped, so this cannot flag correct
    code; it can only miss broken code that is not JSON-shaped.

Exit 0 clean, 1 if any JSON-shaped literal fails to parse.
"""
import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REPORT = os.path.join(ROOT, 'Analysis', 'Results', 'js_data_literal_audit.json')
# JSON-shaped only: a double quote right after the opening bracket(s). A
# hand-written array such as [['Industry', n], ...] starts with a single quote
# and is skipped, so the gate cannot flag correct JavaScript.
DECL = re.compile(r'\b(?:const|let|var)\s+(\w+)\s*=\s*(?=\[\{\s*"|\[\[\s*"|\[\s*"|\{\s*")')


def literal_at(text, start):
    """Return the bracketed literal starting at `start`, honouring strings."""
    depth, i, in_str, esc = 0, start, False, False
    opener = text[start]
    while i < len(text):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c in '[{':
                depth += 1
            elif c in ']}':
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
        i += 1
    return text[start:]


def main():
    findings, checked = [], 0
    for sub in ('docs', 'Dashboards'):
        for path in sorted(glob.glob(os.path.join(ROOT, sub, '**', '*.html'), recursive=True)):
            text = io.open(path, encoding='utf-8', errors='replace').read()
            for m in DECL.finditer(text):
                lit = literal_at(text, m.end())
                checked += 1
                try:
                    json.loads(lit)
                except ValueError as e:
                    pos = getattr(e, 'pos', 0) or 0
                    findings.append({'file': os.path.relpath(path, ROOT), 'name': m.group(1),
                                     'error': str(e)[:120],
                                     'near': lit[max(0, pos - 80):pos + 40]})
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump({'checked': checked, 'broken': len(findings), 'findings': findings}, fh,
                  indent=2, ensure_ascii=False)
    if findings:
        print('[FAIL] %d of %d JSON data literals do not parse (the table they feed will not render):'
              % (len(findings), checked))
        for f in findings:
            print('  %s  %s: %s' % (f['file'], f['name'], f['error']))
        return 1
    print('[OK] all %d JSON data literals on published pages parse' % checked)
    return 0


if __name__ == '__main__':
    sys.exit(main())
