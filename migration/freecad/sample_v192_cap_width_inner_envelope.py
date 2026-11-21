from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];master=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';void=R/'migration/freecad/WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={str(p):sha(p) for p in (master,void)}
assert before[str(void)]==json.loads((R/'analysis/v192_void_all17_fusion.json').read_text())['output_sha256']
out=R/'analysis/v192_cap_width_inner_envelope.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists()
def stage(**kw):
 with log.open('a') as f:f.write(json.dumps(kw)+'\n')
a=App.openDocument(str(master));b=App.openDocument(str(void));rows=[]
try:
 w=a.getObject('WING_R').Shape;objs=[o for o in b.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objs)==1;c=objs[0].Shape
 for y in (185,220,300,380,435):
  stage(stage='section',y=y);plane=Part.makePlane(2000,2000,App.Vector(-1000,y,1000),App.Vector(0,1,0),App.Vector(1,0,0));s=w.section(plane);bb=s.BoundBox;xc=bb.XMin+.35*(bb.XMax-bb.XMin)
  width=16-8*(y-185)/250;zs=[]
  for frac in (-.5,-.25,0,.25,.5):
   x=xc+frac*width;stage(stage='inner_vertical_line',y=y,x=x);inside=c.common(Part.makeLine(App.Vector(x,y,-100),App.Vector(x,y,100)));assert len(inside.Edges)==1
   z=sorted(v.Point.z for v in inside.Vertexes);assert len(z)==2;zs.append({'x_mm':x,'bottom_mm':z[0],'top_mm':z[1]})
  low=max(q['bottom_mm'] for q in zs);high=min(q['top_mm'] for q in zs)
  # .2mm is a study reserve at sampled vertical bounds, not bond qualification.
  lower=[low+.2,low+1.2];upper=[high-1.2,high-.2]
  rows.append({'y_mm':y,'x_center_mm':xc,'cap_width_mm':width,'sampled_inner_bounds':zs,'sampled_common_vertical_interval_mm':[low,high],'assumed_cap_thickness_mm':1,'assumed_vertical_reserve_mm':.2,'lower_cap_z_interval_mm':lower,'upper_cap_z_interval_mm':upper,'cap_centroid_separation_mm':(sum(upper)-sum(lower))/2,'remaining_web_height_mm':upper[0]-lower[1]})
finally:App.closeDocument(b.Name);App.closeDocument(a.Name)
assert all(sha(Path(p))==v for p,v in before.items()) and len(rows)==5
r={'status':'NATIVE_INNER_CAP_WIDTH_SAMPLES_ONLY','input_sha256':before,'rows':rows,'limits':['Five chordwise points at each of five span stations; not continuous-width or continuous-span containment','16-to-8mm tapered width and 1mm caps are unfrozen historical concepts','0.2mm vertical study reserve is not normal clearance, adhesive or tolerance acceptance','No cap solids, web, bonded root connection, buckling, orthotropic material or structural release'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage(stage='complete');print([(r['y_mm'],r['cap_centroid_separation_mm'],r['remaining_web_height_mm']) for r in rows])
