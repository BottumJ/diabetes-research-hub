#!/usr/bin/env python3
"""
Runtime PMID ceiling — replaces the hardcoded "PMIDs above 42000000 are
fabricated" rule.

WHY THIS EXISTS
---------------
The scheduled-task file and several run reports carry a fixed threshold of
42,000,000: any PMID above it is presumed fabricated. PMIDs are assigned
sequentially as records are created, so that threshold has an expiry date and
it has already passed. Measured 2026-08-27 the live maximum was 42,626,404;
measured 2026-08-31 this repo's own weekly sweep returned 42,661,296 straight
from PubMed. Thirty-plus PMIDs in this corpus now sit above 42,000,000 and
every one of them is real. A rule that flags real papers as fabricated is worse
than no rule, because it trains the reader to ignore the flag.

WHAT REPLACES IT
----------------
A ceiling measured from PubMed at runtime and cached. A PMID is IMPOSSIBLE only
if it exceeds the highest PMID PubMed has actually issued, plus a small margin
for records created between cache refreshes.

The margin is not a fudge factor for uncertainty about whether a paper is real.
It absorbs one thing only: PMIDs issued after the cache was written. PubMed
issues roughly 4,000-5,000 PMIDs a day, so a 7-day cache can fall at most about
35,000 behind. MARGIN is set to 250,000 — roughly 50 days of issuance — so a
stale cache produces no false accusations even if the sweep does not run for
weeks. The cost of that conservatism is that a fabricated PMID within 250,000
of the true ceiling passes this gate; that is the correct trade, because
existence is verified for real by verify_pmids.py against the live API. THIS
GATE IS A CHEAP OFFLINE SANITY CHECK, NOT AN EXISTENCE PROOF.

USAGE
    from pmid_ceiling import ceiling, is_impossible, explain
    if is_impossible(pmid): ...
"""
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, '..', '..')
CACHE_FILE = os.path.join(BASE_DIR, 'Analysis', 'Results', '.pmid_ceiling_cache.json')

EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'

# See module docstring: absorbs cache staleness only, never uncertainty.
MARGIN = 250_000

# Refresh cadence. PubMed issues ~4-5k PMIDs/day, so a 7-day cache trails the
# true ceiling by ~35k, comfortably inside MARGIN.
MAX_CACHE_AGE_DAYS = 7

# Used only when the network is unavailable AND no cache exists. This is the
# last value this repo measured directly from PubMed, not a guess. Update it
# when you have a fresh measurement; the whole point of this module is that it
# should almost never be reached.
LAST_MEASURED = {'pmid': 42661296, 'date': '2026-08-31'}


def _fetch_live_ceiling(timeout=30):
    """Highest PMID PubMed has issued, read from the most recent records.

    PMIDs are sequential at record creation, so the newest Entrez dates carry
    the highest PMIDs. Ask for the last 2 days and take the maximum.
    """
    params = urllib.parse.urlencode({
        'db': 'pubmed',
        'term': 'all[sb]',
        'retmode': 'json',
        'retmax': 200,
        'reldate': 2,
        'datetype': 'edat',
        'sort': 'most+recent',
    })
    with urllib.request.urlopen(EUTILS + params, timeout=timeout) as fh:
        data = json.load(fh)
    ids = [int(i) for i in data['esearchresult'].get('idlist', []) if i.isdigit()]
    if not ids:
        raise RuntimeError('esearch returned no ids')
    return max(ids)


def _read_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, encoding='utf-8') as fh:
            return json.load(fh)
    except (ValueError, OSError):
        return None


def _write_cache(payload):
    with open(CACHE_FILE, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)


def ceiling(force_refresh=False, allow_network=True):
    """Return (ceiling_pmid, provenance_dict).

    provenance['source'] is one of:
      'live'          — measured from PubMed on this call
      'cache'         — measured from PubMed on cache['measured'], still fresh
      'stale_cache'   — cache older than MAX_CACHE_AGE_DAYS, refresh failed
      'last_measured' — no cache and no network; module constant
    """
    cache = _read_cache()
    fresh = False
    if cache:
        try:
            age = datetime.now() - datetime.fromisoformat(cache['measured'])
            fresh = age < timedelta(days=MAX_CACHE_AGE_DAYS)
        except (KeyError, ValueError):
            fresh = False

    if cache and fresh and not force_refresh:
        return cache['ceiling'], {'source': 'cache', 'measured': cache['measured']}

    if allow_network:
        try:
            live = _fetch_live_ceiling()
            payload = {
                'ceiling': live,
                'measured': datetime.now().isoformat(),
                'margin': MARGIN,
                'method': 'esearch all[sb] reldate=2 datetype=edat, max of idlist',
            }
            _write_cache(payload)
            return live, {'source': 'live', 'measured': payload['measured']}
        except Exception as exc:  # network down, NCBI throttling, etc.
            if cache:
                return cache['ceiling'], {
                    'source': 'stale_cache',
                    'measured': cache.get('measured'),
                    'refresh_error': f'{type(exc).__name__}: {exc}',
                }
            return LAST_MEASURED['pmid'], {
                'source': 'last_measured',
                'measured': LAST_MEASURED['date'],
                'refresh_error': f'{type(exc).__name__}: {exc}',
            }

    if cache:
        return cache['ceiling'], {'source': 'stale_cache', 'measured': cache.get('measured')}
    return LAST_MEASURED['pmid'], {'source': 'last_measured', 'measured': LAST_MEASURED['date']}


def is_impossible(pmid, cap=None):
    """True only if pmid exceeds a PMID PubMed could plausibly have issued.

    Returns False for anything it cannot rule out. Existence is proved by
    verify_pmids.py against the live API, not here.
    """
    try:
        value = int(str(pmid).strip())
    except (TypeError, ValueError):
        return False
    if value <= 0:
        return True
    if cap is None:
        cap, _ = ceiling()
    return value > cap + MARGIN


def explain():
    """One-line human-readable statement of the current gate."""
    cap, prov = ceiling()
    return (f'PMID ceiling {cap:,} (+{MARGIN:,} margin) = flag above {cap + MARGIN:,}; '
            f"source={prov['source']} measured={prov.get('measured')}")


if __name__ == '__main__':
    cap, prov = ceiling(force_refresh=True)
    print(explain())
    print(json.dumps(prov, indent=2))
    # Demonstrate against the stale rule the task file still carries.
    for probe in (42000001, 42661296, cap + 1, cap + MARGIN + 1):
        verdict = 'IMPOSSIBLE' if is_impossible(probe, cap) else 'plausible'
        print(f'  {probe:>12,} -> {verdict}')
