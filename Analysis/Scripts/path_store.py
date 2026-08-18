#!/usr/bin/env python3
"""
Canonical research-path store.

WHY THIS EXISTS
---------------
Path validation status was historically kept in THREE places that drifted apart:

  1. agent_state.json -> state['paths']            (75 keys, schema A)
  2. agent_state.json -> state['validated_paths']  (75 keys, schema B)
  3. validated_research_paths.json -> ['paths']    (27 keys, schema C, different key spelling)

On 2026-08-16 the work-queue generator read store (2) alone and emitted six false
"NEVER-VALIDATED" work items for paths that had been validated months earlier.
The stores were hand-reconciled on 2026-08-17 -- and by 2026-08-18 they had
ALREADY re-diverged in 8 places, because the reconciliation was a one-off patch
and nothing owned the merge rule.

This module owns the merge rule. Anything that needs to know a path's validation
status must call resolve_paths() rather than reading a store directly.

MERGE RULE (deterministic, auditable)
-------------------------------------
1. KEY NORMALISATION. "NLRP3_inflammasome -> inflammation", "NLRP3_inflammasome_inflammation"
   and "dapagliflozin_to_inflammation" are the same path. Keys are folded to a
   canonical form (lowercase, arrow/underscore/`_to_` collapsed) before merging.

2. RECENCY WINS. Each record's effective date is the MAXIMUM of every
   ISO-8601-looking date found anywhere in it (validated_date, validation_date,
   date, last_reaffirmed, next_revalidation_due is excluded as it is a FUTURE
   date, plus dated key names such as `reaffirm_note_2026-08-05`). The record
   with the latest effective date supplies the status. This is what a human
   reconciler does by hand; encoding it stops the drift.

3. CONSERVATIVE TIE-BREAK. If effective dates tie, the WEAKER claim wins.
   A merge must never silently upgrade a research claim. Ordering:
     EXTRACTION_ARTIFACT < CONTRADICTED < UNVALIDATED < NEEDS_RECHECK
     < PARTIALLY_VALIDATED < VALIDATED

4. NOTHING IS DISCARDED. The canonical record keeps `sources` -- every store
   that held an opinion, its status and its effective date -- so any resolution
   can be re-derived and challenged later.

Run directly to write Analysis/Results/canonical_paths.json and print a
divergence report.
"""
import json
import os
import re
from datetime import datetime, date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RESULTS = os.path.join(BASE_DIR, 'Analysis', 'Results')

STATE_FILE = os.path.join(RESULTS, 'agent_state.json')
VRP_FILE = os.path.join(RESULTS, 'validated_research_paths.json')
RP_FILE = os.path.join(RESULTS, 'research_paths.json')
CANONICAL_FILE = os.path.join(RESULTS, 'canonical_paths.json')

# Lower index == weaker claim == wins a date tie.
STATUS_RANK = [
    'EXTRACTION_ARTIFACT',
    'CONTRADICTED',
    'UNVALIDATED',
    'NEEDS_RECHECK',
    'PARTIALLY_VALIDATED',
    'VALIDATED',
]

DATE_RE = re.compile(r'(20\d{2}-\d{2}-\d{2})')
# Future-dated fields are scheduling metadata, not evidence of recency.
DATE_FIELD_BLOCKLIST = {'next_revalidation_due', 'next_due', 'due', 'next_audit'}


def rank(status):
    """Conservatism rank of a status string. Unknown/variant statuses map to
    their nearest known prefix (e.g. CONTRADICTED_FOR_DIABETIC_NEPHROPATHY)."""
    if not status:
        return len(STATUS_RANK)
    s = str(status).upper()
    if s in STATUS_RANK:
        return STATUS_RANK.index(s)
    for i, known in enumerate(STATUS_RANK):
        if s.startswith(known):
            return i
    return len(STATUS_RANK)


def normalise_key(key):
    """Fold the three key spellings onto one canonical form."""
    k = str(key).strip()
    k = k.replace('->', '_to_')
    k = re.sub(r'\s+', '_', k)
    k = re.sub(r'_+', '_', k)
    k = k.lower().strip('_')
    # `a_to_b` and `a_b` are the same edge; collapse the connector last so that
    # both spellings land on the same bucket.
    k = k.replace('_to_', '_')
    return k


def effective_date(record):
    """Latest ISO date appearing anywhere in the record (values AND key names),
    excluding forward-looking scheduling fields. Returns a date or None."""
    found = []

    def walk(obj, parent_key=None):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in DATE_FIELD_BLOCKLIST:
                    continue
                for m in DATE_RE.findall(str(k)):
                    found.append(m)
                walk(v, k)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, parent_key)
        else:
            if parent_key in DATE_FIELD_BLOCKLIST:
                return
            for m in DATE_RE.findall(str(obj)):
                found.append(m)

    walk(record)
    parsed = []
    for f in found:
        try:
            parsed.append(datetime.strptime(f, '%Y-%m-%d').date())
        except ValueError:
            continue
    # Ignore dates in the future: they are schedules, not observations.
    today = date.today()
    parsed = [p for p in parsed if p <= today]
    return max(parsed) if parsed else None


def status_of(record):
    """Extract the status a record asserts. `status` and `rating` are used
    interchangeably across the three schemas; prefer the weaker of the two if
    a single record disagrees with itself."""
    cands = [record.get('status'), record.get('rating'),
             record.get('validation_status')]
    cands = [c for c in cands if c]
    if not cands:
        return None
    return min(cands, key=rank)


def _load(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def collect_sources():
    """Return {canonical_key: [source_record, ...]} across all three stores."""
    state = _load(STATE_FILE)
    vrp = _load(VRP_FILE)
    rp = _load(RP_FILE)

    stores = [
        ('state.paths', state.get('paths', {})),
        ('state.validated_paths', state.get('validated_paths', {})),
        ('validated_research_paths.json', vrp.get('paths', {})),
        ('research_paths.json', rp.get('paths', {})),
    ]

    buckets = {}
    for store_name, store in stores:
        if not isinstance(store, dict):
            continue
        for raw_key, record in store.items():
            if not isinstance(record, dict):
                continue
            ck = normalise_key(raw_key)
            buckets.setdefault(ck, []).append({
                'store': store_name,
                'raw_key': raw_key,
                'status': status_of(record),
                'effective_date': effective_date(record),
                'data_point_count': record.get('data_point_count')
                                    or record.get('corpus_dpc'),
                'record': record,
            })
    return buckets


def resolve_paths():
    """Apply the merge rule. Returns {canonical_key: resolved_record}."""
    buckets = collect_sources()
    resolved = {}

    for ck, srcs in buckets.items():
        opinions = [s for s in srcs if s['status']]
        if not opinions:
            winner = srcs[0]
            divergent = False
        else:
            # Recency first; conservative tie-break second.
            winner = sorted(
                opinions,
                key=lambda s: (
                    -(s['effective_date'].toordinal() if s['effective_date'] else 0),
                    rank(s['status']),
                ),
            )[0]
            divergent = len({s['status'] for s in opinions}) > 1

        # Prefer the most specific display name we saw (arrow form reads best).
        display = sorted({s['raw_key'] for s in srcs},
                         key=lambda k: (0 if '->' in k else 1, -len(k)))[0]

        dpcs = [s['data_point_count'] for s in srcs
                if isinstance(s['data_point_count'], int)]

        resolved[ck] = {
            'display_key': display,
            'status': winner['status'],
            'resolved_from': winner['store'],
            'effective_date': winner['effective_date'].isoformat()
                              if winner['effective_date'] else None,
            'data_point_count': max(dpcs) if dpcs else 0,
            'divergent': divergent,
            'sources': [
                {
                    'store': s['store'],
                    'raw_key': s['raw_key'],
                    'status': s['status'],
                    'effective_date': s['effective_date'].isoformat()
                                      if s['effective_date'] else None,
                }
                for s in srcs
            ],
        }
    return resolved


def needs_validation(resolved=None, stale_days=120):
    """Paths a work-queue generator should legitimately re-raise.

    A path qualifies if it has NEVER been validated, OR its resolution is
    divergent across stores, OR its evidence is older than `stale_days`.
    Crucially it does NOT re-raise a path merely because one store forgot it --
    that was the 2026-08-16 false-positive bug.
    """
    if resolved is None:
        resolved = resolve_paths()
    today = date.today()
    out = []
    for ck, rec in resolved.items():
        reasons = []
        if not rec['status'] or rec['status'].upper() in ('UNVALIDATED', 'NEEDS_RECHECK'):
            reasons.append('never validated')
        if rec['divergent']:
            statuses = sorted({s['status'] for s in rec['sources'] if s['status']})
            reasons.append('stores disagree: ' + ' vs '.join(statuses))
        if rec['effective_date']:
            age = (today - datetime.strptime(rec['effective_date'], '%Y-%m-%d').date()).days
            if age > stale_days:
                reasons.append(f'stale {age}d')
        else:
            reasons.append('no date on any source')
        if reasons:
            out.append({'key': ck, 'display_key': rec['display_key'],
                        'status': rec['status'], 'reasons': reasons,
                        'data_point_count': rec['data_point_count']})
    out.sort(key=lambda x: -x['data_point_count'])
    return out


def write_canonical():
    resolved = resolve_paths()
    counts = {}
    for rec in resolved.values():
        counts[rec['status'] or 'UNKNOWN'] = counts.get(rec['status'] or 'UNKNOWN', 0) + 1
    payload = {
        'generated': datetime.now().isoformat(),
        'generator': 'Analysis/Scripts/path_store.py',
        'merge_rule': 'recency wins; conservative (weaker claim) tie-break; keys normalised across stores',
        'total_paths': len(resolved),
        'status_counts': counts,
        'divergent_count': sum(1 for r in resolved.values() if r['divergent']),
        'paths': resolved,
    }
    with open(CANONICAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return payload


def sync_validated_research_paths():
    """validated_research_paths.json hardcoded paths_validated=27 while the
    dashboard reported far more. Regenerate the count from the canonical store
    instead of trusting the literal."""
    if not os.path.exists(VRP_FILE):
        return None
    vrp = _load(VRP_FILE)
    resolved = resolve_paths()
    validated = sum(1 for r in resolved.values()
                    if r['status'] and r['status'].upper().startswith(('VALIDATED', 'PARTIALLY_VALIDATED')))
    old = vrp.get('paths_validated')
    vrp['paths_validated'] = validated
    vrp['paths_validated_note'] = (
        f'Regenerated from canonical_paths.json by path_store.py. Counts paths '
        f'resolved to VALIDATED or PARTIALLY_VALIDATED across all stores. '
        f'Previous hardcoded literal: {old}. This file itself still holds only '
        f'{len(vrp.get("paths", {}))} detailed records -- it is a subset view, '
        f'not the source of truth.'
    )
    vrp['paths_validated_regenerated'] = date.today().isoformat()
    with open(VRP_FILE, 'w', encoding='utf-8') as f:
        json.dump(vrp, f, indent=2, ensure_ascii=False)
    return {'old': old, 'new': validated}


def dedupe_state(dry_run=False):
    """Collapse duplicate spellings of the SAME edge inside agent_state.json.

    The 2026-08-17 "reconciliation to 75/75" hit its 75=75 target by MIRRORING
    entries between state['paths'] and state['validated_paths'] under the other
    store's key spelling, rather than merging them. Result: 8 edges exist twice
    in each store (e.g. `dapagliflozin -> T2D` and `dapagliflozin_T2D`), the
    counts agree, and the CONTENT diverges further with every run. True unique
    edge count is 68, not 75.

    This collapses each duplicate pair onto the arrow spelling, unioning the
    field content (winner's status, superset of everything else) so no evidence
    is lost.
    """
    state = _load(STATE_FILE)
    if not state:
        return None
    resolved = resolve_paths()
    report = {'merged': [], 'before': {}, 'after': {}}

    for store_name in ('paths', 'validated_paths'):
        store = state.get(store_name, {})
        report['before'][store_name] = len(store)
        groups = {}
        for raw_key in list(store):
            groups.setdefault(normalise_key(raw_key), []).append(raw_key)

        for ck, raw_keys in groups.items():
            if len(raw_keys) < 2:
                continue
            # Canonical display spelling: prefer the arrow form.
            keep = sorted(raw_keys, key=lambda k: (0 if '->' in k else 1, -len(k)))[0]
            merged = {}
            # Oldest first so newer fields overwrite older ones.
            for k in sorted(raw_keys,
                            key=lambda k: (effective_date(store[k]) or date.min)):
                rec = store[k]
                if isinstance(rec, dict):
                    merged.update(rec)
            # Status comes from the canonical resolution, not from field order.
            canon = resolved.get(ck)
            if canon and canon['status']:
                merged['status'] = canon['status']
                if 'rating' in merged:
                    merged['rating'] = canon['status']
            merged['merged_from'] = raw_keys
            merged['merged_on'] = date.today().isoformat()
            merged['merge_note'] = (
                'Duplicate key spellings of one edge, created by the 2026-08-17 '
                'mirror-reconciliation. Collapsed by path_store.dedupe_state(); '
                'status set by the canonical merge rule (recency, conservative tie-break).'
            )
            if not dry_run:
                for k in raw_keys:
                    store.pop(k, None)
                store[keep] = merged
            report['merged'].append({'store': store_name, 'kept': keep,
                                     'dropped': [k for k in raw_keys if k != keep],
                                     'status': merged.get('status')})
        report['after'][store_name] = len(store)

    if not dry_run:
        state['last_updated'] = datetime.now().isoformat()
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    return report


def main():
    import sys
    if '--dedupe' in sys.argv:
        rep = dedupe_state(dry_run='--dry-run' in sys.argv)
        print('=' * 64)
        print('  STATE DEDUPE' + ('  (DRY RUN)' if '--dry-run' in sys.argv else ''))
        print('=' * 64)
        for store in ('paths', 'validated_paths'):
            print(f"  state['{store}']: {rep['before'][store]} -> {rep['after'][store]}")
        for m in rep['merged']:
            print(f"    {m['store']}: kept {m['kept']!r}  dropped {m['dropped']}  -> {m['status']}")
        print()

    payload = write_canonical()
    print('=' * 64)
    print('  CANONICAL PATH STORE')
    print('=' * 64)
    print(f"  Paths after key normalisation : {payload['total_paths']}")
    print(f"  Divergent across stores       : {payload['divergent_count']}")
    print('  Status counts:')
    for k, v in sorted(payload['status_counts'].items(), key=lambda x: -x[1]):
        print(f'    {v:>4}  {k}')

    div = [r for r in payload['paths'].values() if r['divergent']]
    if div:
        print('\n  DIVERGENCES RESOLVED THIS RUN:')
        for r in sorted(div, key=lambda x: x['display_key']):
            print(f"    {r['display_key']}")
            print(f"      -> {r['status']}  (from {r['resolved_from']}, {r['effective_date']})")
            for s in r['sources']:
                if s['status']:
                    print(f"         {s['store']:<32} {s['status']:<22} {s['effective_date']}")

    sync = sync_validated_research_paths()
    if sync:
        print(f"\n  validated_research_paths.json paths_validated: {sync['old']} -> {sync['new']}")

    nv = needs_validation(payload['paths'])
    print(f"\n  Paths a work-queue generator should raise: {len(nv)}")
    for item in nv[:10]:
        print(f"    [{item['data_point_count']:>4} dp] {item['display_key']}: {'; '.join(item['reasons'])}")

    print(f"\n  Written: {CANONICAL_FILE}")
    print('  [OK] path_store')


if __name__ == '__main__':
    main()
