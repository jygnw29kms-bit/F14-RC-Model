"""Vorhandene A-Nachzeichnung gegen unverändertes Raster prüfen, keine neue Kontur."""
from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';trace=O/'front_sections_pixel_candidates.json';a=np.array(Image.open(src).convert('L'));poly=next(v for v in json.loads(trace.read_text())['profiles'] if v['section']=='A')['loops_pixel'][0];rows=[]
for threshold in [96,128,160]:
 for y in range(245,336,5):
  if 270<=y<=280:continue
  xs=np.where(a[y,1840:1960]<threshold)[0]+1840;assert len(xs) and xs.min()>1840 and xs.max()<1959
  cross=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   if min(p[1],q[1])<=y<max(p[1],q[1]):cross.append(p[0]+(y-p[1])/(q[1]-p[1])*(q[0]-p[0]))
  assert len(cross)==2;cross.sort()
  rows.append(dict(threshold=threshold,y_pixel=y,raster_outer_dark_x=[int(xs.min()),int(xs.max())],trace_intersection_x=cross,left_delta_px=float(cross[0]-xs.min()),right_delta_px=float(cross[1]-xs.max())))
j=dict(status='A_NACHZEICHNUNG_WEICHT_VOM_ORIGINALRASTER_AB',inputs=[dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [src,trace]],method='16ausgewählte Innenzeilen,3Schwellenwerte; horizontale Achsenzeilen270..280 ausgeschlossen. Originalraster-Außenstrichkanten gegen Polygon-Schnittpunkte.',samples=rows,max_abs_delta_pixel=max(abs(v[k]) for v in rows for k in ['left_delta_px','right_delta_px']),befund='Vorhandene grobe A-Polygonkontur ist nicht ausreichend als rastergenau verifiziert. Native Übereinstimmung mit diesem Polygon bestätigt lediglich Übertragungstreue.',limits=['Raster-Außenstrichkante ist nicht Strichmitte; Strichdicke bleibt im Vergleich.','Diese Zeilenprüfung ersetzt keine vollständige neue Nachzeichnung.','Keine Kontur verändert und keine Fertigungstoleranz behauptet.'],next='A-Kontur erneut aus dem Originalraster rekonstruieren, Achsen und Schraffur getrennt behandeln; neue Revision unabhängig prüfen. Vorherige A-basierte Formhypothese nicht als Quellenbeweis verwenden.',production_release=False)
(O/'A_trace_raster_comparison.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(j['max_abs_delta_pixel'])
