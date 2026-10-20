from pathlib import Path
import json,hashlib
import numpy as np
O=Path(__file__).parent;p=O/'C_open_raster_chains.json';j=json.loads(p.read_text(encoding='utf-8'));rows=[]
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def on(a,b,c):return cross(a,b,c)==0 and min(a[0],b[0])<=c[0]<=max(a[0],b[0]) and min(a[1],b[1])<=c[1]<=max(a[1],b[1])
def hit(a,b,c,d):
 x,y,z,w=cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b)
 return (x*y<0 and z*w<0) or on(a,b,c) or on(a,b,d) or on(c,d,a) or on(c,d,b)
for case in j['cases']:
 edges=[(k,i,a,b) for k,s in enumerate(case['segments_pixel']) for i,(a,b) in enumerate(zip(s,s[1:]))];v=np.array([[min(a[0],b[0]),max(a[0],b[0]),min(a[1],b[1]),max(a[1],b[1])] for k,i,a,b in edges]);bad=[];checked=0
 for n,(k,i,a,b) in enumerate(edges):
  candidates=np.where((v[:,0]<=v[n,1])&(v[:,1]>=v[n,0])&(v[:,2]<=v[n,3])&(v[:,3]>=v[n,2]))[0]
  for m in candidates:
   if m<=n:continue
   l,h,c,d=edges[m]
   if k==l and abs(i-h)==1:continue
   checked+=1
   if hit(a,b,c,d):bad.append([k,i,l,h])
 rows.append(dict(threshold=case['threshold'],edge_count=len(edges),bounding_box_candidate_pairs_checked=checked,nonadjacent_intersections=bad));assert not bad,bad
(O/'C_open_chain_intersections.json').write_text(json.dumps(dict(status='OFFENE_C_KETTEN_OHNE_NICHTBENACHBARTE_SCHNITTE',input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=rows,limits=['Exakte ganzzahlige2DStreckentests; benachbarte Kanten ausgenommen.','Keine Aussage ueber fehlende Achsenkontur, Strichmitte oder metrische Originalhaut.'],production_release=False),ensure_ascii=False,indent=2),encoding='utf-8');print(rows)
