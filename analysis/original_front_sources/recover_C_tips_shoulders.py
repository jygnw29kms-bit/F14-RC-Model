"""Fehlende Spitzen und aeussere Schulterrundungen aus originalen Rasterzeilen."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));cases=[]
regions=[('linke_Spitze',810,835,561,571,'min'),('rechte_Spitze',1305,1328,561,571,'max'),('linke_Schulter',875,900,586,599,'min'),('rechte_Schulter',1240,1262,585,599,'max')]
for t in [96,128,160]:
 segs=[]
 for name,lo,hi,y0,y1,side in regions:
  seg=[]
  for y in range(y0,y1):
   xs=np.where(a[y,lo:hi]<t)[0]+lo
   assert len(xs)>0
   x=int(xs.min() if side=='min' else xs.max());assert lo<x<hi-1
   seg.append([x,y])
  segs.append(seg)
 cases.append(dict(threshold=t,segments_pixel=segs))
j=dict(status='C_SPITZEN_SCHULTERN_RASTER_REFERENZEN',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),regions=regions,cases=cases,method='Zeilenweise aeussere Dunkelpixel-Extrema in vier getrennten lokalen ROIs, keine Interpolation.',limits=['Strichaussenkante, keine Strichmitte oder metrisch verifizierte Originalhaut.','Nur lokale offene Referenzen; keine automatische Verknuepfung oder Schliessung.'],production_release=False)
(O/'C_tips_shoulders.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
crop=im.crop((805,520,1335,700)).resize((1590,540));dr=ImageDraw.Draw(crop)
for seg in cases[1]['segments_pixel']:dr.line([((x-805)*3,(y-520)*3) for x,y in seg],fill=(220,0,0),width=2)
crop.save(O/'C_tips_shoulders_overlay.png');print([(v['threshold'],[(s[0],s[-1]) for s in v['segments_pixel']]) for v in cases])
