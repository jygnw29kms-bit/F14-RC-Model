"""Unabhaengiger Vergleich mit gedruckter QUICK-Ausgabe CR2676 Fig9/12."""
from pathlib import Path
import numpy as np,math,json
O=Path(__file__).parent;m=math.tan(math.radians(10));rows=[]
for sign in [-1,1]:
 p0=np.array([10,sign*10*m]);p1=np.array([15,sign*2]);pc=np.array([2/m,sign*2]);dx,dy=p1-p0;t0=pc-p0;t1=pc-p1;M=np.array([[*t0,0],[dx,dy,dx*dx],[*t1,2*dx*t1[0]]]);rhs=np.array([0,-dy*dy,-2*dy*t1[1]]);A,B,C=np.linalg.solve(M,rhs);den=B+2*dy;vx=-(A+2*C*dx)/den;vxx=-(2*C+2*vx*vx)/den;printed_v=sign*2;printed_vxx=-sign*.01295
 assert abs(vxx-printed_vxx)<=.000005 and abs(vx)<1e-12
 checks=[]
 for x,printed in [(5,.88163),(10,1.76327)]:
  computed=sign*x*m;assert abs(computed-sign*printed)<=.000005;checks.append(dict(x=x,computed_v=computed,printed_v=sign*printed))
 rows.append(dict(side_sign=sign,fillet_start=p0.tolist(),fillet_end=p1.tolist(),tangent_intersection_inferred=pc.tolist(),computed_end_v=float(p1[1]),printed_end_v=printed_v,computed_end_vx=float(vx),printed_end_vx=0,computed_end_vxx=float(vxx),printed_end_vxx=printed_vxx,end_vxx_difference=float(vxx-printed_vxx),line_checks=checks))
r=dict(status='QUICK_ELLX_FILLET_ENDABLEITUNG_GEGEN_GEDRUCKTE_AUSGABE_BESTAETIGT',source='NASA-CR2676VolII Fig9PDF57/gedr51 undFig12PDF70/gedr64',input_interpretation='10degGerade bisx10,Ellipsefilletx10..15,anschliessendv=+/-2. TangentenschnittpunktderbeidenGeradenermittelt.',rows=rows,comparison_tolerance='0.000005 inQuellenausgabeeinheiten, aus5NachkommastellendergedrucktenAusgabe; keineGeometrietoleranz.',limits=['Belegt diesenELLXFilletfall undEndableitung, nichtalleELLX/ELLYF14Direktsegmente odergesamteRoutine.','InnenkurveohnegedruckteZwischenproben nochunabhaengigzupruefen.','KeineOriginalF14Haut/Einheitenregistrierung/Produktionsfreigabe.'],production_release=False)
(O/'QUICK_printed_fillet_reference_validation.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(x['side_sign'],x['computed_end_vxx'],x['end_vxx_difference']) for x in rows])
