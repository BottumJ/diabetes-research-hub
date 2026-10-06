#!/usr/bin/env python3
"""
Gate: does a gap's evidence actually mention the gap's own subject?

WHY THIS EXISTS
    On 2026-09-07 canonical Gap #11 ("Islet Transplant Registry Equity") was
    found rated GOLD on exactly two papers: PMID 19104422 (2008 CITR Update)
    and PMID 37105208 (primary graft function vs 5-year outcomes). Both are
    about islet transplantation. NEITHER mentions equity, race, ethnicity,
    socioeconomic status or access anywhere in its stored title or findings.

    Every gap in this project is an INTERSECTION of two subjects: an X axis
    (the clinical domain) and a Y axis (the lens applied to it). Gap #11 is
    islet transplant x equity. Its evidence covered X completely and Y not at
    all -- and nothing failed, because no gate had ever asked.

    That is the specific failure mode this gate catches: evidence that is
    on-topic for the easy half of an intersection and silent on the half that
    makes the gap a gap. Half-covered evidence is the most dangerous kind,
    because it looks relevant to a human skimming the citation list.

WHAT A FAILURE MEANS -- AND DOES NOT MEAN
    A gap failing here is NOT necessarily a false gap. Gap #11 failed and the
    gap itself survived two documented all-time searches. What a failure means
    is narrower and always true: THE STORED EVIDENCE DOES NOT EVIDENCE THE
    CLAIM. An absence claim is evidenced by a dated, reproducible query that
    returns nothing -- not by a citation. So the remedy for a failure is
    either to re-found the gap on a recorded null search, or to admit the gap
    was never tested.

    Conversely, PASSING here is weak news. This gate reads stored titles and
    finding snippets, so it detects the presence of a word, not the presence
    of an analysis. A paper can say "equity" once in passing and pass.
    This is a floor, not a standard.

SCOPE LIMIT, STATED PLAINLY
    Coverage is computed over whatever text gap_evidence.json already holds
    (title + finding snippets). It does not fetch abstracts. A paper whose
    abstract discusses equity but whose stored snippet does not will be
    counted as a miss. Misses are therefore an UPPER bound on the problem;
    treat each one as a prompt to read the paper, not as a proven defect.

OWNER RULINGS AND THE EXPLORATORY TIER (added 2026-09-30)
    DECISION_BRIEF_2026-09-07 put four questions to the owner that this gate
    could detect but had no standing to answer. They were answered on
    2026-09-30 and the answers are recorded in gap_owner_rulings.json:

      * A gap labelled EXPLORATORY asserts no evidential standing, so a
        coverage shortfall under that label is reported in the table and is
        not a finding. This is the same rule the zero-paper branch already
        applied to Gap #9; it now applies to all three branches.
      * A gap with a recorded ruling keeps its finding, at severity
        ACKNOWLEDGED, and does not fail the build -- PROVIDED the ruling
        carries a reader_note, which every builder showing the gap must
        print. A ruling is not an exemption from saying so in public.

    A ruling is keyed to the finding class it answered. If a ruled gap later
    fails in a DIFFERENT way, the ruling does not cover it and the gate fails.

Exit codes: 0 clean or acknowledged-only, 1 unacknowledged findings.
"""
import json
import os
import re
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RESULTS = os.path.join(BASE_DIR, 'Analysis', 'Results')
EVIDENCE = os.path.join(RESULTS, 'gap_evidence.json')
REPORT = os.path.join(RESULTS, 'gap_subject_coverage_audit.json')
RULINGS = os.path.join(RESULTS, 'gap_owner_rulings.json')

# Each gap decomposed into its two axes. The Y axis is deliberately the harder
# one -- it is the lens that makes the intersection a research gap rather than
# a topic. Synonym sets are intentionally GENEROUS: a generous synonym set
# makes a miss more meaningful, because it means the word is absent under any
# reasonable phrasing, not just the one the gap title happened to use.
AXES = {
    1:  {'name': 'Gene Therapy for LADA',
         'x': ('gene therapy', [r'gene therap', r'gene transfer', r'\bAAV\b', r'lentivir',
                                r'CRISPR', r'gene editing', r'vector']),
         'y': ('LADA', [r'\bLADA\b', r'latent autoimmune', r'slowly progressive.{0,20}diabet'])},
    # Restated 2026-10-06 (owner ruling): the gap is equity in BETA CELL
    # therapies, not diabetes equity in general, which is well studied.
    2:  {'name': 'Health Equity in Beta Cell Therapies',
         'x': ('beta cell therapy', [r'islet', r'beta.?cell', r'stem.?cell', r'cell therap',
                                     r'zimislecel', r'replacement therap']),
         'y': ('equity', [r'equit', r'inequit', r'dispar', r'\bracial\b', r'\brace\b', r'ethnic',
                          r'socioeconomic', r'underserved', r'\baccess\b', r'affordab',
                          r'uninsured', r'income'])},
    3:  {'name': 'Insulin Resistance in Islet Transplant',
         'x': ('islet transplant', [r'islet.{0,20}transplant', r'transplant.{0,20}islet',
                                    r'\bCITR\b', r'islet infusion', r'graft']),
         'y': ('insulin resistance', [r'insulin resistan', r'insulin sensitiv', r'\bHOMA',
                                      r'euglycemic clamp', r'glucose disposal'])},
    4:  {'name': 'Drug Repurposing for Islet Transplant',
         'x': ('islet transplant', [r'islet.{0,20}transplant', r'transplant.{0,20}islet',
                                    r'\bCITR\b', r'islet infusion', r'graft']),
         'y': ('repurposing', [r'repurpos', r'repositio', r'off.label', r'existing drug',
                               r'approved drug', r'new indication', r'generic drug'])},
    5:  {'name': 'Treg in Diabetic Neuropathy',
         'x': ('diabetic neuropathy', [r'neuropath', r'neuralg', r'nerve', r'\bDPN\b',
                                       r'neuropathic pain']),
         'y': ('Treg', [r'\bTreg', r'regulatory T', r'\bFoxp3', r'\bCD4\+CD25', r'T.{0,3}reg cell'])},
    6:  {'name': 'CAR-T Access Barriers',
         'x': ('CAR-T', [r'\bCAR.?T\b', r'chimeric antigen', r'\bCAR.?Treg', r'cell therapy']),
         'y': ('access barriers', [r'access', r'barrier', r'cost', r'price', r'afford',
                                   r'equit', r'dispar', r'reimburse', r'coverage', r'availab'])},
    7:  {'name': 'GKA Drug Repurposing',
         'x': ('glucokinase activator', [r'glucokinase', r'\bGKA\b', r'dorzagliatin',
                                         r'\bGCK\b', r'piragliatin']),
         'y': ('repurposing', [r'repurpos', r'repositio', r'off.label', r'new indication',
                               r'existing drug', r'approved drug'])},
    8:  {'name': 'Immunomodulatory Drugs for LADA',
         'x': ('immunomodulation', [r'immunomodul', r'immunosuppress', r'immunotherap',
                                    r'teplizumab', r'abatacept', r'rituximab', r'baricitinib',
                                    r'anti.CD3', r'\bATG\b']),
         'y': ('LADA', [r'\bLADA\b', r'latent autoimmune', r'adult.{0,15}autoimmune diabet'])},
    9:  {'name': 'GKA in LADA',
         'x': ('glucokinase activator', [r'glucokinase', r'\bGKA\b', r'dorzagliatin', r'\bGCK\b']),
         'y': ('LADA', [r'\bLADA\b', r'latent autoimmune'])},
    10: {'name': 'LADA Prevalence by Healthcare Setting',
         'x': ('LADA', [r'\bLADA\b', r'latent autoimmune']),
         'y': ('prevalence by setting', [r'prevalen', r'inciden', r'epidemiolog', r'primary care',
                                         r'specialist', r'healthcare setting', r'population.based',
                                         r'registry', r'cohort'])},
    11: {'name': 'Islet Transplant Registry Equity',
         'x': ('islet transplant registry', [r'islet.{0,20}transplant', r'\bCITR\b',
                                             r'transplant registry', r'islet infusion']),
         'y': ('equity', [r'equit', r'inequit', r'dispar', r'\bracial\b', r'\brace\b', r'ethnic',
                          r'socioeconomic', r'underserved', r'\baccess\b', r'income',
                          r'insurance', r'deprivation'])},
    12: {'name': 'Generic Drug x Diabetes Mechanism Catalog',
         'x': ('generic drugs', [r'generic', r'off.patent', r'\bmetformin\b', r'\bverapamil\b',
                                 r'\bcolchicine\b', r'repurpos', r'low.cost']),
         'y': ('mechanism', [r'mechanis', r'pathway', r'target', r'signal', r'inflammasome',
                             r'\bNLRP3\b', r'receptor', r'mode of action'])},
    13: {'name': 'Personalized Nutrition for Beta Cells',
         'x': ('beta cell', [r'beta.?cell', r'β.?cell', r'islet', r'C.peptide', r'insulin secret']),
         'y': ('personalized nutrition', [r'nutrition', r'\bdiet', r'glycemic index', r'\bfood\b',
                                          r'personali[sz]ed', r'precision nutrition',
                                          r'macronutrient', r'microbiome.{0,20}diet'])},
    14: {'name': 'Personalized Nutrition for LADA',
         'x': ('LADA', [r'\bLADA\b', r'latent autoimmune']),
         'y': ('personalized nutrition', [r'nutrition', r'\bdiet', r'personali[sz]ed',
                                          r'macronutrient', r'precision nutrition'])},
    15: {'name': 'GKA Pricing Trajectory',
         'x': ('glucokinase activator', [r'glucokinase', r'\bGKA\b', r'dorzagliatin']),
         'y': ('pricing', [r'\bpric', r'\bcost', r'afford', r'reimburse', r'market',
                           r'economic', r'expenditure', r'list price'])},
}


def paper_text(paper):
    """All stored text for a paper. Titles plus finding snippets, nothing fetched."""
    parts = [str(paper.get('title', '')), str(paper.get('journal', ''))]
    for finding in paper.get('findings', []) or []:
        parts.append(str(finding.get('text', '')))
    return ' '.join(parts)


def hits(text, patterns):
    return sorted({p for p in patterns if re.search(p, text, re.IGNORECASE)})


def load_rulings():
    """gap_id (int) -> ruling. Missing file means no rulings, not an error."""
    try:
        with open(RULINGS, encoding='utf-8') as fh:
            raw = json.load(fh).get('rulings', {})
    except FileNotFoundError:
        return {}
    return {int(k): v for k, v in raw.items()}


def main():
    with open(EVIDENCE, encoding='utf-8') as fh:
        gaps = json.load(fh)['gaps']
    rulings = load_rulings()

    findings = []
    rows = []

    for key in sorted(gaps, key=lambda k: int(k)):
        gap = gaps[key]
        gid = int(key)
        axes = AXES.get(gid)
        if not axes:
            continue

        papers = gap.get('papers', []) or []
        x_label, x_pat = axes['x']
        y_label, y_pat = axes['y']

        x_cover, y_cover, both_cover = [], [], []
        for paper in papers:
            text = paper_text(paper)
            hx, hy = hits(text, x_pat), hits(text, y_pat)
            if hx:
                x_cover.append(paper.get('pmid'))
            if hy:
                y_cover.append(paper.get('pmid'))
            if hx and hy:
                both_cover.append(paper.get('pmid'))

        n = len(papers)
        row = {
            'gap_id': gid,
            'name': gap.get('name'),
            'tier': gap.get('tier'),
            'papers': n,
            'x_axis': x_label, 'x_covered': len(x_cover),
            'y_axis': y_label, 'y_covered': len(y_cover),
            'both_axes_covered': len(both_cover),
            'papers_covering_both': both_cover,
        }
        rows.append(row)

        # EXPLORATORY claims no evidential standing, so there is nothing for a
        # coverage shortfall to contradict. Reported in the table, not a finding.
        if gap.get('tier') == 'EXPLORATORY':
            row['status'] = 'exploratory - no evidential standing claimed'
            continue

        # The failure that matters: a tiered gap whose evidence never mentions
        # the lens. Zero papers on the Y axis means the gap's own question is
        # unrepresented in its own evidence.
        if n and not y_cover:
            findings.append({
                'gap_id': gid, 'name': gap.get('name'), 'tier': gap.get('tier'),
                'severity': 'HIGH',
                'problem': ('%d evidence paper(s), NONE mentioning the "%s" axis. The stored '
                            'evidence is on-topic for "%s" only. This gap is an intersection '
                            'and its evidence covers one side of it.'
                            % (n, y_label, x_label)),
                'remedy': ('Re-found on a dated null search, or record that the gap has never '
                           'been tested. Do not publish the current citation list as support.'),
                'finding_class': 'lens_axis_absent',
                'pmids': [p.get('pmid') for p in papers],
            })
        elif n and not both_cover:
            findings.append({
                'gap_id': gid, 'name': gap.get('name'), 'tier': gap.get('tier'),
                'severity': 'MEDIUM',
                'problem': ('%d evidence paper(s). %d touch "%s" and %d touch "%s", but NO '
                            'SINGLE PAPER touches both. The intersection itself is unevidenced; '
                            'the two axes are supported separately and joined only by inference.'
                            % (n, len(x_cover), x_label, len(y_cover), y_label)),
                'remedy': ('State explicitly that the intersection rests on inference across '
                           'papers, or find a paper at the intersection.'),
                'finding_class': 'no_paper_at_intersection',
                'pmids': [p.get('pmid') for p in papers],
            })
        elif not n and gap.get('tier') not in ('EXPLORATORY', None):
            findings.append({
                'gap_id': gid, 'name': gap.get('name'), 'tier': gap.get('tier'),
                'severity': 'HIGH',
                'problem': ('Tier %s with ZERO evidence papers. A tier above EXPLORATORY asserts '
                            'evidential standing this gap does not have.' % gap.get('tier')),
                'remedy': 'Demote to EXPLORATORY or attach evidence.',
                'finding_class': 'tier_without_evidence',
                'pmids': [],
            })

    # Apply owner rulings. A ruling answers ONE finding class for ONE gap and
    # must carry the sentence a reader will be shown.
    for f in findings:
        ruling = rulings.get(f['gap_id'])
        if (ruling and ruling.get('reader_note')
                and f['finding_class'] in ruling.get('covers', [])):
            f['detected_severity'] = f['severity']
            f['severity'] = 'ACKNOWLEDGED'
            f['ruling'] = {k: ruling[k] for k in ('date', 'decision') if k in ruling}
            f['reader_note'] = ruling['reader_note']
        else:
            # What a reader is told. The remedy is an instruction to a
            # maintainer and must never be published as if it were a caveat.
            f['reader_note'] = f['problem']
    blocking = [f for f in findings if f['severity'] != 'ACKNOWLEDGED']

    report = {
        'generated': datetime.now().isoformat(),
        'gate': 'gap_subject_coverage',
        'method': ('Regex over stored title + journal + finding snippets in gap_evidence.json. '
                   'No abstracts fetched. Misses are an UPPER bound: a paper whose abstract '
                   'covers the axis but whose stored snippet does not will read as a miss.'),
        'gaps_checked': len(rows),
        'findings_count': len(findings),
        'blocking_count': len(blocking),
        'findings': findings,
        'coverage_table': rows,
    }
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)

    print('GAP SUBJECT COVERAGE AUDIT')
    print('=' * 78)
    print('%-4s %-38s %-6s %5s %6s %6s %6s' % ('GAP', 'NAME', 'TIER', 'PAP', 'X', 'Y', 'BOTH'))
    print('-' * 78)
    for r in rows:
        print('%-4d %-38.38s %-6.6s %5d %6d %6d %6d'
              % (r['gap_id'], r['name'] or '', r['tier'] or '', r['papers'],
                 r['x_covered'], r['y_covered'], r['both_axes_covered']))
    print('-' * 78)
    if findings:
        print('\n%d FINDING(S):\n' % len(findings))
        for f in findings:
            print('  [%s] Gap #%d (%s) %s' % (f['severity'], f['gap_id'], f['tier'], f['name']))
            print('      %s' % f['problem'])
            if f['severity'] == 'ACKNOWLEDGED':
                print('      RULED %s: %s\n' % (f['ruling'].get('date'), f['ruling'].get('decision')))
            else:
                print('      REMEDY: %s\n' % f['remedy'])
    if blocking:
        print('[FAIL] gap_subject_coverage: %d unacknowledged finding(s) -> %s'
              % (len(blocking), REPORT))
        return 1
    if findings:
        print('[OK] gap_subject_coverage: %d finding(s), all under a recorded owner ruling.'
              % len(findings))
        return 0
    print('\n[OK] gap_subject_coverage: every tiered gap\'s evidence mentions both of its axes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
