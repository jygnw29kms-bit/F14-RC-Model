from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[1];source=r/'references/UPC_Figure3_15_source_exact.png';a=np.array(Image.open(source).convert('L'));f=json.loads((r/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text());scale=f['common_scale_mm_per_pixel'];rows=[]
def edge(x,lo,hi,upper):
 ys=np.where(a[lo:hi,x]<128)[0]+lo
 if not len(ys):raise ValueError('Missing contour')
 runs=np.split(ys,np.where(np.diff(ys)>1)[0]+1);v=runs[0] if upper else runs[-1];return float((v[0]+v[-1])/2)
for x in range(1225,1526,25):
 top=None if x in (1350,1375) else edge(x,2705,2780,True);bottom=edge(x,2850,2910,False)
 plan=[edge(x,950,1250,True),edge(x,1340,1650,False)] if x<=1300 else None
 rows.append(dict(source_x_pixel=x,X_candidate_mm=f['x_mapping']['E_model_mm']+(x-f['x_mapping']['E_source_px'])*scale,side_top_stroke_center=top,side_bottom_stroke_center=bottom,top_Z_candidate_mm=(f['z_mapping']['E_axis_source_y_px']-top)*scale if top is not None else None,bottom_Z_candidate_mm=(f['z_mapping']['E_axis_source_y_px']-bottom)*scale,plan_stroke_centers=plan,width_candidate_mm=(plan[1]-plan[0])*scale if plan is not None else None,plan_status='Fixed glove overall projection only' if plan else 'Omitted: swept-wing/wingbox overlap prevents automatic fuselage envelope identification',side_status='Overall side projection; wing/glove features may obscure body. Dorsal appendage overlap omitted at 1350/1375.'))
report=dict(status='ORIGINAL_CD_PROJECTION_CONSTRAINTS_PARTIAL',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),samples=rows,method='Visually reviewed original bands; contiguous dark stroke centers threshold128. Occluded/ambiguous plan contours remain null.',metric_registration_verified=False,fuselage_core_envelope_verified=False,production_geometry=False)
(p/'CD_projection_samples.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('Samples',len(rows),'plan present',sum(v['plan_stroke_centers'] is not None for v in rows))
