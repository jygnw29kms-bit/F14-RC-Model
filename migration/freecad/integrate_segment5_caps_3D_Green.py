from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt,gp_Vec
R=Path(__file__).resolve().parents[2];qp=R/'analysis/gauss_legendre_16_32_64_nodes_weights.json';Q=json.loads(qp.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();p=R/'migration/freecad/WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd';h=H(p);out=R/'analysis/v192_segment5_caps_3D_Green_curve_integral.json';assert not out.exists()
def integrate(wire,n,xref):
 terms=[];endpoints=[];yvals=[]
 nodes,weights=Q[str(n)]
 for e in wire.OrderedEdges:
  c=BRepAdaptor_Curve(topods.Edge(Part.__toPythonOCC__(e)));lo=c.FirstParameter();hi=c.LastParameter();sign=-1 if e.Orientation=='Reversed' else 1;cuts=[lo,hi]
  if hasattr(e.Curve,'getKnots'):cuts+= [k for k in e.Curve.getKnots() if lo<k<hi]
  cuts=sorted(set(cuts));P=gp_Pnt();V=gp_Vec()
  for a,b in zip(cuts,cuts[1:]):
   scale=(b-a)/2;mid=(a+b)/2
   for node,weight in zip(nodes,weights):
    c.D1(mid+scale*node,P,V);terms.append(sign*scale*weight*((P.X()-xref)*V.Z()-P.Z()*V.X())/2)
  first=c.Value(lo if sign==1 else hi);last=c.Value(hi if sign==1 else lo);endpoints.append((first,last));yvals.extend([first.Y(),last.Y()])
 gaps=[];connect=[]
 for i,(start,end) in enumerate(endpoints):
  nxt=endpoints[(i+1)%len(endpoints)][0];gaps.append(end.Distance(nxt));connect.append(((end.X()-xref)*nxt.Z()-(nxt.X()-xref)*end.Z())/2)
 raw=math.fsum(terms);correction=math.fsum(connect)
 return {'gauss_order':n,'x_reference_mm':xref,'raw_signed_area_mm2':raw,'raw_absolute_area_mm2':abs(raw),'hypothetical_line_connector_signed_area_mm2':correction,'area_with_hypothetical_line_connectors_mm2':abs(raw+correction),'max_ordered_curve_endpoint_gap_mm':max(gaps),'sum_ordered_curve_endpoint_gaps_mm':math.fsum(gaps),'endpoint_y_range_mm':[min(yvals),max(yvals)]}
calwire=Part.makePolygon([A.Vector(0,0,0),A.Vector(2,0,0),A.Vector(2,0,3),A.Vector(0,0,3),A.Vector(0,0,0)]);cal=[integrate(calwire,64,x) for x in [0,700]];assert all(abs(r['raw_absolute_area_mm2']-6)<1e-10 for r in cal)
D=A.openDocument(str(p));s=D.getObject('VOID_TOOL_5').Shape.copy();A.closeDocument(D.Name);rows=[]
for y in [230,240]:
 caps=[f for f in s.Faces if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass.y-y)<1e-6 and f.BoundBox.YLength<1e-6];assert len(caps)==1;wire=caps[0].OuterWire;samples=[integrate(wire,n,x) for n in [16,32,64] for x in [0,700]];rows.append({'y_mm':y,'wire_edge_count':len(wire.Edges),'samples':samples});print(y,samples[-2:],flush=True)
assert H(p)==h
out.write_text(json.dumps({'status':'CALIBRATED_3D_CURVE_GREEN_INTEGRAL_CAP_DIAGNOSTIC','input_sha256_unchanged':h,'quadrature_table_sha256':H(qp),'formula':'one half integral ((x-xref) dz-z dx), orientation from ordered edges; intervals split at available 3D BSpline knots','calibration_rectangle_2_by3_mm':cal,'rows':rows,'limits':['Finite Gauss quadrature convergence checked at three orders, no rigorous error bound','Hypothetical line connectors are bookkeeping only and are not added to CAD','3D curve and pcurve area definitions can differ within native tolerances','No source geometry/tolerance changes, exact volume certificate or print/flight release'],'print_release':False,'flight_release':False},indent=2)+'\n')
