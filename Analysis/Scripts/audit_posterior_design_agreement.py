#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Does the published Bayesian posterior agree with the study design underneath it?

WHY THIS EXISTS (2026-08-29)
----------------------------
The work queue item raised 2026-08-28 said: "RANKING IS STILL BY DATA-POINT
COUNT ... build_research_paths.py does not read [the grade], so the published
Research Paths dashboard still orders by count alone."

Working that item found the premise WRONG and the problem WORSE.

  WRONG: Research_Paths.html did not order by count. Its sort key was
  (status, confidence, name) and, every path there being VALIDATED/HIGH, it
  resolved to ALPHABETICAL. Count decided nothing on that page. The 2026-08-28
  item asserted a mechanism nobody had checked, and it was repeated unchecked
  into this file's own predecessor. Recorded here so the correction outlives
  the queue entry.

  WORSE: count-derived ranking is real, but it lives on the STATISTICAL
  ANALYSIS page, not the paths page, and it is expressed as a PROBABILITY.
  statistical_analysis.py::bayesian_path_scoring sets the prior purely from
  data_point_count and PMID count:

      dpc >= 20 and n_pmids >= 3  ->  prior 0.80
      dpc >= 10 and n_pmids >= 2  ->  prior 0.65
      dpc >=  5                   ->  prior 0.50
      dpc >=  2                   ->  prior 0.35
      else                        ->  prior 0.20

  Nothing in that ladder, and nothing in the likelihood term, reads what KIND
  of study the numbers came from. So Statistical_Analysis.html published:

      #4  verapamil -> T1D                 40.0%   NO_RESULTS  (protocol only)
      #5  verapamil -> beta_cell           40.0%   NO_RESULTS  (protocol only)
      #6  dapagliflozin -> nephropathy     26.4%   PRIMARY
      #7  oxidative_stress -> cardiovascular 26.4% PRIMARY
      #9  rapamycin -> inflammation        26.4%   PRIMARY

  Two paths under which NO MEASURED OUTCOME EXISTS ANYWHERE outrank three
  paths that rest on primary data, in a figure the page describes as the
  probability that a path "represents a real, actionable research direction".
  A sorted list invites a reader to infer a ranking. A posterior states one.

WHAT THIS SCRIPT DOES
---------------------
Counts DISCORDANT PAIRS: pairs of live paths (a, b) where a's posterior is
strictly higher than b's while a's evidence design is strictly weaker. That is
the smallest honest statement of the defect - it needs no new model, makes no
claim about what the posterior SHOULD be, and it is zero when the two agree.

It does NOT rewrite the posterior. Choosing what a prior should encode is a
modelling decision, not a data repair, and an unattended run should not make
it. The script reports; build_statistical_analysis.py discloses; the queue
carries the modelling question to a human.

Never fails the build. Writes posterior_design_agreement.json.
"""

import json
import os
import re
import sys
from itertools import combinations

RESULTS = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'Results'))
STATS = os.path.join(RESULTS, 'statistical_analysis.json')
DESIGN = os.path.join(RESULTS, 'path_evidence_design.json')
PATHS = os.path.join(RESULTS, 'research_paths.json')
OUT = os.path.join(RESULTS, 'posterior_design_agreement.json')

# Weakest last. A discordant pair is one where posterior order and this order
# point in opposite directions.
TIER_RANK = {
    'PRIMARY': 0,
    'SYNTHESIS_ONLY': 1,
    'NARRATIVE_ONLY': 2,
    'NO_RESULTS': 3,
}


def tier_key(name):
    """Join key across the two path-name spellings ('a -> b' and 'a_b')."""
    if not name:
        return ''
    k = str(name).replace('->', '_').replace('→', '_').replace(' ', '_')
    return re.sub(r'_+', '_', k).strip('_').lower()


def load(path, label):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        print(f'  [skip] cannot read {label}: {exc}')
        return None


def main():
    print('=' * 74)
    print('POSTERIOR vs EVIDENCE-DESIGN AGREEMENT')
    print('=' * 74)

    stats = load(STATS, 'statistical_analysis.json')
    design = load(DESIGN, 'path_evidence_design.json')
    if not stats or not design:
        print('  Nothing to compare. Exiting clean.')
        return 0

    graded = {tier_key(k): v for k, v in design.get('paths', {}).items()}

    # HOLLOW paths are suppressed from the published page by
    # build_statistical_analysis.py; comparing them here would report a defect
    # the reader never sees. Mirror that suppression exactly.
    hollow = set()
    rp = load(PATHS, 'research_paths.json') or {}
    for name, entry in rp.get('paths', {}).items():
        if str(entry.get('status', '')).upper() == 'HOLLOW':
            hollow.add(tier_key(name))

    rows = []
    ungraded = []
    for entry in stats.get('bayesian_synthesis', {}).get('ranked', []):
        name = entry.get('path') or entry.get('name') or ''
        key = tier_key(name)
        if key in hollow:
            continue
        g = graded.get(key)
        if not g:
            ungraded.append(name)
            continue
        rows.append({
            'path': name,
            'posterior': entry.get('posterior'),
            'strength': entry.get('strength'),
            'tier': g.get('tier'),
            'tier_rank': TIER_RANK.get(g.get('tier'), 9),
            'data_points': g.get('data_points'),
        })

    print(f'\n  Live graded paths compared : {len(rows)}')
    print(f'  Suppressed as HOLLOW       : {len(hollow)}')
    print(f'  On the page but ungraded   : {len(ungraded)}')
    for n in ungraded:
        print(f'      - {n}')

    discordant = []
    comparable = 0
    for a, b in combinations(rows, 2):
        if a['posterior'] is None or b['posterior'] is None:
            continue
        if a['tier_rank'] == b['tier_rank'] or a['posterior'] == b['posterior']:
            continue
        comparable += 1
        hi, lo = (a, b) if a['posterior'] > b['posterior'] else (b, a)
        if hi['tier_rank'] > lo['tier_rank']:
            discordant.append({
                'higher_posterior': hi['path'],
                'higher_posterior_value': hi['posterior'],
                'higher_tier': hi['tier'],
                'lower_posterior': lo['path'],
                'lower_posterior_value': lo['posterior'],
                'lower_tier': lo['tier'],
            })

    rate = (len(discordant) / comparable) if comparable else 0.0
    print(f'\n  Comparable ordered pairs   : {comparable}')
    print(f'  DISCORDANT pairs           : {len(discordant)}  ({rate * 100:.1f}%)')

    if discordant:
        print('\n  Each line below is a path the page scores HIGHER while its'
              '\n  evidence design is WEAKER:\n')
        for d in discordant:
            print(f"    {d['higher_posterior']:<34} {d['higher_posterior_value'] * 100:5.1f}%"
                  f"  {d['higher_tier']:<15}  >  "
                  f"{d['lower_posterior']:<32} {d['lower_posterior_value'] * 100:5.1f}%"
                  f"  {d['lower_tier']}")

    # The sharpest single statement: a path with NO measured outcome anywhere
    # scoring above a path that rests on primary data.
    worst = [d for d in discordant
             if d['higher_tier'] == 'NO_RESULTS' and d['lower_tier'] == 'PRIMARY']
    if worst:
        print(f'\n  OF THOSE, {len(worst)} pair(s) rank a NO_RESULTS path above a PRIMARY path.')
        print('  A NO_RESULTS path has no measured outcome under it in any citing paper.')

    out = {
        'generated': __import__('datetime').date.today().isoformat(),
        'method': ('discordant-pair count between published Bayesian posterior '
                   'and PubMed-derived evidence design tier; no model is refit'),
        'paths_compared': len(rows),
        'ungraded_on_page': ungraded,
        'comparable_pairs': comparable,
        'discordant_pairs': len(discordant),
        'discordance_rate': round(rate, 4),
        'no_results_above_primary': len(worst),
        'detail': discordant,
        'rows': sorted(rows, key=lambda r: -(r['posterior'] or 0)),
    }
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f'\n  Written: {OUT}')
    print('\n[OK] audit_posterior_design_agreement')
    return 0


if __name__ == '__main__':
    sys.exit(main())
