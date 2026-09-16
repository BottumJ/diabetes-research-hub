#!/usr/bin/env python3
"""
Host-side verification for the 2026-09-10 citation repairs.

WHY THIS FILE EXISTS
    The Linux sandbox failed to mount on 2026-09-10 for the second consecutive
    day (same error both days: "source path ... is under Plan9 share 'c' which
    is not mounted"). No Python ran in either session. So the repairs of both
    days were made with file tools and verified by re-grepping, but nothing was
    parsed, nothing was built, and no gate was run.

    That leaves the repo in a specific and easily-missed state: the BUILDER
    SCRIPTS are corrected and the GENERATED HTML is not. A reader of
    Dashboards/ or docs/Dashboards/ still sees every false citation removed on
    2026-09-09 and 2026-09-10, while a grep of Analysis/Scripts/ reports them
    fixed. Do not treat the repairs as applied until the rebuild has run.

RUN THIS ON WINDOWS, IN THIS ORDER
    cd C:\\Users\\justi\\OneDrive\\Diabetes_Research
    python Analysis\\Scripts\\verify_2026_09_10_repairs.py
    python Analysis\\Scripts\\verify_2026_09_09_repairs.py
    python Analysis\\Scripts\\run_quality_improvements.py
    git add -A ; git commit -m "Citation repairs 2026-09-10" ; git push origin main

WHAT THIS CHECKS
    1. agent_state.json still parses as JSON, and its papers / work_queue /
       run_history are intact. It was hand-edited without a parser available,
       which is the single most likely thing to have been broken.
    2. Every file edited on 2026-09-10 compiles as Python. The edits touched
       f-string HTML templates, where an unescaped brace is a live hazard.
    3. PMID 32175717 no longer appears in any builder except inside a repair
       comment or an [UNSOURCED] tooltip.
    4. Every builder that now emits class="unsourced" also defines a .unsourced
       CSS rule. Five builders used the class without defining it before today,
       so their warning markers were rendering as plain text.
    5. The credibility sweep, re-run as code rather than as the grep this
       session had to use.

Exit codes: 0 clean, 1 findings.
"""
import ast
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
STATE = os.path.join(BASE_DIR, 'Analysis', 'Results', 'agent_state.json')

# Files edited on 2026-09-10.
EDITED = [
    'build_generic_drug_catalog.py',
    'build_cart_access.py',
    'build_lada_diagnostic_model.py',
    'build_lada_prevalence.py',
    'build_gka_landscape.py',
    'build_statistical_analysis.py',
    'build_corpus_analysis.py',
    'build_repurposing_dashboard_v2.py',
    'rebuild_research_dashboard.py',
]

findings = []


def check_state():
    """agent_state.json was hand-edited with no parser available."""
    if not os.path.exists(STATE):
        findings.append(f'MISSING: {STATE}')
        return
    try:
        with open(STATE, encoding='utf-8') as fh:
            state = json.load(fh)
    except json.JSONDecodeError as exc:
        findings.append(
            f'agent_state.json DOES NOT PARSE: {exc}. This is the expected '
            f'failure mode of a hand-edited state file. A dated .bak_* sibling '
            f'in the same directory is the recovery path.')
        return

    print(f'  agent_state.json parses. '
          f'papers={len(state.get("papers", {}))} '
          f'queue={len(state.get("work_queue", []))} '
          f'runs={len(state.get("run_history", []))}')

    if state.get('last_run') != '2026-09-10':
        findings.append(
            f'state["last_run"] is {state.get("last_run")!r}, expected '
            f'"2026-09-10" - the run entry may not have been saved.')

    if '37583402' not in state.get('papers', {}):
        findings.append('PMID 37583402 was not added to state["papers"].')
    elif state['papers']['37583402'].get('status') != 'UNVETTED':
        findings.append('PMID 37583402 should be UNVETTED until eutils confirms it.')

    dates = [r.get('date') for r in state.get('run_history', [])]
    if '2026-09-10' not in dates:
        findings.append('No 2026-09-10 entry in run_history.')


def check_syntax():
    """Unescaped braces in f-string HTML templates are the live hazard."""
    for name in EDITED:
        path = os.path.join(SCRIPT_DIR, name)
        if not os.path.exists(path):
            findings.append(f'MISSING: {name}')
            continue
        try:
            with open(path, encoding='utf-8') as fh:
                ast.parse(fh.read(), filename=name)
        except SyntaxError as exc:
            findings.append(f'{name} DOES NOT COMPILE: line {exc.lineno}: {exc.msg}')
        else:
            print(f'  {name}: compiles')


def check_32175717():
    """Only repair comments and tooltips may still mention it."""
    pat = re.compile(r'^.*32175717.*$', re.MULTILINE)
    allowed = ('Repaired', 'repaired', 'WITHDRAWN', 'Withdrawn', 'removed',
               'Citation removed', 'FALSE', 'previously', 'title=', '#')
    for name in os.listdir(SCRIPT_DIR):
        if not name.endswith('.py') or name.startswith('_'):
            continue
        if name.startswith(('verify_', 'audit_')):
            continue
        path = os.path.join(SCRIPT_DIR, name)
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        for line in pat.findall(text):
            if any(token in line for token in allowed):
                continue
            findings.append(
                f'{name}: PMID 32175717 still attached outside a repair note:\n'
                f'      {line.strip()[:160]}')


def check_unsourced_css():
    """A warning nobody can see is not a warning."""
    for name in os.listdir(SCRIPT_DIR):
        if not name.endswith('.py'):
            continue
        path = os.path.join(SCRIPT_DIR, name)
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        if 'class="unsourced"' not in text:
            continue
        # The stylesheet may be an f-string, so the rule may be .unsourced {{
        if not re.search(r'\.unsourced\s*\{\{?', text):
            findings.append(
                f'{name}: emits class="unsourced" but defines no .unsourced CSS '
                f'rule, so its [UNSOURCED] markers render as unstyled text.')
        else:
            print(f'  {name}: .unsourced defined')


def check_credibility_sweep():
    """Step 4 of the scheduled task, as code rather than as grep.

    NOTE the threshold below is deliberately NOT the task file's 42,000,000.
    That rule expired when PubMed crossed 42 million during 2026 and was
    replaced by Analysis/Scripts/pmid_ceiling.py, which resolves the ceiling
    live. This is an offline pre-filter only; audit_impossible_pmids.py is the
    real gate and should be run by run_quality_improvements.py.
    """
    offline_floor = 43_000_000
    phrases = ('zero SAEs', 'zero rejection', 'curative')
    pmid_re = re.compile(r'\b(\d{8})\b')
    for name in os.listdir(SCRIPT_DIR):
        if not name.startswith(('build_', 'rebuild_')) or not name.endswith('.py'):
            continue
        path = os.path.join(SCRIPT_DIR, name)
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        for value in pmid_re.findall(text):
            if int(value) >= offline_floor:
                findings.append(
                    f'{name}: PMID {value} is above the offline pre-filter floor '
                    f'({offline_floor:,}); resolve it through eutils before trusting it.')
        for phrase in phrases:
            if phrase.lower() in text.lower():
                findings.append(f'{name}: contains overclaim phrase {phrase!r}.')


def main():
    print('Verifying 2026-09-10 repairs\n')
    print('[1] agent_state.json')
    check_state()
    print('\n[2] Python syntax of edited builders')
    check_syntax()
    print('\n[3] PMID 32175717 attachments')
    check_32175717()
    print('\n[4] .unsourced CSS coverage')
    check_unsourced_css()
    print('\n[5] Credibility sweep')
    check_credibility_sweep()

    print()
    if findings:
        print(f'[FAIL] {len(findings)} finding(s):')
        for item in findings:
            print(f'  - {item}')
        return 1
    print('[OK] all checks clean')
    print('\nNEXT: run_quality_improvements.py has NOT been run since 2026-09-08.')
    print('Until it is, Dashboards/ and docs/Dashboards/ still contain the false')
    print('citations that were removed from the builder scripts.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
