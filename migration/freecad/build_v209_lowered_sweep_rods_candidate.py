import FreeCAD as App,Part,json,hashlib
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad");src=BASE/'F14_v208_YOKE_CLEARANCE_FINAL_CANDIDATE.FCStd';out=BASE/'F14_v209_LOWERED_SWEEP_RODS_CANDIDATE.FCStd'
d=App.openDocument(str(src))
for n in ['V205_ROD_R_20','V205_ROD_L_20']:
 if d.getObject(n):d.removeObject(n)
DX=108.7860812043256;c=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_candidate23.json").read_text());s=c['samples'][0];x=s['slider_x_mm']-DX

def rod(a,b,r=2):
 va=App.Vector(*a);v=App.Vector(*b)-va;return Part.makeCylinder(r,v.Length,va,v.normalize())
for sign,lab in [(1,'R'),(-1,'L')]:
 cp=(s['crank_pin_mm'][0]-DX,sign*abs(s['crank_pin_mm'][1]));sl=(x,sign*c['slider_attach_y_mm'])
 sh=rod((cp[0],cp[1],7.0),(sl[0],sl[1],7.0));o=d.addObject('PartDesign::Feature',f'V209_ROD_{lab}_20');o.Label=f'v209 4mm sweep rod {lab} @20deg / z7.0';o.Shape=sh
m=d.addObject('App::FeaturePython','V209_META');m.Label='v209 lowered sweep rods';m.addProperty('App::PropertyString','Status','Gate');m.Status='ROD CLEARANCE CANDIDATE / NOT RELEASED';m.addProperty('App::PropertyBool','ProductionRelease','Gate');m.ProductionRelease=False
d.recompute();d.saveAs(str(out));a={'status':'V209_LOWERED_SWEEP_RODS_CANDIDATE','rod_center_z_old_mm':7.5,'rod_center_z_new_mm':7.0,'rod_diameter_mm':4.0,'gates':{'dynamic_clearance_verified':False,'material_verified':False,'print_release':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(BASE/'freecad_v209_lowered_sweep_rods_candidate_audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
