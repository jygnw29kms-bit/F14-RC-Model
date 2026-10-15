import json,pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v163=json.loads((root/'analysis/material_aware_mass_rollup_v163.json').read_text())
v165=json.loads((root/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/cg_v165/F14_v165_battery_retention_tray_audit.json').read_text())
old_vol=v163['sources']
new_tray_vol=v165['geometry']['tray_volume_cm3']
# Rebuild from v163 scenario structure, replacing only tray mass with corrected v165 volume.
rows=[]
for s in v163['scenarios']:
    tray=new_tray_vol*s['secondary_print_density_g_cm3']
    total_geom=s['hardpoint_pair_g']+tray+s['inlet_walls_g']+s['carbon_crossties_g']
    projected=total_geom+s['provisional_hardware_g']+s['baseline_remaining_allocations_g']
    q=dict(s)
    q['battery_tray_g']=tray
    q['geometry_quantified_g']=total_geom
    q['projected_total_g']=projected
    q['margin_1050_g']=1050-projected
    q['margin_1100_g']=1100-projected
    q['margin_1200_g']=1200-projected
    q['internal_print_hardpoint_plus_tray_g']=q['hardpoint_pair_g']+tray
    q['internal_print_target_70g_margin_g']=70-q['internal_print_hardpoint_plus_tray_g']
    rows.append(q)
best=min(rows,key=lambda x:x['projected_total_g']); worst=max(rows,key=lambda x:x['projected_total_g'])
result={
 'status':'V166_MASS_ROLLUP_UPDATED_FOR_CORRECTED_V165_RETENTION_TRAY',
 'supersedes_for_current_geometry':'analysis/material_aware_mass_rollup_v163.json',
 'correction':'v165 corrected retention tray volume is 25.455 cm3 versus v158 22.115 cm3; mass screen updated without changing other provisional allocations.',
 'v165_tray_volume_cm3':new_tray_vol,
 'scenarios':rows,'best_screen':best,'worst_screen':worst,
 'decision':{
   '1050g_target_plausible_all_screened_material_combinations':all(x['margin_1050_g']>=0 for x in rows),
   'worst_screen_margin_to_1050_g':worst['margin_1050_g'],
   'worst_internal_print_target_70g_margin_g':worst['internal_print_target_70g_margin_g'],
   'retention_fix_does_not_trigger_mass_redesign':worst['margin_1050_g']>0 and worst['internal_print_target_70g_margin_g']>0,
   'do_not_lighten_terminal_hardpoints_before_physical_retention_proof':True
 },
 'release':{'hardware_masses_measured':False,'materials_frozen':False,'AUW_frozen':False,'flight_release':False}
}
(root/'analysis/mass_rollup_retention_corrected_v166.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'best':best,'worst':worst,'decision':result['decision']},indent=2))