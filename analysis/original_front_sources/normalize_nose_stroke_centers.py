"""Normalize projection stroke definitions, preserving section-fit residuals."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[1];source=r/'references/UPC_Figure3_15_source_exact.png';a=np.array(Image.open(source).convert('L'))
old=json.loads((p/'nose_to_A_projection_samples.json').read_text());frame=json.loads((r/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text());s=frame['common_scale_mm_per_pixel'];rows=[]
def edges(x,band):
    lo,hi=band;ys=np.where(a[lo:hi,x]<128)[0]+lo
    if not len(ys):raise ValueError('No contour stroke')
    runs=np.split(ys,np.where(np.diff(ys)>1)[0]+1)
    return [float((runs[0][0]+runs[0][-1])/2),float((runs[-1][0]+runs[-1][-1])/2)]
for v in old['samples']:
    x=v['source_x_pixel'];bands=v['selected_view_bands'];sample_x=642.5 if x==642 else float(x)
    values=[edges(x,b) for b in bands]
    if x==642:values=[[(u+w)/2 for u,w in zip(value,edges(643,b))] for value,b in zip(values,bands)]
    plan,side=values
    rows.append(dict(source_x_pixel=sample_x,selected_view_bands=bands,plan_stroke_center_y_pixels=plan,side_stroke_center_y_pixels=side,width_candidate_mm=(plan[1]-plan[0])*s,height_candidate_mm=(side[1]-side[0])*s,X_candidate_mm=frame['x_mapping']['E_model_mm']+(sample_x-frame['x_mapping']['E_source_px'])*s,side_top_Z_candidate_mm=(frame['z_mapping']['E_axis_source_y_px']-side[0])*s,side_bottom_Z_candidate_mm=(frame['z_mapping']['E_axis_source_y_px']-side[1])*s))
section=json.loads((p/'front_shared_frame_candidate.json').read_text())['profiles'][0];pts=section['loops_xyz_candidate_mm'][0];last=rows[-1]
comparison=dict(axial_gap_mm=section['station_X_candidate_mm']-last['X_candidate_mm'],width_difference_mm=last['width_candidate_mm']-(max(v[1] for v in pts)-min(v[1] for v in pts)),height_difference_mm=last['height_candidate_mm']-(max(v[2] for v in pts)-min(v[2] for v in pts)))
report=dict(status='STROKE_CENTER_NORMALIZED_NOSE_TO_A_CANDIDATE',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),method='First/last contiguous dark-run midpoint in each view band. Endpoint at 642.5 linearly averages columns 642 and 643. This normalizes measurement definitions; no snapping or profile distortion.',samples=rows,A_endpoint_comparison=comparison,metric_registration_verified=False,rail_to_section_attachment_verified=False,production_loft_allowed=False)
(p/'nose_to_A_stroke_center_samples.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(comparison))
