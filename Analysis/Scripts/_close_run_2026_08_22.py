#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close out the 2026-08-22 iteration: record findings, reprioritize the queue.

Run summary
-----------
Worked P1 item "AUDIT THE OTHER 8 EXTRACTORS FOR THE UNBOUNDED-WILDCARD
DEFECT" (2026-08-21) and P2 item "SWEEP FOR BASELINE/DESIGN PAPERS CITED AS
OUTCOME EVIDENCE" (2026-08-21). Both were confirmed, both are now gated, and
the corpus headline fell 292 -> 240.
"""

import json
import os
import shutil
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
STATE = os.path.join(RESULTS, 'agent_state.json')
TODAY = '2026-08-22'

shutil.copy(STATE, os.path.join(RESULTS, f'agent_state.json.bak_{TODAY}'))
with open(STATE, encoding='utf-8') as f:
    state = json.load(f)

# ---------------------------------------------------------------------------
# 1. Close completed queue items
# ---------------------------------------------------------------------------
CLOSED_MARKERS = [
    'AUDIT THE OTHER 8 EXTRACTORS',
    'SWEEP FOR BASELINE/DESIGN PAPERS',
    'THE PUBLISHED CORPUS HEADLINE IS NOW 292',
]
queue = state.get('work_queue', [])
kept, closed = [], []
for item in queue:
    target = item.get('target', '')
    if any(m in target for m in CLOSED_MARKERS):
        closed.append(target[:70])
        continue
    kept.append(item)

# ---------------------------------------------------------------------------
# 2. New items found this run
# ---------------------------------------------------------------------------
NEW_ITEMS = [
    {
        'priority': 1,
        'type': 'user_action_required',
        'added': TODAY,
        'target': (
            'HUMAN CALL: THE #2 AND #3 RESEARCH PATHS REST ENTIRELY ON A TRIAL '
            'PROTOCOL. `verapamil -> beta_cell` and `verapamil -> T1D` each cite '
            'exactly one corpus paper, PMID 39613428, whose title ends "protocol '
            'for a randomised, double-blind, placebo-controlled, parallel-group, '
            'multicentre trial" (Ver-A-T1D, BMJ Open 2024). Every one of their '
            'data points is a dose_response label - a PLANNED dose. A protocol '
            'reports no outcomes, so neither path has any corpus evidence that '
            'verapamil does anything. NOTE both retain real external validation '
            '(29988125, 36826844, 40111679 and others) and verapamil beta-cell '
            'preservation is a genuine finding in the literature - the claim is '
            'about the CORPUS, not about verapamil. Options: (a) delist both '
            'until Ver-A-T1D reports, (b) keep them as external-evidence-only '
            'hypotheses with no corpus count, (c) publish the protocol source '
            'explicitly on the card. Delisting two of the top three paths is not '
            'an unattended change, same reasoning as the 2026-08-20 dose-label '
            'item.'
        ),
    },
    {
        'priority': 2,
        'type': 'fix_pipeline',
        'added': TODAY,
        'target': (
            'DECIDE HOW DESIGN/PROTOCOL PAPERS SHOULD COUNT IN THE CORPUS. '
            'audit_baseline_citations.py (new this run) finds 3 corpus papers '
            'that are design or protocol publications, contributing 24 of 240 '
            'data points (10%): 39613428 Ver-A-T1D protocol (15), 36643381 '
            'colchicine hs-CRP protocol (7), 32862232 DAPA-CKD baseline '
            'characteristics (2). All 24 survivors are dose labels, which is '
            'defensible metadata - a protocol IS the right source for a planned '
            'dose. What is not defensible is counting them toward a headline '
            'that reads "data points extracted". Recommended: tag them '
            'source_type=DESIGN in the extraction output and report them '
            'separately, rather than dropping them. Interacts with the still-open '
            'dose_response headline question.'
        ),
    },
    {
        'priority': 2,
        'type': 'verify_citations',
        'added': TODAY,
        'target': (
            'EXTEND THE PROVENANCE GATE BEYOND THE 180-CHAR LOOKBACK. The new '
            'PROJECTED_NOT_MEASURED / ATTRIBUTED_TO_OTHER_STUDY rules in '
            'extract_corpus_data.py read only the 180 characters before a match, '
            'which is about one sentence plus its lead-in. That was enough to '
            'catch PMID 36643381 publishing a power-calculation assumption '
            '("we estimated that hs-CRP is suppressed to 3.22 mg/L") and another '
            'trial\'s result ("the previous report indicating that colchicine '
            '1 mg for 4 weeks reduced hs-CRP by about 60%") as its own findings. '
            'It will NOT catch attribution that opens a paragraph and governs '
            'several sentences. Better signal available: section_type. A number '
            'in INTRO or a rationale section is almost never a finding of the '
            'paper reporting it. Measure before applying - INTRO is also where '
            'some papers state their own headline result.'
        ),
    },
    {
        'priority': 3,
        'type': 'fix_pipeline',
        'added': TODAY,
        'target': (
            'REVIEW THE THREE REMISSION EXTRACTIONS THAT ARE RATIOS, NOT RATES. '
            'Surviving remission set includes "remission; every 1%", "remission '
            'by 2%" (PMID 40982327) and "remission could be no more than 1%" '
            '(37356446). These are per-percentage-point effect statements or '
            'upper bounds, not remission rates, so they are typed wrongly even '
            'though the number is real and the sentence is about remission. Low '
            'severity - 3 of 240 - but it is the residue of the 2026-08-22 '
            'bounding work and should not be forgotten.'
        ),
    },
]

# ---------------------------------------------------------------------------
# 3. Partially advance the "extend the topic screen" item
# ---------------------------------------------------------------------------
for item in kept:
    if 'EXTEND THE TOPIC SCREEN BEYOND external_pmids' in item.get('target', ''):
        item['target'] += (
            ' [2026-08-22 PARTIAL: the corpus arm of audit_baseline_citations.py '
            'now screens paper_stats titles, which is how the Ver-A-T1D protocol '
            'was found supplying 15 data points to two top-ranked paths. Still '
            'open: key_sources free-text PMIDs, extract_evidence.py gap evidence, '
            'and RELEVANCE (not just existence) of builder-literal PMIDs.]'
        )

state['work_queue'] = NEW_ITEMS + kept

# ---------------------------------------------------------------------------
# 4. Doctrine note
# ---------------------------------------------------------------------------
state.setdefault('doctrine_notes', {})[TODAY] = (
    'A regex is a claim about language and must be measured like one. The '
    'unbounded lazy wildcard `.*?` between a marker token and a capture group '
    'has now produced a majority-artifact extractor every single time it has '
    'been measured: inflammatory_markers 57% (2026-08-21), then survival_graft '
    '100%, c_peptide 100%, remission 71%, autoantibody 60%, hba1c_change 50% '
    '(2026-08-22). Five of those six were never measured until the day they '
    'were fixed, and four of them had been publishing to the dashboard for '
    'months. The lesson is not "wildcards are bad" - it is that a pattern which '
    'has never had its OUTPUT read is an untested claim, and this repository '
    'kept treating untested claims as evidence. Second lesson, from the same '
    'run: extract_corpus_data.py was not in run_quality_improvements.py at all, '
    'so a 47/47 green pipeline could be built entirely on stale extraction. A '
    'green check on a step that was never run is worse than a red one.'
)

# ---------------------------------------------------------------------------
# 5. Audit note
# ---------------------------------------------------------------------------
state.setdefault('audit_notes', []).append({
    'date': TODAY,
    'finding': 'Five extractors carried the unbounded-wildcard defect; corpus 292 -> 240.',
    'evidence': 'Analysis/Results/extractor_wildcard_audit.json',
    'artifact_rate_before': '18.2% (53/292)',
    'artifact_rate_after': '0.0% (0/240)',
    'control': ('inflammatory_markers, rewritten 2026-08-21, scored 0% under the '
                'same signature set that failed the other five - so the signal is '
                'the wildcard, not the audit.'),
    'per_type_before': {
        'survival_graft': '6/6 = 100%',
        'c_peptide': '5/5 = 100%',
        'remission': '34/48 = 71%',
        'autoantibody': '3/5 = 60%',
        'hba1c_change': '5/10 = 50%',
        'inflammatory_markers': '0/7 = 0% (control)',
        'dose_response': '0/178 = 0%',
        'odds_ratio': '0/26 = 0%',
        'hazard_ratio': '0/7 = 0%',
    },
    'notable': [
        'c_peptide fell to ZERO surviving extractions. Checked: no research path '
        'in either store drew on c_peptide corpus evidence, so nothing was '
        'hollowed by this. The published landing page did advertise C-peptide '
        'first among its evidence categories; that sentence is now derived from '
        'the live extraction types instead of hardcoded.',
        'PMID 36643381 (colchicine protocol) was publishing a power-calculation '
        'assumption and another trial\'s result as its own inflammatory-marker '
        'findings. Both are now rejected as PROJECTED_NOT_MEASURED and '
        'ATTRIBUTED_TO_OTHER_STUDY.',
        'Trial-registration and molecule-name fractions (CTRI/2020/08/027072, '
        'ethics approval 2018/23JAN/023, CD80/86, F4/80+, HLA DR3/4) were being '
        'counted as remission n/N denominators.',
    ],
})

# ---------------------------------------------------------------------------
# 6. Run history
# ---------------------------------------------------------------------------
state.setdefault('run_history', []).append({
    'date': TODAY,
    'day': 'Saturday',
    'papers_checked': 0,
    'paths_validated': 0,
    'issues_found': 6,
    'changes_pushed': False,
    'summary': (
        'Sat 2026-08-22 - FIVE MORE EXTRACTORS WERE MAJORITY ARTIFACT, AND THE '
        'EXTRACTION STEP WAS NOT IN THE PIPELINE. '
        '(1) THE MEASUREMENT. The P1 item flagged c_peptide, hba1c_change, '
        'survival_graft and remission as suspect BY CONSTRUCTION. All four were, '
        'and so was autoantibody, which the item did not list: survival_graft '
        '6/6 artifact, c_peptide 5/5, remission 34/48, autoantibody 3/5, '
        'hba1c_change 5/10. Corpus artifact rate 18.2%. The control that makes '
        'this credible: inflammatory_markers, rewritten the day before, scored '
        '0% under the identical signature set. '
        '(2) WHAT THEY WERE PUBLISHING. "insulin independence was 45.5 +/- 32.0 '
        'months" became a 7.1% graft survival figure. "glycated hemoglobin level '
        'and insulin dose. RESULTS At 1 year, the mean AUC for the level of C '
        'peptide..." became an HbA1c of 6.76. The trial registration '
        'CTRI/2020/08/027072 became a remission denominator. '
        '(3) THE FIX. Every gap bounded to [^.\\n]{0,N}?, every capture required '
        'to carry a unit, a percent sign or an explicit denominator - the same '
        'three rules applied to inflammatory_markers on 2026-08-21. Plus five '
        'new rejection reasons: IDENTIFIER_FRACTION, IMPLAUSIBLE_FRACTION, '
        'DEFINITION_THRESHOLD, PROJECTED_NOT_MEASURED, ATTRIBUTED_TO_OTHER_STUDY. '
        'Corpus 292 -> 240; artifact rate 18.2% -> 0.0%. '
        '(4) PROVENANCE, A NEW DEFECT CLASS. PMID 36643381 is a colchicine trial '
        'PROTOCOL. It was supplying two inflammatory-marker data points: one from '
        '"we estimated that hs-CRP is suppressed to 3.22 mg/L" - a sample-size '
        'assumption for a trial that had not run - and one from "the previous '
        'report indicating that colchicine 1 mg for 4 weeks reduced hs-CRP by '
        'about 60%", which is somebody else\'s result. A projection served as a '
        'measurement is the worst error this repo can make. '
        '(5) THE BIGGER ONE, FOUND SIDEWAYS. Building the design-paper gate '
        'revealed that PMID 39613428 - titled "...protocol for a randomised, '
        'double-blind ... trial" - is the SOLE corpus source for both '
        '`verapamil -> beta_cell` and `verapamil -> T1D`, the #2 and #3 paths on '
        'the dashboard, and contributes nothing but planned doses. Escalated as '
        'a human call rather than delisted unattended. '
        '(6) THE STRUCTURAL FINDING. extract_corpus_data.py was never in '
        'run_quality_improvements.py. Four dashboards and the landing page read '
        'its output, so the runner could report 47/47 green over arbitrarily '
        'stale extraction - and did: the 2026-08-21 extractor fix had not '
        'reached PMID 32862232 until this run re-ran it by hand. Now step 33 of '
        '50. Two new gates registered alongside it '
        '(audit_extractor_wildcards.py, audit_baseline_citations.py); the '
        'wildcard gate was negative-tested by reinjecting the historical '
        'remission pattern, which it caught along with all 23 artifacts it '
        'reproduced. Pipeline 50/50 [OK].'
    ),
})

state['last_run'] = TODAY
state['last_updated'] = TODAY + 'T00:00:00'

with open(STATE, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=1, ensure_ascii=False)

print(f'Closed {len(closed)} queue item(s):')
for c in closed:
    print(f'  - {c}')
print(f'Added {len(NEW_ITEMS)} new item(s). Queue depth: {len(state["work_queue"])}')
print(f'Run history entries: {len(state["run_history"])}')
print('[OK] state saved')
