#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_run_2026_08_27.py  --  daily iteration, 2026-08-27 (Thursday).

Work-queue items closed this run:
  * verify_citations (P1) : the 14-mismatch prose backlog -> 2 (both known
                            gate false positives, documented below)
  * NEW GATE (6th class)  : audit_citation_coordinates.py, wired into
                            run_quality_improvements.py, GREEN at 107/107
  * NEW GATE (7th class)  : audit_citation_load_bearing.py, standalone
  * credibility sweep     : clean; the >42000000 fabrication rule re-confirmed
                            stale against a live PMID ceiling of 42,649,123

Every PMID, title, journal, volume and page below was resolved LIVE against
NCBI esummary/esearch on 2026-08-27. Nothing here is recalled.
"""

import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE = os.path.join(REPO, "Analysis", "Results", "agent_state.json")
TODAY = "2026-08-27"

with open(STATE, "r", encoding="utf-8") as fh:
    state = json.load(fh)

# ---------------------------------------------------------------------------
# 1. DOCTRINE: two new citation-defect classes, both structurally invisible
#    to all six gates that existed this morning.
# ---------------------------------------------------------------------------
state.setdefault("doctrine_notes", {})

state["doctrine_notes"]["citation_defect_class_6_coordinates"] = {
    "added": TODAY,
    "name": "INVENTED BIBLIOGRAPHIC COORDINATES",
    "statement": (
        "A citation can carry a resolving, on-topic, non-retracted PMID, be "
        "described accurately by the prose around it, and still assert a "
        "journal/volume/page coordinate that matches no PubMed record. The "
        "narrative is right and the numbers are invented, which is precisely "
        "the combination every prior gate passes: audit_prose_citation_titles "
        "scores the NARRATIVE, and the narrative is the true part."
    ),
    "canonical_example": (
        "build_gka_lada.py published 'Diabetes. 2009 Jul;58(7):1416-28. "
        "PMID:19373249' under prose correctly describing Matschinsky's 2009 "
        "glucokinase review. PMID 19373249 is Nat Rev Drug Discov "
        "2009;8(5):399-416. Diabetes vol 58 issue 7 exists and holds 34 "
        "articles; page 1416 is not among them."
    ),
    "found_by": "audit_citation_coordinates.py",
    "scale_on_first_run": (
        "11 suspect of 94 coordinates, across build_gka_lada.py, "
        "build_data_dictionary.py, build_gka_landscape.py. After repair: "
        "107/107 OK."
    ),
    "method_note": (
        "A NEGATIVE probe result is what licenses the word NONRESOLVING, so "
        "the negative must be earned. PubMed's [ta] field indexes NLM "
        "abbreviations and only SOME full titles, and returns an empty "
        "idlist with NO phrasesnotfound error for the rest. Measured today: "
        "'Nature Reviews Endocrinology'[ta] -> 3059 records, but "
        "'Journal of Clinical Investigation'[ta] -> 0 and "
        "'Trends in Endocrinology & Metabolism'[ta] -> 0, all three being "
        "real indexed journals. The gate's first draft called three "
        "build_data_dictionary.py citations NONRESOLVING on that basis - a "
        "verdict reached by a broken instrument, which would have remained "
        "'true' after any repair. Fixed by running a positive control on the "
        "journal token before trusting any negative."
    ),
}

state["doctrine_notes"]["citation_defect_class_7_load_bearing"] = {
    "added": TODAY,
    "name": "THE LOAD-BEARING CITATION",
    "statement": (
        "One real, on-topic, correctly-cited source attached to many distinct "
        "quantitative claims it does not contain. Every individual instance "
        "passes every gate, because every gate asks about the PAPER. This "
        "class is only visible when you ask about the CLAIM."
    ),
    "canonical_example": (
        "PMID 34763823 (Herman WH & Kuo S, '100 years of Insulin: Why is "
        "Insulin So Expensive and What Can be Done to Control Its Cost?', "
        "Endocrinol Metab Clin North Am 2021;50(3S):e21-e34) is cited 91 "
        "times across 91 DISTINCT claim contexts, including GLP-1 agonist "
        "pricing, SGLT2i launch pricing, GKA generic projections to "
        "2042-2045, drug development cost ($2.6B / $300M), CGM device cost, "
        "verapamil therapy cost, and the December 2024 Hikma semaglutide "
        "generic launch. It is a review of INSULIN pricing published in 2021."
    ),
    "found_by": "audit_citation_load_bearing.py",
    "automatable_part": (
        "TEMPORAL IMPOSSIBILITY is fully objective and is what the gate fails "
        "on: a paper cannot report an event that post-dates it. Restricted to "
        "RETROSPECTIVE claims - the first draft flagged a 2023 GBD paper "
        "projecting to 2050, which is what a GBD paper is for. Two filters "
        "are required together: the claim year must not be in the future, and "
        "the claim must not be phrased as a forecast."
    ),
    "judgement_part": (
        "Citation CONCENTRATION is reported, never failed. A landmark trial "
        "is legitimately cited often and the count alone cannot separate the "
        "two cases. Top concentrations measured today: 34763823 (91), "
        "29710129 CAR-T costs (81), 37909353 (47), 32175717 (39)."
    ),
    "human_call_required": True,
}

state["doctrine_notes"]["pmid_ceiling_is_not_a_constant"] = {
    "added": TODAY,
    "supersedes": "the 'PMIDs above 42000000 are fabricated' rule in the scheduled-task file",
    "statement": (
        "Re-confirmed independently today, two days after the 2026-08-25 "
        "note. The live PubMed ceiling measured by esearch sort=most+recent "
        "is 42,649,123, up from 42,626,404 on 2026-08-25 - roughly 11k new "
        "PMIDs per day. Both repo PMIDs above the old threshold resolved and "
        "matched their logged titles exactly: 42608595 (Rogers NM, "
        "Diabetologia 2026, belatacept/sirolimus islet transplantation) and "
        "42631883 (Elsayed MS, Mol Biol Rep 2026, rat myocardial injury). "
        "The sweep must compare against a ceiling QUERIED AT RUNTIME, never "
        "a hardcoded constant, or it will manufacture false fabrication "
        "reports at an accelerating rate."
    ),
}

state["doctrine_notes"]["gates_must_not_be_silenced_by_filename"] = {
    "added": TODAY,
    "statement": (
        "Wiring audit_citation_coordinates.py into the pipeline made it "
        "report, on its first run, the COMMENT in run_quality_improvements.py "
        "that documents why it exists - because that comment necessarily "
        "quotes the fabricated coordinate. The tempting fix, skipping "
        "audit_*.py and the runner by filename, would have opened a blind "
        "spot in files that also carry real citations. Instead the opt-out is "
        "an explicit CITATION-EXAMPLE marker written next to the example, so "
        "every suppression is visible in the diff and greppable. Exactly one "
        "exemption exists in the repo today. Silence must be requested by "
        "name, never inherited from a filename."
    ),
}

# ---------------------------------------------------------------------------
# 2. CITATION REPAIRS. Each pair was resolved live before it was written.
# ---------------------------------------------------------------------------
REPAIRS = [
    ("build_gka_lada.py", "33622669",
     "published as 'Nat Med. 2021 Mar;27(3):455-460'",
     "Klein KR et al. The SimpliciT1 Study. Diabetes Care 2021;44(4):960-968. "
     "Also downgraded 'Phase 2' to 'Phase 1b/2 adaptive', which is the design."),
    ("build_gka_lada.py", "35551292",
     "published as 'Zhu et al. Nat Med 2022 - SEED trial'",
     "Yang W et al., dorzagliatin ADD-ON to metformin = the DAWN trial, Nat Med "
     "2022;28(5):974-981. The two phase 3 trials were transposed."),
    ("build_gka_lada.py", "35551293",
     "published as 'Yang et al. Nat Med 2022 - DAWN trial'",
     "REMOVED. 35551293 is Klein KR, 'A new class of drug in the diabetes "
     "toolbox', Nat Med 2022;28(5):901-902, pubtype Comment. A News & Views "
     "commentary was being published as a phase 3 trial result. The real SEED "
     "trial is Zhu D et al. Nat Med 2022;28(5):965-973, PMID 35551294, now cited."),
    ("build_gka_lada.py", "24056026",
     "published as 'Park et al. J Diabetes Investig 2013 - GKA beta cell preservation'",
     "Oh YS et al., Eur J Pharm Sci 2014;51:137-45. Relabelled PRECLINICAL "
     "(INS-1 cell line), since it was listed among clinical evidence."),
    ("build_gka_lada.py", "19373249",
     "published as 'Diabetes. 2009 Jul;58(7):1416-28' - resolves to no record",
     "Matschinsky FM. Nat Rev Drug Discov 2009;8(5):399-416."),
    ("build_gka_lada.py", "14706052",
     "published as 'UKPDS Group. Diabet Med. 2004 Jan;21(1):31-7' supporting a "
     "baseline C-peptide of ~0.5-0.8 nmol/L",
     "WITHDRAWN, not re-attributed. 14706052 is Aronson D et al., 'Association "
     "between fasting glucose and C-reactive protein in middle-aged subjects', "
     "Diabet Med 2004;21(1):39-44 - not UKPDS, not about C-peptide - and the "
     "asserted page range 31-7 resolves to no record. No corpus source supports "
     "the 0.5-0.8 nmol/L figure, so the FIGURE was removed and the withdrawal "
     "is stated on the card. The qualitative claims are now sourced to UKPDS 25 "
     "(Turner R et al., Lancet 1997;350(9087):1288-93, PMID 9357409) and Li X "
     "et al. JCEM 2020;105(7) (PMID 32307525)."),
    ("build_gka_lada.py", "23835325",
     "published as 'Diabetes. 2013 Dec;62(12):4297-303 ... (LADA review)'",
     "Ilonen J et al., Diabetes 2013;62(10):3636-40, a PAEDIATRIC autoantibody "
     "cohort - not a LADA review. Coordinates and descriptor both corrected."),
    ("build_gka_lada.py", "38349844",
     "published as 'Palmer et al. Diabetes 2024'",
     "Latres E et al., Diabetes 2024;73(6):823-833."),
    ("build_drug_repurposing_screen.py", "1611143",
     "published as 'Feutren et al, Lancet 1986'",
     "The Feutren Lancet 1986 cyclosporine trial is PMID 2873396 "
     "(Lancet 1986;2(8499):119-24) and is now cited as such. 1611143 is Skyler "
     "JS & Rabinovitch A, J Diabetes Complications 1992;6(2):77-88, Miami "
     "Cyclosporine Diabetes Study Group - retained under its own identity."),
    ("build_data_dictionary.py", "30949058",
     "published as 'Frontiers in Diabetes 2019;29:1-24'",
     "Matschinsky FM & Wilson DF, Front Physiol 2019;10:148."),
    ("build_data_dictionary.py", "30303773",
     "published as 'Trends in Endocrinology & Metabolism 2018;29(10):725-737'",
     "Huising MO et al., Physiology (Bethesda) 2018;33(6):403-411."),
    ("build_data_dictionary.py", "24506867",
     "published as 'Journal of Clinical Investigation 2014;124(10):4017-4024'",
     "Gao T et al., Cell Metab 2014;19(2):259-71."),
    ("build_data_dictionary.py", "37202589",
     "published as 'Mathieu C et al. ... Nature Reviews Endocrinology "
     "2023;19(7):379-380'",
     "Speake C & Herold KC, Nat Rev Endocrinol 2023;19(7):377-378. The asserted "
     "page 379 resolves to a DIFFERENT paper, PMID 37221401 (Greenhill C, gut "
     "microbiota) - a POINTS_ELSEWHERE defect, not an invention."),
    ("build_data_dictionary.py", "36455116",
     "published as 'Florez JC. Precision medicine in diabetes: is it time? "
     "Diabetes Care 2022;45(12):3019-3032'",
     "Forouhi NG, 'Nutrition and Type 2 Diabetes: Computational Optimization "
     "Modeling to Expand the Evidence Base for South Asians', Diabetes Care "
     "2022;45(12):2811-2813. Different author, different title, different pages."),
    ("build_gka_landscape.py", "30949058",
     "published as 'Glucokinase as a glucose sensor and therapeutic target for "
     "diabetes mellitus. Diabetes Care. 2002;25(10):1897-1902'",
     "Same paper as above: Front Physiol 2019;10:148. The Diabetes Care 2002 "
     "coordinate resolves to no record. This one was found ONLY by the "
     "end-to-end check of published docs/ HTML, because the builder assembles "
     "it across a boundary the source-side scan did not model."),
    ("build_gka_landscape.py", "38783768",
     "published as 'Dorzagliatin SEED Trial (Phase 3, 52-week ...)' in two places",
     "Jiang Y et al., 'Recent drug development of dorzagliatin', J Diabetes "
     "2024;16(6):e13563 - a REVIEW. Regulatory-status claim re-sourced to Syed "
     "YY, Drugs 2022;82(18):1745-1750 (PMID 36449148); SEED correctly named as "
     "PMID 35551294."),
]

UNSOURCED = [
    ("build_gka_pricing.py",
     "SGLT2i launch pricing (2014) $5,000-$8,000/yr; generic pricing (2024+) "
     "$200-$400/yr; GKA generic precedent 2038-2042",
     "Citation to PMID 34763823 removed and the figures marked [UNSOURCED]. "
     "That paper is a review of INSULIN pricing published in 2021: it contains "
     "no SGLT2i prices and predates the 2024+ figures. Numbers retained, "
     "unsourced and visibly labelled, pending a primary pricing source."),
    ("build_gap_deep_dives.py",
     "Dorzagliatin China NRDL listing, Jan 2024 (4 places)",
     "Citation to PMID 36449148 removed. Syed, Drugs 2022, cannot report a "
     "January 2024 listing. Marked [UNSOURCED]."),
    ("build_gap_deep_dives.py",
     "Hikma semaglutide generic approved USA Dec 2024 at $3-5/day",
     "Citation to PMID 34763823 (2021) removed for the same reason."),
    ("build_trial_equity_mapper.py",
     "VX-880 projected $250-300K in 2035",
     "Relabelled [PROJECTION, not a sourced figure]. PMID 21323736 (Beckwith J "
     "et al., Clin Transplant 2012;26(1):23-33) is retained ONLY as the islet "
     "transplantation cost anchor it actually provides; the 2035 extrapolation "
     "is stated to be this project's, not that paper's."),
]

state.setdefault("audit_notes", []).append({
    "date": TODAY,
    "type": "citation_repair_batch",
    "repairs": [
        {"file": f, "pmid": p, "was": w, "now": n}
        for (f, p, w, n) in REPAIRS
    ],
    "unsourced_markings": [
        {"file": f, "claim": c, "action": a} for (f, c, a) in UNSOURCED
    ],
    "known_false_positives_remaining": [
        {"file": "build_treg_neuropathy.py", "line": 486, "pmid": "8366922",
         "why": "The citation is CORRECT - PMID 8366922 is the DCCT 1993 NEJM "
                "paper and the prose says '(DCCT, 1993)'. audit_prose_citation_"
                "titles compares against esummary's first author, which for a "
                "group-authored trial is 'Diabetes Control and Complications "
                "Trial Research Group / Nathan DM'. The gate needs corporate-"
                "authorship handling; the citation needs nothing."},
        {"file": "build_gka_pricing.py", "line": 460, "pmid": "32175717",
         "why": "The attribution 'Khan et al. 2020' is CORRECT in author and "
                "year. The gate scored scenario prose as an asserted title. "
                "Separately worth a human read: an epidemiology paper is a thin "
                "anchor for a revenue projection, though the prose does label "
                "it 'modeled estimate'."},
    ],
})

# ---------------------------------------------------------------------------
# 3. WORK QUEUE.
# ---------------------------------------------------------------------------
queue = state.get("work_queue", [])
state.setdefault("closed_queue_items", [])

CLOSED_MARKER = "FINISH THE PROSE-CITATION BACKLOG"
remaining = []
for item in queue:
    if CLOSED_MARKER in str(item.get("target", "")):
        item["closed"] = TODAY
        item["closed_note"] = (
            "14 -> 2. Twelve were real and are repaired; the two that remain "
            "are gate false positives, documented in audit_notes. The gate is "
            "still NOT wired into run_quality_improvements.py, deliberately - "
            "it would sit permanently red on two non-defects. The COORDINATE "
            "gate built today IS wired, because it is green at 107/107."
        )
        state["closed_queue_items"].append(item)
    else:
        remaining.append(item)

NEW_ITEMS = [
    {"priority": 1, "type": "user_action_required", "added": TODAY, "target":
     "HUMAN CALL: ONE INSULIN-PRICING REVIEW IS CARRYING 91 DISTINCT CLAIMS. "
     "PMID 34763823 (Herman & Kuo, '100 years of Insulin: Why is Insulin So "
     "Expensive', Endocrinol Metab Clin North Am 2021) is cited across 91 "
     "distinct claim contexts, including GLP-1 agonist pricing, SGLT2i launch "
     "and generic pricing, GKA generic projections to 2042-2045, drug "
     "development cost ($2.6B / $300M), CGM device cost (~$300), verapamil "
     "therapy cost ($50/yr), and the Dec 2024 Hikma semaglutide launch. It is "
     "a review of INSULIN pricing and contains essentially none of them. Four "
     "temporally-impossible instances were stripped and marked [UNSOURCED] "
     "today; the remaining ~87 are a presentation decision across the pricing "
     "dashboards and were NOT touched unattended. Three options: (a) source "
     "each figure properly, (b) mark the unsourceable ones [UNSOURCED] as was "
     "done for SGLT2i today, (c) withdraw the figures. Same reasoning as the "
     "2026-08-20 dose-label item: a citation that lends borrowed authority to "
     "91 claims is a credibility exposure larger than any single bad PMID, and "
     "restating it is not an unattended change. Full inventory with contexts: "
     "Analysis/Results/citation_load_bearing.json. NOTE the next three "
     "concentrations are 29710129 (81 claims, CAR-T costs), 37909353 (47) and "
     "32175717 (39) - the pattern is not confined to one paper."},

    {"priority": 1, "type": "fix_pipeline", "added": TODAY, "target":
     "SEAL THE REMAINING INTAKE DOORS BY CLASS, NOT BY NAME. Carried unchanged "
     "from 2026-08-25; NOT worked today because two higher-severity defect "
     "classes surfaced first. Three doors known: the index harvester (reads "
     "PMIDs out of comments and regex literals), verify_pmids.py (scans "
     "scripts independently of the index), and the two extractors (walk "
     "abstracts/ and fulltext/ directly). Build ONE shared corpus_membership.py "
     "owning not_corpus_pmids.json + FLAGGED + retractions, make every consumer "
     "import it, then add an audit that FAILS if any script reads "
     "abstracts_dir/fulltext_dir/the index without it. TODAY'S RUN ADDS "
     "EVIDENCE FOR THIS ITEM: audit_citation_coordinates.py and "
     "audit_citation_load_bearing.py are two MORE new readers of PMIDs, and "
     "both started life unguarded - exactly the pattern the item predicts."},

    {"priority": 2, "type": "verify_citations", "added": TODAY, "target":
     "TEACH audit_prose_citation_titles.py ABOUT CORPORATE AUTHORSHIP, THEN "
     "WIRE IT. The backlog is down to 2 and BOTH are gate artifacts. (1) PMID "
     "8366922 is the DCCT 1993 NEJM paper cited as '(DCCT, 1993)' - correct - "
     "but esummary's first author for a group-authored trial is the study "
     "group, so the author check can never pass. UKPDS, DCCT, ACCORD, ADVANCE "
     "and EDIC will all fail the same way. Fix: when esummary's author list "
     "contains a corporate entry (Group/Trial/Study/Consortium/Collaborative), "
     "accept a trial acronym appearing in the prose as author agreement. (2) "
     "PMID 32175717 'Khan et al. 2020' is correct in author and year; scenario "
     "prose was scored as an asserted title. Once both are handled the gate "
     "should be green and can join run_quality_improvements.py alongside the "
     "coordinate gate."},

    {"priority": 2, "type": "fix_pipeline", "added": TODAY, "target":
     "THE SOURCE-SIDE SCAN HAS A PUBLISHED-SIDE BLIND SPOT, AND IT WAS "
     "MEASURED, NOT THEORISED. audit_citation_coordinates.py reported 0 "
     "suspect while an independent end-to-end check of docs/*.html found a "
     "real defect the same minute: build_gka_landscape.py asserted 'Diabetes "
     "Care. 2002;25(10):1897-1902' for PMID 30949058 (actually Front Physiol "
     "2019;10:148), assembled across a structural boundary the source-side "
     "window did not model. Repaired, and the gate now cuts the right-hand "
     "window at block-level HTML boundaries - but the general lesson is the "
     "2026-08-24 lesson repeating: A GATE AIMED AT THE BUILDER IS NOT A GATE "
     "AIMED AT THE SITE. Promote the ad-hoc docs/ verifier written today into "
     "a permanent audit_published_coordinates.py so both surfaces are checked "
     "by construction. NOTE the ad-hoc verifier itself reports one false "
     "positive (PMID 38783768 in GKA_Landscape.html) precisely because it "
     "lacks the block-boundary rule - port that rule across when promoting it."},

    {"priority": 2, "type": "audit_gap", "added": TODAY, "target":
     "RE-READ GAP 15 (GKA PRICING) NOW THAT ITS CITATIONS ARE MARKED. "
     "build_gka_pricing.py now carries visible [UNSOURCED] markers on the "
     "SGLT2i launch/generic figures and the GKA generic precedent. Gap 15 is "
     "BRONZE and its dashboard is largely a pricing-trajectory argument; with "
     "the load-bearing citation stripped, re-assess whether the remaining "
     "sourced evidence still supports BRONZE or whether the gap should be "
     "restated as a modelling exercise with an explicit assumptions table."},

    {"priority": 3, "type": "fix_pipeline", "added": TODAY, "target":
     "REPLACE THE HARDCODED FABRICATION THRESHOLD WITH A RUNTIME CEILING. The "
     "scheduled-task file still says 'PMIDs above 42000000 are fabricated'. "
     "Measured live today: the ceiling is 42,649,123 and rising ~11k/day, and "
     "both repo PMIDs above the old threshold (42608595, 42631883) are real "
     "and correctly described. Every future run will otherwise waste sweep "
     "time on false fabrication reports, and worse, may purge real papers. "
     "Query the ceiling with esearch sort=most+recent at sweep time."},
]

remaining.extend(NEW_ITEMS)
remaining.sort(key=lambda i: (i.get("priority", 99), i.get("added", "")))
state["work_queue"] = remaining

# ---------------------------------------------------------------------------
# 4. RUN HISTORY.
# ---------------------------------------------------------------------------
state.setdefault("run_history", []).append({
    "date": TODAY,
    "day": "Thursday",
    "papers_checked": 26,
    "paths_validated": 0,
    "issues_found": 16,
    "changes_pushed": False,
    "summary": (
        "Thu 2026-08-27 - A CITATION CAN BE TRUE IN ITS PROSE AND FICTIONAL IN "
        "ITS NUMBERS, AND NOTHING HERE HAD EVER CHECKED THE NUMBERS. "
        "(1) THE FINDING. Clearing the P1 prose backlog surfaced 'Diabetes. "
        "2009 Jul;58(7):1416-28. PMID:19373249' in build_gka_lada.py, sitting "
        "under prose that correctly describes Matschinsky's 2009 glucokinase "
        "review. The PMID is Nat Rev Drug Discov 2009;8(5):399-416; Diabetes "
        "vol 58 issue 7 holds 34 articles and page 1416 is not one of them. "
        "Every gate passed it, and audit_prose_citation_titles passed it "
        "CORRECTLY - it scores the narrative, and the narrative was the true "
        "part. Built audit_citation_coordinates.py (SIXTH defect class): 11 "
        "suspect of 94, including three build_data_dictionary.py entries "
        "giving real papers invented journals (Gao et al. is Cell Metab "
        "2014;19(2):259-71, published as 'J Clin Invest 2014;124(10):4017'). "
        "All repaired; gate GREEN at 107/107 and WIRED into the pipeline, now "
        "54 steps. "
        "(2) THE GATE ALMOST LIED. Its first draft called three citations "
        "NONRESOLVING because 'Journal of Clinical Investigation'[ta] returns "
        "0 records with no error, while 'Nature Reviews Endocrinology'[ta] "
        "returns 3059 - all real journals. A negative probe is what licenses "
        "the word NONRESOLVING, so it now runs a positive control on the "
        "journal token first and downgrades to COORD_MISMATCH when it cannot "
        "see the journal at all. Three accusations withdrawn before publishing. "
        "(3) THE BIGGER FINDING, ESCALATED NOT ACTED ON. Measuring how often "
        "one PMID carries many claims produced audit_citation_load_bearing.py "
        "(SEVENTH class) and this: PMID 34763823, a 2021 review of INSULIN "
        "pricing, is attached to 91 distinct claims - GLP-1 pricing, SGLT2i "
        "launch pricing, GKA projections to 2042-2045, $2.6B development cost, "
        "CGM device cost, the Dec 2024 Hikma launch. Four temporally-impossible "
        "instances were stripped and marked [UNSOURCED]; the other ~87 are a "
        "dashboard-wide presentation decision and were left for a human, with "
        "the full inventory written to citation_load_bearing.json. 29710129 "
        "(81), 37909353 (47) and 32175717 (39) show the same shape. "
        "(4) WITHDRAWN RATHER THAN RE-ATTRIBUTED. The LADA C-peptide card "
        "asserted ~0.5-0.8 nmol/L at diagnosis sourced to 'UKPDS Group, Diabet "
        "Med 2004;21(1):31-7'. That PMID is Aronson on fasting glucose and CRP "
        "at pages 39-44, and the asserted page range resolves to nothing. No "
        "corpus source supports the figure, so the FIGURE was removed and the "
        "withdrawal is stated on the card; the qualitative claims were "
        "re-sourced to UKPDS 25 (PMID 9357409, verified live) and PMID "
        "32307525. Also removed: PMID 35551293, a Nat Med News & Views "
        "COMMENTARY that was being published as the DAWN phase 3 trial, with "
        "SEED and DAWN transposed on top of it (SEED is 35551294, DAWN is "
        "35551292). Sixteen citations repaired in total across six builders. "
        "(5) THE SOURCE-SIDE GATE HAS A PUBLISHED-SIDE BLIND SPOT. An "
        "independent end-to-end check of docs/*.html found a real defect while "
        "the source-side gate read 0 suspect - build_gka_landscape.py asserting "
        "'Diabetes Care 2002;25(10):1897' for a 2019 Front Physiol paper, "
        "assembled across a boundary the source scan did not model. Repaired, "
        "the gate now cuts at block-level HTML boundaries, and promoting the "
        "docs/ verifier into a permanent audit is queued at P2. This is the "
        "2026-08-24 lesson recurring: a gate aimed at the builder is not a gate "
        "aimed at the site. "
        "(6) SWEEP. Clean. The >42000000 fabrication rule re-confirmed stale: "
        "live ceiling 42,649,123, up ~23k in two days, and both repo PMIDs "
        "above the old threshold resolve and match their logged titles. "
        "Prose-citation backlog 14 -> 2, both gate artifacts (DCCT corporate "
        "authorship; a correct 'Khan et al. 2020'), so that gate stays "
        "standalone rather than sitting permanently red. All 54 pipeline steps "
        "[OK]."
    ),
})

state["last_run"] = TODAY
state["last_updated"] = TODAY + "T00:00:00"

backup = STATE + ".bak_" + TODAY
if not os.path.exists(backup):
    with open(backup, "w", encoding="utf-8") as fh:
        json.dump(json.load(open(STATE, encoding="utf-8")), fh, indent=1)

with open(STATE, "w", encoding="utf-8") as fh:
    json.dump(state, fh, indent=1, ensure_ascii=False)

print("state updated")
print("  work queue:      %d open" % len(state["work_queue"]))
print("  closed this run: %d" % len(state["closed_queue_items"]))
print("  run history:     %d entries" % len(state["run_history"]))
print("  doctrine notes:  %d" % len(state["doctrine_notes"]))
