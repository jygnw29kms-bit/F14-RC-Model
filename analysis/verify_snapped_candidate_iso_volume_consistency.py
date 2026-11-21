from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1];p=R/'analysis/v192_snapped_candidate_surface_iso_Green_sections.json';q=R/'analysis/v192_segment5_snapped_candidate_validation.json';d=json.loads(p.read_text());v=json.loads(q.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();cad=R/'migration/freecad/VOID_SEGMENT5_SNAPPED_ENDPOINT_STUDY_ONLY.FCStd';assert H(cad)==d['input_sha256_unchanged']==v['input_sha256_unchanged'][cad.name];assert len(d['rows'])==5 and d['side_surface_count']==98
for row in d['rows']:
 assert row['edge_count']==98 and len(row['samples'])==4
 assert all(s['max_ordered_curve_endpoint_gap_mm']==0 and s['hypothetical_line_connector_signed_area_mm2']==0 for s in row['samples'])
 assert max(s['raw_absolute_area_mm2'] for s in row['samples'])-min(s['raw_absolute_area_mm2'] for s in row['samples'])<1e-8
areas=[row['samples'][-1]['raw_absolute_area_mm2'] for row in d['rows']];lo,mid,hi=areas[0],areas[2],areas[4]
def fit(t):return lo*2*(t-.5)*(t-1)-mid*4*t*(t-1)+hi*2*t*(t-.5)
res=[areas[i]-fit(d['rows'][i]['fraction']) for i in range(5)];assert max(abs(x) for x in res)<1e-8
volumes={'default':v['default_volume_mm3'],'GK':v['GK_volume_mm3'],'iso_Green_prismoid':d['single_prismoid_volume_mm3'],'iso_Green_composite':d['composite_simpson_volume_mm3']};spread=max(volumes.values())-min(volumes.values());assert spread<1e-8
out=R/'analysis/v192_snapped_candidate_iso_volume_consistency_verification.json';assert not out.exists();out.write_text(json.dumps({'status':'ISOLATED_CANDIDATE_FIVE_SECTION_QUADRATIC_AND_VOLUME_CONSISTENCY_VERIFIED','evidence_sha256':{p.name:H(p),q.name:H(q)},'candidate_sha256':H(cad),'section_area_quadratic_residuals_mm2':res,'volume_diagnostics_mm3':volumes,'numeric_volume_spread_mm3':spread,'limits':['Numerical consistency only for one intentionally modified segment; no rigorous error enclosure','Native Slice area diagnostics were inconsistent; this diagnostic uses direct ruled-surface isocurves','Candidate increased stored tolerances/curve-surface deviations and whole original-shape deviation remain separate open checks','Original cavity, original split volume gate and full aircraft remain unaccepted'],'print_release':False,'flight_release':False},indent=2)+'\n');print('Four volume diagnostics spread',spread,'section residuals',res)
