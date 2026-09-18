#!/usr/bin/env python3
"""
_close_run_2026_09_18.py
========================

State update for the 2026-09-18 daily iteration.

WHAT THIS RUN DID, in one line each:

  1. Cleared the surname gate's two LIVE mismatches. Both were in
     build_nutrition_lada.py and both turned out to be bigger than a surname.
  2. Built, MEASURED and scoped the computed-value citation gate the
     2026-09-13 queue item asked for; gave it a permanent known-positive
     fixture because its original live positive had already been repaired.
  3. Found and fixed a DEFECT IN THE COORDINATE GATE ITSELF: it was failing
     the pipeline on two citations the repository had written correctly, and
     its own probe output contained the disproof.

Run with: python Analysis/Scripts/_close_run_2026_09_18.py
"""

import json
import os
import shutil
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.abspath(os.path.join(HERE, "..", "Results", "agent_state.json"))
TODAY = "2026-09-18"


def main():
    with open(STATE, "r", encoding="utf-8") as fh:
        s = json.load(fh)

    bak = STATE + ".bak_" + TODAY
    if not os.path.exists(bak):
        shutil.copyfile(STATE, bak)

    # ------------------------------------------------------------------
    # 1. PAPER-LEVEL FINDINGS
    #    Two live citations were repaired today. Neither was a bare surname
    #    error; the surname was the thread that led to the rest.
    # ------------------------------------------------------------------
    papers = s.setdefault("papers", {})

    p = papers.setdefault("25940230", {})
    p["status"] = "FLAGGED"
    p["last_checked"] = TODAY
    p.setdefault("issues_found", []).append(
        "2026-09-18 REPAIRED IN PLACE, THREE DEFECTS ON ONE CITATION. "
        "25940230 is Martinez-Gonzalez MA, Salas-Salvado J, Estruch R, "
        "Corella D, Fito M, Ros E; PREDIMED Investigators, 'Benefits of the "
        "Mediterranean Diet: Insights From the PREDIMED Study', Prog "
        "Cardiovasc Dis 2015;58(1):50-60 - an OVERVIEW of the trial, not the "
        "trial report. build_nutrition_lada.py published it (a) attributed to "
        "'Salas-Salvado et al.', who is the second author, (b) described as a "
        "'landmark trial', and (c) sourcing 'reduced new-onset type 2 "
        "diabetes by 30% ... with extra-virgin olive oil or nuts'. "
        "THE 30% IS THE CARDIOVASCULAR NUMBER. The abstract in this "
        "repository's own cache reads: 288 CVD events, HR 0.70 for both "
        "MedDiets; and separately, for incident diabetes, 273 cases among "
        "3,541 non-diabetic participants, HR 0.60 (0.43-0.85) for "
        "MedDiet+EVOO and HR 0.82 (0.61-1.10) for MedDiet+nuts. So the "
        "diabetes effect was 40%, not 30%, and it was significant in ONE arm "
        "only - the page asserted it for both. A trailing claim that "
        "'PREDIMED-Plus showed sustained prevention over 6+ years' was "
        "withdrawn: PREDIMED-Plus is a separate energy-restricted trial and "
        "is not reported by this citation. Both occurrences (lines 485 and "
        "~816) re-sourced with denominators and confidence intervals visible."
    )

    p = papers.setdefault("34021020", {})
    p["status"] = "FLAGGED"
    p["last_checked"] = TODAY
    p.setdefault("issues_found", []).append(
        "2026-09-18 REPAIRED IN PLACE. A POPULATION MISATTRIBUTION, WHICH IS "
        "THE DEFECT CLASS THIS REPOSITORY HAS FOUND MOST OFTEN. "
        "build_nutrition_lada.py headed this entry 'GAD-Alum Immunotherapy in "
        "LADA'. 34021020 is DIAGNODE-2, which enrolled 109 patients aged "
        "12-24 with recent-onset TYPE 1 DIABETES (duration 7-193 days). LADA "
        "is adult-onset. Two further errors on the same entry: the paper was "
        "attributed to 'Casas/Ludvigsson' when Ludvigsson J is first author, "
        "and the result was described as 'dose-dependent C-peptide "
        "preservation' when the trial tested a SINGLE dose (4 ug x 3) and the "
        "subgroup effect was by HLA DR3-DQ2 GENOTYPE, not by dose. "
        "Re-sourced with the real numbers: primary endpoint NOT met in the "
        "full analysis set (TER 1.091, 95% CI 0.845-1.408, P=0.50); DR3-DQ2 "
        "subgroup TER 1.557 (1.126-2.153), P=0.0078 on n=29 vs 17. "
        "ALSO ADDED, because another file in this repo already knew it and "
        "this one did not: the confirmatory DIAGNODE-3 Phase 3 was closed for "
        "futility in 2026. The page was publishing a promising subgroup "
        "signal with no mention that its replication had failed. "
        "And the correction's own first draft was wrong - it claimed no "
        "GAD-alum trial in this corpus enrolled a LADA population. "
        "build_data_dictionary.py names Agardh et al., Diabetologia 2009 "
        "(PMID 19404608), n=47 adult-onset autoimmune diabetes, primary "
        "outcome SAFETY. Corrected before publishing to match the data "
        "dictionary's wording: no adequately powered LADA-specific EFFICACY "
        "trial has reported."
    )

    # ------------------------------------------------------------------
    # 2. DOCTRINE NOTES
    # ------------------------------------------------------------------
    dn = s.setdefault("doctrine_notes", {})

    dn["2026-09-18_gate_failing_on_correct_prose"] = (
        "A GATE FAILED THE PIPELINE ON TWO CITATIONS THE REPOSITORY HAD "
        "WRITTEN CORRECTLY, AND THE DISPROOF WAS IN THE GATE'S OWN OUTPUT. "
        "audit_citation_coordinates.py reported two live POINTS_ELSEWHERE: "
        "build_health_equity.py:1281 (PMID 36215990 asserted at Lancet "
        "Diabetes Endocrinol 2022;10(10):741) and verify_2026_09_13_repairs.py"
        ":37 (PMID 22336824 asserted at JAMA Oncol 2018;4(7):994). Both were "
        "artifacts of window cutting: the coordinate belongs to the PMID "
        "cited a few lines EARLIER in the same block (36113507 and 29710129 "
        "respectively), and the gate's own PROBE line said so verbatim - "
        "'coordinate resolves to PMID 36113507' - while the gate failed "
        "anyway. It had computed the answer and not consulted it. "
        "FIX: harvest() now carries every other PMID within 800 chars; if the "
        "probe resolves the coordinate to one of them, the verdict is "
        "AMBIGUOUS_PAIRING - printed in full, never failed. This does not "
        "mask a real misattribution, because a fabricated coordinate resolves "
        "to a paper that is NOT cited nearby, and the neighbouring PMID's own "
        "coordinate is still harvested and checked independently. "
        "THE GENERAL LESSON, and it is the third time a variant of this has "
        "been recorded here: WHEN A GATE FAILS, READ ITS OUTPUT BEFORE "
        "EDITING THE REPOSITORY. The obvious response to a red coordinate "
        "gate is to 'fix' the citation. Doing that here would have replaced "
        "two correct citations with two wrong ones and left the gate green - "
        "a silent corruption produced by obeying a gate."
    )

    dn["2026-09-18_a_gate_with_no_live_positive"] = (
        "THE COMPUTED-VALUE GATE WAS BUILT AFTER ITS ONLY LIVE POSITIVE HAD "
        "ALREADY BEEN REPAIRED, WHICH MEANS A CLEAN RUN PROVES NOTHING. "
        "The 2026-09-13 defect (build_lada_diagnostic_model.py:763-766, a "
        "PMID inside the same f-string as an interpolated computed cost) was "
        "fixed before audit_computed_value_citations.py existed. A gate that "
        "has only ever returned zero is indistinguishable from a gate that "
        "does not work. Rather than trust the zero, the original defect was "
        "reproduced verbatim in _tmp_gate_known_positive.py, which the "
        "audit's own SKIP_PREFIXES excludes from normal runs and which is "
        "reachable only by calling scan_file() on it directly. Both lines are "
        "reported COMPUTED, confirmed 2026-09-18. EVERY GATE ADDED HERE FROM "
        "NOW ON SHOULD SHIP WITH A FIXTURE IT MUST CATCH, not just a live "
        "count it happens to clear."
    )

    dn["2026-09-18_measure_first_earned_its_keep_again"] = (
        "THE COMPUTED-VALUE GATE'S FIRST MEASUREMENT WAS 13 HITS AND ALL 13 "
        "WERE FALSE. The first implementation asked only whether a PMID "
        "appeared anywhere in the same f-string - but the builders here write "
        "the ENTIRE page as one f-string, so {COLORS['bg']} at the top was "
        "flagged against a PMID four thousand characters below. Adding a "
        "180-character proximity window took it to 4. Excluding verify_/"
        "check_/reconcile_ scripts, which print counts ABOUT PMIDs "
        "(f\"{len(live_bad)} LIVE link(s) to PMID 34763823 remain\") and are "
        "the opposite of the defect, took it to 1. Had this shipped as a "
        "gate on the first measurement it would have failed the pipeline on "
        "13 non-defects and been switched off within a day. Standing "
        "instruction confirmed for the fourth time: MEASURE AND REPORT THE "
        "HIT COUNT BEFORE WIRING A GATE IN."
    )

    dn["2026-09-18_a_gate_that_can_never_go_green"] = (
        "The surname gate's four remaining mismatches after today's repairs "
        "were ALL in frozen archive - dated ACTION_REQUIRED and "
        "iterate_run_report markdown, and a _close_run script - where the "
        "'mismatch' is this repository quoting a defect it had just fixed. "
        "One is literally a fenced HTML block showing the bad anchor. Those "
        "files are history and must not be rewritten; editing a dated run "
        "report to clear a gate is the failure this repo audits for. But left "
        "in the MISMATCH bucket they guarantee the count never reaches zero, "
        "and a gate that can never go green is a gate that gets ignored. "
        "Resolved with a SURFACE SPLIT, not an exclusion: every finding is "
        "still printed and still written to the JSON; only the headline count "
        "and the --gate exit code are scoped to the live publishing surface. "
        "Deliberately NOT done: adding loose strings to CORRECTION_MARKERS. "
        "The note at the top of that tuple warns against exactly that, "
        "because a marker silences a class of finding everywhere, whereas a "
        "surface split silences nothing."
    )

    # ------------------------------------------------------------------
    # 3. WORK QUEUE
    # ------------------------------------------------------------------
    q = s.setdefault("work_queue", [])

    # Close / downgrade what today finished.
    closed = s.setdefault("closed_queue_items", [])
    for item in q:
        t = str(item.get("target", ""))
        if item.get("type") == "verify_citations" and t.startswith(
                "AUDIT AUTHOR SURNAMES"):
            item["status"] = "resolved_2026-09-18"
            closed.append({
                "date": TODAY, "type": item.get("type"),
                "target": t[:160],
                "resolution":
                    "Gate was already built (2026-09-16) and measuring. Its "
                    "two LIVE mismatches were repaired today - both in "
                    "build_nutrition_lada.py, both larger than a surname (see "
                    "papers 25940230 and 34021020). Live surface now reads 0. "
                    "Four archival hits split into a reported-not-failed "
                    "bucket. Gate is a candidate for --gate promotion next "
                    "run, once one run has seen it stay green on real work.",
            })
        if item.get("type") == "fix_pipeline" and t.startswith(
                "A CITATION IS BEING ATTACHED TO THE MODEL'S OWN OUTPUT"):
            item["status"] = "resolved_2026-09-18"
            closed.append({
                "date": TODAY, "type": item.get("type"),
                "target": t[:160],
                "resolution":
                    "audit_computed_value_citations.py built, measured "
                    "(13 -> 4 -> 1 as the false-positive modes were removed), "
                    "proven on a permanent fixture reproducing the original "
                    "2026-09-13 defect, and wired into "
                    "run_quality_improvements.py as stage 'computedcite' in "
                    "--measure mode. The single remaining hit is a "
                    "synthetic-data report whose PMID sources the effect "
                    "sizes, not the sample count.",
            })

    def add(priority, typ, target):
        if any(str(i.get("target", "")).startswith(target[:70]) for i in q):
            return
        q.append({"priority": priority, "type": typ, "added": TODAY,
                  "target": target})

    add(1, "fix_pipeline",
        "TWO EVIDENCE STORES DISAGREE ABOUT GAP #15, AND NEITHER IS MARKED "
        "AUTHORITATIVE. agent_state.json records gaps['15'].corpus_evidence_"
        "points = 1; gap_evidence.json, which is what "
        "audit_gap_subject_coverage.py reads, records 0 papers for the same "
        "gap. The gate therefore reports 'Tier BRONZE with ZERO evidence "
        "papers' while the state file says the gap has evidence. This is the "
        "same shape as the 2026-09-09 finding that one file carried two "
        "incompatible definitions of one trial, except it is across stores "
        "rather than within a file. DECIDE WHICH STORE IS CANONICAL FOR THE "
        "EVIDENCE COUNT and make the other derive from it, or state in both "
        "that they count different things and what those things are. Until "
        "then any tier decision on Gap #15 rests on an unresolved "
        "disagreement, which is why the demotion question below is blocked "
        "on this.")

    add(2, "audit_gap",
        "DECIDE GAP #14 AND GAP #15's TIER - THE GATE HAS ASKED FIVE TIMES "
        "AND THE ANSWER IS OVERDUE, NOT UNKNOWN. audit_gap_subject_coverage.py "
        "reports both as [HIGH] 'Tier BRONZE with ZERO evidence papers. A tier "
        "above EXPLORATORY asserts evidential standing this gap does not "
        "have.' Doctrine (RESEARCH_DOCTRINE.md:212) defines BRONZE as SINGLE "
        "SOURCE. Gap #14's own audit history is the strongest argument for "
        "demotion available: five consecutive documented nulls, most recently "
        "2026-09-06, with the all-time PubMed search returning exactly one "
        "record - PMID 35784546, a PROTOCOL for NCT04698330, which reports no "
        "results. A protocol is not a source in the sense BRONZE means. "
        "NOT DONE TODAY ON PURPOSE: demoting a published tier changes what "
        "the site asserts, Gap #15's count is disputed by the item above, and "
        "this run had already spent its verification budget on three citation "
        "repairs. It should be the first substantive item next run.")

    add(2, "verify_citations",
        "RE-MEASURE THE COORDINATE GATE'S REACH NOW THAT IT NO LONGER "
        "MIS-PAIRS. Today's AMBIGUOUS_PAIRING fix moved 2 of 8 suspects out "
        "of the failing bucket, and the gate's checked count has grown from "
        "119 (2026-09-08) to 151 without anyone measuring what fraction of "
        "bibliographic coordinates in the repo it actually sees. State the "
        "coverage fraction the way audit_prose_citation_titles.py states its "
        "26.3%. TWO POINTS_ELSEWHERE REMAIN, both in _run_2026_08_27.py and "
        "both audit-trail so they do not fail: PMID 2873396 asserted at "
        "Diabetes 2024;73(6):823 (resolves to 38349844) and PMID 37221401 "
        "asserted at Nat Rev Endocrinol 2023;19(7):377 (resolves to 37202589, "
        "two pages off). They were NOT excused by the 800-char ownership scan, "
        "which means either the owning PMID sits further away than that or "
        "they are genuine. Read them before widening the radius - widening to "
        "make a bucket empty is how a gate gets quietly disabled.")

    add(3, "fix_pipeline",
        "PROMOTE 'surnames' AND 'computedcite' FROM --measure TO --gate, but "
        "only after a run in which each stays green on work it did not "
        "itself perform. Both are green as of 2026-09-18: surnames reports 0 "
        "live mismatches, computedcite reports 1 documented non-defect. The "
        "standing reason to wait one run is that today's zero on 'surnames' "
        "was produced by today's own repairs, and a gate that has only been "
        "green on its author's work has not been tested.")

    # ------------------------------------------------------------------
    # 4. RUN HISTORY
    # ------------------------------------------------------------------
    s.setdefault("run_history", []).append({
        "date": TODAY,
        "summary": (
            "A GATE FAILED THE PIPELINE ON TWO CITATIONS THIS REPOSITORY HAD "
            "WRITTEN CORRECTLY, AND THE DISPROOF WAS PRINTED IN THE GATE'S "
            "OWN OUTPUT. audit_citation_coordinates.py reported 2 live "
            "POINTS_ELSEWHERE - build_health_equity.py:1281 and "
            "verify_2026_09_13_repairs.py:37 - while its own PROBE line for "
            "each said the coordinate resolves to a PMID cited a few lines "
            "earlier in the same block (36113507 and 29710129). Both were "
            "window-cutting artifacts. The obvious response, editing the "
            "citation to satisfy the gate, would have replaced two correct "
            "citations with two wrong ones and turned the stage green. Fixed "
            "by having the gate consult its own probe: harvest() now carries "
            "every PMID within 800 chars and a coordinate that resolves to "
            "one of them is AMBIGUOUS_PAIRING - printed, never failed. "
            "THE SURNAME GATE'S TWO LIVE MISMATCHES WERE CLEARED AND BOTH "
            "WERE MUCH LARGER THAN A SURNAME. (1) PMID 25940230 in "
            "build_nutrition_lada.py: attributed to Salas-Salvado (second "
            "author; it is Martinez-Gonzalez), described as a landmark TRIAL "
            "(it is an overview), and sourcing '30% reduction in new-onset "
            "T2D with EVOO or nuts'. 30% is PREDIMED's CARDIOVASCULAR hazard "
            "reduction. The diabetes result, in this repo's own cached "
            "abstract, is HR 0.60 (0.43-0.85) for EVOO and HR 0.82 "
            "(0.61-1.10) for nuts among 3,541 participants - 40%, in one arm "
            "only. A 'PREDIMED-Plus ... 6+ years' claim was withdrawn as "
            "belonging to a different trial. (2) PMID 34021020 in the same "
            "file, headed 'GAD-Alum Immunotherapy in LADA' for DIAGNODE-2, "
            "which enrolled 109 patients aged 12-24 with recent-onset T1D; "
            "also 'Casas/Ludvigsson' for a paper Ludvigsson leads, and "
            "'dose-dependent' preservation for a single-dose trial whose "
            "subgroup was defined by HLA genotype. Re-sourced with the "
            "primary endpoint's actual failure (TER 1.091, P=0.50) and with "
            "the DIAGNODE-3 futility closure that two other files in this "
            "repository already knew about and this one did not. The "
            "correction's own first draft asserted no GAD-alum trial here "
            "enrolled a LADA population; build_data_dictionary.py names "
            "Agardh 2009 (PMID 19404608, n=47, safety primary). Caught and "
            "narrowed before publishing. "
            "THE COMPUTED-VALUE GATE ASKED FOR ON 2026-09-13 WAS BUILT, AND "
            "ITS FIRST MEASUREMENT WAS 13 HITS OF WHICH 13 WERE FALSE - the "
            "builders write whole pages as single f-strings, so any PMID on "
            "the page paired with any interpolation on the page. A "
            "180-character proximity window took it to 4; excluding "
            "verify_/check_/reconcile_ diagnostics took it to 1, a "
            "synthetic-data report whose PMID sources effect sizes rather "
            "than the sample count. Because the original live defect had "
            "already been repaired, the gate would otherwise ship having "
            "never caught anything, so the 2026-09-13 defect was reproduced "
            "verbatim as a permanent fixture it must always flag."
        ),
        "papers_vetted": 0,
        "papers_repaired": 2,
        "paths_validated": 0,
        "gates_added": ["audit_computed_value_citations.py"],
        "gates_repaired": ["audit_citation_coordinates.py",
                           "audit_prose_author_surnames.py"],
        "counts": {
            "live_citation_defects_fixed": 3,
            "distinct_errors_inside_those_3_citations": 8,
            "computedcite_measurements": [13, 4, 1],
            "computedcite_fixture_positives": 2,
            "coordinate_gate_live_failures_before": 2,
            "coordinate_gate_live_failures_after": 0,
            "coordinates_checked": 151,
            "surname_live_mismatches_before": 2,
            "surname_live_mismatches_after": 0,
            "surname_archival_reported": 4,
            "builders_that_do_not_parse": 0,
            "pipeline_stages_run": 76,
            "pipeline_stages_ok": 74,
        },
        "environment": (
            "HEALTHY for compute, UNCHANGED for publishing. Python ran; "
            "extraction and 76 of 79 pipeline stages executed. THREE stages "
            "were not run or did not pass, none of them new: (1) 'gapdata' "
            "skipped again - it is a 240s network-bound slice and the host "
            "caps a tool call well below that; (2) 'gapsubject' FAILS and was "
            "already failing on 2026-09-07 with the same 9 findings, the "
            "sharpest being Gap #14 and Gap #15 at BRONZE with zero stored "
            "evidence papers; (3) 'publishgate' FAILS ON PURPOSE and is the "
            "P0 item below. The full suite also cannot be run in one call - "
            "it exceeds the per-call cap - so it was run in four explicit "
            "stage batches, which is worth knowing because a future run that "
            "invokes run_quality_improvements.py bare will time out and may "
            "report partial success."
        ),
        "blocking": (
            "PUSH. 112 commits unpushed; origin/main tip is 2026-04-20, now "
            "150 days old; 38 of 39 files under docs/ are wrong for a reader "
            "(4 return 404, 34 are stale). The sandbox CAN commit - the "
            "GIT_INDEX_FILE workaround still holds - but it cannot "
            "authenticate: HTTPS remote, no credential helper, no "
            "~/.git-credentials, no GH_TOKEN. ONE COMMAND FROM WINDOWS: "
            "cd 'C:\\Users\\justi\\OneDrive\\Diabetes_Research' ; git push . "
            "Everything this run repaired is real in the working tree and "
            "invisible on the site until that happens."
        ),
    })

    s["last_run"] = TODAY
    s["last_updated"] = TODAY

    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(s, fh, indent=1, ensure_ascii=False)

    print("state updated for", TODAY)
    print("  papers flagged/repaired :", 2)
    print("  doctrine notes added    :", 4)
    print("  queue items closed      : 2")
    print("  queue items added       : 4")
    print("  backup                  :", os.path.basename(bak))


if __name__ == "__main__":
    main()
