#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The gap tiers were assigned by the same metric that just misled on paths.

THE ARGUMENT (work queue, 2026-08-28)
-------------------------------------
GOLD / SILVER / BRONZE were assigned by counting INDEPENDENT SOURCES. On
2026-08-29 the identical logic was shown to fail on research paths: ranking by
count put a trial PROTOCOL - a document that reports no outcome at all - above
paths carrying measured human results, in 62.3% of comparable ordered pairs.
A count answers "how much" and never "of what".

Nothing about that failure is specific to paths. A gap can hold two independent
NARRATIVE REVIEWS and be SILVER on source count while resting on no measured
data whatsoever. This script asks each gap the question its tier never asked:
of the papers under it, how many report primary data?

WHY THIS REPORTS AND DOES NOT RE-TIER
-------------------------------------
Gap tier drives what the dashboards claim is a real research gap, and a tier is
a scientific judgement about a literature, not an arithmetic property of it.
An unattended run may MEASURE the design mix and may say which gaps look
mis-tiered; it may not silently restate a published tier. Same reasoning the
repo applied to the dose-label headline on 2026-08-20 and to the Bayesian prior
on 2026-08-29.

There is a second reason to report rather than act, and it is the more
important one. The design field this audit reads is itself incomplete: as
measured on 2026-08-30, 152 of 359 corpus papers (42%) carry no design-bearing
publication type, rising to 74% of 2026 papers because NCBI assigns those tags
on a lag. So UNKNOWN here means "PubMed has not said", never "not primary".
Any gap whose evidence is mostly UNKNOWN cannot be graded at all, and this
script says so rather than defaulting it to PRIMARY - which is precisely the
silent default that let a protocol rank first.

TIERS, WEAKEST FIRST - deliberately identical to audit_path_evidence_design.py
------------------------------------------------------------------------------
  NO_EVIDENCE       the gap cites no resolvable paper
  NO_RESULTS        every paper is a protocol, editorial, comment or news item
  NARRATIVE_ONLY    every paper is a narrative review
  SYNTHESIS_ONLY    rests on systematic reviews / meta-analyses. High evidence
                    level; flagged for ATTRIBUTION, not for weakness
  PRIMARY_THIN      primary data exists but is a small minority of the papers
  PRIMARY           primary data is a substantial share of the evidence
  UNGRADEABLE       too little of the evidence has a readable design tag

WHY PRIMARY_THIN EXISTS - a defect found by running this script (2026-08-30)
----------------------------------------------------------------------------
The first version of this audit reused the path grader's rule verbatim:
PRIMARY means "at least one paper reports primary data". On a research path
citing one to three papers that is a strict test - one paper is most of the
evidence. On a GAP the denominator is ten to thirty, and the identical
sentence becomes nearly unfalsifiable. It graded three GOLD gaps clean:

    #2  Health Equity          GOLD   1 of 11 primary, 3 narrative reviews
    #6  CAR-T Access Barriers  GOLD   1 of 13 primary, 6 narrative reviews
    #11 Islet Registry Equity  GOLD   1 of 2  primary

"Weakest-wins" over a large collection is strongest-wins in practice, because
a single primary paper outvotes any number of reviews. So the tier vocabulary
carried over from paths silently reversed its meaning when the denominator
grew - the same shape of error as ranking by count, arriving by a different
road. PRIMARY_THIN separates "one paper carries this" from "this rests on
measured data", using PRIMARY_SHARE_FLOOR below.


Reads .pubtype_cache.json (refreshed by refresh_pubtype_cache.py) and never
touches the network itself, so it runs offline and cannot be the stage that
stalls the pipeline. Never fails the build. Writes gap_evidence_design.json.
"""

import json
import os
import sys
import time

RESULTS = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'Results'))
GAPS = os.path.join(RESULTS, 'gap_evidence.json')
CACHE = os.path.join(RESULTS, '.pubtype_cache.json')
OUT = os.path.join(RESULTS, 'gap_evidence_design.json')

NO_RESULTS_TYPES = {
    'Clinical Trial Protocol', 'Editorial', 'Comment', 'Letter',
    'Published Erratum', 'Retraction of Publication', 'News',
    'Bibliometric', 'Video-Audio Media',
}
SYNTHESIS_TYPES = {'Systematic Review', 'Meta-Analysis', 'Network Meta-Analysis',
                   'Consensus Development Conference', 'Guideline',
                   'Practice Guideline'}
NARRATIVE_REVIEW_TYPES = {'Review'}
# Tags that positively assert primary human data. The path grader reads only
# 'Randomized Controlled Trial' and lets everything else fall through to
# PRIMARY; that fall-through is why an untagged paper and a tagged trial score
# alike. Listing the phase and observational tags explicitly lets this audit
# tell "PubMed says primary" apart from "PubMed has not said", which is the
# whole point of the exercise.
PRIMARY_TYPES = {
    'Randomized Controlled Trial', 'Clinical Trial', 'Controlled Clinical Trial',
    'Clinical Trial, Phase I', 'Clinical Trial, Phase II',
    'Clinical Trial, Phase III', 'Clinical Trial, Phase IV',
    'Observational Study', 'Multicenter Study', 'Case Reports',
    'Comparative Study', 'Evaluation Study', 'Validation Study',
    'Equivalence Trial', 'Pragmatic Clinical Trial',
    'Twin Study', 'Clinical Study',
}

# Below this share of design-readable papers, a tier is not a measurement.
# 0.5 is a judgement, stated here rather than buried: it says a grade needs
# more evidence read than unread. Change it in one place and re-run.
READABLE_FLOOR = 0.5

# Share of DESIGN-READABLE papers that must report primary data before a gap
# is called PRIMARY rather than PRIMARY_THIN. Computed over readable papers,
# not over all papers, so that PubMed's indexing lag cannot by itself push a
# gap into THIN. 1/3 is a judgement and is stated rather than buried; it is
# the point where "some of this is measured" stops describing the collection.
PRIMARY_SHARE_FLOOR = 1.0 / 3.0


def classify(pubtypes):
    pts = set(pubtypes or [])
    if pts & NO_RESULTS_TYPES and not (pts & {'Randomized Controlled Trial'}):
        return 'NO_RESULTS'
    if pts & SYNTHESIS_TYPES:
        return 'SYNTHESIS'
    if pts & NARRATIVE_REVIEW_TYPES:
        return 'NARRATIVE'
    if pts & PRIMARY_TYPES:
        return 'PRIMARY'
    return 'UNKNOWN'


def tier_for(kinds):
    """Weakest-wins over what is READABLE; UNKNOWN abstains rather than votes."""
    if not kinds:
        return 'NO_EVIDENCE', 'gap cites no resolvable paper'
    readable = [k for k in kinds if k != 'UNKNOWN']
    if not readable or len(readable) / float(len(kinds)) < READABLE_FLOOR:
        return ('UNGRADEABLE',
                'only %d of %d papers carry a design-bearing PubMed type - too '
                'little to grade, and absence of a tag is not evidence of '
                'absence of design' % (len(readable), len(kinds)))
    if all(k == 'NO_RESULTS' for k in readable):
        return ('NO_RESULTS',
                'every design-readable paper is a protocol/editorial/comment - '
                'no measured outcome exists under this gap')
    if all(k in ('NO_RESULTS', 'NARRATIVE') for k in readable):
        return ('NARRATIVE_ONLY',
                'every design-readable paper is a narrative review - no primary '
                'data and no systematic synthesis')
    if all(k in ('NO_RESULTS', 'SYNTHESIS', 'NARRATIVE') for k in readable):
        return ('SYNTHESIS_ONLY',
                'rests on systematic reviews or meta-analyses - high evidence '
                'level, but numbers scraped from a synthesis cannot be '
                'attributed to the pooled estimate rather than to a tabulated trial')
    n_primary = len([k for k in readable if k == 'PRIMARY'])
    share = n_primary / float(len(readable))
    if share < PRIMARY_SHARE_FLOOR:
        return ('PRIMARY_THIN',
                'only %d of %d design-readable papers (%.0f%%) report primary '
                'data - the rest are reviews or syntheses, so this gap rests on '
                'a small number of measured studies and a larger commentary '
                'literature' % (n_primary, len(readable), 100.0 * share))
    return ('PRIMARY',
            '%d of %d design-readable papers (%.0f%%) report primary data'
            % (n_primary, len(readable), 100.0 * share))


# What a published tier ASSERTS about design, so a mismatch can be named.
# GOLD/SILVER on this repo's dashboards read as "a real, well-evidenced gap".
TIER_EXPECTS_PRIMARY = {'GOLD', 'SILVER'}


def main():
    try:
        with open(GAPS, 'r', encoding='utf-8') as fh:
            gaps = json.load(fh)['gaps']
        with open(CACHE, 'r', encoding='utf-8') as fh:
            cache = json.load(fh)
    except (OSError, ValueError, KeyError) as exc:
        print('  [skip] cannot read inputs: %s' % exc)
        return 0

    report, counts, flags = {}, {}, []
    for gid, gap in sorted(gaps.items(), key=lambda kv: int(kv[0])):
        papers = gap.get('papers', []) or []
        rows, kinds = [], []
        for p in papers:
            pmid = str(p.get('pmid', ''))
            rec = cache.get(pmid, {})
            kind = classify(rec.get('pubtype'))
            kinds.append(kind)
            rows.append({
                'pmid': pmid,
                'kind': kind,
                'title': (rec.get('title') or p.get('title', ''))[:150],
                'journal': rec.get('journal', ''),
                'year': rec.get('year', ''),
                'pubtypes': rec.get('pubtype', []),
                'in_cache': pmid in cache,
            })
        tier, why = tier_for(kinds)
        mix = {}
        for k in kinds:
            mix[k] = mix.get(k, 0) + 1
        n_primary = mix.get('PRIMARY', 0)
        counts[tier] = counts.get(tier, 0) + 1

        published = gap.get('tier', '?')
        mismatch = None
        if published in TIER_EXPECTS_PRIMARY and tier in (
                'NO_EVIDENCE', 'NO_RESULTS', 'NARRATIVE_ONLY'):
            mismatch = ('published %s but no paper under it reports primary data'
                        % published)
        elif published in TIER_EXPECTS_PRIMARY and tier == 'UNGRADEABLE':
            mismatch = ('published %s and its design mix cannot be read - the '
                        'tier is unverifiable, not necessarily wrong' % published)
        elif published in TIER_EXPECTS_PRIMARY and tier == 'PRIMARY_THIN':
            mismatch = ('published %s while %d of %d design-readable papers '
                        'report primary data - the tier rests on a small '
                        'measured core inside a mostly narrative literature'
                        % (published, mix.get('PRIMARY', 0),
                           len([k for k in kinds if k != 'UNKNOWN'])))
        elif published in TIER_EXPECTS_PRIMARY and tier == 'SYNTHESIS_ONLY':
            mismatch = ('published %s on synthesis evidence only - defensible, '
                        'but the attribution caveat applies' % published)
        if mismatch:
            flags.append({'gap_id': gid, 'name': gap.get('name', ''),
                          'published_tier': published, 'design_tier': tier,
                          'note': mismatch})

        report[gid] = {
            'name': gap.get('name', ''),
            'published_tier': published,
            'design_tier': tier,
            'why': why,
            'papers_total': len(papers),
            'papers_primary': n_primary,
            'papers_design_readable': len([k for k in kinds if k != 'UNKNOWN']),
            'design_mix': mix,
            'total_findings': gap.get('total_findings'),
            'papers': rows,
        }

    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump({'generated': time.strftime('%Y-%m-%d'),
                   'readable_floor': READABLE_FLOOR,
                   'counts': counts, 'flags': flags, 'gaps': report},
                  fh, indent=2, ensure_ascii=False)

    print('  %-3s %-40s %-9s %-15s %-9s %s'
          % ('#', 'GAP', 'PUBLISHED', 'BY DESIGN', 'PRIMARY', 'MIX'))
    for gid, r in report.items():
        mix = ' '.join('%s:%d' % (k[:4], v) for k, v in sorted(r['design_mix'].items()))
        print('  %-3s %-40s %-9s %-15s %-9s %s'
              % (gid, r['name'][:40], r['published_tier'], r['design_tier'],
                 '%d/%d' % (r['papers_primary'], r['papers_total']), mix))

    print()
    print('  ' + ', '.join('%s=%d' % kv for kv in sorted(counts.items())))
    if flags:
        print()
        print('  %d gap(s) where the published tier is not supported by design:'
              % len(flags))
        for f in flags:
            print('    #%-3s %-38s %s -> %s'
                  % (f['gap_id'], f['name'][:38], f['published_tier'],
                     f['design_tier']))
            print('         %s' % f['note'])
        print()
        print('  These are REPORTED, not applied. Re-tiering a published gap is')
        print('  a scientific judgement and belongs to a human.')
    print()
    print('  [OK] wrote %s' % os.path.basename(OUT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
