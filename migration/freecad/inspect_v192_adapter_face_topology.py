from pathlib import Path
import FreeCAD as App,json,hashlib
R=Path(__file__).resolve().parents[2]
f=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(f.read_bytes()).hexdigest()
d=App.openDocument(str(f));rows=[]
try:
 for side in ('R','L'):
  sh=d.getObject('INLET_EDF_'+side).Shape;faces=[];curves=[]
  for i,face in enumerate(sh.Faces):
   kind=type(face.Surface).__name__;curves.extend([i] if kind!='Plane' else [])
   faces.append(dict(index=i,surface=kind,area_mm2=face.Area,center=list(face.CenterOfMass),orientation=face.Orientation,
    edge_radii_mm=[float(e.Curve.Radius) for e in face.Edges if hasattr(e.Curve,'Radius')],
    edge_lengths_mm=[e.Length for e in face.Edges]))
  pairs=[]
  for n,i in enumerate(curves):
   for j in curves[n+1:]:
    a,b=sh.Faces[i],sh.Faces[j]
    pairs.append(dict(faces=[i,j],distance_mm=a.distToShape(b)[0],shared_edges=sum(1 for e in a.Edges if any(e.isSame(q) for q in b.Edges))))
  rows.append(dict(object='INLET_EDF_'+side,faces=faces,curved_face_pairs=pairs))
finally:App.closeDocument(d.Name)
assert hashlib.sha256(f.read_bytes()).hexdigest()==before
out=R/'analysis/v192_adapter_face_topology_inspection.json';assert not out.exists()
out.write_text(json.dumps(dict(status='READ_ONLY_FACE_TOPOLOGY_INSPECTION_NOT_WALL_QUALIFICATION',source_sha256=before,rows=rows,print_release=False,flight_release=False),indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows))
