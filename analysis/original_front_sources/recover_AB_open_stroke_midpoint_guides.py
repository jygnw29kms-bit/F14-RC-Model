from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';im=Image.open(src).convert('RGB');a=np.array(im.convert('L'));sections=[]
for sec,x0,x1,ys,axis in [('A',1840,1960,range(245,337),(270,281)),('B',1820,1980,range(499,660),(604,617))]:
 cases=[]
 for t in [96,128,160]:
  segs=[];omitted=[]
  for side in ['left','right']:
   part=[]
   for y in ys:
    reason='Achsenband' if axis[0]<=y<=axis[1] else None
    xs=np.where(a[y,x0:x1]<t)[0]+x0;groups=[g for g in np.split(xs,np.where(np.diff(xs)>1)[0]+1) if len(g)];g=groups[0] if side=='left' else groups[-1]
    if g[0]==x0 or g[-1]==x1-1 or len(g)>6:reason='Randkontakt oder langer Strichlauf'
    q=[float((g[0]+g[-1])/2),y]
    if reason:
     if len(part)>1:segs.append(part)
     part=[];omitted.append(dict(side=side,y=y,reason=reason));continue
    if part and abs(q[0]-part[-1][0])>3:
     if len(part)>1:segs.append(part)
     part=[];omitted.append(dict(side=side,y=y,reason='Sprung groesser3px; keine Verbindung'))
    part.append(q)
   if len(part)>1:segs.append(part)
  cases.append(dict(threshold=t,segments_pixel=segs,omitted=omitted))
 sections.append(dict(section=sec,cases=cases))
r=dict(status='AB_OFFENE_STRICHLAUFMItTELREFERENZEN_ERFASST',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),sections=sections,limits=['Horizontale Strichlaufmittelpunkte, keine unabhaengige normale Mittellinienmessung.','FensterA245..336/B499..659 schliessen Kappen aus; Achsen und langeLaeufe ausgelassen.','Keine Verbindung ueber Luecken oder Spruenge; keine geschlossene Sektion oder metrische Freigabe.'],production_release=False)
(O/'AB_open_stroke_midpoint_guides.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');out=Image.new('RGB',(1280,850),'white')
for k,(s,box) in enumerate(zip(sections,[(1830,230,1970,350),(1810,480,1990,680)])):
 crop=im.crop(box).resize(((box[2]-box[0])*4,(box[3]-box[1])*4));d=ImageDraw.Draw(crop)
 for seg in s['cases'][1]['segments_pixel']:d.line([((x-box[0])*4,(y-box[1])*4) for x,y in seg],fill='red',width=1)
 out.paste(crop,(0 if k==0 else 560,0))
out.save(O/'AB_open_stroke_midpoint_guides_overlay.png');print([(s['section'],[(c['threshold'],[len(v) for v in c['segments_pixel']],len(c['omitted'])) for c in s['cases']]) for s in sections])
