#!/usr/bin/env python3
"""
Corpus Data Extraction Pipeline
Extracts structured quantitative data from 91 full-text papers:
- C-peptide measurements (beta cell function)
- Graft/patient survival rates (islet transplant outcomes)
- HbA1c changes (glycemic efficacy)
- Drug dose-response data (repurposing screen validation)
- Cost/QALY data (health economics)
- Hazard ratios and odds ratios (risk quantification)
- Remission rates (treatment efficacy)

Outputs: extracted_corpus_data.json for use by dashboard build scripts.
"""
import json
import os
import re
from collections import defaultdict
from pathlib import Path

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
results_dir = os.path.join(base_dir, 'Analysis', 'Results')
library_dir = os.path.join(results_dir, 'paper_library')

# Load index
with open(os.path.join(library_dir, 'index.json'), encoding='utf-8') as f:
    index = json.load(f)
papers_meta = index['papers']

# Load agent state to identify FLAGGED off-topic papers that must be excluded
# from the published evidence pipeline (e.g., CRC, smoking-cessation, melanoma
# papers that survived the original PubMed pull but are not diabetes-relevant).
FLAGGED_PMIDS = set()
_state_path = os.path.join(results_dir, 'agent_state.json')
if os.path.exists(_state_path):
    try:
        with open(_state_path, encoding='utf-8') as _f:
            _state = json.load(_f)
        FLAGGED_PMIDS = {
            str(pmid) for pmid, p in _state.get('papers', {}).items()
            if p.get('status') == 'FLAGGED'
        }
    except Exception as _e:
        print(f"  WARNING: could not load agent_state.json FLAGGED list: {_e}")

# Adjudicated non-corpus PMIDs must ALSO be excluded here (added 2026-08-25).
# FLAGGED is derived from state['papers'], but the papers in
# not_corpus_pmids.json were never in state['papers'] at all -- being absent
# from state is precisely why they went unnoticed. So the FLAGGED filter alone
# could not stop them, and their cached full text kept reaching extraction.
_NOT_CORPUS_PMIDS = set()
_nc_path = os.path.join(results_dir, 'not_corpus_pmids.json')
if os.path.exists(_nc_path):
    try:
        with open(_nc_path, encoding='utf-8') as _f:
            _NOT_CORPUS_PMIDS = {str(p) for p in json.load(_f).get('pmids', {})}
    except Exception as _e:
        print(f"  WARNING: could not load not_corpus_pmids.json: {_e}")
FLAGGED_PMIDS |= _NOT_CORPUS_PMIDS

# Section types in PubMed Open-Access XML that should NOT be scanned for
# quantitative claims about the corpus drugs/conditions:
#   REF       - bibliography/references (cites unrelated papers)
#   AUTH_CONT - author contribution statements
#   COMP_INT  - competing interest declarations
#   ACK_FUND  - acknowledgements / funding
#   FIG       - figure captions (numeric values usually not extractable claims)
#   TABLE     - table captions AND tab-delimited table bodies
#   SUPPL     - supplementary material headers
#   ABBR      - abbreviation glossaries ("TNF= Tumor Necrosis Factor; m-TOR=...")
#
# 2026-08-21: FIG, TABLE and ABBR were DOCUMENTED as skip-worthy in this comment
# block since the file was written, but were never added to the set below. That
# implementation-vs-intent gap is the single root cause of BOTH defects logged
# on 2026-08-18:
#   (a) "extractor double-counts bilingual papers" - PMID 39412512 (J Bras
#       Nefrol) carries its results table twice, English at section 60 and
#       Portuguese at section 247, both typed TABLE. That is where "10 mg or"
#       and "10 mg ou" came from. The paper's Portuguese *prose* was already
#       excluded because this journal tags the whole translation as REF; only
#       the duplicated TABLE/FIG leaked through.
#   (b) "extractor scrapes table fragments as data points" - a tab-delimited
#       table body has no sentence boundaries, so a sentence-shaped regex runs
#       across cell borders and returns fragments like
#       "NLRP3 activation in diabetic mice\tDapagliflozinMixed in diet (1".
# Adding the three types closes both. Rejections are still logged individually
# (see REJECT_REASONS) so the decision stays auditable rather than silent.
SKIP_SECTION_TYPES = {
    'REF', 'AUTH_CONT', 'COMP_INT', 'ACK_FUND', 'SUPPL',
    'FIG', 'TABLE', 'ABBR',
}

# ---------------------------------------------------------------------------
# EXTRACTION REJECTION GATE (added 2026-08-21)
# ---------------------------------------------------------------------------
# Section skipping removes bad SOURCES. This gate removes bad MATCHES that
# survive in legitimate prose. Every rejection is recorded with a reason.
#
# Defect found 2026-08-21 while auditing item (b) above: 52 of the 92
# inflammatory_markers extractions (57%) were not measurements at all. The
# patterns end in `.*?(\d+\.?\d*)` - an unbounded lazy wildcard with no unit
# requirement - so the capture group takes the first digit ANYWHERE downstream.
# In immunology prose the nearest digit is almost always part of a molecule
# name or a year:
#     "NLRP3 activation ... Canagliflozin Ameliorates NLRP3"   -> value "3"
#     "NLRP3 expression, Caspase-1"                            -> value "1"
#     "IL-1beta levels and mROS. In 2014"                      -> value "2014"
# A "value" of 3 here is the 3 in NLRP3. These were being counted as
# inflammatory-marker evidence on the published dashboard.

# Molecule/receptor/gene stems whose trailing digit is part of the NAME.
_NAME_STEMS = (
    r'IL|NLRP|NLRC|NLR|NF|TNF|caspase|GSDMD|ASC|TXNIP|CCR|CXCL|CCL|CD|TLR|'
    r'SGLT|GLUT|NOD|P2X|Nrf|AIM|IKK|HOIL|TRAF|IkB|I[kK]appaB|MyD|STAT|JAK|'
    r'SMAD|TGF|IFN|MCP|VEGF|PD-L|PD|GLP|DPP|ACE|AT|S1P|mTORC|AMPK|SIRT|'
    r'HIF|BCL|TREM|LRR|PYD|CARD|ATP|COX|MMP|TIMP|GAD|IA|ZnT|HbA'
)


def rejection_reason(matched_text, values, preceding='', data_type=''):
    """Return a rejection reason string, or None if the match is acceptable.

    `preceding` is the text immediately before the match. It is used only by
    the provenance check, which needs to know whose number this is.

    `data_type` scopes the rules that are only valid for LEVEL-typed extractors.
    A relative change is an artifact in a remission RATE and the whole point of
    an hba1c_change, so the same string must be judged differently depending on
    which extractor produced it.

    Order matters: the cheapest, most certain checks run first.
    """
    if not values:
        return None
    value = str(values[-1])

    # 1. Tab characters mean the regex crossed table-cell boundaries. Requested
    #    explicitly by the 2026-08-18 work-queue item. Kept even though section
    #    skipping now removes most sources, because some journals inline
    #    tab-delimited blocks inside RESULTS.
    if '\t' in matched_text:
        return 'TAB_FRAGMENT'

    # 2. A bare 4-digit 1900-2099 capture is a publication/study year.
    if re.fullmatch(r'(?:19|20)\d\d', value):
        return 'YEAR_AS_VALUE'

    # 3. The captured digit is the trailing digit of a molecule name.
    #    Anchored to the END of the match because that is where the capture
    #    group sits in every affected pattern.
    if re.search(
        r'(?:' + _NAME_STEMS + r')\s*[-‐-―αβ\s]?' + re.escape(value) + r'\s*$',
        matched_text, re.IGNORECASE,
    ):
        return 'MOLECULE_NAME_DIGIT'

    # 4. Value ends the match while an opening parenthesis is still unclosed:
    #    "...Mixed in diet (1" - a truncated dose string, not a measurement.
    if matched_text.count('(') > matched_text.count(')') and matched_text.rstrip().endswith(value):
        return 'UNCLOSED_PAREN_FRAGMENT'

    # 5. IDENTIFIER-SHAPED FRACTION (added 2026-08-22).
    #    Bounding the gaps stops a fraction pairing with a remission mention
    #    two sentences away, but an identifier sitting NEXT TO the word still
    #    matches. These are the ones found in the 2026-08-22 audit:
    #        CTRI/2020/08/027072   trial registration
    #        2018/23JAN/023        ethics approval
    #        CD80/86               co-stimulatory molecule pair
    #        F4/80+                macrophage surface marker
    #        HLA DR3/4             genotype
    #    None is a numerator over a denominator.
    if _IDENTIFIER_FRACTION.search(matched_text):
        return 'IDENTIFIER_FRACTION'

    # 6. DEFINITION THRESHOLD (added 2026-08-22). "remission was defined as an
    #    HbA1c <6.5%" states the study's ENDPOINT DEFINITION, not its result.
    #    Bounding the gaps left three of these as the only surviving remission
    #    artifacts; all three captured 6.5, which is the ADA remission
    #    threshold rather than any trial's remission rate.
    if _DEFINITION_CONTEXT.search(matched_text):
        return 'DEFINITION_THRESHOLD'

    # 7. IMPLAUSIBLE FRACTION: for an n/N event rate the numerator cannot
    #    exceed the denominator. Catches date-shaped pairs (2020/07) that
    #    carry no identifier keyword.
    frac = re.search(r'\b(\d{1,5})\s*/\s*(\d{1,5})\b', matched_text)
    if frac:
        num, den = int(frac.group(1)), int(frac.group(2))
        if den == 0 or num > den:
            return 'IMPLAUSIBLE_FRACTION'

    # 8. WRONG PROVENANCE (added 2026-08-22).
    #
    #    A number in a paper is not automatically a finding OF that paper. Two
    #    provenance classes were found in PMID 36643381 (a colchicine trial
    #    PROTOCOL) while building audit_baseline_citations.py, both published
    #    as corpus evidence for `colchicine -> inflammation`:
    #
    #      "we ESTIMATED that hs-CRP is suppressed to 3.22 mg/L in the
    #       0.25 mg/day treatment group"
    #          -> a sample-size assumption. The trial had not run. This is a
    #             PROJECTION being served as a measurement, which is the most
    #             damaging error class this repository can make.
    #
    #      "because of the PREVIOUS REPORT indicating that colchicine 1 mg for
    #       4 weeks reduced hs-CRP by about 60% in CAD patients with
    #       hs-CRP >=0.2 mg/dL"
    #          -> another trial's result, quoted in the rationale. The captured
    #             0.2 mg/dL is in fact an eligibility threshold.
    #
    #    Same family as the 2026-08-19 insulin_glargine finding, where the
    #    "evidence" came from a meta-analysis's characteristics-of-included-
    #    studies table: the number was real, it just belonged to someone else.
    if preceding and _PROJECTED_VALUE.search(preceding):
        return 'PROJECTED_NOT_MEASURED'
    if preceding and _ATTRIBUTED_ELSEWHERE.search(preceding):
        return 'ATTRIBUTED_TO_OTHER_STUDY'

    # 9. RATIO / BOUND / THRESHOLD MISTYPED AS A RATE (added 2026-08-23).
    #
    #    Raised as a P3 queue item on 2026-08-22: three surviving remission
    #    "rates" are nothing of the kind. Reviewing all 19 found a FOURTH the
    #    item did not list, because it is a different sub-class:
    #
    #      "remission; every 1%"   (40982327)  per-percentage-point effect
    #      "remission by 2%"       (40982327)  relative change, not a level
    #      "remission could be no more than 1%" (37356446)  an upper bound
    #      "remission; <6.0%"      (40982327)  an endpoint threshold  <- MISSED
    #
    #    The fourth escaped the 2026-08-22 DEFINITION_THRESHOLD rule because
    #    that rule keys on the words "defined as"/"criteria"/"cut-off", and
    #    this sentence states the threshold with a bare inequality and no
    #    definitional verb. Checking the abstract of 40982327 confirms the
    #    diagnosis: it is a meta-analysis whose actual remission results are
    #    RISK RATIOS (RR 1.75 and RR 5.80), so no figure in it is a remission
    #    rate at all.
    #
    #    Each number is real. The defect is the TYPE, and a per-point effect
    #    published under a heading that reads "remission rate" is a false
    #    statement about the literature even when every digit is correct.
    #
    #    Anchored to the end of the match so it only fires on the captured
    #    value itself. An unanchored inequality test would reject legitimate
    #    results whose sentence merely contains an eligibility threshold
    #    somewhere earlier ("HbA1c <7% was achieved in 44%").
    if _PER_UNIT_RATE.search(matched_text):
        return 'PER_UNIT_NOT_RATE'
    if _BOUND_NOT_POINT.search(matched_text):
        return 'BOUND_NOT_MEASUREMENT'
    if _TRAILING_INEQUALITY.search(matched_text):
        return 'THRESHOLD_NOT_RATE'

    #    Scoped sub-rule. "increases the probability of reaching remission BY 2%"
    #    is the SAME sentence as the "every 1%" slope above - one statement, two
    #    captures - and it is a change, not a level. But "HbA1c reduced by 1.2%"
    #    is exactly what hba1c_change exists to find. So this only applies to the
    #    extractors whose output is a LEVEL or a RATE.
    #    The verb sits OUTSIDE the match. Every remission pattern anchors on the
    #    word "remission", so in "...increases the probability of reaching
    #    remission by 2%" the match is only "remission by 2%" and the verb that
    #    marks it as a change is in `preceding`. Testing matched_text alone
    #    silently does nothing - which is exactly what happened on the first
    #    attempt at this rule. Joined with a bounded tail of `preceding` for the
    #    same reason the provenance checks read a lookback.
    if data_type in LEVEL_TYPED_EXTRACTORS and \
            _RELATIVE_CHANGE.search(preceding[-120:] + matched_text):
        return 'RELATIVE_CHANGE_NOT_RATE'

    return None


# Language marking a number as PROJECTED rather than observed.
#
# Deliberately does NOT include protocol future tense ("will be randomised",
# "participants will receive"). A first draft did, and it rejected "360 mg
# verapamil" from the Ver-A-T1D protocol - but a planned dose is still the
# dose, and a protocol is the correct source for it. What must be rejected is
# a projected RESULT: a number the study has not yet observed but has assumed
# in order to size itself.
_PROJECTED_VALUE = re.compile(
    r'(?:we\s+(?:estimate|estimated|assume|assumed|anticipate|anticipated|'
    r'expect|expected|project|projected)|assuming\s|sample\s+size\s+'
    r'(?:calculation|estimation|of)|power(?:ed)?\s+(?:calculation|to\s+detect)|'
    r'to\s+achieve\s+\d+\s*%\s+power|is\s+expected\s+to)',
    re.IGNORECASE)

# Language attributing a number to a DIFFERENT study.
_ATTRIBUTED_ELSEWHERE = re.compile(
    r'(?:previous(?:ly)?\s+(?:report|reported|study|studies|trial|shown|'
    r'demonstrated)|prior\s+(?:report|study|studies|trial)|earlier\s+'
    r'(?:report|study|trial)|report\s+indicating|has\s+been\s+reported|'
    r'have\s+been\s+reported|\bet\s+al\.?\s|according\s+to\s+(?:the\s+)?'
    r'(?:previous|prior|a\s+recent))',
    re.IGNORECASE)


# Endpoint-definition phrasing. A number inside one of these is the study's
# threshold for calling an outcome, not the outcome.
_DEFINITION_CONTEXT = re.compile(
    r'(?:defined\s+as|\(defined|definition\s+of|was\s+defined|were\s+defined|'
    r'criteri\w+\s+(?:was|were|of|for)|cut[- ]?off)',
    re.IGNORECASE)

# A number introduced by "every"/"per"/"for each" is an effect PER UNIT of
# something else, not a level. "increases remission; every 1% reduction in
# HbA1c..." is a slope, and a slope filed as a rate is a false claim.
_PER_UNIT_RATE = re.compile(r'\b(?:every|per|for\s+each|each\s+additional)\s+\d',
                            re.IGNORECASE)

# Explicitly bounded or hedged quantities. An upper bound is a statement about
# what the value is NOT.
_BOUND_NOT_POINT = re.compile(
    r'\b(?:no\s+more\s+than|no\s+less\s+than|no\s+greater\s+than|no\s+fewer\s+than|'
    r'at\s+most|at\s+least|not\s+exceed(?:ing)?|up\s+to)\s+[<>≤≥]?\s*\d',
    re.IGNORECASE)

# The captured value is written as an inequality and ends the match: a threshold
# or eligibility criterion, never a measured point estimate.
_TRAILING_INEQUALITY = re.compile(r'[<>≤≥]\s*\d+\.?\d*\s*%?\s*$')

# Extractors whose output is a level or a proportion. For these, a relative
# change ("increased ... by 2%") is a different quantity from the thing being
# extracted. hba1c_change and inflammatory_markers are deliberately absent: a
# change is what they are supposed to capture.
LEVEL_TYPED_EXTRACTORS = {'remission', 'survival_graft', 'autoantibody'}

# "<verb> ... by N%" - a relative change rather than an absolute level.
_RELATIVE_CHANGE = re.compile(
    r'\b(?:increas|decreas|reduc|lower|rais|improv|declin|drop|boost|cut)\w*'
    r'(?:\s+\S+){0,6}?\s+by\s+\d+\.?\d*\s*%?\s*$',
    re.IGNORECASE)

# Identifier contexts in which a `\d+/\d+` string is a name, not a rate.
_IDENTIFIER_FRACTION = re.compile(
    r'(?:CTRI|NCT|ISRCTN|ChiCTR|EudraCT|IRB|REC\b|ethics|approval|'
    r'registr\w*|accession|\bCD\s?\d+\s*/|\bF4\s*/\s*80|\bLy6[A-Z]?\s*/|'
    r'\bHLA|\bDRB1|\bDQB1|\bDQA1|genotype|haplotype)',
    re.IGNORECASE)


def numeric_fingerprint(text):
    """Ordered tuple of numeric tokens in a section.

    Used to detect translated duplicates: a Portuguese rendering of an English
    section restates every number in the same order, so the fingerprints match
    even though almost no words do. This is defence-in-depth behind the
    FIG/TABLE skip - other bilingual journals tag the translation as CONCL or
    METHODS rather than REF, and those types are legitimately scanned.
    """
    return tuple(re.findall(r'\d+(?:\.\d+)?', text))

# ============================================================================
# EXTRACTION PATTERNS
# ============================================================================

EXTRACTORS = {
    # ------------------------------------------------------------------
    # c_peptide, hba1c_change, survival_graft, remission, autoantibody and
    # cost_qaly - BOUNDED 2026-08-22
    #
    # Work-queue item P1 (2026-08-21) flagged these as "suspect by
    # construction" because they carried the same unbounded `.*?` gap that was
    # proven fatal in inflammatory_markers. audit_extractor_wildcards.py
    # measured them on 2026-08-22 and the suspicion was correct - and the
    # damage was larger than the item estimated:
    #
    #     data_type              total   artifact   rate
    #     survival_graft             6          6   100%
    #     c_peptide                  5          5   100%
    #     remission                 48         34    71%
    #     autoantibody               5          3    60%   (not on the suspect list)
    #     hba1c_change              10          5    50%
    #     inflammatory_markers       7          0     0%   (rewritten 2026-08-21)
    #
    # The zero on inflammatory_markers is the control: the same signature set
    # that fails these five passes the one already fixed, so the signal is the
    # wildcard, not the audit.
    #
    # Representative captures the old patterns published as evidence:
    #     "glycated hemoglobin level and insulin dose. RESULTS At 1 year, the
    #      mean AUC for the level of C peptide..."          -> HbA1c = 6.76
    #     "insulin independence was 45.5 +/- 32.0 months"   -> survival = 7.1%
    #     "stimulated C-peptide in ng/mL, fasting blood
    #      glucose in mg/dL, daily needs of..."             -> C-peptide = 0.2
    #     "CTRI/2020/08/027072 ... remission"               -> remission = 2020/07
    #
    # The fix is the same three rules applied to inflammatory_markers:
    #   1. the gap may not cross a sentence boundary or newline -> [^.\n]{0,N}?
    #   2. the captured number must carry a unit, a percent sign, or an
    #      explicit n/N denominator
    #   3. identifier-shaped fractions are rejected by the gate below
    # ------------------------------------------------------------------
    'c_peptide': {
        'patterns': [
            r'[Cc]-peptide\s+(?:level|concentration|was|of|=)\s*(\d+\.?\d*)\s*(pmol/[Ll]|ng/m[Ll]|nmol/[Ll])',
            r'[Cc]-peptide\s+(\d+\.?\d*)\s*±\s*(\d+\.?\d*)\s*(pmol/[Ll]|ng/m[Ll])',
            r'fasting\s+[Cc]-peptide\s*[=:]\s*(\d+\.?\d*)\s*(pmol/[Ll]|ng/m[Ll]|nmol/[Ll])',
            r'[Cc]-peptide\s+(?:increased|decreased|declined|preserved)[^.\n]{0,40}?(\d+\.?\d*)\s*%',
            r'stimulated\s+[Cc]-peptide[^.\n]{0,40}?(\d+\.?\d*)\s*(pmol/[Ll]|ng/m[Ll])',
        ],
        'context_window': 200,
        'gap_relevance': [1, 3, 5, 8, 10],
    },
    'hba1c_change': {
        'patterns': [
            r'HbA1c\s*(?:reduction|decrease|change|lowering)\s*(?:of|was|=)\s*[-−]?\s*(\d+\.?\d*)\s*%',
            r'HbA1c\s*[-−]\s*(\d+\.?\d*)\s*%',
            r'A1c\s+(?:from|was)\s+(\d+\.?\d*)\s*%?\s+to\s+(\d+\.?\d*)\s*%',
            # The trailing `%` is the load-bearing addition: without it this
            # pattern returned the next mean +/- SD in the paper, whatever
            # variable it belonged to (insulin dose, time-in-range, age).
            r'glycated\s+h(?:a)?emoglobin[^.\n]{0,30}?(\d+\.?\d*)\s*±\s*(\d+\.?\d*)\s*%',
            r'HbA1c\s*(\d+\.?\d*)\s*±\s*(\d+\.?\d*)\s*%',
        ],
        'context_window': 200,
        'gap_relevance': [7, 8, 9, 12],
    },
    'survival_graft': {
        'patterns': [
            r'(?:graft|islet|transplant)\s+survival\s*(?:rate|was|of|=)\s*(\d+\.?\d*)\s*%',
            r'insulin\s+independence\s*(?:rate|was|at|of)?[^.\n]{0,40}?(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*%\s*(?:of\s+)?(?:patients?|recipients?)\s+(?:achieved|maintained|remained)\s+insulin\s+independence',
            r'(?:at|after)\s+(\d+)\s*(?:year|yr|month|mo)[^.\n]{0,40}?(\d+\.?\d*)\s*%\s*(?:graft|insulin|survival)',
            r'(\d+)/(\d+)\s*(?:patients?|recipients?)\s+(?:achieved|were)\s+insulin[- ]independent',
        ],
        'context_window': 300,
        'gap_relevance': [2, 3, 4, 11],
    },
    'dose_response': {
        'patterns': [
            r'(\w+(?:\s+\w+)?)\s+(\d+\.?\d*)\s*(mg|µg|mcg|IU|units?)\s*(?:/day|daily|once daily|twice daily|BID|QD)',
            r'(?:dose|dosage)\s+(?:of|was)\s+(\d+\.?\d*)\s*(mg|µg|mcg)',
            r'(\d+\.?\d*)\s*(mg|µg)\s+(?:of\s+)?(\w+)',
        ],
        'context_window': 150,
        'gap_relevance': [4, 7, 8, 12],
    },
    'hazard_ratio': {
        'patterns': [
            r'(?:HR|hazard\s+ratio)\s*[=:]\s*(\d+\.?\d*)\s*(?:\(|,)\s*95%\s*CI\s*[=:,]?\s*(\d+\.?\d*)\s*[-–to]+\s*(\d+\.?\d*)',
            r'(?:HR|hazard\s+ratio)\s*[=:]\s*(\d+\.?\d*)',
        ],
        'context_window': 200,
        'gap_relevance': [2, 6, 11],
    },
    'odds_ratio': {
        'patterns': [
            r'(?:OR|odds\s+ratio)\s*[=:]\s*(\d+\.?\d*)\s*(?:\(|,)\s*95%\s*CI\s*[=:,]?\s*(\d+\.?\d*)\s*[-–to]+\s*(\d+\.?\d*)',
            r'(?:OR|odds\s+ratio)\s*[=:]\s*(\d+\.?\d*)',
        ],
        'context_window': 200,
        'gap_relevance': [2, 6, 10, 11],
    },
    'remission': {
        'patterns': [
            # 34 of 48 remission "data points" were artifact. Pattern 1 ran
            # `.*?` from the word "remission" until it found any digit followed
            # by a percent sign, routinely hundreds of characters and several
            # sentences downstream. Pattern 3 paired ANY two numbers in a
            # sentence with a later mention of remission, which is how the
            # trial-registration number CTRI/2020/08/027072, the ethics
            # approval 2018/23JAN/023, the CD80/86 co-stimulatory pair and the
            # F4/80 macrophage marker all entered the corpus as remission data.
            r'(?:remission|complete\s+response)[^.\n]{0,40}?(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*%\s*(?:remission|complete\s+response)',
            r'\b(\d{1,4})\s*/\s*(\d{1,4})\b[^.\n]{0,40}?(?:remission|complete\s+response)',
        ],
        'context_window': 200,
        'gap_relevance': [7, 8, 9],
    },
    'cost_qaly': {
        'patterns': [
            r'\$\s*(\d[\d,]*\.?\d*)\s*(?:per|/)\s*QALY',
            r'ICER\s*(?:of|was|=)\s*\$?\s*(\d[\d,]*\.?\d*)',
            r'cost[- ]effective(?:ness)?\s*(?:ratio|threshold)[^.\n]{0,40}?\$\s*(\d[\d,]*\.?\d*)',
            r'\$\s*(\d[\d,]*\.?\d*)\s*(?:per\s+patient|annually|per\s+year)',
        ],
        'context_window': 250,
        'gap_relevance': [6, 10, 11, 15],
    },
    # ------------------------------------------------------------------
    # inflammatory_markers - REWRITTEN 2026-08-21
    #
    # The previous patterns ended in `.*?(\d+\.?\d*)`: an UNBOUNDED lazy
    # wildcard, no unit requirement, no sentence boundary. The capture group
    # therefore took the first digit anywhere downstream of the marker name.
    # In immunology prose that digit is essentially never a measurement. Audit
    # of all 92 extractions the old patterns produced:
    #     "NLRP3 activation ... Canagliflozin Ameliorates NLRP3"  -> "3"
    #     "NLRP3 expression, Caspase-1"                           -> "1"
    #     "IL-1beta levels and mROS. In 2014"                     -> "2014"
    #     "NLRP3 activation in diabetic models. 7.2"              -> "7.2"  (section number)
    #     "IL-10 levels ... In a cross-sectional sample of 500"   -> "500"  (sample size)
    # A "value" of 3 is the 3 in NLRP3. None of these are inflammatory-marker
    # levels, and all of them were being served on the published dashboard as
    # extracted corpus evidence.
    #
    # The rewrite enforces three things the old patterns did not:
    #   1. the gap between marker name and number may not cross a sentence
    #      boundary or newline  -> [^.\n]{0,60}?
    #   2. the number must be followed by a CONCENTRATION UNIT, a percent sign
    #      attached to an explicit change verb, or a fold-change token
    #   3. marker names are matched as whole alternatives, so the trailing
    #      digit of the name cannot itself be the capture
    # ------------------------------------------------------------------
    'inflammatory_markers': {
        'patterns': [
            # (1) Absolute level with a concentration unit.
            r'(?:CRP|C-reactive\s+protein|TNF-?[αa]|TNF[- ]alpha|tumor\s+necrosis\s+factor|'
            r'IL-?1\s?[βb]|IL-?6|IL-?10|IL-?18|interleukin[- ]?\d*|NLRP3|NF-?[κk]B)'
            r'[^.\n]{0,60}?(\d+\.?\d*)\s*(pg/m[Ll]|ng/m[Ll]|mg/[Ll]|mg/dL|µg/m[Ll]|ug/m[Ll]|pmol/[Ll]|nmol/[Ll])',
            # (2) Relative change, tied to an explicit direction verb.
            r'(?:CRP|C-reactive\s+protein|TNF-?[αa]|TNF[- ]alpha|IL-?1\s?[βb]|IL-?6|IL-?10|IL-?18|'
            r'NLRP3|NF-?[κk]B)'
            r'[^.\n]{0,60}?(?:increased|decreased|reduced|reduction|elevated|lowered|declined|'
            r'attenuated|suppressed|inhibited|rose|fell)'
            r'[^.\n]{0,40}?(\d+\.?\d*)\s*%',
            # (3) Fold change.
            r'(?:CRP|TNF-?[αa]|IL-?1\s?[βb]|IL-?6|IL-?10|IL-?18|NLRP3|NF-?[κk]B)'
            r'[^.\n]{0,60}?(\d+\.?\d*)[-\s]?fold',
        ],
        'context_window': 200,
        'gap_relevance': [4, 5, 8, 12],
    },
    'autoantibody': {
        'patterns': [
            # Every pattern now requires a percent sign or a titre unit. The
            # bare `(\d+\.?\d*)` in pattern 1 and the `.*?` in patterns 2-4
            # captured the first digit downstream, which produced "95" from
            # "The DIPP study recruited newborns ... HLA DR/DQ genotypes" and
            # "84.6" from "A total of 6,810 patients were screened".
            r'(?:GAD65?|GADA?|GAD\s+antibod)\w*\s*(?:positive|positivity|titer|titre|level|>|=)[^.\n]{0,30}?(\d+\.?\d*)\s*(%|U/m[Ll]|IU/m[Ll])',
            r'(?:IA-2A?|IA-2\s+antibod)\w*\s*(?:positive|positivity|titer|titre|level)[^.\n]{0,30}?(\d+\.?\d*)\s*(%|U/m[Ll]|IU/m[Ll])',
            r'(?:ZnT8A?|ZnT8\s+antibod)\w*\s*(?:positive|positivity|titer|titre|level)[^.\n]{0,30}?(\d+\.?\d*)\s*(%|U/m[Ll]|IU/m[Ll])',
            r'autoantibod\w*\s+(?:positive|positivity|prevalence)[^.\n]{0,30}?(\d+\.?\d*)\s*%',
        ],
        'context_window': 200,
        'gap_relevance': [1, 8, 10],
    },
}


def get_full_text(paper_data):
    """Extract full text from sections.

    Skips sections that are bibliography/admin (REF, AUTH_CONT, COMP_INT,
    ACK_FUND, SUPPL) so that drug/condition co-occurrences in cited paper
    titles do not generate spurious extractions (root cause of PMID 19940299
    rituximab->nephropathy false positive and other reference-section
    contamination bugs).
    """
    sections = paper_data.get('sections', [])
    parts = []
    # Heuristic fallback: if the paper has unstructured strings, also stop
    # scanning once we hit a 'References' / 'Bibliography' header.
    stop_headers = re.compile(r'^\s*(references|bibliography|works cited)\s*$', re.IGNORECASE)
    # Translated-duplicate suppression (2026-08-21). Only sections carrying at
    # least MIN_FP_NUMBERS numeric tokens are fingerprinted; short sections
    # share fingerprints by coincidence far too often to be safe.
    MIN_FP_NUMBERS = 4
    seen_fingerprints = set()
    dup_sections = 0
    for sec in sections:
        if isinstance(sec, dict):
            sec_type = (sec.get('section_type') or '').upper()
            if sec_type in SKIP_SECTION_TYPES:
                continue
            text = sec.get('text', sec.get('content', ''))
            if text:
                fp = numeric_fingerprint(text)
                if len(fp) >= MIN_FP_NUMBERS:
                    if fp in seen_fingerprints:
                        dup_sections += 1
                        continue
                    seen_fingerprints.add(fp)
                parts.append(text)
        elif isinstance(sec, str):
            if stop_headers.match(sec or ''):
                break
            parts.append(sec)
    return ' '.join(parts), dup_sections


def extract_context(text, match_start, match_end, window=200):
    """Get surrounding context for a match."""
    start = max(0, match_start - window)
    end = min(len(text), match_end + window)
    context = text[start:end].strip()
    # Clean up
    context = re.sub(r'\s+', ' ', context)
    return context


def run_extraction():
    """Run all extractors across the corpus."""
    all_extractions = defaultdict(list)
    paper_stats = {}
    dedupe_log = []
    rejected_log = []
    dup_section_log = []

    ft_dir = os.path.join(library_dir, 'fulltext')
    ft_files = sorted(Path(ft_dir).glob('*.json'))

    print(f"Processing {len(ft_files)} full-text papers...")
    print(f"  Excluding {len(FLAGGED_PMIDS)} FLAGGED off-topic PMIDs from extraction.")

    skipped_flagged = 0
    for fp in ft_files:
        with open(fp, encoding='utf-8') as f:
            paper_data = json.load(f)

        pmcid = paper_data.get('pmcid', fp.stem)
        pmid = str(paper_data.get('pmid', ''))

        # Hard-exclude FLAGGED off-topic papers (e.g., CRC, smoking-cessation,
        # melanoma) — they generate spurious drug/condition co-occurrences in
        # the published evidence pipeline. Vetting decisions live in
        # agent_state.json so this stays a single source of truth.
        if pmid and pmid in FLAGGED_PMIDS:
            skipped_flagged += 1
            continue

        full_text, dup_sections = get_full_text(paper_data)
        if dup_sections:
            dup_section_log.append({'pmid': pmid, 'duplicate_sections': dup_sections})

        if not full_text or len(full_text) < 100:
            continue

        meta = papers_meta.get(pmid, {})
        title = meta.get('title', 'Unknown')
        year = meta.get('year', 'Unknown')
        journal = meta.get('journal', 'Unknown')

        paper_extractions = {}

        for data_type, config in EXTRACTORS.items():
            matches_found = []
            for pattern in config['patterns']:
                for match in re.finditer(pattern, full_text, re.IGNORECASE):
                    matched_text = match.group(0)[:200]
                    groups = [g for g in match.groups() if g]

                    # Rejection gate (2026-08-21): drop matches that are
                    # provably not measurements. Logged, never silent.
                    #
                    # The 180-char lookback (added 2026-08-22) feeds the
                    # provenance checks. 180 is roughly one sentence plus its
                    # lead-in, which is the span over which "we estimated" or
                    # "a previous report indicated" governs a number. A wider
                    # window starts capturing unrelated clauses.
                    preceding = full_text[max(0, match.start() - 180):match.start()]
                    reason = rejection_reason(matched_text, groups, preceding,
                                              data_type)
                    if reason:
                        rejected_log.append({
                            'pmid': pmid,
                            'data_type': data_type,
                            'reason': reason,
                            'matched_text': matched_text[:160],
                            'value': str(groups[-1]) if groups else '',
                        })
                        continue

                    context = extract_context(
                        full_text, match.start(), match.end(),
                        config['context_window']
                    )
                    matches_found.append({
                        'matched_text': matched_text,
                        'groups': groups,
                        'context': context[:500],
                        'position': match.start(),
                    })

            if matches_found:
                # Pass 1: deduplicate by position (within 50 chars)
                deduped = []
                seen_positions = set()
                for m in sorted(matches_found, key=lambda x: x['position']):
                    pos_bucket = m['position'] // 50
                    if pos_bucket not in seen_positions:
                        deduped.append(m)
                        seen_positions.add(pos_bucket)

                # Pass 2: deduplicate by NORMALIZED MATCHED TEXT within this
                # (paper, data_type).
                #
                # Added 2026-08-19 after audit found 113/490 corpus data points
                # (23.1%) were the same fact restated in different parts of the
                # same paper. Position bucketing alone cannot catch this: e.g.
                # "360 mg verapamil" occurs 18x in PMID 39613428 at 18 distinct
                # positions and was counted as 18 independent data points. That
                # is one dose, one fact. Counting restatements as evidence
                # inflates data_point_count and makes a single paper look like a
                # body of literature.
                #
                # The first occurrence is kept (with its context); repeat
                # occurrences are recorded as `occurrences` so nothing is lost
                # and the collapse remains auditable.
                text_deduped = []
                by_text = {}
                for m in deduped:
                    norm_text = re.sub(r'\s+', ' ', m['matched_text']).strip().lower()
                    if norm_text in by_text:
                        first = by_text[norm_text]
                        first['occurrences'] += 1
                        first['occurrence_positions'].append(m['position'])
                        continue
                    m['occurrences'] = 1
                    m['occurrence_positions'] = [m['position']]
                    by_text[norm_text] = m
                    text_deduped.append(m)

                dupes_collapsed = len(deduped) - len(text_deduped)
                if dupes_collapsed:
                    dedupe_log.append({
                        'pmid': pmid,
                        'data_type': data_type,
                        'raw': len(deduped),
                        'unique': len(text_deduped),
                        'collapsed': dupes_collapsed,
                    })

                paper_extractions[data_type] = text_deduped
                for m in text_deduped:
                    all_extractions[data_type].append({
                        'pmid': pmid,
                        'pmcid': pmcid,
                        'title': title,
                        'year': year,
                        'journal': journal,
                        'matched_text': m['matched_text'],
                        'values': m['groups'],
                        'context': m['context'],
                        'occurrences': m['occurrences'],
                        'gap_relevance': config['gap_relevance'],
                    })

        if paper_extractions:
            paper_stats[pmid] = {
                'title': title,
                'year': year,
                'journal': journal,
                'pmcid': pmcid,
                'extraction_types': list(paper_extractions.keys()),
                'total_extractions': sum(len(v) for v in paper_extractions.values()),
            }

    if skipped_flagged:
        print(f"  Skipped {skipped_flagged} FLAGGED off-topic full-text papers.")
    return dict(all_extractions), paper_stats, dedupe_log, rejected_log, dup_section_log


def build_cross_gap_evidence(all_extractions):
    """Map extracted data to research gaps."""
    gap_evidence = defaultdict(lambda: defaultdict(list))

    for data_type, extractions in all_extractions.items():
        gap_relevance = EXTRACTORS[data_type]['gap_relevance']
        for ext in extractions:
            for gap_num in gap_relevance:
                gap_evidence[gap_num][data_type].append({
                    'pmid': ext['pmid'],
                    'title': ext['title'],
                    'year': ext['year'],
                    'value': ext['matched_text'][:100],
                    'context': ext['context'][:300],
                })

    return {k: dict(v) for k, v in gap_evidence.items()}


if __name__ == '__main__':
    print("=" * 60)
    print("  CORPUS DATA EXTRACTION PIPELINE")
    print("=" * 60)

    all_extractions, paper_stats, dedupe_log, rejected_log, dup_section_log = run_extraction()

    # Build cross-gap evidence map
    gap_evidence = build_cross_gap_evidence(all_extractions)

    # Summary
    print(f"\n{'=' * 60}")
    print(f"  EXTRACTION SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Papers yielding data: {len(paper_stats)}")
    print()

    total_extractions = 0
    for data_type, extractions in sorted(all_extractions.items(), key=lambda x: -len(x[1])):
        count = len(extractions)
        total_extractions += count
        papers_count = len(set(e['pmid'] for e in extractions))
        print(f"  {data_type:<25} {count:4d} extractions from {papers_count:2d} papers")

    print(f"\n  TOTAL: {total_extractions} data points extracted")

    # Gap evidence summary
    print(f"\n  EVIDENCE BY GAP:")
    gap_names = {
        1: "Gene Therapy LADA", 2: "Health Equity Beta Cell", 3: "Islet Transplant IR",
        4: "Drug Repurposing Islet", 5: "Treg Neuropathy", 6: "CAR-T Access",
        7: "GKA Repurposing", 8: "Immunomod LADA", 9: "GKA LADA",
        10: "LADA Prevalence", 11: "Islet Equity", 12: "Generic Drug Catalog",
        13: "Nutrition Beta", 14: "Nutrition LADA", 15: "GKA Pricing",
    }
    for gap_num in sorted(gap_evidence.keys()):
        types = gap_evidence[gap_num]
        total = sum(len(v) for v in types.values())
        type_list = ', '.join(f"{k}({len(v)})" for k, v in types.items())
        name = gap_names.get(gap_num, f"Gap {gap_num}")
        print(f"    Gap {gap_num:2d} ({name}): {total} data points [{type_list}]")

    # Save output
    collapsed_total = sum(d['collapsed'] for d in dedupe_log)
    print(f"\n  TEXT DEDUPE (added 2026-08-19):")
    print(f"    repeat restatements collapsed: {collapsed_total}")
    print(f"    papers affected              : {len({d['pmid'] for d in dedupe_log})}")
    for d in sorted(dedupe_log, key=lambda x: -x['collapsed'])[:8]:
        print(f"      PMID {d['pmid']} {d['data_type']}: {d['raw']} -> {d['unique']}")

    # Rejection-gate summary
    reason_counts = defaultdict(int)
    for r in rejected_log:
        reason_counts[r['reason']] += 1
    print(f"\n  REJECTION GATE (added 2026-08-21):")
    print(f"    matches rejected as non-measurements: {len(rejected_log)}")
    for reason, n in sorted(reason_counts.items(), key=lambda x: -x[1]):
        print(f"      {reason:<26} {n}")
    dup_total = sum(d['duplicate_sections'] for d in dup_section_log)
    print(f"    translated/duplicate sections dropped: {dup_total} "
          f"across {len(dup_section_log)} papers")

    output = {
        'metadata': {
            'papers_processed': len(paper_stats),
            'total_extractions': total_extractions,
            'extraction_types': {k: len(v) for k, v in all_extractions.items()},
            'rejection_gate': {
                'enabled': True,
                'added': '2026-08-21',
                'rule': 'reject matches that are provably not measurements: tab-crossed '
                        'table fragments, 4-digit years, digits belonging to molecule '
                        'names (the 3 in NLRP3), and values ending inside an unclosed '
                        'parenthesis. Section types FIG/TABLE/ABBR also added to '
                        'SKIP_SECTION_TYPES, matching the intent documented in the '
                        'source comment since the file was written.',
                'rejected_total': len(rejected_log),
                'rejected_by_reason': dict(reason_counts),
                'duplicate_sections_dropped': dup_total,
                'duplicate_section_papers': len(dup_section_log),
            },
            'text_dedupe': {
                'enabled': True,
                'added': '2026-08-19',
                'rule': 'collapse identical normalized matched_text within (pmid, data_type); '
                        'repeat count preserved in the "occurrences" field',
                'restatements_collapsed': collapsed_total,
                'papers_affected': len({d['pmid'] for d in dedupe_log}),
            },
        },
        'dedupe_log': dedupe_log,
        'rejected_log': rejected_log,
        'duplicate_section_log': dup_section_log,
        'extractions': all_extractions,
        'paper_stats': paper_stats,
        'gap_evidence_map': gap_evidence,
    }

    output_path = os.path.join(results_dir, 'extracted_corpus_data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n  Output: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    print(f"\n  Done.")
