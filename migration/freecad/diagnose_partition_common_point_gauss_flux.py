from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain,BRepGProp_Vinert
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt
R=Path(__file__).resolve().parents[2];out=R/'analysis/v192_partition_common_point_gauss_flux.json';assert not out.exists()
def flux(face,p,eps):
 f=topods.Face(Part.__toPythonOCC__(face));v=BRepGProp_Vinert(BRepGProp_Face(f,True),BRepGProp_Domain(f),gp_Pnt(*p),eps);return v.Mass(),v.GetEpsilon()
cal=[]
for p in [(0,0,0),(700,280,0)]:
 total=math.fsum(flux(f,p,1e-11)[0] for f in Part.makeBox(2,3,4).Faces);cal.append({'reference_point_mm':p,'sum_mm3':total});assert abs(total-24)<1e-7
names=['WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd','WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];sh=[]
for p in ps:
 D=A.openDocument(str(p));sh.extend((o.Name,o.Shape.copy()) for o in D.Objects);A.closeDocument(D.Name)
runs=[]
for point,eps in [((700,280,0),1e-9),((700,280,0),1e-11),((700,300,0),1e-11)]:
 rows=[]
 for name,s in sh:
  samples=[]
  for i,f in enumerate(s.Faces,1):
   v,e=flux(f,point,eps);samples.append([i,v,e])
  rows.append({'object':name,'face_count':len(samples),'signed_flux_sum_mm3':math.fsum(v[1] for v in samples),'face_samples_index_flux_error':samples})
 runs.append({'reference_point_mm':point,'requested_relative_epsilon':eps,'rows':rows,'part_sum_minus_source_mm3':math.fsum(r['signed_flux_sum_mm3'] for r in rows[1:])-rows[0]['signed_flux_sum_mm3']});print(point,eps,[r['signed_flux_sum_mm3'] for r in rows],runs[-1]['part_sum_minus_source_mm3'],flush=True);out.write_text(json.dumps({'status':'RUNNING','runs':runs},separators=(',',':'))+'\n')
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'COMMON_POINT_ADAPTIVE_GAUSS_FLUX_MEASURED','input_sha256_unchanged':dict(zip(names,hs)),'calibration_box':cal,'runs':runs,'limits':['Gauss and GK share native geometry and are not independent exact arithmetic certificates','Box calibration does not certify arbitrary spline integrals','Returned relative estimates are not rigorous bounds; no geometry/tolerance changes or release'],'print_release':False,'flight_release':False},separators=(',',':'))+'\n')
