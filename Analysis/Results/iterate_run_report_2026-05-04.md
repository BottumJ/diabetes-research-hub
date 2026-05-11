# Iterate Run Report — 2026-05-04 (Monday)

## Summary
- Papers vetted: **7 VETTED, 1 FLAGGED** (8 total) — corpus now 258 VETTED / 13 FLAGGED / 9 UNVETTED
- Paths modified: 3 (1 removed, 2 cleaned)
- New papers discovered: **9** (weekly PubMed sweep, all eutils-verified)
- Scripts fixed: 2 (overstatement softening + truncation repair)
- Pipeline status: 41/41 OK

## Paper Vetting Decisions
| PMID | Status | Note |
|------|--------|------|
| 41827829 | FLAGGED | MIAMI cell EVs, Cells 2026. Off-topic — abstract has zero diabetes content. |
| 41827917 | VETTED | GENEPEDIAB pediatric atypical diabetes / MODY continuum. |
| 41921761 | VETTED | Oral-gut microbiome axis systematic review in DM. |
| 41891251 | VETTED | PNIPAM/tannic acid hydrogels for diabetic wound healing. |
| 41884608 | VETTED | Levocarnitine-alprostadil combination in ESRD-DN. |
| 41876017 | VETTED | Propyl gallate ferroptosis in diabetic liver (preclinical). |
| 41852470 | VETTED | TCM diabetes review — flag any extraction efficacy claims. |
| 41828705 | VETTED | ER stress genes in DKD bioinformatics + mouse. |

## Rituximab → Nephropathy Path Resolution
**Investigation:** PMID 19940299 (TrialNet rituximab T1D RCT, NEJM 2009) was the sole evidence for `rituximab -> nephropathy`. Inspection of the extraction context revealed the "nephropathy" tag came from the paper's references section citing "Rituximab treatment of idiopathic membranous nephropathy" — a citation about a non-diabetic condition picked up as condition co-occurrence.

**Action taken:**
- Removed `rituximab -> nephropathy` from `research_paths.json` (47 paths now, was 48)
- Stripped `nephropathy` from `rituximab -> T1D` and `rituximab -> beta_cell` `conditions` dicts
- Added `_provenance_note` documenting the false-positive
- Audited 4 drug-repurposing dashboards: no rituximab+DKD claims (clean)
- Edited `Dashboards/Research_Paths.html` to add comment explaining removal
- Backed up original to `research_paths.json.bak_2026-05-04`

## Weekly PubMed Search (Monday cadence)
Query results (last 7 days, filtered to relevant):
- LADA: 0 hits
- islet_transplant: 1 added (41172147 — TP-IAT GI symptoms, Pancreas)
- NLRP3_DKD: 1 added (42065920 — cellular senescence in diabetic atherosclerosis)
- oxidative_combo: 7 added (42066937 SGLT2i+training pyroptosis; 42057440 thujaplicin DKD; 42050925 ezetimibe STZ; 42045987 MSC DFU; 42045904 ROS microneedle; 42021540 melatonin+quercetin; 42070055 purslane+metformin)
- verapamil_T1D, dapa_colchicine, drug_repurpose: 0 hits

All 9 PMIDs verified via NCBI E-utilities `esummary` endpoint. Added as UNVETTED with high-priority vetting in next run.

## Credibility Sweep
- **PMIDs >42M:** No fabrications. Only false positives are PROSPERO IDs (CRD420251073207) which are correctly labelled `[unverified]` in source.
- **"Zero SAEs" / "zero rejection":** None found.
- **"Achieves" / "curative":** Reviewed 5 hits. 4 are benign (mechanism descriptions, ML metrics, model outputs). Fixed 1 in `rebuild_research_dashboard.py`:
  - `"Chinese team achieves insulin independence with iPSC"` → `"Chinese single-patient case: iPSC islet cells reduce exogenous insulin needs"` (n=1 not "achievement")
  - `"Sana engineered islets survive 6 months in humans...holy grail"` → `"reported viable at 6 months in early-phase trial...durability beyond 6 months not yet established"`

## Fixed: Sync-Corrupted Script
`Analysis/Scripts/rebuild_research_dashboard.py` had an on-disk truncation: file ended at line `    pr` (incomplete). Restored the trailing two `print(...)` statements; full rebuild now succeeds. Likely an OneDrive sync interruption from the previous edit.

## Doctrine Update Recommended
The doctrine heuristic "PMIDs above 42000000 are fabricated" needs revision. As of May 2026, real PubMed IDs are in the 42M range (verified via eutils). Future credibility sweeps should verify suspect PMIDs via E-utilities `esummary` rather than rejecting by number alone. Note added to `state['doctrine_notes']`.

## Blockers (Persistent)
**.git lock files cannot be removed from Linux mount** (EPERM, even with chmod):
- `.git/HEAD.lock` (since 2026-04-30)
- `.git/index.lock` (since 2026-04-30)
- `.git/objects/maintenance.lock` (since 2026-04-16)

This is the **2nd consecutive run** the user must clear these locks via Windows PowerShell:
```powershell
cd "C:\Users\justi\OneDrive\Diabetes_Research"
Remove-Item .git\HEAD.lock, .git\index.lock, .git\objects\maintenance.lock -Force
```
Once cleared, the queued commits/pushes from 2026-04-30 onward will go through. State has been preserved on disk; only git operations are blocked.

## Work Queue After This Run (15 items, top 5)
1. **P1** manual_cleanup_required — clear .git lock files (BLOCKED 2 runs now)
2. **P3** extraction_filter_review — PMID 35437333 CRC issue (since 2026-04-29)
3. **P3** vet_papers_batch — 9 new papers from 2026-05-04 PubMed sweep
4. **P3** extract_evidence — PMID 40598585 NMA T1D immunotherapies
5. **P4** extraction_filter_review — refs-section filter (NEW, from rituximab investigation)

## Next Run Priorities
1. Vet the 9 new UNVETTED papers (especially 42066937 SGLT2i+training, since it bears on the SGLT2i combination paths)
2. PMID 40598585 evidence extraction
3. If user has cleared .git locks: commit & push backlog
