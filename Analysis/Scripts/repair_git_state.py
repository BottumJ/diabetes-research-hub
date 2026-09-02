#!/usr/bin/env python3
r"""RUN THIS ON YOUR WINDOWS MACHINE. The agent cannot.

WHAT IS WRONG
=============
Three separate problems, measured 2026-09-01. All three are in .git, none of
them touch your research data, and none of them can be fixed from the agent's
sandbox because the OneDrive mount denies unlink() inside .git at any file age.

1. NOTHING HAS EVER BEEN PUSHED.

       git rev-list --count origin/main..main   ->   96

   Ninety-six daily-iteration commits, the oldest dated 2026-04-21, exist only
   on this machine. .git/FETCH_HEAD does not exist, so the remote has never
   even been contacted since clone. Four and a half months of vetting, gate
   construction and citation repair has exactly one copy, on a disk. The run
   log has recorded "changes_pushed: false" every day since 2026-08-28 and the
   2026-08-17 run diagnosed the cause as "push blocked by credentials only" -
   correct, and then nobody supplied credentials, so the count kept climbing.

   This is the single largest risk in the project and it is not a research
   risk. Fixing it requires YOUR credentials, which is why it is in this file
   and not in an automated run.

2. THE INDEX HAS 60 STAGED DELETIONS OF FILES THAT EXIST ON DISK.

   `git status` reports 60 paths as "D " (staged for deletion) while every one
   of them is present in the working tree. They are precisely the outputs of
   the last four runs - the four monitor reports, the new audit result files,
   and the paper-library abstracts written by the 2026-08-28 miscitation repair
   (21719096 Orban, 28885622 Buzzetti).

   Cause: a previous run called `git add -A` while OneDrive had those files
   dehydrated (cloud-only, not materialised on disk). Git saw absent files and
   staged their deletion. The commit then failed on the lock, leaving the
   poisoned index in place.

   Consequence if ignored: the next `git commit` DELETES all 60 from the repo,
   including the evidence for the August miscitation repairs. This script
   unstages them rather than committing them.

3. .git HAS ACCUMULATED 176 JUNK LOCK FILES AND TWO PHANTOM BRANCHES.

   Because the mount denies unlink, five months of runs each RENAMED the lock
   file they could not delete, generating .git/HEAD.lock.stale_1779696981,
   .git/index.lock.delete-me, .git/index.lock.gone-20260519d and 173 more.
   .git is now 141 MB.

   Worse, two of those renames landed in .git/refs/heads/, so git now reports
   them as branches:

       main.lock.old_1786608612               -> 3fef88e (2026-07-31)
       main.lock.z_1786954612656090835        -> 9437b70 (2026-08-17)

   They are not branches. They are lock-file debris that git is parsing as
   refs, and they will be pushed as branches if you ever `git push --all`.

   There is also a live .git/index.lock created 2026-09-01 03:07 that blocks
   every index write until removed.

WHAT THIS SCRIPT DOES
=====================
Steps 1-3 are safe and local. Step 4 (push) is NOT run automatically - it
needs your credentials and it publishes; the script prints the command and
stops. Nothing here rewrites history, deletes a commit, or touches anything
outside .git except by unstaging.

Run:  python Analysis\Scripts\repair_git_state.py           (report only)
      python Analysis\Scripts\repair_git_state.py --apply   (make the changes)

BEFORE --apply: the script copies .git/index to .git/index.rescue_<date>. If
anything goes wrong, restore that file and you are back where you started.
"""

import argparse
import datetime
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GIT = os.path.join(REPO, '.git')
STAMP = datetime.date.today().isoformat()


def git(*args, check=False):
    r = subprocess.run(['git'] + list(args), cwd=REPO, capture_output=True,
                       text=True, encoding='utf-8', errors='replace')
    if check and r.returncode != 0:
        print(f'    ! git {" ".join(args)} -> {r.returncode}: {r.stderr.strip()[:200]}')
    return r


def section(n, title):
    print(f'\n{"=" * 72}\n{n}. {title}\n{"=" * 72}')


def clear_stale_locks(apply):
    section(1, 'STALE LOCKS AND LOCK DEBRIS')
    live = os.path.join(GIT, 'index.lock')
    if os.path.exists(live):
        print(f'  live index.lock present ({os.path.getmtime(live)}) - blocks all index writes')
        if apply:
            try:
                os.remove(live)
                print('    removed')
            except OSError as e:
                print(f'    ! could not remove: {e}')
                print('      close any open git client / VS Code, and retry')
    else:
        print('  no live index.lock')

    junk = [f for f in os.listdir(GIT)
            if '.lock.' in f or f.startswith('.stale_index.lock')
            or f.endswith(('.lock.bak', '.lock.old', '.lock.stale', '.lock.tmp',
                           '.lock.x', '.lock.s'))]
    junk = [f for f in junk if f not in ('index.lock', 'HEAD.lock')]
    size = sum(os.path.getsize(os.path.join(GIT, f)) for f in junk)
    print(f'  lock debris in .git root: {len(junk)} files, {size / 1024:.0f} KB')
    if apply and junk:
        attic = os.path.join(GIT, f'_lock_debris_{STAMP}')
        os.makedirs(attic, exist_ok=True)
        moved = 0
        for f in junk:
            try:
                shutil.move(os.path.join(GIT, f), os.path.join(attic, f))
                moved += 1
            except OSError:
                pass
        print(f'    moved {moved} into {os.path.relpath(attic, REPO)} '
              f'(delete that folder yourself once git still works)')


def clear_phantom_branches(apply):
    section(2, 'PHANTOM BRANCHES IN refs/heads')
    heads = os.path.join(GIT, 'refs', 'heads')
    phantom = [f for f in os.listdir(heads) if '.lock' in f]
    if not phantom:
        print('  none')
        return
    for f in phantom:
        ref = open(os.path.join(heads, f), encoding='utf-8').read().strip()
        print(f'  {f}  ->  {ref[:12]}')
    print('  These are lock-rename debris git is reading as branches.')
    print('  Their commits are already ancestors of main - nothing is lost.')
    if apply:
        attic = os.path.join(GIT, f'_phantom_refs_{STAMP}')
        os.makedirs(attic, exist_ok=True)
        for f in phantom:
            try:
                shutil.move(os.path.join(heads, f), os.path.join(attic, f))
                print(f'    moved {f}')
            except OSError as e:
                print(f'    ! {f}: {e}')


def fix_phantom_deletions(apply):
    section(3, 'STAGED DELETIONS OF FILES THAT EXIST ON DISK')
    r = git('status', '--porcelain')
    phantom = []
    for line in r.stdout.splitlines():
        if line.startswith('D  '):
            path = line[3:].strip().strip('"')
            if os.path.exists(os.path.join(REPO, path)):
                phantom.append(path)
    print(f'  staged deletions whose file is present on disk: {len(phantom)}')
    for p in phantom[:12]:
        print(f'    {p}')
    if len(phantom) > 12:
        print(f'    ... and {len(phantom) - 12} more')
    if not phantom:
        return
    print('\n  Committing as-is would DELETE these from the repo.')
    if apply:
        idx = os.path.join(GIT, 'index')
        if os.path.exists(idx):
            shutil.copy(idx, os.path.join(GIT, f'index.rescue_{STAMP}'))
            print(f'  index backed up to .git/index.rescue_{STAMP}')
        for i in range(0, len(phantom), 50):
            git('restore', '--staged', '--', *phantom[i:i + 50], check=True)
        still = sum(1 for line in git('status', '--porcelain').stdout.splitlines()
                    if line.startswith('D  '))
        print(f'  unstaged. remaining staged deletions: {still}')


def report_push(apply):
    section(4, 'THE 96 UNPUSHED COMMITS')
    ahead = git('rev-list', '--count', 'origin/main..main').stdout.strip() or '?'
    oldest = git('log', 'origin/main..main', '--format=%ad %s', '--date=short',
                 '--reverse').stdout.splitlines()
    print(f'  commits ahead of origin/main: {ahead}')
    if oldest:
        print(f'  oldest unpushed: {oldest[0][:100]}')
    print('  remote: ' + (git('remote', 'get-url', 'origin').stdout.strip() or '(none)'))
    print("""
  NOT DONE AUTOMATICALLY. Pushing publishes this repository and needs your
  GitHub credentials, so it is your call and your keystroke:

      cd "%s"
      git status                 # confirm step 3 above cleaned the index
      git add -A                 # only after confirming OneDrive files are
                                 # materialised - see note below
      git commit -m "Batch: daily iterations 2026-04-21..2026-09-01"
      git push origin main

  ONEDRIVE NOTE, because this is what caused problem 2: before `git add -A`,
  make sure the files are actually on disk and not cloud-only placeholders.
  Right-click the Diabetes_Research folder -> "Always keep on this device",
  wait for the sync to finish, THEN add. Otherwise git stages deletions for
  every dehydrated file all over again.

  Consider also setting, once:
      git config core.fsmonitor false
      git config core.untrackedCache false
  Both interact badly with a cloud-synced working tree.
""" % REPO)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true',
                    help='make the changes (default is report only)')
    a = ap.parse_args()
    print(f'Repo: {REPO}')
    print('MODE: APPLY' if a.apply else 'MODE: REPORT ONLY (pass --apply to change anything)')
    clear_stale_locks(a.apply)
    clear_phantom_branches(a.apply)
    fix_phantom_deletions(a.apply)
    report_push(a.apply)
    print('\nDone.' if a.apply else '\nNothing changed. Re-run with --apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
