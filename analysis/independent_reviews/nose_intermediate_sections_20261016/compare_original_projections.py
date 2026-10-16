from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[2];source=r/'references/UPC_Figure3_15_source_exact.png';a=np.array(Image.open(source).convert('L'));f=json.loads((r/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text());scale=f['common_scale_mm_per_pixel'];native=json.loads((p/'F14_nose_intermediate_section_audit.json').read_text());rows=[]
def edges(x,lo,hi):
 ys=np.where(a[lo:hi,x]<128)[0]+lo;runs=np.split(ys,np.where(np.diff(ys)>1)[0]+1)
 if not len(ys):raise ValueError('Missing contour')
 return [(runs[0][0]+runs[0][-1])/2,(runs[-1][0]+runs[-1][-1])/2]
for row in native['records']:
 x=f['x_mapping']['E_source_px']+(row['X_mm']-f['x_mapping']['E_model_mm'])/scale;left=int(np.floor(x));weight=x-left;values=[]
 for lo,hi in [(1200,1400),(2700,2870)]:
  a0,b0=edges(left,lo,hi),edges(left+1,lo,hi);v=[(1-weight)*u+weight*w for u,w in zip(a0,b0)];values.append((v[1]-v[0])*scale)
 target=sum(values)/2
 rows.append(dict(source_x_pixel=x,original_plan_width_candidate_mm=values[0],original_side_height_candidate_mm=values[1],equal_weight_source_diameter_mm=target,native_area_equivalent_diameter_mm=row['area_equivalent_diameter_mm'],diameter_residual_mm=row['area_equivalent_diameter_mm']-target))
report=dict(status='INTERMEDIATE_NATIVE_AREA_VS_ORIGINAL_PROJECTION_STUDY',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),records=rows,max_abs_diameter_residual_mm=max(abs(v['diameter_residual_mm']) for v in rows),interpretation='Compares area-equivalent native section diameter with equal-weight source projection widths/heights. No tolerance or production acceptance; does not prove circularity or actual silhouette extent.',production_geometry=False)
(p/'source_comparison.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(report['max_abs_diameter_residual_mm'])
