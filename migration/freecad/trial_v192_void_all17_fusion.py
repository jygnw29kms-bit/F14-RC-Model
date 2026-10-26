"""Fuse first four saved void tools only; no wing subtraction."""
from pathlib import Path
import FreeCAD as App,json,hashlib,time
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();build=json.loads((R/'analysis/v192_adaptive_void_segments_build.json').read_text());assert sha(src)==build['output_sha256'];out=R/'analysis/v192_void_all17_fusion.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
d=App.openDocument(str(src));r=dict(status='ALL17_VOID_TOOLS_FUSION_TRIAL_ONLY',input_sha256=sha(src),indices=list(range(17)),steps=[],print_release=False,flight_release=False)
try:
 shapes=[d.getObject('VOID_TOOL_'+str(i)).Shape.copy() for i in r['indices']];result=shapes[0];total=shapes[0].Volume
 for index,s in zip(r['indices'][1:],shapes[1:]):
  stage('fuse_start',index=index);result=result.fuse(s);stage('fuse_returned',index=index)
  stage('validity_start',index=index);valid=result.isValid();total+=s.Volume
  row=dict(through_index=index,valid=valid,solids=len(result.Solids),faces=len(result.Faces),volume_mm3=result.Volume,sum_input_volumes_mm3=total,volume_balance_residual_mm3=total-result.Volume);r['steps'].append(row);stage('step_done',**row)
  assert valid and len(result.Solids)==1,'fusion not one valid solid'
 path=R/'migration/freecad/WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd';assert not path.exists();trial=App.newDocument('UNRELEASED_VOID_ALL17');obj=trial.addObject('PartDesign::Feature','VOID_TOOL_ALL17_NOT_PRINT_PART');obj.Shape=result;trial.recompute();stage('save_start');trial.saveAs(str(path));App.closeDocument(trial.Name);r['output_sha256']=sha(path);stage('save_done')
except Exception as err:r['status']='VOID_GROUP_FUSION_NOT_ACCEPTED';r['error_type']=type(err).__name__;r['error']=str(err);stage('exception',error=str(err))
finally:App.closeDocument(d.Name)
assert sha(src)==r['input_sha256'];r['elapsed_seconds']=time.time()-start;r['limits']=['17 tools fused over Y180..440 only; root/tip excluded, not a wing shell.','Fusion boundary clearance and containment not independently checked here.','No wing subtraction, structural or print qualification; source tool file unchanged.']
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))

