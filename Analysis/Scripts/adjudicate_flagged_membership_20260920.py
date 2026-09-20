#!/usr/bin/env python3
"""Classify the four FLAGGED papers that had no membership_class.

WHAT THIS IS NOT
----------------
It is NOT a reversal of the 2026-08-28 adjudication, and it is not the
semantic call the 2026-09-19 run queued for a human ("should status=FLAGGED
exclude a paper from the corpus?"). That question is still open and is not
answered here.

It is the NARROWER question that 2026-09-19 folded into the same bucket and
should not have: should a MISSING FIELD exclude a paper? corpus_membership.py
says in its own docstring that it must not -

    "A FLAGGED paper with no membership_class is a bug, not a default.
     Silently picking a meaning here is exactly how the five divergent
     loaders arose."

- and then picks a meaning anyway, because FLAGGED_UNCLASSIFIED is a member of
both excluded_pmids() and uncitable_pmids(). Nothing in the repo calls
unclassified(), so the promised audit does not exist. Nothing calls citable()
either - measured 2026-09-20, it had ZERO call sites - so the module could
report a paper uncitable while it sat on published pages and no stage noticed.

WHAT WAS MEASURED (2026-09-20, before any change)
-------------------------------------------------
  corpus_membership verdict      cited in builder src   present under docs/
  25940230  citable=False         build_nutrition_lada.py      2 pages
  34021020  citable=False         build_immunomod_lada.py,     4 pages
                                  build_lada_model.py,
                                  build_nutrition_lada.py
  37026004  citable=False         (prose only)                 1 page
  42674789  citable=False         (prose only)                 1 page

All four were absent from paper_library/index.json. The eviction ledger gives
the reason for each, verbatim:

    "FLAGGED in agent_state.json with no class recorded"

That is a blank field offered as the justification for deleting three primary
human studies and one protocol. All four PMIDs were re-verified live against
NCBI esummary on 2026-09-20; titles and journals agree with the stored
records. They are real papers and they are on topic.

THE CLASSIFICATIONS, AND WHERE EACH COMES FROM
----------------------------------------------
Each is transcribed from what the paper's OWN vetting record already says in
prose. None of them is a new judgement about the science.
"""

import json
import os
import shutil
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Results'))
STATE = os.path.join(RESULTS, 'agent_state.json')
TODAY = datetime.now().strftime('%Y-%m-%d')

ADJUDICATION = {
    # -------------------------------------------------------------- CORPUS
    # Its record reads "2026-09-18 REPAIRED IN PLACE, THREE DEFECTS ON ONE
    # CITATION" and every defect is in the PROSE: wrong author (second, not
    # first), "landmark trial" for what is an overview, and the 30% CVD hazard
    # reported as the diabetes number. The paper's own diabetes result -
    # 273 incident cases in 3,541 non-diabetic participants, HR 0.60
    # (0.43-0.85) MedDiet+EVOO, HR 0.82 (0.61-1.10) MedDiet+nuts - is real
    # evidence and is now cited correctly. Nothing disqualifies it.
    '25940230': ('CORPUS',
                 'PREDIMED overview, Prog Cardiovasc Dis 2015;58(1):50-60. FLAGGED 2026-09-18 as a PROSE repair, not a membership judgement: the published 30% was the CVD hazard (HR 0.70, 288 events), while the incident-diabetes result is HR 0.60 (0.43-0.85) for MedDiet+EVOO and a non-significant HR 0.82 (0.61-1.10) for MedDiet+nuts, in 3,541 non-diabetic participants. Real, on topic, correctly cited since the repair. Downstream use must carry the arm and the CI; it must not carry the 30%.'),

    # DIAGNODE-2. Flagged because build_nutrition_lada.py headed a TYPE 1
    # trial "GAD-Alum Immunotherapy in LADA". The misdescription was the
    # defect. The trial is a Phase IIb double-blind RCT, n=109, published in
    # Diabetes Care - among the strongest designs in this corpus.
    '34021020': ('CORPUS',
                 'DIAGNODE-2, Diabetes Care 2021. FLAGGED 2026-09-18 for a POPULATION MISATTRIBUTION in the prose - a type 1 trial (n=109, age 12-24, duration 7-193 days) published under a LADA heading - plus a wrong first author and a "dose-dependent" claim about a single-dose trial. Phase IIb double-blind placebo-controlled RCT; the design is a corpus strength, not a disqualifier. Downstream use must carry that the primary endpoint was NOT met in the full analysis set (TER 1.091, 95% CI 0.845-1.408, P=0.50) and that the DR3-DQ2 effect (TER 1.557, 1.126-2.153, P=0.0078) is a genotype subgroup of 29 vs 17.'),

    # The record adjudicates itself in so many words: "Flagged, not rejected -
    # the finding stands, the framing did not." State separately calls it
    # LOAD-BEARING for Gap #11. Excluding it is the one outcome no reading of
    # its own record supports.
    '37026004': ('CORPUS',
                 'CITR HLA-DR registry analysis, Front Immunol 2023;14:1110544. Its own vetting record reads "Flagged, not rejected - the finding stands, the framing did not", and state calls it LOAD-BEARING for the Gap #11 hypothesis. The flag records a DENOMINATOR that must travel with the claim: 965 recipients and 2327 donors screened, 87 single-infusion recipients analysed, and the 78%/24%/35% five-year insulin-independence contrast turns on group B, n=11. Retrospective registry subgroup; the authors write "suggests". Any downstream use must carry n=11 and must not be phrased causally.'),

    # ---------------------------------------------------------- BACKGROUND
    # The only one of the four that is a genuine evidence disqualifier, and
    # its record already states the rule: "reports NO findings and must not
    # contribute evidence weight to any path or gap." That is BACKGROUND as
    # this module defines it - citable, does not count. It is NOT off-topic
    # and must stay reachable, because the watch item depends on finding it
    # again when the results paper appears.
    '42674789': ('BACKGROUND',
                 'Quebec algorithmic-classification cohorts, BMJ Open 2026;16(8):e109209. STUDY PROTOCOL - NO RESULTS. Its intake record already sets the rule: "reports NO findings and must not contribute evidence weight to any path or gap", flagged pre-emptively because this corpus was burned once by ranking research paths on a protocol (PMID 39613428, Ver-A-T1D). BACKGROUND is that rule stated in the field rather than in prose: citable as a watch item for Gap #10, contributes no evidence. Re-classify to CORPUS only when the results publication appears.'),
}


def main():
    with open(STATE, encoding='utf-8') as fh:
        state = json.load(fh)

    papers = state['papers']

    missing = [p for p in ADJUDICATION if p not in papers]
    if missing:
        print('  [FAIL] %d adjudicated PMID(s) are not in state[papers]: %s'
              % (len(missing), ', '.join(missing)))
        return 1

    already = [p for p, r in papers.items()
               if r.get('status') == 'FLAGGED'
               and not r.get('membership_class')
               and p not in ADJUDICATION]
    if already:
        # Not fatal - a new unclassified paper is exactly what the new audit
        # is for - but it must be visible from this script too, because this
        # script is where a human looks when the audit fails.
        print('  [note] %d FLAGGED paper(s) still unclassified and not '
              'handled here: %s' % (len(already), ', '.join(sorted(already))))

    shutil.copy2(STATE, STATE + '.bak_%s' % TODAY)

    counts = {}
    for pmid, (cls, why) in ADJUDICATION.items():
        rec = papers[pmid]
        if rec.get('membership_class'):
            print('  [skip] %s already classified as %s'
                  % (pmid, rec['membership_class']))
            continue
        rec['membership_class'] = cls
        rec['membership_class_why'] = why
        rec['membership_class_date'] = TODAY
        rec['membership_class_source'] = (
            'adjudicate_flagged_membership_20260920.py - transcribed from the '
            "paper's own vetting record; PMID re-verified live via NCBI "
            'esummary on %s' % TODAY)
        counts[cls] = counts.get(cls, 0) + 1
        print('  [set ] %-10s -> %s' % (pmid, cls))

    state['last_updated'] = TODAY
    with open(STATE, 'w', encoding='utf-8') as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)

    print()
    print('  classified %d paper(s): %s'
          % (sum(counts.values()),
             ', '.join('%s=%d' % kv for kv in sorted(counts.items()))))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
