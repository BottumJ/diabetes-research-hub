#!/usr/bin/env python3
"""Two questions corpus_membership.py promised would be asked, and nobody asked.

corpus_membership.py has said since 2026-08-28, in its own source:

    UNCLASSIFIED = 'FLAGGED_UNCLASSIFIED'
    # A FLAGGED paper with no membership_class is a bug, not a default.

    def unclassified():
        '''FLAGGED papers with no membership_class. Should always be empty; an
        audit fails on this rather than letting a consumer guess a meaning.'''

That audit did not exist. Measured 2026-09-20: `unclassified()` had no caller
anywhere in Analysis/Scripts outside the module itself and one dated one-off.
So for 23 days the set was non-empty and nothing said so.

The second unasked question is worse, because the module answers it correctly
and nobody listens. `citable()` - "may this PMID appear in published prose?" -
also had ZERO call sites. The consequence was live and measurable: four PMIDs
for which corpus_membership answered citable() == False were cited in three
builder scripts and appeared on eight pages under docs/. A module that
declares a paper uncitable while the site cites it is not a gate, it is a
comment.

WHAT THIS AUDIT CHECKS
----------------------
  1. unclassified() is empty.
     A FLAGGED paper with no membership_class inherits whichever meaning the
     reading consumer assumes. On 2026-09-19 the meaning one consumer assumed
     was "delete it from the index", and the ledger cited the missing field
     itself as grounds.

  2. No uncitable PMID appears in live builder source or under docs/.
     This is the citable() call site the repo never had. It is the check that
     would have caught PMIDs 20570966 and 28397826 - the two miscitations in
     corpus_membership.py's own founding docstring - at the moment they were
     adjudicated, rather than leaving them on published pages.

WHY (2) IS SCOPED TO OFF_TOPIC/RETRACTED/PROVENANCE AND NOT TO BACKGROUND
-------------------------------------------------------------------------
Because BACKGROUND papers are SUPPOSED to be cited. PMID 18662538 (Massague,
TGF-beta) is the definitional source for a Data Dictionary entry. Failing on
it would train whoever runs this to ignore the audit, which is the only way a
gate dies faster than never being written.

THE TWO EXEMPTIONS, AND WHY THEY ARE STRUCTURAL RATHER THAN A FILENAME LIST
---------------------------------------------------------------------------
The first draft of check 2 failed on six PMIDs and every one was a false
positive. Both causes are the same shape: NAMING a rejected PMID is not
CITING it, and the repo names them on purpose in two places.

  (a) Python comments and docstrings. All three builder-source hits were
      repair notes - "Repaired 2026-08-28. This entry read PMID:20570966,
      which is ..." - i.e. the record of a withdrawal. Deleting those notes to
      satisfy a gate would destroy the only evidence that the repair happened.
      So the scan strips comments and string literals and reads CODE only.

  (b) The PMID verification dashboard. All six docs/ hits were in
      PMID_Verification.html, each in a row whose adjacent cell reads "NOT
      CORPUS" - that page is the rejection ledger and listing them is its job.
      This is matched by the marker beside the PMID, not by the filename, so
      the exemption survives a rename and does NOT extend to a page that
      merely happens to live in the same directory.

A gate whose first run is all false positives gets switched off. Both
exemptions were derived from reading every one of the six, not assumed.
"""

import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RESULTS = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Results'))
DOCS = os.path.join(ROOT, 'docs')
REPORT = os.path.join(RESULTS, 'flagged_membership_class_audit.json')

import corpus_membership  # noqa: E402

PMID_RE = re.compile(r'\b(\d{7,8})\b')

# Text that, appearing beside a PMID, means the page is REPORTING the PMID as
# rejected rather than sourcing a claim to it. See exemption (b) above.
REJECTION_MARKERS = ('NOT CORPUS', 'NOT_CORPUS', 'RETRACTED', 'Verify-',
                     'MISMATCH', 'WITHDRAWN', 'not a corpus paper')
MARKER_WINDOW = 400


def _strip_python_prose(text):
    """Return Python source with COMMENTS and DOCSTRINGS removed, nothing else.

    Exemption (a): a comment recording a withdrawn citation names the PMID and
    must keep naming it. tokenize is used rather than a regex because '#' and
    quotes appear inside each other constantly in this repo's builders.

    ORDINARY STRING LITERALS ARE DELIBERATELY KEPT. Every published citation in
    this repo lives inside an f-string of HTML, so stripping all STRING tokens
    would not make the audit lenient - it would make it vacuous, which is the
    more dangerous of the two failures because it still prints [OK].
    """
    import io
    import tokenize
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        # Unparseable source is audit_builders_compile.py's problem, not this
        # audit's. Fall back to the crude strip rather than skipping the file.
        return re.sub(r'#[^\n]*', '', text)
    out = []
    # A STRING that forms an entire statement is a docstring: prose, like a
    # comment. A STRING anywhere else is data being emitted.
    prev_significant = tokenize.NEWLINE
    for i, tok in enumerate(toks):
        if tok.type == tokenize.COMMENT:
            continue
        if tok.type == tokenize.STRING and prev_significant in (
                tokenize.NEWLINE, tokenize.NL, tokenize.INDENT,
                tokenize.DEDENT, tokenize.ENCODING):
            nxt = next((t for t in toks[i + 1:]
                        if t.type not in (tokenize.COMMENT,)), None)
            if nxt is not None and nxt.type in (tokenize.NEWLINE, tokenize.NL,
                                                tokenize.ENDMARKER):
                continue
        if tok.type not in (tokenize.COMMENT,):
            prev_significant = tok.type
        out.append(tok.string)
    return '\n'.join(out)


def _marker_near(text, idx):
    """Is a rejection marker within MARKER_WINDOW chars of this position?"""
    seg = text[max(0, idx - MARKER_WINDOW): idx + MARKER_WINDOW]
    return any(m in seg for m in REJECTION_MARKERS)


def _live_builder_sources():
    """Builder and rebuilder scripts. Dated one-offs (_run_*, _close_run_*)
    are excluded: they are a historical record of what a past run did and
    rewriting them would falsify it."""
    out = []
    for name in sorted(os.listdir(SCRIPT_DIR)):
        if not name.endswith('.py'):
            continue
        if name.startswith('_'):
            continue
        if not (name.startswith('build_') or name.startswith('rebuild_')):
            continue
        out.append(os.path.join(SCRIPT_DIR, name))
    return out


def _docs_files():
    out = []
    if not os.path.isdir(DOCS):
        return out
    for dirpath, _dirs, files in os.walk(DOCS):
        for f in files:
            if f.endswith(('.html', '.md')):
                out.append(os.path.join(dirpath, f))
    return out


def _scan(paths, targets, is_python=False):
    """Which target PMIDs are ASSERTED (not merely named) in which files.

    Returns {pmid: [relpath, ...]}. A hit is dropped when it sits beside a
    rejection marker, and Python prose is stripped first. See the two
    exemptions in the module docstring.
    """
    hits = {}
    for path in paths:
        try:
            with open(path, encoding='utf-8', errors='replace') as fh:
                text = fh.read()
        except OSError:
            continue
        if is_python:
            text = _strip_python_prose(text)
        for m in PMID_RE.finditer(text):
            pmid = m.group(1)
            if pmid not in targets:
                continue
            if _marker_near(text, m.start()):
                continue
            rel = os.path.relpath(path, ROOT)
            if rel not in hits.setdefault(pmid, []):
                hits[pmid].append(rel)
    return {k: v for k, v in hits.items() if v}


def main():
    corpus_membership.reload()

    failures = []
    report = {'checks': {}}

    # ---- CHECK 1 -------------------------------------------------------
    unclassified = sorted(corpus_membership.unclassified())
    report['checks']['unclassified_flagged'] = {
        'count': len(unclassified),
        'pmids': unclassified,
    }
    if unclassified:
        state_path = os.path.join(RESULTS, 'agent_state.json')
        titles = {}
        try:
            with open(state_path, encoding='utf-8') as fh:
                papers = json.load(fh).get('papers', {})
            titles = {p: (papers.get(p, {}).get('title') or '')
                      for p in unclassified}
        except (OSError, ValueError):
            pass
        failures.append(
            '%d FLAGGED paper(s) have no membership_class. Until one is '
            'recorded they are excluded from evidence AND from prose by '
            'default, which is a meaning nobody chose:' % len(unclassified))
        for p in unclassified:
            failures.append('    %s  %s' % (p, titles.get(p, '')[:70]))
        failures.append(
            '    Remedy: add each to an adjudicate_flagged_membership_*.py '
            'with one of CORPUS / BACKGROUND / OFF_TOPIC / RETRACTED / '
            'PROVENANCE. CORPUS is correct when the flag records a prose '
            'repair or a framing caveat rather than a defect in the paper.')

    # ---- CHECK 2 -------------------------------------------------------
    hard = set()
    for code in ('OFF_TOPIC', 'RETRACTED', 'PROVENANCE'):
        hard |= corpus_membership.excluded_by(code)

    src_hits = _scan(_live_builder_sources(), hard, is_python=True)
    doc_hits = _scan(_docs_files(), hard)

    report['checks']['uncitable_in_live_prose'] = {
        'uncitable_hard_count': len(hard),
        'in_builder_source': {k: sorted(v) for k, v in sorted(src_hits.items())},
        'in_docs': {k: sorted(v)[:6] for k, v in sorted(doc_hits.items())},
    }

    if src_hits or doc_hits:
        failures.append(
            '%d uncitable PMID(s) appear in live prose. corpus_membership '
            'answers citable() == False for each; the repo cites them anyway:'
            % len(set(src_hits) | set(doc_hits)))
        for pmid in sorted(set(src_hits) | set(doc_hits)):
            r = corpus_membership.reason(pmid) or {}
            failures.append('    %s  %-12s %s'
                            % (pmid, r.get('code', '?'),
                               (r.get('title') or r.get('why') or '')[:60]))
            if src_hits.get(pmid):
                failures.append('        builder src: %s'
                                % ', '.join(sorted(src_hits[pmid])))
            if doc_hits.get(pmid):
                n = len(doc_hits[pmid])
                failures.append('        docs/ (%d): %s'
                                % (n, ', '.join(sorted(doc_hits[pmid])[:4])))

    # ---- report --------------------------------------------------------
    report['passed'] = not failures
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)

    if failures:
        print('[FAIL] flagged-membership audit')
        for line in failures:
            print('  ' + line)
        return 1

    print('[OK] every FLAGGED paper carries a membership_class, and no '
          'uncitable PMID appears in builder source or under docs/.')
    print('     (%d unclassified, %d hard-uncitable PMIDs checked against '
          '%d builders and %d published files)'
          % (0, len(hard), len(_live_builder_sources()), len(_docs_files())))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
