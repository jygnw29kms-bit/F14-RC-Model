from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'references'/'UPC_Figure3_15_source_exact.png'
OUT=ROOT/'analysis'/'original_front_sources'/'UPC_plan_coordinate_grid.png'
box=(250,650,2050,2350)
im=Image.open(SRC).convert('RGB').crop(box)
d=ImageDraw.Draw(im)
for x in range(((box[0]+99)//100)*100,box[2],100):
    xx=x-box[0]; d.line((xx,0,xx,im.height),fill=(255,0,0),width=1); d.text((xx+2,2),str(x),fill=(255,0,0))
for y in range(((box[1]+99)//100)*100,box[3],100):
    yy=y-box[1]; d.line((0,yy,im.width,yy),fill=(255,0,0),width=1); d.text((2,yy+2),str(y),fill=(255,0,0))
im.save(OUT)
print(OUT)
