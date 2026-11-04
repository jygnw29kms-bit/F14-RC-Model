"""Unabhaengige Zweig-/Ableitungspruefung der unbestaetigten Semantikhypothese."""
from pathlib import Path
import json,math,hashlib
import numpy as np
O=Path(__file__).parent;p=O/'ellipse_tangent_control_hypothesis.json';j=json.loads(p.read_text(encoding='utf-8'));rows=[]
for c in j['cases']:
 A,B,C=[c['result'][x] for x in ['A','B','C']];x0,y0=c['start'];x1,y1=c['end'];xc,yc=c['control'];u=np.linspace(0,x1-x0,1001);disc=B*B-4*(C*u*u+A*u);assert disc.min()>0;sign=min([-1,1],key=lambda s:abs((-B+s*math.sqrt(disc[0]))/2));v=(-B+sign*np.sqrt(disc))/2
 assert abs(v[0])<1e-9 and abs(v[-1]-(y1-y0))<1e-9
 residual=float(np.max(np.abs(A*u+B*v+C*u*u+v*v)));der=-(A+2*C*u)/(B+2*v);target=[(yc-y0)/(xc-x0),(yc-y1)/(xc-x1)];assert max(abs(der[0]-target[0]),abs(der[-1]-target[1]))<1e-10
 monotone=bool(np.all(np.diff(v)>=-1e-10) or np.all(np.diff(v)<=1e-10));assert monotone
 # Ellipsennormalform als zweite Auswertungsdarstellung.
 cx,cy=c['result']['center_local'];ra,rb=c['result']['semi_axes'];normal=(u-cx)**2/ra**2+(v-cy)**2/rb**2;assert np.max(np.abs(normal-1))<1e-12
 rows.append(dict(name=c['name'],chosen_quadratic_sign=sign,samples=1001,minimum_discriminant=float(disc.min()),max_implicit_equation_residual=residual,max_ellipse_normal_form_residual=float(np.max(np.abs(normal-1))),endpoint_slopes=[float(der[0]),float(der[-1])],control_point_slopes=target,monotone_sampled=True,points_source=[[float(x0+a),float(y0+b)] for a,b in zip(u[::100],v[::100])]))
r=dict(status='HYPOTHESENZWEIGE_UND_ENDSTEIGUNGEN_ANALYTISCH_GEPRUEFT',input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=rows,limits=['Interne mathematische Konsistenz, keine VerifikationderWBPPWOriginalroutine.','Monotoniean1001Proben,keineallgemeineKonturtoleranz.','Einheiten/UPCRegistrierung/Originalhautweiterunbelegt; keineCADUebernahme.'],production_release=False)
(O/'ellipse_hypothesis_branch_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(x['name'],x['max_implicit_equation_residual'],x['endpoint_slopes']) for x in rows])
