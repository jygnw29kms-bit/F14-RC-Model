import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'analysis'/'original_front_sources'
P=SRC/'C_open_raster_chains.json';FRAME=SRC/'front_shared_frame_candidate.json';OUT=SRC/'C_open_chains_semantic_summary.json'
j=json.loads(P.read_text(encoding='utf-8'));f=json.loads(FRAME.read_text(encoding='utf-8'));scale=float(f['profiles'][2]['isotropic_mm_per_section_pixel']);c=next(x for x in j['cases'] if x['threshold']==128)
rows=[]
for i,s in enumerate(c['segments_pixel']):
 xs=[p[0] for p in s];ys=[p[1] for p in s]
 rows.append({'chain_index':i,'points':len(s),'start_pixel':s[0],'end_pixel':s[-1],'x_min':min(xs),'x_max':max(xs),'y_min':min(ys),'y_max':max(ys),'pixel_width':max(xs)-min(xs),'pixel_height':max(ys)-min(ys),'candidate_width_mm':(max(xs)-min(xs))*scale,'candidate_height_mm':(max(ys)-min(ys))*scale})
# Paarweise Endpunktdistanzen, nur als Topologiehilfe.
import math
ends=[]
for r in rows:
 for kind,p in [('start',r['start_pixel']),('end',r['end_pixel'])]:ends.append((r['chain_index'],kind,p))
pairs=[]
for a in range(len(ends)):
 for b in range(a+1,len(ends)):
  ia,ka,pa=ends[a];ib,kb,pb=ends[b]
  if ia==ib:continue
  d=math.dist(pa,pb)
  if d<25:pairs.append({'a':[ia,ka,pa],'b':[ib,kb,pb],'gap_pixel':d,'gap_candidate_mm':d*scale})
out={'status':'C_VIER_OFFENE_KETTEN_SEMANTISCH_ZUSAMMENGEFASST','threshold':128,'candidate_scale_mm_per_pixel':scale,'input_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'chains':rows,'near_endpoint_pairs_under_25px':sorted(pairs,key=lambda x:x['gap_pixel']),'interpretation':['Die vier Ketten bleiben topologisch offen und werden nicht zu einer Haut geschlossen.','Bounding-Box und Endpunktnaehe sind nur Strukturhinweise; sie beweisen keine gemeinsame physische Kontur.','Seitenprojektionshuellen duerfen nur nach Zuordnung zu passenden sichtbaren Ketten als Registrierungsanker verwendet werden.'],'loft_allowed':False,'master_change_allowed':False,'production_release':False}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps(out,indent=2,ensure_ascii=False))
