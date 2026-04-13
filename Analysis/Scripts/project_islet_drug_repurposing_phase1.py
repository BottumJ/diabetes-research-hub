#!/usr/bin/env python3
"""
Project: Islet Transplant × Drug Repurposing — Phase 1: Target Identification
Gap #3 from Literature Gap Analysis | Gap Score: 100.0 | Joint Publications: 0

Queries OpenTargets and STRING to build a comprehensive target list for
islet graft rejection and beta cell protection.

Output: Analysis/Results/islet_repurposing_targets.json
"""

import json
import time
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)

RESULTS_DIR = Path(__file__).parent.parent / "Results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

OPENTARGETS_API = "https://api.platform.opentargets.org/api/v4/graphql"
STRING_API = "https://string-db.org/api"
SPECIES_ID = 9606  # Homo sapiens


# ── OpenTargets Queries ──────────────────────────────────────────────

def query_opentargets(query_str, variables=None):
    """Execute a GraphQL query against OpenTargets."""
    payload = {"query": query_str}
    if variables:
        payload["variables"] = variables
    resp = requests.post(OPENTARGETS_API, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def search_disease_targets(disease_term, size=200):
    """Search OpenTargets for targets associated with a disease term."""
    # First, find disease IDs
    search_q = """
    query SearchDisease($term: String!, $size: Int!) {
      search(queryString: $term, entityNames: ["disease"], page: {index: 0, size: $size}) {
        total
        hits {
          id
          name
          entity
          score
        }
      }
    }
    """
    result = query_opentargets(search_q, {"term": disease_term, "size": 10})
    diseases = result.get("data", {}).get("search", {}).get("hits", [])
    return diseases


def get_disease_targets(disease_id, size=500):
    """Get all targets associated with a disease from OpenTargets."""
    targets_q = """
    query DiseaseTargets($diseaseId: String!, $size: Int!) {
      disease(efoId: $diseaseId) {
        id
        name
        associatedTargets(page: {index: 0, size: $size}) {
          count
          rows {
            target {
              id
              approvedSymbol
              approvedName
              biotype
              tractability {
                label
                modality
                value
              }
            }
            score
            datatypeScores {
              id
              score
            }
          }
        }
      }
    }
    """
    result = query_opentargets(targets_q, {"diseaseId": disease_id, "size": size})
    return result.get("data", {}).get("disease", {})


def search_target_info(gene_symbol):
    """Search OpenTargets for a specific target by gene symbol."""
    q = """
    query SearchTarget($term: String!) {
      search(queryString: $term, entityNames: ["target"], page: {index: 0, size: 5}) {
        hits {
          id
          name
          entity
          score
        }
      }
    }
    """
    result = query_opentargets(q, {"term": gene_symbol})
    return result.get("data", {}).get("search", {}).get("hits", [])


# ── STRING Queries ───────────────────────────────────────────────────

def string_get_interactions(proteins, required_score=700):
    """Get protein-protein interactions from STRING."""
    url = f"{STRING_API}/json/network"
    params = {
        "identifiers": "%0d".join(proteins),
        "species": SPECIES_ID,
        "required_score": required_score,
        "caller_identity": "diabetes_research_hub"
    }
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def string_get_enrichment(proteins):
    """Get functional enrichment from STRING."""
    url = f"{STRING_API}/json/enrichment"
    params = {
        "identifiers": "%0d".join(proteins),
        "species": SPECIES_ID,
        "caller_identity": "diabetes_research_hub"
    }
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def string_map_identifiers(proteins):
    """Resolve gene symbols to STRING IDs."""
    url = f"{STRING_API}/json/get_string_ids"
    params = {
        "identifiers": "%0d".join(proteins),
        "species": SPECIES_ID,
        "caller_identity": "diabetes_research_hub"
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ── Main Pipeline ────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("ISLET TRANSPLANT × DRUG REPURPOSING — Phase 1: Target Identification")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    all_targets = {}  # gene_symbol -> target_info

    # ── Step 1: Query OpenTargets for disease-associated targets ──
    disease_queries = [
        ("graft rejection", "Allograft / graft rejection"),
        ("islet transplantation", "Islet transplantation"),
        ("type 1 diabetes", "Type 1 diabetes (autoimmune)"),
        ("beta cell apoptosis", "Beta cell apoptosis"),
        ("immune tolerance", "Immune tolerance"),
        ("graft versus host", "Graft-versus-host disease"),
    ]

    print("\n[1/4] Querying OpenTargets for disease-associated targets...")
    disease_target_map = {}

    for query_term, label in disease_queries:
        print(f"  Searching: {label}...")
        try:
            diseases = search_disease_targets(query_term)
            if not diseases:
                print(f"    No disease entries found for '{query_term}'")
                continue

            for disease in diseases[:3]:  # top 3 matches per query
                disease_id = disease["id"]
                disease_name = disease["name"]
                print(f"    → {disease_name} ({disease_id})")

                try:
                    disease_data = get_disease_targets(disease_id, size=200)
                    if not disease_data:
                        continue

                    assoc = disease_data.get("associatedTargets", {})
                    rows = assoc.get("rows", [])
                    print(f"      Found {len(rows)} associated targets")

                    for row in rows:
                        target = row["target"]
                        symbol = target["approvedSymbol"]
                        score = row["score"]

                        if symbol not in all_targets:
                            all_targets[symbol] = {
                                "ensembl_id": target["id"],
                                "symbol": symbol,
                                "name": target["approvedName"],
                                "biotype": target["biotype"],
                                "tractability": target.get("tractability", []),
                                "disease_associations": [],
                                "max_score": 0,
                                "sources": set()
                            }

                        all_targets[symbol]["disease_associations"].append({
                            "disease_id": disease_id,
                            "disease_name": disease_name,
                            "query_category": label,
                            "score": score,
                            "datatype_scores": {d["id"]: d["score"] for d in row.get("datatypeScores", [])}
                        })
                        all_targets[symbol]["max_score"] = max(all_targets[symbol]["max_score"], score)
                        all_targets[symbol]["sources"].add(label)

                    time.sleep(0.3)  # polite rate limiting

                except Exception as e:
                    print(f"      Error fetching targets: {e}")
                    continue

        except Exception as e:
            print(f"    Error searching: {e}")
            continue

    print(f"\n  Total unique targets from OpenTargets: {len(all_targets)}")

    # ── Step 2: Add curated seed targets ──
    print("\n[2/4] Adding curated seed targets from literature...")

    seed_targets = {
        # Key rejection/immune targets
        "CXCR3": "Chemokine receptor — key rejection target (PMID 16898223)",
        "CXCL10": "CXCR3 ligand — graft-infiltrating T cell chemoattractant",
        "CXCL9": "CXCR3 ligand — IFN-gamma induced",
        "ICAM1": "Adhesion molecule — T cell-endothelial interaction",
        "VCAM1": "Adhesion molecule — leukocyte recruitment",
        "FAS": "Death receptor — beta cell apoptosis pathway",
        "FASLG": "FAS ligand — immune-mediated killing",
        "TNF": "TNF-alpha — pro-inflammatory, beta cell toxicity",
        "IL1B": "IL-1 beta — islet inflammation",
        "IL6": "IL-6 — inflammatory cascade",
        "IFNG": "IFN-gamma — Th1 rejection response",
        "PDL1": "PD-L1 — immune checkpoint (CD274)",
        "CD274": "PD-L1 — immune checkpoint",
        "CTLA4": "Immune checkpoint — T cell regulation",
        "FOXP3": "Treg master regulator",
        "IL2": "T cell growth factor / Treg survival",
        "IL10": "Anti-inflammatory — tolerance induction",
        "TGFB1": "TGF-beta — immune regulation and fibrosis",

        # Beta cell survival/function
        "PDX1": "Beta cell identity transcription factor",
        "NKX6-1": "Beta cell maturity marker",
        "MAFA": "Beta cell function — insulin gene transactivator",
        "INS": "Insulin gene",
        "GCK": "Glucokinase — glucose sensor",
        "GLP1R": "GLP-1 receptor — beta cell survival signaling",
        "SLC30A8": "Zinc transporter — insulin granule",

        # Graft protection candidates
        "BCL2": "Anti-apoptotic — beta cell survival",
        "BIRC5": "Survivin — anti-apoptotic",
        "HIF1A": "Hypoxia response — graft vascularization",
        "VEGFA": "Vascular growth — graft revascularization",
        "NOS2": "iNOS — nitric oxide-mediated beta cell death",
        "HMOX1": "Heme oxygenase — cytoprotective",
        "NFE2L2": "Nrf2 — oxidative stress defense",
        "CASP3": "Caspase-3 — apoptosis executor",
        "JAK1": "JAK1 — cytokine signaling (baricitinib target)",
        "JAK2": "JAK2 — cytokine signaling (baricitinib target)",
        "EZH2": "Epigenetic regulator — beta cell regeneration (GSK126 target)",
        "MTOR": "mTOR — immunosuppression target (rapamycin)",
        "CALCINEURIN": "Calcineurin — tacrolimus/cyclosporine target",
        "PPP3CA": "Calcineurin catalytic subunit",
        "IMPDH2": "Mycophenolate target — purine synthesis",
    }

    for symbol, rationale in seed_targets.items():
        if symbol not in all_targets:
            all_targets[symbol] = {
                "ensembl_id": None,
                "symbol": symbol,
                "name": rationale,
                "biotype": "protein_coding",
                "tractability": [],
                "disease_associations": [],
                "max_score": 0.5,  # moderate default for curated targets
                "sources": set()
            }
        all_targets[symbol]["sources"].add("Curated (literature)")

    print(f"  Added {len(seed_targets)} seed targets")
    print(f"  Total unique targets: {len(all_targets)}")

    # ── Step 3: Query STRING for protein interactions ──
    print("\n[3/4] Querying STRING for protein interaction network...")

    # Use top-scoring targets for STRING query (API has limits)
    top_targets = sorted(all_targets.values(), key=lambda x: x["max_score"], reverse=True)
    top_symbols = [t["symbol"] for t in top_targets[:100]]

    # Map identifiers
    print(f"  Mapping {len(top_symbols)} top targets to STRING IDs...")
    try:
        string_ids = string_map_identifiers(top_symbols[:50])  # STRING batch limit
        mapped = {item.get("queryItem", ""): item.get("stringId", "") for item in string_ids}
        print(f"  Successfully mapped {len(mapped)} proteins")
    except Exception as e:
        print(f"  STRING ID mapping error: {e}")
        mapped = {}

    # Get interactions
    interactions = []
    if mapped:
        query_batch = list(mapped.keys())[:40]  # conservative batch
        print(f"  Querying interactions for {len(query_batch)} proteins (score ≥700)...")
        try:
            time.sleep(1)
            raw_interactions = string_get_interactions(query_batch, required_score=700)
            interactions = raw_interactions
            print(f"  Found {len(interactions)} high-confidence interactions")

            # Extract interaction partners not in our target list
            new_partners = set()
            for inter in interactions:
                for key in ["preferredName_A", "preferredName_B"]:
                    partner = inter.get(key, "")
                    if partner and partner not in all_targets:
                        new_partners.add(partner)

            print(f"  Discovered {len(new_partners)} new interaction partners")
            for partner in new_partners:
                all_targets[partner] = {
                    "ensembl_id": None,
                    "symbol": partner,
                    "name": f"STRING interaction partner (score ≥700)",
                    "biotype": "protein_coding",
                    "tractability": [],
                    "disease_associations": [],
                    "max_score": 0.3,
                    "sources": {"STRING network expansion"}
                }

        except Exception as e:
            print(f"  STRING interaction query error: {e}")

    # Get functional enrichment for top targets
    print("  Querying functional enrichment...")
    enrichment = []
    try:
        time.sleep(1)
        query_batch_enrich = list(mapped.keys())[:30]
        if query_batch_enrich:
            enrichment = string_get_enrichment(query_batch_enrich)
            kegg_pathways = [e for e in enrichment if e.get("category") == "KEGG"]
            go_bp = [e for e in enrichment if e.get("category") == "Process"]
            print(f"  KEGG pathways enriched: {len(kegg_pathways)}")
            print(f"  GO Biological Process terms: {len(go_bp)}")
    except Exception as e:
        print(f"  Enrichment query error: {e}")

    # ── Step 4: Score and rank targets ──
    print("\n[4/4] Scoring and ranking targets for druggability...")

    target_list = []
    for symbol, info in all_targets.items():
        # Druggability score from tractability data
        drug_score = 0
        modalities = set()
        for tract in info.get("tractability", []) or []:
            if tract and tract.get("value", False):
                drug_score += 1
                modalities.add(tract.get("modality", "unknown"))

        # Multi-source bonus
        source_count = len(info["sources"])
        source_bonus = min(source_count * 0.1, 0.5)

        # Composite score
        composite = info["max_score"] + source_bonus + (drug_score * 0.05)

        target_list.append({
            "symbol": symbol,
            "ensembl_id": info["ensembl_id"],
            "name": info["name"],
            "biotype": info["biotype"],
            "opentargets_score": round(info["max_score"], 4),
            "druggability_hits": drug_score,
            "druggable_modalities": list(modalities),
            "source_count": source_count,
            "sources": list(info["sources"]),
            "disease_associations_count": len(info["disease_associations"]),
            "composite_score": round(composite, 4),
        })

    target_list.sort(key=lambda x: x["composite_score"], reverse=True)

    # ── Save results ──
    output = {
        "metadata": {
            "project": "Islet Transplant × Drug Repurposing",
            "phase": "Phase 1 — Target Identification",
            "date": datetime.now().isoformat(),
            "total_targets": len(target_list),
            "opentargets_queries": len(disease_queries),
            "seed_targets": len(seed_targets),
            "string_interactions": len(interactions),
            "string_enrichment_terms": len(enrichment),
        },
        "targets": target_list,
        "interactions": interactions[:500],  # cap for file size
        "enrichment_kegg": [e for e in enrichment if e.get("category") == "KEGG"][:50],
        "enrichment_go_bp": [e for e in enrichment if e.get("category") == "Process"][:50],
    }

    output_path = RESULTS_DIR / "islet_repurposing_targets.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    # Print summary
    print("\n" + "=" * 70)
    print("PHASE 1 COMPLETE")
    print("=" * 70)
    print(f"Total targets identified: {len(target_list)}")
    print(f"  From OpenTargets disease queries: {sum(1 for t in target_list if any('OpenTargets' not in s and 'Curated' not in s and 'STRING' not in s for s in t['sources']))}")
    print(f"  From curated seed list: {sum(1 for t in target_list if 'Curated (literature)' in t['sources'])}")
    print(f"  From STRING network expansion: {sum(1 for t in target_list if 'STRING network expansion' in t['sources'])}")
    print(f"STRING interactions: {len(interactions)}")

    # Top 20 targets
    print(f"\nTop 20 Targets by Composite Score:")
    print("-" * 70)
    print(f"{'Rank':>4} {'Symbol':<12} {'Score':>6} {'Drug':>5} {'Sources':>4} {'Name':<35}")
    print("-" * 70)
    for i, t in enumerate(target_list[:20], 1):
        name = t['name'][:35] if t['name'] else ''
        print(f"{i:>4} {t['symbol']:<12} {t['composite_score']:>6.3f} {t['druggability_hits']:>5} {t['source_count']:>4} {name}")

    print(f"\nOutput saved to: {output_path}")
    print(f"Next step: Run project_islet_drug_repurposing_phase2.py")

    return output


if __name__ == "__main__":
    main()
