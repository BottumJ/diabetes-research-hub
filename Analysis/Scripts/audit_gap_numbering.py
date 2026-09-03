#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Does gap N in the agent's memory mean the same thing as gap N on the site?

Written 2026-09-03 after a measurement, not a hunch.

On 2026-09-02 a run found that gaps["15"].audit_history in agent_state.json had
been auditing SGLT2i x personalized nutrition since 2026-04-16, while canonical
Gap #15 is the GKA Pricing Trajectory Model. That run treated it as one orphaned
audit trail and queued a re-homing.

It is not one trail. Sweeping all fifteen the same way finds SIX state gap
numbers whose audit trails answer a different question than the gap that number
names on the published site:

    state #4  audits Islet Transplant x Personalized Nutrition
    state #5  audits Islet Transplant x Drug Repurposing   (= canonical #4)
    state #7  audits Polygenic Risk Score x Closed-Loop AID
    state #11 audits CAR-Treg x Personalized Nutrition
    state #12 audits Treg x Diabetic Peripheral Neuropathy (= canonical #5)
    state #15 audits SGLT2i x Personalized Nutrition

Every one of those trails is INTERNALLY CONSISTENT back to April. Nothing
wandered. Two numbering schemes were built independently and never reconciled,
so the agent's memory and the site have been using the same integers to mean
different research questions for five months.

Why that is worse than it looks: a gap's tier is a claim about evidence. If the
agent audits question A and writes the verdict into the slot the site publishes
as question B, then an audit can strengthen or weaken a tier it never examined.
The failure is silent because both halves are individually well-formed.

This gate makes the collision visible, on two axes:

  TIER AGREEMENT  - agent_state, gap_evidence.json and docs/index.html must
                    publish the same tier for the same integer. Any two-way
                    disagreement is a defect regardless of direction: a site
                    that under-claims is still a site that disagrees with its
                    own evidence store.

  TOPIC AGREEMENT - the recent audit notes filed under gap N must mention what
                    gap N is about. Scored by token overlap against the
                    canonical name with light suffix normalisation, because the
                    naive version reports "Immunomodulatory Drugs for LADA" as
                    drift when its audits say "immunomodulator" - a real false
                    positive this gate hit on its first run.

REPORTS, DOES NOT APPLY. Re-homing an audit trail rewrites the audit record,
and which trail is authoritative is a human call, not a scripted one. Same
posture as audit_gap_evidence_design.py.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RESULTS = os.path.join(ROOT, 'Analysis', 'Results')

STATE = os.path.join(RESULTS, 'agent_state.json')
EVIDENCE = os.path.join(RESULTS, 'gap_evidence.json')
SITE = os.path.join(ROOT, 'docs', 'index.html')
OUT = os.path.join(RESULTS, 'gap_numbering_audit.json')

# How many of the most recent audits to read. Enough to be representative,
# few enough that one badly-filed audit does not hide behind ten good ones.
RECENT_AUDITS = 3

# Below this share of DISCRIMINATIVE canonical name tokens appearing in the
# audit text, the trail is reported as answering a different question.
TOPIC_FLOOR = 0.5

# A token appearing in this many canonical gap names or more carries no
# identifying signal and is dropped before scoring. Measured, not assumed: the
# naive all-tokens version passed state #4 and #11 - both genuinely misfiled -
# because "islet", "transplant" and "drug" are shared across several gap names,
# so a trail about islet transplants scored 50% against a gap about islet
# transplant DRUG REPURPOSING while discussing nutrition. Scoring only on the
# words that tell one gap from another is what makes the check discriminating.
COMMON_TOKEN_CUTOFF = 3

# Words that carry no topic signal.
STOP = {
    'for', 'in', 'by', 'the', 'and', 'of', 'a', 'an', 'x', 'to', 'on',
    'with', 'under', 'review', 'analysis', 'model', 'landscape', 'setting',
    'strategy', 'health', 'care',
}

# Suffixes stripped longest-first. Three of these were added because the gate
# reported a false positive on its own first run, not because they seemed
# useful: 'ory'/'or' unify "immunomodulatory" with "immunomodulator" (gap #8),
# 'ic'/'es' unify "diabetic" with "diabetes", and the 4-character stem floor
# unifies "drugs" with "drug". Light on purpose: aggressive stemming would
# collapse distinct terms and hide real drift.
SUFFIXES = ('ational', 'ization', 'isation', 'ology', 'ical', 'ally', 'ing',
            'ory', 'ive', 'ion', 'ess', 'ers', 'er', 'al', 'ed', 'es', 'ic',
            'or', 'y', 's')

MIN_STEM = 4


def normalise(word):
    """Light suffix stripping. Never shortens a word below MIN_STEM."""
    w = word.lower()
    for suf in SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= MIN_STEM:
            return w[:-len(suf)]
    return w


def tokens(text):
    out = []
    for raw in re.findall(r"[A-Za-z0-9]+", text or ''):
        if len(raw) < 3 or raw.lower() in STOP:
            continue
        out.append(normalise(raw))
    return out


def site_tiers(path):
    """Tiers as a reader sees them, parsed from the published page."""
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            html = fh.read()
    except OSError:
        return {}
    found = {}
    for m in re.finditer(r'Gap #(\d+)\s*\((GOLD|SILVER|BRONZE|EXPLORATORY)\b',
                         html):
        found.setdefault(m.group(1), set()).add(m.group(2))
    # A gap labelled two different tiers on one page is itself a defect;
    # keep the set so the caller can say so rather than picking one.
    return found


def source_tiers(scripts_dir):
    """Gap tiers hardcoded as literals in build scripts.

    Found 2026-09-03: the tier is not stored once and read. It is TYPED, in at
    least four places - agent_state.json, gap_evidence.json, the card text in
    rebuild_website.py, and the stage labels in run_quality_improvements.py.
    Three of those disagree on three gaps (#6, #11, #13). A number copied into
    four files will drift; the only question is when. This finds the copies.
    """
    hits = {}
    if not os.path.isdir(scripts_dir):
        return hits
    pat = re.compile(r'Gap #(\d+)\s*\((GOLD|SILVER|BRONZE|EXPLORATORY)\b')
    for fname in sorted(os.listdir(scripts_dir)):
        if not fname.endswith('.py') or fname == os.path.basename(__file__):
            continue
        try:
            with open(os.path.join(scripts_dir, fname), 'r',
                      encoding='utf-8') as fh:
                body = fh.read()
        except OSError:
            continue
        for m in pat.finditer(body):
            line = body.count('\n', 0, m.start()) + 1
            hits.setdefault(m.group(1), []).append(
                {'file': fname, 'line': line, 'tier': m.group(2)})
    return hits


def main():
    try:
        with open(STATE, 'r', encoding='utf-8') as fh:
            state = json.load(fh)
        with open(EVIDENCE, 'r', encoding='utf-8') as fh:
            evidence = json.load(fh)['gaps']
    except (OSError, ValueError, KeyError) as exc:
        print('  [skip] cannot read inputs: %s' % exc)
        return 0

    published = site_tiers(SITE)
    hardcoded = source_tiers(HERE)

    # Which name tokens are shared across the gap set, and therefore say
    # nothing about WHICH gap a piece of text is discussing.
    doc_freq = {}
    for canon in evidence.values():
        for tok in set(tokens(canon.get('name', ''))):
            doc_freq[tok] = doc_freq.get(tok, 0) + 1
    common = {t for t, n in doc_freq.items() if n >= COMMON_TOKEN_CUTOFF}

    rows, tier_defects, topic_defects = {}, [], []

    for gid in sorted(evidence, key=lambda k: int(k)):
        canon = evidence[gid]
        name = canon.get('name', '')
        st = state.get('gaps', {}).get(gid, {})

        state_tier = st.get('tier')
        evid_tier = canon.get('tier')
        site_set = published.get(gid, set())

        # --- tier agreement -------------------------------------------------
        seen = {'agent_state': state_tier, 'gap_evidence': evid_tier}
        if len(site_set) == 1:
            seen['site'] = list(site_set)[0]
        elif len(site_set) > 1:
            seen['site'] = 'AMBIGUOUS:' + '/'.join(sorted(site_set))
        copies = hardcoded.get(gid, [])
        for c in copies:
            seen['%s:%d' % (c['file'], c['line'])] = c['tier']

        distinct = {v for v in seen.values() if v}
        tier_ok = len(distinct) <= 1
        if not tier_ok:
            tier_defects.append({'gap_id': gid, 'name': name, 'tiers': seen,
                                 'hardcoded_copies': copies})

        # --- topic agreement ------------------------------------------------
        history = st.get('audit_history', []) or []
        recent = history[-RECENT_AUDITS:]
        text = ' '.join(json.dumps(a, ensure_ascii=False) for a in recent)
        want = set(tokens(name)) - common
        have = set(tokens(text))
        hits = sorted(want & have)
        share = (len(hits) / len(want)) if want else 1.0
        # No history = never audited: a different defect, reported by the
        # overdue-audit machinery, not by this gate.
        # No discriminative tokens = this gate cannot speak; say so, do not pass.
        topic_ok = share >= TOPIC_FLOOR or not history or not want

        if not topic_ok:
            topic_defects.append({
                'gap_id': gid,
                'name': name,
                'share': round(share, 2),
                'matched_terms': hits,
                'expected_terms': sorted(want),
                'dropped_as_common': sorted(set(tokens(name)) & common),
                'n_audits': len(history),
                'note': ('audit trail filed under this number does not discuss '
                         'what this number names on the site'),
            })

        rows[gid] = {
            'name': name,
            'tiers': seen,
            'tier_agree': tier_ok,
            'topic_share': round(share, 2),
            'topic_agree': topic_ok,
            # False where every word of the gap's name is shared with other
            # gaps (e.g. #9 "GKA in LADA"). Such a gap is not passing the
            # check - the check has nothing to measure. Recorded so a reader
            # does not mistake silence for a clean result.
            'topic_checkable': bool(want),
            'discriminative_terms': sorted(want),
            'n_audits': len(history),
            'last_audit': (history[-1].get('date') if history else None),
        }

    report = {
        'generated': __import__('datetime').date.today().isoformat(),
        'recent_audits_read': RECENT_AUDITS,
        'topic_floor': TOPIC_FLOOR,
        'gaps': rows,
        'tier_defects': tier_defects,
        'topic_defects': topic_defects,
        'annotated_misfiled_trails': sorted(
            (gid for gid, g in state.get('gaps', {}).items()
             if g.get('audit_trail_provenance')), key=lambda k: int(k)),
        'hardcoded_tier_copies': sum(len(v) for v in hardcoded.values()),
    }
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)

    print('  Gap numbering audit: %d gaps checked' % len(rows))
    if tier_defects:
        print('  %d gap(s) where the three stores do not agree on tier:'
              % len(tier_defects))
        for d in tier_defects:
            print('    #%-3s %s' % (d['gap_id'], d['name'][:44]))
            for k, v in d['tiers'].items():
                print('         %-46s %s' % (k, v))
    else:
        print('  [OK] tier agreement across memory, evidence store, site '
              'and every hardcoded copy')

    n_copies = sum(len(v) for v in hardcoded.values())
    print('  Tier is hardcoded in %d place(s) across %d gap(s); the store is '
          'read in none of them.'
          % (n_copies, len(hardcoded)))

    if topic_defects:
        print('  %d gap(s) whose audit trail answers a different question:'
              % len(topic_defects))
        for d in topic_defects:
            print('    #%-3s %-40s overlap %.0f%% (%d audits) matched=%s'
                  % (d['gap_id'], d['name'][:40], 100 * d['share'],
                     d['n_audits'], d['matched_terms'] or '-'))
    else:
        print('  [OK] every audit trail discusses the gap it is filed under')

    # A gap whose trail was misfiled for months and received ONE on-topic
    # audit today drops out of the window check immediately - the recent-3
    # window fills with correct audits and the gate falls silent while 20-odd
    # misfiled entries sit underneath. Observed the day this gate was written:
    # #7 and #12 cleared within hours of being flagged. So report the standing
    # annotation separately and permanently, independent of the window.
    annotated = sorted(
        (gid for gid, g in state.get('gaps', {}).items()
         if g.get('audit_trail_provenance')),
        key=lambda k: int(k))
    if annotated:
        print('  %d gap(s) carry a standing misfiled-trail annotation '
              '(history predates any recent correction): %s'
              % (len(annotated), ', '.join('#' + g for g in annotated)))
        print('    These do NOT clear by adding one on-topic audit. They clear')
        print('    when the historical trail is re-homed or archived.')

    unmeasurable = [g for g, r in rows.items() if not r['topic_checkable']]
    if unmeasurable:
        print('  %d gap(s) this check cannot speak on (name shares every word '
              'with other gaps): %s'
              % (len(unmeasurable), ', '.join('#' + g for g in
                                              sorted(unmeasurable, key=int))))

    if tier_defects or topic_defects:
        print('  REPORTED, NOT APPLIED. Re-homing an audit trail rewrites the')
        print('  audit record; which trail is authoritative is a human call.')
    print('  -> %s' % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
