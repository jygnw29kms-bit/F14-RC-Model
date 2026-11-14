from pathlib import Path
import FreeCAD as A,json,hashlib,math
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/Y300_SHORT_SLEEVE_ASSEMBLY_TRADE_STUDY_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);out=R/'analysis/v192_short_sleeve_bond_contact_measurement.json';assert not out.exists();D=A.openDocument(str(p));rows=[]
try:
 sleeve=D.getObject('GENERIC_4OD_2p2ID_SLEEVE').Shape
 for i,name in enumerate(('ROOT_CARRIER','TIP_CARRIER')):
  bond=D.getObject('GEOMETRIC_BOND_'+str(i)).Shape;carrier=D.getObject(name).Shape;contacts=[]
  for target,s,r in [(name,carrier,2.1),('SLEEVE',sleeve,2.0)]:
   area=sum(f.common(g).Area for f in bond.Faces for g in s.Faces);expected=2*math.pi*r*3.8;overlap=bond.common(s).Volume
   contacts.append({'target':target,'area_mm2':area,'analytic_cylinder_area_mm2':expected,'difference_mm2':area-expected,'overlap_mm3':overlap,'analytic_match':abs(area-expected)<1e-6,'scalar_F_over_A_MPa_per_N':1/area})
  rows.append({'bond_index':i,'contacts':contacts})
finally:A.closeDocument(D.Name)
assert H(p)==h;out.write_text(json.dumps({'status':'SHORT_SLEEVE_CONTACT_AREAS_MEASURED','input_sha256_unchanged':h,'rows':rows,'limits':['F/A per1N bookkeeping only; no assigned load, curved traction distribution, peel or strength analysis','Serial interface areas cannot be added for capacity','Short sleeve is permanent bridge if bonded both sides; no adhesive process or physical assembly acceptance','Partition volume and full aircraft gates remain open'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)
