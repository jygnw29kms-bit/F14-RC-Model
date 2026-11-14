"""Build separate adjacent void tools from interval plan; no fusion/subtraction/release."""
from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];source=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';planpath=R/'analysis/v192_combined_adaptive_interval_plan.json';plan=json.loads(planpath.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(source)==plan['source_sha256']
out=R/'analysis/v192_adaptive_void_segments_build.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
d=App.openDocument(str(source));rows=[];cache={};shapes=[]
try:
 wing=d.getObject('WING_R').Shape
 def wire(y):
  if y not in cache:
   ws=wing.slice(App.Vector(0,1,0),y);assert len(ws)==1,'source section count'
   off=ws[0].makeOffset2D(-.43,0,False,False,False);assert len(off.Wires)==1,'offset count';cache[y]=off.Wires[0]
  return cache[y]
 for i,interval in enumerate(plan['intervals']):
  a,b=interval['y_start'],interval['y_end'];stage('segment_start',index=i,a=a,b=b)
  s=Part.makeLoft([wire(a),wire(b)],True,True);valid=s.isValid();bounds=[s.BoundBox.YMin,s.BoundBox.YMax]
  assert valid and len(s.Solids)==1,'invalid segment'
  assert abs(bounds[0]-a)<1e-6 and abs(bounds[1]-b)<1e-6,'span overshoot'
  rows.append(dict(index=i,y_start=a,y_end=b,valid=valid,solids=len(s.Solids),faces=len(s.Faces),volume_mm3=s.Volume,y_bounds_mm=bounds));shapes.append(s);stage('segment_done',index=i)
 path=R/'migration/freecad/WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd';assert not path.exists();trial=App.newDocument('UNRELEASED_ADAPTIVE_VOID_TOOLS')
 for row,s in zip(rows,shapes):
  obj=trial.addObject('PartDesign::Feature','VOID_TOOL_'+str(row['index']));obj.Shape=s;obj.addProperty('App::PropertyBool','PrintRelease');obj.PrintRelease=False
 trial.recompute();stage('save_start');trial.saveAs(str(path));App.closeDocument(trial.Name);stage('save_done')
 result=dict(status='SEPARATE_ADAPTIVE_VOID_TOOLS_ONLY_NOT_WING_SHELL',source_sha256=sha(source),plan_sha256=sha(planpath),output_sha256=sha(path),rows=rows,sum_segment_volumes_mm3=sum(r['volume_mm3'] for r in rows),elapsed_seconds=time.time()-start,limits=['17 separate adjacent void solids; not fused into one cavity.','Interval Y bounds verified; no whole-body containment or 3D clearance checked here.','Y180..440 only; root and tip excluded.','Not print parts, not a wing shell; no subtraction, joints, ribs or structural qualification.'],print_release=False,flight_release=False)
except Exception as err:result=dict(status='ADAPTIVE_VOID_BUILD_FAILED',rows=rows,error_type=type(err).__name__,error=str(err),source_sha256=sha(source),print_release=False,flight_release=False);stage('exception',error=str(err))
finally:App.closeDocument(d.Name)
assert sha(source)==plan['source_sha256'];out.write_text(json.dumps(result,indent=2)+'\n');stage('complete');print(json.dumps({'status':result['status'],'segments':len(rows)}))
