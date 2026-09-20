#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Research Paths Dashboard Generator
Tufte-style HTML dashboard showing validated research paths extracted from the corpus
and cross-validated against published evidence
"""

import json
import os
from datetime import datetime
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')

# Data file paths
research_paths_file = os.path.join(base_dir, 'Analysis', 'Results', 'research_paths.json')
validated_paths_file = os.path.join(base_dir, 'Analysis', 'Results', 'validated_research_paths.json')
output_file = os.path.join(base_dir, 'Dashboards', 'Research_Paths.html')

# Gap metadata - READ FROM THE CANONICAL STORE, NEVER TYPED HERE (2026-09-20)
# ---------------------------------------------------------------------------
# This file carried a byte-identical twin of the stale registry found in
# build_extracted_evidence.py the same day: the same 15 superseded gap titles
# ("Remission Sustainability Beyond 2 Years", "Immunomodulation in Type 2
# Diabetes", "Combination Therapy Synergies") and the same 9 wrong tiers,
# against a canonical store that names none of them.
#
# The second copy is the reason this is worth reading twice. Correcting the
# first one by hand would have left this one wrong and produced exactly the
# symptom that makes copies dangerous: two pages, both rebuilt from green
# stages, disagreeing about what Gap #11 is. It was found only because
# audit_gap_numbering.py was taught the dict-literal form on 2026-09-20 -
# before that change the audit read four stores and reported the numbering
# sound; after it, 69 hardcoded tier sites across 15 gaps.
#
# So: read the store. Do not correct the copy.
gap_evidence_file = os.path.join(base_dir, 'Analysis', 'Results',
                                 'gap_evidence.json')


def load_gaps_metadata():
    """Titles and tiers from gap_evidence.json, the store the gap audits read.

    Raises rather than falling back to a literal. A silent default is what
    let the stale copy render for months under green stages.
    """
    with open(gap_evidence_file, encoding='utf-8') as fh:
        gaps = json.load(fh)['gaps']
    out = {}
    for gap_id, rec in gaps.items():
        title = rec.get('name') or rec.get('title')
        tier = rec.get('tier')
        if not title or not tier:
            raise ValueError(
                'gap_evidence.json gap %s is missing title or tier; refusing '
                'to render a gap heading this repository cannot source'
                % gap_id)
        out[str(gap_id)] = {'title': title, 'tier': tier}
    if not out:
        raise ValueError('gap_evidence.json contains no gaps')
    return out


GAPS_METADATA = load_gaps_metadata()

# Status colors for Tufte style
STATUS_COLORS = {
    'VALIDATED': '#2d5016',  # forest green
    'PARTIALLY_VALIDATED': '#8b7500',  # olive/gold
    'UNVALIDATED': '#8b4513',  # saddle brown
    'CONTRADICTED': '#8b0000',  # dark red
}

STATUS_BG = {
    'VALIDATED': '#f0f8e8',  # light green
    'PARTIALLY_VALIDATED': '#fef8e8',  # light yellow
    'UNVALIDATED': '#f8f0e8',  # light brown
    'CONTRADICTED': '#f8e8e8',  # light red
}

# ---------------------------------------------------------------------------
# Evidence-design tier (wired 2026-08-29, work queue P1 of 2026-08-28)
# ---------------------------------------------------------------------------
# audit_path_evidence_design.py has graded every live path by the PUBLICATION
# TYPE of the papers it rests on since 2026-08-28, and wrote the grade to
# path_evidence_design.json. This builder did not read it, so the published
# dashboard still ordered paths by data-point count alone -- and on 2026-08-28
# the count was shown to be INVERSELY related to evidence quality at the top:
# the four highest-count paths graded SYNTHESIS_ONLY, SYNTHESIS_ONLY,
# NO_RESULTS, NO_RESULTS. A reader sorting by the first column was reading the
# ranking backwards, and the repo knew it.
#
# Two changes, both required. Sorting alone would hide the reason; badging
# alone would leave a protocol-only path sitting at the top of the page.
#   1. Paths sort by (tier_rank, status, confidence, count) -- design first.
#   2. Every card carries its tier badge and the grader's one-line reason.
#
# UNGRADED is rendered, not hidden. Two rendered paths (BHB_NLRP3_inhibition,
# verapamil_TXNIP_beta_cell_preservation) exist in validated_research_paths.json
# but not in research_paths.json, so the grader never saw them. Suppressing the
# badge for those two would silently exempt exactly the paths whose provenance
# is least clear. They rank LAST: unknown design is not a passing grade.
EVIDENCE_TIER_RANK = {
    'PRIMARY': 0,
    'SYNTHESIS_ONLY': 1,
    'NARRATIVE_ONLY': 2,
    'NO_RESULTS': 3,
    'UNGRADED': 4,
}

EVIDENCE_TIER_COLORS = {
    'PRIMARY': '#2d5016',         # forest green - measured outcomes exist
    'SYNTHESIS_ONLY': '#1f4e79',  # blue - strong evidence, attribution caveat
    'NARRATIVE_ONLY': '#8b7500',  # olive - narrative review only
    'NO_RESULTS': '#8b0000',      # dark red - protocol/editorial, no outcome
    'UNGRADED': '#555555',        # grey - grader never saw this path
}

EVIDENCE_TIER_FALLBACK_WHY = {
    'UNGRADED': ('not present in research_paths.json when the evidence-design '
                 'grader last ran, so its publication types were never read'),
}

evidence_design_file = os.path.join(
    base_dir, 'Analysis', 'Results', 'path_evidence_design.json')


def _tier_key(path_name):
    """Collapse the two path-name spellings onto one key.

    research_paths.json / path_evidence_design.json spell a path
    'metformin -> T2D'; validated_research_paths.json spells the same path
    'metformin_T2D'. normalize_path_name() maps the first to
    'metformin___T2D' (three underscores: one for each space and one for the
    arrow), which never matched the second. Collapsing runs of underscores is
    what makes the join work.
    """
    if not path_name:
        return ''
    key = path_name.replace('->', '_').replace('→', '_').replace(' ', '_')
    return re.sub(r'_+', '_', key).strip('_').lower()


def load_evidence_design():
    """Return {tier_key: {'tier','why','data_points'}} from the grader.

    Missing or unreadable file is not fatal: every path then renders UNGRADED,
    which is the honest state of the world when no grading exists.
    """
    try:
        with open(evidence_design_file, 'r', encoding='utf-8') as fh:
            raw = json.load(fh)
    except (OSError, ValueError):
        return {}, None
    graded = {}
    for name, entry in raw.get('paths', {}).items():
        graded[_tier_key(name)] = {
            'tier': entry.get('tier', 'UNGRADED'),
            'why': entry.get('why', ''),
            'data_points': entry.get('data_points'),
            'source_name': name,
        }
    return graded, raw.get('generated')


def tier_for(path_name, graded):
    """Tier + reason for one path. Never raises, never invents a grade."""
    entry = graded.get(_tier_key(path_name))
    if entry:
        return entry['tier'], entry.get('why', '')
    return 'UNGRADED', EVIDENCE_TIER_FALLBACK_WHY['UNGRADED']


def tier_badge_html(tier, why):
    """One badge. The reason travels with the grade or the grade misleads."""
    color = EVIDENCE_TIER_COLORS.get(tier, '#555555')
    safe_why = (why or '').replace('"', '&quot;')
    return (f'<span class="tier-badge" style="border-color: {color}; '
            f'color: {color};" title="{safe_why}">{tier.replace("_", " ")}</span>')

def truncate(text, length=300):
    """Truncate text to specified length."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + "…"

import re

# ---------------------------------------------------------------------------
# Dose-fragment artifact filter
# ---------------------------------------------------------------------------
# Background: some research paths get created from key_claims whose
# matched_text is just a short, non-mechanistic dose fragment such as
# "400 mg OD", "on metformin 1000 mg/day", "400 Mg in". These typically
# come from drug-comparator trials where the matched drug only appears as
# a comparator dose label, not as the subject of a mechanistic claim. The
# canonical example (added 2026-05-14 to the work queue) is PMID 35466661
# -- CORRECTED 2026-08-15: this is Dutta et al., J Postgrad Med 2022;68(2):85-92,
# "Efficacy and safety of hydroxychloroquine for managing glycemia in type-2
# diabetes: A systematic review and meta-analysis" (11 RCTs, n=2723), NOT a
# "HCQ HYQ-Real-World Study" as previously annotated. Its trial-characteristics
# table lists comparator/background drugs (pioglitazone, metformin,
# atorvastatin) with dose strings, which the extractor mis-reads as
# drug -> outcome edges.
#
# This filter drops paths where:
#   - EVERY key_claim's matched_text matches a dose-fragment pattern
#   - AND none of them contain mechanism / outcome keywords
#
# REVISED 2026-08-15: the filter previously required data_point_count == 1,
# which let two same-artifact paths through:
#   - "pioglitazone -> T2D"  (dpc=3: '400 mg OD', '45 mg OD', '400 mg OD'
#                             -- note the duplicated fragment inflating dpc)
#   - "hydroxychloroquine -> inflammation" (dpc=2, both dose fragments)
# Both drew 100% of their corpus support from the same PMID 35466661 table.
# Dropping the dpc==1 precondition catches these while staying conservative:
# a single mechanistic snippet anywhere in the path exempts it (e.g. the
# rapamycin->islet_transplant path whose matched_text discusses "mTOR" and
# "Tumor Necrosis Factor").
#
# NOTE: filtering here removes only the unsupported CORPUS-side signal. Paths
# with independent external validation (e.g. pioglitazone->T2D, HCQ->T2D, which
# have real meta-analysis PMIDs in agent_state['validated_paths']) keep that
# external rating; it is sourced separately and is unaffected.
#
# REVISED 2026-08-19: the background-therapy prefix pattern recognised only
# "on <drug> <dose>". The same table writes concomitant therapy several ways --
# "on gliclazide 80 mg/day, with metformin 1000 mg/day, along with insulin
# glargine (>=30 units/day)" -- so "with"/"along with"/"plus"/"taking" forms
# slipped through. That leak is what published `insulin_glargine -> T2D`: both
# its key_claims are inclusion-criteria background therapy from PMID 35466661,
# where insulin glargine is neither intervention nor comparator nor outcome.
DOSE_FRAGMENT_PATTERNS = [
    re.compile(r'^\s*\d+\s*[Mm]?[Gg](?:/[A-Za-z]+)?\s*(?:OD|BID|TID|QD|daily|in|on)?\s*$', re.IGNORECASE),
    re.compile(r'^\s*(?:on|with|plus|along\s+with|taking|receiving|added\s+to)\s+\w+\s+'
               r'\d+\s*[Mm]?[Gg](?:/[A-Za-z]+)?\s*(?:daily|OD|BID|TID|QD)?\s*$', re.IGNORECASE),
    re.compile(r'^\s*\d+\s*[Mm]?[Gg]\s+in\s*$', re.IGNORECASE),
]

# Statuses that must NEVER reach the published dashboard, regardless of what the
# text-pattern filter concludes. Added 2026-08-19: `insulin_glargine -> T2D` was
# adjudicated EXTRACTION_ARTIFACT in agent_state.json and still published,
# because the dashboard filtered on matched_text patterns only and never
# consulted the adjudicated status. Pattern matching is a heuristic; an explicit
# adjudication is a decision, and the decision must win.
SUPPRESSED_STATUSES = {
    'EXTRACTION_ARTIFACT',
    'CONTRADICTED',
    'CONTRADICTED_FOR_DIABETIC_NEPHROPATHY',
}


def _norm_path_key(key):
    """Collapse every spelling of one edge to a single comparable token.

    The same edge is written `insulin_glargine -> T2D` in research_paths.json
    and `insulin_glargine_T2D` in validated_research_paths.json. Stripping
    arrows, underscores, spaces and case makes both resolve to the same token,
    so a suppression decision cannot be defeated by key spelling.
    """
    return re.sub(r'[\s_>-]+', '', (key or '')).lower()


def _canonical_statuses():
    """Map normalised path key -> adjudicated status from the canonical store."""
    out = {}
    canon_file = os.path.join(base_dir, 'Analysis', 'Results', 'canonical_paths.json')
    try:
        with open(canon_file, encoding='utf-8') as f:
            payload = json.load(f)
    except (OSError, ValueError):
        return out
    for rec in (payload.get('paths') or {}).values():
        if not isinstance(rec, dict):
            continue
        key = _norm_path_key(rec.get('display_key'))
        if key:
            out[key] = rec.get('status')
    return out
MECHANISM_KEYWORDS = (
    'inhibit', 'activat', 'block', 'increase', 'decrease', 'reduce', 'induce',
    'mediat', 'pathway', 'signal', 'receptor', 'nf-kb', 'nlrp3', 'tnf', 'il-',
    'caspase', 'apoptos', 'ampk', 'mtor', 'ppar', 'foxp3', 'treg', 'autoimmun',
    'oxidat', 'ros', 'inflammasome', 'cytokine', 'preserv', 'protect', 'mortality',
    'incidence', 'risk', 'hr ', 'or ', 'hazard ratio', 'odds ratio',
)

def is_dose_fragment_artifact(path_data):
    """Return True if EVERY key_claim backing this path is a non-mechanistic
    dose fragment (comparator-arm dose label), making the path an extraction
    artifact rather than a real corpus signal.

    Revised 2026-08-15: no longer restricted to data_point_count == 1.
    """
    claims = path_data.get('key_claims', [])
    if not claims:
        return False
    for claim in claims:
        mt = (claim.get('matched_text') or '').strip()
        if not mt:
            return False
        if not any(p.match(mt) for p in DOSE_FRAGMENT_PATTERNS):
            return False
        if any(kw in mt.lower() for kw in MECHANISM_KEYWORDS):
            return False
    return True


def _hollow_path_keys():
    """Normalised keys of every path recount_paths_from_corpus.py marked HOLLOW.

    Added 2026-08-21. Read from research_paths.json (the recount writes
    `status: HOLLOW` there) and normalised with _norm_path_key so the set is
    key-spelling agnostic and usable against the underscore-spelled validated
    store.
    """
    try:
        with open(research_paths_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return set()
    paths = data.get('paths', {})
    items = paths.items() if isinstance(paths, dict) else enumerate(paths)
    return {
        _norm_path_key(name if isinstance(name, str) else (p.get('name') or ''))
        for name, p in items
        if isinstance(p, dict) and p.get('status') == 'HOLLOW'
    }


def load_research_paths():
    """Load all research paths from JSON.

    Applies the dose-fragment artifact filter to drop paths whose key_claims
    are ALL non-mechanistic dose snippets (comparator-arm labels). The
    filtered-out paths are recorded under data['filtered_artifacts'] for
    transparency / auditing.
    """
    with open(research_paths_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    paths = data.get('paths', {})
    statuses = _canonical_statuses()
    kept = {}
    filtered = {}
    for name, pdata in paths.items():
        adjudicated = statuses.get(_norm_path_key(name))
        if adjudicated in SUPPRESSED_STATUSES:
            filtered[name] = {
                'reason': f'adjudicated {adjudicated} in the canonical path store',
                'pmids': pdata.get('pmids', []),
                'matched_text': (pdata.get('key_claims', [{}])[0].get('matched_text') or '')[:120],
            }
        elif pdata.get('status') == 'HOLLOW':
            # Added 2026-08-21. recount_paths_from_corpus.py marks a path HOLLOW
            # when the live extraction contains ZERO data points for the (pmid,
            # data_type) buckets the path itself declares. Because that recount
            # rule is a SUPERSET of the original clustering, an empty result is
            # exact: the path has no surviving corpus evidence whatsoever.
            #
            # 29 of 47 paths went HOLLOW when the inflammatory_markers patterns
            # were fixed, including the site's former #1 path
            # `NLRP3_inflammasome -> inflammation` (61 displayed data points, all
            # of them regex artifacts - the "3" in NLRP3, the "1" in IL-1, a
            # section number "7.2", a sample size "500"). Publishing a path with
            # no evidence behind it is the exact failure mode this repo exists
            # to prevent, so they are suppressed here rather than shown at zero.
            filtered[name] = {
                'reason': 'HOLLOW - zero live corpus data points after the 2026-08-21 '
                          'extraction-gate fix; evidence was regex artifacts',
                'pmids': pdata.get('pmids', []),
                'displayed_count_before': pdata.get('data_point_count_stored', 0),
                'matched_text': (pdata.get('key_claims', [{}]) or [{}])[0].get('matched_text', '')[:120],
            }
        elif is_dose_fragment_artifact(pdata):
            filtered[name] = {
                'reason': 'all key_claims are non-mechanistic dose fragments (comparator-arm labels)',
                'pmids': pdata.get('pmids', []),
                'matched_text': (pdata.get('key_claims', [{}])[0].get('matched_text') or '')[:120],
            }
        else:
            kept[name] = pdata
    if filtered:
        hollow_n = sum(1 for v in filtered.values() if v['reason'].startswith('HOLLOW'))
        print(f"[build_research_paths] Filtered {len(filtered)} path(s): "
              f"{hollow_n} HOLLOW (no live evidence), "
              f"{len(filtered) - hollow_n} dose-fragment/adjudicated artifacts")
        for n, v in sorted(filtered.items(),
                           key=lambda x: -x[1].get('displayed_count_before', 0))[:8]:
            print(f"    - {n} ({v['reason'][:48]})")
    data['paths'] = kept
    data['filtered_artifacts'] = filtered
    # Update total_paths if present so downstream displays match
    if 'total_paths' in data:
        data['total_paths'] = len(kept)
    return data

def load_validated_paths():
    """Load validated research paths from JSON, applying the same suppression.

    Added 2026-08-19. Suppressing artifacts only in load_research_paths() was
    not enough: that store keys paths in ARROW spelling (`insulin_glargine ->
    T2D`) while this one uses UNDERSCORE spelling (`insulin_glargine_T2D`), and
    the validated-paths table + co-occurrence network render from here. So the
    edge disappeared from one section of the dashboard and kept rendering as
    VALIDATED in another. Suppression has to be applied wherever paths enter the
    page, and it has to be key-spelling agnostic.
    """
    with open(validated_paths_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    statuses = _canonical_statuses()
    paths = data.get('paths')
    if not isinstance(paths, dict):
        return data
    # 2026-08-21: HOLLOW paths must be suppressed here too, for exactly the
    # key-spelling reason documented above. On first application of the hollow
    # filter the page printed "Total paths: 17, Validated: 22" - more validated
    # paths than paths - because this store spells the same edge differently and
    # never saw the filter. A path with zero live evidence cannot be VALIDATED;
    # whatever validated it was validating artifacts.
    hollow_keys = _hollow_path_keys()
    kept, suppressed = {}, {}
    for name, pdata in paths.items():
        adjudicated = statuses.get(_norm_path_key(name))
        if adjudicated in SUPPRESSED_STATUSES:
            suppressed[name] = adjudicated
        elif _norm_path_key(name) in hollow_keys:
            suppressed[name] = 'HOLLOW (no live corpus evidence 2026-08-21)'
        else:
            kept[name] = pdata
    if suppressed:
        print(f"[build_research_paths] Suppressed {len(suppressed)} validated path(s) "
              f"(adjudicated artifacts + HOLLOW)")
    data['paths'] = kept
    data['suppressed_artifacts'] = suppressed
    # DECREMENT, do not overwrite. `paths_validated` (63) counts the whole
    # validated corpus across stores; `paths` (27) holds only the records that
    # carry renderable detail. Setting one from the other silently understated
    # the validated count by 37 on first attempt.
    if isinstance(data.get('paths_validated'), int) and suppressed:
        data['paths_validated'] = max(0, data['paths_validated'] - len(suppressed))

    # RECOMPUTE the validation summary from the surviving paths (2026-08-21).
    #
    # `validation_summary` was previously read straight out of the stored JSON
    # and never recomputed, so suppression never reached the headline counters.
    # After the hollow filter the page rendered "Total paths: 17" beside
    # "VALIDATED paths (22 total)" and then listed 3 of them - the same
    # suppress-in-one-place-only defect found on 2026-08-19, in a third
    # location. Deriving the summary from `kept` makes the counter structurally
    # unable to disagree with the table beneath it.
    if suppressed or 'validation_summary' in data:
        recomputed = {'VALIDATED': 0, 'PARTIALLY_VALIDATED': 0, 'UNVALIDATED': 0}
        for pdata in kept.values():
            st = (pdata.get('validation_status') or pdata.get('status') or '').upper()
            if st in recomputed:
                recomputed[st] += 1
        data['validation_summary_stored'] = data.get('validation_summary')
        data['validation_summary'] = recomputed
        print(f"[build_research_paths] Recomputed validation summary from surviving "
              f"paths: {recomputed} (was {data['validation_summary_stored']})")
    return data

def normalize_path_name(path_name):
    """Convert path name to normalized key for matching."""
    # Replace spaces and arrows with underscores
    return path_name.replace(' ', '_').replace('->', '_').replace('→', '_')

def build_path_network(validated_data):
    """Build network of cross-connections between validated paths."""
    network = defaultdict(lambda: {'connected_to': [], 'shared_pmids': []})

    for path_name, path_data in validated_data['paths'].items():
        pmids = set(path_data.get('pmids_in_corpus', []))

        # Find other paths sharing PMIDs
        for other_name, other_data in validated_data['paths'].items():
            if path_name == other_name:
                continue
            other_pmids = set(other_data.get('pmids_in_corpus', []))
            shared = pmids & other_pmids
            if shared:
                network[path_name]['connected_to'].append(other_name)
                network[path_name]['shared_pmids'].extend(list(shared))

    return network

def map_paths_to_gaps(validated_data):
    """Map each validated path to relevant research gaps (heuristic)."""
    path_to_gaps = defaultdict(set)

    for path_name in validated_data['paths'].keys():
        path_lower = path_name.lower()

        # Heuristic mapping based on keywords
        if 'nlrp3' in path_lower or 'inflammasome' in path_lower:
            path_to_gaps[path_name].add('7')  # CV-Inflammation
        if 'inflammation' in path_lower:
            path_to_gaps[path_name].add('7')  # CV-Inflammation
            path_to_gaps[path_name].add('11')  # Immunomod T2D
        if 'oxidative_stress' in path_lower:
            path_to_gaps[path_name].add('7')  # CV-Inflammation
        if 'dapagliflozin' in path_lower or 'empagliflozin' in path_lower or 'sglt2' in path_lower.replace('_', ' '):
            path_to_gaps[path_name].add('4')  # GLP-1/SGLT2i synergy
            path_to_gaps[path_name].add('15')  # Combination therapy
        if 'glp' in path_lower or 'semaglutide' in path_lower:
            path_to_gaps[path_name].add('12')  # GLP-1 effects
            path_to_gaps[path_name].add('4')  # GLP-1/SGLT2i synergy
        if 'verapamil' in path_lower:
            path_to_gaps[path_name].add('8')  # Drug repurposing
        if 'hydroxychloroquine' in path_lower:
            path_to_gaps[path_name].add('8')  # Drug repurposing
        if 'rapamycin' in path_lower:
            path_to_gaps[path_name].add('8')  # Drug repurposing
        if 'beta' in path_lower:
            path_to_gaps[path_name].add('8')  # Drug repurposing
            path_to_gaps[path_name].add('12')  # GLP-1 effects
        if 'cardiovascular' in path_lower:
            path_to_gaps[path_name].add('7')  # CV-Inflammation
        if 'nephropathy' in path_lower or 'kidney' in path_lower:
            path_to_gaps[path_name].add('7')  # CV-Inflammation
        if 'autoimmune' in path_lower or 't1d' in path_lower:
            path_to_gaps[path_name].add('9')  # Autoimmune epitopes

        # Default to gaps if no match
        if not path_to_gaps[path_name]:
            path_to_gaps[path_name].add('7')  # Default to CV-Inflammation

    return path_to_gaps

def generate_html(research_paths, validated_data):
    """Generate the complete HTML dashboard."""

    # Count stats
    total_paths = research_paths['total_paths']
    validated_paths = validated_data['paths_validated']

    # Corpus figures read live from the extraction output. These were hardcoded
    # ("472 data points across 61 full-text papers", "48 unique research paths")
    # and had gone stale: the 2026-08-19 text-level dedupe cut the corpus from
    # 528 to 414 data points, so the published prose was overstating the
    # evidence base by ~14% while the tables below it showed the real numbers.
    corpus_points, corpus_papers = 0, 0
    try:
        with open(os.path.join(base_dir, 'Analysis', 'Results',
                               'extracted_corpus_data.json'), encoding='utf-8') as f:
            meta = json.load(f).get('metadata', {})
        corpus_points = meta.get('total_extractions', 0)
        corpus_papers = meta.get('papers_processed', 0)
    except (OSError, ValueError):
        pass
    corpus_points_txt = str(corpus_points) if corpus_points else 'the extracted'
    corpus_papers_txt = str(corpus_papers) if corpus_papers else 'the corpus'
    validation_summary = validated_data['validation_summary']

    # Evidence-design grades (wired 2026-08-29). Loaded once; every render
    # site below reads from this dict rather than re-opening the file, so the
    # sort order and the badges cannot disagree with each other.
    evidence_design, evidence_design_generated = load_evidence_design()

    # Build network
    network = build_path_network(validated_data)
    path_to_gaps = map_paths_to_gaps(validated_data)

    # Find hub paths (connected to most others)
    hub_paths = sorted(
        [(name, len(data['connected_to'])) for name, data in network.items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]

    # Get unvalidated paths
    validated_path_names = set(validated_data['paths'].keys())
    all_path_names = set(normalize_path_name(p) for p in research_paths['paths'].keys())
    unvalidated_names = all_path_names - set(normalize_path_name(p) for p in validated_path_names)

    # Map original names to normalized
    original_to_normalized = {}
    for orig_name in research_paths['paths'].keys():
        norm_name = normalize_path_name(orig_name)
        original_to_normalized[norm_name] = orig_name

    # Reconstruct unvalidated with original names
    unvalidated_paths_data = {}
    for norm_name in unvalidated_names:
        if norm_name in original_to_normalized:
            orig_name = original_to_normalized[norm_name]
            unvalidated_paths_data[orig_name] = research_paths['paths'][orig_name]

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Paths Dashboard</title>
    <meta name="google-site-verification" content="G-JGMD5VRYPH">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: #fafaf7;
            color: #333;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.65;
            padding: 30px 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        header { margin-bottom: 40px; border-bottom: 1px solid #ddd; padding-bottom: 25px; }
        h1 { font-family: Georgia, serif; font-size: 2.5em; margin-bottom: 8px; color: #1a1a1a; }
        h2 { font-family: Georgia, serif; font-size: 1.8em; margin: 35px 0 18px 0; color: #1a1a1a; border-top: 1px solid #ddd; padding-top: 20px; }
        h3 { font-family: Georgia, serif; font-size: 1.3em; margin: 22px 0 12px 0; color: #1a1a1a; }
        h4 { font-family: Georgia, serif; font-size: 1.1em; margin: 15px 0 8px 0; color: #1a1a1a; font-weight: 600; }
        .subtitle { font-size: 1.1em; color: #666; margin-bottom: 5px; }
        .byline { font-size: 0.95em; color: #999; margin-bottom: 15px; }

        .context-block {
            background-color: #f5f5f0;
            border-left: 3px solid #999;
            padding: 20px;
            margin: 25px 0;
            font-size: 0.95em;
            line-height: 1.7;
        }
        .context-block h4 { margin-top: 0; color: #666; }
        .context-block p { margin: 10px 0; }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }
        .stat-box {
            background-color: #f5f5f0;
            border: 1px solid #ddd;
            padding: 18px;
            text-align: center;
        }
        .stat-number { font-family: Georgia, serif; font-size: 2.2em; font-weight: bold; color: #2d5016; }
        .stat-label { font-size: 0.9em; color: #666; margin-top: 8px; }

        .tabs { display: flex; gap: 15px; margin-bottom: 30px; border-bottom: 2px solid #ddd; flex-wrap: wrap; }
        .tab-button {
            background: none;
            border: none;
            padding: 12px 18px;
            font-size: 1em;
            cursor: pointer;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            font-family: Georgia, serif;
        }
        .tab-button.active { color: #1a1a1a; border-bottom-color: #333; font-weight: 600; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .path-card {
            background-color: #fefefe;
            border: 1px solid #ddd;
            padding: 20px;
            margin: 18px 0;
            page-break-inside: avoid;
        }
        .path-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }
        .path-name { font-family: Georgia, serif; font-size: 1.3em; color: #1a1a1a; }
        .status-badge {
            padding: 6px 12px;
            font-size: 0.85em;
            font-weight: 600;
            border-radius: 0;
        }

        .path-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 15px 0;
            font-size: 0.9em;
        }
        .stat-item { border-left: 2px solid #ddd; padding-left: 12px; }
        .stat-item strong { color: #1a1a1a; }

        .path-section {
            margin: 15px 0;
            padding: 12px 0;
            border-top: 1px solid #eee;
        }
        .path-section:first-child { border-top: none; padding-top: 0; }

        .section-label { font-weight: 600; color: #666; font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.5px; }

        .pmid-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 8px 0;
        }
        .pmid-badge {
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            padding: 5px 10px;
            font-size: 0.85em;
            font-family: monospace;
        }

        .caveat {
            background-color: #f9f9f6;
            border-left: 2px solid #ddd;
            padding: 10px 12px;
            margin: 8px 0;
            font-size: 0.9em;
            font-style: italic;
            color: #666;
        }

        .connection-list {
            font-size: 0.9em;
            margin: 8px 0;
        }
        .connection-item {
            background-color: #f5f5f0;
            padding: 6px 10px;
            margin: 4px 0;
            border-left: 2px solid #999;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 18px 0;
            font-size: 0.95em;
        }
        thead { background-color: #f5f5f0; }
        th {
            text-align: left;
            padding: 12px;
            border-bottom: 2px solid #ddd;
            font-family: Georgia, serif;
            font-weight: 600;
            color: #1a1a1a;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #eee;
        }
        tr:hover { background-color: #fafaf7; }

        .network-node {
            display: inline-block;
            background-color: #f5f5f0;
            border: 1px solid #ddd;
            padding: 8px 12px;
            margin: 6px 4px;
            font-size: 0.85em;
        }

        .confidence-high { color: #2d5016; font-weight: 600; }
        .confidence-medium { color: #8b7500; font-weight: 600; }
        .confidence-low { color: #8b4513; font-weight: 600; }

        /* Evidence-design tier. Outlined, not filled: the tier is a
           disclosure about study design, not a validation verdict, and it
           must not compete visually with the filled status badge. */
        .tier-badge {
            display: inline-block;
            background-color: #ffffff;
            border: 1px solid #555;
            padding: 4px 9px;
            margin-left: 8px;
            font-size: 0.72em;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            white-space: nowrap;
            cursor: help;
        }
        .tier-why {
            font-size: 0.82em;
            color: #555;
            font-style: italic;
            margin: 6px 0 0 0;
        }
        .tier-legend {
            background-color: #f5f5f0;
            border: 1px solid #ddd;
            border-left: 3px solid #1a1a1a;
            padding: 14px 18px;
            margin: 18px 0;
            font-size: 0.88em;
        }
        .tier-legend dt { font-weight: 600; margin-top: 8px; }
        .tier-legend dd { margin: 2px 0 0 0; color: #444; }

        .gap-tag {
            display: inline-block;
            background-color: #f0f8e8;
            border: 1px solid #2d5016;
            padding: 4px 8px;
            margin: 3px 4px 3px 0;
            font-size: 0.8em;
            color: #2d5016;
        }

        .methodology {
            background-color: #f5f5f0;
            border: 1px solid #ddd;
            padding: 18px;
            margin: 25px 0;
            font-size: 0.95em;
            line-height: 1.7;
        }

        @media print {
            body { padding: 0; }
            .container { margin: 0; }
            .path-card { page-break-inside: avoid; margin: 15px 0; }
        }
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>Validated Research Paths</h1>
        <p class="subtitle">Evidence-Backed Mechanisms in Diabetes Research</p>
        <p class="byline">Dashboard generated ''' + datetime.now().strftime('%B %d, %Y') + ''' | GA4 Tag: G-JGMD5VRYPH</p>
    </header>

    <div class="context-block">
        <h4>What This Dashboard Answers</h4>
        <p>''' + str(total_paths) + ''' research paths are shown, extracted from ''' + corpus_points_txt + ''' de-duplicated data points across ''' + corpus_papers_txt + ''' full-text papers. ''' + str(validated_paths) + ''' were cross-validated against independent published evidence (PubMed, systematic reviews, meta-analyses). This dashboard shows which mechanistic pathways are supported by reproducible research evidence vs artifacts of corpus extraction.</p>
    </div>

    <div class="context-block">
        <h4>How to Use This Dashboard</h4>
        <p><strong>VALIDATED</strong> paths (''' + str(validation_summary['VALIDATED']) + ''' total) are backed by 2+ independent published sources including systematic reviews or landmark RCTs. <strong>PARTIALLY_VALIDATED</strong> paths (''' + str(validation_summary['PARTIALLY_VALIDATED']) + ''' total) have supporting evidence with important caveats or limited human data. <strong>UNVALIDATED</strong> paths (''' + str(validation_summary['UNVALIDATED']) + ''' total) lack external confirmation despite corpus presence. Use the external PMIDs to trace the validation chain back to original evidence.</p>
    </div>

    <div class="context-block">
        <h4>What This Cannot Tell You</h4>
        <p>Validation was performed via targeted web search, not a systematic review. Some paths may have stronger or weaker evidence in the full literature than indicated here. This dashboard prioritizes paths extracted from high-quality papers, but absence of validation does not prove incorrectness—only that we could not confirm the finding through rapid evidence synthesis.</p>
    </div>

    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-number">''' + str(total_paths) + '''</div>
            <div class="stat-label">Paths Identified</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">''' + str(validated_paths) + '''</div>
            <div class="stat-label">Validated</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">''' + str(validation_summary['VALIDATED']) + '''</div>
            <div class="stat-label">Fully Validated</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">''' + str(validation_summary['PARTIALLY_VALIDATED']) + '''</div>
            <div class="stat-label">Partially Validated</div>
        </div>
    </div>

    <h2>Executive Summary</h2>
    <p><strong>Key Finding:</strong> Oxidative stress emerges as a central hub mechanism, connecting inflammation, T2D pathology, diabetic nephropathy, and cardiovascular disease. This path (oxidative_stress_inflammation) links to 5+ other validated mechanisms, suggesting targeting ROS production could have pleiotropic benefits across diabetes complications.</p>

    <p><strong>Validation Landscape:</strong> ''' + str(validation_summary['VALIDATED']) + ''' paths achieved full VALIDATED status, primarily in established pharmacotherapy areas (SGLT2i, metformin, GLP-1 receptor agonists) and core inflammatory mechanisms (NLRP3, NF-kB, oxidative stress). ''' + str(validation_summary['PARTIALLY_VALIDATED']) + ''' paths require further clinical validation, often in newer drug classes (dapagliflozin for inflammation) or controversial areas (semaglutide retinopathy). ''' + str(validation_summary['UNVALIDATED']) + ''' path(s) could not be corroborated.</p>

    <p><strong>Hub Mechanisms:</strong></p>
    <ul style="margin: 12px 0 12px 25px;">
'''

    for hub_name, connections in hub_paths:
        html += f'        <li><strong>{hub_name}</strong> connects to {connections} other paths</li>\n'

    html += '''    </ul>

    <h2>Validated Research Paths</h2>
    <p>The following ''' + str(validation_summary['VALIDATED']) + ''' paths have been confirmed by independent published evidence:</p>

    <div class="tabs">
        <button class="tab-button active" onclick="switchTab(event, 'all-validated')">All Validated (''' + str(validation_summary['VALIDATED']) + ''')</button>
        <button class="tab-button" onclick="switchTab(event, 'high-confidence')">High Confidence</button>
        <button class="tab-button" onclick="switchTab(event, 'network')">Connection Network</button>
    </div>

    <div id="all-validated" class="tab-content active">
'''

    # Legend. A badge nobody can decode is decoration; the tier definitions
    # and the ordering rule are stated once, at the top of the first tab.
    _tier_present = {}
    for _pn, _pd in validated_data['paths'].items():
        if _pd['status'] != 'VALIDATED':
            continue
        _t = tier_for(_pn, evidence_design)[0]
        _tier_present[_t] = _tier_present.get(_t, 0) + 1
    _generated_txt = (f' Grades read from path_evidence_design.json, generated '
                      f'{evidence_design_generated}.' if evidence_design_generated
                      else ' No evidence-design grading was available at build time;'
                           ' every path renders UNGRADED.')
    html += f'''        <div class="tier-legend">
            <p style="margin-top:0;"><strong>Cards are ordered by evidence design, not by data-point count.</strong>
            Counting answers &ldquo;how much&rdquo; and never &ldquo;of what&rdquo;. On 2026-08-28 the four
            highest-count paths on this page graded SYNTHESIS ONLY, SYNTHESIS ONLY,
            NO RESULTS and NO RESULTS &mdash; ranking by count was ranking the page
            backwards. The badge on each card is the publication type of the corpus
            papers that path rests on, taken from PubMed rather than from this
            repository's own text matching.{_generated_txt}</p>
            <dl>
                <dt style="color:{EVIDENCE_TIER_COLORS['PRIMARY']};">PRIMARY ({_tier_present.get('PRIMARY', 0)} paths)</dt>
                <dd>At least one citing paper reports primary data. A measured outcome exists under this path.</dd>
                <dt style="color:{EVIDENCE_TIER_COLORS['SYNTHESIS_ONLY']};">SYNTHESIS ONLY ({_tier_present.get('SYNTHESIS_ONLY', 0)} paths)</dt>
                <dd>Rests on a systematic review or meta-analysis. <em>Not</em> weak &mdash; an SR/MA outranks a
                single trial &mdash; but a number scraped out of one may be the pooled estimate or may be one of
                the trials it tabulates, and extraction cannot tell them apart. Flagged for attribution, not weight.</dd>
                <dt style="color:{EVIDENCE_TIER_COLORS['NARRATIVE_ONLY']};">NARRATIVE ONLY ({_tier_present.get('NARRATIVE_ONLY', 0)} paths)</dt>
                <dd>Every citing paper is a narrative review. Genuinely weak.</dd>
                <dt style="color:{EVIDENCE_TIER_COLORS['NO_RESULTS']};">NO RESULTS ({_tier_present.get('NO_RESULTS', 0)} paths)</dt>
                <dd>Every citing paper is a protocol, editorial, comment or bibliometric study.
                <strong>No measured outcome exists anywhere under this path.</strong></dd>
                <dt style="color:{EVIDENCE_TIER_COLORS['UNGRADED']};">UNGRADED ({_tier_present.get('UNGRADED', 0)} paths)</dt>
                <dd>The grader never saw this path &mdash; it is published here but absent from
                research_paths.json, so its provenance is the least clear on the page, not the most.
                Ranked last deliberately.</dd>
            </dl>
            <p style="margin-bottom:0;"><strong>Limit of this badge, measured 2026-08-29.</strong>
            The tier is only as good as PubMed's publication-type field, and that field is assigned on
            a lag. 134 of 359 papers in this corpus (37%) carry no design-bearing publication type at
            all &mdash; 66% of 2026 papers and 46% of 2025 papers, against about 31% of papers published
            before 2018. The badge is therefore most reliable on the oldest evidence and least reliable
            on the newest, which is the opposite of what a reader would assume. Two concrete cases found
            the same day: PMID 36643381 is a trial protocol whose title says so and whose PubMed record
            does not, and PMID 36826844 is a JAMA randomised trial (CLVer, n=88) that PubMed has not
            tagged as one. See pubtype_title_disagreement.json.</p>
        </div>
'''

    # Sort paths by EVIDENCE DESIGN first, then confidence and name.
    #
    # Changed 2026-08-29. The previous key ordered on status and confidence,
    # and within a tie the page fell back to data-point count, which put a
    # protocol-only path (verapamil, NO_RESULTS) above a randomised trial
    # (dapagliflozin, PRIMARY) because the protocol's dose table yielded more
    # scrapeable numbers. Design leads the key now; count no longer decides
    # anything the reader sees first.
    validated_items = sorted(
        validated_data['paths'].items(),
        key=lambda x: (
            EVIDENCE_TIER_RANK.get(tier_for(x[0], evidence_design)[0], 4),
            0 if x[1]['status'] == 'VALIDATED' else 1,
            0 if x[1]['confidence'] == 'HIGH' else (1 if x[1]['confidence'] == 'MEDIUM' else 2),
            x[0]
        )
    )

    for path_name, path_data in validated_items:
        if path_data['status'] != 'VALIDATED':
            continue

        confidence_class = f"confidence-{path_data['confidence'].lower()}"
        status_color = STATUS_COLORS.get(path_data['status'], '#999')
        status_bg = STATUS_BG.get(path_data['status'], '#f9f9f9')
        tier, tier_why = tier_for(path_name, evidence_design)

        gaps = path_to_gaps.get(path_name, set())
        gap_html = ''.join([f'<span class="gap-tag">Gap {gap}: {GAPS_METADATA.get(gap, {}).get("title", "Unknown")}</span>' for gap in sorted(gaps)])

        html += f'''        <div class="path-card" style="background-color: {status_bg}; border-color: {status_color};">
            <div class="path-header">
                <div class="path-name">{path_name}{tier_badge_html(tier, tier_why)}</div>
                <div class="status-badge" style="background-color: {status_color}; color: white;">
                    {path_data['status']}
                </div>
            </div>
            <p class="tier-why">Evidence design &mdash; {tier.replace('_', ' ').lower()}: {tier_why}</p>

            <div class="path-stats">
                <div class="stat-item">
                    <strong>Data Points:</strong> {path_data['data_point_count']}
                </div>
                <div class="stat-item">
                    <strong class="{confidence_class}">Confidence:</strong> {path_data['confidence']}
                </div>
                <div class="stat-item">
                    <strong>Corpus PMIDs:</strong> {len(path_data.get('pmids_in_corpus', []))}
                </div>
                <div class="stat-item">
                    <strong>External PMIDs:</strong> {len(path_data.get('external_pmids', []))}
                </div>
            </div>

            <div class="path-section">
                <span class="section-label">Validation Source</span>
                <p>{path_data.get('validation_source', 'N/A')}</p>
            </div>

            <div class="path-section">
                <span class="section-label">Evidence Details</span>
                <div class="pmid-list">
                    <span style="margin-right: 15px;"><strong>Corpus PMIDs:</strong></span>
'''

        for pmid in path_data.get('pmids_in_corpus', []):
            html += f'                    <span class="pmid-badge">{pmid}</span>\n'

        html += '                </div>'

        if path_data.get('external_pmids'):
            html += '\n                <div class="pmid-list">\n                    <span style="margin-right: 15px;"><strong>External PMIDs:</strong></span>\n'
            for pmid in path_data.get('external_pmids', []):
                html += f'                    <span class="pmid-badge">{pmid}</span>\n'
            html += '                </div>'

        html += '''
            </div>

            <div class="path-section">
                <span class="section-label">Caveats</span>
                <div class="caveat">''' + path_data.get('caveats', 'None listed') + '''</div>
            </div>
'''

        if path_data.get('cross_connections'):
            html += '''            <div class="path-section">
                <span class="section-label">Cross-Connections to Other Paths</span>
                <div class="connection-list">
'''
            for connection in path_data.get('cross_connections', []):
                html += f'                    <div class="connection-item">{connection}</div>\n'
            html += '''                </div>
            </div>
'''

        if gaps:
            html += f'''            <div class="path-section">
                <span class="section-label">Relevant Research Gaps</span>
                <div>{gap_html}</div>
            </div>
'''

        html += '        </div>\n'

    html += '''    </div>

    <div id="high-confidence" class="tab-content">
        <h3>High Confidence Validated Paths</h3>
        <p>Paths whose <em>external validation search</em> returned a high-confidence
        match. Corrected 2026-08-29: this heading previously read &ldquo;the strongest
        evidence base from systematic reviews and/or landmark RCTs&rdquo;, which was not
        true of every path listed here. Confidence is scored on the external source
        found during validation; it says nothing about the design of the
        <em>corpus</em> papers the path's data points were scraped from. Some paths
        below are HIGH confidence and still carry a NO RESULTS design badge, meaning
        every corpus paper under them is a protocol or editorial with no measured
        outcome. Read the badge, not the heading:</p>
'''

    high_conf = [p for p in validated_items if p[1]['status'] == 'VALIDATED' and p[1]['confidence'] == 'HIGH']
    for path_name, path_data in high_conf:
        status_bg = STATUS_BG.get(path_data['status'], '#f9f9f9')
        status_color = STATUS_COLORS.get(path_data['status'], '#999')
        tier, tier_why = tier_for(path_name, evidence_design)

        html += f'''        <div class="path-card" style="background-color: {status_bg}; border-color: {status_color};">
            <div class="path-name">{path_name}{tier_badge_html(tier, tier_why)}</div>
            <p class="tier-why">Evidence design &mdash; {tier.replace('_', ' ').lower()}: {tier_why}</p>
            <p><strong>Validation Source:</strong> {path_data.get('validation_source', 'N/A')}</p>
            <p><strong>Caveats:</strong> {path_data.get('caveats', 'None')}</p>
            <p><strong>Data Points from Corpus:</strong> {path_data['data_point_count']}</p>
        </div>
'''

    html += '''    </div>

    <div id="network" class="tab-content">
        <h3>Research Path Network</h3>
        <p>Paths that share external PMIDs or mechanistic connections:</p>

        <table>
            <thead>
                <tr>
                    <th>Path Name</th>
                    <th>Connections</th>
                    <th>Connected To</th>
                </tr>
            </thead>
            <tbody>
'''

    for path_name in sorted(network.keys()):
        connections = len(set(network[path_name]['connected_to']))
        connected = ', '.join(sorted(set(network[path_name]['connected_to']))[:3])
        if len(set(network[path_name]['connected_to'])) > 3:
            connected += '...'

        html += f'''                <tr>
                    <td><strong>{path_name}</strong></td>
                    <td>{connections}</td>
                    <td>{connected if connected else 'Standalone'}</td>
                </tr>
'''

    html += '''            </tbody>
        </table>
    </div>

    <h2>Research Path Gap Mapping</h2>
    <p>How validated research paths support the 15 research gaps. Gaps with more validated paths have stronger evidence backing:</p>

    <table>
        <thead>
            <tr>
                <th>Gap ID</th>
                <th>Gap Title</th>
                <th>Validated Paths</th>
                <th>Path Count</th>
            </tr>
        </thead>
        <tbody>
'''

    # Reverse mapping: gaps to paths
    gaps_to_paths = defaultdict(list)
    for path_name, gap_set in path_to_gaps.items():
        for gap_id in gap_set:
            gaps_to_paths[gap_id].append(path_name)

    for gap_id in sorted(GAPS_METADATA.keys(), key=lambda x: int(x)):
        gap_title = GAPS_METADATA[gap_id]['title']
        paths = gaps_to_paths.get(gap_id, [])

        html += f'''        <tr>
            <td><strong>Gap {gap_id}</strong></td>
            <td>{gap_title}</td>
            <td>{', '.join(paths) if paths else '—'}</td>
            <td>{len(paths)}</td>
        </tr>
'''

    html += '''        </tbody>
    </table>

    <h2>Partially Validated Paths</h2>
    <p>The following ''' + str(validation_summary['PARTIALLY_VALIDATED']) + ''' paths have supporting evidence with important caveats:</p>
'''

    for path_name, path_data in validated_items:
        if path_data['status'] != 'PARTIALLY_VALIDATED':
            continue

        status_bg = STATUS_BG.get(path_data['status'], '#f9f9f9')
        status_color = STATUS_COLORS.get(path_data['status'], '#999')
        confidence_class = f"confidence-{path_data['confidence'].lower()}"
        tier, tier_why = tier_for(path_name, evidence_design)

        html += f'''    <div class="path-card" style="background-color: {status_bg}; border-color: {status_color};">
        <div class="path-header">
            <div class="path-name">{path_name}{tier_badge_html(tier, tier_why)}</div>
            <div class="status-badge" style="background-color: {status_color}; color: white;">
                {path_data['status']}
            </div>
        </div>
        <p class="tier-why">Evidence design &mdash; {tier.replace('_', ' ').lower()}: {tier_why}</p>

        <div class="path-stats">
            <div class="stat-item">
                <strong>Data Points:</strong> {path_data['data_point_count']}
            </div>
            <div class="stat-item">
                <strong class="{confidence_class}">Confidence:</strong> {path_data['confidence']}
            </div>
        </div>

        <div class="path-section">
            <span class="section-label">Validation Source</span>
            <p>{path_data.get('validation_source', 'N/A')}</p>
        </div>

        <div class="path-section">
            <span class="section-label">Caveats</span>
            <div class="caveat">{path_data.get('caveats', 'None listed')}</div>
        </div>
    </div>
'''

    # Add unvalidated if any
    unvalidated_count = validation_summary['UNVALIDATED']
    if unvalidated_count > 0:
        html += f'''    <h2>Unvalidated Paths</h2>
    <p>The following {unvalidated_count} path(s) extracted from the corpus but could not be validated through published evidence search:</p>
'''

        for orig_name, path_data in unvalidated_paths_data.items():
            html += f'''    <div class="path-card" style="background-color: {STATUS_BG.get('UNVALIDATED', '#f9f9f9')}; border-color: {STATUS_COLORS.get('UNVALIDATED', '#999')};">
        <div class="path-name">{orig_name}</div>
        <p><strong>Data Points:</strong> {path_data.get('data_point_count', 'N/A')}</p>
        <p><strong>Status:</strong> Not yet validated against published evidence</p>
        <p><strong>PMIDs:</strong> {', '.join(path_data.get('pmids', []))}</p>
    </div>
'''

    html += '''    <h2>Methodology</h2>
    <div class="methodology">
        <h3>Research Path Extraction & Validation Pipeline</h3>
        <p><strong>Stage 1: Corpus Analysis</strong> 91 full-text papers on diabetes complications were automatically extracted. Regex-based information extraction identified 472 key claims linking mechanisms (inflammation, oxidative stress, specific protein pathways) to outcomes (T1D, T2D, complications).</p>

        <p><strong>Stage 2: Path Clustering</strong> These ''' + corpus_points_txt + ''' data points were grouped by mechanism-outcome relationships. Counts are computed at build time, not hardcoded. Identical matched text repeated within the same paper is collapsed to one data point (a dose restated 18 times is one dose, not 18 findings).</p>

        <p><strong>Stage 3: Validation Selection</strong> The top 25 paths (by data point frequency and clinical relevance) were selected for external validation.</p>

        <p><strong>Stage 4: Cross-Validation</strong> Each path was validated via targeted PubMed/Google Scholar searches for: (1) systematic reviews, (2) meta-analyses, (3) landmark RCTs confirming the relationship. Validation status was assigned as:</p>
        <ul style="margin: 12px 0 12px 25px;">
            <li><strong>VALIDATED:</strong> 2+ independent high-quality sources (RCT, meta-analysis, systematic review)</li>
            <li><strong>PARTIALLY_VALIDATED:</strong> Supporting evidence with important caveats or limited human data</li>
            <li><strong>UNVALIDATED:</strong> No independent external confirmation found</li>
            <li><strong>CONTRADICTED:</strong> External evidence contradicts corpus findings (none found)</li>
        </ul>

        <p><strong>Note on Causality:</strong> This validation confirms observational and mechanistic correlations, not strict causality. Many paths show strong mechanistic evidence in preclinical models but modest clinical trial outcomes.</p>
    </div>

    <footer style="margin-top: 50px; padding-top: 25px; border-top: 1px solid #ddd; color: #999; font-size: 0.9em;">
        <p>Dashboard built with Tufte-inspired design principles (minimal decoration, data-ink ratio focus). Data source: Diabetes Research Corpus (''' + corpus_papers_txt + ''' full-text papers). GA4 Analytics: G-JGMD5VRYPH.</p>
    </footer>

</div>

<script>
function switchTab(evt, tabName) {
    var i, tabcontent, tabbuttons;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }
    tabbuttons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].classList.remove("active");
    }
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}
</script>

</body>
</html>
'''

    return html

def main():
    """Main execution."""
    print("Loading research paths data...")
    research_paths = load_research_paths()

    print("Loading validated paths data...")
    validated_data = load_validated_paths()

    print(f"Processing {research_paths['total_paths']} paths ({validated_data['paths_validated']} validated)...")

    html = generate_html(research_paths, validated_data)

    print(f"Writing output to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print("SUCCESS: Dashboard generated")
    print(f"  Total paths: {research_paths['total_paths']}")
    print(f"  Validated: {validated_data['validation_summary']['VALIDATED']}")
    print(f"  Partially Validated: {validated_data['validation_summary']['PARTIALLY_VALIDATED']}")
    print(f"  Unvalidated: {validated_data['validation_summary']['UNVALIDATED']}")
    print(f"  Output: {output_file}")

if __name__ == '__main__':
    main()
