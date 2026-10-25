import FreeCAD as App, Part, json, pathlib
R=pathlib.Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model")
d=App.openDocument(str(R/'migration/freecad/F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'))
f=d.getObject('FUSELAGE_CURRENT').Shape
ys=[148.8263775443693,130.8263775443693]
samples=[(490,-3.85),(492,-4.03),(496,-4.25),(500,-4.45),(504.346,-4.742),(508,-4.85),(512,-4.95),(516,-5.05),(520,-5.10)]
clear=1.0
rows=[]
for x,wz in samples:
 rec={'x_mm':x,'wing_lower_proxy_z_mm':wz,'target_outer_glove_z_mm':wz-clear}
 for y in ys:
  line=Part.makeLine(App.Vector(x,y,-100),App.Vector(x,y,100))
  sec=f.section(line)
  zs=sorted([v.Point.z for v in sec.Vertexes])
  key='outer' if y==ys[0] else 'inner'
  rec[key+'_fuselage_z_mm']=zs
  if zs:
   rec[key+'_fuselage_lower_z_mm']=zs[0]
 if 'outer_fuselage_lower_z_mm' in rec:
  rec['required_outer_lowering_mm']=rec['outer_fuselage_lower_z_mm']-rec['target_outer_glove_z_mm']
 if 'inner_fuselage_lower_z_mm' in rec:
  # candidate inner rail = target outer -1.5
  inner_target=rec['target_outer_glove_z_mm']-1.5
  rec['target_inner_glove_z_mm']=inner_target
  rec['required_inner_lowering_mm']=rec['inner_fuselage_lower_z_mm']-inner_target
 rows.append(rec)
vals=[r['required_outer_lowering_mm'] for r in rows if 'required_outer_lowering_mm' in r]
out={'status':'V200_GLOVE_ENVELOPE_VS_CURRENT_FUSELAGE','rows':rows,'outer_required_lowering_range_mm':[min(vals),max(vals)] if vals else None,'interpretation':'positive lowering means candidate glove lower surface must sit below current fuselage lower boundary to preserve 1 mm wing-root clearance','gates':{'review_only':True,'absolute_Z_verified':False,'production_OML':False}}
(R/'migration/freecad/freecad_v200_glove_envelope_vs_fuselage_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
