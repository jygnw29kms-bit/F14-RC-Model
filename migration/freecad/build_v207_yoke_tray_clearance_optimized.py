import FreeCAD as App,Part,json,hashlib
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad");src=BASE/'F14_v206_BATTERY_TRAY_SERVO_CLEARANCE.FCStd';out=BASE/'F14_v207_YOKE_TRAY_CLEARANCE_OPTIMIZED.FCStd'
d=App.openDocument(str(src))
for n in ['BATTERY_TRAY_v206','V205_SYNC_YOKE_20','V205_YOKE_MOTION_ENVELOPE']:
 if d.getObject(n):d.removeObject(n)
zbase=2.407593065391325
def box(x0,x1,y0,y1,z0,z1):return Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0))
# tray optimized
p=[]
for s in [-1,1]:
 ya,yb=sorted([s*19,s*23]);p.append(box(242,437,ya,yb,zbase,zbase+10))
for s in [-1,1]:
 ya,yb=sorted([s*10,s*18]);p.append(box(242,432,ya,yb,zbase,zbase+2))
for x in [246,340,430]:p.append(box(x-2,x+2,-23,23,zbase,zbase+2))
# front hardpoints unchanged; rear asymmetric aft edge 437.1 to preserve 4.0mm ligament after pin edge 433.1
for s in [-1,1]:p.append(box(242,256,s*23-4,s*23+4,zbase,zbase+17))
for s in [-1,1]:p.append(box(424,437.1,s*23-4,s*23+4,zbase,zbase+17))
tray=p[0]
for sh in p[1:]:tray=tray.fuse(sh)
for x in [249,259,269,279,289,299,309,319,329,339,349,359,369,379,389,399,409,419,431]:tray=tray.cut(Part.makeCylinder(2.1,48,App.Vector(x,-24,7.407593065391325),App.Vector(0,1,0)))
for x in [249,431]:
 for s in [-1,1]:
  ya,yb=sorted([s*20,s*28]);tray=tray.cut(Part.makeCylinder(1.65,yb-ya,App.Vector(x,ya,15.407593065391325),App.Vector(0,1,0)))
o=d.addObject('PartDesign::Feature','BATTERY_TRAY_v207');o.Label='v207 tray / yoke clearance / retention preserved';o.Shape=tray
# waisted yoke polygon in XY centered at 20deg x
x20=471.21391879567443;z0=3.;z1=11.
# half widths: 8mm generally, taper to 5mm around +/-19..27 hardpoint bands
profile=[(-68,8),(-31,8),(-27,5),(-19,5),(-15,8),(15,8),(19,5),(27,5),(31,8),(68,8)]
pts=[App.Vector(x20+w,y,z0) for y,w in profile]+[App.Vector(x20-w,y,z0) for y,w in reversed(profile)]
wire=Part.makePolygon(pts+[pts[0]]);face=Part.Face(wire);yoke=face.extrude(App.Vector(0,0,z1-z0))
# scotch slot and rod pin holes
slot=box(x20-2.5,x20+2.5,7,20,z0-.2,z1+.2);yoke=yoke.cut(slot)
for yy in [65,-65]:yoke=yoke.cut(Part.makeCylinder(1.65,z1-z0+.4,App.Vector(x20,yy,z0-.2)))
yo=d.addObject('PartDesign::Feature','V207_SYNC_YOKE_20');yo.Label='v207 waisted 10mm-neck x 8mm-thick sync yoke @20deg';yo.Shape=yoke
# conservative motion bounding envelope with 10mm neck clearance documented separately; display only
xmin=443.4060396423778;xmax=471.21391879567443
env=box(xmin-8,xmax+8,-68,68,z0,z1);eo=d.addObject('PartDesign::Feature','V207_YOKE_MOTION_BBOX_REF');eo.Label='v207 yoke motion bbox reference / NOT physical solid';eo.Shape=env
m=d.addObject('App::FeaturePython','V207_META');m.Label='v207 yoke/tray clearance optimization'
for n,v in [('Status','PACKAGING OPTIMIZED / NOT RELEASED'),('YokeMaterialIntent','G10/CF laminate or metal; not PETG/ASA load path')]:m.addProperty('App::PropertyString',n,'Gate');setattr(m,n,v)
for n,v in [('RetentionPinsPreserved',True),('RearLigament4mm',True),('ProductionRelease',False)]:m.addProperty('App::PropertyBool',n,'Gate');setattr(m,n,v)
d.recompute();d.saveAs(str(out))
a={'status':'V207_YOKE_TRAY_CLEARANCE_OPTIMIZED','tray':{'rail_aft_x_mm':437,'rear_hardpoint_x':[424,437.1],'rear_stop_pin_x':431,'rear_stop_ligament_mm':437.1-(431+2.1)},'yoke':{'z':[3,11],'thickness_mm':8,'normal_width_x_mm':16,'neck_width_x_mm':10,'neck_y_bands_abs_mm':[19,27],'motion_center_x':[xmin,xmax]},'gates':{'battery_retention_geometry_preserved':True,'yoke_tray_dynamic_clearance_verified':False,'yoke_strength_screened':False,'material_verified':False,'print_release':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(BASE/'freecad_v207_yoke_tray_clearance_optimized_audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
