"""RC internal aperture sizing study; original outer and inner traces untouched."""
from pathlib import Path
import json,math,hashlib
p=Path(__file__).parent;source=p/'front_sections_pixel_candidates.json';c=next(v for v in json.loads(source.read_text())['profiles'] if v['section']=='C');mapped=next(v for v in json.loads((p/'front_shared_frame_candidate.json').read_text())['profiles'] if v['section']=='C');scale=mapped['isotropic_mm_per_section_pixel'];outer=c['loops_pixel'][0]
def distance(q,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((q[0]-a[0])*dx+(q[1]-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(q[0]-a[0]-t*dx,q[1]-a[1]-t*dy)
def gap(loop):
 return min(min(distance(a,d,e),distance(b,d,e),distance(d,a,b),distance(e,a,b)) for a,b in zip(loop,loop[1:]+loop[:1]) for d,e in zip(outer,outer[1:]+outer[:1]))*scale
rows=[]
for index in (1,2):
 original=c['loops_pixel'][index];crosses=[a[0]*b[1]-b[0]*a[1] for a,b in zip(original,original[1:]+original[:1])];area=sum(crosses)/2
 center=[sum((a[k]+b[k])*v for a,b,v in zip(original,original[1:]+original[:1],crosses))/(6*area) for k in (0,1)]
 def shrink(t):return [[center[0]+t*(a[0]-center[0]),center[1]+t*(a[1]-center[1])] for a in original]
 target=.81;baseline=gap(original);factor=1.0
 if baseline<target:
  vals=[gap(shrink(1-i*.0005)) for i in range(101)]
  if any(b<a-1e-9 for a,b in zip(vals,vals[1:])):raise ValueError('Gap nonmonotonic; do not bisect')
  if vals[-1]<target:raise ValueError('Study range insufficient')
  low,high=.95,1.0
  for _ in range(45):
   mid=(low+high)/2
   if gap(shrink(mid))>=target:low=mid
   else:high=mid
  factor=low
 candidate=shrink(factor);ax,ay=c['source_section_axis_pixel'];xyz=[[mapped['station_X_candidate_mm'],(x-ax)*scale,mapped['axis_Z_candidate_mm']+(ay-y)*scale] for x,y in candidate]
 rows.append(dict(inner_loop=index,baseline_planar_gap_mm=baseline,homothetic_scale=factor,candidate_planar_gap_mm=gap(candidate),area_loss_fraction=1-factor**2,candidate_aperture_area_mm2=abs(area)*scale**2*factor**2,RC_internal_candidate_loop_xyz_mm=xyz))
report=dict(status='RC_INTERNAL_C_APERTURE_PLANAR_MARGIN_STUDY_ONLY',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),original_outer_trace_modified=False,original_inner_trace_modified=False,planar_margin_target_mm=.81,records=rows,limitations='Candidate frame scale unverified. Homothetic internal aperture reduction is an RC design assumption, not original opening geometry. Planar margin does not establish 3D normal wall thickness, printability or flow performance.',production_geometry=False)
(p/'RC_C_aperture_margin_study.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print([(v['inner_loop'],v['homothetic_scale'],v['candidate_planar_gap_mm'],v['area_loss_fraction']) for v in rows])
