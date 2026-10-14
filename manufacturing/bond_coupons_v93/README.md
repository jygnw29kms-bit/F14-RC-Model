# F14 v93 bond-process coupons

These coupons qualify the printed-material / surface-preparation / adhesive process against the corrected v92 wing-insert bond requirement.

## Geometry
- bar: 70 x 15 x 2.4 mm
- specified overlap: 10 x 15 mm = 150 mm2
- print at least 10 bars per test condition to make 5 lap joints
- optional 0.15 / 0.20 / 0.25 mm shim STLs are setup aids only; measure the cured bondline rather than assuming a one-layer printed shim is exact

## Required load
v92 conservative requirement: 1.670412 MPa average bond shear at the already SF3-amplified model torsion load.
For 150 mm2 overlap the minimum load is 250.562 N, about 25.55 kgf.
Use a controlled pull fixture/load cell and guards; do not test by hanging unsecured masses.

## Test matrix
Each exact combination is its own process. Do not pool results across filament, adhesive or preparation.
1. actual flight-print material (PETG and ASA separately while both remain candidates)
2. as-printed cleaned surface vs lightly abraded + cleaned surface
3. each candidate adhesive separately
4. nominal bondline 0.15 / 0.20 / 0.25 mm as applicable
5. full adhesive cure per its manufacturer
6. baseline room-condition set and a warm-condition screen at 40 C

## Acceptance
For a five-specimen condition:
- every specimen >= 250.562 N
- no adhesive-interface separation below that load
- coefficient of variation <= 20%; otherwise treat the process as insufficiently controlled
- record failure mode: substrate, cohesive adhesive, adhesive-interface, mixed, grip failure

Passing flat coupons does not release the aircraft. A representative v89 joint coupon must subsequently survive the geometry-specific torsion test.