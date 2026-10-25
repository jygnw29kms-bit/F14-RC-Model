import json,math
from pathlib import Path
c=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_candidate23.json").read_text())
horn=17.0;T=2.0;dyn=2.5;DX=108.7860812043256;mid=((c['slider_x_min_mm']+c['slider_x_max_mm'])/2)-DX
rows=[]
for s in c['samples']:
 x=s['slider_x_mm']-DX; off=x-mid; y=math.sqrt(max(1e-9,horn*horn-off*off)); beta=math.degrees(math.atan2(y,off)); force=T/(y/1000); per=force/2; torque=per*(s['moment_arm_mm']/1000)
 rows.append({'sweep_deg':s['sweep_deg'],'slider_x_current_mm':x,'horn_pin_y_mm':y,'servo_angle_deg':beta,'static_total_slider_force_N':force,'static_per_rod_N':per,'theoretical_wing_torque_per_side_Nm':torque,'dynamic_total_force_2p5_N':dyn*force,'dynamic_per_rod_2p5_N':dyn*per})
worst=max(rows,key=lambda r:r['dynamic_total_force_2p5_N']); maxrod=max(r['dynamic_per_rod_2p5_N'] for r in rows)
# stress screens
m3_area=math.pi*3.0**2/4; m3_shear=maxrod/m3_area
rod4_area=math.pi*4.0**2/4; rod_ax=maxrod/rod4_area
# crank neck 14mm wide, 5 thick, 3.3 bore; net tension conservative
net_area=(14-3.3)*5; crank_net=maxrod/net_area
# bearing on 3mm pin in 5mm crank and 8mm yoke
crank_bear=maxrod/(3*5); yoke_bear=maxrod/(3*8)
res={'status':'V209_CANDIDATE23_SERVO_ROD_PIN_LOAD_SCREEN','servo':{'provisional_stall_Nm':T,'horn_radius_mm':horn,'servo_angle_min_deg':min(r['servo_angle_deg'] for r in rows),'servo_angle_max_deg':max(r['servo_angle_deg'] for r in rows),'servo_angle_travel_deg':max(r['servo_angle_deg'] for r in rows)-min(r['servo_angle_deg'] for r in rows)},'performance':{'min_theoretical_wing_torque_per_side_Nm':min(r['theoretical_wing_torque_per_side_Nm'] for r in rows),'max_static_total_slider_force_N':max(r['static_total_slider_force_N'] for r in rows),'max_dynamic_total_slider_force_N':worst['dynamic_total_force_2p5_N'],'max_dynamic_per_rod_N':maxrod,'worst_sweep_deg':worst['sweep_deg']},'stress_screen':{'M3_pin_single_shear_MPa':m3_shear,'4mm_rod_axial_MPa':rod_ax,'14x5_crank_net_section_MPa':crank_net,'3mm_pin_crank_bearing_MPa':crank_bear,'3mm_pin_yoke_bearing_MPa':yoke_bear},'samples':rows,'gates':{'kinematics_valid':True,'actual_servo_selected':False,'rod_end_material_verified':False,'pin_material_verified':False,'crank_material_verified':False,'physical_proof':False,'print_release':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v209_candidate23_servo_rod_pin_load_screen.json").write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='samples'},indent=2))
