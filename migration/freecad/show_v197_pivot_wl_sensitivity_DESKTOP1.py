import FreeCAD as App, FreeCADGui as Gui
p=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v197_PIVOT_WL_SENSITIVITY_REVIEW.FCStd'
d=App.openDocument(p)
for o in d.Objects:
    if hasattr(o,'ViewObject') and o.ViewObject: o.ViewObject.Visibility=True
    n=o.Name
    if n.startswith('CTX_'):
        o.ViewObject.ShapeColor=(0.55,0.55,0.58);o.ViewObject.Transparency=55
    elif n.startswith('BASE_2STATION_'):
        o.ViewObject.ShapeColor=(0.95,0.65,0.15);o.ViewObject.Transparency=25
    elif n.startswith('FIT8_'):
        o.ViewObject.ShapeColor=(0.20,0.75,1.00);o.ViewObject.Transparency=45
    elif n.startswith('FIT_OMIT2_'):
        o.ViewObject.ShapeColor=(0.90,0.25,0.25);o.ViewObject.Transparency=55
    elif n.startswith('PLANE_'):
        o.ViewObject.LineWidth=4.0
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
