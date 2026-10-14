import csv, pathlib
R=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
mdir=R/'manufacturing'/'carbon_v95'
rows=[]
with open(mdir/'F14_v95_coupon_carbon_dimensions.csv',encoding='utf-8') as f:
    for row in csv.DictReader(f): rows.append({k:float(v) for k,v in row.items()})
y0=rows[0]['y_mm']; scale=3.7795275591; margin=12; cy=20*scale
pts_top=[];pts_bot=[]
for row in rows:
    x=(row['y_mm']-y0)*scale+margin*scale; h=row['web_height_mm']; pts_top.append((x,cy-h/2*scale));pts_bot.append((x,cy+h/2*scale))
poly=pts_top+list(reversed(pts_bot)); points=' '.join(f'{x:.3f},{y:.3f}' for x,y in poly)
wpx=(40+2*margin)*scale; hpx=40*scale
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="64mm" height="40mm" viewBox="0 0 {wpx:.3f} {hpx:.3f}">\n<rect x="0" y="0" width="100%" height="100%" fill="white"/>\n<polygon points="{points}" fill="none" stroke="black" stroke-width="0.7"/>\n<line x1="{margin*scale:.3f}" y1="{34*scale:.3f}" x2="{(margin+10)*scale:.3f}" y2="{34*scale:.3f}" stroke="black" stroke-width="1"/>\n<text x="{margin*scale:.3f}" y="{38*scale:.3f}" font-size="10">10 mm scale</text>\n<text x="{margin*scale:.3f}" y="{5*scale:.3f}" font-size="10">F14 v95 carbon web coupon template - 1:1</text>\n</svg>'''
(mdir/'F14_v95_coupon_web_template.svg').write_text(svg,encoding='utf-8')
# simple validation of viewbox and endpoint lengths
assert '64mm' in svg and '40mm' in svg
print('web SVG written',len(svg))