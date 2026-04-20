"""
BASELINE: PubMed Recent Publications Tracker
Pulls the most recent high-impact diabetes publications across all 35
research domains. Saves a snapshot so future runs can detect new papers.

USAGE (PowerShell):
    python baseline_pubmed_alerts.py

OUTPUT:
    ../Results/pubmed_recent_snapshot_YYYY-MM-DD.json
    ../Results/pubmed_recent_summary.md
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import os
import time
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "Results")
os.makedirs(RESULTS_DIR, exist_ok=True)

PUBMED_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
TODAY = datetime.now().strftime("%Y-%m-%d")
LOOKBACK_DAYS = 30

# High-priority alert queries (most likely to surface actionable findings)
ALERT_QUERIES = {
    "T1D Stem Cell Cure": '"type 1 diabetes" AND ("stem cell" OR islet) AND (transplant OR cure OR "insulin independence")',
    "T1D Immunotherapy": '"type 1 diabetes" AND (teplizumab OR baricitinib OR "CAR-T" OR "Treg" OR immunotherapy)',
    "T2D GLP-1 New": '("GLP-1" OR semaglutide OR tirzepatide OR retatrutide OR orforglipron) AND "type 2 diabetes" AND (trial OR results)',
    "T2D Remission": '"type 2 diabetes" AND (remission OR reversal) AND (trial OR study)',
    "Diabetes AI/ML": 'diabetes AND ("machine learning" OR "deep learning" OR "artificial intelligence") AND (prediction OR diagnosis)',
    "Diabetes Biomarker": 'diabetes AND (biomarker OR proteomics OR metabolomics) AND (novel OR discovery)',
    "Diabetes Microbiome": 'diabetes AND (microbiome OR "gut microbiota") AND (mechanism OR therapy OR intervention)',
    "Diabetes Gene Therapy": 'diabetes AND ("gene therapy" OR "gene editing" OR CRISPR)',
    "Closed Loop AP": '("closed loop" OR "artificial pancreas") AND diabetes AND (trial OR outcome)',
    "Diabetes Drug Repurpose": 'diabetes AND ("drug repurposing" OR "drug repositioning") AND (computational OR network OR screening)',
    "Diabetes Epigenetics": 'diabetes AND (epigenetic OR methylation) AND (GWAS OR "genome-wide")',
    "Diabetes Complications New": '("diabetic nephropathy" OR "diabetic retinopathy") AND (novel OR "new treatment" OR breakthrough)',
    "Diabetes Health Equity": 'diabetes AND ("health equity" OR disparity) AND (technology OR access OR CGM)',
    "LADA New Research": '("latent autoimmune diabetes" OR LADA) AND (diagnosis OR treatment)',
    "Diabetes Multi-Omics": 'diabetes AND ("multi-omics" OR "multiomics") AND (integration OR analysis)',
    # Added 2026-04-17: GLP-1 pharmacogenomics domain (Stanford PAM variant discovery)
    "GLP-1 Pharmacogenomics": 'diabetes AND ("GLP-1" OR "glucagon-like peptide") AND (pharmacogenomics OR "genetic variant" OR "drug response" OR PAM OR "peptidyl-glycine") AND (resistance OR response OR polymorphism)',
}

# Key therapies to track across ALL domains via abstract matching.
# These are searched separately because title-only matching misses them.
# Added 2026-04-17 per monitor report recommendation.
KEY_THERAPY_TERMS = [
    "zimislecel",
    "orforglipron",
    "retatrutide",
    "CagriSema",
    "baricitinib",
    "teplizumab",
    "icodec",        # Awiqli / insulin icodec
    "dapagliflozin",  # generic now approved
]

def search_pubmed(query, max_results=10, days_back=LOOKBACK_DAYS):
    """Search PubMed for recent papers matching query."""
    min_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y/%m/%d")
    max_date = datetime.now().strftime("%Y/%m/%d")

    params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "sort": "date",
        "datetype": "pdat",
        "mindate": min_date,
        "maxdate": max_date,
    })

    try:
        url = f"{PUBMED_SEARCH}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "DiabetesResearchHub/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read().decode("utf-8")
        root = ET.fromstring(xml_data)

        id_list = root.find("IdList")
        if id_list is None:
            return [], 0
        pmids = [id_el.text for id_el in id_list.findall("Id")]
        count = int(root.find("Count").text) if root.find("Count") is not None else 0
        return pmids, count
    except Exception as e:
        print(f"    [WARN] Search failed: {e}")
        return [], 0

def fetch_paper_details(pmids):
    """Fetch paper metadata from PubMed."""
    if not pmids:
        return []

    params = urllib.parse.urlencode({
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    })

    try:
        url = f"{PUBMED_FETCH}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "DiabetesResearchHub/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            xml_data = resp.read().decode("utf-8")
        root = ET.fromstring(xml_data)

        papers = []
        for article in root.findall(".//PubmedArticle"):
            medline = article.find("MedlineCitation")
            if medline is None:
                continue

            art = medline.find("Article")
            if art is None:
                continue

            pmid = medline.find("PMID")
            pmid_text = pmid.text if pmid is not None else ""

            title_el = art.find("ArticleTitle")
            title = title_el.text if title_el is not None else "No title"

            # Journal
            journal_el = art.find(".//Journal/Title")
            journal = journal_el.text if journal_el is not None else ""

            # Publication date
            pub_date_el = art.find(".//PubDate")
            if pub_date_el is not None:
                year = pub_date_el.find("Year")
                month = pub_date_el.find("Month")
                day = pub_date_el.find("Day")
                date_str = ""
                if year is not None:
                    date_str = year.text
                if month is not None:
                    date_str += f"-{month.text}"
                if day is not None:
                    date_str += f"-{day.text}"
            else:
                date_str = ""

            # Abstract
            abstract_el = art.find(".//Abstract/AbstractText")
            abstract = abstract_el.text if abstract_el is not None else ""
            if abstract and len(abstract) > 300:
                abstract = abstract[:300] + "..."

            # Authors (first 3)
            authors = []
            for author in art.findall(".//AuthorList/Author")[:3]:
                last = author.find("LastName")
                init = author.find("Initials")
                if last is not None:
                    name = last.text
                    if init is not None:
                        name += f" {init.text}"
                    authors.append(name)

            # DOI
            doi = ""
            for eid in art.findall(".//ELocationID"):
                if eid.get("EIdType") == "doi":
                    doi = eid.text
                    break

            papers.append({
                "pmid": pmid_text,
                "title": title,
                "journal": journal,
                "date": date_str,
                "authors": "; ".join(authors),
                "abstract_snippet": abstract,
                "doi": doi,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid_text}/",
            })

        return papers
    except Exception as e:
        print(f"    [WARN] Fetch failed: {e}")
        return []

def main():
    print("=" * 60)
    print("BASELINE: PubMed Recent Publications Tracker")
    print(f"Date: {TODAY}")
    print(f"Lookback: {LOOKBACK_DAYS} days")
    print(f"Alert queries: {len(ALERT_QUERIES)}")
    print("=" * 60)

    all_papers = {}
    domain_results = {}

    for domain, query in ALERT_QUERIES.items():
        print(f"\n  [{domain}]")
        pmids, total_count = search_pubmed(query)
        print(f"    Total in last {LOOKBACK_DAYS} days: {total_count}")
        print(f"    Fetching top {len(pmids)} details...")
        time.sleep(0.4)

        papers = fetch_paper_details(pmids)
        time.sleep(0.4)

        domain_results[domain] = {
            "total_count": total_count,
            "papers": papers,
        }

        for p in papers:
            if p["pmid"] not in all_papers:
                all_papers[p["pmid"]] = {**p, "domains": [domain]}
            else:
                all_papers[p["pmid"]]["domains"].append(domain)

        if papers:
            print(f"    Latest: {papers[0]['title'][:70]}...")

    # Key Therapy Abstract Search (added 2026-04-17)
    therapy_hits = {}
    if KEY_THERAPY_TERMS:
        print(f"\n  [Key Therapy Abstract Search]")
        for therapy in KEY_THERAPY_TERMS:
            query = f'diabetes AND {therapy}'
            pmids, count = search_pubmed(query, max_results=5, days_back=LOOKBACK_DAYS)
            time.sleep(0.4)
            if pmids:
                papers = fetch_paper_details(pmids)
                time.sleep(0.4)
                therapy_hits[therapy] = {
                    "total_count": count,
                    "papers": papers,
                }
                for p in papers:
                    tag = f"Key Therapy: {therapy}"
                    if p["pmid"] not in all_papers:
                        all_papers[p["pmid"]] = {**p, "domains": [tag]}
                    elif tag not in all_papers[p["pmid"]]["domains"]:
                        all_papers[p["pmid"]]["domains"].append(tag)
                print(f"    {therapy}: {count} papers (fetched {len(papers)})")
            else:
                therapy_hits[therapy] = {"total_count": count, "papers": []}
                print(f"    {therapy}: {count} papers")

    # Save JSON snapshot
    snapshot = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "source": "PubMed E-utilities",
            "lookback_days": LOOKBACK_DAYS,
            "total_unique_papers": len(all_papers),
            "domains_queried": len(ALERT_QUERIES),
            "key_therapies_tracked": len(KEY_THERAPY_TERMS),
        },
        "domain_results": {k: {"total_count": v["total_count"], "paper_count": len(v["papers"])}
                           for k, v in domain_results.items()},
        "therapy_hits": {k: {"total_count": v["total_count"], "paper_count": len(v["papers"])}
                         for k, v in therapy_hits.items()} if therapy_hits else {},
        "papers": all_papers,
    }

    json_path = os.path.join(RESULTS_DIR, f"pubmed_recent_snapshot_{TODAY}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, default=str)
    print(f"\n  Saved: {json_path}")

    latest_path = os.path.join(RESULTS_DIR, "pubmed_recent_latest.json")
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, default=str)

    # Generate summary report
    lines = [
        "# PubMed Recent Publications Report",
        f"**Generated:** {TODAY}",
        f"**Lookback period:** {LOOKBACK_DAYS} days",
        f"**Unique papers found:** {len(all_papers)}",
        "",
        "---",
        "",
        "## Publication Volume by Domain (Last 30 Days)",
        "",
        "| Domain | Total Papers | Trend Signal |",
        "|--------|-------------|--------------|",
    ]
    for domain, res in sorted(domain_results.items(), key=lambda x: -x[1]["total_count"]):
        count = res["total_count"]
        signal = "HIGH ACTIVITY" if count > 50 else "ACTIVE" if count > 10 else "LOW" if count > 0 else "NONE"
        lines.append(f"| {domain} | {count} | {signal} |")

    lines += [
        "",
        "---",
        "",
        "## Most Recent Papers by Domain",
        "",
    ]

    for domain, res in domain_results.items():
        if not res["papers"]:
            continue
        lines.append(f"### {domain}")
        lines.append("")
        for p in res["papers"][:5]:
            lines.append(f"- **{p['title']}**")
            lines.append(f"  {p['journal']} ({p['date']}) | {p['authors']}")
            lines.append(f"  [PubMed]({p['url']})" + (f" | [DOI](https://doi.org/{p['doi']})" if p['doi'] else ""))
            lines.append("")

    # Key therapy mentions section
    if therapy_hits:
        lines += [
            "---",
            "",
            "## Key Therapy Mentions (Abstract Search)",
            "",
            "These therapies are tracked by name across all PubMed abstracts (not just titles).",
            "",
            "| Therapy | Papers (30d) | Status |",
            "|---------|-------------|--------|",
        ]
        for therapy, res in sorted(therapy_hits.items(), key=lambda x: -x[1]["total_count"]):
            count = res["total_count"]
            status = "ACTIVE" if count > 5 else "LOW" if count > 0 else "NONE"
            lines.append(f"| {therapy} | {count} | {status} |")
        lines.append("")
        for therapy, res in therapy_hits.items():
            if res["papers"]:
                lines.append(f"### {therapy}")
                lines.append("")
                for p in res["papers"][:3]:
                    lines.append(f"- **{p['title']}**")
                    lines.append(f"  {p['journal']} ({p['date']}) | {p['authors']}")
                    lines.append(f"  [PubMed]({p['url']})" + (f" | [DOI](https://doi.org/{p['doi']})" if p['doi'] else ""))
                    lines.append("")

    # Cross-domain papers (appear in multiple alerts)
    cross_domain = {k: v for k, v in all_papers.items() if len(v.get("domains", [])) > 1}
    if cross_domain:
        lines += [
            "---",
            "",
            "## Cross-Domain Papers (Appear in Multiple Alerts)",
            "",
            "These papers span multiple research domains -- potentially high-value for synthesis.",
            "",
        ]
        for pmid, p in sorted(cross_domain.items(), key=lambda x: -len(x[1]["domains"])):
            domains_str = ", ".join(p["domains"])
            lines.append(f"- **{p['title']}**")
            lines.append(f"  Domains: {domains_str}")
            lines.append(f"  [PubMed]({p['url']})")
            lines.append("")

    lines += [
        "---",
        f"*Generated by baseline_pubmed_alerts.py -- {TODAY}*",
    ]

    md_path = os.path.join(RESULTS_DIR, "pubmed_recent_summary.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Saved: {md_path}")

    print(f"\n{'='*60}")
    print("COMPLETE")
    print(f"{'='*60}")
    print(f"  Unique papers: {len(all_papers)}")
    print(f"  Cross-domain:  {len(cross_domain)}")
    print(f"  Domains with HIGH activity:")
    for d, r in sorted(domain_results.items(), key=lambda x: -x[1]["total_count"])[:5]:
        print(f"    {d}: {r['total_count']}")

if __name__ == "__main__":
    main()
