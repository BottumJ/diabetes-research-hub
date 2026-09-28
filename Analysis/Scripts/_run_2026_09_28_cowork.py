#!/usr/bin/env python3
"""Cowork cloud scheduled-task run, 2026-09-28.

Work done this run:
  - Verified push blocker unchanged (still no git credential in either
    sandbox; origin/main 125 commits behind local main before this run).
  - Ran credibility sweep (audit_impossible_pmids.py): clean, 0 flags.
  - Confirmed paper-vetting backlog is 0 UNVETTED (349 VETTED, 23 FLAGGED,
    1 VETTED_DO_NOT_INGEST) - nothing new to vet.
  - Worked the #1 work_queue item (gap_subject_coverage, 5 remaining
    findings). Two of the five are HIGH severity (Gap #7 GKA Drug
    Repurposing, Gap #13 Personalized Nutrition for Beta Cells) because
    their stored evidence covers only ONE axis of the claimed
    intersection with zero papers on the other axis at all - the
    audit's remedy for that severity is "re-found on a dated null
    search, or record that the gap has never been tested", not just an
    inline caveat. Ran that dated null search this run via live web
    search (not a repo PMID lookup) rather than re-deriving anything
    already answered by audit_gap_subject_coverage.py. Recorded the
    result in state.gap_audits so a future run does not repeat it.
  - Confirmed (by reading build_extracted_evidence.py, not assumed) that
    the caveat-surfacing wired in on 2026-09-27 is generic: it reads
    every finding out of gap_subject_coverage_audit.json by gap_id and
    renders severity/problem/remedy for ALL of them, including the two
    HIGH ones, with no per-gap-id special-casing needed. So no builder
    code change was required for the caveat text itself; the open gap
    was evidence, not wiring.
  - Did NOT attempt to manufacture a paper at either intersection -
    doctrine is no fabricated citations, and the null search found none.
"""
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_state as A

state = A.load_state()

# --- 1. Record dated null-search findings for the two HIGH-severity gaps ---
today = '2026-09-28'
ga = state.setdefault('gap_audits', {})

ga['7'] = ga.get('7', {})
ga['7'][today] = {
    'gap_title': 'GKA Drug Repurposing',
    'action': 'dated_null_search',
    'method': 'Live web search (not a repo/PubMed API lookup) for a paper '
              'at the intersection of glucokinase activators (GKA) and drug '
              'repurposing specifically.',
    'queries': ['glucokinase activator drug repurposing diabetes review'],
    'result': 'NULL. Search returns substantial GKA-for-T2D literature '
              '(dorzagliatin development/clinical reviews, mechanism '
              'reviews, "humbling lesson in drug development" retrospective) '
              'but nothing framing GKAs as repurposing candidates, and no '
              'paper on repurposing existing (non-GKA) drugs via the GKA '
              'mechanism either. Confirms audit_gap_subject_coverage.py: '
              'the 22 stored evidence papers are on-topic for "GKA" only, '
              'not for "repurposing". Consistent with the gap never having '
              'been directly tested rather than a corpus gap.',
    'sources': [
        'https://pubmed.ncbi.nlm.nih.gov/34714587/',
        'https://www.nature.com/articles/nrd2850',
        'https://onlinelibrary.wiley.com/doi/10.1111/1753-0407.13563',
        'https://diabetesjournals.org/diabetes/article/74/8/1339/162900/Glucokinase-Activators-A-Humbling-Lesson-in-Drug',
    ],
    'conclusion': 'Gap has never been directly tested at its own '
                  'intersection. Caveat text (wired 2026-09-27, confirmed '
                  'generic and live) is the correct treatment - do not '
                  'publish the current 22-paper list as support for '
                  '"repurposing". No further search needed unless new '
                  'GKA-repurposing literature is published.',
}

ga['13'] = ga.get('13', {})
ga['13'][today] = {
    'gap_title': 'Personalized Nutrition for Beta Cells',
    'action': 'dated_null_search',
    'method': 'Live web search for a paper at the intersection of '
              'personalized/precision nutrition and beta-cell function '
              'preservation.',
    'queries': ['personalized nutrition beta cell function type 1 diabetes preservation'],
    'result': 'NULL. Search returns beta-cell preservation literature '
              '(immune interventions, early intensive therapy, general '
              'bioactive-food-component reviews) but nothing that frames '
              'nutrition specifically as PERSONALIZED/precision-tailored '
              'in relation to beta-cell preservation outcomes. Confirms '
              'audit_gap_subject_coverage.py: the 4 stored evidence papers '
              'are on-topic for "beta cell" only, not "personalized '
              'nutrition".',
    'sources': [
        'https://pmc.ncbi.nlm.nih.gov/articles/PMC4732932/',
        'https://pmc.ncbi.nlm.nih.gov/articles/PMC4116378/',
        'https://www.mdpi.com/2072-6643/16/21/3639',
    ],
    'conclusion': 'Gap has never been directly tested at its own '
                  'intersection (consistent with its EXPLORATORY tier, '
                  'not SILVER/BRONZE, so no downstream claim currently '
                  'overstates it). Caveat text is the correct treatment. '
                  'No further search needed unless new personalized-'
                  'nutrition-and-beta-cell literature is published.',
}

# --- 2. Update the standing priority-1 work_queue item with today's progress ---
for item in state.get('work_queue', []):
    if item.get('type') == 'audit_gap' and item.get('added') == '2026-09-26' \
            and 'gap_subject_coverage_audit.json' in (item.get('target') or ''):
        item['progress_2026_09_28'] = (
            'Findings held at 5 (unchanged from 2026-09-27 close - no new '
            'coverage regressed or improved). Ran the two outstanding dated '
            'null searches the HIGH-severity findings (#7 GKA Drug '
            'Repurposing, #13 Personalized Nutrition for Beta Cells) '
            'required per their own remedy text ("re-found on a dated null '
            'search, or record that the gap has never been tested") - both '
            'came back null; see state.gap_audits["7"]["2026-09-28"] and '
            '["13"]["2026-09-28"] for method, queries and sources. Also '
            'verified by reading build_extracted_evidence.py (not assumed) '
            'that the 2026-09-27 caveat wiring is generic over all findings '
            'in gap_subject_coverage_audit.json, so no further code change '
            'was needed for the caveat text on any of the 5. Remaining 3 '
            'MEDIUM findings (#1, #4, #11: inference-only intersections, '
            'each axis separately supported) are lower-severity by the '
            'audit\'s own scale and still carry the generic inline caveat; '
            'did not run dated null searches for those this run - next run '
            'should, to fully close out the finding list rather than leave '
            'it perpetually at "caveated, not resolved".'
        )
        break

# --- 3. Append today's run_history entry ---
rh = state.setdefault('run_history', [])
rh.append({
    'date': today,
    'environment': 'Cowork cloud scheduled task (not the local Windows '
                   'sandbox). Device bridge to the OneDrive-mounted folder '
                   'worked on first attempt.',
    'papers_checked': 0,
    'papers_added': 0,
    'paths_validated': 0,
    'gaps_audited': 2,
    'gap_subject_coverage_findings': '5 (unchanged) - both HIGH-severity '
                                       'findings dated-null-searched this '
                                       'run; 3 MEDIUM findings still open '
                                       'for a future run',
    'gates_fixed': 0,
    'credibility_sweep': 'clean - 0 impossible PMIDs (ceiling 43,017,983), '
                          '0 unhedged preclinical overclaims',
    'changes_pushed': False,
    'push_blocker': 'UNCHANGED: origin/main 125 commits behind local before '
                     'this run (re-verified: git push origin main --dry-run '
                     '-> "could not read Username for \'https://github.com\'" '
                     '- no credential.helper, no GH_TOKEN, no PAT. This has '
                     'been priority-0 since 2026-09-16 (queue item dated '
                     '2026-09-14/16) with no human action taken across 12+ '
                     'daily runs. Last user notification sent 2026-09-26; '
                     'none sent 2026-09-27. Notifying again this run given '
                     'the blocker duration.',
    'agent': 'cowork-cloud-scheduled-task',
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'summary': 'Verified environment healthy end-to-end (device bridge, git '
               'read/local-commit, live web search). Credibility sweep '
               'clean. Paper-vetting backlog confirmed at 0. Worked the '
               'standing #1 queue item: ran the two dated null searches its '
               'HIGH-severity findings required, recorded them in '
               'gap_audits so they are not repeated, and confirmed (by '
               'reading source, not assuming) that yesterday\'s caveat '
               'wiring already covers them generically. Did not fabricate '
               'or force a citation at either unsupported intersection. '
               'Re-escalated the unchanged 12-day-old push-credential '
               'blocker via notification, since it is the only item in the '
               'queue no amount of further agent work can close.',
})

A.save_state(state)
print('State updated. papers:', len(state.get('papers', {})),
      'work_queue:', len(state.get('work_queue', [])),
      'run_history:', len(state.get('run_history', [])))
