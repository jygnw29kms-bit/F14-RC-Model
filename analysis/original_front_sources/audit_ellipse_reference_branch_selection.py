from pathlib import Path
import json, math, hashlib
from ellipse_reference_evaluator import EllipseReference
O=Path(__file__).parent
rows=[]
for direction in (1,-1):
 r=EllipseReference([0,0],[2,direction],[0,direction])
 errors=[]
 for i in range(101):
  x=2*i/100; expected=direction*math.sqrt(1-(x-2)**2/4)
  errors.append(abs(r.value(x)-expected))
 assert max(errors)<1e-12
 try:r.derivatives(0)
 except ValueError:pass
 else:raise AssertionError('Vertikale Tangente nicht erkannt')
 assert abs(r.derivatives(2)[0])<1e-12
 rows.append(dict(case='synthetische Viertellipse',direction=direction,selected_sign=r.sign,max_value_error=max(errors),vertical_start_rejected=True))
j=json.loads((O/'NASA_nose_bodyline_reference_study.json').read_text(encoding='utf-8'))
cases=json.loads((O/'ellipse_tangent_control_hypothesis.json').read_text(encoding='utf-8'))['cases']
for c, previous in zip(cases,j['curves']):
 assert c['name']==previous['name']
 r=EllipseReference(c['start'],c['end'],c['control'])
 delta=max(abs(r.value(x)-y) for x,y in previous['points_source'])
 assert delta<1e-12
 rows.append(dict(case=c['name'],max_difference_from_previous_study=delta))
m=math.tan(math.radians(10));r=EllipseReference([10,10*m],[15,2],[2/m,2])
assert abs(r.derivatives(15)[1]+.01295)<=.000005
report=dict(status='ZWEIGWAHL_REGRESSION_PASS',checks=rows,printed_fillet_reference_pass=True,evaluator_sha256=hashlib.sha256((O/'ellipse_reference_evaluator.py').read_bytes()).hexdigest(),limits=['Synthetische Zweigtests belegen Algebra, keine allgemeine WBPPW-ELLY-Semantik.','Historische Studien behalten ihre damaligen Eingabehashes; keine erneute native Ausfuehrung.','Kein physischer Massstab, keine Masteraenderung oder Produktionsfreigabe.'],production_release=False)
(O/'ellipse_reference_branch_selection_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True))
