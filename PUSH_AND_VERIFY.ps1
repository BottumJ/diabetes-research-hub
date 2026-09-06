# PUSH_AND_VERIFY.ps1 - run this once, from Windows, to unfreeze the published site.
#
# WHY YOU ARE BEING ASKED
# -----------------------
# The scheduled agent cannot hold git credentials. It can READ the remote
# (git fetch works - the repo is public), it just cannot push. So it has been
# able to SEE this problem since 2026-04-20 and never able to fix it.
#
# What that costs, measured 2026-09-06:
#
#     102 commits on main that origin/main does not have
#     origin/main tip f7e976f, 2026-04-20 - 138 days ago
#     under docs/ (the GitHub Pages root):
#         4 files a visitor gets a 404 for
#        34 files a visitor gets a stale copy of
#         1 file of 39 is what the pipeline believes it published
#
# Every quality gate built since April validates docs/ in the working tree on
# your disk. A visitor loads origin/main:docs/. Those have been different
# directories for 138 days, which is why the pipeline could truthfully report
# "1400/1400 links resolve" about a site where the two reports the hub
# advertises as Available both 404.
#
# WHAT THIS SCRIPT DOES
#   1. shows you exactly what will be published, before publishing it
#   2. asks before doing anything
#   3. pushes
#   4. re-runs the publish gate so the fix is verified, not assumed
#
# It does not commit, rebase, force, or touch any file. Push only.

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

Write-Host ''
Write-Host '=== BEFORE ===' -ForegroundColor Cyan
git fetch origin main
$ahead = (git rev-list --count origin/main..HEAD).Trim()
$tip   = (git log -1 --format='%h  %ad  %s' --date=short origin/main)
Write-Host "  commits not on the site : $ahead"
Write-Host "  origin/main tip         : $tip"
Write-Host ''
Write-Host '  files under docs/ a visitor currently gets wrong:'
git diff --name-status origin/main HEAD -- docs/ |
    ForEach-Object {
        $p = $_ -split "`t"
        $label = switch ($p[0].Substring(0,1)) {
            'A' { '404 (missing on site)' }
            'D' { 'deleted here, still served' }
            default { 'stale' }
        }
        '    {0,-28} {1}' -f $label, $p[-1]
    }

Write-Host ''
$answer = Read-Host 'Push these commits to origin/main? (y/N)'
if ($answer -notin @('y','Y')) {
    Write-Host 'Aborted. Nothing was pushed.' -ForegroundColor Yellow
    exit 1
}

Write-Host ''
Write-Host '=== PUSHING ===' -ForegroundColor Cyan
git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host ''
    Write-Host 'Push failed. Most likely you need to authenticate once:' -ForegroundColor Red
    Write-Host '    winget install --id GitHub.cli'
    Write-Host '    gh auth login          # choose HTTPS, then "Yes" to git credential helper'
    Write-Host 'Then re-run this script. Credentials are stored by Windows, not by the agent.'
    exit 1
}

Write-Host ''
Write-Host '=== VERIFYING ===' -ForegroundColor Cyan
# The same gate the pipeline runs. It should now report level and clean; if it
# does not, the push did not do what it appeared to.
python Analysis\Scripts\audit_publish_reachability.py
$gate = $LASTEXITCODE

Write-Host ''
if ($gate -eq 0) {
    Write-Host 'VERIFIED: the site now matches what the pipeline audits.' -ForegroundColor Green
    Write-Host 'GitHub Pages usually rebuilds within a minute or two:'
    Write-Host '    https://bottumj.github.io/diabetes-research-hub/'
} else {
    Write-Host 'The push reported success but the gate still fails. Read its output above.' -ForegroundColor Red
    Write-Host 'Do not treat the site as current until this is clean.'
}
exit $gate
