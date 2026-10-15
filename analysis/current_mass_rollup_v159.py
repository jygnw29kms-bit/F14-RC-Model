import json, math, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
# Source values are intentionally explicit; every non-measured value remains labelled provisional/sensitivity.
v105=json.loads((root/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/center_wingbox_v105/F14_v105_monolithic_module_audit.json').read_text())
v158=json.loads((root/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/cg_v158/F14_v158_battery_tray_frame_interfaces_audit.json').read_text())
inlet=json.loads((root/'analysis/independent_reviews/allowanced_inlet_20261015/F14_allowanced_inlet_wall_audit.json').read_text())
v147=json.loads((root/'analysis/control_servo_power_acceptance_v147.json').read_text())
v144=json.loads((root/'analysis/propulsion_hardware_acceptance_v144.json').read_text())
v152=json.loads((root/'analysis/cg_battery_tray_v152.json').read_text())
# Volumes
hardpoint_vol=sum(x['volume_cm3'] for x in v105['records'])
tray_vol=v158['geometry']['tray_with_interfaces_volume_cm3']
inlet_vol=sum(x['wall_material_volume_cm3'] for x in inlet['wall_candidates'])
# Project-level density sensitivities only, not material release values.
density={'ASA_screen_g_cm3':1.07,'PETG_screen_g_cm3':1.27}
# Cross ties: 2 tubes, 6x4, 144 mm from v97.
tube_area_mm2=math.pi*(6**2-4**2)/4
tube_pair_vol_cm3=tube_area_mm2*144*2/1000
carbon_density_screen=[1.50,1.60,1.70]
# Hardware candidates / budget values.
edf_pair_g=150.0  # two XFly candidate units at published 75 g; not frozen
battery_ref_g=202.0
servo_pair_pref_g=float(v147['mass_budget']['two_stabilator_servos_preferred_total_g_max'])
# Remaining budget lines intentionally kept as baseline allocations, not actual mass.
other_target={
 'printed_aerodynamic_shells_g':250.0,
 'esc_pair_g':55.0,
 'sweep_actuator_linkage_g':45.0,
 'receiver_bec_wiring_g':35.0,
 'fasteners_bearings_inserts_g':35.0,
 'finish_paint_decals_g':40.0,
 'reserve_g':50.0,
}
scenarios=[]
for mat,rho in [('ASA',density['ASA_screen_g_cm3']),('PETG',density['PETG_screen_g_cm3'])]:
    hp=hardpoint_vol*rho; tray=tray_vol*rho; inletm=inlet_vol*rho
    internal=hp+tray
    for crho in carbon_density_screen:
        tubes=tube_pair_vol_cm3*crho
        quantified=internal+inletm+tubes
        provisional=edf_pair_g+battery_ref_g+servo_pair_pref_g
        known_plus_prov=quantified+provisional
        baseline_other=sum(other_target.values())
        projected=known_plus_prov+baseline_other
        scenarios.append({
          'printed_material':mat,'carbon_density_screen_g_cm3':crho,
          'hardpoint_modules_g':hp,'battery_tray_g':tray,'inlet_walls_g':inletm,'carbon_crossties_pair_g':tubes,
          'quantified_geometry_mass_g':quantified,
          'provisional_hardware_mass_g':provisional,
          'known_plus_provisional_g':known_plus_prov,
          'baseline_other_allocations_g':baseline_other,
          'projected_with_baseline_allocations_g':projected,
          'margin_to_1050_g':1050-projected,
          'margin_to_1100_g':1100-projected,
          'margin_to_1200_redesign_g':1200-projected,
          'internal_print_target_70g_margin_g':70-internal,
          'internal_print_hard_90g_margin_g':90-internal,
        })
# Best/worst among screened combinations.
best=min(scenarios,key=lambda x:x['projected_with_baseline_allocations_g'])
worst=max(scenarios,key=lambda x:x['projected_with_baseline_allocations_g'])
result={
 'status':'V159_CURRENT_MASS_ROLLUP_SCREEN_NOT_FINAL_AUW',
 'source_quality':{
   'geometry_quantified':['v105 hardpoint module volumes','v158 tray+frame-interface volume','allowanced inlet wall volumes'],
   'provisional_hardware':['XFly 50 mm EDF candidate published mass 75 g each','Tattu 1800mAh reference battery 202 g','stabilator servo preferred pair budget <=40 g'],
   'budget_only':['shells','ESCs','sweep actuator/linkage','receiver/BEC/wiring','fasteners/bearings/inserts','finish','reserve'],
   'warning':'This is a convergence screen, not a measured ready-to-fly AUW.'
 },
 'geometry_volumes_cm3':{'v105_hardpoint_pair':hardpoint_vol,'v158_battery_tray':tray_vol,'allowanced_inlet_wall_pair':inlet_vol,'two_6x4x144_carbon_tubes':tube_pair_vol_cm3},
 'density_sensitivities':density,
 'provisional_hardware':{'edf_pair_g':edf_pair_g,'battery_reference_g':battery_ref_g,'stabilator_servo_pair_preferred_max_g':servo_pair_pref_g},
 'baseline_other_target_allocations_g':other_target,
 'scenarios':scenarios,
 'best_screen':best,
 'worst_screen':worst,
 'decision':{
   '1050g_design_target_currently_plausible':best['margin_to_1050_g']>=0,
   '1100g_upper_design_target_currently_plausible':worst['margin_to_1100_g']>=0,
   '1200g_redesign_threshold_margin_positive_all_scenarios':worst['margin_to_1200_redesign_g']>0,
   'preferred_print_material_for_mass_if_strength_proof_allows':'ASA','reason':'Current quantified internal-print geometry is lighter under the project density sensitivity; final choice remains physical-proof/material dependent.',
   'next_mass_gate':'replace baseline allocations with measured/frozen masses as EDF, ESC, BEC, sweep actuator, fasteners and shell print settings freeze; optimize only if projected AUW approaches 1100 g or any subsystem hard ceiling is exceeded.'
 },
 'release':{'mass_rollup_measured':False,'hardware_mass_frozen':False,'shell_mass_verified':False,'AUW_frozen':False,'flight_release':False}
}
(root/'analysis/current_mass_rollup_v159.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'volumes_cm3':result['geometry_volumes_cm3'],'best':best,'worst':worst,'decision':result['decision']},indent=2))