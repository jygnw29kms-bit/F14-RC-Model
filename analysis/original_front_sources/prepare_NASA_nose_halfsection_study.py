"""Quelleneinheitenstudie: zwei Viertellipsen aus gebundenen Nasenkontrollpunkten."""
from pathlib import Path
import json,math,hashlib
from ellipse_reference_evaluator import EllipseReference
O=Path(__file__).parent;j=json.loads((O/'ellipse_tangent_control_hypothesis.json').read_text(encoding='utf-8'));curves={c['name']:EllipseReference(c['start'],c['end'],c['control']) for c in j['cases']};rows=[]
for x in [110,125,150,175,200]:
 top=curves['ZTCL_nose'].value(x);bottom=curves['ZBCL_nose'].value(x) if x<=176 else 116.5+(x-176)*(118-116.5)/(205-176);width=curves['YMHB_nose'].value(x);mid=131.45+(x-93)*(138-131.45)/(164-93) if x<=164 else 138+(x-164)*.5/(205-164);assert bottom<mid<top and width>0
 lower=[[width*math.sin(i*math.pi/160),mid-(mid-bottom)*math.cos(i*math.pi/160)] for i in range(81)];upper=[[width*math.cos(i*math.pi/160),mid+(top-mid)*math.sin(i*math.pi/160)] for i in range(1,81)];pts=lower+upper
 for y,z in lower:assert abs((y/width)**2+((z-mid)/(mid-bottom))**2-1)<1e-12
 for y,z in upper:assert abs((y/width)**2+((z-mid)/(top-mid))**2-1)<1e-12
 area=abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(pts,pts[1:]+pts[:1])))/2;exact=math.pi/4*width*(top-bottom);assert abs(area-exact)/exact<1e-4
 rows.append(dict(x_source=x,control_coordinates={'BCL':[0,bottom],'MHB':[width,mid],'TCL':[0,top],'SCPLO':[width,bottom],'SCPUP':[width,top]},points_YZ_source=pts,half_area_analytic_source2=exact,half_area_polygon_source2=area,relative_polygon_area_error=abs(area-exact)/exact,quarter_ellipse_normal_forms_verified=True,join_tangents='AmMHBbeidevertikal;EndenamY0horizontal.'))
r=dict(status='FUENF_LOKALE_NASENHALBSEKTIONEN_NUR_STUDIE_VORBEREITET',binding_sha256=hashlib.sha256((O/'NASA_nose_control_point_bindings.json').read_bytes()).hexdigest(),rows=rows,limits=['ELLIinterpretiertalsachsenparalleleViertellipsenmitTangentenkontrollpunkten; keinOriginalroutinevollnachweis.','BodylineEvaluatorteilverifiziert; Quellenrumpfvereinfacht,keineHerstellerhaut.','Quelleneinheitenunveraendert; keinemmUmrechnung/UPCRegistrierung.','NurHalbsektionen,keineSpiegelung,keineLoft-/Volumen-/Produktionsfreigabe.'],production_release=False)
(O/'NASA_nose_halfsection_reference_study.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(v['x_source'],v['half_area_analytic_source2'],v['relative_polygon_area_error']) for v in rows])
