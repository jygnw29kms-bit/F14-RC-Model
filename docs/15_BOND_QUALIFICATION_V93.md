# F-14 wing joint bond qualification — v93

## Basis
The v92 pointwise audit reduced the verified usable wing-insert bond area to a conservative 66.3576 mm2. The governing v81 worst-airfoil-edge x1.5 dynamic torsion case is 747.392 Nmm. With the project SF3 gate this corresponds to 2.24218 Nm and 110.8445 N equivalent interface force. On the v92 lower-bound area this requires 1.67041 MPa average bond shear.

## Stage A — process coupons
Use `manufacturing/bond_coupons_v93/`. A 10 x 15 mm lap overlap is 150 mm2, so the v92 requirement scales to 250.562 N. Five specimens are required for each exact material/preparation/adhesive/conditioning process.

A condition passes only when every specimen reaches 250.562 N, there is no adhesive-interface failure below that load, and the coefficient of variation is <=20%. The purpose is to qualify the complete process, not a nominal adhesive datasheet value.

## Stage B — representative joint coupon
A sacrificial geometry-representative v89 joint sample will be produced next. It must survive 2.24218 Nm in both torsional directions without insert/skin/carbon-path failure before structural release can proceed.

## Stage C — assembled flight article
The actual flight article is not destructively proofed to SF3. After the sacrificial joint and material/process gates pass, the assembled wing receives a non-destructive torsional proof of 1.12109 Nm (1.5 x the v81 dynamic worst-case torsion), followed by visual inspection and re-measurement for permanent set/slip.

## Open gates
Fit clearance, adhesive/process qualification, warm-condition qualification, representative-joint torsion, and flight-article proof all remain open. No print or flight release yet.