# F14 CAD workflow (headless-first)

The canonical repository is `F14-RC-Model`. FreeCAD is the active CAD engine.

## Rules

- Use `FreeCADCmd.exe` for builds, audits, geometry checks, and exports whenever possible.
- Keep FreeCAD GUI closed unless a visual inspection is required; when opened, close or minimize it immediately afterwards.
- Fusion 360 is NOT an active design tool. It may only be opened temporarily to inspect or export legacy project components when the required historical geometry/data cannot be recovered otherwise. No new F14 geometry is to be created in Fusion. Close Fusion immediately after the legacy extraction/export.
- `migration/freecad/CURRENT.json` is the single pointer to the current CAD master and mandatory audit set.
- Every geometry milestone must be reproducible from scripts/JSON and must produce an audit before commit/push.
- Never set print or flight release true from geometry-only checks.
- Do not keep duplicate transient Fusion export files after their reviewed result has been promoted into `analysis/independent_reviews`.

## Fast commands

`powershell -ExecutionPolicy Bypass -File tools/f14_headless.ps1 status`

`powershell -ExecutionPolicy Bypass -File tools/f14_headless.ps1 verify`

`powershell -ExecutionPolicy Bypass -File tools/f14_headless.ps1 close-gui`


## Unified workflow

Use `tools/f14_workflow.ps1` as the primary entry point:

- `-Mode status` shows Git sync, tracked/untracked state, CAD processes, CURRENT and CANDIDATE.
- `-Mode preflight` enforces the FreeCAD/Fusion policy, validates CURRENT paths/audits and runs `git diff --check`.
- `-Mode verify` closes CAD GUIs, runs preflight, verifies the CURRENT FreeCAD document headlessly, then checks the Git diff.
- `-Mode snapshot` renders the README development image and closes FreeCAD afterwards.
- `-Mode close-gui` closes FreeCAD/Fusion GUI processes.

`migration/freecad/CURRENT.json` is the verified master pointer. `migration/freecad/CANDIDATE.json` may point to newer engineering work but must list every known promotion blocker. A candidate is not the master merely because its revision number is higher.

`tools/promote_freecad_candidate.ps1` refuses promotion while blockers remain or required audits are missing. After promotion, run the full `verify` mode before committing.

Transient legacy Fusion extraction output under `workspace/RC-F14-Tomcat/Fusion/Exports/Current/source_shell_v53/` is ignored by Git. Nothing is deleted automatically. Reviewed evidence must be copied/promoted into a tracked `analysis/independent_reviews/...` location before it is relied upon.