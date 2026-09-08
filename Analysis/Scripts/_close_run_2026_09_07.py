"""Close the 2026-09-07 run: record the gap_subject_coverage sweep result.

Run AFTER _run_2026_09_07.py and audit_gap_subject_coverage.py.
"""
import json
import os
from datetime import datetime

RESULTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Results')
STATE = os.path.join(RESULTS, 'agent_state.json')
AUDIT = os.path.join(RESULTS, 'gap_subject_coverage_audit.json')
TODAY = '2026-09-07'

with open(STATE, encoding='utf-8') as fh:
    state = json.load(fh)
with open(AUDIT, encoding='utf-8') as fh:
    audit = json.load(fh)

# ------------------------------------------------- the sweep, and what it means
HARD = ['1', '11', '13']
SOFT = ['4', '7']

state.setdefault('gap_subject_coverage', {})[TODAY] = {
    'gate': 'audit_gap_subject_coverage.py (new today)',
    'gaps_checked': audit['gaps_checked'],
    'gaps_failing': audit['findings_count'],
    'coverage_table': audit['coverage_table'],
    'interpretation': {
        'headline': (
            'Gap #11 was not an isolated defect. 9 of 15 gaps fail. The hub has been assigning '
            'evidence tiers to intersections while storing evidence for only one side of the '
            'intersection.'),
        'hard_failures': {
            'gaps': HARD,
            'meaning': ('The stored evidence is about a DIFFERENT SUBJECT. Verified by reading '
                        'the stored titles directly, not just the regex verdict:\n'
                        '  #1 Gene Therapy for LADA, SILVER, 31 papers - every one is a LADA '
                        'autoantibody/phenotype/prevalence study (GAD affinity, ICA titres, '
                        'Action LADA, C-peptide screening). ZERO concern gene therapy, vectors, '
                        'AAV, CRISPR or gene transfer. The gap is rated on LADA epidemiology.\n'
                        '  #11 Islet Transplant Registry Equity, GOLD, 2 papers - the 2008 CITR '
                        'update and a graft-function cohort. Neither mentions equity, race, '
                        'ethnicity, socioeconomic status or access.\n'
                        '  #13 Personalized Nutrition for Beta Cells, BRONZE, 3 papers - all '
                        'three are berberine trials in TYPE 2 DIABETES for glycaemic control and '
                        'dyslipidaemia. Berberine is a plant-derived alkaloid drug, not '
                        'personalized nutrition, and none of the three is about beta-cell '
                        'preservation. This is a mis-file, not merely a thin evidence base.'),
        },
        'soft_failures': {
            'gaps': SOFT,
            'meaning': ('HUMAN CALL, and the gate should not decide it. #4 (Drug Repurposing for '
                        'Islet Transplant) cites anakinra, etanercept and rapamycin in islet '
                        'transplant; #7 (GKA Drug Repurposing) cites dorzagliatin trials and GKA '
                        'meta-analyses. Those drugs ARE repurposed agents. But no cited paper '
                        'FRAMES itself as repurposing, so what these gaps have is evidence of '
                        'the drugs, not evidence about the repurposing question. Whether that '
                        'counts is a scientific judgement about what the gap claims.'),
        },
        'zero_evidence_tiers': {
            'gaps': ['14', '15'],
            'meaning': ('BRONZE with zero papers. A tier above EXPLORATORY asserts evidential '
                        'standing neither gap has. Gap #9 holds zero papers too but is correctly '
                        'labelled EXPLORATORY and does not fail.'),
        },
        'inference_only': {
            'gaps': ['8'],
            'meaning': ('#8 Immunomodulatory Drugs for LADA, 27 papers: 7 touch immunomodulation, '
                        '15 touch LADA, and NOT ONE touches both. The intersection is joined by '
                        'inference across papers rather than evidenced by any of them. That may '
                        'be defensible - it may even be the point of the gap - but it must be '
                        'stated, not implied by a citation list.'),
        },
    },
    'what_this_gate_does_not_prove': (
        'It reads stored titles and finding snippets only; it fetches no abstracts. A miss is an '
        'UPPER bound on the problem and a prompt to read the paper, not a proven defect. And '
        'passing is weak news: one passing mention of a word is not an analysis. The three hard '
        'failures above were confirmed by reading the stored titles by hand, which is why they '
        'are stated as fact and the rest are stated as flags.'),
    'not_applied': (
        'No tier was changed and no gap was deleted by this run. Nine simultaneous demotions is a '
        'scientific judgement about the hub\'s own headline claims, and the 2026-09-03 '
        'single-writer refactor has not landed, so a tier written now would fork further.'),
}

state.setdefault('doctrine_notes', {}).setdefault(TODAY, {})['intersection_evidence'] = (
    'EVERY GAP HERE IS AN INTERSECTION, AND EVIDENCE FOR ONE AXIS IS NOT EVIDENCE FOR THE GAP. '
    'Measured 2026-09-07 across all 15 gaps: 9 fail. The recurring shape is a pile of papers on '
    'the easy axis (LADA epidemiology, islet transplant outcomes, GKA trials) standing in for '
    'the hard axis (gene therapy, equity, repurposing) that makes the gap a gap. Half-covered '
    'evidence is the most dangerous kind because a human skimming the citation list sees '
    'on-topic papers and stops. Rule: a gap\'s tier may not exceed what its evidence covers on '
    'its WEAKER axis.')

# --------------------------------------------------------------------- queue
state['work_queue'].append({
    'priority': 1, 'type': 'user_action_required', 'added': TODAY,
    'target': (
        'HUMAN CALL: NINE OF FIFTEEN GAPS ARE TIERED ON EVIDENCE THAT DOES NOT COVER THEIR OWN '
        'QUESTION, AND THREE OF THOSE ARE OUTRIGHT MIS-FILES. Measured 2026-09-07 by the new '
        'Analysis/Scripts/audit_gap_subject_coverage.py, then confirmed by reading the stored '
        'titles by hand. The three that are not judgement calls: #1 Gene Therapy for LADA is '
        'SILVER on 31 papers of which ZERO concern gene therapy - they are GAD-autoantibody and '
        'LADA-prevalence studies. #13 Personalized Nutrition for Beta Cells is BRONZE on three '
        'BERBERINE trials in type 2 diabetes. #11 Islet Transplant Registry Equity is GOLD on a '
        '2008 registry update and a graft-function cohort, neither mentioning equity. '
        'DECISIONS NEEDED. (a) #1 and #13: demote to EXPLORATORY, or re-found on a recorded null '
        'search? Their gaps may well be real - #11\'s survived testing today - but their current '
        'citation lists are not evidence of them. (b) #4 and #7 fail on the word "repurposing" '
        'while citing anakinra, etanercept, rapamycin and dorzagliatin. Those ARE repurposed '
        'drugs; no cited paper says so. Does the hub count drug-level evidence as '
        'repurposing-question evidence? (c) #14 and #15 are BRONZE with zero papers - demote to '
        'EXPLORATORY like #9, which holds zero papers and is labelled honestly? (d) #8 joins its '
        'two axes by inference across 27 papers with none at the intersection - state that on '
        'the card, or find an intersection paper? NOTHING WAS APPLIED. Nine simultaneous tier '
        'changes to the hub\'s headline claims is not an unattended decision.')})

state['run_history'][-1]['gate_status'] = (
    'FULL PIPELINE NOT RUN THIS CYCLE - see pipeline_not_run below. New gate '
    'audit_gap_subject_coverage.py written, run standalone, and registered as stage "gapsubject"; '
    '9 of 15 gaps FAIL.')
state['run_history'][-1]['pipeline_not_run'] = (
    'run_quality_improvements.py was started twice and exceeded the sandbox call limit '
    '(~178s) both times. Background execution is impossible here: each bash call runs in its own '
    'PID namespace, so a nohup\'d process is killed when the call returns - confirmed this run '
    'by a 0-byte log and no surviving process. THIS IS NOT A PASS AND IS NOT RECORDED AS ONE. '
    'The 67 existing stages were NOT verified today. Two things follow: (1) the new gapsubject '
    'stage is registered but has never run inside the runner, only standalone - if it breaks the '
    'runner, that will surface on the first Windows-side run; (2) per the operator\'s standing '
    'preference, long compute belongs on the Windows side. PUSH_AND_VERIFY.ps1 already exists '
    'for the push; the pipeline needs the same treatment.')
state['run_history'][-1]['gaps_swept'] = 'all 15 (subject coverage)'
state['run_history'][-1]['new_scripts'] = ['audit_gap_subject_coverage.py']
state['run_history'][-1]['new_stages'] = ['gapsubject']
state['run_history'][-1]['summary'] += (
    '\n (7) AND THE SAME DEFECT IS IN NINE OF FIFTEEN GAPS. Gap #11 prompted a new gate, '
    'audit_gap_subject_coverage.py, which asks of every gap whether its stored evidence mentions '
    'both axes of its own question. 9 of 15 fail. Three are not judgement calls and were '
    'confirmed by reading the stored titles by hand: #1 "Gene Therapy for LADA" is SILVER on 31 '
    'papers of which ZERO concern gene therapy - they are GAD-autoantibody and LADA-prevalence '
    'studies; #13 "Personalized Nutrition for Beta Cells" is BRONZE on three BERBERINE trials in '
    'type 2 diabetes; #11 as described above. Two more (#4, #7) fail on the word "repurposing" '
    'while citing genuinely repurposed drugs, which is a human call, not a defect. #14 and #15 '
    'hold BRONZE with zero papers. #8 joins its axes by inference across 27 papers with none at '
    'the intersection. NOTHING WAS DEMOTED - nine tier changes to the hub\'s headline claims is '
    'not an unattended decision, and it is now the top human-call item.'
    '\n (8) THE PIPELINE DID NOT RUN AND THIS RUN DOES NOT CLAIM IT DID. '
    'run_quality_improvements.py exceeded the sandbox call limit twice; background execution is '
    'impossible because each bash call gets its own PID namespace. The 67 existing stages are '
    'UNVERIFIED today. Combined with the P0 push failure, the honest status of this repository '
    'is: work is accumulating in a working tree that no reader can reach and no full gate run '
    'has confirmed.')

with open(STATE, 'w', encoding='utf-8') as fh:
    json.dump(state, fh, indent=2, ensure_ascii=False)

print('[OK] run closed %s' % TODAY)
print('[OK] gap subject coverage recorded: %d/%d gaps failing'
      % (audit['findings_count'], audit['gaps_checked']))
print('[OK] queue: %d items' % len(state['work_queue']))
