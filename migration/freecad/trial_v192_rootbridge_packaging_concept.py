"""Unfrozen root-bridge packaging concept from historical generic dimensions."""
from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(src.read_bytes()).hexdigest();out=R/'analysis/v192_rootbridge_concept_packaging.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
d=App.openDocument(str(src));r=dict(status='UNFROZEN_ROOTBRIDGE_PACKAGING_CONCEPT_ONLY',source_sha256=before,assumptions=dict(chord_mm=40,height_mm=16,boss_od_mm=24,nominal_pin_bore_mm=6,root_overlap_mm=10,hardware_selected=False,pivot_z_frozen=False),print_release=False,flight_release=False)
try:
 px,py=613.1323905812828,125.20927023775282;wing=d.getObject('WING_R').Shape;body=d.getObject('FUSELAGE_CURRENT').Shape;root=wing.BoundBox.YMin
 stage('build_concept');lug=Part.makeBox(40,root+10-py,16,App.Vector(px-20,py,-8));boss=Part.makeCylinder(12,16,App.Vector(px,py,-8));bore=Part.makeCylinder(3,20,App.Vector(px,py,-10));bridge=lug.fuse(boss).cut(bore)
 assert bridge.isValid() and len(bridge.Solids)==1;r.update(valid=True,solids=1,volume_mm3=bridge.Volume,root_y_mm=root)
 stage('root_contact_start');r['reference_wing_overlap_volume_mm3']=bridge.common(wing).Volume;stage('root_contact_done')
 rows=[]
 for sweep in (20,44,68):
  stage('packaging_start',sweep=sweep);b=bridge.copy();w=wing.copy()
  b.rotate(App.Vector(px,py,0),App.Vector(0,0,1),-(sweep-20));w.rotate(App.Vector(px,py,0),App.Vector(0,0,1),-(sweep-20))
  outside=b.cut(body).cut(w);rows.append(dict(sweep_deg=sweep,outside_current_body_or_moving_wing_volume_mm3=outside.Volume));stage('packaging_done',**rows[-1])
 r['packaging_samples']=rows;r['packaging_accepted_against_current_reference']=all(x['outside_current_body_or_moving_wing_volume_mm3']<=1e-6 for x in rows)
 path=R/'migration/freecad/ROOTBRIDGE_UNFROZEN_PACKAGING_CONCEPT_ONLY.FCStd';assert not path.exists();trial=App.newDocument('ROOTBRIDGE_UNFROZEN_CONCEPT');obj=trial.addObject('PartDesign::Feature','UNFROZEN_ROOTBRIDGE_NOT_PRINT_RELEASED');obj.Shape=bridge;trial.recompute();trial.saveAs(str(path));App.closeDocument(trial.Name);r['concept_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
except Exception as err:r['status']='ROOTBRIDGE_CONCEPT_TRIAL_FAILED';r['error_type']=type(err).__name__;r['error']=str(err);stage('exception',error=str(err))
finally:App.closeDocument(d.Name)
assert hashlib.sha256(src.read_bytes()).hexdigest()==before;r['elapsed_seconds']=time.time()-start;r['limits']=['Generic historical dimensions only; no actual pin/bearing/thrust-stack or material selected.','Overlap is geometric only, not a verified bond, hard contact or load-transfer design.','Three sweep samples against provisional current body/wing only; missing glove and original OML registration remain open.','No continuous sweep, stress, fatigue, print tolerance, physical proof or production integration.'];out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))
