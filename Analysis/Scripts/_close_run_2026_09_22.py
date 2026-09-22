#!/usr/bin/env python3
"""Close the 2026-09-22 run: record it, reprioritise the queue, save state."""

import json
import os
import shutil
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', '..'))
STATE = os.path.join(ROOT, 'Analysis', 'Results', 'agent_state.json')
TODAY = date.today().isoformat()

SUMMARY = (
    "A GATE THAT PRINTS [FAIL] AND EXITS 0 IS NOT A WEAK GATE, IT IS NOT A "
    "GATE -- AND THE SAME SENTENCE TURNS OUT TO DESCRIBE A GATE THAT CHECKS "
    "ONE MENTION OF AN IDENTIFIER AND DISCARDS THE REST. Both were found "
    "today, both had been green for their whole existence, and between them "
    "they were hiding twelve live defects.\n\n"
    "(1) run_quality_improvements.run_script() decides pass/fail on "
    "`result.returncode != 0` and nothing else. audit_gate_exit_codes.py (new) "
    "reads the runner's own SCRIPTS dict and asks, of each wired stage, "
    "whether its verdict can reach that line. One real defect: path_store.py "
    "carries a block captioned UNBACKED-STATUS GATE that prints '[FAIL] N "
    "path(s) assert a validated status with no evidence anywhere' out of a "
    "main() that returned None into a bare `main()` call. It had never been "
    "able to fail. Fixed and proven in both directions (clean tree exits 0; "
    "an injected unbacked path exits 1). The audit's own first draft produced "
    "TWO FALSE POSITIVES out of three findings -- it asked whether ANY "
    "function returns a non-zero literal, and caught "
    "rebuild_website.get_trial_count() returning 42 -- so the rule was "
    "narrowed to the entry point and both false-positive shapes are now "
    "pinned as fixtures (--selftest, wired as its own stage).\n\n"
    "(2) audit_nct_identifiers.py reported 30/30 OK while "
    "build_trial_equity_mapper.py held EIGHT records disagreeing with the "
    "live registry. Three independent reasons, each worth naming: "
    "(a) `site = by_nct[nct][0]` -- only the FIRST mention of each identifier "
    "was ever examined, so 31 of 61 sites had never been checked at all, and "
    "the skipped ones skew toward the builder dicts that assert the most; "
    "(b) enrollment was matched by a PROSE regex requiring the word "
    "'patients', so `'enrollment': 330,` matched nothing; (c) recruitment "
    "STATUS was not an audited attribute anywhere in the repo. Six records "
    "published Active or Recruiting for trials ClinicalTrials.gov records as "
    "COMPLETED, the oldest finished in 2015 -- the one wrong attribute a "
    "reader might act on.\n\n"
    "NCT04262479 was not stale, it was the wrong trial. Labelled 'DIAGNODE-3 "
    "(GAD-Alum intralymphatic vaccine)', Diamyd Medical, US/SE/FI/DE, T1D, "
    "Phase 3, n=330 'per ClinicalTrials.gov'. The registry record is "
    "GADinLADA: Norwegian University of Science and Technology, Norway and "
    "Sweden, LADA, Phase 2, n=14 ACTUAL, completed 2022-05-05. Every field "
    "but 'Sweden' belonged to a different trial. THIS IS AN EQUITY MAPPER, so "
    "the countries field is the product: a 14-patient Norwegian/Swedish study "
    "was on the map as a 330-patient four-country US-led phase 3, an error in "
    "the direction that makes trial access look broader than it is.\n\n"
    "Two more wrong-trial citations fell out once every mention was checked. "
    "NCT01319331 in build_drug_repurposing_islet.py carried indication 'Islet "
    "Transplant', outcome 'Islet graft survival', and the RESULT 'Improved "
    "graft function; reduced early islet loss' -- it is a 12-patient phase 1 "
    "study of AAT on the PROGRESSION of type 1 diabetes, which transplanted "
    "no islets. NCT04786262 in build_gap_deep_dives.py was cited for "
    "baricitinib; it is Vertex VX-880. Both withdrawn as UNSOURCED with no "
    "substitute invented (house rule, 2026-08-29).\n\n"
    "ISLET CHART: the modelled belatacept curve is gone rather than adjusted. "
    "The flag carried since 2026-09-14 framed it as a 15-point disagreement "
    "between the curve's 55% endpoint and the prose's 70%. Re-read against "
    "the abstract, that is the smallest of four problems: PMID 37359825 "
    "reports NO per-drug rate at any timepoint (70% is 7 of 10, 'four EFA, "
    "three BELA'); three of those seven had received a whole pancreas (PAI), "
    "so it is not an islet-transplant outcome; and nine of the curve's eleven "
    "points appear nowhere in the paper. Raising 55 to 70 would have left an "
    "invented annual curve terminating on a real number, which reads as "
    "better sourced than what it replaced. The chart now plots the paper's "
    "two reported timepoints as hollow markers with no connecting line, "
    "because nothing was measured between them. A fifth 10-year figure "
    "('~70% ... modeled trajectory') and the claim that 'belatacept "
    "recipients maintain superior graft function throughout follow-up' were "
    "withdrawn in the same pass -- the source's only per-drug number points "
    "the other way, four of seven responders being on efalizumab.\n\n"
    "The unsourced '20-30% at 10 years', flagged since 2026-09-14, was "
    "sourced by going to the literature rather than by picking one of the "
    "page's own numbers: Vantyghem MC et al., Diabetes Care 2019;42(11):"
    "2042-2049 (PMID 31615852), 28% (95% CI 13-45) by Kaplan-Meier, n=28. The "
    "first search result attributed that paper to 'Lablanche', who is not an "
    "author of it; identity and first author were verified live before use. "
    "The old range had no cohort, no citation and no interval, and its lower "
    "bound of 20% excluded the published confidence floor of 13%.\n\n"
    "All six remaining UNVETTED papers vetted; UNVETTED is now zero. All six "
    "resolved with exact identity agreement, so the value is in the "
    "over-reading notes: FINE-ONE (41780000) is n=242 over 6 MONTHS on a "
    "SURROGATE endpoint (UACR -25% vs placebo) with hyperkalemia 10.1% vs "
    "3.3% and a STEEPER eGFR fall than placebo -- not a hard-outcome trial, "
    "whatever 'phase 3 supporting an FDA approval' suggests. The BCG review "
    "(42738899) is the Faustman lab reviewing its own trials and states the "
    "HbA1c effect occurs 'without any recovery of pancreatic function', so "
    "BCG must never be filed under beta-cell preservation. 42760903 entered "
    "on the query 'islet transplant outcomes' and is mouse islets ex vivo "
    "with no transplant; screened out."
)

QUEUE_ADDS = [
    {'type': 'fix_pipeline', 'priority': 1, 'added': TODAY, 'target': (
        'APPLY TODAY\'S TWO STRUCTURAL LESSONS TO THE OTHER GATES, BECAUSE '
        'NEITHER WAS SPECIFIC TO THE GATE IT WAS FOUND IN. '
        '(a) ONE-SITE-PER-IDENTIFIER: audit_nct_identifiers.py checked '
        '`by_nct[nct][0]` and threw the rest away, hiding 4 defects behind '
        'clean first mentions. Any audit here that groups sites by identifier '
        'and then checks one representative has the same bug. Grep for '
        '`[0]` applied to a grouped-sites dict in audit_path_citations.py, '
        'audit_citation_identifiers.py, audit_prose_citation_titles.py and '
        'audit_citation_coordinates.py. MEASURE the site-vs-identifier counts '
        'in each report first: where sites > distinct ids, the difference is '
        'the number of assertions never examined. '
        '(b) PROSE-ONLY MATCHING: ENROLL_RE required the word "patients", so '
        'structured `\'enrollment\': 330` was invisible. Same question for '
        'every regex-driven gate -- does it read the dict-literal form of the '
        'claim it checks? This is the third time a dict-literal blind spot '
        'has been found (audit_gap_numbering 2026-09-20, this, and the '
        'GRAFT_DATA curve today, which was numbers in a dict that no prose '
        'gate could see).')},
    {'type': 'verify_citations', 'priority': 1, 'added': TODAY, 'target': (
        'RE-AUDIT THE REMAINING HAND-WRITTEN REGISTRY FIELDS THE WAY '
        'build_trial_equity_mapper.py WAS RE-AUDITED TODAY, AND EXPECT THE '
        'SAME HIT RATE. Eight of twelve records there disagreed with '
        'ClinicalTrials.gov and all twelve sat under a hand-written '
        '"# --- VERIFIED ---" banner. Those banners are now replaced with a '
        'dated, sourced line, but the same unverifiable-VERIFIED pattern '
        'still exists elsewhere: build_drug_repurposing_islet.py '
        'CLINICAL_TRIALS (one wrong-trial record found today, rest '
        'unchecked), build_gka_landscape.py, build_repurposing_dashboard_v2.py. '
        'A registry fact is not the kind of fact that stays checked -- four '
        'of today\'s six stale statuses changed AFTER the VERIFIED comment '
        'was written. Consider deriving these fields at build time from the '
        'nct cache instead of typing them.')},
    {'type': 'fix_pipeline', 'priority': 2, 'added': TODAY, 'target': (
        'SHORTEN THE NCT REGISTRY CACHE FOR STATUS-BEARING FIELDS. fetch() in '
        'audit_nct_identifiers.py caches for 30 days. That is fine for a '
        'title and wrong for a recruitment status, which is the attribute '
        'most likely to change and the one a reader may act on. Measured '
        'today: the cache held a 21-day-old copy and it happened to be '
        'current, but nothing guarantees that. Either cache status separately '
        'with a short TTL, or record the cache age beside each finding so a '
        'green result carries its own staleness.')},
    {'type': 'audit_gap', 'priority': 2, 'added': TODAY, 'target': (
        'DECIDE WHERE FINERENONE BELONGS, NOW THAT FINE-ONE IS VETTED. PMID '
        '41780000 is vetted CORPUS with an explicit ceiling: citable for '
        'albuminuria at 6 months in T1D CKD, NOT for kidney failure, eGFR '
        'slope, CV or mortality outcomes. Nothing in the hub cites it yet, '
        'which is the right state to decide from rather than to repair from. '
        'Two constraints that must travel with any row: finerenone is BRANDED '
        'and on-patent, so it does not belong in the generic-repurposing '
        'catalogue; and the trial\'s own eGFR result went the WRONG way '
        '(-5.6 vs -2.7), reversing on washout. Any card must state n=242, '
        '6 months, surrogate endpoint, and hyperkalemia 10.1% vs 3.3%.')},
    {'type': 'analysis', 'priority': 2, 'added': TODAY, 'target': (
        'SWEEP THE REPO FOR OTHER "MODELLED TRAJECTORY" SERIES PLOTTED AS '
        'DATA. Today removed one: an eleven-point annual belatacept curve in '
        'build_islet_outcomes.GRAFT_DATA, captioned "Modeled trajectory" in '
        'its own source comment and rendered in the same line weight and '
        'colour family as a 1,477-recipient registry curve. Nine of its '
        'eleven points were interpolation with a printed percentage label '
        'over every marker. NO GATE IN THIS REPO CAN SEE THIS CLASS: the '
        'numbers live in a dict, carry no citation to be checked, and the '
        'disclosure was in a comment a reader never sees. Grep for "model", '
        '"projected", "estimated", "trajectory", "extrapolat" near chart data '
        'structures in every builder. The renderer now supports '
        "style='points' for series that report only specific timepoints; use "
        'it rather than deleting a real two-point series.')},
]

CLOSE = [
    ('2026-09-21', 'audit_gap', 'RECONCILE THE REMAINING THREE 10-YEAR ISLET FIGURES'),
    ('2026-09-21', 'fix_pipeline', 'AUDIT EVERY GATE IN run_quality_improvements.py'),
    ('2026-09-14', 'audit_gap', 'RECONCILE THE BELATACEPT 10-YEAR NUMBER'),
    ('2026-09-19', 'analysis', 'VET PMID 41780000 (FINE-ONE)'),
]

RUN = {
    'date': TODAY,
    'day': 'Tuesday',
    'environment': ('HEALTHY. Sandbox mount, Python, live PubMed and '
                    'ClinicalTrials.gov all functional. git commit works from '
                    'the sandbox; git push still has no credential.'),
    'queue_items_processed': 5,
    'papers_vetted': 6,
    'papers_unvetted_remaining': 0,
    'gates_added': 2,
    'gates_extended': 1,
    'gate_false_positives_caught_before_shipping': 4,
    'builders_fixed': 5,
    'wrong_trial_citations_withdrawn': 3,
    'registry_fields_repaired': 10,
    'invented_chart_series_withdrawn': 1,
    'figures_sourced': 1,
    'changes_pushed': False,
    'pipeline_red_stages': ['publishgate (by design, needs a human push)',
                            'gapsubject (pre-existing human call, 9 of 15 gaps)'],
    'summary': SUMMARY,
}


def main():
    shutil.copy(STATE, STATE + '.bak2_' + TODAY)
    with open(STATE, encoding='utf-8') as fh:
        state = json.load(fh)

    state['last_run'] = TODAY
    state['last_updated'] = TODAY
    state.setdefault('run_history', []).append(RUN)

    # Close what this run actually finished.
    closed = 0
    remaining = []
    for item in state.get('work_queue', []):
        if isinstance(item, dict):
            t = item.get('target', '')
            if any(item.get('added') == d and item.get('type') == ty and t.startswith(pre)
                   for d, ty, pre in CLOSE):
                state.setdefault('closed_queue_items', []).append(
                    dict(item, closed_on=TODAY))
                closed += 1
                continue
        remaining.append(item)
    state['work_queue'] = remaining + QUEUE_ADDS

    state.setdefault('doctrine_notes', {})[TODAY] = (
        "A green stage count is evidence about the stages, not about the "
        "repository, and today it was wrong in two independent ways at once: "
        "a gate whose verdict could not reach the runner, and a gate that "
        "examined one mention of each identifier and discarded the rest. Both "
        "produce the same artifact -- a confident [OK] beside an unexamined "
        "defect. The general rule this suggests, which the next run should "
        "test rather than assume: before trusting any gate's green, ask what "
        "it would take for that gate to be INCAPABLE of red, and check that "
        "the number of things it examined matches the number of things there "
        "are. Today those two questions were worth twelve live defects."
    )

    with open(STATE, 'w', encoding='utf-8') as fh:
        json.dump(state, fh, indent=2)

    print('  RUN CLOSED %s' % TODAY)
    print('    queue items closed : %d' % closed)
    print('    queue items added  : %d' % len(QUEUE_ADDS))
    print('    open queue size    : %d' % len(state['work_queue']))
    print('    papers UNVETTED    : %d' % sum(
        1 for v in state['papers'].values() if v.get('status') == 'UNVETTED'))
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
