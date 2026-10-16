from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[1];source=r/'references/UPC_Figure3_15_source_exact.png';a=np.array(Image.open(source).convert('L'));f=json.loads((r/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text());scale=f['common_scale_mm_per_pixel'];rows=[]
def edge_runs(x,lo,hi):
 ys=np.where(a[lo:hi,x]<128)[0]+lo
 if not len(ys):raise ValueError('No source contour')
 runs=np.split(ys,np.where(np.diff(ys)>1)[0]+1)
 return [float((runs[0][0]+runs[0][-1])/2),float((runs[-1][0]+runs[-1][-1])/2)]
for x in range(675,876,25):
 plan=edge_runs(x,1200,1400);top=edge_runs(x,2668,2770)[0];bottom=edge_runs(x,2840,2870)[1] if x>=750 else None
 rows.append(dict(source_x_pixel=x,plan_stroke_centers=plan,side_top_stroke_center=top,side_bottom_stroke_center=bottom,lower_contour_status='Sampled body outline' if bottom is not None else 'Omitted: nose gear overlaps lower projection; do not infer an aircraft contour from it.',X_candidate_mm=f['x_mapping']['E_model_mm']+(x-f['x_mapping']['E_source_px'])*scale,width_candidate_mm=(plan[1]-plan[0])*scale,top_Z_candidate_mm=(f['z_mapping']['E_axis_source_y_px']-top)*scale,bottom_Z_candidate_mm=(f['z_mapping']['E_axis_source_y_px']-bottom)*scale if bottom is not None else None))
report=dict(status='ORIGINAL_AB_FOREBODY_PROJECTION_CONSTRAINTS_CANDIDATE',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),view_bands=dict(plan=[1200,1400],side_top=[2668,2770],side_bottom=[2840,2870]),samples=rows,method='Contiguous stroke centers at threshold128, visually reviewed source regions. Lower projection deliberately omitted in gear overlap columns.',metric_registration_verified=False,cross_section_shape_assumed=False,production_geometry=False)
(p/'AB_forebody_projection_samples.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print([(v['source_x_pixel'],v['side_top_stroke_center'],v['side_bottom_stroke_center']) for v in rows])
