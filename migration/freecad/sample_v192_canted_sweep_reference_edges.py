from pathlib import Path
import FreeCAD as App,json,hashlib
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/CANTED_AXIS_SWEEP_REFERENCE_STUDY_ONLY.FCStd';before=hashlib.sha256(p.read_bytes()).hexdigest();prior=json.loads((R/'analysis/v192_canted_sweep_reference_build.json').read_text());assert before==prior['output_sha256'];out=R/'analysis/v192_canted_sweep_edge_samples.json';assert not out.exists();d=App.openDocument(str(p));rows=[]
try:
 for obj in d.Objects:
  if hasattr(obj,'Shape') and not obj.Shape.isNull():
   lines=[[list(point) for point in edge.discretize(Number=9)] for edge in obj.Shape.Edges]
   rows.append(dict(object=obj.Name,polylines_xyz_mm=lines))
finally:App.closeDocument(d.Name)
assert before==hashlib.sha256(p.read_bytes()).hexdigest();assert len(rows)==8
out.write_text(json.dumps(dict(status='NATIVE_EDGE_SAMPLES_FOR_WIREFRAME_REVIEW_ONLY',reference_sha256=before,rows=rows,limits=['Nine sample points per native edge; visual overview only, not exact curve or hidden-line rendering.','Not a CAD screenshot or collision/manufacturing verification.'],production_release=False),indent=2)+'\n');print('8 saved native reference objects reopened and sampled for wireframe review')
