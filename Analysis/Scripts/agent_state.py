#!/usr/bin/env python3
"""
Agent State Manager for the Diabetes Research Hub automated iteration loop.

Maintains persistent state about:
- Which papers have been fully vetted (PMID verified, claims checked)
- Which research paths have been validated and when
- Which gaps were last audited and their evidence status
- What the agent checked on its last run
- A queue of items that still need attention

This prevents the agent from repeating stale work and ensures
comprehensive coverage over time.
"""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import path_store  # canonical path resolution; see path_store.py docstring

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
STATE_FILE = os.path.join(base_dir, 'Analysis', 'Results', 'agent_state.json')


def load_state():
    """Load the current agent state, or create a fresh one."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding='utf-8') as f:
            return json.load(f)
    return create_initial_state()


def save_state(state):
    """Save the current agent state."""
    state['last_updated'] = datetime.now().isoformat()
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Weekly PubMed sweep queries — THE authoritative list.
#
# Retired 2026-08-18: "oxidative stress diabetes combination". On 2026-08-17 it
# returned 8 of 8 off-topic hits (hydrogels, cryogels, donkey-blood peptide,
# Carica papaya, a bariatric surgery review) and was traced as the intake path
# for the 13 off-topic FLAGGED papers already in the corpus. Bare keyword AND
# has no field qualifiers, so "combination" matched materials-science papers
# that merely mention diabetic wound healing.
#
# Replacement rule for every query in this list:
#   1. Qualify fields ([tiab], [mh]) so terms cannot match a stray sentence.
#   2. Bind the diabetes context explicitly — never rely on one loose keyword.
#   3. Constrain the design (randomized/trial/cohort) or the species (humans).
# ---------------------------------------------------------------------------
SWEEP_QUERIES = [
    {
        'key': 'oxidative_stress_combination',
        'query': ('("oxidative stress"[tiab] OR "reactive oxygen species"[tiab]) '
                  'AND ("diabetes mellitus, type 1"[mh] OR "diabetes mellitus, type 2"[mh]) '
                  'AND (randomized controlled trial[pt] OR clinical trial[pt] '
                  'OR meta-analysis[pt] OR systematic review[pt]) '
                  'AND humans[mh]'),
        'priority': 2,
        'rationale': ('Combination/antioxidant therapy evidence in diabetes. Replaces the '
                      'retired bare-keyword query that produced 8/8 off-topic hits on 2026-08-17.'),
        'retired_predecessor': 'oxidative stress diabetes combination',
        'replaced_on': '2026-08-18',
    },
    {
        'key': 'lada',
        'query': ('("latent autoimmune diabetes"[tiab] OR LADA[tiab]) '
                  'AND (adult*[tiab] OR humans[mh])'),
        'priority': 1,
        'rationale': 'Core hub topic (Gaps #1, #8, #10, #14).',
    },
    {
        'key': 'islet_transplant_outcomes',
        'query': ('("islet transplantation"[mh] OR "islet transplant"[tiab]) '
                  'AND (outcome*[tiab] OR graft survival[tiab] OR insulin independence[tiab]) '
                  'AND humans[mh]'),
        'priority': 1,
        'rationale': 'Gap #3 (GOLD) and Gap #11 (BRONZE, 2026-09-30 owner ruling; SILVER from 2026-09-08) depend on current outcome data.',
    },
    {
        'key': 'nlrp3_dkd',
        'query': ('("NLRP3"[tiab] OR inflammasome*[tiab]) '
                  'AND ("diabetic nephropathies"[mh] OR "diabetic kidney disease"[tiab])'),
        'priority': 2,
        'rationale': ('Watch for the missing link between NLRP3 suppression and RENAL HARD '
                      'ENDPOINTS. Best human data (32358544) is a surrogate biomarker RCT.'),
    },
    {
        'key': 'drug_repurposing',
        'query': ('("drug repositioning"[mh] OR "drug repurposing"[tiab]) '
                  'AND ("diabetes mellitus"[mh]) AND humans[mh]'),
        'priority': 2,
        'rationale': 'Gaps #4, #7, #12 (generic-drug repurposing arm).',
    },
    {
        'key': 'verapamil_t1d',
        'query': 'verapamil[tiab] AND ("diabetes mellitus, type 1"[mh] OR beta cell*[tiab])',
        'priority': 2,
        'rationale': 'Active path verapamil -> T1D; beta-cell preservation trials.',
    },
    {
        'key': 'sglt2_colchicine_combination',
        'query': ('(dapagliflozin[tiab] OR colchicine[tiab]) AND ("diabetes mellitus"[mh]) '
                  'AND (combination[tiab] OR add-on[tiab] OR adjunct*[tiab]) AND humans[mh]'),
        'priority': 3,
        'rationale': 'Tracked combination; no clinical evidence found to date.',
    },
]


def get_sweep_queries(min_priority=5):
    """The queries a weekly sweep should run, highest priority first."""
    return sorted([q for q in SWEEP_QUERIES if q.get('priority', 5) <= min_priority],
                  key=lambda q: q.get('priority', 5))


def create_initial_state():
    """Create the initial state from the current project."""
    state = {
        'version': 1,
        'created': datetime.now().isoformat(),
        'last_updated': datetime.now().isoformat(),
        'last_run': None,

        # Track paper vetting status
        'papers': {
            # pmid: {
            #   'status': 'VETTED' | 'UNVETTED' | 'FLAGGED',
            #   'vetted_date': iso_date,
            #   'pmid_verified': True/False,
            #   'claims_checked': True/False,
            #   'issues_found': [],
            #   'last_checked': iso_date,
            # }
        },

        # Track research path validation
        'paths': {
            # path_key: {
            #   'status': 'VALIDATED' | 'PARTIALLY_VALIDATED' | 'UNVALIDATED' | 'NEEDS_RECHECK',
            #   'validated_date': iso_date,
            #   'data_point_count': N,
            #   'last_data_point_count': N,  # detect changes
            #   'external_pmids': [],
            # }
        },

        # Track gap audit status
        'gaps': {
            # gap_num: {
            #   'tier': 'GOLD'|'SILVER'|'BRONZE'|'EXPLORATORY',
            #   'last_audited': iso_date,
            #   'corpus_evidence_points': N,
            #   'credibility_issues': [],
            #   'promotion_candidate': True/False,
            # }
        },

        # Work queue — items the agent should tackle next
        'work_queue': [],
        # Format: { 'type': 'vet_paper'|'validate_path'|'audit_gap'|'check_combination'|'search_pubmed',
        #           'target': identifier,
        #           'priority': 1-5 (1=highest),
        #           'reason': why this needs attention,
        #           'added': iso_date }

        # Run history
        'run_history': [],
        # Format: { 'date': iso_date, 'papers_checked': N, 'paths_validated': N,
        #           'issues_found': N, 'changes_pushed': True/False, 'summary': text }
    }
    return state


def initialize_from_project():
    """Scan the project and build initial state from existing data."""
    state = create_initial_state()

    # Load paper index
    index_path = os.path.join(base_dir, 'Analysis', 'Results', 'paper_library', 'index.json')
    if os.path.exists(index_path):
        with open(index_path, encoding='utf-8') as f:
            index = json.load(f)
        for pmid, meta in index.get('papers', {}).items():
            state['papers'][pmid] = {
                'status': 'UNVETTED',  # Mark all as unvetted initially
                'vetted_date': None,
                'pmid_verified': False,
                'claims_checked': False,
                'issues_found': [],
                'last_checked': None,
                'title': meta.get('title', '')[:80],
                'year': meta.get('year', '?'),
            }

    # Load paths from the CANONICAL store, never from a single raw store.
    # Reading one store directly is what produced six false "NEVER-VALIDATED"
    # work items on 2026-08-16 for paths validated months earlier.
    for key, rec in path_store.resolve_paths().items():
        state['paths'][rec['display_key']] = {
            'status': rec['status'] or 'UNVALIDATED',
            'validated_date': rec['effective_date'],
            'data_point_count': rec['data_point_count'],
            'last_data_point_count': rec['data_point_count'],
            'external_pmids': [],
            'canonical_key': key,
            'resolved_from': rec['resolved_from'],
        }

    # Initialize gap tracking
    gap_tiers = {
        1: 'SILVER', 2: 'GOLD', 3: 'GOLD', 4: 'SILVER', 5: 'SILVER',
        6: 'GOLD', 7: 'SILVER', 8: 'SILVER', 9: 'EXPLORATORY', 10: 'SILVER',
        11: 'GOLD', 12: 'SILVER', 13: 'BRONZE', 14: 'BRONZE', 15: 'BRONZE',
    }
    for gap_num, tier in gap_tiers.items():
        state['gaps'][str(gap_num)] = {
            'tier': tier,
            'last_audited': '2026-03-20',
            'corpus_evidence_points': 0,
            'credibility_issues': [],
            'promotion_candidate': tier == 'BRONZE',
        }

    # Build initial work queue — prioritize unvetted papers and unvalidated paths
    unvetted_count = sum(1 for p in state['papers'].values() if p['status'] == 'UNVETTED')

    state['work_queue'].append({
        'type': 'vet_papers_batch',
        'target': f'{unvetted_count} unvetted papers',
        'priority': 2,
        'reason': 'Initial state — papers have not been individually vetted for PMID accuracy and claim validity',
        'added': datetime.now().isoformat(),
    })

    state['work_queue'].extend(generate_path_work_items(limit=10))

    for gap_num in [13, 14, 15]:
        state['work_queue'].append({
            'type': 'audit_gap',
            'target': f'Gap {gap_num}',
            'priority': 4,
            'reason': f'BRONZE gap — check for new evidence that could support SILVER promotion',
            'added': datetime.now().isoformat(),
        })

    for q in SWEEP_QUERIES:
        if q.get('priority', 5) <= 2:
            state['work_queue'].append({
                'type': 'search_pubmed',
                'target': q['query'],
                'priority': q['priority'],
                'reason': q['rationale'],
                'added': datetime.now().isoformat(),
            })

    save_state(state)
    return state


def generate_path_work_items(limit=10, stale_days=120):
    """Emit validate_path work items from the CANONICAL path store.

    This is the fix for the 2026-08-16 false-positive incident. The old
    generator listed every path whose status was 'UNVALIDATED' in whichever
    single store it happened to read, so a path validated in store B but absent
    from store A was re-raised as "never validated". path_store.needs_validation()
    resolves all stores first and only raises a path for a stated, checkable
    reason: genuinely never validated, stores disagree, or evidence gone stale.
    """
    items = []
    for cand in path_store.needs_validation(stale_days=stale_days)[:limit]:
        reasons = cand['reasons']
        # Store disagreement is a data-integrity problem: outrank staleness.
        priority = 2 if any(r.startswith('stores disagree') for r in reasons) else 3
        items.append({
            'type': 'validate_path',
            'target': cand['display_key'],
            'priority': priority,
            'reason': '; '.join(reasons) + f" (status={cand['status']}, "
                      f"{cand['data_point_count']} data points)",
            'added': datetime.now().strftime('%Y-%m-%d'),
            'source': 'path_store.needs_validation',
        })
    return items


def refresh_path_queue(state, limit=10, stale_days=120):
    """Replace auto-generated validate_path items with a freshly resolved set,
    leaving hand-written queue items untouched."""
    kept = [i for i in state.get('work_queue', [])
            if i.get('source') != 'path_store.needs_validation']
    new = generate_path_work_items(limit=limit, stale_days=stale_days)
    existing_targets = {i.get('target') for i in kept if i.get('type') == 'validate_path'}
    new = [i for i in new if i['target'] not in existing_targets]
    state['work_queue'] = kept + new
    return new


def get_next_work_items(state, n=5):
    """Get the next N highest-priority items from the work queue."""
    queue = sorted(state.get('work_queue', []), key=lambda x: x.get('priority', 5))
    return queue[:n]


def mark_paper_vetted(state, pmid, issues=None):
    """Mark a paper as vetted."""
    if pmid in state['papers']:
        state['papers'][pmid]['status'] = 'FLAGGED' if issues else 'VETTED'
        state['papers'][pmid]['vetted_date'] = datetime.now().isoformat()
        state['papers'][pmid]['pmid_verified'] = True
        state['papers'][pmid]['claims_checked'] = True
        state['papers'][pmid]['issues_found'] = issues or []
        state['papers'][pmid]['last_checked'] = datetime.now().isoformat()


def record_run(state, summary, papers_checked=0, paths_validated=0, issues_found=0, pushed=False):
    """Record a completed run."""
    state['run_history'].append({
        'date': datetime.now().isoformat(),
        'papers_checked': papers_checked,
        'paths_validated': paths_validated,
        'issues_found': issues_found,
        'changes_pushed': pushed,
        'summary': summary,
    })
    state['last_run'] = datetime.now().isoformat()
    # Keep last 30 runs
    state['run_history'] = state['run_history'][-30:]


if __name__ == '__main__':
    print("Initializing agent state from current project...")
    state = initialize_from_project()
    print(f"  Papers tracked: {len(state['papers'])}")
    print(f"  Research paths tracked: {len(state['paths'])}")
    print(f"  Gaps tracked: {len(state['gaps'])}")
    print(f"  Work queue items: {len(state['work_queue'])}")
    print(f"\n  Next work items:")
    for item in get_next_work_items(state):
        print(f"    [{item['priority']}] {item['type']}: {item['target']}")
    print(f"\n  State saved to: {STATE_FILE}")
