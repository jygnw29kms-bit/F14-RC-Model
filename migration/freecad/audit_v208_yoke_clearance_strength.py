import FreeCAD as App,Part,json,math
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v208_YOKE_CLEARANCE_FINAL_CANDIDATE.FCStd")
d=App.openDocument(str(p));tray=d.getObject('BATTERY_TRAY_v207').Shape;service=d.getObject('V205_SWEEP_SERVO_SERVICE').Shape;body=d.getObject('V205_SWEEP_SERVO_BODY_REF').Shape
c=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_candidate23.json").read_text());DX=108.7860812043256;mid=457.3099792190261;r=17.;profile=[(-68,8),(-31,8),(-27,5),(-19,5),(-15,8),(15,8),(19,5),(27,5),(31,8),(68,8)]
def yoke(x):
 pts=[App.Vector(x+w,y,2.5) for y,w in profile]+[App.Vector(x-w,y,2.5) for y,w in reversed(profile)];sh=Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(App.Vector(0,0,8));sh=sh.cut(Part.makeBox(5,13,8.4,App.Vector(x-2.5,7,2.3)))
 for yy in [65,-65]:sh=sh.cut(Part.makeCylinder(1.65,8.4,App.Vector(x,yy,2.3)))
 return sh
rows=[]
for s in c['samples']:
 x=s['slider_x_mm']-DX;sh=yoke(x)
 for name,t in [('tray',tray),('servo_service',service),('servo_body',body),('wingbox_R',d.getObject('V204_MONO_LOWER_R').Shape),('wingbox_L',d.getObject('V204_MONO_LOWER_L').Shape)]:rows.append({'sweep_deg':s['sweep_deg'],'target':name,'distance_mm':sh.distToShape(t)[0]})
# exact scotch-yoke force screen, 2.0 Nm provisional servo, 2.5 dynamic factor
forces=[]
for s in c['samples']:
 x=s['slider_x_mm']-DX;off=x-mid;yp=math.sqrt(max(0,r*r-off*off));lever_m=yp/1000;F=2.0/lever_m;forces.append({'sweep_deg':s['sweep_deg'],'pin_y_mm':yp,'static_slider_force_N':F,'dynamic_total_force_N':2.5*F,'dynamic_per_side_N':1.25*F})
worst=max(forces,key=lambda q:q['dynamic_total_force_N']);per=worst['dynamic_per_side_N']
# neck y 23 to rod y65: 42mm lever; section 10mm x-width x 8mm z-thickness, bending about z
M_neck=per*42;W_neck=8*10**2/6;stress=M_neck/W_neck
# central normal width 16, conservative 65mm lever
M_center=per*65;W_center=8*16**2/6;stress_center=M_center/W_center
pin_bearing=worst['dynamic_total_force_N']/(4.0*8.0) # 4mm pin x 8mm thickness
res={'status':'V208_YOKE_CLEARANCE_AND_STRENGTH_SCREEN','clearance':{'minimum':min(rows,key=lambda q:q['distance_mm']),'minimum_by_target':{t:min(q['distance_mm'] for q in rows if q['target']==t) for t in sorted(set(q['target'] for q in rows))},'passes_gt_1mm':all(q['distance_mm']>1.0 for q in rows)},'load_screen':{'provisional_servo_stall_Nm':2.0,'dynamic_factor':2.5,'worst_force':worst,'neck_bending_moment_Nmm':M_neck,'neck_section_modulus_mm3':W_neck,'neck_nominal_bending_stress_MPa':stress,'neck_1p5x_concentration_MPa':1.5*stress,'center_nominal_bending_stress_MPa':stress_center,'servo_pin_nominal_bearing_MPa':pin_bearing},'gates':{'2deg_clearance_gt_1mm':all(q['distance_mm']>1 for q in rows),'stress_screen_complete':True,'actual_material_allowable_verified':False,'actual_servo_torque_verified':False,'physical_proof':False,'print_release':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v208_yoke_clearance_strength_audit.json").write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
