"""Native Endprofilprüfung gegen unveränderte OriginalsektionA, keine Modelländerung."""
import FreeCAD as App,Part,json,hashlib,math
from pathlib import Path
B=Path(__file__).parent;paths=[B/'F14_NOSE_A_SHAPE_SENSITIVITY.FCStd',B/'F14_ORIGINAL_ABCDEF_SECTION_CANDIDATES.FCStd'];hs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};d=App.openDocument(str(paths[0]));e=App.openDocument(str(paths[1]));a=e.getObject('SOURCE_SECTION_A').Shape;w=d.getObject('HYPOTHESE_8').Shape;b=Part.Face(w);assert a.isValid() and b.isValid()
ba=a.BoundBox;bb=b.BoundBox;assert abs(ba.XMin-bb.XMin)<1e-6 and abs(ba.XMax-bb.XMax)<1e-6
common=a.common(b);assert common.isValid();ab=a.cut(b);bc=b.cut(a)
for shape in [ab,bc]:
 if not shape.isNull():assert shape.isValid()
def sample_distance(src,dst):
 vals=[]
 for edge in src.Edges:
  for v in edge.discretize(Deflection=.01):
   value=Part.Vertex(v).distToShape(dst)[0];assert math.isfinite(value);vals.append(value)
 return max(vals)
wa=a.Wires[0];wb=b.Wires[0]
j=dict(status='NATIVER_ENDPROFILVERGLEICH_ORIGINAL_A_AUSGEFUEHRT',inputs=hs,original_A_area_mm2=a.Area,hypothesis_end_area_mm2=b.Area,intersection_area_mm2=common.Area,original_minus_hypothesis_area_mm2=0 if ab.isNull() else ab.Area,hypothesis_minus_original_area_mm2=0 if bc.isNull() else bc.Area,width_difference_mm=bb.YLength-ba.YLength,height_difference_mm=bb.ZLength-ba.ZLength,original_to_hypothesis_sampled_boundary_distance_mm=sample_distance(wa,wb),hypothesis_to_original_sampled_boundary_distance_mm=sample_distance(wb,wa),hinweise=['Distanzabfrage an diskreten Quellkantensamples; kein exakter Hausdorff-Nachweis.','Gleiche X-Ebene ist noch keine verifizierte gemeinsame Quellenregistrierung.','Flächen- und Randabweichungen zeigen: keine nahtlose Übernahme als Original-A-Anschluss.'],master_geaendert=False,originalform_freigegeben=False,produktion_freigegeben=False)
App.closeDocument(d.Name);App.closeDocument(e.Name);assert hs=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};(B/'freecad_nose_endpoint_original_A_comparison.json').write_text(json.dumps(j,ensure_ascii=False,indent=2));print(json.dumps(j))
