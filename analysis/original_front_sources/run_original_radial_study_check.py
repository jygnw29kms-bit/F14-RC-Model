"""Isolierter Originalroutinenvergleich fuer vorbereitete Querschnittsstudien."""
from pathlib import Path
import json,math,re,subprocess,hashlib,tempfile,sys
O=Path(__file__).parent
study=O/sys.argv[1];prefix=sys.argv[2]
j=json.loads(study.read_text(encoding='utf-8'));topologies=json.loads((O/'NASA_all_section_model_topologies.json').read_text(encoding='utf-8'))['models']
old=(O/'run_SHIFARC_CSCALC_reference.f').read_text(encoding='utf-8');head=old[:re.search(r'(?m)^ +cp=0\.',old).start()];calls=[];expected=[]
for row in j['rows']:
 controls=row['controls'];x=row['x_source'];zm=row['mapaxis_Z_source'];offset=0;top=topologies[row['model']-1]['arcs']
 for k,a in enumerate(top,1):
  elliptic=a['shape']=='ELLI';size=101 if elliptic else 2;pts=row['points_YZ_source'][offset:offset+size];offset+=size-1
  assert len(pts)==size
  p0,p1=controls[a['start']],controls[a['end']];pc=controls[a['slope_control']] if elliptic else p0
  assert math.dist(pts[0],p0)<1e-9 and math.dist(pts[-1],p1)<1e-9
  calls.append('      cp=0.\n')
  for col,point in [(1,p0),(7,p1),(13,pc),(19,pc if elliptic else p1)]:
   calls.append(f'      cp({k},{col})={point[0]:.12f}\n      cp({k},{col+3})={point[1]-zm:.12f}\n')
  shape=3 if elliptic else 1;calls.append(f'      call csmcoe({k},{shape},1,0)\n      icsash({k},1)={shape}\n')
  for i in (range(0,101,10) if elliptic else range(2)):
   y,z=pts[i];h=math.atan2(z-zm,y);serial=len(expected)+1
   calls.append(f"      h={h:.12f}\n      call cscalc({x:.8f},1,{k},h,r,rx,rh,rxx,rxh,0)\n      write(*,*) 'CHECK',{serial},r\n")
   expected.append(dict(index=serial,model=row['model'],x_source=x,arc=a['name'],radius_source=math.hypot(y,z-zm)))
  assert len(expected)>0
 assert offset==len(row['points_YZ_source'])-1
f=O/(prefix+'_driver.f');f.write_text(head+''.join(calls)+'      end\n',encoding='utf-8')
compiler=Path(r'C:/Users/dezen/AppData/Local/PRINTBENCH/toolchain/strawberry-perl-5.42.3.1/c/bin/gfortran.exe');exe=Path(tempfile.gettempdir())/(prefix+'.exe')
names=['SHIFARC_CSMCOE_review_only.for','SHIFARC_CSCALC_review_only.for','SHIFARC_VDOTV_review_only.for','SHIFARC_MDOTV_review_only.for']
cmd=[str(compiler),'-std=legacy','-fno-automatic','-ffixed-line-length-72']+[str(O/n) for n in names]+[str(f),'-o',str(exe)]
subprocess.run(cmd,check=True,capture_output=True,text=True)
result=subprocess.run([str(exe)],check=True,capture_output=True,text=True)
raw=O/(prefix+'_raw.txt');raw.write_text(result.stdout,encoding='utf-8');assert 'NEGATIVE NUMBER' not in result.stdout
values=[l.split() for l in result.stdout.splitlines() if l.strip().startswith('CHECK')];assert len(values)==len(expected)
for (_,idx,value),e in zip(values,expected):
 assert int(idx)==e['index'];e['radius_original']=float(value);e['error_source']=abs(float(value)-e['radius_source']);assert math.isfinite(e['error_source'])
maximum=max(e['error_source'] for e in expected);assert maximum<2e-4
report=dict(status='ORIGINALRADIEN_VERGLEICH_PASS',samples=len(expected),maximum_error_source=maximum,acceptance_threshold_source=2e-4,rows=expected,input_sha256={n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in names+[study.name,f.name,raw.name]},limits=['NDERV0: nurRadien, keineTHELIM/CSMINTGesamtauswertung.','HistorischeVersion, keinephysischeEinheiten-/Herstellerhaut-/Produktionsfreigabe.'],production_release=False)
(O/(prefix+'_audit.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(len(expected),maximum)
