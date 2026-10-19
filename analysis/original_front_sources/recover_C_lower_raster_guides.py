"""Stückweise untere C-Rasterkante; Achsenreste und unklare Übergänge auslassen."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));cases=[]
for t in [96,128,160]:
 segments=[];current=[];omitted=[]
 for x in range(817,1320):
  reason=None
  if 1066<=x<=1070:reason='Vertikale Achse'
  ys=np.where(a[530:695,x]<t)[0]+530;ys=ys[(ys<607)|(ys>612)]
  if not len(ys):reason='Kein von Achsen getrennter Strich'
  elif ys.max() in [606,613]:reason='Unterkontur grenzt direkt an ausgelassenes Achsenband'
  if reason:
   if len(current)>1:segments.append(current)
   current=[];omitted.append(dict(x_pixel=x,reason=reason));continue
  assert ys.max()<694;current.append([x,int(ys.max())])
 if len(current)>1:segments.append(current)
 safe=[];breaks=[]
 for seg in segments:
  part=[seg[0]]
  for v in seg[1:]:
   if abs(v[1]-part[-1][1])>3:
    breaks.append([part[-1],v])
    if len(part)>1:safe.append(part)
    part=[v]
   else:part.append(v)
  if len(part)>1:safe.append(part)
 cases.append(dict(threshold=t,segments_pixel=safe,omitted=omitted,unconnected_steep_jumps=breaks))
j=dict(status='C_UNTERE_RASTERKANTE_STUECKWEISE_ERFASST',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),cases=cases,method='Unterste Dunkelpixel pro Spalte; horizontales Achsenband607..612 ausgeschlossen, benachbarte unklare Konturpunkte ebenfalls ausgelassen. Keine Verbindung zwischen Segmenten. Sprünge über3Pixel je Spalte werden separat unterbrochen, um Luftbereiche nicht zu überbrücken.',limits=['Nur Strich-Außenkante, keine Strichmitte.','Keine geschlossene Außenkontur, keine Aussage über weiße Einlauföffnungen.','Seitliche Extrembereiche und Achsenlücken unvollständig.','Metrischer Rahmen und Originaloberfläche ungeprüft.'],production_release=False)
(O/'C_lower_raster_guides.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');crop=im.crop((805,530,1330,700)).resize((1050,340));dr=ImageDraw.Draw(crop)
for seg in cases[1]['segments_pixel']:dr.line([((x-805)*2,(y-530)*2) for x,y in seg],fill=(220,0,0),width=1)
crop.save(O/'C_lower_raster_guides_overlay.png');print([(c['threshold'],[len(s) for s in c['segments_pixel']],len(c['omitted'])) for c in cases])
