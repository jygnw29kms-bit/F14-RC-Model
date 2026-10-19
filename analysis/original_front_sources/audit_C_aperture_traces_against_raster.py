"""C-Einlaufnachzeichnungen gegen freie Rasteröffnungen prüfen; keine neue Kontur."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';trace=O/'front_sections_pixel_candidates.json';im=np.array(Image.open(src).convert('L'));c=next(v for v in json.loads(trace.read_text())['profiles'] if v['section']=='C');rows=[]
for threshold in [96,128,160]:
 for idx,(lo,hi) in [(1,(900,1000)),(2,(1140,1240))]:
  poly=c['loops_pixel'][idx]
  for y in range(600,676,5):
   if 605<=y<=615:continue
   xx=np.where(im[y,lo:hi]>=threshold)[0]+lo;assert len(xx);runs=np.split(xx,np.where(np.diff(xx)>1)[0]+1);z=max(runs,key=len);assert len(z)>20 and z[0]>lo and z[-1]<hi-1;cs=[]
   for p,q in zip(poly,poly[1:]+poly[:1]):
    if min(p[1],q[1])<=y<max(p[1],q[1]):cs.append(p[0]+(y-p[1])/(q[1]-p[1])*(q[0]-p[0]))
   assert len(cs)==2;cs.sort();rows.append(dict(loop=idx,threshold=threshold,y_pixel=y,raster_white_interval_px=[int(z[0]),int(z[-1])],trace_intersections=cs,left_delta_px=float(cs[0]-z[0]),right_delta_px=float(cs[-1]-z[-1])))
a=dict(status='C_EINLAUF_NACHZEICHNUNGEN_GEGEN_RASTER_TEILWEISE_GEPRUEFT',inputs=[dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [src,trace]],rows=rows,max_abs_delta_pixel=max(abs(v[k]) for v in rows for k in ['left_delta_px','right_delta_px']),hinweise=['Größter zusammenhängender weißer Lauf im visuell ausgewählten Öffnungsband, nicht Strichmitte.','Achsenzeilen605..615 ausgeschlossen; nur13Innenzeilen je Öffnung und Schwellenwert.','Rasterstrichdicke und Nachzeichnungsfehler sind nicht getrennt.','Kein vollständiger Kontur-/Fertigungsnachweis.','Frühere auf groben C-Loops beruhende Flächen- und Wandabstandsrechnungen sind Kandidaten, kein Originalkontur-Nachweis.'],next='C-Öffnungen vor mechanischer oder ductseitiger Freigabe separat neu nachzeichnen und Verschachtelung/Außenwand prüfen.',quellkontur_geaendert=False,produktion_freigegeben=False)
(O/'C_aperture_trace_raster_comparison.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(len(rows),a['max_abs_delta_pixel'])
