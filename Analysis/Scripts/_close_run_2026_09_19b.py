#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Second half of the 2026-09-19 close: the eviction finding."""
import json, os
from datetime import date
HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, '..', 'Results', 'agent_state.json')
TODAY = str(date.today())
with open(STATE, encoding='utf-8') as f:
    s = json.load(f)

s['audit_notes'].append({
    'date': TODAY,
    'finding': ('FLAGGING A PAPER DELETES IT FROM THE CORPUS, AND ONE OF THE FOUR '
                'PAPERS THIS HAS HAPPENED TO IS THE ONE STATE ITSELF CALLS '
                'LOAD-BEARING FOR GAP #11.'),
    'how_found': ('audit_index_field_invariants.py - written today for an unrelated bug '
                  '- failed the pipeline on arithmetic: metadata.total_indexed=347 '
                  'against a papers dict of 345. Two papers had been removed from the '
                  'index DURING today\'s run and nothing had reported it.'),
    'mechanism': ('corpus_membership.excluded_pmids() assigns the code '
                  'FLAGGED_UNCLASSIFIED to any PMID that is FLAGGED in agent_state with '
                  'no membership_class recorded, and treats it as adjudicated NOT A '
                  'CORPUS PAPER. reconcile_paper_index.py then evicts it from '
                  'index.json. So "flagged for review" and "adjudicated off-topic" are '
                  'the same act, though they are opposite judgements: one says look '
                  'closer, the other says this does not belong.'),
    'evicted_population': {
        'total_excluded_pmids': 52,
        'by_code': {'PROVENANCE': 29, 'OFF_TOPIC': 11, 'BACKGROUND': 7,
                    'FLAGGED_UNCLASSIFIED': 4, 'RETRACTED': 1},
        'flagged_unclassified': [
            {'pmid': '25940230', 'title': 'Benefits of the Mediterranean Diet: Insights '
             'From the PREDIMED Study.', 'evicted': TODAY,
             'note': 'Flagged by the 2026-09-18 run, which corrected the PREDIMED 30% '
                     'figure to the CVD number. The correction caused the eviction.'},
            {'pmid': '34021020', 'title': 'Intralymphatic Glutamic Acid Decarboxylase '
             'With Vitamin D Supplementation in Recent-Onset Type 1 Diabetes (DIAGNODE-2).',
             'evicted': TODAY,
             'note': 'Also flagged by the 2026-09-18 run (published as LADA). Same '
                     'pattern: yesterday corrected it, today it vanished.'},
            {'pmid': '37026004', 'title': 'Matching for HLA-DR excluding diabetogenic '
             'HLA-DR3 and HLA-DR4...', 'evicted': 'before 2026-09-19, date unrecorded',
             'note': 'agent_state describes this paper as LOAD-BEARING for the Gap #11 '
                     'hypothesis. Its full text is on disk as PMC10070978. So the '
                     'repository holds the full text of a paper it calls load-bearing '
                     'for a gap, and does not list the paper.'},
            {'pmid': '42674789', 'title': 'Retrospective population-based cohorts for '
             'assessing the performance of...', 'evicted': 'before 2026-09-19, date '
             'unrecorded', 'note': 'FLAGGED PROTOCOL, relevant to canonical Gap #10.'},
        ],
    },
    'connection_to_the_other_finding': ('This is the same mechanism as the I3 note from '
                                        'the pmcid repair earlier today: 18 full texts '
                                        'sit on disk for papers the index does not list. '
                                        'Eviction leaves the full text behind.'),
    'applied_today': ['reconcile_paper_index.py now writes an eviction LEDGER '
                      '(pmid, date, adjudication code, why, title) into index metadata '
                      'and updates total_indexed when it deletes entries. Previously it '
                      'recorded only a date.',
                      'The four existing evictions were backfilled into that ledger; '
                      'the two pre-dating today are marked date-unrecorded rather than '
                      'given an invented date.',
                      'metadata.total_indexed repaired 347 -> 345; the invariant gate '
                      'now passes.'],
    'NOT_applied': ('The adjudication semantics were NOT changed. Whether FLAGGED with '
                    'no class should mean EXCLUDED is a corpus-membership decision, not '
                    'a bug fix, and reversing it unattended would silently re-admit four '
                    'papers - including one flagged as a protocol and one whose flag has '
                    'never been read. Queued for a human call.'),
})

s['doctrine_notes'][TODAY] += (
    ' Third lesson, from the eviction: a gate written for one bug caught a different and '
    'worse one within an hour, because arithmetic does not care what you were looking '
    'for. The cheapest checks in this repository have consistently been the ones that '
    'compare a file to itself.'
)

s['work_queue'].extend([
    {'type': 'user_action_required', 'priority': 1, 'added': TODAY,
     'target': ('DECIDE WHETHER "FLAGGED" SHOULD MEAN "NOT A CORPUS PAPER". '
                'corpus_membership.excluded_pmids() gives the code '
                'FLAGGED_UNCLASSIFIED to any paper FLAGGED in agent_state with no '
                'membership_class, and reconcile_paper_index.py evicts it from the '
                'paper index. Four papers are out on that basis, including 37026004, '
                'which agent_state itself calls LOAD-BEARING for the Gap #11 '
                'hypothesis, and 42674789, a flagged protocol for Gap #10. Worse, the '
                'trigger runs backwards: the 2026-09-18 run CORRECTED PREDIMED '
                '(25940230) and DIAGNODE-2 (34021020) and flagged them, and today they '
                'were deleted from the corpus - correcting a paper is what removed it. '
                'Three options: (a) FLAGGED papers stay indexed and carry a flag field, '
                'with exclusion reserved for an explicit off-topic adjudication; (b) '
                'each of the 4 gets a membership_class now, one at a time; (c) keep the '
                'current behaviour and state it on the methodology page, since the '
                'corpus headline count depends on it. The eviction is now at least '
                'visible (ledger in index metadata) and the count is honest, so this is '
                'no longer silent - but it is still happening.')},
    {'type': 'fix_pipeline', 'priority': 2, 'added': TODAY,
     'target': ('GIVE THE OTHER 19 FLAGGED PAPERS A MEMBERSHIP CLASS BEFORE THEY '
                'DISAPPEAR TOO. 23 papers are FLAGGED in agent_state; 4 have already '
                'been evicted as FLAGGED_UNCLASSIFIED. Every remaining flag without a '
                'membership_class is a paper one reconcile run away from leaving the '
                'corpus. Classify them explicitly, or implement option (a) above.')},
])

s['run_history'][-1]['summary'] += (
    ' LATE FINDING, from the new gate\'s first pipeline run: it failed on '
    'total_indexed=347 vs 345 papers and exposed that FLAGGED papers are being EVICTED '
    'from the corpus index as "adjudicated not a corpus paper". Four are out, including '
    'PMID 37026004 which state itself calls load-bearing for Gap #11 - and the two '
    'evicted today were evicted BECAUSE yesterday\'s run corrected them. Eviction is now '
    'ledgered and the count is honest; the adjudication semantics are a queued human '
    'call, not something to reverse unattended.'
)
s['run_history'][-1]['gates_added'].append(
    'reconcile_paper_index.py eviction ledger + total_indexed repair')
s['run_history'][-1]['queue_items_added'] = 8

with open(STATE, 'w', encoding='utf-8') as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
print('state updated. queue=%d audit_notes=%d' % (len(s['work_queue']), len(s['audit_notes'])))
