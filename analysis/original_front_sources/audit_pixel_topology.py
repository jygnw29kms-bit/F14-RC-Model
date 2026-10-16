"""Audit traced pixel polygons only; no metric or aircraft fidelity approval."""
from pathlib import Path
import json, hashlib, math

def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def on(a,b,c):
    return abs(cross(a,b,c))<1e-9 and all(min(a[k],b[k])-1e-9<=c[k]<=max(a[k],b[k])+1e-9 for k in (0,1))
def intersects(a,b,c,d):
    x,y,z,w=cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b)
    return (x*y<0 and z*w<0) or on(a,b,c) or on(a,b,d) or on(c,d,a) or on(c,d,b)
def audit(path):
    raw=path.read_bytes(); data=json.loads(raw); results=[]
    for profile in data['profiles']:
        loops=profile['loops_pixel']; pairs=[]
        for n,pts in enumerate(loops):
            size=len(pts); hits=[]
            for i in range(size):
                for j in range(i+1,size):
                    if j==i+1 or (i==0 and j==size-1): continue
                    if intersects(pts[i],pts[(i+1)%size],pts[j],pts[(j+1)%size]): hits.append([i,j])
            zero=[i for i in range(size) if pts[i]==pts[(i+1)%size]]
            results.append(dict(section=profile['section'],loop=n,vertices=size,finite=all(math.isfinite(v) for pt in pts for v in pt),zero_length_edges=zero,nonadjacent_intersections=hits,simple_polygon=not hits and not zero))
        for i in range(len(loops)):
            for j in range(i+1,len(loops)):
                hits=[]
                for a in range(len(loops[i])):
                    for b in range(len(loops[j])):
                        if intersects(loops[i][a],loops[i][(a+1)%len(loops[i])],loops[j][b],loops[j][(b+1)%len(loops[j])]): hits.append([a,b])
                pairs.append(dict(loops=[i,j],boundary_intersections=hits))
        for row in results:
            if row['section']==profile['section']: row['inter_loop_boundary_checks']=pairs
    return dict(input_sha256=hashlib.sha256(raw).hexdigest(),scope='Manual straight-segment pixel polygons only; excludes curve interpolation, tracing accuracy, scale, station registration and loop containment semantics.',results=results,all_loops_simple=all(x['simple_polygon'] and x['finite'] for x in results),production_loft_allowed=False)
if __name__=='__main__':
    p=Path(__file__).parent
    report=audit(p/'front_sections_pixel_candidates.json')
    (p/'front_sections_topology_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
