import FreeCAD as App, Part, json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v204_STRUCTURAL_WINGBOX_CANDIDATE.FCStd")
d=App.openDocument(str(p)); servo=d.getObject('SWEEP_SERVO_SERVICE_REF').Shape
rows=[]
for c in [305,340,375]:
 pack=Part.makeBox(106,36,25,App.Vector(c-53,-18,4.407593065391325))
 dist=pack.distToShape(servo)[0]; inter=pack.common(servo); vol=inter.Volume if not inter.isNull() else 0
 rows.append({'center_x_mm':c,'pack_x':[c-53,c+53],'distance_mm':dist,'intersection_mm3':vol})
res={'status':'V205_BATTERY_SERVO_ALL_POSITIONS','rows':rows,'all_clear':all(r['distance_mm']>0.05 for r in rows)}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v205_battery_servo_positions_audit.json").write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps(res,indent=2))
