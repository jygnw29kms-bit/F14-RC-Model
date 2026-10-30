from pathlib import Path
import FreeCAD as App,json,hashlib
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();socket=R/'migration/freecad/FLARED_ROOT_SOCKET_UNFROZEN_CONCEPT_ONLY.FCStd';spar=R/'migration/freecad/FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd';basis=R/'analysis/v192_cap_width_inner_envelope.json';inputs={str(p):sha(p) for p in (socket,spar,basis)};out=R/'analysis/v192_socket_insertion_sample_screen.json';assert not out.exists();a=App.openDocument(str(socket));b=App.openDocument(str(spar));rows=[]
try:
 s=next(o.Shape for o in a.Objects if hasattr(o,'Shape') and not o.Shape.isNull());cap=b.getObject('CONTINUOUS_LOWER_CAP_REFERENCE').Shape;f=next(f for f in cap.Faces if abs(f.BoundBox.YMin-149)<1e-7 and f.BoundBox.YLength<1e-7);x0=(f.BoundBox.XMin+f.BoundBox.XMax)/2;x185=json.loads(basis.read_text())['rows'][0]['x_center_mm'];slope=(x185-x0)/36
 for dy in (26,20,15,10,5,1,0):
  trans=App.Vector(slope*dy,dy,0)
  for o in b.Objects:
   if not hasattr(o,'Shape') or o.Shape.isNull():continue
   t=o.Shape.copy();t.translate(trans);overlap=s.common(t).Volume;gap=s.distToShape(t)[0]
   rows.append({'outboard_translation_y_mm':dy,'translation_xyz_mm':list(trans),'object':o.Name,'overlap_volume_mm3':overlap,'distance_mm':gap})
finally:App.closeDocument(b.Name);App.closeDocument(a.Name)
assert all(sha(Path(p))==h for p,h in inputs.items()) and len(rows)==35
r={'status':'SEVEN_SAMPLED_STRAIGHT_INSERTION_POSES_ONLY','input_sha256':inputs,'rows':rows,'all_sampled_overlap_volumes_below_1e_6_mm3':all(r['overlap_volume_mm3']<1e-6 for r in rows),'limits':['Seven discrete translations of full five-body spar along inboard straight centerline direction, not continuous swept-volume proof','Socket only: surrounding wing, body, bearings, wires and access not included','No tolerance worst case, assembly force, adhesive process, physical insertion or retention proof','Exterior body/glove packaging remains rejected; pivotZ0/bore/axis/hardware unfrozen','No file geometry modified'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');print('35 object/pose comparisons; max overlap mm3',max(r['overlap_volume_mm3'] for r in rows))
