from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd';h=hashlib.sha256(p.read_bytes()).hexdigest();out=R/'analysis/v192_hollow_wing_adaptive_volume_diagnostic.json';assert not out.exists();D=A.openDocument(str(p));s=D.Objects[0].Shape.copy();A.closeDocument(D.Name);box=Part.makeBox(2000,1000,2000,A.Vector(-1000,300,-1000));shapes=[s,s.cut(box),s.common(box)];rows=[]
for eps in (1e-9,1e-11):
 vals=[]
 for shape in shapes:
  props=GProp_GProps();err=brepgprop.VolumeProperties(Part.__toPythonOCC__(shape),props,eps,True,False);vals.append({'volume_mm3':props.Mass(),'estimated_relative_integration_error':err})
 row={'requested_relative_epsilon':eps,'source_root_tip':vals,'part_sum_minus_source_mm3':vals[1]['volume_mm3']+vals[2]['volume_mm3']-vals[0]['volume_mm3']};rows.append(row);out.write_text(json.dumps({'status':'RUNNING','rows':rows},indent=2)+'\n');print(row,flush=True)
assert hashlib.sha256(p.read_bytes()).hexdigest()==h;out.write_text(json.dumps({'status':'ADAPTIVE_VOLUME_DIAGNOSTIC_COMPLETE_NOT_RELEASED','input_sha256_unchanged':h,'installed_OCC_version':Part.OCC_VERSION,'binding':'Existing FreeCAD bundled OCC; no module installation or core replacement','rows':rows,'limits':['Reported integration errors are algorithm estimates, not rigorous geometry error bounds','No saved split CAD, structural joint or printing acceptance','Source experimental hollow wing remains unreleased']},indent=2)+'\n')
