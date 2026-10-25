import FreeCAD as App, FreeCADGui as Gui
p=r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v214_CURRENT_ENDMODEL_DEVELOPMENT_STATE.FCStd"
d=App.openDocument(p)
for o in d.Objects:
    if hasattr(o,'ViewObject') and o.ViewObject:
        o.ViewObject.Visibility=True
        n=o.Name
        if n.startswith('WING_'): o.ViewObject.ShapeColor=(0.93,0.55,0.12); o.ViewObject.Transparency=8
        elif n.startswith('V204_'): o.ViewObject.ShapeColor=(0.82,0.30,0.12); o.ViewObject.Transparency=10
        elif n.startswith('V210_') or n.startswith('V209_'): o.ViewObject.ShapeColor=(0.85,0.85,0.20); o.ViewObject.Transparency=0
        elif n.startswith('BATTERY_TRAY'): o.ViewObject.ShapeColor=(0.30,0.75,0.95); o.ViewObject.Transparency=15
        elif n.startswith('V211_'): o.ViewObject.ShapeColor=(0.55,0.85,0.35); o.ViewObject.Transparency=10
        elif n.startswith('V212_'): o.ViewObject.ShapeColor=(0.75,0.35,0.85); o.ViewObject.Transparency=10
        elif n.startswith('V203_GLOVE'): o.ViewObject.ShapeColor=(0.25,0.80,0.70); o.ViewObject.Transparency=30
        elif n=='FUSELAGE_CURRENT': o.ViewObject.ShapeColor=(0.70,0.70,0.72); o.ViewObject.Transparency=55
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
out=r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/docs/images/F14_v214_CURRENT_ENDMODEL_20261025.png"
Gui.activeDocument().activeView().saveImage(out,1920,1080,'Current')
