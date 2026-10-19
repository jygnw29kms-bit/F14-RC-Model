"""C-Oberkante als zwei getrennte Raster-Prüflinien; kein geschlossener Querschnitt."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));cases=[]
for t in [96,128,160]:
 segments=[]
 for lo,hi in [(817,1066),(1071,1320)]:
  pts=[]
  for x in range(lo,hi):
   ys=np.where(a[520:605,x]<t)[0]+520;assert len(ys) and ys.min()>520;pts.append([x,int(ys.min())])
  segments.append(pts)
 cases.append(dict(threshold=t,segments_pixel=segments))
j=dict(status='C_OBERE_RASTERKANTE_GETRENNT_ERFASST',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),cases=cases,omissions=['Vertikale Achsenregion1066..1070 vollständig ausgelassen; keine Verbindung über die Lücke.','Seitliche Extrembereiche außerhalb817..1319 nicht erfasst.'],limits=['Äußerste Dunkelpixel, nicht Strichmitte.','Nur obere Kontur; keine geschlossene Außenhülle oder Originaloberfläche.','Historische Originalnachzeichnung unverändert.'],production_release=False)
(O/'C_upper_raster_guides.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');crop=im.crop((805,520,1330,605)).resize((1050,170));dr=ImageDraw.Draw(crop)
for seg in cases[1]['segments_pixel']:dr.line([((x-805)*2,(y-520)*2) for x,y in seg],fill=(220,0,0),width=1)
crop.save(O/'C_upper_raster_guides_overlay.png');print([len(v) for v in cases[1]['segments_pixel']])
