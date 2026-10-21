from pathlib import Path
import json,hashlib
from PIL import Image
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'analysis'/'independent_reviews'/'crank_localization_20261017'/'Navy_F14_station_diagram.jpg'
OUT=ROOT/'analysis'/'original_front_sources'/'Navy_F14_station_ruler_calibration.json'
a=np.array(Image.open(SRC).convert('L'))
x0,x1=60,600; y0,y1=630,680
c=a[y0:y1+1,x0:x1+1]<180
counts=c.sum(axis=0)
sel=np.where(counts>=9)[0]+x0
groups=[]
for x in sel.tolist():
    if not groups or x>groups[-1][-1]+1: groups.append([x])
    else: groups[-1].append(x)
centers=[sum(g)/len(g) for g in groups]
best=None
for start in range(len(centers)):
    seq=[centers[start]]; last=centers[start]
    for q in centers[start+1:]:
        if 25<=q-last<=36:
            seq.append(q); last=q
            if len(seq)==18: break
    if len(seq)>=10:
        err=np.std(np.diff(seq)) if len(seq)>1 else 999
        score=(len(seq),-float(err))
        if best is None or score>best[0]: best=(score,seq)
major=best[1] if best else []
if len(major)>=2:
    fs=np.arange(len(major),dtype=float)*50.0; x=np.array(major,float)
    A=np.vstack([fs,np.ones_like(fs)]).T
    px_per_in,fs0_x=np.linalg.lstsq(A,x,rcond=None)[0]
    res=x-(px_per_in*fs+fs0_x)
else:
    px_per_in=fs0_x=float('nan');res=np.array([])
out={'status':'NAVY_F14_FIG4_7_FS_RULER_PIXEL_CALIBRATION','source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'roi':[x0,y0,x1,y1],'dark_column_groups':groups,'group_centers_px':centers,'selected_major_tick_centers_px':major,'assigned_FS_in':[50*i for i in range(len(major))],'fit':{'px_per_FS_in':float(px_per_in),'FS_in_per_px':float(1/px_per_in) if px_per_in==px_per_in else None,'FS0_x_px':float(fs0_x),'rms_px':float(np.sqrt(np.mean(res**2))) if len(res) else None,'max_abs_px':float(np.max(np.abs(res))) if len(res) else None,'FS93_x_px':float(fs0_x+px_per_in*93) if px_per_in==px_per_in else None},'limits':['Figure4-7 is a low-resolution Navy training schematic; ruler calibration supports station correspondence, not subpixel airframe metrology.','Major tick selection must be visually checked against the raster.'],'production_release':False}
OUT.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out['fit'],indent=2));print('major',major)
