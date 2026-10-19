"""Neue A-Rasterhüllkontur; historische Nachzeichnung unverändert erhalten."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));cases=[]
for threshold in [96,128,160]:
 left=[];right=[]
 for y in range(238,342):
  if 275<=y<=277:continue
  xs=np.where(a[y,1840:1960]<threshold)[0]+1840;assert len(xs) and xs.min()>1840 and xs.max()<1959
  left.append([int(xs.min()),y]);right.append([int(xs.max()),y])
 loop=left+right[::-1];area=abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(loop,loop[1:]+loop[:1])))/2
 cases.append(dict(threshold=threshold,loop_pixel=loop,points=len(loop),area_pixel2=area,bounds=[[min(p[0] for p in loop),238],[max(p[0] for p in loop),341]]))
report=dict(status='NEUE_A_RASTER_AUSSENHUELLKONTUR_V2_KANDIDAT',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),method='Linke/rechte äußere Dunkelpixel je Originalzeile238..341; horizontale Achsenzeilen275..277 ausgelassen. Keine Glättung, Strichmittenkorrektur oder metrische Anpassung.',cases=cases,omissions=[dict(y_pixel=[275,276,277],reason='Horizontale Achse überlagert Umriss; Polygon verbindet274mit278, dieser4px-Abschnitt ist nicht unabhängig gemessen.')],limits=['Äußere Strichkante, nicht physische Außenhaut und nicht Strichmitte.','Obere und untere Abschlüsse auf erster/letzter klarer Konturzeile; vollständige Subpixelkontur nicht nachgewiesen.','Schraffur-/Kerbsemantik und Konturtopologie müssen unabhängig geprüft werden.','Historische A-Kontur und sämtliche CAD-Referenzen unverändert.'],metric_registration_verified=False,production_release=False)
(O/'A_raster_envelope_v2_candidates.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Diagnosebild: unverändertes Raster mit farbiger Prüflinie als separate Datei.
crop=im.crop((1840,230,1960,350)).resize((720,720));dr=ImageDraw.Draw(crop);pts=[((x-1840)*6,(y-230)*6) for x,y in cases[1]['loop_pixel']];dr.line(pts+[pts[0]],fill=(220,0,0),width=2);crop.save(O/'A_raster_envelope_v2_overlay.png');print([(c['threshold'],c['points'],c['area_pixel2']) for c in cases])
