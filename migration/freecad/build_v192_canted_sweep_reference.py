"""Separate calibrated canted-axis sweep reference; not production assembly."""
from pathlib import Path
import FreeCAD as App,Part,json,hashlib,math
R=Path(__file__).resolve().parents[2];source=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';calpath=R/'analysis/v192_canted_axis_LE_direction_calibration.json';cal=json.loads(calpath.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(source);path=R/'migration/freecad/CANTED_AXIS_SWEEP_REFERENCE_STUDY_ONLY.FCStd';out=R/'analysis/v192_canted_sweep_reference_build.json';assert not path.exists() and not out.exists()
a=App.openDocument(str(source));trial=App.newDocument('CANTED_AXIS_SWEEP_REFERENCE_ONLY');rows=[]
try:
 for side,sign in (('R',1),('L',-1)):
  pivot=App.Vector(613.1323905812828,sign*125.20927023775282,0);axis=App.Vector(0,sign*math.sin(math.radians(1.5)),math.cos(math.radians(1.5)))
  line=trial.addObject('PartDesign::Feature','PROVISIONAL_AXIS_'+side);line.Shape=Part.makeLine(pivot-axis*20,pivot+axis*20)
  for nominal in (20,40,68):
   case=next(x for x in cal['rows'] if x['nominal_label_deg']==nominal);shape=a.getObject('WING_'+side).Shape.copy();baseline=shape.Volume;shape.rotate(pivot,axis,sign*case['calibrated_rotation_deg']);assert shape.isValid() and len(shape.Solids)==1 and abs(shape.Volume-baseline)<1e-5
   obj=trial.addObject('PartDesign::Feature','REFERENCE_WING_'+side+'_NOMINAL_'+str(nominal));obj.Shape=shape;obj.addProperty('App::PropertyString','AxisPointStatus');obj.AxisPointStatus='PROVISIONAL_LOCAL_Z0_NOT_VERIFIED_PIVOT_WL';obj.addProperty('App::PropertyBool','PrintRelease');obj.PrintRelease=False
   b=shape.BoundBox;rows.append(dict(object=obj.Name,side=side,nominal_label_deg=nominal,rotation_deg=sign*case['calibrated_rotation_deg'],bounds_mm={k:[getattr(b,k+'Min'),getattr(b,k+'Max')] for k in ('X','Y','Z')},valid=True,volume_mm3=shape.Volume))
 for nominal in (20,40,68):
  rr=next(x for x in rows if x['side']=='R' and x['nominal_label_deg']==nominal)['bounds_mm'];ll=next(x for x in rows if x['side']=='L' and x['nominal_label_deg']==nominal)['bounds_mm']
  assert max([abs(rr[k][i]-ll[k][i]) for k in ('X','Z') for i in (0,1)]+[abs(rr['Y'][0]+ll['Y'][1]),abs(rr['Y'][1]+ll['Y'][0])])<1e-5
 trial.recompute();trial.saveAs(str(path))
finally:App.closeDocument(trial.Name);App.closeDocument(a.Name)
assert sha(source)==before
r=dict(status='SEPARATE_CANTED_SWEEP_REFERENCE_ONLY',source_sha256=before,calibration_sha256=sha(calpath),output_sha256=sha(path),rows=rows,limits=['Six overlapping reference poses, not six physical wings or a production assembly.','Direction calibrated only from source root-tip LE line; provisional axis point Z0 and cant-plane interpretation remain assumptions.','No original glove registration, body collision, mechanical fit, load path or printing qualification.','Master unchanged; no automatic promotion of tilted axis.'],print_release=False,flight_release=False)
out.write_text(json.dumps(r,indent=2)+'\n');print('6 valid calibrated reference poses; bilateral bounds symmetric; separate file saved')
