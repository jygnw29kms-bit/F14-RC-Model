from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/Y300_SKIN_BOND_VERTICAL_RECESS_STUDY_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);out=R/'analysis/v192_y300_recessed_sleeve_bond_contacts.json';assert not out.exists();prior=json.loads((R/'analysis/v192_y300_sleeve_bond_geometry_audit.json').read_text());D=A.openDocument(str(p));rows=[]
try:
 sleeve=D.getObject('GENERIC_4OD_2p2ID_SLEEVE').Shape
 for i,name in enumerate(('ROOT_CARRIER','TIP_CARRIER')):
  bond=D.getObject('GEOMETRIC_BOND_'+str(i)).Shape;carrier=D.getObject(name).Shape;contacts=[]
  for target,s in [(name,carrier),('SLEEVE',sleeve)]:
   area=sum(f.common(g).Area for f in bond.Faces for g in s.Faces);expected=prior['rows'][i]['contacts'][0 if target==name else 1]['common_face_area_mm2'];contacts.append({'target':target,'area_mm2':area,'prior_area_mm2':expected,'difference_mm2':area-expected,'overlap_mm3':bond.common(s).Volume})
  rows.append({'bond_index':i,'contacts':contacts})
finally:A.closeDocument(D.Name)
assert H(p)==h;out.write_text(json.dumps({'status':'RECESSED_CARRIER_SLEEVE_BOND_CONTACTS_REMEASURED','input_sha256_unchanged':h,'rows':rows,'limits':['Face-area changes after skin recess must be retained, not assumed identical','No adhesive strength, cure, manufacturing tolerance or assembly proof','Source partition remains volume-blocked; no print or flight acceptance'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)
