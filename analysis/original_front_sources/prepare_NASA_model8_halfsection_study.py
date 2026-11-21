from pathlib import Path
import json,math,hashlib,numpy as np
O=Path(__file__).parent;src=O/"NASA_model8_control_bindings_with_source_jump.json";j=json.loads(src.read_text(encoding="utf-8"));top=json.loads((O/"NASA_all_section_model_topologies.json").read_text(encoding="utf-8"))["models"];rows=[]
def arc(p0,p1,pc,zm):
 end=np.subtract(p1,p0);control=np.subtract(pc,p0);y,z=end;u,v=control;ty,tz=control-end
 M=np.array([[0,0,0,0,1],[y*y,z*z,y,z,1],[0,0,u,v,0],[2*y*ty,2*z*tz,ty,tz,0]],float)
 _,_,V=np.linalg.svd(M);q=V[-1];a,b,c,d,e=q
 h0=math.atan2(p0[1]-zm,p0[0]);h1=math.atan2(p1[1]-zm,p1[0]);assert h1>h0
 previous=math.hypot(p0[0],p0[1]-zm);points=[]
 for i in range(101):
  h=h0+(h1-h0)*i/100;ch,sh=math.cos(h),math.sin(h);dz=zm-p0[1]
  qa=a*ch*ch+b*sh*sh;qb=-2*a*p0[0]*ch+2*b*dz*sh+c*ch+d*sh;qc=a*p0[0]**2+b*dz*dz-c*p0[0]+d*dz+e
  disc=qb*qb-4*qa*qc;assert disc>=0
  if abs(qa)<1e-14:roots=[-qc/qb]
  else:
   stable=-.5*(qb+math.copysign(math.sqrt(disc),qb))
   roots=[stable/qa,qc/stable] if stable!=0 else [-qb/(2*qa)]
  positive=[float(r) for r in roots if math.isfinite(r) and r>0];assert positive
  radius=min(positive,key=lambda r:abs(r-previous));previous=radius
  point=[radius*ch,zm+radius*sh];du=point[0]-p0[0];dv=point[1]-p0[1]
  assert abs(a*du*du+b*dv*dv+c*du+d*dv+e)<1e-8
  points.append(point)
 assert math.dist(points[0],p0)<1e-7 and math.dist(points[-1],p1)<1e-7
 return points,float(np.max(np.abs(M@q)))
for row in j['station_values']:
 model=row['model'];x=row['x_source'];c=row['controls'];zm=146+(x-352)/428;points=[];arcs=[]
 for a in top[model-1]['arcs']:
  p0,p1=c[a['start']],c[a['end']]
  if math.dist(p0,p1)<1e-9:
   arcs.append(dict(name=a['name'],degenerate=True));continue
  try:pts,res=arc(p0,p1,c[a['slope_control']],zm) if a['shape']=='ELLI' else ([p0,p1],0.)
  except AssertionError:
   failure=dict(status='MODELL6_7_STUDIE_AN_NICHTELLIPTISCHEN_CONSTRAINTS_GESTOPPT',model=model,x_source=x,arc=a['name'],start=p0,end=p1,control=c[a['slope_control']],limits=['Keine abgeschlossene Neunsektionspruefung.','Quelle unveraendert; Klassifikation/Originalroutine an diesem Fall pruefen.','Keine CAD-/Produktionsfreigabe.'],production_release=False)
   (O/'NASA_model8_halfsection_failure.json').write_text(json.dumps(failure,ensure_ascii=False,indent=2),encoding='utf-8');print(failure);raise SystemExit(0)
  if points:assert math.dist(points[-1],pts[0])<1e-9
  points.extend(pts if not points else pts[1:]);arcs.append(dict(name=a['name'],degenerate=False,shape=a['shape'],constraint_residual=res))
 zm=146+(x-352)/428;angles=[math.atan2(z-zm,y) for y,z in points];step=min(b-a for a,b in zip(angles,angles[1:]))
 rows.append(dict(model=model,x_source=x,source_boundary_side=row.get('source_boundary_side'),controls=c,arcs=arcs,points_YZ_source=points,mapaxis_Z_source=zm,minimum_sampled_angular_step=step,strict_sampled_angular_order=step>0))
r=dict(status='SIEBEN_MODELL8_HALBSEKTIONS_STUDIEN_MIT_697_GRENZWERTEN',input_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),rows=rows,limits=['Degenerierte Punktboegen ausgelassen und protokolliert.','Allgemeine reelle achsenparallele Konik, radiale stabile Wurzeln; Auswahl ueber Endpunkt und lokale Kontinuitaet, keine globale Wurzeleindeutigkeit.','Winkelordnung nur diskret; keine CAD-/Einheiten-/Produktionsfreigabe.'],production_release=False)
(O/'NASA_model8_halfsection_study.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(v['model'],v['x_source'],v['strict_sampled_angular_order']) for v in rows])
