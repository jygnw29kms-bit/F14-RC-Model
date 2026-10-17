from pathlib import Path
import json,math,hashlib
p=Path(__file__).parent;source=p/'front_sections_pixel_candidates.json';data=json.loads(source.read_text());c=next(v for v in data['profiles'] if v['section']=='C');mapped=next(v for v in json.loads((p/'front_shared_frame_candidate.json').read_text())['profiles'] if v['section']=='C');scale=mapped['isotropic_mm_per_section_pixel'];outer=c['loops_pixel'][0]
def point_segment(q,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];den=dx*dx+dy*dy
 if den==0:return math.dist(q,a)
 t=max(0,min(1,((q[0]-a[0])*dx+(q[1]-a[1])*dy)/den));return math.hypot(q[0]-a[0]-t*dx,q[1]-a[1]-t*dy)
assert abs(point_segment([1,1],[0,0],[2,0])-1)<1e-12
rows=[]
for i in [1,2]:
 inner=c['loops_pixel'][i];best=None
 for j,(a,b) in enumerate(zip(inner,inner[1:]+inner[:1])):
  for k,(d,e) in enumerate(zip(outer,outer[1:]+outer[:1])):
   distance=min(point_segment(a,d,e),point_segment(b,d,e),point_segment(d,a,b),point_segment(e,a,b))
   if best is None or distance<best[0]:best=(distance,j,k)
 area=abs(c['loop_summary'][i]['signed_area_pixels2'])*scale**2
 rows.append(dict(inner_loop=i,minimum_polygon_boundary_gap_pixels=best[0],minimum_candidate_gap_mm=best[0]*scale,inner_edge_index=best[1],outer_edge_index=best[2],candidate_aperture_area_mm2=area,ratio_to_assumed_50mm_fan_28mm_hub_FSA=area/(math.pi*(50**2-28**2)/4)))
report=dict(status='C_PIXEL_SECTION_APERTURE_AND_BOUNDARY_GAP_STUDY',input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),candidate_mm_per_pixel=scale,records=rows,method='Minimum endpoint-to-segment distances over nonintersecting straight polygon edges; exact for these planar polygon boundaries. Does not represent 3D normal wall thickness.',metric_registration_verified=False,physical_wall_thickness_verified=False,flow_performance_verified=False,production_geometry=False)
(p/'C_aperture_and_gap_study.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(rows)
