from pathlib import Path
import json,hashlib
from quick_elly_bodyline_reference import QuickEllyBodylineReference
O=Path(__file__).parent;r=QuickEllyBodylineReference([313,203],[352,199.5],[331,203]);errors=[]
for line in (O/'SHIFARC_ELLY_original_run.txt').read_text(encoding='utf-8-sig').splitlines()[1:]:
 i,u,v,t,s=map(float,line.split());x=313+u;first,second=r.derivatives(x)
 errors.append([abs(r.value(x)-203-v),abs(first-t),abs(second-s)])
maximum=[max(v[i] for v in errors) for i in range(3)]
assert len(errors)==101 and maximum[0]<3e-7 and maximum[1]<2e-8 and maximum[2]<1e-9
for x in [312.999,352.001]:
 try:r.value(x)
 except ValueError:pass
 else:raise AssertionError('Extrapolation nicht gesperrt')
audit=dict(status='GETRENNTER_ELLY_BODYLINE_EVALUATOR_ORIGINALVERGLEICH_PASS',sample_count=len(errors),coefficients=dict(A=r.A,B=r.B,C=r.C),max_error_vs_executed_historical_routine=dict(value=maximum[0],first_derivative=maximum[1],second_derivative=maximum[2]),inputs_sha256={n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in ['quick_elly_bodyline_reference.py','SHIFARC_ELLY_original_run.txt']},limits=['Ein ausgefuehrter Originalvergleichsfall; keine allgemeine WBPPW-Versionsfreigabe.','Historische Parabelfallbacks und Ableitungs-Clamping bewusst nicht implementiert; entsprechende Faelle werden abgelehnt.','ELLI-Querschnitte unveraendert; keine CAD-/Master- oder Produktionsfreigabe.'],production_release=False)
(O/'quick_elly_bodyline_reference_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8');print(maximum)
