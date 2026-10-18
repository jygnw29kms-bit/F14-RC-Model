"""Original sampled projections only; no invented nose cross sections."""
import FreeCAD as App,Part,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];B=Path(__file__).parent
p=R/'analysis/original_front_sources/nose_to_A_stroke_center_samples.json';f=R/'analysis/propulsion_source_silhouette_constraints_v134.json';h={str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [p,f]};j=json.loads(p.read_text());frame=json.loads(f.read_text());s=frame['common_scale_mm_per_pixel'];d=App.newDocument('F14_ORIGINAL_NOSE_PROJECTION_GUIDES');rows=[]
for name in ['PLAN_UPPER','PLAN_LOWER','SIDE_TOP','SIDE_BOTTOM']:
 pts=[]
 for t in j['samples']:
  x=t['X_candidate_mm']
  if name.startswith('PLAN'):v=App.Vector(x,(t['plan_stroke_center_y_pixels'][0 if name.endswith('UPPER') else 1]-1296.25)*s,0)
  else:v=App.Vector(x,0,t['side_top_Z_candidate_mm'] if name.endswith('TOP') else t['side_bottom_Z_candidate_mm'])
  pts.append(v)
 sh=Part.makePolygon(pts);assert sh.isValid() and len(sh.Edges)==8
 obj=d.addObject('PartDesign::Feature',name);obj.Shape=sh;obj.Label=name+' Originalprojektion / Kandidatenrahmen ungeprueft'
 rows.append(dict(name=name,points=len(pts),edges=len(sh.Edges),valid=sh.isValid(),solids=len(sh.Solids),first=[pts[0].x,pts[0].y,pts[0].z],last=[pts[-1].x,pts[-1].y,pts[-1].z]))
d.recompute();out=B/'F14_ORIGINAL_NOSE_PROJECTION_GUIDES.FCStd';d.saveAs(str(out));App.closeDocument(d.Name)
assert h=={str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [p,f]}
a=dict(status='NATIVE_ORIGINAL_NOSE_PROJECTION_GUIDES_CREATED',inputs=h,rows=rows,output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),hinweise=['Gerade Segmente verbinden Originalproben; Zwischenkontur nicht quellenverifiziert.','Fehlende Koordinate null bedeutet Projektion, keine Oberflaechenlage.','Gemeinsamer X-Ursprung und metrischer Rahmen bleiben ungeprueft.','Keine Querschnittsform, Oberflaeche oder Produktionsgeometrie erzeugt.'],master_geaendert=False,produktion_freigegeben=False)
(B/'freecad_original_nose_projection_guides_audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a))
