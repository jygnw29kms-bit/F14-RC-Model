from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();master=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';study=R/'migration/freecad/FLANGED_WEB_BONDLINE_UNFROZEN_TRIAL_ONLY.FCStd';basis=R/'analysis/v192_cap_width_inner_envelope.json';b=json.loads(basis.read_text());inputs={str(p):sha(p) for p in (master,study,basis)}
out=R/'analysis/v192_continuous_inboard_cap_build.json';path=R/'migration/freecad/CONTINUOUS_INBOARD_CAPS_UNFROZEN_STUDY_ONLY.FCStd';assert not out.exists() and not path.exists();a=App.openDocument(str(master));old=App.openDocument(str(study));d=App.newDocument('CONTINUOUS_INBOARD_CAPS_STUDY');rows=[]
try:
 w=a.getObject('WING_R').Shape;plane=Part.makePlane(2000,2000,App.Vector(-1000,149,1000),App.Vector(0,1,0),App.Vector(1,0,0));bb=w.section(plane).BoundBox;root=dict(b['rows'][0]);root['y_mm']=149;root['x_center_mm']=bb.XMin+.35*(bb.XMax-bb.XMin)
 for side in ('lower','upper'):
  wires=[]
  for r in [root]+b['rows']:
   x=r['x_center_mm'];y=r['y_mm'];half=r['cap_width_mm']/2;lo,hi=r[side+'_cap_z_interval_mm'];pts=[App.Vector(x-half,y,lo),App.Vector(x+half,y,lo),App.Vector(x+half,y,hi),App.Vector(x-half,y,hi)];wires.append(Part.makePolygon(pts+[pts[0]]))
  s=Part.makeLoft(wires,True,True);assert s.isValid() and len(s.Solids)==1;outside=s.cut(w).Volume;assert outside<=1e-6
  o=d.addObject('PartDesign::Feature','CONTINUOUS_'+side.upper()+'_CAP_REFERENCE');o.Shape=s
  rows.append({'object':o.Name,'valid':True,'solids':1,'volume_mm3':s.Volume,'outside_wing_volume_mm3':outside,'y_bounds_mm':[s.BoundBox.YMin,s.BoundBox.YMax]})
 for o in old.Objects:
  if hasattr(o,'Shape') and not o.Shape.isNull() and 'CAP' not in o.Name:new=d.addObject('PartDesign::Feature',o.Name);new.Shape=o.Shape.copy()
 assert len(d.Objects)==5;d.recompute();d.saveAs(str(path))
finally:App.closeDocument(d.Name);App.closeDocument(old.Name);App.closeDocument(a.Name)
d=App.openDocument(str(path))
try:
 assert len(d.Objects)==5
 for o in d.Objects:assert o.Shape.isValid() and len(o.Shape.Solids)==1
finally:App.closeDocument(d.Name)
assert all(sha(Path(p))==h for p,h in inputs.items())
r={'status':'SIX_SECTION_CONTINUOUS_CAP_ENVELOPES_SAVED_REOPENED','input_sha256':inputs,'output_sha256':sha(path),'rows':rows,'reopened_valid_single_solids':5,'limits':['One CAD solid per cap removes butt-joint geometry atY185 but does not establish continuous carbon fibres, forming method or manufacturing','Ruled loft has slope changes at stations; laminate bending radius and construction remain unresolved','Web/flanges/bond layers retained onlyY185..435; root support and load transfer missing','Reference wing is massive belowY180; sockets/assembly access not designed','No pivot attachment, bearing selection, original glove registration, material or structural release'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(rows))
