import json, math, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v113=json.loads((root/'analysis/propulsion_local_packaging_v113.json').read_text())
v114=json.loads((root/'analysis/propulsion_duct_area_v114.json').read_text())
wall=0.8
max_fsa=max(c['fan_swept_area_mm2'] for c in v114['cases'])
rows=[]
for s in v113['sections']:
    outer=s['available_disk_diameter_mm']
    inner=max(0,outer-2*wall)
    area=math.pi*inner**2/4
    rows.append({'section':s['section'],'x_mm':s['x_mm'],'sampled_available_outer_disk_mm':outer,'assumed_duct_wall_mm':wall,'resulting_clear_inner_diameter_mm':inner,'clear_round_duct_area_mm2':area,'max_screened_single_FSA_mm2':max_fsa,'area_ratio_to_max_FSA':area/max_fsa,'100pct_FSA_area_pass':area>=max_fsa})
out={'status':'V115_D_E_F_INTAKE_AREA_SCREEN','sources':['analysis/propulsion_local_packaging_v113.json','analysis/propulsion_duct_area_v114.json'],'wall_assumption_mm':wall,'sections':rows,'result':{'D_can_carry_100pct_FSA_as_duct':rows[0]['100pct_FSA_area_pass'],'minimum_area_ratio_to_max_FSA':min(x['area_ratio_to_max_FSA'] for x in rows),'important_distinction':'D rejects the EDF shroud but does not reject a duct. Housing begins aft of D; upstream transition may remain circular or become non-circular while preserving area.'},'limitations':['uses sampled local inscribed disks from provisional source registration','does not include boundary-layer displacement, splitter thickness, surface roughness, bends or intake losses','does not prove a common continuous centerline between source sections'],'gates':{'continuous_duct_CAD_created':False,'common_axis_or_transition_verified':False,'minimum_area_along_transition_verified':False,'installed_thrust_verified':False,'propulsion_packaging_freeze':False,'flight_release':False}}
(root/'analysis/propulsion_intake_area_v115.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(rows,indent=2))