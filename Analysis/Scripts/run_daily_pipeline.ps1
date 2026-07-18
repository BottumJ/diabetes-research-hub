<#
    run_daily_pipeline.ps1
    Runs the FULL Diabetes Research Hub daily pull, in order, on your machine:
        1. baseline_clinical_trials.py
        2. baseline_pubmed_alerts.py
        3. gap_analysis_daily.py        (resumable literature gap analysis)
        4. hub_monitor.py               (captures the fresh gap data LAST)

    It delegates the ordering/failure handling to run_daily_local.py and just
    adds a timestamped log. This is what Windows Task Scheduler launches at 5 AM.

    Run manually to test:
        powershell -ExecutionPolicy Bypass -File "run_daily_pipeline.ps1"
#>

$ErrorActionPreference = "Stop"

# --- Paths (this script lives in ...\Analysis\Scripts) ---
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$Orchestrator = Join-Path $ScriptDir "run_daily_local.py"
$LogDir      = Join-Path $ScriptDir "..\Logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$LogFile     = Join-Path $LogDir ("daily_pipeline_{0}.log" -f (Get-Date -Format "yyyy-MM-dd"))

# --- OPTIONAL: NCBI API key (raises PubMed limit 3 -> 10 req/sec) ---
# Get a free key at https://www.ncbi.nlm.nih.gov/account/ , then uncomment:
# $env:NCBI_API_KEY = "paste_your_key_here"

# --- Find Python ---
$Python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $Python) { $Python = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $Python) {
    "ERROR: Python not found on PATH. Install Python 3 or hardcode its full path in this script." |
        Tee-Object -FilePath $LogFile -Append
    exit 1
}

if (-not (Test-Path $Orchestrator)) {
    "ERROR: run_daily_local.py not found at $Orchestrator" | Tee-Object -FilePath $LogFile -Append
    exit 1
}

# --- Run the full pipeline ---
"===== Daily pipeline started $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') =====" |
    Tee-Object -FilePath $LogFile -Append

& $Python "-u" $Orchestrator *>&1 | Tee-Object -FilePath $LogFile -Append
$code = $LASTEXITCODE

"===== Finished $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') (exit $code) =====" |
    Tee-Object -FilePath $LogFile -Append

exit $code
