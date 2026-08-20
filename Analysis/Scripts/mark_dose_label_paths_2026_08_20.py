#!/usr/bin/env python3
"""2026-08-20: mark paths whose entire corpus evidence is dose labels.

THE QUESTION ASKED
------------------
Work-queue item (P3, 2026-08-19): "CHECK WHETHER THE 'occurrences' FIELD CHANGES
ANY PATH RANKING ... Specifically re-rank verapamil -> T1D and verapamil ->
beta_cell, both sourced solely from 39613428."

THE ANSWER, WHICH IS WORSE THAN THE QUESTION ASSUMED
----------------------------------------------------
Three findings, in ascending order of seriousness.

1. research_paths.json was last written 2026-05-04 and NOTHING WRITES IT.
   build_research_paths.py only reads it. Every per-path data_point_count on the
   dashboard is a 107-day-old snapshot that the 2026-08-19 dedupe never touched.
   So the ranking was never recomputed and the question of "does the ranking
   change" had no basis to be asked yet.

2. Recomputing against the live dedupe_log: 13 of 47 paths carry restated
   evidence. verapamil -> T1D loses 7 of 7 data points; verapamil -> beta_cell
   loses 6 of 6. They ranked #7 and #8; corrected they rank #46 and #47 of 47.
   hydroxychloroquine -> T2D is 53% restatement (32 -> 15), metformin -> T2D 65%
   (26 -> 9).

3. Reading the surviving records rather than counting them: ALL 16 unique
   dose_response extractions from PMID 39613428 are dose LABELS -
   "360 mg verapamil", "120 mg tablets", "240 mg at", "120 mg less". Not one is
   a finding. Widening the check: all 192 dose_response records in the corpus
   (46% of the 414 headline total) are bare dose labels, none carrying an outcome
   or mechanism token. The verapamil paths are not merely inflated - their corpus
   contribution is a drug titration schedule.

CONVERGENT VALIDATION - why this method is trustworthy
------------------------------------------------------
Run blind over all 47 paths, the same arithmetic independently drives to zero
FOUR paths that were adjudicated as artifacts on 2026-08-19 by a completely
different route (a human reading the source table in PMID 35466661):
insulin_glargine -> T2D, atorvastatin -> T2D, metformin -> inflammation,
pioglitazone -> inflammation. Four for four, with no knowledge of those
adjudications. That agreement is the evidence that the two verapamil paths it
also drives to zero are real findings and not an artifact of the arithmetic.

WHAT THIS SCRIPT DOES - AND DELIBERATELY DOES NOT DO
-----------------------------------------------------
Marks the 12 affected paths corpus_contribution = ARTIFACT (the precedent set on
2026-08-19). It does NOT demote their status, because - unlike
insulin_glargine -> T2D, which had external_pmids = [] - every one of these 12
holds real external validation. verapamil -> beta_cell rests on Nature Medicine
2018 (29988125) and JAMA 2023 (36826844); hydroxychloroquine -> T2D on the Dutta
meta-analysis. Their ratings are externally sourced and stand. What was false was
the impression that the corpus independently corroborated them.

It also does NOT broaden DOSE_FRAGMENT_PATTERNS in build_research_paths.py.
The widened pattern was written and tested today: it catches 118 additional
strings with zero regressions, all verified dose labels. But it would filter 18
of 47 paths off the dashboard including well-validated ones, and removing a third
of the page is not a change an unattended run should make. Patch and measurements
are queued for review.
"""

import json
import os
import shutil
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(BASE, 'Results', 'agent_state.json')
TODAY = date.today().isoformat()

# path -> (stored_count, corrected_count, sole_or_main_source)
# Computed by audit_path_count_staleness.py against the live dedupe_log.
DOSE_LABEL_PATHS = {
    'verapamil -> T1D':                (7, 0, '39613428'),
    'verapamil -> beta_cell':          (6, 0, '39613428'),
    'hydroxychloroquine -> T2D':       (32, 15, '35466661'),
    'metformin -> T2D':                (26, 9, '35466661'),
    'dapagliflozin -> T2D':            (7, 6, '39843169'),
    'dapagliflozin -> nephropathy':    (3, 2, '39843169'),
    'metformin -> nephropathy':        (1, 0, '39843169'),
    'dapagliflozin -> cardiovascular': (2, 0, '39412512'),
    'dorzagliatin -> T2D':             (2, 0, '38783768'),
    'empagliflozin -> T2D':            (1, 0, '39412512'),
    'empagliflozin -> cardiovascular': (1, 0, '39412512'),
    'calcineurin -> islet_transplant': (1, 0, '32627352'),
}

NOTE = (
    'CORPUS CONTRIBUTION MARKED ARTIFACT 2026-08-20. Stored data_point_count {stored} -> '
    'corrected {corrected} once restated text and dose labels are removed (main source PMID '
    '{src}). The path\'s STATUS AND CONFIDENCE ARE UNCHANGED and rest on its external PMIDs, '
    'which were verified separately. What is corrected is the claim that the corpus supplies '
    'independent evidence depth here: the underlying extractions are drug dose labels '
    '(e.g. "360 mg verapamil", "120 mg tablets"), not findings. All 192 dose_response '
    'extractions in the corpus - 46% of the 414 headline data points - are bare dose labels '
    'carrying no outcome or mechanism. Do not cite this path\'s data_point_count as evidence '
    'of corroboration.'
)


def main():
    backup = STATE + '.bak_doselabel_' + TODAY
    if not os.path.exists(backup):
        shutil.copy2(STATE, backup)

    with open(STATE, encoding='utf-8') as f:
        state = json.load(f)

    marked = []
    for key, (stored, corrected, src) in DOSE_LABEL_PATHS.items():
        for store in ('paths', 'validated_paths'):
            rec = state.get(store, {}).get(key)
            if not isinstance(rec, dict):
                continue
            rec['corpus_contribution'] = 'ARTIFACT'
            rec['corpus_data_points_stored'] = stored
            rec['corpus_data_points_corrected'] = corrected
            existing = rec.get('notes') or ''
            addition = NOTE.format(stored=stored, corrected=corrected, src=src)
            if 'CORPUS CONTRIBUTION MARKED ARTIFACT 2026-08-20' not in existing:
                rec['notes'] = (existing + ' ' if existing else '') + addition
            marked.append(f'{store}:{key} ({stored} -> {corrected})')

    state.setdefault('audit_notes', []).append({
        'date': TODAY,
        'type': 'dose_label_corpus_contribution',
        'summary': (
            'research_paths.json has not been written since 2026-05-04 and no script writes it, '
            'so every per-path data_point_count on the dashboard predates the 2026-08-19 dedupe '
            'by 107 days. Recomputed against the live dedupe_log: 13 of 47 paths carry restated '
            'evidence. verapamil -> T1D (7 -> 0) and verapamil -> beta_cell (6 -> 0) lose ALL '
            'corpus evidence and fall from ranks #7 and #8 to #46 and #47 of 47. Reading the '
            'surviving records: all 16 unique dose_response extractions from PMID 39613428 are '
            'dose labels, and so are all 192 dose_response records corpus-wide - 46% of the 414 '
            'headline data points carry no outcome or mechanism. 12 paths marked '
            'corpus_contribution=ARTIFACT; statuses unchanged because all 12 hold verified '
            'external evidence. Method validated by convergence: run blind, it independently '
            'reproduced 4 artifact adjudications made on 2026-08-19 by human table-reading.'
        ),
        'paths_marked': sorted(DOSE_LABEL_PATHS),
    })

    state['last_updated'] = TODAY + 'T00:00:00'
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f'Marked {len(marked)} path record(s) corpus_contribution=ARTIFACT:')
    for m in marked:
        print('  -', m)
    print(f'\nBackup: {backup}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
