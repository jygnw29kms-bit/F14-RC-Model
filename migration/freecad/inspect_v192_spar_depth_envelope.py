from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(src)
out=R/'analysis/v192_spar_depth_envelope.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists()
def stage(**kw):
 with log.open('a') as h:h.write(json.dumps(kw)+'\n')
d=App.openDocument(str(src));rows=[]
try:
 w=d.getObject('WING_R').Shape
 for y in (155,180,220,300,380,440):
  stage(stage='section',y=y)
  plane=Part.makePlane(2000,2000,App.Vector(-1000,y,1000),App.Vector(0,1,0),App.Vector(1,0,0));s=w.section(plane);assert len(s.Edges)>0
  b=s.BoundBox;chord=b.XMax-b.XMin;assert chord>0
  for frac in (.25,.35,.45):
   x=b.XMin+frac*chord;stage(stage='vertical_intersection',y=y,fraction=frac)
   line=Part.makeLine(App.Vector(x,y,-100),App.Vector(x,y,100));inside=w.common(line)
   assert len(inside.Edges)==1
   z=sorted(v.Point.z for v in inside.Vertexes);assert len(z)==2 and z[1]>z[0]
   rows.append({'y_mm':y,'fraction_of_section_X_bounds':frac,'x_mm':x,'section_X_bounds_mm':[b.XMin,b.XMax],'z_bottom_mm':z[0],'z_top_mm':z[1],'vertical_outer_depth_mm':z[1]-z[0]})
finally:App.closeDocument(d.Name)
assert sha(src)==before and len(rows)==18
r={'status':'NATIVE_READ_ONLY_VERTICAL_OUTER_DEPTH_SAMPLES','source_sha256':before,'rows':rows,'limits':['Outer reference depth, not available inner depth: skin, adhesive, tolerances and spar caps not subtracted','Chord fractions use section X bounds; not a selected spar axis','18 local samples do not prove a continuous straight spar fits','No stresses, hardware choice, cavity modification, structure or print release'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage(stage='complete',rows=len(rows));print('18 outer vertical depth samples verified; source unchanged')
