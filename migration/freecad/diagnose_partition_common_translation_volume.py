from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
R=Path(__file__).resolve().parents[2];names=['WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd','WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_partition_volume_common_translation_diagnostic.json';assert not out.exists();sh=[]
for p in ps:
 D=A.openDocument(str(p));sh.extend((o.Name,o.Shape.copy()) for o in D.Objects);A.closeDocument(D.Name)
rows=[]
for shift in [(0,0,0),(-700,-300,0),(-700,-300,4)]:
 measures=[]
 for name,s in sh:
  t=s.copy();t.translate(A.Vector(*shift));props=GProp_GProps();err=brepgprop.VolumePropertiesGK(Part.__toPythonOCC__(t),props,1e-11,True,True,False,False,False)
  measures.append({'object':name,'GK_volume_mm3':props.Mass(),'estimated_relative_error':err});print(shift,name,props.Mass(),flush=True)
 rows.append({'common_translation_mm':shift,'measurements':measures,'part_sum_minus_source_mm3':sum(m['GK_volume_mm3'] for m in measures[1:])-measures[0]['GK_volume_mm3']})
 out.write_text(json.dumps({'status':'RUNNING','rows':rows},indent=2)+'\n')
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'COMMON_TRANSLATION_VOLUME_CONDITIONING_MEASURED','input_sha256_unchanged':dict(zip(names,hs)),'requested_relative_epsilon':1e-11,'rows':rows,'limits':['Rigid translation in memory only; saved CAD unchanged','Native error estimates not rigorous volume bounds','Three coordinate frames do not establish convergence, exact geometry identity or acceptance','No tolerance or core change; source partition remains review only'],'print_release':False,'flight_release':False},indent=2)+'\n')
