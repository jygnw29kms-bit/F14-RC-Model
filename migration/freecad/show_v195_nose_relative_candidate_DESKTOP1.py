import FreeCAD as App, FreeCADGui as Gui, time
from pathlib import Path
p=Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\migration\freecad\F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd")
out=Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\docs\images\F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE_20261025.png")
doc=App.openDocument(str(p))
for o in doc.Objects:
    try:
        if hasattr(o,'Shape') and not o.Shape.isNull():
            o.ViewObject.Visibility=True
            try:o.ViewObject.DisplayMode='Flat Lines'
            except:pass
            n=o.Name
            if n in ('WING_R','WING_L') or 'PIVOT_REF' in n or 'WINGBOX_REF' in n:
                o.ViewObject.ShapeColor=(1.0,0.58,0.0); o.ViewObject.LineColor=(1.0,0.8,0.1)
            elif n.startswith('WING_') and 'SWEEP_' in n:
                o.ViewObject.ShapeColor=(0.9,0.55,0.15); o.ViewObject.Transparency=65
            elif 'SWEEP_' in n or n.startswith('V194_'):
                o.ViewObject.ShapeColor=(0.2,0.7,1.0); o.ViewObject.Transparency=25
            elif n=='FUSELAGE_CURRENT':
                o.ViewObject.ShapeColor=(0.72,0.72,0.72); o.ViewObject.Transparency=15
            else:
                o.ViewObject.ShapeColor=(0.62,0.62,0.62)
    except:pass
Gui.activeDocument().activeView().viewAxonometric(); Gui.activeDocument().activeView().fitAll(); Gui.updateGui(); time.sleep(1)
Gui.activeDocument().activeView().saveImage(str(out),1600,1000,'Current'); doc.save(); print('READY',out)
