#!/usr/bin/env python3
"""Vetting batch, 2026-09-22. Six UNVETTED papers -> classified.

Every identity field below (title, journal, year, first author, pub types) was
compared against a live PubMed esummary call this run, not against the record
that was written when the paper was ingested. All six resolved and all six
agreed exactly, so no identity defect is recorded.

Identity agreement is the cheap half. The notes below are the other half: what
each paper can and cannot be cited FOR. Three of the six carry a specific
over-reading risk, and in two cases the risk is the obvious reading.
"""

import json
import os
import shutil
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', '..'))
STATE = os.path.join(ROOT, 'Analysis', 'Results', 'agent_state.json')
TODAY = date.today().isoformat()

VETTING = {
    '41780000': {
        'status': 'VETTED',
        'membership_class': 'CORPUS',
        'design': 'Phase 3 RCT (FINE-ONE)',
        'citable_for': 'albuminuria (UACR) change at 6 months in T1D CKD',
        'not_citable_for': 'kidney failure, eGFR slope, cardiovascular or '
                           'mortality outcomes in type 1 diabetes',
        'vetting_note': (
            'Heerspink HJL et al., N Engl J Med 2026 (FINE-ONE). Identity '
            'verified live. THE OVER-READING RISK HERE IS THE OBVIOUS READING, '
            'and it is worth stating before any builder cites this. "Phase 3 '
            'RCT supporting an FDA approval" invites the sentence "finerenone '
            'improves kidney outcomes in type 1 diabetes". The trial does not '
            'support that sentence. n=242, duration 6 MONTHS, and the primary '
            'outcome is UACR -- a surrogate. Result: 25% greater UACR '
            'reduction than placebo (geometric mean ratio 0.75, 95% CI '
            '0.65-0.87). No hard kidney endpoint was measured. Two findings '
            'cut the other way and must travel with any citation: hyperkalemia '
            '10.1% vs 3.3% on placebo (2 discontinuations), and eGFR fell MORE '
            'on finerenone (-5.6 vs -2.7 mL/min/1.73m2), returning toward '
            'baseline during washout. The defensible claim is "reduces '
            'albuminuria over 6 months in T1D CKD; hard outcomes untested in '
            'this population".'),
    },
    '42739778': {
        'status': 'VETTED',
        'membership_class': 'CORPUS',
        'design': 'Narrative review',
        'citable_for': 'context and framing on islet/pancreas transplant and '
                       'CNI-sparing immunosuppression',
        'not_citable_for': 'any numeric endpoint',
        'vetting_note': (
            'Bellini MI & Papalois V, J Clin Med 2026. Identity verified live. '
            'Queued on 2026-09-21 as the paper that "may carry a registry '
            'figure that settles which cohort 20-30% means". IT CANNOT SETTLE '
            'IT, AND NOT ONLY BECAUSE THE ABSTRACT REPORTS NO SUCH RATE: it is '
            'a narrative review, so a registry number taken from it would be '
            'the registry quoted at one remove, which is the secondary-source '
            'substitution audit_baseline_citations.py exists to stop. The '
            '20-30% figure was instead sourced this run to the primary cohort '
            '(Vantyghem et al., PMID 31615852). Admitted as context: it is '
            'directly on Gap #3 and covers costimulation blockade and '
            'Treg-based immunoprotection, which touch Gaps #5 and #12.'),
    },
    '42738899': {
        'status': 'VETTED',
        'membership_class': 'CORPUS',
        'design': 'Narrative review by the originating investigators',
        'citable_for': 'BCG mechanism and the authors\' own trial programme, '
                       'attributed as such',
        'not_citable_for': 'independent confirmation of BCG efficacy; beta-cell '
                           'preservation of any kind',
        'vetting_note': (
            'Faustman DL, Hashiguchi S, Davis M, Kuhtreiber W; Cells 2026. '
            'Identity verified live. TWO CAUTIONS, BOTH LOAD-BEARING. (1) NOT '
            'INDEPENDENT: this is the Faustman laboratory reviewing the '
            'Faustman laboratory\'s own multi-dose BCG trials. It is evidence '
            'of what that programme reports, not corroboration of it, and any '
            'claim sourced here must name the authorship relationship. (2) A '
            'TRAP SPECIFIC TO THIS HUB: the abstract states the HbA1c '
            'improvement occurs "without any recovery of pancreatic function '
            'from its negligible baseline level". This hub organises much of '
            'its T1D/LADA work around beta-cell preservation, so BCG is one '
            'plausible mis-file away from being listed as a beta-cell agent. '
            'By its own authors\' account it is not one: the mechanism claimed '
            'is correction of aerobic glycolysis in lymphoid cells. Any row '
            'placing BCG under beta-cell preservation is wrong on the source\'s '
            'own terms.'),
    },
    '42760903': {
        'status': 'VETTED',
        'membership_class': 'SCREENED_OUT',
        'design': 'Preclinical, mouse islets ex vivo',
        'screened_out_reason': 'query artifact; no transplant outcome, no human data',
        'vetting_note': (
            'Fowlds K et al., J Biophotonics 2026. Identity verified live. '
            'Entered on the sweep query "islet transplant outcomes" and '
            'reports NO transplant outcome: mouse islets isolated by '
            'pancreatectomy, cultured ex vivo, photobiomodulation daily for 7 '
            'days, ~2-fold increase in insulin secretion at 3 days. No '
            'transplantation was performed, no animal received a graft, and '
            'the intervention is a light device rather than a repurposable '
            'agent. Screened out of outcome claims. Recorded rather than '
            'silently dropped so a later sweep does not re-ingest it and read '
            'the title as an outcomes paper.'),
    },
    '42753472': {
        'status': 'VETTED',
        'membership_class': 'PRECLINICAL_ONLY',
        'design': 'Preclinical (cell/rodent), plant-derived extracellular vesicles',
        'citable_for': 'NLRP3 mechanism in diabetic kidney disease, preclinical only',
        'not_citable_for': 'any clinical or human claim; drug-repurposing candidacy',
        'vetting_note': (
            'Zhou Y et al., Phytomedicine 2026, Xuzhou Medical University '
            'Department of Pathophysiology. Identity verified live. On-topic '
            'for the NLRP3/diabetic-kidney line, but it is a botanical '
            'extracellular-vesicle preparation in a basic-science model, not a '
            'generic drug and not a clinical agent. Admitted as mechanism '
            'evidence with a preclinical-only ceiling so it cannot drift into '
            'the repurposing catalogue, whose entries are marketed drugs.'),
    },
    '42739042': {
        'status': 'VETTED',
        'membership_class': 'CORPUS',
        'design': 'Integrative review',
        'citable_for': 'framing of the ferroptosis / pyroptosis / NRF2 axis in '
                       'diabetic microvascular complications',
        'not_citable_for': 'efficacy of any polyphenol; any numeric endpoint',
        'vetting_note': (
            'Garcia-Munoz AM et al., Nutrients 2026. Identity verified live. '
            'Integrative review, and its own language is hedged throughout -- '
            'dietary polyphenols "MAY influence this network". Admitted for '
            'framing only. Flagged because the hub\'s nutrition dashboards are '
            'the place where a hedged mechanism review most easily becomes an '
            'unhedged sentence: "polyphenols inhibit NLRP3 in diabetic '
            'nephropathy" is not what this paper says.'),
    },
}


def main():
    shutil.copy(STATE, STATE + '.bak_' + TODAY)
    with open(STATE, encoding='utf-8') as fh:
        state = json.load(fh)

    changed = []
    for pmid, fields in VETTING.items():
        rec = state['papers'].get(pmid)
        if rec is None:
            print('  [WARN] %s not in state; skipped' % pmid)
            continue
        before = rec.get('status')
        rec.update(fields)
        rec['vetted_date'] = TODAY
        rec['identity_verified_against'] = 'PubMed esummary, live, ' + TODAY
        changed.append((pmid, before, rec['status'], rec['membership_class']))

    state.setdefault('audit_notes', []).append({
        'date': TODAY,
        'note': ('Vetted the six remaining UNVETTED papers. All six resolved '
                 'live on PubMed with exact title/journal/year agreement, so '
                 'no identity defect. Three carry over-reading risks recorded '
                 'per paper: FINE-ONE (41780000) is a 6-month n=242 SURROGATE '
                 '(UACR) trial with a 3x hyperkalemia signal and a steeper '
                 'eGFR fall than placebo, not a hard-outcome trial; the BCG '
                 'review (42738899) is the Faustman lab reviewing its own '
                 'trials AND states the HbA1c effect occurs without beta-cell '
                 'recovery, so BCG must not be filed as a beta-cell agent; '
                 '42760903 is mouse islets ex vivo with no transplant at all '
                 'and was screened out as an artifact of the "islet transplant '
                 'outcomes" query.'),
    })

    with open(STATE, 'w', encoding='utf-8') as fh:
        json.dump(state, fh, indent=2)

    print('  VETTING BATCH 2026-09-22')
    for pmid, before, after, cls in changed:
        print('    %s  %s -> %s  [%s]' % (pmid, before, after, cls))
    remaining = sum(1 for v in state['papers'].values()
                    if v.get('status') == 'UNVETTED')
    print('    UNVETTED remaining: %d' % remaining)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
