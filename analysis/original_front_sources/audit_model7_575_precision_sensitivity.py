from pathlib import Path
import json,math,re,numpy as np,subprocess,tempfile,hashlib
O=Path(__file__).parent
compiler=r'C:/Users/dezen/AppData/Local/PRINTBENCH/toolchain/strawberry-perl-5.42.3.1/c/bin/gfortran.exe'
names=['SHIFARC_CSMCOE_review_only.for','SHIFARC_CSCALC_review_only.for','SHIFARC_VDOTV_review_only.for','SHIFARC_MDOTV_review_only.for','run_SHIFARC_model7_575_radial.f']
exe=Path(tempfile.gettempdir())/'f14_model7_575_real8_experiment.exe'
flags=['-std=legacy','-fno-automatic','-ffixed-line-length-72','-fdefault-real-8']
subprocess.run([compiler,*flags,*[str(O/n) for n in names],'-o',str(exe)],check=True,capture_output=True)
run=subprocess.run([str(exe)],check=True,capture_output=True,text=True)
(O/'SHIFARC_model7_575_real8_experiment_raw.txt').write_text(run.stdout,encoding='utf-8')
j=json.loads((O/'NASA_models6_7_halfsection_failure.json').read_text(encoding='utf-8'));p0=j['start'];p1=j['end'];pc=j['control'];y,z=np.subtract(p1,p0);u,v=np.subtract(pc,p0);ty,tz=np.subtract(pc,p1)
M=np.array([[0,0,0,0,1],[y*y,z*z,y,z,1],[0,0,u,v,0],[2*y*ty,2*z*tz,ty,tz,0]],float);a,b,c,d,e=np.linalg.svd(M)[2][-1];zm=146+223/428
angles=[float(v) for v in re.findall(r'^ +h=([0-9.]+)',(O/names[-1]).read_text(),re.M)];assert len(angles)==101
expected=[]
for h in angles:
 ch,sh=math.cos(h),math.sin(h);dz=zm-p0[1];qa=a*ch*ch+b*sh*sh;qb=-2*a*p0[0]*ch+2*b*dz*sh+c*ch+d*sh;qc=a*p0[0]**2+b*dz*dz-c*p0[0]+d*dz+e;disc=qb*qb-4*qa*qc;assert disc>0
 roots=[(-qb+sg*math.sqrt(disc))/(2*qa) for sg in [-1,1]];expected.append(min(r for r in roots if r>0))
def errors(text):
 lines=[l.split() for l in text.splitlines() if l.strip().startswith('CHECK')];assert len(lines)==101
 return [abs(float(v)-r) for (_,i,v),r in zip(lines,expected)]
base=errors((O/'SHIFARC_model7_575_radial_raw.txt').read_text(encoding='utf-8'));double=errors(run.stdout)
assert max(base)>2e-4 and max(double)<2e-4
r=dict(status='PRAEZISIONS_SENSITIVITAETSEXPERIMENT_AUSGEFUEHRT',samples=101,baseline_max_error_source=max(base),promoted_real8_max_error_source=max(double),real8_experiment_flags=flags,source_files_unchanged_sha256={n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in names},limits=['REAL8 ist explizites Praezisionsexperiment, kein unveraenderter historischer Singleprecision-Lauf.','Starker Fehlerrueckgang stuetzt Rundung/Kondition als Ursache; ersetzt keine globale Routinenfreigabe.','Zweigwahl beschraenkte kleinepositiveWurzel; keineglobaleWurzeleindeutigkeit.','Keine CAD-/Master- oder Produktionsfreigabe.'],production_release=False)
(O/'SHIFARC_model7_575_precision_sensitivity.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(max(base),max(double))
