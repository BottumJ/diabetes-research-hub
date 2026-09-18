#!/usr/bin/env python3
"""
audit_computed_value_citations.py
=================================

MEASURE-FIRST gate proposed by the work-queue item of 2026-09-13:

    "A CITATION IS BEING ATTACHED TO THE MODEL'S OWN OUTPUT, AND NO EXISTING
     GATE CAN SEE IT."

Every other citation gate in this repository asks whether a PMID matches the
text near it.  None asks whether the NUMBER near it was computed locally by
the very script that prints the citation.  The failing shape found on
2026-09-13 in build_lada_diagnostic_model.py was:

    <td>${result['total_cost']:,.0f} (PMID:37909353)</td>

The dollar figure is an f-string interpolation of a value the script computed
seconds earlier; the PMID makes it look published.

THE TELL IS PURELY SYNTACTIC AND NEEDS NO LOOKUP: a PMID marker inside the
same f-string literal as a {...} interpolation whose expression is a computed
lookup (subscript, call, arithmetic) rather than a bare transcribed constant.

Severity split, because not every hit is a defect:

  COMPUTED    the interpolated expression subscripts or calls something
              (result['x'], row["y"], model.get(...), fn(...), a*b) -- the
              value is produced at runtime.  These are the defect class.

  BARE_NAME   the interpolation is a plain identifier or attribute
              (e.g. {n_patients}, {cfg.year}).  Frequently a constant
              transcribed FROM the cited paper and assigned once at module
              level.  Reported separately as REVIEW, not flagged.

Exclusions: this repository's own correction prose.  A withdrawal note that
quotes the offending line back ("previously read ... (PMID:xxxx)") must not be
counted as a live attachment -- the 2026-09-14 queue item documents an 8x
count inflation from exactly this cause.

Usage:
    python audit_computed_value_citations.py            # measure, exit 0
    python audit_computed_value_citations.py --gate     # exit 1 on COMPUTED

Output: Analysis/Results/computed_value_citation_audit.json
"""

import ast
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RESULTS = os.path.join(REPO, "Analysis", "Results")
OUT = os.path.join(RESULTS, "computed_value_citation_audit.json")

PMID_MARK = re.compile(r"PMID[:\s]*\d{6,8}", re.IGNORECASE)

# Prose this repository writes about its OWN corrections.  An occurrence whose
# window contains any of these is a withdrawal record, not a live citation.
CORRECTION_MARKERS = (
    "withdrawn", "withdraw", "removed", "mis-attributed", "misattributed",
    "previously read", "previously cited", "unsourced", "corrected 2026-",
    "no longer cited", "false attribution", "does not support",
)

# Files that are not part of the published surface.
#   _run_ / _close_run_ / _tmp_  : dated one-shot run scripts, history
#   audit_                       : the gates themselves
#   verify_                      : dated repair-verification scripts. Measured
#     2026-09-18: 3 of the 4 initial COMPUTED hits were verify_*.py printing
#     diagnostics like f"{len(live_bad)} LIVE link(s) to PMID 34763823 remain".
#     That is a gate reporting a count ABOUT a PMID, not a citation sourcing a
#     number - the opposite of the defect. Excluding them is scoping, not
#     silencing: nothing these scripts print reaches a dashboard.
SKIP_PREFIXES = ("_run_", "_close_run_", "_tmp_", "audit_", "verify_",
                 "check_", "reconcile_")


def is_correction_prose(window: str) -> bool:
    low = window.lower()
    return any(m in low for m in CORRECTION_MARKERS)


def classify_expression(expr_src: str) -> str:
    """COMPUTED if the interpolation reads a container, calls, or does math."""
    try:
        node = ast.parse(expr_src.strip(), mode="eval").body
    except SyntaxError:
        # format specs and nested quotes can defeat a standalone parse;
        # fall back to the textual tell
        if any(ch in expr_src for ch in "[(*+-/"):
            return "COMPUTED"
        return "BARE_NAME"

    if isinstance(node, (ast.Subscript, ast.Call, ast.BinOp)):
        return "COMPUTED"
    if isinstance(node, ast.Attribute):
        # obj.method(...) already caught as Call; a plain attribute is a name
        return "BARE_NAME"
    if isinstance(node, ast.Name):
        return "BARE_NAME"
    return "COMPUTED"


# How close (in rendered characters) an interpolation must sit to a PMID
# marker before the citation can plausibly be read as sourcing that value.
# A whole-page f-string holds the entire HTML document and dozens of PMIDs;
# without this window the gate fires on {COLORS['bg']} at the top of the page
# because a PMID appears 4,000 characters later.  That is the false-positive
# mode found when this gate was first measured on 2026-09-18.
PROXIMITY_CHARS = 180


def scan_file(path: str, rel: str):
    """Walk the AST; for every f-string that contains a PMID marker, flatten
    it back to text with placeholders so that DISTANCE between a PMID and an
    interpolation can be measured, and flag only the nearby ones."""
    findings = []
    try:
        src = open(path, "r", encoding="utf-8").read()
    except Exception:
        return findings
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return findings

    lines = src.splitlines()

    for node in ast.walk(tree):
        if not isinstance(node, ast.JoinedStr):
            continue

        # Flatten: build the rendered string with each interpolation replaced
        # by a fixed-width token, recording the offset of every token.
        flat = []
        slots = []          # (offset_in_flat, expr_src, lineno)
        pos = 0
        for v in node.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                flat.append(v.value)
                pos += len(v.value)
            elif isinstance(v, ast.FormattedValue):
                try:
                    expr_src = ast.unparse(v.value)
                except Exception:
                    expr_src = "<unparseable>"
                token = "\x00SLOT\x00"
                slots.append((pos, expr_src, getattr(v, "lineno", node.lineno)))
                flat.append(token)
                pos += len(token)
        text = "".join(flat)

        pmid_hits = [(m.start(), re.sub(r"\D", "", m.group()))
                     for m in PMID_MARK.finditer(text)]
        if not pmid_hits or not slots:
            continue

        for offset, expr_src, lineno in slots:
            near = [p for (ppos, p) in pmid_hits
                    if abs(ppos - offset) <= PROXIMITY_CHARS]
            if not near:
                continue

            # correction-prose exclusion, measured on the rendered window
            lo_c = max(0, offset - PROXIMITY_CHARS * 2)
            hi_c = min(len(text), offset + PROXIMITY_CHARS * 2)
            rendered_window = text[lo_c:hi_c]
            src_lo = max(0, lineno - 3)
            src_hi = min(len(lines), lineno + 3)
            src_window = "\n".join(lines[src_lo:src_hi])
            if is_correction_prose(rendered_window) or is_correction_prose(src_window):
                findings.append({
                    "file": rel, "line": lineno,
                    "severity": "EXCLUDED_CORRECTION",
                    "pmids": sorted(set(near)),
                    "expression": expr_src[:120],
                    "snippet": rendered_window.replace("\x00SLOT\x00",
                                                       "{...}")[:200],
                })
                continue

            findings.append({
                "file": rel,
                "line": lineno,
                "severity": classify_expression(expr_src),
                "pmids": sorted(set(near)),
                "expression": expr_src[:120],
                "snippet": rendered_window.replace("\x00SLOT\x00", "{...}")
                                          .strip()[:220],
            })

    return findings


def main():
    gate = "--gate" in sys.argv
    scripts_dir = os.path.join(REPO, "Analysis", "Scripts")

    all_findings = []
    files_scanned = 0
    for fn in sorted(os.listdir(scripts_dir)):
        if not fn.endswith(".py"):
            continue
        if fn.startswith(SKIP_PREFIXES):
            continue
        files_scanned += 1
        all_findings.extend(
            scan_file(os.path.join(scripts_dir, fn), f"Analysis/Scripts/{fn}")
        )

    computed = [f for f in all_findings if f["severity"] == "COMPUTED"]
    bare = [f for f in all_findings if f["severity"] == "BARE_NAME"]
    excluded = [f for f in all_findings if f["severity"] == "EXCLUDED_CORRECTION"]

    # de-duplicate COMPUTED by (file, line) for the headline count
    seen = set()
    computed_unique = []
    for f in computed:
        k = (f["file"], f["line"])
        if k in seen:
            continue
        seen.add(k)
        computed_unique.append(f)

    print("=" * 62)
    print("  COMPUTED-VALUE CITATION AUDIT")
    print("=" * 62)
    print(f"  builder files scanned                     : {files_scanned}")
    print(f"  f-strings carrying a PMID + interpolation : "
          f"{len(computed) + len(bare)}")
    print(f"    COMPUTED  (citation on a runtime value) : {len(computed_unique)}")
    print(f"    BARE_NAME (review; may be transcribed)  : {len(bare)}")
    print(f"  excluded as this repo's correction prose  : {len(excluded)}")
    print()

    if computed_unique:
        print("  COMPUTED -- a PMID is attached to a value this script computes")
        print("  " + "-" * 58)
        for f in computed_unique:
            print(f"  {f['file']}:{f['line']}")
            print(f"      PMID(s)    : {', '.join(f['pmids'])}")
            print(f"      expression : {f['expression']}")
            print(f"      line       : {f['snippet'][:150]}")
            print()

    if bare:
        print("  BARE_NAME -- review only, not flagged")
        print("  " + "-" * 58)
        for f in bare[:15]:
            print(f"  {f['file']}:{f['line']}  {{{f['expression']}}}  "
                  f"PMID {', '.join(f['pmids'])}")
        if len(bare) > 15:
            print(f"  ... and {len(bare) - 15} more")
        print()

    payload = {
        "audit": "computed_value_citations",
        "run_date": str(date.today()),
        "files_scanned": files_scanned,
        "counts": {
            "computed_unique": len(computed_unique),
            "computed_raw": len(computed),
            "bare_name": len(bare),
            "excluded_correction_prose": len(excluded),
        },
        "computed": computed_unique,
        "bare_name": bare,
        "excluded": excluded,
    }
    os.makedirs(RESULTS, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"  Output: {OUT}")

    if gate and computed_unique:
        print("  [FAIL] citations attached to locally computed values")
        return 1
    print("  [MEASURE] reporting only; not gating"
          if not gate else "  [OK] no computed-value citations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
