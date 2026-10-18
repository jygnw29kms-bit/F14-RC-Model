"""Original-pixel nose evidence; threshold width is not an aircraft station identifier."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[3]
src=R/'references/UPC_Figure3_15_source_exact.png'
a=np.array(Image.open(src).convert('L'))
f=json.loads((R/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text())
s=f['common_scale_mm_per_pixel']; zero=f['x_mapping']['E_source_px']-f['x_mapping']['E_model_mm']/s
rows=[]
for name,(lo,hi) in {'plan':(1270,1320),'side':(2800,2865)}.items():
 samples=[]
 for x in range(410,471):
  ys=np.where(a[lo:hi,x]<128)[0]+lo
  samples.append(dict(x_px=x,outer_dark_y_px=[int(ys.min()),int(ys.max())] if len(ys) else None))
 rows.append(dict(view=name,roi_y=[lo,hi],samples=samples))
report=dict(status='UPC_IMPLIED_ZERO_LIES_IN_NOSE_PROBE_REGION_NOT_VERIFIED_RADOME_NOSE',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),implied_x_zero_px=zero,scale_mm_per_pixel_candidate=s,rows=rows,visual_observation='Both original views show a short narrow forward probe and a shoulder before the widening radome. The implied X=0 at432.35px lies on that narrow probe/shoulder region, not at an unambiguous radome tip.',radome_flare_transition_band_visually_estimated_px=[443,450],possible_origin_bias_mm_candidate=[(443-zero)*s,(450-zero)*s],limits=['Transition band is a visual selection, not a verified FS93 landmark.','Pixel width includes line thickness; no subpixel aircraft accuracy is asserted.','Navy nose definition and UPC probe/radome correspondence require an independent station or dimension.','Do not snap origin to first dark pixel or automatically subtract93 from the assembled model.'],metric_registration_verified=False,geometry_changed=False,production_release=False)
Path(__file__).with_name('UPC_nose_origin_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['implied_x_zero_px','possible_origin_bias_mm_candidate']}))
