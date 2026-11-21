from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();paths=[R/'migration/freecad/FLARED_ROOT_SOCKET_UNFROZEN_CONCEPT_ONLY.FCStd',R/'migration/freecad/FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd'];before={str(p):sha(p) for p in paths};out=R/'analysis/v192_root_socket_section_samples.json';assert not out.exists();docs=[App.openDocument(str(p)) for p in paths];rows=[]
try:
 for y in (150,160,174):
  plane=Part.makePlane(2000,2000,App.Vector(-1000,y,1000),App.Vector(0,1,0),App.Vector(1,0,0))
  cap=docs[1].getObject('CONTINUOUS_LOWER_CAP_REFERENCE').Shape.section(plane);xc=(cap.BoundBox.XMin+cap.BoundBox.XMax)/2
  for d in docs:
   for o in d.Objects:
    if not hasattr(o,'Shape') or o.Shape.isNull():continue
    s=o.Shape.section(plane);assert len(s.Edges)>0
    rows.append({'y_mm':y,'object':o.Name,'local_x_origin_mm':xc,'segments_xyz_mm':[[list(v) for v in e.discretize(Number=3)] for e in s.Edges]})
finally:
 for d in docs:App.closeDocument(d.Name)
assert all(sha(Path(p))==h for p,h in before.items()) and len(rows)==18
out.write_text(json.dumps({'status':'NATIVE_SAVED_SOCKET_AND_SPAR_SECTION_EDGES_ONLY','input_sha256':before,'rows':rows,'limits':['Sections at150/160/174 only; no full insertion/sweep or exterior packaging release','Coordinates for equal scale diagram, not CAD screenshot'],'production_release':False},indent=2)+'\n');print('18 saved native object sections sampled; sources unchanged')
