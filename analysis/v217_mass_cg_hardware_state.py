import json
from pathlib import Path
base=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v213_current_mass_rollup.json").read_text())
old=base['projected_total_g']; total=old + (44-40) + 35
bat=202;travel=70;authority=bat/total*travel
res={'status':'V217_MASS_CG_WITH_TORQ_DUAL_HV_POWER','base_v213_g':old,'changes_g':{'stabilator_servos_budget_40_to_2x_TORQ22':4.0,'second_taileron_UBEC10A_HV':35.0},'projected_total_g':total,'working_target_g':1175,'redesign_threshold_g':1200,'margin_to_1200_g':1200-total,'battery':{'mass_g':bat,'center_positions_mm':[305,340,375],'travel_mm':travel,'CG_authority_mm_at_projected_AUW':authority},'published_twin_EDF_thrust_g':1800,'published_static_thrust_to_weight':1800/total,'decision':{'1050_target_retired':True,'1150_target_exceeded_slightly':total>1150,'1175_working_target':True,'1200_redesign_threshold_retained':True,'battery_travel_retained':True,'ballast_last_resort':True},'gates':{'actual_component_masses_measured':False,'installed_thrust_measured':False,'dry_CG_measured':False,'AUW_frozen':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v217_mass_cg_hardware_state.json").write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
