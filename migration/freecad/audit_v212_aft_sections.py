import FreeCAD as App,Part,json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v211_SWEEP_POWER_BEC.FCStd")
d=App.openDocument(str(p));fus=d.getObject('FUSELAGE_CURRENT').Shape
rows=[]
for x in [620,650,680,700,720]:
 for y in [50,60,70,80,90,100,110,120]:
  edge=Part.makeLine(App.Vector(x,y,-80),App.Vector(x,y,100));sec=fus.section(edge);zs=sorted(set(round(v.Point.z,4) for v in sec.Vertexes));rows.append({'x':x,'y':y,'z':zs,'lower':zs[0] if zs else None,'upper':zs[-1] if zs else None,'height':zs[-1]-zs[0] if len(zs)>=2 else None})
res={'status':'V212_AFT_VERTICAL_SECTIONS','rows':rows};Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v212_aft_sections.json").write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
