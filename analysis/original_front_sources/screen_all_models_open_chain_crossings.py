"""Independent strict interior crossing screen of sampled open NASA chains."""
from pathlib import Path
import json,hashlib,math
O=Path(__file__).resolve().parent
inv=json.loads((O/'NASA_all_models_reference_study_inventory.json').read_text(encoding='utf-8'))
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
rows=[]
for ent in inv['rows']:
 p=O/ent['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==ent['sha256']
 for index,sec in enumerate(json.loads(p.read_text(encoding='utf-8'))['rows']):
  pts=sec['points_YZ_source'];assert all(math.isfinite(v) for pt in pts for v in pt)
  crossings=[];edges=list(zip(pts[:-1],pts[1:]))
  for i,(a,b) in enumerate(edges):
   for j in range(i+2,len(edges)):
    c,d=edges[j]
    ab1,ab2,cd1,cd2=cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b)
    if ab1*ab2 < 0 and cd1*cd2 < 0:crossings.append([i,j])
  rows.append(dict(file=ent['file'],row=index,model=sec.get('model',ent['models'][0]),x_source=sec['x_source'],boundary_side=sec.get('source_boundary_side'),
   points=len(pts),strict_interior_crossings=crossings,minimum_edge_length_source_units=min(math.dist(a,b) for a,b in edges)))
assert len(rows)==35
result=dict(status='SAMPLED_OPEN_CHAIN_STRICT_CROSSING_SCREEN',rows=rows,
 strict_crossing_count=sum(len(r['strict_interior_crossings']) for r in rows),
 limits=['Only strict interior intersections of nonadjacent sampled straight edges; collinear overlaps and tangential touches are outside this screen.',
 'No closing axis edge added; no polygon, surface, loft or solid constructed.',
 'No guarantee between samples or across longitudinal stations; 697 left/right remain separate.',
 'Physical units, registration and original aircraft skin remain unverified.'],production_release=False)
(O/'NASA_all_models_open_chain_crossing_screen.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'sections':len(rows),'strict_crossings':result['strict_crossing_count'],'zero_length_edges_present':any(r['minimum_edge_length_source_units']==0 for r in rows)}))
