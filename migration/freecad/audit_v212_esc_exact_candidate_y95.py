import FreeCAD as App,Part,json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v211_SWEEP_POWER_BEC.FCStd")
d=App.openDocument(str(p));fus=d.getObject('FUSELAGE_CURRENT').Shape;rows=[]
for sign,lab in [(1,'R'),(-1,'L')]:
 sh=Part.makeBox(60,25,8,App.Vector(650,sign*95-12.5,21));c=sh.common(fus);frac=c.Volume/sh.Volume;edf=d.getObject('INLET_EDF_'+lab).Shape
 rows.append({'side':lab,'inside_fraction':frac,'edf_distance_mm':sh.distToShape(edf)[0]})
res={'status':'V212_ESC_EXACT_X680_Y95_Z25','rows':rows,'both_contained':all(r['inside_fraction']>.99999 for r in rows)};Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v212_esc_exact_y95.json").write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
