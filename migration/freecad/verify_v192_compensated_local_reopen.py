"""Reopen local cavity artifact and inspect sampled planar boundary gaps only."""
from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_COMPENSATED_LOCAL_TRIAL_ONLY.FCStd';out=R/'analysis/v192_compensated_local_reopen_audit.json';assert not out.exists()
before=hashlib.sha256(p.read_bytes()).hexdigest();prior=json.loads((R/'analysis/v192_compensated_local_subtraction.json').read_text());assert before==prior['trial_sha256']
d=App.openDocument(str(p));rows=[]
try:
 objects=[o for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objects)==1
 sh=objects[0].Shape;r=dict(status='REOPENED_COMPENSATED_LOCAL_CAVITY_BOUNDARY_AUDIT',trial_sha256=before,valid=sh.isValid(),solid_count=len(sh.Solids),shell_count=len(sh.Shells),volume_mm3=sh.Volume)
 for y in (225,230,235,240,245,250,255):
  wires=sh.slice(App.Vector(0,1,0),y);row=dict(y_mm=y,wire_count=len(wires))
  if len(wires)==2:
   wires=sorted(wires,key=lambda w:Part.Face(w).Area);inner,outer=wires
   row.update(inner_area_mm2=Part.Face(inner).Area,outer_area_mm2=Part.Face(outer).Area,minimum_boundary_separation_mm=inner.distToShape(outer)[0],inner_outside_outer_area_mm2=Part.Face(inner).cut(Part.Face(outer)).Area)
  rows.append(row)
 r['rows']=rows
 assert len(sh.Shells)==2
 distance,points,info=sh.Shells[0].distToShape(sh.Shells[1]);r['minimum_between_result_boundary_shells_mm']=distance
 r['closest_point_pairs_xyz_mm']=[[list(a),list(b)] for a,b in points]
finally:App.closeDocument(d.Name)
assert before==hashlib.sha256(p.read_bytes()).hexdigest()
r['limits']=['Seven planar sections and native minimum distance between the two saved result boundary shells; no normal-thickness field.','No whole-wing shell, structural thickness selection, joints, spars or print qualification.','Shape validity and wire separation do not establish strength or flight readiness.'];r['print_release']=False;r['flight_release']=False
out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps(r))

