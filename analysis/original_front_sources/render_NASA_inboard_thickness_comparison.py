from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).resolve().parent
base=json.loads((p/'NASA_CR172559_inboard_first_three_profiles.json').read_text())
profiles={}
for r in base['rows']:profiles[(20,r['header_raw_fields'][1])]=(base['common_chord_grid_xc'],r)
for n in ('centerline','span68p5','span99'):
 for r in json.loads((p/f'NASA_CR172559_{n}_25_35_profiles.json').read_text())['rows']:profiles[(r['nominal_sweep_deg'],r['header_raw_fields'][1])]=(r['grid_xc'],r)
fontpath='C:/Windows/Fonts/arial.ttf'
f=lambda n:ImageFont.truetype(fontpath,n)
im=Image.new('RGB',(1800,1100),'white');d=ImageDraw.Draw(im)
d.text((65,25),'NASA CR172559: inboard thickness versus source X',fill='black',font=f(30))
d.text((65,70),'Conditional chord scaling; no absolute Z, no aircraft skin registration, no CAD release',fill='#a22',font=f(22))
d.text((65,105),'Vertical axis: thickness (source units); horizontal axis: X (source units)',fill='#444',font=f(19))
colors={20:'#1255ba',25:'#d06b00',35:'#25803d'}
curves={}
for key,(g,r) in profiles.items():
 h=r['header_raw_fields'];c=h[2]-h[0]
 curves[key]=[(h[0]+x*c,(u-l)*c) for x,u,l in zip(g,r['ordinate_upper'],r['ordinate_lower'])]
for panel,span in enumerate((0,68.5,99)):
 left=90+panel*570;top=190;w=480;height=680
 xs=[v[0] for a in colors for v in curves[(a,span)]];ys=[v[1] for a in colors for v in curves[(a,span)]]
 xmin=min(xs);xmax=max(xs);ymax=max(ys)*1.08
 xy=lambda x,y:(left+(x-xmin)/(xmax-xmin)*w,top+height-y/ymax*height)
 d.text((left,135),f'Span source coordinate = {span}',fill='black',font=f(23))
 for i in range(6):
  x=xmin+(xmax-xmin)*i/5;y=ymax*i/5
  px,_=xy(x,0);_,py=xy(xmin,y)
  d.line((px,top,px,top+height),fill='#ddd');d.line((left,py,left+w,py),fill='#ddd')
  d.text((px-20,top+height+12),f'{x:.0f}',fill='black',font=f(18))
  d.text((left-55,py-10),f'{y:.1f}',fill='black',font=f(18))
 d.rectangle((left,top,left+w,top+height),outline='black',width=2)
 for a,color in colors.items():
  pts=[xy(x,y) for x,y in curves[(a,span)]]
  assert all(left-1<=x<=left+w+1 and top-1<=y<=top+height+1 for x,y in pts)
  d.line(pts,fill=color,width=4)
 d.text((left+125,top+height+50),'X (source units)',fill='black',font=f(21))
 for j,(a,color) in enumerate(colors.items()):d.text((left+j*150,965),f'{a} deg',fill=color,font=f(22))
d.text((65,1020),'Thickness = chord * (upper - lower); each curve retains its own original X grid.',fill='black',font=f(23))
d.text((65,1055),'Linear segments between 50 source samples. Different panel scales. Centerline may be computational continuation.',fill='#444',font=f(19))
out=p/'NASA_CR172559_inboard_thickness_comparison_review.png';im.save(out)
print('Rendered 9 curves in 3 panels, all within bounds:',out)
