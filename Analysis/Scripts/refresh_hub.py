#!/usr/bin/env python3
"""
refresh_hub.py — Run all daily refresh scripts, then commit and push to GitHub.

Sequence:
  1. baseline_clinical_trials.py       (ClinicalTrials.gov snapshot)
  2. baseline_pubmed_alerts.py         (PubMed 30-day rolling window)
  3. hub_monitor.py                    (file scan + snapshot diffs)
  4. project1_literature_gap_analysis.py  (gap matrix + report)
  5. git add / commit / push           (auto-summarize changes)

Usage (from the repo root, C:\\Users\\justi\\OneDrive\\Diabetes_Research):
  python Analysis\\Scripts\\refresh_hub.py
  python Analysis\\Scripts\\refresh_hub.py --no-push         # commit locally, don't push
  python Analysis\\Scripts\\refresh_hub.py --no-commit       # scripts only, no git
  python Analysis\\Scripts\\refresh_hub.py --results-only    # only stage Analysis/Results/
  python Analysis\\Scripts\\refresh_hub.py --branch main     # push target (default: main)
  python Analysis\\Scripts\\refresh_hub.py --skip SCRIPT     # skip one refresh step
                                                             # (repeatable)

Exit codes: 0 = success, non-zero = any step failed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent            # Analysis/Scripts
REPO_ROOT = SCRIPT_DIR.parents[1]                       # repo root
GIT_DIR = REPO_ROOT / ".git"

REFRESH_SCRIPTS = [
    "baseline_clinical_trials.py",
    "resolve_predictions.py",        # science arm: score ledger vs fresh snapshot
    "build_prediction_ledger.py",    # science arm: rebuild ledger dashboard
    "baseline_pubmed_alerts.py",
    "hub_monitor.py",
    "project1_literature_gap_analysis.py",
]

# Scripts whose non-zero exit is a SIGNAL, not a failure.
# resolve_predictions.py returns 2 when a locked prediction's trial has posted
# results and awaits manual resolution -- that must not abort the daily chain.
TOLERATED_EXITS = {"resolve_predictions.py": (0, 2)}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def header(title: str) -> None:
    bar = "=" * 72
    print(f"\n{bar}\n {title}\n{bar}")


def run(cmd: list[str], cwd: Path = REPO_ROOT, check: bool = True,
        capture: bool = False) -> subprocess.CompletedProcess:
    """Run a command, streaming output unless capture=True."""
    print(f"$ {' '.join(str(c) for c in cmd)}")
    if capture:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    else:
        r = subprocess.run(cmd, cwd=cwd)
    if check and r.returncode != 0:
        err = f"Command failed (exit {r.returncode}): {' '.join(cmd)}"
        if capture and r.stderr:
            err += f"\nstderr: {r.stderr.strip()}"
        sys.exit(err)
    return r


def clear_git_locks(verbose: bool = True) -> int:
    """Remove stray *.lock files in .git/ (OneDrive sometimes leaves them)."""
    if not GIT_DIR.exists():
        return 0
    cleared = 0
    for lock in list(GIT_DIR.glob("*.lock")):
        try:
            lock.unlink()
            cleared += 1
            if verbose:
                print(f"  cleared stale lock: .git/{lock.name}")
        except OSError as e:
            print(f"  WARNING: could not remove {lock}: {e}")
    # Also check refs/ subtree (e.g., refs/heads/main.lock)
    refs_dir = GIT_DIR / "refs"
    if refs_dir.exists():
        for lock in refs_dir.rglob("*.lock"):
            try:
                lock.unlink()
                cleared += 1
                if verbose:
                    print(f"  cleared stale lock: {lock.relative_to(GIT_DIR).as_posix()}")
            except OSError as e:
                print(f"  WARNING: could not remove {lock}: {e}")
    return cleared


def git_has_changes(paths: list[str] | None = None) -> bool:
    cmd = ["git", "status", "--porcelain"]
    if paths:
        cmd += ["--"] + paths
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    return bool(r.stdout.strip())


def git_status_short(paths: list[str] | None = None) -> str:
    cmd = ["git", "status", "--short"]
    if paths:
        cmd += ["--"] + paths
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    return r.stdout


def git_try(cmd: list[str], retries: int = 3, delay: float = 2.0) -> int:
    """Run git command, retrying if we hit a lock race with OneDrive."""
    for attempt in range(1, retries + 1):
        print(f"$ {' '.join(cmd)}")
        r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        if r.stdout:
            print(r.stdout, end="")
        if r.returncode == 0:
            return 0
        stderr = (r.stderr or "").lower()
        if "index.lock" in stderr or "head.lock" in stderr or "cannot lock ref" in stderr:
            print(f"  lock collision (attempt {attempt}/{retries}); clearing + retrying in {delay}s")
            clear_git_locks(verbose=False)
            time.sleep(delay)
            continue
        # Other failure — print stderr and bail
        print(r.stderr, end="", file=sys.stderr)
        return r.returncode
    return r.returncode  # exhausted retries


def build_commit_message(status_output: str) -> tuple[str, str]:
    """Build (subject, body) commit message from a `git status --short` dump."""
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"Daily hub refresh {today}"

    added, modified, deleted, renamed = [], [], [], []
    for line in status_output.splitlines():
        if not line.strip():
            continue
        code = line[:2]
        path = line[3:].strip()
        if code.startswith("A") or code.startswith("??"):
            added.append(path)
        elif code.startswith("D"):
            deleted.append(path)
        elif code.startswith("R"):
            renamed.append(path)
        else:
            modified.append(path)

    def summarize_list(label: str, items: list[str], cap: int = 6) -> str | None:
        if not items:
            return None
        sample = items[:cap]
        extra = f" (+{len(items) - cap} more)" if len(items) > cap else ""
        return f"- {label} ({len(items)}): " + ", ".join(sample) + extra

    lines = [
        f"- Scripts run: {', '.join(REFRESH_SCRIPTS)}",
    ]
    for part in (
        summarize_list("added", added),
        summarize_list("modified", modified),
        summarize_list("deleted", deleted),
        summarize_list("renamed", renamed),
    ):
        if part:
            lines.append(part)
    body = "\n".join(lines)
    return subject, body


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-push", action="store_true", help="Commit but don't push.")
    ap.add_argument("--no-commit", action="store_true", help="Run scripts only; skip all git.")
    ap.add_argument("--results-only", action="store_true",
                    help="Only stage Analysis/Results/ (default: stage everything).")
    ap.add_argument("--branch", default="main", help="Push target branch (default: main).")
    ap.add_argument("--skip", action="append", default=[],
                    help="Skip a refresh script (e.g., --skip hub_monitor.py). Repeatable.")
    args = ap.parse_args()

    # 1. Run refresh scripts
    header("Running refresh scripts")
    for script in REFRESH_SCRIPTS:
        if script in args.skip:
            print(f"  SKIPPED: {script}")
            continue
        path = SCRIPT_DIR / script
        if not path.exists():
            sys.exit(f"Missing script: {path}")
        print(f"\n--- {script} ---")
        allowed = TOLERATED_EXITS.get(script, (0,))
        r = run([sys.executable, str(path)], cwd=REPO_ROOT, check=False)
        if r.returncode not in allowed:
            sys.exit(f"Command failed (exit {r.returncode}): {script}")
        if script == "resolve_predictions.py" and r.returncode == 2:
            print("  NOTE: a locked prediction's trial has posted results and "
                  "awaits manual resolution (see prediction_ledger_report.md).")

    if args.no_commit:
        header("Done (--no-commit set; git skipped)")
        return

    # 2. Git: clear any stale OneDrive locks first
    header("Git operations")
    if not GIT_DIR.exists():
        sys.exit(f"No .git/ directory at {REPO_ROOT}; not a git repo?")
    clear_git_locks()

    # 3. Check for changes
    stage_paths = ["Analysis/Results"] if args.results_only else None
    if not git_has_changes(stage_paths):
        print("No changes detected; nothing to commit. Done.")
        return

    # 4. Show status
    print("\nStatus preview:")
    print(git_status_short(stage_paths))

    # 5. Stage
    add_cmd = ["git", "add"]
    if args.results_only:
        add_cmd += ["Analysis/Results"]
    else:
        add_cmd += ["-A"]
    if git_try(add_cmd) != 0:
        sys.exit("git add failed after retries; aborting.")

    # 6. Capture staged status for message building (only staged items)
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-status"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    ).stdout
    # Convert name-status output into --short-ish for our summarizer
    synthetic_short = ""
    for line in staged.splitlines():
        if "\t" not in line:
            continue
        code, path = line.split("\t", 1)
        synthetic_short += f"{code:<2} {path}\n"

    if not synthetic_short.strip():
        print("Nothing got staged; skipping commit.")
        return

    subject, body = build_commit_message(synthetic_short)
    commit_cmd = ["git", "commit", "-m", subject, "-m", body]
    if git_try(commit_cmd) != 0:
        sys.exit("git commit failed after retries; aborting.")

    if args.no_push:
        header("Committed locally (--no-push set).")
        run(["git", "log", "-1", "--oneline"])
        return

    # 7. Push
    clear_git_locks(verbose=False)
    if git_try(["git", "push", "origin", args.branch]) != 0:
        sys.exit("git push failed. Resolve manually with `git push origin main`.")

    header("Refresh + push complete")
    run(["git", "log", "-1", "--oneline"])


if __name__ == "__main__":
    main()
