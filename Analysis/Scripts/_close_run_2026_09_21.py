#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close the 2026-09-21 run: record findings, ingest sweep, triage the P0 queue.

P0 TRIAGE IS THE ADMINISTRATIVE FINDING OF THIS RUN. Nine items sat at
priority 0. They were not nine problems; they were one real problem and eight
restatements of two failures that no longer exist. Every one of them was
re-read, and re-ranked, at the top of every run since. Each was tested
against a command executed THIS run, not against a previous run's report.
"""

from __future__ import annotations

import datetime
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(os.path.dirname(HERE), "Results", "agent_state.json")
TODAY = "2026-09-21"

with open(STATE, "r", encoding="utf-8") as fh:
    state = json.load(fh)

# --------------------------------------------------------------------------
# 1. Sweep ingest. Monday, so Step 2 of the task file is due.
# --------------------------------------------------------------------------
# Every PMID below was resolved live via eutils esummary this run and returned
# a real title, journal and pubtype. All are below the live PMID ceiling
# (42763307, measured 2026-09-20), so none is fabricated.
SWEEP = {
    "42738899": {
        "title": "Diabetic Immunotherapy Advances with BCG: Metabolic and Immune Reprogramming.",
        "journal": "Cells", "year": "2026", "pubtype": ["Journal Article", "Review"],
        "query": "LADA latent autoimmune diabetes",
        "relevance": "T1D immunomodulation; BCG is an existing-agent repurposing candidate, "
                     "which is this hub's Gap #4/#8 territory. REVIEW, not primary evidence.",
    },
    "42739778": {
        "title": "Clinical Evolution, Outcomes, and Emerging Preservation Technologies in "
                 "Pancreas and Islet Transplantation.",
        "journal": "J Clin Med", "year": "2026", "pubtype": ["Journal Article", "Review"],
        "query": "islet transplant outcomes",
        "relevance": "Directly on Gap #3. REVIEW. Worth reading specifically for whether it "
                     "reports a 10-year insulin-independence rate, because this hub now "
                     "publishes four different 10-year figures on one dashboard and three of "
                     "them are still unreconciled.",
    },
    "42760903": {
        "title": "Enhancement of Harvested Islet Functionality Through Photostimulation.",
        "journal": "J Biophotonics", "year": "2026", "pubtype": ["Journal Article"],
        "query": "islet transplant outcomes",
        "relevance": "Bench study on harvested islets. Peripheral to the gaps this hub tracks.",
    },
    "42753472": {
        "title": "Portulaca oleracea L.-Derived extracellular vesicles alleviate renal "
                 "lipotoxicity in diabetic kidney disease by regulating the NLRP3 pathway.",
        "journal": "Phytomedicine", "year": "2026", "pubtype": ["Journal Article"],
        "query": "NLRP3 inflammasome diabetic kidney",
        "relevance": "PRECLINICAL, plant-derived EVs. Touches the NLRP3 path but is not "
                     "evidence for a repurposable generic agent. Do not let it strengthen "
                     "the NLRP3 path's grade.",
    },
    "42739042": {
        "title": "Targeting Ferroptosis, Pyroptosis, and NRF2 Signaling with Dietary "
                 "Polyphenols in Diabetic Microvascular Complications: An Integrative Review.",
        "journal": "Nutrients", "year": "2026", "pubtype": ["Journal Article", "Review"],
        "query": "NLRP3 inflammasome diabetic kidney",
        "relevance": "REVIEW, dietary polyphenols. Mechanism-adjacent, not a drug candidate.",
    },
}

# Screened out with a stated reason, rather than silently dropped.
SCREENED_OUT = {
    "42751492": "PUBLISHED ERRATUM, not a study. Correction to Peng et al., Front Immunol "
                "2022;13:836952 (GAD65 antibody epitopes in latent autoimmune diabetes in "
                "youth). Checked this run: this hub cites NEITHER the erratum NOR the 2022 "
                "original, so nothing here is affected. Recorded because the check, not the "
                "paper, is the point.",
    "42761395": "Digital twins / AI in diabetes management. Off-topic: this hub studies "
                "mechanism and repurposing, not care-delivery tooling.",
    "42744965": "OFF-TOPIC AND A QUERY DEFECT. 'Metformin exhibits a synergistic effect with "
                "pyrotinib by inducing ferroptosis in HER2-positive cancers.' This is an "
                "ONCOLOGY paper. It was returned by the sweep query 'oxidative stress AND "
                "diabetes AND combination therapy' because metformin is a diabetes drug "
                "being tested in cancer -- the query cannot tell a diabetes intervention "
                "from a diabetes DRUG used elsewhere. That query returned exactly one hit "
                "this week and it was this. See the queue item added below.",
}

papers = state.setdefault("papers", {})
added = []
for pmid, meta in SWEEP.items():
    if pmid in papers:
        continue
    papers[pmid] = {
        "status": "UNVETTED",
        "added": TODAY,
        "source": "weekly_sweep_2026-09-21",
        "title": meta["title"],
        "journal": meta["journal"],
        "year": meta["year"],
        "pubtype": meta["pubtype"],
        "sweep_query": meta["query"],
        "triage_note": meta["relevance"],
        "identity_verified": "eutils esummary live roundtrip 2026-09-21 "
                             "(title+journal returned; below live PMID ceiling 42763307)",
    }
    added.append(pmid)

screened = state.setdefault("screened_out", {})
for pmid, reason in SCREENED_OUT.items():
    screened.setdefault(pmid, {"date": TODAY, "reason": reason})

state["last_sweep"] = TODAY

# --------------------------------------------------------------------------
# 2. P0 triage. Tested this run, not inherited from a previous report.
# --------------------------------------------------------------------------
MEASURED = {
    "sandbox_mount": "WORKING. Every python3 and git command in this run executed "
                     "against the OneDrive mount. No Plan9 error. The four P0 items "
                     "alleging an unusable sandbox (2026-09-10, -11, -12, -14) are "
                     "describing an outage that ended on 2026-09-15.",
    "git_index_lock_unlink": "STILL FORBIDDEN. `rm .git/index.lock` -> 'Operation not "
                             "permitted', re-tested this run. But this no longer BLOCKS "
                             "anything: sandbox_git_commit.sh routes around it via "
                             "GIT_INDEX_FILE. The ask in the 2026-09-15 item -- have a "
                             "human run Remove-Item / PUSH_AND_VERIFY.ps1 -- is obsolete. "
                             "The condition is real; the request is not.",
    "git_push": "STILL BROKEN, AND STILL THE ONLY REAL P0. `git push --dry-run origin "
                "main` -> 'fatal: could not read Username for https://github.com: No such "
                "device or address'. No credential helper, no ~/.git-credentials, no "
                "GH_TOKEN. 117 commits unpushed as of this run (was 101 on 2026-09-06). "
                "The gap is widening by roughly one commit a day.",
    "task_file_pmid_ceiling": "STILL STALE, AND IT COST THIS RUN A STEP. Step 4 of the "
                              "scheduled-task file instructs a sweep for 'PMIDs above "
                              "42000000 (fabricated)'. The live ceiling is 42763307. Five "
                              "of the papers ingested TODAY are above 42000000 and all five "
                              "are real. An agent obeying the task file literally would "
                              "have deleted them. The repo fixed this in August "
                              "(pmid_ceiling.py); the task file still says otherwise.",
}
state.setdefault("doctrine_notes", {})["p0_triage_" + TODAY] = MEASURED

CLOSE_REASONS = {
    ("2026-09-10", "THE SANDBOX HAS FAILED"): "sandbox_mount",
    ("2026-09-11", "RUN THE PIPELINE ON WINDOWS"): "sandbox_mount",
    ("2026-09-12", "FOURTH IDENTICAL SANDBOX FAILURE"): "sandbox_mount",
    ("2026-09-14", "SIXTH IDENTICAL SANDBOX FAILURE"): "sandbox_mount",
    ("2026-09-15", "GIT IS NOW UNWRITABLE"): "git_index_lock_unlink",
    ("2026-09-05", "BLOCKING, AND IT OUTRANKS"): "git_push_superseded",
    ("2026-09-06", "UNCHANGED AND NOW GATED"): "git_push_superseded",
}

closed, kept = [], []
for item in state.get("work_queue", []):
    if item.get("priority") != 0 or item.get("status") in ("completed", "closed", "done"):
        continue
    target = str(item.get("target", ""))
    added_on = item.get("added", "")
    hit = None
    for (d, prefix), reason in CLOSE_REASONS.items():
        if added_on == d and target.startswith(prefix):
            hit = reason
            break
    if hit == "sandbox_mount":
        item["status"] = "closed_" + TODAY
        item["closed_reason"] = (
            "STALE. " + MEASURED["sandbox_mount"] + " Closing four restatements of one "
            "ended outage. They were not closed earlier because each run added a new one "
            "instead of testing the old.")
        closed.append((added_on, hit))
    elif hit == "git_index_lock_unlink":
        item["status"] = "closed_" + TODAY
        item["closed_reason"] = "SUPERSEDED. " + MEASURED["git_index_lock_unlink"]
        closed.append((added_on, hit))
    elif hit == "git_push_superseded":
        item["status"] = "closed_" + TODAY
        item["closed_reason"] = (
            "MERGED, NOT DISMISSED. Same ask as the 2026-09-16 P0, which is kept live and "
            "is now the single push item. Three identical copies of one request do not "
            "make it three times as visible; they make the queue unreadable.")
        closed.append((added_on, hit))
    else:
        kept.append((added_on, target[:60]))

# --------------------------------------------------------------------------
# 3. New queue items from this run's findings.
# --------------------------------------------------------------------------
NEW_ITEMS = [
    {
        "type": "fix_pipeline", "priority": 1, "added": TODAY,
        "target": "DRIVE THE UNSOURCED-ENDPOINT RATCHET DOWN, STARTING WITH "
                  "build_gap_deep_dives.py. audit_endpoint_value_agreement.py measured it "
                  "this run: 46 endpoint-values live in builder source and only THREE carry "
                  "a citation in the same statement. 35 carry none (post-correction count). "
                  "21 of them were in build_gap_deep_dives.py before today's repair. This is "
                  "the condition that let 'Belatacept 70% at 10yr' be wrong for months -- it "
                  "was never mis-cited, it was never cited. The ratchet now blocks NEW ones; "
                  "it does nothing about the backlog. Work the largest file first and lower "
                  "the baseline each run. NOTE the second-order effect: every value that "
                  "gains a citation also enters the conflict check's reach, which is dormant "
                  "today only because so little is attributed.",
    },
    {
        "type": "audit_gap", "priority": 1, "added": TODAY,
        "target": "RECONCILE THE REMAINING THREE 10-YEAR ISLET FIGURES. Today's repair fixed "
                  "the per-drug invention and the 6/10-vs-70% contradiction, but "
                  "Islet_Transplant_Analysis.html still publishes FOUR distinct 10-year "
                  "insulin-independence figures: 20% (Edmonton/CITR, sourced, n=1477), 70% "
                  "(Wisel, sourced, n=10), 55% (the plotted belatacept curve endpoint, "
                  "flagged 2026-09-14 and NOT CHANGED since) and '20-30%' (unsourced, cohort "
                  "unstated). The 55% curve is the sharpest problem: the page plots one "
                  "trajectory and states another number in prose beside it. PMID 42739778 "
                  "(ingested today, J Clin Med 2026 review of islet transplant outcomes) may "
                  "carry a registry figure that settles which cohort '20-30%' means.",
    },
    {
        "type": "fix_pipeline", "priority": 2, "added": TODAY,
        "target": "NARROW THE 'oxidative stress + diabetes + combination' SWEEP QUERY. It "
                  "returned exactly one paper this week and it was an oncology study "
                  "(metformin + pyrotinib in HER2-positive cancer, PMID 42744965). The query "
                  "matches any paper containing a diabetes DRUG, not papers about a diabetes "
                  "INTERVENTION. Add a MeSH constraint on Diabetes Mellitus as the studied "
                  "condition. Check the other six sweep queries for the same failure before "
                  "editing just this one -- 'verapamil' and 'dapagliflozin+colchicine' "
                  "returned zero this week, which may mean the window is right or may mean "
                  "they are too narrow to ever fire.",
    },
    {
        "type": "vet_papers_batch", "priority": 2, "added": TODAY,
        "target": "VET THE FIVE PAPERS INGESTED 2026-09-21 (42738899, 42739778, 42760903, "
                  "42753472, 42739042). Identity is already verified live; what is NOT done "
                  "is the claims check. THREE OF THE FIVE ARE REVIEWS and one is a plant-"
                  "extract preclinical study -- none is primary clinical evidence, and none "
                  "should be allowed to raise a path or gap grade. Record that explicitly "
                  "when vetting, because the failure mode here is a review's summary of a "
                  "trial being ingested as if it were the trial.",
    },
]
state["work_queue"].extend(NEW_ITEMS)

# --------------------------------------------------------------------------
# 4. Run history.
# --------------------------------------------------------------------------
state["run_history"].append({
    "date": TODAY,
    "day": "Monday",
    "environment": "HEALTHY. Sandbox mount, Python, git read/commit all functional. "
                   "git push still has no credential.",
    "queue_items_processed": 5,
    "papers_ingested": len(added),
    "papers_screened_out": len(SCREENED_OUT),
    "builders_fixed": 1,
    "gates_added": 1,
    "gates_discarded_before_shipping": 1,
    "p0_items_closed": len(closed),
    "changes_pushed": False,
    "summary":
        "THE HUB PUBLISHED TWO DRUG-SPECIFIC SUCCESS RATES THAT ITS SOURCE NEVER REPORTED, "
        "AND IT BUILT THEM OUT OF ONE COHORT MEASURED TWICE. Wisel et al., Transpl Int 2023 "
        "(PMID 37359825) is ten consecutive T1D islet recipients, five on belatacept and "
        "five on efalizumab. Its abstract says 70% (four EFA, three BELA) were insulin "
        "independent at 10 years and 60% at mean follow-up 13.3 years -- the same ten "
        "people, twice. build_gap_deep_dives.py published 'Belatacept 70% at 10yr, "
        "Efalizumab 60% at 13.3yr', which converts a difference of TIMEPOINT into a "
        "difference of DRUG, manufactures two per-drug rates that do not exist in the "
        "paper, and assigns belatacept the better number when efalizumab in fact "
        "contributed MORE of the seven responders (four versus three). The same invention "
        "appeared a second time in clinical_pipeline. A third error in the same file pinned "
        "the 13.3-year numerator to the 10-year endpoint ('6/10 insulin-independent at 10 "
        "years'), so the file simultaneously published 70%-at-10-years and 6/10-at-10-years "
        "for one paper, 34 lines apart. A fourth line promised a 'Belatacept comparative "
        "efficacy' study that does not exist: the paper the hub relies on has no comparator "
        "arm at all. Also unstated anywhere: three of the seven ten-year successes got there "
        "via PANCREAS-after-islet transplant and are therefore back on a calcineurin "
        "inhibitor -- in a field whose entire claim is calcineurin-sparing. "
        "WHY EIGHTY-ODD GREEN GATES SAW NONE OF IT: every gate in this repository scores ONE "
        "assertion against ONE source. 37359825 is a real PMID, correctly titled, correctly "
        "attributed to Wisel, genuinely about belatacept and islet transplant -- it passes "
        "the identifier gate, the title gate, the surname gate, the subject gate and the "
        "trial-phase gate individually. A contradiction is not a property of any single "
        "claim, so no quantity of per-claim gates can ever see one. build_islet_outcomes.py "
        "had carried the CORRECT pooled reading, with denominators, since 2026-09-14. The "
        "repository held the right answer and the invented one at the same time, in two "
        "files, both green. "
        "THE NEW GATE'S FIRST DESIGN WAS WRONG AND WAS THROWN AWAY, WHICH IS THE MORE USEFUL "
        "HALF OF THIS RUN. Version one associated a value with the sole PMID within 900 "
        "characters. Its first measurement reported a conflict: PMID 40544428 at one year "
        "holding 61%, 61%, 67%. That is not a defect -- 61% is Edmonton and 67% is LANTIDRA, "
        "two different cohorts correctly having different one-year rates near one citation. "
        "The gate had manufactured a contradiction out of proximity, which is exactly the "
        "failure its own docstring claimed to have made impossible, and exactly what the "
        "2026-09-15 surname gate (103 reported, nearly all invented) and the 2026-09-18 "
        "coordinate gate had already taught. Rewritten so attribution is EXPLICIT ONLY: a "
        "value belongs to an identifier when the author wrote them in the same statement. "
        "Nothing is inferred from distance. "
        "THAT HONESTY COST THE GATE ITS GRIP ON THE DEFECT THAT MOTIVATED IT, AND MEASURING "
        "WHY IS THE REAL FINDING. Under the strict rule the conflict check is silent on "
        "37359825, because only one statement about it carries a PMID. So: 46 endpoint-"
        "values exist across builder source, and THREE carry a citation in the same "
        "statement. Thirty-five carry none. 'Belatacept 70% at 10yr' was never mis-cited -- "
        "it was never cited, and neither is almost any clinical percentage this hub "
        "publishes. A reader meets a number with no source, no denominator and no cohort, "
        "and it looks authoritative only because of the company it keeps. The gate ships "
        "with a ratchet on that count: it may fall, it must never rise, so a new uncited "
        "clinical percentage now fails the build the day it is added. The conflict half is "
        "dormant by construction and becomes load-bearing only as the ratchet drives the "
        "backlog down. "
        "NINE P0 ITEMS WERE ONE REAL PROBLEM AND EIGHT RESTATEMENTS OF TWO DEAD ONES. Tested "
        "by command this run, not inherited from a report: the sandbox mount works (four "
        "items describing an outage that ended 2026-09-15, closed); .git/index.lock still "
        "cannot be unlinked but sandbox_git_commit.sh routes around it, so the request to "
        "have a human clear it is obsolete (closed); and `git push --dry-run` still fails "
        "for want of a credential, with 117 commits unpushed, up from 101 on 2026-09-06 "
        "(KEPT -- it is the only genuine P0, now a single item instead of three). Each run "
        "had been adding a new P0 rather than testing the old one, so the queue's top was "
        "nine items deep in text that no longer described the machine it ran on. "
        "The scheduled-task file's own Step 4 remains stale and nearly cost real data today: "
        "it instructs deletion of 'PMIDs above 42000000 (fabricated)', while the live "
        "ceiling is 42763307 and all five papers ingested this Monday sit above 42000000 "
        "and are real.",
    "verification":
        "Wisel abstract fetched live from eutils this run and quoted verbatim in both the "
        "builder comment and the gate docstring -- the correction is checkable against the "
        "primary source without re-fetching. New gate proven in BOTH directions on a "
        "fixture: it fires on 70%-vs-6/10 at 10 years for one PMID, and stays silent on the "
        "60%-at-13.3-years statement (different endpoint) and on Edmonton-61% vs "
        "LANTIDRA-67% at one year (different PMIDs) -- the two discriminations whose absence "
        "created the original defect and the discarded version's false positive "
        "respectively. Repaired HTML re-grepped after rebuild: the three invented strings "
        "are absent from Dashboards/ AND docs/Dashboards/ (count 0), and the pooled text "
        "with its denominator is present in both. Pipeline stages compile / "
        "endpointagreement / deepdives / islet / syncdocs all [OK]; 158 builders parse.",
})

state["last_run"] = TODAY
state["last_updated"] = TODAY

with open(STATE, "w", encoding="utf-8") as fh:
    json.dump(state, fh, indent=2, ensure_ascii=False)

print("papers ingested   :", added)
print("screened out      :", list(SCREENED_OUT))
print("P0 items closed   :", len(closed), closed)
print("P0 items kept     :", len(kept))
for d, t in kept:
    print("   KEPT", d, t)
print("new queue items   :", len(NEW_ITEMS))
print("queue length      :", len(state["work_queue"]))
