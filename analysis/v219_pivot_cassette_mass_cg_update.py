import json
from pathlib import Path
R=Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
base=json.loads((R/'analysis/v217_mass_cg_hardware_state.json').read_text())
v213=json.loads((R/'analysis/v213_current_mass_rollup.json').read_text())
mp=json.loads((R/'migration/freecad/freecad_v218_cassette_massprops.json').read_text())
old_mass=v213['quantified_geometry_g']['wingbox_PPA_CF']; old_x=503.95270557914637; new_x=mp['pair_center_x_mm']; vol=mp['pair_volume_cm3']
tmin,tmax=596.0704536162777,604.7380091718334; bat=202.0; b0,b1=305.0,375.0
scenarios=[]
for material,density in [('Bambu PPA-CF screen',1.25),('Bambu PA6-CF screen',1.09)]:
 new_mass=vol*density; total=base['projected_total_g']-old_mass+new_mass; dry=total-bat
 lower=(tmax*total-bat*b1)/dry; upper=(tmin*total-bat*b0)/dry
 scenarios.append({'material':material,'density_g_cm3':density,'cassette_pair_mass_g':new_mass,'replaced_v204_mass_g':old_mass,'mass_delta_g':new_mass-old_mass,'projected_AUW_g':total,'margin_to_1200_g':1200-total,'battery_CG_authority_mm':bat/total*(b1-b0),'dry_airframe_CG_interval_to_cover_seed_mm':[lower,upper] if lower<=upper else None,'full_seed_range_coverable_by_70mm_battery_travel':lower<=upper,'published_static_thrust_to_weight':1800/total})
res={'status':'V219_PIVOT_CASSETTE_MASS_CG_UPDATE','sources':['analysis/v217_mass_cg_hardware_state.json','analysis/v213_current_mass_rollup.json','migration/freecad/freecad_v218_cassette_massprops.json'],'old_v204_pair_center_x_mm':old_x,'v217_pair_center_x_mm':new_x,'center_shift_mm':new_x-old_x,'preliminary_CG_seed_range_mm':[tmin,tmax],'battery':{'mass_g':bat,'center_positions_mm':[305,340,375],'travel_mm':70},'scenarios':scenarios,'decision':{'PPA_CF_keeps_below_1200':scenarios[0]['projected_AUW_g']<1200,'PPA_CF_margin_under_10g':scenarios[0]['margin_to_1200_g']<10,'PA6_CF_keeps_below_1200':scenarios[1]['projected_AUW_g']<1200,'cassette_lightweighting_required_before_freeze':scenarios[0]['margin_to_1200_g']<25,'do_not_reduce_pivot_bearing_or_primary_fork_sections':True,'battery_70mm_travel_retained':all(s['full_seed_range_coverable_by_70mm_battery_travel'] for s in scenarios)},'gates':{'material_frozen':False,'actual_print_mass_measured':False,'dry_CG_measured':False,'AUW_frozen':False,'flight_release':False}}
(R/'analysis/v219_pivot_cassette_mass_cg_update.json').write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps(res,indent=2))