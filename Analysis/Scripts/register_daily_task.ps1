<#
    register_daily_task.ps1
    Registers a Windows Task Scheduler job that runs the FULL daily pipeline
    (clinical trials -> pubmed -> gap analysis -> hub monitor) every morning at
    5:00 AM. Run this ONCE.

    HOW TO RUN (ordinary PowerShell window -- admin NOT required for a per-user task):
        cd "C:\Users\justi\OneDrive\Diabetes_Research\Analysis\Scripts"
        powershell -ExecutionPolicy Bypass -File "register_daily_task.ps1"

    Change the time via $RunTime below.
    Remove later:
        Unregister-ScheduledTask -TaskName "DiabetesHub_DailyPipeline" -Confirm:$false
#>

$ErrorActionPreference = "Stop"

$TaskName  = "DiabetesHub_DailyPipeline"
$RunTime   = "5:00AM"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Wrapper   = Join-Path $ScriptDir "run_daily_pipeline.ps1"

if (-not (Test-Path $Wrapper)) {
    Write-Error "Cannot find run_daily_pipeline.ps1 next to this script ($Wrapper)."
    exit 1
}

# What runs: PowerShell -> the wrapper script
$Action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Wrapper`""

# When: every day at 5:00 AM
$Trigger = New-ScheduledTaskTrigger -Daily -At $RunTime

# Behavior:
#   StartWhenAvailable -> if the PC was asleep/off at 5am, run at next opportunity
#   WakeToRun          -> wake the machine from sleep to run (best-effort)
#   1.5h limit         -> full pipeline is longer than gap-only; generous ceiling
#   Run only when this user is logged on (no stored password needed)
$Settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -WakeToRun `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1 -Minutes 30) `
    -MultipleInstances IgnoreNew

$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

# Remove any prior version (including the old gap-only task), then register fresh
foreach ($old in @("DiabetesHub_DailyPipeline", "DiabetesHub_GapAnalysis")) {
    if (Get-ScheduledTask -TaskName $old -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $old -Confirm:$false
    }
}

Register-ScheduledTask -TaskName $TaskName `
    -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal `
    -Description "Diabetes Research Hub: full daily data pull (trials, pubmed, gap analysis, hub monitor)." | Out-Null

Write-Host ""
Write-Host "Registered scheduled task '$TaskName' -> runs daily at $RunTime." -ForegroundColor Green
Write-Host "Test it now with:  Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "Check status with: Get-ScheduledTaskInfo -TaskName '$TaskName'"
Write-Host "Logs land in:      ..\Logs\daily_pipeline_<date>.log"
