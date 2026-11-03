from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[1];p=R/'analysis/v192_partition_all_faces_common_point_flux.json';q=R/'analysis/v192_partition_volume_common_translation_diagnostic.json';d=json.loads(p.read_text());g=json.loads(q.read_text());assert d['status']=='ALL_FACES_COMMON_POINT_TRIMMED_FLUX_MEASURED';assert [r['face_count'] for r in d['rows']]==[2285,1186,1200]
for r in d['rows']:
 assert len(r['faces'])==r['face_count'] and [f['face'] for f in r['faces']]==list(range(1,r['face_count']+1))
 assert math.fsum(f['signed_flux_mm3'] for f in r['faces'])==r['signed_flux_sum_mm3']
for n,h in d['input_sha256_unchanged'].items():assert hashlib.sha256((R/'migration/freecad'/n).read_bytes()).hexdigest()==h and g['input_sha256_unchanged'][n]==h
residual=math.fsum(r['signed_flux_sum_mm3'] for r in d['rows'][1:])-d['rows'][0]['signed_flux_sum_mm3'];assert residual==d['part_sum_minus_source_mm3'];comparisons=[]
for r,old in zip(d['rows'],g['rows'][0]['measurements']):
 assert r['object']==old['object'];comparisons.append({'object':r['object'],'face_sum_minus_whole_shape_GK_mm3':r['signed_flux_sum_mm3']-old['GK_volume_mm3']})
out=R/'analysis/v192_partition_common_point_flux_verification.json';assert not out.exists();out.write_text(json.dumps({'status':'FACE_COMPLETENESS_HASHES_SUMS_VERIFIED_NUMERIC_BALANCE_ONLY','evidence_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest(),q.name:hashlib.sha256(q.read_bytes()).hexdigest()},'total_face_count':sum(r['face_count'] for r in d['rows']),'common_point_face_sum_balance_residual_mm3':residual,'strict_numeric_balance_guard_mm3':1e-5,'this_numeric_balance_within_guard':abs(residual)<1e-5,'comparisons':comparisons,'limits':['This one diagnostic numeric balance is within guard, not accepted partition volume certification','Absolute source/part results differ from whole-shape GK; integration discrepancy unresolved','Need independent reference-point/epsilon consistency and seam orientation audit','No rigorous integration bounds, exact geometry identity, print or flight release'],'print_release':False,'flight_release':False},indent=2)+'\n');print(residual,comparisons)
