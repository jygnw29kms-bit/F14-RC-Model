from pathlib import Path
import json, hashlib, math
O=Path(__file__).parent
src=O/'NASA_nose_halfsection_reference_study.json'
j=json.loads(src.read_text(encoding='utf-8'));rows=[]
for row in j['rows']:
 c=row['control_coordinates'];w,mid=c['MHB'];lo=mid-c['BCL'][1];hi=c['TCL'][1]-mid
 assert min(w,lo,hi)>0
 # Analytische Ableitungen beider Parametrisierungen am MHB:
 # unten: (0,lo), oben: (0,hi). Gleiche normierte Tangente,
 # unterschiedliche Geschwindigkeit und im Allgemeinen Kruemmung.
 k_lower=w/(lo*lo);k_upper=w/(hi*hi)
 ratio=max(k_lower,k_upper)/min(k_lower,k_upper)
 rows.append(dict(x_source=row['x_source'],halfwidth_source=w,lower_height_source=lo,upper_height_source=hi,normalized_join_tangent_lower=[0,1],normalized_join_tangent_upper=[0,1],position_and_unit_tangent_continuous=True,curvature_lower_inverse_source=k_lower,curvature_upper_inverse_source=k_upper,curvature_ratio=ratio,curvature_continuous=math.isclose(k_lower,k_upper,rel_tol=1e-10)))
assert all(not r['curvature_continuous'] for r in rows)
r=dict(status='HALBSEKTIONS_STUDIE_G1_ABER_NICHT_G2_AN_MHB',input_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),rows=rows,limits=['Nur analytische Eigenschaften der vorbereiteten Viertellipsenstudie.','G1 bedeutet hier gleiche Position und normierte Tangentenrichtung am MHB; keine Laengs-/Loft-Stetigkeitsaussage.','Kruemmungssprung ist ein Befund, keine automatisch zu glaettende Quellenabweichung.','Keine native Ausfuehrung, kein physischer Massstab, keine Herstellerhaut- oder Produktionsfreigabe.'],production_release=False)
(O/'NASA_halfsection_join_curvature_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print([(x['x_source'],x['curvature_ratio']) for x in rows])
