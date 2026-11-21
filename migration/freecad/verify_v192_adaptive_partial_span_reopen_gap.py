from pathlib import Path
import FreeCAD as App,json,hashlib,time
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd';prior=json.loads((R/'analysis/v192_adaptive_partial_span_subtraction.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(p)==prior['trial_sha256'];out=R/'analysis/v192_adaptive_partial_span_reopen_gap.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
d=App.openDocument(str(p));r=dict(status='REOPENED_ADAPTIVE_PARTIAL_SPAN_BOUNDARY_GAP_ONLY',trial_sha256=sha(p),print_release=False,flight_release=False)
try:
 objects=[o for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objects)==1;s=objects[0].Shape
 stage('validity_start');r.update(valid=s.isValid(),solids=len(s.Solids),shells=len(s.Shells),faces=len(s.Faces),volume_mm3=s.Volume);stage('validity_done',**r);assert r['valid'] and r['solids']==1 and r['shells']==2
 stage('boundary_distance_start');distance,points,info=s.Shells[0].distToShape(s.Shells[1]);stage('boundary_distance_done',distance_mm=distance)
 r.update(minimum_between_boundary_shells_mm=distance,closest_point_pairs_xyz_mm=[[list(a),list(b)] for a,b in points])
except Exception as err:r['status']='REOPEN_BOUNDARY_CHECK_FAILED';r['error_type']=type(err).__name__;r['error']=str(err);stage('exception',error=str(err))
finally:App.closeDocument(d.Name)
assert sha(p)==r['trial_sha256'];r['elapsed_seconds']=time.time()-start;r['limits']=['Only saved partial-span wing trial; root and tip remain solid.','Native minimum boundary distance is not a structural thickness requirement or printing qualification.','No normal-thickness field, ribs, joints, spars, physical tests or complete-model release.'];out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))
