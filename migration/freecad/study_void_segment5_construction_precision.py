from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain,BRepGProp_Vinert
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt
R=Path(__file__).resolve().parents[2];names=['F14_CURRENT_FULL_VIEW_v192.FCStd','WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];bp=R/'analysis/v192_adaptive_void_segments_build.json';build=json.loads(bp.read_text());assert hs[0]==build['source_sha256'] and hs[1]==build['output_sha256'];out=R/'analysis/v192_void_segment5_precision_study.json';cad=R/'migration/freecad/VOID_SEGMENT5_PRECISION_COMPARISON_STUDY_ONLY.FCStd';assert not out.exists() and not cad.exists();span=build['rows'][5];ys=[span['y_start'],span['y_end']];D=A.openDocument(str(ps[0]));wing=D.getObject('WING_R').Shape;wires=[]
for y in ys:
 ws=wing.slice(A.Vector(0,1,0),y);assert len(ws)==1;off=ws[0].makeOffset2D(-.43,0,False,False,False);assert len(off.Wires)==1;wires.append(off.Wires[0].copy())
A.closeDocument(D.Name);D=A.openDocument(str(ps[1]));original=D.getObject('VOID_TOOL_5').Shape.copy();A.closeDocument(D.Name);shapes=[('ORIGINAL_SAVED_SEG5',None,original)]
for precision in [1e-6,1e-9]:
 loft=BRepOffsetAPI_ThruSections(True,True,precision);loft.CheckCompatibility(True)
 for w in wires:loft.AddWire(topods.Wire(Part.__toPythonOCC__(w.copy())))
 loft.Build();assert loft.IsDone();s=Part.__fromPythonOCC__(loft.Shape());assert s.isValid() and len(s.Solids)==1;shapes.append(('REBUILT_PRES_'+str(precision).replace('-','m').replace('.','p'),precision,s))
rows=[]
for name,precision,s in shapes:
 samples=[]
 for point in [(700,280,0),(700,300,0)]:
  values=[]
  for face in s.Faces:
   f=topods.Face(Part.__toPythonOCC__(face));v=BRepGProp_Vinert(BRepGProp_Face(f,True),BRepGProp_Domain(f),gp_Pnt(*point),1e-11);values.append(v.Mass())
  samples.append(math.fsum(values))
 rows.append({'object':name,'construction_pres3d_mm':precision,'faces':len(s.Faces),'valid':s.isValid(),'solids':len(s.Solids),'default_volume_mm3':s.Volume,'max_native_tolerance_mm':s.getTolerance(1),'P280_P300_signed_flux_sums_mm3':samples,'reference_change_mm3':samples[1]-samples[0]});print(rows[-1],flush=True)
D=A.newDocument('SEG5_PRECISION_STUDY')
for name,precision,s in shapes:
 o=D.addObject('PartDesign::Feature',name);o.Shape=s;o.addProperty('App::PropertyBool','PrintRelease');o.PrintRelease=False
D.recompute();D.saveAs(str(cad));A.closeDocument(D.Name);D=A.openDocument(str(cad));assert len(D.Objects)==3 and all(o.Shape.isValid() and not o.PrintRelease for o in D.Objects);A.closeDocument(D.Name);assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'ISOLATED_SEGMENT5_CONSTRUCTION_PRECISION_COMPARISON_SAVED_REOPENED','input_sha256_unchanged':dict(zip(names,hs)),'output_sha256':H(cad),'span_mm':ys,'source_offset_mm':-.43,'rows':rows,'limits':['New separate study only; existing master and cavity unchanged','pres3d is a construction criterion, not proven achieved accuracy or automatic tolerance override','Recreated offset sections and native builder may differ from original FreeCAD builder','No assembly, strength, global volume, print or flight acceptance'],'print_release':False,'flight_release':False},indent=2)+'\n')
