from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
O=Path(__file__).parent;inv=json.loads((O/'NASA_all_models_reference_study_inventory.json').read_text(encoding='utf-8'));records=[]
for entry in inv['rows']:
 f=O/entry['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==entry['sha256']
 for r in json.loads(f.read_text(encoding='utf-8'))['rows']:records.append((r.get('model',entry['models'][0]),r))
im=Image.new('RGB',(2400,1400),'white');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20);big=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',37)
colors=['#1565c0','#00897b','#ef6c00','#8e24aa','#c62828','#3949ab','#558b2f','#795548']
d.text((55,35),'NASA-Quellenstudie: 35 offene Halbsektionen / 8 Modelle',font=big,fill='black')
d.text((55,90),'Unskalierte Quellenkoordinaten; keine geschlossene Haut, RC-Massstab oder Produktionsfreigabe.',font=font,fill='#b71c1c')
d.text((55,145),'Oblique Projektion der gespeicherten Studienpunkte (keine CAD-Bildschirmaufnahme)',font=small,fill='black')
for model,r in records:
 x=r['x_source']-93
 pts=[(80+3*(x+.75*y),610-3*((z-131.45)+.45*y)) for y,z in r['points_YZ_source']]
 d.line(pts,fill=colors[model-1],width=2)
for m in range(1,9):
 xx=65+(m-1)*280;d.line((xx,220,xx+35,220),fill=colors[m-1],width=5);d.text((xx+45,205),'Modell '+str(m),font=font,fill='black')
d.line((55,720,2345,720),fill='#bbbbbb',width=2)
d.text((55,750),'Ausgewaehlte Halbsektionen in gleicher Y/Z-Darstellung; Ursprung Y=0, Z=131.45',font=font,fill='black')
selected=[(1,110),(2,250),(3,390),(4,420),(6,475),(7,575),(8,725)]
for idx,(model,x) in enumerate(selected):
 r=next(r for m,r in records if m==model and r['x_source']==x);left=60+idx*330
 d.text((left,815),f'M{model} / X={x}',font=font,fill=colors[model-1]);d.line((left+15,880,left+15,1260),fill='#bbbbbb');d.line((left,1180,left+285,1180),fill='#dddddd')
 pts=[(left+15+3*y,1180-3*(z-131.45)) for y,z in r['points_YZ_source']];d.line(pts,fill=colors[model-1],width=3)
d.text((55,1320),'Station 697: beide Quellengrenzen getrennt erhalten. Offene Symmetrie-Seite nicht geschlossen oder gespiegelt.',font=small,fill='#b71c1c')
im.save(O/'NASA_all_models_reference_visual_review.png');print('35Quellenpunktreihen gerendert')
