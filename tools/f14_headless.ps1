param(
  [ValidateSet('status','verify','close-gui')]
  [string]$Mode='status'
)
$workflow=Join-Path $PSScriptRoot 'f14_workflow.ps1'
& powershell -NoProfile -ExecutionPolicy Bypass -File $workflow -Mode $Mode
exit $LASTEXITCODE