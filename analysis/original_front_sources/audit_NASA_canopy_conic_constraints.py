from pathlib import Path
import json,math,hashlib,numpy as np
from ellipse_reference_evaluator import EllipseReference
O=Path(__file__).parent;j=json.loads((O/'NASA_canopy_control_point_bindings.json').read_text(encoding='utf-8'));yc=json.loads((O/'NASA_canopy_YCREASE_line_reference.json').read_text(encoding='utf-8'))['points_source']
def line(points,x):
 for a,b in zip(points,points[1:]):
  if a[0]<=x<=b[0]:return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])
 raise ValueError('Keine Extrapolation')
wcurve=EllipseReference([93,0],[352,31],[164,31])
try:
 tail=EllipseReference([313,203],[352,199.5],[331,203])
except ValueError as error:
 r=dict(status='CANOPY_STUDIE_GESPERRT_DIREKT_ELLY_NICHT_ELLIPTISCH',rejected_source_segment=dict(shape='ELLY',start=[313,203],end=[352,199.5],control=[331,203]),error=str(error),limits=['Die bisherige Tangentenschnittpunkt-/achsenparallele-Conic-Hypothese ergibt hier keine Ellipse.','Quelle nicht aendern, nicht zu LINE/Parabel glaetten und keinen Zweig erzwingen.','Dies belegt eine Grenze der Studieninterpretation, keinen Fehler der NASA-Tabelle.','Keine zehn Canopybogen-Pruefungen ausgefuehrt; keine neue Geometrie oder Produktionsfreigabe.'],production_release=False)
 (O/'NASA_canopy_conic_constraint_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
 print(r['status']);raise SystemExit(0)
tcurves=[(205,241,None),(241,313,EllipseReference([241,191.65],[313,203],[274,203])),(313,352,tail)]
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
  rows.append(dict(x_source=x,arc=name,start=p0,end=p1,control=pc,center_source=(center+p0).tolist(),semiaxes_source=np.sqrt(axes2).tolist(),max_constraint_residual=residual,smallest_constraint_singular_value=float(s[-1])))
r=dict(status='ZEHN_CANOPY_BOGEN_KEGELSCHNITT_CONSTRAINTS_PASS',binding_sha256=hashlib.sha256((O/'NASA_canopy_control_point_bindings.json').read_bytes()).hexdigest(),rows=rows,limits=['Explizite Hypothese: Kontrollpunkt ist Schnitt der Endtangenten; noch kein vollstaendiger Originalroutinebeleg.','Positive Ellipsenachsen und Endpunkt-/Tangentenconstraints geprueft; Bogen-Zweigwahl und gegenseitige Ueberdeckung noch offen.','Keine CAD-Boegen, Flaechen oder Loft ausgefuehrt; Quelleneinheiten unveraendert.','Keine Herstellerhaut-/Produktionsfreigabe.'],production_release=False)
(O/'NASA_canopy_conic_constraint_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print('10EllipsenconstraintsPASS; maxRest',max(r['max_constraint_residual'] for r in rows))
