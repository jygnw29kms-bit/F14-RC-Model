"""Sichtbare Eckfragmente vor und nach horizontaler Achsenueberdeckung."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));cases=[]
for t in [96,128,160]:
 segs=[]
 for x0,x1 in [(902,913),(1223,1234)]:
  s=[]
  for x in range(x0,x1):
   ys=np.where(a[598:607,x]<t)[0]+598;assert len(ys)>0;s.append([x,int(ys.max())])
  segs.append(s)
 for lo,hi,side in [(900,918,'min'),(1218,1238,'max')]:
  s=[]
  for y in range(613,617):
   xs=np.where(a[y,lo:hi]<t)[0]+lo;assert len(xs)>0;x=int(xs.min() if side=='min' else xs.max());assert lo<x<hi-1;s.append([x,y])
  segs.append(s)
 cases.append(dict(threshold=t,segments_pixel=segs))
j=dict(status='C_ACHSENECKEN_SICHTBARE_FRAGmente',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),cases=cases,method='Oberhalb: unterste Dunkelpixel y598..606 in Spalten902..912 und1223..1233. Unterhalb: aeussere Zeilenextrema613..616. Band607..612 bleibt vollstaendig ausgelassen.',limits=['Endpunkte bei606 sind Messfenstergrenzen; Fortsetzung Richtung Achse nicht verifiziert.','Keine Verbindung ueber ausgelassenes Achsenband; Strichaussenkante statt Strichmitte.','Keine geschlossene Kontur oder metrisch verifizierte Haut.'],production_release=False)
(O/'C_axis_corner_fragments.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
crop=im.crop((880,590,1250,630)).resize((1480,160));dr=ImageDraw.Draw(crop)
for s in cases[1]['segments_pixel']:dr.line([((x-880)*4,(y-590)*4) for x,y in s],fill='red',width=2)
crop.save(O/'C_axis_corner_fragments_overlay.png');print(cases)
