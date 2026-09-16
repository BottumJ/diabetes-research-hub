# run_pending_pipeline.ps1
# -----------------------------------------------------------------------------
# Written 2026-09-14 by the scheduled research agent, because the Linux sandbox
# has failed to mount for six consecutive days (Plan9 share error, attributed to
# the Windows update released 2026-09-08). No Python has executed since
# 2026-09-08, so the repository is diverged in the worst direction: the .py
# sources are correct and the generated HTML under Dashboards/ and docs/ is not.
# A grep of the scripts reports the problems fixed while an actual reader still
# sees every false citation.
#
# This script does exactly what the P0 queue item asks, in order, and stops on
# the first failure. It is the whole of the pending user action.
#
# USAGE, from the repository root:
#     powershell -ExecutionPolicy Bypass -File Analysis\Scripts\run_pending_pipeline.ps1
#
# Add -Push to commit and push when every step succeeds. Without it the script
# stages nothing and leaves the working tree for you to inspect.
# -----------------------------------------------------------------------------

[CmdletBinding()]
param(
    [switch]$Push,
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

# Resolve the repo root as the grandparent of this script's directory, so the
# script works regardless of the directory it is invoked from.
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent (Split-Path -Parent $ScriptDir)
Set-Location $RepoRoot

Write-Host ""
Write-Host "Repository root: $RepoRoot" -ForegroundColor Cyan
Write-Host ""

# Verify the interpreter exists before doing anything else.
try {
    $pyVersion = & $Python --version 2>&1
    Write-Host "Interpreter: $pyVersion" -ForegroundColor Cyan
}
catch {
    Write-Host "FATAL: could not run '$Python'." -ForegroundColor Red
    Write-Host "Pass an explicit path, e.g. -Python 'C:\Python312\python.exe'." -ForegroundColor Red
    exit 1
}

# Ordered as the queue specifies: the two cheap verifiers first, because their
# real job is to syntax-check six days of unexecuted file-tool edits, and that
# is the largest single risk. Only then the rebuild.
$Steps = @(
    @{
        Name   = "Verify 2026-09-13 repairs (also syntax-checks every builder)"
        Script = "Analysis\Scripts\verify_2026_09_13_repairs.py"
        Fatal  = $true
    },
    @{
        Name   = "Verify 2026-09-11 repairs"
        Script = "Analysis\Scripts\verify_2026_09_11_repairs.py"
        Fatal  = $true
    },
    @{
        Name   = "Verify 2026-09-12 repairs"
        Script = "Analysis\Scripts\verify_2026_09_12_repairs.py"
        Fatal  = $false   # not named in the P0 item; run if present, do not block on it
    },
    @{
        Name   = "Rebuild all dashboards and run quality gates"
        Script = "Analysis\Scripts\run_quality_improvements.py"
        Fatal  = $true
    }
)

$Failed    = @()
$Skipped   = @()
$Succeeded = @()

foreach ($step in $Steps) {

    $path = Join-Path $RepoRoot $step.Script

    if (-not (Test-Path $path)) {
        Write-Host "SKIP  $($step.Name)" -ForegroundColor DarkYellow
        Write-Host "      not found: $($step.Script)"
        $Skipped += $step.Name
        continue
    }

    Write-Host ""
    Write-Host ("-" * 78)
    Write-Host "RUN   $($step.Name)" -ForegroundColor White
    Write-Host "      $($step.Script)"
    Write-Host ("-" * 78)

    # Do not let a non-zero exit terminate the script via ErrorActionPreference;
    # handle the exit code explicitly so the summary below is always printed.
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $Python $path
    $code = $LASTEXITCODE
    $ErrorActionPreference = $prev

    if ($code -eq 0) {
        Write-Host "OK    $($step.Name)" -ForegroundColor Green
        $Succeeded += $step.Name
    }
    else {
        Write-Host "FAIL  $($step.Name) (exit $code)" -ForegroundColor Red
        $Failed += $step.Name
        if ($step.Fatal) {
            Write-Host ""
            Write-Host "Stopping: this step is required by the pending queue item." -ForegroundColor Red
            Write-Host "Nothing has been committed. Fix the failure and re-run." -ForegroundColor Red
            exit $code
        }
    }
}

Write-Host ""
Write-Host ("=" * 78)
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host ("=" * 78)
foreach ($n in $Succeeded) { Write-Host "  OK    $n" -ForegroundColor Green }
foreach ($n in $Skipped)   { Write-Host "  SKIP  $n" -ForegroundColor DarkYellow }
foreach ($n in $Failed)    { Write-Host "  FAIL  $n" -ForegroundColor Red }
Write-Host ""

if ($Failed.Count -gt 0) {
    Write-Host "One or more non-fatal steps failed. Not pushing." -ForegroundColor Yellow
    exit 1
}

# Show what changed, so the rebuild can be inspected before anything is pushed.
Write-Host "Working tree status:" -ForegroundColor Cyan
git status --short
Write-Host ""

if (-not $Push) {
    Write-Host "Pipeline complete. Re-run with -Push to commit and push," -ForegroundColor Cyan
    Write-Host "or review the diff first:  git diff --stat" -ForegroundColor Cyan
    exit 0
}

$changes = git status --porcelain
if ([string]::IsNullOrWhiteSpace($changes)) {
    Write-Host "No changes to commit." -ForegroundColor Cyan
    exit 0
}

$stamp = Get-Date -Format "yyyy-MM-dd"
git add -A
git commit -m "Rebuild dashboards after sandbox outage; apply citation repairs 2026-09-09..$stamp"
git push

Write-Host ""
Write-Host "Pushed. The published HTML and the builder sources are back in sync." -ForegroundColor Green
