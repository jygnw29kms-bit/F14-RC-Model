import FreeCAD as App,Part,json,os,hashlib,math
BASE=r'C:/Users/dezen/Desktop/F14-RC-Model'
SOURCE=os.path.join(BASE,'analysis/original_front_sources/ABCDEF_shared_frame_candidate.json')
EXPECTED='88d48b48e1b479ef391080caef5876077c7eee682dded99b1dbe3e11b7a65ee2'
raw=open(SOURCE,'rb').read()
if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise RuntimeError('Original candidate sections changed')
data=json.loads(raw);doc=App.newDocument('ORIGINAL_OUTER_SECTION_LOFT_STUDY');wires=[]
for row in data['profiles']:
 pts=row['loops_xyz_candidate_mm'][0];index=max(range(len(pts)),key=lambda i:(pts[i][1],pts[i][2]));pts=pts[index:]+pts[:index];vertices=[App.Vector(*v) for v in pts];wires.append(Part.makePolygon(vertices+[vertices[0]]))
def align_exact_polygon_edges(first,second):
 def parameters(wire):
  pts=[v.Point for v in wire.Vertexes];lengths=[(b-a).Length for a,b in zip(pts,pts[1:]+pts[:1])];total=sum(lengths);ts=[0.0]
  for value in lengths[:-1]:ts.append(ts[-1]+value/total)
  return pts,ts,lengths,total
 data=[parameters(first),parameters(second)];knots=sorted(set(t for pts,ts,lengths,total in data for t in ts));result=[]
 for pts,ts,lengths,total in data:
  output=[]
  for t in knots:
   j=max(i for i,value in enumerate(ts) if value<=t);u=(t-ts[j])*total/lengths[j];output.append(pts[j]+(pts[(j+1)%len(pts)]-pts[j])*u)
  wire=Part.makePolygon(output+[output[0]])
  if abs(Part.Face(wire).Area-Part.Face(first if len(result)==0 else second).Area)>1e-6:raise RuntimeError('Edge subdivision changed source polygon area')
  result.append(wire)
 return result
records=[]
for i in range(len(wires)-1):
 a,b=data['profiles'][i:i+2]
 try: shape=Part.makeLoft(align_exact_polygon_edges(wires[i],wires[i+1]),True,True)
 except Exception as exc:raise RuntimeError('Original polygon loft failed '+a['section']+'-'+b['section']) from exc
 if shape.isNull() or not shape.isValid() or len(shape.Solids)!=1:raise RuntimeError('Invalid original section loft study')
 name=a['section']+'_TO_'+b['section'];obj=doc.addObject('PartDesign::Feature',name);obj.Label='Original outer polygon ruled study '+name+' / NOT OML VERIFIED';obj.Shape=shape
 x=(a['station_X_candidate_mm']+b['station_X_candidate_mm'])/2;cuts=shape.slice(App.Vector(1,0,0),x)
 if len(cuts)!=1:raise RuntimeError('Expected one midpoint outer section')
 midpoint=Part.Face(cuts[0])
 if not midpoint.isValid():raise RuntimeError('Invalid midpoint section')
 records.append(dict(segment=name,valid=shape.isValid(),solid_count=len(shape.Solids),volume_mm3=shape.Volume,midpoint_X_mm=x,midpoint_area_mm2=midpoint.Area,source_outer_vertex_counts=[len(a['loops_xyz_candidate_mm'][0]),len(b['loops_xyz_candidate_mm'][0])],original_boundary_shape_preserved=True,original_edges_subdivided_for_correspondence=True))
doc.recompute();doc.saveAs(os.path.join(BASE,'migration/freecad/F14_ORIGINAL_OUTER_RULED_LOFT_STUDY.FCStd'))
report=dict(status='NATIVE_ORIGINAL_OUTER_POLYGON_RULED_SEGMENT_STUDY',source_sha256=EXPECTED,records=records,section_frame_verified=False,intermediate_source_silhouettes_verified=False,C_inlet_holes_propagated=False,nose_and_tail_included=False,production_geometry=False,print_release=False)
with open(os.path.join(BASE,'migration/freecad/freecad_original_outer_ruled_loft_audit.json'),'w') as f:json.dump(report,f,indent=2)
print(json.dumps(records,indent=2))
