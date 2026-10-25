import json,math
from pathlib import Path
vol=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v213_current_geometry_volumes.json").read_text())['rows']
V={r['name']:r['volume_cm3'] for r in vol}
# geometry candidates
hard=(V['V204_MONO_LOWER_R']+V['V204_MONO_LOWER_L']+V['V204_UPPER_FORK_R']+V['V204_UPPER_FORK_L'])*1.25
tray=V['BATTERY_TRAY_v207']*1.07
inlet=14.825460934091986
crossties=6.785840131753954
# Yoke + crank candidate in 7075
alu=(V['V210_SYNC_YOKE_M4_20']+V['V210_CRANK_M4_R_20']+V['V210_CRANK_M4_L_20'])*2.80
# rods as 4x2 CF tube, L from candidate23
c=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_candidate23.json").read_text());L=c['rod_length_mm'];area=math.pi/4*(4**2-2**2);rodpair=2*area*L/1000*1.6
# real/current hardware
hw={'EDF_pair':150.0,'battery':202.0,'stabilator_servos_pair_budget':40.0,'sweep_servo_A80BHSF':79.0,'sweep_UBEC_10A_HV':35.0,'ESC_pair':72.0,'receiver_and_signal_wiring_budget':25.0,'fasteners_bearings_inserts_budget':35.0}
other={'printed_aero_shells_budget':250.0,'finish_paint_decals_budget':40.0,'reserve':50.0}
quant={'wingbox_PPA_CF':hard,'battery_tray_ASA':tray,'inlet_walls_ASA':inlet,'carbon_crossties':crossties,'7075_yoke_cranks_solid':alu,'CF_4x2_rods_pair':rodpair}
known=sum(quant.values())+sum(hw.values());total=known+sum(other.values())
res={'status':'V213_CURRENT_MASS_ROLLUP_WITH_REAL_SWEEP_HARDWARE','quantified_geometry_g':quant,'hardware_and_budgets_g':hw,'remaining_allocations_g':other,'known_plus_current_budgets_g':known,'projected_total_g':total,'margins_g':{'to_1050':1050-total,'to_1100':1100-total,'to_1200_redesign':1200-total},'published_twin_EDF_thrust_g':1800,'published_static_thrust_to_projected_weight':1800/total,'installed_thrust_gate':{'minimum_g':1000,'preferred_g':1200},'decision':{'1050_target_rejected_current_hardware':total>1050,'1100_target_rejected_current_hardware':total>1100,'1200_redesign_threshold_margin_positive':total<1200,'new_working_AUW_target_g':1150,'hard_redesign_threshold_g':1200,'lightweighting_focus':['7075 yoke pockets after FEA/strength screen','shell print mass','wiring/fastener real masses'],'do_not_reduce':['wingbox pivot load path','1mm packaging clearances','battery 70mm travel']},'gates':{'actual_EDF_mass_measured':False,'EDF_shroud_OD_verified':False,'actual_battery_mass_measured':False,'actual_shell_mass_verified':False,'AUW_frozen':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v213_current_mass_rollup.json").write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
