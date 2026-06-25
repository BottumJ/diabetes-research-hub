#!/usr/bin/env python3
"""
build_prediction_ledger.py - Render the prediction ledger as a dashboard.

Reads  Analysis/Results/prediction_ledger.json
Writes Dashboards/Prediction_Ledger.html

Static HTML, data baked in at build time (matches the rest of the hub's
build_*.py -> Dashboards/*.html convention; works offline). Run after
resolve_predictions.py on each daily refresh.

Design: Tufte-leaning. The centerpiece is a calibration plot (predicted vs
observed) with the 45-degree reference line - the single picture that shows
whether the science arm is honest about its own uncertainty. Empty until
predictions resolve; the empty frame is intentional (the system is built to
be scored, and shows it).
"""
from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = SCRIPT_DIR.parent / "Results"
DASH_DIR = SCRIPT_DIR.parent.parent / "Dashboards"
LEDGER = RESULTS_DIR / "prediction_ledger.json"
OUT = DASH_DIR / "Prediction_Ledger.html"

EVIDENCE_COLOR = {"BRONZE": "#b07a3a", "SILVER": "#8a8a8a", "GOLD": "#d4a017"}
CONF_COLOR = {"Certain": "#2d7d46", "Likely": "#2c5f8a", "Guessing": "#d67c3b"}


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""))


def calibration_svg(cal_bins: list, scored: list) -> str:
    """Tufte calibration plot: x=predicted P(true), y=observed frequency.
    45-degree line = perfect calibration. Points above = underconfident,
    below = overconfident. Dot area ~ number of predictions in the bin."""
    W, H, M = 360, 360, 44
    x0, y0 = M, H - M
    x1, y1 = W - 12, 12
    def px(p): return x0 + p * (x1 - x0)
    def py(f): return y0 - f * (y0 - y1)

    parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
             f'font-family="Georgia, serif" role="img" aria-label="Calibration plot">']
    # gridlines
    for t in (0, 0.25, 0.5, 0.75, 1.0):
        parts.append(f'<line x1="{px(t):.1f}" y1="{y0}" x2="{px(t):.1f}" y2="{y1}" '
                     f'stroke="#eee" stroke-width="1"/>')
        parts.append(f'<line x1="{x0}" y1="{py(t):.1f}" x2="{x1}" y2="{py(t):.1f}" '
                     f'stroke="#eee" stroke-width="1"/>')
        parts.append(f'<text x="{px(t):.1f}" y="{y0+16}" font-size="10" fill="#999" '
                     f'text-anchor="middle">{t:.2f}</text>')
        parts.append(f'<text x="{x0-8}" y="{py(t)+3:.1f}" font-size="10" fill="#999" '
                     f'text-anchor="end">{t:.2f}</text>')
    # axes
    parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#1a1a1a" stroke-width="1.2"/>')
    parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#1a1a1a" stroke-width="1.2"/>')
    # 45-degree perfect-calibration reference
    parts.append(f'<line x1="{px(0):.1f}" y1="{py(0):.1f}" x2="{px(1):.1f}" y2="{py(1):.1f}" '
                 f'stroke="#bbb" stroke-width="1.2" stroke-dasharray="4 3"/>')
    parts.append(f'<text x="{px(0.62):.1f}" y="{py(0.72):.1f}" font-size="9.5" fill="#aaa" '
                 f'transform="rotate(-45 {px(0.62):.1f} {py(0.72):.1f})">perfect calibration</text>')
    # axis labels
    parts.append(f'<text x="{(x0+x1)/2:.0f}" y="{H-6}" font-size="11" fill="#636363" '
                 f'text-anchor="middle">predicted P(true)</text>')
    parts.append(f'<text x="14" y="{(y0+y1)/2:.0f}" font-size="11" fill="#636363" '
                 f'text-anchor="middle" transform="rotate(-90 14 {(y0+y1)/2:.0f})">observed frequency</text>')
    # bin points
    for b in cal_bins:
        cx, cy = px(b["mean_predicted"]), py(b["observed_frequency"])
        r = 4 + (b["n"] ** 0.5) * 4
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#2c5f8a" '
                     f'fill-opacity="0.55" stroke="#2c5f8a" stroke-width="1"/>')
        parts.append(f'<text x="{cx:.1f}" y="{cy-r-3:.1f}" font-size="9" fill="#2c5f8a" '
                     f'text-anchor="middle">n={b["n"]}</text>')
    if not cal_bins:
        parts.append(f'<text x="{(x0+x1)/2:.0f}" y="{(y0+y1)/2:.0f}" font-size="12" '
                     f'fill="#bbb" text-anchor="middle" font-style="italic">'
                     f'no resolved predictions yet</text>')
        parts.append(f'<text x="{(x0+x1)/2:.0f}" y="{(y0+y1)/2+18:.0f}" font-size="10" '
                     f'fill="#ccc" text-anchor="middle">points appear here as trials read out</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def prob_bar(p: float, resolved: str | None) -> str:
    """A small horizontal probability bar, 0..1."""
    pct = p * 100
    color = "#2c5f8a"
    if resolved == "TRUE":
        color = "#2d7d46"
    elif resolved == "FALSE":
        color = "#c0392b"
    return (f'<div class="bar"><div class="bar-fill" style="width:{pct:.0f}%;'
            f'background:{color}"></div><span class="bar-label">{p:.2f}</span></div>')


def status_of(p: dict) -> tuple[str, str]:
    if p.get("resolution"):
        cls = {"TRUE": "ok", "FALSE": "bad", "PARTIAL": "warn"}.get(p["resolution"], "")
        return (f'RESOLVED &middot; {esc(p["resolution"])}'
                f'{" ("+esc(p.get("resolved_date"))+")" if p.get("resolved_date") else ""}', cls)
    if p.get("locked_date"):
        s = f'LOCKED {esc(p["locked_date"])}'
        if p.get("_snapshot_has_results"):
            s += ' &middot; <strong>results posted - resolve now</strong>'
            return s, "warn"
        return s, "lock"
    return "UNLOCKED &middot; not pre-registered", "open"


def build() -> None:
    led = json.loads(LEDGER.read_text(encoding="utf-8"))
    s = led["scoring_summary"]
    preds = led["predictions"]
    scored = [p for p in preds if p.get("brier_component") is not None]
    cal = s.get("calibration_bins", [])
    mb = s.get("mean_brier")

    cards = []
    for p in preds:
        st_text, st_cls = status_of(p)
        ev = p.get("evidence_level_at_prediction", "BRONZE")
        evc = EVIDENCE_COLOR.get(ev, "#888")
        cc = CONF_COLOR.get(p.get("confidence_label", ""), "#636363")
        cure = p.get("cure_relevance", "")
        cure_badge = (f'<span class="badge" style="background:#f0ede4;color:#636363">'
                      f'cure relevance: {esc(cure)}</span>' if cure else "")
        bc = p.get("brier_component")
        bc_html = (f'<div class="metric"><span class="metric-n">{bc}</span>'
                   f'<span class="metric-l">Brier component</span></div>'
                   if bc is not None else "")
        notes = []
        for key, label in (("readout_note", "Readout"),
                           ("registered_primary_endpoint_note", "Endpoint / provenance"),
                           ("todo_before_lock", "Before lock"),
                           ("owner_note", "Owner note")):
            if p.get(key):
                notes.append(f'<p class="note"><span class="note-k">{label}:</span> {esc(p[key])}</p>')
        cards.append(f"""
        <div class="card">
          <div class="card-head">
            <div>
              <span class="pid">{esc(p['prediction_id'])}</span>
              <a class="nct" href="{esc(p.get('source_url','#'))}" target="_blank" rel="noopener">{esc(p['nct_id'])} &#8599;</a>
            </div>
            <div class="badges">
              <span class="badge" style="background:{evc};color:#fff">{esc(ev)}</span>
              <span class="badge" style="background:{cc};color:#fff">[{esc(p.get('confidence_label'))}]</span>
              {cure_badge}
            </div>
          </div>
          <div class="trial">{esc(p.get('trial_short_name',''))}</div>
          <div class="claim">&ldquo;{esc(p['claim'])}&rdquo;</div>
          <div class="row">
            <div class="prob-block">
              <span class="metric-l">P(true) at prediction</span>
              {prob_bar(p['probability'], p.get('resolution'))}
            </div>
            <div class="status status-{st_cls}">{st_text}</div>
            {bc_html}
          </div>
          <p class="reason">{esc(p.get('reasoning',''))}</p>
          {''.join(notes)}
        </div>""")

    gov = led["metadata"].get("governance", {})
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    mb_display = f"{mb}" if mb is not None else "&mdash;"

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Prediction Ledger &middot; Science Arm</title>
<style>
:root {{
  --bg:#fafaf7; --surface:#fff; --text:#1a1a1a; --muted:#636363; --light:#999;
  --border:#e0ddd5; --accent:#2c5f8a; --green:#2d7d46; --gold:#d4a017; --red:#c0392b;
  --serif:Georgia,'Times New Roman',serif;
  --sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  --mono:'SF Mono',Consolas,Monaco,monospace;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:var(--sans);background:var(--bg);color:var(--text);line-height:1.6;}}
.page-header{{max-width:980px;margin:0 auto;padding:48px 32px 24px;border-bottom:1px solid var(--border);}}
.page-header h1{{font-family:var(--serif);font-size:32px;font-weight:400;margin-bottom:8px;}}
.page-header .subtitle{{font-size:13px;color:var(--muted);max-width:760px;}}
.page-header .meta{{font-size:12px;color:var(--light);margin-top:10px;font-family:var(--mono);}}
.container{{max-width:980px;margin:0 auto;padding:32px;}}
section{{margin-bottom:44px;padding-bottom:28px;border-bottom:1px solid var(--border);}}
section:last-of-type{{border-bottom:none;}}
h2{{font-family:var(--serif);font-size:20px;font-weight:400;margin-bottom:6px;}}
.lead{{font-size:13px;color:var(--muted);margin-bottom:20px;max-width:740px;}}
.stats{{display:flex;gap:14px;flex-wrap:wrap;}}
.stat{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 18px;min-width:120px;}}
.stat .n{{font-family:var(--serif);font-size:26px;color:var(--accent);}}
.stat .l{{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;}}
.calib-wrap{{display:flex;gap:28px;align-items:flex-start;flex-wrap:wrap;}}
.calib-wrap svg{{background:var(--surface);border:1px solid var(--border);border-radius:6px;}}
.calib-note{{font-size:13px;color:var(--muted);max-width:380px;}}
.calib-note strong{{color:var(--text);}}
.card{{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px 22px;margin-bottom:18px;}}
.card-head{{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;}}
.pid{{font-family:var(--mono);font-size:13px;color:var(--accent);font-weight:600;margin-right:10px;}}
.nct{{font-family:var(--mono);font-size:12px;color:var(--muted);text-decoration:none;}}
.nct:hover{{color:var(--accent);}}
.badges{{display:flex;gap:6px;flex-wrap:wrap;}}
.badge{{font-size:10.5px;padding:3px 8px;border-radius:10px;letter-spacing:.03em;font-weight:600;}}
.trial{{font-size:13px;color:var(--muted);margin:8px 0 4px;}}
.claim{{font-family:var(--serif);font-size:16px;line-height:1.45;margin:8px 0 16px;}}
.row{{display:flex;gap:24px;align-items:center;flex-wrap:wrap;margin-bottom:12px;}}
.prob-block{{min-width:200px;}}
.metric-l{{font-size:10.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;display:block;margin-bottom:4px;}}
.bar{{position:relative;background:#f0ede4;border-radius:4px;height:22px;width:200px;overflow:hidden;}}
.bar-fill{{height:100%;}}
.bar-label{{position:absolute;right:8px;top:1px;font-family:var(--mono);font-size:12px;color:#1a1a1a;}}
.status{{font-size:12px;padding:5px 10px;border-radius:5px;font-family:var(--mono);}}
.status-open{{background:#f4f1e8;color:var(--muted);}}
.status-lock{{background:#eaf0f5;color:var(--accent);}}
.status-warn{{background:#fbf0e2;color:var(--gold);}}
.status-ok{{background:#e8f3ec;color:var(--green);}}
.status-bad{{background:#f9e9e7;color:var(--red);}}
.metric{{text-align:center;}}
.metric-n{{font-family:var(--serif);font-size:20px;color:var(--text);display:block;}}
.reason{{font-size:13px;color:#444;margin-top:4px;}}
.note{{font-size:12px;color:var(--muted);margin-top:8px;background:#f7f5ef;border-left:3px solid var(--border);padding:7px 10px;border-radius:0 4px 4px 0;}}
.note-k{{font-weight:600;color:#555;}}
.gov li{{font-size:13px;color:#444;margin:6px 0 6px 20px;}}
code{{font-family:var(--mono);font-size:12px;background:#f0ede4;padding:1px 5px;border-radius:3px;}}
.footer{{font-size:12px;color:var(--light);text-align:center;padding:24px;}}
</style>
</head>
<body>
<div class="page-header">
  <h1>Prediction Ledger</h1>
  <p class="subtitle">The science arm's closed loop: dated, falsifiable predictions on tracked trials, scored against reality.
  A prediction counts only once <em>locked before its readout</em>. Being wrong changes the score &mdash; that is the point.</p>
  <p class="meta">Generated {generated} &middot; build_prediction_ledger.py &middot; source: prediction_ledger.json</p>
</div>
<div class="container">

  <section>
    <h2>Standings</h2>
    <p class="lead">Brier score = mean of (probability &minus; outcome)&sup2; over scored predictions. Lower is better:
    0.00 is perfect, 0.25 is what you'd get always guessing 50/50. Nothing is scored until it is both locked and resolved.</p>
    <div class="stats">
      <div class="stat"><span class="n">{s['n_total']}</span><span class="l">Predictions</span></div>
      <div class="stat"><span class="n">{s['n_locked']}</span><span class="l">Locked (pre-reg)</span></div>
      <div class="stat"><span class="n">{s['n_resolved']}</span><span class="l">Resolved</span></div>
      <div class="stat"><span class="n">{s.get('n_scored',0)}</span><span class="l">Brier-scored</span></div>
      <div class="stat"><span class="n">{mb_display}</span><span class="l">Mean Brier</span></div>
    </div>
  </section>

  <section>
    <h2>Calibration</h2>
    <p class="lead">Are the probabilities honest? Each resolved bin plots mean predicted probability against the observed
    frequency of "true." On the dashed 45&deg; line, confidence matches reality. Above it = underconfident; below = overconfident.</p>
    <div class="calib-wrap">
      {calibration_svg(cal, scored)}
      <div class="calib-note">
        <p><strong>Why this chart and not a number.</strong> A single Brier score hides <em>direction</em> of error.
        The calibration curve shows whether the analyst is systematically over- or under-confident &mdash; the signal that
        feeds back into the doctrine (charter &sect;5). It starts empty by design: the system is built to be scored, and the
        empty frame is the honest state until trials read out.</p>
      </div>
    </div>
  </section>

  <section>
    <h2>The predictions</h2>
    <p class="lead">Each carries an evidence level, a confidence label, the probability assigned, and full provenance to an NCT id.
    Claims are written to match each trial's <em>registered primary endpoint</em>.</p>
    {''.join(cards)}
  </section>

  <section class="gov">
    <h2>Governance</h2>
    <ul>
      <li><strong>Pre-registration.</strong> {esc(gov.get('pre_registration',''))}</li>
      <li><strong>Evidence levels.</strong> {esc(gov.get('evidence_levels',''))}</li>
      <li><strong>Provenance.</strong> {esc(gov.get('provenance',''))}</li>
      <li><strong>To lock a prediction:</strong> <code>python Analysis/Scripts/resolve_predictions.py --lock PRED-2026-001 --date YYYY-MM-DD</code></li>
      <li><strong>To resolve after a readout:</strong> <code>python Analysis/Scripts/resolve_predictions.py --resolve PRED-2026-001 --outcome TRUE</code></li>
    </ul>
  </section>

  <div class="footer">Diabetes Research Hub &middot; Science Arm &middot; charter: SCIENCE_ARM_BUILD_CHARTER.md</div>
</div>
</body>
</html>"""
    DASH_DIR.mkdir(exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"  Dashboard written: {OUT}  ({len(doc):,} bytes)")


if __name__ == "__main__":
    build()
