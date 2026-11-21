from pathlib import Path
import FreeCAD as App,json,hashlib
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();bridge=R/'migration/freecad/ROOTBRIDGE_UNFROZEN_PACKAGING_CONCEPT_ONLY.FCStd';spar=R/'migration/freecad/FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd';inputs={str(p):sha(p) for p in (bridge,spar)}
assert sha(bridge)==json.loads((R/'analysis/v192_rootbridge_concept_packaging.json').read_text())['concept_sha256'];assert sha(spar)==json.loads((R/'analysis/v192_fullspan_spar_reference_build.json').read_text())['output_sha256']
out=R/'analysis/v192_rootbridge_to_spar_interface.json';assert not out.exists();a=App.openDocument(str(bridge));b=App.openDocument(str(spar));rows=[]
try:
 objs=[o for o in a.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objs)==1;s=objs[0].Shape
 for o in b.Objects:
  if not hasattr(o,'Shape') or o.Shape.isNull():continue
  distance,points,info=s.distToShape(o.Shape);common=s.common(o.Shape)
  rows.append({'object':o.Name,'distance_to_rootbridge_mm':distance,'common_volume_mm3':common.Volume,'closest_point_pairs_mm':[[list(p),list(q)] for p,q in points]})
finally:App.closeDocument(b.Name);App.closeDocument(a.Name)
assert all(sha(Path(p))==h for p,h in inputs.items())
r={'status':'REFERENCE_ROOTBRIDGE_TO_CURRENT_SPAR_GEOMETRIC_INTERFACE_ONLY','input_sha256':inputs,'rows':rows,'limits':['Rootbridge remains rejected against incomplete body/glove envelope; generic bore and pivotZ0 are unfrozen','Contact/overlap alone does not transfer load or establish bearing/metal insert/bond geometry','No modifications, integration, material, structural or print release'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');print([(r['object'],r['distance_to_rootbridge_mm'],r['common_volume_mm3']) for r in rows])
