from pathlib import Path
import json,math,hashlib
O=Path(__file__).parent;src=O/'NASA_canopy_conic_constraint_v2_audit.json';j=json.loads(src.read_text(encoding='utf-8'));rows=[]
def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def intersects(a,b,c,d):
 if max(a[0],b[0])+1e-9<min(c[0],d[0]) or max(c[0],d[0])+1e-9<min(a[0],b[0]) or max(a[1],b[1])+1e-9<min(c[1],d[1]) or max(c[1],d[1])+1e-9<min(a[1],b[1]):return False
 v=[orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)]
 return v[0]*v[1]<=0 and v[2]*v[3]<=0
for x in sorted(set(r['x_source'] for r in j['rows'])):
 arcs={r['arc']:r for r in j['rows'] if r['x_source']==x};fup=arcs['BUP']['start'];w=fup[0];mid=138.5+(x-205)*(130.5-138.5)/147;bottom=118+(x-205)*3.75/147
 assert bottom<mid<fup[1]
 lower=[[w*math.sin(i*math.pi/200),mid-(mid-bottom)*math.cos(i*math.pi/200)] for i in range(101)]
 pts=lower+[fup]+arcs['BUP']['points_YZ_source'][1:]+arcs['CAN']['points_YZ_source'][1:]
 assert min(v[0] for v in pts)>-1e-9
 edges=list(zip(pts,pts[1:]+pts[:1]));hits=[]
 for i,(a,b) in enumerate(edges):
  assert math.dist(a,b)>1e-10
  for k in range(i+2,len(edges)):
   if i==0 and k==len(edges)-1:continue
   if intersects(a,b,*edges[k]):hits.append([i,k])
 assert not hits,(x,hits)
 area=sum(a[0]*b[1]-a[1]*b[0] for a,b in edges)/2;assert area>0
 rows.append(dict(x_source=x,points_YZ_source=pts,point_count=len(pts),closed_polygon_half_area_source2=area,nonadjacent_segment_intersections=hits,closure='Nur Pruefpolygon: gerade Symmetrieachsenverbindung TCL->BCL, keine neue Hautkante.',components=['BLO Viertellipse','BSI Linie','BUP Studienellipse','CAN Studienellipse']))
r=dict(status='FUENF_CANOPY_HALBSEKTIONS_PRUEFPOLYGONE_OHNE_SELBSTSCHNITT',input_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),rows=rows,limits=['Diskrete Polylinienpruefung, kein exakter analytischer Bogenschnittnachweis.','BLO/ELLI weiterhin geometrische Studieninterpretation, keine ausgefuehrte Originalquerschnittsroutine.','Keine Spiegelung, native CAD-Flaeche, Loft-, Einheiten- oder Produktionsfreigabe.'],production_release=False)
(O/'NASA_canopy_halfsection_polygon_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(r['x_source'],r['point_count'],r['closed_polygon_half_area_source2']) for r in rows])
