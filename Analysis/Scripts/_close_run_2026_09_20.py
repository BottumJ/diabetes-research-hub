#!/usr/bin/env python3
"""Close the 2026-09-20 run: record findings, reprioritise the queue.

Theme of the run: THREE STORES, ONE DISORDER. Every finding today is the same
shape - a question this repository already knows how to answer, asked in a
form no gate was reading.
"""

import json
import os
import shutil
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Results'))
STATE = os.path.join(RESULTS, 'agent_state.json')
TODAY = '2026-09-20'

SUMMARY = (
    "A BLANK FIELD DELETED THREE PRIMARY STUDIES, AND A SEVEN-MONTH-STALE GAP "
    "REGISTRY PUBLISHED FOURTEEN RESEARCH QUESTIONS THIS HUB DOES NOT STUDY. "
    "Both were invisible to 80+ green stages for the same reason, and it is a "
    "reason worth naming precisely: this repository's gates check the CONTENT "
    "of an assertion, and both defects were defects of FORM. "
    "(1) corpus_membership.py says in its own source that a FLAGGED paper with "
    "no membership_class 'is a bug, not a default', and that an audit fails on "
    "it. No such audit existed - unclassified() had no caller for 23 days - so "
    "the module used the missing field AS a default, and on 2026-09-19 a "
    "reconcile run deleted the four papers from the index with the ledger "
    "reason recorded verbatim as 'FLAGGED in agent_state.json with no class "
    "recorded'. Three were real primary studies: DIAGNODE-2 (Diabetes Care "
    "Phase IIb RCT), PREDIMED, and the CITR HLA-DR analysis that state itself "
    "calls load-bearing for Gap #11. All three were simultaneously cited on "
    "live pages while corpus_membership answered citable()==False for them, "
    "because citable() ALSO had zero call sites. Classified all four from "
    "their own vetting records, added the CORPUS class so a repair note stops "
    "being a disqualifier, and made eviction require an affirmative code - "
    "exclusion is reversible, eviction destroys the row. "
    "(2) build_extracted_evidence.py and build_research_paths.py each carried "
    "a byte-identical hard-coded gap registry in which 14 of 15 TITLES and 9 "
    "of 15 TIERS disagreed with the canonical store. Not drift - a different "
    "set of research questions. Extracted_Evidence.html published 'Gap 11: "
    "Immunomodulation in Type 2 Diabetes, BRONZE, 39 points' over correctly "
    "extracted, correctly cited glucokinase-activator odds ratios; canonical "
    "Gap #11 is Islet Transplant Registry Equity, GOLD. Zero canonical gap "
    "names appeared on the page. audit_gap_numbering.py could not see it "
    "because it reads the prose form 'Gap #N (TIER)' and a dict literal is not "
    "a sentence - it reported on four stores and called the numbering sound. "
    "Taught it the dict form: it went from 4 stores to 69 hardcoded tier sites "
    "across 15 gaps, and the second stale copy was found only by that change. "
    "Both builders now read the store; neither carries an answer. "
    "(3) ANSWERED THE 13-DAY-OLD GAP #11 QUESTION FROM FULL TEXT, NOT "
    "ABSTRACT. PMC10070978 was on disk the whole time. In 39,486 characters "
    "including the complete baseline and potential-confounder tables, PMID "
    "37026004 contains ZERO occurrences of race, ethnicity, Hispanic, Black, "
    "African American, Caucasian or demographic. It reports sex, age, BMI and "
    "donor cause of death. So the Gap #11 equity intersection is not merely "
    "unevidenced in this corpus - the load-bearing paper CANNOT evidence it, "
    "because it never collected the variable. That requires a CITR data "
    "request, not another PubMed sweep. Closed 'INDEX THE 17 PAPERS WHOSE FULL "
    "TEXT IS ON DISK' with a measurement rather than work: 16 of 17 are "
    "excluded on purpose (14 uncitable, 2 BACKGROUND); 37026004 was the only "
    "real item and classification fixed it. The backlog is zero."
)

NEW_ITEMS = [
    dict(priority=1, type='audit_gap', added=TODAY, target=(
        'GAP #11 NEEDS A CITR DATA REQUEST OR A RESTATED CLAIM - THE PUBLISHED '
        'LITERATURE CANNOT SETTLE IT AND THAT IS NOW MEASURED, NOT SUSPECTED. '
        'Read PMC10070978 (PMID 37026004) in full 2026-09-20: 39,486 chars, '
        'complete Table 3 baseline and the full potential-confounder table, '
        'and ZERO occurrences of race / ethnicity / Hispanic / Black / African '
        'American / Caucasian / demographic. It reports % Female, age, BMI, '
        'donor gender and cause of death. audit_gap_subject_coverage.py rates '
        'this gap [MEDIUM] "6 papers touch the registry axis, 1 touches '
        'equity, none touches both" and offers two remedies: state that the '
        'intersection rests on inference, or find a paper at the '
        'intersection. The second remedy is now known to be unavailable from '
        'this paper. TWO REAL OPTIONS: (a) request recipient race/ethnicity '
        'from the CITR data coordinating centre, which is a human action with '
        'a form to fill in; (b) restate Gap #11 as what the evidence supports '
        '- that the registry does not PUBLISH recipient race, which is itself '
        'an equity finding and a stronger one than an inferred disparity. '
        'Option (b) needs no data request and is defensible today. Do not '
        'publish the inferred version while (a) is pending.')),
    dict(priority=1, type='fix_pipeline', added=TODAY, target=(
        'SWEEP THE OTHER DICT-LITERAL REGISTRIES NOW THAT THE AUDIT CAN SEE '
        'THEM. audit_gap_numbering.py learned the dict form today and the '
        'count went from 4 stores to 69 hardcoded tier sites across 15 gaps. '
        'Two of those sites were seven-month-stale registries publishing 14 '
        'wrong gap titles each, and the SECOND one was found only by the '
        'audit change - reading the first by hand would have left it. That is '
        'the generalisation worth making: a hand-corrected copy is the same '
        'defect one edit later. Work the 69 down by making each site READ the '
        'store, in descending order of whether the site renders to docs/. '
        'build_gap_deep_dives.py and rebuild_website.py are next; they agree '
        'with canonical today, which is exactly when a copy is cheapest to '
        'remove. ALSO: the same question should be asked of every other '
        'registry this repo hardcodes - drug lists, trial phases, tier '
        'definitions - by grepping for dict literals keyed on an id that also '
        'exists in a Results/*.json store.')),
    dict(priority=2, type='fix_pipeline', added=TODAY, target=(
        'DECIDE WHETHER BACKGROUND PAPERS BELONG IN paper_library/index.json. '
        'Raised by, but deliberately NOT settled by, the 2026-09-20 '
        'membership work. reconcile_paper_index.py refuses index admission to '
        'everything in corpus_membership.excluded_pmids(), which includes the '
        '8 BACKGROUND papers - yet corpus_membership.py\'s own docstring '
        'quotes the 2026-04-20 note on PMID 25714673 verbatim: "Keep in '
        'paper_library but exclude from mechanism-evidence extraction." The '
        'module and the consumer disagree about what BACKGROUND means, and '
        'the module is the one with the written rule. MEASURED 2026-09-20: 2 '
        'of the 16 unindexed full texts on disk (18662538 Massague TGF-beta, '
        '39428507 CAR-Treg/MS) are BACKGROUND papers the repo can read and '
        'does not list. This was left alone today ON PURPOSE and the '
        'distinction matters: the four evictions reversed today were '
        'justified by a BLANK FIELD, which is a bug with one correct answer. '
        'BACKGROUND exclusion is justified by an affirmative adjudication - '
        'debatable design, not a bug - and changing it moves corpus counts. '
        'Decide it deliberately, then make the module and the consumer agree.')),
    dict(priority=2, type='audit_gap', added=TODAY, target=(
        'GAP #14 AND #15 TIER: THE GATE HAS NOW ASKED SIX TIMES. Unchanged '
        'and still overdue - audit_gap_subject_coverage.py rates both [HIGH] '
        '"Tier BRONZE with ZERO evidence papers". NEW TODAY, and it makes the '
        'edit bigger than it looked: the tier is written in 69 places, not '
        'the 24 previously counted, because the dict-literal form was '
        'invisible until audit_gap_numbering.py was extended. Do NOT hand-'
        'edit 69 sites. Demote in the canonical store (gap_evidence.json + '
        'agent_state) and convert the renderers to read it, which is the same '
        'work item as the dict-literal sweep above. Sequence them together.')),
    dict(priority=3, type='note', added=TODAY, target=(
        'TASK-FILE STEP 4 IS STILL GENERATING FALSE WORK, AND TODAY GIVES THE '
        'NUMBER. The scheduled task file instructs a sweep for "PMIDs above '
        '42000000 (fabricated)". Measured live 2026-09-20: the real PubMed '
        'ceiling is 42,763,307 and pmid_ceiling.py flags above 43,013,307. '
        'The highest PMID anywhere in this repo is 42,698,953 - a real paper, '
        '698,953 above the task file\'s line and 314,354 below the correct '
        'one. Anyone following the task file literally would open a '
        'fabrication investigation into a genuine 2026 citation. The repo '
        'fixed this on 2026-08-25/31; the task file has carried the stale '
        'rule since. One-line edit, ninth day of asking.')),
]

CLOSE_MATCH = [
    ('GIVE THE OTHER 19 FLAGGED PAPERS A MEMBERSHIP CLASS',
     'RESOLVED 2026-09-20. Measured: the other 19 already carried a class '
     'from the 2026-08-28 adjudication; the 4 unclassified were the whole '
     'set and all 4 are now classified (3 CORPUS, 1 BACKGROUND). '
     'corpus_membership.unclassified() is empty and '
     'audit_flagged_membership_class.py now fails the build if it is not. '
     'The underlying risk the item named - "one reconcile run away from '
     'leaving the corpus" - is separately closed by evictable_pmids(), which '
     'refuses to evict on a missing field.'),
    ('INDEX THE 17 PAPERS WHOSE FULL TEXT IS ALREADY ON DISK',
     'RESOLVED 2026-09-20 BY MEASUREMENT, NOT BY INGESTION. The 17 were an '
     'undifferentiated count. repair_index_pmcid_map.py now splits them '
     'through corpus_membership: 16 are excluded on purpose (8 PROVENANCE, 5 '
     'OFF_TOPIC, 1 RETRACTED, 2 BACKGROUND) - for those the index is correct '
     'and the file on disk is residue. 37026004 was the only genuine item, '
     'and classifying it restored it. Ingestion backlog: zero. The BACKGROUND '
     'pair is carried forward as a separate design question.'),
    ('READ PMID 37026004 IN FULL AND ANSWER ONE QUESTION',
     'ANSWERED 2026-09-20: NO. PMC10070978, 39,486 chars including the '
     'complete baseline and potential-confounder tables, contains zero '
     'occurrences of race, ethnicity, Hispanic, Black, African American, '
     'Caucasian or demographic. The CITR HLA-DR analysis does not report '
     'recipient race or ethnicity at all. Per the item\'s own framing, that '
     'settles it: the Gap #11 equity hypothesis is NOT testable from '
     'published data and requires a CITR data request. Follow-up filed at '
     'priority 1. SECONDARY FINDING, recorded because it bears on how the '
     'paper may be cited at all: group B (n=11) is better matched at HLA-A '
     '(73% vs 48%) and HLA-B (45% vs 17%) than group A, and neither variable '
     'appears in the paper\'s 19-row confounder table. The authors\' own '
     'group D vs E comparison (>=3 vs <3 average A,B,DR matches, insulin '
     'independence p=0.8) argues against general matching explaining the '
     'result, which is a real defence - but maintenance immunosuppression '
     'with mTOR+CNI differs 90% vs 14% at p=0.2, and a 6.4-fold difference '
     'reported non-significant on n=11 is a power artifact, not evidence of '
     'comparability. Any use must carry n=11 and must not be causal.'),
]


def main():
    with open(STATE, encoding='utf-8') as fh:
        state = json.load(fh)

    shutil.copy2(STATE, STATE + '.bak_%s_close' % TODAY)

    state.setdefault('run_history', []).append({
        'date': TODAY,
        'day': 'Sunday',
        'papers_checked': 4,
        'papers_classified': 4,
        'papers_readmitted': 3,
        'fulltext_read': 1,
        'gates_added': 1,
        'gates_extended': 2,
        'builders_fixed': 2,
        'issues_found': 5,
        'changes_pushed': False,
        'summary': SUMMARY,
    })

    # ---- close resolved items -----------------------------------------
    closed = []
    for item in state.get('work_queue', []):
        tgt = item.get('target') or ''
        for needle, resolution in CLOSE_MATCH:
            if needle in tgt and item.get('status') not in ('closed',):
                item['status'] = 'closed'
                item['closed_on'] = TODAY
                item['resolution'] = resolution
                closed.append(needle[:50])

    # ---- add new items -------------------------------------------------
    existing = {(i.get('target') or '')[:80] for i in state.get('work_queue', [])}
    added = 0
    for item in NEW_ITEMS:
        if item['target'][:80] in existing:
            continue
        state.setdefault('work_queue', []).append(item)
        added += 1

    # ---- doctrine note -------------------------------------------------
    state.setdefault('doctrine_notes', {})[TODAY] = (
        'A GATE THAT NAMES ITS OWN MISSING ENFORCEMENT IS NOT ENFORCED. '
        'corpus_membership.py contained, in its own source, both the rule '
        '("a FLAGGED paper with no membership_class is a bug, not a default") '
        'and the remedy ("an audit fails on this") - and the audit did not '
        'exist. The docstring read as if it did, which is worse than silence: '
        'it made every reader of that module, human and agent, believe the '
        'check was running. Two of the three defects found today were of this '
        'form. THE TEST TO APPLY: for every invariant a module DESCRIBES, '
        'grep for a caller of the function that checks it. A documented '
        'invariant with zero call sites is a comment. citable() had zero call '
        'sites while the site cited four papers it answered False for. '
        'SECOND, NARROWER RULE, and it generalises past membership: EXCLUSION '
        'AND DELETION MUST NOT SHARE A PREDICATE. Excluding a record is '
        'reversible and its reason can be re-read tomorrow; deleting it '
        'leaves nothing to reverse. So deletion must require an affirmative '
        'adjudication and must never be triggered by the ABSENCE of one. The '
        '2026-09-19 eviction ledger recorded a blank field as the '
        'justification for removing three primary human studies, and it was '
        'internally consistent while doing so.'
    )

    state['last_updated'] = TODAY
    state['last_run'] = TODAY

    with open(STATE, 'w', encoding='utf-8') as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)

    print('  run recorded for %s' % TODAY)
    print('  queue items closed : %d' % len(closed))
    for c in closed:
        print('      %s...' % c)
    print('  queue items added  : %d' % added)
    open_items = [i for i in state['work_queue']
                  if i.get('status') not in ('closed', 'done', 'completed')]
    print('  open queue items   : %d' % len(open_items))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
