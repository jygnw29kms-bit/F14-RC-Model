Recovered source A/B/C manual pixel traces from preserved legacy engineering data, tied byte-exactly to original UPC structure report page31 raster. Only pixel-space outlines and local axes promoted; old mixed-frame NASA metric fitting and provisional FS/length pairing intentionally excluded. C loops are separately traced components, not automatically valid holes in one solid. Next independently register station X, per-section scale and common vertical datum before any fuselage loft. These data do not establish continuous original OML or production geometry.

Topology audit: all five traced A/B/C straight-segment loops have finite coordinates, no zero-length edges and no nonadjacent segment intersections. The three C loop boundaries do not intersect each other. This does not establish nesting semantics, spline validity, tracing accuracy or metric registration. Reproduce with audit_pixel_topology.py; evidence in front_sections_topology_audit.json.

Original bottom-side-view A/B/C station tick X positions are now independently localized in the exact raster: 642.5, 905.5 and 1197.5 native pixels. Visually selected tick-only ROIs and threshold method are recorded in front_station_ticks.json and reproducible with locate_station_ticks.py. This replaces no aircraft datum: tick Y positions are annotation locations, not waterlines. Physical scale and aircraft station X remain unverified.

Same-source A/B plan/side envelope comparison is recorded in front_AB_envelope_comparison.json. Width-derived isotropic scaling leaves a larger A height residual than B; investigate the original section trace/station depiction before lofting. No independent width/height deformation or production acceptance is applied. Reproduce with compare_AB_envelopes.py.

Station-column sensitivity scans plus/minus five native pixels with separately selected contiguous outer-line runs (audit_station_sensitivity.py). Disconnected hatch/internal runs must not be averaged together. The report is a sensitivity experiment, not a confidence interval or a metric registration acceptance test.

Vertical registration candidates now retain separate upper- and lower-contour anchors. Their disagreement is the envelope residual; the equal-weight translation midpoint is only a study candidate. Section annotation axes are not assumed to establish a common aircraft waterline. See front_vertical_registration_candidates.json and derive_vertical_registration.py.

C loop semantics refined after direct original-raster overlay and polygon nesting checks: loop 0 encloses both disjoint inlet loops 1/2. Thus the traced pixel region supports one outer boundary with two holes, rather than three separately filled solids. C_loop_nesting_audit.json records the checks; spline topology, metric scale and 3D continuity remain unverified.

front_shared_frame_candidate.json places original A/B/C polygon traces in the existing aft candidate raster frame, retaining isotropic section scale and all side-height residuals. This is reference placement only: inherited metric scale, cross-view X alignment and C inlet-lip step remain assumptions. No continuous fuselage loft or production release is permitted by these data.

Seven original nose projection samples at native raster X450..600 are extracted reproducibly in nose_projection_samples.json. These give separate plan width and side height constraints; they do not imply ellipse sections or establish the nose-tip/pitot boundary. The inherited aft metric frame remains a candidate.

Nose-to-A coverage extends the original projection sampling to X625 and A-column X642 in nose_to_A_projection_samples.json. Dedicated side bands exclude the A label/tick; nose-gear and appendage separation still require review. Existing native nose-guide archive uses the earlier seven samples and is preserved unchanged.

Projection measurement definitions normalized in nose_to_A_stroke_center_samples.json: contiguous stroke centers and half-pixel endpoint interpolation replace outer dark bounds. Remaining A width/height residuals are retained, with no snapping or anisotropic profile deformation. Native guide attachment remains unverified.

Primary NASA CR-163098 text reviewed: PDF page20 (printed16) qualitatively describes circular forebody cross-section; page10 (printed6) identifies the tested 1/72-scale model. forebody_shape_source_evidence.json records source hash and applicability limits. This supports a clearly labeled shape study, not station-specific aircraft geometry or replacement of UPC A/B contours.

Circular forward-nose sensitivity inputs and compiled Fusion generator prepared separately from original contours. Equal-weight plan/side diameter fits retain residuals and exclude A, the tip and pitot. Not installed or executed; no native geometry or original-OML approval claimed.

Original midpoint projection extraction checked at grayscale thresholds 96/128/160 in nose_threshold_sensitivity.json. These deterministic ranges do not establish accuracy bounds. The circular study retains measurable width/height disagreements and is not promoted to original OML.

A-to-B forebody/canopy projections now sampled at nine original columns X675..875. Lower contours are omitted at X675/700/725 where the nose gear overlaps the projection; missing coordinates remain null. These constraints do not imply interpolated section shapes or verified metric registration.

B-to-C reference coverage: eleven columns X925..1175, with dorsal-antenna-overlapped upper contours omitted at X1125/1150. Plan envelopes from X975 include the fixed wing glove and must not be interpreted as fuselage-core widths. Original side/plan crops were visually reviewed. See BC_projection_samples.json.

Partial C-D projection coverage records thirteen original side columns X1225..1525. Upper appendage-overlap samples X1350/1375 and plan contours beyond X1300 remain null; swept wings obscure the fuselage envelope there. The four retained plan widths describe overall fixed-glove projection only. These data cannot establish a continuous C-D fuselage loft.

Leading-edge crop confirms separate upper/lower projected components near raster X965 with visible gaps to the central forebody. Local vertical-stroke candidates are recorded in glove_inlet_leading_edge_candidates.json; they are not a continuous fuselage boundary or verified 3D component identification.

C inner-loop plan correspondence quantified in C_inner_loop_plan_correspondence.json. Candidate isotropic lateral bounds are compared with selected plan strokes at X1197. These strokes are not yet verified aperture boundaries, so this is correspondence evidence only, not inlet fit or metric registration approval.
