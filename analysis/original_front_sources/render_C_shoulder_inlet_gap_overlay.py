from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

O=Path(__file__).parent;R=O.parents[1]
src=R/'references'/'UPC_Figure3_15_source_exact.png'
im=Image.open(src).convert('RGB')
box=(850,575,1285,630);scale=4
crop=im.crop(box).resize(((box[2]-box[0])*scale,(box[3]-box[1])*scale))
d=ImageDraw.Draw(crop)
def pt(p,c,r=6):
 x=(p[0]-box[0])*scale;y=(p[1]-box[1])*scale;d.ellipse((x-r,y-r,x+r,y+r),fill=c,outline='black')
def line(a,b,c,w=3):
 d.line([((a[0]-box[0])*scale,(a[1]-box[1])*scale),((b[0]-box[0])*scale,(b[1]-box[1])*scale)],fill=c,width=w)
for a,b in [((902,603),(910,616)),((1233,603),(1225,616))]:
 line(a,b,(255,165,0),4);pt(a,(255,0,0));pt(b,(0,100,255))
# Mark the source ROIs / actual missing zone only, without inventing contour.
d.rectangle(((875-box[0])*scale,(585-box[1])*scale,(925-box[0])*scale,(620-box[1])*scale),outline=(255,0,255),width=2)
d.rectangle(((1210-box[0])*scale,(585-box[1])*scale,(1262-box[0])*scale,(620-box[1])*scale),outline=(255,0,255),width=2)
out=O/'C_shoulder_inlet_gap_overlay.png';crop.save(out);print(out)
