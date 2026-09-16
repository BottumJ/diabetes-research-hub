#!/usr/bin/env python3
"""
Master runner for all quality improvements.

Runs all improvement scripts in order:
  1. rebuild_clinical_trial_dashboard.py — Tufte-style trial dashboard
  2. rebuild_research_dashboard.py — Tufte-style research dashboard
  3. improve_gap_analysis.py — Interpreted gap classifications
  4. add_citations.py — Source citations for Research Findings Summary
  5. rebuild_website.py — Tufte-style GitHub Pages site

Usage:
  python run_quality_improvements.py           # Run all
  python run_quality_improvements.py --dashboard   # Trial dashboard only
  python run_quality_improvements.py --research    # Research dashboard only
  python run_quality_improvements.py --gaps        # Gap analysis only
  python run_quality_improvements.py --citations   # Citations only
  python run_quality_improvements.py --website     # Website only
"""

import subprocess
import sys
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = {
    'dashboard': ('rebuild_clinical_trial_dashboard.py', 'Rebuilding Clinical Trial Dashboard (Tufte style)'),
    'research': ('rebuild_research_dashboard.py', 'Rebuilding Research Dashboard (Tufte style)'),
    # Added 2026-09-05, and it MUST sit immediately before 'gaps', which renders
    # literature_gap_report.md from the JSON this stage writes.
    #
    # THE DEFECT THIS CLOSES IS WORSE THAN THE ONE IT LOOKS LIKE. On 2026-09-04
    # the stale publication monitor was found and this file was cleared in the
    # same breath - "literature_gap_report.md, which regenerates (2026-09-03) and
    # is therefore fine". Measured 2026-09-05, that clearance was wrong:
    #
    #     literature_gap_report.md   rendered 2026-09-04  <- fresh, and published
    #     literature_gap_data.json   written  2026-07-17  <- 50 days old
    #
    # improve_gap_analysis.py re-rendered the report from frozen JSON every day
    # and stamped each copy "**Generated:** <today>". pubmed_recent_summary.md at
    # least declared its true age; this one laundered 50-day-old data behind a
    # fresh date. Checking whether a report REGENERATES answers a different
    # question from whether its DATA is current, and only the second one matters
    # to a reader.
    #
    # Not wired in before because the sweep is 465 sequential PubMed queries at
    # NCBI's 3 req/s anonymous limit - ~6 min, past the 300s stage timeout. The
    # script was already checkpointed for exactly this; --budget 240 makes it a
    # bounded stage that resumes, so a full sweep completes across two runs and
    # each run exits 0. Set NCBI_API_KEY to finish in one.
    'gapdata': ('gap_analysis_daily.py',
                'Refreshing literature gap PubMed counts (resumable; bounded slice)',
                ('--budget', '240')),
    'gaps': ('improve_gap_analysis.py', 'Improving Literature Gap Analysis (interpretive classifications)'),
    'synthesis': ('build_gap_synthesis.py', 'Building Gap Synthesis Dashboard (scientific method framework)'),
    'equity': ('build_equity_map.py', 'Building Beta Cell Therapy Equity Analysis'),
    'deepdives': ('build_gap_deep_dives.py', 'Building Gap Deep Dives (all 15 gaps)'),
    'acronyms': ('build_acronym_db.py', 'Building Acronym & Abbreviation Database'),
    'dictionary': ('build_data_dictionary.py', 'Building Medical Data Dictionary (117 terms, cited)'),
    'lada': ('build_lada_model.py', 'Building LADA Natural History Model (Gap #1 SILVER)'),
    'islet': ('build_islet_outcomes.py', 'Building Islet Transplant Outcomes Analysis (Gap #3 GOLD)'),
    'drugrepurpose': ('build_drug_repurposing_islet.py', 'Building Drug Repurposing for Islet Transplant (Gap #4 SILVER)'),  # Promoted to SILVER: 11 independent papers from multiple research groups confirm this gap exists.
    'immunomod': ('build_immunomod_lada.py', 'Building Immunomodulatory Drugs for LADA (Gap #8 SILVER)'),
    'treg': ('build_treg_neuropathy.py', 'Building Treg in Diabetic Neuropathy (Gap #5 SILVER)'),  # Promoted to SILVER: 12 papers from independent groups confirm both sides of the gap.
    'cartaccess': ('build_cart_access.py', 'Building CAR-T Access Barriers Analysis (Gap #6 GOLD)'),
    'gka': ('build_gka_landscape.py', 'Building GKA Drug Repurposing Landscape (Gap #7 SILVER)'),
    'isletequity': ('build_islet_equity.py', 'Building Islet Transplant Registry Equity (Gap #11 GOLD)'),
    'genericdrug': ('build_generic_drug_catalog.py', 'Building Generic Drug x Diabetes Mechanism Catalog (Gap #12 SILVER)'),
    'gkalada': ('build_gka_lada.py', 'Building GKA in LADA Analysis (Gap #9 EXPLORATORY)'),
    'ladaprev': ('build_lada_prevalence.py', 'Building LADA Prevalence by Healthcare Setting (Gap #10 SILVER)'),
    'nutribeta': ('build_nutrition_beta.py', 'Building Personalized Nutrition for Beta Cells (Gap #13 SILVER)'),
    'nutrilada': ('build_nutrition_lada.py', 'Building Personalized Nutrition for LADA (Gap #14 BRONZE)'),
    'gkapricing': ('build_gka_pricing.py', 'Building GKA Pricing Trajectory Model (Gap #15 BRONZE)'),
    'healthequity': ('build_health_equity.py', 'Building Health Equity Dashboard (Gap #2 GOLD)'),
    'methodology': ('build_methodology.py', 'Building Methodology & Validation Framework'),
    'pmidverify': ('verify_pmids.py', 'Verifying PMIDs against PubMed API'),
    'pmidtracker': ('track_unfound_pmids.py', 'Tracking unfound PMIDs (Verify-* markers)'),
    'citations': ('add_citations.py', 'Adding source citations to Research Findings Summary'),
    'ingest': ('ingest_papers.py', 'Ingesting paper abstracts and full text from PubMed/PMC'),
    # Must run AFTER ingest and BEFORE validate. verify_pmids.py only scans .py
    # source literals, so any paper that entered via extraction output or a
    # PubMed sweep never reached index.json and the citation gate was blind to
    # it. 39 such orphans were found on 2026-08-18 (13% of fetched abstracts),
    # including the sole source for NLRP3_inflammasome -> nephropathy.
    'orphans': ('reconcile_paper_index.py', 'Folding un-indexed corpus papers into the audit gate'),
    'validate': ('validate_citations.py', 'Validating citations and building evidence network'),
    # Gate: consumes validate_citations.py output. Added 2026-08-16 after 7 real
    # miscitations were found sitting unactioned in citation_validation.json.
    # Must run immediately after 'validate'.
    'mismatchgate': ('check_citation_mismatches.py', 'Gating on unresolved citation MISMATCHes'),
    # Added 2026-08-20. check_citation_mismatches.py consumes validate_citations.py,
    # which scans .py SOURCE LITERALS - it never saw the external_pmids stored on
    # research paths in agent_state.json. Screening those against PubMed titles found
    # 17 real PMIDs attached to unrelated papers, including PMID 37889505 ("probiotic
    # breads") cited as the PROTECT teplizumab trial and recorded as verified evidence
    # in the 2026-08-19 run history. Presence of a PMID is not correctness of a PMID.
    'pathcitegate': ('audit_path_citations.py',
                     'Gating on off-topic / unresolvable external citations on research paths'),
    # Added 2026-08-22. extract_corpus_data.py was NOT in this pipeline. It was
    # run by hand, while build_corpus_analysis.py, build_extracted_evidence.py,
    # build_research_paths.py and rebuild_website.py all read its output - so
    # every corpus figure on the published site could be arbitrarily stale
    # while this runner reported 47/47 green. Structurally identical to the
    # docs/Dashboards freeze found on 2026-08-16 (33 stale, 2 missing, runner
    # all-green), and to the reason the 2026-08-21 extractor fix did not reach
    # PMID 32862232 until it was re-run manually on 2026-08-22.
    # Must precede every consumer of extracted_corpus_data.json.
    'extractcorpus': ('extract_corpus_data.py',
                      'Extracting quantitative data points from the full-text corpus'),
    # Added 2026-08-22. Third distinct citation-defect class in four days, and
    # each slipped the gate built for the previous one:
    #   PMID >= 42M sweep         -> catches FABRICATION only
    #   audit_path_citations.py   -> catches wrong SUBJECT only
    #   this                      -> catches wrong PAPER TYPE
    # A trial publishes a design paper, a baseline-characteristics paper and an
    # outcomes paper. All three resolve, all three are on topic, and only one
    # reports a result. `dapagliflozin -> nephropathy` cited the DAPA-CKD
    # BASELINE paper (PMID 32862232) as proof of renoprotection and every prior
    # gate passed it. The corpus arm of the same script found the larger case:
    # PMID 39613428 is a trial PROTOCOL supplying 15 data points to the paths
    # that published at ranks #7 and #8.
    'designcitegate': ('audit_baseline_citations.py',
                       'Gating on design/baseline papers cited as outcome evidence'),
    # Added 2026-08-23. FOURTH distinct citation-defect class, and again it slipped
    # every gate built for the previous three - this time not by being a different
    # KIND of wrong paper, but by living in a different FIELD and a different
    # IDENTIFIER NAMESPACE.
    #
    # audit_path_citations.py reads `external_pmids` and nothing else. Path records
    # carry citations under at least nine field names and in three namespaces
    # (PMID, PMC id, DOI). Consequence measured 2026-08-23: NINE of the PMIDs the
    # 2026-08-20 run reported as PURGED were still asserted as fact in narrative
    # fields, including `teplizumab -> autoimmune` still reading
    #     "PROTECT phase 3 (Ramos et al. NEJM 2023, PMID 37889505 ...)"
    # where 37889505 is the probiotic-breads paper. The purge cleaned the list and
    # left the prose making the identical false claim. Repaired by
    # repair_prose_citations_20260823.py; this gate is what stops it recurring.
    #
    # It also resolves PMC ids and DOIs, which no gate had ever checked: two
    # VALIDATED HIGH/HIGH paths (`NF_kB -> inflammation`,
    # `oxidative_stress -> cardiovascular`) rest entirely on them.
    'identifiergate': ('audit_citation_identifiers.py',
                       'Gating on citations in every field and identifier namespace'),
    # Added 2026-08-26. The one citation defect where EVERY gate above is silent
    # by construction. A retracted paper resolves, is on-topic, and carries a
    # correct title, so validate_citations, audit_path_citations,
    # audit_builder_title_agreement and audit_prose_citation_titles all pass it.
    # Found on its first run: PMID 38918878 (IL-1 inhibitors and colchicine in
    # T2D, Diabetol Metab Syndr 2024), pubtype "Retracted Publication", cited in
    # 18 files, published on three dashboards, and supplying two colchicine
    # dose_response extractions to Gap 4 and Gap 7. Nothing had ever asked
    # PubMed whether a paper had been withdrawn.
    'retractiongate': ('audit_retractions.py',
                       'Gating on retracted papers cited as evidence'),
    # Added 2026-08-27. The SIXTH defect class, and the second where every gate
    # above is silent by construction rather than merely aimed elsewhere.
    #
    # Every control this repo owns asks a question about the PAPER: does the
    # PMID resolve, is it on-topic, is the title right, was it retracted. This
    # one asks whether the BIBLIOGRAPHIC COORDINATE is real. Found on its first
    # run in build_gka_lada.py (CITATION-EXAMPLE: the coordinate quoted below
    # is the defect being described, not a live citation - the marker is what
    # exempts it from the gate, and every exemption must be written by name):
    #     prose:      "Matschinsky FM et al. (2009). Comprehensive review of
    #                  glucokinase as beta cell glucose sensor."     <- TRUE
    #     coordinate: "Diabetes. 2009 Jul;58(7):1416-28"             <- FICTION
    # PMID 19373249 is Nat Rev Drug Discov 2009;8(5):399-416. Diabetes vol 58
    # issue 7 exists and holds 34 articles; page 1416 is not among them.
    # audit_prose_citation_titles PASSES this, correctly - it scores the prose,
    # and the prose is the part that is true.
    #
    # Eight more were found the same way, including three in
    # build_data_dictionary.py where a real paper was given an invented journal
    # (Gao et al. is Cell Metab 2014;19(2):259-71, published as "Journal of
    # Clinical Investigation 2014;124(10):4017-4024") and one in
    # build_gka_landscape.py. All repaired 2026-08-27; the gate is GREEN at
    # 102/102 coordinates, which is why it is wired here rather than left
    # standalone like the prose gate.
    'coordinategate': ('audit_citation_coordinates.py',
                       'Gating on invented journal/volume/page coordinates'),
    # Added 2026-08-26. Replaces the free-text adjudication step of the
    # credibility sweep with a rule that can be checked: an absolute verb
    # (eliminates / abolishes / prevents / cures / guarantees / zero) attached
    # to a CLINICAL ENDPOINT must cite a PMID whose abstract contains a
    # same-family absolute. The grep was never the problem - both
    # overstatements repaired on 2026-08-25 had been read by earlier sweeps and
    # cleared as "factual/contextual", and "eliminates hypoglycemia risk" sat
    # live for four months after being looked at twice. Judgement drifts; a
    # fetched abstract does not.
    'absoluteclaims': ('audit_absolute_claims.py',
                       'Gating on absolute clinical claims not echoed by their '
                       'cited abstract'),
    # Added 2026-08-22. Measures the artifact rate of every extractor and fails
    # if an unbounded `.*?` wildcard gap reappears between a marker token and
    # its capture group. That construction is the single root cause of the
    # 2026-08-21 inflammatory_markers defect (57% artifact) and of the five
    # further extractors measured on 2026-08-22 (remission 71%, survival_graft
    # 100%, c_peptide 100%, autoantibody 60%, hba1c_change 50%). Regression
    # protection: the pattern style, not the symptom.
    'wildcardaudit': ('audit_extractor_wildcards.py',
                      'Auditing extractors for unbounded-wildcard artifacts'),
    # Added 2026-08-28. Closes the intake-door class instead of naming doors.
    # Every previous seal here was applied to a specific script after that
    # script leaked; this one fails any LIVE script that reads the abstracts
    # dir, the fulltext dir or the library index without importing
    # corpus_membership, whether or not it has leaked yet. Its first run
    # found three more unguarded readers (build_corpus_analysis.py,
    # rebuild_website.py, validate_citations.py) that no leak had surfaced.
    'membershipgate': ('audit_unguarded_pmid_readers.py',
                       'Gating on PMID readers that bypass corpus_membership'),
    # Added 2026-08-28. Grades what KIND of study each live path rests on,
    # from PubMed publication type rather than from this repo's own regexes.
    # First run: the four highest-ranked paths by data-point count all rest
    # on no primary data - ranks 1 and 2 on a meta-analysis whose numbers
    # cannot be attributed, ranks 4 and 5 on a clinical trial PROTOCOL. A
    # count answers "how much" and never "of what". Reports, never fails:
    # labelling honest weak evidence is the goal, deleting it is not.
    'pathdesign': ('audit_path_evidence_design.py',
                   'Grading research-path evidence by study design (PubMed pubtype)'),
    # Added 2026-08-29. pathdesign trusts PubMed's publication-type field
    # because a builder cannot invent it - true, but PubMed can OMIT it, and
    # absence reads as "unknown design". Found running BOTH ways in one
    # 16-paper batch: PMID 36643381 is an untagged protocol supplying 7 live
    # extractions, PMID 36826844 is an untagged JAMA RCT (CLVer, n=88)
    # supplying none. 134 of 359 corpus papers carry no design pubtype at all,
    # rising to 66% for 2026 papers. Must run BEFORE pathdesign consumers so
    # the caveat is current when the dashboards render it.
    'pubtypegap': ('audit_pubtype_title_disagreement.py',
                   'Checking PubMed pubtype against the verified title (design-blind coverage)'),
    # Added 2026-08-30. Gap tiers (GOLD/SILVER/BRONZE) were assigned by
    # INDEPENDENT-SOURCE COUNT - the same metric shown on 2026-08-29 to rank a
    # trial protocol above measured evidence on 62.3% of path pairs. Nothing
    # about that failure was specific to paths. Reads the pubtype cache
    # offline, so it cannot be the stage that stalls the pipeline. Reports
    # and never re-tiers: a gap tier is a scientific judgement.
    'gapdesign': ('audit_gap_evidence_design.py',
                  'Grading the 15 research gaps by evidence design (offline, from pubtype cache)'),
    # Added 2026-09-03. The gate above grades gap N's EVIDENCE. Nothing checked
    # that gap N meant the same thing in the agent's memory as on the site. On
    # 2026-09-02 a run found gaps["15"].audit_history had audited SGLT2i x
    # personalized nutrition since April while canonical Gap #15 is GKA
    # Pricing, and treated it as one orphaned trail. Sweeping all fifteen finds
    # FIVE: #4, #5, #7, #11 and #12 are each filed under a number that names a
    # different question, consistently since April - two numbering schemes
    # built independently and never reconciled. Also cross-checks the tier in
    # agent_state, gap_evidence.json and docs/index.html, which disagree on
    # three gaps. Offline; reports and never re-homes.
    'gapnumbering': ('audit_gap_numbering.py',
                     'Checking gap numbering + tier agreement across memory, evidence store and site'),
    # Added 2026-08-30. THE EIGHTH DEFECT CLASS: every identifier correct and
    # the claim still unsupported. PMID 29710129 sourced 47 drug-screen cost
    # claims while being a 14-word JAMA Oncology CAR-T letter; PMID, title,
    # journal, year and first author were all correct, so all seven existing
    # gates passed it. Two independent weak signals, deliberately unmerged:
    # IDF-weighted claim-to-abstract overlap (validated at 4.92x lift over
    # random pairings) and claims-per-100-source-words, which needs no
    # semantics and is what actually catches the founding case. Reports the
    # worst N; never gates, because a gate on topical overlap would fail
    # honest citations and teach the prose to please a scorer.
    'semanticsupport': ('audit_citation_semantic_support.py',
                        'Scoring citation semantic support and claim density (reports worst N)'),
    # Added 2026-08-31. Every citation gate above scans .py and only .py
    # (verify_pmids.py:44, audit_prose_citation_titles.py:349), so the markdown
    # documents were never audited by anything. On the day this was wired, a
    # first pass over them found misattributed PMIDs in RESEARCH_DOCTRINE.md -
    # the file that DEFINES the citation standard, whose "PMID-Verified
    # (Strongest)" exemplar cited a perovskite solar-cell paper and whose
    # correct-format exemplar cited a RETRACTED ginsenoside study - and a
    # GOLD-rated claim in Research_Findings_Summary.md resting on a paper about
    # something else entirely.
    'mdcitations': ('audit_markdown_citations.py',
                    'Auditing markdown citations against PubMed (doctrine + summaries)'),
    # Pins the gate above. It reported 0 findings on its first clean run, which
    # proves nothing on its own because the same run had just repaired every
    # defect it was built for. This replays the pre-repair text.
    'mdcitegate': ('test_markdown_citation_gate.py',
                   'Regression fixture: markdown gate sensitivity AND specificity'),
    # Every gate above this line checks a PMID. None of them had ever checked an
    # NCT, and NCT numbers carry claims on the published summary in exactly the
    # same way. First run, 2026-09-01: 21 of 32 hand-authored trial citations
    # disagree with ClinicalTrials.gov, 9 of them naming a study in an unrelated
    # field - the baricitinib Phase 3 entry cited a radioligand oncology trial,
    # the teplizumab PETITE entry cited a chlorhexidine obstetrics trial. The
    # repo had already found one wrong NCT by hand in March 2026
    # (build_trial_equity_mapper.py: "NCT03812588 (wrong study)") and never
    # generalised it into a gate. This is that gate.
    'nctgate': ('audit_nct_identifiers.py',
                'Auditing trial-registry identifiers against ClinicalTrials.gov'),
    # Replaces the scheduled-task file's "PMIDs above 42000000 are fabricated"
    # rule, which PubMed passed months ago (live ceiling 42,669,647 measured
    # 2026-08-31; 30+ real corpus PMIDs sit above the old threshold).
    'credibility': ('audit_impossible_pmids.py',
                    'Credibility sweep: runtime PMID ceiling + preclinical overclaim'),
    'evidence': ('extract_evidence.py', 'Extracting evidence from papers for 15 research gaps'),
    'paperlibrary': ('build_paper_library.py', 'Building Paper Library Dashboard'),
    'drugscreen': ('build_drug_repurposing_screen.py', 'Building Generic Drug Repurposing Screen (34 drugs, pressure-tested)'),
    'ladadiagnostic': ('build_lada_diagnostic_model.py', 'Building LADA Diagnostic Cost-Effectiveness Model'),
    'trialequity': ('build_trial_equity_mapper.py', 'Building Clinical Trial Site Equity Mapper'),
    'corpus': ('build_corpus_analysis.py', 'Building Corpus Analysis Dashboard (co-occurrence network; counts printed by the builder)'),
    'extracted': ('build_extracted_evidence.py', 'Building Extracted Evidence Dashboard (counts printed by the builder)'),
    'researchpaths': ('build_research_paths.py', 'Building Research Paths Dashboard (post-artifact-filter counts printed by the builder)'),
    # Resolves state.paths / state.validated_paths / validated_research_paths.json
    # into one canonical store. Reading any single store directly is what emitted
    # six false "NEVER-VALIDATED" work items on 2026-08-16.
    'pathstore': ('path_store.py', 'Resolving the canonical research-path store (merge rule: recency, conservative tie-break)'),
    # Added 2026-08-29, and it MUST sit between pathstore and statistics: it
    # reads statistical_analysis.json plus the design grades and writes the
    # discordance figures that build_statistical_analysis.py prints above its
    # Bayesian ranking. Run it after that builder and the page publishes last
    # run's numbers beside this run's ranking.
    # Added 2026-09-06, immediately after pathstore because it audits the store
    # pathstore resolves FROM.
    #
    # A path's verdict lives under `rating` (37 records), `status` (51) or both
    # (32). path_store.status_of() reads all three names defensively, so every
    # consumer routed through it is correct today - but the correctness is
    # conventional, not structural, and three stored records contradicted
    # themselves. The worst was validated_paths['GLP1_RA -> neuroprotection'],
    # carrying status PARTIALLY_VALIDATED beside rating VALIDATED: the
    # 2026-08-20 downgrade - the one that caught ELAD (PMID 41326666) being
    # cited as validation when it MISSED its primary endpoint, P = 0.14 - wrote
    # `status` and left `rating` at the withdrawn verdict. Every PMID in that
    # record is real and correctly transcribed, so no citation gate would ever
    # object; one direct rec.get('rating') republishes a retraction.
    #
    # path_store.dedupe_state() does canonicalise both keys, but only inside
    # its duplicate-spelling loop (`if len(raw_keys) < 2: continue`), so a
    # single-spelling record with two disagreeing keys is never reached.
    'verdictkeys': ('audit_verdict_key_agreement.py',
                    'Asserting no stored path record asserts two verdicts about itself'),
    'posterioragree': ('audit_posterior_design_agreement.py',
                       'Measuring posterior-vs-study-design discordance on the Bayesian ranking'),
    'statistics': ('build_statistical_analysis.py', 'Building Statistical Analysis Dashboard (meta-analysis, Bayesian synthesis, Monte Carlo)'),
    'repurposev2': ('build_repurposing_dashboard_v2.py', 'Building Islet Drug Repurposing Pipeline v2'),
    'website': ('rebuild_website.py', 'Rebuilding GitHub Pages site (Tufte style)'),
    'postprocess': ('postprocess_dashboards.py', 'Post-processing dashboards (nav, PMID links, ARIA)'),
    # Publish step. MUST run last: postprocess_dashboards.py rewrites
    # Dashboards/*.html, so syncing before it would publish pre-processed files.
    # Added 2026-08-16 after docs/Dashboards/ was found frozen since 2026-03-29
    # (33 stale, 2 missing, 0 in sync) while this runner reported all-green,
    # because rebuild_website.py only ever wrote docs/index.html.
    'syncdocs': ('sync_docs_dashboards.py', 'Publishing rebuilt dashboards to docs/ (GitHub Pages)'),
    # Added 2026-09-05, and it must precede syncreports so the file that gets
    # published is this run's, not the last one that happened to be generated
    # by hand.
    #
    # WHY IT WAS NEVER HERE, MEASURED RATHER THAN GUESSED. The 2026-09-04 run
    # asked why the daily pipeline does not regenerate pubmed_recent_summary.md
    # and left the question open. The answer is that there is no reason: timed
    # 2026-09-05, a full sweep of 16 domain queries and 8 therapy queries against
    # live PubMed E-utilities completes in 35.6s, against this runner's 300s
    # per-stage timeout. It was not excluded for cost, for flakiness or for
    # network policy. It was simply never added, and nothing existed that could
    # notice - which is the whole finding, and is why 'reportfreshness' below
    # exists rather than this line alone.
    #
    # The hub card called this a "Rolling 30-day PubMed snapshot" with status
    # "Available" while the file underneath declared Generated: 2026-07-17, a
    # 49-day-old rolling window. 2026-09-04 made the age VISIBLE by adding a
    # provenance banner in sync_docs_reports.py. Disclosure is not repair; this
    # is the repair.
    'pubmedmonitor': ('baseline_pubmed_alerts.py',
                      'Refreshing the rolling PubMed publication monitor (live E-utilities sweep)'),
    # Added 2026-09-04. syncdocs copies *.html only, so the two MARKDOWN reports
    # the hub advertises as "Available" had never been published at all - their
    # hrefs resolved to docs/Analysis/Results/..., which has never existed.
    'syncreports': ('sync_docs_reports.py',
                    'Publishing the markdown reports the hub advertises to docs/Reports/'),
    # POST-PUBLISH ASSERTION, added 2026-09-05. Generalises the stage above
    # instead of trusting it.
    #
    # Wiring one generator in fixes one file. The defect class is that a report
    # can DECLARE its own freshness ("Lookback period: 30 days") and be older
    # than that declaration, with every gate in this pipeline silent because
    # every gate here asks whether a CITATION is true and none asks whether a
    # PAGE is current. pubmed_recent_summary.md was 49 days into a 30-day
    # window and 47 green stages said nothing.
    #
    # The rule is self-referential on purpose, so it needs no maintained list:
    # a published report's declared age must not exceed the window it claims to
    # cover. Scope is derived from docs/index.html at run time, the same rule
    # sync_docs_reports.py uses, so a report added to the hub is gated the day
    # it is added.
    'reportfreshness': ('audit_report_freshness.py',
                        'Asserting published reports are no older than the window they advertise'),
    # Pins the gate above, on the same reasoning as mdcitegate. It passed 2/2 on
    # its first run, which is equally consistent with "the repo is clean" and
    # "the gate is a no-op", because the run that first executed it had already
    # repaired both defects it was built for. This replays the pre-repair text:
    # the 49-day rolling window AND the fresh-stamp-over-50-day-old-data case
    # that 2026-09-04 inspected and cleared. Offline; touches no repo file.
    'freshnessgate': ('test_report_freshness_gate.py',
                      'Regression fixture: freshness gate sensitivity AND specificity'),
    # POST-PUBLISH ASSERTION. Must run dead last - it reads docs/, which only
    # exists in its final form after syncdocs. Added 2026-08-20 after an
    # adjudicated EXTRACTION_ARTIFACT (insulin_glargine -> T2D) reached the
    # published page TWICE on 2026-08-19: once because the dashboard consulted
    # text patterns instead of the adjudication, and once because the two path
    # stores use different key spellings. Both holes were patched in
    # build_research_paths.py, but a patch is not a guarantee - this gate is the
    # standing proof that the patches still hold.
    'suppressiongate': ('regression_suppression_gate.py',
                        'Asserting no adjudicated-artifact path is live on the published site'),
    # POST-PUBLISH ASSERTION, and it must stay last for the same reason
    # suppressiongate does: it reads docs/, which is only final after the sync
    # stages. Added 2026-09-04, when an end-to-end read of the published site
    # found 41 dead links against 1359 live ones - including a dead "<- Hub"
    # back-link on all 34 dashboards, produced BY the publish step, because the
    # step verified byte equality with the source and byte equality is exactly
    # what makes a depth-relative link wrong at a different depth.
    'linkgate': ('audit_published_links.py',
                 'Asserting every link the published site advertises resolves under docs/'),
    # POST-BUILD ASSERTION, added 2026-09-06. Must run after the builders and
    # after syncdocs, because it reads rendered output, not source.
    #
    # An absence claim - "zero publications", "has never been tested", "no
    # study has measured" - is the only claim class in this repo produced by
    # finding NOTHING, so it has no citation for the fourteen citation gates to
    # check. They are silent on precisely the claims that are easiest to get
    # wrong, because an empty result set is a fact about a QUERY and gets
    # written down as a fact about the world.
    #
    # Generalises the 2026-09-05 Gap #3 finding (2020-bounded sweeps could
    # never see the pre-2020 papers that falsified an "unmeasured" claim).
    # Re-running the repo's absence claims all-time on 2026-09-06 found the
    # same defect twice more: "Treg-based therapy has never been tested for
    # diabetic neuropathy" is falsified by PMID 42698953, published two days
    # before the check, and "generic drugs have never been systematically
    # evaluated for repurposing" is weakened by PMID 37399599. A third,
    # "computational drug screening has not been applied [to islet
    # transplant]", turned out TRUE beside a pair_count of 0 that is FALSE -
    # right conclusion, wrong evidence, indistinguishable from the outside.
    #
    # The gate cannot check truth offline. It checks that each claim declares
    # the scope of the search behind it, which is the property all four cases
    # were missing and the one that lets a reader know what would falsify it.
    'absencescope': ('audit_absence_claim_scope.py',
                     'Asserting every published absence claim declares the search that produced it'),
    # Added 2026-09-07. absencescope above asks whether a claim DECLARES its
    # search. This asks the prior question: does the gap's stored evidence
    # mention the gap's own subject at all?
    #
    # Canonical Gap #11 was GOLD on two papers - a 2008 CITR update and a
    # graft-function cohort - neither of which contains the words equity, race,
    # ethnicity or access anywhere. Every gap here is an intersection (X domain
    # x Y lens), and #11's evidence covered X fully and Y not once. Nothing
    # failed because nothing had asked. First run, 2026-09-07: 9 of 15 gaps
    # fail, so #11 was the tip, not the case.
    #
    # KNOWN SOFT SPOT, stated so no one over-reads a failure: the gate detects
    # the presence of a WORD, not of an ANALYSIS. Gaps #4 and #7 fail on
    # "repurposing" while citing anakinra, etanercept, rapamycin and
    # dorzagliatin - drugs that ARE repurposed but whose papers never use the
    # term. Those are arguably labelling gaps, not evidence gaps, and need a
    # human call. Gaps #1, #11 and #13 are the hard failures: their evidence is
    # about a different subject entirely.
    'gapsubject': ('audit_gap_subject_coverage.py',
                   "Asserting each gap's stored evidence mentions both axes of the gap's own question"),
    # DEAD LAST, added 2026-09-06, and it is the gate every stage above needs
    # in order to mean what it says.
    #
    # syncdocs, syncreports, reportfreshness, suppressiongate and linkgate all
    # validate docs/ IN THE WORKING TREE. docs/ is the Pages root, so that is
    # the directory this agent BUILDS; the directory a reader LOADS is
    # origin/main:docs/. Measured 2026-09-06: main is 101 commits ahead,
    # origin/main tip is 2026-04-20 (138 days), and 38 of the 39 files under
    # docs/ are stale or absent for a reader - 4 return 404, 34 are old copies,
    # 1 is right. On 2026-09-05 this runner reported "1400/1400 published links
    # resolve" and "both reports fresh at 0 days" with 71 stages green. Every
    # one of those statements is true about the working tree and false about
    # the site.
    #
    # The push failure was recorded in ELEVEN run summaries from 2026-05-24 on
    # and changed nothing, because noticing lived in prose and prose is not
    # wired to anything. This line is the wiring: the runner's SUMMARY block
    # cannot print all-OK while the site is behind, so the condition has to be
    # cleared rather than re-observed.
    #
    # It will be RED until a human pushes. That is intended. It is also why the
    # fixture below is not optional.
    'publishgate': ('audit_publish_reachability.py',
                    'Asserting the published SITE matches what this pipeline audits (reads origin)'),
    # Pins the gate above, same reasoning as mdcitegate and freshnessgate, with
    # one addition specific to this one: publishgate is red on arrival and will
    # stay red, and an alarm never observed to switch off is indistinguishable
    # from an alarm that is stuck - which is precisely how eleven prior notices
    # decayed into background noise. This fixture builds throwaway repos and
    # proves the gate PASSES when a site is level and clean (specificity), as
    # well as failing on behind / diverged / dirty / unreachable (sensitivity).
    # It earned its place on its first execution: it caught `cwd=ROOT` bound as
    # a default argument in the gate, which made all five cases silently audit
    # THIS repository instead of the fixture clone. Offline; touches no repo
    # file.
    'publishgatetest': ('test_publish_reachability_gate.py',
                        'Regression fixture: publish gate sensitivity AND specificity'),
    # Added 2026-09-16, and it is a REPORTING stage, not a failing gate. Read
    # the PAIRING RULE comment in the script before changing anything here.
    #
    # WHY REPORT-ONLY. Measured as the 2026-09-14 queue item specified it - a
    # symmetric ~80-char window - this gate produced 103 mismatches that were
    # almost entirely FALSE, because a symmetric window reaches backwards into
    # the previous citation in a semicolon-separated run and tests every
    # surname against its predecessor's PMID. Six false-positive classes have
    # now been found and fixed (reverse straddle, PubMed initials, slash-joined
    # runs, entity/diacritic folding, comma-separated reference lists, and
    # malformed library records). The survivors it still prints include
    # archived run reports and NON_FIRST_AUTHOR cases that are not defects, so
    # failing the build on them would train the pipeline's red to be ignored.
    #
    # WHY THE FLAGS. --html scans generated .html for <a> elements whose PMID
    # sits in an attribute (onclick/data-/href) with the surname in the anchor
    # text. That class is invisible to prose pairing and it is where the
    # Shapiro/10919952 defect survived a full sweep - it is also, per
    # occurrence, the citation a reader is most likely to click.
    # --resolve-unknown looks up PMIDs absent from the local paper library
    # against NCBI esummary (cached to .surname_resolve_cache.json). That
    # bucket was not neutral: a PMID is missing from the library exactly when
    # it was added recently and by hand, which is also when it is most likely
    # to be wrong. PMID 37359825 hid there for two days as "Voglova et al."
    # (it is Wisel et al.) after a verification pass confirmed its CONTENTS and
    # inherited the surname. Network failure inside the resolver is caught and
    # leaves the PMID in the UNKNOWN bucket, so this stage cannot fail on a
    # blip; it exits 0 in --measure mode regardless.
    'surnames': ('audit_prose_author_surnames.py',
                 'Auditing author-surname attributions (REPORT ONLY; prose + '
                 'HTML anchors + NCBI resolution of unknowns)',
                 ('--measure', '--html', '--resolve-unknown')),
}

def run_script(name, desc, script_args=()):
    """Run one stage.

    script_args added 2026-09-05 for gap_analysis_daily.py, the first stage that
    cannot finish inside the 300s timeout and does not need to. It checkpoints
    every 15 queries, so --budget lets it do a bounded slice, exit 0, and resume
    on the next run. Every other stage passes no args and behaves exactly as
    before.
    """
    path = os.path.join(SCRIPT_DIR, name)
    print(f"\n{'='*60}")
    print(f"  {desc}")
    print(f"{'='*60}")
    start = time.time()

    try:
        result = subprocess.run(
            [sys.executable, path, *script_args],
            capture_output=True, text=True, timeout=300
        )
        elapsed = time.time() - start

        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                print(f"  {line}")

        if result.returncode != 0:
            print(f"  ERROR (exit code {result.returncode})")
            if result.stderr:
                for line in result.stderr.strip().split('\n')[:10]:
                    print(f"  ! {line}")
            return False

        print(f"  Completed in {elapsed:.1f}s")
        return True

    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT after 300s")
        return False
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        return False


def commit_changes(message):
    """Commit via git_commit_safe.py rather than plain `git commit`.

    The mount denies unlink() inside .git/ at every file age, so git's standard
    create-lock/rename-over-then-delete cycle leaves a fresh lock on EVERY
    invocation and `git commit` only succeeds intermittently (~150 lock corpses
    had accumulated since April, one per daily run). git_commit_safe.py builds
    the commit with plumbing against an index held off the mount, which is
    deterministic. Push still requires host credentials -- see that script.
    """
    safe = os.path.join(SCRIPT_DIR, 'git_commit_safe.py')
    if not os.path.exists(safe):
        print('  ! git_commit_safe.py not found; skipping commit')
        return False
    print(f"\n{'='*60}")
    print('  Committing via git_commit_safe.py (deterministic plumbing path)')
    print(f"{'='*60}")
    try:
        # Must run from the repo root: git_commit_safe.py resolves the repository
        # from the current working directory, and a bare subprocess inherits the
        # caller's cwd (often Analysis/Scripts) -> "not a git repository".
        repo_root = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
        result = subprocess.run([sys.executable, safe, '-m', message],
                                capture_output=True, text=True, timeout=180,
                                cwd=repo_root)
        for line in (result.stdout or '').strip().split('\n'):
            if line:
                print(f'  {line}')
        if result.returncode != 0:
            for line in (result.stderr or '').strip().split('\n')[:10]:
                print(f'  ! {line}')
            print('  COMMIT FAILED')
            return False
        print('  [OK] committed')
        return True
    except Exception as e:
        print(f'  EXCEPTION during commit: {e}')
        return False


def main():
    args = sys.argv[1:]

    commit_msg = None
    if '--commit' in args:
        i = args.index('--commit')
        if i + 1 < len(args) and not args[i + 1].startswith('-'):
            commit_msg = args[i + 1]
            del args[i:i + 2]
        else:
            commit_msg = 'Automated pipeline rebuild'
            del args[i]

    if not args:
        targets = list(SCRIPTS.keys())
    else:
        targets = [a.lstrip('-') for a in args if a.lstrip('-') in SCRIPTS]
        if not targets:
            print("Usage: python run_quality_improvements.py [--dashboard] [--research] [--gaps] [--citations] [--website]")
            print("  No flags = run all improvements")
            sys.exit(1)

    print("=" * 60)
    print("  DIABETES RESEARCH HUB — QUALITY IMPROVEMENTS")
    print("=" * 60)
    print(f"  Running {len(targets)} improvement(s): {', '.join(targets)}")

    results = {}
    for key in targets:
        entry = SCRIPTS[key]
        name, desc = entry[0], entry[1]
        script_args = entry[2] if len(entry) > 2 else ()
        results[key] = run_script(name, desc, script_args)

    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    for key, success in results.items():
        status = "OK" if success else "FAILED"
        print(f"  [{status}] {SCRIPTS[key][1]}")

    failed = sum(1 for v in results.values() if not v)
    if failed:
        print(f"\n  {failed} script(s) failed. Check output above.")
        sys.exit(1)
    else:
        print(f"\n  All {len(results)} improvements completed successfully.")
        # Only commit a green build. A failed build must never be committed.
        if commit_msg:
            commit_changes(commit_msg)
        print(f"\n  NEXT STEPS:")
        print(f"  1. Review the updated files in your project folder")
        print(f"  2. Verify placeholder citations marked 'verify' in Research_Findings_Summary.md")
        print(f"  3. Open the dashboards in a browser to confirm visual quality")
        if commit_msg:
            print(f"  4. Push from the Windows host (sandbox has no credential):")
            print(f"     cd C:\\Users\\justi\\OneDrive\\Diabetes_Research ; git push origin main")
        else:
            print(f"  4. To commit automatically next time, pass --commit \"message\"")


if __name__ == '__main__':
    main()
