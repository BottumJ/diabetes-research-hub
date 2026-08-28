#!/usr/bin/env python3
"""Does every script that reads PMIDs ask corpus_membership whether they count?

THE PATTERN THIS GATE EXISTS TO BREAK
-------------------------------------
Every previous seal in this repo was applied BY NAME, after a leak:

  2026-08-24  ingest_papers.py            guarded after 12345678 entered
  2026-08-24  reconcile_paper_index.py    guarded after the index re-added it
  2026-08-25  extract_evidence.py         guarded after 30078372 kept publishing
  2026-08-25  extract_corpus_data.py      guarded, same run
  2026-08-27  work-queue note: audit_citation_coordinates.py and
              audit_citation_load_bearing.py are two MORE new readers and both
              started life unguarded - the pattern predicting itself

Naming doors does not close the class. This gate asks a structural question
instead: if a script reads the abstracts directory, the full-text directory,
or the paper-library index, does it import corpus_membership? If not, it
fails, whether or not it has leaked yet.

CLASSIFY BEFORE SCORING
-----------------------
Written this way deliberately, because in this repo new gates over-fire on
their first run and then get tuned into meaninglessness:
audit_prose_citation_titles.py reported 249 mismatches of which almost none
were real, and audit_retractions.py went red on the record of its own fix.
Both were fixed by classifying the input before scoring it, so that is the
starting design here rather than the repair.

  LIVE       builders, extractors and the pipeline runner. These publish.
             Reading PMIDs without membership is a FAILURE.
  AUDIT      audit_*.py, verify_*.py, reconcile_*.py. These exist to look at
             everything, including excluded papers, and must NOT be forced to
             filter them out - an audit that cannot see the excluded set
             cannot report on it. Reported, never failed.
  ONESHOT    _run_*.py, _close_run_*.py, *_20260825.py. Dated one-shot
             repair scripts, already executed, kept as an audit trail.
             Rewriting history to satisfy a gate would be worse than the gate.
  TOOL       corpus_membership.py itself and this file.

POSITIVE CONTROL
----------------
A gate that reports zero because its detector is broken looks identical to a
gate that reports zero because the repo is clean. So before judging anything
this script proves its own detector fires: it must find the known readers
(extract_corpus_data.py, extract_evidence.py) as PMID readers, and it must
see corpus_membership imported in them. If the control fails, the run aborts
rather than printing a reassuring zero.

Exit 1 on any LIVE script reading PMIDs without membership.
"""

import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Signals that a script reads the paper corpus off disk or out of the index.
READER_SIGNALS = [
    (re.compile(r"abstracts_dir|['\"]abstracts['\"]"), 'abstracts dir'),
    (re.compile(r"fulltext_dir|['\"]fulltext['\"]"), 'fulltext dir'),
    (re.compile(r"paper_library.*index\.json|['\"]index\.json['\"]"), 'library index'),
    (re.compile(r"not_corpus_pmids\.json"), 'not-corpus registry'),
    (re.compile(r"status'?\]?\s*==\s*['\"]FLAGGED['\"]"), 'FLAGGED status'),
]

GUARD = re.compile(r'^\s*(?:import\s+corpus_membership|from\s+corpus_membership\s+import)',
                   re.M)

# Two shapes, and they need different anchors. The first draft wrote them as
# one alternation under re.match, which anchors every branch at position 0 and
# so silently never matched the DATED-SUFFIX form - it reported
# adjudicate_flagged_membership_20260828.py as a LIVE failure on its first
# run. Left visible because it is the same class of error the gate hunts:
# a check that looks correct and is aimed at the wrong surface.
ONESHOT_PREFIX = re.compile(r'^(_run_|_close_run_|_tmp_)')
ONESHOT_SUFFIX = re.compile(r'_\d{8}\.py$|_\d{4}_\d{2}_\d{2}\.py$')
AUDIT = re.compile(r'^(audit_|verify_|reconcile_|check_|track_)')

TOOL_FILES = {'corpus_membership.py', 'audit_unguarded_pmid_readers.py'}

# Scripts that read PMIDs but legitimately must see the excluded set, named
# with a reason. Kept SHORT and explicit; an exemption list that grows without
# reasons is how a gate stops meaning anything.
EXEMPT = {
    'agent_state.py': 'owns agent_state.json; corpus_membership reads it, so importing it here would be circular',
    'build_paper_library.py': 'the library dashboard must SHOW excluded papers with their status, not hide them',
}


def classify(name):
    if name in TOOL_FILES:
        return 'TOOL'
    if ONESHOT_PREFIX.match(name) or ONESHOT_SUFFIX.search(name):
        return 'ONESHOT'
    if AUDIT.match(name):
        return 'AUDIT'
    return 'LIVE'


def scan():
    rows = []
    for name in sorted(os.listdir(SCRIPT_DIR)):
        if not name.endswith('.py'):
            continue
        path = os.path.join(SCRIPT_DIR, name)
        try:
            with open(path, encoding='utf-8') as fh:
                src = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        signals = [label for pat, label in READER_SIGNALS if pat.search(src)]
        if not signals:
            continue
        rows.append({
            'file': name,
            'klass': classify(name),
            'signals': signals,
            'guarded': bool(GUARD.search(src)),
        })
    return rows


def positive_control(rows):
    """Prove the detector fires before trusting it to report zero."""
    by = {r['file']: r for r in rows}
    problems = []
    for known in ('extract_corpus_data.py', 'extract_evidence.py'):
        if known not in by:
            problems.append('%s not detected as a PMID reader' % known)
        elif not by[known]['guarded']:
            problems.append('%s detected but its corpus_membership import was not seen'
                            % known)
    return problems


def main():
    rows = scan()

    problems = positive_control(rows)
    if problems:
        print('CONTROL FAILED - not reporting a verdict:')
        for p in problems:
            print('  ' + p)
        print('A zero from a broken detector is indistinguishable from a clean repo.')
        return 2

    failures = [r for r in rows
                if r['klass'] == 'LIVE' and not r['guarded']
                and r['file'] not in EXEMPT]

    counts = {}
    for r in rows:
        counts[r['klass']] = counts.get(r['klass'], 0) + 1

    print('PMID readers found: %d  (%s)'
          % (len(rows), ', '.join('%s=%d' % kv for kv in sorted(counts.items()))))
    print('Control: detector fires on both known readers and sees their guard.')
    print()

    for klass in ('LIVE', 'AUDIT', 'ONESHOT', 'TOOL'):
        sel = [r for r in rows if r['klass'] == klass]
        if not sel:
            continue
        guarded = sum(1 for r in sel if r['guarded'])
        print('  %-8s %2d reader(s), %d guarded' % (klass, len(sel), guarded))

    if EXEMPT:
        print()
        print('  Exempt by name, with reason:')
        for k, v in sorted(EXEMPT.items()):
            print('    %-32s %s' % (k, v))

    if failures:
        print()
        print('[FAIL] %d LIVE script(s) read PMIDs without asking corpus_membership:'
              % len(failures))
        for r in failures:
            print('  %-40s reads: %s' % (r['file'], ', '.join(r['signals'])))
        print()
        print('  Add "import corpus_membership" and filter through it, or add an')
        print('  entry to EXEMPT with a written reason. Do not add a local loader:')
        print('  five local loaders is how 17 adjudicated-off-topic papers came to')
        print('  be excluded by one consumer and admitted by four others.')
        return 1

    print()
    print('[OK] every LIVE PMID reader goes through corpus_membership.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
