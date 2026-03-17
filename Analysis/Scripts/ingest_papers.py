#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper Ingestion Pipeline - Step 1: Fetch & Store
=================================================
Retrieves abstracts and (where available) full text for all verified PMIDs
in the Diabetes Research Hub, then stores them in a structured paper library.

Pipeline stages:
  1. Load verified PMIDs from pmid_verification.json
  2. Batch-fetch abstracts via NCBI EFetch API
  3. Convert PMIDs to PMCIDs via NCBI ID Converter API
  4. Check PMC Open Access availability
  5. Fetch full text via BioC API for OA papers
  6. Store everything in Analysis/Results/paper_library/

Rate limits: 3 requests/sec without API key (we stay under with 0.4s sleeps).
All network calls have retry logic and graceful degradation.

Outputs:
  1. Analysis/Results/paper_library/abstracts/  - one JSON per PMID
  2. Analysis/Results/paper_library/fulltext/   - one JSON per PMCID (OA only)
  3. Analysis/Results/paper_library/index.json  - master index of all papers
  4. Console progress report

This script is designed to run as part of the daily build suite.
On subsequent runs it skips papers already fetched (incremental mode).
"""

import os
import re
import json
import time
import sys
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import quote_plus

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
results_dir = os.path.join(base_dir, 'Analysis', 'Results')
library_dir = os.path.join(results_dir, 'paper_library')
abstracts_dir = os.path.join(library_dir, 'abstracts')
fulltext_dir = os.path.join(library_dir, 'fulltext')

for d in [library_dir, abstracts_dir, fulltext_dir]:
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------
EUTILS_BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
EFETCH_URL = EUTILS_BASE + '/efetch.fcgi'
ESUMMARY_URL = EUTILS_BASE + '/esummary.fcgi'
ID_CONVERTER_URL = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/'
BIOC_BASE = 'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json'
OA_SERVICE_URL = 'https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi'

REQUEST_DELAY = 0.4  # seconds between API calls (stay under 3/sec)
BATCH_SIZE = 50      # PMIDs per EFetch batch request
MAX_RETRIES = 3

USER_AGENT = 'DiabetesResearchHub/1.0 (research; mailto:justin.bottum@gmail.com)'


def api_request(url, retries=MAX_RETRIES):
    """Make an HTTP GET request with retries and rate limiting."""
    for attempt in range(retries):
        try:
            req = Request(url, headers={'User-Agent': USER_AGENT})
            with urlopen(req, timeout=30) as resp:
                return resp.read().decode('utf-8')
        except HTTPError as e:
            if e.code == 429:
                wait = 2 ** (attempt + 1)
                print(f'    Rate limited (429), waiting {wait}s...'.encode('ascii', 'replace').decode('ascii'))
                time.sleep(wait)
                continue
            elif e.code >= 500:
                time.sleep(1)
                continue
            else:
                return None
        except (URLError, OSError, TimeoutError):
            time.sleep(1)
            continue
    return None


# ---------------------------------------------------------------------------
# Stage 1: Load verified PMIDs
# ---------------------------------------------------------------------------
def load_verified_pmids():
    """Load the list of verified PMIDs from the verification results."""
    json_path = os.path.join(results_dir, 'pmid_verification.json')
    if not os.path.exists(json_path):
        print('  ERROR: pmid_verification.json not found. Run verify_pmids.py first.')
        return {}
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Only include PMIDs that were verified as existing
    verified = {}
    for pmid, info in data.get('results', {}).items():
        if info.get('exists', False):
            verified[pmid] = {
                'title': info.get('title', ''),
                'authors': info.get('authors', ''),
                'journal': info.get('journal', ''),
                'year': info.get('year', ''),
                'doi': info.get('doi', ''),
                'locations': info.get('locations', [])
            }
    return verified


# ---------------------------------------------------------------------------
# Stage 2: Fetch abstracts in batches
# ---------------------------------------------------------------------------
def fetch_abstracts_batch(pmids):
    """Fetch abstracts for a batch of PMIDs using EFetch XML."""
    id_str = ','.join(pmids)
    url = f'{EFETCH_URL}?db=pubmed&id={id_str}&rettype=abstract&retmode=xml'
    xml_text = api_request(url)
    if not xml_text:
        return {}

    # Parse the XML to extract abstracts
    # We use simple regex parsing to avoid lxml dependency
    results = {}
    # Split into individual article blocks
    articles = re.findall(r'<PubmedArticle>(.*?)</PubmedArticle>', xml_text, re.DOTALL)
    for article in articles:
        # Extract PMID
        pmid_match = re.search(r'<PMID[^>]*>(\d+)</PMID>', article)
        if not pmid_match:
            continue
        pmid = pmid_match.group(1)

        # Extract title
        title_match = re.search(r'<ArticleTitle>(.*?)</ArticleTitle>', article, re.DOTALL)
        title = title_match.group(1).strip() if title_match else ''
        # Clean XML tags from title
        title = re.sub(r'<[^>]+>', '', title)

        # Extract abstract text (may have multiple AbstractText elements)
        abstract_parts = re.findall(
            r'<AbstractText[^>]*>(.*?)</AbstractText>', article, re.DOTALL
        )
        abstract = ' '.join(re.sub(r'<[^>]+>', '', part).strip() for part in abstract_parts)

        # Extract keywords
        keywords = re.findall(r'<Keyword[^>]*>(.*?)</Keyword>', article, re.DOTALL)
        keywords = [re.sub(r'<[^>]+>', '', kw).strip() for kw in keywords]

        # Extract MeSH terms
        mesh_terms = re.findall(r'<DescriptorName[^>]*>(.*?)</DescriptorName>', article, re.DOTALL)
        mesh_terms = [re.sub(r'<[^>]+>', '', m).strip() for m in mesh_terms]

        # Extract publication type
        pub_types = re.findall(r'<PublicationType[^>]*>(.*?)</PublicationType>', article, re.DOTALL)
        pub_types = [re.sub(r'<[^>]+>', '', pt).strip() for pt in pub_types]

        # Extract DOI
        doi_match = re.search(r'<ArticleId IdType="doi">(.*?)</ArticleId>', article)
        doi = doi_match.group(1).strip() if doi_match else ''

        # Extract journal
        journal_match = re.search(r'<ISOAbbreviation>(.*?)</ISOAbbreviation>', article)
        journal = journal_match.group(1).strip() if journal_match else ''

        # Extract year
        year_match = re.search(r'<PubDate>.*?<Year>(\d{4})</Year>', article, re.DOTALL)
        year = year_match.group(1) if year_match else ''

        # Extract all author names
        author_blocks = re.findall(r'<Author[^>]*>(.*?)</Author>', article, re.DOTALL)
        authors = []
        for ab in author_blocks:
            last = re.search(r'<LastName>(.*?)</LastName>', ab)
            first = re.search(r'<ForeName>(.*?)</ForeName>', ab)
            if last:
                name = last.group(1)
                if first:
                    name += ' ' + first.group(1)[0]  # last + first initial
                authors.append(name)

        # Extract references cited by this paper
        ref_pmids = re.findall(r'<ArticleId IdType="pubmed">(\d+)</ArticleId>', article)
        # The first match is the article's own PMID in some contexts, filter it
        cited_pmids = [r for r in ref_pmids if r != pmid]

        results[pmid] = {
            'pmid': pmid,
            'title': title,
            'abstract': abstract,
            'keywords': keywords,
            'mesh_terms': mesh_terms,
            'pub_types': pub_types,
            'doi': doi,
            'journal': journal,
            'year': year,
            'authors': authors,
            'cited_pmids': cited_pmids,
            'fetched_at': datetime.now().isoformat()
        }

    return results


def fetch_all_abstracts(pmids, existing_abstracts):
    """Fetch abstracts for all PMIDs, skipping already-fetched ones."""
    to_fetch = [p for p in pmids if p not in existing_abstracts]
    if not to_fetch:
        print(f'  All {len(pmids)} abstracts already fetched (incremental mode).')
        return {}

    print(f'  Fetching abstracts for {len(to_fetch)} new PMIDs ({len(existing_abstracts)} cached)...')
    all_results = {}
    batches = [to_fetch[i:i+BATCH_SIZE] for i in range(0, len(to_fetch), BATCH_SIZE)]

    for batch_num, batch in enumerate(batches, 1):
        print(f'    Batch {batch_num}/{len(batches)} ({len(batch)} PMIDs)...')
        results = fetch_abstracts_batch(batch)
        all_results.update(results)

        # Save each abstract individually
        for pmid, data in results.items():
            fpath = os.path.join(abstracts_dir, f'{pmid}.json')
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        if batch_num < len(batches):
            time.sleep(REQUEST_DELAY)

    # Report any PMIDs we couldn't fetch
    missing = set(to_fetch) - set(all_results.keys())
    if missing:
        print(f'    Warning: Could not fetch abstracts for {len(missing)} PMIDs: {sorted(missing)[:5]}...')

    return all_results


# ---------------------------------------------------------------------------
# Stage 3: Convert PMIDs to PMCIDs
# ---------------------------------------------------------------------------
def convert_pmids_to_pmcids(pmids):
    """Use NCBI ID Converter to find PMCIDs for our PMIDs."""
    pmcid_map = {}  # pmid -> pmcid
    batches = [pmids[i:i+200] for i in range(0, len(pmids), 200)]

    for batch_num, batch in enumerate(batches, 1):
        id_str = ','.join(batch)
        url = f'{ID_CONVERTER_URL}?ids={id_str}&format=json&tool=DiabetesResearchHub&email=justin.bottum@gmail.com'
        resp = api_request(url)
        if not resp:
            continue

        try:
            data = json.loads(resp)
            for record in data.get('records', []):
                pmid = record.get('pmid', '')
                pmcid = record.get('pmcid', '')
                if pmid and pmcid:
                    pmcid_map[pmid] = pmcid
        except (json.JSONDecodeError, KeyError):
            pass

        if batch_num < len(batches):
            time.sleep(REQUEST_DELAY)

    return pmcid_map


# ---------------------------------------------------------------------------
# Stage 4: Fetch full text from PMC BioC API
# ---------------------------------------------------------------------------
def fetch_fulltext(pmcid):
    """Fetch structured full text for a single PMCID via BioC JSON API."""
    url = f'{BIOC_BASE}/{pmcid}/unicode'
    resp = api_request(url)
    if not resp:
        return None

    try:
        data = json.loads(resp)
    except json.JSONDecodeError:
        return None

    # Extract structured sections from BioC format
    sections = []
    for doc in data if isinstance(data, list) else [data]:
        for passage_source in _get_passages(doc):
            section_type = ''
            text = ''
            for annot in passage_source.get('infons', {}).items():
                if annot[0] == 'section_type':
                    section_type = annot[1]
                elif annot[0] == 'type' and not section_type:
                    section_type = annot[1]
            text = passage_source.get('text', '')
            if text.strip():
                sections.append({
                    'section_type': section_type,
                    'text': text.strip()
                })

    return {
        'pmcid': pmcid,
        'sections': sections,
        'fetched_at': datetime.now().isoformat()
    }


def _get_passages(doc):
    """Recursively extract passages from BioC JSON structure."""
    passages = []
    if isinstance(doc, dict):
        if 'passages' in doc:
            passages.extend(doc['passages'])
        if 'documents' in doc:
            for d in doc['documents']:
                passages.extend(_get_passages(d))
    return passages


def fetch_all_fulltext(pmcid_map, existing_fulltext):
    """Fetch full text for all available PMCIDs, skipping cached."""
    to_fetch = {pmid: pmcid for pmid, pmcid in pmcid_map.items()
                if pmcid not in existing_fulltext}

    if not to_fetch:
        print(f'  All {len(pmcid_map)} full texts already fetched (incremental mode).')
        return {}

    print(f'  Fetching full text for {len(to_fetch)} PMC Open Access papers ({len(existing_fulltext)} cached)...')
    all_results = {}
    items = list(to_fetch.items())

    for i, (pmid, pmcid) in enumerate(items, 1):
        if i % 10 == 0 or i == len(items):
            print(f'    Progress: {i}/{len(items)}...')

        result = fetch_fulltext(pmcid)
        if result:
            result['pmid'] = pmid
            all_results[pmcid] = result

            fpath = os.path.join(fulltext_dir, f'{pmcid}.json')
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

        time.sleep(REQUEST_DELAY)

    return all_results


# ---------------------------------------------------------------------------
# Stage 5: Build master index
# ---------------------------------------------------------------------------
def build_index(verified_pmids, abstract_data, pmcid_map, fulltext_pmcids):
    """Build the master paper library index with cross-references."""
    index = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_pmids': len(verified_pmids),
            'abstracts_fetched': 0,
            'pmc_available': len(pmcid_map),
            'fulltext_fetched': len(fulltext_pmcids),
        },
        'papers': {},
        'cross_references': {
            'papers_citing_each_other': {},
            'shared_mesh_terms': {}
        }
    }

    # Load all abstract files to build complete picture
    abstract_count = 0
    all_mesh = {}  # mesh_term -> list of pmids

    for pmid in sorted(verified_pmids.keys()):
        paper = {
            'pmid': pmid,
            'title': verified_pmids[pmid]['title'],
            'journal': verified_pmids[pmid]['journal'],
            'year': verified_pmids[pmid]['year'],
            'doi': verified_pmids[pmid]['doi'],
            'has_abstract': False,
            'has_fulltext': False,
            'pmcid': pmcid_map.get(pmid, ''),
            'dashboard_locations': verified_pmids[pmid].get('locations', []),
        }

        # Check if abstract exists
        abs_path = os.path.join(abstracts_dir, f'{pmid}.json')
        if os.path.exists(abs_path):
            paper['has_abstract'] = True
            abstract_count += 1
            try:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    abs_data = json.load(f)
                paper['mesh_terms'] = abs_data.get('mesh_terms', [])
                paper['keywords'] = abs_data.get('keywords', [])
                paper['pub_types'] = abs_data.get('pub_types', [])
                paper['cited_pmids_in_hub'] = [
                    p for p in abs_data.get('cited_pmids', [])
                    if p in verified_pmids
                ]
                paper['abstract_length'] = len(abs_data.get('abstract', ''))

                # Track mesh terms for cross-referencing
                for mesh in abs_data.get('mesh_terms', []):
                    if mesh not in all_mesh:
                        all_mesh[mesh] = []
                    all_mesh[mesh].append(pmid)
            except (json.JSONDecodeError, KeyError):
                pass

        # Check if full text exists
        pmcid = pmcid_map.get(pmid, '')
        if pmcid:
            ft_path = os.path.join(fulltext_dir, f'{pmcid}.json')
            if os.path.exists(ft_path):
                paper['has_fulltext'] = True
                try:
                    with open(ft_path, 'r', encoding='utf-8') as f:
                        ft_data = json.load(f)
                    paper['fulltext_sections'] = len(ft_data.get('sections', []))
                    paper['fulltext_chars'] = sum(
                        len(s.get('text', '')) for s in ft_data.get('sections', [])
                    )
                except (json.JSONDecodeError, KeyError):
                    pass

        index['papers'][pmid] = paper

    index['metadata']['abstracts_fetched'] = abstract_count

    # Build cross-references: papers that cite each other within our hub
    citations_within = {}
    for pmid, paper in index['papers'].items():
        cited = paper.get('cited_pmids_in_hub', [])
        if cited:
            citations_within[pmid] = cited
    index['cross_references']['papers_citing_each_other'] = citations_within

    # Build shared MeSH term clusters (terms shared by 3+ papers)
    shared_mesh = {
        term: pmid_list for term, pmid_list in all_mesh.items()
        if len(pmid_list) >= 3
    }
    index['cross_references']['shared_mesh_terms'] = shared_mesh

    # Save index
    index_path = os.path.join(library_dir, 'index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    return index


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print('Paper Ingestion Pipeline')
    print('=' * 60)
    start_time = time.time()

    # Stage 1: Load verified PMIDs
    print('\n  Stage 1: Loading verified PMIDs...')
    verified = load_verified_pmids()
    if not verified:
        print('  No verified PMIDs found. Exiting.')
        return 1
    print(f'  Found {len(verified)} verified PMIDs.')

    # Check what we already have cached
    existing_abstracts = set()
    for fname in os.listdir(abstracts_dir):
        if fname.endswith('.json'):
            existing_abstracts.add(fname.replace('.json', ''))

    existing_fulltext = set()
    for fname in os.listdir(fulltext_dir):
        if fname.endswith('.json'):
            existing_fulltext.add(fname.replace('.json', ''))

    # Stage 2: Fetch abstracts
    print('\n  Stage 2: Fetching abstracts via EFetch API...')
    pmid_list = sorted(verified.keys())
    new_abstracts = fetch_all_abstracts(pmid_list, existing_abstracts)
    total_abstracts = len(existing_abstracts) + len(new_abstracts)
    print(f'  Abstracts available: {total_abstracts}/{len(verified)}')

    # Stage 3: Convert PMIDs to PMCIDs
    print('\n  Stage 3: Converting PMIDs to PMCIDs...')
    pmcid_map = convert_pmids_to_pmcids(pmid_list)
    print(f'  PMC papers found: {len(pmcid_map)}/{len(verified)}')

    # Stage 4: Fetch full text for OA papers
    print('\n  Stage 4: Fetching full text from PMC Open Access...')
    new_fulltext = fetch_all_fulltext(pmcid_map, existing_fulltext)
    total_fulltext = len(existing_fulltext) + len(new_fulltext)
    print(f'  Full text available: {total_fulltext}/{len(pmcid_map)} PMC papers')

    # Stage 5: Build master index
    print('\n  Stage 5: Building master paper library index...')
    index = build_index(verified, new_abstracts, pmcid_map, existing_fulltext | set(new_fulltext.keys()))

    # Summary
    elapsed = time.time() - start_time
    meta = index['metadata']
    cross = index['cross_references']
    citations_count = sum(len(v) for v in cross.get('papers_citing_each_other', {}).values())
    mesh_clusters = len(cross.get('shared_mesh_terms', {}))

    print('\n' + '=' * 60)
    print('  Paper Library Summary')
    print('  ' + '-' * 40)
    print(f'  Total papers:          {meta["total_pmids"]}')
    print(f'  Abstracts fetched:     {meta["abstracts_fetched"]}')
    print(f'  PMC available:         {meta["pmc_available"]}')
    print(f'  Full text fetched:     {meta["fulltext_fetched"]}')
    print(f'  Cross-citations found: {citations_count}')
    print(f'  Shared MeSH clusters:  {mesh_clusters}')
    print(f'  Elapsed time:          {elapsed:.1f}s')
    print(f'  Library path:          {library_dir}')
    print(f'\n  Paper Ingestion Pipeline: complete')

    return 0


if __name__ == '__main__':
    sys.exit(main())
