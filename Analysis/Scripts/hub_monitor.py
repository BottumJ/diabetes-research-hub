"""
DIABETES RESEARCH HUB — File & Dataset Monitor
Scans the Research Hub folder tree for changes since last run.
Generates a change report and flags items needing review.

USAGE (PowerShell):
    python hub_monitor.py                  # Full scan
    python hub_monitor.py --quick          # Quick scan (modified files only)
    python hub_monitor.py --report-only    # Show last report without scanning

OUTPUT:
    ../Results/hub_monitor_state.json      (persistent state)
    ../Results/hub_monitor_report.md       (human-readable change report)
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HUB_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "Results")
STATE_FILE = os.path.join(RESULTS_DIR, "hub_monitor_state.json")
REPORT_FILE = os.path.join(RESULTS_DIR, "hub_monitor_report.md")

os.makedirs(RESULTS_DIR, exist_ok=True)

# File types we track
TRACKED_EXTENSIONS = {
    ".md", ".xlsx", ".html", ".json", ".py", ".csv", ".tsv",
    ".pdf", ".docx", ".ipynb", ".txt", ".yaml", ".yml",
}

# Folders to skip
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".skills", ".venv", "venv"}

def file_hash(filepath, block_size=65536):
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while True:
                block = f.read(block_size)
                if not block:
                    break
                h.update(block)
        return h.hexdigest()
    except (PermissionError, OSError):
        return "ERROR"

def scan_hub(root):
    """Walk the hub directory and collect file metadata."""
    files = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in TRACKED_EXTENSIONS:
                continue
            fpath = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(fpath, root)
            try:
                stat = os.stat(fpath)
                files[rel_path] = {
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "hash": file_hash(fpath),
                    "extension": ext,
                }
            except (PermissionError, OSError):
                pass
    return files

def load_state():
    """Load previous scan state."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_scan": None, "files": {}}

def save_state(state):
    """Persist current scan state."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def compute_changes(old_files, new_files):
    """Diff two file states."""
    old_set = set(old_files.keys())
    new_set = set(new_files.keys())

    added = sorted(new_set - old_set)
    removed = sorted(old_set - new_set)
    common = old_set & new_set

    modified = []
    unchanged = []
    for path in sorted(common):
        if old_files[path]["hash"] != new_files[path]["hash"]:
            modified.append(path)
        else:
            unchanged.append(path)

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged": unchanged,
    }

def generate_report(changes, new_files, old_state, scan_time):
    """Generate a human-readable change report."""
    lines = [
        "# Hub Monitor Report",
        f"**Scan time:** {scan_time}",
        f"**Previous scan:** {old_state.get('last_scan', 'Never')}",
        f"**Hub root:** `{HUB_ROOT}`",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total files tracked | {len(new_files)} |",
        f"| New files | {len(changes['added'])} |",
        f"| Modified files | {len(changes['modified'])} |",
        f"| Removed files | {len(changes['removed'])} |",
        f"| Unchanged files | {len(changes['unchanged'])} |",
        "",
    ]

    if changes["added"]:
        lines += ["## New Files", ""]
        for p in changes["added"]:
            sz = new_files[p]["size"]
            lines.append(f"- **{p}** ({_fmt_size(sz)})")
        lines.append("")

    if changes["modified"]:
        lines += ["## Modified Files", ""]
        for p in changes["modified"]:
            sz = new_files[p]["size"]
            lines.append(f"- **{p}** ({_fmt_size(sz)}, modified: {new_files[p]['modified']})")
        lines.append("")

    if changes["removed"]:
        lines += ["## Removed Files", ""]
        for p in changes["removed"]:
            lines.append(f"- ~~{p}~~")
        lines.append("")

    # File breakdown by type
    ext_counts = {}
    for p, meta in new_files.items():
        ext = meta["extension"]
        ext_counts[ext] = ext_counts.get(ext, 0) + 1

    lines += [
        "## File Inventory by Type",
        "",
        "| Extension | Count |",
        "|-----------|-------|",
    ]
    for ext, count in sorted(ext_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {ext} | {count} |")

    # Folder structure summary
    folder_counts = {}
    for p in new_files:
        folder = os.path.dirname(p) or "(root)"
        folder_counts[folder] = folder_counts.get(folder, 0) + 1

    lines += [
        "",
        "## Folder Inventory",
        "",
        "| Folder | Files |",
        "|--------|-------|",
    ]
    for folder, count in sorted(folder_counts.items()):
        lines.append(f"| {folder} | {count} |")

    # Review flags
    lines += [
        "",
        "## Review Flags",
        "",
    ]
    flags = []
    results_files = [p for p in new_files if "Results" in p]
    if not results_files:
        flags.append("No analysis results found. Run Project scripts to generate outputs.")
    stale_results = [p for p in results_files
                     if (datetime.now() - datetime.fromisoformat(new_files[p]["modified"])).days > 14]
    if stale_results:
        flags.append(f"{len(stale_results)} result file(s) older than 14 days — may need refresh.")
    tracker = [p for p in new_files if "Tracker" in p and p.endswith(".xlsx")]
    if not tracker:
        flags.append("Research Tracker spreadsheet not found.")
    doctrine = [p for p in new_files if "DOCTRINE" in p]
    if not doctrine:
        flags.append("Research Doctrine document not found.")

    if flags:
        for f in flags:
            lines.append(f"- {f}")
    else:
        lines.append("- All clear. No issues flagged.")

    lines += [
        "",
        "---",
        f"*Generated by hub_monitor.py — {scan_time}*",
    ]

    report = "\n".join(lines)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    return report

def _fmt_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def main():
    args = sys.argv[1:]
    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "--report-only" in args:
        if os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, "r") as f:
                print(f.read())
        else:
            print("No report found. Run a scan first.")
        return

    print(f"Scanning hub: {HUB_ROOT}")
    old_state = load_state()
    new_files = scan_hub(HUB_ROOT)

    changes = compute_changes(old_state.get("files", {}), new_files)

    report = generate_report(changes, new_files, old_state, scan_time)

    # Save new state
    save_state({"last_scan": scan_time, "files": new_files})

    # Run snapshot diff if snapshots exist
    snapshot_diff = diff_snapshots(RESULTS_DIR)
    if snapshot_diff:
        append_snapshot_diff_to_report(REPORT_FILE, snapshot_diff)

    # Print summary
    print(f"\nFiles tracked: {len(new_files)}")
    print(f"  Added:     {len(changes['added'])}")
    print(f"  Modified:  {len(changes['modified'])}")
    print(f"  Removed:   {len(changes['removed'])}")
    print(f"  Unchanged: {len(changes['unchanged'])}")
    print(f"\nReport saved: {REPORT_FILE}")
    print(f"State saved:  {STATE_FILE}")

    if changes["added"] or changes["modified"]:
        print("\n--- Changes Detected ---")
        for p in changes["added"]:
            print(f"  [NEW] {p}")
        for p in changes["modified"]:
            print(f"  [MOD] {p}")

    if snapshot_diff:
        print("\n--- Snapshot Diffs ---")
        for dtype, diff in snapshot_diff.items():
            print(f"  [{dtype}] +{diff['added']} new, -{diff['removed']} dropped, ~{diff['changed']} changed")


def diff_snapshots(results_dir):
    """Compare dated snapshot files to detect changes in clinical trials and PubMed data."""
    import glob
    diffs = {}

    for prefix in ["clinical_trials_snapshot", "pubmed_recent_snapshot"]:
        pattern = os.path.join(results_dir, f"{prefix}_*.json")
        snapshots = sorted(glob.glob(pattern))
        if len(snapshots) < 2:
            continue

        old_path, new_path = snapshots[-2], snapshots[-1]
        try:
            with open(old_path, "r", encoding="utf-8") as f:
                old_data = json.load(f)
            with open(new_path, "r", encoding="utf-8") as f:
                new_data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        dtype = "trials" if "trials" in prefix else "pubmed"

        if dtype == "trials" and "trials" in old_data and "trials" in new_data:
            old_ids = set(old_data["trials"].keys())
            new_ids = set(new_data["trials"].keys())
            added = new_ids - old_ids
            removed = old_ids - new_ids
            changed = []
            for nct in old_ids & new_ids:
                if old_data["trials"][nct].get("status") != new_data["trials"][nct].get("status"):
                    changed.append({
                        "id": nct,
                        "old_status": old_data["trials"][nct].get("status"),
                        "new_status": new_data["trials"][nct].get("status"),
                        "title": new_data["trials"][nct].get("title", "")[:80],
                    })
            results_posted = []
            for nct in old_ids & new_ids:
                if not old_data["trials"][nct].get("has_results") and new_data["trials"][nct].get("has_results"):
                    results_posted.append(nct)
            diffs["trials"] = {
                "old_file": os.path.basename(old_path),
                "new_file": os.path.basename(new_path),
                "added": len(added),
                "removed": len(removed),
                "changed": len(changed),
                "status_changes": changed,
                "results_posted": results_posted,
                "added_ids": sorted(added),
                "removed_ids": sorted(removed),
            }

        elif dtype == "pubmed" and "papers" in old_data and "papers" in new_data:
            old_ids = set(old_data["papers"].keys())
            new_ids = set(new_data["papers"].keys())
            added = new_ids - old_ids
            removed = old_ids - new_ids
            new_papers = []
            for pmid in sorted(added):
                p = new_data["papers"][pmid]
                new_papers.append({
                    "pmid": pmid,
                    "title": p.get("title", "")[:100],
                    "domains": p.get("domains", []),
                })
            diffs["pubmed"] = {
                "old_file": os.path.basename(old_path),
                "new_file": os.path.basename(new_path),
                "added": len(added),
                "removed": len(removed),
                "changed": 0,
                "new_papers": new_papers,
                "cross_domain": [p for p in new_papers if len(p["domains"]) > 1],
            }

    return diffs


def append_snapshot_diff_to_report(report_file, diffs):
    """Append snapshot diff section to the hub monitor report."""
    lines = ["\n## Snapshot Diffs (Automated)\n"]

    if "trials" in diffs:
        d = diffs["trials"]
        lines.append(f"### Clinical Trials ({d['old_file']} → {d['new_file']})")
        lines.append(f"- New trials: {d['added']}")
        lines.append(f"- Removed trials: {d['removed']}")
        lines.append(f"- Status changes: {d['changed']}")
        lines.append(f"- New results posted: {len(d['results_posted'])}")
        if d["status_changes"]:
            lines.append("\n**Status Changes:**")
            for sc in d["status_changes"]:
                lines.append(f"- {sc['id']}: {sc['old_status']} → {sc['new_status']} | {sc['title']}")
        if d["results_posted"]:
            lines.append("\n**New Results Posted:**")
            for nct in d["results_posted"]:
                lines.append(f"- {nct}")
        lines.append("")

    if "pubmed" in diffs:
        d = diffs["pubmed"]
        lines.append(f"### PubMed ({d['old_file']} → {d['new_file']})")
        lines.append(f"- New papers: {d['added']}")
        lines.append(f"- Dropped papers: {d['removed']}")
        if d["cross_domain"]:
            lines.append(f"\n**Cross-Domain New Papers ({len(d['cross_domain'])}):**")
            for p in d["cross_domain"]:
                lines.append(f"- [{p['pmid']}] {p['title']} — Domains: {', '.join(p['domains'])}")
        lines.append("")

    with open(report_file, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
