import FreeCAD as App,Part,json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v210_A80BHSF_M4_MECHANISM.FCStd")
d=App.openDocument(str(p));fus=d.getObject('FUSELAGE_CURRENT').Shape
fixed=[]
for n in ['BATTERY_TRAY_v207','V205_SWEEP_SERVO_SERVICE','V208_YOKE_MOTION_BBOX_REF','V204_MONO_LOWER_R','V204_MONO_LOWER_L','INLET_EDF_R','INLET_EDF_L']:
 o=d.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull(): fixed.append((n,o.Shape))
bats=[('BAT305',Part.makeBox(106,36,25,App.Vector(252,-18,4.407593065391325))),('BAT340',Part.makeBox(106,36,25,App.Vector(287,-18,4.407593065391325))),('BAT375',Part.makeBox(106,36,25,App.Vector(322,-18,4.407593065391325)))]
cands=[(300,50,45),(330,50,45),(360,50,45),(300,-50,45),(330,-50,45),(360,-50,45),(330,60,45),(330,-60,45),(300,50,55),(360,50,55)]
rows=[]
for cen in cands:
 xc,yc,zc=cen;sh=Part.makeBox(55,25,12,App.Vector(xc-27.5,yc-12.5,zc-6));inter=sh.common(fus);frac=inter.Volume/sh.Volume
 ds={n:sh.distToShape(t)[0] for n,t in fixed};ds.update({n:sh.distToShape(t)[0] for n,t in bats})
 rows.append({'center':cen,'inside_fraction':frac,'minimum_distance_mm':min(ds.values()),'distances':ds})
rows.sort(key=lambda r:(r['inside_fraction']>=.999,r['minimum_distance_mm']),reverse=True);res={'status':'V211_UBEC_SHORTLIST','rows':rows,'best':rows[0]};Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v211_ubec_shortlist.json").write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
