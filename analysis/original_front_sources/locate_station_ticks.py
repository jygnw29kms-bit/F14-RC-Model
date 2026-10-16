"""Locate original A/B/C station ticks in visually selected raster ROIs."""
from pathlib import Path
from PIL import Image
import numpy as np, json, hashlib
root=Path(__file__).resolve().parents[2]
source=root/'references/UPC_Figure3_15_source_exact.png'
raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='63413c7958648165ca381ebda27ef31a4d6aabed725b84d3e2f804da5bafb5b4'
im=np.array(Image.open(source).convert('L'))
rows=[]
for label,box in [('A',(636,2725,649,2747)),('B',(899,2638,913,2662)),('C',(1191,2679,1205,2704))]:
    x0,y0,x1,y1=box
    counts=(im[y0:y1,x0:x1]<128).sum(axis=0)
    columns=np.where(counts>=.75*max(counts))[0]+x0
    assert len(columns)>0
    rows.append(dict(section=label,roi_native_pixels=box,dark_threshold=128,selected_columns=columns.tolist(),tick_center_x_pixel=float(columns.mean()),tick_center_y_pixel=None,interpretation='Station tick above bottom side view; x only. Tick height is a label location, not an aircraft waterline.'))
report=dict(source_image='references/UPC_Figure3_15_source_exact.png',source_sha256=hashlib.sha256(raw).hexdigest(),method='Visually selected tick-only ROI; columns with dark-pixel count at least 75 percent of ROI maximum; center is mean selected column. Pixel localization only, no physical uncertainty estimate.',stations=rows,station_deltas_pixels={'A_to_B':rows[1]['tick_center_x_pixel']-rows[0]['tick_center_x_pixel'],'B_to_C':rows[2]['tick_center_x_pixel']-rows[1]['tick_center_x_pixel']},aircraft_X_registration_verified=False,metric_scale_verified=False,common_waterline_verified=False,production_loft_allowed=False)
out=Path(__file__).with_name('front_station_ticks.json')
out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
