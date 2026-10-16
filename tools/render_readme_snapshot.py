import FreeCAD as App
import FreeCADGui as Gui
import os
repo=r'C:/Users/dezen/Desktop/F14-RC-Model'
fc=os.path.join(repo,'migration','freecad','F14_CURRENT_FULL_VIEW_v194_DYNAMIC_LINKAGE.FCStd')
out=os.path.join(repo,'docs','images','f14_freecad_current_20261016.png')
doc=App.openDocument(fc)
# Hide absolutely everything first.
for o in doc.Objects:
    try: o.ViewObject.Visibility=False
    except: pass
# Explicit leaf objects for the README view. No UPC/fuselage hull, no reference envelopes.
visible=[
 'WING_R','WING_L','STABILATOR_R','STABILATOR_L','VTAIL_R','VTAIL_L','VENTRAL_R','VENTRAL_L',
 'INLET_EDF_R','INLET_EDF_L','BATTERY_TRAY_v165',
 'STAB_SHAFT_R','STAB_SHAFT_L','STAB_BEARING_R_1','STAB_BEARING_R_2','STAB_BEARING_L_1','STAB_BEARING_L_2',
 'STAB_HOUSING_R_1','STAB_HOUSING_R_2','STAB_HOUSING_L_1','STAB_HOUSING_L_2','STAB_CRANK_R','STAB_CRANK_L',
 'SWEEP_SLIDER_R','SWEEP_SLIDER_L','V194_CRANK_R_44','V194_CRANK_L_44','V194_ROD_R_44','V194_ROD_L_44','V194_SLIDER_R_44','V194_SLIDER_L_44'
]
for name in visible:
    o=doc.getObject(name)
    if o:
        o.ViewObject.Visibility=True
        try:
            o.ViewObject.DisplayMode='Flat Lines'
            o.ViewObject.LineWidth=1.5
        except: pass
# Colors: airframe neutral, propulsion blue, mechanisms orange, battery green.
for name in ['WING_R','WING_L','STABILATOR_R','STABILATOR_L','VTAIL_R','VTAIL_L','VENTRAL_R','VENTRAL_L']:
    o=doc.getObject(name)
    if o: o.ViewObject.ShapeColor=(0.72,0.74,0.78)
for name in ['INLET_EDF_R','INLET_EDF_L']:
    o=doc.getObject(name)
    if o: o.ViewObject.ShapeColor=(0.20,0.52,0.88)
for name in ['BATTERY_TRAY_v165']:
    o=doc.getObject(name)
    if o: o.ViewObject.ShapeColor=(0.30,0.70,0.35)
for name in visible:
    if name.startswith('STAB_') or name.startswith('SWEEP_') or name.startswith('V194_'):
        o=doc.getObject(name)
        if o: o.ViewObject.ShapeColor=(0.95,0.55,0.18)
view=Gui.activeDocument().activeView()
try: view.setAnimationEnabled(False)
except: pass
view.viewAxonometric(); view.fitAll(); Gui.updateGui()
view.saveImage(out,1920,1080,'Current')
print('SAVED',out)
Gui.getMainWindow().close()
