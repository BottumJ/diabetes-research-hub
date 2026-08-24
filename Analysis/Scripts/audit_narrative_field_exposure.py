"""audit_narrative_field_exposure.py

WHY THIS EXISTS
---------------
On 2026-08-23 nine false prose citations sat in path narrative fields for three
days before repair. Nobody had ever measured whether those fields are RENDERED
into docs/ (public exposure) or are internal-only bookkeeping (private
exposure). That distinction sets the severity of the entire class of
"wrong citation buried in prose" defects, and it was unknown.

WHAT IT MEASURES
----------------
For every narrative (free-text) field on every record in state["paths"],
state["validated_paths"] and state["gaps"], take distinctive fixed-length
windows of the text, normalise them the same way the published HTML is
normalised (tags stripped, entities decoded, whitespace collapsed), and test
whether any window appears in docs/.

A field TYPE is PUBLIC if any of its values is found in docs/.
A field TYPE is INTERNAL if none of its values is found anywhere in docs/.

Output: Analysis/Results/narrative_field_exposure.json

METHOD NOTES / LIMITS
---------------------
- Absence of a match is evidence the string is not published VERBATIM. A
  builder that paraphrases or truncates a field would defeat this test, so
  INTERNAL means "not rendered verbatim", not "provably never surfaced".
- Windows are taken from the middle of the text as well as the head, because
  several builders emit a truncated prefix.
- Short fields (< MIN_LEN chars) are skipped as non-distinctive.
"""

import html
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE = os.path.join(REPO, "Analysis", "Results", "agent_state.json")
DOCS = os.path.join(REPO, "docs")
OUT = os.path.join(REPO, "Analysis", "Results", "narrative_field_exposure.json")

WINDOW = 45          # chars per probe window - long enough to be unique
STRICT_WINDOW = 110  # a match this long cannot be boilerplate collision
MIN_LEN = 40         # skip fields shorter than this
PROBES_PER_VALUE = 4  # head, 1/3, 1/2, 2/3

# Fields that are structured identifiers / dates / enums, not prose.
NON_NARRATIVE = {
    "status", "rating", "date", "validated_date", "last_validated",
    "validation_date", "validation_status", "confidence", "tier",
    "external_pmids", "corpus_pmids", "pmids_supporting", "data_point_count",
    "last_data_point_count", "corpus_data_points_stored",
    "corpus_data_points_corrected", "corpus_dpc", "backfilled_on",
    "merged_on", "merged_from", "mirrored_on", "mirrored_from",
    "last_audited", "last_audit_date", "next_due", "next_audit_due",
    "next_audit", "revisited_date", "last_reaffirmed", "last_revalidated",
    "last_revisited", "reaffirmed", "corpus_evidence_points",
    "promotion_candidate", "preclinical_confidence", "clinical_confidence",
    "validated_by", "path_name", "external_urls", "watch_flag",
    "dashboard_tier_reconciled", "requires_dashboard_update",
    "backfilled_from", "source",
}

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def normalise(text):
    """Collapse to the canonical comparison form used on both sides."""
    text = html.unescape(text)
    text = TAG.sub(" ", text)
    text = WS.sub(" ", text)
    return text.strip().lower()


def load_docs_corpus():
    """Every rendered byte under docs/, normalised, concatenated."""
    chunks = []
    files = 0
    for root, _dirs, names in os.walk(DOCS):
        for name in names:
            if not name.lower().endswith((".html", ".htm", ".md", ".js", ".json", ".csv")):
                continue
            path = os.path.join(root, name)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    chunks.append(normalise(fh.read()))
                files += 1
            except OSError:
                continue
    return " ".join(chunks), files


def probes(value):
    """Distinctive windows drawn from head and interior of the string."""
    norm = normalise(value)
    if len(norm) < MIN_LEN:
        return []
    out = []
    span = max(len(norm) - WINDOW, 0)
    for i in range(PROBES_PER_VALUE):
        start = int(span * i / PROBES_PER_VALUE)
        out.append(norm[start:start + WINDOW])
    return [p for p in out if len(p) >= MIN_LEN]


def walk_strings(obj, prefix=""):
    """Yield (field_name, string) for every string leaf, keyed by its own key."""
    if isinstance(obj, dict):
        for key, val in obj.items():
            yield from walk_strings(val, key)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_strings(item, prefix)
    elif isinstance(obj, str):
        yield prefix, obj


def main():
    with open(STATE, "r", encoding="utf-8") as fh:
        state = json.load(fh)

    corpus, n_files = load_docs_corpus()
    print("[docs] scanned %d rendered files, %d normalised chars"
          % (n_files, len(corpus)))

    # field_type -> {"values": n, "found": n, "examples_found": [...]}
    tally = {}

    for store in ("paths", "validated_paths", "gaps"):
        records = state.get(store, {})
        for record_key, record in records.items():
            for field, value in walk_strings(record):
                if field in NON_NARRATIVE or not field:
                    continue
                windows = probes(value)
                if not windows:
                    continue
                slot = tally.setdefault(
                    "%s.%s" % (store, field),
                    {"values_tested": 0, "values_found": 0,
                     "found_examples": [], "unfound_example": None},
                )
                slot["values_tested"] += 1
                matched = [w for w in windows if w in corpus]
                if matched:
                    slot["values_found"] += 1
                    # STRICT tier: a 45-char head can collide with generic
                    # boilerplate ("calcineurin inhibitors (tacrolimus,
                    # cyclospor" matched the data dictionary by coincidence on
                    # 2026-08-24). Require >=2 windows AND a long window.
                    long_win = normalise(value)[:STRICT_WINDOW]
                    strict = len(matched) >= 2 and len(long_win) >= STRICT_WINDOW \
                        and long_win in corpus
                    if strict:
                        slot["values_found_strict"] = \
                            slot.get("values_found_strict", 0) + 1
                    if len(slot["found_examples"]) < 3:
                        slot["found_examples"].append(
                            {"record": record_key, "matched_window": matched[0],
                             "strict": strict})
                elif slot["unfound_example"] is None:
                    slot["unfound_example"] = {
                        "record": record_key, "probe": windows[0]}

    public, internal, weak = [], [], []
    for name, slot in sorted(tally.items()):
        slot.setdefault("values_found_strict", 0)
        if slot["values_found_strict"]:
            slot["verdict"] = "PUBLIC"
            public.append(name)
        elif slot["values_found"]:
            slot["verdict"] = "COLLISION_ONLY"
            weak.append(name)
        else:
            slot["verdict"] = "INTERNAL"
            internal.append(name)

    result = {
        "generated": "audit_narrative_field_exposure.py",
        "docs_files_scanned": n_files,
        "method": "verbatim %d-char window match after tag-strip + whitespace "
                  "collapse; INTERNAL means not rendered VERBATIM, not "
                  "provably never surfaced" % WINDOW,
        "public_fields": public,
        "collision_only_fields": weak,
        "internal_fields": internal,
        "detail": tally,
    }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)

    print("\n=== NARRATIVE FIELD EXPOSURE ===")
    for name in sorted(tally, key=lambda n: -tally[n]["values_found_strict"]):
        slot = tally[name]
        if slot["verdict"] == "INTERNAL":
            continue
        print("  %-45s %-15s strict %d/%d  loose %d/%d"
              % (name, slot["verdict"], slot["values_found_strict"],
                 slot["values_tested"], slot["values_found"],
                 slot["values_tested"]))
    print("\nPUBLIC field types (rendered verbatim): %d" % len(public))
    print("COLLISION_ONLY (short-window match only): %d" % len(weak))
    print("INTERNAL field types: %d" % len(internal))
    print("[OK] wrote %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
