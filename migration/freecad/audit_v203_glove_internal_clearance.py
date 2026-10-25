import FreeCAD as App, json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v203_INTEGRATED_FULL_MODEL_CANDIDATE.FCStd")
d=App.openDocument(str(p))
rows=[]
for side,gname,ysign in [('R','V203_GLOVE_BLEND_R',1),('L','V203_GLOVE_BLEND_L',-1)]:
 g=d.getObject(gname); gb=g.Shape.BoundBox
 for o in d.Objects:
  if o.Name==gname or not hasattr(o,'Shape') or o.Shape.isNull(): continue
  b=o.Shape.BoundBox
  # broad zone around glove
  if b.XMax < gb.XMin-5 or b.XMin > gb.XMax+5: continue
  if ysign>0 and (b.YMax < 115 or b.YMin > 165): continue
  if ysign<0 and (b.YMin > -115 or b.YMax < -165): continue
  try: dist=g.Shape.distToShape(o.Shape)[0]
  except Exception: dist=None
  rows.append({'side':side,'name':o.Name,'label':o.Label,'distance_mm':dist,'bbox':{'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]}})
rows.sort(key=lambda r:999999 if r['distance_mm'] is None else r['distance_mm'])
out={'status':'V203_GLOVE_INTERNAL_CLEARANCE_SCREEN','rows':rows,'zero_distance_objects':[r['name'] for r in rows if r['distance_mm'] is not None and r['distance_mm']<1e-6],'gates':{'review_only':True,'absolute_Z_verified':False,'production_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v203_glove_internal_clearance_audit.json").write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
