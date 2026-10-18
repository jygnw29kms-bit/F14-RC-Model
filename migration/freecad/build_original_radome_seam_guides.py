"""Separate projected source guides in the historical UNVERIFIED candidate frame."""
import FreeCAD as App,Part,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];base=Path(__file__).parent
source=R/'analysis/independent_reviews/crank_localization_20261017/UPC_forward_radome_seam_traces.json';frame=R/'analysis/propulsion_source_silhouette_constraints_v134.json'
hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,frame]}
j=json.loads(source.read_text());f=json.loads(frame.read_text());s=f['common_scale_mm_per_pixel'];d=App.newDocument('F14_ORIGINAL_RADOME_SEAM_GUIDES');rows=[]
for v in j['views']:
 pts=[]
 for p in v['points']:
  x=f['x_mapping']['E_model_mm']+(p['x_stroke_center_px']-f['x_mapping']['E_source_px'])*s
  if v['view']=='plan': vec=App.Vector(x,(p['y_px']-1296.25)*s,0)
  else: vec=App.Vector(x,0,(f['z_mapping']['E_axis_source_y_px']-p['y_px'])*s)
  pts.append(vec)
 shape=Part.makePolygon(pts);assert shape.isValid() and len(shape.Edges)==len(pts)-1
 o=d.addObject('PartDesign::Feature','RADOME_SEAM_'+v['view'].upper());o.Label=v['view']+' original seam PROJECTION / unverified metric frame';o.Shape=shape
 for name in ['MetricFrameVerified','SurfaceRailVerified','ProductionRelease']:
  o.addProperty('App::PropertyBool',name,'Evidence');setattr(o,name,False)
 rows.append(dict(view=v['view'],points=len(pts),native_edges=len(shape.Edges),valid=shape.isValid(),solids=len(shape.Solids),length_candidate_mm=shape.Length))
d.recompute();output=base/'F14_ORIGINAL_RADOME_SEAM_GUIDES.FCStd';d.saveAs(str(output));App.closeDocument(d.Name)
assert hashes=={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,frame]}
a=dict(status='NATIVE_ORIGINAL_RADOME_SEAM_PROJECTION_GUIDES_CREATED',inputs=hashes,rows=rows,output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),limitations=['Two independent projected curves; missing coordinate zero is projection only.','Historical metric candidate frame retained for study only.','Not a 3D seam, surface rail, constant FS station or registered assembly.'],current_master_modified=False,production_release=False)
(base/'freecad_original_radome_seam_guides_audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a))
