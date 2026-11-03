# Short sleeve assembly study: review status

This separate candidate is not the active seam study or aircraft master. Its sleeve spans Y296..304 mm; each sleeve bond spans 3.8 mm. The active long sleeve uses 9.8 mm per side. Nominal cylindrical bond area is therefore 38.78% of the long version; no capacity acceptance follows from this ratio.

## Executed and verified

The native short candidate was saved and reopened. The linked reports establish the declared local rigid translation range Y0..5 mm for four moving objects against ten fixed objects (40 pairs), under native numerical distance, bounds and volume assumptions. Contact is allowed by volume screens. Evidence: `v192_short_sleeve_40_pair_path_scope_verification.json` and its hash-linked reports. Root skin is included; the rest of the aircraft and tooling are omitted.

## Prepared, not executed

`audit_short_sleeve_bond_contacts.py` measures the four short sleeve bond face contacts and compares each with 2*pi*r*3.8. Its output must exist and be checked before claiming native short contact areas. It also reports F/A per 1 N as bookkeeping, without assigning a force or calculating actual joint stress.

## Proposed assembly sequence, not validated

1. Prepare root and tip skin/carrier subassemblies with a fixture that controls alignment.
2. Fix the sleeve to the root carrier and cure that interface with the tip removed.
3. Prepare the tip interface, place the tip at +5 mm Y, and translate it to the seam datum.
4. Hold seam position and sleeve alignment during the second cure.

Only the rigid local geometry in step 3 has supporting path evidence. Adhesive application access, wet-film displacement, trapped excess adhesive, cure sequence, fixture removal, pin access and insertion force are unresolved. This is a permanent bonded bridge, not a demonstrated detachable joint. No real adhesive or material is selected.

## Next acceptance work

Measure short bond contacts natively; then determine an accessible application/fixture concept before treating the sequence as executable. Establish sleeve loads and stiffness sharing with skin and spar before sizing the joint. Resolve the source partition volume discrepancy, aircraft OML/datum registration, print design and all aircraft checks. No print or flight release.
