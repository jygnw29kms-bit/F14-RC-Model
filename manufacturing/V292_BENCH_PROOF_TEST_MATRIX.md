# F-14 v292 Bench / Proof Test Matrix

> Engineering test plan. These targets do not replace purchased-material certificates or flight test.

## WING_JOINER_ASSEMBLY
- Basis: v282 three 8x6 joiners per wing
- Proof target: `{"factor": 1.5, "seam_moment_Nm": 12.647613102681026}`
- Pass:
  - no visible cracking, tube slip or sleeve debond
  - permanent tip/set after unload <=0.5 mm at measurement point
  - no clamp/key damage

## TAIL_ROOT_FITTING_TORSION
- Basis: existing severe taileron chain screen / light v284 fitting
- Proof target: `{"factor": 2.0, "torque_Nm": 1.34}`
- Pass:
  - no D-bore slip
  - no bond-line crack or frame delamination
  - angular backlash increase <=0.25 deg after unload

## SEGMENT_C_RING_CLAMP
- Basis: v287 captive M3 C-ring retention
- Proof target: `{"axial_pull_N": 100, "cycles": 25}`
- Pass:
  - no rider sleeve axial slip >0.2 mm
  - no nut-pocket rotation or cracking
  - M3 fastener remains removable after cycling
- Note: 100 N is a retention/service proof target, not a claimed flight load derived from aero model

## EDF_ADAPTER_RING
- Basis: v291 split adapter ring family
- Proof target: `{"thermal_cycles": 3, "temperature_range_C": [20, 70], "axial_pull_N": 50}`
- Pass:
  - no shroud crushing/ovalisation
  - no adapter crack or creep preventing removal
  - measured OD unchanged within 0.1 mm after cycle
- Note: final temperature target to be checked against actual measured EDF/ESC bay temperature
