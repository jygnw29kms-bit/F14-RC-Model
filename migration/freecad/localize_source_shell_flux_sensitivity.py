from pathlib import Path
import FreeCAD as A,json,hashlib,math
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);q=R/'analysis/v192_partition_common_point_gauss_flux.json';d=json.loads(q.read_text());assert d['input_sha256_unchanged'][p.name]==h;out=R/'analysis/v192_source_shell_flux_sensitivity.json';assert not out.exists();D=A.openDocument(str(p));s=D.Objects[0].Shape.copy();A.closeDocument(D.Name);lookup={}
for i,f in enumerate(s.Faces,1):lookup.setdefault(f.hashCode(),[]).append((i,f))
rows=[];all_indices=[]
for k,shell in enumerate(s.Shells):
 indices=[]
 for f in shell.Faces:
  matches=[i for i,g in lookup[f.hashCode()] if f.isSame(g)];assert len(matches)==1;indices.append(matches[0])
 all_indices.extend(indices);samples=[]
 for run in d['runs'][1:]:
  values=run['rows'][0]['face_samples_index_flux_error'];samples.append({'reference_point_mm':run['reference_point_mm'],'signed_flux_sum_mm3':math.fsum(values[i-1][1] for i in indices)})
 rows.append({'shell_index_zero_based':k,'face_count':len(indices),'face_indices_one_based':indices,'native_is_closed':shell.isClosed(),'native_area_mm2':shell.Area,'samples':samples,'P300_minus_P280_signed_flux_mm3':samples[1]['signed_flux_sum_mm3']-samples[0]['signed_flux_sum_mm3']})
assert sorted(all_indices)==list(range(1,len(s.Faces)+1)) and len(all_indices)==len(set(all_indices));assert H(p)==h
out.write_text(json.dumps({'status':'SOURCE_FACE_FLUX_REFERENCE_SENSITIVITY_LOCALIZED_BY_SHELL','input_sha256_unchanged':h,'flux_report_sha256':H(q),'rows':rows,'limits':['Membership matched by native identity, not assumed geometric name','Topology closed flag does not establish exact trimmed-surface closure or volume accuracy','Reuses numerical face fluxes; not new physical volume or error bound','No geometry/tolerance modification or release'],'print_release':False,'flight_release':False},indent=2)+'\n');print([(r['shell_index_zero_based'],r['face_count'],r['samples'],r['P300_minus_P280_signed_flux_mm3']) for r in rows])
