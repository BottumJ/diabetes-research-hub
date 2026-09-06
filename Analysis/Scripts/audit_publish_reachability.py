#!/usr/bin/env python3
"""Does the thing this pipeline audits match the thing a reader loads?

WHY THIS EXISTS
---------------
Every publish-side assertion this repo owns validates `docs/` IN THE WORKING
TREE. `docs/` is the GitHub Pages root, so the working-tree copy is the thing
this agent builds; the thing a reader loads is `origin/main:docs/`. Those have
been different objects since 2026-04-20.

Measured 2026-09-06:

    main is 101 commits ahead of origin/main
    origin/main tip f7e976f, 2026-04-20 -> 139 days
    docs/ in the working tree      39 files
    docs/ on origin/main           35 files
      4 files a reader gets 404 for  (Islet_Drug_Repurposing.html,
                                      Prediction_Ledger.html,
                                      Reports/literature_gap_report.md,
                                      Reports/pubmed_recent_summary.md)
     34 files a reader gets a stale copy of
      1 file of 39 is what this pipeline thinks it published

So on 2026-09-05 the runner reported "1400/1400 published links resolve, 0
dead" and "both published reports pass the freshness gate at 0 days". Both
statements are TRUE about the working tree and FALSE about the site. 38 of 39
published files are wrong or absent for a real reader, and 71 green stages said
nothing, because not one of them ever looked at the remote.

That is not an oversight in any single gate. It is the shared blind spot of all
of them: they take the publish root's LOCATION as the definition of "published"
when the actual definition is "reachable by someone who is not this agent". A
gate that never leaves the working tree cannot fail for the one reason that
matters most.

The failure was also NOTICED ELEVEN TIMES without changing anything. Run
summaries on 2026-05-24, 06-03, 06-06, 06-09, 07-01, 07-02, 07-11, 07-18,
07-25, 08-03 and 08-17 each record a push failure and move on. A finding that
does not change what the next run DOES is not memory, it is a diary. This gate
is the conversion: from now on the pipeline cannot go green while the site is
stale, so the condition has to be fixed rather than re-noticed.

WHAT THIS GATE ASSERTS
----------------------
    PUBLISH_BEHIND      origin/main is behind main. The site does not have work
                        this repo has committed. Reports the commit count, the
                        age of the remote tip, and - the number that matters -
                        how many files under the publish root a reader would
                        get stale or 404.
    PUBLISH_DIVERGED    origin/main has commits main does not. Someone else
                        published; a push would be rejected or would clobber.
    UNCOMMITTED_PUBLISH files under docs/ are modified or untracked. Even a
                        successful push would not carry them, so a green
                        publish-side gate is again describing a private object.
    FETCH_FAILED        the remote could not be read, so publish state is
                        UNKNOWN. Unknown is not clean, and this exits non-zero
                        on purpose: the entire defect being closed here is a
                        pipeline reporting success it had not verified.

Read-only. Runs `git fetch` (read access needs no credential on a public
remote - verified 2026-09-06, exit 0) and otherwise only inspects refs. Never
pushes: a scheduled agent silently publishing on the user's behalf is a
different and worse problem than a stale site.

Exit codes: 0 clean, 1 findings.
"""
import json
import os
import subprocess
import sys
from datetime import date, datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
ROOT = os.path.dirname(BASE)
REPORT = os.path.join(BASE, 'Results', 'publish_reachability_audit.json')

PUBLISH_ROOT = 'docs'
REMOTE = 'origin'
BRANCH = 'main'
FETCH_TIMEOUT = 90


def git(*args, cwd=None, timeout=30):
    """Run a git command. Returns (exit_code, stdout, stderr) - never raises.

    cwd defaults to None and is resolved to the module-level ROOT AT CALL TIME,
    not bound as a default argument. This is not a style preference: the first
    run of test_publish_reachability_gate.py failed 14 of 19 assertions because
    `cwd=ROOT` in the signature was evaluated at import, so redirecting
    mod.ROOT at a temp clone left every git call pointed at this repository.
    The gate then reported this repo's 101 unpushed commits for all five
    fixture cases and looked like it was "working".

    That is the headline defect of this whole gate, reproduced one level down:
    a check whose subject is not the object it claims to describe. Left as a
    default argument it would have been invisible, because the answers it
    returned were true - just about the wrong repository.
    """
    cwd = cwd if cwd is not None else ROOT
    try:
        r = subprocess.run(['git', *args], cwd=cwd, capture_output=True,
                           text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, '', f'timeout after {timeout}s'
    except OSError as exc:
        return 127, '', str(exc)


def remote_tip_age_days(ref):
    code, out, _ = git('log', '-1', '--format=%cI', ref)
    if code != 0 or not out:
        return None, None
    try:
        tip = datetime.fromisoformat(out)
    except ValueError:
        return None, None
    now = datetime.now(timezone.utc)
    return tip.date().isoformat(), (now - tip).days


def publish_root_divergence(remote_ref):
    """How many files under the publish root would a reader get wrong?

    This is the translation step the eleven prior notices were missing. A
    commit count is an engineering fact; "34 stale pages and 4 that 404" is
    the reader-facing consequence, and it is the one that justifies failing
    the pipeline.
    """
    code, out, _ = git('diff', '--name-status', remote_ref, 'HEAD', '--',
                       PUBLISH_ROOT + '/')
    if code != 0:
        return None
    added, modified, deleted = [], [], []
    for line in out.splitlines():
        parts = line.split('\t')
        if len(parts) < 2:
            continue
        status, path = parts[0][:1], parts[-1]
        if status == 'A':
            added.append(path)       # exists locally, 404 for a reader
        elif status == 'D':
            deleted.append(path)     # reader still served a file we removed
        else:
            modified.append(path)    # reader served an older copy

    code, out, _ = git('ls-tree', '-r', '--name-only', remote_ref,
                       '--', PUBLISH_ROOT + '/')
    remote_count = len([p for p in out.splitlines() if p.strip()]) if code == 0 else None

    local_total = 0
    for dirpath, _dirs, files in os.walk(os.path.join(ROOT, PUBLISH_ROOT)):
        local_total += len(files)

    wrong = len(added) + len(modified) + len(deleted)
    return {
        'files_local': local_total,
        'files_on_remote': remote_count,
        'missing_for_reader': sorted(added),
        'stale_for_reader': sorted(modified),
        'removed_but_still_served': sorted(deleted),
        'files_wrong_for_reader': wrong,
        'files_correct_for_reader': (local_total - wrong) if local_total else None,
    }


def uncommitted_under_publish_root():
    code, out, _ = git('status', '--porcelain', '--', PUBLISH_ROOT + '/')
    if code != 0:
        return []
    return [ln[3:] for ln in out.splitlines() if ln.strip()]


def main():
    findings = []
    remote_ref = f'{REMOTE}/{BRANCH}'
    result = {
        'audit': 'publish_reachability',
        'run_date': date.today().isoformat(),
        'publish_root': PUBLISH_ROOT,
        'remote_ref': remote_ref,
    }

    print('=' * 60)
    print('  PUBLISH REACHABILITY GATE')
    print('=' * 60)

    # --- 1. Read the remote. Read access needs no credential. -------------
    code, _out, err = git('fetch', REMOTE, BRANCH, timeout=FETCH_TIMEOUT)
    result['fetch_ok'] = (code == 0)
    if code != 0:
        result['fetch_error'] = err[:500]
        findings.append({
            'kind': 'FETCH_FAILED',
            'detail': f'could not read {remote_ref}: {err[:200]}',
            'consequence': 'publish state is UNKNOWN; no publish-side gate in '
                           'this pipeline can be trusted this run',
        })
        result['findings'] = findings
        _write(result)
        _print_findings(findings)
        return 1

    # --- 2. Ahead / behind ------------------------------------------------
    code, out, _ = git('rev-list', '--left-right', '--count',
                       f'{remote_ref}...HEAD')
    if code != 0:
        findings.append({
            'kind': 'FETCH_FAILED',
            'detail': f'{remote_ref} not resolvable after a successful fetch',
            'consequence': 'publish state is UNKNOWN',
        })
        result['findings'] = findings
        _write(result)
        _print_findings(findings)
        return 1

    behind_remote, ahead_of_remote = (int(x) for x in out.split())
    tip_date, tip_age = remote_tip_age_days(remote_ref)
    result.update({
        'commits_unpushed': ahead_of_remote,
        'commits_only_on_remote': behind_remote,
        'remote_tip_date': tip_date,
        'remote_tip_age_days': tip_age,
    })
    print(f'  {remote_ref} tip: {tip_date} ({tip_age} days old)')
    print(f'  commits on main not on the site: {ahead_of_remote}')

    if ahead_of_remote > 0:
        div = publish_root_divergence(remote_ref) or {}
        result['publish_root_divergence'] = div
        wrong = div.get('files_wrong_for_reader')
        total = div.get('files_local')
        missing = len(div.get('missing_for_reader', []))
        stale = len(div.get('stale_for_reader', []))
        detail = (f'{ahead_of_remote} commits unpushed; {remote_ref} tip is '
                  f'{tip_date} ({tip_age} days old)')
        if wrong is not None and total:
            detail += (f'; {wrong} of {total} files under {PUBLISH_ROOT}/ are '
                       f'wrong for a reader ({missing} return 404, '
                       f'{stale} are stale)')
        findings.append({
            'kind': 'PUBLISH_BEHIND',
            'detail': detail,
            'consequence': 'every other publish-side assertion in this pipeline '
                           'describes the working tree, not the site',
            'action': 'push from a host that holds credentials, or provision a '
                      'PAT / gh credential for the scheduled task',
        })
        if wrong is not None and total:
            print(f'  reader-facing: {wrong}/{total} files under {PUBLISH_ROOT}/ '
                  f'wrong ({missing} x 404, {stale} x stale)')

    if behind_remote > 0:
        findings.append({
            'kind': 'PUBLISH_DIVERGED',
            'detail': f'{behind_remote} commits exist on {remote_ref} that main '
                      f'does not have',
            'consequence': 'a push would be rejected, or would need a merge no '
                           'gate has reviewed',
        })

    # --- 3. Work that even a push would not carry -------------------------
    dirty = uncommitted_under_publish_root()
    result['uncommitted_publish_files'] = dirty
    if dirty:
        findings.append({
            'kind': 'UNCOMMITTED_PUBLISH',
            'detail': f'{len(dirty)} file(s) under {PUBLISH_ROOT}/ are modified '
                      f'or untracked: {", ".join(dirty[:5])}'
                      + (' ...' if len(dirty) > 5 else ''),
            'consequence': 'these would not reach the site even if the push '
                           'succeeded',
        })

    result['findings'] = findings
    _write(result)

    if not findings:
        print(f'\n  [OK] {remote_ref} is level with main and {PUBLISH_ROOT}/ is '
              f'clean.')
        print('       What this pipeline audits is what a reader loads.')
        return 0

    _print_findings(findings)
    return 1


def _write(result):
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(result, fh, indent=2)
    print(f'\n  Report: {os.path.relpath(REPORT, ROOT)}')


def _print_findings(findings):
    print(f'\n  [FAIL] {len(findings)} finding(s):')
    for f in findings:
        print(f'\n   {f["kind"]}')
        print(f'     {f["detail"]}')
        print(f'     -> {f["consequence"]}')
        if f.get('action'):
            print(f'     ACTION: {f["action"]}')
    print('\n  This gate fails on purpose. A pipeline that reports a successful')
    print('  publish it did not perform is the defect; a red stage is the fix.')


if __name__ == '__main__':
    sys.exit(main())
