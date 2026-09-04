#!/usr/bin/env python3
"""Close out the 2026-09-04 daily iteration: record findings, requeue, save state.

Run once. Idempotent guard: refuses if run_history already carries 2026-09-04.
"""
import json
import os
import shutil
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(BASE, 'Results', 'agent_state.json')
TODAY = '2026-09-04'


def main():
    with open(STATE, encoding='utf-8') as fh:
        s = json.load(fh)

    if any(r.get('date') == TODAY for r in s.get('run_history', [])):
        print('[SKIP] %s already recorded.' % TODAY)
        return 0

    shutil.copy2(STATE, STATE + '.bak_' + TODAY)

    # ------------------------------------------------------------------ gaps
    audits = {
        '5': {
            'date': TODAY,
            'new_evidence_found': False,
            'notes': (
                'FIRST ON-TOPIC AUDIT OF THIS GAP. audit_gap_numbering.py reports '
                'gap #5 (Treg in Diabetic Neuropathy) at 0% topic overlap across all '
                '5 prior audits - the trail discusses drug repurposing for islet '
                'transplant, which is gap #4. Its SILVER tier has therefore never '
                'rested on evidence about its own question. Audited the real question '
                'today. BOUNDED QUERY: PubMed (regulatory T cell*[tiab] OR Treg*[tiab]) '
                'AND (diabetic neuropathy[tiab] OR diabetic peripheral neuropathy[tiab]) '
                'returns 6 records TOTAL, all time. None reports a Treg-directed '
                'intervention in diabetic neuropathy. Most recent is PMID 41958676 '
                '(Front Immunol 2026;17:1763798), a narrative review of Treg in diabetes '
                'and traditional Chinese medicine whose abstract enumerates nephropathy '
                'and vasculopathy, not neuropathy. Two others (40161211, 39976904) are '
                'Mendelian randomisation on neuropathic pain generally, not diabetic '
                'neuropathy specifically. REMAINS SILVER: the absence is now measured '
                'rather than assumed, but no second independent source evaluates the '
                'intersection, which is what promotion requires.')
        },
        '4': {
            'date': TODAY,
            'new_evidence_found': True,
            'notes': (
                'FIRST ON-TOPIC AUDIT OF THIS GAP (same 0%-overlap finding as #5; the '
                'trail here discusses personalised nutrition for islet-transplant graft '
                'outcomes). BOUNDED QUERY: (drug repurpos*[tiab] OR repurposed drug*[tiab] '
                'OR drug screen*[tiab]) AND (islet transplant*[tiab] OR islet graft*[tiab]) '
                'returns 8 records, 7 of which are bioengineering/organoid reviews matching '
                'on "drug screen" as a use-case for islet models, NOT screens of drugs for '
                'graft outcomes. The one substantive hit is PMID 27821710 (J Pharmacol Exp '
                'Ther 2016), an alpha-1 antitrypsin dosing study - a single repurposed '
                'agent, not a screen. ADJACENT COUNTER-EVIDENCE, AND A TRAP AVOIDED: web '
                'search surfaced PMID 39911401 (Front Immunol 2025;16:1539645) as a '
                'Connectivity Map repurposing screen identifying rosiglitazone, synergistic '
                'with rapamycin, "prolonging graft survival" - which reads like closure. '
                'Read the paper: the expression data are kidney/heart/lung biopsies and the '
                'in vivo validation is a MOUSE SKIN transplant model. No islet anywhere. '
                'REMAINS SILVER, and the finding STRENGTHENS rather than weakens it: the '
                'method now demonstrably exists and has still not been pointed at islets.')
        },
        '2': {
            'date': TODAY,
            'new_evidence_found': True,
            'notes': (
                'SECOND COMPLETED EQUITY RCT IN THREE WEEKS - the premise of this GOLD tier '
                'is now falsified twice. PMID 42478360 (Circulation 2026 Aug 18;154(7):624-635; '
                'NCT05407376): medically tailored groceries vs usual care in 460 Medicaid-insured '
                'adults with T2D (85.2% Hispanic, 58% food-insecure, baseline HbA1c 9.40). '
                'HbA1c treatment difference -0.40 points (95% CI -0.73 to -0.08; P=0.016); '
                'food security OR 2.12 (1.13-3.99), nutrition security OR 3.65 (1.84-7.25); '
                'hypertension and BMI unchanged. This follows PMID 41587834 (Ann Fam Med 2026, '
                'n=186, 0.7 pp) found on 2026-08-16. TWO independent completed equity-focused '
                'RCTs with concordant direction and a ~1.75x disagreement in magnitude. '
                'WHAT REMAINS OPEN is narrower than what the GOLD tier currently asserts: both '
                'are 6-month, single-country, surrogate-endpoint (HbA1c) trials with no hard '
                'outcomes and no durability data. RECOMMENDATION, REPORTED NOT APPLIED: the gap '
                'statement should be re-scoped from "no completed equity RCT" to "no equity RCT '
                'with hard outcomes or durability beyond 6 months", and the tier reconsidered '
                'against the re-scoped statement. Re-tiering a published GOLD gap is a human call.')
        },
        '1': {
            'date': TODAY,
            'new_evidence_found': False,
            'notes': (
                'Bounded falsification test, cleanest result in the gap set: PubMed '
                '(gene therapy[tiab] OR CRISPR[tiab] OR gene editing[tiab]) AND (LADA[tiab] '
                'OR latent autoimmune diabetes[tiab]) returns ZERO records, all time. '
                'Consistent with the 2026-08-16 audit, which found only T1D-scoped CRISPR '
                'work (Lin et al., Diabetes Obes Metab 2026, doi 10.1111/dom.70800) where '
                'LADA appears as conceptual extension. REMAINS SILVER, not a promotion '
                'candidate: an empty query is evidence of absence in the indexed literature, '
                'not an independent secondary source evaluating feasibility in LADA.')
        },
        '6': {
            'date': TODAY,
            'new_evidence_found': False,
            'notes': (
                'Monthly audit. The 2026 CAR-T-in-autoimmunity literature is active but none '
                'of it addresses ACCESS, which is what this gap is about. Screened 8 most '
                'recent: PMID 42561661 (Int Immunopharmacol 2026, review, immune resetting), '
                '42431595 (Autoimmun Rev 2026, TCR-Treg), 42409472 (Adv Pharmacol 2026, '
                'transient T cell therapies). A SECOND TRAP AVOIDED: PMID 42486100 (Med 2026 '
                'Aug 14;7(8):101226) is a Phase I of low-dose cord-blood CD19 CAR-NK cells '
                'motivated explicitly by CAR-T cost and manufacturing burden - i.e. it reads '
                'as access counter-evidence - but the indication is refractory SLE, not '
                'diabetes. Logged as adjacent watch, NOT as corpus evidence. NO TIER CHANGE '
                'APPLIED, and note the standing disagreement: agent_state and gap_evidence '
                'say GOLD, the published site says SILVER (audit_gap_numbering.py, still open '
                'as a human call).')
        },
    }
    for gid, entry in audits.items():
        g = s['gaps'][gid]
        g.setdefault('audit_history', []).append(entry)
        g['last_audited'] = TODAY

    # ------------------------------------------------------------ audit notes
    s.setdefault('audit_notes', []).append({
        'date': TODAY,
        'title': ('The site advertised 41 links it could not serve, and the publish '
                  'step was what broke 34 of them'),
        'detail': (
            'audit_published_links.py (new today) resolved every relative href/src in '
            'docs/**.html against the filesystem: 1359 resolved, 41 did not. '
            'THE BULK IS ONE DEFECT. postprocess_dashboards.py inserts a "<- Hub" '
            'back-link as href="../docs/index.html", which is correct at Dashboards/X.html '
            'and wrong at docs/Dashboards/X.html, where it resolves to docs/docs/index.html. '
            'All 34 published dashboards carried it. THE REASON IT SURVIVED SINCE 2026-08-16 '
            'IS THE VERIFICATION ITSELF: sync_docs_dashboards.py verified byte equality '
            'between source and published copy, and byte equality is exactly what guarantees '
            'this defect - a depth-relative link MUST differ between depths for both to work. '
            'A copy step that verifies sameness cannot detect a defect whose fix is difference. '
            'Also found: three hand-written nav links (build_drug_repurposing_screen "Home", '
            'build_lada_diagnostic_model "<- Back to Index", build_trial_equity_mapper '
            '"<- Dashboard Home") pointing at a docs/Dashboards/index.html that has never '
            'existed, one build_corpus_analysis href="/" pointing at the Pages DOMAIN root '
            'rather than this project, and the two hub report cards below. '
            'FIXED: the four builders now emit the repo-root form; sync_docs_dashboards.py '
            'declares a PUBLISH_REWRITES table, applies it on copy and verifies against the '
            'transformed text; audit_published_links.py is wired as the last pipeline stage. '
            '41 -> 0.')
    })
    s['audit_notes'].append({
        'date': TODAY,
        'title': ('Two reports were advertised as "Available" on the hub and have '
                  'never been servable'),
        'detail': (
            'docs/index.html carries two cards with status "live"/"Available": Literature '
            'Gap Analysis -> Analysis/Results/literature_gap_report.md and Publication '
            'Monitor -> Analysis/Results/pubmed_recent_summary.md. docs/ is the Pages '
            'publish root, so both hrefs resolve to docs/Analysis/Results/..., which has '
            'never existed. sync_docs_dashboards.py copies *.html only, so no publisher '
            'ever looked at them. This answers the 2026-08-31 queue item, which asked '
            'whether the blanket exclusion of Analysis/Results/*.md was "still true, since '
            'some are linked from dashboards": it was not true, for exactly 2 of 257 files. '
            'FIXED: sync_docs_reports.py derives its scope from the hub rather than a hard '
            'list, publishes to docs/Reports/, and rebuild_website.py now links there; '
            'audit_markdown_citations.py picks the same two files up by the same derivation '
            '(both carry zero PMIDs today, which is a fact about today, not a reason to '
            'leave them ungated). '
            'A SECOND DEFECT SHIPPED WITH THE FIX AND HAD TO BE DISCLOSED: '
            'pubmed_recent_summary.md is titled "Recent Publications" with a declared '
            '30-day lookback and was generated 2026-07-17 - 49 days stale. Repairing the '
            'link without saying so would replace a 404 with a page that silently misleads, '
            'so each published copy now carries a provenance banner naming its source path '
            'and declared generation date. THE UNDERLYING STALENESS IS NOT FIXED and is '
            'queued: a "rolling 30-day snapshot" that is 49 days old is a live claim the '
            'pipeline is not refreshing.')
    })
    s['audit_notes'].append({
        'date': TODAY,
        'title': 'Two gaps had never been audited on their own question; both survive it',
        'detail': (
            'Gaps #4 (Drug Repurposing for Islet Transplant) and #5 (Treg in Diabetic '
            'Neuropathy) carry 0% topic overlap across all 5 prior audits each - their '
            'trails are each other\'s and a third topic\'s. Their SILVER tiers had never '
            'rested on evidence about their own questions. Both audited on-topic today '
            'with bounded PubMed queries and both hold. Notably BOTH on-topic audits '
            'surfaced a near-miss that a looser reading would have logged as gap closure: '
            'PMID 39911401 is a genuine repurposing screen validated in mouse SKIN grafts, '
            'not islets, and PMID 42486100 is a cost-motivated CAR-NK Phase I in SLE, not '
            'diabetes. The gap set\'s exposure is not that audits find nothing - it is that '
            'an audit reading only search-result summaries would have closed two gaps today '
            'on papers about the wrong tissue and the wrong disease.')
    })

    # -------------------------------------------------------------- run entry
    s.setdefault('run_history', []).append({
        'date': TODAY,
        'day': 'Fri',
        'queue_items_worked': [
            'audit_gap #6', 'audit_gap #5', 'audit_gap #4', 'audit_gap #1', 'audit_gap #2',
            'fix_pipeline 2026-08-31 (remaining generated markdown)',
        ],
        'gaps_audited': ['1', '2', '4', '5', '6'],
        'gate_status': '67/67 [OK] including new syncreports and linkgate stages',
        'new_scripts': ['audit_published_links.py', 'sync_docs_reports.py'],
        'published_links_before_after': '41 dead / 1359 live -> 0 dead / 1400 live',
        'summary': (
            'Fri 2026-09-04 - THE PUBLISH STEP WAS BREAKING 34 LINKS AND ITS VERIFICATION '
            'GUARANTEED IT, AND TWO GAPS HAD NEVER BEEN AUDITED ON THEIR OWN QUESTION. '
            '(1) 41 of 1400 links on the published site were dead. 34 were the "<- Hub" '
            'back-link on every dashboard, created BY sync_docs_dashboards.py, which '
            'verified byte equality with the source - and byte equality is precisely what '
            'makes a depth-relative link wrong at a different depth. A copy step whose '
            'success condition is sameness cannot see a defect whose fix is difference. '
            'Fixed at the four builders plus a declared PUBLISH_REWRITES table, and '
            'audit_published_links.py now runs last. 41 -> 0. '
            '(2) The two markdown reports the hub advertises as "Available" have never '
            'been servable and were outside every citation gate - answering the 2026-08-31 '
            'item, which suspected exactly this. Now published via sync_docs_reports.py '
            'with scope derived from the hub, and gated. One of them declares a rolling '
            '30-day lookback and is 49 days old; disclosed on the page, queued for repair. '
            '(3) Gaps #4 and #5 were audited on their real questions for the first time '
            '(0% topic overlap in all 10 prior audits between them). Both hold. Both '
            'near-missed a false closure: a skin-graft repurposing screen and an SLE '
            'CAR-NK trial, either of which a summary-level read would have banked. '
            '(4) Gap #2 GOLD is now falsified twice on its stated premise - PMID 42478360 '
            '(Circulation 2026, n=460, HbA1c -0.40 pp, 95% CI -0.73 to -0.08) joins PMID '
            '41587834 from 2026-08-16. Recommended re-scope reported, not applied.')
    })

    # ------------------------------------------------------------- work queue
    s['work_queue'].append({
        'priority': 1,
        'type': 'fix_pipeline',
        'added': TODAY,
        'target': (
            'THE PUBLICATION MONITOR IS 49 DAYS STALE AND SAYS "ROLLING 30-DAY SNAPSHOT". '
            'pubmed_recent_summary.md declares Generated: 2026-07-17 and a 30-day lookback; '
            'the hub card calls it a "Rolling 30-day PubMed snapshot" with status '
            '"Available". Today made it reachable for the first time and added a provenance '
            'banner so the age is visible, which is disclosure, not repair. Find why the '
            'daily pipeline does not regenerate it - baseline_pubmed_alerts.py and '
            'hub_monitor.py both write in this area and neither is in '
            'run_quality_improvements.py STAGES - then either wire the generator in or '
            'change the card to say what the file actually is. The same question applies to '
            'literature_gap_report.md, which regenerates (2026-09-03) and is therefore fine. '
            'A "live" badge over a 49-day-old rolling window is the badge defect of '
            '2026-08-23 in a new place.')
    })
    s['work_queue'].append({
        'priority': 2,
        'type': 'analysis',
        'added': TODAY,
        'target': (
            'GENERALISE THE BYTE-EQUALITY LESSON TO EVERY COPY STEP. sync_docs_dashboards.py '
            'verified that the published copy was IDENTICAL to the source, which is the wrong '
            'invariant whenever the two live at different depths or under different roots - '
            'and it is why 34 dead links passed a green gate for 19 days. Audit the other '
            'copy/publish paths for the same wrong invariant: postprocess_dashboards.py '
            '(rewrites in place), add_citations.py (holds the real text of '
            'Research_Findings_Summary.md), and any script using shutil.copy into docs/. '
            'The rule to enforce: a publish step must verify the PUBLISHED form, computed '
            'from a declared transform, not the source form.')
    })
    s['work_queue'].append({
        'priority': 2,
        'type': 'audit_gap',
        'added': TODAY,
        'target': (
            'RE-SCOPE GAP #2 BEFORE RE-TIERING IT. Two completed equity RCTs now exist '
            '(41587834 n=186 0.7 pp; 42478360 n=460 -0.40 pp, Circulation 2026, NCT05407376) '
            'and the gap statement that justified GOLD - absence of completed equity-focused '
            'trials - is false. What is still absent is narrower and worth stating exactly: '
            'hard outcomes, durability beyond 6 months, and replication outside the US. '
            'Rewrite the gap statement to that, THEN ask what tier the rewritten statement '
            'earns. Re-tiering the old statement is answering a question nobody should still '
            'be asking. Human call on the tier itself; the re-scope is a research judgement '
            'that should be made explicit either way.')
    })
    s['work_queue'].append({
        'priority': 2,
        'type': 'analysis',
        'added': TODAY,
        'target': (
            'THE GAP AUDITS ARE ONE SUMMARY-LEVEL READ AWAY FROM FALSE CLOSURES, AND TODAY '
            'PRODUCED TWO EXAMPLES IN ONE RUN. PMID 39911401 reads as "drug repurposing screen '
            'prolongs graft survival" in every search summary and is a mouse SKIN transplant; '
            'PMID 42486100 reads as "CAR therapy motivated by cost and manufacturing burden" '
            'and is refractory SLE. Both would have closed a gap if logged from the summary. '
            'Propose a standing audit rule with teeth: no gap audit may record new_evidence_found '
            'or change a tier on a paper whose TISSUE/MODEL and INDICATION have not been read '
            'from the abstract itself, and record those two fields alongside the PMID in the '
            'audit entry so the check is visible afterwards. Cheap, and it targets the exact '
            'failure mode.')
    })
    s['work_queue'].append({
        'priority': 3,
        'type': 'audit_gap',
        'added': TODAY,
        'target': (
            'GAPS #4 AND #5 NOW EACH HAVE EXACTLY ONE ON-TOPIC AUDIT (2026-09-04) UNDER FIVE '
            'OFF-TOPIC ONES. The misfiled-trail annotation does not clear by adding an on-topic '
            'audit - audit_gap_numbering.py says so explicitly - but the tier decision now has '
            'a real basis for the first time. When the human call on re-homing the historical '
            'trails is made, re-run both audits so each gap has two independent on-topic reads '
            'before any promotion is considered. Same applies to #7, #11, #12, #15, which carry '
            'the annotation and have NOT yet had an on-topic audit.')
    })

    s['last_updated'] = TODAY
    s['last_run'] = TODAY

    with open(STATE, 'w', encoding='utf-8') as fh:
        json.dump(s, fh, indent=2)

    print('[OK] state updated for %s' % TODAY)
    print('  gaps audited      : %s' % ', '.join(sorted(audits)))
    print('  audit notes added : 3')
    print('  queue items added : 5')
    print('  run_history       : %d entries' % len(s['run_history']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
