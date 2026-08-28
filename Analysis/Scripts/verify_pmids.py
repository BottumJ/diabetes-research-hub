#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PMID Verification Tool
Scans all dashboard build scripts for PMIDs, then queries the NCBI PubMed API
to verify each one exists and reports what paper it actually points to.

Outputs:
  1. Console report showing PASS/FAIL/MISMATCH for each PMID
  2. HTML verification report at Dashboards/PMID_Verification.html
  3. JSON results at Analysis/Results/pmid_verification.json

Usage:
  python verify_pmids.py           # verify all PMIDs
  python verify_pmids.py --fix     # (future) auto-fix known mismatches
"""

import os
import re
import json
import time
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
output_dir = os.path.join(base_dir, 'Dashboards')
results_dir = os.path.join(base_dir, 'Analysis', 'Results')
os.makedirs(output_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

# NCBI E-utilities base URL
EUTILS_BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'

def find_all_pmids():
    """Scan all Python build scripts and HTML dashboards for PMIDs."""
    pmid_locations = {}  # pmid -> list of {file, line, context}

    # Scan Python scripts
    for fname in os.listdir(script_dir):
        if not fname.endswith('.py'):
            continue
        fpath = os.path.join(script_dir, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue

        for i, line in enumerate(lines, 1):
            # Skip pure comment lines to avoid false positives from examples
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            # Match PMID patterns in code and HTML strings
            matches = re.findall(r'(?:PMID[:\s]*|key_pmids[\'\"]\s*:\s*[\'\"])(\d{7,8})', line, re.IGNORECASE)
            if not matches:
                # Also catch pmid references in HTML strings
                matches = re.findall(r'PMID[:\s]+(\d{7,8})', line, re.IGNORECASE)

            for pmid in matches:
                if pmid not in pmid_locations:
                    pmid_locations[pmid] = []
                context = line.strip()[:120]
                pmid_locations[pmid].append({
                    'file': fname,
                    'line': i,
                    'context': context
                })

    return pmid_locations


def verify_pmid_batch(pmids):
    """Query NCBI E-utilities to verify a batch of PMIDs.
    Returns dict of pmid -> {exists, title, authors, journal, year, doi}
    """
    results = {}

    # Process in batches of 20 (NCBI rate limit friendly)
    pmid_list = list(pmids)
    batch_size = 20

    for batch_start in range(0, len(pmid_list), batch_size):
        batch = pmid_list[batch_start:batch_start + batch_size]
        ids_str = ','.join(batch)

        url = f'{EUTILS_BASE}/esummary.fcgi?db=pubmed&id={ids_str}&retmode=json'

        try:
            req = Request(url, headers={'User-Agent': 'DiabetesResearchHub/1.0 (justin.bottum@gmail.com)'})
            with urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
        except (URLError, HTTPError, Exception) as e:
            print(f"  API error for batch starting {batch[0]}: {e}")
            for pmid in batch:
                results[pmid] = {
                    'exists': None,
                    'error': str(e),
                    'title': '',
                    'authors': '',
                    'journal': '',
                    'year': '',
                    'doi': ''
                }
            continue

        result_data = data.get('result', {})

        for pmid in batch:
            if pmid in result_data and 'error' not in result_data[pmid]:
                entry = result_data[pmid]
                authors_list = entry.get('authors', [])
                first_author = authors_list[0].get('name', '') if authors_list else 'Unknown'

                # Extract DOI from articleids
                doi = ''
                for aid in entry.get('articleids', []):
                    if aid.get('idtype') == 'doi':
                        doi = aid.get('value', '')
                        break

                results[pmid] = {
                    'exists': True,
                    'title': entry.get('title', ''),
                    'authors': first_author,
                    'journal': entry.get('source', ''),
                    'year': entry.get('pubdate', '')[:4],
                    'doi': doi,
                    'error': ''
                }
            else:
                error_msg = ''
                if pmid in result_data and 'error' in result_data[pmid]:
                    error_msg = result_data[pmid]['error']
                results[pmid] = {
                    'exists': False,
                    'error': error_msg or 'PMID not found in PubMed',
                    'title': '',
                    'authors': '',
                    'journal': '',
                    'year': '',
                    'doi': ''
                }

        # Rate limit: NCBI asks for max 3 requests/second without API key
        if batch_start + batch_size < len(pmid_list):
            time.sleep(0.5)

    return results


def generate_html_report(pmid_locations, verification_results, output_path):
    """Generate an HTML verification report."""

    total = len(verification_results)
    verified = sum(1 for v in verification_results.values() if v.get('exists') is True)
    failed = sum(1 for v in verification_results.values() if v.get('exists') is False)
    errors = sum(1 for v in verification_results.values() if v.get('exists') is None)

    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    # ADJUDICATED OFF-TOPIC VERDICTS (added 2026-08-23).
    #
    # Until today this table rendered a green "VERIFIED" badge next to
    # "Recent advances in probiotic breads; a market trend in the functional
    # bakery products" - a paper this repository had ALREADY adjudicated, on
    # 2026-08-20, as an off-topic citation wrongly standing in for the PROTECT
    # teplizumab trial. The badge was not lying by its own definition: here
    # VERIFIED has only ever meant "this PMID resolves". But the page said so in
    # a footnote 24,000 characters below the row, and a reader scanning a green
    # column does not read footers.
    #
    # Presence is not correctness. That sentence is written in three scripts in
    # this repo and was still being contradicted by the published page. So the
    # verdict is now JOINED IN and the label states what was actually checked.
    offtopic = {}
    _reg = os.path.join(results_dir, 'adjudicated_offtopic_pmids.json')
    if os.path.exists(_reg):
        try:
            with open(_reg, encoding='utf-8') as _f:
                offtopic = json.load(_f).get('pmids', {})
        except Exception as _e:
            print(f'  WARNING: could not load adjudicated off-topic registry: {_e}')
    print(f'  Adjudicated off-topic PMIDs loaded: {len(offtopic)}')

    # NOT-A-CORPUS-PAPER VERDICTS (added 2026-08-24).
    #
    # Same defect shape as the off-topic join above, one layer further out.
    # PMID 12345678 ("Denpasar Declaration on Population and Development",
    # Integration 1994) rendered here as a green RESOLVES row. It does resolve.
    # It is also not a citation at all: it was harvested from the comment
    # `# match PMID: 12345678` beside a regex in postprocess_dashboards.py. It
    # was purged from the paper library index today, but this page does not read
    # the index - it scans scripts for PMID literals - so purging the index left
    # the row standing. A verdict is only as good as the surfaces that join it.
    # Rewired 2026-08-28 to corpus_membership. This page scans SCRIPTS for
    # PMID literals rather than reading the index, which is exactly why it
    # needed its own guard - and why reading only not_corpus_pmids.json left
    # it rendering 17 adjudicated-off-topic papers as ordinary RESOLVES rows.
    # The reason dict now carries the CLASS, so OFF_TOPIC and BACKGROUND can
    # be rendered as the different things they are instead of collapsing into
    # "NOT CORPUS", which would have said "never was a corpus paper" about a
    # correctly-cited TGF-beta definition.
    import corpus_membership
    not_corpus = {p: corpus_membership.reason(p)
                  for p in corpus_membership.excluded_pmids()}
    _by = {}
    for _r in not_corpus.values():
        _by[_r['code']] = _by.get(_r['code'], 0) + 1
    print('  Excluded PMIDs loaded: %d (%s)'
          % (len(not_corpus), ', '.join('%s=%d' % kv for kv in sorted(_by.items()))))

    # Build table rows
    rows = ''
    for pmid in sorted(verification_results.keys(), key=lambda x: int(x)):
        v = verification_results[pmid]
        locs = pmid_locations.get(pmid, [])
        files_list = ', '.join(set(l['file'] for l in locs))

        if v.get('exists') is True and pmid in not_corpus \
                and (not_corpus[pmid] or {}).get('provenance') == 'RETRACTED':
            # A retraction is NOT the same fact as "never was a corpus paper",
            # and rendering it as NOT CORPUS would hide the more serious one.
            # This paper WAS cited as evidence and the literature withdrew it.
            # It gets its own colour so a reader cannot mistake exclusion-for-
            # provenance for exclusion-for-retraction.
            status = 'RETRACTED'
            status_color = '#b71c1c'
            status_bg = '#ffcdd2'
        elif v.get('exists') is True and pmid in not_corpus \
                and (not_corpus[pmid] or {}).get('code') == 'BACKGROUND':
            # Added 2026-08-28. Resolves, is cited CORRECTLY, and supplies no
            # diabetes finding - definitional, methodological or preclinical
            # context. Rendering this as NOT CORPUS would assert "never was a
            # corpus paper" about a true citation; rendering it as RESOLVES
            # would let a reader count it as evidence. It is neither.
            status = 'BACKGROUND'
            status_color = '#8d6e00'
            status_bg = '#fff8e1'
        elif v.get('exists') is True and pmid in not_corpus:
            # Resolves, but is not a corpus paper and never was: no claim in
            # this repository rests on it. Rendering it green implied the
            # opposite.
            status = 'NOT CORPUS'
            status_color = '#6a1b9a'
            status_bg = '#f3e5f5'
        elif v.get('exists') is True and pmid in offtopic:
            # Resolves, but adjudicated as attached to the wrong claim. This is
            # strictly worse than NOT FOUND: a dead PMID gets fixed, a live one
            # cited for something it does not say gets believed.
            status = 'OFF-TOPIC'
            status_color = '#c62828'
            status_bg = '#ffebee'
        elif v.get('exists') is True:
            status = 'RESOLVES'
            status_color = '#2d7d46'
            status_bg = '#e8f5e9'
        elif v.get('exists') is False:
            status = 'NOT FOUND'
            status_color = '#c62828'
            status_bg = '#ffebee'
        else:
            status = 'API ERROR'
            status_color = '#8b6914'
            status_bg = '#fff8e1'

        title = v.get('title', '') or v.get('error', '')
        if len(title) > 100:
            title = title[:97] + '...'

        rows += f'''
            <tr>
                <td><a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank" style="color:#2c5f8a;font-family:'SF Mono','Consolas',monospace;">{pmid}</a></td>
                <td style="background:{status_bg};color:{status_color};font-weight:600;text-align:center;">{status}</td>
                <td>{v.get("authors", "")}</td>
                <td>{title}</td>
                <td>{v.get("journal", "")}</td>
                <td>{v.get("year", "")}</td>
                <td style="font-size:0.85em;color:#636363;">{files_list}</td>
            </tr>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PMID Verification Report | Diabetes Research Hub</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif;
            background-color: #fafaf7;
            color: #1a1a1a;
            line-height: 1.6;
            padding: 20px;
        }}
        .header {{
            max-width: 1400px;
            margin: 0 auto 30px;
            border-bottom: 1px solid #e0ddd5;
            padding-bottom: 20px;
        }}
        h1 {{
            font-family: Georgia, serif;
            font-size: 2em;
            font-weight: normal;
            margin-bottom: 8px;
        }}
        .tagline {{
            font-size: 0.95em;
            color: #636363;
            font-style: italic;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        .stat-box {{
            background: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 15px 20px;
            font-family: "SF Mono", "Consolas", monospace;
        }}
        .stat-number {{
            font-size: 1.6em;
            font-weight: bold;
            display: block;
        }}
        .stat-label {{
            font-size: 0.85em;
            color: #636363;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            margin: 20px 0;
            font-size: 0.9em;
        }}
        th {{
            background: #ffffff;
            border-bottom: 2px solid #e0ddd5;
            padding: 10px 8px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            border-bottom: 1px solid #e0ddd5;
            padding: 10px 8px;
        }}
        tr:hover {{ background: #fafaf7; }}
        .filter-row {{
            margin: 15px 0;
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        .filter-btn {{
            padding: 8px 16px;
            border: 1px solid #e0ddd5;
            background: #ffffff;
            cursor: pointer;
            font-family: inherit;
            font-size: 0.9em;
        }}
        .filter-btn.active {{
            background: #2c5f8a;
            color: #ffffff;
            border-color: #2c5f8a;
        }}
        #searchBox {{
            padding: 8px 12px;
            border: 1px solid #e0ddd5;
            font-size: 0.9em;
            width: 250px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 15px;
            border-top: 1px solid #e0ddd5;
            font-size: 0.85em;
            color: #636363;
            text-align: center;
        }}
    </style>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-JGMD5VRYPH');</script>
</head>
<body>
<div style="background:#ffffff;border-bottom:1px solid #e0ddd5;padding:8px 20px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:13px;display:flex;gap:16px;align-items:center;flex-wrap:wrap;">
  <a href="../index.html" style="color:#2c5f8a;text-decoration:none;font-weight:600;">&larr; Diabetes Research Hub</a>
  <span style="color:#e0ddd5;">|</span>
  <a href="Research_Dashboard.html" style="color:#636363;text-decoration:none;">Research</a>
  <a href="Clinical_Trial_Dashboard.html" style="color:#636363;text-decoration:none;">Trials</a>
  <a href="Gap_Deep_Dives.html" style="color:#636363;text-decoration:none;">Gaps</a>
  <a href="Gap_Synthesis.html" style="color:#636363;text-decoration:none;">Synthesis</a>
  <a href="Equity_Map.html" style="color:#636363;text-decoration:none;">Equity</a>
  <a href="Medical_Data_Dictionary.html" style="color:#636363;text-decoration:none;">Dictionary</a>
  <a href="Acronym_Database.html" style="color:#636363;text-decoration:none;">Acronyms</a>
</div>

<div class="header">
    <h1>PMID Verification Report</h1>
    <p class="tagline">Automated citation verification against NCBI PubMed — Last run: {now}</p>
</div>

<div class="container">
    <div class="stats">
        <div class="stat-box">
            <span class="stat-number">{total}</span>
            <span class="stat-label">Total PMIDs</span>
        </div>
        <div class="stat-box">
            <span class="stat-number" style="color:#2d7d46;">{verified}</span>
            <span class="stat-label">Verified</span>
        </div>
        <div class="stat-box">
            <span class="stat-number" style="color:#c62828;">{failed}</span>
            <span class="stat-label">Not Found</span>
        </div>
        <div class="stat-box">
            <span class="stat-number" style="color:#8b6914;">{errors}</span>
            <span class="stat-label">API Errors</span>
        </div>
        <div class="stat-box">
            <span class="stat-number">{len(pmid_locations)}</span>
            <span class="stat-label">Source Files</span>
        </div>
    </div>

    <div class="filter-row">
        <button class="filter-btn active" onclick="filterTable('all')">All</button>
        <button class="filter-btn" onclick="filterTable('RESOLVES')">Resolves</button>
        <button class="filter-btn" onclick="filterTable('OFF-TOPIC')">Off-topic</button>
        <button class="filter-btn" onclick="filterTable('NOT CORPUS')">Not corpus</button>
        <button class="filter-btn" onclick="filterTable('NOT FOUND')">Not Found</button>
        <button class="filter-btn" onclick="filterTable('API ERROR')">API Errors</button>
        <input type="text" id="searchBox" placeholder="Search by PMID, title, author..." oninput="searchTable()">
    </div>

    <table id="pmidTable">
        <thead>
            <tr>
                <th>PMID</th>
                <th>Status</th>
                <th>First Author</th>
                <th>Title</th>
                <th>Journal</th>
                <th>Year</th>
                <th>Used In</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>

    <p style="margin-top:20px;font-size:0.9em;color:#636363;">
        <strong>What this checks:</strong> Each PMID is queried against the NCBI PubMed database via E-utilities API.
        "RESOLVES" means only that the PMID returns a real record from PubMed. It does NOT confirm that the
        paper supports the claim it is cited for. "NOT CORPUS" means the PMID resolves but is not a corpus
        paper at all - it was harvested from a code comment or exists here only because this repository
        documented it as a bad citation; no claim rests on it. "RETRACTED" is a different and more serious
        finding: the paper resolves, is on-topic, has a correct title, and WAS cited as evidence here — the
        journal has withdrawn it. PubMed's publication type is the source; see retraction_audit.json.
        Note that a retracted paper passes every other check on this page by construction, which is why
        audit_retractions.py exists. "OFF-TOPIC" means the PMID resolves but this repository has
        adjudicated it as attached to the wrong claim — see citation_identifier_audit.json.
        Click any PMID to open it on PubMed for manual verification.
    </p>

    <p style="margin-top:10px;font-size:0.9em;color:#636363;">
        <strong>To re-run this verification:</strong> <code style="background:#f0ede6;padding:2px 6px;">python Analysis/Scripts/verify_pmids.py</code>
    </p>
</div>

<div class="footer">
    <p>PMID Verification Report | Diabetes Research Hub | Generated {now}</p>
</div>

<script>
function filterTable(status) {{
    const rows = document.querySelectorAll('#pmidTable tbody tr');
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');

    rows.forEach(row => {{
        if (status === 'all') {{
            row.style.display = '';
        }} else {{
            const cellText = row.cells[1].textContent.trim();
            row.style.display = cellText === status ? '' : 'none';
        }}
    }});
}}

function searchTable() {{
    const term = document.getElementById('searchBox').value.toLowerCase();
    const rows = document.querySelectorAll('#pmidTable tbody tr');
    rows.forEach(row => {{
        row.style.display = row.textContent.toLowerCase().includes(term) ? '' : 'none';
    }});
}}
</script>
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    print("PMID Verification Tool")
    print("=" * 60)

    # Step 1: Find all PMIDs in source files
    print("  [1/4] Scanning build scripts for PMIDs...")
    pmid_locations = find_all_pmids()
    print(f"         Found {len(pmid_locations)} unique PMIDs across {len(set(f for locs in pmid_locations.values() for f in [l['file'] for l in locs]))} files")

    # Step 2: Verify against PubMed API
    print("  [2/4] Querying NCBI PubMed API...")
    verification_results = verify_pmid_batch(pmid_locations.keys())

    verified = sum(1 for v in verification_results.values() if v.get('exists') is True)
    failed = sum(1 for v in verification_results.values() if v.get('exists') is False)
    errors = sum(1 for v in verification_results.values() if v.get('exists') is None)

    print(f"         Verified: {verified} | Not Found: {failed} | API Errors: {errors}")

    # Step 3: Generate HTML report
    print("  [3/4] Generating verification report...")
    html_path = os.path.join(output_dir, 'PMID_Verification.html')
    generate_html_report(pmid_locations, verification_results, html_path)
    print(f"         HTML report: {html_path}")

    # Step 4: Save JSON results
    print("  [4/4] Saving JSON results...")
    json_path = os.path.join(results_dir, 'pmid_verification.json')
    json_output = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total': len(verification_results),
            'verified': verified,
            'not_found': failed,
            'api_errors': errors
        },
        'results': {}
    }
    for pmid, v in verification_results.items():
        json_output['results'][pmid] = {
            **v,
            'locations': pmid_locations.get(pmid, [])
        }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2, ensure_ascii=False)
    print(f"         JSON results: {json_path}")

    # Console summary
    print()
    print("  RESULTS")
    print("  " + "-" * 56)

    for pmid in sorted(verification_results.keys(), key=lambda x: int(x)):
        v = verification_results[pmid]
        if v.get('exists') is True:
            status = "PASS"
            detail = f"{v['authors']} ({v['year']}) - {v['title'][:60]}".encode('ascii', 'replace').decode('ascii')
        elif v.get('exists') is False:
            status = "FAIL"
            detail = v.get('error', 'Not found')
        else:
            status = "ERR "
            detail = v.get('error', 'API error')

        files = ', '.join(set(l['file'] for l in pmid_locations.get(pmid, [])))
        print(f"  [{status}] PMID:{pmid} | {detail}")

    print()
    print(f"  PMID Verification: {os.path.getsize(html_path):,} bytes")

    if failed > 0:
        print(f"\n  WARNING: {failed} PMID(s) could not be verified. Review the report.")
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
