#!/usr/bin/env python3
"""
audit_prose_author_surnames.py
==============================
Added 2026-09-15.

WHAT THIS CHECKS
----------------
An entire assertion class that no other gate in this repository sees.

Existing gate `audit_prose_citation_titles.py` checks whether a citation
asserts a TITLE and whether that title matches the library. It has nothing
to say about a SURNAME. So a builder can print

    "Hering et al. (PMID: 37105208)"

and every gate passes, even though PMID 37105208 is Chetboun et al.

This gate reads the first author from the paper library's own abstracts JSON
(`authors[0]`), so it needs NO web lookup and NO eutils call.

WHAT IT DOES *NOT* DO
---------------------
It does not flag a PMID that is absent from the library. Those are reported
as UNKNOWN, separately and without prejudice, because the assertion may be
perfectly true -- we simply have no local ground truth for it.

It does not flag the repository's own correction prose. A sentence that
says "the 'Zarin et al.' attribution was withdrawn" contains both a surname
and a PMID and is CORRECT prose about an incorrect citation. Counting those
as live defects is exactly the inflation that made the 29710129 estimate
wrong by 8x (see work_queue 2026-09-14).

EXIT CODE
---------
0 always in --measure mode (reporting only).
1 when run as a gate (--gate) and live mismatches exist.
"""

import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LIB = ROOT / "Analysis" / "Results" / "paper_library" / "abstracts"
OUT = ROOT / "Analysis" / "Results" / "prose_author_surname_audit.json"

# --- how close a surname has to be to a PMID to count as an attribution ---
#
# PAIRING RULE (rewritten 2026-09-15 after the first measurement).
#
# The obvious rule -- "find a PMID within N characters either side of the
# surname" -- DOES NOT WORK in this repository and must not be reinstated.
# It produced 103 hits, and inspection of the source showed essentially all
# of them were correct citations. The reason is that this repo writes its
# sources as semicolon-separated runs:
#
#   Hoppe et al. Lancet Diabetes Endocrinol 2017 (PMID:28010783) - ...;
#   Zhang et al. BMC Med 2022 (PMID:36109742) - ...;
#   Clemens et al. Diabetes Care 2020 (PMID:32312859) - ...
#
# A symmetric window centred on "Zhang" reaches BACKWARDS into Hoppe's PMID
# and matches it first, so every surname in the list gets tested against its
# PREDECESSOR's PMID. The result is a perfect shift-by-one chain of fake
# mismatches, which is exactly what the first run reported.
#
# The citation format is "<Surname> et al. <Journal> <Year> (PMID:NNNN)", so
# the PMID that belongs to a surname is the NEXT one FORWARD. We therefore:
#   * scan forward only,
#   * stop at a separator that ends the citation (; newline, bullet), and
#   * stop if another "et al." claims the PMID first.
WINDOW = 160       # forward reach, surname -> its own PMID
BACK_WINDOW = 60   # backward reach, for "[PMID:N - Surname et al.]" order

# --- the repository's own correction / withdrawal prose ---------------------
# An occurrence whose surrounding window contains any of these is prose ABOUT
# a citation, not a live citation. Mirrors the exclusion the 2026-09-14 queue
# item specified for the load-bearing counts.
CORRECTION_MARKERS = (
    "withdrawn", "withdrew", "withdrawal",
    "removed", "removal",
    "mis-attributed", "misattributed", "misattribution",
    "previously cited", "previously attributed", "previously given",
    "unsourced", "UNSOURCED",
    "corrected 2026-", "corrected 2025-",
    "incorrectly", "wrongly", "false attribution",
    "not in fact", "is actually", "it is actually",
    # past-tense prose ABOUT a citation, and retraction exemplars
    "this block cited", "still reads", "still reading",
    "retracted", "exemplar", "was cited", "had cited",
    # ADDED 2026-09-16. Every marker below was harvested from a real flag in
    # this run that turned out to be the repository correctly DESCRIBING a bad
    # citation - including three comments written by this run's own repairs.
    # NOTE what is deliberately NOT here: "not a defect". That phrase is how
    # PMID 37359825 was laundered into agent_state.json as verified on
    # 2026-09-14 while carrying a false surname. A gate must not be silenced
    # by an assertion that there is nothing to see.
    "was labelled", "was labeled", "were jointly labelled",
    "re-pointed", "repointed", "the intended paper is",
    "this row read", "this entry read", "why each is wrong",
    "none was correct", "wrong author", "wrong journal", "wrong subject",
    "attributed to", "surname corrected", "is not an author",
    "hid there", "inherited the surname",
)

# --- surnames that are not surnames ---------------------------------------
# "et al." is sometimes preceded by a placeholder or a group name.
NOT_A_SURNAME = {
    "Author", "Authors", "Surname", "Name", "Study", "Trial", "Group",
    "Investigators", "Consortium", "Collaboration", "Et", "See", "Ibid",
    "The", "A", "An", "Of", "In", "By", "As", "Per", "Source", "Ref",
    "Example", "Placeholder", "Smith", "Doe",
}

PMID_RE = re.compile(r"PMID[:\s#]*(\d{6,9})", re.IGNORECASE)

# A capitalised surname, optionally followed by PubMed-style initials
# ("Khan MAB et al.", "Herold KC, et al."), then "et al".
# Group 1 is the surname; the initials group is discarded. Without this the
# initials themselves were captured as the surname, producing hits like
# "MAB et al." and "KC et al." -- 22 of them in the first measurement.
# Also tolerates slash-joined author runs -- this repo writes
# "Reichman/Markmann/Odorico et al." -- where the FIRST element is the first
# author. Capturing only the token adjacent to "et al" picked up the LAST
# name in the chain and reported a false mismatch.
SURNAME_RE = re.compile(
    r"\b([A-Z][A-Za-z'’‐-]{1,24}"        # surname ...
    r"(?:/[A-Z][A-Za-z'’‐-]{1,24})*)"    # ... optional /-joined run
    r"(?:\s+[A-Z]{1,4})?"                          # optional initials block
    r"\s*,?\s+et\s+al\b"
)

# What ends a citation. If one of these appears between the surname and the
# next PMID, that PMID belongs to a different citation.
SEPARATOR_RE = re.compile(r"[;\n•]|</|\|\|")


# ---------------------------------------------------------------------------
# ADDED 2026-09-16 -- two reach gaps, both found by a real defect, not theory.
#
# GAP 1: IDENTIFIERS INSIDE MARKUP, NOT PROSE.
#   build_islet_outcomes.py emitted
#       <a href="#" onclick="alert('PMID: 10919952')">Shapiro et al., NEJM</a>
#   The PMID sits in a JavaScript string and the surname in the anchor text.
#   The prose pairing rule CANNOT bind them: scanning backward from "Shapiro"
#   crosses "'); return false;\">", and SEPARATOR_RE stops on the semicolon,
#   so the pair is discarded; scanning forward then reaches the NEXT row's
#   PMID. Loosening the separator rule to fix this would reintroduce exactly
#   the shift-by-one chain the PAIRING RULE above exists to prevent.
#   So this is a SEPARATE scanner with its own, tighter rule: one anchor
#   element, PMID anywhere in its attributes, surname in its own text. There
#   is no ambiguity about which PMID belongs to which name inside one <a>.
#   These are the citations a reader actually clicks, so their reach matters
#   more per occurrence than prose.
#
# GAP 2: "UNKNOWN" WAS A HIDING PLACE, NOT A NEUTRAL BUCKET.
#   The gate deliberately does not flag a PMID absent from the local library.
#   That is defensible, but on 2026-09-16 the class it protects turned out to
#   contain a live defect: PMID 37359825 was attributed to "Voglova et al." in
#   five places; it is Wisel SA et al., Transpl Int 2023;36:11367, and
#   "Voglova" is not an author on it. It was invisible because the paper is
#   not in the library. Worse, a 2026-09-14 verification pass had confirmed
#   the paper's CONTENTS (which are reported correctly) and inherited the
#   surname from the prose it was auditing, then recorded it in agent_state
#   as "Not a defect - the CORRECT source", which would have made every later
#   sweep skip it.
#   NOTE THE SELECTION EFFECT: a PMID is missing from the library precisely
#   when it was added recently and by hand -- which is also when it is most
#   likely to be wrong. "Unknown" was concentrated on the riskiest citations.
#   --resolve-unknown therefore looks the remainder up against NCBI esummary
#   and caches the answer. It is OPT-IN so the default run stays offline and
#   the pipeline cannot fail on a network blip.
# ---------------------------------------------------------------------------

RESOLVE_CACHE = ROOT / "Analysis" / "Results" / ".surname_resolve_cache.json"

# One <a ...> element: attributes (which may carry a PMID) then anchor text.
ANCHOR_RE = re.compile(
    r"<a\b([^>]*)>(.*?)</a>", re.IGNORECASE | re.DOTALL)

# HTML comments are this repo's correction prose in generated output.
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def load_resolve_cache():
    try:
        return json.loads(RESOLVE_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_resolve_cache(cache):
    RESOLVE_CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True),
                             encoding="utf-8")


def resolve_pmids(pmids, cache):
    """pmid -> {surname, all_surnames, journal, year, title} via NCBI esummary.

    Cached on disk. Never raises: a network failure leaves the PMID unresolved
    and it stays in the UNKNOWN bucket, which is the pre-existing behaviour.
    """
    import urllib.request
    todo = [p for p in sorted(set(pmids)) if p not in cache]
    for i in range(0, len(todo), 100):
        chunk = todo[i:i + 100]
        url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
               "?db=pubmed&retmode=json&id=" + ",".join(chunk))
        try:
            with urllib.request.urlopen(url, timeout=30) as fh:
                res = json.loads(fh.read().decode("utf-8", "replace"))["result"]
        except Exception as exc:          # offline / rate-limited / 5xx
            print(f"  [warn] esummary lookup failed ({type(exc).__name__}); "
                  f"{len(chunk)} PMIDs stay UNKNOWN")
            break
        for uid in res.get("uids", []):
            r = res.get(uid, {})
            authors = [a.get("name", "") for a in (r.get("authors") or [])
                       if a.get("authtype") == "Author" or "name" in a]
            if not authors:
                continue
            cache[uid] = {
                "surname": surname_of(authors[0]),
                "all_surnames": [surname_of(a) for a in authors],
                "journal": r.get("source", ""),
                "year": (r.get("pubdate") or "")[:4],
                "title": r.get("title", ""),
                "_src": "ncbi_esummary",
            }
        for uid in chunk:                 # record misses so we do not re-ask
            cache.setdefault(uid, None)
    return cache


def scan_html_anchors(text, path_label, lib):
    """Yield (surname, pmid, context) for every <a> whose attributes carry a
    PMID and whose anchor text names an author. Unambiguous by construction:
    one element, one identifier, one name."""
    text = HTML_COMMENT_RE.sub(" ", text)
    for m in ANCHOR_RE.finditer(text):
        attrs, inner = m.group(1), m.group(2)
        pm = PMID_RE.search(attrs)
        if not pm:
            continue
        inner_plain = re.sub(r"<[^>]+>", " ", inner)
        sm = SURNAME_RE.search(inner_plain)
        if not sm:
            continue
        surname = sm.group(1).split("/")[0]
        if surname in NOT_A_SURNAME:
            continue
        yield surname, pm.group(1), " ".join(m.group(0).split())[:220]


_INITIALS = re.compile(r"^[A-Z]{1,4}$")


def author_list(raw):
    """Coerce a library 'authors' field to a list of 'Surname Initials' strings.

    2026-09-23: the 41986815 'B' defect was NOT a name-splitting bug. That one
    record (hand-curated, 2026-04-17) stores authors as a single comma-joined
    STRING; str[0] is its first character. It is the only str-typed record of
    389 (376 list-of-str, 8 empty list, 4 missing). Coercing here removes the
    class instead of guessing at it by length.
    """
    if isinstance(raw, str):
        raw = [a for a in raw.split(",")]
    return [html.unescape(str(a)).strip() for a in (raw or []) if str(a).strip()]


def surname_of(author):
    """'De Meyts P' -> 'De Meyts'; 'Chetboun M' -> 'Chetboun'; 'So M' -> 'So'.

    The previous rule, split()[0], turned every multi-word surname into its
    first particle ('De', 'Machado', 'Abdelfadil'). Drop only a trailing
    PubMed initials token; keep everything before it.
    """
    toks = author.split()
    if len(toks) > 1 and _INITIALS.match(toks[-1]):
        toks = toks[:-1]
    return " ".join(toks)


def surname_variants(surname):
    """Forms under which prose may legitimately cite this surname: the whole
    thing, and each word of it (prose often writes 'Meyts' or 'Cigrovski')."""
    toks = surname.split()
    return {normalise(surname)} | ({normalise(t) for t in toks if len(t) > 1}
                                   if len(toks) > 1 else set())


def load_library():
    """pmid -> (first_author_surname, journal, year, title)"""
    lib = {}
    if not LIB.is_dir():
        return lib
    for p in LIB.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        authors = author_list(d.get("authors"))
        if not authors:
            continue
        # PubMed author strings are "Surname Initials" e.g. "Chetboun M"
        surname = surname_of(authors[0])
        lib[str(d.get("pmid") or p.stem)] = {
            "surname": surname,
            "all_surnames": [surname_of(a) for a in authors],
            "journal": d.get("journal", ""),
            "year": d.get("year", ""),
            "title": d.get("title", ""),
        }
    return lib


def target_files():
    """Every .py and .md in the repo except caches, backups and this script."""
    skip_parts = {"__pycache__", ".git", "fulltext", "abstracts", "node_modules"}
    for ext in ("*.py", "*.md"):
        for p in ROOT.rglob(ext):
            if any(s in p.parts for s in skip_parts):
                continue
            if p.name == Path(__file__).name:
                continue
            if ".bak" in p.name:
                continue
            yield p


def is_correction_prose(window_text):
    low = window_text.lower()
    return any(m.lower() in low for m in CORRECTION_MARKERS)


def normalise(s):
    """Fold to bare lowercase ASCII letters.

    Two things have to happen before comparison or the gate reports false
    mismatches on names it has spelled perfectly well:

      * HTML entities. The library stores PubMed's accented names as escaped
        entities ("Abr&#xe0;moff", "Stenstr&#xf6;m"), while the builders
        write the ASCII-folded form ("Abramoff", "Stenstrom"). Unescaped,
        every accented author looked like a mismatch.
      * Diacritics. "Martinez-Gonzalez" and "Martínez-González" are
        the same person, and so are "Salas-Salvado" and "Salas-Salvadó".
    """
    s = html.unescape(str(s))
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z]", "", s.lower())


def audit(scan_html=False, resolve_unknown=False):
    lib = load_library()
    flagged, unknown, ok, excluded = [], [], [], []
    anchor_recs = []

    for path in target_files():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if "et al" not in text:
            continue
        lines = text.splitlines()
        offsets, running = [], 0
        for ln in lines:
            offsets.append(running)
            running += len(ln) + 1

        def line_of(pos):
            lo, hi = 0, len(offsets) - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if offsets[mid] <= pos:
                    lo = mid
                else:
                    hi = mid - 1
            return lo + 1

        for m in SURNAME_RE.finditer(text):
            surname = m.group(1)
            if surname in NOT_A_SURNAME:
                continue
            # Slash-joined run: the FIRST element is the first author.
            surname = surname.split("/")[0]
            if surname in NOT_A_SURNAME:
                continue

            # --- BACKWARD pairing first (see PAIRING RULE at top) ---
            # This repo also writes the PMID BEFORE the name:
            #     [PMID:38055252 - Waibel et al., NEJM 2023]
            #     PMID:18397984 (Yin et al 2008)
            # When a PMID sits immediately behind the surname with nothing
            # between them, it is that surname's PMID, and scanning forward
            # would wrongly bind the surname to the NEXT citation's PMID.
            pmid = None
            back_lo = max(0, m.start() - BACK_WINDOW)
            back = text[back_lo:m.start()]
            bm = None
            for cand in PMID_RE.finditer(back):
                bm = cand  # keep the last (nearest) one
            if bm:
                between_b = back[bm.end():]
                # FALSE-POSITIVE CLASS 5, found 2026-09-16. The shift-by-one
                # problem the PAIRING RULE describes also occurs in COMMA form:
                #     "(PMID 41921761, Qin et al. 2012, Karlsson et al. 2013)"
                # Here one PMID is followed by a list of OTHER sources cited by
                # author-year with no identifier of their own. Backward pairing
                # bound "Qin" to 41921761 (which is Nee et al.) and reported a
                # mismatch on a perfectly correct sentence. A comma between the
                # identifier and the surname means they are list SIBLINGS, not
                # a pair. The documented legitimate backward forms - "[PMID:N -
                # Waibel et al., NEJM 2023]" and "PMID:N (Yin et al 2008)" -
                # carry no comma BEFORE the surname, so this costs no reach.
                if not re.search(r"\bet\s+al\b", between_b) \
                        and not SEPARATOR_RE.search(between_b) \
                        and "," not in between_b:
                    pmid = bm.group(1)

            # --- else FORWARD pairing ---
            fwd_lo = m.end()
            if pmid is None:
                fwd_hi = min(len(text), m.end() + WINDOW)
                forward = text[fwd_lo:fwd_hi]
                pm = PMID_RE.search(forward)
                if not pm:
                    continue  # surname with no PMID either side: nothing to check
                between = forward[: pm.start()]
                # Another "et al." got there first -> that PMID is not ours.
                if re.search(r"\bet\s+al\b", between):
                    continue
                # A citation separator intervened -> that PMID is not ours.
                if SEPARATOR_RE.search(between):
                    continue
                pmid = pm.group(1)

            lo = max(0, m.start() - 120)
            hi = min(len(text), m.end() + WINDOW)
            window = text[lo:hi]
            lineno = line_of(m.start())
            rec = {
                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "line": lineno,
                "asserted_surname": surname,
                "pmid": pmid,
                "context": " ".join(window.split())[:220],
            }
            if is_correction_prose(window):
                excluded.append(rec)
                continue
            entry = lib.get(pmid)
            # FALSE-POSITIVE CLASS 6, found 2026-09-16. A library record can be
            # CORRUPT rather than absent: PMID 41986815 stored authors[0] as
            # "B", so a correct "Blencowe et al." was reported as a mismatch
            # against "B et al.". A one- or two-character first author is not a
            # surname; it is a broken record. Treat it as NO ground truth
            # (UNKNOWN, resolvable against NCBI) rather than as evidence of a
            # defect. The gate must never assert a mismatch on the strength of
            # a field it can see is malformed.
            #
            # 2026-09-23 CORRECTION TO THE ABOVE. The '< 3 letters' test was
            # itself a defect: it quarantined four CORRECT citations whose
            # first authors really do have two-letter surnames (So M, PMID
            # 42627334 x3; Li X, PMID 32307525; both confirmed on esummary
            # 2026-09-23), and would have hidden any WRONG two-letter-surname
            # citation the same way. The 'B' record is now fixed at source
            # and author_list() coerces the str-typed schema that caused it,
            # so malformed now means only: fewer than two letters survive.
            if entry and len(re.sub(r"[^A-Za-z]", "", entry["surname"])) < 2:
                entry = None
                rec["library_record_malformed"] = True
            if not entry:
                rec.setdefault("reason", "pmid not in local paper library")
                unknown.append(rec)
                continue
            rec["library_first_author"] = entry["surname"]
            rec["library_journal"] = entry["journal"]
            rec["library_year"] = entry["year"]
            if normalise(surname) in surname_variants(entry["surname"]):
                ok.append(rec)
            elif any(normalise(surname) in surname_variants(s)
                     for s in entry["all_surnames"]):
                # Named author is on the paper but is not first author.
                # "X et al." conventionally means X is first author, so this is
                # reported but held at a lower severity than a stranger.
                rec["severity"] = "NON_FIRST_AUTHOR"
                flagged.append(rec)
            else:
                rec["severity"] = "NOT_AN_AUTHOR"
                flagged.append(rec)

    # ---- HTML anchor pass (GAP 1) -----------------------------------------
    if scan_html:
        html_roots = [ROOT / "docs", ROOT / "Dashboards"]
        seen_anchor = set()
        for root in html_roots:
            if not root.is_dir():
                continue
            for hp in sorted(root.rglob("*.html")):
                try:
                    htext = hp.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue
                if "PMID" not in htext:
                    continue
                label = str(hp.relative_to(ROOT)).replace("\\", "/")
                for surname, pmid, ctx in scan_html_anchors(htext, label, lib):
                    key = (surname, pmid)
                    rec = {
                        "file": label,
                        "line": htext[:htext.find(ctx[:60])].count("\n") + 1
                                if ctx[:60] in htext else 0,
                        "asserted_surname": surname,
                        "pmid": pmid,
                        "context": ctx,
                        "source_kind": "html_anchor",
                    }
                    anchor_recs.append(rec)
                    seen_anchor.add(key)

        for rec in anchor_recs:
            entry = lib.get(rec["pmid"])
            if entry and len(re.sub(r"[^A-Za-z]", "", entry["surname"])) < 2:  # 2026-09-23: was < 3; see correction note above
                entry = None
                rec["library_record_malformed"] = True
            if not entry:
                rec["reason"] = "pmid not in local paper library"
                unknown.append(rec)
                continue
            rec["library_first_author"] = entry["surname"]
            rec["library_journal"] = entry["journal"]
            rec["library_year"] = entry["year"]
            if normalise(rec["asserted_surname"]) in surname_variants(entry["surname"]):
                ok.append(rec)
            elif any(normalise(rec["asserted_surname"]) in surname_variants(x)
                     for x in entry["all_surnames"]):
                rec["severity"] = "NON_FIRST_AUTHOR"
                flagged.append(rec)
            else:
                rec["severity"] = "NOT_AN_AUTHOR"
                flagged.append(rec)

    # ---- resolve the UNKNOWN bucket against NCBI (GAP 2) -------------------
    resolved_counts = {"attempted": 0, "resolved": 0, "still_unknown": 0}
    if resolve_unknown and unknown:
        cache = load_resolve_cache()
        want = [r["pmid"] for r in unknown]
        resolved_counts["attempted"] = len(unknown)
        resolved_counts["distinct_pmids"] = len(set(want))
        cache = resolve_pmids(want, cache)
        save_resolve_cache(cache)
        still = []
        for rec in unknown:
            entry = cache.get(rec["pmid"])
            if not entry:
                resolved_counts["still_unknown"] += 1
                still.append(rec)
                continue
            resolved_counts["resolved"] += 1
            rec["library_first_author"] = entry["surname"]
            rec["library_journal"] = entry["journal"]
            rec["library_year"] = entry["year"]
            rec["resolved_via"] = "ncbi_esummary"
            if normalise(rec["asserted_surname"]) in surname_variants(entry["surname"]):
                ok.append(rec)
            elif any(normalise(rec["asserted_surname"]) in surname_variants(x)
                     for x in entry["all_surnames"]):
                rec["severity"] = "NON_FIRST_AUTHOR"
                flagged.append(rec)
            else:
                rec["severity"] = "NOT_AN_AUTHOR"
                flagged.append(rec)
        unknown = still

    return {
        "generated": "2026-09-16",
        "html_anchor_scan": bool(scan_html),
        "html_anchor_attributions": len(anchor_recs),
        "unknown_resolution": resolved_counts,
        "window_chars": WINDOW,
        "library_pmids_with_authors": len(lib),
        "counts": {
            "matched_ok": len(ok),
            "flagged": len(flagged),
            "unknown_pmid": len(unknown),
            "excluded_as_correction_prose": len(excluded),
        },
        "flagged": sorted(flagged, key=lambda r: (r.get("severity", ""), r["file"], r["line"])),
        "unknown": sorted(unknown, key=lambda r: (r["file"], r["line"])),
        "excluded": sorted(excluded, key=lambda r: (r["file"], r["line"])),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true",
                    help="exit 1 if live mismatches exist")
    ap.add_argument("--measure", action="store_true", help="report only (default)")
    ap.add_argument("--html", action="store_true",
                    help="also scan generated .html for <a> citations whose "
                         "PMID sits in an attribute (onclick/data-/href)")
    ap.add_argument("--resolve-unknown", action="store_true",
                    help="look PMIDs absent from the local library up against "
                         "NCBI esummary (cached); opt-in so the default run "
                         "stays offline")
    args = ap.parse_args()

    res = audit(scan_html=args.html, resolve_unknown=args.resolve_unknown)

    # ------------------------------------------------------------------
    # SURFACE SPLIT, added 2026-09-18.
    #
    # On 2026-09-18 the gate's two LIVE hits were repaired and the four that
    # remained were all in FROZEN ARCHIVE: dated ACTION_REQUIRED_*.md and
    # iterate_run_report_*.md files, and a _close_run_*.py, in which the
    # "mismatch" is this repository quoting a defect it had just fixed. One of
    # them is literally a fenced HTML block showing the bad anchor.
    #
    # Those files are history and MUST NOT be rewritten - editing a dated run
    # report to make a gate go green is the failure this repo audits for.
    # But left in the MISMATCH bucket they guarantee the count never reaches
    # zero, and a gate that can never go green is a gate that gets ignored.
    #
    # The fix is a SPLIT, not an exclusion. Every finding is still printed and
    # still written to the JSON. Only the headline MISMATCH count - and the
    # --gate exit code - are scoped to the live publishing surface. This
    # deliberately avoids adding loose strings to CORRECTION_MARKERS, which
    # the note at the top of that tuple warns against: a marker silences a
    # class of finding everywhere, a surface split silences nothing.
    # ------------------------------------------------------------------
    ARCHIVE_PAT = re.compile(
        r"(ACTION_REQUIRED_\d{4}-\d{2}-\d{2}\.md"
        r"|iterate_run_report_\d{4}-\d{2}-\d{2}\.md"
        r"|DECISION_BRIEF_\d{4}-\d{2}-\d{2}\.md"
        r"|Platform_Audit_\d{4}-\d{2}-\d{2}\.md"
        r"|/_close_run_|/_run_|\\\\_close_run_|\\\\_run_"
        r"|^_close_run_|^_run_)"
    )

    def _is_archival(path_str):
        name = str(path_str).replace("\\", "/")
        return bool(ARCHIVE_PAT.search(name) or
                    ARCHIVE_PAT.search(name.rsplit("/", 1)[-1]))

    all_flagged = res.get("flagged", [])
    archival = [r for r in all_flagged if _is_archival(r["file"])]
    live = [r for r in all_flagged if not _is_archival(r["file"])]
    for r in archival:
        r["surface"] = "ARCHIVAL"
    for r in live:
        r["surface"] = "LIVE"

    res["flagged"] = live
    res["flagged_archival"] = archival
    res["counts"]["flagged"] = len(live)
    res["counts"]["flagged_archival"] = len(archival)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")

    c = res["counts"]
    print("=" * 62)
    print("  PROSE AUTHOR SURNAME AUDIT")
    print("=" * 62)
    print(f"  library PMIDs carrying an authors[] array : {res['library_pmids_with_authors']}")
    print(f"  surname+PMID attributions checked         : {c['matched_ok'] + c['flagged']}")
    print(f"    matched first author                    : {c['matched_ok']}")
    print(f"    MISMATCH (live publishing surface)      : {c['flagged']}")
    print(f"    in frozen archive (reported, not fixed) : "
          f"{c['flagged_archival']}")
    print(f"  not checkable (PMID not in library)       : {c['unknown_pmid']}")
    print(f"  excluded as this repo's correction prose  : {c['excluded_as_correction_prose']}")
    if res.get("html_anchor_scan"):
        print(f"  html <a> citations scanned (markup reach)  : {res['html_anchor_attributions']}")
    ur = res.get("unknown_resolution") or {}
    if ur.get("attempted"):
        print(f"  unknown PMIDs resolved via NCBI            : "
              f"{ur['resolved']} of {ur['attempted']} "
              f"({ur['still_unknown']} unresolvable)")
    print()

    if res["flagged"]:
        print("  MISMATCHES - LIVE")
        print("  " + "-" * 58)
        for r in res["flagged"]:
            print(f"  [{r.get('severity')}] {r['file']}:{r['line']}")
            print(f"      asserts : {r['asserted_surname']} et al.  (PMID {r['pmid']})")
            print(f"      library : {r['library_first_author']} et al., "
                  f"{r['library_journal']} {r['library_year']}")
            print()

    if res.get("flagged_archival"):
        print("  IN FROZEN ARCHIVE - reported for the record, NOT to be edited")
        print("  (a dated run report is history; rewriting one to clear a gate")
        print("   is the exact failure this repository audits for)")
        print("  " + "-" * 58)
        for r in res["flagged_archival"]:
            print(f"  [{r.get('severity')}] {r['file']}:{r['line']}")
            print(f"      asserts : {r['asserted_surname']} et al.  (PMID {r['pmid']})")
            print(f"      library : {r['library_first_author']} et al., "
                  f"{r['library_journal']} {r['library_year']}")
            print()

    print(f"  Output: {OUT}")
    if args.gate and res["flagged"]:
        print("  [FAIL] live author-surname mismatches present")
        return 1
    print("  [OK]" if not res["flagged"] else "  [MEASURE] reporting only; not gating")
    return 0


if __name__ == "__main__":
    sys.exit(main())
