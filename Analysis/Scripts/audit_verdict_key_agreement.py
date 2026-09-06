#!/usr/bin/env python3
"""Does any stored path record assert two different verdicts about itself?

WHY THIS EXISTS
---------------
A path's validation verdict is stored under `rating`, under `status`, or under
both. Measured 2026-09-06 across state['validated_paths'] (67 records):

    rating only   37
    status only   10
    both          20

path_store.resolve_paths() reads these defensively - status_of() tries
`status`, then `rating`, then `validation_status` - so every consumer that
routes through path_store gets the right answer today. Nothing published is
currently wrong because of this, and this gate does not claim otherwise.

The defect is that the correctness is CONVENTIONAL rather than structural. It
holds only while every consumer remembers to route through path_store, and one
of the twenty both-key records disagrees with itself:

    GLP1_RA -> neuroprotection      rating: VALIDATED
                                    status: PARTIALLY_VALIDATED

That record is the repo's most consequential downgrade. On 2026-08-20 the
bare-string audit resolved its flagship citation and found ELAD (PMID 41326666,
Nat Med 2026) was NEGATIVE on its primary endpoint - cerebral glucose metabolic
rate, difference -0.17 (95% CI -0.39 to 0.06), P = 0.14 - with ADCS-ADL P =
0.65 and CDR-SoB P = 0.81 both null, in 204 participants WITHOUT diabetes. The
verdict was moved VALIDATED/HIGH -> PARTIALLY_VALIDATED/LOW. The downgrade
wrote `status` and left `rating` at VALIDATED.

So the single most carefully-reasoned retraction in this repository is still
sitting in the store labelled VALIDATED under the key that 57 of 67 records use
as their primary. One direct `rec.get('rating')` anywhere - in a new script, in
a notebook, in a future dashboard - republishes a verdict the project
explicitly withdrew, and no citation gate would object, because every PMID in
the record is real and correctly transcribed. The claim would be false and its
citations perfect.

WHY path_store's OWN CANONICALISER DOES NOT CATCH IT
----------------------------------------------------
path_store.dedupe_state() does write the canonical verdict into both keys - but
only inside its duplicate-spelling loop, which begins `if len(raw_keys) < 2:
continue`. A record with ONE spelling and TWO disagreeing verdict keys is never
reached. The canonicaliser was built for a different defect (the 2026-08-17
mirror-reconciliation) and happens to fix this one only as a side effect, for
the subset of records that also had duplicate names.

WHAT THIS GATE ASSERTS
----------------------
    VERDICT_DISAGREEMENT  one record, two verdict keys, two different values.
                          The store contradicts itself and which answer a
                          reader gets depends on which key a consumer happens
                          to read.

Applies to state['paths'] and state['validated_paths'].
Read-only. Use --fix to write the conservative resolution into every verdict
key on the record (see rank order below), preserving both keys so no existing
consumer breaks.

Exit codes: 0 clean, 1 findings.
"""
import argparse
import json
import os
import shutil
import sys
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
STATE = os.path.join(BASE, 'Results', 'agent_state.json')
REPORT = os.path.join(BASE, 'Results', 'verdict_key_agreement_audit.json')

VERDICT_KEYS = ('status', 'rating', 'validation_status')
STORES = ('paths', 'validated_paths')

# Conservatism order, least to most confident. A disagreement resolves DOWN:
# the project's own doctrine is that an overstated verdict is the expensive
# error, and every disagreement found so far arose from a downgrade that only
# half-landed - so the lower value is also the newer one.
RANK = {
    'CONTRADICTED': 0,
    'CONTRADICTED_FOR_DIABETIC_NEPHROPATHY': 0,
    'EXTRACTION_ARTIFACT': 0,
    'HOLLOW': 1,
    'UNVALIDATED': 2,
    'NEEDS_RECHECK': 2,
    'PARTIALLY_VALIDATED': 3,
    'VALIDATED': 4,
}


def rank(value):
    return RANK.get(str(value).upper(), 2)


def in_vocabulary(value):
    """Is this a plain verdict, or a verdict about a DIFFERENT proposition?

    Added after this gate's own first run, which reported three disagreements
    and would have corrupted one of them under --fix.

        paths['atorvastatin -> T2D']   status: CONTRADICTED
                                       rating: VALIDATED_AS_RISK_FACTOR

    Those are not two answers to one question. They are one answer each to two
    questions: the THERAPEUTIC claim (atorvastatin treats T2D) is contradicted,
    and the CAUSAL claim (atorvastatin raises T2D incidence) is validated -
    Sattar 2010, PMID 19794004, IPD meta-analysis of 13 trials and 91,140
    patients, +9% incident T2D; Navarese 2016, PMID 27277934, atorvastatin
    specifically +12%. Resolving "conservatively" to CONTRADICTED would have
    overwritten a correct, well-cited finding with a verdict about a different
    proposition, and the record's own notes field would have been the only
    surviving trace.

    The tell is that VALIDATED_AS_RISK_FACTOR is not in the standard verdict
    vocabulary. A verdict value carrying its own qualifier is a scoped verdict,
    and scoped verdicts cannot be compared to plain ones by rank. So they are
    reported as VERDICT_SCOPE_MISMATCH and never auto-resolved: a human has to
    say which proposition the record is about.

    A gate that silently destroys evidence to make a store self-consistent is
    worse than the inconsistency it removes.
    """
    return str(value).upper() in RANK


def verdicts(rec):
    return {k: rec[k] for k in VERDICT_KEYS
            if isinstance(rec, dict) and rec.get(k)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fix', action='store_true',
                    help='write the conservative resolution into every verdict '
                         'key on each disagreeing record')
    args = ap.parse_args()

    print('=' * 60)
    print('  VERDICT-KEY AGREEMENT GATE')
    print('=' * 60)

    with open(STATE, encoding='utf-8') as fh:
        state = json.load(fh)

    findings, key_census = [], {}
    for store_name in STORES:
        store = state.get(store_name, {})
        for path_key, rec in store.items():
            if not isinstance(rec, dict):
                continue
            v = verdicts(rec)
            shape = '+'.join(sorted(v)) or 'none'
            key_census[shape] = key_census.get(shape, 0) + 1
            if len(set(str(x).upper() for x in v.values())) > 1:
                scoped = {k: x for k, x in v.items() if not in_vocabulary(x)}
                if scoped:
                    findings.append({
                        'kind': 'VERDICT_SCOPE_MISMATCH',
                        'store': store_name,
                        'path': path_key,
                        'verdicts': v,
                        'off_vocabulary': scoped,
                        'conservative_resolution': None,
                        'note': 'A verdict value outside the standard vocabulary '
                                'is a verdict about a different proposition, not '
                                'a competing answer to the same one. Not '
                                'auto-resolvable; needs a human to say which '
                                'proposition the record is about.',
                    })
                else:
                    findings.append({
                        'kind': 'VERDICT_DISAGREEMENT',
                        'store': store_name,
                        'path': path_key,
                        'verdicts': v,
                        'conservative_resolution': min(v.values(), key=rank),
                    })

    fixable = [f for f in findings if f['kind'] == 'VERDICT_DISAGREEMENT']
    unfixable = [f for f in findings if f['kind'] == 'VERDICT_SCOPE_MISMATCH']

    fixed = []
    if args.fix and fixable:
        shutil.copy2(STATE, STATE + f'.bak_{date.today().isoformat()}_verdictkeys')
        for f in fixable:
            rec = state[f['store']][f['path']]
            for k in list(verdicts(rec)):
                rec[k] = f['conservative_resolution']
            rec['verdict_key_normalised_on'] = date.today().isoformat()
            rec['verdict_key_normalised_note'] = (
                f"Record asserted {f['verdicts']} simultaneously. Resolved to "
                f"the conservative value by audit_verdict_key_agreement.py; "
                f"both keys now carry it so a direct read of either cannot "
                f"republish a withdrawn verdict."
            )
            fixed.append(f['path'])
        with open(STATE, 'w', encoding='utf-8') as fh:
            json.dump(state, fh, indent=2)

    result = {
        'audit': 'verdict_key_agreement',
        'run_date': date.today().isoformat(),
        'records_examined': sum(key_census.values()),
        'verdict_key_shapes': key_census,
        'findings': findings,
        'fixed': fixed,
    }
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(result, fh, indent=2)

    print(f'  Records examined: {result["records_examined"]}')
    print(f'  Verdict-key shapes: {key_census}')
    print(f'  Report: {os.path.relpath(REPORT, os.path.dirname(BASE))}')

    if fixed:
        print(f'\n  [FIXED] normalised {len(fixed)} record(s): {", ".join(fixed)}')
    remaining = [f for f in findings if f['path'] not in fixed]

    if not remaining:
        print('\n  [OK] no stored record asserts two different verdicts about '
              'the same proposition.')
        return 0

    dis = [f for f in remaining if f['kind'] == 'VERDICT_DISAGREEMENT']
    scope = [f for f in remaining if f['kind'] == 'VERDICT_SCOPE_MISMATCH']

    if dis:
        print(f'\n  [FAIL] {len(dis)} record(s) contradict themselves:')
        for f in dis:
            print(f'\n   {f["store"]}[{f["path"]}]')
            for k, v in f['verdicts'].items():
                print(f'     {k}: {v}')
            print(f'     -> conservative resolution: {f["conservative_resolution"]}')
        print('\n  Which verdict a reader gets should not depend on which key a')
        print('  consumer happens to read. Re-run with --fix.')

    if scope:
        print(f'\n  [HOLD] {len(scope)} record(s) carry a SCOPED verdict '
              f'(not auto-resolvable):')
        for f in scope:
            print(f'\n   {f["store"]}[{f["path"]}]')
            for k, v in f['verdicts'].items():
                mark = '  <- outside the standard vocabulary' \
                    if k in f['off_vocabulary'] else ''
                print(f'     {k}: {v}{mark}')
            print('     -> two propositions, not two answers. Needs a human.')

    return 1 if dis else 0


if __name__ == '__main__':
    sys.exit(main())
