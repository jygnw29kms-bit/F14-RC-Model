import FreeCAD as App, FreeCADGui as Gui
from pathlib import Path
p=Path(r'C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\migration\freecad\F14_CURRENT_TOTAL_PROGRESS_v204.FCStd')
out=Path(r'C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\docs\images\F14_CURRENT_TOTAL_PROGRESS_v204_20261025.png')
d=App.openDocument(str(p)); Gui.activeDocument().activeView().setAnimationEnabled(False)
for o in d.Objects:
    vo=getattr(o,'ViewObject',None)
    if not vo: continue
    try: vo.Visibility=True
    except: pass
    n=o.Name.upper(); lab=getattr(o,'Label','').upper()
    try:
        vo.DisplayMode='Flat Lines'
        vo.LineWidth=1.5
        if 'FUSELAGE' in n or 'OUTER_AIRFRAME' in n:
            vo.ShapeColor=(0.65,0.65,0.68); vo.Transparency=72
        elif 'WING_R' in n or 'WING_L' in n:
            vo.ShapeColor=(0.95,0.48,0.12); vo.Transparency=15; vo.LineWidth=2.0
        elif 'TOTAL_V204' in n or '[STRUCT]' in lab:
            vo.ShapeColor=(0.90,0.12,0.12); vo.Transparency=0; vo.LineWidth=2.5
        elif 'BATTERY' in n:
            vo.ShapeColor=(0.20,0.80,0.25); vo.Transparency=10
        elif 'EDF' in n or 'INLET' in n:
            vo.ShapeColor=(0.20,0.45,0.95); vo.Transparency=20
        elif 'LINKAGE' in n or 'SLIDER' in n or 'CRANK' in n or 'ROD_' in n or 'SERVO' in n:
            vo.ShapeColor=(0.95,0.78,0.12); vo.Transparency=10; vo.LineWidth=2.0
        elif 'GLOVE' in n or 'CLEARANCE' in n:
            vo.ShapeColor=(0.85,0.15,0.75); vo.Transparency=20; vo.LineWidth=2.0
        else:
            vo.ShapeColor=(0.72,0.72,0.72); vo.Transparency=55
    except: pass
v=Gui.activeDocument().activeView(); v.viewAxonometric(); v.fitAll();
try: v.saveImage(str(out),1920,1080,'White')
except: v.saveImage(str(out),1920,1080,'Current')
print('SAVED',out)
