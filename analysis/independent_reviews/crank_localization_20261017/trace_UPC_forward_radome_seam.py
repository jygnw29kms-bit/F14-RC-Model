"""Trace original visible forward radome seam; no 3D station inferred."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[3];src=R/'references/UPC_Figure3_15_source_exact.png';a=np.array(Image.open(src).convert('L'));rows=[]
for name,ys in [('plan',range(1270,1321)),('side',range(2810,2846))]:
 pts=[]
 for y in ys:
  x=np.where(a[y,520:550]<128)[0]+520
  assert len(x)>0
  assert np.all(np.diff(x)==1), 'Ambiguous disconnected stroke'
  pts.append(dict(y_px=y,x_stroke_interval_px=[int(x.min()),int(x.max())],x_stroke_center_px=float((x.min()+x.max())/2)))
 rows.append(dict(view=name,points=pts,x_center_range_px=[min(p['x_stroke_center_px'] for p in pts),max(p['x_stroke_center_px'] for p in pts)]))
j=dict(status='ORIGINAL_FORWARD_RADOME_SEAM_PIXEL_TRACES_RECOVERED',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),selection='Visually reviewed narrow x520..549 band; interior seam rows only, excluding outer-contour intersections.',views=rows,visual_finding='Forward seam is curved in plan and tilted in side. Source supports a physical boundary curve, not one constant-X station.',registration_implication='Do not register two views by arbitrary seam midpoints at different Y/WL. No verified homologous seam point or station number has been recovered.',limits=['Traced segment excludes seam ends.','Stroke center does not imply subpixel aircraft accuracy.','Do not flatten this boundary to a plane or use it as a verified FS value.'],next='Seek manufacturer/Navy station label for an identifiable homologous point; retain nose view offsets independently until that evidence exists.',metric_registration_verified=False,geometry_changed=False,production_release=False)
Path(__file__).with_name('UPC_forward_radome_seam_traces.json').write_text(json.dumps(j,indent=2)+'\n');print([(r['view'],len(r['points']),r['x_center_range_px']) for r in rows])
