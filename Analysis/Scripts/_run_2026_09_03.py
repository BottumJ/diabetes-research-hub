#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""State update for the 2026-09-03 scheduled run.

Headline: yesterday's Gap #15 finding was under-called by 5x. Five state gap
numbers - not one - carry audit trails answering a different question than the
number names on the site, and the gap TIER is hardcoded in 24 places with no
store read in any of them.

Also: three canonical gap audits (two of them first-ever under the correct
question), three overdue trial watches, and one memory-vs-store tier correction.
"""

import json
import os
import shutil
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RESULTS = os.path.join(ROOT, 'Analysis', 'Results')
STATE = os.path.join(RESULTS, 'agent_state.json')
TODAY = '2026-09-03'

shutil.copy(STATE, STATE + '.bak_' + TODAY)
with open(STATE, 'r', encoding='utf-8') as fh:
    s = json.load(fh)

gaps = s['gaps']

# ---------------------------------------------------------------------------
# 1. THE NUMBERING COLLISION. Annotate, do not re-home.
# ---------------------------------------------------------------------------
# Each of these trails is internally consistent back to April. They are real
# audits of real questions, filed under a number that names a different one.
# Deleting or moving them would destroy the evidence that the collision is
# systemic rather than a one-off, which is the whole finding.
MISFILED = {
    '4':  ('Islet Transplant x Personalized Nutrition',
           'not in the canonical 15-gap registry'),
    '5':  ('Islet Transplant x Drug Repurposing',
           'is canonical Gap #4'),
    '7':  ('Polygenic Risk Score x Closed-Loop AID',
           'not in the canonical 15-gap registry'),
    '11': ('CAR-Treg x Personalized Nutrition',
           'not in the canonical 15-gap registry'),
    '12': ('Treg x Diabetic Peripheral Neuropathy',
           'is canonical Gap #5'),
    '15': ('SGLT2i x Personalized Nutrition',
           'not in the canonical 15-gap registry; identified 2026-09-02'),
}
for gid, (subject, where) in MISFILED.items():
    gaps.setdefault(gid, {})['audit_trail_provenance'] = {
        'flagged': TODAY,
        'trail_actually_audits': subject,
        'that_question_is': where,
        'canonical_name_of_this_number': None,   # filled below
        'action': ('ANNOTATED, NOT RE-HOMED. Re-homing rewrites the audit '
                   'record and the destination gap has its own parallel '
                   'history; which trail is authoritative is a human call.'),
        'detector': 'Analysis/Scripts/audit_gap_numbering.py',
    }

with open(os.path.join(RESULTS, 'gap_evidence.json'), 'r',
          encoding='utf-8') as fh:
    canonical = json.load(fh)['gaps']
for gid in MISFILED:
    gaps[gid]['audit_trail_provenance']['canonical_name_of_this_number'] = (
        canonical.get(gid, {}).get('name'))

# ---------------------------------------------------------------------------
# 2. TIER: correct MEMORY to match the store. Do not touch the SITE.
# ---------------------------------------------------------------------------
# #13: agent_state said SILVER; gap_evidence.json AND the published site both
# say BRONZE. Memory was the outlier and it was the optimistic outlier, so
# aligning it down is a correction, not a re-tiering. The 2026-08-04 audit
# had already concluded "promotion not justified" - the tier field simply never
# followed the verdict.
gaps['13']['tier'] = 'BRONZE'
gaps['13']['tier_corrected'] = {
    'date': TODAY,
    'from': 'SILVER',
    'to': 'BRONZE',
    'why': ('agent_state was the only store claiming SILVER; gap_evidence.json '
            'and docs/index.html both publish BRONZE, and the 2026-08-04 audit '
            'in this same record concluded promotion was not justified. '
            'Memory corrected to the store; no published claim changed.'),
}
# #6 and #11 are the OPPOSITE direction - store and memory say GOLD while the
# site publishes SILVER. Raising a published tier is a scientific judgement, so
# those go to the human queue below rather than being applied here.

# ---------------------------------------------------------------------------
# 3. GAP AUDITS
# ---------------------------------------------------------------------------
gaps['13'].setdefault('audit_history', []).append({
    'date': TODAY,
    'tier_before': 'SILVER (memory) / BRONZE (store+site)',
    'tier_after': 'BRONZE (all stores)',
    'auditor': 'scheduled-iterate',
    'new_evidence_found': True,
    'promotes_gap': False,
    'notes': (
        'Monthly audit (prev 2026-08-04, 30d). THE COMPARATOR LITERATURE '
        'MATURED AND THE GAP GOT WIDER, NOT NARROWER. Search surfaced a '
        'systematic review + network meta-analysis of interventions preserving '
        'beta-cell function in new-onset T1D covering 60 trials / 4,597 '
        'patients / 32 intervention classes, reporting 11 interventions with '
        'significantly higher C-peptide than placebo at 12 months (MSC, '
        'azathioprine, interferon-alpha, autologous dendritic cells, '
        'golimumab, low-dose ATG, teplizumab variants, baricitinib, '
        'cyclosporin). PMC12211534 - PMID NOT VERIFIED THIS RUN, logged as a '
        'pending identifier, not cited. Its relevance here is as a NEGATIVE '
        'result for this gap: 32 intervention classes were mapped against a '
        'C-peptide endpoint and NOT ONE of them is a nutrition intervention. '
        'The drug side of the beta-cell-preservation question now has a '
        'network meta-analysis; the nutrition side still has no trial with a '
        'C-peptide or beta-cell primary endpoint at all. That asymmetry is '
        'evidence the gap is real, not evidence it is closing. Also searched '
        'precision-nutrition x C-peptide 2026 directly: nothing new since the '
        '2026-08-04 finding that both 2025 SR&MAs address dietary patterns -> '
        'glycemic/weight outcomes, not personalized nutrition -> beta-cell '
        'preservation. REMAINS BRONZE. Promotion trigger unchanged: one trial '
        'with a personalized/precision-nutrition intervention and a C-peptide '
        'or beta-cell-function PRIMARY endpoint. Next audit ~2026-10-03.'),
})
gaps['13']['last_audited'] = TODAY

gaps['7'].setdefault('audit_history', []).append({
    'date': TODAY,
    'tier_before': 'SILVER',
    'tier_after': 'SILVER',
    'auditor': 'scheduled-iterate',
    'new_evidence_found': True,
    'promotes_gap': False,
    'first_audit_under_canonical_question': True,
    'notes': (
        'FIRST AUDIT THIS GAP HAS EVER RECEIVED UNDER ITS OWN QUESTION. The '
        'four prior entries under gaps["7"] (2026-04-24 through 2026-08-05) '
        'audit polygenic risk score x closed-loop AID; canonical Gap #7 is the '
        'GKA Drug Repurposing Landscape. Those four are annotated, not moved. '
        'FINDINGS, all UNVERIFIED identifiers - browser access to '
        'ClinicalTrials.gov and NCBI was denied during this unattended run, so '
        'nothing below is cited anywhere and all of it is queued for '
        'verification. (a) NCT06976658 "RESENSE", an allosteric glucokinase '
        'activator in monogenic diabetes from inactivating GCK mutations, '
        'reported start 2025-04-30, estimated completion 2026-12-31. If real, '
        'this is the strongest signal the gap has: a GKA deployed in an '
        'indication outside T2D, which is precisely the repurposing question. '
        '(b) A 2025 perspective in Diabetes (reported 74(8):1339) titled '
        '"Glucokinase Activators: A Humbling Lesson in Drug Development" - a '
        'candidate authoritative source for the why-most-GKAs-failed section '
        'the dashboard already carries. (c) Dorzagliatin in GCK-MODY '
        '(increased absolute and incremental second-phase insulin secretion '
        'vs placebo) reconfirms the monogenic direction. NOTHING CHANGES '
        'TODAY: the design grader rates this gap PRIMARY_THIN (3 of 13 '
        'design-readable papers report primary data), and adding an '
        'unverified trial to a thin gap would make it worse, not better. '
        'REMAINS SILVER. Next audit ~2026-10-03, gated on verifying (a).'),
})
gaps['7']['last_audited'] = TODAY

gaps['12'].setdefault('audit_history', []).append({
    'date': TODAY,
    'tier_before': 'SILVER',
    'tier_after': 'SILVER',
    'auditor': 'scheduled-iterate',
    'new_evidence_found': False,
    'promotes_gap': False,
    'first_audit_under_canonical_question': True,
    'notes': (
        'FIRST AUDIT THIS GAP HAS EVER RECEIVED UNDER ITS OWN QUESTION. The '
        'four prior entries under gaps["12"] (2026-04-19 through 2026-08-07) '
        'audit Treg / CAR-T x diabetic peripheral neuropathy, which is '
        'canonical Gap #5. Annotated, not moved. FINDING: no systematic '
        'catalogue mapping off-patent generic drugs to diabetes MECHANISMS '
        'exists. What exists is mechanism-agnostic and computational - a '
        'genetically-supported EHR repurposing pipeline for diabetes, omics '
        'repositioning by connectivity mapping (58 drugs screened, 9 '
        'candidates, COX2 and ADRA2A targets) - none of which is organised as '
        'a drug x mechanism map, and none of which restricts to generics. The '
        'intersection stays open. VERIFIED NEGATIVE, worth recording because '
        'it is the failure mode this gap invites: the published card reads '
        '"verapamil (beta cell protection), fenofibrate (retinopathy), '
        'colchicine (CV risk)" and each of those three attributions is '
        'correct. Fibrates have NO cardiovascular outcome benefit in T2D on '
        'statins (neither ACCORD-Lipid nor PROMINENT), and the card does not '
        'claim one - checked by hand across all published HTML this run. '
        'CAVEAT ON THE TIER: the design grader rates this gap UNGRADEABLE - '
        '4 of 7 papers carry no design-bearing pubtype and ZERO report primary '
        'data. SILVER here is unverifiable rather than wrong, and this audit '
        'does not change that. REMAINS SILVER. Next audit ~2026-10-03.'),
})
gaps['12']['last_audited'] = TODAY

# ---------------------------------------------------------------------------
# 4. TRIAL WATCHES DUE 2026-09-02
# ---------------------------------------------------------------------------
s.setdefault('topic_checks', {})
s['topic_checks']['bandit_96week_2026_09'] = {
    'topic': 'BANDIT baricitinib T1D 96-week off-therapy follow-up',
    'date_checked': TODAY,
    'status': 'PRESENTED_NOT_INDEXED',
    'findings': [
        'EASD Vienna 2025 (Sep 15-19) presentation + broad trade coverage: '
        'benefit does not survive withdrawal. C-peptide significantly higher '
        'at week 72, NO LONGER significant at week 96.',
        'Reported means: 72w 0.49 (baricitinib) vs 0.36 (placebo); '
        '96w 0.37 vs 0.26. Treatment was 48 weeks, follow-up 96 weeks from '
        'treatment start, n=91, ages 10-30, within 100 days of diagnosis.',
        'No peer-reviewed journal publication of the 96-week readout located. '
        'The 48-week result remains NEJM 2023 (PMID 38055252).',
    ],
    'why_it_matters': (
        'The repo carries baricitinib as an active repurposing signal. The '
        '96-week result is the strongest available evidence that the effect '
        'is suppression, not modification - no dashboard may imply durable '
        'benefit off therapy. Effect sizes above are from conference and '
        'trade reporting, NOT from a peer-reviewed source, and must not be '
        'published as measurements until a journal version exists.'),
    'next_recheck': '2026-10-03',
}
s['topic_checks']['dapan_dia_2026_09'] = {
    'topic': 'DAPAN-DIA NCT06047262 dapansutrile T2D primary results',
    'date_checked': TODAY,
    'status': 'ENROLLING_NO_RESULTS',
    'findings': [
        'Still enrolling. Design per AHA 2024 abstract 4115645 (Circulation '
        '150 suppl 1): n=300, T2D with HbA1c >7.5% and hsCRP >1.5 mg/L, '
        'dapansutrile 1000 mg BID vs placebo 2:1, 6 months, primary endpoint '
        'change in HbA1c; secondaries IL-1beta, IL-6, hsCRP, MASLD progression.',
        'Described as the first adequately-powered placebo-controlled trial '
        'of an oral NLRP3-specific inhibitor. Estimated completion 2026.',
    ],
    'why_it_matters': (
        'This is the trial that would move SGLT2i_NLRP3_DKD off surrogate '
        'biomarkers - except it will not: the primary endpoint is HbA1c, and '
        'the secondaries are inflammatory biomarkers. Even a positive '
        'DAPAN-DIA does NOT supply the renal hard endpoint the P4 queue item '
        'has been waiting for since 2026-08-17. Recording that now so a '
        'future run does not mistake this readout for gap closure.'),
    'next_recheck': '2026-10-03',
}
s['topic_checks']['protect_extension_2026_09'] = {
    'topic': 'PROTECT extension NCT04598893 teplizumab long-term readout',
    'date_checked': TODAY,
    'status': 'NO_PUBLICATION',
    'findings': [
        'Observational extension, 42-month follow-up of PROTECT completers, '
        'no study drug administered. Parent PROTECT: phase 3, ages 8-17, '
        'within 6 weeks of diagnosis, ~300 randomised 2:1.',
        'No peer-reviewed publication of extension results located.',
        'Adjacent and NEW: NCT07360080 "Long-Term Outcomes of Teplizumab in '
        'Routine Clinical Care" - registry-style real-world study. '
        'UNVERIFIED identifier, queued for registry confirmation.',
    ],
    'next_recheck': '2026-10-03',
}

# ---------------------------------------------------------------------------
# 5. UNVERIFIED IDENTIFIERS - the honest parking place
# ---------------------------------------------------------------------------
s.setdefault('watch_items_pending_pmid', [])
for item in [
    {
        'identifier': 'NCT06976658',
        'label': ('RESENSE - allosteric glucokinase activator in monogenic '
                  'diabetes from inactivating GCK mutations'),
        'source': 'WebSearch result (clinicaltrials.gov listing), 2026-09-03',
        'relevance': 'Canonical Gap #7 (GKA Drug Repurposing) - new indication',
        'status': 'UNVERIFIED_REGISTRY_ACCESS_DENIED',
        'verified_real': ('NO. ClinicalTrials.gov could not be opened during '
                          'this unattended run (browser navigation denied, '
                          'web_fetch returned an unrendered shell).'),
        'do_not_cite_until': 'registry record read directly',
        'logged_date': TODAY,
        'next_recheck': '2026-09-10',
    },
    {
        'identifier': 'Diabetes 2025;74(8):1339',
        'label': ('"Glucokinase Activators: A Humbling Lesson in Drug '
                  'Development" (ADA journal perspective)'),
        'source': 'WebSearch result (diabetesjournals.org), 2026-09-03',
        'relevance': 'Canonical Gap #7 - candidate authoritative source',
        'status': 'UNVERIFIED_NO_PMID',
        'verified_real': 'NO. Publisher page returned empty; no PMID resolved.',
        'do_not_cite_until': 'PMID resolved via PubMed',
        'logged_date': TODAY,
        'next_recheck': '2026-09-10',
    },
    {
        'identifier': 'PMC12211534',
        'label': ('SR + network meta-analysis, interventions preserving '
                  'beta-cell function in new-onset T1D (60 trials, 4,597 '
                  'patients, 32 intervention classes)'),
        'source': 'WebSearch result (ncbi.nlm.nih.gov/pmc), 2026-09-03',
        'relevance': ('Gap #13 as a NEGATIVE (no nutrition arm among 32 '
                      'classes); also touches baricitinib and teplizumab '
                      'paths'),
        'status': 'UNVERIFIED_NO_PMID',
        'verified_real': 'NO. PMCID seen in search result only; not resolved.',
        'do_not_cite_until': 'PMID resolved via PubMed',
        'logged_date': TODAY,
        'next_recheck': '2026-09-10',
    },
    {
        'identifier': 'NCT07360080',
        'label': 'Long-Term Outcomes of Teplizumab in Routine Clinical Care',
        'source': 'WebSearch result (clinicaltrials.gov), 2026-09-03',
        'relevance': 'PROTECT extension watch - real-world teplizumab arm',
        'status': 'UNVERIFIED_REGISTRY_ACCESS_DENIED',
        'verified_real': 'NO. Registry unreachable this run.',
        'do_not_cite_until': 'registry record read directly',
        'logged_date': TODAY,
        'next_recheck': '2026-09-10',
    },
]:
    s['watch_items_pending_pmid'].append(item)

# ---------------------------------------------------------------------------
# 6. DOCTRINE
# ---------------------------------------------------------------------------
s.setdefault('doctrine_notes', {})[TODAY] = (
    'A NUMBER COPIED INTO FOUR FILES IS NOT A FACT, IT IS FOUR FACTS THAT '
    'HAPPEN TO AGREE FOR A WHILE. Two findings, one cause. '
    '(1) NUMBERING. On 2026-09-02 a run found gaps["15"] had been auditing '
    'SGLT2i x personalized nutrition since April while canonical Gap #15 is '
    'GKA Pricing, and queued a re-homing of that one trail. Sweeping all '
    'fifteen the same way finds FIVE more: state #4, #5, #7, #11 and #12 each '
    'answer a question their number does not name, every one of them '
    'internally consistent back to April. Nothing drifted. Two numbering '
    'schemes were built independently and never reconciled. The lesson is not '
    'about gaps: when a run finds one instance of a defect, the next question '
    'is always how many instances the same measurement would find, and the '
    '2026-09-02 run stopped at one. '
    '(2) TIER. The gap tier is hardcoded in 24 places across 15 gaps and read '
    'from the evidence store in none of them - agent_state.json, '
    'gap_evidence.json, the card text in rebuild_website.py and the stage '
    'labels in run_quality_improvements.py all carry their own typed copy. '
    'Three gaps already disagree: #6 and #11 are GOLD in memory and in the '
    'store but publish as SILVER, #13 was SILVER in memory against BRONZE '
    'everywhere else. Memory was corrected down for #13 because it was the '
    'optimistic outlier; #6 and #11 go to the human queue because raising a '
    'published tier is a scientific judgement, not a reconciliation. '
    'GENERAL RULE ADOPTED: any value that appears on the published site and '
    'also in the agent memory must have exactly one writer and be read from '
    'it, or be gated. Gap tiers are now gated by '
    'Analysis/Scripts/audit_gap_numbering.py; they are not yet single-writer.'
)

# ---------------------------------------------------------------------------
# 7. QUEUE
# ---------------------------------------------------------------------------
q = s['work_queue']
s.setdefault('closed_queue_items', [])

# The 2026-09-02 item asked to re-home ONE trail. It is superseded, not done.
kept = []
for item in q:
    tgt = str(item.get('target') or '')
    if 'RE-HOME THE ORPHANED SGLT2i' in tgt:
        item['closed'] = TODAY
        item['closed_reason'] = (
            'SUPERSEDED, NOT COMPLETED. This item scoped the problem to one '
            'audit trail. The 2026-09-03 sweep found five more of the same '
            'shape, so re-homing #15 alone would have destroyed the evidence '
            'that the collision is systemic. Replaced by the consolidated '
            'P1 item added 2026-09-03.')
        s['closed_queue_items'].append(item)
        continue
    kept.append(item)
q = kept

q.insert(0, {
    'priority': 1,
    'type': 'user_action_required',
    'added': TODAY,
    'target': (
        'HUMAN CALL, AND IT REPLACES YESTERDAY\'S NARROWER ONE: THE AGENT\'S '
        'MEMORY AND THE PUBLISHED SITE USE THE SAME GAP NUMBERS FOR DIFFERENT '
        'QUESTIONS. Measured 2026-09-03 by Analysis/Scripts/audit_gap_'
        'numbering.py across all 15 gaps. FIVE trails are misfiled: state #4 '
        'audits islet transplant x personalized nutrition; #5 audits islet '
        'transplant x drug repurposing (= canonical #4); #7 audits polygenic '
        'risk score x closed-loop AID; #11 audits CAR-Treg x personalized '
        'nutrition; #12 audits Treg x diabetic peripheral neuropathy '
        '(= canonical #5). Plus #15, found yesterday. Every trail is '
        'internally consistent since April, so this is two numbering schemes, '
        'not drift, and 22 audits of real work are sitting under the wrong '
        'labels. THREE DECISIONS NEEDED. (a) Which numbering is authoritative '
        '- the site\'s (build_data_dictionary.py GAPS, mirrored in '
        'gap_evidence.json and extract_corpus_data.py) or the memory\'s? The '
        'site\'s is used by four scripts and is what readers see, so it is '
        'the obvious answer, but that means 22 audits need re-homing and two '
        'destination gaps (#4, #5) already have their own parallel history to '
        'merge with. (b) The four trails auditing questions that are NOT in '
        'the canonical 15 (islet x nutrition, PRS x AID, CAR-Treg x '
        'nutrition, SGLT2i x nutrition) are real research on real gaps with '
        'nowhere to live - promote them to gaps #16-#19, or archive? (c) '
        'TIER: #6 CAR-T Access and #11 Islet Registry Equity are GOLD in both '
        'agent_state and gap_evidence.json but publish as SILVER on '
        'docs/index.html. Raising a published tier is a scientific judgement '
        'so nothing was applied; but the site currently under-states two gaps '
        'relative to its own evidence store, and one of them (#11) rests on '
        'just 2 papers, which may mean the STORE is wrong rather than the '
        'site. Decide which way each goes.'),
})

q.insert(1, {
    'priority': 1,
    'type': 'fix_pipeline',
    'added': TODAY,
    'target': (
        'MAKE THE GAP TIER SINGLE-WRITER. Measured: the tier is typed into 24 '
        'places across 15 gaps (agent_state.json, gap_evidence.json, card '
        'text in rebuild_website.py, stage labels in '
        'run_quality_improvements.py) and read from a store in NONE of them. '
        'That is why #6, #11 and #13 could disagree without anything failing. '
        'audit_gap_numbering.py now catches disagreement, which is the '
        'stopgap, not the fix. The fix: gap_evidence.json becomes the single '
        'writer, rebuild_website.py and run_quality_improvements.py read the '
        'tier from it at build time, and agent_state stores no tier at all. '
        'Sequence matters - do this AFTER the human call above resolves which '
        'tier is right for #6 and #11, or the refactor will freeze the wrong '
        'value into the one place that then feeds everything.'),
})

q.insert(2, {
    'priority': 2,
    'type': 'verify_citations',
    'added': TODAY,
    'target': (
        'VERIFY THE FOUR IDENTIFIERS LOGGED UNVERIFIED ON 2026-09-03. Neither '
        'ClinicalTrials.gov nor NCBI could be reached during the unattended '
        'run - browser navigation was denied and web_fetch returned an '
        'unrendered page shell - so all four are parked in '
        'watch_items_pending_pmid and cited nowhere. (a) NCT06976658 RESENSE, '
        'allosteric GKA in monogenic GCK diabetes: the single most material '
        'find for canonical Gap #7 and the reason that gap did not move '
        'today. (b) Diabetes 2025;74(8):1339 "Glucokinase Activators: A '
        'Humbling Lesson in Drug Development" - needs a PMID. (c) PMC12211534 '
        'beta-cell-preservation network meta-analysis (60 trials, 32 '
        'intervention classes) - needs a PMID; load-bearing for the Gap #13 '
        'verdict and touches the baricitinib and teplizumab paths. (d) '
        'NCT07360080 real-world teplizumab outcomes. NONE may be cited until '
        'read from the registry or PubMed directly.'),
})

q.insert(3, {
    'priority': 2,
    'type': 'audit_gap',
    'added': TODAY,
    'target': (
        'RE-AUDIT THE FOUR GAPS WHOSE CANONICAL QUESTION HAS NEVER BEEN '
        'ASKED. Today gave canonical #7 and #12 their first audit under their '
        'own names. Canonical #4 (Drug Repurposing for Islet Transplant), #5 '
        '(Treg in Diabetic Neuropathy) and #11 (Islet Transplant Registry '
        'Equity) still have not had one - the trails filed under those '
        'numbers audit other questions. Note #5 and #4 are the exception: '
        'their questions HAVE been audited, just under numbers #12 and #5 '
        'respectively, so those two may only need re-homing rather than fresh '
        'work. #11 needs genuine new work - its published GOLD rests on 2 '
        'papers and nothing has audited islet transplant registry equity '
        'directly.'),
})

s['work_queue'] = q

# ---------------------------------------------------------------------------
# 8. RUN HISTORY
# ---------------------------------------------------------------------------
s['run_history'].append({
    'date': TODAY,
    'day': 'Thu',
    'queue_items_worked': 6,
    'gaps_audited': ['13', '7', '12'],
    'gate_status': '65/65 [OK] including the new gapnumbering stage',
    'summary': (
        'Thu 2026-09-03 - YESTERDAY\'S FINDING WAS UNDER-CALLED BY FIVE TIMES, '
        'AND THE TIER IT ARGUED ABOUT IS HARDCODED IN 24 PLACES. '
        '(1) THE COLLISION IS SYSTEMIC. The 2026-09-02 run found gaps["15"] '
        'auditing the wrong question since April and queued a re-homing of '
        'that one trail. Applying the same measurement to all fifteen finds '
        'FIVE more - state #4, #5, #7, #11, #12 - each internally consistent '
        'back to April. Two numbering schemes, never reconciled; 22 audits of '
        'real work filed under labels that name other questions. Built '
        'audit_gap_numbering.py to catch it, wired as pipeline stage '
        '"gapnumbering". The gate flagged a false positive on its own first '
        'run (#8 Immunomodulatory vs "immunomodulator") and two false '
        'negatives (#4, #11 passed on shared words like "islet"); both fixed '
        'by scoring only tokens that appear in fewer than 3 gap names, which '
        'is what made it find #4 and #11 at all. '
        '(2) TIER HAS NO OWNER. 24 hardcoded copies across 4 files, store read '
        'in none. Three already disagree: #6 and #11 GOLD in memory and store '
        'but SILVER on the site; #13 SILVER in memory against BRONZE '
        'everywhere else. Corrected #13 down in memory (optimistic outlier, '
        'and its own 2026-08-04 audit had already said promotion was not '
        'justified). Left #6/#11 alone and queued them: raising a published '
        'tier is a judgement, and #11 GOLD rests on 2 papers so the store may '
        'be the wrong one. '
        '(3) TWO GAPS AUDITED FOR THE FIRST TIME UNDER THEIR OWN QUESTION. '
        'Canonical #7 (GKA Drug Repurposing): found NCT06976658 RESENSE, an '
        'allosteric GKA in monogenic GCK diabetes - the strongest repurposing '
        'signal this gap has - but registry access was denied, so it is '
        'logged UNVERIFIED and the gap did not move. Canonical #12 (Generic '
        'Drug x Mechanism Catalog): no such catalogue exists; verified by '
        'hand that the published card does not overstate fenofibrate (it says '
        'retinopathy, correct - fibrates have no CV benefit in T2D on statins '
        'per ACCORD-Lipid and PROMINENT). Both remain SILVER, #12 with the '
        'standing caveat that its design grade is UNGRADEABLE. '
        '(4) GAP #13 audited on time: the beta-cell-preservation literature '
        'now has a 60-trial network meta-analysis across 32 intervention '
        'classes and NOT ONE is a nutrition intervention. That widens this '
        'gap rather than closing it. REMAINS BRONZE. '
        '(5) THREE OVERDUE TRIAL WATCHES CLEARED. BANDIT 96-week: benefit '
        'does not survive withdrawal (C-peptide significant at 72w, not at '
        '96w) - conference and trade sources only, no journal version, so the '
        'numbers are recorded as unpublishable. DAPAN-DIA still enrolling, '
        'and recorded now that its HbA1c primary endpoint means it will NOT '
        'supply the renal hard endpoint the NLRP3 queue item is waiting for. '
        'PROTECT extension: no publication. '
        '(6) Credibility sweep clean; 65/65 stages [OK]. Four new identifiers '
        'logged UNVERIFIED and cited nowhere - the unattended run had no '
        'registry or PubMed access.'),
})

s['last_run'] = TODAY
s['last_updated'] = TODAY

with open(STATE, 'w', encoding='utf-8') as fh:
    json.dump(s, fh, indent=2, ensure_ascii=False)

print('State updated for %s' % TODAY)
print('  gaps audited      : 13, 7, 12')
print('  trails annotated  : %s' % ', '.join(sorted(MISFILED, key=int)))
print('  tier corrected    : #13 SILVER -> BRONZE (memory aligned to store)')
print('  unverified logged : 4')
print('  queue             : %d open (1 closed as superseded)' % len(q))
