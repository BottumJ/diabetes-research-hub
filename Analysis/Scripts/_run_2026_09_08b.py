"""Daily iteration run - 2026-09-08, part B (post-gate corrections).

Part A queued a fix_pipeline item asserting that audit_prose_citation_titles.py
"scans .py only for title mismatch, not author/journal/n". Running the gate
afterwards showed that claim is WRONG: the gate emits journal_ok, year_ok and
author_ok per reference and already checks all three. This script replaces that
item with an accurate one, and records the two real gate findings from the run.

Idempotent: safe to re-run.
"""
import json
import os
from datetime import datetime

RESULTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Results')
STATE = os.path.join(RESULTS, 'agent_state.json')
TODAY = '2026-09-08'

with open(STATE, encoding='utf-8') as fh:
    state = json.load(fh)

# ------------------------------------------------- replace the wrong item
queue = [q for q in state['work_queue']
         if not (q.get('added') == TODAY
                 and 'NO GATE CATCHES A CITATION WHOSE DESCRIPTION CONTRADICTS ITS PMID'
                 in str(q.get('target', '')))]

CORRECTED = [
    {
        'type': 'fix_pipeline', 'priority': 1, 'added': TODAY,
        'target': (
            'THE CITATION GATE CHECKS ONLY 26.3% OF REFERENCES, AND TODAY\'S DEFECT WAS IN THE '
            'OTHER 73.7%. Correcting what this item said earlier today: '
            'audit_prose_citation_titles.py DOES check author, journal and year - it emits '
            'author_ok / journal_ok / year_ok per reference. The blind spot is not which '
            'fields it compares, it is which references it will look at. The gate\'s own '
            'closing line reads: "Coverage: 26.3% of builder PMID references assert an '
            'identity and were checked; the rest are descriptive and are NOT verified here." '
            'The Gap #11 evidence-catalog entry corrected today - which named the wrong '
            'author, wrong title, wrong journal and wrong denominator for PMID 19104422 - sat '
            'squarely in that unchecked 73.7%, because it reads as description rather than as '
            'an identity assertion. So the gate is sound and its REACH is the defect. '
            'PROPOSAL: treat an evidence-catalog or source-list entry as an identity assertion '
            'by structure rather than by phrasing, since those blocks exist precisely to say '
            'what a paper is. Measure first: run the gate with the identity-assertion test '
            'relaxed to include any PMID inside an evidence-item / source / catalog block, '
            'report the new coverage fraction and the new mismatch count, and only then decide '
            'whether the false-positive rate is tolerable enough to wire in.'
        ),
    },
    {
        'type': 'fix_pipeline', 'priority': 2, 'added': TODAY,
        'target': (
            'THE CITATION GATE CANNOT TELL A PMID BEING USED FROM A PMID BEING QUOTED AS AN '
            'ERROR, AND THIS REPO DOCUMENTS ITS CORRECTIONS IN PLACE. Measured today: the gate '
            'went from 2 mismatches at HEAD to 3, and the new one is a false positive. '
            'build_immunomod_lada.py:331 is flagged for PMID 20570966 (FUT2/Crohn\'s, Hum Mol '
            'Genet 2010) - but that PMID appears only inside a repair comment reading '
            '"Repaired 2026-08-28. This entry read PMID:20570966, which is ... not an '
            'abatacept trial", i.e. the comment exists BECAUSE the citation was already fixed. '
            'The gate re-flags the fix as the fault. This is not cosmetic: the standing '
            'practice here is to leave a visible correction notice quoting the wrong original, '
            'and the Gap #11 correction written today does exactly that in '
            'build_islet_equity.py - it quotes the false "International Islet Transplant '
            'Registry / 1,477 recipients / American Journal of Transplantation" wording next to '
            'PMID 19104422. It did not trip the gate today, but only because the marker '
            'heuristic happened not to fire. Every future correction is a coin flip. '
            'FIX: have the gate skip PMIDs occurring inside a Python comment or inside a span '
            'marked as a correction, and count them separately as "quoted_as_error" so they '
            'stay visible without failing the build.'
        ),
    },
    {
        'type': 'verify_citations', 'priority': 2, 'added': TODAY,
        'target': (
            'A REAL GATE HIT THAT PREDATES TODAY AND IS STILL OPEN: build_gka_pricing.py:462 '
            'attaches PMID 32175717 to a GKA revenue projection ("Scenario A: Niche T2D ... '
            'Projected Revenue: <$500M by 2030 (modeled estimate - Khan et al. 2020)"). '
            'PMID 32175717 is Khan et al. 2020, "Epidemiology of Type 2 Diabetes - Global '
            'Burden of Disease and Forecasted Trends", J Epidemiol Glob Health. Author and '
            'year match, so it is not a fabricated citation - but a T2D epidemiology paper '
            'cannot support a glucokinase-activator revenue forecast. The prose does say '
            '"modeled estimate", which is honest about the number; what is wrong is hanging a '
            'PMID off it, because that reads as though the source produced the forecast. '
            'Either state the model\'s own assumptions and cite 32175717 only for the '
            'prevalence input it actually supplies, or drop the PMID and label the figure '
            'unsourced. Present at HEAD (flagged there too), so this is not a regression.'
        ),
    },
]
state['work_queue'] = CORRECTED + queue

# --------------------------------------------------------- gate findings
state.setdefault('audit_notes', []).append({
    'date': TODAY,
    'artifact': 'Analysis/Scripts/audit_prose_citation_titles.py',
    'finding': (
        'Gate run after today\'s edits: [FAIL] 3 mismatches, up from 2 at HEAD. Adjudicated '
        'individually rather than by the count. '
        '(1) build_gka_pricing.py:462 / PMID 32175717 - REAL, pre-existing at HEAD, queued. '
        '(2) build_treg_neuropathy.py:486 / PMID 8366922 - FALSE POSITIVE, pre-existing at '
        'HEAD. 8366922 is the DCCT 1993 NEJM paper and the prose cites it correctly as '
        '"DCCT, 1993"; journal_ok and year_ok are both true and only author_ok fails, because '
        'the prose names the trial rather than Nathan. The overlap heuristic additionally '
        'scraped HTML attributes into the "asserted title". '
        '(3) build_immunomod_lada.py:331 / PMID 20570966 - FALSE POSITIVE, NEW today, and the '
        'gate is flagging a repair comment that documents an already-completed fix. Queued. '
        'Net: no new real citation defect was introduced by this run, and the gate\'s own '
        'reported coverage of 26.3% is the reason it missed the Gap #11 defect that this run '
        'found by hand.'
    ),
})

state['last_updated'] = TODAY
with open(STATE, 'w', encoding='utf-8') as fh:
    json.dump(state, fh, indent=2, ensure_ascii=False)

print('[OK] replaced 1 inaccurate queue item, added 3 accurate ones')
print('[OK] queue len', len(state['work_queue']))
