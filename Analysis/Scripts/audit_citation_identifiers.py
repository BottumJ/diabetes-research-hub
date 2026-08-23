#!/usr/bin/env python3
"""Gate: a path's RATING must rest on at least one resolvable, on-topic citation
-- in ANY identifier namespace, not just the one field the earlier gate reads.

WHY THIS EXISTS
---------------
audit_path_citations.py (2026-08-20) screens `external_pmids` and nothing else.
It was written after 17 real-but-unrelated PubMed records were found sitting on
research paths. It closed that hole for one field, in one namespace.

On 2026-08-23 a sweep of every rated path found that citations are stored under
at least NINE different field names, in THREE identifier namespaces:

  external_pmids        list or dict     screened by the 2026-08-20 gate
  external_refs         dict             PMC ids and DOIs   -- NEVER SCREENED
  external_evidence     list of prose    -- NEVER SCREENED
  external_urls         list of URLs     PMC / pubmed links -- NEVER SCREENED
  corpus_pmids          list             -- NEVER SCREENED
  pmids_supporting      list             -- NEVER SCREENED
  key_sources           prose w/ PMIDs   -- NEVER SCREENED (queue item 2026-08-20)
  revalidation_history  prose w/ PMIDs   -- NEVER SCREENED
  notes / update_*      prose w/ PMIDs   -- NEVER SCREENED

Concretely: `NF_kB -> inflammation` is rated VALIDATED with clinical confidence
HIGH and has ZERO entries in external_pmids. It is not uncited -- its three
sources are PMC5681994, PMC12395217 and DOI 10.1016/j.cmet.2010.12.008. Every
one of them was invisible to every gate in this repo. The same is true of
`oxidative_stress -> cardiovascular` (VALIDATED, HIGH/HIGH, three PMC ids).

An unscreened citation is not a safer citation because it is a PMC id. It is the
identical defect class that put a bakery paper on the teplizumab path, in a
namespace nobody was looking at.

WHAT IT DOES
------------
1. Harvests PMIDs, PMC ids and DOIs from the WHOLE record, every field.
2. Normalises all three namespaces to a PMID:
     PMC id -> NCBI ID Converter
     DOI    -> PubMed esearch "<doi>[doi]"
   Anything that will not normalise is reported, not silently dropped.
3. Resolves each PMID to a title and applies the two-part topic screen from
   audit_path_citations.py (domain vocabulary OR path-key tokens).
4. FAILS if a path carrying a rating has zero verified on-topic citations.

Not-in-PubMed is reported as UNINDEXED rather than FAIL: a legitimate source can
be a preprint, a conference abstract or a press release. What is not acceptable
is a HIGH-confidence rating whose entire support is unindexed -- that is flagged
loudly and counts as unsupported, unless the path is listed in
UNINDEXED_BY_DESIGN with a written reason, in which case it is printed under its
own heading every run but does not fail the build.

Exit 0 = clean. Exit 1 = a rated path has no verifiable on-topic support, or an
off-topic citation is present and unreviewed.
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
CACHE = os.path.join(RESULTS, '.citation_identifier_cache.json')
REPORT = os.path.join(RESULTS, 'citation_identifier_audit.json')

ESUMMARY = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?'
ESEARCH = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
IDCONV = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?'
TOOL = {'tool': 'diabetes_research_hub', 'email': 'justin.bottum@gmail.com'}

# Same vocabulary as audit_path_citations.py. Kept as a literal copy rather than
# an import so that gate can be changed without silently changing this one.
DOMAIN = re.compile(
    r'diabet|insulin|beta.?cell|β.?cell|islet|glyc|hba1c|glucose|glucotox|autoimmun|'
    r'nlrp3|inflammasome|inflammat|metformin|sglt.?2|glp.?1|dpp.?4|verapamil|colchicine|'
    r'pioglitazone|thiazolidinedione|hydroxychloroquine|chloroquine|nephropath|retinopath|'
    r'neuropath|treg|regulatory t|c-peptide|lada|obes|metabolic|cardiovascular|kidney|renal|'
    r'statin|immun|pancrea|gliflozin|gliptin|liraglutide|semaglutide|teplizumab|rituximab|'
    r'tacrolimus|calcineurin|transplant|rapamycin|sirolimus|mtor|ampk|oxidative stress|'
    r'reactive oxygen|nf-?.?b|cytokine|interleukin|tnf|c-reactive|crp|hyperglyc|glucagon|'
    r'endothelial|vascular|atheroscler|ros\b|antioxidant|mitochondri',
    re.I)

STOP = {'to', 'the', 'and', 'of', 'in', 'a', 'for', 'via', 'on'}

# Paths whose evidence is genuinely not in PubMed. Each needs a reason and a
# re-check date - an unexplained exemption is how a gate rots. These are still
# printed under their own heading every run; they just do not fail the build,
# because "not indexed" is a fact about the literature, not a defect in the repo.
UNINDEXED_BY_DESIGN = {
    'tegoprubart_islet_t1d': (
        'Evidence is ADA/ATTD conference presentation + Eledon press releases only; '
        'the record itself says so and explicitly forbids citing it as vetted. '
        'The rating is PARTIALLY_VALIDATED, which is the correct rating for '
        'unpublished data. Re-check for a peer-reviewed publication monthly.'),
}

RE_PMC = re.compile(r'PMC(\d{6,9})')
RE_DOI = re.compile(r'\b(10\.\d{4,9}/[^\s"\',;)\]]+)')
RE_PMID_PROSE = re.compile(r'PMID[:\s=]*(\d{7,8})', re.I)
RE_PUBMED_URL = re.compile(r'pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,8})')

# Structured fields whose values are bare PMIDs (list or dict-keyed).
PMID_FIELDS = ('external_pmids', 'corpus_pmids', 'pmids_supporting',
               'supporting_pmids', 'pmids')

# Repair-log fields. These EXIST to name a bad citation ("before": [...],
# "replaces": "X - off topic"). Screening them re-flags every citation the repo
# has already fixed, which would train the reader to ignore this gate. They are
# skipped for the off-topic test and contribute no support either way.
AUDIT_TRAIL_FIELDS = {'citation_fixes', 'citation_repairs', 'prose_citation_repairs',
                      'purged_citations', 'corrections'}


def path_tokens(key):
    parts = re.split(r'[^A-Za-z0-9]+', key or '')
    return {p.lower() for p in parts if len(p) > 2 and p.lower() not in STOP}


def canonical(key):
    """`NF_kB -> inflammation` and `NF_kB_to_inflammation` are the same path.

    The two stores spell keys differently; the 2026-08-21 run recorded that this
    divergence caused false NEVER-VALIDATED queue items. Support must therefore be
    counted per underlying path, not per stored record, or this gate reports a
    well-cited path as unsupported purely because the citations sit in the other
    store's copy.
    """
    k = re.sub(r'(?:\s*->\s*|_to_)', ' ', key or '', flags=re.I)
    return ' '.join(sorted(t for t in re.split(r'[^A-Za-z0-9]+', k.lower()) if t))


def load_cache():
    if os.path.exists(CACHE):
        try:
            with open(CACHE, encoding='utf-8') as f:
                return json.load(f)
        except ValueError:
            pass
    return {'pmc': {}, 'doi': {}, 'title': {}}


def save_cache(c):
    with open(CACHE, 'w', encoding='utf-8') as f:
        json.dump(c, f, indent=1, ensure_ascii=False)


def _get(url, timeout=60):
    return urllib.request.urlopen(url, timeout=timeout).read().decode('utf-8', 'replace')


def resolve_pmc(pmcids, cache):
    missing = [p for p in pmcids if p not in cache['pmc']]
    for i in range(0, len(missing), 100):
        batch = missing[i:i + 100]
        q = dict(TOOL, format='json', ids=','.join('PMC' + b for b in batch))
        try:
            data = json.loads(_get(IDCONV + urllib.parse.urlencode(q)))
        except Exception as exc:
            print(f'  [WARN] PMC id conversion failed: {exc}')
            continue
        for rec in data.get('records', []):
            key = str(rec.get('requested-id', '')).replace('PMC', '')
            cache['pmc'][key] = str(rec.get('pmid')) if rec.get('pmid') else None
        time.sleep(0.4)
    return {p: cache['pmc'].get(p) for p in pmcids}


def resolve_doi(dois, cache):
    for d in dois:
        if d in cache['doi']:
            continue
        q = dict(TOOL, db='pubmed', retmode='json', term=f'{d}[doi]')
        try:
            r = json.loads(_get(ESEARCH + urllib.parse.urlencode(q), timeout=30))
            ids = r['esearchresult'].get('idlist') or []
            cache['doi'][d] = ids[0] if ids else None
        except Exception as exc:
            print(f'  [WARN] DOI lookup failed for {d}: {exc}')
        time.sleep(0.4)
    return {d: cache['doi'].get(d) for d in dois}


def resolve_titles(pmids, cache):
    missing = sorted({p for p in pmids if p and p not in cache['title']})
    for i in range(0, len(missing), 150):
        batch = missing[i:i + 150]
        q = dict(TOOL, db='pubmed', retmode='json', id=','.join(batch))
        try:
            data = json.loads(_get(ESUMMARY + urllib.parse.urlencode(q)))
        except Exception as exc:
            print(f'  [WARN] esummary failed: {exc}')
            continue
        res = data.get('result', {})
        for p in batch:
            rec = res.get(p)
            if isinstance(rec, dict) and rec.get('title'):
                cache['title'][p] = {'title': rec['title'],
                                     'journal': rec.get('fulljournalname', ''),
                                     'year': (rec.get('pubdate') or '')[:4]}
            else:
                cache['title'][p] = None
        time.sleep(0.4)
    return {p: cache['title'].get(p) for p in pmids if p}


def harvest(key, rec):
    """Every citation identifier in a record, with the field it came from."""
    found = []           # (namespace, value, field)
    for field in PMID_FIELDS:
        val = rec.get(field)
        ids = list(val) if isinstance(val, (list, dict)) else []
        for v in ids:
            v = str(v).strip()
            if re.fullmatch(r'\d{7,8}', v):
                found.append(('pmid', v, field))
            elif v.upper().startswith('PMC'):
                found.append(('pmc', v.upper().replace('PMC', ''), field))
    scanned = {k: v for k, v in rec.items() if k not in AUDIT_TRAIL_FIELDS}
    blob = json.dumps(scanned, ensure_ascii=False)
    for m in RE_PMC.finditer(blob):
        found.append(('pmc', m.group(1), 'prose_or_refs'))
    for m in RE_DOI.finditer(blob):
        doi = m.group(1).rstrip('.,;)"\'')
        # DOIs harvested out of publisher URLs carry a page suffix that is not part
        # of the DOI; leaving it on makes a resolvable DOI look unindexed.
        doi = re.sub(r'/(full|abstract|pdf|html|epdf)$', '', doi, flags=re.I)
        found.append(('doi', doi, 'prose_or_refs'))
    for m in RE_PMID_PROSE.finditer(blob):
        found.append(('pmid', m.group(1), 'prose'))
    for m in RE_PUBMED_URL.finditer(blob):
        found.append(('pmid', m.group(1), 'url'))
    # de-duplicate on (namespace, value), keeping the most structured field
    seen, out = {}, []
    for ns, val, field in found:
        if (ns, val) not in seen:
            seen[(ns, val)] = field
            out.append({'ns': ns, 'value': val, 'field': field})
    return out


def main():
    with open(STATE, encoding='utf-8') as f:
        state = json.load(f)
    cache = load_cache()

    records = []
    for store in ('paths', 'validated_paths'):
        for key, rec in (state.get(store) or {}).items():
            if not isinstance(rec, dict):
                continue
            rating = rec.get('status') or rec.get('rating')
            records.append({'store': store, 'key': key, 'rating': rating,
                            'clin': rec.get('clinical_confidence'),
                            'pre': rec.get('preclinical_confidence'),
                            'ids': harvest(key, rec)})

    pmcs = sorted({i['value'] for r in records for i in r['ids'] if i['ns'] == 'pmc'})
    dois = sorted({i['value'] for r in records for i in r['ids'] if i['ns'] == 'doi'})
    print(f'Harvested {sum(len(r["ids"]) for r in records)} identifiers across '
          f'{len(records)} path records: {len(pmcs)} PMC ids, {len(dois)} DOIs.')

    pmc_map = resolve_pmc(pmcs, cache)
    doi_map = resolve_doi(dois, cache)

    wanted = set()
    for r in records:
        for i in r['ids']:
            i['pmid'] = (i['value'] if i['ns'] == 'pmid'
                         else pmc_map.get(i['value']) if i['ns'] == 'pmc'
                         else doi_map.get(i['value']))
            if i['pmid']:
                wanted.add(i['pmid'])
    titles = resolve_titles(sorted(wanted), cache)
    save_cache(cache)

    unsupported, offtopic, unindexed, exempted = [], [], [], []
    for r in records:
        toks = path_tokens(r['key'])
        supported = 0
        for i in r['ids']:
            meta = titles.get(i['pmid']) if i['pmid'] else None
            if not meta:
                i['verdict'] = 'UNINDEXED'
                unindexed.append((r['key'], i))
                continue
            i['title'] = meta['title']
            i['journal'] = meta['journal']
            i['year'] = meta['year']
            tl = meta['title'].lower()
            on = bool(DOMAIN.search(tl)) or any(t in tl for t in toks)
            i['verdict'] = 'ON_TOPIC' if on else 'OFF_TOPIC'
            if on:
                supported += 1
            else:
                offtopic.append((r['key'], i))
        r['supported'] = supported

    # Aggregate per underlying path: a record with no citations is not a problem
    # if the same path's other store copy carries verified ones.
    by_path = {}
    for r in records:
        slot = by_path.setdefault(canonical(r['key']), {'keys': set(), 'ratings': set(),
                                                        'supported': 0, 'ids': 0})
        slot['keys'].add(r['key'])
        slot['supported'] += r['supported']
        slot['ids'] += len(r['ids'])
        if r['rating']:
            slot['ratings'].add(r['rating'])
    SOFT = {'EXTRACTION_ARTIFACT', 'HOLLOW', 'UNVALIDATED'}
    for canon, slot in sorted(by_path.items()):
        hard = {x for x in slot['ratings'] if x not in SOFT}
        if hard and slot['supported'] == 0:
            exempt = next((UNINDEXED_BY_DESIGN[k] for k in slot['keys']
                           if k in UNINDEXED_BY_DESIGN), None)
            entry = {'key': ' / '.join(sorted(slot['keys'])),
                     'rating': ', '.join(sorted(hard)),
                     'clin': None, 'ids': [None] * slot['ids'], 'exempt': exempt}
            (exempted if exempt else unsupported).append(entry)

    print()
    print('=' * 74)
    print(f'PATH RECORDS: {len(records)}  ->  DISTINCT PATHS: {len(by_path)}')
    print(f'RATED PATHS WITH ZERO VERIFIED ON-TOPIC CITATIONS: {len(unsupported)}')
    for r in unsupported:
        print(f'  {r["key"][:46]:46s} {str(r["rating"])[:22]:22s} '
              f'identifiers_present={len(r["ids"])}')
    if exempted:
        print(f'\nEXEMPT - EVIDENCE NOT PUBMED-INDEXED BY DESIGN: {len(exempted)}')
        for r in exempted:
            print(f'  {r["key"][:46]:46s} {str(r["rating"])[:22]:22s}')
            print(f'      reason: {r["exempt"]}')
    print()
    print(f'OFF-TOPIC CITATIONS: {len(offtopic)}')
    for key, i in offtopic:
        print(f'  {key:42s} {i["ns"]}:{i["value"]} -> {i.get("title", "")[:70]}')
    print()
    print(f'UNINDEXED IDENTIFIERS (reported, not failed): {len(unindexed)}')
    for key, i in unindexed[:30]:
        print(f'  {key:42s} {i["ns"]}:{i["value"]}  [{i["field"]}]')
    if len(unindexed) > 30:
        print(f'  ... and {len(unindexed) - 30} more')

    with open(REPORT, 'w', encoding='utf-8') as f:
        json.dump({'generated': time.strftime('%Y-%m-%d'),
                   'records': records,
                   'unsupported': [r['key'] for r in unsupported],
                   'exempt_unindexed': [r['key'] for r in exempted],
                   'offtopic': [[k, i] for k, i in offtopic],
                   'unindexed': [[k, i] for k, i in unindexed]},
                  f, indent=1, ensure_ascii=False)
    print(f'\nReport: {REPORT}')

    bad = len(unsupported) + len(offtopic)
    print('[OK]' if bad == 0 else f'[FAIL] {bad} issue(s)')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
