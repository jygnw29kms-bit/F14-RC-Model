import traceback
try:
 from pathlib import Path
 import FreeCAD as A,Part,json,hashlib,math
 from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain,BRepGProp_Vinert
 from OCC.Core.TopoDS import topods
 from OCC.Core.gp import gp_Pnt
 R=Path(__file__).resolve().parents[2];names=['WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd','WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_cavity_shell_saved_void_comparison.json';assert not out.exists();D=A.openDocument(str(ps[0]));s=D.Objects[0].Shape.copy();A.closeDocument(D.Name);shell=next(x for x in s.Shells if len(x.Faces)==2184);cavity=Part.makeSolid(shell);initial_volume=cavity.Volume
 if initial_volume<0:cavity.reverse()
 assert cavity.Volume>0 and cavity.isValid();D=A.openDocument(str(ps[1]));void=D.Objects[0].Shape.copy();A.closeDocument(D.Name)
 rows=[]
 for point in [(700,280,0),(700,300,0)]:
  vals=[]
  for f in void.Faces:
   face=topods.Face(Part.__toPythonOCC__(f));v=BRepGProp_Vinert(BRepGProp_Face(face,True),BRepGProp_Domain(face),gp_Pnt(*point),1e-11);vals.append(v.Mass())
  rows.append({'reference_point_mm':point,'saved_void_signed_face_flux_sum_mm3':math.fsum(vals)})
 comparisons={'temporary_cavity_initial_signed_volume_mm3':initial_volume,'cavity_solid_face_count':len(cavity.Faces),'saved_void_face_count':len(void.Faces),'cavity_default_volume_mm3':cavity.Volume,'saved_void_default_volume_mm3':void.Volume,'cavity_minus_saved_void_mm3':cavity.cut(void).Volume,'saved_void_minus_cavity_mm3':void.cut(cavity).Volume}
 assert [H(p) for p in ps]==hs
 out.write_text(json.dumps({'status':'INNER_SHELL_SOLID_COMPARED_WITH_SAVED_FUSED_VOID','input_sha256_unchanged':dict(zip(names,hs)),'comparisons':comparisons,'rows':rows,'limits':['In-memory inner shell reorientation only; no saved model modified','Zero native Boolean difference volume is not exact trim identity or rigorous volume error bound','Flux reuses same native integrator and two references; not independent geometry certification','No tolerance changes or print/flight acceptance'],'print_release':False,'flight_release':False},indent=2)+'\n');print(comparisons,rows)
 
except Exception:
 print(traceback.format_exc(),flush=True)
 raise


