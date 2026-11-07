# v323 Nozzle Transition: clearance-screened candidate, not print-ready

**Branch:** `wip/v321-transition-wall-20261103`. **Main:** last verified v320 geometry. The v323 model is an engineering diagnostic candidate only.

## Geometry and measurements

- Built with 1.5 mm nominal keepout inset, 0.8 mm nominal wall and source-constrained OML.
- Reduced verification mesh uses 24 sampled ring points and seven stations along X=754.962..810.5 mm. **This resolution is not approved for manufacturing.**
- Minimum flow area ~0.928963 FSA. Minimum nominal wall offset 0.800 mm. Maximum center shift 2.485 mm per *10-mm station interval*. These are computed from sections, not a complete physical wall-thickness proof.
- Generator's sampled outer-centroid OML and keepout checks found no violations on either side.
- Independent v323 candidate screen (every 6th facet midpoint plus vertex subset) also found no keepout or OML collisions. **Sampling is not a full volumetric clearance test.**
- FreeCAD confirms both mesh objects are closed solids and not non-manifold.
- Full FreeCAD self-intersection analysis FAILS: right 79 raw returns / 26 unique intersecting facet pairs; left 55 raw / 11 unique pairs. None of those unique pairs shares a mesh vertex. Thus this is not only an artifact of duplicate adjacent facets.
- v324 test combining prior-inner-ring and current-outer-ring phase alignment produced **identical** self-intersection pairs. Hypothesis rejected.

## Critical next engineering work

Resolve self-intersections in both ducts by inspecting and rebuilding the strip triangulation / ring parameterization, especially near irregular 2D cross-sections and X~765/773/810 mm. Verify all facets and the entire 3D wall against OML and v310 keepout, not just vertices or centroids. Re-run the full self-intersection check on the final high-resolution mesh, perform slicer checks and physical fit test.

**No STL release, print clearance or flight release.**

Files: `migration/freecad/F14_v323_PRINTABLE_TRANSITION_WALL_MESH.FCStd`, `build_v323_clearance_transition_wall_candidate.py`, `freecad_v323_printable_transition_wall_mesh_audit.json`, and the independent and self-intersection diagnostic scripts and JSON reports.
