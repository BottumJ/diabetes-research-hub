#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PMID Fixer — searches PubMed for the correct PMID when a mismatch is detected.
Uses NCBI E-utilities esearch to find papers by title/author keywords.
"""

import json
import time
from urllib.request import urlopen, Request
from urllib.parse import quote_plus

EUTILS_BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'

def search_pubmed(query, max_results=5):
    """Search PubMed and return list of {pmid, title, authors, year, journal}."""
    url = f'{EUTILS_BASE}/esearch.fcgi?db=pubmed&term={quote_plus(query)}&retmax={max_results}&retmode=json'
    req = Request(url, headers={'User-Agent': 'DiabetesResearchHub/1.0 (justin.bottum@gmail.com)'})
    with urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode('utf-8'))

    pmids = data.get('esearchresult', {}).get('idlist', [])
    if not pmids:
        return []

    time.sleep(0.4)

    # Get summaries
    ids_str = ','.join(pmids)
    url2 = f'{EUTILS_BASE}/esummary.fcgi?db=pubmed&id={ids_str}&retmode=json'
    req2 = Request(url2, headers={'User-Agent': 'DiabetesResearchHub/1.0 (justin.bottum@gmail.com)'})
    with urlopen(req2, timeout=30) as response2:
        data2 = json.loads(response2.read().decode('utf-8'))

    results = []
    for pmid in pmids:
        entry = data2.get('result', {}).get(pmid, {})
        if 'error' in entry:
            continue
        authors_list = entry.get('authors', [])
        first_author = authors_list[0].get('name', '') if authors_list else ''
        results.append({
            'pmid': pmid,
            'title': entry.get('title', ''),
            'authors': first_author,
            'year': entry.get('pubdate', '')[:4],
            'journal': entry.get('source', '')
        })
    return results


# Searches for each mismatched PMID
SEARCHES = [
    # Generic Drug Catalog mismatches
    ('Verapamil beta cell TXNIP type 1 diabetes RCT', 'Verapamil T1D - should be Ovalle et al. or Xu et al.'),
    ('hydroxychloroquine type 2 diabetes HbA1c meta-analysis', 'HCQ in T2D meta-analysis'),
    ('dapsone anti-inflammatory beta cell diabetes', 'Dapsone diabetes'),
    ('pentoxifylline diabetic nephropathy proteinuria meta-analysis', 'Pentoxifylline DKD meta-analysis'),
    ('doxycycline MMP inhibition diabetic retinopathy', 'Doxycycline MMP diabetes'),
    ('N-acetylcysteine insulin sensitivity diabetes oxidative stress', 'NAC diabetes'),
    ('alpha lipoic acid diabetic neuropathy NATHAN trial', 'Alpha-lipoic acid NATHAN 1'),
    ('nicotinamide ENDIT trial type 1 diabetes prevention', 'ENDIT trial nicotinamide'),
    ('minocycline neuroprotective diabetic neuropathy', 'Minocycline diabetic neuropathy'),
    ('allopurinol renal protection diabetes kidney', 'Allopurinol CKD diabetes'),
    ('losartan RENAAL trial diabetic nephropathy', 'RENAAL trial'),
    ('atorvastatin CARDS trial type 2 diabetes cardiovascular', 'CARDS trial'),
    ('fenofibrate FIELD trial diabetic retinopathy', 'FIELD trial fenofibrate'),
    # Health Equity dashboard mismatches
    ('clinical trial diversity type 1 diabetes race ethnicity representation', 'T1D trial diversity'),
    ('global distribution diabetes clinical trials low middle income', 'Global diabetes trial distribution'),
    ('ADA health equity position statement diabetes disparities', 'ADA health equity'),
    ('social determinants diabetes outcomes race', 'Social determinants diabetes'),
    ('racial disparities diabetes technology CGM insulin pump', 'Diabetes tech disparities'),
]

if __name__ == '__main__':
    print("PubMed Search for Correct PMIDs")
    print("=" * 70)

    for query, label in SEARCHES:
        print(f"\n  {label}")
        print(f"  Query: {query}")
        results = search_pubmed(query)
        for r in results:
            print(f"    PMID:{r['pmid']} | {r['authors']} ({r['year']}) | {r['title'][:80]}")
        time.sleep(0.5)
