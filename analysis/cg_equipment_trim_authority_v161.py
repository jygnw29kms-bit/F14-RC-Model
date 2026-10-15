import json, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v160=json.loads((root/'analysis/cg_dry_airframe_feasibility_v160.json').read_text())
dry=848.0
items={
 'ESC_pair_budget_g':55.0,
 'receiver_BEC_wiring_budget_g':35.0,
 'sweep_actuator_linkage_budget_g':45.0,
 'ESC_plus_receiver_power_g':90.0,
 'all_three_flexible_budget_groups_g':135.0,
}
travels=[25,50,75,100,150]
rows=[]
for name,m in items.items():
  for dx in travels:
    rows.append({'item':name,'mass_g':m,'relocation_mm':dx,'dry_CG_shift_mm':m*dx/dry})
# How much relocation is required to correct common dry-CG errors.
errors=[2,5,10,15]
corrections=[]
for name,m in items.items():
  for err in errors:
    corrections.append({'item':name,'mass_g':m,'desired_dry_CG_correction_mm':err,'required_component_relocation_mm':err*dry/m})
result={
 'status':'V161_EQUIPMENT_PLACEMENT_CG_TRIM_AUTHORITY',
 'source':'analysis/cg_dry_airframe_feasibility_v160.json',
 'reference_dry_airframe_mass_g':dry,
 'reference_required_dry_CG_interval_mm':v160['decision']['required_reference_dry_airframe_CG_interval_mm'],
 'budget_masses_not_frozen':items,
 'relocation_sensitivity':rows,
 'correction_distance_sensitivity':corrections,
 'decision':{
   'ballast_last_resort':True,
   'equipment_placement_is_primary_dry_CG_tuning_method':True,
   'example':'Moving the 90 g ESC + receiver/BEC/wiring allocation by 50 mm shifts the 848 g dry-airframe CG by about 5.31 mm.',
   'design_rule':'Keep flexible avionics and ESC mounting longitudinally relocatable until a physical dry-airframe mass/CG measurement exists.',
   'freeze_rule':'Do not permanently bond flexible electronics trays before measured dry CG confirms the v160 interval or an equipment-placement correction is calculated.'
 },
 'release':{'component_masses_measured':False,'component_mount_stations_frozen':False,'dry_CG_trim_verified':False,'flight_release':False}
}
(root/'analysis/cg_equipment_trim_authority_v161.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'90g_50mm_shift':90*50/dry,'90g_100mm_shift':90*100/dry,'135g_50mm_shift':135*50/dry,'decision':result['decision']},indent=2))