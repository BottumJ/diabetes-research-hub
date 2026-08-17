#!/usr/bin/env python3
"""
git_commit_safe.py -- commit the Diabetes Research Hub from the sandbox despite the
OneDrive mount's inability to unlink files inside .git/.

BACKGROUND (root-caused 2026-08-17, replacing a wrong 3-week-old diagnosis)
---------------------------------------------------------------------------
The failure was recorded for three weeks as "a stale .git/index.lock that needs one
manual delete on the Windows host". That is wrong, and the wrongness matters: a
host-side delete fixes exactly ONE run. Evidence:

  * unlink() inside .git/ is denied at EVERY file age. Tested by creating a file and
    deleting it after 0s, 20s and 60s -- BLOCKED in all three cases. It is not a
    settling/OneDrive-handle race.
  * Therefore git's standard atomic write (create foo.lock -> rename over foo) leaves
    a fresh lock behind on every single invocation, for the index AND for refs
    (.git/HEAD.lock, .git/refs/heads/main.lock).
  * Corroboration: ~150 renamed lock corpses had accumulated in .git/ since April --
    one per daily run, each the residue of a "fix" that only lasted a day.

WHAT ACTUALLY WORKS
-------------------
Two operations ARE permitted on the mount: creating a new file, and rename-over an
existing file. Only unlink is denied. So:

  1. Keep the index OFF the mount        -> GIT_INDEX_FILE=/tmp/...
  2. Build the commit with plumbing      -> write-tree / commit-tree (no index lock)
  3. Move the ref by rename-over         -> write .git/refs/heads/<branch> directly
                                            instead of `git update-ref`

Note that `git commit` succeeds only intermittently here; the plumbing path is
deterministic. Prefer this script.

WHAT THIS SCRIPT CANNOT DO
--------------------------
Push. The sandbox holds no GitHub credential, so `git push` fails with
"could not read Username for 'https://github.com'". That is a separate and much
smaller problem than the lock issue. Run on the Windows host:

    cd C:\\Users\\justi\\OneDrive\\Diabetes_Research ; git push origin main

Usage:  python Analysis/Scripts/git_commit_safe.py -m "commit message"
        python Analysis/Scripts/git_commit_safe.py -m "msg" --branch main
"""

import argparse
import os
import re
import subprocess
import sys
import time

SHA_RE = re.compile(rb"\b[0-9a-f]{40}\b")


def run(args, env=None, cwd=None):
    """Run a git command. Returns (rc, stdout_bytes, stderr_bytes)."""
    p = subprocess.run(args, capture_output=True, env=env, cwd=cwd)
    return p.returncode, p.stdout, p.stderr


def last_sha(blob):
    """Extract a 40-char SHA from output that git may have polluted with warnings.

    `unable to unlink ... tmp_obj_*` warnings are emitted on stdout by write-tree and
    commit-tree on this mount, so naive `.strip()` yields a non-SHA and the next
    command dies with "not a valid SHA1". This is the single most common way the
    workaround silently breaks.
    """
    found = SHA_RE.findall(blob)
    return found[-1].decode() if found else None


def clear_locks(repo):
    """Rename stale lock files out of the way. Rename is permitted; unlink is not."""
    cleared = []
    candidates = [
        os.path.join(repo, ".git", "index.lock"),
        os.path.join(repo, ".git", "HEAD.lock"),
    ]
    refs_dir = os.path.join(repo, ".git", "refs", "heads")
    if os.path.isdir(refs_dir):
        for name in os.listdir(refs_dir):
            if name.endswith(".lock"):
                candidates.append(os.path.join(refs_dir, name))
    for path in candidates:
        if not os.path.exists(path):
            continue
        try:
            os.rename(path, "%s.z_%d" % (path, time.time_ns()))
            cleared.append(os.path.basename(path))
        except OSError:
            # Renames are occasionally refused too; the plumbing path does not
            # depend on the lock being gone, so this is not fatal.
            pass
    return cleared


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--message", required=True)
    ap.add_argument("--branch", default="main")
    ap.add_argument("--repo", default=os.getcwd())
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(os.path.join(repo, ".git")):
        sys.exit("[FAIL] not a git repository: %s" % repo)

    env = dict(os.environ)
    env["GIT_INDEX_FILE"] = "/tmp/gitidx_safe_%d" % os.getpid()

    cleared = clear_locks(repo)
    if cleared:
        print("[..] cleared stale locks: %s" % ", ".join(cleared))

    # Seed the off-mount index from the on-mount one so `add -A` diffs correctly.
    src = os.path.join(repo, ".git", "index")
    if os.path.exists(src):
        with open(src, "rb") as f_in, open(env["GIT_INDEX_FILE"], "wb") as f_out:
            f_out.write(f_in.read())

    rc, _, err = run(["git", "add", "-A"], env=env, cwd=repo)
    if rc != 0:
        sys.exit("[FAIL] git add: %s" % err.decode(errors="replace")[:500])

    rc, out, _ = run(["git", "diff", "--cached", "--name-only"], env=env, cwd=repo)
    staged = [l for l in out.decode(errors="replace").splitlines() if l.strip()]
    if not staged:
        print("[OK] nothing to commit; working tree matches HEAD.")
        return 0
    print("[..] staged %d file(s)" % len(staged))

    rc, out, err = run(["git", "write-tree"], env=env, cwd=repo)
    tree = last_sha(out) or last_sha(err)
    if not tree:
        sys.exit("[FAIL] write-tree produced no SHA: %s" % err.decode(errors="replace")[:500])
    print("[..] tree   %s" % tree)

    rc, out, _ = run(["git", "rev-parse", "HEAD"], env=env, cwd=repo)
    parent = last_sha(out)
    if not parent:
        sys.exit("[FAIL] could not resolve HEAD")

    p = subprocess.run(
        ["git", "commit-tree", tree, "-p", parent],
        input=args.message.encode("utf-8"),
        capture_output=True, env=env, cwd=repo,
    )
    commit = last_sha(p.stdout) or last_sha(p.stderr)
    if not commit:
        sys.exit("[FAIL] commit-tree produced no SHA: %s" % p.stderr.decode(errors="replace")[:500])
    print("[..] commit %s" % commit)

    # Move the ref by rename-over. `git update-ref` would need <ref>.lock and fails here.
    ref_path = os.path.join(repo, ".git", "refs", "heads", args.branch)
    tmp_path = os.path.join(repo, ".git", "refs", "heads", ".%s.new" % args.branch)
    with open(tmp_path, "w", encoding="utf-8") as fh:
        fh.write(commit + "\n")
    os.rename(tmp_path, ref_path)

    rc, out, _ = run(["git", "rev-parse", args.branch], env=env, cwd=repo)
    if last_sha(out) != commit:
        sys.exit("[FAIL] ref did not move; %s still at %s" % (args.branch, out.decode()[:60]))
    print("[OK] %s -> %s" % (args.branch, commit[:8]))

    rc, out, _ = run(["git", "rev-list", "--count", "origin/%s..%s" % (args.branch, args.branch)],
                     env=env, cwd=repo)
    ahead = out.decode(errors="replace").strip() or "?"
    print("[!!] %s commit(s) ahead of origin. Push needs host credentials:" % ahead)
    print("     cd C:\\Users\\justi\\OneDrive\\Diabetes_Research ; git push origin main")

    try:
        os.remove(env["GIT_INDEX_FILE"])
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
