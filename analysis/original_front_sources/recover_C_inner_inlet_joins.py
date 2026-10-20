"""Kurze aeussere Einlaufanschluesse unter dem zentralen Rumpfboden."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));cases=[]
for t in [96,128,160]:
 segs=[]
 for lo,hi,side in [(978,1000,'max'),(1135,1156,'min')]:
  seg=[]
  for y in range(646,651):
   xs=np.where(a[y,lo:hi]<t)[0]+lo;assert len(xs)>0
   x=int(xs.max() if side=='max' else xs.min());assert lo<x<hi-1;seg.append([x,y])
  segs.append(seg)
 cases.append(dict(threshold=t,segments_pixel=segs))
j=dict(status='C_INNERE_EINLAUFANSCHLUESSE_RASTER',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),cases=cases,method='Zeilen646..650: aeussere rechte Kante des linken Einlaufs und aeussere linke Kante des rechten Einlaufs. Ab646 ist der zentrale horizontale Bodenstrich nicht mehr im ROI durchgehend.',limits=['Nur5Rasterpunkte je Anschluss; Strichaussenkante, keine Strichmitte.','Keine automatische Verbindung, keine Achsenbruecke oder metrisch verifizierte Originalhaut.'],production_release=False)
(O/'C_inner_inlet_joins.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
crop=im.crop((960,625,1170,670)).resize((1260,270));dr=ImageDraw.Draw(crop)
for s in cases[1]['segments_pixel']:dr.line([((x-960)*6,(y-625)*6) for x,y in s],fill='red',width=2)
crop.save(O/'C_inner_inlet_joins_overlay.png');print(cases)
