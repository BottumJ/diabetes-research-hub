<#
    RUN_PIPELINE_AND_PUSH.ps1
    Written 2026-09-07 by the scheduled research agent.

    WHY THIS FILE EXISTS
      Two things the agent cannot do from its sandbox, both now blocking:

      1. PUSH. `git push` fails with "could not read Username for
         https://github.com" - the remote is HTTPS and the sandbox has no
         credential helper, no ~/.git-credentials and no GH_TOKEN. As of today
         main is 103 commits ahead of origin/main and origin's tip is f7e976f
         dated 2026-04-20. That is 140 days in which nothing this agent built
         reached a reader.

      2. RUN THE FULL PIPELINE. run_quality_improvements.py exceeds the
         sandbox's ~178-second per-call limit, and background execution is
         impossible there because every call gets its own PID namespace - a
         nohup'd process dies when the call returns. Verified 2026-09-07.
         So the 67 gates have not been verified in the sandbox.

      Both are compute-and-credential problems, not judgement problems, which
      is why they belong on your machine.

    USAGE
      cd $HOME\OneDrive\Diabetes_Research
      .\RUN_PIPELINE_AND_PUSH.ps1              # run gates, then prompt to push
      .\RUN_PIPELINE_AND_PUSH.ps1 -GatesOnly   # run gates, never push
      .\RUN_PIPELINE_AND_PUSH.ps1 -SkipGates   # push only (gates already green)

    IT WILL NOT PUSH WITHOUT ASKING. Nothing here force-pushes or rewrites
    history.
#>

[CmdletBinding()]
param(
    [switch]$GatesOnly,
    [switch]$SkipGates
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repo

function Write-Section($text) {
    Write-Host ''
    Write-Host ('=' * 74) -ForegroundColor Cyan
    Write-Host $text -ForegroundColor Cyan
    Write-Host ('=' * 74) -ForegroundColor Cyan
}

# --------------------------------------------------------------- 0. WHERE WE ARE
Write-Section '0. CURRENT STATE'

$python = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { throw 'No python on PATH. Install Python or fix PATH, then re-run.' }
Write-Host ("python : {0}" -f $python.Source)

git fetch origin 2>&1 | Out-Null
$ahead  = (git rev-list --count origin/main..main).Trim()
$behind = (git rev-list --count main..origin/main).Trim()
$originTip = (git log -1 --format='%h %ad %s' --date=short origin/main)

Write-Host ("main is {0} commit(s) AHEAD of origin/main" -f $ahead)
Write-Host ("main is {0} commit(s) BEHIND origin/main" -f $behind)
Write-Host ("origin/main tip : {0}" -f $originTip)

if ([int]$behind -gt 0) {
    Write-Host ''
    Write-Host 'origin/main has commits main does not. This script will NOT resolve that.' -ForegroundColor Yellow
    Write-Host 'Reconcile by hand (git pull --rebase, or merge) before pushing.' -ForegroundColor Yellow
    return
}

# ------------------------------------------------------------------- 1. GATES
if (-not $SkipGates) {
    Write-Section '1. QUALITY PIPELINE'
    Write-Host 'Running run_quality_improvements.py. This is the long step.' -ForegroundColor Gray
    Write-Host 'Every stage must report [OK]. Any [FAIL] stops the push.' -ForegroundColor Gray
    Write-Host ''

    $log = Join-Path $repo ('Analysis\Logs\pipeline_{0}.log' -f (Get-Date -Format 'yyyy-MM-dd'))
    $logDir = Split-Path -Parent $log
    if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

    & $python.Source 'Analysis\Scripts\run_quality_improvements.py' 2>&1 |
        Tee-Object -FilePath $log
    $gateExit = $LASTEXITCODE

    Write-Host ''
    Write-Host ("full log: {0}" -f $log) -ForegroundColor Gray

    $failures = Select-String -Path $log -Pattern '\[FAIL\]' -ErrorAction SilentlyContinue
    if ($failures) {
        Write-Host ''
        Write-Host ('{0} stage(s) FAILED:' -f $failures.Count) -ForegroundColor Red
        $failures | ForEach-Object { Write-Host ('  ' + $_.Line) -ForegroundColor Red }
    }

    # EXPECTED FAILURE, 2026-09-07: the new "gapsubject" stage fails by design.
    # 9 of 15 gaps are tiered on evidence that does not cover their own
    # question. That is a real finding awaiting your decision, not a broken
    # gate - see DECISION_BRIEF_2026-09-07.md. Do not "fix" it by loosening
    # the gate.
    if ($gateExit -ne 0 -or $failures) {
        Write-Host ''
        Write-Host 'NOTE: as of 2026-09-07 the "gapsubject" stage is EXPECTED to fail.' -ForegroundColor Yellow
        Write-Host 'It reports 9 of 15 gaps tiered on evidence that never mentions the' -ForegroundColor Yellow
        Write-Host 'gap''s own subject. That is a finding awaiting your call, not a bug.' -ForegroundColor Yellow
        Write-Host 'See DECISION_BRIEF_2026-09-07.md. Any OTHER failure is a real defect.' -ForegroundColor Yellow
    }

    if ($GatesOnly) { Write-Host ''; Write-Host 'GatesOnly set. Stopping.' -ForegroundColor Gray; return }

    if ($gateExit -ne 0 -or $failures) {
        Write-Host ''
        $go = Read-Host 'Gates did not come back clean. Push anyway? (type YES to push)'
        if ($go -ne 'YES') { Write-Host 'Not pushing.' -ForegroundColor Gray; return }
    }
}

if ($GatesOnly) { return }

# -------------------------------------------------------------- 2. WHAT SHIPS
Write-Section '2. WHAT WOULD BE PUBLISHED'

Write-Host 'Commits main has that origin/main does not (newest 15):'
git log --oneline -15 origin/main..main | ForEach-Object { Write-Host ('  ' + $_) }
Write-Host ''
Write-Host ("files changed vs origin/main: {0}" -f (git diff --name-only origin/main..main | Measure-Object).Count)
Write-Host ''
Write-Host 'Uncommitted changes in the working tree:'
$dirty = git status --porcelain
if ($dirty) { $dirty | Select-Object -First 25 | ForEach-Object { Write-Host ('  ' + $_) } }
else        { Write-Host '  (none)' }

if ($dirty) {
    Write-Host ''
    $stage = Read-Host 'Commit these first? (type YES to commit, anything else to skip)'
    if ($stage -eq 'YES') {
        git add -A
        $msg = Read-Host 'Commit message (blank for default)'
        if ([string]::IsNullOrWhiteSpace($msg)) {
            $msg = ('Daily iteration {0}: gap subject-coverage gate, 9/15 gaps flagged' -f (Get-Date -Format 'yyyy-MM-dd'))
        }
        git commit -m $msg
    }
}

# ------------------------------------------------------------------- 3. PUSH
Write-Section '3. PUSH'

Write-Host 'This pushes main to origin/main. It does not force and does not rewrite history.'
Write-Host ''
$confirm = Read-Host 'Push? (type PUSH to proceed)'
if ($confirm -ne 'PUSH') { Write-Host 'Not pushing.' -ForegroundColor Gray; return }

git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host ''
    Write-Host 'Push failed. Most likely you need credentials on this machine:' -ForegroundColor Red
    Write-Host '  gh auth login                      (GitHub CLI, easiest)' -ForegroundColor Gray
    Write-Host '  git config --global credential.helper manager' -ForegroundColor Gray
    Write-Host ''
    Write-Host 'To let the SCHEDULED agent push unattended, it needs a PAT reachable' -ForegroundColor Gray
    Write-Host 'from its environment - otherwise this stays a manual step forever.' -ForegroundColor Gray
    return
}

# ---------------------------------------------------------------- 4. VERIFY
Write-Section '4. VERIFY THE READER CAN ACTUALLY SEE IT'

git fetch origin 2>&1 | Out-Null
$aheadAfter = (git rev-list --count origin/main..main).Trim()
Write-Host ("main is now {0} commit(s) ahead of origin/main" -f $aheadAfter)

if ($aheadAfter -eq '0') {
    Write-Host 'origin/main is current.' -ForegroundColor Green
} else {
    Write-Host 'Still ahead. The push did not land everything.' -ForegroundColor Red
    return
}

# docs/Reports/ has never existed on origin/main. That is why two reports the
# hub advertises as "Available" return 404 for a real reader.
Write-Host ''
Write-Host 'Checking docs/Reports/ now exists on the published branch:'
$reports = git ls-tree --name-only origin/main docs/Reports/ 2>$null
if ($reports) {
    Write-Host ('  present: {0} entr(y/ies)' -f ($reports | Measure-Object).Count) -ForegroundColor Green
} else {
    Write-Host '  STILL ABSENT on origin/main - the advertised reports will still 404.' -ForegroundColor Red
}

Write-Host ''
Write-Host 'Pages redeploys on push; allow a minute, then load the site and confirm' -ForegroundColor Gray
Write-Host 'a page you know changed. A green push is not a served page.' -ForegroundColor Gray
