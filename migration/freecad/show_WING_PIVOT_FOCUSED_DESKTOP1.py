import FreeCAD as App, FreeCADGui as Gui, time
from pathlib import Path
p=Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\migration\freecad\F14_WING_PIVOT_FOCUSED_REVIEW.FCStd")
out=Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\docs\images\F14_WING_PIVOT_FOCUSED_REVIEW_20261025.png")
doc=App.openDocument(str(p))
for o in doc.Objects:
    try:
        o.ViewObject.Visibility=True
        if hasattr(o,'Shape') and not o.Shape.isNull():
            o.ViewObject.DisplayMode='Flat Lines'
            if 'CORR' in o.Name or 'NADC' in o.Name:
                o.ViewObject.ShapeColor=(1.0,0.55,0.0); o.ViewObject.LineColor=(1.0,0.8,0.1)
            elif 'OLD' in o.Name:
                o.ViewObject.ShapeColor=(0.55,0.55,0.55); o.ViewObject.Transparency=55
            elif 'FUSELAGE' in o.Name:
                o.ViewObject.ShapeColor=(0.72,0.72,0.72); o.ViewObject.Transparency=20
            else:
                o.ViewObject.ShapeColor=(0.65,0.65,0.65)
    except: pass
Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()
Gui.updateGui(); time.sleep(1)
Gui.activeDocument().activeView().saveImage(str(out),1600,1000,'Current')
doc.recompute(); doc.save()
print('READY',len(doc.Objects),out)
