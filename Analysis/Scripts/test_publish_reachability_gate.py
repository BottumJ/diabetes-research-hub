#!/usr/bin/env python3
"""Regression fixture: does the publish-reachability gate go GREEN when fixed?

WHY THIS EXISTS
---------------
audit_publish_reachability.py is RED on the first day it ships, and will stay
red until a human pushes. That is the correct behaviour and it is also the
dangerous kind of gate: an alarm that has never been observed to turn off is
indistinguishable from an alarm that is stuck, and the repo's own history says
what happens next - the push failure was noticed in eleven run summaries and
became background noise every time.

So the gate has to be shown to have BOTH properties before it is worth
anything:

    sensitivity   it fails when the site is behind, diverged, or dirty
    specificity   it PASSES when the site is level and clean

Only the second one is unobservable in this repo right now, and it is the one
that makes the red state meaningful. Without it, "the publish gate is red"
carries no information.

HOW
---
Builds throwaway git repositories in a temp directory - a bare "remote" and a
clone - and drives the gate against them by pointing its module-level ROOT at
the clone. Touches no file in this repository and reaches no network.

Five cases:

    1  level + clean              -> expect PASS   (specificity: the one that matters)
    2  clone ahead of remote      -> expect PUBLISH_BEHIND, with the reader-facing
                                     file counts correct
    3  remote ahead of clone      -> expect PUBLISH_DIVERGED
    4  uncommitted file in docs/  -> expect UNCOMMITTED_PUBLISH
    5  unreachable remote         -> expect FETCH_FAILED (unknown is not clean)

Exit codes: 0 all cases behave, 1 any case misbehaves.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GATE_PATH = os.path.join(SCRIPT_DIR, 'audit_publish_reachability.py')

ENV = dict(os.environ)
ENV.update({
    'GIT_AUTHOR_NAME': 'fixture', 'GIT_AUTHOR_EMAIL': 'fixture@example.invalid',
    'GIT_COMMITTER_NAME': 'fixture', 'GIT_COMMITTER_EMAIL': 'fixture@example.invalid',
    'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_SYSTEM': os.devnull,
})


def git(repo, *args):
    r = subprocess.run(['git', *args], cwd=repo, capture_output=True,
                       text=True, env=ENV, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)} failed in {repo}: {r.stderr}')
    return r.stdout


def load_gate():
    """Fresh module instance per case - the gate holds ROOT at module level."""
    spec = importlib.util.spec_from_file_location('_pubgate', GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_gate(clone, report_dir):
    mod = load_gate()
    mod.ROOT = clone
    mod.REPORT = os.path.join(report_dir, 'publish_reachability_audit.json')
    code = mod.main()
    import json
    with open(mod.REPORT, encoding='utf-8') as fh:
        return code, json.load(fh)


def write(repo, rel, text):
    path = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)


def build_pair(tmp, n_docs=3):
    """A bare remote and a clone, level with each other, with a docs/ root."""
    remote = os.path.join(tmp, 'remote.git')
    seed = os.path.join(tmp, 'seed')
    clone = os.path.join(tmp, 'clone')

    git(tmp, 'init', '--bare', '--initial-branch=main', remote)
    git(tmp, 'init', '--initial-branch=main', seed)
    for i in range(n_docs):
        write(seed, f'docs/page{i}.html', f'<html>v1 page {i}</html>\n')
    git(seed, 'add', '-A')
    git(seed, 'commit', '-m', 'seed')
    git(seed, 'remote', 'add', 'origin', remote)
    git(seed, 'push', 'origin', 'main')

    git(tmp, 'clone', remote, clone)
    git(clone, 'checkout', 'main')
    return remote, seed, clone


def kinds(report):
    return sorted(f['kind'] for f in report.get('findings', []))


def main():
    failures = []
    results = []

    def check(label, condition, detail=''):
        results.append((label, condition, detail))
        if not condition:
            failures.append(f'{label}: {detail}')

    # --- CASE 1: level and clean -> PASS (specificity) --------------------
    with tempfile.TemporaryDirectory() as tmp:
        _remote, _seed, clone = build_pair(tmp)
        code, rep = run_gate(clone, tmp)
        check('case1 level+clean exits 0', code == 0, f'exit {code}, {kinds(rep)}')
        check('case1 no findings', rep.get('findings') == [], str(kinds(rep)))
        check('case1 counts level', rep.get('commits_unpushed') == 0,
              str(rep.get('commits_unpushed')))

    # --- CASE 2: clone ahead -> PUBLISH_BEHIND with correct file counts ---
    with tempfile.TemporaryDirectory() as tmp:
        _remote, _seed, clone = build_pair(tmp, n_docs=3)
        write(clone, 'docs/page0.html', '<html>v2 page 0</html>\n')   # stale for reader
        write(clone, 'docs/page1.html', '<html>v2 page 1</html>\n')   # stale for reader
        write(clone, 'docs/brand_new.html', '<html>new</html>\n')     # 404 for reader
        git(clone, 'add', '-A')
        git(clone, 'commit', '-m', 'local work that never reached the site')
        code, rep = run_gate(clone, tmp)
        check('case2 exits 1', code == 1, f'exit {code}')
        check('case2 flags PUBLISH_BEHIND', 'PUBLISH_BEHIND' in kinds(rep), str(kinds(rep)))
        check('case2 counts the unpushed commit', rep.get('commits_unpushed') == 1,
              str(rep.get('commits_unpushed')))
        div = rep.get('publish_root_divergence', {})
        check('case2 sees 1 file a reader 404s',
              len(div.get('missing_for_reader', [])) == 1,
              str(div.get('missing_for_reader')))
        check('case2 sees 2 stale files',
              len(div.get('stale_for_reader', [])) == 2,
              str(div.get('stale_for_reader')))
        check('case2 reports 4 local files, 3 remote',
              div.get('files_local') == 4 and div.get('files_on_remote') == 3,
              f"{div.get('files_local')} local / {div.get('files_on_remote')} remote")
        check('case2 reports 1 of 4 correct for a reader',
              div.get('files_correct_for_reader') == 1,
              str(div.get('files_correct_for_reader')))

    # --- CASE 3: remote ahead -> PUBLISH_DIVERGED -------------------------
    with tempfile.TemporaryDirectory() as tmp:
        _remote, seed, clone = build_pair(tmp)
        write(seed, 'docs/page0.html', '<html>someone else published</html>\n')
        git(seed, 'add', '-A')
        git(seed, 'commit', '-m', 'published elsewhere')
        git(seed, 'push', 'origin', 'main')
        code, rep = run_gate(clone, tmp)
        check('case3 exits 1', code == 1, f'exit {code}')
        check('case3 flags PUBLISH_DIVERGED', 'PUBLISH_DIVERGED' in kinds(rep), str(kinds(rep)))
        check('case3 does NOT flag PUBLISH_BEHIND',
              'PUBLISH_BEHIND' not in kinds(rep), str(kinds(rep)))

    # --- CASE 4: uncommitted file under docs/ -> UNCOMMITTED_PUBLISH ------
    with tempfile.TemporaryDirectory() as tmp:
        _remote, _seed, clone = build_pair(tmp)
        write(clone, 'docs/page0.html', '<html>edited, never committed</html>\n')
        code, rep = run_gate(clone, tmp)
        check('case4 exits 1', code == 1, f'exit {code}')
        check('case4 flags UNCOMMITTED_PUBLISH',
              'UNCOMMITTED_PUBLISH' in kinds(rep), str(kinds(rep)))
        check('case4 lists the dirty file',
              any('page0' in p for p in rep.get('uncommitted_publish_files', [])),
              str(rep.get('uncommitted_publish_files')))

    # --- CASE 5: unreachable remote -> FETCH_FAILED, not silence ----------
    with tempfile.TemporaryDirectory() as tmp:
        remote, _seed, clone = build_pair(tmp)
        shutil.rmtree(remote)          # remote vanishes; fetch cannot succeed
        code, rep = run_gate(clone, tmp)
        check('case5 exits 1 (unknown is not clean)', code == 1, f'exit {code}')
        check('case5 flags FETCH_FAILED', 'FETCH_FAILED' in kinds(rep), str(kinds(rep)))
        check('case5 records fetch_ok False', rep.get('fetch_ok') is False,
              str(rep.get('fetch_ok')))

    print('\n' + '=' * 60)
    print('  PUBLISH REACHABILITY GATE - REGRESSION FIXTURE')
    print('=' * 60)
    for label, ok, detail in results:
        mark = 'PASS' if ok else 'FAIL'
        print(f'  [{mark}] {label}' + (f'   ({detail})' if not ok else ''))

    if failures:
        print(f'\n  [FAIL] {len(failures)} of {len(results)} assertions failed.')
        return 1
    print(f'\n  [OK] {len(results)}/{len(results)} assertions.')
    print('       Sensitivity: fails on behind, diverged, dirty and unreachable.')
    print('       Specificity: PASSES when the site is level and clean - so the')
    print('       red state in this repo is information, not a stuck alarm.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
