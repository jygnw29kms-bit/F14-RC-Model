# F-14 EDF axis adapter v176 review

Fusion/ShapeManager review of the corrected ellipse-to-circle inlet transition.

- The previous x=658 mm fan-face center was displaced by 1.381637 mm from the source-derived inlet centerline.
- v176 moves the nominal fan face to y=+/-66.284584861 mm, z=-10.508688348 mm while preserving the exact x=650 mm annular inlet interface.
- Both joined inlet/adapter solids are valid, connected, and manifold by the native BRep edge/face checks.
- The assumed 52.5 mm EDF housing, 54.5 mm housing+skin/service envelope, and 55.2 mm mount candidate all remain fully contained in the current source envelope on both sides.
- Fan hardware dimensions are still assumed, not measured. Normal wall thickness through the transition, aerodynamic smoothness, mechanism clearance, slicing, print release, and flight release remain open gates.

This is a geometry/packaging candidate, not a manufacturing release.
