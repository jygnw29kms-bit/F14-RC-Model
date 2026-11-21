from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];names=['FLARED_ROOT_SOCKET_UNFROZEN_CONCEPT_ONLY.FCStd','CANTED_BEARING_ENVELOPES_UNSELECTED_ONLY.FCStd'];paths=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in paths];out=R/'analysis/v192_canted_rings_vs_old_socket.json';assert not out.exists();D=A.openDocument(str(paths[0]));socket=D.Objects[0].Shape.copy();A.closeDocument(D.Name);D=A.openDocument(str(paths[1]));rows=[]
try:
 for o in D.Objects:
  s=o.Shape;common=s.common(socket);outside=s.cut(socket);assert common.isValid() and outside.isValid();assert abs(common.Volume+outside.Volume-s.Volume)<1e-5;rows.append({'object':o.Name,'ring_volume_mm3':s.Volume,'overlap_old_socket_mm3':common.Volume,'outside_old_socket_mm3':outside.Volume,'geometrically_assembled_without_seat_cuts':common.Volume<1e-7})
finally:A.closeDocument(D.Name)
assert [H(p) for p in paths]==hs;out.write_text(json.dumps({'status':'OLD_SOCKET_INCOMPATIBLE_WITH_CANTED_RING_ENVELOPES','input_sha256_unchanged':dict(zip(names,hs)),'rows':rows,'interpretation':'Positive overlap requires seat/housing redesign; outside-socket material is not by itself outside-aircraft geometry','limits':['Generic envelope rings only, no bearing selection','No cut or modification to old socket; old external packaging rejection unchanged','No installed assembly, contact/retention/thrust path or material verification'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)
