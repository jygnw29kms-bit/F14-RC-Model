param(
  [ValidateSet('status','verify','close-gui')]
  [string]$Mode='status'
)
$ErrorActionPreference='Stop'
$Repo=Split-Path -Parent $PSScriptRoot
$FreeCADCmd='C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe'
Set-Location $Repo
function Close-CadGui {
  Get-Process freecad,Fusion360 -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
}
switch($Mode){
  'close-gui' { Close-CadGui; Write-Host 'CAD GUI processes closed.' }
  'verify' {
    Close-CadGui
    if(!(Test-Path $FreeCADCmd)){ throw 'FreeCADCmd not found' }
    & $FreeCADCmd (Join-Path $Repo 'migration\freecad\verify_current.py')
    if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }
    git status --short
  }
  'status' {
    Write-Host 'HEAD:'; git log -1 --oneline
    Write-Host 'SYNC:'; git rev-list --left-right --count origin/main...HEAD
    Write-Host 'STATUS:'; git status --short
    Write-Host 'CAD GUI:'; $cad=Get-Process freecad,Fusion360 -ErrorAction SilentlyContinue; $cad | Select-Object Id,ProcessName,MainWindowTitle; if($cad | Where-Object ProcessName -eq 'Fusion360'){ Write-Warning 'Fusion is running. Policy: legacy inspection/export only; close immediately after use.' }
    Write-Host 'CURRENT:'; Get-Content 'migration\freecad\CURRENT.json'
  }
}

