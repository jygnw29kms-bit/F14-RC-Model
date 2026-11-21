"""Revisionsbound root load-path basis; historical hardware dimensions are unfrozen concepts."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];paths={
 'current_root_gap':R/'analysis/v192_wing_root_pivot_interface_screen.json',
 'historical_cassette_concept':R/'analysis/pivot_cassette_screen_v30.py',
 'historical_wingbox_plan':R/'analysis/center_wingbox_monolithic_module_v105.json',
 'project_requirements':R/'docs/00_PROJECT_REQUIREMENTS.md',
 'datum_freeze_gates':R/'docs/10_ENGINEERING_CONTINUATION_20261006.md'}
a=json.loads(paths['current_root_gap'].read_text());gap=a['rows'][0]['pivot_point_to_wing_distance_mm'];assert all(abs(x['pivot_point_to_wing_distance_mm']-gap)<1e-10 for x in a['rows'])
cases=[]
for mass in (1.05,1.2):
 for n in (6,8):
  for side in (.5,.7):
   force=mass*9.80665*n*side
   cases.append(dict(assumed_mass_kg=mass,load_factor=n,assigned_side_lift_fraction=side,assigned_side_vertical_force_N=force,additional_pivot_moment_from_reference_root_gap_Nm=force*gap/1000))
r=dict(status='ROOT_LOADPATH_PREPARATION_NOT_HARDWARE_OR_GEOMETRY_FREEZE',source_sha256={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},current_cad_sha256=a['source_sha256'],reference_root_gap_mm=gap,
 historical_unfrozen_concept=dict(source='pivot_cassette_screen_v30.py',metal_pivot_diameter_mm=6,generic_bearing_size_mm=[6,13,5],boss_outer_diameter_mm=24,fore_aft_lug_contact_chord_mm=40,lug_height_mm=16,actual_hardware_selected=False,physical_dimensions_measured=False),
 reaction_screen=dict(assumption='Conservatively assign selected fraction of total n*m*g lift to one wing; not an aerodynamic simulation.',formula='F_side=m*g*n*fraction; added moment=F_side*reference_root_gap',cases=cases),
 design_requirements=['Root bending must enter dedicated fore/aft hard contacts and central wingbox; printed skin and pin alone are not the load path.',
 'Connect carbon spar/caps to root hardpoints with explicit transfer geometry; do not count reference envelopes as structural parts.',
 'Check actual shaft alloy, bearing ratings, thrust faces, retention, load eccentricity and anisotropic print properties before sizing release.'],
 freeze_gates=['Second-source pivot registration and actual pivot waterline/bearing stack.','Registered fixed glove/body envelope and 20..68 degree continuous sweep packaging.','Current wing spar/root transfer geometry and selected hardware dimensions.','Material allowables, joint load analysis, mass and physical proof evidence.'],
 limits=['1.05/1.2 kg are design/redesign screens, not measured AUW.','Added root-gap moment is one geometric contribution, not total root bending moment.','No stress/FOS, simulation, CAD root bridge, hardware acceptance or physical test produced.'],mechanical_detail_release=False,print_release=False,flight_release=False)
(R/'analysis/v192_root_loadpath_preparation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'gap_mm':gap,'cases':len(cases),'max_added_moment_Nm':max(x['additional_pivot_moment_from_reference_root_gap_Nm'] for x in cases)}))
