#!/usr/bin/env python3
"""Close out the 2026-08-21 automated iteration: record findings, requeue work.

Run summary
-----------
Root-caused the two extractor defects logged 2026-08-18 to a SINGLE cause, then
found a third and much larger defect of the same class while proving the fix.
See run_history entry for the full account.
"""
import json
import os
import shutil
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
STATE = os.path.join(RESULTS, 'agent_state.json')
TODAY = '2026-08-21'

with open(STATE, encoding='utf-8') as f:
    state = json.load(f)

bak = f'{STATE}.bak_{TODAY}'
if not os.path.exists(bak):
    shutil.copyfile(STATE, bak)

# ---------------------------------------------------------------------------
# 1. Verified citation replacements (queue item P1, 2026-08-20)
#    Every PMID below was resolved through the NCBI eutils esummary API during
#    this run; title/journal/year recorded so the check is reproducible.
# ---------------------------------------------------------------------------
VERIFIED = {
    'metformin -> cardiovascular': {
        'add_pmids': ['33549430', '21205121'],
        'replaces': '22473097 (aspirin/cancer - off topic, purged 2026-08-20)',
        'verified': [
            '33549430 | 2021 | Nutr Metab Cardiovasc Dis | Effect of metformin on all-cause '
            'mortality and major adverse cardiovascular events: an updated meta-analysis of RCTs',
            '21205121 | 2011 | Diabetes Obes Metab | Effect of metformin on cardiovascular '
            'events and mortality: a meta-analysis of randomized clinical trials',
        ],
        'note': 'Both are RCT meta-analyses of the exact claim. Neither overturns the existing '
                'PARTIALLY_VALIDATED rating: 21205121 finds benefit vs placebo but not vs '
                'active comparator, and 33549430 reaches significance for all-cause mortality '
                'only after excluding SU/SGLT2i/GLP-1 comparators. Rating unchanged.',
    },
    'dapagliflozin -> nephropathy': {
        'add_pmids': ['32970396', '33338413'],
        'replaces': '35364937 (Bhattacharyya distance - off topic, purged 2026-08-20)',
        'verified': [
            '32970396 | 2020 | N Engl J Med | Dapagliflozin in Patients with Chronic Kidney '
            'Disease (DAPA-CKD primary results)',
            '33338413 | 2021 | Lancet Diabetes Endocrinol | Effects of dapagliflozin on major '
            'adverse kidney and cardiovascular events in diabetic and non-diabetic CKD',
        ],
        'note': 'SEPARATE DEFECT FOUND while doing this: the path\'s only stored external PMID '
                'was 32862232, which is the DAPA-CKD BASELINE CHARACTERISTICS paper, not the '
                'outcome paper. A baseline-characteristics publication reports who was enrolled, '
                'not what happened to them, so it cannot support a renoprotection claim. The '
                'primary results paper (32970396) is now cited. This is the same defect class as '
                'the 2026-08-19 insulin_glargine finding (inclusion-criteria text read as '
                'outcome evidence) and suggests a targeted sweep is warranted - queued.',
    },
    'pioglitazone -> inflammation': {
        'add_pmids': ['16490432', '20926154'],
        'replaces': '19136609 (cardiac fibroblasts - off topic, purged 2026-08-20)',
        'verified': [
            '16490432 | 2006 | Am J Cardiol | Meta-analysis of the effect of thiazolidinediones '
            'on serum C-reactive protein levels',
            '20926154 | 2010 | Diabetes Res Clin Pract | The impacts of thiazolidinediones on '
            'circulating C-reactive protein levels in different diseases: a meta-analysis',
        ],
        'note': 'Confirms the union the 2026-08-20 queue item anticipated. Both are TZD/CRP '
                'meta-analyses, i.e. CLASS-level not pioglitazone-specific, and both measure CRP '
                'only - they do not support the stored IL-6/TNF-alpha part of the claim. The '
                '2026-08-15 PARTIALLY_VALIDATED downgrade stands and is reinforced.',
    },
}

for path, rec in VERIFIED.items():
    entry = state['validated_paths'].setdefault(path, {})
    pmids = entry.get('external_pmids', [])
    for p in rec['add_pmids']:
        if p not in pmids:
            pmids.append(p)
    entry['external_pmids'] = pmids
    entry.setdefault('citation_repairs', []).append({
        'date': TODAY,
        'replaces': rec['replaces'],
        'added': rec['add_pmids'],
        'verified_via': 'NCBI eutils esummary, this run',
        'verified_records': rec['verified'],
        'note': rec['note'],
    })

# ---------------------------------------------------------------------------
# 2. Doctrine note - the finding that matters most from this run
# ---------------------------------------------------------------------------
state['doctrine_notes'][TODAY] = (
    'A REGEX WITH AN UNBOUNDED WILDCARD IS NOT AN EXTRACTOR, IT IS A RANDOM NUMBER '
    'GENERATOR. The inflammatory_markers patterns ended in `.*?(\\d+\\.?\\d*)` - no '
    'distance bound, no sentence boundary, no unit requirement - so the capture group '
    'took the first digit anywhere downstream of the marker name. In immunology prose '
    'that digit is almost never a measurement: it is the 3 in NLRP3, the 1 in IL-1, a '
    'publication year, a section number, a sample size. 85 of 92 extractions were '
    'artifacts, and they were the entire evidence base of the site\'s top-ranked '
    'research path. GENERAL RULE, now applied: a numeric extraction must be bounded by '
    'a sentence boundary AND anchored to a unit, a percent tied to a direction verb, or '
    'a fold-change token. A number with no unit is not a measurement. Corollary that '
    'cost four separate patches today: suppression applied in one place is not '
    'suppression - the same hollow path was still live in the validated-path store, the '
    'validation summary counter, and the Bayesian ranking after being removed from the '
    'path dashboard.'
)

# ---------------------------------------------------------------------------
# 3. Audit notes
# ---------------------------------------------------------------------------
state['audit_notes'].append({
    'date': TODAY,
    'finding': 'inflammatory_markers extraction was 92% artifact; 29 of 47 research paths '
               'had zero surviving corpus evidence once it was fixed.',
    'evidence': 'Corpus 414 -> 292 data points. inflammatory_markers 92 -> 7; all 7 survivors '
                'carry an explicit unit (pg/mL, mg/L, ng/ml, mg/dL) or a fold-change. '
                'Path recount against live extraction: 29 HOLLOW (exact zero, since the '
                'recount rule is a superset of the original clustering).',
    'top_casualty': 'NLRP3_inflammasome -> inflammation, formerly rank #1 with 61 data points '
                    'from 2 narrative reviews (31036962, 39412512), now 0.',
    'also_removed': 'oxidative_stress -> inflammation (22 -> 0) was ranked #1 in the published '
                    'Bayesian synthesis at posterior 72.7% MODERATE; NLRP3_inflammasome -> '
                    'inflammation was #2 at 55.3%. Posteriors computed from artifact counts.',
    'confirms': 'Queue item of 2026-08-18 ("re-audit every path whose corpus evidence is a '
                'REVIEW ARTICLE only") - independently and more broadly than it anticipated.',
})

# ---------------------------------------------------------------------------
# 4. Work queue: drop completed, add what this run exposed
# ---------------------------------------------------------------------------
DONE_MARKERS = (
    'EXTRACTOR DOUBLE-COUNTS BILINGUAL',
    'EXTRACTOR SCRAPES TABLE FRAGMENTS',
    'research_paths.json IS AN ORPHAN',
)
queue = [q for q in state['work_queue']
         if not any(m in q.get('target', '') for m in DONE_MARKERS)]

NEW = [
    {
        'priority': 1,
        'type': 'user_action_required',
        'added': TODAY,
        'target': 'HUMAN CALL: 29 OF 47 RESEARCH PATHS ARE NOW SUPPRESSED AS HOLLOW. The '
                  '2026-08-21 extraction fix removed their entire evidence base because it was '
                  'regex artifact. They are hidden from the dashboards, NOT deleted, and '
                  'research_paths.json retains data_point_count_stored for every one. Three '
                  'options per path: (a) re-source it from the corpus with the corrected '
                  'extractor, (b) keep it as a hypothesis with external-only evidence and no '
                  'corpus count, (c) retire it. Highest-value first: NLRP3_inflammasome -> '
                  'inflammation (61 displayed), oxidative_stress -> inflammation (22), '
                  'dapagliflozin -> inflammation (7), NF_kB -> inflammation (5). NOTE these are '
                  'mechanistically plausible paths with real external validation - the corpus '
                  'never supported them, which is a different statement from them being wrong.',
    },
    {
        'priority': 1,
        'type': 'verify_publish',
        'added': TODAY,
        'target': 'THE PUBLISHED CORPUS HEADLINE IS NOW 292, NOT 414. Every dashboard rebuilt '
                  'this run reflects it, but any prose in README.md, RESEARCH_DOCTRINE.md, '
                  'Research_Findings_Summary.md or OSF_PREREGISTRATION.md that quotes 414 (or '
                  '490, or 528) is now wrong. Grep for those figures and reconcile. Related and '
                  'still open: the P1 item asking whether 178 dose_response labels belong in a '
                  'headline "data points" figure at all - if that is answered no, the honest '
                  'headline is roughly 114 findings + 178 dose/protocol descriptors.',
    },
    {
        'priority': 1,
        'type': 'fix_pipeline',
        'added': TODAY,
        'target': 'AUDIT THE OTHER 8 EXTRACTORS FOR THE UNBOUNDED-WILDCARD DEFECT. Only '
                  'inflammatory_markers was rewritten this run, because that is the one where '
                  'the defect was proven. c_peptide, hba1c_change, survival_graft and remission '
                  'all contain `.*?` between the marker and the capture group and are therefore '
                  'suspect by construction. remission is the priority: 48 of the surviving 292 '
                  'data points (16%) come from it and its third pattern is '
                  'r"(\\d+)/(\\d+).*?(?:remission|complete response)", which can pair any two '
                  'numbers in a sentence with a later mention of remission. Method that worked: '
                  'dump every extraction for the type with its matched_text, classify by hand, '
                  'then require a unit or an explicit denominator.',
    },
    {
        'priority': 2,
        'type': 'verify_citations',
        'added': TODAY,
        'target': 'SWEEP FOR BASELINE/DESIGN PAPERS CITED AS OUTCOME EVIDENCE. Found this run: '
                  'dapagliflozin -> nephropathy cited PMID 32862232, the DAPA-CKD BASELINE '
                  'CHARACTERISTICS paper, as proof of renoprotection. That PMID resolves and is '
                  'on topic, so every existing gate passes it - the defect is that a '
                  'baseline-characteristics paper reports who enrolled, not what happened. Same '
                  'class as the 2026-08-19 insulin_glargine finding. Detection: flag cited '
                  'titles matching /baseline characteristic|study protocol|rationale and design|'
                  'design and methods|statistical analysis plan/i and require a second PMID '
                  'carrying the actual result.',
    },
    {
        'priority': 2,
        'type': 'verify_citations',
        'added': TODAY,
        'target': 'REPLACE THE REMAINING 8 PURGED OFF-TOPIC CITATIONS. Three done and verified '
                  'via eutils this run (metformin -> cardiovascular, dapagliflozin -> '
                  'nephropathy, pioglitazone -> inflammation). Still needed: rapamycin -> '
                  'islet_transplant (was 11961148), NF_kB -> inflammation (was 21067385), '
                  'oxidative_stress -> inflammation (was 29515440), dapagliflozin -> '
                  'inflammation (was 32332732 + 37973095), metformin -> inflammation (was '
                  '32398655 + 34107285), dapagliflozin -> cardiovascular (was 36041242), '
                  'empagliflozin -> inflammation (was 36547847), empagliflozin -> nephropathy '
                  '(was 38934094). All eight are currently HOLLOW, so this is lower urgency '
                  'than it was - but if the human call above re-sources any of them, its '
                  'external citation must be correct first.',
    },
    {
        'priority': 3,
        'type': 'fix_pipeline',
        'added': TODAY,
        'target': 'RESTORE EXACT PER-PATH COUNTS. recount_paths_from_corpus.py deliberately '
                  'publishes an UPPER BOUND, because its rule (pmids x data_types cross product) '
                  'is a superset of the original clustering - verified: it yields 62 for '
                  'NF_kB -> inflammation where the file stores 5. Zero is exact, so the HOLLOW '
                  'verdicts are safe, but nonzero figures must not be published as measurements '
                  'and are currently written to data_point_count_upper_bound rather than '
                  'data_point_count. Recovering exact counts needs the original clustering rule, '
                  'which is still not in the repo.',
    },
]
queue = NEW + queue
for i, q in enumerate(queue):
    q['queue_position'] = i
state['work_queue'] = queue

# ---------------------------------------------------------------------------
# 5. Run history
# ---------------------------------------------------------------------------
state['run_history'].append({
    'date': TODAY,
    'day': 'Friday',
    'papers_checked': 0,
    'paths_validated': 3,
    'issues_found': 6,
    'changes_pushed': False,
    'summary': (
        'Fri 2026-08-21 - THE TOP-RANKED RESEARCH PATH ON THE SITE HAD NO EVIDENCE BEHIND IT. '
        '(1) ONE ROOT CAUSE, NOT TWO. The bilingual double-count and the table-fragment defect '
        'logged 2026-08-18 are the same bug: section types FIG, TABLE and ABBR were documented '
        'as skip-worthy in the source comment since the file was written but were never added '
        'to SKIP_SECTION_TYPES. PMID 39412512 carries its results table twice (English section '
        '60, Portuguese section 247, both typed TABLE) - that is where "10 mg or"/"10 mg ou" '
        'came from. Measured both options rather than assuming: scanning TABLE yields 58 extra '
        'extractions, and all 58 were inspected individually - 46 bare dose labels, 7 '
        'abbreviation glossaries, 5 table cross-references, zero measurements. TABLE stays '
        'skipped. (2) THE LARGER DEFECT, found while proving the fix. inflammatory_markers '
        'patterns ended in an unbounded `.*?(\\d+)`, so the capture took the first digit '
        'downstream regardless of distance, sentence boundary or unit. 85 of 92 extractions '
        'were not measurements: the 3 in NLRP3, the 1 in IL-1, the year 2014, section number '
        '7.2, sample size 500. Patterns rewritten to require a sentence-bounded gap plus a unit, '
        'a direction-verb-tied percent, or a fold change: 92 -> 7, and all 7 survivors carry an '
        'explicit unit. Corpus 414 -> 292. (3) THE CASUALTIES. Recounted all 47 paths against '
        'live extraction; 29 are HOLLOW with exactly zero surviving data points. Worst is '
        'NLRP3_inflammasome -> inflammation, formerly rank #1 with 61 data points, whose '
        'displayed key_claims were prose fragments like "NLRP3 activation could be a trigger '
        'for DKD. Additionally, pharmacological inhibition of the IL-1" with "value" = 1. Its '
        'two sources are both narrative reviews. (4) SUPPRESSION LEAKED THREE MORE TIMES. '
        'Removing hollow paths from the path dashboard left them live in the validated-path '
        'store (different key spelling), in the validation_summary counter (read from a '
        'precomputed field, never recomputed - page rendered "Total paths: 17" beside '
        '"VALIDATED paths (22 total)"), and in the Bayesian ranking, which was still publishing '
        'oxidative_stress -> inflammation at posterior 72.7% MODERATE and NLRP3_inflammasome -> '
        'inflammation at 55.3% - both with zero evidence. All four sites patched; verified no '
        'hollow path string survives anywhere under docs/. (5) CITATIONS. Three of the 13 '
        'purged off-topic citations replaced with sources verified through eutils this run. '
        'Found a new defect class doing it: dapagliflozin -> nephropathy was citing the '
        'DAPA-CKD BASELINE CHARACTERISTICS paper (32862232) as evidence of renoprotection - it '
        'resolves, it is on topic, every gate passes it, and it reports who enrolled rather '
        'than what happened. Queued a targeted sweep. (6) Credibility sweep clean; 54/54 '
        'pipeline scripts [OK] after the four patches.'
    ),
})

state['last_run'] = TODAY
state['last_updated'] = f'{TODAY}T00:00:00'

with open(STATE, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f'[OK] state saved  (backup: {os.path.basename(bak)})')
print(f'     work queue   : {len(state["work_queue"])} items ({len(NEW)} new)')
print(f'     validated_paths repaired: {len(VERIFIED)}')
print(f'     run_history  : {len(state["run_history"])} runs')
