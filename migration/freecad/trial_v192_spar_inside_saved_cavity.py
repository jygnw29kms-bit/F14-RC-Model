from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd';basis=R/'analysis/v192_straight_spar_packaging_trial.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(src);expected=json.loads((R/'analysis/v192_void_all17_fusion.json').read_text())['output_sha256'];assert before==expected
b=json.loads(basis.read_text());out=R/'analysis/v192_spar_inside_saved_cavity_trial.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
a=App.Vector(*b['axis_start_mm']);z=App.Vector(*b['axis_end_mm']);v=z-a
p=a+v*((185-a.y)/v.y);q=a+v*((435-a.y)/v.y);axis=q-p;tool=Part.makeCylinder(2,axis.Length,p,axis);assert tool.isValid()
stage('open_saved_void');d=App.openDocument(str(src))
try:
 objects=[o for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objects)==1;c=objects[0].Shape;assert c.isValid() and len(c.Solids)==1
 stage('outside_cavity_cut_start');outside=tool.cut(c).Volume;stage('outside_cavity_cut_done',outside_volume_mm3=outside)
 stage('cavity_boundary_distance_start');gap,pts,info=tool.Shells[0].distToShape(c.Shells[0]);stage('cavity_boundary_distance_done',distance_mm=gap)
finally:App.closeDocument(d.Name)
assert sha(src)==before
r={'status':'SHORTENED_4MM_ENVELOPE_VS_SAVED_VOID_ONLY','void_sha256':before,'spar_axis_basis_sha256':sha(basis),'axis_start_mm':list(p),'axis_end_mm':list(q),'diameter_mm':4,'length_mm':axis.Length,'candidate_volume_mm3':tool.Volume,'outside_cavity_volume_mm3':outside,'native_minimum_cavity_boundary_gap_mm':gap,'closest_point_pairs_mm':[[list(p),list(q)] for p,q in pts],'contained_within_1e_7_mm3':outside<1e-7,'limits':['Same straight axis as earlier trial, shortened to Y185..435 to exclude cavity endcaps','Not full original Y155..440 spar fit; root/tip still require transfer geometry','Bare 4mm packaging cylinder; no adhesive allowance, tolerances, caps, ribs or selected carbon hardware','Void remains numerical hollowing trial, not structurally released interior','No CAD edits or manufactured part'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))
