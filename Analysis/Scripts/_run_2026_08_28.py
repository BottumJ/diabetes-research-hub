#!/usr/bin/env python3
"""Close-out for the 2026-08-28 run: record what was decided, not just what ran.

Three things are written here:
  1. The 11 UNSCREENED_ORPHAN papers, adjudicated one at a time.
  2. The verapamil path validation, which finally has an external anchor.
  3. The evidence-design tiers, folded back onto the paths themselves.
"""

import json
import os
import shutil
from datetime import date

RESULTS = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'Results'))
STATE = os.path.join(RESULTS, 'agent_state.json')
TODAY = '2026-08-28'

# ---------------------------------------------------------------------------
# 1. The 11 orphans. Every title, journal, year and publication type below was
#    read from a live NCBI esummary call on 2026-08-28, not from memory.
# ---------------------------------------------------------------------------
ORPHANS = {
    '30291106': dict(
        title='Management of Hyperglycemia in Type 2 Diabetes, 2018. A Consensus Report by the ADA and the EASD',
        journal='Diabetes Care', year='2018', pubtype='Consensus Statement',
        disposition='IN_CORPUS', tier='GUIDELINE',
        why='On topic and authoritative, but a consensus report states recommendations, not measured outcomes. Citable as standard of care; must not supply data points.'),
    '39173844': dict(
        title='Compromised chronic efficacy of a glucokinase activator AZD1656 in mouse models for common human GCKR variants',
        journal='Biochem Pharmacol', year='2024', pubtype='Journal Article',
        disposition='IN_CORPUS', tier='PRECLINICAL_ONLY',
        why='Directly relevant to the GKA arm (Gap 7/9) and a genuinely useful NEGATIVE result - efficacy compromised, not confirmed. Mouse models; no human data.'),
    '39412512': dict(
        title='SGLT2 inhibitors and NLRP3 inflammasome: potential target in diabetic kidney disease',
        journal='J Bras Nefrol', year='2024', pubtype='Review',
        disposition='IN_CORPUS', tier='NARRATIVE_REVIEW',
        why='Already cited by the dapagliflozin paths. Narrative review: its numbers are second-hand and must not be extracted as findings.'),
    '39428507': dict(
        title='MOG-specific CAR Tregs: a novel approach to treat multiple sclerosis',
        journal='J Neuroinflammation', year='2024', pubtype='Journal Article',
        disposition='BACKGROUND', tier='METHODOLOGY',
        why='CAR-Treg engineering, but the disease is multiple sclerosis. Citable as CAR-Treg methodology for the Gap 6 access arm; contains no diabetes outcome and must not count as corpus evidence.'),
    '39613428': dict(
        title='Investigating the effect of verapamil on preservation of beta-cell function in adults with newly diagnosed type 1 diabetes mellitus (Ver-A-T1D): protocol for a randomised controlled trial',
        journal='BMJ Open', year='2024', pubtype='Clinical Trial Protocol',
        disposition='IN_CORPUS', tier='PROTOCOL_NO_RESULTS',
        why='A PROTOCOL. It reports design, dose and endpoints - no outcome. It is currently the sole corpus support for the #4 and #5 ranked paths, which is the open P1 human call; indexing it correctly does not resolve that call, it makes the situation legible.'),
    '40598585': dict(
        title='A systematic review and network meta-analysis of interventions to preserve insulin-secreting beta cell function in people newly diagnosed with type 1 diabetes: results from randomised controlled trials of immunomodulatory therapies',
        journal='BMC Med', year='2025', pubtype='Systematic Review, Network Meta-Analysis',
        disposition='IN_CORPUS', tier='SYNTHESIS_HIGH',
        why='The strongest single paper in this batch: 60 trials, 4597 patients, 32 intervention classes. 11 of 42 interventions beat placebo on 12-month C-peptide (I2=66%). SCOPE MATTERS: it covers IMMUNOTHERAPIES only, so verapamil was never eligible - its absence from the 11 is not evidence against verapamil and must not be read as such.'),
    '40988828': dict(
        title='Vitamin D Supplementation in Deficiency States and Combined Calcium-Vitamin D Therapy in Diabetes Prevention and Management: A Systematic Review of Clinical Evidence',
        journal='Cureus', year='2025', pubtype='Review',
        disposition='IN_CORPUS', tier='NARRATIVE_REVIEW',
        why='Already the sole support for vitamin_d -> autoimmune. Cureus applies limited peer review; the path is graded NARRATIVE_ONLY today and that grade should be visible wherever it ranks.'),
    '41618067': dict(
        title='Artificial Intelligence-Based Medical Devices for Diabetic Retinopathy Screening in the European Union',
        journal='Ophthalmol Ther', year='2026', pubtype='Review',
        disposition='IN_CORPUS', tier='NARRATIVE_REVIEW',
        why='On topic for the access/equity arm (screening device availability), not for any mechanism path. Regulatory landscape review.'),
    '41935855': dict(
        title='Subclinical carotid atherosclerosis in latent autoimmune diabetes in adults and type 2 diabetes mellitus: a cross-sectional study',
        journal='Nutr Metab Cardiovasc Dis', year='2026', pubtype='Comparative Study',
        disposition='IN_CORPUS', tier='OBSERVATIONAL_PRIMARY',
        why='Primary human LADA data with a T2D comparator - directly relevant to Gap 1. Cross-sectional, so associational only.'),
    '41986815': dict(
        title='Multi-tissue multi-omics integration reveals tissue-specific pathways, gene networks and drug candidates for type 1 diabetes',
        journal='Diabetologia', year='2026', pubtype='Journal Article',
        disposition='IN_CORPUS', tier='COMPUTATIONAL',
        why='Drug-candidate generation for T1D from multi-omics. Hypothesis-generating: candidates are predicted, not tested, and must never be reported as demonstrated effects.'),
    '41994768': dict(
        title='Sodium-Glucose Cotransporter-2 Inhibitors Across the Glycemic Spectrum: Cardiovascular and Renal Outcomes With Mechanistic Insights',
        journal='Cureus', year='2026', pubtype='Review',
        disposition='IN_CORPUS', tier='NARRATIVE_REVIEW',
        why='Relevant to the SGLT2i paths. Narrative review in a limited-peer-review journal; background only.'),
}

# ---------------------------------------------------------------------------
# 2. Path validation. External evidence resolved live against PubMed.
# ---------------------------------------------------------------------------
PATH_VALIDATION = {
    'verapamil -> beta_cell': dict(
        rating='PARTIALLY_VALIDATED',
        date=TODAY,
        external_pmids=['40111679'],
        finding=(
            'Tu S et al., "Effect of Verapamil on Blood Glucose in Type 1 and Type 2 '
            'Diabetes Mellitus: A Systematic Review and Meta-Analysis", Cardiovasc Drugs '
            'Ther 2026;40(1):347-359. PMID 40111679. Eight RCTs, 1100 patients. '
            'HbA1c WMD -0.45% (95% CI -0.66 to -0.23), p<0.001, 7 trials. '
            'Blood glucose WMD -6.38 mg/dL (95% CI -12.52 to -0.25), p=0.04, 6 trials. '
            'C-peptide AUC WMD +0.27 pmol/mL (95% CI 0.21 to 0.32), p<0.0001. '
            'No significant excess adverse events (OR 1.33, 95% CI 0.85-2.09).'),
        why_not_validated=(
            'PARTIALLY, not VALIDATED, and the reason is one number in the abstract: '
            'the C-peptide result - the only outcome that speaks to BETA-CELL '
            'PRESERVATION rather than to glycaemia - pools TWO trials. The HbA1c '
            'result pools seven. Reporting this path as validated on the strength of '
            'the HbA1c estimate would be validating a different claim than the path '
            'makes. The authors themselves note limited RCT scale and heterogeneity '
            'of background regimens.'),
        also_found=[
            '40650745 Diabetologia 2025 - verapamil + low-dose anti-thymocyte globulin '
            'reverses recent-onset T1D in NOD MICE. Preclinical; relevant to the '
            'combination arm, not to a human claim.',
            '41227341 Cells 2025 - verapamil restores beta-cell mass in diabetogenic '
            'stress models. Preclinical.'],
        ver_a_t1d_status=(
            'Ver-A-T1D primary RESULTS are still not in PubMed as of 2026-08-28. '
            'A PubMed search for Ver-A-T1D and for Pieber[au]+verapamil returns the '
            'protocol (39613428) and one unrelated phase I trial. Results were '
            'presented at EASD Vienna in September 2025 and are reported in press '
            'and trade coverage, which is NOT a citable source for this corpus. '
            'The corpus should continue to carry no Ver-A-T1D outcome until a '
            'peer-reviewed publication exists.'),
    ),
    'verapamil -> T1D': dict(
        rating='PARTIALLY_VALIDATED',
        date=TODAY,
        external_pmids=['40111679'],
        finding='Same anchor as verapamil -> beta_cell; see that entry. The meta-analysis covers T1D and T2D together and does not report a T1D-only C-peptide estimate.',
        why_not_validated='The corpus evidence for this path is still a protocol only. The external anchor is real but pools T1D with T2D, so it cannot carry a T1D-specific claim on its own.',
    ),
}

DOCTRINE = {
    'membership_is_two_questions': (
        'Asked on 2026-08-28 after FLAGGED was found to mean two incompatible '
        'things at once. "May this PMID be cited?" and "May it count as evidence?" '
        'are different questions and a single boolean answers neither well. '
        'PMID 18662538 (Massague, TGFbeta in Cancer, Cell 2008) is cited correctly '
        'as the definitional source for a data-dictionary term and supplies no '
        'diabetes finding: both facts have to survive. corpus_membership.py owns '
        'the distinction; nothing else may re-implement it.'),
    'count_never_answers_of_what': (
        'The four highest-ranked live research paths by data-point count all rest '
        'on no primary data: ranks 1 and 2 on a meta-analysis whose extracted '
        'numbers cannot be attributed to the pooled estimate, ranks 4 and 5 on a '
        'clinical trial PROTOCOL. Ranking by count is therefore inversely related '
        'to evidence quality at the top of this dashboard. Publication type is the '
        'cheapest honest answer and it comes from PubMed, not from local regexes.'),
    'absence_from_a_synthesis_is_not_evidence_against': (
        'PMID 40598585 (BMC Med 2025 network meta-analysis) names 11 interventions '
        'that beat placebo on 12-month C-peptide and verapamil is not among them. '
        'That is because the review covers IMMUNOTHERAPIES and verapamil was never '
        'eligible for inclusion. Reading a scope exclusion as a negative result is '
        'a mistake this corpus is well placed to make and must not.'),
}


def main():
    with open(STATE, encoding='utf-8') as fh:
        state = json.load(fh)

    if not os.path.exists(STATE + '.bak_%s' % TODAY):
        shutil.copy2(STATE, STATE + '.bak_%s' % TODAY)

    papers = state['papers']
    promoted = background = 0
    for pmid, rec in ORPHANS.items():
        entry = papers.get(pmid, {})
        entry.update({
            'title': rec['title'],
            'journal': rec['journal'],
            'year': rec['year'],
            'pub_type': rec['pubtype'],
            'status': 'VETTED' if rec['disposition'] == 'IN_CORPUS' else 'FLAGGED',
            'corpus_status': rec['disposition'],
            'evidence_tier': rec['tier'],
            'vetting_note': rec['why'],
            'vetted_date': TODAY,
            'pmid_verified': True,
            'pmid_verified_how': 'live NCBI esummary 2026-08-28; title, journal, year and publication type all read from the response',
            'claims_checked': True,
        })
        if rec['disposition'] == 'BACKGROUND':
            entry['membership_class'] = 'BACKGROUND'
            entry['membership_class_why'] = rec['why']
            entry['membership_class_date'] = TODAY
            background += 1
        else:
            promoted += 1
        papers[pmid] = entry

    state.setdefault('validated_paths', {})
    for name, val in PATH_VALIDATION.items():
        state['validated_paths'][name] = {
            **state['validated_paths'].get(name, {}), **val}

    state.setdefault('doctrine_notes', {}).update(DOCTRINE)

    # Fold the design tiers back onto the paths so the grade travels with the
    # path rather than living only in an audit file nobody reads.
    design_path = os.path.join(RESULTS, 'path_evidence_design.json')
    tiers = 0
    if os.path.exists(design_path):
        with open(design_path, encoding='utf-8') as fh:
            design = json.load(fh)['paths']
        for name, rec in design.items():
            slot = state['validated_paths'].setdefault(name, {})
            slot['evidence_design_tier'] = rec['tier']
            slot['evidence_design_why'] = rec['why']
            slot['evidence_design_date'] = TODAY
            tiers += 1

    state['last_updated'] = TODAY
    state['last_run'] = TODAY
    with open(STATE, 'w', encoding='utf-8') as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)

    print('  Orphans adjudicated: %d IN_CORPUS, %d BACKGROUND' % (promoted, background))
    print('  Paths validated against external evidence: %d' % len(PATH_VALIDATION))
    print('  Design tiers folded onto paths: %d' % tiers)
    print('  Doctrine notes added: %d' % len(DOCTRINE))
    print('  [OK]')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
