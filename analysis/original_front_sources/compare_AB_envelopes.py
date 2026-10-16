"""Compare separately drawn A/B sections to same-raster view envelopes."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[1]
source=r/'references/UPC_Figure3_15_source_exact.png'
a=np.array(Image.open(source).convert('L'))
profiles=json.loads((p/'front_sections_pixel_candidates.json').read_text())['profiles']
rows=[]
for label,x,bands in [('A',642,[(1238,1247),(1346,1354),(2757,2765),(2862,2870)]),('B',905,[(1225,1234),(1358,1367),(2674,2682),(2856,2863)])]:
    edges=[]
    for lo,hi in bands:
        ys=np.where(a[lo:hi,x]<128)[0]+lo
        assert len(ys)>0
        edges.append(float((ys.min()+ys.max())/2))
    profile=next(v for v in profiles if v['section']==label)
    low,high=profile['loop_summary'][0]['bounds_pixels']
    width,height=high[0]-low[0],high[1]-low[1]
    plan=edges[1]-edges[0];side=edges[3]-edges[2];scale=plan/width
    rows.append(dict(section=label,sample_x_pixel=x,visually_selected_edge_y_bands=bands,edge_centers_y_pixel=edges,plan_width_pixels=plan,side_height_pixels=side,section_width_pixels=width,section_height_pixels=height,plan_derived_isotropic_multiplier=scale,predicted_side_height_pixels=height*scale,height_residual_pixels=height*scale-side,interpretation='Manually selected outer contour bands. Side A excludes protruding nose gear. No automatic accuracy tolerance or acceptance is assigned.'))
report=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),status='SAME_SOURCE_AB_ENVELOPE_COMPARISON_CANDIDATE',comparisons=rows,metric_scale_verified=False,common_waterline_verified=False,production_loft_allowed=False,limitations='Separately drawn sections may differ in scale or station depiction. A residual must be investigated before lofting; do not distort profiles independently in width/height to force agreement. Source contour band selection and raster uncertainty remain review items.')
(p/'front_AB_envelope_comparison.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
