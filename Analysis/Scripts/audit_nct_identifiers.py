#!/usr/bin/env python3
"""Do the TRIAL REGISTRY identifiers name the trials the text says they name?

WHY THIS EXISTS
---------------
This repo has built nine gates around PMIDs. It had built zero around NCT
numbers, and NCT numbers carry claims on the published surface exactly the way
PMIDs do:

    Research_Findings_Summary.md
      "Baricitinib (BARICADE): JAK inhibitor entering Phase 3 trials for T1D
       beta cell preservation. [NCT:NCT06640413] Validation: BRONZE"

NCT06640413 is TheraTri - a phase 1 study of [177Lu]Lu-OncoFAP-23, a
radioligand oncology agent, in FAP-expressing tumours. It is not baricitinib,
it is not diabetes, and it is not phase 3.

The identifier RESOLVES. That is the entire problem, and it is the same problem
the 2026-08-27 through 2026-08-31 runs found eight times over with PMIDs: every
check this repo owns asks whether an identifier is *syntactically valid* or
*reachable*, and a wrong-but-real identifier passes all of them. A reader who
clicks through lands on a genuine ClinicalTrials.gov record and has no reason to
doubt it unless they read the title.

The repo already knew this could happen to an NCT and never generalised it.
build_trial_equity_mapper.py carries this comment:

    # Trials removed in 2026-03-17 audit: NCT03812588 (wrong study), ...

One wrong NCT was found by hand in March, removed, and no gate was built. Five
months later the first systematic pass found 14 of 34 hand-authored NCT
citations naming a different study.

WHAT THIS GATE DOES
-------------------
For every NCT id in the NARRATIVE surface - the documents and builder prose a
human wrote, not the bulk registry snapshots a script pulled - fetch the live
ClinicalTrials.gov v2 record and compare it with the text around the citation:

  NOT_FOUND       the registry has no such study. Published as evidence anyway.
  TOPIC_MISMATCH  the citing text and the registry record share fewer than TWO
                  substantive content words. Generic clinical vocabulary
                  ("study", "phase", "patients", "safety") is stoplisted first,
                  precisely so that two unrelated trials cannot agree by
                  speaking the same boilerplate.
  WEAK_TOPIC_OVERLAP
                  exactly one shared content word. Reported separately rather
                  than folded into either bucket - see FIRST DRAFT below.
  ATTRIBUTE_DISAGREEMENT
                  the topic matches but an asserted attribute does not:
                  acronym, phase, or enrollment count. This catches the case
                  where the right disease and drug are named but the wrong
                  trial in the programme is registered - e.g. NCT04233034 is
                  cited as "Ver-A-T1D" and is actually CLVer.
  OK              nothing falsifiable disagrees.

THE FIRST DRAFT OF THIS GATE WAS WRONG IN TWO WAYS AND THE FIRST RUN PROVED IT
------------------------------------------------------------------------------
Recording both, because the 2026-08-30 run established that a new audit which
is not itself audited just reproduces the defect it was built to catch.

(1) THE CONTEXT WINDOW BLED ACROSS RECORDS. Attributes were read from a flat
    +/-320 character window. In build_trial_equity_mapper.py the trials are a
    list of dict literals roughly 300 characters each, so the window reached
    into the NEIGHBOURING trial and attributed its phase and enrollment to this
    one. NCT05210530 was flagged "text says Phase 3, registry says PHASE1" -
    the text says Phase 1, correctly; the "Phase 3" belonged to the record
    above it. Attribute assertions are now read from the ENCLOSING RECORD only
    (the surrounding `{...}` literal, or the line/sentence in prose).

(2) ONE SHARED WORD WAS TREATED AS TOPICAL AGREEMENT. NCT06176573 is cited as
    the PETITE teplizumab trial and is really a chlorhexidine vaginal-cleansing
    study for post-cesarean infection. It PASSED the topic check on the single
    shared word "prevention". NCT05210530 passed on "type". A threshold of one
    is not a threshold. Raised to two, with the one-token case surfaced as
    WEAK_TOPIC_OVERLAP rather than quietly dropped into OK.

Also removed from the acronym check: drug and target tokens (CD20, CTLA-4),
code-comment words (VERIFIED), and this project's own prediction identifiers
(PRED-2026-002), all of which the first draft offered as "trial acronyms the
text asserts". The check now fires only where the text actually uses a
trial-naming construction next to the identifier.

SCOPE, AND WHY IT IS NARROW
---------------------------
888 distinct NCT ids appear across the repo. 854 of them arrive inside
registry snapshots that baseline_clinical_trials.py pulled from
ClinicalTrials.gov itself; auditing those would be asking the registry whether
it agrees with the registry. The 34 that a human typed next to a claim are the
ones that can be wrong in the way that matters, so those are the ones checked.

SELF-EXCLUSION
--------------
Correction notes written by this project quote the wrong identifier in order to
record it, and code comments record identifiers already removed by an earlier
audit. Both would otherwise be re-flagged forever. Lines carrying a correction
marker are skipped, and the skips are counted and reported rather than hidden.

WHAT THIS GATE DOES NOT DO
--------------------------
It does not invent substitutes. Where the cited trial is wrong, the finding
names the defect and stops. Choosing the right trial is research, and the
2026-08-29 run established the house rule the hard way: mark UNSOURCED, change
no value, invent no replacement.
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS = os.path.join(REPO, 'Analysis', 'Results')
REPORT = os.path.join(RESULTS, 'nct_identifier_audit.json')
CACHE = os.path.join(RESULTS, '.nct_registry_cache.json')

API = 'https://clinicaltrials.gov/api/v2/studies/'

# Narrative surface: what a human wrote a claim into.
NARRATIVE_DIRS = [('docs', '.md'), ('Notes', '.md')]
NARRATIVE_SCRIPT_PREFIXES = ('build_', 'add_')

# Bulk registry pulls: the registry agreeing with itself proves nothing.
EXCLUDED_SCRIPTS = {'baseline_clinical_trials.py', 'audit_nct_identifiers.py'}

CORRECTION_MARKERS = (
    'corrected', 'correction', 'previously cited', 'was wrong', 'wrong study',
    'removed in', 'unsourced', 'do not cite', 'no longer cited', 'retracted',
)

# Clinical boilerplate. Two unrelated trials share all of this and it means
# nothing; leaving it in would let a solar-cell paper "match" a diabetes claim
# on the word "study".
STOP = set("""
a an the and or of for in on to with without at by from as is are was were be been
study studies trial trials phase phases patient patients participant participants
subject subjects treatment treated therapy therapies safety efficacy effect effects
evaluate evaluating evaluation assess assessing assessment placebo randomized
randomised controlled control open label blind blinded double single arm arms dose
doses dosing clinical adult adults child children pediatric paediatric new onset
using use used versus vs compared comparison group groups multicentre multicenter
long term follow up outcome outcomes primary secondary endpoint endpoints year years
month months week weeks day days pts n no not this that these those it its their
who have has had can may will not first second third one two three preliminary
signs tolerability pharmacokinetics recruiting completed active status sponsor
university hospital center centre national institute research program programme
data results reported report ongoing anticipated validation bronze silver gold
""".split())

TOKEN_RE = re.compile(r'[A-Za-z][A-Za-z0-9\-]{3,}')
NCT_RE = re.compile(r'NCT\d{8}')
PHASE_RE = re.compile(r'\bphase[\s:]*([1-4](?:\s*/\s*[1-4])?|i{1,3}v?|early\s*1)\b', re.I)
# 2026-09-23: accept thousands separators. '2,376 enrolled' was read as 376
# (\b matched after the comma) and reported as a registry disagreement on a
# correct figure. Group 1 may now contain commas; callers strip them.
ENROLL_RE = re.compile(r'(?<![\d,])(\d{1,3}(?:,\d{3})+|\d{1,6})\s*(?:pts|patients|participants|subjects|enrolled)\b', re.I)
# Structured-field forms of the same three assertions. See check_attributes().
FIELD_ENROLL_RE = re.compile(r"""['"]enrollment['"]\s*:\s*(\d{1,6})""")

FIELD_STATUS_RE = re.compile(r"""['"]status['"]\s*:\s*['"]([^'"]+)['"]""", re.I)
# Registry states in which the trial is OVER. ACTIVE_NOT_RECRUITING is
# deliberately NOT here: such a trial is still running, so calling it "Active"
# is a fair paraphrase and failing it would be a false positive. Only the
# open-asserted-but-closed direction is a defect.
CLOSED_STATUSES = {
    'COMPLETED', 'TERMINATED', 'WITHDRAWN', 'SUSPENDED', 'NO_LONGER_AVAILABLE',
}
# Words this repo uses to assert a trial IS open. 'active' is included
# deliberately: on this hub's pages it sits beside 'Completed' in the same
# column and is read as "you could still join this".
OPEN_WORDS = {'active', 'recruiting', 'enrolling', 'open', 'ongoing',
              'active, recruiting', 'not yet recruiting'}
ACRONYM_RE = re.compile(r'\b([A-Z][A-Z0-9]{2,}(?:-[A-Z0-9]+)*)\b')

PHASE_MAP = {
    'PHASE1': {'1', 'i'}, 'PHASE2': {'2', 'ii'}, 'PHASE3': {'3', 'iii'},
    'PHASE4': {'4', 'iv'}, 'EARLY_PHASE1': {'early 1', '1', 'i'},
}


def tokens(text):
    return {t.lower() for t in TOKEN_RE.findall(text or '') if t.lower() not in STOP}


def narrative_files():
    out = []
    for name in sorted(os.listdir(REPO)):
        if name.endswith('.md'):
            out.append(os.path.join(REPO, name))
    for sub, ext in NARRATIVE_DIRS:
        base = os.path.join(REPO, sub)
        if not os.path.isdir(base):
            continue
        for dp, _dn, fn in os.walk(base):
            for f in sorted(fn):
                if f.endswith(ext):
                    out.append(os.path.join(dp, f))
    scripts = os.path.join(REPO, 'Analysis', 'Scripts')
    for f in sorted(os.listdir(scripts)):
        if not f.endswith('.py') or f in EXCLUDED_SCRIPTS:
            continue
        if f.startswith(NARRATIVE_SCRIPT_PREFIXES):
            out.append(os.path.join(scripts, f))
    return out


def collect_sites():
    """Every NCT mention on the narrative surface, with the text around it."""
    sites, skipped = [], 0
    for path in narrative_files():
        try:
            text = open(path, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        rel = os.path.relpath(path, REPO)
        for m in NCT_RE.finditer(text):
            line_start = text.rfind('\n', 0, m.start()) + 1
            line_end = text.find('\n', m.end())
            line = text[line_start:line_end if line_end != -1 else len(text)]
            if any(k in line.lower() for k in CORRECTION_MARKERS):
                skipped += 1
                continue
            ctx = re.sub(r'\s+', ' ', text[max(0, m.start() - 320):m.end() + 160])
            sites.append({
                'nct': m.group(0),
                'file': rel.replace('\\', '/'),
                'line': text.count('\n', 0, m.start()) + 1,
                'context': ctx.strip(),
                'record': enclosing_record(text, m.start(), m.end()),
            })
    return sites, skipped


def enclosing_record(text, start, end):
    """The smallest unit that actually ASSERTS things about THIS trial.

    A flat character window is wrong here: these trials are stored as adjacent
    dict literals of about the same size as the window, so a window centred on
    one record reads the phase and enrollment of its neighbour. Prefer the
    enclosing brace literal; fall back to the sentence, then the line.
    """
    # A MENTION INSIDE A COMMENT IS NOT INSIDE THE RECORD ABOVE IT.
    # Added 2026-09-22 after this function handed back a neighbouring trial's
    # dict for an id mentioned in a `#` comment BETWEEN two records: the
    # nearest preceding `{` belonged to the previous trial, the brace-count
    # test passed, and the gate reported "text says 328" for a record whose own
    # enrollment line reads 48. That is the same cross-record bleed the
    # docstring above records as first-draft defect (1), returning by a
    # different route - and it is the worst kind of false positive, because
    # acting on it would replace a correct value with a wrong one.
    line_start_here = text.rfind('\n', 0, start) + 1
    in_comment = text[line_start_here:start].lstrip().startswith('#')

    open_brace = -1 if in_comment else text.rfind('{', max(0, start - 1200), start)
    if open_brace != -1:
        close_brace = text.find('}', end, end + 1200)
        if close_brace != -1 and text.count('{', open_brace, start) == 1:
            return re.sub(r'\s+', ' ', text[open_brace:close_brace + 1]).strip()

    line_start = text.rfind('\n', 0, start) + 1
    line_end = text.find('\n', end)
    line = text[line_start:line_end if line_end != -1 else len(text)]

    # In prose a claim runs to the sentence boundary, which is usually tighter
    # than the line for a markdown paragraph.
    rel_start = start - line_start
    left = max((line.rfind(s, 0, rel_start) for s in ('. ', '! ', '? ', '** ')), default=-1)
    right = min((p for p in (line.find(s, rel_start) for s in ('. ', '! ', '? '))
                 if p != -1), default=-1)
    seg = line[left + 1 if left != -1 else 0: right + 1 if right != -1 else len(line)]
    return re.sub(r'\s+', ' ', seg).strip() or re.sub(r'\s+', ' ', line).strip()


def load_cache():
    if os.path.exists(CACHE):
        try:
            return json.load(open(CACHE, encoding='utf-8'))
        except (ValueError, OSError):
            pass
    return {}


def fetch(nct, cache, max_age_days=30):
    rec = cache.get(nct)
    if rec and (time.time() - rec.get('_fetched', 0)) < max_age_days * 86400:
        return rec
    out = {'_fetched': time.time()}
    try:
        with urllib.request.urlopen(API + nct, timeout=30) as fh:
            d = json.load(fh)
        p = d.get('protocolSection', {})
        idm = p.get('identificationModule', {})
        stm = p.get('statusModule', {})
        dm = p.get('designModule', {})
        cm = p.get('conditionsModule', {})
        am = p.get('armsInterventionsModule', {})
        out.update({
            'found': True,
            'title': idm.get('briefTitle'),
            'official_title': idm.get('officialTitle'),
            'acronym': idm.get('acronym'),
            'sponsor': (idm.get('organization') or {}).get('fullName'),
            'status': stm.get('overallStatus'),
            'start': (stm.get('startDateStruct') or {}).get('date'),
            'phases': dm.get('phases') or [],
            'enrollment': (dm.get('enrollmentInfo') or {}).get('count'),
            'conditions': cm.get('conditions') or [],
            'interventions': [x.get('name') for x in (am.get('interventions') or [])],
        })
    except urllib.error.HTTPError as e:
        out.update({'found': False, 'http': e.code})
    except Exception as e:  # network/parse
        out.update({'found': None, 'error': str(e)})
    cache[nct] = out
    return out


def registry_tokens(rec):
    parts = [rec.get('title') or '', rec.get('acronym') or '', rec.get('sponsor') or '']
    parts += rec.get('conditions') or []
    parts += [x for x in (rec.get('interventions') or []) if x]
    return tokens(' '.join(parts))


def check_attributes(site, rec):
    """Topic agrees; does anything the text ASSERTS still disagree?

    Reads the ENCLOSING RECORD, not the wide context window. The first draft
    read the window and reported a neighbouring trial's phase as this one's.
    """
    issues = []
    ctx = site['record']

    # An attribute must be asserted NEXT TO the identifier to be an assertion
    # ABOUT it. "Validation: GOLD (phase 2 plus two independent phase 3 RCTs)"
    # describes an evidence base, not this trial's phase, and the first draft
    # read it as a phase claim.
    at = ctx.find(site['nct'])
    near = ctx[max(0, at - 100):at + 100] if at != -1 else ''
    # ...but not across a FIELD boundary. Added 2026-09-22.
    # A dict record is one "enclosing record" but several separate assertions,
    # and the 100-char window spans them. build_immunomod_lada.py stores
    #     "t1d_evidence":  "DIAGNODE-3 Phase 3 ... did NOT replicate in the
    #                       confirmatory Phase 3."
    #     "lada_evidence": "... small pilot data (NCT04262479, n=14) ..."
    # Both true, both correctly written. The window reached back over the field
    # boundary, picked up the DIAGNODE-3 phase, and reported it as a phase
    # claim about NCT04262479 - failing a line whose author had got it right.
    # Trimming at the nearest field delimiter keeps an assertion attached to
    # the field that makes it.
    if at != -1:
        rel = min(at, 100)
        left = max(near.rfind(d, 0, rel) for d in ('",', "',", '":', "':"))
        right_cands = [p for p in (near.find(d, rel + len(site['nct']))
                                   for d in ('",', "',")) if p != -1]
        near = near[left + 2 if left != -1 else 0:
                    min(right_cands) if right_cands else len(near)]

    m = PHASE_RE.search(near)
    if m and rec.get('phases'):
        asserted = m.group(1).lower().replace(' ', '')
        reg = set()
        for ph in rec['phases']:
            reg |= PHASE_MAP.get(ph, set())
        claimed = {p for p in re.split(r'/', asserted) if p}
        if reg and claimed and not (claimed & reg):
            issues.append({
                'attribute': 'phase',
                'asserted': m.group(0), 'registry': rec['phases'],
            })

    # ------------------------------------------------------------------
    # STRUCTURED-FIELD ASSERTIONS, added 2026-09-22.
    #
    # Until today every check here read PROSE: ENROLL_RE requires the number to
    # be followed by "patients"/"participants"/"subjects"/"enrolled". This repo
    # also asserts the same facts as DICT FIELDS -- `'enrollment': 330,` -- and
    # against those the regex matches nothing, so the check did not fail, it
    # never ran. Measured this run: build_trial_equity_mapper.py holds 12 trial
    # records, five of which state an enrollment that disagrees with the live
    # registry (one by 330 vs 14), and this gate reported 30/30 OK.
    #
    # Same shape as the dict-literal blind spot audit_gap_numbering.py found on
    # 2026-09-20. A gate that reads only prose is not checking a repository
    # that stores half its claims as data.
    # NOTE on phase: no structured form is needed. The dict field reads
    # `'phase': 'Phase 3'`, which PHASE_RE already matches on the prose path.
    field_enroll = FIELD_ENROLL_RE.search(ctx)

    asserted_n = None
    if m := ENROLL_RE.search(near):
        asserted_n = int(m.group(1).replace(',', ''))
    elif field_enroll:
        asserted_n = int(field_enroll.group(1))
    if asserted_n is not None and rec.get('enrollment'):
        reg_n = rec['enrollment']
        # A stated participant count is a factual claim. Allow 10% drift for
        # planned-vs-actual, flag anything wider.
        if reg_n and abs(asserted_n - reg_n) > max(3, 0.10 * reg_n):
            issues.append({
                'attribute': 'enrollment',
                'asserted': asserted_n, 'registry': reg_n,
            })

    # ------------------------------------------------------------------
    # RECRUITMENT STATUS, added 2026-09-22, and it was never an audited
    # attribute anywhere in this repository.
    #
    # "Active" / "Recruiting" beside a trial the registry closed years ago is
    # the one wrong attribute a reader may ACT on: it is the difference between
    # a trial a patient could ask to join and one that finished before they
    # read the page. Six of the twelve entries in build_trial_equity_mapper.py
    # asserted Active or Recruiting for trials ClinicalTrials.gov records as
    # COMPLETED, the oldest completed in 2014.
    #
    # Only the open-vs-closed DIRECTION is failed, not exact string equality.
    # "Active" against ACTIVE_NOT_RECRUITING is a reasonable paraphrase; the
    # defect is asserting a trial is open when the registry says it is closed.
    fs = FIELD_STATUS_RE.search(ctx)
    if fs and rec.get('status'):
        asserted_s = fs.group(1).strip().lower()
        reg_s = rec['status']
        if asserted_s in OPEN_WORDS and reg_s in CLOSED_STATUSES:
            issues.append({
                'attribute': 'status',
                'asserted': fs.group(1), 'registry': reg_s,
            })

    reg_acr = (rec.get('acronym') or '').upper()
    if reg_acr:
        cands = asserted_trial_names(ctx, rec)
        if cands:
            base = reg_acr.split('-')[0]
            if reg_acr not in cands and not any(c.split('-')[0] == base for c in cands):
                issues.append({
                    'attribute': 'acronym',
                    'asserted': sorted(cands), 'registry': rec['acronym'],
                })
    return issues


# Constructions that actually NAME a trial, as opposed to any capitalised token
# that happens to sit nearby. The first draft accepted CD20, CTLA-4, VERIFIED
# and PRED-2026-002 as "trial acronyms the text asserts"; none of them are.
NAME_FIELD_RE = re.compile(r"""['"]name['"]\s*:\s*['"]([^'"]+)['"]""")
# A trial name the author put in parentheses at the end of a label:
#   'Verapamil for beta cell preservation in T1D (Ver-A-T1D)'  ->  Ver-A-T1D
#   'Teplizumab PROTECT (anti-CD3 for recent-onset T1D)'       ->  (a description)
TRAILING_PAREN_RE = re.compile(r'\(([^)]{2,40})\)\s*$')
NOT_A_TRIAL_NAME = {
    'T1D', 'T2D', 'LADA', 'VERIFIED', 'UNVERIFIED', 'CORRECTED', 'UNSOURCED',
    'GOLD', 'SILVER', 'BRONZE', 'PHASE', 'NOTE', 'TODO', 'FIXME', 'PMID',
    'DOI', 'FDA', 'NIH', 'NIDDK', 'NIAID', 'RCT', 'CGM', 'HCL', 'AUC',
    'USA', 'PPH', 'US', 'UK',
}


def asserted_trial_names(ctx, rec):
    """Trial names the text actually asserts, not every capitalised token.

    Deliberately narrow. The only construction trusted is a parenthesised name
    at the end of an explicit `'name'` label, because that is the one place in
    this repo where an author is unambiguously naming the trial rather than
    describing it. Everything looser produced noise: the first draft offered
    CD20, CTLA-4, VERIFIED and PRED-2026-002 as asserted trial acronyms, and
    the second offered the words FOR and NEW-ONSET.
    """
    out = set()
    for raw in NAME_FIELD_RE.findall(ctx):
        m = TRAILING_PAREN_RE.search(raw.strip())
        if not m:
            continue
        cand = m.group(1).strip()
        if ' ' in cand:          # a description, not a name
            continue
        out.add(cand.upper())

    reg_words = {w.upper() for w in TOKEN_RE.findall(
        ' '.join([rec.get('title') or '', rec.get('official_title') or '',
                  rec.get('sponsor') or '']
                 + (rec.get('interventions') or []) + (rec.get('conditions') or [])))}
    out -= reg_words
    out -= NOT_A_TRIAL_NAME
    out = {a for a in out if not re.match(r'^(PRED|GAP|PATH|RUN)[-_]', a)}
    out = {a for a in out if not re.match(r'^[A-Z]{2,4}-?\d+$', a)}
    return out


def main():
    sites, skipped = collect_sites()
    by_nct = {}
    for s in sites:
        by_nct.setdefault(s['nct'], []).append(s)

    print(f'NCT sites on narrative surface: {len(sites)}  '
          f'distinct: {len(by_nct)}  correction-note skips: {skipped}')

    cache = load_cache()
    findings = []
    counts = {'OK': 0, 'NOT_FOUND': 0, 'TOPIC_MISMATCH': 0,
              'WEAK_TOPIC_OVERLAP': 0, 'ATTRIBUTE_DISAGREEMENT': 0,
              'UNREACHABLE': 0}

    for nct in sorted(by_nct):
        rec = fetch(nct, cache)
        time.sleep(0.12)
        site = by_nct[nct][0]

        if rec.get('found') is None:
            counts['UNREACHABLE'] += 1
            continue

        if not rec.get('found'):
            counts['NOT_FOUND'] += 1
            findings.append({
                'nct': nct, 'verdict': 'NOT_FOUND',
                'detail': 'ClinicalTrials.gov returns no study with this id',
                'sites': by_nct[nct],
            })
            continue

        shared = tokens(site['context']) & registry_tokens(rec)
        if len(shared) < 2 and len(by_nct[nct]) > 1:
            # Topic is judged on the FIRST site only (see note on the attribute
            # loop below for why attributes are not). Where an id is cited in
            # several places, use the site with the strongest overlap so a bare
            # mention in a doc cannot make a well-described citation look
            # off-topic.
            best = max(by_nct[nct],
                       key=lambda s: len(tokens(s['context']) & registry_tokens(rec)))
            site = best
            shared = tokens(site['context']) & registry_tokens(rec)
        if len(shared) < 2:
            # A threshold of one is not a threshold: a chlorhexidine cesarean
            # trial passed as PETITE teplizumab on the shared word "prevention".
            verdict = 'TOPIC_MISMATCH' if not shared else 'WEAK_TOPIC_OVERLAP'
            counts[verdict] += 1
            findings.append({
                'nct': nct, 'verdict': verdict,
                'registry_title': rec.get('title'),
                'registry_conditions': rec.get('conditions'),
                'registry_interventions': rec.get('interventions'),
                'shared_terms': sorted(shared),
                'detail': ('fewer than two substantive content words are shared '
                           'between the citing text and the registry record'),
                'sites': by_nct[nct],
            })
            continue

        # EVERY SITE, added 2026-09-22. Until today this line read
        #
        #     attr = check_attributes(site, rec)
        #
        # with `site = by_nct[nct][0]` fixed above it, so exactly ONE mention of
        # each identifier was examined and every other mention was discarded
        # unread. Measured on the run that found it: 61 sites, 30 distinct ids
        # -- so 31 mentions, more than half the narrative surface, had never
        # been checked by this gate at any point in its existence.
        #
        # It is not a uniform loss. The mention most likely to be skipped is
        # the one most likely to be wrong, because the skipped mentions are the
        # SECOND AND LATER ones, and this repo's richest assertions live in the
        # builder dict literals that tend to sort after a passing reference in
        # a markdown doc. NCT04786262 is the case: twelve sites, first is
        # RESEARCH_DOCTRINE.md asserting nothing, twelfth is
        # build_trial_equity_mapper.py declaring "Phase 1/2" and n=17 for a
        # trial the registry now lists as PHASE3 with 57. Both disagreements
        # were computed correctly by check_attributes() and then thrown away.
        attr, seen = [], set()
        for s in by_nct[nct]:
            for d in check_attributes(s, rec):
                key = (d['attribute'], repr(d['asserted']))
                if key in seen:
                    continue
                seen.add(key)
                attr.append(dict(d, site='%s:%d' % (s['file'], s['line'])))
        if attr:
            counts['ATTRIBUTE_DISAGREEMENT'] += 1
            findings.append({
                'nct': nct, 'verdict': 'ATTRIBUTE_DISAGREEMENT',
                'registry_title': rec.get('title'),
                'registry_acronym': rec.get('acronym'),
                'registry_status': rec.get('status'),
                'shared_terms': sorted(shared)[:12],
                'disagreements': attr,
                'sites': by_nct[nct],
            })
            continue

        counts['OK'] += 1

    os.makedirs(RESULTS, exist_ok=True)
    with open(CACHE, 'w', encoding='utf-8') as fh:
        json.dump(cache, fh, indent=1, ensure_ascii=False)

    report = {
        'generated': time.strftime('%Y-%m-%d'),
        'scope': ('repo-root .md, docs/, Notes/, and Analysis/Scripts/build_*.py '
                  'and add_*.py prose. Bulk registry snapshots excluded: asking '
                  'ClinicalTrials.gov whether it agrees with ClinicalTrials.gov '
                  'proves nothing.'),
        'sites_checked': len(sites),
        'distinct_nct': len(by_nct),
        'correction_note_skips': skipped,
        'counts': counts,
        'findings': findings,
    }
    with open(REPORT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)

    print('  ' + '   '.join(f'{k}: {v}' for k, v in counts.items()))
    for f in findings:
        print(f'\n  [{f["verdict"]}] {f["nct"]}  ({len(f["sites"])} site(s))')
        if f.get('registry_title'):
            print(f'      registry: {f["registry_title"][:96]}')
        if f.get('disagreements'):
            for d in f['disagreements']:
                print(f'      {d["attribute"]}: text says {d["asserted"]!r}, '
                      f'registry says {d["registry"]!r}')
                if d.get('site'):
                    print(f'          at {d["site"]}')
        else:
            print(f'      cited in: {f["sites"][0]["file"]}:{f["sites"][0]["line"]}')

    print(f'\nReport: {os.path.relpath(REPORT, REPO)}')
    if findings:
        print('\n[FAIL] NCT identifier audit found issues')
        return 1
    print('\n[OK] trial registry identifiers agree with ClinicalTrials.gov')
    return 0


if __name__ == '__main__':
    sys.exit(main())
