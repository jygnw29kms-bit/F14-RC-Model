from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[1];source=r/'references/UPC_Figure3_15_source_exact.png';image=np.array(Image.open(source).convert('L'));frame=json.loads((r/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text());scale=frame['common_scale_mm_per_pixel'];native=json.loads((r/'analysis/independent_reviews/nose_intermediate_extents_20261016/F14_nose_intermediate_extent_audit.json').read_text());rows=[]
def edge(x,lo,hi,threshold):
 ys=np.where(image[lo:hi,x]<threshold)[0]+lo
 if not len(ys):raise ValueError('Missing contour')
 runs=np.split(ys,np.where(np.diff(ys)>1)[0]+1)
 return [(runs[0][0]+runs[0][-1])/2,(runs[-1][0]+runs[-1][-1])/2]
for v in native['records']:
 x=frame['x_mapping']['E_source_px']+(v['X_mm']-frame['x_mapping']['E_model_mm'])/scale;left=int(np.floor(x));w=x-left;variants=[]
 for threshold in [96,128,160]:
  dimensions=[]
  for lo,hi in [(1200,1400),(2700,2870)]:
   aa,bb=edge(left,lo,hi,threshold),edge(left+1,lo,hi,threshold);e=[(1-w)*a+w*b for a,b in zip(aa,bb)];dimensions.append((e[1]-e[0])*scale)
  variants.append(dict(threshold=threshold,width_residual_mm=v['sampled_width_mm']-dimensions[0],height_residual_mm=v['sampled_height_mm']-dimensions[1]))
 rows.append(dict(X_mm=v['X_mm'],source_x_pixel=x,variants=variants,width_residual_range_mm=[min(q['width_residual_mm'] for q in variants),max(q['width_residual_mm'] for q in variants)],height_residual_range_mm=[min(q['height_residual_mm'] for q in variants),max(q['height_residual_mm'] for q in variants)]))
report=dict(status='NOSE_SOURCE_THRESHOLD_SENSITIVITY',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),records=rows,interpretation='Deterministic threshold sensitivity only, not confidence bounds or a geometric acceptance test. Original curve tracing, registration and circle hypothesis remain unresolved.',production_geometry=False)
(p/'nose_threshold_sensitivity.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print([(v['source_x_pixel'],v['width_residual_range_mm'],v['height_residual_range_mm']) for v in rows])
