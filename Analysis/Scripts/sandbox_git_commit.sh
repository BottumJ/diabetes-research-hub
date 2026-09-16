#!/usr/bin/env bash
# sandbox_git_commit.sh — commit from the Linux sandbox on the OneDrive mount.
#
# Added 2026-09-16, after seven runs (2026-09-09 .. 2026-09-15) recorded "git is
# unwritable from the sandbox" and escalated it to the user as a P0 requiring a
# Windows-side Remove-Item. It did not require one. The diagnosis was too coarse.
#
# WHAT IS ACTUALLY FORBIDDEN ON THIS MOUNT IS *UNLINK*, AND NOTHING ELSE.
#     rm    .git/anything   -> EPERM  "Operation not permitted"
#     touch .git/anything   -> works
#     mv    .git/a .git/b   -> works
#
# Git's lock protocol is: create X.lock, write it, rename X.lock -> X. Creation
# and rename both work here, so git can commit perfectly well. What breaks is
# only the cleanup of a lock left behind by an interrupted earlier run, because
# removing it needs unlink. Two such locks matter:
#
#   .git/index.lock  taken to protect the index git is about to write. Point
#                    GIT_INDEX_FILE at a path OUTSIDE the mount and git never
#                    touches that lock at all.
#   .git/HEAD.lock   taken to move the branch ref. There is no env var for it,
#                    but it can be RENAMED out of the way, which is permitted.
#                    (The .git directory already holds a dozen HEAD.lock.* files
#                    from prior runs rediscovering this by hand.)
#
# Usage:  bash Analysis/Scripts/sandbox_git_commit.sh "commit message"
#
# This does NOT push. Push fails for an unrelated and genuine reason: the remote
# is HTTPS with no credential helper, no ~/.git-credentials and no GH_TOKEN in
# the sandbox. That half still needs a human or a provisioned PAT.

set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
MSG="${1:?usage: sandbox_git_commit.sh \"commit message\"}"
STAMP="$(date +%Y%m%d_%H%M%S)"

cd "$REPO" || exit 1

# 1. An index outside the mount, seeded from the real one so staging is incremental.
ALT="$(mktemp -u /tmp/gitindex_XXXXXX)"
[ -f .git/index ] && cp .git/index "$ALT"
export GIT_INDEX_FILE="$ALT"

# 2. Rename any stale HEAD.lock aside. Renaming is permitted; unlinking is not.
if [ -e .git/HEAD.lock ]; then
    mv .git/HEAD.lock ".git/HEAD.lock.stale_$STAMP" 2>/dev/null \
        && echo "  moved stale .git/HEAD.lock aside (cannot unlink on this mount)"
fi

# 3. Stage. The "unable to unlink .git/objects/*/tmp_obj_*" warnings are cosmetic:
#    the object is written by rename first, and only the temp cleanup fails. Blobs
#    read back correctly (verified with git cat-file on 2026-09-16).
git add -A 2>&1 | grep -v "unable to unlink" | grep -v "^warning: $"

if git diff --cached --quiet; then
    echo "  nothing staged; no commit made"
    rm -f "$ALT"
    exit 0
fi

# NOTE (fixed on first execution, 2026-09-16): `RC=$?` after a pipeline captures
# the status of the LAST element - here `grep`, which exits 1 when it filters out
# every line, i.e. exactly when the commit was clean. The script's own first run
# committed successfully and then reported "COMMIT FAILED". Read git's status
# directly instead of the pipeline's.
git -c user.name="Diabetes Research Agent" \
    -c user.email="justin.bottum@gmail.com" \
    commit -q -m "$MSG" > /tmp/_sgc_out 2>&1
RC=$?
grep -v "unable to unlink" /tmp/_sgc_out | head -20
rm -f /tmp/_sgc_out

rm -f "$ALT"

if [ "$RC" -eq 0 ]; then
    echo "  committed: $(git log --oneline -1)"
    echo "  unpushed commits: $(git rev-list --count origin/main..HEAD 2>/dev/null || echo '?')"
    echo "  NOT PUSHED - no credential in the sandbox. Run 'git push' from Windows."
else
    echo "  COMMIT FAILED (rc=$RC) - this is a NEW failure mode, not the lock problem."
fi
exit "$RC"
