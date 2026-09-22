#!/usr/bin/env python3
"""Assert that every gate wired into run_quality_improvements.py can actually FAIL.

WHY THIS EXISTS, AND WHY IT IS DIFFERENT FROM EVERY OTHER AUDIT HERE.

run_quality_improvements.run_script() decides pass/fail on exactly one thing:

    if result.returncode != 0:
        ...
        return False

Nothing else is consulted. Not stdout, not the word FAIL, not a report file.
So a gate that detects its defect, prints "[FAIL] 1 conflict", and then returns
control to the interpreter without a non-zero exit is not a weak gate -- it is
not a gate at all. The runner records it GREEN, the stage counter says 80/80,
and the defect ships. This was found live on 2026-09-21 in
audit_endpoint_value_agreement.py, which printed FAIL and exited 0.

Every other audit in this repository checks the CONTENT of an assertion. This
one checks whether the MECHANISM that is supposed to stop a bad assertion is
connected to anything. A gate with this bug is invisible to all of them,
including to itself, because its own output is correct -- it says FAIL, and
means it, and no one is listening.

THE THREE PATTERNS IT LOOKS FOR
  A. Prints a failure marker but the module contains no non-zero exit at all.
  B. main()-shaped function returns a non-zero literal, but the module-level
     call site is a bare `main()` rather than `sys.exit(main())`. The return
     value is discarded and the process exits 0. This is the 2026-09-21 bug.
  C. A non-zero exit exists, but only inside an `except` handler -- i.e. the
     script can fail on a crash but not on a finding.

DELIBERATE NON-GOAL. This does not check whether a gate's LOGIC is right, only
whether its verdict can reach the runner. A gate that never detects anything
still passes here, correctly: that is a different defect and gates like
test_markdown_citation_gate.py exist to catch it.

Exit 0 when every wired gate can fail; 1 otherwise.
"""

import ast
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RUNNER = os.path.join(SCRIPT_DIR, 'run_quality_improvements.py')
OUT = os.path.join(ROOT, 'Analysis', 'Results', 'gate_exit_code_audit.json')

# Markers a stage prints when it has found its defect. Matched against string
# literals in the source, case-sensitively for the bracketed forms because
# lowercase "fail" appears in ordinary prose ("failed to resolve", "failure
# mode") throughout this repo.
FAIL_MARKERS = (
    '[FAIL]', '[BLOCK]', '[BLOCKING]', '[VIOLATION]', '[DEFECT]', '[RED]',
)

# Stages that are BUILDERS, not gates. A builder's job is to write a file; it
# has no verdict to report, so "cannot fail on a finding" is correct for it.
# Kept as a prefix list rather than a maintained inventory so a new builder is
# classified the day it is added.
BUILDER_PREFIXES = ('build_', 'rebuild_', 'sync_', 'improve_', 'add_',
                    'ingest_', 'extract_', 'baseline_', 'reconcile_',
                    'gap_analysis_', 'postprocess_', 'track_')


def stage_scripts():
    """Read the SCRIPTS dict out of the runner without importing it.

    Parsed rather than imported so this audit cannot be broken by, or silently
    pick up, anything the runner does at import time.
    """
    tree = ast.parse(open(RUNNER, encoding='utf-8').read())
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(getattr(t, 'id', None) == 'SCRIPTS' for t in node.targets):
            continue
        out = []
        for key, val in zip(node.value.keys, node.value.values):
            # value is a tuple: (filename, description[, args])
            fname = val.elts[0].value
            out.append((key.value, fname))
        return out
    raise SystemExit('audit_gate_exit_codes: SCRIPTS dict not found in runner')


def literal_int(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return node.value
    return None


def analyse(path):
    """Return a verdict dict for one stage script."""
    src = open(path, encoding='utf-8').read()
    tree = ast.parse(src)

    fail_markers_found = sorted({
        m for m in FAIL_MARKERS
        for n in ast.walk(tree)
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and m in n.value
    })

    # --- every sys.exit / SystemExit in the file, with the handler depth ---
    nonzero_exits = []          # (lineno, in_except)
    zero_exits = []
    exit_in_except = []

    def walk_scope(node, in_except):
        for child in ast.iter_child_nodes(node):
            nxt = in_except or isinstance(child, ast.ExceptHandler)
            if isinstance(child, ast.Call):
                fn = child.func
                name = None
                if isinstance(fn, ast.Attribute) and fn.attr == 'exit':
                    name = 'exit'
                elif isinstance(fn, ast.Name) and fn.id in ('exit', 'SystemExit'):
                    name = 'exit'
                if name:
                    arg = child.args[0] if child.args else None
                    v = literal_int(arg) if arg is not None else 0
                    if arg is not None and v is None:
                        # sys.exit(main()) or sys.exit(<expr>) -- non-literal,
                        # treated as capable of being non-zero.
                        nonzero_exits.append((child.lineno, nxt, 'expr'))
                    elif v:
                        nonzero_exits.append((child.lineno, nxt, str(v)))
                    else:
                        zero_exits.append(child.lineno)
                    if nxt:
                        exit_in_except.append(child.lineno)
            if isinstance(child, ast.Raise):
                exc = child.exc
                if isinstance(exc, ast.Call) and getattr(exc.func, 'id', '') == 'SystemExit':
                    arg = exc.args[0] if exc.args else None
                    v = literal_int(arg) if arg is not None else 1
                    nonzero_exits.append((child.lineno, nxt, str(v if v is not None else 'expr')))
                    if nxt:
                        exit_in_except.append(child.lineno)
                elif isinstance(exc, (ast.Name, ast.Call)) and not nxt:
                    # a bare raise at module/function scope also exits non-zero
                    nonzero_exits.append((child.lineno, nxt, 'raise'))
            walk_scope(child, nxt)

    walk_scope(tree, False)

    # --- pattern B: the ENTRY POINT returns non-zero but the call drops it ---
    #
    # SCOPED TO THE ENTRY POINT ON PURPOSE. A first draft of this audit asked
    # whether ANY function in the file returns a non-zero literal, and it
    # produced two false positives out of three findings on its first run:
    # rebuild_website.get_trial_count() and postprocess_dashboards.
    # is_inside_href() return ordinary integers and booleans that have nothing
    # to do with a verdict. Only the function the `if __name__ == "__main__"`
    # block calls can carry an exit code, so only that function is examined.
    entry_calls = []            # [(func_name, lineno, wrapped_in_exit)]
    for node in tree.body:
        if not (isinstance(node, ast.If) and
                isinstance(node.test, ast.Compare) and
                getattr(node.test.left, 'id', '') == '__name__'):
            continue
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                # bare `main()` -- return value discarded
                nm = getattr(stmt.value.func, 'id', None)
                if nm:
                    entry_calls.append((nm, stmt.lineno, False))
            elif isinstance(stmt, ast.Call):
                fn = stmt.func
                is_exit = ((isinstance(fn, ast.Attribute) and fn.attr == 'exit')
                           or (isinstance(fn, ast.Name) and
                               fn.id in ('exit', 'SystemExit')))
                if is_exit:
                    for a in stmt.args:
                        nm = getattr(getattr(a, 'func', None), 'id', None)
                        if nm:
                            entry_calls.append((nm, stmt.lineno, True))

    fns = {n.name: n for n in ast.walk(tree)
           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

    def returns_nonzero(name):
        fn = fns.get(name)
        if fn is None:
            return False
        for n in ast.walk(fn):
            if isinstance(n, ast.Return) and literal_int(n.value):
                return True
        return False

    entry_returns_nonzero = sorted({nm for nm, _, _ in entry_calls
                                    if returns_nonzero(nm)})
    dropped_returns = [(nm, ln) for nm, ln, wrapped in entry_calls
                       if not wrapped and returns_nonzero(nm)]

    return {
        'fail_markers': fail_markers_found,
        'nonzero_exits': [{'line': l, 'in_except': e, 'code': c}
                          for l, e, c in nonzero_exits],
        'nonzero_outside_except': [l for l, e, c in nonzero_exits if not e],
        'zero_exits': zero_exits,
        'entry_points': [{'func': n, 'line': l, 'exit_wrapped': w}
                         for n, l, w in entry_calls],
        'entry_returns_nonzero': entry_returns_nonzero,
        'dropped_nonzero_returns': [{'func': f, 'line': l}
                                    for f, l in dropped_returns],
    }


SELFTEST_FIXTURES = {
    # (A) The live 2026-09-21 bug shape: a real verdict, discarded.
    'A_dropped_return': ('''
import sys
def main():
    if find_conflicts():
        print("  [FAIL] 1 conflict")
        return 1
    return 0
if __name__ == "__main__":
    main()
''', 'dropped'),
    # (B) The same file, repaired. Must NOT be flagged.
    'B_repaired': ('''
import sys
def main():
    if find_conflicts():
        print("  [FAIL] 1 conflict")
        return 1
    return 0
if __name__ == "__main__":
    sys.exit(main())
''', 'clean'),
    # (C) A builder whose HELPER returns a non-zero int. This shape produced
    #     two false positives in this audit's first draft, so it is pinned.
    'C_builder_helper_int': ('''
def get_trial_count():
    return 42
def main():
    print("Written: index.html")
if __name__ == "__main__":
    main()
''', 'clean'),
    # (D) Can crash but cannot fail on a finding.
    'D_exit_only_on_crash': ('''
import sys
def main():
    try:
        check()
    except Exception:
        sys.exit(1)
    print("  [FAIL] found a defect")
if __name__ == "__main__":
    main()
''', 'crash_only'),
    # (E) Prints a verdict, no exit path of any kind.
    'E_no_exit_at_all': ('''
def main():
    print("  [FAIL] 3 violations")
if __name__ == "__main__":
    main()
''', 'no_exit'),
}


def selftest():
    """Prove the audit in BOTH directions before trusting a green run.

    A gate that has only ever been run against a clean tree is indistinguishable
    from a gate that detects nothing. These fixtures replay the exact shape of
    the defect this audit was built for AND the shape of its own two false
    positives, so a future edit that loosens the rule fails here rather than in
    a run report.
    """
    import tempfile
    ok = True
    print('  SELFTEST (sensitivity and specificity)')
    for name, (src, expect) in sorted(SELFTEST_FIXTURES.items()):
        with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False,
                                         encoding='utf-8') as fh:
            fh.write(src)
            tmp = fh.name
        try:
            a = analyse(tmp)
        finally:
            os.unlink(tmp)

        if expect == 'dropped':
            got = bool(a['dropped_nonzero_returns'])
        elif expect == 'clean':
            got = not a['dropped_nonzero_returns'] and not (
                a['fail_markers'] and not a['nonzero_exits'])
        elif expect == 'crash_only':
            got = bool(a['nonzero_exits']) and not a['nonzero_outside_except']
        elif expect == 'no_exit':
            got = bool(a['fail_markers']) and not a['nonzero_exits']
        else:
            got = False
        print('    %-24s expect %-10s %s' % (name, expect,
                                             '[OK]' if got else '[FAIL]'))
        ok = ok and got
    print('    -> %s' % ('all fixtures behaved as specified' if ok else
                         'FIXTURE MISMATCH - the rule has drifted'))
    return ok


def main():
    if '--selftest' in sys.argv:
        return 0 if selftest() else 1

    print('=' * 68)
    print('  GATE EXIT-CODE AUDIT')
    print("  Can each wired gate's verdict reach the runner?")
    print('=' * 68)

    stages = stage_scripts()
    records = []
    defects = []

    for key, fname in stages:
        path = os.path.join(SCRIPT_DIR, fname)
        if not os.path.exists(path):
            defects.append({'stage': key, 'script': fname,
                            'pattern': 'MISSING_SCRIPT',
                            'detail': 'wired into the runner but not on disk'})
            continue

        is_builder = fname.startswith(BUILDER_PREFIXES)
        try:
            a = analyse(path)
        except SyntaxError as e:
            # audit_builders_compile.py owns this finding; do not double-report.
            records.append({'stage': key, 'script': fname,
                            'role': 'unparseable', 'note': str(e)})
            continue

        role = 'builder' if is_builder else 'gate'
        rec = {'stage': key, 'script': fname, 'role': role}
        rec.update(a)

        # ---- pattern B, checked FIRST because it is the live bug class ------
        if a['dropped_nonzero_returns']:
            for d in a['dropped_nonzero_returns']:
                defects.append({
                    'stage': key, 'script': fname, 'pattern': 'DROPPED_RETURN',
                    'detail': ("%s() returns a non-zero code at least once but "
                               "line %d calls it as a bare statement, so the "
                               "code is discarded and the process exits 0"
                               % (d['func'], d['line'])),
                })
            rec['verdict'] = 'DEFECT'
        elif not a['fail_markers'] and not a['entry_returns_nonzero']:
            # Nothing that looks like a verdict: no failure marker in the
            # output and no non-zero code out of the entry point. Builders
            # live here and belong here -- a builder's product is a file, not
            # a judgement. Reported, never failed.
            rec['verdict'] = 'NO_VERDICT'
        elif not a['nonzero_exits']:
            defects.append({
                'stage': key, 'script': fname, 'pattern': 'NO_NONZERO_EXIT',
                'detail': ('prints %s but the module contains no non-zero exit '
                           'path at all' % ', '.join(a['fail_markers'] or
                                                     ['a failure return'])),
            })
            rec['verdict'] = 'DEFECT'
        elif not a['nonzero_outside_except']:
            defects.append({
                'stage': key, 'script': fname, 'pattern': 'EXIT_ONLY_ON_CRASH',
                'detail': ('every non-zero exit sits inside an except handler, '
                           'so this stage can fail on an exception but not on '
                           'a finding'),
            })
            rec['verdict'] = 'DEFECT'
        else:
            rec['verdict'] = 'OK'
        records.append(rec)

    gates = [r for r in records if r.get('role') == 'gate']
    ok = [r for r in gates if r.get('verdict') == 'OK']
    print('\n  stages wired      : %d' % len(stages))
    print('  classified gates  : %d' % len(gates))
    print('  gates that can FAIL: %d' % len(ok))
    print('  defects           : %d' % len(defects))

    if defects:
        print('\n  ' + '-' * 64)
        for d in defects:
            print('  [FAIL] %-16s %s' % (d['stage'], d['script']))
            print('         %s: %s' % (d['pattern'], d['detail']))
        print('  ' + '-' * 64)
        print('  A gate in this list is reported GREEN by the runner no matter')
        print('  what it finds. Its stage count is not evidence of anything.')
    else:
        print('\n  [OK] every wired gate can return a non-zero exit on a finding')

    payload = {
        'generated': __import__('datetime').date.today().isoformat(),
        'runner': os.path.relpath(RUNNER, ROOT).replace('\\', '/'),
        'stages_wired': len(stages),
        'gates_classified': len(gates),
        'gates_that_can_fail': len(ok),
        'defects': defects,
        'records': records,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=2)
    print('  -> %s' % os.path.relpath(OUT, ROOT).replace('\\', '/'))

    return 1 if defects else 0


if __name__ == '__main__':
    sys.exit(main())
