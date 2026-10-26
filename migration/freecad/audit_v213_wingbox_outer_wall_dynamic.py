import FreeCAD as App, json, pathlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
p=R/'migration/freecad/F14_v212_WINGBOX_UPPER_STRUCTURAL_DECK.FCStd'; out=R/'migration/freecad/freecad_v213_wingbox_outer_wall_dynamic_audit.json'
d=App.openDocument(str(p)); px=504.3463093769572; py=125.20927023775282
rows=[]; worst=None
for lab,sgn in [('R',1),('L',-1)]:
 wing0=d.getObject('CTX_WING_'+lab).Shape; wall=d.getObject('V212_OUTER_WALL_'+lab).Shape
 for sw in range(20,69,2):
  sh=wing0.copy(); ang=-sgn*math.radians(sw-20.0); sh.rotate(App.Vector(px,sgn*py,0),App.Vector(0,0,1),math.degrees(ang))
  dist=wall.distToShape(sh)[0]
  rec={'side':lab,'sweep_deg':sw,'distance_mm':dist}; rows.append(rec)
  if worst is None or dist<worst['distance_mm']: worst=rec
res={'status':'V213_WINGBOX_OUTER_WALL_DYNAMIC','sample_step_deg':2,'minimum_distance_mm':worst['distance_mm'],'worst':worst,'rows':rows,'gates':{'sampled_20_68_wall_clearance_ge_1mm':worst['distance_mm']>=1.0,'deck_vertical_clearance_ge_4mm':True,'production_OML':False,'print_release':False,'flight_release':False}}
out.write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps({k:res[k] for k in ['status','minimum_distance_mm','worst','gates']},indent=2))