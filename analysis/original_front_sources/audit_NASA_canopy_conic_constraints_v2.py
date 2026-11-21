from pathlib import Path
import json,math,hashlib,numpy as np
from ellipse_reference_evaluator import EllipseReference
from quick_elly_bodyline_reference import QuickEllyBodylineReference
O=Path(__file__).parent;j=json.loads((O/'NASA_canopy_control_point_bindings.json').read_text(encoding='utf-8'));yc=json.loads((O/'NASA_canopy_YCREASE_line_reference.json').read_text(encoding='utf-8'))['points_source']
def line(points,x):
 for a,b in zip(points,points[1:]):
  if a[0]<=x<=b[0]:return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])
 raise ValueError('Keine Extrapolation')
wcurve=EllipseReference([93,0],[352,31],[164,31])
tcurves=[(205,241,None),(241,313,QuickEllyBodylineReference([241,191.65],[313,203],[274,203])),(313,352,QuickEllyBodylineReference([313,203],[352,199.5],[331,203]))]
def top(x):
 for a,b,r in tcurves:
  if a<=x<=b:return r.value(x) if r else line([[205,171],[241,191.65]],x)
 raise ValueError('Keine Extrapolation')
rows=[]
for x in [210,220,250,300,340]:
 w=wcurve.value(x);crease=[line(yc,x),line(j['linear_curves_points']['ZCREASE'],x)];fup=[w,line(j['linear_curves_points']['ZFUP'],x)];tcl=[0,top(x)]
 scpup=[w,line(j['linear_curves_points']['ZSCPUP'],x)];scpcan=[line(j['linear_curves_points']['YSCPCAN'],x),top(x)]
 for name,p0,p1,pc in [('BUP',fup,crease,scpup),('CAN',crease,tcl,scpcan)]:
  # Lokale Translation verbessert die Kondition; homogene vier Constraints.
  end=np.subtract(p1,p0);control=np.subtract(pc,p0);y,z=end;u,v=control;ty,tz=np.subtract(control,end)
  M=np.array([[0,0,0,0,1],[y*y,z*z,y,z,1],[0,0,u,v,0],[2*y*ty,2*z*tz,ty,tz,0]],float)
  _,s,V=np.linalg.svd(M);q=V[-1];a,b,c,d,e=q
  assert a*b>0
  center=np.array([-c/(2*a),-d/(2*b)]);k=a*center[0]**2+b*center[1]**2-e;axes2=np.array([k/a,k/b]);assert min(axes2)>0
  residual=float(np.max(np.abs(M@q)));assert residual<1e-10
  axes=np.sqrt(axes2);a0=math.atan2(-center[1]/axes[1],-center[0]/axes[0]);a1=math.atan2((end[1]-center[1])/axes[1],(end[0]-center[0])/axes[0])
  tangent=np.array([-axes[0]*math.sin(a0),axes[1]*math.cos(a0)])
  direction=1 if np.dot(tangent,control)>0 else -1
  sweep=(a1-a0)%(2*math.pi) if direction==1 else -((a0-a1)%(2*math.pi))
  assert abs(sweep)<math.pi
  samples=[(center+axes*np.array([math.cos(a0+sweep*i/100),math.sin(a0+sweep*i/100)])+p0).tolist() for i in range(101)]
  assert np.linalg.norm(np.subtract(samples[0],p0))<1e-9 and np.linalg.norm(np.subtract(samples[-1],p1))<1e-9
  endtan=direction*np.array([-axes[0]*math.sin(a1),axes[1]*math.cos(a1)])
  expected=np.subtract(p1,pc);cosine=float(np.dot(endtan,expected)/(np.linalg.norm(endtan)*np.linalg.norm(expected)));assert cosine>1-1e-10
  rows.append(dict(x_source=x,arc=name,sweep_radians=sweep,end_directed_tangent_cosine=cosine,points_YZ_source=samples,start=p0,end=p1,control=pc,center_source=(center+p0).tolist(),semiaxes_source=np.sqrt(axes2).tolist(),max_constraint_residual=residual,smallest_constraint_singular_value=float(s[-1])))
r=dict(status='ZEHN_CANOPY_BOGEN_CONSTRAINTS_MIT_ORIGINALVERGLICHENEM_ELLY_PASS',binding_sha256=hashlib.sha256((O/'NASA_canopy_control_point_bindings.json').read_bytes()).hexdigest(),rows=rows,limits=['Explizite Hypothese: Kontrollpunkt ist Schnitt der Endtangenten; noch kein vollstaendiger Originalroutinebeleg.','Positive Ellipsenachsen und Endpunkt-/Tangentenconstraints geprueft; Gerichteter kurzer Bogen mit101Punkten geprueft; gegenseitige Ueberdeckung noch offen. Bodyline-ELLY separat nach Originalvergleich ausgewertet.','Keine CAD-Boegen, Flaechen oder Loft ausgefuehrt; Quelleneinheiten unveraendert.','Keine Herstellerhaut-/Produktionsfreigabe.'],production_release=False)
(O/'NASA_canopy_conic_constraint_v2_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print('10EllipsenconstraintsPASS; maxRest',max(r['max_constraint_residual'] for r in rows))
