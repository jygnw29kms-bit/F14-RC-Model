import FreeCAD as App, os, json
p=r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v196_GLOVE_TRANSITION_OVERLAY.FCStd"
d=App.openDocument(p)
rows=[]
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull():
  b=o.Shape.BoundBox
  rows.append({'name':o.Name,'valid':o.Shape.isValid(),'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]})
print(json.dumps({'count':len(rows),'all_valid':all(x['valid'] for x in rows),'rows':rows},indent=2))
