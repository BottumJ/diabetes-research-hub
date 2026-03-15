"""
BASELINE: Clinical Trial Snapshot
Pulls all active diabetes clinical trials from ClinicalTrials.gov API v2.
Saves a timestamped snapshot so future runs can detect new trials,
status changes, and newly posted results.

USAGE (PowerShell):
    python baseline_clinical_trials.py

OUTPUT:
    ../Results/clinical_trials_snapshot_YYYY-MM-DD.json
    ../Results/clinical_trials_summary.md
"""

import urllib.request
import json
import os
import time
from datetime import datetime
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "Results")
os.makedirs(RESULTS_DIR, exist_ok=True)

API_BASE = "https://clinicaltrials.gov/api/v2/studies"
PAGE_SIZE = 100
TODAY = datetime.now().strftime("%Y-%m-%d")

# We pull trials that are actively relevant — not ancient completed ones
QUERIES = [
    {
        "label": "T1D Cure & Cell Therapy",
        "filter": 'AREA[Condition](type 1 diabetes) AND AREA[InterventionType](BIOLOGICAL OR DEVICE) AND AREA[OverallStatus](RECRUITING OR NOT_YET_RECRUITING OR ACTIVE_NOT_RECRUITING OR ENROLLING_BY_INVITATION)',
    },
    {
        "label": "T1D Immunotherapy & Prevention",
        "filter": 'AREA[Condition](type 1 diabetes) AND AREA[InterventionType](DRUG) AND AREA[Phase](PHASE3 OR PHASE2) AND AREA[OverallStatus](RECRUITING OR NOT_YET_RECRUITING OR ACTIVE_NOT_RECRUITING)',
    },
    {
        "label": "T2D Novel Therapies (Phase 2-3)",
        "filter": 'AREA[Condition](type 2 diabetes) AND AREA[Phase](PHASE3 OR PHASE2) AND AREA[OverallStatus](RECRUITING OR NOT_YET_RECRUITING OR ACTIVE_NOT_RECRUITING) AND AREA[StudyFirstPostDate]RANGE[2023-01-01, MAX]',
    },
    {
        "label": "Diabetes Technology (Devices)",
        "filter": 'AREA[Condition](diabetes) AND AREA[InterventionType](DEVICE) AND AREA[Phase](NA) AND AREA[OverallStatus](RECRUITING OR NOT_YET_RECRUITING OR ACTIVE_NOT_RECRUITING) AND AREA[StudyFirstPostDate]RANGE[2023-01-01, MAX]',
    },
    {
        "label": "Diabetes Recently Completed with Results",
        "filter": 'AREA[Condition](diabetes) AND AREA[OverallStatus](COMPLETED) AND AREA[ResultsFirstPostDate]RANGE[2025-01-01, MAX]',
    },
]

def fetch_trials(query_filter, max_pages=10):
    """Fetch trials from ClinicalTrials.gov API v2."""
    trials = []
    next_token = None

    for page in range(max_pages):
        params = {
            "format": "json",
            "pageSize": PAGE_SIZE,
            "filter.advanced": query_filter,
            "fields": "NCTId,BriefTitle,OverallStatus,Phase,EnrollmentCount,"
                      "StartDate,CompletionDate,LeadSponsorName,InterventionName,"
                      "InterventionType,StudyFirstPostDate,ResultsFirstPostDate,"
                      "Condition,StudyType",
        }
        if next_token:
            params["pageToken"] = next_token

        url = f"{API_BASE}?{'&'.join(f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items())}"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "DiabetesResearchHub/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            studies = data.get("studies", [])
            for study in studies:
                proto = study.get("protocolSection", {})
                ident = proto.get("identificationModule", {})
                status = proto.get("statusModule", {})
                design = proto.get("designModule", {})
                sponsor = proto.get("sponsorCollaboratorsModule", {})
                interventions = proto.get("armsInterventionsModule", {})
                conditions = proto.get("conditionsModule", {})
                results_sec = study.get("resultsSection")

                # Extract intervention names
                intv_list = interventions.get("interventions", [])
                intv_names = [i.get("name", "") for i in intv_list]
                intv_types = [i.get("type", "") for i in intv_list]

                # Extract phases
                phases = design.get("phases", [])

                # Extract lead sponsor
                lead = sponsor.get("leadSponsor", {})

                trial = {
                    "nct_id": ident.get("nctId", ""),
                    "title": ident.get("briefTitle", ""),
                    "status": status.get("overallStatus", ""),
                    "phase": ", ".join(phases) if phases else "N/A",
                    "enrollment": design.get("enrollmentInfo", {}).get("count", ""),
                    "start_date": status.get("startDateStruct", {}).get("date", ""),
                    "completion_date": status.get("completionDateStruct", {}).get("date", ""),
                    "sponsor": lead.get("name", ""),
                    "interventions": "; ".join(intv_names[:3]),
                    "intervention_types": "; ".join(set(intv_types)),
                    "conditions": ", ".join(conditions.get("conditions", [])[:3]),
                    "first_posted": status.get("studyFirstPostDateStruct", {}).get("date", ""),
                    "results_posted": status.get("resultsFirstPostDateStruct", {}).get("date", ""),
                    "has_results": results_sec is not None,
                }
                trials.append(trial)

            next_token = data.get("nextPageToken")
            if not next_token or not studies:
                break
            time.sleep(0.5)

        except Exception as e:
            print(f"    [WARN] API error on page {page+1}: {e}")
            break

    return trials

import urllib.parse

def main():
    print("=" * 60)
    print("BASELINE: Clinical Trial Snapshot")
    print(f"Date: {TODAY}")
    print("=" * 60)

    all_trials = {}
    category_counts = {}

    for q in QUERIES:
        print(f"\n  Querying: {q['label']}...")
        trials = fetch_trials(q["filter"])
        print(f"    Found: {len(trials)} trials")
        category_counts[q["label"]] = len(trials)
        for t in trials:
            all_trials[t["nct_id"]] = {**t, "category": q["label"]}

    print(f"\n  Total unique trials: {len(all_trials)}")

    # ── Save JSON snapshot ──
    snapshot = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "source": "ClinicalTrials.gov API v2",
            "total_trials": len(all_trials),
            "category_counts": category_counts,
        },
        "trials": all_trials,
    }

    json_path = os.path.join(RESULTS_DIR, f"clinical_trials_snapshot_{TODAY}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
    print(f"\n  Saved: {json_path}")

    # Also save as "latest" for easy diffing
    latest_path = os.path.join(RESULTS_DIR, "clinical_trials_latest.json")
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    # ── Generate summary report ──
    status_counts = Counter(t["status"] for t in all_trials.values())
    phase_counts = Counter(t["phase"] for t in all_trials.values())
    sponsor_counts = Counter(t["sponsor"] for t in all_trials.values())
    top_sponsors = sponsor_counts.most_common(15)
    with_results = [t for t in all_trials.values() if t["has_results"]]

    lines = [
        "# Clinical Trial Snapshot Report",
        f"**Generated:** {TODAY}",
        f"**Source:** ClinicalTrials.gov API v2",
        f"**Total unique trials:** {len(all_trials)}",
        "",
        "---",
        "",
        "## Trials by Category",
        "",
        "| Category | Count |",
        "|----------|-------|",
    ]
    for cat, count in category_counts.items():
        lines.append(f"| {cat} | {count} |")

    lines += [
        "",
        "## Trials by Status",
        "",
        "| Status | Count |",
        "|--------|-------|",
    ]
    for status, count in status_counts.most_common():
        lines.append(f"| {status} | {count} |")

    lines += [
        "",
        "## Trials by Phase",
        "",
        "| Phase | Count |",
        "|-------|-------|",
    ]
    for phase, count in phase_counts.most_common():
        lines.append(f"| {phase} | {count} |")

    lines += [
        "",
        "## Top 15 Sponsors",
        "",
        "| Sponsor | Trials |",
        "|---------|--------|",
    ]
    for sponsor, count in top_sponsors:
        lines.append(f"| {sponsor} | {count} |")

    if with_results:
        lines += [
            "",
            "## Trials with Recently Posted Results (2025+)",
            "",
            "| NCT ID | Title | Sponsor | Results Posted |",
            "|--------|-------|---------|----------------|",
        ]
        for t in sorted(with_results, key=lambda x: x.get("results_posted", ""), reverse=True)[:30]:
            lines.append(f"| {t['nct_id']} | {t['title'][:60]}{'...' if len(t['title'])>60 else ''} | {t['sponsor'][:30]} | {t['results_posted']} |")

    lines += [
        "",
        "---",
        "",
        "## Notable Trials to Watch",
        "",
        "*(Manually curated after review — add entries here as you identify key trials)*",
        "",
        "| NCT ID | Name | Why It Matters |",
        "|--------|------|----------------|",
        "| | | |",
        "",
        "---",
        f"*Generated by baseline_clinical_trials.py — {TODAY}*",
    ]

    md_path = os.path.join(RESULTS_DIR, "clinical_trials_summary.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Saved: {md_path}")

    # ── Print highlights ──
    print(f"\n{'='*60}")
    print("SNAPSHOT COMPLETE")
    print(f"{'='*60}")
    print(f"  Unique trials: {len(all_trials)}")
    print(f"  With results:  {len(with_results)}")
    print(f"  By status:")
    for s, c in status_counts.most_common():
        print(f"    {s}: {c}")
    print(f"\n  Top sponsors:")
    for s, c in top_sponsors[:5]:
        print(f"    {s}: {c}")

if __name__ == "__main__":
    main()
