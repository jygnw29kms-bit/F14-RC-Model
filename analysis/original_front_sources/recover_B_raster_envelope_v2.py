"""Neue B-Rasterhüllkontur; historische Nachzeichnung unverändert erhalten."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));cases=[]
for threshold in [96,128,160]:
 left=[];right=[]
 for y in range(489,670):
  if 608<=y<=609:continue
  xs=np.where(a[y,1820:1980]<threshold)[0]+1820;assert len(xs) and xs.min()>1820 and xs.max()<1979
  left.append([int(xs.min()),y]);right.append([int(xs.max()),y])
 loop=left+right[::-1];area=abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(loop,loop[1:]+loop[:1])))/2
 cases.append(dict(threshold=threshold,loop_pixel=loop,points=len(loop),area_pixel2=area,bounds=[[min(p[0] for p in loop),489],[max(p[0] for p in loop),669]]))
report=dict(status='NEUE_B_RASTER_AUSSENHUELLKONTUR_V2_KANDIDAT',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),method='Linke/rechte äußere Dunkelpixel je Originalzeile489..669; horizontale Achsenzeilen608..609 ausgelassen. Keine Glättung, Strichmittenkorrektur oder metrische Anpassung.',cases=cases,omissions=[dict(y_pixel=[608,609],reason='Horizontale Achse überlagert Umriss; Polygon verbindet607mit610, dieser3px-Abschnitt ist nicht unabhängig gemessen.')],limits=['Äußere Strichkante, nicht physische Außenhaut und nicht Strichmitte.','Obere und untere Abschlüsse auf erster/letzter klarer Konturzeile; vollständige Subpixelkontur nicht nachgewiesen.','Schraffur-/Kerbsemantik und Konturtopologie müssen unabhängig geprüft werden.','Historische A-Kontur und sämtliche CAD-Referenzen unverändert.'],metric_registration_verified=False,production_release=False)
(O/'B_raster_envelope_v2_candidates.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Diagnosebild: unverändertes Raster mit farbiger Prüflinie als separate Datei.
crop=im.crop((1820,480,1980,680)).resize((640,800));dr=ImageDraw.Draw(crop);pts=[((x-1820)*4,(y-480)*4) for x,y in cases[1]['loop_pixel']];dr.line(pts+[pts[0]],fill=(220,0,0),width=2);crop.save(O/'B_raster_envelope_v2_overlay.png');print([(c['threshold'],c['points'],c['area_pixel2']) for c in cases])
