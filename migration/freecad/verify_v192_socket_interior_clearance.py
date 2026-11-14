from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();socket=R/'migration/freecad/FLARED_ROOT_SOCKET_UNFROZEN_CONCEPT_ONLY.FCStd';spar=R/'migration/freecad/FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd';prior=json.loads((R/'analysis/v192_flared_root_socket_trial.json').read_text());assert sha(socket)==prior['output_sha256'];before={str(p):sha(p) for p in (socket,spar)}
out=R/'analysis/v192_socket_reopen_interior_clearance.json';assert not out.exists();a=App.openDocument(str(socket));b=App.openDocument(str(spar));rows=[]
try:
 objs=[o for o in a.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objs)==1;s=objs[0].Shape;assert s.isValid() and len(s.Solids)==1
 clip=Part.makeBox(2000,24,2000,App.Vector(-1000,150,-1000))
 for o in b.Objects:
  if not hasattr(o,'Shape') or o.Shape.isNull():continue
  trimmed=o.Shape.common(clip);assert trimmed.isValid() and len(trimmed.Solids)==1;dist,pts,info=s.distToShape(trimmed);overlap=s.common(trimmed).Volume
  full_dist,full_pts,_=s.distToShape(o.Shape)
  rows.append({'object':o.Name,'clipped_y_interval_mm':[150,174],'trimmed_volume_mm3':trimmed.Volume,'distance_to_socket_mm':dist,'overlap_volume_mm3':overlap,'closest_point_pairs_mm':[[list(p),list(q)] for p,q in pts],'full_object_distance_mm':full_dist,'full_object_closest_point_pairs_mm':[[list(p),list(q)] for p,q in full_pts]})
finally:App.closeDocument(b.Name);App.closeDocument(a.Name)
assert all(sha(Path(p))==h for p,h in before.items())
r={'status':'SOCKET_REOPEN_AND_TRIMMED_INTERIOR_CLEARANCE_ONLY','input_sha256':before,'socket_valid':True,'socket_solids':1,'socket_volume_mm3':s.Volume,'rows':rows,'limits':['Trim excludesY149 stop andY175 open end: positive interior clearance cannot certify full assembly insertion','Trim is diagnostic only, no production geometry modified','0.15 coordinate offsets not qualified print or bond tolerances','Original baseline exterior packaging remains rejected, pivotZ/axis/hardware unfrozen','No root load transfer, strength, contact-pressure or physical test release'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');print([(r['object'],r['distance_to_socket_mm'],r['overlap_volume_mm3']) for r in rows])
