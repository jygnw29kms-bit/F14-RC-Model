from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];names=['CANTED_HOUSING_SHOULDER_CONCEPT_ONLY.FCStd','F14_CURRENT_FULL_VIEW_v192.FCStd'];paths=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in paths];out=R/'analysis/v192_canted_housing_current_envelope_audit.json';assert not out.exists();D=A.openDocument(str(paths[0]));shapes=[(o.Name,o.Shape.copy()) for o in D.Objects];A.closeDocument(D.Name);D=A.openDocument(str(paths[1]));rows=[]
try:
 body=D.getObject('FUSELAGE_CURRENT').Shape;wing=D.getObject('WING_R').Shape
 for name,s in shapes:
  outside=s.cut(body).cut(wing);assert outside.isValid();rows.append({'object':name,'volume_mm3':s.Volume,'outside_current_body_or_wing_mm3':outside.Volume,'accepted_against_current_reference':outside.Volume<=1e-6})
finally:A.closeDocument(D.Name)
assert [H(p) for p in paths]==hs;out.write_text(json.dumps({'status':'CURRENT_ENVELOPE_CONTAINMENT_SCREEN_AT_BASELINE20_ONLY','input_sha256_unchanged':dict(zip(names,hs)),'rows':rows,'limits':['Current body/glove incomplete; rejection is against current CAD reference not original-aircraft proof','Provisional pivotZ0, generic unselected rings/housing','No exterior enlargement, relocation or master modification','No sweep, attachment, retention, tolerances, load rating or physical proof'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)
