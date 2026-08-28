#!/usr/bin/env python3
"""ONE place that answers: may this PMID be used as corpus evidence?

WHY THIS MODULE EXISTS
----------------------
The work-queue item "SEAL THE REMAINING INTAKE DOORS BY CLASS, NOT BY NAME"
was raised 2026-08-25 and carried unchanged on 2026-08-27. Its observation is
that every NEW reader of PMIDs in this repo starts life unguarded, so the
repo has been sealing doors one at a time, by name, after each one leaks.

Before this module there were FIVE hand-rolled loaders of the same two
registries, and they did not agree with each other:

  extract_corpus_data.py    not_corpus  + FLAGGED          (the only complete one)
  extract_evidence.py       not_corpus  only               <- FLAGGED leaked
  ingest_papers.py          not_corpus  only               <- FLAGGED leaked
  reconcile_paper_index.py  not_corpus  + FLAGGED (report only, does not exclude)
  verify_pmids.py           not_corpus  + RETRACTED split

WHAT THAT DIVERGENCE COST (measured 2026-08-28, not hypothesised)
-----------------------------------------------------------------
18 papers carry status FLAGGED in agent_state.json - the repo's own written
adjudication that they are off-topic. Only 1 of the 18 had also been entered
in not_corpus_pmids.json. So 17 adjudicated-off-topic papers were excluded by
exactly one consumer and by no other, and 12 of them still had cached
abstracts on disk feeding extract_evidence.py.

Two of them were live miscitations on published dashboards:

  20570966  published as "Orban et al., Abatacept Phase 2 in T1D"
            actually  "Fucosyltransferase 2 (FUT2) non-secretor status is
                      associated with Crohn's disease", Hum Mol Genet 2010
  28397826  published as "Buzzetti et al. Management of latent autoimmune
                      diabetes in adults, Nat Rev Endocrinol"
            actually  "Immunotherapy: Hiding in plain sight...", Nat Rev
                      Clin Oncol 2017

Both had passed every gate this repo owns, because both resolve, both have
correct stored titles nowhere, and neither was in the registry that the gates
consult. FLAGGED knew about both and nothing enforced FLAGGED.

THE DESIGN RULE
---------------
Membership is a QUESTION ABOUT A PMID, not a filtering step inside one
script. Ask it here. Consumers must not re-implement it, because the five
re-implementations above diverged silently over four months and the
divergence is what published the two miscitations.

MEMBERSHIP IS TWO QUESTIONS, NOT ONE
------------------------------------
The naive fix - make FLAGGED a hard exclusion everywhere, since
extract_corpus_data.py already treats it that way - is wrong, and reading all
18 FLAGGED records is what showed it. FLAGGED had been carrying two
incompatible meanings: "not a diabetes paper" (metastatic colon cancer) and
"a diabetes paper whose evidence does not count" (metformin pyroptosis in
HK-2 cells, evidence_tier IN_VITRO_ONLY). One boolean cannot express both,
and hard-excluding the second group deletes real on-topic papers.

The repo had already written the distinction down and had nowhere to put it.
The note stored against PMID 25714673 on 2026-04-20 reads, verbatim:
"Keep in paper_library but exclude from mechanism-evidence extraction."

So this module answers two questions and keeps them apart:

  citable(pmid)            may this PMID appear in prose at all?
  counts_as_evidence(pmid) may it support a diabetes claim / be counted?

FIVE DISQUALIFIERS, KEPT DISTINCT
---------------------------------
Not merged into one boolean, because the remedy differs and collapsing them
destroys the reason the evidence count changed - the same mistake
not_corpus_pmids.json was extended on 2026-08-26 to avoid when RETRACTION was
nearly filed under PROVENANCE.

                          citable  evidence  remedy
  PROVENANCE                 no       no     delete; nothing was ever there
  RETRACTED                  no       no     exclude AND record the withdrawal
  OFF_TOPIC                  no       no     repair or withdraw the citation
  BACKGROUND                YES       no     keep the citation, drop the count
  (unlisted)                YES      YES     ordinary corpus paper

BACKGROUND is the class that a single boolean was destroying. PMID 18662538
(Massague, "TGFbeta in Cancer", Cell 2008) is the definitional source for the
TGF-beta entry in the Medical Data Dictionary. The citation is true. It
supplies no diabetes finding. Both facts have to survive.

WHAT THIS MODULE DOES NOT DO
----------------------------
It does not decide whether a citation names the right paper. That is
audit_builder_title_agreement.py and audit_citation_coordinates.py. This
module answers membership only.
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Results'))

NOT_CORPUS_PATH = os.path.join(RESULTS, 'not_corpus_pmids.json')
STATE_PATH = os.path.join(RESULTS, 'agent_state.json')

# Disqualifier codes. The most serious classification wins, so a retracted
# paper is never reported merely as off-topic.
RETRACTED = 'RETRACTED'
PROVENANCE = 'PROVENANCE'
OFF_TOPIC = 'OFF_TOPIC'
BACKGROUND = 'BACKGROUND'

# Codes that also forbid CITING the paper, not merely counting it.
NOT_CITABLE = (RETRACTED, PROVENANCE, OFF_TOPIC)

# A FLAGGED paper with no membership_class is a bug, not a default. Silently
# picking a meaning here is exactly how the five divergent loaders arose.
UNCLASSIFIED = 'FLAGGED_UNCLASSIFIED'

_cache = None


def _load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        # Deliberately loud. A silent empty registry means every excluded
        # paper is silently re-admitted, which is the failure mode this
        # module exists to prevent.
        print('  [corpus_membership] WARNING: could not read %s: %s'
              % (os.path.basename(path), exc))
        return {}


def _build():
    """Read both registries once and classify every disqualified PMID."""
    registry = _load_json(NOT_CORPUS_PATH).get('pmids') or {}
    state = _load_json(STATE_PATH)
    papers = state.get('papers') or {}

    reasons = {}

    for pmid, rec in registry.items():
        pmid = str(pmid)
        prov = (rec or {}).get('provenance') or PROVENANCE
        code = RETRACTED if prov == RETRACTED else PROVENANCE
        reasons[pmid] = {
            'code': code,
            'why': (rec or {}).get('why', ''),
            'title': (rec or {}).get('actual_title', ''),
            'source': 'not_corpus_pmids.json',
        }

    for pmid, rec in papers.items():
        pmid = str(pmid)
        if (rec or {}).get('status') != 'FLAGGED':
            continue

        cls = (rec or {}).get('membership_class') or UNCLASSIFIED
        why = ((rec or {}).get('membership_class_why')
               or (rec or {}).get('flag_reason') or '')

        if pmid in reasons:
            # Both registries know about it. Keep whichever is more serious;
            # RETRACTED must never be downgraded to a topic judgement.
            existing = reasons[pmid]['code']
            if existing == RETRACTED or cls == existing:
                reasons[pmid]['also_flagged_as'] = cls
                continue
        reasons[pmid] = {
            'code': cls,
            'why': why or 'FLAGGED in agent_state.json with no class recorded',
            'title': (rec or {}).get('title', ''),
            'source': 'agent_state.json:papers.membership_class',
        }

    return reasons


def _reasons():
    global _cache
    if _cache is None:
        _cache = _build()
    return _cache


def reload():
    """Drop the cache. For scripts that mutate the registries mid-run."""
    global _cache
    _cache = None


def excluded_pmids():
    """Every PMID that must not COUNT AS EVIDENCE, any disqualifier.

    This is the set the extractors want, and it is deliberately the widest
    one: BACKGROUND papers are citable but contribute no data points.
    """
    return set(_reasons())


def uncitable_pmids():
    """PMIDs that must not appear in live prose at all.

    Narrower than excluded_pmids(). A builder repairing citations wants this
    set; using excluded_pmids() here would strip correct citations such as
    the Massague TGF-beta definition.
    """
    return {p for p, r in _reasons().items()
            if r['code'] in NOT_CITABLE or r['code'] == UNCLASSIFIED}


def excluded_by(code):
    """PMIDs excluded under one specific disqualifier."""
    return {p for p, r in _reasons().items() if r['code'] == code}


def counts_as_evidence(pmid):
    """May this PMID support a diabetes claim or be counted in the corpus?"""
    return str(pmid) not in _reasons()


def citable(pmid):
    """May this PMID appear in published prose?"""
    return str(pmid) not in uncitable_pmids()


# Retained name so the five existing call sites keep their current meaning.
def is_corpus(pmid):
    """Alias of counts_as_evidence(). Kept because five consumers already
    ask the evidence-level question under this name."""
    return counts_as_evidence(pmid)


def unclassified():
    """FLAGGED papers with no membership_class. Should always be empty; an
    audit fails on this rather than letting a consumer guess a meaning."""
    return excluded_by(UNCLASSIFIED)


def reason(pmid):
    """Why a PMID is excluded, or None. Never returns a bare boolean, so a
    caller that wants to explain an exclusion is never forced to guess."""
    return _reasons().get(str(pmid))


def filter_pmids(pmids, label=''):
    """Split an iterable into (kept, dropped). Prints one accountable line.

    Returning the dropped list rather than silently filtering is deliberate:
    every consumer should be able to say how many papers it excluded and
    why, and the 2026-08-25 leak persisted partly because exclusions were
    invisible in the run output.
    """
    kept, dropped = [], []
    for p in pmids:
        (kept if is_corpus(p) else dropped).append(str(p))
    if dropped:
        by = {}
        for p in dropped:
            by.setdefault(reason(p)['code'], []).append(p)
        parts = ', '.join('%s=%d' % (k, len(v)) for k, v in sorted(by.items()))
        print('  [corpus_membership]%s excluded %d PMID(s) (%s)'
              % (' ' + label if label else '', len(dropped), parts))
    return kept, dropped


def summary():
    r = _reasons()
    out = {}
    for rec in r.values():
        out[rec['code']] = out.get(rec['code'], 0) + 1
    return {'total_excluded': len(r), 'by_code': out}


if __name__ == '__main__':
    s = summary()
    print('corpus_membership: %d PMID(s) excluded' % s['total_excluded'])
    for code, n in sorted(s['by_code'].items()):
        print('  %-22s %d' % (code, n))
    print()
    for pmid, rec in sorted(_reasons().items()):
        print('  %-10s %-22s %s' % (pmid, rec['code'], (rec['title'] or rec['why'])[:70]))
