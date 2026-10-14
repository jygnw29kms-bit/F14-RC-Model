# F-14 center wingbox crosstie retention — v97/v98

## v97 structural screen
The existing 6 x 4 mm CF cross-ties were screened against the conservative legacy 1.4 kg, 8 g, 70/30 asymmetric load case (19.221 Nm root bending moment).

With the intended 50/50 front/rear load sharing:
- front tie couple force: 600.66 N; axial stress 38.24 MPa; pinned Euler buckling FoS 2.83
- rear tie couple force: 565.32 N; axial stress 35.99 MPa; pinned Euler buckling FoS 3.01

The deliberately pessimistic single-frame sensitivity gives 1.42–1.50 Euler buckling FoS. The actual tube modulus/strength must still be verified from the selected stock.

## v98 retention correction
The old v34 socket was 10 mm long at |Y|=68…78 mm, but the 144 mm cross-tie ended at |Y|=72 mm. Actual tube engagement was therefore only 4 mm.

v98 extends the socket mainly inboard to |Y|=50…74 mm while keeping the existing tube end at |Y|=72 mm. Actual engagement becomes 22 mm without drilling the carbon tube.

Verified CAD results:
- minimum tube engagement: 22.0 mm
- cylindrical interface area per socket: 414.69 mm²
- all four sockets: 100% contained by the fuselage clearance body
- all four sockets engage their lower fork
- dense 20–68° sweep collision screen: zero residual collisions
- required average interface shear at intended load share: 1.45 MPa front / 1.36 MPa rear
- pessimistic one-frame sensitivity: 2.90 / 2.73 MPa

## Mass penalty and next step
The longer solid sockets increase estimated socket mass by about 6.9 g in PETG compared with v34. This is acceptable for a structural prototype but not automatically accepted for the final weight budget. v99 will hollow/rib the non-load-bearing socket regions while preserving the 22 mm engagement, fork overlap and sweep clearance.

No transverse retention hole through the 6 x 4 carbon tube is permitted. Actual carbon stock, adhesive/process and physical center-box proof remain open release gates.