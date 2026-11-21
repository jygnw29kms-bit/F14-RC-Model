"""Direction-only pivot-axis sensitivity; same provisional point, no CAD update."""
from pathlib import Path
import FreeCAD as App,json,hashlib,math
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(src.read_bytes()).hexdigest();out=R/'analysis/v192_pivot_cant_sensitivity.json';assert not out.exists();d=App.openDocument(str(src));rows=[]
try:
 for side,sign in (('R',1),('L',-1)):
  shape=d.getObject('WING_'+side).Shape;p=App.Vector(613.1323905812828,sign*125.20927023775282,0);vertical=App.Vector(0,0,1);canted=App.Vector(0,sign*math.sin(math.radians(1.5)),math.cos(math.radians(1.5)))
  for nominal in (20,30,40,50,54,60,68):
   angle=-sign*(nominal-20);rot0=App.Rotation(vertical,angle);rot1=App.Rotation(canted,angle);samples=[]
   for vertex in shape.Vertexes:
    point=vertex.Point;v=rot0.multVec(point-p)+p;c=rot1.multVec(point-p)+p
    samples.append(dict(source_xyz_mm=list(point),vertical_axis_xyz_mm=list(v),canted_axis_xyz_mm=list(c),displacement_mm=(c-v).Length,z_difference_mm=c.z-v.z))
   worst=max(samples,key=lambda x:x['displacement_mm']);z_worst=max(samples,key=lambda x:abs(x['z_difference_mm']))
   a=shape.copy();a.rotate(p,vertical,angle);b=shape.copy();b.rotate(p,canted,angle)
   bounds=lambda s:{axis:[getattr(s.BoundBox,axis+'Min'),getattr(s.BoundBox,axis+'Max')] for axis in ('X','Y','Z')}
   rows.append(dict(side=side,nominal_sweep_input_deg=nominal,rotation_increment_deg=angle,provisional_axis_point_xyz_mm=list(p),canted_unit_direction=list(canted),sampled_vertices=len(samples),max_vertex_displacement=worst,max_abs_vertex_z_difference=z_worst,vertical_bounds_mm=bounds(a),canted_bounds_mm=bounds(b),both_shapes_valid=a.isValid() and b.isValid(),volume_delta_mm3=b.Volume-a.Volume))
finally:App.closeDocument(d.Name)
assert before==hashlib.sha256(src.read_bytes()).hexdigest()
r=dict(status='PIVOT_AXIS_DIRECTION_ONLY_SENSITIVITY_NOT_REGISTERED_SWEEP',source_sha256=before,source_cant_reference='NASA_TM4124_second_pivot_reference_audit.json',rows=rows,limits=['Axis point fixed at existing provisional local Z0; true pivot waterline remains unknown.','Assumes cant in transverse YZ plane toward outboard; source-model/production registration not frozen.','Same rotation increments used; canted-axis resulting LE sweep is not separately calibrated.','Reported displacement maxima are over BREP vertices, not certified all-surface maxima.','No body/glove collision, mechanism, strength or manufacturing release; master unchanged.'],print_release=False,flight_release=False)
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps([dict(side=x['side'],sweep=x['nominal_sweep_input_deg'],max_vertex_displacement_mm=x['max_vertex_displacement']['displacement_mm'],max_abs_vertex_z_difference_mm=abs(x['max_abs_vertex_z_difference']['z_difference_mm'])) for x in rows if x['nominal_sweep_input_deg']==68]))
