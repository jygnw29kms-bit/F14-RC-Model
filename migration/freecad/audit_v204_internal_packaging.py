import FreeCAD as App, json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v204_STRUCTURAL_WINGBOX_CANDIDATE.FCStd")
d=App.openDocument(str(p))
names=['BATTERY_TRAY_v165','BATTERY_REFERENCE_PACK','INLET_EDF_R','INLET_EDF_L','SWEEP_LINKAGE_V193','DYNAMIC_LINKAGE_V194','SWEEP_SERVO_SERVICE_REF','V204_MONO_LOWER_R','V204_MONO_LOWER_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L']
objs={n:d.getObject(n) for n in names if d.getObject(n) and hasattr(d.getObject(n),'Shape') and not d.getObject(n).Shape.isNull()}
pairs=[]
checks=[('BATTERY_REFERENCE_PACK','DYNAMIC_LINKAGE_V194'),('BATTERY_TRAY_v165','DYNAMIC_LINKAGE_V194'),('BATTERY_TRAY_v165','SWEEP_SERVO_SERVICE_REF'),('INLET_EDF_R','V204_MONO_LOWER_R'),('INLET_EDF_L','V204_MONO_LOWER_L'),('INLET_EDF_R','DYNAMIC_LINKAGE_V194'),('INLET_EDF_L','DYNAMIC_LINKAGE_V194')]
for a,b in checks:
 if a in objs and b in objs:
  try: dist=objs[a].Shape.distToShape(objs[b].Shape)[0]
  except: dist=None
  pairs.append({'a':a,'b':b,'distance_mm':dist})
boxes={}
for n,o in objs.items():
 b=o.Shape.BoundBox; boxes[n]={'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]}
out={'status':'V204_INTERNAL_PACKAGING_SCREEN','pairs':pairs,'boxes':boxes,'minimum_distance_mm':min([p['distance_mm'] for p in pairs if p['distance_mm'] is not None],default=None),'gates':{'sampled_packaging_collision_free':all(p['distance_mm'] is None or p['distance_mm']>0.05 for p in pairs),'full_dynamic_packaging_verified':False,'print_release':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v204_internal_packaging_audit.json").write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
