"""Reopen verified void tool; subtract locally without updating master."""
from pathlib import Path
import FreeCAD as App,json,hashlib,time
R=Path(__file__).resolve().parents[2];source=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';tool=R/'migration/freecad/WING_R_COMPENSATED_LOCAL_CAVITY_TOOL_ONLY.FCStd';prior=json.loads((R/'analysis/v192_compensated_local_cavity_containment.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source)==prior['source_sha256'] and sha(tool)==prior['cavity_tool_sha256']
out=R/'analysis/v192_compensated_local_subtraction.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
a=App.openDocument(str(source));b=App.openDocument(str(tool));r=dict(status='REOPENED_TOOL_LOCAL_SUBTRACTION_TRIAL_ONLY',source_sha256=sha(source),cavity_tool_sha256=sha(tool),print_release=False,flight_release=False)
try:
 wing=a.getObject('WING_R').Shape;objects=[o for o in b.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objects)==1;cavity=objects[0].Shape
 stage('tool_reopen_validity');r.update(tool_valid=cavity.isValid(),tool_solids=len(cavity.Solids),tool_volume_mm3=cavity.Volume);assert r['tool_valid'] and r['tool_solids']==1
 stage('subtraction_start');result=wing.cut(cavity);stage('subtraction_returned',faces=len(result.Faces))
 stage('result_validity_start');valid=result.isValid();stage('result_validity_done',valid=valid)
 r.update(result_valid=valid,result_solids=len(result.Solids),result_volume_mm3=result.Volume,source_volume_mm3=wing.Volume,volume_balance_residual_mm3=wing.Volume-cavity.Volume-result.Volume)
 if valid and len(result.Solids)==1:
  path=R/'migration/freecad/WING_R_COMPENSATED_LOCAL_TRIAL_ONLY.FCStd';assert not path.exists();trial=App.newDocument('COMPENSATED_LOCAL_WING_TRIAL');obj=trial.addObject('PartDesign::Feature','UNRELEASED_LOCAL_CAVITY_WING_R');obj.Shape=result;trial.recompute();stage('save_start');trial.saveAs(str(path));App.closeDocument(trial.Name);r['trial_sha256']=sha(path);stage('save_done')
except Exception as err:r['error']=str(err);r['status']='LOCAL_COMPENSATED_SUBTRACTION_FAILED';stage('exception',error=str(err))
finally:App.closeDocument(b.Name);App.closeDocument(a.Name)
assert sha(source)==r['source_sha256'] and sha(tool)==r['cavity_tool_sha256'];r['elapsed_seconds']=time.time()-start
r['limits']=['Only 40 mm span cavity removed; most wing remains solid. Not a complete wing shell.','0.43 mm planar inset is numerical experiment, not structural wall selection.','Previous distance measurement is not a reopened-artifact wall qualification.','No ribs, joints, spars, slicer, physical testing or whole-model release.']
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))
