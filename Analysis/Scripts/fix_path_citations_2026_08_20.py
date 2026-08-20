#!/usr/bin/env python3
"""2026-08-20: purge 17 off-topic external citations from research paths.

FINDING
-------
audit_path_citations.py (new today) resolved all 164 distinct external_pmids
cited by research paths against PubMed. 17 are real, resolvable records about
subjects with no connection to the path citing them: group A streptococci,
triple-negative breast cancer, borosilicate glass chemistry, C. elegans RNA
interference, phytoplankton metabarcoding, cesarean anesthesia, ageing-in-place
programs in China, osteoporosis screening tools, probiotic bakery products.

The most consequential is PMID 37889505. `teplizumab -> autoimmune` cites it as
the PROTECT trial, and the 2026-08-19 run history records that citation as
CHECKED EVIDENCE: "teplizumab->autoimmune cites TN-10 31180194 + PROTECT
37889505". 31180194 really is TN-10 (NEJM 2019). 37889505 is "Recent advances in
probiotic breads; a market trend in the functional bakery products". The real
PROTECT trial is PMID 37861217 (Teplizumab and beta-Cell Function in Newly
Diagnosed Type 1 Diabetes, NEJM 2023 Dec 7), verified today.

That is the lesson of this fix. The 2026-08-19 mirror sweep concluded 11 of 12
mirrored entries "hold full evidence" by confirming a PMID was PRESENT. Presence
is not correctness, and no gate in the pipeline was checking correctness.
audit_path_citations.py now does, every run.

WHAT THIS SCRIPT DOES
---------------------
1. REPLACES four citations where the correct PMID was verified today.
2. PURGES the remaining off-topic citations.
3. Removes PMID 39613428 from verapamil -> beta_cell external_pmids: that is the
   path's own CORPUS paper being used as its external validation - the same
   circularity caught on SGLT2i_NLRP3_DKD on 2026-08-17.

Purging is safe here: no path is left without evidence once the union across
both stores is taken. pioglitazone -> inflammation loses its only citation in
`paths` but retains PMIDs 16490432 and 20926154 (thiazolidinedione vs CRP
meta-analyses) in `validated_paths`. verapamil -> beta_cell loses both of its
`validated_paths` citations and gains the three verified verapamil trials.

NOT DONE HERE: replacing the 13 purged citations with the correct sources. Each
needs its own literature check, and guessing a replacement is how the wrong PMIDs
got here. Queued instead.
"""

import json
import os
import shutil
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(BASE, 'Results', 'agent_state.json')
TODAY = date.today().isoformat()

# PMID -> what it actually is. Every title confirmed via E-utilities today.
OFF_TOPIC = {
    '11961148': 'Erythromycin-resistant group A streptococci in schoolchildren in Pittsburgh',
    '19136609': 'Cardiac fibroblasts require focal adhesion kinase for proliferation and migration',
    '21067385': 'Triple-negative breast cancer',
    '22473097': 'The role of aspirin in cancer prevention',
    '29515440': 'Resveratrol - potential antibacterial agent against foodborne pathogens',
    '29987247': 'Performance of the Osteoporosis Self-Assessment Tool (OST)',
    '32332732': 'Targeting zonulin and intestinal epithelial barrier to prevent arthritis',
    '32398655': 'Structural investigation of borosilicate glasses containing lanthanide ions',
    '34107285': 'Impacts of diphenylamine NSAID halogenation on bioactivation risks',
    '35364937': 'Robust estimation of source bearing via minimizing Bhattacharyya distance',
    '36041242': 'Cesarean delivery anesthesia with paravertebral block and dexmedetomidine',
    '36547847': 'Is Nrf2 behind endogenous neuroprotection of the hippocampal CA2-4,DG region?',
    '37368959': 'Lifestyle Medicine Practitioners implementing lifestyle medicine',
    '37865119': 'Diversification of small RNA pathways in wild Caenorhabditis',
    '37889505': 'Recent advances in probiotic breads; functional bakery products',
    '37973095': 'Metabarcoding profiling of phytoplankton communities in algal blooms',
    '38934094': 'Value co-creation to improve ageing-in-place programs in China',
}

# (store, path) -> {wrong_pmid: correct_pmid}. Only verified replacements.
REPLACE = {
    ('paths', 'teplizumab -> autoimmune'): {
        '37889505': '37861217',   # PROTECT, Teplizumab and beta-Cell Function in
                                  # Newly Diagnosed T1D. N Engl J Med 2023 Dec 7.
    },
    ('paths', 'teplizumab -> T1D'): {
        '37865119': '37861217',   # C. elegans RNAi -> PROTECT trial.
    },
    ('validated_paths', 'verapamil -> beta_cell'): {
        '29987247': '29988125',   # Osteoporosis tool -> Verapamil and beta cell
                                  # function in adults with recent-onset T1D,
                                  # Nat Med 2018 Aug.
        '37368959': '36826844',   # Lifestyle medicine -> Effect of Verapamil on
                                  # Pancreatic Beta Cell Function in Newly
                                  # Diagnosed Pediatric T1D, JAMA 2023 Mar 28.
    },
}

# Extra verified citations to add after replacement.
ADD = {
    ('validated_paths', 'verapamil -> beta_cell'): [
        '40111679',               # Effect of Verapamil on Blood Glucose in T1D and
                                  # T2D: systematic review. Cardiovasc Drugs Ther 2026 Feb.
    ],
}

# Corpus papers wrongly listed as a path's own EXTERNAL validation (circularity).
CIRCULAR = {
    ('paths', 'verapamil -> beta_cell'): ['39613428'],
}


def ids_of(rec):
    ep = rec.get('external_pmids')
    return [str(x) for x in ep] if isinstance(ep, (list, dict)) else None


def main():
    backup = STATE + '.bak_citations_' + TODAY
    if not os.path.exists(backup):
        shutil.copy2(STATE, backup)

    with open(STATE, encoding='utf-8') as f:
        state = json.load(f)

    log = []
    for store in ('paths', 'validated_paths'):
        for key, rec in (state.get(store) or {}).items():
            if not isinstance(rec, dict):
                continue
            ids = ids_of(rec)
            if ids is None:
                continue
            original = list(ids)
            slot = (store, key)

            for wrong, right in REPLACE.get(slot, {}).items():
                if wrong in ids:
                    ids[ids.index(wrong)] = right
                    log.append(f'{store}:{key}  REPLACED {wrong} -> {right} '
                               f'({OFF_TOPIC.get(wrong, "?")})')

            for pmid in CIRCULAR.get(slot, []):
                if pmid in ids:
                    ids.remove(pmid)
                    log.append(f'{store}:{key}  REMOVED {pmid} (CIRCULAR: path\'s own corpus paper)')

            for pmid in list(ids):
                if pmid in OFF_TOPIC:
                    ids.remove(pmid)
                    log.append(f'{store}:{key}  PURGED   {pmid} ({OFF_TOPIC[pmid]})')

            for pmid in ADD.get(slot, []):
                if pmid not in ids:
                    ids.append(pmid)
                    log.append(f'{store}:{key}  ADDED    {pmid} (verified)')

            if ids != original:
                rec['external_pmids'] = ids
                rec.setdefault('citation_fixes', []).append({
                    'date': TODAY,
                    'before': original,
                    'after': ids,
                    'reason': 'off-topic external citations found by audit_path_citations.py',
                })

    state.setdefault('audit_notes', []).append({
        'date': TODAY,
        'type': 'off_topic_citation_purge',
        'summary': (
            f'Screened all 164 distinct external_pmids on research paths against PubMed titles. '
            f'17 resolved to papers on unrelated subjects and were purged or corrected across '
            f'14 path records. Four replacements verified: PROTECT is PMID 37861217, NOT 37889505 '
            f'("probiotic breads") which the 2026-08-19 run history recorded as checked evidence '
            f'for teplizumab -> autoimmune; verapamil -> beta_cell had an osteoporosis screening '
            f'tool (29987247) and a lifestyle-medicine survey (37368959) standing in for the '
            f'Nature Medicine 2018 (29988125) and JAMA 2023 (36826844) verapamil trials. '
            f'Also removed PMID 39613428 from verapamil -> beta_cell external_pmids: it is the '
            f'path\'s own corpus paper (circular validation, same defect as SGLT2i_NLRP3_DKD '
            f'on 2026-08-17). 13 purged citations still need correct replacements - queued, '
            f'not guessed. New gate audit_path_citations.py runs every build.'
        ),
        'purged': sorted(OFF_TOPIC),
    })

    state['last_updated'] = TODAY + 'T00:00:00'
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f'Applied {len(log)} citation correction(s):')
    for line in log:
        print('  ', line)
    print(f'\nBackup: {backup}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
