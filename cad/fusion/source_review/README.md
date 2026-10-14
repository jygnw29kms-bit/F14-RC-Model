# F-14 Wing Shell / Rib Study Sources

Centralized on 2026-10-14 from the former Codex F-14 worktree. This directory is now the authoritative source location for the v53+ wing shell, spar-clearance, section and rib-review scripts.

## Revision chain

- v53-v56: native wing-shell feasibility studies.
- v57: hollow wing-segment checkpoint.
- v58-v62: carbon spar / skin clearance studies; v62 is the current geometry source for the rib work.
- v63: source spar section-property analysis (see `analysis/`).
- v64: joint-section references.
- v65: native span-section scan.
- v66: sampled native-geometry uniform-load sensitivity (see `analysis/`).
- v67: 0.8 mm zero-clearance joint rib blanks.
- v68-v69: rib-to-skin collision-screen correction.
- v70: conformal rib trimming; all skin-interference screens pass, but no manufacturing clearance is yet claimed.
- v71: 0.10 mm inward side-face offset candidate, preserving rib end faces. Verified own-skin gaps are 0.09995-0.09996 mm, spar gaps are effectively 0.10000 mm, and all skin-interference screens pass. This is a tolerance candidate only; assembly/structural/print/flight release remain false.

## Release discipline

These are engineering studies, not flight-release evidence. A passing geometry screen does not by itself establish assembly, material, buckling, bond, fatigue, sweep-torsion, print-process, or flight capacity. Production/print/flight release remains false until those gates are explicitly verified.

## Central paths

Execution add-in source: `cad/fusion/F14TomcatRC/`

Fusion outputs: `workspace/RC-F14-Tomcat/Fusion/Exports/Current/source_shell_v53/`

Do not continue development in the old Spandau side-project or Codex worktree.
