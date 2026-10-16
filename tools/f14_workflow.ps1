param(
  [ValidateSet('status','preflight','verify','close-gui','snapshot')]
  [string]$Mode='status'
)
$ErrorActionPreference='Stop'
$Repo=Split-Path -Parent $PSScriptRoot
$FreeCADCmd='C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe'
$FreeCADGui='C:\Program Files\FreeCAD 1.1\bin\FreeCAD.exe'
Set-Location $Repo
function Stop-CadGui { Get-Process freecad,Fusion360 -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue }
function Assert-NoFusion { if(Get-Process Fusion360 -ErrorAction SilentlyContinue){ throw 'Fusion360 is running. F14 policy permits Fusion only for explicit unavoidable legacy read/export; close it before normal workflow.' } }
function Show-CoreStatus {
  Write-Host 'HEAD:'; git log -1 --oneline
  Write-Host 'SYNC:'; git rev-list --left-right --count origin/main...HEAD
  Write-Host 'TRACKED STATUS:'; git status --short --untracked-files=no
  Write-Host 'UNTRACKED (non-ignored):'; git ls-files --others --exclude-standard
  Write-Host 'CAD GUI:'; Get-Process freecad,Fusion360 -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,MainWindowTitle
  Write-Host 'CURRENT:'; Get-Content 'migration\freecad\CURRENT.json'
  if(Test-Path 'migration\freecad\CANDIDATE.json'){ Write-Host 'CANDIDATE:'; Get-Content 'migration\freecad\CANDIDATE.json' }
}
function Invoke-PolicyCheck {
  Assert-NoFusion
  if(!(Test-Path $FreeCADCmd)){ throw 'FreeCADCmd not found' }
  $meta=Get-Content 'migration\freecad\CURRENT.json' -Raw | ConvertFrom-Json
  if(!(Test-Path $meta.current_master)){ throw "CURRENT master missing: $($meta.current_master)" }
  foreach($a in $meta.required_audits){ if(!(Test-Path $a)){ throw "Required audit missing: $a" } }
  $bad=Select-String -Path 'tools\*.ps1','migration\freecad\*.py' -Pattern 'Start-Process\s+.*Fusion|Fusion360\.exe' -ErrorAction SilentlyContinue
  if($bad){ throw 'Active FreeCAD workflow contains a Fusion launch command. Policy violation.' }
  Write-Host 'POLICY: PASS'
}
switch($Mode){
  'close-gui' { Stop-CadGui; Write-Host 'CAD GUI processes closed.' }
  'status' { Show-CoreStatus }
  'preflight' { Invoke-PolicyCheck; git diff --check; if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}; Write-Host 'PREFLIGHT: PASS' }
  'verify' { Stop-CadGui; Invoke-PolicyCheck; & $FreeCADCmd (Join-Path $Repo 'migration\freecad\verify_current.py'); if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}; git diff --check; if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}; Write-Host 'VERIFY: PASS' }
  'snapshot' { Assert-NoFusion; if(!(Test-Path $FreeCADGui)){throw 'FreeCAD GUI not found'}; & $FreeCADGui (Join-Path $Repo 'tools\render_readme_snapshot.py'); Start-Sleep -Seconds 2; Get-Process freecad -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue; Write-Host 'SNAPSHOT: rendered and FreeCAD GUI closed.' }
}