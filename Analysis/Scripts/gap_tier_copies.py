#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gap_tier_copies.py
==================

NEW 2026-10-01. One place that knows (a) what each gap's tier IS and (b) every
place in the builders that TYPES it.

WHY
    On 2026-09-30 four tier rulings (#1, #3, #11, #13) and three
    reconciliations (#6, #14, #15) each had to be applied by hand to between
    six and nine files. Each time, the audit that is meant to find the copies
    missed some: it saw "Gap #3 (GOLD)" but not "Gap #6 GOLD Validated",
    "Gap #11, SILVER)", a methodology badge, or a registry keyed by integer
    with "name" instead of "title". Those copies were found by grepping, after
    the fact, and published wrong in the meantime.

    So the tier now lives in Analysis/Results/gap_tiers.json, and this module
    is the single locator for its copies. audit_gap_numbering.py compares every
    copy against the file; set_gap_tier.py rewrites every copy from it.

    The copies are not removed. Fifteen builders interpolate the tier into
    hand-written HTML in different ways, and rewriting each to read the file is
    a larger change than can be checked in one sitting. What this guarantees
    instead is that a copy cannot disagree with the file without failing the
    build, and that a ruling is one command.
"""

from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
STORE = os.path.join(ROOT, "Analysis", "Results", "gap_tiers.json")
TIERS = ("GOLD", "SILVER", "BRONZE", "EXPLORATORY")
_T = "(?P<tier>GOLD|SILVER|BRONZE|EXPLORATORY)"

# Every form a tier has been found typed in, 2026-09-03 to 2026-10-01.
# Each pattern captures the gap number as `gap` and the tier word as `tier`;
# only the tier word is ever rewritten.
PATTERNS = [
    ("prose_paren", re.compile(r"Gap #(?P<gap>\d{1,2})\s*\(" + _T + r"\b")),
    ("prose_comma", re.compile(r"Gap #(?P<gap>\d{1,2}),\s*" + _T + r"\b")),
    ("prose_bare", re.compile(r"(?i:gap) #(?P<gap>\d{1,2}) " + _T + r"\b")),
    ("tier_before", re.compile(_T + r"[- ](?:Validated )?Research Gap #(?P<gap>\d{1,2})\b")),
    ("badge", re.compile(
        r'class="gap-title">Gap #(?P<gap>\d{1,2}):[^<]*</div>\s*'
        r'<span class="gap-validation (?P<cls>\w+)">' + _T + r"</span>")),
    ("registry_quoted", re.compile(
        r'["\'](?P<gap>\d{1,2})["\']\s*:\s*\{\s*["\'](?:title|name)["\']\s*:\s*["\'][^"\']+["\'],\s*'
        r'["\']tier["\']\s*:\s*["\']' + _T + r'["\']')),
    ("registry_int", re.compile(
        r'^\s*(?P<gap>\d{1,2})\s*:\s*\{\s*["\'](?:title|name)["\']\s*:\s*["\'][^"\']+["\'],\s*'
        r'["\']tier["\']\s*:\s*["\']' + _T + r'["\']', re.M)),
]
# Files whose tier mentions are history, not claims: run logs, one-off run
# scripts, audits and verifiers that quote old values on purpose.
SKIP_PREFIX = ("_", "audit_", "verify_", "test_", "regression_")
SKIP_FILES = {"gap_tier_copies.py", "set_gap_tier.py"}


def load_store():
    with open(STORE, encoding="utf-8") as fh:
        return json.load(fh)


def canonical_tiers():
    return {str(k): v["tier"] for k, v in load_store()["gaps"].items()}


def _skip_line(before):
    """A copy inside a comment or a correction note is history.

    `before` is the text on the line BEFORE the tier word, so a trailing
    comment that mentions an old tier does not hide the live value it follows.
    """
    s = before.lstrip()
    return (s.startswith("#") or " # " in before
            or re.search(r"(?i)corrected|previously|withdrawn|was (?:GOLD|SILVER|BRONZE)", before))


def find_copies(scripts_dir=HERE):
    """Every typed tier: [{'file','line','gap','tier','form','start','end'}].

    start/end delimit the tier word itself, so a caller can replace exactly it.
    """
    out = []
    for fname in sorted(os.listdir(scripts_dir)):
        if (not fname.endswith(".py") or fname.startswith(SKIP_PREFIX)
                or fname in SKIP_FILES):
            continue
        path = os.path.join(scripts_dir, fname)
        with open(path, encoding="utf-8") as fh:
            body = fh.read()
        seen = set()
        for form, pat in PATTERNS:
            for m in pat.finditer(body):
                a, b = m.span("tier")
                if (a, b) in seen:
                    continue
                ls = body.rfind("\n", 0, a) + 1
                if _skip_line(body[ls:a]):
                    continue
                seen.add((a, b))
                out.append({"file": fname, "path": path,
                            "line": body.count("\n", 0, a) + 1,
                            "gap": str(int(m.group("gap"))), "tier": m.group("tier"),
                            "form": form, "start": a, "end": b,
                            "cls_span": m.span("cls") if "cls" in pat.groupindex else None})
    return out


def disagreements(scripts_dir=HERE):
    want = canonical_tiers()
    return [c for c in find_copies(scripts_dir)
            if c["gap"] in want and c["tier"] != want[c["gap"]]]


if __name__ == "__main__":
    want = canonical_tiers()
    copies = find_copies()
    bad = [c for c in copies if c["gap"] in want and c["tier"] != want[c["gap"]]]
    print("gap_tiers.json: %s" % ", ".join("#%s %s" % (k, v) for k, v in
                                          sorted(want.items(), key=lambda x: int(x[0]))))
    print("%d typed copies found; %d disagree with the store" % (len(copies), len(bad)))
    for c in bad:
        print("  %s:%d  Gap #%s typed %s, store says %s  (%s)"
              % (c["file"], c["line"], c["gap"], c["tier"], want[c["gap"]], c["form"]))
