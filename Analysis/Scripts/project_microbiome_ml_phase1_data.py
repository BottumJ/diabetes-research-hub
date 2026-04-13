#!/usr/bin/env python3
"""
Project: Multi-Omic Microbiome ML Diagnostic Pipeline — Phase 1: Data Acquisition
Inspired by PMID 41921761 (oral-gut microbiome axis, AUC >0.83)
Tier 1 Alignment: AI/ML Prediction (18/20) + Multi-Omics Biomarker Integration (19/20)

Phase 1 scans available public datasets and builds a catalog of usable data.
"""

import json
import time
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests library required.")
    sys.exit(1)

RESULTS_DIR = Path(__file__).parent.parent / "Results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def search_ncbi_gds(term, retmax=50):
    """Search NCBI GEO DataSets for microbiome + diabetes studies."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "gds",
        "term": term,
        "retmax": retmax,
        "retmode": "json",
        "usehistory": "y",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    result = data.get("esearchresult", {})
    return {
        "count": int(result.get("count", 0)),
        "ids": result.get("idlist", []),
        "query_key": result.get("querykey"),
        "web_env": result.get("webenv"),
    }


def fetch_gds_summaries(ids):
    """Fetch dataset summaries from NCBI."""
    if not ids:
        return []
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "gds",
        "id": ",".join(ids[:20]),
        "retmode": "json",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("result", {})
    summaries = []
    for gds_id in ids[:20]:
        if gds_id in results:
            entry = results[gds_id]
            summaries.append({
                "id": gds_id,
                "accession": entry.get("accession", ""),
                "title": entry.get("title", ""),
                "summary": entry.get("summary", "")[:300],
                "platform": entry.get("gpl", ""),
                "samples": entry.get("n_samples", 0),
                "organism": entry.get("taxon", ""),
                "type": entry.get("entrytype", ""),
                "pubmed_ids": entry.get("pubmedids", []),
            })
    return summaries


def search_metabolomics_workbench(query):
    """Search Metabolomics Workbench for diabetes-related studies."""
    url = "https://www.metabolomicsworkbench.org/rest/study/study_title"
    try:
        resp = requests.get(f"{url}/{query}/summary", timeout=30)
        if resp.status_code == 200:
            # MW returns tab-delimited text
            lines = resp.text.strip().split("\n")
            if len(lines) > 1:
                headers = lines[0].split("\t")
                studies = []
                for line in lines[1:]:
                    fields = line.split("\t")
                    study = dict(zip(headers, fields))
                    studies.append(study)
                return studies
        return []
    except Exception:
        return []


def search_pubmed_datasets(term, retmax=20):
    """Search PubMed for papers with associated datasets."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": f"{term} AND (dataset[tiab] OR repository[tiab] OR accession[tiab] OR supplementary[tiab])",
        "retmax": retmax,
        "retmode": "json",
        "sort": "relevance",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    result = resp.json().get("esearchresult", {})
    return {
        "count": int(result.get("count", 0)),
        "ids": result.get("idlist", []),
    }


def check_gmrepo_availability():
    """Check GMrepo database for diabetes-related gut microbiome data."""
    url = "https://gmrepo.humangut.info/api/getAssociatedPhenotypesByMeshID"
    try:
        # Check for diabetes phenotype
        resp = requests.post(url, json={"mesh_id": "D003920"}, timeout=15)  # D003920 = Diabetes Mellitus
        if resp.status_code == 200:
            data = resp.json()
            return {"available": True, "phenotypes": data if isinstance(data, list) else [data]}
        return {"available": False, "error": f"Status {resp.status_code}"}
    except Exception as e:
        return {"available": False, "error": str(e)}


def main():
    print("=" * 70)
    print("MICROBIOME ML PIPELINE — Phase 1: Data Acquisition & Cataloging")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("Inspired by: PMID 41921761 (oral-gut microbiome axis, AUC >0.83)")
    print("=" * 70)

    catalog = {
        "metadata": {
            "project": "Multi-Omic Microbiome ML Diagnostic Pipeline",
            "phase": "Phase 1 — Data Acquisition",
            "date": datetime.now().isoformat(),
            "reference_paper": "PMID 41921761",
        },
        "geo_datasets": {},
        "metabolomics_workbench": {},
        "pubmed_dataset_papers": {},
        "gmrepo": {},
        "public_resources": [],
    }

    # ── 1. Search GEO for microbiome + diabetes datasets ──
    geo_queries = [
        ("diabetes microbiome 16S", "Gut microbiome 16S studies in diabetes"),
        ("diabetes metagenome", "Shotgun metagenomics in diabetes"),
        ("type 1 diabetes gut microbiome", "T1D gut microbiome studies"),
        ("type 2 diabetes gut microbiome", "T2D gut microbiome studies"),
        ("gestational diabetes microbiome", "GDM microbiome studies"),
        ("diabetes oral microbiome", "Oral microbiome in diabetes"),
        ("diabetes metabolomics SCFA", "SCFA metabolomics in diabetes"),
        ("LADA autoimmune diabetes microbiome", "LADA microbiome studies"),
    ]

    print("\n[1/5] Searching NCBI GEO DataSets...")
    all_geo_ids = set()
    for query, label in geo_queries:
        print(f"  Query: {label}...")
        try:
            result = search_ncbi_gds(query, retmax=30)
            count = result["count"]
            ids = result["ids"]
            all_geo_ids.update(ids)
            catalog["geo_datasets"][label] = {
                "query": query,
                "total_results": count,
                "ids_retrieved": len(ids),
            }
            print(f"    Found {count} datasets ({len(ids)} retrieved)")
            time.sleep(0.4)
        except Exception as e:
            print(f"    Error: {e}")
            catalog["geo_datasets"][label] = {"query": query, "error": str(e)}

    # Fetch summaries for unique datasets
    print(f"\n  Fetching summaries for {len(all_geo_ids)} unique datasets...")
    geo_summaries = []
    id_list = list(all_geo_ids)
    for batch_start in range(0, len(id_list), 20):
        batch = id_list[batch_start:batch_start + 20]
        try:
            summaries = fetch_gds_summaries(batch)
            geo_summaries.extend(summaries)
            time.sleep(0.5)
        except Exception as e:
            print(f"    Batch error: {e}")

    catalog["geo_summaries"] = geo_summaries
    print(f"  Retrieved {len(geo_summaries)} dataset summaries")

    # ── 2. Search Metabolomics Workbench ──
    print("\n[2/5] Searching Metabolomics Workbench...")
    mw_queries = ["diabetes", "microbiome", "SCFA", "bile acid diabetes"]
    mw_studies = []
    for query in mw_queries:
        print(f"  Query: {query}...")
        try:
            studies = search_metabolomics_workbench(query)
            mw_studies.extend(studies)
            print(f"    Found {len(studies)} studies")
            time.sleep(0.5)
        except Exception as e:
            print(f"    Error: {e}")

    catalog["metabolomics_workbench"] = {
        "total_studies": len(mw_studies),
        "studies": mw_studies[:30],
    }

    # ── 3. Search PubMed for papers with deposited datasets ──
    print("\n[3/5] Searching PubMed for dataset-associated papers...")
    pubmed_queries = [
        ("gut microbiome diabetes prediction model", "ML prediction models"),
        ("oral microbiome type 2 diabetes", "Oral microbiome T2D"),
        ("multi-omics diabetes microbiome", "Multi-omics integration"),
        ("microbiome biomarker diabetes diagnosis", "Microbiome biomarkers"),
    ]

    for query, label in pubmed_queries:
        print(f"  Query: {label}...")
        try:
            result = search_pubmed_datasets(query, retmax=15)
            catalog["pubmed_dataset_papers"][label] = {
                "query": query,
                "total_results": result["count"],
                "pmids": result["ids"],
            }
            print(f"    Found {result['count']} papers ({len(result['ids'])} retrieved)")
            time.sleep(0.4)
        except Exception as e:
            print(f"    Error: {e}")

    # ── 4. Check GMrepo availability ──
    print("\n[4/5] Checking GMrepo database...")
    gmrepo_result = check_gmrepo_availability()
    catalog["gmrepo"] = gmrepo_result
    print(f"  GMrepo available: {gmrepo_result.get('available', False)}")

    # ── 5. Catalog known public resources ──
    print("\n[5/5] Cataloging known public resources...")
    catalog["public_resources"] = [
        {
            "name": "curatedMetagenomicData",
            "url": "https://bioconductor.org/packages/curatedMetagenomicData/",
            "description": "Curated metagenomic profiles from 50+ published studies, >20,000 samples",
            "access": "Free via Bioconductor (R) or Python wrapper",
            "relevance": "PRIMARY SOURCE — pre-harmonized taxonomic profiles with phenotype metadata",
            "diabetes_studies": "Multiple T1D and T2D studies included",
            "status": "Available — install via: BiocManager::install('curatedMetagenomicData')",
        },
        {
            "name": "Human Microbiome Project (HMP)",
            "url": "https://hmpdacc.org/",
            "description": "Reference human microbiome data from 4,788+ samples across body sites",
            "access": "Free via HMPDACC portal",
            "relevance": "Reference microbiomes for healthy controls; oral + gut paired data",
            "status": "Available",
        },
        {
            "name": "DIAGRAM Consortium",
            "url": "https://diagram-consortium.org/",
            "description": "T2D GWAS summary statistics from largest meta-analyses",
            "access": "Free download (summary statistics only)",
            "relevance": "Genomic layer for multi-omic integration; T2D risk variants",
            "status": "Available — download summary stats from consortium website",
        },
        {
            "name": "T1D Knowledge Portal",
            "url": "https://t1d.hugeamp.org/",
            "description": "T1D-specific GWAS, gene-level, and variant-level associations",
            "access": "Free web portal + bulk download",
            "relevance": "T1D genetic risk variants for multi-omic integration",
            "status": "Available",
        },
        {
            "name": "Metabolomics Workbench",
            "url": "https://www.metabolomicsworkbench.org/",
            "description": "National metabolomics data repository with SCFA, bile acid profiles",
            "access": "Free — REST API available",
            "relevance": "Metabolomic layer — SCFA profiles linked to microbiome composition",
            "status": "Available — queried in this scan",
        },
        {
            "name": "Human Metabolome Database (HMDB)",
            "url": "https://hmdb.ca/",
            "description": "Comprehensive metabolite reference database",
            "access": "Free download",
            "relevance": "Metabolite annotation and pathway mapping",
            "status": "Available",
        },
        {
            "name": "UK Biobank Proteomics",
            "url": "https://www.ukbiobank.ac.uk/",
            "description": "Olink proteomics on 50,000+ participants",
            "access": "Requires application (6-8 week approval)",
            "relevance": "Proteomic layer — inflammatory markers, gut barrier proteins",
            "status": "Application required",
        },
        {
            "name": "Gene Expression Omnibus (GEO)",
            "url": "https://www.ncbi.nlm.nih.gov/geo/",
            "description": "Transcriptomic datasets — gut epithelial gene expression",
            "access": "Free — queried in this scan",
            "relevance": "Transcriptomic layer for multi-omic integration",
            "status": "Available — queried in this scan",
        },
        {
            "name": "GMrepo",
            "url": "https://gmrepo.humangut.info/",
            "description": "Curated gut microbiome database with 58,000+ samples and phenotype data",
            "access": "Free — REST API available",
            "relevance": "Cross-population microbiome data with disease phenotypes",
            "status": f"Available: {gmrepo_result.get('available', 'Unknown')}",
        },
    ]

    for resource in catalog["public_resources"]:
        print(f"  {resource['name']}: {resource['status']}")

    # ── Save catalog ──
    output_path = RESULTS_DIR / "microbiome_ml_data_catalog.json"
    with open(output_path, "w") as f:
        json.dump(catalog, f, indent=2, default=str)

    # ── Summary ──
    total_geo = sum(v.get("total_results", 0) for v in catalog["geo_datasets"].values() if isinstance(v, dict) and "total_results" in v)
    total_mw = catalog["metabolomics_workbench"].get("total_studies", 0)
    total_pubmed = sum(v.get("total_results", 0) for v in catalog["pubmed_dataset_papers"].values() if isinstance(v, dict))
    total_resources = len(catalog["public_resources"])

    print("\n" + "=" * 70)
    print("PHASE 1 COMPLETE — Data Acquisition Catalog")
    print("=" * 70)
    print(f"GEO datasets found: {total_geo} (across {len(geo_queries)} queries)")
    print(f"GEO summaries retrieved: {len(geo_summaries)}")
    print(f"Metabolomics Workbench studies: {total_mw}")
    print(f"PubMed dataset papers: {total_pubmed}")
    print(f"Public resources cataloged: {total_resources}")
    print(f"\nOutput saved to: {output_path}")

    # Print top GEO datasets by sample count
    if geo_summaries:
        print(f"\nTop 10 GEO Datasets by Sample Count:")
        print("-" * 70)
        sorted_geo = sorted(geo_summaries, key=lambda x: int(x.get("samples", 0)) if str(x.get("samples", 0)).isdigit() else 0, reverse=True)
        for g in sorted_geo[:10]:
            samples = g.get("samples", "?")
            print(f"  {g['accession']:12s} | {str(samples):>6} samples | {g['title'][:50]}")

    print(f"\nNext step: Run project_microbiome_ml_phase2_features.py")
    print("  (Requires: pip install biom-format scikit-bio pandas)")


if __name__ == "__main__":
    main()
