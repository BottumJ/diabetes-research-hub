#!/usr/bin/env python3
"""
Project: Islet Transplant × Drug Repurposing — Phase 2: Drug-Target Mapping
Reads Phase 1 targets and maps FDA-approved drugs via ChEMBL and OpenTargets.

Input: Analysis/Results/islet_repurposing_targets.json
Output: Analysis/Results/islet_repurposing_drug_candidates.json
        Analysis/Results/islet_repurposing_report.md
"""

import json
import time
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

try:
    import requests
except ImportError:
    print("ERROR: requests library required.")
    sys.exit(1)

RESULTS_DIR = Path(__file__).parent.parent / "Results"
CHEMBL_API = "https://www.ebi.ac.uk/chembl/api/data"
OPENTARGETS_API = "https://api.platform.opentargets.org/api/v4/graphql"

# Standard immunosuppressants to flag (not exclude — they're the baseline)
STANDARD_IMMUNOSUPPRESSANTS = {
    "TACROLIMUS", "CYCLOSPORINE", "MYCOPHENOLATE MOFETIL", "MYCOPHENOLIC ACID",
    "SIROLIMUS", "EVEROLIMUS", "AZATHIOPRINE", "PREDNISONE", "PREDNISOLONE",
    "METHYLPREDNISOLONE", "BASILIXIMAB", "ANTITHYMOCYTE GLOBULIN",
}


def query_opentargets_drugs(target_id):
    """Get drugs associated with a target from OpenTargets (v26.03 schema)."""
    q = """
    query TargetDrugs($targetId: String!) {
      target(ensemblId: $targetId) {
        approvedSymbol
        drugAndClinicalCandidates {
          count
          rows {
            maxClinicalStage
            drug {
              id
              name
              drugType
              maximumClinicalStage
              drugWarnings { warningType toxicityClass }
              mechanismsOfAction {
                rows { actionType mechanismOfAction }
              }
            }
          }
        }
      }
    }
    """
    result = requests.post(OPENTARGETS_API, json={"query": q, "variables": {"targetId": target_id}}, timeout=30)
    result.raise_for_status()
    return result.json().get("data", {}).get("target", {})


def query_chembl_target_drugs(gene_symbol):
    """Query ChEMBL for drugs targeting a specific gene."""
    # Search for target
    url = f"{CHEMBL_API}/target/search.json"
    params = {"q": gene_symbol, "limit": 5, "format": "json"}
    resp = requests.get(url, params=params, timeout=20)
    if resp.status_code != 200:
        return []

    data = resp.json()
    targets = data.get("targets", [])
    if not targets:
        return []

    # Get mechanisms for top target
    target_chembl = targets[0].get("target_chembl_id")
    if not target_chembl:
        return []

    mech_url = f"{CHEMBL_API}/mechanism.json"
    mech_params = {"target_chembl_id": target_chembl, "limit": 50, "format": "json"}
    mech_resp = requests.get(mech_url, params=mech_params, timeout=20)
    if mech_resp.status_code != 200:
        return []

    mechanisms = mech_resp.json().get("mechanisms", [])

    drugs = []
    for mech in mechanisms:
        mol_chembl = mech.get("molecule_chembl_id")
        if mol_chembl:
            drugs.append({
                "molecule_chembl_id": mol_chembl,
                "mechanism": mech.get("mechanism_of_action", ""),
                "action_type": mech.get("action_type", ""),
                "target_chembl_id": target_chembl,
            })

    return drugs


def get_chembl_molecule_info(chembl_id):
    """Get molecule details from ChEMBL."""
    url = f"{CHEMBL_API}/molecule/{chembl_id}.json"
    resp = requests.get(url, timeout=20)
    if resp.status_code != 200:
        return None
    data = resp.json()
    return {
        "chembl_id": chembl_id,
        "name": data.get("pref_name", ""),
        "max_phase": data.get("max_phase", 0),
        "molecule_type": data.get("molecule_type", ""),
        "first_approval": data.get("first_approval"),
        "withdrawn": data.get("withdrawn_flag", False),
        "oral": data.get("oral", False),
        "indication_class": data.get("indication_class", ""),
    }


def main():
    print("=" * 70)
    print("ISLET TRANSPLANT × DRUG REPURPOSING — Phase 2: Drug-Target Mapping")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    # Load Phase 1 targets
    targets_path = RESULTS_DIR / "islet_repurposing_targets.json"
    if not targets_path.exists():
        print("ERROR: Phase 1 output not found. Run phase 1 first.")
        sys.exit(1)

    with open(targets_path) as f:
        phase1 = json.load(f)

    targets = phase1["targets"]
    print(f"Loaded {len(targets)} targets from Phase 1")

    # Take top targets by composite score (API rate limits)
    top_n = 60
    top_targets = targets[:top_n]
    print(f"Querying drugs for top {top_n} targets...\n")

    # ── Query OpenTargets for approved drugs ──
    drug_map = {}  # drug_name -> drug_info
    drug_target_links = []  # (drug, target, mechanism)

    STAGE_RANK = {"APPROVAL": 5, "PHASE_4": 4, "PHASE_3": 3, "PHASE_2": 2, "PHASE_1": 1}

    print("[1/3] Querying OpenTargets for drug-target associations...")
    ot_success = 0
    for i, target in enumerate(top_targets):
        ensembl_id = target.get("ensembl_id")
        symbol = target["symbol"]

        if not ensembl_id:
            continue

        try:
            result = query_opentargets_drugs(ensembl_id)
            if not result:
                continue

            drug_data = result.get("drugAndClinicalCandidates", {})
            rows = drug_data.get("rows", [])

            approved_count = 0
            for row in rows:
                drug = row.get("drug", {})
                drug_name = (drug.get("name") or "").upper()
                max_stage = drug.get("maximumClinicalStage", "")
                stage_num = STAGE_RANK.get(max_stage, 0)
                warnings = drug.get("drugWarnings", []) or []
                is_withdrawn = any(w.get("warningType") == "Withdrawn" for w in warnings)

                if not drug_name:
                    continue

                # Include Phase 3+ and approved
                if stage_num >= 3:
                    # Get mechanisms
                    moa_rows = (drug.get("mechanismsOfAction") or {}).get("rows", [])
                    moa_text = "; ".join(m.get("mechanismOfAction", "") for m in moa_rows[:3] if m.get("mechanismOfAction"))

                    if drug_name not in drug_map:
                        drug_map[drug_name] = {
                            "name": drug_name,
                            "drug_id": drug.get("id"),
                            "drug_type": drug.get("drugType"),
                            "max_phase": stage_num,
                            "max_stage": max_stage,
                            "is_approved": max_stage == "APPROVAL",
                            "withdrawn": is_withdrawn,
                            "targets_hit": [],
                            "mechanisms": [],
                            "is_standard_immunosuppressant": drug_name in STANDARD_IMMUNOSUPPRESSANTS,
                        }
                    drug_map[drug_name]["targets_hit"].append(symbol)
                    if moa_text:
                        drug_map[drug_name]["mechanisms"].append(moa_text)
                    drug_target_links.append((drug_name, symbol, moa_text))
                    approved_count += 1

            if approved_count > 0:
                ot_success += 1

            if (i + 1) % 10 == 0:
                print(f"  [{i+1}/{top_n}] {ot_success} targets with drugs found, {len(drug_map)} unique drugs")

            time.sleep(0.2)

        except Exception as e:
            if "429" in str(e) or "rate" in str(e).lower():
                print(f"  Rate limited at {symbol}, waiting 5s...")
                time.sleep(5)
            continue

    print(f"  OpenTargets: {len(drug_map)} drugs found across {ot_success} targets\n")

    # ── Query ChEMBL for additional drug-target mappings ──
    print("[2/3] Querying ChEMBL for additional drug mechanisms...")
    chembl_additions = 0
    for i, target in enumerate(top_targets[:30]):  # smaller batch for ChEMBL
        symbol = target["symbol"]
        try:
            chembl_drugs = query_chembl_target_drugs(symbol)
            for cd in chembl_drugs:
                mol_id = cd["molecule_chembl_id"]
                # Get molecule details
                mol_info = get_chembl_molecule_info(mol_id)
                if mol_info and mol_info.get("max_phase", 0) >= 3:
                    drug_name = (mol_info.get("name") or mol_id).upper()
                    if drug_name and drug_name not in drug_map:
                        drug_map[drug_name] = {
                            "name": drug_name,
                            "drug_id": mol_id,
                            "drug_type": mol_info.get("molecule_type"),
                            "max_phase": mol_info["max_phase"],
                            "is_approved": mol_info["max_phase"] >= 4,
                            "withdrawn": mol_info.get("withdrawn", False),
                            "targets_hit": [symbol],
                            "mechanisms": [cd.get("mechanism", "")],
                            "is_standard_immunosuppressant": drug_name in STANDARD_IMMUNOSUPPRESSANTS,
                            "chembl_info": mol_info,
                        }
                        chembl_additions += 1
                    elif drug_name in drug_map and symbol not in drug_map[drug_name]["targets_hit"]:
                        drug_map[drug_name]["targets_hit"].append(symbol)

            time.sleep(0.3)

        except Exception as e:
            continue

        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/30] {chembl_additions} new drugs from ChEMBL")

    print(f"  ChEMBL: {chembl_additions} additional drugs found\n")

    # ── Score and rank candidates ──
    print("[3/3] Scoring and ranking drug candidates...")

    candidates = []
    for drug_name, info in drug_map.items():
        # Deduplicate targets and mechanisms
        unique_targets = list(set(info["targets_hit"]))
        unique_mechs = list(set(m for m in info["mechanisms"] if m))

        # Scoring
        target_count = len(unique_targets)
        is_approved = 1 if info.get("is_approved") else 0
        is_withdrawn = 1 if info.get("withdrawn") else 0
        is_standard = 1 if info.get("is_standard_immunosuppressant") else 0

        # Composite repurposing score:
        # - More targets = better (multi-target drugs are more interesting)
        # - Approved > Phase 3
        # - Penalize withdrawn drugs
        # - Flag (don't penalize) standard immunosuppressants
        repurposing_score = (
            target_count * 2.0 +
            is_approved * 1.0 +
            (info.get("max_phase", 0) * 0.25) -
            is_withdrawn * 5.0
        )

        # Novelty bonus: NOT a standard immunosuppressant = more interesting
        if not is_standard:
            repurposing_score += 2.0

        candidates.append({
            "drug_name": drug_name,
            "drug_id": info.get("drug_id"),
            "drug_type": info.get("drug_type"),
            "max_phase": info.get("max_phase"),
            "is_approved": info.get("is_approved"),
            "withdrawn": info.get("withdrawn"),
            "is_standard_immunosuppressant": is_standard,
            "targets_hit": unique_targets,
            "target_count": target_count,
            "mechanisms": unique_mechs,
            "repurposing_score": round(repurposing_score, 2),
        })

    candidates.sort(key=lambda x: x["repurposing_score"], reverse=True)

    # Separate novel from standard
    novel_candidates = [c for c in candidates if not c["is_standard_immunosuppressant"] and not c["withdrawn"]]
    standard_drugs = [c for c in candidates if c["is_standard_immunosuppressant"]]
    withdrawn_drugs = [c for c in candidates if c["withdrawn"]]

    # ── Save results ──
    output = {
        "metadata": {
            "project": "Islet Transplant × Drug Repurposing",
            "phase": "Phase 2 — Drug-Target Mapping",
            "date": datetime.now().isoformat(),
            "targets_queried": top_n,
            "total_drugs_found": len(candidates),
            "novel_candidates": len(novel_candidates),
            "standard_immunosuppressants": len(standard_drugs),
            "withdrawn": len(withdrawn_drugs),
        },
        "novel_candidates": novel_candidates[:100],
        "standard_drugs": standard_drugs,
        "withdrawn_drugs": withdrawn_drugs[:20],
        "drug_target_links": drug_target_links[:500],
    }

    output_path = RESULTS_DIR / "islet_repurposing_drug_candidates.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    # ── Generate markdown report ──
    report_lines = [
        "# Islet Transplant × Drug Repurposing — Candidate Report",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Gap Score:** 100.0 (zero joint publications in PubMed 2020-2026)",
        f"**Validation Level:** BRONZE (computational screening; requires expert review)",
        f"**Evidence Level:** 4 (mechanism-based reasoning; computational)",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"Screened **{top_n} protein targets** involved in islet graft rejection and beta cell protection",
        f"against **{len(candidates)} drugs** (Phase 3+ or FDA-approved) from OpenTargets and ChEMBL.",
        "",
        f"| Category | Count |",
        f"|----------|-------|",
        f"| Novel repurposing candidates | {len(novel_candidates)} |",
        f"| Standard immunosuppressants (baseline) | {len(standard_drugs)} |",
        f"| Withdrawn (excluded) | {len(withdrawn_drugs)} |",
        "",
        "---",
        "",
        "## Top 30 Novel Repurposing Candidates",
        "",
        "These drugs are NOT standard transplant immunosuppressants but hit targets relevant to",
        "islet graft protection. They represent the novel repurposing opportunities.",
        "",
        "| Rank | Drug | Type | Phase | Targets Hit | Score | Key Mechanisms |",
        "|------|------|------|-------|-------------|-------|----------------|",
    ]

    for i, c in enumerate(novel_candidates[:30], 1):
        mechs = "; ".join(c["mechanisms"][:2]) if c["mechanisms"] else "—"
        if len(mechs) > 50:
            mechs = mechs[:47] + "..."
        targets = ", ".join(c["targets_hit"][:4])
        if len(c["targets_hit"]) > 4:
            targets += f" +{len(c['targets_hit'])-4}"
        phase = f"Phase {c['max_phase']}" if c['max_phase'] else "?"
        report_lines.append(
            f"| {i} | **{c['drug_name']}** | {c['drug_type'] or '—'} | {phase} | {targets} | {c['repurposing_score']} | {mechs} |"
        )

    report_lines.extend([
        "",
        "---",
        "",
        "## Standard Immunosuppressants (Baseline Comparison)",
        "",
        "These drugs are already used in transplant settings. Listed for reference.",
        "",
        "| Drug | Targets Hit | Score |",
        "|------|-------------|-------|",
    ])

    for c in standard_drugs:
        targets = ", ".join(c["targets_hit"][:3])
        report_lines.append(f"| {c['drug_name']} | {targets} | {c['repurposing_score']} |")

    report_lines.extend([
        "",
        "---",
        "",
        "## Interpretation & Next Steps",
        "",
        "### What This Means",
        "",
        "The novel candidates are drugs approved for OTHER indications (cancer, autoimmune disease,",
        "cardiovascular) that happen to target proteins involved in islet graft rejection or beta cell",
        "protection. They represent potential repurposing opportunities where:",
        "",
        "1. The drug is already safety-tested in humans (shorter path to clinical use)",
        "2. The mechanism of action is relevant to islet protection",
        "3. The drug is NOT the standard immunosuppressive regimen",
        "",
        "### Caveats (Per Research Doctrine)",
        "",
        "- **Evidence Level 4**: These are computational predictions based on target overlap,",
        "  not clinical evidence of islet protection",
        "- **Validation needed**: Each candidate requires literature review for existing evidence",
        "  of islet-relevant activity (Phase 4 of research plan)",
        "- **Off-target effects**: Multi-target drugs may have unwanted effects on islet function",
        "- **Dosing**: Approved doses for original indication may not be appropriate for islet protection",
        "",
        "### Recommended Actions",
        "",
        "1. **Review top 10 candidates** — Literature search for existing islet/beta cell evidence",
        "2. **Cross-reference with ClinicalTrials.gov** — Any trials using these drugs in diabetes?",
        "3. **Consult domain experts** — Present candidates to transplant immunologists",
        "4. **Phase 3**: Network pharmacology analysis to identify multi-target synergies",
        "",
        "---",
        "",
        f"*Generated by Diabetes Research Hub | Research Doctrine v1.1 | Phase 2 of 6*",
    ])

    report_path = RESULTS_DIR / "islet_repurposing_report.md"
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))

    # Print summary
    print("\n" + "=" * 70)
    print("PHASE 2 COMPLETE")
    print("=" * 70)
    print(f"Total drugs mapped: {len(candidates)}")
    print(f"Novel repurposing candidates: {len(novel_candidates)}")
    print(f"Standard immunosuppressants: {len(standard_drugs)}")
    print(f"Withdrawn (excluded): {len(withdrawn_drugs)}")
    print(f"\nTop 15 Novel Repurposing Candidates:")
    print("-" * 70)
    print(f"{'Rank':>4} {'Drug':<25} {'Phase':>6} {'Targets':>8} {'Score':>6}")
    print("-" * 70)
    for i, c in enumerate(novel_candidates[:15], 1):
        name = c['drug_name'][:24]
        phase = c['max_phase'] or '?'
        print(f"{i:>4} {name:<25} {phase:>6} {c['target_count']:>8} {c['repurposing_score']:>6.1f}")

    print(f"\nOutputs saved to:")
    print(f"  {output_path}")
    print(f"  {report_path}")


if __name__ == "__main__":
    main()
