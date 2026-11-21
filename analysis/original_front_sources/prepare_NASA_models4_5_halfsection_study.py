from pathlib import Path
import json,math,hashlib,numpy as np
O=Path(__file__).parent;src=O/"NASA_models4_5_control_bindings.json";j=json.loads(src.read_text(encoding="utf-8"));rows=[];omitted=[]
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
 model=row['model'];x=row['x_source'];c=row['controls']
 if row['BLO_ellipse_degenerate']:
  omitted.append(dict(model=model,x_source=x,reason='Kollineare ELLI-Grenze, durch Quellenmodell5-LINE an derselben Station separat vertreten.'));continue
 topology=[('BLO','BCL','FLO','SCPLO' if model==4 else None),('NACLO','FLO','INLTLO',None),('NACSI','INLTLO','INLTUP',None),('NACUP','INLTUP','FUP',None),('BUP','FUP','CREASE','SCPUP'),('CAN','CREASE','TCL','SCPCAN')]
 points=[];arcs=[]
 for name,a,b,scp in topology:
  pts,res=arc(c[a],c[b],c[scp]) if scp else ([c[a],c[b]],0.)
  if points:assert math.dist(points[-1],pts[0])<1e-9
  points.extend(pts if not points else pts[1:]);arcs.append(dict(name=name,shape='ELLI' if scp else 'LINE',constraint_residual=res))
 zm=146+(x-352)/428;angles=[math.atan2(z-zm,y) for y,z in points];step=min(b-a for a,b in zip(angles,angles[1:]))
 rows.append(dict(model=model,x_source=x,controls=c,points_YZ_source=points,arcs=arcs,mapaxis_Z_source=zm,minimum_sampled_angular_step=step,strict_sampled_angular_order=step>0))
previous=json.loads((O/'NASA_model3_halfsection_study.json').read_text(encoding='utf-8'))['rows'][-1]
assert previous['x_source']==rows[0]['x_source']==414.5
assert len(previous['points_YZ_source'])==len(rows[0]['points_YZ_source'])
join_error=max(math.dist(a,b) for a,b in zip(previous['points_YZ_source'],rows[0]['points_YZ_source']));assert join_error<1e-9
r=dict(model3_to_model4_boundary_max_point_error_source=join_error,status='MODELLE4_5_FUENF_HALBSEKTIONS_STUDIEN_AUSGEWERTET',input_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),rows=rows,omitted=omitted,limits=['Regulaere Studienellipsen und Linien, keine Originalroutinen fuer diese Abschnitte ausgefuehrt.','Winkelordnung nur diskret geprueft; kein analytischer Schnitt-/THELIM-Nachweis.','Keine native CAD-Haut, physische Einheiten oder Produktionsfreigabe.'],production_release=False)
(O/'NASA_models4_5_halfsection_study.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(v['model'],v['x_source'],v['strict_sampled_angular_order']) for v in rows])
