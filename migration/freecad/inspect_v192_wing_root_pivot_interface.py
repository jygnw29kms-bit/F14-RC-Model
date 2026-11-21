from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(p.read_bytes()).hexdigest();out=R/'analysis/v192_wing_root_pivot_interface_screen.json';assert not out.exists();d=App.openDocument(str(p));rows=[]
try:
 for side,sign in (('R',1),('L',-1)):
  wing=d.getObject('WING_'+side).Shape;pivot=App.Vector(613.1323905812828,sign*125.20927023775282,0)
  distance,points,info=wing.distToShape(Part.Vertex(pivot));refs=[]
  for name in ('PIVOT_REF_'+side,'WINGBOX_REF'):
   obj=d.getObject(name)
   if obj is not None and hasattr(obj,'Shape') and not obj.Shape.isNull():
    refs.append(dict(object=name,label=obj.Label,distance_to_wing_mm=wing.distToShape(obj.Shape)[0],role='REFERENCE_GEOMETRY_NOT_VERIFIED_LOAD_PATH'))
  rows.append(dict(side=side,pivot_xyz_mm=list(pivot),pivot_inside_wing_reference=wing.isInside(pivot,1e-7,True),pivot_point_to_wing_distance_mm=distance,closest_point_pairs_xyz_mm=[[list(a),list(b)] for a,b in points],reference_interfaces=refs))
finally:App.closeDocument(d.Name)
assert hashlib.sha256(p.read_bytes()).hexdigest()==before
r=dict(status='CURRENT_REFERENCE_WING_ROOT_PIVOT_INTERFACE_SCREEN_ONLY',source_sha256=before,rows=rows,
 limits=['Point and reference-body distances only; no actual pin/bearing/root bridge design or load capacity verified.','WINGBOX_REF/PIVOT_REF names and contact do not establish a manufactured structural connection.','No joint, spar, insert or production geometry created; master unchanged.','Current aircraft datum/OML registration and whole-aircraft qualification remain open.'],print_release=False,flight_release=False)
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
