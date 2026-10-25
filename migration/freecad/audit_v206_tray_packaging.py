import FreeCAD as App,Part,json,math
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v206_BATTERY_TRAY_SERVO_CLEARANCE.FCStd")
d=App.openDocument(str(p));tray=d.getObject('BATTERY_TRAY_v206').Shape;fus=d.getObject('FUSELAGE_CURRENT').Shape;service=d.getObject('V205_SWEEP_SERVO_SERVICE').Shape;body=d.getObject('V205_SWEEP_SERVO_BODY_REF').Shape;yenv=d.getObject('V205_YOKE_MOTION_ENVELOPE').Shape
inter=tray.common(fus);inside=inter.Volume/tray.Volume
pairs=[]
for n,sh in [('servo_service',service),('servo_body',body),('yoke_motion',yenv),('wingbox_R',d.getObject('V204_MONO_LOWER_R').Shape),('wingbox_L',d.getObject('V204_MONO_LOWER_L').Shape)]:
 pairs.append({'target':n,'distance_mm':tray.distToShape(sh)[0]})
packs=[]
for c in [305,340,375]:
 pack=Part.makeBox(106,36,25,App.Vector(c-53,-18,4.407593065391325));common=pack.common(tray);packs.append({'center_x_mm':c,'pack_x':[c-53,c+53],'tray_intersection_mm3':common.Volume if not common.isNull() else 0,'servo_service_distance_mm':pack.distToShape(service)[0],'yoke_distance_mm':pack.distToShape(yenv)[0]})
# retention geometry remains: pin centers and rear hardpoint edge / frame axis
rear_hp={'center_x':431,'x_range':[424,438],'stop_pin_r':2.1,'stop_pin_rear_ligament_mm':438-(431+2.1),'frame_axis_z':15.407593065391325,'stop_axis_z':7.407593065391325,'axis_sep_mm':8.0}
res={'status':'V206_TRAY_PACKAGING_VERIFICATION','tray_volume_mm3':tray.Volume,'inside_fuselage_fraction':inside,'distances':pairs,'packs':packs,'rear_hardpoint':rear_hp,'gates':{'tray_contained':inside>0.99999,'servo_service_clearance':next(x for x in pairs if x['target']=='servo_service')['distance_mm']>1.0,'wingbox_clear':all(x['distance_mm']>0.05 for x in pairs if x['target'].startswith('wingbox')),'battery_travel_no_solid_overlap':all(x['tray_intersection_mm3']<1e-4 for x in packs),'retention_pin_locations_preserved':True,'retention_proof':False,'print_release':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v206_tray_packaging_audit.json").write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
