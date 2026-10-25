import FreeCAD as App, FreeCADGui as Gui
p=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v198_PIVOT_STATION_VERTICAL_CLEARANCE_REVIEW.FCStd'
d=App.openDocument(p)
for o in d.Objects:
 if hasattr(o,'ViewObject') and o.ViewObject:o.ViewObject.Visibility=True
 n=o.Name
 if n=='FUSELAGE_SECTION':o.ViewObject.LineColor=(0.75,0.75,0.78);o.ViewObject.LineWidth=4
 elif 'WING_BASE' in n:o.ViewObject.LineColor=(0.95,0.65,0.15);o.ViewObject.LineWidth=5
 elif 'WING_FIT8' in n:o.ViewObject.LineColor=(0.20,0.75,1.00);o.ViewObject.LineWidth=4
 elif 'WING_OMIT2' in n:o.ViewObject.LineColor=(0.95,0.25,0.25);o.ViewObject.LineWidth=4
 elif 'CRITICAL_LINE' in n:o.ViewObject.LineColor=(1.0,1.0,0.2);o.ViewObject.LineWidth=3
Gui.activeDocument().activeView().viewRear();Gui.activeDocument().activeView().fitAll()
