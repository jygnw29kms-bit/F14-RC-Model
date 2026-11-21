from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];src=R/'analysis/v192_flanged_spar_section_samples.json';b=json.loads(src.read_text());im=Image.new('RGB',(1800,850),'white');d=ImageDraw.Draw(im);font=lambda n:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
d.text((45,25),'Saved flanged spar trial: native sections',fill='black',font=font(32));d.text((45,75),'Unfrozen concept. Section edges, not a CAD screenshot or structural validation.',fill='#a22',font=font(22))
scale=30
for col,y in enumerate((185,300,435)):
 cx=300+600*col;cy=450
 d.text((cx-135,145),f'Section Y = {y} mm',fill='black',font=font(25))
 d.rectangle((cx-270,205,cx+270,700),outline='#aaa')
 d.line((cx-250,cy,cx+250,cy),fill='#ddd');d.line((cx,225,cx,680),fill='#ddd')
 for r in [r for r in b['rows'] if r['y_mm']==y]:
  ox,oz=r['display_origin_xz_mm'];color='#d34b00' if 'BOND' in r['object'] else '#248140' if 'WEB' in r['object'] else '#175dc0'
  for line in r['segments_xyz_mm']:
   pts=[(cx+(v[0]-ox)*scale,cy-(v[2]-oz)*scale) for v in line]
   assert all(cx-270<=x<=cx+270 and 205<=z<=700 for x,z in pts)
   d.line(pts,fill=color,width=2)
 d.line((cx-75,740,cx+75,740),fill='black',width=3);d.text((cx-35,755),'5 mm',fill='black',font=font(20))
d.text((45,805),'Blue: caps   Green: flanged web   Orange: geometric bond layers | Equal X/Z scale: 30 px/mm; local origins.',fill='black',font=font(22))
out=R/'analysis/v192_flanged_spar_section_review.png';im.save(out)
(R/'analysis/v192_flanged_spar_section_visual_audit.json').write_text(json.dumps({'status':'RENDERED_NATIVE_SECTION_EDGE_CHART_FOR_VISUAL_REVIEW','section_data_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_cad_sha256':b['source_sha256'],'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'scale_px_per_mm':30,'section_count':3,'objects_per_section':5,'limits':['No full span visual inspection, root connection, manufacturability or structural acceptance','Bond layer outlines show geometric placeholders only'],'production_release':False},indent=2)+'\n')
print('Three equal-scale native section charts rendered')
