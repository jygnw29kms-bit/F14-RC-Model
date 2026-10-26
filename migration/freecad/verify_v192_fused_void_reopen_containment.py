from pathlib import Path
import FreeCAD as App,json,hashlib,time
R=Path(__file__).resolve().parents[2];master=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';tool=R/'migration/freecad/WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fusion=json.loads((R/'analysis/v192_void_all17_fusion.json').read_text());assert sha(tool)==fusion['output_sha256'];out=R/'analysis/v192_fused_void_reopen_containment.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();before=sha(master);start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
a=App.openDocument(str(master));b=App.openDocument(str(tool));r=dict(status='FUSED_PARTIAL_SPAN_VOID_REOPEN_CONTAINMENT_ONLY',master_sha256=before,tool_sha256=sha(tool),print_release=False,flight_release=False)
try:
 objects=[o for o in b.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objects)==1;s=objects[0].Shape;wing=a.getObject('WING_R').Shape
 stage('reopen_validity');r.update(valid=s.isValid(),solids=len(s.Solids),faces=len(s.Faces),volume_mm3=s.Volume);assert r['valid'] and r['solids']==1
 stage('containment_cut_start');outside=s.cut(wing);stage('containment_cut_returned',outside_volume_mm3=outside.Volume);r.update(outside_volume_mm3=outside.Volume,contained_within_1e_6_mm3=outside.Volume<=1e-6)
except Exception as err:r['status']='FUSED_VOID_REOPEN_CHECK_FAILED';r['error_type']=type(err).__name__;r['error']=str(err);stage('exception',error=str(err))
finally:App.closeDocument(b.Name);App.closeDocument(a.Name)
assert sha(master)==before and sha(tool)==r['tool_sha256'];r['elapsed_seconds']=time.time()-start;r['limits']=['Only saved fused void tool Y180..440; root and tip excluded.','No boundary clearance, wing subtraction, whole-shell or structural/printing qualification.'];out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))
