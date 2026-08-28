#!/usr/bin/env python3
"""Record the 2026-08-28 run and reprioritise the work queue."""

import json
import os
from datetime import date

RESULTS = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'Results'))
STATE = os.path.join(RESULTS, 'agent_state.json')
TODAY = '2026-08-28'

SUMMARY = (
    "Fri 2026-08-28 - THE REPO HAD ADJUDICATED 17 PAPERS OFF-TOPIC AND ENFORCED "
    "IT IN EXACTLY ONE PLACE. (1) THE P1 ITEM, WORKED AND FOUND TO BE UNDERSTATED. "
    "'SEAL THE INTAKE DOORS BY CLASS' was raised 2026-08-25 and carried unchanged "
    "on 2026-08-27. Tracing its five hand-rolled membership loaders showed they "
    "did not agree: extract_corpus_data.py read not_corpus + FLAGGED, "
    "extract_evidence.py and ingest_papers.py read the registry ONLY, "
    "reconcile_paper_index.py reported FLAGGED without excluding it. 18 papers "
    "carry status FLAGGED; only 1 was also in the registry. So 17 adjudicated-"
    "off-topic papers were excluded by one consumer and admitted by four, and 12 "
    "still had cached abstracts feeding extraction. (2) TWO LIVE MISCITATIONS, "
    "FOUND BY ENFORCING WHAT WAS ALREADY DECIDED. Immunod_LADA.html published "
    "PMID 20570966 as 'Orban et al., Abatacept Phase 2 in T1D'; it is FUT2 non-"
    "secretor status and Crohn's disease, Hum Mol Genet 2010. Nutrition_LADA.html "
    "published PMID 28397826 as Buzzetti's LADA management review; it is "
    "'Immunotherapy: Hiding in plain sight', Nat Rev Clin Oncol 2017 - both 2017 "
    "Nature Reviews titles, a transposition no topic screen can see. Both "
    "repaired live against NCBI (21719096 Orban Lancet 2011; 28885622 Buzzetti "
    "Nat Rev Endocrinol 2017), asserted titles replaced with PubMed's. Both "
    "papers had been FLAGGED since April and were published anyway for four "
    "months. (3) THE NAIVE FIX WOULD HAVE BEEN WRONG. Making FLAGGED a hard "
    "exclusion everywhere - what the queue item implies and what "
    "extract_corpus_data.py already did - deletes real on-topic papers, because "
    "FLAGGED was carrying TWO meanings: 'not a diabetes paper' (metastatic colon "
    "cancer) and 'a diabetes paper whose evidence does not count' (metformin "
    "pyroptosis in HK-2 cells, IN_VITRO_ONLY). The repo had written the "
    "distinction down on 2026-04-20 and had nowhere to put it: the note on PMID "
    "25714673 reads 'keep in paper_library but exclude from mechanism-evidence "
    "extraction'. corpus_membership.py now answers TWO questions - citable() and "
    "counts_as_evidence() - across five kept-distinct disqualifiers; all 18 "
    "FLAGGED papers classified one at a time (11 OFF_TOPIC, 6 BACKGROUND, 1 "
    "RETRACTED, the last surfaced only because the adjudicator refused to run "
    "with any paper unclassified). (4) THE CLASS GATE, AND WHAT IT CAUGHT "
    "IMMEDIATELY. audit_unguarded_pmid_readers.py fails any LIVE script reading "
    "abstracts/, fulltext/ or the index without importing corpus_membership, and "
    "runs a positive control first so a zero from a broken detector cannot pass "
    "as a clean repo. First run found THREE more unguarded readers no leak had "
    "surfaced: validate_citations.py (a SIXTH loader), build_corpus_analysis.py "
    "(a SEVENTH notion of membership, the index's own corpus_status field), and "
    "rebuild_website.py, whose landing-page headline counted every indexed "
    "record including the retracted one. All rewired. (5) A COUNT NEVER ANSWERS "
    "'OF WHAT'. audit_path_evidence_design.py grades each live path by PubMed "
    "publication type. The FOUR highest-ranked paths by data-point count all "
    "rest on no primary data: ranks 1-2 on a meta-analysis whose scraped numbers "
    "cannot be attributed to the pooled estimate rather than to a tabulated "
    "trial, ranks 4-5 (verapamil -> T1D, verapamil -> beta_cell) on a clinical "
    "trial PROTOCOL. Ranking by count is inversely related to evidence quality "
    "at the top of this dashboard. SYNTHESIS_ONLY was split from NARRATIVE_ONLY "
    "deliberately: calling a systematic review WEAK would be backwards. "
    "18 paths graded: PRIMARY 9, NARRATIVE_ONLY 5, SYNTHESIS_ONLY 2, NO_RESULTS 2. "
    "(6) THE VERAPAMIL PATHS FINALLY HAVE AN EXTERNAL ANCHOR - PARTIAL. PMID "
    "40111679 (Tu S, Cardiovasc Drugs Ther 2026;40(1):347-359), 8 RCTs, 1100 "
    "patients: HbA1c WMD -0.45% (95% CI -0.66,-0.23) p<0.001 from 7 trials; "
    "C-peptide AUC WMD +0.27 pmol/mL (95% CI 0.21,0.32) p<0.0001 from TWO. Rated "
    "PARTIALLY_VALIDATED, not VALIDATED, because the C-peptide result is the one "
    "that speaks to beta-cell preservation and it pools two trials. Ver-A-T1D "
    "primary results are still NOT in PubMed; the EASD Vienna 2025 presentation "
    "is press coverage and is not citable here. Also recorded: absence of "
    "verapamil from the 11 winners in PMID 40598585 (BMC Med 2025 network MA) is "
    "a SCOPE exclusion - that review covers immunotherapies - and must not be "
    "read as a negative result. (7) THE COORDINATE GATE WENT RED ON THE RECORD OF "
    "YESTERDAY'S FIX. All 5 failures were inside _run_2026_08_27.py, quoting the "
    "miscitations it repaired; 4 were proximity artifacts of scanning prose about "
    "citations. The two coordinates that also appear in LIVE builders were "
    "hand-checked and both correct. Split LIVE vs AUDIT_TRAIL - the third time "
    "this repo has hit that shape - and proved the exemption is scoped by "
    "injecting a fabricated coordinate into a live builder and confirming the "
    "gate still failed. (8) AND THE REPAIR NOTE ITSELF BECAME A CITATION. The "
    "Buzzetti fix was first written as an HTML comment; postprocess_dashboards.py "
    "linkified the quoted dead PMID inside it and put it back on the published "
    "page - the exact shape (a PMID in a comment) that admitted 12345678 to this "
    "corpus. Moved into the builder. Pipeline 54 -> 56 steps, all [OK]. "
    "Extraction 232 data points from 53 papers."
)

CLOSE = [
    'SEAL THE REMAINING INTAKE DOORS BY CLASS',   # both copies, 08-25 and 08-27
    'Screen the 11 UNSCREENED_ORPHAN papers',
    'Re-audit every path whose corpus evidence is a REVIEW ARTICLE only',
]

NEW_ITEMS = [
    dict(priority=1, type='user_action_required', added=TODAY, target=(
        'HUMAN CALL, NOW WITH NUMBERS: THE TWO VERAPAMIL PATHS RANK 4TH AND 5TH ON '
        'A PROTOCOL, AND THE BEST EXTERNAL EVIDENCE FOR THEM POOLS TWO TRIALS. The '
        '2026-08-22 item asked whether paths resting on PMID 39613428 (Ver-A-T1D '
        'PROTOCOL, no results) should rank. Today they were graded NO_RESULTS by '
        'design, and an external anchor was found: PMID 40111679, a 2026 SR/MA of 8 '
        'RCTs, 1100 patients. It supports verapamil on GLYCAEMIA firmly (HbA1c WMD '
        '-0.45%, 7 trials) and on BETA-CELL PRESERVATION weakly (C-peptide AUC WMD '
        '+0.27 pmol/mL from 2 trials). Ver-A-T1D results remain unpublished in '
        'PubMed as of today. Three options and none is obviously right: (a) keep '
        'the paths, re-source them to 40111679 and re-rank them below the PRIMARY '
        'paths; (b) split them into verapamil->glycaemia (supported) and '
        'verapamil->beta_cell (thin); (c) suspend them until Ver-A-T1D publishes. '
        'This is a scientific framing decision, not a data-repair task.')),
    dict(priority=1, type='fix_pipeline', added=TODAY, target=(
        'RANKING IS STILL BY DATA-POINT COUNT, WHICH TODAY WAS SHOWN TO BE '
        'INVERSELY RELATED TO EVIDENCE QUALITY AT THE TOP. path_evidence_design.json '
        'now grades all 18 live paths, and the top four are SYNTHESIS_ONLY, '
        'SYNTHESIS_ONLY, NO_RESULTS, NO_RESULTS. The grade is stored and printed '
        'but build_research_paths.py does not read it, so the published Research '
        'Paths dashboard still orders by count alone. Either sort by (tier, count) '
        'or render the tier badge on every card - preferably both. Until then the '
        'dashboard invites the reader to draw exactly the wrong conclusion, and it '
        'does so more confidently now that the grading exists and is unused.')),
    dict(priority=2, type='verify_citations', added=TODAY, target=(
        'THE OTHER 12 BACKGROUND AND OFF_TOPIC PAPERS WERE CHECKED FOR PRESENCE ON '
        'THE SITE, NOT FOR CORRECTNESS OF THEIR PROSE. Today confirmed 0 uncitable '
        'PMIDs render on any dashboard except the verification page, which must '
        'show them. But the 6 BACKGROUND papers ARE still cited by design, and only '
        'two of them (18662538 TGF-beta in the data dictionary, 25714673 minocycline '
        'in the generic drug catalog) had their citation prose read against the '
        'actual paper. Run audit_builder_title_agreement.py and '
        'audit_citation_coordinates.py restricted to the BACKGROUND set and confirm '
        'each surviving citation says what its paper says. A BACKGROUND paper is by '
        'definition cited for a claim it was not written to support, which is the '
        'condition under which paraphrase drifts.')),
    dict(priority=2, type='audit_gap', added=TODAY, target=(
        'GRADE THE 15 GAPS BY EVIDENCE DESIGN THE WAY THE PATHS NOW ARE. '
        'audit_path_evidence_design.py reads research_paths.json only. The gap '
        'tiers (GOLD/SILVER/BRONZE) were assigned by independent-source COUNT, the '
        'same metric just shown to mislead on paths - a gap can hold two '
        'independent narrative reviews and be SILVER. Extend the audit to '
        'gap_evidence.json and report, for each gap, how many of its papers report '
        'primary data. Expect at least one demotion; do not pre-announce which.')),
    dict(priority=3, type='fix_pipeline', added=TODAY, target=(
        'MAKE THE HTML-COMMENT INTAKE DOOR IMPOSSIBLE RATHER THAN REMEMBERED. '
        'postprocess_dashboards.py linkifies PMIDs inside HTML comments; that is '
        'how a repair note written today put a dead PMID back on a published page, '
        'and it is the same shape that admitted 12345678. Two fixes, both cheap: '
        'strip HTML comments before linkifying, and have the linkifier refuse any '
        'PMID that corpus_membership marks uncitable.')),
]


def main():
    with open(STATE, encoding='utf-8') as fh:
        state = json.load(fh)

    state.setdefault('run_history', []).append({
        'date': TODAY,
        'day': 'Friday',
        'papers_checked': 29,          # 18 FLAGGED adjudicated + 11 orphans
        'paths_validated': 2,
        'paths_graded': 18,
        'issues_found': 8,
        'changes_pushed': False,
        'summary': SUMMARY,
    })

    queue = state.get('work_queue', [])
    kept, closed = [], []
    for item in queue:
        target = item.get('target', '')
        if any(c in target for c in CLOSE):
            closed.append(item)
        else:
            kept.append(item)

    state.setdefault('closed_queue_items', []).extend(
        [{'closed': TODAY, 'item': c} for c in closed])

    kept.extend(NEW_ITEMS)
    kept.sort(key=lambda i: (i.get('priority', 9), i.get('added', '')))
    state['work_queue'] = kept

    state['last_run'] = TODAY
    state['last_updated'] = TODAY
    state['last_path_validation_batch'] = TODAY

    with open(STATE, 'w', encoding='utf-8') as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)

    print('  Closed %d queue item(s); added %d; queue now %d'
          % (len(closed), len(NEW_ITEMS), len(kept)))
    print('  [OK]')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
