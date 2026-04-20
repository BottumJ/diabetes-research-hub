# Scheduled Data-Pull Report — 2026-04-20

**Status:** FAILED — execution environment unavailable

## What happened

The daily data-pull scheduled task (`diabetes-data-pull`) was triggered but could not execute any of the three Python scripts. The Linux shell sandbox that runs the scripts returned a persistent infrastructure error on every invocation:

```
bash failed on resume, create, and re-resume.
useradd: /etc/passwd.XXXXX: No space left on device
useradd: cannot lock /etc/passwd; try again later.
```

This means the sandbox itself could not initialize a user session — not a script-level error. I retried several times across the session; every attempt failed identically.

## What did NOT run

None of the three scripts executed:

| # | Script | Status |
|---|---|---|
| 1 | `baseline_clinical_trials.py` | Not run — sandbox unavailable |
| 2 | `baseline_pubmed_alerts.py` | Not run — sandbox unavailable |
| 3 | `hub_monitor.py` | Not run — sandbox unavailable |

## Output file verification

Checked for the expected "latest" output files in `Analysis/Results/`:

| File | Present? |
|---|---|
| clinical_trials_latest.json | Not found |
| clinical_trials_summary.md | Not found |
| pubmed_recent_latest.json | Not found |
| pubmed_recent_summary.md | Not found |
| hub_monitor_report.md | Not found |
| hub_monitor_state.json | Not found |

Note: date-stamped snapshot files from earlier runs are still present (most recent dated snapshots: `clinical_trials_snapshot_2026-03-16.json`, `pubmed_recent_snapshot_2026-03-16.json`, `monitor_report_2026-03-16.md`). No "latest"-named canonical files were found, so the review scan will not have fresh data today.

## Counts

- Total trials pulled today: **0**
- Total papers pulled today: **0**

## Workspace confirmation

- Workspace folder `Diabetes_Research` — confirmed present
- Scripts directory `Analysis/Scripts/` — confirmed present, all three target scripts exist at expected paths
- Results directory `Analysis/Results/` — confirmed present

## Needs attention

The scheduled task cannot proceed until the sandbox is healthy. Recommended next steps for the user:

1. Re-run the task manually once the sandbox is back up, or
2. Run the three scripts locally from a terminal:
   ```
   cd Diabetes_Research/Analysis/Scripts
   python baseline_clinical_trials.py
   python baseline_pubmed_alerts.py
   python hub_monitor.py
   ```
3. If the sandbox error persists across sessions, this is an infrastructure issue (disk full on the Cowork execution host) — report via the thumbs-down feedback in the UI.

No retries were attempted from within this scheduled run, per the task instructions.
