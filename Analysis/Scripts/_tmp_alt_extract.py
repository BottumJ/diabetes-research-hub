# SUPERSEDED SCRATCH FILE - 2026-08-21
#
# This was a one-off A/B copy of extract_corpus_data.py used to measure whether
# section type TABLE should be scanned or skipped. Result of that measurement:
#
#   TABLE skipped  -> 292 extractions
#   TABLE scanned  -> 345 extractions (+58)
#
# All 58 extras were inspected individually. None were measurements:
#   46 x dose_response      bare dose labels ("5mg bid", "400 mg od"), including
#                           the bilingual pair "10 mg or" / "10 mg ou" from
#                           PMID 39412512 that prompted the investigation
#    7 x hba1c_change       table-legend abbreviation glossaries
#                           ("glycated hemoglobin, hdl high-density lipoprotein...")
#    2 x remission          supplementary-table cross-references
#    1 x survival_graft     "a.muciniphila reduced the levels of relevant" - not a rate
#    1 x odds_ratio, 1 x autoantibody   cohort-table fragments
#
# Conclusion: TABLE stays in SKIP_SECTION_TYPES. Scanning it adds no evidence
# and reintroduces the bilingual double-count.
#
# The OneDrive mount denies unlink, so this file cannot be deleted from the
# sandbox; it is tombstoned instead. Safe to delete from Windows.
raise SystemExit("superseded scratch file - see comment header")
