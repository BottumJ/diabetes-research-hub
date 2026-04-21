<#
.SYNOPSIS
  Diabetes Research Hub — daily refresh launcher.

.DESCRIPTION
  Wraps Analysis\Scripts\refresh_hub.py so Windows Task Scheduler can run
  the daily refresh (baselines + hub_monitor + gap analysis + git push) with
  a durable, timestamped log.

.PARAMETER NoPush
  Commit locally but do not push.

.PARAMETER NoCommit
  Run the refresh scripts only; skip all git steps.

.PARAMETER ResultsOnly
  Stage only Analysis/Results/ (skip dashboards, scripts, etc. that may be
  mid-edit).

.PARAMETER Branch
  Push target branch (default: main).

.EXAMPLE
  .\refresh.ps1
  .\refresh.ps1 -NoPush
  .\refresh.ps1 -ResultsOnly

.NOTES
  Log file: Analysis\Results\logs\refresh_<yyyy-MM-dd_HHmm>.log
  Exit 0 on success, non-zero on any failure.
#>

param(
    [switch]$NoPush,
    [switch]$NoCommit,
    [switch]$ResultsOnly,
    [string]$Branch = "main"
)

$ErrorActionPreference = "Continue"

# Anchor to the folder this script lives in (repo root).
$RepoRoot = $PSScriptRoot
Set-Location $RepoRoot

# Log directory + file
$LogDir = Join-Path $RepoRoot "Analysis\Results\logs"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
}
$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmm"
$LogFile  = Join-Path $LogDir "refresh_$Timestamp.log"

# Resolve python (prefer 'py -3' on Windows if present; fall back to 'python')
$PythonCmd = "python"
if (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonCmd = "py"
}

# Build argument list
$ScriptPath = "Analysis\Scripts\refresh_hub.py"
$PyArgs = @()
if ($PythonCmd -eq "py") { $PyArgs += "-3" }
$PyArgs += $ScriptPath
if ($NoPush)      { $PyArgs += "--no-push" }
if ($NoCommit)    { $PyArgs += "--no-commit" }
if ($ResultsOnly) { $PyArgs += "--results-only" }
if ($Branch -and $Branch -ne "main") {
    $PyArgs += @("--branch", $Branch)
}

# Banner
$Banner = @"
================================================================
 Diabetes Research Hub — refresh.ps1
 Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')
 Repo:    $RepoRoot
 Cmd:     $PythonCmd $($PyArgs -join ' ')
 Log:     $LogFile
================================================================
"@
Write-Host $Banner
$Banner | Out-File -FilePath $LogFile -Encoding utf8

# Run it, tee-ing stdout+stderr into the log
try {
    & $PythonCmd @PyArgs 2>&1 | Tee-Object -FilePath $LogFile -Append
    $ExitCode = $LASTEXITCODE
}
catch {
    Write-Host "ERROR: $_"
    "ERROR: $_" | Out-File -FilePath $LogFile -Append -Encoding utf8
    $ExitCode = 1
}

$Footer = @"

================================================================
 Finished: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')
 Exit code: $ExitCode
================================================================
"@
Write-Host $Footer
$Footer | Out-File -FilePath $LogFile -Append -Encoding utf8

exit $ExitCode
