#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
set_gap_tier.py — apply a gap-tier ruling everywhere, in one command.

    python set_gap_tier.py 2 BRONZE --reason "Owner ruling 2026-10-02: ..."
    python set_gap_tier.py --sync          # rewrite stray copies to match the store

Writes, in order:
  1. Analysis/Results/gap_tiers.json        (the tier, with dated history)
  2. Analysis/Results/agent_state.json      (gaps[N].tier + an audit_history entry)
  3. every typed copy gap_tier_copies.py can find in the builders
     (the tier word only; a methodology badge's CSS class follows it)
  4. the README tier table row and its tier-count column

It does NOT rebuild pages or regenerate gap_evidence.json; run the pipeline
(or at least extract_evidence.py and the affected builders) afterwards, and
audit_gap_numbering.py will fail if anything was missed.

A ruling is the owner's. This tool only makes applying one mechanical; it
refuses to run without --reason, so the store always records why.
"""

from __future__ import annotations

import argparse
import datetime
import io
import json
import os
import re
import sys

import gap_tier_copies as gtc

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = gtc.ROOT
README = os.path.join(ROOT, "README.md")
TODAY = datetime.date.today().isoformat()


def _rw(path, fn):
    with io.open(path, encoding="utf-8", newline="") as fh:
        s = fh.read()
    new = fn(s)
    if new != s:
        with io.open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        return True
    return False


def rewrite_copies(want):
    """Rewrite every typed copy that disagrees with `want` ({gap: tier})."""
    changed = []
    by_file = {}
    for c in gtc.find_copies():
        if c["gap"] in want and c["tier"] != want[c["gap"]]:
            by_file.setdefault(c["path"], []).append(c)
    for path, copies in by_file.items():
        def fix(s, copies=copies):
            # Right to left, so earlier offsets stay valid.
            spans = []
            for c in copies:
                spans.append((c["start"], c["end"], want[c["gap"]]))
                if c.get("cls_span"):
                    spans.append((c["cls_span"][0], c["cls_span"][1],
                                  {"EXPLORATORY": "review"}.get(want[c["gap"]], want[c["gap"]].lower())))
            for a, b, txt in sorted(spans, reverse=True):
                s = s[:a] + txt + s[b:]
            return s
        _rw(path, fix)
        compile(open(path, encoding="utf-8").read(), path, "exec")
        changed += ["%s:%d #%s %s -> %s" % (c["file"], c["line"], c["gap"], c["tier"], want[c["gap"]])
                    for c in copies]
    return changed


def update_readme(want):
    def fix(s):
        for gap, tier in want.items():
            s = re.sub(r"(^\| %s \| [^|\n]+\| )(GOLD|SILVER|BRONZE|EXPLORATORY)( \|)" % gap,
                       lambda m: m.group(1) + tier + m.group(3), s, flags=re.M)
        counts = {t: list(want.values()).count(t) for t in gtc.TIERS}
        for t in gtc.TIERS:
            s = re.sub(r"(^\| \*\*%s\*\* \|[^|\n]+\| )\d+ gaps?( \|)" % t,
                       lambda m, t=t: m.group(1) + "%d gap%s" % (counts[t], "" if counts[t] == 1 else "s") + m.group(2),
                       s, flags=re.M)
        return s
    return _rw(README, fix)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("gap", nargs="?")
    ap.add_argument("tier", nargs="?", choices=gtc.TIERS)
    ap.add_argument("--reason")
    ap.add_argument("--sync", action="store_true",
                    help="no ruling: rewrite stray copies to match gap_tiers.json")
    a = ap.parse_args(argv[1:])

    store = gtc.load_store()
    if not a.sync:
        if not (a.gap and a.tier and a.reason):
            ap.error("give GAP TIER --reason, or --sync")
        g = store["gaps"][str(int(a.gap))]
        was = g["tier"]
        g.setdefault("history", []).append({"date": TODAY, "from": was, "to": a.tier, "reason": a.reason})
        g["tier"] = a.tier
        store["as_of"] = TODAY
        with io.open(gtc.STORE, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(store, indent=2, ensure_ascii=False) + "\n")
        print("gap_tiers.json: #%s %s -> %s" % (a.gap, was, a.tier))

        sys.path.insert(0, HERE)
        import agent_state as A
        st = A.load_state()
        sg = st["gaps"][str(int(a.gap))]
        sg["tier"] = a.tier
        sg.setdefault("audit_history", []).append({
            "date": TODAY, "tier_before": was, "tier_after": a.tier,
            "action": "TIER SET via set_gap_tier.py", "new_evidence_found": False, "notes": a.reason})
        A.save_state(st)
        print("agent_state.json: #%s -> %s" % (a.gap, a.tier))

    want = {k: v["tier"] for k, v in gtc.load_store()["gaps"].items()}
    changed = rewrite_copies(want)
    for c in changed:
        print("  rewrote %s" % c)
    print("README: %s" % ("updated" if update_readme(want) else "already in agreement"))
    left = gtc.disagreements()
    if left:
        print("[FAIL] %d copies still disagree:" % len(left))
        for c in left:
            print("  %s:%d #%s %s" % (c["file"], c["line"], c["gap"], c["tier"]))
        return 1
    print("[OK] every typed copy agrees with gap_tiers.json. Now run extract_evidence.py and the pipeline.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
