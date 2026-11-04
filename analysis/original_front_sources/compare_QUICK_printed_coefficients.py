"""Gedruckte Zwischenkoeffizienten gegen getrennte analytische Auswertung."""
from pathlib import Path
import numpy as np,math,json
O=Path(__file__).parent;rows=[]
for sign in [-1,1]:
 A,B,C=-.048419379,sign*.2746033,.0048419349;printed_y0=sign*1.76327;u=np.linspace(0,5,1001);disc=B*B-4*(C*u*u+A*u);root_sign=sign;v=(-B+root_sign*np.sqrt(disc))/2;printed_curve=printed_y0+v
 m=sign*math.tan(math.radians(10));y0=10*m;end=sign*2;dy=end-y0;cx=end/m;tx0=cx-10;tx1=cx-15;M=np.array([[tx0,dy,0],[5,dy,25],[tx1,0,10*tx1]]);rhs=np.array([0,-dy*dy,0]);a,b,c=np.linalg.solve(M,rhs);computed=y0+(-b+sign*np.sqrt(b*b-4*(c*u*u+a*u)))/2
 rows.append(dict(sign=sign,printed_coefficients_local={'A':A,'B':B,'C':C},computed_coefficients_local={'A':float(a),'B':float(b),'C':float(c)},printed_local_origin=[10,printed_y0],samples=1001,maximum_sampled_value_difference=float(np.max(np.abs(printed_curve-computed))),printed_coefficient_curve_end=float(printed_curve[-1]),expected_end=end))
r=dict(status='GEDRUCKTE_QUICK_KOEFFIZIENTEN_NUMERISCH_VERGLICHEN',source='CR2676 Fig11f PDF69/gedr63, ZweigeINXBLM2/3Segment2',interpretation='GedruckteKoeffizientenwerdenalsAx+By+Cx2+y2=0inKoordinatenrelativzuSegmentstartausgewertet.',rows=rows,limits=['VergleichbelegtlokaleTranslationundFormfuerdiesenELLXFillet-ReferenzfallinnerhalbangegebenerNumerikabweichungen.','OriginaldruckkoeffizientenundEndpunktegerundet; keinbitgenauerCodeabgleich.','NichtalleF14Direktsegmente/ELLYoderGenerikvalidiert, keineOriginalhaut-/Produktionsfreigabe.'],production_release=False)
(O/'QUICK_printed_coefficient_comparison.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(x['sign'],x['maximum_sampled_value_difference']) for x in rows])
