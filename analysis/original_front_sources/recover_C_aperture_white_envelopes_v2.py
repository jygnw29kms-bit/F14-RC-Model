"""C-Öffnungen aus Weißkomponenten rekonstruieren; keine Kontur ersetzen."""
from pathlib import Path
from collections import deque
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));cases=[]
for threshold in [96,128,160]:
 loops=[]
 for label,(lo,hi),seeds in [('links',(900,1000),[(950,600),(950,640)]),('rechts',(1140,1240),[(1180,600),(1180,640)])]:
  comps=[]
  for seed in seeds:
   assert a[seed[1],seed[0]]>=threshold;q=deque([seed]);seen={seed}
   while q:
    x,y=q.popleft()
    for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
     if lo<=xx<hi and 580<=yy<690 and (xx,yy) not in seen and a[yy,xx]>=threshold:seen.add((xx,yy));q.append((xx,yy))
   assert all(lo<x<hi-1 and 580<y<689 for x,y in seen);comps.append(seen)
  assert not comps[0].intersection(comps[1]);points=comps[0]|comps[1];ys=sorted(set(y for x,y in points if not 607<=y<=611));missing=[y for y in range(ys[0],ys[-1]+1) if y not in ys];assert all(607<=y<=611 for y in missing)
  left=[[min(x for x,yy in points if yy==y),y] for y in ys];right=[[max(x for x,yy in points if yy==y),y] for y in ys];loop=left+right[::-1]
  # Some tip rows contain a single white pixel; remove consecutive duplicates, including closure.
  clean=[]
  for v in loop:
   if not clean or v!=clean[-1]:clean.append(v)
  if clean[0]==clean[-1]:clean.pop()
  area=abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(clean,clean[1:]+clean[:1])))/2
  loops.append(dict(label=label,loop_pixel=clean,white_component_pixel_counts=[len(c) for c in comps],omitted_axis_rows=missing,area_pixel2=area))
 cases.append(dict(threshold=threshold,apertures=loops))
j=dict(status='C_WEISSRAUMHUELLEN_V2_SEPARAT_REKONSTRUIERT',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),method='Zwei vierfach verbundene Weißkomponenten je Öffnung, oberhalb/unterhalb der horizontalen Achse; zeilenweise Randhülle.',cases=cases,limits=['Weißraumrand ist nicht Strichmitte oder physische Kanalfläche.','Achsenlücke wird nur durch Polygonkanten überbrückt und bleibt ungemessen.','Native Topologie, Verschachtelung und Außenwandabstand noch ungeprüft.','Historische C-Loops und alle CAD-/Masterdateien unverändert.'],metric_registration_verified=False,production_release=False)
(O/'C_aperture_white_envelopes_v2.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');crop=im.crop((895,575,1240,695)).resize((1035,360));dr=ImageDraw.Draw(crop)
for v in cases[1]['apertures']:
 pts=[((x-895)*3,(y-575)*3) for x,y in v['loop_pixel']];dr.line(pts+[pts[0]],fill=(220,0,0),width=1)
crop.save(O/'C_aperture_white_envelopes_v2_overlay.png');print([(v['threshold'],[(q['label'],len(q['loop_pixel']),q['area_pixel2'],q['omitted_axis_rows']) for q in v['apertures']]) for v in cases])
