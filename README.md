# 135er F-14 Tomcat RC

Clean-sheet restart of the RC/FDM F-14 project.

## Current FreeCAD development snapshot

![Current F-14 FreeCAD development snapshot without UPC reference hull](docs/images/f14_freecad_current_20261016.png)

*FreeCAD v194 development view, 16 October 2026. UPC/source fuselage reference hull and reference envelopes are hidden so the currently modeled airframe surfaces, inlet/EDF geometry and mechanism candidates remain visible. This is a development snapshot, not a print or flight release.*
## Current engineering status - 16 October 2026

The aircraft remains **incomplete, not print-ready and not flight-released**.
Original continuous fuselage/wing-glove geometry, common assembly registration,
measured RC hardware, full structural validation and physical proof remain open.
A containment result against an interpolated source candidate is not proof of the
original aircraft outer mold line.

Recent executed development work includes native joined inlet/adapter walls,
internal exhaust candidates, a twin-EDF internal layout, and local P2S slicing
trials. The exhaust also has a native parametric Fusion history with six named
parameters; reimport, parameter regeneration and candidate-loft containment have
been checked. The STL/3MF files remain explicitly unreleased development artifacts.

- [Current propulsion evidence and remaining gates](docs/PROPULSION_CANDIDATE_STATUS_20261016.md)
- [Source-wing review workflow](cad/fusion/source_review/README.md)
- [Authoritative mass budget](docs/04_MASS_BUDGET.md)
- [Verification plan](docs/05_DESIGN_VERIFICATION.md)

## Design target
- visually scale-faithful Grumman F-14 Tomcat outer mold line
- 900 mm span at 20 deg wing sweep
- approximately 1:21.7 scale
- twin 50 mm EDF
- 4S LiPo
- functional 20-68 deg variable-sweep wings
- full-flying stabilators
- FDM-first structure for Bambu Lab P2S
- FreeCAD 1.1.4 headless-first master CAD; Fusion only for unavoidable legacy inspection/export, never for new design

## Non-negotiable rule
The retired F14_RC_FDM R2/R3/R4 geometry, OpenSCAD, STL/3MF files and hardware assumptions are not design inputs for this project.

## Engineering workflow
1. establish authoritative full-scale reference geometry
2. lock scale and outer mold line
3. define aerodynamic and CG envelope
4. design central wing box and sweep mechanism
5. package EDF/ESC/battery/electronics
6. design lightweight FDM structure and carbon reinforcement
7. mass-properties review
8. export printable modules
9. bench verification
10. controlled flight-test expansion

## Documentation
- [Requirements](docs/00_PROJECT_REQUIREMENTS.md)
- [Reference baseline](docs/01_REFERENCE_BASELINE.md)
- [RC benchmark references](docs/02_RC_BENCHMARKS.md)
- [System architecture](docs/03_SYSTEM_ARCHITECTURE.md)
- [Mass budget](docs/04_MASS_BUDGET.md)
- [Verification plan](docs/05_DESIGN_VERIFICATION.md)

## CAD
FreeCAD 1.1.4 is the active headless-first CAD workflow under `migration/freecad`. The legacy Fusion add-in under `cad/fusion/F14TomcatRC` is retained only for traceability and unavoidable legacy inspection/export. It must not be used for new F14 design work and is closed immediately after any such legacy task.


