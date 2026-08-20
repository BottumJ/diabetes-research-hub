#!/usr/bin/env python3
"""Gate: every external_pmid on a research path must be a REAL paper ABOUT that path.

WHY THIS EXISTS
---------------
On 2026-08-16 a note was added to the work queue: "Grepping for PMIDs >= 42M is
NOT sufficient - it cannot catch a real PMID attached to the wrong claim."
That note was correct, and nothing was built to act on it. check_citation_mismatches.py
consumes validate_citations.py output, which scans .py source literals. Path
`external_pmids` in agent_state.json were never screened by anything.

On 2026-08-20 a sweep of all 164 distinct external PMIDs cited by research paths
found 20 that are real, resolvable PubMed records about entirely unrelated
subjects. Among them:

  37889505  "Probiotic breads; a market trend in functional bakery products"
            cited as the PROTECT teplizumab trial by `teplizumab -> autoimmune`
            -- and recorded as verified evidence in the 2026-08-19 run history.
  29987247  "Osteoporosis Self-Assessment Tool"       -> verapamil -> beta_cell
  37865119  "C. elegans germline RNA interference"    -> teplizumab -> T1D
  32398655  "Borosilicate glasses containing lanthanide ions" -> metformin -> inflammation
  38934094  "Value co-creation in ageing-in-place programs in China" -> empagliflozin -> nephropathy

This is the exact failure the 2026-08-19 mirror sweep could not see, because it
asked "does this path have external evidence?" and not "is the external evidence
about this path?". Presence is not correctness.

WHAT IT DOES
------------
For every external_pmid on every path in both stores:
  1. Resolve it against PubMed (NCBI E-utilities). Unresolvable => FAIL.
  2. Check the title against a domain vocabulary AND against tokens taken from
     the path key itself. A title matching neither => FLAG as off-topic.

Deliberately a two-part test. A domain-only screen passes anything about
diabetes, which would let a metformin paper sit on a teplizumab path. A
path-token-only screen fails legitimate mechanism papers that never name the
drug. Requiring one or the other keeps false positives low while still catching
bakery science on an immunotherapy path.

Known-good exceptions live in ACCEPTED so a reviewed citation stops re-alarming.

Exit 0 = clean. Exit 1 = unresolvable or unreviewed off-topic citation present.
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, 'Results')
STATE = os.path.join(RESULTS, 'agent_state.json')
CACHE = os.path.join(RESULTS, '.pmid_title_cache.json')
EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?'

# Vocabulary of the corpus domain. A cited title touching any of this is at least
# plausibly on-topic for a diabetes research path.
DOMAIN = re.compile(
    r'diabet|insulin|beta.?cell|β.?cell|islet|glyc|hba1c|glucose|glucotox|autoimmun|'
    r'nlrp3|inflammasome|inflammat|metformin|sglt.?2|glp.?1|dpp.?4|verapamil|colchicine|'
    r'pioglitazone|thiazolidinedione|hydroxychloroquine|chloroquine|nephropath|retinopath|'
    r'neuropath|treg|regulatory t|c-peptide|lada|obes|metabolic|cardiovascular|kidney|renal|'
    r'statin|immun|pancrea|gliflozin|gliptin|liraglutide|semaglutide|teplizumab|rituximab|'
    r'tacrolimus|calcineurin|transplant|rapamycin|sirolimus|mtor|ampk|oxidative stress|'
    r'reactive oxygen|nf-?.?b|cytokine|interleukin|tnf|c-reactive|crp|hyperglyc|glucagon',
    re.I)

# Citations reviewed and accepted despite failing the automatic screen.
# Each needs a reason - an unexplained exception is how a gate rots.
ACCEPTED = {
    '41892868': 'SGLT-2 inhibitor safety network meta-analysis; screen missed the hyphenated "SGLT-2".',
    '16490432': 'Thiazolidinediones vs serum CRP meta-analysis - directly on-topic for pioglitazone -> inflammation.',
    '20926154': 'Thiazolidinediones vs circulating CRP - directly on-topic for pioglitazone -> inflammation.',
}

STOP = {'to', 'the', 'and', 'of', 'in', 'a', 'for', 'via', 'on'}


def path_tokens(key):
    """Content words from a path key, e.g. 'verapamil -> beta_cell' -> {verapamil, beta, cell}."""
    parts = re.split(r'[^A-Za-z0-9]+', key or '')
    return {p.lower() for p in parts if len(p) > 2 and p.lower() not in STOP}


def collect(state):
    """{pmid: [where, ...]} across both path stores."""
    out = {}
    for store in ('paths', 'validated_paths'):
        for key, rec in (state.get(store) or {}).items():
            if not isinstance(rec, dict):
                continue
            ep = rec.get('external_pmids')
            ids = list(ep) if isinstance(ep, (list, dict)) else []
            for pmid in ids:
                pmid = str(pmid)
                if re.fullmatch(r'\d{7,8}', pmid):
                    out.setdefault(pmid, []).append((store, key))
    return out


def fetch_titles(pmids):
    cache = {}
    if os.path.exists(CACHE):
        try:
            with open(CACHE, encoding='utf-8') as f:
                cache = json.load(f)
        except ValueError:
            cache = {}
    missing = [p for p in pmids if p not in cache]
    for i in range(0, len(missing), 150):
        batch = missing[i:i + 150]
        q = urllib.parse.urlencode({'db': 'pubmed', 'retmode': 'json', 'id': ','.join(batch)})
        try:
            data = json.load(urllib.request.urlopen(EUTILS + q, timeout=60))
        except Exception as exc:                      # network flake must not fake a pass
            print(f'  [WARN] PubMed lookup failed for a batch: {exc}')
            continue
        for p in batch:
            cache[p] = (data.get('result', {}).get(p, {}) or {}).get('title', '')
        time.sleep(0.4)
    with open(CACHE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=1, ensure_ascii=False)
    return cache


def main():
    with open(STATE, encoding='utf-8') as f:
        state = json.load(f)

    cited = collect(state)
    titles = fetch_titles(sorted(cited))

    unresolved, offtopic, accepted_hits = [], [], []
    for pmid in sorted(cited):
        title = titles.get(pmid, '')
        if not title:
            unresolved.append((pmid, cited[pmid]))
            continue
        if pmid in ACCEPTED:
            accepted_hits.append(pmid)
            continue
        if DOMAIN.search(title):
            continue
        # Last chance: does the title name something from the path key itself?
        if any(tok in title.lower() for _, key in cited[pmid] for tok in path_tokens(key)):
            continue
        offtopic.append((pmid, title, cited[pmid]))

    print('Path external-citation audit')
    print(f'  paths screened from : {STATE}')
    print(f'  distinct PMIDs cited: {len(cited)}')
    print(f'  resolved            : {len(cited) - len(unresolved)}')
    print(f'  reviewed exceptions : {len(accepted_hits)}')

    if unresolved:
        print(f'\n[FAIL] {len(unresolved)} PMID(s) do not resolve in PubMed:')
        for pmid, where in unresolved:
            print(f'  - {pmid} cited by {where}')

    if offtopic:
        print(f'\n[FAIL] {len(offtopic)} citation(s) resolve to papers on unrelated subjects:')
        for pmid, title, where in offtopic:
            print(f'  - {pmid} "{title[:88]}"')
            for store, key in where:
                print(f'      cited by {store}:{key}')

    if not unresolved and not offtopic:
        print('\n[OK] Every path citation resolves and is on-topic.')
        return 0

    print('\nEach must be corrected to the right PMID or removed. If a flagged '
          'citation is genuinely correct, add it to ACCEPTED with a reason.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
