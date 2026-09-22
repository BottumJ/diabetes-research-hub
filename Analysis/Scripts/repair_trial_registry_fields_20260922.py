#!/usr/bin/env python3
"""Bring build_trial_equity_mapper.py's twelve trial records back to the registry.

WHAT WAS WRONG, AND WHY EVERY GATE WAS GREEN ON IT
--------------------------------------------------
Each of the twelve records sits under a hand-written `# --- VERIFIED: ... ---`
comment. Checked against live ClinicalTrials.gov on 2026-09-22, eight of the
twelve disagreed with the registry, six of them about whether the trial is
still open:

    NCT03875729  Teplizumab PROTECT    file Active      registry COMPLETED 2023-05
    NCT02691247  CLBS03 T-Rex          file Active      registry COMPLETED 2020-01
    NCT01341899  Autologous HSCT       file Active      registry COMPLETED 2015-12
    NCT01773707  Abatacept TN-18       file Active      registry COMPLETED 2022-12
    NCT05210530  VCTX210A              file Recruiting  registry COMPLETED 2023-01
    NCT00434811  CIT-07                file Completed   registry COMPLETED 2014-05  (enrollment only)

"Active" is the attribute a reader is most likely to ACT on: on the published
equity map it is the difference between a trial someone could ask to join and
one that closed before they opened the page. The oldest of these finished in
2015.

THE `VERIFIED` COMMENT IS THE FINDING, NOT A MITIGATION. It records that
somebody checked once. Nothing re-checks, and a registry fact is not the kind
of fact that stays checked -- four of these six trials completed AFTER the
comment was written. This is the case the open queue item "the VERIFIED
comments are not verification" predicted, now with numbers.

ONE ENTRY IS NOT STALE, IT IS THE WRONG TRIAL
---------------------------------------------
NCT04262479 was labelled:

    'name':       'DIAGNODE-3 (GAD-Alum intralymphatic vaccine)'
    'phase':      'Phase 3'
    'enrollment': 330,   # DIAGNODE-3 target enrollment per ClinicalTrials.gov

The registry record for NCT04262479 is "Injections of Glutamic Acid
Decarboxylase (GAD) for LADA Type of Diabetes" -- PHASE 2, 14 participants
(ACTUAL), completed 2022-05-05. It is a fourteen-patient LADA study. The name,
the phase and the enrollment all belong to a different trial in the same
sponsor's programme, and the trailing comment sourced the wrong number "per
ClinicalTrials.gov" while pointing at a record that says something else.

Same defect class as the teplizumab "Phase 3 (TN-10)" mislabel already in the
work queue: right drug, right sponsor, wrong trial, and every identifier
resolves.

NOT GUESSED AT: this repair does NOT substitute the DIAGNODE-3 identifier. The
house rule from 2026-08-29 is that a wrong citation is corrected to what the
cited record actually says, or marked, but never swapped for an invented
replacement. NCT04262479 is restated as the LADA study it is -- which is, as it
happens, squarely on this hub's Gap #1 and #8 subject matter.

PROVENANCE
----------
Every value written below was read from
https://clinicaltrials.gov/api/v2/studies/<NCT> on 2026-09-22. Enrollment type
(ACTUAL vs ESTIMATED) is recorded with the number, because the two mean
different things and conflating them is how "330 planned" became "330 enrolled".
"""

import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', '..'))
TARGET = os.path.join(ROOT, 'Analysis', 'Scripts', 'build_trial_equity_mapper.py')
ASOF = '2026-09-22'

# nct -> field updates, read live from ClinicalTrials.gov on ASOF.
REGISTRY = {
    'NCT04786262': {'status': 'Recruiting', 'enrollment': 57,
                    'phase': 'Phase 3',
                    'enrollment_type': 'ESTIMATED'},
    'NCT04262479': {'status': 'Completed', 'enrollment': 14,
                    'phase': 'Phase 2',
                    'name': 'GAD-Alum intralymphatic injections in LADA',
                    'enrollment_type': 'ACTUAL'},
    'NCT03875729': {'status': 'Completed', 'enrollment': 328,
                    'enrollment_type': 'ACTUAL'},
    'NCT00434811': {'status': 'Completed', 'enrollment': 48,
                    'enrollment_type': 'ACTUAL'},
    'NCT02081326': {'status': 'Active, not recruiting', 'enrollment': 150,
                    'enrollment_type': 'ESTIMATED'},
    'NCT02691247': {'status': 'Completed', 'enrollment': 113,
                    'enrollment_type': 'ACTUAL'},
    'NCT01341899': {'status': 'Completed', 'enrollment': 50,
                    'enrollment_type': 'ACTUAL'},
    'NCT00279305': {'status': 'Completed', 'enrollment': 87,
                    'phase': 'Phase 2',
                    'enrollment_type': 'ACTUAL'},
    'NCT01773707': {'status': 'Completed', 'enrollment': 212,
                    'enrollment_type': 'ACTUAL'},
    'NCT04545151': {'status': 'Completed', 'enrollment': 136,
                    'enrollment_type': 'ACTUAL'},
    'NCT04233034': {'status': 'Completed', 'enrollment': 113,
                    'enrollment_type': 'ACTUAL'},
    'NCT05210530': {'status': 'Completed', 'enrollment': 7,
                    'enrollment_type': 'ACTUAL'},
}

RECORD_RE = re.compile(r"\{[^{}]*?'nct_id':\s*'(NCT\d+)'[^{}]*?\}", re.S)


def patch_record(block, nct, updates):
    changes = []
    out = block
    for field in ('name', 'phase', 'status'):
        if field not in updates:
            continue
        m = re.search(r"('%s':\s*')([^']*)(')" % field, out)
        if m and m.group(2) != updates[field]:
            changes.append('%s %r -> %r' % (field, m.group(2), updates[field]))
            out = out[:m.start(2)] + updates[field] + out[m.end(2):]

    if 'enrollment' in updates:
        m = re.search(r"('enrollment':\s*)(\d+)(,?)([^\n]*)", out)
        if m:
            old = int(m.group(2))
            new = updates['enrollment']
            # The trailing comment is replaced whether or not the number moved:
            # on NCT04262479 the number was wrong AND its comment cited the
            # registry for a value the registry does not contain.
            note = ("  # %s per ClinicalTrials.gov %s"
                    % (updates.get('enrollment_type', 'ACTUAL'), ASOF))
            if old != new:
                changes.append('enrollment %d -> %d' % (old, new))
            out = (out[:m.start(2)] + str(new) + m.group(3) + note
                   + out[m.end(4):])
    return out, changes


def main():
    src = open(TARGET, encoding='utf-8').read()
    original = src
    all_changes = []

    for m in list(RECORD_RE.finditer(src)):
        nct = m.group(1)
        upd = REGISTRY.get(nct)
        if not upd:
            continue
        new_block, changes = patch_record(m.group(0), nct, upd)
        if changes:
            src = src.replace(m.group(0), new_block, 1)
            all_changes.append((nct, changes))

    # Replace the unverifiable VERIFIED banners with a dated, sourced one.
    # Left as a single sweep rather than per-record edits so no banner is
    # missed: the claim "VERIFIED" with no date and no source is exactly what
    # made eight stale records look checked.
    src = re.sub(r'# --- VERIFIED(?: against ClinicalTrials\.gov [\d-]+)?:?',
                 '# --- registry fields refreshed from ClinicalTrials.gov %s:' % ASOF,
                 src)
    src = re.sub(r'# --- registry fields refreshed from ClinicalTrials\.gov '
                 r'%s --- *\n' % ASOF,
                 '# --- registry fields refreshed from ClinicalTrials.gov %s ---\n' % ASOF,
                 src)

    if src == original:
        print('  no changes')
        return 0

    with open(TARGET, 'w', encoding='utf-8') as fh:
        fh.write(src)

    print('  TRIAL REGISTRY FIELD REPAIR  (%s)' % ASOF)
    for nct, changes in all_changes:
        print('    %s' % nct)
        for c in changes:
            print('        %s' % c)
    print('    records repaired: %d of %d' % (len(all_changes), len(REGISTRY)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
