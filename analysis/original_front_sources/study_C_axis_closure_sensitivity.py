"""Explizite hypothetische Achsenschliessung, keine Messung verdeckter Kontur."""
from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
O=Path(__file__).parent;R=O.parents[1];src=O/'C_open_raster_chains.json';j=json.loads(src.read_text(encoding='utf-8'));rows=[]
def area(p):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1])))/2
for c in j['cases']:
 for offset in [-1,0,1]:
  pts=[];bridges=[]
  for i,s in enumerate(c['segments_pixel']):
   pts.extend(s);a=s[-1];b=c['segments_pixel'][(i+1)%4][0];dx=b[0]-a[0];dy=b[1]-a[1];d=math.hypot(dx,dy);mid=[(a[0]+b[0])/2-offset*dy/d,(a[1]+b[1])/2+offset*dx/d]
   if offset:pts.append(mid)
   bridges.append(dict(after_chain=i,start=a,end=b,midpoint_assumed=mid if offset else None,normal_offset_pixel=offset,measured=False))
  rows.append(dict(threshold=c['threshold'],offset_pixel=offset,points_pixel=pts,bridges=bridges,area_pixel2=area(pts)))
r=dict(status='C_ACHSENSCHLIESSUNG_NUR_HYPOTHESENSTUDIE',input_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),cases=rows,method='Vier Luecken jeVariante mit Geraden oder angenommener Mitte bei+/-1px Normalversatz verbinden. Alle vier Versatzwerte gemeinsam variiert.',limits=['Saemtliche Bruecken sind Annahmen, nicht Originalmessungen.','Drei gewaehlte Varianten sind keine Unsicherheitsgrenze, keine unabhaengige4Parameteroptimierung.','Flaechen nur2DRaster; native Gueltigkeit, Selbstschnittfreiheit und Oeffnungscontainment noch nicht geprueft.','Keine geschlossene Originalsektion, metrische Registrierung oder Produktionsfreigabe.'],production_release=False)
(O/'C_axis_closure_sensitivity.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');im=Image.open(R/'references/UPC_Figure3_15_source_exact.png').convert('RGB').crop((805,520,1330,700)).resize((1575,540));dr=ImageDraw.Draw(im)
for c,col in zip([x for x in rows if x['threshold']==128],['red','blue','green']):
 for b in c['bridges']:
  pts=[b['start']]+([b['midpoint_assumed']] if b['midpoint_assumed'] else [])+[b['end']];dr.line([((x-805)*3,(y-520)*3) for x,y in pts],fill=col,width=1)
im.save(O/'C_axis_closure_sensitivity_overlay.png');print([(c['threshold'],c['offset_pixel'],c['area_pixel2']) for c in rows])
