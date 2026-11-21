from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;d=json.loads((P/'NASA_outboard_r2_native_edge_samples.json').read_text());im=Image.new('RGB',(1400,950),'white');dr=ImageDraw.Draw(im);dr.text((25,20),'Saved native R2 outboard reference: sampled edge projections, NOT CAD screenshot',fill='black');dr.text((25,45),'Conditional source coordinates; source units only. No factory OML / physical registration / print / flight acceptance.',fill='black')
for label,origin,scale,project in [('PLAN X/Y equal scale',(40,130),2.5,lambda x,y,z:(x-490,y-120)),('SIDE Y/Z equal scale',(40,870),2.5,lambda x,y,z:(y-120,-(z-150)))]:
 dr.text((origin[0],(900 if label.startswith('SIDE') else origin[1]-30)),label,fill='black')
 for e in d['edges']:
  pts=[(origin[0]+scale*project(*v)[0],origin[1]+scale*project(*v)[1]) for v in e];assert all(0<=x<1400 and 0<=y<950 for x,y in pts);dr.line(pts,fill='#337187',width=1)
out=P/'NASA_outboard_r2_native_edge_review.png';im.save(out)

