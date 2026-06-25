#!/usr/bin/env python3
"""
resolve_predictions.py - Science arm: lock, resolve, and score the prediction ledger.

This is the closed-loop scorer described in SCIENCE_ARM_BUILD_CHARTER.md (sec 4).
It rides the daily clinical-trial snapshot (clinical_trials_latest.json) that the
surveillance arm already produces. When a tracked trial's results post, this flags
it for resolution; once an outcome is recorded it computes the Brier component,
the running mean Brier score, and a calibration table.

It NEVER auto-decides whether a claim was TRUE or FALSE. A posted result only means
"go read the readout and record the outcome." Endpoint judgement is the analyst's.

USAGE
  # Daily / on each run: detect trials whose results have posted since last scan
  python resolve_predictions.py                 # scan + report (no writes to outcomes)
  python resolve_predictions.py --report-only    # just print current standings

  # Pre-registration: lock a prediction BEFORE its readout (charter sec 5)
  python resolve_predictions.py --lock PRED-2026-001 --date 2026-06-24

  # Resolution: record the real-world outcome after reading the posted result
  python resolve_predictions.py --resolve PRED-2026-001 --outcome TRUE
  python resolve_predictions.py --resolve PRED-2026-001 --outcome FALSE --date 2027-03-01
  #   --outcome accepts TRUE | FALSE | PARTIAL (PARTIAL is recorded but not Brier-scored)

Exit codes: 0 ok; 2 = a locked trial has posted results and awaits resolution (CI signal).

Paths are resolved relative to this file (Analysis/Scripts/), matching the rest of the hub.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent          # Analysis/Scripts
RESULTS_DIR = SCRIPT_DIR.parent / "Results"           # Analysis/Results
LEDGER = RESULTS_DIR / "prediction_ledger.json"
SNAPSHOT = RESULTS_DIR / "clinical_trials_latest.json"
REPORT = RESULTS_DIR / "prediction_ledger_report.md"

VALID_OUTCOMES = {"TRUE": 1.0, "FALSE": 0.0, "PARTIAL": None}


# --------------------------------------------------------------------------- IO
def load_ledger() -> dict:
    if not LEDGER.exists():
        sys.exit(f"ERROR: ledger not found at {LEDGER}")
    with open(LEDGER, encoding="utf-8") as f:
        return json.load(f)


def save_ledger(led: dict) -> None:
    # Back up before every write - the ledger is the system of record.
    if LEDGER.exists():
        stamp = datetime.now().strftime("%Y-%m-%d")
        shutil.copy2(LEDGER, LEDGER.with_suffix(f".json.bak_{stamp}"))
    led["metadata"]["last_updated"] = date.today().isoformat()
    # ATOMIC WRITE: serialize fully to a temp file in the same directory, flush+fsync,
    # then os.replace() to swap it in. On a sync'd folder (OneDrive/Dropbox) a reader
    # never sees a half-written file - the swap is atomic on the same filesystem.
    # (Direct json.dump to the live file caused partial-file corruption when OneDrive
    # read mid-write.) Validate the serialized text before the swap so a bug can never
    # replace a good ledger with broken JSON.
    import os, tempfile
    payload = json.dumps(led, indent=2)
    json.loads(payload)  # self-check: refuse to write invalid JSON
    fd, tmp = tempfile.mkstemp(dir=str(LEDGER.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, LEDGER)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def load_snapshot_results() -> dict:
    """Return {nct_id: {'results_posted': str, 'has_results': bool, 'status': str}}."""
    if not SNAPSHOT.exists():
        print(f"  [warn] snapshot not found at {SNAPSHOT}; cannot check readouts.")
        return {}
    with open(SNAPSHOT, encoding="utf-8") as f:
        data = json.load(f)
    trials = data.get("trials", {})
    out = {}
    # trials is a dict keyed by NCT id in this hub; tolerate a list too.
    items = trials.items() if isinstance(trials, dict) else (
        (t.get("nct_id"), t) for t in trials)
    for nct, t in items:
        if not nct:
            continue
        out[nct] = {
            "results_posted": (t.get("results_posted") or "").strip(),
            "has_results": bool(t.get("has_results")),
            "status": t.get("status", ""),
            "title": t.get("title", ""),
        }
    return out


def find(led: dict, pid: str) -> dict:
    for p in led["predictions"]:
        if p["prediction_id"] == pid:
            return p
    sys.exit(f"ERROR: prediction {pid} not found in ledger.")


# ----------------------------------------------------------------------- SCORING
def recompute_summary(led: dict) -> dict:
    preds = led["predictions"]
    locked = [p for p in preds if p.get("locked_date")]
    # Only locked + TRUE/FALSE predictions are Brier-scored. PARTIAL is excluded.
    scored = [p for p in preds
              if p.get("resolution") in ("TRUE", "FALSE")
              and p.get("locked_date")
              and p.get("brier_component") is not None]

    mean_brier = round(sum(p["brier_component"] for p in scored) / len(scored), 4) \
        if scored else None

    # Calibration: bin predicted probability, compare to observed frequency of TRUE.
    bins = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0001)]
    cal = []
    for lo, hi in bins:
        members = [p for p in scored if lo <= p["probability"] < hi]
        if not members:
            continue
        observed = sum(1 for p in members if p["resolution"] == "TRUE") / len(members)
        cal.append({
            "bin": f"{lo:.1f}-{min(hi,1.0):.1f}",
            "n": len(members),
            "mean_predicted": round(sum(p["probability"] for p in members) / len(members), 3),
            "observed_frequency": round(observed, 3),
        })

    summary = {
        "n_total": len(preds),
        "n_locked": len(locked),
        "n_resolved": len([p for p in preds if p.get("resolution")]),
        "n_scored": len(scored),
        "mean_brier": mean_brier,
        "calibration_bins": cal,
        "note": ("No predictions scored yet (need locked + resolved TRUE/FALSE)."
                 if not scored else
                 "Lower mean Brier is better. Reference: always-0.5 guessing = 0.25; "
                 "perfect = 0.0. Calibration: mean_predicted should track observed_frequency."),
    }
    led["scoring_summary"] = summary
    return summary


# ------------------------------------------------------------------------ ACTIONS
def do_lock(led: dict, pid: str, when: str) -> None:
    p = find(led, pid)
    if p.get("locked_date"):
        print(f"  {pid} already locked on {p['locked_date']}; no change.")
        return
    if p.get("resolution"):
        sys.exit(f"REFUSED: {pid} already has a resolution; locking now would be "
                 f"post-hoc and void (charter sec 5).")
    p["locked_date"] = when
    print(f"  LOCKED {pid} as of {when} "
          f"(prob={p['probability']}, '{p['claim'][:60]}...').")


def do_resolve(led: dict, pid: str, outcome: str, when: str,
               snap: dict, source: str | None, allow_no_results: bool) -> None:
    p = find(led, pid)
    outcome = outcome.upper()
    if outcome not in VALID_OUTCOMES:
        sys.exit(f"ERROR: --outcome must be one of {sorted(VALID_OUTCOMES)}.")
    if not p.get("locked_date"):
        sys.exit(f"REFUSED: {pid} was never locked. An unlocked prediction is not "
                 f"pre-registered and cannot be scored (charter sec 5). Lock it first "
                 f"only if no readout has occurred.")
    # PROVENANCE GUARD: a resolution must trace to a real readout (charter sec 5).
    # Check the daily snapshot; if the trial shows no posted results, refuse unless
    # the analyst supplies a --source (e.g. a topline press release that precedes
    # registry posting) or explicitly overrides with --allow-no-results.
    s = snap.get(p["nct_id"]) if snap else None
    has_results = bool(s and (s["has_results"] or s["results_posted"]))
    if not has_results and not source and not allow_no_results:
        sys.exit(
            f"REFUSED: {p['nct_id']} shows NO posted results in the latest snapshot "
            f"(has_results=false). Resolving now would record an outcome with no "
            f"provenance -- the exact failure the ledger exists to prevent (charter sec 5).\n"
            f"  If a real readout exists (e.g. a company topline press release before "
            f"registry posting), re-run with:\n"
            f"     --resolve {pid} --outcome {outcome} --source \"<URL or citation>\"\n"
            f"  To override deliberately (not recommended), add --allow-no-results.")
    if not source and not has_results:
        source = "OVERRIDE: --allow-no-results (no registry results, no source cited)"
    if p.get("resolution"):
        print(f"  [warn] {pid} already resolved as {p['resolution']}; overwriting.")
    p["resolution"] = outcome
    p["resolved_date"] = when
    p["resolution_source"] = source or f"snapshot: {p['nct_id']} has_results=true ({when})"
    val = VALID_OUTCOMES[outcome]
    if val is None:
        p["brier_component"] = None
        print(f"  RESOLVED {pid} = PARTIAL (recorded, not Brier-scored).")
    else:
        p["brier_component"] = round((p["probability"] - val) ** 2, 4)
        print(f"  RESOLVED {pid} = {outcome}. "
              f"Brier component = ({p['probability']} - {val:.0f})^2 = {p['brier_component']}.")
    print(f"  provenance: {p['resolution_source']}")


def do_unresolve(led: dict, pid: str) -> None:
    """Void a resolution (e.g. one recorded in error / for a test). The lock stays."""
    p = find(led, pid)
    if not p.get("resolution"):
        print(f"  {pid} has no resolution to void; no change.")
        return
    prev = p.get("resolution")
    p["resolution"] = None
    p["resolved_date"] = None
    p["brier_component"] = None
    p["resolution_source"] = None
    print(f"  UNRESOLVED {pid} (was {prev}). Lock preserved; removed from scoring.")


def scan_readouts(led: dict, snap: dict) -> list:
    """Flag locked, unresolved predictions whose trial now has posted results."""
    flagged = []
    for p in led["predictions"]:
        s = snap.get(p["nct_id"])
        posted = bool(s and (s["has_results"] or s["results_posted"]))
        already = bool(p.get("resolution"))
        # record what the monitor sees, for the dashboard/report
        p["_snapshot_has_results"] = posted
        p["_snapshot_status"] = s["status"] if s else "NOT_IN_SNAPSHOT"
        if posted and not already and p.get("locked_date"):
            flagged.append(p)
    return flagged


# ------------------------------------------------------------------------- REPORT
def conf_icon(label: str) -> str:
    return {"Certain": "[Certain]", "Likely": "[Likely]", "Guessing": "[Guessing]"}.get(label, label)


def write_report(led: dict, flagged: list) -> None:
    s = led["scoring_summary"]
    lines = []
    lines.append("# Prediction Ledger - Standings")
    lines.append("")
    lines.append(f"_Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} by resolve_predictions.py_")
    lines.append("")
    lines.append(f"- Total predictions: **{s['n_total']}**  |  Locked (pre-registered): "
                 f"**{s['n_locked']}**  |  Resolved: **{s['n_resolved']}**  |  "
                 f"Brier-scored: **{s.get('n_scored',0)}**")
    mb = s["mean_brier"]
    lines.append(f"- Running mean Brier score: **{mb if mb is not None else 'n/a (none scored)'}**"
                 + ("  _(lower better; 0.25 = always-guess-0.5 baseline)_" if mb is not None else ""))
    lines.append("")
    if flagged:
        lines.append("## ACTION NEEDED - readouts have posted")
        for p in flagged:
            lines.append(f"- **{p['prediction_id']}** ({p['nct_id']}) results are posted. "
                         f"Read the readout, then run: "
                         f"`python resolve_predictions.py --resolve {p['prediction_id']} --outcome TRUE|FALSE`")
        lines.append("")
    lines.append("## Predictions")
    lines.append("")
    lines.append("| ID | Trial | Claim (abbrev) | P(true) | Conf | Status | Brier |")
    lines.append("|----|-------|----------------|:------:|:----:|--------|:-----:|")
    for p in led["predictions"]:
        if p.get("resolution"):
            status = f"RESOLVED {p['resolution']} ({p.get('resolved_date','')})"
        elif p.get("locked_date"):
            status = f"LOCKED {p['locked_date']}"
        else:
            status = "UNLOCKED (not pre-registered)"
        if p.get("_snapshot_has_results"):
            status += " - results posted!"
        claim = p["claim"][:50] + ("..." if len(p["claim"]) > 50 else "")
        bc = p.get("brier_component")
        lines.append(f"| {p['prediction_id']} | {p['nct_id']} | {claim} | "
                     f"{p['probability']:.2f} | {conf_icon(p['confidence_label'])} | "
                     f"{status} | {bc if bc is not None else '-'} |")
    lines.append("")
    if s.get("calibration_bins"):
        lines.append("## Calibration")
        lines.append("")
        lines.append("| Prob bin | n | Mean predicted | Observed freq TRUE |")
        lines.append("|----------|:-:|:--------------:|:------------------:|")
        for b in s["calibration_bins"]:
            lines.append(f"| {b['bin']} | {b['n']} | {b['mean_predicted']} | {b['observed_frequency']} |")
        lines.append("")
    lines.append("---")
    lines.append("_Pre-registration rule: a prediction edited after its readout is void. "
                 "Lock before you can be scored._")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Report written: {REPORT}")


# --------------------------------------------------------------------------- MAIN
def main() -> int:
    ap = argparse.ArgumentParser(description="Lock, resolve, and score the prediction ledger.")
    ap.add_argument("--lock", metavar="PRED_ID", help="Pre-register a prediction (set locked_date).")
    ap.add_argument("--resolve", metavar="PRED_ID", help="Record an outcome for a locked prediction.")
    ap.add_argument("--outcome", choices=["TRUE", "FALSE", "PARTIAL", "true", "false", "partial"],
                    help="Outcome for --resolve.")
    ap.add_argument("--date", help="Date for --lock/--resolve (YYYY-MM-DD). Default: today.")
    ap.add_argument("--source", help="Provenance for --resolve: URL/citation of the readout "
                    "(required if the trial has no posted results in the snapshot).")
    ap.add_argument("--allow-no-results", action="store_true",
                    help="Override the provenance guard and resolve despite no posted results "
                    "(records the override; not recommended).")
    ap.add_argument("--unresolve", metavar="PRED_ID",
                    help="Void a resolution recorded in error / for a test (keeps the lock).")
    ap.add_argument("--report-only", action="store_true", help="Print standings; no scan.")
    args = ap.parse_args()
    when = args.date or date.today().isoformat()

    led = load_ledger()
    # Snapshot is needed up front so --resolve can enforce the provenance guard.
    snap = {} if args.report_only else load_snapshot_results()

    if args.lock:
        do_lock(led, args.lock, when)
        recompute_summary(led)
        save_ledger(led)

    if args.unresolve:
        do_unresolve(led, args.unresolve)
        recompute_summary(led)
        save_ledger(led)

    if args.resolve:
        if not args.outcome:
            sys.exit("ERROR: --resolve requires --outcome TRUE|FALSE|PARTIAL.")
        do_resolve(led, args.resolve, args.outcome, when,
                   snap, args.source, args.allow_no_results)
        recompute_summary(led)
        save_ledger(led)

    # Refresh summary + readout scan for reporting (unless pure report-only).
    flagged = scan_readouts(led, snap) if snap else []
    recompute_summary(led)
    # scan_readouts annotates predictions with _snapshot_* fields; persist them
    if not args.report_only:
        save_ledger(led)
    write_report(led, flagged)

    # Console summary
    s = led["scoring_summary"]
    print(f"\n  Ledger: {s['n_total']} total | {s['n_locked']} locked | "
          f"{s['n_resolved']} resolved | mean Brier = {s['mean_brier']}")
    if flagged:
        print(f"  >>> {len(flagged)} locked prediction(s) have posted results and await resolution.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
