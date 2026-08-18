#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""State updates for the 2026-08-18 iteration run. One-shot; safe to re-run."""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_state as A

TODAY = '2026-08-18'
state = A.load_state()

# ---------------------------------------------------------------- paper vetting
VETTING = {
    '42598998': {
        'status': 'VETTED',
        'journal': 'Endocr Connect 2026',
        'design': 'Retrospective observational cohort, single academic network (NE Ohio), 2021-2023',
        'relevance': 'HIGH - LADA/GAD-65 diagnostics (Gaps #1, #10)',
        'issues_found': [
            'OVER-PRECISION RISK: reports P<0.0001 for a change in non-insulin '
            'antihyperglycemic classes while the MEDIAN IS UNCHANGED (1 [0-2] before '
            'vs 1 [0-1.5] after). The significance reflects a distribution shift, not '
            'a change in the reported central estimate. Do not quote this as "GAD-65 '
            'testing reduced therapy classes" without that qualifier.',
            'Single integrated delivery network, retrospective EMR - no causal claim '
            'available; treatment change may reflect clinician awareness rather than '
            'the antibody result.',
            'Cohort n not stated in the abstract; 73.3% white, median BMI 26.2 - '
            'limited generalisability.',
        ],
        'usable_for': 'Descriptive evidence that GAD-65 positivity in T2D is followed by '
                      'deprescribing of non-insulin agents. NOT evidence of benefit.',
    },
    '42577431': {
        'status': 'VETTED',
        'journal': 'Front Immunol 2026',
        'design': 'Multicenter retrospective, 5 Chinese tertiary hospitals, n=752 LADA inpatients, 2019-2025',
        'relevance': 'MEDIUM - LADA inpatient cohort; largest LADA n in corpus',
        'issues_found': [
            'Derivation vs external validation hypoglycemia incidence differs markedly '
            '(44.8% vs 54.4%). Case mix is not exchangeable across the two cohorts; '
            'treat external validation performance as optimistic.',
            'Tertiary-hospital inpatients only - incidence figures must NOT be read as '
            'LADA population rates (relevant to Gap #10, LADA prevalence by setting).',
            'Retrospective; predictors are routine clinical data, so confounding by '
            'indication for insulin is unaddressed.',
        ],
        'usable_for': 'LADA cohort characteristics and inpatient glycemic lability. '
                      'NOT usable for prevalence or natural-history claims.',
    },
    '42601001': {
        'status': 'VETTED',
        'journal': 'Eur J Pharmacol 2026',
        'design': 'PRECLINICAL - streptozotocin diabetic RATS (dapagliflozin, 12 wk) plus '
                  'human lens epithelial transcriptomics',
        'relevance': 'LOW-MEDIUM - downgraded from MEDIUM on vetting',
        'issues_found': [
            'PRECLINICAL, RODENT. Recorded at intake as "SGLT2i mechanism" without that '
            'qualifier. Must not be allowed to strengthen any clinical SGLT2i path.',
            'Endpoint is LENS OPACITY / diabetic cataract - not a hub gap. The hub '
            'tracks SGLT2i in nephropathy, inflammation and cardiovascular outcomes; '
            'this is a different organ and a different mechanism (AGE-RAGE-IGFBP2-FBN1).',
            'STZ rat model is chemically induced beta-cell ablation - a poor model for '
            'the T2D population in which SGLT2i is actually used.',
        ],
        'usable_for': 'Mechanistic hypothesis generation only. Tag PRECLINICAL on any use.',
        'relevance_downgraded_from': 'MEDIUM - SGLT2i mechanism',
    },
    '42574278': {
        'status': 'FLAGGED',
        'journal': 'Brief Bioinform 2026',
        'design': 'Computational framework paper; case study = MIGRAINE',
        'relevance': 'OFF-TOPIC for the diabetes corpus',
        'issues_found': [
            'CONTAINS NO DIABETES DATA. The sole case study is MIGRAINE (733 UK Biobank '
            'participants, 53 cases / 680 controls). Admitted at intake as "repurposing '
            'arm methodology" - that is a methods citation, not corpus evidence.',
            '53 cases is a very small positive class; ROC-AUC 0.775 / PR-AUC 0.475 on '
            'internal held-out data within the same analytical framework is weak and '
            'not externally validated.',
            'Same intake class as the 13 off-topic FLAGGED papers: admitted on topic '
            'adjacency (the word "repurposing") rather than diabetes content.',
        ],
        'usable_for': 'May be cited as METHODOLOGY in the repurposing arm. Must be '
                      'excluded from corpus evidence counts and from any path.',
        'disposition': 'Keep as methodology reference; exclude from corpus evidence.',
    },
}

for pmid, v in VETTING.items():
    rec = state['papers'].setdefault(pmid, {})
    rec.update(v)
    rec['pmid_verified'] = True
    rec['pmid_verified_via'] = 'NCBI esummary + efetch abstract round-trip 2026-08-18'
    rec['claims_checked'] = True
    rec['vetted_date'] = TODAY
    rec['last_checked'] = TODAY

# ------------------------------------------------- PMID 39412512 corpus finding
p = state['papers'].setdefault('39412512', {})
p.update({
    'status': 'VETTED',
    'title': 'SGLT2 inhibitors and NLRP3 inflammasome: potential target in diabetic kidney disease',
    'journal': 'J Bras Nefrol 2024',
    'design': 'NARRATIVE REVIEW (PublicationType: Review)',
    'pmid_verified': True,
    'pmid_verified_via': 'NCBI esummary 2026-08-18',
    'claims_checked': True,
    'vetted_date': TODAY,
    'last_checked': TODAY,
    'issues_found': [
        'INDEXING GAP CLOSED: was absent from paper_library/index.json despite having '
        'both abstract and full text on disk, so the citation audit gate could not see '
        'it. Folded in 2026-08-18 by reconcile_paper_index.py.',
        'QUEUE ITEM CLAIM WAS WRONG: the 2026-08-17 work item stated this paper '
        '"supplies 61 data points to NLRP3_inflammasome -> inflammation". It supplies 9. '
        'The path total of 61 is shared with PMID 31036962 (Nat Rev Immunol 2019), which '
        'supplies the remainder. Over-attribution of roughly 6x.',
        'EXTRACTION QUALITY: of 11 extractions, 2 are the SAME dose sentence counted '
        'twice - once from the English abstract and once from the Portuguese ("10 mg or" '
        'and "10 mg ou"). J Bras Nefrol publishes bilingually; the extractor double-counts '
        'every bilingual paper.',
        'EXTRACTION QUALITY: several inflammatory_marker "data points" are TABLE-ROW '
        'FRAGMENTS restating other authors\' mouse experiments, e.g. "NLRP3 activation in '
        'diabetic mice\\tDapagliflozinMixed in diet (1" with extracted value "1" - the '
        'stray digit from a truncated dose string, not a measurement.',
        'It is a REVIEW, so its data points are not independent observations; they are '
        'restatements of primary studies the corpus does not hold.',
    ],
    'sole_source_for': ['NLRP3_inflammasome -> nephropathy'],
})

# ----------------------------------------- path correction: NLRP3 -> nephropathy
np_key = 'NLRP3_inflammasome -> nephropathy'
if np_key in state['paths']:
    state['paths'][np_key].update({
        'status': 'PARTIALLY_VALIDATED',
        'validated_date': TODAY,
        'corpus_evidence_quality': 'WEAK',
        'corpus_evidence_note': (
            'All 3 corpus data points come from a single NARRATIVE REVIEW (PMID 39412512, '
            'J Bras Nefrol 2024) and are table-row fragments restating rodent experiments. '
            'The corpus contributes essentially no independent evidence to this path. The '
            'PARTIALLY_VALIDATED rating is carried by EXTERNAL evidence, not by the corpus.'
        ),
    })
state['validated_paths'][np_key] = {
    **state['validated_paths'].get(np_key, {}),
    'status': 'PARTIALLY_VALIDATED',
    'rating': 'PARTIALLY_VALIDATED',
    'date': TODAY,
    'confidence': 'MEDIUM for mechanism; LOW for clinical outcome',
    'external_pmids': ['32358544', '34918381'],
    'external_evidence': (
        'PMID 32358544 (Kim et al., Nat Commun 2020) is a randomized human trial: '
        'empagliflozin vs sulfonylurea in T2D at high cardiovascular risk produced greater '
        'IL-1beta secretion reduction from circulating macrophages, with raised serum '
        'beta-hydroxybutyrate and lowered insulin; ex vivo macrophage work supported the '
        'mechanism. PMID 34918381 (FASEB J 2022) shows SGLT2i counteracting NLRP3 via the '
        'tubular metabolite itaconate - rodent fibrosis model.'
    ),
    'what_is_validated': 'SGLT2 inhibition suppresses NLRP3 inflammasome activity in humans, '
                         'measured as IL-1beta secretion.',
    'what_is_NOT_validated': (
        'That NLRP3 suppression is the mechanism by which SGLT2i protects the kidney. Human '
        'evidence stops at inflammatory surrogates; no trial links NLRP3 suppression to '
        'renal hard endpoints (eGFR decline, ESKD, doubling of creatinine). The renal '
        'endpoint data come from separate outcome trials that did not measure NLRP3.'
    ),
    'validated_by': 'external web search + NCBI verification, 2026-08-18',
    'corpus_contribution': 'NEGLIGIBLE - see PMID 39412512 vetting notes.',
}

# ------------------------------------------------------------ sweep query change
state.setdefault('sweep_queries', {})
state['sweep_queries'] = {
    'authoritative_source': 'Analysis/Scripts/agent_state.py :: SWEEP_QUERIES',
    'updated': TODAY,
    'retired': {
        'oxidative stress diabetes combination': {
            'retired_on': TODAY,
            'reason': ('8/8 off-topic hits on 2026-08-17 (hydrogels, cryogels, donkey-blood '
                       'peptide, Carica papaya, bariatric surgery review). Bare keyword AND '
                       'with no field qualifiers; "combination" matched materials-science '
                       'papers mentioning diabetic wound healing. Traced as the intake path '
                       'for the 13 off-topic FLAGGED papers.'),
            'replacement_key': 'oxidative_stress_combination',
        }
    },
    'active_count': len(A.SWEEP_QUERIES),
}

# --------------------------------------------------------------- orphan finding
state.setdefault('audit_notes', []).append({
    'date': TODAY,
    'note': (
        'CITATION GATE BLIND SPOT, root-caused and closed. verify_pmids.py scans only .py '
        'source literals, so papers entering via extraction output or a PubMed sweep never '
        'reached paper_library/index.json and were invisible to validate_citations.py and '
        'check_citation_mismatches.py. 39 such orphans existed (13% of the 298 fetched '
        'abstracts). New script reconcile_paper_index.py folds them in, screened: 11 '
        'UNSCREENED_ORPHAN (topic vocabulary present), 6 OFF_TOPIC (already FLAGGED in a '
        'prior run), 22 OFF_TOPIC_PRESUMED (no diabetes vocabulary anywhere). Orphans are '
        'indexed for auditability but EXCLUDED from the headline corpus count until '
        'reviewed: metadata.total_pmids stays 260, metadata.total_indexed becomes 299.'
    ),
    'caveat': (
        'The topic screen is keyword-based and produced at least 2 known false negatives: '
        'PMID 39869107 (belatacept vs tacrolimus, UNOS transplant outcomes - relevant to '
        'Gap #3/#11) and PMID 40291594 (CAR-T manufacturing cost - relevant to Gap #6) were '
        'marked OFF_TOPIC_PRESUMED because neither title nor MeSH carries diabetes '
        'vocabulary. Human review of the 22 must not treat the screen as a verdict.'
    ),
})

state['audit_notes'].append({
    'date': TODAY,
    'note': (
        'PATH STORE DIVERGENCE, root-caused. The 2026-08-17 "reconciliation to 75/75" did '
        'not merge the stores - it MIRRORED entries between state.paths and '
        'state.validated_paths under each other\'s key spelling. The counts matched (75=75) '
        'while the content kept diverging, and 8 edges existed TWICE per store under two '
        'spellings (e.g. "dapagliflozin -> T2D" and "dapagliflozin_T2D"). True unique edge '
        'count was 68, not 75 - the path total was inflated ~10%. Both stores deduped to 67 '
        'on 2026-08-18; canonical store (68, includes one vrp-only key) written to '
        'canonical_paths.json by the new Analysis/Scripts/path_store.py, which owns the '
        'merge rule: recency wins, conservative (weaker claim) tie-break, keys normalised. '
        'agent_state.generate_path_work_items() now reads it, so the 2026-08-16 false '
        '"NEVER-VALIDATED" class cannot recur. validated_research_paths.json '
        'paths_validated regenerated 27 -> 64.'
    ),
})

# ------------------------------------------------------------------- work queue
done_markers = [
    'Make the work-queue generator read the RECONCILED path store',
    'Backfill PMID 39412512',
    'REPLACE the weekly sweep query',
    'Wire Analysis/Scripts/git_commit_safe.py',
    'Vet the 4 papers ingested 2026-08-17',
]
queue = [i for i in state['work_queue']
         if not any(m in str(i.get('target', '')) for m in done_markers)]

queue.extend([
    {
        'priority': 2, 'type': 'vet_papers_batch', 'added': TODAY,
        'target': ('Review the 22 OFF_TOPIC_PRESUMED orphans from reconcile_paper_index.py '
                   'and decide purge vs retain. START with the 2 known screen false '
                   'negatives: 39869107 (belatacept/tacrolimus UNOS - Gap #3/#11) and '
                   '40291594 (CAR-T manufacturing cost - Gap #6). Then confirm the other 20 '
                   'are genuinely off-topic before purging.'),
    },
    {
        'priority': 2, 'type': 'vet_papers_batch', 'added': TODAY,
        'target': ('Screen the 11 UNSCREENED_ORPHAN papers into the corpus properly: '
                   '30291106, 39173844, 39412512, 39428507, 39613428, 40598585, 40988828, '
                   '41618067, 41935855, 41986815, 41994768. Several look genuinely relevant '
                   '(39613428 verapamil beta-cell BMJ Open; 41935855 LADA carotid '
                   'atherosclerosis; 40598585 network MA of beta-cell preservation). '
                   'Promote to IN_CORPUS on review and set metadata.total_pmids accordingly.'),
    },
    {
        'priority': 1, 'type': 'fix_pipeline', 'added': TODAY,
        'target': ('EXTRACTOR DOUBLE-COUNTS BILINGUAL PAPERS. PMID 39412512 (J Bras Nefrol, '
                   'English + Portuguese abstract) had the same dose sentence extracted '
                   'twice ("10 mg or" / "10 mg ou"). Every bilingual paper in the corpus '
                   'inflates its own data_point_count. Add a language/duplicate filter to '
                   'extract_corpus_data.py and RE-COUNT all path data_point_count values '
                   'afterwards - the dashboard figures depend on them.'),
    },
    {
        'priority': 1, 'type': 'fix_pipeline', 'added': TODAY,
        'target': ('EXTRACTOR SCRAPES TABLE FRAGMENTS AS DATA POINTS. Example from 39412512: '
                   'matched_text "NLRP3 activation in diabetic mice\\tDapagliflozinMixed in '
                   'diet (1" yields value "1" - a truncated dose string, not a measurement. '
                   'Tab characters indicate a table row. Reject extractions containing tabs '
                   'or whose numeric value is adjacent to an unclosed parenthesis, then '
                   're-run and diff the path counts.'),
    },
    {
        'priority': 2, 'type': 'audit_gap', 'added': TODAY,
        'target': ('Re-audit every path whose corpus evidence is a REVIEW ARTICLE only. '
                   'NLRP3_inflammasome -> nephropathy was found on 2026-08-18 to rest '
                   'entirely on table fragments from one narrative review. Enumerate paths '
                   'whose corpus_pmids are all PublicationType=Review and mark their '
                   'corpus_evidence_quality WEAK.'),
    },
    {
        'priority': 3, 'type': 'validate_path', 'added': TODAY,
        'target': ('Re-check the 11 path divergences path_store resolved on 2026-08-18 '
                   'against external evidence, in data-point order: dapagliflozin -> '
                   'inflammation, verapamil -> T1D, hydroxychloroquine -> inflammation, '
                   'rapamycin -> islet_transplant, oxidative_stress -> T1D, pioglitazone -> '
                   'inflammation, metformin -> nephropathy, semaglutide -> retinopathy, '
                   'alpha_lipoic_acid -> diabetic_neuropathy. The merge rule picked a '
                   'winner by date; that is a tie-breaker, not evidence.'),
    },
])
state['work_queue'] = queue

# --------------------------------------------------------------------- run log
state.setdefault('run_history', []).append({
    'date': TODAY,
    'day': 'Tuesday',
    'papers_checked': 5,
    'paths_validated': 1,
    'issues_found': 6,
    'changes_pushed': False,
    'summary': (
        'Tue 2026-08-18 - THREE SYSTEMIC DEFECTS FOUND, all previously invisible because the '
        'checks that should have caught them were themselves incomplete. (1) PATH STORE: the '
        '2026-08-17 "reconciliation to 75/75" was itself the bug - it mirrored entries between '
        'stores rather than merging, so counts matched while content diverged and 8 edges were '
        'double-counted. True path count 68, not 75. New path_store.py owns the merge rule; '
        'both stores deduped 75 -> 67; work-queue generator rewired; 2026-08-16 false-positive '
        'class regression-tested closed. (2) CITATION GATE BLIND SPOT: verify_pmids.py scans '
        'only .py literals, so 39 papers with abstracts already on disk (13% of the corpus) '
        'were never indexed and could not be audited - including PMID 39412512, sole source '
        'for NLRP3_inflammasome -> nephropathy. New reconcile_paper_index.py folds them in '
        'with a topic screen; orphans held OUT of the headline corpus count pending review. '
        '(3) EXTRACTOR DEFECTS: 39412512 double-counts its bilingual abstract and yields '
        'table-row fragments as data points; the queue item asserting it supplied 61 data '
        'points over-attributed by 6x (actual: 9). Path NLRP3_inflammasome -> nephropathy '
        'confirmed PARTIALLY_VALIDATED on EXTERNAL evidence (PMID 32358544, Kim et al. Nat '
        'Commun 2020 randomized human trial, IL-1beta surrogate) with corpus contribution '
        'marked NEGLIGIBLE. Papers vetted: 42598998 and 42577431 VETTED with caveats, '
        '42601001 VETTED but downgraded to preclinical-rodent lens-opacity, 42574278 FLAGGED '
        'OFF-TOPIC (its only case study is MIGRAINE, no diabetes data). Retired the '
        '"oxidative stress diabetes combination" sweep query; SWEEP_QUERIES now field-qualified '
        'and version-controlled in agent_state.py. git_commit_safe.py wired into '
        'run_quality_improvements.py --commit (green builds only).'
    ),
})
state['last_run'] = TODAY
state['last_updated'] = datetime.now().isoformat()

A.save_state(state)
print(f'[OK] state saved: {len(state["papers"])} papers, {len(state["paths"])} paths, '
      f'{len(state["work_queue"])} queue items, {len(state["run_history"])} runs')
