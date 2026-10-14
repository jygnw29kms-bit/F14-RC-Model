# Center wingbox material gate — v108

The v105/v106 hardpoint geometry is acceptable, but material selection remains a proof-qualified gate.

Current printed proof candidates:

1. **PPA-CF** — strongest published XY bending candidate (208 MPa dry / 202 MPa wet). It offers the largest margin against the v105 58.68 MPa tip-load sensitivity, but its Z-direction strength is not established by the data used here and the P2S operates at the lower edge of its recommended temperature window. It is therefore a proof candidate, not an automatic release.
2. **PA6-CF** — 151 MPa XY dry and 80 MPa Z dry, with a large wet-state reduction (95 MPa XY / 45 MPa Z). It fits comfortably in the P2S temperature range, but moisture conditioning is mandatory.
3. **PAHT-CF** — more moisture-stable, but only 61 MPa Z dry / 49 MPa Z wet; requires proof with favorable orientation.
4. **PET-CF** — good dimensional/moisture behavior but only 49 MPa Z dry; not preferred for the monolithic hardpoint.
5. **PPS-CF** — excluded from the P2S baseline because its recommended nozzle range begins above the P2S 300 °C maximum.

Target orientation is the lower fork plate on the build plate so the primary crosstie Y-axis load is carried predominantly in the XY print plane. The v107 proof remains mandatory because the socket region still introduces interlayer shear/peel and local stress concentrations.

If printed candidates fail proof, retain the v105 envelope but change the hardpoint to a G10/CF-laminate or metal structural module rather than weakening the proof criteria.