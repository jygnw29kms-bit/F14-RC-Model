from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain,BRepGProp_VinertGK
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt
R=Path(__file__).resolve().parents[2];names=['WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd','WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_partition_all_faces_common_point_flux.json';assert not out.exists();rows=[]
for p in ps:
 D=A.openDocument(str(p))
 for o in D.Objects:
  faces=[]
  for i,face in enumerate(o.Shape.Faces,1):
   f=topods.Face(Part.__toPythonOCC__(face));v=BRepGProp_VinertGK(BRepGProp_Face(f,True),BRepGProp_Domain(f),gp_Pnt(700,300,0),1e-11,False,False)
   faces.append({'face':i,'surface_type':type(face.Surface).__name__,'signed_flux_mm3':v.Mass(),'reported_error_reached':v.GetErrorReached()})
   if i%250==0:print(o.Name,i,flush=True)
  rows.append({'object':o.Name,'face_count':len(faces),'signed_flux_sum_mm3':math.fsum(f['signed_flux_mm3'] for f in faces),'faces':faces})
  out.write_text(json.dumps({'status':'RUNNING','completed_objects':rows},indent=2)+'\n')
 A.closeDocument(D.Name)
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'ALL_FACES_COMMON_POINT_TRIMMED_FLUX_MEASURED','input_sha256_unchanged':dict(zip(names,hs)),'common_reference_point_mm':[700,300,0],'requested_relative_epsilon':1e-11,'rows':rows,'part_sum_minus_source_mm3':math.fsum(r['signed_flux_sum_mm3'] for r in rows[1:])-rows[0]['signed_flux_sum_mm3'],'limits':['Signed face contributions are not physical component volumes','Native returned errors are not rigorous bounds; compare with whole-shape integration and calibrated box study','No geometry or tolerance changes; no print or flight release'],'print_release':False,'flight_release':False},indent=2)+'\n');print('COMPLETE',[r['signed_flux_sum_mm3'] for r in rows],flush=True)
