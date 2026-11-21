from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1];p=R/'analysis/v192_partition_flux_reference_epsilon_geometric_seams.json';q=R/'analysis/v192_partition_all_faces_common_point_flux.json';d=json.loads(p.read_text());old=json.loads(q.read_text());assert len(d['runs'])==3
for n,h in d['input_sha256_unchanged'].items():assert hashlib.sha256((R/'migration/freecad'/n).read_bytes()).hexdigest()==h==old['input_sha256_unchanged'][n]
for run in d['runs']:
 assert [r['face_count'] for r in run['rows']]==[2285,1186,1200]
 for row in run['rows']:
  assert [s[0] for s in row['face_samples_index_flux_error']]==list(range(1,row['face_count']+1));assert math.fsum(s[1] for s in row['face_samples_index_flux_error'])==row['signed_flux_sum_mm3']
 assert len(run['seam_faces'])==2 and {s['face'] for s in run['seam_faces']}=={3,5};assert abs(math.fsum(s['signed_flux_mm3'] for s in run['seam_faces']))<1e-10
assert all(abs(run['part_sum_minus_source_mm3'])<1e-5 for run in d['runs'])
ref_change=[{'object':a['object'],'P700_300_0_minus_P700_280_0_at_eps1e11_mm3':a['signed_flux_sum_mm3']-b['signed_flux_sum_mm3']} for a,b in zip(old['rows'],d['runs'][1]['rows'])]
out=R/'analysis/v192_partition_flux_reference_epsilon_verification.json';assert not out.exists();out.write_text(json.dumps({'status':'THREE_BALANCES_AND_SEAM_CANCELLATION_VERIFIED_REFERENCE_SENSITIVITY_UNRESOLVED','evidence_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest(),q.name:hashlib.sha256(q.read_bytes()).hexdigest()},'residuals_mm3':[run['part_sum_minus_source_mm3'] for run in d['runs']],'reference_point_absolute_volume_changes':ref_change,'limits':['Each numeric balance is within1e-5 but individual volumes change by more than this guard with reference point','Correlated integration errors can cancel in balance; no rigorous volume certification','Seam face indexing corrected by geometric selection before verification; earlier zero-based audit indices must not be reused as one-based','No geometry/tolerance modification or print/flight release'],'print_release':False,'flight_release':False},indent=2)+'\n');print(ref_change)
