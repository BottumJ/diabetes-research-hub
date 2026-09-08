"""Daily iteration run - Monday 2026-09-07.

Work performed this run (all verified against live NCBI eutils / ClinicalTrials.gov API v2):
  1. Vetted the 5 UNVETTED papers carried in from 2026-09-06 (esummary round-trip).
  2. Resolved all four identifiers parked UNVERIFIED on 2026-09-03 (P2 queue item).
  3. Monday sweep: 6 topic queries, 12 hits, 5 ingested / 7 screened out.
  4. FIRST-EVER audit of canonical Gap #11 (Islet Transplant Registry Equity)
     under its own question.

Writes agent_state.json. Idempotent: safe to re-run.
"""
import json
import os
import shutil
from datetime import datetime

RESULTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Results')
STATE = os.path.join(RESULTS, 'agent_state.json')
TODAY = '2026-09-07'

with open(STATE, encoding='utf-8') as fh:
    state = json.load(fh)

shutil.copyfile(STATE, os.path.join(RESULTS, 'agent_state.json.bak_%s' % TODAY))

papers = state['papers']

# ---------------------------------------------------------------- 1. VETTING
# Every PMID below was round-tripped through
# eutils esummary.fcgi?db=pubmed on 2026-09-07; title, journal and year
# returned by PubMed matched the note recorded at intake on 2026-09-06.
VETTED_TODAY = {
    '42698953': {
        'title': ('Acid-Responsive Zeolitic Imidazolate Framework-8 Core-Shell Nanovesicles '
                  'Loaded with Interleukin-2 Nanoplatforms Selectively Expand Regulatory T Cells '
                  'to Reconstruct Immunometabolic Homeostasis in Diabetic Neuropathy.'),
        'journal': 'Biomaterials research',
        'year': '2026',
        'design': 'PRECLINICAL (murine DPN model)',
        'notes': ('PMID verified live 2026-09-07. Biomater Res 2026;30:0407, epub Sep 4 2026, '
                  'PMC13542432, doi 10.34133/bmr.0407. Pubtype "Journal Article" - no trial tag. '
                  'CAVEAT ON USE: this is a nanoparticle drug-delivery study in mice. It falsifies '
                  'the absence claim "Treg-based therapy has never been tested for diabetic '
                  'neuropathy" ONLY at the preclinical level. It is NOT evidence of human efficacy '
                  'and must never be cited as such.'),
    },
    '39084449': {
        'title': ('Alleviated diabetic osteoporosis and peripheral neuropathic pain by Rehmannia '
                  'glutinosa Libosch polysaccharide via increasing regulatory T cells.'),
        'journal': 'International journal of biological macromolecules',
        'year': '2024',
        'design': 'PRECLINICAL (animal model)',
        'notes': ('PMID verified live 2026-09-07. Int J Biol Macromol 2024;277(Pt 4):134241, '
                  'doi 10.1016/j.ijbiomac.2024.134241. Second preclinical counterexample to the '
                  'same absence claim. Botanical polysaccharide, Treg increase is an observed '
                  'correlate, not a demonstrated mechanism of the analgesic effect.'),
    },
    '37399599': {
        'title': ('A genetically supported drug repurposing pipeline for diabetes treatment using '
                  'electronic health records.'),
        'journal': 'EBioMedicine',
        'year': '2023',
        'design': 'Genetic instrument + EHR observational (Mendelian-randomisation flavour)',
        'notes': ('PMID verified live 2026-09-07. EBioMedicine 2023;94:104674, PMC10328805. '
                  'Weakens - does not refute - "generic drugs have never been systematically '
                  'evaluated for repurposing in diabetes": the pipeline is genetically-targeted '
                  'and EHR-based, not a systematic evaluation of the generic formulary. '
                  'Scope of its claim must be stated whenever it is cited.'),
    },
    '42373533': {
        'title': ('Impact of Autoimmune Hypothyroidism and Celiac Disease on Progression to '
                  'Diabetes in Individuals Positive for GAD65 or IA-2 Autoantibodies.'),
        'journal': 'Diabetes, obesity & metabolism',
        'year': '2026',
        'design': 'Observational cohort',
        'notes': ('PMID verified live 2026-09-07. Diabetes Obes Metab 2026;28(9):8452-8459, '
                  'PMC13449009, doi 10.1111/dom.71044. Relevant to canonical Gap #8 '
                  '(Immunomodulatory Drugs for LADA) as background on progression risk in '
                  'autoantibody-positive adults. Observational - no intervention.'),
    },
    '42014686': {
        'title': ('A pharmacokinetic and pharmacodynamic drug-drug interaction study of '
                  'dorzagliatin and empagliflozin in patients with type 2 diabetes and obesity: '
                  'an open-label phase I trial.'),
        'journal': 'Nature communications',
        'year': '2026',
        'design': 'Phase I open-label DDI trial (pubtype "Clinical Trial, Phase I")',
        'notes': ('PMID verified live 2026-09-07. Nat Commun 2026;17(1), PMC13287472. '
                  'Phase I PK/PD in T2D+obesity. CAVEAT: a DDI study is powered for exposure, '
                  'not for glycaemic outcome; it is evidence that the combination is '
                  'pharmacokinetically characterised, NOT that it works. Links canonical Gap #15 '
                  '(GKA Pricing) and Gap #7 (GKA Repurposing) to the same molecule as '
                  'NCT06976658 - see the dorzagliatin note added to doctrine today.'),
    },
}

for pmid, meta in VETTED_TODAY.items():
    rec = papers.setdefault(pmid, {})
    rec['status'] = 'VETTED'
    rec['pmid_verified'] = True
    rec['claims_checked'] = True
    rec['vetted_date'] = TODAY
    rec['last_checked'] = TODAY
    rec['claims_checked_method'] = (
        'eutils_esummary_live_roundtrip_2026-09-07 '
        '(title + journal + year returned by PubMed matched the intake note verbatim)')
    rec['title'] = meta['title']
    rec['journal'] = meta['journal']
    rec['year'] = meta['year']
    rec['design'] = meta['design']
    rec['vetting_notes'] = meta['notes']
    rec.setdefault('issues_found', [])

# ------------------------------------------- 2. RESOLVE THE FOUR IDENTIFIERS
# P2 queue item added 2026-09-03. All four were parked because NCBI and
# ClinicalTrials.gov were unreachable on that run. Both were reachable today.
RESOLUTIONS = {
    'NCT06976658': {
        'status': 'VERIFIED_REGISTRY_READ_2026-09-07',
        'source': 'ClinicalTrials.gov API v2, /studies/NCT06976658, fetched 2026-09-07',
        'verified_fields': {
            'briefTitle': 'Glucokinase Activator in Monogenic Diabetes',
            'overallStatus': 'RECRUITING',
            'studyType': 'INTERVENTIONAL',
            'phase': 'PHASE2',
            'enrollment': 44,
            'leadSponsor': 'Chinese University of Hong Kong',
            'conditions': ['Diabetes Mellitus', 'Monogenic Diabetes'],
            'interventions': ['Dorzagliatin', 'matched placebo'],
            'startDate': '2025-04-30',
            'primaryCompletionDate': '2026-12-31',
        },
        'correction': (
            'The 2026-09-03 label called this "allosteric glucokinase activator in monogenic '
            'diabetes FROM INACTIVATING GCK MUTATIONS". The registry brief title and condition '
            'fields say "Monogenic Diabetes" only. The GCK-inactivating-mutation restriction is '
            'NOT confirmed by the fields read today and must not be asserted until the detailed '
            'eligibility module is read. The drug is dorzagliatin - a named, already-approved '
            '(China) GKA - not an unnamed novel agent.'),
        'citable': ('YES for canonical Gap #7, as a registered, recruiting Phase 2 trial. '
                    'NOT citable for any efficacy claim: primary completion is 2026-12-31 and '
                    'no results are posted.'),
    },
    'Diabetes 2025;74(8):1339': {
        'status': 'RESOLVED_TO_PMID_2026-09-07',
        'pmid': '40690616',
        'source': 'eutils esearch db=pubmed, exact title match, 1 hit, fetched 2026-09-07',
        'verified_fields': {
            'title': 'Glucokinase Activators. A Humbling Lesson in Drug Development.',
            'authors': ['Agius L', 'Magnuson MA'],
            'journal': 'Diabetes',
            'citation': '2025;74(8):1339-1341',
            'doi': '10.2337/dbi25-0028',
            'pubtype': ['Editorial', 'Comment'],
            'comment_on_pmid': '40272935',
        },
        'correction': (
            'The 2026-09-03 note listed this as a "candidate authoritative source" for Gap #7. '
            'PubMed types it EDITORIAL + COMMENT. It is a two-page commentary, not primary '
            'evidence and not a systematic review. It may be cited for framing/opinion with the '
            'word "editorial" attached, never as evidence. NOTE: the article it comments on, '
            'PMID 40272935, is ALREADY IN THIS CORPUS and is vetted - the editorial is secondary '
            'to a source already held.'),
        'citable': 'YES as an editorial, explicitly labelled. NO as evidence.',
    },
    'PMC12211534': {
        'status': 'RESOLVED_TO_PMID_2026-09-07_ALREADY_IN_CORPUS',
        'pmid': '40598585',
        'source': ('eutils esearch db=pubmed PMC12211534[pmcid] -> 40598585; '
                   'efetch abstract read in full, 2026-09-07'),
        'verified_fields': {
            'title': ('A systematic review and network meta-analysis of interventions to preserve '
                      'insulin-secreting beta cell function in people newly diagnosed with type 1 '
                      'diabetes: results from randomised controlled trials of IMMUNOMODULATORY '
                      'THERAPIES.'),
            'journal': 'BMC Medicine 2025;23(1):351',
            'doi': '10.1186/s12916-025-04201-z',
            'pubtype': ['Journal Article', 'Systematic Review', 'Network Meta-Analysis'],
            'trials': 60, 'patients': 4597, 'intervention_classes': 32,
            'in_nma': '41 trials / 42 interventions',
            'search_cutoff': '2024-07-31',
            'prospero': 'CRD42018107904',
            'heterogeneity': 'I2 = 66% (substantial), authors call findings hypothesis-generating',
        },
        'correction': (
            'MATERIAL. The 2026-09-03 note filed this as supporting Gap #13 "as a NEGATIVE (no '
            'nutrition arm)". That inference is CIRCULAR and must not be published. The review\'s '
            'stated inclusion criterion is "RCTs of IMMUNOTHERAPIES to preserve beta cells" - a '
            'nutrition arm was excluded by design, so its absence from the network says nothing '
            'about whether nutrition has been trialled. Using it that way would manufacture an '
            'evidence gap out of another study\'s scope. Two further limits on any citation: the '
            'search stopped 2024-07-31, so it is silent on anything since; and the authors '
            'themselves flag I2=66% and label the rankings hypothesis-generating. '
            'SECOND FINDING: the paper was ALREADY IN THE CORPUS as PMID 40598585, VETTED. '
            'The 2026-09-03 run logged it as a novel external find because the intake path '
            'matched on PMCID and the corpus is keyed on PMID - a dedup blind spot.'),
        'citable': ('YES, as an already-held corpus paper, for what it actually reports: 11 of 42 '
                    'IMMUNOMODULATORY interventions beat placebo on 12-month C-peptide. '
                    'NO for any claim about nutrition, and NO for anything after 2024-07-31.'),
    },
    'NCT07360080': {
        'status': 'VERIFIED_REGISTRY_READ_2026-09-07',
        'source': 'ClinicalTrials.gov API v2, /studies/NCT07360080, fetched 2026-09-07',
        'verified_fields': {
            'briefTitle': 'Long-Term Outcomes of Teplizumab in Routine Clinical Care',
            'overallStatus': 'RECRUITING',
            'studyType': 'OBSERVATIONAL',
            'enrollment': 1000,
            'leadSponsor': 'Sanofi',
            'conditions': ['Type 1 Diabetes'],
            'interventions': ['Teplizumab'],
            'startDate': '2026-03-19',
            'primaryCompletionDate': '2035-10-29',
        },
        'correction': (
            'Real, but the watch priority was set wrong. Primary completion is 2035-10-29 - nine '
            'years out. It is an observational registry study, not the "PROTECT extension" it was '
            'filed under. It cannot inform any verdict this decade. Demote from active watch to '
            'a dated long-horizon note; stop re-surfacing it in the queue.'),
        'citable': ('YES as evidence that a 1,000-patient real-world teplizumab cohort is '
                    'enrolling. NO for outcomes, now or for years.'),
    },
}

state.setdefault('resolved_identifiers', {})[TODAY] = RESOLUTIONS

# The four are no longer pending. Keep the record, mark it closed.
for item in state.get('watch_items_pending_pmid', []):
    ident = item.get('identifier')
    if ident in RESOLUTIONS:
        item['status'] = RESOLUTIONS[ident]['status']
        item['resolved_date'] = TODAY
        item['resolution_ref'] = 'state["resolved_identifiers"]["%s"]["%s"]' % (TODAY, ident)

# ------------------------------------------------------- 3. MONDAY SWEEP
# 6 eutils queries run 2026-09-07 (entry-date windowed). 12 unique hits.
INGEST = {
    '42688599': {
        'priority': 'high',
        'title': ('Impact of preformed donor-specific anti-HLA antibodies on pancreatic islet '
                  'transplantation outcomes: do they matter as they do in solid organ '
                  'transplantation?'),
        'journal': 'Frontiers in immunology', 'year': '2026',
        'design': 'Review',
        'note': ('Front Immunol 2026;17:1909238, PMC13534801. Directly on islet transplant '
                 'outcomes and HLA sensitisation. Feeds the canonical Gap #11 audit performed '
                 'today - see gap_audits["11"]. Review, not primary data.'),
    },
    '42674789': {
        'priority': 'medium',
        'title': ('Retrospective population-based cohorts for assessing the performance of '
                  'algorithmic diabetes classification and for quantifying the true burden of '
                  'type 1, type 2 and LADA phenotypes in Quebec: a study protocol.'),
        'journal': 'BMJ Open', 'year': '2026',
        'design': 'STUDY PROTOCOL - NO RESULTS',
        'note': ('BMJ Open 2026;16(8):e109209, PMC13536008. Relevant to canonical Gap #10 (LADA '
                 'Prevalence by Healthcare Setting). FLAGGED PROTOCOL AT INTAKE: this corpus has '
                 'already been burned once by ranking research paths on a protocol '
                 '(PMID 39613428, Ver-A-T1D). This paper reports NO findings and must not '
                 'contribute evidence weight to any path or gap. Watch for the results paper.'),
    },
    '42694315': {
        'priority': 'low',
        'title': ('Metabolic-epigenetic crosstalk in latent autoimmune diabetes in adults: '
                  'potential roles of lactate-induced histone lactylation in immune regulation '
                  'and pancreatic beta-cell fate.'),
        'journal': 'Frontiers in endocrinology', 'year': '2026',
        'design': 'Narrative review (mechanistic hypothesis)',
        'note': ('Front Endocrinol 2026;17:1896333, PMC13539050. Note the hedge in its own title '
                 '("potential roles"). Hypothesis-generating only.'),
    },
    '42686659': {
        'priority': 'low',
        'title': 'The Ferroptosis-Immunity Axis in Diabetic Kidney Disease: Emerging Therapeutic Targets.',
        'journal': 'Antioxidants & redox signaling', 'year': '2026',
        'design': 'Review',
        'note': ('Antioxid Redox Signal, epub 2026-09-02, doi 10.1177/15230864261483982. '
                 'Same territory as the ferroptosis/NLRP3 DKD watch item already held. '
                 'Review, no primary data.'),
    },
    '42688475': {
        'priority': 'low',
        'title': ("Extracellular vesicles at the immune-metabolic crossroads of Hashimoto's "
                  "thyroiditis and diabetes mellitus."),
        'journal': 'Frontiers in immunology', 'year': '2026',
        'design': 'Review',
        'note': ('Front Immunol 2026;17:1914528, PMC13535534. Pairs thematically with PMID '
                 '42373533 vetted today (autoimmune hypothyroidism and progression in '
                 'autoantibody-positive adults). Review only.'),
    },
}

for pmid, meta in INGEST.items():
    if pmid in papers and papers[pmid].get('status') == 'VETTED':
        continue
    papers[pmid] = {
        'status': 'UNVETTED',
        'added': TODAY,
        'priority': meta['priority'],
        'source': '2026-09-07 Monday sweep (eutils esearch, entry-date windowed)',
        'title': meta['title'],
        'journal': meta['journal'],
        'year': meta['year'],
        'design': meta['design'],
        'note': meta['note'],
    }

# Candidates surfaced by the Gap #11 audit rather than the sweep.
GAP11_INGEST = {
    '37026004': {
        'priority': 'high',
        'title': ('Matching for HLA-DR excluding diabetogenic HLA-DR3 and HLA-DR4 predicts '
                  'insulin independence after pancreatic islet transplantation.'),
        'journal': 'Frontiers in immunology', 'year': '2023',
        'design': 'CITR registry analysis (Research Support, NIH Extramural)',
        'note': ('Front Immunol 2023;14:1110544, PMC10070978. Ballou/Barton/Payne/Muller, CITR '
                 'authorship. LOAD-BEARING for the Gap #11 hypothesis recorded today: it is the '
                 'link showing HLA-DR matching predicts islet transplant success. Must be read '
                 'in full before the hypothesis is published anywhere.'),
    },
    '39951130': {
        'priority': 'medium',
        'title': ('Islet Transplantation Versus Standard of Care for Type 1 Diabetes Complicated '
                  'by Severe Hypoglycemia From the Collaborative Islet Transplant Registry and '
                  'the T1D Exchange Registry.'),
        'journal': 'Diabetes Care', 'year': '2025',
        'design': 'Registry comparison (CITR vs T1D Exchange)',
        'note': ('Diabetes Care 2025;48(5):737-744, PMC12034893. The most recent substantive CITR '
                 'output found in the 2026-09-07 census of 31 CITR-indexed papers. Screened '
                 'today at title/abstract level only: reports no equity stratification in its '
                 'title or abstract. Ingested so the Gap #11 absence claim can be checked '
                 'against its full text rather than its abstract.'),
    },
}
for pmid, meta in GAP11_INGEST.items():
    if pmid in papers and papers[pmid].get('status') == 'VETTED':
        continue
    papers[pmid] = dict(meta, status='UNVETTED', added=TODAY,
                        source='2026-09-07 canonical Gap #11 audit')

state.setdefault('screened_out', {})[TODAY] = {
    'pmids': ['42609797', '42683551', '42689362', '42688438',
              '42682404', '42688959', '42687181'],
    'reason': (
        'Screened OUT at intake on 2026-09-07, deliberately NOT ingested. All seven are query '
        'artifacts rather than topic matches. 42609797 gout urate-lowering review (matched '
        '"colchicine", not about diabetes). 42683551 SGLT2i repurposed for pulmonary arterial '
        'hypertension (matched "repurposing", outcome is not diabetes). 42689362 telmisartan '
        'synthesis/pharmacology review (chemistry, not repurposing-in-diabetes). 42688438 orphan '
        'GPCRs in diabetes (de-novo drug development, not repurposing of generics). 42682404 '
        'metronidazole/gut anaerobes and transplant rejection (not islet). 42688959 PANoptosis '
        'review and 42687181 protein tyrosine phosphatase review (both narrative reviews adding '
        'no primary data to the NLRP3/DKD line already held). '
        'Recording these keeps the sweep auditable: 12 hits, 5 in, 7 out.'),
    'queries_run': [
        '(LADA OR "latent autoimmune diabetes") reldate=8 datetype=edat -> 3',
        'islet transplant* AND outcome* reldate=8 -> 2',
        'NLRP3 AND (diabetic kidney OR diabetic nephropathy) reldate=8 -> 2',
        '(drug repurposing OR repurposed) AND diabetes reldate=8 -> 4',
        'verapamil AND (type 1 diabetes OR beta cell) reldate=30 -> 0',
        '(colchicine AND diabetes) OR (dapagliflozin AND colchicine) reldate=30 -> 1',
    ],
}
state['last_sweep'] = TODAY

# ------------------------------------- 4. CANONICAL GAP #11 - FIRST AUDIT
GAP11 = {
    'gap_id': 11,
    'canonical_name': 'Islet Transplant Registry Equity Analysis',
    'audit_date': TODAY,
    'audit_number': 1,
    'note': ('This is the FIRST audit of canonical Gap #11 under its own question. The trail '
             'previously filed under "#11" in agent memory audits CAR-Treg x personalized '
             'nutrition, a different question (see the 2026-09-03 numbering item).'),

    'finding_1_current_evidence_does_not_support_the_claim': {
        'severity': 'HIGH',
        'detail': (
            'gap_evidence.json rates Gap #11 GOLD on exactly two papers: PMID 19104422 (2008 CITR '
            'Update) and PMID 37105208 (primary graft function vs 5-year outcomes, CITR, n=1210). '
            'Neither is an equity analysis. Both establish that the registry EXISTS and reports '
            'graft outcomes. Nothing in either paper bears on race, ethnicity, socioeconomic '
            'status or access. An absence claim cannot be evidenced by two papers that are not '
            'about the thing claimed absent - it needs a documented search that returns nothing. '
            'Until today no such search had been run.'),
    },

    'finding_2_the_gap_itself_survives_testing': {
        'verdict': 'VALID',
        'confidence': 'LIKELY (not certain - see scope limit below)',
        'searches_run_2026_09_07': [
            {'query': ('islet transplantation AND (disparities[tiab] OR equity[tiab] OR '
                       'inequity[tiab] OR racial[tiab] OR socioeconomic[tiab])'),
             'window': 'all time', 'hits': 23,
             'screened': ('10 highest-relevance records read at summary level; 0 are equity '
                          'analyses of islet transplantation. The set is dominated by other '
                          'fields: 35845323 racial disparities in LIVING DONOR KIDNEY '
                          'transplant; 36566139 kidney organ allocation fairness; 42548012 '
                          'xenotransplantation consensus; 41694652 global aortic aneurysm '
                          'mortality; 42626230 pancreatic nerve anatomy across species; '
                          '36328836 cardiorenal clinical complexity; 39229679 pediatric donor '
                          'pancreas-kidney utilisation; 42488823 ATMP bioengineering; '
                          '40668408 monogenic diabetes; 33444224 beta-cell function review.')},
            {'query': '"Collaborative Islet Transplant Registry"', 'window': 'all time', 'hits': 31,
             'screened': ('Full PMID list retrieved. No record is titled on equity, disparity, '
                          'race, ethnicity or access. The CITR output line is graft function, '
                          'C-peptide, HLA matching, hypoglycaemia and registry updates.')},
        ],
        'statement_that_is_supportable': (
            'As of 2026-09-07 there is no PubMed-indexed analysis of equity - racial, ethnic or '
            'socioeconomic - in access to or outcomes of islet transplantation, including in the '
            '31 PubMed-indexed papers drawing on the Collaborative Islet Transplant Registry.'),
        'statement_that_is_NOT_supportable': (
            'That no such analysis exists. CITR annual reports, NIDDK data-request outputs, '
            'conference abstracts and theses are grey literature and are not indexed the way '
            'these searches index. The claim must be scoped to "PubMed-indexed" every time it '
            'is published. This is why the confidence is LIKELY, not CERTAIN.'),
        'path_to_certain': (
            'Read the CITR Annual Report scientific summaries directly (citregistry.org) and '
            'search Embase + conference proceedings. Neither was reachable this run.'),
    },

    'finding_3_mechanistic_hypothesis': {
        'label': 'HYPOTHESIS - NOT A FINDING. Do not publish as a result.',
        'confidence': 'LIKELY as a hypothesis worth testing; UNTESTED as a claim about the world',
        'chain': [
            {'link': 'HLA-DR matching predicts insulin independence after islet transplantation',
             'evidence': 'PMID 37026004 (CITR analysis, Front Immunol 2023)',
             'status': 'INGESTED TODAY AS UNVETTED - full text not yet read'},
            {'link': 'Preformed donor-specific anti-HLA antibodies are being examined as a '
                     'determinant of islet transplant outcome',
             'evidence': 'PMID 42688599 (Front Immunol 2026, review)',
             'status': 'INGESTED TODAY AS UNVETTED - review, not primary data'},
            {'link': 'HLA-matching-based allocation is a documented source of racial disparity '
                     'in SOLID ORGAN (kidney) transplant',
             'evidence': 'PMID 35845323, PMID 36566139 - EXTERNAL comparators, different organ. '
                         'NOT ingested into this corpus.',
             'status': 'ANALOGY, NOT TRANSFER. Kidney allocation is a national list with formal '
                       'HLA points; islet allocation is not organised that way. The analogy may '
                       'fail for exactly that reason and that must be tested, not assumed.'},
        ],
        'implication_if_it_holds': (
            'Islet transplantation would have a mechanistically predicted equity problem that '
            'has never been measured - which is a sharper and more testable version of Gap #11 '
            'than the gap as currently written.'),
        'what_would_falsify_it': (
            'Any CITR stratification showing recipient race/ethnicity distribution matching the '
            'T1D population; or evidence that HLA-DR matching plays no role in islet allocation '
            'in practice.'),
        'next_step': ('Read 37026004 in full and check whether it reports recipient '
                      'race/ethnicity at all. That single fact decides whether this hypothesis '
                      'is testable from published data or needs a CITR data request.'),
    },

    'tier_recommendation': {
        'recommend': 'HOLD AT GOLD, but re-found the evidence.',
        'reasoning': (
            'The 2026-09-03 human-call item asked whether #11 publishing as SILVER while the '
            'store says GOLD meant the STORE was wrong, given it rests on 2 papers. Today '
            'answers that: the store is wrong about WHICH papers, not about the tier. The gap '
            'survives a documented all-time double search. Replace 19104422 and 37105208 as the '
            'evidentiary basis with the two null searches recorded above, and keep the two CITR '
            'papers only as context for what the registry does report.'),
        'not_applied': ('No tier value was written by this run. Changing a published tier is a '
                        'scientific judgement and the 2026-09-03 single-writer refactor has not '
                        'landed - writing a tier now would fork it further.'),
    },
}
state.setdefault('gap_audits', {}).setdefault('11', []).append(GAP11)

gaps = state.setdefault('gaps', {})
g11 = gaps.setdefault('11', {})
g11['last_audited'] = TODAY
g11['canonical_question_audited'] = True
g11['audit_ref'] = 'state["gap_audits"]["11"][-1]'

# --------------------------------------------------------- 5. DOCTRINE NOTES
state.setdefault('doctrine_notes', {})[TODAY] = {
    'scope_artifact_absence': (
        'AN ABSENCE INSIDE ANOTHER STUDY\'S INCLUSION CRITERIA IS NOT AN EVIDENCE GAP. '
        'Caught today in PMID 40598585: a network meta-analysis restricted by design to '
        'immunomodulatory RCTs was being read as evidence that nutrition has not been trialled. '
        'Before any "X was absent from Y" claim is published, read Y\'s inclusion criteria and '
        'confirm X was ELIGIBLE and MISSING rather than EXCLUDED. Candidate gate: flag any '
        'absence claim whose supporting citation is a systematic review, since SRs always have '
        'inclusion criteria that manufacture absences.'),
    'pmcid_pmid_dedup_blind_spot': (
        'The intake path can log a paper already in the corpus as a novel external find when the '
        'source gives a PMCID and the corpus is keyed on PMID. Happened with PMC12211534 = PMID '
        '40598585 (already VETTED). Fix: resolve every PMCID to a PMID at intake, before the '
        'novelty check.'),
    'absence_claims_need_a_search_not_a_citation': (
        'Gap #11 rated GOLD for months on two papers that were not about its question. The '
        'evidence for "nobody has studied X" is a dated, reproducible query string and its hit '
        'count - not a citation. Any gap whose evidence list contains only papers that do not '
        'mention the gap\'s own subject should fail a gate.'),
    'dorzagliatin_convergence': (
        'Three separately-tracked items are the same molecule: NCT06976658 (Phase 2, monogenic '
        'diabetes, CUHK), PMID 42014686 (Phase I DDI with empagliflozin), and the GKA paths '
        'under canonical Gaps #7 and #15. They should be reconciled before the GKA line is '
        'presented as several independent threads.'),
}

# ------------------------------------------------------------- 6. QUEUE WORK
CLOSED = [
    {'closed': TODAY, 'was_priority': 2, 'type': 'verify_citations',
     'summary': ('VERIFY THE FOUR IDENTIFIERS LOGGED UNVERIFIED ON 2026-09-03 - DONE. All four '
                 'read from live registries today. Two carried material corrections: '
                 'PMC12211534 was already in the corpus as PMID 40598585 and its "no nutrition '
                 'arm" reading is circular; the Diabetes 74(8):1339 item is PMID 40690616 and is '
                 'an EDITORIAL, not a source. NCT06976658 is dorzagliatin, Phase 2, n=44. '
                 'NCT07360080 is real but completes 2035 and was over-prioritised.')},
]
state.setdefault('closed_queue_items', []).extend(CLOSED)

queue = [q for q in state['work_queue']
         if not (q.get('type') == 'verify_citations' and q.get('added') == '2026-09-03')]

NEW_ITEMS = [
    {'priority': 1, 'type': 'fix_pipeline', 'added': TODAY,
     'target': (
         'GATE THE ABSENCE CLAIMS AGAINST THEIR OWN EVIDENCE. Today found canonical Gap #11 '
         'rated GOLD on two papers (19104422, 37105208) neither of which mentions equity, race, '
         'ethnicity or access - the gap\'s entire subject. audit_absence_claim_scope.py already '
         'exists; extend it to FAIL when a gap\'s evidence papers contain none of the gap\'s own '
         'subject terms in title or abstract. That single check would have caught #11 months ago '
         'and should be run across all 15 gaps immediately, because #11 is unlikely to be the '
         'only one.')},
    {'priority': 1, 'type': 'fix_pipeline', 'added': TODAY,
     'target': (
         'RESOLVE PMCID -> PMID AT INTAKE. PMC12211534 was logged 2026-09-03 as a novel external '
         'find and carried in the queue for four days; it was already in the corpus as VETTED '
         'PMID 40598585. The novelty check runs before the identifier is normalised. Add PMCID '
         'normalisation ahead of the dedup check and re-run it over watch_items_pending_pmid, '
         'which may hold more of these.')},
    {'priority': 2, 'type': 'vet_papers_batch', 'added': TODAY,
     'target': (
         'READ PMID 37026004 IN FULL AND ANSWER ONE QUESTION: does the CITR HLA-DR matching '
         'analysis report recipient race or ethnicity at all? That fact alone decides whether '
         'the Gap #11 equity hypothesis recorded today is testable from published data or '
         'requires a CITR data request. Also vet the other 6 papers ingested today '
         '(42688599, 42674789, 42694315, 42686659, 42688475, 39951130).')},
    {'priority': 3, 'type': 'audit_gap', 'added': TODAY,
     'target': (
         'RAISE GAP #11 FROM LIKELY TO CERTAIN, OR ACCEPT LIKELY PERMANENTLY. The absence claim '
         'is currently scoped to PubMed-indexed literature only. To close it: read the CITR '
         'Annual Report scientific summaries at citregistry.org and search Embase / conference '
         'proceedings. Neither was attempted this run. If those are not reachable from this '
         'agent, the honest move is to publish the claim permanently scoped as "no '
         'PubMed-indexed analysis" and stop queueing it.')},
]
queue.extend(NEW_ITEMS)
state['work_queue'] = queue

# ------------------------------------------------------------- 7. RUN RECORD
state['run_history'].append({
    'date': TODAY,
    'day': 'Mon',
    'queue_items_worked': [
        'verify_citations 2026-09-03 (four unverified identifiers) - CLOSED',
        'audit_gap canonical #11 - FIRST AUDIT UNDER ITS OWN QUESTION',
        'vet_papers_batch (5 carried from 2026-09-06) - all VETTED',
        'Monday sweep - 6 queries, 12 hits, 5 in / 7 out',
        'P0 publish blocker - re-measured, still blocking',
    ],
    'papers_vetted': list(VETTED_TODAY),
    'papers_added': list(INGEST) + list(GAP11_INGEST),
    'papers_screened_out': state['screened_out'][TODAY]['pmids'],
    'gaps_audited': ['11'],
    'identifiers_resolved': list(RESOLUTIONS),
    'corrections_made': [
        'PMC12211534 "no nutrition arm" reading is CIRCULAR - the review excludes nutrition by '
        'design. Blocked before publication.',
        'PMC12211534 = PMID 40598585, already in corpus and VETTED. Was logged as a novel find.',
        'Diabetes 74(8):1339 = PMID 40690616, pubtype EDITORIAL + COMMENT, comments on corpus '
        'paper 40272935. Not an authoritative source.',
        'NCT06976658 intervention is dorzagliatin; the "inactivating GCK mutations" restriction '
        'is NOT in the registry fields read and was asserted without support.',
        'NCT07360080 primary completion 2035-10-29 - demoted from active watch.',
        'Canonical Gap #11 GOLD tier rested on two papers that never mention its subject.',
    ],
    'summary': (
        'Mon 2026-09-07 - THE HUB\'S BEST-RATED GAP WAS EVIDENCED BY TWO PAPERS THAT ARE NOT '
        'ABOUT IT, AND A REVIEW\'S INCLUSION CRITERIA WAS ABOUT TO BE PUBLISHED AS AN EVIDENCE '
        'GAP.\n'
        ' (0) P0 UNCHANGED AND NOW 140 DAYS OLD. main is 103 commits ahead of origin/main; '
        'origin tip is still f7e976f (2026-04-20). Push was attempted and failed with '
        '"could not read Username for https://github.com" - no credential helper, no '
        '~/.git-credentials, no GH_TOKEN. Everything below exists only in the working tree. '
        'PUSH_AND_VERIFY.ps1 is staged on the Windows side and needs a human to run it.\n'
        ' (1) CANONICAL GAP #11 got its first audit under its own question. Its GOLD tier rested '
        'on PMID 19104422 and 37105208 - a 2008 registry update and a graft-function cohort. '
        'Neither mentions equity, race, ethnicity or access. An absence claim was being carried '
        'by two papers that are not about the thing claimed absent. Two all-time searches were '
        'run today (islet transplantation x equity terms: 23 hits, 0 relevant on screening; '
        '"Collaborative Islet Transplant Registry": 31 hits, none on equity). The gap SURVIVES - '
        'verdict VALID at LIKELY - but must be scoped to "no PubMed-indexed analysis", since '
        'CITR annual reports and conference abstracts were not reachable. Tier held at GOLD, not '
        'rewritten, because the single-writer refactor has not landed.\n'
        ' (2) A CIRCULAR ABSENCE CLAIM WAS CAUGHT BEFORE PUBLICATION. PMC12211534 was filed on '
        '2026-09-03 as supporting Gap #13 "as a NEGATIVE (no nutrition arm)". Reading the actual '
        'abstract today: the review includes only RCTs of IMMUNOMODULATORY therapies. Nutrition '
        'was excluded by design, so its absence says nothing. Publishing that would have '
        'manufactured an evidence gap out of another study\'s scope. New doctrine note written.\n'
        ' (3) THE SAME PAPER WAS ALREADY IN THE CORPUS. PMC12211534 = PMID 40598585, VETTED. '
        'The novelty check runs before PMCID normalisation, so a held paper was carried as an '
        'external find for four days. Queued as a pipeline fix.\n'
        ' (4) ALL FOUR IDENTIFIERS PARKED ON 2026-09-03 ARE NOW RESOLVED. NCBI and '
        'ClinicalTrials.gov were both reachable this run via web_fetch against the JSON APIs, '
        'which is what failed last time. Two carried corrections beyond the ones above: '
        'Diabetes 74(8):1339 is PMID 40690616 and is an EDITORIAL commenting on corpus paper '
        '40272935, not an authoritative source; NCT06976658 is dorzagliatin (Phase 2, n=44, '
        'CUHK, completes 2026-12-31) and the "inactivating GCK mutations" restriction is not in '
        'the registry fields. NCT07360080 is real but completes 2035-10-29 and was demoted.\n'
        ' (5) 5 PAPERS VETTED, 7 INGESTED, 7 SCREENED OUT. The 5 carried from yesterday all '
        'round-tripped against live PubMed. Two of them (42698953, 39084449) are PRECLINICAL and '
        'are flagged so they can never be cited as human evidence. The Monday sweep returned 12 '
        'hits across 6 queries; 7 were query artifacts (gout, pulmonary hypertension, telmisartan '
        'chemistry) and were screened out with reasons recorded. Verapamil returned zero over 30 '
        'days.\n'
        ' (6) DORZAGLIATIN CONVERGENCE. NCT06976658, PMID 42014686 and the GKA paths under Gaps '
        '#7 and #15 are all the same molecule and are being tracked as separate threads. '
        'Reconcile before the GKA line is presented as independent evidence.'),
})

state['last_run'] = TODAY
state['last_updated'] = TODAY

with open(STATE, 'w', encoding='utf-8') as fh:
    json.dump(state, fh, indent=2, ensure_ascii=False)

print('[OK] agent_state.json written %s' % TODAY)
print('[OK] papers vetted: %d' % len(VETTED_TODAY))
print('[OK] papers ingested: %d' % (len(INGEST) + len(GAP11_INGEST)))
print('[OK] papers screened out: %d' % len(state['screened_out'][TODAY]['pmids']))
print('[OK] identifiers resolved: %d' % len(RESOLUTIONS))
print('[OK] gaps audited: 11 (first audit on canonical question)')
print('[OK] queue: %d items (%d closed, %d added)' % (len(state['work_queue']), len(CLOSED), len(NEW_ITEMS)))
from collections import Counter
print('[OK] paper status: %s' % Counter(v.get('status') for v in papers.values()))
