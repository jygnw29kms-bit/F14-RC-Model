import json, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v111=json.loads((root/'analysis/propulsion_aft_of_D_v111.json').read_text())
pair_claimed=v111['screen']['twin_static_thrust_benchmark_g']
weights=[1050,1100,1200,1300,1400]
retentions=[1.0,.9,.85,.8,.75]
rows=[]
for m in weights:
  rec={'auw_g':m,'cases':[]}
  for f in retentions:
    T=pair_claimed*f
    rec['cases'].append({'installed_thrust_retention':f,'pair_thrust_g':T,'static_TW':T/m})
  rows.append(rec)
# old 1800mAh battery at 80% usable, use 80A conservative pair benchmark
capacity_Ah=1.8
for current in (68,80):
    pass
out={'status':'V112_PROPULSION_INSTALLED_MARGIN_SCREEN','candidate':v111['candidate'],'pair_claimed_thrust_benchmark_g':pair_claimed,'mass_cases':rows,'electrical':{'pair_current_benchmark_A':80,'legacy_pair_current_A_QX':68,'battery_candidate_mAh':1800,'ideal_full_power_minutes_at_80A':capacity_Ah/80*60,'ideal_80pct_minutes_at_80A':capacity_Ah*.8/80*60,'minimum_ESC_each_A':50,'recommended_design_ESC_each_A':60},'decision':{'design_AUW_target_g':1100,'hard_propulsion_screen_AUW_g':1200,'structural_review_mass_1400g_is_not_mass_target':True,'minimum_desired_installed_static_TW_at_1200g':1.10,'required_pair_installed_thrust_g_at_1200g':1320,'required_retention_of_1700g_benchmark':1320/pair_claimed,'interpretation':'FMS 850g each benchmark is viable at <=1200g only if installed duct system preserves roughly 78% or more of open-air benchmark thrust. This must be measured, not assumed.'},'gates':{'installed_thrust_retention_measured':False,'pair_current_measured':False,'voltage_sag_measured':False,'esc_thermal_verified':False,'battery_C_real_verified':False,'propulsion_release':False,'flight_release':False}}
(root/'analysis/propulsion_margin_v112.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'required_retention':out['decision']['required_retention_of_1700g_benchmark'],'TW_1200_at_80pct':pair_claimed*.8/1200,'TW_1400_at_80pct':pair_claimed*.8/1400,'full_power_80pct_min':out['electrical']['ideal_80pct_minutes_at_80A']},indent=2))