"""Determine C polygon nesting after its separate boundary-intersection audit."""
from pathlib import Path
import json,hashlib,runpy
p=Path(__file__).parent
source=p/'front_sections_pixel_candidates.json';raw=source.read_bytes()
profile=next(v for v in json.loads(raw)['profiles'] if v['section']=='C');loops=profile['loops_pixel']
topology=runpy.run_path(str(p/'audit_pixel_topology.py'))['audit'](source)
assert topology['all_loops_simple']
assert all(not pair['boundary_intersections'] for row in topology['results'] if row['section']=='C' for pair in row['inter_loop_boundary_checks'])
def inside(pt,poly):
    x,y=pt;hit=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:hit=not hit
    return hit
assert inside((1,1),[[0,0],[2,0],[2,2],[0,2]])
assert not inside((3,1),[[0,0],[2,0],[2,2],[0,2]])
checks=[]
for i in range(len(loops)):
    for j in range(len(loops)):
        if i!=j:checks.append(dict(inner_loop=i,container_loop=j,all_vertices_inside=all(inside(v,loops[j]) for v in loops[i])))
assert all(next(v['all_vertices_inside'] for v in checks if v['inner_loop']==i and v['container_loop']==0) for i in (1,2))
assert not any(v['all_vertices_inside'] for v in checks if v['container_loop']!=0)
area=abs(profile['loop_summary'][0]['signed_area_pixels2'])-sum(abs(v['signed_area_pixels2']) for v in profile['loop_summary'][1:])
report=dict(source_sha256=hashlib.sha256(raw).hexdigest(),section='C',checks=checks,pixel_region_interpretation='One outer polygon (loop 0) encloses two disjoint inner polygons (loops 1 and 2). The traced source candidate therefore supports a perforated section region, not three separate filled solids.',net_polygon_area_pixels2=area,visually_reviewed_against_original_raster=True,curve_interpolation_verified=False,metric_registration_verified=False,production_loft_allowed=False,limitations='Nesting applies only to straight-segment traced polygons. Original raster overlay reviewed; hatch and inlet openings are consistent with this topology. Does not establish 3D duct continuity, wall thickness, metric accuracy or production readiness.')
(p/'C_loop_nesting_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
