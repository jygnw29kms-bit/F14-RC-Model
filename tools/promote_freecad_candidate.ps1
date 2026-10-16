param([switch]$Apply)
$ErrorActionPreference='Stop'
$Repo=Split-Path -Parent $PSScriptRoot
Set-Location $Repo
$candidatePath='migration\freecad\CANDIDATE.json'
$currentPath='migration\freecad\CURRENT.json'
if(!(Test-Path $candidatePath)){ throw 'CANDIDATE.json missing' }
$c=Get-Content $candidatePath -Raw | ConvertFrom-Json
if(!(Test-Path $c.candidate_master)){ throw "Candidate master missing: $($c.candidate_master)" }
foreach($a in $c.required_audits){ if(!(Test-Path $a)){ throw "Candidate audit missing: $a" } }
$blockers=@($c.promotion_blockers | Where-Object { $_ -and $_.Trim() })
if($blockers.Count -gt 0){
  Write-Host 'PROMOTION BLOCKED:'
  $blockers | ForEach-Object { Write-Host " - $_" }
  exit 3
}
if(!$Apply){ Write-Host 'PROMOTION READY. Re-run with -Apply to update CURRENT.json.'; exit 0 }
$current=Get-Content $currentPath -Raw | ConvertFrom-Json
$current.current_master=$c.candidate_master
$current.current_revision=$c.candidate_revision
$current.required_audits=@($current.required_audits + $c.required_audits | Select-Object -Unique)
$current.baseline_commit=(git rev-parse --short HEAD).Trim()
$current | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $currentPath
$c.promoted_to_current=$true
$c | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $candidatePath
Write-Host "PROMOTED $($c.candidate_revision) -> CURRENT. Run tools/f14_workflow.ps1 -Mode verify before commit."