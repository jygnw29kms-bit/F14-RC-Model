import FreeCAD as App, Part, json, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); kinp=R/'analysis/F14_sweep_linkage_kinematics_v40.json'; out=R/'migration/freecad/freecad_v215_pivot_guard_dynamic_audit.json'
kin=json.loads(kinp.read_text(encoding='utf-8')); c=kin['top_candidates'][23]; samples={int(r['sweep_deg']):r for r in c['samples']}; shift=108.7860812043256; px=504.3463093769572; py=125.20927023775282; sy=float(c['slider_attach_y_mm'])
rows=[]; worst=None
for lab,sgn in [('R',1),('L',-1)]:
 center=App.Vector(px,sgn*py,-13.5); ring=Part.makeCylinder(22,27,center).cut(Part.makeCylinder(20.5,27,center))
 for sw in range(20,69,2):
  r=samples[sw]; sx=r['slider_x_mm']-shift; cp=App.Vector(r['crank_pin_mm'][0]-shift,sgn*abs(r['crank_pin_mm'][1]),5); sp=App.Vector(sx,sgn*sy,5); vec=cp-sp; rod=Part.makeCylinder(2.0,vec.Length,sp,vec)
  dist=ring.distToShape(rod)[0]; rec={'side':lab,'sweep_deg':sw,'ring_to_rod_mm':dist}; rows.append(rec)
  if worst is None or dist<worst['ring_to_rod_mm']: worst=rec
res={'status':'V215_PIVOT_GUARD_DYNAMIC','ring_inner_radius_mm':20.5,'ring_outer_radius_mm':22.0,'wing_radial_min_mm':23.61710730661649,'wing_radial_clearance_mm':1.61710730661649,'minimum_ring_to_rod_mm':worst['ring_to_rod_mm'],'worst':worst,'rows':rows,'gates':{'wing_clearance_ge_1p5mm':1.61710730661649>=1.5,'dynamic_rod_clearance_ge_1p5mm':worst['ring_to_rod_mm']>=1.5,'sampled_20_68_complete':True,'production_OML':False,'print_release':False,'flight_release':False}}
out.write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps({k:res[k] for k in ['status','wing_radial_clearance_mm','minimum_ring_to_rod_mm','worst','gates']},indent=2))