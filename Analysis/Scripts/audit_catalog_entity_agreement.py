#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_catalog_entity_agreement.py
=================================

NEW 2026-09-19, from two live defects found the same day in
build_generic_drug_catalog.py's evidence catalog:

  1. The Spironolactone entry's only citation was PMID 33264825 --
     "Effect of Finerenone on Chronic Kidney Disease Outcomes in Type 2
     Diabetes" (FIDELIO-DKD, NEJM 2020).  That is a trial of FINERENONE.
     Spironolactone appears nowhere in it.  The entry was graded MODERATE
     on it.

  2. The Minocycline entry's first citation was PMID 25714673 -- "Loss of
     survival factors and activation of inflammatory cascades in brain
     sympathetic centers in type 1 diabetic mice."  No minocycline, no
     neuropathy trial.  The entry described it as "Hu et al. 2015 diabetic
     neuropathy" and claimed "MIND trial showed neuropathy improvement."

WHY NO EXISTING GATE SAW EITHER ONE.  Every citation gate here scores the
PMID against the PROSE beside it.  In both defects the prose and the PMID
agreed with each other perfectly: the Spironolactone entry's reference text
says "FIDELIO-DKD (Bakris et al. 2020)", which is exactly what 33264825 is.
What disagreed was neither the title, the author, the journal nor the year --
it was the SUBJECT OF THE RECORD.  A catalog row is an assertion that the
cited paper is evidence ABOUT THE THING THE ROW IS NAMED AFTER, and nothing
in this repository tested that.

THE TEST.  For every catalog record that carries both a subject-entity field
('name', 'drug') and a citation field ('key_pmids', 'pmids', 'pmid'), look up
each cited PMID in the local paper library and ask whether the entity -- or a
declared alias -- appears anywhere in the title, abstract, MeSH terms or
keywords.

Verdicts:

  AGREE        entity (or alias) found in the cited paper's indexed text.
  ABSENT       entity found NOWHERE in title, abstract, MeSH or keywords.
               This is the defect class.  Both 2026-09-19 defects are here.
  UNCHECKABLE  PMID is cited by a catalog but is not in the paper library, so
               the repository has never held text to check it against.
               Reported, not failed -- the remedy is ingestion, not editing.

DELIBERATE LIMITS, stated so the next run does not overread a green line:
  * An ABSENT verdict says the cited paper does not mention the entity.  It
    does not say the paper is the wrong paper for every purpose -- a
    mechanism paper may legitimately support a row without naming the drug
    (class-effect reasoning).  ABSENT means "this needs a stated reason",
    not "this is false".  The two 2026-09-19 defects were both genuinely
    wrong; a third ABSENT could be a legitimate class citation.  The gate
    therefore requires an explicit in-file waiver comment rather than
    silence.
  * Only records reachable by literal-dict parsing are covered.  Records
    assembled at runtime are out of reach and counted in `records_skipped`.
  * Correction prose is NOT a citation.  A withdrawal note that quotes the
    offending PMID back is excluded, per the 2026-09-14 count-inflation
    finding.

Waiver: put  # ENTITY-WAIVER: <reason>  on the key_pmids line or the line
above it.  Waived records are listed separately and do not fail the gate.

Usage:
    python audit_catalog_entity_agreement.py           # measure, exit 0
    python audit_catalog_entity_agreement.py --gate    # exit 1 on ABSENT

Output: Analysis/Results/catalog_entity_agreement_audit.json
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
LIB = os.path.join(RESULTS, "paper_library")
OUT = os.path.join(RESULTS, "catalog_entity_agreement_audit.json")

ENTITY_FIELDS = ("name", "drug", "drug_name", "agent")
CITE_FIELDS = ("key_pmids", "pmids", "pmid", "key_pmid")

# Entities whose catalog row is not a drug and for which the test is
# meaningless (the row names a category, not a molecule).
NON_DRUG_ENTITIES = set()

WAIVER = re.compile(r"#\s*ENTITY-WAIVER:\s*(.+)")
# A withdrawn / corrected citation is annotated, not asserted.
WITHDRAWN = re.compile(
    r"WITHDRAWN|WRONG DRUG|WRONG PAPER|UNSOURCED|Repaired \d{4}-\d{2}-\d{2}|"
    r"CITATION REMOVED|previously read|previously attributed",
    re.IGNORECASE,
)


def load_library():
    idx_path = os.path.join(LIB, "index.json")
    if not os.path.exists(idx_path):
        return {}
    with open(idx_path, encoding="utf-8") as fh:
        idx = json.load(fh)
    return idx.get("papers", idx)


def load_external_titles():
    """Titles for cited-but-not-ingested PMIDs.

    Added the same day the gate was written, because the second 2026-09-19
    defect (minocycline <- PMID 25714673) landed in UNCHECKABLE purely
    because the paper had never been ingested, while its title was
    retrievable in one lookup. A title-only cache lets the gate reach that
    class. It is explicitly NOT evidence of support -- see the file header.
    """
    path = os.path.join(RESULTS, "external_pmid_titles.json")
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as fh:
            return (json.load(fh) or {}).get("papers", {})
    except (OSError, ValueError):
        return {}


EXTERNAL = None


def indexed_text(pmid, lib):
    """Title + abstract + MeSH + keywords for a PMID, lowercased.

    Falls back to the external title cache (title only, no abstract), whose
    verdicts are reported as TITLE_ONLY-sourced so nobody reads them as
    full-text checks.
    """
    entry = lib.get(str(pmid))
    if not isinstance(entry, dict):
        ext = (EXTERNAL or {}).get(str(pmid))
        if isinstance(ext, dict) and ext.get("title"):
            # TITLE ONLY. The cache's own `note` field discusses the defect
            # and names the entity, so including it would make every cached
            # PMID self-satisfy the test.
            return str(ext["title"]).lower()
        return None
    parts = [
        str(entry.get("title") or ""),
        " ".join(entry.get("mesh_terms") or []),
        " ".join(entry.get("keywords") or []),
    ]
    abs_path = os.path.join(LIB, "abstracts", f"{pmid}.json")
    if os.path.exists(abs_path):
        try:
            with open(abs_path, encoding="utf-8") as fh:
                a = json.load(fh)
            if isinstance(a, dict):
                for k in ("abstract", "text", "abstract_text"):
                    if a.get(k):
                        parts.append(str(a[k]))
                        break
                else:
                    parts.append(json.dumps(a))
            else:
                parts.append(str(a))
        except (OSError, ValueError):
            pass
    return " ".join(parts).lower()


def aliases(entity):
    """Search terms for a catalog entity name.

    'N-acetylcysteine (NAC)'  -> n-acetylcysteine, nac, acetylcysteine
    'Alpha-lipoic acid'       -> alpha-lipoic, lipoic
    """
    e = entity.strip().lower()
    out = {e}
    paren = re.findall(r"\(([^)]+)\)", e)
    for p in paren:
        out.add(p.strip())
    base = re.sub(r"\([^)]*\)", "", e).strip()
    out.add(base)
    # greek / hyphen variants and the distinctive stem
    if base.startswith("alpha-"):
        out.add(base.replace("alpha-", "α-"))
        out.add(base.split("-", 1)[1])
    if base.startswith("n-acetyl"):
        out.add("acetylcysteine")
    # longest token of >=5 chars is the distinctive stem (e.g. 'lipoic')
    toks = [t for t in re.split(r"[^a-zα]+", base) if len(t) >= 5]
    if toks:
        out.add(max(toks, key=len))
    return {a for a in out if len(a) >= 3}


def dict_records(tree, src_lines):
    """Yield (entity, [pmids], lineno, raw_lines) for literal dicts."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        fields = {}
        for k, v in zip(node.keys, node.values):
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                fields[k.value] = v
        ent_key = next((f for f in ENTITY_FIELDS if f in fields), None)
        cite_key = next((f for f in CITE_FIELDS if f in fields), None)
        if not ent_key or not cite_key:
            continue
        ent_node, cite_node = fields[ent_key], fields[cite_key]
        if not (isinstance(ent_node, ast.Constant)
                and isinstance(ent_node.value, str)):
            continue
        if isinstance(cite_node, ast.Constant) and isinstance(cite_node.value, str):
            raw = cite_node.value
        elif isinstance(cite_node, ast.List):
            raw = ", ".join(
                str(e.value) for e in cite_node.elts
                if isinstance(e, ast.Constant)
            )
        else:
            continue
        pmids = re.findall(r"\b\d{7,8}\b", raw)
        if not pmids:
            continue
        ln = getattr(cite_node, "lineno", node.lineno)
        ctx = "\n".join(src_lines[max(0, ln - 2):ln + 1])
        yield ent_node.value, pmids, ln, ctx


def main():
    global EXTERNAL
    gate = "--gate" in sys.argv
    lib = load_library()
    EXTERNAL = load_external_titles()
    print("=" * 62)
    print("  CATALOG ENTITY <-> CITATION AGREEMENT")
    print("=" * 62)
    print(f"  Paper library: {len(lib)} indexed PMIDs")

    agree, absent, uncheckable, waived = [], [], [], []
    files_scanned = 0
    records_skipped = 0

    for fn in sorted(os.listdir(HERE)):
        if not fn.endswith(".py") or fn == os.path.basename(__file__):
            continue
        path = os.path.join(HERE, fn)
        try:
            src = open(path, encoding="utf-8").read()
            tree = ast.parse(src)
        except (OSError, SyntaxError, UnicodeDecodeError):
            records_skipped += 1
            continue
        lines = src.splitlines()
        seen_any = False
        for entity, pmids, ln, ctx in dict_records(tree, lines):
            seen_any = True
            if entity in NON_DRUG_ENTITIES:
                continue
            wv = WAIVER.search(ctx)
            terms = aliases(entity)
            for pmid in pmids:
                rec = {
                    "file": fn, "line": ln, "entity": entity,
                    "pmid": pmid, "aliases": sorted(terms),
                }
                if WITHDRAWN.search(ctx) and not wv:
                    # annotated correction, not a live assertion
                    continue
                text = indexed_text(pmid, lib)
                if text is None:
                    rec["verdict"] = "UNCHECKABLE"
                    rec["reason"] = "PMID not in paper library"
                    uncheckable.append(rec)
                    continue
                hit = next((a for a in terms if a in text), None)
                in_lib = isinstance(lib.get(pmid), dict)
                rec["evidence_source"] = (
                    "library_title_abstract_mesh" if in_lib else
                    "external_title_cache_TITLE_ONLY")
                rec["title"] = (
                    (lib.get(pmid) or {}).get("title", "")[:120] if in_lib
                    else str((EXTERNAL.get(pmid) or {}).get("title", ""))[:120])
                if hit:
                    rec["verdict"] = "AGREE"
                    rec["matched_on"] = hit
                    agree.append(rec)
                elif wv:
                    rec["verdict"] = "WAIVED"
                    rec["waiver"] = wv.group(1).strip()
                    waived.append(rec)
                else:
                    rec["verdict"] = "ABSENT"
                    absent.append(rec)
        if seen_any:
            files_scanned += 1

    print(f"  Builders with parseable catalog records: {files_scanned}")
    print(f"  AGREE       {len(agree)}")
    print(f"  ABSENT      {len(absent)}   <- defect class")
    print(f"  UNCHECKABLE {len(uncheckable)}  (cited but never ingested)")
    print(f"  WAIVED      {len(waived)}")
    print()

    if absent:
        print("  ABSENT -- cited paper does not mention the entity anywhere")
        print("  " + "-" * 58)
        for r in absent:
            print(f"  {r['file']}:{r['line']}  {r['entity']}  <- PMID {r['pmid']}")
            print(f"      cited paper: {r['title']}")
        print()

    if uncheckable:
        print("  UNCHECKABLE -- cited by a catalog, absent from the library")
        print("  " + "-" * 58)
        by_ent = {}
        for r in uncheckable:
            by_ent.setdefault(f"{r['file']} {r['entity']}", []).append(r["pmid"])
        for k, v in sorted(by_ent.items()):
            print(f"  {k}: {', '.join(v)}")
        print()

    payload = {
        "audit": "catalog_entity_agreement",
        "run_date": str(date.today()),
        "library_size": len(lib),
        "files_with_records": files_scanned,
        "counts": {
            "agree": len(agree),
            "absent": len(absent),
            "uncheckable": len(uncheckable),
            "waived": len(waived),
        },
        "absent": absent,
        "uncheckable": uncheckable,
        "waived": waived,
        "agree": agree,
        "limits": [
            "ABSENT means the cited paper does not name the entity; a "
            "legitimate class-effect citation can land here and needs a "
            "stated ENTITY-WAIVER reason rather than silence.",
            "Only literal-dict records are reachable; runtime-assembled "
            "records are out of scope.",
            "Annotated corrections and withdrawals are excluded from live "
            "counts (2026-09-14 count-inflation finding).",
        ],
    }
    os.makedirs(RESULTS, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"  Output: {OUT}")

    if gate and absent:
        print("  [FAIL] catalog records cite papers that never mention them")
        return 1
    print("  [OK] no unexplained entity/citation disagreement" if gate
          else "  [MEASURE] reporting only; not gating")
    return 0


if __name__ == "__main__":
    sys.exit(main())
