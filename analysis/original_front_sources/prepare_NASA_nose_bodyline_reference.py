from pathlib import Path
import json,hashlib,math
from ellipse_reference_evaluator import EllipseReference
O=Path(__file__).parent;src=O/'ellipse_tangent_control_hypothesis.json';j=json.loads(src.read_text(encoding='utf-8'));rows=[]
# Unabhaengiger gedruckter Filletfall.
m=math.tan(math.radians(10));r=EllipseReference([10,10*m],[15,2],[2/m,2]);assert abs(r.derivatives(15)[1]+.01295)<=.000005
for c in j['cases']:
 r=EllipseReference(c['start'],c['end'],c['control']);x0,x1=c['start'][0],c['end'][0];pts=[[x0+(x1-x0)*i/100,r.value(x0+(x1-x0)*i/100)] for i in range(101)]
 try:r.value(x0-1)
 except ValueError:pass
 else:raise AssertionError('Extrapolation nicht gesperrt')
 rows.append(dict(name=c['name'],points_source=pts,source_domain=[x0,x1],endpoint_derivatives=[r.derivatives(x0),r.derivatives(x1)]))
report=dict(status='NASA_NASEN_BODYLINES_STUDIENREFERENZEN_VORBEREITET',inputs={src.name:hashlib.sha256(src.read_bytes()).hexdigest(),'ellipse_reference_evaluator.py':hashlib.sha256((O/'ellipse_reference_evaluator.py').read_bytes()).hexdigest()},curves=rows,coordinate_units='UnveraenderteQuellenzahlen; EinheitennichtfuerCADumgerechnet.',limits=['DirekteF14SegmentsemantiknochkeineallgemeineOriginalroutineverifikation.','KeineQuerschnittsboegenoder3DHautausdiesenBodylineserfunden.','KeineUPCRegistrierung/Wasserlinie/MasteraenderungoderProduktionsfreigabe.'],production_release=False)
(O/'NASA_nose_bodyline_reference_study.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('3offeneBodylineStudienreferenzen je101Punkte;FilletreferenzundExtrapolationssperrePASS.')
