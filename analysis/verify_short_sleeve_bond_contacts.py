from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1];p=R/'analysis/v192_short_sleeve_bond_contact_measurement.json';q=R/'analysis/v192_short_sleeve_analytic_area_trade.json'
d=json.loads(p.read_text());a=json.loads(q.read_text());cad=R/'migration/freecad/Y300_SHORT_SLEEVE_ASSEMBLY_TRADE_STUDY_ONLY.FCStd'
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert d['status']=='SHORT_SLEEVE_CONTACT_AREAS_MEASURED' and d['input_sha256_unchanged']==H(cad)
assert len(d['rows'])==2
checks=[]
for row in d['rows']:
 assert len(row['contacts'])==2
 for c in row['contacts']:
  radius=2.0 if c['target']=='SLEEVE' else 2.1
  expected=next(r for r in a['rows'] if r['nominal_radius_mm']==radius)
  residual=c['area_mm2']-expected['short_analytic_area_mm2']
  assert abs(residual)<1e-6 and abs(c['overlap_mm3'])<1e-7
  assert abs(c['scalar_F_over_A_MPa_per_N']*c['area_mm2']-1)<1e-12
  checks.append({'bond_index':row['bond_index'],'target':c['target'],'area_residual_mm2':residual})
out=R/'analysis/v192_short_sleeve_bond_contact_verification.json';assert not out.exists()
out.write_text(json.dumps({'status':'FOUR_NATIVE_SHORT_CONTACTS_MATCH_INDEPENDENT_ANALYTIC_AREAS','evidence_sha256':{p.name:H(p),q.name:H(q)},'cad_sha256':H(cad),'checks':checks,'limits':['Contact geometry only, not adhesive or joint strength acceptance','No assigned load, physical assembly, tooling, tolerance or cure validation','Partition volume balance and full aircraft checks remain open'],'print_release':False,'flight_release':False},indent=2)+'\n');print('Four short sleeve contacts independently verified')
