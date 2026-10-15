# F14 CAD workflow (headless-first)

The canonical repository is `F14-RC-Model`. FreeCAD is the active CAD engine.

## Rules

- Use `FreeCADCmd.exe` for builds, audits, geometry checks, and exports whenever possible.
- Keep FreeCAD GUI closed unless a visual inspection is required; when opened, close or minimize it immediately afterwards.
- Keep Fusion 360 closed. It may only be opened for an explicit legacy `.f3d` export that cannot be reconstructed from source data.
- `migration/freecad/CURRENT.json` is the single pointer to the current CAD master and mandatory audit set.
- Every geometry milestone must be reproducible from scripts/JSON and must produce an audit before commit/push.
- Never set print or flight release true from geometry-only checks.
- Do not keep duplicate transient Fusion export files after their reviewed result has been promoted into `analysis/independent_reviews`.

## Fast commands

`powershell -ExecutionPolicy Bypass -File tools/f14_headless.ps1 status`

`powershell -ExecutionPolicy Bypass -File tools/f14_headless.ps1 verify`

`powershell -ExecutionPolicy Bypass -File tools/f14_headless.ps1 close-gui`
