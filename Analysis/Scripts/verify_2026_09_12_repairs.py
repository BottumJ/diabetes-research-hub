#!/usr/bin/env python3
"""
verify_2026_09_12_repairs.py

Written by the 2026-09-12 scheduled run, which had NO PYTHON: the Linux sandbox
failed to mount for the FOURTH consecutive day with the same Plan9 error
("share 'c' is not mounted"), attributed to a Windows update released
2026-09-08. Every edit that run made was made with file tools and was never
executed or parsed.

Run this on Windows BEFORE run_quality_improvements.py. It is cheap and it
checks the two things an unexecuted edit can break - JSON validity and Python
syntax - plus the specific claims the 2026-09-12 run asserted.

    python Analysis/Scripts/verify_2026_09_12_repairs.py

Exit code 0 = all checks pass. Non-zero = something needs attention.

WHAT IT CHECKS
  1. agent_state.json still parses, and the 2026-09-12 run record and its five
     new/updated queue items are present.
  2. The two edited builders still compile as Python.
  3. build_health_equity.py no longer attaches any of the four trial PMIDs to a
     demographic figure, and the fabricated cells are gone.
  4. build_generic_drug_catalog.py has no remaining LIVE (non-comment)
     attachment of PMID 34763823 to a price or cost figure.
  5. The NARROWED self-confessed-doubt pattern (without the bare term
     'unverified') really does have zero hits in builder-emitted text - this is
     the measurement the P2 gate item rests on, so it should be reproducible.
  6. Step 4 credibility phrases, as a script rather than by grep.

NOTE ON SCOPE: this does NOT rebuild anything. Until run_quality_improvements.py
runs, the generated HTML in Dashboards/ and docs/Dashboards/ still shows every
citation removed on 2026-09-09, 09-10, 09-11 and 09-12. That divergence is the
top P0 item and is now four days old.
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


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


# --------------------------------------------------------------------------
# 1. State file parses and carries this run
# --------------------------------------------------------------------------
print("\n=== 1. agent_state.json ===")
state = None
try:
    state = json.loads(read(STATE))
    ok("agent_state.json parses as JSON")
except json.JSONDecodeError as e:
    fail(f"agent_state.json does NOT parse: {e}")

if state is not None:
    if state.get("last_run") == "2026-09-12":
        ok("last_run == 2026-09-12")
    else:
        fail(f"last_run is {state.get('last_run')!r}, expected '2026-09-12'")

    runs = [r for r in state.get("run_history", []) if r.get("date") == "2026-09-12"]
    if len(runs) == 1:
        ok("exactly one 2026-09-12 run record present")
        rec = runs[0]
        for key in ("finding_1_gate_premise_refuted",
                    "finding_2_trial_demographics",
                    "finding_3_cost_column",
                    "finding_4_negative_result",
                    "finding_5_new_flag"):
            if key in rec:
                ok(f"run record carries {key}")
            else:
                fail(f"run record is missing {key}")
    else:
        fail(f"found {len(runs)} run records dated 2026-09-12, expected 1")

    q = state.get("work_queue", [])
    added_today = [i for i in q if i.get("added") == "2026-09-12"]
    if len(added_today) >= 5:
        ok(f"{len(added_today)} queue items added 2026-09-12")
    else:
        fail(f"only {len(added_today)} queue items added 2026-09-12, expected >= 5")

    resolved_today = [i for i in q if i.get("resolved") == "2026-09-12"]
    if len(resolved_today) >= 2:
        ok(f"{len(resolved_today)} queue items resolved 2026-09-12")
    else:
        fail(f"only {len(resolved_today)} queue items resolved 2026-09-12, expected >= 2")


# --------------------------------------------------------------------------
# 2. Edited builders still compile
# --------------------------------------------------------------------------
print("\n=== 2. Python syntax of edited builders ===")
EDITED = ["build_health_equity.py", "build_generic_drug_catalog.py"]
for name in EDITED:
    p = SCRIPTS / name
    if not p.exists():
        fail(f"{name} does not exist")
        continue
    try:
        ast.parse(read(p))
        ok(f"{name} parses as Python")
    except SyntaxError as e:
        fail(f"{name} has a SyntaxError at line {e.lineno}: {e.msg}")


# --------------------------------------------------------------------------
# 3. Health-equity trial demographics
# --------------------------------------------------------------------------
print("\n=== 3. build_health_equity.py trial demographics ===")
he = SCRIPTS / "build_health_equity.py"
if he.exists():
    txt = read(he)

    # The fabricated cells must be gone.
    gone = {
        '"60% white, 25% Black, 12% Hispanic"': "60% white, 25% Black, 12% Hispanic",
        "ACCORD heterogeneous-treatment-effects claim": "heterogeneous treatment effects by race",
        "EMPA-REG 'not consistently reported' claim": "Subgroup analyses by race not consistently reported",
        "the uncited SGLT2i Trials row": "SGLT2i Trials</strong> (2013+)",
    }
    for label, needle in gone.items():
        # Allow the string to survive inside the withdrawal record, which quotes
        # what was removed. Only flag it if it appears OUTSIDE that record.
        hits = [m.start() for m in re.finditer(re.escape(needle), txt)]
        live = []
        for h in hits:
            window = txt[max(0, h - 600):h]
            if "WITHDRAWN" not in window and "Repaired 2026-09-12" not in window:
                live.append(h)
        if live:
            fail(f"{label} still appears OUTSIDE a withdrawal record ({len(live)}x)")
        else:
            ok(f"{label} appears only inside a withdrawal record (or not at all)")

    # The corrected figures must be present.
    for label, needle in {
        "ACCORD 62.4%": "62.4%",
        "ACCORD source PMID 37715820": "37715820",
        "UKPDS ethnicity source PMID 7955993": "7955993",
        "EMPA-REG Asian subgroup PMID 28025462": "28025462",
        "EMPA-REG 21.6% Asian": "21.6%",
    }.items():
        if needle in txt:
            ok(f"{label} present")
        else:
            fail(f"{label} is MISSING - the repair may not have been saved")

    # No live demographic attachment to the four primary-outcomes PMIDs.
    for pmid in ("8366922", "9742976", "18539917", "26378978"):
        for m in re.finditer(re.escape(pmid), txt):
            window = txt[m.start():m.start() + 400]
            if re.search(r"\d+(\.\d+)?%\s*(white|black|hispanic|asian)", window, re.I):
                # Acceptable only if the window is explicitly a correction.
                if "Repaired 2026-09-12" not in window and "<strong>not</strong>" not in window:
                    fail(f"PMID {pmid} still sits next to a demographic percentage")
                    break
        else:
            ok(f"PMID {pmid}: no un-annotated demographic attachment")


# --------------------------------------------------------------------------
# 4. Generic drug catalog cost column
# --------------------------------------------------------------------------
print("\n=== 4. build_generic_drug_catalog.py cost attributions ===")
gc = SCRIPTS / "build_generic_drug_catalog.py"
if gc.exists():
    txt = read(gc)

    if "WHO model pricing" in txt and "previously read" not in txt:
        fail("the 'WHO model pricing' claim is still asserted, not withdrawn")
    else:
        ok("'WHO model pricing' claim is withdrawn or annotated")

    # Every surviving 34763823 must be inside a comment or a correction note.
    live_bad = []
    for m in re.finditer(r"34763823", txt):
        line_start = txt.rfind("\n", 0, m.start()) + 1
        line_end = txt.find("\n", m.start())
        line = txt[line_start:line_end if line_end != -1 else len(txt)]
        stripped = line.lstrip()
        is_comment = stripped.startswith("#") or stripped.startswith("//") or "<!--" in line
        is_correction = ("Repaired" in line or "removed 2026" in line
                         or "previously read" in line or "standing caveat" in line
                         or "Both halves were false" in line)
        is_href = 'pubmed.ncbi.nlm.nih.gov/34763823' in line
        if is_href and not (is_comment or is_correction):
            live_bad.append(line.strip()[:120])
    if live_bad:
        fail(f"{len(live_bad)} LIVE link(s) to PMID 34763823 remain:")
        for l in live_bad:
            print(f"         {l}")
    else:
        ok("no live reader-facing link to PMID 34763823 remains in this file")

    if "[UNSOURCED]" in txt:
        ok("[UNSOURCED] markers present")
    else:
        fail("[UNSOURCED] markers are missing - the repair may not have been saved")


# --------------------------------------------------------------------------
# 5. The narrowed self-confessed-doubt measurement, reproduced
# --------------------------------------------------------------------------
print("\n=== 5. narrowed self-confessed-doubt pattern (P2 gate item) ===")
# NOTE the deliberate absence of a bare \bunverified\b alternative. Including it
# was the 2026-09-11 item's error: it fires on this repo's own disclosure
# vocabulary (the UNVERIFIED validation tier, the pricing-provenance notes, the
# '[unverified]' PROSPERO label). See the 2026-09-12 resolution in the queue.
NARROW = re.compile(r"needs manual verification|needs verification|\bTODO\b|\bFIXME\b")
TOOLING = {"audit_nct_identifiers.py",
           "verify_2026_09_11_repairs.py",
           "verify_2026_09_12_repairs.py"}

builder_hits = []
for p in sorted(SCRIPTS.glob("*.py")):
    if p.name in TOOLING:
        continue
    for i, line in enumerate(read(p).splitlines(), 1):
        if NARROW.search(line):
            builder_hits.append(f"{p.name}:{i}: {line.strip()[:110]}")

if builder_hits:
    fail(f"narrowed pattern has {len(builder_hits)} hit(s) outside tooling "
         f"- expected 0 as measured on 2026-09-12:")
    for h in builder_hits:
        print(f"         {h}")
else:
    ok("narrowed pattern: 0 hits outside tooling, reproducing the 2026-09-12 measurement")

# And show what the WIDE pattern would have done, so nobody re-proposes it.
WIDE = re.compile(r"needs manual verification|needs verification|\bunverified\b|\bTODO\b|\bFIXME\b",
                  re.I)
wide_count = 0
for p in sorted(SCRIPTS.glob("*.py")):
    if p.name in TOOLING:
        continue
    wide_count += sum(1 for line in read(p).splitlines() if WIDE.search(line))
print(f"[INFO] the WIDE pattern (including bare 'unverified') would fire "
      f"{wide_count} time(s) outside tooling.")
print("[INFO] Those are this repository's own disclosures - the UNVERIFIED validation")
print("[INFO] tier, the pricing-provenance notes, the '[unverified]' PROSPERO label.")
print("[INFO] Do NOT wire in the wide pattern. See the 2026-09-12 queue resolution.")


# --------------------------------------------------------------------------
# 6. Step 4 credibility phrases
# --------------------------------------------------------------------------
print("\n=== 6. credibility sweep (Step 4 phrases) ===")
# The PMID-integer half of Step 4 is deliberately NOT reimplemented here: that
# rule is retired. audit_impossible_pmids.py resolves the ceiling live.
BANNED = [
    (r"\bcurative\b", "curative"),
    (r"\bcures? type [12]\b", "cures type 1/2"),
    (r"zero SAEs", "zero SAEs"),
    (r"zero rejection", "zero rejection"),
    (r"achieves (remission|cure|normoglyc)", "achieves remission/cure/normoglycaemia"),
]
AUDIT_TRAIL = ("audit_", "verify_", "_run_", "_close_run_", "repair_", "reconcile_",
               "adjudicate_", "falsify_", "test_", "check_")
banned_hits = []
for p in sorted(SCRIPTS.glob("*.py")):
    if p.name.startswith(AUDIT_TRAIL):
        continue  # records of absence, not claims
    body = read(p)
    for pat, label in BANNED:
        for i, line in enumerate(body.splitlines(), 1):
            if re.search(pat, line, re.I):
                banned_hits.append(f"{p.name}:{i} [{label}] {line.strip()[:100]}")
if banned_hits:
    fail(f"{len(banned_hits)} banned-phrase hit(s):")
    for h in banned_hits:
        print(f"         {h}")
else:
    ok("no banned overstatement phrases in builder scripts")


# --------------------------------------------------------------------------
print("\n" + "=" * 72)
if failures:
    print(f"RESULT: {len(failures)} FAILURE(S), {len(warnings_)} warning(s)")
    for f_ in failures:
        print(f"  - {f_}")
    print("\nNEXT: fix the above, then run "
          "python Analysis/Scripts/run_quality_improvements.py")
    sys.exit(1)
else:
    print(f"RESULT: all checks passed ({len(warnings_)} warning(s))")
    print("\nNEXT, AND THIS IS THE POINT: the builders above are CORRECT IN SOURCE")
    print("and have NOT been executed since 2026-09-08. The published HTML in")
    print("Dashboards/ and docs/Dashboards/ still shows the false citations.")
    print("Run:  python Analysis/Scripts/run_quality_improvements.py")
    print("then push. Nothing this agent has written since 2026-04-20 has reached")
    print("origin/main.")
    sys.exit(0)
