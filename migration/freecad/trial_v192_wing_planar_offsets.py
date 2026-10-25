"""Planar inward offset feasibility of sampled current wing sections; no shell creation."""
from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];f=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(f.read_bytes()).hexdigest();out=R/'analysis/v192_wing_planar_offset_trials.json';assert not out.exists()
d=App.openDocument(str(f));rows=[]
try:
 wing=d.getObject('WING_R').Shape
 for y in (180,220,260,300,340,380,420,440):
  row=dict(y_mm=y,trials=[])
  try:
   wires=wing.slice(App.Vector(0,1,0),y);row['section_wire_count']=len(wires);assert len(wires)==1
   face=Part.Face(wires[0]);row['outer_section_area_mm2']=face.Area
   for offset in (-0.4,0.4):
    trial=dict(signed_offset_mm=offset)
    try:
     w=wires[0].makeOffset2D(offset,0,False,False,False);trial.update(valid=w.isValid(),wires=len(w.Wires))
     assert len(w.Wires)==1 and w.Wires[0].isClosed()
     inner=Part.Face(w.Wires[0]);outside=inner.cut(face).Area
     trial.update(area_mm2=inner.Area,outside_area_mm2=outside,
      contained_smaller_section=bool(inner.isValid() and 0<inner.Area<face.Area and outside<1e-6))
    except Exception as err:trial['error']=str(err)
    row['trials'].append(trial)
  except Exception as err:row['section_error']=str(err)
  rows.append(row)
finally:App.closeDocument(d.Name)
assert before==hashlib.sha256(f.read_bytes()).hexdigest()
r=dict(status='SAMPLED_PLANAR_WING_OFFSET_FEASIBILITY_ONLY',source_sha256=before,rows=rows,
 limits=['0.4 mm is a numerical trial, not selected structural thickness.','Planar offsets do not establish three-dimensional normal wall thickness.','No loft/cavity/shell or manufacturing export created; no validity between sampled stations.','Current OML registration, joints, load paths and print qualification remain open.'],print_release=False,flight_release=False)
out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps(rows))
