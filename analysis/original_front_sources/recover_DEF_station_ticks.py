from pathlib import Path
import json, hashlib
from PIL import Image
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'references'/'UPC_Figure3_15_source_exact.png'
OUT=ROOT/'analysis'/'original_front_sources'/'DEF_station_ticks.json'
a=np.array(Image.open(SRC).convert('L'))
# Visuell begrenzte Label-/Tick-ROIs im unteren Seitenriss. Nur x-Position der vertikalen Stationsmarke.
rois={
 'D':(1548,2685,1575,2738),
 'E':(1650,2685,1678,2738),
 'F':(1845,2565,1885,2650),
}
rows=[]
for sec,(x0,y0,x1,y1) in rois.items():
    crop=a[y0:y1+1,x0:x1+1]
    dark=crop<128
    counts=dark.sum(axis=0)
    maxc=int(counts.max())
    # Tick/label stem columns: retain strongest near-vertical columns; contiguous groups kept explicit.
    selected=np.where(counts>=0.72*maxc)[0]+x0
    groups=[]
    for x in selected.tolist():
        if not groups or x>groups[-1][-1]+1: groups.append([x])
        else: groups[-1].append(x)
    # choose group nearest visually expected center of ROI, rather than label side strokes
    center=(x0+x1)/2
    g=min(groups,key=lambda q:abs(sum(q)/len(q)-center)) if groups else []
    rows.append({'section':sec,'roi_native_pixels':[x0,y0,x1,y1],'dark_threshold':128,'max_dark_count_per_column':maxc,'selected_strong_columns':selected.tolist(),'contiguous_groups':groups,'chosen_tick_columns':g,'tick_center_x_pixel':sum(g)/len(g) if g else None,'interpretation':'Vertikale Stationsmarke im UPC-Seitenriss; nur x-Lage, keine Waterline.'})
out={'status':'UPC_DEF_STATION_TICKS_PIXEL_SPACE_ONLY','source_image':str(SRC.relative_to(ROOT)).replace('\\','/'),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'method':'Visuell begrenzte Tick-ROIs, dunkle Spalten nach relativer Spaltenbelegung; gewählte Gruppe muss im Originalcrop visuell als vertikale Stationsmarke verifiziert werden.','stations':rows,'aircraft_X_registration_verified_by_this_file':False,'common_waterline_verified':False,'production_release':False}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
for r in rows: print(r['section'],r['chosen_tick_columns'],r['tick_center_x_pixel'],r['contiguous_groups'])
