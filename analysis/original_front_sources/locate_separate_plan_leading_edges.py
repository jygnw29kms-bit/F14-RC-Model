from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[1];source=r/'references/UPC_Figure3_15_source_exact.png';a=np.array(Image.open(source).convert('L'));rows=[]
for label,band,end_band in [('upper_plan_component',(1155,1210),(1140,1225)),('lower_plan_component',(1380,1435),(1370,1450))]:
 lo,hi=band;counts=(a[lo:hi,958:973]<128).sum(axis=0);columns=np.where(counts>=.95*max(counts))[0]+958;x=int(columns[0]);el,eh=end_band;ys=np.where(a[el:eh,x]<128)[0]+el;runs=np.split(ys,np.where(np.diff(ys)>1)[0]+1);run=max(runs,key=len)
 rows.append(dict(component=label,column_detection_roi=[958,lo,973,hi],supported_columns=columns.tolist(),leading_edge_x_candidate_pixel=float(columns.mean()),representative_column=x,longest_contiguous_dark_segment_y=[int(run[0]),int(run[-1])],segment_endpoint_accuracy_verified=False))
report=dict(status='ORIGINAL_SEPARATE_PLAN_COMPONENT_LEADING_EDGE_CANDIDATES',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),records=rows,interpretation='Original plan view shows separate leading projected component boundaries near X965, with gaps to the central forebody silhouette. These are local raster features; component physical identity and 3D connection are not established by this detector.',method='Visually selected vertical stroke ROIs; columns with >=95 percent of maximal dark support at threshold128; longest contiguous run at first supported column.',continuous_fuselage_outline_verified=False,production_geometry=False)
(p/'glove_inlet_leading_edge_candidates.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(rows)
