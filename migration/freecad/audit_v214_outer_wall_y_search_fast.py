import FreeCAD as App, Part, json, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); p=R/'migration/freecad/F14_v212_WINGBOX_UPPER_STRUCTURAL_DECK.FCStd'; out=R/'migration/freecad/freecad_v214_outer_wall_y_search_fast.json'
d=App.openDocument(str(p)); wing0=d.getObject('CTX_WING_R').Shape; px=504.3463093769572; py=125.20927023775282; x0=482.3463093769572; x1=526.3463093769572
rows=[]
for ywall in [147.8,146,144,142,140,139,138.5,138.25]:
 wall=Part.makeBox(x1-x0,1.5,27.0,App.Vector(x0,ywall-1.5,-13.5)); mind=999; worst=None
 for sw in range(20,69,4):
  sh=wing0.copy(); sh.rotate(App.Vector(px,py,0),App.Vector(0,0,1),-(sw-20.0)); dist=wall.distToShape(sh)[0]
  if dist<mind: mind=dist; worst={'sweep_deg':sw,'distance_mm':dist}
 rows.append({'outer_wall_y_mm':ywall,'minimum_distance_mm':mind,'worst':worst,'clear_of_fork_outer_mm':ywall-137.20927023775283})
valid=[r for r in rows if r['minimum_distance_mm']>=1.0 and r['clear_of_fork_outer_mm']>=1.0]
res={'status':'V214_OUTER_WALL_Y_SEARCH_FAST','sample_step_deg':4,'rows':rows,'best_outermost_passing':valid[0] if valid else None}
out.write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps(res,indent=2))