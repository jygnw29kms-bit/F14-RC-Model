"""Reopen verified void tool; subtract locally without updating master."""
from pathlib import Path
import FreeCAD as App,json,hashlib,time
R=Path(__file__).resolve().parents[2];source=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';tool=R/'migration/freecad/WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd';prior=json.loads((R/'analysis/v192_fused_void_reopen_containment.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source)==prior['master_sha256'] and sha(tool)==prior['tool_sha256']
out=R/'analysis/v192_adaptive_partial_span_subtraction.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
a=App.openDocument(str(source));b=App.openDocument(str(tool));r=dict(status='ADAPTIVE_PARTIAL_SPAN_SUBTRACTION_TRIAL_ONLY',source_sha256=sha(source),cavity_tool_sha256=sha(tool),print_release=False,flight_release=False)
try:
 wing=a.getObject('WING_R').Shape;objects=[o for o in b.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objects)==1;cavity=objects[0].Shape
 stage('tool_reopen_validity');r.update(tool_valid=cavity.isValid(),tool_solids=len(cavity.Solids),tool_volume_mm3=cavity.Volume);assert r['tool_valid'] and r['tool_solids']==1
 stage('subtraction_start');result=wing.cut(cavity);stage('subtraction_returned',faces=len(result.Faces))
 stage('result_validity_start');valid=result.isValid();stage('result_validity_done',valid=valid)
 r.update(result_valid=valid,result_solids=len(result.Solids),result_volume_mm3=result.Volume,source_volume_mm3=wing.Volume,volume_balance_residual_mm3=wing.Volume-cavity.Volume-result.Volume)
 if valid and len(result.Solids)==1:
  path=R/'migration/freecad/WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd';assert not path.exists();trial=App.newDocument('ADAPTIVE_PARTIAL_SPAN_WING_TRIAL');obj=trial.addObject('PartDesign::Feature','UNRELEASED_PARTIAL_SPAN_HOLLOW_WING_R');obj.Shape=result;trial.recompute();stage('save_start');trial.saveAs(str(path));App.closeDocument(trial.Name);r['trial_sha256']=sha(path);stage('save_done')
except Exception as err:r['error']=str(err);r['status']='LOCAL_COMPENSATED_SUBTRACTION_FAILED';stage('exception',error=str(err))
finally:App.closeDocument(b.Name);App.closeDocument(a.Name)
assert sha(source)==r['source_sha256'] and sha(tool)==r['cavity_tool_sha256'];r['elapsed_seconds']=time.time()-start
r['limits']=['Void tool covers Y180..440 only; root and tip remain solid. Not a complete wing shell.','0.43 mm planar inset is numerical experiment, not structural wall selection.','Whole partial-span boundary distance has not been checked; local distance studies cannot be extrapolated.','No ribs, joints, spars, slicer, physical testing or whole-model release.']
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))

