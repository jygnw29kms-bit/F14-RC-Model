import FreeCAD as App, Part, json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v204_STRUCTURAL_WINGBOX_CANDIDATE.FCStd")
d=App.openDocument(str(p)); fus=d.getObject('FUSELAGE_CURRENT').Shape
x=457.3099792190261
rows=[]
for y in [-70,-65,-50,-34,0,34,50,65,70]:
 edge=Part.makeLine(App.Vector(x,y,-80),App.Vector(x,y,100)); sec=fus.section(edge); zs=sorted(set(round(v.Point.z,6) for v in sec.Vertexes));rows.append({'x':x,'y':y,'z':zs,'lower':zs[0] if zs else None,'upper':zs[-1] if zs else None,'height':zs[-1]-zs[0] if len(zs)>=2 else None})
res={'status':'V205_SERVO_CROSS_SECTION','rows':rows};Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v205_servo_cross_section_audit.json").write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
