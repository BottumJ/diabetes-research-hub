#!/usr/bin/env python3
"""2026-08-20 adjudication: resolve bare journal-name key_sources to PMIDs.

Work-queue item P2 (added 2026-08-19) flagged that the 2026-08-19 mirror sweep
only asked "is there ANY evidence in either store". It never asked whether that
evidence RESOLVES. Three paths carried key_sources that were bare
journal-name strings with no PMID -- unresolvable claims are the same weakness
as the bare URLs fixed on the oxidative_stress paths, because nobody can check
them and nobody can tell a real citation from an invented one.

All nine strings were resolved against the NCBI E-utilities API today. Two of
the three paths survive with sources upgraded. One does not survive its own
flagship citation.

THE FINDING: GLP1_RA -> neuroprotection was rated VALIDATED / confidence HIGH.
Its lead source is the ELAD trial, now PMID 41326666 (Nat Med 2026;32(1):353-361).
ELAD MISSED ITS PRIMARY ENDPOINT: no difference in cerebral glucose metabolism
(diff -0.17, 95% CI -0.39 to 0.06, P = 0.14). ADCS-ADL (P = 0.65) and CDR-SoB
(P = 0.81) were null. One secondary domain, ADAS-Exec, was nominally positive on
an UNADJUSTED P = 0.01. The 204 participants explicitly had NO DIABETES. The
stored note -- "2025 phase 2b liraglutide AD trial + large propensity-matched
cohorts show 40-70% lower dementia incidence" -- reads the failed trial and the
observational cohorts as one converging body of evidence. They are not: the
40-70% figure comes only from the cohorts, and the trial is a negative result.
Downgraded to PARTIALLY_VALIDATED / LOW.
"""

import json
import os
import shutil
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(BASE, 'Results', 'agent_state.json')
TODAY = date.today().isoformat()

# ---------------------------------------------------------------------------
# Resolutions verified today via eutils esearch + esummary + efetch.
# Every PMID below was confirmed to exist AND to carry the title the stored
# string described. Nothing here is inferred from a search-engine snippet.
# ---------------------------------------------------------------------------
RESOLVED = {
    'colchicine -> inflammation': {
        'status': 'VALIDATED',
        'confidence': 'MEDIUM',          # was HIGH
        'date': TODAY,
        'key_sources': [
            'PMID 40648980 - Role of NLRP3 Inflammasome in T2DM and Its Macrovascular '
            'Complications. J Clin Med 2025 Jun 29. REVIEW (mechanistic narrative, not primary data). '
            'Resolves the former bare string "MDPI J Clin Med 2025".',
            'PMID 41889274 - Effect of colchicine for secondary prevention of cardiovascular '
            'diseases in individuals with diabetes: meta-analysis of randomized trials. '
            'Diab Vasc Dis Res 2026;23(2). 5 RCTs, n=2977 WITH DIABETES, MACE HR 0.79 '
            '(95% CI 0.67-0.94, p=0.006) at 0.5 mg/day over median 28.6 months. '
            'PROSPERO CRD42024575366. HARD CLINICAL ENDPOINT, diabetes-specific.',
            'Molecular Medicine Reports 2025 (PMC12395217) - NLRP3 inflammasome in diabetes '
            'and complications. PMCID only; PMID not resolved - treat as supporting, not load-bearing.',
        ],
        'notes': (
            'CONFIDENCE CUT HIGH -> MEDIUM on 2026-08-20, and the source list rebuilt. '
            'The former lead source "Exploration Pub 2025 - New perspectives on NLRP3 '
            'inflammasome-colchicine and metabolic syndrome" is NOT PubMed-indexed and could '
            'not be resolved to a PMID by title, journal or author search; it is DROPPED. '
            'A citation nobody can look up cannot carry a HIGH rating. '
            'What replaces it is stronger in one dimension and weaker in another. Stronger: '
            'PMID 41889274 is a diabetes-specific meta-analysis of 5 RCTs on a HARD endpoint '
            '(MACE), which the path previously lacked entirely. Weaker: the path as written is '
            'colchicine -> INFLAMMATION, and 41889274 measures cardiovascular events, not '
            'inflammatory markers. The direct marker-level evidence IN A DIABETES POPULATION is '
            'still thin. EXPLICITLY EXCLUDED: PMID 36643381 (Biomed Hub 2022, low-dose colchicine '
            'on hs-CRP in CAD+T2DM) surfaced in the search and looks like exactly the missing '
            'evidence, but it is a PROTOCOL paper - "patients WILL BE randomly assigned", no '
            'results reported. Recorded here so a future run does not re-find it and mistake it '
            'for a results publication. '
            'RETAINED WARNING: Springer Diabetology & Metabolic Syndrome colchicine review '
            '(PMID 38918878) is RETRACTED - must not be cited.'
        ),
        'external_pmids': ['40648980', '41889274'],
    },

    'SGLT2i -> beta_cell': {
        'status': 'PARTIALLY_VALIDATED',   # unchanged
        'confidence': 'MEDIUM',            # unchanged
        'date': TODAY,
        'key_sources': [
            'PMID 35563495 - Effects of Sodium-Glucose Co-Transporter-2 Inhibitors on Pancreatic '
            'beta-Cell Mass and Function. Int J Mol Sci 2022 May 4. REVIEW. '
            'Resolves the former bare string "MDPI IJMS 2022".',
            'PMID 32712220 - Dapagliflozin promotes beta cell regeneration by inducing pancreatic '
            'endocrine cell phenotype conversion in type 2 diabetic mice. Metabolism 2020 Oct. '
            'MURINE. Resolves the former bare string "ScienceDirect 2020".',
            'PMID 35180212 - SGLT2 inhibitors therapy protects glucotoxicity-induced beta-cell '
            'failure in a mouse model of human KATP-induced diabetes. PLoS One 2022. MURINE. '
            'Resolves the former bare string "PLOS One 2021" - the stored YEAR WAS WRONG (2022).',
            'PMID 40697602 - SGLT2 inhibitors improve insulin resistance and beta-cell function in '
            'type 2 diabetes: a meta-analysis. World J Diabetes 2025 Jul 15;16(7):107335. '
            '24 RCTs; HOMA-IR MD -0.81 (95% CI -1.11 to -0.52, I2=82%); HOMA-beta MD +7.90 '
            '(95% CI 5.44-10.37, I2=74%); GRADE MODERATE. RESOLVES the former "PMID=PENDING".',
            'Diabetology International 2019 (PMC6357236) - SGLT2 inhibitors and protection against '
            'beta cell failure. PMCID only; supporting, not load-bearing.',
        ],
        'notes': (
            'RATING UNCHANGED (PARTIALLY_VALIDATED / MEDIUM) - this update is a citation-integrity '
            'fix, not a re-rating. Four bare journal strings resolved to PMIDs on 2026-08-20, '
            'including the "PMID=PENDING" placeholder carried since 2026-08-08, which is now '
            'PubMed-indexed as 40697602. One stored fact was WRONG: the PLoS One paper is 2022, '
            'not 2021. '
            'TWO NEW CAVEATS surfaced by reading the resolved sources rather than the strings. '
            '(1) COI: all four first-listed authors of 40697602 are MSD China employees and a '
            'fifth is Merck Sharp and Dohme LLC - a manufacturer-affiliated meta-analysis of that '
            'manufacturer''s drug class. Declared, not disqualifying, but it belongs next to the '
            'result. (2) HETEROGENEITY: I2 = 74-82% is substantial, which is why GRADE certainty '
            'is only moderate. '
            'The promotion blocker is unchanged and is the real point: HOMA-beta is a surrogate '
            'for possibly REVERSIBLE functional recovery, not durable beta-cell MASS preservation, '
            'and the only mass-level evidence (32712220, 35180212) is MURINE. No off-drug or '
            'mass-endpoint human trial exists. Next revalidate ~2026-11-08.'
        ),
        'external_pmids': ['35563495', '32712220', '35180212', '40697602'],
    },

    'GLP1_RA -> neuroprotection': {
        'status': 'PARTIALLY_VALIDATED',   # was VALIDATED
        'confidence': 'LOW',               # was HIGH
        'date': TODAY,
        'key_sources': [
            'PMID 41326666 - Liraglutide in mild to moderate Alzheimer\'s disease: a phase 2b '
            'clinical trial (ELAD, NCT01843075). Nat Med 2026 Jan;32(1):353-361. '
            'NEGATIVE ON ITS PRIMARY ENDPOINT: change in cerebral glucose metabolic rate, '
            'difference -0.17 (95% CI -0.39 to 0.06), P = 0.14. ADCS-ADL P = 0.65 and CDR-SoB '
            'P = 0.81 both null. ADAS-Exec 0.15 (95% CI 0.03-0.28) on UNADJUSTED P = 0.01. '
            'n=204, participants had NO DIABETES. Resolves the former bare string '
            '"Nature Medicine 2025".',
            'PMID 40898408 - Real-world observations of GLP-1 receptor agonists and SGLT-2 '
            'inhibitors as potential treatments for Alzheimer\'s disease. Alzheimers Dement '
            '2025 Sep;21(9):e70639. OBSERVATIONAL pharmacoepidemiology, covariate-adjusted Cox. '
            'Resolves the former bare string "Alzheimer\'s & Dementia 2025 (Zhang et al)".',
            'PMID 41356006 - GLP-1 receptor agonists in Alzheimer\'s and Parkinson\'s disease: '
            'endocrine pathways, clinical evidence, and future directions. Front Endocrinol 2025. '
            'REVIEW. Resolves the former bare string "Frontiers in Endocrinology 2025".',
            'PMC12536097 2025 - GLP-1 RAs against AD: propensity-matched cohort. PMCID only; '
            'OBSERVATIONAL.',
        ],
        'notes': (
            'DOWNGRADED 2026-08-20: VALIDATED/HIGH -> PARTIALLY_VALIDATED/LOW. This path was the '
            'single worst case found by the bare-string audit - rated HIGH confidence on zero '
            'resolvable PMIDs, and when the strings were resolved the flagship citation turned out '
            'to be a NEGATIVE TRIAL. '
            'ELAD (PMID 41326666) missed its primary endpoint (P = 0.14) and was null on both '
            'functional/global secondaries (ADCS-ADL P = 0.65, CDR-SoB P = 0.81). The one positive, '
            'ADAS-Exec, rests on an unadjusted P = 0.01 across a multi-endpoint battery. The widely '
            'circulated "18% slower cognitive decline / ~50% less brain atrophy" figures are '
            'EXPLORATORY outputs reported in press coverage, not in the trial''s stated endpoint '
            'hierarchy - they must not be cited as trial results. '
            'The stored note previously read "2025 phase 2b liraglutide AD trial + large '
            'propensity-matched cohorts show 40-70% lower dementia incidence", which fuses a '
            'negative RCT and positive observational cohorts into one apparent body of converging '
            'evidence. The 40-70% figure comes ONLY from the cohorts. Corrected. '
            'RELEVANCE CAVEAT, separate from the statistics: ELAD enrolled participants with NO '
            'DIABETES. Its bearing on a diabetes corpus is indirect at best. '
            'What remains: one negative RCT, two observational datasets subject to confounding by '
            'indication, and one narrative review. That supports "biologically plausible, '
            'clinically unproven" - which is PARTIALLY_VALIDATED / LOW, not VALIDATED / HIGH. '
            'DECIDING EVIDENCE PENDING: EVOKE / EVOKE+ (semaglutide, phase 3, AD). Those readouts '
            'are what would move this path, not another cohort study.'
        ),
        'external_pmids': ['41326666', '40898408', '41356006'],
    },
}


def main():
    backup = STATE + '.bak_' + TODAY
    if not os.path.exists(backup):
        shutil.copy2(STATE, backup)

    with open(STATE, encoding='utf-8') as f:
        state = json.load(f)

    changed = []
    for key, new in RESOLVED.items():
        for store in ('paths', 'validated_paths'):
            rec = state.get(store, {}).get(key)
            if not isinstance(rec, dict):
                continue
            before = (rec.get('status'), rec.get('confidence'))
            rec.update(new)
            after = (rec.get('status'), rec.get('confidence'))
            if before != after:
                changed.append(f'{store}:{key} {before[0]}/{before[1]} -> {after[0]}/{after[1]}')
            else:
                changed.append(f'{store}:{key} sources resolved (rating unchanged {after[0]}/{after[1]})')

    state.setdefault('audit_notes', []).append({
        'date': TODAY,
        'type': 'bare_source_resolution',
        'summary': (
            'Resolved all 9 bare journal-name key_sources across 3 paths to verified PMIDs via '
            'NCBI E-utilities. GLP1_RA -> neuroprotection DOWNGRADED VALIDATED/HIGH -> '
            'PARTIALLY_VALIDATED/LOW: its flagship source, ELAD (PMID 41326666), missed its '
            'primary endpoint (P=0.14) in a non-diabetic population. colchicine -> inflammation '
            'confidence cut HIGH -> MEDIUM (lead source not PubMed-indexed, dropped) but gained a '
            'diabetes-specific hard-endpoint meta-analysis (PMID 41889274, MACE HR 0.79). '
            'SGLT2i -> beta_cell rating unchanged; its 2026-08-08 "PMID=PENDING" placeholder is '
            'now indexed as PMID 40697602, and a stored year was wrong (PLoS One 2022, not 2021).'
        ),
        'paths_touched': sorted(RESOLVED),
    })

    state['last_updated'] = TODAY + 'T00:00:00'
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print('Bare-source resolution applied:')
    for c in changed:
        print('  -', c)
    print(f'\nBackup: {backup}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
