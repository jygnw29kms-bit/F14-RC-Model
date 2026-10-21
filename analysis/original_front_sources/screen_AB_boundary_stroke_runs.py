"""Strichlauf-Screening, keine automatische Strichmittelkontur."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';a=np.array(Image.open(src).convert('L'));sections=[]
for sec,x0,x1,ys,axis in [('A',1840,1960,range(245,337,7),(270,281)),('B',1820,1980,range(499,660,10),(604,617))]:
 rows=[]
 for y in ys:
  if axis[0]<=y<=axis[1]:continue
  for t in [96,128,160]:
   xs=np.where(a[y,x0:x1]<t)[0]+x0;assert len(xs)>0;groups=[g for g in np.split(xs,np.where(np.diff(xs)>1)[0]+1) if len(g)];left,right=groups[0],groups[-1]
   bounds=[]
   for side,g in [('left',left),('right',right)]:
    border=g[0]==x0 or g[-1]==x1-1;merged=len(g)>6
    bounds.append(dict(side=side,first_x=int(g[0]),last_x=int(g[-1]),dark_run_pixels=len(g),roi_border=bool(border),possible_merged_or_tangent_run=bool(merged),run_midpoint_x_candidate=None if border or merged else float((g[0]+g[-1])/2)))
   rows.append(dict(y_pixel=y,threshold=t,boundaries=bounds))
 sections.append(dict(section=sec,samples=rows,flagged_boundaries=sum(b['roi_border'] or b['possible_merged_or_tangent_run'] for r in rows for b in r['boundaries']),maximum_run_pixels=max(b['dark_run_pixels'] for r in rows for b in r['boundaries'])))
r=dict(status='AB_RANDSTRICHLAEUFE_GESCREENT_KEINE_MITTELKONTUR',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),sections=sections,limits=['Horizontale Lauflaenge abhaengig von Neigung und Kruemmung, keine normale Strichdicke.','Grenze6Pixel ist nur Screeningheuristik, keine Messunsicherheit oder physikalischer Grenzwert.','Kurze Laeufe koennen semantisch trotzdem falsch sein; Mittelpunkte sind nur Kandidaten, nicht freigegebene Konturpunkte.','Achsenbereiche ausgelassen; keine Geometrie, Registrierung oder Produktionsfreigabe.'],production_release=False)
(O/'AB_boundary_stroke_run_screen.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(s['section'],len(s['samples']),s['flagged_boundaries'],s['maximum_run_pixels']) for s in sections])
