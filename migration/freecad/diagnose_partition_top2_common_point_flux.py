from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain,BRepGProp_VinertGK
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt
R=Path(__file__).resolve().parents[2];out=R/'analysis/v192_partition_top2_common_point_flux.json';assert not out.exists()
def flux(face,p):
 f=topods.Face(Part.__toPythonOCC__(face));v=BRepGProp_VinertGK(BRepGProp_Face(f,True),BRepGProp_Domain(f),gp_Pnt(*p),1e-11,False,False);return v.Mass(),v.GetErrorReached()
box=Part.makeBox(2,3,4);cal=[]
for p in [(0,0,0),(700,300,0)]:
 value=sum(flux(f,p)[0] for f in box.Faces);cal.append({'reference_point_mm':p,'sum_signed_face_contribution_mm3':value,'analytic_volume_mm3':24})
assert all(abs(c['sum_signed_face_contribution_mm3']-24)<1e-7 for c in cal)
names=['WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd','WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];sh={}
for p in ps:
 D=A.openDocument(str(p));sh.update({o.Name:o.Shape.copy() for o in D.Objects});A.closeDocument(D.Name)
priorp=R/'analysis/v192_partition_bspline_surface_area_groups.json';prior=json.loads(priorp.read_text());rows=[]
for g in prior['largest_30_groups'][:2]:
 values={};samples=[]
 for side in ['SOURCE','PARTS']:
  values[side]=0
  for r in g['faces'][side]:
   v,e=flux(sh[r['object']].Faces[r['face']-1],(700,300,0));values[side]+=v;samples.append({'side':side,'object':r['object'],'face':r['face'],'signed_contribution_mm3':v,'reported_error_reached':e})
 rows.append({'surface_data_sha256':g['surface_data_sha256'],'samples':samples,'part_minus_source_signed_contribution_mm3':values['PARTS']-values['SOURCE']})
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'CALIBRATED_COMMON_POINT_TRIMMED_FACE_FLUX_TOP_TWO_GROUPS_MEASURED','input_sha256_unchanged':dict(zip(names,hs)),'prior_group_report_sha256':H(priorp),'calibration_box':cal,'common_reference_point_mm':[700,300,0],'rows':rows,'limits':['Top two surface groups only, not whole shape balance','Signed individual face contributions are not physical component volumes','Returned errors not rigorous bounds; two box checks do not certify arbitrary spline integrals','No geometry/tolerance changes or release'],'print_release':False,'flight_release':False},indent=2)+'\n');print(cal,rows)
