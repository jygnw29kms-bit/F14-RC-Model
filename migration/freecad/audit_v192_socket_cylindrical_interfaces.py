from pathlib import Path
import FreeCAD as A,json,hashlib,math
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/FLARED_ROOT_SOCKET_UNFROZEN_CONCEPT_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=H(p);out=R/'analysis/v192_socket_actual_cylindrical_interfaces.json';assert not out.exists();D=A.openDocument(str(p));rows=[]
try:
 s=D.Objects[0].Shape
 for i,f in enumerate(s.Faces):
  surf=f.Surface
  if type(surf).__name__=='Cylinder':
   axis=surf.Axis;rows.append({'face_index':i,'radius_mm':surf.Radius,'axis':[axis.x,axis.y,axis.z],'area_mm2':f.Area,'z_bounds_mm':[f.BoundBox.ZMin,f.BoundBox.ZMax]})
finally:A.closeDocument(D.Name)
assert H(p)==before;assert any(abs(r['radius_mm']-3)<1e-7 for r in rows)
out.write_text(json.dumps({'status':'SAVED_SOCKET_CYLINDER_GEOMETRY_AUDIT_NOT_HARDWARE_CONTACT','input_sha256_unchanged':before,'cylindrical_faces':rows,'findings':['Existing socket bore follows global Z, not the source1.5deg canted axis','A cylindrical6mm hole is not two selected bearing seats or a thrust retention assembly','Prior baseline external packaging rejection remains in force'],'limits':['Face area is geometric bore area, not effective bearing contact area','No hardware fit tolerance, contact pressure, material or load capacity accepted','Provisional pivot Z0 and incomplete glove remain unresolved'],'production_release':False},indent=2)+'\n');print(rows)
