from pathlib import Path
import FreeCAD as A,Part,json,hashlib
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd';h=hashlib.sha256(p.read_bytes()).hexdigest();out=R/'analysis/v192_hollow_wing_split_fine_mesh_volume_diagnostic.json';assert not out.exists();D=A.openDocument(str(p));s=D.Objects[0].Shape.copy();A.closeDocument(D.Name);box=Part.makeBox(2000,1000,2000,A.Vector(-1000,300,-1000));parts=[s.cut(box),s.common(box)];rows=[];origin=A.Vector(650,300,0)
for tol in (.005,.002,.001):
 vals=[]
 for shape in [s]+parts:
  vs,fs=shape.tessellate(tol);v=[x-origin for x in vs];volume=abs(sum(v[a].dot(v[b].cross(v[c])) for a,b,c in fs)/6);vals.append({'triangles':len(fs),'signed_divergence_abs_volume_mm3':volume})
 rows.append({'requested_linear_deflection_mm':tol,'source_root_tip':vals,'part_sum_minus_source_mm3':vals[1]['signed_divergence_abs_volume_mm3']+vals[2]['signed_divergence_abs_volume_mm3']-vals[0]['signed_divergence_abs_volume_mm3']});out.write_text(json.dumps({'status':'RUNNING','rows':rows},indent=2)+'\n');print(rows[-1],flush=True)
assert hashlib.sha256(p.read_bytes()).hexdigest()==h;out.write_text(json.dumps({'status':'MESH_INTEGRATION_DIAGNOSTIC_COMPLETE_NOT_RELEASE','input_sha256_unchanged':h,'rows':rows,'limits':['Tessellation is approximate, not exact BRep volume proof','No saved mesh exports or STL/manifold/print acceptance','Deflection convergence is diagnostic only; original strict balance failure remains unresolved']},indent=2)+'\n')
