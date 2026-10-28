from pathlib import Path
import json,math,hashlib
O=Path(__file__).parent
source=O/'NASA_canopy_conic_constraint_v2_audit.json';raw=O/'SHIFARC_CSCALC_original_run.txt'
j=json.loads(source.read_text(encoding='utf-8'));text=raw.read_text(encoding='utf-8-sig');rows=[];seen=set()
assert 'NEGATIVE NUMBER' not in text
for line in text.splitlines():
 if not line.strip().startswith('RADIUS'):continue
 _,k,i,v=line.split();k=int(k);i=int(i);v=float(v)
 assert 1<=k<=10 and i in range(0,101,10) and (k,i) not in seen
 seen.add((k,i));arc=j['rows'][k-1];x=arc['x_source'];mapz=131.45+(x-93)*14.55/259
 y,z=arc['points_YZ_source'][i];expected=math.hypot(y,z-mapz)
 assert math.isfinite(v) and v>0
 rows.append(dict(arc_index=k,point_index=i,radius_original=v,radius_study=expected,error_source=abs(v-expected)))
assert seen=={(k,i) for k in range(1,11) for i in range(0,101,10)}
maximum=max(r['error_source'] for r in rows);assert maximum<2e-5
names=['NASA_canopy_conic_constraint_v2_audit.json','SHIFARC_CSCALC_original_run.txt','SHIFARC_CSCALC_review_only.for','SHIFARC_CSMCOE_review_only.for','SHIFARC_VDOTV_review_only.for','SHIFARC_MDOTV_review_only.for','run_SHIFARC_CSCALC_reference.f']
audit=dict(status='ORIGINAL_CSCALC_110_RADIEN_UNABHAENGIG_REPRODUZIERBAR_GEPRUEFT',sample_count=110,maximum_error_source=maximum,acceptance_threshold_source=2e-5,sha256={n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in names},rows=rows,compiler_requirement='gfortran -std=legacy -fno-automatic -ffixed-line-length-72; statische lokale Speicherung fuer Cache zwingend.',limits=['Hier werden gespeicherte Originalrohdaten unabhaengig nachgerechnet; keine erneute Kompilierung.','NDERV0, nurRadien; keine THELIM/CSMINT-Aussenhuellenwahl oder Ableitungspruefung.','Quelleneinheiten bleiben unskaliert; keine Herstellerhaut-/Produktionsfreigabe.'],production_release=False)
(O/'SHIFARC_canopy_radial_independent_verification.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8');print('110einmaligeProbenPASS,maxFehler',maximum)
