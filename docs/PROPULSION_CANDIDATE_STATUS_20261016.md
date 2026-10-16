# Propulsion candidate status - 16 October 2026

These are executed development results, not a finished or flight-released aircraft.

| Result | Evidence | Remaining limits |
|---|---|---|
| Joined inlet/adapter walls: valid connected native solids, normal surface gaps above 0.8 mm | [Native topology audit](../analysis/independent_reviews/joined_inlets_20261015/F14_joined_inlet_audit.json) | Actual fan fit, upstream inlet, attachment and flow performance |
| Candidate fan face X658; assumed OD52.5 x73.5 housing and expanded OD54.5 envelope contained bilaterally | [Placement audit](../analysis/independent_reviews/shifted_edf_interface_20261015/F14_shifted_edf_interface_audit.json) | Candidate loft only; real shroud/flange/cables and mechanism registration |
| Parametric internal exhaust with six user parameters; ratios0.85/0.90/0.95 regenerate and baseline restores | [Regeneration audit](../analysis/independent_reviews/parametric_exhaust_20261016/F14_parametric_exhaust_regeneration_audit.json) | Hub28 mm and exit-area policy assumed; original external nozzle not established |
| Eight bilateral regenerated exhaust containment screens pass | [Variant audit](../analysis/independent_reviews/exhaust_variant_containment_20261016/F14_parametric_exhaust_variant_containment_audit.json) | Candidate continuous interpolation is not original-aircraft fidelity |
| Four duct walls: 21.50393649 cm3, analytic PLA mass27.09496 g | [Layout audit](../analysis/independent_reviews/internal_propulsion_layout_20261015/F14_internal_layout_audit.json) | Assumed density1.26; excludes EDF/mounts/adhesive and does not establish aircraft CG |
| Actual local P2S0.4/0.20 Standard/PLA inlet slice:311 layers, estimated18.31 g | [Inlet slicer trial](../manufacturing/candidates/inlet_slice_trial_20261015/trial_review.json) | Geometric trial material; seam/fit/physical process unverified |
| Actual local exhaust slice:117 layers, estimated6.33 g | [Exhaust slicer trial](../manufacturing/candidates/exhaust_slice_trial_20261016/slice_audit.json) | Same qualification limits; no printer transmission |

The two slicer estimates total24.64 g, while native volume times assumed density
gives27.09496 g. These are different estimates and must not be combined or reported
as a measured part mass. Printed mass, seams, leakage, retention and EDF thrust/current
require physical evidence before release.

Priority remains original continuous exterior and common-frame assembly integration,
followed by actual hardware interfaces, retention and appropriate structural/flow
verification. Existing candidate files must not be marked production-ready.
