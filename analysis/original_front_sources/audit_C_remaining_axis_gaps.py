"""Verbleibende Komponentenabstaende, keine erfundenen Achsenbruecken."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
O=Path(__file__).parent;R=O.parents[1];graph=json.loads((O/'C_raster_segment_coverage_v3.json').read_text(encoding='utf-8'));names=list(graph['inputs']);data={n:json.loads((O/(n+'.json')).read_text(encoding='utf-8')) for n in names};rows=[]
for k,row in enumerate(graph['rows']):
 pts={n+':'+str(i):s for n in names for i,s in enumerate(data[n]['cases'][k]['segments_pixel'])};groups=[sum((pts[n] for n in comp),[]) for comp in row['components']];pairs=[]
 for i,j,label in [(0,1,'obere_vertikale_Achse'),(2,3,'untere_vertikale_Achse'),(0,2,'linker_aeusserer_Achsenanschluss'),(1,3,'rechter_aeusserer_Achsenanschluss')]:
  a=np.array(groups[i]);b=np.array(groups[j]);ds=((a[:,None,:]-b[None,:,:])**2).sum(axis=2);u,v=np.unravel_index(ds.argmin(),ds.shape)
  pairs.append(dict(region=label,a=groups[i][u],b=groups[j][v],minimum_sample_gap_pixel=math.sqrt(float(ds[u,v])),measured_bridge=False))
 rows.append(dict(threshold=row['threshold'],pairs=pairs))
r=dict(status='C_VERBLEIBENDE_ACHSENLUECKEN_LOKALISIERT',input_sha256=hashlib.sha256((O/'C_raster_segment_coverage_v3.json').read_bytes()).hexdigest(),rows=rows,limits=['Minimaler Abstand vorhandener Rasterpunkte, keine Konturlaenge oder Fehlergrenze.','Horizontale und vertikale Achsen ueberlagern Originalstriche. Fehlende Punkte sind ungemessen.','Keine Verbindung, Interpolation oder geschlossene Sektion erzeugt.'],production_release=False)
(O/'C_remaining_axis_gaps.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
im=Image.open(R/'references/UPC_Figure3_15_source_exact.png').convert('RGB');canvas=Image.new('RGB',(1000,480),'white');dr=ImageDraw.Draw(canvas)
for k,pair in enumerate(rows[1]['pairs']):
 a,b=pair['a'],pair['b'];cx=(a[0]+b[0])//2;cy=(a[1]+b[1])//2;box=(cx-30,cy-20,cx+30,cy+20);crop=im.crop(box).resize((480,320));cd=ImageDraw.Draw(crop)
 for x,y in [a,b]:
  xx=(x-box[0])*8;yy=(y-box[1])*8;cd.ellipse((xx-4,yy-4,xx+4,yy+4),outline='red',width=2)
 # Four panels in one row pair, kept separate from underlying source.
 x=(k%2)*500;y=(k//2)*240;canvas.paste(crop.resize((300,200)),(x,y+25));dr.text((x,y),pair['region'],fill='black')
canvas.save(O/'C_remaining_axis_gaps_overlay.png');print(rows)
