import FreeCAD as App, FreeCADGui as Gui, os
p=r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v196_GLOVE_TRANSITION_OVERLAY.FCStd"
d=App.openDocument(p); Gui.activeDocument().activeView().viewTop()
for o in d.Objects:
 if hasattr(o,'ViewObject') and o.ViewObject: o.ViewObject.Visibility=True
for o in d.Objects:
 n=o.Name
 if 'V195_FUSELAGE' in n:
  o.ViewObject.ShapeColor=(0.55,0.55,0.58); o.ViewObject.Transparency=35
 elif 'V195_WING' in n:
  o.ViewObject.ShapeColor=(0.95,0.62,0.12); o.ViewObject.Transparency=15
 elif 'GLOVE' in n:
  o.ViewObject.LineColor=(0.20,0.75,1.00); o.ViewObject.LineWidth=4.0
 elif 'TRANS_TRANSITION_RAIL' in n:
  o.ViewObject.LineColor=(0.20,1.00,0.35); o.ViewObject.LineWidth=6.0
 elif 'TRANS_DIRECT_CHORD' in n:
  o.ViewObject.LineColor=(1.00,0.25,0.25); o.ViewObject.LineWidth=2.0
 elif 'TARGET' in n or 'PIVOT' in n:
  try:o.ViewObject.LineColor=(1.00,1.00,0.15);o.ViewObject.LineWidth=4.0
  except:pass
Gui.activeDocument().activeView().fitAll()
out=r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/docs/images/F14_v196_GLOVE_TRANSITION_OVERLAY_20261025.png"
Gui.activeDocument().activeView().saveImage(out,1600,1000,'Current')
d.save()
