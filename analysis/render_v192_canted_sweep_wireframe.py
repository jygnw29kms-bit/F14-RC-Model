from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[1];p=R/'analysis/v192_canted_sweep_edge_samples.json';a=json.loads(p.read_text());rows={x['object']:x['polylines_xyz_mm'] for x in a['rows']}
img=Image.new('RGB',(2400,1320),'white');d=ImageDraw.Draw(img)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23);large=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',34)
d.text((35,20),'CANTED-AXIS REFERENCE — sampled native edges, not CAD screenshot',font=large,fill='#16263a')
d.text((35,65),'Provisional pivot Z0; no glove registration, collision, structural or print release. Independent axis scales.',font=font,fill='#752b22')
allpoints=[q for lines in rows.values() for line in lines for q in line]
views=[('Top: Y horizontal / X aft vertical',1,0),('Side: X aft horizontal / Z vertical',0,2)]
for ri,(title,ix,iy) in enumerate(views):
 lo=min(p[ix] for p in allpoints);hi=max(p[ix] for p in allpoints);bottom=min(p[iy] for p in allpoints);top=max(p[iy] for p in allpoints)
 padx=(hi-lo)*.04;pady=(top-bottom)*.08;lo-=padx;hi+=padx;bottom-=pady;top+=pady
 for ci,nominal in enumerate((20,40,68)):
  x0=35+ci*790;y0=125+ri*575;box=(x0+65,y0+65,x0+735,y0+490)
  d.text((x0+20,y0),f'Nominal label {nominal} deg — {title}',font=font,fill='#16263a');d.rectangle(box,outline='#a9b3c0',width=2)
  def xy(p):return (box[0]+(p[ix]-lo)/(hi-lo)*(box[2]-box[0]),box[3]-(p[iy]-bottom)/(top-bottom)*(box[3]-box[1]))
  for side,color in [('R','#156ba5'),('L','#ce6c22')]:
   for line in rows[f'REFERENCE_WING_{side}_NOMINAL_{nominal}']:d.line([xy(p) for p in line],fill=color,width=1)
   for line in rows['PROVISIONAL_AXIS_'+side]:d.line([xy(p) for p in line],fill='#25843e',width=3)
  d.text((box[0],box[3]+12),f'horizontal {lo:.1f} .. {hi:.1f} mm',font=font,fill='#455362')
  d.text((box[0],box[3]+40),f'vertical {bottom:.1f} .. {top:.1f} mm',font=font,fill='#455362')
d.text((35,1280),'Blue: R   Orange: L   Green: provisional axis segment. Poses are references, not multiple physical wings.',font=font,fill='#16263a')
out=R/'analysis/v192_canted_sweep_wireframe_review.png';img.save(out)
r=dict(status='NATIVE_EDGE_DATA_WIREFRAME_RENDER_PREPARED_FOR_VISUAL_REVIEW',input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),limits=['Sampled wireframe, independent plot axis scales, no hidden-line removal.','No CAD screenshot, dimensional image registration or engineering release.'],production_release=False)
(R/'analysis/v192_canted_sweep_wireframe_render.json').write_text(json.dumps(r,indent=2)+'\n')

