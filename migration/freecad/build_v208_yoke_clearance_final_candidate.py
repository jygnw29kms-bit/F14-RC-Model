import FreeCAD as App,Part,json,hashlib
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad");src=BASE/'F14_v207_YOKE_TRAY_CLEARANCE_OPTIMIZED.FCStd';out=BASE/'F14_v208_YOKE_CLEARANCE_FINAL_CANDIDATE.FCStd'
d=App.openDocument(str(src))
for n in ['V207_SYNC_YOKE_20','V207_YOKE_MOTION_BBOX_REF']:
 if d.getObject(n):d.removeObject(n)
x20=471.21391879567443;xmin=443.4060396423778;xmax=x20;z0=2.5;z1=10.5
profile=[(-68,8),(-31,8),(-27,5),(-19,5),(-15,8),(15,8),(19,5),(27,5),(31,8),(68,8)]
pts=[App.Vector(x20+w,y,z0) for y,w in profile]+[App.Vector(x20-w,y,z0) for y,w in reversed(profile)];sh=Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(App.Vector(0,0,z1-z0));sh=sh.cut(Part.makeBox(5,13,8.4,App.Vector(x20-2.5,7,z0-.2)))
for yy in [65,-65]:sh=sh.cut(Part.makeCylinder(1.65,z1-z0+.4,App.Vector(x20,yy,z0-.2)))
o=d.addObject('PartDesign::Feature','V208_SYNC_YOKE_20');o.Label='v208 waisted sync yoke @20deg / z2.5..10.5';o.Shape=sh
env=Part.makeBox((xmax-xmin)+16,136,z1-z0,App.Vector(xmin-8,-68,z0));e=d.addObject('PartDesign::Feature','V208_YOKE_MOTION_BBOX_REF');e.Label='v208 yoke motion bbox ref / not solid';e.Shape=env
m=d.addObject('App::FeaturePython','V208_META');m.Label='v208 yoke clearance final candidate';m.addProperty('App::PropertyString','Status','Gate');m.Status='CLEARANCE CANDIDATE / MATERIAL NOT RELEASED';m.addProperty('App::PropertyBool','ProductionRelease','Gate');m.ProductionRelease=False
d.recompute();d.saveAs(str(out));a={'status':'V208_YOKE_CLEARANCE_FINAL_CANDIDATE','yoke_z_mm':[z0,z1],'thickness_mm':8,'neck_width_mm':10,'normal_width_mm':16,'gates':{'dynamic_clearance_verified':False,'strength_screened':False,'material_verified':False,'print_release':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(BASE/'freecad_v208_yoke_clearance_final_candidate_audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
