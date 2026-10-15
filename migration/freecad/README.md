# FreeCAD migration package

Purpose: transfer the current F-14 CAD state out of Fusion with STEP as the geometry bridge.

Contents prepared now:
- F14_v187_WALL_CORRECTED_EDF_ADAPTER.f3d — authoritative Fusion archive reference
- F14_v187_section_inputs.json — parametric/interface inputs
- F14_v187_wall_corrected_edf_adapter_audit.json — topology/packaging audit
- exact_interface_conics.json — independently reconstructed inlet interface geometry

Planned Fusion export:
- STEP AP214/AP242 of the v187 joined inlet/EDF geometry
- STL only as mesh cross-check, not as CAD master

FreeCAD validation gates:
1. import STEP as Part solids
2. verify body count and validity
3. compare bounding boxes and volumes against Fusion audit
4. preserve axis convention X longitudinal / Y lateral / Z vertical
5. no print release until geometry comparison passes

The repo remains the source of truth. Do not edit or overwrite the .f3d reference during migration.
