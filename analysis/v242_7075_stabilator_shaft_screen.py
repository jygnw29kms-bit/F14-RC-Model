import json
from pathlib import Path
R=Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
v149=json.loads((R/'analysis/control_stabilator_pivot_shaft_v149.json').read_text())
v174=json.loads((R/'analysis/control_stabilator_d_shaft_v174.json').read_text())
vol_pair=2*1.680589067446606
m_steel=vol_pair*7.85
m_7075=vol_pair*2.81
row=next(x for x in v149['screen']['shaft_rows'] if x['shaft_d_mm']==6)
dflat=v174['load_screen']['1p5x_stress_concentration_screen_MPa']
res={'status':'V242_7075_STABILATOR_SHAFT_SCREEN','geometry':{'pair_volume_cm3':vol_pair,'diameter_mm':6.0,'round_abs_y_mm':[45,76],'D_abs_y_mm':[76,106]},'mass':{'steel_density_g_cm3':7.85,'steel_pair_g':m_steel,'7075_density_g_cm3':2.81,'7075_pair_g':m_7075,'saving_g':m_steel-m_7075},'stress':{'v149_combined_von_mises_MPa':row['combined_von_mises_MPa'],'v149_7075_yield_SF':row['7075T6_400MPa_yield_SF'],'v174_D_flat_1p5x_screen_MPa':dflat,'7075_400MPa_SF_at_D_flat_screen':400/dflat},'decision':{'7075_static_strength_screen_pass':row['7075T6_400MPa_yield_SF']>=5 and 400/dflat>=5,'mass_reason_to_prefer_7075':m_steel-m_7075>10,'bearing_wear_interface_is_remaining_primary_material_gate':True,'preferred_candidate':'7075-T6 precision shaft with bearing journal finish/hardness wear test; steel remains fallback if journal wear/fretting fails'},'gates':{'7075_certificate_verified':False,'journal_surface_finish_specified':False,'bearing_journal_wear_test_pass':False,'D_flat_machining_tolerance_verified':False,'proof_moment_0p67Nm_100cycles_pass':False,'flight_release':False}}
(R/'analysis/v242_7075_stabilator_shaft_screen.json').write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps(res,indent=2))