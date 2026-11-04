from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);out=R/'analysis/v192_void_segment5_cap_wire_face_area_comparison.json';assert not out.exists();D=A.openDocument(str(p));s=D.getObject('VOID_TOOL_5').Shape.copy();A.closeDocument(D.Name);rows=[]
for y in [230,240]:
 caps=[f for f in s.Faces if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass.y-y)<1e-6 and f.BoundBox.YLength<1e-6];assert len(caps)==1;cap=caps[0];assert len(cap.Wires)==1;rebuilt=Part.Face(cap.OuterWire.copy());assert rebuilt.isValid();methods=[('saved_cap',cap),('rebuilt_from_same_outer_wire',rebuilt)];sliced=s.slice(A.Vector(0,1,0),y)
 if len(sliced)==1:methods.append(('native_slice_endpoint_face',Part.Face(sliced[0])))
 measures=[]
 for name,f in methods:
  vals=[]
  for eps in [1e-7,1e-9,1e-11]:
   props=GProp_GProps();err=brepgprop.SurfaceProperties(Part.__toPythonOCC__(f),props,eps,False);vals.append({'requested_relative_epsilon':eps,'area_mm2':props.Mass(),'estimated_relative_error':err})
  measures.append({'method':name,'default_area_mm2':f.Area,'surface_type':type(f.Surface).__name__,'samples':vals})
 rows.append({'y_mm':y,'endpoint_slice_wire_count':len(sliced),'same_wire_rebuilt_minus_saved_area_at1e11_mm2':measures[1]['samples'][-1]['area_mm2']-measures[0]['samples'][-1]['area_mm2'],'same_wire_rebuilt_common_saved_area_mm2':rebuilt.common(cap).Area,'measurements':measures});print(rows[-1],flush=True)
assert H(p)==h
out.write_text(json.dumps({'status':'SEGMENT5_CAP_AND_REBUILT_PLANAR_FACE_AREAS_COMPARED','input_sha256_unchanged':h,'rows':rows,'limits':['Same 3D outer wire reused, but supporting plane and pcurve representation may differ','Native area and face common operations numerical; no exact geometry or volume proof','Endpoint slices may differ from saved cap construction; wire counts retained','No saved CAD or tolerance changes; no print/flight release'],'print_release':False,'flight_release':False},indent=2)+'\n')
