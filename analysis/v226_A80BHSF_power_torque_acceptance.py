import json, math
from pathlib import Path
R=Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
c=json.loads((R/'analysis/v40_candidate23.json').read_text())
servo_torque_Nm=36.0*0.0980665
horn_r_mm=17.0
travel=c['slider_travel_mm']; half=travel/2.0
beta=math.acos(half/horn_r_mm)
servo_travel_deg=180.0-2.0*math.degrees(beta)
min_effective_horn_mm=horn_r_mm*math.sin(beta)
max_slider_force_N=servo_torque_Nm/(min_effective_horn_mm/1000.0)
per_rod=max_slider_force_N/2.0
min_wing_torque_Nm=per_rod*(c['min_linkage_moment_arm_mm']/1000.0)
provisional_servo_Nm=2.0
res={
 'status':'V226_A80BHSF_POWER_TORQUE_ACCEPTANCE_SCREEN',
 'sources':{
   'servo':'AGFRC A80BHSF V2 current manufacturer datasheet checked 2026-10-26',
   'bec':'Hobbywing UBEC 10A HV PN30608000 current manufacturer data checked 2026-10-26',
   'kinematics':'analysis/v40_candidate23.json'
 },
 'servo':{'model':'AGFRC A80BHSF V2','weight_g':79,'voltage_V':8.4,'stall_torque_kgcm':36,'stall_torque_Nm':servo_torque_Nm,'loading_current_A':5.0,'operating_travel_deg':180,'travel_tolerance_deg':10,'speed_s_per_60deg':0.071,'dimensions_mm':[40,20,37.5]},
 'kinematics':{'slider_travel_mm':travel,'servo_horn_radius_mm':horn_r_mm,'required_servo_travel_deg':servo_travel_deg,'travel_margin_to_nominal_180deg':180-servo_travel_deg,'minimum_effective_servo_horn_arm_mm':min_effective_horn_mm,'min_wing_linkage_moment_arm_mm':c['min_linkage_moment_arm_mm']},
 'torque_screen':{'previous_provisional_servo_stall_Nm':provisional_servo_Nm,'actual_to_provisional_torque_factor':servo_torque_Nm/provisional_servo_Nm,'max_theoretical_slider_force_at_stall_N':max_slider_force_N,'per_rod_force_equal_split_N':per_rod,'minimum_theoretical_wing_torque_capacity_each_side_Nm':min_wing_torque_Nm},
 'bec':{'model':'Hobbywing UBEC 10A HV','PN':'30608000','output_V':8.4,'continuous_A':10,'instantaneous_A':25,'servo_loading_current_A':5.0,'continuous_headroom_factor_vs_servo_loading_current':10/5.0,'instantaneous_headroom_factor_vs_servo_loading_current':25/5.0,'input_4S_compatible':True},
 'gates':{
   'servo_travel_pass':servo_travel_deg <=170.0,
   'actual_servo_torque_exceeds_2Nm_provisional_screen':servo_torque_Nm>provisional_servo_Nm,
   'UBEC_continuous_vs_published_loading_current_pass':10>=5,
   'UBEC_peak_vs_published_loading_current_pass':25>=5,
   'stall_current_known':False,
   'servo_output_horn_real_part_verified':False,
   'installed_current_temperature_bench_pass':False,
   'mechanism_proof_load_pass':False,
   'flight_release':False
 }
}
(R/'analysis/v226_A80BHSF_power_torque_acceptance.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))