import FreeCAD as App,json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v211_SWEEP_POWER_BEC.FCStd")
d=App.openDocument(str(p));names=['V210_SYNC_YOKE_M4_20','V210_CRANK_M4_R_20','V210_CRANK_M4_L_20','V209_ROD_R_20','V209_ROD_L_20','V204_MONO_LOWER_R','V204_MONO_LOWER_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L','BATTERY_TRAY_v207']
rows=[]
for n in names:
 o=d.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull():rows.append({'name':n,'volume_cm3':o.Shape.Volume/1000})
print(json.dumps(rows,indent=2));Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v213_current_geometry_volumes.json").write_text(json.dumps({'status':'V213_CURRENT_GEOMETRY_VOLUMES','rows':rows},indent=2))
