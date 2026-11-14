from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
from OCC.Core.BRepLib import breplib,BRepLib_CheckCurveOnSurface
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain,BRepGProp_Vinert
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);out=R/'analysis/v192_void_segment5_sameparameter_study.json';cad=R/'migration/freecad/VOID_SEGMENT5_SAMEPARAMETER_STUDY_ONLY.FCStd';assert not out.exists() and not cad.exists();D=A.openDocument(str(p));original=D.getObject('VOID_TOOL_5').Shape.copy();A.closeDocument(D.Name);native=Part.__toPythonOCC__(original.copy());breplib.SameParameter(native,1e-10,True);candidate=Part.__fromPythonOCC__(native);assert candidate.isValid() and len(candidate.Solids)==1
rows=[]
for name,s in [('ORIGINAL_SAVED_SEG5',original),('FORCED_SAMEPARAMETER_REQUEST_1em10',candidate)]:
 sums=[]
 for point in [(700,280,0),(700,300,0)]:
  vals=[]
  for face in s.Faces:
   f=topods.Face(Part.__toPythonOCC__(face));v=BRepGProp_Vinert(BRepGProp_Face(f,True),BRepGProp_Domain(f),gp_Pnt(*point),1e-11);vals.append(v.Mass())
  sums.append(math.fsum(vals))
 distances=[];failed=0
 for face in s.Faces:
  f=topods.Face(Part.__toPythonOCC__(face))
  for e in face.Edges:
   check=BRepLib_CheckCurveOnSurface(topods.Edge(Part.__toPythonOCC__(e)),f);check.Perform()
   if check.IsDone() and check.ErrorStatus()==0:distances.append(check.MaxDistance())
   else:failed+=1
 rows.append({'object':name,'face_count':len(s.Faces),'valid':s.isValid(),'solids':len(s.Solids),'default_volume_mm3':s.Volume,'max_native_tolerance_mm':s.getTolerance(1),'P280_P300_flux_mm3':sums,'reference_change_mm3':sums[1]-sums[0],'curve_surface_pair_count':len(distances)+failed,'failed_curve_surface_pairs':failed,'max_curve_surface_distance_mm':max(distances)});print(rows[-1],flush=True)
D=A.newDocument('SEG5_PCURVE_STUDY')
for (name,s) in [('ORIGINAL_SAVED_SEG5',original),('FORCED_SAMEPARAMETER_REQUEST_1em10',candidate)]:
 o=D.addObject('PartDesign::Feature',name);o.Shape=s;o.addProperty('App::PropertyBool','PrintRelease');o.PrintRelease=False
D.recompute();D.saveAs(str(cad));A.closeDocument(D.Name);D=A.openDocument(str(cad));assert len(D.Objects)==2 and all(o.Shape.isValid() and not o.PrintRelease for o in D.Objects);A.closeDocument(D.Name);assert H(p)==h
out.write_text(json.dumps({'status':'ISOLATED_FORCED_SAMEPARAMETER_STUDY_SAVED_REOPENED','input_sha256_unchanged':h,'output_sha256':H(cad),'requested_sameparameter_tolerance_mm':1e-10,'forced':True,'rows':rows,'limits':['Recomputed pcurves on a copied shape; does not set all stored tolerances to the requested value','Candidate geometry must be separately compared; not promoted to cavity or aircraft','Reference sensitivity/curve mismatch do not by themselves establish volume accuracy or manufacturing fitness','No existing CAD or tolerance setter changes; no print/flight release'],'print_release':False,'flight_release':False},indent=2)+'\n')
