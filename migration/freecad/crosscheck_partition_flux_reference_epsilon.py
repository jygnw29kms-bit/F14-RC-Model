from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain,BRepGProp_VinertGK
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt
R=Path(__file__).resolve().parents[2];names=['WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd','WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_partition_flux_reference_epsilon_geometric_seams.json';assert not out.exists();sh=[]
for p in ps:
 D=A.openDocument(str(p));sh.extend((o.Name,o.Shape.copy()) for o in D.Objects);A.closeDocument(D.Name)
runs=[]
for point,eps in [((700,280,0),1e-9),((700,280,0),1e-11),((700,300,0),1e-9)]:
 rows=[];seams=[]
 for name,s in sh:
  samples=[]
  for i,face in enumerate(s.Faces,1):
   f=topods.Face(Part.__toPythonOCC__(face));v=BRepGProp_VinertGK(BRepGProp_Face(f,True),BRepGProp_Domain(f),gp_Pnt(*point),eps,False,False);mass=v.Mass();samples.append([i,mass,v.GetErrorReached()])
   if name.startswith('BLOCKED_PART_') and type(face.Surface).__name__=='Plane' and abs(face.CenterOfMass.y-300)<1e-6 and face.BoundBox.YLength<1e-6:seams.append({'object':name,'face':i,'orientation':face.Orientation,'signed_flux_mm3':mass})
  rows.append({'object':name,'face_count':len(samples),'signed_flux_sum_mm3':math.fsum(v[1] for v in samples),'face_samples_index_flux_error':samples})
 runs.append({'reference_point_mm':point,'requested_relative_epsilon':eps,'rows':rows,'part_sum_minus_source_mm3':math.fsum(r['signed_flux_sum_mm3'] for r in rows[1:])-rows[0]['signed_flux_sum_mm3'],'seam_faces':seams,'seam_signed_flux_sum_mm3':math.fsum(s['signed_flux_mm3'] for s in seams)})
 print(point,eps,[r['signed_flux_sum_mm3'] for r in rows],runs[-1]['part_sum_minus_source_mm3'],seams,flush=True);out.write_text(json.dumps({'status':'RUNNING','runs':runs},indent=2)+'\n')
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'COMMON_POINT_FLUX_REFERENCE_AND_EPSILON_CROSSCHECK_MEASURED','input_sha256_unchanged':dict(zip(names,hs)),'runs':runs,'limits':['Native integrator estimates not rigorous bounds; reference/epsilon sensitivity is diagnostic','Seam faces selected geometrically; reported face indices one-based','No geometry or tolerance change; one favorable balance is not full acceptance'],'print_release':False,'flight_release':False},separators=(',',':'))+'\n')

