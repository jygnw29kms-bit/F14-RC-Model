import FreeCAD as App,Part,json,hashlib
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad");src=BASE/'F14_v205_SYNCHRONIZED_SWEEP_CANDIDATE.FCStd';out=BASE/'F14_v206_BATTERY_TRAY_SERVO_CLEARANCE.FCStd'
d=App.openDocument(str(src))
if d.getObject('BATTERY_TRAY_v165'):d.removeObject('BATTERY_TRAY_v165')
zbase=2.407593065391325; floor_t=2.; rail_h=10.; rail_y0=19.;rail_y1=23.;floor_yc=14.; floor_w=8.
def box(x0,x1,y0,y1,z0,z1):return Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0))
p=[]
# outer rails preserve full original length 242..438
for s in [-1,1]:
 ya,yb=sorted([s*rail_y0,s*rail_y1]);p.append(box(242,438,ya,yb,zbase,zbase+rail_h))
# inner floor strips stop at 432 to clear servo-service x433.31
for s in [-1,1]:
 ya,yb=sorted([s*(floor_yc-floor_w/2),s*(floor_yc+floor_w/2)]);p.append(box(242,432,ya,yb,zbase,zbase+floor_t))
# crossbars: aft moved 434 -> 430
for x in [246,340,430]:p.append(box(x-2,x+2,-23,23,zbase,zbase+2))
# terminal hardpoints unchanged x249,431, outboard y +/-23, 14x8x17
for x in [249,431]:
 for s in [-1,1]:p.append(box(x-7,x+7,s*23-4,s*23+4,zbase,zbase+17))
tray=p[0]
for sh in p[1:]:tray=tray.fuse(sh)
# stop holes unchanged
for x in [249,259,269,279,289,299,309,319,329,339,349,359,369,379,389,399,409,419,431]:
 hole=Part.makeCylinder(2.1,48,App.Vector(x,-24,7.407593065391325),App.Vector(0,1,0));tray=tray.cut(hole)
# M3 frame holes at terminal pads
for x in [249,431]:
 for s in [-1,1]:
  ya,yb=sorted([s*20,s*28]);hole=Part.makeCylinder(1.65,yb-ya,App.Vector(x,ya,15.407593065391325),App.Vector(0,1,0));tray=tray.cut(hole)
o=d.addObject('PartDesign::Feature','BATTERY_TRAY_v206');o.Label='v206 battery tray / 70mm travel / servo-clearance';o.Shape=tray
m=d.addObject('App::FeaturePython','V206_META');m.Label='v206 battery tray servo-clearance revision'
for n,v in [('Status','RETENTION GEOMETRY PRESERVED / NOT RELEASED'),('Change','rear crossbar 434->430; floor strips end 432; rails/hardpoints unchanged')]:m.addProperty('App::PropertyString',n,'Gate');setattr(m,n,v)
for n,v in [('RetentionPinsUnchanged',True),('BatteryCentersUnchanged',True),('ProductionRelease',False)]:m.addProperty('App::PropertyBool',n,'Gate');setattr(m,n,v)
d.recompute();d.saveAs(str(out))
a={'status':'V206_BATTERY_TRAY_SERVO_CLEARANCE','changes':{'rear_crossbar_x_mm':[434,430],'floor_strip_aft_x_mm':[438,432],'rail_aft_x_mm':438,'rear_hardpoint_x_mm':431,'retention_holes_unchanged':True},'gates':{'70mm_travel_geometry_preserved':True,'retention_pin_index_preserved':True,'servo_clearance_verified':False,'containment_verified':False,'retention_proof':False,'print_release':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(BASE/'freecad_v206_battery_tray_servo_clearance_audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
