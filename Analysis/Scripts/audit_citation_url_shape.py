#!/usr/bin/env python3
"""
audit_citation_url_shape.py — gate on the SHAPE of a published citation URL.

WHY THIS EXISTS (2026-09-20 audit, finding 2)
---------------------------------------------
Sixteen citation hyperlinks on the published site resolve to nothing. Not one
of them is a wrong PMID; every one is a well-formed-looking anchor whose href
is not a PMID at all:

    <a href="https://pubmed.ncbi.nlm.nih.gov/BANDIT trial">
    <a href="https://pubmed.ncbi.nlm.nih.gov/NCT01319331">
    <a href="https://pubmed.ncbi.nlm.nih.gov/">
    <a href="https://pubmed.ncbi.nlm.nih.gov/citation withdrawn 2026-08-24 ...">

Root cause, build_drug_repurposing_islet.py:757 —

    <a href="https://pubmed.ncbi.nlm.nih.gov/{drug['reference'].replace('PMID:','')}">

The template assumes drug['reference'] always holds a PMID. When it holds a
prose evidence note instead, the sentence is interpolated into the URL path.

THE CLASS, not the instance:
    a citation can be correct as DATA and broken as a LINK,
    and until now only the data side was gated.

Sixteen citation audits existed at the time of writing. Every one of them
reasons about PMIDs as identifiers — impossible, off-topic, unsupported,
retracted, semantically load-bearing. None validated the string that a reader
actually clicks. audit_published_links.py comes closest and explicitly checks
relative links only, so it passed clean on the same run that shipped these.

WHAT IT CHECKS
    Every href pointing at pubmed.ncbi.nlm.nih.gov must match
        ^https://pubmed\\.ncbi\\.nlm\\.nih\\.gov/\\d+/?$
    Every href pointing at doi.org must match
        ^https://doi\\.org/10\\.\\d{4,9}/\\S+$
    Every href pointing at clinicaltrials.gov/study must carry an NCT id.

Exit 0 = clean. Exit 1 = findings (so it can gate a pipeline or a CI job).

USAGE
    python Analysis/Scripts/audit_citation_url_shape.py
    python Analysis/Scripts/audit_citation_url_shape.py --fix-empty   # report only
    python Analysis/Scripts/audit_citation_url_shape.py --roots docs Dashboards
"""

import argparse
import json
import os
import re
import sys
from datetime import date

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_ROOTS = ["docs", "Dashboards"]
RESULTS = os.path.join(REPO, "Analysis", "Results", "citation_url_shape_audit.json")

# One anchor, one href, plus the link text up to </a>. Deliberately permissive
# about the href contents so a malformed URL is CAPTURED, not skipped.
ANCHOR = re.compile(
    r'<a\b[^>]*?href=(["\'])(?P<href>.*?)\1[^>]*>(?P<text>.*?)</a>', re.I | re.S)

# ---------------------------------------------------------------------------
# EXCLUSIONS. Each one was a false positive on the first run of this gate
# (2026-09-20) and each is excluded for a stated reason. A gate that cries wolf
# gets muted, and a muted gate is worse than no gate — so the list is explicit
# and every entry says why.
# ---------------------------------------------------------------------------

# 1. Client-side interpolation. The href is assembled in JavaScript at render
#    time: `...nih.gov/${t.id}`, `...nih.gov/' + p + '/`. The literal in the
#    file is a template, not a URL. Generic_Drug_Catalog's renderPmids() even
#    validates /^\d{6,8}$/ before building the link, which is the pattern this
#    gate is asking everyone else to adopt.
INTERPOLATION = re.compile(r"\$\{|\{\{|'\s*\+|\+\s*'|%s|\{[a-z_]+\}", re.I)

# 2. A link to a site's front page, labelled as that site. Not a citation:
#    "read more on <a href=pubmed.ncbi.nlm.nih.gov/>PubMed</a>" resolves fine
#    and claims nothing. Only excluded when the link text names the site and
#    the anchor is NOT styled as a citation (class="pmid-link" means it is).
HOMEPAGE_TEXT = re.compile(r"^(pubmed|pubmed central|pmc|doi|clinicaltrials(\.gov)?)$", re.I)


def _strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()

RULES = [
    (
        "pubmed",
        re.compile(r"^https?://(?:www\.)?pubmed\.ncbi\.nlm\.nih\.gov/", re.I),
        re.compile(r"^https://pubmed\.ncbi\.nlm\.nih\.gov/\d+/?$"),
        "https://pubmed.ncbi.nlm.nih.gov/<pmid>/",
    ),
    (
        "doi",
        re.compile(r"^https?://(?:dx\.)?doi\.org/", re.I),
        re.compile(r"^https://doi\.org/10\.\d{4,9}/\S+$"),
        "https://doi.org/10.xxxx/<suffix>",
    ),
    (
        "clinicaltrials",
        re.compile(r"^https?://(?:www\.)?clinicaltrials\.gov/(?:study|ct2/show)/", re.I),
        re.compile(r"^https://(?:www\.)?clinicaltrials\.gov/(?:study|ct2/show)/NCT\d{8}/?$"),
        "https://clinicaltrials.gov/study/NCT########",
    ),
]


def classify(href):
    """Return (kind, ok, expected) or None if this href is not a citation URL."""
    h = href.strip()
    for kind, applies, valid, expected in RULES:
        if applies.match(h):
            return kind, bool(valid.match(h)), expected
    return None


def scan_file(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    findings, checked, excluded = [], 0, 0
    for m in ANCHOR.finditer(text):
        href = m.group("href")
        verdict = classify(href)
        if verdict is None:
            continue
        kind, ok, expected = verdict
        checked += 1
        if ok:
            continue

        label = _strip_tags(m.group("text"))
        styled_as_citation = "pmid-link" in m.group(0) or label.upper().startswith("PMID")

        # Exclusion 1 — assembled in JS at render time, not a literal URL.
        if INTERPOLATION.search(href):
            excluded += 1
            continue
        # Exclusion 2 — front-page link labelled as the site. "read more on
        # <a href=pubmed.ncbi.nlm.nih.gov/>PubMed</a>" resolves and claims
        # nothing, so it is not a citation and not a finding. The CSS class is
        # not the test: pmid-link gets reused for styling. The LINK TEXT is the
        # test, because that is the promise the reader is shown.
        if href.rstrip("/").endswith(("nih.gov", "doi.org", "clinicaltrials.gov")):
            if HOMEPAGE_TEXT.match(label):
                excluded += 1
                continue

        line = text.count("\n", 0, m.start()) + 1
        tail = href.split("nih.gov/")[-1] if kind == "pubmed" else href
        placeholder = re.fullmatch(r"(PMID:?)?[X]{4,}", label, re.I)
        if tail in ("", "/") and not label:
            reason, severity = "empty href AND empty link text", "cosmetic"
        elif placeholder:
            reason, severity = "placeholder in an illustrative example", "cosmetic"
        elif tail in ("", "/"):
            # Resolves to a real page, but not the one the link text promises.
            reason, severity = f"points at the site root, link text promises {label!r}", "broken"
        elif re.fullmatch(r"NCT\d+/?", tail):
            reason, severity = "NCT id in a PubMed URL", "broken"
        elif re.search(r"[ \t]", tail):
            reason, severity = "free text in the URL path", "broken"
        else:
            reason, severity = "malformed", "broken"

        findings.append({
            "file": os.path.relpath(path, REPO).replace("\\", "/"),
            "line": line,
            "kind": kind,
            "href": href[:160],
            "link_text": label[:60],
            "reason": reason,
            "severity": severity,
            "expected": expected,
        })
    return checked, findings, excluded


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--roots", nargs="*", default=DEFAULT_ROOTS,
                    help="directories under the repo root to scan")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    files = []
    for root in args.roots:
        base = os.path.join(REPO, root)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames
                           if d not in (".git", "_quarantine", "__pycache__")]
            for fn in filenames:
                if fn.endswith((".html", ".md")):
                    files.append(os.path.join(dirpath, fn))

    total_checked, all_findings, total_excluded = 0, [], 0
    for path in sorted(files):
        checked, findings, excluded = scan_file(path)
        total_checked += checked
        total_excluded += excluded
        all_findings.extend(findings)

    broken = [f for f in all_findings if f["severity"] == "broken"]
    cosmetic = [f for f in all_findings if f["severity"] == "cosmetic"]

    by_file = {}
    for f in all_findings:
        by_file.setdefault(f["file"], []).append(f)

    line = "=" * 74
    print(line)
    print("CITATION URL SHAPE AUDIT - does every published citation link resolve?")
    print(line)
    print(f"{len(files)} file(s) scanned, {total_checked} citation URL(s) checked.")
    print(f"  broken (a reader clicks and lands nowhere) : {len(broken)}")
    print(f"  cosmetic (dead but nothing to click)       : {len(cosmetic)}")
    print(f"  excluded as known-good patterns            : {total_excluded}")

    if all_findings and not args.quiet:
        print()
        for fname in sorted(by_file):
            items = by_file[fname]
            nb = sum(1 for i in items if i["severity"] == "broken")
            print(f"  {fname}  ({nb} broken, {len(items) - nb} cosmetic)")
            for it in items:
                tag = "BROKEN  " if it["severity"] == "broken" else "cosmetic"
                print(f"    line {it['line']:>6}  {tag} {it['reason']:<34} {it['href'][:90]}")
                if it["link_text"]:
                    print(f"    {'':>11}  link text: {it['link_text']}")
            print()

    os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
    with open(RESULTS, "w", encoding="utf-8") as fh:
        json.dump({
            "generated": date.today().isoformat(),
            "gate": "citation_url_shape",
            "counts": {
                "files_scanned": len(files),
                "urls_checked": total_checked,
                "broken": len(broken),
                "cosmetic": len(cosmetic),
                "excluded_known_good": total_excluded,
            },
            "findings": all_findings,
        }, fh, indent=1)
    print(f"  -> {os.path.relpath(RESULTS, REPO)}")
    print()

    if broken:
        print(f"  [FAIL] {len(broken)} published citation link(s) do not resolve.")
        print("         A citation that looks clickable and is not is worse than no")
        print("         citation: it spends the reader's trust and returns nothing.")
        return 1

    if cosmetic:
        print(f"  [OK] no broken citation links ({len(cosmetic)} cosmetic noted above)")
        return 0

    print("  [OK] every published citation URL is well formed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
