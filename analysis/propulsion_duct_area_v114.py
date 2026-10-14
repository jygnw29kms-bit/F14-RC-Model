import json, math, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
# 50 mm rotor; hub diameter not yet measured, so screen a realistic sensitivity range.
rotor=50.0
hub_cases=[22,24,26,28]
rows=[]
for hub in hub_cases:
    fsa=math.pi/4*(rotor**2-hub**2)
    eq=math.sqrt(4*fsa/math.pi)
    outlets=[]
    for ratio in (.80,.85,.90,1.00):
        area=fsa*ratio
        d=math.sqrt(4*area/math.pi)
        outlets.append({'FSA_ratio':ratio,'area_mm2':area,'equivalent_round_diameter_mm':d})
    rows.append({'hub_diameter_mm':hub,'fan_swept_area_mm2':fsa,'equivalent_open_diameter_mm':eq,'outlet_sensitivity':outlets})
# Conservative design basis uses largest hub -> smallest FSA for required flow area? For inlet sizing use largest FSA = smallest hub.
max_fsa=max(x['fan_swept_area_mm2'] for x in rows)
min_fsa=min(x['fan_swept_area_mm2'] for x in rows)
out={'status':'V114_TWIN_50MM_DUCT_AREA_TARGETS_PREPARED','rotor_diameter_mm':rotor,'hub_diameter_unverified_sensitivity_mm':hub_cases,'cases':rows,'twin_targets':{'max_screened_twin_FSA_mm2':2*max_fsa,'min_screened_twin_FSA_mm2':2*min_fsa,'inlet_design_target_policy':'maintain >=100% total FSA after boundary-layer/structure deductions until installed thrust testing proves otherwise','outlet_screen_range':'80-90% FSA sensitivity only; final nozzle ratio selected by thrust/current bench test'},'architecture':{'EDF_housing_starts_aft_of_D':True,'station_D_role':'non-circular intake/transition duct only','station_E_role':'EDF entry / shroud packaging gate','station_F_role':'EDF and exhaust transition continuity gate'},'gates':{'actual_FMS_hub_diameter_measured':False,'D_usable_duct_area_measured':False,'E_usable_duct_area_measured':False,'F_usable_duct_area_measured':False,'continuous_inlet_area_verified':False,'outlet_ratio_bench_selected':False,'installed_thrust_verified':False,'flight_release':False}}
(root/'analysis/propulsion_duct_area_v114.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'max_single_FSA_mm2':max_fsa,'max_twin_FSA_mm2':2*max_fsa,'26mm_hub_FSA':next(x['fan_swept_area_mm2'] for x in rows if x['hub_diameter_mm']==26),'26mm_85pct_outlet_d_mm':next(y['equivalent_round_diameter_mm'] for y in next(x for x in rows if x['hub_diameter_mm']==26)['outlet_sensitivity'] if y['FSA_ratio']==.85)},indent=2))