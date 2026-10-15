import json, pathlib, math
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v159=json.loads((root/'analysis/current_mass_rollup_v159.json').read_text())
v108=json.loads((root/'analysis/center_wingbox_material_screen_v108.json').read_text())
vol=v159['geometry_volumes_cm3']
mat108={m['name']:m for m in v108['materials']}
hardpoint_materials={
 'Bambu PPA-CF':float(mat108['Bambu PPA-CF']['density_g_cm3']),
 'Bambu PA6-CF':float(mat108['Bambu PA6-CF']['density_g_cm3']),
}
secondary_print={'ASA_screen':1.07,'PETG_screen':1.27}
carbon=[1.50,1.60,1.70]
provisional=v159['provisional_hardware']
other=v159['baseline_other_target_allocations_g']
rows=[]
for hp_name,hp_rho in hardpoint_materials.items():
  for sec_name,sec_rho in secondary_print.items():
    for crho in carbon:
      hp=vol['v105_hardpoint_pair']*hp_rho
      tray=vol['v158_battery_tray']*sec_rho
      inlet=vol['allowanced_inlet_wall_pair']*sec_rho
      tubes=vol['two_6x4x144_carbon_tubes']*crho
      geometry=hp+tray+inlet+tubes
      prov=sum(float(x) for x in provisional.values())
      baseline=sum(float(x) for x in other.values())
      total=geometry+prov+baseline
      rows.append({
       'hardpoint_material':hp_name,'hardpoint_density_g_cm3':hp_rho,
       'secondary_print_material':sec_name,'secondary_print_density_g_cm3':sec_rho,
       'carbon_density_g_cm3':crho,
       'hardpoint_pair_g':hp,'battery_tray_g':tray,'inlet_walls_g':inlet,'carbon_crossties_g':tubes,
       'geometry_quantified_g':geometry,'provisional_hardware_g':prov,'baseline_remaining_allocations_g':baseline,
       'projected_total_g':total,'margin_1050_g':1050-total,'margin_1100_g':1100-total,'margin_1200_g':1200-total,
       'internal_print_hardpoint_plus_tray_g':hp+tray,'internal_print_target_70g_margin_g':70-(hp+tray)
      })
best=min(rows,key=lambda x:x['projected_total_g']); worst=max(rows,key=lambda x:x['projected_total_g'])
result={
 'status':'V163_MATERIAL_AWARE_MASS_ROLLUP_CORRECTS_V159',
 'supersedes':'analysis/current_mass_rollup_v159.json',
 'correction_reason':'v159 incorrectly applied ASA/PETG density sensitivity to v105 hardpoint modules even though v108 structural material path is PPA-CF/PA6-CF proof candidates.',
 'sources':['analysis/current_mass_rollup_v159.json','analysis/center_wingbox_material_screen_v108.json','workspace/RC-F14-Tomcat/Fusion/Exports/Current/center_wingbox_v105/F14_v105_monolithic_module_audit.json','workspace/RC-F14-Tomcat/Fusion/Exports/Current/cg_v158/F14_v158_battery_tray_frame_interfaces_audit.json','analysis/independent_reviews/allowanced_inlet_20261015/F14_allowanced_inlet_wall_audit.json'],
 'material_assignment':{
   'v105_hardpoints':'PPA-CF primary proof candidate or PA6-CF fallback; actual material still requires v107 proof',
   'v158_battery_tray':'ASA/PETG mass sensitivity until tray material proof/freeze',
   'allowanced_inlet_walls':'ASA/PETG mass sensitivity; structural role is duct wall, not wingbox hardpoint',
   'carbon_crossties':'density sensitivity only; exact purchased tube not frozen'
 },
 'scenarios':rows,'best_screen':best,'worst_screen':worst,
 'decision':{
   '1050g_target_plausible_all_screened_material_combinations':all(x['margin_1050_g']>=0 for x in rows),
   'worst_screen_margin_to_1050_g':worst['margin_1050_g'],
   'worst_screen_margin_to_1200_g':worst['margin_1200_g'],
   'mass_does_not_select_hardpoint_material':True,
   'hardpoint_material_selection_rule':'v107 physical proof and conditioned-state performance override small mass differences.',
   'mass_optimization_trigger':'optimize if measured/frozen rollup approaches 1100 g or subsystem hard ceilings; do not remove safety-critical material merely to chase 1050 g.'
 },
 'release':{'material_systems_frozen':False,'hardware_masses_measured':False,'shell_mass_measured':False,'AUW_frozen':False,'flight_release':False}
}
(root/'analysis/material_aware_mass_rollup_v163.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'best':best,'worst':worst,'decision':result['decision']},indent=2))