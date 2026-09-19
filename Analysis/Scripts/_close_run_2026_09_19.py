#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close the 2026-09-19 run: state updates for the day's findings."""
import json, os, shutil
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, '..', 'Results', 'agent_state.json')
TODAY = str(date.today())

with open(STATE, encoding='utf-8') as f:
    s = json.load(f)
shutil.copy2(STATE, STATE + f'.bak_{TODAY}')

# ---- 1. New verified paper: FINE-ONE -------------------------------------
s['papers']['41780000'] = {
    'status': 'UNVETTED',
    'priority': 'HIGH',
    'added': TODAY,
    'title': 'Finerenone in Type 1 Diabetes and Chronic Kidney Disease.',
    'journal': 'N Engl J Med', 'year': '2026',
    'doi': '10.1056/NEJMoa2512854',
    'pub_types': ['Randomized Controlled Trial', 'Clinical Trial, Phase III',
                  'Multicenter Study'],
    'identity_verified': ('PubMed record fetched live 2026-09-19 via the repo\'s own '
                          'ingest_papers.fetch_abstracts_batch; title, journal, year, '
                          'DOI and publication types all read from that record.'),
    'why_ingested': ('FDA approved finerenone (Kerendia) for CKD associated with TYPE 1 '
                     'diabetes on 2026-09-16, the first new agent for that population in '
                     '30+ years. FINE-ONE is the single trial the approval rests on. '
                     'Nothing in the hub tracked finerenone before today.'),
    'do_not_overstate': ('Primary endpoint is relative change in UACR at 6 months - a '
                         'surrogate. It is NOT a hard-outcome trial: no eGFR-decline or '
                         'ESKD endpoint was met, because none was powered. Hyperkalaemia '
                         'was more frequent on finerenone. Any hub text must say '
                         '"reduced albuminuria over 6 months", never "protects kidneys" '
                         'or "prevents kidney failure".'),
}

# ---- 2. Audit notes ------------------------------------------------------
s.setdefault('audit_notes', []).append({
    'date': TODAY,
    'finding': ('TWO CATALOG ROWS RESTED ON PAPERS ABOUT SOMETHING ELSE, AND EVERY '
                'CITATION GATE HERE WAS CORRECTLY GREEN ON BOTH.'),
    'detail': [
        'build_generic_drug_catalog.py Spironolactone cited only PMID 33264825 = '
        '"Effect of Finerenone on Chronic Kidney Disease Outcomes in Type 2 Diabetes" '
        '(FIDELIO-DKD). That is finerenone: a different molecule, branded and '
        'on-patent, which fails this catalog\'s own off-patent inclusion rule. '
        'Spironolactone is not in the paper. Row graded MODERATE on it.',
        'build_generic_drug_catalog.py Minocycline cited PMID 25714673 = "Loss of '
        'survival factors and activation of inflammatory cascades in brain sympathetic '
        'centers in type 1 diabetic mice" - a mouse study, no minocycline, no clinical '
        'neuropathy trial - described in the catalog as "Hu et al. 2015 diabetic '
        'neuropathy" carrying the claim "MIND trial showed neuropathy improvement".',
        'WHY NOTHING CAUGHT THEM: every gate in this repo scores a PMID against the '
        'prose beside it. For Spironolactone the prose said "FIDELIO-DKD (Bakris et al. '
        '2020)", which is exactly what 33264825 IS - so title, author, journal and year '
        'gates were all right to pass. What disagreed was the SUBJECT OF THE RECORD.',
    ],
    'action': ('Both citations withdrawn in place with the defect stated on the page. '
               'Grades NOT changed unattended (2026-08-20 precedent). New gate '
               'audit_catalog_entity_agreement.py written, measured ABSENT 2 -> 0, '
               'shipped in --gate on live catches rather than a fixture.'),
    'residual': ('11 PMIDs this catalog publishes have never been ingested, so nothing '
                 'here has ever held text to check them against. That is a backlog, '
                 'not a pass.'),
})
s['audit_notes'].append({
    'date': TODAY,
    'finding': ('THE PAPER LIBRARY HELD 150 FULL TEXTS AND ITS INDEX RECORDED NONE OF '
                'THEM, FOR AT LEAST 33 DAYS.'),
    'measured': {
        'metadata.pmc_available': 174,
        'metadata.fulltext_fetched': 150,
        'records_with_pmcid_before': 1,
        'records_with_has_fulltext_before': 0,
        'records_total': 347,
        'fulltext_files_on_disk': 150,
        'records_with_pmcid_after': 134,
        'records_with_has_fulltext_after': 133,
    },
    'root_cause': ('PROVEN, not inferred: ingest_papers.convert_pmids_to_pmcids() '
                   'returns a map keyed by INT (the NCBI ID converter sends pmid as a '
                   'JSON number) while build_index() looks it up with a STR pmid. Every '
                   'per-paper lookup missed. Confirmed by calling the function directly '
                   'on 2026-09-19: {37026004: "PMC10070978", ...} - int keys. '
                   'fetch_all_fulltext() iterates the map directly, which is why the '
                   'DOWNLOADS always worked.'),
    'consequences': [
        'The published Paper Library dashboard showed "PMC Available: 174" above 347 '
        'rows of which not one said "Full Text". After repair: 133 rows do.',
        'The scheduled task\'s own vetting step says "if the paper has full text (check '
        'fulltext/ directory), scan for red flags". Driven off this index it evaluated '
        'False for all 347 papers, so full-text red-flag scanning has never run.',
        'The 2026-09-07 queue item about PMCID->PMID normalisation has the same single '
        'cause: PMC12211534 was carried four days as a novel find while already in '
        'corpus as PMID 40598585 - whose full text was on disk as PMC12211534.json.',
    ],
    'fixed': ['str() at both ends in ingest_papers.py',
              'repair_index_pmcid_map.py rebuilds the fields from fulltext/*.json '
              '(authoritative, local, no network) - applied',
              'Analysis/Results/pmcid_to_pmid.json now exists (150 entries) for intake '
              'normalisation; PMC12211534 -> 40598585 verified',
              'audit_index_field_invariants.py gates the invariant, proven in both '
              'directions'],
    'new_finding_from_the_repair': ('17 full texts on disk belong to PMIDs the index '
                                    'does not list at all, including 37026004 (FLAGGED '
                                    'as load-bearing for Gap #11), 38918878, 39428507 '
                                    'and 41827829. Held text, unindexed papers.'),
})

# ---- 3. Doctrine note ----------------------------------------------------
s.setdefault('doctrine_notes', {})[TODAY] = (
    'A citation gate that only compares a PMID to the words next to it cannot see a '
    'wrong-SUBJECT citation, because the words next to it were written from the same '
    'wrong paper. Both 2026-09-19 defects were internally consistent and externally '
    'false. The check that works asks a question neither the prose nor the PMID can '
    'answer alone: does the cited paper mention the thing this record is ABOUT. '
    'Second lesson, from the index bug: a summary count and the records it summarises '
    'are two independent assertions about the same fact, and this repository had never '
    'compared any pair of them. A lookup that silently misses produces well-formed '
    'empty fields and a confident metadata line, which is indistinguishable from '
    'success unless something checks the file against itself.'
)

# ---- 4. Queue surgery ----------------------------------------------------
q = s.setdefault('work_queue', [])
def resolve(pred, note):
    n = 0
    for it in q:
        if isinstance(it, dict) and pred(str(it.get('target') or '')):
            it['status'] = f'resolved_{TODAY}'
            it['resolution'] = note
            n += 1
    return n

n1 = resolve(lambda t: 'RESOLVE PMCID -> PMID AT INTAKE' in t,
             'Root cause found and fixed 2026-09-19 (int/str key mismatch in '
             'ingest_papers.convert_pmids_to_pmcids). pmcid_to_pmid.json (150 entries) '
             'now exists for pre-dedup normalisation; PMC12211534 -> 40598585 verified. '
             'watch_items_pending_pmid re-checked: all 8 already resolved, no further '
             'PMCID-shaped entries pending.')

for item in [
    {'type': 'user_action_required', 'priority': 1, 'added': TODAY,
     'target': ('RE-GRADE OR RE-EVIDENCE SPIRONOLACTONE. Its only citation was a '
                'FINERENONE trial (FIDELIO-DKD, PMID 33264825) and was withdrawn '
                '2026-09-19, so the row now publishes MODERATE with NO cited evidence '
                'and a visible [NO CITED EVIDENCE] marker. Grading is a human call '
                '(2026-08-20 precedent). Real spironolactone-in-DKD RCT evidence exists '
                'and was surfaced but NOT inserted, because neither PMID was verified: '
                'a low-dose 12.5 mg/day open-label multicentre RCT in T2D with '
                'albuminuria, J Clin Endocrinol Metab 2023;108(9):2203 (positive on '
                'UACR), and PRIORITY, Lancet Diabetes Endocrinol 2020 (NULL for '
                'preventing microalbuminuria). Ingest and identity-check both, then '
                'decide the grade on a positive surrogate trial plus a null prevention '
                'trial.')},
    {'type': 'fix_pipeline', 'priority': 1, 'added': TODAY,
     'target': ('INGEST THE 11 CATALOG PMIDS NOBODY HAS EVER CHECKED. '
                'audit_catalog_entity_agreement.py reports 11 UNCHECKABLE citations in '
                'build_generic_drug_catalog.py - PMIDs the dashboard publishes that are '
                'absent from the paper library, so no gate has ever held text to compare '
                'them against: 26651260 (Alpha-lipoic acid), 16873688 (Berberine), '
                '27241260 (Colchicine), 36125533 (Dapsone), 21782948 (Doxycycline), '
                '25669071 (Hydroxychloroquine), 28303409 (Methotrexate), 24497205 '
                '(Minocycline - now this row\'s ONLY citation), 8805029 (Nicotinamide), '
                '19402055 (Pioglitazone), 36060506 (Verapamil), 25205139 (Vitamin D). '
                'Start with 24497205: the Minocycline row rests on it alone and the '
                'claim it used to carry ("MIND trial showed neuropathy improvement") is '
                'currently suspended. The real MIND study appears to be Syngle et al., '
                'Neurol Sci 2014; whether 24497205 IS that paper is NOT established.')},
    {'type': 'fix_pipeline', 'priority': 1, 'added': TODAY,
     'target': ('INDEX THE 17 PAPERS WHOSE FULL TEXT IS ALREADY ON DISK. The 2026-09-19 '
                'pmcid repair found 17 fulltext/*.json files whose PMID appears nowhere '
                'in index.json - the repository holds their full text and does not list '
                'the paper. Includes 37026004 (FLAGGED, load-bearing for the Gap #11 '
                'hypothesis), 38918878, 39428507, 41827829, 37467726, 37544201, '
                '30078372, 22723585. audit_index_field_invariants.py reports this as '
                'I3-NOTE (not a failure) because it is an ingestion question. Resolve by '
                'running ingest/reconcile now that the pmcid map is correct, then '
                'confirm I3 closes.')},
    {'type': 'analysis', 'priority': 1, 'added': TODAY,
     'target': ('VET PMID 41780000 (FINE-ONE) AND DECIDE WHERE FINERENONE BELONGS. FDA '
                'approved finerenone for CKD in TYPE 1 diabetes on 2026-09-16 - first '
                'new agent for that population in 30+ years - and the hub tracked '
                'nothing about it until 2026-09-19. Three specific jobs: (i) vet the '
                'paper; the primary endpoint is a 6-month UACR surrogate, not a hard '
                'outcome, and hyperkalaemia was more frequent, so guard against any hub '
                'text saying "protects kidneys"; (ii) finerenone is BRANDED and '
                'ON-PATENT, so it must NOT enter the generic/off-patent catalog - the '
                'row it wrongly propped up (Spironolactone) is the steroidal MRA that '
                'IS generic, and the distinction is now load-bearing; (iii) check '
                'whether the NLRP3 / diabetic-kidney paths and any MRA-adjacent gap '
                'need updating, since a new approved comparator changes what counts as '
                'an unmet need.')},
    {'type': 'fix_pipeline', 'priority': 2, 'added': TODAY,
     'target': ('EXTEND THE ENTITY-AGREEMENT TEST BEYOND ONE FILE. '
                'audit_catalog_entity_agreement.py found parseable subject+citation '
                'records in exactly ONE builder (build_generic_drug_catalog.py, 20 '
                'rows). build_drug_repurposing_screen.py (34 drugs), '
                'build_drug_repurposing_islet.py and build_gka_landscape.py hold the '
                'same KIND of record but assemble it in a shape the AST walk does not '
                'reach - so the gate\'s green line covers far less than it appears to. '
                'Measure the reach first (print records_skipped per file), then widen '
                'it. A gate with unstated reach was the 2026-09-08 finding, restated.')},
    {'type': 'verify_citations', 'priority': 2, 'added': TODAY,
     'target': ('GROW external_pmid_titles.json OR STOP CITING UNINGESTED PAPERS. The '
                'cache created 2026-09-19 holds ONE entry and it exists only because '
                'the minocycline defect was invisible without it. Every UNCHECKABLE '
                'verdict in the entity gate is a citation this repository publishes and '
                'cannot check. Either ingest the paper or record its verified title. '
                'Model memory is not an allowed source for that file.')},
]:
    q.append(item)

# ---- 5. Run history ------------------------------------------------------
s['run_history'].append({
    'date': TODAY,
    'summary': ('THE REPOSITORY HELD 150 FULL TEXTS AND ITS OWN INDEX SAID IT HELD '
                'NONE, AND TWO DRUG ROWS WERE GRADED ON PAPERS ABOUT OTHER DRUGS. '
                'Neither had anything to do with the other, and both were invisible to '
                'all 70+ green stages for the same structural reason: every gate here '
                'checks the CONTENT of an assertion against the words beside it. A '
                'wrong-SUBJECT citation is internally consistent (the prose was written '
                'from the wrong paper, so it matches it perfectly), and a silent lookup '
                'miss is internally consistent too (well-formed empty fields under a '
                'confident metadata line). Fixed both, and shipped the two gates that '
                'ask the questions the others structurally cannot: does the cited paper '
                'mention the thing the record is ABOUT, and does a summary count agree '
                'with the records it summarises. Both proven in both directions on live '
                'data, not fixtures. Also ingested FINE-ONE (PMID 41780000, identity '
                'verified live): the FDA approved finerenone for CKD in TYPE 1 diabetes '
                'on 2026-09-16 and this hub tracked no finerenone at all - while '
                'simultaneously citing a finerenone trial as its spironolactone '
                'evidence.'),
    'gates_added': ['audit_catalog_entity_agreement.py (--gate)',
                    'audit_index_field_invariants.py (--gate)'],
    'measured': {'catalog_ABSENT': '2 -> 0',
                 'index_records_with_fulltext': '0 -> 133',
                 'index_records_with_pmcid': '1 -> 134',
                 'paper_library_dashboard_fulltext_rows': '0 -> 133'},
    'papers_added': ['41780000'],
    'queue_items_resolved': n1,
    'queue_items_added': 6,
})
s['last_run'] = TODAY
s['last_updated'] = TODAY

with open(STATE, 'w', encoding='utf-8') as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
print(f'state written. papers={len(s["papers"])} queue={len(s["work_queue"])} '
      f'resolved_pmcid_items={n1}')
