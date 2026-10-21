from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'references'/'UPC_Figure3_15_source_exact.png'
J=ROOT/'analysis'/'original_front_sources'/'DEF_station_ticks.json'
OUT=ROOT/'analysis'/'original_front_sources'/'DEF_station_ticks_overlay.png'
j=json.loads(J.read_text(encoding='utf-8'))
box=(1450,2520,1950,2780)
im=Image.open(SRC).convert('RGB').crop(box)
d=ImageDraw.Draw(im)
for r in j['stations']:
    x=r['tick_center_x_pixel']-box[0]
    d.line((x,0,x,im.height),fill=(255,0,0),width=2)
    d.text((x+4,8),r['section'],fill=(255,0,0))
im.save(OUT)
print(OUT)
