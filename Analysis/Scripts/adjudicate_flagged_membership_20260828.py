#!/usr/bin/env python3
"""Split FLAGGED into OFF_TOPIC and BACKGROUND, one paper at a time.

WHY THIS IS NOT A BULK OPERATION
--------------------------------
The obvious way to satisfy the P1 work item was to make FLAGGED a hard
exclusion everywhere, since extract_corpus_data.py already treats it that
way. Reading all 18 FLAGGED records before doing so showed that would have
been wrong, because FLAGGED has been carrying two incompatible meanings:

  "not a diabetes paper"        18794064 metastatic colon cancer
                                19237585 nicotinic receptors / epilepsy
                                20519905 endotoxin removal in septic shock

  "a diabetes paper whose
   evidence does not count"     42618537 metformin pyroptosis in HK-2 cells,
                                         evidence_tier IN_VITRO_ONLY
                                42611761 bibliometric analysis - counts
                                         PUBLICATIONS, contains no patients

Hard-excluding the second group deletes real, on-topic, correctly-cited 2026
diabetes papers on a tier judgement. That is a category error, and it is the
same error not_corpus_pmids.json was extended on 2026-08-26 to avoid when
RETRACTION was nearly filed under PROVENANCE.

THE DISTINCTION WAS ALREADY WRITTEN DOWN AND NEVER ENCODED
----------------------------------------------------------
This is not a new taxonomy invented today. The note stored against PMID
25714673 on 2026-04-20 reads, verbatim:

    "Flagged off-topic. Keep in paper_library but exclude from
     mechanism-evidence extraction."

That is exactly CITABLE-but-NOT-EVIDENCE. The repo had the right model four
months ago, wrote it into a free-text note field, and then had one boolean to
express it with. Every consumer since has had to guess which meaning applied.

WHAT EACH CLASS MEANS
---------------------
  OFF_TOPIC   not about this corpus. Must not be cited AND must not count as
              evidence. If it appears in live prose, the citation is wrong
              and needs repair or withdrawal, not just suppression.
  BACKGROUND  may be cited (definitional, methodological or mechanistic
              background) and must NOT count as corpus evidence for a
              diabetes claim.

Run once. Idempotent: re-running only rewrites the same fields.
"""

import json
import os
import shutil
from datetime import date

RESULTS = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'Results'))
STATE = os.path.join(RESULTS, 'agent_state.json')

TODAY = date.today().isoformat()

# Every entry below was decided by reading the paper's own stored
# flag_reason/issues_found and, where a live dashboard cited it, the
# citation context. No paper was classified from its title alone.
ADJUDICATION = {
    # ---- OFF_TOPIC: not about this corpus -------------------------------
    '18794064': ('OFF_TOPIC', 'Clin Colorectal Cancer 2008, recurrent metastatic colon cancer. No diabetes content.'),
    '19237585': ('OFF_TOPIC', 'Mol Pharmacol 2009, nicotinic receptor stoichiometry / epilepsy. No diabetes content.'),
    '20519905': ('OFF_TOPIC', 'Contrib Nephrol 2010, endotoxin removal in septic shock. No diabetes content.'),
    '20570966': ('OFF_TOPIC', 'Hum Mol Genet 2010, FUT2 non-secretor status and Crohn disease. Was published on Immunomod_LADA as an abatacept T1D trial; that is a different paper (21719096).'),
    '27512794': ('OFF_TOPIC', 'CADTH brief "Drugs for Smoking Cessation". Not a diabetes paper and not a journal article.'),
    '28397826': ('OFF_TOPIC', 'Nat Rev Clin Oncol 2017, immune escape in T-cell immunotherapy. Was published on Nutrition_LADA as Buzzetti LADA management; that is a different paper (28885622).'),
    '29562193': ('OFF_TOPIC', 'Immunity 2018, immune checkpoint blockade combinations in cancer. No diabetes content.'),
    '32243867': ('OFF_TOPIC', 'Braz J Infect Dis 2020, MMP-2/-9 and vitamin D in multiple sclerosis with HHV-6. Entered on an MMP/vitamin-D keyword collision.'),
    '35437333': ('OFF_TOPIC', 'Nat Metab 2022, formate and colorectal cancer. Previously mis-cited for dorzagliatin; the correct paper is 35551294.'),
    '37133585': ('OFF_TOPIC', 'NEJM 2023, trifluridine-tipiracil in refractory metastatic CRC. Previously mis-cited for teplizumab TN-10; the correct paper is 31180194.'),
    '41827829': ('OFF_TOPIC', 'Cells 2026, MIAMI-cell extracellular vesicles. Abstract contains no mention of diabetes, insulin, islet or beta cell.'),

    # ---- BACKGROUND: citable, not corpus evidence -----------------------
    '18662538': ('BACKGROUND',
                 'Massague, "TGFbeta in Cancer", Cell 2008. Cited CORRECTLY on Medical_Data_Dictionary as the definitional source for the TGF-beta term. The citation is true and load-bearing for a definition, so withdrawing it would delete a correct citation to satisfy a topic screen. It supplies no diabetes finding, so it must not count as corpus evidence.'),
    '25714673': ('BACKGROUND',
                 'Hu P et al., Am J Physiol Endocrinol Metab 2015. A genuine type 1 diabetes study (T1D mice; minocycline normalised MMP-2, IDO and CD39), so the 2026-04 "off-topic" label was too strong - but its own stored note already says "keep in paper_library but exclude from mechanism-evidence extraction". Cited on Generic_Drug_Catalog for minocycline, correctly by PMID.'),
    '42574278': ('BACKGROUND',
                 'Brief Bioinform 2026, G2DR genotype-first repurposing framework. Its own vetting record says "May be cited as METHODOLOGY in the repurposing arm. Must be excluded from corpus evidence counts and from any path." Sole case study is migraine.'),
    '42611761': ('BACKGROUND',
                 'J Vis Exp 2026 bibliometric analysis of mitochondrial research in diabetic nephropathy. On topic, but it counts PUBLICATIONS - it contains no patients and no measured outcome, so there is nothing in it that can be corpus evidence.'),
    '42612128': ('BACKGROUND',
                 'J Vis Exp 2026, network pharmacology + ML + in vivo validation of Danzhi Jiangtang Capsule in diabetic nephropathy. On topic and real; evidence_tier PRECLINICAL_ONLY. Citable as preclinical context, not as corpus evidence for a human claim.'),
    # ---- RETRACTED: a THIRD meaning that FLAGGED was also carrying ------
    # Found by this script refusing to run rather than by inspection: it
    # demanded a class for every FLAGGED paper and this one had none that
    # fit. Its exclusion is already correct via not_corpus_pmids.json
    # (provenance=RETRACTED, audit_retractions.py 2026-08-26); the point of
    # naming it here is that state['papers'] was ALSO calling it FLAGGED, so
    # a consumer reading state alone would have reported a withdrawn paper
    # as merely off-topic and lost the reason the evidence count moved.
    '38918878': ('RETRACTED',
                 'Diabetol Metab Syndr 2024, IL-1 inhibitors and colchicine in T2D. PubMed pubtype "Retracted Publication". Excluded from evidence AND from citation; the retraction, not the topic, is the disqualifier.'),

    '42618537': ('BACKGROUND',
                 'Diabetes Obes Metab 2026, metformin and high-glucose-induced pyroptosis in HK-2 cells via SIRT1. On topic and real; evidence_tier IN_VITRO_ONLY (immortalised proximal tubule line). Citable as mechanism, not as corpus evidence for a patient claim.'),
}


def main():
    with open(STATE, encoding='utf-8') as fh:
        state = json.load(fh)

    papers = state['papers']
    flagged = {p for p, r in papers.items() if r.get('status') == 'FLAGGED'}

    unhandled = sorted(flagged - set(ADJUDICATION))
    unknown = sorted(set(ADJUDICATION) - flagged)

    if unknown:
        # Not fatal: a paper may have been moved to not_corpus_pmids.json
        # since. But it must be visible, never silent.
        print('  [note] %d adjudicated PMID(s) are no longer FLAGGED: %s'
              % (len(unknown), ', '.join(unknown)))

    if unhandled:
        print('  [FAIL] %d FLAGGED paper(s) have no membership class. '
              'Refusing to run: an unclassified paper would silently inherit '
              'whichever meaning the reading consumer happens to assume, '
              'which is the defect this script exists to remove.'
              % len(unhandled))
        for p in unhandled:
            print('         %s  %s' % (p, str(papers[p].get('title', ''))[:70]))
        return 1

    shutil.copy2(STATE, STATE + '.bak_%s' % TODAY)

    counts = {}
    for pmid, (cls, why) in ADJUDICATION.items():
        if pmid not in papers:
            continue
        papers[pmid]['membership_class'] = cls
        papers[pmid]['membership_class_why'] = why
        papers[pmid]['membership_class_date'] = TODAY
        counts[cls] = counts.get(cls, 0) + 1

    state['last_updated'] = TODAY
    with open(STATE, 'w', encoding='utf-8') as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)

    print('  Classified %d FLAGGED paper(s): %s'
          % (sum(counts.values()),
             ', '.join('%s=%d' % kv for kv in sorted(counts.items()))))
    print('  [OK] every FLAGGED paper now states which of the two meanings applies.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
