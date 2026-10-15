# F-14 inlet/EDF v184 slicer review

This review is tied to the centerline-corrected v176 inlet/EDF Fusion archive, SHA-256 `ea6fab92314b3e9cc58afb0cdc3cddbd5a416df548012ffde3036bc45f17431a`.

## Geometry gate

Both v176 joined inlet/EDF bodies were exported by Fusion/ShapeManager as high-refinement binary STL in millimetres. Orca's independent mesh inspection reports one manifold part per side with 8,596 facets. Mesh volume differs from the native BRep by only -0.01146% (R) and -0.01390% (L).

## P2S slicer gate

The local Orca/PRINTBENCH CLI profile inheritance was flattened before slicing so inherited material values cannot fall back to generic defaults. The verified profiles are:

- Bambu Lab P2S, 0.4 mm nozzle
- 0.20 mm Standard process
- Bambu PETG Basic, material type PETG, density 1.25 g/cm3
- Textured PEI Plate

Both sides sliced successfully to 3MF with embedded G-code. Each uses 311 layers and about 7.42 cm3 filament. Estimated total time is 1:16:06 for R and 1:17:45 for L.

## Release state

This closes the current mesh/slicer compatibility gate for the v176 geometry only. It does **not** release the inlet for printing or flight. Normal wall thickness through the transition, aerodynamic smoothness, flight-material/process optimisation, real print quality, EDF hardware fit, and bench/flight proof remain open.
