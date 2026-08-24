#!/usr/bin/env python3
"""Repair the 9 builder citation records that named the wrong paper (2026-08-24).

FINDING
-------
audit_builder_title_agreement.py found 9 of the 11 builder citation records that
carry BOTH a pmid and a title assert a title that is not the title of that PMID.
All 9 render into published dashboards:

  Drug_Repurposing_Islet.html   6 records, 4 of them tagged evidence_tier GOLD
  LADA_Natural_History.html     3 records + 1 WEAK

The worst example: PMID 19148081, published as "Edmonton Protocol: allogeneic
islet transplantation... Shapiro et al., NEJM 2006, GOLD", is actually "Your
inbox, Mr President." -- a Nature editorial.

REPAIR POLICY
-------------
1. Where the paper the builder DESCRIBES could be located in PubMed by live
   search, the PMID is replaced AND the stored title/authors/year/journal are
   overwritten with the values PubMed returns. The builder's paraphrase is
   discarded. A stored paraphrase is exactly what let these records drift, so
   the repair removes the ability to drift rather than re-stating it correctly.
2. Where the described paper could NOT be located, the record is NOT given a
   guessed PMID. It is marked unresolved: pmid emptied, evidence_tier demoted to
   UNSOURCED, and the title prefixed so the dashboard reader sees the status.
   Three records fall here; the underlying claims may be true, but this repo has
   no citation for them and will not manufacture one.

VERIFICATION NOTE
-----------------
While resolving these, the first candidate PMID recalled from memory for
UKPDS 25 (9400508) turned out to be a soft-tissue sarcoma meta-analysis. Every
replacement below was resolved by live PubMed query and confirmed against the
returned title, journal, year and author list. None was recalled.

Idempotent: re-running after a successful repair is a no-op.
"""

import io
import json
import os
import re
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(BASE, 'Scripts')
RESULTS = os.path.join(BASE, 'Results')
LOG = os.path.join(RESULTS, 'builder_citation_repairs_20260824.json')

# --- REPLACEMENTS -------------------------------------------------------
# Every field below is the value PubMed esummary returned on 2026-08-24.
REPLACE = {
    '22723585': {
        'pmid': '17429083',
        'title': 'Interleukin-1-receptor antagonist in type 2 diabetes mellitus.',
        'authors': 'Larsen CM, et al.',
        'year': 2007,
        'journal': 'N Engl J Med',
        'described_as': 'IL-1 receptor antagonist in type 2 diabetes and beta '
                        'cell preservation (Larsen, NEJM)',
        'why': 'Builder asserted NEJM 2012; the anakinra T2D NEJM paper is '
               '2007. 22723585 is a fructose/glycemic-control systematic '
               'review in Diabetes Care.',
    },
    '24931610': {
        'pmid': '22442301',
        'title': 'Preventing beta-cell loss and diabetes with calcium channel blockers.',
        'authors': 'Xu G, Chen J, Jing G, Shalev A',
        'year': 2012,
        'journal': 'Diabetes',
        'described_as': 'Verapamil blocks TXNIP and protects beta cells from '
                        'apoptosis (Shalev)',
        'why': 'Builder asserted Cell Metabolism 2014; the Shalev TXNIP/CCB '
               'beta-cell paper is Diabetes 2012. 24931610 is a SETD2 histone '
               'methylation paper in Cell Reports.',
    },
    '19148081': {
        'pmid': '17005949',
        'title': 'International trial of the Edmonton protocol for islet transplantation.',
        'authors': 'Shapiro AM, et al.',
        'year': 2006,
        'journal': 'N Engl J Med',
        'described_as': 'Edmonton Protocol international trial (Shapiro, NEJM 2006)',
        'why': '19148081 is "Your inbox, Mr President.", a Nature 2009 '
               'editorial. Published on the site as GOLD-tier evidence.',
    },
    '31529065': {
        'pmid': '32307525',
        'title': 'Decline Pattern of Beta-cell Function in Adult-onset Latent '
                 'Autoimmune Diabetes: an 8-year Prospective Study.',
        'authors': 'Li X, Chen Y, Xie Y, Xiang Y, et al.',
        'year': 2020,
        'journal': 'J Clin Endocrinol Metab',
        'described_as': 'Biphasic C-peptide decline in Chinese LADA cohort (2020)',
        'why': '31529065 is a mobile-app psychosocial study in JAMIA. The '
               'described study is the Central South University 8-year LADA '
               'beta-cell decline cohort. Builder had named Zhou as first '
               'author; PubMed lists Li X first, so authors are corrected too.',
    },
    '9742976': {
        'pmid': '9357409',
        'title': 'UKPDS 25: autoantibodies to islet-cell cytoplasm and glutamic '
                 'acid decarboxylase for prediction of insulin requirement in '
                 'type 2 diabetes.',
        'authors': 'Turner R, Stratton I, Horton V, et al.',
        'year': 1997,
        'journal': 'Lancet',
        'described_as': 'UKPDS: 84% GADA+ patients require insulin by 6 years',
        'why': '9742976 is UKPDS 33 (intensive glucose control), which contains '
               'no autoantibody prediction result. The GADA/ICA insulin-'
               'requirement finding is UKPDS 25.',
    },
    '30369313': {
        'pmid': '34318969',
        'title': 'Low C-peptide together with a high glutamic acid decarboxylase '
                 'autoantibody level predicts progression to insulin dependence '
                 'in latent autoimmune diabetes in adults.',
        'authors': 'Sorgjerd EP, Asvold BO, Grill V',
        'year': 2021,
        'journal': 'Diabetes Obes Metab',
        'described_as': 'HUNT study autoantibody risk stratification; HR 6.40 '
                        'low C-peptide, HR 5.37 high GADA titre',
        'why': '30369313 is a cardiac resynchronisation therapy outcomes paper '
               'in JAHA. Sorgjerd/Asvold are the HUNT (Nord-Trondelag) group '
               'and this is the paper carrying the C-peptide/GADA hazard '
               'ratios the record cites.',
    },
    '23835333': {
        'pmid': '23248199',
        'title': 'Adult-onset autoimmune diabetes in Europe is prevalent with a '
                 'broad clinical phenotype: Action LADA 7.',
        'authors': 'Hawa MI, Kolb H, Schloot N, et al.',
        'year': 2013,
        'journal': 'Diabetes Care',
        'described_as': 'ACTION LADA: clinical and genetic characteristics of '
                        'LADA (Hawa, Diabetes Care 2013)',
        'why': '23835333 is the teplizumab anti-CD3 C-peptide paper in '
               'Diabetes - a real diabetes paper, which is why the topic '
               'screen passed it and only title agreement caught it.',
    },
}

# --- UNRESOLVED ---------------------------------------------------------
UNRESOLVED = {
    '28864502': {
        'described_as': 'GLP-1 receptor agonists enhance islet graft function '
                        'in rodent transplant models (Markmann, Transplantation 2017)',
        'why': '28864502 is a sulfonylurea cardiovascular-risk paper in '
               'Diabetes Care. Searches for Markmann islet 2017 and for '
               'GLP-1/islet-transplantation/graft-function returned no paper '
               'matching this description. No substitute is asserted.',
    },
    '15644441': {
        'described_as': 'Etanercept and instant blood-mediated inflammatory '
                        'reaction in islet transplantation (Bennet, Transplantation 2005)',
        'why': '15644441 is a placental syncytin gene paper in PNAS. Bennet\'s '
               'IBMIR paper is Ups J Med Sci 2000 (11095109) and concerns no '
               'etanercept; the etanercept islet trial found is a 2023 pilot '
               '(36443174). Neither is the asserted paper.',
    },
    '16498215': {
        'described_as': 'Instant blood-mediated inflammatory reaction in islet '
                        'transplantation: mechanisms and mitigation (Nilsson, '
                        'Transplantation Reviews 2006)',
        'why': '16498215 is a rabbit calvarial bone transport paper in '
               'Neurol Med Chir. No 2006 Nilsson IBMIR review was located; the '
               'nearest is Curr Opin Organ Transplant 2011 (21971510), which is '
               'a different paper.',
    },
}

FIELD_RE = {
    'title': re.compile(r'(["\']title["\']\s*:\s*)(["\'])(.*?)(\2)', re.S),
    'authors': re.compile(r'(["\']authors["\']\s*:\s*)(["\'])(.*?)(\2)', re.S),
    'journal': re.compile(r'(["\']journal["\']\s*:\s*)(["\'])(.*?)(\2)', re.S),
    'year': re.compile(r'(["\']year["\']\s*:\s*)(\d{4})'),
    'tier': re.compile(r'(["\'](?:evidence_tier|evidence_level)["\']\s*:\s*)'
                       r'(["\'])(.*?)(\2)', re.S),
}


def find_record_span(text, pmid):
    """Character span of the dict literal containing this pmid literal."""
    m = re.search(r'["\']pmid["\']\s*:\s*["\']%s["\']' % pmid, text)
    if not m:
        return None
    start = text.rfind('{', 0, m.start())
    depth, i = 0, start
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return start, i + 1
        i += 1
    return None


def set_field(block, field, value, quote_style="'"):
    rx = FIELD_RE[field]
    if field == 'year':
        if rx.search(block):
            return rx.sub(lambda m: m.group(1) + str(value), block, count=1)
        return block
    if not rx.search(block):
        return block
    safe = str(value).replace('"', "'")
    return rx.sub(lambda m: '%s%s%s%s' % (m.group(1), m.group(2), safe,
                                          m.group(4)), block, count=1)


WITHDRAWN_MARKER = ('citation withdrawn 2026-08-24 - asserted PMID named a '
                    'different paper and no verified source was located')


def repair_file(path, log):
    # newline='' preserves CRLF. The first attempt at this repair rewrote both
    # files LF-only, which turned a 10-line change into a 1133-line diff and
    # would have buried the actual repair in review.
    with io.open(path, encoding='utf-8', newline='') as fh:
        text = fh.read()
    original = text
    name = os.path.basename(path)

    for bad, new in REPLACE.items():
        span = find_record_span(text, bad)
        if not span:
            continue
        block = text[span[0]:span[1]]
        block = block.replace('"%s"' % bad, '"%s"' % new['pmid'])
        block = block.replace("'%s'" % bad, "'%s'" % new['pmid'])
        block = set_field(block, 'title', new['title'])
        block = set_field(block, 'authors', new['authors'])
        block = set_field(block, 'journal', new['journal'])
        block = set_field(block, 'year', new['year'])
        text = text[:span[0]] + block + text[span[1]:]
        # The structured record is only one of the places the PMID appears.
        # These builders also print it inside HTML template prose
        # ("PMID:22723585 shows IL-1 blockade preserves beta cells...") and in
        # `"reference": "PMID:..."` on unrelated drug records. Repairing the
        # dict alone is the 2026-08-20 mistake: the field gets fixed and the
        # prose keeps asserting the wrong paper.
        remaining = text.count(bad)
        if remaining:
            text = text.replace(bad, new['pmid'])
        log.append({'file': name, 'action': 'REPLACE', 'was': bad,
                    'now': new['pmid'], 'verified_title': new['title'],
                    'described_as': new['described_as'], 'why': new['why'],
                    'other_occurrences_rewritten': remaining})

    for bad, info in UNRESOLVED.items():
        span = find_record_span(text, bad)
        if not span:
            continue
        block = text[span[0]:span[1]]
        block = block.replace('"%s"' % bad, '""').replace("'%s'" % bad, "''")
        block = set_field(block, 'title',
                          'UNSOURCED - citation withdrawn 2026-08-24: %s'
                          % info['described_as'])
        block = set_field(block, 'authors', 'not established')
        block = set_field(block, 'tier', 'UNSOURCED')
        text = text[:span[0]] + block + text[span[1]:]
        # Same reasoning as above, inverted: every surviving mention becomes an
        # explicit withdrawal so a reader never sees a bare wrong PMID.
        remaining = text.count('PMID:%s' % bad) + text.count(bad)
        text = text.replace('PMID:%s' % bad, WITHDRAWN_MARKER)
        text = text.replace(bad, WITHDRAWN_MARKER)
        log.append({'file': name, 'action': 'WITHDRAW', 'was': bad,
                    'now': None, 'described_as': info['described_as'],
                    'why': info['why'],
                    'other_occurrences_rewritten': remaining})

    if text != original:
        with io.open(path, 'w', encoding='utf-8', newline='') as fh:
            fh.write(text)
        return True
    return False


def main():
    log = []
    changed = []
    for name in ('build_drug_repurposing_islet.py', 'build_lada_model.py'):
        path = os.path.join(SCRIPTS, name)
        if not os.path.exists(path):
            print('  [WARN] missing %s' % name)
            continue
        if repair_file(path, log):
            changed.append(name)

    if not log:
        print('[OK] nothing to repair - already clean')
        return 0

    print('Repaired %d citation record(s) in %d file(s):'
          % (len(log), len(changed)))
    for entry in log:
        print('  %-8s %-34s %s -> %s'
              % (entry['action'], entry['file'], entry['was'],
                 entry['now'] or 'WITHDRAWN'))

    payload = {'date': '2026-08-24',
               'found_by': 'audit_builder_title_agreement.py',
               'files_changed': changed,
               'repairs': log}
    with io.open(LOG, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(payload, indent=1, ensure_ascii=False))
    print('\nLog: %s' % LOG)
    print('[OK]')
    return 0


if __name__ == '__main__':
    sys.exit(main())
