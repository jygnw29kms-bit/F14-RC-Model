from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
NAVY=ROOT/'analysis/independent_reviews/crank_localization_20261017/Navy_F14_station_diagram.jpg'
UPC=ROOT/'references/UPC_Figure3_15_source_exact.png'
OUT=ROOT/'docs/images/f14_side_x_registration_20261021.png'
# Crop side views and enlarge Navy for comparable readability.
n=Image.open(NAVY).convert('RGB').crop((45,490,600,635)).resize((1665,435))
u=Image.open(UPC).convert('RGB').crop((350,2550,2113,2925))
# Both output rows width 1763; center Navy crop on white canvas.
W=1763; H=435+40+375
canvas=Image.new('RGB',(W,H),'white');canvas.paste(n,((W-n.width)//2,0));canvas.paste(u,(0,475))
d=ImageDraw.Draw(canvas)
# Source x -> displayed x.
navy_off=(W-n.width)//2; navy_scale=3.0
navy_marks=[('FS93 / Radom',127.4224),('Canopy-Bow',253.0),('Nozzle aft',569.0)]
for label,x in navy_marks:
 xx=navy_off+(x-45)*navy_scale;d.line((xx,0,xx,435),fill=(220,0,0),width=3);d.text((xx+5,8),label,fill=(180,0,0))
upc_marks=[('FS93 / Radom',441.0),('Canopy-Bow',909.5),('Nozzle aft',2087.0)]
for label,x in upc_marks:
 xx=x-350;d.line((xx,475,xx,H),fill=(220,0,0),width=3);d.text((xx+5,483),label,fill=(180,0,0))
d.text((10,445),'Navy Figure 4-7 oben | UPC Figure 3.15 unten | rote Linien = drei homologe X-Landmarken, keine OML-Freigabe',fill=(0,0,0))
OUT.parent.mkdir(parents=True,exist_ok=True);canvas.save(OUT);print(OUT)
