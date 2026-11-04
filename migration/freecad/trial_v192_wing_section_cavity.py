"""Partial-span cavity trial, not a complete wing shell or approved thickness."""
from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];source=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(source.read_bytes()).hexdigest();out=R/'analysis/v192_wing_section_cavity_trial.json';assert not out.exists()
d=App.openDocument(str(source));start=time.time();r=dict(status='PARTIAL_SPAN_CAVITY_FEASIBILITY_ONLY',source_sha256=before,station_y_mm=[180,220,260,300,340,380,420,440],planar_inset_mm=0.4,print_release=False,flight_release=False)
try:
 wing=d.getObject('WING_R').Shape.copy();wires=[]
 for y in r['station_y_mm']:
  section=wing.slice(App.Vector(0,1,0),y);assert len(section)==1
  inset=section[0].makeOffset2D(-0.4,0,False,False,False);assert len(inset.Wires)==1
  wires.append(inset.Wires[0])
 cavity=Part.makeLoft(wires,True,True);r.update(cavity_valid=cavity.isValid(),cavity_solids=len(cavity.Solids),cavity_volume_mm3=cavity.Volume)
 assert cavity.isValid() and len(cavity.Solids)==1
 outside=cavity.cut(wing);r['cavity_outside_reference_volume_mm3']=outside.Volume
 r['containment_volume_tolerance_mm3']=1e-6
 if outside.Volume<=1e-6:
  hollow=wing.cut(cavity);r.update(result_valid=hollow.isValid(),result_solids=len(hollow.Solids),result_volume_mm3=hollow.Volume,source_volume_mm3=wing.Volume)
  if hollow.isValid() and len(hollow.Solids)==1:
   trial=App.newDocument('PARTIAL_WING_CAVITY_TRIAL');o=trial.addObject('PartDesign::Feature','UNRELEASED_PARTIAL_CAVITY_WING_R');o.Shape=hollow
   p=R/'migration/freecad/WING_R_PARTIAL_CAVITY_TRIAL_ONLY.FCStd';assert not p.exists();trial.recompute();trial.saveAs(str(p));App.closeDocument(trial.Name);r['trial_fcstd_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
 else:r['status']='PARTIAL_CAVITY_PROTRUDES_NO_SHELL_OUTPUT'
except Exception as err:r['error']=str(err);r['status']='PARTIAL_CAVITY_TRIAL_FAILED'
finally:App.closeDocument(d.Name)
assert before==hashlib.sha256(source.read_bytes()).hexdigest();r['elapsed_seconds']=time.time()-start
r['limits']=['Only Y180..440 mm cavity; root and tip remain solid.','Ruled planar inset loft is not a uniform normal offset.','No rib/spar/joint/load-path design, opening, segmentation, slicer or physical test.','OML registration and whole-aircraft mass/flight qualification remain open; master unchanged.']
out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps(r))
