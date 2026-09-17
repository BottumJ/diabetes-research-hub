#!/usr/bin/env python3
"""
audit_trial_phase.py
====================
Added 2026-09-17.

WHAT THIS CHECKS
----------------
Whether a "Phase N" label asserted next to a PMID agrees with what PubMed
says that paper is.

WHY IT EXISTS
-------------
On 2026-09-16 `build_immunomod_lada.py` was found labelling PMID 29291885
as "Herold et al., Teplizumab Phase 3 (TN-10)". Three independent errors in
six words:

  * PMID 29291885 is Zanelli & Rogol, growth hormone in short children.
  * The real TN-10 paper is 31180194.
  * TN-10 is PHASE 2, n=76. PubMed publication type reads
    "Clinical Trial, Phase II" and the abstract's METHODS opens
    "We conducted a phase 2, randomized, placebo-controlled, double-blind
    trial."

The surname gate built on 2026-09-15 catches the first two. NOTHING in this
repository catches the third. That matters more than a wrong surname to a
reader weighing a result: Phase 3 implies registrational evidence, a
pre-specified primary endpoint and a regulatory audience. Phase 2 does not.
Phase inflation borrows authority the paper does not have.

THE PAIRING RULE -- AND WHY IT IS NOT THE SURNAME GATE'S RULE
-------------------------------------------------------------
The surname gate pairs by scanning FORWARD from the name to the next PMID,
because a citation reads "<Surname> et al. <Journal> <Year> (PMID:N)" and
the name always precedes its identifier. A phase label has no such fixed
position. It is written on both sides:

    "PMID 31180194 - Herold et al., teplizumab Phase 2 (TN-10)"
    "the Phase 3 ONWARDS programme [PMID:37354562, JAMA, 2023]"

A directional rule would therefore have to reach both ways, and a
bidirectional window is exactly what produced the shift-by-one chain of
fake mismatches the surname gate's PAIRING RULE exists to forbid.

So this gate does not use a window at all. It splits the text into CITATION
UNITS on the separators that end a citation in this repository, and asks
whether a phase label and a PMID are inside the SAME unit. Containment is
symmetric, so it needs no direction, and a unit holding two PMIDs is
reported AMBIGUOUS rather than guessed at.

THE UNKNOWN BUCKET IS RESOLVED, NOT EXCUSED
-------------------------------------------
`esummary` carries phase verbatim in `pubtype` ("Clinical Trial, Phase II")
but only for papers PubMed has indexed that way -- which is roughly the
registrational trials and not much else. A paper whose phase is stated only
in its abstract has no phase pubtype at all.

Leaving those UNKNOWN would repeat the 2026-09-16 finding that "unknown"
was not a neutral bucket but a hiding place selected for risk. So
--resolve-unknown fetches the ABSTRACT via efetch and reads the phase out
of the sentence that states it, and the record says which of the two
sources answered. Both are cached on disk.

WHAT IS DELIBERATELY NOT FLAGGED
--------------------------------
  * Seamless designs. "Phase 1/2" and "Phase 2/3" are real designs, and a
    paper indexed "Clinical Trial, Phase II" may legitimately be described
    as "Phase 1/2". An asserted RANGE that contains the true phase is
    CONSISTENT, not a mismatch.
  * This repository's own correction prose. A sentence explaining that a
    "Phase 3" label was withdrawn contains both a phase and a PMID and is
    CORRECT prose about an incorrect citation. Counting it is the inflation
    that made the 29710129 estimate wrong by 8x (work_queue 2026-09-14).
  * Phase 4 / post-marketing, which this repo asserts only from registry
    records, not from papers.
  * "Phase N" meaning a stage of THIS PROJECT's own workflow. This repo
    writes "Phase 2 constructed a feature-engineered multi-omic dataset" and
    "Phase 3 trained and evaluated 5 classifiers" in its microbiome pipeline
    reports, with corpus PMIDs in the same sentence. Those are not trial
    phases at all. See FALSE-POSITIVE CLASS 4.
  * A phase label bound to an NCT id rather than a PMID. Registry phase is
    already covered by the NCT gate added 2026-09-02. This is enforced
    MECHANICALLY, not just stated: see NCT_BINDS_CLOSER below.

THE FIRST MEASUREMENT'S JOB IS TO FIND THE GATE'S DEFECTS, NOT THE REPO'S
------------------------------------------------------------------------
Measured 2026-09-17 before wiring anything in, per standing instruction.
The first run reported 5 mismatches. ALL FIVE WERE GATE DEFECTS. They are
recorded here because the next person to extend this file will otherwise
reintroduce them.

FALSE-POSITIVE CLASS 1 -- THE RESOLVER READ THE PAPER'S BIBLIOGRAPHY.
  efetch returns the whole <PubmedArticle>, which includes <ReferenceList>.
  Stripping tags and scanning the blob read phases out of the cited works:
  PMID 42108533 (a review) was assigned "phase 2" from its own reference
  "...retatrutide for obesity - a phase 2 trial. N Engl J Med. 2023", and
  PMID 40896829 was assigned "phase 1" from a reference to PMID 33610858.
  A resolver that reads a phase out of a bibliography assigns essentially an
  arbitrary phase, and every comparison downstream is noise. The abstract
  scan is now confined to <ArticleTitle> and <Abstract> and nothing else.

FALSE-POSITIVE CLASS 2 -- THE PAPER HAS NO PHASE OF ITS OWN.
  A Review, Comment, Editorial, Letter or News item describes other people's
  trials; a preclinical animal study has no phase at all. PMID 41984238 is a
  Letter critiquing orforglipron's statistics and PMID 42034968 is a mouse
  study of "experimental autoimmune type 1 diabetes". Neither has a phase,
  so neither can contradict one. A phase is now inferred from an abstract
  ONLY when pubtype shows the paper is itself a trial report.

FALSE-POSITIVE CLASS 4 -- "PHASE N" WAS A STAGE OF THIS PROJECT, NOT A TRIAL.
  "Phase 2 constructed a feature-engineered multi-omic dataset of 1,200
  synthetic samples" is a sentence about the repository's own ML pipeline
  that happens to sit near a corpus PMID. The tell is grammatical and needs
  no lookup: a trial phase is a NOUN MODIFIER -- it is followed by a trial
  word ("phase 2 trial", "phase 3 RCT", "Phase 3 (TN-10)") or attached to a
  drug name. A project stage is a SUBJECT -- it is followed by a past-tense
  verb. Requiring a trial word near the label is the cheaper half of that
  test and is what is implemented.

FALSE-POSITIVE CLASS 3 -- THE PHASE BELONGED TO THE NCT, NOT THE PMID.
  "NCT05971940 - Orforglipron in T2D, Phase 3 - results posted 2026-04-22.
  Pair with the new pharmacokinetic bioequivalence paper (PMID 41994902)"
  is a correct sentence. The registry record is phase 3; the PMID is a
  phase 1 bioequivalence study; the citation unit contains both. Where an
  NCT id sits closer to the phase label than the PMID does, the phase is the
  registry's and this gate has nothing to say about it.

EXIT CODE
---------
0 always in --measure mode (reporting only).
1 when run as --gate and live mismatches exist.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "Analysis" / "Results" / "trial_phase_audit.json"
PHASE_CACHE = ROOT / "Analysis" / "Results" / ".trial_phase_cache.json"

PMID_RE = re.compile(r"PMID[:\s#]*(\d{6,9})", re.IGNORECASE)
NCT_RE = re.compile(r"\bNCT\d{8}\b", re.IGNORECASE)

# FALSE-POSITIVE CLASS 4. A trial phase is a noun modifier: a trial word sits
# near it. A project stage is a subject: "Phase 2 constructed...".
TRIAL_WORD_RE = re.compile(
    r"\b(trial|trials|study|studies|RCT|randomi[sz]ed|programme|program|"
    r"cohort|arm|open-label|double-blind|placebo|efficacy|enrol|enroll|"
    r"topline|readout|pivotal|registrational|completed|recruiting|"
    r"data|results|remission|monotherapy|add-on)\b", re.IGNORECASE)
TRIAL_WORD_REACH = 60  # characters either side of the phase label

# A phase assertion. Arabic, Roman, and the two seamless forms this repo uses.
# Ordered so the seamless forms match before their bare prefixes.
PHASE_RE = re.compile(
    r"\bphase[\s‑_-]*"
    r"(I/II|II/III|1/2|2/3|III|II|IV|I|1|2|3|4)\b",
    re.IGNORECASE)

# What ends a citation in this repository. Same set as the surname gate, plus
# the bracket forms this repo uses to delimit a reference: "[PMID:N, ...]".
SEPARATOR_RE = re.compile(r"[;\n•\[\]]|</|\|\|")

# Reused verbatim from audit_prose_author_surnames.py. See the note there on
# why "not a defect" is deliberately absent: that phrase is how PMID 37359825
# was laundered into agent_state.json as verified while carrying a false
# surname. A gate must not be silenced by an assertion that there is nothing
# to see.
CORRECTION_MARKERS = (
    "withdrawn", "withdrew", "withdrawal",
    "removed", "removal",
    "mis-attributed", "misattributed", "misattribution",
    "previously cited", "previously attributed", "previously given",
    "unsourced",
    "corrected 2026-", "corrected 2025-",
    "incorrectly", "wrongly", "false attribution",
    "not in fact", "is actually", "it is actually",
    "this block cited", "still reads", "still reading",
    "retracted", "exemplar", "was cited", "had cited",
    "was labelled", "was labeled", "were jointly labelled",
    "re-pointed", "repointed", "the intended paper is",
    "this row read", "this entry read", "why each is wrong",
    "none was correct", "wrong author", "wrong journal", "wrong subject",
    "surname corrected", "is not an author",
    "hid there", "inherited the surname",
    # ADDED 2026-09-17, harvested from real flags in this run's first
    # measurement that were the repository correctly describing a bad label.
    "phase inflation", "phase 3 -> phase 2", "phase 3 to phase 2",
    "transposed", "not a source", "being published as",
    "over-prioritised", "over-prioritized", "trap avoided",
)

# Asserted label -> the set of true phases it is consistent with.
PHASE_SETS = {
    "1": {1}, "i": {1},
    "2": {2}, "ii": {2},
    "3": {3}, "iii": {3},
    "4": {4}, "iv": {4},
    "1/2": {1, 2}, "i/ii": {1, 2},
    "2/3": {2, 3}, "ii/iii": {2, 3},
}

# esummary pubtype strings -> phase integer.
PUBTYPE_PHASE = {
    "clinical trial, phase i": 1,
    "clinical trial, phase ii": 2,
    "clinical trial, phase iii": 3,
    "clinical trial, phase iv": 4,
}

# Publication types that mean the paper reports a trial of its own, and so
# may legitimately have a phase read out of its abstract. FALSE-POSITIVE
# CLASS 2: without this, a Letter or a mouse study is assigned the phase of
# whatever trial its abstract happens to discuss.
TRIAL_PUBTYPES = {
    "clinical trial", "randomized controlled trial",
    "controlled clinical trial", "clinical trial, phase i",
    "clinical trial, phase ii", "clinical trial, phase iii",
    "clinical trial, phase iv", "pragmatic clinical trial",
    "equivalence trial", "adaptive clinical trial",
}
# Publication types that mean the paper is ABOUT other people's trials and
# therefore has no phase of its own, whatever its abstract says.
NON_TRIAL_PUBTYPES = {
    "review", "systematic review", "meta-analysis", "comment", "editorial",
    "letter", "news", "published erratum", "historical article",
    "practice guideline", "guideline",
}

# How a paper states its own phase in an abstract. Deliberately narrow: it
# must be a claim about THIS trial's design, not a mention of some other
# trial's phase in a background sentence.
ABSTRACT_PHASE_RE = re.compile(
    r"(?:we\s+(?:conducted|report|performed|undertook)|"
    r"this\s+(?:was|is)|in\s+this|"
    r"a\s+(?:multicent(?:er|re)\s+)?(?:randomi[sz]ed,?\s+)?"
    r"(?:double-blind,?\s+)?(?:placebo-controlled,?\s+)?)"
    r"[^.]{0,80}?\bphase[\s‑-]*"
    r"(I/II|II/III|1/2|2/3|III|II|IV|I|1|2|3|4)\b",
    re.IGNORECASE)


def norm_label(tok):
    return tok.replace("‑", "/").lower()


def load_cache():
    try:
        return json.loads(PHASE_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_cache(cache):
    PHASE_CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True),
                           encoding="utf-8")


def resolve_pubtypes(pmids, cache):
    """pmid -> {'phase': int|None, 'pubtype': [...], 'title':..., 'source':...}

    Never raises. A network failure leaves the PMID unresolved, which keeps
    it in the UNKNOWN bucket -- reported, not flagged.
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
        except Exception as exc:
            print(f"  [warn] esummary failed ({type(exc).__name__}); "
                  f"{len(chunk)} PMIDs stay UNKNOWN")
            break
        for uid in res.get("uids", []):
            r = res.get(uid, {})
            pubtypes = [str(p) for p in (r.get("pubtype") or [])]
            phase = None
            for pt in pubtypes:
                if pt.strip().lower() in PUBTYPE_PHASE:
                    phase = PUBTYPE_PHASE[pt.strip().lower()]
                    break
            cache[uid] = {
                "phase": phase,
                "phase_source": "pubtype" if phase else None,
                "pubtype": pubtypes,
                "title": r.get("title", ""),
                "journal": r.get("source", ""),
                "year": (r.get("pubdate") or "")[:4],
            }
        for uid in chunk:
            cache.setdefault(uid, None)
    return cache


def resolve_from_abstracts(pmids, cache):
    """Second pass for PMIDs esummary gave no phase pubtype for.

    Reads the phase out of the abstract's own design sentence. Records the
    sentence, so a later reader can check the gate's reading rather than
    taking its word -- which is the whole lesson of 2026-09-16.
    """
    import urllib.request
    def eligible(p):
        """A phase may be read from an abstract only when the paper is itself
        a trial report. FALSE-POSITIVE CLASS 2 -- see module docstring."""
        e = cache.get(p)
        if not isinstance(e, dict) or e.get("phase") is not None:
            return False
        if "abstract_checked" in e:
            return False
        pts = {str(x).strip().lower() for x in (e.get("pubtype") or [])}
        if pts & NON_TRIAL_PUBTYPES:
            e["phase_source"] = "not_applicable_non_trial"
            e["abstract_checked"] = True
            return False
        if not (pts & TRIAL_PUBTYPES):
            e["phase_source"] = "not_applicable_no_trial_pubtype"
            e["abstract_checked"] = True
            return False
        return True

    todo = [p for p in sorted(set(pmids)) if eligible(p)]
    for i in range(0, len(todo), 50):
        chunk = todo[i:i + 50]
        url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
               "?db=pubmed&retmode=xml&rettype=abstract&id=" + ",".join(chunk))
        try:
            with urllib.request.urlopen(url, timeout=60) as fh:
                xml = fh.read().decode("utf-8", "replace")
        except Exception as exc:
            print(f"  [warn] efetch failed ({type(exc).__name__}); "
                  f"{len(chunk)} PMIDs stay UNKNOWN")
            break
        # Split per article so a phase read from one abstract cannot be
        # attributed to its neighbour.
        for art in re.split(r"(?=<PubmedArticle>)", xml):
            pm = re.search(r"<PMID[^>]*>(\d+)</PMID>", art)
            if not pm or pm.group(1) not in cache:
                continue
            uid = pm.group(1)
            if not isinstance(cache[uid], dict):
                continue
            # FALSE-POSITIVE CLASS 1. Read ONLY the title and the abstract.
            # <ReferenceList> carries other papers' phases and reading it
            # assigns this paper an arbitrary one.
            art = re.sub(r"<ReferenceList\b.*?</ReferenceList>", " ", art,
                         flags=re.DOTALL | re.IGNORECASE)
            parts = re.findall(
                r"<(?:ArticleTitle|AbstractText)\b[^>]*>(.*?)"
                r"</(?:ArticleTitle|AbstractText)>",
                art, flags=re.DOTALL | re.IGNORECASE)
            text = " ".join(" ".join(re.sub(r"<[^>]+>", " ", p).split())
                            for p in parts)
            cache[uid]["abstract_checked"] = True
            am = ABSTRACT_PHASE_RE.search(text)
            if am:
                ph = PHASE_SETS.get(norm_label(am.group(1)))
                if ph and len(ph) == 1:
                    cache[uid]["phase"] = next(iter(ph))
                    cache[uid]["phase_source"] = "abstract"
                elif ph:
                    cache[uid]["phase_set"] = sorted(ph)
                    cache[uid]["phase_source"] = "abstract_seamless"
                cache[uid]["abstract_evidence"] = \
                    text[max(0, am.start() - 40):am.end() + 40]
        for uid in chunk:
            if isinstance(cache.get(uid), dict):
                cache[uid].setdefault("abstract_checked", True)
    return cache


def target_files():
    skip_parts = {"__pycache__", ".git", "fulltext", "abstracts",
                  "node_modules"}
    for ext in ("*.py", "*.md"):
        for p in ROOT.rglob(ext):
            if any(s in p.parts for s in skip_parts):
                continue
            if p.name == Path(__file__).name:
                continue
            if ".bak" in p.name:
                continue
            yield p


def is_correction_prose(text):
    low = text.lower()
    return any(m in low for m in CORRECTION_MARKERS)


def citation_units(text):
    """Yield (start_offset, unit_text). A unit is the span between two
    citation separators -- the scope inside which a phase label and an
    identifier belong to each other."""
    pos = 0
    for m in SEPARATOR_RE.finditer(text):
        if m.start() > pos:
            yield pos, text[pos:m.start()]
        pos = m.end()
    if pos < len(text):
        yield pos, text[pos:]


def collect(scan_html=False):
    """First pass: every (phase label, PMID) pair the repo asserts."""
    pairs, ambiguous, excluded = [], [], []
    roots = [target_files()]
    if scan_html:
        roots.append(
            p for d in ("Dashboards", "docs")
            for p in sorted((ROOT / d).rglob("*.html")))

    for src in roots:
        for path in src:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if "phase" not in text.lower() or "PMID" not in text.upper():
                continue

            offsets, running = [], 0
            for ln in text.splitlines():
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

            for start, unit in citation_units(text):
                phases = [
                    m for m in PHASE_RE.finditer(unit)
                    if TRIAL_WORD_RE.search(
                        unit[max(0, m.start() - TRIAL_WORD_REACH):
                             m.end() + TRIAL_WORD_REACH])]
                if not phases:
                    continue
                pmids = list(PMID_RE.finditer(unit))
                if not pmids:
                    continue
                rec_base = {
                    "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "line": line_of(start + phases[0].start()),
                    "context": " ".join(unit.split())[:240],
                }
                if is_correction_prose(unit):
                    excluded.append(dict(rec_base,
                                         reason="repository correction prose"))
                    continue
                distinct = sorted({m.group(1) for m in pmids})
                if len(distinct) > 1:
                    ambiguous.append(dict(
                        rec_base, pmids=distinct,
                        asserted=[m.group(1) for m in phases],
                        reason="more than one PMID in the citation unit; "
                               "which one the phase label belongs to is not "
                               "decidable without judgement"))
                    continue
                # FALSE-POSITIVE CLASS 3. If a registry id sits closer to the
                # phase label than the PMID does, the phase is the registry
                # record's, and the NCT gate (2026-09-02) owns it.
                nct_closer = False
                for pm_ in phases:
                    d_pmid = min(abs(pm_.start() - x.start()) for x in pmids)
                    ncts = list(NCT_RE.finditer(unit))
                    if ncts and min(abs(pm_.start() - x.start())
                                    for x in ncts) < d_pmid:
                        nct_closer = True
                        break
                if nct_closer:
                    excluded.append(dict(
                        rec_base, pmid=distinct[0],
                        reason="phase label binds to an NCT id, not to the "
                               "PMID; registry phase is the NCT gate's scope"))
                    continue

                labels = sorted({norm_label(m.group(1)) for m in phases})
                if len(labels) > 1:
                    ambiguous.append(dict(
                        rec_base, pmids=distinct, asserted=labels,
                        reason="more than one distinct phase label in the "
                               "citation unit"))
                    continue
                pairs.append(dict(rec_base, pmid=distinct[0],
                                  asserted_phase=labels[0]))
    return pairs, ambiguous, excluded


def audit(scan_html=False, resolve_unknown=False):
    pairs, ambiguous, excluded = collect(scan_html=scan_html)
    cache = load_cache()
    if resolve_unknown and pairs:
        cache = resolve_pubtypes([p["pmid"] for p in pairs], cache)
        cache = resolve_from_abstracts([p["pmid"] for p in pairs], cache)
        save_cache(cache)

    flagged, ok, unknown = [], [], []
    for rec in pairs:
        entry = cache.get(rec["pmid"])
        if not isinstance(entry, dict):
            unknown.append(dict(rec, reason="PMID not resolved against NCBI "
                                            "(run with --resolve-unknown)"))
            continue
        rec["pubtype"] = entry.get("pubtype", [])
        rec["true_title"] = entry.get("title", "")[:110]
        true_phase = entry.get("phase")
        true_set = set(entry.get("phase_set") or
                       ([true_phase] if true_phase else []))
        if not true_set:
            unknown.append(dict(
                rec, reason="PubMed states no phase for this paper: no phase "
                            "publication type and no design sentence in the "
                            "abstract"))
            continue
        rec["true_phase"] = sorted(true_set)
        rec["phase_source"] = entry.get("phase_source")
        if entry.get("abstract_evidence"):
            rec["abstract_evidence"] = entry["abstract_evidence"][:260]
        asserted_set = PHASE_SETS.get(rec["asserted_phase"], set())
        if asserted_set & true_set:
            ok.append(rec)
        else:
            rec["verdict"] = "PHASE_MISMATCH"
            rec["direction"] = ("INFLATED"
                                if min(asserted_set or {0}) > max(true_set)
                                else "UNDERSTATED")
            flagged.append(rec)

    report = {
        "generated": "2026-09-17",
        "gate": "trial_phase",
        "counts": {
            "pairs_checked": len(pairs),
            "correct": len(ok),
            "flagged": len(flagged),
            "unknown": len(unknown),
            "ambiguous_not_checked": len(ambiguous),
            "excluded_correction_prose": len(excluded),
        },
        "flagged": flagged,
        "unknown": unknown,
        "ambiguous": ambiguous,
        "excluded": excluded[:40],
        "correct": [{k: r[k] for k in
                     ("file", "line", "pmid", "asserted_phase",
                      "true_phase", "phase_source") if k in r}
                    for r in ok],
    }
    OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", action="store_true",
                    help="report only; always exits 0 (default)")
    ap.add_argument("--gate", action="store_true",
                    help="exit 1 if live phase mismatches exist")
    ap.add_argument("--html", action="store_true",
                    help="also scan generated HTML under Dashboards/ and docs/")
    ap.add_argument("--resolve-unknown", action="store_true",
                    help="resolve phase against NCBI esummary pubtype, then "
                         "against the abstract's own design sentence (cached)")
    args = ap.parse_args()

    rep = audit(scan_html=args.html, resolve_unknown=args.resolve_unknown)
    c = rep["counts"]
    print("TRIAL PHASE AUDIT")
    print(f"  pairs checked      : {c['pairs_checked']}")
    print(f"  correct            : {c['correct']}")
    print(f"  FLAGGED            : {c['flagged']}")
    print(f"  unknown            : {c['unknown']}")
    print(f"  ambiguous (skipped): {c['ambiguous_not_checked']}")
    print(f"  correction prose   : {c['excluded_correction_prose']}")
    for r in rep["flagged"]:
        print(f"\n  [{r['direction']}] {r['file']}:{r['line']}")
        print(f"    asserts Phase {r['asserted_phase'].upper()} for "
              f"PMID {r['pmid']}; PubMed says phase "
              f"{r['true_phase']} (via {r['phase_source']})")
        print(f"    {r['true_title']}")
    print(f"\n  report: {OUT.relative_to(ROOT)}")
    if args.gate and rep["counts"]["flagged"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
