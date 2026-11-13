# UPC C–D fairing study review

The source in analysis/original_front_sources/CD_projection_samples_v2.json corrects two lower boundary picks. At raster X 1225 and 1250 the old picks fell on the separate section E drawing. The corrected points lie on the plan outline. Nine later stations lack a usable width pick because the wing obscures the outline.

| Source X (px) | Width residual of the original study loft (mm) |
| --- | ---: |
| 1225 | -12.91 |
| 1250 | -26.18 |
| 1275 | -38.66 |
| 1300 | -50.62 |

The four local fairing patches use four intermediate profiles, two assumed edge heights per side, and attachment points at 80% of each section's lateral extent. The ruled Bézier patches showed normal changes up to 1.81° across their internal segment joints at 48 sampled points. The smooth loft variants gave these measurements over X 417.820–457.354 mm in the study frame.

- 228 intermediate sections gave a maximum sampled attachment gap of 0.003886 mm and a maximum lateral deviation from the plan polyline of 0.082669 mm.
- 24 midpoint normal comparisons against the study fuselage gave 0.024°–2.205°.
- Twelve attachment curves were cut directly from the study fuselage and reopened in FreeCAD. Their comparison against the smooth patch boundaries is pending.

The smooth loft is the candidate for the next attachment test. Check positional and tangent continuity against the extracted curves before joining the surfaces. Registration to v192 and the physical edge heights remain open. The measurements apply to the isolated study.

Study loft SHA-256: A1CB207D14AC861484BCD90B3148915F8F826066CC203EE6B51205004F47FDD9

## Sewn cubic study · 13 November 2026

FreeCAD produced one valid open shell from 56 patches. The reopened shell gave one intersection at each of six previously double-hit positions. The 165 internal seam samples gave position differences below 0.000001 mm and a maximum normal angle of about 0.0000012°. At the 56 patch midpoints, the largest measured offsets were 0.000056 mm to the inner attachment curve and 0.000235 mm to the outer study guide.

The measurements cover a local positive-Y portion in study coordinates. The guide height remains a design assumption. Registration to v192 and the connection to the fuselage are pending.

Local study file SHA-256: 662c5d1a292164e01a2b6256fea430e667f3d762923d2ebdbc3a5eebbd37558c
