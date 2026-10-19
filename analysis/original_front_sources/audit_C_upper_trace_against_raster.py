"""C-Oberkontur direkt am Raster prüfen; keine Gesamtaußenkontur behaupten."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';tr=O/'front_sections_pixel_candidates.json';a=np.array(Image.open(src).convert('L'));poly=next(v for v in json.loads(tr.read_text())['profiles'] if v['section']=='C')['loops_pixel'][0];rows=[]
for threshold in [96,128,160]:
 for x in range(830,1301,10):
  if 1065<=x<=1075:continue
  yy=np.where(a[520:605,x]<threshold)[0]+520;assert len(yy) and yy.min()>520;cs=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   if min(p[0],q[0])<=x<max(p[0],q[0]):cs.append(p[1]+(x-p[0])/(q[0]-p[0])*(q[1]-p[1]))
  assert len(cs)>=2;top=min(cs);rows.append(dict(threshold=threshold,x_pixel=x,raster_top_dark_edge_y=int(yy.min()),trace_top_y=top,delta_pixel=float(top-yy.min())))
j=dict(status='C_OBERE_AUSSENKONTUR_TEILWEISE_GEGEN_RASTER_GEPRUEFT',inputs=[dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [src,tr]],rows=rows,max_abs_delta_pixel=max(abs(v['delta_pixel']) for v in rows),hinweise=['Nur obere sichtbare Außenstrichkante; vertikale Achsenregion1065..1075 ausgelassen.','Kein Nachweis für Unterkontur, Einlaufwände oder Schleifenverschachtelung.','Rasterstrichkante statt Strichmitte; Strichdicke und Nachzeichnungsfehler nicht getrennt.','Keine alte Kontur oder CAD-Datei verändert.'],next='Obere C-Rasterhülle separat erfassen; Unterkontur wegen Mehrfachinseln und Achsenüberdeckung getrennt behandeln.',produktion_freigegeben=False)
(O/'C_upper_trace_raster_comparison.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(len(rows),j['max_abs_delta_pixel'])
