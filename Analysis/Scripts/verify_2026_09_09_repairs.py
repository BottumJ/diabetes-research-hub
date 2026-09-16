"""
verify_2026_09_09_repairs.py
=============================

Run this on Windows. The 2026-09-09 scheduled run could not execute any Python:
the Linux sandbox failed to mount on all four attempts ("Plan9 share 'c' is not
mounted"), so every edit that run made was applied with file tools and has never
been parsed, built or gated.

This script does the verification that run could not do. It is read-only except
for its own report file. It does NOT rebuild the site and does NOT touch git.

    cd C:\\Users\\justi\\OneDrive\\Diabetes_Research
    python Analysis\\Scripts\\verify_2026_09_09_repairs.py

Exit code 0 = all checks passed. Exit code 1 = at least one check failed.

WHAT IT CHECKS
--------------
1. SYNTAX. The two edited builders and agent_state.json still parse. This is the
   check that matters most, because the edits inserted prose into f-string HTML
   bodies, and an unbalanced brace or quote there is a build-breaking error that
   no one would notice until the next rebuild.

2. THE REPAIR HELD. The ten false PMID:32175717 attachments are gone from
   build_gka_pricing.py, and PMID:19104422 is no longer attached to the 1,477
   headline in build_islet_equity.py.

3. THE SAME DEFECT ELSEWHERE. Khan 2020 (PMID 32175717) is a five-page GBD
   analysis of type 2 diabetes prevalence. It contains no cost data and no type 1
   data. So ANY occurrence of that PMID near a currency symbol or near "T1D" /
   "type 1" is false by construction. This sweeps the whole repo for those, which
   is the queued P1 item "audit the other ~28 attachments".

4. THE STALE THRESHOLD. Reports how many PMIDs above 42,000,000 the repo cites,
   and (with --online) resolves them against PubMed. The daily task still calls
   everything above that ceiling "fabricated"; as of 2026-09-09 all seven tested
   were real. This quantifies the false-positive rate so the rule can be replaced
   rather than argued about.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "Analysis" / "Scripts"
STATE = REPO / "Analysis" / "Results" / "agent_state.json"

GKA = SCRIPTS / "build_gka_pricing.py"
ISLET = SCRIPTS / "build_islet_equity.py"

# Khan MAB et al. J Epidemiol Glob Health 2020;10(1):107-111.
# Type 2 prevalence only. No cost data. No type 1 data.
KHAN = "32175717"
# Alejandro R et al. Transplantation 2008;86(12):1783-8. n=325 as of April 2008.
ALEJANDRO = "19104422"

CURRENCY = re.compile(r"[$\u00a3\u20ac]|\bUSD\b|\bcost\b|\bprice\b|\bpricing\b|\brevenue\b", re.I)
TYPE1 = re.compile(r"\bT1D\b|\btype 1\b", re.I)

failures: list[str] = []
notes: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  [FAIL] {msg}")


def ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def note(msg: str) -> None:
    notes.append(msg)
    print(f"  [NOTE] {msg}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------- check 1
def check_syntax() -> None:
    print("\n[1] SYNTAX -- do the edited files still parse?")
    for path in (GKA, ISLET):
        if not path.exists():
            fail(f"{path.name} not found at {path}")
            continue
        try:
            ast.parse(read(path))
            ok(f"{path.name} parses")
        except SyntaxError as exc:
            fail(
                f"{path.name} DOES NOT PARSE: line {exc.lineno}: {exc.msg}. "
                "The 2026-09-09 edits inserted prose into an f-string HTML body; "
                "look for an unescaped brace or an unbalanced quote near that line."
            )
    try:
        json.loads(read(STATE))
        ok("agent_state.json parses")
    except json.JSONDecodeError as exc:
        fail(f"agent_state.json DOES NOT PARSE: line {exc.lineno} col {exc.colno}: {exc.msg}")


# ---------------------------------------------------------------- check 2
def check_repair_held() -> None:
    print("\n[2] REPAIR HELD -- are the false attributions actually gone?")

    if GKA.exists():
        text = read(GKA)
        bad = []
        for i, line in enumerate(text.splitlines(), 1):
            if KHAN not in line:
                continue
            # Legitimate: source lists, the correction note, the one true
            # prevalence attribution. Illegitimate: currency or type 1 nearby.
            if CURRENCY.search(line) and "UNSOURCED" not in line and "Citation note" not in line:
                if "cost-effectiveness" in line or "T2D global burden" in line:
                    continue
                bad.append((i, line.strip()[:150]))
            elif TYPE1.search(line) and "UNSOURCED" not in line and "no type 1 data" not in line:
                bad.append((i, line.strip()[:150]))
        if bad:
            fail(f"build_gka_pricing.py still attaches PMID {KHAN} to {len(bad)} cost/T1D claim(s):")
            for lineno, snippet in bad:
                print(f"           line {lineno}: {snippet}")
        else:
            ok(f"build_gka_pricing.py: no PMID {KHAN} left on any cost or type 1 claim")

        if "Citation note (correction, 2026-09-09)" in text:
            ok("build_gka_pricing.py: correction note present and visible to readers")
        else:
            fail("build_gka_pricing.py: the 2026-09-09 correction note is missing")

    if ISLET.exists():
        text = read(ISLET)
        for i, line in enumerate(text.splitlines(), 1):
            if "1,477" in line and ALEJANDRO in line:
                fail(
                    f"build_islet_equity.py line {i} still attaches PMID {ALEJANDRO} to the "
                    "1,477 headline. That paper reports 325 recipients as of April 2008."
                )
                break
        else:
            ok(f"build_islet_equity.py: 1,477 headline no longer cites PMID {ALEJANDRO}")

        if "WITHDRAWN 2026-09-09" in text:
            ok("build_islet_equity.py: race-bar withdrawal notice present")
        else:
            fail("build_islet_equity.py: the race-bar withdrawal notice is missing")

        # The six withdrawn bars must not still be rendering as bar-fills.
        stale = re.findall(r'bar-fill[^>]*width:\s*(85|62|18|20)%', text)
        if stale:
            fail(
                f"build_islet_equity.py still renders {len(stale)} bar(s) at the withdrawn "
                "race percentages. Check whether another block reuses those widths."
            )
        else:
            ok("build_islet_equity.py: no withdrawn race bars still rendering")


# ---------------------------------------------------------------- check 3
def check_khan_repo_wide() -> None:
    print(f"\n[3] SAME DEFECT ELSEWHERE -- every PMID {KHAN} in the repo, near money or type 1")
    print("    Khan 2020 has no cost data and no type 1 data, so these are false by construction.")

    suspect = 0
    total = 0
    for path in sorted(REPO.rglob("*.py")):
        if ".git" in path.parts or path.name == Path(__file__).name:
            continue
        try:
            lines = read(path).splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if KHAN not in line:
                continue
            total += 1
            if "UNSOURCED" in line or "no cost data" in line or "T2D global burden" in line:
                continue
            if CURRENCY.search(line) or TYPE1.search(line):
                suspect += 1
                rel = path.relative_to(REPO)
                print(f"  [SUSPECT] {rel}:{i}")
                print(f"            {line.strip()[:170]}")

    if suspect:
        fail(
            f"{suspect} of {total} remaining PMID {KHAN} attachments sit next to a cost, "
            "price, revenue or type 1 claim. citation_load_bearing.json records 39 claims "
            "repo-wide for this PMID; the 2026-09-09 run repaired only build_gka_pricing.py."
        )
    else:
        ok(f"all {total} remaining PMID {KHAN} attachments look defensible")


# ---------------------------------------------------------------- check 4
def check_stale_threshold(online: bool) -> None:
    print("\n[4] STALE THRESHOLD -- how many real papers does the 42,000,000 rule flag?")

    found: dict[str, list[str]] = {}
    for path in sorted(REPO.rglob("*.py")):
        if ".git" in path.parts or path.name == Path(__file__).name:
            continue
        try:
            text = read(path)
        except OSError:
            continue
        for pmid in re.findall(r"\b(4[2-9]\d{6})\b", text):
            found.setdefault(pmid, []).append(path.name)

    if not found:
        ok("no PMIDs above 42,000,000 cited anywhere")
        return

    note(
        f"{len(found)} distinct PMIDs above 42,000,000 are cited. The daily task calls all "
        "of these 'fabricated'. On 2026-09-09, seven of them were round-tripped through "
        "eutils and all seven were real."
    )
    print("           " + ", ".join(sorted(found)))

    if not online:
        note("re-run with --online to resolve each against PubMed and get the true false-positive rate")
        return

    try:
        from urllib.request import urlopen
    except ImportError:
        note("urllib unavailable; skipping online resolution")
        return

    ids = ",".join(sorted(found))
    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        f"?db=pubmed&id={ids}&retmode=json"
    )
    try:
        with urlopen(url, timeout=45) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        note(f"PubMed lookup failed ({exc}); threshold check inconclusive")
        return

    result = payload.get("result", {})
    real, missing = [], []
    for pmid in sorted(found):
        entry = result.get(pmid)
        if entry and entry.get("title"):
            real.append(pmid)
        else:
            missing.append(pmid)

    print(f"  [RESULT] resolved on PubMed: {len(real)}   did NOT resolve: {len(missing)}")
    if missing:
        fail(
            "these PMIDs above 42,000,000 did NOT resolve and are genuine candidates for "
            f"fabrication: {', '.join(missing)}"
        )
    if real:
        note(
            f"{len(real)} of {len(found)} flagged PMIDs are real papers. The threshold rule's "
            f"false-positive rate is {100 * len(real) / len(found):.0f}%. Replace the integer "
            "ceiling with this resolution check."
        )


# ---------------------------------------------------------------- main
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--online",
        action="store_true",
        help="resolve high PMIDs against PubMed (one eutils call, no key needed)",
    )
    args = parser.parse_args()

    print("=" * 78)
    print("VERIFY 2026-09-09 REPAIRS")
    print(f"repo: {REPO}")
    print(f"run:  {date.today().isoformat()}")
    print("=" * 78)

    check_syntax()
    check_repair_held()
    check_khan_repo_wide()
    check_stale_threshold(args.online)

    print("\n" + "=" * 78)
    if failures:
        print(f"FAILED -- {len(failures)} check(s) did not pass:")
        for f in failures:
            print(f"  - {f}")
    else:
        print("PASSED -- all checks clean.")
    if notes:
        print(f"\n{len(notes)} note(s) requiring a decision, not a fix:")
        for n in notes:
            print(f"  - {n}")
    print("=" * 78)
    print(
        "\nNEXT, IF THIS PASSED: the site still has to be rebuilt and pushed. The rebuild\n"
        "never ran on 2026-09-09 because the sandbox was down, so these corrections exist\n"
        "in the builders only, not in docs/. And origin/main has been frozen at 2026-04-20\n"
        "for 142 days, so nothing here reaches a reader either way:\n"
        "    python Analysis\\Scripts\\run_quality_improvements.py\n"
        "    git add -A ; git commit -m \"2026-09-09 citation repairs\" ; git push origin main\n"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
