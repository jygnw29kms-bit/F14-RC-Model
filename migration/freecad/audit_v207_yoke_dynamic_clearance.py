import FreeCAD as App,Part,json,math
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v207_YOKE_TRAY_CLEARANCE_OPTIMIZED.FCStd")
d=App.openDocument(str(p));tray=d.getObject('BATTERY_TRAY_v207').Shape;service=d.getObject('V205_SWEEP_SERVO_SERVICE').Shape;body=d.getObject('V205_SWEEP_SERVO_BODY_REF').Shape
c=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_candidate23.json").read_text());DX=108.7860812043256
profile=[(-68,8),(-31,8),(-27,5),(-19,5),(-15,8),(15,8),(19,5),(27,5),(31,8),(68,8)]
def yoke(x):
 pts=[App.Vector(x+w,y,3) for y,w in profile]+[App.Vector(x-w,y,3) for y,w in reversed(profile)];wire=Part.makePolygon(pts+[pts[0]]);sh=Part.Face(wire).extrude(App.Vector(0,0,8));sh=sh.cut(Part.makeBox(5,13,8.4,App.Vector(x-2.5,7,2.8)))
 for yy in [65,-65]:sh=sh.cut(Part.makeCylinder(1.65,8.4,App.Vector(x,yy,2.8)))
 return sh
rows=[]
for s in c['samples']:
 x=s['slider_x_mm']-DX;sh=yoke(x)
 for name,target in [('tray',tray),('servo_service',service),('servo_body',body),('wingbox_R',d.getObject('V204_MONO_LOWER_R').Shape),('wingbox_L',d.getObject('V204_MONO_LOWER_L').Shape)]:rows.append({'sweep_deg':s['sweep_deg'],'x_mm':x,'target':name,'distance_mm':sh.distToShape(target)[0]})
crit=min(rows,key=lambda r:r['distance_mm']);res={'status':'V207_YOKE_DYNAMIC_CLEARANCE_2DEG','minimum':crit,'minimum_by_target':{t:min(r['distance_mm'] for r in rows if r['target']==t) for t in sorted(set(r['target'] for r in rows))},'all_clear_over_1mm':all(r['distance_mm']>1.0 for r in rows),'rows':rows,'gates':{'2deg_dynamic_clearance_verified':all(r['distance_mm']>1.0 for r in rows),'continuous_analytic_between_samples_verified':False,'material_verified':False,'print_release':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v207_yoke_dynamic_clearance_audit.json").write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='rows'},indent=2))
