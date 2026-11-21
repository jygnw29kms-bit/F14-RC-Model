from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd';h=hashlib.sha256(p.read_bytes()).hexdigest();out=R/'analysis/v192_generalfuse_adaptive_tolerance_diagnostic.json';assert not out.exists();D=A.openDocument(str(p));s=D.Objects[0].Shape.copy();A.closeDocument(D.Name);pts=[A.Vector(-1000,300,-1000),A.Vector(1000,300,-1000),A.Vector(1000,300,1000),A.Vector(-1000,300,1000)];res,_=s.generalFuse([Part.Face(Part.makePolygon(pts+[pts[0]]))]);rows=[]
for name,x in [('SOURCE',s)]+[('PART'+str(i),x) for i,x in enumerate(res.Solids)]:
 props=GProp_GProps();err=brepgprop.VolumePropertiesGK(Part.__toPythonOCC__(x),props,1e-11,True,True,False,False,False);rows.append({'name':name,'GK_volume_mm3':props.Mass(),'estimated_relative_error':err,'tolerance_by_mode':{str(i):x.getTolerance(i) for i in (0,1,2)}})
r={'status':'GENERALFUSE_GK_AND_NATIVE_TOLERANCES_MEASURED','input_sha256_unchanged':h,'rows':rows,'native_tolerance_method_doc':s.getTolerance.__doc__,'part_sum_minus_source_mm3':sum(r['GK_volume_mm3'] for r in rows[1:])-rows[0]['GK_volume_mm3'],'limits':['Topological tolerances are local geometry tolerances, not a rigorous volume error bound','No tolerance modification or relaxed gate','No saved split CAD or printing acceptance']};assert hashlib.sha256(p.read_bytes()).hexdigest()==h;out.write_text(json.dumps(r,indent=2)+'\n');print(r)
