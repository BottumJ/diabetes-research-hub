#!/usr/bin/env python3
"""One-shot repair: the 2026-08-20 off-topic purge only cleaned `external_pmids`.

WHAT WAS FOUND (2026-08-23)
---------------------------
audit_citation_identifiers.py harvests citation identifiers from EVERY field of a
path record, not just the one structured list. It found that nine of the PMIDs
purged on 2026-08-20 as off-topic are still asserted as fact in NARRATIVE fields
(`notes`, `validation_notes`, `evidence_summary`, `external_evidence`) - the text
that gets read by a human and, in some cases, rendered. Purging the list left the
prose making the same false claim.

The clearest case: `teplizumab -> autoimmune` still reads

    "PROTECT phase 3 (Ramos et al. NEJM 2023, PMID 37889505, n=328 ...)"

37889505 is "Recent advances in probiotic breads; a market trend in the functional
bakery products". This is the exact citation the 2026-08-20 run reported as
corrected.

EVERY replacement below was resolved live against PubMed E-utilities in the same
run that wrote this file, by searching for the paper the prose DESCRIBES, and the
returned title was checked against that description. None was guessed. Two of the
guesses a human would most likely have made were wrong and are recorded here so
the next reader does not repeat them:

  Boussageon 2012 PLoS Med metformin  -> 22509138, NOT 22563304
  Edmonton protocol NEJM 2006         -> 17005949, NOT 16968130

Audit-trail fields (`citation_fixes`, `citation_repairs`, and correction notes
that say "was X") legitimately name the bad PMID and are NOT touched.
"""

import json
import os
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(BASE, 'Results', 'agent_state.json')
TOOL = {'tool': 'diabetes_research_hub', 'email': 'justin.bottum@gmail.com'}
ESUMMARY = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?'

# (store, path key, field, wrong pmid, right pmid, expected-title fragment, what the prose claims)
REPAIRS = [
    ('paths', 'teplizumab -> autoimmune', 'validation_notes', '37889505', '37861217',
     'teplizumab', 'PROTECT phase 3, Ramos NEJM 2023'),
    ('paths', 'teplizumab -> T1D', 'validation_notes', '37865119', '37861217',
     'teplizumab', 'PROTECT NEJM 2023'),
    ('paths', 'metformin -> inflammation', 'notes', '32398655', '32194991',
     'keratinocytes', 'metformin IL-1beta suppression, Cell Death Discov 2020'),
    ('paths', 'metformin -> inflammation', 'notes', '34107285', '34115964',
     'NLRP3 inflammasome', 'metformin mtDNA/ATP-dependent NLRP3, Immunity 2021'),
    ('paths', 'metformin -> cardiovascular', 'validation_notes', '22473097', '22509138',
     'metformin', 'Boussageon 2012 PLoS Med metformin reappraisal'),
    ('paths', 'pioglitazone -> inflammation', 'notes', '19136609', '18755353',
     'pioglitazone', 'pioglitazone represses inflammation via PPAR-gamma (PMC2633943)'),
    ('paths', 'rapamycin -> islet_transplant', 'notes', '16968130', '17005949',
     'Edmonton protocol', 'Edmonton protocol NEJM 2006 international trial'),
    ('paths', 'NLRP3_inflammasome -> T2D', 'notes', '17554302', '17429083',
     'Interleukin-1-receptor antagonist', 'Larsen NEJM 2007 anakinra in T2D'),
    ('paths', 'tacrolimus -> inflammation', 'notes', '27291296', '27295076',
     'Calcineurin inhibitors', 'tacrolimus induces vascular inflammation (Sci Rep 2016)'),
    ('validated_paths', 'dapagliflozin -> cardiovascular', 'external_evidence',
     '36041242', '36030328', 'ejection fraction',
     'Nat Med 2022, dapagliflozin across the range of EF, pooled meta-analysis'),
    ('paths', 'dapagliflozin -> inflammation', 'evidence_summary',
     '32332732', '32358544', 'SGLT2', 'Nat Commun 2020, SGLT2i modulates NLRP3 via ketones'),
]


def verify(pmids):
    q = dict(TOOL, db='pubmed', retmode='json', id=','.join(sorted(set(pmids))))
    data = json.loads(urllib.request.urlopen(ESUMMARY + urllib.parse.urlencode(q),
                                             timeout=60).read().decode())
    out = {}
    for pmid, rec in data.get('result', {}).items():
        if isinstance(rec, dict) and rec.get('title'):
            out[pmid] = f"{rec['title']} [{rec.get('source', '')} {(rec.get('pubdate') or '')[:4]}]"
    return out


def main():
    with open(STATE, encoding='utf-8') as f:
        state = json.load(f)

    titles = verify([r[4] for r in REPAIRS])

    print('VERIFYING REPLACEMENTS AGAINST LIVE PUBMED')
    ok = True
    for _, _, _, wrong, right, frag, claim in REPAIRS:
        title = titles.get(right, '')
        good = frag.lower() in title.lower()
        ok &= good
        print(f'  {"[OK]  " if good else "[FAIL]"} {wrong} -> {right}  {title[:88]}')
    if not ok:
        print('\nA replacement did not match its expected title fragment. Nothing written.')
        return 1

    shutil.copy2(STATE, STATE + '.bak_prose_citations')
    applied, missed = 0, []
    for store, key, field, wrong, right, _frag, claim in REPAIRS:
        rec = (state.get(store) or {}).get(key)
        if not isinstance(rec, dict) or field not in rec:
            missed.append((store, key, field, 'record or field absent'))
            continue
        blob = json.dumps(rec[field], ensure_ascii=False)
        if wrong not in blob:
            missed.append((store, key, field, f'{wrong} not present'))
            continue
        rec[field] = json.loads(re.sub(r'\b' + wrong + r'\b', right, blob))
        rec.setdefault('prose_citation_repairs', []).append({
            'date': '2026-08-23', 'field': field, 'was': wrong, 'now': right,
            'claim_in_prose': claim, 'verified_title': titles[right],
            'why': ('purged from external_pmids on 2026-08-20 as off-topic but left '
                    'asserted as fact in narrative text; replacement resolved live '
                    'from PubMed by searching for the paper the prose describes'),
        })
        applied += 1

    if missed:
        print('\nNOT APPLIED:')
        for m in missed:
            print('  ', m)

    state['last_updated'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=1, ensure_ascii=False)
    print(f'\n[OK] {applied}/{len(REPAIRS)} prose citations repaired. '
          f'Backup: {os.path.basename(STATE)}.bak_prose_citations')
    return 0


if __name__ == '__main__':
    sys.exit(main())
