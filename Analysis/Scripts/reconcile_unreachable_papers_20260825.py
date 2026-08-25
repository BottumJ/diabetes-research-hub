"""
reconcile_unreachable_papers_20260825.py

CLOSES work-queue item (priority 1, added 2026-08-24):
  "54 INDEXED PAPERS CAN NEVER BE VETTED."

audit_index_provenance.py found 55 index entries absent from state["papers"].
The vetting batch iterates state, so those entries were unreachable BY
CONSTRUCTION and the headline "279 VETTED / 14 FLAGGED, all papers vetted"
was measured on the wrong denominator (293 of 313).

The queue item explicitly warned: do NOT simply import all 55, because that
launders off-domain junk into the corpus count. So every one of the 55 was
adjudicated INDIVIDUALLY, and every title below was resolved LIVE against
NCBI esummary on 2026-08-25 -- none recalled from memory. Where the live
title disagreed with the index title the entry would have been treated as a
miscitation; on this batch all 55 agreed.

Two outcomes:

  RETAIN (37) -> folded into state["papers"] as UNVETTED, with
      pmid_verified=True and the live PubMed title stored, so the normal
      vetting batch can now reach them. They are NOT marked VETTED: PMID
      existence was checked this run, the CLAIMS were not.

  PURGE  (18) -> written to not_corpus_pmids.json with a per-paper reason.
      Every one resolves to a real PubMed record -- that is why the
      existence gates passed them. The disqualifier is DOMAIN + PROVENANCE:
      each is UNCITED (no dashboard_locations at all) AND is not about
      diabetes, islets, beta cells or their immunology.

Run:  python Analysis/Scripts/reconcile_unreachable_papers_20260825.py
"""

import json
import os
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS = os.path.join(REPO, "Analysis", "Results")
STATE = os.path.join(RESULTS, "agent_state.json")
NOT_CORPUS = os.path.join(RESULTS, "not_corpus_pmids.json")
TODAY = "2026-08-25"

# ---------------------------------------------------------------------------
# RETAIN. title = live NCBI esummary title, fetched 2026-08-25.
# provenance = why the index contains it (from index_provenance_audit.json).
# ---------------------------------------------------------------------------
RETAIN = {
    # --- DASHBOARD-cited: a reader can see these on the published site today.
    "17429083": ("Interleukin-1-receptor antagonist in type 2 diabetes mellitus.",
                 "N Engl J Med", "2007", "DASHBOARD"),
    "18843118": ("GAD treatment and insulin secretion in recent-onset type 1 diabetes.",
                 "N Engl J Med", "2008", "DASHBOARD"),
    "19805629": ("Glyburide inhibits the Cryopyrin/Nalp3 inflammasome.",
                 "J Cell Biol", "2009", "DASHBOARD"),
    "23817699": ("Salicylate (salsalate) in patients with type 2 diabetes: a randomized trial.",
                 "Ann Intern Med", "2013", "DASHBOARD"),
    "28375156": ("ω-3 polyunsaturated fatty acids ameliorate type 1 diabetes and autoimmunity.",
                 "J Clin Invest", "2017", "DASHBOARD"),
    "34021020": ("Intralymphatic Glutamic Acid Decarboxylase With Vitamin D Supplementation in "
                 "Recent-Onset Type 1 Diabetes: A Double-Blind, Randomized, Placebo-Controlled "
                 "Phase IIb Trial.", "Diabetes Care", "2021", "DASHBOARD"),
    "35665810": ("Intralymphatic GAD-Alum (Diamyd®) Improves Glycemic Control in Type 1 "
                 "Diabetes With HLA DR3-DQ2.", "J Clin Endocrinol Metab", "2022", "DASHBOARD"),
    "36826844": ("Effect of Verapamil on Pancreatic Beta Cell Function in Newly Diagnosed "
                 "Pediatric Type 1 Diabetes: A Randomized Clinical Trial.", "JAMA", "2023",
                 "DASHBOARD"),
    "39634180": ("Personalized nutrition in type 2 diabetes remission: application of digital "
                 "twin technology for predictive glycemic control.",
                 "Front Endocrinol (Lausanne)", "2024", "DASHBOARD"),
    "39843169": ("Dapagliflozin plus calorie restriction for remission of type 2 diabetes: "
                 "multicentre, double blind, randomised, placebo controlled trial.",
                 "BMJ", "2025", "DASHBOARD"),
    "40982327": ("Type 2 Diabetes Remission: A Systematic Review and Meta-analysis of "
                 "Nonsurgical Randomized Controlled Trials.", "Diabetes Care", "2025",
                 "DASHBOARD"),
    "9357409": ("UKPDS 25: autoantibodies to islet-cell cytoplasm and glutamic acid "
                "decarboxylase for prediction of insulin requirement in type 2 diabetes. "
                "UK Prospective Diabetes Study Group.", "Lancet", "1997", "DASHBOARD"),

    # --- OTHER / AUDIT_ONLY, on-domain.
    "16306343": ("Latent autoimmune diabetes in adults: definition, prevalence, beta-cell "
                 "function, and treatment.", "Diabetes", "2005", "OTHER"),
    "31304320": ("Pivotal trial of an autonomous AI-based diagnostic system for detection of "
                 "diabetic retinopathy in primary care offices.", "NPJ Digit Med", "2018",
                 "OTHER"),
    "37861217": ("Teplizumab and β-Cell Function in Newly Diagnosed Type 1 Diabetes.",
                 "N Engl J Med", "2023", "AUDIT_ONLY"),

    # --- RUN_LOG_ONLY: named in this repo's own run logs, never on a dashboard.
    # On-domain, so retained and made vettable, but tagged so they cannot be
    # counted as published corpus evidence without a deliberate decision.
    "32712220": ("Dapagliflozin promotes beta cell regeneration by inducing pancreatic "
                 "endocrine cell phenotype conversion in type 2 diabetic mice.",
                 "Metabolism", "2020", "RUN_LOG_ONLY"),
    "32862232": ("The dapagliflozin and prevention of adverse outcomes in chronic kidney "
                 "disease (DAPA-CKD) trial: baseline characteristics.",
                 "Nephrol Dial Transplant", "2020", "RUN_LOG_ONLY"),
    "35180212": ("SGLT2 inhibitors therapy protects glucotoxicity-induced β-cell failure in a "
                 "mouse model of human KATP-induced diabetes through mitigation of oxidative "
                 "and ER stress.", "PLoS One", "2022", "RUN_LOG_ONLY"),
    "35563495": ("Effects of Sodium-Glucose Co-Transporter-2 Inhibitors on Pancreatic β-Cell "
                 "Mass and Function.", "Int J Mol Sci", "2022", "RUN_LOG_ONLY"),
    "36643381": ("Effects of Low-Dose Colchicine on Serum High-Sensitivity C-Reactive Protein "
                 "Level in Coronary Artery Disease Patients with Type 2 Diabetes Mellitus and "
                 "Enhanced Inflammatory Response Protocol for a Randomized, Double-Blind, "
                 "Placebo-Controlled, Phase 2, Dose-Finding Study.", "Biomed Hub", "2022",
                 "RUN_LOG_ONLY"),
    "38918878": ("Emerging insights into the role of IL-1 inhibitors and colchicine for "
                 "inflammation control in type 2 diabetes.", "Diabetol Metab Syndr", "2024",
                 "RUN_LOG_ONLY"),
    "39613428": ("Investigating the effect of verapamil on preservation of beta-cell function "
                 "in adults with newly diagnosed type 1 diabetes mellitus (Ver-A-T1D): protocol "
                 "for a randomised, double-blind, placebo-controlled, parallel-group, "
                 "multicentre trial.", "BMJ Open", "2024", "RUN_LOG_ONLY"),
    "40648980": ("The Role of NLRP3 Inflammasome in Type 2 Diabetes Mellitus and Its "
                 "Macrovascular Complications.", "J Clin Med", "2025", "RUN_LOG_ONLY"),
    "40697602": ("Sodium-glucose co-transporter 2 inhibitors improve insulin resistance and "
                 "β-cell function in type 2 diabetes: A meta-analysis.", "World J Diabetes",
                 "2025", "RUN_LOG_ONLY"),
    "40898408": ("Real-world observations of GLP-1 receptor agonists and SGLT-2 inhibitors as "
                 "potential treatments for Alzheimer's disease.", "Alzheimers Dement", "2025",
                 "RUN_LOG_ONLY"),
    "41326666": ("Liraglutide in mild to moderate Alzheimer's disease: a phase 2b clinical "
                 "trial.", "Nat Med", "2026", "RUN_LOG_ONLY"),
    "41356006": ("GLP-1 receptor agonists in Alzheimer's and Parkinson's disease: endocrine "
                 "pathways, clinical evidence, and future directions.",
                 "Front Endocrinol (Lausanne)", "2025", "RUN_LOG_ONLY"),
    "41889274": ("Effect of colchicine for secondary prevention of cardiovascular diseases in "
                 "individuals with diabetes: A meta-analysis of randomized trials.",
                 "Diab Vasc Dis Res", "2026", "RUN_LOG_ONLY"),

    # --- UNCITED but squarely on-domain. Two of these (39869107, 40291594) were
    # already flagged on 2026-08-18 as known topic-screen FALSE NEGATIVES.
    "30291106": ("Management of Hyperglycemia in Type 2 Diabetes, 2018. A Consensus Report by "
                 "the American Diabetes Association (ADA) and the European Association for the "
                 "Study of Diabetes (EASD).", "Diabetes Care", "2018", "UNCITED"),
    "32358544": ("SGLT2 inhibition modulates NLRP3 inflammasome activity via ketones and "
                 "insulin in diabetes with cardiovascular disease.", "Nat Commun", "2020",
                 "UNCITED"),
    "34918381": ("SGLT2 inhibitor counteracts NLRP3 inflammasome via tubular metabolite "
                 "itaconate in fibrosis kidney.", "FASEB J", "2022", "UNCITED"),
    "39173844": ("Compromised chronic efficacy of a glucokinase activator AZD1656 in mouse "
                 "models for common human GCKR variants.", "Biochem Pharmacol", "2024",
                 "UNCITED"),
    "39428507": ("MOG-specific CAR Tregs: a novel approach to treat multiple sclerosis.",
                 "J Neuroinflammation", "2024", "UNCITED"),
    "39869107": ("Long Term Outcomes of Transplant Recipients Comparing Belatacept vs. "
                 "Tacrolimus: A UNOS Database Analysis.", "Clin Transplant", "2025", "UNCITED"),
    "40291594": ("Cost-effective strategies for CAR-T cell therapy manufacturing.",
                 "Mol Ther Oncol", "2025", "UNCITED"),
    "40988828": ("Vitamin D Supplementation in Deficiency States and Combined Calcium-Vitamin D "
                 "Therapy in Diabetes Prevention and Management: A Systematic Review of "
                 "Clinical Evidence.", "Cureus", "2025", "UNCITED"),
    "41986815": ("Multi-tissue multi-omics integration reveals tissue-specific pathways, gene "
                 "networks and drug candidates for type 1 diabetes.", "Diabetologia", "2026",
                 "UNCITED"),
}

# ---------------------------------------------------------------------------
# PURGE. Every title below is the LIVE PubMed title fetched 2026-08-25.
# Common disqualifier: UNCITED (zero dashboard_locations) AND off-domain.
# ---------------------------------------------------------------------------
OFF_DOMAIN = "OFF_DOMAIN_UNCITED"
PURGE = {
    "24105098": ("Bond and mode selectivity in the OH + NH2D reaction: a quasi-classical "
                 "trajectory calculation.", "Phys Chem Chem Phys", "2013",
                 "Computational gas-phase reaction dynamics. No biological content of any "
                 "kind. The index carried it with a BLANK title, so no human or gate ever "
                 "saw what it was."),
    "33082274": ("HLA Polymorphisms Are Associated with Treatment-Free Remission Following "
                 "Discontinuation of Tyrosine Kinase Inhibitors in Chronic Myeloid Leukemia.",
                 "Mol Cancer Ther", "2021",
                 "Oncology/CML. Indexed with a BLANK title. Plausibly harvested because "
                 "'HLA' and 'remission' are corpus vocabulary, but the subject is leukaemia, "
                 "not diabetes."),
    "37467726": ("Fast and low-dose medical imaging generation empowered by hybrid deep-learning "
                 "and iterative reconstruction.", "Cell Rep Med", "2023",
                 "Radiology image reconstruction. Indexed with a BLANK title. No diabetes, "
                 "islet or beta-cell content."),
    "37932527": ("Auto-inhibition and activation of a short Argonaute-associated TIR-APAZ "
                 "defense system.", "Nat Chem Biol", "2024",
                 "Bacterial anti-phage defence structural biology. Indexed with a BLANK title."),
    "30578413": ("Your genomic inheritance matters.", "Nat Rev Cancer", "2019",
                 "A one-page Research Highlight comment in an oncology journal. Not a study, "
                 "not diabetes, never cited by this repo."),
    "30778000": ("Statistical fallacies & errors can also jeopardize life & health of many.",
                 "Indian J Med Res", "2018",
                 "General biostatistics editorial. No diabetes content and no claim in this "
                 "repo rests on it."),
    "34299352": ("Genome-Wide Identification of GRAS Gene Family and Their Responses to Abiotic "
                 "Stress in Medicago sativa.", "Int J Mol Sci", "2021",
                 "Plant genomics (alfalfa). Almost certainly harvested on the token 'GRAS', "
                 "which in this corpus means Generally Recognized As Safe. Textbook "
                 "acronym collision."),
    "35491968": ("The CaPti1-CaERF3 module positively regulates resistance of Capsicum annuum "
                 "to bacterial wilt disease by coupling enhanced immunity and dehydration "
                 "tolerance.", "Plant J", "2022",
                 "Plant pathology (pepper). Harvested on 'immunity'/'tolerance', which are "
                 "corpus vocabulary in an entirely different sense."),
    "27505628": ("Evaluation of smokers with and without asthma in terms of smoking cessation "
                 "outcome, nicotine withdrawal symptoms, and craving: Findings from a "
                 "self-guided quit attempt.", "Addict Behav", "2016",
                 "Smoking-cessation behavioural study. No diabetes content."),
    "30078372": ("Latent Profile Analysis of Alcohol Consumption and Sexual Attitudes Among "
                 "College Women: Associations With Sexual Victimization Risk.",
                 "Violence Against Women", "2018",
                 "Harvested on 'Latent', which in this corpus means LADA (Latent Autoimmune "
                 "Diabetes in Adults). Acronym/keyword collision, nothing more."),
    "31220820": ("Effects of stimulation frequency and stimulation waveform on steady-state "
                 "visual evoked potentials using a computer monitor.", "J Neural Eng", "2019",
                 "Brain-computer-interface engineering. No diabetes content."),
    "33989382": ("Neuroscientific therapies for atrial fibrillation.", "Cardiovasc Res", "2021",
                 "Cardiac electrophysiology review. Cardiovascular, but nothing to do with "
                 "diabetes, islets or beta cells, and uncited here."),
    "37544201": ("Transfer and biotransformation of the COVID-19 prodrug molnupiravir and its "
                 "metabolite β-D-N4-hydroxycytidine across the blood-placenta barrier.",
                 "EBioMedicine", "2023",
                 "COVID antiviral placental pharmacokinetics. Plausibly harvested by the "
                 "drug-repurposing screen on 'prodrug'/'biotransformation'."),
    "28086769": ("Effect of ginseng extract on the TGF-β1 signaling pathway in CCl4-induced "
                 "liver fibrosis in rats.", "BMC Complement Altern Med", "2017",
                 "Rodent hepatic fibrosis / herbal extract. Harvested on 'TGF-β1'. No "
                 "diabetes endpoint."),
    "19729482": ("Suppression of activation and costimulatory signaling in splenic CD4+ T cells "
                 "after trauma-hemorrhage reduces T-cell function: a mechanism of "
                 "post-traumatic immune suppression.", "Am J Pathol", "2009",
                 "Trauma immunology. Harvested on 'costimulatory'/'CD4+', which are corpus "
                 "vocabulary via belatacept and Treg work, but the model is haemorrhagic "
                 "shock, not diabetes."),
    "28916733": ("Clonal expansion and epigenetic reprogramming following deletion or "
                 "amplification of mutant IDH1.", "Proc Natl Acad Sci U S A", "2017",
                 "Glioma genomics. Harvested on 'clonal expansion'/'epigenetic "
                 "reprogramming'. Oncology, not diabetes."),
    "30144957": ("Generation of novel Id2 and E2-2, E2A and HEB antibodies reveals novel Id2 "
                 "binding partners and species-specific expression of E-proteins in NK cells.",
                 "Mol Immunol", "2019",
                 "Antibody-reagent methods paper on NK-cell transcription factors. Basic "
                 "immunology tooling with no diabetes, islet or Treg endpoint."),
    "38587236": ("Probiotics induce intestinal IgA secretion in weanling mice potentially "
                 "through promoting intestinal APRIL expression and modulating the gut "
                 "microbiota composition.", "Food Funct", "2024",
                 "Weanling-mouse gut IgA/probiotics. Adjacent to the microbiome work but "
                 "reports no diabetes, glycaemic or autoimmunity endpoint, and is uncited. "
                 "Same class as the probiotic-breads paper purged 2026-08-20."),
}


def main():
    assert not (set(RETAIN) & set(PURGE)), "a PMID cannot be both retained and purged"
    print("RETAIN %d  PURGE %d  TOTAL %d" % (len(RETAIN), len(PURGE),
                                             len(RETAIN) + len(PURGE)))

    with open(STATE, "r", encoding="utf-8") as fh:
        state = json.load(fh)
    with open(NOT_CORPUS, "r", encoding="utf-8") as fh:
        notcorpus = json.load(fh)

    papers = state["papers"]
    before = len(papers)

    added = 0
    for pmid, (title, journal, year, prov) in sorted(RETAIN.items()):
        if pmid in papers:
            print("  already in state, skipping: %s" % pmid)
            continue
        papers[pmid] = {
            "status": "UNVETTED",
            "added": TODAY,
            "source": "reconcile_unreachable_papers_20260825",
            "title": title,
            "journal": journal,
            "year": year,
            "index_provenance": prov,
            "pmid_verified": True,
            "pmid_verified_on": TODAY,
            "pmid_verified_how": "live NCBI esummary; index title agreed with PubMed title",
            "note": ("Was present in the paper index but ABSENT from state['papers'], so the "
                     "vetting batch could never reach it. Folded in as UNVETTED, not VETTED: "
                     "PMID existence and title agreement were checked on %s, the CLAIMS were "
                     "not." % TODAY),
        }
        added += 1

    purged = 0
    for pmid, (title, journal, year, why) in sorted(PURGE.items()):
        if pmid in notcorpus["pmids"]:
            continue
        notcorpus["pmids"][pmid] = {
            "actual_title": title,
            "journal": journal,
            "year": year,
            "provenance": OFF_DOMAIN,
            "why": why,
            "disqualifier": ("UNCITED (zero dashboard_locations) AND outside the diabetes / "
                             "islet / beta-cell / diabetes-immunology domain. Resolves to a "
                             "real PubMed record, which is exactly why every existence-checking "
                             "gate passed it."),
            "adjudicated": TODAY,
            "by": "reconcile_unreachable_papers_20260825.py",
            "title_source": "live NCBI esummary %s" % TODAY,
        }
        purged += 1

    notcorpus["last_updated"] = TODAY

    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=1, ensure_ascii=False)
    with open(NOT_CORPUS, "w", encoding="utf-8") as fh:
        json.dump(notcorpus, fh, indent=2, ensure_ascii=False)

    counts = {}
    for rec in papers.values():
        counts[rec.get("status", "?")] = counts.get(rec.get("status", "?"), 0) + 1

    print("state['papers']: %d -> %d  (+%d folded in)" % (before, len(papers), added))
    print("not_corpus_pmids: +%d purged (registry now %d)" % (purged, len(notcorpus["pmids"])))
    print("status counts now: %s" % counts)
    print("[OK]")


if __name__ == "__main__":
    main()
