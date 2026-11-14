from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1];p=R/'analysis/v192_partition_common_point_gauss_flux.json';q=R/'analysis/v192_partition_flux_reference_epsilon_geometric_seams.json';t=R/'analysis/v192_partition_all_faces_common_point_flux.json';d=json.loads(p.read_text());g=json.loads(q.read_text());old=json.loads(t.read_text());assert d['status']=='COMMON_POINT_ADAPTIVE_GAUSS_FLUX_MEASURED'
for n,h in d['input_sha256_unchanged'].items():assert hashlib.sha256((R/'migration/freecad'/n).read_bytes()).hexdigest()==h==g['input_sha256_unchanged'][n]
for run in d['runs']:
 assert [r['face_count'] for r in run['rows']]==[2285,1186,1200]
 for row in run['rows']:
  samples=row['face_samples_index_flux_error'];assert len(samples)==row['face_count'];assert [s[0] for s in samples]==list(range(1,row['face_count']+1));assert math.fsum(s[1] for s in samples)==row['signed_flux_sum_mm3']
comparisons=[]
for gauss,gk in [(d['runs'][1],g['runs'][1]),(d['runs'][2],{'rows':old['rows']})]:
 comparisons.append({'reference_point_mm':gauss['reference_point_mm'],'gauss_minus_GK_by_object_mm3':[{ 'object':a['object'],'difference':a['signed_flux_sum_mm3']-b['signed_flux_sum_mm3']} for a,b in zip(gauss['rows'],gk['rows'])]})
out=R/'analysis/v192_partition_gauss_GK_comparison.json';assert not out.exists();out.write_text(json.dumps({'status':'GAUSS_COMPLETENESS_AND_HIGH_PRECISION_METHOD_COMPARISON_VERIFIED','evidence_sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [p,q,t]},'gauss_balance_residuals_mm3':[run['part_sum_minus_source_mm3'] for run in d['runs']],'comparisons':comparisons,'gauss_reference_point_changes_at1e11_mm3':[a['signed_flux_sum_mm3']-b['signed_flux_sum_mm3'] for a,b in zip(d['runs'][2]['rows'],d['runs'][1]['rows'])],'limits':['High precision Gauss and GK agree locally but both retain reference-point sensitivity of individual volumes','Shared geometry/integration infrastructure prevents treating agreement as independent exact proof','No numerical guard relaxation or print/flight acceptance'],'print_release':False,'flight_release':False},indent=2)+'\n');print(comparisons)

