from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[1];source=r/'references/UPC_Figure3_15_source_exact.png';image=np.array(Image.open(source).convert('L'));traces=json.loads((p/'front_sections_pixel_candidates.json').read_text());c=next(v for v in traces['profiles'] if v['section']=='C');frame=json.loads((p/'front_shared_frame_candidate.json').read_text());mapped=next(v for v in frame['profiles'] if v['section']=='C');aft=json.loads((r/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text());mult=mapped['isotropic_mm_per_section_pixel']/aft['common_scale_mm_per_pixel'];center=(1077.5+1515)/2;bands=[(1153,1161),(1215,1226),(1367,1377),(1431,1439)];edges=[]
for lo,hi in bands:
 ys=np.where(image[lo:hi,1197]<128)[0]+lo
 if not len(ys):raise ValueError('Missing candidate edge')
 runs=np.split(ys,np.where(np.diff(ys)>1)[0]+1);run=max(runs,key=len);edges.append(float((run[0]+run[-1])/2))
rows=[]
for index,observed in [(1,edges[:2]),(2,edges[2:])]:
 loop=c['loops_pixel'][index];bounds=[min(v[0] for v in loop),max(v[0] for v in loop)];projected=[center+(v-c['source_section_axis_pixel'][0])*mult for v in bounds]
 rows.append(dict(loop=index,projected_lateral_bounds_in_plan_pixels=projected,candidate_plan_stroke_centers=observed,bound_residual_pixels=[a-b for a,b in zip(projected,observed)]))
report=dict(status='C_INNER_LOOP_PLAN_CORRESPONDENCE_CANDIDATE',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),station_column=1197,plan_center_candidate_pixel=center,edge_bands=bands,records=rows,interpretation='Compares isotropically mapped section C inner-loop lateral bounds with selected plan-view strokes. Selected strokes are correspondence candidates, not verified aperture edges. No automatic acceptance or physical inlet fit is inferred.',component_identity_verified=False,metric_registration_verified=False,production_geometry=False)
(p/'C_inner_loop_plan_correspondence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(rows)
