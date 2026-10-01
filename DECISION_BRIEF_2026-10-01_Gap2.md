# Decision Brief — Gap #2, the last GOLD gap (2026-10-01)

**Asks for one ruling.** Nothing about Gap #2's tier has been changed. Factual errors on its page have
been corrected (listed at the end), because those were not judgement calls.

---

## 1. Gap #2 is two different questions sharing one number

| Where | Title | What it claims |
|---|---|---|
| `gap_evidence.json`, `extract_evidence.py`, Extracted Evidence page | **Health Equity in Diabetes** | Disparities in diabetes care and outcomes by race, ethnicity and income |
| Gap Deep Dives, Methodology, README, landing page | **Health Equity in Beta Cell Therapies** | Cell therapies for type 1 diabetes are being trialled only where few of the world's patients live |

The gates check one and the reader sees the other. The tier-agreement gate passes because the *tier*
matches in every copy; nothing compares the *question*.

## 2. Read as "Health Equity in Diabetes", it is not a gap

All 15 stored papers are about diabetes disparities, and 14 of them cover both halves of the question.
That is the opposite of an absence: disparities in diabetes are heavily studied. The scheduled agent
said so twice:

- **2026-08-16:** a completed equity RCT, conditional pharmacy vouchers in low-income adults with type 2
  diabetes, n=186, HbA1c difference 0.7 points (PMID 41587834).
- **2026-09-04:** a second, medically tailored groceries for 460 Medicaid-insured adults, 85% Hispanic,
  HbA1c difference −0.40 points (PMID 42478360, *Circulation* 2026). The agent wrote that "the premise
  of this GOLD tier is now falsified twice", and no one ruled.

Under Lesson 9 this version cannot be GOLD, or any tier: there is no absence to evidence.

## 3. Read as "Health Equity in Beta Cell Therapies", it is a real, narrower gap

**The absence.** One source: the hub's PubMed co-publication matrix (health equity × beta cell,
0 joint publications). No dated, recorded null search for an equity analysis of access to cell therapies
exists in the repository.

**The premise, now measurable and measured** (ClinicalTrials.gov, queried 2026-10-01, reproducible):

- Zimislecel, the most advanced product: **36 site listings across its two trials, in 10 countries, all
  high-income** (United States 15,
  Canada 6, United Kingdom 4, Saudi Arabia 4, France 2, one each in Germany, Italy, Netherlands, Norway,
  Switzerland). Not approved; regulatory submission expected in 2026.
- All active type 1 diabetes islet, stem-cell and beta-cell studies with listed sites: **76 studies; none
  in India or any African country**; most common are the United States (31), China (11) and France (8).
- Not sourced: how type 1 diabetes burden is distributed by country income. The page's "81% of burden in
  LMICs" figure had no source and has been withdrawn.

**Under Lesson 9:** one search source for the absence, premise partly sourced (trial geography yes,
burden distribution no). That is **BRONZE**.

## 4. The ruling

| Option | Effect |
|---|---|
| **A. Keep "Beta Cell Therapies", set BRONZE (recommended)** | One question everywhere. The evidence store is re-pointed at cell-therapy access, and the 15 general-disparity papers become context. A second search source (e.g. the WHO or IDF type 1 burden figures plus a dated null search for cell-therapy equity analyses) would make it SILVER. |
| B. Keep "Beta Cell Therapies", EXPLORATORY | The same, but treats the single matrix query as not yet a documented search. |
| C. Keep "Health Equity in Diabetes" | The general topic, which is well studied. Under Lesson 9 it is not a gap, so it would be retired rather than tiered. |
| D. Leave GOLD | Not supportable under either reading. |

Either way, after this ruling **no gap is GOLD**. That is what the rule implies for a portfolio of absence
claims searched in one database: the evidence has not yet reached three independent sources for any gap.

## 5. Corrected today on Gap #2's page (not tier decisions)

- **"VX-880 (zimislecel): FDA approved"** — false in three places, including the data dictionary. It is in
  the phase 3 portion of FORWARD; the sponsor expects to submit in 2026.
- **Mechanism detail** described a "GADA-selected iPSC line genetically matched to donor HLA" with a
  day-by-day protocol and potency figures. None had a source, and HLA matching contradicts an allogeneic
  product given with immunosuppression. Replaced with the NEJM description (PMID 40544428).
- **Trial-site list** named Sweden, Belgium, Spain and Australia (no site) and omitted five countries that
  have one. Replaced with the registry counts above.
- **"149M in LADA/T1D burden"** summed total adult diabetes counts and labelled them type 1. Relabelled
  and marked unsourced.
- **"iPSC-derived islets show improved outcomes vs allogeneic"** had no source. Removed.

---

*Sources: ClinicalTrials.gov API v2 (NCT04786262, NCT06832410, and a condition/intervention query for
active type 1 cell-therapy studies), 2026-10-01; Breakthrough T1D summary of Vertex's 2025 update
(VX-264 discontinued; zimislecel submission expected 2026); PMIDs 40544428, 41587834, 42478360.*
