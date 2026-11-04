"""Reopen local cavity artifact and inspect sampled planar boundary gaps only."""
from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_LOCAL_CAVITY_TRIAL_ONLY.FCStd';out=R/'analysis/v192_local_cavity_reopen_section_audit.json';assert not out.exists()
before=hashlib.sha256(p.read_bytes()).hexdigest();prior=json.loads((R/'analysis/v192_two_section_subtraction.json').read_text());assert before==prior['trial_fcstd_sha256']
d=App.openDocument(str(p));rows=[]
try:
 objects=[o for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objects)==1
 sh=objects[0].Shape;r=dict(status='REOPENED_LOCAL_CAVITY_SAMPLED_SECTION_AUDIT',trial_sha256=before,valid=sh.isValid(),solid_count=len(sh.Solids),shell_count=len(sh.Shells),volume_mm3=sh.Volume)
 for y in (225,230,240,250,255):
  wires=sh.slice(App.Vector(0,1,0),y);row=dict(y_mm=y,wire_count=len(wires))
  if len(wires)==2:
   wires=sorted(wires,key=lambda w:Part.Face(w).Area);inner,outer=wires
   row.update(inner_area_mm2=Part.Face(inner).Area,outer_area_mm2=Part.Face(outer).Area,minimum_boundary_separation_mm=inner.distToShape(outer)[0],inner_outside_outer_area_mm2=Part.Face(inner).cut(Part.Face(outer)).Area)
  rows.append(row)
 r['rows']=rows
finally:App.closeDocument(d.Name)
assert before==hashlib.sha256(p.read_bytes()).hexdigest()
r['limits']=['Only five planar sections inside 40 mm span cavity; no global three-dimensional normal wall field.','No whole-wing shell, structural thickness selection, joints, spars or print qualification.','Shape validity and wire separation do not establish strength or flight readiness.'];r['print_release']=False;r['flight_release']=False
out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps(r))
