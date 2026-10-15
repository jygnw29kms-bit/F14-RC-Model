import FreeCAD as App, json, os
p=r'C:/Users/dezen/Desktop/F14-RC-Model/migration/freecad/F14_CURRENT_FULL_VIEW_v190.FCStd'
d=App.openDocument(p)
rows=[]
for o in d.Objects:
    s=getattr(o,'Shape',None)
    if not s or s.isNull(): continue
    b=s.BoundBox
    if o.Name.startswith(('FUSELAGE','WING_','STABILATOR_','VTAIL_','VENTRAL_','INLET_EDF_','WINGBOX_REF','PIVOT_REF','BATTERY_','STAB_')):
        rows.append({'name':o.Name,'label':o.Label,'bounds':{'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]},'center':[b.Center.x,b.Center.y,b.Center.z]})
print(json.dumps(rows,indent=2))
