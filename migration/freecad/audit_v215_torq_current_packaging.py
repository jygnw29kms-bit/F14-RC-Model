import FreeCAD as App,Part,json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v214_CURRENT_ENDMODEL_DEVELOPMENT_STATE.FCStd")
d=App.openDocument(str(p));fus=d.getObject('FUSELAGE_CURRENT').Shape;rows=[]
for sign,lab in [(1,'R'),(-1,'L')]:
 # old v181 service envelope A_XL_ZW: 27 x 31.5 x16 at center 700,+/-60,0
 sh=Part.makeBox(27,31.5,16,App.Vector(700-13.5,sign*60-15.75,-8));c=sh.common(fus);frac=c.Volume/sh.Volume
 ds={}
 for n in ['INLET_EDF_R','INLET_EDF_L','V212_SKYWALKER50A_R','V212_SKYWALKER50A_L','V211_HOBBYWING_UBEC10A_HV','BATTERY_TRAY_v207','V205_SWEEP_SERVO_SERVICE']:
  o=d.getObject(n)
  if o and hasattr(o,'Shape') and not o.Shape.isNull():ds[n]=sh.distToShape(o.Shape)[0]
 rows.append({'side':lab,'inside_fraction':frac,'distances_mm':ds,'minimum_distance_mm':min(ds.values())})
res={'status':'V215_OLD_TORQ_POSITION_CURRENT_MODEL_SCREEN','old_center_mm':[700,60,0],'service_dims_mm':[27,31.5,16],'rows':rows,'passes':all(r['inside_fraction']>.99999 and r['minimum_distance_mm']>1 for r in rows)};Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v215_torq_current_packaging_audit.json").write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
