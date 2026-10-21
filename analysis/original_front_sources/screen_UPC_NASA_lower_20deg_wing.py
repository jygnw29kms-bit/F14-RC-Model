from pathlib import Path
import json, hashlib
from PIL import Image
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'references'/'UPC_Figure3_15_source_exact.png'
WING=ROOT/'cad'/'fusion'/'F14TomcatRC'/'NASA_F14_basic_wing_v08.json'
OUT=ROOT/'analysis'/'original_front_sources'/'UPC_NASA_lower_20deg_wing_screen.json'
a=np.array(Image.open(SRC).convert('L'))
w=json.loads(WING.read_text(encoding='utf-8'))
sections=w['sections']
# Independently measured plan-view centerline from the nose tip, and lower extended-wing tip.
center_y=1296.5
lower_tip_y=2146.0
halfspan_px=lower_tip_y-center_y
wbl_tip=float(sections[-1]['wbl_in'])
y_scale_in_per_px=wbl_tip/halfspan_px
threshold=128
x_roi=(1300,1750)
rows=[]
for sec in sections:
    wbl=float(sec['wbl_in'])
    yf=center_y+wbl/y_scale_in_per_px
    yc=int(round(yf))
    samples=[]
    for y in range(yc-2,yc+3):
        xs=np.where(a[y,x_roi[0]:x_roi[1]+1]<threshold)[0]+x_roi[0]
        if len(xs): samples.append({'y_px':y,'x_min_px':int(xs.min()),'x_max_px':int(xs.max()),'dark_count':int(len(xs))})
    rows.append({'wbl_in':wbl,'nasa_le_fs_in':float(sec['leading_edge_fs_in']),'nasa_te_fs_in':float(sec['trailing_edge_fs_in']),'predicted_y_px':yf,'sample_rows':samples})
out={'status':'UPC_LOWER_EXTENDED_WING_VS_NASA_20DEG_RASTER_SCREEN','source_image_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'wing_data_sha256':hashlib.sha256(WING.read_bytes()).hexdigest(),'plan_centerline':{'method':'nose-tip minimum-x pixels in plan-view ROI','y_px':center_y},'lower_wingtip':{'method':'maximum-y dark pixels in isolated lower-wingtip ROI x1300..1800 y1800..2180','y_px':lower_tip_y,'x_at_tip_px':[1655,1659]},'halfspan_px':halfspan_px,'nasa_tip_wbl_in':wbl_tip,'y_scale_fullscale_in_per_px':y_scale_in_per_px,'threshold':threshold,'x_roi_px':list(x_roi),'rows':rows,'limits':['Only the lower, visibly extended wing half is compared to the NASA/Grumman 20-degree wing dataset.','Upper swept wing half is excluded.','Raster x extrema are candidates until LE/TE continuity and affine FS fit are checked.','No CAD/master change.'],'production_release':False}
OUT.write_text(json.dumps(out,indent=2),encoding='utf-8')
print('center',center_y,'tip',lower_tip_y,'halfspan',halfspan_px,'scale',y_scale_in_per_px)
for r in rows: print(r['wbl_in'],round(r['predicted_y_px'],2),[(s['x_min_px'],s['x_max_px']) for s in r['sample_rows']])
