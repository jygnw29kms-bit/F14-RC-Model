import FreeCAD as App, json, os
base=r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad"
v=App.openDocument(os.path.join(base,'F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'))
g=App.openDocument(os.path.join(base,'F14_ORIGINAL_GLOVE_PLAN_GUIDES.FCStd'))
out={'guides':{},'wing_root':{}}
for name in ['PLAN_UPPER_GLOVE_COMPONENT','PLAN_LOWER_GLOVE_COMPONENT']:
 o=g.getObject(name); pts=[]
 for vert in o.Shape.Vertexes: pts.append([vert.Point.x,vert.Point.y])
 out['guides'][name]={'points':pts,'aftmost':max(pts,key=lambda p:p[0])}
for name in ['WING_R','WING_L']:
 o=v.getObject(name); verts=[[q.Point.x,q.Point.y,q.Point.z] for q in o.Shape.Vertexes]
 if name.endswith('R'): iy=min(p[1] for p in verts)
 else: iy=max(p[1] for p in verts)
 near=[p for p in verts if abs(p[1]-iy)<1e-5]
 # unique XY
 xy=[]
 for p in near:
  q=[p[0],p[1]]
  if q not in xy: xy.append(q)
 out['wing_root'][name]={'inner_y':iy,'points_xy':sorted(xy),'forward':min(xy,key=lambda p:p[0]),'aft':max(xy,key=lambda p:p[0])}
print(json.dumps(out,indent=2))
