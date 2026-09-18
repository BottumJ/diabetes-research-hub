"""
KNOWN-POSITIVE FIXTURE for audit_computed_value_citations.py
============================================================

THIS FILE IS NOT A BUILDER. It publishes nothing and is never executed by the
pipeline. It exists so that the computed-value citation gate has a defect it
must always catch.

WHY IT EXISTS
-------------
The defect this gate hunts was found live on 2026-09-13 in
build_lada_diagnostic_model.py:763-766 - a PMID printed inside the same
f-string as an interpolation of a value the script had computed seconds
earlier, so a locally modelled dollar figure was dressed as a published one.
That defect was repaired before the gate was written, which left the gate with
NO live positive to prove itself on. A gate that has only ever returned zero
is indistinguishable from a gate that does not work.

The two lines below reproduce the original defect verbatim in shape. Both
must be reported as COMPUTED. Verify with:

    python - <<'EOF'
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "m", "Analysis/Scripts/audit_computed_value_citations.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for x in m.scan_file("Analysis/Scripts/_tmp_gate_known_positive.py", "FIXTURE"):
        print(x["severity"], x["line"], x["expression"], x["pmids"])
    EOF

Expected, and confirmed 2026-09-18:
    COMPUTED 32 result['total_cost'] ['37909353']
    COMPUTED 33 result['icer']       ['37909353']

The audit's own SKIP_PREFIXES excludes "_tmp_", so this file is invisible to a
normal run and cannot inflate the repo-wide count. It is reachable only by
calling scan_file() on it directly, which is what the check above does.

PMID 37909353 is the Economic Costs of Diabetes in the US 2022 paper. It is
used here as the *wrong* citation in a deliberately wrong construction. Nothing
in this file is an assertion about what that paper reports.
"""

result = {"total_cost": 1000000000, "icer": 25000}
rows = []
rows.append(f"<td>${result['total_cost']:,.0f} (PMID:37909353)</td>")
rows.append(f"<td>${result['icer']:,.0f} per QALY (PMID:37909353)</td>")
