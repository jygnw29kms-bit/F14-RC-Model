from pathlib import Path
import json,math,hashlib,numpy as np
O=Path(__file__).parent;src=O/"NASA_models6_7_control_bindings.json";j=json.loads(src.read_text(encoding="utf-8"));top=json.loads((O/"NASA_all_section_model_topologies.json").read_text(encoding="utf-8"))["models"];rows=[]
def arc(p0,p1,pc):
 end=np.subtract(p1,p0);control=np.subtract(pc,p0);y,z=end;u,v=control;ty,tz=control-end
 M=np.array([[0,0,0,0,1],[y*y,z*z,y,z,1],[0,0,u,v,0],[2*y*ty,2*z*tz,ty,tz,0]],float)
 _,_,V=np.linalg.svd(M);q=V[-1];a,b,c,d,e=q;assert a*b>0
 center=np.array([-c/(2*a),-d/(2*b)]);k=a*center[0]**2+b*center[1]**2-e;axes2=np.array([k/a,k/b]);assert min(axes2)>0
 axes=np.sqrt(axes2);t0=math.atan2(-center[1]/axes[1],-center[0]/axes[0]);t1=math.atan2((end[1]-center[1])/axes[1],(end[0]-center[0])/axes[0])
 tangent=np.array([-axes[0]*math.sin(t0),axes[1]*math.cos(t0)]);direction=1 if np.dot(tangent,control)>0 else -1
 sweep=(t1-t0)%(2*math.pi) if direction==1 else -((t0-t1)%(2*math.pi));assert abs(sweep)<math.pi
 pts=[(center+axes*np.array([math.cos(t0+sweep*i/100),math.sin(t0+sweep*i/100)])+p0).tolist() for i in range(101)]
 assert math.dist(pts[0],p0)<1e-9 and math.dist(pts[-1],p1)<1e-9
 return pts,float(np.max(np.abs(M@q)))
for row in j['station_values']:
 model=row['model'];x=row['x_source'];c=row['controls'];points=[];arcs=[]
 for a in top[model-1]['arcs']:
  p0,p1=c[a['start']],c[a['end']]
  if math.dist(p0,p1)<1e-9:
   arcs.append(dict(name=a['name'],degenerate=True));continue
  try:pts,res=arc(p0,p1,c[a['slope_control']]) if a['shape']=='ELLI' else ([p0,p1],0.)
  except AssertionError:
   failure=dict(status='MODELL6_7_STUDIE_AN_NICHTELLIPTISCHEN_CONSTRAINTS_GESTOPPT',model=model,x_source=x,arc=a['name'],start=p0,end=p1,control=c[a['slope_control']],limits=['Keine abgeschlossene Neunsektionspruefung.','Quelle unveraendert; Klassifikation/Originalroutine an diesem Fall pruefen.','Keine CAD-/Produktionsfreigabe.'],production_release=False)
   (O/'NASA_models6_7_halfsection_failure.json').write_text(json.dumps(failure,ensure_ascii=False,indent=2),encoding='utf-8');print(failure);raise SystemExit(0)
  if points:assert math.dist(points[-1],pts[0])<1e-9
  points.extend(pts if not points else pts[1:]);arcs.append(dict(name=a['name'],degenerate=False,shape=a['shape'],constraint_residual=res))
 zm=146+(x-352)/428;angles=[math.atan2(z-zm,y) for y,z in points];step=min(b-a for a,b in zip(angles,angles[1:]))
 rows.append(dict(model=model,x_source=x,controls=c,arcs=arcs,points_YZ_source=points,mapaxis_Z_source=zm,minimum_sampled_angular_step=step,strict_sampled_angular_order=step>0))
r=dict(status='NEUN_MODELL6_7_HALBSEKTIONS_STUDIEN_AUSGEWERTET',input_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),rows=rows,limits=['Degenerierte Punktboegen ausgelassen und protokolliert.','Studieninterpretation, noch kein Originalvergleich fuer diese Abschnitte.','Winkelordnung nur diskret; keine CAD-/Einheiten-/Produktionsfreigabe.'],production_release=False)
(O/'NASA_models6_7_halfsection_study.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(v['model'],v['x_source'],v['strict_sampled_angular_order']) for v in rows])
