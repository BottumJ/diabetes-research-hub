#!/usr/bin/env python3
"""SPENT one-shot script from the 2026-08-18 iteration run.

Its state updates have been applied and saved to
Analysis/Results/agent_state.json. Re-running it would only re-append the same
run_history entry and audit_notes, so it is neutralised rather than deleted:
the OneDrive mount denies unlink() inside the repo (see git_commit_safe.py),
so files can be overwritten but not removed from the sandbox.

Safe to delete from the Windows host.
"""
raise SystemExit(
    '_run_2026_08_18.py is a spent one-shot script. Its changes are already in '
    'agent_state.json. Delete it from the Windows host.'
)
