# Normalized wing studies: volume-method review

This review concerns the separate normalized cavity, hollow-wing and Y300 partition candidates. It does not replace the active master or accept the aircraft outer form, structure, manufacture or flight.

The numerical balance guard remains 0.00001 mm3. Changing integration method changes the observed residual; the tolerance has not been relaxed. The reports retain both results:

| Operation | Default native residual (mm3) | Adaptive GK residual (mm3) |
| --- | ---: | ---: |
| Wing minus cavity minus hollow | 0.023179655851 | -9.53878043219e-09 |
| Root plus tip minus source | 0.130608986619 | 6.72094756737e-07 |

Both default residuals exceed the guard. The adaptive residuals are within it. The partition face-flux balances at two common reference points are also within it. This is numerical consistency evidence, not a rigorous bound on absolute volume. Shared surface or integration errors can cancel in a conservation equation.

The original cavity segment examined in detail had small gaps between underlying 3D curve endpoints, despite topological closure within stored tolerances. The new study explicitly approximates offset curves to B-splines and averages adjacent endpoints. This intentionally changes separate candidate geometry. All 18 shared profiles are constructed once; the 17 solids were saved and reopened, their pair coverage and native containment were checked, and their targeted fusion conserved the input volumes numerically.

The new candidates also have larger stored native tolerances and measured curve/surface distances than the original segment. Those measurements remain visible in the reports. A successful native exact-method check uses those stored tolerances and does not imply zero geometric mismatch.

A separate cross-section calculation using native slice curves gave inconsistent results. Direct ruled-surface isocurves with a calibrated 3D Green contour integral agreed with the candidate's default and adaptive volumes on the isolated segment. That agreement supports the diagnostic method for that case; it is not an absolute error certificate for the full wing.

Before any candidate promotion, complete the complementary partition Boolean checks, review the original-to-candidate geometry deviation, repeat seam/structure checks against the new artifact hashes, and validate the exported mesh and manufacturing design. Full primary-source OML and datum registration remain open. No STL/3MF production or flight release follows from these numerical balances.

Evidence: [hollow verification](v192_normalized_hollow_wing_verification.json), [partition verification](v192_normalized_partition_numeric_verification.json), [fusion verification](v192_normalized_fused_cavity_verification.json), [isolated isocurve verification](v192_snapped_candidate_iso_volume_consistency_verification.json).

