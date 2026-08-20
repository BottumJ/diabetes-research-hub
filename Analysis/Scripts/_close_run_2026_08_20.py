#!/usr/bin/env python3
"""Close out the 2026-08-20 run: reprioritise the queue, record run history."""

import json
import os
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(BASE, 'Results', 'agent_state.json')
TODAY = date.today().isoformat()

# Queue items completed today. Matched on a distinctive substring of `target`.
CLOSED = [
    'REGRESSION-TEST THE SUPPRESSION GATE EVERY RUN',
    'AUDIT THE REMAINING 15 MIRRORED ENTRIES',
    'EXTEND THE DEDUPE AUDIT TO THE OTHER BUILDERS',
    "CHECK WHETHER THE 'occurrences' FIELD CHANGES ANY PATH RANKING",
    'Run sync_docs_dashboards.py --check every run',
    'Run check_citation_mismatches.py EVERY run',
]

NEW_ITEMS = [
    {
        'priority': 1,
        'type': 'verify_citations',
        'added': TODAY,
        'target': (
            'REPLACE THE 13 PURGED OFF-TOPIC CITATIONS WITH CORRECT SOURCES. Purged today because '
            'they resolve to unrelated papers; each path still needs the source it was MEANT to '
            'cite, and guessing is exactly how the wrong PMIDs got in. One per path, verify each '
            'against PubMed before storing: rapamycin -> islet_transplant (was 11961148 group A '
            'streptococci); pioglitazone -> inflammation (was 19136609 cardiac fibroblasts - note '
            'validated_paths already holds the correct thiazolidinedione/CRP meta-analyses '
            '16490432 + 20926154, so this may just need the union); NF_kB -> inflammation (was '
            '21067385 breast cancer); metformin -> cardiovascular (was 22473097 aspirin/cancer); '
            'oxidative_stress -> inflammation (was 29515440 resveratrol/foodborne); '
            'dapagliflozin -> inflammation (was 32332732 zonulin/arthritis AND 37973095 '
            'phytoplankton); metformin -> inflammation (was 32398655 borosilicate glass AND '
            '34107285 NSAID halogenation); dapagliflozin -> nephropathy (was 35364937 '
            'Bhattacharyya distance); dapagliflozin -> cardiovascular (was 36041242 cesarean '
            'anesthesia); empagliflozin -> inflammation (was 36547847 Nrf2/hippocampus); '
            'empagliflozin -> nephropathy (was 38934094 ageing-in-place China). '
            'DO NOT close this item by deleting the paths - all of them retain other verified '
            'external evidence.'
        ),
    },
    {
        'priority': 1,
        'type': 'verify_publish',
        'added': TODAY,
        'target': (
            'research_paths.json IS AN ORPHAN AND THE DASHBOARD RENDERS FROM IT. Last written '
            '2026-05-04; NO script in Analysis/Scripts/ writes it - build_research_paths.py, '
            'statistical_analysis.py and path_store.py only READ it. Every per-path '
            'data_point_count on the published Research Paths page is a frozen snapshot that the '
            '2026-08-19 dedupe never reached, which is why 13 paths still display inflated counts '
            '(hydroxychloroquine -> T2D shows 32, real 15; metformin -> T2D shows 26, real 9). '
            'Two options: (a) write a builder that regenerates research_paths.json from '
            'extracted_corpus_data.json each run, or (b) retire the file and have the dashboard '
            'read the extraction output directly. Option (a) needs the original path-clustering '
            'rule, which is not in the repo - reconstruct it from the stored data_types / '
            'mechanisms / conditions histograms. Until this is fixed, per-path counts on the '
            'dashboard should be treated as indicative, not current.'
        ),
    },
    {
        'priority': 1,
        'type': 'validate_path',
        'added': TODAY,
        'target': (
            'DECIDE WHETHER dose_response BELONGS IN THE HEADLINE CORPUS COUNT. All 192 '
            'dose_response extractions - 46% of the 414 data points the site advertises - are '
            'bare dose labels ("360 mg verapamil", "120 mg tablets", "10 mg of dapagliflozin"). '
            'ZERO carry an outcome or mechanism token. Knowing which doses a trial used is '
            'legitimate metadata, but counting it as "evidence extracted from the corpus" '
            'overstates the evidentiary base by roughly half. Recommended: split the headline '
            'into "N findings + M dose/protocol descriptors" rather than one blended figure. '
            'This is a presentation decision with a credibility cost either way, so it needs a '
            'human call - an unattended run should not unilaterally restate the corpus headline.'
        ),
    },
    {
        'priority': 2,
        'type': 'verify_publish',
        'added': TODAY,
        'target': (
            'REVIEW THE TESTED DOSE_FRAGMENT_PATTERNS WIDENING (written and measured 2026-08-20, '
            'NOT applied). Current patterns allow only a short trailing-token list '
            '(OD|BID|TID|QD|daily|in|on), so "360 mg verapamil", "120 mg tablets" and "120 mg to" '
            'all escape the artifact filter - which is why verapamil -> T1D and '
            'verapamil -> beta_cell published at ranks #7 and #8 on 100% dose-label evidence. '
            'Proposed addition: r"^\\s*(?:(?:a\\s+)?dose\\s+of\\s+)?\\d+(?:\\.\\d+)?\\s*[Mm]?[Gg]'
            '(?:/[A-Za-z]+)?(?:\\s+[A-Za-z]+){0,3}\\s*$" plus a trailing-conjunction variant, '
            'keeping the MECHANISM_KEYWORDS veto. MEASURED EFFECT: +118 distinct strings flagged '
            '(all manually verified as dose labels, no findings among them), 0 regressions, but '
            'paths filtered off the dashboard go 6 -> 18 of 47. Removing a third of the page is '
            'not an unattended change. Decide: apply the pattern, or keep the paths and rely on '
            'the corpus_contribution=ARTIFACT marking applied today.'
        ),
    },
    {
        'priority': 2,
        'type': 'verify_citations',
        'added': TODAY,
        'target': (
            'EXTEND THE TOPIC SCREEN BEYOND external_pmids. audit_path_citations.py now checks '
            'that every PMID cited by a path resolves AND is on-topic, which found 17 bad '
            'citations that four earlier gates missed. But it only reads external_pmids. The same '
            'defect class can live in: key_sources free-text strings (which embed PMIDs in prose), '
            'gap evidence in extract_evidence.py output, and the PMIDs hardcoded in builder '
            'literals that validate_citations.py checks for EXISTENCE but not for RELEVANCE. '
            'Reuse the DOMAIN regex and the path-token fallback from audit_path_citations.py.'
        ),
    },
]


def main():
    with open(STATE, encoding='utf-8') as f:
        state = json.load(f)

    queue = state.get('work_queue', [])
    before = len(queue)
    kept = []
    closed = []
    for item in queue:
        target = str(item.get('target', ''))
        if any(marker in target for marker in CLOSED):
            closed.append(target[:70])
            continue
        kept.append(item)

    queue = NEW_ITEMS + kept
    # Age-based promotion: anything waiting since before July moves up one band.
    for item in queue:
        added = str(item.get('added', ''))
        if added and added < '2026-07-01' and item.get('priority', 9) > 2:
            item['priority'] = item['priority'] - 1
            item['promoted'] = TODAY
    queue.sort(key=lambda i: i.get('priority', 9))
    for pos, item in enumerate(queue):
        item['queue_pos'] = pos
    state['work_queue'] = queue

    state.setdefault('run_history', []).append({
        'date': TODAY,
        'day': 'Thursday',
        'papers_checked': 0,
        'paths_validated': 3,
        'issues_found': 5,
        'changes_pushed': False,
        'summary': (
            'Thu 2026-08-20 - THE CORPUS WAS CITING A BAKERY PAPER AS A PHASE 3 TRIAL. '
            '(1) OFF-TOPIC CITATIONS, 17 OF THEM. Screened all 164 distinct external_pmids on '
            'research paths against PubMed titles - something no existing gate did, because '
            'validate_citations.py scans .py source literals and never saw agent_state.json. '
            '17 resolve to real papers on unrelated subjects: group A streptococci, '
            'triple-negative breast cancer, borosilicate glass chemistry, C. elegans RNAi, '
            'phytoplankton metabarcoding, cesarean anesthesia, ageing-in-place programs in China. '
            'Worst case: PMID 37889505 ("Recent advances in probiotic breads") is cited by '
            'teplizumab -> autoimmune as the PROTECT trial, AND the 2026-08-19 run history '
            'records it as checked evidence. Real PROTECT is 37861217 (NEJM 2023), verified and '
            'substituted. verapamil -> beta_cell had an osteoporosis screening tool (29987247) '
            'and a lifestyle-medicine survey (37368959) standing in for Nat Med 2018 (29988125) '
            'and JAMA 2023 (36826844). 4 corrected, 13 purged, 0 paths left without evidence. '
            'New gate audit_path_citations.py wired into the pipeline; re-run clean at 146/146. '
            'The lesson: the 2026-08-19 mirror sweep certified 11 of 12 entries by confirming a '
            'PMID was PRESENT. Presence is not correctness. '
            '(2) A HIGH-CONFIDENCE PATH RESTING ON A FAILED TRIAL. Resolved all 9 bare '
            'journal-name key_sources across 3 paths. GLP1_RA -> neuroprotection was VALIDATED / '
            'HIGH on zero resolvable PMIDs; its flagship source is ELAD, now PMID 41326666, which '
            'MISSED ITS PRIMARY ENDPOINT (cerebral glucose metabolism, P = 0.14) and was null on '
            'ADCS-ADL (P = 0.65) and CDR-SoB (P = 0.81) in a population with NO DIABETES. '
            'Downgraded to PARTIALLY_VALIDATED / LOW. colchicine -> inflammation cut HIGH -> '
            'MEDIUM (lead source not PubMed-indexed, dropped) but gained a diabetes-specific '
            'hard-endpoint meta-analysis (41889274, MACE HR 0.79 in 2977 diabetic patients). '
            'SGLT2i -> beta_cell rating unchanged; its "PMID=PENDING" placeholder is now indexed '
            'as 40697602, a stored year was wrong, and the SR/MA turns out to be authored by MSD '
            'employees. Unresolvable source strings across both stores: 0. '
            '(3) research_paths.json IS AN ORPHAN. Last written 2026-05-04; nothing writes it, '
            'three scripts read it. Every per-path data_point_count on the published page is a '
            '107-day-old snapshot the dedupe never reached. Recomputed: 13 of 47 paths carry '
            'restated evidence; verapamil -> T1D (7 -> 0) and verapamil -> beta_cell (6 -> 0) '
            'fall from ranks #7/#8 to #46/#47. '
            '(4) 46% OF THE HEADLINE CORPUS IS DRUG LABELLING. All 16 unique dose_response '
            'records from PMID 39613428 are dose labels ("360 mg verapamil", "120 mg tablets"), '
            'and so are all 192 dose_response records corpus-wide - zero carry an outcome or '
            'mechanism. 12 paths marked corpus_contribution=ARTIFACT; statuses left alone because '
            'all 12 hold verified external evidence. Method validated by convergence: run blind '
            'it independently reproduced 4 artifact adjudications made 2026-08-19 by human '
            'table-reading. A widened dose-fragment regex was written and measured (+118 strings, '
            '0 regressions) but NOT applied - it would filter 18 of 47 paths off the page, which '
            'is a human call. Queued P2 with the measurements. '
            '(5) STALE HARDCODED COUNTS. Landing page said "202 indexed papers" against a real '
            '314; Extracted Evidence subtitle said 61 full-text papers while the paragraph below '
            'it rendered the live 69 - the page contradicted itself. Both now read at build time. '
            '(6) SUPPRESSION GATE NOW SELF-PROVING. regression_suppression_gate.py asserts against '
            'the PUBLISHED html, not the builder, across all 4 key spellings; negative-controlled '
            'by injecting each spelling and confirming exit 1. Pipeline 47/47 [OK], docs in sync, '
            'credibility sweep clean.'
        ),
        'queue_len': len(queue),
    })

    state['last_run'] = TODAY
    state['last_updated'] = TODAY + 'T00:00:00'
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f'Queue: {before} -> {len(queue)}  ({len(closed)} closed, {len(NEW_ITEMS)} added)')
    print('\nClosed:')
    for c in closed:
        print('  -', c)
    print('\nTop of queue:')
    for item in queue[:6]:
        print(f'  P{item.get("priority")} {item.get("type"):<18} {str(item.get("target"))[:78]}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
