import json,math
from pathlib import Path
c=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_candidate23.json").read_text())
T=36*9.80665/100 # 36 kg-cm to N-m
horn=17.;dyn=2.5;DX=108.7860812043256;mid=((c['slider_x_min_mm']+c['slider_x_max_mm'])/2)-DX
rows=[]
for s in c['samples']:
 x=s['slider_x_mm']-DX; off=x-mid; y=math.sqrt(max(1e-9,horn**2-off**2));F=T/(y/1000);per=F/2
 rows.append({'sweep_deg':s['sweep_deg'],'pin_y_mm':y,'static_slider_force_N':F,'dynamic_total_N':dyn*F,'dynamic_per_side_N':dyn*per,'wing_torque_per_side_Nm':per*s['moment_arm_mm']/1000})
worst=max(rows,key=lambda r:r['dynamic_total_N']); per=worst['dynamic_per_side_N']
# existing v208 yoke section 10mm x 8mm at neck, concentration 1.5
M=per*42;W=8*10**2/6;nom=M/W;peak=1.5*nom
center=per*65/(8*16**2/6)
pin_shear=per/(math.pi*3**2/4);rod=per/(math.pi*4**2/4);crank=per/((14-3.3)*5);crank_bear=per/(3*5);yoke_bear=per/(3*8)
res={'status':'V210_A80BHSF_FULL_STALL_MECHANISM_SCREEN','servo':{'model':'AGFRC A80BHSF/A80BHS V2 geometry equivalent','voltage_V':8.4,'published_stall_kgcm':36,'stall_Nm':T,'dimensions_mm':[40,20,37.5],'travel_deg':180},'loads':{'dynamic_factor':dyn,'worst':worst,'minimum_static_wing_torque_per_side_Nm':min(r['wing_torque_per_side_Nm'] for r in rows)},'stress_existing_v208':{'yoke_neck_nominal_MPa':nom,'yoke_neck_1p5x_MPa':peak,'yoke_center_nominal_MPa':center,'M3_pin_single_shear_MPa':pin_shear,'4mm_rod_axial_MPa':rod,'crank_net_section_MPa':crank,'crank_pin_bearing_MPa':crank_bear,'yoke_pin_bearing_MPa':yoke_bear},'material_implication':{'FDM_structural_yoke_rejected':True,'aluminum_or_CF_laminate_required':True,'specific_alloy_not_released':True},'samples':rows,'gates':{'servo_dimensions_fit_envelope':True,'servo_torque_exceeds_2Nm_provisional':True,'full_stall_load_screen_complete':True,'actual_servo_purchased_verified':False,'material_allowable_verified':False,'BEC_current_verified':False,'physical_proof':False,'print_release':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v210_A80BHSF_full_stall_mechanism_screen.json").write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='samples'},indent=2))
