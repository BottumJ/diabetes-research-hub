#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A citation can be RIGHT about its paper and wrong about what the paper says.

THE FINDING (2026-08-29)
------------------------
build_drug_repurposing_screen.py attributes the monthly cost of all 34 screened
drugs to:

    "Hernandez 2018 (PMID:29710129) generic drug pricing"

Every identifier in that string is correct. PMID 29710129 resolves. The first
author is Hernandez. The year is 2018. The title agrees with PubMed. It passes
PMID validation, title agreement, coordinate checking and the retraction gate,
because there is nothing wrong with the citation.

There is something wrong with the CLAIM. PMID 29710129 is Hernandez I, Prasad V,
Gellad WF, "Total Costs of Chimeric Antigen Receptor T-Cell Immunotherapy",
JAMA Oncology 2018;4(7):994-996. It is a cost analysis of CAR-T cancer therapy.
It is not a generic drug pricing database and it contains no price for
metformin, glyburide, verapamil or any other drug on this page.

The same PMID is cited CORRECTLY elsewhere in this repo: build_cart_access.py
cites it as "Hernandez et al. JAMA Oncol 2018" in a CAR-T access discussion,
which is exactly what it is. The screen appears to have borrowed the identifier
from there.

REACH
-----
  34 cost_source strings  - one per screened drug
   1 per-drug cost table footnote "(PMID:29710129)"
   1 executive-summary sentence: "27 candidates cost under $1/month ...
     (Hernandez 2018, PMID:29710129)"

So the single most-repeated citation on the page is the source for none of the
numbers it is attached to.

WHY EVERY EXISTING GATE MISSED IT
---------------------------------
audit_prose_citation_titles.py DID see it, at build_drug_repurposing_screen.py
line 41, and filed it under `journal_not_recognised` - a bucket for gate
artifacts. The gate compares the citation's stated journal against PubMed's.
The screen's string names no journal at all, so the comparison could not run and
the finding was classified as noise rather than as a claim the paper does not
support. A gate that only checks whether a citation IDENTIFIES the right paper
cannot check whether the paper SUPPORTS the sentence.

WHAT THIS SCRIPT DOES, AND WHAT IT REFUSES TO DO
------------------------------------------------
It does NOT substitute a different pricing source. No source for these figures
exists in this repository, and inventing a plausible one would convert a
traceable error into an untraceable one. It marks the figures UNSOURCED, which
is what they are, and leaves the numbers themselves untouched - they may well
be approximately right, but "probably right" is not a provenance.

It also repairs two overstatements in the same entry, found in the same pass:

  1. Glyburide evidence read "Lamkanfi et al (J Cell Biol 2009, PMID:19805629)
     demonstrated direct NLRP3 inhibition at concentrations achievable in vivo."
     That paper is mouse macrophage and human monocyte work in vitro, plus one
     mouse endotoxemia survival experiment. Its abstract makes no claim about
     concentrations achievable in vivo, and no human received glyburide for
     inflammation in it. The model is now stated.

  2. The same entry read "Widely studied in gestational diabetes
     (PMID:23738527)." PMID 23738527 is "A method for accounting for maintenance
     costs in flux balance analysis improves the prediction of plant cell
     metabolic phenotypes under stress conditions." It is a PLANT METABOLISM
     paper. The claim is removed rather than re-sourced.

Idempotent: running twice changes nothing the second time.
"""

import io
import json
import os
import re
import sys
from datetime import date

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.abspath(os.path.join(SCRIPTS, '..', 'Results'))
TARGET = os.path.join(SCRIPTS, 'build_drug_repurposing_screen.py')
OUT = os.path.join(RESULTS, 'cost_provenance_repair_20260829.json')

UNSOURCED = ('UNSOURCED - see cost_provenance_repair_20260829.json; '
             'previously mis-attributed to PMID:29710129, a CAR-T cost analysis')


def main():
    with io.open(TARGET, 'r', encoding='utf-8') as fh:
        src = fh.read()
    original = src
    changes = []

    # ------------------------------------------------------------------
    # 1. The 34 cost_source strings.
    # ------------------------------------------------------------------
    pattern = re.compile(
        r'("cost_source":\s*")Hernandez 2018 \(PMID:29710129\) generic drug pricing[^"]*(")')
    n_cost = len(pattern.findall(src))
    if n_cost:
        src = pattern.sub(r'\1' + UNSOURCED + r'\2', src)
        changes.append({
            'what': 'cost_source strings',
            'count': n_cost,
            'from': 'Hernandez 2018 (PMID:29710129) generic drug pricing',
            'to': UNSOURCED,
            'reason': ('PMID 29710129 is a JAMA Oncology CAR-T cost analysis and '
                       'contains no generic drug prices'),
        })

    # ------------------------------------------------------------------
    # 2. The per-drug cost table footnote.
    # ------------------------------------------------------------------
    old_footnote = ('cost_formatted = f"${drug_data[\'generic_cost\']:.2f}'
                    '<br/><small>(PMID:29710129)</small>"')
    # Written as an implicit-concatenation pair, NOT as one f-string with a
    # nested title="..." attribute: on Python 3.10 the inner double quotes
    # terminate the f-string and the file stops parsing. Caught by the syntax
    # check on first application of this repair.
    new_footnote = ('cost_formatted = (f"${drug_data[\'generic_cost\']:.2f}<br/>"\n'
                    '                          f"<small>(unsourced)</small>")')
    if old_footnote in src:
        src = src.replace(old_footnote, new_footnote)
        changes.append({
            'what': 'per-drug cost table footnote',
            'count': 1,
            'from': '(PMID:29710129)',
            'to': '(unsourced), with the history in a tooltip',
            'reason': 'same mis-attribution, rendered on every table row',
        })

    # ------------------------------------------------------------------
    # 3. The executive-summary sentence.
    # ------------------------------------------------------------------
    old_exec = ('candidates cost under $1/month with relevant mechanisms for both '
                'T2D and autoimmune diabetes (Hernandez 2018, PMID:29710129)')
    new_exec = ('candidates cost under $1/month with relevant mechanisms for both '
                'T2D and autoimmune diabetes (cost figures are UNSOURCED: they '
                'were attributed to Hernandez 2018, PMID:29710129 until '
                '2026-08-29, but that paper is a JAMA Oncology analysis of CAR-T '
                'therapy costs and holds no generic drug prices; the figures are '
                'retained unchanged and their provenance is open)')
    if old_exec in src:
        src = src.replace(old_exec, new_exec)
        changes.append({
            'what': 'executive-summary cost claim',
            'count': 1,
            'from': old_exec,
            'to': new_exec,
            'reason': ('the headline "27 candidates cost under $1/month" carried '
                       'the mis-attribution into the summary a reader reads first'),
        })

    # ------------------------------------------------------------------
    # 4. Glyburide: preclinical overstatement + a plant-metabolism citation.
    # ------------------------------------------------------------------
    old_gly = ('Lamkanfi et al (J Cell Biol 2009, PMID:19805629) demonstrated '
               'direct NLRP3 inhibition at concentrations achievable in vivo. '
               'WHO Essential Medicine. Dual mechanism: glucose-lowering via '
               'insulin secretion AND anti-inflammatory via NLRP3. Widely '
               'studied in gestational diabetes (PMID:23738527). Hypoglycemia '
               'risk is the primary safety limitation')
    new_gly = ('PRECLINICAL. Lamkanfi et al (J Cell Biol 2009, PMID:19805629) '
               'showed glyburide prevents Cryopyrin/NLRP3 inflammasome '
               'activation in mouse macrophages and in human monocytes ex vivo, '
               'and delayed LPS-induced lethality in mice. No human received '
               'glyburide for an inflammatory outcome in that study, and it '
               # No nested double quotes: the target dict uses double-quoted
               # string values, so a quoted phrase here ends the value early.
               # Same trap as the footnote above, hit twice in one repair.
               'makes no claim about concentrations achievable in vivo - that '
               'phrase appeared here until 2026-08-29 and is not supported by '
               'the paper. WHO '
               'Essential Medicine. Proposed dual mechanism: glucose-lowering '
               'via insulin secretion AND anti-inflammatory via NLRP3, the '
               'second demonstrated only preclinically. Hypoglycemia risk is '
               'the primary safety limitation')
    if old_gly in src:
        src = src.replace(old_gly, new_gly)
        changes.append({
            'what': 'glyburide evidence string',
            'count': 1,
            'removed_claims': [
                {'claim': 'direct NLRP3 inhibition at concentrations achievable in vivo',
                 'why': ('PMID 19805629 is in vitro macrophage/monocyte work plus a '
                         'mouse endotoxemia survival experiment; it states no '
                         'in vivo achievable concentration')},
                {'claim': 'Widely studied in gestational diabetes (PMID:23738527)',
                 'why': ('PMID 23738527 is "A method for accounting for maintenance '
                         'costs in flux balance analysis improves the prediction of '
                         'plant cell metabolic phenotypes under stress conditions" '
                         '- a plant metabolism paper, unrelated to glyburide or to '
                         'gestational diabetes')},
            ],
            'reason': 'preclinical evidence presented without its model; one citation to an unrelated paper',
        })

    # ------------------------------------------------------------------
    # 5. THE SECOND PASS, and the reason there had to be one.
    # ------------------------------------------------------------------
    # The first pass repaired the 34 cost_source strings, the table footnote
    # and the executive summary, and a grep afterwards still found the PMID
    # asserted as a pricing source in TWELVE more places: a stat-card label, a
    # cost-chart caption, five cost bars, five combination-therapy cost cells,
    # a scoring-rubric definition and the methodology paragraph. Repairing "the
    # citation" meant repairing the places it was easiest to see.
    #
    # The methodology paragraph was the worst of them. It did not merely cite
    # the paper, it DESCRIBED it: "Hernandez 2018 (PMID:29710129) systematic
    # review of global generic drug pricing". PMID 29710129 is a JAMA Oncology
    # research letter on CAR-T therapy costs. It is not a systematic review, it
    # is not about generic drugs, and it is not about pricing across countries.
    # An invented description is worse than a bare wrong citation: it tells the
    # reader what they would have found had they checked.
    SECOND_PASS = [
        ('Agents Under $1/Month (PMID:29710129)',
         'Agents Under $1/Month (cost source unverified)',
         'stat-card label'),
        ('Pricing data from Hernandez 2018 (PMID:29710129) and WHO generic drug databases.',
         'Pricing provenance is UNRESOLVED. These figures were attributed to '
         'Hernandez 2018 (PMID:29710129) until 2026-08-29; that paper is a JAMA '
         'Oncology analysis of CAR-T therapy costs and holds no generic drug '
         'prices. No WHO database extract is held in this repository either. '
         'The values are unchanged and unverified.',
         'cost-chart caption'),
        ('<span style="font-size: 0.75rem;">(PMID:29710129)</span>',
         '<span style="font-size: 0.75rem;">(unsourced)</span>',
         'cost bar labels'),
        ('Sub-$0.20/month agents widely manufactured score 9-10 (Hernandez 2018, '
         'PMID:29710129). Agents under $1/month with established generics score '
         '7-9 (PMID:29710129). Agents requiring specialized manufacturing or '
         'pricing >$2/month score 4-6 (PMID:29710129).',
         'Sub-$0.20/month agents widely manufactured score 9-10; agents under '
         '$1/month with established generics score 7-9; agents requiring '
         'specialized manufacturing or pricing >$2/month score 4-6. These '
         'thresholds were attributed to Hernandez 2018 (PMID:29710129) until '
         '2026-08-29. That paper is a CAR-T cost analysis and sets none of them; '
         'the thresholds are this screen own convention.',
         'availability-score rubric'),
        ('Generic drug pricing data sourced from Hernandez 2018 (PMID:29710129) '
         'systematic review of global generic drug pricing and WHO Essential '
         'Medicines List procurement databases.',
         'Generic drug pricing data are UNSOURCED. Until 2026-08-29 this '
         'paragraph described PMID:29710129 as a systematic review of global '
         'generic drug pricing; it is Hernandez I, Prasad V, Gellad WF, Total '
         'Costs of Chimeric Antigen Receptor T-Cell Immunotherapy, JAMA Oncol '
         '2018 - a research letter on CAR-T therapy costs, not a systematic '
         'review, not about generic drugs and not about international pricing. '
         'No WHO procurement extract is held here either. The cost figures on '
         'this page are retained unchanged and should be treated as '
         'unverified order-of-magnitude estimates.',
         'methodology paragraph (invented description of the cited paper)'),
        # Found by a THIRD grep, after the second pass reported success. The
        # combination-cost caption sits 21 lines below the one already fixed
        # and phrases the same claim differently ("WHO pricing databases"
        # rather than "WHO generic drug databases"), so neither the literal
        # match nor the regex reached it. Three passes to clear one citation
        # is the measurement worth keeping: a wrong source spreads by
        # paraphrase, and grep for the identifier is the only reliable sweep.
        ('Combination costs from Hernandez 2018 (PMID:29710129) and WHO pricing databases.',
         'Combination costs are UNSOURCED. They were attributed to Hernandez '
         '2018 (PMID:29710129) until 2026-08-29; that paper is a CAR-T cost '
         'analysis and holds no generic drug prices. No WHO pricing extract is '
         'held in this repository.',
         'combination-cost caption'),
    ]
    for old, new, label in SECOND_PASS:
        n = src.count(old)
        if n:
            src = src.replace(old, new)
            changes.append({'what': label, 'count': n, 'from': old[:120],
                            'to': new[:120],
                            'reason': 'asserted PMID:29710129 as a generic-pricing source'})

    # Combination-therapy cost cells: same claim, five near-identical strings.
    combo = re.compile(r'\(((?:generic markets|generic); )?Hernandez 2018, PMID:29710129\)')
    n_combo = len(combo.findall(src))
    if n_combo:
        src = combo.sub(lambda m: '(' + (m.group(1) or '') + 'cost unsourced)', src)
        changes.append({'what': 'combination-therapy cost cells', 'count': n_combo,
                        'from': '(Hernandez 2018, PMID:29710129)',
                        'to': '(cost unsourced)',
                        'reason': 'asserted PMID:29710129 as a generic-pricing source'})

    if src == original:
        print('  Nothing to repair - already applied.')
        report = {'generated': date.today().isoformat(), 'changes': [],
                  'note': 'idempotent no-op'}
    else:
        with io.open(TARGET, 'w', encoding='utf-8') as fh:
            fh.write(src)
        report = {
            'generated': date.today().isoformat(),
            'target': 'Analysis/Scripts/build_drug_repurposing_screen.py',
            'defect_class': ('CITATION RESOLVES AND IDENTIFIES THE RIGHT PAPER, '
                             'BUT THE PAPER DOES NOT SUPPORT THE CLAIM'),
            'wrong_source': {
                'pmid': '29710129',
                'actual': ('Hernandez I, Prasad V, Gellad WF. Total Costs of '
                           'Chimeric Antigen Receptor T-Cell Immunotherapy. '
                           'JAMA Oncol. 2018;4(7):994-996.'),
                'was_cited_as': 'generic drug pricing database',
                'correct_use_elsewhere': ('build_cart_access.py cites the same PMID '
                                          'correctly, in a CAR-T access context'),
            },
            'unrelated_citation_removed': {
                'pmid': '23738527',
                'actual': ('A method for accounting for maintenance costs in flux '
                           'balance analysis improves the prediction of plant cell '
                           'metabolic phenotypes under stress conditions.'),
                'was_cited_as': 'glyburide widely studied in gestational diabetes',
            },
            'numbers_changed': 0,
            'note': ('Cost VALUES are untouched. Only their provenance claim '
                     'changed, from a false one to none.'),
            'changes': changes,
        }
        print(f'  Repaired {len(changes)} site group(s) in build_drug_repurposing_screen.py')
        for c in changes:
            print(f"    - {c['what']} x{c['count']}")

    with io.open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print(f'  Written: {OUT}')
    print('\n[OK] repair_cost_provenance_20260829')
    return 0


if __name__ == '__main__':
    sys.exit(main())
