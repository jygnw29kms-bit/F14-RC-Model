import FreeCAD as App, FreeCADGui as Gui
p=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_GESAMTSTAND_REVIEW.FCStd'
d=App.openDocument(p)
for o in d.Objects:
    try:
        o.ViewObject.Visibility=True
        n=o.Name
        if n.startswith('LEGACY_FULL_'):
            o.ViewObject.ShapeColor=(0.72,0.72,0.72); o.ViewObject.LineColor=(0.35,0.35,0.35); o.ViewObject.Transparency=78; o.ViewObject.LineWidth=1.0
        elif n.startswith('CURRENT_SURFACE_'):
            o.ViewObject.ShapeColor=(0.95,0.55,0.18); o.ViewObject.LineColor=(1.0,0.80,0.25); o.ViewObject.Transparency=12; o.ViewObject.LineWidth=2.0
        elif n.startswith('RADOME_GUIDES_'):
            o.ViewObject.ShapeColor=(1.0,0.2,0.2); o.ViewObject.LineColor=(1.0,0.2,0.2); o.ViewObject.LineWidth=4.0
        elif n.startswith('NOSE_GUIDES_'):
            o.ViewObject.ShapeColor=(0.2,1.0,0.3); o.ViewObject.LineColor=(0.2,1.0,0.3); o.ViewObject.LineWidth=4.0
        elif n.startswith('GLOVE_GUIDES_'):
            o.ViewObject.ShapeColor=(0.15,0.75,1.0); o.ViewObject.LineColor=(0.15,0.75,1.0); o.ViewObject.LineWidth=4.0
        elif n.startswith('NOSE_A_SENS_'):
            o.ViewObject.ShapeColor=(0.95,0.2,0.95); o.ViewObject.LineColor=(0.95,0.2,0.95); o.ViewObject.LineWidth=3.0
    except: pass
Gui.activeDocument().activeView().viewAxonometric(); Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/docs/images/F14_GESAMTSTAND_REVIEW_20261025.png',1920,1080,'Current')
