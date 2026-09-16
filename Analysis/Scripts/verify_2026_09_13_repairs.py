"""
verify_2026_09_13_repairs.py

Checks that the citation repairs made on 2026-09-13 are still present in builder
source, and that none of them regressed. Cheap, no network, no PubMed lookup.

Run BEFORE run_quality_improvements.py:
    python Analysis/Scripts/verify_2026_09_13_repairs.py

WHAT WAS REPAIRED ON 2026-09-13
-------------------------------
Two of the three known citation concentrations were swept using the mechanical
content test (no lookup required, because each paper's true contents are known):

  PMID 34763823 - Herman & Kuo, "100 Years of Insulin: Why Is Insulin So
      Expensive", Endocrinol Metab Clin North Am 2021. A review of INSULIN
      pricing. TEST: any attachment to a price for a NON-insulin drug, to a
      device cost, to a clinician fee, or to a date after 2021 is false by
      construction. 32 such attachments removed across 6 files. Five insulin
      attachments were deliberately RETAINED as on-topic (build_gka_pricing.py
      552-554 and 599; build_health_equity.py 940, 944, 1005) - a guard that
      fails on those is wrong; see the note on the regression guard below.

  PMID 37909353 - "Economic Costs of Diabetes in the U.S. in 2022",
      Diabetes Care 2024;47(1):26-43. A US cost-of-illness study reporting
      national aggregates ($412.9B total, $306.6B direct, $106.3B indirect,
      $19,736 mean per-person expenditure, $12,022 attributable, 2.6x ratio,
      17% of direct costs on glucose-lowering drugs/supplies). TEST: it
      contains no ICER, no QALY, no cost-effectiveness threshold, no unit
      price, no Medicare median, and no global figure. 41 attachments removed
      from build_lada_diagnostic_model.py.

  PMID 29710129 - Hernandez, Prasad & Gellad, "Total Costs of Chimeric Antigen
      Receptor T-Cell Immunotherapy", JAMA Oncol 2018;4(7):994-996. TEST: any
      attachment to a non-CAR-T cost is false. 2 removed.

  PMID 22336824 - Shan et al., "Pentoxifylline for diabetic kidney disease",
      Cochrane 2012. NOT a misattribution: correctly identified, but cited in
      SUPPORT of a MODERATE grade when its stated conclusion is that evidence
      is INSUFFICIENT. Direction disclosed in place; grade left unchanged.

Confidence: LIKELY, not CERTAIN. Paper contents were read from published
abstracts and journal listings via web search, not round-tripped through
eutils, because the sandbox has been unavailable since 2026-09-09.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "Analysis" / "Scripts"

# Files that hold these PMIDs only as audit records or correction notices,
# never as live attachments. This script never opens them; the set is kept as
# documentation for the next run's sweep, which should skip them too.
AUDIT_TRAIL_FILES = (
    "audit_citation_load_bearing.py",
    "build_corpus_analysis.py",
    "build_statistical_analysis.py",
    "_run_2026_08_27.py",
    "verify_2026_09_12_repairs.py",
    "verify_2026_09_13_repairs.py",
)

CURRENCY = re.compile(r"[$£€]")

failures = []
notes = []


def live_attachments(pmid, filename, window=200):
    """Return contexts where the PMID sits inside a citation marker."""
    path = SCRIPTS / filename
    if not path.exists():
        notes.append(f"SKIP {filename} (not found)")
        return []
    text = path.read_text(encoding="utf-8")
    hits = []
    for m in re.finditer(r"\(PMID:%s\)|PMID:%s" % (pmid, pmid), text):
        start = max(0, m.start() - window)
        ctx = text[start:m.end() + window]
        hits.append((m.start(), ctx))
    return hits


def check_no_currency_attachment(pmid, filename, allow_substring=None):
    """
    Fail if the PMID appears with a currency symbol nearby and WITHOUT the
    exempting substring (e.g. 'insulin') in the same window.
    """
    for pos, ctx in live_attachments(pmid, filename):
        if not CURRENCY.search(ctx):
            continue
        low = ctx.lower()
        if allow_substring and allow_substring in low:
            continue
        # A withdrawal notice quoting the PMID is not an attachment.
        if "unsourced" in low or "citation removed" in low or "withdraw" in low:
            continue
        excerpt = " ".join(ctx.split())[:220]
        failures.append(
            f"{filename}: PMID {pmid} still attached to a currency figure "
            f"at offset {pos}\n    ...{excerpt}..."
        )


def check_absent(pmid, filename):
    """Fail if any live '(PMID:x)' marker remains at all."""
    path = SCRIPTS / filename
    if not path.exists():
        notes.append(f"SKIP {filename} (not found)")
        return
    text = path.read_text(encoding="utf-8")
    n = text.count("(PMID:%s)" % pmid)
    if n:
        failures.append(
            f"{filename}: {n} live '(PMID:{pmid})' marker(s) remain; "
            f"expected 0 after the 2026-09-13 sweep"
        )


def check_contains(filename, needle, label):
    path = SCRIPTS / filename
    if not path.exists():
        notes.append(f"SKIP {filename} (not found)")
        return
    if needle not in path.read_text(encoding="utf-8"):
        failures.append(f"{filename}: expected marker missing - {label}")


print("=" * 72)
print("verify_2026_09_13_repairs.py")
print("=" * 72)

# --- PMID 34763823: insulin-pricing review -------------------------------
# 'insulin' in the window exempts the attachment (the paper's real subject).
for f in (
    "build_gka_pricing.py",
    "build_gka_landscape.py",
    "build_health_equity.py",
    "build_gap_deep_dives.py",
    "build_gap_synthesis.py",
):
    check_no_currency_attachment("34763823", f, allow_substring="insulin")

# --- PMID 37909353: US cost-of-illness study -----------------------------
check_absent("37909353", "build_lada_diagnostic_model.py")
check_contains(
    "build_lada_diagnostic_model.py",
    "FORTY-ONE",
    "provenance-withdrawal note for the 41 attachments of PMID 37909353",
)

# --- PMID 29710129: CAR-T cost research letter ---------------------------
check_no_currency_attachment("29710129", "build_gka_landscape.py")
check_no_currency_attachment("29710129", "build_gap_deep_dives.py")

# --- PMID 22336824: direction disclosure ---------------------------------
check_contains(
    "build_generic_drug_catalog.py",
    "CITATION DIRECTION CORRECTED 2026-09-13",
    "pentoxifylline Cochrane direction disclosure",
)

# --- Regression guard: the correction-scope defect -----------------------
# A file must not simultaneously mark a figure UNSOURCED and re-assert the
# same PMID as its provenance elsewhere. Three instances of this were found
# on 2026-09-13 in build_gka_pricing.py and build_gap_deep_dives.py.
#
# NOTE ON THIS GUARD'S FIRST DRAFT, kept because the repo documents its own
# corrections: as originally written it tested `withdrawn` FILE-WIDE, so any
# file containing both the PMID and the string UNSOURCED anywhere counted as
# withdrawn. It therefore fired on build_gka_pricing.py:599 - the one
# attachment this run deliberately KEPT, because it correctly describes the
# paper as an insulin-pricing review. A guard that fails on the correct
# citation is the same mistake the 2026-09-12 run caught in the
# self-confessed-doubt gate: measure before wiring in. Now scoped to a single
# source line, with the same 'insulin' exemption used above.
SOURCE_LINE = re.compile(r"(Data source|Sources?|Data compiled from):(.*)")

for filename in ("build_gka_pricing.py", "build_gap_deep_dives.py",
                 "build_gka_landscape.py"):
    path = SCRIPTS / filename
    if not path.exists():
        continue
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = SOURCE_LINE.search(line)
        if not m:
            continue
        tail = m.group(2)
        low = line.lower()
        # A line that withdraws provenance, or that quotes the old wording in
        # a correction notice, is not a live source assertion.
        if any(k in low for k in
               ("unsourced", "citation removed", "no primary source",
                "no source", "corrected 20", "previously read")):
            continue
        for pmid, exempt in (("34763823", "insulin"),
                             ("37909353", None),
                             ("29710129", "car-t")):
            if ("PMID:%s" % pmid) not in tail:
                continue
            if exempt and exempt in low:
                continue
            failures.append(
                f"{filename}:{lineno}: PMID {pmid} is still named as provenance "
                f"in a source line, with no topic exemption. This is the "
                f"2026-09-09 correction-scope defect.\n    {line.strip()[:180]}"
            )

# --- Syntax check: four days of unexecuted file-tool edits ---------------
import ast

for path in sorted(SCRIPTS.glob("build_*.py")):
    try:
        ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as e:
        failures.append(f"{path.name}: SYNTAX ERROR line {e.lineno}: {e.msg}")

print()
for n in notes:
    print("  [note]", n)

if failures:
    print("\n[FAIL] %d issue(s):\n" % len(failures))
    for f in failures:
        print("  -", f)
    sys.exit(1)

print("\n[OK] all 2026-09-13 repairs present; no regressions; all builders parse.")
sys.exit(0)
