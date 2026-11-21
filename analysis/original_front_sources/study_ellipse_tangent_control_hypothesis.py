"""Nur Hypothese: Kontrollpunkt bestimmt beide Endtangenten als Verbindungsgeraden."""
from pathlib import Path
import numpy as np,json,math
O=Path(__file__).parent
def solve(p0,p1,pc):
 dx,dy=np.subtract(p1,p0);tx0,ty0=np.subtract(pc,p0);tx1,ty1=np.subtract(pc,p1)
 M=np.array([[tx0,ty0,0],[dx,dy,dx*dx],[tx1,ty1,2*dx*tx1]],float);rhs=np.array([0,-dy*dy,-2*dy*ty1]);A,B,C=np.linalg.solve(M,rhs);res=float(np.max(np.abs(M@np.array([A,B,C])-rhs)));xc=-A/(2*C);yc=-B/2;k=C*xc*xc+yc*yc;ellipse=C>0 and k>0
 return dict(A=float(A),B=float(B),C=float(C),equation='A*u+B*v+C*u^2+v^2=0;u=x-xStart,v=y-yStart',maximum_constraint_residual=res,ellipse=bool(ellipse),center_local=[float(xc),float(yc)],semi_axes=[math.sqrt(k/C),math.sqrt(k)] if ellipse else None)
known=solve([0,0],[2,1],[0,1]);assert abs(known['C']-.25)<1e-12 and np.linalg.norm(np.array(known['center_local'])-[2,0])<1e-12
cases=[]
for name,p0,p1,pc in [('ZTCL_nose',[93,131.45],[205,171],[127.5,152]),('ZBCL_nose',[93,131.45],[176,116.5],[129.5,116.5]),('YMHB_nose',[93,0],[352,31],[164,31])]:
 r=solve(p0,p1,pc);cases.append(dict(name=name,start=p0,end=p1,control=pc,result=r))
r=dict(status='ENDTANGENTEN_KONTROLLPUNKT_HYPOTHESE_ANALYTISCH_GETESTET',assumption='GeradenEndpunkt->Kontrollpunkt sindEndtangenten; nochkeineBestaetigungderOriginalroutine.',synthetic_quarter_ellipse_test=known,cases=cases,limits=['SynthetischerTestverifiziertAlgebra, nichtWBPPW-Semantik oderF14Geometrie.','EllipsentypundEndconstraintsbeweisenkeinekorrekteZweigwahl oderOriginalhaut.','ELLX/ELLYNormalisierung/Versionsverhalten weiterhinseparatzuvalidieren.','KeineCADGeometrie/Masteraenderung oderProduktionsfreigabe.'],production_release=False)
(O/'ellipse_tangent_control_hypothesis.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(c['name'],c['result']['ellipse'],c['result']['maximum_constraint_residual']) for c in cases])
