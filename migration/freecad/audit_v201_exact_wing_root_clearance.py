import FreeCAD as App, Part, json, pathlib, math
R=pathlib.Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model")
d=App.openDocument(str(R/'migration/freecad/F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'))
w=d.getObject('WING_R').Shape; y=148.8263775443693
xs=[490,492,496,500,504.346,508,512,516,520]
# v201 target rail used proxies:
proxy={490:-4.85,492:-5.03,496:-5.25,500:-5.45,504.346:-5.742,508:-5.85,512:-5.95,516:-6.05,520:-6.10}
rows=[]
for x in xs:
 line=Part.makeLine(App.Vector(x,y,-100),App.Vector(x,y,100)); sec=w.section(line); zs=sorted(set(round(v.Point.z,9) for v in sec.Vertexes))
 if len(zs)>=2:
  zlo,zhi=zs[0],zs[-1]
 elif zs:
  zlo=zhi=zs[0]
 else:
  zlo=zhi=None
 target=proxy[x]
 rows.append({'x_mm':x,'wing_intersections_z_mm':zs,'exact_lower_z_mm':zlo,'v201_outer_target_z_mm':target,'exact_clearance_mm':(zlo-target) if zlo is not None else None})
vals=[r['exact_clearance_mm'] for r in rows if r['exact_clearance_mm'] is not None]
out={'status':'V201_EXACT_WING_ROOT_CLEARANCE_AUDIT','rows':rows,'clearance_range_mm':[min(vals),max(vals)] if vals else None,'minimum_clearance_mm':min(vals) if vals else None,'passes_1mm_target':min(vals)>=0.95 if vals else False,'gates':{'exact_section_screen':True,'absolute_Z_verified':False,'production_OML':False}}
(R/'migration/freecad/freecad_v201_exact_wing_root_clearance_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
