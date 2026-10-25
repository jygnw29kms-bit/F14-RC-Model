import FreeCAD as App, json, os
BASE=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'
v=App.openDocument(os.path.join(BASE,'migration','freecad','F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'))
g=App.openDocument(os.path.join(BASE,'migration','freecad','F14_ORIGINAL_GLOVE_PLAN_GUIDES.FCStd'))
out={'status':'V195_GLOVE_PLAN_ALIGNMENT_SCREEN','wing':{},'glove':{},'gates':{'Y_source_backed':True,'Z_verified':False,'glove_fit_verified':False,'master_changed':False}}
for n in ['WING_R','WING_L']:
 o=v.getObject(n); b=o.Shape.BoundBox
 out['wing'][n]={'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]}
for o in g.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull():
  b=o.Shape.BoundBox
  out['glove'][o.Name]={'label':o.Label,'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]}
print(json.dumps(out,indent=2))
with open(os.path.join(BASE,'migration','freecad','freecad_v195_glove_plan_alignment_audit.json'),'w') as fh: json.dump(out,fh,indent=2)
