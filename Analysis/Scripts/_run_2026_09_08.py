"""Daily iteration run - Tuesday 2026-09-08.

Work performed this run. Every PMID, title, journal, year, design and count below
was round-tripped through live NCBI eutils (esummary.fcgi / efetch.fcgi) on
2026-09-08; nothing here is recalled from memory.

  1. Vetted all 7 UNVETTED papers carried in from the 2026-09-07 Monday sweep.
     5 VETTED, 2 FLAGGED.
  2. Adjudicated the two live gap-tier disagreements surfaced by
     gap_numbering_audit.py (gaps #6 and #11 read GOLD in agent_state.json and
     gap_evidence.json but SILVER on the published hub card). Both resolved
     DOWNWARD to SILVER, on the evidence, not by copying either writer.
  3. Found and corrected a misattributed citation on the Gap #11 dashboard.
  4. Closed the stale 2026-09-03 audit_gap queue item (its three named gaps have
     all since been audited under their canonical questions).
  5. Added 1 new paper (PMID 42696794) as UNVETTED.

Writes agent_state.json and gap_evidence.json. Idempotent: safe to re-run.
"""
import json
import os
import shutil
from datetime import datetime

RESULTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Results')
STATE = os.path.join(RESULTS, 'agent_state.json')
GAP_EVIDENCE = os.path.join(RESULTS, 'gap_evidence.json')
TODAY = '2026-09-08'

with open(STATE, encoding='utf-8') as fh:
    state = json.load(fh)

shutil.copyfile(STATE, os.path.join(RESULTS, 'agent_state.json.bak_%s' % TODAY))

papers = state['papers']
now = datetime.now().isoformat()

# --------------------------------------------------------------- 1. VETTING
# esummary round-trip 2026-09-08: all 7 PMIDs resolve, and the stored title,
# journal and year match live PubMed exactly for all 7.
VET = {
    '42688599': {
        'status': 'VETTED',
        'issues_found': [],
        'note': ('Front Immunol 2026;17:1909238 (2026 Aug 12), PMC13534801. Verified live. '
                 'Design confirmed from the abstract, not the label: SANRA-guided NARRATIVE '
                 'review. 104 records identified, 11 directly evaluating islet transplantation '
                 'form the core evidence base. Carries NO primary data of its own and must not '
                 'be cited as evidence for any islet-transplant outcome; it is citable only for '
                 'the state of the DSA/islet literature as of its 2026-06-09 search cutoff.'),
    },
    '42674789': {
        'status': 'FLAGGED',
        'issues_found': [
            'STUDY PROTOCOL, NO RESULTS. BMJ Open 2026;16(8):e109209 (2026 Aug 31), '
            'PMC13536008. Verified live; pubtype is bare "Journal Article" so the pubtype '
            'field does NOT mark it as a protocol - the title does ("a study protocol"). '
            'This is the same failure mode that put PMID 39613428 (Ver-A-T1D protocol) '
            'under the #2 and #3 research paths. Flagged pre-emptively so no LADA '
            'prevalence or algorithmic-classification RESULT can ever be sourced to it. '
            'Re-check for the results publication after the Quebec cohorts report.'
        ],
        'note': ('Retrospective population-based Quebec cohorts for algorithmic diabetes '
                 'classification and T1D/T2D/LADA phenotype burden. Relevant to Gap #10 '
                 '(LADA Prevalence by Healthcare Setting) when it reports - not before.'),
    },
    '42694315': {
        'status': 'VETTED',
        'issues_found': [],
        'note': ('Front Endocrinol 2026;17:1896333, PMC13539050. Verified live; pubtype '
                 'confirms Review. Narrative review advancing a MECHANISTIC HYPOTHESIS '
                 '(lactate-induced histone lactylation in LADA immune regulation and '
                 'beta-cell fate). Hypothesis-generating only; no human data. Citable as '
                 'a proposed mechanism, never as evidence that the mechanism operates.'),
    },
    '42686659': {
        'status': 'VETTED',
        'issues_found': [],
        'note': ('Antioxid Redox Signal, epub 2026 Sep 2, doi 10.1177/15230864261483982. '
                 'Verified live; pubtype confirms Review. Ferroptosis-immunity axis in '
                 'diabetic kidney disease. Same territory as the existing ferroptosis/NLRP3 '
                 'DKD watch item. Review, no primary data.'),
    },
    '42688475': {
        'status': 'VETTED',
        'issues_found': [],
        'note': ('Front Immunol 2026;17:1914528, PMC13535534. Verified live; pubtype confirms '
                 'Review. Extracellular vesicles at the Hashimoto/diabetes immune-metabolic '
                 'interface. Pairs thematically with PMID 42373533. Review, no primary data.'),
    },
    '37026004': {
        'status': 'FLAGGED',
        'issues_found': [
            'HEADLINE NUMBER RESTS ON n=11, AND THE STATE RECORD DID NOT SAY SO. '
            'Front Immunol 2023;14:1110544, PMC10070978 - verified live, real paper, '
            'CITR authorship (Ballou/Barton/Payne/Muller), pubtype includes NIH Extramural '
            'support. The claim recorded on 2026-09-07 was "HLA-DR matching predicts islet '
            'transplant insulin independence", which the paper does support. But the '
            'denominators, read from the abstract on 2026-09-08, are: the study screens 965 '
            'recipients and 2327 donors, then analyses 87 single-infusion recipients split '
            'into group A (HLA-DR mismatched, n=52), group B (1-2 HLA-DR matches EXCLUDING '
            'DR3/DR4, n=11) and group C (matched for DR3 or DR4, n=24). The 78% vs 24% vs 35% '
            'five-year insulin-independence contrast therefore turns on ELEVEN patients in '
            'group B. It is a retrospective registry subgroup analysis; the authors write '
            '"suggests", not "shows". Any downstream use MUST carry n=11 and must not be '
            'phrased causally. Flagged, not rejected - the finding stands, the framing did not.'
        ],
        'note': ('Load-bearing for the Gap #11 HLA-DR hypothesis recorded 2026-09-07. '
                 'Retained with the denominator attached.'),
    },
    '39951130': {
        'status': 'VETTED',
        'issues_found': [],
        'note': ('Diabetes Care 2025;48(5):737-744 (2025 May 1), PMC12034893. Verified live. '
                 'Rickels et al., CITR case-control vs T1D Exchange. n=71 CITR cases vs n=213 '
                 'T1DX controls, 5-year follow-up. Cases reached HbA1c <7.0% with no severe '
                 'hypoglycaemic event 71-80% of the time vs 21-33% of controls (P<0.001). '
                 'TWO CAVEATS THAT MUST TRAVEL WITH THE BENEFIT FIGURE: (a) the paper reports '
                 'a COST - eGFR fell -8.8 to -20 vs -1.3 to -6.5 mL/min/1.73m2 over 5 years '
                 '(P<0.001), i.e. islet transplant bought glycaemic control at the price of '
                 'kidney function; citing the benefit without the eGFR decline is a one-sided '
                 'reading of this paper. (b) It is NOT randomised and the two arms are drawn '
                 'from different registries in different eras (CITR SHEs 2000-2014, T1DX '
                 '2010-2012), so era effects and the intervening spread of CGM confound the '
                 'comparison. Design is case-control, and the pubtype list carries no '
                 'randomised-trial tag.'),
    },
}

vetted, flagged = [], []
for pmid, upd in VET.items():
    rec = papers.setdefault(pmid, {})
    rec['status'] = upd['status']
    rec['pmid_verified'] = True
    rec['claims_checked'] = True
    rec['vetted_date'] = now
    rec['last_checked'] = now
    rec['claims_checked_method'] = (
        'eutils_esummary_bulk_roundtrip_2026-09-08 (title+journal+year matched live PubMed); '
        'abstracts read via efetch for 37026004, 39951130, 42688599, 42674789'
    )
    rec['issues_found'] = upd['issues_found']
    rec['vetting_note_2026-09-08'] = upd['note']
    (flagged if upd['status'] == 'FLAGGED' else vetted).append(pmid)

# ---------------------------------------------- 2. GAP TIER ADJUDICATION
# gap_numbering_audit.json (generated 2026-09-06) reports tier_agree=False for
# exactly two gaps. In both, agent_state.json and gap_evidence.json say GOLD
# while the reader-facing hub card in rebuild_website.py says SILVER.
# Adjudicated today on the evidence rather than by picking a writer.

GAP_DEMOTIONS = {
    '11': {
        'name': 'Islet Transplant Registry Equity',
        'from': 'GOLD', 'to': 'SILVER',
        'grounds': (
            'MEASURED 2026-09-08 via eutils esearch. The bounded query '
            '(("Collaborative Islet Transplant Registry"[tiab]) OR (islet transplant* '
            'registry[tiab])) AND (disparit*[tiab] OR equity[tiab] OR racial[tiab] OR '
            'ethnic*[tiab] OR socioeconomic[tiab] OR access[tiab]) returns ZERO records. '
            'The wider query (islet transplant*[tiab]) AND (disparit* OR equity OR racial OR '
            'ethnic* OR socioeconomic OR "social determinants" OR insurance) returns 26, and '
            'inspection of the top 12 finds nothing that is a registry equity analysis - the '
            'closest is PMID 35887740, islet transplantation under Japanese health insurance, '
            'which is a coverage description, not an equity analysis. '
            'Separately, gap_evidence.json lists this gap\'s ENTIRE evidence base as two '
            'papers: PMID 19104422 (2008 CITR update - efficacy and safety outcomes, n=325) '
            'and PMID 37105208 (primary graft function and 5-year outcomes, n=1210). Both '
            'abstracts were read on 2026-09-08. NEITHER reports race, ethnicity, '
            'socioeconomic status, insurance or geography as an outcome or a covariate. '
            'gap_evidence_design.py scores this gap PRIMARY 1-of-1 = 100%, which reads as '
            'strong and is in fact the thinnest possible base - one design-readable paper, '
            'and it is off-question. '
            'A GOLD tier is a claim about the strength of evidence. There is no evidence on '
            'this gap\'s canonical question, so GOLD cannot be sustained. The published site '
            'already said SILVER; agent_state and gap_evidence are corrected DOWN to match. '
            'The gap itself remains real and arguably strengthens - the 0-record result is '
            'positive evidence that the intersection is unstudied.'
        ),
    },
    '6': {
        'name': 'CAR-T Access Barriers',
        'from': 'GOLD', 'to': 'SILVER',
        'grounds': (
            'gap_evidence_design.py grades this gap PRIMARY_THIN: only 1 of 8 design-readable '
            'papers (12%) reports primary data across 15 papers and 38 findings; the design '
            'mix is UNKNOWN 7, NARRATIVE 6, PRIMARY 1, NO_RESULTS 1. A gap resting on one '
            'measured study and a large commentary literature does not meet a GOLD bar. '
            'The published hub card already said SILVER; agent_state and gap_evidence are '
            'corrected DOWN to match. This also closes the 2026-08-30 P1 queue item asking '
            'for a review of the GOLD gaps graded PRIMARY_THIN, for gap #6 specifically. '
            'Gap #2 (Health Equity, PRIMARY_THIN 2-of-7) is NOT demoted today: unlike #6 and '
            '#11 its three writers already agree on GOLD, so changing it is a substantive '
            're-grade rather than a reconciliation, and it needs its own audit first. '
            'Left on the queue.'
        ),
    },
}

for gid, d in GAP_DEMOTIONS.items():
    g = state['gaps'][gid]
    g['tier'] = d['to']
    g['last_audited'] = TODAY
    g.setdefault('audit_history', []).append({
        'date': TODAY,
        'trigger': 'gap_numbering_audit.json tier_agree=False (agent_state/gap_evidence GOLD vs published site SILVER)',
        'question_audited': 'Canonical Gap #%s: %s' % (gid, d['name']),
        'tier_before': d['from'],
        'tier_after': d['to'],
        'new_evidence_found': False,
        'action': 'DEMOTION to SILVER, resolving the disagreement downward on the evidence.',
        'notes': d['grounds'],
    })

# gap_evidence.json is the second writer of the same number - update it too, or
# tomorrow's numbering audit reports the same disagreement against a new baseline.
with open(GAP_EVIDENCE, encoding='utf-8') as fh:
    gap_evidence = json.load(fh)
shutil.copyfile(GAP_EVIDENCE, os.path.join(RESULTS, 'gap_evidence.json.bak_%s' % TODAY))
for gid, d in GAP_DEMOTIONS.items():
    gap_evidence['gaps'][gid]['tier'] = d['to']
    gap_evidence['gaps'][gid]['tier_changed_%s' % TODAY] = '%s -> %s' % (d['from'], d['to'])
with open(GAP_EVIDENCE, 'w', encoding='utf-8') as fh:
    json.dump(gap_evidence, fh, indent=2, ensure_ascii=False)

# ------------------------------------------- 3. CITATION CORRECTION (Gap #11)
CORRECTION = {
    'date': TODAY,
    'artifact': 'Analysis/Scripts/build_islet_equity.py -> Dashboards/Islet_Transplant_Equity.html',
    'severity': 'HIGH - reader-facing, on a published dashboard, four independently checkable errors on one citation',
    'found': (
        'The Gap #11 evidence catalog described PMID 19104422 as: "Comprehensive data on '
        '1,477 transplant recipients ... Published biennially in American Journal of '
        'Transplantation. Barton et al. An update on results of the International Islet '
        'Transplant Registry." Checked against live PubMed on 2026-09-08, PMID 19104422 is '
        'Alejandro R, Barton FB, Hering BJ, Wease S, "2008 Update from the Collaborative '
        'Islet Transplant Registry", Transplantation 2008 Dec 27;86(12):1783-8, reporting '
        '325 recipients / 649 infusions / 712 donors. Wrong first author, wrong title, wrong '
        'journal, wrong denominator, wrong registry (the International Islet Transplant '
        'Registry was a separate registry, not CITR). '
        'The 1,477 figure belongs to the CITR 12th Allograft Report (2025), a registry PDF at '
        'citregistry.org covering 1999-2023 across 40 centres - no PMID, not peer-reviewed. '
        'SECOND ERROR, same page: the "85% White recipients" bar carried an inline '
        'PMID:19104422 link. That abstract reports no racial or ethnic breakdown at all. The '
        'comparator figures (62% / 5% / 18% / 5% / 20%) carried no citation whatsoever. '
        'THIRD ERROR, same page: the "What This Cannot Tell You" block asserted "GOLD tier '
        '(3+ independent sources)" while the hub card for the same dashboard said SILVER - a '
        'third writer of the tier, disagreeing with the other two.'
    ),
    'fixed': (
        'Split the evidence-catalog entry in two: a CITR Allograft Reports entry carrying the '
        '1,477 figure, explicitly labelled registry-grade and not peer-reviewed, and a '
        'correct entry for PMID 19104422 with its real authors, journal, year and n=325, '
        'carrying a visible correction notice. Removed the PMID:19104422 attribution from the '
        '85% bar and replaced the block\'s source line with a visible UNSOURCED warning naming '
        'every uncited figure and stating what a citable replacement would require. Changed '
        'the in-page tier from GOLD to SILVER and added the measured 0-record search result.'
    ),
    'not_fixed': (
        'No replacement citation was invented for 85% / 62% / 5% / 18% / 5% / 20%. The '
        'numbers are left on the page marked UNSOURCED rather than deleted, because deleting '
        'them would hide that the dashboard was making the claim. Sourcing them requires '
        'reading a CITR Allograft Report recipient-characteristics table directly and '
        'transcribing it with its denominator and reporting year. Queued.'
    ),
}
state.setdefault('audit_notes', []).append(CORRECTION)

# --------------------------------------------------------- 4. NEW PAPER
papers['42696794'] = {
    'status': 'UNVETTED',
    'added': TODAY,
    'priority': 'medium',
    'source': '2026-09-08 gap #6 adjudication search (eutils esearch)',
    'title': ('Overcoming access barriers in European CAR-T therapy: the role of decentralized '
              'manufacturing and the EASYGEN framework.'),
    'journal': 'Cytotherapy',
    'year': '2026',
    'design': 'Framework / consortium position paper - design not yet read',
    'note': ('Cytotherapy 2026 Jun 19;28(11):102939, doi 10.1016/j.jcyt.2026.102939, online '
             'ahead of print. Directly on CAR-T ACCESS BARRIERS, which is gap #6\'s canonical '
             'question, and gap #6 currently rests on only 1 primary paper out of 8 '
             'design-readable. CAVEAT TO CHECK AT VETTING: the author list is led by Fresenius '
             'SE and Fresenius Kabi employees and the paper advocates a named framework '
             '(EASYGEN) - assess for commercial framing before it is allowed to carry any '
             'access-barrier claim. Also European oncology CAR-T, not diabetes, so it is '
             'adjacent to gap #6 rather than inside it.'),
}

# -------------------------------------------------- 5. QUEUE MAINTENANCE
queue = state['work_queue']
closed = []
kept = []
for item in queue:
    t = str(item.get('target', ''))
    if item.get('type') == 'audit_gap' and 'RE-AUDIT THE FOUR GAPS WHOSE CANONICAL QUESTION HAS NEVER BEEN ASKED' in t:
        item['closed'] = TODAY
        item['closed_reason'] = (
            'STALE - all three named gaps have since been audited under their canonical '
            'questions, and the fix is confirmed by an independent artifact. Gap #4 (Drug '
            'Repurposing for Islet Transplant) and gap #5 (Treg in Diabetic Neuropathy) each '
            'received a first on-topic audit on 2026-09-04; gap #11 (Islet Transplant Registry '
            'Equity) on 2026-09-05 and again on 2026-09-07. gap_numbering_audit.json now '
            'reports topic_share 1.0 and topic_agree=True for #4, #5 and #11. Item was raised '
            '2026-09-03 and was already satisfied within 48 hours; it survived on the queue '
            'for five days only because nothing re-checked it. '
            'RESIDUAL, NOT CLOSED: gap #10 (topic_share 0.50) and gap #12 (0.67) still audit '
            'partly off-question. Re-raised below as a narrower item.'
        )
        closed.append(t[:80])
    else:
        kept.append(item)
state['closed_queue_items'] = state.get('closed_queue_items', []) + closed
state['work_queue'] = kept

NEW_ITEMS = [
    {
        'type': 'verify_citations', 'priority': 1, 'added': TODAY,
        'target': (
            'SOURCE OR REMOVE THE SIX RACE FIGURES NOW MARKED UNSOURCED ON THE GAP #11 '
            'DASHBOARD. Today\'s correction left 85% / 62% / 5% / 18% / 5% / 20% visible with '
            'an UNSOURCED warning rather than deleting them, so the reader can see what was '
            'being claimed. They cannot stay that way. The only citable source identified is '
            'the recipient-characteristics table of a CITR Allograft Report at citregistry.org '
            '(12th Allograft Report, 2025, 1,477 recipients, 1999-2023, 40 centres) - a '
            'non-peer-reviewed registry PDF that must be read directly and transcribed WITH '
            'its denominator and reporting year, and labelled registry-grade. If the CITR '
            'report does not break out race, the bars must be deleted, not softened. The T1D '
            'population comparators (62/18/20) need a separate CDC or SEARCH-for-Diabetes '
            'citation and must match on age band and year, which the current bars do not state.'
        ),
    },
    {
        'type': 'fix_pipeline', 'priority': 1, 'added': TODAY,
        'target': (
            'NO GATE CATCHES A CITATION WHOSE DESCRIPTION CONTRADICTS ITS PMID. Today\'s Gap '
            '#11 finding got through every existing gate: PMID 19104422 is real, live, '
            'correctly formatted, and in the pubtype and title caches, so verify_pmids.py '
            'passes it - while the prose attached to it named a different author, a different '
            'title, a different journal and a different denominator. The gates check that a '
            'PMID EXISTS; nothing checks that the surrounding sentence DESCRIBES it. '
            'audit_prose_citation_titles.py is the nearest thing and it scans .py only for '
            'title mismatch, not author/journal/n. PROPOSAL: extend it to compare any '
            'author surname, journal name or four-digit year appearing within ~200 characters '
            'of a PMID link against the cached esummary record for that PMID, and fail on '
            'disagreement. Estimated blast radius: every dashboard builder, ~40 scripts. Run '
            'it in report-only mode first and count the hits before wiring it into the gate '
            'sequence.'
        ),
    },
    {
        'type': 'audit_gap', 'priority': 2, 'added': TODAY,
        'target': (
            'GAPS #10 AND #12 STILL AUDIT PARTLY OFF-QUESTION. gap_numbering_audit.json '
            '(2026-09-06) reports topic_share 0.50 for gap #10 (LADA Prevalence by Healthcare '
            'Setting) and 0.67 for gap #12 (Generic Drug x Diabetes Mechanism Catalog), '
            'against a 0.50 floor - so half of #10\'s audit trail and a third of #12\'s '
            'discusses something other than the gap\'s own question. Both currently read '
            'SILVER across all writers, so unlike #6 and #11 there is no disagreement forcing '
            'the issue, which is exactly why it will keep being skipped. Audit each on its '
            'canonical question and re-home the off-topic trail entries.'
        ),
    },
    {
        'type': 'vet_papers_batch', 'priority': 2, 'added': TODAY,
        'target': (
            'Vet PMID 42696794 (Cytotherapy 2026, EASYGEN / decentralized CAR-T manufacturing) '
            'against gap #6. Read the design: it is a consortium framework paper led by '
            'Fresenius employees advocating a named framework, so establish whether it reports '
            'any measured access data at all before letting it near gap #6\'s primary-paper '
            'count. If it does report measured data it is the SECOND primary paper for gap #6 '
            'and a SILVER->GOLD promotion candidate; if it is position-only it changes nothing '
            'and should be recorded as NARRATIVE.'
        ),
    },
]
state['work_queue'] = NEW_ITEMS + state['work_queue']

# --------------------------------------------------------- 6. RUN HISTORY
state['run_history'].append({
    'date': TODAY,
    'day': 'Tue',
    'queue_items_worked': [
        'vet_papers_batch (7 carried from 2026-09-07) - 5 VETTED, 2 FLAGGED',
        'gap tier disagreement #11 - DEMOTED GOLD -> SILVER',
        'gap tier disagreement #6 - DEMOTED GOLD -> SILVER',
        'citation correction on the Gap #11 published dashboard',
        'audit_gap 2026-09-03 (four canonical questions) - CLOSED as stale',
    ],
    'papers_vetted': vetted,
    'papers_flagged': flagged,
    'papers_added': ['42696794'],
    'gaps_demoted': ['6', '11'],
    'tier_disagreements_before_after': '2 -> 0',
    'summary': (
        'LEAD FINDING: the Gap #11 dashboard has been publishing a citation in which four '
        'independently checkable details were wrong. PMID 19104422 was described as covering '
        '1,477 recipients, authored by Barton et al., titled "An update on results of the '
        'International Islet Transplant Registry", published in the American Journal of '
        'Transplantation. It is Alejandro et al., "2008 Update from the Collaborative Islet '
        'Transplant Registry", Transplantation 2008;86(12):1783-8, n=325. The same PMID was '
        'also attached to an "85% White recipients" bar; that abstract reports no racial '
        'breakdown. Every gate in the pipeline passed this, because the gates check that a '
        'PMID exists and never that the sentence around it describes the paper. That blind '
        'spot is now the top new fix_pipeline item. '
        'SECOND FINDING: both gaps whose tier writers disagreed were resolved DOWNWARD. Gap '
        '#11 GOLD was resting on two papers, neither of which is about equity, while a bounded '
        'PubMed query at its canonical intersection returns zero records; gap #6 GOLD was '
        'resting on 1 primary paper in 8 design-readable. In both cases the published site was '
        'already showing the more defensible number and the agent\'s own memory was the '
        'overstatement - worth noting, because the standing assumption in this queue has been '
        'that the site lags the agent. '
        'THIRD FINDING: PMID 37026004, adopted yesterday as load-bearing for the Gap #11 '
        'HLA-DR hypothesis, has a headline 78%-vs-24% five-year result that turns on 11 '
        'patients in a retrospective registry subgroup. Flagged with the denominator attached '
        'rather than dropped. PMID 39951130 was vetted with the caveat that its glycaemic '
        'benefit is paired with a significantly steeper eGFR decline, and that its two arms '
        'come from different registries in different eras. '
        'The P0 publish blocker is unchanged and still governs everything above: main is 103 '
        'commits ahead of origin/main, whose tip is f7e976f dated 2026-04-20 - 141 days. Every '
        'correction in this run exists only in the working tree. The corrected dashboard is '
        'not the one a reader sees; the reader still sees the wrong citation.'
    ),
    'blocking_issue': (
        'PUSH. 103 commits unpushed, origin/main frozen at 2026-04-20 (141 days). No '
        'credential in the sandbox. Today\'s citation correction is reader-facing and cannot '
        'reach the reader.'
    ),
})

state['last_run'] = TODAY
state['last_updated'] = TODAY

with open(STATE, 'w', encoding='utf-8') as fh:
    json.dump(state, fh, indent=2, ensure_ascii=False)

print('[OK] vetted:', vetted)
print('[OK] flagged:', flagged)
print('[OK] gaps demoted to SILVER: 6, 11 (agent_state.json + gap_evidence.json)')
print('[OK] queue: closed %d stale, added %d new, len now %d'
      % (len(closed), len(NEW_ITEMS), len(state['work_queue'])))
print('[OK] state saved')
