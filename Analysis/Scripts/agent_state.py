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
from datetime import datetime

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

    # Load validated research paths
    vp_path = os.path.join(base_dir, 'Analysis', 'Results', 'validated_research_paths.json')
    if os.path.exists(vp_path):
        with open(vp_path, encoding='utf-8') as f:
            vp = json.load(f)
        for key, path in vp.get('paths', {}).items():
            state['paths'][key] = {
                'status': path.get('status', 'UNVALIDATED'),
                'validated_date': '2026-03-20',
                'data_point_count': path.get('data_point_count', 0),
                'last_data_point_count': path.get('data_point_count', 0),
                'external_pmids': path.get('external_pmids', []),
            }

    # Load research paths (includes unvalidated ones)
    rp_path = os.path.join(base_dir, 'Analysis', 'Results', 'research_paths.json')
    if os.path.exists(rp_path):
        with open(rp_path, encoding='utf-8') as f:
            rp = json.load(f)
        for key, path in rp.get('paths', {}).items():
            if key not in state['paths']:
                state['paths'][key] = {
                    'status': 'UNVALIDATED',
                    'validated_date': None,
                    'data_point_count': path.get('data_point_count', 0),
                    'last_data_point_count': 0,
                    'external_pmids': [],
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
    unvalidated_paths = [k for k, v in state['paths'].items() if v['status'] == 'UNVALIDATED']

    state['work_queue'].append({
        'type': 'vet_papers_batch',
        'target': f'{unvetted_count} unvetted papers',
        'priority': 2,
        'reason': 'Initial state — papers have not been individually vetted for PMID accuracy and claim validity',
        'added': datetime.now().isoformat(),
    })

    for path_key in unvalidated_paths[:10]:
        state['work_queue'].append({
            'type': 'validate_path',
            'target': path_key,
            'priority': 3,
            'reason': 'Unvalidated research path — needs cross-validation against PubMed',
            'added': datetime.now().isoformat(),
        })

    for gap_num in [13, 14, 15]:
        state['work_queue'].append({
            'type': 'audit_gap',
            'target': f'Gap {gap_num}',
            'priority': 4,
            'reason': f'BRONZE gap — check for new evidence that could support SILVER promotion',
            'added': datetime.now().isoformat(),
        })

    state['work_queue'].append({
        'type': 'search_pubmed',
        'target': 'oxidative stress combination therapy diabetes',
        'priority': 1,
        'reason': 'Highest-priority hub finding — search for new combination therapy evidence',
        'added': datetime.now().isoformat(),
    })

    save_state(state)
    return state


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
