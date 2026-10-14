# F14 v95 carbon fabrication reference — representative joint coupon

This folder converts the existing CAD carbon reference into practical 1:1 cutting references for the 40 mm v94 representative joint coupon.

## Current candidate laminate geometry

The structural model still treats the carbon build as a candidate until actual stock and laminate properties are fixed.

At the 40 mm v94 coupon boundaries and center:

| Y station | cap width | web height | nominal cap thickness | implied web thickness |
|---:|---:|---:|---:|---:|
| 343.9688 mm | 10.8165 mm | 3.6207 mm | 1.0 mm | 0.8 mm |
| 363.9688 mm | 10.2852 mm | 3.0346 mm | 1.0 mm | 0.8 mm |
| 383.9688 mm | 9.7540 mm | 2.3231 mm | 1.0 mm | 0.8 mm |

Use two cap pieces from the cap-strip 1:1 template and one web piece from the web 1:1 template. The CSV contains 2 mm stations for dimensional inspection.

Do not scale SVG files in the printer dialog. Verify the included 10 mm scale bar with calipers before using a paper pattern. Final carbon stock dimensions and material allowables remain an open gate.

## Torsion fixture

The sacrificial v94/v95 assembly target is 2.24218 Nm. A 250 mm lever requires 8.9687 N (about 0.9146 kgf) at the load line. Apply in both directions with the coupon supported in broad conformal cradles. The eventual flight article receives only the non-destructive 1.12109 Nm proof, equivalent to 4.4844 N (about 0.4573 kgf) at 250 mm.

The printed shell must not be point-clamped. v96 will create the conformal support/lever fixture around the v94 geometry.