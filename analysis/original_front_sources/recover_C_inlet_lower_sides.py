"""Untere Einlaufseiten aus zeilenweisen Dunkelpixel-Extrema; offene Referenzen."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));cases=[]
for t in [96,128,160]:
 segments=[]
 for lo,hi in [(890,1005),(1135,1240)]:
  sides=[[],[]]
  for y in range(650,676):
   xs=np.where(a[y,lo:hi]<t)[0]+lo
   assert len(xs)>1 and xs.min()>lo and xs.max()<hi-1
   sides[0].append([int(xs.min()),y]);sides[1].append([int(xs.max()),y])
  segments.extend(sides)
 cases.append(dict(threshold=t,segments_pixel=segments))
j=dict(status='C_UNTERE_EINLAUFSEITEN_RASTER_REFERENZEN',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),cases=cases,method='Zeilen650..675, linke und rechte Dunkelpixel-Extrema je Einlauf-ROI. Vier getrennte offene Linien je Schwelle.',limits=['Nur untere Seitenabschnitte unterhalb der zentralen Rumpfunterkante.','Strichaussenkante, keine Strichmitte oder originale metrische Haut.','Keine automatische Verbindung mit oberen oder unteren Rasterlinien.','Keine geschlossene Sektion; historischer Rahmen ungeprueft.'],production_release=False)
(O/'C_inlet_lower_sides.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
crop=im.crop((805,530,1330,700)).resize((1050,340));dr=ImageDraw.Draw(crop)
for seg in cases[1]['segments_pixel']:dr.line([((x-805)*2,(y-530)*2) for x,y in seg],fill=(220,0,0),width=1)
crop.save(O/'C_inlet_lower_sides_overlay.png');print('12 offene Rasterlinien mit jeweils26Punkten erfasst.')
