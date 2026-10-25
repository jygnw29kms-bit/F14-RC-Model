import FreeCAD as App, FreeCADGui as Gui, os
BASE=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'
path=os.path.join(BASE,'migration','freecad','F14_v195_GLOVE_TOP_OVERLAY.FCStd')
d=App.openDocument(path)
for o in d.Objects:
 try:
  if hasattr(o,'Shape') and not o.Shape.isNull(): o.ViewObject.Visibility=True
 except: pass
# colors
for n in ['FUSELAGE_CURRENT']:
 o=d.getObject(n)
 if o: o.ViewObject.ShapeColor=(0.65,0.65,0.68); o.ViewObject.Transparency=55
for n in ['WING_R','WING_L']:
 o=d.getObject(n)
 if o: o.ViewObject.ShapeColor=(1.0,0.65,0.05); o.ViewObject.Transparency=15
for o in d.Objects:
 if o.Name.startswith('GUIDE_'):
  o.ViewObject.LineColor=(0.2,0.8,1.0); o.ViewObject.LineWidth=5.0
 if o.Name.startswith('GAP_'):
  o.ViewObject.LineColor=(1.0,0.2,0.2); o.ViewObject.LineWidth=6.0
 if o.Name.startswith('PIVOT_CENTER_'):
  o.ViewObject.ShapeColor=(0.2,1.0,0.2)
Gui.activeDocument().activeView().viewTop()
Gui.activeDocument().activeView().fitAll()
out=os.path.join(BASE,'docs','images','F14_v195_GLOVE_TOP_OVERLAY_20261025.png')
Gui.activeDocument().activeView().saveImage(out,1600,1000,'Current')
