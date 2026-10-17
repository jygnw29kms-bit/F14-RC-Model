from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[1];source=r/'references/UPC_Figure3_15_source_exact.png';a=np.array(Image.open(source).convert('L'));f=json.loads((r/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text());scale=f['common_scale_mm_per_pixel'];rows=[]
def edge(x,lo,hi,upper):
 ys=np.where(a[lo:hi,x]<128)[0]+lo
 if not len(ys):raise ValueError('Missing source contour')
 runs=np.split(ys,np.where(np.diff(ys)>1)[0]+1);run=runs[0] if upper else runs[-1]
 return float((run[0]+run[-1])/2)
for x in range(925,1176,25):
 top=None if x in (1125,1150) else edge(x,2670,2740,True)
 bottom=edge(x,2840,2870,False)
 plan=[edge(x,1000,1250,True),edge(x,1340,1550,False)]
 rows.append(dict(source_x_pixel=x,X_candidate_mm=f['x_mapping']['E_model_mm']+(x-f['x_mapping']['E_source_px'])*scale,plan_stroke_centers=plan,plan_region='Forebody only' if x<965 else 'Overall envelope includes fixed wing glove; not fuselage-core width',width_candidate_mm=(plan[1]-plan[0])*scale,side_top_stroke_center=top,side_bottom_stroke_center=bottom,top_Z_candidate_mm=(f['z_mapping']['E_axis_source_y_px']-top)*scale if top is not None else None,bottom_Z_candidate_mm=(f['z_mapping']['E_axis_source_y_px']-bottom)*scale,top_status='Omitted: dorsal antenna projection overlap' if top is None else 'Sampled upper body/canopy contour'))
report=dict(status='ORIGINAL_BC_PROJECTION_CONSTRAINTS_WITH_GLOVE_SEMANTICS',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),method='Visually reviewed view bands, contiguous dark stroke centers threshold128. Antenna overlap omitted; fixed glove explicitly included in overall plan width.',samples=rows,metric_registration_verified=False,cross_section_shape_assumed=False,production_geometry=False)
(p/'BC_projection_samples.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print([(v['source_x_pixel'],v['side_top_stroke_center'],v['plan_stroke_centers']) for v in rows])
