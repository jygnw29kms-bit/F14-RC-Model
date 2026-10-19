import FreeCAD as App,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];B=Path(__file__).parent;p=B/'F14_NOSE_A_SHAPE_SENSITIVITY.FCStd';h=hashlib.sha256(p.read_bytes()).hexdigest();d=App.openDocument(str(p));sh=d.getObject('FORMHYPOTHESE').Shape;rows=[]
for s in json.loads((R/'analysis/original_front_sources/nose_intermediate_projection_check_samples.json').read_text())['samples']:
 x=s['X_candidate_mm'];w=sh.slice(App.Vector(1,0,0),x);assert len(w)==1;pts=[]
 for e in w[0].Edges:pts.extend(e.discretize(Deflection=.001))
 assert pts and max(abs(v.x-x) for v in pts)<1e-6
 width=max(v.y for v in pts)-min(v.y for v in pts);top=max(v.z for v in pts);bottom=min(v.z for v in pts)
 rows.append(dict(source_x_pixel=s['source_x_pixel'],width_residual_mm=width-s['width_candidate_mm'],top_residual_mm=top-s['top_Z_candidate_mm'],bottom_residual_mm=bottom-s['bottom_Z_candidate_mm']))
App.closeDocument(d.Name);assert hashlib.sha256(p.read_bytes()).hexdigest()==h
report=dict(status='NATIVE_NASENHYPOTHESE_AN_UNABHAENGIGEN_ZWISCHENPROBEN_GEPRUEFT',archive_sha256=h,records=rows,max_abs_projection_residual_mm=max(abs(v[k]) for v in rows for k in ['width_residual_mm','top_residual_mm','bottom_residual_mm']),hinweis='Projektionsvergleich im ungeprueften gemeinsamen Kandidatenrahmen. Kein Querschnittsformnachweis; Ursprungskorrektur nicht angewandt.',produktion_freigegeben=False,originalform_bestaetigt=False)
(B/'freecad_nose_A_shape_projection_comparison.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
