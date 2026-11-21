from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();master=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';study=R/'migration/freecad/FLANGED_WEB_BONDLINE_UNFROZEN_TRIAL_ONLY.FCStd';basis=R/'analysis/v192_cap_width_inner_envelope.json';b=json.loads(basis.read_text())['rows'][0];inputs={str(p):sha(p) for p in (master,study,basis)}
out=R/'analysis/v192_inboard_cap_extension_trial.json';log=out.with_suffix('.jsonl');path=R/'migration/freecad/INBOARD_CAP_EXTENSIONS_UNFROZEN_TRIAL_ONLY.FCStd';assert not out.exists() and not log.exists() and not path.exists()
def stage(name,**kw):
 with log.open('a') as f:f.write(json.dumps(dict(stage=name,**kw))+'\n')
 print(name,flush=True)
a=App.openDocument(str(master));old=App.openDocument(str(study));d=App.newDocument('INBOARD_CAP_EXTENSIONS_TRIAL');rows=[]
try:
 wing=a.getObject('WING_R').Shape;y0=149;plane=Part.makePlane(2000,2000,App.Vector(-1000,y0,1000),App.Vector(0,1,0),App.Vector(1,0,0));sec=wing.section(plane);bb=sec.BoundBox;x0=bb.XMin+.35*(bb.XMax-bb.XMin)
 for side in ('lower','upper'):
  wires=[]
  for y,x in ((y0,x0),(185,b['x_center_mm'])):
   lo,hi=b[side+'_cap_z_interval_mm'];pts=[App.Vector(x-8,y,lo),App.Vector(x+8,y,lo),App.Vector(x+8,y,hi),App.Vector(x-8,y,hi)];wires.append(Part.makePolygon(pts+[pts[0]]))
  s=Part.makeLoft(wires,True,True);assert s.isValid() and len(s.Solids)==1;stage('outside_wing',side=side);outside=s.cut(wing).Volume;stage('boundary_gap',side=side);gap=s.Shells[0].distToShape(wing.Shells[0])[0]
  cap=old.getObject('UNFROZEN_'+side.upper()+'_CAP').Shape;face_area=0
  for f in s.Faces:
   if abs(f.BoundBox.YMin-185)>1e-7 or f.BoundBox.YLength>1e-7:continue
   for g in cap.Faces:
    if abs(g.BoundBox.YMin-185)<1e-7 and g.BoundBox.YLength<1e-7:face_area+=f.common(g).Area
  o=d.addObject('PartDesign::Feature','UNFROZEN_'+side.upper()+'_INBOARD_EXTENSION');o.Shape=s
  rows.append({'side':side,'valid':True,'solids':1,'volume_mm3':s.Volume,'outside_wing_volume_mm3':outside,'minimum_outer_boundary_gap_mm':gap,'end_face_contact_area_to_existing_cap_mm2':face_area,'y_interval_mm':[149,185]})
 for o in old.Objects:
  if hasattr(o,'Shape') and not o.Shape.isNull():new=d.addObject('PartDesign::Feature',o.Name);new.Shape=o.Shape.copy()
 d.recompute();d.saveAs(str(path))
finally:App.closeDocument(d.Name);App.closeDocument(old.Name);App.closeDocument(a.Name)
assert all(sha(Path(p))==h for p,h in inputs.items())
r={'status':'INBOARD_CAP_EXTENSION_PACKAGING_ONLY_NOT_ROOT_CONNECTION','input_sha256':inputs,'output_sha256':sha(path),'rows':rows,'limits':['Extensions use constant1mm vertical thickness and16mm width at existing Y185 heights','End-face contact is a butt joint, not a continuous carbon layup or qualified bonded splice','Reference wing remains massive belowY180; no socket/removal/assembly access designed','Y149 remains outboard of pivotY125.209; pivot/root load transfer absent','Outer clearance includes proximity to root end plane; no structural or print release','Saved7body study, native reopen remains open; master unchanged'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(rows))
