from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain
from OCC.Core.TopoDS import topods
R=Path(__file__).resolve().parents[2];names=['WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd','WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_partition_trim_arc_parameter_census.json';assert not out.exists();rows=[]
for p in ps:
 D=A.openDocument(str(p))
 for o in D.Objects:
  count=0;small=[];minimum=None
  for i,face in enumerate(o.Shape.Faces,1):
   f=topods.Face(Part.__toPythonOCC__(face));surf=BRepGProp_Face(f,True);dom=BRepGProp_Domain(f);arc=0
   while dom.More():
    arc+=1;surf.Load(dom.Value());lo=surf.FirstParameter();hi=surf.LastParameter();width=hi-lo;count+=1;minimum=width if minimum is None else min(width,minimum)
    if width<1e-9:small.append({'face':i,'arc':arc,'parameter_start':lo,'parameter_end':hi,'parameter_width':width})
    dom.Next()
  rows.append({'object':o.Name,'trim_arc_count':count,'minimum_full_arc_parameter_width':minimum,'full_arcs_below_1e_minus9':small})
 A.closeDocument(D.Name)
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'FULL_TRIM_ARC_PARAMETER_WIDTH_CENSUS_NOT_SUBSPAN_AUDIT','input_sha256_unchanged':dict(zip(names,hs)),'upstream_source':'https://raw.githubusercontent.com/Open-Cascade-SAS/OCCT/master/src/ModelingAlgorithms/TKTopAlgo/BRepGProp/BRepGProp_VinertGK.cxx','upstream_observation':'Master source skips T knot subintervals narrower than1e-9; no proof installed binary identical','rows':rows,'limits':['Counts full arc parameter widths only; internal knot subintervals may be smaller','Parameter widths are not physical lengths or volume error bounds','Cannot confirm or exclude skipped-subspan contribution from this census alone','No integrator/core/tolerance changes or release'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)
