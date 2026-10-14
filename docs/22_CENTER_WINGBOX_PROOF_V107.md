# Center wingbox physical proof — v107

The v105/v106 geometry is a valid candidate, but it is not released for flight until the material and manufacturing process pass a real proof test.

The primary load path is axial through the front and rear crosstie sockets. For the current 1.4 kg / 8 g review case the equal-share design loads are approximately 600.7 N front and 565.3 N rear. The v107 proof target is 1.5× those loads: approximately 901 N front and 848 N rear.

Clamp only the outboard fork region (nominal abs-Y 95–135 mm). Do not support the socket/tail region abs-Y 50–90 mm, otherwise the fixture bypasses the structure being qualified. Apply load through a smooth 6 mm steel proof pin on the socket axis. Use a calibrated >=2 kN load cell and measure socket displacement with <=0.01 mm resolution.

Provisional acceptance: no cracking/delamination/layer separation, no visible socket rotation or fork separation, <=0.20 mm permanent set, <=0.10 mm bore growth, <=10% stiffness loss after proof, and survival of the full 1.5× proof load for 10 seconds. These are qualification gates, not a substitute for material datasheets or a completed flight release.

The template `manufacturing/proof_fixtures/v107/proof_log_template.csv` records the test. `analysis/evaluate_center_wingbox_proof_v107.py` evaluates the dimensional screens from the completed log.