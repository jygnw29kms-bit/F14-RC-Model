from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain
from OCC.Core.TopoDS import topods
from OCC.Core.TColStd import TColStd_HArray1OfReal
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd';h=hashlib.sha256(p.read_bytes()).hexdigest();out=R/'analysis/v192_GetTKnots_binding_probe.json';assert not out.exists();D=A.openDocument(str(p));f=topods.Face(Part.__toPythonOCC__(D.Objects[0].Shape.Faces[7]));surf=BRepGProp_Face(f,True);dom=BRepGProp_Domain(f);rows=[]
while dom.More():
 surf.Load(dom.Value());lo=surf.FirstParameter();hi=surf.LastParameter();arr=TColStd_HArray1OfReal(1,2);arr.SetValue(1,-999);arr.SetValue(2,-999)
 try:
  ret=surf.GetTKnots(lo,hi,arr);values=[arr.Value(i) for i in range(arr.Lower(),arr.Upper()+1)];rows.append({'arc':len(rows)+1,'range':[lo,hi],'return_type':type(ret).__name__,'array_values':values,'endpoints_match':abs(values[0]-lo)<1e-12 and abs(values[-1]-hi)<1e-12})
 except Exception as e:rows.append({'arc':len(rows)+1,'exception':str(e)})
 dom.Next()
A.closeDocument(D.Name);assert hashlib.sha256(p.read_bytes()).hexdigest()==h
out.write_text(json.dumps({'status':'INSTALLED_GETTKnots_OUTPUT_HANDLE_PROBED','input_sha256_unchanged':h,'source_face_one_based':8,'rows':rows,'limits':['Binding behavior probe only, not parameter census or integration proof'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)
