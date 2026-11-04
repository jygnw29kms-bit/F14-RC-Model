from pathlib import Path
import json, math, hashlib
from ellipse_reference_evaluator import EllipseReference
O=Path(__file__).parent;src=O/'ellipse_tangent_control_hypothesis.json'
j=json.loads(src.read_text(encoding='utf-8'));c={x['name']:EllipseReference(x['start'],x['end'],x['control']) for x in j['cases']}
x0=93.;top=c['ZTCL_nose'];bottom=c['ZBCL_nose'];width=c['YMHB_nose']
assert abs(width.value(x0))<1e-12 and abs(top.value(x0)-bottom.value(x0))<1e-12
st=top.derivatives(x0)[0];sb=bottom.derivatives(x0)[0];sw=width.derivatives(x0)[0]
sm=(138-131.45)/(164-93)
assert st>sm>sb and sw>0
limit=math.pi/4*sw*(st-sb);rows=[]
for dx in [1.,.1,.01,.001]:
 x=x0+dx;w=width.value(x);t=top.value(x);b=bottom.value(x);mid=131.45+sm*dx
 assert b<mid<t and w>0
 area=math.pi/4*w*(t-b)
 rows.append(dict(dx_source=dx,halfwidth_source=w,half_area_source2=area,area_divided_by_dx2=area/(dx*dx),relative_difference_from_leading_limit=abs(area/(dx*dx)-limit)/limit))
assert rows[-1]['relative_difference_from_leading_limit']<rows[0]['relative_difference_from_leading_limit']
r=dict(status='NASENSPITZE_DEGENERIERT_ZU_EINEM_PUNKT',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),evaluator_sha256=hashlib.sha256((O/'ellipse_reference_evaluator.py').read_bytes()).hexdigest(),apex_source=[93,0,131.45],endpoint_slopes_source=dict(top=st,bottom=sb,halfwidth=sw,midline=sm),leading_half_area_coefficient=limit,samples=rows,construction_implications=['Bei X=93 sind Breite und beide Viertellipsenhoehen null: keine regulaere Ellipsensektion.','Der Spitzenabschluss braucht eine explizite Punkt-/Polbehandlung; keine erfundene endliche Startsektion.','Endliche nichtgleiche Randsteigungen ergeben in dieser Studie einen spitzen lokalen Abschluss; keine belegte abgerundete Herstellernase.'],limits=['Analytische Eigenschaften des teilverifizierten Studienmodells, kein Originalroutine-/Herstellerhautnachweis.','Keine native Flaeche, kein Loft oder Export ausgefuehrt.','Physische Einheiten, UPC-Registrierung und Produktionsfreigabe bleiben offen.'],production_release=False)
(O/'NASA_nose_apex_degeneracy_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r,ensure_ascii=True))
