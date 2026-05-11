# Evidence Extract: PMID 40598585 (Beese SE et al, BMC Medicine 2025)

## Bibliographic
- Title: "A systematic review and network meta-analysis of interventions to preserve insulin-secreting beta cell function in people newly diagnosed with type 1 diabetes: results from randomised controlled trials of immunomodulatory therapies"
- Journal: BMC Med 2025
- DOI: 10.1186/s12916-025-04201-z
- PMCID: PMC12211534
- PROSPERO: CRD42018107904

## Methods
- 60 RCTs included; 4597 patients; 32 intervention classes
- 41 trials of 42 interventions eligible for NMA
- Searches through 31 Jul 2024
- Random-effects NMA, primary outcome = C-peptide at 12 months
- Cochrane RoB Tool 1

## 11 Interventions Statistically Significantly Higher C-peptide vs Placebo at 12 mo
1. Autologous mesenchymal stem cells
2. Wharton's jelly-derived MSCs
3. Azathioprine
4. Interferon-alpha (5000 IU)
5. Autologous dendritic cells
6. Anti-TNF golimumab
7. Low-dose ATG (anti-thymocyte globulin)
8. Teplizumab 3 mg 1-course (anti-CD3)
9. Baricitinib (JAK1/2 inhibitor)
10. Cyclosporin
11. Teplizumab 9/11 mg 2-course (anti-CD3)

## CRITICAL FINDING — corrects prior state note
- **Rituximab is NOT in the top 11 list per the abstract.**
- Prior state note (2026-05-06 audit) claimed "rituximab is among 11/42" — this appears to overstate. The abstract enumerates exactly 11 and rituximab is not named among them.
- Action: correct rituximab → T1D / rituximab → beta_cell validation rationale to remove the BMC Med 2025 NMA as supporting evidence; rely on Pescovitz NEJM 2009 (PMID 19940299) and Pescovitz Diabetes Care 2014 (PMID 24026563) only. Status remains PARTIALLY_VALIDATED on the basis of those two trials but no longer "confirmed by NMA top-11."

## Cross-reference vs existing path validations
| Intervention (top-11)            | Existing path?                     | Path status               |
|----------------------------------|------------------------------------|---------------------------|
| Teplizumab (both dosings)        | teplizumab-related (TN-10/PROTECT) | Independently validated   |
| Low-dose ATG                     | START / minATG                     | Already validated         |
| Golimumab (anti-TNF)             | anti-TNF -> beta_cell              | NEW VALIDATION CANDIDATE  |
| Baricitinib (JAK1/2)             | not in research_paths.json yet     | NEW PATH CANDIDATE        |
| Cyclosporin                      | historical, not active path        | n/a                       |
| Azathioprine                     | not in active paths                | n/a                       |
| MSC (auto + Wharton's)           | partial coverage                   | NEW VALIDATION CANDIDATE  |
| IFN-alpha (5000 IU)              | not in active paths                | n/a                       |
| Autologous dendritic cells       | not in active paths                | n/a                       |

## Caveats from authors (verbatim short)
- "data for some interventions originated from small studies (mesenchymal stem cell therapies, azathioprine, autologous dendritic cells) and findings should be considered as hypothesis generating"
- "substantial heterogeneity present"

## Recommended state updates
1. Add 2 candidate paths to validate: golimumab → T1D beta-cell, baricitinib → T1D beta-cell
2. Correct rituximab validation rationale (remove NMA top-11 claim)
3. Mark teplizumab and low-dose ATG paths as cross-confirmed by NMA
