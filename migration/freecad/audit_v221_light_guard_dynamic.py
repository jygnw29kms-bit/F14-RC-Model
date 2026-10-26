import FreeCAD as App, Part, json, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); kin=json.loads((R/'analysis/F14_sweep_linkage_kinematics_v40.json').read_text()); c=kin['top_candidates'][23]; sm={int(r['sweep_deg']):r for r in c['samples']}; out=R/'migration/freecad/freecad_v221_light_guard_dynamic_audit.json'; shift=108.7860812043256; px=504.3463093769572; py=125.20927023775282; sy=float(c['slider_attach_y_mm'])
rows=[]; worst=None
for lab,sgn in [('R',1),('L',-1)]:
 guard=Part.makeCylinder(22.0,25.0,App.Vector(px,sgn*py,-12.5)).cut(Part.makeCylinder(20.8,25.0,App.Vector(px,sgn*py,-12.5)))
 for sw in range(20,69,2):
  r=sm[sw]; sx=r['slider_x_mm']-shift; cp=App.Vector(r['crank_pin_mm'][0]-shift,sgn*abs(r['crank_pin_mm'][1]),5); sp=App.Vector(sx,sgn*sy,5); v=cp-sp; rod=Part.makeCylinder(2.0,v.Length,sp,v); dist=guard.distToShape(rod)[0]; rec={'side':lab,'sweep_deg':sw,'distance_mm':dist}; rows.append(rec); worst=rec if worst is None or dist<worst['distance_mm'] else worst
res={'status':'V221_LIGHT_GUARD_DYNAMIC','sample_step_deg':2,'minimum_guard_to_rod_mm':worst['distance_mm'],'worst':worst,'rows':rows,'gates':{'dynamic_20_68_guard_rod_clearance_ge_1p5mm':worst['distance_mm']>=1.5,'guard_strength_verified':False,'print_release':False,'flight_release':False}}
out.write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps({k:res[k] for k in ['status','minimum_guard_to_rod_mm','worst','gates']},indent=2))