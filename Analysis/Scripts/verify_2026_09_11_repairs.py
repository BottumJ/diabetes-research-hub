#!/usr/bin/env python3
"""
verify_2026_09_11_repairs.py

Written by the 2026-09-11 scheduled run, which had NO PYTHON: the Linux sandbox
failed to mount for the third consecutive day (Plan9 'share c is not mounted',
attributed to a Windows update released 2026-09-08). Every edit that run made
was made with file tools and was never executed or parsed.

This script is the missing verification step. Run it on Windows FIRST, before
run_quality_improvements.py, because it is cheap and it checks the two things
an unexecuted edit can break: JSON validity and Python syntax.

    python Analysis/Scripts/verify_2026_09_11_repairs.py

Exit code 0 = all checks pass. Non-zero = something needs attention.

WHAT IT CHECKS
  1. agent_state.json still parses as JSON, and the 2026-09-11 run record and
     the four new/updated queue items are present.
  2. The two edited builders still compile as Python.
  3. Each of the three repaired PMIDs has NO remaining un-annotated attachment
     in build_health_equity.py. This is the "re-grep the whole file" discipline
     added to the queue on 2026-09-09, applied mechanically.
  4. The self-confessed-doubt marker that motivated the new P1 gate item
     ('needs manual verification') is gone from the repaired file, and is
     reported repo-wide so the proposed gate's hit count is known before
     anyone wires it in.
  5. Step 4 credibility phrases, re-run as a script rather than by grep.

NOTE ON SCOPE: this does NOT rebuild anything. Until
run_quality_improvements.py runs, the generated HTML in Dashboards/ and
docs/Dashboards/ still contains every citation removed on 2026-09-09, 09-10
and 09-11. That divergence is the top P0 item.
"""

import ast
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "Analysis" / "Scripts"
STATE = REPO / "Analysis" / "Results" / "agent_state.json"

failures = []
warnings_ = []


def ok(msg):
    print(f"[OK]   {msg}")


def fail(msg):
    print(f"[FAIL] {msg}")
    failures.append(msg)


def warn(msg):
    print(f"[WARN] {msg}")
    warnings_.append(msg)


# ---------------------------------------------------------------- 1. state JSON
print("\n=== 1. agent_state.json integrity ===")
state = None
try:
    with open(STATE, encoding="utf-8") as fh:
        state = json.load(fh)
    ok(f"agent_state.json parses ({STATE.stat().st_size:,} bytes)")
except json.JSONDecodeError as exc:
    fail(f"agent_state.json DOES NOT PARSE: {exc}")
    print("\n  The 2026-09-11 run edited this file without being able to parse it.")
    print("  A backup of the last known-good state may exist alongside it.")
    sys.exit(1)
except OSError as exc:
    fail(f"agent_state.json unreadable: {exc}")
    sys.exit(1)

if state.get("last_run") == "2026-09-11":
    ok("last_run == 2026-09-11")
else:
    fail(f"last_run is {state.get('last_run')!r}, expected '2026-09-11'")

runs = state.get("run_history", [])
todays = [r for r in runs if isinstance(r, dict) and r.get("date") == "2026-09-11"]
if todays:
    ok(f"run_history contains the 2026-09-11 record ({len(runs)} runs total)")
else:
    fail("run_history has no 2026-09-11 record")

paper = state.get("papers", {}).get("37583402", {})
if paper.get("status") == "VETTED_DO_NOT_INGEST":
    ok("PMID 37583402 recorded as VETTED_DO_NOT_INGEST (not independent of 40111679)")
else:
    fail(f"PMID 37583402 status is {paper.get('status')!r}, expected VETTED_DO_NOT_INGEST")

queue = state.get("work_queue", [])
new_items = [q for q in queue if q.get("added") == "2026-09-11"]
if len(new_items) >= 4:
    ok(f"work_queue has {len(new_items)} items added 2026-09-11")
else:
    warn(f"work_queue has only {len(new_items)} items added 2026-09-11, expected 4")

p0 = [q for q in queue if q.get("priority") == 0]
print(f"       {len(p0)} P0 items are open. P0 means a human must act; "
      f"no amount of agent runs will clear them.")


# ------------------------------------------------------------- 2. Python syntax
print("\n=== 2. Edited builders still compile ===")
EDITED = ["build_health_equity.py", "build_lada_diagnostic_model.py"]
for name in EDITED:
    path = SCRIPTS / name
    if not path.exists():
        fail(f"{name} not found")
        continue
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        ok(f"{name} parses")
    except SyntaxError as exc:
        fail(f"{name} SYNTAX ERROR line {exc.lineno}: {exc.msg}")


# ------------------------------------------- 3. no un-annotated PMID leftovers
print("\n=== 3. Repaired PMIDs have no un-annotated attachments left ===")
# Each PMID maps to what it actually is, so the message can say why a hit is wrong.
REPAIRED = {
    "34421203": "Ebekozien, Clinical Diabetes 2021 - T1D Exchange registry OUTCOMES "
                "(HbA1c/DKA/hypo/tech use). NOT a trial-enrolment analysis.",
    "36113507": "Gregory, Lancet Diabetes Endocrinol 2022 - T1D burden MODELLING study. "
                "No trial geography, no funding data, T1D only.",
    "33139407": "Hill-Briggs, Diabetes Care 2021 - Social Determinants of Health and "
                "Diabetes, a NARRATIVE REVIEW. Not a position statement, not a meta-analysis.",
}
# A line is considered annotated if the repair marker appears within this window.
WINDOW = 6
MARKERS = ("CITATION CORRECTED", "CITATION REMOVED", "CITATION WITHDRAWN",
           "WITHDRAWN AND REPLACED", "SECTION CORRECTED", "ENTRIES MERGED",
           "UNSOURCED")

heq = SCRIPTS / "build_health_equity.py"
lines = heq.read_text(encoding="utf-8").splitlines()
for pmid, truth in REPAIRED.items():
    hits = [i for i, ln in enumerate(lines) if pmid in ln]
    bare = []
    for i in hits:
        ctx = "\n".join(lines[max(0, i - WINDOW): i + WINDOW + 1])
        if not any(m in ctx for m in MARKERS):
            bare.append(i + 1)
    if bare:
        fail(f"PMID {pmid}: {len(bare)} attachment(s) with no repair annotation "
             f"at line(s) {bare}")
        print(f"         What it actually is: {truth}")
    else:
        ok(f"PMID {pmid}: all {len(hits)} occurrence(s) annotated")


# --------------------------------------------- 4. self-confessed-doubt markers
print("\n=== 4. Self-confessed-doubt markers (the proposed P1 gate) ===")
DOUBT = re.compile(
    r"needs manual verification|needs verification|\bunverified\b|\bTODO\b|\bFIXME\b",
    re.IGNORECASE)

if DOUBT.search(heq.read_text(encoding="utf-8")):
    fail("build_health_equity.py still contains a doubt marker - the 2026-09-11 "
         "repair was supposed to remove all four")
else:
    ok("build_health_equity.py is clean of doubt markers")

print("\n       Repo-wide count, so the gate's cost is known before it is wired in.")
print("       On 2026-09-11 every one of the four markers in build_health_equity.py")
print("       sat on a citation that turned out to be wrong. Hit rate was 4/4.")
total_hits = 0
for path in sorted(SCRIPTS.glob("build_*.py")) + sorted(SCRIPTS.glob("rebuild_*.py")):
    text = path.read_text(encoding="utf-8", errors="replace")
    n = len(DOUBT.findall(text))
    if n:
        total_hits += n
        print(f"       {n:>3}  {path.name}")
if total_hits:
    warn(f"{total_hits} doubt marker(s) remain across builders - each is a "
         f"published admission that a claim was never checked")
else:
    ok("no doubt markers anywhere in the builders")


# ------------------------------------------------- 5. Step 4 credibility sweep
print("\n=== 5. Step 4 credibility sweep (phrases only) ===")
print("       The PMID-ceiling half of Step 4 is RETIRED - PubMed crossed 42M during")
print("       2026. audit_impossible_pmids.py resolves the ceiling live. See the")
print("       standing P0 item asking for the task file's Step 4 to be edited.")
BAD = re.compile(
    r"zero SAEs|zero rejection|\bcurative\b|cures (?:type ?[12]|diabetes)|"
    r"achieves (?:remission|cure|normoglyc)", re.IGNORECASE)
dirty = 0
for path in sorted(SCRIPTS.glob("build_*.py")) + sorted(SCRIPTS.glob("rebuild_*.py")):
    for i, ln in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if BAD.search(ln):
            dirty += 1
            fail(f"{path.name}:{i}: {ln.strip()[:110]}")
if not dirty:
    ok("no overstatement phrases in any builder")


# ----------------------------------------------------------------- conclusion
print("\n" + "=" * 70)
if failures:
    print(f"RESULT: {len(failures)} FAILURE(S), {len(warnings_)} warning(s)")
else:
    print(f"RESULT: all checks pass ({len(warnings_)} warning(s))")

print("""
THIS SCRIPT VERIFIES EDITS. IT DOES NOT PUBLISH THEM.

The repo is currently diverged in the direction that is hardest to notice:
builder SOURCE has been corrected on 2026-09-09, 09-10 and 09-11 (39 citations
removed in total) and NONE of those builders has been executed since
2026-09-08. So grepping the scripts reports the repo clean while a reader of
Dashboards/ or docs/Dashboards/ still sees every false citation - including,
from 2026-09-11, the health-equity dashboard's headline statistics, and from
2026-09-10, the main Research Dashboard.

NEXT, IN ORDER:
    python Analysis/Scripts/run_quality_improvements.py
    python Analysis/Scripts/verify_2026_09_09_repairs.py
    python Analysis/Scripts/verify_2026_09_10_repairs.py
    git add -A ; git commit -m "..." ; git push

And origin/main has not moved since 2026-04-20.
""")

sys.exit(1 if failures else 0)
