from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;d=json.loads((P/'v192_y300_seam_study_section_samples.json').read_text());im=Image.new('RGB',(1400,650),'white');dr=ImageDraw.Draw(im);dr.text((20,15),'Native section edge charts Y295 / Y305; X/Z equal8 px/mm. NOT CAD screenshot.',fill='black');dr.text((20,40),'Gray skin, blue spar, green carriers, red sleeve, orange geometric bond. No print / strength release.',fill='black')
for row,cy in zip(d['rows'],(200,480)):
 dr.text((20,cy-110),'Y='+str(row['y_mm'])+' mm',fill='black')
 for o in sorted(row['objects'],key=lambda o:0 if 'HOLLOW' in o['object'] else 1):
  n=o['object'];c='#555555' if 'HOLLOW' in n else '#cc6500' if 'GEOMETRIC_BOND_' in n else '#d03030' if 'SLEEVE' in n else '#27823b' if 'CARRIER' in n else '#245bb0'
  for e in o['edges']:
   pts=[(30+(x-610)*8,cy-z*8) for x,z in e];assert all(0<=x<1400 and 0<=y<650 for x,y in pts);dr.line(pts,fill=c,width=2)
dr.text((20,615),'Carrier-to-skin interface still zero adhesive thickness; partition volume acceptance remains blocked.',fill='black');p=P/'v192_y300_seam_study_section_review.png';assert not p.exists();im.save(p)
