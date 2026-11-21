from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math,collections
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain,BRepGProp_Vinert
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_TrimmedCurve
from OCC.Core.GeomConvert import GeomConvert_ApproxCurve
from OCC.Core.GeomAbs import GeomAbs_C1
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);out=R/'analysis/v192_segment5_snapped_endpoint_study.json';cad=R/'migration/freecad/VOID_SEGMENT5_SNAPPED_ENDPOINT_STUDY_ONLY.FCStd';assert not out.exists() and not cad.exists();D=A.openDocument(str(p));original=D.getObject('VOID_TOOL_5').Shape.copy();A.closeDocument(D.Name);wires=[];wire_rows=[]
for y in [230,240]:
 cap=next(f for f in original.Faces if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass.y-y)<1e-6 and f.BoundBox.YLength<1e-6);edges=cap.OuterWire.OrderedEdges;types=collections.Counter(type(e.Curve).__name__ for e in edges);curves=[];approx_errors=[]
 for e in edges:
  handle,lo,hi=BRep_Tool.Curve(topods.Edge(Part.__toPythonOCC__(e)));ap=GeomConvert_ApproxCurve(Geom_TrimmedCurve(handle,lo,hi),1e-9,GeomAbs_C1,100,12);assert ap.IsDone() and ap.MaxError()<=1e-9;approx_errors.append(ap.MaxError());converted=Part.__fromPythonOCC__(BRepBuilderAPI_MakeEdge(ap.Curve()).Edge());c=converted.Edges[0].Curve.copy();c.segment(c.FirstParameter,c.LastParameter)
  if e.Orientation=='Reversed':c.reverse()
  poles=c.getPoles();assert c.value(c.FirstParameter).distanceToPoint(poles[0])<1e-10 and c.value(c.LastParameter).distanceToPoint(poles[-1])<1e-10
  curves.append(c)
 starts=[c.value(c.FirstParameter) for c in curves];ends=[c.value(c.LastParameter) for c in curves];targets=[]
 for i in range(len(curves)):
  v=(ends[i-1]+starts[i])*.5;v.y=y;targets.append(v)
 moves=[];samplemax=0;newedges=[]
 for i,c in enumerate(curves):
  before=c.copy();poles=c.getPoles();weights=c.getWeights();assert all(w>0 for w in weights);a=targets[i];b=targets[(i+1)%len(curves)];moves.extend([poles[0].distanceToPoint(a),poles[-1].distanceToPoint(b)]);c.setPole(1,a,weights[0]);c.setPole(len(poles),b,weights[-1]);assert c.getWeights()==weights
  for j in range(33):
   t=c.FirstParameter+(c.LastParameter-c.FirstParameter)*j/32;samplemax=max(samplemax,c.value(t).distanceToPoint(before.value(t)))
  newedges.append(c.toShape())
 wire=Part.Wire(newedges);assert wire.isClosed() and wire.isValid();gaps=[curves[i].value(curves[i].LastParameter).distanceToPoint(curves[(i+1)%len(curves)].value(curves[(i+1)%len(curves)].FirstParameter)) for i in range(len(curves))];wires.append(wire);wire_rows.append({'y_mm':y,'source_edge_curve_types':dict(types),'requested_curve_approximation_tolerance_mm':1e-9,'max_reported_curve_approximation_error_mm':max(approx_errors),'max_pre_snap_approximated_endpoint_gap_mm':max(ends[i-1].distanceToPoint(starts[i]) for i in range(len(curves))),'max_endpoint_pole_displacement_mm':max(moves),'sampled_max_same_parameter_curve_displacement_mm':samplemax,'post_edit_max_curve_endpoint_gap_mm':max(gaps)})
candidate=Part.makeLoft(wires,True,True);assert candidate.isValid() and len(candidate.Solids)==1;rows=[]
for name,s in [('ORIGINAL_SAVED_SEG5',original),('SNAPPED_ENDPOINT_CANDIDATE_ONLY',candidate)]:
 vals=[]
 for point in [(700,280,0),(700,300,0)]:
  terms=[]
  for face in s.Faces:
   f=topods.Face(Part.__toPythonOCC__(face));v=BRepGProp_Vinert(BRepGProp_Face(f,True),BRepGProp_Domain(f),gp_Pnt(*point),1e-11);terms.append(v.Mass())
  vals.append(math.fsum(terms))
 rows.append({'object':name,'valid':s.isValid(),'solids':len(s.Solids),'faces':len(s.Faces),'default_volume_mm3':s.Volume,'max_native_tolerance_mm':s.getTolerance(1),'P280_P300_flux_mm3':vals,'reference_change_mm3':vals[1]-vals[0]});print(rows[-1],flush=True)
D=A.newDocument('SNAPPED_SEG5_STUDY')
for name,s in [('ORIGINAL_SAVED_SEG5',original),('SNAPPED_ENDPOINT_CANDIDATE_ONLY',candidate)]:
 o=D.addObject('PartDesign::Feature',name);o.Shape=s;o.addProperty('App::PropertyBool','PrintRelease');o.PrintRelease=False
D.recompute();D.saveAs(str(cad));A.closeDocument(D.Name);D=A.openDocument(str(cad));assert len(D.Objects)==2 and all(o.Shape.isValid() and not o.PrintRelease for o in D.Objects);A.closeDocument(D.Name);assert H(p)==h
out.write_text(json.dumps({'status':'SEPARATE_APPROXIMATED_AND_SNAPPED_ENDPOINT_CANDIDATE_SAVED_REOPENED','input_sha256_unchanged':h,'output_sha256':H(cad),'wire_edits':wire_rows,'rows':rows,'limits':['Geometry intentionally edited on separate candidate only; OffsetCurve/Circle approximated to BSplines, then endpoints averaged with weights unchanged','Positive rational basis gives theoretical curve displacement at most maximum pole displacement, subject to floating computation; sampled check not global numerical proof','Loft may reparameterize or alter intermediate surfaces; whole candidate deviation and cavity containment not yet checked','No promotion, exact volume certificate, manufacturing or flight acceptance'],'print_release':False,'flight_release':False},indent=2)+'\n');print(wire_rows)


