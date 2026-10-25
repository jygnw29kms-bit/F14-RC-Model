import FreeCAD as App, Part, json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v204_STRUCTURAL_WINGBOX_CANDIDATE.FCStd")
d=App.openDocument(str(p)); fus=d.getObject('FUSELAGE_CURRENT').Shape
xs=[482.346,488.346,496.346,504.346,512.346,520.346,526.346]
ys=[105.209,115.0,125.209,130.826,137.209]
rows=[]
for x in xs:
 for y in ys:
  edge=Part.makeLine(App.Vector(x,y,-40),App.Vector(x,y,60)); sec=fus.section(edge)
  zs=sorted(set(round(v.Point.z,6) for v in sec.Vertexes))
  rows.append({'x':x,'y':y,'z_intersections':zs,'lower_z':zs[0] if zs else None,'pad_bottom_z':-12.5,'contained_bottom':(zs and -12.5>=zs[0])})
res={'status':'V204_PAD_VERTICAL_MAP','rows':rows,'outside_samples':[r for r in rows if r['lower_z'] is not None and not r['contained_bottom']]}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v204_pad_vertical_map_audit.json").write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps(res,indent=2))
