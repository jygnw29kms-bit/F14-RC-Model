from pathlib import Path
import json,hashlib,itertools
R=Path(__file__).resolve().parents[1];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'analysis/v192_short_sleeve_36_pair_path_scope_verification.json';q=R/'analysis/v192_short_sleeve_root_skin_path_bounds.json'
a=json.loads(p.read_text());b=json.loads(q.read_text());assert a['pair_count']==36 and b['all_pairs_covered']
for n,h in a['evidence_report_sha256'].items():assert H(R/'analysis'/n)==h
for n,h in b['input_sha256_unchanged'].items():assert a['input_cad_sha256'][n]==h
for n,h in a['input_cad_sha256'].items():assert H(R/'migration/freecad'/n)==h
assert b['translation_global_y_mm']==a['translation_global_y_mm']==[0,5]
pairs={(r['moving'],r['fixed']) for r in a['pairs']};assert len(pairs)==36
for row in b['rows']:
 assert row['covered'] and row['fixed']=='ROOT_SKIN'
 if row['moving']=='TIP_SKIN':
  assert max(abs(row[k]) for k in ['root_outside_Y_le300_mm3','tip_outside_Y_ge300_mm3','initial_common_mm3'])<1e-7
 else:assert row['gap_lower_bound_mm']>1e-6
 assert (row['moving'],row['fixed']) not in pairs;pairs.add((row['moving'],row['fixed']))
fixed=a['fixed_objects']+['ROOT_SKIN'];assert pairs==set(itertools.product(a['moving_objects'],fixed)) and len(pairs)==40
out=R/'analysis/v192_short_sleeve_40_pair_path_scope_verification.json';assert not out.exists()
out.write_text(json.dumps({'status':'DECLARED_40_PAIR_RIGID_PATH_SCOPE_AND_HASH_LINKS_VERIFIED','translation_global_y_mm':[0,5],'input_cad_sha256':a['input_cad_sha256'],'evidence_report_sha256':{p.name:H(p),q.name:H(q)},'moving_objects':a['moving_objects'],'fixed_objects':fixed,'pair_count':40,'limits':['Native numerical distance, bounds and volume assumptions; contact allowed, no exact arithmetic certificate','Only listed local wing assembly objects; aircraft body, other mechanisms, access and tools omitted','Rigid adhesive placeholders; no material, strength, cure, fit or physical assembly acceptance','Source partition volume gate blocked; short sleeve bond area unqualified; no master promotion'],'print_release':False,'flight_release':False},indent=2)+'\n');print('Verified declared 40 pair scope')
