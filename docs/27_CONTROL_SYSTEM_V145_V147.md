# F-14 control system v145-v147

Baseline flight control is two independently driven all-moving stabilators mixed for pitch and differential roll. This avoids baseline aileron servos and wiring through the variable-sweep wings. Wing spoilers/other roll devices remain optional until a taileron authority test proves they are needed.

The NASA-derived model stabilator is 1.520 dm² per side. A sensitivity screen places the design servo class above 6 kg·cm, The initial 10/15 mm linkage screen produced a 14 kg·cm preferred class, but v148 replaces it with an 8/20 mm linkage. The severe 60 m/s sensitivity then requires about 7.8 kg·cm including the same linkage loss and 2x factor, so the hardware gate becomes a 10 kg·cm nominal class. This is a hardware class, not a final servo release, because the true stabilator pivot axis and hinge moment remain to be source-verified.

Each stabilator uses an external metal shaft/bearing system. The servo output does not serve as the aerodynamic bearing. Candidate linkage starts at 8 mm servo arm / 20 mm stabilator crank (about ±17.9° surface for ±50° servo travel) and must use retained ball links or positive clevises. Total neutral freeplay must stay below 0.5°.

Receiver power starts with a dedicated 7.4 V HV BEC class of at least 10 A continuous / 15 A peak. Final BEC selection is based on measured servo/sweep peak currents and a brownout test; unverified ESC BEC outputs are not paralleled.
