# Short sleeve assembly study: review status

This separate candidate is not the active seam study or aircraft master. Its sleeve spans Y296..304 mm; each sleeve bond spans 3.8 mm. The active long sleeve uses 9.8 mm per side. Nominal cylindrical bond area is therefore 38.78% of the long version; no capacity acceptance follows from this ratio.

## Executed and verified

The native short candidate was saved and reopened. The linked reports establish the declared local rigid translation range Y0..5 mm for four moving objects against ten fixed objects (40 pairs), under native numerical distance, bounds and volume assumptions. Contact is allowed by volume screens. Evidence: `v192_short_sleeve_40_pair_path_scope_verification.json` and its hash-linked reports. Root skin is included; the rest of the aircraft and tooling are omitted.

## Executed short contact and limited access checks

The four short sleeve bond contacts were measured natively and independently checked against the earlier analytical cylinder areas: carrier side 50.1398187513 mm2 and sleeve side 47.7522083346 mm2 on each half, with zero measured bond/target volume overlap. Evidence: `v192_short_sleeve_bond_contact_measurement.json` and `v192_short_sleeve_bond_contact_verification.json`. F/A values remain bookkeeping without load assignment or strength acceptance.

At tip translation +5 mm, four hypothetical radius0.25 mm, length40 mm radial probe corridors at Y302.5 were screened against 14 local bodies. The minusX corridor intersects the spar web by 0.1570796208 mm3 and is rejected. The plusX, plusZ and minusZ corridors have zero measured local volume overlap. These finite probes do not establish real applicator access, handle clearance, an approach from outside, or adhesive application feasibility. Evidence: `v192_short_sleeve_seam_probe_access_screen.json`.

## Proposed assembly sequence, not validated

1. Prepare root and tip skin/carrier subassemblies with a fixture that controls alignment.
2. Fix the sleeve to the root carrier and cure that interface with the tip removed.
3. Prepare the tip interface, place the tip at +5 mm Y, and translate it to the seam datum.
4. Hold seam position and sleeve alignment during the second cure.

Only the rigid local geometry in step 3 has supporting path evidence. Adhesive application access, wet-film displacement, trapped excess adhesive, cure sequence, fixture removal, pin access and insertion force are unresolved. This is a permanent bonded bridge, not a demonstrated detachable joint. No real adhesive or material is selected.

## Next acceptance work

Measure short bond contacts natively; then determine an accessible application/fixture concept before treating the sequence as executable. Establish sleeve loads and stiffness sharing with skin and spar before sizing the joint. Resolve the source partition volume discrepancy, aircraft OML/datum registration, print design and all aircraft checks. No print or flight release.


## Extended hypothetical probe approach

The separate plusZ screen extends a radius0.25 mm probe from the inner radial stop to 50 mm above the enclosing local Z maximum. A radius3 mm, length45 mm handle remains at least 5 mm above that maximum. Native checks measured zero positive volume overlap against all 14 listed local bodies, with unchanged CAD hashes. This supports only that hypothetical local probe approach; the remaining aircraft, a real tool, adhesive application and cure fixtures are still unverified. Evidence: `v192_short_sleeve_plusZ_probe_handle_approach.json`.

## Nominal space beyond the tip sleeve end

A connected annular corridor with radii2.0..2.1 mm at Y304.0001..310.1 mm was screened in the final pose: zero measured volume overlap with all 14 local bodies. Its volume matches the analytical annulus calculation. The 0.0001 mm offset excludes the nominal end-face tolerance region. This establishes a local empty corridor only; continuity through that excluded end region, an external outlet, adhesive flow, air escape and excess removal remain unverified. Evidence: `v192_short_sleeve_tip_end_relief_path.json`.
