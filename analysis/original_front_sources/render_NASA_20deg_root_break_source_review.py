from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;a=json.loads((P/'NASA_CR172559_inboard_first_three_profiles.json').read_text());b=json.loads((P/'NASA_CR172559_20deg_root_break_profiles.json').read_text()); profiles=[]
for d in (a,b):
 for r in d['rows']:
  h=r['header_raw_fields'];c=h[2]-h[0];pairs=list(zip(d['common_chord_grid_xc'],r['ordinate_upper']))+list(reversed(list(zip(d['common_chord_grid_xc'],r['ordinate_lower']))));profiles.append((h[1],[(h[0]+x*c,h[5]+z*c) for x,z in pairs]))
im=Image.new('RGB',(1500,1000),'white');dr=ImageDraw.Draw(im);dr.text((25,20),'NASA CR172559 combined 20 deg - CONDITIONAL SOURCE REFERENCE',fill='black');dr.text((25,45),'X=XPL+xc*chord; Y=raw span; Z=field6+ordinate*chord. Source units; NOT model mm.',fill='black');dr.text((25,70),'Input contour chart, not CAD screenshot. Ruled loft is a reconstruction choice. No factory OML / print / flight release.',fill='black')
colors=['#555555','#137c8b','#425bc4','#c84c24','#348b3e']
# Plan: equal 1.7 px per source unit in X and Y, profiles appear as chord lines.
dr.text((25,110),'PLAN: equal X/Y scale; separate 127.22 / 127.24 overlap visually at this scale',fill='black')
for (y,pts),col in zip(profiles,colors):
 x0=min(x for x,z in pts);x1=max(x for x,z in pts);yy=160+y*1.7;dr.line((50+(x0-180)*1.7,yy,50+(x1-180)*1.7,yy),fill=col,width=2);dr.text((970,yy-15 if y==127.22 else yy+3 if y==127.24 else yy-5),str(y),fill=col)
dr.text((25,425),'ROOT BREAK: equal X/Z scale, 9 px per source unit; no span-gap bridge',fill='black')
for (y,pts),col in zip(profiles[-2:],colors[-2:]):
 pix=[(40+(x-500)*9,850-(z-150)*9) for x,z in pts];assert all(0<=x<1500 and 450<=z<950 for x,z in pix);dr.line(pix,fill=col,width=2);dr.text((80,465+(0 if y==127.22 else 25)),str(y),fill=col)
dr.text((25,945),'Two source contours remain distinct. Tiny Y separation does not justify blending their different thicknesses.',fill='black');out=P/'NASA_20deg_inboard_root_break_source_review.png';im.save(out)

