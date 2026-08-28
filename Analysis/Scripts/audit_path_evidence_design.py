#!/usr/bin/env python3
"""What KIND of study is each live research path actually resting on?

THE FINDING THAT PROMPTED THIS (work queue, 2026-08-18)
-------------------------------------------------------
NLRP3_inflammasome -> nephropathy was found to rest entirely on table
fragments from ONE narrative review. The path displayed a data-point count
like any other path, and nothing on the dashboard distinguished 61 numbers
scraped out of a review's summary table from 61 numbers measured in patients.

The queue item asked for review-only paths to be marked WEAK. This script
does that and one thing more, because a second design class turned out to be
just as load-bearing and just as invisible: a CLINICAL TRIAL PROTOCOL, which
by definition reports no results at all. Two of the three highest-ranked
paths cite exactly one paper each, and that paper is a protocol.

WHY DESIGN AND NOT COUNT
------------------------
A data-point count answers "how much", never "of what". Ranking paths by
count silently ranks a protocol's dose table above a meta-analysis's effect
estimate. Publication type is the cheapest available proxy for the question
the count cannot answer, it comes from PubMed rather than from this repo's
own regexes, and it is the one field a builder cannot accidentally invent.

TIERS, WEAKEST FIRST
--------------------
  NO_RESULTS      every citing paper is a protocol, editorial, comment or
                  bibliometric study. There is no measured outcome anywhere
                  under this path.
  NARRATIVE_ONLY  every citing paper is a narrative review. Genuinely weak.
  SYNTHESIS_ONLY  rests on a systematic review or meta-analysis. NOT weak
                  evidence - an SR/MA outranks a single trial - but numbers
                  scraped from one cannot be attributed to the pooled
                  estimate rather than to a trial the synthesis tabulates.
                  Flagged for attribution, not for weight.
  PRIMARY         at least one citing paper reports primary data.

Never fails the build. A tier is a disclosure, not a defect - failing on it
would push the repo toward deleting honest weak evidence rather than
labelling it. Writes path_evidence_design.json.
"""

import json
import os
import sys
import time
import urllib.request

RESULTS = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'Results'))
PATHS = os.path.join(RESULTS, 'research_paths.json')
OUT = os.path.join(RESULTS, 'path_evidence_design.json')

ESUMMARY = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
            '?db=pubmed&retmode=json&id=%s')

# PubMed publication types, mapped to the question "does this contain a
# measured outcome, and in whom".
NO_RESULTS_TYPES = {
    'Clinical Trial Protocol', 'Editorial', 'Comment', 'Letter',
    'Published Erratum', 'Retraction of Publication', 'News',
    'Bibliometric', 'Video-Audio Media',
}
# Split deliberately. Collapsing these into one "review" bucket would call a
# systematic review and meta-analysis WEAK, which is backwards - an SR/MA sits
# at the TOP of the evidence hierarchy. The problem with a synthesis here is
# not its evidential weight, it is ATTRIBUTION: this repo's extractor scrapes
# numbers out of text, and a number inside a meta-analysis may be the pooled
# estimate or may be one of the trials it tabulates. Those are different
# claims and extraction cannot tell them apart. A narrative review is the
# genuinely weak case.
SYNTHESIS_TYPES = {'Systematic Review', 'Meta-Analysis', 'Network Meta-Analysis',
                   'Consensus Development Conference', 'Guideline',
                   'Practice Guideline'}
NARRATIVE_REVIEW_TYPES = {'Review'}

# Preclinical is not a PubMed publication type, so it cannot be read off the
# same field. Left as UNKNOWN rather than guessed from the title: inferring
# "animal study" from words in a title is exactly the kind of regex judgement
# that produced the hollow paths in the first place.


def fetch(pmids):
    out = {}
    pmids = [str(p) for p in pmids]
    for i in range(0, len(pmids), 40):
        chunk = pmids[i:i + 40]
        url = ESUMMARY % ','.join(chunk)
        try:
            with urllib.request.urlopen(url, timeout=45) as fh:
                data = json.loads(fh.read().decode('utf-8'))['result']
        except Exception as exc:
            print('  [WARN] esummary failed for %d PMID(s): %s' % (len(chunk), exc))
            continue
        for p in data.get('uids', []):
            rec = data[p]
            out[p] = {
                'title': rec.get('title', ''),
                'journal': rec.get('source', ''),
                'year': (rec.get('pubdate', '') or '')[:4],
                'pubtypes': rec.get('pubtype', []),
            }
        time.sleep(0.4)
    return out


def tier_for(pmid_records):
    """Weakest-wins across the papers a path cites."""
    if not pmid_records:
        return 'NO_EVIDENCE', 'path cites no resolvable paper'

    kinds = []
    for rec in pmid_records:
        pts = set(rec['pubtypes'])
        if pts & NO_RESULTS_TYPES and not (pts & {'Randomized Controlled Trial'}):
            kinds.append('NO_RESULTS')
        elif pts & SYNTHESIS_TYPES:
            kinds.append('SYNTHESIS')
        elif pts & NARRATIVE_REVIEW_TYPES:
            kinds.append('NARRATIVE')
        else:
            kinds.append('PRIMARY')

    if all(k == 'NO_RESULTS' for k in kinds):
        return 'NO_RESULTS', 'every citing paper is a protocol/editorial/comment - no measured outcome exists under this path'
    if all(k in ('NO_RESULTS', 'NARRATIVE') for k in kinds):
        return 'NARRATIVE_ONLY', 'every citing paper is a narrative review - no primary data and no systematic synthesis'
    if all(k in ('NO_RESULTS', 'SYNTHESIS', 'NARRATIVE') for k in kinds):
        return 'SYNTHESIS_ONLY', 'rests on a systematic review or meta-analysis - high evidence level, but extracted numbers cannot be attributed to the pooled estimate rather than to a tabulated trial'
    return 'PRIMARY', 'at least one citing paper reports primary data'


def main():
    with open(PATHS, encoding='utf-8') as fh:
        store = json.load(fh)
    paths = store['paths']

    live = {k: v for k, v in paths.items() if v.get('status') != 'HOLLOW'}
    wanted = sorted({str(p) for v in live.values() for p in v.get('pmids', [])})
    print('  Live paths: %d   distinct cited PMIDs: %d' % (len(live), len(wanted)))

    meta = fetch(wanted)
    missing = [p for p in wanted if p not in meta]
    if missing:
        # Refuse to grade what could not be read. A path graded PRIMARY
        # because its lookup silently failed is worse than an ungraded path.
        print('  [WARN] %d PMID(s) did not resolve and are graded UNRESOLVED: %s'
              % (len(missing), ', '.join(missing)))

    report = {}
    counts = {}
    for name, rec in sorted(live.items(),
                            key=lambda kv: -(kv[1].get('data_point_count_stored') or 0)):
        pmids = [str(p) for p in rec.get('pmids', [])]
        known = [meta[p] for p in pmids if p in meta]
        if len(known) != len(pmids):
            tier, why = 'UNRESOLVED', 'one or more cited PMIDs did not resolve at audit time'
        else:
            tier, why = tier_for(known)
        counts[tier] = counts.get(tier, 0) + 1
        report[name] = {
            'tier': tier,
            'why': why,
            'data_points': rec.get('data_point_count_stored'),
            'papers': [
                {'pmid': p,
                 'title': meta.get(p, {}).get('title', ''),
                 'journal': meta.get(p, {}).get('journal', ''),
                 'year': meta.get(p, {}).get('year', ''),
                 'pubtypes': meta.get(p, {}).get('pubtypes', [])}
                for p in pmids
            ],
        }

    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump({'generated': time.strftime('%Y-%m-%d'),
                   'counts': counts, 'paths': report}, fh,
                  indent=2, ensure_ascii=False)

    print()
    print('  %-34s %-6s %-12s %s' % ('PATH', 'PTS', 'TIER', 'CITED DESIGN'))
    for name, r in report.items():
        designs = '; '.join(
            '%s %s' % (p['pmid'], '/'.join(p['pubtypes'][:2]) or 'Journal Article')
            for p in r['papers'])
        print('  %-34s %-6s %-12s %s' % (name[:34], r['data_points'], r['tier'], designs[:70]))

    print()
    print('  ' + ', '.join('%s=%d' % kv for kv in sorted(counts.items())))
    weak = [n for n, r in report.items()
            if r['tier'] in ('NO_RESULTS', 'NARRATIVE_ONLY', 'SYNTHESIS_ONLY')]
    if weak:
        print()
        print('  %d path(s) rest on no primary data. These must not be ranked'
              % len(weak))
        print('  alongside paths carrying measured human outcomes:')
        for n in weak:
            print('    %-34s %s' % (n[:34], report[n]['tier']))
    print()
    print('  [OK] wrote %s' % os.path.basename(OUT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
