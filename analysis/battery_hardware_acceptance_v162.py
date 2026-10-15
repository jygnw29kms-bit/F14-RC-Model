import json, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v152=json.loads((root/'analysis/cg_battery_tray_v152.json').read_text())
v157=json.loads((root/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/cg_v157/F14_v157_battery_skeleton_tray_audit.json').read_text())
ref=v152['reference_pack_only_not_frozen']
result={
 'status':'V162_BATTERY_HARDWARE_DIMENSION_MASS_ACCEPTANCE_GATE',
 'sources':['analysis/cg_battery_tray_v152.json','workspace/RC-F14-Tomcat/Fusion/Exports/Current/cg_v157/F14_v157_battery_skeleton_tray_audit.json','analysis/battery_retention_architecture_v156.json'],
 'currently_CAD_proven_reference':{
   'candidate':ref['candidate'],'dimensions_mm':ref['dimensions_mm'],'mass_g':ref['mass_g'],
   'battery_center_travel_mm':70,
   'proven_center_positions_mm':[x['center_x_mm'] for x in v157['reference_pack_travel_checks']],
   'all_three_positions_pass':all(x['pass'] for x in v157['reference_pack_travel_checks'])
 },
 'automatic_acceptance_without_new_CAD':{
   'maximum_dimensions_mm':[106,36,25],
   'maximum_mass_g':240,
   'required_connector_orientation':'must remain within the v155 20 mm connector service allowance and carry no restraint load',
   'note':'The dimension limits are not a generic tray maximum. They are the envelope actually proven at all three 70 mm travel positions.'
 },
 'if_candidate_exceeds_any_limit':[
   'do not reduce the 70 mm CG travel silently',
   'rerun battery-envelope and actual-tray collision checks with measured dimensions',
   'rerun v160 dry-airframe CG authority using the measured battery mass and resulting usable center travel',
   'rerun 20 g retention load using measured battery mass',
   'verify connector service and strap routing'
 ],
 'mandatory_measurements_before_freeze':['exact pack length, width and height including hard wire exit/bulge','mass with final connector','connector/lead bend envelope','three 10 s installed twin-EDF full-power runs: minimum voltage, total current and temperature','post-run swelling/dimensional change check'],
 'electrical_acceptance':{
   'capacity_is_not_a_geometry_acceptance_metric':True,
   'label_C_rating_is_not_acceptance_evidence':True,
   'pack_must_pass_installed_sag_current_temperature_gate':True,
   'reference_capacity_mAh':1800,
   'larger_capacity_allowed_only_if_measured_geometry_and_mass_requalify':True
 },
 'release':{'specific_battery_frozen':False,'measured_pack_dimensions_verified':False,'installed_power_bench_pass':False,'retention_proof_pass':False,'flight_release':False}
}
(root/'analysis/battery_hardware_acceptance_v162.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))