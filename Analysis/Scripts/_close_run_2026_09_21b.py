#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Second pass, 2026-09-21. Amend the run record after adversarial re-check.

The first pass of this run wrote a confident summary and a verification note.
An independent adversarial re-check of that summary falsified part of it
within minutes. What it found was worse than what the first pass fixed, and
the amendment below is the honest version.
"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(os.path.dirname(HERE), "Results", "agent_state.json")
TODAY = "2026-09-21"

with open(STATE, "r", encoding="utf-8") as fh:
    state = json.load(fh)

run = state["run_history"][-1]
assert run["date"] == TODAY, "expected today's run at the tail of run_history"

run["second_pass"] = (
    "THE FIRST PASS OF THIS RUN CLAIMED TO HAVE FIXED THE BELATACEPT FABRICATION AND HAD "
    "FIXED ONE INSTANCE OF IT IN ONE FILE. An adversarial re-check of that claim -- run "
    "specifically to try to falsify it rather than confirm it -- found the same invented "
    "figure live in FOUR builders and in both published dashboard copies. "
    "build_gap_deep_dives.py line 278, twenty lines below a correction the first pass had "
    "just written, read 'CTLA-4 Ig (belatacept): 70% graft survival at 10yr vs 32% with "
    "tacrolimus'. build_data_dictionary.py carried it twice with a 50% comparator, cited to "
    "PMID:16120857. build_gap_synthesis.py carried it with no comparator and no citation. "
    "THREE FILES, THREE DIFFERENT TACROLIMUS COMPARATORS (32%, 50%, none) FOR ONE NUMBER, "
    "which is by itself sufficient evidence that the number was never read off a paper. "
    "PMID 16120857 was fetched live this run: Vincenti et al., NEJM 2005, a RENAL "
    "transplant trial whose comparator is CYCLOSPORINE, not tacrolimus, with endpoints of "
    "acute rejection at SIX MONTHS and GFR at TWELVE MONTHS. It contains no ten-year "
    "endpoint, no graft-survival percentage, no 70 and no 50. A fourth conflation runs "
    "through all of it: GRAFT SURVIVAL is not INSULIN INDEPENDENCE. The only long-term "
    "figure this hub legitimately holds is 7-of-10 insulin independence (PMID:37359825) -- "
    "a different outcome, a different population, and n=10. All four sites are now "
    "corrected and re-verified absent from source and from both published copies. "
    "THE LESSON IS ABOUT THE FIRST PASS'S METHOD, NOT ITS LUCK. It found the defect by "
    "reading one paper against one file, then verified its repair by grepping for THE "
    "STRINGS IT HAD JUST EDITED. That test can only ever confirm the edit; it cannot find a "
    "fifth copy, because a grep for text you wrote is a grep for your own memory. The "
    "search that worked was the one that started from the CLAIM ('belatacept, 70%, ten "
    "years') and swept the whole corpus for anything asserting it. Verify the claim, not "
    "the edit. "
    "THE NEW GATE WAS ALSO WRONG IN TWO WAYS, BOTH FOUND BY THE SAME RE-CHECK AND BOTH NOW "
    "FIXED. (1) IT COULD NOT FAIL A BUILD. main() computed status='FAIL' and then returned "
    "0 unconditionally, while run_quality_improvements.py dispatches on the return code. "
    "Every claim the first pass made about this gate 'failing the build the day a new "
    "uncited percentage is added' was therefore false as shipped -- a gate that reports and "
    "calls itself a gate is worse than no gate, because the green line is now evidence of "
    "nothing while looking like evidence of something. (2) IT HAD REAL FALSE POSITIVES: it "
    "keys on (identifier, timepoint) and never parses WHAT IS MEASURED, so '61% at 5 years "
    "in adults' versus '32% at 5 years in children', and 'insulin independence 44% at 1 "
    "year' versus 'C-peptide positivity 90% at 1 year', both registered as contradictions. "
    "Both are correct writing. An outcome-word filter and an explicit closed list of "
    "cohort-partition words now suppress both classes, re-proven on fixtures. But a "
    "heuristic that works most of the time must not be allowed to fail a build -- that is "
    "the 2026-09-15 surname mistake and the 2026-09-18 coordinate mistake, and this "
    "repository has now made some version of it three times, twice in this single run. So "
    "the split is explicit: the RATCHET fails (purely mechanical -- an identifier is on the "
    "line or it is not), the CONFLICT check only reports and a human adjudicates. "
    "Ratchet moved 35 -> 31 as the corrections added citations."
)

run["verification"] = (
    run["verification"]
    + " | SECOND PASS, after adversarial re-check falsified the first: all SIX fabricated "
      "strings ('Belatacept 70% at 10yr', 'Belatacept-based: 70%', 'Efalizumab-based: 60%', "
      "'6/10 insulin-independent at 10 years', '70% graft survival at 10yr', '70% graft "
      "survival at 10 years') now return count 0 across Dashboards/*.html AND "
      "docs/Dashboards/*.html, and 0 in non-comment builder source. PMID 16120857 fetched "
      "live and quoted in the repair. Gate re-proven on a nine-case fixture: fires on the "
      "real 70%-vs-6/10 conflict; silent on different timepoint, different PMID, different "
      "outcome at one timepoint, and adult-vs-child subgroups; exits 1 on ratchet "
      "regression and 0 otherwise (both directions executed). Pipeline stages compile, "
      "endpointagreement, deepdives, synthesis, dictionary, islet, syncdocs all [OK]; "
      "159 builders parse."
)
run["builders_fixed"] = 4
run["gates_added"] = 1
run["gate_defects_found_by_self_review"] = 2
run["adversarial_recheck"] = "performed; falsified the first pass's central repair claim"

state.setdefault("doctrine_notes", {})["verification_method_" + TODAY] = (
    "VERIFY THE CLAIM, NOT THE EDIT. A repair verified by grepping for the strings you just "
    "wrote is self-confirming: it proves the edit landed and is structurally incapable of "
    "finding another copy of the same falsehood elsewhere. On 2026-09-21 that method "
    "returned a clean result while the identical fabrication was live in three other "
    "builders and both published dashboard copies. The test that works starts from the "
    "ASSERTION -- drug, number, endpoint -- and sweeps the whole corpus for anything that "
    "states it, however worded. Corollary, learned the same day: a NEW GATE MUST BE TESTED "
    "FOR ITS EXIT CODE, not just its printed verdict. This one printed [FAIL] and returned "
    "0 for its entire first life."
)

NEW = [
    {
        "type": "verify_citations", "priority": 1, "added": TODAY,
        "target": "SWEEP THE CORPUS FOR THE OTHER FABRICATED-FIGURE FAMILIES, USING THE "
                  "METHOD THAT WORKED TODAY. Today's second pass found one invented number "
                  "('belatacept, 70%, 10 years') replicated across four builders with three "
                  "mutually inconsistent comparators, after a first pass had declared it "
                  "fixed. The tell was not any single statement -- each was internally "
                  "plausible -- it was the DISAGREEMENT BETWEEN COPIES. Do this "
                  "deliberately: extract every (entity, value, endpoint) triple from builder "
                  "source, group by entity+endpoint ACROSS FILES, and list every group whose "
                  "values or comparators disagree. The new gate cannot do this; its buckets "
                  "are per-file by construction and that limit is documented in its "
                  "docstring. This is the cross-file version and it is where the next one of "
                  "these is hiding.",
    },
    {
        "type": "fix_pipeline", "priority": 1, "added": TODAY,
        "target": "AUDIT EVERY GATE IN run_quality_improvements.py FOR THE EXIT-CODE BUG "
                  "FOUND IN audit_endpoint_value_agreement.py TODAY. It printed '[FAIL] ... "
                  "1 conflicts' and returned 0, so the runner -- which dispatches on the "
                  "return code -- recorded [OK]. If any other audit script computes a FAIL "
                  "verdict and then returns 0, its green line in every historical run report "
                  "is worthless, and worse than worthless because it was counted as "
                  "assurance. This is mechanically checkable in minutes: for each audit_*.py, "
                  "confirm that a constructed failing input produces a NONZERO exit. Do not "
                  "trust the printed verdict -- that is exactly what failed here. Check all "
                  "of them, including the ones with fixtures.",
    },
]
state["work_queue"].extend(NEW)

with open(STATE, "w", encoding="utf-8") as fh:
    json.dump(state, fh, indent=2, ensure_ascii=False)

print("second pass recorded; new queue items:", len(NEW))
print("queue length:", len(state["work_queue"]))
