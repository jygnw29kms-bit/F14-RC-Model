from pathlib import Path
import FreeCAD as A,json,hashlib,math
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/CANTED_HOUSING_SHOULDER_CONCEPT_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=H(p);out=R/'analysis/v192_canted_housing_face_contact_audit.json';assert not out.exists();D=A.openDocument(str(p));rows=[]
try:
 housing=D.getObject('HOUSING').Shape
 for o in D.Objects:
  if o.Name=='HOUSING':continue
  contacts=[]
  for i,f in enumerate(housing.Faces):
   for j,g in enumerate(o.Shape.Faces):
    area=f.common(g).Area
    if area>1e-7:contacts.append({'housing_face':i,'ring_face':j,'surface_type':type(f.Surface).__name__,'area_mm2':area})
  planar=sum(c['area_mm2'] for c in contacts if c['surface_type']=='Plane');cyl=sum(c['area_mm2'] for c in contacts if c['surface_type']=='Cylinder');assert abs(planar-math.pi*(6.5**2-4**2))<1e-6;assert abs(cyl-2*math.pi*6.5*5)<1e-6;rows.append({'ring':o.Name,'contacts':contacts,'planar_shoulder_area_mm2':planar,'cylindrical_seat_area_mm2':cyl})
finally:A.closeDocument(D.Name)
assert H(p)==before;out.write_text(json.dumps({'status':'NATIVE_FACE_CONTACT_GEOMETRY_ONLY','input_sha256_unchanged':before,'rows':rows,'independent_annulus_and_cylinder_area_checks_passed':True,'limits':['Generic solid rings include both races as one envelope; areas are not actual race contact','Zero nominal fit does not establish pressure, clearance or preload','Current-envelope packaging rejected; no hardware, strength or thrust capacity accepted'],'flight_release':False,'print_release':False},indent=2)+'\n');print(rows)
