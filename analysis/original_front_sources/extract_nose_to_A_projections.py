"""Extract original nose view silhouettes; no cross-section shape assumption."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[1];source=r/'references/UPC_Figure3_15_source_exact.png';raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='63413c7958648165ca381ebda27ef31a4d6aabed725b84d3e2f804da5bafb5b4'
a=np.array(Image.open(source).convert('L'));frame=r/'analysis/propulsion_source_silhouette_constraints_v134.json';f=json.loads(frame.read_text());s=f['common_scale_mm_per_pixel'];rows=[]
for x in list(range(450,626,25))+[642]:
    ext=[]
    bands=[(1200,1400),(2753,2870)] if x==642 else [(1200,1400),(2735,2870)] if x==625 else [(1200,1400),(2700,2870)]
    for lo,hi in bands:
        ys=np.where(a[lo:hi,x]<128)[0]+lo
        if not len(ys):raise ValueError('Missing original contour')
        ext.append([int(ys.min()),int(ys.max())])
    plan,side=ext;model_x=f['x_mapping']['E_model_mm']+(x-f['x_mapping']['E_source_px'])*s
    rows.append(dict(source_x_pixel=x,selected_view_bands=bands,plan_outer_dark_y_pixels=plan,side_outer_dark_y_pixels=side,plan_center_pixel=sum(plan)/2,width_candidate_mm=(plan[1]-plan[0])*s,height_candidate_mm=(side[1]-side[0])*s,X_candidate_mm=model_x,side_top_Z_candidate_mm=(f['z_mapping']['E_axis_source_y_px']-side[0])*s,side_bottom_Z_candidate_mm=(f['z_mapping']['E_axis_source_y_px']-side[1])*s))
report=dict(status='ORIGINAL_NOSE_TO_A_PROJECTION_SAMPLES_CANDIDATE',source_sha256=hashlib.sha256(raw).hexdigest(),frame_sha256=hashlib.sha256(frame.read_bytes()).hexdigest(),method='First/last dark pixel at threshold 128 within visually reviewed nose-only view bands. Outer stroke edges rather than fitted stroke centers; no subpixel accuracy claimed.',view_bands_native_pixels=dict(plan=[1200,1400],side=[2700,2870]),samples=rows,projection_only=True,cross_section_shape_assumed=False,metric_registration_verified=False,tip_and_pitot_separation_verified=False,production_loft_allowed=False)
(p/'nose_to_A_projection_samples.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print([(v['source_x_pixel'],v['width_candidate_mm'],v['height_candidate_mm']) for v in rows])
