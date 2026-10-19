"""Obere aeussere Einlaufseiten; Rumpfanschluss nicht als Innenwand deuten."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));cases=[]
for t in [96,128,160]:
 segments=[]
 for lo,hi,side in [(890,925,'min'),(1210,1245,'max')]:
  seg=[]
  for y in range(616,650):
   xs=np.where(a[y,lo:hi]<t)[0]+lo
   assert len(xs)>1 and xs.min()>lo and xs.max()<hi-1
   seg.append([int(xs.min() if side=='min' else xs.max()),y])
  segments.append(seg)
 cases.append(dict(threshold=t,segments_pixel=segments))
j=dict(status='C_OBERE_AEUSSERE_EINLAUFSEITEN_RASTER',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),cases=cases,method='Zeilen616..649: linke aeussere Minimalkante ROI890..924, rechte aeussere Maximalkante ROI1210..1244. Achsenband nicht enthalten.',limits=['Nur zwei aeussere Seiten; zentrale Rumpffuellung ist hier keine getrennte innere Aussenkontur.','Strichaussenkante, keine Strichmitte oder metrisch verifizierte Haut.','Keine geschlossene Sektion und keine Verbindung ueber Achsenluecken.'],production_release=False)
(O/'C_inlet_outer_upper_sides.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
crop=im.crop((805,530,1330,700)).resize((1050,340));dr=ImageDraw.Draw(crop)
for seg in cases[1]['segments_pixel']:dr.line([((x-805)*2,(y-530)*2) for x,y in seg],fill=(220,0,0),width=1)
crop.save(O/'C_inlet_outer_upper_sides_overlay.png');print('6 offene Rasterlinien mit jeweils34Punkten erfasst.')
