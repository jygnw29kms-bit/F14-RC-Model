from pathlib import Path
import json,math,hashlib,numpy as np
O=Path(__file__).parent;src=O/'NASA_model3_inlet_control_bindings.json';j=json.loads(src.read_text(encoding='utf-8'));rows=[]
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
 x=row['x_source'];c=row['controls'];points=[];arcs=[]
 for name,a,b,scp in [('BLO','BCL','MHB','SCPLO'),('BSI','MHB','FLO',None),('NACLO','FLO','INLTLO',None),('NACSI','INLTLO','INLTUP',None),('NACUP','INLTUP','FUP',None),('BUP','FUP','CREASE','SCPUP'),('CAN','CREASE','TCL','SCPCAN')]:
  if math.dist(c[a],c[b])<1e-10:
   arcs.append(dict(name=name,degenerate=True));continue
  pts,res=arc(c[a],c[b],c[scp]) if scp else ([c[a],c[b]],0.)
  if points:assert math.dist(points[-1],pts[0])<1e-9
  points.extend(pts if not points else pts[1:]);arcs.append(dict(name=name,degenerate=False,constraint_residual=res))
 zm=146+(x-352)/428;angles=[math.atan2(z-zm,y) for y,z in points];steps=[b-a for a,b in zip(angles,angles[1:])]
 rows.append(dict(x_source=x,points_YZ_source=points,arcs=arcs,mapaxis_Z_source=zm,minimum_sampled_angular_step=min(steps),strict_angular_order=min(steps)>0))
r=dict(status='VIER_MODELL3_HALBSEKTIONEN_STUDIE_AUSGEWERTET',input_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),rows=rows,limits=['ELLI als achsenparallele Studienellipse; keine Originalroutine fuer diese Abschnitte ausgefuehrt.','Winkelordnung ist gesonderter Befund, keine automatische Aussenhuellenauswahl.','Keine EDF-Innenkanaele, native CAD-Haut oder Produktionsfreigabe.'],production_release=False)
(O/'NASA_model3_halfsection_study.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(v['x_source'],v['strict_angular_order'],v['minimum_sampled_angular_step']) for v in rows])
