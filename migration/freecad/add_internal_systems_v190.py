import FreeCAD as App, Part, os, json
base=os.path.dirname(os.path.abspath(__file__))
src=os.path.join(base,'F14_CURRENT_FULL_VIEW.FCStd')
out=os.path.join(base,'F14_CURRENT_FULL_VIEW_v190.FCStd')
audit_path=os.path.join(base,'freecad_v190_internal_systems_audit.json')
d=App.openDocument(src)

def feat(name,label,shape):
    o=d.getObject(name) or d.addObject('PartDesign::Feature',name)
    o.Label=label
    o.Shape=shape
    return o

def box_center(cx,cy,cz,dx,dy,dz):
    return Part.makeBox(dx,dy,dz,App.Vector(cx-dx/2,cy-dy/2,cz-dz/2))

def cyl_y(cx,y0,cz,r,length,sign=1):
    return Part.makeCylinder(r,length,App.Vector(cx,y0,cz),App.Vector(0,sign,0))

# Battery tray v165: native construction from checked dimensions.
x0,x1=242.0,438.0
parts=[]
for y0 in (19.0,-23.0):
    parts.append(Part.makeBox(x1-x0,4.0,10.0,App.Vector(x0,y0,190.0)))
for cy in (14.0,-14.0):
    parts.append(box_center((x0+x1)/2,cy,191.0,x1-x0,8.0,2.0))
for cx in (246.0,340.0,434.0):
    parts.append(box_center(cx,0,191.0,4.0,46.0,2.0))
for cx in (249.0,431.0):
    for cy in (23.0,-23.0):
        parts.append(box_center(cx,cy,198.5,14.0,8.0,17.0))
tray=parts[0]
for s in parts[1:]: tray=tray.fuse(s)
feat('BATTERY_TRAY_v165','Battery tray v165 candidate',tray)
# Reference battery envelope at nominal center station.
feat('BATTERY_REFERENCE_PACK','4S reference battery 106x36x25 @ x340',box_center(340.0,0,204.5,106.0,36.0,25.0))
# Retention-hole references only; not cutting until hardware/process freeze.
holes=[]
for cx in [249,259,269,279,289,299,309,319,329,339,349,359,369,379,389,399,409,419,431]:
    holes.append(cyl_y(float(cx),-24.0,195.0,2.1,48.0,1))
refholes=holes[0]
for s in holes[1:]: refholes=refholes.fuse(s)
feat('BATTERY_RETENTION_HOLE_REFS','Battery stop-pin hole references v165',refholes)

# Stabilator hardware v177/v180 and servo packaging v181.
pivot_x=736.0078983334656
for side,sgn in [('R',1),('L',-1)]:
    # 6 mm shaft, inboard to outboard. Candidate axis at z=0.
    shaft=cyl_y(pivot_x,sgn*45.0,0.0,3.0,66.0,sgn)
    feat('STAB_SHAFT_'+side,'Stabilator 6mm shaft '+side+' v177',shaft)
    # two 13x5 bearings and 17 mm printed housing envelopes.
    for idx,ay in enumerate((52.5,72.5),1):
        ystart=sgn*(ay-2.5)
        bearing=cyl_y(pivot_x,ystart,0.0,6.5,5.0,sgn)
        bore=cyl_y(pivot_x,ystart,0.0,3.0,5.0,sgn)
        bearing=bearing.cut(bore)
        feat('STAB_BEARING_%s_%d'%(side,idx),'Stabilator bearing '+side+' '+str(idx)+' v177',bearing)
        housing=cyl_y(pivot_x,ystart,0.0,8.5,5.0,sgn).cut(cyl_y(pivot_x,ystart,0.0,6.5,5.0,sgn))
        feat('STAB_HOUSING_%s_%d'%(side,idx),'Printed bearing housing '+side+' '+str(idx),housing)
    # Crank candidate, radial disc at abs y 78; 4 mm thick.
    y0=sgn*(78.0-2.0)
    crank=cyl_y(pivot_x,y0,0.0,18.9,4.0,sgn).cut(cyl_y(pivot_x,y0,0.0,3.05,4.0,sgn))
    feat('STAB_CRANK_'+side,'Stabilator crank '+side+' r18.9 v180',crank)
    # Selected servo service envelope v181.
    feat('STAB_SERVO_ENV_'+side,'TORQ TCM-1022 service envelope '+side+' v181',box_center(700.0,sgn*60.0,0.0,27.0,31.5,16.0))

# Organize groups without changing geometry.
for gname,label,names in [
 ('GRP_BATTERY','Battery / CG candidates',['BATTERY_TRAY_v165','BATTERY_REFERENCE_PACK','BATTERY_RETENTION_HOLE_REFS']),
 ('GRP_STABILATOR_HW','Stabilator mechanism candidates',[o.Name for o in d.Objects if o.Name.startswith('STAB_')])]:
    g=d.getObject(gname) or d.addObject('App::DocumentObjectGroup',gname); g.Label=label
    for n in names:
        o=d.getObject(n)
        if o and o not in g.Group: g.addObject(o)

d.recompute(); d.saveAs(out)
# Numeric audit.
rows=[]
for n in ['BATTERY_TRAY_v165','BATTERY_REFERENCE_PACK','STAB_SERVO_ENV_R','STAB_SERVO_ENV_L','STAB_SHAFT_R','STAB_SHAFT_L','STAB_CRANK_R','STAB_CRANK_L']:
    o=d.getObject(n); b=o.Shape.BoundBox
    rows.append({'name':n,'valid':o.Shape.isValid(),'solids':len(o.Shape.Solids),'volume_mm3':o.Shape.Volume,'bounds_mm':{'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]}})
audit={'status':'FREECAD_V190_INTERNAL_SYSTEMS_PORT','source_full_view':src,'output_fcstd':out,'objects':rows,'battery_geometry_basis':'Fusion v165 section inputs','stabilator_geometry_basis':'Fusion v177/v180 section inputs plus v181 selected servo package','retention_holes_reference_only':True,'servo_actual_unit_measured':False,'hardware_frozen':False,'print_release':False,'flight_release':False}
with open(audit_path,'w',encoding='utf-8') as f: json.dump(audit,f,indent=2)
print(json.dumps(audit,indent=2))
