#!/usr/bin/env python3
"""
audit_builders_compile.py
=========================
Added 2026-09-17.

WHAT THIS CHECKS
----------------
That every Python file in Analysis/Scripts/ parses.

WHY IT EXISTS
-------------
On 2026-09-17 `build_gap_deep_dives.py` was found to be syntactically
invalid AT HEAD. Line 982 held a correction note that embedded an
unescaped double-quoted phrase inside a double-quoted string:

    "... This note first read "all seven ... in this gap record" and was
    corrected the same day ..."

The break was introduced by the 2026-09-16 commit -- a commit whose own run
report stated that the rebuild had cleared stale rows from this dashboard's
output. It could not have. The file cannot be imported or executed at all,
so `Dashboards/Gap_Deep_Dives.html` was frozen at its last good build while
seven correction passes went on editing the source that generates it.

THE SHAPE OF THE DEFECT IS WORTH NAMING
---------------------------------------
Every gate in this repository checks the CONTENT of an assertion: does this
PMID exist, is this surname right, is this phase real, is this number
sourced. Not one of them checks that the file making the assertion can run.
So the most complete failure available -- a builder that produces no output
whatever -- was the only one nothing could see.

It is also self-inflicted in a specific way: the correction notes this
project writes are long, quote the text they are replacing, and are pasted
into string literals. That is precisely the habit that produces unescaped
quotes. The more carefully a run documents its repairs, the more likely it
is to break the file it is repairing. This check is the guard for that.

COST
----
Under one second for 142 files, no network, no library, no judgement, and
zero possible false positives: a file either parses or it does not.

EXIT CODE
---------
0 when everything parses. 1 otherwise. Safe to wire in as a hard gate --
unlike the content gates, this one cannot be wrong about what it found.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "Analysis" / "Scripts"
OUT = ROOT / "Analysis" / "Results" / "builder_compile_audit.json"


def audit():
    checked, broken = 0, []
    for p in sorted(SCRIPTS.glob("*.py")):
        checked += 1
        try:
            compile(p.read_text(encoding="utf-8", errors="replace"),
                    str(p), "exec")
        except SyntaxError as exc:
            broken.append({
                "file": f"Analysis/Scripts/{p.name}",
                "line": exc.lineno,
                "error": exc.msg,
                "text": (exc.text or "").strip()[:200],
            })
        except Exception as exc:                 # unreadable, encoding, etc.
            broken.append({
                "file": f"Analysis/Scripts/{p.name}",
                "line": None,
                "error": f"{type(exc).__name__}: {exc}",
                "text": "",
            })
    report = {"generated": "2026-09-17", "gate": "builders_compile",
              "counts": {"checked": checked, "broken": len(broken)},
              "broken": broken}
    OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")
    return report


def main():
    rep = audit()
    c = rep["counts"]
    print("BUILDER COMPILE AUDIT")
    print(f"  files checked : {c['checked']}")
    print(f"  DO NOT PARSE  : {c['broken']}")
    for b in rep["broken"]:
        print(f"\n  {b['file']}:{b['line']}  {b['error']}")
        if b["text"]:
            print(f"    {b['text']}")
    if c["broken"]:
        print("\n  A builder that does not parse produces no output at all, "
              "so its dashboard is frozen at its last good build while the "
              "source keeps being edited.")
        return 1
    print("\n  [OK] every script in Analysis/Scripts parses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
