"""Abstandsgraph vorhandener C-Rastersegmente, ohne neue Verbindungsgeometrie."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
O=Path(__file__).parent;R=O.parents[1];names=['C_upper_raster_guides','C_lower_raster_guides','C_inlet_lower_sides','C_inlet_outer_upper_sides','C_tips_shoulders'];data={n:json.loads((O/(n+'.json')).read_text(encoding='utf-8')) for n in names};rows=[]
for k,t in enumerate([96,128,160]):
 segs=[(n+':'+str(i),s) for n in names for i,s in enumerate(data[n]['cases'][k]['segments_pixel'])];edges=[];parent=list(range(len(segs)))
 def root(i):
  while parent[i]!=i:i=parent[i]
  return i
 for i,(ni,si) in enumerate(segs):
  for j in range(i+1,len(segs)):
   nj,sj=segs[j];aa=np.array(si);bb=np.array(sj);ds=((aa[:,None,:]-bb[None,:,:])**2).sum(axis=2);ii,jj=np.unravel_index(ds.argmin(),ds.shape);gap=math.sqrt(float(ds[ii,jj]))
   if gap<=math.sqrt(2)+1e-9:
    parent[root(j)]=root(i);edges.append(dict(a=ni,b=nj,minimum_gap_pixel=gap,point_a=si[ii],point_b=sj[jj]))
 comps={}
 for i,(n,s) in enumerate(segs):comps.setdefault(root(i),[]).append(n)
 rows.append(dict(threshold=t,segment_count=len(segs),near_pairs=edges,components=list(comps.values()),component_count=len(comps)))
report=dict(status='C_RASTERSEGMENT_ABDECKUNG_GEPRUEFT',inputs={n:hashlib.sha256((O/(n+'.json')).read_bytes()).hexdigest() for n in names},rows=rows,method='Minimaler Punktabstand aller Segmentpaare. Graphkante nur bei Abstand<=sqrt(2)Pixel. Naehe ist keine bewiesene geometrische Verbindung.',limits=['Abstandsgraph prueft keine zyklische Kontur, Orientierung, Selbstschnittfreiheit oder Strichidentitaet.','Luecken nicht geschlossen. Achsenband, aeussere Spitzen und Schulteranschluesse bleiben separat zu verfolgen.','Ueberlappende Rasterproben koennen derselben Strichkante folgen, ohne identische native Polylinien zu bilden.'],production_release=False)
(O/'C_raster_segment_coverage_v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
im=Image.open(R/'references/UPC_Figure3_15_source_exact.png').convert('RGB').crop((805,520,1330,700)).resize((1575,540));dr=ImageDraw.Draw(im);colors=['red','blue','green','magenta','orange']
for n,col in zip(names,colors):
 for i,s in enumerate(data[n]['cases'][1]['segments_pixel']):
  pts=[((x-805)*3,(y-520)*3) for x,y in s];dr.line(pts,fill=col,width=1);x,y=pts[len(pts)//2];dr.text((x,y),str(names.index(n))+':'+str(i),fill=col)
im.save(O/'C_raster_segment_coverage_v2_overlay.png');print([(r['threshold'],r['segment_count'],r['component_count']) for r in rows])
