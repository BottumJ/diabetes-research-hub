#!/usr/bin/env python3
"""Do the MARKDOWN documents cite the papers they say they cite?

WHY THIS EXISTS
---------------
Every citation gate in this repo scans `.py` files and only `.py` files:

    verify_pmids.py:44             if not fname.endswith('.py'): continue
    audit_prose_citation_titles.py:349   if not name.endswith('.py'): continue

That was a defensible scope while the dashboards were the only published
surface. It stopped being defensible once the governing documents themselves
started carrying citations. On 2026-08-31 a first manual pass over the root
markdown found miscitations in the two most load-bearing documents in the repo:

  RESEARCH_DOCTRINE.md   - the document that DEFINES the citation standard -
                           carried FOUR misattributed PMIDs inside its own
                           worked examples of correct citation. Its "PMID-
                           Verified (Strongest)" exemplar pointed at a
                           perovskite solar-cell paper (35912345). Its
                           correct-citation-format exemplar pointed at a
                           RETRACTED ginsenoside study (38234567). Its GOLD-tier
                           exemplar pointed at an HPV self-sampling survey
                           (37234567) and a cell-migration paper (37456789).

  Research_Findings_Summary.md - the public-facing summary - rated a claim GOLD
                           while citing a health-policy commentary that contains
                           none of the trials the rating was based on
                           (37356449), cited a semaglutide Comment as the
                           evidence for orforglipron (37385277), and reported a
                           retatrutide weight-loss figure (28.7% at 68 weeks)
                           that does not appear in the paper cited for it
                           (37366315 reports 24.2% at 48 weeks).

Every one of those PMIDs RESOLVES. That is the whole point: syntactic validity
is not support. A reader who clicks through lands on a real paper and has no
reason to doubt it unless they read the title.

WHAT THIS GATE DOES
-------------------
For every labelled PMID in a tracked markdown file, fetch the real title,
journal and year and compare them with the text around the citation:

  TITLE_ASSERTED    the surrounding text asserts enough title-like content
                    words to score against the real title
  COORDINATE_ONLY   the text asserts journal and/or year but no title; check
                    those coordinates instead
  BARE              the text asserts only the number; nothing to falsify, but
                    the PMID's existence is still confirmed

Reuses the classification and scoring built for the .py prose gate rather than
inventing a second standard, so a citation is judged the same way whichever file
it lives in.

SELF-EXCLUSION
--------------
Correction notes written by this project quote the wrong citation in order to
record it ("previously cited PMID 35912345 ... a solar-cell paper"). Those lines
would otherwise be re-flagged forever. Lines inside a blockquote that carry a
correction marker are skipped, and the skip is counted and reported so the
exclusion can never become silent.

Exit codes: 0 clean, 1 findings.
"""
import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audit_citation_identifiers import load_cache, save_cache, resolve_titles  # noqa: E402
from audit_builder_title_agreement import (  # noqa: E402
    content_words, overlap, MATCH_THRESHOLD, WEAK_THRESHOLD,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(BASE)
RESULTS = os.path.join(BASE, 'Results')
REPORT = os.path.join(RESULTS, 'markdown_citation_audit.json')

PMID_RE = re.compile(r'PMID[:\s#]*(\d{7,9})', re.IGNORECASE)

# Window of text around a citation that may assert things about it.
LOOKBACK = 320
LOOKAHEAD = 60
MIN_TITLE_WORDS = 4
YEAR_SLACK = 1

# Documents this project writes and publishes. Analysis/Results holds machine
# output and dated run reports — a historical record, not a live claim — so it
# is out of scope by class, the same exclusion audit_impossible_pmids.py makes.
TRACKED_DIRS = ['', 'docs', 'Notes']
EXCLUDED_DIR_PARTS = {'.git', 'Results', 'Logs', 'Papers', '_site', 'node_modules'}

# A DATED document is a record of a point in time, not a live claim — the same
# reasoning that puts Analysis/Results out of scope above, and the same rule
# audit_citation_coordinates.py applies to `_run_YYYYMMDD.py` files.
#
# This was forced by measurement on 2026-08-31, not anticipated.
# DECISION_BRIEF_2026-08-31.md is a TABLE of the day's repairs: its left column
# is the wrong attribution and its right column is the right one. The gate
# flagged all six rows, correctly by its own logic and wrongly in substance —
# quoting a defect in order to report it is not committing it. The blockquote
# exclusion did not cover it because a table row is not a blockquote.
#
# THE OBVIOUS RISK IS THAT THIS BECOMES A LOOPHOLE: date a filename, dodge the
# gate. Two things hold it shut. The exclusion is counted and printed every run,
# so it can never go silent; and it cannot reach an undated document, which is
# what every live claim in this repo lives in.
RE_DATED_DOCUMENT = re.compile(r'_\d{4}-\d{2}-\d{2}\.md$|_\d{8}\.md$')

# Distinctive journal tokens. Only these are treated as "the text names a
# journal", so the journal test asks whether the text CONTRADICTS PubMed rather
# than whether it is SILENT. Silence is not a defect; a wrong name is.
#
# Built from the corpus's own resolved metadata plus the handful of abbreviated
# forms this project writes by hand. A token qualifies only if it is rare enough
# to identify a journal — "diabetes", "journal", "medicine" and "clinical" name
# dozens and are excluded.
JOURNAL_STOPWORDS = {
    'journal', 'journals', 'medicine', 'medical', 'clinical', 'clinics',
    'research', 'reviews', 'review', 'international', 'american', 'european',
    'british', 'official', 'society', 'association', 'annals', 'archives',
    'frontiers', 'reports', 'science', 'sciences', 'health', 'care', 'therapy',
    'diabetes', 'diabetic', 'metabolism', 'metabolic', 'endocrinology',
    'obesity', 'north', 'america', 'targets', 'advances', 'current', 'open',
    'molecular', 'cell', 'cellular', 'biology', 'nutrition', 'public',
}

# Hand-written abbreviations that appear in this repo's prose and unambiguously
# identify a journal. Verified against the full names on 2026-08-31.
JOURNAL_ALIASES = {
    'nejm': 'new england journal of medicine',
    'jama': 'jama',
    'lancet': 'lancet',
    'diabetologia': 'diabetologia',
    'bmj': 'bmj',
    'nature': 'nature',
    'ajt': 'american journal of transplantation',
    'jcem': 'journal of clinical endocrinology and metabolism',
}


def journal_lexicon(meta_by_pmid):
    """The curated alias map. Kept as a function so callers stay stable.

    A CORPUS-DERIVED LEXICON WAS TRIED AND REJECTED, 2026-08-31.
    The idea was to harvest every token from every journal name in the resolved
    metadata cache and treat those tokens as journal-identifying. It yielded 235
    tokens and 14 findings, and every one of the 14 was false: "drug",
    "national", "development", "kidney" and "safety" all appear in some
    journal's name somewhere in a 350-paper corpus, so ordinary sentences were
    read as naming a journal. `- Use PMID 36449148 ... for approval and
    development history` was reported as naming a journal because *Drug
    Development* exists.

    Appearing in a journal title does not make a word distinctive. Establishing
    that a word is rare in ordinary prose needs a frequency corpus this script
    does not have, so the honest move is the small hand-verified list: it covers
    the abbreviations this repo actually writes, and it cannot fire on prose.
    `meta_by_pmid` is accepted and ignored so the signature survives if a real
    frequency source is ever wired in.
    """
    return dict(JOURNAL_ALIASES)


# A citation record in this repo's markdown is bracketed:
#     [PMID:37366315, JAMA, 2024]
#     [PMID:40544435, N Engl J Med, 2025 Sep 18]
# The journal claim belongs to the record it sits in. Checking a flat character
# window instead cross-attributes: a sentence citing three ONWARDS trials in
# three brackets made each one appear to name the others' journals (measured
# 2026-08-31, 7 false findings).
RECORD_RE = re.compile(r'\[([^\[\]]{0,300}?PMID[:\s#]*(\d{7,9})[^\[\]]{0,300}?)\]',
                       re.IGNORECASE)


def citation_record(window, pmid):
    """The bracketed record asserting this PMID, or None if unbracketed."""
    for match in RECORD_RE.finditer(window):
        if match.group(2) == pmid:
            return match.group(1)
    return None


def journal_contradiction(record, real_journal, lexicon):
    """Does this citation record name a DIFFERENT journal than PubMed reports?

    Returns [] when the record names no journal we recognise. Silence is not a
    defect.
    """
    if not record:
        return []
    real = (real_journal or '').lower()
    text = record.lower()
    named = []
    for alias, canonical in lexicon.items():
        if not re.search(r'\b' + re.escape(alias) + r'\b', text):
            continue
        if canonical in real or real in canonical or (
                real and content_words(canonical) & content_words(real)):
            continue
        named.append(alias)
    return sorted(named)


# A line that is BOTH a blockquote and carries a correction marker is this
# project recording a defect it already fixed. Both conditions required: a bare
# blockquote is still a claim, and a bare "CORRECTED" in body text is still live.
CORRECTION_MARKER = re.compile(
    r'\b(CORRECTED|SUPERSEDED|previously (?:cited|read)|WAS WRONG|'
    r'UNSOURCED|no PMID: template)\b', re.IGNORECASE)


def correction_block(lines, index):
    """Is this line inside a blockquote that carries a correction marker?

    Walks the contiguous run of `>` lines in both directions. Requires BOTH the
    blockquote and the marker, so an ordinary blockquote is still audited and a
    bare 'CORRECTED' in body text is still audited.
    """
    start = index
    while start > 0 and lines[start - 1].lstrip().startswith('>'):
        start -= 1
    end = index
    while end + 1 < len(lines) and lines[end + 1].lstrip().startswith('>'):
        end += 1
    return any(CORRECTION_MARKER.search(line) for line in lines[start:end + 1])


def published_results_markdown():
    """Analysis/Results markdown that the published hub actually links to.

    The blanket exclusion of Analysis/Results was correct for 255 of its 257
    markdown files: dated run records, a historical log, not a live claim. It
    was WRONG for two, and the 2026-08-31 queue item said so - "verify that is
    still true, since some are linked from dashboards". Verified 2026-09-04 and
    it was not true: docs/index.html advertises literature_gap_report.md and
    pubmed_recent_summary.md as live reports. Both are generated, both are
    undated, and no citation gate had ever read either.

    Scope is DERIVED from the hub rather than listed here, so a report added to
    or dropped from the site changes what is checked without anyone remembering
    to edit this function. Both files carry zero PMIDs today; that is a fact
    about today, not a reason to leave them ungated.
    """
    index = os.path.join(REPO, 'docs', 'index.html')
    if not os.path.exists(index):
        return
    with open(index, encoding='utf-8', errors='replace') as fh:
        html = fh.read()
    names = set(re.findall(r'href="Reports/([A-Za-z0-9_\-.]+\.md)"', html))
    names |= set(re.findall(r'href="Analysis/Results/([A-Za-z0-9_\-.]+\.md)"', html))
    for name in sorted(names):
        path = os.path.join(RESULTS, name)
        if os.path.isfile(path):
            yield path


def tracked_markdown():
    yield from published_results_markdown()
    for rel_dir in TRACKED_DIRS:
        directory = os.path.join(REPO, rel_dir) if rel_dir else REPO
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            path = os.path.join(directory, name)
            if not os.path.isfile(path) or not name.endswith('.md'):
                continue
            if any(part in EXCLUDED_DIR_PARTS for part in path.split(os.sep)):
                continue
            yield path


# A title assertion in markdown is MARKED UP, not merely adjacent. These are the
# forms this repo actually uses. See classify() for why this matters.
# NOTE the deliberate absence of `**bold**`. Measured 2026-08-31: this repo uses
# bold for EMPHASIS ("**Validation: GOLD**", "**Both are narrative reviews**"),
# never for titles. Including it classified emphasis as a title assertion and
# produced 7 spurious MISMATCHes while catching zero real ones. Titles here are
# quoted or italicised.
TITLE_SPAN_RE = re.compile(
    r'"([^"\n]{12,300})"'                 # "Islet transplantation outcomes..."
    r'|“([^”\n]{12,300})”'  # curly quotes
    r'|(?<!\*)\*([^*\n]{12,300})\*(?!\*)'  # *Italic Title*
)

# A title assertion has to sit BESIDE the identifier. A quoted phrase 300
# characters away in an unrelated sentence is not a claim about this paper.
TITLE_PROXIMITY = 130


# A span that swallows a fence, a blank line or another marker is a greedy-match
# artifact, not a title. The straight-quote alternative in TITLE_SPAN_RE has no
# right boundary of its own, so an UNBALANCED quote earlier in the window (the
# format template `"Title," Journal Vol(Issue):Pages`) will happily run forward
# and consume the real quoted title behind it. Measured 2026-08-31: that is
# exactly what made the correct, hand-verified citation at RESEARCH_DOCTRINE.md
# :550 score 0.0 and report MISMATCH. Same defect class as
# audit_extractor_wildcards.py.
SPAN_POISON = ('```', '\n\n', 'XXXXX', 'Vol(Issue)')


def title_spans(window, pmid_pos=None):
    """Marked-up title assertions, nearest the citation first."""
    found = []
    for match in TITLE_SPAN_RE.finditer(window):
        span = next(g for g in match.groups() if g is not None)
        if any(poison in span for poison in SPAN_POISON):
            continue
        if len(content_words(span)) < MIN_TITLE_WORDS:
            continue
        if pmid_pos is None:
            found.append((0, span))
            continue
        # Distance from the nearest edge of the span to the identifier.
        distance = min(abs(match.end() - pmid_pos), abs(match.start() - pmid_pos))
        if distance > TITLE_PROXIMITY:
            continue
        found.append((distance, span))
    found.sort(key=lambda pair: pair[0])
    return [span for _, span in found]


def classify(window, meta):
    """Which test can actually falsify this citation?

    THIS FUNCTION WAS WRONG ON ITS FIRST DRAFT AND THE FIRST RUN PROVED IT.
    The draft classified a citation as TITLE_ASSERTED whenever >= 4 content
    words survived in the 320-char window after removing journal and year
    tokens. In markdown almost every window clears that bar, because the words
    around a citation are ordinary prose:

        "- General diabetes drug cost-effectiveness (PMID 38639547) covers
           SGLT2i and GLP-1 agonists"

    That sentence asserts nothing about the paper's TITLE. Scored against the
    real title ("Cost-Effectiveness of Newer Pharmacologic Treatments in Adults
    With Type 2 Diabetes...") it returns near zero, and the citation is
    perfectly correct. The draft flagged 71 of 73 sites — a 97% false-positive
    rate, which is the identical failure audit_prose_citation_titles.py records
    for its own first draft (249 spurious mismatches on 2026-08-26) and the
    identical failure audit_gap_evidence_design.py reproduced on 2026-08-30.
    Three gates, one mistake: scoring a claim the text never made.

    A markdown title assertion is MARKED UP — quoted, bolded or italicised.
    Descriptive prose beside a PMID is a summary, not a claim about the title,
    and the only thing it can be checked against is whether the paper exists.
    So descriptive prose now falls through to DESCRIPTIVE and is not scored.

    Measured on the same corpus after this change: see the counts this script
    prints, and markdown_citation_audit.json['calibration'].
    """
    spans = title_spans(window, pmid_pos=len(window) - LOOKAHEAD)
    if spans:
        return 'TITLE_ASSERTED', spans
    journal_words = content_words(meta.get('journal') or '')
    window_words = content_words(window)
    years = [int(y) for y in re.findall(r'\b((?:19|20)\d{2})\b', window)]
    if (journal_words and (journal_words & window_words)) or years:
        return 'COORDINATE_ONLY', spans
    return 'DESCRIPTIVE', spans


def main():
    findings, checked, skipped_corrections = [], [], 0
    occurrences = []
    skipped_dated = {}

    for path in tracked_markdown():
        rel = os.path.relpath(path, REPO)
        if RE_DATED_DOCUMENT.search(os.path.basename(path)):
            with open(path, encoding='utf-8', errors='replace') as fh:
                skipped_dated[rel] = len(PMID_RE.findall(fh.read()))
            continue
        with open(path, encoding='utf-8', errors='replace') as fh:
            text = fh.read()
        lines = text.split('\n')
        offset = 0
        line_start = []
        for line in lines:
            line_start.append(offset)
            offset += len(line) + 1

        for match in PMID_RE.finditer(text):
            pos = match.start()
            lineno = max(i for i, s in enumerate(line_start) if s <= pos) + 1
            line = lines[lineno - 1]
            # A correction note is a BLOCK, not a line: the marker sits in the
            # first line of the blockquote and the offending PMID is quoted two
            # lines down. Checking the single line missed those and re-flagged
            # this project's own repair record forever (measured 2026-08-31).
            if line.lstrip().startswith('>') and correction_block(lines, lineno - 1):
                skipped_corrections += 1
                continue
            window = text[max(0, pos - LOOKBACK):pos + LOOKAHEAD]
            occurrences.append({'pmid': match.group(1), 'file': rel,
                                'line': lineno, 'window': window,
                                'text': line.strip()[:200]})

    pmids = sorted({o['pmid'] for o in occurrences})
    print('=' * 74)
    print('MARKDOWN CITATION AUDIT - do the .md documents cite what they claim?')
    print('=' * 74)
    print(f'{len(pmids)} distinct PMIDs across {len(occurrences)} citation sites '
          f'in tracked markdown.')
    print(f'{skipped_corrections} sites skipped as this project\'s own correction notes.')
    if skipped_dated:
        total_dated = sum(skipped_dated.values())
        print(f'{total_dated} sites skipped in {len(skipped_dated)} DATED documents '
              f'(records of a point in time, not live claims):')
        for name, count in sorted(skipped_dated.items()):
            print(f'    {name}: {count}')

    cache = load_cache()
    meta_by_pmid = resolve_titles(pmids, cache)
    save_cache(cache)
    # Lexicon is built from the whole resolved cache, not just today's PMIDs, so
    # a journal named in prose is recognisable even if no paper from it is cited
    # on this page.
    lexicon = journal_lexicon(cache.get('title', cache))
    print(f'Journal lexicon: {len(lexicon)} distinctive tokens.')

    for occ in occurrences:
        meta = meta_by_pmid.get(occ['pmid']) or {}
        title = meta.get('title')
        if not title:
            findings.append({**{k: occ[k] for k in ('pmid', 'file', 'line', 'text')},
                             'verdict': 'UNRESOLVED',
                             'detail': 'PubMed returned no record for this PMID'})
            continue
        kind, residual = classify(occ['window'], meta)
        record = {k: occ[k] for k in ('pmid', 'file', 'line', 'text')}
        record.update({'kind': kind, 'real_title': title,
                       'real_journal': meta.get('journal'), 'real_year': meta.get('year')})

        if kind == 'TITLE_ASSERTED':
            # Score the ASSERTED span, not the whole window: the window carries
            # surrounding prose that dilutes a correct assertion toward zero.
            score = max(overlap(span, title) for span in residual)
            record['score'] = round(score, 3)
            record['asserted'] = [s[:140] for s in residual]
            if score < WEAK_THRESHOLD:
                record['verdict'] = 'MISMATCH'
                record['detail'] = ('surrounding text shares almost no content with '
                                    'the real title')
                findings.append(record)
            elif score < MATCH_THRESHOLD:
                record['verdict'] = 'WEAK'
                record['detail'] = 'partial overlap; read it'
                findings.append(record)
            else:
                record['verdict'] = 'OK'
                checked.append(record)
        elif kind == 'COORDINATE_ONLY':
            # ONLY the year is checked here.
            #
            # The draft also flagged a journal mismatch whenever the real
            # journal's words were absent from the window. That is a test for
            # SILENCE, not for contradiction: "- Use PMID 38639547 for general
            # cost-effectiveness framework" names no journal at all and was
            # reported as asserting the wrong one. It produced 16 spurious
            # COORDINATE_MISMATCHes on 2026-08-31 and no true ones. Deciding
            # that a span of prose names *some* journal needs a journal lexicon
            # this script does not have; a four-digit year needs nothing.
            problems = []
            cite_record = citation_record(occ['window'], occ['pmid'])
            scope = cite_record if cite_record else occ['window'][-160:]
            years = [int(y) for y in re.findall(r'\b((?:19|20)\d{2})\b', scope)]
            real_year = meta.get('year')
            if years and real_year and not any(abs(y - int(real_year)) <= YEAR_SLACK
                                               for y in years):
                problems.append(f'year asserted beside the PMID is {years}, '
                                f'PubMed says {real_year}')
            # YEAR_SLACK=1 exists because e-pub and print years legitimately
            # differ by one. That slack is also a hole: "[PMID:37366315, JAMA,
            # 2024]" for an NEJM 2023 paper passes the year test on a one-year
            # difference, and the thing that is actually wrong is the journal.
            # Found by test_markdown_citation_gate.py, not by inspection.
            named = journal_contradiction(cite_record, meta.get('journal'), lexicon)
            if named:
                problems.append(f'text names {named} beside the PMID; '
                                f'PubMed says {meta.get("journal")!r}')
            if problems:
                record['verdict'] = 'COORDINATE_MISMATCH'
                record['detail'] = '; '.join(problems)
                findings.append(record)
            else:
                record['verdict'] = 'OK'
                checked.append(record)
        else:
            # DESCRIPTIVE: the text summarises the paper but asserts no title
            # and no coordinates. Nothing here is falsifiable beyond existence,
            # which resolve_titles() has just confirmed. Not a finding.
            record['verdict'] = 'DESCRIPTIVE_EXISTS'
            checked.append(record)

    kinds = {}
    for rec in checked + findings:
        kinds[rec.get('kind', 'UNRESOLVED')] = kinds.get(rec.get('kind', 'UNRESOLVED'), 0) + 1
    by_verdict = {}
    for f in findings:
        by_verdict.setdefault(f['verdict'], []).append(f)
    print('\nClassification: ' + ', '.join(f'{k}={v}' for k, v in sorted(kinds.items())))
    print(f'Passed: {len(checked)}   Flagged: {len(findings)}')
    for verdict in ('UNRESOLVED', 'MISMATCH', 'COORDINATE_MISMATCH', 'WEAK'):
        items = by_verdict.get(verdict, [])
        if not items:
            continue
        print(f'\n--- {verdict} ({len(items)}) ---')
        for f in items:
            print(f"  {f['pmid']}  {f['file']}:{f['line']}")
            print(f"      says : {f['text'][:150]}")
            print(f"      is   : {(f.get('real_title') or '?')[:110]}")
            print(f"             {f.get('real_journal')} {f.get('real_year')}")
            if f.get('detail'):
                print(f"      why  : {f['detail']}")

    report = {
        'generated': datetime.now().isoformat(),
        'scope': 'tracked markdown (repo root, docs/, Notes/)',
        'gap_this_closes': ('verify_pmids.py and audit_prose_citation_titles.py '
                            'both scan .py only; markdown was never audited'),
        'citation_sites': len(occurrences),
        'distinct_pmids': len(pmids),
        'correction_notes_skipped': skipped_corrections,
        'dated_documents_skipped': skipped_dated,
        'passed': len(checked),
        'flagged': len(findings),
        'classification': kinds,
        'calibration': {
            'first_draft_2026-08-31': {
                'rule': 'TITLE_ASSERTED if >=4 residual content words in a 320-char window',
                'flagged': 71,
                'of_sites': 73,
                'false_positive_rate': '~97%',
                'why': ('descriptive prose beside a PMID was scored as if it '
                        'asserted the title'),
            },
            'shipped_rule': ('TITLE_ASSERTED only for a quoted/bold/italic span of '
                             '>=4 content words; descriptive prose falls through to '
                             'DESCRIPTIVE and is checked for existence only'),
            'shipped_flagged': len(findings),
            'shipped_of_sites': len(occurrences),
        },
        'findings': findings,
    }
    os.makedirs(RESULTS, exist_ok=True)
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print(f'\nReport: {os.path.relpath(REPORT, REPO)}')

    if findings:
        print('\n[FAIL] markdown citation audit found issues')
        return 1
    print('\n[OK] markdown citations agree with PubMed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
