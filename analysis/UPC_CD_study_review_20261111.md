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

## Body intersection screen · 14 November 2026

The local C–D study fuselage was cropped to X 417.981–443.992 mm in study coordinates and reopened as one valid solid. Of 280 sampled shell points, 115 classified inside the cropped fuselage. A separate FreeCAD section and inside/outside classification found one crossing at 43 of 56 section midpoints and three crossings at the other 13. These 13 sampled positions lie between X 421.759 and 429.429 mm. The trim path remains unresolved.

Crossing report SHA-256: ab9afef2bfc282984b6a0d6dbbaac617dd7c6283c6840a066ccc323b82c7c098

## Follow-up trim checks · 15 November 2026

Of 168 sampled sections, 131 showed one crossing and 37 showed three in the tested interior parameter range. The longest intersection wire spans 26.012 mm in X. After excluding hits near the patch boundaries, seven of its 39 sampled X planes still contain three hits. In the second region the 17 recorded edges form a connected sequence with reversals in X. Selecting intersections by transverse order alone leaves the trim unresolved.

FreeCAD identified one valid closed intersection wire with three edges and a total length of 0.133 mm. Its X bounds are 427.164 to 427.229 mm in study coordinates. The physical significance of this local feature remains unresolved.

Closed-wire report SHA-256: 81b30af39f0b89cc6557508be03a3edc6488b6a088425ebd5631b042a4532b2e

## Boolean trim trial

FreeCAD reported valid inside and outside results against the local body slab. The outside result includes one shell of 736.756 mm2 and eight smaller shells. The original area minus the sum of both output areas is approximately -0.000036 mm2. FreeCAD logged topology hasher mismatch warnings during the run. The largest outside component was saved separately and reopened as one valid shell with 69 faces and an unchanged area of 736.756 mm2. The topology warnings and disposition of the eight smaller components remain open. Local study file SHA-256: 70425d230512dcdf840e0beba2c00ccb5c8b29f118a66ee64c3ae0d0ac19ad1c

Boolean report SHA-256: e392fc4886799b6a74cef8da0272ecdde089f11fc8ad66903f685dd49254cae8

A repeat cut reproduced the warnings and nine valid outside shell components. The eight detached shells total 0.227406 mm2, or 0.03086% of the outside area. The component report records area, face count and bounds in study coordinates. Area alone is insufficient to decide whether these components affect the attachment.

Component report SHA-256: b6f08d9961ef433969d2689f546b90d5d85c4b05e37f5351ff077f1a4ad34b62

FreeCAD minimum distances from the eight detached shells to the largest outside shell range from 5.515 to 6.977 mm. The study coordinates and nearest-point pairs are recorded in the distance report. The trim remains a local candidate.

Distance report SHA-256: ab360f27b2cf008e6d313139334db4be8c3cf0b837835a8ebe4501c2caea1b15
