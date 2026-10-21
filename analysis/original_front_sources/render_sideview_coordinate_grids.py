from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
pairs=[
 (ROOT/'analysis/independent_reviews/crank_localization_20261017/Navy_F14_station_diagram.jpg',(40,490,620,640),20,10,ROOT/'analysis/original_front_sources/Navy_side_coordinate_grid.png'),
 (ROOT/'references/UPC_Figure3_15_source_exact.png',(350,2550,2113,2953),100,50,ROOT/'analysis/original_front_sources/UPC_side_coordinate_grid.png'),
]
for src,box,xstep,ystep,out in pairs:
 im=Image.open(src).convert('RGB').crop(box);d=ImageDraw.Draw(im)
 for x in range(((box[0]+xstep-1)//xstep)*xstep,box[2],xstep):
  xx=x-box[0];d.line((xx,0,xx,im.height),fill=(255,0,0),width=1);d.text((xx+2,2),str(x),fill=(255,0,0))
 for y in range(((box[1]+ystep-1)//ystep)*ystep,box[3],ystep):
  yy=y-box[1];d.line((0,yy,im.width,yy),fill=(255,0,0),width=1);d.text((2,yy+1),str(y),fill=(255,0,0))
 im.save(out);print(out)
