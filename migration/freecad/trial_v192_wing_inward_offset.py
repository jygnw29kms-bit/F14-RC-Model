"""Isolated offset feasibility trial; 0.4 mm is a numerical experiment, not design thickness."""
from pathlib import Path
import FreeCAD as App,json,hashlib,time
R=Path(__file__).resolve().parents[2];source=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';out=R/'analysis/v192_wing_inward_offset_feasibility.json';assert not out.exists()
before=hashlib.sha256(source.read_bytes()).hexdigest();doc=App.openDocument(str(source));start=time.time()
report=dict(status='INWARD_OFFSET_FEASIBILITY_ONLY',source_sha256=before,object='WING_R',trial_offset_mm=-0.4,production_release=False,flight_release=False)
try:
 wing=doc.getObject('WING_R').Shape.copy();report['source_valid']=wing.isValid()
 inner=wing.makeOffsetShape(-0.4,0.00001,False,False,0,0,False)
 report.update(offset_valid=inner.isValid(),offset_solids=len(inner.Solids),offset_volume_mm3=inner.Volume,source_volume_mm3=wing.Volume)
 if inner.isValid() and len(inner.Solids)==1 and 0<inner.Volume<wing.Volume:
  outside=inner.cut(wing).Volume;report['cavity_outside_reference_volume_mm3']=outside
  shell=wing.cut(inner);report.update(shell_valid=shell.isValid(),shell_solids=len(shell.Solids),shell_volume_mm3=shell.Volume)
  if shell.isValid() and len(shell.Solids)==1 and outside<1e-6:
   trial=App.newDocument('WING_R_OFFSET_FEASIBILITY_ONLY');obj=trial.addObject('PartDesign::Feature','UNRELEASED_WING_R_OFFSET_TRIAL');obj.Shape=shell
   path=R/'migration/freecad/WING_R_OFFSET_FEASIBILITY_ONLY.FCStd';assert not path.exists();trial.recompute();trial.saveAs(str(path));App.closeDocument(trial.Name);report['trial_fcstd_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
except Exception as err:report['error']=str(err);report['status']='OFFSET_TRIAL_FAILED_NO_SHELL_RELEASE'
finally:App.closeDocument(doc.Name)
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
report['elapsed_seconds']=time.time()-start
report['limits']=['Numerical feasibility trial only; no chosen structural wall thickness.','No spar, rib, joint, root load path, opening or print segmentation added.','No normal-thickness field, mesh, slicer or physical test verified.','Current reference OML registration remains unverified; master not modified.']
out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
