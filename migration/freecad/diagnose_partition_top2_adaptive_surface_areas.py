from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
R=Path(__file__).resolve().parents[2];names=['WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd','WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_partition_top2_adaptive_surface_areas.json';assert not out.exists();priorp=R/'analysis/v192_partition_bspline_surface_area_groups.json';prior=json.loads(priorp.read_text());sh={}
for p in ps:
 D=A.openDocument(str(p));sh.update({o.Name:o.Shape.copy() for o in D.Objects});A.closeDocument(D.Name)
rows=[]
for g in prior['largest_30_groups'][:2]:
 samples=[]
 for eps in [1e-7,1e-9,1e-11]:
  by={};measures=[]
  for side in ['SOURCE','PARTS']:
   by[side]=0
   for f in g['faces'][side]:
    face=sh[f['object']].Faces[f['face']-1];props=GProp_GProps();err=brepgprop.SurfaceProperties(Part.__toPythonOCC__(face),props,eps,False);area=props.Mass();by[side]+=area;measures.append({'side':side,'object':f['object'],'face':f['face'],'area_mm2':area,'estimated_relative_error':err})
  samples.append({'requested_relative_epsilon':eps,'measurements':measures,'part_minus_source_area_mm2':by['PARTS']-by['SOURCE']})
 rows.append({'surface_data_sha256':g['surface_data_sha256'],'default_area_residual_mm2':g['part_minus_source_area_mm2'],'adaptive_samples':samples})
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'TOP_TWO_MATCHED_SURFACE_GROUPS_ADAPTIVE_AREA_MEASURED','input_sha256_unchanged':dict(zip(names,hs)),'prior_group_report_sha256':H(priorp),'rows':rows,'limits':['Two groups only, not global surface or volume acceptance','Returned relative estimates not rigorous error bounds','Matching underlying surfaces does not establish identical trimmed domains','No geometry or tolerance modification, print or flight release'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)
