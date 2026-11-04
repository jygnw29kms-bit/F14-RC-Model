"""Native CAD helpers for separate unapproved normalized-profile studies."""
import FreeCAD as A,Part,collections,json,hashlib,math
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopoDS import topods
from OCC.Core.Geom import Geom_TrimmedCurve
from OCC.Core.GeomConvert import GeomConvert_ApproxCurve
from OCC.Core.GeomAbs import GeomAbs_C1
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain,BRepGProp_Vinert
from OCC.Core.gp import gp_Pnt

def profile_digest(wire):
 data=[]
 for e in wire.OrderedEdges:
  c=e.Curve;data.append([c.Degree,c.getKnots(),c.getMultiplicities(),c.getWeights(),[[v.x,v.y,v.z] for v in c.getPoles()],e.Orientation])
 return hashlib.sha256(json.dumps(data,separators=(',',':')).encode()).hexdigest()

def normalize_wire(wire,y):
 edges=wire.OrderedEdges;curves=[];errors=[]
 for e in edges:
  handle,lo,hi=BRep_Tool.Curve(topods.Edge(Part.__toPythonOCC__(e)));ap=GeomConvert_ApproxCurve(Geom_TrimmedCurve(handle,lo,hi),1e-9,GeomAbs_C1,100,12);assert ap.IsDone() and ap.MaxError()<=1e-9;errors.append(ap.MaxError());converted=Part.__fromPythonOCC__(BRepBuilderAPI_MakeEdge(ap.Curve()).Edge());c=converted.Edges[0].Curve.copy();c.segment(c.FirstParameter,c.LastParameter)
  if e.Orientation=='Reversed':c.reverse()
  poles=c.getPoles();assert c.value(c.FirstParameter).distanceToPoint(poles[0])<1e-10 and c.value(c.LastParameter).distanceToPoint(poles[-1])<1e-10;curves.append(c)
 starts=[c.value(c.FirstParameter) for c in curves];ends=[c.value(c.LastParameter) for c in curves];targets=[]
 for i in range(len(curves)):
  v=(ends[i-1]+starts[i])*.5;v.y=y;targets.append(v)
 moves=[];newedges=[]
 for i,c in enumerate(curves):
  poles=c.getPoles();weights=c.getWeights();assert all(w>0 for w in weights);a=targets[i];b=targets[(i+1)%len(curves)];moves.extend([poles[0].distanceToPoint(a),poles[-1].distanceToPoint(b)]);c.setPole(1,a,weights[0]);c.setPole(len(poles),b,weights[-1]);assert c.getWeights()==weights;newedges.append(c.toShape())
 assert max(moves)<1e-5,'unexpected profile edit above study guard'
 result=Part.Wire(newedges);assert result.isClosed() and result.isValid();gap=max(curves[i].value(curves[i].LastParameter).distanceToPoint(curves[(i+1)%len(curves)].value(curves[(i+1)%len(curves)].FirstParameter)) for i in range(len(curves)));assert gap<1e-12
 return result,{'y_mm':y,'edge_count':len(edges),'source_curve_types':dict(collections.Counter(type(e.Curve).__name__ for e in edges)),'max_reported_approximation_error_mm':max(errors),'max_endpoint_pole_shift_mm':max(moves),'max_pre_snap_curve_endpoint_gap_mm':max(ends[i-1].distanceToPoint(starts[i]) for i in range(len(curves))),'post_snap_curve_endpoint_gap_mm':gap,'normalized_profile_data_sha256':profile_digest(result)}

def flux(s,point):
 terms=[]
 for face in s.Faces:
  f=topods.Face(Part.__toPythonOCC__(face));v=BRepGProp_Vinert(BRepGProp_Face(f,True),BRepGProp_Domain(f),gp_Pnt(*point),1e-11);terms.append(v.Mass())
 return math.fsum(terms)
