import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'analysis'/'original_front_sources'
FRAME=json.loads((SRC/'ABCDEF_shared_frame_candidate.json').read_text(encoding='utf-8'))
XREG=json.loads((SRC/'ABCDEF_FS_from_Navy_UPC_side_registration.json').read_text(encoding='utf-8'))
profiles={p['section']:p for p in FRAME['profiles']}; xmap={r['section']:r for r in XREG['sections']}
W,H=1400,820
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="white"/>','<text x="700" y="34" text-anchor="middle" font-family="Arial" font-size="24">F-14 A–F – X registriert, Z lokal – Entwicklungsstand 22.10.2026</text>','<text x="700" y="58" text-anchor="middle" font-family="Arial" font-size="13">Navy/UPC-Seiten-X-Registrierung; keine gemeinsame Aircraft-Waterline, kein Loft</text>']
# Oberer Bereich: longitudinale Positionen und lokale Z-Hoehen
left,right,top,bottom=90,1320,100,360
xs=[xmap[s]['nose_relative_X_nominal_mm'] for s in 'ABCDEF']
xmin,xmax=0,max(xs)+40
sx=lambda x:left+(x-xmin)/(xmax-xmin)*(right-left)
allzr=[]
for s in 'ABCDEF':
 p=profiles[s]; z0=float(p.get('axis_Z_candidate_mm',0)); zs=[q[2]-z0 for loop in p['loops_xyz_candidate_mm'] for q in loop]; allzr += zs
zmin,zmax=min(allzr)-10,max(allzr)+10
sz=lambda z:bottom-(z-zmin)/(zmax-zmin)*(bottom-top)
svg += [f'<line x1="{left}" y1="{sz(0):.1f}" x2="{right}" y2="{sz(0):.1f}" stroke="#777" stroke-dasharray="6,5"/>',f'<text x="{left}" y="{sz(0)-8:.1f}" font-family="Arial" font-size="12">lokales Z=0, keine Aircraft-WL</text>']
for s in 'ABCDEF':
 p=profiles[s]; xr=xmap[s]; z0=float(p.get('axis_Z_candidate_mm',0)); zs=[q[2]-z0 for loop in p['loops_xyz_candidate_mm'] for q in loop]; x=float(xr['nose_relative_X_nominal_mm']); lo,hi=xr['nose_relative_X_sensitivity_range_mm']
 svg.append(f'<rect x="{sx(lo):.1f}" y="{top}" width="{max(1,sx(hi)-sx(lo)):.1f}" height="{bottom-top}" fill="#eeeeee"/>')
 svg.append(f'<line x1="{sx(x):.1f}" y1="{sz(min(zs)):.1f}" x2="{sx(x):.1f}" y2="{sz(max(zs)):.1f}" stroke="black" stroke-width="3"/>')
 svg.append(f'<circle cx="{sx(x):.1f}" cy="{sz(0):.1f}" r="5" fill="white" stroke="black"/>')
 svg.append(f'<text x="{sx(x):.1f}" y="{top-10}" text-anchor="middle" font-family="Arial" font-size="14">{s}</text>')
 svg.append(f'<text x="{sx(x):.1f}" y="{bottom+22}" text-anchor="middle" font-family="Arial" font-size="11">X={x:.1f} mm</text>')
# Unterer Bereich: Frontansichten der sechs lokalen Querschnitte
panel_y0,panel_h=440,300; panel_w=210
for i,s in enumerate('ABCDEF'):
 p=profiles[s]; z0=float(p.get('axis_Z_candidate_mm',0)); loops=p['loops_xyz_candidate_mm']; ys=[q[1] for loop in loops for q in loop]; zs=[q[2]-z0 for loop in loops for q in loop]
 cx=80+i*220+105; cy=panel_y0+150; span=max(max(abs(min(ys)),abs(max(ys))),max(abs(min(zs)),abs(max(zs))),1); k=90/span
 svg.append(f'<rect x="{cx-100}" y="{panel_y0}" width="200" height="{panel_h}" fill="none" stroke="#cccccc"/>')
 svg.append(f'<text x="{cx}" y="{panel_y0+20}" text-anchor="middle" font-family="Arial" font-size="15">Sektion {s}</text>')
 svg.append(f'<line x1="{cx-85}" y1="{cy}" x2="{cx+85}" y2="{cy}" stroke="#dddddd"/><line x1="{cx}" y1="{cy-105}" x2="{cx}" y2="{cy+105}" stroke="#dddddd"/>')
 for loop in loops:
  pts=' '.join(f'{cx+q[1]*k:.1f},{cy-(q[2]-z0)*k:.1f}' for q in loop+[loop[0]])
  svg.append(f'<polyline points="{pts}" fill="none" stroke="black" stroke-width="1.8"/>')
 svg.append(f'<text x="{cx}" y="{panel_y0+282}" text-anchor="middle" font-family="Arial" font-size="11">FS {xmap[s]["FS_nominal_in"]:.1f} in</text>')
svg.append('<text x="700" y="800" text-anchor="middle" font-family="Arial" font-size="12">Entwicklungsstudie: X-Lage belastbarer als gestern; absolute Z-Lage weiterhin bewusst unregistriert.</text>')
svg.append('</svg>')
out=ROOT/'docs'/'images'/'f14_ABCDEF_X_registered_local_Z_20261022.svg'; out.write_text('\n'.join(svg),encoding='utf-8'); print(out)
