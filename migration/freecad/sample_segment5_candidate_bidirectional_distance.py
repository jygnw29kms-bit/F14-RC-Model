from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/VOID_SEGMENT5_SNAPPED_ENDPOINT_STUDY_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);out=R/'analysis/v192_segment5_candidate_bidirectional_sample_distance.json';assert not out.exists();D=A.openDocument(str(p));sh=[(n,D.getObject(n).Shape.copy()) for n in ['ORIGINAL_SAVED_SEG5','SNAPPED_ENDPOINT_CANDIDATE_ONLY']];A.closeDocument(D.Name);rows=[]
for (name,source),(target_name,target) in [(sh[0],sh[1]),(sh[1],sh[0])]:
 assert len(target.Shells)==1;boundary=target.Shells[0];faces=[];largest=[]
 for i,f in enumerate(source.Faces,1):
  points,triangles=f.tessellate(.02);assert points;ids=sorted(set(round(k*(len(points)-1)/8) for k in range(9))) if len(points)>9 else list(range(len(points)));samples=[]
  for j in ids:
   point=points[j];distance=boundary.distToShape(Part.Vertex(point))[0];samples.append(distance);largest.append({'face_one_based':i,'point_mm':[point.x,point.y,point.z],'distance_to_target_boundary_mm':distance})
  faces.append({'face_one_based':i,'mesh_vertex_count':len(points),'sample_count':len(ids),'max_sample_distance_mm':max(samples)})
  if i%25==0:print(name,i,flush=True)
 largest.sort(key=lambda x:x['distance_to_target_boundary_mm'],reverse=True);rows.append({'source':name,'target':target_name,'face_count':len(faces),'sample_count':sum(f['sample_count'] for f in faces),'max_sample_distance_mm':largest[0]['distance_to_target_boundary_mm'],'largest20_samples':largest[:20],'faces':faces});out.write_text(json.dumps({'status':'RUNNING','completed_directions':rows},indent=2)+'\n')
assert H(p)==h
out.write_text(json.dumps({'status':'TWO_DIRECTION_BOUNDARY_SAMPLE_DISTANCES_MEASURED_NOT_HAUSDORFF_BOUND','input_sha256_unchanged':h,'mesh_deflection_mm':.02,'max_samples_per_face':9,'rows':rows,'limits':['Deterministic finite samples from native face tessellations; not continuous deviation or Hausdorff bound','Native tessellation and distance routines introduce numerical/tolerance effects','Distances target boundary shell, not solid interior; interior points do not trivially get zero distance','Sample agreement does not qualify altered loft globally, neighboring segment interfaces, cavity or print/flight acceptance'],'print_release':False,'flight_release':False},indent=2)+'\n');print([(r['source'],r['sample_count'],r['max_sample_distance_mm']) for r in rows],flush=True)
